"use client";

import { useEffect, useState } from "react";
import { listKnowledgeBases, createKnowledgeBase, searchKnowledge } from "@/lib/api";

interface KB {
  name: string;
  description?: string;
  doc_count: number;
  status?: string;
}

export default function KnowledgeView() {
  const [kbs, setKbs] = useState<KB[]>([]);
  const [loading, setLoading] = useState(true);
  const [newName, setNewName] = useState("");
  const [newDesc, setNewDesc] = useState("");
  const [searchQ, setSearchQ] = useState("");
  const [searchKb, setSearchKb] = useState("");
  const [searchResults, setSearchResults] = useState<unknown[]>([]);
  const [creating, setCreating] = useState(false);
  const [searching, setSearching] = useState(false);

  useEffect(() => {
    loadKbs();
  }, []);

  const loadKbs = async () => {
    setLoading(true);
    try {
      const data = await listKnowledgeBases();
      setKbs(data as KB[]);
    } catch {
      setKbs([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!newName.trim()) return;
    setCreating(true);
    try {
      await createKnowledgeBase(newName.trim(), newDesc.trim());
      setNewName("");
      setNewDesc("");
      await loadKbs();
    } catch (e: unknown) {
      alert(e instanceof Error ? e.message : "Failed");
    } finally {
      setCreating(false);
    }
  };

  const handleSearch = async () => {
    if (!searchKb || !searchQ.trim()) return;
    setSearching(true);
    try {
      const data = await searchKnowledge(searchKb, searchQ.trim());
      setSearchResults((data as { results?: unknown[] }).results || [data]);
    } catch (e: unknown) {
      setSearchResults([{ error: e instanceof Error ? e.message : "Search failed" }]);
    } finally {
      setSearching(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-primary-500 mb-1">📚 Knowledge Base</h1>
      <p className="text-[var(--muted)] text-sm mb-6">
        Build RAG-ready document collections for UPSC preparation
      </p>

      {/* Create KB */}
      <div className="bg-[var(--card)] border border-[var(--card-border)] rounded-xl p-5 mb-6">
        <h3 className="text-sm font-semibold mb-3">Create New Knowledge Base</h3>
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="Name (e.g. polity-notes)"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            className="flex-1 px-3 py-2 text-sm rounded-lg bg-[var(--background)] border border-[var(--card-border)] focus:outline-none"
          />
          <input
            type="text"
            placeholder="Description (optional)"
            value={newDesc}
            onChange={(e) => setNewDesc(e.target.value)}
            className="flex-1 px-3 py-2 text-sm rounded-lg bg-[var(--background)] border border-[var(--card-border)] focus:outline-none"
          />
          <button
            onClick={handleCreate}
            disabled={creating || !newName.trim()}
            className="px-4 py-2 rounded-lg bg-blue-500 text-white text-sm font-semibold disabled:opacity-50"
          >
            {creating ? "..." : "Create"}
          </button>
        </div>
      </div>

      {/* KB List */}
      <div className="bg-[var(--card)] border border-[var(--card-border)] rounded-xl p-5 mb-6">
        <h3 className="text-sm font-semibold mb-3">Your Knowledge Bases</h3>
        {loading ? (
          <p className="text-sm text-[var(--muted)]">Loading...</p>
        ) : kbs.length === 0 ? (
          <p className="text-sm text-[var(--muted)]">
            No knowledge bases yet. Create one above, then upload UPSC PDFs, notes, or textbooks.
          </p>
        ) : (
          <div className="space-y-2">
            {kbs.map((kb) => (
              <div
                key={kb.name}
                className="flex items-center justify-between p-3 rounded-lg bg-[var(--background)] border border-[var(--card-border)]"
              >
                <div>
                  <span className="font-medium text-sm">{kb.name}</span>
                  {kb.description && (
                    <span className="text-xs text-[var(--muted)] ml-2">{kb.description}</span>
                  )}
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xs text-[var(--muted)]">{kb.doc_count} docs</span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded-full ${
                      kb.status === "ready"
                        ? "bg-green-500/10 text-green-400"
                        : "bg-yellow-500/10 text-yellow-400"
                    }`}
                  >
                    {kb.status || "ready"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Search KB */}
      <div className="bg-[var(--card)] border border-[var(--card-border)] rounded-xl p-5">
        <h3 className="text-sm font-semibold mb-3">Search Knowledge Base</h3>
        <div className="flex gap-3 mb-3">
          <select
            value={searchKb}
            onChange={(e) => setSearchKb(e.target.value)}
            className="px-3 py-2 text-sm rounded-lg bg-[var(--background)] border border-[var(--card-border)] focus:outline-none"
          >
            <option value="">Select KB</option>
            {kbs.map((kb) => (
              <option key={kb.name} value={kb.name}>{kb.name}</option>
            ))}
          </select>
          <input
            type="text"
            placeholder="Search query..."
            value={searchQ}
            onChange={(e) => setSearchQ(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            className="flex-1 px-3 py-2 text-sm rounded-lg bg-[var(--background)] border border-[var(--card-border)] focus:outline-none"
          />
          <button
            onClick={handleSearch}
            disabled={searching || !searchKb || !searchQ.trim()}
            className="px-4 py-2 rounded-lg bg-blue-500 text-white text-sm font-semibold disabled:opacity-50"
          >
            {searching ? "..." : "Search"}
          </button>
        </div>
        {searchResults.length > 0 && (
          <div className="space-y-2">
            {searchResults.map((r, i) => (
              <div key={i} className="p-3 rounded-lg bg-[var(--background)] text-sm whitespace-pre-wrap">
                {typeof r === "string" ? r : JSON.stringify(r, null, 2)}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
