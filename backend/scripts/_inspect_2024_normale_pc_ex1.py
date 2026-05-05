import json
from pathlib import Path
d = json.loads(Path('backend/data/exams/physique/2024-normale/exam.json').read_text(encoding='utf-8-sig'))
ex = d['parts'][0]['exercises'][0]
print('EX NAME:', ex.get('name'))
print('CTX:', (ex.get('context','') or '')[:200])
for q in ex['questions'][:5]:
    print('=' * 60)
    print(f'Q{q.get("number")} (type={q.get("type")}, pts={q.get("points")})')
    print('content:'); print(q.get('content',''))
    print('---')
    print('correction:'); 
    c = q.get('correction')
    if isinstance(c, dict):
        print(json.dumps(c, ensure_ascii=False, indent=2)[:800])
    else:
        print(c)
    print('---')
    print('sub_questions:', len(q.get('sub_questions') or []))
    print('answers:', q.get('answers'))
    print('choices:', q.get('choices'))
    print('metadata:', q.get('metadata'))
