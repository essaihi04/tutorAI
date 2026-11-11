import json
from pathlib import Path
p = Path(r"backend/data/curriculum/programme_semestre1.json")
d = json.loads(p.read_text(encoding="utf-8"))
n = 0
for c in d["Physique-Chimie"]:
    if c.get("cle") == "ondes_lumineuses":
        c["statut"] = "construit"; c["cours"] = "phys_ch3_ondes_lumineuses"; n += 1
assert n == 1
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok")
