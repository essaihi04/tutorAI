import json, re
from pathlib import Path
p = Path('backend/data/exams/physique/2018-normale/exam.json')
d = json.loads(p.read_text(encoding='utf-8-sig'))
PARTIE_RE = re.compile(r'\*\*Partie\s+([IVX\d]+)[^*]*\*\*')
for ei, ex in enumerate(d['parts'][0]['exercises']):
    ctx = ex.get('context','') or ''
    parties_in_ctx = PARTIE_RE.findall(ctx)
    qcount = len(ex.get('questions',[]))
    print(f'Ex{ei+1}: {ex.get("name","")[:60]}')
    print(f'  ctx_len={len(ctx)}  parties_in_context={parties_in_ctx}  questions={qcount}')
    # Look for Partie markers in question content
    parties_in_q = []
    for q in ex.get('questions',[]):
        c = q.get('content','') or ''
        ms = PARTIE_RE.findall(c)
        if ms:
            parties_in_q.append((q.get('number'), ms))
    print(f'  parties_in_questions={parties_in_q}')
    print()
