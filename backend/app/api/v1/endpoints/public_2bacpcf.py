"""Le lien libre des révisions de 2ᵉ Bac PC (https://moalim.online/2bacpcf/, 23 novembre 2026) : fiche et suivi.

Même principe que le Tronc Commun (`public_tronc_commun.py`, dont les outils sont repris) : hors de la base des élèves,
la fiche est remplie une seule fois (nom, prénom, classe 2BACPCF + numéro, père, téléphone) ; la même fiche redonne le
même identifiant. La page envoie le temps passé dans chaque séance, les diapositives vues, les réponses dans les cours et
les deux examens de 30 minutes (physique, chimie), une seule réponse comptée par question. L'admin lit tout dans
l'onglet « 2ᵉ Bac PC » (`/admin/2bacpcf`). Les examens sont toujours ouverts (pas de seuil de diapositives).

Données hors dépôt (data/ ignoré) : `data/2bacpcf/eleves.jsonl` et `suivi.jsonl`, une ligne JSON par événement.
"""
from __future__ import annotations

import json
import re
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Query, Request

from app.api.v1.endpoints import course_player as cp
from app.api.v1.endpoints import public_tronc_commun as tc

router = APIRouter(prefix="/public/2bacpcf", tags=["public"])

DOSSIER = Path(__file__).resolve().parents[4] / "data" / "2bacpcf"
ELEVES = DOSSIER / "eleves.jsonl"
SUIVI = DOSSIER / "suivi.jsonl"
PREFIXE_CLASSE = "2BACPCF"
#: chaque séance qui s'ouvre au tableau, et son nombre de diapositives (révisions allégées le 24/11 : 27 et 26)
COURS = {
    "rev_phys_ondes_radioactivite": ("Révision de physique", 27),
    "phys_ch3_ondes_lumineuses": ("Propagation d'une onde lumineuse", 68),
    "phys_ch4_radioactivite": ("Décroissance radioactive", 87),
    "rev_chim_deux_sens_equilibre": ("Révision de chimie", 26),
    "phys_ch11_transformations_deux_sens": ("Transformations dans les deux sens", 56),
    "phys_ch12_etat_equilibre": ("État d'équilibre", 58),
}
#: les deux examens de 30 minutes, chacun sur 20 points
EXAMENS = {"examen_physique": "Physique", "examen_chimie": "Chimie"}
TOTAL_EXAMEN = 20


def _ecrire(fichier: Path, ligne: dict) -> None:
    DOSSIER.mkdir(parents=True, exist_ok=True)
    with fichier.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")


def lire_eleves() -> dict[str, dict]:
    return {e["id"]: e for e in tc._lire(ELEVES) if e.get("id")}


def _eleve(eleve_id: Optional[str]) -> dict:
    e = lire_eleves().get(re.sub(r"[^a-f0-9-]", "", eleve_id or "")[:40])
    if not e:
        raise HTTPException(401, "Élève inconnu : remplis la fiche d'entrée.")
    return e


def classe_normale(c: str) -> str:
    """« 2bac pc 3 », « 2BACPCF-3 », « 3 » → « 2BACPCF 3 » ; sans numéro (le « 2 » de « 2bac » ne compte pas), telle quelle."""
    reste = re.sub(r"^\s*2\s*bac", "", c or "", flags=re.I)
    m = re.search(r"\d+", reste)
    return f"{PREFIXE_CLASSE} {int(m.group())}" if m else (c or "").strip()


@router.post("/inscription")
async def inscription(body: tc.Inscription, request: Request):
    """Une seule fiche par élève : même nom et même téléphone → le même identifiant (pas de doublon)."""
    tel = tc.telephone_normalise(body.telephone)
    if not tel:
        raise HTTPException(422, "Numéro de téléphone invalide (ex. 06 12 34 56 78).")
    complet = " ".join(f"{body.nom} {body.prenom}".split())
    cle = f"{tc._cle_nom(complet)}|{tel}"
    tc._autoriser("inscription", "2bac:" + cle, request)
    for e in lire_eleves().values():
        if e.get("cle") == cle:
            return {"eleve_id": e["id"], "nom": e["nom"], "classe": e["classe"], "deja": True}
    e = {"id": str(uuid.uuid4()), "cle": cle, "nom": complet, "nom_famille": " ".join(body.nom.split()),
         "prenom": " ".join(body.prenom.split()), "classe": classe_normale(body.classe),
         "pere": " ".join(body.pere.split()), "telephone": tel, "date": tc._maintenant()}
    _ecrire(ELEVES, e)
    return {"eleve_id": e["id"], "nom": e["nom"], "classe": e["classe"], "deja": False}


def _deja(eleve: str, body: tc.Evenement) -> bool:
    """Une seule réponse compte dans chaque tentative d'un examen (refaire l'examen en ouvre une nouvelle qui écrase
    l'ancienne, 25/11/2026) ; la première réponse à chaque question d'un cours."""
    if body.type.startswith("examen"):
        return tc.deja_dans_tentative(tc._lire(SUIVI), eleve, body)
    for ev in tc._lire(SUIVI):
        if ev.get("eleve") != eleve or ev.get("type") != body.type or ev.get("cours", "") != body.cours:
            continue
        if body.type == "reponse_cours" and ev.get("slide_id") == body.slide_id and ev.get("enonce", "") == body.enonce:
            return True
    return False


@router.post("/suivi")
async def suivi(body: tc.Evenement, request: Request, x_eleve: str | None = Header(default=None)):
    e = _eleve(x_eleve)
    tc._autoriser("suivi", e["id"], request)
    if body.cours and body.cours not in COURS and body.cours not in EXAMENS:
        raise HTTPException(404, "Cours introuvable")
    if body.type.startswith("examen") and body.cours not in EXAMENS:
        raise HTTPException(422, "Examen inconnu")
    if body.type in ("examen_debut", "examen_question", "examen_fin", "reponse_cours") and _deja(e["id"], body):
        return {"ok": True, "deja": True}
    if len(json.dumps(body.etat, ensure_ascii=False)) > 12000:
        raise HTTPException(413, "État trop grand")
    ligne = {k: v for k, v in body.model_dump().items() if v not in ("", None, [], 0, {}) or k in ("note", "correct")}
    _ecrire(SUIVI, {**ligne, "eleve": e["id"], "date": tc._maintenant()})
    return {"ok": True, "deja": False}


@router.get("/examen")
async def mon_examen(request: Request, cours: str = Query(default="examen_physique"), x_eleve: str | None = Header(default=None)):
    """Les questions déjà rendues de cet examen (la page les remontre, verrouillées), et s'il est fini. Toujours ouvert."""
    e = _eleve(x_eleve)
    tc._autoriser("suivi", e["id"], request)
    if cours not in EXAMENS:
        raise HTTPException(404, "Examen inconnu")
    debut, fini, questions = tc.etat_tentative(tc.tentative(tc._lire(SUIVI), e["id"], cours))
    return {"debut": debut, "fini": fini, "questions": questions, "ouvert": True}


@router.get("/a-retravailler")
async def a_retravailler(request: Request, x_eleve: str | None = Header(default=None)):
    """Les questions d'examen ratées et les réponses fausses dans les cours : la page mène chacune à sa diapositive."""
    e = _eleve(x_eleve)
    tc._autoriser("suivi", e["id"], request)
    return tc.a_retravailler_de(tc._lire(SUIVI), e["id"], EXAMENS, COURS)


@router.get("/reprise")
async def reprise(request: Request, x_eleve: str | None = Header(default=None)):
    """La dernière diapositive de chaque séance et les diapositives déjà vues : la page reprend le cours là."""
    e = _eleve(x_eleve)
    tc._autoriser("suivi", e["id"], request)
    return {"cours": tc.reprise_de(tc._lire(SUIVI), e["id"], COURS)}


@router.post("/answer-reaction")
async def answer_reaction(body: cp.AnswerReactionRequest, request: Request, x_eleve: str | None = Header(default=None)):
    """La correction d'une réponse rédigée (examens, questions des cours), plafonnée par élève inscrit."""
    e = _eleve(x_eleve)
    tc._autoriser("llm", e["id"], request)
    return await cp.answer_reaction(body, {"id": f"public-2bac-{e['id']}"})


def bilan() -> list[dict]:
    """Une ligne par élève : sa fiche, son temps et sa progression par séance, ses réponses dans les cours, ses deux
    examens (questions rendues, note, éléments du barème perdus) et ses lacunes. Tests et doublons signalés."""
    eleves = lire_eleves()
    par: dict[str, dict] = {i: {**{k: v for k, v in e.items() if k != "cle"}, "temps": defaultdict(int), "diapos": defaultdict(set),
                                "reponses_cours": {}, "ex": {x: {"questions": {}, "debut": None, "fin": None, "tentative": 1} for x in EXAMENS},
                                "derniere": e.get("date", "")}
                            for i, e in eleves.items()}
    for ev in tc._lire(SUIVI):
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
        elif cours in EXAMENS:
            x = b["ex"][cours]
            if t == "examen_reprise":   # l'élève refait l'examen : la nouvelle tentative écrase l'ancienne (25/11/2026)
                x.update(questions={}, debut=ev.get("date"), fin=None, tentative=x["tentative"] + 1)
            elif t == "examen_debut":
                x["debut"] = x["debut"] or ev.get("date")
            elif t == "examen_question":
                x["questions"].setdefault(ev.get("question_id", "?"), {
                    k: ev.get(k) for k in ("partie", "note", "sur", "verdict", "pertes", "enonce", "reponse", "date")})
            elif t == "examen_fin":
                x["fin"] = x["fin"] or {"date": ev.get("date")}
    out, vus = [], {}
    for b in sorted(par.values(), key=lambda x: x.get("date", "")):
        rep = list(b["reponses_cours"].values())
        fausses = [r for r in rep if r.get("correct") is False]
        examens = {}
        lacunes = []
        for cle, nom in EXAMENS.items():
            x = b["ex"][cle]
            qs = x["questions"]
            examens[cle] = {"nom": nom, "note": sum(q.get("note") or 0 for q in qs.values()),
                            "sur_fait": sum(q.get("sur") or 0 for q in qs.values()), "sur": TOTAL_EXAMEN,
                            "faites": len(qs), "fini": bool(x["fin"]), "debut": x["debut"],
                            "date": (x["fin"] or {}).get("date"), "questions": qs,
                            "tentative": x["tentative"]}
            lacunes += [f"{nom} Q{qid} : {p}" for qid, q in sorted(qs.items()) for p in (q.get("pertes") or [])]
        lacunes += [f"Cours — {r.get('titre') or r.get('slide_id')} : {r.get('enonce', '')[:120]}" for r in fausses[-15:]]
        classe = classe_normale(b.get("classe", ""))
        nom_cle = tc._cle_nom(b.get("nom", ""))
        test = not re.search(r"\d", classe) or "test" in nom_cle.split() or classe.lower() == "prof"
        doublon = vus.get(nom_cle) if nom_cle and not test else None
        if nom_cle and not test and not doublon:
            vus[nom_cle] = b["id"]
        out.append({
            **{k: b.get(k, "") for k in ("id", "nom", "pere", "telephone", "date", "derniere")},
            "classe": classe, "classe_ecrite": b.get("classe", ""), "test": test, "doublon_de": doublon,
            "temps": {c: b["temps"].get(c, 0) for c in [*COURS, *EXAMENS]},
            "progression": {c: {"vues": len(b["diapos"].get(c, ())), "total": n} for c, (_, n) in COURS.items()},
            "reponses_cours": {"total": len(rep), "justes": sum(1 for r in rep if r.get("correct") is True), "fausses": len(fausses)},
            "examens": examens, "lacunes": lacunes[:40],
        })
    return sorted(out, key=lambda x: x.get("derniere", ""), reverse=True)
