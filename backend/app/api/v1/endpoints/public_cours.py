"""La page publique du cours exemple des ondes (https://moalim.online/cours-ondes/, 8 novembre 2026).

Sans compte : le visiteur est reconnu par un identifiant tiré au hasard dans son navigateur (`X-Visiteur`), qui sert
de clé à son suivi des acquis (`public-<id>`). Les mêmes services que le lecteur connecté répondent :
  - photo de la feuille de l'élève lue par l'OCR (`/ocr-reponse`, plafond « llm »), montrée dans le champ avant l'envoi ;
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
import json
import re
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.api.v1.endpoints import course_player as cp
from app.api.v1.endpoints.memoire import EvenementMemoire as memoire_evenement_corps

router = APIRouter(prefix="/public/cours-ondes", tags=["public"])

COURS = "phys_ch1_waves_exemple"
_DOSSIER_COURS = Path(__file__).resolve().parents[4] / "data" / "courses"
#: Les avis des profs qui relisent les cours sur le lien libre (10 novembre 2026), une ligne JSON par avis ; le
#: dernier avis d'un relecteur sur une diapositive remplace les précédents (`lire_avis`). Hors dépôt (data/ ignoré).
FICHIER_AVIS = Path(__file__).resolve().parents[4] / "data" / "avis_profs" / "avis.jsonl"
#: (nombre d'appels, fenêtre en secondes) par visiteur ET par adresse IP ; puis pour tous les visiteurs ensemble.
LIMITES = {"llm": (40, 3600), "voix": (200, 3600), "eveil": (30, 3600), "acquis": (300, 3600), "micro": (60, 3600),
           "avis": (400, 3600)}
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


def cours_publics() -> set[str]:
    """Les cours servis sur le lien libre : le cours exemple et chaque cours refait en mode concentration
    (`backend/data/courses/<matière>_chN_<clé>.json`, `mode: concentration`), brouillons compris : les profs les relisent
    avant leur validation."""
    ids = {COURS}
    for f in _DOSSIER_COURS.glob("*_ch*_*.json"):
        if f.stem.endswith("_course_v1") or "_script_" in f.stem:
            continue
        try:
            if json.loads(f.read_text(encoding="utf-8")).get("mode") == "concentration":
                ids.add(f.stem)
        except (OSError, ValueError):
            continue
    return ids


def _ce_cours(deck_id: str | None) -> None:
    if deck_id and not any(deck_id.startswith(c) for c in cours_publics()):
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


@router.post("/ocr-reponse")
async def ocr_reponse(body: cp.OcrReponseRequest, request: Request, x_visiteur: str | None = Header(default=None)):
    """« 📷 Photo » : la feuille de l'élève lue (Mistral OCR + DeepSeek), montrée dans le champ avant tout envoi."""
    if len(body.image_b64) > 6_000_000:
        raise HTTPException(413, "Image trop lourde.")
    _ce_cours(body.deck_id)
    return await cp.ocr_reponse(body, _autoriser("llm", _visiteur(x_visiteur), request))


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



# ── Mémoire longue (11 novembre 2026) : les rappels espacés et le cycle des blocs marchent aussi sur le lien libre,
# le visiteur à la place du compte (`public-<id>`). Pas de notification ici : pas d'écran d'accueil. ──

@router.get("/memoire/seance/{deck_id}")
async def memoire_seance(deck_id: str, request: Request, x_visiteur: str | None = Header(default=None)):
    from app.api.v1.endpoints import memoire
    _ce_cours(deck_id)
    return await memoire.debut_de_seance(deck_id, _autoriser("acquis", _visiteur(x_visiteur), request))


@router.post("/memoire/evenement")
async def memoire_evenement(body: memoire_evenement_corps, request: Request, x_visiteur: str | None = Header(default=None)):
    from app.api.v1.endpoints import memoire
    if body.evenement == "notification":
        raise HTTPException(400, "Pas de notification sur le lien libre")
    _ce_cours(body.cours_id)
    return await memoire.evenement(body, _autoriser("acquis", _visiteur(x_visiteur), request))

# ── Relecture par les profs (10 novembre 2026) : sur le lien libre, chaque diapositive reçoit un vote « bon » ou
# « à corriger » et un commentaire ; l'admin les lit dans le tableau de bord (onglet « Avis des profs »). ──

class Avis(BaseModel):
    deck_id: str = Field(..., min_length=3, max_length=80)
    slide_id: str = Field(..., min_length=1, max_length=120)
    slide_titre: str = Field(default="", max_length=300)
    position: int = Field(default=0, ge=0, le=1000)
    vote: str | None = Field(default=None, pattern="^(bon|mauvais)$")
    commentaire: str = Field(default="", max_length=4000)
    relecteur: str = Field(default="", max_length=80)


def lire_avis() -> list[dict]:
    """Tous les avis, le dernier d'un relecteur sur une diapositive seulement (les plus récents d'abord)."""
    if not FICHIER_AVIS.exists():
        return []
    derniers: dict[tuple, dict] = {}
    for ligne in FICHIER_AVIS.read_text(encoding="utf-8").splitlines():
        try:
            a = json.loads(ligne)
        except ValueError:
            continue
        if a.get("type") == "statut":          # l'admin a marqué l'avis corrigé / à faire
            cle = tuple(a.get("cle") or ())
            if cle in derniers:
                derniers[cle]["statut"] = a.get("statut", "a_faire")
            continue
        cle = (a.get("visiteur"), a.get("deck_id"), a.get("slide_id"))
        ancien = derniers.get(cle)
        a.setdefault("statut", ancien.get("statut", "a_faire") if ancien else "a_faire")
        derniers[cle] = a
    return sorted(derniers.values(), key=lambda a: a.get("date", ""), reverse=True)


def _ecrire(ligne: dict) -> None:
    FICHIER_AVIS.parent.mkdir(parents=True, exist_ok=True)
    with FICHIER_AVIS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")


@router.post("/avis")
async def donner_avis(body: Avis, request: Request, x_visiteur: str | None = Header(default=None)):
    visiteur = _visiteur(x_visiteur)
    _autoriser("avis", visiteur, request)
    _ce_cours(body.deck_id)
    if not body.vote and not body.commentaire.strip():
        raise HTTPException(400, "Avis vide")
    _ecrire({**body.model_dump(), "commentaire": body.commentaire.strip(), "relecteur": body.relecteur.strip(),
             "visiteur": visiteur, "date": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    return {"ok": True}


@router.get("/avis/{deck_id}")
async def mes_avis(deck_id: str, request: Request, x_visiteur: str | None = Header(default=None)):
    """Les avis que CE relecteur a déjà donnés sur ce cours (la page les remontre diapositive par diapositive)."""
    visiteur = _visiteur(x_visiteur)
    _autoriser("avis", visiteur, request)
    _ce_cours(deck_id)
    return {"avis": {a["slide_id"]: {"vote": a.get("vote"), "commentaire": a.get("commentaire", "")}
                     for a in lire_avis() if a.get("visiteur") == visiteur and a.get("deck_id") == deck_id}}


def marquer_avis(visiteur: str, deck_id: str, slide_id: str, statut: str) -> None:
    _ecrire({"type": "statut", "cle": [visiteur, deck_id, slide_id], "statut": statut,
             "date": datetime.now(timezone.utc).isoformat(timespec="seconds")})
