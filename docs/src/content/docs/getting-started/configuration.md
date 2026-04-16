---
title: Configuration
description: Environment variables and secrets for GS360.
---

## Backend (`gs360-live/.env`)

### Required

| Variable | Description | Example |
|---|---|---|
| `LLM_BINDING` | LLM provider binding | `openai` |
| `LLM_MODEL` | Model name | `gpt-4o-mini` |
| `LLM_API_KEY` | API key for the LLM provider | `sk-...` |
| `LLM_HOST` | API base URL | `https://api.openai.com/v1` |

### Recommended

| Variable | Description | Example |
|---|---|---|
| `EMBEDDING_API_KEY` | API key for embeddings | `sk-...` |
| `GS360_SECRET_KEY` | JWT signing secret (long random string) | `my-super-secret-key-...` |

## Frontend (`gs360-live/web/.env.local`)

| Variable | Description | Example |
|---|---|---|
| `NEXT_PUBLIC_API_BASE` | Backend API URL | `http://localhost:8000` |

## Security guidelines

- **Never** commit `.env` files to the repository.
- Rotate keys immediately if they are exposed in logs or chat history.
- Use long, random values for `GS360_SECRET_KEY`.
- The `.gitignore` already excludes `.env` files — do not override this.
