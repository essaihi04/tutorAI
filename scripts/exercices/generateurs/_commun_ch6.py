# Aides communes aux exercices du ch. 6 (nombres complexes, première partie) : math_ex_ch6_complexes_<n>.py.
# Une donnée changée une fois change partout ; le JSON suit le contrat de .agents/skills/exercices/SKILL.md.
import json

SIM = "/media/simulations/maths/operations-formes-tableau/"


def rep(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}


def qcm(sid, titre, intro, prompt, options, bonne, reactions, enonce_dit):
    """QCM « plus facile » : une réaction préparée pour CHAQUE option (juste ; 1 = indice, 2 = réponse)."""
    assert set(reactions) == {str(i) for i in range(len(options))}
    for k, r in reactions.items():
        assert ("juste" in r) == (int(k) == bonne), (sid, k)
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": prompt}, "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "qcm", "prompt": prompt, "options": options, "correct": bonne, "enonce_dit": enonce_dit},
            "concentration": {"demarrer": "reset", "reponses": {"q": reactions}}}


def vrai_faux(sid, titre, lead, intro, affirmations):
    """affirmations : [(texte, vrai ?, explication)]"""
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "none"}, "speech_text": {"mixed": intro},
            "exercises": [{"type": "vrai_faux", "prompt": "Vrai ou faux ?", "statements": [
                {"text": t, "correct": v, "explanation": e} for t, v, e in affirmations]}],
            "concentration": {"demarrer": "reset"}}


def association(sid, titre, lead, intro, prompt, gauche, droite, couples, retours, bilan):
    """gauche/droite : [(id, texte)] ; retours : {"1-a": (texte, dit)} pour CHAQUE paire ; bilan : (texte, dit)."""
    for g, _ in gauche:
        for d, _ in droite:
            assert f"{g}-{d}" in retours, (sid, g, d)
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "none"}, "speech_text": {"mixed": intro},
            "question": {"type": "association", "prompt": prompt, "association": {
                "gauche": [{"id": i, "texte": t} for i, t in gauche],
                "droite": [{"id": i, "texte": t} for i, t in droite],
                "couples": couples,
                "retours": {k: {"juste": couples.get(k.split("-")[0]) == k.split("-")[1], "texte": t, "dit": d} for k, (t, d) in retours.items()},
                "bilan": {"texte": bilan[0], "dit": bilan[1]}, "melanger": True, "essais": 2}},
            "concentration": {"demarrer": "reset"}}


def anime(sid, titre, lead, vue, caption, parole, centre, pointage):
    """Diapositive d'explication : une simulation EXISTANTE du cours (vue = « fichier.html?vue=… »).
    centre : [(texte écrit, mot)] ; pointage : [(mot, commande|None, paramètres|repère|cible)]."""
    pts = []
    for mot, cmd, p in pointage:
        if cmd == "play_until":
            pts.append({"mot": mot, "commande": "play_until", "parametres": {"moment": p}})
        elif cmd == "set":
            pts.append({"mot": mot, "commande": "set_parameters", "parametres": p})
        elif cmd == "repere":
            pts.append({"mot": mot, "repere": p})
        elif cmd == "centre":
            pts.append({"mot": mot, "cible": f"centre:{p}"})
    return {"id": sid, "slide_type": "simulation", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "simulation", "url": SIM + vue, "caption": caption},
            "speech_text": {"mixed": parole},
            "concentration": {"demarrer": "reset", "centre": [{"texte": t, "mot": m} for t, m in centre], "pointage": pts}}


def question(qid, texte, texte_dit, reponse, clavier, aides, lignes, parole, explication=None, facile=None):
    q = {"id": qid, "texte": texte}
    if texte_dit:
        q["texte_dit"] = texte_dit
    q["reponse"] = reponse
    q["clavier"] = {"aides": clavier[0], "pieges": clavier[1]}
    if aides:
        q["aides"] = [{"texte": t, "dit": d} for t, d in aides]
    q["correction"] = {"lignes": [{"texte": t, "mot": m} for t, m in lignes], "parole": parole}
    if explication:
        q["explication"] = explication
    if facile:
        q["facile"] = facile
    return q


def valeur(grandeur, v, attendu, tol=0.001):
    return {"type": "valeur", "grandeur": grandeur, "valeur": v, "tolerance": tol, "attendu": attendu}


def phrase(attendu):
    return {"type": "phrase", "attendu": attendu}


def plan(titre, legende, points, xs=(-2, 5), ys=(-2, 4), autres=None):
    """Le plan complexe (repère orthonormé direct) avec des points : [(nom, x, y, couleur, pos)]."""
    x0, x1 = xs
    y0, y1 = ys
    el = []
    for nom, x, y, coul, pos in points:
        el.append({"f": "point", "at": [x, y], "couleur": coul, "t": nom, "pos": pos})
    el += autres or []
    return {"type": "courbe", "titre": titre, "legende": legende, "ratio": round((y1 - y0) / (x1 - x0), 2),
            "axes": {"x": {"min": x0, "max": x1, "nom": "axe réel", "graduations": [k for k in range(x0, x1 + 1) if k]},
                     "y": {"min": y0, "max": y1, "nom": "axe imaginaire", "graduations": [k for k in range(y0, y1 + 1) if k]}},
            "elements": el}


def ecrire(ex, chemin):
    ids_ex = {s["id"] for a in ex["explication"]["activities"] for s in a["slides"]}
    ids_fa = {s["id"] for a in ex["facile"]["activities"] for s in a["slides"]}
    for q in ex["enonce"]["questions"]:
        assert q.get("explication") in ids_ex and q.get("facile") in ids_fa, q["id"]
        assert len(q.get("aides", [])) >= 2, q["id"]
    assert len(ex["similaire"]["enonce"]["questions"]) == len(ex["enonce"]["questions"])
    json.dump(ex, open(chemin, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("ok", chemin)


ORIGINE = "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série)."

SOURCES = """Sources comparées (lecture seule, rien n'est copié) :
- vidéos des 10 professeurs : backend/data/curriculum/exploration/operations_formes.json (video_exercices : maths variés
  x9KP-xDiziY correction 2023 N, mostapha maths M6cl9HYFlIA partie 1 ; cas_types, pieges, erreurs_des_videos,
  erreurs_examen, redaction_nationale, a_ne_pas_dire, exclus_hors_programme, renvois.a_la_partie_2) ;
- nationaux 2016-2025 (backend/data/exams/mathematiques/*/exam.json) : 2017 N (b = (1 + i)a, identification cos 5π/12),
  2020 R et 2023 R (puissance réelle par Moivre), 2021 R (alignement par un quotient réel), 2022 R (milieu),
  2023 N (forme trigonométrique, b − d = c, alignement), 2024 N (|a| = √6, b²⁴ réel), 2025 N (ΩA = ΩB = ΩC),
  2025 R (|a| = 1, arg a = 5π/6) ; on garde seulement les types de questions de la partie 1 ;
- séries marocaines 2ᵉ Bac PC BIOF (titres et extraits lus par recherche web le 22/11/2026, les PDF n'étant pas
  joignables depuis l'environnement) : moutamadris « exercices Nombres complexes Partie 1 2bac Sciences Physiques et
  svt » (module, argument, forme trigonométrique), talamidi « nombres complexes 1 série d'exercices » (ensemble des
  M(z) tels que U soit imaginaire pur), dyrassa « Nombres Complexes » série 06 2BAC SP-SVT BIOF (R. Fanidi, Tiznit),
  dreamjob « nombres complexes partie 1 cours exercices corrigés 2bac », moutamadris « exercices nombres complexes 1
  2bac biof » (calculs de modules) ;
- le cours math_ch6_nombres_complexes (simulations operations-formes-tableau) : rien n'est demandé qu'il n'enseigne."""
