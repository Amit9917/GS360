"""GS360 configuration — bridges to DeepTutor's config system when available."""

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup — make the cloned DeepTutor repo importable.
# ---------------------------------------------------------------------------
_WORKSPACE_ROOT = Path(__file__).resolve().parents[3]  # E:\git hub\GS360-1
_DEEPTUTOR_ROOT = _WORKSPACE_ROOT / "deeptutor"
_GS360_ROOT = _WORKSPACE_ROOT / "gs360-live"

if str(_DEEPTUTOR_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEEPTUTOR_ROOT))


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_env_file(_GS360_ROOT / ".env")
_load_env_file(_DEEPTUTOR_ROOT / ".env")


def _try_deeptutor_config() -> dict | None:
    """Try to load DeepTutor's runtime config. Returns None on failure."""
    try:
        from deeptutor.services.config import PROJECT_ROOT, load_config_with_main

        return load_config_with_main("main.yaml", PROJECT_ROOT)
    except Exception:
        return None


@dataclass
class Settings:
    app_name: str = "GS360 — UPSC AI Tutor"
    env: str = os.getenv("GS360_ENV", "dev")
    secret_key: str = os.getenv("GS360_SECRET_KEY", "change-me")
    access_token_exp_minutes: int = int(os.getenv("GS360_TOKEN_EXP_MIN", "60"))

    # LLM — prefer DeepTutor's env vars, fall back to OPENAI_API_KEY
    llm_binding: str = os.getenv("LLM_BINDING", "openai")
    llm_model: str = os.getenv("LLM_MODEL", os.getenv("GS360_MODEL", "gpt-4o-mini"))
    llm_api_key: str = os.getenv("LLM_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    llm_host: str = os.getenv("LLM_HOST", "https://api.openai.com/v1")

    # Embedding
    embedding_binding: str = os.getenv("EMBEDDING_BINDING", "openai")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    embedding_api_key: str = os.getenv("EMBEDDING_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    embedding_host: str = os.getenv("EMBEDDING_HOST", "https://api.openai.com/v1")

    # Ports
    backend_port: int = int(os.getenv("BACKEND_PORT", "8001"))
    frontend_port: int = int(os.getenv("FRONTEND_PORT", "3000"))

    # Paths
    workspace_root: Path = field(default_factory=lambda: _WORKSPACE_ROOT)
    deeptutor_root: Path = field(default_factory=lambda: _DEEPTUTOR_ROOT)
    content_packs_dir: Path = field(
        default_factory=lambda: _WORKSPACE_ROOT / "gs360-live" / "content-packs"
    )

    @property
    def deeptutor_available(self) -> bool:
        try:
            import deeptutor  # noqa: F401

            return True
        except ImportError:
            return False


settings = Settings()
