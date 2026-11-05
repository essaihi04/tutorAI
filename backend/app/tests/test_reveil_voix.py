"""Réveil anticipé de la voix du prof depuis les pages du site."""
import asyncio

from app.api.v1.endpoints import kaggle_tts as ep


class FauxPilote:
    def __init__(self, cible=None):
        self.raisons, self._cible, self.etat = [], cible, "eteint"

    def besoin_de_voix(self, raison="parole"):
        self.raisons.append(raison)

    def cible(self):
        return self._cible


def test_reveil_allume_sans_compter_comme_parole(monkeypatch):
    p = FauxPilote()
    monkeypatch.setattr(ep, "pilote", p)
    assert asyncio.run(ep.reveil()) == {"etat": "eteint"}
    assert p.raisons == ["page"]          # « parole » repousserait la veille


def test_reveil_garde_eveille_un_kernel_pret(monkeypatch):
    p, gardes = FauxPilote(("https://x.trycloudflare.com", "j")), []

    async def garder(url, jeton):
        gardes.append(url)

    monkeypatch.setattr(ep, "pilote", p)
    monkeypatch.setattr(ep, "_garder", garder)

    async def tour():
        await ep.reveil()
        await asyncio.sleep(0)

    asyncio.run(tour())
    assert gardes == ["https://x.trycloudflare.com"]
