---
title: Content Pack Guide
description: How to create, format, and contribute content packs to GS360.
---

GS360 is powered by community-contributed **Content Packs**. This guide explains how to create, format, and share your own.

## Pack structure

A Content Pack is a directory with a specific layout:

```
your-pack-name/
├── pack.json           # Pack metadata
├── documents/          # Raw source materials (PDF, MD, TXT)
├── questions/          # MCQ + Mains question banks (JSON)
├── notes/              # Pre-made study notes (Markdown)
├── prompts/            # TutorBot personas (Markdown)
└── flashcards/         # Spaced repetition cards (JSON)
```

## Shipped content

GS360 ships with a "Cold-Start" suite of content packs:

| Pack | Description |
|---|---|
| **UPSC PYQs (2000–2025)** | ~2,500 questions with AI-verified explanations |
| **NCERT Essentials** | Summaries and MCQs for History, Polity, Geography, Economy |
| **PIB/Survey/Budget** | Real-time summaries for current affairs |

## How to contribute

1. **Copy the template**: Use `templates/pack-template/` as a starting point.
2. **Add your content**: Place materials in the respective folders.
3. **Validate**: Run `python scripts/validate-pack.py` to check your pack structure.
4. **Submit a PR**: Add your pack to the `content-packs/` directory.

## Validation

```bash
cd gs360-live
python scripts/validate-pack.py
```

This checks JSON schemas, file structure, and required metadata fields.
