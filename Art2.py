### EarLier code
def get_observation_table(data, download_pdf=None) -> dict:
    security_observations_html = {"Critical": "", "High": "", "Medium": "", "Low": ""}

    if data.get("Critical"):
        i = 1
        for value in data["Critical"].values():
            value["numbering"] = f"4.1.{i}"
            security_observations_html["Critical"] += get_observation_table_html(
                value, download_pdf
            )
            i += 1
    else:
        security_observations_html["Critical"] = (
            "There were no critical-risk findings discovered during this review"
        )

    if data.get("High"):
        i = 1
        for value in data["High"].values():
            value["numbering"] = f"4.2.{i}"
            security_observations_html["High"] += get_observation_table_html(
                value, download_pdf
            )
            i += 1
    else:
        security_observations_html["High"] = (
            "There were no high-risk findings discovered during this review"
        )

    if data.get("Medium"):
        i = 1
        for value in data["Medium"].values():
            value["numbering"] = f"4.3.{i}"
            security_observations_html["Medium"] += get_observation_table_html(
                value, download_pdf
            )
            i += 1
    else:
        security_observations_html["Medium"] = (
            "There were no medium-risk findings discovered during this review"
        )

    if data.get("Low"):
        i = 1
        for value in data["Low"].values():
            value["numbering"] = f"4.4.{i}"
            security_observations_html["Low"] += get_observation_table_html(
                value, download_pdf
            )
            i += 1
    else:
        security_observations_html["Low"] = (
            "There were no low-risk findings discovered during this review"
        )

    return security_observations_html


def get_observation_table_html(data, download_pdf=None) -> str:

    finding_category_name = (
        SecurityFindings.FINDING_CATEGORY_CHOICES.get(data.get("finding_category"), "-")
        if data.get("finding_category")
        else "-"
    )

    cb_severity = {"low": "f", "medium": "f", "high": "f", "critical": "f"}
    cb_likelihood = {1: "f", 2: "f", 3: "f", 4: "f"}
    cb_overall = {"low": "f", "medium": "f", "high": "f", "critical": "f"}

    mark_severity = {"low": "☐", "medium": "☐", "high": "☐", "critical": "☐"}
    mark_likelihood = {1: "☐", 2: "☐", 3: "☐", 4: "☐"}
    mark_overall = {"low": "☐", "medium": "☐", "high": "☐", "critical": "☐"}
    mark_residual = {"low": "☐", "medium": "☐", "high": "☐", "critical": "☐"}

    pdf_attr_severity = {"low": "", "medium": "", "high": "", "critical": ""}
    pdf_attr_likelihood = {1: "", 2: "", 3: "", 4: ""}
    pdf_attr_overall = {"low": "", "medium": "", "high": "", "critical": ""}
    pdf_attr_residual = {"low": "", "medium": "", "high": "", "critical": ""}

    sev = data.get("severity")
    if sev == SecurityFindings.SEVERITY_LOW:
        cb_severity["low"] = "t"
        mark_severity["low"] = "☒"
        pdf_attr_severity["low"] = 'checked="checked"'
    elif sev == SecurityFindings.SEVERITY_MEDIUM:
        cb_severity["medium"] = "t"
        mark_severity["medium"] = "☒"
        pdf_attr_severity["medium"] = 'checked="checked"'
    elif sev == SecurityFindings.SEVERITY_HIGH:
        cb_severity["high"] = "t"
        mark_severity["high"] = "☒"
        pdf_attr_severity["high"] = 'checked="checked"'
    elif sev == SecurityFindings.SEVERITY_CRITICAL:
        cb_severity["critical"] = "t"
        mark_severity["critical"] = "☒"
        pdf_attr_severity["critical"] = 'checked="checked"'

    lk = data.get("likelihood")
    if lk in (1, 2, 3, 4):
        cb_likelihood[lk] = "t"
        mark_likelihood[lk] = "☒"
        pdf_attr_likelihood[lk] = 'checked="checked"'

    overall_name = (data.get("overall_risk_name") or "").lower()
    if overall_name in cb_overall:
        cb_overall[overall_name] = "t"
        mark_overall[overall_name] = "☒"
        pdf_attr_overall[overall_name] = 'checked="checked"'

    residual = data.get("residual_risk")
    if residual == SecurityFindings.SEVERITY_LOW:
        mark_residual["low"] = "☒"
        pdf_attr_residual["low"] = 'checked="checked"'
    elif residual == SecurityFindings.SEVERITY_MEDIUM:
        mark_residual["medium"] = "☒"
        pdf_attr_residual["medium"] = 'checked="checked"'
    elif residual == SecurityFindings.SEVERITY_HIGH:
        mark_residual["high"] = "☒"
        pdf_attr_residual["high"] = 'checked="checked"'
    elif residual == SecurityFindings.SEVERITY_CRITICAL:
        mark_residual["critical"] = "☒"
        pdf_attr_residual["critical"] = 'checked="checked"'

    risk_status_html = ""
    if data.get("risk_status") == SecurityFindings.STATUS_ACCEPT:
        risk_status_html = (
            '<p style="margin-bottom:0in;"><u><span><b>Risk Status</b></span></u></p>'
            "<h6>Accept</h6>"
        )
    elif data.get("risk_status") == SecurityFindings.STATUS_MITIGATE:
        risk_status_html = (
            '<p style="margin-bottom:0in;"><u><span><b>Risk Status</b></span></u></p>'
            "<h6>Mitigate</h6>"
        )

    if download_pdf is not None:
        severity_html = (
            f'<p style="margin:0in;"><input {pdf_attr_severity["low"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Low</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_severity["medium"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Medium</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_severity["high"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>High</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_severity["critical"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Critical</span></p>'
        )
        likelihood_html = (
            f'<p style="margin:0in;"><input {pdf_attr_likelihood[1]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Unlikely (1+ years)</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_likelihood[2]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Possible (6-12 months)</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_likelihood[3]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Probable (1-6 months)</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_likelihood[4]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Likely (0-30 days)</span></p>'
        )
        risk_html = (
            f'<p style="margin:0in;"><input {pdf_attr_overall["low"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Low</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_overall["medium"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Medium</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_overall["high"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>High</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_overall["critical"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Critical</span></p>'
        )
        residual_risk_html = (
            f'<input {pdf_attr_residual["low"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Low</span>'
            f'<input {pdf_attr_residual["medium"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Medium</span>'
            f'<input {pdf_attr_residual["high"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>High</span>'
            f'<input {pdf_attr_residual["critical"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Critical</span>'
        )
    else:
        severity_html = (
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_severity["low"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_severity["low"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Low</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_severity["medium"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_severity["medium"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Medium</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_severity["high"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_severity["high"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>High</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_severity["critical"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_severity["critical"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Critical</span></p>'
        )
        likelihood_html = (
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_likelihood[1]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span style="font-size:10.0pt;">{mark_likelihood[1]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Unlikely (1+ years)</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_likelihood[2]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span style="font-size:10.0pt;">{mark_likelihood[2]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Possible (6-12 months)</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_likelihood[3]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span style="font-size:10.0pt;">{mark_likelihood[3]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Probable (1-6 months)</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_likelihood[4]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span style="font-size:10.0pt;">{mark_likelihood[4]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Likely (0-30 days)</span></p>'
        )
        risk_html = (
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_overall["low"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_overall["low"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Low</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_overall["medium"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_overall["medium"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Medium</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_overall["high"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_overall["high"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>High</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_overall["critical"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_overall["critical"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Critical</span></p>'
        )
        residual_risk_html = (
            f'<span style="font-size:10.0pt;">{mark_residual["low"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Low</span>'
            f'<span style="font-size:10.0pt;">{mark_residual["medium"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Medium</span>'
            f'<span style="font-size:10.0pt;">{mark_residual["high"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">High</span>'
            f'<span style="font-size:10.0pt;">{mark_residual["critical"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Critical</span>'
        )

    second_style = "200.95pt"

    def fmt_date(val):
        if not val:
            return ""
        try:
            if isinstance(val, str):
                return datetime.strptime(val, "%Y-%m-%d").strftime("%d-%b-%Y")
            return val.strftime("%d-%b-%Y")
        except Exception:
            return str(val)

    identified_html = fmt_date(data.get("date_identified")) or fmt_date(
        data.get("tester_response_date")
    )

    finding_category_html = fmt_date(data.get("finding_category", "-"))

    resolve_date = fmt_date(data.get("target_resolve_date")) or "N/A"

    affected_device = html.escape(str(data.get("affected_device", "")))

    affected_device_html = ""
    if data.get("affected_device"):
        affected_device_html = (
            f"<br><p><u><span><b>Affected Components: </b></span></u></p>"
            f'<span style="font-family:Arial; white-space: pre-wrap;">'
            f"<h6>{affected_device}</h6></span>"
        )

    comp_control = html.escape(str(data.get("compensating_control", "")))

    remediation_html = ""
    if data.get("compensating_control") and data["compensating_control"] != "-":
        second_style = "350.95pt"
        remediation_html = (
            f"<br><p><u><span><b>Compensating Control: </b></span></u></p>"
            f'<span style="font-family:Arial; white-space: pre-wrap;">'
            f"<h6>{comp_control}</h6></span>"
        )

    notes = html.escape(str(data.get("notes", "")))

    finding_notes_html = ""
    if data.get("notes") and data["notes"] != "-":
        finding_notes_html = (
            f'<tr class="table-border" style="height:17.15pt;">'
            f'<td class="table-border" colspan="3" valign="top" '
            f'style="border-top:none;padding:0in 5.4pt 0in 5.4pt;height:17.15pt;">'
            f"<p><u><span><b>Notes: </b></span></u></p>"
            f'<span style="font-family:Arial; white-space: pre-wrap;">'
            f"<h6>{notes}</h6></span></td></tr>"
        )

    if data.get("cwe_id") is not None:
        cwe_text = f'{data.get("cwe_category_name", "")} - {data.get("cwe_own_id", "")}'
        if data.get("cwe_own_id") == 0 and data.get("cwe_other"):
            cwe_text = f'{cwe_text} - {data.get("cwe_other", "")}'
    else:
        cwe_text = data.get("cwe_other") or "-"

    description = html.escape(str(data.get("description", "")))
    impact = html.escape(str(data.get("impact", "")))
    recommendation = html.escape(str(data.get("recommendation", "")))
    title = html.escape(str(data.get("title", "")))
    action_owner = html.escape(str(data.get("action_owner", "")))
    unique_id = data.get("unique_id")
    unique_id_html = f"#{unique_id} " if unique_id else "" 

    html_code = f"""<table class="table-border" border="1" cellspacing="0" cellpadding="0" width="840" style="width: 8.75in; border: none;">
                    <thead>
                        <tr class="table-border" style="height:16.05pt;">
                            <td class="table-border" width="840" colspan="3" valign="top" style="width:8.75in;padding:0in 5.4pt 0in 5.4pt;height:16.05pt;">
                                <p><a name="_Hlk65858326"><b><span style="color:#00338D;">{data.get("numbering", "")} {finding_category_name}: {unique_id_html} {title}</span></b></a></p>
                                <p><a name="_Hlk65858326"><b><span style="color:#00338D;">CWE: {cwe_text}</span></b></a></p>
                            </td>
                        </tr>
                        <tr class="table-border">
                            <td class="table-border" width="246" valign="top" style="width:184.25pt;border-top:none;padding:0in 5.4pt 0in 5.4pt;height:100.95pt;">
                                <p><span style="white-space: pre-wrap;"><h6>{description}</h6></span></p>
                            </td>
                            <td class="table-border" width="120" rowspan="2" valign="top" style="width:1.25in;border-top:none;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:100.95pt;">
                                <p style="margin-bottom:0in; white-space: nowrap;"><u><span><b>Finding Category</b></span></u></p>
                                <h6>{finding_category_html}</h6>
                                <p style="margin-bottom:0in;"><u><span><b>Date Identified</b></span></u></p>
                                <h6>{identified_html}</h6>{risk_status_html}
                                <p style="margin:0in;"><u><span><b>Date to Resolve</b></span></u></p>
                                <h6>{resolve_date}</h6>
                                <p style="margin:0in;"><u><span><b>Action Owner</b></span></u></p>
                                <h6>{action_owner}</h6>
                            </td>
                            <td class="table-border" width="474" valign="top" style="width:355.75pt;border-top:none;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:{second_style};">
                                <p style="margin-bottom:2.0pt;"><u><span><b>Initial Risk: </b></span></u></p>
                                <table border="1" cellspacing="0" cellpadding="0" style="border: none;">
                                    <tbody>
                                        <tr class="table-border" style="border:none;">
                                            <td class="table-border" width="130" valign="top" style="width:97.6pt;border:none;background:#002060;padding:0in 5.4pt 0in 5.4pt;">
                                                <p align="center" style="margin:0in;text-align:center;"><b><span style="font-family:Arial;color:white;">Impact / Severity</span></b></p>
                                            </td>
                                            <td class="table-border" width="186" valign="top" style="width:139.5pt;border:none;background:#002060;padding:0in 5.4pt 0in 5.4pt;">
                                                <p align="center" style="margin:0in;text-align:center;"><b><span style="font-family:Arial;color:white;">Likelihood</span></b></p>
                                            </td>
                                            <td class="table-border" width="149" valign="top" style="width:111.5pt;border:none;background:#002060;padding:0in 5.4pt 0in 5.4pt;">
                                                <p align="center" style="margin:0in;text-align:center;"><b><span style="font-family:Arial;color:white;">Risk</span></b></p>
                                            </td>
                                        </tr>
                                        <tr class="table-border" style="border-top:none;">
                                            <td class="table-border" width="130" valign="top" style="width:97.6pt;border-top:none;padding:0in 5.4pt 0in 5.4pt;">
                                                <h6>{severity_html}</h6></td>
                                            <td class="table-border" width="186" valign="top" style="width:139.5pt;border-top:none;border-left:none;padding:0in 5.4pt 0in 5.4pt;">
                                                <h6>{likelihood_html}</h6></td>
                                            <td class="table-border" width="149" valign="top" style="width:111.5pt;border-top:none;border-left:none;padding:0in 5.4pt 0in 5.4pt;">
                                                <h6>{risk_html}</h6></td>
                                        </tr>
                                    </tbody>
                                </table>{affected_device_html}{remediation_html}
                            </td>
                        </tr>
                        <tr class="table-border">
                            <td class="table-border" width="246" valign="top" style="width:184.25pt;border-top:none;padding:0in 5.4pt 0in 5.4pt;">
                                <p><u><span><b>Impact Description: </b></span></u><span style="font-family:Arial;"></span></p>
                                <p><span style="white-space: pre-wrap;"><h6>{impact}</h6></span></p>
                            </td>
                            <td class="table-border" width="474" valign="top" style="width:355.75pt;border-top:none;border-left:none;padding:0in 5.4pt 0in 5.4pt;">
                                <p style="margin:0in;"><u><span><b>Residual Risk: </b></span></u>{residual_risk_html}</p>
                                <br>
                                <p><u><span><b>Recommended Remediation: </b></span></u></p>
                                <p><span style="font-family:Arial;white-space: pre-wrap;"><h6>{recommendation}</h6></span></p>
                            </td>
                        </tr>{finding_notes_html}
                    </thead>
                </table>
                <br>"""

    return html_code


####### New Code

def get_observation_table_html(data, download_pdf=None) -> str:

    finding_category_name = (
        SecurityFindings.FINDING_CATEGORY_CHOICES.get(data.get("finding_category"), "-")
        if data.get("finding_category")
        else "-"
    )

    cb_severity = {"low": "f", "medium": "f", "high": "f", "critical": "f"}
    cb_likelihood = {1: "f", 2: "f", 3: "f", 4: "f"}
    cb_overall = {"low": "f", "medium": "f", "high": "f", "critical": "f"}

    mark_severity = {"low": "☐", "medium": "☐", "high": "☐", "critical": "☐"}
    mark_likelihood = {1: "☐", 2: "☐", 3: "☐", 4: "☐"}
    mark_overall = {"low": "☐", "medium": "☐", "high": "☐", "critical": "☐"}
    mark_residual = {"low": "☐", "medium": "☐", "high": "☐", "critical": "☐"}

    pdf_attr_severity = {"low": "", "medium": "", "high": "", "critical": ""}
    pdf_attr_likelihood = {1: "", 2: "", 3: "", 4: ""}
    pdf_attr_overall = {"low": "", "medium": "", "high": "", "critical": ""}
    pdf_attr_residual = {"low": "", "medium": "", "high": "", "critical": ""}

    sev = data.get("severity")
    if sev == SecurityFindings.SEVERITY_LOW:
        cb_severity["low"] = "t"
        mark_severity["low"] = "☒"
        pdf_attr_severity["low"] = 'checked="checked"'
    elif sev == SecurityFindings.SEVERITY_MEDIUM:
        cb_severity["medium"] = "t"
        mark_severity["medium"] = "☒"
        pdf_attr_severity["medium"] = 'checked="checked"'
    elif sev == SecurityFindings.SEVERITY_HIGH:
        cb_severity["high"] = "t"
        mark_severity["high"] = "☒"
        pdf_attr_severity["high"] = 'checked="checked"'
    elif sev == SecurityFindings.SEVERITY_CRITICAL:
        cb_severity["critical"] = "t"
        mark_severity["critical"] = "☒"
        pdf_attr_severity["critical"] = 'checked="checked"'

    lk = data.get("likelihood")
    if lk in (1, 2, 3, 4):
        cb_likelihood[lk] = "t"
        mark_likelihood[lk] = "☒"
        pdf_attr_likelihood[lk] = 'checked="checked"'

    overall_name = (data.get("overall_risk_name") or "").lower()
    if overall_name in cb_overall:
        cb_overall[overall_name] = "t"
        mark_overall[overall_name] = "☒"
        pdf_attr_overall[overall_name] = 'checked="checked"'

    residual = data.get("residual_risk")
    if residual == SecurityFindings.SEVERITY_LOW:
        mark_residual["low"] = "☒"
        pdf_attr_residual["low"] = 'checked="checked"'
    elif residual == SecurityFindings.SEVERITY_MEDIUM:
        mark_residual["medium"] = "☒"
        pdf_attr_residual["medium"] = 'checked="checked"'
    elif residual == SecurityFindings.SEVERITY_HIGH:
        mark_residual["high"] = "☒"
        pdf_attr_residual["high"] = 'checked="checked"'
    elif residual == SecurityFindings.SEVERITY_CRITICAL:
        mark_residual["critical"] = "☒"
        pdf_attr_residual["critical"] = 'checked="checked"'

    risk_status_html = ""
    if data.get("risk_status") == SecurityFindings.STATUS_ACCEPT:
        risk_status_html = (
            '<p style="margin-bottom:0in;"><u><span><b>Risk Status</b></span></u></p>'
            "<h6>Accept</h6>"
        )
    elif data.get("risk_status") == SecurityFindings.STATUS_MITIGATE:
        risk_status_html = (
            '<p style="margin-bottom:0in;"><u><span><b>Risk Status</b></span></u></p>'
            "<h6>Mitigate</h6>"
        )

    if download_pdf is not None:
        severity_html = (
            f'<p style="margin:0in;"><input {pdf_attr_severity["low"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Low</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_severity["medium"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Medium</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_severity["high"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>High</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_severity["critical"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Critical</span></p>'
        )
        likelihood_html = (
            f'<p style="margin:0in;"><input {pdf_attr_likelihood[1]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Unlikely (1+ years)</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_likelihood[2]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Possible (6-12 months)</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_likelihood[3]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Probable (1-6 months)</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_likelihood[4]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Likely (0-30 days)</span></p>'
        )
        risk_html = (
            f'<p style="margin:0in;"><input {pdf_attr_overall["low"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Low</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_overall["medium"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Medium</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_overall["high"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>High</span></p>'
            f'<p style="margin:0in;"><input {pdf_attr_overall["critical"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Critical</span></p>'
        )
        residual_risk_html = (
            f'<input {pdf_attr_residual["low"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Low</span>'
            f'<input {pdf_attr_residual["medium"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Medium</span>'
            f'<input {pdf_attr_residual["high"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>High</span>'
            f'<input {pdf_attr_residual["critical"]} style="width:300px;" type="checkbox" value="kpmg_high_confidential"><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Critical</span>'
        )
    else:
        severity_html = (
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_severity["low"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_severity["low"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Low</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_severity["medium"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_severity["medium"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Medium</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_severity["high"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_severity["high"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>High</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_severity["critical"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_severity["critical"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Critical</span></p>'
        )
        likelihood_html = (
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_likelihood[1]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span style="font-size:10.0pt;">{mark_likelihood[1]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Unlikely (1+ years)</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_likelihood[2]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span style="font-size:10.0pt;">{mark_likelihood[2]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Possible (6-12 months)</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_likelihood[3]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span style="font-size:10.0pt;">{mark_likelihood[3]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Probable (1-6 months)</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_likelihood[4]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span style="font-size:10.0pt;">{mark_likelihood[4]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Likely (0-30 days)</span></p>'
        )
        risk_html = (
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_overall["low"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_overall["low"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Low</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_overall["medium"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_overall["medium"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Medium</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_overall["high"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_overall["high"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>High</span></p>'
            f'<p style="margin:0in;"><w:sdt checkbox="t" checkboxischecked="{cb_overall["critical"]}" checkboxvaluechecked="☒" checkboxvalueunchecked="☐" checkboxfontchecked="MS Gothic" checkboxfontunchecked="MS Gothic"><span>{mark_overall["critical"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span></w:sdt><span style="font-size:10.0pt;font-family:Arial;"> </span><span>Critical</span></p>'
        )
        residual_risk_html = (
            f'<span style="font-size:10.0pt;">{mark_residual["low"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Low</span>'
            f'<span style="font-size:10.0pt;">{mark_residual["medium"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Medium</span>'
            f'<span style="font-size:10.0pt;">{mark_residual["high"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">High</span>'
            f'<span style="font-size:10.0pt;">{mark_residual["critical"]}</span><span style="font-size:10.0pt;font-family:Arial;"></span><span style="font-size:10.0pt;font-family:Arial;"> </span><span style="font-family:Arial;">Critical</span>'
        )

    second_style = "200.95pt"

    def fmt_date(val):
        if not val:
            return ""
        try:
            if isinstance(val, str):
                return datetime.strptime(val, "%Y-%m-%d").strftime("%d-%b-%Y")
            return val.strftime("%d-%b-%Y")
        except Exception:
            return str(val)

    identified_html = fmt_date(data.get("date_identified")) or fmt_date(
        data.get("tester_response_date")
    )

    finding_category_html = fmt_date(data.get("finding_category", "-"))

    resolve_date = fmt_date(data.get("target_resolve_date")) or "N/A"

    affected_device = html.escape(str(data.get("affected_device", "")))

    affected_device_html = ""
    if data.get("affected_device"):
        affected_device_html = (
            f"<br><p><u><span><b>Affected Components: </b></span></u></p>"
            f'<span style="font-family:Arial; white-space: pre-wrap;">'
            f"<h6>{affected_device}</h6></span>"
        )

    comp_control = html.escape(str(data.get("compensating_control", "")))

    remediation_html = ""
    if data.get("compensating_control") and data["compensating_control"] != "-":
        second_style = "350.95pt"
        remediation_html = (
            f"<br><p><u><span><b>Compensating Control: </b></span></u></p>"
            f'<span style="font-family:Arial; white-space: pre-wrap;">'
            f"<h6>{comp_control}</h6></span>"
        )

    notes = html.escape(str(data.get("notes", "")))

    finding_notes_html = ""
    if data.get("notes") and data["notes"] != "-":
        finding_notes_html = (
            f'<tr class="table-border" style="height:17.15pt;">'
            f'<td class="table-border" colspan="3" valign="top" '
            f'style="border-top:none;padding:0in 5.4pt 0in 5.4pt;height:17.15pt;">'
            f"<p><u><span><b>Notes: </b></span></u></p>"
            f'<span style="font-family:Arial; white-space: pre-wrap;">'
            f"<h6>{notes}</h6></span></td></tr>"
        )

    if data.get("cwe_id") is not None:
        cwe_text = f'{data.get("cwe_category_name", "")} - {data.get("cwe_own_id", "")}'
        if data.get("cwe_own_id") == 0 and data.get("cwe_other"):
            cwe_text = f'{cwe_text} - {data.get("cwe_other", "")}'
    else:
        cwe_text = data.get("cwe_other") or "-"

    description = html.escape(str(data.get("description", "")))
    impact = html.escape(str(data.get("impact", "")))
    recommendation = html.escape(str(data.get("recommendation", "")))
    title = html.escape(str(data.get("title", "")))
    action_owner = html.escape(str(data.get("action_owner", "")))
    unique_id = data.get("unique_id")
    unique_id_html = f"#{unique_id} " if unique_id else "" 

    html_code = f"""<table class="table-border" border="1" cellspacing="0" cellpadding="0" width="840" style="width: 8.75in; border: none;">
                <thead>
                    <tr class="table-border" style="height:16.05pt;">
                        <td
                            class="table-border"
                            width="840"
                            colspan="3"
                            valign="top"
                            style="
                                width:8.75in;
                                padding:4pt 5.4pt;
                                height:16.05pt;
                            "
                        >
                            <!--
                                border="1" is intentional: mPDF keeps a single global
                                "table border attribute" flag, and a nested table with
                                border="0" resets it, which strips the internal borders
                                from every outer-table cell rendered after this one.
                                The visible border is still removed via style="border:none".
                            -->
                            <table
                                width="100%"
                                border="1"
                                cellspacing="0"
                                cellpadding="0"
                                style="
                                    width:100%;
                                    border:none;
                                    border-collapse:collapse;
                                "
                            >
                                <tr>
                                    <td
                                        valign="top"
                                        style="
                                            border:none;
                                            padding:0 8px 2px 0;
                                        "
                                    >
                                        <p style="margin:0;">
                                            <a name="_Hlk65858326">
                                                <b>
                                                    <span style="color:#00338D;">
                                                        {data.get("numbering", "")}
                                                        {finding_category_name}: {title}
                                                    </span>
                                                </b>
                                            </a>
                                        </p>
                                    </td>

                                    <td
                                        width="170"
                                        rowspan="2"
                                        valign="middle"
                                        align="right"
                                        style="
                                            width:170px;
                                            border:none;
                                            padding:0;
                                            text-align:right;
                                            vertical-align:middle;
                                            white-space:nowrap;
                                        "
                                    >
                                        <span
                                            style="
                                                display:inline-block;
                                                background-color:#002060;
                                                color:#FFFFFF !important;
                                                padding:5px 10px;
                                                border-radius:3px;
                                                font-weight:bold;
                                                line-height:1.2;
                                            "
                                        >
                                            {unique_id_html}
                                        </span>
                                    </td>
                                </tr>

                                <!-- CWE row -->
                                <tr>
                                    <td
                                        valign="top"
                                        style="
                                            border:none;
                                            padding:2px 8px 0 0;
                                        "
                                    >
                                        <p style="margin:0;">
                                            <b>
                                                <span style="color:#00338D;">
                                                    CWE: {cwe_text}
                                                </span>
                                            </b>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr class="table-border">
                        <td class="table-border" width="246" valign="top" style="width:184.25pt;border-top:none;padding:0in 5.4pt 0in 5.4pt;height:100.95pt;">
                            <p><span style="white-space: pre-wrap;"><h6>{description}</h6></span></p>
                        </td>
                        <td class="table-border" width="120" rowspan="2" valign="top" style="width:1.25in;border-top:none;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:100.95pt;">
                            <p style="margin-bottom:0in; white-space: nowrap;"><u><span><b>Finding Category</b></span></u></p>
                            <h6>{finding_category_html}</h6>
                            <p style="margin-bottom:0in;"><u><span><b>Date Identified</b></span></u></p>
                            <h6>{identified_html}</h6>{risk_status_html}
                            <p style="margin:0in;"><u><span><b>Date to Resolve</b></span></u></p>
                            <h6>{resolve_date}</h6>
                            <p style="margin:0in;"><u><span><b>Action Owner</b></span></u></p>
                            <h6>{action_owner}</h6>
                        </td>
                        <td class="table-border" width="474" valign="top" style="width:355.75pt;border-top:none;border-left:none;padding:0in 5.4pt 0in 5.4pt;height:{second_style};">
                            <p style="margin-bottom:2.0pt;"><u><span><b>Initial Risk: </b></span></u></p>
                            <table border="1" cellspacing="0" cellpadding="0" style="border: none;">
                                <tbody>
                                    <tr class="table-border" style="border:none;">
                                        <td class="table-border" width="130" valign="top" style="width:97.6pt;border:none;background:#002060;padding:0in 5.4pt 0in 5.4pt;">
                                            <p align="center" style="margin:0in;text-align:center;"><b><span style="font-family:Arial;color:white;">Impact / Severity</span></b></p>
                                        </td>
                                        <td class="table-border" width="186" valign="top" style="width:139.5pt;border:none;background:#002060;padding:0in 5.4pt 0in 5.4pt;">
                                            <p align="center" style="margin:0in;text-align:center;"><b><span style="font-family:Arial;color:white;">Likelihood</span></b></p>
                                        </td>
                                        <td class="table-border" width="149" valign="top" style="width:111.5pt;border:none;background:#002060;padding:0in 5.4pt 0in 5.4pt;">
                                            <p align="center" style="margin:0in;text-align:center;"><b><span style="font-family:Arial;color:white;">Risk</span></b></p>
                                        </td>
                                    </tr>
                                    <tr class="table-border" style="border-top:none;">
                                        <td class="table-border" width="130" valign="top" style="width:97.6pt;border-top:none;padding:0in 5.4pt 0in 5.4pt;">
                                            <h6>{severity_html}</h6></td>
                                        <td class="table-border" width="186" valign="top" style="width:139.5pt;border-top:none;border-left:none;padding:0in 5.4pt 0in 5.4pt;">
                                            <h6>{likelihood_html}</h6></td>
                                        <td class="table-border" width="149" valign="top" style="width:111.5pt;border-top:none;border-left:none;padding:0in 5.4pt 0in 5.4pt;">
                                            <h6>{risk_html}</h6></td>
                                    </tr>
                                </tbody>
                            </table>{affected_device_html}{remediation_html}
                        </td>
                    </tr>
                    <tr class="table-border">
                        <td class="table-border" width="246" valign="top" style="width:184.25pt;border-top:none;padding:0in 5.4pt 0in 5.4pt;">
                            <p><u><span><b>Impact Description: </b></span></u><span style="font-family:Arial;"></span></p>
                            <p><span style="white-space: pre-wrap;"><h6>{impact}</h6></span></p>
                        </td>
                        <td class="table-border" width="474" valign="top" style="width:355.75pt;border-top:none;border-left:none;padding:0in 5.4pt 0in 5.4pt;">
                            <p style="margin:0in;"><u><span><b>Residual Risk: </b></span></u>{residual_risk_html}</p>
                            <br>
                            <p><u><span><b>Recommended Remediation: </b></span></u></p>
                            <p><span style="font-family:Arial;white-space: pre-wrap;"><h6>{recommendation}</h6></span></p>
                        </td>
                    </tr>{finding_notes_html}
                </thead>
            </table>
            <br>"""

    return html_code

=============


<?php

declare(strict_types=1);

use Mpdf\HTMLParserMode;
use Mpdf\Mpdf;

function debug_log(string $message, array $context = []): void
{
    // Debug logging intentionally disabled for production PDF generation.
}

function fail_pdf(string $message, int $code = 1): void
{
    debug_log('Fatal PDF error', ['message' => $message, 'code' => $code]);
    fwrite(STDERR, $message . PHP_EOL);
    exit($code);
}

function find_autoload(): ?string
{
    $paths = [
        __DIR__ . '/vendor/autoload.php',
        __DIR__ . '/../../../../vendor/autoload.php',
        __DIR__ . '/../../../vendor/autoload.php',
        __DIR__ . '/../../vendor/autoload.php',
    ];

    foreach ($paths as $path) {
        if (is_file($path) && is_readable($path)) {
            return $path;
        }
    }

    $directory = __DIR__;
    for ($index = 0; $index < 10; $index++) {
        $path = $directory . '/vendor/autoload.php';
        if (is_file($path) && is_readable($path)) {
            return $path;
        }

        $parent = dirname($directory);
        if ($parent === $directory) {
            break;
        }
        $directory = $parent;
    }

    return null;
}

function read_payload(): array
{
    $raw = trim((string) stream_get_contents(STDIN));
    if ($raw === '') {
        return [];
    }

    $payload = json_decode($raw, true);
    if (!is_array($payload)) {
        fail_pdf('Invalid JSON payload: ' . json_last_error_msg(), 2);
    }

    return $payload;
}

function normalize_paths(string $html, string $targetBaseUrl): string
{
    $targetBaseUrl = rtrim($targetBaseUrl, '/') . '/';
    $sourceUrls = [
        'https://gisgsolutionreviewone.stg.kworld.kpmg.com/api/',
        'https://gisgsolutionreviewoneone.stg.kworld.kpmg.com/api/',
    ];

    foreach ($sourceUrls as $sourceUrl) {
        $html = str_replace('src="' . $sourceUrl, 'src="' . $targetBaseUrl, $html);
        $html = str_replace("src='" . $sourceUrl, "src='" . $targetBaseUrl, $html);
        $html = str_replace('href="' . $sourceUrl, 'href="' . $targetBaseUrl, $html);
        $html = str_replace("href='" . $sourceUrl, "href='" . $targetBaseUrl, $html);
    }

    return $html;
}

function clean_residual_risk_badge(string $html): string
{
    if (trim($html) === '') {
        return '';
    }

    return preg_replace_callback(
        '#<h4([^>]*)>(.*?)</h4>#is',
        static function (array $matches): string {
            $attrs = $matches[1];
            $inner = $matches[2];

            $inner = preg_replace('/(?:&nbsp;|\x{00A0})+/u', ' ', $inner) ?? $inner;
            $inner = preg_replace('/>\s+/', '>', $inner) ?? $inner;
            $inner = preg_replace('/\s+</', '<', $inner) ?? $inner;
            $inner = trim($inner);

            $attrs = preg_replace('/\salign\s*=\s*(["\']).*?\1/i', '', $attrs) ?? $attrs;
            $attrs .= ' align="left"';

            return '<h4' . $attrs . ' style="text-align:left;margin-left:0.5in;">' . $inner . '</h4>';
        },
        $html
    ) ?? $html;
}

function clean_html(string $html): string
{
    $html = str_replace("\0", '', $html);
    $html = preg_replace('/[\x01-\x08\x0B\x0C\x0E-\x1F\x7F]/', '', $html) ?? $html;
    $html = preg_replace('#<script\b[^>]*>.*?</script>#is', '', $html) ?? $html;
    $html = preg_replace('#<iframe\b[^>]*>.*?</iframe>#is', '', $html) ?? $html;
    return $html;
}

function fix_relative_paths(string $html, string $basePath): string
{
    if (trim($basePath) === '') {
        return $html;
    }

    $prefix = rtrim($basePath, "/\\") . DIRECTORY_SEPARATOR;

    return preg_replace_callback(
        '/\s(src|href)\s*=\s*(["\'])(?![a-zA-Z][a-zA-Z0-9+.-]*:|\/|#)(.*?)\2/i',
        static function (array $matches) use ($prefix): string {
            $relative = ltrim($matches[3], "/\\");
            $absolute = $prefix . str_replace(['/', '\\'], DIRECTORY_SEPARATOR, $relative);
            return ' ' . $matches[1] . '=' . $matches[2] . $absolute . $matches[2];
        },
        $html
    ) ?? $html;
}

function localize_architecture_paths(string $html, string $architectureBasePath, string $sgpId): string
{
    if (trim($architectureBasePath) === '') {
        return $html;
    }

    $root = rtrim($architectureBasePath, "/\\");

    $resolver = static function (string $value) use ($root, $sgpId): string {
        $value = trim(html_entity_decode($value, ENT_QUOTES | ENT_HTML5, 'UTF-8'));
        if ($value === '' || str_starts_with($value, 'data:') || str_starts_with($value, '#')) {
            return $value;
        }

        $path = parse_url($value, PHP_URL_PATH);
        $path = is_string($path) && $path !== '' ? $path : $value;
        $path = rtrim(str_replace('\\', '/', $path), '/');

        $relative = '';
        if ($sgpId !== '') {
            foreach ([
                '/serve-architecture-files/' . $sgpId . '/',
                '/requestor/' . $sgpId . '/',
            ] as $marker) {
                $position = strpos($path, $marker);
                if ($position !== false) {
                    $relative = substr($path, $position + strlen($marker));
                    break;
                }
            }
        }

        if ($relative === '') {
            $relative = basename($path);
        }

        return $root . DIRECTORY_SEPARATOR . str_replace('/', DIRECTORY_SEPARATOR, ltrim($relative, "/\\"));
    };

    $html = preg_replace_callback(
        '/\s(src|href)\s*=\s*(["\'])(.*?)\2/i',
        static function (array $matches) use ($resolver): string {
            return ' ' . $matches[1] . '=' . $matches[2] . $resolver($matches[3]) . $matches[2];
        },
        $html
    ) ?? $html;

    return preg_replace_callback(
        '/url\(\s*([\'\"]?)(.*?)\1\s*\)/i',
        static fn(array $matches): string => 'url("' . $resolver($matches[2]) . '")',
        $html
    ) ?? $html;
}

function visible_text(string $html): string
{
    return trim(preg_replace('/\s+/u', ' ', strip_tags(html_entity_decode($html, ENT_QUOTES | ENT_HTML5, 'UTF-8'))) ?? '');
}

function heading_html(string $tag, string $text, int $top = 10): string
{
    return '<div style="max-width:83%;margin-left:auto;margin-right:auto;padding-top:' . $top . 'px;">' .
        '<' . $tag . ' class="text-primary">' . htmlspecialchars($text, ENT_QUOTES, 'UTF-8') . '</' . $tag . '>' .
        '</div>';
}

function write_section(Mpdf $pdf, string $name, string $html): void
{
    $html = clean_html($html);
    if (trim($html) === '') {
        return;
    }

    $before = $pdf->page;
    $pdf->WriteHTML($html, HTMLParserMode::HTML_BODY);
    debug_log('Section rendered', [
        'section' => $name,
        'page_before' => $before,
        'page_after' => $pdf->page,
        'html_bytes' => strlen($html),
    ]);
}

/**
 * Register a TOC entry AND write the heading itself in one call, so the two
 * can never drift out of sync with each other.
 */
function toc_heading(Mpdf $pdf, string $name, string $tocLabel, int $level, string $tag, string $headingText, int $top = 10): void
{
    $pdf->TOC_Entry($tocLabel, $level);
    write_section($pdf, $name, heading_html($tag, $headingText, $top));
}

/**
 * Return the complete outer HTML of the first element containing the requested
 * CSS class. DOM parsing is used because regular expressions stop at the first
 * nested closing div and can silently drop part of the cover content.
 */
function element_html_by_class(string $html, string $className): string
{
    if (trim($html) === '' || !class_exists('DOMDocument')) {
        return '';
    }

    $previous = libxml_use_internal_errors(true);

    $document = new DOMDocument('1.0', 'UTF-8');
    $wrapped = '<?xml encoding="UTF-8"><div id="sar-cover-root">' . $html . '</div>';
    $loaded = $document->loadHTML(
        $wrapped,
        LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD
    );

    if (!$loaded) {
        libxml_clear_errors();
        libxml_use_internal_errors($previous);
        return '';
    }

    $xpath = new DOMXPath($document);
    $query = sprintf(
        '//*[contains(concat(" ", normalize-space(@class), " "), " %s ")]',
        $className
    );
    $nodes = $xpath->query($query);

    $result = '';
    if ($nodes !== false && $nodes->length > 0) {
        $result = (string) $document->saveHTML($nodes->item(0));
    }

    libxml_clear_errors();
    libxml_use_internal_errors($previous);

    return $result;
}

/**
 * Remove editing-only paragraphs from the centered cover block without
 * removing the remaining subtitle, version, risk, APM/TPM and restriction text.
 */
function clean_centered_cover_html(string $html): string
{
    if (trim($html) === '') {
        return '';
    }

    return preg_replace(
        '#<p\b[^>]*class\s*=\s*[^>]*\bcomb_residual_edit\b[^>]*>.*?</p>#is',
        '',
        $html
    ) ?? $html;
}

$autoload = find_autoload();
if ($autoload === null) {
    fail_pdf('Unable to locate Composer autoload.php', 3);
}
require_once $autoload;

$payload = read_payload();
$sar = $payload['sar_combine_data'] ?? null;
$observations = $payload['security_observations_data'] ?? [];

if (!is_array($sar)) {
    fail_pdf('Missing required field: sar_combine_data', 4);
}
if (!is_array($observations)) {
    $observations = [];
}

$baseUrl = (string) ($payload['base_url'] ?? '');
$basePath = (string) ($payload['base_path'] ?? '');
$architectureBasePath = (string) ($payload['architecture_base_path'] ?? '');
$sgpId = (string) ($payload['sgp_id'] ?? '');
$title = (string) ($payload['title'] ?? 'document.pdf');
$watermark = (string) ($payload['watermark'] ?? '');
$format = (string) ($payload['format'] ?? 'A4');
$orientation = (string) ($payload['orientation'] ?? 'P');
$font = (string) ($payload['default_font'] ?? 'Arial');
$confidentialityHtml = (string) ($payload['conf_header_html'] ?? '');
$contactHtml = (string) ($payload['contact_header_html'] ?? '');
$cssFiles = $payload['css_files'] ?? [];

if (is_string($cssFiles)) {
    $cssFiles = trim($cssFiles) === '' ? [] : [$cssFiles];
}
if (!is_array($cssFiles)) {
    $cssFiles = [];
}

ini_set('memory_limit', '-1');
set_time_limit(0);

$inlineCss = <<<'CSS'
body{font-family:Arial;}
div.template{text-shadow:rgb(0 0 0 / 15%) 0 0 1px;font-size:1rem;font-weight:400;line-height:1.2;color:#424242;}
div.upper{position:absolute;transform:translate(-30%,-90%);font-size:10rem;margin-left:0in;}
div.centered{position:absolute;transform:translate(-30%,-70%);margin-left:0.2in;}
.text-primary{color:#00338D!important;}
table{width:100%;}
h5.font-weight-bold{font-weight:bold;}
.image1{float:left;}
.image2{}
.image3{transform:translate(30%,-90%);margin-left:0.1in;}
.text-warning{color:#424242;}
CSS;

try {
    $temporaryFiles = [];
    $newTemp = static function (string $prefix) use (&$temporaryFiles): string {
        $path = tempnam(sys_get_temp_dir(), $prefix);
        if ($path === false) {
            throw new RuntimeException('Unable to allocate temporary PDF file');
        }
        $temporaryFiles[] = $path;
        return $path;
    };

    $coverFile = $newTemp('sar_cover_');
    $mainFile = $newTemp('sar_main_');

    $staticBaseUrl = rtrim($baseUrl, '/') . '/';
    $coverImageUrl = $staticBaseUrl . 'img/first_page_sar.jpg';
    $mainLogoUrl = $staticBaseUrl . 'img/logo_new.png';
    $footerLogoUrl = $staticBaseUrl . 'img/login_kpmg.png';

    debug_log('Using original static image resolution', [
        'base_url' => $baseUrl,
        'cover' => $coverImageUrl,
        'logo' => $mainLogoUrl,
        'footer_logo' => $footerLogoUrl,
        'cwd' => getcwd(),
    ]);

    $applyStyles = static function (Mpdf $pdf) use ($inlineCss, $cssFiles, $basePath): void {
        $pdf->WriteHTML($inlineCss, HTMLParserMode::HEADER_CSS);
        foreach ($cssFiles as $file) {
            if (!is_string($file) || trim($file) === '') {
                continue;
            }
            $candidate = trim($file);
            if (!is_file($candidate) && $basePath !== '' && ($candidate[0] ?? '') !== '/') {
                $candidate = rtrim($basePath, "/\\") . DIRECTORY_SEPARATOR . $candidate;
            }
            if (is_file($candidate) && is_readable($candidate)) {
                $css = file_get_contents($candidate);
                if ($css !== false) {
                    $pdf->WriteHTML($css, HTMLParserMode::HEADER_CSS);
                }
            }
        }
    };

    $footerHtml = '<table width="100%"><tr>' .
        '<td style="text-align:left;"><img width="10%" height="3%" src="' .
        htmlspecialchars($footerLogoUrl, ENT_QUOTES, 'UTF-8') . '"></td>' .
        '<td style="text-align:center;">Data Classification: KPMG Restricted - For KPMG Internal Use Only</td>' .
        '<td style="text-align:right;">{PAGENO}</td>' .
        '</tr></table>';

    $newPdf = static function (bool $footer = true) use (
        $format,
        $orientation,
        $font,
        $title,
        $watermark,
        $footerHtml,
        $applyStyles
    ): Mpdf {
        $pdf = new Mpdf([
            'mode' => 'utf-8',
            'format' => $format,
            'orientation' => $orientation,
            'default_font' => $font,
            'tempDir' => sys_get_temp_dir(),
            'margin_left' => 15,
            'margin_right' => 15,
            'margin_top' => 15,
            'margin_bottom' => 20,
        ]);
        $pdf->showImageErrors = false;
        $pdf->SetTitle($title);
        $applyStyles($pdf);
        if ($footer) {
            $pdf->SetHTMLFooter($footerHtml);
        }
        if (trim($watermark) !== '') {
            $pdf->SetWatermarkText($watermark);
            $pdf->showWatermarkText = true;
        }
        return $pdf;
    };

    /*
    |--------------------------------------------------------------------------
    | Cover page
    |--------------------------------------------------------------------------
    |
    | The cover background and logo continue to use the original base_url
    | resolution. The logo, title and lower information are placed in explicit
    | millimetre-based boxes so browser transforms cannot move or clip them.
    | This page is rendered in its own zero-margin Mpdf instance (fixed
    | positioning needs full-bleed coordinates) and merged in afterwards via
    | FPDI. Because it carries no TOC targets, flattening it during merge
    | costs nothing.
    |
    */
    $coverPdf = new Mpdf([
        'mode' => 'utf-8',
        'format' => $format,
        'orientation' => $orientation,
        'default_font' => $font,
        'tempDir' => sys_get_temp_dir(),
        'margin_left' => 0,
        'margin_right' => 0,
        'margin_top' => 0,
        'margin_bottom' => 0,
        'margin_header' => 0,
        'margin_footer' => 0,
    ]);

    $coverPdf->showImageErrors = false;
    $coverPdf->SetTitle($title);
    $applyStyles($coverPdf);

    $headerFirst = normalize_paths(
        (string) ($sar['header_first_page'] ?? ''),
        $baseUrl
    );

    $headerFirst = str_replace(
        'KPMG Confidential',
        'KPMG Restricted',
        $headerFirst
    );

    $headerFirst = str_replace(
        'Access to this document is restricted to Member Firm National IT Security Officers (NITSOs), Privacy Liaisons (PLs) and the solution business sponsor and project team.',
        'Access to this document is restricted to Member Firm National IT Security Officers (NITSOs), and Privacy Liaisons (PLs).',
        $headerFirst
    );

    /* DOM extraction preserves all nested cover-page content. */
    $upperHtml = element_html_by_class($headerFirst, 'upper');
    $centeredHtml = element_html_by_class($headerFirst, 'centered');
    $centeredHtml = clean_centered_cover_html($centeredHtml);
    $centeredHtml = clean_residual_risk_badge($centeredHtml);

    /* Full-page background image. */
    $coverPdf->WriteHTML(
        '<div style="position:absolute;left:0;top:0;width:210mm;height:297mm;margin:0;padding:0;">' .
        '<img src="' . htmlspecialchars($coverImageUrl, ENT_QUOTES, 'UTF-8') .
        '" style="width:210mm;height:297mm;margin:0;padding:0;">' .
        '</div>',
        HTMLParserMode::HTML_BODY
    );

    /*
     * Do not reuse image3 here. image3 contains a translate transform and was
     * clipping the logo above the page. The image source is unchanged.
     */
    $coverPdf->WriteFixedPosHTML(
        '<img src="' . htmlspecialchars($mainLogoUrl, ENT_QUOTES, 'UTF-8') .
        '" style="width:44mm;height:auto;">',
        15,
        12,
        50,
        24,
        'visible'
    );

    /*
     * Reset only cover-content layout properties. Text colours and emphasis
     * from the payload are retained, including the residual-risk colour.
     */
    $coverPdf->WriteHTML(
        '.cover-title, .cover-information {' .
            'font-family: Arial;' .
            'color: #ffffff;' .
        '}' .
        '.cover-title .upper, .cover-information .centered {' .
            'position: static !important;' .
            'transform: none !important;' .
            'float: none !important;' .
            'width: auto !important;' .
            'height: auto !important;' .
            'margin: 0 !important;' .
            'padding: 0 !important;' .
        '}' .
        '.cover-title div, .cover-title p, .cover-title span, ' .
        '.cover-information div, .cover-information p, .cover-information span {' .
            'position: static !important;' .
            'transform: none !important;' .
            'float: none !important;' .
            'margin-left: 0 !important;' .
            'margin-right: 0 !important;' .
            'padding-left: 0 !important;' .
            'padding-right: 0 !important;' .
        '}' .
        '.cover-title {' .
            'font-size: 25pt;' .
            'font-weight: 400;' .
            'line-height: 1.10;' .
            'text-align: left;' .
        '}' .
        '.cover-title p, .cover-title h1, .cover-title h2, ' .
        '.cover-title h3, .cover-title h4 {' .
            'font-size: 25pt !important;' .
            'font-weight: 400 !important;' .
            'line-height: 1.10 !important;' .
            'margin-top: 0 !important;' .
            'margin-bottom: 2.5mm !important;' .
            'padding: 0 !important;' .
        '}' .
        '.cover-information {' .
            'font-size: 9.5pt;' .
            'line-height: 1.22;' .
            'text-align: left;' .
        '}' .
        '.cover-information p {' .
            'margin-top: 0 !important;' .
            'margin-bottom: 1.4mm !important;' .
            'padding: 0 !important;' .
            'line-height: 1.22 !important;' .
        '}',
        HTMLParserMode::HEADER_CSS
    );

    /* Solution name / cover title. */
    if (trim($upperHtml) !== '') {
        $coverPdf->WriteFixedPosHTML(
            '<div class="cover-title">' . $upperHtml . '</div>',
            5,
            40,
            136,
            48,
            'visible'
        );
    }

    /*
     * Subtitle/version, residual risk, report name, APM/TPM number,
     * classification and access restriction. The block is compacted and
     * aligned to the same 37 mm left edge as the title.
     */
    if (trim($centeredHtml) !== '') {
        $coverPdf->WriteFixedPosHTML(
            '<div class="cover-information">' . $centeredHtml . '</div>',
            5,
            202,
            157,
            82,
            'visible'
        );
    }

    /* Ensure mPDF materializes the cover page. */
    $coverPdf->WriteFixedPosHTML(
        '<div style="color:transparent;font-size:1pt;">SAR Cover</div>',
        0,
        0,
        1,
        1,
        'hidden'
    );

    $coverPdf->Output($coverFile, 'F');

    /*
    |--------------------------------------------------------------------------
    | Main document: information, revision, contents (TOC) and body
    |--------------------------------------------------------------------------
    |
    | Everything from here on is written into ONE Mpdf instance so that
    | TOC_Entry() / TOCpagebreakByArray() can generate real, clickable
    | internal links. Splitting these sections into separate Mpdf instances
    | and merging them back together via FPDI (as an earlier version of this
    | script did) flattens each page into a static template and silently
    | discards all link/destination data - that was the root cause of the
    | "Contents" page losing its clickable links.
    |
    */
    $mainPdf = $newPdf(true);

    /* Information / confidentiality page. */
    write_section(
        $mainPdf,
        'confidentiality',
        fix_relative_paths(normalize_paths($confidentialityHtml, $baseUrl), $basePath)
    );

    /* Revision page. */
    $mainPdf->AddPage();
    write_section($mainPdf, 'review_heading', heading_html('h2', 'Document review and approval', 30));
    write_section(
        $mainPdf,
        'revision',
        fix_relative_paths(normalize_paths((string) ($sar['header_revision_second_page'] ?? ''), $baseUrl), $basePath)
    );
    write_section(
        $mainPdf,
        'reviewer',
        fix_relative_paths(normalize_paths((string) ($sar['header_reviewer_second_page'] ?? ''), $baseUrl), $basePath)
    );

    /* Contents (TOC) page - native mPDF TOC, rendered with real links. */
    $mainPdf->TOCpagebreakByArray([
        'links' => true,
        'toc_preHTML' => heading_html('h2', 'Contents', 30),
    ]);

    $renderSar = static function (string $key) use ($mainPdf, $sar, $baseUrl, $basePath): void {
        $value = (string) ($sar[$key] ?? '');
        if ($value !== '') {
            write_section($mainPdf, $key, fix_relative_paths(normalize_paths($value, $baseUrl), $basePath));
        }
    };
    $renderObservation = static function (string $key) use ($mainPdf, $observations, $baseUrl, $basePath): void {
        $value = (string) ($observations[$key] ?? '');
        if ($value !== '') {
            write_section($mainPdf, 'observations_' . strtolower($key), fix_relative_paths(normalize_paths($value, $baseUrl), $basePath));
        }
    };

    toc_heading($mainPdf, 'heading_1', '1   Solution Overview', 0, 'h2', '1   Solution Overview', 30);
    $renderSar('header_1');

    toc_heading($mainPdf, 'heading_1_1', '1.1   Risk Summary', 1, 'h3', '1.1   Risk Summary');
    $renderSar('header_1_1');

    toc_heading($mainPdf, 'heading_1_2', '1.2   Solution Summary', 1, 'h3', '1.2   Solution Summary');
    $renderSar('header_1_2');

    toc_heading($mainPdf, 'heading_1_3', '1.3   Data Classification and Business Criticality', 1, 'h3', '1.3   Data Classification and Business Criticality');
    $renderSar('header_1_3');

    toc_heading($mainPdf, 'heading_1_4', '1.4   Users', 1, 'h3', '1.4   Users');
    $renderSar('header_1_4');

    toc_heading($mainPdf, 'heading_1_5', '1.5   Hosting', 1, 'h3', '1.5   Hosting');
    $renderSar('header_1_5');

    toc_heading($mainPdf, 'heading_2', '2   Architecture', 0, 'h2', '2   Architecture');
    $renderSar('header_2');

    toc_heading($mainPdf, 'heading_2_1', '2.1   High Level Technical Architecture Diagram', 1, 'h3', '2.1   High Level Technical Architecture Diagram');
    if (!empty($sar['header_2_1'])) {
        write_section(
            $mainPdf,
            'header_2_1',
            localize_architecture_paths((string) $sar['header_2_1'], $architectureBasePath, $sgpId)
        );
    }

    if (!empty($sar['header_2_2_1'])) {
        toc_heading($mainPdf, 'heading_2_2', '2.2   Key Security Features', 1, 'h3', '2.2   Key Security Features');
        $renderSar('header_2_2');
        foreach ([
            ['2.2.1', 'General Environment', 'header_2_2_1'],
            ['2.2.2', 'Authentication / Authorization', 'header_2_2_2'],
            ['2.2.3', 'Data Separation', 'header_2_2_3'],
            ['2.2.4', 'Encryption', 'header_2_2_4'],
            ['2.2.5', 'Logging and Monitoring (Auditing)', 'header_2_2_5'],
            ['2.2.6', 'Reporting / Data Exporting', 'header_2_2_6'],
            ['2.2.7', 'External Content', 'header_2_2_7'],
        ] as [$number, $label, $key]) {
            $label = $number . '   ' . $label;
            toc_heading($mainPdf, 'heading_' . str_replace('.', '_', $number), $label, 2, 'h4', $label);
            $renderSar($key);
        }
    }

    if (!empty($sar['header_3_1'])) {
        toc_heading($mainPdf, 'heading_3', '3   Assessment Overview', 0, 'h2', '3   Assessment Overview');
        $renderSar('header_3');
        toc_heading($mainPdf, 'heading_3_1', '3.1   Overview', 1, 'h3', '3.1   Overview');
        $renderSar('header_3_1');
        toc_heading($mainPdf, 'heading_3_2', '3.2  Core Security Requirements', 1, 'h3', '3.2   Core Security Requirements');
        $renderSar('header_3_2');
        // toc_heading($mainPdf, 'heading_3_3', '3.3   Testing Approach', 1, 'h3', '3.3   Testing Approach');
        // $renderSar('header_3_3');
        // toc_heading($mainPdf, 'heading_3_4', '3.4   High Level Security Requirements', 1, 'h3', '3.4   High Level Security Requirements');
        // $renderSar('header_3_4');
    } else {
        toc_heading($mainPdf, 'heading_3', '3   Assessment Overview', 0, 'h2', '3   Assessment Overview');
        $renderSar('header_3');
        toc_heading($mainPdf, 'heading_3_1', '3.1   Overview', 1, 'h3', '3.1   Overview');
        $renderSar('header_3_2');
        toc_heading($mainPdf, 'heading_3_2_requirements', '3.2   Core Security Requirements', 1, 'h3', '3.2   Core Security Requirements');
        $renderSar('header_3_4');
    }

    toc_heading($mainPdf, 'heading_4', '4   Plan of Action and Milestone (POA&M)', 0, 'h2', '4   Plan of Action and Milestone (POA&M)');
    $renderSar('header_6');
    foreach ([
        ['4.1', 'Critical Risk Findings', 'Critical'],
        ['4.2', 'High Risk Findings', 'High'],
        ['4.3', 'Medium Risk Findings', 'Medium'],
        ['4.4', 'Low Risk Findings', 'Low'],
    ] as [$number, $label, $key]) {
        $label = $number . '   ' . $label;
        toc_heading($mainPdf, 'heading_' . str_replace('.', '_', $number), $label, 1, 'h3', $label);
        $renderObservation($key);
    }

    $supportHeading = '5   Key Contact Details';
    $addendumHeading = '6   Addendum';
    if (!empty($sar['header_7'])) {
        $header7 = fix_relative_paths(normalize_paths((string) $sar['header_7'], $baseUrl), $basePath);
        if (visible_text($header7) !== '') {
            toc_heading($mainPdf, 'heading_5', '5   Additional Business Considerations', 0, 'h2', '5   Additional Business Considerations');
            write_section($mainPdf, 'header_7', $header7);
            $supportHeading = '6   Key Contact Details';
            $addendumHeading = '7   Addendum';
        }
    }

    $mainPdf->TOC_Entry($supportHeading, 0);
    // write_section($mainPdf, 'heading_support', heading_html('h2', $supportHeading));
    $renderSar('header_support_team');

    if (array_key_exists('addendum_header', $sar)) {
        $addendum = fix_relative_paths(normalize_paths((string) $sar['addendum_header'], $baseUrl), $basePath);
        $addendum = preg_replace('#<button\b[^>]*addTestingOverview_7[^>]*>.*?</button>#is', '', $addendum) ?? $addendum;
        if (visible_text($addendum) !== '') {
            $mainPdf->TOC_Entry($addendumHeading, 0);
            write_section($mainPdf, 'heading_addendum', heading_html('h2', $addendumHeading));
            write_section($mainPdf, 'addendum', $addendum);
        }
    }

    if (trim($contactHtml) !== '') {
        $mainPdf->AddPage();
        write_section($mainPdf, 'contact', fix_relative_paths(normalize_paths($contactHtml, $baseUrl), $basePath));
    }

    $mainPdf->Output($mainFile, 'F');

    /*
    |--------------------------------------------------------------------------
    | Merge cover + main document
    |--------------------------------------------------------------------------
    |
    | Only the cover needs to be merged via FPDI now - it carries no TOC
    | targets, so flattening it costs nothing. The main document keeps its
    | native, clickable TOC links because it was never split apart.
    |
    */
    $finalPdf = new Mpdf([
        'mode' => 'utf-8',
        'format' => $format,
        'orientation' => $orientation,
        'tempDir' => sys_get_temp_dir(),
        'margin_left' => 0,
        'margin_right' => 0,
        'margin_top' => 0,
        'margin_bottom' => 0,
    ]);

    $mergedPages = 0;
    foreach ([$coverFile, $mainFile] as $part) {
        if (!is_file($part) || filesize($part) === 0) {
            continue;
        }
        $pageCount = $finalPdf->SetSourceFile($part);
        for ($page = 1; $page <= $pageCount; $page++) {
            $template = $finalPdf->ImportPage($page);
            $size = $finalPdf->getTemplateSize($template);
            $finalPdf->AddPageByArray([
                'orientation' => $size['orientation'],
                'sheet-size' => [$size['width'], $size['height']],
                'margin-left' => 0,
                'margin-right' => 0,
                'margin-top' => 0,
                'margin-bottom' => 0,
            ]);
            $finalPdf->UseTemplate($template, 0, 0, $size['width'], $size['height'], true);
            $mergedPages++;
        }
    }

    if ($mergedPages === 0) {
        throw new RuntimeException('No pages were available for merging');
    }

    $pdfBytes = $finalPdf->Output('', 'S');

    foreach ($temporaryFiles as $file) {
        if (is_file($file)) {
            @unlink($file);
        }
    }

    debug_log('PDF complete', [
        'pages' => $mergedPages,
        'bytes' => strlen($pdfBytes),
        'header_valid' => str_starts_with($pdfBytes, '%PDF-'),
        'eof_valid' => str_contains(substr($pdfBytes, -2048), '%%EOF'),
    ]);

    fwrite(STDOUT, $pdfBytes);
    exit(0);
} catch (Throwable $exception) {
    if (isset($temporaryFiles) && is_array($temporaryFiles)) {
        foreach ($temporaryFiles as $file) {
            if (is_string($file) && is_file($file)) {
                @unlink($file);
            }
        }
    }

    fail_pdf('SAR PDF generation failed: ' . $exception->getMessage(), 6);
}
