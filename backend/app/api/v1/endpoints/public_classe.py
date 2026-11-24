"""Le mode classe du lien libre (24 novembre 2026) : une évaluation EN CLASSE, collective, question par question.

Le professeur projette une question (https://moalim.online/tronc-commun/?classe) ; les élèves répondent sur leur feuille ;
chacun (ou le prof, avec son téléphone, pour la feuille d'un élève) photographie la feuille sur `?c=<code>` : la photo est
lue (OCR), la réponse corrigée (barème, éléments perdus, correction), puis publiée au mur de la séance, que toute la classe
voit au tableau et sur son téléphone.

Demande de l'utilisateur : **ni nom, ni enregistrement**. Rien sur disque, rien en base : une séance vit dans la mémoire du
serveur (UN seul worker uvicorn en prod, un dictionnaire suffit) et disparaît après 4 h sans activité, ou quand le prof la
termine. Les réponses sont anonymes (« Réponse 1, 2… ») ; un identifiant de téléphone tiré au hasard (`X-Telephone`, gardé
en sessionStorage) permet seulement de remplacer sa propre réponse à la même question au lieu d'en empiler.

Le serveur ne connaît pas le sujet (il est dans la page) : il garde l'identifiant de la question projetée et ce que les
téléphones publient. Ouvert à tous, donc borné : nombre de séances, créations par adresse, appels à l'OCR et au LLM par
séance (une classe de 40 sur le même wifi = une seule adresse : le plafond principal est celui de la séance), mémoire par
séance et totale, taille des miniatures.
"""
from __future__ import annotations

import base64
import re
import secrets
import time
import uuid
from dataclasses import dataclass, field
from typing import Literal, Optional

from fastapi import APIRouter, Header, HTTPException, Query, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.api.v1.endpoints import course_player as cp
#: les compteurs en mémoire sont ceux du relais photo (même principe : un écran, des téléphones, un code court)
from app.api.v1.endpoints.public_relais import _appels, _compter, _ip  # noqa: F401

router = APIRouter(prefix="/public/classe", tags=["public"])

#: une séance oubliée disparaît après 4 h sans activité
EXPIRATION = 4 * 3600
MAX_SEANCES = 150
#: une miniature (JPEG déjà réduit sur le téléphone, ~480 px)
MAX_IMAGE = 120_000
#: mémoire des miniatures : par séance (les plus anciennes, hors question projetée, sont lâchées d'abord), puis en tout
MAX_OCTETS_SEANCE = 12_000_000
MAX_OCTETS_TOTAL = 600_000_000
MAX_REPONSES_QUESTION = 120
#: (nombre, fenêtre en secondes) — par séance, par adresse IP, pour tout le serveur
LIMITES_SEANCE = {"lire": (300, 3600), "corriger": (300, 3600), "reponse": (600, 3600)}
LIMITES_IP = {"creer": (20, 3600), "lire": (900, 3600), "corriger": (900, 3600), "reponse": (2000, 3600), "inconnue": (120, 3600)}
LIMITES_TOTALES = {"lire": (5000, 86400), "corriger": (5000, 86400)}



@dataclass
class Reponse:
    id: str
    numero: int
    question: str
    telephone: str
    texte: str
    note: Optional[float]
    sur: float
    verdict: str
    pertes: list[str]
    bien: list[str]
    retour: str
    image: Optional[bytes]
    quand: float


@dataclass
class Seance:
    code: str
    cle_prof: str
    sujet: str
    question: str = ""
    correction: bool = False
    version: int = 1
    actif: float = field(default_factory=time.monotonic)
    #: question → identifiant de réponse → réponse (ordre d'arrivée)
    reponses: dict[str, dict[str, Reponse]] = field(default_factory=dict)
    numeros: dict[str, int] = field(default_factory=dict)

    def toucher(self, changement: bool = True) -> None:
        self.actif = time.monotonic()
        if changement:
            self.version += 1

    def octets(self) -> int:
        return sum(len(r.image or b"") for rs in self.reponses.values() for r in rs.values())


SEANCES: dict[str, Seance] = {}


def _autoriser(quoi: str, seance: Optional[Seance], request: Request) -> None:
    if seance is not None and quoi in LIMITES_SEANCE and not _compter("s:" + seance.code, quoi, LIMITES_SEANCE[quoi]):
        raise HTTPException(429, "La classe a fait beaucoup de demandes : reprends dans un moment.")
    if quoi in LIMITES_IP and not _compter("ip:" + _ip(request), quoi, LIMITES_IP[quoi]):
        raise HTTPException(429, "Trop de demandes : reprends dans un moment.")
    if quoi in LIMITES_TOTALES and not _compter("*", quoi, LIMITES_TOTALES[quoi]):
        raise HTTPException(429, "Le mode classe est très demandé : reprends un peu plus tard.")


def _purger() -> None:
    maintenant = time.monotonic()
    for code in [c for c, s in SEANCES.items() if maintenant - s.actif > EXPIRATION]:
        SEANCES.pop(code, None)


def _seance(code: str, request: Request) -> Seance:
    _purger()
    s = SEANCES.get(code) if re.fullmatch(r"\d{4}", code or "") else None
    if s is None:
        # deviner les codes au hasard : plafonné par adresse
        if not _compter("ip:" + _ip(request), "inconnue", LIMITES_IP["inconnue"]):
            raise HTTPException(429, "Trop de demandes : reprends dans un moment.")
        raise HTTPException(404, "Séance introuvable ou terminée : vérifie le code au tableau.")
    return s


def _prof(s: Seance, x_prof: Optional[str]) -> None:
    if not x_prof or not secrets.compare_digest(x_prof.encode(), s.cle_prof.encode()):
        raise HTTPException(403, "Réservé au professeur de la séance.")


def _telephone(x_telephone: Optional[str]) -> str:
    t = re.sub(r"[^a-zA-Z0-9-]", "", x_telephone or "")[:40]
    if len(t) < 8:
        raise HTTPException(400, "Téléphone inconnu : recharge la page.")
    return t


ID_QUESTION = r"^[A-Za-z0-9_.-]{1,20}$"


class Creation(BaseModel):
    #: le sujet projeté (« tc » : l'évaluation formative du Tronc Commun ; d'autres viendront, 2ᵉ Bac)
    sujet: str = Field(default="tc", pattern=r"^[a-z0-9_-]{1,30}$")


@router.post("")
async def creer(request: Request, body: Optional[Creation] = None):
    """Une nouvelle séance : le code à taper (4 chiffres) et la clé secrète du professeur."""
    _purger()
    _autoriser("creer", None, request)
    if len(SEANCES) >= MAX_SEANCES:
        raise HTTPException(503, "Trop de séances en cours : reprends dans un moment.")
    libres = [c for c in (f"{secrets.randbelow(9000) + 1000}" for _ in range(60)) if c not in SEANCES]
    if not libres:
        raise HTTPException(503, "Trop de séances en cours : reprends dans un moment.")
    s = Seance(code=libres[0], cle_prof=secrets.token_urlsafe(24), sujet=(body.sujet if body else "tc"))
    SEANCES[s.code] = s
    return {"code": s.code, "cle_prof": s.cle_prof, "sujet": s.sujet, "expiration_s": EXPIRATION}


class ChoixQuestion(BaseModel):
    question: str = Field(..., pattern=ID_QUESTION)


@router.post("/{code}/question")
async def projeter(code: str, body: ChoixQuestion, request: Request, x_prof: str | None = Header(default=None)):
    """La question projetée : les téléphones la suivent ; la correction est cachée à chaque changement."""
    s = _seance(code, request)
    _prof(s, x_prof)
    if s.question != body.question:
        s.question, s.correction = body.question, False
    s.toucher()
    return {"ok": True, "version": s.version}


class Montrer(BaseModel):
    montrer: bool


@router.post("/{code}/correction")
async def correction(code: str, body: Montrer, request: Request, x_prof: str | None = Header(default=None)):
    s = _seance(code, request)
    _prof(s, x_prof)
    s.correction = body.montrer
    s.toucher()
    return {"ok": True, "version": s.version}


@router.delete("/{code}")
async def terminer(code: str, request: Request, x_prof: str | None = Header(default=None)):
    """Fin de la séance : tout est effacé tout de suite."""
    s = _seance(code, request)
    _prof(s, x_prof)
    SEANCES.pop(s.code, None)
    return {"ok": True}


@router.delete("/{code}/reponse/{rid}")
async def retirer(code: str, rid: str, request: Request, x_prof: str | None = Header(default=None)):
    """Le prof retire une réponse du mur (photo hors sujet, doublon…)."""
    s = _seance(code, request)
    _prof(s, x_prof)
    for rs in s.reponses.values():
        if rs.pop(rid, None) is not None:
            s.toucher()
            return {"ok": True}
    raise HTTPException(404, "Réponse introuvable")


def _vue(r: Reponse, telephone: str) -> dict:
    return {"id": r.id, "numero": r.numero, "question": r.question, "texte": r.texte, "note": r.note, "sur": r.sur,
            "verdict": r.verdict, "pertes": r.pertes, "bien": r.bien, "retour": r.retour, "image": r.image is not None,
            "mien": bool(telephone) and r.telephone == telephone}


@router.get("/{code}")
async def etat(code: str, request: Request, v: int = Query(default=0), x_telephone: str | None = Header(default=None)):
    """L'état de la séance (interrogé toutes les 2 à 3 s) ; `?v=<version>` : rien de neuf → `{inchange: true}`."""
    s = _seance(code, request)
    s.toucher(changement=False)
    if v and v == s.version:
        return {"version": s.version, "inchange": True}
    tel = re.sub(r"[^a-zA-Z0-9-]", "", x_telephone or "")[:40]
    courantes = s.reponses.get(s.question, {})
    return {"code": s.code, "sujet": s.sujet, "version": s.version, "question": s.question, "correction": s.correction,
            "reponses": [_vue(r, tel) for r in sorted(courantes.values(), key=lambda r: r.numero)],
            "par_question": {q: len(rs) for q, rs in s.reponses.items() if rs}}


@router.get("/{code}/image/{rid}")
async def image(code: str, rid: str, request: Request):
    """La miniature d'une réponse (JPEG) ; l'identifiant change à chaque nouvelle réponse : mise en cache sans risque."""
    s = _seance(code, request)
    for rs in s.reponses.values():
        r = rs.get(rid)
        if r is not None and r.image:
            return Response(r.image, media_type="image/jpeg",
                            headers={"Cache-Control": "private, max-age=14400", "X-Content-Type-Options": "nosniff"})
    raise HTTPException(404, "Image introuvable")


class Lecture(BaseModel):
    """La photo de la feuille (réduite à ~1280 px sur le téléphone) et la question, pour bien lire."""
    image_b64: str = Field(..., min_length=10, max_length=3_000_000)
    image_mime: str = Field(default="image/jpeg", pattern=r"^image/(jpeg|png|webp)$")
    question: str = Field(default="", pattern=r"^[A-Za-z0-9_.-]{0,20}$")
    enonce: str = Field(default="", max_length=1500)
    titre: str = Field(default="", max_length=300)
    matiere: str = Field(default="svt", max_length=40)
    niveau: str = Field(default="Tronc Commun Sciences BIOF", max_length=80)


def contexte_lecture(body: Lecture) -> str:
    lignes = [
        f"C'est la photo de la feuille d'un élève de {body.niveau} (Maroc), en classe : sa réponse à une question d'évaluation, écrite à la main.",
        f"Matière : {body.matiere}." + (f" Partie : {body.titre}." if body.titre else ""),
        f"Question posée : {body.enonce}" if body.enonce else "",
        "Pour un QCM ou un vrai/faux, garde le repère de chaque proposition (a, b, c…) et la lettre ou le mot choisi (A, B, vrai, faux).",
        "Normalise les symboles et les unités (exposants en Unicode : m², 10⁻³ ; flèches →). Jamais de LaTeX ni de signe $.",
        "Garde les mots de l'élève et son raisonnement : ne corrige NI ses erreurs NI ses résultats, ne complète rien, n'ajoute aucune explication.",
        "Rends uniquement le texte lu.",
    ]
    return "\n".join(x for x in lignes if x)


@router.post("/{code}/lire")
async def lire(code: str, body: Lecture, request: Request):
    """La photo → le texte (Mistral OCR puis correction de la notation, comme `ocr-reponse`), montré avant tout envoi.
    La photo n'est pas gardée."""
    from app.services import ocr_service

    s = _seance(code, request)
    _autoriser("lire", s, request)
    s.toucher(changement=False)
    try:
        r = await ocr_service.extract_text_from_image(body.image_b64, body.image_mime, correct_math=True,
                                                      subject=body.matiere, contexte=contexte_lecture(body))
    except Exception:  # noqa: BLE001
        r = {}
    texte = re.sub(r"\$+", "", str((r or {}).get("text") or (r or {}).get("markdown") or "")).strip()[:3000]
    if not texte:
        raise HTTPException(422, "Je n’ai pas pu lire la photo : reprends-la de plus près, bien éclairée, ou écris la réponse.")
    return {"texte": texte}


@router.post("/{code}/corriger")
async def corriger(code: str, body: cp.AnswerReactionRequest, request: Request):
    """Une réponse rédigée, notée sur les éléments du barème (même logique que `answer-reaction`, un seul essai)."""
    s = _seance(code, request)
    _autoriser("corriger", s, request)
    s.toucher(changement=False)
    body.tentative = 2
    return await cp.answer_reaction(body, {"id": f"public-classe-{s.code}"})


class Publication(BaseModel):
    question: str = Field(..., pattern=ID_QUESTION)
    texte: str = Field(default="", max_length=3000)
    note: Optional[float] = Field(default=None, ge=0, le=100)
    sur: float = Field(default=0, ge=0, le=100)
    verdict: Literal["juste", "partiel", "faux", "nonjuge", "regarder"]
    pertes: list[str] = Field(default_factory=list, max_length=12)
    bien: list[str] = Field(default_factory=list, max_length=12)
    retour: str = Field(default="", max_length=800)
    #: la miniature JPEG (base64, avec ou sans `data:image/jpeg;base64,`), 120 Ko au plus
    image_b64: Optional[str] = Field(default=None, max_length=200_000)
    #: le prof photographie plusieurs feuilles : une nouvelle réponse au lieu de remplacer la précédente
    nouvelle: bool = False


def _image(b64: Optional[str]) -> Optional[bytes]:
    if not b64:
        return None
    try:
        brut = base64.b64decode(b64.split(",", 1)[-1], validate=False)
    except (ValueError, TypeError):
        raise HTTPException(422, "Image illisible.") from None
    if len(brut) > MAX_IMAGE:
        raise HTTPException(413, "Image trop lourde (120 Ko au plus).")
    if not brut.startswith(b"\xff\xd8\xff"):
        raise HTTPException(422, "L'image doit être un JPEG.")
    return brut


def _lacher_images(s: Seance, besoin: int) -> None:
    """Fait de la place : les miniatures les plus anciennes, hors question projetée, sont lâchées (le texte reste)."""
    total = sum(x.octets() for x in SEANCES.values())
    vieilles = sorted((r for q, rs in s.reponses.items() if q != s.question for r in rs.values() if r.image), key=lambda r: r.quand)
    for r in vieilles:
        if s.octets() + besoin <= MAX_OCTETS_SEANCE and total + besoin <= MAX_OCTETS_TOTAL:
            return
        total -= len(r.image or b"")
        r.image = None
    if s.octets() + besoin > MAX_OCTETS_SEANCE or total + besoin > MAX_OCTETS_TOTAL:
        raise HTTPException(507, "Le mur est plein : passe à la question suivante.")


def _ligne(x: str) -> str:
    return " ".join(str(x).split())[:300]


@router.post("/{code}/reponse")
async def publier(code: str, body: Publication, request: Request, x_telephone: str | None = Header(default=None)):
    """La réponse corrigée, au mur de la séance (anonyme). Le même téléphone remplace sa réponse à la même question."""
    s = _seance(code, request)
    tel = _telephone(x_telephone)
    _autoriser("reponse", s, request)
    img = _image(body.image_b64)
    rs = s.reponses.setdefault(body.question, {})
    ancienne = None if body.nouvelle else next((r for r in rs.values() if r.telephone == tel), None)
    if ancienne is None and len(rs) >= MAX_REPONSES_QUESTION:
        raise HTTPException(507, "Trop de réponses pour cette question.")
    garde = ancienne.image if ancienne is not None else None
    if ancienne is not None:
        ancienne.image = None  # la place qu'elle occupait est rendue avant de compter
    if img:
        try:
            _lacher_images(s, len(img))
        except HTTPException:
            if ancienne is not None:
                ancienne.image = garde
            raise
    if ancienne is not None:
        rs.pop(ancienne.id, None)
        numero = ancienne.numero
    else:
        s.numeros[body.question] = numero = s.numeros.get(body.question, 0) + 1
    r = Reponse(id=uuid.uuid4().hex[:16], numero=numero, question=body.question, telephone=tel, texte=body.texte.strip(),
                note=body.note, sur=body.sur, verdict=body.verdict, pertes=[_ligne(x) for x in body.pertes if str(x).strip()],
                bien=[_ligne(x) for x in body.bien if str(x).strip()], retour=body.retour.strip(), image=img, quand=time.monotonic())
    rs[r.id] = r
    s.toucher()
    return {"id": r.id, "numero": r.numero, "remplace": ancienne is not None, "version": s.version}
