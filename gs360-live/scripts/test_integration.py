"""GS360 integration smoke test — validates all imports and bridge wiring."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # gs360-live/
WORKSPACE = ROOT.parent

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(WORKSPACE))

passed = 0
failed = 0


def check(label, fn):
    global passed, failed
    try:
        result = fn()
        print(f"  [PASS] {label}: {result}")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] {label}: {e}")
        failed += 1


# 1. DeepTutor import
check("DeepTutor import", lambda: __import__("deeptutor").__file__)

# 2. Config
def test_config():
    from backend.app.config import settings
    return f"app={settings.app_name}, dt={settings.deeptutor_available}"

check("GS360 config", test_config)

# 3. Schemas
check("Schemas", lambda: (
    __import__("backend.app.schemas", fromlist=["ChatRequest"]).ChatRequest,
    "OK"
)[1])

# 4. Security
def test_security():
    from backend.app.security import create_token, decode_token
    t = create_token("test-user")
    p = decode_token(t)
    return f"sub={p['sub']}"

check("Security (JWT)", test_security)

# 5. Bridge
def test_bridge():
    from backend.app.services.deeptutor_bridge import DeepTutorBridge
    b = DeepTutorBridge()
    return f"available={b.available}, packs={b.count_packs()}, health={b.health()}"

check("DeepTutor Bridge", test_bridge)

# 6. FastAPI app creation
def test_app():
    from backend.app.main import app
    routes = [r.path for r in app.routes if hasattr(r, "path")]
    return f"{len(routes)} routes: {routes[:8]}..."

check("FastAPI app", test_app)

# 7. LLM client
def test_llm():
    from backend.app.services.llm_client import LLMClient
    c = LLMClient()
    return f"enabled={c.enabled}"

check("LLM client", test_llm)

print(f"\n=== RESULTS: {passed} passed, {failed} failed ===")
sys.exit(1 if failed else 0)
