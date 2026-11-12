"""Mémoire longue (11 novembre 2026) : rappels espacés, cycle des blocs, traçabilité et notifications de l'élève.

Les routes sont sous `/course-player/memoire/…` : la page publique (`public_cours.py`) les sert aussi, sous
`/public/cours-ondes/memoire/…`, avec le visiteur à la place du compte. Tout passe par `suivi_acquis.enregistrer`
(un JSONL par élève, aucune table) ; le calcul est dans `services/memoire_longue.py`.
"""
from __future__ import annotations

from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.dependencies import get_current_student

router = APIRouter(prefix="/course-player/memoire", tags=["memoire"])


class EvenementMemoire(BaseModel):
    """Un moment du cycle (cahier, retrouver, exercice), d'un rappel, d'une séance, d'une saturation, d'une notification."""
    evenement: Literal["cahier", "retrouver", "exercice_bloc", "rappel", "saturation", "seance_debut", "seance_fin",
                       "notification", "pause"]
    cours_id: Optional[str] = Field(default=None, max_length=120)
    seance_id: Optional[str] = Field(default=None, max_length=120)
    bloc_id: Optional[str] = Field(default=None, max_length=120)
    competence_id: Optional[str] = Field(default=None, max_length=120)
    rappel_id: Optional[str] = Field(default=None, max_length=120)
    matiere: Optional[str] = Field(default=None, max_length=40)
    enonce: str = Field(default="", max_length=600)
    reponse: str = Field(default="", max_length=800)
    reponse_2: str = Field(default="", max_length=800)
    #: le premier essai ; `correct_2` : le second (un rappel réussi au 2ᵉ essai reste sur sa marche)
    correct: Optional[bool] = None
    correct_2: Optional[bool] = None
    #: l'élève a passé la question (bouton « Passer », avec `correct: null`) : ni réussie ni une erreur ; un rappel
    #: passé revient bientôt (retour à J+1, comme un raté, mais noté « passe »)
    passee: bool = False
    #: secondes : temps passé à écrire le cahier, à répondre, durée de la séance
    duree_s: Optional[float] = Field(default=None, ge=0, le=86400)
    en_avance: bool = False
    complete: bool = False
    #: saturation : `cause` (deux_fausses | trop_rapide | inactivite) et `action` (cahier | exercice | pause) ;
    #: notification : `action` (ouverte)
    cause: Optional[str] = Field(default=None, max_length=40)
    action: Optional[str] = Field(default=None, max_length=40)
    bloc_index: Optional[int] = Field(default=None, ge=0, le=50)
    seance_index: Optional[int] = Field(default=None, ge=0, le=50)
    type: Optional[str] = Field(default=None, max_length=20)


class Preferences(BaseModel):
    """L'élève choisit l'heure de son rappel ou coupe les notifications, d'un geste."""
    heure: Optional[int] = Field(default=None, ge=0, le=23)
    coupees: bool = False


def _sid(student: dict) -> str:
    return str(student["id"])


@router.get("/seance/{deck_id}")
async def debut_de_seance(deck_id: str, student: dict = Depends(get_current_student)):
    """Ce qui ouvre la séance : les rappels dus de la MÊME matière que ce cours, et où l'élève en est dans les blocs."""
    from app.services import memoire_longue as ml, suivi_acquis
    cours = ml.tous_les_cours()
    deck = cours.get(deck_id) or {}
    cid = ml.cours_id(deck_id, cours)
    matiere = ml.matiere_de(cid, deck)
    evs = suivi_acquis.lire(_sid(student))
    return {"cours_id": cid, "matiere": matiere, "rappels": ml.rappels_du_jour(evs, matiere, cours=cours),
            "progression": ml.progression(evs, deck) if deck else None}


@router.get("/rappels/{matiere}")
async def rappels(matiere: str, student: dict = Depends(get_current_student)):
    """Les rappels dus d'une matière : ce que la notification de l'écran d'accueil ouvre, d'un geste."""
    from app.services import memoire_longue as ml, suivi_acquis
    if matiere not in ml.MATIERES:
        raise HTTPException(404, "Matière inconnue")
    return ml.rappels_du_jour(suivi_acquis.lire(_sid(student)), matiere)


@router.post("/evenement")
async def evenement(body: EvenementMemoire, student: dict = Depends(get_current_student)):
    """Note un événement, daté, au même endroit que les réponses. Un rappel est enrichi par le serveur (marche, jours
    depuis la dernière fois, prochaine date) : l'élève apprend seulement « on la revoit bientôt » ou « à dans N jours »."""
    from app.services import memoire_longue as ml, suivi_acquis
    e = {k: v for k, v in body.model_dump().items()
         if k == "evenement" or not (v is None or v == "" or v is False) or (k == "correct" and body.evenement == "rappel")}
    sid = _sid(student)
    if body.evenement == "rappel":
        if not body.cours_id or not body.competence_id:
            raise HTTPException(400, "Rappel sans compétence")
        e = ml.enrichir_rappel(suivi_acquis.lire(sid), e)
    elif body.evenement == "notification" and body.action != "ouverte":
        raise HTTPException(400, "Seule l'ouverture d'une notification est notée par l'écran")
    elif body.cours_id:
        cours = ml.tous_les_cours()
        e["cours_id"] = ml.cours_id(body.cours_id, cours)
        e.setdefault("matiere", ml.matiere_de(e["cours_id"], cours.get(e["cours_id"])))
    suivi_acquis.enregistrer(sid, e)
    out = {"ok": True}
    if body.evenement == "rappel":
        out.update(marche=e.get("marche_apres"), prochaine=e.get("prochaine"))
    return out


@router.get("/accueil")
async def accueil(student: dict = Depends(get_current_student)):
    """Le badge et la bannière de l'écran d'accueil. La première bannière du jour est notée « envoyée »."""
    from app.services import memoire_longue as ml, suivi_acquis
    sid = _sid(student)
    a = ml.accueil(suivi_acquis.lire(sid))
    n = a.get("notification")
    if n and n.get("nouvelle"):
        suivi_acquis.enregistrer(sid, {"evenement": "notification", "action": "envoyee", "canal": "application",
                                       "matiere": n["matiere"], "nombre": n["nombre"], "niveau": n["niveau"]})
    return a


@router.post("/preferences")
async def changer_preferences(body: Preferences, student: dict = Depends(get_current_student)):
    from app.services import suivi_acquis
    suivi_acquis.enregistrer(_sid(student), {"evenement": "preferences", **body.model_dump()})
    return {"ok": True, **body.model_dump()}
