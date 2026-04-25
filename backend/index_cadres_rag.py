"""
Script to force OCR extraction of cadres de référence PDFs and rebuild RAG index.
Run this once to extract text from scanned PDFs using Gemini Vision.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app.services.rag_service import get_rag_service

def main():
    print("=" * 60)
    print("INDEXATION DES CADRES DE RÉFÉRENCE BAC")
    print("=" * 60)
    
    rag = get_rag_service()
    
    # Force reindex to trigger fresh OCR extraction
    print("\n[1/2] Indexation des cours SVT...")
    rag.index_subject("SVT", force_reindex=False)  # Use cache if available
    
    print("\n[2/2] Indexation des cadres de référence (OCR Gemini)...")
    print("    - Mathématiques")
    print("    - Physique-Chimie") 
    print("    - SVT")
    rag.index_cadres_de_reference(force_reindex=True)  # Force fresh OCR
    
    print("\n" + "=" * 60)
    print(f"TERMINÉ: {len(rag.documents)} chunks indexés au total")
    print("=" * 60)
    
    # Show breakdown by subject
    subjects = {}
    for doc in rag.documents:
        subj = doc.get('subject', 'Unknown')
        doc_type = doc.get('doc_type', 'cours')
        key = f"{subj} ({doc_type})"
        subjects[key] = subjects.get(key, 0) + 1
    
    print("\nRépartition par matière:")
    for subj, count in sorted(subjects.items()):
        print(f"  - {subj}: {count} chunks")
    
    # Test search
    print("\n" + "-" * 60)
    print("TEST DE RECHERCHE:")
    
    test_queries = [
        "dérivée fonction limite",
        "glycolyse ATP",
        "acide base pH",
        "mécanique Newton"
    ]
    
    for query in test_queries:
        results = rag.search(query, top_k=2)
        print(f"\n  Query: '{query}'")
        for r in results[:2]:
            subj = r.get('subject', '?')
            doc_type = r.get('doc_type', 'cours')
            source = r.get('source', '?')[:30]
            text_preview = r.get('text', '')[:80].replace('\n', ' ')
            print(f"    → [{subj}|{doc_type}] {source}...")
            print(f"      \"{text_preview}...\"")

if __name__ == "__main__":
    main()
