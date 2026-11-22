"""Le lien libre du Tronc Commun (https://moalim.online/tronc-commun/, 22 novembre 2026) : la fiche de l'élève et son suivi.

Hors de la base des élèves (demande de l'utilisateur : ni comptes, ni application) : avant d'entrer, l'élève donne une
seule fois son nom, sa classe, le nom de son père et le numéro de téléphone ; le navigateur garde son identifiant, et la
même fiche (même nom, même téléphone) redonne le même identifiant. Ensuite la page envoie son suivi : le temps passé dans
chaque cours, les diapositives vues, ses réponses dans les cours, chaque question de l'évaluation (note, éléments du
barème perdus) et la note finale. L'admin lit tout dans l'onglet « Tronc Commun » (`/admin/tronc-commun`).

Les corrections du tuteur passent par ici (`/answer-reaction`) et non par les routes du cours des ondes : une classe
partage souvent le même wifi, donc la même adresse IP ; le plafond est compté par élève inscrit, l'adresse a un plafond
large.

Données hors dépôt (data/ ignoré), une ligne JSON par événement, comme les avis des profs.
"""
from __future__ import annotations

import json
import re
import time
import unicodedata
import uuid
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, Field

from app.api.v1.endpoints import course_player as cp

router = APIRouter(prefix="/public/tronc-commun", tags=["public"])

DOSSIER = Path(__file__).resolve().parents[4] / "data" / "tronc_commun"
ELEVES = DOSSIER / "eleves.jsonl"
SUIVI = DOSSIER / "suivi.jsonl"
COURS = {"tc_svt_sortie_ecologique": "La sortie écologique", "tc_svt_facteurs_edaphiques": "Les facteurs édaphiques",
         "tc_svt_revision": "Révision avec le tuteur"}
#: (nombre, fenêtre en secondes) par élève, puis par adresse (large : toute une classe derrière le même wifi), puis total
LIMITES = {"inscription": (10, 3600), "suivi": (2000, 3600), "llm": (80, 3600)}
LIMITES_IP = {"inscription": (200, 3600), "suivi": (40000, 3600), "llm": (1500, 3600)}
LIMITES_TOTALES = {"llm": (6000, 86400)}
_appels: dict[tuple[str, str], deque] = defaultdict(deque)


def _compter(cle: str, quoi: str, limite: tuple[int, int]) -> bool:
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


def _autoriser(quoi: str, cle: str, request: Request) -> None:
    if not (_compter("e:" + cle, quoi, LIMITES[quoi]) and _compter("ip:" + _ip(request), quoi, LIMITES_IP[quoi])):
        raise HTTPException(429, "Trop de demandes : reprends dans un moment.")
    if quoi in LIMITES_TOTALES and not _compter("*", quoi, LIMITES_TOTALES[quoi]):
        raise HTTPException(429, "La page est très demandée : reprends un peu plus tard.")


def _maintenant() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _ecrire(fichier: Path, ligne: dict) -> None:
    DOSSIER.mkdir(parents=True, exist_ok=True)
    with fichier.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")


def _lire(fichier: Path) -> list[dict]:
    if not fichier.exists():
        return []
    out = []
    for ligne in fichier.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(ligne))
        except ValueError:
            continue
    return out


def telephone_normalise(t: str) -> str:
    """« +212 6 12-34-56-78 » → « 0612345678 » ; vide si ce n'est pas un numéro marocain plausible."""
    c = re.sub(r"\D", "", t or "")
    if c.startswith("00212"):
        c = "0" + c[5:]
    elif c.startswith("212") and len(c) == 12:
        c = "0" + c[3:]
    return c if re.fullmatch(r"0[5-7]\d{8}", c) else ""


def _cle_nom(nom: str) -> str:
    s = unicodedata.normalize("NFKD", nom or "").encode("ascii", "ignore").decode().lower()
    return " ".join(re.findall(r"[a-z0-9]+", s)) or (nom or "").strip().lower()


def lire_eleves() -> dict[str, dict]:
    return {e["id"]: e for e in _lire(ELEVES) if e.get("id")}


def _eleve(eleve_id: Optional[str]) -> dict:
    e = lire_eleves().get(re.sub(r"[^a-f0-9-]", "", eleve_id or "")[:40])
    if not e:
        raise HTTPException(401, "Élève inconnu : remplis la fiche d'entrée.")
    return e


class Inscription(BaseModel):
    nom: str = Field(..., min_length=2, max_length=80)
    classe: str = Field(..., min_length=1, max_length=40)
    pere: str = Field(..., min_length=2, max_length=80)
    telephone: str = Field(..., min_length=8, max_length=25)


@router.post("/inscription")
async def inscription(body: Inscription, request: Request):
    """Une seule fiche par élève : même nom et même téléphone → le même identifiant (pas de doublon)."""
    tel = telephone_normalise(body.telephone)
    if not tel:
        raise HTTPException(422, "Numéro de téléphone invalide (ex. 06 12 34 56 78).")
    cle = f"{_cle_nom(body.nom)}|{tel}"
    _autoriser("inscription", cle, request)
    for e in lire_eleves().values():
        if e.get("cle") == cle:
            return {"eleve_id": e["id"], "nom": e["nom"], "classe": e["classe"], "deja": True}
    e = {"id": str(uuid.uuid4()), "cle": cle, "nom": " ".join(body.nom.split()), "classe": " ".join(body.classe.split()),
         "pere": " ".join(body.pere.split()), "telephone": tel, "date": _maintenant()}
    _ecrire(ELEVES, e)
    return {"eleve_id": e["id"], "nom": e["nom"], "classe": e["classe"], "deja": False}


class Evenement(BaseModel):
    #: temps (secondes passées sur un cours ou l'évaluation), diapo (vue), reponse_cours, examen_question, examen_fin
    type: str = Field(..., pattern="^(temps|diapo|reponse_cours|examen_debut|examen_question|examen_fin)$")
    cours: str = Field(default="", max_length=60)
    secondes: int = Field(default=0, ge=0, le=600)
    slide_id: str = Field(default="", max_length=120)
    titre: str = Field(default="", max_length=300)
    position: int = Field(default=0, ge=0, le=1000)
    total: int = Field(default=0, ge=0, le=1000)
    enonce: str = Field(default="", max_length=500)
    reponse: str = Field(default="", max_length=800)
    correct: Optional[bool] = None
    question_id: str = Field(default="", max_length=20)
    partie: str = Field(default="", max_length=120)
    note: float = Field(default=0, ge=0, le=20)
    sur: float = Field(default=0, ge=0, le=20)
    verdict: str = Field(default="", max_length=20)
    pertes: list[str] = Field(default_factory=list, max_length=12)


@router.post("/suivi")
async def suivi(body: Evenement, request: Request, x_eleve: str | None = Header(default=None)):
    e = _eleve(x_eleve)
    _autoriser("suivi", e["id"], request)
    if body.cours and body.cours not in COURS and body.cours != "examen":
        raise HTTPException(404, "Cours introuvable")
    ligne = {k: v for k, v in body.model_dump().items() if v not in ("", None, [], 0) or k in ("note", "correct")}
    _ecrire(SUIVI, {**ligne, "eleve": e["id"], "date": _maintenant()})
    return {"ok": True}


@router.post("/answer-reaction")
async def answer_reaction(body: cp.AnswerReactionRequest, request: Request, x_eleve: str | None = Header(default=None)):
    """La correction d'une réponse rédigée (évaluation, questions du cours), plafonnée par élève inscrit."""
    e = _eleve(x_eleve)
    _autoriser("llm", e["id"], request)
    return await cp.answer_reaction(body, {"id": f"public-tc-{e['id']}"})


def bilan() -> list[dict]:
    """Une ligne par élève : sa fiche, son temps par cours, sa progression, ses réponses, son évaluation, ses lacunes."""
    eleves = lire_eleves()
    par: dict[str, dict] = {i: {**{k: v for k, v in e.items() if k != "cle"}, "temps": defaultdict(int), "diapos": defaultdict(set),
                                "total_diapos": {}, "reponses_cours": [], "examen": {}, "examens": [], "derniere": e.get("date", "")}
                            for i, e in eleves.items()}
    for ev in _lire(SUIVI):
        b = par.get(ev.get("eleve", ""))
        if not b:
            continue
        b["derniere"] = max(b["derniere"], ev.get("date", ""))
        t, cours = ev.get("type"), ev.get("cours", "")
        if t == "temps":
            b["temps"][cours] += int(ev.get("secondes", 0))
        elif t == "diapo":
            b["diapos"][cours].add(ev.get("slide_id", ""))
            if ev.get("total"):
                b["total_diapos"][cours] = ev["total"]
        elif t == "reponse_cours":
            b["reponses_cours"].append({k: ev.get(k) for k in ("cours", "slide_id", "titre", "enonce", "reponse", "correct", "date")})
        elif t == "examen_debut":
            b["examen"] = {"debut": ev.get("date"), "questions": {}}
        elif t == "examen_question":
            b["examen"].setdefault("questions", {})[ev.get("question_id", "?")] = {
                k: ev.get(k) for k in ("partie", "note", "sur", "verdict", "pertes", "enonce", "reponse", "date")}
        elif t == "examen_fin":
            b["examens"].append({"note": ev.get("note"), "sur": ev.get("sur"), "date": ev.get("date"),
                                 "questions": b["examen"].get("questions", {}), "debut": b["examen"].get("debut")})
    out = []
    for b in par.values():
        qs = b["examen"].get("questions", {}) if b["examen"] else {}
        en_cours = {"note": sum(q.get("note") or 0 for q in qs.values()), "sur": sum(q.get("sur") or 0 for q in qs.values()),
                    "faites": len(qs), "questions": qs, "debut": b["examen"].get("debut") if b["examen"] else None}
        lacunes = [f"Q{qid} : {p}" for qid, q in qs.items() for p in (q.get("pertes") or [])]
        fausses = [r for r in b["reponses_cours"] if r.get("correct") is False]
        lacunes += [f"Cours — {r.get('titre') or r.get('slide_id')} : {r.get('enonce', '')[:120]}" for r in fausses[-15:]]
        out.append({
            **{k: b[k] for k in ("id", "nom", "classe", "pere", "telephone", "date", "derniere")},
            "temps": {c: b["temps"].get(c, 0) for c in [*COURS, "examen"]},
            "progression": {c: {"vues": len(b["diapos"].get(c, ())), "total": b["total_diapos"].get(c, 0)} for c in COURS},
            "reponses_cours": {"total": len(b["reponses_cours"]), "justes": sum(1 for r in b["reponses_cours"] if r.get("correct") is True),
                               "fausses": len(fausses)},
            "examen_en_cours": en_cours, "examens": b["examens"], "lacunes": lacunes[:40],
        })
    return sorted(out, key=lambda x: x.get("derniere", ""), reverse=True)
