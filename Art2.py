"use client";

import React, { useState, useEffect } from "react";
import DOMPurify from "dompurify";
import { useRouter } from "next/navigation";
import { X, Search } from "lucide-react";
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
  const [showSolutionTypeModal, setShowSolutionTypeModal] = useState(false);
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

    setShowSolutionTypeModal(false);

    // Existing navigation same rahega
    router.push(`/requests/add?solution_type=${selectedSolutionType.value}`);
  };

  const breadcrumbs = [
    { label: "Home", href: "/" },
    { label: "Requests", href: "/requests" },
    { label: "Add Request" },
  ];

  return (
    <>
      <Breadcrumbs items={breadcrumbs} />

      {isFullLoading && <LoadingOverlay />}
      <div
        className={clsx(
          "bg-white dark:bg-slate-900 w-full min-h-[90vh] overflow-hidden transform transition-all duration-300",
          isClosingModal ? "scale-95 opacity-0" : "scale-100 opacity-100",
        )}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between px-8 py-5 border-b border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900">
          <h2 className="text-xl font-bold text-slate-900 dark:text-blue-400 tracking-tight">
            Add Request
          </h2>
        </div>

        <div className="p-8 bg-white dark:bg-slate-900 overflow-y-auto max-h-[calc(85vh-80px)] custom-scrollbar space-y-6">
          <div className="flex items-center justify-between gap-4 p-4 bg-blue-50/50 dark:bg-slate-800/50 rounded-xl border border-blue-100 dark:border-slate-700">
            <p className="text-[13px] font-medium text-slate-700 dark:text-slate-300">
              Search from KIEPs (Don't have an APM / TPM ID.
              {/* <span className="text-blue-600 dark:text-blue-400 font-bold cursor-pointer underline" onClick={() => router.push("/requests/add")}>Click here</span> */}
              <span
                className="text-blue-600 dark:text-blue-400 font-bold cursor-pointer underline"
                onClick={() => setShowSolutionTypeModal(true)}
              >
                Click here
              </span>
              )
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="relative flex-1">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400">
                <Search className="w-5 h-5" />
              </div>
              <input
                type="text"
                value={searchValue}
                onChange={handleSearchValueChange}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleSearch();
                }}
                className="block w-full pl-11 pr-4 py-2.5 border border-slate-200 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-800 text-sm text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500/20 outline-none transition-all"
                placeholder="Search APM ID"
              />
            </div>
            <button
              onClick={handleSearch}
              disabled={loading}
              className={`px-8 py-2.5 bg-blue-600 text-white rounded-lg font-bold text-xs uppercase tracking-wider  transition-all shadow-md disabled:opacity-50 ${!loading ? "cursor-pointer" : "cursor-not-allowed"}`}
            >
              Search
            </button>
          </div>

          {error && (
            <div
              className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-800 dark:text-red-300 text-sm font-medium"
              dangerouslySetInnerHTML={{
                __html: DOMPurify.sanitize(error),
              }}
            />
          )}

          <div className="border border-gray-200 dark:border-slate-700 rounded-xl overflow-hidden shadow-sm">
            <table className="w-full text-left border-collapse table-auto">
              <thead className="sticky top-0 z-30 border-b border-blue-100 dark:border-slate-700 backdrop-blur-sm bg-[#f0f7ff] dark:bg-slate-800">
                <tr>
                  <th className="px-4 py-4 text-center font-semibold uppercase tracking-wider text-[#2563eb] dark:text-[#adcbfb] text-[11px]">
                    Project Name
                  </th>
                  <th className="px-4 py-4 text-center font-semibold uppercase tracking-wider text-[#2563eb] dark:text-[#adcbfb] text-[11px]">
                    Solution Name
                  </th>
                  <th className="px-4 py-4 text-center font-semibold uppercase tracking-wider text-[#2563eb] dark:text-[#adcbfb] text-[11px]">
                    APM ID
                  </th>
                  <th className="px-4 py-4 text-center font-semibold uppercase tracking-wider text-[#2563eb] dark:text-[#adcbfb] text-[11px]">
                    Family ID
                  </th>
                  <th className="px-4 py-4 text-center font-semibold uppercase tracking-wider text-[#2563eb] dark:text-[#adcbfb] text-[11px]">
                    Solution Type
                  </th>
                  <th className="px-4 py-4 text-center font-semibold uppercase tracking-wider text-[#2563eb] dark:text-[#adcbfb] text-[11px]">
                    Action
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-slate-700">
                {loading && !apmData ? (
                  <tr>
                    <td
                      colSpan={5}
                      className="px-6 py-12 text-center text-slate-400 animate-pulse text-[10px] font-bold uppercase tracking-widest"
                    >
                      Loading...
                    </td>
                  </tr>
                ) : apmData ? (
                  <tr className="bg-white dark:bg-slate-900 transition-colors hover:bg-gray-50 dark:hover:bg-slate-900">
                    <td
                      className="px-3 py-5 align-middle text-center border-none font-semibold text-slate-800 dark:text-white"
                      style={{ fontSize: "10.5px" }}
                    >
                      {apmData.project_name}
                    </td>
                    <td
                      className="px-3 py-5 align-middle text-center border-none font-normal text-slate-600 dark:text-slate-400"
                      style={{ fontSize: "10.5px" }}
                    >
                      {apmData.solution_name}
                    </td>
                    <td className="px-3 py-5 align-middle text-center border-none">
                      <span
                        className="bg-blue-50 dark:bg-dark-highlight-blue text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800/50 px-2 py-1 rounded font-medium"
                        style={{ fontSize: "10.5px" }}
                      >
                        {apmData.apm_id}
                      </span>
                    </td>
                    <td
                      className="px-3 py-5 align-middle text-center border-none font-normal text-slate-600 dark:text-slate-400"
                      style={{ fontSize: "10.5px" }}
                    >
                      {apmData.family_id}
                    </td>
                    <td
                      className="px-3 py-5 align-middle text-center border-none font-normal text-slate-600 dark:text-slate-400 w-50"
                      style={{ fontSize: "10.5px" }}
                    >
                      {apmData?.isExisting ? (
                        <span
                          className={`inline-flex items-center rounded-md px-2 py-[2px] text-[10px] font-semibold border whitespace-nowrap
                                                    ${
                                                      apmData?.solution_type ===
                                                      1
                                                        ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                                                        : apmData?.solution_type ===
                                                            2
                                                          ? "bg-blue-50 text-blue-700 border-blue-200"
                                                          : apmData?.solution_type ===
                                                              3
                                                            ? "bg-purple-50 text-purple-700 border-purple-200"
                                                            : "bg-gray-50 text-gray-600 border-gray-200"
                                                    }
                                                `}
                        >
                          {apmData.solution_type === 1
                            ? "KPMG Hosted"
                            : apmData.solution_type === 2
                              ? "SaaS"
                              : apmData.solution_type === 3
                                ? "SaaS Plus"
                                : "NA"}
                          {/* {apmData?.solution_type ?? "NA"} */}
                        </span>
                      ) : (
                        <Select
                          options={options}
                          value={
                            options.find((opt: any) => opt.value === isSaas) ||
                            null
                          }
                          onChange={(option: any) => setIsSaas(option.value)}
                          placeholder="Select an option"
                          styles={isDarkMode ? darkModeStyles : customStyles}
                          className="react-select-container"
                          classNamePrefix="react-select"
                          menuPortalTarget={
                            typeof document !== "undefined"
                              ? document.body
                              : null
                          }
                          menuPosition="fixed"
                          menuPlacement="auto"
                        />
                      )}
                      {/* <label className="flex items-center cursor-pointer px-2 py-1 bg-slate-50 dark:bg-[#1e293b] rounded-full border border-slate-200 dark:border-[#334155] mr-2">
                                                <input
                                                type="radio"
                                                value="1"
                                                checked={isSaas == "1"}
                                                onChange={(e) => setIsSaas(e.target.value)}
                                                className="mr-1.5! align-middle! accent-blue-600 dark:accent-[#ADCBFB] cursor-pointer"
                                                />
                                                <span className="text-xs font-bold uppercase tracking-wide dark:text-white">YES</span>
                                            </label>
                                            <label className="flex items-center cursor-pointer px-2 py-1 bg-slate-50 dark:bg-[#1e293b] rounded-full border border-slate-200 dark:border-[#334155]">
                                                <input
                                                type="radio"
                                                value="0"
                                                checked={isSaas == "0"}
                                                onChange={(e) => setIsSaas(e.target.value)}
                                                className="mr-1.5! align-middle! accent-blue-600 dark:accent-[#ADCBFB] cursor-pointer"
                                                />
                                                <span className="text-xs font-bold uppercase tracking-wide dark:text-white">NO</span>
                                            </label> */}
                    </td>
                    <td className="px-3 py-5 align-middle text-center border-none">
                      <div className="flex justify-center">
                        {!apmData?.isExisting ? (
                          <button
                            onClick={() => setIsOpen(true)}
                            disabled={loading || isSaas === ""}
                            className="px-4 py-2 rounded-lg cursor-pointer border border-blue-200 dark:border-blue-900/50 text-white bg-blue-600 font-bold text-xs shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            {loading ? "..." : "Create intake form"}
                          </button>
                        ) : apmData.actionType === "edit_intake" ? (
                          <button
                            onClick={() =>
                              router.push(
                                `/requests/${apmData.sgp_id}/edit/?activeTab=2`,
                              )
                            }
                            className="px-4 py-2 rounded-lg cursor-pointer border border-blue-200 dark:border-blue-900/50 text-white bg-blue-600 font-bold text-xs shadow-sm"
                          >
                            Edit intake form
                          </button>
                        ) : apmData.actionType === "restart_assessment" ? (
                          <button
                            onClick={() => {
                              setSelectedSgpId(apmData.sgp_id);
                              setShowConfirmStartAssessment(true);
                            }}
                            className="px-4 py-2 rounded-lg cursor-pointer border border-blue-200 dark:border-blue-900/50 text-white bg-blue-600 font-bold text-xs shadow-sm"
                          >
                            Restart assessment
                          </button>
                        ) : (
                          <span className="inline-flex items-center rounded-md px-2.5 py-1 text-[11px] font-semibold border bg-gray-50 text-gray-700 border-gray-200 whitespace-nowrap">
                            {apmData.statusString || "NA"}
                          </span>
                        )}
                      </div>
                    </td>
                  </tr>
                ) : (
                  !apmData &&
                  !loading && (
                    <tr>
                      <td
                        colSpan={5}
                        className="text-center py-12 text-slate-500 dark:text-slate-400 italic text-sm"
                      >
                        No data available. Please perform a search.
                      </td>
                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm">
          <div className="bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-[#1E293B] w-full max-w-[480px] mx-4 overflow-hidden flex flex-col shadow-2xl rounded-2xl">
            {loading && <LoadingOverlay />}
            <div className="bg-blue-50 dark:bg-blue-900/40 px-5 py-4 border-b border-blue-100 dark:border-blue-800 flex items-center justify-between">
              <h3 className="text-[13px] font-bold text-[#00338D] dark:text-blue-400">
                Confirm Request Creation
              </h3>
              <button
                onClick={() => setIsOpen(false)}
                className="text-slate-400 hover:text-rose-500 transition-colors cursor-pointer"
                aria-label="Close"
              >
                <X size={18} />
              </button>
            </div>
            <div className="p-6 space-y-4">
              <div className="space-y-1.5">
                <p className="text-[13px] text-center text-slate-700 dark:text-slate-300 tracking-wide block">
                  You are about to create a request for a{" "}
                  <span className="text-kpmg-default">
                    <b>{`${options.find((o: any) => o.value === isSaas)?.label}`}</b>
                  </span>{" "}
                  Application. <br /> {`Do you want to continue?`}
                </p>
              </div>
              <div className="pt-2 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className="px-4 py-1.5 text-[13px] hover:-translate-y-0.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 transition-colors cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={() => handleCreateIntake(apmData.apm_id)}
                  className="bg-submit-btn hover:-translate-y-0.5 flex gap-2 items-center text-white px-4 py-1.5 rounded-lg text-[13px] transition-all shadow-lg cursor-pointer"
                >
                  Yes, Continue
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {showSolutionTypeModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm">
          <div className="bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-[#1E293B] w-full max-w-md rounded-2xl shadow-2xl">
            <div className="flex items-center justify-between px-5 py-4 border-b border-slate-200 dark:border-slate-700">
              <h3 className="text-sm font-bold text-[#00338D] dark:text-blue-400">
                Select Solution Type
              </h3>

              <button
                onClick={() => {
                  setShowSolutionTypeModal(false);
                  setSolutionTypeError("");
                  setSelectedSolutionType(null);
                }}
              >
                <X size={18} />
              </button>
            </div>

            <div className="p-5 space-y-4">
              <div>
                <label className="block mb-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                  Solution Type <span className="text-red-500">*</span>
                </label>

                <Select
                  options={Typeoptions}
                  value={selectedSolutionType}
                  onChange={(option: any) => setSelectedSolutionType(option)}
                  placeholder="Select Solution Type"
                  styles={isDarkMode ? darkModeStyles : customStyles}
                />

                {solutionTypeError && (
                  <p className="mt-1 text-xs font-medium text-red-600 dark:text-red-400">
                    {solutionTypeError}
                  </p>
                )}
              </div>

              <div className="flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => {
                    setShowSolutionTypeModal(false);
                    setSolutionTypeError("");
                    setSelectedSolutionType(null);
                  }}
                  className="px-4 py-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 cursor-pointer"
                >
                  Cancel
                </button>

                <button
                  type="button"
                  onClick={handleSolutionTypeSubmit}
                  className="px-4 py-2 rounded-lg bg-blue-600 text-white font-medium cursor-pointer"
                >
                  Submit
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
      {showConfirmStartAssessment && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm"
          onClick={(e) =>
            e.target === e.currentTarget && setShowConfirmStartAssessment(false)
          }
        >
          <div className="bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-[#1E293B] w-full max-w-[480px] mx-4 overflow-hidden shadow-2xl rounded-2xl">
            {isSubmittingAPI && <LoadingOverlay />}
            <div className="bg-blue-50 dark:bg-blue-900/40 px-5 py-4 border-b border-blue-100 dark:border-blue-800 flex items-center justify-between">
              <h3 className="text-[13px] font-bold text-[#00338D] dark:text-blue-400">
                Confirm Action
              </h3>
              <button
                onClick={() => setShowConfirmStartAssessment(false)}
                className="text-slate-400 hover:text-rose-500"
              >
                <X size={18} />
              </button>
            </div>
            <div className="p-6 space-y-4">
              <p className="text-[13px] text-slate-700 dark:text-slate-300">
                Are you sure you want to start a new assessment cycle? If yes,
                please select review type.
              </p>
              <div>
                <label className="block mb-1 text-sm font-medium text-slate-700 dark:text-slate-300">
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
                  <p className="mt-1 text-[12px] text-red-600 font-medium">
                    {reviewTypeError}
                  </p>
                )}
              </div>
              <div className="pt-2 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowConfirmStartAssessment(false)}
                  className="px-4 py-1.5 bg-kpmg-blue cursor-pointer text-[13px] rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
                >
                  Close
                </button>
                <button
                  type="button"
                  onClick={onStartAssessment}
                  disabled={isSubmittingAPI}
                  className="bg-kpmg-blue cursor-pointer text-white px-4 py-1.5 rounded-lg text-[13px] shadow-lg"
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
