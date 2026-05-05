"""Convert 4 mislabeled 'open' questions in 2022-rattrapage PC Ex2 into
QCM. Each has a markdown table with options A/B/C/D and the correction
explicitly names the correct letter. The generic fix_mislabeled_qcm.py
skipped them because their intros lack 'choisir/cochez/...' keywords
(the QCM instruction sits at the Partie-preamble level instead).

Questions fixed: Ex2 Q3, Q4, Q1.1, Q1.2 — which map to frontend
numbering 16, 17, 18, 19 respectively.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fix_mislabeled_qcm import extract_choices, extract_correct_answer  # noqa: E402

DRY = '--apply' not in sys.argv
P = Path('backend/data/exams/physique/2022-rattrapage/exam.json')
d = json.loads(P.read_text(encoding='utf-8-sig'))
qs = d['parts'][0]['exercises'][1]['questions']

TARGETS = {'3', '4', '1.1', '1.2'}
for q in qs:
    if str(q.get('number')) not in TARGETS or q.get('type') == 'qcm':
        continue
    result = extract_choices(q.get('content', '') or '')
    if not result:
        print(f"  skip Q{q.get('number')}: no markdown choices table")
        continue
    choices, cleaned = result
    q['type'] = 'qcm'
    q['content'] = cleaned
    q['choices'] = choices
    letters = [c['letter'] for c in choices]
    ans = extract_correct_answer(q.get('correction'), letters)
    if ans:
        q['correct_answer'] = ans
    print(f"  Q{q.get('number')}: open→qcm, letters={letters}, correct_answer={ans}")

if DRY:
    print('\n[DRY RUN]')
else:
    P.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print('\n[APPLIED]')
