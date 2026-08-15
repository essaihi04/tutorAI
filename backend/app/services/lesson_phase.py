"""Les phases d'une leçon, et les seules transitions permises.

La phase existait déjà, mais **trois mécanismes l'écrivaient sans se parler** :

  1. un « PHASE_SUIVANTE » repéré dans la prose du modèle, qui avançait d'un
     cran à l'aveugle ;
  2. un calcul de ratio d'objectifs terminés, qui visait une phase cible ;
  3. un message `change_phase` du navigateur, qui écrivait la valeur **sans
     la valider**.

Le troisième cassait les deux autres : une valeur inconnue arrivait jusqu'à
`phase_order.index()`, qui levait `ValueError`. L'exception était avalée par
un `except Exception` large, si bien que la suite de `_advance_next_objective`
— dont la détection de fin de leçon — ne s'exécutait plus du tout, en ne
laissant qu'une ligne de journal. Une leçon pouvait donc ne jamais se
terminer sans que rien ne le signale.

Ce module est désormais le SEUL à décider d'une transition. Aucune méthode ne
lève : une entrée absurde est refusée et renvoie False, elle ne peut plus
empoisonner l'état de la session.
"""
from __future__ import annotations


# L'ordre est la progression pédagogique : on ne saute pas l'activation pour
# aller directement à l'application.
PHASES: tuple[str, ...] = (
    "activation",
    "exploration",
    "explanation",
    "application",
    "consolidation",
)

# Le mode libre n'est pas une étape de leçon : il n'a ni avant ni après. Il
# est accepté comme état, mais reste hors de la progression — sans ça, la
# session libre héritait de « activation » et les prompts recevaient une
# phase de cours qui n'avait aucun sens.
HORS_PROGRESSION: tuple[str, ...] = ("libre",)

TOUTES: tuple[str, ...] = PHASES + HORS_PROGRESSION


class PhaseLesson:
    """Détient la phase courante et arbitre les transitions."""

    def __init__(self, depart: str = "activation"):
        self.courante: str = depart if depart in TOUTES else PHASES[0]

    # ── Lecture ───────────────────────────────────────────────────
    @property
    def dans_la_progression(self) -> bool:
        return self.courante in PHASES

    def _rang(self) -> int:
        return PHASES.index(self.courante)

    # ── Transitions ───────────────────────────────────────────────
    def avancer(self) -> bool:
        """Passe au cran suivant. False si dernière phase, ou hors progression.

        C'est ce que déclenche « PHASE_SUIVANTE ». Renvoyer False plutôt que
        de boucler évite d'annoncer au navigateur un changement qui n'a pas
        eu lieu.
        """
        if not self.dans_la_progression:
            return False
        rang = self._rang()
        if rang >= len(PHASES) - 1:
            return False
        self.courante = PHASES[rang + 1]
        return True

    def viser(self, phase: str) -> bool:
        """Va à `phase`, mais seulement si elle est EN AVANT.

        Une leçon ne recule pas toute seule : refaire à l'élève une étape
        qu'il vient de terminer serait pris pour un bug. Les reculs restent
        possibles, mais uniquement par un geste explicite — `definir`.
        """
        if phase not in PHASES or not self.dans_la_progression:
            return False
        if PHASES.index(phase) <= self._rang():
            return False
        self.courante = phase
        return True

    def definir(self, phase: str) -> bool:
        """Saut explicite : reprise de session, ou choix du navigateur.

        Refuse ce qui n'est pas une phase connue AU LIEU DE LE STOCKER —
        c'est précisément le trou qui figeait la progression.
        """
        if phase not in TOUTES or phase == self.courante:
            return False
        self.courante = phase
        return True

    # ── Suggestion ────────────────────────────────────────────────
    @staticmethod
    def pour_avancement(ratio_objectifs: float, lecon_terminee: bool) -> str:
        """La phase que l'avancement des objectifs suggère.

        Ne décide rien : la décision revient à `viser`, qui refusera un
        recul. Séparer les deux permet de tester le barème sans session.
        """
        if lecon_terminee:
            return "consolidation"
        if ratio_objectifs <= 0.20:
            return "exploration"
        if ratio_objectifs <= 0.70:
            return "explanation"
        return "application"
