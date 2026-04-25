"""
Exam Extraction API — OCR text extraction, Vision-based document zone
detection, document description, and publish-to-students for admin exam builder.

Pipeline:
  1. Frontend renders PDF pages → Canvas → JPEG base64
  2. /ocr-page       → Mistral OCR extracts raw text per page
  3. /detect-zones   → Mistral Vision finds document bounding-boxes
  4. /describe-doc   → Mistral Vision describes a cropped document image
  5. /publish        → Save extraction data (text + docs) to disk
"""
import logging
import re
import json
import base64
import httpx
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/exam-extract", tags=["exam-extraction"])

settings = get_settings()

MISTRAL_CHAT_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_OCR_URL = "https://api.mistral.ai/v1/ocr"
MISTRAL_OCR_MODEL = "mistral-ocr-latest"
MISTRAL_VISION_MODEL = "pixtral-large-latest"


# ── Request / Response models ────────────────────────────────

class OcrPageRequest(BaseModel):
    image_base64: str          # JPEG/PNG base64 of a rendered page
    page_number: int
    subject: Optional[str] = ""  # e.g. "svt", "physique"


class OcrPageResponse(BaseModel):
    page_number: int
    text: str
    markdown: str
    success: bool
    error: Optional[str] = None


class DescribeDocRequest(BaseModel):
    image_base64: str          # Cropped document image (PNG base64)
    doc_name: str              # e.g. "Document 1"
    subject: Optional[str] = ""


class DescribeDocResponse(BaseModel):
    doc_name: str
    description: str
    success: bool
    error: Optional[str] = None


class DetectZonesRequest(BaseModel):
    image_base64: str  # JPEG base64 of the full page rendered by PDF.js
    page_number: int
    hint: Optional[str] = ""  # Optional hint like "Document 1, Document 2"


class DetectZonesResponse(BaseModel):
    zones: list[dict]  # [{name, type, description, box_2d: [ymin, xmin, ymax, xmax]}]
    raw_response: Optional[str] = None


@router.post("/detect-zones", response_model=DetectZonesResponse)
async def detect_zones(req: DetectZonesRequest):
    """Send a page image to Mistral Vision and get back box_2d coordinates for each document zone."""
    
    if not settings.mistral_api_key:
        raise HTTPException(status_code=500, detail="Mistral API key not configured")
    
    hint_text = f"\nIndice: cette page contient probablement: {req.hint}" if req.hint else ""
    
    prompt = f"""Tu es un expert en analyse de pages d'examens scientifiques marocains.

Cette image est la page {req.page_number} d'un examen. Elle peut contenir des documents visuels (graphiques, courbes, schémas, tableaux, figures) qui sont entourés d'un CADRE RECTANGULAIRE et nommés "Document 1", "Document 2", etc.
{hint_text}

Ta tâche: identifie CHAQUE zone visuelle (document, figure, schéma, tableau, graphique) entourée d'un cadre rectangulaire.

Pour CHAQUE zone trouvée, retourne:
- "name": le nom exact tel qu'il apparaît ("Document 1", "Document 2", "Figure a", etc.)
- "type": "graphique" | "schema" | "tableau" | "courbe" | "figure"
- "description": UNE phrase décrivant le contenu
- "box_2d": [ymin, xmin, ymax, xmax] — coordonnées normalisées entre 0 et 1000, où (0,0) est le coin supérieur gauche et (1000,1000) est le coin inférieur droit

RÈGLES CRITIQUES POUR box_2d:
1. Les coordonnées doivent correspondre au CADRE RECTANGULAIRE noir qui entoure le document
2. ymin = bord SUPÉRIEUR du cadre, ymax = bord INFÉRIEUR du cadre
3. xmin = bord GAUCHE du cadre, xmax = bord DROIT du cadre
4. Inclure le titre "Document N" au-dessus du cadre dans la zone
5. Si un document contient plusieurs sous-figures (Figure a, b, c...), englober TOUT dans une seule zone

Réponds UNIQUEMENT avec du JSON valide:
{{"zones": [
  {{"name": "Document 1", "type": "graphique", "description": "...", "box_2d": [150, 50, 550, 950]}}
]}}

Si aucune zone visuelle n'est trouvée: {{"zones": []}}"""

    headers = {
        "Authorization": f"Bearer {settings.mistral_api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": MISTRAL_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{req.image_base64}"},
                    },
                ],
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.1,
    }
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(MISTRAL_CHAT_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        
        vision_text = ""
        choices = data.get("choices", [])
        if choices:
            vision_text = choices[0].get("message", {}).get("content", "")
        
        logger.info(f"Page {req.page_number}: Mistral Vision response ({len(vision_text)} chars)")
        
        if not vision_text:
            return DetectZonesResponse(zones=[], raw_response="")
        
        # Parse JSON from response
        json_str = vision_text.strip()
        if json_str.startswith("```"):
            json_str = re.sub(r'^```(?:json)?\s*', '', json_str)
            json_str = re.sub(r'\s*```$', '', json_str)
        
        if not json_str.startswith('{'):
            json_match = re.search(r'(\{[\s\S]*\})', json_str)
            if json_match:
                json_str = json_match.group(1)
        
        try:
            parsed = json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Page {req.page_number}: JSON parse error: {e}\nRaw: {json_str[:500]}")
            return DetectZonesResponse(zones=[], raw_response=vision_text)
        
        zones = parsed.get("zones", [])
        
        # Validate box_2d values
        valid_zones = []
        for z in zones:
            box = z.get("box_2d", [])
            if not box or len(box) != 4:
                continue
            ymin, xmin, ymax, xmax = box
            if ymin >= ymax or xmin >= xmax:
                continue
            # Clamp to 0-1000
            z["box_2d"] = [
                max(0, min(1000, ymin)),
                max(0, min(1000, xmin)),
                max(0, min(1000, ymax)),
                max(0, min(1000, xmax)),
            ]
            valid_zones.append(z)
        
        logger.info(f"Page {req.page_number}: Found {len(valid_zones)} valid zones")
        return DetectZonesResponse(zones=valid_zones, raw_response=vision_text)
        
    except httpx.HTTPStatusError as e:
        logger.error(f"Mistral Vision API error: {e.response.status_code} {e.response.text[:200]}")
        raise HTTPException(status_code=502, detail=f"Mistral Vision API error: {e.response.status_code}")
    except Exception as e:
        logger.error(f"detect_zones failed: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── OCR Page Endpoint ────────────────────────────────────────

@router.post("/ocr-page", response_model=OcrPageResponse)
async def ocr_page(req: OcrPageRequest):
    """Extract text from a rendered PDF page image using Mistral OCR."""

    if not settings.mistral_api_key:
        raise HTTPException(status_code=500, detail="Mistral API key not configured")

    headers = {
        "Authorization": f"Bearer {settings.mistral_api_key}",
        "Content-Type": "application/json",
    }

    # Detect mime type from base64 header or default to png
    mime_type = "image/png"
    img_data = req.image_base64
    if img_data.startswith("data:"):
        header, img_data = img_data.split(",", 1)
        if ";" in header:
            mime_type = header.split(":")[1].split(";")[0]

    payload = {
        "model": MISTRAL_OCR_MODEL,
        "document": {
            "type": "image_url",
            "image_url": f"data:{mime_type};base64,{img_data}",
        },
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(MISTRAL_OCR_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        pages = data.get("pages", [])
        if not pages:
            return OcrPageResponse(
                page_number=req.page_number, text="", markdown="",
                success=False, error="Aucun texte détecté."
            )

        markdown_parts = []
        text_parts = []
        for page in pages:
            md = page.get("markdown", "") if isinstance(page, dict) else ""
            if md:
                markdown_parts.append(md)
                plain = md.replace("**", "").replace("*", "").replace("`", "")
                text_parts.append(plain)

        raw_text = "\n\n".join(text_parts)
        raw_md = "\n\n".join(markdown_parts)

        logger.info(f"OCR page {req.page_number}: extracted {len(raw_text)} chars")
        return OcrPageResponse(
            page_number=req.page_number,
            text=raw_text,
            markdown=raw_md,
            success=bool(raw_text),
            error=None if raw_text else "Aucun texte détecté.",
        )

    except httpx.HTTPStatusError as e:
        logger.error(f"Mistral OCR API error: {e.response.status_code} {e.response.text[:200]}")
        raise HTTPException(status_code=502, detail=f"Mistral OCR API error: {e.response.status_code}")
    except Exception as e:
        logger.error(f"ocr_page failed: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Describe Document Endpoint ───────────────────────────────

@router.post("/describe-doc", response_model=DescribeDocResponse)
async def describe_doc(req: DescribeDocRequest):
    """Describe a cropped document image using Mistral Vision."""

    if not settings.mistral_api_key:
        raise HTTPException(status_code=500, detail="Mistral API key not configured")

    mime_type = "image/png"
    img_data = req.image_base64
    if img_data.startswith("data:"):
        header, img_data = img_data.split(",", 1)
        if ";" in header:
            mime_type = header.split(":")[1].split(";")[0]

    subject_hint = f" ({req.subject})" if req.subject else ""

    prompt = f"""Tu es un expert en analyse de documents d'examens scientifiques marocains{subject_hint}.

Cette image est un document extrait d'un examen national : « {req.doc_name} ».

Décris PRÉCISÉMENT et BRIÈVEMENT le contenu de ce document en français :
- Type : graphique, courbe, tableau, schéma, figure, diagramme, carte, etc.
- Contenu : axes, légendes, valeurs clés, structures, étapes, relations, etc.
- En 2 à 4 phrases maximum.

Réponds directement avec la description, sans préfixe ni titre."""

    headers = {
        "Authorization": f"Bearer {settings.mistral_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MISTRAL_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{img_data}"},
                    },
                ],
            }
        ],
        "max_tokens": 500,
        "temperature": 0.15,
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(MISTRAL_CHAT_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        description = ""
        choices = data.get("choices", [])
        if choices:
            description = choices[0].get("message", {}).get("content", "").strip()

        logger.info(f"Describe '{req.doc_name}': {len(description)} chars")
        return DescribeDocResponse(
            doc_name=req.doc_name,
            description=description,
            success=bool(description),
            error=None if description else "Aucune description générée.",
        )

    except httpx.HTTPStatusError as e:
        logger.error(f"Mistral Vision API error: {e.response.status_code} {e.response.text[:200]}")
        raise HTTPException(status_code=502, detail=f"Mistral Vision API error: {e.response.status_code}")
    except Exception as e:
        logger.error(f"describe_doc failed: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Publish Exam Endpoint ────────────────────────────────────

EXAMS_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "data" / "exams"


class PublishExamRequest(BaseModel):
    exam_id: str               # e.g. "svt_2022_normale"
    subject: str               # e.g. "svt"
    year: int
    session: str               # "Normale" | "Rattrapage"
    title: str
    subject_full: str
    duration_minutes: int = 180
    coefficient: int = 5
    total_points: int = 20
    note: str = ""
    sujet_text: str            # Full OCR text of subject
    correction_text: str       # Full OCR text of correction
    documents: list[dict]      # [{name, type, description, dataUrl}]
    structured_exam: Optional[dict] = None  # Structured exam JSON from LLM


@router.post("/publish")
async def publish_exam(req: PublishExamRequest):
    """Save extracted exam data to disk and register in index.json."""

    # Build folder path:  data/exams/<subject>/<year>-<session_slug>/
    session_slug = req.session.lower().replace(" ", "-")
    folder_name = f"{req.year}-{session_slug}"
    exam_dir = EXAMS_DIR / req.subject.lower() / folder_name
    assets_dir = exam_dir / "assets"

    try:
        exam_dir.mkdir(parents=True, exist_ok=True)
        assets_dir.mkdir(parents=True, exist_ok=True)

        # Save document images
        saved_docs = []
        for i, doc in enumerate(req.documents, 1):
            img_filename = f"document_{i}.png"
            data_url = doc.get("dataUrl", "")
            if data_url:
                # Strip data URL prefix
                raw = data_url
                if "," in raw:
                    raw = raw.split(",", 1)[1]
                img_bytes = base64.b64decode(raw)
                (assets_dir / img_filename).write_bytes(img_bytes)
            saved_docs.append({
                "id": f"Doc {i}",
                "name": doc.get("name", f"Document {i}"),
                "type": doc.get("type", "figure"),
                "description": doc.get("description", ""),
                "src": f"assets/{img_filename}",
            })

        # Save structured exam.json if provided
        if req.structured_exam:
            with open(exam_dir / "exam.json", "w", encoding="utf-8") as f:
                json.dump(req.structured_exam, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved structured exam.json to {exam_dir}")

        # Save extraction package
        package = {
            "exam_id": req.exam_id,
            "subject": req.subject,
            "year": req.year,
            "session": req.session,
            "title": req.title,
            "sujet_text": req.sujet_text,
            "correction_text": req.correction_text,
            "documents": saved_docs,
        }
        with open(exam_dir / "extraction.json", "w", encoding="utf-8") as f:
            json.dump(package, f, ensure_ascii=False, indent=2)

        # Update index.json
        index_path = EXAMS_DIR / "index.json"
        index_data = []
        if index_path.exists():
            with open(index_path, "r", encoding="utf-8-sig") as f:
                index_data = json.load(f)

        # Remove old entry with same id
        index_data = [e for e in index_data if e.get("id") != req.exam_id]

        index_data.append({
            "id": req.exam_id,
            "subject": req.subject.upper() if len(req.subject) <= 3 else req.subject.capitalize(),
            "year": req.year,
            "session": req.session,
            "path": f"{req.subject.lower()}/{folder_name}",
            "title": req.title,
            "subject_full": req.subject_full,
            "duration_minutes": req.duration_minutes,
            "coefficient": req.coefficient,
            "total_points": req.total_points,
            "note": req.note,
        })

        # Sort by year desc then subject
        index_data.sort(key=lambda e: (-e.get("year", 0), e.get("subject", "")))

        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)

        has_exam_json = req.structured_exam is not None
        logger.info(f"Published exam '{req.exam_id}' to {exam_dir} (exam.json={'yes' if has_exam_json else 'no'}, docs={len(saved_docs)})")
        return {
            "success": True,
            "exam_id": req.exam_id,
            "path": str(exam_dir),
            "documents_saved": len(saved_docs),
            "exam_json_saved": has_exam_json,
            "index_updated": True,
        }

    except Exception as e:
        logger.error(f"publish_exam failed: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Admin: List / Delete / Update published exams ────────────

def _load_index() -> list:
    index_path = EXAMS_DIR / "index.json"
    if not index_path.exists():
        return []
    with open(index_path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def _save_index(data: list):
    index_path = EXAMS_DIR / "index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@router.get("/published-exams")
async def list_published_exams():
    """List all published exams from index.json AND exam_documents table."""
    # 1) Local exams from index.json
    index = _load_index()
    result = []
    seen_ids = set()
    for entry in index:
        exam_path = EXAMS_DIR / entry.get("path", "") / "exam.json"
        has_json = exam_path.exists()
        assets_dir = EXAMS_DIR / entry.get("path", "") / "assets"
        doc_count = len(list(assets_dir.glob("*.png"))) if assets_dir.exists() else 0
        result.append({
            **entry,
            "has_exam_json": has_json,
            "document_count": doc_count,
            "source": "local",
        })
        seen_ids.add(entry.get("id"))

    # 2) Extracted exams from Supabase exam_documents table
    try:
        from app.supabase_client import supabase_admin
        db_result = supabase_admin.table("exam_documents").select(
            "id, subject, year, session, exam_title, created_at"
        ).order("year", desc=True).execute()
        for row in (db_result.data or []):
            if row["id"] in seen_ids:
                continue
            result.append({
                "id": row["id"],
                "subject": row.get("subject") or "Examen",
                "year": row.get("year") or 0,
                "session": row.get("session") or "normale",
                "title": row.get("exam_title") or "Examen extrait",
                "has_exam_json": True,
                "document_count": 0,
                "source": "database",
                "created_at": row.get("created_at"),
            })
            seen_ids.add(row["id"])
    except Exception as e:
        logger.warning(f"Could not load exam_documents: {e}")

    return {"exams": result, "count": len(result)}


@router.delete("/published-exams/{exam_id}")
async def delete_published_exam(exam_id: str):
    """Delete a published exam: remove from index.json and/or exam_documents table."""
    import shutil
    deleted_local = False
    deleted_db = False

    # Try local index.json first
    index = _load_index()
    entry = next((e for e in index if e["id"] == exam_id), None)
    if entry:
        exam_dir = EXAMS_DIR / entry["path"]
        if exam_dir.exists():
            shutil.rmtree(exam_dir)
            logger.info(f"Deleted exam folder: {exam_dir}")
        index = [e for e in index if e["id"] != exam_id]
        _save_index(index)
        logger.info(f"Removed '{exam_id}' from index.json")
        deleted_local = True

    # Try exam_documents table
    try:
        from app.supabase_client import supabase_admin
        supabase_admin.table("exam_documents").delete().eq("id", exam_id).execute()
        deleted_db = True
        logger.info(f"Removed '{exam_id}' from exam_documents table")
    except Exception as e:
        logger.warning(f"Could not delete from exam_documents: {e}")

    if not deleted_local and not deleted_db:
        raise HTTPException(status_code=404, detail="Examen introuvable")

    return {"success": True, "message": f"Examen '{exam_id}' supprimé"}


class UpdateExamRequest(BaseModel):
    subject: Optional[str] = None
    title: Optional[str] = None
    subject_full: Optional[str] = None
    year: Optional[int] = None
    session: Optional[str] = None
    duration_minutes: Optional[int] = None
    coefficient: Optional[int] = None
    total_points: Optional[int] = None
    note: Optional[str] = None


@router.put("/published-exams/{exam_id}")
async def update_published_exam(exam_id: str, req: UpdateExamRequest):
    """Update metadata of a published exam in index.json and/or exam_documents."""
    updates = req.dict(exclude_none=True)
    updated_local = False
    updated_db = False

    # Try local index.json
    index = _load_index()
    entry = next((e for e in index if e["id"] == exam_id), None)
    if entry:
        entry.update(updates)
        # Also update exam.json title/note if it exists
        exam_json_path = EXAMS_DIR / entry["path"] / "exam.json"
        if exam_json_path.exists():
            try:
                with open(exam_json_path, "r", encoding="utf-8") as f:
                    exam_data = json.load(f)
                for k in ("subject", "title", "subject_full", "year", "session", "note", "duration_minutes", "coefficient", "total_points"):
                    if k in updates:
                        exam_data[k] = updates[k]
                with open(exam_json_path, "w", encoding="utf-8") as f:
                    json.dump(exam_data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.warning(f"Could not update exam.json for {exam_id}: {e}")
        _save_index(index)
        updated_local = True

    # Try exam_documents table
    try:
        from app.supabase_client import supabase_admin
        db_updates = {}
        if "title" in updates:
            db_updates["exam_title"] = updates["title"]
        for k in ("subject", "year", "session", "duration_minutes", "coefficient", "total_points"):
            if k in updates:
                db_updates[k] = updates[k]
        if db_updates:
            supabase_admin.table("exam_documents").update(db_updates).eq("id", exam_id).execute()
            updated_db = True
    except Exception as e:
        logger.warning(f"Could not update exam_documents for {exam_id}: {e}")

    if not updated_local and not updated_db:
        raise HTTPException(status_code=404, detail="Examen introuvable")

    logger.info(f"Updated metadata for '{exam_id}': {updates}")
    return {"success": True, "exam": entry or {"id": exam_id, **updates}}


# ── JSON repair helper ────────────────────────────────────────

def _parse_or_repair_json(content: str, finish_reason: str = "") -> dict:
    """Parse JSON from LLM output, auto-repairing truncated responses."""
    if not content or not content.strip():
        raise ValueError("Empty LLM response")

    # 1) Direct parse
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # 2) Extract from markdown code block
    m = re.search(r'```(?:json)?\s*(\{.*)', content, re.DOTALL)
    raw = m.group(1) if m else content

    # 3) Find the first { 
    start = raw.find('{')
    if start < 0:
        raise ValueError(f"No JSON object found in LLM response (finish_reason={finish_reason})")
    raw = raw[start:]

    # 4) Try parsing as-is (maybe it's valid after extraction)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # 5) Stack-based repair for truncated JSON
    repaired = _repair_truncated_json(raw)
    try:
        result = json.loads(repaired)
        logger.warning(f"Auto-repaired truncated JSON ({len(content)} chars, finish_reason={finish_reason})")
        return result
    except json.JSONDecodeError as e:
        logger.error(f"JSON repair failed: {e}")
        logger.error(f"Last 300 chars of raw: ...{raw[-300:]}")
        raise ValueError(f"LLM output trop long (finish_reason={finish_reason}). Le JSON a été tronqué et n'a pas pu être réparé.")


def _repair_truncated_json(text: str) -> str:
    """Stack-based JSON repair for truncated output.
    
    Walks the string character by character tracking open structures,
    then truncates at the last valid position and closes everything.
    """
    stack = []  # tracks [ and {
    in_string = False
    escape_next = False
    last_valid = 0  # last position where we could safely truncate
    i = 0

    while i < len(text):
        c = text[i]

        if escape_next:
            escape_next = False
            i += 1
            continue

        if c == '\\' and in_string:
            escape_next = True
            i += 1
            continue

        if c == '"':
            in_string = not in_string
            if not in_string:
                last_valid = i  # end of a string is a valid cut point
            i += 1
            continue

        if in_string:
            i += 1
            continue

        # Outside string
        if c in ('{', '['):
            stack.append(c)
            i += 1
            continue
        if c == '}':
            if stack and stack[-1] == '{':
                stack.pop()
                last_valid = i
            i += 1
            continue
        if c == ']':
            if stack and stack[-1] == '[':
                stack.pop()
                last_valid = i
            i += 1
            continue
        # For values, commas, colons — mark as valid cut point
        if c in (',', ':', ' ', '\n', '\r', '\t'):
            i += 1
            continue
        # digits, true, false, null
        last_valid = i
        i += 1

    # If nothing to close, return as-is
    if not stack and not in_string:
        return text

    # Truncate at last valid position + 1 if we're in a broken string
    if in_string:
        # Close the current string
        cut = text[:i] + '"'
    else:
        cut = text[:last_valid + 1]

    # Remove trailing comma before closing
    cut = cut.rstrip()
    while cut.endswith(','):
        cut = cut[:-1].rstrip()

    # Close all open structures in reverse order
    for opener in reversed(stack):
        if opener == '{':
            cut += '}'
        elif opener == '[':
            cut += ']'

    return cut


# ── Structure Exam JSON Endpoint ─────────────────────────────

class StructureExamRequest(BaseModel):
    sujet_text: str
    correction_text: str
    subject: str
    year: int
    session: str
    title: str
    documents: list[dict]  # [{name, type, description}]


@router.post("/structure-exam")
async def structure_exam(req: StructureExamRequest):
    """Use DeepSeek LLM to parse OCR text into structured exam JSON matching exam viewer format."""

    # Build document list with GLOBAL index so LLM maps correctly
    docs_lines = []
    for i, d in enumerate(req.documents, 1):
        page = d.get("pageNumber", "?")
        name = d.get("name", f"Document {i}").replace('"', "'")
        desc = d.get("description", "").replace('"', "'").replace('|', ' ')
        dtype = d.get("type", "figure")
        docs_lines.append(
            f'  GLOBAL_DOC_{i}: nom="{name}" | type={dtype} | page_pdf={page} | '
            f'fichier="assets/document_{i}.png" | description="{desc}"'
        )
    docs_block = "\n".join(docs_lines) if docs_lines else "  (aucun document détecté)"

    # Sanitize OCR text: remove characters that could break JSON payload or f-string
    def _sanitize(text: str) -> str:
        # Remove null bytes and control chars except newline/tab
        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)

    sujet_clean = _sanitize(req.sujet_text[:30000])
    correction_clean = _sanitize(req.correction_text[:30000])
    # Sanitize interpolated fields to prevent f-string breakage
    safe_title = req.title.replace('{', '').replace('}', '')
    safe_subject = req.subject.replace('{', '').replace('}', '')
    safe_session = req.session.replace('{', '').replace('}', '')

    # ── Shared rules block ──
    rules_block = f"""RÈGLES CRITIQUES:

1. DISTINCTION SUJET vs CORRECTION (TRÈS IMPORTANT):
   - "content" = texte de la QUESTION tel qu'il apparaît dans le SUJET (ce que l'élève doit faire). JAMAIS la réponse.
   - "correction.content" = la RÉPONSE/CORRECTION officielle uniquement.

2. TYPES — Examens marocains:
   QCM: items numérotés avec propositions a,b,c,d → type="qcm" avec sub_questions. Chaque sub_question a "points", "choices":[{{"letter":"a","text":"..."}}], "correction":{{"correct_answer":"c"}}
   ASSOCIATION: "Recopiez les couples..." → type="association" avec "items_left":[...], "items_right":[...], "correction":{{"content":"...","correct_pairs":[{{"left":"1","right":"b"}}]}}
   VRAI_FAUX: → sub_questions avec correction.correct_answer ("vrai"/"faux")
   SCHEMA: question utilisant document/figure → type="schema" avec "documents":[{{"id":"doc_gN","type":"figure","title":"...","description":"...","src":"assets/document_N.png"}}]
   OPEN: toute autre question

3. SOUS-QUESTIONS: 1.a, 1.b = sub_questions SÉPARÉES.
4. Contenu des questions: recopier le texte ORIGINAL du SUJET, pas un résumé.
5. Corrections: concises mais complètes."""

    # ── Helper to call DeepSeek ──
    async def _call_deepseek(prompt_text: str, label: str) -> tuple[dict, str]:
        headers = {
            "Authorization": f"Bearer {settings.deepseek_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.deepseek_model,
            "messages": [
                {"role": "system", "content": "Expert en structuration d'examens marocains. 'content' = QUESTION du SUJET, 'correction.content' = RÉPONSE. Réponds uniquement en JSON valide."},
                {"role": "user", "content": prompt_text},
            ],
            "max_tokens": 8192,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
        logger.info(f"[{label}] prompt size: {len(prompt_text)} chars (~{len(prompt_text)//4} tokens)")
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(settings.deepseek_api_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        finish_reason = data.get("choices", [{}])[0].get("finish_reason", "")
        logger.info(f"[{label}] response: {len(content)} chars, finish_reason={finish_reason}")
        return _parse_or_repair_json(content, finish_reason), finish_reason

    # ── Diagnostic ──
    has_p1 = "première partie" in sujet_clean.lower() or "restitution" in sujet_clean.lower()
    has_p2 = "deuxième partie" in sujet_clean.lower() or "exploitation" in sujet_clean.lower()
    logger.info(f"OCR diagnostic: sujet={len(sujet_clean)} chars, corr={len(correction_clean)} chars, has_P1={has_p1}, has_P2={has_p2}")

    try:
        # ═══ CALL 1: Première partie (Restitution des connaissances, ~5pts) ═══
        prompt_p1 = f"""Structure UNIQUEMENT la "Première partie" (Restitution des connaissances, ~5pts) de cet examen BAC marocain en JSON.

SUJET COMPLET:
{sujet_clean}

CORRECTION COMPLÈTE:
{correction_clean}

DOCUMENTS:
{docs_block}

{rules_block}

Pour la Première partie, les documents sont directement dans la question.

Réponds avec EXACTEMENT ce format JSON:
{{"name":"Première partie : Restitution des connaissances","points":5,"questions":[
{{"id":"p1q1","number":"I","type":"open","points":N,"content":"texte question...","correction":{{"content":"réponse..."}}}},
{{"id":"p1q2","number":"II","type":"qcm","points":N,"content":"Pour chaque item...","sub_questions":[
{{"id":"p1q2_1","number":"1","type":"qcm","points":0.5,"content":"...","choices":[{{"letter":"a","text":"..."}},{{"letter":"b","text":"..."}}],"correction":{{"correct_answer":"c"}}}}
]}}
]}}

JSON uniquement — un seul objet avec "name", "points", "questions"."""

        part1_json, fr1 = await _call_deepseek(prompt_p1, "Part1")
        logger.info(f"Part1 result: {len(part1_json.get('questions', []))} questions")

        # ═══ CALL 2: Deuxième partie (Exploitation des documents, ~15pts) ═══
        prompt_p2 = f"""Structure UNIQUEMENT la "Deuxième partie" (Exploitation des documents, ~15pts) de cet examen BAC marocain en JSON.

SUJET COMPLET:
{sujet_clean}

CORRECTION COMPLÈTE:
{correction_clean}

DOCUMENTS:
{docs_block}

{rules_block}

Pour la Deuxième partie, les documents sont dans l'exercice ET référencés dans chaque question via "documents":["doc_gN"].

Réponds avec EXACTEMENT ce format JSON:
{{"name":"Deuxième partie : Exploitation des documents","points":15,"exercises":[
{{"name":"Exercice 1","points":5,"context":"résumé bref...","documents":[{{"id":"doc_g2","type":"figure","title":"Document 1","description":"...","src":"assets/document_2.png"}}],
"questions":[{{"id":"ex1q1","number":"1","type":"open","points":1.5,"content":"texte question...","documents":["doc_g2"],"correction":{{"content":"réponse..."}}}}]
}},
{{"name":"Exercice 2","points":5,"context":"...","documents":[...],"questions":[...]}}
]}}

JSON uniquement — un seul objet avec "name", "points", "exercises"."""

        part2_json, fr2 = await _call_deepseek(prompt_p2, "Part2")
        logger.info(f"Part2 result: {len(part2_json.get('exercises', []))} exercises")

        # ═══ MERGE into final exam JSON ═══
        exam_json = {
            "title": safe_title,
            "subject": safe_subject.upper() if len(safe_subject) <= 3 else safe_subject,
            "subject_full": part1_json.get("subject_full") or part2_json.get("subject_full") or safe_title,
            "year": req.year,
            "session": safe_session,
            "duration_minutes": 180,
            "coefficient": 5,
            "total_points": 20,
            "parts": [part1_json, part2_json],
        }

        part_names = [p.get("name", "?") for p in exam_json["parts"]]
        logger.info(f"Structured exam: {len(part_names)} parts: {part_names}")
        truncated = fr1 == "length" or fr2 == "length"
        if truncated:
            logger.warning("One or more LLM calls were TRUNCATED (finish_reason=length)")

        return {"success": True, "exam_json": exam_json, "finish_reason": f"p1={fr1},p2={fr2}"}

    except httpx.HTTPStatusError as e:
        error_body = e.response.text[:500]
        logger.error(f"DeepSeek API error: {e.response.status_code} — {error_body}")
        raise HTTPException(status_code=502, detail=f"DeepSeek API error: {e.response.status_code} — {error_body}")
    except Exception as e:
        logger.error(f"structure_exam failed: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
