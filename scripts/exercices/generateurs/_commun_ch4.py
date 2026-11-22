# Aides communes aux générateurs des exercices du ch. 4 (fonctions primitives) : mêmes formes que le pilote
# math_ex_ch1_continuite_1.py (rep, qcm_facile, diapositive de simulation), pour écrire chaque exercice sans répéter
# la structure. Aucune donnée d'exercice ici.
import json

SIM = "/media/simulations/maths/primitives-tableau/"
COURS = "math_ch4_primitives"
ORIGINE = "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série)."


def rep(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}


def valeur(grandeur, v, attendu, tol=0.001):
    return {"type": "valeur", "grandeur": grandeur, "valeur": v, "tolerance": tol, "attendu": attendu}


def phrase(attendu):
    return {"type": "phrase", "attendu": attendu}


def aide(texte, dit):
    return {"texte": texte, "dit": dit}


def question(qid, texte, texte_dit, reponse, clavier, aides, lignes, parole, ex=None, fa=None):
    q = {"id": qid, "texte": texte}
    if texte_dit:
        q["texte_dit"] = texte_dit
    q["reponse"] = reponse
    q["clavier"] = {"aides": clavier[0], "pieges": clavier[1]}
    if aides:
        q["aides"] = [aide(t, d) for t, d in aides]
    q["correction"] = {"lignes": [{"texte": t, "mot": m} for t, m in lignes], "parole": parole}
    if ex:
        q["explication"] = ex
    if fa:
        q["facile"] = fa
    return q


def q_sim(qid, texte, reponse, clavier, lignes, parole):
    """Question de l'exercice semblable : réponse, clavier, correction seulement."""
    return {"id": qid, "texte": texte, "reponse": reponse, "clavier": {"aides": clavier[0], "pieges": clavier[1]},
            "correction": {"lignes": [{"texte": t, "mot": m} for t, m in lignes], "parole": parole}}


def sim(sid, titre, lead, vue, caption, mixed, centre, pointage):
    """Diapositive d'explication animée sur une simulation EXISTANTE du cours (vue = « fichier.html?vue=… »)."""
    return {"id": sid, "slide_type": "simulation", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "simulation", "url": SIM + vue, "caption": caption},
            "speech_text": {"mixed": mixed},
            "concentration": {"demarrer": "reset", "centre": [{"texte": t, "mot": m} for t, m in centre],
                              "pointage": pointage}}


def pu(mot, moment):
    return {"mot": mot, "commande": "play_until", "parametres": {"moment": moment}}


def sp(mot, **params):
    return {"mot": mot, "commande": "set_parameters", "parametres": params}


def rp(mot, repere):
    return {"mot": mot, "repere": repere}


def ce(mot, i):
    return {"mot": mot, "cible": f"centre:{i}"}


def qcm(sid, titre, intro, prompt, enonce_dit, options, bonne, reactions):
    """options : textes affichés ; bonne : index juste ; reactions : {i: rep} pour la bonne,
    {i: (rep_indice, rep_reponse)} pour chaque fausse."""
    q = {}
    for i in range(len(options)):
        r = reactions[i]
        q[str(i)] = {"juste": r} if i == bonne else {"1": r[0], "2": r[1]}
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": prompt}, "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "qcm", "prompt": prompt, "options": options, "correct": bonne, "enonce_dit": enonce_dit},
            "concentration": {"demarrer": "reset", "reponses": {"q": q}}}


def vrai_faux(sid, titre, lead, intro, affirmations):
    """affirmations : [(texte, juste, explication)]"""
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "none"}, "speech_text": {"mixed": intro},
            "exercises": [{"type": "vrai_faux", "prompt": "Vrai ou faux ?", "statements": [
                {"text": t, "correct": c, "explanation": e} for t, c, e in affirmations]}],
            "concentration": {"demarrer": "reset"}}


def association(sid, titre, lead, intro, prompt, gauche, droite, couples, retours, bilan):
    """gauche/droite : [(id, texte)] ; retours : {"1-a": (juste, texte, dit)} ; bilan : (texte, dit)"""
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "none"}, "speech_text": {"mixed": intro},
            "question": {"type": "association", "prompt": prompt, "association": {
                "gauche": [{"id": i, "texte": t} for i, t in gauche],
                "droite": [{"id": i, "texte": t} for i, t in droite],
                "couples": couples,
                "retours": {k: {"juste": j, "texte": t, "dit": d} for k, (j, t, d) in retours.items()},
                "bilan": {"texte": bilan[0], "dit": bilan[1]}, "melanger": True, "essais": 2}},
            "concentration": {"demarrer": "reset"}}


def courbe(titre, legende, x, y, elements):
    """x, y : (min, max, graduations)"""
    return {"type": "courbe", "titre": titre, "legende": legende,
            "axes": {"x": {"min": x[0], "max": x[1], "nom": "x", "graduations": x[2]},
                     "y": {"min": y[0], "max": y[1], "nom": "y", "graduations": y[2]}},
            "elements": elements}


def exercice(id_, titre, niveau, duree, competences, intro, intro_dit, figures, donnees, questions,
             explications, faciles, sim_titre, sim_intro, sim_intro_dit, sim_figures, sim_donnees, sim_questions):
    return {
        "id": id_, "type": "exercice", "version": 1, "status": "published",
        "matiere": "mathematiques", "chapitre": "primitives", "cours": COURS,
        "titre": titre, "niveau": niveau, "duree_min": duree, "origine": ORIGINE, "competences": competences,
        "enonce": {"intro": intro, "intro_dit": intro_dit, "figures": figures, "donnees": donnees, "questions": questions},
        "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": explications}]},
        "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": faciles}]},
        "similaire": {"id": id_ + "_b", "titre": sim_titre,
                      "enonce": {"intro": sim_intro, "intro_dit": sim_intro_dit, "figures": sim_figures,
                                 "donnees": sim_donnees, "questions": sim_questions}},
    }


def ecrire(ex, chemin):
    json.dump(ex, open(chemin, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("ok", chemin)


SOURCES = """Sources comparées (lecture seule, rien de copié) :
- backend/data/curriculum/exploration/primitives.json : cas_types (vérifier une primitive 11 sujets/20, ensemble des
  primitives, primitive avec condition, u′uⁿ, u′/u², u′/√u, dérivée d'un produit), pieges, erreurs_examen,
  redaction_nationale, exclus_hors_programme (pas d'Arctan, de changement de variable, de ln/exp, d'intégrale),
  a_ne_pas_dire ; vidéos d'exercices des profs : FA8JqAIvyIA (Ait Lahbib, huit fonctions), N8jDoK4COvc (Prof fati),
  SOsZjm5vQL0 (Timath, correction de série), Kihb9h-EXOI (maths variés).
- Nationaux 2016-2025 (backend/data/exams/mathematiques/*/exam.json) : « Montrer / Vérifier que H est une primitive
  de h sur I » (2017 N, 2017 R, 2018 N, 2018 R, 2019 N, 2019 R, 2020 N, 2020 R, 2022 N, 2023 N, 2025 N), rédaction en
  trois lignes (dérivable, H′(x) = … = h(x), conclusion).
- Séries marocaines 2ᵉ Bac PC/SVT BIOF repérées en ligne (titres et extraits de recherche seulement : les sites ne
  répondent pas depuis le conteneur) : moutamadris « exercices Fonctions primitives 2bac Sciences Physiques et svt 1 »
  (Atmani, classées par formes u′uⁿ, u′/(2√u)) et « … 2 » (dérivée puis primitive, primitive avec F(1) = 0) ;
  talamidi « fonctions primitives série d'exercices 2 » (par formes) et « exercices non corrigés 1 » ; monstremath
  « Cours 04 Fonctions primitives 2 BAC Sciences pc et svt modèle 2 » (applications du cours) ; alloschool
  (cours + exercices).
- Cours math_ch4_primitives (diapositives, simulations primitives-tableau) : seules les notions enseignées sont demandées."""
