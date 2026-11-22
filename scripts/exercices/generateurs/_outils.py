"""Outils communs aux générateurs d'exercices (mêmes formes que le pilote phys_ex_ch1_corde_1.py).

Usage dans un générateur :
    import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from _outils import *
    ...
    ecrire(EX)   # passe voix (thêta -> teta), contrôles de structure, puis json.dump vers sys.argv[1]
"""
import json, math, re, sys
from pathlib import Path
_RACINE = Path(__file__).resolve().parents[3]


def rep(parole, ecrit):
    """Une réaction préparée : la voix (parole) et le texte écrit (ecrit)."""
    return {"parole": parole, "ecrit": ecrit}


def qcm_facile(sid, titre, intro, prompt, options, bonne, reactions, enonce_dit):
    """Diapositive « version facile » QCM : une réaction préparée par option.
    reactions = {"<i bonne>": {"juste": rep(..)}, "<i fausse>": {"1": rep(1er essai), "2": rep(2e essai : la réponse)}}"""
    return {"id": sid, "slide_type": "exercise", "title": titre,
            "screen_content": {"lead": prompt},
            "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "qcm", "prompt": prompt, "options": options, "correct": bonne, "enonce_dit": enonce_dit},
            "concentration": {"demarrer": "reset", "reponses": {"q": reactions}}}


def vf_facile(sid, titre, intro, lead, affirmations, prompt="Vrai ou faux ?"):
    """Diapositive « version facile » vrai/faux. affirmations = [(texte, True|False, explication), ...]"""
    return {"id": sid, "slide_type": "exercise", "title": titre,
            "screen_content": {"lead": lead},
            "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "exercises": [{"type": "vrai_faux", "prompt": prompt, "statements": [
                {"text": t, "correct": c, "explanation": e} for (t, c, e) in affirmations]}],
            "concentration": {"demarrer": "reset"}}


def assoc_facile(sid, titre, intro, lead, prompt, gauche, droite, couples, retours, bilan):
    """Diapositive « version facile » association (professeur règle 47).
    gauche = [("1", "texte"), ...] ; droite = [("a", "texte"), ...] ; couples = {"1": "a", ...}
    retours = {"1-a": (True|False, texte, dit), ...} — UN retour pour CHAQUE paire gauche × droite ;
    bilan = (texte, dit)."""
    for g, _ in gauche:
        for d, _ in droite:
            assert f"{g}-{d}" in retours, f"{sid} : retour manquant {g}-{d}"
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": lead},
            "visual": {"kind": "none"}, "speech_text": {"mixed": intro},
            "question": {"type": "association", "prompt": prompt, "association": {
                "gauche": [{"id": i, "texte": t} for i, t in gauche],
                "droite": [{"id": i, "texte": t} for i, t in droite],
                "couples": couples,
                "retours": {k: {"juste": j, "texte": t, "dit": d} for k, (j, t, d) in retours.items()},
                "bilan": {"texte": bilan[0], "dit": bilan[1]},
                "melanger": True, "essais": 2}},
            "concentration": {"demarrer": "reset"}}


def diapo_sim(sid, titre, lead, url, caption, mixed, centre, pointage):
    """Diapositive d'explication animée avec une simulation EXISTANTE du cours.
    centre = [(texte, mot), ...] ; pointage = [dict(mot=..., commande=..., parametres=...) | dict(mot=..., repere=...) | dict(mot=..., cible="centre:0")]
    Chaque « mot » doit être un morceau exact de mixed."""
    return {"id": sid, "slide_type": "simulation", "title": titre,
            "screen_content": {"lead": lead},
            "visual": {"kind": "simulation", "url": url, "caption": caption},
            "speech_text": {"mixed": mixed},
            "concentration": {"demarrer": "reset",
                              "centre": [{"texte": t, "mot": m} for t, m in centre],
                              "pointage": pointage}}


def correction(lignes, parole):
    """lignes = [(texte écrit, mot dit), ...]"""
    return {"lignes": [{"texte": t, "mot": m} for t, m in lignes], "parole": parole}


def aide(texte, dit):
    return {"texte": texte, "dit": dit}


def valeur(grandeur, v, unite, attendu, tolerance=0.03):
    return {"type": "valeur", "grandeur": grandeur, "valeur": v, "unite": unite, "tolerance": tolerance, "attendu": attendu}


def phrase(attendu):
    return {"type": "phrase", "attendu": attendu}


# ---------- même lecture que frontend/src/components/exercice/juger.ts ----------
_EXP = {'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-'}


def lire_nombre(texte):
    s = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+", lambda m: "^" + "".join(_EXP[c] for c in m.group(0)), texte)
    coupe = max(s.rfind("="), s.rfind("≈"))
    if coupe >= 0:
        s = s[coupe + 1:]
    s = re.sub(r"\s+", "", s).replace(",", ".").replace("−", "-")
    s = re.sub(r"[×x·*]10\^?\(?(-?\d+)\)?", r"e\1", s)
    m = re.search(r"-?\d+(?:\.\d+)?(?:e-?\d+)?", s)
    return float(m.group(0)) if m else None


def _voix(o):
    if isinstance(o, dict):
        return {k: _voix(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_voix(v) for v in o]
    if isinstance(o, str):
        return o.replace("thêta", "teta").replace("thèta", "teta")
    return o


def verifier(EX):
    """Contrôles de structure (skill exercices § 7) ; lève AssertionError avec la liste des problèmes."""
    pb = []
    ids_ex = {s["id"] for a in EX["explication"]["activities"] for s in a["slides"]}
    ids_fa = {s["id"] for a in EX["facile"]["activities"] for s in a["slides"]}
    qs = EX["enonce"]["questions"]
    for q in qs:
        for k in ("id", "texte", "texte_dit", "reponse", "clavier", "aides", "correction", "explication", "facile"):
            if k not in q:
                pb.append(f"Q{q.get('id')} : champ {k} manquant")
        if len(q.get("aides", [])) < 2:
            pb.append(f"Q{q['id']} : moins de 2 aides")
        if q.get("explication") not in ids_ex:
            pb.append(f"Q{q['id']} : explication {q.get('explication')} absente")
        if q.get("facile") not in ids_fa:
            pb.append(f"Q{q['id']} : facile {q.get('facile')} absente")
    sq = EX["similaire"]["enonce"]["questions"]
    if len(sq) != len(qs):
        pb.append(f"similaire : {len(sq)} questions au lieu de {len(qs)}")
    for q in qs + sq:
        r = q["reponse"]
        if r["type"] == "valeur":
            lu = lire_nombre(r["attendu"])
            if lu is None or abs(lu - r["valeur"]) > r.get("tolerance", 0.02) * max(abs(r["valeur"]), 1e-12):
                pb.append(f"Q{q['id']} : attendu « {r['attendu']} » lu {lu} ≠ valeur {r['valeur']}")
            if r.get("unite") is None:
                pb.append(f"Q{q['id']} : unité manquante")
        for k in ("reponse", "clavier", "correction"):
            if k not in q:
                pb.append(f"Q{q['id']} : {k} manquant (similaire ?)")
    for a in EX["explication"]["activities"]:
        for s in a["slides"]:
            if "simulation" not in s.get("visual", {}).get("kind", ""):
                pb.append(f"{s['id']} : explication sans simulation")
            else:
                url = s["visual"]["url"].split("?")[0]
                if not (_RACINE / "frontend" / "public" / url.lstrip("/")).exists():
                    pb.append(f"{s['id']} : simulation introuvable {url}")
    if pb:
        raise AssertionError("\n".join(pb))


def ecrire(EX):
    EX = _voix(EX)
    verifier(EX)
    json.dump(EX, open(sys.argv[1], "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("ok", sys.argv[1])


# ---------- écriture des nombres (calculer en Python, puis écrire) ----------
_SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def fr(x, decimales=2):
    """1.5 -> « 1,5 » ; 0.30 avec decimales=2 -> « 0,3 » (zéros de fin retirés). Pour garder les zéros : f-string puis .replace('.', ',')."""
    s = f"{x:.{decimales}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",").replace("-", "−")


def sci(x, chiffres=3):
    """3.7e7 -> « 3,7 × 10⁷ » (chiffres significatifs, zéros de fin retirés)."""
    if x == 0:
        return "0"
    e = math.floor(math.log10(abs(x)))
    m = round(x / 10 ** e, chiffres - 1)
    if abs(m) >= 10:
        m /= 10; e += 1
    ms = fr(m, chiffres - 1)
    return ms if e == 0 else f"{ms} × 10{str(e).translate(_SUP)}"
