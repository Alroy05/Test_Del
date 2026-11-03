"""
Legacy SAR HTML -> JSON migration.

Reads the HTML stored in ``SarTemplateData.header_data`` for a request and
rebuilds the JSON documents that ``SarTemplateJsonData`` now stores, in the
exact shapes consumed by ``ingestion_service`` / ``initialize_form_service``.

Legacy HTML header  ->  JSON header
-----------------------------------
header_first_page             -> header_first_page
header_revision_second_page   -> header_revision_second_page
header_reviewer_second_page   -> header_reviewer_second_page
header_1 / 1_1 / 1_2 / 1_3 / 1_4 / 1_5 -> same names
header_2 / header_2_1         -> same names
header_3                      -> header_3
header_3_2 (testing overview) -> header_3_1   (events table)
header_3_4 (security controls)-> header_3_2   (old or new controls template,
                                                 picked per SAR, see below)
header_6   (POA&M)            -> header_4     ({})
header_7   (business consid.) -> header_5     (is_enabled / description)
header_support_team           -> header_support_team
addendum_header               -> addendum_header

Security controls: the controls catalogue changed while SARs were being
written, so a legacy SAR uses either CONTROLS_DICT_OLD (no ``is_new`` key) or
CONTROLS_DICT (``is_new: True``). The parser matches every HTML row against
both catalogues, picks the one that fits best, and emits the full catalogue in
template order with the values from the HTML filled in.

The parsers are pure functions (HTML in, dict out) so they can be unit
tested without a database.
"""

import copy
import hashlib
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from html import unescape
from typing import Callable, Optional
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup

from app.constants import CONTROLS_DICT, CONTROLS_DICT_OLD
from app.services.ingestion_service import (
    NEW_CATEGORY_TITLE_MAPPING,
    OLD_CATEGORY_TITLE_MAPPING,
    RISK_COLOR_MAP,
    STATUS_CONFIG,
    YES_NO_CONTROL_KEYS,
    YES_NO_STATUS_CONFIG,
)

DEFAULT_POLICY_URL = (
    "https://kieps.kpmg.com/spgip/#/doc/f8f79305-492a-ef11-86d4-002248206d19"
)

DEFAULT_HEADER_3_1_DESCRIPTION = (
    "In determining this solution's residual risk, the technology "
    "security and information management teams adjudicate each "
    "finding against the likely threat(s), the vulnerabilities "
    "severity and the potential impact. This section presents a "
    "summary of any outstanding high and medium risk items."
)

# Placeholder text that the legacy generator wrote when there was no input.
HEADER_1_2_PLACEHOLDERS = {
    "provide background information on the business case and the "
    "project/implementation's scope.",
}

# Legacy HTML headers that have no JSON equivalent. They are reported, not
# migrated.
KNOWN_UNMAPPED_LEGACY_HEADERS = {
    "header_1_1_1",
    "header_3_1",  # legacy "Activities" text (new header_3_1 is the events table)
    "header_3_3",
}

# Legacy HTML rows superseded by a differently named JSON section. Used by the
# command's --archive-legacy-html option.
LEGACY_HTML_SUPERSEDED_BY = {
    "header_3_4": "header_3_2",
    "header_7": "header_5",
}


# ---------------------------------------------------------------------------
# Context / result containers
# ---------------------------------------------------------------------------


@dataclass
class SarParseContext:
    """Request-level values used as fallbacks when the HTML is incomplete."""

    sgp_id: str = ""
    solution_name: str = ""
    overall_risk: Optional[str] = None
    go_live_date: Optional[date] = None
    apm_solution_id: str = ""
    is_editable: bool = True
    # (category, normalized requirement title) -> placeholder text, taken from
    # the default controls template. Fills placeholder_text for rows whose
    # implementation was already filled in (so the HTML no longer shows it).
    control_placeholders: dict = field(default_factory=dict)

    @classmethod
    def from_request(cls, request_details, request_type_new=None, control_placeholders=None):
        go_live = getattr(request_details, "go_live_date", None)
        if isinstance(go_live, datetime):
            go_live = go_live.date()

        request_type = getattr(request_details, "request_type", None)

        return cls(
            sgp_id=str(getattr(request_details, "sgp_id", "") or ""),
            solution_name=getattr(request_details, "solution_name", "") or "",
            overall_risk=getattr(request_details, "overall_risk", None) or None,
            go_live_date=go_live,
            apm_solution_id=str(
                getattr(request_details, "apm_solution_id", "") or ""
            ),
            is_editable=(
                request_type != request_type_new
                if request_type_new is not None
                else True
            ),
            control_placeholders=control_placeholders or {},
        )


@dataclass
class SarMigrationPlan:
    sections: dict = field(default_factory=dict)  # json header -> json_data
    sources: dict = field(default_factory=dict)  # json header -> legacy header
    warnings: dict = field(default_factory=dict)  # json header -> [str]
    errors: dict = field(default_factory=dict)  # json header -> str
    unmapped_legacy_headers: list = field(default_factory=list)

    def warn(self, header_name, message):
        self.warnings.setdefault(header_name, []).append(message)

    def as_dict(self):
        return {
            "sections": self.sections,
            "sources": self.sources,
            "warnings": self.warnings,
            "errors": self.errors,
            "unmapped_legacy_headers": self.unmapped_legacy_headers,
        }


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

BLOCK_TAGS = [
    "p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
    "li", "ul", "ol", "table", "tr",
]


def make_soup(html_content):
    html_content = html_content or ""
    # Same detection rule the ingestion service uses.
    if "&lt;" in html_content and "&gt;" in html_content:
        html_content = unescape(html_content)
    return BeautifulSoup(html_content, "html.parser")


def clean_text(value):
    return " ".join(str(value or "").replace("\xa0", " ").split())


def node_text(node):
    if node is None:
        return ""
    return clean_text(node.get_text(" ", strip=True))


def normalize_key(value):
    return clean_text(value).lower()


def element_paragraphs(element):
    """
    Return the text of ``element`` as a list of paragraphs.

    ``<br><br>`` and block-level children start new paragraphs, which is the
    inverse of how the ingestion service writes "\\n\\n"-separated text.
    """
    if element is None:
        return []

    element = copy.copy(element)

    for br in element.find_all("br"):
        br.replace_with("\n")

    for block in element.find_all(BLOCK_TAGS):
        block.insert_before("\n\n")
        block.insert_after("\n\n")

    text = element.get_text("").replace("\xa0", " ")

    return [
        clean_text(part)
        for part in re.split(r"\n[ \t\r]*\n", text)
        if clean_text(part)
    ]


def description_from_headings(soup, tag_name="h5", exclude_inside=("table",)):
    """Join the paragraphs of every <h5> (not nested in a table)."""
    paragraphs = []

    for heading in soup.find_all(tag_name):
        if exclude_inside and heading.find_parent(list(exclude_inside)):
            continue
        paragraphs.extend(element_paragraphs(heading))

    return "\n\n".join(paragraphs)


def strip_label(text, label):
    text = clean_text(text)
    if text.lower().startswith(label.lower()):
        text = text[len(label):]
    return text.strip()


def int_or_none(value):
    value = str(value or "").strip()
    return int(value) if value.isdigit() else None


def is_checked(input_tag):
    if input_tag is None or not input_tag.has_attr("checked"):
        return False
    return str(input_tag.get("checked")).strip().lower() not in {"false", "0"}


def slugify_key(value):
    return re.sub(r"[^a-z0-9]+", "_", clean_text(value).lower()).strip("_")


_DATE_FORMATS_WITH_DAY = (
    "%Y-%m-%d",
    "%B %d %Y",
    "%b %d %Y",
    "%d %B %Y",
    "%d %b %Y",
    "%d/%m/%Y",
    "%d-%m-%Y",
)
_DATE_FORMATS_MONTH_ONLY = ("%Y-%m", "%B %Y", "%b %Y")


def parse_loose_date(text):
    """
    Parse the human dates written by the legacy generator, e.g.
    "September 19th 2026", "September 05<sup>th</sup> 2026", "Sep 2026",
    "October 05, 2026", "2026-09-19T10:00:00Z".

    Returns ``(date, has_day)`` or ``(None, False)``.
    """
    value = clean_text(text)
    if not value:
        return None, False

    try:
        iso_value = value[:-1] + "+00:00" if value.endswith("Z") else value
        return datetime.fromisoformat(iso_value).date(), True
    except ValueError:
        pass

    value = re.sub(r"(\d{1,2})\s*(st|nd|rd|th)\b", r"\1", value, flags=re.I)
    value = re.sub(r"\bSept\b", "Sep", value, flags=re.I)
    value = clean_text(value.replace(",", " "))

    for fmt in _DATE_FORMATS_WITH_DAY:
        try:
            return datetime.strptime(value, fmt).date(), True
        except ValueError:
            continue

    for fmt in _DATE_FORMATS_MONTH_ONLY:
        try:
            return datetime.strptime(value, fmt).date(), False
        except ValueError:
            continue

    return None, False


def resolve_date(text, fallback=None, prefer_fallback_same_month=True):
    """
    Parse ``text`` into an ISO date string.

    Month-only values ("Sep 2026") are resolved to ``fallback`` when it falls
    in the same month (keeps the real go-live day), otherwise to the 1st.
    Returns ``(iso_string_or_None, ok)``; ok is False when text was present
    but could not be parsed.
    """
    parsed, has_day = parse_loose_date(text)

    if parsed is None:
        if clean_text(text):
            return (fallback.isoformat() if fallback else None), False
        return (fallback.isoformat() if fallback else None), True

    if (
        not has_day
        and prefer_fallback_same_month
        and fallback
        and (fallback.year, fallback.month) == (parsed.year, parsed.month)
    ):
        return fallback.isoformat(), True

    return parsed.isoformat(), True


def stable_row_id(*parts, length=19):
    """
    Deterministic stand-in for the random base-36 row ids the SAR editor
    gives revision rows (e.g. "et3bm0vzhxqmuv3a4vz"). Same input -> same id,
    so dry runs and re-runs produce identical JSON.
    """
    digest = hashlib.sha1("|".join(str(p) for p in parts).encode("utf-8")).digest()
    number = int.from_bytes(digest, "big")
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    chars = []
    while len(chars) < length:
        number, rem = divmod(number, 36)
        chars.append(alphabet[rem])
    return "".join(chars)


def _valid_risk(value):
    value = clean_text(value).upper()
    return value if value in RISK_COLOR_MAP else None


# ---------------------------------------------------------------------------
# Section parsers. Signature: (html, ctx, warn) -> dict
# ---------------------------------------------------------------------------


def parse_header_first_page(html_content, ctx, warn):
    soup = make_soup(html_content)

    # Solution name: the "upper" block, split across several <p> lines.
    solution_name = ""
    upper = soup.select_one("div.upper")
    if upper is not None:
        parts = upper.select("span.project_nm") or upper.find_all("p")
        solution_name = clean_text(" ".join(node_text(p) for p in parts))
    if not solution_name:
        solution_name = ctx.solution_name
        warn("Solution name not found in HTML; used the request's value.")

    # Version: first paragraph of the "centered" block.
    version = ""
    centered = soup.select_one("div.centered")
    if centered is not None:
        first_paragraph = centered.find("p")
        if first_paragraph is not None and "comb_residual_view" not in (
            first_paragraph.get("class") or []
        ):
            version = node_text(first_paragraph)
    if version.strip("[]").lower() == "subtitle/version":
        version = ""

    # Overall risk.
    overall_risk = _valid_risk(node_text(soup.select_one(".comb_residual_view")))
    if overall_risk is None:
        overall_risk = _valid_risk(ctx.overall_risk or "")
        warn("Overall risk not found/invalid in HTML; used the request's value.")

    # APM id and go-live date (the paragraph just above the APM line).
    apm_solution_id = ""
    go_live_date = ctx.go_live_date.isoformat() if ctx.go_live_date else None

    apm_node = soup.find(
        string=lambda value: isinstance(value, str) and "APM/TPM" in value
    )
    if apm_node is not None:
        apm_text = clean_text(apm_node)
        apm_solution_id = apm_text.split("#", 1)[1].strip() if "#" in apm_text else ""
        if apm_solution_id.lower() == "none":
            apm_solution_id = ""

        apm_paragraph = apm_node.find_parent("p")
        previous_paragraph = (
            apm_paragraph.find_previous_sibling("p") if apm_paragraph else None
        )
        if previous_paragraph is not None:
            go_live_text = node_text(previous_paragraph)
            go_live_date, ok = resolve_date(go_live_text, ctx.go_live_date)
            if not ok:
                warn(
                    f"Could not parse go-live date '{go_live_text}'; "
                    "used the request's value."
                )
    else:
        warn("APM/TPM line not found in HTML.")

    if not apm_solution_id:
        apm_solution_id = ctx.apm_solution_id

    return {
        "solution_name": solution_name,
        "version": version,
        "overall_risk": overall_risk,
        "go_live_date": go_live_date,
        "apm_solution_id": apm_solution_id,
    }


def _table_body_rows(table):
    if table is None:
        return []
    bodies = table.find_all("tbody")
    if bodies:
        return [row for body in bodies for row in body.find_all("tr", recursive=False)]
    return [row for row in table.find_all("tr") if row.find("td")]


def parse_revision_history(html_content, ctx, warn):
    soup = make_soup(html_content)
    table = soup.select_one("table#reviewer_his_row") or soup.find("table")

    revisions = []
    for row in _table_body_rows(table):
        cells = row.find_all("td", recursive=False)
        if not cells:
            continue

        values = [node_text(cell) for cell in cells] + [""] * 4
        version, author, date_text, revision = values[:4]

        if not any([version, author, date_text, revision]):
            continue

        revision_date, ok = resolve_date(date_text)
        if not ok:
            warn(f"Revision {version!r}: could not parse date '{date_text}'.")

        row_id = str(row.get("id") or "").strip() or stable_row_id(
            ctx.sgp_id, "revision", len(revisions), version, date_text
        )
        revisions.append(
            {
                "id": row_id,
                "version": version,
                "author": author,
                "date": revision_date,
                "revision": revision,
            }
        )

    return {"revisions": revisions}


def parse_reviewers(html_content, ctx, warn):
    soup = make_soup(html_content)
    table = soup.select_one("table#reviewer_row") or soup.find("table")

    reviewers = []
    for row in _table_body_rows(table):
        cells = row.find_all("td", recursive=False)
        if not cells:
            continue

        values = [node_text(cell) for cell in cells] + [""] * 2
        reviewer_name, date_text = values[:2]

        if not reviewer_name and not date_text:
            continue

        reviewer_date, ok = resolve_date(date_text)
        if not ok:
            warn(f"Reviewer {reviewer_name!r}: could not parse date '{date_text}'.")

        row_id = str(row.get("id") or "").strip()
        reviewers.append(
            {
                # The command replaces this with the platform user's id when
                # the name matches exactly one user (same as
                # add_leadership_reviewer_on_approval writes); otherwise the
                # 1-based row number is kept.
                "id": int_or_none(row_id) or row_id or len(reviewers) + 1,
                "reviewer": reviewer_name,
                "date": reviewer_date,
            }
        )

    return {"reviewers": reviewers}


def parse_description_section(html_content, ctx, warn):
    """header_2: the description text is real content."""
    return {"description": description_from_headings(make_soup(html_content))}


def parse_status_only_section(html_content, ctx, warn):
    """
    header_1, header_3: the JSON row only carries the section status; the
    intro text is static and rendered by the template, so description stays
    empty (an imported legacy text would be rendered twice).
    """
    return {"description": ""}


def parse_header_1_1(html_content, ctx, warn):
    soup = make_soup(html_content)

    solution_name = ""
    for heading in soup.find_all("h5"):
        heading_text = node_text(heading)
        if "classifies" in heading_text and "production use" in heading_text:
            bold = heading.find("b")
            if bold is not None:
                solution_name = node_text(bold)
            else:
                match = re.search(r"classifies\s+(.*?)\s+production use", heading_text)
                solution_name = match.group(1) if match else ""
            break

    if not solution_name:
        solution_name = ctx.solution_name
        warn("Solution name sentence not found; used the request's value.")

    risk_container = soup.select_one(".overall_residual_risk")
    risk_status = _valid_risk(
        node_text(risk_container.find("span") if risk_container else None)
        or node_text(risk_container)
    )
    if risk_status is None:
        risk_status = _valid_risk(ctx.overall_risk or "")
        warn("Residual risk not found/invalid in HTML; used the request's value.")

    return {"description": solution_name, "risk_status": risk_status}


def parse_header_1_2(html_content, ctx, warn):
    description = description_from_headings(make_soup(html_content))
    if normalize_key(description) in HEADER_1_2_PLACEHOLDERS:
        description = ""
    return {"description": description}


def parse_header_1_3(html_content, ctx, warn):
    soup = make_soup(html_content)

    data_classification = {
        "kpmg_public": False,
        "kpmg_confidential": False,
        "kpmg_restricted": False,
    }
    business_criticality = {
        "bc0_low_impact": False,
        "bc1_important": False,
        "bc2_critical": False,
        "bc3_essential": False,
        "bc4_mission_critical": False,
    }
    bc_keys = {
        "busi_bc0": "bc0_low_impact",
        "busi_bc1": "bc1_important",
        "busi_bc2": "bc2_critical",
        "busi_bc3": "bc3_essential",
        "busi_bc4": "bc4_mission_critical",
    }

    found_bc4 = False

    for checkbox in soup.find_all("input"):
        if str(checkbox.get("type") or "checkbox").lower() != "checkbox":
            continue

        identifier = str(checkbox.get("id") or checkbox.get("value") or "").lower()
        checked = is_checked(checkbox)

        if identifier in bc_keys:
            business_criticality[bc_keys[identifier]] = checked
            found_bc4 = found_bc4 or identifier == "busi_bc4"
        elif identifier.endswith("high_confidential") or identifier.endswith("_restricted"):
            data_classification["kpmg_restricted"] = checked
        elif identifier.endswith("_confidential"):
            data_classification["kpmg_confidential"] = checked
        elif identifier.endswith("_public"):
            data_classification["kpmg_public"] = checked

    policy_url = ""
    for link in soup.find_all("a"):
        href = str(link.get("href") or "").strip()
        if href:
            policy_url = href
            break

    return {
        "data_classification": data_classification,
        "business_criticality": business_criticality,
        "show_bc4": found_bc4 or business_criticality["bc4_mission_critical"],
        "is_editable": ctx.is_editable,
        "policy_url": policy_url or DEFAULT_POLICY_URL,
    }


def parse_header_1_4(html_content, ctx, warn):
    soup = make_soup(html_content)
    mapping = {
        "users_1": "internal_client_service_delivery",
        "users_2": "internal_client_support_service",
        "users_3": "external_third_party_vendor",
        "users_4": "external_public",
        "users_5": "external_client",
    }
    # The JSON carries both the legacy users_N flags and the named flags.
    result = {legacy_key: False for legacy_key in mapping}
    result.update({json_key: False for json_key in mapping.values()})

    for checkbox in soup.find_all("input"):
        identifier = str(
            checkbox.get("value") or checkbox.get("name") or checkbox.get("id") or ""
        ).lower()
        if identifier in mapping:
            checked = is_checked(checkbox)
            result[identifier] = checked
            result[mapping[identifier]] = checked

    return result


def parse_header_1_5(html_content, ctx, warn):
    soup = make_soup(html_content)

    details_element = soup.select_one("h5.hosting-details")
    model_element = None
    for heading in soup.find_all("h5"):
        if heading is not details_element:
            model_element = heading
            break

    hosting_model = ""
    hosting_details = ""

    if details_element is not None:
        hosting_details = "\n\n".join(element_paragraphs(details_element))

    if model_element is not None:
        model_copy = copy.copy(model_element)
        nested = model_copy.find_all(["div", "span"], recursive=False)
        nested_text = "\n\n".join(
            paragraph for node in nested for paragraph in element_paragraphs(node)
        )
        for node in nested:
            node.decompose()
        hosting_model = node_text(model_copy)

        if not hosting_model and nested_text:
            hosting_model = nested_text
        elif nested_text and not hosting_details:
            # Legacy "Other" layout: <h5>Other<div><span>details</span></div></h5>
            hosting_details = nested_text

    return {
        "hosting_model": hosting_model,
        "hosting_details": hosting_details,
        "has_details": bool(hosting_details),
    }


def parse_header_2_1(html_content, ctx, warn):
    soup = make_soup(html_content)
    container = soup.select_one("#header_2_1_img_show") or soup

    image_links = []
    for index, image in enumerate(container.find_all("img"), start=1):
        src = str(image.get("src") or "").strip()
        if not src:
            continue

        file_name = str(image.get("data-file-name") or image.get("alt") or "").strip()
        if not file_name:
            if src.startswith("data:"):
                file_name = f"architecture_image_{index}"
                warn(f"Image {index} is an inline data URI; kept as-is.")
            else:
                path = urlparse(src).path.rstrip("/")
                file_name = unquote(path.rsplit("/", 1)[-1]) or f"architecture_image_{index}"

        image_links.append({"file_name": file_name, "url": src})

    return {"image_links": image_links}


def _find_table_with_header(soup, *needles):
    for table in soup.find_all("table"):
        header_text = normalize_key(
            " ".join(node_text(th) for th in table.find_all("th"))
        )
        if all(needle in header_text for needle in needles):
            return table
    return None


def _event_type_from_radios(cell):
    in_house = third_party = False
    radios = [
        radio for radio in cell.find_all("input")
        if str(radio.get("type") or "").lower() == "radio"
    ]
    for position, radio in enumerate(radios):
        if not is_checked(radio):
            continue
        marker = " ".join(
            str(radio.get(attr) or "") for attr in ("value", "id")
        ).lower()
        if "third" in marker or "radio_2" in marker:
            third_party = True
        elif "in_house" in marker or "radio_1" in marker:
            in_house = True
        elif position == 0:
            in_house = True
        else:
            third_party = True

    if in_house and third_party:
        third_party = False  # ingestion rejects both; keep the first option
    return in_house, third_party


def _parse_event_rows(table, warn, date_fallback=None, keep_ids=False, month_only=False):
    events = []
    current = None

    for row in _table_body_rows(table):
        cells = row.find_all("td", recursive=False)
        if not cells:
            continue

        is_event_row = len(cells) >= 3 or cells[0].has_attr("rowspan")

        if is_event_row:
            name_cell = copy.copy(cells[0])
            in_house, third_party = _event_type_from_radios(cells[0])
            for node in name_cell.find_all(["div", "input", "label"]):
                node.decompose()

            date_text = node_text(cells[1]) if len(cells) > 1 else ""
            test_date, ok = resolve_date(date_text, date_fallback)
            if not ok:
                warn(f"Could not parse test date '{date_text}'.")
            if month_only and test_date:
                test_date = test_date[:7]  # header_3_1 stores "YYYY-MM"

            current = {
                "event_name": node_text(name_cell),
                "test_date": test_date,
                "in_house": in_house,
                "third_party": third_party,
                "result": strip_label(node_text(cells[2]), "Result:")
                if len(cells) > 2 else "",
                "scope": "",
            }
            if keep_ids:
                current = {"id": int_or_none(row.get("data-event-id")), **current}
            events.append(current)
        elif current is not None:
            current["scope"] = strip_label(node_text(cells[0]), "Scope:")

    return events


def parse_testing_overview(html_content, ctx, warn):
    """Legacy header_3_2 -> JSON header_3_1."""
    soup = make_soup(html_content)

    if _find_table_with_header(soup, "security requirement"):
        raise ValueError(
            "Legacy header_3_2 contains security-control tables, not the "
            "testing-overview events table; it looks already migrated."
        )

    # The intro paragraph is static template text; the JSON only stores the
    # events. Flag SARs where someone edited it, so the change is not lost
    # silently.
    description = description_from_headings(soup)
    if description and normalize_key(description) != normalize_key(
        DEFAULT_HEADER_3_1_DESCRIPTION
    ):
        warn(
            "Custom overview text is not part of the header_3_1 JSON and was "
            "not migrated: " + description[:120]
        )

    table = _find_table_with_header(soup, "event") or soup.find("table")
    if table is None:
        warn("Events table not found; header_3_1 will have no events.")

    events = _parse_event_rows(
        table, warn, date_fallback=ctx.go_live_date, month_only=True
    )

    return {"events": events}


# --- Security controls (legacy header_3_4 -> header_3_2) -------------------

_STATUS_LABEL_TO_KEY = {
    normalize_key(config["label"]): key for key, config in STATUS_CONFIG.items()
}
_STATUS_VALUE_TO_KEY = {
    config["value"]: key for key, config in STATUS_CONFIG.items()
}
_YES_NO_LABEL_TO_KEY = {
    normalize_key(config["label"]): key for key, config in YES_NO_STATUS_CONFIG.items()
}
_YES_NO_VALUE_TO_KEY = {
    config["value"]: key for key, config in YES_NO_STATUS_CONFIG.items()
}
_EMPTY_STATUS_LABELS = {"", "-", "select status", "select"}


def _alnum(value):
    """Lower-case letters/digits only: "Backup / Disaster RecoveryVM ..." and
    "Backup / Disaster Recovery" + "VM ..." compare equal."""
    return re.sub(r"[^a-z0-9]+", "", normalize_key(value))


class ControlsCatalogue:
    """One controls template (CONTROLS_DICT or CONTROLS_DICT_OLD)."""

    def __init__(self, template, is_new, category_titles):
        template = template if isinstance(template, dict) else {}
        self.is_new = is_new
        self.controls = [
            control for control in template.get("controls", [])
            if isinstance(control, dict) and control.get("key")
        ]
        self.by_key = {control["key"]: control for control in self.controls}
        # normalized category title -> category key
        self.category_titles = {
            normalize_key(title): key for key, title in category_titles.items()
        }
        self.categories = set(category_titles) | {
            control.get("category") for control in self.controls
        }

    def empty_json(self):
        data = {"is_new": True} if self.is_new else {}
        data["controls"] = [copy.deepcopy(control) for control in self.controls]
        return data

    def match(self, title, hint, category=None, explicit_key=None, used=()):
        """
        Return (template_control, score) for a legacy row, or (None, 0).

        Score 3: explicit key or "title + hint" equals the template's control
                 text (old templates fold the hint into the control text).
        Score 2: the title alone equals the control text or key.
        Score 1: the control text starts with the title.
        Within a tier a control from the same category is preferred.
        """
        if explicit_key and explicit_key in self.by_key and explicit_key not in used:
            return self.by_key[explicit_key], 3

        title_alnum = _alnum(title)
        full_alnum = _alnum(f"{title} {hint}") if hint else None
        if not title_alnum:
            return None, 0

        available = [c for c in self.controls if c["key"] not in used]

        def texts(control):
            return {
                _alnum(control.get(field_name))
                for field_name in ("control", "title", "key")
                if control.get(field_name)
            }

        tiers = (
            (3, lambda c: full_alnum is not None and full_alnum in texts(c)),
            (2, lambda c: title_alnum in texts(c) or slugify_key(title) == c["key"]),
            (
                1,
                lambda c: len(title_alnum) >= 4
                and _alnum(c.get("control")).startswith(title_alnum),
            ),
        )
        for score, predicate in tiers:
            candidates = [c for c in available if predicate(c)]
            if candidates:
                same_category = [c for c in candidates if c.get("category") == category]
                return (same_category or candidates)[0], score
        return None, 0


def _controls_catalogues():
    return (
        ControlsCatalogue(CONTROLS_DICT_OLD, False, OLD_CATEGORY_TITLE_MAPPING),
        ControlsCatalogue(CONTROLS_DICT, True, NEW_CATEGORY_TITLE_MAPPING),
    )


def _parse_status(cell, control_key, warn, title):
    yes_no = control_key in YES_NO_CONTROL_KEYS
    label_map = _YES_NO_LABEL_TO_KEY if yes_no else _STATUS_LABEL_TO_KEY
    value_map = _YES_NO_VALUE_TO_KEY if yes_no else _STATUS_VALUE_TO_KEY

    select = cell.find("select")
    if select is not None:
        option = select.find("option", selected=True)
        if option is not None:
            value = str(option.get("value") or "").strip()
            if value in value_map:
                return value_map[value]

    label = normalize_key(
        node_text(cell.select_one(".header_3_4_security_value") or cell)
    )
    if label in _EMPTY_STATUS_LABELS:
        return ""
    if label in label_map:
        return label_map[label]

    warn(f"Control '{title}': unknown status '{label}', left empty.")
    return ""


def _parse_implementation(cell, template_placeholder=""):
    text = node_text(cell)
    if text in {"", "-"}:
        return "", ""

    placeholder_flag = str(cell.get("data-is-placeholder") or "").lower() == "true"
    bracketed = re.fullmatch(r"\[(.*)\]", text, flags=re.S)

    if placeholder_flag or bracketed:
        return "", (bracketed.group(1).strip() if bracketed else text)

    # Some renderers wrote the placeholder without brackets.
    if template_placeholder and _alnum(text) == _alnum(template_placeholder):
        return "", template_placeholder

    return "\n\n".join(element_paragraphs(cell)) or text, ""


def _iter_security_rows(soup, warn):
    """
    Walk the control tables. Returns a list of
    (table_title, tr, cells[:4], requirement_title, requirement_hint).
    """
    tables = []
    for table in soup.find_all("table"):
        heading = table.select_one("thead tr th")
        if heading is not None:
            tables.append((normalize_key(node_text(heading)), table))

    if not tables:
        raise ValueError("No security-control tables found.")

    rows = []
    for title, table in tables:
        for row in _table_body_rows(table):
            cells = row.find_all("td", recursive=False)
            if len(cells) < 4:
                warn(f"'{title}': row with {len(cells)} cells skipped.")
                continue

            requirement_cell = cells[0]
            requirement_title = (
                node_text(requirement_cell.find("b")) or node_text(requirement_cell)
            )
            requirement_hint = node_text(requirement_cell.find("h6"))
            rows.append((title, row, cells[:4], requirement_title, requirement_hint))

    return rows


def _table_category(table_title, catalogue, other):
    return catalogue.category_titles.get(table_title) or other.category_titles.get(
        table_title
    )


def choose_controls_catalogue(rows, catalogues=None):
    """
    Decide whether a SAR was written against the old or the new controls.

    Every row is matched against both catalogues (rows matching the full
    "title + hint" text weigh more than bare-title matches), and every table
    title found in only one catalogue adds a point. Ties go to the old
    catalogue, because only pre-JSON SARs are migrated.
    """
    old, new = catalogues or _controls_catalogues()
    scores = {False: 0, True: 0}

    for catalogue in (old, new):
        used = set()
        for table_title, row, _cells, title, hint in rows:
            category = catalogue.category_titles.get(table_title)
            control, score = catalogue.match(
                title, hint, category,
                explicit_key=str(row.get("data-control-key") or "").strip() or None,
                used=used,
            )
            if control is not None:
                used.add(control["key"])
                scores[catalogue.is_new] += score

    for table_title in {row[0] for row in rows}:
        in_old = table_title in old.category_titles
        in_new = table_title in new.category_titles
        if in_old and not in_new:
            scores[False] += 1
        elif in_new and not in_old:
            scores[True] += 1

    chosen, other = (new, old) if scores[True] > scores[False] else (old, new)
    return chosen, other, scores


def parse_security_controls(html_content, ctx, warn):
    """
    Legacy header_3_4 -> JSON header_3_2.

    Output has exactly the shape of the chosen template: CONTROLS_DICT_OLD ->
    {"controls": [...]}, CONTROLS_DICT -> {"is_new": True, "controls": [...]},
    each control with key / category / status / comment / control /
    placeholder_text / implementation_details, in template order.
    """
    soup = make_soup(html_content)
    rows = _iter_security_rows(soup, warn)
    catalogue, other, _scores = choose_controls_catalogue(rows)

    filled = {}
    extras = []
    used_keys = set()

    for table_title, row, cells, requirement_title, requirement_hint in rows:
        _, implementation_cell, status_cell, comment_cell = cells
        table_category = _table_category(table_title, catalogue, other)
        explicit_key = str(row.get("data-control-key") or "").strip() or None

        template, _score = catalogue.match(
            requirement_title, requirement_hint, table_category,
            explicit_key=explicit_key, used=used_keys,
        )

        if template is not None:
            control = copy.deepcopy(template)
        else:
            if table_category is None:
                warn(
                    f"Control '{requirement_title}' in unknown table "
                    f"'{table_title}' matches no template control; skipped."
                )
                continue
            base_key = explicit_key or slugify_key(requirement_title)
            control_key, suffix = base_key, 2
            while control_key in used_keys or control_key in catalogue.by_key:
                control_key = f"{base_key}_{suffix}"
                suffix += 1
            control = {
                "key": control_key,
                "category": table_category,
                "status": "",
                "comment": "",
                "control": clean_text(f"{requirement_title} {requirement_hint}"),
                "placeholder_text": "",
                "implementation_details": "",
            }
            warn(
                f"Control '{requirement_title}' is not in the "
                f"{'new' if catalogue.is_new else 'old'} controls template; "
                f"kept as extra control '{control_key}'."
            )

        used_keys.add(control["key"])

        implementation_details, html_placeholder = _parse_implementation(
            implementation_cell, control.get("placeholder_text") or ""
        )
        comment = "\n\n".join(element_paragraphs(comment_cell))
        if comment.strip() == "-":
            comment = ""

        control["status"] = _parse_status(
            status_cell, control["key"], warn, requirement_title
        )
        control["implementation_details"] = implementation_details
        control["comment"] = comment
        control["placeholder_text"] = (
            control.get("placeholder_text")
            or html_placeholder
            or ctx.control_placeholders.get(
                (table_category, normalize_key(requirement_title))
            )
            or ""
        )

        if template is not None:
            filled[control["key"]] = control
        else:
            extras.append(control)

    result = catalogue.empty_json()
    missing = [c["key"] for c in result["controls"] if c["key"] not in filled]
    result["controls"] = [
        filled.get(control["key"], control) for control in result["controls"]
    ] + extras

    if missing:
        warn(
            f"{len(missing)} template control(s) not present in the HTML were "
            f"added empty: {missing}"
        )
    return result


def build_control_placeholder_index(template_html):
    """
    Parse a default (unfilled) controls template and return
    {(category, normalized requirement title): placeholder_text}.
    Only used as a last resort for rows that match no template control.
    """
    if not (template_html or "").strip():
        return {}

    old, new = _controls_catalogues()
    rows = _iter_security_rows(make_soup(template_html), lambda message: None)
    index = {}
    for table_title, _row, cells, requirement_title, _hint in rows:
        category = _table_category(table_title, old, new)
        _, placeholder_text = _parse_implementation(cells[1])
        if placeholder_text and category:
            index[(category, normalize_key(requirement_title))] = placeholder_text
    return index


def parse_poam(html_content, ctx, warn):
    """Legacy header_6 -> JSON header_4 (static section, no data)."""
    return {}


def parse_business_considerations(html_content, ctx, warn):
    """Legacy header_7 -> JSON header_5. Missing row means disabled."""
    if html_content is None:
        return {"is_enabled": False, "description": ""}

    return {
        "is_enabled": True,
        "description": description_from_headings(make_soup(html_content)),
    }


def parse_support_team(html_content, ctx, warn):
    soup = make_soup(html_content)
    table = soup.select_one("table#support_team_row") or soup.find("table")

    contacts = []
    for row in _table_body_rows(table):
        cells = row.find_all("td", recursive=False)
        if not cells:
            continue
        values = [node_text(cell) for cell in cells] + [""] * 3
        role, name, email = values[:3]
        if role or name or email:
            contacts.append({"role": role, "name": name, "email": email})

    return {"contacts": contacts}


def parse_addendum(html_content, ctx, warn):
    """
    Handles both the generated layout (.addendum-subsection-item blocks) and
    older free-form layouts: each events table closes one subsection, the
    nearest preceding <h3> gives its date, and <h5> text before it is the
    description.
    """
    if html_content is None:
        return {"is_enabled": False, "subsections": []}

    soup = make_soup(html_content)
    root = soup.select_one(".addendum_subsection") or soup

    subsections = []
    current = None

    def start(heading=None):
        item = heading.find_parent(class_="addendum-subsection-item") if heading else None
        return {
            "id": int_or_none(item.get("data-subsection-id")) if item else None,
            "date": None,
            "description_parts": [],
            "events": [],
        }

    for element in root.find_all(["h3", "h5", "table"]):
        if element.name != "table" and element.find_parent("table"):
            continue

        if element.name == "h3":
            if current and (current["description_parts"] or current["date"]):
                subsections.append(current)
            current = start(element)
            heading_text = re.sub(r"^\s*\d+(\.\d+)*\s*", "", node_text(element))
            current["date"], ok = resolve_date(heading_text)
            if not ok:
                warn(f"Addendum heading '{node_text(element)}': date not parsed.")

        elif element.name == "h5":
            if current is None:
                current = start(element)
            current["description_parts"].extend(element_paragraphs(element))

        elif element.name == "table":
            header_text = normalize_key(
                " ".join(node_text(th) for th in element.find_all("th"))
            )
            if "event" not in header_text:
                continue
            if current is None:
                current = start(element)
            current["events"] = _parse_event_rows(element, warn, keep_ids=True)
            for event in current["events"]:
                event.pop("in_house", None)
                event.pop("third_party", None)
            subsections.append(current)
            current = None

    if current and (current["description_parts"] or current["date"]):
        subsections.append(current)

    result = []
    for subsection in subsections:
        result.append(
            {
                "id": subsection["id"],
                "date": subsection["date"],
                "description": "\n\n".join(subsection["description_parts"]),
                "events": subsection["events"],
            }
        )

    if not result:
        warn("No addendum subsections recognised; review this SAR manually.")

    return {"is_enabled": True, "subsections": result}


# ---------------------------------------------------------------------------
# Section registry and plan builder
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SectionSpec:
    json_header: str
    legacy_headers: tuple
    parser: Callable
    parse_when_missing: bool = False  # call parser with html=None if absent


SECTION_SPECS = (
    SectionSpec("header_first_page", ("header_first_page",), parse_header_first_page),
    SectionSpec("header_revision_second_page", ("header_revision_second_page",), parse_revision_history),
    SectionSpec("header_reviewer_second_page", ("header_reviewer_second_page",), parse_reviewers),
    SectionSpec("header_1", ("header_1",), parse_status_only_section),
    SectionSpec("header_1_1", ("header_1_1",), parse_header_1_1),
    SectionSpec("header_1_2", ("header_1_2",), parse_header_1_2),
    SectionSpec("header_1_3", ("header_1_3",), parse_header_1_3),
    SectionSpec("header_1_4", ("header_1_4",), parse_header_1_4),
    SectionSpec("header_1_5", ("header_1_5",), parse_header_1_5),
    SectionSpec("header_2", ("header_2",), parse_description_section),
    SectionSpec("header_2_1", ("header_2_1",), parse_header_2_1),
    SectionSpec("header_3", ("header_3",), parse_status_only_section),
    SectionSpec("header_3_1", ("header_3_2",), parse_testing_overview),
    SectionSpec("header_3_2", ("header_3_4",), parse_security_controls),
    SectionSpec("header_4", ("header_6",), parse_poam),
    SectionSpec("header_5", ("header_7",), parse_business_considerations, parse_when_missing=True),
    SectionSpec("header_support_team", ("header_support_team",), parse_support_team),
    SectionSpec("addendum_header", ("addendum_header",), parse_addendum, parse_when_missing=True),
)


def build_migration_plan(legacy_rows, ctx):
    """
    legacy_rows: {legacy_header_name: html} (latest active row per header)
    Returns a SarMigrationPlan; parsing failures are recorded per section.
    """
    plan = SarMigrationPlan()
    consumed = set()

    for spec in SECTION_SPECS:
        source = next((h for h in spec.legacy_headers if legacy_rows.get(h)), None)

        if source is None and not spec.parse_when_missing:
            continue

        html_content = legacy_rows.get(source) if source else None

        def warn(message, _header=spec.json_header):
            plan.warn(_header, message)

        try:
            data = spec.parser(html_content, ctx, warn)
            plan.sections[spec.json_header] = data
            plan.sources[spec.json_header] = source or "(absent -> disabled)"
            if spec.parser is parse_security_controls:
                plan.sources[spec.json_header] += (
                    " (NEW controls)" if data.get("is_new") else " (OLD controls)"
                )
        except Exception as exc:  # noqa: BLE001 - reported per section
            plan.errors[spec.json_header] = f"{type(exc).__name__}: {exc}"

        if source:
            consumed.add(source)

    plan.unmapped_legacy_headers = sorted(
        header for header, html in legacy_rows.items()
        if html and header not in consumed
    )
    return plan
