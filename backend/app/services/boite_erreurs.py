"""La boîte à erreurs : ce que l'élève a raté et n'a pas encore reconquis.

Une erreur ne sort de la boîte que par une NOUVELLE réussite : une autre
question sur la même notion, réussie plus tard. Relire la correction, ou
réussir la question jumelle posée dans la foulée de la réponse, ne prouve pas
que la notion tient — l'élève a encore l'explication sous les yeux. C'est la
différence entre « exercice terminé avec aide » et « notion reconquise ».

L'idée vient du tuteur de Duolingo (octobre 2026) : son serveur ne retire une
erreur de la boîte que si la séance contenait un exercice du même générateur.

Aucune table : la boîte se reconstruit depuis `student_answer_history`, comme
la mémoire des tactiques. Cette table n'a pas d'identifiant de séance ; un
délai minimal entre l'erreur et la réussite en tient lieu.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

#: Une réussite plus proche que cela de l'erreur est la question jumelle de la
#: même séance : elle ne vide pas la boîte.
DELAI_AVANT_RECONQUETE = timedelta(hours=1)
#: Des notions trop vagues pour qu'on sache quoi faire revoir.
NOTIONS_VAGUES = {"", "général", "general", "conversation"}


@dataclass
class Erreur:
    sujet: str
    notion: str
    question: str
    reponse_eleve: str
    quand: datetime


@dataclass
class NotionARevoir:
    sujet: str
    notion: str
    erreurs: list[Erreur] = field(default_factory=list)

    @property
    def plus_ancienne(self) -> datetime:
        return min(e.quand for e in self.erreurs)


def _date(valeur) -> Optional[datetime]:
    if isinstance(valeur, datetime):
        return valeur
    if not valeur:
        return None
    try:
        return datetime.fromisoformat(str(valeur).replace("Z", "+00:00"))
    except ValueError:
        return None


def _meme_question(a: str, b: str) -> bool:
    normaliser = lambda t: re.sub(r"\W+", " ", (t or "").lower()).strip()
    return normaliser(a) == normaliser(b)


def depuis_historique(lignes: Optional[list]) -> list[Erreur]:
    """Les erreurs encore ouvertes, de la plus ancienne à la plus récente."""
    reponses = []
    for ligne in lignes or []:
        if not isinstance(ligne, dict):
            continue
        quand = _date(ligne.get("created_at"))
        notion = str(ligne.get("topic") or "").strip()
        if quand is None or notion.lower() in NOTIONS_VAGUES:
            continue
        reponses.append((quand, ligne, notion))
    reponses.sort(key=lambda r: r[0])

    ouvertes: list[Erreur] = []
    for quand, ligne, notion in reponses:
        sujet = str(ligne.get("subject") or "").strip()
        question = str(ligne.get("question_content") or "")
        if not ligne.get("is_correct"):
            ouvertes.append(Erreur(sujet, notion, question, str(ligne.get("student_answer") or ""), quand))
            continue
        ouvertes = [
            e for e in ouvertes
            if not (
                e.sujet == sujet and e.notion == notion
                and quand - e.quand >= DELAI_AVANT_RECONQUETE
                and not _meme_question(e.question, question)
            )
        ]
    return ouvertes


def a_revoir(erreurs: list[Erreur], limite: int = 3) -> list[NotionARevoir]:
    """Les notions à reprendre d'abord : les plus ratées, puis les plus anciennes."""
    par_notion: dict[tuple[str, str], NotionARevoir] = {}
    for e in erreurs:
        par_notion.setdefault((e.sujet, e.notion), NotionARevoir(e.sujet, e.notion)).erreurs.append(e)
    notions = sorted(par_notion.values(), key=lambda n: (-len(n.erreurs), n.plus_ancienne))
    return notions[:limite]
