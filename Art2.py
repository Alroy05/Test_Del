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
import { Download, History, LucideRotateCcw, RotateCcwClock, RotateCcwSquare } from "lucide-react";
import TitleBar from "@/components/TitleBar";
import Breadcrumbs from "@/components/Breadcrumbs";
import { Rotate90DegreesCcwRounded } from "@mui/icons-material";

const downloadableFileRegEx =
  /\.(doc|docx|xls|xlsx|pdf|jpg|jpeg|png|gif|webp|txt|csv|ppt|pptx|zip|rar|7z)$/i;

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
    return <>-</>;
  }

  return (
    <div>
      {items.map((item: string, index: number) => {
        const filename = item
          .replace(/\\/g, "/")
          .split("/")
          .pop() ?? item;

        const hasDownloadableExtension =
          downloadableFileRegEx.test(filename);

        if (!hasDownloadableExtension) {
          return (
            <div key={index} className="pb-2">
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
          <div key={index} className="pb-2">
            <Link
              href={downloadUrl}
              target="_blank"
              className="text-blue-600 hover:underline text-[13px] font-medium"
            >
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
        <br />
        <div className="flex items-center justify-between mt-1">
          <button
            type="button"
            onClick={() => setIsExpanded(p => !p)}
            className="text-kpmg-blue dark:text-blue-600 cursor-pointer hover:underline text-[13px] font-semibold"
          >
            {isExpanded ? "- Read Less" : "+ Read More"}
          </button>
          <button
            type="button"
            className="text-kpmg-blue  dark:text-blue-600 cursor-pointer hover:underline text-[13px] font-semibold"
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
      <div>
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
              <div key={index} className="pb-2">
                <Link
                  href={`/download?api=${api}&filename=${btoa(filename!)}&from=1`}
                  target="_blank"
                  className="text-blue-600 hover:underline text-[13px] font-medium"
                >
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
      width: "w-45",

      render: (value: any) => (
        <span className="text-[13px] text-slate-700 dark:text-slate-300 whitespace-nowrap">
          {formatDateTime(value)}
        </span>
      ),

    },
    {
      key: "created_by_name",
      label: "Name",
      width: "w-36",
      render: (value: any) => (
        <span className="font-bold text-slate-700 dark:text-slate-200">{value ?? "-"}</span>
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
      width: "w-[420px]",
      render: (_: any, row: any) => <UpdateCell row={row} requestId={requestId} />,
    },
    {
      key: "old_value_str",
      label: "Old Data",
      width: "w-48",
      render: (value: any, row: any) =>
        row.event == 10 ? (
          <Event10Value
            value={row.old_value ?? value}
            requestId={requestId}
          />
        ) : (
          <div
            dangerouslySetInnerHTML={{
              __html: DOMPurify.sanitize(value ?? ""),
            }}
          />
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
      width: "w-32",
      render: (value: any) => {
        const colorMap: Record<string, string> = {
          Artifacts: "text-sky-700 dark:text-sky-400",
          Comment: "text-green-700 dark:text-green-400",
          Status: "text-pink-700 dark:text-pink-400",
        };
        return (
          <span className={`font-medium text-[13px] ${colorMap[value] ?? "text-slate-500"}`}>
            {value ?? "-"}
          </span>
        );
      },
    },
    {
      key: "user_role",
      label: "User Role",
      width: "w-40",
      render: (value: any) => (
        <>{value ?? "-"}</>
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

        <div className="max-w-[1400px] mx-auto space-y-4 pb-20">
          <TitleBar
            sarId={requestId}
            projectName={allData?.projectName ?? "—"}
            solutionName={allData?.solutionName ?? "—"}
            solutionType={allData?.solutionType ?? "—"}
          />

          <div className="bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-800 rounded-2xl">
            <div className="flex items-center justify-between gap-6 py-4 px-6">
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
              <div className="flex items-center justify-center gap-3 text-lg font-bold text-kpmg-blue">
                <span className="px-2 py-2 flex justify-center items-center rounded-xl text-sm font-bold bg-[#E8EEFF]"><History className="size-5" /></span>Activity Logs<span className="px-3 py-1 flex justify-center items-center rounded-2xl text-sm font-bold bg-[#E8EEFF]">{totalRecords}</span>
              </div>
              <button
                onClick={() => {
                  const api = btoa(`/request/requestor-artifacts-export`);
                  const url = `/download?api=${api}&data=${encodeURIComponent(JSON.stringify({ requestId: requestId }))}&xlName=${btoa(`Export details - ${allData?.solutionName}`)}&contentType=${btoa(`application/zip, application/octet-stream`)}&from=3`;
                  window.open(url, '_blank', 'noopener,noreferrer');
                }
                }
                // className="inline-flex items-center gap-2 px-5 py-3 bg-kpmg-blue hover:-translate-y-px transition-all text-white font-medium text-[13px] rounded-[10px] shadow-md whitespace-nowrap cursor-pointer border-none"
                className="flex items-center gap-2 cursor-pointer text-white px-4 py-2.5 rounded-xl shadow-md font-semibold text-sm transition-all bg-kpmg-blue hover:-translate-y-px">
                <Download className="w-4 h-4" />
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
          </div>
        </div>
      </div>
    </div>
  );
};

export default RequestorArtifactory;
