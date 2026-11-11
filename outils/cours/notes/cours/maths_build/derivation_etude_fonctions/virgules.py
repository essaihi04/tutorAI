"""Coupe par une virgule les suites de plus de dix mots français dans la voix (règle voix-du-cours)."""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open(r'backend/data/courses/math_ch2_derivation_etude_fonctions.json', encoding='utf-8'))
def runs(t):
    out = []
    for seg in re.split(r"[,،.:;؟?!]", t):
        cur = []
        for w in seg.split():
            if re.search(r"[\u0600-\u06FF]", w):
                if len(cur) > 10: out.append(' '.join(cur))
                cur = []
            else: cur.append(w)
        if len(cur) > 10: out.append(' '.join(cur))
    return out
def couper(r, virg):
    w = r.split()
    for cle in ("égale", "est", "a", "en", "au"):
        for i in range(3, len(w) - 2):
            if w[i] == cle: return ' '.join(w[:i]) + virg + ' ' + ' '.join(w[i:])
    m = len(w) // 2
    return ' '.join(w[:m]) + virg + ' ' + ' '.join(w[m:])
todo = []
for a in d['activities']:
    for s in a['slides']:
        for r in runs(s['speech_text']['mixed']): todo.append((r, couper(r, '،')))
        for o in [s.get('question')] + s.get('exercises', []):
            if o and o.get('demonstration'):
                for r in runs(o['demonstration']['parole']): todo.append((r, couper(r, ',')))
files = {p: p.read_text(encoding='utf-8') for p in Path('.').glob('p[1-5].py')}
for a, b in dict(todo).items():
    n = 0
    for p in files:
        if a in files[p]: files[p] = files[p].replace(a, b); n += 1
    print(n, '|', b)
for p, s in files.items(): p.write_text(s, encoding='utf-8')
