"""Construit backend/data/courses/phys_ch9_transformations_lentes_rapides.json depuis p1..p4.py (lancer depuis la racine du dépôt).
`python3 outils/cours/notes/cours/transformations_lentes_rapides_build/build.py --garder-reponses` garde réactions, séances, rappels et prédictions déjà posés."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import PARTIE1, PARTIE2, PARTIE3, PARTIE4
from p2 import PARTIE5, PARTIE6, PARTIE7
from p3 import PARTIE8, PARTIE9, PARTIE10, BILAN

ACTS = [
 ("tl_partie0", "Ouverture", "explanation", PARTIE1),
 ("tl_partie1", "I. Oxydants et réducteurs", "explanation", PARTIE2),
 ("tl_partie2", "II. Les demi-équations électroniques", "explanation", PARTIE3),
 ("tl_partie3", "III. L'équation d'oxydoréduction", "application", PARTIE4),
 ("tl_partie4", "IV. Transformations rapides et lentes", "explanation", PARTIE5),
 ("tl_partie5", "V. Voir, classer, titrer", "application", PARTIE6),
 ("tl_partie6", "VI. La température, facteur cinétique", "explanation", PARTIE7),
 ("tl_partie7", "VII. La concentration des réactifs", "explanation", PARTIE8),
 ("tl_partie8", "VIII. Trempe, vie quotidienne et catalyseur", "explanation", PARTIE9),
 ("tl_partie9", "IX. Deux sujets du national", "evaluation", PARTIE10),
 ("tl_bilan", "X. Bilan du chapitre", "evaluation", BILAN),
]
COMP = [
 ("C1", "Définir oxydant, réducteur, couple Ox/Red, oxydation et réduction ; reconnaître l'oxydant et le réducteur d'une réaction", ["TLR1"],
  "reconnaître l'oxydant et le réducteur"),
 ("C2", "Écrire la demi-équation électronique d'un couple Ox/Red en milieu acide", ["TLR2"], "écrire une demi-équation électronique"),
 ("C3", "Écrire l'équation d'une réaction d'oxydoréduction à partir des deux couples", ["TLR3"], "écrire l'équation d'oxydoréduction"),
 ("C4", "Distinguer une transformation rapide d'une transformation lente et citer des exemples", ["TLR4"], "distinguer une transformation rapide d'une lente"),
 ("C5", "Montrer que la température est un facteur cinétique et expliquer son effet", ["TLR5", "TLR6"], "montrer l'effet de la température"),
 ("C6", "Montrer que la concentration initiale des réactifs est un facteur cinétique", ["TLR5", "TLR6"], "montrer l'effet de la concentration"),
 ("C7", "Exploiter des expériences et des courbes comparées ; connaître la trempe, le catalyseur et les applications des facteurs cinétiques", ["TLR6", "TLR7"],
  "exploiter des courbes, connaître la trempe et le catalyseur"),
]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit}
         for cid, lab, cad, dit in COMP]
deck = {
 "id": "phys_ch9_transformations_lentes_rapides", "stable_id": "phys_ch9_transformations_lentes_rapides",
 "title": "Transformations lentes et transformations rapides", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["transformations lentes et transformations rapides", "transformations lentes et rapides", "facteurs cinétiques",
                  "facteurs cinetiques", "oxydoréduction", "oxydo-réduction", "demi-équation", "couple oxydant réducteur", "trempe", "catalyseur"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : oxydants, réducteurs et couples Ox/Red, demi-équations électroniques en milieu acide, équation d'une réaction d'oxydoréduction, transformations rapides et lentes, facteurs cinétiques (température, concentration des réactifs, catalyseur), trempe et applications, avec les nationaux 2017 R et 2025 N.",
             "cover_alt": "Deux béchers à la craie : l'un se décolore aussitôt, l'autre brunit lentement",
             "essential_topics": ["Ox + n e⁻ ⇌ Red", "MnO₄⁻ + 8H⁺ + 5e⁻ ⇌ Mn²⁺ + 4H₂O", "Équation : même nombre d'électrons, aucun électron dans le bilan",
                                  "Rapide : achevée dès le mélange ; lente : de quelques secondes à des heures",
                                  "Température, concentration des réactifs, catalyseur : plus rapide, même état final", "Trempe : eau glacée pour bloquer"]},
 "note": "Cours 9 de physique-chimie (chimie), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/transformations_lentes_rapides.json ; vidéos non auditées, nationaux 2016-2025) et le contrat des simulations (outils/cours/notes/cours/transformations_lentes_rapides_contrat_simulations.md, chimie/transformations-lentes-rapides-tableau/). Brouillon : voix à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path("backend/data/courses/phys_ch9_transformations_lentes_rapides.json")
if out.exists() and "--garder-reponses" in sys.argv:
    old = json.loads(out.read_text(encoding="utf-8"))
    oldr = {s["id"]: s.get("concentration", {}).get("reponses") for a in old["activities"] for s in a["slides"]}
    for s in slides:
        if oldr.get(s["id"]): s["concentration"]["reponses"] = oldr[s["id"]]
    if "seances" in old: deck["seances"] = old["seances"]
    oc = {c["id"]: c for c in old.get("competences", [])}
    for c in comps:
        if oc.get(c["id"], {}).get("rappels"): c["rappels"] = oc[c["id"]]["rappels"]
    oq = {s["id"]: (s.get("question") or {}) for a in old["activities"] for s in a["slides"]}
    for s in slides:
        if s.get("question") and oq.get(s["id"], {}).get("prediction"): s["question"]["prediction"] = True
out.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(slides), "diapositives ;", sum(1 for s in slides if s.get("question")), "questions ;",
      sum(1 for s in slides if (s.get("question") or {}).get("prediction")), "prédictions ;", sum(len(s.get("exercises", [])) for s in slides), "exercices")
for c in comps: print(c["id"], len(c["slide_ids"]))
