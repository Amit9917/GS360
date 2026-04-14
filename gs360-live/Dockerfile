# ============================================
# GS360 — UPSC AI Tutor (DeepTutor-powered)
# Multi-stage: Next.js frontend + FastAPI backend
# ============================================

# ── Stage 1: Frontend Builder ────────────────────────────────────────
FROM --platform=$BUILDPLATFORM node:22-slim AS frontend-builder
WORKDIR /app/web
COPY web/package.json web/package-lock.json* ./
RUN npm ci --legacy-peer-deps 2>/dev/null || npm install
COPY web/ ./
RUN echo "NEXT_PUBLIC_API_BASE=__NEXT_PUBLIC_API_BASE_PLACEHOLDER__" > .env.local
RUN npm run build

# ── Stage 2: Python + DeepTutor ──────────────────────────────────────
FROM python:3.11-slim AS production
LABEL maintainer="GS360 Team" description="GS360 UPSC AI Tutor powered by DeepTutor"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BACKEND_PORT=8001 \
    FRONTEND_PORT=3000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*

# Node for Next.js
COPY --from=node:22-slim /usr/local/bin/node /usr/local/bin/
COPY --from=node:22-slim /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -sf /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm

# Install DeepTutor from sibling dir (COPY context must include it)
COPY ../deeptutor /app/deeptutor
RUN pip install --upgrade pip && pip install -e /app/deeptutor[server] || true

# GS360 Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# GS360 backend code
COPY backend/ ./backend/
COPY core/ ./core/
COPY content-packs/ ./content-packs/

# Built frontend
COPY --from=frontend-builder /app/web/.next/standalone ./web/
COPY --from=frontend-builder /app/web/.next/static ./web/.next/static
COPY --from=frontend-builder /app/web/public ./web/public

EXPOSE 8001 3000
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8001/health || exit 1

CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8001} & node web/server.js & wait"]

