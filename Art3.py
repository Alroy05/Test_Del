"""
Migrate legacy HTML-based SARs (SarTemplateData) to JSON-based SARs
(SarTemplateJsonData).

Examples
--------
# Preview one SAR, print the JSON, check it renders through the ingestion pipeline
python manage.py migrate_sar_html_to_json --sgp-id SGP-1234 --dry-run --validate -v 2

# Dump what would be created for every un-migrated SAR, without writing
python manage.py migrate_sar_html_to_json --all --dry-run --output-dir /tmp/sar_json

# Migrate everything not yet migrated. created_by of each JSON section is the
# user who created the legacy HTML row; --user-email is only the fallback
# (default: the GSSR platform user) for rows without a resolvable author.
python manage.py migrate_sar_html_to_json --all --user-email admin@example.com

# Re-migrate one SAR, overwrite its JSON (old JSON archived), and re-render HTML
python manage.py migrate_sar_html_to_json --sgp-id SGP-1234 --force --refresh-html
"""

import json
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Value
from django.db.models.functions import Concat

from app.models import RequestorTeam, SarTemplateData, SarTemplateJsonData
from app.models.default_template_data import DefaultTemplateData
from app.models.sar_json_history_data import SarJsonHistoryData
from app.models.sar_template_data_history import SarTemplateDataHistory
from app.services.initialize_form_service import initialize_sar_sections
from app.services.sar_form_service import (
    INGESTION_FUNCTION_MAP,
    refresh_sar_html,
    render_header_html,
)
from app.crypto import hash_field
from app.constants import GSSR_USER_EMAIL
from app.management.commands.sar_html_json_migration import (
    LEGACY_HTML_SUPERSEDED_BY,
    SarParseContext,
    build_control_placeholder_index,
    build_migration_plan,
)


class Command(BaseCommand):
    help = (
        "Convert legacy HTML SAR sections (SarTemplateData) into JSON SAR "
        "sections (SarTemplateJsonData)."
    )

    # ------------------------------------------------------------------ args

    def add_arguments(self, parser):
        target = parser.add_mutually_exclusive_group(required=True)
        target.add_argument(
            "--sgp-id",
            action="append",
            dest="sgp_ids",
            help="SGP id to migrate. Repeat for several.",
        )
        target.add_argument(
            "--all",
            action="store_true",
            help=(
                "Every request with active HTML SAR rows. Requests that already "
                "have active JSON rows are skipped unless --force is given."
            ),
        )

        parser.add_argument("--limit", type=int, help="Process at most N requests.")
        parser.add_argument(
            "--user-id",
            help=(
                "Fallback user for created_by when the legacy HTML row has no "
                "(existing) author, and the user recorded as archived_by. "
                "Default: the GSSR platform user."
            ),
        )
        parser.add_argument("--user-email", help="Same as --user-id, by email.")

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report only; nothing is written.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help=(
                "Overwrite JSON sections that already exist (the old JSON is "
                "archived to SarJsonHistoryData). Without it, existing sections "
                "are left untouched."
            ),
        )
        parser.add_argument(
            "--validate",
            action="store_true",
            help=(
                "Render each JSON section through the ingestion functions "
                "(read-only) to confirm it is accepted."
            ),
        )
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Skip a SAR entirely if any section fails to parse or validate.",
        )
        parser.add_argument(
            "--skip-defaults",
            action="store_true",
            help=(
                "Do not create default JSON for sections missing from the legacy "
                "HTML (by default initialize_sar_sections fills them in)."
            ),
        )
        parser.add_argument(
            "--refresh-html",
            action="store_true",
            help=(
                "Mark migrated sections needs_refresh and re-render the HTML "
                "from the JSON via refresh_sar_html. Without it the existing "
                "HTML is left exactly as it is."
            ),
        )
        parser.add_argument(
            "--archive-legacy-html",
            action="store_true",
            help=(
                "With --refresh-html: move legacy-only HTML rows that the JSON "
                "now supersedes (header_3_4, header_7) to SarTemplateDataHistory."
            ),
        )
        parser.add_argument(
            "--output-dir",
            help="Write the extracted JSON for each SAR to <dir>/<sgp_id>.json.",
        )

    # ------------------------------------------------------------------ main

    def handle(self, *args, **options):
        if options["archive_legacy_html"] and not options["refresh_html"]:
            raise CommandError("--archive-legacy-html requires --refresh-html.")

        self.verbosity = options["verbosity"]
        # Platform user: created_by fallback, and the actor for archive rows /
        # HTML refresh. Required for writes, optional for dry runs.
        user = self._resolve_user(options, required=not options["dry_run"])

        output_dir = None
        if options["output_dir"]:
            output_dir = Path(options["output_dir"])
            output_dir.mkdir(parents=True, exist_ok=True)

        requests = self._get_requests(options)
        total = len(requests)

        if not total:
            self.stdout.write(self.style.WARNING("No SARs to migrate."))
            return

        mode = "DRY RUN" if options["dry_run"] else "MIGRATING"
        self.stdout.write(self.style.MIGRATE_HEADING(f"{mode}: {total} SAR(s)"))

        # The legacy controls template (is_active=3) is what ingest_header_3_2_json
        # renders old SARs with; use it to restore placeholder_text for controls
        # whose implementation text was already filled in.
        old_controls_template = (
            DefaultTemplateData.objects.filter(header_name="header_3_2", is_active=3)
            .order_by("-id")
            .values_list("header_data", flat=True)
            .first()
        )
        self.control_placeholders = build_control_placeholder_index(old_controls_template)
        if not old_controls_template:
            self.stdout.write(
                self.style.WARNING(
                    "No DefaultTemplateData(header_3_2, is_active=3) found; old-layout "
                    "controls will not render until it exists."
                )
            )

        totals = {"migrated": 0, "skipped": 0, "failed": 0, "with_warnings": 0}

        for index, request_details in enumerate(requests, start=1):
            prefix = f"[{index}/{total}] {request_details.sgp_id}"
            try:
                outcome = self._process_request(
                    request_details, user, options, output_dir, prefix
                )
            except Exception as exc:  # noqa: BLE001 - keep going with other SARs
                totals["failed"] += 1
                self.stdout.write(self.style.ERROR(f"{prefix}: FAILED - {exc}"))
                if self.verbosity >= 3:
                    import traceback
                    self.stdout.write(traceback.format_exc())
                continue

            totals[outcome["status"]] += 1
            if outcome["warnings"]:
                totals["with_warnings"] += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. migrated={totals['migrated']} skipped={totals['skipped']} "
                f"failed={totals['failed']} with_warnings={totals['with_warnings']}"
            )
        )

    # -------------------------------------------------------------- per SAR

    def _process_request(self, request_details, user, options, output_dir, prefix):
        legacy_rows, legacy_authors = self._latest_legacy_rows(request_details)

        if not legacy_rows:
            self.stdout.write(self.style.WARNING(f"{prefix}: no active HTML rows, skipped."))
            return {"status": "skipped", "warnings": False}

        ctx = SarParseContext.from_request(
            request_details,
            request_type_new=getattr(RequestorTeam, "REQUEST_TYPE_NEW", None),
            control_placeholders=self.control_placeholders,
        )
        plan = build_migration_plan(legacy_rows, ctx)
        self._link_reviewer_ids(plan)

        # created_by per JSON section = author of the legacy HTML row it came
        # from; sections without a source row (defaults, disabled header_5 /
        # addendum) get the SAR's author, i.e. who created its first HTML row.
        sar_author = legacy_authors.get("__sar__") or user
        # (sources read e.g. "header_3_4 (OLD controls)"; the first word is
        # the legacy header name.)
        section_authors = {
            header_name: legacy_authors.get(source.split(" ", 1)[0]) or sar_author
            for header_name, source in plan.sources.items()
        }

        validation_errors = {}
        if options["validate"]:
            validation_errors = self._validate(plan, request_details)

        if output_dir is not None:
            payload = {
                "sgp_id": request_details.sgp_id,
                **plan.as_dict(),
                "created_by": {
                    header_name: self._describe_user(author)
                    for header_name, author in section_authors.items()
                },
                "validation_errors": validation_errors,
            }
            (output_dir / f"{request_details.sgp_id}.json").write_text(
                json.dumps(payload, indent=2, default=str), encoding="utf-8"
            )

        self._report_plan(prefix, plan, validation_errors, section_authors, user)
        has_warnings = bool(plan.warnings or plan.errors or validation_errors)

        if options["strict"] and (plan.errors or validation_errors):
            self.stdout.write(
                self.style.ERROR(f"{prefix}: skipped (--strict, see errors above).")
            )
            return {"status": "skipped", "warnings": has_warnings}

        if options["dry_run"]:
            if self.verbosity >= 2:
                self.stdout.write(json.dumps(plan.sections, indent=2, default=str))
            return {"status": "migrated", "warnings": has_warnings}

        with transaction.atomic():
            written, kept = self._write_sections(
                request_details,
                plan.sections,
                section_authors,
                actor=user,
                force=options["force"],
                needs_refresh=options["refresh_html"],
            )

            defaults_created = []
            if not options["skip_defaults"]:
                before = set(self._active_json_headers(request_details))
                initialize_sar_sections(request_details, sar_author)
                defaults_created = sorted(
                    set(self._active_json_headers(request_details)) - before
                )

            refresh_result = None
            archived_legacy = []
            if options["refresh_html"]:
                refresh_result = refresh_sar_html(request_details, user)
                if options["archive_legacy_html"]:
                    archived_legacy = self._archive_superseded_html(
                        request_details, user, refresh_result
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"{prefix}: wrote {len(written)} section(s)"
                + (f", kept existing {len(kept)}" if kept else "")
                + (f", defaults {defaults_created}" if defaults_created else "")
            )
        )
        if kept and self.verbosity >= 2:
            self.stdout.write(f"    kept existing JSON (use --force to overwrite): {kept}")

        if refresh_result is not None:
            failed = refresh_result.get("failed_headers") or {}
            self.stdout.write(
                f"    refreshed HTML: {refresh_result.get('refreshed_headers')}"
            )
            for header_name, message in failed.items():
                self.stdout.write(self.style.ERROR(f"    render failed {header_name}: {message}"))
            if archived_legacy:
                self.stdout.write(f"    archived legacy HTML: {archived_legacy}")

        return {"status": "migrated", "warnings": has_warnings}

    # ---------------------------------------------------------------- reads

    def _get_requests(self, options):
        target_field = SarTemplateData._meta.get_field("request").target_field.attname

        if options["sgp_ids"]:
            queryset = RequestorTeam.objects.filter(sgp_id__in=options["sgp_ids"])
            found = set(queryset.values_list("sgp_id", flat=True))
            missing = [s for s in options["sgp_ids"] if s not in found]
            if missing:
                self.stdout.write(self.style.WARNING(f"Unknown SGP id(s): {missing}"))
        else:
            html_request_ids = (
                SarTemplateData.objects.filter(is_active=1)
                .values_list("request", flat=True)
                .distinct()
            )
            queryset = RequestorTeam.objects.filter(
                **{f"{target_field}__in": html_request_ids}
            )

            if not options["force"]:
                json_target = SarTemplateJsonData._meta.get_field(
                    "request"
                ).target_field.attname
                json_request_ids = (
                    SarTemplateJsonData.objects.filter(is_active=1)
                    .values_list("request", flat=True)
                    .distinct()
                )
                queryset = queryset.exclude(**{f"{json_target}__in": json_request_ids})

        queryset = queryset.order_by(target_field)
        if options["limit"]:
            queryset = queryset[: options["limit"]]
        return list(queryset)

    def _latest_legacy_rows(self, request_details):
        """
        Returns (html, authors):
          html    {legacy header: html of the latest active row}
          authors {legacy header: user who created that row,
                   "__sar__": user who created the SAR's earliest active row}
        Authors that are unset or no longer exist are left out, so callers
        fall back to the platform user.
        """
        rows = list(
            SarTemplateData.objects.filter(request=request_details, is_active=1)
            .order_by("header_name", "-created_date", "-id")
            .values_list("header_name", "header_data", "created_by_id", "created_date", "id")
        )
        latest, author_ids = {}, {}
        for header_name, header_data, created_by_id, _created, _id in rows:
            if header_name and header_name not in latest:
                latest[header_name] = header_data or ""
                if created_by_id:
                    author_ids[header_name] = created_by_id

        # Earliest row that has an author = who created the SAR.
        with_author = [row for row in rows if row[2]]
        if with_author:
            earliest = min(
                with_author,
                key=lambda row: (row[3] is None, row[3] if row[3] is not None else 0, row[4]),
            )
            author_ids["__sar__"] = earliest[2]

        users = get_user_model().objects.in_bulk(set(author_ids.values()))
        authors = {
            header_name: users[user_id]
            for header_name, user_id in author_ids.items()
            if user_id in users
        }
        return latest, authors

    def _active_json_headers(self, request_details):
        return SarTemplateJsonData.objects.filter(
            request=request_details, is_active=1
        ).values_list("header_name", flat=True)

    def _resolve_user(self, options, required=True):
        user_model = get_user_model()

        if options["user_id"]:
            user = user_model.objects.filter(
                pk=options["user_id"]
            ).first()

        elif options["user_email"]:
            user = user_model.objects.filter(
                email_hash=hash_field(options["user_email"])
            ).first()

        else:
            user = user_model.objects.filter(
                email_hash=hash_field(GSSR_USER_EMAIL)
            ).first()

        if user is None and not required:
            self.stdout.write(
                self.style.WARNING(
                    "Platform fallback user not found; sections without an HTML "
                    "author would get created_by=None."
                )
            )
            return None

        if user is None:
            raise CommandError(
                "Could not resolve the user to record as created_by. "
                "Verify GSSR_USER_EMAIL or pass --user-id/--user-email."
            )

        return user

    def _link_reviewer_ids(self, plan):
        """
        Give migrated reviewers the platform user's id when the name matches
        exactly one user, as add_leadership_reviewer_on_approval does, so the
        same person is not added twice on approval.
        """
        reviewers = (plan.sections.get("header_reviewer_second_page") or {}).get(
            "reviewers"
        ) or []
        if not reviewers:
            return

        user_model = get_user_model()
        for entry in reviewers:
            name = " ".join(str(entry.get("reviewer") or "").split())
            if not name:
                continue
            matches = list(
                user_model.objects.annotate(
                    _full_name=Concat("first_name", Value(" "), "last_name")
                )
                .filter(_full_name__iexact=name)
                .values_list("pk", flat=True)[:2]
            )
            if len(matches) == 1:
                entry["id"] = matches[0]

    @staticmethod
    def _describe_user(user):
        if user is None:
            return None
        return {"id": user.pk, "name": user.get_full_name()}

    # --------------------------------------------------------------- writes

    def _write_sections(self, request_details, sections, authors, actor, force, needs_refresh):
        """
        authors: {json header: user recorded as created_by}
        actor:   platform user recorded as archived_by.
        """
        existing_rows = {}
        for row in (
            SarTemplateJsonData.objects.select_for_update()
            .filter(request=request_details, is_active=1, header_name__in=sections.keys())
            .order_by("header_name", "-created_date")
        ):
            existing_rows.setdefault(row.header_name, []).append(row)

        written, kept = [], []

        for header_name, json_data in sections.items():
            rows = existing_rows.get(header_name, [])

            if rows and not force:
                kept.append(header_name)
                continue

            create_kwargs = {
                "header_name": header_name,
                "json_data": json_data,
                "request": request_details,
                "created_by": authors.get(header_name) or actor,
                "is_active": 1,
                "needs_refresh": needs_refresh,
            }
            if rows:
                create_kwargs["section_status"] = rows[0].section_status

            for row in rows:
                SarJsonHistoryData.objects.create(
                    original_id=row.id,
                    header_name=row.header_name,
                    json_data=row.json_data,
                    request=row.request,
                    created_by=row.created_by,
                    original_created_date=row.created_date,
                    archived_by=actor,
                )
                row.delete()

            SarTemplateJsonData.objects.create(**create_kwargs)
            written.append(header_name)

        return written, kept

    def _archive_superseded_html(self, request_details, user, refresh_result):
        refreshed = set(refresh_result.get("refreshed_headers") or [])
        archived = []

        for legacy_header, json_header in LEGACY_HTML_SUPERSEDED_BY.items():
            # header_5 may legitimately be "refreshed" as disabled (no HTML).
            if json_header not in refreshed:
                continue

            for row in SarTemplateData.objects.select_for_update().filter(
                request=request_details, header_name=legacy_header, is_active=1
            ):
                SarTemplateDataHistory.objects.create(
                    original_id=row.id,
                    header_name=row.header_name,
                    header_data=row.header_data,
                    request_id=row.request_id,
                    comment=row.comment,
                    created_by_id=row.created_by_id,
                    original_created_date=row.created_date,
                    archived_by_id=user.id,
                )
                row.delete()
                archived.append(legacy_header)

        return archived

    # ------------------------------------------------------------ reporting

    def _validate(self, plan, request_details):
        errors = {}
        for header_name, json_data in plan.sections.items():
            if header_name not in INGESTION_FUNCTION_MAP:
                continue
            try:
                render_header_html(
                    header_name=header_name,
                    json_data=json_data,
                    request_obj=request_details,
                )
            except Exception as exc:  # noqa: BLE001
                errors[header_name] = f"{type(exc).__name__}: {exc}"
        return errors

    def _report_plan(self, prefix, plan, validation_errors, section_authors=None, fallback=None):
        self.stdout.write(
            f"{prefix}: parsed {len(plan.sections)} section(s)"
            + (f", {len(plan.errors)} parse error(s)" if plan.errors else "")
            + (f", {len(validation_errors)} validation error(s)" if validation_errors else "")
        )

        if self.verbosity >= 2:
            section_authors = section_authors or {}
            for header_name, source in plan.sources.items():
                author = section_authors.get(header_name)
                if author is None:
                    by = "created_by=None"
                else:
                    by = f"created_by={author.get_full_name() or author.pk}"
                    if fallback is not None and author.pk == fallback.pk:
                        by += " (platform fallback)"
                self.stdout.write(f"    {source} -> {header_name}  [{by}]")

        for header_name, message in plan.errors.items():
            self.stdout.write(self.style.ERROR(f"    parse error {header_name}: {message}"))

        for header_name, message in validation_errors.items():
            self.stdout.write(self.style.ERROR(f"    validation {header_name}: {message}"))

        if self.verbosity >= 1:
            for header_name, messages in plan.warnings.items():
                for message in messages:
                    self.stdout.write(self.style.WARNING(f"    {header_name}: {message}"))

        if plan.unmapped_legacy_headers and self.verbosity >= 2:
            self.stdout.write(
                f"    legacy HTML not migrated (no JSON equivalent): "
                f"{plan.unmapped_legacy_headers}"
            )
