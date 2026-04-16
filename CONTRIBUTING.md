# Contributing to GS360

Thanks for your interest in contributing to the first open-source, AI-powered UPSC learning platform. This document covers everything you need to get started.

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker and Docker Compose (recommended)
- A Gemini API Key (for AI features)

## Local Setup

```bash
# Clone and enter the repo
git clone https://github.com/JINA-CODE-SYSTEMS/gs360.git
cd gs360

# Setup backend
cd gs360-live
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd ../demo-gs360
npm install
```

Detailed setup instructions for each component are in their respective directories.

## Running Tests

We prioritize RAG accuracy and security.

```bash
# Run RAG evaluation (from gs360-live)
python eval/eval_runner.py
```

All PRs must pass the existing test suite and not regress RAG accuracy by more than 3% (on the full golden set).

## Code Standards

- No hardcoded secrets or credentials.
- All file paths must be sanitized via `UserNamespace` pattern to prevent traversal.
- RAG grounding is mandatory — answers must be cited.

## Making a Pull Request

1. **Fork** the repo and create a branch from `main`.
2. **Keep PRs small and focused**.
3. **Write tests** for any new functionality.
4. **Use conventional commits** (e.g., `feat:`, `fix:`, `docs:`, `chore:`).

## Content Contributions

Contributing content packs doesn't require code. 
- Copy `templates/pack-template/` to `content-packs/your-pack-name/`.
- Add your materials (PDFs, MCQs, notes).
- Submit a PR.

## What Needs a Discussion First

Open a discussion or issue before starting work on:
- Major architectural changes.
- New core features not on the roadmap.
- Changes to the multi-tenancy or security layer.

## Questions?

Open a discussion — we're happy to help.
