"""Audit pédagogique des cours en mode concentration (demande de l'utilisateur du 26/11/2026).

Mesure, pour chaque cours, ce qui peut perturber l'élève :
  A. questions trop tôt : première diapo qui pose une question (écrite, d'observation, exercice ou voix
     qui finit sur « ? »), et première question de bloc ;
  B. synchronisation dit = écrit : phrases qui disent une formule sans qu'elle s'écrive (aucun `mot` de
     `pointage` / `centre` dans la phrase) et plus long passage parlé sans aucun geste ;
  C. notions importantes redites : diapos clés (définition, formule écrite, « Je relis ») avec une
     deuxième façon de le dire (« autrement dit », « بطريقة أخرى », relecture…) ;
  D. annonce d'attention avant une notion importante (« ركز معايا », « suis bien »…) et variété des phrases ;
  E. tuteur robotique : débuts de voix répétés, mêmes tournures recopiées de diapo en diapo, réactions
     identiques mot pour mot.

L'ordre des notions (une notion dite avant celle dont elle dépend) ne se mesure pas avec des motifs :
il se lit diapo par diapo (voir docs/audit-pedagogie/ordre-des-notions/).

Usage : python -I scripts/audit/audit_pedagogie.py [cours.json ...] [--md docs/audit-pedagogie/mesures.md]
Sans fichier : tous les cours `backend/data/courses/*.json` en mode concentration.
"""
from __future__ import annotations

import collections
import glob
import json
import os
import re
import sys

PREMIERES = 6  # « premières diapos » : aucune question avant la 7ᵉ diapo (ouverture comprise)

FORMULE = re.compile(
    r"\b(égale|egale|fois|divisé|puissance|sur delta|racine|au carré|moins un sur|plus un sur)\b", re.I)
REDIRE = re.compile(
    r"(autrement dit|dit autrement|en d'autres termes|je relis|je répète|بطريقة أخرى|بطريقة خرى|بمعنى آخر|"
    r"بمعنى اخر|بعبارة أخرى|نعاود نقرا|نعاودها|نعاود نقولها|عاود معايا|يعني بالدارجة|بكلمة أخرى|نقولها بطريقة)",
    re.I)
# Annonce AVANT une notion (règle 55). « رد البال : … » signale un piège après coup : ce n'est pas une annonce.
ATTENTION = re.compile(
    r"(ركز معايا|ركّز معايا|ركز مزيان|حل عينيك|حلّ عينيك|تبع معايا|تبعني|سمعني مزيان|وقف معايا|"
    r"هادي مهمة|هاد الجزء مهم|مهم بزاف|هنا المهم|القلب ديال الدرس|اللحظة المهمة|بغيتك تحفظ|"
    r"suis bien|sois attentif|concentre-toi|écoute bien|c'est important|partie importante|le plus important)", re.I)


def mots(t: str) -> list[str]:
    return re.findall(r"\S+", t or "")


def phrases(t: str) -> list[str]:
    return [p.strip() for p in re.split(r"(?<=[.!?؟:])\s+", t or "") if p.strip()]


def charger(p: str):
    d = json.load(open(p, encoding="utf-8"))
    if d.get("mode") != "concentration":
        return None
    slides = [s for a in d.get("activities", []) for s in a.get("slides", [])]
    return d, slides


def a_question(s: dict) -> str | None:
    c = s.get("concentration") or {}
    if s.get("question"):
        return "question"
    if s.get("exercises"):
        return "exercice"
    if c.get("observation"):
        return "observation"
    t = (s.get("speech_text") or {}).get("mixed") or ""
    if t.rstrip().endswith(("?", "؟")) and not s.get("ouverture_cours"):
        return "voix finit sur ?"
    return None


def ancres(s: dict, texte: str) -> list[int]:
    """Positions (en caractères) des gestes posés sur le texte parlé."""
    c = s.get("concentration") or {}
    pos = []
    for g in (c.get("pointage") or []) + (c.get("centre") or []):
        m = g.get("mot") if isinstance(g, dict) else None
        if m:
            i = texte.find(m)
            if i >= 0:
                pos.append(i)
    obs = c.get("observation") or {}
    if obs.get("apres_mot") and texte.find(obs["apres_mot"]) >= 0:
        pos.append(texte.find(obs["apres_mot"]))
    return sorted(pos)


def est_cle(s: dict) -> bool:
    c = s.get("concentration") or {}
    t = s.get("title", "")
    fr = (s.get("speech_text") or {}).get("fr") or ""
    cah = c.get("cahier") or ""
    if s.get("ouverture_cours") or s.get("fermeture_cours") or s.get("slide_type") == "synthesis":
        return False
    if re.search(r"^(rappel|national|cas type)", t, re.I):
        return False
    return bool(
        c.get("centre")
        or re.search(r"définition|je relis", fr, re.I)
        or re.match(r"(Définition|Formule|Méthode|Loi|Propriété)", cah)
        or s.get("slide_type") == "concept"
    )


def auditer(p: str) -> dict | None:
    r = charger(p)
    if not r:
        return None
    d, slides = r
    deck = os.path.basename(p)[:-5]
    out: dict = {"deck": deck, "diapos": len(slides)}

    # A. questions trop tôt
    premieres = []
    for i, s in enumerate(slides[:PREMIERES]):
        q = a_question(s)
        if q:
            premieres.append((i + 1, s["id"], q))
    pos = {s["id"]: i for i, s in enumerate(slides)}
    premier_bloc = None
    for se in d.get("seances", []):
        for b in se.get("blocs", []):
            if b.get("retrouver") or b.get("exercice"):
                fin = max((pos.get(x, -1) for x in b.get("slide_ids", [])), default=-1)
                premier_bloc = (fin + 1, b["id"])
                break
        if premier_bloc:
            break
    out["questions_debut"] = premieres
    out["premier_bloc_question_apres_diapo"] = premier_bloc

    # B. synchronisation
    formules_sans = []
    trous = []
    for i, s in enumerate(slides):
        t = (s.get("speech_text") or {}).get("mixed") or ""
        if not t:
            continue
        a = ancres(s, t)
        bornes = [0] + a + [len(t)]
        plus_long = max(len(mots(t[bornes[k]:bornes[k + 1]])) for k in range(len(bornes) - 1))
        enonce = "enonce" in s["id"] or re.search(r"énoncé", s.get("title", ""), re.I)
        if plus_long >= 60 and not enonce:
            trous.append((i + 1, s["id"], plus_long))
        debut = 0
        for ph in phrases(t):
            j = t.find(ph, debut)
            debut = j + len(ph)
            # écrite à cette phrase, ou au plus une dizaine de mots avant (le geste précède la parole)
            avant = len(" ".join(mots(t[:j])[-12:]))
            if FORMULE.search(ph) and not any(j - avant <= x < j + len(ph) for x in a):
                formules_sans.append((i + 1, s["id"], ph[:90]))
    out["formules_dites_non_ecrites"] = formules_sans
    out["passages_sans_geste_60mots"] = trous

    # C. et D. notions clés : redites, annoncées
    cles = [(i, s) for i, s in enumerate(slides) if est_cle(s)]
    redites, annoncees, phrases_att = 0, 0, []
    sans_redire = []
    for i, s in cles:
        t = (s.get("speech_text") or {}).get("mixed") or ""
        fr = (s.get("speech_text") or {}).get("fr") or ""
        if REDIRE.search(t) or REDIRE.search(fr):
            redites += 1
        else:
            sans_redire.append((i + 1, s["id"], s["title"][:60]))
        prec = (slides[i - 1].get("speech_text") or {}).get("mixed", "") if i else ""
        tete = " ".join(mots(t)[:25]) + " " + " ".join(mots(prec)[-20:])
        m = ATTENTION.search(tete)
        if m:
            annoncees += 1
            phrases_att.append(m.group(0))
    out["cles"] = len(cles)
    out["cles_redites"] = redites
    out["cles_sans_redire"] = sans_redire
    out["cles_annoncees"] = annoncees
    out["annonces_distinctes"] = len(set(phrases_att))

    # E. robotique
    debuts = collections.Counter()
    premiers = collections.Counter()
    suites = 0
    ngr = collections.defaultdict(set)
    avant = None
    for i, s in enumerate(slides):
        w = mots((s.get("speech_text") or {}).get("mixed") or "")
        if len(w) >= 2:
            debuts[" ".join(w[:2])] += 1
        if w:
            premiers[w[0].strip("،,:.")] += 1
            if w[0] == avant:
                suites += 1
            avant = w[0]
        for k in range(len(w) - 5):
            ngr[" ".join(w[k:k + 6])].add(i)
    out["debuts_frequents"] = [(k, v) for k, v in debuts.most_common(4) if v >= 4]
    mot1, n1 = premiers.most_common(1)[0] if premiers else ("", 0)
    out["premier_mot_le_plus_frequent"] = (mot1, round(100 * n1 / max(len(slides), 1)))
    out["diapos_suivantes_meme_premier_mot"] = suites
    out["tournures_recopiees"] = sorted(
        [(k, len(v)) for k, v in ngr.items() if len(v) >= 5], key=lambda x: -x[1])[:6]
    paroles = collections.Counter()
    for s in slides:
        for q in ((s.get("concentration") or {}).get("reponses") or {}).values():
            for opt in (q or {}).values():
                for r in (opt or {}).values() if isinstance(opt, dict) and "parole" not in opt else [opt]:
                    if isinstance(r, dict) and r.get("parole"):
                        paroles[" ".join(mots(r["parole"])[:6])] += 1
    out["reactions"] = sum(paroles.values())
    out["reactions_meme_debut"] = [(k, v) for k, v in paroles.most_common(3) if v >= 4]
    return out


def tableau(res: list[dict]) -> str:
    l = ["| Cours | Diapos | Questions dans les 6 premières | Formules dites non écrites | Passages ≥ 60 mots sans geste "
         "| Notions clés | redites | annoncées (phrases ≠) | Premier mot le plus fréquent | Diapos qui suivent avec le même premier mot "
         "| Débuts de voix répétés | Tournures recopiées ≥ 5 diapos |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        l.append(
            f"| {r['deck']} | {r['diapos']} | {len(r['questions_debut'])} | {len(r['formules_dites_non_ecrites'])} "
            f"| {len(r['passages_sans_geste_60mots'])} | {r['cles']} | {r['cles_redites']} "
            f"| {r['cles_annoncees']} ({r['annonces_distinctes']}) "
            f"| « {r['premier_mot_le_plus_frequent'][0]} » {r['premier_mot_le_plus_frequent'][1]} % "
            f"| {r['diapos_suivantes_meme_premier_mot']} "
            f"| {', '.join(f'« {k} » ×{v}' for k, v in r['debuts_frequents'][:2]) or '—'} "
            f"| {len(r['tournures_recopiees'])} |")
    return "\n".join(l)


def detail(r: dict) -> str:
    l = [f"### {r['deck']}", ""]
    if r["questions_debut"]:
        l.append("- Questions trop tôt : " + " ; ".join(f"diapo {n} `{i}` ({q})" for n, i, q in r["questions_debut"]))
    if r["premier_bloc_question_apres_diapo"]:
        n, b = r["premier_bloc_question_apres_diapo"]
        l.append(f"- Première question de bloc : après la diapo {n} (`{b}`)")
    for n, i, ph in r["formules_dites_non_ecrites"][:5]:
        l.append(f"- Dit sans être écrit, diapo {n} `{i}` : « {ph} »")
    for n, i, w in sorted(r["passages_sans_geste_60mots"], key=lambda x: -x[2])[:3]:
        l.append(f"- {w} mots sans aucun geste, diapo {n} `{i}`")
    for k, v in r["tournures_recopiees"][:3]:
        l.append(f"- Tournure recopiée dans {v} diapos : « {k} »")
    for k, v in r["reactions_meme_debut"]:
        l.append(f"- {v} réactions commencent par « {k} »")
    return "\n".join(l)


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    md = None
    if "--md" in argv:
        k = argv.index("--md")
        md = argv[k + 1]
        argv = argv[:k] + argv[k + 2:]
    fichiers = argv or sorted(glob.glob("backend/data/courses/*.json"))
    res = [r for r in (auditer(p) for p in fichiers) if r]
    texte = tableau(res) + "\n\n" + "\n\n".join(detail(r) for r in res)
    if md:
        os.makedirs(os.path.dirname(md), exist_ok=True)
        open(md, "w", encoding="utf-8").write(texte + "\n")
        json.dump(res, open(md[:-3] + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(tableau(res))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
