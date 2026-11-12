"""Construit backend/data/courses/phys_ch13_acides_bases.json depuis p1..p4.py (lancer depuis la racine du dépôt).
`python3 outils/cours/notes/cours/acides_bases_build/build.py --garder-reponses` garde réactions, séances, rappels et prédictions déjà posés.
Les compétences (C1…C9) sont lues dans l'exploration (plan.competences)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import PARTIE1, PARTIE2, PARTIE3, PARTIE4
from p2 import PARTIE5, PARTIE6, PARTIE7
from p3 import PARTIE8, PARTIE9, PARTIE10
from p4 import PARTIE11, PARTIE12, BILAN

ACTS = [
 ("ab_partie0", "Ouverture", "explanation", PARTIE1),
 ("ab_partie1", "I. Rappels : couples acide/base, pH, constante d'équilibre", "explanation", PARTIE2),
 ("ab_partie2", "II. L'autoprotolyse de l'eau et le produit ionique Ke", "explanation", PARTIE3),
 ("ab_partie3", "III. Une base dans l'eau : pH et taux d'avancement final", "application", PARTIE4),
 ("ab_partie4", "IV. La constante d'acidité Ka et le pKa", "explanation", PARTIE5),
 ("ab_partie5", "V. Comparer des acides et des bases", "explanation", PARTIE6),
 ("ab_partie6", "VI. La constante d'équilibre d'une réaction acide-base", "application", PARTIE7),
 ("ab_partie7", "VII. Domaines de prédominance et diagramme de distribution", "explanation", PARTIE8),
 ("ab_partie8", "VIII. Les indicateurs colorés", "explanation", PARTIE9),
 ("ab_partie9", "IX. Le dosage acido-basique : réaction, équivalence, courbe", "explanation", PARTIE10),
 ("ab_partie10", "X. Exploiter une courbe de dosage", "application", PARTIE11),
 ("ab_partie11", "XI. Sujets du national", "evaluation", PARTIE12),
 ("ab_bilan", "XII. Bilan du chapitre", "evaluation", BILAN),
]
ex = json.loads(Path("backend/data/curriculum/exploration/acides_bases.json").read_text(encoding="utf-8"))
COMP = [(c["id"], c["verbe"], c.get("cadre_ids", []), c.get("dit", "")) for c in ex["plan"]["competences"]]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit}
         for cid, lab, cad, dit in COMP]
deck = {
 "id": "phys_ch13_acides_bases", "stable_id": "phys_ch13_acides_bases",
 "title": "Transformations liées aux réactions acide-base", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["transformations liées aux réactions acide-base", "réactions acido-basiques", "réactions acide-base", "produit ionique de l'eau",
                  "autoprotolyse de l'eau", "constante d'acidité", "Ka", "pKa", "Ke", "domaine de prédominance", "diagramme de distribution",
                  "indicateur coloré", "zone de virage", "dosage acido-basique", "titrage acido-basique", "dosage pH-métrique", "équivalence",
                  "demi-équivalence", "méthode des tangentes"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : autoprotolyse de l'eau et produit ionique Ke, solutions acides, neutres, basiques, pH et taux d'avancement final d'une base, constante d'acidité Ka et pKa (couples de l'eau, couple d'une base), comparaison des acides et des bases, constante K = Ka₁/Ka₂ d'une réaction acide-base, pH = pKa + log([A⁻]/[AH]), domaines de prédominance et diagramme de distribution, indicateurs colorés, puis le dosage acido-basique : réaction de dosage, équivalence C_A·V_A = C_B·V_BE, courbe pH = f(V), méthode des tangentes et courbe dérivée, pH à l'équivalence, demi-équivalence pH = pKa, choix de l'indicateur, dosage conductimétrique, avec des sujets du national.",
             "cover_alt": "Une burette au-dessus d'un bécher sur agitateur, un pH-mètre et la courbe de dosage à la craie avec ses deux tangentes parallèles et le point d'équivalence E",
             "essential_topics": ["Ke = [H₃O⁺]·[HO⁻]", "pKe = −log Ke = 14", "Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq", "pKa = −log Ka", "K = Ka₁/Ka₂",
                                  "pH = pKa + log([A⁻]_éq/[AH]_éq)", "C_A·V_A = C_B·V_BE", "pH = pKa à V_B = V_BE/2",
                                  "l'indicateur choisi a une zone de virage qui contient pH_E"]},
 "note": "Cours 13 de physique-chimie (chimie), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/acides_bases.json ; vidéos non auditées, nationaux 2016-2025) et le contrat des simulations (outils/cours/notes/cours/acides_bases_contrat_simulations.md, chimie/acides-bases-tableau/). Le dosage acido-basique (clé dosage de perimetre.json) est la partie finale de ce cours. Brouillon : voix à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path("backend/data/courses/phys_ch13_acides_bases.json")
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
