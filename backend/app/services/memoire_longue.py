"""Mémoire longue : cycle des blocs, rappels espacés (même matière), traçabilité et notifications (11 novembre 2026).

Règle de l'utilisateur : « on veut des résultats, pas seulement une belle plateforme ». Ce qui compte est ce que l'élève
sait encore une semaine et un mois plus tard (skills `cours-concentration` « Memory and rhythm » et `suivi-des-acquis`
sections 6 à 8). Ce module :
  - note chaque événement du cycle des blocs (cahier écrit, retrouver, exercice), des séances (début, fin, durée),
    de la saturation (cause, ce que le tuteur a fait), des rappels et des notifications — au même endroit que les
    réponses du cours (`suivi_acquis.enregistrer`, un JSONL par élève, aucune table) ;
  - tient, par élève et par compétence, l'échelle des rappels (J+1, J+3, J+7, J+21, puis avant l'examen) : réussi du
    premier coup → marche suivante, raté → retour à J+1, réussi au deuxième essai → même marche ;
  - choisit les 3 à 5 rappels qui ouvrent une séance, UNIQUEMENT dans la matière du cours ouvert, les plus en retard
    d'abord, avec une autre formulation que la dernière fois ;
  - décide de la notification du jour (matière, nombre, durée ; à l'heure habituelle ; une par jour au plus ; plus
    discrète après plusieurs ignorées ; aucune si rien n'est dû) ;
  - calcule la rétention à J+7 et J+30 (réussite du premier coup à un rappel, au moins un jour après la dernière fois)
    par cours, par compétence et par élève, pour le tableau de bord.

Les événements de ce module portent `evenement` (le genre) et `cours_id`, jamais `deck_id` : ainsi le bilan d'un cours
(`suivi_acquis.lire(eleve, deck_id)`) ne voit que les réponses du cours, comme avant.
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

from app.services import suivi_acquis

try:
    from zoneinfo import ZoneInfo
    FUSEAU = ZoneInfo("Africa/Casablanca")
except Exception:  # noqa: BLE001 — pas de base des fuseaux : le Maroc est à UTC+1 presque toute l'année
    FUSEAU = timezone(timedelta(hours=1))

DOSSIER_COURS = Path(__file__).resolve().parents[2] / "data" / "courses"

#: L'échelle des rappels : la marche n est due `ECHELLE_JOURS[n]` jours après la dernière fois ; la dernière marche
#: (`MARCHE_EXAMEN`) revient tous les `INTERVALLE_ENTRETIEN` jours et une dernière fois avant l'examen.
ECHELLE_JOURS = [1, 3, 7, 21]
MARCHE_EXAMEN = len(ECHELLE_JOURS)
INTERVALLE_ENTRETIEN = 30
#: Examen national du 2ᵉ Bac (date approximative, à confirmer chaque année) ; le dernier rappel tombe deux semaines avant.
DATE_EXAMEN = date(2027, 6, 1)
AVANCE_EXAMEN = 14

RAPPELS_MIN, RAPPELS_MAX = 3, 5
#: Un rappel non encore dû peut compléter la séance jusqu'à 3 questions s'il l'est dans les 2 jours ; il ne fait
#: alors pas monter la marche (ce serait raccourcir l'espacement), mais un échec le ramène à J+1.
AVANCE_JOURS = 2
HEURE_PAR_DEFAUT = 18

GENRES = {"cahier", "retrouver", "exercice_bloc", "rappel", "saturation", "seance_debut", "seance_fin",
          "notification", "preferences", "pause"}

MATIERES = {"physique-chimie": "physique-chimie", "svt": "SVT", "mathematiques": "maths"}


# ── Le temps : les « jours » de l'élève sont ceux du Maroc ────────────────────

def _instant(e: dict) -> Optional[datetime]:
    try:
        t = datetime.fromisoformat(str(e.get("quand") or ""))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def jour_local(t: datetime) -> date:
    return t.astimezone(FUSEAU).date()


def maintenant_utc() -> datetime:
    return datetime.now(timezone.utc)


# ── Les cours et leur matière ─────────────────────────────────────────────────

_cache: dict[str, Any] = {"cle": None, "cours": {}}


def tous_les_cours() -> dict[str, dict]:
    """Les manifestes locaux (`data/courses/*.json`) par id ET par stable_id, relus seulement s'ils ont changé."""
    fichiers = sorted(DOSSIER_COURS.glob("*.json")) if DOSSIER_COURS.exists() else []
    cle = (str(DOSSIER_COURS), tuple((p.name, p.stat().st_mtime_ns) for p in fichiers))
    if _cache["cle"] == cle:
        return _cache["cours"]
    cours: dict[str, dict] = {}
    for p in fichiers:
        try:
            m = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(m, dict) and m.get("id") and isinstance(m.get("activities"), list):
            for k in {m.get("id"), m.get("stable_id")} - {None, ""}:
                cours.setdefault(k, m)
    _cache.update(cle=cle, cours=cours)
    return cours


def cours_id(deck_id: str, cours: Optional[dict[str, dict]] = None) -> str:
    """L'id du manifeste (le même pour son id et son stable_id) : la clé du planning."""
    m = (cours if cours is not None else tous_les_cours()).get(deck_id or "")
    return str(m["id"]) if m else str(deck_id or "")


def matiere_de(deck_id: str, deck: Optional[dict] = None) -> str:
    """physique-chimie, svt ou mathematiques : d'après l'id du cours (`phys_`, `chem_`, `svt_`, `math_`), sinon son champ
    `subject`. Physique et chimie vont ensemble (une seule matière au bac PC)."""
    c = (deck_id or "").lower()
    for prefixe, m in (("phys", "physique-chimie"), ("chem", "physique-chimie"), ("chim", "physique-chimie"),
                       ("pc_", "physique-chimie"), ("svt", "svt"), ("math", "mathematiques")):
        if c.startswith(prefixe):
            return m
    d = deck or {}
    sujet = " ".join(str(x or "") for x in (d.get("subject"), d.get("matiere"), (d.get("catalog") or {}).get("subject"))).lower()
    if "math" in sujet:
        return "mathematiques"
    if "svt" in sujet or "vie" in sujet or "bio" in sujet:
        return "svt"
    if "phys" in sujet or "chim" in sujet:
        return "physique-chimie"
    return ""


def _competence(deck: dict, comp_id: str) -> Optional[dict]:
    return next((c for c in deck.get("competences") or [] if c.get("id") == comp_id), None)


# ── Le planning : une échelle par élève et par compétence ─────────────────────

def due_apres(marche: int, jour: date) -> date:
    """Le jour où une compétence posée sur `marche` le `jour` revient."""
    if marche < MARCHE_EXAMEN:
        return jour + timedelta(days=ECHELLE_JOURS[max(0, marche)])
    avant_examen = DATE_EXAMEN - timedelta(days=AVANCE_EXAMEN)
    prochain = jour + timedelta(days=INTERVALLE_ENTRETIEN)
    if jour < avant_examen < prochain:          # le dernier rappel avant l'examen ne doit pas sauter
        return max(jour + timedelta(days=1), avant_examen)
    return prochain


def resultat_rappel(e: dict) -> Optional[str]:
    """premier_coup, second_essai, rate, ou None (rien de jugeable)."""
    if e.get("correct") is True:
        return "premier_coup"
    if e.get("correct") is False:
        return "second_essai" if e.get("correct_2") is True else "rate"
    return None


def planning(evenements: Iterable[dict], cours: Optional[dict[str, dict]] = None) -> dict[str, dict]:
    """Par compétence travaillée (`<cours>::<compétence>`) : marche, dernière fois, prochain jour dû, historique.

    Une compétence entre dans le planning à sa première réponse jugée dans le cours (ou au « retrouver » de son bloc),
    due à J+1 ; seuls les rappels la font ensuite monter ou redescendre."""
    cours = tous_les_cours() if cours is None else cours
    plan: dict[str, dict] = {}

    def entrer(cid: str, comp: str, t: datetime) -> None:
        cle = f"{cid}::{comp}"
        if cle in plan or not comp:
            return
        deck = cours.get(cid) or {}
        c = _competence(deck, comp) or {}
        j = jour_local(t)
        plan[cle] = {"cle": cle, "cours_id": cid, "competence_id": comp, "label": c.get("label") or comp,
                     "cours_titre": deck.get("title", cid), "matiere": matiere_de(cid, deck),
                     "appris": j.isoformat(), "marche": 0, "derniere": j.isoformat(), "due": due_apres(0, j).isoformat(),
                     "rappels": [], "questions_posees": []}

    for e in sorted((e for e in evenements if _instant(e)), key=_instant):
        t = _instant(e)
        genre = e.get("evenement") or "reponse"
        if genre == "reponse":
            if e.get("correct") is None or not e.get("deck_id"):
                continue
            cid = cours_id(e["deck_id"], cours)
            for comp in e.get("competence_ids") or []:
                entrer(cid, comp, t)
        elif genre == "retrouver" and e.get("cours_id") and e.get("competence_id"):
            entrer(cours_id(e["cours_id"], cours), e["competence_id"], t)
        elif genre == "rappel" and e.get("cours_id") and e.get("competence_id"):
            cid = cours_id(e["cours_id"], cours)
            entrer(cid, e["competence_id"], t)
            p = plan[f"{cid}::{e['competence_id']}"]
            r = resultat_rappel(e)
            if e.get("rappel_id"):
                p["questions_posees"].append(e["rappel_id"])
            if r is None:
                continue
            avant = p["marche"]
            if r == "premier_coup" and not e.get("en_avance"):
                p["marche"] = min(avant + 1, MARCHE_EXAMEN)
            elif r == "rate":
                p["marche"] = 0
            j = jour_local(t)
            p["derniere"], p["due"] = j.isoformat(), due_apres(p["marche"], j).isoformat()
            p["rappels"].append({"quand": e.get("quand"), "resultat": r, "marche_avant": avant, "marche": p["marche"]})
    return plan


def _questions(deck: dict, comp_id: str) -> list[dict]:
    return [q for q in (_competence(deck, comp_id) or {}).get("rappels") or [] if isinstance(q, dict) and q.get("prompt")]


def choisir_question(rappels: list[dict], deja_posees: list[str]) -> Optional[dict]:
    """Une autre formulation que la dernière fois : d'abord une question jamais posée, sinon la moins récente."""
    if not rappels:
        return None
    rang = {qid: i for i, qid in enumerate(deja_posees)}       # le dernier indice = la plus récente
    jamais = [q for q in rappels if q.get("id") not in rang]
    if jamais:
        return jamais[0]
    return min(rappels, key=lambda q: rang.get(q.get("id"), -1))


def minutes_pour(n: int) -> int:
    return max(1, math.ceil(n * 0.7))


def rappels_du_jour(evenements: list[dict], matiere: str, maintenant: Optional[datetime] = None,
                    cours: Optional[dict[str, dict]] = None) -> dict:
    """Les 3 à 5 questions qui ouvrent la séance, dans `matiere` seulement, les plus en retard d'abord."""
    cours = tous_les_cours() if cours is None else cours
    aujourd_hui = jour_local(maintenant or maintenant_utc())
    plan = planning(evenements, cours)
    candidats = [p for p in plan.values() if p["matiere"] == matiere and matiere and _questions(cours.get(p["cours_id"]) or {}, p["competence_id"])]
    dus = sorted((p for p in candidats if date.fromisoformat(p["due"]) <= aujourd_hui), key=lambda p: (p["due"], p["marche"]))
    choix = [(p, False) for p in dus[:RAPPELS_MAX]]
    if choix and len(choix) < RAPPELS_MIN:
        bientot = sorted((p for p in candidats if aujourd_hui < date.fromisoformat(p["due"]) <= aujourd_hui + timedelta(days=AVANCE_JOURS)),
                         key=lambda p: p["due"])
        choix += [(p, True) for p in bientot[:RAPPELS_MIN - len(choix)]]
    questions = []
    for p, en_avance in choix:
        q = choisir_question(_questions(cours[p["cours_id"]], p["competence_id"]), p["questions_posees"])
        if not q:
            continue
        questions.append({"cours_id": p["cours_id"], "cours_titre": p["cours_titre"], "competence_id": p["competence_id"],
                          "competence": p["label"], "marche": p["marche"], "due": p["due"], "en_avance": en_avance,
                          "jours_de_retard": (aujourd_hui - date.fromisoformat(p["due"])).days,
                          "question": q})
    return {"matiere": matiere, "nom_matiere": MATIERES.get(matiere, matiere), "questions": questions,
            "minutes": minutes_pour(len(questions)) if questions else 0}


def enrichir_rappel(evenements: list[dict], e: dict, maintenant: Optional[datetime] = None,
                    cours: Optional[dict[str, dict]] = None) -> dict:
    """Avant d'enregistrer un rappel : la marche où il était, les jours depuis la dernière fois et depuis l'apprentissage,
    et ce qui suit (marche et jour dû après ce rappel)."""
    cours = tous_les_cours() if cours is None else cours
    cid = cours_id(e.get("cours_id") or "", cours)
    aujourd_hui = jour_local(maintenant or maintenant_utc())
    p = planning(evenements, cours).get(f"{cid}::{e.get('competence_id')}")
    e = {**e, "cours_id": cid, "matiere": matiere_de(cid, cours.get(cid))}
    if p:
        e.update(marche=p["marche"], jours_depuis=(aujourd_hui - date.fromisoformat(p["derniere"])).days,
                 age_jours=(aujourd_hui - date.fromisoformat(p["appris"])).days)
    else:
        e.update(marche=0, jours_depuis=0, age_jours=0)
    apres = planning([*evenements, {**e, "evenement": "rappel", "quand": (maintenant or maintenant_utc()).isoformat()}], cours)
    q = apres.get(f"{cid}::{e.get('competence_id')}") or {}
    e.update(marche_apres=q.get("marche", 0), prochaine=q.get("due"))
    return e


# ── La progression dans les blocs (l'élève reprend là où il s'est arrêté) ─────

def seances_du_cours(deck: dict) -> list[dict]:
    return [s for s in deck.get("seances") or [] if isinstance(s, dict) and s.get("blocs")]


def progression(evenements: Iterable[dict], deck: dict) -> dict:
    """Pour chaque bloc : cahier écrit, retrouver fait, exercice fait ; la séance et le bloc où reprendre."""
    cid = str(deck.get("id") or "")
    ids = {cid, str(deck.get("stable_id") or cid)}
    fait: dict[str, dict] = defaultdict(lambda: {"cahier": False, "retrouver": None, "exercice": None})
    seances_finies: set[str] = set()
    for e in evenements:
        if e.get("cours_id") not in ids:
            continue
        g, b = e.get("evenement"), e.get("bloc_id")
        if g == "cahier" and b:
            fait[b]["cahier"] = True
        elif g == "retrouver" and b:
            fait[b]["retrouver"] = resultat_rappel(e) or "fait"
        elif g == "exercice_bloc" and b:
            fait[b]["exercice"] = resultat_rappel(e) or "fait"
        elif g == "seance_fin" and e.get("seance_id") and e.get("complete"):
            seances_finies.add(e["seance_id"])
    seances = seances_du_cours(deck)
    reprise = None
    for i, s in enumerate(seances):
        for j, b in enumerate(s["blocs"]):
            f = fait.get(b.get("id"), {})
            if not (f.get("cahier") and f.get("retrouver") and f.get("exercice")):
                reprise = {"seance": i, "bloc": j, "seance_id": s.get("id"), "bloc_id": b.get("id"),
                           "etape": "cahier" if not f.get("cahier") else "retrouver" if not f.get("retrouver") else "exercice"}
                break
        if reprise:
            break
    return {"blocs": {k: v for k, v in fait.items()}, "seances_finies": sorted(seances_finies), "reprise": reprise,
            "nb_seances": len(seances), "termine": bool(seances) and reprise is None}


# ── Les notifications : seulement ce qui est dû pour CET élève ────────────────

def preferences(evenements: Iterable[dict]) -> dict:
    p = {"heure": None, "coupees": False}
    for e in evenements:
        if e.get("evenement") == "preferences":
            p = {"heure": e.get("heure"), "coupees": bool(e.get("coupees"))}
    return p


def heure_habituelle(evenements: Iterable[dict]) -> Optional[int]:
    """L'heure (au Maroc) où l'élève commence le plus souvent ses séances, sur ses 30 dernières ; à défaut l'heure de
    ses réponses. Rien tant qu'on n'a pas au moins deux jours différents."""
    debuts = [t for e in evenements if e.get("evenement") == "seance_debut" and (t := _instant(e))]
    if len({jour_local(t) for t in debuts}) < 2:
        debuts = [t for e in evenements if (e.get("evenement") or "reponse") == "reponse" and (t := _instant(e))]
        # une heure par jour : la première réponse de la journée
        par_jour: dict[date, datetime] = {}
        for t in sorted(debuts):
            par_jour.setdefault(jour_local(t), t)
        debuts = list(par_jour.values())
    if len({jour_local(t) for t in debuts}) < 2:
        return None
    heures = Counter(t.astimezone(FUSEAU).hour for t in sorted(debuts)[-30:])
    return max(heures.items(), key=lambda kv: (kv[1], -kv[0]))[0]


def notifications_ignorees(evenements: Iterable[dict]) -> int:
    """Le nombre de notifications envoyées de suite sans être ouvertes (les plus récentes)."""
    jours_envoyees: list[date] = []
    jours_ouvertes: set[date] = set()
    for e in evenements:
        if e.get("evenement") != "notification" or not (t := _instant(e)):
            continue
        (jours_envoyees.append(jour_local(t)) if e.get("action") == "envoyee" else
         jours_ouvertes.add(jour_local(t)) if e.get("action") == "ouverte" else None)
    n = 0
    for j in sorted(set(jours_envoyees), reverse=True):
        if j in jours_ouvertes:
            break
        n += 1
    return n


def dus_par_matiere(evenements: list[dict], maintenant: Optional[datetime] = None,
                    cours: Optional[dict[str, dict]] = None) -> dict[str, int]:
    cours = tous_les_cours() if cours is None else cours
    aujourd_hui = jour_local(maintenant or maintenant_utc())
    n: dict[str, int] = defaultdict(int)
    for p in planning(evenements, cours).values():
        if p["matiere"] and date.fromisoformat(p["due"]) <= aujourd_hui and _questions(cours.get(p["cours_id"]) or {}, p["competence_id"]):
            n[p["matiere"]] += 1
    return dict(n)


def texte_notification(matiere: str, n: int) -> str:
    nom = MATIERES.get(matiere, matiere)
    return f"{n} rappel{'s' if n > 1 else ''} de {nom} t'attend{'ent' if n > 1 else ''} ({minutes_pour(n)} min)"


def accueil(evenements: list[dict], maintenant: Optional[datetime] = None, cours: Optional[dict[str, dict]] = None) -> dict:
    """Ce que l'écran d'accueil montre : le badge (toujours, s'il y a du dû), la bannière (à l'heure de l'élève, une
    par jour au plus, plus discrète après plusieurs ignorées) et ses préférences."""
    t = maintenant or maintenant_utc()
    aujourd_hui, heure_locale = jour_local(t), t.astimezone(FUSEAU).hour
    prefs = preferences(evenements)
    habituelle = heure_habituelle(evenements)
    heure = prefs["heure"] if prefs["heure"] is not None else (habituelle if habituelle is not None else HEURE_PAR_DEFAUT)
    dus = {m: min(k, RAPPELS_MAX) for m, k in dus_par_matiere(evenements, t, cours).items()}
    total = sum(dus.values())
    ignorees = notifications_ignorees(evenements)
    envoyees = sorted(jour_local(x) for e in evenements
                      if e.get("evenement") == "notification" and e.get("action") == "envoyee" and (x := _instant(e)))
    deja_aujourdhui = bool(envoyees) and envoyees[-1] == aujourd_hui
    notification = None
    if total and not prefs["coupees"]:
        matiere = max(dus.items(), key=lambda kv: kv[1])[0]
        niveau = "banniere" if ignorees < 3 else "discret"
        espacee = ignorees >= 5 and envoyees and (aujourd_hui - envoyees[-1]).days < 3 and not deja_aujourdhui
        if (heure_locale >= heure or deja_aujourdhui) and not espacee:
            notification = {"matiere": matiere, "nom_matiere": MATIERES.get(matiere, matiere), "nombre": dus[matiere],
                            "minutes": minutes_pour(dus[matiere]), "texte": texte_notification(matiere, dus[matiere]),
                            "niveau": niveau, "nouvelle": not deja_aujourdhui}
    return {"badge": total, "dus": dus, "notification": notification, "heure": heure, "heure_habituelle": habituelle,
            "preferences": prefs, "ignorees": ignorees}


# ── La rétention : ce qui reste vraiment (tableau de bord) ────────────────────

def _taux(liste: list[bool]) -> dict:
    return {"n": len(liste), "reussis": sum(liste), "taux": round(sum(liste) / len(liste), 2) if liste else None}


def retention(evenements_par_eleve: dict[str, list[dict]], maintenant: Optional[datetime] = None,
              cours: Optional[dict[str, dict]] = None) -> dict:
    """Taux de rétention : réussite du premier coup aux rappels faits au moins un jour après la dernière fois.
    « J+7 » : rappels faits 7 à 29 jours après l'apprentissage ; « J+30 » : 30 jours et plus. Par cours, par compétence,
    par élève ; avec le nombre de rappels dus, les séances (durée), les saturations et les notifications."""
    cours = tous_les_cours() if cours is None else cours
    aujourd_hui = jour_local(maintenant or maintenant_utc())

    def seau() -> dict:
        return {"tous": [], "j7": [], "j30": []}

    par_cours: dict[str, dict] = defaultdict(seau)
    par_comp: dict[str, dict] = defaultdict(seau)
    eleves = []
    for eleve, evs in evenements_par_eleve.items():
        mien = seau()
        seances, saturations, cahiers = [], Counter(), 0
        notifs = Counter()
        for e in evs:
            g = e.get("evenement")
            if g == "rappel" and (r := resultat_rappel(e)) and (e.get("jours_depuis") or 0) >= 1:
                ok, age = r == "premier_coup", e.get("age_jours") or 0
                cid = cours_id(e.get("cours_id") or "", cours)
                for s in (mien, par_cours[cid], par_comp[f"{cid}::{e.get('competence_id')}"]):
                    s["tous"].append(ok)
                    if 7 <= age < 30:
                        s["j7"].append(ok)
                    elif age >= 30:
                        s["j30"].append(ok)
            elif g == "seance_fin" and e.get("duree_s"):
                seances.append(float(e["duree_s"]))
            elif g == "saturation":
                saturations[e.get("cause") or "?"] += 1
            elif g == "cahier":
                cahiers += 1
            elif g == "notification":
                notifs[e.get("action") or "?"] += 1
        plan = planning(evs, cours)
        dus = sum(1 for p in plan.values() if date.fromisoformat(p["due"]) <= aujourd_hui)
        dernier = max((e.get("quand") or "" for e in evs), default="")
        eleves.append({"eleve": eleve, "public": eleve.startswith("public"), "competences_suivies": len(plan), "dus": dus,
                       "rappels": _taux(mien["tous"]), "j7": _taux(mien["j7"]), "j30": _taux(mien["j30"]),
                       "seances": len(seances), "duree_moyenne_min": round(sum(seances) / len(seances) / 60, 1) if seances else None,
                       "cahiers": cahiers, "saturations": dict(saturations), "notifications": dict(notifs),
                       "dernier_evenement": dernier})
        for p in plan.values():                 # les compétences travaillées comptent même sans rappel encore
            par_comp[p["cle"]]
            par_cours[p["cours_id"]]

    def ligne_cours(cid: str, s: dict) -> dict:
        deck = cours.get(cid) or {}
        return {"cours_id": cid, "titre": deck.get("title", cid), "matiere": matiere_de(cid, deck),
                "rappels": _taux(s["tous"]), "j7": _taux(s["j7"]), "j30": _taux(s["j30"])}

    def ligne_comp(cle: str, s: dict) -> dict:
        cid, comp = cle.split("::", 1)
        c = _competence(cours.get(cid) or {}, comp) or {}
        return {"cle": cle, "cours_id": cid, "competence_id": comp, "label": c.get("label") or comp,
                "rappels": _taux(s["tous"]), "j7": _taux(s["j7"]), "j30": _taux(s["j30"])}

    return {"par_cours": sorted((ligne_cours(k, v) for k, v in par_cours.items()), key=lambda x: x["cours_id"]),
            "par_competence": sorted((ligne_comp(k, v) for k, v in par_comp.items()), key=lambda x: x["cle"]),
            "par_eleve": sorted(eleves, key=lambda x: x["dernier_evenement"], reverse=True),
            "definition": "Réussite du premier coup aux rappels faits au moins un jour après la dernière fois. "
                          "J+7 : rappels faits 7 à 29 jours après l'apprentissage ; J+30 : 30 jours et plus."}


def tous_les_eleves() -> dict[str, list[dict]]:
    """Les événements de chaque élève (fichiers JSONL du suivi des acquis)."""
    out: dict[str, list[dict]] = {}
    dossier = suivi_acquis.DOSSIER
    if not dossier.exists():
        return out
    for p in sorted(dossier.glob("*.jsonl")):
        evs = []
        for ligne in p.read_text(encoding="utf-8").splitlines():
            try:
                evs.append(json.loads(ligne))
            except ValueError:
                continue
        if evs:
            out[str(evs[0].get("student_id") or p.stem)] = evs
    return out
