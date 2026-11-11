"""Voix du prof sur Kaggle à la demande : cycle de vie, annonces, budget."""
import asyncio
import json
import time
from pathlib import Path

import pytest

from app.config import get_settings
from app.services import kaggle_tts
from app.services.kaggle_tts import PiloteKaggle, construire_kernel
from app.services.kaggle_tts import kaggle_cli as kaggle_cli_reel

settings = get_settings()


@pytest.fixture
def actif(monkeypatch):
    monkeypatch.setattr(settings, "kaggle_tts_actif", 1)
    monkeypatch.setattr(settings, "kaggle_username", "prof")
    monkeypatch.setattr(settings, "kaggle_api_token", "jeton-kaggle")
    monkeypatch.setattr(settings, "kaggle_tts_socle", "")
    monkeypatch.setattr(kaggle_tts, "_env_fichier", lambda: {})     # pas de comptes de secours venus de backend/.env
    for n in range(2, 11):
        monkeypatch.delenv(f"KAGGLE{n}_USERNAME", raising=False)
        monkeypatch.delenv(f"KAGGLE{n}_API_TOKEN", raising=False)
    pousses = []
    monkeypatch.setattr(kaggle_tts, "pousser_kernel", lambda cle, lancement, jeton, **k: pousses.append(
        (cle, lancement, getattr(k.get("compte"), "nom", None))))

    async def sante_ok(url, jeton):
        return True
    monkeypatch.setattr(kaggle_tts, "_sante", sante_ok)
    monkeypatch.setattr(kaggle_tts, "kaggle_cli", lambda *a, **k: 'has status "KernelWorkerStatus.COMPLETE"')
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


@pytest.fixture
def dossier_kernel(tmp_path, monkeypatch):
    """La voix de référence n'existe que sur le serveur : en local, on la remplace par un faux FLAC."""
    if (kaggle_tts.DOSSIER_KERNEL / settings.kaggle_tts_reference).exists():
        return
    import shutil
    d = tmp_path / "kernel_src"
    d.mkdir()
    for nom in ("serveur.py", "texte_parle.py"):
        shutil.copy(kaggle_tts.DOSSIER_KERNEL / nom, d / nom)
    (d / settings.kaggle_tts_reference).write_bytes(b"fLaC" + bytes(64))
    monkeypatch.setattr(kaggle_tts, "DOSSIER_KERNEL", d)


def test_kernel_construit(tmp_path, actif, dossier_kernel):
    construire_kernel(tmp_path, "CLE'\"", "l1", "jeton")
    meta = json.loads((tmp_path / "kernel-metadata.json").read_text(encoding="utf-8"))
    assert meta["id"] == "prof/academy-tts-direct" and meta["is_private"] and meta["enable_gpu"]
    assert meta["kernel_sources"] == ["prof/academy-v5-bodi", "prof/academy-moulsot-v4"]   # voix + MoulSot v4
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
    assert "kaggle-v5-bodi" in tts_service._reglages_signature("academy")


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


def test_kernel_cru_eteint_mais_vivant_est_repris(tmp_path, actif):
    """Après un redémarrage du backend, la veille estimée peut déclarer éteint
    un kernel qui tourne encore : on le reprend au lieu d'en pousser un autre."""
    p = _pilote(tmp_path)
    _reveiller(p)
    asyncio.run(p.recevoir_annonce({"etat": "pret", "cle": p.cle, "lancement": p.lancement,
                                    "url": "https://h.trycloudflare.com", "jeton": "j"}))
    cle = p.cle
    p.derniere_parole = p.depuis = time.time() - 3600       # « silence » d'une heure
    assert p.cible() is None and p.etat == "eteint"
    p.dernier_echec = 0
    _reveiller(p)
    assert p.etat == "pret" and len(actif) == 1 and p.cle == cle


def test_session_kaggle_encore_en_cours(tmp_path, actif, monkeypatch):
    monkeypatch.setattr(kaggle_tts, "kaggle_cli", lambda *a, **k: 'has status "KernelWorkerStatus.RUNNING"')
    p = _pilote(tmp_path)
    _reveiller(p)
    assert p.etat == "eteint" and not actif


def test_un_morceau_qui_murmure_est_refait():
    """La voix qui décroche (son faible, ni parole ni silence, >= 0,9 s) est repérée ; la parole et les silences non."""
    import re
    import numpy as np
    source = (Path(__file__).resolve().parents[2] / "kaggle_tts" / "serveur.py").read_text(encoding="utf-8")
    module = re.search(r"MODULE_TRAVAILLEUR = r'''(.*?)\n'''", source, re.S).group(1)
    assert "if murmure(w, m.sr):" in module
    ns = {}
    exec(module.split("\ndef murmure")[1].join(["def murmure", ""]).split("\ndef travailleur")[0], ns)
    sr = 24000
    t = np.arange(int(1.5 * sr)) / sr
    parole = 0.3 * np.sin(2 * np.pi * 180 * t)
    silence = np.zeros(sr)
    marmonne = 0.01 * np.sin(2 * np.pi * 120 * t)              # ~ -43 dB pendant 1,5 s
    assert ns["murmure"](np.concatenate([parole, silence, parole]), sr) == 0
    assert ns["murmure"](np.concatenate([parole, marmonne, parole]), sr) >= 1.4


# ── Plusieurs comptes Kaggle (11 novembre 2026) ──

@pytest.fixture
def comptes(actif, monkeypatch):
    """Principal « prof » + deux comptes de secours."""
    monkeypatch.setenv("KAGGLE2_USERNAME", "secours1")
    monkeypatch.setenv("KAGGLE2_API_TOKEN", "t2")
    monkeypatch.setenv("KAGGLE3_USERNAME", "secours2")
    monkeypatch.setenv("KAGGLE3_API_TOKEN", "t3")
    return actif


def _noms(pousses):
    return [n for _, _, n in pousses]


async def _laisser_finir(p):
    """Laisse finir les lancements, et la bascule qui suit un échec."""
    for _ in range(10):
        await asyncio.sleep(0)
        t = p._tache
        if t and not t.done():
            await t


def _besoin(p, raison="parole"):
    async def go():
        p.besoin_de_voix(raison)
        await _laisser_finir(p)
    asyncio.run(go())


def _compte(p, nom):
    return next(c for c in p.comptes() if c.nom == nom)


def _pret(p, nom):
    c = _compte(p, nom)
    url = f"https://{nom}.trycloudflare.com"
    assert asyncio.run(p.recevoir_annonce({"etat": "pret", "cle": c.cle, "lancement": c.lancement,
                                           "url": url, "jeton": "j-" + nom}))
    return url


def test_un_seul_compte_comme_avant(tmp_path, actif):
    p = _pilote(tmp_path)
    assert [c.nom for c in p.comptes()] == ["prof"]
    _besoin(p)
    _pret(p, "prof")
    r = p.resume()
    assert r["etat"] == "pret" and [c["nom"] for c in r["comptes"]] == ["prof"] and r["comptes"][0]["sert"]
    assert _noms(actif) == ["prof"]


def test_comptes_lus_dans_l_environnement(actif, monkeypatch):
    monkeypatch.setenv("KAGGLE3_USERNAME", "trois")      # un numéro manquant n'arrête pas la lecture
    monkeypatch.setenv("KAGGLE3_API_TOKEN", "t3")
    monkeypatch.setenv("KAGGLE4_USERNAME", "sans-jeton")
    monkeypatch.setenv("KAGGLE5_USERNAME", "prof")       # doublon du principal : ignoré
    monkeypatch.setenv("KAGGLE5_API_TOKEN", "x")
    assert kaggle_tts.comptes_configures() == [("prof", "jeton-kaggle"), ("trois", "t3")]


def test_principal_garde_la_priorite(tmp_path, comptes):
    p = _pilote(tmp_path)
    _besoin(p)
    assert _noms(comptes) == ["prof"]                    # un seul réveil, le principal
    _besoin(p)
    assert _noms(comptes) == ["prof"]                    # il démarre : on attend, pas de 2e réveil
    url = _pret(p, "prof")
    _besoin(p)
    assert p.cible() == (url, "j-prof") and _noms(comptes) == ["prof"]


def test_saturation_reveille_le_secours_puis_bascule(tmp_path, comptes, monkeypatch):
    monkeypatch.setattr(settings, "kaggle_tts_attente_max", 3)
    p = _pilote(tmp_path)
    _besoin(p)
    url_prof = _pret(p, "prof")
    principal = _compte(p, "prof")
    principal.porte.attente = 2                          # presque saturé : réveil à l'avance
    _besoin(p)
    assert _noms(comptes) == ["prof", "secours1"]
    assert p.cible() == (url_prof, "j-prof")            # le principal parle encore
    _besoin(p)
    assert len(comptes) == 2                             # le secours démarre : pas d'autre réveil
    url_s1 = _pret(p, "secours1")
    principal.porte.attente = 3                          # saturé : la voix passe au secours
    assert p.cible() == (url_s1, "j-secours1")
    assert {c["nom"]: c["statut"] for c in p.resume()["comptes"]}["prof"] == "sature"
    principal.porte.attente = 0                          # plus de file : le principal reprend la main
    assert p.cible() == (url_prof, "j-prof")


def test_porte_par_kernel_dans_tts_service(tmp_path, comptes, monkeypatch):
    from app.services import tts_service
    p = _pilote(tmp_path)
    monkeypatch.setattr(kaggle_tts, "pilote", p)
    _besoin(p)
    url = _pret(p, "prof")
    assert tts_service._academy_sem(url) is _compte(p, "prof").porte

    async def deux_requetes():
        porte = tts_service._academy_sem(url)
        async with porte:
            assert porte.en_cours == 1 and _compte(p, "prof").charge() == 1
        assert porte.en_cours == 0
    asyncio.run(deux_requetes())


def test_503_bascule_sans_perdre_le_principal(tmp_path, comptes):
    p = _pilote(tmp_path)
    _besoin(p)
    url_prof = _pret(p, "prof")

    async def scenario():
        p.signaler_injoignable(url_prof)                 # 503 : saturé, mais /health répond encore
        await _laisser_finir(p)
    asyncio.run(scenario())
    assert _noms(comptes) == ["prof", "secours1"]
    principal = _compte(p, "prof")
    assert principal.etat == "pret" and p.cible() is None   # au repos ; le secours démarre
    principal.repos_jusqua = 0
    assert p.cible() == (url_prof, "j-prof")


def test_tunnel_mort_en_multi_comptes(tmp_path, comptes, monkeypatch):
    p = _pilote(tmp_path)
    _besoin(p)
    url_prof = _pret(p, "prof")

    async def muet(url, jeton):
        return False
    monkeypatch.setattr(kaggle_tts, "_sante", muet)

    async def scenario():
        p.signaler_injoignable(url_prof)
        await _laisser_finir(p)
    asyncio.run(scenario())
    assert _compte(p, "prof").etat == "eteint"
    assert _noms(comptes) == ["prof", "secours1"]


def test_quota_epuise_passe_au_suivant(tmp_path, comptes, monkeypatch):
    monkeypatch.setattr(settings, "kaggle_tts_budget_h_semaine", 2.0)
    p = _pilote(tmp_path)
    now = time.time()
    _compte(p, "prof").sessions = [[now - 3 * 3600, now - 0.5 * 3600]]
    _besoin(p)
    assert _noms(comptes) == ["secours1"]
    statuts = {c["nom"]: c["statut"] for c in p.resume()["comptes"]}
    assert statuts["prof"] == "quota" and statuts["secours1"] == "file_kaggle"


@pytest.mark.parametrize("message, statut", [
    ("Maximum batch GPU session count of 2 reached", "sessions_pleines"),
    ("You have exceeded your weekly GPU quota", "quota"),
    ("401 Unauthorized", "erreur"),
])
def test_push_refuse_passe_au_suivant(tmp_path, comptes, monkeypatch, message, statut):
    def pousser(cle, lancement, jeton, **k):
        if k["compte"].nom == "prof":
            raise RuntimeError(message)
        comptes.append((cle, lancement, k["compte"].nom))
    monkeypatch.setattr(kaggle_tts, "pousser_kernel", pousser)
    p = _pilote(tmp_path)
    _besoin(p)
    assert _noms(comptes) == ["secours1"]               # parti aussitôt, sans attendre la phrase suivante
    r = {c["nom"]: c for c in p.resume()["comptes"]}
    assert r["prof"]["statut"] == statut and message in r["prof"]["derniere_erreur"]
    _compte(p, "secours1").etat = "eteint"
    _compte(p, "secours1").dernier_echec = time.time()
    _besoin(p)
    assert _noms(comptes) == ["secours1", "secours2"]   # le principal en pause n'est pas relancé


def test_compte_en_erreur_au_demarrage(tmp_path, comptes):
    p = _pilote(tmp_path)
    _besoin(p)
    _compte(p, "prof").depuis = time.time() - settings.kaggle_tts_demarrage_max_s - 1
    _besoin(p)
    assert _noms(comptes) == ["prof", "secours1"]
    assert {c["nom"]: c["statut"] for c in p.resume()["comptes"]}["prof"] == "erreur"


def test_file_kaggle_trop_longue_un_seul_reveil_de_plus(tmp_path, comptes, monkeypatch):
    monkeypatch.setattr(settings, "kaggle_tts_file_kaggle_max_s", 180)
    p = _pilote(tmp_path)
    _besoin(p)
    _compte(p, "prof").depuis = time.time() - 200       # toujours dans la file de Kaggle
    _besoin(p)
    assert _noms(comptes) == ["prof", "secours1"]
    _compte(p, "secours1").depuis = time.time() - 200
    _besoin(p)
    assert _noms(comptes) == ["prof", "secours1"]       # jamais un troisième


def test_kernel_sorti_de_file_pas_de_reveil_en_plus(tmp_path, comptes):
    p = _pilote(tmp_path)
    _besoin(p)
    c = _compte(p, "prof")
    assert asyncio.run(p.recevoir_annonce({"etat": "demarrage", "cle": c.cle, "lancement": c.lancement}))
    c.depuis = time.time() - 200
    _besoin(p)
    assert _noms(comptes) == ["prof"]


def test_moins_charge_parmi_les_secours(tmp_path, comptes):
    p = _pilote(tmp_path)
    for nom in ("prof", "secours1", "secours2"):
        c = _compte(p, nom)
        c.cle, c.lancement = "cle-" + nom, "l-" + nom
        _pret(p, nom)
    _compte(p, "prof").repos_jusqua = time.time() + 60     # le principal vient de répondre 503
    _compte(p, "secours1").porte.en_cours = 2
    assert p.cible() == ("https://secours2.trycloudflare.com", "j-secours2")
    _compte(p, "secours1").porte.en_cours = 0
    _compte(p, "secours1").sessions = [[time.time() - 3600, 0]]
    _compte(p, "secours2").sessions = [[time.time() - 7200, 0]]
    assert p.cible() == ("https://secours1.trycloudflare.com", "j-secours1")   # à charge égale : moins d'heures


def test_annonce_d_un_compte_de_secours(tmp_path, comptes):
    p = _pilote(tmp_path)
    c1, c2 = _compte(p, "secours1"), _compte(p, "secours2")
    c1.cle, c1.lancement = "cle1", "l1"
    c2.cle, c2.lancement = "cle2", "l2"
    pret = {"etat": "pret", "url": "https://x.trycloudflare.com", "jeton": "j"}
    assert not asyncio.run(p.recevoir_annonce({**pret, "cle": "cle1", "lancement": "l2"}))   # clés croisées
    assert asyncio.run(p.recevoir_annonce({**pret, "cle": "cle2", "lancement": "l2"}))
    assert c2.etat == "pret" and c1.etat == "eteint"
    assert _pilote(tmp_path).cible() == ("https://x.trycloudflare.com", "j")   # survit au redémarrage


def test_ancien_fichier_d_etat_repris(tmp_path, comptes):
    (tmp_path / "etat.json").write_text(json.dumps({
        "etat": "pret", "url": "https://vieux.trycloudflare.com", "jeton": "j", "cle": "c", "lancement": "l",
        "depuis": time.time(), "sessions": [[time.time() - 60, 0]], "derniere_parole": time.time()}),
        encoding="utf-8")
    p = _pilote(tmp_path)
    assert p.cible() == ("https://vieux.trycloudflare.com", "j")
    assert _compte(p, "prof").etat == "pret" and _compte(p, "secours1").etat == "eteint"


def test_kernel_d_un_compte_de_secours(tmp_path, comptes, dossier_kernel):
    p = _pilote(tmp_path)
    construire_kernel(tmp_path, "c", "l", "j", compte=_compte(p, "secours1"))
    meta = json.loads((tmp_path / "kernel-metadata.json").read_text(encoding="utf-8"))
    assert meta["id"] == "secours1/academy-tts-direct"
    assert meta["kernel_sources"] and all(s.startswith("prof/") for s in meta["kernel_sources"])   # poids du principal


def test_cli_avec_le_jeton_du_compte(tmp_path, comptes, monkeypatch):
    vus = {}

    class R:
        returncode, stdout, stderr = 0, "ok", ""

    def run(cmd, **k):
        vus.update(k["env"])
        return R()
    monkeypatch.setattr(kaggle_tts.subprocess, "run", run)
    p = _pilote(tmp_path)
    kaggle_cli_reel("kernels", "list", compte=_compte(p, "secours1"))
    assert vus["KAGGLE_USERNAME"] == "secours1" and vus["KAGGLE_API_TOKEN"] == "t2"
    kaggle_cli_reel("kernels", "list")
    assert vus["KAGGLE_USERNAME"] == "prof" and vus["KAGGLE_API_TOKEN"] == "jeton-kaggle"
