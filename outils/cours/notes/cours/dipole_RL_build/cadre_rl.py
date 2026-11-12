"""Ajoute (ou remplace) la seule clé chapitres.dipole_RL : relit le fichier, ajoute la clé, réécrit aussitôt."""
import json, copy
from pathlib import Path
REPO = Path("backend/data/curriculum")
ex = json.loads((REPO / "exploration/dipole_RL.json").read_text(encoding="utf-8"))
fiche = copy.deepcopy(ex["cadre"])
fiche["_note"] = ("Fiche ajoutée le 12 novembre 2026 (routine cloud) depuis exploration/dipole_RL.json (nationaux PC 2016-2025, perimetre.json ; "
                  "vidéos non auditées). Capacités RL1 à RL8 provisoires, à collationner avec le texte officiel.")
fiche["decisions"] = [d["question"] + " → " + d["proposition"] for d in ex["decisions_utilisateur"]]
p = REPO / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["dipole_RL"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("chapitres.dipole_RL :", len(fiche["capacites"]), "capacités,", len(fiche["formules"]), "formules,", len(fiche["hors_cadre"]["mots"]), "mots hors cadre")
