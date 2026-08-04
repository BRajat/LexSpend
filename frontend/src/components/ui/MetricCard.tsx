"use client";

interface MetricCardProps {
  title: string;
  value: string;
  delta?: string;
  positive?: boolean;
}

export function MetricCard({ title, value, delta, positive }: MetricCardProps) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
        {title}
      </p>
      <p className="mt-2 text-3xl font-bold text-brand-900">{value}</p>
      {delta && (
        <p
          className={`mt-1 text-sm font-medium ${
            positive ? "text-green-600" : "text-red-500"
          }`}
        >
          {delta}
        </p>
      )}
    </div>
  );
}
