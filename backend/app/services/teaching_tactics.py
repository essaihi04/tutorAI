"""Comment expliquer à CET élève — mesuré, pas postulé.

L'idée qu'un élève aurait un canal privilégié — visuel, auditif,
kinesthésique — et qu'il faudrait lui enseigner dans ce canal est l'une des
hypothèses les plus testées et les plus systématiquement infirmées de la
recherche en éducation (Pashler et coll., 2008, et les réplications depuis).
Construire une détection de « style » serait donc bâtir une machinerie
sophistiquée sur un résultat négatif.

Ce qui marche vraiment, c'est le **double codage** — mot + image apprend
mieux que mot seul, POUR TOUT LE MONDE. Le tuteur écrit déjà au tableau à
chaque réponse : le vrai principe est donc déjà appliqué, et il ne faut
surtout pas le conditionner à un profil.

Reste une question légitime, et différente : **qu'est-ce qui a marché pour
cet élève, sur cette notion ?** Ce n'est pas un trait de personnalité, c'est
une mesure. Un tuteur humain la fait sans y penser — il essaie une analogie,
voit que ça ne prend pas, passe à un exemple résolu.

C'est un problème de bandit manchot : plusieurs façons d'expliquer, un
retour bruité après chaque essai, un arbitrage entre exploiter ce qui marche
et essayer autre chose.

**UCB1 plutôt qu'ε-greedy**, pour une raison de terrain : il est
DÉTERMINISTE. Pas de tirage aléatoire, donc un comportement reproductible,
testable au chiffre près, et explicable en une phrase — « on reprend ce qui a
le mieux marché, avec un bonus pour ce qu'on a peu essayé ». Un tuteur dont
on ne peut pas expliquer les choix est un tuteur qu'on ne peut pas corriger.

Ce module ne connaît ni élève, ni base, ni session : il prend des succès et
des échecs, il rend un nom de tactique.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Tactique:
    cle: str
    #: L'instruction réellement injectée dans le plan de séance. Impérative
    #: et courte : une consigne longue se fait paraphraser au lieu d'être
    #: suivie.
    consigne: str


#: Cinq façons d'expliquer une même notion. Elles se distinguent par la
#: FORME du raisonnement demandé à l'élève, pas par un canal sensoriel —
#: c'est précisément la différence avec les « styles d'apprentissage ».
TACTIQUES: tuple[Tactique, ...] = (
    Tactique(
        "exemple",
        "Explique par un exemple résolu, étape par étape, en montrant "
        "chaque décision — pas seulement le calcul.",
    ),
    Tactique(
        "schema",
        "Construis un schéma au tableau et fais-le parler : chaque flèche, "
        "chaque étiquette doit dire quelque chose.",
    ),
    Tactique(
        "analogie",
        "Pars d'une analogie concrète de son quotidien, puis reviens "
        "explicitement au vocabulaire du programme.",
    ),
    Tactique(
        "socratique",
        "Ne donne pas la règle : amène-le à la trouver par une suite de "
        "questions courtes, une idée à la fois.",
    ),
    Tactique(
        "contre_exemple",
        "Montre d'abord l'erreur typique sur cette notion, fais-lui dire "
        "pourquoi elle est fausse, puis énonce la règle correcte.",
    ),
)

TACTIQUES_PAR_CLE: dict[str, Tactique] = {t.cle: t for t in TACTIQUES}

#: Le terme d'exploration d'UCB1. sqrt(2) est la valeur de référence ; plus
#: haut, le tuteur change de méthode sans arrêt et l'élève trouve ça
#: incohérent.
EXPLORATION = math.sqrt(2)


@dataclass
class Score:
    essais: int = 0
    reussites: int = 0

    @property
    def moyenne(self) -> float:
        return (self.reussites / self.essais) if self.essais else 0.0


@dataclass
class BanditTactiques:
    """Choisit la façon d'expliquer, et apprend de ce qui suit.

    La récompense est booléenne — la réponse suivante de l'élève est juste ou
    non. On pourrait utiliser le gain de maîtrise estimé par le BKT, mais il
    diminue mécaniquement quand la maîtrise approche de 1 : les tactiques
    employées en fin de parcours seraient pénalisées sans l'avoir mérité.
    """

    exploration: float = EXPLORATION
    _scores: dict[str, Score] = field(default_factory=dict)

    def score(self, cle: str) -> Score:
        if cle not in self._scores:
            self._scores[cle] = Score()
        return self._scores[cle]

    @property
    def total_essais(self) -> int:
        return sum(s.essais for s in self._scores.values())

    def _priorite(self, cle: str, total: int) -> float:
        s = self.score(cle)
        if s.essais == 0:
            # Jamais essayée : priorité absolue. UCB1 garantit ainsi que
            # chaque tactique est tentée au moins une fois avant qu'on
            # conclue quoi que ce soit — sans ça, une bonne méthode écartée
            # par malchance au premier essai ne reviendrait jamais.
            return float("inf")
        return s.moyenne + self.exploration * math.sqrt(math.log(total) / s.essais)

    def choisir(self, exclure: Optional[str] = None) -> Tactique:
        """La tactique à employer maintenant.

        `exclure` évite de répéter à l'identique celle qui vient d'échouer :
        réexpliquer « autrement » est le principe même du retour au cours, et
        rejouer la même méthode serait ressenti comme du radotage.
        """
        total = max(1, self.total_essais)
        candidates = [t for t in TACTIQUES if t.cle != exclure] or list(TACTIQUES)
        # `max` garde le PREMIER maximum : à égalité, l'ordre de déclaration
        # tranche. Le choix reste donc reproductible.
        return max(candidates, key=lambda t: self._priorite(t.cle, total))

    def recompenser(self, cle: str, reussite: bool) -> None:
        if cle not in TACTIQUES_PAR_CLE:
            return
        s = self.score(cle)
        s.essais += 1
        if reussite:
            s.reussites += 1

    def classement(self) -> list[tuple[str, int, int]]:
        """(tactique, réussites, essais), du plus efficace au moins.

        Sert au journal et à l'explication : « pour cet élève, l'exemple
        résolu marche 4 fois sur 5, l'analogie 1 fois sur 4 ».
        """
        lignes = [(cle, s.reussites, s.essais) for cle, s in self._scores.items() if s.essais]
        lignes.sort(key=lambda l: (-(l[1] / l[2]), -l[2]))
        return lignes


# ── Mémoire entre séances ─────────────────────────────────────────

#: Le marqueur ajouté à la colonne `source` de `student_answer_history`.
#: Aucune migration : la colonne est du texte libre, et elle est déjà lue par
#: le calcul de compétences. Un bandit qui oublie à chaque connexion
#: n'apprend rien — c'est le seul moyen d'accumuler dès aujourd'hui.
MARQUEUR = "|tactique="


def marquer_source(source: str, tactique: Optional[str]) -> str:
    if not tactique or tactique not in TACTIQUES_PAR_CLE:
        return source
    return f"{source}{MARQUEUR}{tactique}"


def lire_tactique(source: str) -> Optional[str]:
    if not source or MARQUEUR not in source:
        return None
    cle = source.split(MARQUEUR, 1)[1].strip()
    return cle if cle in TACTIQUES_PAR_CLE else None


def depuis_historique(reponses: Optional[list]) -> BanditTactiques:
    """Reconstruit le bandit depuis les réponses déjà enregistrées.

    Ce que l'élève a montré la semaine dernière compte autant qu'aujourd'hui :
    sans cette relecture, chaque séance repartirait de zéro et le bandit
    passerait sa vie à explorer.
    """
    bandit = BanditTactiques()
    for ligne in reponses or []:
        if not isinstance(ligne, dict):
            continue
        cle = lire_tactique(str(ligne.get("source") or ""))
        if cle:
            bandit.recompenser(cle, bool(ligne.get("is_correct")))
    return bandit
