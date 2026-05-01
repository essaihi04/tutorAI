"""
Test empirique — RE-OUVERTURE D'UN NOUVEL EXERCICE BAC alors qu'un examen
est déjà ouvert dans le panneau.

Bug rapporté par l'utilisateur :
  « Quand je demande un autre exercice de type BAC, la plateforme n'arrive
    pas à fermer l'examen initial et ouvrir le nouveau. »

Hypothèse principale : le system prompt est augmenté d'un bloc
``[CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ]`` (session_handler.py L1614)
qui force le LLM à :

    « Tu ne mentionnes JAMAIS un examen/année différent à moins que
      l'étudiant ne te le demande explicitement. »

Le LLM peut alors :
  (a) répondre en restant sur l'examen courant (ne pas émettre de
      ``<exam_exercise>`` pour le nouvel exercice demandé) ; OU
  (b) émettre un ``<exam_exercise>`` mais avec un contenu vague qui
      retourne le même exercice ; OU
  (c) émettre correctement un nouveau tag.

Ce test couvre 3 scénarios :
  T1. LIBRE  — un examen SVT (mitose) est ouvert, l'élève demande un
      autre exercice BAC SVT sur la génétique.
  T2. LIBRE  — un examen SVT ouvert, l'élève demande un autre exercice
      BAC sur le même thème (mitose) — doit ré-ouvrir un autre exercice
      (pas refuser).
  T3. COACHING — un examen est ouvert pendant la leçon, l'élève demande
      explicitement un autre exercice BAC.

Pour chaque scénario :
  1. Construit le system prompt en mode prod : libre/coaching prompt
     + bloc EXAMEN ACTUELLEMENT AFFICHÉ avec un examen courant.
  2. Appelle le LLM avec la nouvelle demande de l'étudiant.
  3. Vérifie que le LLM émet un nouveau ``<exam_exercise>`` ET que la
     thématique du tag correspond à la nouvelle demande, pas à l'examen
     courant.

Sortie : scripts/test_exam_switch_report.md
"""
from __future__ import annotations

import asyncio
import re
import sys
import time
import types as _types
from dataclasses import dataclass
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

# Stub heavy ML deps so we can import LLMService.
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
def build_exam_view_block(*, subject: str, year: str, session: str,
                          exam_title: str, exercise_name: str,
                          q_num: int, q_total: int,
                          q_content: str,
                          q_correction: str = "") -> str:
    """Mirror of session_handler.py L1614-L1632 — the exam-view block
    that gets appended to the system prompt when an exam panel is open.
    """
    session_label = session.capitalize() if session else ""
    header = " — ".join([b for b in [subject, session_label, year] if b])
    block = f"""
[CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ À L'ÉTUDIANT]
⚠️ L'étudiant a CE PANNEAU D'EXAMEN ouvert en ce moment. Tu DOIS te baser EXCLUSIVEMENT sur ces informations. NE JAMAIS inventer une autre année, session, exercice ou question.

📚 Examen : {header}
📖 {exercise_name}
❓ Question {q_num}/{q_total}

ÉNONCÉ EXACT DE LA QUESTION AFFICHÉE :
{q_content}
"""
    if q_correction:
        block += f"\nCORRECTION OFFICIELLE DE CETTE QUESTION :\n{q_correction}\n"
    block += """
RÈGLES STRICTES :
- Si l'étudiant parle de "cette question", "la question N°X", "l'exercice", "l'examen", il parle TOUJOURS de CE qui est affiché ci-dessus.
- Tu cites l'année et la session EXACTES indiquées ci-dessus. JAMAIS d'autres.
- Tu ne mentionnes JAMAIS un examen/année différent à moins que l'étudiant ne te le demande explicitement.

🔄 BASCULE VERS UN AUTRE EXERCICE BAC :
- Si l'étudiant demande explicitement « un AUTRE exercice », « un nouvel exercice », « ferme et ouvre », « différent », « autre année », « autre session » (même thème ou thème différent), tu DOIS :
  1. Émettre IMMÉDIATEMENT un nouveau `<exam_exercise>mots-clés du thème demandé</exam_exercise>` afin que le SYSTÈME charge un VRAI exercice depuis la banque officielle BAC.
  2. NE PAS fabriquer un faux énoncé d'examen sur le tableau (`<ui>` whiteboard). NE JAMAIS inventer un titre comme « BAC National 2022 — Session Normale » avec un énoncé que tu rédigerais toi-même : seuls les exercices ouverts via `<exam_exercise>` sont des VRAIS exercices BAC.
  3. NE PAS citer une année/session précise dans ta phrase d'introduction — laisse le système choisir l'exercice et afficher les vraies métadonnées dans le panneau.
  4. Annonce simplement : « D'accord, je t'ouvre un autre exercice BAC sur [thème] » puis émets le tag.
- Si l'étudiant veut continuer sur l'exercice actuel, reste sur celui affiché ci-dessus.
"""
    return block


# ─────────────────────────────────────────────────────────────────────
@dataclass
class Scenario:
    name: str
    mode: str                     # "libre" | "coaching"
    ctx_subject: str
    # Currently-open exam (simulating an active panel)
    open_subject: str
    open_year: str
    open_session: str
    open_exam_title: str
    open_exercise_name: str
    open_q_content: str
    open_q_topic: str             # used to detect "same exercise" responses
    # New request
    user_msg: str
    expected_new_topic_kw: list[str]  # at least one must appear in the new tag
    # Coaching-only
    chapter_title: str = ""
    lesson_title: str = ""
    objective: str = ""


SCENARIOS: list[Scenario] = [
    Scenario(
        name="T1 • LIBRE — examen SVT mitose ouvert → demande nouvelle exercice génétique",
        mode="libre",
        ctx_subject="Général",
        open_subject="SVT", open_year="2025", open_session="Rattrapage",
        open_exam_title="SVT 2025 Rattrapage",
        open_exercise_name="Exercice 2 — Mitose et division cellulaire",
        open_q_content=(
            "1. Définissez les phases de la mitose et indiquez sur un schéma "
            "annoté l'aspect des chromosomes en métaphase. (3 pts)"
        ),
        open_q_topic="mitose",
        user_msg=(
            "Merci pour cet exercice ! Maintenant, donne-moi un AUTRE exercice "
            "BAC en SVT, mais cette fois sur la GÉNÉTIQUE mendélienne — "
            "croisement dihybride avec échiquier. Ferme l'exercice actuel et "
            "ouvre le nouveau."
        ),
        expected_new_topic_kw=["génétique", "genetique", "mendel", "dihybrid",
                               "monohybrid", "croisement", "échiquier",
                               "echiquier", "allèle", "allele"],
    ),
    Scenario(
        name="T2 • LIBRE — examen SVT mitose ouvert → demande un autre BAC SVT (même thème)",
        mode="libre",
        ctx_subject="Général",
        open_subject="SVT", open_year="2025", open_session="Rattrapage",
        open_exam_title="SVT 2025 Rattrapage",
        open_exercise_name="Exercice 2 — Mitose",
        open_q_content="1. Décrivez la prophase mitotique. (2 pts)",
        open_q_topic="mitose",
        user_msg=(
            "J'ai fini cet exercice. Donne-moi un AUTRE exercice BAC SVT "
            "(année différente) toujours sur la mitose / division cellulaire "
            "pour m'entraîner sur un autre énoncé."
        ),
        # Even on the same topic, the LLM should propose a NEW exercise
        # (different exam_id / year), not say "we're already on it"
        expected_new_topic_kw=["mitose", "division cellulaire",
                               "cellule", "cellulaire", "chromosome"],
    ),
    Scenario(
        name="T3 • COACHING — examen génétique ouvert → demande explicitement un autre",
        mode="coaching",
        ctx_subject="SVT",
        chapter_title="Génétique humaine — transmission de deux gènes",
        lesson_title="Brassage interchromosomique — dihybridisme",
        objective="Maîtriser le dihybridisme et l'échiquier de fécondation",
        open_subject="SVT", open_year="2024", open_session="Normale",
        open_exam_title="SVT 2024 Normale",
        open_exercise_name="Exercice 3 — Génétique mendélienne",
        open_q_content=(
            "1. À partir du croisement F1 × F1 fourni, déterminez les "
            "génotypes parentaux et établissez l'échiquier des gamètes. (4 pts)"
        ),
        open_q_topic="génétique",
        user_msg=(
            "Cet exercice je l'ai fait. Donne-moi un autre exercice BAC SVT "
            "sur le brassage interchromosomique (génétique), une autre année. "
            "Ferme l'examen actuel et ouvre le nouveau."
        ),
        expected_new_topic_kw=["brassage", "interchromos", "génétique",
                               "genetique", "dihybrid", "échiquier",
                               "echiquier", "croisement"],
    ),
]


# ─────────────────────────────────────────────────────────────────────
def build_system_prompt(llm: LLMService, sc: Scenario) -> str:
    if sc.mode == "libre":
        sys_prompt = llm.build_libre_prompt(
            language="français",
            student_name="Audit",
            proficiency="intermédiaire",
            user_query=sc.user_msg,
        )
    elif sc.mode == "coaching":
        sys_prompt = llm.build_system_prompt(
            subject=sc.ctx_subject,
            language="français",
            chapter_title=sc.chapter_title,
            lesson_title=sc.lesson_title,
            phase="application",
            objective=sc.objective,
            scenario_context="",
            student_name="Audit",
            proficiency="intermédiaire",
            user_query=sc.user_msg,
        )
    else:
        raise ValueError(sc.mode)

    # Append the EXAM-VIEW block exactly like session_handler does at L1614
    exam_view_block = build_exam_view_block(
        subject=sc.open_subject, year=sc.open_year, session=sc.open_session,
        exam_title=sc.open_exam_title, exercise_name=sc.open_exercise_name,
        q_num=1, q_total=4, q_content=sc.open_q_content,
    )
    return sys_prompt + "\n\n" + exam_view_block


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
def _norm(s: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s or "")
                   if unicodedata.category(c) != "Mn").lower()


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
    new_tag: str
    checks: list[CheckResult]


def run_checks(sc: Scenario, response: str, new_tag: str) -> list[CheckResult]:
    out: list[CheckResult] = []
    resp_norm = _norm(response)
    tag_norm = _norm(new_tag)

    # ⭐ Core check #1 — the LLM emitted a NEW <exam_exercise> tag
    out.append(CheckResult(
        "⭐ Le LLM a émis un nouveau <exam_exercise> (close + open new)",
        bool(new_tag),
        f"contenu : {new_tag[:120]!r}" if new_tag
        else "❌ pas de tag <exam_exercise> — la prod va rester sur l'ancien examen"))

    # ⭐ Core check #2 — the new tag is on the NEW topic, not the open one
    if new_tag:
        topic_match = any(_norm(kw) in tag_norm
                          for kw in sc.expected_new_topic_kw)
        out.append(CheckResult(
            "⭐ Le tag pointe vers la NOUVELLE thématique demandée",
            topic_match,
            f"keywords attendus : {sc.expected_new_topic_kw[:5]} | "
            f"trouvé : {topic_match}"))

    # Check #3 — the LLM did NOT explicitly refuse to switch
    refusal_markers = [
        "je ne peux pas changer",
        "reste sur l'examen actuel",
        "concentrons-nous sur",
        "terminez d'abord",
        "finis d'abord",
        "termine d'abord",
        "concentre-toi sur",
        "on reste sur",
    ]
    refused = any(_norm(m) in resp_norm for m in refusal_markers)
    out.append(CheckResult(
        "Le LLM n'a PAS refusé de changer d'exercice",
        not refused,
        ("aucun refus détecté" if not refused
         else f"❌ marqueur de refus trouvé dans la réponse")))

    return out


# ─────────────────────────────────────────────────────────────────────
async def run_scenario(client, api_key, base_url, llm: LLMService,
                       sc: Scenario) -> ScenarioReport:
    print(f"\n[{sc.name}]")
    print(f"  → mode={sc.mode}  open_exam={sc.open_subject} {sc.open_year} {sc.open_session}")
    print(f"  → user_msg: {sc.user_msg[:100]}...")

    sys_prompt = build_system_prompt(llm, sc)
    response, elapsed = await call_llm(
        client, api_key, base_url, sys_prompt, sc.user_msg, max_tokens=1500,
    )
    print(f"  ← {len(response)} chars en {elapsed:.1f}s")

    # Find the LAST <exam_exercise> tag (in case the LLM mentioned the
    # current one and then opened a new one)
    matches = re.findall(r'<exam_exercise>(.*?)</exam_exercise>',
                         response, re.DOTALL)
    new_tag = matches[-1].strip() if matches else ""
    print(f"  tag_count={len(matches)}  new_tag={new_tag[:80]!r}")

    checks = run_checks(sc, response, new_tag)
    for c in checks:
        flag = "✅" if c.passed else "❌"
        print(f"   {flag} {c.name}")

    return ScenarioReport(scenario=sc, response=response, elapsed=elapsed,
                          new_tag=new_tag, checks=checks)


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
    out.append("# Test — RE-OUVERTURE D'UN NOUVEL EXERCICE BAC\n")
    out.append(f"_Généré le {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")
    out.append(
        "\nObjectif : confirmer que quand un examen est déjà ouvert dans "
        "le panneau et que l'utilisateur demande explicitement un AUTRE "
        "exercice BAC, le LLM ferme bien l'ancien et émet un nouveau "
        "`<exam_exercise>` correspondant à la nouvelle demande.\n"
    )

    grand_passed = sum(sum(1 for c in r.checks if c.passed) for r in reports)
    grand_total = sum(len(r.checks) for r in reports)
    full_pass = all(all(c.passed for c in r.checks) for r in reports)
    verdict = "🎉 TOUT VERT" if full_pass else (
        f"⚠️ {grand_total - grand_passed} FAIL")
    out.append(f"\n## Score global : **{grand_passed}/{grand_total}** — {verdict}\n")

    out.append("\n| # | Scénario | Mode | Tag émis | Topic OK | Verdict |")
    out.append("|---|---|---|---|---|---|")
    for i, r in enumerate(reports, 1):
        sc = r.scenario
        passed = sum(1 for c in r.checks if c.passed)
        total = len(r.checks)
        v = "✅" if passed == total else f"❌ {total-passed} FAIL"
        tag = "✅" if r.new_tag else "❌"
        topic_check = next(
            (c for c in r.checks if "NOUVELLE thématique" in c.name), None)
        topic = "—" if topic_check is None else (
            "✅" if topic_check.passed else "❌")
        out.append(f"| {i} | {sc.name[:60]} | `{sc.mode}` | {tag} | {topic} | "
                   f"{passed}/{total} {v} |")

    for i, r in enumerate(reports, 1):
        sc = r.scenario
        out.append(f"\n---\n\n## {i}. {sc.name}\n")
        out.append(f"- **Mode** : `{sc.mode}`")
        out.append(f"- **Examen ouvert** : {sc.open_subject} {sc.open_year} "
                   f"{sc.open_session} — {sc.open_exercise_name}")
        out.append(f"- **Topic ouvert** : {sc.open_q_topic}")
        out.append(f"- **Topic demandé** : {sc.expected_new_topic_kw[:5]}")
        out.append(f"- **Temps LLM** : {r.elapsed:.1f}s  •  "
                   f"**Réponse** : {len(r.response)} chars")
        out.append("")
        out.append(f"**Message envoyé :**\n> {sc.user_msg}\n")

        out.append("### Tag <exam_exercise> émis")
        if r.new_tag:
            out.append(f"- **Contenu** : `{r.new_tag}`")
        else:
            out.append("- **❌ Aucun tag émis** — le LLM est resté sur "
                       "l'examen courant ou a refusé.")

        out.append("\n### Checks")
        out.append("| # | Vérification | Statut | Détail |")
        out.append("|---|---|---|---|")
        for j, c in enumerate(r.checks, 1):
            flag = "✅ PASS" if c.passed else "❌ FAIL"
            out.append(f"| {j} | {c.name} | {flag} | {c.detail} |")

        out.append(f"\n### Réponse LLM ({len(r.response)} chars — extrait)")
        out.append("```")
        out.append(r.response[:3500] + ("\n…[tronqué]"
                   if len(r.response) > 3500 else ""))
        out.append("```")

    out.append(f"\n---\n\n**Score final : {grand_passed}/{grand_total}** — {verdict}\n")

    report = Path(__file__).parent / "test_exam_switch_report.md"
    report.write_text("\n".join(out), encoding="utf-8")
    print(f"\n[TEST] Rapport : {report}")
    print(f"[TEST] Score global : {grand_passed}/{grand_total} — {verdict}")


if __name__ == "__main__":
    asyncio.run(main())
