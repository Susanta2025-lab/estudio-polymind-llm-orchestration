"""Bounded authenticated synchronous load for Phase 15 Kind validation."""

import argparse
import concurrent.futures
import json
import time
import urllib.request


def request(url: str, token: str, sequence: int) -> bool:
    body = json.dumps({
        "query": "Tell me a phase15-slow-query joke.",
        "session_id": f"phase15-load-{sequence}",
    }).encode()
    target = urllib.request.Request(
        f"{url.rstrip('/')}/query", body, method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(target, timeout=30) as response:
        return response.status == 200 and json.load(response).get("route") == "direct"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:18001")
    parser.add_argument("--token", required=True)
    parser.add_argument("--concurrency", type=int, default=8, choices=range(1, 17))
    parser.add_argument("--requests", type=int, default=80, choices=range(1, 201))
    args = parser.parse_args()
    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(args.concurrency) as executor:
        results = list(executor.map(
            lambda sequence: request(args.url, args.token, sequence), range(args.requests)
        ))
    print(json.dumps({
        "requests": len(results), "successes": sum(results),
        "duration_seconds": round(time.monotonic() - started, 3),
    }))
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
