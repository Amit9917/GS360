"use client";

import { useEffect, useState } from "react";
import { listPacks, getPack } from "@/lib/api";

interface Pack {
  id: string;
  title: string;
  subject: string;
  topic_count: number;
  version: string;
}

export default function PacksView() {
  const [packs, setPacks] = useState<Pack[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    listPacks()
      .then((data) => setPacks(data as Pack[]))
      .catch(() => setPacks([]))
      .finally(() => setLoading(false));
  }, []);

  const viewPack = async (id: string) => {
    try {
      const data = await getPack(id);
      setSelected(data as Record<string, unknown>);
    } catch {
      setSelected(null);
    }
  };

  const subjectColors: Record<string, string> = {
    polity: "from-blue-500 to-blue-700",
    history: "from-amber-500 to-amber-700",
    geography: "from-emerald-500 to-emerald-700",
    economy: "from-violet-500 to-violet-700",
    science: "from-red-500 to-red-700",
    environment: "from-green-500 to-green-700",
    ethics: "from-cyan-500 to-cyan-700",
    current: "from-orange-500 to-orange-700",
  };

  const getGradient = (subject: string) => {
    const key = Object.keys(subjectColors).find((k) => subject.toLowerCase().includes(k));
    return subjectColors[key || "polity"];
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold text-primary-500 mb-1">📦 Content Packs</h1>
      <p className="text-[var(--muted)] text-sm mb-6">
        UPSC subject-wise curated content — study materials, question banks, and topic guides
      </p>

      {loading ? (
        <p className="text-[var(--muted)]">Loading packs...</p>
      ) : packs.length === 0 ? (
        <p className="text-[var(--muted)]">No content packs available.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {packs.map((p) => (
            <button
              key={p.id}
              onClick={() => viewPack(p.id)}
              className={`text-left bg-gradient-to-br ${getGradient(
                p.subject || p.id
              )} rounded-xl p-5 text-white hover:scale-[1.02] transition-transform`}
            >
              <div className="font-bold text-lg mb-1">{p.title}</div>
              <div className="text-white/70 text-sm">{p.subject || p.id}</div>
              <div className="flex gap-3 mt-3 text-xs text-white/60">
                <span>{p.topic_count} topics</span>
                <span>v{p.version}</span>
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Detail view */}
      {selected && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-6">
          <div className="bg-[var(--card)] border border-[var(--card-border)] rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-6">
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-xl font-bold">
                {(selected.title as string) || (selected.id as string)}
              </h2>
              <button
                onClick={() => setSelected(null)}
                className="text-[var(--muted)] hover:text-[var(--foreground)] text-xl"
              >
                ×
              </button>
            </div>
            <pre className="text-xs bg-[var(--background)] p-4 rounded-lg overflow-auto whitespace-pre-wrap">
              {JSON.stringify(selected, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
