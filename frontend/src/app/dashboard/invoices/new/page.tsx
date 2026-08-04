import type { Metadata } from "next";
import { PDFReviewLayout } from "@/components/ui/PDFReviewLayout";

export const metadata: Metadata = { title: "New Invoice – LexSpend" };

export default function NewInvoicePage() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">Upload &amp; Review Invoice</h1>
      <PDFReviewLayout />
    </div>
  );
}
