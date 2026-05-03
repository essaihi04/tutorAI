"""Audit all exam JSONs for raw markdown artifacts that may display poorly
in the frontend (literal ** or --- instead of rendered bold/separator).

Usage:
    python backend/scripts/audit_markdown_artifacts.py           # report only
    python backend/scripts/audit_markdown_artifacts.py --fix     # auto-clean
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMS_DIR = ROOT / 'backend' / 'data' / 'exams'

FIX = '--fix' in sys.argv
VERBOSE = '-v' in sys.argv

# Patterns considered "artifacts" when the content is shown without markdown processing.
PARTIE_PREAMBLE_WITH_SEP = re.compile(r'^(\s*\*\*Partie\s+\d[\s\S]*?)\n\s*---\s*\n([\s\S]*)$')
TRIPLE_DASH_STANDALONE = re.compile(r'(?:^|\n)\s*---\s*(?:\n|$)')
DOUBLE_STAR_UNPAIRED = re.compile(r'(?<!\*)\*\*(?!\*)')  # rough: any **

CATEGORIES = {
    'partie_preamble_in_content': 0,
    'triple_dash_separator': 0,
    'bold_markdown': 0,
    'in_correction': 0,
}


def classify(text: str, where: str, exam_path: str, loc: str, issues: list):
    """Classify problems in a single text blob."""
    if not text:
        return
    if where == 'question' and PARTIE_PREAMBLE_WITH_SEP.match(text):
        CATEGORIES['partie_preamble_in_content'] += 1
        issues.append((exam_path, loc, 'partie_preamble_in_content', text[:100]))
    # count standalone --- outside of partie preamble scenario
    if where == 'correction' and TRIPLE_DASH_STANDALONE.search(text):
        CATEGORIES['triple_dash_separator'] += 1
        issues.append((exam_path, loc, 'triple_dash_in_correction', text[:100]))
        CATEGORIES['in_correction'] += 1
    if where == 'correction':
        # Count ** markers in corrections (these will render fine if LatexRenderer handles bold)
        stars = len(DOUBLE_STAR_UNPAIRED.findall(text))
        if stars > 0 and VERBOSE:
            issues.append((exam_path, loc, f'bold_markdown_in_correction ({stars}x)', text[:80]))


def scan_exam(exam_json: Path, issues: list):
    try:
        d = json.loads(exam_json.read_text(encoding='utf-8-sig'))
    except Exception as e:
        print(f'  ERROR reading {exam_json}: {e}')
        return
    rel = str(exam_json.relative_to(ROOT))
    for part in d.get('parts', []):
        for ex_idx, ex in enumerate(part.get('exercises', [])):
            for q_idx, q in enumerate(ex.get('questions', [])):
                loc = f"ex{ex_idx+1}.q{q_idx+1} ({q.get('number','?')})"
                classify(q.get('content', ''), 'question', rel, loc, issues)
                corr = q.get('correction')
                if isinstance(corr, dict):
                    classify(corr.get('content', ''), 'correction', rel, loc + '.correction', issues)


def main():
    issues: list = []
    count = 0
    for exam_json in sorted(EXAMS_DIR.rglob('exam.json')):
        scan_exam(exam_json, issues)
        count += 1
    print(f'Scanned {count} exam files')
    print(f'Totals: {CATEGORIES}')
    print('-' * 70)
    # Group by category for readability
    by_cat: dict = {}
    for exam, loc, cat, snippet in issues:
        by_cat.setdefault(cat, []).append((exam, loc, snippet))
    for cat, items in by_cat.items():
        print(f'\n[{cat}] {len(items)} occurrences')
        for exam, loc, snippet in items[:30]:
            print(f'  {exam}  {loc}')
            if VERBOSE:
                print(f'      {snippet!r}')
        if len(items) > 30:
            print(f'  ... and {len(items) - 30} more')
    if not issues:
        print('\n✓ No artifacts detected.')


if __name__ == '__main__':
    main()
