import json
import pathlib


def main():
    base = pathlib.Path(__file__).resolve().parents[1]
    src = base / "eval" / "micro_golden_set_30.json"
    out = base / "eval" / "golden_set_200_scaffold.json"

    micro = json.loads(src.read_text(encoding="utf-8"))
    rows = []
    i = 1
    while len(rows) < 200:
        for item in micro:
            row = dict(item)
            row["id"] = f"golden-{i:03d}"
            rows.append(row)
            i += 1
            if len(rows) >= 200:
                break

    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print("GOLDEN_SET_200_OK")


if __name__ == "__main__":
    main()
