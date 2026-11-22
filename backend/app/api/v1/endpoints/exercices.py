"""Partie « Exercices » (22 novembre 2026) : résultats de l'élève et progression croisée cours + exercices."""
from typing import Literal, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.dependencies import get_current_student

router = APIRouter(prefix="/exercices", tags=["exercices"])


class ResultatQuestion(BaseModel):
    """Une réponse notée d'un exercice (dernier essai d'une question)."""
    exercice_id: str = Field(min_length=1, max_length=120)
    cours: str = Field(default="", max_length=120)
    matiere: str = Field(default="", max_length=40)
    niveau: Optional[str] = Field(default=None, max_length=20)
    mode: Literal["exercice", "similaire"] = "exercice"
    question_id: str = Field(min_length=1, max_length=20)
    tentative: int = Field(default=1, ge=1, le=5)
    note: float = Field(default=0, ge=0, le=20)
    sur: float = Field(default=0, ge=0, le=20)
    juste: Optional[bool] = None
    partiel: bool = False
    aides: int = Field(default=0, ge=0, le=10)
    explication: bool = False
    facile: bool = False
    pertes: list[str] = Field(default_factory=list, max_length=8)


@router.post("/resultat")
async def enregistrer_resultat(body: ResultatQuestion, student: dict = Depends(get_current_student)):
    from app.services import resultats_exercices as rx
    e = body.model_dump()
    e["pertes"] = [str(p)[:160] for p in e["pertes"]]
    e["note"] = min(e["note"], e["sur"]) if e["sur"] else e["note"]
    rx.enregistrer(str(student["id"]), e)
    return {"ok": True}


@router.get("/progression")
async def progression(student: dict = Depends(get_current_student)):
    """Notes par exercice, par cours et par matière (cours + exercices), points forts, lacunes, points perdus."""
    from app.services import resultats_exercices as rx
    return rx.progression(str(student["id"]))
