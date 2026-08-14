"""
TTS à la demande — utilisé par le tableau en direct (« Mode Prof en Direct »).

Le tableau écrit ligne par ligne et doit entendre CHAQUE ligne au moment où il
l'écrit. Il ne peut donc pas se contenter du flux audio de la réponse globale :
il demande ici la synthèse d'un fragment précis, puis la joue en synchronisant
l'écriture sur la lecture.

La voix est TOUJOURS celle de nos modèles serveur (Academy en tête) — jamais la
synthèse du navigateur, qui ne sait pas dire la darija.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.services.tts_service import synthesize

router = APIRouter(prefix="/tts", tags=["tts"])


class SpeakRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    # 'fr' | 'ar' | 'mixed' (darija) — même vocabulaire que la session.
    # Darija par défaut : c'est la langue d'enseignement.
    language: str = "mixed"


@router.post("/speak")
async def speak(payload: SpeakRequest):
    """Synthétise un fragment et renvoie l'audio brut (WAV ou MP3).

    Le cache disque du service évite de refaire générer une phrase déjà dite —
    ce qui compte beaucoup ici : un cours rejoué ne recalcule rien.
    """
    lang = payload.language if payload.language in ("fr", "ar", "mixed") else "mixed"
    result = await synthesize(payload.text, lang)

    if not result.audio_b64:
        # 503 : le tableau retombe alors sur une écriture minutée, sans voix.
        raise HTTPException(
            status_code=503,
            detail=f"Synthèse vocale indisponible (provider={result.provider})",
        )

    import base64

    return Response(
        content=base64.b64decode(result.audio_b64),
        media_type=result.mime or "audio/wav",
        headers={
            "X-TTS-Provider": result.provider,
            "X-TTS-Cached": "1" if result.cached else "0",
            # Le navigateur peut garder le fragment : même texte = même audio.
            "Cache-Control": "public, max-age=86400",
        },
    )
