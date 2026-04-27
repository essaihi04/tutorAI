"""
Load test for moalim.online homepage.

Simulates N concurrent users each loading the full first-paint payload:
  - GET /                       (index.html, served by nginx)
  - GET /assets/<main>.js       (main React bundle, ~2.4 MB)
  - GET /assets/<main>.css      (main stylesheet, ~216 KB)

Usage:
    python tools/loadtest_homepage.py 1000            # 1000 users, default ramp 10s
    python tools/loadtest_homepage.py 1000 --ramp 5   # ramp over 5s
    python tools/loadtest_homepage.py 100 --base http://localhost:5173

Outputs per-user latency, p50/p95/p99, total RPS, error breakdown.
"""
import argparse
import asyncio
import re
import statistics
import sys
import time
from collections import Counter
from typing import Optional

import aiohttp


# Default base URL (production)
DEFAULT_BASE = "https://moalim.online"

# Request timeout per HTTP call (seconds)
REQ_TIMEOUT = 30


async def fetch_index_assets(session: aiohttp.ClientSession, base: str) -> tuple[str, str]:
    """Fetch / once and parse the actual hashed JS+CSS asset URLs from index.html.

    Returns (js_url, css_url) so the load test hits the REAL assets currently
    deployed (not a hard-coded hash that would 404 after every redeploy).
    """
    async with session.get(base + "/", timeout=aiohttp.ClientTimeout(total=REQ_TIMEOUT)) as r:
        html = await r.text()
    js_match = re.search(r'/assets/(index-[A-Za-z0-9_-]+\.js)', html)
    css_match = re.search(r'/assets/(index-[A-Za-z0-9_-]+\.css)', html)
    if not js_match or not css_match:
        raise RuntimeError(
            "Could not parse index.html assets — is the server serving the SPA?"
        )
    return f"/assets/{js_match.group(1)}", f"/assets/{css_match.group(1)}"


async def one_user(
    session: aiohttp.ClientSession,
    base: str,
    js_path: str,
    css_path: str,
    user_id: int,
    delay_s: float,
    results: list,
) -> None:
    """Simulate one user opening the homepage cold."""
    if delay_s > 0:
        await asyncio.sleep(delay_s)

    timings: dict[str, float] = {}
    statuses: dict[str, int] = {}
    error: Optional[str] = None

    try:
        # 1. index.html
        t0 = time.perf_counter()
        async with session.get(
            base + "/",
            timeout=aiohttp.ClientTimeout(total=REQ_TIMEOUT),
            headers={"User-Agent": f"loadtest/{user_id}"},
        ) as r:
            await r.read()
            timings["html"] = (time.perf_counter() - t0) * 1000
            statuses["html"] = r.status

        # 2. main JS bundle (parallel with CSS)
        async def _js() -> None:
            t = time.perf_counter()
            async with session.get(
                base + js_path,
                timeout=aiohttp.ClientTimeout(total=REQ_TIMEOUT),
            ) as resp:
                await resp.read()
                timings["js"] = (time.perf_counter() - t) * 1000
                statuses["js"] = resp.status

        async def _css() -> None:
            t = time.perf_counter()
            async with session.get(
                base + css_path,
                timeout=aiohttp.ClientTimeout(total=REQ_TIMEOUT),
            ) as resp:
                await resp.read()
                timings["css"] = (time.perf_counter() - t) * 1000
                statuses["css"] = resp.status

        await asyncio.gather(_js(), _css())

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


def format_summary(label: str, values: list[float]) -> str:
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


async def run(n_users: int, base: str, ramp_s: float) -> dict:
    print(f"\n{'='*70}")
    print(f"Load test → {base}")
    print(f"  Users:        {n_users}")
    print(f"  Ramp-up:      {ramp_s}s  (=> {n_users/ramp_s:.0f} new users/s)")
    print(f"  Per user:     GET / + main.js + main.css")
    print(f"{'='*70}")

    # Single warm-up call to discover current asset hashes
    connector = aiohttp.TCPConnector(limit=0, limit_per_host=0, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as warmup:
        try:
            js_path, css_path = await fetch_index_assets(warmup, base)
        except Exception as e:
            print(f"❌ Warm-up failed: {e}")
            return {"error": "warmup_failed"}
        print(f"  Detected JS:  {js_path}")
        print(f"  Detected CSS: {css_path}\n")

    # Real load test — fresh connector, plenty of slots
    results: list = []
    connector = aiohttp.TCPConnector(
        limit=n_users + 50,
        limit_per_host=n_users + 50,
        ttl_dns_cache=300,
        force_close=False,
    )
    async with aiohttp.ClientSession(connector=connector) as session:
        per_user_delay = ramp_s / n_users if n_users > 1 else 0
        t_start = time.perf_counter()
        tasks = [
            asyncio.create_task(
                one_user(
                    session=session,
                    base=base,
                    js_path=js_path,
                    css_path=css_path,
                    user_id=i,
                    delay_s=i * per_user_delay,
                    results=results,
                )
            )
            for i in range(n_users)
        ]

        # Progress bar
        total = len(tasks)
        done_count = 0
        while done_count < total:
            await asyncio.sleep(0.5)
            done_count = sum(1 for t in tasks if t.done())
            elapsed = time.perf_counter() - t_start
            print(
                f"\r  Progress: {done_count:5d}/{total} ({100*done_count/total:5.1f}%) "
                f"elapsed={elapsed:6.1f}s",
                end="",
                flush=True,
            )

        await asyncio.gather(*tasks, return_exceptions=True)
        total_time = time.perf_counter() - t_start

    print()  # newline after progress bar

    # ── Aggregation ───────────────────────────────────────────────────
    success = [r for r in results if not r["error"]]
    errored = [r for r in results if r["error"]]

    html_lat = [r["timings"]["html"] for r in success if "html" in r["timings"]]
    js_lat = [r["timings"]["js"] for r in success if "js" in r["timings"]]
    css_lat = [r["timings"]["css"] for r in success if "css" in r["timings"]]
    total_lat = [r["total_ms"] for r in success]

    status_counter: Counter = Counter()
    for r in results:
        for kind, code in r["statuses"].items():
            status_counter[f"{kind}={code}"] += 1
    error_counter: Counter = Counter(r["error"] for r in errored)

    print("\n📊 Results")
    print(f"  Total time:        {total_time:.2f}s")
    print(f"  Effective RPS:     {(len(success)*3)/total_time:.0f} req/s "
          f"(3 reqs per user)")
    print(f"  Successful users:  {len(success):4d}/{n_users}  "
          f"({100*len(success)/n_users:.1f}%)")
    print(f"  Failed users:      {len(errored):4d}/{n_users}  "
          f"({100*len(errored)/n_users:.1f}%)")

    print("\n⏱  Latency per resource")
    print(format_summary("index.html", html_lat))
    print(format_summary("main.js   ", js_lat))
    print(format_summary("main.css  ", css_lat))
    print(format_summary("TOTAL/user", total_lat))

    print("\n📦 HTTP status codes")
    for k in sorted(status_counter):
        print(f"  {k}: {status_counter[k]}")

    if error_counter:
        print("\n❌ Errors")
        for k, v in error_counter.most_common():
            print(f"  {k}: {v}")

    return {
        "n_users": n_users,
        "success": len(success),
        "errored": len(errored),
        "total_time_s": total_time,
        "p50_total_ms": percentile(total_lat, 0.50),
        "p95_total_ms": percentile(total_lat, 0.95),
        "p99_total_ms": percentile(total_lat, 0.99),
        "rps": (len(success) * 3) / total_time if total_time else 0,
        "errors": dict(error_counter),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("users", type=int, help="Number of concurrent users to simulate")
    parser.add_argument("--base", default=DEFAULT_BASE, help=f"Base URL (default: {DEFAULT_BASE})")
    parser.add_argument(
        "--ramp",
        type=float,
        default=10.0,
        help="Ramp-up duration in seconds (spread the user starts; default 10s)",
    )
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
