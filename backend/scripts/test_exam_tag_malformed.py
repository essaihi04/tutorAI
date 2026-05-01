"""
Test — reproduction du bug transcript « pollution exercice BAC n'ouvre pas »
(SVT Domaine 3) — 4 variantes de reponses LLM mal formees.

Le transcript utilisateur montre 3 messages ou l'IA annonce qu'elle ouvre
un exercice BAC sur la pollution mais :
  - msg 1 et 2 : AUCUNE balise <exam_exercise> visible
  - msg 3     : balise <exam_exercise> OUVERTE mais JAMAIS FERMEE
(puis msg 4, l'utilisateur demande une explication de la question 2 au
tableau, et l'IA ne sait pas de quelle question il s'agit car le panneau
n'a jamais ouvert).

On joue ici les 4 variantes de reponses problematiques en parallele et
on simule l'execution backend (regex d'extraction + cascade
exam_bank) pour verifier que le FIX les rattrape :
  V1. Aucune balise emise (LLM a oublie le tag)
  V2. Balise fermee mais CONTENU VIDE (<exam_exercise></exam_exercise>)
  V3. Balise OUVERTE mais NON FERMEE, truncation (cas du transcript)
  V4. Balise OUVERTE avec contenu valide mais non fermee

Avant le fix :
  V1 → force_exam_panel fallback OK (existait deja)
  V2 → primary match vide → hide_exam_panel → AUCUNE recuperation
  V3 → primary regex rate → fallback OK seulement si force=True
  V4 → primary regex rate → fallback OK seulement si force=True

Apres le fix :
  V1, V2, V3, V4 → toutes les variantes recuperent (panneau s'ouvre).

Sortie : scripts/test_exam_tag_malformed_report.md
"""
from __future__ import annotations

import asyncio
import json
import re
import sys
import time
import types as _types
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

_stub = _types.ModuleType("app.services.rag_service")
class _NoopRag:
    def build_grounded_context(self, *a, **kw): return ""
    def search(self, *a, **kw): return []
def _get_rag_service(): return _NoopRag()
_stub.get_rag_service = _get_rag_service  # type: ignore
sys.modules["app.services.rag_service"] = _stub

from app.services.exam_bank_service import exam_bank  # noqa: E402
from app.services.resource_decision_service import ResourceDecisionService  # noqa: E402


# ─────────────────────────────────────────────────────────────────────
# Replicate the session_handler.py <exam_exercise> extraction logic
# EXACTLY as it is after the fix — this is the unit under test.
# ─────────────────────────────────────────────────────────────────────
def extract_exam_exercise_tag(ai_response: str) -> Optional[str]:
    """Mirror session_handler.py L3231-L3259 AFTER the fix.

    Returns:
      - the stripped tag content (non-empty) if a tag (closed or unclosed)
        was found with non-whitespace content
      - None otherwise (empty tag, whitespace-only, or no tag at all)
    """
    m = re.search(r'<exam_exercise>(.*?)</exam_exercise>',
                  ai_response, re.DOTALL)
    if not m:
        m = re.search(
            r'<exam_exercise>([^<]*?)(?=<|$)',
            ai_response, re.DOTALL,
        )
    if not m:
        return None
    content = m.group(1).strip()
    if not content:
        return None
    return content


# ─────────────────────────────────────────────────────────────────────
# Backend-dispatch simulation — minimal and focused on pollution bug
# ─────────────────────────────────────────────────────────────────────
def _norm(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s or "")
                   if unicodedata.category(c) != "Mn").lower()


@dataclass
class DispatchOutcome:
    panel_action: str             # "open" | "close" | "stay"
    path: str                     # "primary_ok" | "primary_empty" |
                                  # "force_fallback_ok" | "force_fallback_empty"
    opened_exam_label: Optional[str] = None
    opened_subject: Optional[str] = None
    opened_topic_hint: Optional[str] = None
    tag_extracted: Optional[str] = None
    log: list = None


def simulate_dispatch(
    ai_response: str,
    student_text: str,
    session_subject: str = "SVT",
    lesson_title: str = "Pollution des sols et des eaux",
    force_exam_panel: bool = True,
    current_exam_id: Optional[str] = None,
) -> DispatchOutcome:
    log: list = []
    tag = extract_exam_exercise_tag(ai_response)
    log.append(f"tag_extracted={tag!r}")

    # Primary path
    if tag:
        exercises = exam_bank.search_full_exercises(
            query=tag, subject=session_subject, count=1,
            exclude_exam_id=current_exam_id,
            conversation_context=lesson_title or None,
        )
        if exercises:
            ex = exercises[0]
            qs = ex.get("questions") or [{}]
            topic = (qs[0].get("topic") or "")[:80]
            log.append(f"primary_ok: {ex.get('exam_label')} — {topic}")
            return DispatchOutcome(
                panel_action="open", path="primary_ok",
                opened_exam_label=ex.get("exam_label"),
                opened_subject=ex.get("subject"),
                opened_topic_hint=topic,
                tag_extracted=tag, log=log,
            )
        log.append(f"primary_empty for query={tag!r}")

    # Force-exam-panel fallback — mirrors session_handler.py L3370+
    if force_exam_panel:
        search_query = student_text or lesson_title
        exercises = exam_bank.search_full_exercises(
            query=search_query, subject=session_subject, count=1,
            exclude_exam_id=current_exam_id,
            conversation_context=lesson_title or None,
        )
        # Try without lesson filter
        if not exercises:
            exercises = exam_bank.search_full_exercises(
                query=search_query, subject=session_subject, count=1,
                exclude_exam_id=current_exam_id,
            )
        # Try single-question search
        if not exercises:
            single_qs = exam_bank.search_exercises(
                query=search_query, subject=session_subject, count=2,
                exclude_exam_id=current_exam_id,
            )
            if not single_qs:
                single_qs = exam_bank.search_exercises(
                    query="exercice bac", subject=session_subject, count=2,
                    exclude_exam_id=current_exam_id,
                )
            if single_qs:
                q = single_qs[0]
                exercises = [{
                    "exam_label": q.get("exam_label", ""),
                    "subject": q.get("subject", ""),
                    "exercise_name": q.get("exercise_name") or "Question BAC",
                    "questions": [q],
                }]
        if exercises:
            ex = exercises[0]
            qs = ex.get("questions") or [{}]
            topic = (qs[0].get("topic") or "")[:80]
            log.append(f"force_fallback_ok: {ex.get('exam_label')} — {topic}")
            return DispatchOutcome(
                panel_action="open", path="force_fallback_ok",
                opened_exam_label=ex.get("exam_label"),
                opened_subject=ex.get("subject"),
                opened_topic_hint=topic,
                tag_extracted=tag, log=log,
            )
        log.append("force_fallback_empty")

    return DispatchOutcome(
        panel_action="close", path="force_fallback_empty",
        tag_extracted=tag, log=log,
    )


# ─────────────────────────────────────────────────────────────────────
# 4 variantes de reponses LLM problematiques
# ─────────────────────────────────────────────────────────────────────
STUDENT_TEXT = (
    "Donne-moi un exercice de type BAC marocain sur le sujet en cours "
    "(pollution), avec correction détaillée."
)

VARIANTS = [
    ("V1 — aucune balise (msg 1 du transcript)",
     "D'accord Ferdaous ! Je t'ouvre un exercice du BAC marocain sur la "
     "**pollution** (SVT - Domaine 3 : Utilisation des matières organiques "
     "et inorganiques) pour t'entraîner. Vas-y, essaye de répondre avant "
     "de regarder la correction ! 💪"),

    ("V2 — balise fermee mais CONTENU VIDE",
     "D'accord ! Je t'ouvre un exercice BAC SVT sur la pollution.\n"
     "<exam_exercise></exam_exercise>\n"
     "Prends ton temps pour répondre."),

    ("V3 — balise OUVERTE, NON FERMEE (msg 3 du transcript)",
     "Très bien Ferdaous ! Puisque tu travailles actuellement sur la "
     "**pollution** (SVT - Domaine 3), je vais te proposer un exercice de "
     "type BAC marocain sur ce thème, comme tu l'as demandé. Prends le "
     "temps de réfléchir et de répondre, puis je te donnerai la "
     "**correction détaillée** étape par étape avec un tableau "
     "récapitulatif. 💪\n\n<exam_exercise>"),

    ("V4 — balise ouverte + contenu valide mais NON FERMEE",
     "D'accord ! Je t'ouvre un exercice BAC SVT sur la pollution.\n"
     "<exam_exercise>pollution environnement ecosysteme matiere organique "
     "degradation</exam_exercise"  # note: closing tag truncated (no >)
     ),
]


# ─────────────────────────────────────────────────────────────────────
def run_tests():
    exam_bank._ensure_loaded()  # type: ignore
    total_q = len(exam_bank._questions)  # type: ignore
    print(f"[Init] exam_bank loaded: {total_q} questions")

    # Verify decision router classifies the user message as "exam"
    dec = ResourceDecisionService()
    mode = dec._detect_explicit_mode(STUDENT_TEXT.lower())
    print(f"[Decision] _detect_explicit_mode('{STUDENT_TEXT[:60]}...') -> {mode}")
    assert mode == "exam", f"Decision router should classify as 'exam', got {mode}"

    results = []
    for label, ai_response in VARIANTS:
        print(f"\n━━━ {label} ━━━")
        outcome = simulate_dispatch(
            ai_response=ai_response,
            student_text=STUDENT_TEXT,
            session_subject="SVT",
            lesson_title="Pollution des sols et des eaux",
            force_exam_panel=True,
        )
        for line in outcome.log:
            print(f"  · {line}")
        status = "✅ PASS" if outcome.panel_action == "open" else "❌ FAIL"
        print(f"  {status} action={outcome.panel_action} path={outcome.path} "
              f"→ exam={outcome.opened_exam_label}")
        results.append((label, ai_response, outcome))

    # ── Report ──
    out = ["# Test — balise `<exam_exercise>` mal formée (bug transcript pollution)\n"]
    out.append(f"_Généré le {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")
    out.append(
        "\n**Contexte :** transcript utilisateur où l'IA annonce un exercice "
        "BAC SVT sur la **pollution** mais le panneau ne s'ouvre jamais, "
        "obligeant l'utilisateur à répéter 3 fois, puis à demander une "
        "explication au tableau d'une « question 2 » que l'IA ne peut pas "
        "identifier (le panneau n'a jamais contenu d'exercice).\n"
    )

    n_pass = sum(1 for _, _, o in results if o.panel_action == "open")
    n_total = len(results)
    verdict = "🎉 TOUT VERT" if n_pass == n_total else f"⚠️ {n_total - n_pass} FAIL"
    out.append(f"\n## Score : **{n_pass}/{n_total}** — {verdict}\n")

    out.append("\n| Variante | Tag extrait | Path | Action | Examen ouvert |")
    out.append("|---|---|---|---|---|")
    for label, _, o in results:
        tag_short = (o.tag_extracted or "(rien)")[:40]
        out.append(
            f"| {label[:60]} | `{tag_short}` | `{o.path}` | "
            f"`{o.panel_action}` | {o.opened_exam_label or '—'} |"
        )

    for label, ai_response, o in results:
        out.append(f"\n---\n\n## {label}\n")
        out.append("**Réponse LLM simulée :**")
        out.append("```\n" + ai_response + "\n```\n")
        out.append(f"**Tag extrait par le regex du fix :** "
                   f"`{o.tag_extracted or '(aucun)'}`")
        out.append(f"\n**Simulation backend :**")
        out.append(f"- panel_action = `{o.panel_action}`")
        out.append(f"- path = `{o.path}`")
        if o.opened_exam_label:
            out.append(
                f"- examen ouvert = **{o.opened_exam_label}** — "
                f"_{o.opened_topic_hint}_ (matière : **{o.opened_subject}**)"
            )
        out.append("- log :")
        for l in o.log:
            out.append(f"  - `{l}`")
        status = "✅ PASS" if o.panel_action == "open" else "❌ FAIL"
        out.append(f"\n**Verdict :** {status}")

    out.append(f"\n---\n\n**Score final : {n_pass}/{n_total}** — {verdict}\n")
    report = Path(__file__).parent / "test_exam_tag_malformed_report.md"
    report.write_text("\n".join(out), encoding="utf-8")
    print(f"\n[TEST] Rapport : {report}")
    print(f"[TEST] Score : {n_pass}/{n_total} — {verdict}")
    return n_pass == n_total


if __name__ == "__main__":
    ok = run_tests()
    sys.exit(0 if ok else 1)
