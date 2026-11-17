"use client";

import React, { useState, useEffect } from "react";
import DOMPurify from "dompurify";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  X,
  Search,
  Check,
  Cloud,
  Info,
  Keyboard,
  Layers,
  Pencil,
  Plus,
  RotateCcw,
  Server,
} from "lucide-react";
import { callBackend, callBackendFormData } from "@/lib/helpers";
import toast from "react-hot-toast";
import clsx from "clsx";
import LoadingOverlay from "@/components/LoadingOverlay";
import Select from "react-select";
import { customStyles, darkModeStyles } from "@/lib/styles";
import Breadcrumbs from "@/components/Breadcrumbs";
import "@/styles/pages/request-add.css";

interface ApmData {
  project_name: string;
  solution_name: string;
  apm_id: string;
  family_id: string;
  isExisting?: boolean;
  sgp_id?: string | null;
  solution_type?: number | null;
  actionType?: "edit_intake" | "restart_assessment" | "status";
  statusString?: string | null;
}

/* The page itself uses the design stylesheet (request-add.css, scoped to .pg-request-add).
   These Tailwind classes style the popups, which render outside that wrapper.
   Light / dark tokens: brand #1E3A8A / #7DA2FF, surface #FFFFFF / #121831,
   border #E6E9F2 / #232B45, text #0F1B3D / #E6EAF5, muted #5B6785 / #A3AEC8. */
const mutedCls = "text-[#5B6785] dark:text-[#A3AEC8]";
const borderCls = "border-[#E6E9F2] dark:border-[#232B45]";
const focusCls =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#3B6CF6] dark:focus-visible:outline-[#7DA2FF]";
const brandFillCls =
  "bg-[#1E3A8A] text-white dark:bg-[#7DA2FF] dark:text-[#0F172B]";
const btnCls = `inline-flex items-center justify-center gap-2 h-9 px-4 rounded-[10px] text-[13px] font-semibold whitespace-nowrap cursor-pointer transition-all ${focusCls}`;
const ghostBtnCls = `${btnCls} border ${borderCls} bg-white dark:bg-[#121831] text-[#0F1B3D] dark:text-[#E6EAF5] hover:bg-[#F3F5FB] dark:hover:bg-[#182040]`;
const primaryBtnCls = `${btnCls} ${brandFillCls} shadow-[0_8px_18px_-10px_rgba(30,58,138,0.7)] hover:brightness-110 disabled:opacity-45 disabled:cursor-not-allowed disabled:shadow-none disabled:hover:brightness-100`;
const modalScrimCls =
  "fixed inset-0 z-50 flex items-center justify-center bg-[#0F1B3D]/35 dark:bg-black/55 backdrop-blur-sm";
const modalCls = `bg-white dark:bg-[#121831] border ${borderCls} w-full max-w-[480px] mx-4 overflow-hidden flex flex-col rounded-2xl shadow-[0_24px_60px_-20px_rgba(15,27,61,0.45)]`;
const modalHeadCls = `flex items-center justify-between px-5 py-3.5 border-b ${borderCls} bg-[linear-gradient(100deg,#EEF3FF_0%,#F4EFFF_55%,#FDF0F7_100%)] dark:bg-[linear-gradient(100deg,#141D3F_0%,#1B1840_55%,#251633_100%)]`;
const modalTitleCls =
  "text-[14px] font-bold text-[#1E3A8A] dark:text-[#7DA2FF]";
const modalCloseCls = `grid place-items-center size-7 rounded-lg cursor-pointer text-[#8A94AD] dark:text-[#6F7A96] hover:text-rose-500 hover:bg-white/70 dark:hover:bg-white/5 transition-colors ${focusCls}`;

/* Grey pill for a status, or a solution type the page doesn't know */
const neutralPillStyle: React.CSSProperties = {
  color: "var(--text-muted)",
  background: "var(--surface-2)",
  border: "1px solid var(--border)",
};

/* Filled tick for the selected answer / solution type card; .ck in the stylesheet
   positions it and sets its colour, the tick is cut out in the card colour */
const CheckMark = ({ size }: { size: number }) => (
  <span className="ck" aria-hidden="true">
    <span
      className="grid place-items-center rounded-full bg-current"
      style={{ width: size, height: size }}
    >
      <Check
        size={size - 6}
        strokeWidth={3.2}
        style={{ color: "var(--surface)" }}
      />
    </span>
  </span>
);

/* Solution type cards, in the order of the design. `value` is the solution type sent to the API,
   `key` the design's card class, light / dark the type colour (same as the stylesheet's --tc). */
const TYPE_CARDS: {
  value: number;
  key: "saas" | "kpmg" | "saasplus";
  Icon: React.ElementType;
  desc: string;
  light: string;
  dark: string;
}[] = [
  {
    value: 2,
    key: "saas",
    Icon: Cloud,
    desc: "Vendor-hosted software used as-is through a subscription.",
    light: "#0E7490",
    dark: "#22D3EE",
  },
  {
    value: 1,
    key: "kpmg",
    Icon: Server,
    desc: "Built or hosted by KPMG, e.g. on ONE Platform or a KPMG data centre.",
    light: "#047857",
    dark: "#34D399",
  },
  {
    value: 3,
    key: "saasplus",
    Icon: Layers,
    desc: "Vendor SaaS with KPMG customisation, integrations or data flows.",
    light: "#7C3AED",
    dark: "#A78BFA",
  },
];

export default function AddRequest() {
  const [isClosingModal, setIsClosingModal] = useState(false);
  const [searchValue, setSearchValue] = useState("");
  const [apmData, setApmData] = useState<ApmData | null | any>(null);
  const [loading, setLoading] = useState(false);
  const [isFullLoading, setIsFullLoading] = useState(false);
  const [error, setError] = useState("");
  const [isSaas, setIsSaas] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  // "Do you have an APM / TPM ID?": "no" is the manual intake path (was the "Click here" popup)
  const [hasApm, setHasApm] = useState<"yes" | "no" | null>(null);
  const [selectedSolutionType, setSelectedSolutionType] = useState<any>(null);

  const [showConfirmStartAssessment, setShowConfirmStartAssessment] =
    useState(false);
  const [isSubmittingAPI, setIsSubmittingAPI] = useState(false);
  const [selectedSgpId, setSelectedSgpId] = useState<string | null>(null);
  const [reviewType, setReviewType] = useState<any>(null);
  const [reviewTypeError, setReviewTypeError] = useState("");
  const reviewTypeOptions = [
    { label: "Major", value: "2" },
    { label: "Minor", value: "3" },
  ];
  const [currentRole] = useState(
    typeof window !== "undefined" ? localStorage.getItem("current_role") : "",
  );
  const allowedRoles = ["security resource"];

  const router = useRouter();

  const checkAccess = async () => {
    setIsFullLoading(true);
    await callBackend("request/add/", "GET");
    setIsFullLoading(false);
  };

  useEffect(() => {
    checkAccess();
  }, []);

  const handleSearch = async () => {
    if (!searchValue.trim()) {
      setError("Please enter an APM/TPM ID");
      return;
    }
    setLoading(true);
    setError("");
    setApmData(null);
    setIsSaas("");
    try {
      const formData = new FormData();
      formData.append("apm_solution_id", searchValue);
      formData.append("api_type", "search");
      const response = await callBackendFormData(
        `request/search-apm-solution-data/`,
        "POST",
        formData,
      );
      const result = response.data;

      if (result.status && result.data) {
        // setApmData(result.data);

        setApmData({
          ...result.data,
          isExisting: false,
          sgp_id: null,
          solution_type: null,
          canEditIntake: false,
        });
      } else {
        if (result.errors && result.data?.data) {
          setApmData({
            ...result.data?.data,
            isExisting: true,
            sgp_id: result.data?.sgp_id,
            solution_type: result.data?.solution_type,
            actionType: result.data?.action_type,
            statusString: result.data?.status_string,
          });

          const allErrors = Object.values(result.errors)
            .flat()
            .map((err, i) => `${err}`)
            .join("\n");

          setError(allErrors);
        } else if (result.message) {
          setError(result.message);
          console.log(JSON.stringify(result.message));
        } else {
          setError("Unknown error occurred");
        }
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSearchValueChange = (event: any) => {
    const value = event.target.value;
    setSearchValue(value);
    if (error) {
      setError("");
    }
    if (apmData) {
      setApmData(null);
    }
  };

  const onStartAssessment = () => {
    if (!reviewType) {
      setReviewTypeError("Review Type is required");
      return;
    }
    setReviewTypeError("");
    handleStartAssessment(selectedSgpId, Number(reviewType?.value));
  };

  const handleStartAssessment = async (sgpId: any, reviewType: number) => {
    if (!sgpId) return toast.error("Invalid SGP ID");
    setLoading(true);
    setIsSubmittingAPI(true);
    try {
      const { data } = await callBackend(
        `ca/${sgpId}/assessment/restart/ `,
        "POST",
        { reviewType },
      );
      if (data?.status) {
        toast.success(data.message || "New cycle initiated successfully!");
        setShowConfirmStartAssessment(false);
        if (allowedRoles.some((r) => currentRole?.toLowerCase().includes(r))) {
          router.push(`/requests`);
        } else {
          router.push(`/requests/${sgpId}/edit/?activeTab=2`);
        }
      } else {
        toast.error(data?.message || "Failed to start new cycle.");
      }
    } catch (error) {
      toast.error("Something went wrong.");
    } finally {
      setIsSubmittingAPI(false);
      setLoading(false);
    }
  };

  const handleCreateIntake = async (apmId: string) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("apm_solution_id", apmId);
      formData.append("api_type", "insert");
      formData.append("solution_type", isSaas);
      const response = await callBackendFormData(
        `request/search-apm-solution-data/`,
        "POST",
        formData,
      );
      const result = response.data;
      if (result.status && result.data?.sgpId) {
        setIsOpen(false);
        toast.success("Request Created Successfully");
        router.push(`/requests/${result.data.sgpId}/edit`);
      } else {
        setLoading(false);
        toast.error(result.message || "Failed to create intake form");
        setError(result.message || "Failed to create intake form");
      }
    } catch (err) {
      setError("Something went wrong.");
    } finally {
      setTimeout(() => {
        setLoading(false);
      }, 3000);
    }
  };

  const options: any = [
    { value: 1, label: "KPMG Hosted" },
    { value: 2, label: "SaaS" },
    { value: 3, label: "SaaS-Plus" },
  ];
  const Typeoptions: any = [
    { value: 1, label: "KPMG Hosted" },
    { value: 2, label: "SaaS" },
    { value: 3, label: "SaaS-Plus" },
  ];

  useEffect(() => {
    const observer = new MutationObserver(() => {
      setIsDarkMode(document.documentElement.classList.contains("dark"));
    });
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });
    setIsDarkMode(document.documentElement.classList.contains("dark"));
    return () => observer.disconnect();
  }, []);

  const [solutionTypeError, setSolutionTypeError] = useState("");

  const handleSolutionTypeSubmit = () => {
    if (!selectedSolutionType) {
      setSolutionTypeError("Solution Type is required");
      return;
    }

    setSolutionTypeError("");

    // Existing navigation same rahega
    router.push(`/requests/add?solution_type=${selectedSolutionType.value}`);
  };

  const breadcrumbs = [
    { label: "Home", href: "/" },
    { label: "Requests", href: "/requests" },
    { label: "Add Request" },
  ];

  /* View state for the design: nothing below changes what is sent or where the page goes */
  const isManual = hasApm === "no";
  // searching counts as "Yes, I have one" until an answer is picked
  const isApmSearch =
    hasApm === "yes" ||
    (hasApm === null &&
      (searchValue !== "" || !!apmData || loading || !!error));
  const isExisting = !!apmData?.isExisting;
  const ready = isManual || !!apmData; // solution type opens once this is settled
  const canPickType = isManual || (!!apmData && !isExisting);
  const pickedType: any = isManual
    ? (selectedSolutionType?.value ?? null)
    : isExisting
      ? (apmData?.solution_type ?? null)
      : isSaas === ""
        ? null
        : isSaas;
  const existingType = TYPE_CARDS.find(
    (t) => t.value === apmData?.solution_type,
  );
  const showStatus =
    isExisting &&
    apmData.actionType !== "edit_intake" &&
    apmData.actionType !== "restart_assessment";

  const chooseHasApm = () => {
    if (isManual) {
      setSelectedSolutionType(null);
      setSolutionTypeError("");
    }
    setHasApm("yes");
  };

  const chooseNoApm = () => {
    setHasApm("no");
    setSearchValue("");
    setError("");
    setApmData(null);
    setIsSaas("");
  };

  const pickSolutionType = (option: any) => {
    if (isManual) {
      setSelectedSolutionType(option);
      setSolutionTypeError("");
    } else {
      setIsSaas(option.value);
    }
  };

  return (
    <>
      <Breadcrumbs items={breadcrumbs} />

      {isFullLoading && <LoadingOverlay />}
      {/* the design stylesheet switches theme on [data-theme="dark"]; the app uses the .dark class */}
      <div data-theme={isDarkMode ? "dark" : "light"}>
        <div
          className={clsx(
            "pg-request-add w-full min-h-[90vh] px-3 transform transition-all duration-300",
            isClosingModal ? "scale-95 opacity-0" : "scale-100 opacity-100",
          )}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="st-wrap">
            <div className="st-card">
              {/* 1. APM / TPM ID */}
              <div className="st-sec">
                <div className="st-label">
                  <span className="n">1</span>
                  Do you have an APM / TPM ID for this solution?
                </div>
                <div
                  className="st-ask"
                  role="radiogroup"
                  aria-label="Has an APM / TPM ID"
                >
                  <button
                    type="button"
                    className="st-ans"
                    role="radio"
                    aria-checked={isApmSearch}
                    onClick={chooseHasApm}
                  >
                    <span className="ti">
                      <Search size={16} />
                    </span>
                    <span>
                      <b>Yes, I have one</b>
                      <small>Find the application in KIEPs</small>
                    </span>
                    <CheckMark size={18} />
                  </button>
                  <button
                    type="button"
                    className="st-ans"
                    role="radio"
                    aria-checked={isManual}
                    disabled={loading}
                    onClick={chooseNoApm}
                  >
                    <span className="ti">
                      <Keyboard size={16} />
                    </span>
                    <span>
                      <b>No, not yet</b>
                      <small>
                        Continue with a manual intake; the ID can be added later
                      </small>
                    </span>
                    <CheckMark size={18} />
                  </button>
                </div>

                {/* search is always shown; it's disabled when there's no APM / TPM ID */}
                <div className={clsx("st-find", isManual && "off")}>
                  <div className="st-sub-l">Search by APM / TPM ID</div>
                  {/* a div, not a label: globals.css gives every label a bottom margin */}
                  <div className="st-search">
                    <i aria-hidden="true">
                      <Search size={16} />
                    </i>
                    <input
                      type="search"
                      value={searchValue}
                      onChange={handleSearchValueChange}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") handleSearch();
                      }}
                      disabled={isManual}
                      autoComplete="off"
                      aria-label="Search APM ID"
                      placeholder="Search APM ID, e.g. GO-AV-00000117"
                    />
                    {searchValue && (
                      <button
                        type="button"
                        aria-label="Clear search"
                        disabled={isManual}
                        onClick={() =>
                          handleSearchValueChange({ target: { value: "" } })
                        }
                      >
                        <X size={14} />
                      </button>
                    )}
                    <button
                      type="button"
                      className={clsx(
                        "st-go disabled:opacity-60",
                        !loading && !isManual
                          ? "cursor-pointer"
                          : "cursor-not-allowed",
                      )}
                      onClick={handleSearch}
                      disabled={loading || isManual}
                    >
                      <Search size={13} />
                      Search
                    </button>
                  </div>

                  {error && (
                    <div className="flex items-start gap-2.5 mt-3 px-3.5 py-2.5 rounded-xl border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300 text-[13px] font-medium">
                      <Info
                        className="size-4 shrink-0 mt-[1px]"
                        aria-hidden="true"
                      />
                      <div
                        className="min-w-0 [overflow-wrap:anywhere] [&_a]:underline"
                        dangerouslySetInnerHTML={{
                          __html: DOMPurify.sanitize(error),
                        }}
                      />
                    </div>
                  )}

                  <div className="st-meta">
                    <span>
                      {!isManual && apmData ? "Selected application" : ""}
                    </span>
                    <span>Source: KIEPs</span>
                  </div>

                  {!isManual && loading && !apmData && (
                    <div className="st-list">
                      <div className="st-empty animate-pulse">Loading...</div>
                    </div>
                  )}
                  {!isManual && apmData && (
                    <div
                      className="st-list"
                      role="radiogroup"
                      aria-label="Applications"
                    >
                      {/* --th-fg: the stylesheet's dark-blue default is unreadable in dark mode */}
                      <div
                        className="st-row head"
                        style={{ "--th-fg": "var(--brand)" } as React.CSSProperties}
                      >
                        <span />
                        <span>APM / TPM ID</span>
                        <span>Project name</span>
                        <span>Solution name</span>
                      </div>
                      <div className="st-row" role="radio" aria-checked="true">
                        <span className="st-radio" />
                        <span className="st-apm [overflow-wrap:anywhere]">
                          {apmData.apm_id}
                        </span>
                        <span>
                          <b>{apmData.project_name}</b>
                          <small>Family ID {apmData.family_id}</small>
                        </span>
                        <span>
                          <b>{apmData.solution_name}</b>
                          {isExisting && (
                            <span className="flex flex-wrap gap-1.5 mt-1.5">
                              <span
                                className="pill"
                                style={
                                  existingType
                                    ? ({
                                        "--tc": isDarkMode
                                          ? existingType.dark
                                          : existingType.light,
                                        color: "var(--tc)",
                                        background:
                                          "color-mix(in srgb, var(--tc) 12%, var(--surface))",
                                      } as React.CSSProperties)
                                    : neutralPillStyle
                                }
                              >
                                {apmData.solution_type === 1
                                  ? "KPMG Hosted"
                                  : apmData.solution_type === 2
                                    ? "SaaS"
                                    : apmData.solution_type === 3
                                      ? "SaaS Plus"
                                      : "NA"}
                              </span>
                              {showStatus && (
                                <span
                                  className="pill"
                                  style={{
                                    ...neutralPillStyle,
                                    whiteSpace: "normal",
                                  }}
                                >
                                  {apmData.statusString || "NA"}
                                </span>
                              )}
                            </span>
                          )}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* 2. Solution type */}
              <div className="st-sec">
                <div className="st-label">
                  <span className={clsx("n", !ready && "off")}>2</span>
                  Choose the solution type
                </div>
                <div
                  className="st-types"
                  role="radiogroup"
                  aria-label="Solution type"
                >
                  {TYPE_CARDS.map(({ value, key, Icon, desc }) => {
                    const option = (isManual ? Typeoptions : options).find(
                      (opt: any) => opt.value === value,
                    );
                    const checked = pickedType === value;
                    return (
                      <button
                        key={value}
                        type="button"
                        className={`st-type ${key}`}
                        role="radio"
                        aria-checked={checked}
                        disabled={!canPickType}
                        // an existing request keeps its type: show it at full strength
                        style={
                          checked && !canPickType ? { opacity: 1 } : undefined
                        }
                        onClick={() => pickSolutionType(option)}
                      >
                        <span className="ti">
                          <Icon size={16} />
                        </span>
                        <b>{option?.label}</b>
                        <small>{desc}</small>
                        <CheckMark size={17} />
                      </button>
                    );
                  })}
                </div>
                {solutionTypeError && (
                  <p className="mt-2 text-[12px] font-medium text-red-600 dark:text-red-400">
                    {solutionTypeError}
                  </p>
                )}
              </div>

              <div className="st-foot">
                <Link href="/requests" className="st-btn">
                  Cancel
                </Link>
                {isManual ? (
                  <button
                    type="button"
                    className="st-btn primary"
                    onClick={handleSolutionTypeSubmit}
                    disabled={!selectedSolutionType}
                  >
                    <Plus size={15} />
                    Create new request
                  </button>
                ) : !apmData?.isExisting ? (
                  <button
                    type="button"
                    className="st-btn primary"
                    onClick={() => setIsOpen(true)}
                    disabled={!apmData || loading || isSaas === ""}
                  >
                    {loading ? (
                      "..."
                    ) : (
                      <>
                        <Plus size={15} />
                        Create intake form
                      </>
                    )}
                  </button>
                ) : apmData.actionType === "edit_intake" ? (
                  <button
                    type="button"
                    className="st-btn primary"
                    onClick={() =>
                      router.push(
                        `/requests/${apmData.sgp_id}/edit/?activeTab=2`,
                      )
                    }
                  >
                    <Pencil size={14} />
                    Edit intake form
                  </button>
                ) : apmData.actionType === "restart_assessment" ? (
                  <button
                    type="button"
                    className="st-btn primary"
                    onClick={() => {
                      setSelectedSgpId(apmData.sgp_id);
                      setShowConfirmStartAssessment(true);
                    }}
                  >
                    <RotateCcw size={14} />
                    Restart assessment
                  </button>
                ) : null}
              </div>
            </div>
          </div>
        </div>
      </div>

      {isOpen && (
        <div className={modalScrimCls}>
          <div className={modalCls}>
            {loading && <LoadingOverlay />}
            <div className={modalHeadCls}>
              <h3 className={modalTitleCls}>Confirm Request Creation</h3>
              <button
                onClick={() => setIsOpen(false)}
                className={modalCloseCls}
                aria-label="Close"
              >
                <X size={18} />
              </button>
            </div>
            <div className="p-6 space-y-4">
              <div className="space-y-1.5">
                <p className="text-[13.5px] leading-relaxed text-center text-[#0F1B3D] dark:text-[#E6EAF5] block">
                  You are about to create a request for a{" "}
                  <span className="text-[#1E3A8A] dark:text-[#7DA2FF]">
                    <b>{`${options.find((o: any) => o.value === isSaas)?.label}`}</b>
                  </span>{" "}
                  Application. <br /> {`Do you want to continue?`}
                </p>
              </div>
              <div className="pt-2 flex justify-end gap-2.5">
                <button
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className={ghostBtnCls}
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={() => handleCreateIntake(apmData.apm_id)}
                  className={primaryBtnCls}
                >
                  Yes, Continue
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {showConfirmStartAssessment && (
        <div
          className={modalScrimCls}
          onClick={(e) =>
            e.target === e.currentTarget && setShowConfirmStartAssessment(false)
          }
        >
          <div className={modalCls}>
            {isSubmittingAPI && <LoadingOverlay />}
            <div className={modalHeadCls}>
              <h3 className={modalTitleCls}>Confirm Action</h3>
              <button
                onClick={() => setShowConfirmStartAssessment(false)}
                className={modalCloseCls}
                aria-label="Close"
              >
                <X size={18} />
              </button>
            </div>
            <div className="p-6 space-y-4">
              <p className="text-[13.5px] leading-relaxed text-[#0F1B3D] dark:text-[#E6EAF5]">
                Are you sure you want to start a new assessment cycle? If yes,
                please select review type.
              </p>
              <div>
                <label
                  className={`block mb-1.5 text-[12.5px] font-semibold ${mutedCls}`}
                >
                  Review Type <span className="text-red-500">*</span>
                </label>
                <Select
                  options={reviewTypeOptions}
                  isClearable
                  value={reviewType}
                  onChange={(val: any) => {
                    setReviewType(val);
                    setReviewTypeError("");
                  }}
                  placeholder="Select review type"
                  styles={isDarkMode ? darkModeStyles : customStyles}
                  menuPortalTarget={
                    typeof document !== "undefined" ? document.body : null
                  }
                  menuPosition="fixed"
                />
                {reviewTypeError && (
                  <p className="mt-1 text-[12px] text-red-600 dark:text-red-400 font-medium">
                    {reviewTypeError}
                  </p>
                )}
              </div>
              <div className="pt-2 flex justify-end gap-2.5">
                <button
                  type="button"
                  onClick={() => setShowConfirmStartAssessment(false)}
                  className={ghostBtnCls}
                >
                  Close
                </button>
                <button
                  type="button"
                  onClick={onStartAssessment}
                  disabled={isSubmittingAPI}
                  className={primaryBtnCls}
                >
                  {isSubmittingAPI ? "Processing..." : "Yes, Start"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
