"""
Script to extract cadres de référence with slower rate to avoid Gemini rate limiting.
Processes one page at a time with longer delays.
"""
import os
import sys
import time
import json
import base64
import hashlib
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import fitz  # PyMuPDF
import httpx
from app.config import get_settings

settings = get_settings()

CACHE_DIR = Path(__file__).parent / "data" / "rag_cache"
COURSES_DIR = Path(__file__).parent / "cours 2bac pc" / "cadres de references 2BAC PC"

CADRE_SUBJECT_MAP = {
    "maths": "Mathématiques",
    "physique-chimie": "Physique-Chimie",
    "svt": "SVT",
}

def detect_subject(filename: str) -> str:
    fname_lower = filename.lower()
    for key, subject in CADRE_SUBJECT_MAP.items():
        if key in fname_lower:
            return subject
    return "Général"

def get_pdf_hash(pdf_path: Path) -> str:
    with open(pdf_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def ocr_page_deepseek(image_bytes: bytes, page_num: int, pdf_name: str) -> str:
    """OCR a single page with DeepSeek Vision, with retries"""
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = """Extrais TOUT le texte visible de cette image de document officiel marocain.

INSTRUCTIONS:
1. Extrais chaque mot, chaque phrase, chaque tableau, chaque formule
2. Garde la structure: titres, sous-titres, paragraphes, listes
3. Pour les tableaux: utilise | pour séparer les colonnes
4. Pour les formules mathématiques: utilise la notation LaTeX si possible
5. Ne saute AUCUN texte, même petit ou en marge
6. Réponds UNIQUEMENT avec le texte extrait, sans commentaires

Si la page est vide ou ne contient que des images sans texte, réponds: [PAGE VIDE]"""

    for attempt in range(5):  # More retries
        try:
            response = httpx.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.deepseek_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_base64}"
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ],
                    "temperature": 0.1,
                    "max_tokens": 8192
                },
                timeout=120.0
            )
            
            if response.status_code == 200:
                data = response.json()
                text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                text = text.strip()
                if text == "[PAGE VIDE]":
                    return ""
                if text and len(text) > 10:
                    return text
                # Empty, retry
                print(f"  [!] Empty response, retry {attempt+1}/5...")
                time.sleep(2)
                continue
                
            elif response.status_code == 429:
                wait = (attempt + 1) * 10
                print(f"  [!] Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            else:
                print(f"  [!] Error {response.status_code}: {response.text[:100]}, retry...")
                time.sleep(3)
                continue
                
        except Exception as e:
            print(f"  [!] Exception: {e}, retry...")
            time.sleep(5)
            continue
    
    return ""

def extract_pdf(pdf_path: Path, subject: str) -> list[dict]:
    """Extract all pages from a PDF using OCR"""
    chunks = []
    doc = fitz.open(pdf_path)
    pdf_name = pdf_path.stem
    total_pages = len(doc)
    
    print(f"\n  Extracting {total_pages} pages from {pdf_name}...")
    
    for page_num, page in enumerate(doc):
        print(f"  Page {page_num + 1}/{total_pages}...", end=" ", flush=True)
        
        # Render page to image
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        
        text = ocr_page_deepseek(img_bytes, page_num + 1, pdf_name)
        
        if text:
            print(f"{len(text)} chars")
            # Split into chunks
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            current_chunk = ""
            for para in paragraphs:
                if len(current_chunk) + len(para) < 1000:
                    current_chunk += "\n" + para if current_chunk else para
                else:
                    if current_chunk:
                        chunks.append({
                            'text': current_chunk,
                            'source': pdf_name,
                            'page': page_num + 1,
                            'subject': subject,
                            'doc_type': 'cadre_reference',
                            'type': 'text'
                        })
                    current_chunk = para
            if current_chunk:
                chunks.append({
                    'text': current_chunk,
                    'source': pdf_name,
                    'page': page_num + 1,
                    'subject': subject,
                    'doc_type': 'cadre_reference',
                    'type': 'text'
                })
        else:
            print("0 chars (empty/image only)")
        
        # Wait between pages to avoid rate limiting
        if page_num < total_pages - 1:
            time.sleep(5)
    
    doc.close()
    return chunks

def main():
    print("=" * 60)
    print("EXTRACTION LENTE DES CADRES DE RÉFÉRENCE")
    print("(avec délais pour éviter le rate limiting)")
    print("=" * 60)
    
    if not COURSES_DIR.exists():
        print(f"ERROR: Directory not found: {COURSES_DIR}")
        return
    
    pdf_files = list(COURSES_DIR.glob("*.pdf"))
    print(f"\nFound {len(pdf_files)} PDF files")
    
    all_chunks = []
    
    for pdf_path in pdf_files:
        subject = detect_subject(pdf_path.name)
        cache_key = f"cadre_{subject.lower().replace(' ', '_').replace('-', '_')}"
        cache_path = CACHE_DIR / f"{cache_key}_rag_cache.json"
        
        print(f"\n{'='*40}")
        print(f"Processing: {pdf_path.name}")
        print(f"Subject: {subject}")
        
        # Check if already cached
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                cached_hash = cache_data.get('file_hashes', {}).get(pdf_path.name)
                current_hash = get_pdf_hash(pdf_path)
                if cached_hash == current_hash:
                    chunks = cache_data.get('documents', [])
                    print(f"  Using cache: {len(chunks)} chunks")
                    all_chunks.extend(chunks)
                    continue
            except:
                pass
        
        # Extract fresh
        chunks = extract_pdf(pdf_path, subject)
        
        # Save to cache
        cache_data = {
            'file_hashes': {pdf_path.name: get_pdf_hash(pdf_path)},
            'documents': chunks
        }
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        print(f"  Saved {len(chunks)} chunks to cache")
        all_chunks.extend(chunks)
        
        # Wait between PDFs
        print("  Waiting 10s before next PDF...")
        time.sleep(10)
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {len(all_chunks)} chunks extracted")
    print("=" * 60)
    
    # Show breakdown
    subjects = {}
    for chunk in all_chunks:
        subj = chunk.get('subject', 'Unknown')
        subjects[subj] = subjects.get(subj, 0) + 1
    
    print("\nPar matière:")
    for subj, count in sorted(subjects.items()):
        print(f"  - {subj}: {count} chunks")
    
    print("\nDone! Now restart the backend to use the new RAG index.")

if __name__ == "__main__":
    main()
