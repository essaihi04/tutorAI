"""
Reproduction test — "exercice type BAC sur la pollution" ouvre un exercice de génétique.

Ce script reproduit le chemin exact exécuté par le WebSocket handler quand
l'utilisateur demande un exercice BAC sur un sujet donné :

    session_handler.py
      └── exam_bank.search_full_exercises(query=..., subject="SVT", count=1)

Il affiche, pour chaque requête de test :
    1) la query brute,
    2) l'expansion d'alias (_expand_query_aliases),
    3) les keywords extraits (_extract_keywords → _get_topical_keywords),
    4) le TOP 10 des exercices scorés (topic + exercise_name + score),
    5) l'exercice finalement renvoyé à l'utilisateur (count=1),
    6) un verdict PASS / FAIL selon que le topic/exercise_name contient
       bien le domaine attendu (pollution/déchets/environnement) ou non
       (génétique / ADN / chromosome / méiose…).

Usage :
    python backend/scripts/test_pollution_query.py
    # ou pour plus de verbosité :
    python backend/scripts/test_pollution_query.py --verbose

Aucune connexion réseau requise — le script charge directement la banque
d'examens locale et appelle le service en mémoire.
"""
from __future__ import annotations

import argparse
import logging
import re
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
#  Test cases — chaque tuple = (label, query, expected_kw, forbidden_kw)
# ──────────────────────────────────────────────────────────────────────
# expected_kw  : le topic / exercise_name de l'exercice retourné DOIT
#                contenir au moins un de ces mots (accent-insensible).
# forbidden_kw : si le topic contient l'un de ces mots, c'est un FAIL
#                (= le bug reproduit par l'utilisateur).
POLLUTION_KW = [
    "pollution", "polluant", "dechet", "déchet", "environnement",
    "pesticide", "bioaccumulation", "contamination", "ecologie",
    "écologie", "ordure", "radioactif", "radioactivit",
    "effet de serre", "climat", "biogaz", "compost",
]
GENETIQUE_KW = [
    "genetique", "génétique", "adn", "arn", "chromosome", "meiose",
    "méiose", "mitose", "allele", "allèle", "mendel", "mutation",
    "gene", "gène", "caryotype", "drosophile", "hérédité", "heredite",
    "dihybridisme", "monohybridisme", "brca",
]
# ATP / énergie / respiration cellulaire — thème "Consommation de matière
# organique et flux d'énergie"
ATP_ENERGIE_KW = [
    "atp", "respiration", "mitochondr", "glycolyse", "krebs",
    "fermentation", "glucose", "pyruvate", "nadh", "fadh",
    "phosphorylation", "chaîne respiratoire", "chaine respiratoire",
    "matière organique", "matiere organique", "énergie cellulaire",
    "energie cellulaire", "levure", "muscle",
]

TEST_CASES = [
    # (label, query, subject, expected_kw, forbidden_kw, conv_context)
    # conv_context simulates session_context["lesson_title"] / ["chapter_title"]
    # which session_handler passes as `conversation_context=` — this is the
    # STRICT lesson filter that REJECTS any exercise not overlapping with
    # the current lesson keywords (see exam_bank_service.py §686-711).
    ("pollution — direct",
     "exercice type bac sur la pollution", "SVT",
     POLLUTION_KW, GENETIQUE_KW, None),
    ("pollution — courte",
     "pollution", "SVT", POLLUTION_KW, GENETIQUE_KW, None),
    ("déchets ménagers",
     "donne-moi un exercice bac sur les déchets ménagers", "SVT",
     POLLUTION_KW, GENETIQUE_KW, None),
    ("environnement",
     "exercice type bac sur l'environnement", "SVT",
     POLLUTION_KW, GENETIQUE_KW, None),
    ("pesticides / bioaccumulation",
     "exercice bac pesticides bioaccumulation", "SVT",
     POLLUTION_KW, GENETIQUE_KW, None),
    ("effet de serre",
     "exercice bac sur l'effet de serre", "SVT",
     POLLUTION_KW, GENETIQUE_KW, None),

    # ─── Reproduction du bug utilisateur — lesson_title injecté ────
    # Scénario : l'élève étudiait la génétique, puis demande « exercice
    # bac sur la pollution ». Le session_handler passe lesson_title
    # comme conversation_context → le STRICT LESSON FILTER rejette tous
    # les exercices de pollution car leur texte ne contient pas les
    # mots-clés « génétique ». Il ne reste QUE des exercices de génétique.
    ("BUG — pollution + lesson=génétique",
     "exercice type bac sur la pollution", "SVT",
     POLLUTION_KW, GENETIQUE_KW,
     "Génétique humaine — transmission des caractères héréditaires"),
    ("BUG — pollution + lesson=méiose",
     "donne-moi un exercice bac sur la pollution", "SVT",
     POLLUTION_KW, GENETIQUE_KW,
     "La méiose et le brassage génétique"),
    ("BUG — déchets + lesson=ADN",
     "exercice bac sur les déchets", "SVT",
     POLLUTION_KW, GENETIQUE_KW,
     "L'ADN support de l'information génétique"),

    # Control — confirm genetics queries still route to genetics
    ("CONTROL génétique",
     "exercice type bac sur la génétique", "SVT",
     GENETIQUE_KW, POLLUTION_KW, None),

    # ─── ATP / énergie / respiration cellulaire ─────────────────────
    ("ATP — direct",
     "exercice type bac sur l'ATP", "SVT",
     ATP_ENERGIE_KW, GENETIQUE_KW, None),
    ("ATP — courte",
     "atp", "SVT", ATP_ENERGIE_KW, GENETIQUE_KW, None),
    ("respiration cellulaire",
     "exercice bac sur la respiration cellulaire", "SVT",
     ATP_ENERGIE_KW, GENETIQUE_KW, None),
    ("fermentation",
     "exercice bac fermentation lactique", "SVT",
     ATP_ENERGIE_KW, GENETIQUE_KW, None),
    ("matière organique / énergie",
     "exercice bac consommation matière organique énergie", "SVT",
     ATP_ENERGIE_KW, GENETIQUE_KW, None),
    # Bug scenario — user was studying génétique, asks for ATP exercise
    ("BUG — ATP + lesson=génétique",
     "exercice bac sur l'ATP", "SVT",
     ATP_ENERGIE_KW, GENETIQUE_KW,
     "Génétique humaine — transmission des caractères héréditaires"),
    ("BUG — respiration + lesson=méiose",
     "exercice bac sur la respiration cellulaire", "SVT",
     ATP_ENERGIE_KW, GENETIQUE_KW,
     "La méiose et le brassage génétique"),
    ("BUG — fermentation + lesson=ADN",
     "exercice bac fermentation", "SVT",
     ATP_ENERGIE_KW, GENETIQUE_KW,
     "L'ADN support de l'information génétique"),
]


def _strip(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s or "")
        if unicodedata.category(c) != "Mn"
    ).lower()


def _haystack(ex: dict) -> str:
    """Concatenate topic + exercise_name + exercise_context + first question."""
    parts = [
        ex.get("topic", ""),
        ex.get("exercise_name", ""),
        ex.get("exercise_context", "") or "",
    ]
    qs = ex.get("questions") or []
    if qs:
        parts.append((qs[0].get("content", "") or "")[:300])
    return _strip(" ".join(parts))


def _matches_any(haystack: str, needles: list[str]) -> list[str]:
    hits = []
    for n in needles:
        n_norm = _strip(n)
        if not n_norm:
            continue
        # Use word-ish substring match; stem for longer words.
        if len(n_norm) >= 6:
            if n_norm[:5] in haystack:
                hits.append(n)
        else:
            if n_norm in haystack:
                hits.append(n)
    return hits


def run_one(label: str, query: str, subject: str,
            expected_kw: list[str], forbidden_kw: list[str],
            conv_context: str, verbose: bool) -> bool:
    print(f"\n{'═' * 78}")
    print(f"■ {label}")
    print(f"  query     = {query!r}")
    print(f"  subject   = {subject}")
    print(f"  lesson_ctx= {conv_context!r}")
    print(f"{'═' * 78}")

    # 1) Expansion & keywords — peek at private helpers to explain scoring
    expanded = exam_bank._expand_query_aliases(query)
    query_kw = exam_bank._extract_keywords(expanded)
    topical = exam_bank._get_topical_keywords(query_kw)
    print(f"  ▸ expansion  : {expanded[:200]}")
    print(f"  ▸ keywords   : {sorted(query_kw)[:15]}")
    print(f"  ▸ topical    : {sorted(topical)[:15]}")

    # 2) Call the EXACT same API the WebSocket handler calls (count=1)
    results = exam_bank.search_full_exercises(
        query=query,
        subject=subject,
        count=1,
        conversation_context=conv_context,
    )

    if not results:
        print("  ⚠️  Aucun exercice retourné (search_full_exercises vide).")
        return False

    # 3) Show top candidates (ask for count=10 to see scoring context)
    top10 = exam_bank.search_full_exercises(
        query=query, subject=subject, count=10,
        conversation_context=conv_context,
    )
    if verbose and top10:
        print(f"\n  Top {min(10, len(top10))} candidats :")
        for i, ex in enumerate(top10, 1):
            marker = "◀ CHOISI" if i == 1 else ""
            print(f"   {i:2d}. score={ex.get('_match_score', 0):.3f}  "
                  f"year={ex.get('year','?')}  "
                  f"topic={ex.get('topic','')[:40]!r:42s}  "
                  f"ex={ex.get('exercise_name','')[:50]!r} {marker}")

    # 4) Verdict on the returned exercise
    chosen = results[0]
    hay = _haystack(chosen)
    exp_hits = _matches_any(hay, expected_kw)
    forb_hits = _matches_any(hay, forbidden_kw)

    print(f"\n  ▸ EXERCICE RENVOYÉ :")
    print(f"      exam         : {chosen.get('exam_label','')}")
    print(f"      topic        : {chosen.get('topic','')!r}")
    print(f"      exercise_name: {chosen.get('exercise_name','')!r}")
    print(f"      score        : {chosen.get('_match_score', 0)}")
    print(f"      expected_hits: {exp_hits}")
    print(f"      forbidden_hits: {forb_hits}")

    if forb_hits and not exp_hits:
        print(f"  ❌ FAIL — l'exercice renvoyé est du DOMAINE INTERDIT "
              f"({forb_hits}) au lieu du domaine attendu.")
        return False
    if not exp_hits:
        print(f"  ⚠️  WARN — aucun mot-clé attendu trouvé mais pas de forbidden. "
              f"Classification ambiguë.")
        return False
    print(f"  ✅ PASS — l'exercice correspond au domaine demandé.")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="Afficher le top-10 des candidats pour chaque requête.")
    ap.add_argument("--log", action="store_true",
                    help="Activer les logs INFO de exam_bank_service (verbeux).")
    args = ap.parse_args()

    if args.log:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s %(name)s: %(message)s")

    # Force index load upfront so log lines don't interleave with test output
    exam_bank._ensure_loaded()
    print(f"[test_pollution_query] {len(exam_bank._questions)} questions indexées.")

    results = []
    for label, query, subject, exp, forb, ctx in TEST_CASES:
        ok = run_one(label, query, subject, exp, forb, ctx, verbose=args.verbose)
        results.append((label, ok))

    # ── Summary ────────────────────────────────────────────────────
    print(f"\n{'═' * 78}")
    print("RÉSUMÉ")
    print(f"{'═' * 78}")
    passed = sum(1 for _, ok in results if ok)
    for label, ok in results:
        flag = "✅ PASS" if ok else "❌ FAIL"
        print(f"  {flag}  {label}")
    print(f"\n  {passed}/{len(results)} requêtes correctement routées.")
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
