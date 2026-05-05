"""Split bundled Parties in 2018-normale Ex1 (chimie) and Ex4 (mécanique).

Convention: each "Partie N" preamble is moved into the OWNER question's
content, prefixed before a "---" separator, so the frontend regex
detects it and propagates to all sibling questions of that Partie.

Ex1 (Électrolyse + acide lactique) is split into 3 Parties:
  Partie 1 → Électrolyse                   (Q1, Q2, Q3, Q4)
  Partie 2 → Dosage acide lactique         (Q1.1 - Q1.5)
  Partie 3 → Estérification (méthanol)     (Q2.1 - Q2.4)

Ex4 (Mécanique) keeps the original 2 Parties:
  Partie 1 → Chute visqueuse                (Q1, Q2, Q3, Q4)
  Partie 2 → Oscillateur                    (Q5, Q6, Q7)
"""
from __future__ import annotations
import json, sys
from pathlib import Path

DRY = '--apply' not in sys.argv
p = Path('backend/data/exams/physique/2018-normale/exam.json')
d = json.loads(p.read_text(encoding='utf-8-sig'))


def find_q(ex: dict, num: str) -> dict:
    for q in ex['questions']:
        if str(q.get('number')) == num:
            return q
    raise KeyError(num)


def inject_preamble(q: dict, preamble: str):
    """Prepend the preamble + '---' separator to question content (idempotent)."""
    content = q.get('content', '') or ''
    if content.lstrip().startswith('**Partie'):
        print(f'  [SKIP] Q{q.get("number")} already has a Partie preamble')
        return
    q['content'] = preamble.strip() + '\n\n---\n\n' + content


# ─────────────────────────────────────────────────────────────────────
# EX1 — Électrolyse + acide lactique (split into 3 Parties)
# ─────────────────────────────────────────────────────────────────────
ex1 = d['parts'][0]['exercises'][0]
ctx1 = ex1['context']

# Locate the major split markers
m_p1 = ctx1.index("**Partie I -")
m_p2 = ctx1.index("**Partie II -")
m_sub1 = ctx1.index("**1. Réaction de l'acide lactique avec l'hydroxyde")
m_sub2 = ctx1.index("**2. Réaction entre l'acide lactique et le méthanol")

partie1_text = ctx1[m_p1:m_p2].strip()           # Electrolyse
partie2_intro = ctx1[m_p2:m_sub1].strip()        # acide lactique global intro
partie2_sub1 = ctx1[m_sub1:m_sub2].strip()       # dosage
partie2_sub2 = ctx1[m_sub2:].strip()             # estérification

# Rename "Partie I" → "Partie 1", and split "Partie II" into "Partie 2"
# (dosage) and "Partie 3" (estérification). Keep the rest of the text.
preamble_q1 = partie1_text.replace("**Partie I -", "**Partie 1 -", 1)

# Partie 2: dosage. The "**1. Réaction..." sub-header is renamed to the
# Partie 2 title, since this is now a stand-alone Partie. Include the
# acide lactique global intro before the dosage details.
sub1_renamed = partie2_sub1.replace(
    "**1. Réaction de l'acide lactique avec l'hydroxyde de sodium**",
    "**Partie 2 - Réaction de l'acide lactique avec l'hydroxyde de sodium**",
    1,
)
# Strip the original "Partie II" header line from the intro since the
# Partie 2 title now lives in sub1_renamed.
partie2_intro_clean = partie2_intro
header_line = partie2_intro_clean.split('\n', 1)[0]
if header_line.startswith("**Partie II -"):
    partie2_intro_clean = partie2_intro_clean.split('\n', 1)[1].strip()

# Final Partie 2 preamble = renamed sub1 header followed by global intro
# and the dosage details (intro paragraph integrated inside).
preamble_q11 = sub1_renamed.replace(
    "**Partie 2 - Réaction de l'acide lactique avec l'hydroxyde de sodium**",
    "**Partie 2 - Réaction de l'acide lactique avec l'hydroxyde de sodium**\n\n"
    + partie2_intro_clean,
    1,
)

# Partie 3: estérification.
preamble_q21 = partie2_sub2.replace(
    "**2. Réaction entre l'acide lactique et le méthanol**",
    "**Partie 3 - Réaction entre l'acide lactique et le méthanol**",
    1,
)

inject_preamble(find_q(ex1, '1'),   preamble_q1)
inject_preamble(find_q(ex1, '1.1'), preamble_q11)
inject_preamble(find_q(ex1, '2.1'), preamble_q21)

# Reset context to the lead-in only (the rest is now in question contents).
ex1['context'] = "Les trois parties sont indépendantes."

# ─────────────────────────────────────────────────────────────────────
# EX4 — Mécanique (split into 2 Parties)
# ─────────────────────────────────────────────────────────────────────
ex4 = d['parts'][0]['exercises'][3]
ctx4 = ex4['context']

m_p1 = ctx4.index("**Partie I -")
m_p2 = ctx4.index("**Partie II -")
partie1_text4 = ctx4[m_p1:m_p2].strip().replace("**Partie I -", "**Partie 1 -", 1)
partie2_text4 = ctx4[m_p2:].strip().replace("**Partie II -", "**Partie 2 -", 1)

# Owner questions: Q1 (chute) and Q5 (oscillateur)
inject_preamble(find_q(ex4, '1'), partie1_text4)
inject_preamble(find_q(ex4, '5'), partie2_text4)
ex4['context'] = "Les deux parties sont indépendantes."

# ─────────────────────────────────────────────────────────────────────
print('=' * 70)
print('AFTER FIX — EX1')
print('  context:', repr(ex1['context']))
for n in ('1', '1.1', '2.1'):
    q = find_q(ex1, n)
    print(f'  Q{n} content[:150]: {q["content"][:150]!r}')
print()
print('AFTER FIX — EX4')
print('  context:', repr(ex4['context']))
for n in ('1', '5'):
    q = find_q(ex4, n)
    print(f'  Q{n} content[:150]: {q["content"][:150]!r}')

if DRY:
    print('\n[DRY RUN] Re-run with --apply to write.')
else:
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print('\n[APPLIED] File written.')
