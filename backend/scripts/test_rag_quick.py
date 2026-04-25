"""Quick timing test: load RAG from caches, run a semantic search."""
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["RAG_DISABLED"] = "0"

from app.services.rag_service import get_rag_service

t0 = time.perf_counter()
rag = get_rag_service()
rag.index_all()
t_load = time.perf_counter() - t0

t1 = time.perf_counter()
results = rag.search("photosynthèse ATP phase claire", top_k=3)
t_search = time.perf_counter() - t1

t2 = time.perf_counter()
grounded = rag.build_grounded_context("photosynthèse ATP phase claire", subject="SVT", max_tokens=800)
t_ground = time.perf_counter() - t2

print(f"\n=== TIMINGS ===")
print(f"  index_all (from cache): {t_load:.2f}s")
print(f"  search (top-3):         {t_search*1000:.1f}ms")
print(f"  build_grounded_context: {t_ground*1000:.1f}ms")
print(f"\n=== TOP 3 for 'photosynthèse ATP phase claire' ===")
for r in results:
    sid = rag.make_src_id(r)
    print(f"  [src:{sid}] score={r['score']:.3f} | {r['text'][:90]}...")
print(f"\nGrounded context length: {len(grounded)} chars")
print(f"Citations in context: {len(rag.parse_citations(grounded))}")
