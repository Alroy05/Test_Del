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

/* Styles from the request-add design (light / dark tokens):
   brand #1E3A8A / #7DA2FF, brand-soft #E8EEFF / #1B2547, surface #FFFFFF / #121831,
   surface-2 #F9FAFD / #0F1529, border #E6E9F2 / #232B45, text #0F1B3D / #E6EAF5,
   muted #5B6785 / #A3AEC8, faint #8A94AD / #6F7A96, focus #3B6CF6 / #7DA2FF. */
const mutedCls = "text-[#5B6785] dark:text-[#A3AEC8]";
const faintCls = "text-[#8A94AD] dark:text-[#6F7A96]";
const borderCls = "border-[#E6E9F2] dark:border-[#232B45]";
const focusCls =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#3B6CF6] dark:focus-visible:outline-[#7DA2FF]";
const brandFillCls =
  "bg-[#1E3A8A] text-white dark:bg-[#7DA2FF] dark:text-[#0F172B]";
const btnCls = `inline-flex items-center justify-center gap-2 h-9 px-4 rounded-[10px] text-[13px] font-semibold whitespace-nowrap cursor-pointer transition-all ${focusCls}`;
const ghostBtnCls = `${btnCls} border ${borderCls} bg-white dark:bg-[#121831] text-[#0F1B3D] dark:text-[#E6EAF5] hover:bg-[#F3F5FB] dark:hover:bg-[#182040]`;
const primaryBtnCls = `${btnCls} ${brandFillCls} shadow-[0_8px_18px_-10px_rgba(30,58,138,0.7)] hover:brightness-110 disabled:opacity-45 disabled:cursor-not-allowed disabled:shadow-none disabled:hover:brightness-100`;
const stepNumCls =
  "grid place-items-center size-[22px] shrink-0 rounded-full text-[11.5px] font-bold transition-colors";
const stepNumOffCls =
  "bg-[#E6E9F2] text-[#8A94AD] dark:bg-[#232B45] dark:text-[#6F7A96]";
const sectionLabelCls =
  "flex flex-wrap items-center gap-x-2.5 gap-y-1 mb-3 text-[14px] font-semibold text-[#0F1B3D] dark:text-[#E6EAF5]";
const answerCls = `group flex items-center gap-3 w-full p-3.5 rounded-xl border text-left cursor-pointer transition-all disabled:cursor-not-allowed disabled:opacity-60 ${focusCls}`;
const answerOffCls = `${borderCls} bg-white dark:bg-[#121831] hover:border-[#D5DAE7] hover:bg-[#F9FAFD] dark:hover:border-[#2F3958] dark:hover:bg-[#182040]`;
const answerOnCls =
  "border-[#1E3A8A] bg-[#E8EEFF]/55 shadow-[0_0_0_3px_rgba(59,108,246,0.12)] dark:border-[#7DA2FF] dark:bg-[#1B2547]/70 dark:shadow-[0_0_0_3px_rgba(125,162,255,0.14)]";
const tileCls =
  "grid place-items-center size-9 shrink-0 rounded-[10px] text-[#1E3A8A] bg-[#E8EEFF] dark:text-[#7DA2FF] dark:bg-[#1B2547]";
const pillCls =
  "inline-flex items-center px-[10px] py-[3px] rounded-full text-[12px] font-semibold whitespace-nowrap";
const neutralPillCls =
  "text-[#475569] bg-[#475569]/11 dark:text-[#A3AEC8] dark:bg-[#A3AEC8]/14";
const colHeadCls =
  "text-[11px] font-semibold uppercase tracking-wider text-[#8A94AD] dark:text-[#6F7A96]";
const modalScrimCls =
  "fixed inset-0 z-50 flex items-center justify-center bg-[#0F1B3D]/35 dark:bg-black/55 backdrop-blur-sm";
const modalCls = `bg-white dark:bg-[#121831] border ${borderCls} w-full max-w-[480px] mx-4 overflow-hidden flex flex-col rounded-2xl shadow-[0_24px_60px_-20px_rgba(15,27,61,0.45)]`;
const modalHeadCls = `flex items-center justify-between px-5 py-3.5 border-b ${borderCls} bg-[linear-gradient(100deg,#EEF3FF_0%,#F4EFFF_55%,#FDF0F7_100%)] dark:bg-[linear-gradient(100deg,#141D3F_0%,#1B1840_55%,#251633_100%)]`;
const modalTitleCls =
  "text-[14px] font-bold text-[#1E3A8A] dark:text-[#7DA2FF]";
const modalCloseCls = `grid place-items-center size-7 rounded-lg cursor-pointer text-[#8A94AD] dark:text-[#6F7A96] hover:text-rose-500 hover:bg-white/70 dark:hover:bg-white/5 transition-colors ${focusCls}`;

/* Solution type cards, in the order of the design. Keys are the solution type values. */
const TYPE_CARDS: {
  value: number;
  Icon: React.ElementType;
  desc: string;
  tile: string;
  on: string;
  check: string;
  pill: string;
}[] = [
  {
    value: 2,
    Icon: Cloud,
    desc: "Vendor-hosted software used as-is through a subscription.",
    tile: "text-[#0E7490] bg-[#0E7490]/11 dark:text-[#22D3EE] dark:bg-[#22D3EE]/14",
    on: "border-[#0E7490] bg-[#0E7490]/[0.05] shadow-[0_0_0_3px_rgba(14,116,144,0.12)] dark:border-[#22D3EE] dark:bg-[#22D3EE]/[0.07] dark:shadow-[0_0_0_3px_rgba(34,211,238,0.12)]",
    check: "bg-[#0E7490] dark:bg-[#22D3EE]",
    pill: "text-[#0E7490] bg-[#0E7490]/11 dark:text-[#22D3EE] dark:bg-[#22D3EE]/14",
  },
  {
    value: 1,
    Icon: Server,
    desc: "Built or hosted by KPMG, e.g. on ONE Platform or a KPMG data centre.",
    tile: "text-[#047857] bg-[#047857]/11 dark:text-[#4ADE9F] dark:bg-[#4ADE9F]/14",
    on: "border-[#047857] bg-[#047857]/[0.05] shadow-[0_0_0_3px_rgba(4,120,87,0.12)] dark:border-[#4ADE9F] dark:bg-[#4ADE9F]/[0.07] dark:shadow-[0_0_0_3px_rgba(74,222,159,0.12)]",
    check: "bg-[#047857] dark:bg-[#4ADE9F]",
    pill: "text-[#047857] bg-[#047857]/11 dark:text-[#4ADE9F] dark:bg-[#4ADE9F]/14",
  },
  {
    value: 3,
    Icon: Layers,
    desc: "Vendor SaaS with KPMG customisation, integrations or data flows.",
    tile: "text-[#7C3AED] bg-[#7C3AED]/11 dark:text-[#A78BFA] dark:bg-[#A78BFA]/14",
    on: "border-[#7C3AED] bg-[#7C3AED]/[0.05] shadow-[0_0_0_3px_rgba(124,58,237,0.12)] dark:border-[#A78BFA] dark:bg-[#A78BFA]/[0.07] dark:shadow-[0_0_0_3px_rgba(167,139,250,0.12)]",
    check: "bg-[#7C3AED] dark:bg-[#A78BFA]",
    pill: "text-[#7C3AED] bg-[#7C3AED]/11 dark:text-[#A78BFA] dark:bg-[#A78BFA]/14",
  },
];

/* Tick that fades in on the selected answer / solution type card */
const CheckMark = ({ on, className }: { on: boolean; className?: string }) => (
  <span
    aria-hidden="true"
    className={clsx(
      "grid place-items-center size-[18px] shrink-0 rounded-full text-white dark:text-[#0F172B] transition-all duration-150",
      on ? "opacity-100 scale-100" : "opacity-0 scale-75",
      className,
    )}
  >
    <Check className="size-3" strokeWidth={3} />
  </span>
);


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
  const rowGridCls = isExisting
    ? "sm:grid-cols-[18px_minmax(0,0.9fr)_minmax(0,1.2fr)_minmax(0,1.2fr)_minmax(0,1fr)]"
    : "sm:grid-cols-[18px_minmax(0,0.9fr)_minmax(0,1.3fr)_minmax(0,1.3fr)]";

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
      <div
        className={clsx(
          "bg-white dark:bg-slate-900 text-[#0F1B3D] dark:text-[#E6EAF5] w-full min-h-[90vh] transform transition-all duration-300",
          isClosingModal ? "scale-95 opacity-0" : "scale-100 opacity-100",
        )}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mx-auto w-full max-w-[980px] px-3 sm:px-4 pt-3 pb-10">
          <div
            className={`rounded-2xl border ${borderCls} bg-white dark:bg-[#121831] shadow-[0_1px_2px_rgba(15,27,61,0.04),0_8px_24px_-16px_rgba(15,27,61,0.18)] dark:shadow-[0_1px_2px_rgba(0,0,0,0.3),0_8px_24px_-16px_rgba(0,0,0,0.7)] overflow-hidden`}
          >
            {/* 1. APM / TPM ID */}
            <div className="p-4 sm:p-5">
              <div className={sectionLabelCls}>
                <span className={clsx(stepNumCls, brandFillCls)}>1</span>
                Do you have an APM / TPM ID for this solution?
              </div>

              <div
                className="grid grid-cols-1 sm:grid-cols-2 gap-3"
                role="radiogroup"
                aria-label="Has an APM / TPM ID"
              >
                <button
                  type="button"
                  role="radio"
                  aria-checked={isApmSearch}
                  onClick={chooseHasApm}
                  className={clsx(
                    answerCls,
                    isApmSearch ? answerOnCls : answerOffCls,
                  )}
                >
                  <span className={tileCls}>
                    <Search className="size-4" />
                  </span>
                  <span className="flex-1 min-w-0 leading-snug">
                    <b className="block text-[13.5px] font-semibold">
                      Yes, I have one
                    </b>
                    <small className={`block text-[12px] ${mutedCls}`}>
                      Find the application in KIEPs
                    </small>
                  </span>
                  <CheckMark
                    on={isApmSearch}
                    className="bg-[#1E3A8A] dark:bg-[#7DA2FF]"
                  />
                </button>
                <button
                  type="button"
                  role="radio"
                  aria-checked={isManual}
                  disabled={loading}
                  onClick={chooseNoApm}
                  className={clsx(
                    answerCls,
                    isManual ? answerOnCls : answerOffCls,
                  )}
                >
                  <span className={tileCls}>
                    <Keyboard className="size-4" />
                  </span>
                  <span className="flex-1 min-w-0 leading-snug">
                    <b className="block text-[13.5px] font-semibold">
                      No, not yet
                    </b>
                    <small className={`block text-[12px] ${mutedCls}`}>
                      Continue with a manual intake; the ID can be added later
                    </small>
                  </span>
                  <CheckMark
                    on={isManual}
                    className="bg-[#1E3A8A] dark:bg-[#7DA2FF]"
                  />
                </button>
              </div>

              {/* search is always shown; it's disabled when there's no APM / TPM ID */}
              <div
                className={clsx(
                  "mt-4 transition-opacity",
                  isManual && "opacity-50",
                )}
              >
                <div className={`mb-1.5 text-[12px] font-medium ${mutedCls}`}>
                  Search from KIEPs by APM / TPM ID
                </div>
                {/* a div, not a label: globals.css makes every label inline-block, which breaks the row */}
                <div
                  className={clsx(
                    `flex items-center gap-2 w-full h-11 pl-3.5 pr-1.5 rounded-xl border ${borderCls} transition-all`,
                    isManual
                      ? "bg-[#F9FAFD] dark:bg-[#0F1529] cursor-not-allowed"
                      : "bg-white dark:bg-[#0F1529] focus-within:border-[#3B6CF6] focus-within:shadow-[0_0_0_3px_rgba(59,108,246,0.14)] dark:focus-within:border-[#7DA2FF] dark:focus-within:shadow-[0_0_0_3px_rgba(125,162,255,0.16)]",
                  )}
                >
                  <Search
                    className={`size-4 shrink-0 ${faintCls}`}
                    aria-hidden="true"
                  />
                  <input
                    type="text"
                    value={searchValue}
                    onChange={handleSearchValueChange}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") handleSearch();
                    }}
                    disabled={isManual}
                    autoComplete="off"
                    aria-label="Search APM ID"
                    className="flex-1 min-w-0 h-full bg-transparent outline-none text-[13.5px] text-[#0F1B3D] dark:text-[#E6EAF5] placeholder:text-[#8A94AD] dark:placeholder:text-[#6F7A96] disabled:cursor-not-allowed"
                    placeholder="Search APM ID"
                  />
                  {searchValue && (
                    <button
                      type="button"
                      aria-label="Clear search"
                      disabled={isManual}
                      onClick={() =>
                        handleSearchValueChange({ target: { value: "" } })
                      }
                      className={`grid place-items-center size-7 shrink-0 rounded-lg cursor-pointer ${faintCls} hover:text-[#0F1B3D] hover:bg-[#F3F5FB] dark:hover:text-[#E6EAF5] dark:hover:bg-[#182040] transition-colors ${focusCls}`}
                    >
                      <X className="size-3.5" />
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={handleSearch}
                    disabled={loading || isManual}
                    className={`inline-flex items-center gap-1.5 h-8 px-3.5 shrink-0 rounded-lg text-[12.5px] font-semibold ${brandFillCls} transition-all hover:brightness-110 disabled:opacity-50 disabled:hover:brightness-100 ${!loading && !isManual ? "cursor-pointer" : "cursor-not-allowed"} ${focusCls}`}
                  >
                    <Search className="size-3.5" />
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

                <div
                  className={`flex items-center justify-between gap-3 mt-2.5 text-[12px] ${faintCls}`}
                >
                  <span className="min-w-0 truncate">
                    {!isManual && apmData ? "Selected application" : ""}
                  </span>
                  <span className="shrink-0">Source: KIEPs</span>
                </div>

                {!isManual && (
                  <div className="mt-2">
                    {loading && !apmData ? (
                      <div
                        className={`rounded-xl border ${borderCls} px-4 py-8 text-center animate-pulse text-[11px] font-bold uppercase tracking-widest ${faintCls}`}
                      >
                        Loading...
                      </div>
                    ) : apmData ? (
                      <div
                        className={`rounded-xl border ${borderCls} overflow-hidden`}
                      >
                        <div
                          className={`hidden sm:grid ${rowGridCls} items-center gap-x-4 px-4 py-2.5 border-b ${borderCls} bg-[#F9FAFD] dark:bg-[#0F1529] ${colHeadCls}`}
                        >
                          <span />
                          <span>APM ID</span>
                          <span>Project Name</span>
                          <span>Solution Name</span>
                          {isExisting && (
                            <span>
                              {showStatus
                                ? "Solution Type / Status"
                                : "Solution Type"}
                            </span>
                          )}
                        </div>
                        <div
                          className={`grid grid-cols-[18px_minmax(0,1fr)] ${rowGridCls} items-center gap-x-4 gap-y-2.5 px-4 py-3.5 bg-[#E8EEFF]/45 dark:bg-[#1B2547]/55`}
                        >
                          <span
                            aria-hidden="true"
                            className="grid place-items-center size-[18px] rounded-full border-2 border-[#1E3A8A] dark:border-[#7DA2FF] self-start sm:self-center"
                          >
                            <span className="size-2 rounded-full bg-[#1E3A8A] dark:bg-[#7DA2FF]" />
                          </span>
                          <span className="min-w-0">
                            <small className={`block sm:hidden ${colHeadCls}`}>
                              APM ID
                            </small>
                            <span className="text-[13px] font-semibold text-[#1E3A8A] dark:text-[#7DA2FF] [overflow-wrap:anywhere]">
                              {apmData.apm_id}
                            </span>
                          </span>
                          <span className="min-w-0 col-start-2 sm:col-start-auto leading-snug">
                            <small className={`block sm:hidden ${colHeadCls}`}>
                              Project Name
                            </small>
                            <b className="block text-[13px] font-semibold [overflow-wrap:anywhere]">
                              {apmData.project_name}
                            </b>
                            <small className={`block text-[12px] ${mutedCls}`}>
                              Family ID {apmData.family_id}
                            </small>
                          </span>
                          <span className="min-w-0 col-start-2 sm:col-start-auto leading-snug">
                            <small className={`block sm:hidden ${colHeadCls}`}>
                              Solution Name
                            </small>
                            <b className="block text-[13px] font-semibold [overflow-wrap:anywhere]">
                              {apmData.solution_name}
                            </b>
                          </span>
                          {isExisting && (
                            <span className="min-w-0 col-start-2 sm:col-start-auto flex flex-wrap items-center gap-1.5">
                              <span
                                className={clsx(
                                  pillCls,
                                  existingType
                                    ? existingType.pill
                                    : neutralPillCls,
                                )}
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
                                  className={clsx(
                                    pillCls,
                                    neutralPillCls,
                                    "whitespace-normal",
                                  )}
                                >
                                  {apmData.statusString || "NA"}
                                </span>
                              )}
                            </span>
                          )}
                        </div>
                      </div>
                    ) : null}
                  </div>
                )}
              </div>
            </div>

            {/* 2. Solution type */}
            <div className={`p-4 sm:p-5 border-t ${borderCls}`}>
              <div className={sectionLabelCls}>
                <span
                  className={clsx(
                    stepNumCls,
                    ready ? brandFillCls : stepNumOffCls,
                  )}
                >
                  2
                </span>
                Choose the solution type
                {existingType && (
                  <span className={`text-[12px] font-medium ${faintCls}`}>
                    (already set for this request)
                  </span>
                )}
              </div>
              <div
                className="grid grid-cols-1 sm:grid-cols-3 gap-3"
                role="radiogroup"
                aria-label="Solution type"
              >
                {TYPE_CARDS.map(({ value, Icon, desc, tile, on, check }) => {
                  const option = (isManual ? Typeoptions : options).find(
                    (opt: any) => opt.value === value,
                  );
                  const checked = pickedType === value;
                  return (
                    <button
                      key={value}
                      type="button"
                      role="radio"
                      aria-checked={checked}
                      disabled={!canPickType}
                      onClick={() => pickSolutionType(option)}
                      className={clsx(
                        `relative flex flex-col items-start gap-1.5 p-4 rounded-xl border text-left transition-all ${focusCls}`,
                        checked
                          ? on
                          : `${borderCls} bg-white dark:bg-[#121831]`,
                        canPickType
                          ? "cursor-pointer"
                          : "cursor-not-allowed",
                        canPickType &&
                          !checked &&
                          "hover:border-[#D5DAE7] hover:bg-[#F9FAFD] dark:hover:border-[#2F3958] dark:hover:bg-[#182040]",
                        !canPickType && !checked && "opacity-55",
                      )}
                    >
                      <span
                        className={`grid place-items-center size-9 rounded-[10px] mb-1 ${tile}`}
                      >
                        <Icon className="size-[18px]" />
                      </span>
                      <b className="text-[13.5px] font-semibold">
                        {option?.label}
                      </b>
                      <small
                        className={`text-[12px] leading-snug ${mutedCls}`}
                      >
                        {desc}
                      </small>
                      <CheckMark
                        on={checked}
                        className={`absolute top-3.5 right-3.5 ${check}`}
                      />
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

            {/* Actions */}
            <div
              className={`flex flex-wrap items-center justify-end gap-2.5 px-4 sm:px-5 py-3.5 border-t ${borderCls} bg-[#F9FAFD] dark:bg-[#0F1529]`}
            >
              <Link href="/requests" className={ghostBtnCls}>
                Cancel
              </Link>
              {isManual ? (
                <button
                  type="button"
                  onClick={handleSolutionTypeSubmit}
                  disabled={!selectedSolutionType}
                  className={primaryBtnCls}
                >
                  <Plus className="size-4" />
                  Create new request
                </button>
              ) : !apmData?.isExisting ? (
                <button
                  type="button"
                  onClick={() => setIsOpen(true)}
                  disabled={!apmData || loading || isSaas === ""}
                  className={primaryBtnCls}
                >
                  {loading ? (
                    "..."
                  ) : (
                    <>
                      <Plus className="size-4" />
                      Create intake form
                    </>
                  )}
                </button>
              ) : apmData.actionType === "edit_intake" ? (
                <button
                  type="button"
                  onClick={() =>
                    router.push(`/requests/${apmData.sgp_id}/edit/?activeTab=2`)
                  }
                  className={primaryBtnCls}
                >
                  <Pencil className="size-3.5" />
                  Edit intake form
                </button>
              ) : apmData.actionType === "restart_assessment" ? (
                <button
                  type="button"
                  onClick={() => {
                    setSelectedSgpId(apmData.sgp_id);
                    setShowConfirmStartAssessment(true);
                  }}
                  className={primaryBtnCls}
                >
                  <RotateCcw className="size-3.5" />
                  Restart assessment
                </button>
              ) : null}
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
