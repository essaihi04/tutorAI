"""
Test multi-tours — changement de THÈME d'exercice BAC en mode libre.

Scénario utilisateur :
  Tour 1  « exercice bac sur la pollution »   → attendu : panneau pollution
  Tour 2  « exercice bac sur la génétique »   → attendu : panneau GÉNÉTIQUE
  Tour 3  « exercice bac sur l'ATP »          → attendu : panneau ATP
  Tour 4  « exercice bac sur la radioactivité »→ attendu : panneau nucléaire
  Tour 5  « exercice bac sur l'immunité »      → attendu : panneau immun

Bug observé : après le tour 1, les tours suivants ne changent pas d'exercice
— le système reste collé sur la pollution.

Ce script reproduit fidèlement la chaîne prod :
  (1) build le system prompt libre (+ exam_view_block une fois qu'un exam
      est ouvert),
  (2) appelle le LLM avec l'historique chat,
  (3) cherche un tag <exam_exercise>…</exam_exercise> dans la réponse,
  (4) si présent, appelle exam_bank.search_full_exercises comme prod,
  (5) met à jour current_exam_view avec l'exercice retourné (comme le
      frontend envoie set_exam_panel_view),
  (6) enchaîne au tour suivant.

Pour chaque tour, on vérifie :
  • Le LLM a-t-il émis <exam_exercise> ?  (critique)
  • Le topic/exercice_name renvoyé contient-il le thème attendu ?
  • L'exam_id a-t-il changé par rapport au tour précédent ?

Usage :
    python backend/scripts/test_multiturn_topic_switch.py
    python backend/scripts/test_multiturn_topic_switch.py -v     # verbose
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import types as _types
import unicodedata
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Stub heavy ML deps so we can import LLMService without loading FAISS.
_stub = _types.ModuleType("app.services.rag_service")
class _NoopRag:
    def build_grounded_context(self, *a, **kw): return ""
    def search(self, *a, **kw): return []
def _get_rag_service(): return _NoopRag()
_stub.get_rag_service = _get_rag_service  # type: ignore
sys.modules["app.services.rag_service"] = _stub

from app.config import get_settings  # noqa: E402
from app.services.exam_bank_service import exam_bank  # noqa: E402
from app.services.llm_service import LLMService, llm_service  # noqa: E402

LLMService._ensure_rag_initialized = lambda self: None  # type: ignore


# ──────────────────────────────────────────────────────────────────────
#  Scénario multi-tours
# ──────────────────────────────────────────────────────────────────────
TURNS = [
    # (user_text, expected_theme_keywords, human_label)
    ("Donne-moi un exercice type BAC sur la pollution.",
     ["pollution", "polluant", "environnement", "dechet", "déchet",
      "ecologie", "écologie", "pesticide", "inorganique"],
     "Tour 1 — pollution"),
    ("Maintenant je veux un exercice type BAC sur la génétique.",
     ["genetique", "génétique", "adn", "arn", "chromosome", "meiose",
      "méiose", "allele", "allèle", "gene", "gène", "mendel", "brca",
      "drosophile", "caryotype", "hérédité", "heredite"],
     "Tour 2 — génétique (switch #1)"),
    ("Je veux un autre exercice type BAC sur l'ATP.",
     ["atp", "respiration", "mitochondr", "glycolyse", "krebs",
      "fermentation", "matière organique", "matiere organique", "levure"],
     "Tour 3 — ATP (switch #2)"),
    ("Change, donne-moi un exercice type BAC sur la radioactivité.",
     ["nucléaire", "nucleaire", "radioactivit", "désintégration",
      "desintegration", "noyau", "période", "periode"],
     "Tour 4 — nucléaire (switch #3)"),
    # NB: on évite l'immunité car elle n'est PAS au programme 2BAC Sciences
    # Physiques BIOF (elle est dans le track SVT). Le LLM refuse correctement
    # ce sujet. On teste plutôt la géologie, qui EST au programme.
    ("Et maintenant un exercice type BAC sur la tectonique des plaques.",
     ["geologie", "géologie", "subduction", "tectonique", "plaques",
      "lithosphère", "lithosphere", "métamorphisme", "metamorphisme",
      "chaîne de montagne", "chaine de montagne", "ophiolite", "gneiss"],
     "Tour 5 — géologie (switch #4)"),
]


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


def _matches(haystack: str, needles: list[str]) -> list[str]:
    hits = []
    for n in needles:
        n_norm = _strip(n)
        if not n_norm:
            continue
        stem = n_norm[:5] if len(n_norm) >= 6 else n_norm
        if stem in haystack:
            hits.append(n)
    return hits


def build_exam_view_block(view: dict) -> str:
    """Reproduit session_handler:1614-1675 (version condensée)."""
    subject = str(view.get("subject", "") or "").strip()
    year = str(view.get("year", "") or "").strip()
    session = str(view.get("session", "") or "").strip()
    exam_title = str(view.get("exam_title", "") or "").strip()
    exercise_name = str(view.get("exercise_name", "") or "").strip()
    q_content = str(view.get("question_content", "") or "").strip()
    q_correction = str(view.get("question_correction", "") or "").strip()

    header = " — ".join(
        b for b in [subject, session.capitalize() if session else "", year] if b
    ) or (exam_title or "Examen")

    block = f"""
[CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ À L'ÉTUDIANT]
⚠️ L'étudiant a CE PANNEAU D'EXAMEN ouvert en ce moment. Tu DOIS te baser EXCLUSIVEMENT sur ces informations. NE JAMAIS inventer une autre année, session, exercice ou question.

📚 Examen : {header}
📖 {exercise_name}

ÉNONCÉ EXACT DE LA QUESTION AFFICHÉE :
{q_content if q_content else '(non disponible)'}
"""
    if q_correction:
        block += f"\nCORRECTION OFFICIELLE :\n{q_correction}\n"
    block += """
RÈGLES STRICTES :
- Si l'étudiant parle de "cette question", "l'exercice", "l'examen", il parle TOUJOURS de CE qui est affiché ci-dessus.
- Tu cites l'année et la session EXACTES indiquées ci-dessus. JAMAIS d'autres.

🔄 BASCULE VERS UN AUTRE EXERCICE BAC — RÈGLE ÉLARGIE :
Tu DOIS émettre IMMÉDIATEMENT `<exam_exercise>mots-clés du thème demandé</exam_exercise>` dans CHACUN des cas suivants :
  (a) L'étudiant dit « autre exercice », « nouvel exercice », « ferme et ouvre », « différent », « autre année », « autre session », « change ».
  (b) L'étudiant demande un exercice BAC sur UN THÈME DIFFÉRENT de celui actuellement affiché ci-dessus, même SANS dire « autre ».
  (c) L'étudiant mentionne un thème clairement hors-sujet de l'exercice courant.

RÈGLES STRICTES pour la bascule :
  1. TOUJOURS émettre `<exam_exercise>…</exam_exercise>` — JAMAIS juste du texte ou un `<ui>` whiteboard.
  2. NE PAS fabriquer un faux énoncé d'examen sur le tableau.
  3. Annonce brièvement : « D'accord, je t'ouvre un exercice BAC sur [thème] » puis émets le tag IMMÉDIATEMENT après.

- EN CAS DE DOUTE entre « rester » et « basculer », BASCULE — émets le tag.
"""
    return block


async def call_llm(system_prompt: str, history: list[dict]) -> str:
    settings = get_settings()
    api_key = (getattr(settings, "deepseek_api_key", None)
               or getattr(settings, "DEEPSEEK_API_KEY", None))
    base_url = (getattr(settings, "deepseek_base_url", None)
                or "https://api.deepseek.com/v1")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY not set")

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": system_prompt}, *history],
        "temperature": 0.3,
        "max_tokens": 1500,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=90.0) as client:
        r = await client.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json=payload,
        )
        r.raise_for_status()
        return r.json().get("choices", [{}])[0].get("message", {}).get("content", "") or ""


# ──────────────────────────────────────────────────────────────────────
async def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    exam_bank._ensure_loaded()
    print(f"[test_multiturn] {len(exam_bank._questions)} questions indexées.")

    # Session state — mirrors session_handler attributes
    conversation_history: list[dict] = []
    current_exam_view: dict | None = None

    # Session context (libre mode, SVT by default — user was in libre mode)
    session_ctx = {
        "subject": "SVT",  # matches user report (SVT libre mode)
        "lesson_title": "",  # libre mode — no lesson
        "proficiency": "intermédiaire",
        "student_name": "Élève",
    }

    results = []
    for idx, (user_text, expected_kw, label) in enumerate(TURNS, 1):
        print("\n" + "═" * 78)
        print(f"■ {label}")
        print(f"   user_text = {user_text!r}")
        print("═" * 78)

        # 1) Build system prompt as session_handler does.
        libre_prompt = llm_service.build_libre_prompt(
            language="français",
            student_name=session_ctx["student_name"],
            proficiency=session_ctx["proficiency"],
            user_query=user_text,
        )
        system_prompt = libre_prompt
        if current_exam_view:
            system_prompt += "\n\n" + build_exam_view_block(current_exam_view)

        # 2) Push user message and call LLM.
        conversation_history.append({"role": "user", "content": user_text})
        ai_response = await call_llm(system_prompt, conversation_history)
        conversation_history.append({"role": "assistant", "content": ai_response})

        # 3) Extract <exam_exercise>…</exam_exercise> tag.
        m = re.search(r"<exam_exercise>(.*?)</exam_exercise>",
                      ai_response, re.DOTALL)
        if not m:
            m = re.search(r"<exam_exercise>([^<]*?)(?=<|$)",
                          ai_response, re.DOTALL)
        tag_content = m.group(1).strip() if m else None
        emitted_tag = bool(tag_content)

        print(f"   <exam_exercise> tag émis ? : "
              f"{'OUI ✅' if emitted_tag else 'NON ❌'}")
        if emitted_tag:
            print(f"   tag content              : {tag_content[:120]!r}")
        else:
            # Show a short snippet so we understand why the LLM did not switch.
            snip = ai_response[:300].replace("\n", " ")
            print(f"   LLM response (extrait)   : {snip!r}")

        # 4) If tag present, use its content. Otherwise, simulate the prod
        # `force_exam_panel` fallback: the resource_decision_service detects
        # exam intent from the user text ("exercice bac"…) and the backend
        # calls search_full_exercises with student_text as the query.
        # See session_handler.py:3407-3464.
        returned_exam = None
        search_origin = "tag"
        search_query = tag_content
        if not emitted_tag:
            student_lower = user_text.lower()
            exam_intent_kws = ("exercice bac", "exercice type bac",
                               "type bac", "sujet bac", "bac sur",
                               "bac national", "examen bac", "entraîne")
            if any(kw in student_lower for kw in exam_intent_kws):
                search_origin = "force_exam_panel fallback"
                search_query = user_text
                print(f"   (force_exam_panel fallback : "
                      f"search_query = student_text)")
            else:
                search_query = None

        if search_query:
            open_exam_id = (current_exam_view or {}).get("exam_id")
            results_list = exam_bank.search_full_exercises(
                query=search_query,
                subject=session_ctx.get("subject"),
                count=1,
                exclude_exam_id=open_exam_id,
                conversation_context=session_ctx.get("lesson_title") or None,
            )
            if results_list:
                returned_exam = results_list[0]
                hay = _haystack(returned_exam)
                hits = _matches(hay, expected_kw)
                print(f"   exercice renvoyé [{search_origin}] : "
                      f"{returned_exam.get('exam_label','?')} — "
                      f"{returned_exam.get('exercise_name','?')}  "
                      f"topic={returned_exam.get('topic','')[:40]!r}")
                print(f"   expected_hits            : {hits[:5]}")
                if args.verbose:
                    print(f"   exam_id                  : {returned_exam.get('exam_id','?')}")
            else:
                print(f"   ⚠️  search_full_exercises a renvoyé 0 résultat pour "
                      f"'{search_query}'")

        # 5) Verdict for this turn.
        verdict = "FAIL"
        reason = ""
        if returned_exam is None:
            if not emitted_tag and search_query is None:
                reason = ("LLM n'a PAS émis <exam_exercise> et aucun mot-clé "
                          "d'intent n'a déclenché le fallback")
            elif not emitted_tag:
                reason = (f"fallback force_exam_panel appelé mais 0 résultat "
                          f"pour '{search_query}'")
            else:
                reason = "LLM a émis le tag mais search = 0 résultat"
            verdict = "FAIL"
        else:
            hay = _haystack(returned_exam)
            hits = _matches(hay, expected_kw)
            if not hits:
                reason = (f"exercice NE MATCHE PAS le thème [via {search_origin}] "
                          f"(topic={returned_exam.get('topic','')[:30]})")
                verdict = "FAIL"
            elif idx > 1 and current_exam_view and returned_exam.get("exam_id") == current_exam_view.get("exam_id"):
                reason = f"même exam_id que le tour précédent — pas de switch [via {search_origin}]"
                verdict = "FAIL"
            else:
                reason = f"switch OK via {search_origin} (hits={hits[:3]})"
                verdict = "PASS"

        print(f"   >>> VERDICT : {'✅ ' + reason if verdict == 'PASS' else '❌ ' + reason}")
        results.append((label, verdict, reason, emitted_tag, returned_exam))

        # 6) Update current_exam_view for next turn (simulates frontend sending
        # set_exam_panel_view with the newly-opened exercise's first question).
        if returned_exam:
            qs = returned_exam.get("questions") or []
            first_q = qs[0] if qs else {}
            current_exam_view = {
                "exam_id": returned_exam.get("exam_id"),
                "subject": returned_exam.get("subject"),
                "year": returned_exam.get("year"),
                "session": returned_exam.get("session"),
                "exam_title": returned_exam.get("exam_label"),
                "exercise_name": returned_exam.get("exercise_name"),
                "exercise_index": 0,
                "exercise_total": 1,
                "question_number": 1,
                "question_total": len(qs),
                "question_content": (first_q.get("content") or "")[:1500],
                "question_correction": (first_q.get("correction") or "")[:1500],
                "topic": returned_exam.get("topic", ""),
            }

    # ── Summary ──
    print("\n" + "═" * 78)
    print("RÉSUMÉ")
    print("═" * 78)
    passed = sum(1 for _, v, _, _, _ in results if v == "PASS")
    for label, v, reason, emitted, ex in results:
        flag = "✅" if v == "PASS" else "❌"
        tag_flag = "tag=OK" if emitted else "tag=MANQUANT"
        print(f"  {flag}  {label:40s}  [{tag_flag}]  {reason}")
    print(f"\n  {passed}/{len(results)} tours ont correctement changé de thème.")

    # ── Diagnostic ──
    tag_failures = sum(1 for _, v, _, em, _ in results if v == "FAIL" and not em)
    search_failures = sum(1 for _, v, _, em, ex in results if v == "FAIL" and em and ex is None)
    topic_failures = sum(1 for _, v, _, em, ex in results if v == "FAIL" and em and ex is not None)

    if tag_failures:
        print(f"\n  🔎 {tag_failures} tours SANS tag <exam_exercise> "
              f"→ le LLM ne déclenche PAS la bascule. "
              f"Cause probable : exam_view_block trop restrictif (règle « BASCULE »). "
              f"Le prompt exige « AUTRE/NOUVEL/DIFFÉRENT… » — si l'étudiant ne "
              f"répète pas un de ces déclencheurs, le LLM reste sur l'exercice "
              f"courant.")
    if search_failures:
        print(f"\n  🔎 {search_failures} tours avec tag mais 0 résultat "
              f"→ exam_bank search fail. Vérifier les keywords/aliases.")
    if topic_failures:
        print(f"\n  🔎 {topic_failures} tours avec tag + résultat mais mauvais thème "
              f"→ bug de routage (exam_bank_service).")

    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    asyncio.run(main())
