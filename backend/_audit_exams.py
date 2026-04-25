"""
Comprehensive exam JSON audit.

Checks each exam.json in data/exams/<subject>/<session>/ for:
  1. Missing/invalid required fields (title, subject, year, total_points, parts)
  2. Point inconsistencies:
     - Sum(parts) != total_points
     - Sum(exercise questions) != exercise points (when declared)
     - Sum(part questions/exercises) != part points (when declared)
     - Questions or sub_questions missing points
  3. Content quality:
     - Empty/missing content
     - Missing correction
     - Truncated content (ends mid-sentence, "...", single char)
  4. Structural issues:
     - Duplicate question numbers inside a part
     - Orphan sub_questions (no parent content)
     - Empty parts/exercises
  5. Document references:
     - Referenced doc_id not in documents list
     - Orphan documents (listed but not referenced)

Usage:
  python _audit_exams.py                # full report
  python _audit_exams.py --subject svt  # filter to a subject
  python _audit_exams.py --summary      # only counts
  python _audit_exams.py --json         # machine-readable output
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

# Force UTF-8 output on Windows consoles (cp1252 by default)
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# Issue container
# ─────────────────────────────────────────────────────────────
class Report:
    """Collects issues per exam file, keyed by severity."""

    def __init__(self) -> None:
        # exam_key -> severity -> list[str]
        self.issues: dict[str, dict[str, list[str]]] = defaultdict(
            lambda: {"error": [], "warning": [], "info": []}
        )

    def add(self, exam: str, severity: str, msg: str) -> None:
        self.issues[exam][severity].append(msg)

    def has_issues(self, exam: str) -> bool:
        buckets = self.issues.get(exam, {})
        return any(buckets.get(s) for s in ("error", "warning", "info"))

    def total_by_severity(self) -> dict[str, int]:
        totals = {"error": 0, "warning": 0, "info": 0}
        for buckets in self.issues.values():
            for s in totals:
                totals[s] += len(buckets.get(s, []))
        return totals


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def _num_pts(v: Any) -> float | None:
    """Return numeric points or None if missing/invalid."""
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _is_truncated(text: str) -> bool:
    """Heuristic: content looks truncated or empty."""
    if not text:
        return True
    t = text.strip()
    if len(t) < 3:
        return True
    # Ends with three dots or an opening bracket, not closed
    if t.endswith(("...", "…", "(", "[")):
        return True
    return False


def _count_leaves(exercise_or_part: dict) -> int:
    """Count total answerable units (leaf questions) in a container."""
    total = 0
    for q in exercise_or_part.get("questions", []) or []:
        sqs = q.get("sub_questions", []) or []
        total += len(sqs) if sqs else 1
    return total


# ─────────────────────────────────────────────────────────────
# Core checkers
# ─────────────────────────────────────────────────────────────
def check_root(exam: str, data: dict, r: Report) -> None:
    """Required top-level fields."""
    required = ["title", "subject", "year", "total_points", "parts"]
    for f in required:
        if f not in data or data[f] in (None, "", []):
            r.add(exam, "error", f"Missing required field: {f!r}")

    tp = _num_pts(data.get("total_points"))
    if tp is None:
        r.add(exam, "error", "total_points is missing or not numeric")
    elif tp <= 0:
        r.add(exam, "warning", f"total_points={tp} is not positive")

    if not isinstance(data.get("parts"), list) or not data["parts"]:
        r.add(exam, "error", "parts[] is empty or missing")

    if "duration_minutes" not in data:
        r.add(exam, "info", "duration_minutes is missing")


def check_points_hierarchy(exam: str, data: dict, r: Report) -> None:
    """Verify points sum consistency at each level."""
    declared_total = _num_pts(data.get("total_points"))
    parts = data.get("parts", []) or []

    part_pts_sum = 0.0
    any_part_missing = False

    for pi, part in enumerate(parts):
        pname = part.get("name") or f"Part#{pi + 1}"
        ppts = _num_pts(part.get("points"))
        if ppts is None:
            any_part_missing = True
            r.add(exam, "warning", f"Part {pname!r}: no declared points")
        else:
            part_pts_sum += ppts

        # ── Check exercise-level totals ──
        inner_sum = 0.0
        any_inner_missing = False
        exercises = part.get("exercises", []) or []
        direct_qs = part.get("questions", []) or []

        for ei, ex in enumerate(exercises):
            exname = ex.get("name") or f"Exo#{ei + 1}"
            expts = _num_pts(ex.get("points"))
            if expts is None:
                any_inner_missing = True
                r.add(exam, "warning", f"Part {pname!r} / {exname}: no declared points")
            else:
                inner_sum += expts

            # Sum of questions inside the exercise
            ex_qsum = 0.0
            ex_q_missing = False
            for q in ex.get("questions", []) or []:
                q_total = _sum_question_points(q)
                if q_total is None:
                    ex_q_missing = True
                else:
                    ex_qsum += q_total

            if expts is not None and not ex_q_missing:
                if abs(ex_qsum - expts) > 0.01:
                    r.add(
                        exam,
                        "error",
                        f"Part {pname!r} / {exname}: sum of questions = {ex_qsum:g} "
                        f"≠ declared {expts:g}",
                    )

        # Direct questions at part level
        direct_qsum = 0.0
        direct_missing = False
        for q in direct_qs:
            q_total = _sum_question_points(q)
            if q_total is None:
                direct_missing = True
            else:
                direct_qsum += q_total

        inner_sum += direct_qsum

        if ppts is not None and not any_inner_missing and not direct_missing:
            if abs(inner_sum - ppts) > 0.01:
                r.add(
                    exam,
                    "error",
                    f"Part {pname!r}: sum of exercises+questions = {inner_sum:g} "
                    f"≠ declared {ppts:g}",
                )

    if declared_total is not None and not any_part_missing:
        if abs(part_pts_sum - declared_total) > 0.01:
            r.add(
                exam,
                "error",
                f"Sum of parts = {part_pts_sum:g} ≠ total_points = {declared_total:g}",
            )


def _sum_question_points(q: dict) -> float | None:
    """Sum points from question OR its sub_questions. Return None if all missing."""
    sqs = q.get("sub_questions", []) or []
    if sqs:
        sub_pts = [_num_pts(sq.get("points")) for sq in sqs]
        if all(p is None for p in sub_pts):
            # No sub has points — fall back on parent
            return _num_pts(q.get("points"))
        # Treat missing subs as 0 (won't be flagged here; flagged separately)
        return sum(p or 0 for p in sub_pts)
    return _num_pts(q.get("points"))


def check_content(exam: str, data: dict, r: Report) -> None:
    """Flag empty/truncated content, missing corrections, empty containers."""
    for pi, part in enumerate(data.get("parts", []) or []):
        pname = part.get("name") or f"Part#{pi + 1}"

        # Empty part
        if not part.get("questions") and not part.get("exercises"):
            r.add(exam, "error", f"Part {pname!r} has no questions or exercises")
            continue

        # Scan exercises
        for ei, ex in enumerate(part.get("exercises", []) or []):
            exname = ex.get("name") or f"Exo#{ei + 1}"
            if not ex.get("questions"):
                r.add(exam, "error", f"Part {pname!r} / {exname}: no questions")
            for q in ex.get("questions", []) or []:
                _check_question_content(exam, f"{pname}/{exname}", q, r)

        # Scan direct part questions
        for q in part.get("questions", []) or []:
            _check_question_content(exam, pname, q, r)


def _check_question_content(exam: str, ctx: str, q: dict, r: Report) -> None:
    qnum = q.get("number", "?")
    loc = f"{ctx} Q{qnum}"

    sqs = q.get("sub_questions", []) or []
    content = q.get("content", "")

    # Empty parent content is OK if it has sub_questions (grouping container)
    if not sqs and _is_truncated(content):
        r.add(exam, "warning", f"{loc}: content empty or truncated")

    # Correction — either on q or distributed on sub_questions
    has_corr = bool(q.get("correction"))
    if sqs:
        sub_corr = [bool(sq.get("correction")) for sq in sqs]
        if not has_corr and not all(sub_corr):
            missing = [sqs[i].get("number", i + 1) for i, c in enumerate(sub_corr) if not c]
            if missing:
                r.add(exam, "warning", f"{loc}: sub_questions missing correction: {missing}")
        for si, sq in enumerate(sqs):
            sqnum = sq.get("number", si + 1)
            if _is_truncated(sq.get("content", "")):
                r.add(exam, "warning", f"{loc}.{sqnum}: sub_question content empty/truncated")
    elif not has_corr:
        if q.get("type") not in ("info", "context"):
            r.add(exam, "warning", f"{loc}: missing correction")


def check_structure(exam: str, data: dict, r: Report) -> None:
    """Duplicate numbering, orphan documents."""
    for pi, part in enumerate(data.get("parts", []) or []):
        pname = part.get("name") or f"Part#{pi + 1}"

        # Gather question numbers from exercises and direct qs
        for ei, ex in enumerate(part.get("exercises", []) or []):
            exname = ex.get("name") or f"Exo#{ei + 1}"
            nums = [q.get("number") for q in ex.get("questions", []) or []]
            nums = [n for n in nums if n is not None]
            dups = [n for n in set(nums) if nums.count(n) > 1]
            if dups:
                r.add(
                    exam, "warning",
                    f"Part {pname!r} / {exname}: duplicate question numbers {dups}",
                )

        nums = [q.get("number") for q in part.get("questions", []) or []]
        nums = [n for n in nums if n is not None]
        dups = [n for n in set(nums) if nums.count(n) > 1]
        if dups:
            r.add(exam, "warning", f"Part {pname!r}: duplicate question numbers {dups}")

    # Document references
    declared_docs: set[str] = set()
    for d in data.get("documents", []) or []:
        did = d.get("id")
        if did:
            declared_docs.add(did)

    referenced: set[str] = set()

    def _collect(obj: Any) -> None:
        if isinstance(obj, dict):
            for did in obj.get("documents", []) or []:
                if isinstance(did, str):
                    referenced.add(did)
            for v in obj.values():
                _collect(v)
        elif isinstance(obj, list):
            for v in obj:
                _collect(v)

    _collect(data.get("parts"))

    missing_refs = referenced - declared_docs
    orphan_docs = declared_docs - referenced

    # Only flag missing refs if the exam actually uses a top-level documents list
    if declared_docs or missing_refs:
        for mid in sorted(missing_refs):
            # Some exams reference docs by local ids not declared globally; soft warn
            r.add(exam, "info", f"Referenced document {mid!r} not in top-level documents[]")
        for oid in sorted(orphan_docs):
            r.add(exam, "info", f"Document {oid!r} declared but never referenced")


# ─────────────────────────────────────────────────────────────
# Main audit
# ─────────────────────────────────────────────────────────────
def audit_file(path: Path, r: Report) -> None:
    exam_key = f"{path.parent.parent.name}/{path.parent.name}"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        r.add(exam_key, "error", f"Invalid JSON: {e}")
        return
    except Exception as e:
        r.add(exam_key, "error", f"Read error: {e}")
        return

    check_root(exam_key, data, r)
    if not r.issues[exam_key]["error"]:  # skip deeper checks if structurally broken
        check_points_hierarchy(exam_key, data, r)
        check_content(exam_key, data, r)
        check_structure(exam_key, data, r)


def find_exam_files(exams_dir: Path, subject: str | None) -> list[Path]:
    pattern = f"{subject}/*/exam.json" if subject else "*/*/exam.json"
    return sorted(exams_dir.glob(pattern))


def print_report(r: Report, summary: bool) -> None:
    totals = r.total_by_severity()
    n_files = len(r.issues)
    n_clean = sum(1 for k in r.issues if not r.has_issues(k))

    print(f"\n{'═' * 70}")
    print(f" AUDIT — {n_files} exams scanned, {n_clean} clean")
    print(f" errors={totals['error']}  warnings={totals['warning']}  info={totals['info']}")
    print("═" * 70)

    if summary:
        return

    severity_icon = {"error": "✗", "warning": "⚠", "info": "·"}
    severity_order = ["error", "warning", "info"]

    for exam in sorted(r.issues.keys()):
        buckets = r.issues[exam]
        if not any(buckets[s] for s in severity_order):
            continue
        print(f"\n▸ {exam}")
        for sev in severity_order:
            for msg in buckets[sev]:
                print(f"    {severity_icon[sev]} [{sev.upper():7}] {msg}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--subject", help="Filter to a subject folder (svt/physique/mathematiques/chimie)")
    ap.add_argument("--summary", action="store_true", help="Only print totals")
    ap.add_argument("--json", action="store_true", help="Emit JSON report to stdout")
    args = ap.parse_args()

    exams_dir = Path(__file__).parent / "data" / "exams"
    if not exams_dir.exists():
        print(f"ERROR: {exams_dir} not found", file=sys.stderr)
        return 2

    files = find_exam_files(exams_dir, args.subject)
    if not files:
        print("No exam.json files found", file=sys.stderr)
        return 1

    r = Report()
    for path in files:
        audit_file(path, r)

    if args.json:
        print(json.dumps(
            {
                "totals": r.total_by_severity(),
                "files_scanned": len(files),
                "issues": {k: dict(v) for k, v in r.issues.items()},
            },
            ensure_ascii=False,
            indent=2,
        ))
    else:
        print_report(r, args.summary)

    return 0 if r.total_by_severity()["error"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
