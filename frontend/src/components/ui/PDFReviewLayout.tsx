"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api";

interface ParsedLineItem {
  timekeeper?: string;
  description?: string;
  hours?: number;
  rate?: number;
  amount?: number;
}

interface ParsedInvoice {
  invoice_number?: string;
  invoice_date?: string;
  vendor_name?: string;
  matter_number?: string;
  total_amount?: number;
  currency?: string;
  line_items?: ParsedLineItem[];
}

interface PdfMeta {
  name: string;
  sizeKb: number;
}

export function PDFReviewLayout() {
  const [pdfMeta, setPdfMeta] = useState<PdfMeta | null>(null);
  const [parsed, setParsed] = useState<ParsedInvoice | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setPdfMeta({ name: file.name, sizeKb: Math.round(file.size / 1024) });
    setParsed(null);
    setError(null);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);
      const data = await apiClient.parsePdf(formData);
      setParsed(data.parsed);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Extraction failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <label className="inline-flex cursor-pointer items-center gap-2 rounded-lg bg-brand-500 px-4 py-2 text-sm text-white hover:bg-blue-600 w-fit">
        <span>Select PDF</span>
        <input
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={handleFileChange}
        />
      </label>

      {(pdfMeta || parsed) && (
        <div className="flex gap-6 min-h-[60vh]">
          {/* Left: PDF file info panel */}
          <div className="flex-1 rounded-xl border border-gray-200 bg-gray-50 flex flex-col items-center justify-center gap-3 p-8">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-16 w-16 text-red-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1.5}
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"
              />
            </svg>
            {pdfMeta && (
              <>
                <p className="text-base font-semibold text-gray-700 break-all max-w-xs text-center">
                  {pdfMeta.name}
                </p>
                <p className="text-sm text-gray-400">{pdfMeta.sizeKb} KB</p>
              </>
            )}
          </div>

          {/* Right: Extracted data */}
          <div className="w-96 overflow-y-auto rounded-xl border border-gray-200 bg-white p-6">
            <h2 className="mb-4 text-lg font-bold">Extracted Data</h2>
            {loading && (
              <p className="text-sm text-gray-500 animate-pulse">
                Analysing with AI…
              </p>
            )}
            {error && <p className="text-sm text-red-500">{error}</p>}
            {parsed && !loading && (
              <dl className="flex flex-col gap-3 text-sm">
                {[
                  ["Invoice #", parsed.invoice_number],
                  ["Date", parsed.invoice_date],
                  ["Vendor", parsed.vendor_name],
                  ["Matter #", parsed.matter_number],
                  [
                    "Total",
                    parsed.total_amount != null
                      ? `${parsed.currency ?? ""} ${parsed.total_amount}`
                      : undefined,
                  ],
                ].map(([label, val]) =>
                  val ? (
                    <div key={String(label)}>
                      <dt className="font-semibold text-gray-500">{label}</dt>
                      <dd className="text-gray-800">{String(val)}</dd>
                    </div>
                  ) : null
                )}
                {parsed.line_items && parsed.line_items.length > 0 && (
                  <div>
                    <dt className="font-semibold text-gray-500 mb-1">
                      Line Items ({parsed.line_items.length})
                    </dt>
                    {parsed.line_items.map((li, i) => (
                      <dd
                        key={i}
                        className="mb-1 rounded bg-gray-50 px-2 py-1 text-xs"
                      >
                        {li.timekeeper && (
                          <span className="font-medium">{li.timekeeper} – </span>
                        )}
                        {li.description && <span>{li.description} </span>}
                        {li.amount != null && (
                          <span className="float-right font-semibold">
                            ${li.amount}
                          </span>
                        )}
                      </dd>
                    ))}
                  </div>
                )}
              </dl>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
