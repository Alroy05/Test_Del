'use client';

import React, { useEffect, useState, useRef, useMemo } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import ReactSelect, { components } from "react-select";
import DOMPurify from 'dompurify';
import DataTable from "@/components/DataTable";
import LoadingOverlay from "@/components/LoadingOverlay";
import { callBackend, callBackendFormData, forceDownload, downloadFile, downloadPdfFile, formatDateTime, actionBtn } from "@/lib/helpers";
import { customStyles, darkModeStyles } from "@/lib/styles";
import { toast } from "react-hot-toast";
import { ArrowLeftRight, Calendar, Check, ChevronDown, ChevronUp, ClipboardList, Download, FileText, Filter, GitBranch, History, ListChecks, LucideRotateCcw, Mail, MessageSquare, RefreshCw, Reply, RotateCcw, RotateCcwClock, RotateCcwSquare, ShieldAlert, ShieldCheck, Signal, Sparkles, Tag } from "lucide-react";
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

/* Links inside HTML that comes from the API (email bodies etc.) */
const htmlCls = "[&_a]:underline [&_a]:[overflow-wrap:anywhere] [&_a]:text-[#1E3A8A] dark:[&_a]:text-[#7DA2FF]";

/* The API sends null, "" or "-" when there is nothing to show */
const isBlank = (value: any) => value == null || value === "" || value === "-";

/* Internal keys such as "request_sub_status" read as "Request sub status" */
const formatResponseFor = (value: any) =>
  typeof value === "string" && /^[a-z0-9]+(_[a-z0-9]+)+$/.test(value)
    ? value.charAt(0).toUpperCase() + value.slice(1).replace(/_/g, " ")
    : value;

/* Log type pills. Keys are the event names from logEventList, in lower case. */
const TONES = {
  blue: "text-[#2563EB] bg-[#2563EB]/11 dark:text-[#8DB0FF] dark:bg-[#8DB0FF]/14",
  violet: "text-[#7C3AED] bg-[#7C3AED]/11 dark:text-[#A78BFA] dark:bg-[#A78BFA]/14",
  cyan: "text-[#0E7490] bg-[#0E7490]/11 dark:text-[#22D3EE] dark:bg-[#22D3EE]/14",
  amber: "text-[#B45309] bg-[#B45309]/11 dark:text-[#FBBF24] dark:bg-[#FBBF24]/14",
  green: "text-[#047857] bg-[#047857]/11 dark:text-[#34D399] dark:bg-[#34D399]/14",
  pink: "text-[#BE185D] bg-[#BE185D]/11 dark:text-[#F472B6] dark:bg-[#F472B6]/14",
  indigo: "text-[#4338CA] bg-[#4338CA]/11 dark:text-[#A5B4FC] dark:bg-[#A5B4FC]/14",
  teal: "text-[#0F766E] bg-[#0F766E]/11 dark:text-[#2DD4BF] dark:bg-[#2DD4BF]/14",
  red: "text-[#DC2626] bg-[#DC2626]/11 dark:text-[#F87171] dark:bg-[#F87171]/14",
  orange: "text-[#C2410C] bg-[#C2410C]/11 dark:text-[#FB923C] dark:bg-[#FB923C]/14",
  sky: "text-[#0369A1] bg-[#0369A1]/11 dark:text-[#38BDF8] dark:bg-[#38BDF8]/14",
  slate: "text-[#475569] bg-[#475569]/11 dark:text-[#A3AEC8] dark:bg-[#A3AEC8]/14",
};
const TYPE_PILLS: Record<string, [React.ElementType, string]> = {
  "status": [Signal, TONES.blue],
  "comment": [MessageSquare, TONES.cyan],
  "coordinator comments": [MessageSquare, TONES.cyan],
  "security resource comments": [MessageSquare, TONES.cyan],
  "artifacts": [FileText, TONES.slate],
  "email": [Mail, TONES.amber],
  "intake form data": [ClipboardList, TONES.indigo],
  "date change": [Calendar, TONES.sky],
  "response provided": [Reply, TONES.green],
  "checklist update": [ListChecks, TONES.teal],
  "ai": [Sparkles, TONES.violet],
  "ato status event": [ShieldCheck, TONES.pink],
  "findings": [ShieldAlert, TONES.red],
  "ado": [GitBranch, TONES.sky],
  "reset intake": [RotateCcw, TONES.orange],
  "reset review": [RotateCcw, TONES.orange],
  "change solution type": [ArrowLeftRight, TONES.indigo],
  "re-initiate assessment": [RefreshCw, TONES.orange],
};
const DEFAULT_TYPE_PILL: [React.ElementType, string] = [Tag, TONES.slate];

/* Long labels are split into two lines of similar length so the pill hugs its text */
const splitLabel = (label: string): string[] => {
  if (label.length <= 17) return [label];
  const middle = label.length / 2;
  let cut = -1;
  for (let i = label.indexOf(" "); i !== -1; i = label.indexOf(" ", i + 1)) {
    if (cut === -1 || Math.abs(i - middle) < Math.abs(cut - middle)) cut = i;
  }
  return cut === -1 ? [label] : [label.slice(0, cut), label.slice(cut + 1)];
};

const TypePill = ({ value }: { value: any }) => {
  if (isBlank(value)) return <span className={faintCls}>-</span>;
  const label = String(value).trim();
  const [Icon, tone] = TYPE_PILLS[label.toLowerCase()] ?? DEFAULT_TYPE_PILL;

  return (
    <span className={`inline-flex items-start gap-1.5 max-w-full px-[9px] py-[3px] rounded-[1.1em] text-[0.885em] leading-snug font-semibold ${tone}`}>
      <Icon className="size-[0.95em] shrink-0 mt-[0.2em]" />
      <span className="min-w-0 break-words">
        {splitLabel(label).map((line, index) => (
          <span key={index} className="block">{line}</span>
        ))}
      </span>
    </span>
  );
};

/* Log type filter: react-select styled as the design's pill dropdown */
/* Breakpoints for the select: Tailwind's sm, and the large-monitor size used across this page.
   Laptops (below 1920px wide) keep the standard sizes. */
const FROM_SM = "@media (min-width: 640px)";
const FROM_LARGE = "@media (min-width: 1920px)";

const logTypeSelectStyles = (dark: boolean): any => {
  const c = dark
    ? { surface: "#121831", hover: "#182040", border: "#232B45", text: "#E6EAF5", faint: "#6F7A96", brand: "#7DA2FF", soft: "#1B2547" }
    : { surface: "#FFFFFF", hover: "#F3F5FB", border: "#E6E9F2", text: "#0F1B3D", faint: "#8A94AD", brand: "#1E3A8A", soft: "#E8EEFF" };
  const indicator = {
    color: c.faint, cursor: "pointer", "&:hover": { color: c.text },
    svg: { width: 14, height: 14 }, [FROM_LARGE]: { svg: { width: 18, height: 18 } },
  };

  return {
    container: (base: any) => ({ ...base, flex: 1, minWidth: 0 }),
    control: (base: any) => ({
      ...base, width: "100%", height: 34, minHeight: 34, flexWrap: "nowrap", cursor: "pointer",
      border: 0, borderRadius: 999, boxShadow: "none", background: "transparent", fontSize: 13, fontWeight: 600,
      [FROM_SM]: { width: 200 },
      [FROM_LARGE]: { width: 260, height: 42, minHeight: 42, fontSize: 17 },
    }),
    valueContainer: (base: any) => ({ ...base, flexWrap: "nowrap", padding: "0 4px 0 8px" }),
    placeholder: (base: any) => ({
      ...base, margin: 0, color: c.text, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
    }),
    input: (base: any) => ({ ...base, margin: 0, padding: 0, color: c.text }),
    indicatorSeparator: () => ({ display: "none" }),
    clearIndicator: (base: any) => ({ ...base, ...indicator, padding: "0 2px" }),
    dropdownIndicator: (base: any, state: any) => ({
      ...base, ...indicator, padding: "0 12px 0 4px", transition: "transform 0.2s ease",
      transform: state.selectProps.menuIsOpen ? "rotate(180deg)" : undefined,
    }),
    menu: (base: any) => ({
      ...base, left: "auto", right: 0, width: "max-content", minWidth: "100%", marginTop: 8, padding: 5, zIndex: 200,
      background: c.surface, border: `1px solid ${c.border}`, borderRadius: 12,
      boxShadow: "0 18px 40px -16px rgba(15, 27, 61, 0.45)",
    }),
    menuList: (base: any) => ({ ...base, padding: 0, maxHeight: 280, [FROM_LARGE]: { maxHeight: 420 } }),
    option: (base: any, state: any) => ({
      ...base, display: "flex", alignItems: "center", gap: 10, padding: "8px 10px", borderRadius: 8,
      fontSize: 13, cursor: "pointer", fontWeight: state.isSelected ? 600 : 500,
      [FROM_LARGE]: { fontSize: 17, padding: "10px 12px" },
      color: state.isSelected ? c.brand : c.text,
      background: state.isSelected ? c.soft : state.isFocused ? c.hover : "transparent",
      "&:active": { background: state.isSelected ? c.soft : c.hover },
    }),
    noOptionsMessage: (base: any) => ({ ...base, fontSize: 13, color: c.faint, [FROM_LARGE]: { fontSize: 17 } }),
  };
};

const LogTypeControl = ({ children, ...props }: any) => (
  <components.Control {...props}>
    <Filter className="ml-3 size-3 min-[1920px]:size-4 shrink-0 text-[#1E3A8A] dark:text-[#7DA2FF]" />
    {children}
  </components.Control>
);

const LogTypeOption = ({ children, ...props }: any) => (
  <components.Option {...props}>
    <span className="flex-1 min-w-0">{children}</span>
    {props.isSelected && <Check className="size-3 min-[1920px]:size-4 shrink-0" />}
  </components.Option>
);

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
          <div className={htmlCls} dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(extra) }} />
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

  return <div className={htmlCls} dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(row.new_value_str) }} />;
};

const RequestorArtifactory = () => {
  const params = useParams();
  const requestId = params?.id as string;

  const objectToArray = (dropdown: any) =>
    Object.entries(dropdown).map(([key, value]) => ({ key, value }));

  const [logTypeOptions, setLogTypeOptions] = useState<any>();
  const [selectedLogTypes, setSelectedLogTypes] = useState<any[]>([]);
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
      width: "w-34",
      render: (value: any) =>
        isBlank(value) ? <span className={faintCls}>-</span> : <span className="font-semibold">{value}</span>,
    },
    {
      key: "response_for",
      label: "Response For",
      width: "w-40",
      render: (value: any) =>
        isBlank(value) ? <span className={faintCls}>-</span> : <>{formatResponseFor(value)}</>,
    },
    {
      key: "new_value_str",
      label: "Update",
      width: "w-96",
      render: (_: any, row: any) => <UpdateCell row={row} requestId={requestId} />,
    },
    {
      key: "old_value_str",
      label: "Old Data",
      width: "w-38",
      render: (value: any, row: any) =>
        row.event == 10 ? (
          <div className={mutedCls}>
            <Event10Value
              value={row.old_value ?? value}
              requestId={requestId}
            />
          </div>
        ) : !isBlank(value) ? (
          <div
            className={`${mutedCls} ${htmlCls}`}
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
      width: "w-46",
      render: (value: any) => <TypePill value={value} />,
    },
    {
      key: "user_role",
      label: "User Role",
      width: "w-32",
      render: (value: any) => (
        <span className={`text-[0.96em] ${isBlank(value) ? faintCls : mutedCls}`}>{isBlank(value) ? "-" : value}</span>
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

        <div className="max-w-[1400px] min-[1920px]:max-w-none mx-auto space-y-3 pb-20">
          <TitleBar
            sarId={requestId}
            projectName={allData?.projectName ?? "—"}
            solutionName={allData?.solutionName ?? "—"}
            solutionType={allData?.solutionType ?? "—"}
          />

          <section className="text-[#0F1B3D] dark:text-[#E6EAF5]">
            {/* the DataTable below draws the rest of the card frame */}
            <div className="flex flex-wrap items-center gap-[10px] min-[1920px]:gap-3.5 px-[18px] py-[14px] min-[1920px]:px-6 min-[1920px]:py-[18px] bg-white dark:bg-[#121831] border border-b-0 border-[#E6E9F2] dark:border-[#232B45] rounded-t-2xl">
              <span className="size-7 min-[1920px]:size-10 shrink-0 inline-flex items-center justify-center rounded-lg min-[1920px]:rounded-[10px] text-[#1E3A8A] bg-[#E8EEFF] dark:text-[#7DA2FF] dark:bg-[#1B2547]">
                <History className="size-[14px] min-[1920px]:size-5" />
              </span>
              <h2 className="font-jakarta-sans text-[15px] min-[1920px]:text-[22px] font-bold text-[#1E3A8A] dark:text-[#7DA2FF]">Activity Logs</h2>
              <span className="px-[9px] py-0.5 min-[1920px]:px-3 min-[1920px]:py-1 rounded-full text-[11.5px] min-[1920px]:text-[15px] font-bold text-[#1E3A8A] bg-[#E8EEFF] dark:text-[#7DA2FF] dark:bg-[#1B2547]">{totalRecords}</span>
              <div className="w-full sm:w-auto sm:ml-auto flex items-center gap-2 min-[1920px]:gap-3">
                <div className="flex flex-1 sm:flex-none min-w-0 items-center h-[38px] min-[1920px]:h-[46px] rounded-full border-[1.5px] border-transparent transition-shadow [background:linear-gradient(#fff,#fff)_padding-box,linear-gradient(90deg,#3B6CF6_0%,#8B5CF6_50%,#EC4899_100%)_border-box] dark:[background:linear-gradient(#121831,#121831)_padding-box,linear-gradient(90deg,#6B93FF_0%,#A78BFA_50%,#F472B6_100%)_border-box] shadow-[0_8px_22px_-14px_rgba(139,92,246,0.28)] focus-within:shadow-[0_0_0_4px_rgba(139,92,246,0.16),0_10px_28px_-12px_rgba(139,92,246,0.28)]">
                  <ReactSelect
                    isMulti
                    name="logType"
                    instanceId="log-type"
                    aria-label="Log type"
                    placeholder={
                      !selectedLogTypes.length
                        ? "All log types"
                        : selectedLogTypes.length === 1
                          ? selectedLogTypes[0].label
                          : `${selectedLogTypes.length} log types`
                    }
                    value={selectedLogTypes}
                    onChange={(selectedOption: any) => {
                      setSelectedLogTypes(selectedOption ?? []);
                      filter(selectedOption);
                    }}
                    options={logTypeOptions?.map((option: any) => ({
                      value: option.key,
                      label: option.value,
                    }))}
                    controlShouldRenderValue={false}
                    hideSelectedOptions={false}
                    styles={logTypeSelectStyles(isDarkMode)}
                    components={{ Control: LogTypeControl, Option: LogTypeOption }}
                  />
                </div>
                <button
                  onClick={() => {
                    const api = btoa(`/request/requestor-artifacts-export`);
                    const url = `/download?api=${api}&data=${encodeURIComponent(JSON.stringify({ requestId: requestId }))}&xlName=${btoa(`Export details - ${allData?.solutionName}`)}&contentType=${btoa(`application/zip, application/octet-stream`)}&from=3`;
                    window.open(url, '_blank', 'noopener,noreferrer');
                  }
                  }
                  // className="inline-flex items-center gap-2 px-5 py-3 bg-kpmg-blue hover:-translate-y-px transition-all text-white font-medium text-[13px] rounded-[10px] shadow-md whitespace-nowrap cursor-pointer border-none"
                  className="inline-flex shrink-0 items-center gap-2 cursor-pointer px-[14px] py-2 min-[1920px]:px-5 min-[1920px]:py-[11px] rounded-[10px] min-[1920px]:rounded-xl text-[13px] min-[1920px]:text-[17px] font-semibold whitespace-nowrap border border-[#1E3A8A] bg-[#1E3A8A] text-white transition-[filter] hover:brightness-110 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#3B6CF6] dark:border-[#7DA2FF] dark:bg-[#7DA2FF] dark:text-[#0B1020]">
                  <Download className="size-[14px] min-[1920px]:size-[18px]" />
                  Export Artifacts
                </button>
              </div>
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
              stickyHeader
            />
          </section>
        </div>
      </div>
    </div>
  );
};

export default RequestorArtifactory;
