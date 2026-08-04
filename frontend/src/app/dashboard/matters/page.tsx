import type { Metadata } from "next";
import { DataTable } from "@/components/ui/DataTable";

export const metadata: Metadata = { title: "Matters – LexSpend" };

const COLUMNS = [
  { key: "matter_number", label: "Matter #" },
  { key: "description", label: "Description" },
  { key: "budget", label: "Budget" },
  { key: "is_open", label: "Status" },
];

// In a real app these would be fetched server-side.
const PLACEHOLDER_ROWS = [
  { id: "1", matter_number: "2024-001", description: "Johnson v. Acme Corp", budget: "$120,000", is_open: "Open" },
  { id: "2", matter_number: "2024-002", description: "IP Portfolio Review", budget: "$45,000", is_open: "Open" },
  { id: "3", matter_number: "2023-099", description: "Employment Dispute", budget: "$60,000", is_open: "Closed" },
];

export default function MattersPage() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">Matters</h1>
      <DataTable columns={COLUMNS} rows={PLACEHOLDER_ROWS} />
    </div>
  );
}
