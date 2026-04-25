"""
Speech-to-Text service using Gemini 1.5 Flash (multimodal).

Advantages over Google Cloud Speech-to-Text:
  • No separate GCP credentials needed (reuses gemini_api_key)
  • Native multilingual support (French, Arabic MSA, Darija, code-switching)
  • Better accuracy for Moroccan Darija than ar-MA model
  • Pay-per-token pricing (~$0.075 / 1M input tokens for audio)
"""
from __future__ import annotations

import base64
import sys
from typing import Optional

import httpx

from app.config import get_settings


settings = get_settings()


def _safe_log(*parts):
    message = " ".join(str(p) for p in parts)
    try:
        print(message)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        print(message.encode(enc, errors="replace").decode(enc, errors="replace"))


# Gemini 1.5 Flash: native multilingual STT (FR, MSA, Darija),
# $0.075 / 1M input tokens (audio = 32 tokens/s → ~$0.009 / hour of audio).
# gemini-2.5-flash supports audio input. gemini-1.5-flash and gemini-2.0-flash
# have been retired for newly created API keys (return 404).
# Override with env var GEMINI_STT_MODEL if needed.
import os as _os
_GEMINI_STT_MODEL = _os.environ.get("GEMINI_STT_MODEL", "gemini-2.5-flash")
_GEMINI_STT_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent?key={key}"
)


def _mime_for(audio_bytes: bytes) -> str:
    """Guess audio MIME type from magic bytes (covers what MediaRecorder emits)."""
    if len(audio_bytes) < 16:
        return "audio/webm"
    head = audio_bytes[:16]
    # WebM / Matroska
    if head[:4] == b"\x1a\x45\xdf\xa3":
        return "audio/webm"
    # OGG
    if head[:4] == b"OggS":
        return "audio/ogg"
    # WAV (RIFF…WAVE)
    if head[:4] == b"RIFF" and head[8:12] == b"WAVE":
        return "audio/wav"
    # MP3 (ID3 tag or 0xFFFB frame)
    if head[:3] == b"ID3" or (head[0] == 0xFF and (head[1] & 0xE0) == 0xE0):
        return "audio/mpeg"
    # MP4 / M4A
    if head[4:8] == b"ftyp":
        return "audio/mp4"
    return "audio/webm"


def _prompt_for(language: str) -> str:
    """Transcription prompt tuned by session language."""
    if language in ("mixed", "darija"):
        return (
            "Transcris cet audio en darija marocaine. "
            "Écris les mots en darija en ALPHABET ARABE uniquement. "
            "Garde les termes techniques/scientifiques en FRANÇAIS (la vitesse, "
            "la force, la dérivée, etc.). Ne traduis rien. "
            "Réponds UNIQUEMENT avec la transcription, sans préfixe ni commentaire."
        )
    if language == "ar":
        return (
            "Transcris cet audio en arabe standard moderne (MSA). "
            "Utilise les termes scientifiques officiels. "
            "Réponds UNIQUEMENT avec la transcription."
        )
    # fr / unknown
    return (
        "Transcris cet audio en français. Ponctue correctement. "
        "Réponds UNIQUEMENT avec la transcription, sans préfixe ni commentaire."
    )


class STTService:
    async def transcribe_audio(
        self,
        audio_content: bytes,
        language: str = "fr",
    ) -> Optional[str]:
        """Transcribe audio bytes via Gemini. Returns text or None."""
        if not audio_content:
            return None

        key = settings.gemini_tts_api_key or settings.gemini_api_key
        if not key:
            _safe_log("[STT] No Gemini API key configured")
            return None

        mime = _mime_for(audio_content)
        audio_b64 = base64.b64encode(audio_content).decode("ascii")
        prompt = _prompt_for(language)

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inlineData": {"mimeType": mime, "data": audio_b64}},
                ]
            }],
            "generationConfig": {
                "temperature": 0.0,
                "maxOutputTokens": 1024,
            },
        }

        url = _GEMINI_STT_URL.format(model=_GEMINI_STT_MODEL, key=key)
        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                resp = await client.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
            if resp.status_code != 200:
                _safe_log(f"[STT][Gemini] HTTP {resp.status_code}: {resp.text[:300]}")
                return None
            data = resp.json()
            candidates = data.get("candidates") or []
            if not candidates:
                _safe_log(f"[STT][Gemini] No candidates: {str(data)[:300]}")
                return None
            cand = candidates[0]
            finish_reason = cand.get("finishReason", "?")
            parts = cand.get("content", {}).get("parts", [])
            text_chunks = [p.get("text", "") for p in parts if p.get("text")]
            transcript = "".join(text_chunks).strip()
            for prefix in ("Transcription :", "Transcription:", "Texte :", "Texte:"):
                if transcript.startswith(prefix):
                    transcript = transcript[len(prefix):].strip()
            _safe_log(
                f"[STT] Gemini lang={language} mime={mime} "
                f"bytes={len(audio_content)} chars={len(transcript)} "
                f"finish={finish_reason}"
            )
            if not transcript:
                _safe_log(f"[STT][Gemini] Empty body: {str(data)[:500]}")
            return transcript or None
        except httpx.TimeoutException:
            _safe_log("[STT][Gemini] Timeout after 45s")
            return None
        except Exception as e:
            _safe_log(f"[STT][Gemini] Exception: {e}")
            return None


stt_service = STTService()
