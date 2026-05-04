"""Audit math exam JSONs for missing data and structural issues.

Checks per exercise:
  - Points mismatch (sum of question points != exercise points)
  - Empty question content / empty correction
  - Figure or schema references in content but no documents attached
  - Numbering gaps (e.g. Q1.a, Q1.b, Q2.a missing, Q3.a present)
  - Missing 'topic' tag
  - Whole-exam total-points mismatch

Usage:
    python backend/scripts/audit_math_exams.py [year] [-v]
    # e.g. python backend/scripts/audit_math_exams.py 2025
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'backend' / 'data' / 'exams' / 'mathematiques'
VERBOSE = '-v' in sys.argv
YEAR_FILTER = next((a for a in sys.argv[1:] if a.isdigit()), None)

# Only flag references to figures/schémas/graphes — NOT "tableau" because
# tables are usually inlined as markdown.
FIG_REF = re.compile(r'\b(figure|schéma|graphe|diagramme|courbe ci-)\s*\d*', re.IGNORECASE)
MD_TABLE = re.compile(r'\n\s*\|[^\n]*\|', re.MULTILINE)
NUM_RE = re.compile(r'^(\d+)([a-z])?$|^(\d+)\.([a-z0-9]+)$')


def check_numbering(qs: list) -> list[str]:
    """Flag gaps in Q-numbering."""
    issues = []
    nums = [str(q.get('number', '')) for q in qs]
    # Group by main index
    from collections import defaultdict
    groups = defaultdict(list)
    for n in nums:
        m = re.match(r'^(\d+)(?:\.(.*))?$', n)
        if m:
            groups[int(m.group(1))].append(m.group(2) or '')
    # Check main indices are contiguous 1..N
    if groups:
        main = sorted(groups.keys())
        if main != list(range(main[0], main[-1] + 1)):
            issues.append(f'non-contiguous main-question indices: {main}')
    return issues


def audit_exam(path: Path, findings: list):
    rel = str(path.relative_to(ROOT))
    try:
        d = json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception as e:
        findings.append((rel, 'FILE', f'JSON read error: {e}'))
        return

    declared_total = d.get('total_points', 20)
    computed_total = 0.0

    for pi, part in enumerate(d.get('parts', [])):
        for ei, ex in enumerate(part.get('exercises', []) or []):
            exlabel = f'ex{ei+1}: {ex.get("name","")[:60]}'
            qs = ex.get('questions', []) or []
            docs = ex.get('documents', []) or []
            topic = ex.get('topic', '')

            if not topic:
                findings.append((rel, exlabel, 'missing "topic" tag'))

            # Walk all leaf questions (flat or sub)
            leaves = []
            for q in qs:
                sub = q.get('sub_questions', []) or []
                if sub:
                    leaves.extend(sub)
                else:
                    leaves.append(q)

            # Points sum
            ex_pts = ex.get('points')
            sum_pts = sum(float(q.get('points') or 0) for q in leaves)
            if ex_pts is not None:
                computed_total += float(ex_pts)
                if abs(sum_pts - float(ex_pts)) > 0.01:
                    findings.append((rel, exlabel,
                        f'points mismatch: sum(questions)={sum_pts} but ex.points={ex_pts}'))

            # Empty content / correction
            for q in leaves:
                num = q.get('number', '?')
                content = (q.get('content') or '').strip()
                corr = q.get('correction')
                if not content:
                    findings.append((rel, exlabel, f'Q{num}: EMPTY content'))
                if not corr or (isinstance(corr, dict) and not (corr.get('content') or '').strip()):
                    findings.append((rel, exlabel, f'Q{num}: EMPTY/missing correction'))
                if (q.get('points') or 0) == 0:
                    findings.append((rel, exlabel, f'Q{num}: points=0'))

                # Figure references without docs
                if FIG_REF.search(content) and not docs:
                    findings.append((rel, exlabel,
                        f'Q{num}: references a figure/schéma but exercise has 0 documents'))

            # Numbering gaps
            for issue in check_numbering(qs):
                findings.append((rel, exlabel, issue))

    # Total points check
    if abs(computed_total - float(declared_total)) > 0.01:
        findings.append((rel, 'TOTAL',
            f'exam total mismatch: sum(ex.points)={computed_total} but declared={declared_total}'))


def main():
    findings: list = []
    files = sorted(DIR.rglob('exam.json'))
    if YEAR_FILTER:
        files = [f for f in files if YEAR_FILTER in f.parts[-2]]
    for f in files:
        audit_exam(f, findings)
    print(f'Scanned {len(files)} math exam file(s)\n')
    if not findings:
        print('✓ No issues detected.')
        return
    # Group by file
    from collections import defaultdict
    by_file: dict[str, list] = defaultdict(list)
    for rel, where, msg in findings:
        by_file[rel].append((where, msg))
    print(f'Found {len(findings)} issue(s) in {len(by_file)} file(s):\n')
    for rel, items in by_file.items():
        print(f'=== {rel}')
        for where, msg in items:
            print(f'  [{where}] {msg}')
        print()


if __name__ == '__main__':
    main()
