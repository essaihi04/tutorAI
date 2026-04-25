"""Detailed verification of RAG content distribution + queryability."""
import sys, os, json
sys.path.insert(0, "/root/moalim/backend")
os.chdir("/root/moalim/backend")

from app.services.rag_service import get_rag_service

rag = get_rag_service()
rag.index_all()

print(f"\n=== RAG TOTAL: {len(rag.documents)} chunks ===\n")

if rag.documents:
    sample = rag.documents[0]
    print("Sample document keys:", list(sample.keys()))
    print("Sample document fields:")
    for k, v in sample.items():
        s = str(v)[:80].replace("\n", " ")
        print(f"  {k}: {s}")
    print()

# Try to discover subject from any field
def get_subject(d):
    for key in ("subject", "matiere", "type"):
        if key in d:
            return d[key]
    meta = d.get("metadata") or {}
    if isinstance(meta, dict):
        for key in ("subject", "matiere"):
            if key in meta:
                return meta[key]
    src = (d.get("source") or "").lower()
    if any(t in src for t in ("svt", "biolog")):
        return "SVT"
    if any(t in src for t in ("math", "exp", "logarit")):
        return "Mathematiques"
    if any(t in src for t in ("pc1.ma", "physiq", "chimi", "newton", "rlc", "acide", "dipole")):
        return "Physique-Chimie"
    if "cadre" in src:
        return "Cadre-de-reference"
    if "exam" in src or "national" in src:
        return "Examen"
    return "Inconnu"

dist = {}
sources = {}
for d in rag.documents:
    s = get_subject(d)
    dist[s] = dist.get(s, 0) + 1
    sources.setdefault(s, set()).add(d.get("source") or "?")

print("Distribution par matiere/categorie:")
for s in sorted(dist.keys(), key=lambda k: -dist[k]):
    print(f"  {s:30s}: {dist[s]:5d} chunks  ({len(sources[s])} sources)")

# Sample sources for each
print("\nExemples de sources par categorie:")
for s, srcs in sources.items():
    print(f"\n  --- {s} ---")
    for src in list(srcs)[:6]:
        print(f"     - {src[:80]}")

# Search tests
print("\n\n=== Tests de recherche RAG ===")
queries = [
    ("glycolyse ATP mitochondrie", "SVT"),
    ("derivation fonction logarithme", "Mathematiques"),
    ("dipole RC charge condensateur", "Physique-Chimie"),
    ("acide base pH dosage", "Physique-Chimie"),
    ("genetique humaine croisement", "SVT"),
    ("nombre complexe argument module", "Mathematiques"),
    ("ondes mecaniques periodiques", "Physique-Chimie"),
    ("chromosome ADN replication", "SVT"),
]
for query, subj in queries:
    try:
        results = rag.search(query, top_k=3, subject=subj)
    except TypeError:
        results = rag.search(query, top_k=3)
    print(f"\n  Q: {query!r}  (subject={subj})")
    print(f"     -> {len(results)} hits")
    for r in results[:3]:
        if not isinstance(r, dict):
            print(f"     {r}")
            continue
        src = (r.get("source") or "?")[:50]
        sc = r.get("score", 0)
        text_preview = (r.get("text") or "")[:60].replace("\n", " ")
        print(f"     [{get_subject(r):20s}] {src:55s} score={sc:.2f}")
        print(f"     -> {text_preview}...")

print("\nDone.")
