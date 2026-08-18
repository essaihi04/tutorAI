"""Numérotation de la file de morceaux audio envoyée au navigateur.

Le lecteur du navigateur joue les morceaux DANS L'ORDRE : il attend le morceau
n avant de jouer le n+1. Or la synthèse peut échouer sur un segment isolé, et
`stream_synthesize_segments` saute alors ce segment en conservant les indices
d'origine. La file arrivait donc trouée, avec deux symptômes entendus en
séance :

  • segment 0 en échec → le morceau d'indice 0 n'arrivait jamais, la lecture ne
    démarrait pas du tout et le tour entier restait muet ;
  • segment du milieu en échec → la voix s'arrêtait là et le navigateur
    patientait quatre-vingt-dix secondes pour un morceau inexistant.

D'où ces deux garanties : les indices envoyés sont CONTIGUS, et la file est
toujours refermée par `audio_chunks_end` portant le compte réel.
"""
import asyncio

import pytest

from app.services.tts_service import TTSSegment
from app.websockets import session_handler as mod
from app.websockets.session_handler import SessionHandler


class FauxWebSocket:
    """On ne teste pas le transport : on regarde ce qui part."""

    def __init__(self):
        self.envoyes: list[dict] = []

    async def send_json(self, message: dict):
        self.envoyes.append(message)


def _segment(texte: str) -> TTSSegment:
    return TTSSegment(
        audio_b64="AAAA",
        mime="audio/wav",
        provider="academy",
        language="fr",
        cached=False,
        text=texte,
    )


@pytest.fixture
def handler(monkeypatch):
    """Handler réduit à ce que ces tests exercent, sans transport ni réseau.

    Le chemin PCM continu est court-circuité : ces tests portent sur le repli
    par segments, seul chemin qui numérote des morceaux.
    """
    async def pas_de_flux_pcm(self, ai_response, lang):
        return False

    monkeypatch.setattr(SessionHandler, "_send_audio_stream", pas_de_flux_pcm)

    h = SessionHandler.__new__(SessionHandler)
    h.websocket = FauxWebSocket()
    h.language = "fr"
    return h


def _jouer(handler, monkeypatch, rendus):
    """Fait tourner l'envoi avec `rendus` = (indice_segment, total, segment).

    C'est dans cette liste qu'on simule les trous laissés par un segment dont
    la synthèse a échoué.
    """
    async def faux_flux(text, language="fr"):
        for rendu in rendus:
            yield rendu

    monkeypatch.setattr(mod.tts_service, "stream_synthesize_segments", faux_flux)
    asyncio.run(handler.generate_and_send_audio_chunks("peu importe"))


def _indices(handler) -> list[int]:
    return [
        m["chunk_index"]
        for m in handler.websocket.envoyes
        if m["type"] == "audio_chunk"
    ]


def _fin(handler) -> dict | None:
    fins = [m for m in handler.websocket.envoyes if m["type"] == "audio_chunks_end"]
    return fins[-1] if fins else None


def test_indices_contigus_quand_le_premier_segment_echoue(handler, monkeypatch):
    """Le tour restait MUET : la lecture n'attendait que l'indice 0."""
    _jouer(handler, monkeypatch, [
        (1, 3, _segment("deuxieme phrase")),
        (2, 3, _segment("troisieme phrase")),
    ])

    assert _indices(handler) == [0, 1]
    assert _fin(handler) == {"type": "audio_chunks_end", "total_chunks": 2}


def test_indices_contigus_quand_un_segment_du_milieu_echoue(handler, monkeypatch):
    """La voix s'arrêtait au trou, puis le navigateur attendait 90 s."""
    _jouer(handler, monkeypatch, [
        (0, 3, _segment("premiere phrase")),
        (2, 3, _segment("troisieme phrase")),
    ])

    assert _indices(handler) == [0, 1]
    assert _fin(handler)["total_chunks"] == 2


def test_file_refermee_meme_sans_aucun_morceau(handler, monkeypatch):
    """Sans ce message, le lecteur reste suspendu sur une file vide."""
    _jouer(handler, monkeypatch, [])

    assert _indices(handler) == []
    assert _fin(handler) == {"type": "audio_chunks_end", "total_chunks": 0}
