import json, re, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

p = Path("backend/data/exams/physique/2024-normale/extraction.json")
d = json.loads(p.read_text(encoding="utf-8"))
sujet = d.get("sujet_text", "")
print(f"=== SUJET ({len(sujet)} chars) ===\n")
print(sujet[:4000])
print("\n\n=== FIGURE CAPTIONS ===")
for m in re.finditer(r"(?i)(figure|diagramme|schéma|graphique|fig\.?|doc\.?)\s*([^\n.,;]*)", sujet):
    print(f"  [{m.start()}] {m.group(0).strip()}")
