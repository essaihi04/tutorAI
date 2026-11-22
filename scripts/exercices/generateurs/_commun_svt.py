# Aides communes aux générateurs d'exercices (formats des pilotes : svt_ex_ch1_levures_1, phys_ex_ch1_corde_1).
# Usage dans un générateur : `from _commun import rep, qcm_facile, vrai_faux, association, ecrire`
# (le dossier du générateur est sur sys.path quand on lance `python scripts/exercices/generateurs/<id>.py <json>`).
import json


def rep(parole, ecrit):
    """Réaction préparée : ce que dit le tuteur (darija + français) et ce qu'il écrit."""
    return {"parole": parole, "ecrit": ecrit}


def qcm_facile(sid, titre, intro, prompt, options, bonne, reactions, enonce_dit):
    """QCM de la version facile. `reactions` : {"<i>": {"juste": rep(...)} pour la bonne,
    {"1": rep(1er essai faux), "2": rep(2e essai faux, donne la réponse)} pour chaque fausse} (professeur règle 20)."""
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": prompt}, "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "qcm", "prompt": prompt, "options": options, "correct": bonne, "enonce_dit": enonce_dit},
            "concentration": {"demarrer": "reset", "reponses": {"q": reactions}}}


def vrai_faux(sid, titre, lead, intro, affirmations):
    """`affirmations` : [(texte, vrai: bool, explication), ...]."""
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead}, "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "exercises": [{"type": "vrai_faux", "prompt": "Vrai ou faux ?",
                           "statements": [{"text": t, "correct": v, "explanation": x} for t, v, x in affirmations]}],
            "concentration": {"demarrer": "reset"}}


def association(sid, titre, lead, intro, prompt, gauche, droite, couples, retours, bilan):
    """Association (professeur règle 47). gauche/droite : [(id, texte)] ; couples {"1": "a"} ;
    retours {"1-a": (juste, texte, dit)} pour CHAQUE paire possible ; bilan (texte, dit)."""
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "none"}, "speech_text": {"mixed": intro},
            "question": {"type": "association", "prompt": prompt,
                         "association": {"gauche": [{"id": i, "texte": t} for i, t in gauche],
                                         "droite": [{"id": i, "texte": t} for i, t in droite],
                                         "couples": couples,
                                         "retours": {k: {"juste": j, "texte": t, "dit": d} for k, (j, t, d) in retours.items()},
                                         "bilan": {"texte": bilan[0], "dit": bilan[1]},
                                         "melanger": True, "essais": 2}},
            "concentration": {"demarrer": "reset"}}


def ecrire(ex, chemin):
    json.dump(ex, open(chemin, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("ok", chemin)
