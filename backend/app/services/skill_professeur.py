"""Le geste de prof, tour par tour.

Le tuteur savait QUOI enseigner (le scénario), AVEC QUOI (le routeur de
surfaces) et COMMENT expliquer à cet élève (les tactiques). Il ne savait pas
QUAND : quand expliquer, quand s'arrêter, quand questionner, quand laisser
chercher, quand donner la réponse. Un vrai prof décide cela à chaque tour,
et c'est ce qui fait qu'on le suit.

Les règles viennent d'un professeur de dix ans de métier (octobre 2026) :

  • Expliquer en UN bloc complet (5 à 8 phrases), sans s'interrompre, puis
    s'arrêter et poser UNE question. Jamais de monologue au-delà, jamais deux
    questions.
  • Vérifier la compréhension par une REFORMULATION : l'élève explique avec
    ses mots, comme à un camarade ; ensuite seulement une question courte
    d'application.
  • Devant une erreur : nommer ce qui est juste, donner UN indice ciblé,
    laisser réessayer. La réponse n'est donnée qu'après DEUX essais, avec son
    explication, puis une question jumelle pour vérifier.
  • Chaleureux et exigeant : féliciter précisément ce qui est mérité, nommer
    ce qui manque sans détour, ne jamais avancer sur de l'approximatif.
  • Une réponse qu'on ne peut pas trancher (ambiguë, coupée, mal transcrite)
    n'est ni juste ni fausse : on demande de préciser, sans indice et sans
    compter d'essai. Une seule fois : au tour suivant, on tranche.

Le module ne lit ni base ni réseau. Il tient trois faits — une question
est-elle en attente, combien d'essais l'élève a-t-il faits, combien de tours
ont passé — et rend une consigne. Le jugement « correct / partiel / faux / incertain »
appartient au modèle, qui le déclare en tête de réponse dans une balise
``<eval>`` retirée avant l'affichage ; le module le lit pour compter les
essais. Pas d'état parallèle : ce qui n'est pas dans la réponse n'existe pas.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

EVALUATIONS: tuple[str, ...] = ("correct", "partiel", "faux", "incertain", "aucune")
#: Essais accordés avant de donner la réponse.
ESSAIS_AVANT_REPONSE = 2
#: Demandes de précision accordées avant de devoir trancher.
PRECISIONS_AVANT_JUGEMENT = 1
BALISE_EVAL = re.compile(r"\s*\**\s*<eval>\s*([a-zA-Zé]+)\s*</eval>\s*\**\s*", re.IGNORECASE)
_SANS_ACCENT = {"é": "e"}
_DEMANDE_EXPLICATION = re.compile(
    r"\b(expli|c['’]est quoi|qu['’]est[- ]ce|comment|pourquoi|d[ée]finition|je ne comprends|"
    r"chno|kifach|3lach|ach|شنو|كيفاش|علاش|اشرح)",
    re.IGNORECASE,
)
_DEMANDE_EXERCICE = re.compile(r"\b(exercice|entra[iî]ne|exo|tmrin|تمرين|question bac|qcm)\b", re.IGNORECASE)
_NE_SAIT_PAS = re.compile(
    r"\b(je ne sais pas|je sais pas|aucune id[ée]e|ma 3reft|ma3reftch|معرفتش|مافهمتش|je ne comprends pas)\b",
    re.IGNORECASE,
)

STYLE = (
    "Style : chaleureux et exigeant — félicite précisément ce qui est juste et pourquoi, "
    "nomme ce qui manque sans détour, et n'avance jamais sur de l'approximatif. "
    "Pas de flatterie : « presque » seulement si c'est vrai."
)
RYTHME = (
    "Rythme : quand tu expliques, fais-le en UN bloc complet de 5 à 8 phrases, sans t'interrompre ; "
    "puis arrête-toi et pose UNE seule question — jamais deux. Termine toujours par cette question "
    "(ou par une consigne de manipulation précise si tu pilotes une scène)."
)
REFORMULATION = (
    "La vérification après une explication est une REFORMULATION : « Explique-moi ça avec tes mots, "
    "comme à un camarade. » Ensuite seulement, une question courte d'application."
)


@dataclass
class SkillProfesseur:
    """Trois faits, une consigne par tour."""

    question_en_attente: bool = False
    tentatives: int = 0
    #: Demandes de précision d'affilée sur la question en attente.
    incertains: int = 0
    tours: int = 0
    reussites: int = 0
    derniere_evaluation: str = "aucune"

    # ------------------------------------------------------------ avant que le modèle parle
    def consigne(self, demande: str, phase: str = "") -> str:
        """La consigne du tour, à ajouter au prompt système."""
        demande = (demande or "").strip()
        lignes: list[str] = []
        if self.question_en_attente:
            essai = self.tentatives + 1
            lignes.append(
                f"Situation : tu attends la réponse à ta question (essai n°{essai} de l'élève)."
            )
            lignes.append(
                "Si c'est correct : félicite précisément (ce qui est juste et pourquoi), puis "
                + ("passe à la suite avec une question courte d'application." if essai == 1
                   else "passe à la suite avec une question courte d'application, sans revenir sur les essais manqués.")
            )
            if essai < ESSAIS_AVANT_REPONSE + 1 and essai <= ESSAIS_AVANT_REPONSE:
                lignes.append(
                    "Si c'est partiel : dis ce qui est juste, nomme exactement ce qui manque, donne UN indice "
                    "ciblé et repose la même question. Ne donne pas la réponse."
                    if essai < ESSAIS_AVANT_REPONSE else
                    "Si c'est partiel ou faux : c'était le dernier essai — donne maintenant la réponse complète "
                    "et son explication en un bloc, puis pose une question jumelle (même idée, autre exemple) "
                    "pour vérifier."
                )
                if essai < ESSAIS_AVANT_REPONSE:
                    lignes.append(
                        "Si c'est faux : ne donne pas la réponse. Nomme ce qui est juste s'il y a quelque chose, "
                        "pose le doigt sur la confusion, donne UN indice ciblé et repose la question."
                    )
            if self.incertains < PRECISIONS_AVANT_JUGEMENT:
                lignes.append(
                    "Si tu ne peux pas trancher (réponse ambiguë, coupée, mal transcrite) : ne juge pas et ne "
                    "donne pas d'indice ; demande-lui de préciser en UNE question courte (« tu veux dire… ? »). "
                    "Évaluation « incertain »."
                )
            else:
                lignes.append(
                    "Tu lui as déjà demandé de préciser : cette fois tranche (correct, partiel ou faux), "
                    "n'emploie pas « incertain »."
                )
            if _NE_SAIT_PAS.search(demande):
                lignes.append(
                    "L'élève dit ne pas savoir : compte cela comme un essai « faux », rassure en une phrase et "
                    "donne l'indice ; au dernier essai, donne la réponse et son explication."
                )
            else:
                lignes.append(
                    "S'il pose une autre question au lieu de répondre : réponds-lui brièvement, puis ramène-le "
                    "à ta question en attente (évaluation « aucune »)."
                )
        elif self.tours == 0:
            lignes.append("Situation : premier tour. Salue, annonce le plan en une phrase, puis commence par "
                          "une question d'accroche liée à son vécu. Pas de nouvelle notion encore.")
        elif _DEMANDE_EXERCICE.search(demande):
            lignes.append("Situation : l'élève veut s'entraîner. Pose UN exercice adapté à la phase, sans la "
                          "solution, et attends sa réponse.")
        elif _DEMANDE_EXPLICATION.search(demande) or phase in ("explanation", "exploration"):
            lignes.append("Situation : une notion à expliquer. Explique en un bloc complet : l'idée, un exemple "
                          "concret, la formule et le sens de chaque terme s'il y en a une ; puis arrête-toi et "
                          "demande une reformulation avec ses mots.")
        else:
            lignes.append("Situation : échange libre. Réponds, puis termine par une question qui fait avancer "
                          "l'objectif de la phase.")
        return (
            "\n\n[GESTE DE PROF — ce tour]\n"
            "Commence ta réponse par la balise <eval>…</eval> : « correct », « partiel », « faux » ou "
            "« incertain » si l'élève vient de répondre à ta question, « aucune » sinon. Elle est retirée avant l'affichage ; ne la "
            "commente jamais.\n"
            + "\n".join(f"- {ligne}" for ligne in lignes)
            + f"\n- {RYTHME}\n- {REFORMULATION}\n- {STYLE}\n"
        )

    # ------------------------------------------------------------ après la réponse du modèle
    def lire_reponse(self, reponse_brute: str, texte_affiche: str) -> str:
        """Lit l'évaluation déclarée, met à jour les essais, note si une question reste en attente.

        Rend l'évaluation lue (« aucune » si la balise manque).
        """
        self.tours += 1
        evaluation = "aucune"
        if match := BALISE_EVAL.search(reponse_brute or ""):
            valeur = match.group(1).lower()
            valeur = "".join(_SANS_ACCENT.get(c, c) for c in valeur)
            if valeur in EVALUATIONS:
                evaluation = valeur
        if evaluation == "incertain" and self.incertains >= PRECISIONS_AVANT_JUGEMENT:
            # Déjà demandé de préciser : rester flou une deuxième fois compte un essai.
            evaluation = "faux"
        if self.question_en_attente:
            if evaluation == "incertain":
                self.incertains += 1
            else:
                self.incertains = 0
            if evaluation == "correct":
                self.reussites += 1
                self.tentatives = 0
            elif evaluation in ("partiel", "faux"):
                self.tentatives += 1
                if self.tentatives >= ESSAIS_AVANT_REPONSE:
                    # La réponse a été donnée ce tour : la question jumelle repart de zéro.
                    self.tentatives = 0
        else:
            self.tentatives = 0
            self.incertains = 0
        self.derniere_evaluation = evaluation
        self.question_en_attente = se_termine_par_une_question(texte_affiche)
        return evaluation


def se_termine_par_une_question(texte: str) -> bool:
    """Une question en attente : la dernière phrase du texte lu par l'élève en est une."""
    texte = (texte or "").strip()
    if not texte:
        return False
    phrases = [p for p in re.split(r"(?<=[.!?؟…])\s+", texte) if p.strip()]
    return phrases[-1].rstrip().endswith(("?", "؟")) if phrases else False


def retirer_balise_eval(texte: str) -> str:
    """La balise ne doit jamais atteindre l'élève (chat, voix, historique)."""
    return BALISE_EVAL.sub(" ", texte or "", count=1).lstrip()
