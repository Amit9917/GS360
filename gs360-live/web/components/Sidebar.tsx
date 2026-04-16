"use client";

import { logout } from "@/lib/api";

const NAV_ITEMS = [
  { id: "dashboard", label: "Dashboard", icon: "📊" },
  { id: "chat", label: "UPSC Chat", icon: "💬" },
  { id: "solve", label: "Deep Solve", icon: "🧠" },
  { id: "quiz", label: "Quiz Arena", icon: "🧩" },
  { id: "research", label: "Deep Research", icon: "🔬" },
  { id: "guide", label: "Guided Learning", icon: "🎓" },
  { id: "knowledge", label: "Knowledge Base", icon: "📚" },
  { id: "packs", label: "Content Packs", icon: "📦" },
];

const SUBJECTS = [
  { name: "Polity", color: "bg-upsc-polity" },
  { name: "History", color: "bg-upsc-history" },
  { name: "Geography", color: "bg-upsc-geography" },
  { name: "Economy", color: "bg-upsc-economy" },
  { name: "Science", color: "bg-upsc-science" },
  { name: "Ethics", color: "bg-upsc-ethics" },
  { name: "Current", color: "bg-upsc-current" },
  { name: "Environment", color: "bg-upsc-environment" },
];

interface SidebarProps {
  active: string;
  onNavigate: (view: string) => void;
}

export default function Sidebar({ active, onNavigate }: SidebarProps) {
  return (
    <aside className="w-64 h-screen bg-primary-900 text-white flex flex-col border-r border-primary-700/50">
      {/* Logo */}
      <div className="p-5 border-b border-primary-700/50">
        <h1 className="text-2xl font-bold tracking-tight">GS360</h1>
        <p className="text-xs text-blue-300/70 mt-0.5">UPSC AI Tutor · DeepTutor Engine</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-3">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            onClick={() => onNavigate(item.id)}
            className={`w-full flex items-center gap-3 px-5 py-2.5 text-sm transition-colors ${
              active === item.id
                ? "bg-blue-500/20 text-blue-300 border-r-2 border-blue-400"
                : "text-white/70 hover:bg-white/5 hover:text-white"
            }`}
          >
            <span className="text-base">{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>

      {/* Subject Tags */}
      <div className="p-4 border-t border-primary-700/50">
        <p className="text-xs text-white/40 mb-2 uppercase tracking-wider">Subjects</p>
        <div className="flex flex-wrap gap-1.5">
          {SUBJECTS.map((s) => (
            <span
              key={s.name}
              className={`${s.color} text-white text-[10px] px-2 py-0.5 rounded-full`}
            >
              {s.name}
            </span>
          ))}
        </div>
      </div>

      {/* Logout */}
      <div className="p-4 border-t border-primary-700/50">
        <button
          onClick={() => {
            logout();
            window.location.reload();
          }}
          className="w-full text-sm text-white/50 hover:text-white py-2 rounded-lg hover:bg-white/5 transition"
        >
          Sign Out
        </button>
      </div>
    </aside>
  );
}
