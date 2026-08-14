"""
Cellule Colab — lance l'API TTS Academy et ouvre le tunnel public.

À coller dans UNE seule cellule d'un notebook Colab avec GPU (Exécution →
Modifier le type d'exécution → T4). Elle affiche à la fin l'URL et le jeton
à reporter dans `backend/.env` ET `deploy/backend.env`.

⚠️ Ce fichier ne contient PAS le serveur lui-même. `serveur_tts.py` et
`normaliser_texte_darija.py` vivent sur ton Drive (`academy_tts/`) : ce sont
eux qui portent le contrat de l'API, et ils restent la référence. Cette
cellule ne fait que les installer, les câbler et les exposer.

Le tunnel `trycloudflare.com` est PUBLIC et son URL change à chaque
exécution — d'où le jeton régénéré à chaque fois, et le report obligatoire
dans les deux .env (voir tts_colab/README.md).
"""

# ── 1. Dépendances ───────────────────────────────────────────────────
# `datasets` est épinglé sous la 4.0 : la 4.x a retiré des symboles dont
# lahgtna dépend encore. torch est déjà présent sur Colab, on n'y touche pas.
!pip install -q "transformers>=4.44" "datasets>=3.6,<4" soundfile librosa \
    safetensors resemble-perth conformer diffusers s3tokenizer omegaconf \
    einops fastapi "uvicorn[standard]"

# ── 2. Drive (checkpoints + voix de référence) ───────────────────────
from google.colab import drive
drive.mount('/content/drive')

# ── 3. Code de base lahgtna ──────────────────────────────────────────
# ⚠️ `patch_finetune*.py` ne sert QU'À L'ENTRAÎNEMENT. L'inférence n'en a pas
# besoin : serveur_tts.py applique lui-même le seul correctif nécessaire (le
# passage de l'attention en `eager`).
import os
if not os.path.isdir('/content/lahgtna'):
    !git clone -q https://github.com/Oddadmix/lahgtna-chatterbox.git /content/lahgtna

# ── 4. Poids de base (~1,5 Go, mis en cache par le hub) ──────────────
from huggingface_hub import snapshot_download
base = snapshot_download(
    "oddadmix/lahgtna-chatterbox-v1",
    local_dir="/content/lahgtna_base",
    allow_patterns=[
        "ve.pt", "s3gen.pt", "t3_mtl23ls_v2.safetensors",
        "grapheme_mtl_merged_expanded_v1.json", "conds.pt", "Cangjie5_TC.json",
    ],
)
print("Base :", base)

# ── 5. Câblage du serveur ────────────────────────────────────────────
import secrets, shutil

DRIVE = '/content/drive/MyDrive/academy_tts'

os.environ['LAHGTNA_SRC'] = '/content/lahgtna/src'
os.environ['TTS_BASE']    = base
# Le checkpoint fine-tuné de la voix du prof (2,0 Go) — une par voix entraînée.
os.environ['TTS_CKPT']    = f'{DRIVE}/ckpt_prof_faress/t3_mtl23ls_v2.safetensors'
# ⚠️ Données de PRODUCTION : la voix vient de ces clips de 6 s, pas des poids.
# En changer sans prévenir s'entend immédiatement côté élève.
os.environ['TTS_VOIX']    = f'{DRIVE}/voix'
# Jeton neuf à chaque session : le tunnel précédent reste ouvert quelques
# minutes et n'importe qui peut l'atteindre.
os.environ['TTS_TOKEN']   = secrets.token_urlsafe(24)

# Le serveur et le normaliseur vivent sur Drive ; on les copie à côté du
# notebook pour qu'uvicorn les importe comme un module ordinaire.
for f in ('serveur_tts.py', 'normaliser_texte_darija.py'):
    shutil.copy(f'{DRIVE}/{f}', f'/content/{f}')

# ── 6. cloudflared ───────────────────────────────────────────────────
if not os.path.exists('/usr/local/bin/cloudflared'):
    !wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
        -O /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared

# ── 7. Lancement ─────────────────────────────────────────────────────
# UN SEUL worker, jamais plus : une génération occupe le GPU entièrement, et
# deux workers se disputeraient la VRAM en doublant la latence des deux.
import re, subprocess, time, urllib.request

subprocess.Popen(
    ['uvicorn', 'serveur_tts:app', '--host', '0.0.0.0', '--port', '8000',
     '--workers', '1'],
    cwd='/content',
    stdout=open('/content/uvicorn.log', 'wb'),
    stderr=subprocess.STDOUT,
)

tunnel = subprocess.Popen(
    ['cloudflared', 'tunnel', '--url', 'http://127.0.0.1:8000',
     '--no-autoupdate'],
    stdout=open('/content/cloudflared.log', 'wb'),
    stderr=subprocess.STDOUT,
)

# L'URL n'apparaît dans le log de cloudflared qu'au bout de quelques secondes.
url = None
for _ in range(60):
    time.sleep(1)
    try:
        log = open('/content/cloudflared.log').read()
    except FileNotFoundError:
        continue
    m = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', log)
    if m:
        url = m.group(0)
        break

if not url:
    raise RuntimeError(
        "Tunnel non ouvert. Voir /content/cloudflared.log — "
        "cloudflared échoue parfois au premier essai, relance la cellule."
    )

# Le modèle met ~1 min à charger : tant qu'il n'est pas prêt, /health répond
# {"statut":"chargement"}. On attend vraiment "ok" pour ne pas annoncer une
# API qui renverrait des 503 à la première phrase.
statut = None
for _ in range(180):
    try:
        with urllib.request.urlopen(f'{url}/health', timeout=10) as r:
            import json
            statut = json.load(r).get('statut')
        if statut == 'ok':
            break
    except Exception:
        pass
    time.sleep(2)

print()
print('=' * 68)
print('  API PRETE' if statut == 'ok' else f'  API NON PRETE (statut={statut})')
print('=' * 68)
print('  URL   ', url)
print('  JETON ', os.environ['TTS_TOKEN'])
print('  DOC   ', f'{url}/docs')
print('=' * 68)
print()
print('À reporter dans backend/.env ET deploy/backend.env :')
print(f'  ACADEMY_TTS_URL={url}')
print(f'  ACADEMY_TTS_TOKEN={os.environ["TTS_TOKEN"]}')
print()
print('Puis, à la racine du projet :')
print('  powershell -ExecutionPolicy Bypass -Command "& { '
      '.\\deploy\\remote-deploy.ps1 -UpdateEnv }"')
print()
print('⚠️ Garde cet onglet ouvert : si le notebook se déconnecte, le tunnel')
print('   meurt (Cloudflare error 1033) et la voix retombe côté élève.')

# Bloque la cellule pour maintenir le tunnel ouvert.
tunnel.wait()
