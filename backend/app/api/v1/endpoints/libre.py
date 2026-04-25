"""
Libre Mode API Endpoints
Handles free-form Q&A sessions without chapter constraints.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.dependencies import get_current_student
from app.supabase_client import get_supabase_admin
from datetime import datetime
import uuid

router = APIRouter(prefix="/libre", tags=["libre"])
supabase = get_supabase_admin()


class LibreStartRequest(BaseModel):
    title: Optional[str] = None


class LibreMessageRequest(BaseModel):
    conversation_id: str
    message: str


@router.post("/start")
async def start_libre_session(
    data: LibreStartRequest,
    student: dict = Depends(get_current_student)
):
    """
    Start a new libre conversation session.
    No chapter required - student can ask anything.
    """
    try:
        conversation_data = {
            "id": str(uuid.uuid4()),
            "student_id": student['id'],
            "title": data.title or "Conversation libre",
            "started_at": datetime.utcnow().isoformat()
        }
        
        result = supabase.table('libre_conversations').insert(conversation_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create conversation")
        
        return result.data[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_libre_history(
    student: dict = Depends(get_current_student),
    limit: int = 20
):
    """
    Get past libre conversations for the student.
    Returns most recent conversations.
    """
    try:
        result = supabase.table('libre_conversations').select(
            '*'
        ).eq('student_id', student['id']).order(
            'started_at', desc=True
        ).limit(limit).execute()
        
        return {
            "conversations": result.data if result.data else [],
            "count": len(result.data) if result.data else 0
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    student: dict = Depends(get_current_student)
):
    """
    Get a specific conversation with all messages.
    """
    try:
        # Verify ownership
        conv_result = supabase.table('libre_conversations').select(
            '*'
        ).eq('id', conversation_id).eq('student_id', student['id']).execute()
        
        if not conv_result.data:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get messages
        messages_result = supabase.table('libre_messages').select(
            '*'
        ).eq('conversation_id', conversation_id).order('timestamp').execute()
        
        return {
            "conversation": conv_result.data[0],
            "messages": messages_result.data if messages_result.data else []
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/end/{conversation_id}")
async def end_libre_session(
    conversation_id: str,
    student: dict = Depends(get_current_student)
):
    """
    End a libre conversation session.
    Updates ended_at timestamp.
    """
    try:
        result = supabase.table('libre_conversations').update({
            "ended_at": datetime.utcnow().isoformat()
        }).eq('id', conversation_id).eq('student_id', student['id']).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {"success": True, "conversation_id": conversation_id}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
