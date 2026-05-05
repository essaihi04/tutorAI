import json
from pathlib import Path
d = json.loads(Path('backend/data/exams/physique/2024-rattrapage/exam.json').read_text(encoding='utf-8-sig'))
ex = d['parts'][0]['exercises'][1]
for q in ex['questions']:
    if str(q.get('number')) == '2' and q.get('type') == 'vrai_faux':
        print('FOUND Ex2 Q2')
        print('points:', q.get('points'))
        print('content:'); print(q.get('content',''))
        print('---')
        print('correction:'); print(json.dumps(q.get('correction',{}), ensure_ascii=False, indent=2))
        break
