import json
import pathlib
import sys
from datetime import date

BASE = pathlib.Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from core.feature_freeze import FREEZE_DATE


def main():
    out = BASE / "eval" / "week10_freeze_gate.json"
    payload = {
        "feature_freeze_date": FREEZE_DATE.isoformat(),
        "generated_on": date.today().isoformat(),
        "policy": "No new features after freeze; bug fixes only.",
        "status": "active",
    }
    with out.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("WEEK10_FREEZE_GATE_OK")


if __name__ == "__main__":
    main()
