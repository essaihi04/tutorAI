"""Find the canonical PC + Math taxonomy — recursively surface any text
containing 'Domaine', 'Chapitre', or weight percentages."""
import json, re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "cours 2bac pc" / "cadres de references 2BAC PC"

def find_topics(obj, path=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            hits += find_topics(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, x in enumerate(obj):
            hits += find_topics(x, f"{path}[{i}]")
    elif isinstance(obj, str):
        low = obj.lower()
        # Heuristics: anything with domaine/chapitre, OR a percentage pattern, OR section headers
        if re.search(r"\bdomaine\b|\bchapitre\b|\b\d{1,2}\s*%", low) or re.search(r"^(chapitre|domaine|partie|th[eè]me)\s", low):
            hits.append((path, obj[:220]))
    return hits


for fname, label in [
    ("cadre-de-reference-de-l-examen-national-physique-chimie-spc-2.json", "PC"),
    ("cadre-de-reference-de-l-examen-national-maths-sciences-experimentales.json", "MATH"),
]:
    print(f"\n{'=' * 80}\n{label}\n{'=' * 80}")
    d = json.loads((BASE / fname).read_text(encoding="utf-8"))
    hits = find_topics(d)
    seen = set()
    for path, txt in hits:
        key = txt[:80]
        if key in seen:
            continue
        seen.add(key)
        print(f"  [{path}]")
        print(f"    {txt}")
