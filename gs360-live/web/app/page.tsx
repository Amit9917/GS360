"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import ChatView from "@/components/ChatView";
import QuizView from "@/components/QuizView";
import KnowledgeView from "@/components/KnowledgeView";
import DashboardView from "@/components/DashboardView";
import PacksView from "@/components/PacksView";
import LoginGate from "@/components/LoginGate";
import { onAuthExpired, restoreToken } from "@/lib/api";

type View = "chat" | "quiz" | "knowledge" | "dashboard" | "packs" | "solve" | "research" | "guide";

export default function Home() {
  const [view, setView] = useState<View>("dashboard");
  const [authed, setAuthed] = useState(false);

  useEffect(() => {
    setAuthed(restoreToken());
    return onAuthExpired(() => setAuthed(false));
  }, []);

  if (!authed) {
    return <LoginGate onLogin={() => setAuthed(true)} />;
  }

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar active={view} onNavigate={(v) => setView(v as View)} />
      <main className="flex-1 overflow-y-auto">
        {view === "dashboard" && <DashboardView />}
        {view === "chat" && <ChatView capability="chat" />}
        {view === "solve" && <ChatView capability="deep_solve" />}
        {view === "research" && <ChatView capability="deep_research" />}
        {view === "guide" && <ChatView capability="chat" />}
        {view === "quiz" && <QuizView />}
        {view === "knowledge" && <KnowledgeView />}
        {view === "packs" && <PacksView />}
      </main>
    </div>
  );
}
