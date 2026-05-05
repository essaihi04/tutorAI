"""Split 2022-normale PC Ex2 Q1 into two vrai_faux questions.

Original Q1 had:
  - Partie 1 preamble + '---' separator
  - Two items 1.1, 1.2 bundled in content
  - Single correction covering both
  - type=vrai_faux, points=0.5, no correct_answer

After: two questions Q1.1 and Q1.2 (each 0.25pt), Q1.1 keeps the
Partie 1 preamble so all Partie-1 questions inherit it via the
propagation regex.
"""
import json, re, sys
from pathlib import Path

DRY = '--apply' not in sys.argv
P = Path('backend/data/exams/physique/2022-normale/exam.json')
d = json.loads(P.read_text(encoding='utf-8-sig'))
qs = d['parts'][0]['exercises'][1]['questions']
q1 = qs[0]
assert str(q1['number']) == '1' and q1.get('type') == 'vrai_faux', 'Q1 layout changed'

content = q1['content']
# Split preamble (everything up to the '---') from items.
preamble, _, rest = content.partition('\n---\n')
# Extract items "N.N. text" — there are 2 items (1.1 and 1.2)
item_re = re.compile(r'^\s*(1\.\d+)\.\s*(.+?)(?=\n\s*1\.\d+\.|\Z)', re.MULTILINE | re.DOTALL)
items = [(m.group(1), m.group(2).strip()) for m in item_re.finditer(rest)]
assert len(items) == 2, f'Expected 2 items, got {len(items)}'

# Parse verdict from correction
corr_text = (q1.get('correction') or {}).get('content', '')
verdict_map = {}
for num, v in re.findall(r'(1\.\d+)\.?\s*(Vrai|Faux)', corr_text, re.IGNORECASE):
    verdict_map[num] = v.lower()
assert len(verdict_map) == 2, f'Could not parse both verdicts: {verdict_map}'

# Split correction into per-item justifications
just_map = {}
for m in re.finditer(r'(1\.\d+)\.\s*(.+?)(?=\n\s*1\.\d+\.|\Z)', corr_text, re.DOTALL):
    just_map[m.group(1)] = m.group(2).strip()

# Intro line from items block (e.g., "Recopier le numéro...")
intro = rest.split('\n', 1)[0].strip()
items_body_first = intro.startswith('Recopier') or intro.startswith('Répondre')

new_questions = []
for i, (num, text) in enumerate(items):
    verdict = verdict_map[num]
    just = just_map.get(num, f'{"Vrai" if verdict == "vrai" else "Faux"}.')
    if i == 0:
        nc = preamble.strip() + '\n\n---\n\n' + (intro + '\n\n' if items_body_first else '') + text
    else:
        nc = text
    new_questions.append({
        'number': num,
        'type': 'vrai_faux',
        'points': 0.25,
        'content': nc,
        'correct_answer': verdict,
        'correction': {
            'content': just,
            'correct_answer': verdict,
        },
    })

qs[0:1] = new_questions
for nq in new_questions:
    print(f"  Q{nq['number']} (0.25pt) ans={nq['correct_answer']}  {(nq['content'] or '')[:80]!r}")

if DRY:
    print('\n[DRY RUN]')
else:
    P.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print('\n[APPLIED]')
