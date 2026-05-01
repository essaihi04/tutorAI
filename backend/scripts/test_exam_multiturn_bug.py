"""
Test MULTI-TOURS — reproduction du bug rapporte par l'utilisateur :

  « Il ferme et ouvre les exercices BAC 3 fois, mais quand je demande un
    exercice BAC sur la genetique de DEUX GENES LIES, rien ne se ferme
    ni ne s'ouvre. Apres plusieurs tentatives il m'ouvre un autre examen,
    et quand je demande le tableau puis un autre examen, il n'arrive pas
    a ouvrir un autre examen et parfois ouvre un examen d'une autre
    matiere. »

Le test joue 7 tours contre le VRAI LLM (DeepSeek) et SIMULE le
backend entre chaque tour :

  1. Construit le system prompt prod (libre + exam-view block si un
     examen est "ouvert").
  2. Envoie le message utilisateur au LLM avec l'historique complet.
  3. Extrait le tag <exam_exercise> emis + les <ui> show_board.
  4. Simule le backend en appelant le VRAI exam_bank.search_full_exercises
     (avec le meme cascading retry que session_handler.py), ce qui dit
     si le panneau s'ouvrirait reellement en prod, resterait bloque, ou
     ouvrirait un exercice d'une autre matiere.
  5. Met a jour current_exam_view et conversation_history pour le tour
     suivant — EXACTEMENT comme le ferait le backend en prod.

Scenarios joues en une SEULE conversation :
  T1. Ouvrir un premier exercice BAC SVT sur la mitose.
  T2. « Un autre exercice BAC SVT » (switch facile).
  T3. « Encore un autre » (switch facile, 2e fois).
  T4. « Un autre exercice BAC SVT sur la genetique avec DEUX GENES LIES »
      ← bug rapporte : rien ne s'ouvre.
  T5. (retry user) « Alors donne-moi un autre exercice BAC, peu importe »
      ← bug rapporte : ouvre parfois une autre matiere.
  T6. « Explique-moi au tableau la methode des deux genes lies. »
  T7. « Maintenant donne-moi un exercice BAC sur ce theme. »
      ← bug rapporte : apres le tableau, ne s'ouvre plus.

Sortie : scripts/test_exam_multiturn_bug_report.md
"""
from __future__ import annotations

import asyncio
import json
import re
import sys
import time
import types as _types
import unicodedata
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

# Stub heavy ML deps so we can import LLMService without FAISS.
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

LLMService._ensure_rag_initialized = lambda self: None  # type: ignore


# ─────────────────────────────────────────────────────────────────────
# Subject detection — simplified mirror of session_handler._detect_subject_from_text
# ─────────────────────────────────────────────────────────────────────
def _norm(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s or "")
                   if unicodedata.category(c) != "Mn").lower()


SUBJECT_KW = {
    "SVT": [
        "svt", "biologie", "geologie", "genetique", "gene", "allele",
        "adn", "arn", "proteine", "mitose", "meiose", "chromosome",
        "dihybrid", "monohybrid", "brassage", "echiquier", "gamete",
        "phenotype", "genotype", "mendel", "morgan", "drosophile",
        "cellule", "tissu", "immun", "muscle", "glycolyse", "krebs",
        "tectonique", "subduction", "faille", "magma",
    ],
    "Physique": [
        "physique", "mecanique", "electricite", "rlc", "condensateur",
        "bobine", "onde", "frequence", "radioactivite", "nucleaire",
        "cinematique", "dynamique", "gravite",
    ],
    "Chimie": [
        "chimie", "ph", "acide", "base", "solution", "oxydoreduction",
        "esterification", "cinetique chimique", "dosage", "molaire",
        "equilibre chimique",
    ],
    "Mathématiques": [
        "mathematique", "math", "maths", "fonction", "derivee",
        "integrale", "limite", "probabilite", "statistique", "geometrie",
        "suite", "logarithme", "exponentiel", "trigonometrie",
    ],
}


def detect_subject_from_text(text: str) -> Optional[str]:
    """Scored keyword match — whichever subject has the most hits wins."""
    if not text:
        return None
    t = " " + _norm(text) + " "
    best = None
    best_score = 0
    for subj, kws in SUBJECT_KW.items():
        score = sum(1 for kw in kws if f" {kw}" in t or f"{kw} " in t
                    or f"-{kw}" in t or f"{kw}-" in t)
        if score > best_score:
            best = subj
            best_score = score
    return best


# ─────────────────────────────────────────────────────────────────────
# Simulate session_handler exam dispatch exactly
# ─────────────────────────────────────────────────────────────────────
@dataclass
class BackendSimResult:
    """Mirror of what the session_handler would actually do."""
    tag_content: str                 # raw <exam_exercise> tag content
    subject_hint: Optional[str]      # detected subject
    subject_from_user: bool          # whether we trust it enough to NOT cross-load
    path_taken: str                  # "primary_ok" / "primary_empty_hide" / "primary_fallback_ok" / "force_fallback" / "no_tag" / etc.
    exercises: list                  # final exercises returned (what goes to frontend)
    panel_action: str                # "open" | "close" | "stay" | "wrong_subject"
    opened_subject: Optional[str]    # subject of the opened exercise (to detect wrong-subject bug)
    opened_exam_label: Optional[str] # label of the opened exam
    opened_exercise_name: Optional[str]
    log: list[str] = field(default_factory=list)


def _summarize_exercise(ex: dict) -> str:
    """Produce a short human-readable topic summary for an exercise: its
    name + the topic/keywords of its first question (the exercise_name is
    usually just 'Exercice 3' — useless on its own)."""
    name = ex.get("exercise_name") or "Exercice"
    qs = ex.get("questions") or []
    topic_bits: list[str] = []
    if qs:
        q0 = qs[0]
        topic = q0.get("topic") or ""
        if topic:
            topic_bits.append(topic)
        kws = q0.get("keywords") or []
        if kws:
            topic_bits.append(", ".join(str(k) for k in kws[:6]))
        # Also stuff the first 120 chars of the content
        content = (q0.get("content") or "")[:120]
        if content:
            topic_bits.append(content)
    return name + (" | " + " · ".join(topic_bits) if topic_bits else "")


def simulate_backend_exam_dispatch(
    ai_response: str,
    student_text: str,
    current_exam_view: Optional[dict],
    session_mode: str = "libre",
    force_exam_panel: bool = False,
) -> BackendSimResult:
    """Reproduce session_handler.py L3231-L3460 logic with the real exam_bank."""
    log: list[str] = []

    # Extract the LAST <exam_exercise> tag (the one that would be processed)
    matches = re.findall(r'<exam_exercise>(.*?)</exam_exercise>',
                         ai_response, re.DOTALL)
    tag_content = matches[-1].strip() if matches else ""

    has_ui_show_board = bool(re.search(r'<ui>\s*\{.*?show_board', ai_response,
                                       re.DOTALL))
    if has_ui_show_board:
        log.append("AI emitted <ui> show_board (whiteboard)")

    # ── Primary path: LLM emitted a <exam_exercise> tag ──
    if tag_content:
        exam_query = tag_content
        log.append(f"primary: tag='{exam_query[:80]}'")

        # Subject detection — same order as backend
        subject_hint = None
        subject_from_user = False

        # Try tag content
        subject_hint = detect_subject_from_text(exam_query)
        if subject_hint:
            subject_from_user = True
            log.append(f"subject from tag -> {subject_hint}")

        # Fallback: announcement text right before the tag (last 400 chars)
        if not subject_hint:
            m = re.search(r'<exam_exercise>', ai_response)
            pre = ai_response[:m.start()][-400:] if m else ""
            subject_hint = detect_subject_from_text(pre)
            if subject_hint:
                subject_from_user = True
                log.append(f"subject from pre_text -> {subject_hint}")

        # Fallback: user message (simulates _infer_subject_from_context via
        # student text scan — this is best-effort in the test)
        if not subject_hint:
            subject_hint = detect_subject_from_text(student_text)
            if subject_hint:
                subject_from_user = True
                log.append(f"subject from student_text -> {subject_hint}")

        # If still nothing — assume current exam subject (weak signal)
        if not subject_hint and current_exam_view:
            subject_hint = current_exam_view.get("subject")
            log.append(f"subject from current_exam_view -> {subject_hint}")

        open_exam_id = None
        if current_exam_view:
            open_exam_id = current_exam_view.get("exam_id") or None
        exercises = exam_bank.search_full_exercises(
            query=exam_query, subject=subject_hint, count=1,
            exclude_exam_id=open_exam_id,
        )
        # Last-resort: drop exclude_exam_id if we get nothing
        if not exercises and open_exam_id:
            log.append(f"primary_retry: dropping exclude_exam_id='{open_exam_id}'")
            exercises = exam_bank.search_full_exercises(
                query=exam_query, subject=subject_hint, count=1,
            )
        if exercises:
            log.append(f"primary_ok: {len(exercises)} ex found")
            ex = exercises[0]
            return BackendSimResult(
                tag_content=tag_content, subject_hint=subject_hint,
                subject_from_user=subject_from_user,
                path_taken="primary_ok",
                exercises=exercises, panel_action="open",
                opened_subject=ex.get("subject"),
                opened_exam_label=ex.get("exam_label"),
                opened_exercise_name=_summarize_exercise(ex),
                log=log,
            )

        # Primary: retry WITHOUT subject ONLY when subject was not user-asked
        if subject_hint and not subject_from_user:
            log.append("primary_empty: retrying without subject filter")
            exercises = exam_bank.search_full_exercises(
                query=exam_query, subject=None, count=1,
            )
            if exercises:
                ex = exercises[0]
                return BackendSimResult(
                    tag_content=tag_content, subject_hint=subject_hint,
                    subject_from_user=False,
                    path_taken="primary_fallback_ok_no_subject",
                    exercises=exercises, panel_action="open",
                    opened_subject=ex.get("subject"),
                    opened_exam_label=ex.get("exam_label"),
                    opened_exercise_name=_summarize_exercise(ex),
                    log=log,
                )

        # Primary failed — backend sends hide_exam_panel
        log.append(
            f"primary_empty_hide: subject_from_user={subject_from_user}, "
            "backend would send hide_exam_panel (no fallback triggered)"
            if not force_exam_panel else
            f"primary_empty: trying force_exam_panel fallback"
        )
        if not force_exam_panel:
            return BackendSimResult(
                tag_content=tag_content, subject_hint=subject_hint,
                subject_from_user=subject_from_user,
                path_taken="primary_empty_hide",
                exercises=[], panel_action="close",
                opened_subject=None, opened_exam_label=None,
                opened_exercise_name=None, log=log,
            )

    # ── Force fallback path (primary_mode==exam OR no tag emitted) ──
    if force_exam_panel:
        search_query = student_text
        subject_hint = detect_subject_from_text(search_query)
        subject_from_user = bool(subject_hint)
        if not subject_hint:
            subject_hint = detect_subject_from_text(ai_response[-600:])
            if subject_hint:
                subject_from_user = True
        if not subject_hint and current_exam_view:
            subject_hint = current_exam_view.get("subject")
        log.append(
            f"force_fallback: query='{search_query[:60]}' subject='{subject_hint}' "
            f"subject_from_user={subject_from_user}"
        )

        open_exam_id_fb = None
        if current_exam_view:
            open_exam_id_fb = current_exam_view.get("exam_id") or None
        # Cascade level 1: search_full + subject + exclude_exam_id
        exercises = exam_bank.search_full_exercises(
            query=search_query, subject=subject_hint, count=1,
            exclude_exam_id=open_exam_id_fb,
        )
        # Level 3: single-question + subject
        single_qs = []
        if not exercises and subject_hint:
            single_qs = exam_bank.search_exercises(
                query=search_query, subject=subject_hint, count=2,
            )
            if not single_qs:
                single_qs = exam_bank.search_exercises(
                    query="exercice bac", subject=subject_hint, count=2,
                )
        # Level 5: drop subject (only if !subject_from_user)
        if not exercises and not single_qs and not subject_from_user:
            log.append("force_fallback: dropping subject filter")
            exercises = exam_bank.search_full_exercises(
                query=search_query, subject=None, count=1,
            )
            if not exercises:
                single_qs = exam_bank.search_exercises(
                    query=search_query or "exercice bac", subject=None, count=2,
                )
        elif not exercises and not single_qs and subject_from_user:
            log.append(
                f"force_fallback: 0 for subject='{subject_hint}' but "
                "subject_from_user=True — NOT cross-loading another subject"
            )

        if not exercises and single_qs:
            exercises = [{
                "exam_id": q.get("exam_id", ""),
                "exam_label": q.get("exam_label", ""),
                "subject": q.get("subject", ""),
                "exercise_name": q.get("exercise_name") or q.get("part_name") or "Question BAC",
                "questions": [q],
            } for q in single_qs[:1]]

        if exercises:
            ex = exercises[0]
            log.append(f"force_fallback_ok: {ex.get('exam_label')}")
            return BackendSimResult(
                tag_content=tag_content, subject_hint=subject_hint,
                subject_from_user=subject_from_user,
                path_taken="force_fallback_ok",
                exercises=exercises, panel_action="open",
                opened_subject=ex.get("subject"),
                opened_exam_label=ex.get("exam_label"),
                opened_exercise_name=_summarize_exercise(ex),
                log=log,
            )
        log.append("force_fallback_empty: panel stays / hides")
        return BackendSimResult(
            tag_content=tag_content, subject_hint=subject_hint,
            subject_from_user=subject_from_user,
            path_taken="force_fallback_empty",
            exercises=[], panel_action="close",
            opened_subject=None, opened_exam_label=None,
            opened_exercise_name=None, log=log,
        )

    # ── No tag and no force → panel untouched ──
    log.append("no_tag_no_force: panel stays as-is")
    return BackendSimResult(
        tag_content="", subject_hint=None, subject_from_user=False,
        path_taken="no_action",
        exercises=[], panel_action="stay",
        opened_subject=None, opened_exam_label=None,
        opened_exercise_name=None, log=log,
    )


# ─────────────────────────────────────────────────────────────────────
# Prompt building — mirrors session_handler for exam-view block
# ─────────────────────────────────────────────────────────────────────
def build_exam_view_block(v: dict) -> str:
    subject = str(v.get("subject", "") or "").strip()
    year = str(v.get("year", "") or "").strip()
    session = str(v.get("session", "") or "").strip()
    exam_title = str(v.get("exam_title", "") or "").strip()
    exercise_name = str(v.get("exercise_name", "") or "").strip()
    q_num = v.get("question_number")
    q_total = v.get("question_total")
    q_content = str(v.get("question_content", "") or "").strip()

    session_label = session.capitalize() if session else ""
    header = " — ".join([b for b in [subject, session_label, year] if b]) or exam_title or "Examen"

    block = f"""
[CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ À L'ÉTUDIANT]
⚠️ L'étudiant a CE PANNEAU D'EXAMEN ouvert en ce moment. Tu DOIS te baser EXCLUSIVEMENT sur ces informations. NE JAMAIS inventer une autre année, session, exercice ou question.

📚 Examen : {header}
📖 {exercise_name}
❓ Question {q_num}/{q_total}

ÉNONCÉ EXACT DE LA QUESTION AFFICHÉE :
{q_content or '(non disponible)'}

RÈGLES STRICTES :
- Si l'étudiant parle de "cette question", "la question N°X", "l'exercice", "l'examen", il parle TOUJOURS de CE qui est affiché ci-dessus.
- Tu cites l'année et la session EXACTES indiquées ci-dessus. JAMAIS d'autres.
- Tu ne mentionnes JAMAIS un examen/année différent à moins que l'étudiant ne te le demande explicitement.

🔄 BASCULE VERS UN AUTRE EXERCICE BAC :
- Si l'étudiant demande explicitement « un AUTRE exercice », « un nouvel exercice », « ferme et ouvre », « différent », « autre année », « autre session » (même thème ou thème différent), tu DOIS :
  1. Émettre IMMÉDIATEMENT un nouveau `<exam_exercise>mots-clés du thème demandé</exam_exercise>` afin que le SYSTÈME charge un VRAI exercice depuis la banque officielle BAC.
  2. NE PAS fabriquer un faux énoncé d'examen sur le tableau (`<ui>` whiteboard).
  3. NE PAS citer une année/session précise dans ta phrase d'introduction.
  4. Annonce simplement : « D'accord, je t'ouvre un autre exercice BAC sur [thème] » puis émets le tag.
- Si l'étudiant veut continuer sur l'exercice actuel, reste sur celui affiché ci-dessus.
"""
    return block


# ─────────────────────────────────────────────────────────────────────
# LLM call
# ─────────────────────────────────────────────────────────────────────
async def call_llm(client, api_key, base_url, system_prompt, history, user_msg,
                   max_tokens: int = 1800):
    messages = [{"role": "system", "content": system_prompt}] + history + [
        {"role": "user", "content": user_msg}
    ]
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
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
# Scenario turns
# ─────────────────────────────────────────────────────────────────────
@dataclass
class Turn:
    label: str
    user_msg: str
    force_exam_panel: bool = True   # treat BAC requests as exam primary_mode
    # Expectations
    should_open_exam: bool = True
    expected_subject: Optional[str] = "SVT"
    # Optional: keyword that must appear in the opened exercise topic
    must_contain_in_opened: list[str] = field(default_factory=list)


TURNS: list[Turn] = [
    Turn(
        label="T1 — ouvrir un premier exercice BAC SVT (mitose)",
        user_msg=(
            "Salut ! Je suis en 2BAC SVT BIOF. Peux-tu m'ouvrir un exercice "
            "BAC SVT sur la mitose ou la division cellulaire pour m'entraîner ?"
        ),
        expected_subject="SVT",
        must_contain_in_opened=["mitose", "cellulaire", "cellule", "chromosome"],
    ),
    Turn(
        label="T2 — un autre exercice BAC SVT (switch facile #1)",
        user_msg=(
            "Super ! Maintenant ferme celui-ci et donne-moi un AUTRE exercice "
            "BAC SVT sur la génétique mendélienne (monohybridisme ou dihybridisme)."
        ),
        expected_subject="SVT",
        must_contain_in_opened=["gen", "mendel", "hybrid", "croisement",
                                "echiquier", "allele"],
    ),
    Turn(
        label="T3 — encore un autre BAC SVT (switch facile #2)",
        user_msg=(
            "Merci. Ferme et ouvre-moi un AUTRE exercice BAC SVT, par "
            "exemple sur les chaînes de transmission génétique ou l'ADN."
        ),
        expected_subject="SVT",
        must_contain_in_opened=["gen", "adn", "allele", "chromosome",
                                "proteine", "mutation", "hybrid"],
    ),
    Turn(
        label="T4 — BUG RAPPORTÉ : génétique DEUX GÈNES LIÉS",
        user_msg=(
            "Parfait. Maintenant je veux un autre exercice BAC SVT sur la "
            "génétique avec DEUX GÈNES LIÉS (linkage / gènes liés sur le "
            "même chromosome, brassage intrachromosomique). Ferme celui-ci "
            "et ouvre le nouveau."
        ),
        expected_subject="SVT",
        must_contain_in_opened=["lie", "linkage", "intrachromos",
                                "brassage", "hybrid", "recomb"],
    ),
    Turn(
        label="T5 — BUG RAPPORTÉ : retry → ouvre n'importe quoi",
        user_msg=(
            "Ça n'a pas marché. Donne-moi alors un autre exercice BAC SVT, "
            "peu importe le thème tant que c'est SVT."
        ),
        expected_subject="SVT",
        must_contain_in_opened=[],
    ),
    Turn(
        label="T6 — demande tableau (whiteboard)",
        user_msg=(
            "OK. Explique-moi plutôt au TABLEAU la méthode pour résoudre "
            "un croisement avec deux gènes LIÉS : test-cross, recombinants, "
            "parentaux, carte génétique."
        ),
        force_exam_panel=False,
        should_open_exam=False,
        expected_subject=None,
    ),
    Turn(
        label="T7 — BUG RAPPORTÉ : après tableau, ré-ouvrir un examen",
        user_msg=(
            "Merci pour l'explication. Maintenant donne-moi un exercice BAC "
            "SVT sur ce même thème (génétique, gènes liés ou brassage) pour "
            "que je m'entraîne."
        ),
        expected_subject="SVT",
        must_contain_in_opened=["gen", "hybrid", "croisement", "brassage"],
    ),
]


# ─────────────────────────────────────────────────────────────────────
# Main run
# ─────────────────────────────────────────────────────────────────────
@dataclass
class TurnReport:
    turn: Turn
    response: str
    elapsed: float
    sim: BackendSimResult
    current_exam_view_before: Optional[dict]
    current_exam_view_after: Optional[dict]
    passed: bool
    failures: list[str]
    warnings: list[str] = field(default_factory=list)


def evaluate(turn: Turn, sim: BackendSimResult,
             previous_exam_id: Optional[str]) -> tuple[bool, list[str], list[str]]:
    """Return (passed, hard_failures, soft_warnings).

    HARD failures (real bugs):
      - Requested an exam but panel did NOT open
      - Opened a DIFFERENT subject than requested
      - Asked for ANOTHER exercise but got the SAME exam_id as before
      - Asked NOT to open an exam but one opened anyway

    SOFT warnings (corpus / LLM quality, not a code bug):
      - Opened exercise topic does not contain any of the expected keywords
    """
    failures: list[str] = []
    warnings: list[str] = []

    opened_id = None
    if sim.exercises:
        opened_id = (sim.exercises[0] or {}).get("exam_id")

    if turn.should_open_exam:
        if sim.panel_action != "open":
            failures.append(
                f"panneau n'a PAS ouvert (action='{sim.panel_action}', "
                f"path='{sim.path_taken}')"
            )
        else:
            if turn.expected_subject and sim.opened_subject \
                    and _norm(sim.opened_subject) != _norm(turn.expected_subject):
                failures.append(
                    f"MAUVAISE MATIERE : attendue '{turn.expected_subject}', "
                    f"ouverte '{sim.opened_subject}' (exam='{sim.opened_exam_label}')"
                )
            # Hard failure: same exam_id as previous turn when user asked
            # for ANOTHER exercise (this was the user's #1 reported bug)
            if previous_exam_id and opened_id and opened_id == previous_exam_id:
                failures.append(
                    f"MEME EXAMEN RE-OUVERT : exam_id='{opened_id}' "
                    "inchangé alors que l'utilisateur demandait un AUTRE "
                    "exercice → perception utilisateur « rien ne ferme ni n'ouvre »"
                )
            # Soft warning on topic relevance
            if turn.must_contain_in_opened:
                ex_name = _norm(sim.opened_exercise_name or "")
                if not any(_norm(kw) in ex_name for kw in turn.must_contain_in_opened):
                    warnings.append(
                        f"topic opened='{(sim.opened_exercise_name or '')[:80]}' "
                        f"ne contient aucun de {turn.must_contain_in_opened[:5]} "
                        "(⚠️ couverture du corpus / scoring de search_full_exercises)"
                    )
    else:
        if sim.panel_action == "open":
            failures.append(
                f"panneau a ouvert alors qu'on demandait seulement le "
                f"tableau (exam='{sim.opened_exam_label}')"
            )
    return (not failures), failures, warnings


async def main():
    settings = get_settings()
    api_key = (getattr(settings, "deepseek_api_key", None)
               or getattr(settings, "DEEPSEEK_API_KEY", None))
    base_url = (getattr(settings, "deepseek_base_url", None)
                or "https://api.deepseek.com/v1")
    if not api_key:
        print("[FATAL] DEEPSEEK_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Preload exam bank so first call is honest
    exam_bank._ensure_loaded()  # type: ignore
    print(f"[Init] exam_bank loaded: {len(exam_bank._questions)} questions")  # type: ignore

    llm = LLMService()

    # Stateful conversation
    conversation_history: list[dict] = []
    current_exam_view: Optional[dict] = None

    reports: list[TurnReport] = []
    async with httpx.AsyncClient() as client:
        for turn in TURNS:
            print(f"\n━━━ {turn.label} ━━━")
            print(f"  USER: {turn.user_msg[:100]}...")

            # Build system prompt
            base_prompt = llm.build_libre_prompt(
                language="français",
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
                session_mode="libre",
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

            # Update conversation history and current_exam_view
            conversation_history.append({"role": "user", "content": turn.user_msg})
            # Store a cleaned response (no heavy tags) to keep ctx manageable
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
            # "stay" — keep as-is

            view_after = dict(current_exam_view) if current_exam_view else None

            reports.append(TurnReport(
                turn=turn, response=response, elapsed=elapsed, sim=sim,
                current_exam_view_before=view_before,
                current_exam_view_after=view_after,
                passed=passed, failures=failures, warnings=warnings,
            ))

    # ── Build markdown report ────────────────────────────────────────
    out: list[str] = []
    out.append("# Test MULTI-TOURS — BUG exam switch / genes liés / après tableau\n")
    out.append(f"_Généré le {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")
    out.append(
        "\nObjectif : reproduire le scénario exact rapporté par "
        "l'utilisateur en jouant une conversation à 7 tours contre le "
        "vrai LLM DeepSeek et en simulant le backend (exam_bank + "
        "cascading retries) entre chaque tour.\n"
    )

    grand_passed = sum(1 for r in reports if r.passed)
    grand_total = len(reports)
    verdict = "🎉 TOUT VERT" if grand_passed == grand_total else (
        f"⚠️ {grand_total - grand_passed} FAIL (bugs reproduits)")
    out.append(f"\n## Score : **{grand_passed}/{grand_total}** — {verdict}\n")

    out.append("\n| # | Tour | Path | Action | Subject ouverte | Verdict |")
    out.append("|---|---|---|---|---|---|")
    for i, r in enumerate(reports, 1):
        label = r.turn.label[:55]
        verdict_cell = "✅" if r.passed else f"❌ {len(r.failures)}"
        out.append(
            f"| {i} | {label} | `{r.sim.path_taken}` | "
            f"`{r.sim.panel_action}` | "
            f"`{r.sim.opened_subject or '—'}` | {verdict_cell} |"
        )

    for i, r in enumerate(reports, 1):
        out.append(f"\n---\n\n## {i}. {r.turn.label}\n")
        out.append(f"**Message utilisateur :**\n> {r.turn.user_msg}\n")
        out.append("**État AVANT ce tour :**")
        out.append("```json")
        out.append(json.dumps(r.current_exam_view_before, ensure_ascii=False, indent=2)
                   if r.current_exam_view_before else "null (aucun examen ouvert)")
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

    report = Path(__file__).parent / "test_exam_multiturn_bug_report.md"
    report.write_text("\n".join(out), encoding="utf-8")
    print(f"\n[TEST] Rapport : {report}")
    print(f"[TEST] Score : {grand_passed}/{grand_total} — {verdict}")


if __name__ == "__main__":
    asyncio.run(main())
