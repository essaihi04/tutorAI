from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""

    # Database
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/ai_tutor_bac"
    database_url_sync: str = "postgresql://postgres:password@localhost:5432/ai_tutor_bac"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT Auth
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # DeepSeek API
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_api_url: str = "https://api.deepseek.com/chat/completions"
    deepseek_model: str = "deepseek-chat"

    # Google Cloud (not used - using Gemini API key instead)
    # google_application_credentials: str = ""
    # google_cloud_project_id: str = ""
    # google_cloud_credentials_path: str = ""
    # gcp_project_id: str = ""
    # vertex_project_id: str = ""
    # vertex_location: str = ""

    # Gemini API (used for LLM, NOT for TTS)
    gemini_api_key: str = "AIzaSyDgiqb3bRFO97SIPvUnLBI0wF6iU1aLgI8"

    # Gemini TTS (using 2.5 Flash Preview for fast multilingual TTS)
    # Used ONLY for Darija (mixed) — expressive voice needed for dialect
    gemini_tts_api_key: str = "AIzaSyChw2Ab-CXl1Ynm2c9iS-lp35cqD1HRQNo"
    gemini_tts_model: str = "gemini-2.5-flash-preview-tts"
    gemini_tts_voice: str = "Kore"  # Fast, clear female voice

    # Google Cloud Text-to-Speech (Standard voices, ~4$/1M chars)
    # Used for Arabic MSA (ar-XA). French uses browser Web Speech API (free).
    # Reuses Gemini API key by default — requires Cloud TTS API enabled on the same project.
    google_cloud_tts_api_key: str = "AIzaSyAmfczktE0VKLvdeA6dWflDj8PTowr97tY"   # falls back to gemini_tts_api_key if empty
    google_cloud_tts_voice_ar: str = "ar-XA-Standard-D"  # female MSA standard voice
    google_cloud_tts_voice_fr: str = "fr-FR-Standard-C"  # used only if frontend fallback fails

    # Self-hosted Darija TTS (Gradio endpoint — e.g. Chatterbox on Colab)
    # Set this to your Gradio public URL; leave empty to disable.
    gradio_tts_url: str = "https://46a78facb3c86e65b4.gradio.live"
    gradio_tts_exaggeration: float = 0.5
    gradio_tts_temperature: float = 0.8
    gradio_tts_cfg_weight: float = 0.5

    # TTS cache (filesystem)
    tts_cache_enabled: int = 1
    tts_cache_dir: str = "data/tts_cache"
    tts_cache_max_bytes: int = 500 * 1024 * 1024  # 500 MB cap
    # Global kill-switch: set to 1 to disable all server-side TTS (costs $0)
    tts_disabled: int = 1

    # Mistral OCR API (for extracting text from images)
    mistral_api_key: str = "vagL3uMJ8KSNqbVptYHCRjEphmUzSGmf"
    mistral_ocr_model: str = "mistral-ocr-latest"

    # Google Cloud Vertex AI (not used - using Gemini API key instead)
    # gcp_project_id: str = ""
    # vertex_project_id: str = ""
    # vertex_location: str = ""

    # Admin Dashboard
    admin_password: str = "admin123"  # Change in production via .env

    # App
    app_env: str = "development"
    cors_origins: str = "http://localhost:5173"
    
    # RAG
    rag_disabled: int = 0

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
