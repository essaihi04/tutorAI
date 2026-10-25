"""Socle de la voix en direct — à lancer UNE fois (et après un changement de
dépendances), sur CPU : il ne consomme donc pas de quota GPU.

Il prépare dans sa sortie tout ce qui coûte du temps au réveil du kernel
`academy-tts-direct` :
  roues/              les paquets pip absents de l'image Kaggle (installés hors ligne en ~10 s)
  lahgtna-chatterbox/ le code du modèle
  lahgtna_base/       les poids de base (ve, s3gen, t3, tokenizer…)
  cloudflared         le binaire du tunnel
  socle.json          versions et date

Le kernel direct l'attache en `kernel_sources` (réglage KAGGLE_TTS_SOCLE).
Poussé par `python -m scripts.kaggle_tts socle`.
"""
import json
import os
import shutil
import subprocess
import time

W = "/kaggle/working"
PAQUETS = ["transformers==4.57.6", "tokenizers==0.22.1", "accelerate==1.12.0", "huggingface-hub==0.36.0",
           "resemble-perth", "conformer", "diffusers", "s3tokenizer", "omegaconf", "einops", "safetensors",
           "fastapi", "uvicorn"]


def sh(cmd):
    print("$", cmd[:120], flush=True)
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash")
    if r.returncode:
        print((r.stdout + r.stderr)[-800:], flush=True)
    return r


def gel():
    sortie = sh("pip list --format=freeze").stdout
    return dict(l.split("==", 1) for l in sortie.splitlines() if "==" in l)


avant = gel()
sh("pip -q install " + " ".join(f"'{p}'" for p in PAQUETS))
apres = gel()
# Seuls les paquets ajoutés ou changés par l'installation deviennent des roues :
# torch, numpy… restent ceux de l'image, compilés pour ses cartes.
nouveaux = {n: v for n, v in apres.items() if avant.get(n) != v}
os.makedirs(f"{W}/roues", exist_ok=True)
for n, v in sorted(nouveaux.items()):
    sh(f"pip wheel -q --no-deps -w {W}/roues '{n}=={v}'")
print(len(nouveaux), "paquets ->", len(os.listdir(f"{W}/roues")), "roues", flush=True)

sh(f"git clone -q --depth 1 https://github.com/Oddadmix/lahgtna-chatterbox.git {W}/lahgtna-chatterbox")
shutil.rmtree(f"{W}/lahgtna-chatterbox/.git", ignore_errors=True)

from huggingface_hub import snapshot_download  # noqa: E402

snapshot_download("oddadmix/lahgtna-chatterbox-v1", local_dir=f"{W}/lahgtna_base",
                  allow_patterns=["ve.pt", "s3gen.pt", "t3_mtl23ls_v2.safetensors",
                                  "grapheme_mtl_merged_expanded_v1.json", "conds.pt", "Cangjie5_TC.json"])
shutil.rmtree(f"{W}/lahgtna_base/.cache", ignore_errors=True)

sh(f"curl -sL -o {W}/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
   f" && chmod +x {W}/cloudflared")

json.dump({"date": time.strftime("%Y-%m-%d %H:%M"), "paquets": nouveaux,
           "base": sorted(os.listdir(f"{W}/lahgtna_base"))},
          open(f"{W}/socle.json", "w"), indent=1)
print("socle prêt", flush=True)
