"""Reconstruit frontend/public/media/exercices/index.json (la liste lue par la page /exercices).
Chaque fiche : id, matière, chapitre, cours (+ son titre), titre, niveau, durée, nombre de questions, barème total
estimé, et la première figure de l'énoncé (miniature de la carte, 22 novembre 2026).
Usage (dans le dépôt) : python -X utf8 scripts/exercices/index.py   (MOALIM_COURS : autre dossier des cours)"""
import json, glob, os
from pathlib import Path
R = Path(__file__).resolve().parents[2]
D = R / "frontend" / "public" / "media" / "exercices"
COURS = Path(os.environ.get("MOALIM_COURS") or R / "backend" / "data" / "courses")
ORDRE = {"facile": 0, "moyen": 1, "difficile": 2}


def titre_du_cours(cid, memo={}):
    if cid not in memo:
        try:
            memo[cid] = json.load(open(COURS / f"{cid}.json", encoding="utf-8")).get("title") or cid
        except (OSError, ValueError):
            memo[cid] = cid
    return memo[cid]


def points(q):
    # même estimation que pointsDe() du front (types.ts)
    if isinstance(q.get("points"), (int, float)) and q["points"] > 0:
        return q["points"]
    n = len((q.get("correction") or {}).get("lignes") or []) or 1
    return 0.5 if n <= 2 else 0.75 if n == 3 else 1 if n <= 5 else 1.25


L = []
for f in sorted(glob.glob(str(D / "*.json"))):
    if f.endswith("index.json"):
        continue
    e = json.load(open(f, encoding="utf-8"))
    qs = e["enonce"]["questions"]
    figs = e["enonce"].get("figures") or []
    L.append({k: e.get(k) for k in ("id", "matiere", "chapitre", "cours", "titre", "niveau", "duree_min")}
             | {"cours_titre": titre_du_cours(e.get("cours")), "questions": len(qs),
                "bareme": sum(points(q) for q in qs), "figure": figs[0] if figs else None})
import re
num = lambda c: int((re.search(r"_ch(\d+)_", str(c or "")) or [0, 0])[1])
L.sort(key=lambda x: (x["matiere"] or "", num(x["cours"]), ORDRE.get(x["niveau"] or "", 9), x["id"]))
open(D / "index.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"version": 2, "exercices": L}, ensure_ascii=False, indent=1))
print(len(L), "exercices")
