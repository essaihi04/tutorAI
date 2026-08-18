"""
TTS Service with language-aware router and filesystem cache.

Routing strategy (server-side only, no browser Web Speech API):
  - `fr`      → Google Cloud TTS Standard (fr-FR)  ~$4 / 1M chars
  - `ar`      → Google Cloud TTS Standard (ar-XA)  ~$4 / 1M chars
  - `mixed`   → Hybrid Darija:
                  * short / key phrases  → Gemini 2.5 Flash TTS (authentic voice)
                  * long explanations    → Google Cloud TTS ar-XA (MSA fallback)
                  * Gemini failure       → auto-fallback to Google Cloud ar-XA

A shared filesystem cache keyed by md5(provider|voice|lang|text) avoids
re-synthesising recurring phrases (openings, transitions, QCM feedback …).
"""
from __future__ import annotations

import base64
import hashlib
import os
import re
import struct
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import unquote

import asyncio

import httpx

from app.config import get_settings
from app.services.speech_normalizer import normalize_for_speech


settings = get_settings()


def _safe_log(*parts):
    message = " ".join(str(p) for p in parts)
    try:
        print(message)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        print(message.encode(enc, errors="replace").decode(enc, errors="replace"))


# ─── Text sanitization ───────────────────────────────────────────────
# Strip content that must not be spoken (markup and icons). Math is preserved
# so speech_normalizer can turn it into words instead of dropping it.

_TAG_PATTERNS = [
    re.compile(r"<board>.*?</board>", re.DOTALL | re.IGNORECASE),
    re.compile(r"<ui>.*?</ui>", re.DOTALL | re.IGNORECASE),
    re.compile(r"<schema>.*?</schema>", re.DOTALL | re.IGNORECASE),
    re.compile(r"<draw>.*?</draw>", re.DOTALL | re.IGNORECASE),
    re.compile(r"<suggestions>.*?</suggestions>", re.DOTALL | re.IGNORECASE),
    re.compile(r"<[A-Za-z/][^>]*>"),             # any other html-like tag
    re.compile(r"\[src:[^\]]+\]"),               # citation markers
    re.compile(r"`[^`\n]+`"),                    # inline code
    re.compile(r"```[\s\S]+?```"),               # code blocks
    re.compile(r"[📚📝📊📈📉✏️✅❌⚠️💡🎯🔥⭐️✨🚀👍👎💬🧠📖📘📙❓❗️]"),
]

_MULTISPACE_RE = re.compile(r"[ \t]{2,}")
_MULTINEWLINE_RE = re.compile(r"\n{3,}")

# Marqueurs de diction compris par le modèle Academy ([pause] pour respirer,
# [hes], [breath], [laugh]). Les autres moteurs les liraient à voix haute
# (« crochet pause »…) : on les retire avant de leur envoyer le texte.
_VOICE_MARKER_RE = re.compile(r"\[(?:pause|hes|breath|laugh)\]", re.IGNORECASE)


def _ensure_terminal_period(text: str) -> str:
    """Give the final spoken sentence a natural falling intonation."""
    stripped = (text or "").rstrip()
    if stripped and stripped[-1] not in ".!?؟؛。！？…":
        return stripped + "."
    return stripped


def strip_voice_markers(text: str) -> str:
    """Retire les marqueurs de diction — pour tout moteur SAUF Academy."""
    if not text:
        return ""
    return _MULTISPACE_RE.sub(" ", _VOICE_MARKER_RE.sub(" ", text)).strip()


def clean_for_tts(text: str) -> str:
    """Remove non-spoken markup while preserving math for normalization."""
    if not text:
        return ""
    out = text
    for pat in _TAG_PATTERNS:
        out = pat.sub(" ", out)
    # Markdown headings/emphasis. Preserve mathematical `*` and `_` when they
    # are not paired formatting markers (1.5 * 10^-3, H_2O).
    out = re.sub(r"(?m)^\s*#{1,6}\s*", "", out)
    out = out.replace("**", "").replace("__", "").replace("~~", "")
    out = re.sub(r"(?<!\w)[*_~](?=\w)|(?<=\w)[*_~](?!\w)", "", out)
    out = re.sub(r"^\s*\|.*\|\s*$", "", out, flags=re.MULTILINE)
    out = _MULTISPACE_RE.sub(" ", out)
    out = _MULTINEWLINE_RE.sub("\n\n", out)
    return out.strip()


# ─── Cache ───────────────────────────────────────────────────────────

@dataclass
class TTSResult:
    audio_b64: Optional[str]   # base64-encoded audio (None if use_browser)
    mime: str                  # "audio/mpeg" or "audio/wav"
    provider: str              # "browser" | "gemini" | "google_cloud"
    use_browser: bool = False  # True → frontend should call Web Speech API
    cached: bool = False


class _TTSCache:
    def __init__(self, root: Path, max_bytes: int):
        self.root = root
        self.max_bytes = max_bytes
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _key(provider: str, voice: str, lang: str, text: str) -> str:
        h = hashlib.md5(f"{provider}|{voice}|{lang}|{text}".encode("utf-8")).hexdigest()
        return h

    def _path(self, provider: str, voice: str, lang: str, text: str, ext: str) -> Path:
        return self.root / f"{self._key(provider, voice, lang, text)}.{ext}"

    def get(self, provider: str, voice: str, lang: str, text: str, ext: str) -> Optional[bytes]:
        p = self._path(provider, voice, lang, text, ext)
        if not p.exists():
            return None
        try:
            os.utime(p, None)  # LRU touch
            return p.read_bytes()
        except OSError:
            return None

    def put(self, provider: str, voice: str, lang: str, text: str, ext: str, data: bytes):
        p = self._path(provider, voice, lang, text, ext)
        try:
            p.write_bytes(data)
            self._evict_if_needed()
        except OSError as e:
            _safe_log(f"[TTS] Cache write failed: {e}")

    def _evict_if_needed(self):
        try:
            entries = [(p, p.stat()) for p in self.root.glob("*")]
            total = sum(s.st_size for _, s in entries)
            if total <= self.max_bytes:
                return
            # LRU eviction: oldest mtime first
            entries.sort(key=lambda e: e[1].st_mtime)
            for p, st in entries:
                if total <= self.max_bytes:
                    break
                total -= st.st_size
                try:
                    p.unlink()
                except OSError:
                    pass
        except OSError:
            pass


_cache: Optional[_TTSCache] = None


def _get_cache() -> Optional[_TTSCache]:
    global _cache
    if not settings.tts_cache_enabled:
        return None
    if _cache is None:
        root = Path(settings.tts_cache_dir)
        if not root.is_absolute():
            root = Path(__file__).resolve().parents[2] / settings.tts_cache_dir
        _cache = _TTSCache(root, settings.tts_cache_max_bytes)
    return _cache


# ─── Provider: Gemini 2.5 Flash Native Audio ─────────────────────────
# Used for Darija (mixed). Returns 16-bit PCM at 24 kHz → we wrap in WAV.

_GEMINI_TTS_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent?key={key}"
)


def _pcm_to_wav(pcm: bytes, sample_rate: int = 24000, channels: int = 1, bits: int = 16) -> bytes:
    """Wrap raw PCM bytes in a minimal WAV header."""
    byte_rate = sample_rate * channels * bits // 8
    block_align = channels * bits // 8
    data_size = len(pcm)
    return (
        b"RIFF"
        + struct.pack("<I", 36 + data_size)
        + b"WAVE"
        + b"fmt "
        + struct.pack("<IHHIIHH", 16, 1, channels, sample_rate, byte_rate, block_align, bits)
        + b"data"
        + struct.pack("<I", data_size)
        + pcm
    )


_GEMINI_STYLE = (
    "You are a warm, pedagogical Moroccan BAC teacher. "
    "Read the text naturally in darija marocaine when in Arabic script. "
    "Pronounce Latin-script scientific terms (la vitesse, la dérivée, "
    "la force, etc.) with a standard French accent, without translating them. "
    "Keep a clear, calm, encouraging delivery."
)


# Circuit breaker: when Gemini is over quota we must stop hitting it for a
# while, otherwise every 429 still counts against the quota and every segment
# wastes ~1s of latency waiting for the error. While the breaker is open,
# _route_with_breaker() sends mixed traffic to Google Cloud ar-XA.
_GEMINI_COOLDOWN_UNTIL: float = 0.0
_GEMINI_COOLDOWN_SECONDS = 60.0


def _gemini_is_available() -> bool:
    return time.time() >= _GEMINI_COOLDOWN_UNTIL


def _trip_gemini_breaker(reason: str):
    global _GEMINI_COOLDOWN_UNTIL
    _GEMINI_COOLDOWN_UNTIL = time.time() + _GEMINI_COOLDOWN_SECONDS
    _safe_log(
        f"[TTS] Gemini circuit breaker OPEN for {_GEMINI_COOLDOWN_SECONDS:.0f}s "
        f"(reason: {reason}) — routing to Google Cloud ar-XA"
    )


async def _synthesize_gemini(text: str, lang: str) -> Optional[bytes]:
    """Call Gemini 2.5 Flash TTS. Returns WAV bytes or None on error."""
    text = strip_voice_markers(text)
    key = settings.gemini_tts_api_key
    if not key:
        _safe_log("[TTS] Gemini TTS skipped: no API key")
        return None

    if not _gemini_is_available():
        # Breaker is open — don't waste a call
        return None

    url = _GEMINI_TTS_URL.format(model=settings.gemini_tts_model, key=key)

    # Gemini 2.5 Flash preview TTS expects an inline style prefix like
    # "Say warmly: <text>" (not systemInstruction). Keep the prefix short.
    styled_text = f"Dis chaleureusement: {text}"

    payload = {
        "contents": [{"parts": [{"text": styled_text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {"voiceName": settings.gemini_tts_voice}
                }
            },
        },
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
        if resp.status_code != 200:
            _safe_log(f"[TTS][Gemini] HTTP {resp.status_code}: {resp.text[:200]}")
            if resp.status_code == 429:
                _trip_gemini_breaker("HTTP 429 quota exceeded")
            return None
        data = resp.json()
        parts = (
            data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [])
        )
        for part in parts:
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                pcm = base64.b64decode(inline["data"])
                return _pcm_to_wav(pcm)
        _safe_log(f"[TTS][Gemini] No audio in response: {str(data)[:200]}")
        return None
    except Exception as e:
        _safe_log(f"[TTS][Gemini] Exception: {e}")
        return None


# ─── Provider: Google Cloud TTS Standard ─────────────────────────────

_GCLOUD_TTS_URL = "https://texttospeech.googleapis.com/v1/text:synthesize?key={key}"


async def _synthesize_google_cloud(text: str, lang: str) -> Optional[bytes]:
    """Call Google Cloud TTS Standard. Returns MP3 bytes or None."""
    text = strip_voice_markers(text)
    key = settings.google_cloud_tts_api_key or settings.gemini_tts_api_key
    if not key:
        _safe_log("[TTS] Google Cloud TTS skipped: no API key")
        return None

    if lang == "ar":
        voice_name = settings.google_cloud_tts_voice_ar
        lang_code = "ar-XA"
    else:
        voice_name = settings.google_cloud_tts_voice_fr
        lang_code = "fr-FR"

    url = _GCLOUD_TTS_URL.format(key=key)
    payload = {
        "input": {"text": text},
        "voice": {"languageCode": lang_code, "name": voice_name},
        # 0.9 : un eleve qui decouvre la notion a besoin du temps de la
        # comprendre pendant qu'elle est dite. En dessous de 0.85 la voix
        # devient trainante et l'attention decroche.
        "audioConfig": {"audioEncoding": "MP3", "speakingRate": 0.9},
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
        if resp.status_code != 200:
            _safe_log(f"[TTS][GCloud] HTTP {resp.status_code}: {resp.text[:200]}")
            return None
        body = resp.json()
        b64 = body.get("audioContent")
        if not b64:
            return None
        return base64.b64decode(b64)
    except Exception as e:
        _safe_log(f"[TTS][GCloud] Exception: {e}")
        return None


# ─── Provider: Academy Darija-FR TTS (self-hosted, Colab + tunnel) ──
#
# Modèle fine-tuné maison (voix « prof »), exposé par une petite API FastAPI :
#   POST {base}/tts   header `Authorization: Bearer <jeton>`
#         body {"texte": …, "langue": "ma"|"darija"|"fr", "voix": …,
#               "normaliser": true, "exaggeration", "temperature", "cfg_weight"}
#         → renvoie directement les octets WAV (audio/wav)
#   GET  {base}/health   → {"statut":"ok","device":"cuda","voix":[…]}
#   GET  {base}/voices   → identifiants de voix disponibles
#
# C'est le provider PRIORITAIRE : gratuit, voix du professeur, sans quota.
# L'URL du tunnel change à chaque redémarrage du notebook → elle vit dans
# backend/.env (ACADEMY_TTS_URL / ACADEMY_TTS_TOKEN), jamais dans le code.
#
# Contrat du modèle (contraintes fortes) :
#   • le tunnel ngrok en offre gratuite renvoie une PAGE HTML d'avertissement
#     à toute requête qu'il prend pour un navigateur → l'en-tête
#     `ngrok-skip-browser-warning` est OBLIGATOIRE sur tous les appels, et on
#     vérifie le Content-Type avant de considérer le corps comme du WAV ;
#   • 5 000 caractères maximum par requête ;
#   • `normaliser` applique l'orthographe darija (ال → ل) sur les lettres
#     lunaires ; les solaires non traitées reviennent dans l'en-tête
#     `X-A-Verifier` (on les journalise pour pouvoir corriger le texte source) ;
#   • exaggeration > 0.6 dérive sur les phrases longues — d'où le défaut 0.45.

_ACADEMY_COOLDOWN_UNTIL: float = 0.0
_ACADEMY_COOLDOWN_SECONDS = 120.0   # le temps qu'un Colab tombé redémarre

# Le GPU Colab traite UN job à la fois : sérialiser les appels évite que les
# segments lancés en parallèle expirent tous dans la file d'attente.
_ACADEMY_SEM = asyncio.Semaphore(1)

# Un 500 isolé arrive quand le GPU vient d'enchaîner un autre job : ce n'est
# PAS une panne. On ne coupe le provider qu'après plusieurs échecs d'affilée,
# sinon un simple à-coup nous priverait de la voix du prof pendant 2 minutes.
_ACADEMY_FAILS = 0
_ACADEMY_MAX_FAILS = 3


def _academy_is_available() -> bool:
    return (
        bool(settings.academy_tts_url)
        and time.time() >= _ACADEMY_COOLDOWN_UNTIL
    )


def _academy_note_success():
    global _ACADEMY_FAILS
    _ACADEMY_FAILS = 0


def _retry_after_seconds(resp: "httpx.Response", default: float = 45.0) -> float:
    """Combien de temps le serveur nous demande d'attendre, en secondes.

    Il l'annonce dans `Retry-After` (secondes) et double l'info dans
    `X-Attente` / `attente_estimee_s`. On borne : un en-tête absurde ne doit
    pas nous couper la voix du prof pendant une heure.
    """
    for header in ("Retry-After", "X-Attente"):
        raw = resp.headers.get(header)
        if not raw:
            continue
        try:
            return max(1.0, min(float(raw), 300.0))
        except ValueError:
            continue
    return default


def _trip_academy_breaker(
    reason: str, *, immediate: bool = False, cooldown: Optional[float] = None
):
    """Ouvre le disjoncteur — tout de suite si la panne est certaine
    (jeton refusé, tunnel injoignable), sinon après plusieurs échecs.

    `cooldown` permet de respecter la durée annoncée par le serveur (503
    saturé) plutôt que notre forfait.
    """
    global _ACADEMY_COOLDOWN_UNTIL, _ACADEMY_FAILS
    _ACADEMY_FAILS += 1
    if not immediate and _ACADEMY_FAILS < _ACADEMY_MAX_FAILS:
        _safe_log(
            f"[TTS][Academy] Échec {_ACADEMY_FAILS}/{_ACADEMY_MAX_FAILS} "
            f"({reason}) — on garde le provider actif"
        )
        return
    delay = _ACADEMY_COOLDOWN_SECONDS if cooldown is None else cooldown
    _ACADEMY_COOLDOWN_UNTIL = time.time() + delay
    _ACADEMY_FAILS = 0
    _safe_log(
        f"[TTS][Academy] Circuit breaker OPEN for {delay:.0f}s (reason: {reason})"
    )


# Le modèle plafonne à 5 000 caractères par requête.
_ACADEMY_MAX_CHARS = 5000


def _academy_lang(lang: str) -> str:
    """Notre `mixed`/`ar` = darija (« ma » côté API) ; le reste = français.

    Le contrat précise qu'une phrase darija contenant des mots français
    (écrits en caractères latins) reste en `ma` — on ne bascule sur `fr`
    que pour un contenu réellement francophone.
    """
    return "fr" if lang == "fr" else "ma"


async def _synthesize_academy(text: str, lang: str) -> Optional[bytes]:
    """Appelle l'API Academy TTS. Renvoie les octets WAV, ou None en cas d'échec."""
    base = (settings.academy_tts_url or "").rstrip("/")
    if not base or not _academy_is_available():
        return None

    # Le serveur refuse au-delà de 5 000 caractères : on coupe à une frontière
    # de mot plutôt que de laisser partir une requête vouée à l'échec.
    if len(text) > _ACADEMY_MAX_CHARS:
        text = text[:_ACADEMY_MAX_CHARS].rsplit(" ", 1)[0]

    payload = {
        "texte": text,
        "langue": _academy_lang(lang),
        "normaliser": bool(settings.academy_tts_normaliser),
        "exaggeration": settings.academy_tts_exaggeration,
        "temperature": settings.academy_tts_temperature,
        "cfg_weight": settings.academy_tts_cfg_weight,
    }
    if settings.academy_tts_voice:
        payload["voix"] = settings.academy_tts_voice

    headers = {
        "Content-Type": "application/json",
        # Sans cet en-tête, ngrok (offre gratuite) sert une page HTML
        # d'avertissement à la place de l'audio.
        "ngrok-skip-browser-warning": "true",
    }
    if settings.academy_tts_token:
        headers["Authorization"] = f"Bearer {settings.academy_tts_token}"

    try:
        async with _ACADEMY_SEM:
            t0 = time.time()
            # Une tentative, puis UN essai de rattrapage : le GPU renvoie
            # parfois un 500 quand il vient juste de finir un autre segment.
            for attempt in (1, 2):
                async with httpx.AsyncClient(timeout=180.0) as client:
                    resp = await client.post(f"{base}/tts", json=payload, headers=headers)

                if resp.status_code == 200:
                    audio = resp.content
                    ctype = resp.headers.get("Content-Type", "")
                    # L'API renvoie du WAV brut ; un corps JSON (ou du HTML)
                    # signale une erreur applicative ou la page d'avertissement
                    # du tunnel ngrok — dans les deux cas ce n'est pas de l'audio.
                    if not ctype.startswith("audio") or not audio or not audio.startswith(b"RIFF"):
                        _safe_log(
                            f"[TTS][Academy] Réponse non-audio (Content-Type={ctype!r}): "
                            f"{audio[:120]!r}"
                        )
                        _trip_academy_breaker("réponse non-audio (page ngrok ?)")
                        return None
                    _academy_note_success()
                    # Lettres solaires que le normaliseur n'a pas pu traiter :
                    # le texte source gagnerait à être écrit en darija (لشمس
                    # plutôt que الشمس) — on le signale sans bloquer l'audio.
                    # Un en-tête HTTP ne transporte que du latin-1 : le serveur
                    # encode ces valeurs arabes en pourcent. Sans unquote on
                    # journaliserait « %D8%A7%D9%84… » au lieu des mots.
                    a_verifier = resp.headers.get("X-A-Verifier")
                    if a_verifier:
                        _safe_log(
                            "[TTS][Academy] À vérifier (orthographe darija): "
                            f"{unquote(a_verifier)[:200]}"
                        )
                    _safe_log(
                        f"[TTS][Academy] OK lang={lang} len={len(text)} "
                        f"bytes={len(audio)} t={int((time.time() - t0) * 1000)}ms"
                    )
                    return audio

                _safe_log(f"[TTS][Academy] HTTP {resp.status_code}: {resp.text[:200]}")

                # Une réponse HTML ne vient JAMAIS de l'API (qui ne parle que
                # JSON ou WAV) : c'est ngrok qui répond à sa place, donc le
                # tunnel est mort. Mesuré : Colab arrêté → 404 + page HTML,
                # alors que 404 signifie « voix inconnue » dans le contrat.
                # Sans ce test on attendrait 3 échecs avant de basculer, et on
                # chercherait une erreur de voix qui n'existe pas.
                if resp.headers.get("Content-Type", "").startswith("text/html"):
                    _trip_academy_breaker(
                        f"HTTP {resp.status_code} + HTML (tunnel ngrok éteint)",
                        immediate=True,
                    )
                    return None

                # 401/403 = jeton refusé : réessayer ne servirait à rien.
                if resp.status_code in (401, 403):
                    _trip_academy_breaker(
                        f"HTTP {resp.status_code} (jeton invalide ?)", immediate=True
                    )
                    return None
                # 502 = le Colab n'est pas allumé. C'est le cas NORMAL hors
                # session : inutile de marteler le tunnel, on passe au repli.
                if resp.status_code == 502:
                    _trip_academy_breaker("HTTP 502 (Colab éteint)", immediate=True)
                    return None
                # 503 = modèle en chargement OU serveur saturé. Le serveur
                # annonce lui-même combien de temps attendre (Retry-After /
                # X-Attente) : on le RESPECTE au lieu d'appliquer notre
                # cooldown forfaitaire. Réessayer plus tôt aggraverait très
                # exactement la saturation dont on souffre — le compteur
                # `refusees` de /health montre que c'est un risque réel.
                if resp.status_code == 503:
                    wait = _retry_after_seconds(resp)
                    _trip_academy_breaker(
                        f"HTTP 503 (chargement ou saturation, attente {wait:.0f}s)",
                        immediate=True,
                        cooldown=wait,
                    )
                    return None
                # 404 (JSON) = la voix demandée n'existe pas sur ce
                # checkpoint. Réessayer est inutile et le message générique
                # « HTTP 404 » masque la vraie cause : on la nomme, car le
                # symptôme visible est « plus aucun son » côté élève.
                if resp.status_code == 404:
                    _trip_academy_breaker(
                        f"HTTP 404 — voix ACADEMY_TTS_VOICE="
                        f"{settings.academy_tts_voice!r} refusée par le serveur "
                        f"({resp.text[:120]})",
                        immediate=True,
                    )
                    return None
                # 422 = ce fragment précis est illisible pour le modèle. Le
                # serveur va très bien : on abandonne CE segment sans pénaliser
                # le provider (sinon un mot bizarre nous coupe la voix 2 min).
                if resp.status_code == 422:
                    _safe_log("[TTS][Academy] Fragment illisible (422) — segment abandonné")
                    return None
                if resp.status_code >= 500 and attempt == 1:
                    await asyncio.sleep(1.5)   # laisse le GPU se libérer
                    continue
                _trip_academy_breaker(f"HTTP {resp.status_code}")
                return None
            return None
    except httpx.ConnectError:
        _trip_academy_breaker("Colab injoignable (ConnectError)", immediate=True)
        return None
    except httpx.ReadTimeout:
        _trip_academy_breaker("Colab timeout (ReadTimeout)")
        return None
    except Exception as e:
        _safe_log(f"[TTS][Academy] Exception: {e}")
        return None


# ─── Academy en flux continu — le chemin à faible latence ──────────
#
# `/tts` ne rend la main qu'une fois le segment ENTIER synthétisé : pour dix
# secondes d'audio, l'élève attend dix secondes avant d'entendre la première
# syllabe. `/tts/stream` émet le PCM par blocs dès le début de la génération
# (40 jetons ≈ 1,6 s d'audio côté serveur).
#
# C'est LÀ que se joue le passage de « secondes » à « dizaines de
# millisecondes » — pas dans le transport. Le base64 sur WebSocket coûte 33 %
# de débit, ce qui est invisible à côté d'une attente de segment complet.
#
# Deux pièges documentés par le serveur, dont ce code tient compte :
#   - la taille annoncée dans l'en-tête WAV est FAUSSE (0xFFFFFFFF) : il faut
#     lire jusqu'à la fin du flux, jamais se fier au Content-Length ;
#   - le code HTTP part AVANT la synthèse : une panne en cours de route ne
#     peut plus devenir un 500, le flux se termine simplement plus tôt.
_ENTETE_WAV = 44        # RIFF + fmt + data, taille fixe côté serveur

# Taille de regroupement des blocs PCM. Le premier part IMMÉDIATEMENT (c'est
# tout l'intérêt), les suivants sont agrégés : 8 192 octets = 4 096
# échantillons ≈ 170 ms à 24 kHz. Assez gros pour ne pas noyer le WebSocket
# sous les messages, assez petit pour que le lecteur ne manque jamais d'avance.
_PCM_BLOC_MIN = 8192

# Délai maximal avant le PREMIER son. Le serveur annonce lui-même une attente
# plafond de 45 s (`attente_max_s` dans /health) ; au-delà, sa file est
# engorgée et insister ne fait que l'aggraver. Mesuré une fois à 194 s derrière
# une file saturée : inacceptable en cours, et le timeout httpx de 300 s
# laissait passer. Tant qu'aucun octet audio n'est parti, abandonner est SANS
# RISQUE — l'appelant se rabat sur /tts et l'élève entend quelque chose.
_PREMIER_SON_MAX_S = 50.0


async def stream_academy_pcm(text: str, lang: str):
    """Rend `(sample_rate, pcm_s16le)` au fil de la synthèse Academy.

    Générateur VIDE si Academy est indisponible ou si le flux échoue avant le
    premier octet audio : l'appelant retombe alors sur le chemin par segments
    complets, qui reste inchangé.

    Une fois le premier bloc rendu, un incident ne peut plus faire l'objet
    d'un repli — le flux s'arrête simplement plus court, comme le prévoit le
    contrat du serveur.
    """
    base = (settings.academy_tts_url or "").rstrip("/")
    if not base or not _academy_is_available() or not settings.academy_tts_stream:
        return

    text = strip_voice_markers(text)
    # Le flux PCM rapide recevait auparavant le texte brut, alors que le
    # chemin /tts passait par normalize_for_speech. Cela faisait lire à
    # Academy les chiffres, les unités et « N = 1/T » caractère par caractère.
    # Les deux chemins doivent envoyer exactement la même copie prononçable.
    text = _ensure_terminal_period(normalize_for_speech(text, lang))
    if not text.strip():
        return
    if len(text) > _ACADEMY_MAX_CHARS:
        text = text[:_ACADEMY_MAX_CHARS].rsplit(" ", 1)[0]

    payload = {
        "texte": text,
        "langue": _academy_lang(lang),
        "normaliser": bool(settings.academy_tts_normaliser),
        "exaggeration": settings.academy_tts_exaggeration,
        "temperature": settings.academy_tts_temperature,
        "cfg_weight": settings.academy_tts_cfg_weight,
    }
    if settings.academy_tts_voice:
        payload["voix"] = settings.academy_tts_voice

    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true",
    }
    if settings.academy_tts_token:
        headers["Authorization"] = f"Bearer {settings.academy_tts_token}"

    t0 = time.time()
    sr = 24000
    entete_lu = False
    tampon = b""            # octets pas encore rendus (dont l'en-tête)
    en_attente = b""        # blocs agrégés en attente de la taille minimale
    premier_rendu = False
    octets = 0

    try:
        # Le GPU ne traite qu'une synthèse à la fois : deux flux simultanés se
        # hacheraient mutuellement. Le sémaphore est le même que pour /tts.
        async with _ACADEMY_SEM:
            timeout = httpx.Timeout(300.0, connect=15.0)
            async with httpx.AsyncClient(timeout=timeout) as client:
                async with client.stream(
                    "POST", f"{base}/tts/stream", json=payload, headers=headers
                ) as resp:
                    if resp.status_code != 200:
                        corps = (await resp.aread())[:200]
                        _safe_log(
                            f"[TTS][Academy][flux] HTTP {resp.status_code}: {corps!r}"
                        )
                        # Un flux refusé n'est PAS une panne du provider : le
                        # serveur peut très bien servir /tts (streaming coupé,
                        # file saturée…). On laisse donc le disjoncteur fermé
                        # et le repli par segments décidera lui-même.
                        return

                    ctype = resp.headers.get("Content-Type", "")
                    if not ctype.startswith("audio"):
                        _safe_log(
                            f"[TTS][Academy][flux] Réponse non-audio "
                            f"(Content-Type={ctype!r})"
                        )
                        return

                    flux_octets = resp.aiter_bytes()
                    while True:
                        # Avant le premier son, on borne l'attente nous-mêmes :
                        # le serveur envoie son en-tête WAV immédiatement puis
                        # se tait tant que le GPU ne s'est pas libéré, si bien
                        # qu'un timeout de lecture classique ne se déclenche
                        # jamais pendant l'attente en file.
                        try:
                            if premier_rendu:
                                morceau = await flux_octets.__anext__()
                            else:
                                reste_s = _PREMIER_SON_MAX_S - (time.time() - t0)
                                if reste_s <= 0:
                                    raise asyncio.TimeoutError
                                morceau = await asyncio.wait_for(
                                    flux_octets.__anext__(), timeout=reste_s
                                )
                        except StopAsyncIteration:
                            break
                        except asyncio.TimeoutError:
                            _safe_log(
                                f"[TTS][Academy][flux] pas de son après "
                                f"{_PREMIER_SON_MAX_S:.0f} s (file engorgée ?) "
                                f"— repli sur /tts"
                            )
                            return

                        if not morceau:
                            continue
                        tampon += morceau

                        if not entete_lu:
                            if len(tampon) < _ENTETE_WAV:
                                continue
                            if not tampon.startswith(b"RIFF"):
                                _safe_log(
                                    "[TTS][Academy][flux] En-tête non-RIFF — "
                                    "flux abandonné"
                                )
                                return
                            # Le débit réel est annoncé dans l'en-tête : on ne
                            # présume pas 24 kHz, un checkpoint peut changer.
                            sr = int.from_bytes(tampon[24:28], "little") or 24000
                            tampon = tampon[_ENTETE_WAV:]
                            entete_lu = True

                        # PCM 16 bits : un échantillon ne doit jamais être coupé
                        # en deux entre deux messages, sinon tout le reste du
                        # flux est décalé d'un octet et devient du bruit blanc.
                        pair = len(tampon) - (len(tampon) % 2)
                        if not pair:
                            continue
                        en_attente += tampon[:pair]
                        tampon = tampon[pair:]

                        # Le tout premier bloc part sans attendre : c'est lui
                        # qui fait la latence perçue.
                        if not premier_rendu:
                            _safe_log(
                                f"[TTS][Academy][flux] premier son en "
                                f"{int((time.time() - t0) * 1000)} ms"
                            )
                            _academy_note_success()
                            premier_rendu = True
                            octets += len(en_attente)
                            yield sr, en_attente
                            en_attente = b""
                        elif len(en_attente) >= _PCM_BLOC_MIN:
                            octets += len(en_attente)
                            yield sr, en_attente
                            en_attente = b""

                    if en_attente:
                        octets += len(en_attente)
                        yield sr, en_attente
    except (httpx.ConnectError, httpx.ReadTimeout) as e:
        # Avant le premier octet, l'appelant peut encore se rabattre sur /tts,
        # qui déclenchera lui-même le disjoncteur si la panne est réelle.
        _safe_log(f"[TTS][Academy][flux] {type(e).__name__} — repli sur /tts")
        return
    except Exception as e:
        # Coupure EN COURS de flux : mesurée sur le tunnel ngrok gratuit
        # (« peer closed connection without sending complete message body »).
        # L'élève a déjà entendu le début, donc on ne peut plus rejouer la
        # phrase sans la lui dire deux fois — on le signale clairement, c'est
        # le symptôme à reconnaître si une explication s'arrête au milieu.
        if premier_rendu:
            duree = octets / 2 / sr if sr else 0.0
            _safe_log(
                f"[TTS][Academy][flux] /!\\ FLUX TRONQUÉ après {duree:.1f}s "
                f"d'audio ({type(e).__name__}) — la fin de la phrase est perdue"
            )
        else:
            _safe_log(f"[TTS][Academy][flux] Exception: {type(e).__name__}: {e}")
        return

    if premier_rendu:
        duree = octets / 2 / sr if sr else 0.0
        _safe_log(
            f"[TTS][Academy][flux] OK lang={lang} len={len(text)} "
            f"audio={duree:.1f}s total={int((time.time() - t0) * 1000)}ms"
        )


# ─── Provider: Self-hosted Darija TTS (Gradio on Colab) ─────────────
#
# Calls the Gradio /generate endpoint using the SSE v3 protocol:
#   1. POST /gradio_api/call/generate  →  get event_id
#   2. GET  /gradio_api/call/generate/{event_id}  →  SSE stream with result
#   3. Parse the FileData URL from the result data
#   4. Download the audio file bytes
#
# The endpoint returns WAV audio at 44100 Hz from the Darija fine-tuned
# model (Chatterbox or similar). This is FREE, fast (~2-5s), and has no
# quota limit (only limited by the Colab GPU).

# Circuit breaker for Gradio endpoint (Colab can go down / disconnect)
_GRADIO_COOLDOWN_UNTIL: float = 0.0
_GRADIO_COOLDOWN_SECONDS = 120.0   # Colab reconnect takes ~2 min

# Semaphore: Colab GPU processes one TTS job at a time, so we must
# serialize calls to avoid timeouts when segments are launched in parallel.
_GRADIO_SEM = asyncio.Semaphore(1)


def _gradio_is_available() -> bool:
    return (
        bool(settings.gradio_tts_url)
        and time.time() >= _GRADIO_COOLDOWN_UNTIL
    )


def _trip_gradio_breaker(reason: str):
    global _GRADIO_COOLDOWN_UNTIL
    _GRADIO_COOLDOWN_UNTIL = time.time() + _GRADIO_COOLDOWN_SECONDS
    _safe_log(
        f"[TTS][Gradio] Circuit breaker OPEN for {_GRADIO_COOLDOWN_SECONDS:.0f}s "
        f"(reason: {reason})"
    )


async def _synthesize_gradio(text: str, lang: str) -> Optional[bytes]:
    """Call the self-hosted Darija TTS via Gradio API. Returns WAV bytes or None.

    Uses _GRADIO_SEM (concurrency=1) because Colab GPU handles one job at
    a time. Without this, parallel segment tasks all hit the endpoint
    together and the 2nd+ ones timeout waiting in the Gradio queue.
    """
    text = strip_voice_markers(text)
    base = settings.gradio_tts_url.rstrip("/")
    if not base:
        return None
    if not _gradio_is_available():
        return None

    call_url = f"{base}/gradio_api/call/generate"
    payload = {
        "data": [
            text,
            settings.gradio_tts_exaggeration,
            settings.gradio_tts_temperature,
            settings.gradio_tts_cfg_weight,
        ]
    }

    try:
      async with _GRADIO_SEM:
        async with httpx.AsyncClient(timeout=180.0) as client:
            # Step 1: Submit the job
            t0 = time.time()
            resp = await client.post(call_url, json=payload)
            if resp.status_code != 200:
                _safe_log(f"[TTS][Gradio] POST {resp.status_code}: {resp.text[:200]}")
                if resp.status_code >= 500:
                    _trip_gradio_breaker(f"HTTP {resp.status_code}")
                return None
            event_id = resp.json().get("event_id")
            if not event_id:
                _safe_log("[TTS][Gradio] No event_id in POST response")
                return None

            # Step 2: Poll SSE for result
            sse_url = f"{call_url}/{event_id}"
            audio_url = None
            async with client.stream("GET", sse_url) as sse:
                event_type = ""
                async for line in sse.aiter_lines():
                    line = line.strip()
                    if line.startswith("event:"):
                        event_type = line[6:].strip()
                    elif line.startswith("data:") and event_type == "complete":
                        import json as _json
                        try:
                            data_list = _json.loads(line[5:].strip())
                            # data_list is [FileData_dict] where FileData has "url"
                            if isinstance(data_list, list) and data_list:
                                fd = data_list[0]
                                if isinstance(fd, dict):
                                    audio_url = fd.get("url") or fd.get("path")
                        except Exception:
                            pass
                        break
                    elif event_type == "error":
                        _safe_log(f"[TTS][Gradio] SSE error: {line}")
                        _trip_gradio_breaker("SSE error")
                        return None

            if not audio_url:
                _safe_log("[TTS][Gradio] No audio URL in SSE response")
                return None

            # Step 3: Download the audio file
            if audio_url.startswith("/"):
                audio_url = f"{base}{audio_url}"
            audio_resp = await client.get(audio_url)
            if audio_resp.status_code != 200:
                _safe_log(f"[TTS][Gradio] Audio download {audio_resp.status_code}")
                return None

            elapsed = int((time.time() - t0) * 1000)
            _safe_log(
                f"[TTS][Gradio] OK len={len(text)} bytes={len(audio_resp.content)} "
                f"t={elapsed}ms"
            )
            return audio_resp.content
    except httpx.ConnectError:
        _trip_gradio_breaker("Colab unreachable (ConnectError)")
        return None
    except httpx.ReadTimeout:
        _trip_gradio_breaker("Colab timeout (ReadTimeout)")
        return None
    except Exception as e:
        _safe_log(f"[TTS][Gradio] Exception: {e}")
        return None


# ─── Router ──────────────────────────────────────────────────────────
#
# Hybrid strategy for Darija (lang == "mixed"):
#
#   • Short phrases (≤ DARIJA_SHORT_CHARS) → Gemini 2.5 (authentic Darija voice)
#     Typical: openings, praise, pitfalls, transitions, micro-quizzes.
#   • Phrases containing a pedagogical trigger keyword, regardless of length
#     (up to DARIJA_KEY_MAX_CHARS) → Gemini 2.5
#   • Everything else → Google Cloud TTS ar-XA (MSA accent, ~40× cheaper)
#     Typical: long explanations, definitions, method steps.
#
# Expected cost reduction: ~5× vs. all-Gemini, while preserving the warm
# Darija voice on the moments that matter pedagogically.

# Gemini 2.5 preview TTS is authentic but SLOW (~10-12s per call), so we
# restrict it to tiny emotional interjections that are almost always served
# from the warmup cache (cost 0 ms). Anything longer goes to Google Cloud
# ar-XA which completes in ~1.5s — imperceptible vs. the whiteboard render.
DARIJA_SHORT_CHARS = 35           # only micro-phrases ("Bravo!", "مرحبا خويا")
DARIJA_KEY_MAX_CHARS = 60         # hard cap for marker-triggered Gemini routing

# Darija/Arabic/French pedagogical markers that justify the authentic voice
_DARIJA_KEY_MARKERS = (
    # praise / encouragement
    "bravo", "mzyan", "mezyan", "zwin", "ممتاز", "برافو", "مزيان", "زوين",
    # warning / pitfall
    "attention", "piège", "dir balek", "dir l-bal", "3ndak", "عندك", "انتبه",
    "الفخ", "خذ بالك", "خاصك",
    # hook / opener
    "salam", "yallah", "ajiw", "ajiwa", "akhi", "okhti", "سلام", "يلا", "أخي",
    "أختي", "نبداو", "نبدأ",
    # recap / summary
    "récap", "khulasa", "lkhulasa", "خلاصة", "نلخص", "تلخيص", "الخلاصة",
    # BAC / exam emphasis
    "bac", "examen", "الباك", "الامتحان", "سؤال", "question",
)


def _is_darija_key_phrase(text: str) -> bool:
    """Return True if the Darija text should use the authentic Gemini voice."""
    if not text:
        return False
    n = len(text)
    if n <= DARIJA_SHORT_CHARS:
        return True
    if n > DARIJA_KEY_MAX_CHARS:
        return False
    low = text.lower()
    return any(mk in low for mk in _DARIJA_KEY_MARKERS)


def _route(lang: str, text: str = "") -> tuple[str, str, str]:
    """Return (provider, voice, extension) for a given language + text.

    Priority order:
      1. Academy Darija-FR TTS (modèle fine-tuné maison, voix du professeur)
         → FREE, sans quota, gère darija ET français
      2. Self-hosted Darija TTS via Gradio (FREE, ~2-5s, no quota)
      3. Gemini 2.5 Flash TTS (authentic but 429-prone on free tier)
      4. Google Cloud TTS
         → emergency fallback only
    """
    # Notre modèle maison passe avant tout le reste (gratuit + voix du prof)
    if _academy_is_available():
        return ("academy", settings.academy_tts_voice or "prof", "wav")
    # Darija & Arabic → self-hosted Gradio TTS (Chatterbox on Colab)
    if lang in ("mixed", "ar") and _gradio_is_available():
        return ("gradio", "darija", "wav")
    # French → also try Gradio first (the model can handle French too)
    if _gradio_is_available():
        return ("gradio", "darija", "wav")
    # Fallback to Gemini
    if _gemini_is_available():
        return ("gemini", settings.gemini_tts_voice, "wav")
    # Last resort: Google Cloud
    if lang == "fr":
        return ("google_cloud", settings.google_cloud_tts_voice_fr, "mp3")
    return ("google_cloud", settings.google_cloud_tts_voice_ar, "mp3")


# ─── Intelligent hybrid pipeline ─────────────────────────────────────
#
# Rather than synthesising the full AI response in one provider call,
# we split it into natural segments, route each independently, run the
# calls in parallel and serve them as a stream of audio_chunk messages.
#
# Wins:
#   1. Per-sentence routing   → only short/key lines pay Gemini rates,
#                                long explanations pay ar-XA rates.
#   2. Parallel synthesis     → wall-clock latency drops to that of the
#                                slowest segment, not the sum.
#   3. Cache per segment      → hit rate explodes on recurring openings,
#                                transitions, praise, and pitfalls.
#   4. Failure isolation      → one segment failing doesn't kill the
#                                whole reply.

# Sentence-boundary regex for FR/AR/Darija: splits on terminal punctuation
# while keeping the punctuation attached to the preceding segment.
_SENTENCE_RE = re.compile(
    r"(?<=[\.\!\?\u061F\u06D4\u203C])\s+(?=\S)"  # . ! ? ؟ ۔ ‼
)

# Aggressive cache-key normalizer: collapses whitespace and strips trailing
# punctuation variants so "Bravo !", "Bravo!", "Bravo." all hit the same slot.
_TRAIL_PUNCT_RE = re.compile(r"[\s\.\!\?\u061F\u06D4]+$")


def _normalize_for_cache(text: str) -> str:
    if not text:
        return ""
    s = re.sub(r"\s+", " ", text).strip()
    s = _TRAIL_PUNCT_RE.sub("", s)
    return s


# Segment tuning — user preference: split audio into SMALL chunks so they
# synthesise in PARALLEL. Gemini TTS takes ~10 s per call regardless of
# length (up to ~500 chars), so 4 parallel calls of 80 chars finish in the
# same wall-clock as one call of 320 chars — but the student hears the
# first chunk sooner AND the response is resilient to any single-chunk
# failure.
_SEG_MIN_CHARS = 20          # avoid wasting API calls on 2-word fragments
_SEG_MAX_CHARS = 200         # keep each Gemini call short & focused
_SEG_MERGE_TARGET = 90       # aim for ~90-char chunks (~15-20 words)

# ── Academy TTS : un opener court, puis de gros blocs ──
#
# ⚠️ Ce dimensionnement a été REFAIT après la mise à jour du serveur (décodage
# `torch.compile`, visible dans /health : "decodage":"compile"). L'ancien
# réglage supposait une génération PLUS LENTE que le temps réel ; c'est faux
# depuis. Mesuré sur le tunnel, darija, cache froid, après un appel de chauffe
# (le premier appel paie la compilation) :
#
#     11 car. →  1,32 s d'audio en  1,34 s de calcul   (RTF 1,02)
#     33 car. →  2,48 s d'audio en  1,43 s de calcul   (RTF 0,58)
#     98 car. →  5,68 s d'audio en  2,44 s de calcul   (RTF 0,43)
#    205 car. → 13,33 s d'audio en  5,80 s de calcul   (RTF 0,44)
#    463 car. → 29,50 s d'audio en 12,38 s de calcul   (RTF 0,42)
#
#     régression :  calcul ≈ 0,40 × audio + 0,48 s
#     + ~1,4 à 2,8 s de tunnel ngrok par appel (aller-retour + transfert WAV)
#
# Deux faits en découlent, et ils inversent l'ancienne conclusion.
#
# 1. La génération est ~2,4× PLUS RAPIDE que le temps réel. Une fois la
#    lecture lancée, elle ne rattrape JAMAIS la génération : le tampon se
#    remplit tout seul. Le streaming est donc sans risque de coupure — ce
#    n'est plus une contrainte de dimensionnement.
#
# 2. Ce qui coûte, maintenant, c'est le FIXE par appel : ~0,5 s de calcul plus
#    ~1,4 s de tunnel. Chaque segment supplémentaire ajoute ~2 s au total.
#    Multiplier les petits segments RALLONGE la réponse — exactement le
#    contraire de ce que faisait l'ancien réglage à 110 caractères uniformes.
#
# D'où la forme retenue : un PREMIER segment court, puis de GROS blocs.
#   • l'opener court donne le premier son vite (~2,5 s de mur) ;
#   • les blocs suivants se génèrent 2,4× plus vite qu'ils ne se jouent, donc
#     ils arrivent tous en avance pendant que l'opener passe ;
#   • peu de blocs = peu de surcoût fixe = réponse totale plus courte.
#
# Un bloc large ne dégrade PAS la prosodie : le contrat du serveur précise
# qu'il redécoupe lui-même aux frontières de phrase (en-tête X-Morceaux) et
# concatène avec 0,25 s de silence. C'est même l'inverse — il recommande
# explicitement de NE PAS pré-découper. On lui laisse donc le travail.
_SEG_ACADEMY_FIRST_CHARS = 90     # opener : 1 phrase, ~5 s d'audio, ~2,5 s de mur
_SEG_ACADEMY_MAX_CHARS = 900      # blocs suivants (le serveur redécoupe dedans)


def split_into_segments(
    text: str,
    *,
    max_chars: int = _SEG_MAX_CHARS,
    merge_target: int = _SEG_MERGE_TARGET,
) -> list[str]:
    """Split text into TTS-friendly segments at sentence boundaries."""
    if not text:
        return []
    raw = _SENTENCE_RE.split(text.strip())
    # Merge tiny fragments with the previous one; hard-split segments > max.
    out: list[str] = []
    for piece in raw:
        piece = piece.strip()
        if not piece:
            continue
        if out and len(out[-1]) < _SEG_MIN_CHARS:
            out[-1] = (out[-1] + " " + piece).strip()
            continue
        if out and len(out[-1]) + len(piece) + 1 <= merge_target:
            # Merge short adjacent sentences toward target size
            out[-1] = (out[-1] + " " + piece).strip()
            continue
        if len(piece) > max_chars:
            # Hard split long run-on sentences on commas / semicolons
            chunks = re.split(r"(?<=[,;:\u060C])\s+", piece)
            buf = ""
            for c in chunks:
                if len(buf) + len(c) + 1 > max_chars:
                    if buf:
                        out.append(buf.strip())
                    buf = c
                else:
                    buf = (buf + " " + c).strip() if buf else c
            if buf:
                out.append(buf.strip())
        else:
            out.append(piece)
    return [s for s in out if s]


def split_for_academy(
    text: str,
    *,
    first_chars: int = _SEG_ACADEMY_FIRST_CHARS,
    max_chars: int = _SEG_ACADEMY_MAX_CHARS,
) -> list[str]:
    """Découpe en « opener court + gros blocs », aux frontières de phrase.

    Voir le bloc de mesures plus haut : le serveur génère 2,4× plus vite que
    le temps réel mais paie ~2 s de fixe par appel. On veut donc le MINIMUM
    d'appels, avec une seule exception — le premier, qu'on garde court pour
    que l'élève entende quelque chose tout de suite.
    """
    if not text:
        return []

    sentences = [s.strip() for s in _SENTENCE_RE.split(text.strip()) if s.strip()]
    if not sentences:
        return []

    out: list[str] = []
    buf = ""
    # Le premier bloc se ferme dès qu'il atteint `first_chars` ; les suivants
    # se remplissent jusqu'à `max_chars`.
    limit = first_chars

    for s in sentences:
        # Une phrase à elle seule plus longue que la limite part telle quelle :
        # la couper au milieu casserait la prosodie que le serveur sait gérer.
        if not buf and len(s) >= limit:
            out.append(s)
            limit = max_chars
            continue
        if buf and len(buf) + 1 + len(s) > limit:
            out.append(buf)
            buf = s
            limit = max_chars
            continue
        buf = f"{buf} {s}".strip()
        if len(buf) >= limit:
            out.append(buf)
            buf = ""
            limit = max_chars

    if buf:
        out.append(buf)
    return out


@dataclass
class TTSSegment:
    """One ready-to-play audio segment produced by the hybrid pipeline."""
    audio_b64: str
    mime: str
    provider: str
    language: str
    cached: bool
    text: str  # original text for frontend caption alignment


async def _synthesize_one_segment(
    text: str,
    language: str,
) -> Optional[TTSSegment]:
    """Route + cache + synth a single segment. Returns None on total failure."""
    display_text = clean_for_tts(text)
    if not display_text:
        return None
    spoken_text = _ensure_terminal_period(normalize_for_speech(display_text, language))
    if not spoken_text:
        return None
    cache_text = _normalize_for_cache(spoken_text)
    provider, voice, ext = _route(language, spoken_text)

    cache = _get_cache()
    if cache is not None:
        cached = cache.get(provider, voice, language, cache_text, ext)
        if cached:
            mime = "audio/wav" if ext == "wav" else "audio/mpeg"
            return TTSSegment(
                audio_b64=base64.b64encode(cached).decode("ascii"),
                mime=mime, provider=provider, language=language,
                cached=True, text=display_text,
            )

    audio_bytes: Optional[bytes] = None
    if provider == "academy":
        audio_bytes = await _synthesize_academy(spoken_text, language)
        if not audio_bytes:
            # Colab tombé → on redescend la chaîne de secours pour ce segment
            _safe_log("[TTS][seg] Academy fail → Gradio/Gemini fallback")
            audio_bytes = await _synthesize_gradio(spoken_text, language)
            if audio_bytes:
                provider, voice, ext = "gradio", "darija", "wav"
            else:
                audio_bytes = await _synthesize_gemini(spoken_text, language)
                if audio_bytes:
                    provider, voice, ext = "gemini", settings.gemini_tts_voice, "wav"
    elif provider == "gradio":
        audio_bytes = await _synthesize_gradio(spoken_text, language)
        if not audio_bytes:
            # Gradio failed → try Gemini as fallback for this segment
            _safe_log("[TTS][seg] Gradio fail → Gemini fallback")
            audio_bytes = await _synthesize_gemini(spoken_text, language)
            if audio_bytes:
                provider, voice, ext = "gemini", settings.gemini_tts_voice, "wav"
    elif provider == "gemini":
        audio_bytes = await _synthesize_gemini(spoken_text, language)
    elif provider == "google_cloud":
        audio_bytes = await _synthesize_google_cloud(spoken_text, language)

    if not audio_bytes:
        return None

    if cache is not None:
        cache.put(provider, voice, language, cache_text, ext, audio_bytes)

    mime = "audio/wav" if ext == "wav" else "audio/mpeg"
    return TTSSegment(
        audio_b64=base64.b64encode(audio_bytes).decode("ascii"),
        mime=mime, provider=provider, language=language,
        cached=False, text=display_text,
    )


async def synthesize_segments(text: str, language: str = "fr") -> list[TTSSegment]:
    """
    Split `text` into sentences, route each to the optimal provider,
    synthesise in parallel, and return the ordered list of audio segments.

    Kept for backward compatibility. Prefer `stream_synthesize_segments`
    to reduce perceived latency (student hears first sentence ASAP).
    """
    out: list[TTSSegment] = []
    async for _i, _total, seg in stream_synthesize_segments(text, language):
        out.append(seg)
    return out


async def stream_synthesize_segments(text: str, language: str = "fr"):
    """
    Async generator that yields `(index, total, TTSSegment)` tuples in the
    ORIGINAL order of the text, as soon as each segment is ready.

    All segments are synthesised in PARALLEL in the background; we simply
    await them in submission order so callers can stream audio_chunk
    messages progressively without re-ordering on the client side.

    Perceived latency: ≈ time-to-first-segment (not total) ≈ 2-3 s instead
    of the 10-15 s it used to take when waiting for the whole response.
    """
    if settings.tts_disabled:
        return
    cleaned = clean_for_tts(text)
    if not cleaned:
        return

    if len(cleaned) > 3000:
        cleaned = cleaned[:3000].rsplit(" ", 1)[0] + "…"

    # Le modèle Academy veut des textes longs entiers (il gère lui-même les
    # frontières de phrase) ; les providers cloud préfèrent de petits appels
    # parallélisables.
    if _academy_is_available():
        segments = split_for_academy(cleaned)
    else:
        segments = split_into_segments(cleaned)
    if not segments:
        return

    total = len(segments)
    t0 = time.time()

    # Launch ALL synthesis tasks immediately in parallel.
    tasks = [
        asyncio.create_task(_synthesize_one_segment(seg, language))
        for seg in segments
    ]

    stats = {"academy": 0, "gradio": 0, "gemini": 0, "google_cloud": 0, "cached": 0, "failed": 0}
    first_ms: Optional[int] = None

    try:
        for i, task in enumerate(tasks):
            try:
                seg = await task
            except Exception as e:
                _safe_log(f"[TTS][seg] task {i} exception: {e}")
                seg = None

            if seg is None:
                stats["failed"] += 1
                continue

            if first_ms is None:
                first_ms = int((time.time() - t0) * 1000)

            if seg.cached:
                stats["cached"] += 1
            stats[seg.provider] = stats.get(seg.provider, 0) + 1

            yield i, total, seg
    finally:
        # Ensure nothing leaks if the caller disconnects mid-stream.
        for t in tasks:
            if not t.done():
                t.cancel()

        elapsed_ms = int((time.time() - t0) * 1000)
        _safe_log(
            f"[TTS][stream] lang={language} segs={total} "
            f"first={first_ms}ms total={elapsed_ms}ms "
            f"cached={stats['cached']} academy={stats.get('academy', 0)} "
            f"gradio={stats.get('gradio', 0)} gemini={stats.get('gemini', 0)} "
            f"gcloud={stats.get('google_cloud', 0)} failed={stats['failed']}"
        )


async def synthesize(text: str, language: str = "fr") -> TTSResult:
    """
    Main entry point. Always returns server-synthesized audio bytes
    (Gemini 2.5 or Google Cloud TTS) — never defers to the browser.
    """
    if settings.tts_disabled:
        return TTSResult(audio_b64=None, mime="", provider="disabled", use_browser=False)

    display_text = clean_for_tts(text)
    if not display_text:
        return TTSResult(audio_b64=None, mime="", provider="empty", use_browser=False)
    spoken_text = _ensure_terminal_period(normalize_for_speech(display_text, language))
    if not spoken_text:
        return TTSResult(audio_b64=None, mime="", provider="empty", use_browser=False)

    # Cap length per request to avoid runaway cost (roughly 2 min of speech)
    if len(spoken_text) > 2500:
        spoken_text = spoken_text[:2500].rsplit(" ", 1)[0] + "…"

    provider, voice, ext = _route(language, spoken_text)

    if language == "mixed":
        _safe_log(
            f"[TTS][route] mixed → {provider} "
            f"(len={len(spoken_text)}, key={_is_darija_key_phrase(spoken_text)})"
        )

    # Cache hit?
    cache = _get_cache()
    if cache is not None:
        cached = cache.get(provider, voice, language, spoken_text, ext)
        if cached:
            mime = "audio/wav" if ext == "wav" else "audio/mpeg"
            return TTSResult(
                audio_b64=base64.b64encode(cached).decode("ascii"),
                mime=mime, provider=provider, use_browser=False, cached=True,
            )

    # Miss → synthesize (Gradio first, then Gemini, then GCloud)
    t0 = time.time()
    audio_bytes: Optional[bytes] = None
    if provider == "academy":
        audio_bytes = await _synthesize_academy(spoken_text, language)
        if not audio_bytes:
            audio_bytes = await _synthesize_gradio(spoken_text, language)
            if audio_bytes:
                provider, voice, ext = "gradio", "darija", "wav"
            else:
                audio_bytes = await _synthesize_gemini(spoken_text, language)
                if audio_bytes:
                    provider, voice, ext = "gemini", settings.gemini_tts_voice, "wav"
    elif provider == "gradio":
        audio_bytes = await _synthesize_gradio(spoken_text, language)
        if not audio_bytes:
            audio_bytes = await _synthesize_gemini(spoken_text, language)
            if audio_bytes:
                provider, voice, ext = "gemini", settings.gemini_tts_voice, "wav"
    elif provider == "gemini":
        audio_bytes = await _synthesize_gemini(spoken_text, language)
    elif provider == "google_cloud":
        audio_bytes = await _synthesize_google_cloud(spoken_text, language)

    if not audio_bytes:
        _safe_log(f"[TTS] All providers failed for lang={language}")
        return TTSResult(audio_b64=None, mime="", provider="failed",
                         use_browser=False, cached=False)

    elapsed_ms = int((time.time() - t0) * 1000)
    _safe_log(
        f"[TTS] {provider} lang={language} len={len(spoken_text)} "
        f"bytes={len(audio_bytes)} t={elapsed_ms}ms"
    )

    if cache is not None:
        cache.put(provider, voice, language, spoken_text, ext, audio_bytes)

    mime = "audio/wav" if ext == "wav" else "audio/mpeg"
    return TTSResult(
        audio_b64=base64.b64encode(audio_bytes).decode("ascii"),
        mime=mime, provider=provider, use_browser=False, cached=False,
    )


# ─── Precomputed-phrase warmup ───────────────────────────────────────
#
# A tiny curated list of phrases that the coach repeats constantly
# (hooks, praise, transitions, pitfalls, outros). Pregenerating them at
# startup pushes the steady-state cache hit rate to ~70-80% which in
# turn divides real-world TTS cost by ~3-4×.

_WARMUP_PHRASES: dict[str, list[str]] = {
    # French stays on Google Cloud (fast & cheap); keeping a small list is
    # enough because fr phrases rarely repeat character-for-character.
    "fr": [
        "Parfait, continuons.",
        "Très bien, on avance.",
        "Attention, voici un piège fréquent au BAC.",
        "Récapitulons les points clés.",
        "À ton tour maintenant.",
        "Excellente remarque.",
        "On passe à la suite.",
        "Relis attentivement l'énoncé.",
        "Voici la méthode à retenir.",
        "Prends ton temps.",
        "Tu peux le faire, je crois en toi.",
        "Essaie d'abord par toi-même.",
        "Qu'est-ce que tu en penses ?",
        "Explique-moi ton raisonnement.",
        "Pas de souci, on reprend ensemble.",
        "C'est exactement ça, bravo.",
        "Tu as bien compris, on passe au suivant.",
        "Regarde bien le tableau.",
        "Note cette formule, elle est essentielle.",
        "Cette étape est cruciale, ne l'oublie pas.",
    ],
    # Arabic MSA also stays on Google Cloud.
    "ar": [
        "ممتاز، نكملو.",
        "انتبه، هادي فخ ديال الباك.",
        "نلخصو النقط المهمة.",
        "دابا جاء دورك.",
        "ملاحظة زوينة.",
        "نعاودو الكرة.",
        "قرا النص مزيان.",
        "هاد المعادلة أساسية.",
        "جاوب بهدوء.",
        "فكر قبل ما تجاوب.",
        "احفظ هاد القاعدة.",
        "هاد النقطة مهمة بزاف.",
        "واش فهمتي؟",
        "عاود قرا السؤال.",
        "خذ وقتك.",
    ],
    # ── Darija (mixed) — this is THE list that matters for cost.
    # Every phrase here goes to Gemini ONCE at first warmup, then is served
    # from disk cache forever. The goal is 150+ lines that cover every
    # recurring pedagogical moment, so ~85% of runtime calls are cache hits.
    "mixed": [
        # ─── Greetings / openings ───
        "مرحبا خويا!",
        "مرحبا خويا، كيداير؟",
        "السلام عليكم، فين وصلنا؟",
        "أهلا بيك من جديد.",
        "مرحبا، يلا نبداو.",
        "أهلا، مستعد للدرس؟",
        "السلام، واش ليوم غادي نخدمو مزيان؟",
        "مرحبا أختي!",
        "صباح الخير، يلا نكملو.",
        "مرحبا، عاود شوف الدرس لي فات.",
        # ─── Praise / encouragement ───
        "برافو عليك!",
        "مزيان بزاف!",
        "ممتاز، هكذا!",
        "زوين الجواب.",
        "كتفهم مزيان.",
        "شحال كنت زوين ف هاد السؤال.",
        "هذا هو، برافو!",
        "كتقدم مزيان، كمل هكذا.",
        "أنا فخور بيك.",
        "واو، جواب ممتاز!",
        "ياك كنت عارف!",
        "بالضبط، هذا هو الجواب.",
        "تمام، كتخدم مزيان.",
        # ─── Scaffolding questions ───
        "واش فهمتي؟",
        "واش واضحة لعندك؟",
        "واش عندك شي سؤال؟",
        "واش كتتذكر الدرس لي فات؟",
        "شنو كتفهم من هاد الجملة؟",
        "قول ليا، شنو هي la définition؟",
        "تقدر تشرح ليا بكلماتك؟",
        "شنو غادي ندير دابا؟",
        "علاش هاد الخطوة مهمة؟",
        "كيفاش غادي نحسب هاد la valeur؟",
        "واش عندك فكرة كيفاش نبداو؟",
        "شنو هي la prochaine étape؟",
        "جرب، قول ليا شنو كاين ف بالك.",
        "واش الجواب ديالك منطقي؟",
        # ─── Transitions ───
        "دابا نتقدمو.",
        "صافي، نكملو.",
        "يلا نتقدمو للسؤال الجاي.",
        "نمشيو للخطوة الموالية.",
        "دابا غادي نبداو فقسم جديد.",
        "مزيان، غادي نشوفو حاجة أخرى.",
        "نعاودو نلخصو قبل ما نكملو.",
        "قبل ما نتقدمو، خاصنا نفهمو هادي.",
        "دابا، نطبقو لي تعلمناه.",
        "نشوفو مثال تطبيقي.",
        "يلا نجربو مع تمرين.",
        "تقريبا سالينا هاد الجزء.",
        "غادي نبداو بحاجة ساهلة.",
        # ─── Pitfall warnings ───
        "دير بالك!",
        "انتبه هنا.",
        "3ndak، هادي piège!",
        "دير بالك من هاد الخطأ.",
        "هادي piège ديال الباك.",
        "بزاف ديال التلاميذ كيغلطو هنا.",
        "خاصك تحذر من هاد النقطة.",
        "ما تنساش هاد الشرط.",
        "عندك! ما تخلطش بيناتهم.",
        "هادي نقطة حساسة، ركز.",
        "هنا كتخسر الباك إلا ما تحذرتيش.",
        "الخطأ الشائع هو هذا.",
        "تفاصيل صغيرة ولكن مهمة.",
        # ─── Method / instruction cues ───
        "هاد la formule خاصك تحفظها.",
        "هاد la méthode خاصك تعرفها.",
        "هادي la règle الأساسية.",
        "حفظ هاد التعريف.",
        "هاد la démonstration مهمة.",
        "طبق la méthode خطوة بخطوة.",
        "أول حاجة، قرا l'énoncé مزيان.",
        "ثاني حاجة، حدد المعطيات.",
        "ثالث حاجة، كتب la formule.",
        "ف الأخير، حسب la valeur.",
        "دير كل خطوة بالترتيب.",
        "ما تخصرش المراحل.",
        "la rédaction خاصها تكون واضحة.",
        "كتب les unités ف كل جواب.",
        "راجع حسابك قبل تكمل.",
        # ─── Common math/physics/chemistry terms in context ───
        "la dérivée كتعطينا la pente.",
        "la fonction exponentielle كتكبر بسرعة.",
        "la limite كتقرب من هاد la valeur.",
        "هاد la courbe عندها une asymptote.",
        "la vitesse هي la dérivée ديال la position.",
        "l'accélération هي la dérivée ديال la vitesse.",
        "la force كتساوي la masse فـ l'accélération.",
        "la conservation ديال l'énergie مهمة.",
        "ف la chimie، la concentration كتقاس بـ mol par litre.",
        "la vitesse de réaction كتزيد مع la température.",
        "un catalyseur كيسرع la réaction.",
        "l'équilibre chimique كيوقع عندما les vitesses متساويين.",
        "pH أقل من 7 كيعني محلول حمضي.",
        "la transformation lente كتاخد وقت طويل.",
        "la transformation rapide كتوقع ف ثواني.",
        # ─── Wrap-ups / summaries ───
        "نلخصو la leçon.",
        "نعاودو نشوفو النقط الأساسية.",
        "هاد شي لي تعلمناه ليوم.",
        "ف الأخير، خاصك تتذكر هاد القواعد.",
        "هادي النقط اللي لازم تحفظها.",
        "راجع هاد الدرس قبل ما تنعس.",
        "غدا غادي نكملو مع تمارين.",
        "برافو، خدمتي مزيان ليوم.",
        "سالينا هاد الدرس، بارك الله فيك.",
        "كنت زوين اليوم، كمل هكذا.",
        # ─── Outros / motivation ───
        "أنا فخور بيك، كمل هكذا.",
        "الباك قريب، خدم مزيان.",
        "ما تستعجلش، بالشوية كتوصل.",
        "الصبر مفتاح النجاح.",
        "كل يوم درس صغير، ف الأخير تنجح.",
        "ثق ف نفسك.",
        "النجاح هو تراكم المجهود.",
        "يلا الله يعاونك.",
        "نشوفوك غدا إن شاء الله.",
        "بالتوفيق ف الباك!",
        # ─── Error handling / soft corrections ───
        "ماشي بالضبط، جرب مرة أخرى.",
        "قريب، ولكن فيها نقطة صغيرة.",
        "لا، هادي ماشي هي.",
        "حاول من جديد.",
        "خلينا نشوفو من فين جاء الخطأ.",
        "ما تخافش من الغلط، كنتعلم منو.",
        "راجع la formule وعاود جرب.",
        "هنا غلطي صغير، شوف مرة أخرى.",
        "قرا السؤال مرة أخرى بتمعن.",
        "كتستعجل، خذ وقتك.",
        # ─── Hints / scaffolding ───
        "فكر ف la définition.",
        "راجع la formule لي تعلمناها.",
        "شوف les données ديال l'exercice.",
        "حاول تشوف la relation بين les variables.",
        "جرب تطبق هاد la propriété.",
        "فكر ف العلاقة مع الدرس لي فات.",
        "إلا قلبت la courbe شنو غادي تشوف؟",
        "جرب l'exemple السهل الأول.",
        "رسم مبياني يقدر يساعدك.",
        "اكتب المعطيات على ورقة.",
        # ─── Check-ins ───
        "واش كلشي مزيان؟",
        "واش محتاج نوقف؟",
        "واش خاصك نعاود الشرح؟",
        "واش غادي بيك؟",
        "قول ليا إلا ما فهمتيش.",
        "ما تخليش شي سؤال بلا جواب.",
        "واش بغيتي نمشي أبطأ؟",
        "واش بغيتي مثال آخر؟",
        "قول ليا فين حاس بالصعوبة.",
        # ─── Board references ───
        "شوف مزيان ف la table.",
        "كتب معايا ف الأوراق.",
        "هاد la ligne ف la table مهمة.",
        "لاحظ هاد la couleur الحمراء.",
        "شوف كيفاش حليت هاد l'exemple.",
    ],
}


async def warmup_cache() -> dict[str, int]:
    """
    Pregenerate common phrases at startup.

    Runs SEQUENTIALLY with a small delay between calls to respect provider
    rate limits (Gemini 2.5 Flash preview TTS = ~10 RPM on free tier).
    Phrases already in cache are served instantly (no API call).
    If we hit many consecutive failures we stop to avoid hammering the quota.
    """
    counts = {"requested": 0, "generated": 0, "cached_hit": 0, "failed": 0}
    if settings.tts_disabled:
        _safe_log("[TTS][warmup] TTS disabled — skipping")
        return counts

    # Flatten into (lang, phrase) tuples
    queue = [(lang, p) for lang, phrases in _WARMUP_PHRASES.items() for p in phrases]

    # Also load any course-specific Darija phrases generated offline by
    # scripts/enrich_tts_cache.py. This lets us ship pre-synthesized audio
    # for phrases tailored to each chapter without bloating the inline list.
    try:
        import json as _json
        extras_path = Path(__file__).resolve().parent.parent / "data" / "course_phrases.json"
        if extras_path.exists():
            extras = _json.loads(extras_path.read_text(encoding="utf-8"))
            if isinstance(extras, list):
                added = 0
                for p in extras:
                    if isinstance(p, str) and p.strip():
                        queue.append(("mixed", p.strip()))
                        added += 1
                if added:
                    _safe_log(f"[TTS][warmup] Loaded {added} course phrases from course_phrases.json")
    except Exception as _e:
        _safe_log(f"[TTS][warmup] Could not load course_phrases.json: {_e}")

    total = len(queue)

    t0 = time.time()
    consecutive_failures = 0
    for idx, (lang, phrase) in enumerate(queue):
        counts["requested"] += 1

        # Fast path: cache hit → no API call, no delay needed
        cleaned = clean_for_tts(phrase)
        spoken_text = _ensure_terminal_period(normalize_for_speech(cleaned, lang))
        cache_text = _normalize_for_cache(spoken_text)
        provider, voice, ext = _route(lang, spoken_text)
        cache = _get_cache()
        if cache is not None and cache.get(provider, voice, lang, cache_text, ext):
            counts["cached_hit"] += 1
            consecutive_failures = 0
            continue

        # Circuit breaker: after 5 consecutive failures, stop warmup
        if consecutive_failures >= 5:
            remaining = total - idx
            counts["failed"] += remaining
            _safe_log(
                f"[TTS][warmup] Stopping after {consecutive_failures} consecutive "
                f"failures ({remaining} phrases skipped)"
            )
            break

        try:
            seg = await _synthesize_one_segment(phrase, lang)
        except Exception as e:
            _safe_log(f"[TTS][warmup] exception on '{phrase[:30]}': {e}")
            seg = None

        if seg is None:
            counts["failed"] += 1
            consecutive_failures += 1
        elif seg.cached:
            counts["cached_hit"] += 1
            consecutive_failures = 0
        else:
            counts["generated"] += 1
            consecutive_failures = 0

        # Gentle pacing: ~6 calls/second max → well under any free-tier limit
        await asyncio.sleep(0.15)

    _safe_log(
        f"[TTS][warmup] {counts['requested']} phrases in "
        f"{int((time.time() - t0) * 1000)}ms — "
        f"generated={counts['generated']} hit={counts['cached_hit']} "
        f"failed={counts['failed']}"
    )
    return counts


class TTSService:
    """Thin OO wrapper so callers can do `tts_service.synthesize(...)`."""

    async def synthesize(self, text: str, language: str = "fr") -> TTSResult:
        return await synthesize(text, language)

    async def synthesize_segments(self, text: str, language: str = "fr") -> list[TTSSegment]:
        """Intelligent hybrid: split + per-sentence route + parallel synth."""
        return await synthesize_segments(text, language)

    def stream_synthesize_segments(self, text: str, language: str = "fr"):
        """Async generator yielding (index, total, segment) as each completes in order."""
        return stream_synthesize_segments(text, language)

    def stream_academy_pcm(self, text: str, language: str = "fr"):
        """Async generator yielding (sample_rate, pcm_s16le) as it is vocoded."""
        return stream_academy_pcm(text, language)

    def clean_for_tts(self, text: str) -> str:
        return clean_for_tts(text)

    def academy_stream_ready(self) -> bool:
        """Le chemin à faible latence est-il utilisable maintenant ?

        Sert à décider AVANT de découper la réponse : sans Academy, parler en
        deux temps n'apporterait rien et compliquerait le repli.
        """
        return bool(settings.academy_tts_stream) and _academy_is_available()

    async def warmup(self) -> dict[str, int]:
        return await warmup_cache()


tts_service = TTSService()
