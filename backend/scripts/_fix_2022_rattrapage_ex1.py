"""One-off fix for backend/data/exams/physique/2022-rattrapage/exam.json Ex1.

The `context` field contains three blocks concatenated:
  - lead-in "Les parties 1 et 2 sont indépendantes."
  - "**Partie I : ..." (Roman I — must be renamed to "Partie 1" so the
    frontend regex ^\*\*Partie\s+\d works)
  - "**Partie 2 : ..." which itself contains two sub-sections:
      "**1. Étude d'une solution..."   → Q1.1 preamble
      "**2. Dosage d'une solution..."  → Q2.1 preamble

After this script:
  context = "Les parties 1 et 2 sont indépendantes."
  Q1.content   = "**Partie 1 : ...**\n...\n---\n<original Q1 text>"
  Q1.1.content = "**Partie 2 : ...**\n...[intro]...\n**1. Étude...**\n...\n---\n<original Q1.1 text>"
  Q2.1.content = "**2. Dosage d'une solution aqueuse de méthylamine**\n...\n---\n<original Q2.1 text>"
"""
from __future__ import annotations
import json, sys
from pathlib import Path

DRY = '--apply' not in sys.argv
p = Path('backend/data/exams/physique/2022-rattrapage/exam.json')
d = json.loads(p.read_text(encoding='utf-8-sig'))
ex = d['parts'][0]['exercises'][0]
ctx = ex['context']

# Split points in the current context string
MARK_P1 = '**Partie I :'
MARK_P2 = '**Partie 2 :'
MARK_SUB2 = '**2. Dosage'

i_p1 = ctx.index(MARK_P1)
i_p2 = ctx.index(MARK_P2)
i_sub2 = ctx.index(MARK_SUB2)

lead_in = ctx[:i_p1].rstrip()
partie1 = ctx[i_p1:i_p2].rstrip()
partie2_with_sub1 = ctx[i_p2:i_sub2].rstrip()
sub2 = ctx[i_sub2:].rstrip()

# Rename "Partie I" → "Partie 1" so the frontend regex matches.
partie1 = partie1.replace('**Partie I :', '**Partie 1 :', 1)

print(f'[Plan]')
print(f'  lead_in ({len(lead_in)}): {lead_in!r}')
print(f'  partie1 ({len(partie1)}): starts={partie1[:80]!r}')
print(f'  partie2+sub1 ({len(partie2_with_sub1)}): starts={partie2_with_sub1[:80]!r}')
print(f'  sub2 ({len(sub2)}): starts={sub2[:80]!r}')

# Find target questions by number
def find(num):
    for q in ex['questions']:
        if str(q.get('number')) == num:
            return q
    raise KeyError(num)

q1 = find('1')
q11 = find('1.1')
q21 = find('2.1')

# Only prepend if the content doesn't already start with a Partie marker
# (avoid double-prepend if the script was already run).
def prepend(q, block):
    if q['content'].lstrip().startswith('**Partie') or q['content'].lstrip().startswith('**2. Dosage'):
        print(f'  SKIP q{q.get("number")} (already prefixed)')
        return False
    q['content'] = block + '\n\n---\n\n' + q['content']
    return True

ch1 = prepend(q1, partie1)
ch2 = prepend(q11, partie2_with_sub1)
ch3 = prepend(q21, sub2)

ex['context'] = lead_in

if DRY:
    print(f'\n[DRY RUN] 3 prepends: Q1={ch1}, Q1.1={ch2}, Q2.1={ch3}. New ctx={ex["context"]!r}')
    print('Re-run with --apply to write.')
else:
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print('\n[APPLIED] File written.')
