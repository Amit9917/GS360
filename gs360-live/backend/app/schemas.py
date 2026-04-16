"""GS360 API request / response schemas."""

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


class TokenRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=64)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------------------------------------------------------------------------
# Chat / Solve / Research
# ---------------------------------------------------------------------------


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str | None = None
    knowledge_bases: list[str] = []
    capability: str = "chat"  # chat | deep_solve | deep_research | deep_question
    tools: list[str] = []  # rag, web_search, reason, code_execution, etc.


class ChatResponse(BaseModel):
    user: str
    answer: str
    session_id: str | None = None


# ---------------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------------


class QuizRequest(BaseModel):
    size: int = Field(default=10, ge=1, le=50)
    topic: str | None = None
    knowledge_bases: list[str] = []
    style: str = "upsc_prelims"  # upsc_prelims | upsc_mains | conceptual | mixed


# ---------------------------------------------------------------------------
# Notes
# ---------------------------------------------------------------------------


class NotesRequest(BaseModel):
    topic: str
    context_chunks: list[str] = []


# ---------------------------------------------------------------------------
# Eval
# ---------------------------------------------------------------------------


class EvalRequest(BaseModel):
    question: str
    reference_answer: str


# ---------------------------------------------------------------------------
# Knowledge Base
# ---------------------------------------------------------------------------


class KBCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    description: str = ""


class KBOut(BaseModel):
    name: str
    description: str = ""
    doc_count: int = 0
    status: str = "ready"


# ---------------------------------------------------------------------------
# Content Packs
# ---------------------------------------------------------------------------


class ContentPackOut(BaseModel):
    id: str
    title: str
    subject: str = ""
    topic_count: int = 0
    version: str = "1.0"
