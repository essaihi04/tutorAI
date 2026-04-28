"""Clear ``src`` fields in mock exam JSON for documents whose image file
hasn't actually been uploaded yet, so the frontend doesn't try to load
broken images.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent / "data" / "mock_exams"


def walk_docs(node):
    """Yield every document dict found inside a mock exam tree."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "documents" and isinstance(v, list):
                for d in v:
                    if isinstance(d, dict):
                        yield d
            else:
                yield from walk_docs(v)
    elif isinstance(node, list):
        for item in node:
            yield from walk_docs(item)


def process(exam_dir: Path) -> int:
    exam_path = exam_dir / "exam.json"
    if not exam_path.exists():
        return 0
    raw = json.loads(exam_path.read_text(encoding="utf-8-sig"))
    assets_dir = exam_dir / "assets"
    uploaded = {f.stem for f in assets_dir.glob("*") if f.is_file()} if assets_dir.exists() else set()
    cleared = 0
    for doc in walk_docs(raw):
        src = doc.get("src")
        doc_id = doc.get("id")
        if src and doc_id and doc_id not in uploaded:
            doc["src"] = ""
            cleared += 1
    if cleared:
        exam_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    return cleared


total = 0
for subj in ROOT.iterdir():
    if not subj.is_dir():
        continue
    for exam in subj.iterdir():
        if exam.is_dir():
            n = process(exam)
            if n:
                print(f"[{subj.name}/{exam.name}] cleared {n} orphan src")
                total += n
print(f"Done. Total cleared: {total}")
