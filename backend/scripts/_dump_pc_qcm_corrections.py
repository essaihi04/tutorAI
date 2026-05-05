"""Dump corrections of QCM-disguised-as-open questions to identify correct answers."""
import json, re
from pathlib import Path

FILES = {
    '2020-normale': 'backend/data/exams/physique/2020-normale/exam.json',
    '2021-normale': 'backend/data/exams/physique/2021-normale/exam.json',
    '2022-normale': 'backend/data/exams/physique/2022-normale/exam.json',
}
QCM_TABLE = re.compile(r'\|\s*[Aa]\s*\|.+\|\s*[Bb]\s*\|', re.DOTALL)
ROOT = Path(__file__).resolve().parents[2]

for label, fpath in FILES.items():
    d = json.loads((ROOT / fpath).read_text(encoding='utf-8'))
    print(f'\n===== {label} =====')
    for ei, ex in enumerate(d['parts'][0]['exercises']):
        for q in ex.get('questions', []):
            if q['type'] == 'open' and QCM_TABLE.search(q.get('content', '')):
                corr = q.get('correction', {})
                corr_txt = corr.get('content', '') if isinstance(corr, dict) else str(corr)
                print(f'  Q{q["number"]} ({q["id"]}):')
                print(f'    CORRECTION: {corr_txt[:300]}')
                print()
