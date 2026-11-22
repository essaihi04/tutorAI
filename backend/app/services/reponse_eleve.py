"""Le tuteur réagit à CHAQUE réponse de l'élève aux questions d'une diapositive (mode concentration).

Les questions de la diapositive (`slide.question`) et ses exercices (`slide.exercises`) s'affichent dès la fin
de la voix ; chaque réponse reçoit une réaction dite à voix haute, générée à l'instant (DeepSeek), selon les
gestes du skill `professeur` :
  - juste : on dit précisément ce qui est juste et pourquoi ;
  - fausse, 1er essai : on nomme ce qui est juste, un seul indice ciblé, SANS donner la réponse, et il réessaie ;
  - fausse, 2e essai : la bonne réponse et sa justification ;
  - réponse libre qu'on ne peut pas juger (coupée, ambiguë) : on lui demande de préciser, une seule fois.
Quand la clé est connue (exercices), le verdict est imposé au modèle : il explique, il ne rejuge pas.
"""
from __future__ import annotations

from typing import Any, Optional

from app.services.simulation_reaction import REGLES_VOIX, cle_attendue, lire_json, parole_propre


# Ton du professeur (voix Bodi, choisie le 2026-11-10 pour ses encouragements) : chaleureux, jamais de reproche.
TON = """Ton : chaleureux et sincère, comme un professeur qui croit en lui. Commence par une courte phrase d'encouragement
naturelle en darija, adaptée à la situation, puis l'explication. Exemples de ce registre (ne les recopie pas mot pour mot) :
  - juste : « برافو عليك! », « تبارك الله عليك، هادا هو الجواب. », « شفتي؟ قلت ليك راك قادر عليها! »
  - fausse au 1er essai : « ما تقلقش، راه غلطة كيديروها بزاف ديال التلاميذ. », « قريب بزاف! يالاه نشوفو مجموعين. »
  - fausse encore : « ماشي مشكل، حنا هنا باش نتعلمو. », « خود الوقت ديالك، وغادي تشدها. »
Jamais de reproche ni d'ironie ; ne félicite pas une réponse fausse."""


MATIERES = {"physique": "physique-chimie", "physique-chimie": "physique-chimie", "chimie": "physique-chimie",
            "mathematiques": "mathématiques", "maths": "mathématiques", "svt": "SVT"}


def elements_bareme(question: dict) -> list[dict]:
    """Le barème (`bareme`, en points) réparti par quarts de point sur les éléments attendus (`elements`, ex. les lignes
    de la correction) ; trop d'éléments pour le barème : ils sont regroupés. [] sans barème."""
    try:
        b = float(question.get("bareme") or 0)
    except (TypeError, ValueError):
        return []
    els = [str(e).strip() for e in (question.get("elements") or []) if str(e).strip()][:8]
    if b <= 0:
        return []
    if not els:
        els = ["Réponse complète et justifiée"]
    quarts = max(1, round(b / 0.25))
    n = min(len(els), quarts)
    groupes = [els[i * len(els) // n:(i + 1) * len(els) // n] for i in range(n)]
    parts = [quarts // n + (1 if i < quarts % n else 0) for i in range(n)]
    return [{"element": " ; ".join(g), "sur": q * 0.25} for g, q in zip(groupes, parts)]


def prompt_reponse(diapo: dict, question: dict, reponse: Any, tentative: int, verdict: Optional[bool]) -> str:
    choix = question.get("choix") or []
    lignes_choix = "\n".join(f"  {chr(65 + i)}. {c}" for i, c in enumerate(choix))
    bonne = question.get("bonne")
    cle = ""
    if isinstance(bonne, int) and 0 <= bonne < len(choix):
        cle = f"Bonne réponse : {chr(65 + bonne)}. {choix[bonne]}"
    elif question.get("attendu"):
        cle = cle_attendue(question['attendu'])
    impose = "" if verdict is None else (
        f"VERDICT IMPOSÉ (la clé est connue) : la réponse est {'JUSTE' if verdict else 'FAUSSE'}. Ne le rejuge pas, explique-le.")
    matiere = MATIERES.get(str(question.get("matiere") or "").lower(), "physique-chimie")
    libre = not choix
    if verdict is None:
        consigne_juge = ("Juge d'abord la réponse avec le cours ci-dessus (le fond compte, pas l'orthographe ni les accents). "
                         "« correct » : true si elle est juste et complète, false si elle est fausse ou incomplète, null "
                         "seulement si une réponse LIBRE est trop coupée ou ambiguë pour être jugée.")
        if libre:
            # 22/11/2026 : une réponse au fond juste mais sans la justification demandée n'est ni « juste » ni « fausse »
            consigne_juge += (" « partiel » : true quand le fond est juste mais la réponse incomplète (justification "
                              "demandée absente, une des parties de la question manque) ; alors « correct » vaut false, "
                              "tu dis d'abord clairement ce qui est juste, puis ce qui manque, sans donner ce qui manque.")
    else:
        consigne_juge = "« correct » reprend le verdict imposé."
    if tentative <= 1:
        geste = ("S'il se trompe : nomme ce qui est juste dans sa réponse s'il y a quelque chose, puis donne UN seul "
                 "indice ciblé qui le fait réfléchir (en montrant ce qu'il faut regarder dans l'expérience ou le cours). "
                 "NE DONNE PAS la bonne réponse : il va réessayer. Termine en l'invitant à réessayer.")
    else:
        geste = ("S'il se trompe encore : donne la bonne réponse et sa justification en deux phrases, "
                 "sans le décourager.")
    bar = elements_bareme(question)
    consigne_note = "" if not bar else (
        "Note aussi la réponse comme un correcteur du bac. Barème de la question, élément par élément :\n"
        + "\n".join(f"  {i + 1}. {e['element']} ({e['sur']:g} pt)" for i, e in enumerate(bar))
        + "\nLis la réponse de l'élève mot à mot (souvent sans accents ni apostrophes : « linterieure » = « l'intérieur », "
          "« extrieur » = « extérieur ») et ne lui prête rien qu'il n'a pas écrit. Pour CHAQUE élément, dans l'ordre : « n » = "
          "son numéro ; « cite » = l'extrait EXACT de la réponse de l'élève qui traite cet élément (vide s'il n'en parle pas) ; "
          "« obtenu » = ses points si l'extrait est juste, la moitié s'il est incomplet, 0 s'il est faux ou absent ; « perte » "
          "= en quelques mots ce qui manque ou est faux (vide si tout est obtenu). Note d'abord (« details »), puis écris "
          "« parole » et « ecrit » d'accord avec ta note. Le fond compte, pas l'orthographe.")
    json_note = "" if not bar else ", ".join(f'{{"n": {i + 1}, "cite": "", "obtenu": 0, "perte": ""}}' for i in range(len(bar)))
    return f"""Tu es le professeur de {matiere} d'un élève de 2e Bac PC BIOF au Maroc. Diapositive « {diapo.get('title', '')} ».
Ce que tu viens d'expliquer à voix haute : {str(diapo.get('speech') or '')[:1200]}

Question posée ({question.get('type', 'qcm')}) : {question.get('enonce', '')}
{lignes_choix}
{cle}
Réponse de l'élève (essai n° {tentative}) : {str(reponse)[:500]}
{impose}

{consigne_juge}
S'il a juste : dis précisément ce qui est juste et pourquoi, en une ou deux phrases, sans en faire trop.
{geste}
{TON}

{REGLES_VOIX}
{consigne_note}

Réponds UNIQUEMENT par ce JSON :
{{{('"details": [' + json_note + '], ') if json_note else ''}"correct": true, "partiel": false, "parole": "ce que tu dis (règles de la voix)", "ecrit": "la même chose en français écrit, court, avec les valeurs"}}"""


def reaction_reponse(texte_llm: str, verdict: Optional[bool], question: Optional[dict] = None) -> Optional[dict]:
    d = lire_json(texte_llm)
    if not d:
        return None
    correct = d.get("correct")
    if verdict is not None:
        correct = verdict                       # la clé connue l'emporte toujours sur le modèle
    elif correct is not None and not isinstance(correct, bool):
        return None
    parole = parole_propre(d.get("parole"))
    if not parole:
        return None
    partiel = d.get("partiel") is True and correct is not True
    out = {"correct": correct, "partiel": partiel, "parole": parole, "ecrit": str(d.get("ecrit") or "").strip()[:600]}
    bar = elements_bareme(question or {})
    if bar:
        recu = [r for r in (d.get("details") if isinstance(d.get("details"), list) else []) if isinstance(r, dict)]
        par_n = {}
        for j, r in enumerate(recu):
            try:
                par_n.setdefault(int(r.get("n", j + 1)), r)
            except (TypeError, ValueError):
                par_n.setdefault(j + 1, r)
        details = []
        for i, e in enumerate(bar):
            r = par_n.get(i + 1, {})
            try:
                o = float(r.get("obtenu", 0))
            except (TypeError, ValueError):
                o = 0.0
            o = round(min(max(o, 0.0), e["sur"]) * 4) / 4
            if "cite" in r and not str(r.get("cite") or "").strip():
                o = 0.0                         # l'élève n'en parle pas : pas de points
            if correct is True:
                o = e["sur"]                    # juste et complète : tous les points
            details.append({"element": e["element"], "sur": e["sur"], "obtenu": o,
                            "perte": "" if o >= e["sur"] else str(r.get("perte") or "").strip()[:160]})
        if correct is False and not partiel and sum(x["obtenu"] for x in details) >= sum(x["sur"] for x in details):
            details[-1]["obtenu"] = max(0.0, details[-1]["sur"] - 0.25)   # fausse : jamais la note entière
        out["details"] = details
        out["note"] = sum(x["obtenu"] for x in details)
        out["bareme"] = sum(x["sur"] for x in details)
    return out
