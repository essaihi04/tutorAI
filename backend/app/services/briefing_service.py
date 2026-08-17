"""Ce que le tuteur sait de l'élève AVANT que celui-ci ait parlé.

Le tuteur est un bon prof qui rencontre l'élève pour la première fois à
chaque connexion. Toutes les données existent — `student_proficiency_service`,
`study_plan_service`, `session_progress_service`, `subject_access_service` —
mais elles sont lues par des **pages React**, jamais injectées dans son
contexte. Il ne peut donc ni accueillir l'élève par son nom, ni dire « la
dernière fois tu bloquais sur les limites », ni décider quoi proposer.

Ce module produit ce briefing. Trois règles le tiennent :

**1. Un budget de caractères, tenu par un test.**
Le prompt de production fait déjà 82 000 caractères. Chaque service voudra
ajouter « juste une info utile », et le briefing grossira jusqu'à noyer le
reste. Le budget est donc une constante avec un test qui échoue quand on la
dépasse, et non une intention. Les sections sont écrites par ordre de valeur
décroissante : ce qui déborde est coupé par la fin, jamais tronqué au milieu
d'une phrase.

**2. Des faits, pas de conseils.**
`get_llm_context` produit déjà des `adaptation_hints` — plusieurs milliers de
caractères de stratégie pédagogique (ZPD, Bloom, urgence). Ce n'est pas le
même besoin et il ne faut surtout pas le refaire ici : le briefing dit QUI est
l'élève et OÙ il en est, en chiffres. Ce que le tuteur en fait le regarde.
Mélanger les deux, c'est reconstruire un prompt de 82 000 caractères.

**3. Ne lève jamais.**
Même principe que `tag_decoder` : une source indisponible dégrade le briefing,
elle n'empêche pas le cours de démarrer. Un tuteur qui ne connaît pas le score
de physique reste un tuteur ; un tuteur qui ne démarre pas n'est rien.

La collecte (I/O) et le formatage sont séparés : `_donnees_*` lit, `composer`
écrit. Le budget se teste donc sans base de données.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Optional

_log = logging.getLogger(__name__)


#: Taille maximale du briefing injecté dans le prompt. Voir règle 1.
BUDGET_CARACTERES = 800

#: Au-delà, l'élève ne lit plus la liste et le modèle non plus.
MAX_MATIERES = 4

#: Le résumé de la dernière séance est écrit par le modèle : il est
#: bavard par nature, on le coupe à la source plutôt que de laisser la
#: coupe budgétaire supprimer la section entière.
MAX_RESUME = 130


# ── Formatage ─────────────────────────────────────────────────────

def note_sur_20(pourcentage: float) -> str:
    """Un lycéen marocain pense en /20, pas en %.

    Le tableau de bord fait déjà cette conversion (`scoreOn20`) : le tuteur
    doit parler le même langage que l'écran, sinon l'élève voit deux chiffres
    différents pour la même chose.
    """
    note = round(float(pourcentage or 0) * 0.2, 1)
    return f"{int(note)}/20" if note == int(note) else f"{note}/20"


def _court(texte: str, maximum: int) -> str:
    texte = " ".join(str(texte or "").split())
    if len(texte) <= maximum:
        return texte
    return texte[: maximum - 1].rstrip(" ,;.") + "…"


@dataclass
class Donnees:
    """Les faits bruts, déjà extraits de leurs sources.

    Tout est optionnel : chaque champ absent fait disparaître sa ligne, ce
    qui est exactement le comportement voulu pour un élève qui vient de
    s'inscrire.
    """

    prenom: str = ""
    filiere: str = ""
    jours_avant_bac: Optional[int] = None
    #: [("Mathématiques", 65.0), ...] — score en pourcentage
    matieres: list[tuple[str, float]] = field(default_factory=list)
    #: Matières auxquelles l'élève a accès, quand aucun score n'existe encore
    matieres_sans_donnees: list[str] = field(default_factory=list)
    #: {"topic": ..., "subject": ..., "score": ...}
    lacune: Optional[dict[str, Any]] = None
    tendance: str = "stable"
    derniere_seance: str = ""
    prochaine_seance: str = ""


def _sections(d: Donnees) -> list[str]:
    """Les lignes du briefing, de la plus utile à la moins utile.

    L'ordre EST la politique de coupe : la ligne d'identité survit toujours,
    la séance planifiée est la première sacrifiée. Un tuteur qui connaît le
    prénom et l'échéance mais pas le planning reste utile ; l'inverse, non.
    """
    lignes: list[str] = []

    identite = ", ".join(p for p in (d.prenom, d.filiere) if p)
    if d.jours_avant_bac is not None and d.jours_avant_bac >= 0:
        echeance = f"J-{d.jours_avant_bac} avant le BAC"
        identite = f"{identite}. {echeance}" if identite else echeance
    if identite:
        lignes.append(identite.rstrip(".") + ".")

    if d.matieres:
        notes = " · ".join(
            f"{nom} {note_sur_20(pct)}" for nom, pct in d.matieres[:MAX_MATIERES]
        )
        lignes.append(f"Niveau : {notes}.")
    elif d.matieres_sans_donnees:
        inscrit = ", ".join(d.matieres_sans_donnees[:MAX_MATIERES])
        lignes.append(f"Aucun résultat encore. Matières : {inscrit}.")

    if d.lacune and d.lacune.get("topic"):
        matiere = d.lacune.get("subject") or ""
        score = d.lacune.get("score")
        detail = " ".join(
            p for p in (matiere, note_sur_20(score) if score is not None else "") if p
        )
        sujet = str(d.lacune["topic"])
        lignes.append(f"Bloque sur : {sujet}{f' ({detail})' if detail else ''}.")

    if d.tendance == "declining":
        lignes.append("Tendance : en baisse ces derniers jours.")
    elif d.tendance == "improving":
        lignes.append("Tendance : en progression.")

    if d.derniere_seance:
        lignes.append(f"Dernière séance : {_court(d.derniere_seance, MAX_RESUME)}")

    if d.prochaine_seance:
        lignes.append(f"Prévu aujourd'hui : {d.prochaine_seance}.")

    return lignes


@dataclass(frozen=True)
class Briefing:
    texte: str
    #: Les sections effectivement retenues, pour journaliser ce qui a été coupé.
    sections: tuple[str, ...]
    coupe: bool

    def __bool__(self) -> bool:
        return bool(self.texte)


def composer(donnees: Donnees, budget: int = BUDGET_CARACTERES) -> Briefing:
    """Assemble les sections tant que le budget le permet.

    On s'arrête à la PREMIÈRE section qui déborde plutôt que de continuer à
    chercher une suivante plus petite : garder l'ordre de priorité intact
    vaut mieux qu'un briefing plus rempli mais désordonné.
    """
    retenues: list[str] = []
    taille = 0
    coupe = False

    for ligne in _sections(donnees):
        cout = len(ligne) + (1 if retenues else 0)  # le saut de ligne
        if taille + cout > budget:
            coupe = True
            break
        retenues.append(ligne)
        taille += cout

    texte = "\n".join(retenues)
    if not retenues:
        # Une première ligne à elle seule plus longue que le budget ne doit
        # pas rendre le briefing vide : mieux vaut un prénom tronqué que rien.
        premieres = _sections(donnees)
        if premieres:
            texte = _court(premieres[0], budget)
            retenues = [texte]
            coupe = True

    return Briefing(texte=texte, sections=tuple(retenues), coupe=coupe)


# ── Collecte ──────────────────────────────────────────────────────

async def _rien(valeur: Any = None) -> Any:
    return valeur


async def _essayer(coroutine, defaut, quoi: str):
    """Aucune source ne peut empêcher la session de démarrer (règle 3)."""
    try:
        return await coroutine
    except Exception as exc:  # noqa: BLE001 — dégradation volontaire
        _log.warning("[Briefing] %s indisponible : %s", quoi, exc)
        return defaut


def _matieres_notees(resume: dict) -> list[tuple[str, float]]:
    """Les matières où l'élève a assez répondu pour qu'un score veuille dire
    quelque chose. Annoncer « Physique 4/20 » sur deux réponses est faux et
    décourageant."""
    matieres = (resume or {}).get("subjects") or {}
    notees = [
        (nom, float(data.get("score") or 0))
        for nom, data in matieres.items()
        if int(data.get("total") or 0) >= 3
    ]
    notees.sort(key=lambda item: item[1])  # le plus faible d'abord : c'est le sujet du jour
    return notees


def _derniere_seance(progressions: list[dict]) -> str:
    """`get_all_lesson_progress` est déjà trié par `updated_at` décroissant."""
    for ligne in progressions or []:
        resume = (ligne.get("last_ai_summary") or "").strip()
        if resume:
            return resume
        sujets = ligne.get("topics_covered") or []
        if sujets:
            return ", ".join(str(s) for s in sujets[:3])
    return ""


def _prochaine_seance(seances: list[dict]) -> str:
    for seance in seances or []:
        if (seance.get("status") or "") in ("completed", "skipped"):
            continue
        chapitre = ((seance.get("chapters") or {}).get("title_fr") or "").strip()
        matiere = ((seance.get("subjects") or {}).get("name_fr") or "").strip()
        minutes = seance.get("duration_minutes")
        titre = chapitre or matiere
        if not titre:
            continue
        details = [p for p in (matiere if chapitre else "", f"{minutes} min" if minutes else "") if p]
        return f"{titre} ({', '.join(details)})" if details else titre
    return ""


async def collecter(
    student_id: str,
    *,
    student: Optional[dict] = None,
    nom_complet: str = "",
    acces: Optional[dict] = None,
    resume_proficiency: Optional[dict] = None,
) -> Donnees:
    """Lit les sources et renvoie des faits bruts.

    `acces` et `resume_proficiency` sont des résultats DÉJÀ calculés que
    l'appelant peut prêter. Le handler de session tient les deux au démarrage,
    et `get_proficiency_summary` lit 500 réponses : le premier son arrive
    aujourd'hui à ~3 s, on ne rachète pas ce travail avec des requêtes
    redondantes.
    """
    from app.services.session_progress_service import session_progress_service
    from app.services.student_proficiency_service import proficiency_service
    from app.services.study_plan_service import study_plan_service
    from app.services.subject_access_service import subject_access_service

    resume, progressions, seances = await asyncio.gather(
        _essayer(
            _rien(resume_proficiency)
            if resume_proficiency is not None
            else proficiency_service.get_proficiency_summary(student_id),
            {},
            "profil de compétences",
        ),
        _essayer(
            session_progress_service.get_all_lesson_progress(student_id),
            [],
            "historique des leçons",
        ),
        _essayer(
            study_plan_service.get_today_schedule(student_id),
            [],
            "planning du jour",
        ),
    )

    if acces is None:
        acces = {}
        try:
            acces = (
                subject_access_service.get_context(student)
                if student
                else subject_access_service.get_context_for_student_id(student_id)
            )
        except Exception as exc:  # noqa: BLE001
            _log.warning("[Briefing] accès matières indisponible : %s", exc)

    try:
        jours = int(study_plan_service.calculate_days_until_exam())
    except Exception as exc:  # noqa: BLE001
        _log.warning("[Briefing] compte à rebours indisponible : %s", exc)
        jours = None

    nom = (nom_complet or str((student or {}).get("full_name") or "")).strip()
    lacunes = (resume or {}).get("lacunes") or []

    return Donnees(
        prenom=nom.split()[0] if nom else "",
        filiere=str(acces.get("filiere") or ""),
        jours_avant_bac=jours,
        matieres=_matieres_notees(resume),
        matieres_sans_donnees=[str(n) for n in (acces.get("subject_names") or []) if n],
        lacune=lacunes[0] if lacunes else None,
        tendance=str((resume or {}).get("recent_trend") or "stable"),
        derniere_seance=_derniere_seance(progressions),
        prochaine_seance=_prochaine_seance(seances),
    )


async def pour_eleve(
    student_id: str,
    *,
    student: Optional[dict] = None,
    nom_complet: str = "",
    acces: Optional[dict] = None,
    resume_proficiency: Optional[dict] = None,
    budget: int = BUDGET_CARACTERES,
) -> Briefing:
    """Le briefing prêt à injecter. Ne lève jamais."""
    try:
        donnees = await collecter(
            student_id,
            student=student,
            nom_complet=nom_complet,
            acces=acces,
            resume_proficiency=resume_proficiency,
        )
    except Exception as exc:  # noqa: BLE001
        _log.error("[Briefing] collecte impossible pour %s : %s", student_id, exc)
        return Briefing(texte="", sections=(), coupe=False)

    briefing = composer(donnees, budget=budget)
    if briefing.coupe:
        _log.info(
            "[Briefing] budget %d atteint, %d section(s) retenue(s)",
            budget,
            len(briefing.sections),
        )
    return briefing
