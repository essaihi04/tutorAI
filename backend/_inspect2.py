import json
d = json.loads(open('data/exams/svt/2020-rattrapage/exam.json', encoding='utf-8').read())
for ex in d['parts'][1]['exercises']:
    ctx = ex.get('context', '')[:200]
    name = ex.get('name', '?')
    pts = ex.get('points', '?')
    print(f'--- {name} ({pts}pts) ---')
    print(f'Context: {ctx}')
    print()
