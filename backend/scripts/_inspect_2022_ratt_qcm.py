import json
from pathlib import Path
d = json.loads(Path('backend/data/exams/physique/2022-rattrapage/exam.json').read_text(encoding='utf-8-sig'))
ex = d['parts'][0]['exercises'][1]
for i, q in enumerate(ex['questions']):
    if q.get('number') in ('3', '4', '1.1', '1.2'):
        print(f"idx={i} Q{q.get('number')} type={q.get('type')} pts={q.get('points')}")
        print('  content:', (q.get('content') or '')[:300].replace('\n', ' | '))
        corr = q.get('correction') or {}
        print('  corr:', (corr.get('content') or '')[:400].replace('\n', ' | '))
        print()
