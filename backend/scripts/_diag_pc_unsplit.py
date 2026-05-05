"""Quick diagnostic of the 8 exercises with unsplit Parties in ex.context.
Prints for each:
  - Partie headers detected in ex.context
  - Sub-section markers like "**1. ...**" / "**2. ...**" inside ex.context
  - Question numbers to identify which question owns which Partie
"""
import json, re
from pathlib import Path

CASES = [
    ('physique/2016-normale',    0),  # Ex1 Chimie
    ('physique/2016-normale',    3),  # Ex4 Mouvement magnétique
    ('physique/2018-rattrapage', 3),  # Ex4 Lorentz + pendule
    ('physique/2023-normale',    3),  # Ex4 Chute + ?
    ('physique/2023-rattrapage', 0),  # Ex1 Chimie
    ('physique/2023-rattrapage', 3),  # Ex4 Parabolique + pendule
    ('physique/2025-rattrapage', 2),  # Ex3 Circuit RL/LC/modulation
    ('physique/2025-rattrapage', 3),  # Ex4 Skieur + pendule
]
PARTIE_RE = re.compile(r'\*\*Partie\s+([IVX\d]+)[^*\n]*\*\*')
SUBSECT_RE = re.compile(r'^\s*\*\*(\d+)\.\s[^*]*\*\*', re.MULTILINE)

for path, ex_idx in CASES:
    print('=' * 70)
    print(f'{path}  Ex{ex_idx+1}')
    d = json.loads(Path(f'backend/data/exams/{path}/exam.json').read_text(encoding='utf-8-sig'))
    ex = d['parts'][0]['exercises'][ex_idx]
    ctx = ex.get('context', '') or ''
    print(f'  ctx_len={len(ctx)}')
    for m in PARTIE_RE.finditer(ctx):
        print(f'    Partie: {m.group(0)[:80]} at char {m.start()}')
    subs = list(SUBSECT_RE.finditer(ctx))
    if subs:
        print(f'  sub-sections ({len(subs)}):')
        for m in subs:
            print(f'    {m.group(0)[:80]} at char {m.start()}')
    # Question numbers
    nums = [q.get('number') for q in ex.get('questions', [])]
    print(f'  question numbers: {nums}')
    print()
