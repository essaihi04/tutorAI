"""Quick probe: does each PC PDF have a native text layer?"""
import fitz
from pathlib import Path

d = Path(__file__).resolve().parent.parent / "cours 2bac pc" / "PC"
print(f"Scanning: {d}\n")
for p in sorted(d.glob("*.pdf")):
    doc = fitz.open(p)
    page_chars = [len(page.get_text("text").strip()) for page in doc]
    with_text = sum(1 for c in page_chars if c > 50)
    total = len(page_chars)
    avg = sum(page_chars) / total if total else 0
    marker = "OK" if with_text >= total * 0.8 else ("PARTIAL" if with_text > 0 else "SCANNED")
    print(f"[{marker:8s}] {p.name}: {total} pages, {with_text} with text, avg {avg:.0f} chars/page")
    doc.close()
