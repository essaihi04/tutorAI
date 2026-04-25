from pathlib import Path
from collections import Counter

root = Path("backend/data/exams/physique")
all_names = []
for d in sorted(root.iterdir()):
    if not d.is_dir():
        continue
    a = d / "assets"
    files = sorted(p.name for p in a.glob("*.png")) if a.exists() else []
    all_names.extend(files)
    print(f"{d.name:<20} ({len(files):>2} files): {files}")

print("\n=== Unique prefixes ===")
prefixes = Counter()
for n in all_names:
    stem = n.rsplit(".",1)[0]
    # strip trailing digits/letters after "p<digit>"
    prefixes[stem.split("p")[0] if "p" in stem else stem] += 1
for k,v in prefixes.most_common():
    print(f"  {k}: {v}")
