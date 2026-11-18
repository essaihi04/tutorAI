"""Liste des pistes à mettre en voix après une nouvelle logique : <deck>_voix.json (skill logique-de-cours, § 5).
Usage : python -X utf8 scripts/logique/pistes_a_voix.py <deck> <cours_avant.json>
Une piste est à faire quand son texte n'existait pas dans le cours d'avant (une réaction ou une démonstration
déplacée garde sa voix : son url voyage avec elle), ou quand une diapositive n'a pas de voix.
Les questions sans réactions préparées sont listées à part (preparer_reponses.py items, sur le VPS)."""
import json, os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..")
sys.path.insert(0, os.path.join(RACINE, "scripts", "voix"))
from pistes_cours import pistes

deck, avant = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
m = json.load(open(os.path.join(RACINE, "backend/data/courses/en_attente", deck + ".json"), encoding="utf-8"))
vus = {(t, i, x) for t, i, x, _ in pistes(avant)}
textes_vus = {(t, x) for t, i, x, _ in pistes(avant)}   # une réaction déplacée garde sa voix (url dans l'objet)
S = {s["id"]: s for a in m["activities"] for s in a["slides"]}
voix_posees = set()          # textes dont l'objet porte déjà sa piste (réaction, démonstration, énoncé déplacés)


def _parcourir(o):
    if isinstance(o, dict):
        if o.get("audio") and isinstance(o.get("parole"), str):
            voix_posees.add(o["parole"].strip())
        if o.get("enonce_audio") and isinstance(o.get("enonce_dit"), str):
            voix_posees.add(o["enonce_dit"].strip())
        for v in o.values():
            _parcourir(v)
    elif isinstance(o, list):
        for v in o:
            _parcourir(v)


_parcourir(m["activities"])
sortie = []
for t, i, x, _ in pistes(m):
    sans_voix = t == "mixed" and not (S.get(i, {}).get("audio") or {}).get("mixed")
    deplacee = t != "mixed" and ((t, x) in textes_vus or x in voix_posees)
    if ((t, i, x) not in vus and not deplacee) or sans_voix:
        sortie.append({"type": t, "id": i, "texte": x})
reactions = []
for s in S.values():
    rep = (s.get("concentration") or {}).get("reponses") or {}
    if s.get("question") and not rep.get("q"):
        reactions.append(f"{s['id']}/q")
    for k, _ in enumerate(s.get("exercises") or []):
        if not rep.get(f"e{k}"):
            reactions.append(f"{s['id']}/e{k}")
p = os.path.join(RACINE, "backend/data/curriculum/architecture", deck + "_voix.json")
json.dump({"deck": deck, "fichier": f"backend/data/courses/en_attente/{deck}.json",
           "note": "Pistes dont le texte est nouveau ou changé (voix Bodi à faire sur le VPS), et questions dont les "
                   "réactions préparées sont à écrire (preparer_reponses.py items, puis gen_reponses_vps.py).",
           "pistes": sortie, "reactions_a_preparer": reactions},
          open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{deck} : {len(sortie)} pistes à mettre en voix ({sum(1 for x in sortie if x['type']=='mixed')} diapositives), "
      f"{len(reactions)} questions sans réactions préparées")
