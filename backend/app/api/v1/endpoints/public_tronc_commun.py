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
TOTAL_EXAMEN = 20
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
    #: 23/11/2026 : nom et prénom séparés et obligatoires (les anciennes fiches n'ont que `nom`)
    prenom: str = Field(default="", max_length=80)
    classe: str = Field(..., min_length=1, max_length=40)
    pere: str = Field(..., min_length=2, max_length=80)
    telephone: str = Field(..., min_length=8, max_length=25)


@router.post("/inscription")
async def inscription(body: Inscription, request: Request):
    """Une seule fiche par élève : même nom et même téléphone → le même identifiant (pas de doublon)."""
    tel = telephone_normalise(body.telephone)
    if not tel:
        raise HTTPException(422, "Numéro de téléphone invalide (ex. 06 12 34 56 78).")
    complet = " ".join(f"{body.nom} {body.prenom}".split())
    cle = f"{_cle_nom(complet)}|{tel}"
    _autoriser("inscription", cle, request)
    for e in lire_eleves().values():
        if e.get("cle") == cle:
            return {"eleve_id": e["id"], "nom": e["nom"], "classe": e["classe"], "deja": True}
    e = {"id": str(uuid.uuid4()), "cle": cle, "nom": complet, "nom_famille": " ".join(body.nom.split()),
         "prenom": " ".join(body.prenom.split()), "classe": classe_normale(body.classe),
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
    #: l'état affiché de la question de l'évaluation (verdict, détails du barème, tracés), pour la remontrer telle quelle
    etat: dict = Field(default_factory=dict)


def _deja(eleve: str, body: "Evenement") -> bool:
    """Une seule réponse compte (23/11/2026) : la première question rendue de l'évaluation, le premier début et la
    première fin, la première réponse à chaque question d'un cours."""
    for ev in _lire(SUIVI):
        if ev.get("eleve") != eleve or ev.get("type") != body.type:
            continue
        if body.type in ("examen_debut", "examen_fin"):
            return True
        if body.type == "examen_question" and ev.get("question_id") == body.question_id:
            return True
        if body.type == "reponse_cours" and ev.get("cours") == body.cours and ev.get("slide_id") == body.slide_id                 and ev.get("enonce", "") == body.enonce:
            return True
    return False


@router.post("/suivi")
async def suivi(body: Evenement, request: Request, x_eleve: str | None = Header(default=None)):
    e = _eleve(x_eleve)
    _autoriser("suivi", e["id"], request)
    if body.cours and body.cours not in COURS and body.cours != "examen":
        raise HTTPException(404, "Cours introuvable")
    if body.type in ("examen_debut", "examen_question", "examen_fin", "reponse_cours") and _deja(e["id"], body):
        return {"ok": True, "deja": True}
    if len(json.dumps(body.etat, ensure_ascii=False)) > 12000:
        raise HTTPException(413, "État trop grand")
    ligne = {k: v for k, v in body.model_dump().items() if v not in ("", None, [], 0, {}) or k in ("note", "correct")}
    _ecrire(SUIVI, {**ligne, "eleve": e["id"], "date": _maintenant()})
    return {"ok": True, "deja": False}


@router.get("/examen")
async def mon_examen(request: Request, x_eleve: str | None = Header(default=None)):
    """Les questions de l'évaluation déjà rendues par cet élève (la page les remontre, verrouillées), et s'il a fini."""
    e = _eleve(x_eleve)
    _autoriser("suivi", e["id"], request)
    questions, debut, fini = {}, False, False
    for ev in _lire(SUIVI):
        if ev.get("eleve") != e["id"]:
            continue
        if ev.get("type") == "examen_debut":
            debut = True
        elif ev.get("type") == "examen_question":
            questions.setdefault(ev.get("question_id", "?"), ev.get("etat") or {"fait": True, "note": ev.get("note", 0)})
        elif ev.get("type") == "examen_fin":
            fini = True
    prog = progression(e["id"])
    return {"debut": debut, "fini": fini, "questions": questions, "progression": prog,
            "ouvert": examen_ouvert(prog, bool(questions)), "seuil": SEUIL_OUVERTURE}


def reprise_de(suivi: list[dict], eleve: str, cours_connus) -> dict:
    """Où l'élève en est dans chaque cours (24/11/2026, « garder l'avancement de chaque élève, ne pas recommencer à
    zéro ») : la dernière diapositive ouverte et celles déjà vues, d'après le suivi ; le même élève les retrouve sur
    n'importe quel appareil."""
    out: dict[str, dict] = {}
    for ev in suivi:
        c = ev.get("cours", "")
        if ev.get("eleve") != eleve or ev.get("type") != "diapo" or c not in cours_connus or not ev.get("slide_id"):
            continue
        r = out.setdefault(c, {"derniere": "", "position": 0, "total": 0, "vues": []})
        r["derniere"], r["position"], r["total"] = ev["slide_id"], ev.get("position", 0), ev.get("total", 0)
        if ev["slide_id"] not in r["vues"]:
            r["vues"].append(ev["slide_id"])
    return out


def a_retravailler_de(suivi: list[dict], eleve: str, examens, cours_connus) -> dict:
    """Ce que l'élève doit retravailler (24/11/2026) : chaque question d'examen où il n'a pas eu tous les points (sa
    première réponse, avec les éléments du barème perdus) et chaque première réponse fausse dans un cours. La page mène
    de chaque ligne à la diapositive du cours qui l'explique."""
    questions: dict[tuple, dict] = {}
    fausses: dict[tuple, dict] = {}
    for ev in suivi:
        if ev.get("eleve") != eleve:
            continue
        c = ev.get("cours", "")
        if ev.get("type") == "examen_question" and c in examens:
            questions.setdefault((c, ev.get("question_id", "")), {
                "examen": c, "id": ev.get("question_id", ""), "note": ev.get("note") or 0, "sur": ev.get("sur") or 0,
                "pertes": ev.get("pertes") or [], "enonce": ev.get("enonce", "")})
        elif ev.get("type") == "reponse_cours" and c in cours_connus:
            cle = (c, ev.get("slide_id"), ev.get("enonce", ""))
            if cle not in fausses:
                fausses[cle] = {"cours": c, "slide_id": ev.get("slide_id", ""), "titre": ev.get("titre", ""),
                                "enonce": ev.get("enonce", ""), "correct": ev.get("correct")}
    return {"questions": [q for q in questions.values() if q["sur"] and q["note"] < q["sur"]],
            "cours": [{k: v for k, v in r.items() if k != "correct"} for r in fausses.values() if r["correct"] is False]}


@router.get("/a-retravailler")
async def a_retravailler(request: Request, x_eleve: str | None = Header(default=None)):
    e = _eleve(x_eleve)
    _autoriser("suivi", e["id"], request)
    return a_retravailler_de(_lire(SUIVI), e["id"], {"examen"}, COURS)


@router.get("/reprise")
async def reprise(request: Request, x_eleve: str | None = Header(default=None)):
    """La dernière diapositive de chaque cours et les diapositives déjà vues : la page reprend le cours là."""
    e = _eleve(x_eleve)
    _autoriser("suivi", e["id"], request)
    return {"cours": reprise_de(_lire(SUIVI), e["id"], COURS)}


@router.post("/answer-reaction")
async def answer_reaction(body: cp.AnswerReactionRequest, request: Request, x_eleve: str | None = Header(default=None)):
    """La correction d'une réponse rédigée (évaluation, questions du cours), plafonnée par élève inscrit."""
    e = _eleve(x_eleve)
    _autoriser("llm", e["id"], request)
    return await cp.answer_reaction(body, {"id": f"public-tc-{e['id']}"})


#: 23/11/2026 : les classes de Tronc Commun sciences BIOF ; l'élève ne tape que le numéro (« 12 » → « TCSF 12 »)
PREFIXE_CLASSE = "TCSF"
#: nombre de diapositives de chaque cours (quand la page ne l'a pas encore envoyé)
TOTAUX = {"tc_svt_sortie_ecologique": 35, "tc_svt_facteurs_edaphiques": 55, "tc_svt_revision": 15}
#: l'évaluation s'ouvre quand la révision OU un des deux cours est parcouru à ce point (diapositives vues / total)
SEUIL_OUVERTURE = 0.8


def classe_normale(c: str) -> str:
    """« Tc 12 », « TCSF-12 », « tcsf12 », « 12 » → « TCSF 12 » ; sans numéro, la classe telle qu'écrite (ex. « prof »)."""
    m = re.search(r"\d+", c or "")
    return f"{PREFIXE_CLASSE} {int(m.group())}" if m else (c or "").strip()


def progression(eleve: str) -> dict:
    vues: dict[str, set] = defaultdict(set)
    for ev in _lire(SUIVI):
        if ev.get("eleve") == eleve and ev.get("type") == "diapo" and ev.get("cours") in COURS:
            vues[ev["cours"]].add(ev.get("slide_id", ""))
    return {c: {"vues": len(vues.get(c, ())), "total": TOTAUX[c]} for c in COURS}


def examen_ouvert(prog: dict, deja_commence: bool) -> bool:
    """Ouvert après la révision ou un des deux cours (80 % des diapositives vues) ; un élève déjà commencé garde l'accès."""
    return deja_commence or any(p["vues"] >= SEUIL_OUVERTURE * p["total"] for p in prog.values())


def bilan() -> list[dict]:
    """Une ligne par élève : sa fiche, son temps par cours, sa progression, ses réponses, son évaluation, ses lacunes.
    Une seule réponse compte (la première), même pour les données d'avant le 23/11/2026 ; les comptes de test (classe
    sans numéro comme « prof », ou nom contenant « test ») et les doublons (même nom inscrit deux fois) sont signalés."""
    eleves = lire_eleves()
    par: dict[str, dict] = {i: {**{k: v for k, v in e.items() if k != "cle"}, "temps": defaultdict(int), "diapos": defaultdict(set),
                                "reponses_cours": {}, "questions": {}, "debut": None, "fin": None, "derniere": e.get("date", "")}
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
        elif t == "reponse_cours":
            b["reponses_cours"].setdefault((cours, ev.get("slide_id"), ev.get("enonce", "")),
                                           {k: ev.get(k) for k in ("cours", "slide_id", "titre", "enonce", "reponse", "correct", "date")})
        elif t == "examen_debut":
            b["debut"] = b["debut"] or ev.get("date")
        elif t == "examen_question":
            b["questions"].setdefault(ev.get("question_id", "?"), {
                k: ev.get(k) for k in ("partie", "note", "sur", "verdict", "pertes", "enonce", "reponse", "date")})
        elif t == "examen_fin":
            b["fin"] = b["fin"] or {"note": ev.get("note"), "sur": ev.get("sur"), "date": ev.get("date")}
    out, vus = [], {}
    for b in sorted(par.values(), key=lambda x: x.get("date", "")):
        qs = b["questions"]
        note = sum(q.get("note") or 0 for q in qs.values())
        rep = list(b["reponses_cours"].values())
        fausses = [r for r in rep if r.get("correct") is False]
        lacunes = [f"Q{qid} : {p}" for qid, q in sorted(qs.items()) for p in (q.get("pertes") or [])]
        lacunes += [f"Cours — {r.get('titre') or r.get('slide_id')} : {r.get('enonce', '')[:120]}" for r in fausses[-15:]]
        classe = classe_normale(b.get("classe", ""))
        nom_cle = _cle_nom(b.get("nom", ""))
        test = not re.search(r"\d", classe) or "test" in nom_cle.split() or classe.lower() == "prof"
        doublon = vus.get(nom_cle) if nom_cle and not test else None
        if nom_cle and not test and not doublon:
            vus[nom_cle] = b["id"]
        prog = {c: {"vues": len(b["diapos"].get(c, ())), "total": TOTAUX[c]} for c in COURS}
        examens = [{"note": note, "sur": TOTAL_EXAMEN, "date": b["fin"]["date"], "debut": b["debut"], "questions": qs}] if b["fin"] else []
        out.append({
            **{k: b.get(k, "") for k in ("id", "nom", "pere", "telephone", "date", "derniere")},
            "classe": classe, "classe_ecrite": b.get("classe", ""), "test": test, "doublon_de": doublon,
            "temps": {c: b["temps"].get(c, 0) for c in [*COURS, "examen"]},
            "progression": prog,
            "reponses_cours": {"total": len(rep), "justes": sum(1 for r in rep if r.get("correct") is True), "fausses": len(fausses)},
            "examen_en_cours": {"note": note, "sur": sum(q.get("sur") or 0 for q in qs.values()), "faites": len(qs), "questions": qs,
                                "debut": b["debut"]},
            "examens": examens, "lacunes": lacunes[:40],
        })
    # un doublon montre aussi qui il double (le plus ancien garde la ligne principale)
    return sorted(out, key=lambda x: x.get("derniere", ""), reverse=True)
