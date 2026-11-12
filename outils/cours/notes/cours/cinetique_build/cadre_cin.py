"""Ajoute (ou remplace) la seule clé chapitres.cinetique : relit le fichier, ajoute la clé, réécrit aussitôt."""
import json, copy
from pathlib import Path
REPO = Path("backend/data/curriculum")
ex = json.loads((REPO / "exploration/cinetique.json").read_text(encoding="utf-8"))
fiche = copy.deepcopy(ex["cadre"])
fiche["_note"] = ("Fiche ajoutée le 12 novembre 2026 (routine cloud) depuis exploration/cinetique.json (nationaux PC 2016-2025, "
                  "perimetre.json clé cinetique ; vidéos non auditées). Capacités CIN provisoires, à collationner avec le texte officiel.")
fiche["decisions"] = [d["question"] + " → " + d["proposition"] for d in ex["decisions_utilisateur"]]
p = REPO / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["cinetique"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("chapitres.cinetique :", len(fiche["capacites"]), "capacités,", len(fiche["formules"]), "formules,", len(fiche["hors_cadre"]["mots"]), "mots hors cadre")
