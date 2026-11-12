"""programme_semestre1.json : etat_equilibre → construit, cours phys_ch12_etat_equilibre (relit, change la seule entrée, réécrit)."""
import json
from pathlib import Path
p = Path("backend/data/curriculum/programme_semestre1.json")
d = json.loads(p.read_text(encoding="utf-8"))
n = 0
for c in d["Physique-Chimie"]:
    if c.get("cle") == "etat_equilibre":
        c["statut"] = "construit"; c["cours"] = "phys_ch12_etat_equilibre"; n += 1
assert n == 1, n
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok")
