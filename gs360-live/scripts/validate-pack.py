import json
import pathlib
import sys


REQUIRED_PACK_FIELDS = {
    "id",
    "name",
    "exam",
    "subject",
    "language",
    "version",
    "documents",
    "question_files",
    "flashcard_files",
    "contributor",
    "license",
}

REQUIRED_QUESTION_FIELDS = {
    "id",
    "year",
    "question",
    "options",
    "correct",
    "explanation",
    "difficulty",
    "topics",
    "source",
    "contributor",
}


def load_json(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_pack(pack_dir: pathlib.Path):
    errors = []
    pack_path = pack_dir / "pack.json"
    if not pack_path.exists():
        return [f"Missing pack.json in {pack_dir}"]

    pack = load_json(pack_path)
    missing = REQUIRED_PACK_FIELDS - set(pack.keys())
    if missing:
        errors.append(f"{pack_path}: missing fields: {sorted(missing)}")

    for rel in pack.get("question_files", []):
        q_path = pack_dir / rel
        if not q_path.exists():
            errors.append(f"Missing question file: {q_path}")
            continue
        questions = load_json(q_path)
        if not isinstance(questions, list):
            errors.append(f"{q_path}: expected list")
            continue
        for i, q in enumerate(questions):
            q_missing = REQUIRED_QUESTION_FIELDS - set(q.keys())
            if q_missing:
                errors.append(f"{q_path}[{i}]: missing fields: {sorted(q_missing)}")

    return errors


def main():
    root = pathlib.Path(__file__).resolve().parents[1] / "content-packs"
    registry = load_json(root / "registry.json")
    all_errors = []

    for item in registry.get("packs", []):
        pack_json_path = root / item["path"]
        pack_dir = pack_json_path.parent
        all_errors.extend(validate_pack(pack_dir))

    if all_errors:
        print("VALIDATION_FAILED")
        for err in all_errors:
            print(f"- {err}")
        sys.exit(1)

    print("VALIDATION_OK")


if __name__ == "__main__":
    main()
