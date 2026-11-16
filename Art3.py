"use client";

import { useState, type CSSProperties } from "react";
import AppShell, { useToast } from "@/components/AppShell";
import Breadcrumbs, { HOME_CRUMB, REQUESTS_CRUMB } from "@/components/Breadcrumbs";
import Select from "@/components/Select";
import TitleBar from "@/components/TitleBar";
import { HOSTING, findRequest } from "@/lib/data/requests";
import { cx } from "@/lib/helpers";
import "@/styles/pages/logs.css";

/* Activity logs for a request: search, filter by type, sort by date, download emails */
export default function LogsPage({ params }: { params: { id: string } }) {
  return (
    <AppShell page="pg-logs">
      <Logs id={params.id} />
    </AppShell>
  );
}

/* log types: [icon, colour] */
const TYPES: Record<string, [string, string]> = {
  Status: ["fa-solid fa-signal", "#2563EB"],
  AI: ["fa-solid fa-wand-magic-sparkles", "#7C3AED"],
  Comments: ["fa-regular fa-comment", "#0E7490"],
  Email: ["fa-regular fa-envelope", "#B45309"],
  Identifiers: ["fa-solid fa-fingerprint", "#059669"],
  Delegate: ["fa-solid fa-user-plus", "#BE185D"],
  Documents: ["fa-regular fa-file-lines", "#475569"],
};
const MAIL = "To: go-fmipgsolutionrevi@kpmg.com, go-fmredteamser@kpmg.com, go-dlsecurecodeanaly@kpmg.com";
interface Log { date: string; name: string; role: string; resp: string; update: string; old: string; type: string; mail?: boolean }
const logsFor = (id: string): Log[] => [
  { date: "2026-10-16T12:30:23", name: "GSSR System", role: "GSSR System", resp: "Request sub status", update: "Security findings validation", old: "Business context generation", type: "Status" },
  { date: "2026-10-16T12:30:10", name: "Sec Team", role: "GSSR System", resp: "Skip AI evaluation", update: "No", old: "", type: "AI" },
  { date: "2026-10-16T12:30:10", name: "Sec Team", role: "Security Resource", resp: "Approved", update: "Intake reviewed; all certifications present and identifiers verified.", old: "", type: "Comments" },
  { date: "2026-10-16T12:30:10", name: "GSSR System", role: "GSSR System", resp: `Global Security Solution Review: Additional Security Assessment Activities Identified | ABC | SR ${id}`, update: `${MAIL}\n\nHello team, additional security assessment activities have been identified for this solution. Please review the attached summary of findings and complete the outstanding activities in GSSR by the due date. Reach out to the Security Resource assigned to this request with any questions.`, old: "", type: "Email", mail: true },
  { date: "2026-10-15T17:42:05", name: "GSSR System", role: "GSSR System", resp: "Request status", update: "Assessment in progress", old: "Intake verification", type: "Status" },
  { date: "2026-10-15T17:40:51", name: "Coord Team", role: "Coordinator", resp: "Delegate added", update: "priya.nair@kpmg.com, daniel.ross@kpmg.com", old: "", type: "Delegate" },
  { date: "2026-10-15T16:12:37", name: "Sec Team", role: "Security Resource", resp: "FoD Release ID (QA)", update: "1184529, 1184530", old: "1184529", type: "Identifiers" },
  { date: "2026-10-15T16:10:02", name: "Sec Team", role: "Security Resource", resp: "Mend product", update: "ABC-Platform", old: "N/A", type: "Identifiers" },
  { date: "2026-10-15T11:05:44", name: "GSSR System", role: "GSSR System", resp: "AI risk context", update: "Generated · KPMG Public / BC0 / Low", old: "", type: "AI" },
  { date: "2026-10-14T18:22:19", name: "Sol Team", role: "Solution Team", resp: "SOC 2 Type II report", update: "SOC2_TypeII_2026.pdf, Bridge_Letter_Q3.pdf", old: "SOC2_TypeII_2025.pdf", type: "Documents" },
  { date: "2026-10-14T18:20:03", name: "Sol Team", role: "Solution Team", resp: "Intake response", update: "Please find the updated architecture diagram attached.", old: "", type: "Comments" },
  { date: "2026-10-14T09:31:58", name: "GSSR System", role: "GSSR System", resp: "Intake submitted", update: `${MAIL}\n\nA new intake has been submitted for review. The Coordinator will assign a Security Resource within two business days.`, old: "", type: "Email", mail: true },
  { date: "2026-10-13T15:47:26", name: "Coord Team", role: "Coordinator", resp: "Request status", update: "Intake verification", old: "Draft", type: "Status" },
  { date: "2026-10-13T15:45:10", name: "Coord Team", role: "Coordinator", resp: "Assigned to", update: "Sec Team (Security Resource)", old: "Unassigned", type: "Status" },
  { date: "2026-10-12T10:02:41", name: "Sol Team", role: "Solution Team", resp: "Request created", update: `SAR ${id} created from KIEP`, old: "", type: "Status" },
];

function Logs({ id }: { id: string }) {
  const toast = useToast();
  const r = findRequest(id);
  const logs = logsFor(id);
  const [q, setQ] = useState("");
  const [type, setType] = useState("");
  const [desc, setDesc] = useState(true);

  const query = q.trim().toLowerCase();
  const rows = logs
    .filter((l) => (!type || l.type === type) && (!query || [l.name, l.role, l.resp, l.update, l.old].join(" ").toLowerCase().includes(query)))
    .sort((a, b) => (desc ? b.date.localeCompare(a.date) : a.date.localeCompare(b.date)));

  const updateCell = (l: Log) => {
    if (!l.mail) return l.update;
    const [to, ...rest] = l.update.split("\n\n");
    const addrs = to.replace(/^To:\s*/, "").split(/,\s*/);
    return (
      <>
        <div className="lg-more lg-mail"><b>To:</b> {addrs.map((a, i) => <span key={a}>{i > 0 && ", "}<span className="addr">{a}</span></span>)}<br /><br />{rest.join(" ")}</div>
        <div className="lg-links"><button type="button" onClick={() => toast(`Downloading email · ${l.resp.slice(0, 40)}…`)}><i className="fa-solid fa-download" />Download</button></div>
      </>
    );
  };

  return (
    <main className="shell">
      <Breadcrumbs items={[HOME_CRUMB, REQUESTS_CRUMB, { label: `View Logs - ${id}`, icon: "fa-solid fa-clock-rotate-left" }]} />
      <TitleBar projectName={r?.project ?? "ABC"} solutionName={r?.solution ?? "ABC"}
        meta={[{ label: "Solution type", value: <span className={cx("pill", r ? { kpmg: "pill-host", saas: "pill-saas", saasplus: "pill-saasplus" }[r.host] : "pill-host")}>{r ? HOSTING[r.host].label : "KPMG Hosted"}</span> }]} />

      <section className="nt-card">
        <div className="nl-head">
          <span className="sec-icon"><i className="fa-solid fa-clock-rotate-left" /></span>
          <h2 className="nl-title">Activity Logs</h2>
          <span className="nl-count">{rows.length}</span>
          <div className="lg-tools">
            <div className="lg-bar">
              <label className="lg-search"><i className="fa-solid fa-magnifying-glass" /><input type="search" placeholder="Search by name, update or data" aria-label="Search logs" value={q} onChange={(e) => setQ(e.target.value)} /></label>
              <span className="lg-div" aria-hidden="true" />
              <Select className="inp lg-type" value={type} placeholder="All log types" options={Object.keys(TYPES)} aria-label="Log type" onChange={setType} />
            </div>
            <button type="button" className="vbtn primary" onClick={() => toast(`Exporting artifacts for SAR ${id}`)}><i className="fa-solid fa-download" />Export Artifacts</button>
          </div>
        </div>
        <div className="lg-wrap">
          <table className="ltable">
            <colgroup><col style={{ width: "13%" }} /><col style={{ width: "13%" }} /><col style={{ width: "15%" }} /><col style={{ width: "25%" }} /><col style={{ width: "13%" }} /><col style={{ width: "10%" }} /><col style={{ width: "11%" }} /></colgroup>
            <thead><tr>
              <th className="sortable" aria-sort={desc ? "descending" : "ascending"} onClick={() => setDesc(!desc)}>Date<i className={`fa-solid ${desc ? "fa-arrow-down" : "fa-arrow-up"}`} /></th>
              <th>Name</th><th>Response For</th><th>Update</th><th>Old Data</th><th>Type</th><th>User Role</th>
            </tr></thead>
            <tbody>
              {rows.length ? rows.map((l) => {
                const d = new Date(l.date), [ico, col] = TYPES[l.type];
                return (
                  <tr key={l.date + l.resp}>
                    <td className="lg-date"><b>{d.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" })}</b>{d.toLocaleTimeString("en-GB")}</td>
                    <td className="lg-who">{l.name}</td>
                    <td>{l.resp}</td>
                    <td>{updateCell(l)}</td>
                    <td>{l.old ? <span className="lg-old">{l.old}</span> : <span className="lg-none">—</span>}</td>
                    <td><span className="lg-type-pill" style={{ "--tc": col } as CSSProperties}><i className={ico} />{l.type}</span></td>
                    <td className="lg-role">{l.role}</td>
                  </tr>
                );
              }) : <tr><td colSpan={7}><div className="nl-empty"><i className="fa-regular fa-file-lines" />No logs found</div></td></tr>}
            </tbody>
          </table>
        </div>
        <div className="lg-foot"><span>Showing {rows.length} of {logs.length} entries</span><span>Times are shown in your local time zone</span></div>
      </section>
      <footer className="vi-foot">© 2026 KPMG | All rights reserved | v3.0.1</footer>
    </main>
  );
}
