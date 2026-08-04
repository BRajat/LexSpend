import Link from "next/link";

const navItems = [
  { href: "/dashboard/matters", label: "Matters" },
  { href: "/dashboard/invoices/new", label: "New Invoice" },
  { href: "/dashboard/analytics", label: "Analytics" },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen">
      <aside className="w-56 bg-brand-900 text-white flex flex-col py-8 px-4 gap-2">
        <span className="mb-6 text-xl font-bold tracking-tight">LexSpend</span>
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="rounded-lg px-3 py-2 text-sm hover:bg-blue-800"
          >
            {item.label}
          </Link>
        ))}
      </aside>
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
}
