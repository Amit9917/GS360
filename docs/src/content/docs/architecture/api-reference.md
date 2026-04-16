---
title: API Reference
description: GS360 backend REST and WebSocket endpoints.
---

## Base URL

```
http://localhost:8000
```

## Health

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check — returns `200` if the backend is running. |

## Authentication

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/token` | Issue a JWT token. |

All other endpoints require `Authorization: Bearer <token>` header.

## Chat & AI

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/chat` | Send a message and receive an AI-grounded response. |
| `POST` | `/api/solve` | Deep problem-solving (DeepTutor `deep_solve`). |
| `POST` | `/api/research` | Deep research on a topic (DeepTutor `deep_research`). |
| `WS` | `/ws/chat?token=<jwt>` | Real-time streaming chat via WebSocket. |

## Knowledge Base

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/knowledge` | List indexed knowledge items. |
| `POST` | `/api/knowledge` | Upload a document to the knowledge base. |

## Quiz

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/quiz` | Generate quiz questions from indexed content. |

## Notes

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/notes` | Generate AI study notes on a topic. |

## Content Packs

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/packs` | List available content packs. |

## Evaluation

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/eval/live` | Run live evaluation against the Golden Dataset. |

## Study Guide

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/guide/generate` | Generate a personalized study guide. |
