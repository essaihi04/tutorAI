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
  • Ce qui se retient mot pour mot pour le bac se RELIT : à la fin du bloc,
    le prof relit la phrase-clé (définition ou formule), telle qu'au tableau.
    Si l'élève demande de réentendre, on relit à l'identique, sans rien
    ajouter. « Je ne comprends pas » est autre chose : on change d'angle.
  • Un énoncé se lit deux fois avant tout calcul : d'abord « de quoi parle
    l'exercice ? », puis une relecture active — données et unités, ce qui
    est demandé, le verbe de la consigne.
  • Quand l'erreur vient d'une compétence des années antérieures (dériver,
    projeter un vecteur, la structure de la cellule…), le prof ouvre une
    PARENTHÈSE : il la nomme, la réexplique en quelques phrases avec un
    exemple du niveau d'origine, vérifie d'une question, et revient reposer
    la question du cours telle quelle. Jamais deux parenthèses imbriquées,
    trois au plus par séance ; au-delà, c'est un autre cours à planifier.
    Les prérequis possibles viennent de `prerequis.py`, par chapitre, et le
    modèle en déclare un avec ``<prerequis>id</prerequis>``.

Le module ne lit ni base ni réseau. Il tient trois faits — une question
est-elle en attente, combien d'essais l'élève a-t-il faits, combien de tours
ont passé — et rend une consigne. Le jugement « correct / partiel / faux / incertain »
appartient au modèle, qui le déclare en tête de réponse dans une balise
``<eval>`` retirée avant l'affichage ; le module le lit pour compter les
essais. Pas d'état parallèle : ce qui n'est pas dans la réponse n'existe pas.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Optional

from app.services.prerequis import BALISE_PREREQUIS, bloc_candidats

EVALUATIONS: tuple[str, ...] = ("correct", "partiel", "faux", "incertain", "aucune")
#: Essais accordés avant de donner la réponse.
ESSAIS_AVANT_REPONSE = 2
#: Demandes de précision accordées avant de devoir trancher.
PRECISIONS_AVANT_JUGEMENT = 1
#: Parenthèses de prérequis par séance. Au-delà, ce n'est plus une parenthèse,
#: c'est un autre cours : on le note pour le plan d'études et on continue.
PARENTHESES_MAX = 3
BALISE_EVAL = re.compile(r"\s*\**\s*<eval>\s*([a-zA-Zé]+)\s*</eval>\s*\**\s*", re.IGNORECASE)
_SANS_ACCENT = {"é": "e"}
_DEMANDE_EXPLICATION = re.compile(
    r"\b(expli|c['’]est quoi|qu['’]est[- ]ce|comment|pourquoi|d[ée]finition|je ne comprends|"
    r"chno|kifach|3lach|ach|شنو|كيفاش|علاش|اشرح)",
    re.IGNORECASE,
)
_DEMANDE_EXERCICE = re.compile(r"\b(exercice|entra[iî]ne|exo|tmrin|تمرين|question bac|qcm)\b", re.IGNORECASE)
#: Réentendre, pas réexpliquer : l'élève a mal entendu ou veut fixer la phrase.
#: « se répète » est une réponse de physique (un phénomène périodique), pas une demande.
_DEMANDE_RELECTURE = re.compile(
    r"(?<!se )(?<!s'e)\b(r[ée]p[èeé]te[rz]?|relis|relire|redis|redire|encore une fois|une autre fois|"
    r"3awd|3awed|عاود|عاودها|عاودلي|ماسمعتش|ما سمعتش)",
    re.IGNORECASE,
)
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
RELECTURE = (
    "Juste avant ta question, RELIS la phrase à retenir (la définition, ou la formule avec le sens de "
    "chaque terme), annoncée par « Je relis : », mot pour mot comme au tableau, en phrases courtes. "
    "Une seule phrase-clé, relue une seule fois."
)
LECTURE_ACTIVE = (
    "Lecture de l'énoncé, deuxième temps : quelle que soit sa réponse, fais maintenant la RELECTURE "
    "ACTIVE avec lui — les données (avec leurs unités), ce qui est demandé, et le verbe de la consigne "
    "(calculer, justifier, montrer que, déduire). Une seule question pour la lancer. Aucun calcul encore. "
    "Ces deux lectures ne sont pas notées : évaluation « aucune »."
)


@dataclass
class Parenthese:
    """Un détour par une compétence des années antérieures, ouvert sur une
    erreur, fermé sur une vérification. Jamais imbriqué."""

    id: str
    titre: str
    niveau: str
    essais: int = 0
    #: Une question du cours attendait quand on a ouvert : on la reposera.
    question_suspendue: bool = True


@dataclass
class SkillProfesseur:
    """Trois faits, une consigne par tour."""

    question_en_attente: bool = False
    tentatives: int = 0
    #: Demandes de précision d'affilée sur la question en attente.
    incertains: int = 0
    #: Lecture de l'énoncé en cours : 0 aucune, 1 première lecture posée, 2 relecture active posée.
    lecture_enonce: int = 0
    tours: int = 0
    reussites: int = 0
    derniere_evaluation: str = "aucune"
    #: Les prérequis plausibles du chapitre en cours (objets de `prerequis.py`).
    candidats: list[Any] = field(default_factory=list)
    parenthese: Optional[Parenthese] = None
    parentheses_faites: list[str] = field(default_factory=list)
    #: Ce qui s'est passé ce tour côté parenthèse, pour le journal et l'écran :
    #: {"etat": "ouverte" | "fermee", "id", "titre", "niveau", "reussite", "essais"} ou None.
    evenement_parenthese: Optional[dict] = None

    def proposer_prerequis(self, candidats: list[Any]) -> None:
        """Les prérequis du chapitre, donnés par la séance. Rien n'est ouvert ici."""
        self.candidats = list(candidats or [])

    @property
    def _candidats_restants(self) -> list[Any]:
        if self.parenthese or len(self.parentheses_faites) >= PARENTHESES_MAX:
            return []
        return [c for c in self.candidats if c.id not in self.parentheses_faites]

    def _consigne_parenthese(self) -> list[str]:
        p = self.parenthese
        retour = (
            "puis REPOSE telle quelle la question du cours qui attendait, sans la reformuler."
            if p.question_suspendue else "puis reprends le cours exactement où tu l'avais laissé."
        )
        if not self.question_en_attente:
            return [
                f"Situation : parenthèse ouverte sur « {p.titre} » ({p.niveau}), mais tu n'as pas posé la "
                "question de vérification. Pose-la maintenant, seule. Évaluation « aucune ».",
            ]
        essai = p.essais + 1
        lignes = [
            f"Situation : parenthèse sur « {p.titre} » ({p.niveau}) — tu attends la réponse à ta question "
            f"de vérification (essai n°{essai}). Pas de nouvelle parenthèse.",
            "Si c'est correct : dis en une phrase que ce prérequis est en place et que tu fermes la parenthèse "
            f"(« On ferme la parenthèse »), {retour}",
        ]
        if essai < ESSAIS_AVANT_REPONSE:
            lignes.append(
                "Si c'est partiel ou faux : UN indice sur ce prérequis seulement, et repose la même question de "
                "vérification. Ne reviens pas encore au cours."
            )
        else:
            lignes.append(
                "Si c'est partiel ou faux : c'était le dernier essai — donne la réponse du prérequis en deux "
                f"phrases, ferme la parenthèse (« On ferme la parenthèse »), {retour}"
            )
        return lignes

    # ------------------------------------------------------------ avant que le modèle parle
    def consigne(self, demande: str, phase: str = "") -> str:
        """La consigne du tour, à ajouter au prompt système."""
        demande = (demande or "").strip()
        lignes: list[str] = []
        if self.parenthese and not (_DEMANDE_RELECTURE.search(demande) and not _NE_SAIT_PAS.search(demande)):
            lignes.extend(self._consigne_parenthese())
        elif self.tours > 0 and _DEMANDE_RELECTURE.search(demande) and not _NE_SAIT_PAS.search(demande):
            # Réentendre n'est pas réexpliquer : on redonne la même phrase, rien de plus.
            lignes.append(
                "Situation : l'élève demande de réentendre. RELIS mot pour mot ce qu'il redemande — ta "
                "phrase-clé ou ta question — lentement, en phrases courtes. N'ajoute ni explication ni "
                "question nouvelle. C'est l'exception à « ne répète pas » : il l'a demandé. Évaluation « aucune »."
            )
        elif self.question_en_attente and self.lecture_enonce == 1:
            self.lecture_enonce = 2
            lignes.append("Situation : il vient de dire de quoi parle l'exercice (première lecture).")
            lignes.append(LECTURE_ACTIVE)
        elif self.question_en_attente and self.lecture_enonce == 2:
            self.lecture_enonce = 0
            lignes.append(
                "Situation : il vient de faire la relecture active de l'énoncé. Confirme les données justes, "
                "complète ou corrige celles qui manquent, puis lance la première étape de résolution par UNE "
                "question. Évaluation « aucune »."
            )
        elif self.question_en_attente:
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
            # Après un premier essai manqué, un prof se demande si le blocage
            # n'est pas en amont. On ne propose les prérequis qu'à ce moment-là :
            # les lister dès la première question inviterait à ouvrir des
            # parenthèses sans raison.
            if self.tentatives >= 1 and self._candidats_restants:
                lignes.append(bloc_candidats(self._candidats_restants))
        elif self.tours == 0:
            lignes.append("Situation : premier tour. Salue, annonce le plan en une phrase, puis commence par "
                          "une question d'accroche liée à son vécu. Pas de nouvelle notion encore.")
        elif _DEMANDE_EXERCICE.search(demande):
            self.lecture_enonce = 1
            lignes.append("Situation : l'élève veut s'entraîner. Pose UN exercice adapté à la phase, sans la "
                          "solution. Puis lance la PREMIÈRE LECTURE de l'énoncé : demande-lui seulement de quoi "
                          "parle l'exercice, en une phrase. Aucun calcul avant la relecture.")
        elif _DEMANDE_EXPLICATION.search(demande) or phase in ("explanation", "exploration"):
            lignes.append("Situation : une notion à expliquer. Explique en un bloc complet : l'idée, un exemple "
                          "concret, la formule et le sens de chaque terme s'il y en a une ; puis arrête-toi et "
                          "demande une reformulation avec ses mots.")
            lignes.append(RELECTURE)
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
        self.evenement_parenthese = None
        if self.parenthese and self.question_en_attente:
            # Le tour juge la vérification du prérequis, pas la question du cours.
            p = self.parenthese
            if evaluation == "correct":
                self._fermer_parenthese(reussite=True)
            elif evaluation in ("partiel", "faux"):
                p.essais += 1
                if p.essais >= ESSAIS_AVANT_REPONSE:
                    self._fermer_parenthese(reussite=False)
            self.derniere_evaluation = evaluation
            self.question_en_attente = se_termine_par_une_question(texte_affiche)
            return evaluation
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
        self._ouvrir_si_declaree(reponse_brute)
        self.question_en_attente = se_termine_par_une_question(texte_affiche)
        if not self.question_en_attente:
            # Sans question posée, la lecture guidée de l'énoncé s'est arrêtée là.
            self.lecture_enonce = 0
        return evaluation

    # ------------------------------------------------------------ la parenthèse
    def _ouvrir_si_declaree(self, reponse_brute: str) -> None:
        """Ouvre la parenthèse que le modèle vient de déclarer, si elle est légitime :
        un prérequis du chapitre, pas déjà traité, pas de parenthèse en cours."""
        match = BALISE_PREREQUIS.search(reponse_brute or "")
        if not match:
            return
        voulu = match.group(1).lower()
        choisi = next((c for c in self._candidats_restants if c.id == voulu), None)
        if choisi is None:
            return
        self.parenthese = Parenthese(
            id=choisi.id, titre=choisi.titre, niveau=choisi.niveau_lisible,
            question_suspendue=self.question_en_attente,
        )
        self.evenement_parenthese = {
            "etat": "ouverte", "id": choisi.id, "titre": choisi.titre, "niveau": choisi.niveau_lisible,
        }

    def _fermer_parenthese(self, reussite: bool) -> None:
        p = self.parenthese
        self.parenthese = None
        self.parentheses_faites.append(p.id)
        # Le prérequis vient d'être remis en place : la question du cours
        # repart avec des essais neufs. La compter comme déjà manquée
        # punirait l'élève pour ce qu'on vient précisément de lui apprendre.
        self.tentatives = 0
        self.incertains = 0
        self.evenement_parenthese = {
            "etat": "fermee", "id": p.id, "titre": p.titre, "niveau": p.niveau,
            "reussite": reussite, "essais": p.essais,
        }


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
