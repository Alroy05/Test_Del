from django.db import transaction
from django.utils import timezone

from app.models import LogUpdate, RequestorTeam
from app.constants import ERRORS
from app.models.user import UserData
from app.utils import build_risk_treatment_findings_html, common_email_notification, get_notification_user_ids


def send_clearance_emails(request_details, user, ato_status):
    try:
        with transaction.atomic():
            _advance_status(user, request_details, ato_status)

        return {
            "success": True,
            "message": "Clearance emails sent successfully",
            "errors": [],
        }

    except Exception as ex:
        msg = ERRORS.get("syntax_error_access", "Syntax error or database access error")
        return _err(msg, [str(ex)])


def transfer_qa_tool_data_to_prod(
    request_instance,
):
    field_mapping = {
        # GHAS identifiers
        "ghas_org_name_prod": "ghas_org_name",
        "ghas_repo_names_prod": "ghas_repo_names",
        "ghas_scan_type_prod": "ghas_scan_type",

        # FOD identifiers
        "release_id_prod": "release_id",

        # Mendio identifiers
        "mend_product_name_prod": "mend_product_name",
        "mend_project_names_prod": "mend_project_names",
        "mend_project_tokens_prod": "mend_project_tokens",

        # Fetch values
        "fetch_ghas_prod": "fetch_ghas",
        "fetch_fod_prod": "fetch_fod",
        "fetch_mendio_prod": "fetch_mendio",
        "fetch_qualys_prod": "fetch_qualys",

        #CSPM is skipped intentionally
    }

    for prod_field, qa_field in field_mapping.items():
        setattr(
            request_instance,
            prod_field,
            getattr(request_instance, qa_field),
        )

    request_instance.save(
        update_fields=[
            *field_mapping.keys(),
            "updated_on",
        ]
    )

    return request_instance


def _advance_status(
    user,
    request_details: RequestorTeam,
    ato_status,
) -> None:
    old_status = request_details.status

    if (
        request_details.solution_type
        != RequestorTeam.SOLUTION_TYPE_SAAS
        and not request_details.prod_onboarding_done
    ):
        new_status = RequestorTeam.STATUS_PROD_ONBOARDING
    else:
        new_status = RequestorTeam.STATUS_CONTINUOUS_MONITORING

    LogUpdate.objects.create(
        request=request_details,
        event=LogUpdate.STATUS_EVENT,
        old_value=old_status,
        new_value=new_status,
        response_for=LogUpdate.RES_FOR_REQUEST,
        created_by=user,
        user_role=user.current_role,
    )

    old_sub_status = request_details.sub_status

    if (
        request_details.solution_type
        != RequestorTeam.SOLUTION_TYPE_SAAS
        and not request_details.prod_onboarding_done
    ):
        new_sub_status = RequestorTeam.SUB_STATUS_SEC_FINDINGS_VALID
    else:
        new_sub_status = RequestorTeam.SUB_STATUS_REPORT

    LogUpdate.objects.create(
        request=request_details,
        event=LogUpdate.STATUS_EVENT,
        old_value=old_sub_status,
        new_value=new_sub_status,
        response_for=LogUpdate.RES_FOR_SUB_STATUS,
        created_by=user,
        user_role=user.current_role,
    )

    request_details.status = new_status
    request_details.sub_status = new_sub_status

    if ato_status:
        old_ato_status = request_details.ato_status
        new_ato_status = int(ato_status)

        request_details.ato_status = new_ato_status

        LogUpdate.objects.create(
            request=request_details,
            event=LogUpdate.ATO_STATUS_EVENT,
            old_value=str(old_ato_status),
            new_value=str(new_ato_status),
            response_for="ATO Status",
            created_by=user,
            user_role=user.current_role,
        )

    # common_email_notification(
    #     requestor=request_details, email_template="status_change_csa", user=user
    # )
    if request_details.cycle_number == 1:
        transfer_qa_tool_data_to_prod(request_details)

    request_details.sar_status = RequestorTeam.SAR_CREATED
    request_details.last_publish_date = timezone.now()

    if not request_details.first_publish_date:
        request_details.first_publish_date = timezone.now()

    request_details.cycle_number += 1
    request_details.sar_ato_email_date = timezone.now()
    request_details.save()

    solution_team_user_ids = get_notification_user_ids(
        "request_owner",
        request_details,
    )

    if solution_team_user_ids:
        if new_status == RequestorTeam.STATUS_PROD_ONBOARDING:
            email_template = "assessment_complete_provisional"

        elif new_status == RequestorTeam.STATUS_CONTINUOUS_MONITORING:
            email_template = "assessment_complete_compliant"

        else:
            email_template = None

        if email_template:
            common_email_notification(
                requestor=request_details,
                email_template=email_template,
                user=user,
                extra_data={
                    "user_id": solution_team_user_ids,
                },
            )

    accepted_findings_html, mitigation_findings_html, has_findings = (
        build_risk_treatment_findings_html(
            request_details,
        )
    )

    if has_findings:
        business_owner_email = str(
            request_details.bussiness_sponser or ""
        ).strip()

        business_owner_name = (
            " ".join(
                value
                for value in [
                    str(
                        request_details.business_sponsor_first_name
                        or ""
                    ).strip(),
                    str(
                        request_details.business_sponsor_last_name
                        or ""
                    ).strip(),
                ]
                if value
            )
            or "Business Owner"
        )

        solution_team_emails = []

        solution_team_users = UserData.objects.filter(
            id__in=solution_team_user_ids,
            is_active=True,
            is_deleted=False,
        )

        for solution_team_user in solution_team_users:
            solution_team_email = str(
                solution_team_user.email or ""
            ).strip()

            if solution_team_email:
                solution_team_emails.append(solution_team_email)

        solution_team_emails = list(
            dict.fromkeys(solution_team_emails)
        )


        leadership_emails = []

        leadership_users = (
            request_details.get_assigned_leadership_users()
            .filter(
                is_active=True,
                is_deleted=False,
            )
        )

        for leadership_user in leadership_users:
            leadership_email = str(
                leadership_user.email or ""
            ).strip()

            if leadership_email:
                leadership_emails.append(leadership_email)

        leadership_emails = list(
            dict.fromkeys(leadership_emails)
        )

        if business_owner_email:
            common_email_notification(
                requestor=request_details,
                email_template="findings_review_complete",
                user=user,
                extra_data={
                    "user_id": [business_owner_email],
                    "business_owner_name": business_owner_name,
                    "accepted_findings_html": accepted_findings_html,
                    "mitigation_findings_html": mitigation_findings_html,
                    "solution_team_emails": solution_team_emails,
                    "leadership_emails": leadership_emails,
                },
            )


def _err(message: str, errors: list) -> dict:
    return {"success": False, "message": message, "errors": errors}




