"""Inspect the raw JSON structure of PC + Math cadres."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "cours 2bac pc" / "cadres de references 2BAC PC"

for fname, label in [
    ("cadre-de-reference-de-l-examen-national-physique-chimie-spc-2.json", "PC"),
    ("cadre-de-reference-de-l-examen-national-maths-sciences-experimentales.json", "MATH"),
]:
    print(f"\n{'=' * 80}\n{label}\n{'=' * 80}")
    d = json.loads((BASE / fname).read_text(encoding="utf-8"))
    print(f"Type: {type(d).__name__}")
    if isinstance(d, list):
        print(f"Length: {len(d)}")
        if d:
            print(f"First item keys: {list(d[0].keys()) if isinstance(d[0], dict) else type(d[0])}")
            print(f"First item (first 1500 chars):")
            print(json.dumps(d[0], ensure_ascii=False, indent=2)[:2000])
    elif isinstance(d, dict):
        print(f"Top keys: {list(d.keys())}")
        print(json.dumps(d, ensure_ascii=False, indent=2)[:2000])
