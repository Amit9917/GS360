import json
import pathlib


SEED_PACKS = [
    "upsc-polity-seed",
    "upsc-history-seed",
    "upsc-geography-seed",
    "upsc-economy-seed",
    "upsc-environment-seed",
    "upsc-science-tech-seed",
    "upsc-ethics-seed",
    "upsc-current-affairs-seed",
]


def main():
    base = pathlib.Path(__file__).resolve().parents[1]
    packs_root = base / "content-packs"
    created = []

    for pid in SEED_PACKS:
        pdir = packs_root / pid
        (pdir / "documents").mkdir(parents=True, exist_ok=True)
        (pdir / "questions").mkdir(parents=True, exist_ok=True)
        (pdir / "flashcards").mkdir(parents=True, exist_ok=True)

        pack = {
            "id": pid,
            "name": pid.replace("-", " ").title(),
            "exam": "UPSC",
            "subject": pid.split("-")[1],
            "language": "en",
            "version": "0.1.0",
            "documents": ["documents/README.md"],
            "question_files": ["questions/seed_questions.json"],
            "flashcard_files": ["flashcards/seed_flashcards.json"],
            "contributor": "gs360-core",
            "license": "CC-BY-4.0",
        }

        (pdir / "pack.json").write_text(json.dumps(pack, indent=2), encoding="utf-8")
        (pdir / "documents" / "README.md").write_text("Seed docs placeholder\n", encoding="utf-8")
        (pdir / "questions" / "seed_questions.json").write_text("[]\n", encoding="utf-8")
        (pdir / "flashcards" / "seed_flashcards.json").write_text("[]\n", encoding="utf-8")
        created.append(pid)

    out = base / "eval" / "week11_seed_pack_report.json"
    out.write_text(json.dumps({"count": len(created), "packs": created}, indent=2), encoding="utf-8")
    print(f"SEED_PACKS_OK count={len(created)}")


if __name__ == "__main__":
    main()
