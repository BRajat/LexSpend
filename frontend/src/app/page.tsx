import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 p-8">
      <h1 className="text-4xl font-bold text-brand-900">LexSpend</h1>
      <p className="text-lg text-gray-600">
        AI-powered legal invoice tracking &amp; spend management
      </p>
      <div className="flex gap-4">
        <Link
          href="/login"
          className="rounded-lg bg-brand-500 px-6 py-3 text-white hover:bg-blue-600"
        >
          Sign in
        </Link>
        <Link
          href="/dashboard/matters"
          className="rounded-lg border border-gray-300 px-6 py-3 hover:bg-gray-100"
        >
          Dashboard
        </Link>
      </div>
    </main>
  );
}
