"""Le kernel Kaggle de la voix du prof annonce ici son état (démarrage, prêt
avec l'adresse de son tunnel, éteint). Pas de compte élève : il s'authentifie
avec la clé tirée au sort pour CE lancement (cf. app/services/kaggle_tts.py)."""
import asyncio

from fastapi import APIRouter, Depends, HTTPException, Request

from app.dependencies import get_current_student
from app.services.kaggle_tts import _garder, pilote

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


@router.post("/reveil", dependencies=[Depends(get_current_student)])
async def reveil():
    """L'élève est sur le site (accueil, cours, tuteur) : on allume la voix
    AVANT qu'il ouvre une séance. Le démarrage à froid (~2 min 20) se passe
    pendant qu'il choisit son cours au lieu de se faire attendre à la première
    question. Un kernel déjà prêt est seulement gardé éveillé ; s'il ne sert
    pas, il s'éteint seul après la veille (5 min). Ne compte pas comme parole."""
    pilote.besoin_de_voix("page")
    cible = pilote.cible()
    if cible:
        asyncio.get_running_loop().create_task(_garder(*cible))
    return {"etat": pilote.etat}
