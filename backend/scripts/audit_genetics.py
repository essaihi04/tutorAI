"""
Audit du PROTOCOLE GÉNÉTIQUE — vérifie en LIVE que le LLM produit
un rendu tableau (échiquier de croisement) conforme au BAC SVT BIOF
marocain pour les questions de génétique mendélienne.

Pour chaque question génétique :
1. Construit le prompt libre (qui injecte GENETICS_BOARD_PROTOCOL).
2. Appelle DeepSeek.
3. Vérifie que la réponse contient :
   - Au moins un bloc <ui>{...show_board...}</ui>
   - Au moins UNE ligne `"type":"table"` avec `headers` + `rows`
     (= échiquier de fécondation OBLIGATOIRE)
   - Une notation chromosomique LaTeX `\\dfrac{...}{...}` (génotypes)
   - PAS de texte inline interdit (« Parents : [.. ; ..] // Génotypes : .. // .. »)
   - PAS de fécondation textuelle « X × Y → Z »

Sortie : scripts/audit_genetics_report.md
Usage  : python scripts/audit_genetics.py [--limit N]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import time
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

# Stub heavy ML deps before importing LLMService
import types as _types
_stub_rag = _types.ModuleType("app.services.rag_service")


class _NoopRag:
    def build_grounded_context(self, *a, **kw): return ""
    def search(self, *a, **kw): return []


def _get_rag_service():  # noqa
    return _NoopRag()


_stub_rag.get_rag_service = _get_rag_service  # type: ignore
sys.modules["app.services.rag_service"] = _stub_rag

from app.config import get_settings  # noqa: E402
from app.services.llm_service import LLMService  # noqa: E402

LLMService._ensure_rag_initialized = lambda self: None  # type: ignore


# ── Test cases — questions BAC génétique ──────────────────────────────
@dataclass
class GeneticsCase:
    label: str
    query: str
    must_have_table: bool = True
    expected_min_table_cells: int = 4  # F1×F1 = 4 cases minimum (mono)


CASES: list[GeneticsCase] = [
    GeneticsCase(
        "Monohybridisme F1×F1",
        "Chez la drosophile, le caractère couleur du corps présente "
        "deux phénotypes : corps gris [g+] dominant et corps noir [g] récessif. "
        "On croise un mâle homozygote gris avec une femelle homozygote noire. "
        "Donne l'interprétation chromosomique du croisement P1×P2 puis F1×F1.",
        expected_min_table_cells=4,
    ),
    GeneticsCase(
        "Dihybridisme indépendant — test-cross",
        "On considère deux gènes indépendants chez la drosophile : "
        "couleur du corps (gris [g+] dominant / noir [g]) et longueur des ailes "
        "(longues [vg+] dominant / vestigiales [vg]). Réalise le test-cross "
        "d'un individu F1 double hétérozygote avec un double homozygote récessif. "
        "Donne l'interprétation chromosomique complète.",
        expected_min_table_cells=4,
    ),
    GeneticsCase(
        "Dihybridisme gènes liés (linkage)",
        "Chez la drosophile, le gène de la couleur du corps et le gène de la "
        "longueur des ailes sont LIÉS sur le même chromosome, à une distance "
        "de 17 centiMorgans. On effectue un test-cross. Donne l'interprétation "
        "chromosomique avec les pourcentages de gamètes parentaux et recombinés.",
        expected_min_table_cells=4,
    ),
]


# ── Patterns d'évaluation ─────────────────────────────────────────────
RE_UI_BLOCK = re.compile(r"<ui>\s*(.*?)\s*</ui>", re.DOTALL)

# Texte inline interdit : style « Parents : [vg ; b] × [vg+ ; b+] »
# détecté HORS de tout bloc <ui>.
RE_INLINE_PARENTS = re.compile(
    r"(?im)^\s*(?:parents?|p\d?)\s*[:.\-]\s*\[[^\]]+\]\s*[×x]\s*\[[^\]]+\]"
)
# « vg b // vg b » (fraction simulée en ASCII)
RE_INLINE_FRACTION = re.compile(r"[A-Za-z+]+\s+[A-Za-z+]+\s*//\s*[A-Za-z+]+\s+[A-Za-z+]+")
# Fécondation textuelle « X × Y → Z »
RE_INLINE_FECOND = re.compile(r"\[[^\]]+\]\s*[×x]\s*\[[^\]]+\]\s*[→➔]")


@dataclass
class CaseResult:
    case: GeneticsCase
    response: str
    elapsed_s: float
    has_ui: bool = False
    has_table: bool = False
    table_cells: int = 0
    has_dfrac: bool = False
    inline_violations: list[str] = field(default_factory=list)
    parse_error: Optional[str] = None

    @property
    def passed(self) -> bool:
        if self.parse_error:
            return False
        if not self.has_ui or not self.has_table:
            return False
        if self.case.must_have_table and self.table_cells < self.case.expected_min_table_cells:
            return False
        if not self.has_dfrac:
            return False
        if self.inline_violations:
            return False
        return True


def _strip_ui_blocks(text: str) -> str:
    """Return the text with all <ui>…</ui> blocks removed, so we can hunt
    inline violations only in the *spoken* portion."""
    return RE_UI_BLOCK.sub(" ", text)


def evaluate(case: GeneticsCase, response: str) -> CaseResult:
    res = CaseResult(case=case, response=response, elapsed_s=0.0)
    if not response or response.startswith("[ERROR"):
        res.parse_error = response or "empty"
        return res

    # 1. Extract ALL <ui> blocks
    ui_blocks = RE_UI_BLOCK.findall(response)
    res.has_ui = len(ui_blocks) > 0

    # 2. Walk every block, look for show_board with at least one
    # type=table line whose rows×cols >= expected_min_table_cells.
    max_cells = 0
    has_dfrac = False
    for raw in ui_blocks:
        try:
            obj = json.loads(raw)
        except Exception:
            # Tolerate minor format issues — try a permissive extraction
            if "\\dfrac" in raw:
                has_dfrac = True
            if '"type":"table"' in raw or '"type": "table"' in raw:
                res.has_table = True
            continue

        actions = obj.get("actions") or []
        for act in actions:
            if act.get("action") != "show_board":
                continue
            payload = act.get("payload") or {}
            for line in payload.get("lines") or []:
                if line.get("type") == "table":
                    res.has_table = True
                    rows = line.get("rows") or []
                    headers = line.get("headers") or []
                    n_cols = max((len(r) if isinstance(r, list) else 0) for r in rows) if rows else len(headers)
                    n_rows = len(rows)
                    max_cells = max(max_cells, n_cols * n_rows)
                content = str(line.get("content", ""))
                if "\\dfrac" in content or "\\frac" in content:
                    has_dfrac = True
    res.table_cells = max_cells
    res.has_dfrac = has_dfrac

    # 3. Inline violations: only in text OUTSIDE <ui> blocks
    spoken = _strip_ui_blocks(response)
    if RE_INLINE_PARENTS.search(spoken):
        res.inline_violations.append("inline-parents")
    if RE_INLINE_FRACTION.search(spoken):
        res.inline_violations.append("inline-fraction (// notation)")
    if RE_INLINE_FECOND.search(spoken):
        res.inline_violations.append("inline-fecondation (→)")

    return res


async def run_case(client, api_key, base_url, system_prompt, case: GeneticsCase) -> CaseResult:
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": case.query},
        ],
        "temperature": 0.3,
        "max_tokens": 2200,
        "stream": False,
    }
    t0 = time.time()
    try:
        resp = await client.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=120.0,
        )
        resp.raise_for_status()
        content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "") or ""
    except Exception as e:
        content = f"[ERROR: {e}]"
    elapsed = time.time() - t0
    r = evaluate(case, content)
    r.elapsed_s = elapsed
    return r


async def main(limit: Optional[int] = None):
    settings = get_settings()
    api_key = getattr(settings, "deepseek_api_key", None) or getattr(settings, "DEEPSEEK_API_KEY", None)
    base_url = getattr(settings, "deepseek_base_url", None) or "https://api.deepseek.com/v1"
    if not api_key:
        print("[FATAL] DEEPSEEK_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    cases = CASES[:limit] if limit else CASES
    print(f"[AUDIT-GENETICS] Running {len(cases)} cases against DeepSeek …")
    llm = LLMService()

    results: list[CaseResult] = []
    async with httpx.AsyncClient() as client:
        for i, case in enumerate(cases, 1):
            system_prompt = llm.build_libre_prompt(
                language="français",
                student_name="Audit",
                proficiency="intermédiaire",
                user_query=case.query,
            )
            # Sanity check: protocol must be present in prompt.
            assert "PROTOCOLE_GÉNÉTIQUE" in system_prompt, (
                f"Genetics protocol NOT injected for case '{case.label}'"
            )
            r = await run_case(client, api_key, base_url, system_prompt, case)
            results.append(r)
            status = "PASS" if r.passed else "FAIL"
            note_parts = []
            if not r.has_ui:
                note_parts.append("no-<ui>")
            if not r.has_table:
                note_parts.append("no-table")
            else:
                note_parts.append(f"cells={r.table_cells}")
            if not r.has_dfrac:
                note_parts.append("no-dfrac")
            if r.inline_violations:
                note_parts.append("inline=" + ",".join(r.inline_violations))
            print(f"[{i}/{len(cases)}] {status} ({r.elapsed_s:5.1f}s) {case.label} | {' | '.join(note_parts)}")

    passed_n = sum(1 for r in results if r.passed)
    failed_n = len(results) - passed_n

    out: list[str] = []
    out.append("# Audit Protocole Génétique BAC SVT BIOF — Rapport\n")
    out.append(f"_Généré le {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")
    out.append(f"\n## Résumé\n")
    out.append(f"- **Total cas** : {len(results)}")
    out.append(f"- **Réussis** : {passed_n} ({100*passed_n/max(len(results),1):.0f}%)")
    out.append(f"- **Échecs** : {failed_n}\n")
    out.append("Critères de réussite (TOUS requis) :")
    out.append("- au moins un bloc `<ui>{…show_board…}</ui>`")
    out.append("- au moins une ligne `type:table` (échiquier) avec ≥ 4 cellules")
    out.append("- au moins une notation `\\dfrac{…}{…}` (génotype chromosomique)")
    out.append("- AUCUN texte inline interdit (« Parents : [..] × [..] », « // », « → »)\n")

    out.append("\n## Détails par cas\n")
    for r in results:
        flag = "PASS" if r.passed else "FAIL"
        out.append(f"### [{flag}] {r.case.label}")
        out.append(f"- query : `{r.case.query[:140]}…`")
        out.append(f"- has_ui : {r.has_ui}")
        out.append(f"- has_table : {r.has_table} (cells={r.table_cells})")
        out.append(f"- has_dfrac : {r.has_dfrac}")
        out.append(f"- inline_violations : {r.inline_violations or '∅'}")
        out.append(f"- elapsed : {r.elapsed_s:.1f}s")
        if r.parse_error:
            out.append(f"- parse_error : {r.parse_error}")
        out.append("\n**Réponse LLM (extrait 2.5k char) :**\n")
        snippet = (r.response or "")[:2500].strip()
        if len(r.response or "") > 2500:
            snippet += "\n…[tronqué]"
        out.append("```\n" + snippet + "\n```\n")

    report_path = Path(__file__).parent / "audit_genetics_report.md"
    report_path.write_text("\n".join(out), encoding="utf-8")
    print(f"\n[AUDIT-GENETICS] Rapport : {report_path}")
    print(f"[AUDIT-GENETICS] Score : {passed_n}/{len(results)} ({100*passed_n/max(len(results),1):.0f}%)")
    sys.exit(0 if failed_n == 0 else 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    asyncio.run(main(limit=args.limit))
