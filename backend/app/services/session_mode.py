"""Ce que l'élève est en train de faire, et qui a le droit d'en changer.

Jusqu'ici le mode était une ROUTE : `/session` pour le cours, `/libre` pour
une question, `/exam` pour un examen. C'est l'élève qui choisissait, et le
tuteur obéissait. L'inverse est le but — l'élève dit son intention en parlant,
le tuteur choisit le mode — mais un modèle ne peut pas changer de route.

Le mode devient donc un ÉTAT, que le tuteur demande avec ``<mode>`` et que ce
module arbitre. Trois choses le distinguent d'un simple attribut :

**1. Changer de mode n'écrit JAMAIS la phase de leçon.**
C'est le mécanisme qui fait tenir « un seul endroit ». L'élève interrompt son
cours pour poser une question, puis revient : la leçon doit reprendre où elle
était. Si le mode écrivait la phase — comme `_init_session` le fait
aujourd'hui en imposant `PhaseLesson("libre")` hors coaching — la position
serait perdue à chaque digression, et l'élève referait deux fois la même
étape. `PhaseLesson` reste seul juge de la progression ; ce module ne la
touche pas.

**2. Le tuteur ne peut pas sortir l'élève d'un examen.**
Il peut y entrer, pas en sortir. Un examen a un chronomètre et une note : un
modèle qui décide au milieu qu'il vaut mieux réviser annule une épreuve
commencée. Seul un geste explicite de l'élève — ou la fin de l'épreuve —
quitte le mode examen.

**3. Un mot inconnu est refusé, pas stocké.**
Exactement le trou qui figeait la progression dans `lesson_phase` : une valeur
non validée arrivait jusqu'à un `index()` qui levait. Ici, une demande absurde
renvoie None et l'écran ne bouge pas.

Le vocabulaire vit en un seul endroit, comme celui des balises d'affichage
(cf. `tag_decoder`) : les quatre mots de l'élève, leur correspondance avec les
valeurs historiques de `session_mode`, et les synonymes que le modèle produit
en pratique.
"""
from __future__ import annotations

from typing import Any, Optional


# ── Le vocabulaire ────────────────────────────────────────────────

#: Les quatre choses qu'un élève peut être en train de faire. Ce sont les
#: mots de l'ÉLÈVE, pas ceux du code : c'est ce que le modèle lit dans le
#: prompt et ce qu'il réémet.
MODES: tuple[str, ...] = ("cours", "exercice", "examen", "question")

#: Les modes qui font partie d'une leçon suivie. Les deux autres sont des
#: parenthèses : on y entre et on en revient sans avoir avancé le cours.
DANS_LA_LECON: tuple[str, ...] = ("cours", "exercice")

#: Correspondance avec `session_handler.session_mode`, dont les valeurs sont
#: lues à une trentaine d'endroits (choix du prompt, RAG, ressources). On ne
#: renomme pas tout ça : on traduit ici, une fois.
#:
#: `examen` → `explain` n'est pas un raccourci : c'est le mode qui injecte
#: l'énoncé et la correction officielle dans le prompt à chaque tour, ce dont
#: une épreuve a précisément besoin.
LEGACY: dict[str, str] = {
    "cours": "coaching",
    "exercice": "coaching",
    "examen": "explain",
    "question": "libre",
}

#: Ce que le modèle écrit VRAIMENT quand on lui demande un mode. Refuser une
#: quasi-bonne réponse laisserait l'élève coincé dans le mauvais écran, ce qui
#: est pire que d'accepter une orthographe approximative.
_SYNONYMES: dict[str, str] = {
    "coaching": "cours",
    "lecon": "cours",
    "leçon": "cours",
    "explication": "cours",
    # `explain` est la valeur HISTORIQUE du mode examen (celle qui injecte
    # l'énoncé et la correction), pas un synonyme d'« explication ». Les
    # confondre renverrait au cours un élève que le navigateur ouvre sur une
    # question d'examen.
    "explain": "examen",
    "entrainement": "exercice",
    "entraînement": "exercice",
    "exercices": "exercice",
    "pratique": "exercice",
    "qcm": "exercice",
    "exam": "examen",
    "evaluation": "examen",
    "évaluation": "examen",
    "controle": "examen",
    "contrôle": "examen",
    "test": "examen",
    "libre": "question",
    "questions": "question",
    "discussion": "question",
    "chat": "question",
}


def normaliser(valeur: Any) -> Optional[str]:
    """Le mode demandé, ou None si ce n'en est pas un.

    Ne lève jamais : la valeur vient du modèle, donc de l'extérieur.
    """
    if not isinstance(valeur, str):
        return None
    mot = valeur.strip().lower()
    if mot in MODES:
        return mot
    return _SYNONYMES.get(mot)


def lire_demande(donnees: Any) -> Optional[str]:
    """Le mode contenu dans un bloc ``<mode>`` décodé.

    Le modèle écrit tantôt ``{"mode": "examen"}``, tantôt ``{"mode":
    {"type": "examen"}}``, tantôt la chaîne nue. Les trois content la même
    chose ; les distinguer ne servirait qu'à perdre des demandes valides.
    """
    if isinstance(donnees, str):
        return normaliser(donnees)
    if isinstance(donnees, dict):
        for cle in ("mode", "type", "valeur", "value"):
            if cle in donnees:
                trouve = lire_demande(donnees[cle])
                if trouve:
                    return trouve
    return None


def raison(donnees: Any) -> str:
    """La justification que le tuteur a jointe, si elle existe.

    Elle n'est pas décorative : elle part au journal et à l'écran de l'élève
    (« on passe en examen »), pour qu'un changement de mode ne soit jamais
    une surprise.
    """
    if isinstance(donnees, dict):
        for cle in ("raison", "reason", "pourquoi", "message"):
            valeur = donnees.get(cle)
            if isinstance(valeur, str) and valeur.strip():
                return " ".join(valeur.split())[:160]
    return ""


# ── L'arbitre ─────────────────────────────────────────────────────

class ModeSession:
    """Détient le mode courant et arbitre les demandes de changement."""

    def __init__(self, depart: str = "cours"):
        self.courant: str = normaliser(depart) or MODES[0]

    # ── Lecture ───────────────────────────────────────────────────
    @property
    def legacy(self) -> str:
        """La valeur attendue par `session_mode` dans le handler."""
        return LEGACY[self.courant]

    @property
    def dans_la_lecon(self) -> bool:
        return self.courant in DANS_LA_LECON

    @property
    def en_examen(self) -> bool:
        return self.courant == "examen"

    # ── Transitions ───────────────────────────────────────────────
    def demander(self, valeur: Any, *, par: str = "tuteur") -> Optional[str]:
        """Applique la demande et renvoie le nouveau mode, ou None.

        None veut dire « rien n'a bougé » : mot inconnu, mode déjà courant,
        ou sortie d'examen tentée par le tuteur. L'appelant s'en sert pour
        décider s'il doit prévenir le navigateur — annoncer un changement qui
        n'a pas eu lieu désynchroniserait l'écran de la session.
        """
        vise = normaliser(valeur)
        if vise is None or vise == self.courant:
            return None
        if self.en_examen and par != "eleve":
            # Règle 2 : une épreuve commencée ne s'annule pas toute seule.
            return None
        self.courant = vise
        return vise

    def terminer_examen(self, retour: str = "cours") -> Optional[str]:
        """Fin de l'épreuve : la seule sortie d'examen qui ne vienne pas de
        l'élève. Sans elle, la règle 2 enfermerait la session."""
        if not self.en_examen:
            return None
        return self.demander(retour, par="eleve")
