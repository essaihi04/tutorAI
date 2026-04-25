import json
from pathlib import Path

a = json.load(open(Path(__file__).resolve().parent.parent / "data" / "exams" / "topic_atlas.json", "r", encoding="utf-8"))

def short(d: str, n: int = 60) -> str:
    return d if len(d) <= n else d[:n-1] + "…"

for subject in ["SVT", "Physique-Chimie", "Mathematiques"]:
    print(f"\n════════════  {subject}  ════════════")
    for d, data in a[subject]["rotation"].items():
        p = data.get("prediction_2026") or {}
        fmt = p.get("format_probable") or ""
        w = p.get("cadre_weight_pct", 0)
        print(f"  {short(d,65):66s} {p.get('level','?'):6s}  "
              f"appear={data.get('total_appearances',0):2d}  "
              f"last={data.get('last_tested_year') or '—':>4}  "
              f"gap={data.get('years_since_last','—'):>3}  "
              f"weight={w:>5.0f}%  {fmt}")

print("\n════════════  SVT 2024 normale (sample)  ════════════")
svt2024n = a["SVT"]["years"]["2024"]["normale"]
for part in svt2024n["parts"]:
    print(f"\n  Part: {part['name']}")
    if dq := part.get("direct_questions"):
        print(f"    Part1 → {short(dq['primary_domain'],60)}  score={dq['match_score']}  hits={dq['keywords_hit'][:4]}")
    for ex in part.get("exercises", []):
        print(f"    {ex['name']:14s} ({ex['points']:.1f}p)  fmt={ex['format']:18s}  {short(ex['primary_domain'],55)}")

print("\n════════════  SVT 2025 normale  ════════════")
svt2025n = a["SVT"]["years"].get("2025", {}).get("normale", {})
for part in svt2025n.get("parts", []):
    print(f"\n  Part: {part['name']}")
    if dq := part.get("direct_questions"):
        print(f"    Part1 → {short(dq['primary_domain'],60)}  score={dq['match_score']}")
    for ex in part.get("exercises", []):
        print(f"    {ex['name']:14s} ({ex['points']:.1f}p)  {short(ex['primary_domain'],55)}")
