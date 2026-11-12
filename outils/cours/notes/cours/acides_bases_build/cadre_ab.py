"""Ajoute (ou remplace) la seule clé chapitres.acides_bases : relit le fichier, ajoute la clé, réécrit aussitôt.
Lancer depuis la racine du dépôt : python3 outils/cours/notes/cours/acides_bases_build/cadre_ab.py"""
import json, copy
from pathlib import Path
REPO = Path("backend/data/curriculum")
ex = json.loads((REPO / "exploration/acides_bases.json").read_text(encoding="utf-8"))
fiche = copy.deepcopy(ex["cadre"])
fiche["_note"] = ("Fiche ajoutée le 12 novembre 2026 (routine cloud) depuis exploration/acides_bases.json (nationaux PC 2016-2025, "
                  "perimetre.json clés acides_bases et dosage ; vidéos non auditées). Capacités AB provisoires, à collationner avec le texte officiel.")
fiche["decisions"] = [d["question"] + " → " + d["proposition"] for d in ex["decisions_utilisateur"]]
p = REPO / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["acides_bases"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("chapitres.acides_bases :", len(fiche["capacites"]), "capacités,", len(fiche["formules"]), "formules,",
      len(fiche["hors_cadre"]["mots"]), "mots hors cadre")
