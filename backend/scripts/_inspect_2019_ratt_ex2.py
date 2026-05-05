import json
from pathlib import Path
d = json.loads(Path('backend/data/exams/physique/2019-rattrapage/exam.json').read_text(encoding='utf-8-sig'))
ex = d['parts'][0]['exercises'][1]
print('EX2 points:', ex.get('points'))
print('EX2 context:', (ex.get('context') or '')[:300])
for q in ex['questions']:
    print(f"\nQ{q.get('number')} | type={q.get('type')} | pts={q.get('points')}")
    print(f"  content[:150]: {(q.get('content') or '')[:150]!r}")
    print(f"  correction: {json.dumps(q.get('correction'), ensure_ascii=False)[:200] if q.get('correction') else 'None'}")
    sub = q.get('sub_questions', []) or []
    for sq in sub:
        print(f"    SQ{sq.get('number')} | pts={sq.get('points')} | {(sq.get('content') or '')[:100]!r}")
        print(f"      corr: {json.dumps(sq.get('correction'), ensure_ascii=False)[:200] if sq.get('correction') else 'None'}")
