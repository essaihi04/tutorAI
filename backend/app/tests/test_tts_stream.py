"""Découpage du flux PCM d'Academy.

Le serveur envoie un en-tête WAV puis du PCM 16 bits, en blocs dont les
frontières ne tombent NI sur la fin de l'en-tête NI sur une frontière
d'échantillon. Se tromper d'un octet décale tout le reste du flux et le
transforme en bruit blanc — d'où ces cas volontairement hostiles.
"""
import asyncio
import json
import struct
import time

import httpx
import pytest

from app.services import tts_service as tts


SR = 24000


def _entete(sr: int = SR) -> bytes:
    maxi = 0xFFFFFFFF
    return (
        b"RIFF" + struct.pack("<I", maxi - 8) + b"WAVEfmt "
        + struct.pack("<IHHIIHH", 16, 1, 1, sr, sr * 2, 2, 16)
        + b"data" + struct.pack("<I", maxi - 44)
    )


def _pcm(n_echantillons: int) -> bytes:
    return b"".join(struct.pack("<h", (i % 1000) - 500) for i in range(n_echantillons))


def _client_factice(monkeypatch, blocs, *, statut=200, ctype="audio/wav"):
    """Remplace httpx.AsyncClient pour servir `blocs` en flux."""

    async def flux():
        for b in blocs:
            yield b

    def handler(request):
        return httpx.Response(statut, headers={"Content-Type": ctype}, content=flux())

    transport = httpx.MockTransport(handler)
    vrai = httpx.AsyncClient

    def fabrique(*a, **kw):
        kw.pop("timeout", None)
        return vrai(transport=transport, timeout=5.0)

    monkeypatch.setattr(tts.httpx, "AsyncClient", fabrique)


@pytest.fixture(autouse=True)
def _academy_actif(monkeypatch):
    monkeypatch.setattr(tts.settings, "academy_tts_url", "https://exemple.test")
    monkeypatch.setattr(tts, "_ACADEMY_COOLDOWN_UNTIL", 0.0)


async def _collecter(texte="salam"):
    sr_vu, morceaux = None, []
    async for sr, pcm in tts.stream_academy_pcm(texte, "mixed"):
        sr_vu = sr
        morceaux.append(pcm)
    return sr_vu, morceaux


def test_entete_coupe_en_deux_et_pcm_reconstruit(monkeypatch):
    """L'en-tête peut arriver en plusieurs morceaux : il n'est jamais joué."""
    entete, pcm = _entete(), _pcm(8000)
    _client_factice(monkeypatch, [entete[:20], entete[20:] + pcm[:100], pcm[100:]])

    sr, morceaux = asyncio.run(_collecter())

    assert sr == SR
    assert b"".join(morceaux) == pcm, "le PCM rendu doit être exactement celui émis"
    assert not b"".join(morceaux).startswith(b"RIFF")


def test_echantillon_coupe_entre_deux_blocs(monkeypatch):
    """Un bloc de longueur impaire ne doit pas décaler le flux d'un octet."""
    entete, pcm = _entete(), _pcm(4000)
    # Coupures volontairement impaires : 1er bloc = en-tête + 101 octets.
    _client_factice(monkeypatch, [entete + pcm[:101], pcm[101:2003], pcm[2003:]])

    _, morceaux = asyncio.run(_collecter())

    assert b"".join(morceaux) == pcm
    assert all(len(m) % 2 == 0 for m in morceaux), "aucun bloc ne coupe un échantillon"


def test_premier_bloc_part_avant_la_fin_du_flux(monkeypatch):
    """C'est tout l'intérêt : ne pas attendre la fin de la synthèse."""
    entete, pcm = _entete(), _pcm(40000)
    _client_factice(monkeypatch, [entete + pcm[:2000]] + [pcm[2000:]])

    _, morceaux = asyncio.run(_collecter())

    assert len(morceaux) >= 2, "le flux doit être rendu progressivement"
    assert len(morceaux[0]) == 2000, "le premier bloc part sans être agrégé"


def test_sample_rate_lu_dans_l_entete(monkeypatch):
    """On ne présume pas 24 kHz : un autre checkpoint peut changer le débit."""
    _client_factice(monkeypatch, [_entete(16000) + _pcm(100)])

    sr, _ = asyncio.run(_collecter())

    assert sr == 16000


def test_erreur_http_ne_rend_aucun_bloc(monkeypatch):
    """Rien ne sort : l'appelant doit pouvoir se rabattre sur /tts."""
    _client_factice(monkeypatch, [b""], statut=503, ctype="application/json")

    _, morceaux = asyncio.run(_collecter())

    assert morceaux == []


def test_reponse_non_audio_ignoree(monkeypatch):
    """La page d'avertissement ngrok ne doit jamais être jouée comme du son."""
    _client_factice(monkeypatch, [b"<!DOCTYPE html>"], ctype="text/html")

    _, morceaux = asyncio.run(_collecter())

    assert morceaux == []


def test_flux_envoie_la_copie_prononcable_a_academy(monkeypatch):
    """Le flux rapide ne doit pas contourner le normaliseur de parole."""
    entete, pcm = _entete(), _pcm(100)
    payloads = []

    async def flux():
        yield entete + pcm

    def handler(request):
        payloads.append(json.loads(request.content.decode("utf-8")))
        return httpx.Response(
            200,
            headers={"Content-Type": "audio/wav"},
            content=flux(),
        )

    transport = httpx.MockTransport(handler)
    vrai = httpx.AsyncClient
    monkeypatch.setattr(
        tts.httpx,
        "AsyncClient",
        lambda *a, **kw: vrai(transport=transport, timeout=5.0),
    )

    asyncio.run(_collecter("La relation est N = 1/T et vaut 25% en 4 Hz."))

    assert payloads
    texte = payloads[0]["texte"]
    assert "la fréquence est égale à un sur la période" in texte
    assert "vingt-cinq pour cent" in texte
    assert "quatre Hertz" not in texte


def test_abandon_si_le_premier_son_tarde_trop(monkeypatch):
    """File engorgée : on renonce vite au lieu d'attendre des minutes.

    Le serveur envoie son en-tête WAV tout de suite puis se tait tant que le
    GPU n'est pas libre — un timeout de lecture classique ne se déclencherait
    donc jamais. Mesuré une fois à 194 s d'attente réelle.
    """
    import asyncio as _aio

    async def flux_qui_se_tait():
        yield _entete()
        await _aio.sleep(30)        # le GPU ne se libère jamais
        yield _pcm(100)

    def handler(request):
        return httpx.Response(200, headers={"Content-Type": "audio/wav"},
                              content=flux_qui_se_tait())

    transport = httpx.MockTransport(handler)
    vrai = httpx.AsyncClient
    monkeypatch.setattr(
        tts.httpx, "AsyncClient",
        lambda *a, **kw: vrai(transport=transport, timeout=60.0),
    )
    monkeypatch.setattr(tts, "_PREMIER_SON_MAX_S", 0.3)

    debut = time.time()
    _, morceaux = asyncio.run(_collecter())

    assert morceaux == [], "aucun son : l'appelant doit pouvoir se rabattre"
    assert time.time() - debut < 5, "on ne doit pas attendre la fin du silence"
