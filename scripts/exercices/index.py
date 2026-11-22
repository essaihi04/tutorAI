"""Reconstruit frontend/public/media/exercices/index.json (la liste lue par la page /exercices).
Usage (dans le dépôt) : python -X utf8 scripts/exercices/index.py"""
import json, glob
from pathlib import Path
D = Path(__file__).resolve().parents[2] / "frontend" / "public" / "media" / "exercices"
L = []
for f in sorted(glob.glob(str(D / "*.json"))):
    if f.endswith("index.json"):
        continue
    e = json.load(open(f, encoding="utf-8"))
    L.append({k: e.get(k) for k in ("id", "matiere", "chapitre", "cours", "titre", "niveau", "duree_min")} | {"questions": len(e["enonce"]["questions"])})
open(D / "index.json", "w", encoding="utf-8", newline="
").write(json.dumps({"version": 1, "exercices": L}, ensure_ascii=False, indent=1))
print(len(L), "exercices")
