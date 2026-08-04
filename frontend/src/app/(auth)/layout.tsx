import type { Metadata } from "next";

export const metadata: Metadata = { title: "Sign In – LexSpend" };

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-brand-50">
      {children}
    </div>
  );
}
