"""Quick inspection of the 2025-normale math exam JSON structure."""
import json
from pathlib import Path

p = Path('backend/data/exams/mathematiques/2025-normale/exam.json')
d = json.loads(p.read_text(encoding='utf-8-sig'))

print('TOP-LEVEL KEYS:', list(d.keys()))
print(f'subject={d.get("subject")}  year={d.get("year")}  session={d.get("session")}')
print(f'total_points={d.get("total_points")}  duration={d.get("duration_minutes")}')
print(f'note: {(d.get("note") or "")[:200]!r}')
print()
for pi, part in enumerate(d.get('parts', [])):
    exs = part.get('exercises', []) or []
    qs_direct = part.get('questions', []) or []
    print(f'=== Part {pi+1}: {part.get("name","")!r}  pts={part.get("points","?")}')
    print(f'    direct_questions={len(qs_direct)}  exercises={len(exs)}')
    for ei, ex in enumerate(exs):
        qs = ex.get('questions', []) or []
        docs = ex.get('documents', []) or []
        ctx = ex.get('context', '') or ''
        corr_count = sum(1 for q in qs if q.get('correction'))
        sub_count = sum(len(q.get('sub_questions', []) or []) for q in qs)
        print(f'    Ex{ei+1}: {ex.get("name","")!r}  pts={ex.get("points","?")}')
        print(f'      topic={ex.get("topic","?")!r}  context={len(ctx)}ch  docs={len(docs)}')
        print(f'      questions={len(qs)} (sub-questions total={sub_count})  corrections={corr_count}')
        for qi, q in enumerate(qs):
            num = q.get('number', '?')
            qtype = q.get('type', '?')
            pts = q.get('points', '?')
            content = (q.get('content') or '').strip()
            cor = q.get('correction')
            cor_ok = bool(cor and (isinstance(cor, dict) and cor.get('content')))
            subq = q.get('sub_questions', []) or []
            marker = '✓' if cor_ok else '✗'
            print(f'        Q{num} [{qtype}] pts={pts} corr={marker} len={len(content)} sub={len(subq)}')
            if not content:
                print(f'          ⚠ EMPTY CONTENT')
            if subq:
                for si, sq in enumerate(subq):
                    snum = sq.get('number', f'{num}.{si+1}')
                    sc = (sq.get('content') or '').strip()
                    scor = sq.get('correction')
                    scor_ok = bool(scor and (isinstance(scor, dict) and scor.get('content')))
                    sm = '✓' if scor_ok else '✗'
                    print(f'            Q{snum} len={len(sc)} corr={sm}')
                    if not sc:
                        print(f'              ⚠ EMPTY SUB CONTENT')
