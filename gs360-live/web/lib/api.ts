/**
 * GS360 API client — talks to the FastAPI backend.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8001";
const AUTH_EXPIRED_EVENT = "gs360:auth-expired";

let _token: string | null = null;

function notifyAuthExpired(): void {
  if (typeof window !== "undefined") {
    window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
  }
}

function headers(): HeadersInit {
  const h: HeadersInit = { "Content-Type": "application/json" };
  if (_token) h["Authorization"] = `Bearer ${_token}`;
  return h;
}

async function api<T = unknown>(
  path: string,
  opts?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...opts,
    headers: { ...headers(), ...(opts?.headers || {}) },
  });
  if (!res.ok) {
    const body = await res.text();
    if (res.status === 401) {
      logout();
      notifyAuthExpired();
    }
    throw new Error(`API ${res.status}: ${body}`);
  }
  return res.json();
}

// ─── Auth ───────────────────────────────────────────────────────────
export async function login(userId: string): Promise<string> {
  const data = await api<{ access_token: string }>("/auth/token", {
    method: "POST",
    body: JSON.stringify({ user_id: userId }),
  });
  _token = data.access_token;
  if (typeof window !== "undefined") {
    localStorage.setItem("gs360_token", _token);
  }
  return _token;
}

export function restoreToken(): boolean {
  if (typeof window !== "undefined") {
    _token = localStorage.getItem("gs360_token");
  }
  return !!_token;
}

export function getToken(): string | null {
  return _token;
}

export function logout(): void {
  _token = null;
  if (typeof window !== "undefined") {
    localStorage.removeItem("gs360_token");
  }
}

export function onAuthExpired(handler: () => void): () => void {
  if (typeof window === "undefined") {
    return () => {};
  }
  const listener = () => handler();
  window.addEventListener(AUTH_EXPIRED_EVENT, listener);
  return () => window.removeEventListener(AUTH_EXPIRED_EVENT, listener);
}

// ─── Health ─────────────────────────────────────────────────────────
export async function getHealth() {
  return api("/health");
}

// ─── Chat ───────────────────────────────────────────────────────────
export interface ChatPayload {
  message: string;
  session_id?: string;
  knowledge_bases?: string[];
  capability?: string;
  tools?: string[];
}

export async function sendChat(payload: ChatPayload) {
  return api<{ user: string; answer: string; session_id?: string }>(
    "/api/chat",
    { method: "POST", body: JSON.stringify(payload) }
  );
}

export async function sendSolve(payload: ChatPayload) {
  return api("/api/solve", { method: "POST", body: JSON.stringify(payload) });
}

export async function sendResearch(payload: ChatPayload) {
  return api("/api/research", { method: "POST", body: JSON.stringify(payload) });
}

// ─── Quiz ───────────────────────────────────────────────────────────
export interface QuizPayload {
  size?: number;
  topic?: string;
  knowledge_bases?: string[];
  style?: string;
}

export async function generateQuiz(payload: QuizPayload) {
  return api<{ user: string; quiz: unknown[] }>("/api/quiz", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// ─── Knowledge ──────────────────────────────────────────────────────
export async function listKnowledgeBases() {
  return api<{ name: string; doc_count: number }[]>("/api/knowledge");
}

export async function createKnowledgeBase(name: string, description = "") {
  return api("/api/knowledge", {
    method: "POST",
    body: JSON.stringify({ name, description }),
  });
}

export async function searchKnowledge(kbName: string, query: string) {
  return api(`/api/knowledge/${encodeURIComponent(kbName)}/search?q=${encodeURIComponent(query)}`, {
    method: "POST",
  });
}

// ─── Notes ──────────────────────────────────────────────────────────
export async function generateNotes(topic: string, contextChunks: string[] = []) {
  return api("/api/notes", {
    method: "POST",
    body: JSON.stringify({ topic, context_chunks: contextChunks }),
  });
}

// ─── Eval ───────────────────────────────────────────────────────────
export async function evaluateAnswer(question: string, answer: string) {
  return api("/api/eval/live", {
    method: "POST",
    body: JSON.stringify({ question, reference_answer: answer }),
  });
}

// ─── Content Packs ──────────────────────────────────────────────────
export async function listPacks() {
  return api<{ id: string; title: string; subject: string }[]>("/api/packs");
}

export async function getPack(packId: string) {
  return api(`/api/packs/${encodeURIComponent(packId)}`);
}

// ─── Guide ──────────────────────────────────────────────────────────
export async function generateGuide(topic: string, kbs: string[] = []) {
  return api("/api/guide/generate", {
    method: "POST",
    body: JSON.stringify({ message: topic, knowledge_bases: kbs }),
  });
}

// ─── Memory ─────────────────────────────────────────────────────────
export async function getMemory() {
  return api("/api/memory");
}

// ─── Sessions ───────────────────────────────────────────────────────
export async function listSessions() {
  return api("/api/sessions");
}

export async function getSession(sessionId: string) {
  return api(`/api/sessions/${encodeURIComponent(sessionId)}`);
}

// ─── WebSocket ──────────────────────────────────────────────────────
export function connectWs(
  onMessage: (data: Record<string, unknown>) => void,
  onClose?: () => void
): WebSocket | null {
  if (!_token) return null;
  const wsBase = API_BASE.replace(/^http/, "ws");
  const ws = new WebSocket(`${wsBase}/ws/chat?token=${_token}`);
  ws.onmessage = (e) => {
    try {
      onMessage(JSON.parse(e.data));
    } catch {
      onMessage({ raw: e.data });
    }
  };
  ws.onclose = () => onClose?.();
  return ws;
}
