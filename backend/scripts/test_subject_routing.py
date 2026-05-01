"""
Test empirique — ROUTAGE DE LA MATIÈRE pour les demandes d'exercice BAC
dans les modes ``libre`` et ``coaching``.

Bug rapporté par l'utilisateur :
  « Quand je demande un exercice BAC SVT en mode libre/coaching,
    l'AI me donne un exercice de PC. »

Ce test rejoue l'ENSEMBLE de la chaîne de prod :
  1. Construction du system prompt (build_libre_prompt /
     build_system_prompt) — exactement comme en prod.
  2. Appel LLM (DeepSeek) avec une demande d'exercice BAC dans une
     matière précise.
  3. Extraction du tag ``<exam_exercise>...</exam_exercise>`` émis par
     le LLM.
  4. Reproduction EXACTE de la résolution de matière de
     ``session_handler.py`` :
        a) ctx.get("subject")   (avec « Général » → None)
        b) _detect_subject_from_text(exam_query)
        c) _detect_subject_from_text(exam_pre_text)
        d) _infer_subject_from_context(...)
  5. Recherche dans ``exam_bank.search_full_exercises`` avec la matière
     résolue.
  6. Assertion : la matière de l'exercice retourné = matière demandée.

Sortie : scripts/test_subject_routing_report.md
"""
from __future__ import annotations

import asyncio
import json
import re
import sys
import time
import types as _types
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Stub heavy ML deps so we can import LLMService / SessionHandler
# without loading FAISS.
_stub = _types.ModuleType("app.services.rag_service")
class _NoopRag:
    def build_grounded_context(self, *a, **kw): return ""
    def search(self, *a, **kw): return []
def _get_rag_service(): return _NoopRag()
_stub.get_rag_service = _get_rag_service  # type: ignore
sys.modules["app.services.rag_service"] = _stub

from app.config import get_settings  # noqa: E402
from app.services.llm_service import LLMService  # noqa: E402
from app.services.exam_bank_service import exam_bank  # noqa: E402
from app.websockets.session_handler import SessionHandler  # noqa: E402

LLMService._ensure_rag_initialized = lambda self: None  # type: ignore


# ─────────────────────────────────────────────────────────────────────
# Subject resolver — mirror of session_handler.py logic
# ─────────────────────────────────────────────────────────────────────
def _make_handler(session_mode: str, ctx_subject: Optional[str],
                  user_messages: list[str]) -> SessionHandler:
    """Build a fake SessionHandler with the right state to call its
    private subject detection helpers."""
    h = SessionHandler.__new__(SessionHandler)            # bypass __init__
    h.websocket = None                                    # type: ignore
    h.student_id = "test-routing"
    h.session_mode = session_mode
    h.session_context = {
        "subject": ctx_subject or "",
        "lesson_title": "Mode Libre" if session_mode == "libre" else "",
        "chapter_title": "",
    }
    h.conversation_history = [
        {"role": "user", "content": m} for m in user_messages
    ]
    return h


def resolve_subject(handler: SessionHandler, exam_query: str,
                    exam_pre_text: str) -> tuple[Optional[str], list[str]]:
    """Replicate the exact subject-resolution chain from
    ``session_handler._handle_ai_response`` (the <exam_exercise> branch).

    Returns (resolved_subject, trace_steps).
    """
    trace: list[str] = []
    ctx = handler.session_context
    subject_hint = ctx.get("subject", None)
    subject_from_user = False

    trace.append(f"step1: ctx.subject = {subject_hint!r}")

    if subject_hint and subject_hint.lower() in {"général", "general", "mode libre"}:
        subject_hint = None
        trace.append("step1b: neutralised to None (Général)")
    elif subject_hint:
        subject_from_user = True
        trace.append(f"step1c: kept as explicit (subject_from_user=True)")

    if not subject_hint and handler.session_mode in ("libre", "explain"):
        det = handler._detect_subject_from_text(exam_query)
        trace.append(f"step2: _detect_subject_from_text(exam_query={exam_query!r}) = {det}")
        if det:
            subject_hint = det
            subject_from_user = True

    if not subject_hint and handler.session_mode in ("libre", "explain"):
        det = handler._detect_subject_from_text(exam_pre_text)
        trace.append(f"step3: _detect_subject_from_text(pre_text len={len(exam_pre_text)}) = {det}")
        if det:
            subject_hint = det
            subject_from_user = True

    if not subject_hint and handler.session_mode in ("libre", "explain"):
        det = handler._infer_subject_from_context(None)
        trace.append(f"step4: _infer_subject_from_context() = {det}")
        subject_hint = det

    trace.append(f"final: subject_hint={subject_hint} (from_user={subject_from_user})")
    return subject_hint, trace


# ─────────────────────────────────────────────────────────────────────
async def call_llm(client, api_key, base_url, system_prompt, user_msg,
                   max_tokens: int = 1500):
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens,
        "stream": False,
    }
    t0 = time.time()
    try:
        resp = await client.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json=payload, timeout=180.0,
        )
        resp.raise_for_status()
        content = resp.json().get("choices", [{}])[0].get(
            "message", {}).get("content", "")
    except Exception as e:
        content = f"[ERROR: {e}]"
    return content, time.time() - t0


# ─────────────────────────────────────────────────────────────────────
@dataclass
class Scenario:
    name: str
    mode: str                   # "libre" | "coaching"
    ctx_subject: str            # what frontend sends as session subject
    user_msg: str
    expected_subject: str       # "SVT" | "Physique" | "Chimie" | "Mathematiques"
    # Coaching-only fields
    chapter_title: str = ""
    lesson_title: str = ""
    objective: str = ""


SCENARIOS: list[Scenario] = [
    # ─── SVT requests in LIBRE mode ───────────────────────────────
    Scenario(
        name="A1 • LIBRE — exercice BAC en SVT (mitose)",
        mode="libre",
        ctx_subject="Général",
        user_msg=(
            "Donne-moi un exercice BAC en SVT sur la mitose. "
            "Je veux pouvoir m'entraîner sur la division cellulaire."
        ),
        expected_subject="SVT",
    ),
    Scenario(
        name="A2 • LIBRE — exercice BAC SVT (génétique mendelienne)",
        mode="libre",
        ctx_subject="Général",
        user_msg=(
            "Je voudrais un exercice du BAC SVT sur la génétique "
            "mendélienne, croisement dihybride, échiquier."
        ),
        expected_subject="SVT",
    ),
    Scenario(
        name="A3 • LIBRE — exercice BAC SVT (géologie / tectonique)",
        mode="libre",
        ctx_subject="Général",
        user_msg=(
            "Donne-moi un sujet d'examen BAC SVT sur la tectonique des "
            "plaques, subduction, dorsale. Je révise la géologie."
        ),
        expected_subject="SVT",
    ),
    Scenario(
        name="A4 • LIBRE — exercice BAC SVT (consommation matière organique)",
        mode="libre",
        ctx_subject="Général",
        user_msg=(
            "Exercice BAC SVT sur la consommation de la matière "
            "organique : respiration cellulaire, glycolyse, cycle de Krebs."
        ),
        expected_subject="SVT",
    ),
    # ─── Coaching mode SVT ─────────────────────────────────────────
    Scenario(
        name="B1 • COACHING SVT — exercice BAC sur génétique",
        mode="coaching",
        ctx_subject="SVT",
        chapter_title="Génétique humaine — transmission de deux gènes",
        lesson_title="Brassage interchromosomique",
        objective="Maîtriser le dihybridisme et l'échiquier de fécondation",
        user_msg=(
            "Donne-moi un exercice BAC sur la génétique mendélienne, "
            "monohybride ou dihybride, pour m'entraîner."
        ),
        expected_subject="SVT",
    ),
    # ─── Controls : Math + Physique should still route correctly ──
    Scenario(
        name="C1 • LIBRE — exercice BAC Maths (complexes) [contrôle]",
        mode="libre",
        ctx_subject="Général",
        user_msg=(
            "Je veux un exercice BAC en Mathématiques sur les nombres "
            "complexes, module argument, équation."
        ),
        expected_subject="Mathematiques",
    ),
    Scenario(
        name="C2 • LIBRE — exercice BAC Physique (RLC) [contrôle]",
        mode="libre",
        ctx_subject="Général",
        user_msg=(
            "Donne-moi un exercice BAC en Physique sur le circuit RLC, "
            "oscillations électriques."
        ),
        expected_subject="Physique",
    ),
]


# ─────────────────────────────────────────────────────────────────────
def build_system_prompt(llm: LLMService, sc: Scenario) -> str:
    if sc.mode == "libre":
        return llm.build_libre_prompt(
            language="français",
            student_name="Audit",
            proficiency="intermédiaire",
            user_query=sc.user_msg,
        )
    elif sc.mode == "coaching":
        return llm.build_system_prompt(
            subject=sc.ctx_subject,
            language="français",
            chapter_title=sc.chapter_title,
            lesson_title=sc.lesson_title,
            phase="construction",
            objective=sc.objective,
            scenario_context="",
            student_name="Audit",
            proficiency="intermédiaire",
            user_query=sc.user_msg,
        )
    raise ValueError(sc.mode)


def extract_exam_exercise_tag(response: str) -> tuple[str, str]:
    """Return (tag_content, pre_text) — pre_text is the 400 chars before
    the tag, mirroring session_handler line ~3231."""
    m = re.search(r'<exam_exercise>(.*?)</exam_exercise>', response, re.DOTALL)
    if not m:
        return "", ""
    tag_content = m.group(1).strip()
    pre_text = response[:m.start()][-400:]
    return tag_content, pre_text


# ─────────────────────────────────────────────────────────────────────
@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class ScenarioReport:
    scenario: Scenario
    response: str
    elapsed: float
    exam_tag: str
    pre_text: str
    resolved_subject: Optional[str]
    trace: list[str]
    exercises: list[dict]
    checks: list[CheckResult]


def _norm(s: str) -> str:
    """Accent + case insensitive compare."""
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s or "")
                   if unicodedata.category(c) != "Mn").lower()


def _subject_matches(actual: str, expected: str) -> bool:
    """A returned exam subject `actual` matches `expected` if:
      - they are equal accent/case-insensitive, OR
      - expected is one of {Physique, Chimie} and actual is 'Physique-Chimie'
        (the BAC PC bundle), OR
      - actual starts with the first 3 letters of expected
    """
    a = _norm(actual)
    e = _norm(expected)
    if not a or not e:
        return False
    if a == e:
        return True
    # Physique / Chimie / Physique-Chimie are interchangeable for routing
    if e in ("physique", "chimie") and "physique-chimie" in a:
        return True
    if e == "physique-chimie" and a in ("physique", "chimie"):
        return True
    return a.startswith(e[:3])


def run_checks(sc: Scenario, exam_tag: str, resolved: Optional[str],
               exercises: list[dict]) -> list[CheckResult]:
    """The user-reported bug is **routing**: SVT request → PC exercise.
    The single MUST-PASS check is therefore #2 (resolved subject) + #3
    (exam returned in the right subject). Tag emission is informational
    only — production has `force_exam_panel` fallback that handles a
    missing tag by re-detecting the subject from the user's message.
    """
    out: list[CheckResult] = []

    # Informational only — does not count as FAIL
    out.append(CheckResult(
        "ℹ️ Tag <exam_exercise> émis (informationnel — fallback en prod)",
        True,  # never FAIL
        f"contenu : {exam_tag[:80]!r}" if exam_tag
        else "(aucun tag — la prod tombera sur force_exam_panel)"))

    # CORE check #1 : routing resolved correctly
    out.append(CheckResult(
        f"Matière résolue == {sc.expected_subject} (accent-insensitive)",
        _subject_matches(resolved or "", sc.expected_subject),
        f"résolu : {resolved!r}"))

    # CORE check #2 : exam_bank returned an exercise
    out.append(CheckResult(
        "exam_bank a retourné au moins un exercice",
        bool(exercises),
        f"{len(exercises)} exercice(s)"))

    # CORE check #3 (THE big one) : exercise subject matches request
    if exercises:
        first = exercises[0]
        actual_subj = first.get("subject", "")
        out.append(CheckResult(
            f"⭐ L'exercice retourné est en {sc.expected_subject} "
            "(bug original : SVT → PC)",
            _subject_matches(actual_subj, sc.expected_subject),
            f"subject={actual_subj!r}, exam={first.get('exam_label','')!r}, "
            f"topic={first.get('topic','') if first.get('topic') else first.get('exercise_name','')!r}"))
    return out


# ─────────────────────────────────────────────────────────────────────
async def run_scenario(client, api_key, base_url, llm: LLMService,
                       sc: Scenario) -> ScenarioReport:
    print(f"\n[{sc.name}]")
    print(f"  → mode={sc.mode}  ctx.subject={sc.ctx_subject!r}  "
          f"expected={sc.expected_subject}")

    sys_prompt = build_system_prompt(llm, sc)
    response, elapsed = await call_llm(
        client, api_key, base_url, sys_prompt, sc.user_msg, max_tokens=1500,
    )
    print(f"  ← {len(response)} chars en {elapsed:.1f}s")

    exam_tag, pre_text = extract_exam_exercise_tag(response)
    print(f"  tag = {exam_tag[:100]!r}")

    handler = _make_handler(
        session_mode=sc.mode,
        ctx_subject=sc.ctx_subject,
        user_messages=[sc.user_msg],
    )
    if sc.mode == "coaching":
        handler.session_context["chapter_title"] = sc.chapter_title
        handler.session_context["lesson_title"] = sc.lesson_title

    resolved, trace = resolve_subject(handler, exam_tag, pre_text)
    print(f"  resolved subject = {resolved}")

    # Hit exam_bank with the resolved subject
    exercises = []
    try:
        exercises = exam_bank.search_full_exercises(
            query=exam_tag or sc.user_msg,
            subject=resolved,
            count=1,
        )
    except Exception as e:
        print(f"  exam_bank ERROR : {e}")

    if exercises:
        ex = exercises[0]
        print(f"  → exercise subject = {ex.get('subject')!r} "
              f"({ex.get('exam_label','')})")
    else:
        print("  → exam_bank returned 0 exercises")

    checks = run_checks(sc, exam_tag, resolved, exercises)
    return ScenarioReport(
        scenario=sc, response=response, elapsed=elapsed,
        exam_tag=exam_tag, pre_text=pre_text,
        resolved_subject=resolved, trace=trace,
        exercises=exercises, checks=checks,
    )


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

    llm = LLMService()
    reports: list[ScenarioReport] = []
    async with httpx.AsyncClient() as client:
        for sc in SCENARIOS:
            r = await run_scenario(client, api_key, base_url, llm, sc)
            reports.append(r)

    # ── Build report ────────────────────────────────────────────────
    out: list[str] = []
    out.append("# Test — ROUTAGE DE MATIÈRE pour les demandes d'exercice BAC\n")
    out.append(f"_Généré le {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")
    out.append(
        "\nObjectif : confirmer que quand l'utilisateur demande un "
        "exercice BAC dans une matière précise (SVT, Math, Physique…), "
        "l'AI ouvre bien un exercice de cette matière, et pas une autre.\n"
    )

    grand_passed = sum(sum(1 for c in r.checks if c.passed) for r in reports)
    grand_total = sum(len(r.checks) for r in reports)
    full_pass = all(all(c.passed for c in r.checks) for r in reports)
    verdict = "🎉 TOUT VERT" if full_pass else (
        f"⚠️ {grand_total - grand_passed} FAIL")
    out.append(f"\n## Score global : **{grand_passed}/{grand_total}** — {verdict}\n")

    out.append("\n| # | Scénario | Mode | Demandé | Résolu | Match | Verdict |")
    out.append("|---|---|---|---|---|---|---|")
    for i, r in enumerate(reports, 1):
        sc = r.scenario
        ex_subj = r.exercises[0].get("subject", "") if r.exercises else "-"
        match = "✅" if r.exercises and _subject_matches(
            ex_subj, sc.expected_subject) else "❌"
        passed = sum(1 for c in r.checks if c.passed)
        total = len(r.checks)
        v = "✅" if passed == total else f"❌ {total-passed} FAIL"
        out.append(f"| {i} | {sc.name} | `{sc.mode}` | {sc.expected_subject} | "
                   f"{r.resolved_subject or '-'} | {ex_subj} {match} | {passed}/{total} {v} |")

    for i, r in enumerate(reports, 1):
        sc = r.scenario
        out.append(f"\n---\n\n## {i}. {sc.name}\n")
        out.append(f"- **Mode** : `{sc.mode}`")
        out.append(f"- **ctx.subject** : `{sc.ctx_subject}`")
        out.append(f"- **Matière demandée** : **{sc.expected_subject}**")
        if sc.mode == "coaching":
            out.append(f"- **Chapitre** : {sc.chapter_title}")
            out.append(f"- **Leçon** : {sc.lesson_title}")
        out.append(f"- **Temps LLM** : {r.elapsed:.1f}s  •  "
                   f"**Réponse** : {len(r.response)} chars")
        out.append("")
        out.append(f"**Message envoyé :** > {sc.user_msg}\n")

        out.append("### Tag <exam_exercise> émis par le LLM")
        out.append(f"- **Contenu du tag** : `{r.exam_tag or '(vide)'}`")
        if r.pre_text:
            out.append("- **Texte avant le tag (400 derniers chars)** :")
            out.append(f"  > {r.pre_text[-300:].strip()}")

        out.append("\n### Résolution de matière (trace)")
        for s in r.trace:
            out.append(f"- {s}")
        out.append(f"- **➡ Matière finale : {r.resolved_subject!r}**")

        out.append("\n### Exercice retourné par exam_bank")
        if r.exercises:
            ex = r.exercises[0]
            out.append(f"- **subject** : `{ex.get('subject','')}`")
            out.append(f"- **exam_label** : {ex.get('exam_label','')}")
            out.append(f"- **exercise_name** : {ex.get('exercise_name','')}")
            topic = ex.get("topic", "")
            if topic:
                out.append(f"- **topic** : {topic}")
            qcount = len(ex.get("questions", []))
            out.append(f"- **# questions** : {qcount}")
        else:
            out.append("- _(aucun exercice retourné)_")

        out.append("\n### Checks")
        out.append("| # | Vérification | Statut | Détail |")
        out.append("|---|---|---|---|")
        for j, c in enumerate(r.checks, 1):
            flag = "✅ PASS" if c.passed else "❌ FAIL"
            out.append(f"| {j} | {c.name} | {flag} | {c.detail} |")

        # Show end of LLM response for debugging
        out.append(f"\n### Réponse LLM ({len(r.response)} chars — extrait)")
        out.append("```")
        out.append(r.response[:3000] + ("\n…[tronqué]"
                   if len(r.response) > 3000 else ""))
        out.append("```")

    out.append(f"\n---\n\n**Score final : {grand_passed}/{grand_total}** — {verdict}\n")

    report = Path(__file__).parent / "test_subject_routing_report.md"
    report.write_text("\n".join(out), encoding="utf-8")
    print(f"\n[TEST] Rapport : {report}")
    print(f"[TEST] Score global : {grand_passed}/{grand_total} — {verdict}")


if __name__ == "__main__":
    asyncio.run(main())
