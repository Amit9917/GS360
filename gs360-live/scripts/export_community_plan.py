import json
import pathlib
from datetime import date


def main():
    base = pathlib.Path(__file__).resolve().parents[1]
    out = base / "eval" / "week15_community_plan.json"

    payload = {
        "generated_on": date.today().isoformat(),
        "channels": ["discord", "telegram"],
        "docs": ["README.md", "CONTRIBUTING.md", "SECURITY.md", "docs/CONTENT_GUIDE.md"],
        "analytics": "optional_plausible",
        "status": "plan_ready",
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("WEEK15_COMMUNITY_PLAN_OK")


if __name__ == "__main__":
    main()
