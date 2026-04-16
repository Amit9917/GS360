import json
import pathlib
from datetime import date


def main():
    base = pathlib.Path(__file__).resolve().parents[1]
    out = base / "eval" / "week14_deployment_plan.json"

    payload = {
        "generated_on": date.today().isoformat(),
        "frontend_target": "vercel",
        "backend_target": "railway",
        "domain": "gs360.study",
        "ssl": "required",
        "backup_target": "cloudflare_r2",
        "status": "plan_ready",
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("WEEK14_DEPLOYMENT_PLAN_OK")


if __name__ == "__main__":
    main()
