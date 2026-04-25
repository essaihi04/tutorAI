"""
RAG Service for BAC Course Content (all subjects)
Extracts text and images from PDFs and provides semantic search
to ensure AI responses are grounded in official curriculum content.
Supports SVT courses + cadres de référence for Math, Physique-Chimie, SVT.
"""
import os
import re
import json
import hashlib
import base64
import httpx
from pathlib import Path
from typing import Optional
import numpy as np

# PDF extraction
import fitz  # PyMuPDF
from PIL import Image
import io

# For embeddings and vector search
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("[RAG] Warning: sentence-transformers or faiss not installed. Using keyword search fallback.")

from app.config import get_settings
settings = get_settings()

# ─── RAG + OCR KILL-SWITCH ────────────────────────────────────────────
# Set RAG_DISABLED=0 in .env to enable indexing/search/OCR.
# When disabled, all public methods become no-ops so nothing hits Gemini
# or builds embeddings. This protects against runaway rate-limit loops.
RAG_DISABLED = getattr(settings, 'rag_disabled', 1) != 0
if RAG_DISABLED:
    print(f"[RAG] DISABLED via config (rag_disabled={getattr(settings, 'rag_disabled', 'N/A')}). All RAG + OCR calls are no-ops.")


class RAGService:
    """
    Retrieval-Augmented Generation service for BAC courses.
    Extracts content from PDFs and provides semantic search.
    Indexes subject-specific courses AND cadres de référence.
    """
    
    def __init__(self, courses_dir: str = None):
        self.base_dir = Path(__file__).parent.parent.parent  # backend/
        self.courses_dir = Path(courses_dir) if courses_dir else self.base_dir / "cours 2bac pc"
        self.cache_dir = self.base_dir / "data" / "rag_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Document storage
        self.documents: list[dict] = []  # List of {text, metadata, embedding}
        self.index = None  # FAISS index
        
        # Embedding model (multilingual for French/Arabic)
        self.model = None
        self.embedding_dim = 384  # Default for MiniLM
        
        # Track which subjects/sources have been indexed
        self._indexed_sources: set[str] = set()
        self._initialized = False
        
        # Map cadre de ref filenames to subject tags
        self._cadre_subject_map = {
            "cadre-de-reference-de-l-examen-national-maths": "Mathématiques",
            "cadre-de-reference-de-l-examen-national-physique-chimie": "Physique-Chimie",
            "cadre-de-reference-de-l-examen-national-svt": "SVT",
        }
        
    def _get_cache_path(self, subject: str) -> Path:
        """Get cache file path for a subject"""
        return self.cache_dir / f"{subject.lower()}_rag_cache.json"
    
    def _get_pdf_hash(self, pdf_path: Path) -> str:
        """Get hash of PDF file for cache invalidation"""
        with open(pdf_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _load_embedding_model(self):
        """Load the sentence transformer model"""
        if not EMBEDDINGS_AVAILABLE:
            return
        if self.model is None:
            print("[RAG] Loading embedding model...")
            # Use multilingual model for French/Arabic support
            self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            print(f"[RAG] Model loaded. Embedding dim: {self.embedding_dim}")
    
    # ─── Legacy Gemini OCR removed ─────────────────────────────────
    # Gemini Vision was previously used to OCR scanned PDF pages during
    # RAG indexing. This produced rate-limit storms in production and
    # blocked the event loop. Since the cache (data/rag_cache/*.json)
    # contains all the chunks needed for the official BAC programs, we
    # no longer call any external OCR provider here. If a subject's
    # cache is stale, this returns "" and indexing logs a warning.
    # If full OCR is needed again, wire `app.services.ocr_service`
    # (Mistral OCR) here.
    _OCR_DISABLED_LOGGED = False

    def _ocr_page_with_gemini(self, page_image_bytes: bytes, page_num: int, pdf_name: str, max_retries: int = 3) -> str:
        """OCR is disabled — Gemini removed. Returns empty string.

        RAG indexing relies exclusively on the pre-built cache files.
        """
        if not self._OCR_DISABLED_LOGGED:
            print("[RAG] OCR disabled (Gemini removed). Indexing relies on existing cache only.")
            type(self)._OCR_DISABLED_LOGGED = True
        return ""

    def extract_pdf_content(self, pdf_path: Path, use_ocr: bool = True, force_ocr: bool = False) -> list[dict]:
        """
        Extract text and images from a PDF file.
        Uses Gemini Vision OCR for scanned PDFs.
        Returns list of chunks with metadata.
        """
        if RAG_DISABLED:
            return []
        chunks = []
        
        try:
            doc = fitz.open(pdf_path)
            pdf_name = pdf_path.stem  # e.g., "Cours-Unit1-1"
            
            # Parse unit and chapter from filename
            parts = pdf_name.replace("Cours-", "").split("-")
            unit_info = parts[0] if parts else "Unknown"  # e.g., "Unit1"
            
            for page_num, page in enumerate(doc):
                # First try native text extraction unless OCR is forced
                text = ""
                if not force_ocr:
                    text = page.get_text("text").strip()
                
                # If no text found and OCR is enabled, use Gemini Vision
                if use_ocr and (force_ocr or not text):
                    import time
                    # Render page to image
                    mat = fitz.Matrix(2, 2)  # 2x zoom for better OCR
                    pix = page.get_pixmap(matrix=mat)
                    img_bytes = pix.tobytes("png")
                    
                    text = self._ocr_page_with_gemini(img_bytes, page_num + 1, pdf_name)
                    print(f"[RAG] OCR page {page_num + 1}/{len(doc)} of {pdf_name}: {len(text)} chars")
                    
                    # Add delay between pages to avoid rate limiting
                    if page_num < len(doc) - 1:
                        time.sleep(3)
                
                if text:
                    # Split into paragraphs for better chunking
                    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
                    
                    current_chunk = ""
                    for para in paragraphs:
                        # Combine small paragraphs, split large ones
                        if len(current_chunk) + len(para) < 1000:
                            current_chunk += "\n" + para if current_chunk else para
                        else:
                            if current_chunk:
                                chunks.append({
                                    'text': current_chunk,
                                    'source': pdf_name,
                                    'page': page_num + 1,
                                    'unit': unit_info,
                                    'type': 'text'
                                })
                            current_chunk = para
                    
                    # Don't forget the last chunk
                    if current_chunk:
                        chunks.append({
                            'text': current_chunk,
                            'source': pdf_name,
                            'page': page_num + 1,
                            'unit': unit_info,
                            'type': 'text'
                        })
                
                # Extract images with captions
                images = page.get_images()
                for img_idx, img in enumerate(images):
                    try:
                        # Get image info
                        xref = img[0]
                        # Extract surrounding text as potential caption
                        img_rect = page.get_image_rects(xref)
                        if img_rect:
                            # Get text near the image
                            rect = img_rect[0]
                            nearby_text = page.get_text("text", clip=fitz.Rect(
                                rect.x0 - 50, rect.y0 - 30,
                                rect.x1 + 50, rect.y1 + 50
                            ))
                            if nearby_text.strip():
                                chunks.append({
                                    'text': f"[Figure/Schéma] {nearby_text.strip()}",
                                    'source': pdf_name,
                                    'page': page_num + 1,
                                    'unit': unit_info,
                                    'type': 'image_caption',
                                    'image_index': img_idx
                                })
                    except Exception as e:
                        continue  # Skip problematic images
            
            doc.close()
            print(f"[RAG] Extracted {len(chunks)} chunks from {pdf_name}")
            
        except Exception as e:
            print(f"[RAG] Error extracting {pdf_path}: {e}")
        
        return chunks
    
    def _detect_cadre_subject(self, filename: str) -> str:
        """Detect which subject a cadre de référence PDF belongs to."""
        fname_lower = filename.lower()
        for prefix, subject in self._cadre_subject_map.items():
            if prefix in fname_lower:
                return subject
        return "Général"

    def _index_single_source(self, source_key: str, pdf_files: list[Path], subject_tag: str, force_reindex: bool = False) -> list[dict]:
        """
        Index a set of PDFs for a given source key.
        Returns the list of document chunks (from cache or freshly extracted).
        """
        if not pdf_files:
            return []

        cache_path = self._get_cache_path(source_key)
        
        # Check cache validity
        if cache_path.exists() and not force_reindex:
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                cached_hashes = cache_data.get('file_hashes', {})
                current_hashes = {p.name: self._get_pdf_hash(p) for p in pdf_files}
                if cached_hashes == current_hashes:
                    docs = cache_data.get('documents', [])
                    if docs:  # Only use cache if it actually has documents
                        print(f"[RAG] Loaded {len(docs)} chunks from cache for {source_key}")
                        return docs
                    else:
                        print(f"[RAG] Cache for {source_key} has 0 documents — re-indexing")
            except Exception as e:
                print(f"[RAG] Cache load error for {source_key}: {e}")
        
        # Extract fresh
        print(f"[RAG] Indexing {len(pdf_files)} PDFs for {source_key}...")
        docs = []
        for pdf_path in pdf_files:
            force_ocr_for_pdf = "cadre-de-reference" in pdf_path.name.lower()
            chunks = self.extract_pdf_content(pdf_path, use_ocr=True, force_ocr=force_ocr_for_pdf)
            # Tag each chunk with the subject
            for chunk in chunks:
                chunk['subject'] = subject_tag
            docs.extend(chunks)
        
        # Save to cache only if we got actual documents (don't cache failures)
        if docs:
            cache_data = {
                'file_hashes': {p.name: self._get_pdf_hash(p) for p in pdf_files},
                'documents': docs
            }
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            print(f"[RAG] Indexed {len(docs)} chunks for {source_key}, saved to cache")
        else:
            print(f"[RAG] WARNING: 0 chunks extracted for {source_key} from {len(pdf_files)} PDFs — NOT caching")
        return docs

    def index_subject(self, subject: str = "SVT", force_reindex: bool = False, build_index: bool = True):
        """
        Index all PDFs for a subject.
        Uses caching to avoid re-processing unchanged files.

        Pass build_index=False when calling from index_all() so FAISS is built
        only once at the end (re-embedding the full corpus is expensive).
        """
        if RAG_DISABLED:
            return
        if subject in self._indexed_sources and not force_reindex:
            return  # Already indexed

        subject_dir = self.courses_dir / subject
        if not subject_dir.exists():
            print(f"[RAG] Subject directory not found: {subject_dir}")
            return

        pdf_files = list(subject_dir.glob("*.pdf"))
        docs = self._index_single_source(subject, pdf_files, subject, force_reindex)
        
        # Merge into main document store (avoid duplicates)
        self.documents = [d for d in self.documents if d.get('subject') != subject]
        self.documents.extend(docs)
        self._indexed_sources.add(subject)
        
        # Rebuild FAISS index with all documents (skipped during index_all batching)
        if build_index and EMBEDDINGS_AVAILABLE and self.documents:
            self._build_faiss_index()
        
        self._initialized = True

    def _load_json_cadre_maths(self, json_data: list, filename: str) -> list[dict]:
        """Parse Math cadre de référence JSON into chunks"""
        chunks = []
        subject = "Mathématiques"
        
        # First, collect all domains for a summary
        all_domains = []
        for page in json_data:
            if page.get("language") == "ar":
                continue
            content = page.get("content", {})
            main_domain = content.get("main_domain", "")
            if main_domain and main_domain not in all_domains:
                all_domains.append(main_domain)
            for sd in content.get("sub_domains", []):
                sd_name = sd.get("name", "")
                if sd_name and sd_name not in all_domains:
                    all_domains.append(sd_name)
        
        if all_domains:
            domains_text = "\n".join(f"- {d}" for d in all_domains)
            chunks.append({
                'text': f"""[{subject}] PROGRAMME OFFICIEL MATHÉMATIQUES 2BAC SCIENCES PHYSIQUES - MAROC (BIOF)

COEFFICIENT BAC: 7 (Baccalauréat marocain 2BAC Sciences Physiques BIOF)

Domaines et sous-domaines du programme:
{domains_text}

⚠️ Ce programme est DIFFÉRENT du programme français. Il s'agit du programme officiel marocain.""",
                'source': filename,
                'subject': subject,
                'doc_type': 'cadre_reference',
                'type': 'program_overview'
            })
        
        for page in json_data:
            page_num = page.get("page", 0)
            section = page.get("section", "")
            content = page.get("content", {})
            
            # Skip intro pages in Arabic
            if page.get("language") == "ar":
                continue
            
            # Process sub_domains with objectives
            sub_domains = content.get("sub_domains", [])
            for sd in sub_domains:
                sd_name = sd.get("name", "")
                objectives = sd.get("objectives", [])
                
                if objectives:
                    # Create one chunk per group of objectives
                    obj_text = "\n".join(f"- {obj}" for obj in objectives)
                    chunk_text = f"[{subject}] {sd_name}\n\nObjectifs:\n{obj_text}"
                    chunks.append({
                        'text': chunk_text,
                        'source': filename,
                        'page': page_num,
                        'subject': subject,
                        'domain': sd_name,
                        'doc_type': 'cadre_reference',
                        'type': 'objectives'
                    })
            
            # Process specification tables
            if "table_a_domaines" in content:
                table = content["table_a_domaines"]
                rows_text = "\n".join(
                    f"- {r['domaine']}: {r['sous_domaines']} ({r['taux_importance']})"
                    for r in table.get("rows", [])
                )
                chunks.append({
                    'text': f"[{subject}] Répartition des domaines à l'examen:\n{rows_text}",
                    'source': filename,
                    'page': page_num,
                    'subject': subject,
                    'doc_type': 'cadre_reference',
                    'type': 'exam_weights'
                })
            
            if "table_b_habilete" in content:
                table = content["table_b_habilete"]
                rows_text = "\n".join(
                    f"- {r['niveau']}: {r['taux_importance']}"
                    for r in table.get("rows", [])
                )
                chunks.append({
                    'text': f"[{subject}] Niveaux d'habileté à l'examen:\n{rows_text}",
                    'source': filename,
                    'page': page_num,
                    'subject': subject,
                    'doc_type': 'cadre_reference',
                    'type': 'exam_skills'
                })
        
        return chunks

    def _load_json_cadre_pc(self, json_data: list, filename: str) -> list[dict]:
        """Parse Physique-Chimie cadre de référence JSON into chunks"""
        chunks = []
        
        # Extract weights first for use in summaries
        phys_weights = {}
        chem_weights = {}
        skill_levels = []
        
        for item in json_data:
            weights = item.get("weight_tables", {})
            if weights:
                domains_weights = weights.get("domains_weights", {})
                if "PHYSIQUE" in domains_weights:
                    phys_data = domains_weights["PHYSIQUE"]
                    phys_weights = {
                        'total': phys_data.get("total_weight", "67%"),
                        'details': {d['sub_domain']: d['weight'] for d in phys_data.get("details", [])}
                    }
                if "CHIMIE" in domains_weights:
                    chem_data = domains_weights["CHIMIE"]
                    chem_weights = {
                        'total': chem_data.get("total_weight", "33%"),
                        'details': {d['sub_domain']: d['weight'] for d in chem_data.get("details", [])}
                    }
                skill_levels = weights.get("skill_levels_weights", [])
        
        # Create comprehensive summary chunk for Physique-Chimie exam
        chunks.append({
            'text': f"""[Physique-Chimie] RÉPARTITION OFFICIELLE DES POINTS À L'EXAMEN BAC - MAROC (BIOF)

STRUCTURE DE L'EXAMEN PHYSIQUE-CHIMIE (Coefficient 7):
- PHYSIQUE: {phys_weights.get('total', '67%')} de l'examen
- CHIMIE: {chem_weights.get('total', '33%')} de l'examen

DÉTAIL DES POINTS PAR DOMAINE EN PHYSIQUE ({phys_weights.get('total', '67%')}):
- Ondes: {phys_weights.get('details', {}).get('Ondes', '11%')}
- Transformations nucléaires: {phys_weights.get('details', {}).get('Transformations nucléaires', '8%')}
- Électricité: {phys_weights.get('details', {}).get('Electricité', '21%')}
- Mécanique: {phys_weights.get('details', {}).get('Mécanique', '27%')}

DÉTAIL DES POINTS PAR DOMAINE EN CHIMIE ({chem_weights.get('total', '33%')}):
- Transformations rapides et lentes: {chem_weights.get('details', {}).get('Transformations rapides et lentes', '6%')}
- Transformations non totales: {chem_weights.get('details', {}).get('Transformations non totales', '10%')}
- Sens d'évolution: {chem_weights.get('details', {}).get("Sens d'évolution", '10%')}
- Méthode de contrôle: {chem_weights.get('details', {}).get('Méthode de contrôle', '7%')}

CONSEILS STRATÉGIQUES:
1. La MÉCANIQUE (27%) est le domaine le plus important en Physique - à maîtriser en priorité
2. L'ÉLECTRICITÉ (21%) est le 2ème domaine clé - circuits RC, RL, RLC
3. En Chimie, les TRANSFORMATIONS NON TOTALES et SENS D'ÉVOLUTION (10% chacun) sont prioritaires
4. Les ONDES (11%) et NUCLÉAIRE (8%) sont plus légers mais ne pas négliger

⚠️ Ce sont les poids officiels du cadre de référence marocain 2015.""",
            'source': filename,
            'subject': "Physique-Chimie",
            'doc_type': 'cadre_reference',
            'type': 'exam_weights'
        })
        
        # Create summary chunks for Physics and Chemistry programs
        for item in json_data:
            physics = item.get("content_structure_physics", {})
            chemistry = item.get("content_structure_chemistry", {})
            
            if physics:
                phys_domains = [sd.get("title", "") for sd in physics.get("sub_domains", [])]
                if phys_domains:
                    domains_with_weights = []
                    for d in phys_domains:
                        # Extract domain name without "Sous domaine X : "
                        domain_name = d.split(":")[-1].strip() if ":" in d else d
                        weight = phys_weights.get('details', {}).get(domain_name, "")
                        domains_with_weights.append(f"- {d} ({weight})" if weight else f"- {d}")
                    
                    chunks.append({
                        'text': f"""[Physique] PROGRAMME OFFICIEL PHYSIQUE 2BAC SCIENCES PHYSIQUES - MAROC (BIOF)

Poids total Physique à l'examen: {phys_weights.get('total', '67%')}

Sous-domaines du programme de Physique:
""" + "\n".join(domains_with_weights) + """

⚠️ Ce programme est DIFFÉRENT du programme français. Il s'agit du programme officiel marocain.""",
                        'source': filename,
                        'subject': "Physique",
                        'doc_type': 'cadre_reference',
                        'type': 'program_overview'
                    })
            
            if chemistry:
                chem_domains = [sd.get("title", "") for sd in chemistry.get("sub_domains", [])]
                if chem_domains:
                    domains_with_weights = []
                    for d in chem_domains:
                        domain_name = d.split(":")[-1].strip() if ":" in d else d
                        weight = chem_weights.get('details', {}).get(domain_name, "")
                        domains_with_weights.append(f"- {d} ({weight})" if weight else f"- {d}")
                    
                    chunks.append({
                        'text': f"""[Chimie] PROGRAMME OFFICIEL CHIMIE 2BAC SCIENCES PHYSIQUES - MAROC (BIOF)

Poids total Chimie à l'examen: {chem_weights.get('total', '33%')}

Sous-domaines du programme de Chimie:
""" + "\n".join(domains_with_weights) + """

⚠️ Ce programme est DIFFÉRENT du programme français. Il s'agit du programme officiel marocain.""",
                        'source': filename,
                        'subject': "Chimie",
                        'doc_type': 'cadre_reference',
                        'type': 'program_overview'
                    })
        
        # Add skill levels chunk
        if skill_levels:
            skills_text = "\n".join(
                f"- {s['level']}: {s['weight']}\n  Composantes: {', '.join(s.get('components', []))}"
                for s in skill_levels
            )
            chunks.append({
                'text': f"""[Physique-Chimie] NIVEAUX D'HABILETÉ ÉVALUÉS À L'EXAMEN BAC

{skills_text}

CONSEILS:
- 50% de l'examen = Utilisation des ressources (connaissances, définitions, lois)
- 35% = Résolution de problèmes (raisonnement, calculs)
- 15% = Application expérimentale (protocoles, exploitation de données)""",
                'source': filename,
                'subject': "Physique-Chimie",
                'doc_type': 'cadre_reference',
                'type': 'exam_skills'
            })
        
        for item in json_data:
            # Physics content
            physics = item.get("content_structure_physics", {})
            if physics:
                for sd in physics.get("sub_domains", []):
                    title = sd.get("title", "")
                    topics = sd.get("topics", [])
                    topics_text = "\n".join(f"- {t}" for t in topics)
                    chunks.append({
                        'text': f"[Physique] {title}\n\nContenu:\n{topics_text}",
                        'source': filename,
                        'subject': "Physique",
                        'domain': title,
                        'doc_type': 'cadre_reference',
                        'type': 'topics'
                    })
            
            # Chemistry content
            chemistry = item.get("content_structure_chemistry", {})
            if chemistry:
                for sd in chemistry.get("sub_domains", []):
                    title = sd.get("title", "")
                    topics = sd.get("topics", [])
                    topics_text = "\n".join(f"- {t}" for t in topics)
                    chunks.append({
                        'text': f"[Chimie] {title}\n\nContenu:\n{topics_text}",
                        'source': filename,
                        'subject': "Chimie",
                        'domain': title,
                        'doc_type': 'cadre_reference',
                        'type': 'topics'
                    })
            
            # Lab experiments
            annexes = item.get("annexes", {})
            if annexes and "annexe_2" in annexes:
                tp = annexes["annexe_2"]
                physics_tp = tp.get("physics_experiments", [])
                chemistry_tp = tp.get("chemistry_experiments", [])
                
                if physics_tp:
                    chunks.append({
                        'text': f"[Physique] Travaux pratiques officiels:\n" + "\n".join(f"- {t}" for t in physics_tp),
                        'source': filename,
                        'subject': "Physique",
                        'doc_type': 'cadre_reference',
                        'type': 'lab_experiments'
                    })
                if chemistry_tp:
                    chunks.append({
                        'text': f"[Chimie] Travaux pratiques officiels:\n" + "\n".join(f"- {t}" for t in chemistry_tp),
                        'source': filename,
                        'subject': "Chimie",
                        'doc_type': 'cadre_reference',
                        'type': 'lab_experiments'
                    })
        
        return chunks

    def _load_json_cadre_svt(self, json_data: dict, filename: str) -> list[dict]:
        """Parse SVT cadre de référence JSON into chunks"""
        chunks = []
        subject = "SVT"
        
        # First, create a summary chunk listing all domains with weights
        all_domains = []
        domain_weights = {}
        sections = json_data.get("sections", [])
        
        # Extract domain weights from tableau
        for section in sections:
            sous_sections = section.get("sous_sections", [])
            for ss in sous_sections:
                # Get weights from tableau
                tableau = ss.get("tableau", [])
                for entry in tableau:
                    dom_name = entry.get("domaine", "")
                    pct = entry.get("pourcentage_recouvrement", "")
                    if dom_name and pct:
                        domain_weights[dom_name] = pct
                
                # Get domain names
                domaines = ss.get("domaines", [])
                for dom in domaines:
                    dom_name = dom.get("nom", "")
                    if dom_name:
                        all_domains.append(dom_name)
        
        if all_domains:
            domains_text = "\n".join(f"- {d}" for d in all_domains)
            chunks.append({
                'text': f"""[{subject}] PROGRAMME OFFICIEL SVT 2BAC SCIENCES PHYSIQUES - MAROC (BIOF)

COEFFICIENT BAC: 5 (Baccalauréat marocain 2BAC Sciences Physiques BIOF)

Les 4 domaines du programme SVT (chacun vaut 25% = 5 points):
{domains_text}

STRUCTURE DE L'EXAMEN SVT (20 points total):
- Partie I: Restitution des connaissances (5 pts / 25%) - QCM, Vrai/Faux, définitions
- Partie II: Raisonnement scientifique (15 pts / 75%) - 3 exercices de 5 pts chacun

CONSEIL STRATÉGIQUE: Chaque domaine représente 25% de l'examen. Les 4 domaines sont équilibrés.
La partie raisonnement (75%) est plus importante que la restitution (25%).

⚠️ Ce programme est DIFFÉRENT du programme français. Il s'agit du programme officiel marocain.""",
                'source': filename,
                'subject': subject,
                'doc_type': 'cadre_reference',
                'type': 'program_overview'
            })
        
        # Get sections
        for section in sections:
            sous_sections = section.get("sous_sections", [])
            for ss in sous_sections:
                # Competences
                competences = ss.get("competences", [])
                if competences:
                    comp_text = "\n".join(f"- {c}" for c in competences)
                    chunks.append({
                        'text': f"[{subject}] Compétences visées:\n{comp_text}",
                        'source': filename,
                        'subject': subject,
                        'doc_type': 'cadre_reference',
                        'type': 'competences'
                    })
                
                # Domains with knowledge and objectives
                domaines = ss.get("domaines", [])
                for dom in domaines:
                    dom_name = dom.get("nom", "")
                    points_cles = dom.get("points_cles", [])
                    if points_cles:
                        points_text = "\n".join(f"- {p}" for p in points_cles)
                        chunks.append({
                            'text': f"[{subject}] {dom_name}\n\nPoints clés:\n{points_text}",
                            'source': filename,
                            'subject': subject,
                            'domain': dom_name,
                            'doc_type': 'cadre_reference',
                            'type': 'key_points'
                        })
                
                # Detailed table with knowledge and objectives
                tableau = ss.get("tableau", [])
                for entry in tableau:
                    domaine_name = entry.get("domaine", "")
                    pct = entry.get("pourcentage_recouvrement", "")
                    sous_domaines = entry.get("sous_domaines", [])
                    
                    for sd in sous_domaines:
                        sd_name = sd.get("nom", "")
                        connaissances = sd.get("connaissances", [])
                        objectifs = sd.get("objectifs", [])
                        
                        if connaissances:
                            conn_text = "\n".join(f"- {c}" for c in connaissances)
                            chunks.append({
                                'text': f"[{subject}] {sd_name}\n\nConnaissances:\n{conn_text}",
                                'source': filename,
                                'subject': subject,
                                'domain': domaine_name,
                                'sub_domain': sd_name,
                                'doc_type': 'cadre_reference',
                                'type': 'knowledge'
                            })
                        
                        if objectifs:
                            obj_text = "\n".join(f"- {o}" for o in objectifs)
                            chunks.append({
                                'text': f"[{subject}] {sd_name}\n\nObjectifs:\n{obj_text}",
                                'source': filename,
                                'subject': subject,
                                'domain': domaine_name,
                                'sub_domain': sd_name,
                                'doc_type': 'cadre_reference',
                                'type': 'objectives'
                            })
                
                # Extract habiletés (skills) table
                habiletes_tableau = ss.get("tableau", [])
                for entry in habiletes_tableau:
                    hab_domaine = entry.get("domaine_habiletes", "")
                    hab_importance = entry.get("importance", "")
                    hab_list = entry.get("habiletes", [])
                    if hab_domaine and hab_list:
                        hab_text = "\n".join(f"- {h}" for h in hab_list)
                        chunks.append({
                            'text': f"[{subject}] HABILETÉS ÉVALUÉES À L'EXAMEN: {hab_domaine} ({hab_importance})\n\n{hab_text}",
                            'source': filename,
                            'subject': subject,
                            'doc_type': 'cadre_reference',
                            'type': 'exam_skills'
                        })
        
        # Extract exam structure from section III
        for section in sections:
            structure = section.get("structure", {})
            if structure:
                partie1 = structure.get("partie_1", {})
                partie2 = structure.get("partie_2", {})
                
                if partie1 or partie2:
                    exam_text = f"""[{subject}] STRUCTURE DÉTAILLÉE DE L'EXAMEN NATIONAL SVT

PARTIE I - RESTITUTION DES CONNAISSANCES ({partie1.get('notation', '5 pts')}):
Objectif: {partie1.get('objectif', '')}
Types de questions: {', '.join(partie1.get('types_questions', []))}
Note: {partie1.get('note_domaine', '')}

PARTIE II - RAISONNEMENT SCIENTIFIQUE ({partie2.get('notation_totale', '15 pts')}):"""
                    
                    for ex in partie2.get("structure", []):
                        exam_text += f"\n- {ex.get('exercice', '')}: {ex.get('notation', '')} - {ex.get('domaine', '')}"
                    
                    exam_text += """

CONSEILS STRATÉGIQUES POUR L'EXAMEN:
1. Commencez par la Partie I (restitution) - questions rapides, 5 pts faciles
2. Lisez TOUS les exercices de la Partie II avant de commencer
3. Choisissez l'exercice où vous êtes le plus à l'aise en premier
4. Gérez votre temps: ~15 min pour Partie I, ~45 min pour chaque exercice de Partie II
5. Faites des schémas clairs et légendés - ils rapportent des points
6. Utilisez le vocabulaire scientifique précis du cours"""
                    
                    chunks.append({
                        'text': exam_text,
                        'source': filename,
                        'subject': subject,
                        'doc_type': 'cadre_reference',
                        'type': 'exam_structure'
                    })
        
        return chunks

    def index_cadres_de_reference(self, force_reindex: bool = False, build_index: bool = True):
        """
        Index cadres de référence from JSON files (structured exam reference frameworks).
        These cover Math, Physique-Chimie, and SVT official programs.

        Pass build_index=False when batching via index_all().
        Much faster and more accurate than OCR from PDFs.
        """
        if RAG_DISABLED:
            return
        cadres_dir = self.courses_dir / "cadres de references 2BAC PC"
        if not cadres_dir.exists():
            print(f"[RAG] Cadres de référence directory not found: {cadres_dir}")
            return

        if "cadres_ref" in self._indexed_sources and not force_reindex:
            return  # Already indexed

        # Look for JSON files first (preferred), fall back to PDF
        json_files = list(cadres_dir.glob("*.json"))
        
        if json_files:
            print(f"[RAG] Found {len(json_files)} JSON cadres de référence (using structured data)")
            all_cadre_docs = []
            
            for json_path in json_files:
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    filename = json_path.stem
                    
                    # Detect subject and use appropriate parser
                    if "maths" in filename.lower():
                        chunks = self._load_json_cadre_maths(data, filename)
                        print(f"[RAG] Loaded {len(chunks)} chunks from {filename} (Maths)")
                    elif "physique-chimie" in filename.lower():
                        chunks = self._load_json_cadre_pc(data, filename)
                        print(f"[RAG] Loaded {len(chunks)} chunks from {filename} (Physique-Chimie)")
                    elif "svt" in filename.lower():
                        chunks = self._load_json_cadre_svt(data, filename)
                        print(f"[RAG] Loaded {len(chunks)} chunks from {filename} (SVT)")
                    else:
                        print(f"[RAG] Unknown cadre format: {filename}")
                        continue
                    
                    all_cadre_docs.extend(chunks)
                    
                except Exception as e:
                    print(f"[RAG] Error loading {json_path.name}: {e}")
            
            # Remove old cadre docs, add new ones
            self.documents = [d for d in self.documents if d.get('doc_type') != 'cadre_reference']
            self.documents.extend(all_cadre_docs)
            self._indexed_sources.add("cadres_ref")
            
            print(f"[RAG] Total cadres de référence: {len(all_cadre_docs)} chunks indexed from JSON")
            
            # Rebuild FAISS index with all documents (skipped during batching)
            if build_index and EMBEDDINGS_AVAILABLE and self.documents:
                self._build_faiss_index()
            
            self._initialized = True
            return
        
        # Fallback to PDF if no JSON found
        pdf_files = list(cadres_dir.glob("*.pdf"))
        if not pdf_files:
            print("[RAG] No cadre de référence files found (JSON or PDF)")
            return

        print(f"[RAG] No JSON found, falling back to PDF OCR for {len(pdf_files)} files")
        all_cadre_docs = []
        for pdf_path in pdf_files:
            subject_tag = self._detect_cadre_subject(pdf_path.name)
            cache_key = f"cadre_{subject_tag.lower().replace(' ', '_').replace('-', '_')}"
            docs = self._index_single_source(cache_key, [pdf_path], subject_tag, force_reindex)
            for doc in docs:
                doc['doc_type'] = 'cadre_reference'
            all_cadre_docs.extend(docs)

        self.documents = [d for d in self.documents if d.get('doc_type') != 'cadre_reference']
        self.documents.extend(all_cadre_docs)
        self._indexed_sources.add("cadres_ref")
        
        print(f"[RAG] Total cadres de référence: {len(all_cadre_docs)} chunks indexed from PDF")
        
        if build_index and EMBEDDINGS_AVAILABLE and self.documents:
            self._build_faiss_index()
        
        self._initialized = True

    def index_exams(self, force_reindex: bool = False, build_index: bool = True):
        """
        Index national exam questions and corrections into the RAG store.
        This makes exam exercises retrievable in Libre and Coaching modes.

        Pass build_index=False when batching via index_all().
        """
        if RAG_DISABLED:
            return
        if "exams" in self._indexed_sources and not force_reindex:
            return

        exams_dir = self.base_dir / "data" / "exams"
        index_path = exams_dir / "index.json"
        if not index_path.exists():
            print("[RAG] No exam index.json found, skipping exam indexing")
            return

        with open(index_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)

        all_exam_docs = []
        for meta in catalog:
            exam_path = exams_dir / meta["path"] / "exam.json"
            if not exam_path.exists():
                continue
            try:
                with open(exam_path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                chunks = self._parse_exam_for_rag(raw, meta)
                all_exam_docs.extend(chunks)
                print(f"[RAG] Indexed {len(chunks)} chunks from exam {meta['id']}")
            except Exception as e:
                print(f"[RAG] Error indexing exam {meta['id']}: {e}")

        # Merge into document store
        self.documents = [d for d in self.documents if d.get("doc_type") != "exam"]
        self.documents.extend(all_exam_docs)
        self._indexed_sources.add("exams")

        print(f"[RAG] Total exam chunks indexed: {len(all_exam_docs)}")

        if build_index and EMBEDDINGS_AVAILABLE and self.documents:
            self._build_faiss_index()
        self._initialized = True

    def _parse_exam_for_rag(self, raw: dict, meta: dict) -> list[dict]:
        """Parse an exam JSON into RAG-indexable chunks (questions + corrections).
        Supports both the new clean 'parts' format and legacy 'blocks' format."""
        if "parts" in raw:
            return self._parse_clean_exam_for_rag(raw, meta)
        return self._parse_legacy_exam_for_rag(raw, meta)

    def _parse_clean_exam_for_rag(self, raw: dict, meta: dict) -> list[dict]:
        """Parse clean format (parts/exercises/questions) into RAG chunks."""
        chunks = []
        subject = meta["subject"]
        year = meta["year"]
        session = meta["session"]
        label = f"{subject} {year} {session}"
        q_index = 0
        all_topics = set()

        for part in raw.get("parts", []):
            part_name = part.get("name", "")

            # Direct questions in part
            for q in part.get("questions", []):
                sub_qs = q.get("sub_questions", [])
                items = sub_qs if sub_qs else [q]
                for item in items:
                    content = item.get("content", "")
                    corr = item.get("correction") or q.get("correction") or {}
                    corr_text = corr.get("content", "") if isinstance(corr, dict) else str(corr)

                    chunk_text = f"[Examen National {label}] Question {q_index+1}:\n{content}"
                    chunk_text += f"\nPartie: {part_name}"
                    if corr_text:
                        chunk_text += f"\n\nCorrection officielle:\n{corr_text}"

                    chunks.append({
                        "text": chunk_text,
                        "source": f"exam_{meta['id']}",
                        "subject": subject,
                        "doc_type": "exam",
                        "type": "exam_question",
                        "exam_year": year,
                        "exam_session": session,
                        "question_index": q_index,
                        "part_name": part_name,
                    })
                    q_index += 1

            # Questions inside exercises
            for ex in part.get("exercises", []):
                ex_name = ex.get("name", "")
                ex_topic = ex.get("topic", "")
                ex_context = ex.get("context", "")
                if ex_topic:
                    all_topics.add(ex_topic)

                for q in ex.get("questions", []):
                    content = q.get("content", "")
                    corr = q.get("correction") or {}
                    corr_text = corr.get("content", "") if isinstance(corr, dict) else str(corr)

                    chunk_text = f"[Examen National {label} — {ex_name}] Question {q_index+1}:\n{content}"
                    if ex_topic:
                        chunk_text += f"\nThème: {ex_topic}"
                    if ex_context:
                        chunk_text += f"\nContexte: {ex_context[:200]}"
                    chunk_text += f"\nPartie: {part_name}"
                    if corr_text:
                        chunk_text += f"\n\nCorrection officielle:\n{corr_text}"

                    chunks.append({
                        "text": chunk_text,
                        "source": f"exam_{meta['id']}",
                        "subject": subject,
                        "doc_type": "exam",
                        "type": "exam_question",
                        "exam_year": year,
                        "exam_session": session,
                        "question_index": q_index,
                        "part_name": part_name,
                        "topic": ex_topic,
                        "exercise_name": ex_name,
                    })
                    q_index += 1

        # Summary chunk
        if q_index > 0:
            themes_text = "\n".join(f"- {t}" for t in sorted(all_topics)) if all_topics else "Non spécifié"
            chunks.append({
                "text": f"""[Examen National {label}] RÉSUMÉ
Matière: {subject}
Année: {year}
Session: {session}
Nombre de questions: {q_index}
Thèmes abordés:
{themes_text}""",
                "source": f"exam_{meta['id']}",
                "subject": subject,
                "doc_type": "exam",
                "type": "exam_summary",
                "exam_year": year,
                "exam_session": session,
            })

        return chunks

    def _parse_legacy_exam_for_rag(self, raw: dict, meta: dict) -> list[dict]:
        """Parse legacy blocks format into RAG chunks."""
        blocks = raw.get("blocks", raw) if isinstance(raw, dict) else raw
        if isinstance(raw, dict) and "blocks" in raw:
            blocks = raw["blocks"]

        chunks = []
        subject = meta["subject"]
        year = meta["year"]
        session = meta["session"]
        label = f"{subject} {year} {session}"

        questions = []
        corrections = []
        current_context = ""

        for block in blocks:
            btype = block.get("type", "")
            origin = block.get("origin", "")

            if origin == "correction" or btype == "answer":
                corrections.append(block.get("content", ""))
                continue

            if btype == "text":
                current_context += " " + block.get("content", "")
            elif btype == "question":
                page_ctx = block.get("page_context", "")
                questions.append({
                    "content": block.get("content", ""),
                    "context": current_context.strip(),
                    "page_context": page_ctx,
                })
                current_context = ""

        for i, q in enumerate(questions):
            correction_text = corrections[i] if i < len(corrections) else ""
            chunk_text = f"[Examen National {label}] Question {i+1}:\n{q['content']}"
            if q["page_context"]:
                chunk_text += f"\nThème: {q['page_context']}"
            if correction_text:
                chunk_text += f"\n\nCorrection officielle:\n{correction_text}"

            chunks.append({
                "text": chunk_text,
                "source": f"exam_{meta['id']}",
                "subject": subject,
                "doc_type": "exam",
                "type": "exam_question",
                "exam_year": year,
                "exam_session": session,
                "question_index": i,
            })

        if questions:
            themes = list({q["page_context"] for q in questions if q["page_context"]})
            themes_text = "\n".join(f"- {t}" for t in themes) if themes else "Non spécifié"
            chunks.append({
                "text": f"""[Examen National {label}] RÉSUMÉ
Matière: {subject}
Année: {year}
Session: {session}
Nombre de questions: {len(questions)}
Thèmes abordés:
{themes_text}""",
                "source": f"exam_{meta['id']}",
                "subject": subject,
                "doc_type": "exam",
                "type": "exam_summary",
                "exam_year": year,
                "exam_session": session,
            })

        return chunks

    def index_all(self, force_reindex: bool = False):
        """
        Index everything: courses (SVT + Math + PC) + cadres de référence +
        national exams. Call this once at startup to have the full BAC content
        available. Course caches are pre-built by scripts/index_*_courses.py.

        FAISS is built ONCE at the end to avoid re-embedding 5x.
        """
        if RAG_DISABLED:
            return
        # Course content — folder name must match what _get_cache_path expects:
        #   SVT   → cours 2bac pc/SVT/  + svt_rag_cache.json
        #   Math  → cours 2bac pc/Math/ + math_rag_cache.json
        #   PC    → cours 2bac pc/PC/   + pc_rag_cache.json
        self.index_subject("SVT", force_reindex, build_index=False)
        self.index_subject("Math", force_reindex, build_index=False)
        self.index_subject("PC", force_reindex, build_index=False)
        self.index_cadres_de_reference(force_reindex, build_index=False)
        self.index_exams(force_reindex, build_index=False)
        print(f"[RAG] Total documents indexed: {len(self.documents)} chunks")

        # Build FAISS index once, after all documents are loaded
        if EMBEDDINGS_AVAILABLE and self.documents:
            self._build_faiss_index()
        self._initialized = True
    
    def _corpus_fingerprint(self) -> str:
        """Short hash of all document texts — used to validate FAISS disk cache."""
        h = hashlib.md5()
        for doc in self.documents:
            h.update((doc.get("text") or "").encode("utf-8", errors="ignore"))
            h.update(b"\x00")
        return h.hexdigest()

    def _build_faiss_index(self):
        """Build FAISS index, reusing an on-disk cache when the corpus is unchanged.

        Re-embedding 2800+ chunks takes ~5 min, so we serialize the FAISS index
        and a fingerprint to `data/rag_cache/faiss_index.bin` and skip rebuilds
        when nothing has changed.
        """
        self._load_embedding_model()

        index_path = self.cache_dir / "faiss_index.bin"
        fp_path = self.cache_dir / "faiss_fingerprint.txt"
        emb_path = self.cache_dir / "faiss_embeddings.npy"
        corpus_fp = self._corpus_fingerprint()

        # Try cache hit
        if index_path.exists() and fp_path.exists() and emb_path.exists():
            try:
                cached_fp = fp_path.read_text(encoding="utf-8").strip()
                if cached_fp == corpus_fp:
                    self.index = faiss.read_index(str(index_path))
                    embeddings = np.load(emb_path)
                    if self.index.ntotal == len(self.documents) == len(embeddings):
                        for i, doc in enumerate(self.documents):
                            doc["embedding"] = embeddings[i].tolist()
                        print(f"[RAG] FAISS loaded from cache: {self.index.ntotal} vectors")
                        return
                    else:
                        print(f"[RAG] FAISS cache size mismatch "
                              f"({self.index.ntotal} vs {len(self.documents)}) — rebuilding")
            except Exception as e:
                print(f"[RAG] FAISS cache load failed: {e} — rebuilding")

        print(f"[RAG] Building FAISS index for {len(self.documents)} chunks "
              f"(first time or corpus changed)...")
        texts = [doc['text'] for doc in self.documents]
        # batch_size=128 is ~3-4× faster than the default 32 on CPU.
        # normalize_embeddings=True makes the vectors unit-length so we can skip
        # the extra faiss.normalize_L2 pass below.
        embeddings = self.model.encode(
            texts,
            batch_size=128,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).astype('float32')

        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.index.add(embeddings)

        for i, doc in enumerate(self.documents):
            doc['embedding'] = embeddings[i].tolist()

        try:
            faiss.write_index(self.index, str(index_path))
            np.save(emb_path, embeddings)
            fp_path.write_text(corpus_fp, encoding="utf-8")
            print(f"[RAG] FAISS index built ({self.index.ntotal} vectors) + cached to disk")
        except Exception as e:
            print(f"[RAG] WARNING: failed to persist FAISS cache: {e}")
    
    def search(self, query: str, top_k: int = 5, subject: str = None) -> list[dict]:
        """
        Search for relevant content chunks.
        Uses semantic search if available, falls back to keyword search.
        If subject is specified, results from that subject are boosted.
        """
        if RAG_DISABLED:
            return []
        if not self._initialized:
            self.index_all()
        
        if not self.documents:
            return []
        
        if EMBEDDINGS_AVAILABLE and self.index is not None:
            return self._semantic_search(query, top_k)
        else:
            return self._keyword_search(query, top_k)
    
    def _semantic_search(self, query: str, top_k: int) -> list[dict]:
        """Semantic search using FAISS"""
        self._load_embedding_model()
        
        # Encode query
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc['score'] = float(distances[0][i])
                # Remove embedding from result to save memory
                doc.pop('embedding', None)
                results.append(doc)
        
        return results
    
    def _keyword_search(self, query: str, top_k: int) -> list[dict]:
        """Fallback keyword search"""
        query_terms = query.lower().split()
        
        scored_docs = []
        for doc in self.documents:
            text_lower = doc['text'].lower()
            score = sum(1 for term in query_terms if term in text_lower)
            if score > 0:
                result = doc.copy()
                result['score'] = score
                result.pop('embedding', None)
                scored_docs.append(result)
        
        # Sort by score descending
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        return scored_docs[:top_k]
    
    # ─────────────────────── citation helpers ───────────────────────

    _SRC_SUBJECT_PREFIX = {
        "mathématiques": "math",
        "mathematiques": "math",
        "maths": "math",
        "physique-chimie": "pc",
        "physique": "pc",
        "chimie": "pc",
        "svt": "svt",
    }

    @classmethod
    def _slugify_source(cls, s: str) -> str:
        """Short, URL-safe identifier from a source name (16 chars max)."""
        s = re.sub(r"\(.*?\)", "", s or "").strip()
        s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
        return s[:16] or "src"

    @classmethod
    def make_src_id(cls, doc: dict) -> str:
        """Stable, short citation ID for a chunk. Format: <subj>:<source>:p<page>."""
        subj_raw = (doc.get("subject") or "").lower().strip()
        subj = cls._SRC_SUBJECT_PREFIX.get(subj_raw)
        if subj is None:
            for key, prefix in cls._SRC_SUBJECT_PREFIX.items():
                if key in subj_raw:
                    subj = prefix
                    break
        subj = subj or "ref"
        source = cls._slugify_source(doc.get("source") or doc.get("unit") or "src")
        page = doc.get("page", "?")
        doc_type = doc.get("doc_type") or doc.get("type") or ""
        kind = ""
        if doc_type == "cadre_reference":
            kind = "cadre-"
        elif doc_type == "exam":
            kind = "exam-"
        return f"{subj}:{kind}{source}:p{page}"

    CITATION_RULES = (
        "RÈGLES DE CITATION (OBLIGATOIRES):\n"
        "- Chaque extrait ci-dessous commence par un identifiant entre crochets "
        "au format: `[src:` suivi de la référence, puis `]`.\n"
        "- Après CHAQUE fait, formule, définition ou exemple que tu utilises, "
        "recopie l'identifiant de la source entre crochets (avec le préfixe src:).\n"
        "- Si plusieurs sources supportent le même fait, cite-les toutes à la suite.\n"
        "- Si l'information demandée n'est PAS dans le contexte, réponds exactement : "
        "« Cette information ne fait pas partie du programme officiel fourni. » "
        "Ne jamais inventer un fait sans source.\n"
        "- N'invente JAMAIS d'identifiant : utilise uniquement ceux qui apparaissent "
        "littéralement dans le contexte ci-dessous."
    )

    @staticmethod
    def parse_citations(answer: str) -> list[str]:
        """Extract unique [src:...] identifiers cited in an LLM answer.

        Used by the frontend / verifier to build a clickable reference list.
        """
        if not answer:
            return []
        ids = re.findall(r"\[src:([^\]\s]+)\]", answer)
        seen: list[str] = []
        for i in ids:
            if i not in seen:
                seen.append(i)
        return seen

    def get_context_for_query(self, query: str, subject: str = None, max_tokens: int = 2000) -> str:
        """
        Get formatted context for LLM prompt.
        Returns relevant course content as a formatted string with [src:<id>] tags
        prefixing every chunk so the LLM can cite sources in its response.
        """
        if RAG_DISABLED:
            return ""
        results = self.search(query, top_k=8, subject=subject)
        
        # Check if query is about exam weights/points/program structure
        query_lower = query.lower()
        exam_keywords = ['point', 'poids', 'pourcentage', '%', 'examen', 'coefficient', 
                         'répartition', 'domaine', 'programme', 'structure']
        is_exam_query = any(kw in query_lower for kw in exam_keywords)
        
        # If exam-related query, prioritize exam_weights and program_overview chunks
        if is_exam_query:
            priority_chunks = []
            for doc in self.documents:
                doc_type = doc.get('type', '')
                if doc_type in ['exam_weights', 'program_overview', 'exam_structure', 'exam_skills']:
                    doc_subject = doc.get('subject', '').lower()
                    # Include if: no subject filter, or subject matches query terms
                    include = True
                    if subject:
                        include = subject.lower() in doc_subject or doc_subject in subject.lower()
                    else:
                        # Check if query mentions a specific subject
                        if 'physique' in query_lower and 'chimie' not in query_lower:
                            include = 'physique' in doc_subject
                        elif 'chimie' in query_lower and 'physique' not in query_lower:
                            include = 'chimie' in doc_subject
                        elif 'svt' in query_lower:
                            include = 'svt' in doc_subject
                        elif 'math' in query_lower:
                            include = 'math' in doc_subject
                        # For general exam queries, include all exam_weights chunks
                    
                    if include:
                        priority_doc = doc.copy()
                        # Higher priority for exam_weights type
                        priority_doc['score'] = 1.5 if doc_type == 'exam_weights' else 1.0
                        priority_doc.pop('embedding', None)
                        priority_chunks.append(priority_doc)
            
            # Sort priority chunks by score (exam_weights first)
            priority_chunks.sort(key=lambda x: x['score'], reverse=True)
            
            # Add priority chunks at the beginning, avoiding duplicates
            existing_texts = {r['text'] for r in results}
            for pc in priority_chunks:
                if pc['text'] not in existing_texts:
                    results.insert(0, pc)
                    existing_texts.add(pc['text'])
        
        if not results:
            return ""
        
        context_parts = []
        total_chars = 0
        max_chars = max_tokens * 4  # Approximate chars per token
        
        for doc in results:
            text = doc['text']
            source = doc.get('source', 'Unknown')
            page = doc.get('page', '?')
            doc_type = doc.get('doc_type', 'cours')
            subj = doc.get('subject', '')
            if doc_type == 'cadre_reference':
                label = f"{subj} - Cadre de Référence"
            elif doc_type == 'exam':
                label = f"{subj} - Examen National"
            else:
                label = f"{subj} - Cours"

            src_id = self.make_src_id(doc)
            # Stable citation ID on its own line so the model learns the syntax
            # from the context itself. Human-readable label kept for debugging.
            chunk = f"[src:{src_id}] ({label} | {source}, page {page})\n{text}\n"
            
            if total_chars + len(chunk) > max_chars:
                break
            
            context_parts.append(chunk)
            total_chars += len(chunk)
        
        return "\n---\n".join(context_parts)

    def build_grounded_context(
        self,
        query: str,
        subject: str = None,
        max_tokens: int = 2000,
        header: str = "CONTENU OFFICIEL DU BAC MAROCAIN",
    ) -> str:
        """
        One-stop helper for LLM prompts: returns a ready-to-inject block that
        includes the citation rules followed by the retrieved chunks with
        [src:<id>] identifiers.

        Returns an empty string if no context is available, so callers can
        safely concatenate it to their prompt without extra checks.
        """
        context = self.get_context_for_query(query, subject=subject, max_tokens=max_tokens)
        if not context:
            return ""
        return (
            f"{self.CITATION_RULES}\n\n"
            f"[{header}] — n'invente rien en dehors de ces extraits.\n\n"
            f"{context}"
        )

    # ─────────────────────── exam bank helpers (for diagnostic + exam_blanc) ───────────────────────

    @staticmethod
    def _subject_matches(doc_subject: str, wanted: str) -> bool:
        """Loose match between doc subject and requested subject.

        Handles: "Physique" in exams ↔ "Physique-Chimie" in cadres,
        accented vs unaccented ("Mathématiques" vs "Mathematiques"), etc.
        """
        a = (doc_subject or "").lower().replace("é", "e").replace("è", "e").strip()
        b = (wanted or "").lower().replace("é", "e").replace("è", "e").strip()
        if not a or not b:
            return False
        if a == b or a in b or b in a:
            return True
        # Physique / Chimie ⊂ Physique-Chimie
        if b in ("physique", "chimie") and "physique-chimie" in a:
            return True
        if a in ("physique", "chimie") and "physique-chimie" in b:
            return True
        return False

    # Domain keywords used to infer Physique vs Chimie when the exercise
    # name doesn't carry an explicit '— Physique :' / '— Chimie :' prefix.
    _PHYS_DOMAIN_KWS = (
        "mécanique", "mecanique", "newton", "chute", "pendule", "satellite",
        "oscillateur mécanique", "oscillateur mecanique", "mouvement",
        "onde", "ondes", "lumineuse", "lumineuses", "diffraction",
        "interférence", "interference", "propagation",
        "nucléaire", "nucleaire", "désintégration", "desintegration",
        "radioactivité", "radioactivite", "transformations nucléaires",
        "transformations nucleaires",
        "électricité", "electricite", "rc", "rl", "rlc",
        "condensateur", "bobine", "modulation", "démodulation", "demodulation",
    )
    _CHIM_DOMAIN_KWS = (
        "chimie", "dosage", "titrage", "acide", "base", "pka", "ph",
        "pile", "électrolyse", "electrolyse", "estérification", "esterification",
        "hydrolyse", "ester", "équilibre", "equilibre", "avancement",
        "suivi temporel", "cinétique", "cinetique",
    )

    @classmethod
    def _exam_doc_fits_single_subject(cls, doc: dict, wanted: str) -> bool:
        """Fine-grained filter for Physique-Chimie combined exams.

        The BAC BIOF exam stores Physique and Chimie questions side-by-side
        under the same 'Physique-Chimie' label. We infer the real subject of
        each question from:
          (1) explicit markers in the exercise name ('— Chimie :' / '— Physique :')
          (2) domain keywords (e.g. 'Transformations nucléaires' → Physique,
              'Dosage d'une solution acide' → Chimie)

        Returns True if the doc is OK to keep for the caller's subject.
        """
        w = (wanted or "").lower().replace("é", "e").strip()
        if w not in ("physique", "chimie"):
            return True  # Math / SVT don't have this ambiguity

        ex_name = (doc.get("exercise_name") or "").lower()
        topic = (doc.get("topic") or "").lower()
        if not ex_name and not topic:
            return True  # No signal — be permissive

        haystack = f"{ex_name} {topic}"

        # 1. Explicit prefix wins over keyword inference.
        has_chimie_marker = ("— chimie" in ex_name) or (": chimie" in ex_name) or ex_name.startswith("chimie ")
        has_phys_marker = ("— physique" in ex_name) or (": physique" in ex_name) or ex_name.startswith("physique ")

        if has_chimie_marker and not has_phys_marker:
            return w == "chimie"
        if has_phys_marker and not has_chimie_marker:
            return w == "physique"

        # 2. No explicit marker — count domain keyword hits.
        phys_hits = sum(1 for kw in cls._PHYS_DOMAIN_KWS if kw in haystack)
        chim_hits = sum(1 for kw in cls._CHIM_DOMAIN_KWS if kw in haystack)

        if phys_hits == 0 and chim_hits == 0:
            return True  # Unclassifiable — keep (don't starve the LLM)
        if w == "physique":
            return phys_hits >= chim_hits  # Tie → keep (ambiguous)
        # w == "chimie"
        return chim_hits >= phys_hits

    def get_exam_inspiration(
        self,
        subject: str,
        n: int = 3,
        years: Optional[list[str]] = None,
        exclude_topics: Optional[list[str]] = None,
        exclude_question_texts: Optional[list[str]] = None,
    ) -> list[dict]:
        """Return up to `n` real BAC exam questions to inspire diagnostic generation.

        Strategy:
          1. Filter doc_type=='exam' AND type=='exam_question' for the subject.
          2. Drop questions whose topic matches exclude_topics (case-insensitive).
          3. Drop questions whose text fuzzy-matches exclude_question_texts.
          4. Prefer recent years (sort desc), then diversify topics (round-robin).

        Each returned item contains: {src_id, text, topic, year, session, question_index}.
        """
        if RAG_DISABLED:
            return []
        if not self._initialized:
            self.index_all()

        ex_topics = [t.lower().strip() for t in (exclude_topics or []) if t]
        ex_texts = [(t or "")[:120].lower() for t in (exclude_question_texts or []) if t]

        candidates: list[dict] = []
        for doc in self.documents:
            if doc.get("doc_type") != "exam":
                continue
            if doc.get("type") != "exam_question":
                continue
            if not self._subject_matches(doc.get("subject", ""), subject):
                continue
            # Strict single-subject filter: when the caller asks for
            # Physique OR Chimie (not the combined label), drop questions
            # whose exercise_name marks the OTHER subject. Prevents
            # Chimie leaks in Physique diagnostics and vice-versa.
            if not self._exam_doc_fits_single_subject(doc, subject):
                continue
            if years and str(doc.get("exam_year", "")) not in [str(y) for y in years]:
                continue
            topic = (doc.get("topic") or "").lower().strip()
            if topic and any(t in topic or topic in t for t in ex_topics):
                continue
            txt_head = (doc.get("text") or "")[:120].lower()
            if ex_texts and any(ex and ex in txt_head for ex in ex_texts):
                continue
            candidates.append(doc)

        # Sort by year desc (recent first), then by question_index asc
        def _sort_key(d: dict):
            yr = d.get("exam_year") or "0"
            try:
                yr_num = int(str(yr))
            except ValueError:
                yr_num = 0
            return (-yr_num, d.get("question_index", 0))

        candidates.sort(key=_sort_key)

        # Round-robin by topic to maximise diversity in the top N
        by_topic: dict[str, list[dict]] = {}
        for d in candidates:
            key = (d.get("topic") or d.get("exercise_name") or "general").lower()
            by_topic.setdefault(key, []).append(d)

        picked: list[dict] = []
        topic_queues = [q for q in by_topic.values() if q]
        while len(picked) < n and topic_queues:
            remaining: list[list[dict]] = []
            for q in topic_queues:
                if len(picked) >= n:
                    break
                picked.append(q.pop(0))
                if q:
                    remaining.append(q)
            topic_queues = remaining

        return [
            {
                "src_id": self.make_src_id(d),
                "text": d.get("text", ""),
                "topic": d.get("topic", ""),
                "exercise_name": d.get("exercise_name", ""),
                "year": d.get("exam_year", ""),
                "session": d.get("exam_session", ""),
                "question_index": d.get("question_index", 0),
                "source": d.get("source", ""),
            }
            for d in picked[:n]
        ]

    def get_recent_exams_for_subject(self, subject: str, n: int = 4) -> list[dict]:
        """Return up to `n` most recent (year, session) exam identifiers for a subject.

        Used to attach a real exam to each `examen_blanc` session in the study plan.
        Returns items like:
          {id: 'physique_2024_normale', year: '2024', session: 'normale', source: 'exam_physique_2024_normale'}
        """
        if RAG_DISABLED:
            return []
        if not self._initialized:
            self.index_all()

        seen: dict[tuple, dict] = {}
        for doc in self.documents:
            if doc.get("doc_type") != "exam":
                continue
            if not self._subject_matches(doc.get("subject", ""), subject):
                continue
            year = str(doc.get("exam_year", ""))
            session = str(doc.get("exam_session", "")) or "normale"
            key = (year, session)
            if key in seen or not year:
                continue
            source = doc.get("source", "")
            # Build a stable exam id matching backend/data/exams/<subject>/<year>-<session>/
            seen[key] = {
                "id": source.replace("exam_", "") if source.startswith("exam_") else f"{subject.lower()}_{year}_{session}",
                "year": year,
                "session": session,
                "source": source,
            }

        def _sort_key(item: dict):
            try:
                yr = int(item["year"])
            except ValueError:
                yr = 0
            # normale first within same year
            return (-yr, 0 if item["session"] == "normale" else 1)

        return sorted(seen.values(), key=_sort_key)[:n]

    def get_citation_sources(self, ids: list[str]) -> list[dict]:
        """Resolve [src:<id>] identifiers back to their source metadata.

        Used to build a clickable references panel on the frontend.
        Returns a list of {id, subject, source, page, type, text_preview}.
        """
        if not ids:
            return []
        wanted = set(ids)
        resolved: list[dict] = []
        seen_ids: set[str] = set()
        for doc in self.documents:
            sid = self.make_src_id(doc)
            if sid in wanted and sid not in seen_ids:
                seen_ids.add(sid)
                preview = (doc.get("text") or "")[:220]
                resolved.append({
                    "id": sid,
                    "subject": doc.get("subject", ""),
                    "source": doc.get("source", ""),
                    "page": doc.get("page", "?"),
                    "type": doc.get("doc_type") or doc.get("type") or "cours",
                    "preview": preview,
                })
        return resolved
    
    def get_exam_weights_data(self) -> dict:
        """
        Return structured exam weight data for all subjects from cadres de référence.
        Used by study_plan_service and diagnostic_service.
        Returns:
            {
                "Physique": {"total_weight": "67%", "domains": {"Ondes": "11%", ...}},
                "Chimie": {"total_weight": "33%", "domains": {...}},
                "SVT": {"total_weight": "100%", "domains": {...}},
                "Mathématiques": {"total_weight": "100%", "domains": {...}},
            }
        """
        if RAG_DISABLED:
            return {}
        if not self._initialized:
            self.index_all()
        
        weights = {}
        for doc in self.documents:
            if doc.get('doc_type') != 'cadre_reference':
                continue
            doc_type = doc.get('type', '')
            subject = doc.get('subject', '')
            text = doc.get('text', '')
            
            if doc_type == 'exam_weights':
                # Parse the structured text to extract weights
                if 'Physique-Chimie' in subject or ('PHYSIQUE' in text and 'CHIMIE' in text):
                    # Combined PC chunk — parse both
                    for line in text.split('\n'):
                        line = line.strip()
                        if line.startswith('- PHYSIQUE:'):
                            weights.setdefault('Physique', {})['total_weight'] = line.split(':')[-1].strip()
                        elif line.startswith('- CHIMIE:'):
                            weights.setdefault('Chimie', {})['total_weight'] = line.split(':')[-1].strip()
                        elif line.startswith('- Ondes:'):
                            weights.setdefault('Physique', {}).setdefault('domains', {})['Ondes'] = line.split(':')[-1].strip()
                        elif line.startswith('- Transformations nucléaires:'):
                            weights.setdefault('Physique', {}).setdefault('domains', {})['Transformations nucléaires'] = line.split(':')[-1].strip()
                        elif 'lectricité:' in line:
                            weights.setdefault('Physique', {}).setdefault('domains', {})['Électricité'] = line.split(':')[-1].strip()
                        elif line.startswith('- Mécanique:'):
                            weights.setdefault('Physique', {}).setdefault('domains', {})['Mécanique'] = line.split(':')[-1].strip()
                        elif line.startswith('- Transformations rapides'):
                            weights.setdefault('Chimie', {}).setdefault('domains', {})['Transformations rapides et lentes'] = line.split(':')[-1].strip()
                        elif line.startswith('- Transformations non totales'):
                            weights.setdefault('Chimie', {}).setdefault('domains', {})['Transformations non totales'] = line.split(':')[-1].strip()
                        elif "Sens d'évolution" in line:
                            weights.setdefault('Chimie', {}).setdefault('domains', {})["Sens d'évolution"] = line.split(':')[-1].strip()
                        elif 'Méthode de contrôle' in line:
                            weights.setdefault('Chimie', {}).setdefault('domains', {})['Méthode de contrôle'] = line.split(':')[-1].strip()
                elif 'Mathématiques' in subject:
                    weights.setdefault('Mathématiques', {'total_weight': '100%', 'domains': {}})
                    for line in text.split('\n'):
                        line = line.strip()
                        if line.startswith('- ') and '(' in line and '%' in line:
                            # e.g. "- Analyse: ... (55%)"
                            pct = line[line.rfind('(')+1:line.rfind(')')]
                            domain = line[2:line.find(':')]
                            weights['Mathématiques']['domains'][domain] = pct
            
            elif doc_type == 'program_overview' and 'SVT' in subject:
                weights.setdefault('SVT', {'total_weight': '100%', 'domains': {}})
                for line in text.split('\n'):
                    line = line.strip()
                    if line.startswith('- Domaine'):
                        # e.g. "- Domaine 1 : Consommation de la matière organique et flux d'énergie"
                        dom_name = line[2:]
                        weights['SVT']['domains'][dom_name] = '25%'
        
        return weights

    def get_subject_program_context(self, subject_name: str) -> str:
        """
        Get full program context for a specific subject (program overview + weights + skills).
        Used to inject into diagnostic and coaching prompts.
        """
        if RAG_DISABLED:
            return ""
        if not self._initialized:
            self.index_all()
        
        parts = []
        subject_lower = subject_name.lower()
        
        for doc in self.documents:
            if doc.get('doc_type') != 'cadre_reference':
                continue
            doc_subject = doc.get('subject', '').lower()
            doc_type = doc.get('type', '')
            
            # Match subject
            if subject_lower in doc_subject or doc_subject in subject_lower:
                if doc_type in ['program_overview', 'exam_weights', 'exam_skills', 'exam_structure']:
                    parts.append(doc['text'])
            # Also include combined Physique-Chimie chunks for Physique or Chimie
            elif 'physique-chimie' in doc_subject and (subject_lower in ['physique', 'chimie']):
                if doc_type in ['exam_weights', 'exam_skills']:
                    parts.append(doc['text'])
        
        return "\n\n".join(parts) if parts else ""

    def get_all_subjects_program_context(self) -> str:
        """
        Get program context for ALL subjects. Used for diagnostic across all subjects.
        """
        if RAG_DISABLED:
            return ""
        if not self._initialized:
            self.index_all()
        
        parts = []
        seen = set()
        for doc in self.documents:
            if doc.get('doc_type') != 'cadre_reference':
                continue
            doc_type = doc.get('type', '')
            if doc_type in ['program_overview', 'exam_weights', 'exam_skills', 'exam_structure']:
                text = doc['text']
                if text not in seen:
                    parts.append(text)
                    seen.add(text)
        
        return "\n\n---\n\n".join(parts) if parts else ""

    def build_rag_system_prompt(
        self,
        query: str,
        subject: str = "SVT",
        student_name: str = "l'élève",
        language: str = "français"
    ) -> str:
        """
        Build a complete system prompt with RAG context.
        Ensures AI only uses official curriculum content AND cites each fact
        with [src:<id>] tags from the retrieved chunks.
        """
        # Grounded context already includes CITATION_RULES + [src:...] tagged chunks
        grounded = self.build_grounded_context(query, subject=subject)
        if not grounded:
            grounded = "Aucun contenu trouvé pour cette question dans le programme officiel."

        prompt = f"""Tu es un professeur marocain expert du programme officiel du ministère de l'éducation nationale.
Tu enseignes la matière {subject} pour le BAC 2ème année Sciences Physiques BIOF.
Tu parles en {language}.

{grounded}

RÈGLES PÉDAGOGIQUES (EN PLUS DES RÈGLES DE CITATION CI-DESSUS):
1. Utilise UNIQUEMENT le contenu officiel fourni ; n'ajoute aucune information externe.
2. Emploie le vocabulaire scientifique officiel des cours marocains.
3. Adapte ton explication au niveau de l'élève : simple, pédagogique, étape par étape.
4. Donne un exemple concret quand c'est pertinent.
5. Termine par une question de vérification de la compréhension.

FORMAT DE RÉPONSE (avec citations obligatoires):
📚 **Explication:** [Explication avec [src:<id>] après chaque fait]
📝 **Exemple:** [Exemple simple avec citation de la source]
❓ **Question de vérification:** [Question pour vérifier la compréhension]

OBJECTIF:
Aider {student_name} à comprendre le cours officiel et réussir ses examens, en restant 100% fidèle aux sources citées.

Réponds maintenant à la question de l'élève en respectant strictement ces règles."""

        return prompt


# Singleton instance
_rag_service: Optional[RAGService] = None

def get_rag_service() -> RAGService:
    """Get or create RAG service singleton"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service


# CLI for testing/indexing
if __name__ == "__main__":
    import sys
    
    service = RAGService()
    
    if len(sys.argv) > 1 and sys.argv[1] == "index":
        # Index everything
        service.index_all(force_reindex=True)
        print("Indexing complete!")
    else:
        # Test search
        service.index_all()
        query = "glycolyse ATP"
        results = service.search(query, top_k=3)
        print(f"\nSearch results for '{query}':")
        for r in results:
            subj = r.get('subject', '?')
            print(f"  - [{subj} | {r['source']} p.{r['page']}] {r['text'][:100]}...")
        
        # Test cross-subject search
        query2 = "dérivée fonction limite"
        results2 = service.search(query2, top_k=3)
        print(f"\nSearch results for '{query2}':")
        for r in results2:
            subj = r.get('subject', '?')
            print(f"  - [{subj} | {r['source']} p.{r['page']}] {r['text'][:100]}...")
