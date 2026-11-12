"""Assemble l'exploration transformations_lentes_rapides (explo_a + explo_b + nationaux) et l'écrit.
Lancer depuis la racine du dépôt : python3 outils/cours/notes/cours/transformations_lentes_rapides_build/explo.py"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from explo_a import *
from explo_b import *

CAS_TYPES = [
 {"cas": "lente et limitée", "mots": "« Donner deux caractéristiques de cette transformation »", "methode": "lente : elle dure (courbe qui monte pendant des minutes ou des heures) ; limitée : x_f < x_max (chapitre suivant)", "points": "0,25-0,5", "frequence": "4 fois (estérification, hydrolyse)"},
 {"cas": "rôle du catalyseur (acide sulfurique)", "mots": "« Quel est le rôle de l'acide sulfurique ? »", "methode": "catalyseur : il accélère la transformation sans modifier l'état final", "points": "0,25-0,5", "frequence": "2 fois"},
 {"cas": "associer une courbe à une condition", "mots": "« Indiquer, en justifiant, la courbe qui correspond à… (catalyseur, θ₂ > θ₁) »", "methode": "la courbe qui atteint son palier le plus tôt (la plus raide au début) ; même palier ; justifier par la durée ou t₁/₂", "points": "0,5", "frequence": "2 fois (2023 N, 2025 N)"},
 {"cas": "état final inchangé", "mots": "« Vrai ou faux : x_f est le même dans les trois expériences »", "methode": "vrai : température et catalyseur changent la durée, pas l'état final (mêmes quantités initiales)", "points": "0,75", "frequence": "1 fois (2025 N)"},
 {"cas": "citer des facteurs cinétiques", "mots": "« Proposer deux facteurs cinétiques pour accélérer… »", "methode": "élever la température ; ajouter un catalyseur (ou augmenter la concentration d'un réactif)", "points": "0,5", "frequence": "1 fois (2017 R)"},
 {"cas": "trempe", "mots": "« Objectif de l'eau glacée avant le dosage »", "methode": "refroidir brusquement pour bloquer la transformation et doser la quantité présente à l'instant t", "points": "0,25", "frequence": "1 fois (2017 R)"},
 {"cas": "chauffage à reflux", "mots": "« Intérêt du chauffage à reflux »", "methode": "chauffer accélère (facteur température) sans perte de matière", "points": "0,5", "frequence": "1 fois (2017 N) ; choix du montage 1 fois (2018 R)"},
 {"cas": "vrai/faux de cours", "mots": "« La concentration initiale des réactifs est un facteur cinétique »", "methode": "vrai", "points": "0,25", "frequence": "1 fois (2024 N)"},
 {"cas": "demi-équations et équation (parties pile / électrolyse)", "mots": "« Écrire les demi-équations… l'équation bilan »", "methode": "Ox + n e⁻ ⇌ Red ; même nombre d'électrons ; O₂/H₂O seul couple avec H⁺", "points": "0,25-0,75", "frequence": "16 questions dans 14 sessions (chapitre piles, compté à part)"},
]

ERREURS_EXAMEN = [
 {"erreur": "choisir la courbe au palier le plus haut au lieu de celle qui atteint son palier le plus tôt", "geste": "même palier : on compare les durées (ou t₁/₂)", "source": "2023 N, 2025 N"},
 {"erreur": "« courbe C₁ » sans justification", "geste": "écrire : l'état final est atteint plus tôt (t₁/₂ plus petit), donc la transformation est plus rapide", "source": "2023 N"},
 {"erreur": "ne citer qu'un facteur quand on en demande deux, ou citer « l'agitation »", "geste": "deux facteurs du cours : température, catalyseur, concentration des réactifs", "source": "2017 R"},
 {"erreur": "en 2025 N, ne citer qu'une cause pour l'expérience 3", "geste": "deux facteurs à la fois : température plus élevée ET catalyseur", "source": "2025 N"},
 {"erreur": "eau glacée « pour refroidir » sans dire le but", "geste": "« pour bloquer (arrêter) la transformation avant le dosage »", "source": "2017 R"},
 {"erreur": "électrons du mauvais côté, charges non équilibrées", "geste": "électrons du côté de l'oxydant ; vérifier la charge des deux côtés", "source": "parties piles"},
]

CONSEILS = [
 "justifier toujours une association courbe ↔ condition par la durée (ou t₁/₂) et dire que l'état final est le même",
 "écrire « catalyseur : accélère la transformation sans modifier l'état final » (phrase du barème)",
 "trempe : dire le geste (eau glacée) ET le but (bloquer la transformation)",
 "demi-équation : vérifier les charges avant de passer à la suite",
]

REDACTION = {
 "_note": "lignes attendues d'après les corrigés du dépôt (erreurs du dépôt relevées dans nationaux.md § 4)",
 "courbe_catalyseur": ["les deux courbes ont le même état final", "C₁ atteint son état final plus tôt (t₁/₂ plus petit)", "donc C₁ correspond à l'expérience avec catalyseur"],
 "trempe": ["on verse le prélèvement dans l'eau glacée", "le refroidissement brusque (et la dilution) bloque la transformation", "on dose la quantité présente à cet instant"],
 "equation": ["demi-équation de réduction de l'oxydant", "demi-équation d'oxydation du réducteur", "× pour égaliser les électrons", "équation bilan sans électrons, éléments et charges conservés"],
}

DECISIONS = [
 {"question": "Faut-il un vrai cours d'oxydoréduction (10 diapositives) alors que le national ne le demande que dans les parties piles ?", "constat": "16 questions de demi-équations dans 14 sessions, mais toutes dans les piles/électrolyse ; le programme met le rappel d'oxydoréduction en tête de ce chapitre", "proposition": "oui : 10 diapositives (x1-x10), avec les couples du programme (permanganate, eau oxygénée, iodure, peroxodisulfate, thiosulfate) ; ils resservent au suivi temporel et aux piles"},
 {"question": "Le catalyseur dans ce chapitre ?", "constat": "question de facteur la plus posée (6 questions, 5 sessions, toujours H₂SO₄ dans l'estérification) ; perimetre.json le met dans cinetique", "proposition": "oui : t3 (définition, expérience) et t4 (courbe avec/sans, 2023 N), sans types de catalyse"},
 {"question": "« Chocs efficaces » ?", "constat": "perimetre.json le met hors programme, mais le vrai/faux de 2024 N l'emploie (réponse vrai)", "proposition": "non dit dans le cours (règle du périmètre) ; on dit « les entités se rencontrent plus souvent » ; à revoir si l'utilisateur veut suivre 2024 N"},
 {"question": "Exemples de réactions", "constat": "les nationaux prennent l'estérification et la saponification (chapitres suivants) ; les exemples classiques (I⁻ + H₂O₂…) n'y tombent jamais", "proposition": "garder les exemples classiques pour voir (couleurs) et renvoyer à l'estérification par les deux nationaux n1 (2025 N) et n2 (2017 R)"},
 {"question": "Clé du chapitre et identifiant du cours", "constat": "transformations_lentes_rapides absent de perimetre.json (la clé cinetique couvre les deux chapitres)", "proposition": "fiche du cadre chapitres.transformations_lentes_rapides ; perimetre.json NON modifié ; cours phys_ch9_transformations_lentes_rapides (ordre 9 du programme)"},
 {"question": "Flèches", "constat": "les corrigés écrivent ⇌, ⇄ ou =", "proposition": "⇌ pour les demi-équations, → pour l'équation de la réaction"},
]

LIMITES = [
 "vidéos non auditées (YouTube bloqué depuis le cloud) : 10 audits à faire depuis le PC avant validation",
 "texte officiel du cadre de référence non relu mot à mot : TLR1-TLR7 provisoires",
 "valeurs des simulations choisies pour l'œil (durées 3 fois plus courtes à 40 °C) : pas une loi, à dire comme un ordre de grandeur",
]

ex = {**ENTETE, "sources": SOURCES, "comparaison": COMPARAISON, "cadre": CADRE, "insistances": INSISTANCES,
      "valeurs_reperes": VALEURS_REPERES, "cas_types": CAS_TYPES, "pieges": PIEGES, "erreurs_examen": ERREURS_EXAMEN,
      "conseils": CONSEILS, "analogies_validees": ANALOGIES, "a_ne_pas_dire": A_NE_PAS_DIRE, "exclus_hors_programme": EXCLUS,
      "questions_eleves": QUESTIONS_ELEVES, "commentaires_eleves": COMMENTAIRES, "notions_complexes": NOTIONS,
      "cours_existant": COURS_EXISTANT, "visuels": VISUELS, "regles_des_simulations": REGLES_SIMULATIONS,
      "redaction_nationale": REDACTION, "plan": PLAN, "renvois": RENVOIS, "decisions_utilisateur": DECISIONS,
      "limites_de_l_exploration": LIMITES}

# vérifications : chaque capacité dans le plan, ids, séances
caps = {}
comp_caps = {c["id"]: c["cadre_ids"] for c in COMPETENCES}
for d in DIAPOS:
    for c in d["competences"]:
        for k in comp_caps[c]:
            caps.setdefault(k, []).append(d["id"])
ids = [d["id"] for d in DIAPOS]
assert len(ids) == len(set(ids)) == 36, len(ids)
assert [x for s in SEANCES for b in s["blocs"] for x in b] == ids
assert set(caps) == {c["id"] for c in CADRE["capacites"]}, set(caps)
for c in COMPETENCES:
    assert 3 <= len(c["rappels"]) <= 4 and len({r["type"] for r in c["rappels"]}) >= 2
ex["verification"] = {"dix_professeurs": "non : aucune vidéo (YouTube bloqué depuis le cloud) ; remplacés par les 20 nationaux",
                      "capacites_du_cadre_dans_le_plan": caps, "toutes_les_capacites": True, "diapositives": len(ids),
                      "predictions": sum(d["prediction"] for d in DIAPOS)}
out = Path("backend/data/curriculum/exploration/transformations_lentes_rapides.json")
out.write_text(json.dumps(ex, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("écrit", out, len(ids), "diapositives,", ex["verification"]["predictions"], "prédictions")
