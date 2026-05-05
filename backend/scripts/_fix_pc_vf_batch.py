"""Batch fix for PC vrai_faux questions missing correct_answer.

Case A — single-item vrai_faux: parse first word of correction.content
         ('Vrai.'/'Faux.') and set q.correct_answer accordingly.

Case B — bundled vrai_faux (multiple a-, b-, c- items): split into one
         question per item with its own correct_answer, same pattern as
         the 2024 PC fix.

2022-normale Ex2 Q1 has an embedded Partie preamble on top of a bundled
vrai_faux. It is NOT handled here — addressed in a dedicated script.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

DRY = '--apply' not in sys.argv
EXAMS = Path('backend/data/exams')

CASE_A = [
    # (exam_dir, ex_idx, leaf_number)
    ('physique/2023-normale',    1, '5.a'),
    ('physique/2023-normale',    1, '5.b'),
    ('physique/2023-normale',    2, '3.2.a'),
    ('physique/2023-normale',    2, '3.2.b'),
    ('physique/2025-normale',    0, '2.3'),
    ('physique/2025-rattrapage', 0, '3.2'),
]

CASE_B = [
    # (exam_dir, ex_idx, q_number)
    ('physique/2021-rattrapage', 1, '1'),
]


def walk(qs):
    for q in qs:
        sub = q.get('sub_questions', []) or []
        if sub:
            for c in walk(sub):
                yield c
        else:
            yield q


def parse_verdict(text: str) -> str | None:
    """Return 'vrai' or 'faux' from first verdict-word in correction text."""
    m = re.match(r'\s*(Vrai|Faux)\b', text, re.IGNORECASE)
    return m.group(1).lower() if m else None


def fix_case_a(exam_dir: str, ex_idx: int, qnum: str):
    path = EXAMS / exam_dir / 'exam.json'
    d = json.loads(path.read_text(encoding='utf-8-sig'))
    ex = d['parts'][0]['exercises'][ex_idx]

    # find leaf question
    target = None
    for q in walk(ex['questions']):
        if str(q.get('number')) == qnum:
            target = q
            break
    assert target is not None, f'{exam_dir} Ex{ex_idx+1} Q{qnum} not found'

    corr = target.get('correction') or {}
    text = corr.get('content', '') if isinstance(corr, dict) else ''
    verdict = parse_verdict(text)
    assert verdict, f'Cannot parse verdict from correction: {text[:80]!r}'

    target['correct_answer'] = verdict
    # Also store in correction for consistency
    if isinstance(target.get('correction'), dict):
        target['correction']['correct_answer'] = verdict
    print(f'  [A] {exam_dir} Ex{ex_idx+1} Q{qnum}: correct_answer=\'{verdict}\'')

    if not DRY:
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')


def fix_case_b(exam_dir: str, ex_idx: int, qnum: str):
    """Split a bundled vrai_faux question into per-item questions."""
    path = EXAMS / exam_dir / 'exam.json'
    d = json.loads(path.read_text(encoding='utf-8-sig'))
    ex = d['parts'][0]['exercises'][ex_idx]
    qs = ex['questions']

    # find the bundled question at the top level
    target_idx = next(
        (i for i, q in enumerate(qs)
         if str(q.get('number')) == qnum and q.get('type') == 'vrai_faux'),
        None,
    )
    assert target_idx is not None, f'{exam_dir} Ex{ex_idx+1} Q{qnum} not found'
    orig = qs[target_idx]
    content = orig.get('content') or ''

    # items: lines like "a) ..." or "a- ..." or "a. ..."
    items = re.findall(r'^\s*([a-z])[\)\-\.]\s*(.+)$', content, re.MULTILINE)

    # verdicts: parse from correction text "a) Faux. ... b) Vrai..."
    corr = orig.get('correction') or {}
    corr_text = corr.get('content', '') if isinstance(corr, dict) else ''
    verdict_map = {}
    for letter, v in re.findall(r'([a-z])[\)\-\.]\s*(Vrai|Faux)', corr_text, re.IGNORECASE):
        verdict_map[letter.lower()] = v.lower()

    assert set(l for l, _ in items) == set(verdict_map.keys()), \
        f'item/verdict mismatch: items={[l for l,_ in items]} verdicts={list(verdict_map)}'

    # also extract per-item justification from correction (best-effort)
    just_map = {}
    for m in re.finditer(r'([a-z])[\)\-\.]\s*(.+?)(?=\n[a-z][\)\-\.]|\Z)', corr_text, re.DOTALL | re.IGNORECASE):
        just_map[m.group(1).lower()] = m.group(2).strip()

    total_pts = float(orig.get('points') or 0.0)
    per_pt = round(total_pts / len(items), 3)
    intro = content.split('\n', 1)[0].strip() if content else ''
    new_questions = []
    for i, (letter, text) in enumerate(items):
        verdict = verdict_map[letter]
        just = just_map.get(letter, f'{"Vrai" if verdict == "vrai" else "Faux"}.')
        prefix = f'{intro}\n\n**{letter}.** ' if (i == 0 and intro.lower().startswith(('recopier', 'répondre'))) else f'**{letter}.** '
        nq = {
            'number': f'{qnum}.{letter}',
            'type': 'vrai_faux',
            'points': per_pt,
            'content': prefix + text.strip(),
            'correct_answer': verdict,
            'correction': {
                'content': just,
                'correct_answer': verdict,
            },
        }
        new_questions.append(nq)

    qs[target_idx:target_idx + 1] = new_questions
    print(f'  [B] {exam_dir} Ex{ex_idx+1} Q{qnum}: split into {len(new_questions)} items @ {per_pt}pt each')
    for nq in new_questions:
        print(f"       → Q{nq['number']} ans={nq['correct_answer']}")

    if not DRY:
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')


print('CASE A — single-item vrai_faux, add correct_answer:')
for t in CASE_A:
    fix_case_a(*t)

print('\nCASE B — bundled vrai_faux, split into per-item questions:')
for t in CASE_B:
    fix_case_b(*t)

if DRY:
    print('\n[DRY RUN] Re-run with --apply to write.')
else:
    print('\n[APPLIED]')
