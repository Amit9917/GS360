import os
import time
from concurrent.futures import ThreadPoolExecutor

import httpx


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
N = int(os.getenv("LOAD_REQUESTS", "100"))


def one_call(client: httpx.Client):
    r = client.get(f"{BASE_URL}/health", timeout=10)
    return r.status_code


def main():
    start = time.time()
    with httpx.Client() as client:
        with ThreadPoolExecutor(max_workers=20) as ex:
            results = list(ex.map(lambda _: one_call(client), range(N)))
    ok = sum(1 for c in results if c == 200)
    elapsed = time.time() - start
    print(f"LOAD_OK success={ok}/{N} rps={round(N/elapsed,2)}")


if __name__ == "__main__":
    main()
