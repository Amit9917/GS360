import json
import pathlib


def main():
    root = pathlib.Path(__file__).resolve().parents[1] / "content-packs"
    registry_path = root / "registry.json"

    with registry_path.open("r", encoding="utf-8") as f:
        registry = json.load(f)

    ingested = []
    for entry in registry.get("packs", []):
        if not entry.get("enabled", True):
            continue

        pack_path = root / entry["path"]
        with pack_path.open("r", encoding="utf-8") as pf:
            pack = json.load(pf)

        ingested.append(
            {
                "id": pack["id"],
                "subject": pack["subject"],
                "question_files": pack.get("question_files", []),
                "flashcard_files": pack.get("flashcard_files", []),
            }
        )

    out_path = pathlib.Path(__file__).resolve().parents[1] / "ingest-report.json"
    with out_path.open("w", encoding="utf-8") as out:
        json.dump({"count": len(ingested), "packs": ingested}, out, indent=2)

    print(f"INGEST_OK count={len(ingested)} report={out_path}")


if __name__ == "__main__":
    main()
