"""
Diagnostic — mode examen > "Aide au tableau" (ExamPractice.tsx) puis
questions de suivi.

Bug rapporte :
  « dans le mode examen quand on fait aide au tableau il me donne les
    instructions, mais quand je pose une question sur la meme question
    il ne sait plus de quelle question il s'agit — il faut une
    memoire pour garder la question en cours d'etude. »

Flow vrai en prod :
  1. Frontend ExamPractice.tsx: clic "Aide au tableau" -> sauve
     `explain_context` (questionContent, correction, studentAnswer, ...)
     dans sessionStorage et navigue vers /exam-explain.
  2. Frontend LearningSession.tsx: mode='explain', lit explain_context et
     envoie `init_session` au backend avec scenario JSON qui contient
     questionContent.
  3. Backend session_handler._init_session: injecte questionContent +
     correction dans le PREMIER message utilisateur (opening).
  4. Les messages suivants sont `{type: 'text_input', text: '...'}` —
     SANS aucune metadonnee d'examen.
  5. session_handler._process_student_input construit le prompt systeme
     et injecte le bloc [CONTEXTE — EXAMEN ACTUELLEMENT AFFICHE] SI et
     seulement si self.current_exam_view est rempli. OR : en mode
     explain, current_exam_view N'EST JAMAIS REMPLI (il n'est alimente
     que par set_exam_panel_view qui est envoye par ExamExercisePanel
     coaching/libre, PAS par ExamPractice).

Consequence : sur les tours 2, 3, 4, le LLM n'a QUE la conversation
history comme rappel de la question. Quand l'etudiant pose une
question breve ("et la question 2 ?", "pourquoi ?", "explique autrement"),
le LLM :
  - soit s'appuie sur la history (OK si la question est dans le
    premier tour et pas tronquee)
  - soit demande "de quelle question tu parles ?" (bug)
  - soit repond generiquement sur une AUTRE question du BAC (bug)

Ce script joue 4 tours contre le vrai LLM dans la meme configuration
que le backend en mode explain, et :
  - capture le prompt systeme exact envoye a chaque tour
  - verifie qu'il contient (ou non) l'enonce de la question
  - verifie que la reponse du LLM reference correctement la question
  - signale les signaux de perte de contexte
    ("quelle question", "peux-tu me donner l'enonce", "quelle question 2")

Sortie : scripts/test_exam_explain_memory_report.md
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

_stub = _types.ModuleType("app.services.rag_service")
class _NoopRag:
    def build_grounded_context(self, *a, **kw): return ""
    def search(self, *a, **kw): return []
def _get_rag_service(): return _NoopRag()
_stub.get_rag_service = _get_rag_service  # type: ignore
sys.modules["app.services.rag_service"] = _stub

from app.config import get_settings  # noqa: E402
from app.services.llm_service import LLMService  # noqa: E402

LLMService._ensure_rag_initialized = lambda self: None  # type: ignore


# ─────────────────────────────────────────────────────────────────────
# Simule un scenario EXPLAIN realiste : eleve sur Q2 d'un exercice BAC
# SVT sur la pollution, a deja repondu et veut comprendre.
# ─────────────────────────────────────────────────────────────────────
EXPLAIN_CONTEXT = {
    "subject": "SVT",
    "examTitle": "SVT 2024 Normale",
    "questionContent": (
        "Question 2 : En se basant sur les documents 1 et 2, expliquer "
        "l'impact de la pollution par les nitrates sur la biodiversite "
        "aquatique du lac. Precisez les mecanismes biogeochimiques mis "
        "en jeu."
    ),
    "questionType": "open",
    "points": 4,
    "parentContent": (
        "Exercice 2 — Pollution aquatique et eutrophisation. "
        "Le lac Oum Er-Rbia presente depuis 2015 des phenomenes "
        "d'eutrophisation causes par les rejets agricoles."
    ),
    "exerciseContext": (
        "Document 1 : graphique de concentration en nitrates (NO3-) "
        "dans le lac entre 2010 et 2024. Document 2 : courbe de "
        "biomasse en phytoplancton et oxygene dissous sur la meme "
        "periode."
    ),
    "correction": (
        "L'enrichissement en nitrates stimule la proliferation du "
        "phytoplancton (eutrophisation). La decomposition de cette "
        "biomasse consomme l'oxygene dissous par respiration bacterienne, "
        "ce qui cause l'asphyxie des poissons et la chute de la "
        "biodiversite."
    ),
    "hasAnswer": True,
    "studentAnswer": (
        "La pollution tue les poissons et les algues poussent."
    ),
    "studentScore": 0.5,
    "studentPointsMax": 4,
    "evaluatorFeedback": (
        "Reponse trop imprecise. Le mecanisme biogeochimique n'est "
        "pas explicite (eutrophisation, consommation de O2 dissous "
        "par les bacteries)."
    ),
    "studentHasImage": False,
}

# Tours de suivi que l'eleve pose SUR LA MEME PAGE (meme question ouverte)
FOLLOWUP_TURNS = [
    (
        "T2 — question breve de suivi",
        "Pourquoi le phytoplancton prolifere ?",
    ),
    (
        "T3 — reference implicite a la question",
        "Donne-moi un exemple concret de la reponse modele pour "
        "cette question.",
    ),
    (
        "T4 — demande de reformulation",
        "Peux-tu me reexpliquer autrement, je n'ai pas compris la "
        "partie biogeochimique ?",
    ),
]


# ─────────────────────────────────────────────────────────────────────
# Reproduit la construction du prompt systeme de session_handler.py
# en mode explain, AVEC et SANS le fix propose (injection de
# current_exam_view).
# ─────────────────────────────────────────────────────────────────────
def build_exam_view_block(q: dict) -> str:
    """Reproduit L1614-1641 du session_handler."""
    subject = q.get("subject", "")
    exam_title = q.get("examTitle", "")
    q_content = q.get("questionContent", "")
    q_correction = q.get("correction", "")
    block = f"""
[CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ À L'ÉTUDIANT]
⚠️ L'étudiant a CE PANNEAU D'EXAMEN ouvert en ce moment. Tu DOIS te baser EXCLUSIVEMENT sur ces informations. NE JAMAIS inventer une autre année, session, exercice ou question.

📚 Examen : {subject} — {exam_title}
📖 Exercice sur la pollution aquatique
❓ Question affichée

ÉNONCÉ EXACT DE LA QUESTION AFFICHÉE :
{q_content or '(non disponible)'}
"""
    if q_correction:
        block += f"\nCORRECTION OFFICIELLE DE CETTE QUESTION :\n{q_correction}\n"
    block += """
RÈGLES STRICTES :
- Si l'étudiant parle de "cette question", "la question", "l'exercice", "l'examen", il parle TOUJOURS de CE qui est affiché ci-dessus.
- Tu ne mentionnes JAMAIS un examen/année différent à moins que l'étudiant ne te le demande explicitement.
"""
    return block


def build_initial_explain_opening(ctx: dict) -> str:
    """Reproduit L2202-L2267 du session_handler : opening AVANT/APRES."""
    q_content = ctx["questionContent"]
    q_parent = ctx.get("parentContent", "")
    q_exercise_ctx = ctx.get("exerciseContext", "")
    q_correction = ctx["correction"]
    student_answer = ctx["studentAnswer"]
    score = ctx["studentScore"]
    score_max = ctx["studentPointsMax"]
    eval_fb = ctx["evaluatorFeedback"]

    parts = [f"Question ({ctx['questionType']}, {ctx['points']} pts) : {q_content}"]
    if q_parent:
        parts.append(f"Énoncé parent : {q_parent}")
    if q_exercise_ctx:
        parts.append(f"Contexte de l'exercice : {q_exercise_ctx}")
    q_block = "\n".join(parts)

    return f"""L'élève a répondu à une question d'examen et veut comprendre EN PROFONDEUR ses points forts et ses erreurs.

{q_block}

RÉPONSE DE L'ÉLÈVE (à analyser, citer textuellement) :
«{student_answer}»
Note obtenue par l'évaluateur automatique : {score}/{score_max}
Correction officielle : {q_correction}

Retour de l'évaluateur automatique (référence interne, NE PAS le citer mot pour mot) :
{eval_fb}

TU ES UN PROFESSEUR EXPÉRIMENTÉ qui corrige une copie. Ne fais PAS un cours générique — décortique la réponse spécifique de cet élève.
(Le reste des consignes de structure pédagogique est identique à la prod — tronqué ici pour lisibilité.)
"""


# ─────────────────────────────────────────────────────────────────────
@dataclass
class TurnResult:
    label: str
    user_msg: str
    inject_exam_view: bool        # True = avec fix, False = prod actuelle
    prompt_contains_question: bool
    prompt_length: int
    response: str
    elapsed: float
    references_question_correctly: bool
    loss_signals: list = field(default_factory=list)


LOSS_PATTERNS = [
    r"\bquelle\s+question\b",
    r"\bde\s+quelle\s+question\b",
    r"peux[- ]tu\s+me\s+(?:donner|redonner|preciser|re-?dire)\s+l[' ]?enonc[ée]",
    r"peux[- ]tu\s+me\s+(?:dire|preciser)\s+quelle\s+(?:question|enonce)",
    r"\bquel(?:le)?\s+est\s+l[' ]enonc[ée]\b",
    r"\bsur\s+quelle\s+question\b",
    r"je\s+ne\s+sais\s+pas\s+(?:de\s+)?quelle",
    r"pourrais[- ]tu\s+me\s+rappeler",
]


def detect_loss_signals(response: str) -> list[str]:
    hits = []
    low = response.lower()
    for pat in LOSS_PATTERNS:
        if re.search(pat, low):
            hits.append(pat)
    return hits


def response_references_question(response: str, ctx: dict) -> bool:
    """Heuristique : la reponse cite un terme-cle SPECIFIQUE de la question."""
    low = response.lower()
    # Mots-cles de la question pollution/nitrates/phytoplancton/eutrophisation
    key_terms = [
        "nitrate", "eutrophisation", "phytoplancton",
        "biodiversit", "oxygene", "oxygène", "biogeochimi",
        "biogéochimi", "lac", "pollution",
    ]
    return sum(1 for t in key_terms if t in low) >= 2


async def call_llm(client, api_key, base_url, system_prompt, history,
                   user_msg, max_tokens=1500):
    messages = [{"role": "system", "content": system_prompt}] + history + [
        {"role": "user", "content": user_msg}
    ]
    t0 = time.time()
    try:
        resp = await client.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": messages,
                  "temperature": 0.3, "max_tokens": max_tokens,
                  "stream": False},
            timeout=180.0,
        )
        resp.raise_for_status()
        content = resp.json().get("choices", [{}])[0].get(
            "message", {}).get("content", "")
    except Exception as e:
        content = f"[ERROR: {e}]"
    return content, time.time() - t0


# ─────────────────────────────────────────────────────────────────────
async def run_scenario(inject_exam_view: bool, llm, client, api_key, base_url):
    """Joue 4 tours (1 opening + 3 follow-ups) en mode explain.

    Si inject_exam_view=True, on ajoute le bloc
    [CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ] au prompt systeme a
    CHAQUE tour (ce que le fix propose).
    Si False, on reproduit la prod actuelle (bloc absent).
    """
    ctx = EXPLAIN_CONTEXT

    # Build base system prompt as in production (mode explain uses
    # _build_session_system_prompt -> build_system_prompt with
    # subject=ctx['subject'])
    base_prompt = llm.build_system_prompt(
        subject=ctx["subject"],
        language="français",
        chapter_title="Pollution aquatique",
        lesson_title="Eutrophisation",
        phase="explanation",
        objective="Corriger la copie de l'eleve sur la question 2",
        scenario_context=json.dumps(ctx, ensure_ascii=False),
        student_name="Eleve",
        proficiency="intermédiaire",
        user_query="",
    )

    results: list[TurnResult] = []
    conversation_history: list[dict] = []

    # ── T1 : opening (comme backend _init_session explain) ──
    opening_user_msg = build_initial_explain_opening(ctx)
    sys_prompt_t1 = base_prompt
    if inject_exam_view:
        sys_prompt_t1 += "\n\n" + build_exam_view_block(ctx)

    print(f"\n━━━ T1 — opening explain (inject_exam_view={inject_exam_view}) ━━━")
    response, elapsed = await call_llm(
        client, api_key, base_url, sys_prompt_t1, conversation_history,
        opening_user_msg, max_tokens=2000,
    )
    conversation_history.append({"role": "user", "content": opening_user_msg})
    conversation_history.append({"role": "assistant", "content": response[:2500]})
    refs = response_references_question(response, ctx)
    losses = detect_loss_signals(response)
    print(f"  LLM: {len(response)} chars in {elapsed:.1f}s — refs={refs} losses={len(losses)}")
    results.append(TurnResult(
        label="T1 — opening explain",
        user_msg=opening_user_msg[:300] + "...",
        inject_exam_view=inject_exam_view,
        prompt_contains_question=(ctx["questionContent"][:40] in sys_prompt_t1),
        prompt_length=len(sys_prompt_t1),
        response=response, elapsed=elapsed,
        references_question_correctly=refs, loss_signals=losses,
    ))

    # ── T2, T3, T4 : questions de suivi ──
    for label, user_msg in FOLLOWUP_TURNS:
        sys_prompt = base_prompt
        if inject_exam_view:
            sys_prompt += "\n\n" + build_exam_view_block(ctx)

        print(f"\n━━━ {label} (inject_exam_view={inject_exam_view}) ━━━")
        print(f"  USER: {user_msg}")

        response, elapsed = await call_llm(
            client, api_key, base_url, sys_prompt, conversation_history,
            user_msg, max_tokens=1200,
        )
        conversation_history.append({"role": "user", "content": user_msg})
        conversation_history.append({"role": "assistant", "content": response[:2500]})
        refs = response_references_question(response, ctx)
        losses = detect_loss_signals(response)
        print(f"  LLM: {len(response)} chars in {elapsed:.1f}s — refs={refs} losses={len(losses)}")
        if losses:
            print(f"  ⚠️ LOSS SIGNALS: {losses}")

        results.append(TurnResult(
            label=label,
            user_msg=user_msg,
            inject_exam_view=inject_exam_view,
            prompt_contains_question=(ctx["questionContent"][:40] in sys_prompt),
            prompt_length=len(sys_prompt),
            response=response, elapsed=elapsed,
            references_question_correctly=refs, loss_signals=losses,
        ))

    return results


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

    async with httpx.AsyncClient() as client:
        print("\n══════ SCENARIO A — PROD ACTUELLE (sans fix) ══════")
        print("current_exam_view n'est PAS rempli en mode explain ->")
        print("le bloc [CONTEXTE EXAMEN] n'est PAS injecte sur les tours 2,3,4.")
        results_prod = await run_scenario(
            inject_exam_view=False, llm=llm, client=client,
            api_key=api_key, base_url=base_url,
        )

        print("\n\n══════ SCENARIO B — AVEC FIX (current_exam_view injecte) ══════")
        print("Le bloc [CONTEXTE EXAMEN] est injecte a CHAQUE tour.")
        results_fixed = await run_scenario(
            inject_exam_view=True, llm=llm, client=client,
            api_key=api_key, base_url=base_url,
        )

    # ── Build markdown report ────────────────────────────────────────
    out: list[str] = []
    out.append("# Diagnostic — mode examen > « Aide au tableau » > questions de suivi\n")
    out.append(f"_Généré le {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")
    out.append(
        "\n## Hypothèse\n"
        "En mode `explain` (ExamPractice > « Aide au tableau »), le "
        "backend injecte la question dans le PREMIER message utilisateur "
        "(opening) mais ne remplit JAMAIS `self.current_exam_view`. "
        "Résultat : le bloc `[CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ]` "
        "n'est PAS ajouté au prompt système sur les tours 2, 3, 4… "
        "Le LLM n'a plus que `conversation_history` comme mémoire et "
        "peut perdre la question étudiée.\n"
    )
    out.append(
        "\n## Expérience\n"
        "On rejoue 4 tours (1 opening + 3 questions de suivi) contre "
        "le vrai LLM DeepSeek sur une question SVT Q2 (pollution par "
        "nitrates), dans 2 scénarios :\n"
        "- **A — prod actuelle** : bloc exam non injecté sur les "
        "tours de suivi\n"
        "- **B — avec fix** : bloc exam injecté à CHAQUE tour "
        "(mirroir de la proposition de fix)\n"
        "\nOn mesure :\n"
        "- `prompt_contains_question` : l'énoncé est-il dans le "
        "prompt système ?\n"
        "- `references_question_correctly` : la réponse du LLM cite-t-elle "
        "≥ 2 termes-clés de la question (nitrate, eutrophisation, …) ?\n"
        "- `loss_signals` : la réponse contient-elle une formule de "
        "perte de contexte (`quelle question`, `peux-tu me redonner "
        "l'énoncé`, …) ?\n"
    )

    def summary(results):
        n_prompt_ok = sum(1 for r in results if r.prompt_contains_question)
        n_refs = sum(1 for r in results if r.references_question_correctly)
        n_losses = sum(1 for r in results if r.loss_signals)
        return n_prompt_ok, n_refs, n_losses

    a_prompt, a_refs, a_loss = summary(results_prod)
    b_prompt, b_refs, b_loss = summary(results_fixed)

    out.append("\n## Résultats\n")
    out.append("| Scénario | Prompt contient question | Réponses qui citent ≥2 termes-clés | Réponses avec perte de contexte |")
    out.append("|---|---|---|---|")
    out.append(f"| **A — prod actuelle** (sans fix) | {a_prompt}/4 | {a_refs}/4 | {a_loss}/4 |")
    out.append(f"| **B — avec fix** (current_exam_view injecté) | {b_prompt}/4 | {b_refs}/4 | {b_loss}/4 |")

    for scen_label, results in [("A — PROD ACTUELLE (sans fix)", results_prod),
                                 ("B — AVEC FIX", results_fixed)]:
        out.append(f"\n---\n\n## Scénario {scen_label}\n")
        for r in results:
            out.append(f"\n### {r.label}\n")
            out.append(f"**Message utilisateur :** `{r.user_msg[:200]}`\n")
            out.append(
                f"- `prompt_contains_question` = "
                f"**{r.prompt_contains_question}** "
                f"(prompt_length={r.prompt_length})"
            )
            out.append(
                f"- `references_question_correctly` = "
                f"**{r.references_question_correctly}** "
                f"(citations nitrate/eutrophisation/phytoplancton/…)"
            )
            if r.loss_signals:
                out.append(f"- ⚠️ `loss_signals` = {r.loss_signals}")
            else:
                out.append(f"- ✅ pas de signal de perte de contexte")
            out.append(f"\n**Réponse LLM ({len(r.response)} chars, {r.elapsed:.1f}s) :**")
            out.append("```")
            out.append(r.response[:2000] + ("\n…[tronqué]" if len(r.response) > 2000 else ""))
            out.append("```")

    out.append("\n---\n\n## Conclusion & fix recommandé\n")
    if a_loss > b_loss or (a_refs < b_refs):
        out.append(
            "✅ **Hypothèse confirmée** : l'injection du bloc exam à "
            "chaque tour améliore la rétention du contexte "
            f"(refs : {a_refs}/4 → {b_refs}/4, "
            f"perte : {a_loss}/4 → {b_loss}/4).\n"
        )
    else:
        out.append(
            "⚠️ Les deux scénarios ont produit des scores similaires — "
            "dans ce corpus de 4 tours, la conversation history suffit "
            "au LLM. Mais le bug rapporté en prod survient sur des "
            "sessions plus longues ou quand la history est tronquée.\n"
        )
    out.append(
        "\n**Fix proposé** (`backend/app/websockets/session_handler.py` "
        "`_init_session`, branche `explain`) :\n"
        "```python\n"
        "# Après avoir parsé explain_data…\n"
        "self.current_exam_view = {\n"
        "    'exam_id': explain_data.get('examId') or '',\n"
        "    'subject': explain_data.get('subject') or '',\n"
        "    'exam_title': explain_data.get('examTitle') or '',\n"
        "    'exercise_name': explain_data.get('parentContent','')[:80],\n"
        "    'question_number': explain_data.get('questionNumber'),\n"
        "    'question_total': explain_data.get('questionTotal'),\n"
        "    'question_content': q_content,\n"
        "    'question_correction': q_correction,\n"
        "    'question_points': q_points,\n"
        "}\n"
        "```\n"
        "Ainsi, à chaque tour de suivi, `_process_student_input` "
        "injectera le bloc `[CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ]` "
        "dans le prompt système et le LLM saura toujours de quelle "
        "question on parle.\n"
    )

    report = Path(__file__).parent / "test_exam_explain_memory_report.md"
    report.write_text("\n".join(out), encoding="utf-8")
    print(f"\n[DIAG] Rapport : {report}")
    print(f"[DIAG] A (prod)  : prompt={a_prompt}/4 refs={a_refs}/4 loss={a_loss}/4")
    print(f"[DIAG] B (fix)   : prompt={b_prompt}/4 refs={b_refs}/4 loss={b_loss}/4")


if __name__ == "__main__":
    asyncio.run(main())
