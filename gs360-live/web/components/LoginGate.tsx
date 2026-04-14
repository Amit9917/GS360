"use client";

import { useState } from "react";
import { login } from "@/lib/api";

export default function LoginGate({ onLogin }: { onLogin: () => void }) {
  const [userId, setUserId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async () => {
    if (!userId.trim()) return;
    setLoading(true);
    setError("");
    try {
      await login(userId.trim());
      onLogin();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-800 via-primary-900 to-black">
      <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-8 w-full max-w-md border border-white/20 shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">GS360</h1>
          <p className="text-white/70 text-lg">UPSC AI Tutor</p>
          <p className="text-white/50 text-sm mt-1">Powered by DeepTutor</p>
        </div>

        <div className="space-y-4">
          <input
            type="text"
            placeholder="Enter your User ID"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleLogin()}
            className="w-full px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-blue-400/50"
          />

          {error && <p className="text-red-400 text-sm">{error}</p>}

          <button
            onClick={handleLogin}
            disabled={loading || !userId.trim()}
            className="w-full py-3 rounded-xl bg-blue-500 hover:bg-blue-600 text-white font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Connecting..." : "Start Preparation"}
          </button>
        </div>

        <div className="mt-6 grid grid-cols-4 gap-2 text-center text-xs text-white/50">
          <div className="bg-white/5 rounded-lg p-2">
            <div className="text-lg">💬</div>Chat
          </div>
          <div className="bg-white/5 rounded-lg p-2">
            <div className="text-lg">🧩</div>Quiz
          </div>
          <div className="bg-white/5 rounded-lg p-2">
            <div className="text-lg">🔬</div>Research
          </div>
          <div className="bg-white/5 rounded-lg p-2">
            <div className="text-lg">📚</div>Knowledge
          </div>
        </div>
      </div>
    </div>
  );
}
