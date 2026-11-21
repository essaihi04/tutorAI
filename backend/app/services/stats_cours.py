"""Les statistiques de lecture d'un cours, par élève (21 novembre 2026).

Demande de l'utilisateur : sur la carte du cours, le pourcentage vu et terminé ; un cours peut être lu plusieurs fois,
donc combien de fois, combien de temps, combien de compétences restent, et une barre des compétences acquises pour
que l'élève voie vite ses lacunes ; un bouton « Détails » avec des métriques et des graphiques.

Le lecteur envoie trois événements (POST /course-player/stats) :
  - « ouverture » : l'élève lance le cours (Commencer, Reprendre, Revoir, Recommencer) ;
  - « temps » : toutes les 30 s tant que le cours est lancé et l'onglet visible, avec la diapositive en cours ;
  - « terminaison » : il arrive au bout du cours (une lecture complète de plus).
Stockage comme le suivi des acquis : un fichier JSONL par élève dans `data/stats_cours/` (pas de table).
Les compétences viennent du suivi des acquis (`suivi_acquis.bilan`) sur la version allégée de chaque cours.
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

from app.services import suivi_acquis

DOSSIER = Path(__file__).resolve().parents[2] / "data" / "stats_cours"
COURS = Path(__file__).resolve().parents[2] / "data" / "courses"
TYPES = ("ouverture", "temps", "terminaison")
#: un battement couvre au plus 2 min : un onglet gelé puis réveillé ne compte pas des heures
SECONDES_MAX = 120
JOURS = 14


def _fichier(student_id: str) -> Path:
    DOSSIER.mkdir(parents=True, exist_ok=True)
    return DOSSIER / f"{suivi_acquis._nettoyer(student_id) or 'inconnu'}.jsonl"


def noter(student_id: str, deck_id: str, type_: str, slide_id: str = "", secondes: int = 0) -> None:
    if type_ not in TYPES or not deck_id:
        return
    e = {"type": type_, "deck_id": deck_id, "quand": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    if slide_id:
        e["slide_id"] = slide_id
    if type_ == "temps":
        e["secondes"] = max(0, min(SECONDES_MAX, int(secondes or 0)))
    with _fichier(student_id).open("a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")


def lire(student_id: str) -> list[dict]:
    p = _fichier(student_id)
    if not p.exists():
        return []
    out = []
    for ligne in p.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(ligne))
        except json.JSONDecodeError:
            continue
    return out


def resumer(evenements: list[dict], maintenant: Optional[datetime] = None) -> dict[str, dict]:
    """Par cours : ouvertures, lectures terminées, temps, diapositives vues, dernière fois, minutes des 14 derniers jours."""
    maintenant = maintenant or datetime.now(timezone.utc)
    jours = [(maintenant - timedelta(days=i)).date().isoformat() for i in range(JOURS - 1, -1, -1)]
    par: dict[str, dict[str, Any]] = {}
    for e in evenements:
        d = e.get("deck_id")
        if not d:
            continue
        s = par.setdefault(d, {"ouvertures": 0, "terminaisons": 0, "secondes": 0, "diapos": set(),
                               "premiere": None, "derniere": None, "par_jour": defaultdict(int)})
        quand = str(e.get("quand") or "")
        s["premiere"] = s["premiere"] or quand
        s["derniere"] = quand or s["derniere"]
        if e.get("slide_id"):
            s["diapos"].add(e["slide_id"])
        t = e.get("type")
        if t == "ouverture":
            s["ouvertures"] += 1
        elif t == "terminaison":
            s["terminaisons"] += 1
        elif t == "temps":
            sec = int(e.get("secondes") or 0)
            s["secondes"] += sec
            s["par_jour"][quand[:10]] += sec
    return {d: {"ouvertures": s["ouvertures"], "terminaisons": s["terminaisons"], "minutes": round(s["secondes"] / 60),
                "diapos_vues": sorted(s["diapos"]), "premiere": s["premiere"], "derniere": s["derniere"],
                "jours": [{"jour": j, "minutes": round(s["par_jour"].get(j, 0) / 60, 1)} for j in jours]}
            for d, s in par.items()}


# ── Les compétences de chaque cours (version allégée, gardée tant que le fichier ne change pas) ──────────────
_cache: dict[str, tuple[float, dict]] = {}


def _alleger(m: dict) -> dict:
    return {"id": m.get("id"), "stable_id": m.get("stable_id"), "title": m.get("title", ""),
            "competences": m.get("competences") or [],
            "activities": [{"id": a.get("id"), "title": a.get("title", ""),
                            "slides": [{"id": s.get("id"), "competence_ids": s.get("competence_ids") or []}
                                       for s in a.get("slides", [])]}
                           for a in m.get("activities", [])]}


def cours_alleges() -> dict[str, dict]:
    """{stable_id ou id : cours allégé} pour les cours de `data/courses/*.json`."""
    out: dict[str, dict] = {}
    for p in sorted(COURS.glob("*.json")):
        try:
            mtime = p.stat().st_mtime
            if p.name not in _cache or _cache[p.name][0] != mtime:
                m = json.loads(p.read_text(encoding="utf-8"))
                if not isinstance(m, dict) or "activities" not in m:
                    continue
                _cache[p.name] = (mtime, _alleger(m))
        except (OSError, json.JSONDecodeError):
            continue
        leger = _cache[p.name][1]
        for cle in (leger.get("stable_id"), leger.get("id")):
            if cle:
                out[str(cle)] = leger
    return out


#: les méthodes dites à l'élève lui-même (le suivi des acquis les nomme pour le tuteur, à la troisième personne)
POUR_L_ELEVE = {
    "simulation": "une simulation au tableau", "image": "une image commentée", "table": "un tableau comparatif",
    "schema": "un schéma", "scientific": "une figure scientifique", "aucun": "l'explication orale",
    "formules": "les formules écrites pas à pas", "tuteur_montre": "le tuteur qui te montre au tableau",
    "eleve_manipule": "une simulation que tu manipules toi-même", "variante": "une comparaison du tuteur",
    "exercice": "un exercice d'application", "question_cours": "une question de cours", "vrai_faux": "un vrai/faux",
    "qcm": "un QCM", "directe": "une réponse rédigée",
}


def competences(evenements_acquis: list[dict], deck: dict) -> dict:
    """Le résumé des compétences d'un cours pour la carte et le panneau Détails."""
    b = suivi_acquis.bilan(evenements_acquis, deck)
    liste = [{"id": c["id"], "label": c["label"], "statut": c["statut"], "score": c["score"],
              "reprendre_avec": [POUR_L_ELEVE.get(m, suivi_acquis.NOMS_METHODES.get(m, m)) for m in c.get("a_reprendre_avec", [])]}
             for c in b["competences"]]
    compte = {s: sum(1 for c in liste if c["statut"] == s) for s in ("acquis", "partiel", "non_acquis", "non_evalue")}
    return {"total": len(liste), **compte, "liste": liste}


def tableau(student_id: str) -> dict[str, dict]:
    """Pour chaque cours : statistiques de lecture + compétences. Clé : le stable_id (ou l'id) du cours."""
    stats = resumer(lire(student_id))
    acquis: dict[str, list[dict]] = defaultdict(list)
    for e in suivi_acquis.lire(student_id):
        acquis[str(e.get("deck_id") or "")].append(e)
    out: dict[str, dict] = {}
    vus: set[int] = set()
    for cle, deck in cours_alleges().items():
        if id(deck) in vus:
            continue
        vus.add(id(deck))
        cles = [str(k) for k in (deck.get("stable_id"), deck.get("id")) if k]
        evs = [e for k in cles for e in acquis.get(k, [])]
        st = next((stats[k] for k in cles if k in stats), None)
        nb = sum(len(a["slides"]) for a in deck["activities"])
        entree = {"stats": st, "competences": competences(evs, deck), "diapos": nb,
                  "vu_pourcent": min(100, round(len(st["diapos_vues"]) * 100 / nb)) if st and nb else 0}
        if st:
            entree["stats"] = {k: v for k, v in st.items() if k != "diapos_vues"}
        out[cles[0]] = entree
    return out
