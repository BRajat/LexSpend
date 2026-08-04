import type { Metadata } from "next";
import { MetricCard } from "@/components/ui/MetricCard";

export const metadata: Metadata = { title: "Analytics – LexSpend" };

const METRICS = [
  { title: "Total Spend YTD", value: "$1,245,600", delta: "+4.2%", positive: false },
  { title: "Open Invoices", value: "38", delta: "-3 this week", positive: true },
  { title: "Matters Active", value: "14", delta: "+2 this month", positive: true },
  { title: "Avg Invoice Cycle", value: "6.3 days", delta: "-1.1 days", positive: true },
];

export default function AnalyticsPage() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">Analytics</h1>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {METRICS.map((m) => (
          <MetricCard key={m.title} {...m} />
        ))}
      </div>
    </div>
  );
}
