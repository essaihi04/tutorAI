"""Build the BAC topic coverage atlas (SVT / PC / Math, 2016-2025).

Usage:
    python backend/scripts/build_topic_atlas.py [--show-report]

Outputs:
    backend/data/exams/topic_atlas.json
"""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("RAG_DISABLED", "1")  # atlas doesn't need RAG

from app.services.topic_atlas_service import topic_atlas, SUBJECT_DOMAINS


def main():
    print("Building BAC topic atlas…")
    atlas = topic_atlas.rebuild()

    # Sanity report
    print(f"\n═══ ATLAS SUMMARY ═══")
    for subject, entry in atlas.items():
        years = sorted(entry.get("years", {}).keys())
        total_sessions = sum(len(y) for y in entry["years"].values())
        domains = entry.get("domains_seen", [])
        print(f"\n{subject}:")
        print(f"  Years covered: {years[0]}–{years[-1]} ({len(years)} years, {total_sessions} sessions)")
        print(f"  Domains detected: {len(domains)} — {', '.join(domains[:5])}{'…' if len(domains) > 5 else ''}")

        # Prediction summary
        priorities = topic_atlas.predict_2026_priorities(subject)
        print(f"  Predictions for BAC 2026:")
        for level in ("HIGH", "MEDIUM", "LOW"):
            items = priorities.get(level, [])
            if items:
                top = [it["domain"] for it in items[:3]]
                print(f"    {level} ({len(items)}): {', '.join(top)}{'…' if len(items) > 3 else ''}")

    if "--show-report" in sys.argv:
        print("\n═══ FULL HISTORICAL CONTEXT — SVT ═══")
        print(topic_atlas.build_historical_context_for_prompt("SVT", max_years=5))
        print("\n═══ FULL HISTORICAL CONTEXT — Physique-Chimie ═══")
        print(topic_atlas.build_historical_context_for_prompt("Physique-Chimie", max_years=5))

    print(f"\n✓ Atlas saved to backend/data/exams/topic_atlas.json")


if __name__ == "__main__":
    main()
