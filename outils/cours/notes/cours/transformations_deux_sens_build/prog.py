"""programme_semestre1.json : transformations_deux_sens → construit, cours phys_ch11_transformations_deux_sens (relit, change la seule entrée, réécrit)."""
import json
from pathlib import Path
p = Path("backend/data/curriculum/programme_semestre1.json")
d = json.loads(p.read_text(encoding="utf-8"))
n = 0
for c in d["Physique-Chimie"]:
    if c.get("cle") == "transformations_deux_sens":
        c["statut"] = "construit"; c["cours"] = "phys_ch11_transformations_deux_sens"; n += 1
assert n == 1, n
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok")
