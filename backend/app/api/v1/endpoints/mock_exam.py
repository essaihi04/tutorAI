"""
Mock Exam API Endpoints — Generate, list, and manage AI-generated exam blancs.
"""
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.services.mock_exam_service import mock_exam_service

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
