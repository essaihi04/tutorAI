"""Le suivi des acquis, par compétence (skill `suivi-des-acquis`, 8 novembre 2026).

Chaque cours est découpé en COMPÉTENCES (`deck.competences`, et `competence_ids` sur chaque diapositive). Chaque
réponse de l'élève à une question du cours est notée avec la compétence visée et la MANIÈRE dont la notion lui a
été expliquée juste avant (simulation, image, tableau, formules écrites, le tuteur a montré, l'élève a manipulé,
la variante du tuteur, exercice ou question du cours). On en tire, par compétence :
  - un statut : acquis (juste du premier coup), partiel (juste au deuxième essai), non acquis (faux deux fois),
    non évalué ;
  - le trajet : ce qui a été essayé, dans l'ordre, et avec quelle méthode ;
  - les méthodes qui marchent avec CET élève (taux de réussite par méthode) et, pour chaque lacune, la méthode
    avec laquelle la reprendre (la mieux réussie chez lui, différente de celle qui a échoué).
Une question de PRÉDICTION (`type: "prediction"`, posée avant l'explication, 11 novembre 2026) est gardée dans le
trajet mais n'entre ni dans le score ni dans les méthodes : se tromper en prévoyant n'est pas une erreur de compétence.
Le bilan nourrit le mode libre (`bloc_prompt`) et la préparation du cours suivant (`lacunes`).

Stockage : un fichier JSONL par élève dans `data/suivi_acquis/` (aucune table avant la validation de
l'utilisateur ; la même fonction `enregistrer` pourra écrire dans Supabase ensuite).
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

DOSSIER = Path(__file__).resolve().parents[2] / "data" / "suivi_acquis"

SEUIL_ACQUIS, SEUIL_PARTIEL = 0.8, 0.4

#: Comment on nomme chaque méthode à l'élève et au tuteur.
NOMS_METHODES = {
    "simulation": "une simulation manipulée au tableau",
    "image": "une image commentée",
    "table": "un tableau comparatif",
    "schema": "un schéma",
    "scientific": "une figure scientifique",
    "aucun": "l'explication orale seule",
    "formules": "les formules écrites au moment où elles sont dites",
    "tuteur_montre": "le tuteur qui montre du doigt au rythme de la voix",
    "eleve_manipule": "l'élève qui manipule lui-même la simulation",
    "variante": "la comparaison faite par le tuteur (variante)",
    "exercice": "un exercice d'application",
    "question_cours": "une question de cours",
    "vrai_faux": "un vrai/faux",
    "qcm": "un QCM",
    "directe": "une réponse rédigée",
}


def _nettoyer(s: Any) -> str:
    return re.sub(r"[^a-z0-9_]", "", str(s or "").lower())


def methodes_de(evenement: dict) -> list[str]:
    """Les méthodes employées sur la diapositive avant la question, en étiquettes."""
    m = evenement.get("methodes") or {}
    out = [_nettoyer(m.get("visuel") or "aucun") or "aucun"]
    if (m.get("formules_au_centre") or 0) > 0:
        out.append("formules")
    if (m.get("tuteur_a_montre") or 0) > 0:
        out.append("tuteur_montre")
    if m.get("eleve_a_manipule"):
        out.append("eleve_manipule")
    if m.get("variante_du_tuteur"):
        out.append("variante")
    out.append("exercice" if m.get("exercice") else "question_cours")
    t = _nettoyer(evenement.get("type"))
    if t in ("qcm", "vrai_faux", "directe"):
        out.append(t)
    return out


def score_question(tentatives: list[dict]) -> Optional[float]:
    """1 : juste du premier coup ; 0,5 : juste au 2e essai ; 0 : jamais juste ; None : rien de jugeable."""
    juges = [t for t in tentatives if t.get("correct") is not None]
    if not juges:
        return None
    for t in sorted(juges, key=lambda x: x.get("tentative", 1)):
        if t["correct"]:
            return 1.0 if t.get("tentative", 1) <= 1 else 0.5
    return 0.0


def statut(score: Optional[float]) -> str:
    if score is None:
        return "non_evalue"
    return "acquis" if score >= SEUIL_ACQUIS else "partiel" if score >= SEUIL_PARTIEL else "non_acquis"


def competences_du_cours(deck: dict) -> tuple[list[dict], dict[str, list[str]]]:
    """(compétences déclarées, diapositive → compétences). Sans déclaration : une compétence par activité."""
    comps = list(deck.get("competences") or [])
    par_diapo: dict[str, list[str]] = {}
    if comps:
        ids = {c["id"] for c in comps}
        for a in deck.get("activities", []):
            for s in a.get("slides", []):
                par_diapo[s["id"]] = [c for c in (s.get("competence_ids") or []) if c in ids]
        return comps, par_diapo
    for a in deck.get("activities", []):
        comps.append({"id": a["id"], "label": a.get("title", a["id"])})
        for s in a.get("slides", []):
            par_diapo[s["id"]] = [a["id"]]
    return comps, par_diapo


def charger_deck(deck_id: str) -> Optional[dict]:
    """Le cours (manifeste local `data/courses/*.json`) dont l'id ou le stable_id est `deck_id`."""
    if not deck_id:
        return None
    for p in sorted((Path(__file__).resolve().parents[2] / "data" / "courses").glob("*.json")):
        try:
            m = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(m, dict) and deck_id in (m.get("id"), m.get("stable_id")):
            return m
    return None


# ── Enregistrement ──────────────────────────────────────────────────────────

def _fichier(student_id: str) -> Path:
    DOSSIER.mkdir(parents=True, exist_ok=True)
    return DOSSIER / f"{_nettoyer(student_id) or 'inconnu'}.jsonl"


def enregistrer(student_id: str, evenement: dict) -> dict:
    e = {**evenement, "student_id": student_id, "quand": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    with _fichier(student_id).open("a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return e


def lire(student_id: str, deck_id: Optional[str] = None) -> list[dict]:
    p = _fichier(student_id)
    if not p.exists():
        return []
    out = []
    for ligne in p.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if deck_id is None or e.get("deck_id") == deck_id:
            out.append(e)
    return out


# ── Bilan ───────────────────────────────────────────────────────────────────

def bilan(evenements: Iterable[dict], deck: dict) -> dict:
    """Le bilan d'un élève sur un cours : statut, trajet et méthodes par compétence ; méthodes qui marchent."""
    comps, par_diapo = competences_du_cours(deck)
    labels = {c["id"]: c.get("label", c["id"]) for c in comps}
    # question → tentatives
    questions: dict[tuple[str, str], list[dict]] = defaultdict(list)
    predictions: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for e in evenements:
        cible = predictions if e.get("type") == "prediction" else questions
        cible[(e.get("slide_id", ""), e.get("cle", "q"))].append(e)
    # `dit` : le nom de la compétence tel que la voix le dit (sans symbole), pour que le tuteur nomme les lacunes à voix haute
    par_comp: dict[str, dict] = {c["id"]: {"id": c["id"], "label": labels[c["id"]], "dit": c.get("dit") or "", "questions": [], "predictions": [], "trajet": []} for c in comps}
    reussites: dict[str, list[float]] = defaultdict(list)
    for (slide_id, cle), tent in questions.items():
        sc = score_question(tent)
        premier = min(tent, key=lambda t: t.get("tentative", 1))
        meths = methodes_de(premier)
        cibles = (premier.get("competence_ids") or par_diapo.get(slide_id) or [])
        q = {"slide_id": slide_id, "slide_title": premier.get("slide_title", ""), "cle": cle, "enonce": premier.get("enonce", ""),
             "score": sc, "statut": statut(sc), "methodes": meths,
             "essais": [{"tentative": t.get("tentative", 1), "reponse": t.get("reponse", ""), "correct": t.get("correct")} for t in sorted(tent, key=lambda t: t.get("tentative", 1))]}
        if sc is not None:
            for mth in meths:
                reussites[mth].append(sc)
        for cid in cibles:
            if cid in par_comp:
                par_comp[cid]["questions"].append(q)
                par_comp[cid]["trajet"].append(f"{q['slide_title'] or slide_id} : {q['statut']} ({', '.join(NOMS_METHODES.get(m, m) for m in meths[:3])})")
    # Les prédictions : notées pour le trajet (ce que l'élève pensait avant l'explication), jamais dans le score.
    for (slide_id, cle), tent in predictions.items():
        premier = min(tent, key=lambda t: t.get("tentative", 1))
        juste = premier.get("correct")
        p = {"slide_id": slide_id, "slide_title": premier.get("slide_title", ""), "cle": cle, "enonce": premier.get("enonce", ""),
             "reponse": premier.get("reponse", ""), "juste_du_premier_coup": juste}
        for cid in (premier.get("competence_ids") or par_diapo.get(slide_id) or []):
            if cid in par_comp:
                par_comp[cid]["predictions"].append(p)
                verdict = "juste" if juste else "fausse" if juste is False else "non jugée"
                par_comp[cid]["trajet"].append(f"{p['slide_title'] or slide_id} : prédiction {verdict} (avant l'explication, non notée)")
    taux = {m: round(sum(v) / len(v), 2) for m, v in reussites.items() if v}
    marchent = [m for m, _ in sorted(taux.items(), key=lambda kv: -kv[1]) if taux[m] >= SEUIL_ACQUIS]
    for c in par_comp.values():
        scores = [q["score"] for q in c["questions"] if q["score"] is not None]
        c["score"] = round(sum(scores) / len(scores), 2) if scores else None
        c["statut"] = statut(c["score"])
        if c["statut"] in ("non_acquis", "partiel"):
            ratees = {m for q in c["questions"] if q["score"] is not None and q["score"] < SEUIL_ACQUIS for m in q["methodes"]}
            c["methodes_qui_ont_echoue"] = sorted(ratees)
            # la méthode avec laquelle reprendre : la mieux réussie chez lui, autre que celles qui ont échoué ;
            # à défaut, la simulation manipulée par l'élève puis l'exercice, qui marchent le plus souvent.
            candidates = [m for m in marchent if m not in ratees] or [m for m in ("eleve_manipule", "simulation", "exercice", "vrai_faux") if m not in ratees] or ["simulation"]
            c["a_reprendre_avec"] = candidates[:2]
    return {"competences": list(par_comp.values()), "taux_par_methode": taux, "methodes_qui_marchent": marchent,
            "resume": {s: [c["label"] for c in par_comp.values() if c["statut"] == s] for s in ("acquis", "partiel", "non_acquis", "non_evalue")}}


def lacunes(b: dict) -> list[dict]:
    """Les compétences à retravailler, avec la méthode conseillée : pour le mode libre et le cours suivant."""
    return [{"id": c["id"], "label": c["label"], "dit": c.get("dit") or "", "statut": c["statut"], "score": c["score"],
             "echoue_avec": [NOMS_METHODES.get(m, m) for m in c.get("methodes_qui_ont_echoue", [])],
             "reprendre_avec": [NOMS_METHODES.get(m, m) for m in c.get("a_reprendre_avec", [])],
             "trajet": c["trajet"]}
            for c in b["competences"] if c["statut"] in ("non_acquis", "partiel")]


def bloc_prompt(b: dict, titre_cours: str = "") -> str:
    """Ce que le tuteur du mode libre sait de l'élève : ses lacunes, et comment lui expliquer."""
    lac = lacunes(b)
    if not lac and not b["resume"]["acquis"]:
        return ""
    lignes = [f"[ACQUIS DE L'ÉLÈVE{' — ' + titre_cours if titre_cours else ''}]"]
    if b["resume"]["acquis"]:
        lignes.append("Acquis (ne pas réexpliquer, s'appuyer dessus) : " + " ; ".join(b["resume"]["acquis"]) + ".")
    for c in lac:
        lignes.append(f"- {'NON ACQUIS' if c['statut'] == 'non_acquis' else 'PARTIEL'} : {c['label']}. "
                      f"Expliqué avec {', '.join(c['echoue_avec']) or 'le cours'} sans succès → reprends-le avec "
                      f"{' puis '.join(c['reprendre_avec'])}. Pose UNE question dessus dès que l'occasion vient, et "
                      f"ne considère la notion reconquise qu'après une réussite sur une nouvelle question.")
    if b["methodes_qui_marchent"]:
        lignes.append("Ce qui marche avec cet élève : " + ", ".join(NOMS_METHODES.get(m, m) for m in b["methodes_qui_marchent"][:4]) + ".")
    return "\n".join(lignes)
