"""Audit physique (PC) exam JSONs for missing data and structural issues.

Extends the math audit with PC-specific checks:
  - Bundled vrai/faux questions (several a-/b-/c- items + no sub_questions
    and no correct_answer → UI shows one Vrai/Faux selector)
  - Multiple `**Partie N**` headers embedded inside a single ex.context
    (= unsplit parties, student sees all preambles bundled)
  - Type=vrai_faux or qcm without correct_answer
  - Figure references without attached documents

Usage:
    python backend/scripts/audit_physique_exams.py [year] [-v]
"""
from __future__ import annotations
import json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'backend' / 'data' / 'exams' / 'physique'
VERBOSE = '-v' in sys.argv
YEAR_FILTER = next((a for a in sys.argv[1:] if a.isdigit()), None)

FIG_REF = re.compile(
    r'\b(figure|schéma|graphe|diagramme|courbe ci-|ci-contre|ci-dessous)\s*\d*',
    re.IGNORECASE,
)
PARTIE_RE = re.compile(r'\*\*Partie\s+([IVX\d]+)[^*]*\*\*')
BUNDLED_VF_RE = re.compile(r'^\s*[a-z]-\s', re.MULTILINE)


def _get_correct_answer(q: dict) -> str | None:
    v = q.get('correct_answer')
    if v:
        return v
    corr = q.get('correction') or {}
    if isinstance(corr, dict):
        return corr.get('correct_answer')
    return None


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
            ctx = ex.get('context', '') or ''

            # Unsplit Parties: context has ≥2 **Partie N** markers.
            parties_in_ctx = PARTIE_RE.findall(ctx)
            if len(parties_in_ctx) >= 2:
                findings.append((rel, exlabel,
                    f'unsplit: ex.context bundles {len(parties_in_ctx)} Parties {parties_in_ctx}'))

            # Walk all leaf questions (flat or sub)
            leaves = []
            for q in qs:
                sub = q.get('sub_questions', []) or []
                if sub:
                    leaves.extend(sub)
                else:
                    leaves.append(q)

            # Points sum vs exercise declared points
            ex_pts = ex.get('points')
            sum_pts = sum(float(q.get('points') or 0) for q in leaves)
            if ex_pts is not None:
                computed_total += float(ex_pts)
                if abs(sum_pts - float(ex_pts)) > 0.01:
                    findings.append((rel, exlabel,
                        f'points mismatch: sum(questions)={sum_pts} but ex.points={ex_pts}'))

            for q in leaves:
                num = q.get('number', '?')
                content = (q.get('content') or '').strip()
                corr = q.get('correction')
                qtype = q.get('type', 'open')

                if not content:
                    findings.append((rel, exlabel, f'Q{num}: EMPTY content'))

                corr_empty = (
                    not corr
                    or (isinstance(corr, dict)
                        and not (corr.get('content') or '').strip()
                        and not corr.get('correct_answer')
                        and not corr.get('correct_pairs'))
                )
                if corr_empty and not q.get('correct_answer') and not q.get('correct_pairs'):
                    findings.append((rel, exlabel, f'Q{num}: EMPTY/missing correction'))

                if (q.get('points') or 0) == 0:
                    findings.append((rel, exlabel, f'Q{num}: points=0'))

                # Figure references without docs — only on the question itself,
                # because a Partie preamble living on Q1 but referencing fig4
                # (used by Q3) would not have docs set on the owner if we
                # look at individual questions. So we check docs at the
                # exercise level instead: if ANY question references figures
                # and ex has no docs → flag.
                # (Already emitted per-question below.)

                # Closed-form without correct_answer
                if qtype in ('qcm', 'vrai_faux'):
                    if not _get_correct_answer(q):
                        findings.append((rel, exlabel,
                            f'Q{num}: type={qtype} but correct_answer missing'))

                # Bundled vrai/faux: single vf question with multiple items
                if qtype == 'vrai_faux' and not q.get('sub_questions'):
                    items = len(BUNDLED_VF_RE.findall(content))
                    if items >= 2 and '.' not in str(num):
                        findings.append((rel, exlabel,
                            f'Q{num}: bundled vrai/faux ({items} items in content)'))

            # Exercise-wide figure references without any docs
            all_text = ctx + '\n' + '\n'.join((q.get('content') or '') for q in leaves)
            fig_mentions = FIG_REF.findall(all_text)
            if fig_mentions and not docs:
                findings.append((rel, exlabel,
                    f'{len(fig_mentions)} figure/schéma reference(s) but 0 documents attached'))

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

    print(f'Scanned {len(files)} physique exam file(s)\n')
    if not findings:
        print('OK  No issues detected.')
        return

    by_file: dict[str, list] = defaultdict(list)
    for rel, where, msg in findings:
        by_file[rel].append((where, msg))
    print(f'Found {len(findings)} issue(s) in {len(by_file)} file(s):\n')
    for rel, items in sorted(by_file.items()):
        print(f'=== {rel}')
        for where, msg in items:
            print(f'  [{where}] {msg}')
        print()


if __name__ == '__main__':
    main()
