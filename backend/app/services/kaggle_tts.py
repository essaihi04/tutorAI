"""Voix du prof sur Kaggle, allumée à la demande comme un GPU loué à l'heure.

Cycle de vie d'un kernel (un par compte Kaggle) :

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

Plusieurs comptes (11 novembre 2026) : le compte principal (KAGGLE_USERNAME)
parle tant qu'il n'est pas saturé ; KAGGLE2_USERNAME / KAGGLE2_API_TOKEN …
KAGGLE10_… prennent le relais quand il l'est (file d'attente, 503, quota de la
semaine, « Maximum batch GPU session count », tunnel muet, push refusé). Un
seul réveil à la fois ; un compte de secours est réveillé à l'avance quand
celui qui parle se charge. Avec un seul compte, rien ne change.

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
from functools import lru_cache
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


# Plusieurs comptes Kaggle (11 novembre 2026) : chaque compte a 2 sessions GPU
# et 30 h par semaine. Quand l'un est saturé, à court de quota ou en panne, la
# voix passe au suivant sans que l'élève attende.
PAUSE_SESSIONS_PLEINES_S = 600     # « Maximum batch GPU session count of 2 reached »
PAUSE_QUOTA_S = 6 * 3600           # quota GPU de la semaine épuisé : on réessaie plus tard
REPOS_APRES_REFUS_S = 90           # 503 / tunnel muet : le compte ne sert plus pendant ce temps
CHAMPS_SAUVES = ("etat", "url", "jeton", "cle", "lancement", "depuis", "sessions", "derniere_parole",
                 "dernier_echec", "derniere_erreur", "repos_jusqua", "quota_jusqua", "pleines_jusqua",
                 "sorti_de_file")


def actif() -> bool:
    return bool(settings.kaggle_tts_actif and settings.kaggle_username and settings.kaggle_api_token)


@lru_cache(maxsize=1)
def _env_fichier() -> dict:
    """Variables de backend/.env (en local). En prod, systemd les met déjà dans l'environnement."""
    if os.environ.get("APP_ENV") == "production":
        return {}
    try:
        from dotenv import dotenv_values
        from app.config import _FICHIER_ENV
        return {k.upper(): v for k, v in dotenv_values(_FICHIER_ENV).items() if v}
    except Exception:
        return {}


def comptes_configures() -> list[tuple[str, str]]:
    """[(nom, jeton)] : le compte principal, puis KAGGLE2_…, KAGGLE3_… dans l'ordre des numéros."""
    if not (settings.kaggle_username and settings.kaggle_api_token):
        return []
    fichier = _env_fichier()
    out, vus = [(settings.kaggle_username, settings.kaggle_api_token)], {settings.kaggle_username}
    for n in range(2, settings.kaggle_tts_comptes_max + 1):
        nom = os.environ.get(f"KAGGLE{n}_USERNAME") or fichier.get(f"KAGGLE{n}_USERNAME", "")
        jeton = os.environ.get(f"KAGGLE{n}_API_TOKEN") or fichier.get(f"KAGGLE{n}_API_TOKEN", "")
        if nom and jeton and nom not in vus:
            out.append((nom, jeton))
            vus.add(nom)
    return out


class _Porte:
    """Comme asyncio.Semaphore(2), mais compte qui attend : c'est la charge du compte."""

    def __init__(self, n: int = 2):
        self._sem = asyncio.Semaphore(n)
        self.attente = 0
        self.en_cours = 0

    async def __aenter__(self):
        self.attente += 1
        try:
            await self._sem.acquire()
        finally:
            self.attente -= 1
        self.en_cours += 1
        return self

    async def __aexit__(self, *exc):
        self.en_cours -= 1
        self._sem.release()
        return False


class CompteKaggle:
    """Un compte Kaggle et SON kernel de voix."""

    def __init__(self, nom: str, jeton_api: str = "", rang: int = 0):
        self.nom, self.jeton_api, self.rang = nom, jeton_api, rang
        self.etat = "eteint"
        self.url = self.jeton = self.cle = self.lancement = ""
        self.depuis = 0.0              # début de l'état courant
        self.derniere_parole = 0.0
        self.dernier_echec = 0.0
        self.derniere_erreur = ""
        self.repos_jusqua = 0.0        # 503 / tunnel muet : ne sert plus jusque-là
        self.quota_jusqua = 0.0        # Kaggle a refusé pour quota
        self.pleines_jusqua = 0.0      # Kaggle a refusé : 2 sessions GPU déjà prises
        self.sorti_de_file = False     # le kernel a annoncé « demarrage » (il tourne)
        self.sessions: list[list[float]] = []   # [début, fin] de chaque kernel, pour le budget
        self.porte = _Porte(2)         # deux requêtes à la fois par kernel (deux cartes)
        self._tache: Optional[asyncio.Task] = None

    def charger(self, d: dict):
        for k in CHAMPS_SAUVES:
            if k in d:
                setattr(self, k, d[k])

    def en_dict(self) -> dict:
        return {k: getattr(self, k) for k in CHAMPS_SAUVES}

    def heures(self, maintenant: Optional[float] = None) -> float:
        maintenant = maintenant or time.time()
        total = 0.0
        for debut, fin in self.sessions:
            fin = fin or maintenant
            if fin > maintenant - SEMAINE_S:
                total += fin - max(debut, maintenant - SEMAINE_S)
        return total / 3600

    def charge(self) -> int:
        return self.porte.attente + self.porte.en_cours

    def lance_en_cours(self) -> bool:
        return bool(self._tache and not self._tache.done())

    def disponible(self, maintenant: float) -> bool:
        """Peut-on réveiller ce compte maintenant ?"""
        return (self.etat == "eteint" and not self.lance_en_cours()
                and maintenant - self.dernier_echec >= PAUSE_APRES_ECHEC_S
                and maintenant >= max(self.repos_jusqua, self.quota_jusqua, self.pleines_jusqua)
                and self.heures(maintenant) < settings.kaggle_tts_budget_h_semaine)

    def statut(self, maintenant: float) -> str:
        """Un mot lisible pour l'admin."""
        if self.etat == "pret":
            sature = (maintenant < self.repos_jusqua
                      or self.porte.attente >= settings.kaggle_tts_attente_max)
            return "sature" if sature else "pret"
        if self.etat == "demarrage":
            return "demarrage" if self.sorti_de_file else "file_kaggle"
        if maintenant < self.quota_jusqua or self.heures(maintenant) >= settings.kaggle_tts_budget_h_semaine:
            return "quota"
        if maintenant < self.pleines_jusqua:
            return "sessions_pleines"
        if maintenant - self.dernier_echec < PAUSE_APRES_ECHEC_S or maintenant < self.repos_jusqua:
            return "erreur"
        return "eteint"


class PiloteKaggle:
    """Tous les comptes Kaggle de la voix. Avec un seul compte, il se comporte
    exactement comme l'ancien pilote, et ses champs (`cle`, `depuis`…) restent
    lisibles et modifiables : ce sont ceux du compte principal."""

    _CHAMPS_PRINCIPAL = ("url", "jeton", "cle", "lancement", "depuis", "derniere_parole",
                         "dernier_echec", "sessions")

    def __init__(self, chemin: Optional[Path] = None):
        self.chemin = Path(chemin or settings.kaggle_tts_etat_path)
        self._comptes: dict[str, CompteKaggle] = {}
        self._brut: dict[str, dict] = {}      # état sauvé, repris quand le compte apparaît
        self._tache: Optional[asyncio.Task] = None   # dernier lancement (pour les tests)
        self._dernier_avis = 0.0
        self._charger()

    def __getattr__(self, nom):
        if nom in PiloteKaggle._CHAMPS_PRINCIPAL:
            return getattr(self._principal(), nom)
        raise AttributeError(nom)

    def __setattr__(self, nom, valeur):
        if nom in PiloteKaggle._CHAMPS_PRINCIPAL:
            setattr(self._principal(), nom, valeur)
        else:
            object.__setattr__(self, nom, valeur)

    # ── comptes ──
    def _compte(self, nom: str, jeton: str, rang: int) -> CompteKaggle:
        c = self._comptes.get(nom)
        if c is None:
            c = self._comptes[nom] = CompteKaggle(nom, jeton, rang)
            d = self._brut.pop(nom, None)
            if d is None and rang == 0:
                d = self._brut.pop("", None)     # ancien fichier : un seul compte, le principal
            if d:
                c.charger(d)
        c.jeton_api, c.rang = jeton, rang
        return c

    def comptes(self) -> list[CompteKaggle]:
        """Comptes configurés, le principal d'abord."""
        return [self._compte(nom, jeton, rang) for rang, (nom, jeton) in enumerate(comptes_configures())]

    def _principal(self) -> CompteKaggle:
        return self._compte(settings.kaggle_username, settings.kaggle_api_token, 0)

    def _tous(self) -> list[CompteKaggle]:
        return self.comptes() or [self._principal()]

    # ── état persistant : un redémarrage du backend ne perd pas un kernel allumé ──
    def _charger(self):
        try:
            d = json.loads(self.chemin.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        if isinstance(d.get("comptes"), dict):
            self._brut = {k: v for k, v in d["comptes"].items() if isinstance(v, dict)}
        elif isinstance(d, dict):
            self._brut = {"": d}

    def _sauver(self):
        try:
            self.chemin.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.chemin.with_suffix(".tmp")
            comptes = dict(self._brut)
            comptes.update({nom: c.en_dict() for nom, c in self._comptes.items()})
            tmp.write_text(json.dumps({"comptes": comptes}), encoding="utf-8")
            os.replace(tmp, self.chemin)
        except OSError as e:
            log.warning("[KaggleTTS] état non sauvegardé : %s", e)

    def _passer(self, c: CompteKaggle, etat: str, maintenant: float):
        c.etat, c.depuis = etat, maintenant
        if etat == "eteint":
            # L'adresse est GARDÉE : avant tout nouveau lancement on vérifie
            # qu'elle ne répond vraiment plus (cf. _lancer). `cible()` ne la
            # rend de toute façon qu'à l'état « pret ».
            if c.sessions and c.sessions[-1][1] == 0:
                c.sessions[-1][1] = maintenant
        elif etat == "pret" and (not c.sessions or c.sessions[-1][1]):
            c.sessions.append([maintenant, 0])      # kernel repris : ses heures comptent aussi
            c.sessions = c.sessions[-200:]
        if etat == "pret":
            c.porte = _Porte(2)
        self._sauver()

    # ── budget ──
    def heures_semaine(self, maintenant: Optional[float] = None) -> float:
        return sum(c.heures(maintenant) for c in self._tous())

    def _verifier_delais(self, c: CompteKaggle, maintenant: float):
        """Corrige un état que le kernel n'a pas pu nous annoncer (annonce perdue)."""
        if c.etat == "demarrage" and maintenant - c.depuis > settings.kaggle_tts_demarrage_max_s:
            log.warning("[KaggleTTS] %s : pas d'annonce après %ss — lancement tenu pour raté",
                        c.nom, settings.kaggle_tts_demarrage_max_s)
            c.dernier_echec = maintenant
            c.derniere_erreur = "pas d'annonce au démarrage"
            self._passer(c, "eteint", maintenant)
        elif c.etat == "pret":
            # Le kernel s'éteint seul après la veille ; +60 s de marge pour son annonce.
            silence = maintenant - max(c.derniere_parole, c.depuis)
            if silence > settings.kaggle_tts_veille_s + 60:
                self._passer(c, "eteint", maintenant)

    def _verifier_tous(self, maintenant: float) -> list[CompteKaggle]:
        comptes = self._tous()
        for c in comptes:
            self._verifier_delais(c, maintenant)
        return comptes

    # ── choix du compte qui parle ──
    @staticmethod
    def _choisir(comptes: list[CompteKaggle], maintenant: float) -> Optional[CompteKaggle]:
        """Le principal s'il est prêt et pas saturé, sinon le moins chargé des prêts."""
        prets = [c for c in comptes if c.etat == "pret" and c.url and maintenant >= c.repos_jusqua]
        if not prets:
            return None
        libres = [c for c in prets if c.porte.attente < settings.kaggle_tts_attente_max] or prets
        if libres[0].rang == 0:
            return libres[0]
        return min(libres, key=lambda c: (c.charge(), c.heures(maintenant), c.rang))

    def _a_reveiller(self, comptes: list[CompteKaggle], sert: Optional[CompteKaggle],
                     maintenant: float) -> Optional[CompteKaggle]:
        if any(c.lance_en_cours() for c in comptes):
            return None                                   # jamais deux réveils à la fois
        if sert is not None:
            # Réveil à l'avance : le compte qui parle se charge ou arrive au bout de son quota.
            presque = (sert.porte.attente >= max(1, settings.kaggle_tts_attente_max - 1)
                       or sert.heures(maintenant) >= settings.kaggle_tts_budget_h_semaine)
            if not presque or any(c is not sert and c.etat in ("pret", "demarrage") for c in comptes):
                return None
        else:
            demarrages = [c for c in comptes if c.etat == "demarrage"]
            if demarrages:
                # Un seul réveil de plus, et seulement si le kernel attend encore dans la file de Kaggle.
                if (len(comptes) == 1 or len(demarrages) > 1 or demarrages[0].sorti_de_file
                        or maintenant - demarrages[0].depuis < settings.kaggle_tts_file_kaggle_max_s):
                    return None
        for c in comptes:
            if c.disponible(maintenant):
                return c
        if sert is None and maintenant - self._dernier_avis > 60:
            self._dernier_avis = maintenant
            log.warning("[KaggleTTS] aucun compte disponible (%s) — voix de secours",
                        ", ".join(f"{c.nom} {c.statut(maintenant)} {c.heures(maintenant):.1f} h" for c in comptes))
        return None

    # ── API utilisée par tts_service et la séance ──
    def cible(self) -> Optional[tuple[str, str]]:
        """(url, jeton) du kernel qui doit parler maintenant, sinon None."""
        if not actif():
            return None
        maintenant = time.time()
        c = self._choisir(self._verifier_tous(maintenant), maintenant)
        return (c.url, c.jeton) if c else None

    def porte(self, url: str) -> Optional[_Porte]:
        """Le « sémaphore » du kernel joint à cette adresse (deux requêtes à la fois)."""
        url = (url or "").rstrip("/")
        for c in self._tous():
            if url and c.url.rstrip("/") == url:
                return c.porte
        return None

    @property
    def etat(self) -> str:
        etats = {c.etat for c in self._tous()}
        return "pret" if "pret" in etats else "demarrage" if "demarrage" in etats else "eteint"

    def besoin_de_voix(self, raison: str = "parole"):
        """La voix est demandée : note l'activité, allume un kernel s'il le faut."""
        if not actif():
            return
        maintenant = time.time()
        comptes = self._verifier_tous(maintenant)
        sert = self._choisir(comptes, maintenant)
        if raison == "parole":
            (sert or comptes[0]).derniere_parole = maintenant
        c = self._a_reveiller(comptes, sert, maintenant)
        if c is None:
            return
        try:
            boucle = asyncio.get_running_loop()
        except RuntimeError:
            return
        c._tache = self._tache = boucle.create_task(self._lancer(c, raison))

    def _basculer(self):
        """Un compte vient de lâcher : on cherche le suivant dès que la tâche en cours est finie."""
        if len(self._tous()) < 2:
            return
        try:
            asyncio.get_running_loop().call_soon(self.besoin_de_voix, "bascule")
        except RuntimeError:
            pass

    def _demarrages(self) -> list[CompteKaggle]:
        return [c for c in self._tous() if c.etat == "demarrage"]

    async def attendre_si_presque_pret(self, max_s: float = 60.0):
        """Le kernel démarre depuis plus de 90 s (prêt vers 145 s) : mieux vaut
        que la réplique en cours attende quelques secondes la voix du prof que
        de partir dans le vide. Plus tôt, on n'attend pas : l'écart serait trop long."""
        if not actif() or self.cible():
            return
        demarrages = self._demarrages()
        if not demarrages or time.time() - min(c.depuis for c in demarrages) < 90:
            return
        fin = time.time() + max_s
        while self._demarrages() and not self.cible() and time.time() < fin:
            await asyncio.sleep(1.0)

    async def attendre_pret(self, max_s: float) -> bool:
        """Attend la fin d'un démarrage en cours ; vrai si la voix est prête."""
        fin = time.time() + max_s
        while self._demarrages() and not self.cible() and time.time() < fin:
            await asyncio.sleep(1.0)
        return self.cible() is not None

    def eleve_actif(self):
        """L'élève vient d'agir : la séance compte comme active pour la veille
        (le kernel ne s'éteint pas pendant qu'il lit ou réfléchit), et un
        kernel éteint est rallumé pour que la réponse ait sa voix."""
        if not actif():
            return
        self.besoin_de_voix("parole")
        cible = self.cible()
        if not cible:
            return
        try:
            asyncio.get_running_loop().create_task(_garder(*cible))
        except RuntimeError:
            pass

    def signaler_injoignable(self, url: str):
        """Le tunnel ne répond plus (502/530, HTML…) ou refuse (503 saturé)."""
        url = (url or "").rstrip("/")
        comptes = self._tous()
        c = next((c for c in comptes if c.etat == "pret" and url and c.url.rstrip("/") == url), None)
        if c is None:
            return
        if len(comptes) == 1:
            log.warning("[KaggleTTS] tunnel injoignable — kernel tenu pour éteint")
            self._passer(c, "eteint", time.time())
            return
        # Plusieurs comptes : celui-ci se repose, un /health dira s'il est mort
        # ou seulement saturé ; la voix passe aussitôt au suivant.
        c.repos_jusqua = time.time() + REPOS_APRES_REFUS_S
        c.derniere_erreur = "tunnel injoignable ou saturé"
        self._sauver()
        log.warning("[KaggleTTS] %s injoignable ou saturé — la voix passe à un autre compte", c.nom)
        try:
            asyncio.get_running_loop().create_task(self._verifier_vivant(c, c.url))
        except RuntimeError:
            self._passer(c, "eteint", time.time())
            return
        self._basculer()

    async def _verifier_vivant(self, c: CompteKaggle, url: str):
        if await _sante(url, c.jeton):
            return                                        # saturé : il reservira après son repos
        if c.etat == "pret" and c.url == url:
            log.warning("[KaggleTTS] %s : /health muet — kernel tenu pour éteint", c.nom)
            self._passer(c, "eteint", time.time())

    async def recevoir_annonce(self, d: dict) -> bool:
        cle = str(d.get("cle", "")).encode()
        c = next((c for c in self._tous() if c.cle and secrets.compare_digest(cle, c.cle.encode())), None)
        if c is None or d.get("lancement") != c.lancement:
            return False
        maintenant = time.time()
        etat = d.get("etat")
        if etat == "demarrage":
            log.info("[KaggleTTS] %s : kernel parti (sorti de la file Kaggle)", c.nom)
            c.sorti_de_file = True
            self._sauver()
        elif etat == "pret":
            url, jeton = str(d.get("url", "")).rstrip("/"), str(d.get("jeton", ""))
            if not url.startswith("https://") or not jeton:
                return False
            if not await _sante(url, jeton):
                log.warning("[KaggleTTS] annonce « pret » mais %s/health ne répond pas", url)
                return True
            c.url, c.jeton = url, jeton
            c.derniere_parole = maintenant   # la veille court à partir d'ici
            c.repos_jusqua, c.derniere_erreur = 0.0, ""
            self._passer(c, "pret", maintenant)
            import app.services.tts_service as voix
            voix.reinitialiser_disjoncteur_academy()
            log.info("[KaggleTTS] %s : voix prête : %s (%s carte(s), démarrage %ss)",
                     c.nom, url, d.get("gpus"), d.get("demarrage_s"))
        elif etat == "eteint":
            log.info("[KaggleTTS] %s : kernel éteint (%s, %ss)", c.nom, d.get("raison"), d.get("duree_s"))
            rate = c.etat == "demarrage"
            if rate:
                c.dernier_echec = maintenant
                c.derniere_erreur = f"éteint au démarrage : {d.get('raison')}"
            self._passer(c, "eteint", maintenant)
            if rate:
                self._basculer()
        return True

    def resume(self) -> dict:
        maintenant = time.time()
        comptes = self._verifier_tous(maintenant)
        sert = self._choisir(comptes, maintenant) if actif() else None
        ref = sert or next((c for c in comptes if c.etat == "demarrage"), comptes[0])
        return {"actif": actif(), "etat": self.etat,
                "depuis_s": round(maintenant - ref.depuis) if ref.depuis else None,
                "heures_semaine": round(self.heures_semaine(maintenant), 2),   # tous comptes
                "budget_h_semaine": settings.kaggle_tts_budget_h_semaine,      # par compte
                "comptes": [{"nom": c.nom, "statut": c.statut(maintenant), "sert": c is sert,
                             "heures_semaine": round(c.heures(maintenant), 2),
                             "depuis_s": round(maintenant - c.depuis) if c.depuis else None,
                             "attente": c.porte.attente, "en_cours": c.porte.en_cours,
                             "derniere_erreur": c.derniere_erreur} for c in comptes]}

    # ── lancement ──
    def _noter_refus(self, c: CompteKaggle, message: str, maintenant: float):
        bas = message.lower()
        if "session count" in bas or "maximum batch gpu" in bas:
            c.pleines_jusqua = maintenant + PAUSE_SESSIONS_PLEINES_S
        elif "quota" in bas:
            c.quota_jusqua = maintenant + PAUSE_QUOTA_S
        else:
            c.dernier_echec = maintenant
        c.derniere_erreur = message[-200:]

    async def _lancer(self, c: CompteKaggle, raison: str):
        # Le kernel est peut-être encore vivant alors qu'on le croyait éteint
        # (redémarrage du backend, horloge de veille approximative). Pousser
        # une nouvelle version changeait alors les clés : l'ancien kernel se
        # faisait refuser ses annonces et le nouveau ne démarrait jamais —
        # plus de voix du tout.
        if c.url and c.jeton and await _sante(c.url, c.jeton):
            log.info("[KaggleTTS] %s : kernel toujours vivant : %s, on le reprend", c.nom, c.url)
            c.derniere_parole = time.time()
            c.repos_jusqua = 0.0
            self._passer(c, "pret", time.time())
            import app.services.tts_service as voix
            voix.reinitialiser_disjoncteur_academy()
            return
        try:
            statut = await asyncio.to_thread(
                kaggle_cli, "kernels", "status", f"{c.nom}/{settings.kaggle_tts_kernel}",
                timeout=30, compte=c)
        except Exception as e:
            statut = str(e)
        if "RUNNING" in statut or "QUEUED" in statut:
            log.warning("[KaggleTTS] %s : une session tourne encore sur Kaggle sans répondre — pas de "
                        "nouveau lancement, nouvel essai dans 1 min", c.nom)
            c.dernier_echec = time.time() - PAUSE_APRES_ECHEC_S + 60
            c.derniere_erreur = "session Kaggle en cours sans réponse"
            self._sauver()
            self._basculer()
            return
        maintenant = time.time()
        c.cle = secrets.token_urlsafe(24)
        c.lancement = secrets.token_hex(6)
        jeton = secrets.token_urlsafe(24)
        c.sorti_de_file = False
        c.sessions.append([maintenant, 0])
        c.sessions = c.sessions[-200:]
        self._passer(c, "demarrage", maintenant)
        log.info("[KaggleTTS] réveil du kernel de %s (%s)", c.nom, raison)
        try:
            await asyncio.to_thread(pousser_kernel, c.cle, c.lancement, jeton, compte=c)
        except Exception as e:
            log.error("[KaggleTTS] %s : push refusé : %s", c.nom, str(e)[-400:])
            self._noter_refus(c, str(e), time.time())
            self._passer(c, "eteint", time.time())
            self._basculer()


def construire_kernel(dossier: Path, cle: str, lancement: str, jeton: str,
                      kernel: Optional[str] = None, compte: Optional[CompteKaggle] = None) -> Path:
    """Écrit serveur.py (CONF + référence Amine) et kernel-metadata.json."""
    import base64
    conf = {"annonce": settings.kaggle_tts_annonce_url, "cle": cle, "lancement": lancement, "jeton": jeton,
            "modele": settings.kaggle_tts_modele, "veille_s": settings.kaggle_tts_veille_s,
            "duree_max_s": settings.kaggle_tts_duree_max_s, "fp16": bool(settings.kaggle_tts_fp16),
            "pas_flow": settings.kaggle_tts_pas_flow, "stt": settings.kaggle_stt_modele}
    source = (DOSSIER_KERNEL / "serveur.py").read_text(encoding="utf-8")
    ref = base64.b64encode((DOSSIER_KERNEL / settings.kaggle_tts_reference).read_bytes()).decode()
    regles = base64.b64encode((DOSSIER_KERNEL / "texte_parle.py").read_bytes()).decode()   # formules, nombres (cf. cours v8)
    source = (source.replace('"__CONF__"', repr(json.dumps(conf)), 1).replace('"__REF_B64__"', repr(ref), 1)
              .replace('"__TEXTE_PARLE_B64__"', repr(regles), 1))
    (dossier / "serveur.py").write_text(source, encoding="utf-8")
    u = compte.nom if compte else settings.kaggle_username
    # Propriétaire des poids et du socle : un 2e compte Kaggle (voix en parallèle, 11 novembre 2026) pousse
    # le kernel sous son nom mais lit les notebooks partagés par le compte principal.
    p = settings.kaggle_sources_proprietaire or settings.kaggle_username
    sources = [f"{p}/{settings.kaggle_tts_modele}"]
    if settings.kaggle_tts_socle:
        sources.append(f"{p}/{settings.kaggle_tts_socle}")
    if settings.kaggle_stt_modele and settings.kaggle_stt_source:
        sources.append(f"{p}/{settings.kaggle_stt_source}")   # poids MoulSot affinés
    kernel = kernel or settings.kaggle_tts_kernel
    meta = {"id": f"{u}/{kernel}", "title": kernel,
            "code_file": "serveur.py", "language": "python", "kernel_type": "script",
            "is_private": True, "enable_gpu": True, "enable_internet": True,
            "machine_shape": "NvidiaTeslaT4", "dataset_sources": [], "competition_sources": [],
            "kernel_sources": sources}
    (dossier / "kernel-metadata.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    return dossier


def kaggle_cli(*args: str, timeout: float = 120, compte: Optional[CompteKaggle] = None) -> str:
    env = {**os.environ, "KAGGLE_USERNAME": compte.nom if compte else settings.kaggle_username,
           "KAGGLE_API_TOKEN": compte.jeton_api if compte else settings.kaggle_api_token}
    r = subprocess.run([sys.executable, "-m", "kaggle", *args], capture_output=True, text=True,
                       timeout=timeout, env=env)
    sortie = (r.stdout + r.stderr).strip()
    if r.returncode:
        raise RuntimeError(sortie[-600:] or f"kaggle {args[0]} : code {r.returncode}")
    return sortie


def pousser_kernel(cle: str, lancement: str, jeton: str, kernel: Optional[str] = None,
                   compte: Optional[CompteKaggle] = None) -> str:
    dossier = Path(tempfile.mkdtemp(prefix="kaggle_tts_"))
    try:
        construire_kernel(dossier, cle, lancement, jeton, kernel, compte)
        # Filet de sécurité côté Kaggle : même si la veille du kernel échouait,
        # Kaggle le couperait peu après la durée maximale.
        return kaggle_cli("kernels", "push", "-p", str(dossier),
                          "-t", str(settings.kaggle_tts_duree_max_s + 600), compte=compte)
    finally:
        shutil.rmtree(dossier, ignore_errors=True)


async def _garder(url: str, jeton: str):
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10.0) as c:
            await c.post(f"{url}/garder", headers={"Authorization": f"Bearer {jeton}"})
    except Exception:
        pass


async def _sante(url: str, jeton: str) -> bool:
    import httpx
    try:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(f"{url}/health", headers={"Authorization": f"Bearer {jeton}"})
        return r.status_code == 200
    except Exception:
        return False


pilote = PiloteKaggle()
