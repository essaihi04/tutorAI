import json
from pathlib import Path

p = Path("backend/data/exams/physique/2025-normale/exam.json")
d = json.loads(p.read_text(encoding="utf-8-sig"))

for ex_idx, ex in enumerate(d["parts"][0]["exercises"]):
    print(f"=== Exercice {ex_idx+1} — {ex['name'][:60]}")
    print(f"   points (déclarés) : {ex['points']}")
    qpts = sum(q['points'] for q in ex['questions'])
    print(f"   points (somme questions) : {qpts}")
    docs = ex.get("documents", [])
    doc_ids = {x["id"] for x in docs}
    print(f"   {len(docs)} document(s) attaché(s) : {sorted(doc_ids)}")
    # Check missing files
    base = p.parent
    for x in docs:
        src = base / x["src"]
        flag = "OK" if src.exists() else "MISSING"
        print(f"     [{flag}] {x['id']} -> {x['src']}")
    # Check question refs
    bad = []
    for q in ex["questions"]:
        for ref in q.get("documents", []):
            if ref not in doc_ids:
                bad.append((q["number"], ref))
    if bad:
        print(f"   ⚠️ refs orphelines : {bad}")

total = sum(e["points"] for e in d["parts"][0]["exercises"])
print(f"\nTotal général : {total}")
