"""Bounded authenticated HTTP capacity baseline for PolyMind.

This intentionally uses only the Python standard library. It measures the HTTP
boundary and records run context; it is not a universal production benchmark.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import platform
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Optional


PROMPTS = {
    "direct": "Tell me a short deterministic joke.",
    "rag": "Search my knowledge base and explain retrieval augmented generation briefly.",
    "stream": "Tell me a short deterministic joke.",
}


@dataclass
class Observation:
    success: bool
    latency_seconds: float
    ttft_seconds: Optional[float] = None
    stream_duration_seconds: Optional[float] = None
    status: Optional[int] = None
    error: Optional[str] = None


def percentile(values: list[float], fraction: float) -> Optional[float]:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int(len(ordered) * fraction + 0.999999) - 1))
    return round(ordered[index], 6)


def git_sha() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def one_request(base_url: str, token: str, workload: str, timeout: float, sequence: int) -> Observation:
    endpoint = "/query/stream" if workload == "stream" else "/query"
    body = json.dumps({
        "query": PROMPTS[workload],
        "session_id": f"phase13-{workload}-{sequence}",
    }).encode()
    request = urllib.request.Request(
        base_url.rstrip("/") + endpoint,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Request-ID": f"phase13-{workload}-{sequence}",
        },
        method="POST",
    )
    started = time.perf_counter()
    first_content = None
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            if workload == "stream":
                done = False
                for raw_line in response:
                    event = json.loads(raw_line)
                    if event.get("type") == "chunk" and first_content is None:
                        first_content = time.perf_counter()
                    if event.get("type") == "error":
                        raise RuntimeError("sanitized_stream_error")
                    done = done or event.get("type") == "done"
                if not done:
                    raise RuntimeError("stream_ended_without_done")
            else:
                payload = json.load(response)
                if payload.get("route") != workload:
                    raise RuntimeError(f"unexpected_route:{payload.get('route')}")
            finished = time.perf_counter()
            return Observation(
                True,
                finished - started,
                None if first_content is None else first_content - started,
                None if workload != "stream" else finished - started,
                response.status,
            )
    except urllib.error.HTTPError as exc:
        return Observation(False, time.perf_counter() - started, status=exc.code, error="http_error")
    except Exception as exc:
        return Observation(
            False, time.perf_counter() - started, error=type(exc).__name__
        )


def execute(args) -> dict:
    if args.concurrency > 32 or args.requests > 1000 or args.duration > 300:
        raise ValueError("safety bounds: concurrency<=32, requests<=1000, duration<=300")
    deadline = time.monotonic() + args.duration if args.duration else None
    next_sequence = 0
    observations: list[Observation] = []
    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        pending = set()
        while True:
            while len(pending) < args.concurrency:
                if deadline is not None and time.monotonic() >= deadline:
                    break
                # Request count is always a hard cap, including duration mode.
                if next_sequence >= args.requests:
                    break
                pending.add(pool.submit(
                    one_request, args.base_url, args.token, args.workload, args.timeout, next_sequence
                ))
                next_sequence += 1
            if not pending:
                break
            done, pending = concurrent.futures.wait(
                pending, return_when=concurrent.futures.FIRST_COMPLETED
            )
            observations.extend(future.result() for future in done)
    elapsed = time.perf_counter() - started
    successful = [item for item in observations if item.success]
    latencies = [item.latency_seconds for item in successful]
    ttfts = [item.ttft_seconds for item in successful if item.ttft_seconds is not None]
    stream_durations = [
        item.stream_duration_seconds for item in successful if item.stream_duration_seconds is not None
    ]
    errors: dict[str, int] = {}
    for item in observations:
        if not item.success:
            key = item.error or f"http_{item.status}"
            errors[key] = errors.get(key, 0) + 1
    return {
        "context": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "git_sha": git_sha(),
            "image": args.image,
            "replica_count": args.replicas,
            "environment": args.environment,
            "resource_configuration": args.resources,
            "host": platform.platform(),
        },
        "workload": args.workload,
        "concurrency": args.concurrency,
        "requested_requests": args.requests,
        "requested_duration_seconds": args.duration or None,
        "timeout_seconds": args.timeout,
        "requests": len(observations),
        "successes": len(successful),
        "failures": len(observations) - len(successful),
        "errors": errors,
        "duration_seconds": round(elapsed, 6),
        "requests_per_second": round(len(successful) / elapsed, 6) if elapsed else None,
        "latency_seconds": {
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
            "p99": percentile(latencies, 0.99),
        },
        "ttft_seconds": {
            "p50": percentile(ttfts, 0.50),
            "p95": percentile(ttfts, 0.95),
        },
        "stream_duration_seconds": {
            "p50": percentile(stream_durations, 0.50),
            "p95": percentile(stream_durations, 0.95),
        },
    }


def parser() -> argparse.ArgumentParser:
    target = argparse.ArgumentParser(description=__doc__)
    target.add_argument("--base-url", default="http://127.0.0.1:8001")
    target.add_argument("--token", default=os.getenv("POLYMIND_BENCHMARK_TOKEN"))
    target.add_argument("--workload", choices=tuple(PROMPTS), required=True)
    target.add_argument("--concurrency", type=int, default=1)
    target.add_argument("--requests", type=int, default=10)
    target.add_argument("--duration", type=float, default=0)
    target.add_argument("--timeout", type=float, default=120)
    target.add_argument("--image", default="unknown")
    target.add_argument("--replicas", type=int, default=1)
    target.add_argument("--environment", default="local")
    target.add_argument("--resources", default="unknown")
    return target


def main() -> None:
    args = parser().parse_args()
    if not args.token:
        raise SystemExit("--token or POLYMIND_BENCHMARK_TOKEN is required")
    if args.concurrency < 1 or args.requests < 1 or args.duration < 0 or args.timeout <= 0:
        raise SystemExit("concurrency, requests, and timeout must be positive; duration cannot be negative")
    print(json.dumps(execute(args), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
