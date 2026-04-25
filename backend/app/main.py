"""
AI Tutor BAC - Main FastAPI Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.api.v1.api import api_router
from app.websockets.session_handler import SessionHandler
from app.supabase_client import get_supabase
import logging
import os
import threading

logger = logging.getLogger(__name__)
settings = get_settings()


def _init_rag_background():
    """Initialize RAG service in background thread so server starts fast."""
    try:
        from app.services.rag_service import get_rag_service
        print("[Startup] ===== RAG INITIALIZATION STARTING =====")
        rag = get_rag_service()
        rag.index_all()
        print(f"[Startup] ===== RAG READY: {len(rag.documents)} chunks indexed =====")
    except Exception as e:
        print(f"[Startup] ===== RAG INIT FAILED: {e} =====")


async def _warmup_tts_background():
    """Pregenerate common TTS phrases so the steady-state cache hit rate is high."""
    try:
        from app.services.tts_service import tts_service
        print("[Startup] Launching TTS cache warmup...")
        counts = await tts_service.warmup()
        print(f"[Startup] TTS warmup done: {counts}")
    except Exception as e:
        print(f"[Startup] TTS warmup failed (non-fatal): {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # RAG initialized once at startup in a background thread (uses cached
    # chunks + FAISS index from data/rag_cache). No OCR is triggered when
    # the cache is hot — startup stays fast and the server is responsive
    # immediately while RAG warms up off-thread.
    if getattr(settings, 'rag_disabled', 0) != 0:
        print("[Startup] RAG explicitly disabled via RAG_DISABLED env var.")
    else:
        print("[Startup] Launching RAG initialization in background...")
        rag_thread = threading.Thread(target=_init_rag_background, daemon=True)
        rag_thread.start()

    # TTS warmup intentionally DISABLED at startup.
    # - Gemini 2.5 preview TTS has a tight free-tier quota (~10 RPM) that
    #   burns out in minutes if we pre-generate phrases on boot.
    # - The cache fills up naturally with real student traffic, which is
    #   a better signal of what phrases actually matter.
    # Use `python -m scripts.enrich_tts_cache` offline if you want to
    # proactively warm the cache between sessions.
    print("[Startup] TTS warmup skipped (cache fills on demand).")

    yield
    print("[Shutdown] Server stopping.")


app = FastAPI(
    title="AI Tutor BAC",
    description="AI Tutoring Platform for Moroccan Baccalaureate - 2ème BAC Sciences",
    version="0.1.0",
    lifespan=lifespan,
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser tous les origins en développement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST API routes
app.include_router(api_router)

# Serve exam assets (images, documents) as static files
_exams_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "exams")
if os.path.isdir(_exams_dir):
    app.mount("/static/exams", StaticFiles(directory=_exams_dir), name="exam_assets")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "ai-tutor-bac"}


@app.websocket("/ws/tutor/{token}")
async def websocket_tutor(websocket: WebSocket, token: str):
    """WebSocket endpoint for real-time tutoring voice pipeline."""
    supabase = get_supabase()
    
    try:
        # Verify token with Supabase Auth
        user_response = supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            # Must accept before closing to avoid 403
            await websocket.accept()
            await websocket.close(code=4001, reason="Invalid or expired token")
            return
        
        student_id = str(user_response.user.id)
        
        handler = SessionHandler(websocket=websocket, student_id=student_id)
        await handler.handle_connection()
        
    except Exception as e:
        logger.error(f"WebSocket auth error: {e}")
        try:
            # Accept first so we can send a proper close frame
            await websocket.accept()
            await websocket.send_json({"type": "error", "message": f"Authentication failed: {str(e)}"})
            await websocket.close(code=4001, reason=f"Authentication failed: {str(e)}")
        except Exception:
            pass
