"""Le relais PC ↔ téléphone des liens libres (24 novembre 2026) : le téléphone de l'élève sert à répondre pour son PC.

L'élève travaille seul sur un PC (cours, évaluation) et répond sur sa feuille. Il choisit « 📱 Avec mon téléphone » : le PC
ouvre un canal → un code court (6 caractères faciles à lire, sans 0/O/1/I), un lien court et un QR code
(moalim.online/tronc-commun/?t=K7P4QX). Le téléphone le rejoint UNE SEULE FOIS ; ensuite :
  - le PC publie sa « vue » (`POST /{code}/vue`) : la question en cours, la liste des questions, le brouillon, le résultat…
    — un simple JSON que le serveur ne lit pas ; le téléphone l'affiche et la suit (`GET /{code}`, toutes les 1 à 2 s) ;
  - le téléphone envoie des messages (`POST /{code}/message`) : aller à une question, le texte tapé ou lu sur la photo de la
    feuille, les choix d'un QCM, « rendre » ; le PC les prend (`GET /{code}/messages`) et les applique — synchronisation
    dans les deux sens, sans nouveau code à chaque question.
La photo reste sur le téléphone : elle y est lue (OCR), le texte modifiable part au PC comme un texte tapé.

Rien sur disque, rien en base : un dictionnaire en mémoire (UN seul worker uvicorn en prod). Un canal vit tant qu'il sert
(3 h sans activité au plus) ; le PC peut le fermer (« Déconnecter le téléphone »). Ouvert à tous, donc borné : ouvertures
et messages par adresse IP et par canal, nombre de canaux, taille de la vue et des messages, messages en attente.

Les compteurs (`_compter`, `_ip`, `_appels`) servent aussi au mode classe (`public_classe`), autre cas d'usage du même
principe : un écran, des téléphones, un code court, tout en mémoire.
"""
from __future__ import annotations

import json
import re
import secrets
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Optional

from fastapi import APIRouter, Header, HTTPException, Query, Request
from pydantic import BaseModel

router = APIRouter(prefix="/public/relais", tags=["public"])

#: 6 caractères sans 0/O/1/I (ni L, ni U : moins de confusions à la lecture et à la frappe)
ALPHABET = "23456789ABCDEFGHJKMNPQRSTVWXYZ"
LONGUEUR = 6
EXPIRATION = 3 * 3600
MAX_CANAUX = 3000
MAX_VUE = 40_000
MAX_MESSAGE = 5_000
MAX_EN_ATTENTE = 60
#: le téléphone est « relié » s'il est venu dans ces dernières secondes
PRESENCE = 15
LIMITES_CANAL = {"message": (3000, 3600), "vue": (6000, 3600), "lire": (40, 3600)}
LIMITES_IP = {"ouvrir": (60, 3600), "message": (20000, 3600), "inconnu": (120, 3600), "lire": (300, 3600)}

_appels: dict[tuple[str, str], deque] = defaultdict(deque)


def _compter(cle: str, quoi: str, limite: tuple[int, int]) -> bool:
    """Fenêtre glissante en mémoire : `limite` = (nombre, secondes)."""
    n, fenetre = limite
    q, maintenant = _appels[(quoi, cle)], time.monotonic()
    while q and maintenant - q[0] > fenetre:
        q.popleft()
    if len(q) >= n:
        return False
    q.append(maintenant)
    return True


def _ip(request: Request) -> str:
    return (request.headers.get("x-real-ip") or request.headers.get("x-forwarded-for", "").split(",")[0]
            or (request.client.host if request.client else "?")).strip()


def _plafond(cle: str, quoi: str, limite: tuple[int, int]) -> None:
    if not _compter(cle, quoi, limite):
        raise HTTPException(429, "Trop de demandes : reprends dans un moment.")


@dataclass
class Canal:
    code: str
    cle_pc: str
    vue: dict = field(default_factory=dict)
    version: int = 1
    actif: float = field(default_factory=time.monotonic)
    #: dernière visite du téléphone (0 : pas encore venu)
    telephone_vu: float = 0.0
    messages: deque = field(default_factory=deque)
    numero: int = 0

    def toucher(self) -> None:
        self.actif = time.monotonic()


CANAUX: dict[str, Canal] = {}


def _purger() -> None:
    maintenant = time.monotonic()
    for code in [c for c, k in CANAUX.items() if maintenant - k.actif > EXPIRATION]:
        CANAUX.pop(code, None)


def normaliser(code: str) -> str:
    """« k7p-4qx », « K7P 4QX » → « K7P4QX » (majuscules, sans espace ni tiret)."""
    return re.sub(r"[\s-]", "", code or "").upper()[:12]


def _canal(code: str, request: Request) -> Canal:
    _purger()
    c = normaliser(code)
    k = CANAUX.get(c) if len(c) == LONGUEUR and all(x in ALPHABET for x in c) else None
    if k is None:
        _plafond("ip:" + _ip(request), "inconnu", LIMITES_IP["inconnu"])
        raise HTTPException(404, "Code inconnu ou expiré : regarde le code affiché sur ton PC.")
    return k


def _pc(k: Canal, x_pc: Optional[str]) -> None:
    if not x_pc or not secrets.compare_digest(x_pc.encode(), k.cle_pc.encode()):
        raise HTTPException(403, "Réservé au PC qui a ouvert le canal.")


def _taille(x: Any) -> int:
    return len(json.dumps(x, ensure_ascii=False))


@router.post("")
async def ouvrir(request: Request):
    """Le PC ouvre un canal : le code court à taper (ou le QR code à viser) sur le téléphone, et la clé secrète du PC."""
    _purger()
    _plafond("ip:" + _ip(request), "ouvrir", LIMITES_IP["ouvrir"])
    if len(CANAUX) >= MAX_CANAUX:
        raise HTTPException(503, "Trop de connexions en cours : reprends dans un moment.")
    for _ in range(50):
        code = "".join(secrets.choice(ALPHABET) for _ in range(LONGUEUR))
        if code not in CANAUX:
            break
    else:
        raise HTTPException(503, "Trop de connexions en cours : reprends dans un moment.")
    k = Canal(code=code, cle_pc=secrets.token_urlsafe(24))
    CANAUX[code] = k
    return {"code": code, "cle_pc": k.cle_pc, "expiration_s": EXPIRATION}


class Vue(BaseModel):
    vue: dict


@router.post("/{code}/vue")
async def publier_vue(code: str, body: Vue, request: Request, x_pc: str | None = Header(default=None)):
    """Ce que le PC montre (question en cours, liste des questions, brouillon, résultat) : le téléphone le suit."""
    k = _canal(code, request)
    _pc(k, x_pc)
    _plafond("c:" + k.code, "vue", LIMITES_CANAL["vue"])
    if _taille(body.vue) > MAX_VUE:
        raise HTTPException(413, "Vue trop lourde.")
    if body.vue != k.vue:
        k.vue, k.version = body.vue, k.version + 1
    k.toucher()
    return {"ok": True, "version": k.version}


@router.get("/{code}/messages")
async def messages(code: str, request: Request, x_pc: str | None = Header(default=None)):
    """Le PC prend les messages du téléphone (oubliés aussitôt) et sait si le téléphone est là."""
    k = _canal(code, request)
    _pc(k, x_pc)
    k.toucher()
    arrives = list(k.messages)
    k.messages.clear()
    vu = k.telephone_vu and time.monotonic() - k.telephone_vu < PRESENCE
    return {"messages": arrives, "telephone": bool(vu)}


@router.get("/{code}")
async def etat(code: str, request: Request, v: int = Query(default=0)):
    """Le téléphone : la vue du PC (interrogée toutes les 1 à 2 s) ; `?v=<version>` : rien de neuf → `{inchange: true}`."""
    k = _canal(code, request)
    k.telephone_vu = time.monotonic()
    k.toucher()
    if v and v == k.version:
        return {"version": k.version, "inchange": True}
    return {"code": k.code, "version": k.version, "vue": k.vue}


class Message(BaseModel):
    message: dict


@router.post("/{code}/message")
async def message(code: str, body: Message, request: Request):
    """Le téléphone : aller à une question, un texte (tapé, ou lu sur la photo), des choix, « rendre »."""
    k = _canal(code, request)
    _plafond("c:" + k.code, "message", LIMITES_CANAL["message"])
    _plafond("ip:" + _ip(request), "message", LIMITES_IP["message"])
    m = body.message
    if not re.fullmatch(r"[a-z_]{1,20}", str(m.get("type") or "")):
        raise HTTPException(422, "Message inconnu.")
    if _taille(m) > MAX_MESSAGE:
        raise HTTPException(413, "Message trop long.")
    # le texte tapé part à chaque pause de frappe : seul le dernier d'une rafale compte
    if m["type"] == "texte" and not m.get("rendre") and k.messages and k.messages[-1].get("type") == "texte" and not k.messages[-1].get("rendre"):
        k.messages.pop()
    if len(k.messages) >= MAX_EN_ATTENTE:
        raise HTTPException(429, "Ton PC ne répond pas : vérifie qu'il est toujours ouvert sur la page.")
    k.numero += 1
    k.messages.append({**m, "n": k.numero})
    k.telephone_vu = time.monotonic()
    k.toucher()
    return {"ok": True, "n": k.numero}


@router.post("/{code}/lire")
async def lire(code: str, request: Request):
    """27/11/2026 : le téléphone relié photographie la feuille (une réponse, ou tout l'exercice) ; la photo est lue ici,
    comme `/course-player/ocr-reponse` (Claude, règles du mode classe), et le texte revient au téléphone.
    Seulement pour le téléphone d'un canal ouvert (le code sert de clé), plafonné par canal et par adresse."""
    from app.api.v1.endpoints import course_player as cp

    k = _canal(code, request)
    _plafond("c:" + k.code, "lire", LIMITES_CANAL["lire"])
    _plafond("ip:" + _ip(request), "lire", LIMITES_IP["lire"])
    try:
        body = cp.OcrReponseRequest(**(await request.json()))
    except Exception:  # noqa: BLE001
        raise HTTPException(422, "Photo illisible.") from None
    k.telephone_vu = time.monotonic()
    k.toucher()
    return await cp.ocr_reponse(body, {"id": f"relais-{k.code}"})


@router.delete("/{code}")
async def fermer(code: str, request: Request, x_pc: str | None = Header(default=None)):
    """« Déconnecter le téléphone » : le canal est effacé tout de suite."""
    k = _canal(code, request)
    _pc(k, x_pc)
    CANAUX.pop(k.code, None)
    return {"ok": True}
