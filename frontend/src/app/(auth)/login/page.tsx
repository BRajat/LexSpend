import type { Metadata } from "next";

export const metadata: Metadata = { title: "Sign In – LexSpend" };

export default function LoginPage() {
  return (
    <div className="w-full max-w-md rounded-2xl bg-white p-10 shadow-lg">
      <h1 className="mb-6 text-2xl font-bold text-brand-900">Sign in to LexSpend</h1>
      <form className="flex flex-col gap-4" action="#" method="POST">
        <div>
          <label htmlFor="email" className="mb-1 block text-sm font-medium">
            Email
          </label>
          <input
            id="email"
            name="email"
            type="email"
            required
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
          />
        </div>
        <div>
          <label htmlFor="password" className="mb-1 block text-sm font-medium">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            required
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
          />
        </div>
        <button
          type="submit"
          className="mt-2 rounded-lg bg-brand-500 py-2 text-white font-semibold hover:bg-blue-600"
        >
          Sign in
        </button>
      </form>
    </div>
  );
}
