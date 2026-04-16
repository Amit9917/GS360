# Content Pack Guide

GS360 is powered by community-contributed Content Packs. This guide explains how to create, format, and share your own packs.

## Pack Structure

A Content Pack is a directory with a specific layout:

```
your-pack-name/
├── pack.json                 # Pack metadata
├── documents/                # Raw source materials (PDF, MD, TXT)
├── questions/                # MCQ + Mains question banks (JSON)
├── notes/                    # Pre-made study notes (Markdown)
├── prompts/                  # TutorBot personas (Markdown)
└── flashcards/               # Spaced repetition cards (JSON)
```

## How to Contribute

1. **Copy the template**: Use `templates/pack-template/` as a starting point.
2. **Add your content**: Place your materials in the respective folders.
3. **Validate**: Ensure your JSON files follow the schemas (TBD).
4. **Submit a PR**: Add your pack to the `content-packs/` directory and update `registry.json`.

*Detailed schemas and automated validation tools are coming in Phase 1.*
