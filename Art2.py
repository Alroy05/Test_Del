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

/* Design tokens from the request-add design, light / dark:
   page #FFFFFF / #0F172B, surface #FFFFFF / #121831, surface-2 #F9FAFD / #0F1529,
   surface-hover #F3F5FB / #182040, border #E6E9F2 / #232B45, border-strong #D5DAE7 / #2F3958,
   text #0F1B3D / #E6EAF5, muted #5B6785 / #A3AEC8, faint #8A94AD / #6F7A96,
   brand #1E3A8A / #7DA2FF, brand-soft #E8EEFF / #1B2547, focus #3B6CF6 / #7DA2FF. */
const textCls = "text-[#0F1B3D] dark:text-[#E6EAF5]";
const mutedCls = "text-[#5B6785] dark:text-[#A3AEC8]";
const faintCls = "text-[#8A94AD] dark:text-[#6F7A96]";
const brandTextCls = "text-[#1E3A8A] dark:text-[#7DA2FF]";
const surfaceCls = "bg-white dark:bg-[#121831]";
const hoverSurfaceCls = "hover:bg-[#F3F5FB] dark:hover:bg-[#182040]";
const borderCls = "border-[#E6E9F2] dark:border-[#232B45]";
const focusCls =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#3B6CF6] dark:focus-visible:outline-[#7DA2FF]";
/* brand fill: dark mode puts near-black text on the light brand blue */
const brandFillCls =
  "bg-[#1E3A8A] text-white dark:bg-[#7DA2FF] dark:text-[#0B1020]";

/* Page layout */
const cardCls = `border ${borderCls} rounded-[18px] ${surfaceCls} shadow-[0_18px_40px_-30px_rgba(15,27,61,0.45)] overflow-hidden`;
const sectionCls = "px-4 py-5 sm:px-[30px] sm:py-[22px]";
const sectionLabelCls = `flex items-center gap-2.5 mb-3 text-[13.5px] font-bold ${textCls}`;
const stepNumCls =
  "inline-flex items-center justify-center size-6 shrink-0 rounded-full text-[12px] font-extrabold";
const stepNumOffCls = `${faintCls} bg-[#F9FAFD] dark:bg-[#0F1529] border ${borderCls}`;

/* "Do you have an APM / TPM ID?" answer cards */
const answerCls = `relative flex items-center gap-3.5 py-4 pl-4 pr-11 rounded-[14px] text-left border-[1.5px] cursor-pointer transition-[border-color,background-color,box-shadow] duration-150 disabled:cursor-not-allowed ${focusCls}`;
const answerOffCls = `${borderCls} ${surfaceCls} hover:border-[#8C9AC3] dark:hover:border-[#4C6099]`;
const answerOnCls =
  "border-[#1E3A8A] bg-[#1E3A8A]/6 shadow-[0_0_0_3px_rgba(30,58,138,0.14)] dark:border-[#7DA2FF] dark:bg-[#7DA2FF]/6 dark:shadow-[0_0_0_3px_rgba(125,162,255,0.14)]";
const answerIconCls =
  "inline-flex items-center justify-center size-10 shrink-0 rounded-[11px] text-[#1E3A8A] bg-[#E8EEFF] dark:text-[#7DA2FF] dark:bg-[#1B2547]";

/* Search bar: pill with a blue → violet → pink gradient border */
const searchBarCls =
  "flex items-center gap-2.5 h-[46px] pl-4 pr-[5px] rounded-full border-[1.5px] border-transparent transition-shadow " +
  "[background:linear-gradient(#FFFFFF,#FFFFFF)_padding-box,linear-gradient(90deg,#3B6CF6_0%,#8B5CF6_50%,#EC4899_100%)_border-box] " +
  "dark:[background:linear-gradient(#121831,#121831)_padding-box,linear-gradient(90deg,#3B6CF6_0%,#8B5CF6_50%,#EC4899_100%)_border-box]";
const searchBarOnCls =
  "shadow-[0_10px_26px_-16px_rgba(139,92,246,0.45)] focus-within:shadow-[0_0_0_4px_rgba(139,92,246,0.16),0_10px_28px_-12px_rgba(139,92,246,0.4)]";
const searchBarOffCls = "grayscale cursor-not-allowed";

/* Result list */
const listCls = `max-h-[330px] overflow-y-auto border ${borderCls} rounded-xl`;
const rowCls =
  "grid grid-cols-[28px_minmax(0,1fr)] min-[761px]:grid-cols-[28px_170px_minmax(0,1fr)_minmax(0,1fr)] items-center gap-3.5 w-full px-4 py-3 text-left";
const rowNarrowCellCls = "max-[760px]:col-start-2"; // stacks the name cells under the ID on phones

const pillCls =
  "inline-flex items-center px-2.5 py-[3px] rounded-full text-[12px] font-semibold whitespace-nowrap";
const neutralPillCls = `${mutedCls} bg-[#F9FAFD] dark:bg-[#0F1529] border ${borderCls}`;

/* Footer buttons */
const footBtnCls = `inline-flex items-center gap-2 px-[18px] py-2.5 rounded-[11px] text-[13px] font-bold border cursor-pointer transition-[filter,background-color] ${focusCls}`;
const footGhostBtnCls = `${footBtnCls} ${borderCls} ${surfaceCls} ${textCls} ${hoverSurfaceCls}`;
const footPrimaryBtnCls = `${footBtnCls} ${brandFillCls} border-[#1E3A8A] dark:border-[#7DA2FF] shadow-[0_10px_22px_-12px_rgba(11,42,122,0.8)] enabled:hover:brightness-110 disabled:opacity-45 disabled:cursor-not-allowed disabled:shadow-none`;

/* Popups */
const btnCls = `inline-flex items-center justify-center gap-2 h-9 px-4 rounded-[10px] text-[13px] font-semibold whitespace-nowrap cursor-pointer transition-all ${focusCls}`;
const ghostBtnCls = `${btnCls} border ${borderCls} ${surfaceCls} ${textCls} ${hoverSurfaceCls}`;
const primaryBtnCls = `${btnCls} ${brandFillCls} shadow-[0_8px_18px_-10px_rgba(30,58,138,0.7)] hover:brightness-110 disabled:opacity-45 disabled:cursor-not-allowed disabled:shadow-none disabled:hover:brightness-100`;
const modalScrimCls =
  "fixed inset-0 z-50 flex items-center justify-center bg-[#0F1B3D]/35 dark:bg-black/55 backdrop-blur-sm";
const modalCls = `${surfaceCls} border ${borderCls} w-full max-w-[480px] mx-4 overflow-hidden flex flex-col rounded-2xl shadow-[0_24px_60px_-20px_rgba(15,27,61,0.45)]`;
const modalHeadCls = `flex items-center justify-between px-5 py-3.5 border-b ${borderCls} bg-[linear-gradient(100deg,#EEF3FF_0%,#F4EFFF_55%,#FDF0F7_100%)] dark:bg-[linear-gradient(100deg,#141D3F_0%,#1B1840_55%,#251633_100%)]`;
const modalTitleCls = `text-[14px] font-bold ${brandTextCls}`;
const modalCloseCls = `grid place-items-center size-7 rounded-lg cursor-pointer ${faintCls} hover:text-rose-500 hover:bg-white/70 dark:hover:bg-white/5 transition-colors ${focusCls}`;

/* Filled tick on the selected answer / solution type card. It takes its colour from
   the parent's text colour, and the tick is cut out in the card colour. */
const CheckMark = ({ on, className }: { on: boolean; className: string }) => (
  <span
    aria-hidden="true"
    className={clsx(
      "absolute inline-flex items-center justify-center size-[18px] rounded-full bg-current transition-opacity duration-150",
      on ? "opacity-100" : "opacity-0",
      className,
    )}
  >
    <Check
      className="size-3 text-white dark:text-[#121831]"
      strokeWidth={3.2}
    />
  </span>
);

/* Solution type cards, in the order of the design. `value` is the solution type sent to the API.
   `tc` sets the card's colour (--tc) for light / dark; the card classes below read it. */
const TYPE_CARDS: {
  value: number;
  Icon: React.ElementType;
  desc: string;
  tc: string;
}[] = [
  {
    value: 2,
    Icon: Cloud,
    desc: "Vendor-hosted software used as-is through a subscription.",
    tc: "[--tc:#0E7490] dark:[--tc:#22D3EE]",
  },
  {
    value: 1,
    Icon: Server,
    desc: "Built or hosted by KPMG, e.g. on ONE Platform or a KPMG data centre.",
    tc: "[--tc:#047857] dark:[--tc:#34D399]",
  },
  {
    value: 3,
    Icon: Layers,
    desc: "Vendor SaaS with KPMG customisation, integrations or data flows.",
    tc: "[--tc:#7C3AED] dark:[--tc:#A78BFA]",
  },
];
const typeCardCls = `relative flex flex-col items-start gap-1.5 p-4 rounded-[14px] text-left border-[1.5px] transition-[border-color,background-color,box-shadow] duration-150 disabled:cursor-not-allowed ${focusCls}`;
const typeCardOffCls = `${borderCls} ${surfaceCls} enabled:cursor-pointer enabled:hover:border-[color-mix(in_srgb,var(--tc)_50%,#E6E9F2)] dark:enabled:hover:border-[color-mix(in_srgb,var(--tc)_50%,#232B45)]`;
const typeCardOnCls =
  "border-(--tc) bg-[color-mix(in_srgb,var(--tc)_6%,transparent)] shadow-[0_0_0_3px_color-mix(in_srgb,var(--tc)_14%,transparent)] enabled:cursor-pointer";
const typeIconCls =
  "inline-flex items-center justify-center size-9 rounded-[10px] text-(--tc) bg-[color-mix(in_srgb,var(--tc)_12%,transparent)]";
const typePillCls = `${pillCls} text-(--tc) bg-[color-mix(in_srgb,var(--tc)_12%,transparent)]`;

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
      <div
        className={clsx(
          `bg-white dark:bg-[#0F172B] ${textCls} w-full min-h-[90vh] px-3 transform transition-all duration-300`,
          isClosingModal ? "scale-95 opacity-0" : "scale-100 opacity-100",
        )}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mt-2 mb-6">
          <div className={cardCls}>
            {/* 1. APM / TPM ID */}
            <div className={sectionCls}>
              <div className={sectionLabelCls}>
                <span className={clsx(stepNumCls, brandFillCls)}>1</span>
                Do you have an APM / TPM ID for this solution?
              </div>
              <div
                className="grid grid-cols-1 min-[761px]:grid-cols-2 gap-3"
                role="radiogroup"
                aria-label="Has an APM / TPM ID"
              >
                {[
                  {
                    checked: isApmSearch,
                    onClick: chooseHasApm,
                    Icon: Search,
                    title: "Yes, I have one",
                    note: "Find the application in KIEPs",
                  },
                  {
                    checked: isManual,
                    onClick: chooseNoApm,
                    Icon: Keyboard,
                    title: "No, not yet",
                    note: "Continue with a manual intake; the ID can be added later",
                    disabled: loading,
                  },
                ].map(({ checked, onClick, Icon, title, note, disabled }) => (
                  <button
                    key={title}
                    type="button"
                    role="radio"
                    aria-checked={checked}
                    disabled={disabled}
                    onClick={onClick}
                    className={clsx(
                      answerCls,
                      checked ? answerOnCls : answerOffCls,
                    )}
                  >
                    <span className={answerIconCls}>
                      <Icon className="size-4" />
                    </span>
                    <span className="min-w-0">
                      <b className={`block text-[14px] font-bold ${textCls}`}>
                        {title}
                      </b>
                      <small className={`block mt-0.5 text-[12px] ${mutedCls}`}>
                        {note}
                      </small>
                    </span>
                    <CheckMark
                      on={checked}
                      className={`top-1/2 right-4 -translate-y-1/2 ${brandTextCls}`}
                    />
                  </button>
                ))}
              </div>

              {/* search is always shown; it's disabled when there's no APM / TPM ID */}
              <div
                className={clsx(
                  `mt-[18px] pt-[18px] border-t border-dashed ${borderCls}`,
                  isManual && "opacity-45",
                )}
              >
                <div
                  className={`mb-2.5 text-[12.5px] font-semibold ${mutedCls}`}
                >
                  Search by APM / TPM ID
                </div>
                <div
                  className={clsx(
                    searchBarCls,
                    isManual ? searchBarOffCls : searchBarOnCls,
                  )}
                >
                  <Search
                    className="size-4 shrink-0 text-[#8B5CF6]"
                    aria-hidden="true"
                  />
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
                    className={`flex-1 min-w-0 h-10 text-[14px] bg-transparent outline-none ${textCls} placeholder:text-[#8A94AD] dark:placeholder:text-[#6F7A96] disabled:cursor-not-allowed [&::-webkit-search-cancel-button]:appearance-none`}
                  />
                  {searchValue && (
                    <button
                      type="button"
                      aria-label="Clear search"
                      disabled={isManual}
                      onClick={() =>
                        handleSearchValueChange({ target: { value: "" } })
                      }
                      className={`inline-flex items-center justify-center size-7 shrink-0 rounded-full cursor-pointer disabled:cursor-not-allowed ${faintCls} hover:bg-[#F3F5FB] hover:text-[#0F1B3D] dark:hover:bg-[#182040] dark:hover:text-[#E6EAF5] ${focusCls}`}
                    >
                      <X className="size-3.5" />
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={handleSearch}
                    disabled={loading || isManual}
                    className={`inline-flex items-center gap-[7px] h-9 px-[18px] shrink-0 rounded-full text-[13px] font-bold ${brandFillCls} shadow-[0_8px_18px_-10px_rgba(11,42,122,0.8)] enabled:hover:brightness-[1.12] disabled:opacity-60 ${!loading && !isManual ? "cursor-pointer" : "cursor-not-allowed"} ${focusCls}`}
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
                  className={`flex justify-between gap-3 mx-0.5 mt-3.5 mb-2 text-[12px] ${faintCls}`}
                >
                  <span>
                    {!isManual && apmData ? "Selected application" : ""}
                  </span>
                  <span>Source: KIEPs</span>
                </div>

                {!isManual && loading && !apmData && (
                  <div className={listCls}>
                    <div
                      className={`px-4 py-[34px] text-center text-[13px] animate-pulse ${faintCls}`}
                    >
                      Loading...
                    </div>
                  </div>
                )}
                {!isManual && apmData && (
                  <div
                    className={listCls}
                    role="radiogroup"
                    aria-label="Applications"
                  >
                    <div
                      className={`${rowCls} max-[760px]:hidden sticky top-0 z-[1] py-[9px] border-b ${borderCls} bg-[#F9FAFD] dark:bg-[#0F1529] font-jakarta-sans text-[12.5px] font-semibold ${brandTextCls}`}
                    >
                      <span />
                      <span>APM / TPM ID</span>
                      <span>Project name</span>
                      <span>Solution name</span>
                    </div>
                    <div
                      role="radio"
                      aria-checked="true"
                      className={`${rowCls} bg-[#1E3A8A]/6 dark:bg-[#7DA2FF]/6 shadow-[inset_3px_0_0_#1E3A8A] dark:shadow-[inset_3px_0_0_#7DA2FF]`}
                    >
                      <span className="inline-flex items-center justify-center size-[18px] rounded-full border-2 border-[#1E3A8A] dark:border-[#7DA2FF]">
                        <span className="size-2 rounded-full bg-[#1E3A8A] dark:bg-[#7DA2FF]" />
                      </span>
                      <span
                        className={`font-mono text-[12.5px] font-semibold [overflow-wrap:anywhere] ${brandTextCls}`}
                      >
                        {apmData.apm_id}
                      </span>
                      <span className={rowNarrowCellCls}>
                        <b className={`text-[13px] font-semibold ${textCls}`}>
                          {apmData.project_name}
                        </b>
                        <small className={`block text-[11.5px] ${faintCls}`}>
                          Family ID {apmData.family_id}
                        </small>
                      </span>
                      <span className={rowNarrowCellCls}>
                        <b className={`text-[13px] font-semibold ${textCls}`}>
                          {apmData.solution_name}
                        </b>
                        {isExisting && (
                          <span className="flex flex-wrap gap-1.5 mt-1.5">
                            <span
                              className={
                                existingType
                                  ? `${typePillCls} ${existingType.tc}`
                                  : `${pillCls} ${neutralPillCls}`
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
                                className={`${pillCls} ${neutralPillCls} whitespace-normal`}
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
            <div className={`${sectionCls} border-t ${borderCls}`}>
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
              </div>
              <div
                className="grid grid-cols-1 min-[761px]:grid-cols-3 gap-3"
                role="radiogroup"
                aria-label="Solution type"
              >
                {TYPE_CARDS.map(({ value, Icon, desc, tc }) => {
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
                        typeCardCls,
                        tc,
                        checked ? typeCardOnCls : typeCardOffCls,
                        // an existing request keeps its type: the other cards fade out
                        !canPickType && !checked && "opacity-50",
                      )}
                    >
                      <span className={typeIconCls}>
                        <Icon className="size-4" />
                      </span>
                      <b className={`text-[14px] font-bold ${textCls}`}>
                        {option?.label}
                      </b>
                      <small
                        className={`text-[12px] leading-[1.45] ${mutedCls}`}
                      >
                        {desc}
                      </small>
                      <CheckMark
                        on={checked}
                        className="top-3.5 right-3.5 text-(--tc)"
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

            <div
              className={`flex flex-wrap justify-end items-center gap-2.5 px-4 sm:px-[30px] py-4 border-t ${borderCls} bg-[#FBFCFE] dark:bg-[#10162D]`}
            >
              <Link href="/requests" className={footGhostBtnCls}>
                Cancel
              </Link>
              {isManual ? (
                <button
                  type="button"
                  onClick={handleSolutionTypeSubmit}
                  disabled={!selectedSolutionType}
                  className={footPrimaryBtnCls}
                >
                  <Plus className="size-4" />
                  Create new request
                </button>
              ) : !apmData?.isExisting ? (
                <button
                  type="button"
                  onClick={() => setIsOpen(true)}
                  disabled={!apmData || loading || isSaas === ""}
                  className={footPrimaryBtnCls}
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
                  className={footPrimaryBtnCls}
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
                  className={footPrimaryBtnCls}
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
