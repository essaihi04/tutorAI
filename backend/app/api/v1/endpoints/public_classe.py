"""Le mode classe du lien libre (24 novembre 2026) : une évaluation EN CLASSE, collective, question par question.

Le professeur projette une question (https://moalim.online/tronc-commun/?classe) ; les élèves répondent sur leur feuille ;
chacun (ou le prof, avec son téléphone, pour la feuille d'un élève) photographie la feuille sur `?c=<code>` : la photo est
lue (OCR), la réponse corrigée (barème, éléments perdus, correction), puis publiée au mur de la séance, que toute la classe
voit au tableau et sur son téléphone.

Demande de l'utilisateur : **rien d'enregistré**. Rien sur disque, rien en base, rien dans les comptes d'élèves : une séance
vit dans la mémoire du serveur (UN seul worker uvicorn en prod, un dictionnaire suffit) et disparaît après 4 h sans
activité, ou quand le prof la termine (il peut télécharger les résultats en CSV, fabriqué dans son navigateur).

Les élèves (25/11/2026) : en scannant le QR, chacun donne une fois son nom, son prénom et sa classe (facultative) ; un
téléphone = un élève (l'identifiant tiré au hasard, `X-Telephone`, gardé en sessionStorage, lie le nom). Chaque réponse
est rattachée à son élève : il remplace sa propre réponse à la même question au lieu d'en empiler.
Le téléphone du prof : l'écran du prof demande un jeton (4 chiffres, 2 minutes, une seule fois, montré en QR et en
chiffres) ; le téléphone qui le donne reçoit sa propre clé (`X-Prof-Tel`). Il saisit alors les réponses de plusieurs
élèves (ceux sans téléphone) : choisis dans la liste, ou nouveaux (`POST /{code}/eleve`), traités comme les autres.
L'écran du prof (`X-Prof`) et son téléphone voient les noms et toutes les réponses ; les téléphones des élèves voient la
liste des noms et le mur anonyme (« Réponse 1, 2… »).

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
MAX_PARTICIPANTS = 60
#: (nombre, fenêtre en secondes) — par séance, par adresse IP, pour tout le serveur
LIMITES_SEANCE = {"lire": (300, 3600), "corriger": (300, 3600), "reponse": (600, 3600), "participant": (300, 3600), "jeton": (20, 3600)}
#: le jeton qui relie le téléphone du prof : valable 2 minutes, une seule fois
DUREE_JETON = 120
LIMITES_IP = {"creer": (20, 3600), "lire": (900, 3600), "corriger": (900, 3600), "reponse": (2000, 3600), "inconnue": (120, 3600)}
LIMITES_TOTALES = {"lire": (5000, 86400), "corriger": (5000, 86400)}



@dataclass
class Reponse:
    id: str
    numero: int
    question: str
    telephone: str
    #: l'élève (identifiant de participant)
    eleve: str
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
class Participant:
    id: str
    nom: str
    prenom: str
    classe: str
    #: le téléphone de l'élève ('' : ajouté par le prof, sans téléphone)
    telephone: str


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
    participants: dict[str, Participant] = field(default_factory=dict)
    #: les questions déjà projetées, dans l'ordre (les résultats sont ramenés sur leurs points)
    posees: list[str] = field(default_factory=list)
    #: le jeton en cours pour relier le téléphone du prof : (jeton, fin)
    jeton: Optional[tuple[str, float]] = None
    #: les clés des téléphones du prof
    cles_tel: set = field(default_factory=set)
    #: « Je suis le professeur » sans code : téléphone → heure de la demande (l'écran du prof accepte ou refuse)
    demandes_prof: dict[str, float] = field(default_factory=dict)
    #: téléphone → sa clé de prof, acceptée par l'écran du prof et pas encore reprise par le téléphone ; ou "" : refusé
    reponses_prof: dict[str, str] = field(default_factory=dict)

    def est_prof(self, x_prof: Optional[str], x_prof_tel: Optional[str] = None) -> bool:
        if x_prof and secrets.compare_digest(x_prof.encode(), self.cle_prof.encode()):
            return True
        return bool(x_prof_tel) and any(secrets.compare_digest(x_prof_tel.encode(), c.encode()) for c in self.cles_tel)

    def eleve_du_telephone(self, tel: str) -> Optional[Participant]:
        return next((p for p in self.participants.values() if p.telephone and p.telephone == tel), None)

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


def _prof(s: Seance, x_prof: Optional[str], x_prof_tel: Optional[str] = None) -> None:
    if not s.est_prof(x_prof, x_prof_tel):
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
    if body.question not in s.posees:
        s.posees.append(body.question)
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


class Identite(BaseModel):
    nom: str = Field(..., min_length=1, max_length=60)
    prenom: str = Field(..., min_length=1, max_length=60)
    classe: str = Field(default="", max_length=20)


def _propre(x: str) -> str:
    return " ".join(str(x).split())[:60]


def _ajouter(s: Seance, ident: Identite, tel: str) -> Participant:
    nom, prenom = _propre(ident.nom), _propre(ident.prenom)
    if not nom or not prenom:
        raise HTTPException(422, "Écris ton nom et ton prénom.")
    if len(s.participants) >= MAX_PARTICIPANTS:
        raise HTTPException(507, f"La séance est complète ({MAX_PARTICIPANTS} élèves).")
    p = Participant(id=uuid.uuid4().hex[:8], nom=nom, prenom=prenom, classe=_propre(ident.classe)[:20], telephone=tel)
    s.participants[p.id] = p
    return p


def _vue_participant(p: Participant) -> dict:
    return {"id": p.id, "nom": p.nom, "prenom": p.prenom, "classe": p.classe}


@router.post("/{code}/participant")
async def participer(code: str, body: Identite, request: Request, x_telephone: str | None = Header(default=None)):
    """L'élève donne une fois son nom, son prénom et sa classe ; un téléphone = un élève (redonner son nom le corrige)."""
    s = _seance(code, request)
    tel = _telephone(x_telephone)
    _autoriser("participant", s, request)
    p = s.eleve_du_telephone(tel)
    if p is None:
        p = _ajouter(s, body, tel)
    else:
        p.nom, p.prenom, p.classe = _propre(body.nom), _propre(body.prenom), _propre(body.classe)[:20]
    s.toucher()
    return _vue_participant(p)


@router.post("/{code}/jeton-prof")
async def jeton_prof(code: str, request: Request, x_prof: str | None = Header(default=None)):
    """L'écran du prof : un jeton pour relier SON téléphone (4 chiffres, 2 minutes, une seule fois)."""
    s = _seance(code, request)
    _prof(s, x_prof)
    s.jeton = (f"{secrets.randbelow(10000):04d}", time.monotonic() + DUREE_JETON)
    s.toucher(changement=False)
    return {"jeton": s.jeton[0], "expiration_s": DUREE_JETON}


class Jeton(BaseModel):
    jeton: str = Field(..., pattern=r"^\d{4}$")


@router.post("/{code}/prof-telephone")
async def prof_telephone(code: str, body: Jeton, request: Request):
    """Le téléphone du prof donne le jeton : il reçoit sa clé de prof (le jeton ne sert plus)."""
    s = _seance(code, request)
    _autoriser("jeton", s, request)
    j = s.jeton
    if not j or time.monotonic() > j[1] or not secrets.compare_digest(body.jeton.encode(), j[0].encode()):
        raise HTTPException(403, "Code du prof faux ou expiré : affiche-le de nouveau sur l'écran du prof.")
    s.jeton = None
    if len(s.cles_tel) >= 5:
        raise HTTPException(507, "Trop de téléphones de prof pour cette séance.")
    cle = secrets.token_urlsafe(24)
    s.cles_tel.add(cle)
    s.toucher(changement=False)
    return {"cle": cle}


def _demandes(s: Seance) -> list[str]:
    """Les demandes « Je suis le professeur » de moins de 5 minutes."""
    t = time.monotonic()
    for tel in [x for x, h in s.demandes_prof.items() if t - h > 300]:
        del s.demandes_prof[tel]
    return list(s.demandes_prof)


@router.post("/{code}/demande-prof")
async def demander_prof(code: str, request: Request, x_telephone: str | None = Header(default=None)):
    """Le téléphone : « Je suis le professeur », sans code. L'écran du prof affiche « Accepter » (un clic)."""
    s = _seance(code, request)
    _autoriser("jeton", s, request)
    tel = _telephone(x_telephone)
    if tel not in s.demandes_prof:
        if len(_demandes(s)) >= 10:
            raise HTTPException(429, "Trop de demandes : réessaie dans un moment.")
        s.demandes_prof[tel] = time.monotonic()
        s.reponses_prof.pop(tel, None)
        s.toucher()
    return {"statut": "attente"}


@router.get("/{code}/demande-prof")
async def statut_demande_prof(code: str, request: Request, x_telephone: str | None = Header(default=None)):
    """Le téléphone attend : sa clé de prof quand l'écran a accepté (une seule fois), « refuse », ou « attente »."""
    s = _seance(code, request)
    tel = _telephone(x_telephone)
    if tel in s.reponses_prof:
        cle = s.reponses_prof.pop(tel)
        return {"statut": "accepte", "cle": cle} if cle else {"statut": "refuse"}
    return {"statut": "attente" if tel in _demandes(s) else "aucune"}


class Decision(BaseModel):
    telephone: str = Field(..., pattern=r"^[a-zA-Z0-9-]{1,40}$")
    accepter: bool


@router.post("/{code}/demande-prof/decision")
async def decider_prof(code: str, body: Decision, request: Request, x_prof: str | None = Header(default=None)):
    """L'écran du prof (lui seul) accepte ou refuse un téléphone."""
    s = _seance(code, request)
    if not x_prof or not secrets.compare_digest(x_prof.encode(), s.cle_prof.encode()):
        raise HTTPException(403, "Réservé à l'écran du prof.")
    if s.demandes_prof.pop(body.telephone, None) is None:
        raise HTTPException(404, "Demande introuvable ou trop ancienne.")
    if body.accepter:
        if len(s.cles_tel) >= 5:
            raise HTTPException(507, "Trop de téléphones de prof pour cette séance.")
        cle = secrets.token_urlsafe(24)
        s.cles_tel.add(cle)
        s.reponses_prof[body.telephone] = cle
    else:
        s.reponses_prof[body.telephone] = ""
    s.toucher()
    return {"ok": True}


@router.post("/{code}/eleve")
async def nouvel_eleve(code: str, body: Identite, request: Request, x_prof: str | None = Header(default=None),
                       x_prof_tel: str | None = Header(default=None)):
    """Le prof ajoute un élève sans téléphone (même nom et prénom : le même élève)."""
    s = _seance(code, request)
    _prof(s, x_prof, x_prof_tel)
    _autoriser("participant", s, request)
    p = _par_nom(s, body) or _ajouter(s, body, "")
    s.toucher()
    return _vue_participant(p)


def _par_nom(s: Seance, ident: Identite) -> Optional[Participant]:
    cle = (_propre(ident.nom).lower(), _propre(ident.prenom).lower())
    return next((p for p in s.participants.values() if (p.nom.lower(), p.prenom.lower()) == cle), None)


@router.delete("/{code}/participant/{pid}")
async def retirer_participant(code: str, pid: str, request: Request, x_prof: str | None = Header(default=None)):
    """Le prof retire un élève (nom mal écrit, doublon) et ses réponses."""
    s = _seance(code, request)
    _prof(s, x_prof)
    if s.participants.pop(pid, None) is None:
        raise HTTPException(404, "Élève introuvable")
    for rs in s.reponses.values():
        for rid in [r.id for r in rs.values() if r.eleve == pid]:
            rs.pop(rid, None)
    s.toucher()
    return {"ok": True}


def _vue(r: Reponse, telephone: str) -> dict:
    return {"id": r.id, "numero": r.numero, "question": r.question, "texte": r.texte, "note": r.note, "sur": r.sur,
            "verdict": r.verdict, "pertes": r.pertes, "bien": r.bien, "retour": r.retour, "image": r.image is not None,
            "mien": bool(telephone) and r.telephone == telephone}


@router.get("/{code}")
async def etat(code: str, request: Request, v: int = Query(default=0), x_telephone: str | None = Header(default=None),
               x_prof: str | None = Header(default=None), x_prof_tel: str | None = Header(default=None)):
    """L'état de la séance (interrogé toutes les 2 à 3 s) ; `?v=<version>` : rien de neuf → `{inchange: true}`.
    Le téléphone : son élève, la liste des noms, le mur anonyme. L'écran du prof (`X-Prof`) : en plus, l'élève de chaque
    réponse et toutes les réponses de la séance (pour les résultats de la classe)."""
    s = _seance(code, request)
    s.toucher(changement=False)
    if v and v == s.version:
        return {"version": s.version, "inchange": True}
    prof = s.est_prof(x_prof, x_prof_tel)
    tel = re.sub(r"[^a-zA-Z0-9-]", "", x_telephone or "")[:40]
    courantes = s.reponses.get(s.question, {})
    moi = s.eleve_du_telephone(tel) if tel else None
    d = {"code": s.code, "sujet": s.sujet, "version": s.version, "question": s.question, "correction": s.correction,
         "posees": s.posees, "participants": [_vue_participant(p) for p in s.participants.values()],
         "moi": _vue_participant(moi) if moi else None, "prof": prof,
         "reponses": [_vue(r, tel) | ({"eleve": r.eleve} if prof else {}) for r in sorted(courantes.values(), key=lambda r: r.numero)],
         "par_question": {q: len(rs) for q, rs in s.reponses.items() if rs}}
    if x_prof and secrets.compare_digest(x_prof.encode(), s.cle_prof.encode()):
        d["demandes_prof"] = _demandes(s)
    if prof:
        d["toutes"] = [_vue(r, "") | {"eleve": r.eleve} for rs in s.reponses.values() for r in rs.values()]
    return d


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
        "Rends le texte lu et, pour chaque dessin (courbe, histogramme, schéma, tableau…), son bloc [Dessin de l'élève : …].",
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
    texte = re.sub(r"\$+", "", str((r or {}).get("text") or (r or {}).get("markdown") or "")).strip()[:4000]
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
    texte: str = Field(default="", max_length=4000)
    note: Optional[float] = Field(default=None, ge=0, le=100)
    sur: float = Field(default=0, ge=0, le=100)
    verdict: Literal["juste", "partiel", "faux", "nonjuge", "regarder"]
    pertes: list[str] = Field(default_factory=list, max_length=12)
    bien: list[str] = Field(default_factory=list, max_length=12)
    retour: str = Field(default="", max_length=800)
    #: la miniature JPEG (base64, avec ou sans `data:image/jpeg;base64,`), 120 Ko au plus
    image_b64: Optional[str] = Field(default=None, max_length=200_000)
    #: le prof photographie la feuille d'un autre élève : choisi dans la liste…
    eleve: Optional[str] = Field(default=None, pattern=r"^[a-f0-9]{8}$")
    #: … ou un nouveau nom (élève sans téléphone)
    nouvel_eleve: Optional[Identite] = None


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
async def publier(code: str, body: Publication, request: Request, x_telephone: str | None = Header(default=None),
                  x_prof: str | None = Header(default=None), x_prof_tel: str | None = Header(default=None)):
    """La réponse corrigée, au mur de la séance (anonyme). Le même téléphone remplace sa réponse à la même question."""
    s = _seance(code, request)
    tel = _telephone(x_telephone)
    _autoriser("reponse", s, request)
    img = _image(body.image_b64)
    if (body.eleve or body.nouvel_eleve) and not s.est_prof(x_prof, x_prof_tel):
        raise HTTPException(403, "Seul le prof rend la feuille d'un autre élève.")
    if body.eleve:
        eleve = s.participants.get(body.eleve)
        if eleve is None:
            raise HTTPException(404, "Élève introuvable dans la séance.")
    elif body.nouvel_eleve:
        eleve = _par_nom(s, body.nouvel_eleve) or _ajouter(s, body.nouvel_eleve, "")
    else:
        eleve = s.eleve_du_telephone(tel)
        if eleve is None:
            raise HTTPException(409, "Écris d'abord ton nom et ton prénom.")
    rs = s.reponses.setdefault(body.question, {})
    ancienne = next((r for r in rs.values() if r.eleve == eleve.id), None)
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
    r = Reponse(id=uuid.uuid4().hex[:16], numero=numero, question=body.question, telephone=tel, eleve=eleve.id, texte=body.texte.strip(),
                note=body.note, sur=body.sur, verdict=body.verdict, pertes=[_ligne(x) for x in body.pertes if str(x).strip()],
                bien=[_ligne(x) for x in body.bien if str(x).strip()], retour=body.retour.strip(), image=img, quand=time.monotonic())
    rs[r.id] = r
    s.toucher()
    return {"id": r.id, "numero": r.numero, "eleve": eleve.id, "remplace": ancienne is not None, "version": s.version}
