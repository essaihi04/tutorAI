"""Show every sub_domain name from the Math cadre."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "cours 2bac pc" / "cadres de references 2BAC PC"
d = json.loads((BASE / "cadre-de-reference-de-l-examen-national-maths-sciences-experimentales.json").read_text(encoding="utf-8"))

for i, page in enumerate(d):
    content = page.get("content", {})
    if not isinstance(content, dict):
        continue
    md = content.get("main_domain")
    if md:
        print(f"\n◉ Page {i}: {md}")
    for key in ("sub_domains", "chapters", "chapitres"):
        for sd in content.get(key, []) or []:
            name = sd.get("name") or sd.get("nom") or sd.get("title", "")
            print(f"    - {name}")
            # Content/objectives
            for objk in ("content", "contenu", "objectives", "objectifs", "contents"):
                for o in sd.get(objk, []) or []:
                    if isinstance(o, str):
                        print(f"        · {o[:120]}")
                    elif isinstance(o, dict):
                        print(f"        · {(o.get('titre') or o.get('nom') or str(o))[:120]}")

    # Also dump the weights table to know domain weights
    if "table_a_domaines" in content:
        print("\n▸ Table des domaines + poids:")
        for row in content["table_a_domaines"].get("rows", []):
            print(f"    {row}")
