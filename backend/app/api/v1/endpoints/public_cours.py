"""La page publique du cours exemple des ondes (https://moalim.online/cours-ondes/, 8 novembre 2026).

Sans compte : le visiteur est reconnu par un identifiant tiré au hasard dans son navigateur (`X-Visiteur`), qui sert
de clé à son suivi des acquis (`public-<id>`). Les mêmes services que le lecteur connecté répondent :
  - questions libres (écrites, au micro — transcrites par Gemini 2.5 Flash —, ou en image), réexplication en
    cycles, réactions aux réponses et aux manipulations : DeepSeek ;
  - la voix du professeur : notre modèle sur Kaggle (`synthesize`), réveillé dès que la page s'ouvre (`/eveil`) ;
  - le suivi des acquis et le bilan de la fiche finale.

Ouvert à tous, donc borné : un seul cours, des tailles maximales, et des plafonds par visiteur (et par adresse) et
pour l'ensemble des visiteurs, pour que la page ne puisse ni vider le quota GPU de Kaggle (30 h par semaine) ni
faire exploser les appels au LLM.
"""
from __future__ import annotations

import asyncio
import base64
import re
import time
from collections import defaultdict, deque

from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.api.v1.endpoints import course_player as cp

router = APIRouter(prefix="/public/cours-ondes", tags=["public"])

COURS = "phys_ch1_waves_exemple"
#: (nombre d'appels, fenêtre en secondes) par visiteur ET par adresse IP ; puis pour tous les visiteurs ensemble.
LIMITES = {"llm": (40, 3600), "voix": (200, 3600), "eveil": (30, 3600), "acquis": (300, 3600), "micro": (60, 3600)}
LIMITES_TOTALES = {"llm": (1500, 86400), "voix": (6000, 86400), "eveil": (300, 86400), "micro": (2000, 86400)}
_appels: dict[tuple[str, str], deque] = defaultdict(deque)


def _visiteur(x_visiteur: str | None) -> str:
    v = re.sub(r"[^a-zA-Z0-9-]", "", x_visiteur or "")[:40]
    if len(v) < 8:
        raise HTTPException(400, "Visiteur inconnu")
    return v


def _ip(request: Request) -> str:
    return (request.headers.get("x-real-ip") or request.headers.get("x-forwarded-for", "").split(",")[0]
            or (request.client.host if request.client else "?")).strip()


def _compter(cle: str, quoi: str, limite: tuple[int, int]) -> bool:
    n, fenetre = limite
    q, maintenant = _appels[(quoi, cle)], time.monotonic()
    while q and maintenant - q[0] > fenetre:
        q.popleft()
    if len(q) >= n:
        return False
    q.append(maintenant)
    return True


def _autoriser(quoi: str, visiteur: str, request: Request) -> dict:
    if not (_compter("v:" + visiteur, quoi, LIMITES[quoi]) and _compter("ip:" + _ip(request), quoi, LIMITES[quoi])):
        raise HTTPException(429, "Trop de demandes : reprends dans un moment.")
    if quoi in LIMITES_TOTALES and not _compter("*", quoi, LIMITES_TOTALES[quoi]):
        raise HTTPException(429, "La page est très demandée : reprends un peu plus tard.")
    return {"id": f"public-{visiteur}"}


def _ce_cours(deck_id: str | None) -> None:
    if deck_id and not deck_id.startswith(COURS):
        raise HTTPException(404, "Cours introuvable")


@router.post("/eveil")
async def eveil(request: Request, x_visiteur: str | None = Header(default=None)):
    """La page vient de s'ouvrir (ou l'élève y travaille encore) : la voix Kaggle s'allume ou reste éveillée."""
    _autoriser("eveil", _visiteur(x_visiteur), request)
    from app.services.kaggle_tts import _garder, pilote
    pilote.besoin_de_voix("page")
    cible = pilote.cible()
    if cible:
        asyncio.get_running_loop().create_task(_garder(*cible))
    return {"etat": pilote.etat}


class Voix(BaseModel):
    text: str = Field(..., min_length=1, max_length=1500)
    language: str = "mixed"


@router.post("/voix")
async def voix(body: Voix, request: Request, x_visiteur: str | None = Header(default=None)):
    """Ce que le professeur répond, dit par notre voix (Kaggle) ; 503 si elle n'est pas encore prête (l'écrit reste)."""
    _autoriser("voix", _visiteur(x_visiteur), request)
    from app.services.tts_service import synthesize
    r = await synthesize(body.text, body.language if body.language in ("fr", "ar", "mixed") else "mixed")
    if not r.audio_b64:
        raise HTTPException(503, f"Voix indisponible (provider={r.provider})")
    return Response(content=base64.b64decode(r.audio_b64), media_type=r.mime or "audio/wav",
                    headers={"X-TTS-Provider": r.provider, "Cache-Control": "public, max-age=86400"})


@router.post("/question-eleve")
async def question_eleve(body: cp.QuestionEleveRequest, request: Request, x_visiteur: str | None = Header(default=None)):
    if body.audio_b64 and len(body.audio_b64) > 3_000_000:
        raise HTTPException(413, "Enregistrement trop long : une minute au plus.")
    if body.image_b64 and len(body.image_b64) > 6_000_000:
        raise HTTPException(413, "Image trop lourde.")
    _ce_cours(body.deck_id)
    return await cp.question_eleve(body, _autoriser("llm", _visiteur(x_visiteur), request))


@router.post("/question-eleve/explication")
async def question_eleve_explication(body: cp.ExplicationRequest, request: Request, x_visiteur: str | None = Header(default=None)):
    """Une notion de base : expliquée sur le tableau effacé (préparée pendant la brosse)."""
    _ce_cours(body.deck_id)
    return await cp.question_eleve_explication(body, _autoriser("llm", _visiteur(x_visiteur), request))


@router.post("/transcrire")
async def transcrire(body: cp.TranscrireRequest, request: Request, x_visiteur: str | None = Header(default=None)):
    """Ce que l'élève vient de dire au micro, transcrit par MoulSot v4 : il le voit dans le champ avant d'envoyer."""
    if len(body.audio_b64) > 3_000_000:
        raise HTTPException(413, "Enregistrement trop long : une minute au plus.")
    return await cp.transcrire(body, _autoriser("micro", _visiteur(x_visiteur), request))


@router.post("/reexplication")
async def reexplication(body: cp.ReexplicationRequest, request: Request, x_visiteur: str | None = Header(default=None)):
    _ce_cours(body.deck_id)
    return await cp.reexplication(body, _autoriser("llm", _visiteur(x_visiteur), request))


@router.post("/answer-reaction")
async def answer_reaction(body: cp.AnswerReactionRequest, request: Request, x_visiteur: str | None = Header(default=None)):
    return await cp.answer_reaction(body, _autoriser("llm", _visiteur(x_visiteur), request))


@router.post("/sim-reaction")
async def sim_reaction(body: cp.SimReactionRequest, request: Request, x_visiteur: str | None = Header(default=None)):
    return await cp.simulation_reaction(body, _autoriser("llm", _visiteur(x_visiteur), request))


@router.post("/acquis")
async def acquis(body: cp.AcquisEvent, request: Request, x_visiteur: str | None = Header(default=None)):
    _ce_cours(body.deck_id)
    return await cp.enregistrer_acquis(body, _autoriser("acquis", _visiteur(x_visiteur), request))


@router.get("/acquis/{deck_id}")
async def bilan(deck_id: str, request: Request, x_visiteur: str | None = Header(default=None)):
    _ce_cours(deck_id)
    return await cp.bilan_acquis(deck_id, _autoriser("acquis", _visiteur(x_visiteur), request))
