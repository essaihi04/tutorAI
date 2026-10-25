"""Voix du prof sur Kaggle à la demande : cycle de vie, annonces, budget."""
import asyncio
import json
import time

import pytest

from app.config import get_settings
from app.services import kaggle_tts
from app.services.kaggle_tts import PiloteKaggle, construire_kernel

settings = get_settings()


@pytest.fixture
def actif(monkeypatch):
    monkeypatch.setattr(settings, "kaggle_tts_actif", 1)
    monkeypatch.setattr(settings, "kaggle_username", "prof")
    monkeypatch.setattr(settings, "kaggle_api_token", "jeton-kaggle")
    monkeypatch.setattr(settings, "kaggle_tts_socle", "")
    pousses = []
    monkeypatch.setattr(kaggle_tts, "pousser_kernel", lambda cle, lancement, jeton: pousses.append((cle, lancement)))

    async def sante_ok(url, jeton):
        return True
    monkeypatch.setattr(kaggle_tts, "_sante", sante_ok)
    return pousses


def _pilote(tmp_path):
    return PiloteKaggle(tmp_path / "etat.json")


def _reveiller(p):
    async def go():
        p.besoin_de_voix("ouverture de séance")
        await p._tache
    asyncio.run(go())


def test_inactif_sans_identifiants(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "kaggle_tts_actif", 1)
    monkeypatch.setattr(settings, "kaggle_api_token", "")
    p = _pilote(tmp_path)
    p.besoin_de_voix()
    assert p.etat == "eteint" and p.cible() is None


def test_reveil_puis_annonce_pret(tmp_path, actif):
    p = _pilote(tmp_path)
    _reveiller(p)
    assert p.etat == "demarrage" and len(actif) == 1
    # Un second besoin pendant le démarrage ne relance pas un deuxième kernel.
    asyncio.run(asyncio.sleep(0)) or p.besoin_de_voix()
    assert len(actif) == 1
    ok = asyncio.run(p.recevoir_annonce({"etat": "pret", "cle": p.cle, "lancement": p.lancement,
                                         "url": "https://abc.trycloudflare.com/", "jeton": "j"}))
    assert ok and p.cible() == ("https://abc.trycloudflare.com", "j")
    # L'état survit à un redémarrage du backend.
    assert _pilote(tmp_path).cible() == ("https://abc.trycloudflare.com", "j")


def test_annonce_avec_mauvaise_cle_refusee(tmp_path, actif):
    p = _pilote(tmp_path)
    _reveiller(p)
    for faux in ({"cle": "x", "lancement": p.lancement}, {"cle": p.cle, "lancement": "ancien"}):
        assert not asyncio.run(p.recevoir_annonce({"etat": "pret", "url": "https://h.trycloudflare.com",
                                                   "jeton": "j", **faux}))
    assert p.cible() is None


def test_extinction_annoncee_ferme_la_session(tmp_path, actif):
    p = _pilote(tmp_path)
    _reveiller(p)
    asyncio.run(p.recevoir_annonce({"etat": "pret", "cle": p.cle, "lancement": p.lancement,
                                    "url": "https://h.trycloudflare.com", "jeton": "j"}))
    asyncio.run(p.recevoir_annonce({"etat": "eteint", "cle": p.cle, "lancement": p.lancement, "raison": "veille"}))
    assert p.etat == "eteint" and p.cible() is None
    assert p.sessions[-1][1] > 0


def test_silence_au_dela_de_la_veille(tmp_path, actif):
    p = _pilote(tmp_path)
    _reveiller(p)
    asyncio.run(p.recevoir_annonce({"etat": "pret", "cle": p.cle, "lancement": p.lancement,
                                    "url": "https://h.trycloudflare.com", "jeton": "j"}))
    p.derniere_parole = p.depuis = time.time() - settings.kaggle_tts_veille_s - 120
    assert p.cible() is None and p.etat == "eteint"


def test_demarrage_sans_annonce_tenu_pour_rate(tmp_path, actif):
    p = _pilote(tmp_path)
    _reveiller(p)
    p.depuis = time.time() - settings.kaggle_tts_demarrage_max_s - 1
    assert p.cible() is None and p.etat == "eteint"
    # Pas de relance immédiate après un échec : le quota ne fond pas en boucle.
    p.besoin_de_voix()
    assert len(actif) == 1


def test_tunnel_injoignable(tmp_path, actif):
    p = _pilote(tmp_path)
    _reveiller(p)
    asyncio.run(p.recevoir_annonce({"etat": "pret", "cle": p.cle, "lancement": p.lancement,
                                    "url": "https://h.trycloudflare.com", "jeton": "j"}))
    p.signaler_injoignable("https://autre.trycloudflare.com")
    assert p.etat == "pret"
    p.signaler_injoignable("https://h.trycloudflare.com/")
    assert p.etat == "eteint"


def test_budget_hebdo(tmp_path, actif, monkeypatch):
    monkeypatch.setattr(settings, "kaggle_tts_budget_h_semaine", 2.0)
    p = _pilote(tmp_path)
    now = time.time()
    p.sessions = [[now - 3 * 3600, now - 0.5 * 3600], [now - 9 * 86400, now - 8 * 86400]]
    assert p.heures_semaine(now) == pytest.approx(2.5, abs=0.01)
    p.besoin_de_voix()
    assert p.etat == "eteint" and not actif


def test_kernel_construit(tmp_path, actif):
    construire_kernel(tmp_path, "CLE'\"", "l1", "jeton")
    meta = json.loads((tmp_path / "kernel-metadata.json").read_text(encoding="utf-8"))
    assert meta["id"] == "prof/academy-tts-direct" and meta["is_private"] and meta["enable_gpu"]
    assert meta["kernel_sources"] == ["prof/academy-entrainement-v3"]
    source = (tmp_path / "serveur.py").read_text(encoding="utf-8")
    assert "__CONF__" not in source and "__REF_B64__" not in source
    compile(source, "serveur.py", "exec")
    ns = {}
    exec(source.split("\nT0 = ")[0], ns)   # en-tête seulement : CONF et la référence décodables
    assert ns["CONF"]["cle"] == "CLE'\"" and ns["CONF"]["veille_s"] == settings.kaggle_tts_veille_s
    import base64
    assert base64.b64decode(ns["REF_B64"])[:4] == b"fLaC"


def test_tts_service_suit_le_kernel(tmp_path, actif, monkeypatch):
    from app.services import tts_service
    p = _pilote(tmp_path)
    monkeypatch.setattr(kaggle_tts, "pilote", p)
    monkeypatch.setattr(settings, "academy_tts_url", "")
    assert tts_service._academy_cible() == ("", settings.academy_tts_token)
    _reveiller(p)
    asyncio.run(p.recevoir_annonce({"etat": "pret", "cle": p.cle, "lancement": p.lancement,
                                    "url": "https://h.trycloudflare.com", "jeton": "j"}))
    assert tts_service._academy_cible() == ("https://h.trycloudflare.com", "j")
    assert "kaggle-v3-amine" in tts_service._reglages_signature("academy")


def test_attente_courte_si_presque_pret(tmp_path, actif, monkeypatch):
    p = _pilote(tmp_path)
    _reveiller(p)
    # Démarrage récent : pas d'attente.
    t = time.time()
    asyncio.run(p.attendre_si_presque_pret(max_s=5))
    assert time.time() - t < 0.5
    # Presque prêt : on attend l'annonce.
    p.depuis = time.time() - 120

    async def scenario():
        async def annonce():
            await asyncio.sleep(1.2)
            await p.recevoir_annonce({"etat": "pret", "cle": p.cle, "lancement": p.lancement,
                                      "url": "https://h.trycloudflare.com", "jeton": "j"})
        asyncio.create_task(annonce())
        await p.attendre_si_presque_pret(max_s=10)
    asyncio.run(scenario())
    assert p.cible() == ("https://h.trycloudflare.com", "j")


def test_replique_muette_rattrapee(tmp_path, actif, monkeypatch):
    from app.websockets import session_handler as sh_mod
    p = _pilote(tmp_path)
    monkeypatch.setattr(kaggle_tts, "pilote", p)
    _reveiller(p)
    dites = []

    class H:
        _RATTRAPAGE_MAX_S = 30
        _rattraper_replique_muette = sh_mod.SessionHandler._rattraper_replique_muette

        async def generate_and_send_audio_chunks(self, texte):
            dites.append(texte)

    h = H()
    h._repliques_dites = 1

    async def scenario():
        h._rattraper_replique_muette("Bonjour, on commence.", 1)
        await asyncio.sleep(0.2)
        await p.recevoir_annonce({"etat": "pret", "cle": p.cle, "lancement": p.lancement,
                                  "url": "https://h.trycloudflare.com", "jeton": "j"})
        await asyncio.sleep(1.5)
    asyncio.run(scenario())
    assert dites == ["Bonjour, on commence."]
