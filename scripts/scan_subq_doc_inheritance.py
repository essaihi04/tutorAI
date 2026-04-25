"""Scan exam.json files to list cases that were affected by the sub-question
document-inheritance bug.

Before the fix, a sub-question without its own `documents` field inherited the
entire exercise doc list, ignoring the narrower scope set on the parent
question. This script reports every such parent/sub-question pair so you can
verify visually that the UI now shows only the correct documents.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "backend" / "data" / "exams"


def scan() -> list[dict]:
    rows: list[dict] = []
    for path in ROOT.rglob("exam.json"):
        try:
            exam = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[WARN] {path}: {e}")
            continue

        rel = str(path.relative_to(ROOT)).replace("\\", "/")

        for part in exam.get("parts", []) or []:
            for ex in part.get("exercises", []) or []:
                ex_docs = ex.get("documents") or []
                ex_doc_count = len(ex_docs)
                if ex_doc_count == 0:
                    continue
                for q in ex.get("questions", []) or []:
                    sqs = q.get("sub_questions") or []
                    if not sqs:
                        continue
                    parent_refs = q.get("documents")
                    # Bug was visible ONLY when parent explicitly narrowed scope
                    if not parent_refs:
                        continue
                    parent_count = len(parent_refs) if isinstance(parent_refs, list) else 0
                    if parent_count == 0 or parent_count >= ex_doc_count:
                        continue  # parent did not narrow the scope
                    for sq in sqs:
                        if sq.get("documents"):
                            continue  # sub-question had its own explicit list
                        rows.append({
                            "file": rel,
                            "exercise": ex.get("name", "?"),
                            "question": q.get("number", q.get("content", "")[:40]),
                            "sub_question": sq.get("number", sq.get("content", "")[:40]),
                            "parent_docs": parent_refs,
                            "exercise_doc_count": ex_doc_count,
                        })
    return rows


def main() -> None:
    rows = scan()
    if not rows:
        print("Aucun cas trouve — le bug n'etait visible nulle part.")
        return
    print(f"{len(rows)} sous-question(s) affectee(s) par le bug (desormais corrigees) :")
    print("=" * 80)
    for r in rows:
        print()
        print(f"  {r['file']}")
        print(f"    {r['exercise']} | Q{r['question']} → sous-q {r['sub_question']}")
        print(f"    parent.documents = {r['parent_docs']}  "
              f"(au lieu de {r['exercise_doc_count']} docs d'exercice)")


if __name__ == "__main__":
    main()
