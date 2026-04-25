"""
Scan all exam.json files for misaligned document numbering.

For each exercise with a `documents[]` array, we check that for every
document:
  1. The `title` number ("Document N") matches the number that appears in
     the `src` filename (e.g. assets/doc3p5.png → "Document 3").
  2. The array order matches the title numbering (Document 1 first, etc.).

When a mismatch is found, we report the exercise and suggest a reorder.

Usage:
    python scripts/scan_document_numbering.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent / "backend" / "data" / "exams"

TITLE_NUM_RE = re.compile(r"Document\s*(\d+)", re.IGNORECASE)
# Capture the LEADING digit group in the filename e.g. doc3p5.png → 3
SRC_NUM_RE = re.compile(r"doc(\d+)p\d+", re.IGNORECASE)


def num_from_title(title: str) -> int | None:
    if not title:
        return None
    m = TITLE_NUM_RE.search(title)
    return int(m.group(1)) if m else None


def num_from_src(src: str) -> int | None:
    if not src:
        return None
    m = SRC_NUM_RE.search(src)
    return int(m.group(1)) if m else None


def scan() -> list[dict]:
    findings: list[dict] = []
    for exam_path in ROOT.rglob("exam.json"):
        try:
            exam = json.loads(exam_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[WARN] cannot parse {exam_path}: {e}")
            continue

        rel = exam_path.relative_to(ROOT)

        # Walk any node with a 'documents' list that looks like figure list
        stack: list[dict] = [exam]
        visited_lists = []
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                docs = node.get("documents")
                if (
                    isinstance(docs, list)
                    and docs
                    and all(isinstance(d, dict) for d in docs)
                    and any(d.get("src") for d in docs)
                    and id(docs) not in visited_lists
                ):
                    visited_lists.append(id(docs))
                    exercise_name = node.get("name") or node.get("id") or "?"
                    issues = []
                    for i, d in enumerate(docs, start=1):
                        t_num = num_from_title(d.get("title", ""))
                        s_num = num_from_src(d.get("src", ""))
                        pos = i
                        # Issue 1: title vs src number mismatch
                        if t_num is not None and s_num is not None and t_num != s_num:
                            issues.append({
                                "kind": "title_src_mismatch",
                                "id": d.get("id"),
                                "title": d.get("title"),
                                "src": d.get("src"),
                                "title_num": t_num,
                                "src_num": s_num,
                            })
                        # Issue 2: title number vs array position
                        if t_num is not None and t_num != pos:
                            issues.append({
                                "kind": "position_mismatch",
                                "id": d.get("id"),
                                "title": d.get("title"),
                                "position": pos,
                                "title_num": t_num,
                            })
                    if issues:
                        findings.append({
                            "file": str(rel).replace("\\", "/"),
                            "exercise": exercise_name,
                            "issues": issues,
                        })
                for v in node.values():
                    if isinstance(v, (dict, list)):
                        stack.append(v)  # type: ignore[arg-type]
            elif isinstance(node, list):
                stack.extend([x for x in node if isinstance(x, (dict, list))])
    return findings


def main() -> None:
    rows = scan()
    if not rows:
        print("OK — aucun desalignement de numerotation detecte.")
        return

    print("=" * 80)
    print(f"{len(rows)} exercice(s) avec un probleme de numerotation de document")
    print("=" * 80)

    for r in rows:
        print()
        print(f"  FILE    : {r['file']}")
        print(f"  EXERCICE: {r['exercise']}")
        for iss in r["issues"]:
            if iss["kind"] == "title_src_mismatch":
                print(
                    f"    - TITRE/SRC :: id={iss['id']}  "
                    f"title='{iss['title']}' (#{iss['title_num']}) "
                    f"src={iss['src']} (#{iss['src_num']})"
                )
            else:
                print(
                    f"    - ORDRE     :: id={iss['id']}  "
                    f"title='{iss['title']}' en position {iss['position']}"
                )


if __name__ == "__main__":
    main()
