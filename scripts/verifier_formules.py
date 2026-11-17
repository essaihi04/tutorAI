"""Relations écrites à plat devant l'élève : ce qu'il faut encore remettre « comme dans le cahier ».

Règle de l'utilisateur (17 novembre 2026, « l'écriture doit être bien écrite comme dans le cahier pour les relations ») :
une division écrite à l'écran est une vraie fraction, numérateur au-dessus du trait.

- Cours (`backend/data/courses/*.json`) : le texte AFFICHÉ (cahier, bullets, ecrit, attendu, texte…) passe par
  `<Formule>`, qui empile « a/b » mais laisse « a / b » (avec espaces) en barre plate. Signale les barres espacées entre
  deux grandeurs et les lettres grecques écrites en toutes lettres (« lambda », « tau ») ; la voix n'est pas lue.
- Simulations (`frontend/public/media/simulations/**.html|.js`) : à la craie, une fraction s'écrit `⟦num|dén⟧`
  (kit `shared/tableau/tableau.js`). Signale, dans les chaînes écrites au tableau (`texte(`, `formules:`, `lignes:`),
  une division à plat.

Usage :  python -I scripts/verifier_formules.py [fichiers ou dossiers…]
         (sans argument : cours de physique et de SVT, et leurs dossiers de simulations)
Ne modifie rien ; code de sortie 1 s'il reste quelque chose.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
COURS = RACINE / "backend" / "data" / "courses"
SIMS = RACINE / "frontend" / "public" / "media" / "simulations"

# Champs qui ne sont pas lus à l'écran (voix, identifiants, courbes) : jamais signalés.
NON_ECRITS = {"speech_text", "note", "alt", "parole", "mot", "dit", "enonce_dit", "enonce_audio", "audio", "expr", "id",
              "url", "speech_hash", "commande", "repere", "moment", "cible", "ancre", "reprend", "phase", "type", "kind",
              "demarrer", "parametres", "apres_mot", "competence_id", "competence_ids", "slide_ids", "cadre_ids",
              "stable_id", "fr", "mixed", "darija"}
MOTS_FONCTION = {"ln", "sin", "cos", "tan", "exp", "lim", "min", "mol", "div", "max"}
BARRE_ESPACEE = re.compile(r"(\S+)\s+/\s+(\S+)")
GREC = re.compile(r"\b(lambda|tau|theta|Delta m|delta m)\b")
UNITE = re.compile(r"^(?:[kcmµnM]?(?:m|s|g|mol|L|V|A|J|W|Hz|N|Pa|Ω|F|H|eV)|°C|h|min|div|j|an|ans|nucléon)$")


def mot(s: str) -> bool:
    """Un mot français (≥ 3 lettres minuscules, hors fonctions et unités) : « opposé / adjacent », « vrai / faux »."""
    return any(w not in MOTS_FONCTION for w in re.findall(r"[a-zéèêàçùâîôûœ']{3,}", s))


def division_espacee(texte: str) -> list[str]:
    trouves = []
    for m in BARRE_ESPACEE.finditer(texte):
        g, d = m.group(1), m.group(2).rstrip(".,;:)")
        if not d or mot(g) or mot(d) or "'" in g + d or "%" in g + d or "Hb" in g + d:
            continue
        if re.fullmatch(r"y\(.\)", g) and re.match(r"y\(.\)", m.group(2)):   # « photo y(x) / film y(t) » : deux options
            continue
        if re.fullmatch(r"[A-Z]", g) and re.fullmatch(r"[A-Z]", d):   # « hémoglobine A / S » : deux formes, pas un rapport
            continue
        trouves.append(m.group(0))
    return trouves


def verifier_cours(f: Path) -> list[str]:
    sortie: list[str] = []

    def walk(o, chemin: str):
        if isinstance(o, dict):
            for k, v in o.items():
                if k not in NON_ECRITS:
                    walk(v, f"{chemin}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{chemin}[{i}]")
        elif isinstance(o, str):
            for d in division_espacee(o):
                sortie.append(f"{f.name}{chemin} : barre à plat « {d} » → écrire « {d.replace(' / ', '/')} » (parenthèses si plusieurs termes)")
            for g in GREC.findall(o):
                sortie.append(f"{f.name}{chemin} : « {g} » en toutes lettres → le symbole")

    walk(json.loads(f.read_text(encoding="utf-8")), "")
    return sortie


CHAINE = re.compile(r"""(['"`])((?:\\.|(?!\1).)*)\1""")
LIGNE_CRAIE = re.compile(r"\.texte\(|formules\s*:|lignes\s*:")


def verifier_simulation(f: Path) -> list[str]:
    sortie = []
    for n, ligne in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not LIGNE_CRAIE.search(ligne):
            continue
        for m in CHAINE.finditer(ligne):
            s = re.sub(r"⟦[^⟧]*⟧", "", m.group(2))
            s = re.sub(r"\$\{(?:[^{}]|\{[^{}]*\})*\}", "…", s)   # un calcul JS dans ${…} (fr(d / 10)) n'est pas de la craie
            s = re.sub(r"\^(\{[^}]*\}|\([^)]*\))", "…", s)   # une barre dans un exposant (e^{−t/τ}) reste une barre
            for d in division_espacee(s):
                sortie.append(f"{f.relative_to(RACINE)}:{n} : à la craie « {d} » → ⟦num|dén⟧")
            for a, b in re.findall(r"([A-Za-zλτθΔν₀-₉²]+)/([A-Za-zλτθΔν(][A-Za-z₀-₉]*)", s):
                if UNITE.match(a) or UNITE.match(b) or mot(a) or mot(b) or (a.isalpha() and len(a) > 2 and b.isalpha() and len(b) > 2):
                    continue
                sortie.append(f"{f.relative_to(RACINE)}:{n} : à la craie « {a}/{b} » → ⟦{a}|{b}⟧")
    return sortie


def cibles(args: list[str]) -> list[Path]:
    if args:
        out = []
        for a in args:
            p = Path(a).resolve()
            out += (sorted(p.rglob("*.html")) + sorted(p.rglob("*.js"))) if p.is_dir() else [p]
        return out
    # les anciens decks (…_v1.json, …_script_v3.json) sont remplacés par les cours en mode concentration
    out = [f for f in sorted(COURS.glob("phys_ch[1-9]_*.json")) + sorted(COURS.glob("svt_ch[1-4]_*.json")) if not re.search(r"_v\d+\.json$", f.name)]
    for d in sorted((SIMS / "physics").glob("*-tableau")) + sorted((SIMS / "svt").glob("*-tableau")):
        out += sorted(d.glob("*.html")) + sorted(d.glob("*.js"))
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    total = 0
    for f in cibles(sys.argv[1:]):
        lignes = verifier_cours(f) if f.suffix == ".json" else verifier_simulation(f)
        for l in lignes:
            print(l)
        total += len(lignes)
    print(f"{total} relation(s) à remettre comme dans le cahier", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
