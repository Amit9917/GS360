---
title: Architecture Overview
description: How GS360 is structured — backend, frontend, and AI pipeline.
---

## High-level architecture

```
┌─────────────────────┐      ┌──────────────────────┐
│  Next.js Frontend   │─────▶│   Auth Layer (JWT)   │
│  (React 19 + TS)    │      └──────────┬───────────┘
└─────────────────────┘               │
                                      ▼
                          ┌───────────────────────┐
                          │  Security Middleware   │
                          └──────────┬────────────┘
                                     │
                                     ▼
                          ┌───────────────────────┐
                          │  FastAPI Backend       │
                          │  (Uvicorn + WebSocket) │
                          └──────────┬────────────┘
                                     │
                      ┌──────────────┼──────────────┐
                      ▼              ▼              ▼
              ┌──────────┐   ┌──────────┐   ┌───────────┐
              │ DeepTutor│   │  LLM     │   │ Content   │
              │ Bridge   │   │ Fallback │   │ Pack Mgr  │
              └────┬─────┘   └────┬─────┘   └─────┬─────┘
                   │              │               │
                   ▼              ▼               ▼
              ┌──────────┐   ┌──────────┐   ┌───────────┐
              │RAG       │   │Gemini /  │   │Shared +   │
              │Pipeline  │   │DeepSeek/ │   │Private    │
              └──────────┘   │Ollama    │   │Indices    │
                             └──────────┘   └───────────┘
```

## Repository layout

| Directory | Purpose |
|---|---|
| `gs360-live/backend/` | FastAPI backend + DeepTutor bridge |
| `gs360-live/web/` | Next.js 15 frontend (React 19, TypeScript) |
| `gs360-live/core/` | Shared domain/runtime helpers (rate limiter, quiz engine, vault, etc.) |
| `gs360-live/scripts/` | Validation, ingestion, and evaluation scripts |
| `demo-gs360/` | Standalone demo UI assets |
| `docs/` | This documentation site |

## Key design decisions

### Multi-tenancy & security
- **Index isolation**: Each user's notes and uploads use physically separate vector stores.
- **Path sanitization**: Mandatory `realpath` validation prevents path traversal.
- **Audit logging**: Request-level authentication bound to unique workspaces.

### LLM fallback chain
GS360 uses a tiered fallback strategy:
1. **DeepTutor runtime** — Full agent chain with RAG grounding.
2. **Direct LLM** — Falls back to a direct OpenAI/Gemini/DeepSeek call if DeepTutor is unavailable.
3. **Ollama (local)** — Fully offline fallback.

### Content pack system
Community-contributed content packs plug into isolated vector indices. The system auto-ingests documents, questions, notes, and flashcards from structured directories-no code required.

### Frontend
- **Next.js 15** with `output: "standalone"` for Docker deployment.
- **React 19** with strict TypeScript.
- Real-time chat via WebSocket (`/ws/chat`).
