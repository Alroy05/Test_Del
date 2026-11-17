"use client";

import { useState, type CSSProperties } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import AppShell, { useToast } from "@/components/AppShell";
import Breadcrumbs, { HOME_CRUMB, REQUESTS_CRUMB } from "@/components/Breadcrumbs";
import IntakeForm from "@/components/intake/IntakeForm";
import { PORTFOLIO, TYPE_COLOR, TYPE_LABEL, emptyForm, type FormData } from "@/components/intake/model";
import { cx } from "@/lib/helpers";
import type { HostKey } from "@/lib/data/requests";
import "@/styles/pages/request-add.css";

/* Add New Request: find the application in KIEPs (or go manual), choose the solution type, then fill in the intake */
export default function RequestAddPage() {
  return (
    <AppShell page="pg-request-add">
      <AddRequest />
    </AppShell>
  );
}

function AddRequest() {
  const toast = useToast();
  const router = useRouter();
  const [step, setStep] = useState<"start" | "form">("start");
  const [hasApm, setHasApm] = useState<"yes" | "no" | null>(null);
  const [query, setQuery] = useState("");
  const [searched, setSearched] = useState("");
  const [apmPick, setApmPick] = useState<string | null>(null);
  const [type, setType] = useState<HostKey | null>(null);
  const [form, setForm] = useState<FormData>(emptyForm());

  const picked = PORTFOLIO.find((r) => r[0] === apmPick);
  const ready = hasApm === "no" || (hasApm === "yes" && !!picked); // solution type opens once this is settled
  const q = searched.toLowerCase();
  // nothing is listed until you search; with an empty search only the chosen application stays visible
  const rows = q ? PORTFOLIO.filter((r) => r.slice(0, 3).join(" ").toLowerCase().includes(q)) : PORTFOLIO.filter((r) => r[0] === apmPick);
  const mark = (t: string) => {
    const i = q ? t.toLowerCase().indexOf(q) : -1;
    return i < 0 ? t : <>{t.slice(0, i)}<mark>{t.slice(i, i + q.length)}</mark>{t.slice(i + q.length)}</>;
  };
  const runSearch = () => {
    if (!hasApm) setHasApm("yes");
    setSearched(query.trim());
    if (!query.trim()) toast("Enter an APM / TPM ID, project name or solution name");
  };

  const create = () => {
    const [apm, proj, sol, fam] = hasApm === "yes" && picked ? picked : ["", "", "", ""];
    // carry the chosen application into the form (a manual intake starts with the names empty)
    setForm((f) => ({ ...f, v: { ...f.v, apm, project: proj, name: sol, family: fam } }));
    setStep("form");
    window.scrollTo({ top: 0 });
    toast(picked && hasApm === "yes" ? `New request started for ${sol}` : "Manual intake started");
  };

  return (
    <main className="shell">
      <Breadcrumbs items={[HOME_CRUMB, REQUESTS_CRUMB, { label: "Add New Request", icon: "fa-solid fa-plus" }]} />

      {step === "start" ? (
        <div className="st-wrap" id="startView">
          <div className="vi-head">
            <div className="vi-steps" aria-label="Steps">
              <span className="on"><b>1</b>APM / TPM ID</span><i className="fa-solid fa-chevron-right" />
              <span className={cx(ready && "on")}><b>2</b>Solution type</span><i className="fa-solid fa-chevron-right" />
              <span className={cx(ready && type && "on")}><b>3</b>Intake</span>
            </div>
          </div>
          <div className="st-card">
            <div className="st-sec">
              <div className="st-label"><span className="n">1</span>Do you have an APM / TPM ID for this solution?</div>
              <div className="st-ask" role="radiogroup" aria-label="Has an APM / TPM ID">
                <button type="button" className="st-ans" role="radio" aria-checked={hasApm === "yes"} onClick={() => setHasApm("yes")}>
                  <span className="ti"><i className="fa-solid fa-magnifying-glass" /></span><span><b>Yes, I have one</b><small>Find the application in KIEPs</small></span><i className="fa-solid fa-circle-check ck" />
                </button>
                <button type="button" className="st-ans" role="radio" aria-checked={hasApm === "no"} onClick={() => { setHasApm("no"); setApmPick(null); setQuery(""); setSearched(""); }}>
                  <span className="ti"><i className="fa-regular fa-keyboard" /></span><span><b>No, not yet</b><small>Continue with a manual intake; the ID can be added later</small></span><i className="fa-solid fa-circle-check ck" />
                </button>
              </div>
              {/* search is always shown; it's disabled when there's no APM / TPM ID */}
              <div className={cx("st-find", hasApm === "no" && "off")}>
                <div className="st-sub-l">Search by APM / TPM ID, project name or solution name</div>
                <label className="st-search">
                  <i className="fa-solid fa-magnifying-glass" />
                  <input type="search" placeholder="e.g. GO-AV-00000117 or Transaction Services" aria-label="Search applications" autoComplete="off" disabled={hasApm === "no"}
                    value={query} onChange={(e) => setQuery(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); runSearch(); } }} />
                  {query && <button type="button" aria-label="Clear search" disabled={hasApm === "no"} onClick={() => { setQuery(""); setSearched(""); }}><i className="fa-solid fa-xmark" /></button>}
                  <button type="button" className="st-go" disabled={hasApm === "no"} onClick={runSearch}><i className="fa-solid fa-magnifying-glass" />Search</button>
                </label>
                <div className="st-meta">
                  <span>{q ? `${rows.length} match${rows.length === 1 ? "" : "es"} for “${searched}”` : apmPick ? "Selected application" : ""}</span>
                  <span>Source: KIEPs</span>
                </div>
                {hasApm !== "no" && (q || apmPick) && (
                  <div className="st-list" role="radiogroup" aria-label="Applications">
                    {rows.length ? (
                      <>
                        <div className="st-row head"><span /><span>APM / TPM ID</span><span>Project name</span><span>Solution name</span></div>
                        {rows.map((r) => (
                          <button key={r[0]} type="button" className="st-row" role="radio" aria-checked={apmPick === r[0]} onClick={() => { setApmPick(r[0]); setHasApm("yes"); }}>
                            <span className="st-radio" /><span className="st-apm">{mark(r[0])}</span>
                            <span><b>{mark(r[1])}</b><small>Family ID {r[3]}</small></span><span><b>{mark(r[2])}</b></span>
                          </button>
                        ))}
                      </>
                    ) : <div className="st-empty"><i className="fa-solid fa-magnifying-glass" />No applications match. Check the APM / TPM ID in KIEPs.</div>}
                  </div>
                )}
              </div>
            </div>
            <div className="st-sec">
              <div className="st-label"><span className={cx("n", !ready && "off")}>2</span>Choose the solution type</div>
              <div className="st-types" role="radiogroup" aria-label="Solution type">
                {([
                  ["saas", "fa-solid fa-cloud", "SaaS", "Vendor-hosted software used as-is through a subscription."],
                  ["kpmg", "fa-solid fa-server", "KPMG Hosted", "Built or hosted by KPMG, e.g. on ONE Platform or a KPMG data centre."],
                  ["saasplus", "fa-solid fa-layer-group", "SaaS Plus", "Vendor SaaS with KPMG customisation, integrations or data flows."],
                ] as [HostKey, string, string, string][]).map(([k, ico, title, desc]) => (
                  <button key={k} type="button" className={`st-type ${k}`} role="radio" aria-checked={type === k} disabled={!ready} onClick={() => setType(k)}>
                    <span className="ti"><i className={ico} /></span><b>{title}</b><small>{desc}</small><i className="fa-solid fa-circle-check ck" />
                  </button>
                ))}
              </div>
            </div>
            <div className="st-foot">
              <Link href="/requests" className="st-btn">Cancel</Link>
              <button type="button" className="st-btn primary" disabled={!(ready && type)} onClick={create}><i className="fa-solid fa-plus" />Create new request</button>
            </div>
          </div>
        </div>
      ) : (
        <div id="add-request-view" className="pt-2 animate-fade-in w-full">
          <div className="vi-head" id="intakeHead">
            <div className="vi-names">
              <div className="vi-name"><span className="vi-name-ico" style={{ "--ic": "#2563EB" } as CSSProperties}><i className="fa-regular fa-folder" /></span><span className="vi-name-txt"><span>Project Name</span><b>{form.v.project || "To be added"}</b></span></div>
              <div className="vi-name"><span className="vi-name-ico" style={{ "--ic": "#7C3AED" } as CSSProperties}><i className="fa-solid fa-cube" /></span><span className="vi-name-txt"><span>Solution Name</span><b>{form.v.name || "To be added"}</b></span></div>
            </div>
            <div className="vi-actions"><button type="button" className="with-label" onClick={() => { setStep("start"); window.scrollTo({ top: 0 }); }}><i className="fa-solid fa-arrow-rotate-left" /><span>Change</span></button></div>
            <div className="vi-meta">
              <div className="meta-item"><span>Solution type</span><span className="pill" style={{ "--tc": TYPE_COLOR[type!] } as CSSProperties}>{TYPE_LABEL[type!]}</span></div>
              <div className="meta-item"><span>Status</span><span className="pill pill-draft">Draft</span></div>
              <div className="meta-item"><span>APM / TPM ID</span><b>{form.v.apm || "Manual intake"}</b></div>
              <div className="meta-item"><span>Assessment created by</span><b>Sec Team</b></div>
            </div>
          </div>
          <div className="bg-white dark:bg-slate-850 rounded-3xl shadow-xl border border-slate-200 dark:border-slate-700 overflow-hidden mb-12">
            <div className="p-6 space-y-6">
              <IntakeForm mode="add" data={form} onChange={setForm} host={type!}
                onSubmit={() => { toast("Request submitted · moving to intake verification"); setTimeout(() => router.push("/requests"), 900); }} />
            </div>
          </div>
        </div>
      )}
      <footer className="vi-foot">© 2026 KPMG | All rights reserved | v3.0.1</footer>
    </main>
  );
}
