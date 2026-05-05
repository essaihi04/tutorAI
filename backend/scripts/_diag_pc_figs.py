import json, re
from pathlib import Path

FIG_RE = re.compile(r'\b(figure|schéma|graphe|courbe)\s*(\d+)?', re.IGNORECASE)

CASES = [
    ('physique/2022-rattrapage', 1),
    ('physique/2023-rattrapage', 0),
    ('physique/2023-rattrapage', 1),
]

for path, ex_idx in CASES:
    print('=' * 70)
    print(f'{path}  Ex{ex_idx+1}')
    d = json.loads(Path(f'backend/data/exams/{path}/exam.json').read_text(encoding='utf-8-sig'))
    ex = d['parts'][0]['exercises'][ex_idx]
    print(f'  name: {ex.get("name")}')
    print(f'  docs: {len(ex.get("documents") or [])}')
    ctx = ex.get('context', '') or ''
    ctx_refs = set(m.group(0) for m in FIG_RE.finditer(ctx))
    if ctx_refs:
        print(f'  ctx fig refs: {ctx_refs}')
    for q in ex.get('questions', []):
        def walk(qq):
            yield qq
            for sq in (qq.get('sub_questions') or []):
                yield from walk(sq)
        for qq in walk(q):
            c = qq.get('content', '') or ''
            refs = set(m.group(0) for m in FIG_RE.finditer(c))
            if refs:
                print(f'  Q{qq.get("number")}: {refs}  |  {c[:100]!r}')
    # Check pages
    pages = sorted(Path(f'backend/data/exams/{path}/pages').glob('sujet_p*.jpg'))
    print(f'  pages: {[p.name for p in pages]}')
