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

from app.services.simulation_reaction import REGLES_VOIX, lire_json, parole_propre


# Ton du professeur (voix Bodi, choisie le 2026-11-10 pour ses encouragements) : chaleureux, jamais de reproche.
TON = """Ton : chaleureux et sincère, comme un professeur qui croit en lui. Commence par une courte phrase d'encouragement
naturelle en darija, adaptée à la situation, puis l'explication. Exemples de ce registre (ne les recopie pas mot pour mot) :
  - juste : « برافو عليك! », « تبارك الله عليك، هادا هو الجواب. », « شفتي؟ قلت ليك راك قادر عليها! »
  - fausse au 1er essai : « ما تقلقش، راه غلطة كيديروها بزاف ديال التلاميذ. », « قريب بزاف! يالاه نشوفو مجموعين. »
  - fausse encore : « ماشي مشكل، حنا هنا باش نتعلمو. », « خود الوقت ديالك، وغادي تشدها. »
Jamais de reproche ni d'ironie ; ne félicite pas une réponse fausse."""


def prompt_reponse(diapo: dict, question: dict, reponse: Any, tentative: int, verdict: Optional[bool]) -> str:
    choix = question.get("choix") or []
    lignes_choix = "\n".join(f"  {chr(65 + i)}. {c}" for i, c in enumerate(choix))
    bonne = question.get("bonne")
    cle = ""
    if isinstance(bonne, int) and 0 <= bonne < len(choix):
        cle = f"Bonne réponse : {chr(65 + bonne)}. {choix[bonne]}"
    elif question.get("attendu"):
        cle = f"Réponse attendue : {question['attendu']}"
    impose = "" if verdict is None else (
        f"VERDICT IMPOSÉ (la clé est connue) : la réponse est {'JUSTE' if verdict else 'FAUSSE'}. Ne le rejuge pas, explique-le.")
    if verdict is None:
        consigne_juge = ("Juge d'abord la réponse avec le cours ci-dessus (le fond compte, pas l'orthographe). "
                         "« correct » : true si elle est juste, false si elle est fausse, null seulement si une réponse "
                         "LIBRE est trop coupée ou ambiguë pour être jugée.")
    else:
        consigne_juge = "« correct » reprend le verdict imposé."
    if tentative <= 1:
        geste = ("S'il se trompe : nomme ce qui est juste dans sa réponse s'il y a quelque chose, puis donne UN seul "
                 "indice ciblé qui le fait réfléchir (en montrant ce qu'il faut regarder dans l'expérience ou le cours). "
                 "NE DONNE PAS la bonne réponse : il va réessayer. Termine en l'invitant à réessayer.")
    else:
        geste = ("S'il se trompe encore : donne la bonne réponse et sa justification en deux phrases, "
                 "sans le décourager.")
    return f"""Tu es le professeur de physique d'un élève de 2e Bac PC BIOF au Maroc. Diapositive « {diapo.get('title', '')} ».
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

Réponds UNIQUEMENT par ce JSON :
{{"correct": true, "parole": "ce que tu dis (règles de la voix)", "ecrit": "la même chose en français écrit, court, avec les valeurs"}}"""


def reaction_reponse(texte_llm: str, verdict: Optional[bool]) -> Optional[dict]:
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
    return {"correct": correct, "parole": parole, "ecrit": str(d.get("ecrit") or "").strip()[:600]}
