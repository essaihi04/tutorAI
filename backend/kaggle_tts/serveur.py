"""Voix du prof en direct sur Kaggle — modèle Academy v4 (corpus v4), voix Amine au ton vif.

Ce script est poussé tel quel comme kernel Kaggle par le backend
(`app/services/kaggle_tts.py`) quand une séance s'ouvre, puis il :

1. ouvre un tunnel cloudflared (en parallèle de tout le reste) ;
2. installe les dépendances — depuis le « socle » préparé une fois pour toutes
   (kernel academy-tts-socle : roues pip, code lahgtna, poids de base,
   cloudflared), sinon depuis Internet ;
3. charge un modèle par carte T4 (2 cartes = 2 phrases calculées en même temps) ;
4. annonce son adresse au backend, qui bascule la voix du prof dessus ;
   si CONF « stt » est donné, charge aussi la reconnaissance vocale MoulSot
   (Qwen3-ASR) sur la dernière carte, à côté de la voix : POST /stt ;
5. s'éteint SEUL après `veille_s` sans parler (5 min) ou au bout de
   `duree_max_s` : un kernel éteint ne consomme plus de quota GPU.

Contrat HTTP = celui du serveur Academy de Colab, déjà parlé par
`tts_service.py` : POST /tts (WAV complet), POST /tts/stream (en-tête WAV puis
PCM 16 bits phrase par phrase), GET /health, GET /voices, POST /stt (audio de
l'élève -> texte ; 503 tant que MoulSot n'est pas prêt). Jeton Bearer.

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
TEXTE_PARLE_B64 = "__TEXTE_PARLE_B64__"   # règles du texte parlé (texte_parle.py), comme les cours v8

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
          if CONF["modele"] in p and "checkpoint" not in p]
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

# ── 0 bis. Reconnaissance vocale (facultative) : poids et paquet préparés en parallèle, sans retarder la voix ──
STT = {"etat": "absent" if not CONF.get("stt") else "preparation", "chemin": None, "qa": f"{WORK}/qa"}
STT_PREP = threading.Event()


def preparer_stt():
    try:
        nom = CONF["stt"]
        # Poids affinés attachés au kernel (sortie du kernel d'entraînement) : copiés en local, sinon Hugging Face.
        local = [os.path.dirname(p) for p in glob.glob(f"/kaggle/input/**/{nom}/config.json", recursive=True)]
        dest = f"{WORK}/stt"
        if local:
            sh(f"mkdir -p {dest} && cp -r '{local[0]}'/. {dest}/")
        else:
            from huggingface_hub import snapshot_download
            snapshot_download(nom, local_dir=dest, ignore_patterns=["rng_state.pth", "trainer_state.json"])
        ok = sh(f"pip -q install --no-deps --target {STT['qa']} qwen-asr==0.0.6 qwen-omni-utils soynlp==0.0.493")
        os.makedirs(f"{STT['qa']}/nagisa", exist_ok=True)       # seul l'aligneur s'en sert ; jamais appelé ici
        open(f"{STT['qa']}/nagisa/__init__.py", "a").close()
        STT["chemin"] = dest if ok else None
        say("STT préparé :", nom, "local" if local else "Hugging Face", "" if ok else "— paquet qwen-asr ÉCHEC")
    except Exception as e:
        say("STT préparation échouée :", repr(e)[:200])
    finally:
        STT_PREP.set()


if CONF.get("stt"):
    threading.Thread(target=preparer_stt, daemon=True).start()


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
    # (19 nov. 2026) Quand Cloudflare refuse un tunnel rapide (trop de demandes), cloudflared écrit l'adresse de son API
    # (« api.trycloudflare.com ») dans son erreur : ce n'est pas notre tunnel. On l'ignore et on redemande, 6 fois au plus.
    for essai in range(6):
        p = subprocess.Popen([binaire, "tunnel", "--no-autoupdate", "--url", "http://127.0.0.1:8000"],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for ligne in p.stdout:
            m = re.search(r"https://(?!api\.)[a-z0-9-]+\.trycloudflare\.com", ligne)
            if m and not URL["v"]:
                URL["v"] = m.group(0)
                say("tunnel", URL["v"])
        if URL["v"]:
            break
        say(f"tunnel refusé par Cloudflare (essai {essai + 1}), nouvelle demande dans {20 * (essai + 1)} s")
        time.sleep(20 * (essai + 1))
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

    with open(f"{WORK}/texte_parle.py", "wb") as f:
        f.write(base64.b64decode(TEXTE_PARLE_B64))
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
from texte_parle import parle, ponctuation_modele   # CO₂ -> « C O deux », nombres en français, écriture du corpus

AR = re.compile("[؀-ۿ]")
IMPORTANT = re.compile(
    r"\b(donc|retiens|retenez|c'est-à-dire|autrement dit|attention|important|essentiel|définition|on appelle|"
    r"par conséquent|conclusion|bilan|la règle|je relis|rappel)\b|=|إذن|يعني|مهم|رد البال|ردو البال|عاقل|خاصك|الخلاصة|نعاود نقرا",
    re.I)
INTERPELLE = re.compile(r"مرحبا|السلام|شوف|شوفو|تخيل|يلاه|هيا|مزيان|برافو|\b(regarde|regardez|imagine|bravo|bienvenue)\b", re.I)
# Réglages des cours v8 (validés à l'écoute le 2026-11-04 : voix vive, plus de mélodie),
# sans l'étirement Rubber Band : en direct, chaque dixième de seconde compte plus qu'un léger ralenti.
STYLES = {
    "essentiel": dict(ex=0.80, cfg=0.25, apres=0.55),
    "normal": dict(ex=0.70, cfg=0.35, apres=0.35),
    "question": dict(ex=0.80, cfg=0.35, apres=0.55),
    "interpelle": dict(ex=0.80, cfg=0.35, apres=0.40),
}


def style_de(p):
    if IMPORTANT.search(p):
        return "essentiel"
    if p.rstrip().endswith(("?", "؟")):
        return "question"
    if INTERPELLE.search(p):
        return "interpelle"
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


def murmure(w, sr, bas=-52.0, haut=-30.0, min_s=0.9):
    """La voix qui décroche : plus long passage (s) de son faible, ni parole ni silence ; 0 si < min_s.
    Entendu comme « un petit bruit, puis plus rien, puis la voix repart » (wx_r1_retard_v4, 8 novembre 2026)."""
    import numpy as np
    n = int(0.05 * sr)
    k = len(w) // n
    if k < 3:
        return 0
    db = 20 * np.log10(np.sqrt((np.asarray(w[:k * n], dtype=np.float64).reshape(k, n) ** 2).mean(1)) + 1e-9)
    f = (db > bas) & (db < haut)
    f[1:-1] |= (~f[1:-1]) & f[:-2] & f[2:]
    best = cur = 0
    for v in f:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return round(best * 0.05, 2) if best * 0.05 >= min_s else 0


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
        # Passages du flow (S3Gen : jetons -> son). lahgtna en fixe 10 en dur ; chacun coûte du GPU.
        # CONF « pas_flow » (défaut 10 = inchangé), et une requête peut le demander (banc d'écoute).
        PAS_DEFAUT = int(conf.get("pas_flow") or 10)
        PAS = [PAS_DEFAUT]
        _decodeur = m.s3gen.flow.decoder
        _forward_flow = _decodeur.forward

        def _forward_pas(*a, **kw):
            if "n_timesteps" in kw:
                kw["n_timesteps"] = PAS[0]
            elif len(a) >= 3:
                a = a[:2] + (PAS[0],) + a[3:]
            return _forward_flow(*a, **kw)
        _decodeur.forward = _forward_pas
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

        # Chauffe sur des phrases de la taille d'un premier morceau, dans les deux langues : avec le
        # seul « Bonjour. », la première vraie réponse d'une séance attendait 2,7 s contre 1,6 s ensuite.
        generer("Bonjour.", "fr", STYLES["normal"])
        generer("D'accord, regardons ça ensemble.", "fr", STYLES["normal"])
        generer("مزيان، دابا غادي نشوفو هادشي مع بعض.", "pl", STYLES["normal"])
        sortie.put(("pret", k, m.sr))
    except Exception as e:
        sortie.put(("echec", k, repr(e)[:300]))
        return
    while True:
        tid, texte, langue, options = entree.get()
        PAS[0] = int((options or {}).get("pas_flow") or PAS_DEFAUT)
        pcm = b""
        try:
            st = STYLES[style_de(texte)]
            lg = "pl" if (langue != "fr" and AR.search(texte)) else "fr"
            w = generer(ponctuation_modele(parle(texte)), lg, st)
            if murmure(w, m.sr):          # une seule reprise : la voix a décroché, on refait le morceau
                print(f"gpu{k} murmure, morceau refait :", texte[:60], flush=True)
                w = generer(ponctuation_modele(parle(texte)), lg, st)
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


def travailleur_stt(k, entree, sortie, conf):
    """Reconnaissance vocale MoulSot sur la carte k, à côté de la voix (≈ 4 Go de plus sur 16)."""
    import os, sys
    os.environ["CUDA_VISIBLE_DEVICES"] = str(k)
    sys.path[:0] = [p for p in conf["chemins"] if p not in sys.path]
    try:
        import numpy as np
        import torch
        from qwen_asr import Qwen3ASRModel
        asr = Qwen3ASRModel.from_pretrained(conf["stt"], dtype=torch.float16, device_map="cuda",
                                            max_new_tokens=256, max_inference_batch_size=4)
        asr.transcribe(audio=(np.zeros(16000, np.float32), 16000), language="Arabic")   # chauffe
        sortie.put(("pret", k, None))
    except Exception as e:
        sortie.put(("echec", k, repr(e)[:300]))
        return
    while True:
        tid, brut, langue = entree.get()
        texte = ""
        try:
            w = np.frombuffer(brut, dtype=np.float32)
            with torch.inference_mode():
                texte = asr.transcribe(audio=(w, 16000), language="French" if langue == "fr" else "Arabic")[0].text
            # Garde-fou : le modèle affiné a, 2 fois sur 841, continué à « transcrire » après la fin de l'audio.
            # Corpus v4 : 99,9 % des extraits sous 21,4 caractères (lettres) par seconde -> au-delà, on coupe.
            plafond = int(22 * len(w) / 16000) + 20
            if sum(c.isalnum() for c in texte) > plafond:
                n, coupe = 0, len(texte)
                for i, c in enumerate(texte):
                    n += c.isalnum()
                    if n > plafond:
                        coupe = i
                        break
                texte = texte[:coupe].rsplit(" ", 1)[0]
                print(f"stt gpu{k} texte trop long pour l'audio, coupé à {plafond} lettres", flush=True)
        except Exception as e:
            print(f"stt gpu{k} échec :", repr(e)[:200], flush=True)
        sortie.put(("fait", tid, (texte or "").strip()))


'''


# Un processus NEUF par carte (« spawn ») : `import chatterbox` initialise
# CUDA dès le chargement, ce qui interdit de forker après lui. Le code des
# processus vit dans un module écrit sur disque, que chacun importe seul.
with open(f"{WORK}/travailleur_tts.py", "w", encoding="utf-8") as f:
    f.write(MODULE_TRAVAILLEUR)
sys.path.insert(0, WORK)
from travailleur_tts import travailleur, travailleur_stt  # noqa: E402
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
                "fp16": bool(CONF.get("fp16")), "pas_flow": CONF.get("pas_flow")}
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

# La reconnaissance vocale se charge APRÈS la voix, sur la dernière carte : la voix est annoncée
# sans l'attendre ; tant que /stt répond 503, le backend garde Gemini.
STT_ENTREE, STT_SORTIE = ctx.Queue(), ctx.Queue()
STT_EN_COURS = {}


def demarrer_stt():
    STT_PREP.wait()
    if not STT["chemin"]:
        STT["etat"] = "echec"
        return
    k = CARTES[-1]
    conf = {"chemins": [STT["qa"]] + [p for p in sys.path if p], "stt": STT["chemin"]}
    ctx.Process(target=travailleur_stt, args=(k, STT_ENTREE, STT_SORTIE, conf), daemon=True).start()
    try:
        etat, _, info = STT_SORTIE.get(timeout=600)
    except Exception:
        etat, info = "echec", "pas de réponse en 10 min"
    STT["etat"] = "pret" if etat == "pret" else "echec"
    say(f"STT gpu{k}", STT["etat"], info or "", f"({time.time() - T0:.0f} s)")
    if etat != "pret":
        return
    while True:
        _, tid, texte = STT_SORTIE.get()
        with VERROU:
            t = STT_EN_COURS.pop(tid, None)
        if t:
            t.texte = texte
            t.fini.set()


if CONF.get("stt"):
    threading.Thread(target=demarrer_stt, daemon=True).start()

# File d'attente commune : chaque carte prend le morceau suivant dès qu'elle
# est libre, si bien que le morceau 2 se calcule pendant que le 1 est joué.
EN_COURS = {}
VERROU = threading.Lock()
COMPTEUR = [0]


class Travail:
    def __init__(self, texte, langue, options=None):
        self.texte, self.langue, self.options = texte, langue, options
        self.fini = threading.Event()
        self.pcm = b""
        self.essais = 0


# ── Contrôle des nombres (24/11/2026, règle de l'utilisateur : aussi pour les réponses libres) ──
# La voix dit parfois mal un nombre français placé juste après un mot arabe (« يعني vingt-deux », « و vingt-deux »
# entendu « و ألف », « حتى ل huit cents » entendu « douze cents ») ou le dit en darija (« cinq » -> « خمسة »).
# Chaque morceau qui contient un nombre français est transcrit par MoulSot ; si la suite des nombres entendue diffère
# du texte, ou si un nombre est entendu en darija, le morceau est refait (2 fois au plus). Les morceaux sans nombre
# ne passent pas par la transcription. Les lots (lot_sans_tunnel.py) font leur propre contrôle : option
# « controle_nombres »: False.
try:
    from num2words import num2words as _n2w
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "-q", "install", "num2words"], capture_output=True)
    try:
        from num2words import num2words as _n2w
    except ImportError:
        _n2w = None
import difflib as _dl
import unicodedata as _ud
_NB = set("zero un une deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize vingt trente "
          "quarante cinquante soixante cent cents mille million millions virgule".split())
_AR_FR = {"واحد": "un", "وحدة": "un", "جوج": "deux", "زوج": "deux", "اثنين": "deux", "تلاتة": "trois", "ثلاثة": "trois",
          "ربعة": "quatre", "اربعة": "quatre", "خمسة": "cinq", "ستة": "six", "سبعة": "sept", "تمنية": "huit", "ثمانية": "huit",
          "تسعة": "neuf", "عشرة": "dix", "حداش": "onze", "طناش": "douze", "تلطاش": "treize", "ربعطاش": "quatorze",
          "خمسطاش": "quinze", "سطاش": "seize", "عشرين": "vingt", "تلاتين": "trente", "ربعين": "quarante", "خمسين": "cinquante",
          "ستين": "soixante", "مية": "cent", "ميا": "cent", "مائة": "cent", "الف": "mille", "صفر": "zero"}


def _chiffres(t):   # MoulSot écrit souvent en chiffres : « 22 », « 6,02 », « 37% »
    t = str(t).replace("%", " pour cent ")
    t = re.sub(r"(?<=\d)[,.](?=\d)", " virgule ", t)
    t = re.sub(r"(?<!\d)0+(?=\d)", lambda m: " zéro" * len(m.group()) + " ", t)
    return re.sub(r"\d+", lambda m: " " + _n2w(int(m.group()), lang="fr") + " ", t) if _n2w else t


def _mots(t):   # sans accents ni hamza (NFD puis on retire les signes)
    t = "".join(c for c in _ud.normalize("NFD", _chiffres(t).lower()) if _ud.category(c) != "Mn")
    return re.findall(r"[\w']+", t.replace("-", " "))


def _nombres(t):   # un nombre dit en darija compte comme son équivalent français (le cas « darija » est relevé à part)
    out = []
    for w in _mots(t):
        w = _AR_FR.get(w, w)
        if w in _NB:
            out.append(w.replace("cents", "cent").replace("une", "un").replace("millions", "million"))
    return out


def fautes_nombres(stt, texte):
    a, b = _nombres(texte), _nombres(stt)
    out = []
    if a != b:
        m = _dl.SequenceMatcher(None, a, b, autojunk=False)
        if max(len(a), len(b)) - sum(x.size for x in m.get_matching_blocks()):
            out.append("NOMBRES " + " ".join(a) + " / " + " ".join(b))
    dits = sorted({w for w in _mots(stt) if w in _AR_FR} - {w for w in _mots(texte) if w in _AR_FR})
    if dits and a:
        out.append("DARIJA " + " ".join(dits))
    return out


def _transcrire_pcm(pcm, attente=20):
    """PCM 16 bits à SR -> texte MoulSot (None si le STT n'est pas prêt ou ne répond pas)."""
    if STT.get("etat") != "pret" or not pcm:
        return None
    import numpy as np
    w = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768
    n = int(len(w) * 16000 / SR)
    w16 = np.interp(np.linspace(0, len(w) - 1, n), np.arange(len(w)), w).astype(np.float32)
    o = Travail("", "mixed")
    o.texte = ""
    with VERROU:
        COMPTEUR[0] += 1
        tid = COMPTEUR[0]
        STT_EN_COURS[tid] = o
    STT_ENTREE.put((tid, w16.tobytes(), "mixed"))
    if not o.fini.wait(attente):
        with VERROU:
            STT_EN_COURS.pop(tid, None)
        return None
    return o.texte


def _a_controler(t):
    return (STT.get("etat") == "pret" and (t.options or {}).get("controle_nombres", True) is not False
            and t.essais < 2 and bool(_nombres(t.texte)))


def _controler(t, pcm):
    try:
        s = _transcrire_pcm(pcm)
        f = fautes_nombres(s, t.texte) if s else []
    except Exception as e:
        say("contrôle des nombres échoué :", repr(e)[:150])
        f = []
    if f:
        t.essais += 1
        say(f"nombres, morceau refait ({t.essais}) :", t.texte[:60], f)
        TRAVAUX.put(t)
        return
    t.pcm = pcm
    t.fini.set()


def recevoir():
    while True:
        etat, tid, pcm = SORTIE.get()
        with VERROU:
            t = EN_COURS.pop(tid, None)
        if t:
            if pcm and _a_controler(t):
                threading.Thread(target=_controler, args=(t, pcm), daemon=True).start()
            else:
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
        ENTREE.put((tid, t.texte, t.langue, t.options))


TRAVAUX = _File()

FIN = re.compile(r"(?<=[.!?؟…])\s+")


# Longueur maximale des morceaux successifs. Le modèle calcule à peu près en
# temps réel sur un T4 : le premier son attend tout le premier morceau, donc il
# est court ; pendant qu'il est joué, l'autre carte prépare le suivant, qui
# peut alors être plus long sans créer de blanc.
PALIERS = (35, 80, 150, 200)   # 1er morceau 45 -> 35 car. (2026-11-04) : premier son plus tôt


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
    req.state.options = {k: d[k] for k in ("pas_flow",) if d.get(k)}   # facultatif (banc d'écoute)
    return texte, ("fr" if d.get("langue") == "fr" else "ma")


def lancer(texte, langue, options=None):
    travaux = [Travail(p, langue, options) for p in phrases(texte)]
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
    return {"status": "ok", "moteur": "academy-v4-amine-vif", "gpus": len(MODELES), "sample_rate": SR,
            "veille_s": CONF["veille_s"], "inactif_s": round(time.time() - ACTIVITE["derniere"]),
            "stt": STT["etat"]}


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
        travaux = lancer(texte, langue, req.state.options)
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
            travaux = lancer(texte, langue, req.state.options)
            yield entete_wav()
            for t in travaux:
                await asyncio.to_thread(t.fini.wait)
                ACTIVITE["derniere"] = time.time()
                if t.pcm:
                    yield t.pcm

    return StreamingResponse(flux(), media_type="audio/wav")


class Ecoute:
    def __init__(self):
        self.fini = threading.Event()
        self.texte = ""


def decoder_audio(octets):
    """webm/ogg/wav/mp3 du navigateur -> float32 mono 16 kHz (ffmpeg)."""
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "pipe:0", "-t", "60", "-ac", "1", "-ar", "16000",
                        "-f", "f32le", "pipe:1"], input=octets, capture_output=True, timeout=20)
    return r.stdout if r.returncode == 0 else b""


@app.post("/stt")
async def stt(req: Request, authorization: str = Header(None)):
    verifier(authorization)
    if STT["etat"] != "pret":
        raise HTTPException(503, f"stt {STT['etat']}")
    octets = await req.body()
    if not octets or len(octets) > 15_000_000:
        raise HTTPException(422, "audio vide ou trop long")
    import asyncio
    t0 = time.time()
    with Parole():
        brut = await asyncio.to_thread(decoder_audio, octets)
        if len(brut) < 16000 * 4 * 0.2:
            raise HTTPException(422, "audio illisible ou trop court")
        e = Ecoute()
        with VERROU:
            COMPTEUR[0] += 1
            tid = COMPTEUR[0]
            STT_EN_COURS[tid] = e
        STT_ENTREE.put((tid, brut, req.query_params.get("langue", "mixed")))
        if not await asyncio.to_thread(e.fini.wait, 30):
            raise HTTPException(504, "stt trop long")
    return {"texte": e.texte, "duree_s": round(len(brut) / 4 / 16000, 2), "calcul_ms": int((time.time() - t0) * 1000)}


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
