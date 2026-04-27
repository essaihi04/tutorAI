"""
Load test for moalim.online EXAM API endpoints.

Simulates N concurrent users each hitting the read-only exam APIs:
  - GET /api/v1/exam/list
  - GET /api/v1/exam/stats
  - GET /api/v1/exam/detail/{exam_id}  (picks a random exam from the list)

Usage:
    python tools/loadtest_api.py 100            # 100 users, default ramp 5s
    python tools/loadtest_api.py 500 --ramp 10

Outputs per-endpoint latency, p50/p95/p99, total RPS, error breakdown.
"""
import argparse
import asyncio
import random
import statistics
import sys
import time
from collections import Counter
from typing import Optional

import aiohttp

DEFAULT_BASE = "https://moalim.online"
REQ_TIMEOUT = 15


async def one_user(
    session: aiohttp.ClientSession,
    base: str,
    exam_ids: list[str],
    user_id: int,
    delay_s: float,
    results: list,
) -> None:
    """Simulate one user browsing the exam hub."""
    if delay_s > 0:
        await asyncio.sleep(delay_s)

    timings: dict[str, float] = {}
    statuses: dict[str, int] = {}
    error: Optional[str] = None

    try:
        # 1. GET /api/v1/exam/list
        t0 = time.perf_counter()
        async with session.get(
            f"{base}/api/v1/exam/list",
            timeout=aiohttp.ClientTimeout(total=REQ_TIMEOUT),
        ) as r:
            await r.read()
            timings["list"] = (time.perf_counter() - t0) * 1000
            statuses["list"] = r.status

        # 2. GET /api/v1/exam/stats
        t0 = time.perf_counter()
        async with session.get(
            f"{base}/api/v1/exam/stats",
            timeout=aiohttp.ClientTimeout(total=REQ_TIMEOUT),
        ) as r:
            await r.read()
            timings["stats"] = (time.perf_counter() - t0) * 1000
            statuses["stats"] = r.status

        # 3. GET /api/v1/exam/detail/{exam_id}  (random exam)
        if exam_ids:
            eid = random.choice(exam_ids)
            t0 = time.perf_counter()
            async with session.get(
                f"{base}/api/v1/exam/detail/{eid}",
                timeout=aiohttp.ClientTimeout(total=REQ_TIMEOUT),
            ) as r:
                await r.read()
                timings["detail"] = (time.perf_counter() - t0) * 1000
                statuses["detail"] = r.status

    except asyncio.TimeoutError:
        error = "timeout"
    except aiohttp.ClientError as e:
        error = f"client_error:{type(e).__name__}"
    except Exception as e:
        error = f"unknown:{type(e).__name__}:{e}"

    total_ms = sum(timings.values()) if timings else 0
    results.append({
        "user_id": user_id,
        "total_ms": total_ms,
        "timings": timings,
        "statuses": statuses,
        "error": error,
    })


def percentile(data: list[float], p: float) -> float:
    if not data:
        return 0.0
    s = sorted(data)
    k = (len(s) - 1) * p
    f = int(k)
    c = min(f + 1, len(s) - 1)
    if f == c:
        return s[f]
    return s[f] + (s[c] - s[f]) * (k - f)


def fmt(label: str, values: list[float]) -> str:
    if not values:
        return f"  {label}: <no data>"
    return (
        f"  {label}: "
        f"avg={statistics.mean(values):7.1f}ms  "
        f"p50={percentile(values, 0.50):7.1f}ms  "
        f"p95={percentile(values, 0.95):7.1f}ms  "
        f"p99={percentile(values, 0.99):7.1f}ms  "
        f"max={max(values):7.1f}ms"
    )


async def run(n_users: int, base: str, ramp_s: float) -> None:
    print(f"\n{'='*70}")
    print(f"API Load test → {base}")
    print(f"  Users:        {n_users}")
    print(f"  Ramp-up:      {ramp_s}s")
    print(f"  Per user:     GET /exam/list + /exam/stats + /exam/detail/{{id}}")
    print(f"{'='*70}")

    # Warm-up: fetch exam list to get IDs
    connector = aiohttp.TCPConnector(limit=0, limit_per_host=0, ttl_dns_cache=300)
    exam_ids: list[str] = []
    async with aiohttp.ClientSession(connector=connector) as warmup:
        try:
            async with warmup.get(
                f"{base}/api/v1/exam/list",
                timeout=aiohttp.ClientTimeout(total=REQ_TIMEOUT),
            ) as r:
                data = await r.json()
                exam_ids = [e["id"] for e in data.get("exams", []) if "id" in e]
        except Exception as e:
            print(f"❌ Warm-up failed: {e}")
            return

    print(f"  Exams found:  {len(exam_ids)}")
    if not exam_ids:
        print("  ⚠️  No exams in catalog — detail endpoint won't be tested")
    print()

    results: list = []
    connector = aiohttp.TCPConnector(
        limit=n_users + 50, limit_per_host=n_users + 50,
        ttl_dns_cache=300, force_close=False,
    )
    async with aiohttp.ClientSession(connector=connector) as session:
        per_user_delay = ramp_s / n_users if n_users > 1 else 0
        t_start = time.perf_counter()
        tasks = [
            asyncio.create_task(
                one_user(session, base, exam_ids, i, i * per_user_delay, results)
            )
            for i in range(n_users)
        ]

        total = len(tasks)
        done_count = 0
        while done_count < total:
            await asyncio.sleep(0.5)
            done_count = sum(1 for t in tasks if t.done())
            elapsed = time.perf_counter() - t_start
            print(
                f"\r  Progress: {done_count:5d}/{total} ({100*done_count/total:5.1f}%) "
                f"elapsed={elapsed:6.1f}s",
                end="", flush=True,
            )

        await asyncio.gather(*tasks, return_exceptions=True)
        total_time = time.perf_counter() - t_start

    print()

    success = [r for r in results if not r["error"]]
    errored = [r for r in results if r["error"]]

    list_lat = [r["timings"]["list"] for r in success if "list" in r["timings"]]
    stats_lat = [r["timings"]["stats"] for r in success if "stats" in r["timings"]]
    detail_lat = [r["timings"]["detail"] for r in success if "detail" in r["timings"]]
    total_lat = [r["total_ms"] for r in success]

    n_reqs_per_user = 3 if exam_ids else 2

    status_counter: Counter = Counter()
    for r in results:
        for kind, code in r["statuses"].items():
            status_counter[f"{kind}={code}"] += 1
    error_counter: Counter = Counter(r["error"] for r in errored)

    print("\n📊 Results")
    print(f"  Total time:        {total_time:.2f}s")
    print(f"  Effective RPS:     {(len(success)*n_reqs_per_user)/total_time:.0f} req/s")
    print(f"  Successful users:  {len(success):4d}/{n_users}  "
          f"({100*len(success)/n_users:.1f}%)")
    print(f"  Failed users:      {len(errored):4d}/{n_users}  "
          f"({100*len(errored)/n_users:.1f}%)")

    print("\n⏱  Latency per endpoint")
    print(fmt("/exam/list  ", list_lat))
    print(fmt("/exam/stats ", stats_lat))
    print(fmt("/exam/detail", detail_lat))
    print(fmt("TOTAL/user  ", total_lat))

    print("\n📦 HTTP status codes")
    for k in sorted(status_counter):
        print(f"  {k}: {status_counter[k]}")

    if error_counter:
        print("\n❌ Errors")
        for k, v in error_counter.most_common():
            print(f"  {k}: {v}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("users", type=int)
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--ramp", type=float, default=5.0)
    args = parser.parse_args()
    if args.users <= 0:
        print("users must be > 0", file=sys.stderr)
        sys.exit(1)
    try:
        asyncio.run(run(args.users, args.base.rstrip("/"), args.ramp))
    except KeyboardInterrupt:
        print("\nInterrupted.")


if __name__ == "__main__":
    main()
