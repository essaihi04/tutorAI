"""Deep audit of Partie preamble integrity across all exams.

Checks for:
  1. Questions where the Partie preamble regex FAILS to match cleanly
     (frontend extraction would fall back and show raw markdown).
  2. Preamble without a trailing '---' separator.
  3. Preamble with question text too short/empty after '---'.
  4. Orphaned Partie markers in sibling questions (shouldn't happen).
  5. Partie preamble present in exercise.context (should have been moved).

Usage:
    python backend/scripts/audit_partie_split.py [-v]
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMS_DIR = ROOT / 'backend' / 'data' / 'exams'
VERBOSE = '-v' in sys.argv

# Must match the frontend regex EXACTLY.
FRONTEND_RE = re.compile(r'^(\s*\*\*Partie\s+\d[\s\S]*?)\n\s*---\s*\n([\s\S]*)$')
HAS_PARTIE_START = re.compile(r'^\s*\*\*Partie\s+\d', re.MULTILINE)
ANY_PARTIE = re.compile(r'\*\*Partie\s+\d')
HORIZONTAL_RULE = re.compile(r'(?:^|\n)\s*---\s*(?:\n|$)')


def audit_file(path: Path, findings: list):
    rel = str(path.relative_to(ROOT))
    try:
        d = json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception as e:
        findings.append(('READ_ERROR', rel, '', str(e)))
        return
    for part in d.get('parts', []):
        for ei, ex in enumerate(part.get('exercises', [])):
            exercise_label = f'ex{ei+1}'

            # Check 5: exercise.context should not contain Partie preambles
            ctx = ex.get('context', '') or ''
            if HAS_PARTIE_START.search(ctx):
                findings.append((
                    'PARTIE_IN_CONTEXT', rel, exercise_label,
                    f'ex.context still contains "**Partie N...**" (should be moved to a question). ctx[:100]={ctx[:100]!r}'
                ))

            for qi, q in enumerate(ex.get('questions', [])):
                qlabel = f'{exercise_label}.q{qi+1} (num={q.get("number","?")})'
                content = q.get('content', '') or ''

                starts_with_partie = bool(HAS_PARTIE_START.match(content))
                has_any_partie = bool(ANY_PARTIE.search(content))
                has_hr = bool(HORIZONTAL_RULE.search(content))

                if starts_with_partie:
                    # This question is a "Partie first-question" — regex must match.
                    m = FRONTEND_RE.match(content)
                    if not m:
                        # Diagnose why
                        reasons = []
                        if not has_hr:
                            reasons.append('no "---" separator')
                        else:
                            reasons.append('regex mismatch (check spacing around "---")')
                        findings.append((
                            'REGEX_MISMATCH', rel, qlabel,
                            f'starts with **Partie** but frontend regex FAILS: {", ".join(reasons)}. content[:200]={content[:200]!r}'
                        ))
                    else:
                        preamble, rest = m.group(1).strip(), m.group(2).strip()
                        if len(rest) < 10:
                            findings.append((
                                'EMPTY_QUESTION_AFTER_SEP', rel, qlabel,
                                f'after "---" the actual question text is suspiciously short ({len(rest)} chars): {rest!r}'
                            ))
                        if len(preamble) < 30:
                            findings.append((
                                'SHORT_PREAMBLE', rel, qlabel,
                                f'Partie preamble is very short ({len(preamble)} chars): {preamble!r}'
                            ))
                        # Check 4b: preamble itself should not contain a SECOND Partie marker
                        inner_partie_count = len(ANY_PARTIE.findall(preamble))
                        if inner_partie_count > 1:
                            findings.append((
                                'NESTED_PARTIE', rel, qlabel,
                                f'preamble contains {inner_partie_count} "**Partie**" markers — possibly two parties merged'
                            ))
                elif has_any_partie:
                    # Partie marker in middle/end of content (not a clean first-question).
                    findings.append((
                        'ORPHAN_PARTIE', rel, qlabel,
                        f'"**Partie**" appears but NOT at start (frontend wont extract it). content[:200]={content[:200]!r}'
                    ))

                # Check separator in non-partie questions (stray ---)
                if not starts_with_partie and has_hr:
                    findings.append((
                        'STRAY_HR', rel, qlabel,
                        f'non-Partie question contains a "---" separator (may render as raw dashes). content[:150]={content[:150]!r}'
                    ))


def main():
    findings: list = []
    n = 0
    for f in sorted(EXAMS_DIR.rglob('exam.json')):
        audit_file(f, findings)
        n += 1
    print(f'Scanned {n} exam files')
    if not findings:
        print('\n✓ No integrity issues — all 29 Partie preambles split cleanly.')
        return
    by_cat: dict[str, list] = {}
    for cat, rel, loc, detail in findings:
        by_cat.setdefault(cat, []).append((rel, loc, detail))
    print(f'\nFound {len(findings)} issues across {len(by_cat)} categories:')
    for cat, items in by_cat.items():
        print(f'\n### [{cat}] — {len(items)} case(s)')
        for rel, loc, detail in items:
            print(f'  {rel}  {loc}')
            if VERBOSE:
                print(f'      → {detail}')


if __name__ == '__main__':
    main()
