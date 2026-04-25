"""Quick verification script that the RAG cache is fully loaded and queryable.

Run on the server: .venv/bin/python scripts/verify_rag_server.py
"""
import sys, os
sys.path.insert(0, "/root/moalim/backend")
os.chdir("/root/moalim/backend")

from app.services.rag_service import get_rag_service

rag = get_rag_service()
rag.index_all()

print(f"\n=== RAG TOTAL: {len(rag.documents)} chunks ===\n")

by_subject = {}
by_source = {}
for d in rag.documents:
    meta = d.get("metadata", {})
    s = meta.get("subject", "?")
    src = meta.get("source", "?")
    by_subject[s] = by_subject.get(s, 0) + 1
    by_source.setdefault(s, set()).add(src)

print("Distribution par matiere:")
for s, c in sorted(by_subject.items(), key=lambda x: -x[1]):
    n_sources = len(by_source.get(s, set()))
    print(f"  {s:30s}: {c:5d} chunks ({n_sources} sources)")

print("\nTests de recherche RAG:")
queries = [
    ("glycolyse ATP mitochondrie", "SVT"),
    ("derivation fonction logarithme", "Mathematiques"),
    ("dipole RC charge condensateur", "Physique-Chimie"),
    ("acide base pH dosage", "Physique-Chimie"),
    ("genetique humaine croisement", "SVT"),
    ("limites continuite suite", "Mathematiques"),
]
for query, subj in queries:
    try:
        results = rag.search(query, top_k=3, subject=subj)
    except TypeError:
        results = rag.search(query, top_k=3)
    print(f"\n  Q: {query!r:55s} ({subj})")
    print(f"     -> {len(results)} hits")
    for r in results[:2]:
        meta = r.get("metadata", {}) if isinstance(r, dict) else {}
        src = (meta.get("source", "?") or "?")[:55]
        sc = r.get("score", 0) if isinstance(r, dict) else 0
        print(f"     [{meta.get('subject','?'):20s}] {src} score={sc:.2f}")

print("\nDone.")
