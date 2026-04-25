"""Smoke test for get_exam_inspiration + get_recent_exams_for_subject."""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["RAG_DISABLED"] = "0"

from app.services.rag_service import get_rag_service

rag = get_rag_service()
rag.index_all()

for subject in ["SVT", "Mathématiques", "Physique", "Chimie"]:
    print(f"\n=== {subject} ===")
    exams = rag.get_recent_exams_for_subject(subject, n=4)
    print(f"  4 exams récents: {[e['id'] for e in exams]}")
    insp = rag.get_exam_inspiration(subject, n=3, years=["2024", "2025"])
    print(f"  3 questions BAC 2024-2025:")
    for q in insp:
        preview = q["text"][:120].replace("\n", " ")
        print(f"    [{q['src_id']}] year={q['year']} topic={q['topic'] or '?':30} -> {preview}...")

# Test avec exclude_topics
print(f"\n=== SVT avec exclusion topic 'photosynthèse' ===")
insp = rag.get_exam_inspiration("SVT", n=3, years=["2024", "2025"], exclude_topics=["photosynthèse", "génétique"])
for q in insp:
    print(f"  topic={q['topic'] or '?':30} year={q['year']}")
