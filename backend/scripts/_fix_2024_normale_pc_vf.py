"""Split bundled Vrai/Faux question in 2024-normale PC Ex1 Q1.

Before: a single question of type vrai_faux bundles 3 affirmations
(a, b, c) with one freetext correction "a- Vrai ; b- Faux ; c- Vrai.",
making the UI show one Vrai/Faux selector that cannot grade the 3
affirmations.

After: Q1 is replaced by three standalone vrai_faux questions
(Q1.a, Q1.b, Q1.c), each with content = single affirmation, points =
0.25 (0.75 total preserved), and correct_answer set to "vrai"/"faux".

Also audits the entire math + physique + svt corpus for similar
patterns (single vrai_faux question bundling multiple items) and
reports them without modifying.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

DRY = '--apply' not in sys.argv
EXAMS = Path('backend/data/exams')

TARGETS = [
    # (exam_json_relative, ex_index, question_number)
    (EXAMS / 'physique' / '2024-normale' / 'exam.json',    0, '1'),
    (EXAMS / 'physique' / '2024-rattrapage' / 'exam.json', 1, '2'),
]


def split_bundled_vf(path: Path, ex_idx: int, qnum: str):
    print('=' * 70)
    print(f'Target: {path}  Ex{ex_idx+1}  Q{qnum}')
    d = json.loads(path.read_text(encoding='utf-8-sig'))
    ex = d['parts'][0]['exercises'][ex_idx]
    qs = ex['questions']
    target_idx = next(
        (i for i, q in enumerate(qs)
         if str(q.get('number')) == qnum and q.get('type') == 'vrai_faux'),
        None,
    )
    assert target_idx is not None, f'Bundled Q{qnum} not found.'
    orig = qs[target_idx]
    content = orig.get('content', '')
    affirmations = re.findall(r'^\s*([a-z])-\s*(.+)$', content, re.MULTILINE)
    corr = orig.get('correction', {}) or {}
    corr_text = corr.get('content', '') if isinstance(corr, dict) else ''
    answer_map = {}
    for letter, verdict in re.findall(r'([a-z])-\s*(Vrai|Faux)', corr_text, re.IGNORECASE):
        answer_map[letter.lower()] = verdict.lower()
    print(f'  {len(affirmations)} affirmations; answers: {answer_map}')
    assert set(l for l, _ in affirmations) == set(answer_map.keys()), \
        f'Mismatch in {path}: {[l for l,_ in affirmations]} vs {list(answer_map)}'

    total_pts = float(orig.get('points') or 0.0)
    per_pt = round(total_pts / len(affirmations), 3)
    intro_line = content.split('\n', 1)[0].strip()
    new_questions = []
    for i, (letter, text) in enumerate(affirmations):
        ans = answer_map[letter]
        if i == 0 and intro_line.lower().startswith('répondre'):
            nc = f'{intro_line}\n\n**{letter}.** {text.strip()}'
        else:
            nc = f'**{letter}.** {text.strip()}'
        new_questions.append({
            'number': f'{qnum}.{letter}',
            'type': 'vrai_faux',
            'points': per_pt,
            'content': nc,
            'correct_answer': ans,
            'correction': {
                'content': f'{"Vrai" if ans == "vrai" else "Faux"}.',
            },
        })
    for q in new_questions:
        print(f"    → Q{q['number']} ({q['points']}pt) ans={q['correct_answer']}")
    qs[target_idx:target_idx + 1] = new_questions
    if not DRY:
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'  [APPLIED]')
    else:
        print(f'  [DRY RUN]')


for t in TARGETS:
    split_bundled_vf(*t)


# --- Audit: find similar bundled vrai_faux across all exams ---
print('\n' + '=' * 70)
print('AUDIT: other bundled vrai_faux questions across all exams')
print('=' * 70)
for f in sorted(EXAMS.rglob('exam.json')):
    try:
        doc = json.loads(f.read_text(encoding='utf-8-sig'))
    except Exception:
        continue
    rel = f.relative_to(Path('backend/data'))
    for part in doc.get('parts', []) or []:
        for ei, exx in enumerate(part.get('exercises', []) or []):
            for q in exx.get('questions', []) or []:
                if q.get('type') != 'vrai_faux':
                    continue
                c = q.get('content', '') or ''
                n_items = len(re.findall(r'^\s*[a-z]-\s', c, re.MULTILINE))
                has_sub = bool(q.get('sub_questions'))
                has_ca = q.get('correct_answer') is not None
                if n_items >= 2 and not has_sub and not has_ca:
                    print(f'  {rel}  Ex{ei+1}  Q{q.get("number")}: {n_items} items bundled')
