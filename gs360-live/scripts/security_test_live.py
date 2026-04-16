import os

import httpx


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def main():
    unauth = httpx.post(f"{BASE_URL}/api/notes", json={"topic": "x", "context_chunks": []}, timeout=15)
    if unauth.status_code != 403 and unauth.status_code != 401:
        raise RuntimeError(f"Expected auth failure, got {unauth.status_code}")

    token_resp = httpx.post(f"{BASE_URL}/auth/token", json={"user_id": "security_test"}, timeout=15)
    token_resp.raise_for_status()
    token = token_resp.json()["access_token"]

    auth = httpx.post(
        f"{BASE_URL}/api/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={"topic": "security", "context_chunks": ["ctx"]},
        timeout=15,
    )
    auth.raise_for_status()
    print("SECURITY_OK")


if __name__ == "__main__":
    main()
