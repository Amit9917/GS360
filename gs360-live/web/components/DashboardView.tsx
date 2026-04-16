"use client";

import { useEffect, useState } from "react";
import { getHealth, listPacks } from "@/lib/api";

interface HealthData {
  status: string;
  version: string;
  deeptutor_available: boolean;
  llm_model: string;
  content_packs: number;
  deeptutor_status?: { connected: boolean; capabilities?: string[] };
}

export default function DashboardView() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [packs, setPacks] = useState<{ id: string; title: string; subject: string }[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getHealth()
      .then((d) => setHealth(d as HealthData))
      .catch((e) => setError(e.message));
    listPacks()
      .then(setPacks)
      .catch(() => {});
  }, []);

  const subjects = [
    { name: "Polity & Governance", icon: "⚖️", color: "from-blue-500 to-blue-700", topics: 42 },
    { name: "History & Culture", icon: "🏛️", color: "from-amber-500 to-amber-700", topics: 65 },
    { name: "Geography", icon: "🌍", color: "from-emerald-500 to-emerald-700", topics: 38 },
    { name: "Economy", icon: "📈", color: "from-violet-500 to-violet-700", topics: 35 },
    { name: "Science & Tech", icon: "🔬", color: "from-red-500 to-red-700", topics: 28 },
    { name: "Environment", icon: "🌿", color: "from-green-500 to-green-700", topics: 22 },
    { name: "Ethics & Integrity", icon: "🎯", color: "from-cyan-500 to-cyan-700", topics: 18 },
    { name: "Current Affairs", icon: "📰", color: "from-orange-500 to-orange-700", topics: 50 },
  ];

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-primary-500 dark:text-blue-300">
          UPSC Command Center
        </h1>
        <p className="text-[var(--muted)] mt-1">
          AI-powered preparation dashboard · Powered by DeepTutor
        </p>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <StatusCard
          title="Engine"
          value={health?.deeptutor_available ? "DeepTutor ✓" : "Local Mode"}
          color={health?.deeptutor_available ? "text-green-500" : "text-yellow-500"}
        />
        <StatusCard title="LLM" value={health?.llm_model || "..."} color="text-blue-500" />
        <StatusCard
          title="Content Packs"
          value={String(health?.content_packs ?? packs.length)}
          color="text-violet-500"
        />
        <StatusCard
          title="Capabilities"
          value={String(health?.deeptutor_status?.capabilities?.length ?? 5)}
          color="text-emerald-500"
        />
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 mb-6 text-red-400 text-sm">
          {error}
        </div>
      )}

      {/* Capabilities */}
      <h2 className="text-xl font-semibold mb-4">AI Capabilities</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <CapabilityCard
          title="UPSC Chat"
          desc="RAG-powered conversations grounded in your UPSC material"
          icon="💬"
        />
        <CapabilityCard
          title="Deep Solve"
          desc="Multi-agent problem solving with citations for complex UPSC questions"
          icon="🧠"
        />
        <CapabilityCard
          title="Quiz Generation"
          desc="Auto-generate Prelims MCQs and Mains questions from your knowledge base"
          icon="🧩"
        />
        <CapabilityCard
          title="Deep Research"
          desc="Multi-agent research across your docs, web, and academic papers"
          icon="🔬"
        />
        <CapabilityCard
          title="Answer Evaluation"
          desc="AI scoring of Mains-style answers with detailed feedback"
          icon="📝"
        />
        <CapabilityCard
          title="Guided Learning"
          desc="Structured UPSC learning paths with progressive knowledge points"
          icon="🎓"
        />
      </div>

      {/* UPSC Subjects */}
      <h2 className="text-xl font-semibold mb-4">UPSC Subjects</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
        {subjects.map((s) => (
          <div
            key={s.name}
            className={`bg-gradient-to-br ${s.color} rounded-xl p-4 text-white cursor-pointer hover:scale-[1.02] transition-transform`}
          >
            <div className="text-2xl mb-2">{s.icon}</div>
            <div className="font-semibold text-sm">{s.name}</div>
            <div className="text-xs text-white/70">{s.topics} topics</div>
          </div>
        ))}
      </div>

      {/* Content Packs */}
      {packs.length > 0 && (
        <>
          <h2 className="text-xl font-semibold mb-4">Content Packs</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {packs.map((p) => (
              <div
                key={p.id}
                className="bg-[var(--card)] border border-[var(--card-border)] rounded-xl p-4"
              >
                <div className="font-semibold text-sm">{p.title}</div>
                <div className="text-xs text-[var(--muted)]">{p.subject || p.id}</div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

function StatusCard({
  title,
  value,
  color,
}: {
  title: string;
  value: string;
  color: string;
}) {
  return (
    <div className="bg-[var(--card)] border border-[var(--card-border)] rounded-xl p-4">
      <div className="text-xs text-[var(--muted)] uppercase tracking-wider">{title}</div>
      <div className={`text-lg font-bold mt-1 ${color}`}>{value}</div>
    </div>
  );
}

function CapabilityCard({
  title,
  desc,
  icon,
}: {
  title: string;
  desc: string;
  icon: string;
}) {
  return (
    <div className="bg-[var(--card)] border border-[var(--card-border)] rounded-xl p-4 hover:border-blue-400/50 transition-colors cursor-pointer">
      <div className="text-2xl mb-2">{icon}</div>
      <div className="font-semibold text-sm">{title}</div>
      <div className="text-xs text-[var(--muted)] mt-1">{desc}</div>
    </div>
  );
}
