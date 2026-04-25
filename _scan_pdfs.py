from pathlib import Path
root = Path("backend/data/exams")
for s in sorted(root.iterdir()):
    if not s.is_dir(): continue
    for e in sorted(s.iterdir()):
        if not e.is_dir(): continue
        pdfs = list((e/"pdfs").glob("*.pdf")) if (e/"pdfs").exists() else []
        pages = list((e/"pages").glob("*.jpg")) if (e/"pages").exists() else []
        if pdfs:
            status = "OK" if pages else "NO_PAGES"
            print(f"  [{status}] {s.name}/{e.name}: {len(pdfs)} pdf(s), {len(pages)} page(s)")
