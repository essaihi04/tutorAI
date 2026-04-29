"""
Mock Exam API Endpoints — Generate, list, and manage AI-generated exam blancs.
"""
import logging
import shutil
from typing import Optional
from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel

from app.services.mock_exam_service import mock_exam_service, MOCK_EXAMS_DIR
from app.services.mock_exam_printable import render_printable_html

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/mock-exam", tags=["mock-exam"])


# ─── Auth dependency (reuse admin token check) ────────────────────────

def _get_admin_dep():
    from app.api.v1.endpoints.admin import _verify_admin_token
    return _verify_admin_token


# ─── Schemas ──────────────────────────────────────────────────────────

class GenerateMockExamRequest(BaseModel):
    subject: str = "SVT"
    target_domains: Optional[list[str]] = None


class UpdateStatusRequest(BaseModel):
    status: str  # draft, published, archived


# ─── Endpoints ────────────────────────────────────────────────────────

@router.post("/generate")
async def generate_mock_exam(
    req: GenerateMockExamRequest,
    admin: bool = Depends(_get_admin_dep()),
):
    """Generate a new mock exam using AI. Admin-only."""
    try:
        exam = await mock_exam_service.generate_mock_exam(
            subject=req.subject,
            target_domains=req.target_domains,
        )
        return {
            "success": True,
            "exam_id": exam["id"],
            "title": exam["title"],
            "domains": exam.get("domains_covered", {}),
            "image_prompts_count": len(mock_exam_service.get_image_prompts(req.subject, exam["id"])),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Mock exam generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.get("/list")
async def list_mock_exams(
    subject: Optional[str] = None,
    admin: bool = Depends(_get_admin_dep()),
):
    """List all generated mock exams. Admin-only."""
    return mock_exam_service.list_mock_exams(subject)


@router.get("/{subject}/{exam_id}")
async def get_mock_exam(subject: str, exam_id: str):
    """Get a specific mock exam. Published exams accessible by students."""
    exam = mock_exam_service.get_mock_exam(subject, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Mock exam not found")
    return exam


@router.get("/{subject}/{exam_id}/printable", response_class=HTMLResponse)
async def get_printable(
    subject: str,
    exam_id: str,
    type: str = Query("sujet", pattern="^(sujet|corrige)$"),
    autoprint: int = Query(0),
):
    """Render a mock exam as a print-ready HTML page (BAC paper layout).

    The user opens it in a new tab and uses the browser's print dialog
    (Ctrl+P → "Save as PDF") to obtain a PDF identical to the rendered
    layout, with embedded images and KaTeX-rendered math.
    """
    exam = mock_exam_service.get_mock_exam(subject, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Mock exam not found")
    subj_norm = mock_exam_service._normalize_subject(subject)
    assets_dir = MOCK_EXAMS_DIR / subj_norm / exam_id / "assets"
    html_str = render_printable_html(exam, subj_norm, variant=type, assets_dir=assets_dir, autoprint=bool(autoprint))
    return HTMLResponse(content=html_str)


@router.get("/{subject}/{exam_id}/image-prompts")
async def get_image_prompts(
    subject: str,
    exam_id: str,
    admin: bool = Depends(_get_admin_dep()),
):
    """Get image generation prompts for a mock exam. Admin-only."""
    prompts = mock_exam_service.get_image_prompts(subject, exam_id)
    if not prompts:
        raise HTTPException(status_code=404, detail="No image prompts found")
    return prompts


@router.patch("/{subject}/{exam_id}/status")
async def update_status(
    subject: str,
    exam_id: str,
    req: UpdateStatusRequest,
    admin: bool = Depends(_get_admin_dep()),
):
    """Update mock exam status (draft → published → archived). Admin-only."""
    if req.status not in ("draft", "published", "archived"):
        raise HTTPException(status_code=400, detail="Invalid status")
    ok = mock_exam_service.update_mock_exam_status(subject, exam_id, req.status)
    if not ok:
        raise HTTPException(status_code=404, detail="Mock exam not found")
    return {"ok": True, "status": req.status}


@router.get("/published")
async def list_published_exams(subject: Optional[str] = None):
    """List published mock exams (accessible by students)."""
    all_exams = mock_exam_service.list_mock_exams(subject)
    return [e for e in all_exams if e.get("status") == "published"]


@router.post("/{subject}/{exam_id}/upload-image")
async def upload_image(
    subject: str,
    exam_id: str,
    doc_id: str = Form(...),
    file: UploadFile = File(...),
    admin: bool = Depends(_get_admin_dep()),
):
    """Upload an image for a specific document in a mock exam. Admin-only."""
    # Validate exam exists
    exam = mock_exam_service.get_mock_exam(subject, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Mock exam not found")
    
    # Validate file type
    allowed = {"image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif", "image/svg+xml"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail=f"Type non supporté: {file.content_type}")
    
    # Determine extension
    ext_map = {"image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg",
               "image/webp": ".webp", "image/gif": ".gif", "image/svg+xml": ".svg"}
    ext = ext_map.get(file.content_type, ".png")
    
    # Save to assets dir (use the same normalization as the service so the
    # upload lands in the SAME directory the loader/serving code reads from —
    # e.g. "Physique-Chimie" → "physique", not "physique-chimie").
    subj_norm = mock_exam_service._normalize_subject(subject)
    assets_dir = MOCK_EXAMS_DIR / subj_norm / exam_id / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{doc_id}{ext}"
    filepath = assets_dir / filename

    # Remove any existing image for this doc_id (incl. different extension)
    # so a PNG → JPG replacement doesn't leave orphan files that confuse the
    # listing endpoint.
    for old in assets_dir.glob(f"{doc_id}.*"):
        if old.is_file() and old.name != filename:
            try:
                old.unlink()
                logger.info(f"[MockExam] Removed stale image {old.name} before replace")
            except Exception as e:
                logger.warning(f"[MockExam] Could not remove stale {old.name}: {e}")

    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Update the exam.json to set the src for this doc_id
    src_path = f"assets/{filename}"
    _update_doc_src(exam, doc_id, src_path)
    from app.services.mock_exam_service import _save_json
    exam_path = MOCK_EXAMS_DIR / subj_norm / exam_id / "exam.json"
    _save_json(exam_path, exam)
    
    # Return the public URL for serving
    public_url = f"/static/mock-exams/{subj_norm}/{exam_id}/assets/{filename}"
    logger.info(f"[MockExam] Uploaded image for {doc_id}: {public_url}")
    
    return {"ok": True, "doc_id": doc_id, "filename": filename, "url": public_url}


@router.delete("/{subject}/{exam_id}/image/{doc_id}")
async def delete_image(
    subject: str,
    exam_id: str,
    doc_id: str,
    admin: bool = Depends(_get_admin_dep()),
):
    """Delete an uploaded image for a specific document. Admin-only.

    Removes all files matching ``{doc_id}.*`` in the assets directory and
    clears the ``src`` field in ``exam.json`` for that doc_id.
    """
    exam = mock_exam_service.get_mock_exam(subject, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Mock exam not found")

    subj_norm = mock_exam_service._normalize_subject(subject)
    assets_dir = MOCK_EXAMS_DIR / subj_norm / exam_id / "assets"
    removed: list[str] = []
    if assets_dir.exists():
        for f in assets_dir.glob(f"{doc_id}.*"):
            if f.is_file():
                try:
                    f.unlink()
                    removed.append(f.name)
                except Exception as e:
                    logger.warning(f"[MockExam] Could not delete {f.name}: {e}")

    # Clear the src field in exam.json for this doc_id
    _update_doc_src(exam, doc_id, "")
    from app.services.mock_exam_service import _save_json
    exam_path = MOCK_EXAMS_DIR / subj_norm / exam_id / "exam.json"
    _save_json(exam_path, exam)

    logger.info(f"[MockExam] Deleted image(s) for {doc_id}: {removed}")
    return {"ok": True, "doc_id": doc_id, "removed": removed}


@router.get("/{subject}/{exam_id}/images")
async def list_uploaded_images(
    subject: str,
    exam_id: str,
    admin: bool = Depends(_get_admin_dep()),
):
    """List all uploaded images for a mock exam. Admin-only."""
    subj_norm = mock_exam_service._normalize_subject(subject)
    assets_dir = MOCK_EXAMS_DIR / subj_norm / exam_id / "assets"
    if not assets_dir.exists():
        return []
    
    images = []
    for f in sorted(assets_dir.iterdir()):
        if f.is_file() and f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}:
            doc_id = f.stem  # filename without extension = doc_id
            images.append({
                "doc_id": doc_id,
                "filename": f.name,
                "url": f"/static/mock-exams/{subj_norm}/{exam_id}/assets/{f.name}",
            })
    return images


def _update_doc_src(exam: dict, doc_id: str, src: str):
    """Update the src field of a document in the exam JSON.

    Scans documents at part level AND inside exercises, since SVT Part 1
    stores documents directly on the part while PC/Math nest them under
    exercises.
    """
    for part in exam.get("parts", []):
        # Documents at part level (e.g. SVT Part 1)
        for doc in part.get("documents", []) or []:
            if doc.get("id") == doc_id:
                doc["src"] = src
                return
        # Documents inside exercises (e.g. SVT Part 2, PC, Math)
        for ex in part.get("exercises", []) or []:
            for doc in ex.get("documents", []) or []:
                if doc.get("id") == doc_id:
                    doc["src"] = src
                    return
