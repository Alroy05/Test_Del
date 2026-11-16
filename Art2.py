'use client';

import React, { useEffect, useState, useRef, useMemo } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import ReactSelect from "react-select";
import DOMPurify from 'dompurify';
import DataTable from "@/components/DataTable";
import LoadingOverlay from "@/components/LoadingOverlay";
import { callBackend, callBackendFormData, forceDownload, downloadFile, downloadPdfFile, formatDateTime, actionBtn } from "@/lib/helpers";
import { customStyles, darkModeStyles } from "@/lib/styles";
import { toast } from "react-hot-toast";
import { ChevronDown, ChevronUp, Download, FileText, Fingerprint, History, LucideRotateCcw, Mail, MessageSquare, RotateCcwClock, RotateCcwSquare, Signal, Sparkles, Tag, UserPlus } from "lucide-react";
import TitleBar from "@/components/TitleBar";
import Breadcrumbs from "@/components/Breadcrumbs";
import { Rotate90DegreesCcwRounded } from "@mui/icons-material";

const downloadableFileRegEx =
  /\.(doc|docx|xls|xlsx|pdf|jpg|jpeg|png|gif|webp|txt|csv|ppt|pptx|zip|rar|7z)$/i;

/* Shared styles from the view-logs design (light / dark tokens):
   brand #1E3A8A / #7DA2FF, brand-soft #E8EEFF / #1B2547, surface #FFFFFF / #121831,
   border #E6E9F2 / #232B45, text #0F1B3D / #E6EAF5, muted #5B6785 / #A3AEC8, faint #8A94AD / #6F7A96.
   Sizes inside table cells are in em so they follow the DataTable cell font size. */
const mutedCls = "text-[#5B6785] dark:text-[#A3AEC8]";
const faintCls = "text-[#8A94AD] dark:text-[#6F7A96]";
const fileLinkCls =
  "inline-flex items-start gap-1.5 font-medium break-all text-[#1E3A8A] dark:text-[#7DA2FF] hover:underline";
const cellActionCls =
  "inline-flex items-center gap-[5px] whitespace-nowrap cursor-pointer text-[0.923em] font-semibold text-[#1E3A8A] dark:text-[#7DA2FF] hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#3B6CF6] rounded";

/* log type pill: [icon, colours] */
const TYPE_PILLS: Record<string, [React.ElementType, string]> = {
  Status: [Signal, "text-[#2563EB] bg-[#2563EB]/11 dark:text-[#8DB0FF] dark:bg-[#8DB0FF]/14"],
  AI: [Sparkles, "text-[#7C3AED] bg-[#7C3AED]/11 dark:text-[#A78BFA] dark:bg-[#A78BFA]/14"],
  Comment: [MessageSquare, "text-[#0E7490] bg-[#0E7490]/11 dark:text-[#22D3EE] dark:bg-[#22D3EE]/14"],
  Comments: [MessageSquare, "text-[#0E7490] bg-[#0E7490]/11 dark:text-[#22D3EE] dark:bg-[#22D3EE]/14"],
  Email: [Mail, "text-[#B45309] bg-[#B45309]/11 dark:text-[#FBBF24] dark:bg-[#FBBF24]/14"],
  Identifiers: [Fingerprint, "text-[#059669] bg-[#059669]/11 dark:text-[#34D399] dark:bg-[#34D399]/14"],
  Delegate: [UserPlus, "text-[#BE185D] bg-[#BE185D]/11 dark:text-[#F472B6] dark:bg-[#F472B6]/14"],
  Documents: [FileText, "text-[#475569] bg-[#475569]/11 dark:text-[#A3AEC8] dark:bg-[#A3AEC8]/14"],
  Artifacts: [FileText, "text-[#475569] bg-[#475569]/11 dark:text-[#A3AEC8] dark:bg-[#A3AEC8]/14"],
};
const DEFAULT_TYPE_PILL: [React.ElementType, string] =
  [Tag, "text-[#475569] bg-[#475569]/11 dark:text-[#A3AEC8] dark:bg-[#A3AEC8]/14"];

/* Date on the first line, time below it; falls back to the plain formatted value */
const DateCell = ({ value }: { value: any }) => {
  const formatted: any = formatDateTime(value);
  const match = typeof formatted === "string" ? formatted.match(/^(.+?)[,\s]+(\d{1,2}:\d{2}.*)$/) : null;

  return (
    <span className={`block text-[0.96em] ${mutedCls}`}>
      {match ? (
        <>
          <b className="block font-semibold text-[#0F1B3D] dark:text-[#E6EAF5]">{match[1]}</b>
          {match[2]}
        </>
      ) : (
        <b className="font-semibold text-[#0F1B3D] dark:text-[#E6EAF5]">{formatted}</b>
      )}
    </span>
  );
};

const Event10Value = ({
  value,
  requestId,
}: {
  value?: string | null;
  requestId: string;
}) => {
  const items = (value ?? "")
    .split("||")
    .map((item: string) => item.trim())
    .filter(Boolean);

  if (!items.length) {
    return <span className={faintCls}>-</span>;
  }

  return (
    <div className="space-y-1.5">
      {items.map((item: string, index: number) => {
        const filename = item
          .replace(/\\/g, "/")
          .split("/")
          .pop() ?? item;

        const hasDownloadableExtension =
          downloadableFileRegEx.test(filename);

        if (!hasDownloadableExtension) {
          return (
            <div key={index}>
              {item}
            </div>
          );
        }

        const serveFilesUrl = (
          process.env.NEXT_PUBLIC_SERVE_FILES ?? ""
        ).replace(/\/+$/, "");

        const normalizedRequestId = requestId
          .trim()
          .replace(/^\/+|\/+$/g, "");

        const encodedFilename = filename
          .split("/")
          .map(encodeURIComponent)
          .join("/");

        const fileApi =
          `${serveFilesUrl}/requestor/` +
          `${normalizedRequestId}/${encodedFilename}/`;

        const downloadUrl =
          `/download?api=${encodeURIComponent(btoa(fileApi))}` +
          `&filename=${encodeURIComponent(btoa(filename))}` +
          `&from=1`;

        return (
          <div key={index}>
            <Link
              href={downloadUrl}
              target="_blank"
              className={fileLinkCls}
            >
              <FileText className="size-[0.9em] shrink-0 mt-[0.3em]" />
              {filename}
            </Link>
          </div>
        );
      })}
    </div>
  );
};

const UpdateCell = ({ row, requestId }: { row: any; requestId: string }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  console.log(row)
  if (row.event == 4) {
    const parts = (row.new_value_str ?? "").split("||");
    const preview = parts[0] + "<br/><br/>";
    const extra = [parts[1], parts[2]].filter(Boolean).join("<br/><br/>");
    console.log(row.id)
    return (
      <div>
        <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(preview) }} />
        {isExpanded && (
          <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(extra) }} />
        )}
        <div className="flex items-center gap-[14px] mt-1.5">
          <button
            type="button"
            onClick={() => setIsExpanded(p => !p)}
            className={cellActionCls}
          >
            {isExpanded ? <ChevronUp className="size-[1em]" /> : <ChevronDown className="size-[1em]" />}
            {isExpanded ? "Read Less" : "Read More"}
          </button>
          <button
            type="button"
            className={cellActionCls}
            onClick={() => {
              const obj = {
                "sgpId": requestId,
                "id": row.id
              }
              const api = btoa(`/clearance/clearance-print-mail`);
              const url = `/download?api=${api}&formData=${encodeURIComponent(JSON.stringify(obj))}&filename=${btoa(`Email document - ${requestId}`)}&from=2`;
              window.open(url, '_blank', 'noopener,noreferrer');
            }}
          >
            <Download className="size-[0.95em]" />
            Download
          </button>
        </div>
      </div>
    );
  }

  // if (row.event == 3) {
  //   return (
  //     <div>
  //       {(row.new_value ?? "").split("||").map((filePath: string, index: number) => {
  //         const filename = filePath.split("/").pop();
  //         const newFilePath = filePath.replace(/\//g, "||");
  //         let api = btoa(`${process.env.NEXT_PUBLIC_SERVE_FILES}/${newFilePath}/`)
  //         return (
  //           <div key={index} className="pb-2">
  //             <Link href={`/download?api=${api}&filename=${btoa(filename!)}&from=1`} target="_blank"
  //               className="text-blue-600 hover:underline text-[13px] font-medium"
  //             >
  //               {filename}
  //             </Link>
  //           </div>
  //         );
  //       })}
  //     </div>
  //   );
  // }

  if (row.event == 3) {
    return (
      <div className="space-y-1.5">
        {(row.new_value ?? "")
          .split("||")
          .filter(Boolean)
          .map((filePath: string, index: number) => {
            const normalizedPath = filePath
              .replace(/\\/g, "/")
              .replace(/^storage\//, "");

            const filename = normalizedPath.split("/").pop();
            const api = btoa(`${process.env.NEXT_PUBLIC_SERVE_FILES}/${normalizedPath}/`);

            return (
              <div key={index}>
                <Link
                  href={`/download?api=${api}&filename=${btoa(filename!)}&from=1`}
                  target="_blank"
                  className={fileLinkCls}
                >
                  <FileText className="size-[0.9em] shrink-0 mt-[0.3em]" />
                  {filename}
                </Link>
              </div>
            );
          })}
      </div>
    );
  }

  if (row.event == 10) {
    return (
      <Event10Value
        value={row.new_value}
        requestId={requestId}
      />
    );
  }

  return <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(row.new_value_str) }} />;
};

const RequestorArtifactory = () => {
  const params = useParams();
  const requestId = params?.id as string;

  const objectToArray = (dropdown: any) =>
    Object.entries(dropdown).map(([key, value]) => ({ key, value }));

  const [logTypeOptions, setLogTypeOptions] = useState<any>();
  const [allData, setAllData] = useState<any>();
  const [tableData, setTableData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  const [sortColumn, setSortColumn] = useState<string>("created_date");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [isPageDropdownOpen, setIsPageDropdownOpen] = useState(false);
  const [tableError, setTableError] = useState('');
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new MutationObserver(() =>
      setIsDarkMode(document.documentElement.classList.contains("dark"))
    );
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
    setIsDarkMode(document.documentElement.classList.contains("dark"));
    return () => observer.disconnect();
  }, []);

  const getArtifactory = async () => {
    if (!requestId) return;
    setIsLoading(true);
    try {
      const { data } = await callBackend(`/request/requestor-artifactory/`, "POST", {
        sgpId: requestId,
        eventFilterStatus: "No",
      });
      if (data.status) {
        setAllData(data.data);
        setTableData(data.data.logUpdateData);
        setLogTypeOptions(objectToArray(data.data.logEventList));
      } else {
        toast.error(data.message);
      }
    } catch {
      toast.error('Something went wrong');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { getArtifactory(); }, []);

  const filter = async (filterData: any) => {
    if (!filterData?.length) {
      getArtifactory();
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append("sgpId", requestId);
    formData.append("eventFilterStatus", "Yes");
    if (filterData?.length) {
      filterData.forEach((f: any) => formData.append("eventFilter", f.value));
    }
    try {
      const { data } = await callBackendFormData(`/request/requestor-artifactory/`, "POST", formData);
      if (data.status) {
        setAllData(data.data);
        setTableData(data.data.logUpdateData);
        setLogTypeOptions(objectToArray(data.data.logEventList));
        setCurrentPage(1);
      } else {
        toast.error(data.message);
      }
    } catch {
      toast.error('Something went wrong');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSort = (column: string) => {
    if (sortColumn === column) {
      setSortOrder(prev => prev === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortOrder("asc");
    }
    setCurrentPage(1);
  };

  const sortedData = useMemo(() => {
    if (!sortColumn) return tableData;
    return [...tableData].sort((a, b) => {
      const aVal = a[sortColumn] ?? "";
      const bVal = b[sortColumn] ?? "";
      if (aVal < bVal) return sortOrder === "asc" ? -1 : 1;
      if (aVal > bVal) return sortOrder === "asc" ? 1 : -1;
      return 0;
    });
  }, [tableData, sortColumn, sortOrder]);

  const totalRecords = sortedData.length;
  const totalPages = Math.max(1, Math.ceil(totalRecords / pageSize));
  const paginatedData = sortedData.slice((currentPage - 1) * pageSize, currentPage * pageSize);


  const columns = useMemo(() => [
    {
      key: "created_date",
      label: "Date",
      sortable: true,
      width: "w-30",
      render: (value: any) => <DateCell value={value} />,
    },
    {
      key: "created_by_name",
      label: "Name",
      width: "w-36",
      render: (value: any) => (
        <span className="font-semibold">{value ?? "-"}</span>
      ),
    },
    {
      key: "response_for",
      label: "Response For",
      width: "w-40",
    },
    {
      key: "new_value_str",
      label: "Update",
      width: "w-94",
      render: (_: any, row: any) => <UpdateCell row={row} requestId={requestId} />,
    },
    {
      key: "old_value_str",
      label: "Old Data",
      width: "w-40",
      render: (value: any, row: any) =>
        row.event == 10 ? (
          <div className={mutedCls}>
            <Event10Value
              value={row.old_value ?? value}
              requestId={requestId}
            />
          </div>
        ) : value != null && value !== "" ? (
          <div
            className={mutedCls}
            dangerouslySetInnerHTML={{
              __html: DOMPurify.sanitize(value ?? ""),
            }}
          />
        ) : (
          <span className={faintCls}>-</span>
        ),
    },
    // {
    //   key: "old_value_str",
    //   label: "Old Data",
    //   width: "w-48",
    // },
    {
      key: "event_string",
      label: "Type",
      width: "w-36",
      render: (value: any) => {
        if (value == null || value === "") return <span className={faintCls}>-</span>;
        const [Icon, pillCls] = TYPE_PILLS[value] ?? DEFAULT_TYPE_PILL;
        return (
          <span className={`inline-flex items-start gap-1.5 max-w-full px-[9px] py-[3px] rounded-[1.1em] text-[0.885em] leading-snug font-semibold ${pillCls}`}>
            <Icon className="size-[0.95em] shrink-0 mt-[0.2em]" />
            <span className="min-w-0 break-words">{value}</span>
          </span>
        );
      },
    },
    {
      key: "user_role",
      label: "User Role",
      width: "w-32",
      render: (value: any) => (
        <span className={`text-[0.96em] ${mutedCls}`}>{value ?? "-"}</span>
      ),
    },
  ], [requestId]);

  const breadcrumbs = [
    { label: "Home", href: "/" },
    { label: "Requests", href: "/requests" },
    { label: `View Logs - ${requestId}` }
  ];

  return (
    <div className="bg-white">
      <Breadcrumbs items={breadcrumbs} />

      <div className="flex-1 overflow-y-auto p-3 bg-white dark:bg-slate-950">
        {isLoading && <LoadingOverlay />}

        <div className="max-w-[1400px] mx-auto space-y-3 pb-20">
          <TitleBar
            sarId={requestId}
            projectName={allData?.projectName ?? "—"}
            solutionName={allData?.solutionName ?? "—"}
            solutionType={allData?.solutionType ?? "—"}
          />

          <section className="text-[#0F1B3D] dark:text-[#E6EAF5]">
            {/* the DataTable below draws the rest of the card frame */}
            <div className="flex flex-wrap items-center gap-[10px] px-[18px] py-[14px] bg-white dark:bg-[#121831] border border-b-0 border-[#E6E9F2] dark:border-[#232B45] rounded-t-2xl">
              {/* <div className="w-full max-w-sm space-y-1.5">
                <label className="block text-[13px] font-bold text-slate-700 dark:text-slate-200">
                  Select Log Type
                </label>
                <ReactSelect
                  isMulti
                  name="logType"
                  placeholder="Select"
                  onChange={selectedOption => filter(selectedOption)}
                  options={logTypeOptions?.map((option: any) => ({
                    value: option.key,
                    label: option.value,
                  }))}
                  styles={isDarkMode ? darkModeStyles : customStyles}
                  className="basic-multi-select"
                  classNamePrefix="select"
                />
                <span className="text-[13px] text-slate-500">
                  (Note: Date is in this format: yyyy-mm-dd)
                </span>
              </div> */}
              <span className="size-7 shrink-0 inline-flex items-center justify-center rounded-lg text-[#1E3A8A] bg-[#E8EEFF] dark:text-[#7DA2FF] dark:bg-[#1B2547]">
                <History className="size-[14px]" />
              </span>
              <h2 className="font-jakarta-sans text-[15px] font-bold text-[#1E3A8A] dark:text-[#7DA2FF]">Activity Logs</h2>
              <span className="px-[9px] py-0.5 rounded-full text-[11.5px] font-bold text-[#1E3A8A] bg-[#E8EEFF] dark:text-[#7DA2FF] dark:bg-[#1B2547]">{totalRecords}</span>
              <button
                onClick={() => {
                  const api = btoa(`/request/requestor-artifacts-export`);
                  const url = `/download?api=${api}&data=${encodeURIComponent(JSON.stringify({ requestId: requestId }))}&xlName=${btoa(`Export details - ${allData?.solutionName}`)}&contentType=${btoa(`application/zip, application/octet-stream`)}&from=3`;
                  window.open(url, '_blank', 'noopener,noreferrer');
                }
                }
                // className="inline-flex items-center gap-2 px-5 py-3 bg-kpmg-blue hover:-translate-y-px transition-all text-white font-medium text-[13px] rounded-[10px] shadow-md whitespace-nowrap cursor-pointer border-none"
                className="ml-auto inline-flex items-center gap-2 cursor-pointer px-[14px] py-2 rounded-[10px] text-[13px] font-semibold whitespace-nowrap border border-[#1E3A8A] bg-[#1E3A8A] text-white transition-[filter] hover:brightness-110 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#3B6CF6] dark:border-[#7DA2FF] dark:bg-[#7DA2FF] dark:text-[#0B1020]">
                <Download className="size-[14px]" />
                Export Artifacts
              </button>
            </div>

            <DataTable
              columns={columns}
              data={paginatedData}
              currentPage={currentPage}
              setCurrentPage={setCurrentPage}
              pageSize={pageSize}
              setPageSize={setPageSize}
              totalPages={totalPages}
              totalRecords={totalRecords}
              isDropdownOpen={isPageDropdownOpen}
              setIsDropdownOpen={setIsPageDropdownOpen}
              dropdownRef={dropdownRef}
              setError={setTableError}
              sortColumn={sortColumn}
              sortOrder={sortOrder}
              onSort={handleSort}
            />
          </section>
        </div>
      </div>
    </div>
  );
};

export default RequestorArtifactory;
