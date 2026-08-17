"""Ce que le tuteur doit faire maintenant, et pourquoi.

Le moteur de décision existait déjà : `study_plan_service.get_adaptive_next_session`
classe par priorité ce que l'élève a de mieux à faire à cet instant —
erreur récurrente, lacune critique, lacune en ZPD, révision espacée, séance
planifiée, examen blanc. **Son résultat partait vers une page React.** Le
tuteur, lui, ne l'a jamais vu. C'est la même maladie que le briefing :
l'intelligence est écrite, elle n'atteint pas celui qui enseigne.

Ce module ne réinvente donc aucune pédagogie. Il traduit une décision déjà
prise en une consigne que le modèle peut suivre, et en un mode que la session
peut adopter.

**La décision est prise en Python, pas dans l'humeur du modèle.** C'est la
raison d'être du module : un tuteur qui improvise son plan de séance donne un
résultat différent à chaque tirage, et rien n'est testable. Ici le modèle
exécute un scénario ; il ne le choisit pas.

Deux disciplines reprises du briefing, pour les mêmes raisons :

  * un budget de caractères tenu par un test — le prompt de production fait
    déjà 82 000 caractères ;
  * ne lève jamais — un scénario absent laisse un tuteur qui enseigne
    normalement, une exception laisse un élève devant un écran vide.

`Progression`, plus bas, ajoute le « quand s'arrêter » : le mode ne change
plus sur l'humeur du modèle mais sur une PREUVE — une réponse juste, une
erreur répétée.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Optional

from app.services.session_mode import mode_pour_seance

_log = logging.getLogger(__name__)


#: Plus court que le briefing : c'est une consigne, pas un dossier.
BUDGET_CARACTERES = 500

#: `reason` est rédigé pour un humain et parfois long (les erreurs
#: récurrentes détaillent le motif). On le coupe à la source.
MAX_MOTIF = 220

#: Ce que chaque recommandation demande au tuteur de FAIRE. Le moteur dit
#: déjà pourquoi ; ces phrases disent comment. Volontairement impératives et
#: courtes — une consigne longue se fait paraphraser au lieu d'être suivie.
CONSIGNES: dict[str, str] = {
    "erreur_recurrente": (
        "Aborde ce point DÈS LE DÉBUT. Cherche la cause de l'erreur "
        "(prérequis manquant ? confusion ?) avant d'expliquer à nouveau."
    ),
    "lacune_critique": (
        "Reprends les prérequis et le vocabulaire de base. "
        "Pas d'exercice complexe tant que les bases ne tiennent pas."
    ),
    "zpd_optimal": (
        "Zone d'apprentissage optimale : laisse-le essayer seul, "
        "donne un indice avant la réponse, corrige sa méthode."
    ),
    "spaced_review": (
        "Révision : fais-le se souvenir par des questions courtes "
        "avant de réexpliquer ce qui manque."
    ),
    "plan_next": "Suis la séance prévue.",
    "exam_practice": (
        "Tout est acquis : sujet complet en conditions réelles, "
        "chronomètre, aucun indice, note sur 20 à la fin."
    ),
}


def _court(texte: Any, maximum: int) -> str:
    texte = " ".join(str(texte or "").split())
    if len(texte) <= maximum:
        return texte
    return texte[: maximum - 1].rstrip(" ,;.") + "…"


@dataclass(frozen=True)
class Directive:
    """La consigne, et le mode qu'elle appelle."""

    texte: str
    #: Le mode que la session devrait adopter — 'cours', 'exercice', 'examen'.
    mode: str
    #: Sur quoi porte la séance, pour l'annonce faite à l'élève.
    sujet: str
    #: La recommandation brute du moteur, pour le journal.
    recommandation: str

    def __bool__(self) -> bool:
        return bool(self.texte)


VIDE = Directive(texte="", mode="cours", sujet="", recommandation="")


def composer(decision: Optional[dict], budget: int = BUDGET_CARACTERES) -> Directive:
    """Traduit une décision du moteur en consigne pour le tuteur.

    Les lignes sont ajoutées par ordre d'utilité et coupées par la fin, comme
    dans le briefing : ce qu'il faut travailler survit toujours, la stratégie
    ZPD est sacrifiée en premier.
    """
    if not isinstance(decision, dict) or not decision:
        return VIDE

    recommandation = str(decision.get("recommendation") or "")
    matiere = str(decision.get("subject") or "").strip()
    sujet = str(decision.get("topic") or decision.get("chapter_title") or "").strip()
    mode = mode_pour_seance(decision.get("session_type"))

    if not sujet and recommandation != "exam_practice":
        # Sans sujet, la consigne dirait « travaille » sans dire quoi : le
        # modèle inventerait le chapitre. Mieux vaut pas de scénario.
        return VIDE

    entete = " ".join(p for p in (sujet, f"({matiere})" if matiere else "") if p)
    lignes = [f"À travailler maintenant : {entete}."]

    consigne = CONSIGNES.get(recommandation)
    if consigne:
        lignes.append(consigne)

    motif = _court(decision.get("reason"), MAX_MOTIF)
    if motif:
        lignes.append(f"Pourquoi : {motif}")

    strategie = _court(decision.get("zpd_strategy"), 120)
    if strategie:
        lignes.append(f"Méthode : {strategie}")

    retenues: list[str] = []
    taille = 0
    for ligne in lignes:
        cout = len(ligne) + (1 if retenues else 0)
        if taille + cout > budget:
            break
        retenues.append(ligne)
        taille += cout

    if not retenues:
        retenues = [_court(lignes[0], budget)]

    return Directive(
        texte="\n".join(retenues),
        mode=mode,
        sujet=entete or sujet,
        recommandation=recommandation,
    )


# ── Les critères de sortie ────────────────────────────────────────

@dataclass(frozen=True)
class Critere:
    """Ce qu'il faut prouver pour quitter un mode.

    `apres_reussites` compte des réussites CONSÉCUTIVES, jamais un total :
    trois bonnes réponses sur dix ne valent pas trois d'affilée, et traiter
    les deux pareil ferait passer en examen un élève qui alterne au hasard.
    """

    apres_reussites: int = 0
    vers: str = ""
    motif_avance: str = ""
    #: Deux échecs, pas un : une erreur isolée est une inattention, deux de
    #: suite sont un trou. Reculer au premier faux pas rendrait le tuteur
    #: instable et humiliant.
    apres_echecs: int = 0
    retour: str = ""
    motif_recul: str = ""


#: La table de scénarios : ce qui fait sortir de chaque mode.
#:
#: `examen` n'y figure pas, et c'est délibéré — une épreuve chronométrée ne
#: s'interrompt ni sur une bonne réponse ni sur une mauvaise. Seul l'élève,
#: ou la fin du sujet, en sort (cf. session_mode). `question` non plus : une
#: parenthèse n'a pas de critère de réussite.
CRITERES: dict[str, Critere] = {
    "cours": Critere(
        apres_reussites=2,
        vers="exercice",
        motif_avance="Tu as compris — on passe à la pratique.",
    ),
    "exercice": Critere(
        apres_reussites=3,
        vers="examen",
        motif_avance="Trois réussites d'affilée : on passe en conditions d'examen.",
        apres_echecs=2,
        retour="cours",
        motif_recul="On reprend la notion : deux erreurs de suite.",
    ),
}


@dataclass(frozen=True)
class Transition:
    mode: str
    #: Montré à l'élève. Un changement non expliqué est vécu comme un bug.
    raison: str


class Progression:
    """Compte les preuves et décide quand le mode doit changer.

    Volontairement sans base de données ni horloge : une séance se raconte
    par la suite des réponses, et rien d'autre. C'est ce qui rend la règle
    testable en trois lignes.
    """

    def __init__(self, mode: str = "cours"):
        self.mode = mode if mode in ("cours", "exercice", "examen", "question") else "cours"
        self.reussites = 0
        self.echecs = 0

    def _basculer(self, vers: str, raison: str) -> Transition:
        self.mode = vers
        # Les compteurs repartent de zéro : sans ça, les réussites accumulées
        # en cours feraient franchir l'étape suivante immédiatement, et
        # l'élève traverserait trois modes sur une seule bonne réponse.
        self.reussites = 0
        self.echecs = 0
        return Transition(mode=vers, raison=raison)

    def enregistrer(self, reussite: bool) -> Optional[Transition]:
        """Prend une preuve, renvoie la transition qu'elle déclenche — ou None.

        None est le cas normal : la plupart des réponses ne changent rien.
        """
        critere = CRITERES.get(self.mode)
        if critere is None:
            # Examen et question : aucune preuve ne fait sortir d'ici.
            return None

        if reussite:
            self.echecs = 0
            self.reussites += 1
            if critere.apres_reussites and self.reussites >= critere.apres_reussites:
                return self._basculer(critere.vers, critere.motif_avance)
            return None

        # Un échec annule la série en cours : la maîtrise doit être continue.
        self.reussites = 0
        self.echecs += 1
        if critere.apres_echecs and self.echecs >= critere.apres_echecs:
            return self._basculer(critere.retour, critere.motif_recul)
        return None


def consigne_de_mode(mode: str, sujet: str = "") -> str:
    """La consigne qui remplace le scénario après une transition.

    Le scénario d'ouverture parlait d'une situation qui n'existe plus — le
    laisser en place ferait redémarrer le tuteur sur l'ancienne étape.
    """
    quoi = f" sur {sujet}" if sujet else ""
    if mode == "exercice":
        return (
            f"À travailler maintenant : des exercices{quoi}.\n"
            "Laisse-le chercher seul, donne un indice avant la réponse, "
            "corrige sa méthode plutôt que son résultat."
        )
    if mode == "examen":
        return (
            f"À travailler maintenant : un sujet complet{quoi}.\n"
            "Conditions réelles : chronomètre, aucun indice, note sur 20 à la fin."
        )
    if mode == "question":
        return ""
    return (
        f"À travailler maintenant : la notion{quoi}.\n"
        "Reprends l'explication autrement — la précédente n'a pas suffi. "
        "Vérifie chaque étape avant de continuer."
    )


async def pour_eleve(
    student_id: str,
    *,
    resume_proficiency: Optional[dict] = None,
    budget: int = BUDGET_CARACTERES,
) -> Directive:
    """La directive du moment. Ne lève jamais."""
    try:
        from app.services.study_plan_service import study_plan_service

        decision = await study_plan_service.get_adaptive_next_session(
            student_id, summary=resume_proficiency
        )
    except Exception as exc:  # noqa: BLE001
        _log.warning("[Scenario] moteur indisponible pour %s : %s", student_id, exc)
        return VIDE

    directive = composer(decision, budget=budget)
    if directive:
        _log.info(
            "[Scenario] %s → mode %s (%s)",
            directive.recommandation,
            directive.mode,
            directive.sujet,
        )
    return directive
