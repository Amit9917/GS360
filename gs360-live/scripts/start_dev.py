#!/usr/bin/env python3
"""
GS360 Local Development Server
===============================
Starts both the FastAPI backend and Next.js frontend.
Automatically installs DeepTutor if found in the workspace.
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # gs360-live/
WORKSPACE = ROOT.parent  # E:\git hub\GS360-1
DEEPTUTOR = WORKSPACE / "deeptutor"
WEB = ROOT / "web"


def banner(text: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> int:
    print(f"  → {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    if check and result.returncode != 0:
        print(f"  ✗ Command failed (exit {result.returncode})")
    return result.returncode


def install_deeptutor() -> None:
    if not DEEPTUTOR.exists():
        print("  DeepTutor not found — using local fallbacks only.")
        return
    banner("Installing DeepTutor")
    run([sys.executable, "-m", "pip", "install", "-e", f"{DEEPTUTOR}[server]"], check=False)


def install_gs360_deps() -> None:
    banner("Installing GS360 Backend Dependencies")
    run([sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")])


def install_frontend() -> None:
    if not (WEB / "node_modules").exists():
        banner("Installing Frontend Dependencies")
        run(["npm", "install"], cwd=WEB, check=False)


def start_backend() -> subprocess.Popen:
    banner("Starting GS360 Backend (port 8001)")
    env = {**os.environ, "PYTHONPATH": str(WORKSPACE)}
    return subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "backend.app.main:app",
            "--host", "0.0.0.0",
            "--port", str(os.getenv("BACKEND_PORT", "8001")),
            "--reload",
        ],
        cwd=str(ROOT),
        env=env,
    )


def start_frontend() -> subprocess.Popen:
    banner("Starting GS360 Frontend (port 3000)")
    return subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=str(WEB),
    )


def main() -> None:
    banner("GS360 — UPSC AI Tutor (Local Dev)")

    install_deeptutor()
    install_gs360_deps()
    install_frontend()

    backend = start_backend()
    frontend = start_frontend()

    print("\n" + "=" * 60)
    print("  GS360 is running!")
    print("  Backend  → http://localhost:8001")
    print("  Frontend → http://localhost:3000")
    print("  API Docs → http://localhost:8001/docs")
    print("  Press Ctrl+C to stop")
    print("=" * 60 + "\n")

    try:
        backend.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("Done.")


if __name__ == "__main__":
    main()
