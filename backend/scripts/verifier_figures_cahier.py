"""Vérifie les dessins du cahier (`cahier_figures`) d'un ou plusieurs cours (format : docs/audit-cahier/FORMAT.md).

    python backend/scripts/verifier_figures_cahier.py backend/data/courses/phys_ch6_dipole_RC.json [...]
    python backend/scripts/verifier_figures_cahier.py --tous

Contrôle : types, champs obligatoires, couleurs, expressions calculables (mêmes fonctions que FigureCahier.tsx),
points dans le cadre, axes avec nom (et unité signalée si absente), légende présente, nombre de figures par bloc.
"""
from __future__ import annotations

import glob
import json
import math
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
COULEURS = {"blanc", "cyan", "jaune", "vert", "orange", "rose", "rouge", "bleu", "violet", "faible"}
TYPES = {"courbe", "schema", "croquis", "variations"}
POS = {"n", "s", "e", "o", "ne", "no", "se", "so", "centre"}
FONCTIONS = {
    "exp": "math.exp", "ln": "math.log", "log": "math.log10", "sqrt": "math.sqrt", "sin": "math.sin",
    "cos": "math.cos", "tan": "math.tan", "abs": "abs", "atan": "math.atan", "pi": "math.pi", "x": "x",
    "floor": "math.floor", "sign": "(lambda v: (v > 0) - (v < 0))",
}
CHAMPS = {
    "courbe": ({"expr"}, {"de", "a", "couleur", "trait", "texte", "texte_x", "pos"}),
    "ligne": ({"pts"}, {"ferme", "lisse", "couleur", "trait", "fleche", "remplir", "epais"}),
    "fleche": ({"de", "a"}, {"couleur", "trait", "texte", "pos"}),
    "cote": ({"de", "a", "t"}, {"couleur", "pos"}),
    "cercle": ({"c", "r"}, {"couleur", "remplir", "trait"}),
    "ellipse": ({"c", "rx", "ry"}, {"couleur", "remplir", "trait"}),
    "rect": ({"de", "a"}, {"couleur", "remplir", "trait", "arrondi"}),
    "arc": ({"c", "r", "de", "a"}, {"couleur", "trait", "fleche"}),
    "texte": ({"at", "t"}, {"couleur", "taille", "ancre"}),
    "point": ({"at"}, {"couleur", "t", "pos", "creux"}),
    "repere": (set(), {"x", "y", "t", "couleur"}),
}


def compiler(expr: str):
    e = expr.replace("−", "-").replace("·", "*").replace("×", "*")
    if not re.fullmatch(r"[\d\s.+\-*/^(),a-zA-Z]*", e):
        return None
    inconnu = []

    def mot(m):
        r = FONCTIONS.get(m.group(0).lower())
        if r is None:
            inconnu.append(m.group(0))
        return r or ""

    js = re.sub(r"[a-zA-Z]+", mot, e.replace("^", "**"))
    if inconnu:
        return None
    try:
        f = eval("lambda x: " + js, {"math": math, "abs": abs})  # noqa: S307 - expression déjà filtrée
        return f
    except SyntaxError:
        return None


def verifier_figure(fig: dict, ou: str, err: list, avert: list) -> None:
    if not isinstance(fig, dict):
        err.append(f"{ou}: figure non objet"); return
    t = fig.get("type")
    if t not in TYPES:
        err.append(f"{ou}: type {t!r} inconnu")
    if not fig.get("legende"):
        avert.append(f"{ou}: pas de légende")
    if not fig.get("titre"):
        avert.append(f"{ou}: pas de titre")
    if t == "variations":
        v = fig.get("variations") or {}
        xs, fs = v.get("x") or [], v.get("f") or []
        if len(xs) < 2 or len(fs) != len(xs):
            err.append(f"{ou}: variations : x et f doivent avoir la même longueur (≥ 2)")
        if v.get("signe") and len(v["signe"]) != len(xs) - 1:
            err.append(f"{ou}: variations : signe doit avoir len(x) − 1 éléments")
        for p in fs:
            if p.get("niveau") not in {"haut", "bas", "milieu"}:
                err.append(f"{ou}: variations : niveau {p.get('niveau')!r}")
        return
    axes, cadre = fig.get("axes"), fig.get("cadre")
    if axes:
        for k in ("x", "y"):
            a = axes.get(k) or {}
            if not isinstance(a.get("min"), (int, float)) or not isinstance(a.get("max"), (int, float)) or a["min"] >= a["max"]:
                err.append(f"{ou}: axe {k} : min < max requis")
            if not a.get("nom"):
                err.append(f"{ou}: axe {k} sans nom")
            if "unite" not in a:
                avert.append(f"{ou}: axe {k} ({a.get('nom')}) sans unité — mettre \"unite\" (ou \"\" si sans dimension)")
        xmin, xmax = axes["x"]["min"], axes["x"]["max"]
        ymin, ymax = axes["y"]["min"], axes["y"]["max"]
    elif cadre:
        xmin, xmax, ymin, ymax = 0, cadre.get("l", 0), 0, cadre.get("h", 0)
        if xmax <= 0 or ymax <= 0:
            err.append(f"{ou}: cadre l, h > 0 requis")
    else:
        err.append(f"{ou}: ni axes ni cadre"); return
    els = fig.get("elements") or []
    if not els:
        err.append(f"{ou}: aucun élément")
    if len(els) > 14:
        avert.append(f"{ou}: {len(els)} éléments — garder l'essentiel")
    dx, dy = (xmax - xmin) * 0.02, (ymax - ymin) * 0.02

    def dedans(p, nom):
        if not (isinstance(p, list) and len(p) == 2 and all(isinstance(v, (int, float)) for v in p)):
            err.append(f"{ou}: {nom} : point [x, y] attendu, reçu {p!r}"); return
        if not (xmin - dx <= p[0] <= xmax + dx and ymin - dy <= p[1] <= ymax + dy):
            avert.append(f"{ou}: {nom} {p} hors du cadre")

    for i, e in enumerate(els):
        f = e.get("f")
        q = f"{ou}.elements[{i}]({f})"
        if f not in CHAMPS:
            err.append(f"{q}: élément inconnu"); continue
        req, opt = CHAMPS[f]
        manque = req - e.keys()
        if manque:
            err.append(f"{q}: manque {sorted(manque)}")
        trop = set(e.keys()) - req - opt - {"f"}
        if trop:
            err.append(f"{q}: champs inconnus {sorted(trop)}")
        if e.get("couleur") and e["couleur"] not in COULEURS:
            err.append(f"{q}: couleur {e['couleur']!r}")
        if e.get("remplir") and e["remplir"] not in COULEURS:
            err.append(f"{q}: remplir {e['remplir']!r}")
        if e.get("pos") and e["pos"] not in POS:
            err.append(f"{q}: pos {e['pos']!r}")
        if f == "courbe" and "expr" in e:
            fn = compiler(e["expr"])
            if fn is None:
                err.append(f"{q}: expr non calculable {e['expr']!r}"); continue
            de, a = e.get("de", xmin), e.get("a", xmax)
            ok = 0
            for k in range(41):
                x = de + (a - de) * k / 40
                try:
                    y = fn(x)
                except (ValueError, ZeroDivisionError, OverflowError):
                    continue
                if isinstance(y, (int, float)) and math.isfinite(y) and ymin <= y <= ymax:
                    ok += 1
            if ok < 5:
                err.append(f"{q}: la courbe {e['expr']!r} sort presque entièrement du cadre")
        if f in ("ligne",):
            for p in e.get("pts") or []:
                dedans(p, "pts")
        for k in ("de", "a", "at", "c"):
            if k in e and not (f in ("arc", "courbe") and k in ("de", "a")):
                dedans(e[k], k)
        if f == "repere" and not axes:
            err.append(f"{q}: repere demande des axes")


def verifier(chemin: str) -> tuple[list, list, int]:
    d = json.loads(Path(chemin).read_text(encoding="utf-8"))
    err, avert, n = [], [], 0
    for a in d.get("activities") or []:
        for s in a.get("slides") or []:
            figs = (s.get("concentration") or {}).get("cahier_figures")
            if figs is None:
                continue
            if not isinstance(figs, list):
                err.append(f"{s['id']}: cahier_figures doit être une liste"); continue
            if len(figs) > 2:
                err.append(f"{s['id']}: {len(figs)} figures (2 au plus)")
            for i, f in enumerate(figs):
                n += 1
                verifier_figure(f, f"{s['id']}[{i}]", err, avert)
    for se in d.get("seances") or []:
        for b in se.get("blocs") or []:
            figs = b.get("cahier_figures")
            if figs is None:
                continue
            if len(figs) > 2:
                err.append(f"bloc {b['id']}: {len(figs)} figures (2 au plus, tout doit tenir dans l'écran)")
            for i, f in enumerate(figs):
                verifier_figure(f, f"bloc {b['id']}[{i}]", err, avert)
    return err, avert, n


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if args == ["--tous"] or not args:
        args = sorted(glob.glob(str(RACINE / "backend/data/courses/*_ch*_*.json")))
        args = [a for a in args if "_course_v1" not in a and "_script_" not in a]
    total_err = 0
    for c in args:
        err, avert, n = verifier(c)
        total_err += len(err)
        print(f"{Path(c).name}: {n} figure(s) de diapo, {len(err)} erreur(s), {len(avert)} avertissement(s)")
        for e in err:
            print("  ERREUR", e)
        for a in avert:
            print("  avert.", a)
    return 1 if total_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
