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

export function PDFReviewLayout() {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [parsed, setParsed] = useState<ParsedInvoice | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setPdfUrl(URL.createObjectURL(file));
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

      {(pdfUrl || parsed) && (
        <div className="flex gap-6 h-[70vh]">
          {/* Left: PDF viewer */}
          <div className="flex-1 rounded-xl border border-gray-200 overflow-hidden">
            {pdfUrl ? (
              <iframe
                src={pdfUrl}
                className="w-full h-full"
                title="Invoice PDF"
              />
            ) : (
              <div className="flex h-full items-center justify-center text-gray-400">
                No PDF loaded
              </div>
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
                  ["Total", parsed.total_amount != null ? `${parsed.currency ?? ""} ${parsed.total_amount}` : undefined],
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
                        {li.timekeeper && <span className="font-medium">{li.timekeeper} – </span>}
                        {li.description && <span>{li.description} </span>}
                        {li.amount != null && <span className="float-right font-semibold">${li.amount}</span>}
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
