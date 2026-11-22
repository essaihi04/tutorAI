# Outils communs aux exercices du ch. 5 (fonctions logarithmiques) : math_ex_ch5_ln_1 … _7.
# Chaque générateur construit son JSON avec ces fonctions, puis l'écrit (même forme que math_ex_ch1_continuite_1.py).
#
# Sources comparées pour les sept exercices (lecture seule, aucun texte copié) :
# - exploration backend/data/curriculum/exploration/fonctions_ln.json : 10 professeurs (Driss DOTCOM, Prof fati, maths variés,
#   Aderdour, Math_houara, Ghazouani, MedBrahmi, Moussaoui, LowDiscovery, biadmostafa) ; video_exercices po2C4bjZYM8 (correction
#   2021 N) et H5c4Zugm9Tc (problème type national) ; cas_types, pieges, erreurs_des_videos (−3 au lieu de +6 de Driss, tableau
#   commencé à −∞, x = 1 gardé alors que ln x est au dénominateur), erreurs_examen, redaction_nationale, a_ne_pas_dire,
#   exclus_hors_programme (pas de log de base a, pas d'exponentielle comme fonction, pas d'intégrale).
# - nationaux du dépôt backend/data/exams/mathematiques : problèmes à ln de 2016 R (g = 2/x − 1 + 2 ln x), 2017 N
#   (g = x² + x − 2 + 2 ln x ; f = x + (1 − 2/x) ln x), 2018 R, 2019 N (x + ½ − ln x + ½(ln x)²), 2020 N ex. 3
#   (2√x − 2 − ln x), 2021 N (2x ln x − 2x), 2021 R ex. 3 (x + ln x), 2022 R (x⁴(ln x − 1)²), 2023 N, 2023 R, 2024 N,
#   2024 R, 2025 N (x − (ln x)²/x), 2017 R (plus petit n) : types de questions, rédaction, barème ; aucune de ces fonctions
#   n'est reprise.
# - séries marocaines 2ᵉ Bac PC/SVT BIOF repérées en ligne (moteur de recherche ; le réseau de la session ne laisse pas ouvrir
#   moutamadris.ma ni sigmaths.net, les autres PDF ont été vus par leurs extraits) : Talamidi « fonctions logarithmiques,
#   exercices non corrigés 4 » (partie A : fonction auxiliaire g, puis f), Talamidi « cours et exercices corrigés » (propriétés,
#   variations et limites, équations et inéquations), moutamadris « exercices fonctions logarithmiques 2bac SP et SVT 1 »,
#   alloschool (série de M. Cheddadi, 2 Bac SPC-SVT), Atmani Najib 2BAC BIOF (inégalités par fonction auxiliaire),
#   dreamjob.ma « étude fonction logarithme exercices corrigés », série Fatihi n° 2 (étude de g sur ]0 ; +∞[) : situations
#   classiques et niveau attendu ; nos fonctions et nos données sont écrites pour Moalim.
import json, sys

ORIGINE = "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série)."
SIM = "/media/simulations/maths/ln-tableau/"


def rep(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}


def debut(seg, n=4):
    """Les n premiers mots d'un segment : le « mot » où une ligne s'écrit."""
    return " ".join(seg.split()[:n])


def corr(lignes, intro=""):
    """lignes = [(texte écrit, segment dit)] → {lignes, parole} ; chaque mot est le début de son segment."""
    parole = " ".join(([intro] if intro else []) + [s for _, s in lignes])
    return {"lignes": [{"texte": t, "mot": debut(s)} for t, s in lignes], "parole": parole}


def aide(texte, dit):
    return {"texte": texte, "dit": dit}


def question(id, texte, texte_dit, reponse, clavier, aides, correction, ex, fa):
    return {"id": id, "texte": texte, "texte_dit": texte_dit, "reponse": reponse, "clavier": clavier,
            "aides": aides, "correction": correction, "explication": ex, "facile": fa}


def qsim(id, texte, reponse, clavier, correction):
    return {"id": id, "texte": texte, "reponse": reponse, "clavier": clavier, "correction": correction}


def phrase(attendu):
    return {"type": "phrase", "attendu": attendu}


def valeur(grandeur, v, attendu, tol=0.001):
    return {"type": "valeur", "grandeur": grandeur, "valeur": v, "tolerance": tol, "attendu": attendu}


def clav(aides, pieges):
    return {"aides": aides, "pieges": pieges}


def sim(sid, titre, lead, vue, caption, parts):
    """Diapo d'explication : parts = [(segment dit, [commandes])] ; commandes : ("m", moment) play_until,
    ("c", texte écrit) ligne du centre, ("r", repère) pointage d'un repère, ("p", {params}) set_parameters."""
    mixed = " ".join(s for s, _ in parts)
    centre, pointage = [], []
    for s, cmds in parts:
        mot = debut(s)
        for c in cmds:
            if c[0] == "m":
                pointage.append({"mot": mot, "commande": "play_until", "parametres": {"moment": c[1]}})
            elif c[0] == "p":
                pointage.append({"mot": mot, "commande": "set_parameters", "parametres": c[1]})
            elif c[0] == "r":
                pointage.append({"mot": mot, "repere": c[1]})
            elif c[0] == "c":
                centre.append({"texte": c[1], "mot": mot})
                pointage.append({"mot": mot, "cible": f"centre:{len(centre) - 1}"})
    return {"id": sid, "slide_type": "simulation", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "simulation", "url": SIM + vue, "caption": caption},
            "speech_text": {"mixed": mixed},
            "concentration": {"demarrer": "reset", "centre": centre, "pointage": pointage}}


def qcm(sid, titre, intro, prompt, options, bonne, reactions, enonce_dit):
    """reactions[i] = rep juste (pour la bonne) ou (rep indice, rep réponse) (pour une fausse)."""
    q = {}
    for i, r in enumerate(reactions):
        q[str(i)] = {"juste": r} if i == bonne else {"1": r[0], "2": r[1]}
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": prompt}, "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "qcm", "prompt": prompt, "options": options, "correct": bonne, "enonce_dit": enonce_dit},
            "concentration": {"demarrer": "reset", "reponses": {"q": q}}}


def vrai_faux(sid, titre, lead, intro, prompt, affirmations):
    """affirmations = [(texte, vrai ?, explication)]"""
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "none"}, "speech_text": {"mixed": intro},
            "exercises": [{"type": "vrai_faux", "prompt": prompt, "statements": [
                {"text": t, "correct": v, "explanation": e} for t, v, e in affirmations]}],
            "concentration": {"demarrer": "reset"}}


def association(sid, titre, lead, intro, prompt, gauche, droite, couples, retours, bilan):
    """gauche/droite = [(id, texte)] ; retours = {"1-a": (texte, dit)} pour CHAQUE paire ; bilan = (texte, dit)."""
    r = {k: {"juste": couples.get(k.split("-")[0]) == k.split("-")[1], "texte": t, "dit": d} for k, (t, d) in retours.items()}
    for g, _ in gauche:
        for d, _ in droite:
            assert f"{g}-{d}" in r, f"retour manquant {g}-{d}"
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "none"}, "speech_text": {"mixed": intro},
            "question": {"type": "association", "prompt": prompt, "association": {
                "gauche": [{"id": i, "texte": t} for i, t in gauche], "droite": [{"id": i, "texte": t} for i, t in droite],
                "couples": couples, "retours": r, "bilan": {"texte": bilan[0], "dit": bilan[1]}, "melanger": True, "essais": 2}},
            "concentration": {"demarrer": "reset"}}


def courbe_fig(titre, legende, expr, xmin, xmax, ymin, ymax, gx, gy, nom="(C)", de=None, a=None, extra=()):
    return {"type": "courbe", "titre": titre, "legende": legende,
            "axes": {"x": {"min": xmin, "max": xmax, "nom": "x", "graduations": gx},
                     "y": {"min": ymin, "max": ymax, "nom": "y", "graduations": gy}},
            "elements": [{"f": "courbe", "expr": expr, "de": xmin if de is None else de, "a": xmax if a is None else a,
                          "couleur": "cyan", "texte": nom, "texte_x": (xmax if a is None else a) - 0.8, "pos": "no"}, *extra]}


def exercice(id, titre, niveau, duree, competences, enonce, ex_slides, fa_slides, sim_titre, sim_enonce):
    ids = {s["id"] for s in ex_slides} | {s["id"] for s in fa_slides}
    assert len(ids) == len(ex_slides) + len(fa_slides), "ids de diapos en double"
    for q in enonce["questions"]:
        assert q["explication"] in ids and q["facile"] in ids, q["id"]
    assert len(sim_enonce["questions"]) == len(enonce["questions"])
    return {"id": id, "type": "exercice", "version": 1, "status": "published", "matiere": "mathematiques",
            "chapitre": "fonctions_ln", "cours": "math_ch5_fonctions_ln", "titre": titre, "niveau": niveau, "duree_min": duree,
            "origine": ORIGINE, "competences": competences, "enonce": enonce,
            "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": ex_slides}]},
            "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": fa_slides}]},
            "similaire": {"id": id + "_b", "titre": sim_titre, "enonce": sim_enonce}}


def ecrire(ex):
    json.dump(ex, open(sys.argv[1], "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("ok", sys.argv[1])
