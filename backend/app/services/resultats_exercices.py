"""Résultats des exercices et progression de l'élève (22 novembre 2026, partie « Exercices »).

Chaque réponse notée d'un exercice est un événement (une ligne JSON par élève, comme le suivi des acquis) :
  exercice_id, cours, matiere, niveau, mode (exercice | similaire), question_id, tentative, note, sur, juste, partiel,
  aides (nombre demandées), explication (vue), facile (vue), pertes (ce qui a coûté des points).
La progression croise ces notes avec les résultats du cours (compétences du suivi des acquis, `stats_cours.tableau`) :
note par exercice, par cours et par matière (sur 20), points forts, lacunes et ce qui fait perdre des points.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

DOSSIER = Path(__file__).resolve().parents[2] / "data" / "resultats_exercices"
INDEX = Path(__file__).resolve().parents[3] / "frontend" / "public" / "media" / "exercices" / "index.json"
MATIERE_DU_COURS = (("math_", "mathematiques"), ("phys_", "physique"), ("svt_", "svt"))
NOMS_MATIERES = {"mathematiques": "Mathématiques", "physique": "Physique-chimie", "svt": "SVT"}
# part des exercices dans la note d'un cours quand les deux existent (le cours compte pour le reste)
POIDS_EXERCICES = 0.6
SEUIL_FORT, SEUIL_FAIBLE = 0.75, 0.5


def _nettoyer(s: Any) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "", str(s or ""))[:80]


def _fichier(student_id: str) -> Path:
    DOSSIER.mkdir(parents=True, exist_ok=True)
    return DOSSIER / f"{_nettoyer(student_id) or 'inconnu'}.jsonl"


def enregistrer(student_id: str, evenement: dict) -> dict:
    e = {**evenement, "quand": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    with _fichier(student_id).open("a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return e


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


def catalogue() -> list[dict]:
    try:
        return json.loads(INDEX.read_text(encoding="utf-8")).get("exercices", [])
    except (OSError, json.JSONDecodeError):
        return []


def matiere_du_cours(cours_id: str) -> str:
    return next((m for p, m in MATIERE_DU_COURS if str(cours_id).startswith(p)), "autre")


def _r(x: Optional[float], n: int = 2) -> Optional[float]:
    return None if x is None else round(x, n)


def par_exercice(evenements: list[dict], cat: list[dict]) -> dict[str, dict]:
    """Pour chaque exercice : la note de chaque question (dernier essai jugé, mode « exercice »), la note totale, la
    part faite, le statut ; et le résultat de l'exercice semblable (fait seul : preuve d'acquisition)."""
    infos = {f["id"]: f for f in cat}
    dernier: dict[tuple[str, str, str], dict] = {}
    for e in evenements:
        cle = (str(e.get("exercice_id") or ""), str(e.get("mode") or "exercice"), str(e.get("question_id") or ""))
        if cle[0] and cle[2]:
            dernier[cle] = e                      # le plus récent l'emporte (fichier dans l'ordre)
    par: dict[str, dict] = {}
    for (ex, mode, q), e in dernier.items():
        d = par.setdefault(ex, {"exercice": {}, "similaire": {}})
        d[mode if mode in d else "exercice"][q] = e
    out = {}
    for ex, d in par.items():
        f = infos.get(ex, {})
        nq = int(f.get("questions") or 0) or len(d["exercice"]) or 1
        fiche = {"id": ex, "titre": f.get("titre", ex), "cours": f.get("cours") or next((e.get("cours") for e in d["exercice"].values()), ""),
                 "niveau": f.get("niveau"), "questions": nq}
        for mode in ("exercice", "similaire"):
            qs = d[mode]
            note = sum(float(e.get("note") or 0) for e in qs.values())
            sur_fait = sum(float(e.get("sur") or 0) for e in qs.values())
            # barème total estimé : la moyenne par question faite × le nombre de questions
            sur = sur_fait / len(qs) * nq if qs else 0.0
            fiche[mode] = {"faites": len(qs), "note": _r(note), "sur": _r(sur), "sur_fait": _r(sur_fait),
                           "pourcent": _r(note / sur if sur else None), "reussite": _r(note / sur_fait if sur_fait else None),
                           "aides": sum(int(e.get("aides") or 0) for e in qs.values()),
                           "explications": sum(1 for e in qs.values() if e.get("explication")),
                           "pertes": [p for e in qs.values() for p in (e.get("pertes") or []) if p][:12]}
        x = fiche["exercice"]
        fini = x["faites"] >= nq
        fiche["statut"] = ("a_faire" if not x["faites"] else "en_cours" if not fini
                           else "reussi" if (x["pourcent"] or 0) >= SEUIL_FORT else "a_revoir" if (x["pourcent"] or 0) < SEUIL_FAIBLE else "moyen")
        s = fiche["similaire"]
        fiche["acquis"] = s["faites"] >= nq and (s["pourcent"] or 0) >= SEUIL_FORT
        out[ex] = fiche
    return out


def progression(student_id: str) -> dict:
    """Notes par exercice, par cours (cours + exercices, sur 20) et par matière ; points forts, lacunes, pertes."""
    from app.services import stats_cours
    cat = catalogue()
    exos = par_exercice(lire(student_id), cat)
    try:
        cours_stats = stats_cours.tableau(student_id, avec_vues=True)
    except Exception:  # noqa: BLE001 — un cours illisible ne doit pas priver l'élève de ses exercices
        cours_stats = {}
    # les cours du programme qui ont des exercices (les anciens cours de démonstration n'entrent pas dans les notes)
    tous_cours = sorted({f.get("cours") for f in cat if f.get("cours")})
    par_cours = {}
    for c in tous_cours:
        if not c or matiere_du_cours(c) == "autre":
            continue
        st = cours_stats.get(c) or {}
        comp = st.get("competences") or {}
        evalues = (comp.get("acquis", 0) + comp.get("partiel", 0) + comp.get("non_acquis", 0))
        p_cours = (comp.get("acquis", 0) + 0.5 * comp.get("partiel", 0)) / evalues if evalues else None
        ex_c = [x for x in exos.values() if x["cours"] == c and x["exercice"]["faites"]]
        note_ex = sum(x["exercice"]["note"] or 0 for x in ex_c)
        # la réussite sur les questions faites : un exercice commencé ne fait pas baisser la note du cours
        sur_ex = sum(x["exercice"]["sur_fait"] or 0 for x in ex_c)
        p_ex = note_ex / sur_ex if sur_ex else None
        p = (POIDS_EXERCICES * p_ex + (1 - POIDS_EXERCICES) * p_cours if p_ex is not None and p_cours is not None
             else p_ex if p_ex is not None else p_cours)
        par_cours[c] = {
            "cours": c, "titre": st.get("titre") or c, "matiere": matiere_du_cours(c),
            "cours_pourcent": _r(p_cours), "cours_vu_pourcent": st.get("vu_pourcent", 0),
            "competences": {k: comp.get(k, 0) for k in ("total", "acquis", "partiel", "non_acquis", "non_evalue")},
            "exercices_faits": len(ex_c), "exercices_total": sum(1 for f in cat if f.get("cours") == c),
            "exercices_reussis": sum(1 for x in ex_c if x["statut"] == "reussi"),
            "exercices_pourcent": _r(p_ex), "pourcent": _r(p), "note20": _r(p * 20 if p is not None else None, 1),
            "lacunes_cours": [x["label"] for x in (comp.get("liste") or []) if x.get("statut") == "non_acquis"][:6],
            "forces_cours": [x["label"] for x in (comp.get("liste") or []) if x.get("statut") == "acquis"][:6],
        }
    par_matiere = {}
    for m, nom in NOMS_MATIERES.items():
        cs = [v for v in par_cours.values() if v["matiere"] == m]
        notes = [v["pourcent"] for v in cs if v["pourcent"] is not None]
        p = sum(notes) / len(notes) if notes else None
        par_matiere[m] = {"matiere": m, "nom": nom, "pourcent": _r(p), "note20": _r(p * 20 if p is not None else None, 1),
                          "cours_notes": len(notes), "cours_total": len(cs),
                          "exercices_faits": sum(v["exercices_faits"] for v in cs), "exercices_total": sum(v["exercices_total"] for v in cs)}
    notes = [v["pourcent"] for v in par_cours.values() if v["pourcent"] is not None]
    pertes = Counter(p for x in exos.values() for p in x["exercice"]["pertes"])
    return {
        "exercices": exos,
        "cours": par_cours,
        "matieres": par_matiere,
        "global": {"pourcent": _r(sum(notes) / len(notes) if notes else None),
                   "note20": _r(sum(notes) / len(notes) * 20 if notes else None, 1),
                   "exercices_faits": sum(1 for x in exos.values() if x["exercice"]["faites"]),
                   "exercices_reussis": sum(1 for x in exos.values() if x["statut"] == "reussi"),
                   "exercices_total": len(cat)},
        "forces": [{"cours": v["cours"], "titre": v["titre"], "pourcent": v["pourcent"]}
                   for v in sorted(par_cours.values(), key=lambda v: -(v["pourcent"] or 0)) if (v["pourcent"] or 0) >= SEUIL_FORT][:5],
        "lacunes": [{"cours": v["cours"], "titre": v["titre"], "pourcent": v["pourcent"], "competences": v["lacunes_cours"]}
                    for v in sorted(par_cours.values(), key=lambda v: v["pourcent"] or 0) if v["pourcent"] is not None and v["pourcent"] < SEUIL_FAIBLE][:5],
        "pertes_frequentes": [{"perte": p, "fois": n} for p, n in pertes.most_common(6)],
    }
