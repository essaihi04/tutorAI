"""Normalize question points in math exam.json so each exercise hits its
declared `points`, and total = 20. Rounds to 0.25 increments then corrects drift."""
import json, sys
from pathlib import Path

ROOT = Path("backend/data/exams/mathematiques")

def round025(x: float) -> float:
    return round(x * 4) / 4

def normalize_exercise(ex: dict) -> None:
    target = float(ex.get("points", 0) or 0)
    qs = ex.get("questions", [])
    if not qs or target <= 0:
        return
    current = sum(float(q.get("points", 0) or 0) for q in qs)
    if abs(current - target) < 0.01:
        return
    if current <= 0:
        # distribute evenly
        each = round025(target / len(qs)) or 0.25
        for q in qs:
            q["points"] = each
    else:
        factor = target / current
        for q in qs:
            q["points"] = round025(float(q.get("points", 0) or 0) * factor)
    # Fix drift: adjust largest question by the remainder
    new_sum = sum(float(q.get("points", 0) or 0) for q in qs)
    diff = round(target - new_sum, 2)
    if abs(diff) >= 0.01:
        # apply delta to the question with the largest value
        biggest = max(qs, key=lambda q: float(q.get("points", 0) or 0))
        biggest["points"] = round(float(biggest["points"]) + diff, 2)

def normalize_exam(path: Path) -> tuple[float, float]:
    data = json.loads(path.read_text(encoding="utf-8"))
    # Ensure exercise points sum to 20 first (scale them if needed)
    all_ex = [ex for p in data.get("parts", []) for ex in p.get("exercises", [])]
    ex_sum = sum(float(ex.get("points", 0) or 0) for ex in all_ex)
    if ex_sum > 0 and abs(ex_sum - 20) > 0.01:
        factor = 20 / ex_sum
        for ex in all_ex:
            ex["points"] = round025(float(ex["points"]) * factor)
        # drift fix on exercises
        new = sum(float(ex["points"]) for ex in all_ex)
        diff = round(20 - new, 2)
        if abs(diff) >= 0.01:
            biggest = max(all_ex, key=lambda e: float(e.get("points", 0) or 0))
            biggest["points"] = round(float(biggest["points"]) + diff, 2)

    # Now normalize questions within each exercise
    for ex in all_ex:
        normalize_exercise(ex)

    # Update part totals
    for p in data.get("parts", []):
        p["points"] = round(sum(float(ex.get("points", 0) or 0) for ex in p.get("exercises", [])), 2)

    total = sum(float(q.get("points", 0) or 0) for ex in all_ex for q in ex.get("questions", []))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return total, ex_sum

targets = sys.argv[1:] if len(sys.argv) > 1 else None
for d in sorted(ROOT.iterdir()):
    if not d.is_dir():
        continue
    if targets and d.name not in targets:
        continue
    f = d / "exam.json"
    if not f.exists():
        continue
    total, before = normalize_exam(f)
    print(f"{d.name:<20} before_ex_sum={before:<6} → total={total}")
