"""Fix 2019-rattrapage PC Ex2 Q2: sub-questions have no points and no
correct_answer. Parent Q2 has points=1.0, so set SQ2.1 = SQ2.2 = 0.5.
Corrections unambiguously say 'Vrai.' / 'Faux.'.
"""
import json, sys
from pathlib import Path

DRY = '--apply' not in sys.argv
P = Path('backend/data/exams/physique/2019-rattrapage/exam.json')
d = json.loads(P.read_text(encoding='utf-8-sig'))
ex = d['parts'][0]['exercises'][1]
q2 = next(q for q in ex['questions'] if str(q.get('number')) == '2')
assert q2.get('type') == 'vrai_faux' and q2.get('sub_questions')

verdicts = {'2.1': 'vrai', '2.2': 'faux'}
per_pt = 0.5
for sq in q2['sub_questions']:
    n = str(sq.get('number'))
    sq['points'] = per_pt
    sq['correct_answer'] = verdicts[n]
    corr = sq.setdefault('correction', {})
    corr['correct_answer'] = verdicts[n]
    print(f'  SQ{n}: pts={per_pt}, correct_answer={verdicts[n]}')

if DRY:
    print('\n[DRY RUN]')
else:
    P.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print('\n[APPLIED]')
