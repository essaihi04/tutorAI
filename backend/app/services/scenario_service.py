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

Ce qui MANQUE encore, et qui viendra avec la table de scénarios : les
critères de sortie (« passe à l'exercice quand il reformule juste »). Pour
l'instant le scénario dit quoi faire et pourquoi, pas quand s'arrêter.
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
