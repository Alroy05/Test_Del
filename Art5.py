import os

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from app.constants import CONTROLS_DICT
from app.models import SarTemplateJsonData, LogUpdate, SpiPsiResponse, RequestorTeam

@transaction.atomic
def initialize_sar_sections(
    request_details,
    user,
):

    existing_rows = list(
        SarTemplateJsonData.objects.select_for_update()
        .filter(
            request=request_details,
            is_active=1,
        )
        .order_by("header_name", "-created_date")
    )

    existing_sections = {}

    for row in existing_rows:
        if row.header_name not in existing_sections:
            existing_sections[row.header_name] = row

    sections_to_create = []

    spi_psi_responses = {
        response.question_id: response
        for response in SpiPsiResponse.objects.filter(
            request=request_details,
            question_id__in=[4, 5, 10, 14, 15],
        )
    }

    def get_response(question_id, attribute="response"):
        response_obj = spi_psi_responses.get(question_id)
        if not response_obj:
            return ""
        value = getattr(response_obj, attribute, None)
        if value is None:
            return ""
        return str(value).strip()

    if "header_first_page" not in existing_sections:
        header_first_page_data = {
            "solution_name": request_details.solution_name or "",
            "version": "",
            "overall_risk": request_details.overall_risk or None,
            "go_live_date": (
                request_details.go_live_date.isoformat()
                if request_details.go_live_date
                else None
            ),
            "apm_solution_id": request_details.apm_solution_id or "",
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_first_page",
                json_data=header_first_page_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    if "header_revision_second_page" not in existing_sections:
        revision_log = (
            LogUpdate.objects.filter(
                request=request_details,
                event=LogUpdate.SAR_LOG_EVENT,
                response_for__in=[
                    "Security Resource",
                    "System Super Admin",
                ],
            )
            .order_by("created_date")
            .first()
        )

        if not revision_log:
            revision_log = (
                LogUpdate.objects.filter(
                    request=request_details,
                    event=LogUpdate.SAR_LOG_EVENT,
                )
                .order_by("created_date")
                .first()
            )

        if revision_log:
            author = revision_log.created_by_name or ""
            revision_id = revision_log.id
            revision_date = revision_log.created_date
        else:
            author = f"{user.first_name} {user.last_name}".strip()
            revision_id = None
            revision_date = timezone.now()

        header_revision_second_page_data = {
            "revisions": [
                {
                    "id": revision_id,
                    "version": "0.1",
                    "author": author,
                    "date": (
                        revision_date.isoformat()
                        if revision_date
                        else None
                    ),
                    "revision": "Initial SAR draft",
                }
            ]
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_revision_second_page",
                json_data=header_revision_second_page_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    if "header_reviewer_second_page" not in existing_sections:
        reviewers = request_details.get_assigned_security_users()
        current_date = timezone.now()

        reviewer_list = []

        for reviewer in reviewers:
            reviewer_name = (
                reviewer.get_full_name()
                if reviewer.first_name and reviewer.last_name
                else ""
            )

            reviewer_list.append(
                {
                    "id": reviewer.id,
                    "reviewer": reviewer_name,
                    "date": current_date.isoformat(),
                }
            )

        header_reviewer_second_page_data = {
            "reviewers": reviewer_list
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_reviewer_second_page",
                json_data=header_reviewer_second_page_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    # Solution Overview
    if "header_1" not in existing_sections:
        header_1_data = {
            "description": (
                "The Global Information Security Group's (GISG) Solution Review "
                "Service provides assessment of security risks and controls in new "
                "technology solutions to ensure minimal residual risk to KPMG, "
                "Global IT and alignment to laws, regulations and other agreements. "
                "Assessments may include reviews of architecture / technical security "
                "conformance and third party involvement in solution delivery and "
                "support.\n\n"
                "The Security Assessment Report (SAR) is the formal GISG document "
                "of a solution's compliance to KPMG International's security testing "
                "and technical security standards. This assessment report on the "
                "production use of solutions and infrastructure operated by or on "
                "behalf of KPMG International, as defined by the Global Information "
                "Security Policy."
            )
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_1",
                json_data=header_1_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    # Risk Summary
    if "header_1_1" not in existing_sections:
        header_1_1_data = {
            "description": request_details.solution_name or "",
            "risk_status": request_details.overall_risk or None,
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_1_1",
                json_data=header_1_1_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
    )

    # Solution Summary
    if "header_1_2" not in existing_sections:
        header_1_2_data = {
            "description": "",
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_1_2",
                json_data=header_1_2_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    # Data Classification and Business Criticality
    if "header_1_3" not in existing_sections:
        ques_14_resp = get_response(14).lower()
        ques_15_resp = get_response(15).lower()

        # Data classification values
        kpmg_public = False
        kpmg_confidential = False
        kpmg_restricted = False

        # Business criticality values
        bc0_low_impact = False
        bc1_important = False
        bc2_critical = False
        bc3_essential = False
        bc4_mission_critical = False

        # Question 15: Data Classification
        if ques_15_resp == "kpmg public":
            kpmg_public = True

        elif ques_15_resp == "kpmg confidential":
            kpmg_confidential = True

        elif ques_15_resp in [
            "kpmg restricted",
            "kpmg highly confidential",
        ]:
            kpmg_restricted = True

        # Question 14: Business Criticality
        if ques_14_resp == "bc0/1":
            bc0_low_impact = True
            bc1_important = True

        elif ques_14_resp in [
            "bc0",
            "bc0 - low impact",
        ]:
            bc0_low_impact = True

        elif ques_14_resp in [
            "bc1",
            "bc1 - important",
        ]:
            bc1_important = True

        elif ques_14_resp in [
            "bc2",
            "bc2 - critical",
        ]:
            bc2_critical = True

        elif ques_14_resp in [
            "bc3",
            "bc3 - essential",
        ]:
            bc3_essential = True

        elif ques_14_resp in [
            "bc4",
            "bc4 - mission critical system",
        ]:
            bc4_mission_critical = True

        header_1_3_data = {
            "data_classification": {
                "kpmg_public": kpmg_public,
                "kpmg_confidential": kpmg_confidential,
                "kpmg_restricted": kpmg_restricted,
            },
            "business_criticality": {
                "bc0_low_impact": bc0_low_impact,
                "bc1_important": bc1_important,
                "bc2_critical": bc2_critical,
                "bc3_essential": bc3_essential,
                "bc4_mission_critical": bc4_mission_critical,
            },
            "show_bc4": bc4_mission_critical,
            "is_editable": request_details.request_type != RequestorTeam.REQUEST_TYPE_NEW,
            "policy_url": (
                "https://kieps.kpmg.com/spgip/#/doc/f8f79305-492a-ef11-86d4-002248206d19"
            ),
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_1_3",
                json_data=header_1_3_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    # Users
    if "header_1_4" not in existing_sections:
        header_1_4_data = {
            "internal_client_service_delivery": False,
            "internal_client_support_service": False,
            "external_third_party_vendor": False,
            "external_public": False,
            "external_client": False,
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_1_4",
                json_data=header_1_4_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    # Hosting
    if "header_1_5" not in existing_sections:
        hosting_model = get_response(4)
        has_details = False
        hosting_details = ""

        if hosting_model.strip().lower() == "other":
            has_details = True
            hosting_details = get_response(
                question_id=5,
                attribute="comments",
            )

        header_1_5_data = {
            "hosting_model": hosting_model,
            "hosting_details": hosting_details,
            "has_details": has_details,
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_1_5",
                json_data=header_1_5_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    # Architecture
    if "header_2" not in existing_sections:
        header_2_data = {
            "description": (
                "A solution's architecture describes how the various elements "
                "fit together - the Business Processes and the Functions "
                "responsible for them, information used and generated by the "
                "business, application and infrastructure capabilities."
            ),
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_2",
                json_data=header_2_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    # High Level Technical Architecture Diagram
    if "header_2_1" not in existing_sections:
        architecture_response = spi_psi_responses.get(10)

        architecture_filename = (
            architecture_response.filename
            if architecture_response
            and architecture_response.filename
            else ""
        )

        image_links = []

        if architecture_filename:
            image_names = [
                file_name.strip()
                for file_name in architecture_filename.split("||")
                if file_name.strip()
            ]

            base_path = os.path.join(
                settings.MEDIA_ROOT,
                f"requestor/{request_details.sgp_id}",
            )

            for file_name in image_names:
                full_path = os.path.join(base_path, file_name)

                if not os.path.exists(full_path):
                    continue

                image_links.append(
                    {
                        "file_name": file_name,
                        "url": (
                            f"{settings.BACKEND_DOMAIN}/storage/"
                            f"serve-architecture-files/"
                            f"{request_details.sgp_id}/"
                            f"{file_name}/"
                        ),
                    }
                )

        header_2_1_data = {
            "image_links": image_links,
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_2_1",
                json_data=header_2_1_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    # Assessment Overview
    if "header_3" not in existing_sections:
        header_3_data = {
            "description": "GISG and other members of the ITS Global team, working in collaboration with the project team, undertook the following activities to understand the solution's potential technology risks. In addition to these activities, GISG reconciles the solution's architectural approaches to meet KPMGI's various security requirements.",
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_3",
                json_data=header_3_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    # header_3_1: Assessment Overview
    if "header_3_1" not in existing_sections:
        go_live_date = (
            request_details.go_live_date.isoformat()
            if request_details.go_live_date
            else None
        )

        solution_name = request_details.solution_name or ""

        header_3_1_data = {
            "description": (
                "In determining this solution's residual risk, the technology "
                "security and information management teams adjudicate each "
                "finding against the likely threat(s), the vulnerabilities "
                "severity and the potential impact. This section presents a "
                "summary of any outstanding high and medium risk items."
            ),
            "events": [
                {
                    "event_name": (
                        f"Architecture Review - {solution_name} environment"
                    ),
                    "test_date": go_live_date,
                    "in_house": False,
                    "third_party": False,
                    "result": "",
                    "scope": "",
                },
                {
                    "event_name": (
                        f"Penetration Test - {solution_name} environment"
                    ),
                    "test_date": go_live_date,
                    "in_house": False,
                    "third_party": False,
                    "result": "",
                    "scope": "",
                },
                {
                    "event_name": (
                        f"Final Static Code Analysis - "
                        f"{solution_name} environment"
                    ),
                    "test_date": go_live_date,
                    "in_house": False,
                    "third_party": False,
                    "result": "",
                    "scope": "",
                },
            ],
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_3_1",
                json_data=header_3_1_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    # header_3_2: Security Controls
    if "header_3_2" not in existing_sections:
        header_3_2_data = CONTROLS_DICT

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_3_2",
                json_data=header_3_2_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    if "header_4" not in existing_sections:
        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_4",
                json_data={},
                request=request_details,
                created_by=user,
                needs_refresh=False,
                is_active=1,
            )
        )

    # header_5: Additional Business Considerations
    if "header_5" not in existing_sections:
        header_5_data = {
            "is_enabled": True,
            "description": "",
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_5",
                json_data=header_5_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    # header_support_team: Key Contact Details
    if "header_support_team" not in existing_sections:
        header_support_team_data = {
            "contacts": [
                {
                    "role": "Business Sponsor",
                    "name": " ".join(
                        filter(
                            None,
                            [
                                request_details.business_sponsor_first_name,
                                request_details.business_sponsor_last_name,
                            ],
                        )
                    ),
                    "email": request_details.bussiness_sponser or "",
                },
                {
                    "role": "Business Lead",
                    "name": " ".join(
                        filter(
                            None,
                            [
                                request_details.business_lead_first_name,
                                request_details.business_lead_last_name,
                            ],
                        )
                    ),
                    "email": request_details.business_lead or "",
                },
                {
                    "role": "Project Manager",
                    "name": " ".join(
                        filter(
                            None,
                            [
                                request_details.project_manager_first_name,
                                request_details.project_manager_last_name,
                            ],
                        )
                    ),
                    "email": request_details.project_manager or "",
                },
                {
                    "role": "Solution Architect",
                    "name": " ".join(
                        filter(
                            None,
                            [
                                request_details.its_arch_first_name,
                                request_details.its_arch_last_name,
                            ],
                        )
                    ),
                    "email": request_details.its_arch or "",
                },
            ]
        }

        sections_to_create.append(
            SarTemplateJsonData(
                header_name="header_support_team",
                json_data=header_support_team_data,
                request=request_details,
                created_by=user,
                is_active=1,
            )
        )

    if sections_to_create:
        created_sections = SarTemplateJsonData.objects.bulk_create(
            sections_to_create
        )

        for section in created_sections:
            existing_sections[section.header_name] = section

    return {
        header_name: section.json_data or {}
        for header_name, section in existing_sections.items()
    }



============


from django.conf import settings
from django.db import models


class SarTemplateJsonData(models.Model):

    STATUS_DRAFT = 1
    STATUS_COMPLETED = 2

    STATUS_LABELS = {
        STATUS_DRAFT: "DRAFT",
        STATUS_COMPLETED: "COMPLETED"
    }

    STATUS_VALUES = {label: value for value, label in STATUS_LABELS.items()}

    id = models.AutoField(primary_key=True)
    header_name = models.CharField(
        max_length=50,
        db_index=True,
        null=True,
        blank=True,
    )
    json_data = models.JSONField(
        default=dict,
        blank=True,
    )
    request = models.ForeignKey(
        "RequestorTeam",
        on_delete=models.CASCADE,
        db_column="sgp_id",
        to_field="sgp_id",
        related_name="sar_template_json_data",
        null=True,
        blank=True,
    )
    section_status = models.PositiveSmallIntegerField(
        default=STATUS_DRAFT,
    )
    needs_refresh = models.BooleanField(default=True, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="created_by",
        related_name="sar_template_json_data_created",
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(
        default=1,
        db_index=True,
    )
    class Meta:
        db_table = "sar_template_json_data"
        indexes = [
            models.Index(
                fields=["request", "is_active"],
                name="sar_json_request_idx",
            ),
            models.Index(
                fields=[
                    "request",
                    "is_active",
                    "header_name",
                    "-created_date",
                ],
                name="sar_json_lookup_idx",
            ),
        ]
        ordering = ["header_name"]

    def __str__(self):
        return (
            f"{self.request_id or 'No request'} - "
            f"{self.header_name or 'No header'}"
        )



import os
from urllib.parse import quote
from django.conf import settings
from django.db import transaction

from app.models import (
    LogUpdate,
    RequestorTeam,
    SarTemplateJsonData,
)
from app.models.default_template_data import DefaultTemplateData
from app.models.role import Role
from app.models.sar_json_history_data import SarJsonHistoryData
from app.models.sar_template_data import SarTemplateData
from app.models.sar_template_data_history import SarTemplateDataHistory
from app.models.spipsi_response import SpiPsiResponse
from app.services import ingestion_service

INGESTION_FUNCTION_MAP = {
    "header_first_page": ingestion_service.ingest_header_first_page_json,
    "header_revision_second_page": ingestion_service.ingest_revision_history_json,
    "header_reviewer_second_page": ingestion_service.ingest_reviewer_json,
    "header_1_1": ingestion_service.ingest_header_1_1_json,
    "header_1_2": ingestion_service.ingest_header_1_2_json,
    "header_1_3": ingestion_service.ingest_header_1_3_json,
    "header_1_4": ingestion_service.ingest_header_1_4_json,
    "header_1_5": ingestion_service.ingest_header_1_5_json,
    "header_2": ingestion_service.ingest_header_2_json,
    "header_2_1": ingestion_service.ingest_header_2_1_json,
    "header_3": ingestion_service.ingest_header_3_json,
    "header_3_1": ingestion_service.ingest_header_3_1_json,
    "header_3_2": ingestion_service.ingest_header_3_2_json,
    "header_5": ingestion_service.ingest_header_5_json,
    "header_support_team": ingestion_service.ingest_support_team_json,
    "addendum_header": ingestion_service.ingest_addendum_header_json,
}


def get_default_template_html(header_name: str) -> str:
    default_row = (
        DefaultTemplateData.objects
        .filter(header_name=header_name, is_active=2)
        .order_by("-id")
        .first()
    )

    if default_row is None or not (default_row.header_data or "").strip():
        raise ValueError(
            f"No active default template found for header_name='{header_name}'."
        )

    return default_row.header_data

def render_header_html(header_name: str, json_data: dict, request_obj) -> str:
    ingest_fn = INGESTION_FUNCTION_MAP.get(header_name)

    if ingest_fn is None:
        raise ValueError(
            f"No ingestion function registered for header_name='{header_name}'."
        )

    default_html = get_default_template_html(header_name)

    return ingest_fn(
        html_content=default_html,
        json_data=json_data or {},
        request_obj=request_obj,
    )


def get_sar_form_context(request_details, user) -> dict:

    sar_json_rows = (
        SarTemplateJsonData.objects.filter(
            request=request_details,
            is_active=1,
        )
        .order_by(
            "header_name",
            "-created_date",
        )
        .values(
            "header_name",
            "json_data",
            "section_status",
        )
    )

    sections = {}
    section_status = {}

    for row in sar_json_rows:
        header_name = row["header_name"]

        if not header_name:
            continue

        if header_name not in sections:
            sections[header_name] = row["json_data"] or {}
            section_status[header_name] = SarTemplateJsonData.STATUS_LABELS.get(
                row["section_status"], "DRAFT"
            )

    user_type = user.user_type
    current_status = request_details.status
    current_sub_status = request_details.sub_status

    data = {
        "page_title": (
            f"View SAR Template - {request_details.sgp_id}"
        ),
        "solutionName": request_details.solution_name or "",
        "projectName": request_details.project_name or "",
        "atoStatus": request_details.ato_status,
        "route_to_view": False,
        "goLiveDate": (
            request_details.go_live_date.strftime("%b %Y")
            if request_details.go_live_date
            else ""
        ),
        "sgpId": request_details.sgp_id,
        "solutionType": (
            RequestorTeam.SOLUTION_TYPE_CHOICES.get(
                request_details.solution_type,
                "-",
            )
        ),
        "is_new": False,
        "sections": sections,
        "section_status": section_status,
        "comments": False,
        "isExportPdf": False,
        "save_as_draft": False,
        "send_to_sol_team": False,
        "send_to_sec_res": False,
        "send_to_leadership": False,
        "show_ato_status": False,
        "draftExportPdf": True,
        "isContentEditable": "false",
        "isContentEditableReviewer": "false",
        "isContentEditableRevision": "false",
        "securityLogComments": [],
        "sarLogComments": [],
        "revisionHistory": [],
    }

    header_3_2 = sections.get("header_3_2", {})
    data["is_new"] = (
        header_3_2.get("is_new", False)
        if isinstance(header_3_2, dict)
        else False
    )
    
    if (
        user_type in [Role.ROLE_TYPE_AU, Role.ROLE_TYPE_TL]
        and current_sub_status
        in [
            RequestorTeam.SUB_STATUS_SECURITY_REVIEW,
            RequestorTeam.SUB_STATUS_AI_COMPLETE,
            RequestorTeam.SUB_STATUS_AI_FAILED,
        ]
        and current_status
        not in [
            RequestorTeam.STATUS_CLEARANCE,
            RequestorTeam.STATUS_CONTINUOUS_MONITORING,
        ]
    ):
        data["show_ato_status"] = True

    if current_sub_status in [
        RequestorTeam.SUB_STATUS_SOL_TEAM_REVIEW
    ] and user_type in [
        Role.ROLE_TYPE_AU,
        Role.ROLE_TYPE_RQ,
    ]:
        data["send_to_sec_res"] = True
        data["comments"] =  True

    elif current_sub_status in [
        RequestorTeam.SUB_STATUS_SECURITY_REVIEW,
        RequestorTeam.SUB_STATUS_AI_COMPLETE,
        RequestorTeam.SUB_STATUS_AI_FAILED,
    ] and user_type in [
        Role.ROLE_TYPE_AU,
        Role.ROLE_TYPE_TL,
    ]:
        data["send_to_leadership"] = True
        data["send_to_sol_team"] = True
        data["isContentEditable"] = "true"
        data["isContentEditableReviewer"] = "true"
        data["isContentEditableRevision"] =  "true"
        data["comments"] =  True
        data["save_as_draft"] =  True

    if current_status in [
        RequestorTeam.STATUS_CONTINUOUS_MONITORING,
        RequestorTeam.STATUS_CLEARANCE,
    ]:
        data["route_to_view"] = True

    if request_details.sar_status == RequestorTeam.SAR_CREATED and request_details.status == RequestorTeam.STATUS_CONTINUOUS_MONITORING:
        data["isExportPdf"] = True

    if request_details.status == RequestorTeam.STATUS_CONTINUOUS_MONITORING:
        data["draftExportPdf"] = False

    return data


def save_sar_form_data(
    request_details,
    data,
    user,
):
    sections=data.get("sections")
    section_status_dict=data.get("section_status")
    action=data.get("action")
    comments=data.get("comments")
    ato_status=data.get("atoStatus")

    updated_headers = []
    skipped_headers = []

    with transaction.atomic():
        if action != "send_to_sec_res": 
            for header_name, new_json_data in sections.items():
                new_json_data = new_json_data or {}

                incoming_status_label = section_status_dict.get(
                    header_name,
                    "DRAFT",
                )
                new_section_status = SarTemplateJsonData.STATUS_VALUES.get(
                    incoming_status_label, 1
                )

                existing_row = (
                    SarTemplateJsonData.objects.select_for_update()
                    .filter(
                        request=request_details,
                        header_name=header_name,
                        is_active=1,
                    )
                    .first()
                )

                json_unchanged = (
                    existing_row
                    and existing_row.json_data == new_json_data
                )

                status_unchanged = (
                    existing_row
                    and existing_row.section_status
                    == new_section_status
                )

                if json_unchanged and status_unchanged:
                    skipped_headers.append(header_name)
                    continue

                needs_refresh = True

                if existing_row:
                    SarJsonHistoryData.objects.create(
                        original_id=existing_row.id,
                        header_name=existing_row.header_name,
                        json_data=existing_row.json_data,
                        request=existing_row.request,
                        created_by=existing_row.created_by,
                        original_created_date=existing_row.created_date,
                        archived_by=user,
                    )
                    existing_row.delete()

                SarTemplateJsonData.objects.create(
                    header_name=header_name,
                    json_data=new_json_data,
                    request=request_details,
                    section_status=new_section_status,
                    needs_refresh=needs_refresh,
                    created_by=user,
                    is_active=1,
                )

                updated_headers.append(header_name)

            if ato_status:
                new_ato_status = ato_status
                old_ato_status = request_details.ato_status
                if str(new_ato_status) != str(old_ato_status):
                    LogUpdate.objects.create(
                        request=request_details,
                        event=LogUpdate.ATO_STATUS_EVENT,
                        old_value=str(old_ato_status),
                        new_value=str(new_ato_status),
                        response_for="ATO Status",
                        created_by=user,
                        user_role=user.current_role,
                    )
                request_details.ato_status = ato_status
                request_details.save()

        if action != "save_as_draft":
            LogUpdate.objects.create(
                request=request_details,
                event=LogUpdate.SAR_LOG_EVENT,
                old_value="-",
                new_value=comments
                or "No Response Provided",
                response_for=Role.get_status_as_string_by_id(user.user_type),
                created_by=user,
                user_role=user.current_role,
            )

    return {
        "updated_headers": updated_headers,
        "skipped_headers": skipped_headers,
    }

@transaction.atomic
def refresh_sar_html(
    request_details,
    user,
    header_names=None,
) -> dict:

    dirty_json_qs = (
        SarTemplateJsonData.objects
        .select_for_update()
        .filter(
            request=request_details,
            is_active=1,
            needs_refresh=True,
        )
    )

    if header_names:
        dirty_json_qs = dirty_json_qs.filter(header_name__in=header_names)

    dirty_rows = {row.header_name: row for row in dirty_json_qs}

    if not dirty_rows:
        return {
            "refreshed_headers": [],
            "unmapped_headers": [],
            "failed_headers": {},
        }

    existing_html_rows = {
        row.header_name: row
        for row in SarTemplateData.objects
        .select_for_update()
        .filter(
            request=request_details,
            is_active=1,
            header_name__in=dirty_rows.keys(),
        )
    }

    refreshed_headers = []
    unmapped_headers = []
    failed_headers = {}
    consumed_row_ids = []

    for header_name, json_row in dirty_rows.items():
        if header_name not in INGESTION_FUNCTION_MAP:
            unmapped_headers.append(header_name)
            continue

        existing_html_row = existing_html_rows.get(
            header_name
        )

        if header_name == "header_5":
            header_5_data = json_row.json_data or {}

            is_header_5_enabled = (
                isinstance(header_5_data, dict)
                and header_5_data.get("is_enabled") is True
            )

            if not is_header_5_enabled:
                consumed_row_ids.append(json_row.id)
                refreshed_headers.append(header_name)
                continue

        if header_name == "addendum_header":
            addendum_data = json_row.json_data or {}

            is_addendum_enabled = (
                isinstance(addendum_data, dict)
                and addendum_data.get("is_enabled") is True
            )

            if not is_addendum_enabled:
                if existing_html_row:
                    SarTemplateDataHistory.objects.create(
                        original_id=existing_html_row.id,
                        header_name=(
                            existing_html_row.header_name
                        ),
                        header_data=(
                            existing_html_row.header_data
                        ),
                        request_id=(
                            existing_html_row.request_id
                        ),
                        comment=(
                            existing_html_row.comment
                        ),
                        created_by_id=(
                            existing_html_row.created_by_id
                        ),
                        original_created_date=(
                            existing_html_row.created_date
                        ),
                        archived_by_id=user.id,
                    )

                    existing_html_row.delete()

                consumed_row_ids.append(json_row.id)

                refreshed_headers.append(header_name)

                continue

        try:
            rendered_html = render_header_html(
                header_name=header_name,
                json_data=json_row.json_data,
                request_obj=request_details,
            )
        except Exception as exc:
            failed_headers[header_name] = str(exc)
            continue

        if existing_html_row:
            SarTemplateDataHistory.objects.create(
                original_id=existing_html_row.id,
                header_name=existing_html_row.header_name,
                header_data=existing_html_row.header_data,
                request_id=existing_html_row.request_id,
                comment=existing_html_row.comment,
                created_by_id=existing_html_row.created_by_id,
                original_created_date=(
                    existing_html_row.created_date
                ),
                archived_by_id=user.id,
            )

            existing_html_row.delete()

        SarTemplateData.objects.create(
            header_name=header_name,
            header_data=rendered_html,
            request_id=request_details.sgp_id,
            created_by=user,
            is_active=1,
        )

        refreshed_headers.append(header_name)
        consumed_row_ids.append(json_row.id)

    if consumed_row_ids:
        SarTemplateJsonData.objects.filter(
            id__in=consumed_row_ids
        ).update(needs_refresh=False)

    optional_section_result = ingestion_service.update_optional_section_html(
        request_details=request_details,
        user=user,
    )

    print(optional_section_result)

    return {
        "refreshed_headers": refreshed_headers,
        "unmapped_headers": unmapped_headers,
        "failed_headers": failed_headers,
    }

@transaction.atomic
def initialize_sar_html(request_details, user) -> dict:
    default_rows = (
        DefaultTemplateData.objects
        .filter(is_active=2)
        .exclude(header_name="addendum_header")
    )

    existing_header_names = set(
        SarTemplateData.objects
        .filter(request=request_details, is_active=1)
        .values_list("header_name", flat=True)
    )

    initialized_headers = []
    skipped_headers = []

    for default_row in default_rows:
        header_name = default_row.header_name

        if header_name in existing_header_names:
            skipped_headers.append(header_name)
            continue

        default_html = (default_row.header_data or "").strip()

        if not default_html:
            skipped_headers.append(header_name)
            continue

        SarTemplateData.objects.create(
            header_name=header_name,
            header_data=default_html,
            request_id=request_details.sgp_id,
            created_by=user,
            is_active=1,
        )

        initialized_headers.append(header_name)

    return {
        "initialized_headers": initialized_headers,
        "skipped_headers": skipped_headers,
    }


@transaction.atomic
def sync_request_derived_json_sections(request_details, user) -> dict:
    derived_header_names = [
        "header_1_1",
        "header_1_5",
        "header_2_1",
        "header_support_team",
    ]

    existing_json_by_header = {
        row.header_name: row.json_data
        for row in SarTemplateJsonData.objects
        .select_for_update()
        .filter(
            request=request_details,
            is_active=1,
            header_name__in=derived_header_names,
        )
    }

    # ---------------------------------------------------------
    # header_1_1 - owns only risk_status; description stays user-owned
    # ---------------------------------------------------------
    header_1_1_fields = {
        "risk_status": (request_details.overall_risk or "LOW").upper(),
    }

    # ---------------------------------------------------------
    # header_1_5 - owns hosting_model, hosting_details, has_details
    # ---------------------------------------------------------
    q4 = _get_spi_psi_response(request_details, 4)
    q5_comments = _get_spi_psi_response(request_details, 5, "comments")
    is_other = q4 == "Other"

    header_1_5_fields = {
        "hosting_model": q4,
        "hosting_details": q5_comments if is_other else "",
        "has_details": bool(is_other and q5_comments),
    }

    # ---------------------------------------------------------
    # header_2_1 - owns image_links entirely.
    # ---------------------------------------------------------

    architecture_filename = (
        SpiPsiResponse.objects
        .filter(
            request=request_details,
            question__qid=10,
        )
        .values_list(
            "filename",
            flat=True,
        )
        .first()
    )
    image_links = []
    if architecture_filename:
        filenames = [
            file_name.strip()
            for file_name in architecture_filename.split("||")
            if file_name.strip()
        ]
        base_path = os.path.join(
            settings.MEDIA_ROOT,
            "requestor",
            str(request_details.sgp_id),
        )
        backend_domain = settings.BACKEND_DOMAIN.rstrip("/")
        for file_name in filenames:
            full_path = os.path.join(
                base_path,
                file_name,
            )
            if not os.path.exists(full_path):
                continue
            encoded_file_name = quote(
                file_name,
                safe="()_-. ",
            ).replace(" ", "%20")
            image_links.append(
                {
                    "file_name": file_name,
                    "url": (
                        f"{backend_domain}/storage/"
                        f"serve-architecture-files/"
                        f"{request_details.sgp_id}/"
                        f"{encoded_file_name}/"
                    ),
                }
            )
    header_2_1_fields = {
        "image_links": image_links,
    }

    role_field_map = [
        ("Business Sponsor", "business_sponsor_first_name", "business_sponsor_last_name", "bussiness_sponser"),
        ("Business Lead", "business_lead_first_name", "business_lead_last_name", "business_lead"),
        ("Project Manager", "project_manager_first_name", "project_manager_last_name", "project_manager"),
        ("Solution Architect", "its_arch_first_name", "its_arch_last_name", "its_arch"),
    ]

    contacts = [
        {
            "role": role,
            "name": f"{getattr(request_details, first_field, '') or ''} "
                    f"{getattr(request_details, last_field, '') or ''}".strip(),
            "email": getattr(request_details, email_field, "") or "",
        }
        for role, first_field, last_field, email_field in role_field_map
    ]

    header_support_team_fields = {"contacts": contacts}
    fields_by_header = {
        "header_1_1": header_1_1_fields,
        "header_1_5": header_1_5_fields,
        "header_2_1": header_2_1_fields,
        "header_support_team": header_support_team_fields,
    }

    updated_headers = []
    unchanged_headers = []

    for header_name, derived_fields in fields_by_header.items():
        merged_json_data = {
            **existing_json_by_header.get(header_name, {}),
            **derived_fields,
        }

        changed = _upsert_json_section(
            request_details=request_details,
            header_name=header_name,
            new_json_data=merged_json_data,
            user=user,
        )

        (updated_headers if changed else unchanged_headers).append(header_name)

    return {
        "updated_headers": updated_headers,
        "unchanged_headers": unchanged_headers,
    }


def _get_spi_psi_response(request_details, question_id, attr="response"):
    row = (
        SpiPsiResponse.objects
        .filter(request=request_details, question_id=question_id)
        .first()
    )
    return getattr(row, attr, None) or "" if row else ""


def _upsert_json_section(request_details, header_name, new_json_data, user) -> bool:
    existing_row = (
        SarTemplateJsonData.objects.select_for_update()
        .filter(request=request_details, header_name=header_name, is_active=1)
        .first()
    )

    if existing_row and existing_row.json_data == new_json_data:
        return False

    section_status = (
        existing_row.section_status
        if existing_row
        else SarTemplateJsonData.STATUS_VALUES.get("DRAFT", 1)
    )

    if existing_row:
        SarJsonHistoryData.objects.create(
            original_id=existing_row.id,
            header_name=existing_row.header_name,
            json_data=existing_row.json_data,
            request=existing_row.request,
            created_by=existing_row.created_by,
            original_created_date=existing_row.created_date,
            archived_by=user,
        )
        existing_row.delete()

    SarTemplateJsonData.objects.create(
        header_name=header_name,
        json_data=new_json_data,
        request=request_details,
        section_status=section_status,
        needs_refresh=True,
        created_by=user,
        is_active=1,
    )

    return True


from django.db import transaction

from app.models import SarTemplateJsonData


def update_sar_go_live_date_json(
    request_details,
    go_live_date,
):
    formatted_go_live_date = (
        go_live_date.isoformat()
        if go_live_date
        else None
    )

    changed_headers = []

    sar_json_rows = (
        SarTemplateJsonData.objects.select_for_update()
        .filter(
            request=request_details,
            is_active=1,
            header_name__in=[
                "header_first_page",
                "header_3_1",
            ],
        )
        .order_by(
            "header_name",
            "-created_date",
        )
    )

    latest_rows = {}

    for row in sar_json_rows:
        if row.header_name not in latest_rows:
            latest_rows[row.header_name] = row

    first_page_row = latest_rows.get(
        "header_first_page"
    )

    if first_page_row:
        first_page_data = dict(
            first_page_row.json_data or {}
        )

        if (
            first_page_data.get("go_live_date")
            != formatted_go_live_date
        ):
            first_page_data["go_live_date"] = (
                formatted_go_live_date
            )

            first_page_row.json_data = first_page_data
            first_page_row.needs_refresh = True

            first_page_row.save(
                update_fields=[
                    "json_data",
                    "needs_refresh",
                    "updated_date",
                ]
            )

            changed_headers.append(
                "header_first_page"
            )
    header_3_1_row = latest_rows.get(
        "header_3_1"
    )

    if header_3_1_row:
        header_3_1_data = dict(
            header_3_1_row.json_data or {}
        )

        events = header_3_1_data.get(
            "events",
            [],
        )

        events_changed = False
        updated_events = []

        if isinstance(events, list):
            for event in events:
                if not isinstance(event, dict):
                    updated_events.append(event)
                    continue

                updated_event = dict(event)

                if (
                    updated_event.get("test_date")
                    != formatted_go_live_date
                ):
                    updated_event["test_date"] = (
                        formatted_go_live_date
                    )
                    events_changed = True

                updated_events.append(updated_event)

        if events_changed:
            header_3_1_data["events"] = updated_events

            header_3_1_row.json_data = (
                header_3_1_data
            )
            header_3_1_row.needs_refresh = True

            header_3_1_row.save(
                update_fields=[
                    "json_data",
                    "needs_refresh",
                    "updated_date",
                ]
            )

            changed_headers.append(
                "header_3_1"
            )

    return changed_headers
