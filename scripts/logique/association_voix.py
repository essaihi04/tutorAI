"""Met à jour <deck>_voix.json après la conversion d'une association (19 novembre 2026), sans toucher aux autres pistes :
retire les pistes des diapositives converties qui n'existent plus (réactions des anciens QCM, démonstrations, énoncés,
diapositives retirées), met à jour le texte des pistes changées, ajoute les retours dits de chaque paire et le bilan
(`<diapo>__<cle>_assoc_<g>-<d>`, `<diapo>__<cle>_assoc_bilan`, type `reaction`).
Usage : python -X utf8 scripts/logique/association_voix.py <deck> <diapo> [<diapo> …]   (diapos : gardées ET retirées)"""
import json, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(R / "scripts/voix")]
from pistes_cours import pistes  # noqa: E402

deck, diapos = sys.argv[1], sys.argv[2:]
m = json.load(open(R / f"backend/data/courses/en_attente/{deck}.json", encoding="utf-8"))
chemin = R / f"backend/data/curriculum/architecture/{deck}_voix.json"
voix = json.load(open(chemin, encoding="utf-8"))
TYPE = {"mixed": "diapositive", "demos": "demonstration"}


def touche(i: str) -> bool:
    return any(i == d or i.startswith(d + "__") or i == f"enonce_{d}_q" for d in diapos)


actuelles = {}
for d, i, t, poser in pistes(m):
    if not touche(i):
        continue
    obj = next((c.cell_contents for c in (poser.__closure__ or ()) if isinstance(c.cell_contents, dict)), {})
    if d == "mixed":
        deja = bool(((obj.get("audio") or {}).get("mixed") or {}).get("url"))
    else:
        deja = bool(obj.get("enonce_audio" if i.startswith("enonce_") else "audio"))
    if not deja:
        actuelles[i] = {"type": "enonce" if i.startswith("enonce_") else TYPE.get(d, "reaction"), "id": i, "texte": t}

garde, vus, retirees, changees = [], set(), [], []
for p in voix["pistes"]:
    if not touche(p["id"]):
        garde.append(p)
    elif p["id"] in actuelles:
        n = actuelles[p["id"]]
        if n["texte"] != p["texte"]:
            changees.append(p["id"])
        garde.append({**p, "texte": n["texte"]})
        vus.add(p["id"])
    else:
        retirees.append(p["id"])
ajoutees = [p for i, p in actuelles.items() if i not in vus]
voix["pistes"] = garde + ajoutees
chemin.write_bytes(json.dumps(voix, ensure_ascii=False, indent=1).encode("utf-8"))
print(f"{deck} : {len(retirees)} retirées, {len(changees)} changées, {len(ajoutees)} ajoutées → {len(voix['pistes'])} pistes")
print("  changées :", ", ".join(changees))
print("  ajoutées :", ", ".join(p["id"] for p in ajoutees))
