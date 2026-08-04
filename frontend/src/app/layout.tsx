import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LexSpend",
  description: "AI-powered legal invoice tracking and spend management",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        {children}
      </body>
    </html>
  );
}
