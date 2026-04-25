import json
from pathlib import Path

ROOT = Path("backend/data/exams/mathematiques")
results = []
for d in sorted(ROOT.iterdir()):
    if not d.is_dir():
        continue
    f = d / "exam.json"
    if not f.exists():
        results.append((d.name, "MISSING", 0, 0))
        continue
    try:
        e = json.loads(f.read_text(encoding="utf-8"))
        total = 0.0
        qcount = 0
        for p in e.get("parts", []):
            for ex in p.get("exercises", []):
                total += sum(q.get("points", 0) for q in ex.get("questions", []))
                qcount += len(ex.get("questions", []))
        status = "OK" if abs(total - 20) < 0.01 else f"MISMATCH({total})"
        results.append((d.name, status, total, qcount))
    except Exception as ex:
        results.append((d.name, f"ERR:{type(ex).__name__}", 0, 0))

print(f"{'Folder':<20} {'Status':<18} {'Pts':<8} {'Q':<4}")
print("-" * 55)
for name, status, total, qcount in results:
    print(f"{name:<20} {status:<18} {total:<8} {qcount:<4}")
ok = sum(1 for _, s, _, _ in results if s == "OK")
print(f"\n{ok}/{len(results)} OK")
