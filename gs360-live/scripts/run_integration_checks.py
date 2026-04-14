import json
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from core.integration_health import ServiceStatus, summarize


def _exists(rel_path: str) -> bool:
    return (BASE / rel_path).exists()


def main():
    statuses = [
        ServiceStatus(
            "frontend",
            _exists("../demo-gs360/index.html"),
            "demo page available" if _exists("../demo-gs360/index.html") else "missing ../demo-gs360/index.html",
        ),
        ServiceStatus(
            "content-packs",
            _exists("content-packs/registry.json"),
            "registry present" if _exists("content-packs/registry.json") else "missing content-packs/registry.json",
        ),
        ServiceStatus(
            "retrieval-core",
            _exists("core/hybrid_retrieval.py"),
            "hybrid retrieval scaffolded" if _exists("core/hybrid_retrieval.py") else "missing core/hybrid_retrieval.py",
        ),
        ServiceStatus(
            "auth-runtime",
            _exists("core/auth_runtime_stub.py"),
            "auth runtime scaffold present" if _exists("core/auth_runtime_stub.py") else "missing core/auth_runtime_stub.py",
        ),
        ServiceStatus(
            "websocket-runtime",
            _exists("core/websocket_runtime_stub.py"),
            "websocket runtime scaffold present"
            if _exists("core/websocket_runtime_stub.py")
            else "missing core/websocket_runtime_stub.py",
        ),
    ]

    report = summarize(statuses)
    out = BASE / "eval" / "week9_integration_report.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"INTEGRATION_CHECK_OK all_green={report['all_green']}")


if __name__ == "__main__":
    main()
