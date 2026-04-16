import os

import httpx


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def main():
    r = httpx.get(f"{BASE_URL}/health", timeout=15)
    r.raise_for_status()
    print("SMOKE_OK /health", r.json().get("status"))


if __name__ == "__main__":
    main()
