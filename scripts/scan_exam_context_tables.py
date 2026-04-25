"""
Scan all exam.json files under backend/data/exams and report exercises
whose `context` field contains pipe-markdown tables.

For each match, indicate whether the exercise also has image documents
(potential duplication → safe to strip) or not (table is the only source
→ must keep / render as HTML).

Usage:
    python scripts/scan_exam_context_tables.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent / "backend" / "data" / "exams"
# A pipe-markdown table needs at least 2 pipe-lines and a separator line (--- | ---).
PIPE_LINE_RE = re.compile(r"^\s*\|.+\|\s*$", re.MULTILINE)
SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", re.MULTILINE)


def has_pipe_table(text: str) -> bool:
    """Heuristic: at least one markdown separator row AND >= 2 pipe-lines."""
    if not text or "|" not in text:
        return False
    if not SEPARATOR_RE.search(text):
        return False
    return len(PIPE_LINE_RE.findall(text)) >= 2


def count_pipe_rows(text: str) -> int:
    return len(PIPE_LINE_RE.findall(text or ""))


def has_image_documents(exercise: dict) -> bool:
    docs = exercise.get("documents") or []
    return any(
        isinstance(d, dict) and (d.get("type") == "figure" or d.get("src"))
        for d in docs
    )


def describes_table(exercise: dict) -> bool:
    """True if any document description mentions a tabular figure — strong
    signal that the pipe table in the context is a duplicate of that image."""
    docs = exercise.get("documents") or []
    for d in docs:
        if not isinstance(d, dict):
            continue
        desc = (d.get("description") or "").lower()
        if "tableau" in desc or "table " in desc or "colonnes" in desc:
            return True
    return False


def scan() -> list[dict]:
    findings: list[dict] = []
    for exam_path in ROOT.rglob("exam.json"):
        try:
            exam = json.loads(exam_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[WARN] cannot parse {exam_path}: {e}")
            continue

        rel = exam_path.relative_to(ROOT)
        for part in exam.get("parts", []):
            # Two shapes: part.questions[] with context, OR part.questions[] of
            # exercise groups that themselves have context.
            # We scan any object that owns a 'context' field.
            stack: list[dict] = [part]
            while stack:
                node = stack.pop()
                if isinstance(node, dict):
                    ctx = node.get("context")
                    if isinstance(ctx, str) and has_pipe_table(ctx):
                        findings.append({
                            "file": str(rel).replace("\\", "/"),
                            "exercise": node.get("name") or node.get("id") or "?",
                            "pipe_rows": count_pipe_rows(ctx),
                            "has_image_docs": has_image_documents(node),
                            "describes_table": describes_table(node),
                        })
                    # Recurse into children
                    for v in node.values():
                        if isinstance(v, (dict, list)):
                            stack.append(v)  # type: ignore[arg-type]
                elif isinstance(node, list):
                    stack.extend([x for x in node if isinstance(x, (dict, list))])
    return findings


def main() -> None:
    rows = scan()
    if not rows:
        print("OK — aucune table pipe-markdown detectee dans les contextes.")
        return

    # Two buckets:
    dup = [r for r in rows if r["describes_table"]]  # duplicate → safe to strip
    only_in_ctx = [r for r in rows if not r["describes_table"]]

    def fmt(rows: list[dict]) -> str:
        return "\n".join(
            f"  - {r['file']:<55} | {r['exercise']:<20} | rows={r['pipe_rows']}"
            for r in rows
        )

    print("=" * 80)
    print(f"TABLES PIPE-MARKDOWN EN DOUBLON (image 'tableau' deja presente)")
    print(f"→ safe to strip from context — {len(dup)} exercice(s)")
    print("=" * 80)
    print(fmt(dup) or "  (aucun)")

    print()
    print("=" * 80)
    print(f"TABLES UNIQUEMENT DANS LE CONTEXTE (pas de doc image tabulaire)")
    print(f"→ A CONSERVER (ou rendre en HTML) — {len(only_in_ctx)} exercice(s)")
    print("=" * 80)
    print(fmt(only_in_ctx) or "  (aucun)")

    print()
    print(f"TOTAL: {len(rows)} exercice(s) avec table pipe dans context")


if __name__ == "__main__":
    main()
