"""[CANDIDAT, pas encore servi : un processus par carte — à valider par `essai` avant de remplacer serveur.py]

Voix du prof en direct sur Kaggle — modèle Academy v3 (étape 1600), voix Amine.

Ce script est poussé tel quel comme kernel Kaggle par le backend
(`app/services/kaggle_tts.py`) quand une séance s'ouvre, puis il :

1. ouvre un tunnel cloudflared (en parallèle de tout le reste) ;
2. installe les dépendances — depuis le « socle » préparé une fois pour toutes
   (kernel academy-tts-socle : roues pip, code lahgtna, poids de base,
   cloudflared), sinon depuis Internet ;
3. charge un modèle par carte T4 (2 cartes = 2 phrases calculées en même temps) ;
4. annonce son adresse au backend, qui bascule la voix du prof dessus ;
5. s'éteint SEUL après `veille_s` sans parler (5 min) ou au bout de
   `duree_max_s` : un kernel éteint ne consomme plus de quota GPU.

Contrat HTTP = celui du serveur Academy de Colab, déjà parlé par
`tts_service.py` : POST /tts (WAV complet), POST /tts/stream (en-tête WAV puis
PCM 16 bits phrase par phrase), GET /health, GET /voices. Jeton Bearer.

Les valeurs `CONF` sont remplacées à chaque lancement par le backend (jeton et
clé d'annonce neufs à chaque fois). Rien ici n'a besoin d'être modifié à la main.
"""
import base64
import glob
import io
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.request

CONF = json.loads("__CONF__")
REF_B64 = "__REF_B64__"

T0 = time.time()
WORK = "/tmp/academy"
os.makedirs(WORK, exist_ok=True)


def say(*a):
    print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash")
    if r.returncode:
        say("$", cmd[:90], "->", r.returncode, (r.stdout + r.stderr)[-300:])
    return r.returncode == 0


def annoncer(etat, **extra):
    """Prévient le backend. Jamais bloquant plus de 10 s, jamais fatal."""
    corps = json.dumps({"etat": etat, "cle": CONF["cle"], "lancement": CONF["lancement"], **extra}).encode()
    req = urllib.request.Request(CONF["annonce"], data=corps, method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            say("annonce", etat, "->", r.status)
    except Exception as e:
        say("annonce", etat, "échouée :", repr(e)[:160])


# ── 0. Le socle (préparé une fois, CPU) : tout ce qui coûte du temps au réveil ──
def trouver_socle():
    for p in glob.glob("/kaggle/input/**/socle.json", recursive=True):
        return os.path.dirname(p)
    return None


SOCLE = trouver_socle()
say("socle :", SOCLE or "absent — installation depuis Internet (plus lent)")

# Les poids sont lus en accès aléatoire (mmap) par safetensors et torch.load.
# Sur /kaggle/input (gcsfuse), cela prenait 9 minutes ; une copie continue sur
# le disque local va à ~160 Mo/s. On la lance tout de suite, en parallèle de
# l'installation des dépendances.
LOCAL = f"{WORK}/base"
COPIE = threading.Event()
FICHIERS_BASE = ["ve.pt", "s3gen.pt", "grapheme_mtl_merged_expanded_v1.json", "conds.pt", "Cangjie5_TC.json"]


def poids_fins():
    t3 = [p for p in glob.glob("/kaggle/input/**/t3_mtl23ls_v2.safetensors", recursive=True)
          if CONF["modele"] in p]
    return t3[0] if t3 else None


def copier():
    try:
        os.makedirs(LOCAL, exist_ok=True)
        fin = poids_fins()
        cmds = [f"cp '{fin}' {LOCAL}/t3_fin.safetensors"] if fin else []
        if SOCLE and os.path.isdir(f"{SOCLE}/lahgtna_base"):
            cmds.append(" && ".join(f"cp '{SOCLE}/lahgtna_base/{f}' {LOCAL}/" for f in FICHIERS_BASE
                                    if os.path.exists(f"{SOCLE}/lahgtna_base/{f}")))
        else:
            cmds.append(f"{sys.executable} -c \"from huggingface_hub import snapshot_download as s; "
                        f"s('oddadmix/lahgtna-chatterbox-v1', local_dir='{LOCAL}', allow_patterns={FICHIERS_BASE!r})\"")
        procs = [subprocess.Popen(c, shell=True, executable="/bin/bash") for c in cmds]
        for p in procs:
            p.wait()
        say("poids copiés en local :", sorted(os.listdir(LOCAL)))
    finally:
        COPIE.set()


SITE = f"{WORK}/site"
SITE_PRET = threading.Event()


def extraire_site():
    try:
        if SOCLE and os.path.exists(f"{SOCLE}/site.tar"):
            os.makedirs(SITE, exist_ok=True)
            if sh(f"tar -xf '{SOCLE}/site.tar' -C {SITE}"):
                say("paquets du socle extraits")
            else:
                shutil.rmtree(SITE, ignore_errors=True)
        if SOCLE and os.path.isdir(f"{SOCLE}/lahgtna-chatterbox"):
            sh(f"cp -r '{SOCLE}/lahgtna-chatterbox' {WORK}/")   # code importé en local, pas via le réseau
    finally:
        SITE_PRET.set()


threading.Thread(target=copier, daemon=True).start()
threading.Thread(target=extraire_site, daemon=True).start()


# ── 1. Tunnel : lancé tout de suite, il s'établit pendant le chargement ──
URL = {"v": None}


def ouvrir_tunnel():
    binaire = f"{SOCLE}/cloudflared" if SOCLE and os.path.exists(f"{SOCLE}/cloudflared") else None
    if not binaire:
        binaire = f"{WORK}/cloudflared"
        sh(f"curl -sL -o {binaire} https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64")
    if not os.access(binaire, os.X_OK):
        local = f"{WORK}/cloudflared-x"
        sh(f"cp '{binaire}' {local} && chmod +x {local}")
        binaire = local
    p = subprocess.Popen([binaire, "tunnel", "--no-autoupdate", "--url", "http://127.0.0.1:8000"],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for ligne in p.stdout:
        m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", ligne)
        if m and not URL["v"]:
            URL["v"] = m.group(0)
            say("tunnel", URL["v"])
    say("cloudflared s'est arrêté")


threading.Thread(target=ouvrir_tunnel, daemon=True).start()
annoncer("demarrage")

# Garde-fou du quota : quoi qu'il arrive au démarrage (installation figée,
# processus de carte mort sans prévenir…), un kernel qui n'est pas prêt en
# 15 minutes s'éteint au lieu de tourner jusqu'à la limite de Kaggle.
PRET = threading.Event()


def garde_fou():
    if not PRET.wait(900):
        say("pas prêt en 15 min — extinction")
        annoncer("eteint", raison="démarrage trop long")
        os._exit(1)


threading.Thread(target=garde_fou, daemon=True).start()


# ── 2. Dépendances ──
PAQUETS = ("'transformers==4.57.6' 'tokenizers==0.22.1' 'accelerate==1.12.0' 'huggingface-hub==0.36.0' "
           "resemble-perth conformer diffusers s3tokenizer omegaconf einops safetensors fastapi uvicorn")


def installer():
    SITE_PRET.wait()
    roues = glob.glob(f"{SOCLE}/roues/*.whl") if SOCLE else []
    if os.path.isdir(SITE):
        sys.path.insert(0, SITE)
    elif roues:
        ok = sh("pip -q install --no-index --no-deps " + " ".join(f"'{r}'" for r in roues))
        say("roues du socle :", len(roues), "ok" if ok else "ÉCHEC")
    try:
        import transformers, s3tokenizer, perth, conformer, diffusers, fastapi, uvicorn  # noqa: F401
        assert transformers.__version__ == "4.57.6"
    except Exception as e:
        say("dépendances incomplètes (", repr(e)[:80], ") — pip en ligne")
        sh("pip -q install " + PAQUETS)

    code = f"{WORK}/lahgtna-chatterbox"
    if not os.path.isdir(code):
        sh(f"git clone -q --depth 1 https://github.com/Oddadmix/lahgtna-chatterbox.git {code}")
    sys.path.insert(0, f"{code}/src")

    ref = f"{WORK}/reference_amine.flac"
    with open(ref, "wb") as f:
        f.write(base64.b64decode(REF_B64))
    COPIE.wait()
    fin = f"{LOCAL}/t3_fin.safetensors"
    if not os.path.exists(fin):
        raise SystemExit(f"poids fins introuvables (kernel {CONF['modele']} non attaché ?)")
    # Les poids fins remplacent ceux de base : s'ils portent exactement les
    # mêmes clés, on les charge directement à leur place (2 Go de moins à lire
    # et à charger). Sinon, repli sur la méthode des cours : base + surcharge.
    from safetensors import safe_open
    from huggingface_hub import hf_hub_download
    with safe_open(fin, "pt") as f:
        cles_fin = set(f.keys())
    base_t3 = (f"{SOCLE}/lahgtna_base/t3_mtl23ls_v2.safetensors" if SOCLE else None)
    if not base_t3 or not os.path.exists(base_t3):
        base_t3 = hf_hub_download("oddadmix/lahgtna-chatterbox-v1", "t3_mtl23ls_v2.safetensors",
                                  local_dir=f"{WORK}/hf")
    with safe_open(base_t3, "pt") as f:
        cles_base = set(f.keys())
    direct = cles_fin == cles_base
    if direct:
        os.replace(fin, f"{LOCAL}/t3_mtl23ls_v2.safetensors")
    else:
        sh(f"cp '{base_t3}' {LOCAL}/t3_mtl23ls_v2.safetensors")
    say(f"poids fins : {len(cles_fin & cles_base)}/{len(cles_base)} clés communes ->",
        "chargement direct" if direct else "base + surcharge")
    return LOCAL, (None if direct else fin), ref


BASE, T3, REF = installer()
say("dépendances prêtes")

import multiprocessing as mp  # noqa: E402

# ── 3. Un PROCESSUS par carte ──
# La génération avance jeton par jeton dans une boucle Python : avec deux fils
# dans un même processus, les deux cartes se disputaient le verrou de
# l'interpréteur et chacune ralentissait (banc fp16 : ×1,8 au lieu de ×1,0).
# Deux processus calculent vraiment en parallèle. Le processus principal ne
# fait que le HTTP.
MODULE_TRAVAILLEUR = r'''"""Processus d'une carte T4 (lancé en « spawn » par serveur.py)."""
import re

AR = re.compile("[؀-ۿ]")
IMPORTANT = re.compile(
    r"\b(donc|retiens|retenez|c'est-à-dire|autrement dit|attention|important|essentiel|définition|on appelle|"
    r"par conséquent|conclusion|bilan|la règle|je relis|rappel)\b|=|إذن|يعني|مهم|رد البال|ردو البال|عاقل|خاصك|الخلاصة|نعاود نقرا",
    re.I)
# Réglages validés à l'écoute pour les cours (v6), sans l'étirement Rubber Band :
# en direct, chaque dixième de seconde compte plus qu'un léger ralenti.
STYLES = {
    "essentiel": dict(ex=0.70, cfg=0.25, apres=0.45),
    "normal": dict(ex=0.60, cfg=0.35, apres=0.28),
    "question": dict(ex=0.70, cfg=0.35, apres=0.45),
}


def style_de(p):
    if IMPORTANT.search(p):
        return "essentiel"
    if p.rstrip().endswith(("?", "؟")):
        return "question"
    return "normal"


def nettoyer(w, sr):
    """Coupe le résidu avant/après la voix (cf. v6), fondus 10/40 ms."""
    import numpy as np
    h = int(0.02 * sr)
    n = len(w) // h
    if n < 3:
        return w
    db = 20 * np.log10(np.sqrt((w[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
    parole = np.where((db > db.max() - 35) & (db > -45))[0]
    if not len(parole):
        return w
    a = max(0, parole[0] * h - int(0.02 * sr))
    b = min(len(w), (parole[-1] + 1) * h + int(0.06 * sr))
    w = w[a:b].copy()
    fi, fo = min(len(w), int(0.01 * sr)), min(len(w), int(0.04 * sr))
    w[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)
    w[len(w) - fo:] *= np.cos(np.linspace(0, np.pi / 2, fo, dtype=np.float32)) ** 2
    return w


def travailleur(k, entree, sortie, conf):
    """Processus d'une carte : charge le modèle, puis synthétise ce qu'on lui donne."""
    import os, sys
    os.environ["CUDA_VISIBLE_DEVICES"] = str(k)   # avant tout import de torch
    sys.path[:0] = [p for p in conf["chemins"] if p not in sys.path]
    BASE, T3, REF = conf["base"], conf["t3"], conf["ref"]
    try:
        import numpy as np
        import torch
        from safetensors.torch import load_file
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        m = ChatterboxMultilingualTTS.from_local(BASE, device="cuda")
        if T3:
            m.t3.load_state_dict(load_file(T3, device="cuda"), strict=False)
        m.t3.to("cuda").eval()
        try:
            m.t3.tfmr.set_attn_implementation("eager")
        except Exception:
            pass
        m.t3.tfmr.config._attn_implementation = "eager"
        # La voix d'Amine n'est analysée qu'une fois : sinon chaque phrase
        # recalculerait l'empreinte de la référence (~0,3 s perdues).
        m.prepare_conditionals(REF, exaggeration=STYLES["normal"]["ex"])
        demi = bool(conf.get("fp16"))

        def generer(texte, lg, st):
            with torch.inference_mode():
                if demi:
                    with torch.autocast("cuda", dtype=torch.float16):
                        w = m.generate(texte, language_id=lg, exaggeration=st["ex"], temperature=0.75,
                                       cfg_weight=st["cfg"])
                else:
                    w = m.generate(texte, language_id=lg, exaggeration=st["ex"], temperature=0.75,
                                   cfg_weight=st["cfg"])
            return w.float().cpu().numpy()[0]

        generer("Bonjour.", "fr", STYLES["normal"])          # chauffe
        sortie.put(("pret", k, m.sr))
    except Exception as e:
        sortie.put(("echec", k, repr(e)[:300]))
        return
    while True:
        tid, texte, langue = entree.get()
        pcm = b""
        try:
            st = STYLES[style_de(texte)]
            lg = "pl" if (langue != "fr" and AR.search(texte)) else "fr"
            w = generer(texte, lg, st)
            # Un morceau coupé à une virgule n'est pas une fin de phrase : souffle court.
            apres = st["apres"] if texte.rstrip()[-1:] in ".!?؟…" else 0.12
            w = np.concatenate([nettoyer(w.astype(np.float32), m.sr), np.zeros(int(apres * m.sr), np.float32)])
            pic = float(np.abs(w).max() or 1)
            if pic > 0.944:
                w *= 0.944 / pic
            pcm = (np.clip(w, -1, 1) * 32767).astype("<i2").tobytes()
        except Exception as e:
            print(f"gpu{k} phrase échouée :", repr(e)[:200], flush=True)
        sortie.put(("fait", tid, pcm))


'''


# Un processus NEUF par carte (« spawn ») : `import chatterbox` initialise
# CUDA dès le chargement, ce qui interdit de forker après lui. Le code des
# processus vit dans un module écrit sur disque, que chacun importe seul.
with open(f"{WORK}/travailleur_tts.py", "w", encoding="utf-8") as f:
    f.write(MODULE_TRAVAILLEUR)
sys.path.insert(0, WORK)
from travailleur_tts import travailleur  # noqa: E402
r = subprocess.run("nvidia-smi -L", shell=True, capture_output=True, text=True)
N = max(1, min(2, r.stdout.count("GPU ")))
ctx = mp.get_context("spawn")
# Un enfant « spawn » réimporte le script principal s'il le trouve sur disque :
# il relançait alors tout le serveur (tunnel, chargement…) et mourait sur
# « RuntimeError: … bootstrapping phase ». Sans chemin, il n'importe que
# travailleur_tts, ce qui est tout ce dont il a besoin.
import __main__  # noqa: E402
for attr in ("__file__",):
    if hasattr(__main__, attr):
        delattr(__main__, attr)
__main__.__spec__ = None
ENTREE, SORTIE = ctx.Queue(), ctx.Queue()
CONF_TRAVAIL = {"chemins": [p for p in sys.path if p], "base": BASE, "t3": T3, "ref": REF,
                "fp16": bool(CONF.get("fp16"))}
for k in range(N):
    ctx.Process(target=travailleur, args=(k, ENTREE, SORTIE, CONF_TRAVAIL), daemon=True).start()
CARTES, SR = [], 24000
for _ in range(N):
    # Jamais d'attente sans fin : un enfant mort sans message laissait le
    # kernel tourner (et consommer le quota) jusqu'à sa limite de 3 h.
    try:
        etat, k, info = SORTIE.get(timeout=600)
    except Exception:
        say("aucune carte n'a répondu en 10 min")
        break
    if etat == "pret":
        CARTES.append(k)
        SR = info
        say(f"gpu{k} prêt")
    else:
        say(f"gpu{k} ÉCHEC", info)
if not CARTES:
    annoncer("eteint", raison="aucun modèle chargé")
    os._exit(1)
MODELES = CARTES

# File d'attente commune : chaque carte prend le morceau suivant dès qu'elle
# est libre, si bien que le morceau 2 se calcule pendant que le 1 est joué.
EN_COURS = {}
VERROU = threading.Lock()
COMPTEUR = [0]


class Travail:
    def __init__(self, texte, langue):
        self.texte, self.langue = texte, langue
        self.fini = threading.Event()
        self.pcm = b""


def recevoir():
    while True:
        etat, tid, pcm = SORTIE.get()
        with VERROU:
            t = EN_COURS.pop(tid, None)
        if t:
            t.pcm = pcm
            t.fini.set()


threading.Thread(target=recevoir, daemon=True).start()


class _File:
    """Même interface que queue.Queue.put pour `lancer()`."""

    @staticmethod
    def put(t):
        with VERROU:
            COMPTEUR[0] += 1
            tid = COMPTEUR[0]
            EN_COURS[tid] = t
        ENTREE.put((tid, t.texte, t.langue))


TRAVAUX = _File()

FIN = re.compile(r"(?<=[.!?؟…])\s+")


# Longueur maximale des morceaux successifs. Le modèle calcule à peu près en
# temps réel sur un T4 : le premier son attend tout le premier morceau, donc il
# est court ; pendant qu'il est joué, l'autre carte prépare le suivant, qui
# peut alors être plus long sans créer de blanc.
PALIERS = (45, 90, 150, 200)


def phrases(texte):
    out = []
    for p in FIN.split(texte.strip()):
        p = p.strip()
        while p:
            limite = PALIERS[min(len(out), len(PALIERS) - 1)]
            if len(p) <= limite + 15:     # ne pas laisser un bout de 2 mots derrière
                out.append(p)
                break
            q = max(p.rfind(",", 15, limite), p.rfind("،", 15, limite), p.rfind(";", 15, limite),
                    p.rfind(":", 15, limite))
            if q <= 0:
                q = p.rfind(" ", 15, limite)
            if q <= 0:
                out.append(p)
                break
            out.append(p[:q + 1].strip())
            p = p[q + 1:].strip()
    return out


def entete_wav(n_octets=0xFFFFFFFF - 36):
    import struct
    return (b"RIFF" + struct.pack("<I", min(n_octets + 36, 0xFFFFFFFF)) + b"WAVEfmt "
            + struct.pack("<IHHIIHH", 16, 1, 1, SR, SR * 2, 2, 16) + b"data" + struct.pack("<I", n_octets))


# ── 4. Serveur HTTP ──
from fastapi import FastAPI, Header, HTTPException, Request  # noqa: E402
from fastapi.responses import Response, StreamingResponse  # noqa: E402
import uvicorn  # noqa: E402

ACTIVITE = {"derniere": time.time(), "en_cours": 0}
app = FastAPI()


def verifier(authorization):
    if authorization != f"Bearer {CONF['jeton']}":
        raise HTTPException(401, "jeton refusé")


async def lire(req: Request):
    d = await req.json()
    texte = (d.get("texte") or d.get("text") or "").strip()
    if not texte or len(texte) > 5000:
        raise HTTPException(422, "texte vide ou trop long")
    return texte, ("fr" if d.get("langue") == "fr" else "ma")


def lancer(texte, langue):
    travaux = [Travail(p, langue) for p in phrases(texte)]
    for t in travaux:
        TRAVAUX.put(t)
    return travaux


class Parole:
    """Compte une requête en cours : la veille ne coupe jamais au milieu d'une phrase."""
    def __enter__(self):
        ACTIVITE["en_cours"] += 1
        ACTIVITE["derniere"] = time.time()

    def __exit__(self, *a):
        ACTIVITE["en_cours"] -= 1
        ACTIVITE["derniere"] = time.time()


@app.get("/health")
def health():
    return {"status": "ok", "moteur": "academy-v3-amine", "gpus": len(MODELES), "sample_rate": SR,
            "veille_s": CONF["veille_s"], "inactif_s": round(time.time() - ACTIVITE["derniere"])}


@app.post("/garder")
def garder(authorization: str = Header(None)):
    """L'élève travaille (il écrit, il répond) : la séance est vivante même
    si le prof se tait. Repousse la veille sans rien calculer."""
    verifier(authorization)
    ACTIVITE["derniere"] = time.time()
    return {"ok": True}


@app.get("/voices")
def voices():
    return ["amine"]


@app.post("/tts")
async def tts(req: Request, authorization: str = Header(None)):
    verifier(authorization)
    texte, langue = await lire(req)
    t0 = time.time()
    with Parole():
        travaux = lancer(texte, langue)
        import asyncio
        for t in travaux:
            await asyncio.to_thread(t.fini.wait)
    pcm = b"".join(t.pcm for t in travaux)
    if not pcm:
        raise HTTPException(500, "synthèse vide")
    return Response(entete_wav(len(pcm)) + pcm, media_type="audio/wav",
                    headers={"X-Duree-Ms": str(int(len(pcm) / 2 / SR * 1000)),
                             "X-Calcul-Ms": str(int((time.time() - t0) * 1000))})


@app.post("/tts/stream")
async def tts_stream(req: Request, authorization: str = Header(None)):
    verifier(authorization)
    texte, langue = await lire(req)
    import asyncio

    async def flux():
        with Parole():
            travaux = lancer(texte, langue)
            yield entete_wav()
            for t in travaux:
                await asyncio.to_thread(t.fini.wait)
                ACTIVITE["derniere"] = time.time()
                if t.pcm:
                    yield t.pcm

    return StreamingResponse(flux(), media_type="audio/wav")


threading.Thread(target=lambda: uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning"),
                 daemon=True).start()

# ── 5. Annonce, puis veille ──
for _ in range(120):            # le tunnel est presque toujours prêt avant les modèles
    if URL["v"]:
        break
    time.sleep(0.5)
if not URL["v"]:
    annoncer("eteint", raison="tunnel non établi")
    os._exit(1)
time.sleep(1.0)                 # laisser uvicorn ouvrir son port
ACTIVITE["derniere"] = time.time()
PRET.set()
annoncer("pret", url=URL["v"], jeton=CONF["jeton"], gpus=len(MODELES), demarrage_s=round(time.time() - T0, 1))
say(f"prêt en {time.time() - T0:.0f} s sur {len(MODELES)} carte(s)")

raison = "veille"
while True:
    time.sleep(5)
    inactif = time.time() - ACTIVITE["derniere"]
    if ACTIVITE["en_cours"] == 0 and inactif > CONF["veille_s"]:
        break
    if time.time() - T0 > CONF["duree_max_s"]:
        raison = "durée maximale"
        break
say(f"extinction ({raison}) après {time.time() - T0:.0f} s")
annoncer("eteint", raison=raison, duree_s=round(time.time() - T0))
os._exit(0)
