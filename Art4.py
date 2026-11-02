@transaction.atomic
def publish_sar_on_leadership_approval(request_details, user) -> int:

    old_prod_onboarding = request_details.prod_onboarding_done

    request_details.prod_onboarding_done = not request_details.prod_onboarding_done
    request_details.save(
        update_fields=[
            "prod_onboarding_done",
        ]
    )

    if (
        request_details.solution_type != RequestorTeam.SOLUTION_TYPE_SAAS
        and old_prod_onboarding
    ):
        from app.services.findings_service import mark_findings_readonly
        mark_findings_readonly(request_details.sgp_id)

    latest_version = SarTemplateDataLog.objects.filter(
        request=request_details
    ).aggregate(Max("version_id"))["version_id__max"]

    next_version = (latest_version or 0) + 1

    existing_pdf_rows = list(SarTemplateDataPdf.objects.filter(request=request_details))
    archived_version = 0

    if existing_pdf_rows:
        log_rows = [
            SarTemplateDataLog(
                header_name=row.header_name,
                header_data=row.header_data,
                request=request_details,
                comment=row.comment,
                created_by=user,
                role=user.user_type,
                version_id=next_version,
            )
            for row in existing_pdf_rows
        ]
        SarTemplateDataLog.objects.bulk_create(log_rows)

        SarTemplateDataPdf.objects.filter(request=request_details).delete()
        archived_version = next_version

    active_data_rows = SarTemplateData.objects.filter(
        request=request_details,
        is_active=1,
    )

    pdf_rows = [
        SarTemplateDataPdf(
            header_name=row.header_name,
            header_data=row.header_data,
            request=request_details,
            comment=row.comment,
            created_by=user,
        )
        for row in active_data_rows
    ]
    SarTemplateDataPdf.objects.bulk_create(pdf_rows)

    SecurityFindingsPdf.objects.filter(request=request_details).delete()

    poam_findings = (
        SecurityFindings.objects.filter(
            request=request_details,
            is_active=True,
            tester_status=SecurityFindings.STATUS_NEW,
        )
        .exclude(
            residual_risk=SecurityFindings.SEVERITY_INFORMATIONAL,
        )
        .exclude(
            overall_risk=SecurityFindings.SEVERITY_INFORMATIONAL,
        )
        .exclude(
            severity=SecurityFindings.SEVERITY_INFORMATIONAL,
        )
    )

    if request_details.prod_onboarding_done:
        poam_findings = poam_findings.exclude(env=SecurityFindings.ENV_STAGING)

    findings_pdf_rows = [
        SecurityFindingsPdf(
            request=request_details,
            unique_id=f.unique_id,
            title=f.title,
            description=f.description,
            severity=f.severity,
            impact=f.impact,
            recommendation=f.recommendation,
            affected_device=f.affected_device,
            compensating_control=f.compensating_control,
            likelihood=f.likelihood,
            residual_risk=f.residual_risk,
            overall_risk=f.overall_risk,
            risk_status=f.risk_status,
            action_owner=f.action_owner,
            cwe_id=f.cwe_id,
            cwe_other=f.cwe_other,
            owasp_id=f.owasp_id,
            notes=f.notes,
            evidence_filenames=f.evidence_filenames,
            date_identified=f.date_identified,
            target_resolve_date=f.target_resolve_date,
            finding_category=f.finding_category,
            tester_comments=f.tester_comments,
            tester_response_date=f.tester_response_date,
            created_by=user,
        )
        for f in poam_findings
    ]

    SecurityFindingsPdf.objects.bulk_create(findings_pdf_rows)

    return archived_version
