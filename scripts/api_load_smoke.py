import argparse
import json
import os
import random
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import requests


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _endpoint_set(base_url: str, email: str):
    return [
        ("GET", f"{base_url}/health"),
        ("GET", f"{base_url}/api/templates"),
        ("GET", f"{base_url}/api/subscription/{email}"),
        ("GET", f"{base_url}/api/resumes/{email}?limit=20&offset=0"),
    ]


def _request_once(session: requests.Session, method: str, url: str, headers: dict, timeout: float):
    start = time.perf_counter()
    try:
        response = session.request(method=method, url=url, headers=headers, timeout=timeout)
        latency_ms = (time.perf_counter() - start) * 1000
        return {
            "ok": response.ok,
            "status_code": response.status_code,
            "latency_ms": latency_ms,
            "url": url,
        }
    except requests.RequestException as exc:
        latency_ms = (time.perf_counter() - start) * 1000
        return {
            "ok": False,
            "status_code": None,
            "latency_ms": latency_ms,
            "url": url,
            "error": str(exc),
        }


def run_load(base_url: str, email: str, token: str, total_requests: int, concurrency: int, timeout: float):
    endpoints = _endpoint_set(base_url, email)
    headers = _headers(token)

    results = []
    start = time.perf_counter()

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = []
            for i in range(total_requests):
                method, url = endpoints[i % len(endpoints)]
                if i % 7 == 0:
                    method, url = random.choice(endpoints)
                futures.append(
                    executor.submit(_request_once, session, method, url, headers, timeout)
                )

            for future in as_completed(futures):
                results.append(future.result())

    total_time = max(time.perf_counter() - start, 0.001)
    latencies = [item["latency_ms"] for item in results]
    success = [item for item in results if item["ok"]]
    failures = [item for item in results if not item["ok"]]

    status_counts = {}
    for item in results:
        code = item["status_code"] if item["status_code"] is not None else "ERR"
        status_counts[code] = status_counts.get(code, 0) + 1

    latencies_sorted = sorted(latencies)
    p50 = statistics.median(latencies_sorted) if latencies_sorted else 0
    p95_index = int(0.95 * (len(latencies_sorted) - 1)) if latencies_sorted else 0
    p95 = latencies_sorted[p95_index] if latencies_sorted else 0

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "base_url": base_url,
        "total_requests": total_requests,
        "concurrency": concurrency,
        "duration_seconds": round(total_time, 3),
        "rps": round(total_requests / total_time, 2),
        "success_count": len(success),
        "failure_count": len(failures),
        "success_rate": round((len(success) / max(total_requests, 1)) * 100, 2),
        "latency_ms": {
            "min": round(min(latencies), 2) if latencies else 0,
            "p50": round(p50, 2),
            "p95": round(p95, 2),
            "max": round(max(latencies), 2) if latencies else 0,
            "avg": round(statistics.mean(latencies), 2) if latencies else 0,
        },
        "status_counts": status_counts,
        "sample_failures": failures[:8],
    }

    os.makedirs("artifacts", exist_ok=True)
    report_file = "artifacts/api_load_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n=== API Load Smoke Report ===")
    print(f"Base URL: {base_url}")
    print(f"Total requests: {summary['total_requests']} | Concurrency: {summary['concurrency']}")
    print(f"Duration: {summary['duration_seconds']}s | Throughput: {summary['rps']} req/s")
    print(f"Success: {summary['success_count']} | Failures: {summary['failure_count']} | Success rate: {summary['success_rate']}%")
    print(
        "Latency ms -> "
        f"min {summary['latency_ms']['min']} | "
        f"p50 {summary['latency_ms']['p50']} | "
        f"p95 {summary['latency_ms']['p95']} | "
        f"max {summary['latency_ms']['max']}"
    )
    print(f"Status counts: {summary['status_counts']}")
    print(f"Report saved: {report_file}")

    return 0 if summary["failure_count"] == 0 else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run lightweight API load smoke checks.")
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="Base URL for API server")
    parser.add_argument("--email", default="loadtest@soulskill.ai", help="Email used for user-scoped endpoints")
    parser.add_argument("--token", default=os.getenv("SOULSKILL_API_TOKEN", "load-test-token"), help="Bearer token")
    parser.add_argument("--requests", type=int, default=80, help="Total request count")
    parser.add_argument("--concurrency", type=int, default=10, help="Parallel request workers")
    parser.add_argument("--timeout", type=float, default=8.0, help="Per-request timeout seconds")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_url = args.url.rstrip("/")
    return run_load(base_url, args.email, args.token, args.requests, args.concurrency, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
