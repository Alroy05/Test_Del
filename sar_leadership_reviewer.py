"""
Add the approving GISG Leadership user to the SAR "Reviewers" section.

When a SAR is approved (submit_id == "clearance_email_send" in
GenerateCombineSarTemplateAPIView), the approving user must appear in the
reviewer table on the SAR second page:

    1. Only if the approving user is GISG Leadership
       (Role.ROLE_TYPE_SECURITY_OFFICER).
    2. Only if that user is not already listed in the reviewers.
    3. If not listed, append the user's name and the approval date.

The reviewer list lives in SarTemplateJsonData (header_name =
"header_reviewer_second_page") as:

    {"reviewers": [{"id": <user id>, "reviewer": "<full name>", "date": "<iso date>"}, ...]}

publish_sar_on_leadership_approval() copies the *rendered HTML*
(SarTemplateData) into SarTemplateDataPdf, so after updating the JSON we
re-render that single section with refresh_sar_html() BEFORE publishing.
Otherwise the new reviewer would not appear in the published/downloaded SAR.
"""

from django.db import transaction
from django.utils import timezone

from app.models import SarTemplateJsonData
from app.models.role import Role
from app.models.sar_json_history_data import SarJsonHistoryData


@transaction.atomic
def add_leadership_reviewer_on_approval(request_details, user, user_type=None) -> bool:
    """
    Add the approving GISG Leadership user to the SAR reviewers, if missing.

    Returns True when a reviewer was added (and the section re-rendered),
    False when nothing had to change.
    """
    header_name = "header_reviewer_second_page"

    # 1) Only GISG Leadership approvals add a reviewer.
    effective_user_type = user_type if user_type is not None else user.user_type
    if effective_user_type != Role.ROLE_TYPE_SECURITY_OFFICER:
        return False

    user_name = user.get_full_name()
    if not user_name:
        return False

    # 2) Load the current reviewer list.
    reviewer_row = (
        SarTemplateJsonData.objects.select_for_update()
        .filter(
            request=request_details,
            header_name=header_name,
            is_active=1,
        )
        .order_by("-created_date")
        .first()
    )

    json_data = dict(reviewer_row.json_data or {}) if reviewer_row else {}
    reviewers = json_data.get("reviewers")
    reviewers = list(reviewers) if isinstance(reviewers, list) else []

    # 3) Skip if the user is already listed: same id, or (for entries typed
    #    manually in the SAR editor, which may have no id) the same full name,
    #    ignoring case and extra whitespace.
    normalized_user_name = " ".join(user_name.split()).casefold()
    for entry in reviewers:
        if not isinstance(entry, dict):
            continue

        entry_id = entry.get("id")
        if entry_id not in (None, "") and str(entry_id) == str(user.id):
            return False

        entry_name = " ".join(str(entry.get("reviewer") or "").split()).casefold()
        if entry_name == normalized_user_name:
            return False

    # 4) Append the user's name and the approval date.
    reviewers.append(
        {
            "id": user.id,
            "reviewer": user_name,
            "date": timezone.now().isoformat(),
        }
    )
    json_data["reviewers"] = reviewers

    # 5) Archive the previous JSON and save the new one (same pattern as
    #    _upsert_json_section / save_sar_form_data).
    section_status = SarTemplateJsonData.STATUS_VALUES.get("DRAFT", 1)
    if reviewer_row:
        section_status = reviewer_row.section_status
        SarJsonHistoryData.objects.create(
            original_id=reviewer_row.id,
            header_name=reviewer_row.header_name,
            json_data=reviewer_row.json_data,
            request=reviewer_row.request,
            created_by=reviewer_row.created_by,
            original_created_date=reviewer_row.created_date,
            archived_by=user,
        )
        reviewer_row.delete()

    SarTemplateJsonData.objects.create(
        header_name=header_name,
        json_data=json_data,
        request=request_details,
        section_status=section_status,
        needs_refresh=True,
        created_by=user,
        is_active=1,
    )

    # 6) Re-render only the reviewer section into SarTemplateData so that
    #    publish_sar_on_leadership_approval() copies the updated HTML.
    #    NOTE: adjust this import to the module where refresh_sar_html lives
    #    (the SAR service shown in Art5.py). Imported lazily, like Art4.py
    #    does, to avoid circular imports.
    from app.services.sar_service import refresh_sar_html

    result = refresh_sar_html(
        request_details,
        user,
        header_names=[header_name],
    )

    failed = (result or {}).get("failed_headers") or {}
    if header_name in failed:
        # Abort the surrounding transaction: approving without the reviewer
        # would publish a SAR that silently misses the approver.
        raise RuntimeError(
            f"Failed to render SAR reviewer section: {failed[header_name]}"
        )

    return True


# ---------------------------------------------------------------------------
# Integration: Art2.py -> GenerateCombineSarTemplateAPIView.post
# ---------------------------------------------------------------------------
#
# 1) Import at the top of the view module:
#
#     from app.services.sar_leadership_reviewer import add_leadership_reviewer_on_approval
#
# 2) In the `elif submit_id == "clearance_email_send":` branch, call it right
#    BEFORE publish_sar_on_leadership_approval(...) (still inside the existing
#    `with transaction.atomic():` block, so it rolls back with the approval):
#
#     elif submit_id == "clearance_email_send":
#         if user_type in [
#             Role.ROLE_TYPE_AU,
#             Role.ROLE_TYPE_SECURITY_OFFICER,
#         ]:
#             action_allowed = True
#
#             try:
#                 result = send_clearance_emails(
#                     request_obj, user, ato_status
#                 )
#                 ...  # unchanged error handling
#             except Exception as e:
#                 ...  # unchanged error handling
#
#             # NEW: add the approving GISG Leadership user to the reviewers
#             add_leadership_reviewer_on_approval(request_obj, user, user_type)
#
#             publish_sar_on_leadership_approval(request_obj, user)
