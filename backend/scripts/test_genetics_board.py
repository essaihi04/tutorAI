"""
Test ciblé : création d'un ÉCHIQUIER DE CROISEMENT dans le mode
« aide au tableau » (explain AVEC réponse de l'élève) sur la question
d'interprétation chromosomique du 2ᵉ croisement — examen national SVT
2025 Normale (Q20 à l'écran / Q19 dans exam.json).

Étapes :
  1. charge la question + correction officielle depuis exam.json,
  2. construit le system prompt explain (scenario block + libre prompt)
     exactement comme en prod,
  3. envoie une requête au LLM (DeepSeek) avec une réponse élève
     plausible et ambiguë (type d'erreur fréquent : génotypes mal
     posés, oubli du ¼ sur les gamètes),
  4. fait passer la réponse brute dans le pipeline de prod :
     ─ extraction du bloc ``<ui>...</ui>``
     ─ ``_escape_bare_backslashes`` (LaTeX survit à JSON)
     ─ ``json.loads``
     ─ ``_sanitize_genetics_cells`` (DO//dø → $\\dfrac{D}{d}\\,\\dfrac{O}{ø}$)
  5. applique une batterie de CHECKS sur le résultat :
     ✓ le LLM a bien émis un bloc ``<ui>`` ou ``<board>``,
     ✓ au moins un ``type=table`` (échiquier de fécondation),
     ✓ le tableau contient BIEN 4 colonnes × 4 lignes minimum,
     ✓ aucune notation ASCII résiduelle (``G//g``, ``G/``, …) après
       sanitisation,
     ✓ présence de ``\\dfrac`` dans les cellules (génotypes / gamètes),
     ✓ pas de ``\\text`` / ``\\times`` / ``\\frac`` corrompus en tab /
       formfeed (régression 5bdc363),
     ✓ présence des phénotypes ``[G,L]``, ``[G,ℓ]``, ``[g,L]``, ``[g,ℓ]``
       (conformes à la correction officielle),
     ✓ les 4 proportions 9/16, 3/16, 3/16, 1/16 (ou 9 : 3 : 3 : 1).

Sortie : scripts/test_genetics_board_report.md
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

# Stub heavy ML deps so we can import LLMService without loading FAISS.
_stub = _types.ModuleType("app.services.rag_service")
class _NoopRag:
    def build_grounded_context(self, *a, **kw): return ""
    def search(self, *a, **kw): return []
def _get_rag_service(): return _NoopRag()
_stub.get_rag_service = _get_rag_service  # type: ignore
sys.modules["app.services.rag_service"] = _stub

from app.config import get_settings  # noqa: E402
from app.services.llm_service import LLMService  # noqa: E402
from app.websockets.session_handler import (  # noqa: E402
    _escape_bare_backslashes,
    _sanitize_genetics_cells,
    _json_cleanup_variants,
    _collapse_latex_padding_raw,
)

LLMService._ensure_rag_initialized = lambda self: None  # type: ignore


# ── Réutilisation du scenario block (copie minimale de la prod) ──────
def build_explain_scenario_block(payload: dict) -> str:
    q_content = (payload.get("questionContent") or "").strip()
    q_type = (payload.get("questionType") or "open").strip()
    q_points = payload.get("points") or 0
    q_correction = (payload.get("correction") or "").strip()
    student_answer = (payload.get("studentAnswer") or "").strip()
    student_score = payload.get("studentScore")
    student_points_max = payload.get("studentPointsMax")
    evaluator_feedback = (payload.get("evaluatorFeedback") or "").strip()
    subject = (payload.get("subject") or "").strip()
    exam_title = (payload.get("examTitle") or "").strip()

    def _trim(s: str, n: int) -> str:
        return s if len(s) <= n else s[:n].rstrip() + " […]"

    lines = [
        "[CONTEXTE EXAMEN — MODE ENTRAÎNEMENT / EXPLICATION DE CORRECTION]",
        "⚠️ L'étudiant travaille sur UNE question d'examen BAC précise. "
        "Tu DOIS baser TOUTE ta correction et tes explications sur la "
        "CORRECTION OFFICIELLE ci-dessous.",
        "",
        "🧬 RÈGLE GÉNÉTIQUE (question de croisement / hérédité) :",
        "- L'interprétation chromosomique va OBLIGATOIREMENT dans un bloc "
        "<ui>{\"actions\":[{\"type\":\"whiteboard\",\"action\":\"show_board\","
        "\"payload\":{\"title\":\"...\",\"lines\":[...]}}]}</ui>, avec : "
        "phénotypes, génotypes en \\\\dfrac, gamètes, ÉCHIQUIER de "
        "fécondation en `type=table`, résultats.",
        "- Dans les cellules : UNIQUEMENT du LaTeX. GÉNOTYPE diploïde → "
        "DEUX BARRES `\\\\dfrac{G}{\\\\overline{g}}\\\\,\\\\dfrac{L}{\\\\overline{\\\\ell}}` "
        "(une paire de chromosomes homologues = deux traits horizontaux). "
        "GAMÈTE haploïde → UNE BARRE `\\\\dfrac{G}{}` (dénominateur vide). "
        "JAMAIS d'ASCII `G//g`, `G/`, `DO//dø`, et JAMAIS de génotype à "
        "une seule barre `\\\\dfrac{G}{g}` (= haploïde, faux).",
        "- Les phénotypes sont notés `[G,L]`, `[g,\\\\ell]` etc.",
        "",
    ]
    if exam_title:
        lines.append(f"📚 Examen : {exam_title}" + (f" ({subject})" if subject else ""))
    lines.append(f"❓ Question ({q_type}, {q_points} pt) :")
    lines.append(_trim(q_content, 1500))
    lines.append("")
    lines.append("✅ CORRECTION OFFICIELLE (source de vérité) :")
    lines.append(_trim(q_correction, 2000))
    lines.append("")
    lines.append("📝 RÉPONSE DE L'ÉLÈVE :")
    lines.append(f"« {_trim(student_answer, 1000)} »")
    if student_score is not None and student_points_max:
        lines.append(f"🔢 Note évaluateur : {student_score}/{student_points_max}")
    if evaluator_feedback:
        lines.append("🧮 Feedback évaluateur :")
        lines.append(_trim(evaluator_feedback, 800))
    lines.append("")
    lines.append("RÈGLES STRICTES : reste sur cette question, utilise "
                 "la correction officielle comme source de vérité, et "
                 "produis OBLIGATOIREMENT un <ui> show_board avec l'échiquier.")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# Pipeline de prod simulé : extrait <ui> → escape → json.loads → sanitize
# ─────────────────────────────────────────────────────────────────────
def extract_ui_boards(response: str) -> list[dict]:
    """Retourne la liste des payloads `show_board` trouvés, après le
    pipeline complet appliqué en prod côté WebSocket."""
    boards: list[dict] = []
    for m in re.finditer(r"<ui>(.*?)</ui>", response, re.DOTALL):
        raw = m.group(1).strip()
        parsed = None
        for variant in _json_cleanup_variants(raw):
            try:
                parsed = json.loads(variant)
                break
            except Exception:
                continue
        if not parsed:
            continue
        actions = parsed.get("actions") if isinstance(parsed, dict) else None
        if not isinstance(actions, list):
            continue
        for action in actions:
            if not isinstance(action, dict):
                continue
            if action.get("type") == "whiteboard" and action.get("action") == "show_board":
                payload = action.get("payload") or {}
                lines = payload.get("lines") or []
                lines = _sanitize_genetics_cells(lines)
                boards.append({
                    "title": payload.get("title", ""),
                    "lines": lines,
                })
    return boards


def extract_board_tags(response: str) -> list[dict]:
    """Ancienne balise ``<board>{...}</board>`` — fallback."""
    boards: list[dict] = []
    for m in re.finditer(r"<board>(.*?)</board>", response, re.DOTALL):
        raw = m.group(1).strip()
        parsed = None
        for variant in _json_cleanup_variants(raw):
            try:
                parsed = json.loads(variant)
                break
            except Exception:
                continue
        if isinstance(parsed, dict) and isinstance(parsed.get("lines"), list):
            lines = _sanitize_genetics_cells(parsed["lines"])
            boards.append({"title": parsed.get("title", ""), "lines": lines})
    return boards


# ─────────────────────────────────────────────────────────────────────
# Checks
# ─────────────────────────────────────────────────────────────────────
ASCII_GENETICS_LEAK = re.compile(
    r"(?<![A-Za-z$\\])[A-Za-zøùéÉØ+\-]{1,2}\s*//\s*[A-Za-zøùéÉØ+\-]{1,2}(?![A-Za-z])"
)
CORRUPTED_CMD = re.compile(
    # TAB/FF/BS/NL/CR suivi de ext|imes|rac|oxed|eg|ightarrow|abla
    r"[\t\x0b\x0c\x08\n\r](?:ext|imes|rac|oxed|eg|ightarrow|abla|orall|angle)"
)


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


def run_checks(boards: list[dict], response: str) -> list[CheckResult]:
    results: list[CheckResult] = []

    # 1. Un board a été produit
    has_board = bool(boards)
    results.append(CheckResult(
        "Un bloc <ui> show_board (ou <board>) est émis",
        has_board,
        f"{len(boards)} board(s) détecté(s)"))

    # 2. Aplatir tout le texte des cellules
    all_text = ""
    table_lines = []
    for b in boards:
        for ln in b["lines"]:
            if not isinstance(ln, dict):
                continue
            if ln.get("type") == "table":
                table_lines.append(ln)
            for key in ("content", "explanation"):
                v = ln.get(key)
                if isinstance(v, str):
                    all_text += "\n" + v
            for h in (ln.get("headers") or []):
                if isinstance(h, str):
                    all_text += "\n" + h
            for row in (ln.get("rows") or []):
                if isinstance(row, list):
                    for cell in row:
                        if isinstance(cell, str):
                            all_text += "\n" + cell

    # 3. Au moins une ligne type=table (échiquier)
    results.append(CheckResult(
        "Au moins une ligne `type=table` (échiquier de fécondation)",
        bool(table_lines),
        f"{len(table_lines)} table(s) trouvée(s)"))

    # 4. Échiquier 4×4 minimum (4 gamètes × 4 gamètes = 16 cases)
    big_table = any(
        len(t.get("rows") or []) >= 4 and
        all(isinstance(r, list) and len(r) >= 4 for r in (t.get("rows") or []))
        for t in table_lines
    )
    results.append(CheckResult(
        "Échiquier dihybride 4×4 (16 zygotes)",
        big_table,
        "table(s) 4×4 : " + str(big_table)))

    # 5. ASCII genetics leak (après sanitisation, il ne doit rester AUCUN)
    leaks = ASCII_GENETICS_LEAK.findall(all_text)
    # Filter out false positives in prose (gene names between parens were
    # stripped by our regex lookbehind, but the joined text has no parens
    # context now — so we re-filter by requiring at least one accented
    # genetics char to reduce noise).
    real_leaks = [lk for lk in leaks if any(c in lk for c in "øùéÉØ") or
                  any(c.isupper() for c in lk)]
    results.append(CheckResult(
        "Aucune notation ASCII `XY//xy` résiduelle (post-sanitizer)",
        not real_leaks,
        f"fuites : {real_leaks[:5]}"))

    # 6. Présence de \dfrac dans au moins une cellule
    has_dfrac = "\\dfrac" in all_text or "\\frac" in all_text
    results.append(CheckResult(
        "Au moins une cellule contient `\\dfrac` / `\\frac`",
        has_dfrac,
        "OK" if has_dfrac else "aucune fraction LaTeX"))

    # 7. Pas de commande LaTeX corrompue (régression 5bdc363)
    corrupted = CORRUPTED_CMD.search(all_text)
    results.append(CheckResult(
        "Pas de `\\text`/`\\times`/`\\frac` corrompu en tab/formfeed",
        corrupted is None,
        "OK" if corrupted is None else f"corruption : {corrupted.group(0)!r}"))

    # 8. Les 4 phénotypes attendus
    expected_phenotypes = ["[G,L]", "[G,ℓ]", "[g,L]", "[g,ℓ]"]
    # Accept also with spaces : [G, L]
    normalized_text = re.sub(r"\s+", "", all_text)
    found_ph = [p for p in expected_phenotypes
                if re.sub(r"\s+", "", p) in normalized_text or
                re.sub(r"\s+", "", p.replace("ℓ", "l")) in normalized_text]
    results.append(CheckResult(
        "Les 4 phénotypes F2 apparaissent : [G,L] [G,ℓ] [g,L] [g,ℓ]",
        len(found_ph) == 4,
        f"trouvés : {found_ph}"))

    # 9. Les 4 proportions 9/16, 3/16, 3/16, 1/16
    props = ["9/16", "3/16", "1/16"]
    found_props = [p for p in props if p in all_text]
    results.append(CheckResult(
        "Proportions 9/16, 3/16, 1/16 mentionnées",
        len(found_props) >= 3,
        f"trouvées : {found_props}"))

    # 10. Génotypes en notation DIPLOÏDE — deux barres horizontales.
    #     On exige qu'au moins une cellule du board contienne
    #     `\dfrac{X}{\overline{Y}}` (la barre d'overline en plus de la
    #     barre de fraction = paire de chromosomes homologues).
    has_double_bar = bool(re.search(r"\\dfrac\{[^{}]+\}\{\\overline\{",
                                    all_text))
    # On compte aussi le nombre de génotypes diploïdes pour avoir un échantillon.
    diploid_count = len(re.findall(r"\\dfrac\{[^{}]+\}\{\\overline\{[^{}]+\}\}",
                                   all_text))
    results.append(CheckResult(
        "Génotypes en notation diploïde (\\overline{} = 2 barres)",
        has_double_bar,
        f"{diploid_count} génotype(s) diploïde(s) détecté(s)"))

    # 11. Aucun génotype haploïde étranger — si une cellule de la TABLE
    #     contient `\dfrac{A}{a}` où a est une lettre simple SANS
    #     overline, c'est une fuite (gamètes ont `\dfrac{A}{}` vide).
    leaked = []
    for tbl in table_lines:
        for row in (tbl.get("rows") or []):
            if not isinstance(row, list):
                continue
            # Skip the first cell (= row header = gamete on the side).
            for cell in row[1:]:
                if not isinstance(cell, str):
                    continue
                # Find any \dfrac{X}{Y} where Y is a non-empty single allele
                # WITHOUT \overline → that's a single-bar genotype = bug.
                for m in re.finditer(r"\\dfrac\{([^{}]+)\}\{([^{}]+)\}", cell):
                    denom = m.group(2)
                    if denom and "\\overline" not in denom and "\\underline" not in denom:
                        leaked.append(m.group(0))
    results.append(CheckResult(
        "Aucun génotype à une seule barre dans les cellules d'échiquier",
        not leaked,
        f"fuites : {leaked[:3]}" if leaked else "OK"))

    return results


# ─────────────────────────────────────────────────────────────────────
async def call_llm(client, api_key, base_url, system_prompt, user_msg,
                   max_tokens=2200):
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
        content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        content = f"[ERROR: {e}]"
    return content, time.time() - t0


async def main():
    settings = get_settings()
    api_key = (getattr(settings, "deepseek_api_key", None)
               or getattr(settings, "DEEPSEEK_API_KEY", None))
    base_url = (getattr(settings, "deepseek_base_url", None)
                or "https://api.deepseek.com/v1")
    if not api_key:
        print("[FATAL] DEEPSEEK_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Load the exam and pick the question
    exam_path = ROOT / "data" / "exams" / "svt" / "2025-normale" / "exam.json"
    exam = json.loads(exam_path.read_text(encoding="utf-8"))

    target_q = None
    def walk(n):
        nonlocal target_q
        if target_q: return
        if isinstance(n, dict):
            if "content" in n and "correction" in n:
                content = (n.get("content") or "").lower()
                if "échiquier de croisement" in content or \
                   "interprétation chromosomique" in content:
                    target_q = n
                    return
            for v in n.values(): walk(v)
        elif isinstance(n, list):
            for v in n: walk(v)
    walk(exam)

    if not target_q:
        print("[FATAL] Question 'échiquier de croisement' introuvable "
              "dans svt_2025_normale.", file=sys.stderr)
        sys.exit(1)

    corr = target_q.get("correction")
    corr_text = corr.get("content", "") if isinstance(corr, dict) else (corr or "")

    # Plausible partial student answer — erreurs typiques :
    # - génotypes mal placés (ne sépare pas les deux gènes)
    # - oubli du facteur ¼ sur les gamètes
    # - pas d'échiquier 4×4 (juste une liste)
    student_answer = (
        "Le croisement F1 × F1 donne la F2. Les parents F1 sont [G,L] × [G,L]. "
        "Les génotypes sont GgLl × GgLl. Les gamètes sont GL, Gl, gL, gl. "
        "Je n'ai pas fait l'échiquier mais je sais qu'on obtient la proportion "
        "9 : 3 : 3 : 1 qui prouve que les gènes sont indépendants."
    )

    scenario = {
        "questionContent": target_q.get("content", ""),
        "questionType": target_q.get("type", "open"),
        "points": target_q.get("points", 1.5),
        "correction": corr_text,
        "subject": "SVT",
        "examTitle": "Examen National Baccalauréat — SVT 2025 Normale",
        "studentAnswer": student_answer,
        "studentScore": 0.75,
        "studentPointsMax": 1.5,
        "evaluatorFeedback": (
            "L'élève a bien identifié GgLl × GgLl et la proportion 9:3:3:1, "
            "mais n'a pas construit l'échiquier de croisement demandé, "
            "et n'a pas noté les génotypes en notation chromosomique "
            "(\\dfrac) ni les proportions ¼ sur chaque gamète."
        ),
    }

    scenario_block = build_explain_scenario_block(scenario)
    llm = LLMService()
    libre_prompt = llm.build_libre_prompt(
        language="français", student_name="Audit",
        proficiency="intermédiaire", user_query=target_q.get("content", ""),
    )
    system_prompt = scenario_block + "\n\n" + libre_prompt

    opening_user = (
        "L'élève a répondu à la question d'examen ci-dessus et veut "
        "comprendre EN PROFONDEUR ses points forts et ses erreurs. "
        "Décortique sa réponse en citant ses phrases entre guillemets, "
        "compare avec la correction officielle, donne la VERSION MODÈLE "
        "rédigée comme un élève le ferait sur sa copie BAC, puis "
        "PRODUIS OBLIGATOIREMENT un bloc <ui> show_board contenant "
        "l'échiquier de croisement complet : Parents → Génotypes en "
        "\\dfrac → Gamètes → Échiquier de fécondation 4×4 (type=table) "
        "→ Résultats (phénotypes avec leurs proportions 9/16, 3/16, "
        "3/16, 1/16)."
    )

    print(f"[TEST] Question ciblée : {target_q.get('content','')[:100]}…")
    print(f"[TEST] Appel LLM en cours (max 180s)…")

    async with httpx.AsyncClient() as client:
        response, elapsed = await call_llm(
            client, api_key, base_url, system_prompt, opening_user,
            max_tokens=3500,  # Match prod: genetics questions get 3500
        )

    print(f"[TEST] Réponse reçue en {elapsed:.1f}s ({len(response)} chars)")

    # Detect the padding-loop pathology before parsing.
    raw_padding_run = re.search(r"(?:\\;){10,}|(?:\\,){20,}|(?:\\quad){10,}",
                                response)
    if raw_padding_run:
        print(f"[TEST] ⚠️ PADDING LOOP détecté dans la réponse brute : "
              f"{len(raw_padding_run.group(0))} chars")

    # Pipeline de prod : collapse padding raw → extract <ui> → sanitize
    response_collapsed = _collapse_latex_padding_raw(response)
    boards = extract_ui_boards(response_collapsed) + extract_board_tags(response_collapsed)
    checks = run_checks(boards, response_collapsed)
    # Add a dedicated check for the padding loop pathology.
    checks.insert(0, CheckResult(
        "Pas de boucle de padding LaTeX dans la réponse brute",
        raw_padding_run is None,
        ("OK" if raw_padding_run is None
         else f"sequence pathologique : {len(raw_padding_run.group(0))} chars de \\; / \\, / \\quad"),
    ))

    # ── Build report ────────────────────────────────────────────────
    out: list[str] = []
    out.append("# Test : Échiquier de croisement — SVT 2025 Normale (Q20)\n")
    out.append(f"_Généré le {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")
    out.append(f"\n**Temps LLM** : {elapsed:.1f}s — **Réponse** : {len(response)} chars\n")
    out.append(f"**Boards détectés** : {len(boards)}\n")

    out.append("\n## Checks\n")
    out.append("| # | Vérification | Statut | Détail |")
    out.append("|---|---|---|---|")
    for i, c in enumerate(checks, 1):
        flag = "✅ PASS" if c.passed else "❌ FAIL"
        out.append(f"| {i} | {c.name} | {flag} | {c.detail} |")

    passed = sum(1 for c in checks if c.passed)
    total = len(checks)
    verdict = "🎉 TOUT VERT" if passed == total else f"⚠️ {total - passed} FAIL"
    out.append(f"\n**Score : {passed}/{total}** — {verdict}\n")

    # Dump boards (sanitized)
    if boards:
        out.append("\n## Contenu des boards (après sanitizer)\n")
        for i, b in enumerate(boards, 1):
            out.append(f"\n### Board {i} — « {b['title']} »\n")
            out.append("```json")
            out.append(json.dumps(b["lines"], ensure_ascii=False, indent=2))
            out.append("```")

    # Raw LLM response (truncated)
    out.append("\n## Réponse brute LLM\n")
    out.append("```")
    out.append(response[:5000] + ("\n…[tronqué]" if len(response) > 5000 else ""))
    out.append("```")

    report = Path(__file__).parent / "test_genetics_board_report.md"
    report.write_text("\n".join(out), encoding="utf-8")
    print(f"\n[TEST] Rapport : {report}")
    print(f"[TEST] Score : {passed}/{total} — {verdict}")


if __name__ == "__main__":
    asyncio.run(main())
