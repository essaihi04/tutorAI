"""Briques communes des générateurs d'exercices (partie « Exercices », skill `.agents/skills/exercices/SKILL.md`).

Les générateurs `scripts/exercices/generateurs/<id>.py` (modèle : `math_ex_ch1_continuite_1.py`) importent ces
fonctions pour écrire les diapositives au format des cours et pour se contrôler avant d'écrire le JSON :
  - `valeur` / `phrase` : la réponse attendue ; `valeur` vérifie que `attendu` se lit bien (comme `juger.ts`) ;
  - `qcm`, `vrai_faux`, `association` : la version « plus facile » (réaction préparée pour chaque option / paire) ;
  - `sim` : une diapositive d'explication animée avec une simulation EXISTANTE du cours ;
  - `ecrire(EX)` : contrôles (ids, mots du pointage, chiffres et symboles dans la voix, jugement des valeurs), puis écrit.
Usage d'un générateur : python -X utf8 scripts/exercices/generateurs/<id>.py frontend/public/media/exercices/<id>.json
"""
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[3]
SIMS = RACINE / "frontend" / "public"
ORIGINE = "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série)."


# ---------------------------------------------------------------- réponses
def lire_nombre(texte):
    """Port de `lireNombre` (frontend/src/components/exercice/juger.ts) : le nombre après le dernier « = » ou « ≈ »."""
    exp = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-"))
    s = re.sub("[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+", lambda m: "^" + "".join(exp[c] for c in m.group()), texte)
    coupe = max(s.rfind("="), s.rfind("≈"))
    if coupe >= 0:
        s = s[coupe + 1:]
    s = re.sub(r"\s+", "", s).replace(",", ".").replace("−", "-")
    s = re.sub(r"[×x·*]10\^?\(?(-?\d+)\)?", r"e\1", s)
    m = re.search(r"-?\d+(?:\.\d+)?(?:e-?\d+)?", s)
    return float(m.group()) if m else None


def valeur(grandeur, v, attendu, tolerance=0.001, unite=None):
    r = {"type": "valeur", "grandeur": grandeur, "valeur": v, "tolerance": tolerance, "attendu": attendu}
    if unite:
        r["unite"] = unite
    return r


def phrase(attendu):
    return {"type": "phrase", "attendu": attendu}


def rep(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}


def aide(texte, dit):
    return {"texte": texte, "dit": dit}


def correction(lignes, parole):
    """lignes : [(texte écrit, mot de la parole)]"""
    return {"lignes": [{"texte": t, "mot": m} for t, m in lignes], "parole": parole}


# ---------------------------------------------------------------- diapositives « plus facile »
def qcm(sid, titre, intro, prompt, options, bonne, reactions, enonce_dit, lead=None):
    """reactions[i] : (parole, ecrit) pour la bonne option ; ((parole1, ecrit1), (parole2, ecrit2)) pour une fausse
    (1 = ce qui ne va pas + un indice, sans la réponse ; 2 = la réponse et sa justification)."""
    q = {}
    for i, r in enumerate(reactions):
        if i == bonne:
            q[str(i)] = {"juste": rep(*r)}
        else:
            q[str(i)] = {"1": rep(*r[0]), "2": rep(*r[1])}
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead or prompt},
            "visual": {"kind": "none"}, "speech_text": {"mixed": intro},
            "question": {"type": "qcm", "prompt": prompt, "options": options, "correct": bonne, "enonce_dit": enonce_dit},
            "concentration": {"demarrer": "reset", "reponses": {"q": q}}}


def vrai_faux(sid, titre, lead, intro, affirmations, prompt="Vrai ou faux ?"):
    """affirmations : [(texte, vrai?, explication)]"""
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "none"}, "speech_text": {"mixed": intro},
            "exercises": [{"type": "vrai_faux", "prompt": prompt,
                           "statements": [{"text": t, "correct": c, "explanation": e} for t, c, e in affirmations]}],
            "concentration": {"demarrer": "reset"}}


def association(sid, titre, lead, intro, prompt, gauche, droite, couples, retours, bilan):
    """gauche/droite : [(id, texte)] ; couples {g: d} ; retours {"g-d": (texte, dit)} (juste déduit des couples) ;
    bilan (texte, dit). Professeur règle 47 : un retour pour CHAQUE paire possible."""
    rt = {}
    for k, (t, d) in retours.items():
        g, dr = k.split("-")
        rt[k] = {"juste": couples.get(g) == dr, "texte": t, "dit": d}
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "none"}, "speech_text": {"mixed": intro},
            "question": {"type": "association", "prompt": prompt, "association": {
                "gauche": [{"id": i, "texte": t} for i, t in gauche], "droite": [{"id": i, "texte": t} for i, t in droite],
                "couples": couples, "retours": rt, "bilan": {"texte": bilan[0], "dit": bilan[1]}, "melanger": True, "essais": 2}},
            "concentration": {"demarrer": "reset"}}


# ---------------------------------------------------------------- explication animée
def sim(sid, titre, lead, url, caption, mixed, centre, pointage, demarrer="reset"):
    """centre : [(texte, mot)] ; pointage : dicts du format des cours ({mot, commande, parametres} | {mot, cible} | {mot, repere})."""
    return {"id": sid, "slide_type": "simulation", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "simulation", "url": url, "caption": caption},
            "speech_text": {"mixed": mixed},
            "concentration": {"demarrer": demarrer, "centre": [{"texte": t, "mot": m} for t, m in centre], "pointage": pointage}}


def jusqua(mot, moment):
    return {"mot": mot, "commande": "play_until", "parametres": {"moment": moment}}


def regle(mot, **p):
    return {"mot": mot, "commande": "set_parameters", "parametres": p}


def montre(mot, cible):
    return {"mot": mot, "cible": cible}


def deck(id_, titre, slides):
    return {"activities": [{"id": id_, "title": titre, "slides": slides}]}


# ---------------------------------------------------------------- contrôles
AR = re.compile(r"[؀-ۿ]")
CHAMPS_VOIX = {"mixed", "dit", "parole", "intro_dit", "texte_dit", "enonce_dit"}
SYMBOLES = re.compile(r"[0-9=+−×÷*/²³√∞≤≥<>()\[\]{}ℝℕ∈⇔⇒→ₙ₀₁₂₃⁰¹⁴⁵⁶⁷⁸⁹ⁿ|πθτ%ℓ]")


def _voix(o, k=""):
    if isinstance(o, dict):
        for kk, v in o.items():
            yield from _voix(v, kk)
    elif isinstance(o, list):
        for v in o:
            yield from _voix(v, k)
    elif isinstance(o, str) and k in CHAMPS_VOIX:
        yield k, o


def controler(EX):
    pb = []
    slides = {}
    for d in ("explication", "facile"):
        for a in EX[d]["activities"]:
            for s in a["slides"]:
                slides[s["id"]] = (d, s)
    qs = EX["enonce"]["questions"]
    sq = EX["similaire"]["enonce"]["questions"]
    if len(qs) != len(sq):
        pb.append(("similaire : nombre de questions", len(qs), len(sq)))
    for q in qs + sq:
        for champ in ("reponse", "clavier", "correction"):
            if champ not in q:
                pb.append(("champ manquant", q["id"], champ))
        r = q.get("reponse", {})
        if r.get("type") == "valeur":
            lu = lire_nombre(r["attendu"])
            if lu is None or abs(lu - r["valeur"]) > r.get("tolerance", 0.02) * max(abs(r["valeur"]), 1e-12):
                pb.append(("attendu mal jugé", q["id"], r["attendu"], lu, r["valeur"]))
        for l in q.get("correction", {}).get("lignes", []):
            if l["mot"] not in q["correction"]["parole"]:
                pb.append(("mot correction absent", q["id"], l["mot"]))
    for q in qs:
        for champ, deck_ in (("explication", "explication"), ("facile", "facile")):
            if q.get(champ) not in slides or slides[q[champ]][0] != deck_:
                pb.append(("diapositive absente", q["id"], champ, q.get(champ)))
        if not (2 <= len(q.get("aides", [])) <= 3):
            pb.append(("aides : 2 ou 3", q["id"]))
    for sid, (d, s) in slides.items():
        c = s.get("concentration", {})
        texte = s["speech_text"]["mixed"]
        pos = -1
        for p in c.get("pointage", []):
            i = texte.find(p["mot"])
            if i < 0:
                pb.append(("mot absent", sid, p["mot"]))
            elif i < pos:
                pb.append(("pointage pas dans l'ordre de la voix", sid, p["mot"]))
            else:
                pos = i
            if p.get("cible", "").startswith("centre:") and int(p["cible"][7:]) >= len(c.get("centre", [])):
                pb.append(("centre:N hors liste", sid, p["cible"]))
        for p in c.get("centre", []):
            if p["mot"] not in texte:
                pb.append(("mot centre absent", sid, p["mot"]))
        if s.get("visual", {}).get("kind") == "simulation":
            f = SIMS / s["visual"]["url"].split("?")[0].lstrip("/")
            if not f.exists():
                pb.append(("simulation absente", sid, s["visual"]["url"]))
        qq = s.get("question")
        if qq and qq.get("type") == "qcm":
            rs = c.get("reponses", {}).get("q", {})
            for i in range(len(qq["options"])):
                attendu = {"juste"} if i == qq["correct"] else {"1", "2"}
                if set(rs.get(str(i), {})) != attendu:
                    pb.append(("réaction manquante", sid, i))
        if qq and qq.get("type") == "association":
            a = qq["association"]
            for g, _ in [(x["id"], 0) for x in a["gauche"]]:
                for dr in [x["id"] for x in a["droite"]]:
                    if f"{g}-{dr}" not in a["retours"] and f"{g}-*" not in a["retours"]:
                        pb.append(("retour de paire manquant", sid, f"{g}-{dr}"))
    for k, t in _voix(EX):
        if SYMBOLES.search(t):
            pb.append(("chiffre ou symbole dans la voix", k, SYMBOLES.search(t).group(), t[:80]))
        m = re.search(r"[A-Za-zÀ-ÿ][\u0621-\u064A]", t)
        if m:
            pb.append(("mot coupé latin+arabe", k, t[max(0, m.start() - 10):m.end() + 10]))
    return pb


def ecrire(EX, chemin=None):
    chemin = chemin or sys.argv[1]
    pb = controler(EX)
    for x in pb:
        print("  !", x)
    json.dump(EX, open(chemin, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("ok" if not pb else f"{len(pb)} problème(s)", chemin)
