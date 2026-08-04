const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      ...(options.headers ?? {}),
    },
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`API error ${res.status}: ${detail}`);
  }

  return res.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Typed API methods
// ---------------------------------------------------------------------------

interface ParsedLineItem {
  timekeeper?: string;
  description?: string;
  hours?: number;
  rate?: number;
  amount?: number;
  task_code?: string;
  activity_code?: string;
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

interface ParsePDFResponse {
  parsed: ParsedInvoice;
  raw_text_preview: string;
}

export const apiClient = {
  /** Upload a PDF and receive AI-extracted structured invoice data. */
  parsePdf(formData: FormData): Promise<ParsePDFResponse> {
    return request<ParsePDFResponse>("/invoices/parse-pdf", {
      method: "POST",
      body: formData,
    });
  },
};
