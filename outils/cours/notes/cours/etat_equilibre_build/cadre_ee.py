"""Ajoute (ou remplace) la seule clé chapitres.etat_equilibre : relit le fichier, ajoute la clé, réécrit aussitôt.
Lancer depuis la racine du dépôt : python3 outils/cours/notes/cours/etat_equilibre_build/cadre_ee.py"""
import json, copy
from pathlib import Path
REPO = Path("backend/data/curriculum")
ex = json.loads((REPO / "exploration/etat_equilibre.json").read_text(encoding="utf-8"))
fiche = copy.deepcopy(ex["cadre"])
fiche["_note"] = ("Fiche ajoutée le 12 novembre 2026 (routine cloud) depuis exploration/etat_equilibre.json (nationaux PC 2016-2025, "
                  "perimetre.json clés acides_bases et piles_electrolyse ; vidéos non auditées). Capacités EE provisoires, à collationner avec le texte officiel.")
fiche["decisions"] = [d["question"] + " → " + d["proposition"] for d in ex["decisions_utilisateur"]]
p = REPO / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["etat_equilibre"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("chapitres.etat_equilibre :", len(fiche["capacites"]), "capacités,", len(fiche["formules"]), "formules,",
      len(fiche["hors_cadre"]["mots"]), "mots hors cadre")
