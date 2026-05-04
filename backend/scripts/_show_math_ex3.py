import json
from pathlib import Path
p = Path('backend/data/exams/mathematiques/2025-normale/exam.json')
d = json.loads(p.read_text(encoding='utf-8-sig'))
ex = d['parts'][0]['exercises'][2]
print('EX NAME:', ex.get('name'))
print('EX CTX:')
print(ex.get('context', ''))
print('EX DOCS:', ex.get('documents', []))
print('---')
for q in ex['questions']:
    print(f'Q{q.get("number")}: ({q.get("points")} pt)')
    print(q.get('content', ''))
    print()
