import { ArrowDown, ArrowUp, ArrowUpDown, ChevronLeft, ChevronRight, ChevronDown, MoveRight } from "lucide-react";
import React, { RefObject, useState, useEffect } from "react";

interface Column {
    key: string;
    label?: string;
    subkey?: string;
    duplicate?: boolean;
    sortable?: boolean;
    width?: string; 
    render?: (value: any, rowData: any) => React.ReactNode;
    labelRender?: () => React.ReactNode;
}

interface DataTableProps {
    columns: Column[];
    data: any[];
    currentPage: number;
    setCurrentPage: (page: number) => void;
    pageSize: number;
    setPageSize: (size: number) => void;
    totalPages: number;
    totalRecords: number;
    isDropdownOpen: boolean;
    setIsDropdownOpen: (open: boolean) => void;
    dropdownRef: RefObject<HTMLDivElement | null>;
    setError: (error: string) => void;
    hidePagination?: boolean;
    sortColumn?: string;
    sortOrder?: "asc" | "desc";
    onSort?: (column: string) => void;
}

function getNestedValue(obj: any, path: string): any {
    if (!obj || !path) return "-";
    return path.split('.').reduce((acc, part) => acc?.[part], obj);
}

export default function DataTable({
    columns = [],
    data = [],
    currentPage,
    setCurrentPage,
    pageSize,
    setPageSize,
    totalPages,
    totalRecords,
    isDropdownOpen,
    setIsDropdownOpen,
    dropdownRef,
    setError,
    hidePagination,
    sortColumn,
    sortOrder,
    onSort,
}: DataTableProps) {
    const pageSizes = [5, 10, 20, 25, 50, 100];
    const [typedPage, setTypedPage] = useState(currentPage);

    useEffect(() => {
        setTypedPage(currentPage);
    }, [currentPage]);

    const getColumnKey = (col: Column, index: number) => {
        if (col.duplicate && col.subkey) return `${col.key}-${col.subkey}`;
        return `${col.key}-${index}`;
    };

    const handleGoToPage = () => {
        const pageNumber = Number(typedPage);
        if (pageNumber >= 1 && pageNumber <= totalPages) {
            setCurrentPage(pageNumber);
        } else {
            setError(`Page must be between 1 and ${totalPages}`);
            setTypedPage(currentPage);
        }
    };

    if (!Array.isArray(data)) {
        return <div className="p-4 text-center text-red-500">Error: Invalid data format</div>;
    }

    return (
        <div className="flex flex-col flex-1 bg-white dark:bg-[#121831] border border-[#E6E9F2] dark:border-[#232B45] shadow-sm overflow-hidden rounded-b-2xl">
            <div className="overflow-x-auto">
                <table className="w-full table-fixed border-collapse">
                    <colgroup>
                        {columns.map((col, index) => (
                            <col
                                key={getColumnKey(col, index)}
                                className={col.width ?? "w-40"}
                            />
                        ))}
                    </colgroup>
                    <thead className="sticky top-0 z-[100] px-3 left-0 shadow-[8px_0_10px_-8px_rgba(15,27,61,0.25)] py-3.5 text-start whitespace-nowrap font-['Plus_Jakarta_Sans',sans-serif] font-semibold tracking-normal capitalize text-[#1e3a8a] dark:text-[#c9d7ff] text-[12.5px] 2xl:text-base bg-[linear-gradient(180deg,#f5f8ff_0%,#eaf0fc_100%)] dark:bg-[linear-gradient(180deg,#1c2646_0%,#172039_100%)] border-b border-[#d5dff3] dark:border-[#2b3760] cursor-pointer hover:brightness-[0.98] dark:hover:brightness-110">
                        <tr>
                            {columns.map((col, index) => (
                                <th
                                    key={getColumnKey(col, index)}
                                    className={`px-[14px] py-[11px] text-left font-semibold tracking-normal text-[#1E3A8A] dark:text-[#C9D7FF] text-[12.5px] 2xl:text-xl ${col.sortable ? 'cursor-pointer hover:bg-blue-100/50 dark:hover:bg-slate-700' : ''}`}
                                    onClick={() => col.sortable && onSort && onSort(col.key)}
                                >
                                    <div className="flex items-center gap-1.5">
                                        {col.labelRender ? col.labelRender() : col.label}
                                        {col.sortable && (
                                            <span className="shrink-0">
                                                {sortColumn === col.key ? (
                                                    sortOrder === 'asc'
                                                        ? <ArrowUp className="w-3 h-3 opacity-80" />
                                                        : <ArrowDown className="w-3 h-3 opacity-80" />
                                                ) : (
                                                    <ArrowUpDown className="w-3 h-3 opacity-40" />
                                                )}
                                            </span>
                                        )}
                                    </div>
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-[#E6E9F2] dark:divide-[#232B45]">
                        {data.length === 0 ? (
                            <tr>
                                <td
                                    colSpan={columns.length}
                                    className="px-[14px] py-10 text-center text-sm text-[#8A94AD] dark:text-[#6F7A96]"
                                >
                                    No data found
                                </td>
                            </tr>
                        ) : (
                            data.map((row, rowIndex) => (
                                <tr
                                    key={rowIndex}
                                    className="transition-colors hover:bg-[#F3F5FB] dark:hover:bg-[#182040]"
                                >
                                    {columns.map((col, colIndex) => (
                                        <td
                                            key={`${rowIndex}-${getColumnKey(col, colIndex)}`}
                                            className="px-[14px] py-[12px] align-top text-[13px] 2xl:text-xl leading-normal text-left text-[#0F1B3D] dark:text-[#E6EAF5] break-words overflow-hidden"
                                        >
                                            {col.render
                                                ? col.render(getNestedValue(row, col.key), row)
                                                : (getNestedValue(row, col.key) ?? "-")}
                                        </td>
                                    ))}
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {!hidePagination && (
                <div className="flex flex-col md:flex-row items-center justify-between px-6 py-4 border-t border-[#E6E9F2] dark:border-[#232B45] gap-3">
                    <div className="flex items-center order-2 md:order-1">
                        <span className="font-semibold text-slate-700 dark:text-slate-200 whitespace-nowrap text-[11px] mr-1">Total Records:</span>
                        <span className="text-[11px] font-semibold text-slate-900 dark:text-white">{totalRecords}</span>
                    </div>

                    <div className="flex items-center gap-4 order-1 md:order-2">
                        <div className="flex items-center space-x-2 border-r border-gray-100 dark:border-slate-700 pr-4 h-6">
                            <span className="font-semibold text-slate-700 dark:text-slate-200 whitespace-nowrap text-[11px] tracking-wide">Show</span>
                            <div className="relative" ref={dropdownRef}>
                                <button
                                    onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                                    className="h-7 flex items-center gap-1 text-[11px] border border-gray-200 dark:border-slate-600 rounded-md bg-white dark:bg-slate-700 text-slate-700 dark:text-white px-2 cursor-pointer"
                                >
                                    {pageSize} <ChevronDown className="w-3 h-3" />
                                </button>
                                {isDropdownOpen && (
                                    <div className="absolute bottom-full left-0 mb-1 w-full min-w-[50px] bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded shadow-lg z-50">
                                        {pageSizes.map((size) => (
                                            <button
                                                key={size}
                                                className="w-full px-2 py-1.5 text-[11px] text-left hover:bg-blue-50 dark:hover:bg-slate-700 cursor-pointer"
                                                onClick={() => { setPageSize(size); setCurrentPage(1); setIsDropdownOpen(false); }}
                                            >
                                                {size}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>

                            <div className="flex items-center space-x-2 border-l border-gray-100 dark:border-slate-700 pl-4 h-6">
                                <span className="font-semibold text-slate-700 dark:text-slate-200 whitespace-nowrap text-[11px] tracking-wide">Go To:</span>
                                <input
                                    type="number"
                                    min="1"
                                    max={totalPages}
                                    value={typedPage}
                                    onChange={(e) => setTypedPage(Number(e.target.value))}
                                    onKeyDown={(e) => e.key === 'Enter' && handleGoToPage()}
                                    className="w-10 h-7 text-center text-[11px] border border-gray-200 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-700 dark:text-white focus:outline-none focus:border-blue-500"
                                />
                                <button
                                    onClick={handleGoToPage}
                                    className="h-7 w-7 flex items-center justify-center border border-gray-200 dark:border-slate-600 text-slate-500 rounded-lg transition-colors cursor-pointer hover:bg-blue-50 dark:hover:bg-slate-700"
                                >
                                    <MoveRight className="w-3 h-3" />
                                </button>
                            </div>
                        </div>
                        <div className="flex items-center text-[11px] space-x-2">
                            <button
                                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                                disabled={currentPage === 1}
                                className={`w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 dark:border-slate-600 text-slate-500 transition-all disabled:opacity-40 cursor-pointer ${currentPage === 1 ? 'hidden' : ''}`}
                            >
                                <ChevronLeft className="w-3 h-3" />
                            </button>
                            <span className="font-semibold text-slate-700 dark:text-slate-200 whitespace-nowrap text-[11px] tracking-wide">
                                Page {currentPage} of {totalPages}
                            </span>
                            <button
                                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                                disabled={currentPage === totalPages}
                                className={`w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 dark:border-slate-600 text-slate-500 transition-all disabled:opacity-40 cursor-pointer ${currentPage === totalPages ? 'hidden' : ''}`}
                            >
                                <ChevronRight className="w-3 h-3" />
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
