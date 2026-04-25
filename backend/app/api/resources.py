from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from pydantic import BaseModel
import uuid
from datetime import datetime
import os
import shutil
from pathlib import Path

from app.dependencies import get_current_student
from app.supabase_client import get_supabase

router = APIRouter()


class ResourceCreate(BaseModel):
    lesson_id: str
    section_title: str
    resource_type: str
    title: str
    description: str
    file_path: Optional[str] = None
    external_url: Optional[str] = None
    trigger_text: Optional[str] = None
    phase: Optional[str] = None
    difficulty_tier: str = "intermediate"
    concepts: List[str] = []
    metadata: dict = {}
    order_index: int = 0


class ResourceUpdate(BaseModel):
    section_title: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    external_url: Optional[str] = None
    trigger_text: Optional[str] = None
    phase: Optional[str] = None
    difficulty_tier: Optional[str] = None
    concepts: Optional[List[str]] = None
    metadata: Optional[dict] = None
    order_index: Optional[int] = None


@router.get("/resources")
async def get_resources(
    type: Optional[str] = None,
    lesson_id: Optional[str] = None,
    current_user: dict = Depends(get_current_student)
):
    """Get all resources, optionally filtered by type or lesson."""
    supabase = get_supabase()
    
    query = supabase.table("lesson_resources").select("*")
    
    if type:
        query = query.eq("resource_type", type)
    if lesson_id:
        query = query.eq("lesson_id", lesson_id)
    
    query = query.order("order_index")
    
    print(f"[GET RESOURCES] Fetching resources - type: {type}, lesson_id: {lesson_id}")
    result = query.execute()
    print(f"[GET RESOURCES] Found {len(result.data)} resources")
    return result.data


@router.get("/resources/{resource_id}")
async def get_resource(
    resource_id: str,
    current_user: dict = Depends(get_current_student)
):
    """Get a specific resource by ID."""
    supabase = get_supabase()
    
    result = supabase.table("lesson_resources").select("*").eq("id", resource_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return result.data[0]


@router.post("/resources")
async def create_resource(
    resource: ResourceCreate,
    current_user: dict = Depends(get_current_student)
):
    """Create a new resource."""
    supabase = get_supabase()
    
    resource_data = {
        "lesson_id": resource.lesson_id,
        "section_title": resource.section_title,
        "resource_type": resource.resource_type,
        "title": resource.title,
        "description": resource.description,
        "file_path": resource.file_path,
        "external_url": resource.external_url,
        "trigger_text": resource.trigger_text,
        "phase": resource.phase,
        "difficulty_tier": resource.difficulty_tier,
        "concepts": resource.concepts,
        "metadata": resource.metadata,
        "order_index": resource.order_index
    }
    
    print(f"[CREATE RESOURCE] Creating resource: {resource.title}")
    print(f"[CREATE RESOURCE] Data: {resource_data}")
    
    try:
        result = supabase.table("lesson_resources").insert(resource_data).execute()
        print(f"[CREATE RESOURCE] Success! Created resource with ID: {result.data[0]['id']}")
        return result.data[0]
    except Exception as e:
        print(f"[CREATE RESOURCE] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating resource: {str(e)}")


@router.put("/resources/{resource_id}")
async def update_resource(
    resource_id: str,
    resource: ResourceUpdate,
    current_user: dict = Depends(get_current_student)
):
    """Update an existing resource."""
    supabase = get_supabase()
    
    # Build update data excluding None values
    update_data = {k: v for k, v in resource.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = supabase.table("lesson_resources").update(update_data).eq("id", resource_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return result.data[0]


@router.delete("/resources/{resource_id}")
async def delete_resource(
    resource_id: str,
    current_user: dict = Depends(get_current_student)
):
    """Delete a resource."""
    supabase = get_supabase()
    
    # Get resource to check file path
    resource_result = supabase.table("lesson_resources").select("*").eq("id", resource_id).execute()
    
    if not resource_result.data:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    resource = resource_result.data[0]
    
    # Delete file from Supabase Storage if it exists
    if resource.get("file_path"):
        file_path = resource["file_path"]
        
        # Check if it's a Supabase Storage URL
        if "supabase" in file_path and "pedagogical-resources" in file_path:
            try:
                # Extract storage path from URL
                # URL format: https://xxx.supabase.co/storage/v1/object/public/pedagogical-resources/path/to/file
                storage_path = file_path.split("pedagogical-resources/")[-1]
                supabase.storage.from_("pedagogical-resources").remove([storage_path])
                print(f"[DELETE] Deleted file from Supabase Storage: {storage_path}")
            except Exception as e:
                print(f"[DELETE] Error deleting file from storage: {e}")
        # Legacy: Delete local files if they exist
        elif file_path.startswith("/media/"):
            local_file_path = Path("frontend/public") / file_path.lstrip("/")
            if local_file_path.exists():
                try:
                    local_file_path.unlink()
                    print(f"[DELETE] Deleted local file: {local_file_path}")
                except Exception as e:
                    print(f"[DELETE] Error deleting local file: {e}")
    
    # Delete from database
    supabase.table("lesson_resources").delete().eq("id", resource_id).execute()
    
    return {"message": "Resource deleted successfully"}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    type: str = Form(...),
    lesson_id: str = Form(...),
    current_user: dict = Depends(get_current_student)
):
    """Upload a file (image or video) to Supabase Storage and return its public URL."""
    
    print(f"[UPLOAD] Starting upload - type: {type}, lesson_id: {lesson_id}, filename: {file.filename}")
    
    # Validate file type
    allowed_types = {
        "image": ["image/jpeg", "image/png", "image/gif", "image/svg+xml", "image/webp"],
        "video": ["video/mp4", "video/webm", "video/ogg"]
    }
    
    if type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid type")
    
    if file.content_type not in allowed_types[type]:
        raise HTTPException(status_code=400, detail=f"Invalid file type for {type}")
    
    # Get lesson info to build path
    supabase = get_supabase()
    lesson_result = supabase.table("lessons").select("*, chapters(*)").eq("id", lesson_id).execute()
    
    if not lesson_result.data:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    lesson = lesson_result.data[0]
    
    # Generate unique filename
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    
    # Build storage path: type/lesson_id/filename
    storage_path = f"{type}s/lesson_{lesson_id[:8]}/{unique_filename}"
    
    print(f"[UPLOAD] Uploading to Supabase Storage: {storage_path}")
    
    # Upload to Supabase Storage
    try:
        # Read file content
        file_content = await file.read()
        
        # Upload to storage bucket
        result = supabase.storage.from_("pedagogical-resources").upload(
            path=storage_path,
            file=file_content,
            file_options={"content-type": file.content_type}
        )
        
        print(f"[UPLOAD] File uploaded successfully to Supabase Storage")
        
        # Get public URL
        public_url = supabase.storage.from_("pedagogical-resources").get_public_url(storage_path)
        
        # Clean URL by removing trailing query parameters (like '?')
        if public_url.endswith('?'):
            public_url = public_url[:-1]
        
        print(f"[UPLOAD] Public URL: {public_url}")
        
        return {
            "file_path": public_url,
            "filename": unique_filename,
            "storage_path": storage_path
        }
        
    except Exception as e:
        print(f"[UPLOAD] Error uploading to Supabase Storage: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.get("/lessons")
async def get_lessons(
    current_user: dict = Depends(get_current_student)
):
    """Get all lessons for dropdown selection."""
    supabase = get_supabase()
    
    result = supabase.table("lessons").select("id, title_fr, chapter_id, content, chapters(title_fr)").order("order_index").execute()
    
    return result.data
