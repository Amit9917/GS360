import json
import pathlib


def score_strategy(name: str) -> float:
    """Placeholder deterministic scorer for scaffold phase."""
    weights = {
        "fixed_512": 0.56,
        "semantic_headers": 0.61,
        "hierarchical_parent_child": 0.64,
        "question_aware": 0.66,
    }
    return weights.get(name, 0.50)


def main():
    base = pathlib.Path(__file__).resolve().parents[1]
    in_file = base / "eval" / "chunking_experiments.json"
    out_file = base / "eval" / "chunking_results.json"

    with in_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    best = None
    for strategy in data.get("strategies", []):
        strategy["score_placeholder"] = score_strategy(strategy["name"])
        if best is None or strategy["score_placeholder"] > best["score_placeholder"]:
            best = strategy

    result = {
        "strategies": data["strategies"],
        "winner": best,
        "note": "Scaffold-only placeholder scoring. Replace with real eval harness outputs.",
    }

    with out_file.open("w", encoding="utf-8") as out:
        json.dump(result, out, indent=2)

    print(f"CHUNKING_EVAL_OK winner={best['name']} score={best['score_placeholder']}")


if __name__ == "__main__":
    main()
