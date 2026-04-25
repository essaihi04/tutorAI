"""
End-to-end smoke test for the citation-grounded RAG.

  1. Loads the 3 course caches (SVT, Math, PC) + cadres + exams.
  2. Runs a sample query per subject.
  3. Prints the grounded context (checks [src:...] tags appear).
  4. Simulates an LLM answer with citations, verifies parse_citations + resolver.

Run: python backend/scripts/test_rag_citations.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# RAG must be enabled for this test
os.environ["RAG_DISABLED"] = "0"

from app.services.rag_service import get_rag_service


SAMPLE_QUERIES = [
    ("SVT", "Qu'est-ce que la photosynthèse ?"),
    ("Math", "Définition de la dérivée d'une fonction en un point"),
    ("PC", "Loi de Newton sur le mouvement"),
]


def banner(msg: str, char: str = "=") -> None:
    print("\n" + char * 72)
    print(msg)
    print(char * 72)


def main() -> None:
    banner("1/4 Loading RAG")
    rag = get_rag_service()
    rag.index_all()
    print(f"  Total chunks: {len(rag.documents)}")
    by_subject: dict[str, int] = {}
    for d in rag.documents:
        key = d.get("subject", "?")
        by_subject[key] = by_subject.get(key, 0) + 1
    for s, n in sorted(by_subject.items()):
        print(f"    · {s}: {n}")

    banner("2/4 Grounded context per subject")
    all_seen_ids: list[str] = []
    for subject, query in SAMPLE_QUERIES:
        print(f"\n  [Query] ({subject}) {query}")
        grounded = rag.build_grounded_context(query, subject=subject, max_tokens=600)
        if not grounded:
            print("    → no context")
            continue
        # Count src tags
        import re
        ids = re.findall(r"\[src:([^\]\s]+)\]", grounded)
        unique_ids = list(dict.fromkeys(ids))
        all_seen_ids.extend(unique_ids)
        print(f"    → {len(unique_ids)} unique sources: {unique_ids[:4]}{'...' if len(unique_ids) > 4 else ''}")
        # Print first 350 chars to show the structure
        preview = grounded[:500].replace("\n", "\n      ")
        print(f"    Preview:\n      {preview}...")

    banner("3/4 parse_citations() from a simulated LLM answer")
    ids_to_test = all_seen_ids[:3] if len(all_seen_ids) >= 3 else all_seen_ids
    fake_answer = (
        "📚 **Explication:** La photosynthèse produit de l'ATP pendant la phase claire "
        f"[src:{ids_to_test[0]}]. Elle se déroule dans les chloroplastes "
        f"[src:{ids_to_test[1] if len(ids_to_test) > 1 else ids_to_test[0]}].\n"
        "📝 **Exemple:** Les plantes vertes sont autotrophes "
        f"[src:{ids_to_test[0]}].\n"
        "❓ **Question:** Quelle est la phase indépendante de la lumière ?"
    )
    print(f"  Fake answer:\n{fake_answer}\n")
    parsed = rag.parse_citations(fake_answer)
    print(f"  parse_citations → {parsed}")

    banner("4/4 get_citation_sources() resolves IDs back to docs")
    resolved = rag.get_citation_sources(parsed)
    for r in resolved:
        print(f"  · [src:{r['id']}]")
        print(f"      subject={r['subject']} | source={r['source']} | page={r['page']} | type={r['type']}")
        print(f"      preview: {r['preview'][:140]}")

    banner("✓ All steps completed", "═")
    print(f"  {len(rag.documents)} chunks, {len(all_seen_ids)} sources cited in samples, "
          f"{len(resolved)} resolved back to docs")


if __name__ == "__main__":
    main()
