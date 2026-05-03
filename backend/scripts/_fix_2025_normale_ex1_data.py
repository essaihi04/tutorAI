"""Move Partie-1-specific data bullets from exercise.context into Q1.1's preamble.

In physique/2025-normale/exam.json, Ex1 had its "Données générales" block
listing 5 bullets in ex.context. Only the first 2 are truly general (25°C,
K_e); the last 3 apply only to Partie 1 (dosage of NaHSO_3):

  - M(NaHSO_3) = 104 g.mol^-1
  - couple HSO_3^- / SO_3^2-
  - pK_A(HSO_3^- / SO_3^2-) = 7,2

They were displayed on Partie 2 questions too, which is misleading.

After this script:
  ex.context = lead-in + "Données générales :" with only the 2 truly
               general bullets (25°C, K_e).
  Q1.1.content = "**Partie 1 : ...**\n<original intro>\n**Données
               spécifiques :**\n- ...\n- ...\n- ...\n---\n<question text>"
"""
from __future__ import annotations
import json, sys
from pathlib import Path

DRY = '--apply' not in sys.argv
p = Path('backend/data/exams/physique/2025-normale/exam.json')
d = json.loads(p.read_text(encoding='utf-8-sig'))
ex = d['parts'][0]['exercises'][0]

ctx = ex['context']

# Split context at "**Données générales :**"
MARK = '**Données générales :**'
i = ctx.index(MARK)
lead_in = ctx[:i].rstrip()
data_block = ctx[i:].strip()

# Within the data block, separate general bullets (first 2) from
# Partie-1-specific bullets (last 3).
# Split by lines starting with "- " to preserve order.
lines = data_block.split('\n')
# lines[0] = "**Données générales :**"
header = lines[0]
bullets = [ln for ln in lines[1:] if ln.strip().startswith('-')]
assert len(bullets) == 5, f'Expected 5 bullets, got {len(bullets)}: {bullets}'

general_bullets = bullets[:2]       # 25°C, K_e
partie1_bullets = bullets[2:]       # NaHSO_3 specific

new_ex_ctx = lead_in + '\n\n' + header + '\n' + '\n'.join(general_bullets)

# Find Q1.1 and prepend Partie-1-specific data before the "---" separator.
q11 = ex['questions'][0]
assert q11.get('number') == '1.1', q11.get('number')
content = q11['content']
assert '\n---\n' in content, 'Expected --- separator in Q1.1 content'

preamble, rest = content.split('\n---\n', 1)
# Avoid double-injection if script run twice
if 'Données spécifiques' in preamble or 'M(\\mathrm{NaHSO}_3)' in preamble:
    print('[SKIP] Q1.1 already has Partie-1 data injected.')
else:
    injected = preamble.rstrip() + '\n\n**Données spécifiques à la Partie 1 :**\n' + '\n'.join(partie1_bullets)
    q11['content'] = injected + '\n\n---\n\n' + rest.lstrip()

ex['context'] = new_ex_ctx

print('[Plan]')
print('NEW EX CTX:')
print(new_ex_ctx)
print('---')
print('NEW Q1.1 CONTENT (first 500 chars):')
print(q11['content'][:500])

if DRY:
    print('\n[DRY RUN] Re-run with --apply to write.')
else:
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print('\n[APPLIED] File written.')
