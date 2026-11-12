"""Assemble methode_blocs/ajouts/phys_ch6_dipole_RC.json depuis blocs_s1..s4.json (séances, prédictions) et les rappels du plan
de l'exploration (plan.competences[].rappels). Lancer depuis la racine du dépôt, puis :
  python3 outils/cours/notes/cours/methode_blocs/blocs.py base      backend/data/courses/phys_ch6_dipole_RC.json   (une fois)
  python3 outils/cours/notes/cours/methode_blocs/blocs.py appliquer backend/data/courses/phys_ch6_dipole_RC.json outils/cours/notes/cours/methode_blocs/ajouts/phys_ch6_dipole_RC.json
"""
import json
from pathlib import Path
ICI = Path(__file__).parent
ex = json.loads(Path("backend/data/curriculum/exploration/dipole_RC.json").read_text(encoding="utf-8"))
seances, preds = [], []
for n in range(1, 5):
    b = json.loads((ICI / f"blocs_s{n}.json").read_text(encoding="utf-8"))
    seances.append(b["seance"]); preds += b.get("predictions", [])
rappels = {}
for c in ex["plan"]["competences"]:
    rs = []
    for r in c["rappels"]:
        r = {k: v for k, v in r.items() if k in ("id", "type", "prompt", "options", "correct", "attendu")}
        if r["id"] == "C2_r4":   # ne jamais écrire la fausse formule « I₀ = q/C » (a_ne_pas_dire) : même idée, affirmation juste
            r = {"id": "C2_r4", "type": "vrai_faux", "prompt": "Avec un générateur idéal de courant, la charge vaut q = I₀·t.", "correct": True}
        rs.append(r)
    rappels[c["id"]] = rs
out = Path("outils/cours/notes/cours/methode_blocs/ajouts/phys_ch6_dipole_RC.json")
out.write_text(json.dumps({"seances": seances, "rappels": rappels, "predictions": preds}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(seances), "séances ;", sum(len(s["blocs"]) for s in seances), "blocs ;", sum(len(v) for v in rappels.values()), "rappels ;", len(preds), "prédictions")
