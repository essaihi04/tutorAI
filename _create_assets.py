"""Create assets/ folders for all physics exams"""
from pathlib import Path

root = Path("backend/data/exams/physique")
for d in sorted(root.iterdir()):
    if not d.is_dir():
        continue
    assets = d / "assets"
    assets.mkdir(exist_ok=True)
    print(f"Created: {d.name}/assets/")
