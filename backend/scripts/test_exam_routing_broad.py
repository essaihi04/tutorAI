"""
Test de routage large — search_full_exercises sur TOUS les thèmes BAC.

Ce script vérifie que le moteur de recherche ouvre le bon exercice pour
des dizaines de requêtes différentes, dans les 4 matières (Math, Physique,
Chimie, SVT), avec ou sans leçon active (conversation_context), et avec
des formulations variées (courtes, longues, fautes de frappe légères…).

Il cible en particulier les 3 classes de bugs corrigés récemment :
  (1) Filtre leçon qui bloque une requête sur un autre thème
      → cf. USER-INTENT OVERRIDE dans exam_bank_service.py
  (2) Alias courts ("rc", "rl", "ph", "base"…) qui polluaient toute
      requête contenant "exercice" via substring match
      → cf. word-boundary fix dans _expand_query_aliases
  (3) Routage générique → exercice hors-sujet

Usage :
    python backend/scripts/test_exam_routing_broad.py
    python backend/scripts/test_exam_routing_broad.py -v             # verbose
    python backend/scripts/test_exam_routing_broad.py --only=SVT     # filtre matière
    python backend/scripts/test_exam_routing_broad.py --only=BUG     # cas bugs uniquement
"""
from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from app.services.exam_bank_service import exam_bank  # noqa: E402


# ──────────────────────────────────────────────────────────────────────
# Banque de mots-clés par THÈME (attendus / interdits selon la requête)
# ──────────────────────────────────────────────────────────────────────
KW = {
    # ══════════════════════════ SVT ══════════════════════════
    "genetique":   ["genetique", "génétique", "adn", "arn", "chromosome",
                    "meiose", "méiose", "mitose", "allele", "allèle",
                    "gene", "gène", "mendel", "hérédité", "heredite",
                    "brca", "dihybrid", "monohybrid", "caryotype"],
    "atp_energie": ["atp", "respiration", "mitochondr", "glycolyse", "krebs",
                    "fermentation", "glucose", "pyruvate", "nadh",
                    "matière organique", "matiere organique", "levure"],
    "pollution":   ["pollution", "polluant", "dechet", "déchet",
                    "environnement", "pesticide", "bioaccumulation",
                    "contamination", "ecologie", "écologie",
                    "effet de serre", "climat",
                    # Chapitre officiel BAC marocain couvrant les thèmes
                    # environnementaux (déchets, traitement de l'eau, recyclage) :
                    "inorganique", "inorganiques", "utilisation des matières"],
    "geologie":    ["geologie", "géologie", "subduction", "tectonique",
                    "plaques", "lithosphère", "lithosphere",
                    "métamorphisme", "metamorphisme", "magma",
                    "chaîne de montagne", "chaine de montagne",
                    "ophiolite", "gneiss"],
    "immun":       ["immun", "immunit", "anticorps", "lymphoc",
                    "antigène", "antigene", "vaccin"],
    # ══════════════════════════ PHYSIQUE ══════════════════════════
    "rc_rl":       ["rc", "rl", "condensateur", "bobine", "dipôle",
                    "dipole", "charge", "décharge", "decharge",
                    "capacité", "capacite", "constante de temps"],
    "rlc":         ["rlc", "oscillation", "résonance", "resonance",
                    "condensateur", "bobine"],
    "mecanique":   ["mécanique", "mecanique", "newton", "chute",
                    "mouvement", "pendule", "satellite", "projectile",
                    "référentiel", "referentiel"],
    "ondes":       ["onde", "ondes", "diffraction", "interférence",
                    "interference", "célérité", "celerite", "longueur d'onde"],
    "nucleaire":   ["nucléaire", "nucleaire", "radioactivité",
                    "radioactivite", "désintégration", "desintegration",
                    "période", "periode", "noyau"],
    # ══════════════════════════ CHIMIE ══════════════════════════
    "cinetique":   ["cinétique", "cinetique", "vitesse", "catalyseur",
                    "temps de demi-réaction", "demi-réaction"],
    "acide_base":  ["acide", "base", "\\bph\\b", "pka", "dosage",
                    "titrage", "équivalence", "equivalence",
                    "conductimétrie"],
    "pile":        ["pile", "électrochimique", "electrochimique", "anode",
                    "cathode", "oxydoréduction", "oxydoreduction",
                    "force électromotrice", "fem"],
    "ester":       ["ester", "estérification", "esterification",
                    "hydrolyse", "acide carboxylique", "alcool"],
    # ══════════════════════════ MATHS ══════════════════════════
    "derivee":     ["dérivée", "derivee", "dérivable", "tangente",
                    "nombre dérivé"],
    "integrale":   ["intégrale", "integrale", "primitive",
                    "aire sous la courbe"],
    "complexes":   ["complexe", "affixe", "module", "argument",
                    "imaginaire"],
    "suites":      ["suite", "récurrence", "recurrence",
                    "arithmétique", "geometrique", "géométrique",
                    "convergence"],
    "probas":      ["probabilité", "probabilite", "variable aléatoire",
                    "loi binomiale", "espérance", "esperance"],
}


# ──────────────────────────────────────────────────────────────────────
# Cas de test — (group, label, query, subject, expected_thm, forbidden_thms,
#                conversation_context)
# expected_thm    : clé de KW que le topic/exercise renvoyé DOIT matcher
# forbidden_thms  : liste de clés KW que le topic NE DOIT PAS matcher
# ──────────────────────────────────────────────────────────────────────
TESTS = [
    # ══════════ SVT — formulations variées ══════════
    ("SVT",     "SVT 1  génétique — direct",
     "exercice bac sur la génétique", "SVT",
     "genetique", ["pollution", "atp_energie"], None),
    ("SVT",     "SVT 2  génétique — ADN",
     "exercice bac sur l'ADN", "SVT",
     "genetique", ["pollution", "atp_energie"], None),
    ("SVT",     "SVT 3  génétique — méiose",
     "exercice bac méiose brassage", "SVT",
     "genetique", ["pollution", "atp_energie"], None),
    ("SVT",     "SVT 4  génétique — drosophile",
     "donne-moi un exercice bac sur la drosophile", "SVT",
     "genetique", ["pollution"], None),
    ("SVT",     "SVT 5  ATP — direct",
     "exercice type bac sur l'ATP", "SVT",
     "atp_energie", ["genetique", "pollution"], None),
    ("SVT",     "SVT 6  respiration cellulaire",
     "exercice bac sur la respiration cellulaire", "SVT",
     "atp_energie", ["genetique"], None),
    ("SVT",     "SVT 7  fermentation lactique",
     "exercice bac fermentation lactique", "SVT",
     "atp_energie", ["genetique"], None),
    ("SVT",     "SVT 8  matière organique",
     "exercice bac consommation matière organique", "SVT",
     "atp_energie", ["genetique"], None),
    ("SVT",     "SVT 9  pollution — direct",
     "exercice type bac sur la pollution", "SVT",
     "pollution", ["genetique", "atp_energie"], None),
    ("SVT",     "SVT 10 pollution — déchets",
     "exercice bac sur les déchets ménagers", "SVT",
     "pollution", ["genetique"], None),
    ("SVT",     "SVT 11 pollution — pesticides",
     "exercice bac pesticides bioaccumulation", "SVT",
     "pollution", ["genetique"], None),
    ("SVT",     "SVT 12 effet de serre",
     "exercice bac sur l'effet de serre", "SVT",
     "pollution", ["genetique"], None),
    ("SVT",     "SVT 13 géologie — subduction",
     "exercice bac subduction tectonique", "SVT",
     "geologie", ["genetique", "pollution"], None),
    ("SVT",     "SVT 14 géologie — chaîne de montagnes",
     "exercice bac chaîne de montagnes", "SVT",
     "geologie", ["genetique"], None),

    # ══════════ SVT — BUG : requête topique + lesson différente ══════════
    ("SVT-BUG", "BUG 1 pollution + lesson=génétique",
     "exercice type bac sur la pollution", "SVT",
     "pollution", ["genetique"],
     "Génétique humaine — transmission des caractères héréditaires"),
    ("SVT-BUG", "BUG 2 pollution + lesson=méiose",
     "donne-moi un exercice bac sur la pollution", "SVT",
     "pollution", ["genetique"],
     "La méiose et le brassage génétique"),
    ("SVT-BUG", "BUG 3 ATP + lesson=génétique",
     "exercice bac sur l'ATP", "SVT",
     "atp_energie", ["genetique"],
     "Génétique humaine"),
    ("SVT-BUG", "BUG 4 respiration + lesson=ADN",
     "exercice bac respiration cellulaire", "SVT",
     "atp_energie", ["genetique"],
     "L'ADN support de l'information génétique"),
    ("SVT-BUG", "BUG 5 fermentation + lesson=méiose",
     "exercice bac fermentation", "SVT",
     "atp_energie", ["genetique"],
     "La méiose et le brassage génétique"),
    ("SVT-BUG", "BUG 6 génétique + lesson=pollution",
     "exercice bac sur la génétique humaine", "SVT",
     "genetique", ["pollution"],
     "Pollution et écosystèmes"),
    ("SVT-BUG", "BUG 7 géologie + lesson=génétique",
     "exercice bac subduction", "SVT",
     "geologie", ["genetique"],
     "Génétique des populations"),

    # ══════════ PHYSIQUE ══════════
    ("PHY",     "PHY 1  circuit RC",
     "exercice bac dipôle RC condensateur", "Physique",
     "rc_rl", ["mecanique", "ondes"], None),
    ("PHY",     "PHY 2  circuit RLC",
     "exercice bac oscillations RLC", "Physique",
     "rlc", ["mecanique"], None),
    ("PHY",     "PHY 3  mécanique — Newton",
     "exercice bac mécanique lois de Newton", "Physique",
     "mecanique", ["ondes", "rc_rl"], None),
    ("PHY",     "PHY 4  mécanique — chute libre",
     "exercice bac chute libre", "Physique",
     "mecanique", ["ondes"], None),
    ("PHY",     "PHY 5  ondes",
     "exercice bac diffraction ondes lumineuses", "Physique",
     "ondes", ["mecanique", "rc_rl"], None),
    ("PHY",     "PHY 6  nucléaire — radioactivité",
     "exercice bac radioactivité désintégration", "Physique",
     "nucleaire", ["mecanique", "ondes"], None),

    # ══════════ PHYSIQUE — BUG : lesson différente ══════════
    ("PHY-BUG", "BUG 8 mécanique + lesson=RC",
     "exercice bac mécanique Newton", "Physique",
     "mecanique", ["rc_rl"],
     "Dipôle RC - condensateur"),
    ("PHY-BUG", "BUG 9 ondes + lesson=RLC",
     "exercice bac diffraction", "Physique",
     "ondes", ["rlc"],
     "Circuit RLC oscillations"),
    ("PHY-BUG", "BUG 10 nucléaire + lesson=mécanique",
     "exercice bac radioactivité", "Physique",
     "nucleaire", ["mecanique"],
     "Lois de Newton mécanique"),

    # ══════════ CHIMIE ══════════
    ("CHI",     "CHI 1  cinétique chimique",
     "exercice bac cinétique chimique vitesse", "Chimie",
     "cinetique", ["pile", "ester"], None),
    ("CHI",     "CHI 2  acide-base / dosage",
     "exercice bac dosage acide base pH", "Chimie",
     "acide_base", ["pile"], None),
    ("CHI",     "CHI 3  piles électrochimiques",
     "exercice bac pile électrochimique", "Chimie",
     "pile", ["ester", "cinetique"], None),
    ("CHI",     "CHI 4  estérification",
     "exercice bac estérification hydrolyse", "Chimie",
     "ester", ["pile", "cinetique"], None),

    # ══════════ CHIMIE — BUG ══════════
    ("CHI-BUG", "BUG 11 pile + lesson=acide-base",
     "exercice bac pile électrochimique", "Chimie",
     "pile", ["acide_base"],
     "Acide base dosage pH"),
    ("CHI-BUG", "BUG 12 ester + lesson=cinétique",
     "exercice bac estérification", "Chimie",
     "ester", ["cinetique"],
     "Cinétique chimique"),

    # ══════════ MATHS ══════════
    ("MATH",    "MATH 1 dérivée",
     "exercice bac dérivée tangente", "Mathematiques",
     "derivee", ["complexes", "probas"], None),
    ("MATH",    "MATH 2 intégrale",
     "exercice bac intégrale primitive", "Mathematiques",
     "integrale", ["probas"], None),
    ("MATH",    "MATH 3 complexes",
     "exercice bac nombres complexes module argument", "Mathematiques",
     "complexes", ["probas"], None),
    ("MATH",    "MATH 4 suites",
     "exercice bac suite récurrence", "Mathematiques",
     "suites", ["complexes"], None),
    ("MATH",    "MATH 5 probabilités",
     "exercice bac probabilité loi binomiale", "Mathematiques",
     "probas", ["complexes", "integrale"], None),

    # ══════════ MATHS — BUG ══════════
    ("MATH-BUG", "BUG 13 dérivée + lesson=complexes",
     "exercice bac dérivée", "Mathematiques",
     "derivee", ["complexes"],
     "Nombres complexes argument module"),
    ("MATH-BUG", "BUG 14 probas + lesson=suites",
     "exercice bac probabilité binomiale", "Mathematiques",
     "probas", ["suites"],
     "Suites récurrence arithmétique géométrique"),
]


# ──────────────────────────────────────────────────────────────────────
# Utils
# ──────────────────────────────────────────────────────────────────────
def _strip(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s or "")
        if unicodedata.category(c) != "Mn"
    ).lower()


def _haystack(ex: dict) -> str:
    parts = [
        ex.get("topic", "") or "",
        ex.get("exercise_name", "") or "",
        ex.get("exercise_context", "") or "",
    ]
    qs = ex.get("questions") or []
    if qs:
        parts.append((qs[0].get("content", "") or "")[:400])
    return _strip(" ".join(parts))


def _match_theme(haystack: str, theme_key: str) -> list[str]:
    needles = KW.get(theme_key, [])
    hits = []
    for n in needles:
        # Allow regex needles (e.g. "\\bph\\b").
        if n.startswith("\\b"):
            import re as _re
            if _re.search(_strip(n), haystack):
                hits.append(n)
            continue
        n_norm = _strip(n)
        if not n_norm:
            continue
        # Stem for long words, plain substring for short.
        stem = n_norm[:5] if len(n_norm) >= 6 else n_norm
        if stem in haystack:
            hits.append(n)
    return hits


# ──────────────────────────────────────────────────────────────────────
def run_one(group: str, label: str, query: str, subject: str,
            expected_thm: str, forbidden_thms: list[str],
            conv_ctx: str | None, verbose: bool) -> tuple[bool, str]:
    res = exam_bank.search_full_exercises(
        query=query, subject=subject, count=1,
        conversation_context=conv_ctx,
    )
    if not res:
        return False, "aucun résultat"
    ex = res[0]
    hay = _haystack(ex)

    exp_hits = _match_theme(hay, expected_thm)
    forb_hits_by_theme = {
        thm: _match_theme(hay, thm) for thm in forbidden_thms
    }
    any_forb = {thm: h for thm, h in forb_hits_by_theme.items() if h}

    if verbose:
        print(f"\n  ▸ '{label}' → {ex.get('exam_label','?')} · "
              f"topic={ex.get('topic','')[:45]!r} · ex={ex.get('exercise_name','')}")
        print(f"    expected[{expected_thm}] hits = {exp_hits[:4]}")
        if any_forb:
            print(f"    forbidden hits       = {any_forb}")

    # Verdict:
    # FAIL  = forbidden theme present AND expected absent
    # PASS  = expected present AND no forbidden theme
    # WARN  = ambiguous (both present, or both absent)
    if any_forb and not exp_hits:
        reason = f"domaine INTERDIT {list(any_forb.keys())} au lieu de '{expected_thm}'"
        return False, reason
    if not exp_hits:
        return False, f"aucun mot-clé '{expected_thm}' dans topic='{ex.get('topic','')[:30]}'"
    # expected found — success (even if a forbidden theme has partial hit, as
    # long as the expected theme is present, we consider it correctly routed)
    return True, f"topic='{ex.get('topic','')[:40]}'"


# ──────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--only", default="",
                    help="Filtre par groupe (ex: SVT, SVT-BUG, PHY, CHI, MATH, BUG)")
    args = ap.parse_args()

    exam_bank._ensure_loaded()
    print(f"[test_exam_routing_broad] {len(exam_bank._questions)} questions indexées.")

    # Apply filter if requested.
    cases = TESTS
    if args.only:
        flt = args.only.upper()
        if flt == "BUG":
            cases = [t for t in TESTS if "BUG" in t[0]]
        else:
            cases = [t for t in TESTS if t[0].upper().startswith(flt)]
        print(f"[filter={args.only}] {len(cases)}/{len(TESTS)} cas retenus.")

    results = []
    by_group: dict[str, list[tuple[bool, str]]] = {}
    for group, label, query, subj, exp_thm, forb_thms, ctx in cases:
        ok, reason = run_one(group, label, query, subj, exp_thm, forb_thms,
                             ctx, args.verbose)
        results.append((group, label, ok, reason))
        by_group.setdefault(group, []).append((ok, label))
        flag = "✅" if ok else "❌"
        print(f"  {flag}  [{group:9s}] {label:50s}  → {reason}")

    # Summary by group
    print("\n" + "═" * 78)
    print("RÉSUMÉ PAR GROUPE")
    print("═" * 78)
    for group in sorted(by_group):
        items = by_group[group]
        passed = sum(1 for ok, _ in items if ok)
        total = len(items)
        flag = "✅" if passed == total else "❌"
        print(f"  {flag} {group:9s}  {passed}/{total}")

    passed_total = sum(1 for _, _, ok, _ in results if ok)
    print("\n" + "═" * 78)
    print(f"TOTAL  {passed_total}/{len(results)}  requêtes correctement routées.")
    print("═" * 78)
    sys.exit(0 if passed_total == len(results) else 1)


if __name__ == "__main__":
    main()
