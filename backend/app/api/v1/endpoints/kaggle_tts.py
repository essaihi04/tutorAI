"""Le kernel Kaggle de la voix du prof annonce ici son état (démarrage, prêt
avec l'adresse de son tunnel, éteint). Pas de compte élève : il s'authentifie
avec la clé tirée au sort pour CE lancement (cf. app/services/kaggle_tts.py)."""
from fastapi import APIRouter, Depends, HTTPException, Request

from app.dependencies import get_current_student
from app.services.kaggle_tts import pilote

router = APIRouter(prefix="/tts-kaggle", tags=["tts"])


@router.post("/annonce")
async def annonce(request: Request):
    try:
        corps = await request.json()
    except ValueError:
        raise HTTPException(400, "JSON attendu")
    if not isinstance(corps, dict) or not await pilote.recevoir_annonce(corps):
        raise HTTPException(403, "annonce refusée")
    return {"ok": True}


@router.get("/etat", dependencies=[Depends(get_current_student)])
async def etat():
    """État de la voix (sans adresse ni jeton) : utile pour suivre le quota."""
    return pilote.resume()
