---
title: Quickstart
description: Get GS360 running locally in under 5 minutes.
---

## Prerequisites

- **Python 3.11+**
- **Node.js 20+**
- **Docker + Docker Compose** (optional, for containerized run)
- A **Gemini / OpenAI API Key** for AI features

## Option 1: Local Development

### 1. Clone

```bash
git clone https://github.com/JINA-CODE-SYSTEMS/GS360.git
cd GS360
```

### 2. Backend setup

```bash
cd gs360-live
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend setup

```bash
cd web
npm install
```

### 4. Environment files

Create `gs360-live/.env` from `gs360-live/.env.example` and configure your API keys.

Create `gs360-live/web/.env.local`:
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

### 5. Run

**Backend** (from `gs360-live/backend`):
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend** (from `gs360-live/web`):
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Option 2: Docker

From the repo root:

```bash
docker compose up --build
```

| Service | Port |
|---|---|
| Frontend | `3000` |
| Backend | `8001` |

## Troubleshooting

### `Failed to fetch` on login
Set `NEXT_PUBLIC_API_BASE=http://localhost:8000` in `gs360-live/web/.env.local` and restart the frontend.

### `Invalid token: Signature verification failed`
Refresh the page and log in again. The frontend auto-clears stale tokens on `401`.

### Next.js chunk errors
Clear the build cache:
```bash
cd gs360-live/web
rm -rf .next
npm run dev
```

### `uvicorn` not found
Activate your virtual env and re-install:
```bash
cd gs360-live
source .venv/bin/activate
pip install -r requirements.txt
```
