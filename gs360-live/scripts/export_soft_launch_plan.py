import json
import pathlib
from datetime import date


def main():
    base = pathlib.Path(__file__).resolve().parents[1]
    out = base / "eval" / "week16_soft_launch_plan.json"

    payload = {
        "generated_on": date.today().isoformat(),
        "beta_user_target": "20-30",
        "monitoring_window_days": 5,
        "daily_hotfix": True,
        "public_launch_channels": ["github", "reddit", "twitter"],
        "status": "soft_launch_ready",
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("WEEK16_SOFT_LAUNCH_PLAN_OK")


if __name__ == "__main__":
    main()
