import json, sys
from pathlib import Path
p = Path(r"backend/data/curriculum/programme_semestre1.json")
d = json.loads(p.read_text(encoding="utf-8")); n = 0
for k, v in d.items():
    if isinstance(v, list):
        for c in v:
            if isinstance(c, dict) and c.get("cle") == "suites_definition":
                c["statut"] = "construit"; c["cours"] = "math_ch3_suites_numeriques"; n += 1
assert n == 1, n
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); print("ok")
