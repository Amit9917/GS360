"""
GS360 Backend — UPSC AI Tutor powered by DeepTutor
===================================================
Exposes UPSC-focused endpoints while delegating AI capabilities
to DeepTutor's engine (RAG, chat, quiz generation, deep solve, etc.).
"""

from __future__ import annotations

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .schemas import (
    ChatRequest,
    ChatResponse,
    ContentPackOut,
    EvalRequest,
    KBCreateRequest,
    KBOut,
    NotesRequest,
    QuizRequest,
    TokenRequest,
    TokenResponse,
)
from .security import create_token, current_user, decode_token
from .services.deeptutor_bridge import DeepTutorBridge
from .websocket_manager import WebSocketManager

logger = logging.getLogger("gs360")

# ---------------------------------------------------------------------------
# Lifespan — start/stop DeepTutor engine when available
# ---------------------------------------------------------------------------

bridge = DeepTutorBridge()
ws_manager = WebSocketManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("GS360 starting — DeepTutor available: %s", bridge.available)
    if bridge.available:
        await bridge.startup()
    yield
    if bridge.available:
        await bridge.shutdown()
    logger.info("GS360 shutdown complete")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="GS360 — UPSC AI Tutor",
    version="2.0.0",
    lifespan=lifespan,
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve GS360 content packs as static files
_packs_dir = settings.content_packs_dir
if _packs_dir.exists():
    app.mount("/static/packs", StaticFiles(directory=str(_packs_dir)), name="packs")

# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "2.0.0",
        "deeptutor_available": bridge.available,
        "deeptutor_status": bridge.health(),
        "llm_model": settings.llm_model,
        "content_packs": bridge.count_packs(),
    }


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


@app.post("/auth/token", response_model=TokenResponse)
def issue_token(payload: TokenRequest):
    return TokenResponse(access_token=create_token(payload.user_id))


# ---------------------------------------------------------------------------
# Chat — proxies to DeepTutor's chat capability with UPSC context
# ---------------------------------------------------------------------------


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, user_id: str = Depends(current_user)):
    answer = await bridge.chat(
        message=req.message,
        session_id=req.session_id,
        knowledge_bases=req.knowledge_bases,
        capability=req.capability,
        tools=req.tools,
    )
    raw_answer = answer.get("answer")
    if isinstance(raw_answer, str):
        answer_text = raw_answer
    else:
        answer_text = json.dumps(raw_answer, ensure_ascii=False, indent=2, default=str)
    return ChatResponse(
        user=user_id,
        answer=answer_text,
        session_id=answer.get("session_id"),
    )


# ---------------------------------------------------------------------------
# Deep Solve — multi-agent problem solving for UPSC answers
# ---------------------------------------------------------------------------


@app.post("/api/solve")
async def deep_solve(req: ChatRequest, user_id: str = Depends(current_user)):
    result = await bridge.chat(
        message=req.message,
        session_id=req.session_id,
        knowledge_bases=req.knowledge_bases,
        capability="deep_solve",
        tools=req.tools,
    )
    return {"user": user_id, **result}


# ---------------------------------------------------------------------------
# Quiz Generation — UPSC-style question generation
# ---------------------------------------------------------------------------


@app.post("/api/quiz")
async def quiz(req: QuizRequest, user_id: str = Depends(current_user)):
    questions = await bridge.generate_quiz(
        topic=req.topic,
        size=req.size,
        knowledge_bases=req.knowledge_bases,
        style=req.style,
    )
    return {"user": user_id, "quiz": questions}


# ---------------------------------------------------------------------------
# Knowledge Base management
# ---------------------------------------------------------------------------


@app.get("/api/knowledge", response_model=list[KBOut])
async def list_knowledge_bases(user_id: str = Depends(current_user)):
    return bridge.list_knowledge_bases()


@app.post("/api/knowledge", response_model=KBOut)
async def create_knowledge_base(req: KBCreateRequest, user_id: str = Depends(current_user)):
    return await bridge.create_knowledge_base(req.name, req.description)


@app.post("/api/knowledge/{kb_name}/search")
async def search_knowledge(kb_name: str, q: str, user_id: str = Depends(current_user)):
    results = await bridge.search_knowledge(kb_name, q)
    return {"user": user_id, "kb": kb_name, "results": results}


# ---------------------------------------------------------------------------
# Notes — grounded AI notes on UPSC topics
# ---------------------------------------------------------------------------


@app.post("/api/notes")
async def notes(req: NotesRequest, user_id: str = Depends(current_user)):
    result = await bridge.generate_notes(req.topic, req.context_chunks)
    return {"user": user_id, "notes": result}


# ---------------------------------------------------------------------------
# Eval — live model-backed answer evaluation
# ---------------------------------------------------------------------------


@app.post("/api/eval/live")
async def eval_live(req: EvalRequest, user_id: str = Depends(current_user)):
    result = await bridge.evaluate_answer(req.question, req.reference_answer)
    return {"user": user_id, "result": result}


# ---------------------------------------------------------------------------
# Content Packs — UPSC subject-wise content
# ---------------------------------------------------------------------------


@app.get("/api/packs", response_model=list[ContentPackOut])
def list_packs():
    return bridge.list_packs()


@app.get("/api/packs/{pack_id}")
def get_pack(pack_id: str):
    pack = bridge.get_pack(pack_id)
    if not pack:
        raise HTTPException(404, f"Pack {pack_id!r} not found")
    return pack


# ---------------------------------------------------------------------------
# Deep Research — multi-agent research on UPSC topics
# ---------------------------------------------------------------------------


@app.post("/api/research")
async def deep_research(req: ChatRequest, user_id: str = Depends(current_user)):
    result = await bridge.chat(
        message=req.message,
        session_id=req.session_id,
        knowledge_bases=req.knowledge_bases,
        capability="deep_research",
        tools=req.tools,
    )
    return {"user": user_id, **result}


# ---------------------------------------------------------------------------
# Guided Learning — structured UPSC learning paths
# ---------------------------------------------------------------------------


@app.post("/api/guide/generate")
async def generate_guide(req: ChatRequest, user_id: str = Depends(current_user)):
    result = await bridge.generate_guide(req.message, req.knowledge_bases)
    return {"user": user_id, **result}


# ---------------------------------------------------------------------------
# Memory — persistent learner profile
# ---------------------------------------------------------------------------


@app.get("/api/memory")
async def get_memory(user_id: str = Depends(current_user)):
    return await bridge.get_memory()


@app.post("/api/memory/update")
async def update_memory(data: dict, user_id: str = Depends(current_user)):
    return await bridge.update_memory(data)


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------


@app.get("/api/sessions")
async def list_sessions(user_id: str = Depends(current_user)):
    return bridge.list_sessions()


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str, user_id: str = Depends(current_user)):
    return bridge.get_session(session_id)


# ---------------------------------------------------------------------------
# WebSocket — real-time UPSC chat with DeepTutor engine
# ---------------------------------------------------------------------------


@app.websocket("/ws/chat")
async def ws_chat(ws: WebSocket, token: str):
    payload = decode_token(token)
    user_id = payload["sub"]
    await ws_manager.connect(user_id, ws)
    try:
        while True:
            raw = await ws.receive_text()
            try:
                data = json.loads(raw)
                message = data.get("message", raw)
                kb = data.get("knowledge_bases", [])
                capability = data.get("capability", "chat")
            except json.JSONDecodeError:
                message = raw
                kb = []
                capability = "chat"

            answer = await bridge.chat(
                message=message,
                knowledge_bases=kb,
                capability=capability,
            )
            await ws_manager.send_user(user_id, {"q": message, **answer})
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id, ws)


# ---------------------------------------------------------------------------
# Landing redirect
# ---------------------------------------------------------------------------


@app.get("/")
def root():
    return {
        "service": "GS360 — UPSC AI Tutor",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
    }

