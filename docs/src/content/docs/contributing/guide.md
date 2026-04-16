---
title: Contribution Guide
description: How to contribute code, content, and fixes to GS360.
---

## Prerequisites

- **Python 3.11+**
- **Node.js 20+**
- **Docker + Docker Compose** (recommended)
- A **Gemini / OpenAI API Key** for AI features

## Local setup

```bash
# Clone and enter the repo
git clone https://github.com/JINA-CODE-SYSTEMS/GS360.git
cd GS360

# Backend
cd gs360-live
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend
cd web
npm install
```

## Running tests

```bash
# Backend (from gs360-live/)
pytest --tb=short -q

# Frontend (from gs360-live/web/)
npm run lint
npm run build
```

All PRs must pass the existing test suite and not regress RAG accuracy by more than 3%.

## Code standards

- **No hardcoded secrets or credentials.**
- All file paths must be sanitized via `UserNamespace` pattern to prevent traversal.
- RAG grounding is mandatory — answers must be cited.
- Use **conventional commits**: `feat:`, `fix:`, `docs:`, `chore:`.

## Making a pull request

1. **Fork** the repo and create a branch from `main`.
2. **Keep PRs small and focused.**
3. **Write tests** for any new functionality.
4. **CI must pass** — lint, security scan, tests, and build.

## Content contributions

Contributing content packs doesn't require code:

1. Copy `templates/pack-template/` to `content-packs/your-pack-name/`.
2. Add your materials (PDFs, MCQs, notes).
3. Run `python scripts/validate-pack.py` to check it.
4. Submit a PR.

See the [Content Pack Guide](/content-packs/guide/) for full details.

## What needs a discussion first

Open an issue before starting work on:
- Major architectural changes.
- New core features not on the roadmap.
- Changes to the multi-tenancy or security layer.
