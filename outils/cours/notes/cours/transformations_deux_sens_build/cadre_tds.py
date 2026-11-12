"""Ajoute (ou remplace) la seule clé chapitres.transformations_deux_sens : relit le fichier, ajoute la clé, réécrit aussitôt.
Lancer depuis la racine du dépôt : python3 outils/cours/notes/cours/transformations_deux_sens_build/cadre_tds.py"""
import json, copy
from pathlib import Path
REPO = Path("backend/data/curriculum")
ex = json.loads((REPO / "exploration/transformations_deux_sens.json").read_text(encoding="utf-8"))
fiche = copy.deepcopy(ex["cadre"])
fiche["_note"] = ("Fiche ajoutée le 12 novembre 2026 (routine cloud) depuis exploration/transformations_deux_sens.json (nationaux PC 2016-2025, "
                  "perimetre.json clé acides_bases ; vidéos non auditées). Capacités TD provisoires, à collationner avec le texte officiel.")
fiche["decisions"] = [d["question"] + " → " + d["proposition"] for d in ex["decisions_utilisateur"]]
p = REPO / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["transformations_deux_sens"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("chapitres.transformations_deux_sens :", len(fiche["capacites"]), "capacités,", len(fiche["formules"]), "formules,",
      len(fiche["hors_cadre"]["mots"]), "mots hors cadre")
