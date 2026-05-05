"""Inspect open questions with QCM tables in 2020-normale, 2021-normale, 2022-normale."""
import json, re
from pathlib import Path

FILES = {
    '2020-normale': 'backend/data/exams/physique/2020-normale/exam.json',
    '2021-normale': 'backend/data/exams/physique/2021-normale/exam.json',
    '2022-normale': 'backend/data/exams/physique/2022-normale/exam.json',
}

QCM_TABLE = re.compile(r'\|\s*[Aa]\s*\|.+\|\s*[Bb]\s*\|', re.DOTALL)
CORR_ANS  = re.compile(r'r[eé]ponse\s+(?:correcte\s+)?est\s+([A-D])', re.IGNORECASE)

ROOT = Path(__file__).resolve().parents[2]

for label, fpath in FILES.items():
    d = json.loads((ROOT / fpath).read_text(encoding='utf-8'))
    print(f'\n===== {label} =====')
    for ei, ex in enumerate(d['parts'][0]['exercises']):
        for q in ex.get('questions', []):
            c = q.get('content', '')
            if q['type'] == 'open' and QCM_TABLE.search(c):
                corr = q.get('correction')
                corr_txt = corr.get('content', '') if isinstance(corr, dict) else ''
                m = CORR_ANS.search(corr_txt)
                ans = m.group(1) if m else '?'
                print(f'  [ex{ei+1}] Q{q["number"]} (id={q["id"]}) correct={ans}')
                # Print the pipe-table lines
                for line in c.strip().split('\n'):
                    if '|' in line:
                        print(f'    {line.strip()}')
