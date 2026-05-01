"""
Test multi-scénarios — STRUCTURATION DU TABLEAU dans les modes
``libre`` et ``coaching``.

Problèmes ciblés :
  • Le LLM donne parfois la réponse en TEXTE BRUT (markdown / paragraphes)
    au lieu d'émettre un bloc ``<ui>`` show_board → l'élève ne voit
    aucun tableau récapitulatif.
  • En génétique, le LLM oublie parfois la notation diploïde (deux
    barres) ou laisse de l'ASCII (``GG//gg``).
  • Le LLM peut entrer en boucle de padding (``\\;\\;\\;…``) ou
    corrompre des commandes LaTeX (``\\text`` → tab).

Scénarios joués contre le vrai LLM (DeepSeek) :

  A. LIBRE + génétique dihybride (croisement F1×F1) → échiquier 4×4 +
     génotypes diploïdes double-barre.
  B. LIBRE + génétique monohybride simple → board avec génotypes
     `\\dfrac{X}{\\overline{Y}}`.
  C. COACHING + chapitre « Génétique et expression de l'information »,
     demande explicite d'échiquier dihybride → board structuré BAC.
  D. LIBRE + non-génétique : « résume-moi la mitose en tableau » →
     test de structuration pure (au moins un <ui> show_board).

Chaque scénario produit un sous-rapport avec un set de checks adapté.
Score global agrégé en fin de rapport.

Sortie : scripts/test_board_structure_report.md
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

import httpx

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Stub heavy ML deps (RAG / sentence-transformers) so we can import
# llm_service without loading FAISS.
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
    _sanitize_genetics_cells,
    _json_cleanup_variants,
    _collapse_latex_padding_raw,
)

LLMService._ensure_rag_initialized = lambda self: None  # type: ignore


# ─────────────────────────────────────────────────────────────────────
# Pipeline de prod simulé
# ─────────────────────────────────────────────────────────────────────
def extract_ui_boards(response: str) -> list[dict]:
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
    r"[\t\x0b\x0c\x08\n\r](?:ext|imes|rac|oxed|eg|ightarrow|abla|orall|angle)"
)
PADDING_LOOP = re.compile(r"(?:\\;){10,}|(?:\\,){20,}|(?:\\quad){10,}")


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


def _flatten_board_text(boards: list[dict]) -> tuple[str, list[dict]]:
    """Return (concatenated cell text, list of table-line dicts)."""
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
    return all_text, table_lines


def _all_board_icons_and_text(boards: list[dict]) -> tuple[str, list[str], list[dict]]:
    """Gather every bit of text/emoji from boards, including ``icon``
    and ``iconSecondary`` fields (not picked up by `_flatten_board_text`)."""
    full_text = ""
    icon_fields: list[str] = []
    illustration_lines: list[dict] = []
    for b in boards:
        if isinstance(b.get("title"), str):
            full_text += "\n" + b["title"]
        for ln in b.get("lines") or []:
            if not isinstance(ln, dict):
                continue
            if ln.get("type") == "illustration":
                illustration_lines.append(ln)
            for key in ("icon", "iconSecondary"):
                v = ln.get(key)
                if isinstance(v, str) and v:
                    icon_fields.append(v)
                    full_text += " " + v
            for key in ("content", "explanation", "label"):
                v = ln.get(key)
                if isinstance(v, str):
                    full_text += "\n" + v
            for h in (ln.get("headers") or []):
                if isinstance(h, str):
                    full_text += "\n" + h
            for row in (ln.get("rows") or []):
                if isinstance(row, list):
                    for cell in row:
                        if isinstance(cell, str):
                            full_text += "\n" + cell
    return full_text, icon_fields, illustration_lines


def icon_checks(boards: list[dict], expected_icons: list[str]) -> list[CheckResult]:
    """Verify topic-relevant icons/illustrations are present for concrete topics."""
    out: list[CheckResult] = []
    full_text, icon_fields, illustrations = _all_board_icons_and_text(boards)

    used_structured_icon = bool(illustrations) or bool(icon_fields)
    out.append(CheckResult(
        "Le board utilise `illustration` ou le champ `icon` structure",
        used_structured_icon,
        (f"{len(illustrations)} illustration(s), "
         f"{len(icon_fields)} champ(s) icon structure(s)")
        if used_structured_icon
        else "aucune icone structuree (pas de `illustration`, pas de champ `icon`)"))

    matched = [e for e in expected_icons if e in full_text]
    out.append(CheckResult(
        f"Emoji contextuel present parmi {expected_icons}",
        bool(matched),
        f"trouves : {matched}"
        if matched else "aucun emoji attendu trouve dans le board"))

    return out


def core_checks(response: str, boards: list[dict]) -> list[CheckResult]:
    """Checks valables pour TOUS les scénarios — structuration de base."""
    out: list[CheckResult] = []

    # 1. Pas de boucle de padding LaTeX
    pad = PADDING_LOOP.search(response)
    out.append(CheckResult(
        "Pas de boucle de padding LaTeX (\\; / \\, / \\quad)",
        pad is None,
        "OK" if pad is None else f"séquence pathologique : {len(pad.group(0))} chars"))

    # 2. Au moins un <ui> show_board ou <board> émis
    has_board = bool(boards)
    out.append(CheckResult(
        "Réponse STRUCTURÉE — un bloc <ui> show_board (ou <board>) est émis",
        has_board,
        f"{len(boards)} board(s) détecté(s)"
        if has_board else "❌ réponse en texte brut, aucun tableau"))

    if not has_board:
        return out

    all_text, _ = _flatten_board_text(boards)

    # 3. Pas de commande LaTeX corrompue
    corrupted = CORRUPTED_CMD.search(all_text)
    out.append(CheckResult(
        "Pas de `\\text`/`\\times`/`\\frac` corrompu en tab/formfeed",
        corrupted is None,
        "OK" if corrupted is None else f"corruption : {corrupted.group(0)!r}"))

    # 4. Le board contient au moins UNE ligne de contenu pédagogique
    n_lines = sum(len(b["lines"]) for b in boards if isinstance(b["lines"], list))
    out.append(CheckResult(
        "Board non vide (≥ 3 lignes)",
        n_lines >= 3,
        f"{n_lines} ligne(s) au total"))

    return out


def genetics_checks(boards: list[dict], expect_4x4: bool) -> list[CheckResult]:
    """Checks génétiques : ASCII, double-barre, échiquier, etc."""
    out: list[CheckResult] = []
    all_text, table_lines = _flatten_board_text(boards)

    # G1. Pas de fuite ASCII (XY//xy) après sanitizer
    leaks = ASCII_GENETICS_LEAK.findall(all_text)
    real_leaks = [lk for lk in leaks if any(c in lk for c in "øùéÉØ")
                  or any(c.isupper() for c in lk)]
    out.append(CheckResult(
        "Aucune notation ASCII `XY//xy` résiduelle",
        not real_leaks,
        f"fuites : {real_leaks[:5]}" if real_leaks else "OK"))

    # G2. Au moins un \dfrac LaTeX dans une cellule
    has_dfrac = "\\dfrac" in all_text or "\\frac" in all_text
    out.append(CheckResult(
        "Au moins une cellule contient `\\dfrac` / `\\frac`",
        has_dfrac,
        "OK" if has_dfrac else "aucune fraction LaTeX"))

    # G3. Génotypes diploïdes (double-barre via \overline)
    has_double_bar = bool(re.search(r"\\dfrac\{[^{}]+\}\{\\overline\{", all_text))
    diploid_count = len(re.findall(
        r"\\dfrac\{[^{}]+\}\{\\overline\{[^{}]+\}\}", all_text))
    out.append(CheckResult(
        "Génotypes en notation DIPLOÏDE (\\overline{} = 2 barres)",
        has_double_bar,
        f"{diploid_count} génotype(s) diploïde(s) détecté(s)"))

    # G4. Aucun génotype haploïde dans cellules d'échiquier
    leaked = []
    for tbl in table_lines:
        for row in (tbl.get("rows") or []):
            if not isinstance(row, list):
                continue
            for cell in row[1:]:           # skip first column (gamete header)
                if not isinstance(cell, str):
                    continue
                for m in re.finditer(r"\\dfrac\{([^{}]+)\}\{([^{}]+)\}", cell):
                    denom = m.group(2)
                    if denom and "\\overline" not in denom \
                            and "\\underline" not in denom:
                        leaked.append(m.group(0))
    out.append(CheckResult(
        "Aucun génotype à une seule barre dans les cellules d'échiquier",
        not leaked,
        f"fuites : {leaked[:3]}" if leaked else "OK"))

    if expect_4x4:
        # G5. Au moins un échiquier 4×4
        big_table = any(
            len(t.get("rows") or []) >= 4 and
            all(isinstance(r, list) and len(r) >= 4 for r in (t.get("rows") or []))
            for t in table_lines
        )
        out.append(CheckResult(
            "Échiquier dihybride 4×4 (16 zygotes)",
            big_table,
            "OK" if big_table else "aucune table ≥ 4×4"))

    return out


# ─────────────────────────────────────────────────────────────────────
# LLM call
# ─────────────────────────────────────────────────────────────────────
async def call_llm(client, api_key, base_url, system_prompt, user_msg,
                   max_tokens: int = 2500):
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
# Scenarios
# ─────────────────────────────────────────────────────────────────────
@dataclass
class Scenario:
    name: str
    mode: str                      # "libre" | "coaching"
    user_msg: str
    is_genetics: bool
    expect_4x4: bool = False
    max_tokens: int = 2500
    # Coaching-only fields
    subject: str = "SVT"
    chapter_title: str = ""
    lesson_title: str = ""
    objective: str = ""
    # Contextual icons expected when topic is CONCRETE (drosophile, ADN,
    # solution, RLC…) — at least one emoji from this list must appear in
    # the board lines (as `icon` field, `iconSecondary`, inside content,
    # or via an `illustration` line).
    expected_icons: list[str] = field(default_factory=list)


SCENARIOS: list[Scenario] = [
    Scenario(
        name="A • LIBRE + Dihybride F1×F1 (échiquier 4×4)",
        mode="libre",
        user_msg=(
            "Je suis en 2BAC SVT BIOF. Explique-moi le croisement dihybride "
            "F1 × F1 entre deux pois doublement hétérozygotes (gènes G/g et "
            "L/l, indépendants). Je veux les phénotypes parents, les "
            "génotypes en notation chromosomique, les 4 gamètes avec leur "
            "pourcentage, l'échiquier de fécondation 4×4 complet, puis les "
            "proportions phénotypiques 9/16, 3/16, 3/16, 1/16. Mets tout "
            "dans un tableau récapitulatif au tableau."
        ),
        is_genetics=True,
        expect_4x4=True,
        max_tokens=3500,
    ),
    Scenario(
        name="B • LIBRE + Monohybride F1×F1 (2×2)",
        mode="libre",
        user_msg=(
            "Explique-moi un croisement monohybride simple : pois lisse (L) "
            "dominant × pois ridé (r) récessif, F1 hétérozygote, puis "
            "F1×F1. Je veux le tableau de fécondation 2×2 avec les "
            "génotypes diploïdes et les proportions 3/4 dominant, 1/4 "
            "récessif. Au tableau."
        ),
        is_genetics=True,
        expect_4x4=False,
        max_tokens=2200,
    ),
    Scenario(
        name="C • COACHING + Génétique (échiquier dihybride)",
        mode="coaching",
        subject="SVT",
        chapter_title="Génétique humaine — transmission de deux gènes",
        lesson_title="Brassage interchromosomique — dihybridisme",
        objective="Construire un échiquier de croisement dihybride pour deux gènes indépendants",
        user_msg=(
            "Donne-moi un exemple complet d'échiquier de croisement dihybride "
            "entre deux F1 hétérozygotes (gènes A/a et B/b indépendants) avec "
            "les 16 zygotes, les 4 phénotypes et leurs proportions. Mets "
            "tout au tableau."
        ),
        is_genetics=True,
        expect_4x4=True,
        max_tokens=3500,
    ),
    Scenario(
        name="D • LIBRE + Mitose (structuration pure, sans génétique)",
        mode="libre",
        user_msg=(
            "Résume-moi les 4 phases de la mitose dans un TABLEAU au "
            "tableau : prophase, métaphase, anaphase, télophase. Pour "
            "chaque phase : événements clés et schéma simplifié."
        ),
        is_genetics=False,
        expect_4x4=False,
        max_tokens=2200,
        expected_icons=["🔬", "🧬", "🧫", "🦠"],
    ),
    # ─── TOPIC CONCRETS — attendus : illustrations / icônes visuelles ───
    Scenario(
        name="E • LIBRE + Drosophile (attendu : 🪰)",
        mode="libre",
        user_msg=(
            "Pourquoi Thomas Morgan a-t-il choisi la drosophile (Drosophila "
            "melanogaster) comme organisme modèle pour la génétique ? Liste "
            "ses avantages dans un TABLEAU au tableau avec un titre et un "
            "visuel en en-tête."
        ),
        is_genetics=False,
        max_tokens=1800,
        expected_icons=["🪰", "🐛", "🐾"],
    ),
    Scenario(
        name="F • LIBRE + ADN (attendu : 🧬)",
        mode="libre",
        user_msg=(
            "Explique-moi la structure de la molécule d'ADN (désoxyribose, "
            "bases azotées, double hélice, appariement A-T / G-C) dans un "
            "TABLEAU structuré au tableau avec un visuel de l'ADN en tête."
        ),
        is_genetics=False,
        max_tokens=2000,
        expected_icons=["🧬"],
    ),
    Scenario(
        name="G • LIBRE + Solution chimique (attendu : 🧪)",
        mode="libre",
        user_msg=(
            "Je prépare une solution aqueuse d'acide chlorhydrique 0,1 mol/L. "
            "Explique-moi le calcul du pH et les étapes de préparation dans "
            "un TABLEAU au tableau avec un visuel de la solution/erlenmeyer."
        ),
        is_genetics=False,
        max_tokens=2000,
        expected_icons=["🧪", "💧"],
    ),
    Scenario(
        name="H • COACHING + Circuit RLC (attendu : ⚡)",
        mode="coaching",
        subject="Physique",
        chapter_title="Circuit RLC série — oscillations libres",
        lesson_title="Décharge d'un condensateur dans une bobine",
        objective="Établir l'équation différentielle de q(t) et identifier "
                  "les régimes",
        user_msg=(
            "Dresse-moi un tableau récapitulatif du circuit RLC série en "
            "oscillations libres : schéma, équation différentielle de q(t), "
            "pseudo-période, régimes (pseudo-périodique, critique, "
            "apériodique). Visuel du circuit en en-tête."
        ),
        is_genetics=False,
        max_tokens=2500,
        expected_icons=["⚡", "🔋"],
    ),
]


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
            subject=sc.subject,
            language="français",
            chapter_title=sc.chapter_title,
            lesson_title=sc.lesson_title,
            phase="construction",
            objective=sc.objective,
            scenario_context="Construction d'un savoir-faire BAC",
            student_name="Audit",
            proficiency="intermédiaire",
            user_query=sc.user_msg,
        )
    raise ValueError(f"unknown mode: {sc.mode}")


# ─────────────────────────────────────────────────────────────────────
async def run_scenario(client, api_key, base_url, llm: LLMService,
                       sc: Scenario) -> dict:
    sys_prompt = build_system_prompt(llm, sc)
    print(f"\n[{sc.name}]")
    print(f"  → mode={sc.mode}  max_tokens={sc.max_tokens}  "
          f"genetics={sc.is_genetics}")

    response, elapsed = await call_llm(
        client, api_key, base_url, sys_prompt, sc.user_msg,
        max_tokens=sc.max_tokens,
    )
    print(f"  ← {len(response)} chars en {elapsed:.1f}s")

    response_collapsed = _collapse_latex_padding_raw(response)
    boards = extract_ui_boards(response_collapsed) \
        + extract_board_tags(response_collapsed)

    checks = core_checks(response, boards)
    if sc.is_genetics and boards:
        checks.extend(genetics_checks(boards, expect_4x4=sc.expect_4x4))
    if sc.expected_icons and boards:
        checks.extend(icon_checks(boards, sc.expected_icons))

    passed = sum(1 for c in checks if c.passed)
    total = len(checks)
    print(f"  ✓ {passed}/{total} checks")

    return {
        "scenario": sc,
        "response": response,
        "elapsed": elapsed,
        "boards": boards,
        "checks": checks,
        "passed": passed,
        "total": total,
    }


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

    results = []
    async with httpx.AsyncClient() as client:
        for sc in SCENARIOS:
            r = await run_scenario(client, api_key, base_url, llm, sc)
            results.append(r)

    # ── Build report ────────────────────────────────────────────────
    out: list[str] = []
    out.append("# Test multi-modes — STRUCTURATION DU TABLEAU\n")
    out.append(f"_Généré le {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")
    out.append(
        "\nObjectif : vérifier que le LLM produit une réponse "
        "**STRUCTURÉE au tableau** (et non en texte brut) dans les modes "
        "`libre` et `coaching`, avec une attention particulière sur la "
        "génétique (notation diploïde double-barre).\n"
    )

    # Aggregate score
    grand_passed = sum(r["passed"] for r in results)
    grand_total = sum(r["total"] for r in results)
    full_pass = all(r["passed"] == r["total"] for r in results)
    verdict = "🎉 TOUT VERT" if full_pass else (
        f"⚠️ {grand_total - grand_passed} FAIL")
    out.append(f"\n## Score global : **{grand_passed}/{grand_total}** — {verdict}\n")

    # Summary table
    out.append("\n| # | Scénario | Mode | Score | Verdict |")
    out.append("|---|---|---|---|---|")
    for i, r in enumerate(results, 1):
        sc = r["scenario"]
        v = "✅" if r["passed"] == r["total"] else f"❌ {r['total']-r['passed']} FAIL"
        out.append(f"| {i} | {sc.name} | `{sc.mode}` | "
                   f"{r['passed']}/{r['total']} | {v} |")

    # Detailed reports per scenario
    for i, r in enumerate(results, 1):
        sc = r["scenario"]
        out.append(f"\n---\n\n## {i}. {sc.name}\n")
        out.append(f"- **Mode** : `{sc.mode}`")
        if sc.mode == "coaching":
            out.append(f"- **Chapitre** : {sc.chapter_title}")
            out.append(f"- **Leçon** : {sc.lesson_title}")
        out.append(f"- **Génétique** : {sc.is_genetics}  •  "
                   f"**Échiquier 4×4 attendu** : {sc.expect_4x4}")
        out.append(f"- **Temps LLM** : {r['elapsed']:.1f}s  •  "
                   f"**Réponse** : {len(r['response'])} chars  •  "
                   f"**Boards** : {len(r['boards'])}\n")
        out.append("**Message envoyé :**")
        out.append(f"> {sc.user_msg}\n")

        out.append("### Checks")
        out.append("| # | Vérification | Statut | Détail |")
        out.append("|---|---|---|---|")
        for j, c in enumerate(r["checks"], 1):
            flag = "✅ PASS" if c.passed else "❌ FAIL"
            out.append(f"| {j} | {c.name} | {flag} | {c.detail} |")

        if r["boards"]:
            out.append("\n### Boards (après sanitizer)")
            for k, b in enumerate(r["boards"], 1):
                out.append(f"\n**Board {k} — « {b['title']} »**\n")
                out.append("```json")
                out.append(json.dumps(b["lines"], ensure_ascii=False, indent=2))
                out.append("```")
        else:
            out.append("\n⚠️ **Aucun board détecté — réponse brute :**\n")
            out.append("```")
            out.append(r["response"][:8000]
                       + ("\n…[tronqué]" if len(r["response"]) > 8000 else ""))
            out.append("```")
            # Also show the LAST 600 chars to detect truncation by max_tokens
            tail = r["response"][-600:]
            out.append(f"\n**Fin de réponse ({len(tail)} derniers chars) :**\n")
            out.append("```")
            out.append(tail)
            out.append("```")

    out.append(f"\n---\n\n**Score final : {grand_passed}/{grand_total}** — {verdict}\n")

    report = Path(__file__).parent / "test_board_structure_report.md"
    report.write_text("\n".join(out), encoding="utf-8")
    print(f"\n[TEST] Rapport : {report}")
    print(f"[TEST] Score global : {grand_passed}/{grand_total} — {verdict}")


if __name__ == "__main__":
    asyncio.run(main())
