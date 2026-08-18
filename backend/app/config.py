from pathlib import Path

from pydantic_settings import BaseSettings
from functools import lru_cache

# Le fichier vit a cote du paquet, pas dans le repertoire d'ou on lance.
# Avec un chemin relatif, `uvicorn --app-dir backend` demarre depuis la
# racine du depot, ne trouve rien, et l'application meurt sur
# « supabase_url is required » — une erreur qui ne dit pas qu'il s'agit
# d'un probleme de repertoire courant.
_FICHIER_ENV = Path(__file__).resolve().parent.parent / ".env"


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

    # ⚠️ AUCUNE CLÉ EN DUR ICI. Ce dépôt est public : une clé écrite dans ce
    # fichier finit indexée, et Google la révoque — c'est exactement ce qui est
    # arrivé à la clé TTS (« Your API key was reported as leaked »), qui a fait
    # tomber le dernier repli vocal le jour où le tunnel Colab s'est coupé.
    # Toutes les valeurs ci-dessous vivent dans backend/.env (et son jumeau de
    # déploiement deploy/backend.env), tous deux ignorés par git.

    # Gemini API (used for LLM, NOT for TTS)
    gemini_api_key: str = ""

    # Gemini TTS (using 2.5 Flash Preview for fast multilingual TTS)
    # Used ONLY for Darija (mixed) — expressive voice needed for dialect
    gemini_tts_api_key: str = ""
    gemini_tts_model: str = "gemini-2.5-flash-preview-tts"
    gemini_tts_voice: str = "Kore"  # Fast, clear female voice

    # Google Cloud Text-to-Speech (Standard voices, ~4$/1M chars)
    # Used for Arabic MSA (ar-XA). French uses browser Web Speech API (free).
    # Reuses Gemini API key by default — requires Cloud TTS API enabled on the same project.
    google_cloud_tts_api_key: str = ""   # falls back to gemini_tts_api_key if empty
    google_cloud_tts_voice_ar: str = "ar-XA-Standard-D"  # female MSA standard voice
    google_cloud_tts_voice_fr: str = "fr-FR-Standard-C"  # used only if frontend fallback fails

    # Self-hosted Darija TTS (Gradio endpoint — e.g. Chatterbox on Colab)
    # Set this to your Gradio public URL; leave empty to disable.
    # ⚠️ Une URL gradio.live expire en ~72 h. En laisser une périmée en dur ne
    # sert à rien et coûte un aller-retour 404 à CHAQUE échec d'Academy, juste
    # avant le repli utile. Vide = repli désactivé ; la remettre via GRADIO_TTS_URL.
    gradio_tts_url: str = ""
    gradio_tts_exaggeration: float = 0.5
    gradio_tts_temperature: float = 0.8
    gradio_tts_cfg_weight: float = 0.5

    # Academy Darija-FR TTS (modèle fine-tuné auto-hébergé — Colab + tunnel).
    # API FastAPI : POST /tts (WAV brut), GET /health, GET /voices.
    # ⚠️ URL et JETON vivent dans backend/.env (jamais dans le dépôt) :
    #    ACADEMY_TTS_URL=https://…trycloudflare.com
    #    ACADEMY_TTS_TOKEN=…
    # L'URL du tunnel change à chaque redémarrage du notebook Colab.
    academy_tts_url: str = ""
    academy_tts_token: str = ""
    academy_tts_voice: str = ""          # vide = première voix du serveur
    academy_tts_normaliser: int = 1      # applique l'orthographe darija (ال → ل)
    academy_tts_exaggeration: float = 0.45   # > 0.6 dérive sur les phrases longues
    academy_tts_temperature: float = 0.7     # 0.3 = quasi déterministe, plus plat
    academy_tts_cfg_weight: float = 0.3      # bas = debit plus lent et pose ;
    #                                        0.7 colle au texte mais accelere
    # Flux continu (/tts/stream) : premier son ~5x plus tôt (2,9 s au lieu de
    # 14,5 s, mesuré). ⚠️ Tant que le serveur n'est pas corrigé, il PERD ~0,7 s
    # à la fin de chaque énoncé (le dernier mot est coupé). Mettre à 0 pour
    # revenir au chemin par segments complets, sans redéploiement de code.
    academy_tts_stream: int = 1

    # TTS cache (filesystem)
    tts_cache_enabled: int = 1
    tts_cache_dir: str = "data/tts_cache"
    tts_cache_max_bytes: int = 500 * 1024 * 1024  # 500 MB cap
    # Global kill-switch: set to 1 to disable all server-side TTS (costs $0)
    tts_disabled: int = 1

    # Mistral OCR API (for extracting text from images)
    mistral_api_key: str = ""
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
        env_file = _FICHIER_ENV
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
