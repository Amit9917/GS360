"""
DeepTutor Bridge — connects GS360 to DeepTutor's full capability stack.

This module imports DeepTutor's application facade, session store,
knowledge-base manager, and capability registry to provide:
  - RAG-powered chat with UPSC knowledge bases
  - Quiz generation (UPSC prelims / mains style)
  - Deep Solve multi-agent problem solving
  - Deep Research with citations
  - Guided Learning path generation
  - Knowledge base CRUD
  - Persistent memory / learner profile
  - Session management

When DeepTutor is not installed, all methods fall back to local
GS360 modules (content packs, quiz engine, grounded notes).
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from pathlib import Path
from typing import Any

from ..config import settings

logger = logging.getLogger("gs360.bridge")

# ── Local fallback imports (always available) ─────────────────────────
import sys

_GS360_LIVE = Path(__file__).resolve().parents[3]
if str(_GS360_LIVE) not in sys.path:
    sys.path.insert(0, str(_GS360_LIVE))

from core.ai_notes import build_grounded_notes
from core.content_pack_manager import ContentPackManager
from core.quiz_engine import QuizEngine
from .llm_client import LLMClient


def _stringify_answer(value: Any) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    if isinstance(value, dict):
        summary = value.get("summary")
        if isinstance(summary, str) and summary.strip():
            return summary
        topic = value.get("topic")
        grounded = value.get("grounded")
        if topic:
            grounded_suffix = " (grounded)" if grounded else ""
            return f"{topic}{grounded_suffix}"
    try:
        return json.dumps(value, ensure_ascii=False, indent=2, default=str)
    except Exception:
        return str(value)


class DeepTutorBridge:
    """Unified gateway that delegates to DeepTutor when available."""

    def __init__(self) -> None:
        self._app = None  # DeepTutorApp facade
        self._kb_manager = None
        self._session_store = None
        self._pack_manager = ContentPackManager(root=_GS360_LIVE)
        self._llm = LLMClient()
        self._available = False
        self._try_init()

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def _try_init(self) -> None:
        """Attempt to import DeepTutor and wire up components."""
        try:
            from deeptutor.app.facade import DeepTutorApp

            self._app = DeepTutorApp()
            self._available = True
            logger.info("DeepTutor engine loaded successfully")
        except Exception as exc:
            logger.warning("DeepTutor not available, using local fallbacks: %s", exc)
            self._available = False

        # Knowledge base manager (DeepTutor)
        if self._available:
            try:
                from deeptutor.knowledge.manager import KnowledgeBaseManager
                from deeptutor.services.config import PROJECT_ROOT

                kb_dir = PROJECT_ROOT / "data" / "knowledge_bases"
                kb_dir.mkdir(parents=True, exist_ok=True)
                self._kb_manager = KnowledgeBaseManager(base_dir=str(kb_dir))
            except Exception as exc:
                logger.warning("KB manager init failed: %s", exc)

    @property
    def available(self) -> bool:
        return self._available

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def startup(self) -> None:
        """Warm-up tasks on server start."""
        if not self._available:
            return
        try:
            from deeptutor.services.llm import get_llm_client

            llm = get_llm_client()
            logger.info("LLM client ready: model=%s", llm.config.model)
        except Exception as exc:
            logger.warning("LLM warm-up failed: %s", exc)

    async def shutdown(self) -> None:
        """Cleanup on server stop."""
        pass

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def health(self) -> dict:
        if not self._available:
            return {"connected": False, "engine": "local_fallback"}
        caps = []
        try:
            caps = [m["name"] for m in self._app.capabilities.get_manifests()]
        except Exception:
            pass
        return {
            "connected": True,
            "engine": "deeptutor",
            "capabilities": caps,
        }

    # ------------------------------------------------------------------
    # Chat / Capabilities
    # ------------------------------------------------------------------

    async def chat(
        self,
        message: str,
        session_id: str | None = None,
        knowledge_bases: list[str] | None = None,
        capability: str = "chat",
        tools: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Send a message through DeepTutor's turn-based runtime.
        Falls back to local grounded response when unavailable.
        """
        if capability in {"deep_solve", "deep_research"}:
            return {
                "answer": await self._fallback_answer(message, capability),
                "session_id": session_id or str(uuid.uuid4()),
            }

        if not self._available or self._app is None:
            return {
                "answer": await self._fallback_answer(message, capability),
                "session_id": session_id or str(uuid.uuid4()),
            }

        try:
            from deeptutor.app.facade import TurnRequest

            sid = session_id or str(uuid.uuid4())
            req = TurnRequest(
                content=message,
                capability=capability,
                session_id=sid,
                tools=tools or [],
                knowledge_bases=knowledge_bases or [],
            )

            # DeepTutor facade starts a turn and exposes a streaming iterator.
            _session, turn = await self._app.start_turn(req)
            chunks: list[str] = []
            async for event in self._app.stream_turn(turn["id"], after_seq=0):
                if not isinstance(event, dict):
                    continue
                if event.get("type") != "content":
                    continue
                content = event.get("content", "")
                if content:
                    chunks.append(str(content))

            if not chunks:
                session_detail = await self._app.get_session(sid)
                messages = [] if session_detail is None else session_detail.get("messages", [])
                for item in reversed(messages):
                    if item.get("role") == "assistant" and item.get("content"):
                        chunks.append(str(item["content"]))
                        break

            if not chunks:
                chunks.append(await self._fallback_answer(message, capability))

            return {
                "answer": "".join(chunks) or "[No response from engine]",
                "session_id": sid,
            }
        except Exception as exc:
            logger.exception("DeepTutor chat failed, falling back")
            return {
                "answer": await self._fallback_answer(message, capability),
                "session_id": session_id or str(uuid.uuid4()),
                "fallback": True,
                "error": str(exc),
            }

    async def _fallback_answer(self, message: str, capability: str) -> str:
        prompt = self._build_fallback_prompt(message, capability)
        if self._llm.enabled:
            try:
                result = await self._llm.complete(prompt, max_tokens=1200)
                text = str(result).strip()
                if text:
                    return text
            except Exception as exc:
                logger.warning("LLM fallback failed: %s", exc)
        return _stringify_answer(build_grounded_notes(message, []))

    @staticmethod
    def _build_fallback_prompt(message: str, capability: str) -> str:
        if capability == "deep_solve":
            return (
                "You are a UPSC tutor. Solve the user's query with structured reasoning. "
                "Respond with: 1) core answer, 2) 3-5 bullet analysis points, 3) brief conclusion.\n\n"
                f"User query: {message}"
            )
        if capability == "deep_research":
            return (
                "You are a UPSC research assistant. Provide a concise research-style response with "
                "key points, context, and significance. Avoid claiming live web citations unless given.\n\n"
                f"Research topic: {message}"
            )
        return (
            "You are an expert UPSC tutor. Answer clearly, accurately, and concisely for an aspirant.\n\n"
            f"Question: {message}"
        )

    # ------------------------------------------------------------------
    # Quiz Generation
    # ------------------------------------------------------------------

    async def generate_quiz(
        self,
        topic: str | None = None,
        size: int = 10,
        knowledge_bases: list[str] | None = None,
        style: str = "upsc_prelims",
    ) -> list[dict]:
        """
        Generate quiz questions — uses DeepTutor's deep_question capability
        when available, falls back to local QuizEngine.
        """
        if self._available and self._app is not None:
            try:
                result = await self.chat(
                    message=self._build_quiz_prompt(topic, size, style),
                    knowledge_bases=knowledge_bases or [],
                    capability="deep_question",
                    tools=["rag"] if knowledge_bases else [],
                )
                # Try to parse structured quiz from response
                return self._parse_quiz_response(result["answer"], size)
            except Exception as exc:
                logger.warning("DeepTutor quiz gen failed: %s", exc)

        # Local fallback
        packs = self._pack_manager.list_packs()
        bank = []
        for p in packs:
            bank.append({
                "id": p["id"],
                "question": f"[{style.upper()}] Sample on {p.get('title', p['id'])}",
                "topics": [topic or "general"],
            })
        engine = QuizEngine(bank)
        return engine.generate(size=size, topic=topic)

    @staticmethod
    def _build_quiz_prompt(topic: str | None, size: int, style: str) -> str:
        style_desc = {
            "upsc_prelims": "UPSC Civil Services Preliminary Exam MCQ style",
            "upsc_mains": "UPSC Mains long-answer analytical style",
            "conceptual": "conceptual understanding questions",
            "mixed": "mixed format (MCQ + short answer + analytical)",
        }
        desc = style_desc.get(style, style)
        topic_str = f" on the topic '{topic}'" if topic else ""
        return (
            f"Generate exactly {size} {desc} questions{topic_str}. "
            f"For each question provide: question text, 4 options (A-D) for MCQ, "
            f"correct answer, and a brief explanation. Format as JSON array."
        )

    @staticmethod
    def _parse_quiz_response(text: str, size: int) -> list[dict]:
        """Try to extract JSON quiz array from LLM response."""
        # Find JSON array in response
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start : end + 1])[:size]
            except json.JSONDecodeError:
                pass
        # Return as single-item if parsing fails
        return [{"question": text, "type": "generated"}]

    # ------------------------------------------------------------------
    # Knowledge Base
    # ------------------------------------------------------------------

    def list_knowledge_bases(self) -> list[dict]:
        if self._kb_manager:
            try:
                return self._kb_manager.list_knowledge_bases()
            except Exception:
                pass
        return []

    async def create_knowledge_base(self, name: str, description: str = "") -> dict:
        if self._kb_manager:
            try:
                self._kb_manager.create_knowledge_base(name)
                return {"name": name, "description": description, "doc_count": 0, "status": "ready"}
            except Exception as exc:
                logger.warning("KB creation failed: %s", exc)
        return {"name": name, "description": description, "doc_count": 0, "status": "local"}

    async def search_knowledge(self, kb_name: str, query: str) -> list[dict]:
        """Search a knowledge base using DeepTutor's RAG pipeline."""
        if not self._available:
            return [{"text": "Knowledge base search requires DeepTutor engine", "score": 0}]
        try:
            result = await self.chat(
                message=query,
                knowledge_bases=[kb_name],
                capability="chat",
                tools=["rag"],
            )
            return [{"text": result["answer"], "source": "rag"}]
        except Exception as exc:
            return [{"text": str(exc), "score": 0}]

    # ------------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------------

    async def generate_notes(self, topic: str, context_chunks: list[str]) -> str:
        if self._available:
            try:
                result = await self.chat(
                    message=f"Generate comprehensive study notes on: {topic}",
                    capability="chat",
                    tools=["rag", "web_search"],
                )
                return result["answer"]
            except Exception:
                pass
        return build_grounded_notes(topic, context_chunks)

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    async def evaluate_answer(self, question: str, reference_answer: str) -> dict:
        if self._available:
            try:
                result = await self.chat(
                    message=(
                        f"Evaluate this UPSC answer.\n\n"
                        f"Question: {question}\n\n"
                        f"Student Answer: {reference_answer}\n\n"
                        f"Provide: score (0-10), strengths, weaknesses, "
                        f"model answer, and improvement suggestions."
                    ),
                    capability="chat",
                    tools=["reason"],
                )
                return {"evaluation": result["answer"], "engine": "deeptutor"}
            except Exception:
                pass
        return {
            "evaluation": f"Local eval — Q: {question[:100]}",
            "engine": "local",
        }

    # ------------------------------------------------------------------
    # Guided Learning
    # ------------------------------------------------------------------

    async def generate_guide(self, topic: str, knowledge_bases: list[str] | None = None) -> dict:
        if self._available:
            try:
                result = await self.chat(
                    message=(
                        f"Create a structured learning guide for UPSC preparation on: {topic}. "
                        f"Include 3-5 progressive knowledge points with explanations, "
                        f"examples, and practice questions."
                    ),
                    knowledge_bases=knowledge_bases or [],
                    capability="chat",
                    tools=["rag"] if knowledge_bases else [],
                )
                return {"guide": result["answer"], "topic": topic}
            except Exception:
                pass
        return {"guide": f"Learning guide for {topic} (requires DeepTutor)", "topic": topic}

    # ------------------------------------------------------------------
    # Memory
    # ------------------------------------------------------------------

    async def get_memory(self) -> dict:
        if self._available:
            try:
                from deeptutor.services.memory import get_memory_manager

                mgr = get_memory_manager()
                return {"summary": mgr.get_summary(), "profile": mgr.get_profile()}
            except Exception:
                pass
        return {"summary": "", "profile": {}}

    async def update_memory(self, data: dict) -> dict:
        if self._available:
            try:
                from deeptutor.services.memory import get_memory_manager

                mgr = get_memory_manager()
                if "summary" in data:
                    mgr.update_summary(data["summary"])
                return {"status": "updated"}
            except Exception:
                pass
        return {"status": "local_only"}

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------

    def list_sessions(self) -> list[dict]:
        if self._available and self._app:
            try:
                return self._app.store.list_sessions(limit=50)
            except Exception:
                pass
        return []

    def get_session(self, session_id: str) -> dict | None:
        if self._available and self._app:
            try:
                return self._app.store.get_session(session_id)
            except Exception:
                pass
        return None

    # ------------------------------------------------------------------
    # Content Packs (local)
    # ------------------------------------------------------------------

    def list_packs(self) -> list[dict]:
        packs = self._pack_manager.list_packs()
        return [
            {
                "id": p["id"],
                "title": p.get("title", p["id"]),
                "subject": p.get("subject", ""),
                "topic_count": len(p.get("topics", [])),
                "version": p.get("version", "1.0"),
            }
            for p in packs
        ]

    def get_pack(self, pack_id: str) -> dict | None:
        for p in self._pack_manager.list_packs():
            if p["id"] == pack_id:
                return p
        return None

    def count_packs(self) -> int:
        return len(self._pack_manager.list_packs())
