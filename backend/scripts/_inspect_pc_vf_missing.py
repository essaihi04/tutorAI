import json
from pathlib import Path

TARGETS = [
    ('physique/2021-rattrapage', 1, '1'),    # Ex2 Q1
    ('physique/2022-normale',    1, '1'),    # Ex2 Q1
    ('physique/2023-normale',    1, '5.a'),  # Ex2 Q5.a
    ('physique/2023-normale',    1, '5.b'),  # Ex2 Q5.b
    ('physique/2023-normale',    2, '3.2.a'),# Ex3 Q3.2.a
    ('physique/2023-normale',    2, '3.2.b'),# Ex3 Q3.2.b
    ('physique/2025-normale',    0, '2.3'),  # Ex1 Q2.3
    ('physique/2025-rattrapage', 0, '3.2'),  # Ex1 Q3.2
]
root = Path('backend/data/exams')
for path, ex_idx, qnum in TARGETS:
    f = root / path / 'exam.json'
    d = json.loads(f.read_text(encoding='utf-8-sig'))
    ex = d['parts'][0]['exercises'][ex_idx]
    print('=' * 70)
    print(f'{path}  Ex{ex_idx+1}  (looking for Q{qnum})')
    # walk all leaf questions
    def walk(qs, parent=None):
        for q in qs:
            sub = q.get('sub_questions', []) or []
            if sub:
                yield from walk(sub, q)
            else:
                yield q, parent
    for q, parent in walk(ex['questions']):
        if str(q.get('number')) == qnum:
            print(f'  points: {q.get("points")}  type: {q.get("type")}')
            print(f'  content: {q.get("content", "")[:250]!r}')
            print(f'  correction: {json.dumps(q.get("correction"), ensure_ascii=False)[:250]}')
            print(f'  correct_answer(q): {q.get("correct_answer")}')
            if parent:
                print(f'  parent Q{parent.get("number")} content[:150]: {parent.get("content","")[:150]!r}')
            break
    else:
        print('  NOT FOUND')
    print()
