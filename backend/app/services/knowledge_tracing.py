"""Ce que l'élève sait vraiment, estimé à chaque réponse.

`Progression` comptait des réussites consécutives. C'est une règle honnête
mais aveugle sur deux points, et les deux se voient en séance :

  * **la chance.** Un QCM à quatre choix se réussit une fois sur quatre sans
    rien savoir. Trois bonnes réponses d'affilée à des QCM, c'est un
    événement de probabilité 1/64 — rare, mais il arrive tous les jours à
    l'échelle d'une classe, et l'élève se retrouvait en examen ;
  * **l'étourderie.** Un élève qui maîtrise se trompe quand même, de temps en
    temps. Le compteur remettait sa série à zéro comme s'il ne savait rien.

Le *Bayesian Knowledge Tracing* (Corbett & Anderson, 1995) traite exactement
ça, et c'est le standard des tuteurs intelligents depuis trente ans. Quatre
paramètres, une mise à jour bayésienne par réponse, aucun entraînement
préalable : il fonctionne dès le premier élève. Ce n'est pas un réseau de
neurones et c'est volontaire — quand il se trompe, on peut lire pourquoi.

Le modèle sépare CE QUE L'ÉLÈVE SAIT de CE QU'IL A RÉPONDU. Une réponse est
une observation bruitée d'un état caché ; la probabilité de maîtrise se
révise à chaque observation, puis on ajoute la chance d'avoir appris depuis.

Ce module ne connaît ni base de données, ni session, ni matière : il prend
des booléens et rend des probabilités. C'est ce qui le rend vérifiable au
chiffre près.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ParametresBKT:
    """Les quatre paramètres du modèle.

    Les valeurs par défaut sont celles de la littérature, pas des réglages
    maison : elles reproduisent presque exactement les seuils empiriques que
    `Progression` utilisait déjà (deux réussites pour quitter le cours, trois
    pour aller à l'examen), ce qui est plutôt rassurant sur les deux.
    """

    #: P(L0) — ce qu'on suppose acquis avant toute observation. Bas, parce
    #: qu'un élève arrive sur une notion qu'il travaille justement parce
    #: qu'elle n'est pas acquise.
    init: float = 0.25
    #: P(T) — chance d'apprendre à chaque occasion. C'est ce terme qui fait
    #: qu'une estimation ne descend jamais durablement à zéro : on continue
    #: de supposer que l'enseignement sert à quelque chose.
    apprentissage: float = 0.15
    #: P(G) — répondre juste sans savoir. 0,20 ≈ un QCM à cinq choix.
    chance: float = 0.20
    #: P(S) — répondre faux en sachant. L'inattention, la fatigue.
    etourderie: float = 0.10

    def __post_init__(self):
        for nom in ("init", "apprentissage", "chance", "etourderie"):
            valeur = getattr(self, nom)
            if not 0.0 <= float(valeur) <= 1.0:
                raise ValueError(f"BKT: {nom}={valeur} hors de [0, 1]")

        # Le garde-fou qui compte (Baker et coll.) : au-delà, le modèle
        # devient DÉGÉNÉRÉ — savoir rendrait l'échec plus probable que
        # réussir, et chaque bonne réponse ferait BAISSER l'estimation. Les
        # équations continueraient de tourner sans rien signaler ; c'est
        # pour ça que le refus est ici et pas dans un commentaire.
        if self.chance >= 0.5 or self.etourderie >= 0.5:
            raise ValueError(
                "BKT dégénéré : chance et étourderie doivent rester sous 0,5, "
                f"reçu chance={self.chance}, etourderie={self.etourderie}"
            )


PARAMETRES_DEFAUT = ParametresBKT()


class Maitrise:
    """La probabilité qu'une compétence soit acquise, révisée à chaque preuve."""

    def __init__(self, parametres: ParametresBKT = PARAMETRES_DEFAUT):
        self.parametres = parametres
        self.p: float = parametres.init
        #: Le nombre d'observations, utile pour refuser de conclure trop tôt.
        self.observations: int = 0

    def observer(self, reussite: bool) -> float:
        """Révise l'estimation avec une réponse, et renvoie la nouvelle.

        Deux temps, et les confondre est l'erreur classique :

          1. **le conditionnement** — sachant ce qu'il vient de répondre, que
             savait-il AVANT ? C'est le théorème de Bayes ;
          2. **la transition** — et depuis, a-t-il appris ? C'est ce second
             terme qui permet à un élève de remonter après un échec.
        """
        p = self.p
        s = self.parametres.etourderie
        g = self.parametres.chance

        if reussite:
            # Il a réussi : soit il savait et n'a pas commis d'étourderie,
            # soit il ne savait pas et a eu de la chance.
            numerateur = p * (1.0 - s)
            denominateur = numerateur + (1.0 - p) * g
        else:
            # Il a échoué : soit il savait et a fait une étourderie, soit il
            # ne savait pas et n'a pas eu de chance.
            numerateur = p * s
            denominateur = numerateur + (1.0 - p) * (1.0 - g)

        # Un dénominateur nul voudrait dire « cette réponse était impossible ».
        # Cela ne peut arriver qu'avec des paramètres extrêmes, mais alors
        # mieux vaut ne rien apprendre de cette observation que diviser par
        # zéro au milieu d'un cours.
        conditionnee = (numerateur / denominateur) if denominateur > 0 else p

        self.p = conditionnee + (1.0 - conditionnee) * self.parametres.apprentissage
        self.observations += 1
        return self.p

    def acquise(self, seuil: float, minimum_observations: int = 1) -> bool:
        """Vrai si la compétence est acquise au seuil demandé.

        `minimum_observations` empêche de conclure sur un a priori : sans lui,
        un seuil placé sous P(L0) déclarerait acquise une compétence sur
        laquelle l'élève n'a jamais rien répondu.
        """
        return self.observations >= minimum_observations and self.p >= seuil

    def __repr__(self) -> str:  # pragma: no cover - confort de journal
        return f"Maitrise(p={self.p:.3f}, n={self.observations})"


@dataclass
class SuiviMaitrise:
    """Une estimation par compétence.

    Une « compétence » n'est pas une matière ni un chapitre : c'est un couple
    (sujet, activité). Expliquer une notion et savoir l'appliquer sont deux
    apprentissages distincts — c'est la distinction que fait la taxonomie de
    Bloom, et le service de compétences l'utilise déjà pour pondérer.
    Confondre les deux ferait passer en examen un élève qui a seulement
    compris l'explication.
    """

    parametres: ParametresBKT = PARAMETRES_DEFAUT
    _competences: dict[str, Maitrise] = field(default_factory=dict)

    @staticmethod
    def cle(sujet: str, activite: str) -> str:
        return f"{(sujet or '').strip().lower()}::{(activite or '').strip().lower()}"

    def pour(self, sujet: str, activite: str) -> Maitrise:
        cle = self.cle(sujet, activite)
        if cle not in self._competences:
            self._competences[cle] = Maitrise(self.parametres)
        return self._competences[cle]

    def observer(self, sujet: str, activite: str, reussite: bool) -> float:
        return self.pour(sujet, activite).observer(reussite)
