"""
Test MULTI-TOURS — mode COACHING — meme scenario que
test_exam_multiturn_bug.py mais dans une lecon coaching (SVT /
Genetique humaine / dihybridisme).

Verifie que le fix exclude_exam_id s'applique AUSSI en coaching et
que :
  - les requetes « un autre exercice BAC » ouvrent bien un exam_id
    DIFFERENT a chaque fois ;
  - apres une explication au tableau, le panneau d'examen peut etre
    re-ouvert sans bloquer ;
  - la matiere verrouillee par le coaching (SVT) n'est jamais
    remplacee par un autre sujet (Physique/Chimie/Maths).

Sortie : scripts/test_exam_multiturn_coaching_report.md
"""
from __future__ import annotations

import asyncio
import json
import sys
import time
import types as _types
from pathlib import Path

# Reuse all infrastructure from the libre test.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_stub = _types.ModuleType("app.services.rag_service")
class _NoopRag:
    def build_grounded_context(self, *a, **kw): return ""
    def search(self, *a, **kw): return []
def _get_rag_service(): return _NoopRag()
_stub.get_rag_service = _get_rag_service  # type: ignore
sys.modules["app.services.rag_service"] = _stub

import httpx  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.services.llm_service import LLMService  # noqa: E402
from app.services.exam_bank_service import exam_bank  # noqa: E402

LLMService._ensure_rag_initialized = lambda self: None  # type: ignore

# Reuse the shared simulation + helpers from the libre test
from test_exam_multiturn_bug import (  # type: ignore  # noqa: E402
    simulate_backend_exam_dispatch,
    build_exam_view_block,
    call_llm,
    evaluate,
    Turn,
    TurnReport,
    _norm,
)


# ─────────────────────────────────────────────────────────────────────
# Coaching lesson context
# ─────────────────────────────────────────────────────────────────────
COACHING_CTX = dict(
    subject="SVT",
    chapter_title="Génétique humaine — transmission de deux gènes",
    lesson_title="Brassage interchromosomique — dihybridisme",
    objective="Maîtriser le dihybridisme et l'échiquier de fécondation",
)


COACHING_TURNS: list[Turn] = [
    Turn(
        label="T1 — coaching : demander un premier exercice BAC",
        user_msg=(
            "Avant de continuer la leçon, peux-tu m'ouvrir un exercice BAC "
            "SVT pour pratiquer le dihybridisme (croisement F1×F1, "
            "échiquier) ? Un vrai exercice BAC officiel."
        ),
        expected_subject="SVT",
        must_contain_in_opened=["gen", "hybrid", "croisement", "echiquier",
                                "allele", "chromosome"],
    ),
    Turn(
        label="T2 — coaching : un AUTRE exercice BAC (switch #1)",
        user_msg=(
            "Merci ! Ferme celui-ci et ouvre-moi un AUTRE exercice BAC SVT "
            "sur la génétique (monohybridisme ou dihybridisme, peu importe)."
        ),
        expected_subject="SVT",
        must_contain_in_opened=["gen", "hybrid", "mendel", "croisement",
                                "allele"],
    ),
    Turn(
        label="T3 — coaching : encore un AUTRE (switch #2)",
        user_msg=(
            "Super. Ferme et ouvre un AUTRE exercice BAC SVT, année "
            "différente si possible, sur le même thème génétique."
        ),
        expected_subject="SVT",
        must_contain_in_opened=["gen", "hybrid", "croisement", "allele"],
    ),
    Turn(
        label="T4 — coaching : BUG — génétique DEUX GÈNES LIÉS",
        user_msg=(
            "Maintenant je veux un exercice BAC SVT sur deux GÈNES LIÉS "
            "(linkage, brassage intrachromosomique, test-cross). Ferme "
            "l'exercice actuel et ouvre le nouveau."
        ),
        expected_subject="SVT",
        must_contain_in_opened=["lie", "linkage", "intrachromos",
                                "brassage", "hybrid", "recomb"],
    ),
    Turn(
        label="T5 — coaching : explication au TABLEAU (pas d'exam)",
        user_msg=(
            "OK. Avant, explique-moi au TABLEAU la méthode pour résoudre "
            "un croisement avec deux gènes liés (test-cross, parentaux, "
            "recombinants, distance génétique)."
        ),
        force_exam_panel=False,
        should_open_exam=False,
        expected_subject=None,
    ),
    Turn(
        label="T6 — coaching : BUG — après tableau, ré-ouvrir un examen",
        user_msg=(
            "Merci pour cette explication. Maintenant donne-moi un "
            "exercice BAC SVT sur ce même thème pour m'entraîner."
        ),
        expected_subject="SVT",
        must_contain_in_opened=["gen", "hybrid", "croisement", "brassage"],
    ),
    Turn(
        label="T7 — coaching : verrou matière (doit rester SVT)",
        user_msg=(
            "Parfait. Ferme celui-ci et ouvre-moi un AUTRE exercice BAC — "
            "peu importe le thème — mais reste bien en SVT (surtout pas "
            "de Physique ni Chimie)."
        ),
        expected_subject="SVT",
        must_contain_in_opened=[],  # any SVT topic is fine
    ),
]


# ─────────────────────────────────────────────────────────────────────
async def main():
    settings = get_settings()
    api_key = (getattr(settings, "deepseek_api_key", None)
               or getattr(settings, "DEEPSEEK_API_KEY", None))
    base_url = (getattr(settings, "deepseek_base_url", None)
                or "https://api.deepseek.com/v1")
    if not api_key:
        print("[FATAL] DEEPSEEK_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    exam_bank._ensure_loaded()  # type: ignore
    print(f"[Init] exam_bank loaded: {len(exam_bank._questions)} questions")  # type: ignore

    llm = LLMService()

    conversation_history: list[dict] = []
    current_exam_view = None
    reports: list[TurnReport] = []

    async with httpx.AsyncClient() as client:
        for turn in COACHING_TURNS:
            print(f"\n━━━ {turn.label} ━━━")
            print(f"  USER: {turn.user_msg[:100]}...")

            # Coaching system prompt (SVT, dihybridisme lesson)
            base_prompt = llm.build_system_prompt(
                subject=COACHING_CTX["subject"],
                language="français",
                chapter_title=COACHING_CTX["chapter_title"],
                lesson_title=COACHING_CTX["lesson_title"],
                phase="application",
                objective=COACHING_CTX["objective"],
                scenario_context="Construction d'un savoir-faire BAC",
                student_name="Audit",
                proficiency="intermédiaire",
                user_query=turn.user_msg,
            )
            if current_exam_view:
                base_prompt += "\n\n" + build_exam_view_block(current_exam_view)
                print(f"  [exam-view] {current_exam_view.get('subject')} "
                      f"{current_exam_view.get('year')} "
                      f"{current_exam_view.get('session')}")
            else:
                print("  [exam-view] NONE")

            view_before = dict(current_exam_view) if current_exam_view else None

            response, elapsed = await call_llm(
                client, api_key, base_url, base_prompt,
                conversation_history, turn.user_msg, max_tokens=1800,
            )
            print(f"  LLM: {len(response)} chars in {elapsed:.1f}s")

            sim = simulate_backend_exam_dispatch(
                ai_response=response,
                student_text=turn.user_msg,
                current_exam_view=current_exam_view,
                session_mode="coaching",
                force_exam_panel=turn.force_exam_panel,
            )
            print(f"  SIM path='{sim.path_taken}' action='{sim.panel_action}' "
                  f"subject='{sim.subject_hint}' "
                  f"opened='{sim.opened_exam_label}'")
            for ll in sim.log:
                print(f"       · {ll}")

            prev_id = (view_before or {}).get("exam_id") if view_before else None
            passed, failures, warnings = evaluate(turn, sim, prev_id)
            for f in failures:
                print(f"  ❌ {f}")
            for w in warnings:
                print(f"  ⚠️ {w}")
            if passed:
                print("  ✅ PASS" + (f" (+{len(warnings)} warn)" if warnings else ""))

            conversation_history.append({"role": "user", "content": turn.user_msg})
            conversation_history.append({"role": "assistant", "content": response[:2000]})

            if sim.panel_action == "open" and sim.exercises:
                ex = sim.exercises[0]
                first_q = (ex.get("questions") or [{}])[0]
                current_exam_view = {
                    "exam_id": ex.get("exam_id"),
                    "subject": ex.get("subject"),
                    "year": ex.get("year"),
                    "session": ex.get("session"),
                    "exam_title": ex.get("exam_label"),
                    "exercise_name": ex.get("exercise_name"),
                    "question_number": 1,
                    "question_total": len(ex.get("questions") or []),
                    "question_content": first_q.get("content", ""),
                }
            elif sim.panel_action == "close":
                current_exam_view = None

            view_after = dict(current_exam_view) if current_exam_view else None
            reports.append(TurnReport(
                turn=turn, response=response, elapsed=elapsed, sim=sim,
                current_exam_view_before=view_before,
                current_exam_view_after=view_after,
                passed=passed, failures=failures, warnings=warnings,
            ))

    # ── Build report ────────────────────────────────────────────────
    out: list[str] = []
    out.append("# Test MULTI-TOURS — COACHING — switch exam / genes liés / tableau\n")
    out.append(f"_Généré le {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")
    out.append(
        f"\n**Contexte coaching :** `{COACHING_CTX['subject']}` — "
        f"{COACHING_CTX['chapter_title']} / {COACHING_CTX['lesson_title']}.\n"
    )

    grand_passed = sum(1 for r in reports if r.passed)
    grand_total = len(reports)
    verdict = "🎉 TOUT VERT" if grand_passed == grand_total else (
        f"⚠️ {grand_total - grand_passed} FAIL")
    out.append(f"\n## Score : **{grand_passed}/{grand_total}** — {verdict}\n")

    out.append("\n| # | Tour | Path | Action | Subject ouverte | exam_id | Verdict |")
    out.append("|---|---|---|---|---|---|---|")
    for i, r in enumerate(reports, 1):
        label = r.turn.label[:55]
        verdict_cell = "✅" if r.passed else f"❌ {len(r.failures)}"
        ex_id = ""
        if r.sim.exercises:
            ex_id = (r.sim.exercises[0] or {}).get("exam_id", "")[:40]
        out.append(
            f"| {i} | {label} | `{r.sim.path_taken}` | `{r.sim.panel_action}` | "
            f"`{r.sim.opened_subject or '—'}` | `{ex_id or '—'}` | {verdict_cell} |"
        )

    for i, r in enumerate(reports, 1):
        out.append(f"\n---\n\n## {i}. {r.turn.label}\n")
        out.append(f"**Message utilisateur :**\n> {r.turn.user_msg}\n")
        out.append("**État AVANT ce tour :**")
        out.append("```json")
        out.append(json.dumps(r.current_exam_view_before, ensure_ascii=False, indent=2)
                   if r.current_exam_view_before else "null")
        out.append("```\n")
        out.append(f"**Tag `<exam_exercise>` émis** : "
                   f"`{r.sim.tag_content[:120] or '(aucun)'}`")
        out.append(f"\n**Simulation backend :**")
        out.append(f"- subject_hint = `{r.sim.subject_hint}` "
                   f"(subject_from_user={r.sim.subject_from_user})")
        out.append(f"- path_taken = `{r.sim.path_taken}`")
        out.append(f"- panel_action = `{r.sim.panel_action}`")
        if r.sim.opened_exam_label:
            out.append(f"- examen ouvert = **{r.sim.opened_exam_label}** — "
                       f"_{r.sim.opened_exercise_name}_ "
                       f"(matière : **{r.sim.opened_subject}**)")
        out.append("- log backend :")
        for ll in r.sim.log:
            out.append(f"  - `{ll}`")

        out.append(f"\n**Checks :**")
        if r.passed:
            out.append("- ✅ PASS" + (f" (mais {len(r.warnings)} warning(s))"
                                       if r.warnings else ""))
        else:
            for f in r.failures:
                out.append(f"- ❌ {f}")
        for w in r.warnings:
            out.append(f"- ⚠️ {w}")

        out.append(f"\n**Réponse LLM ({len(r.response)} chars — extrait) :**")
        out.append("```")
        out.append(r.response[:2500] + ("\n…[tronqué]" if len(r.response) > 2500 else ""))
        out.append("```")
        out.append("\n**État APRÈS ce tour :**")
        out.append("```json")
        out.append(json.dumps(r.current_exam_view_after, ensure_ascii=False, indent=2)
                   if r.current_exam_view_after else "null")
        out.append("```")

    out.append(f"\n---\n\n**Score final : {grand_passed}/{grand_total}** — {verdict}\n")

    report = Path(__file__).parent / "test_exam_multiturn_coaching_report.md"
    report.write_text("\n".join(out), encoding="utf-8")
    print(f"\n[TEST] Rapport : {report}")
    print(f"[TEST] Score : {grand_passed}/{grand_total} — {verdict}")


if __name__ == "__main__":
    asyncio.run(main())
