import json
from pathlib import Path
p = Path('backend/data/exams/physique/2018-normale/exam.json')
d = json.loads(p.read_text(encoding='utf-8-sig'))
for pi, part in enumerate(d.get('parts', [])):
    print(f'=== Part {pi+1}: {part.get("name","")!r}')
    for ei, ex in enumerate(part.get('exercises', []) or []):
        qs = ex.get('questions', []) or []
        print(f'  Ex{ei+1}: {ex.get("name","")!r}  qs={len(qs)}')
        ctx = ex.get('context','') or ''
        if ctx:
            print(f'    context[:200]: {ctx[:200]!r}')
        for qi, q in enumerate(qs):
            num = q.get('number','?')
            content = (q.get('content') or '').strip()
            print(f'    Q{num} (pts={q.get("points")}, len={len(content)})')
            print(f'      content[:200]: {content[:200]!r}')
            sub = q.get('sub_questions', []) or []
            if sub:
                for sq in sub:
                    sn = sq.get('number','?')
                    sc = (sq.get('content') or '').strip()
                    print(f'        SUB Q{sn} (len={len(sc)}): {sc[:120]!r}')
