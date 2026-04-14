import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "GS360 — UPSC AI Tutor",
  description:
    "Open-source UPSC preparation platform powered by DeepTutor — RAG-powered chat, quiz generation, deep solve, and guided learning.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
