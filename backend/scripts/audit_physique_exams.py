"""Audit physique (PC) exam JSONs for missing data and structural issues.

Checks:
  1. Open questions that are actually QCM  (| A | ... | B | ... | C | ... pattern)
  2. Open questions that look like Vrai/Faux (a- / b- / c- items, no sub_questions)
  3. QCM/vrai_faux without correct_answer
  4. Multiple **Partie N** headers bundled in ex.context (unsplit parties)
  5. Bundled vrai/faux (several a-/b-/c- assertions in one vf question)
  6. Zero-point questions
  7. Empty content or correction
  8. Figure references with no attached documents
  9. Exercise points ≠ sum of question points
  10. Exam declared total ≠ sum of exercise points

Usage:
    python backend/scripts/audit_physique_exams.py [year] [-v]
    python backend/scripts/audit_physique_exams.py 2022        # one year
    python backend/scripts/audit_physique_exams.py 2022 ratt   # one session
"""
from __future__ import annotations
import json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'backend' / 'data' / 'exams' / 'physique'
VERBOSE = '-v' in sys.argv
YEAR_FILTER = next((a for a in sys.argv[1:] if a.isdigit()), None)
SESSION_FILTER = next((a for a in sys.argv[1:] if not a.isdigit() and not a.startswith('-')), None)

# ── Regex patterns ───────────────────────────────────────────────────────────
FIG_REF = re.compile(
    r'\b(figure|schéma|graphe|diagramme|courbe ci-|ci-contre|ci-dessous)\s*\d*',
    re.IGNORECASE,
)
PARTIE_RE = re.compile(r'\*\*Partie\s+([IVX\d]+)[^*]*\*\*')
BUNDLED_VF_RE = re.compile(r'^\s*[a-z]-\s', re.MULTILINE)

# A pipe-row with at least 2 labelled choices:  | A | ... | B | ...
# Matches both inline (single row) and multi-row 2×2 grids.
QCM_TABLE_RE = re.compile(
    r'\|\s*[Aa]\s*\|.+\|\s*[Bb]\s*\|',
    re.DOTALL,
)

# Correction text that references a specific answer: "réponse correcte est B"
CORR_ANSWER_RE = re.compile(
    r'(r[eé]ponse\s+(correcte\s+)?est\s+([A-D])|correct[e]?\s+:\s+([A-D]))',
    re.IGNORECASE,
)


def _get_correct_answer(q: dict) -> bool:
    """Return True if a usable correct_answer is set (including index 0)."""
    v = q.get('correct_answer')
    if v is not None:
        return True
    corr = q.get('correction') or {}
    if isinstance(corr, dict):
        ca = corr.get('correct_answer')
        if ca is not None:
            return True
        cp = corr.get('correct_pairs')
        if cp:
            return True
    return False


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

                # ── Check 1: open question that looks like a QCM ──────────
                if qtype == 'open' and QCM_TABLE_RE.search(content):
                    # How many labelled choices A/B/C/D are in the table?
                    n_choices = len(re.findall(r'\|\s*[A-D]\s*\|', content))
                    # Does the correction name a specific answer?
                    corr_text = ''
                    if isinstance(corr, dict):
                        corr_text = corr.get('content', '') or ''
                    elif isinstance(corr, str):
                        corr_text = corr
                    hint = ''
                    m = CORR_ANSWER_RE.search(corr_text)
                    if m:
                        ans = m.group(3) or m.group(4) or ''
                        hint = f' → correct={ans}'
                    findings.append((rel, exlabel,
                        f'Q{num}: type=open but contains QCM table ({n_choices} choices){hint} [CONVERT TO QCM]'))

                # ── Check 2: open question that looks like Vrai/Faux ─────
                if qtype == 'open' and not q.get('sub_questions'):
                    vf_items = BUNDLED_VF_RE.findall(content)
                    if len(vf_items) >= 2:
                        findings.append((rel, exlabel,
                            f'Q{num}: type=open with {len(vf_items)} vrai/faux items (a-/b-/c-) [CONVERT TO VRAI_FAUX]'))

                # ── Check 3: QCM/vrai_faux without correct_answer ────────
                if qtype in ('qcm', 'vrai_faux'):
                    if not _get_correct_answer(q):  # _get_correct_answer handles index=0
                        findings.append((rel, exlabel,
                            f'Q{num}: type={qtype} but correct_answer missing'))

                # ── Check 4: Bundled vrai/faux already typed correctly ───
                if qtype == 'vrai_faux' and not q.get('sub_questions'):
                    items = len(BUNDLED_VF_RE.findall(content))
                    if items >= 2 and '.' not in str(num):
                        findings.append((rel, exlabel,
                            f'Q{num}: bundled vrai/faux ({items} items in content) [SPLIT]'))

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
        files = [f for f in files if YEAR_FILTER in str(f.parent.name)]
    if SESSION_FILTER:
        files = [f for f in files if SESSION_FILTER.lower() in str(f.parent.name).lower()]
    for f in files:
        audit_exam(f, findings)

    print(f'Scanned {len(files)} physique exam file(s)\n')
    if not findings:
        print('OK  No issues detected.')
        return

    # ── Count by category ────────────────────────────────────────────────
    cat_counts: dict[str, int] = defaultdict(int)
    for _, _, msg in findings:
        if 'CONVERT TO QCM' in msg:
            cat_counts['open→QCM'] += 1
        elif 'CONVERT TO VRAI_FAUX' in msg:
            cat_counts['open→VF'] += 1
        elif 'SPLIT' in msg:
            cat_counts['bundled_vf'] += 1
        elif 'unsplit' in msg:
            cat_counts['unsplit_partie'] += 1
        elif 'correct_answer missing' in msg:
            cat_counts['missing_answer'] += 1
        elif 'points=0' in msg:
            cat_counts['zero_points'] += 1
        elif 'EMPTY' in msg:
            cat_counts['empty'] += 1
        elif 'figure' in msg or 'document' in msg:
            cat_counts['missing_fig'] += 1
        elif 'mismatch' in msg:
            cat_counts['pts_mismatch'] += 1
        else:
            cat_counts['other'] += 1

    print('Summary by category:')
    for cat, n in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f'  {cat:<20} {n}')
    print()

    by_file: dict[str, list] = defaultdict(list)
    for rel, where, msg in findings:
        by_file[rel].append((where, msg))
    print(f'Total: {len(findings)} issue(s) in {len(by_file)} file(s):\n')
    for rel, items in sorted(by_file.items()):
        print(f'=== {rel}')
        for where, msg in items:
            marker = ''
            if 'CONVERT TO QCM' in msg:
                marker = '  *** QCM ***'
            elif 'CONVERT TO VRAI_FAUX' in msg:
                marker = '  *** VF ***'
            elif 'SPLIT' in msg:
                marker = '  *** SPLIT ***'
            print(f'  [{where}] {msg}{marker}')
        print()


if __name__ == '__main__':
    main()
