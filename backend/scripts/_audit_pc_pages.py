"""Quick scan: read the first few kilobytes of each physique exam's
assets/*.jpg and pages/*.jpg page headers? That's not feasible from
raw JPG. Instead, report file counts + sizes per exam, and cross-
reference with PDFs in the folder. Goal: detect year mismatches.
"""
from pathlib import Path

ROOT = Path('backend/data/exams/physique')
for year_dir in sorted(ROOT.iterdir()):
    if not year_dir.is_dir():
        continue
    pages_dir = year_dir / 'pages'
    if not pages_dir.exists():
        print(f'{year_dir.name}: NO pages/')
        continue
    pages = sorted(pages_dir.glob('sujet_p*.jpg'))
    print(f'{year_dir.name}: {len(pages)} page(s)')
    pdfs = list(year_dir.glob('*.pdf'))
    if pdfs:
        for p in pdfs:
            print(f'  pdf: {p.name} ({p.stat().st_size//1024}KB)')
