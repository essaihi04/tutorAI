"""
Script to index SVT course PDFs for RAG system.
Run this once to extract and index all PDF content.
Uses Gemini Vision OCR for scanned PDFs.
"""
import sys
import os
import time

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.rag_service import RAGService

def test_single_pdf():
    """Test OCR on a single PDF first"""
    print("=" * 60)
    print("Testing OCR on single PDF...")
    print("=" * 60)
    
    service = RAGService()
    svt_dir = service.courses_dir / "SVT"
    
    # Pick the smallest PDF for testing
    pdf_files = sorted(svt_dir.glob("*.pdf"), key=lambda p: p.stat().st_size)
    if not pdf_files:
        print("No PDFs found!")
        return False
    
    test_pdf = pdf_files[0]
    print(f"\nTesting with: {test_pdf.name} ({test_pdf.stat().st_size / 1024 / 1024:.1f} MB)")
    
    # Extract just first 2 pages
    import fitz
    doc = fitz.open(test_pdf)
    print(f"PDF has {len(doc)} pages")
    
    # Test OCR on page 1
    page = doc[0]
    text = page.get_text("text").strip()
    print(f"\nNative text extraction: {len(text)} chars")
    if text:
        print(f"Sample: {text[:200]}...")
    else:
        print("No native text - will use OCR")
        
        # Render and OCR
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        
        print(f"Image size: {len(img_bytes)} bytes")
        
        ocr_text = service._ocr_page_with_gemini(img_bytes, 1, test_pdf.stem)
        print(f"\nOCR result: {len(ocr_text)} chars")
        if ocr_text:
            print(f"Sample:\n{ocr_text[:500]}...")
            return True
        else:
            print("OCR failed!")
            return False
    
    doc.close()
    return True

def main():
    print("=" * 60)
    print("SVT Course Indexing for RAG System")
    print("=" * 60)
    
    # First test OCR on single page
    if not test_single_pdf():
        print("\nOCR test failed. Check Gemini API key.")
        return
    
    print("\n" + "=" * 60)
    print("OCR test passed! Starting full indexing...")
    print("This will take several minutes due to API rate limits.")
    print("=" * 60)
    
    service = RAGService()
    
    # Check if PDFs exist
    svt_dir = service.courses_dir / "SVT"
    pdf_files = list(svt_dir.glob("*.pdf"))
    print(f"\nFound {len(pdf_files)} PDF files")
    
    # Index with force reindex
    print("\nIndexing PDFs with OCR...")
    service.index_subject("SVT", force_reindex=True)
    
    print(f"\nIndexing complete!")
    print(f"Total chunks extracted: {len(service.documents)}")
    
    # Show sample chunks
    if service.documents:
        print("\nSample chunks:")
        for i, doc in enumerate(service.documents[:3]):
            print(f"\n--- Chunk {i+1} ({doc['source']}, page {doc['page']}) ---")
            print(doc['text'][:300] + "...")
    
    # Test search
    print("\n" + "=" * 60)
    print("Testing search functionality...")
    print("=" * 60)
    
    test_queries = [
        "glycolyse ATP",
        "respiration cellulaire mitochondrie",
        "ADN transcription",
        "photosynthèse"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = service.search(query, top_k=2)
        if results:
            for r in results:
                score = r.get('score', 0)
                score_str = f"{score:.3f}" if isinstance(score, float) else str(score)
                print(f"  [{r['source']} p.{r['page']}] Score: {score_str}")
                print(f"    {r['text'][:100]}...")
        else:
            print("  No results found")
    
    print("\n" + "=" * 60)
    print("RAG system ready for use!")
    print("=" * 60)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-only", action="store_true", help="Only test OCR on one page")
    args = parser.parse_args()
    
    if args.test_only:
        test_single_pdf()
    else:
        main()
