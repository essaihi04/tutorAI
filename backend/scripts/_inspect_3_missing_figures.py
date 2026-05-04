"""Inspect the 3 math questions flagged as 'references figure but no docs'."""
import json, os
from pathlib import Path

CASES = [
    ('mathematiques/2018-rattrapage', 4, 'III.1.b'),   # ex index 4 = Ex5
    ('mathematiques/2022-normale',    4, '5.b'),       # ex index 4 = Ex5
    ('mathematiques/2024-rattrapage', 3, '1.a'),       # ex index 3 = Ex4
]
ROOT = Path('backend/data/exams')

for folder, ex_idx, qnum in CASES:
    exam_dir = ROOT / folder
    p = exam_dir / 'exam.json'
    d = json.loads(p.read_text(encoding='utf-8-sig'))
    ex = d['parts'][0]['exercises'][ex_idx]
    print('=' * 70)
    print(f'{folder}  Ex{ex_idx+1}: {ex.get("name","")!r}')
    q = next((q for q in ex['questions'] if str(q.get('number')) == qnum), None)
    if not q:
        # Try sub-questions
        for parent in ex['questions']:
            for sq in parent.get('sub_questions', []) or []:
                if str(sq.get('number')) == qnum:
                    q = sq
                    break
    print(f'Question Q{qnum} ({q.get("points","?")} pt):')
    print(q.get('content',''))
    print('---')
    print(f'ex.context ({len(ex.get("context","") or "")} ch):')
    print((ex.get('context','') or '')[:500])
    print('---')
    print(f'ex.documents: {ex.get("documents", [])}')
    # List assets
    assets = exam_dir / 'assets'
    if assets.exists():
        files = sorted(os.listdir(assets))
        print(f'assets/ ({len(files)} files):')
        for f in files:
            print(f'  - {f}')
    else:
        print('assets/ does not exist')
    print()
