"""MoulSot dans le kernel de la voix, Gemini en secours (stt_service._transcrire_kaggle)."""
import asyncio

import httpx

from app.services import stt_service as stt


class _Pilote:
    def __init__(self, cible):
        self._cible, self.reveils = cible, []

    def cible(self):
        return self._cible

    def besoin_de_voix(self, raison="parole"):
        self.reveils.append(raison)


def _brancher(monkeypatch, cible, reponse=None, exc=None):
    import app.services.kaggle_tts as kt
    p = _Pilote(cible)
    monkeypatch.setattr(kt, "pilote", p)
    monkeypatch.setattr(stt.settings, "kaggle_stt_modele", "atlasia/moulsot.v0.3")

    def gerer(req):
        if exc:
            raise exc
        assert req.headers["Authorization"] == "Bearer j" and req.url.params["langue"] == "mixed"
        return reponse
    vrai = httpx.AsyncClient
    monkeypatch.setattr(stt.httpx, "AsyncClient", lambda **kw: vrai(transport=httpx.MockTransport(gerer)))
    return p


def test_desactive_par_defaut(monkeypatch):
    monkeypatch.setattr(stt.settings, "kaggle_stt_modele", "")
    assert asyncio.run(stt._transcrire_kaggle(b"x" * 100, "mixed")) is None


def test_kernel_endormi_reveille_et_rend_la_main(monkeypatch):
    p = _brancher(monkeypatch, None)
    assert asyncio.run(stt._transcrire_kaggle(b"x" * 100, "mixed")) is None
    assert p.reveils == ["stt"]


def test_kernel_pret_transcrit(monkeypatch):
    _brancher(monkeypatch, ("https://k", "j"),
              httpx.Response(200, json={"texte": " شنو هي la vitesse ", "duree_s": 2.1, "calcul_ms": 310}))
    assert asyncio.run(stt._transcrire_kaggle(b"x" * 100, "mixed")) == "شنو هي la vitesse"


def test_stt_pas_pret_ou_panne_gemini_en_secours(monkeypatch):
    _brancher(monkeypatch, ("https://k", "j"), httpx.Response(503, json={"detail": "stt preparation"}))
    assert asyncio.run(stt._transcrire_kaggle(b"x" * 100, "mixed")) is None
    _brancher(monkeypatch, ("https://k", "j"), exc=httpx.ConnectTimeout("lent"))
    assert asyncio.run(stt._transcrire_kaggle(b"x" * 100, "mixed")) is None
