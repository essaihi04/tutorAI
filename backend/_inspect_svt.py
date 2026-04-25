"""Inspect SVT exams with point issues."""
import json
from pathlib import Path

for name in ['2016-ratrrapage', '2020-normale', '2020-rattrapage', '2021-normale', '2025-normale']:
    p = Path(f'data/exams/svt/{name}/exam.json')
    d = json.loads(p.read_text(encoding='utf-8'))
    print(f'\n=== {name} ===')
    print(f'  total_points: {d.get("total_points")}')
    for pi, part in enumerate(d.get('parts', [])):
        print(f'  Part {pi}: "{part.get("name","?")[:60]}" | declared_pts={part.get("points")}')
        for ei, ex in enumerate(part.get('exercises', []) or []):
            qs = ex.get('questions', [])
            q_sum = 0
            for q in qs:
                sqs = q.get('sub_questions', [])
                if sqs:
                    q_sum += sum(sq.get('points', 0) or 0 for sq in sqs)
                else:
                    q_sum += q.get('points', 0) or 0
            print(f'    Exo {ei}: "{ex.get("name","?")[:40]}" | declared={ex.get("points")} | sum_qs={q_sum}')
            for q in qs:
                sqs = q.get('sub_questions', [])
                if sqs:
                    s = sum(sq.get('points', 0) or 0 for sq in sqs)
                    print(f'      Q{q.get("number","?")}: declared={q.get("points")} sum_subs={s} ({len(sqs)} subs)')
                else:
                    print(f'      Q{q.get("number","?")}: declared={q.get("points")}')
        for q in part.get('questions', []) or []:
            sqs = q.get('sub_questions', [])
            if sqs:
                s = sum(sq.get('points', 0) or 0 for sq in sqs)
                print(f'    Q{q.get("number","?")}: declared={q.get("points")} sum_subs={s} ({len(sqs)} subs)')
            else:
                print(f'    Q{q.get("number","?")}: declared={q.get("points")}')
