import json, sys
from pathlib import Path
path, ex_idx = sys.argv[1], int(sys.argv[2])
d = json.loads(Path(path).read_text(encoding='utf-8-sig'))
ex = d['parts'][0]['exercises'][ex_idx]
for q in ex['questions']:
    print(f"Q{q.get('number')}: {(q.get('content') or '')[:130]}")
