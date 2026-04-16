"use client";

import { useState, useRef, useEffect } from "react";
import { sendChat, sendSolve, sendResearch } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  capability?: string;
  timestamp: Date;
}

function normalizeContent(value: unknown): string {
  if (typeof value === "string") return value;
  if (value == null) return "";
  if (typeof value === "object") {
    try {
      return JSON.stringify(value, null, 2);
    } catch {
      return String(value);
    }
  }
  return String(value);
}

const CAPABILITY_CONFIG: Record<string, { label: string; icon: string; color: string; placeholder: string }> = {
  chat: {
    label: "UPSC Chat",
    icon: "💬",
    color: "text-blue-400",
    placeholder: "Ask about any UPSC topic — Polity, History, Economy, Geography...",
  },
  deep_solve: {
    label: "Deep Solve",
    icon: "🧠",
    color: "text-purple-400",
    placeholder: "Paste a complex UPSC question for multi-agent analysis...",
  },
  deep_research: {
    label: "Deep Research",
    icon: "🔬",
    color: "text-emerald-400",
    placeholder: "Enter a topic for comprehensive multi-source research...",
  },
};

export default function ChatView({ capability }: { capability: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [selectedKb, setSelectedKb] = useState("");
  const [enableTools, setEnableTools] = useState(true);
  const endRef = useRef<HTMLDivElement>(null);
  const config = CAPABILITY_CONFIG[capability] || CAPABILITY_CONFIG.chat;

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg: Message = { role: "user", content: input.trim(), timestamp: new Date() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const payload = {
        message: userMsg.content,
        session_id: sessionId,
        knowledge_bases: selectedKb ? [selectedKb] : [],
        capability,
        tools: enableTools ? ["rag", "web_search", "reason"] : [],
      };

      let result: Record<string, unknown>;
      if (capability === "deep_solve") {
        result = (await sendSolve(payload)) as Record<string, unknown>;
      } else if (capability === "deep_research") {
        result = (await sendResearch(payload)) as Record<string, unknown>;
      } else {
        result = (await sendChat(payload)) as Record<string, unknown>;
      }

      const answer = normalizeContent(result.answer ?? result);
      if (result.session_id) setSessionId(result.session_id as string);

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: answer, capability, timestamp: new Date() },
      ]);
    } catch (e: unknown) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Error: ${e instanceof Error ? e.message : "Unknown"}`, timestamp: new Date() },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <header className="border-b border-[var(--card-border)] p-4 flex items-center gap-3">
        <span className="text-2xl">{config.icon}</span>
        <div>
          <h2 className={`font-bold ${config.color}`}>{config.label}</h2>
          <p className="text-xs text-[var(--muted)]">
            {sessionId ? `Session: ${sessionId.slice(0, 8)}...` : "New session"}
          </p>
        </div>
        <div className="ml-auto flex items-center gap-3">
          <input
            type="text"
            placeholder="Knowledge base..."
            value={selectedKb}
            onChange={(e) => setSelectedKb(e.target.value)}
            className="px-3 py-1.5 text-xs rounded-lg bg-[var(--card)] border border-[var(--card-border)] focus:outline-none focus:ring-1 focus:ring-blue-400/50 w-40"
          />
          <label className="flex items-center gap-1.5 text-xs text-[var(--muted)] cursor-pointer">
            <input
              type="checkbox"
              checked={enableTools}
              onChange={(e) => setEnableTools(e.target.checked)}
              className="rounded"
            />
            Tools
          </label>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-[var(--muted)] mt-20">
            <div className="text-5xl mb-4">{config.icon}</div>
            <p className="text-lg font-semibold">{config.label}</p>
            <p className="text-sm mt-2 max-w-md mx-auto">{config.placeholder}</p>
            <div className="mt-6 grid grid-cols-2 gap-2 max-w-md mx-auto">
              {QUICK_PROMPTS[capability]?.map((p, i) => (
                <button
                  key={i}
                  onClick={() => setInput(p)}
                  className="text-left text-xs p-3 rounded-lg bg-[var(--card)] border border-[var(--card-border)] hover:border-blue-400/50 transition"
                >
                  {p}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((m, i) => (
          <div
            key={i}
            className={`animate-fadeInUp flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm ${
                m.role === "user"
                  ? "bg-blue-500 text-white rounded-br-sm"
                  : "bg-[var(--card)] border border-[var(--card-border)] rounded-bl-sm"
              }`}
            >
              <div className="whitespace-pre-wrap">{m.content}</div>
              <div className="text-[10px] mt-1 opacity-50">
                {m.timestamp.toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-[var(--card)] border border-[var(--card-border)] rounded-2xl rounded-bl-sm px-4 py-3">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" />
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:0.15s]" />
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:0.3s]" />
              </div>
            </div>
          </div>
        )}

        <div ref={endRef} />
      </div>

      {/* Input */}
      <div className="border-t border-[var(--card-border)] p-4">
        <div className="flex gap-3 max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
            placeholder={config.placeholder}
            className="flex-1 px-4 py-3 rounded-xl bg-[var(--card)] border border-[var(--card-border)] focus:outline-none focus:ring-2 focus:ring-blue-400/30 text-sm"
          />
          <button
            onClick={send}
            disabled={loading || !input.trim()}
            className="px-6 py-3 rounded-xl bg-blue-500 hover:bg-blue-600 text-white font-semibold text-sm transition disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

const QUICK_PROMPTS: Record<string, string[]> = {
  chat: [
    "Explain the basic structure of the Indian Constitution",
    "What are the key provisions of the 73rd Amendment?",
    "Compare and contrast federalism in India and the US",
    "Summarize India's foreign policy since 1947",
  ],
  deep_solve: [
    "Critically analyze the impact of GST on Indian federalism",
    "Evaluate the effectiveness of MGNREGA in rural development",
    "Discuss the challenges of judicial activism in India",
    "Assess India's climate commitments under the Paris Agreement",
  ],
  deep_research: [
    "Research the evolution of India's space program",
    "Analyze trends in India's demographic dividend",
    "Study the impact of digital payments on financial inclusion",
    "Investigate the One Nation One Election debate",
  ],
};
