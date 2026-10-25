"""Voix du prof sur Kaggle, allumée à la demande comme un GPU loué à l'heure.

Cycle de vie (un seul kernel à la fois) :

    eteint ──reveiller()──► demarrage ──annonce « pret »──► pret
       ▲                        │                              │
       └── délai dépassé ◄──────┘     annonce « eteint » ◄─────┘
                                      (5 min sans parler : le kernel s'arrête seul)

- `reveiller()` est appelé à l'ouverture d'une séance (le kernel chauffe pendant
  que l'élève lit l'énoncé) et chaque fois que la voix est demandée.
- Le kernel n'a pas d'adresse fixe : il ouvre un tunnel et nous l'annonce sur
  /api/v1/tts-kaggle/annonce avec la clé reçue au lancement.
- Kaggle n'offre aucun moyen d'arrêter un kernel à distance : c'est le kernel
  qui s'éteint après `kaggle_tts_veille_s` sans requête. Côté backend on ne
  fait que suivre l'état, et on refuse de relancer au-delà du budget hebdo.

Rien ici ne bloque la parole : tant que l'état n'est pas « pret », `cible()`
rend None et tts_service garde sa chaîne habituelle (Academy statique, puis
Google Cloud).
"""
from __future__ import annotations

import asyncio
import json
import os
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

from app.config import get_settings

settings = get_settings()

class _Journal:
    """Comme tts_service : print, que journalctl affiche (les log.info de
    l'application ne sortent pas en production)."""

    @staticmethod
    def _ecrire(niveau, msg, *args):
        texte = msg % args if args else msg
        try:
            print(f"{niveau}{texte}", flush=True)
        except UnicodeEncodeError:
            print(f"{niveau}{texte}".encode("ascii", "replace").decode(), flush=True)

    def info(self, msg, *args):
        self._ecrire("", msg, *args)

    def warning(self, msg, *args):
        self._ecrire("⚠ ", msg, *args)

    def error(self, msg, *args):
        self._ecrire("✖ ", msg, *args)


log = _Journal()

DOSSIER_KERNEL = Path(__file__).resolve().parents[2] / "kaggle_tts"
SEMAINE_S = 7 * 24 * 3600
# Après un lancement raté, on n'insiste pas aussitôt : chaque essai peut
# coûter des minutes de quota.
PAUSE_APRES_ECHEC_S = 180


def actif() -> bool:
    return bool(settings.kaggle_tts_actif and settings.kaggle_username and settings.kaggle_api_token)


class PiloteKaggle:
    def __init__(self, chemin: Optional[Path] = None):
        self.chemin = Path(chemin or settings.kaggle_tts_etat_path)
        self.etat = "eteint"
        self.url = ""
        self.jeton = ""
        self.cle = ""
        self.lancement = ""
        self.depuis = 0.0             # début de l'état courant
        self.derniere_parole = 0.0
        self.dernier_echec = 0.0
        self.sessions: list[list[float]] = []   # [début, fin] de chaque kernel, pour le budget
        self._tache: Optional[asyncio.Task] = None
        self._charger()

    # ── état persistant : un redémarrage du backend ne perd pas un kernel allumé ──
    def _charger(self):
        try:
            d = json.loads(self.chemin.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        for k in ("etat", "url", "jeton", "cle", "lancement", "depuis", "sessions"):
            if k in d:
                setattr(self, k, d[k])

    def _sauver(self):
        try:
            self.chemin.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.chemin.with_suffix(".tmp")
            tmp.write_text(json.dumps({k: getattr(self, k) for k in
                                       ("etat", "url", "jeton", "cle", "lancement", "depuis", "sessions")}),
                           encoding="utf-8")
            os.replace(tmp, self.chemin)
        except OSError as e:
            log.warning("[KaggleTTS] état non sauvegardé : %s", e)

    def _passer(self, etat: str, maintenant: float):
        self.etat, self.depuis = etat, maintenant
        if etat == "eteint":
            self.url = self.jeton = ""
            if self.sessions and self.sessions[-1][1] == 0:
                self.sessions[-1][1] = maintenant
        self._sauver()

    # ── budget ──
    def heures_semaine(self, maintenant: Optional[float] = None) -> float:
        maintenant = maintenant or time.time()
        total = 0.0
        for debut, fin in self.sessions:
            fin = fin or maintenant
            if fin > maintenant - SEMAINE_S:
                total += fin - max(debut, maintenant - SEMAINE_S)
        return total / 3600

    def _verifier_delais(self, maintenant: float):
        """Corrige un état que le kernel n'a pas pu nous annoncer (annonce perdue)."""
        if self.etat == "demarrage" and maintenant - self.depuis > settings.kaggle_tts_demarrage_max_s:
            log.warning("[KaggleTTS] pas d'annonce après %ss — lancement tenu pour raté",
                        settings.kaggle_tts_demarrage_max_s)
            self.dernier_echec = maintenant
            self._passer("eteint", maintenant)
        elif self.etat == "pret":
            # Le kernel s'éteint seul après la veille ; +60 s de marge pour son annonce.
            silence = maintenant - max(self.derniere_parole, self.depuis)
            if silence > settings.kaggle_tts_veille_s + 60:
                self._passer("eteint", maintenant)

    # ── API utilisée par tts_service et la séance ──
    def cible(self) -> Optional[tuple[str, str]]:
        """(url, jeton) du kernel prêt, sinon None."""
        if not actif():
            return None
        self._verifier_delais(time.time())
        return (self.url, self.jeton) if self.etat == "pret" and self.url else None

    def besoin_de_voix(self, raison: str = "parole"):
        """La voix est demandée : note l'activité, allume le kernel s'il dort."""
        if not actif():
            return
        maintenant = time.time()
        if raison == "parole":
            self.derniere_parole = maintenant
        self._verifier_delais(maintenant)
        if self.etat != "eteint" or (self._tache and not self._tache.done()):
            return
        if maintenant - self.dernier_echec < PAUSE_APRES_ECHEC_S:
            return
        if self.heures_semaine(maintenant) >= settings.kaggle_tts_budget_h_semaine:
            log.warning("[KaggleTTS] budget hebdo atteint (%.1f h) — voix de secours",
                        self.heures_semaine(maintenant))
            return
        try:
            boucle = asyncio.get_running_loop()
        except RuntimeError:
            return
        self._tache = boucle.create_task(self._lancer(raison))

    async def attendre_si_presque_pret(self, max_s: float = 60.0):
        """Le kernel démarre depuis plus de 90 s (prêt vers 145 s) : mieux vaut
        que la réplique en cours attende quelques secondes la voix du prof que
        de partir dans le vide. Plus tôt, on n'attend pas : l'écart serait trop long."""
        if not actif() or self.etat != "demarrage" or time.time() - self.depuis < 90:
            return
        fin = time.time() + max_s
        while self.etat == "demarrage" and time.time() < fin:
            await asyncio.sleep(1.0)
            self._verifier_delais(time.time())

    def signaler_injoignable(self, url: str):
        """Le tunnel ne répond plus (502/530, HTML…) : le kernel est parti."""
        if self.etat == "pret" and url and url.rstrip("/") == self.url.rstrip("/"):
            log.warning("[KaggleTTS] tunnel injoignable — kernel tenu pour éteint")
            self._passer("eteint", time.time())

    async def recevoir_annonce(self, d: dict) -> bool:
        if not self.cle or not secrets.compare_digest(str(d.get("cle", "")), self.cle):
            return False
        if d.get("lancement") != self.lancement:
            return False
        maintenant = time.time()
        etat = d.get("etat")
        if etat == "demarrage":
            log.info("[KaggleTTS] kernel parti (sorti de la file Kaggle)")
        elif etat == "pret":
            url, jeton = str(d.get("url", "")).rstrip("/"), str(d.get("jeton", ""))
            if not url.startswith("https://") or not jeton:
                return False
            if not await _sante(url, jeton):
                log.warning("[KaggleTTS] annonce « pret » mais %s/health ne répond pas", url)
                return True
            self.url, self.jeton = url, jeton
            self.derniere_parole = maintenant   # la veille court à partir d'ici
            self._passer("pret", maintenant)
            import app.services.tts_service as voix
            voix.reinitialiser_disjoncteur_academy()
            log.info("[KaggleTTS] voix prête : %s (%s carte(s), démarrage %ss)",
                     url, d.get("gpus"), d.get("demarrage_s"))
        elif etat == "eteint":
            log.info("[KaggleTTS] kernel éteint (%s, %ss)", d.get("raison"), d.get("duree_s"))
            if self.etat == "demarrage":
                self.dernier_echec = maintenant
            self._passer("eteint", maintenant)
        return True

    def resume(self) -> dict:
        self._verifier_delais(time.time())
        return {"actif": actif(), "etat": self.etat, "depuis_s": round(time.time() - self.depuis) if self.depuis else None,
                "heures_semaine": round(self.heures_semaine(), 2),
                "budget_h_semaine": settings.kaggle_tts_budget_h_semaine}

    # ── lancement ──
    async def _lancer(self, raison: str):
        maintenant = time.time()
        self.cle = secrets.token_urlsafe(24)
        self.lancement = secrets.token_hex(6)
        jeton = secrets.token_urlsafe(24)
        self.sessions.append([maintenant, 0])
        self.sessions = self.sessions[-200:]
        self._passer("demarrage", maintenant)
        log.info("[KaggleTTS] réveil du kernel (%s)", raison)
        try:
            await asyncio.to_thread(pousser_kernel, self.cle, self.lancement, jeton)
        except Exception as e:
            log.error("[KaggleTTS] push refusé : %s", str(e)[-400:])
            self.dernier_echec = time.time()
            self._passer("eteint", time.time())


def construire_kernel(dossier: Path, cle: str, lancement: str, jeton: str) -> Path:
    """Écrit serveur.py (CONF + référence Amine) et kernel-metadata.json."""
    import base64
    conf = {"annonce": settings.kaggle_tts_annonce_url, "cle": cle, "lancement": lancement, "jeton": jeton,
            "modele": settings.kaggle_tts_modele, "veille_s": settings.kaggle_tts_veille_s,
            "duree_max_s": settings.kaggle_tts_duree_max_s}
    source = (DOSSIER_KERNEL / "serveur.py").read_text(encoding="utf-8")
    ref = base64.b64encode((DOSSIER_KERNEL / "reference_amine.flac").read_bytes()).decode()
    source = source.replace('"__CONF__"', repr(json.dumps(conf)), 1).replace('"__REF_B64__"', repr(ref), 1)
    (dossier / "serveur.py").write_text(source, encoding="utf-8")
    u = settings.kaggle_username
    sources = [f"{u}/{settings.kaggle_tts_modele}"]
    if settings.kaggle_tts_socle:
        sources.append(f"{u}/{settings.kaggle_tts_socle}")
    meta = {"id": f"{u}/{settings.kaggle_tts_kernel}", "title": settings.kaggle_tts_kernel,
            "code_file": "serveur.py", "language": "python", "kernel_type": "script",
            "is_private": True, "enable_gpu": True, "enable_internet": True,
            "machine_shape": "NvidiaTeslaT4", "dataset_sources": [], "competition_sources": [],
            "kernel_sources": sources}
    (dossier / "kernel-metadata.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    return dossier


def kaggle_cli(*args: str, timeout: float = 120) -> str:
    env = {**os.environ, "KAGGLE_USERNAME": settings.kaggle_username,
           "KAGGLE_API_TOKEN": settings.kaggle_api_token}
    r = subprocess.run([sys.executable, "-m", "kaggle", *args], capture_output=True, text=True,
                       timeout=timeout, env=env)
    sortie = (r.stdout + r.stderr).strip()
    if r.returncode:
        raise RuntimeError(sortie[-600:] or f"kaggle {args[0]} : code {r.returncode}")
    return sortie


def pousser_kernel(cle: str, lancement: str, jeton: str) -> str:
    dossier = Path(tempfile.mkdtemp(prefix="kaggle_tts_"))
    try:
        construire_kernel(dossier, cle, lancement, jeton)
        # Filet de sécurité côté Kaggle : même si la veille du kernel échouait,
        # Kaggle le couperait peu après la durée maximale.
        return kaggle_cli("kernels", "push", "-p", str(dossier),
                          "-t", str(settings.kaggle_tts_duree_max_s + 600))
    finally:
        shutil.rmtree(dossier, ignore_errors=True)


async def _sante(url: str, jeton: str) -> bool:
    import httpx
    try:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(f"{url}/health", headers={"Authorization": f"Bearer {jeton}"})
        return r.status_code == 200
    except Exception:
        return False


pilote = PiloteKaggle()
