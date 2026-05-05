import json
from pathlib import Path
d = json.loads(Path('backend/data/exams/physique/2018-normale/exam.json').read_text(encoding='utf-8-sig'))
ex = d['parts'][0]['exercises'][2]
print('EX3 NAME:', ex.get('name'))
print('FULL CTX:'); print(ex['context'])
print()
for q in ex['questions']:
    print(f'>> Q{q.get("number")} (pts={q.get("points")})')
    print(q.get('content','')[:600])
    print()
