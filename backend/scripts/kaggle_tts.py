"""Outils de la voix Kaggle à la demande.

    python -m scripts.kaggle_tts socle    # une fois : prépare le socle (CPU, sans quota GPU)
    python -m scripts.kaggle_tts statut   # état des kernels socle / direct sur Kaggle
    python -m scripts.kaggle_tts journal  # dernières lignes du kernel direct

Le kernel direct n'est jamais lancé à la main : le backend le pousse quand une
séance s'ouvre (app/services/kaggle_tts.py). Identifiants : KAGGLE_USERNAME et
KAGGLE_API_TOKEN dans l'environnement ou backend/.env.
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

from app.config import get_settings
from app.services.kaggle_tts import DOSSIER_KERNEL, kaggle_cli

settings = get_settings()

SOCLE = "academy-tts-socle"


def socle():
    d = Path(tempfile.mkdtemp(prefix="socle_"))
    try:
        shutil.copy(DOSSIER_KERNEL / "socle.py", d / "socle.py")
        meta = {"id": f"{settings.kaggle_username}/{SOCLE}", "title": SOCLE, "code_file": "socle.py",
                "language": "python", "kernel_type": "script", "is_private": True,
                "enable_gpu": False, "enable_internet": True, "dataset_sources": [],
                "competition_sources": [], "kernel_sources": []}
        (d / "kernel-metadata.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
        print(kaggle_cli("kernels", "push", "-p", str(d)))
        print(f"\nQuand il est terminé (statut « complete »), mettez KAGGLE_TTS_SOCLE={SOCLE} dans l'env du backend.")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def statut():
    for k in (SOCLE, settings.kaggle_tts_kernel):
        try:
            print(kaggle_cli("kernels", "status", f"{settings.kaggle_username}/{k}"))
        except RuntimeError as e:
            print(k, ":", e)


def journal():
    d = Path(tempfile.mkdtemp(prefix="journal_"))
    try:
        kaggle_cli("kernels", "output", f"{settings.kaggle_username}/{settings.kaggle_tts_kernel}", "-p", str(d),
                   timeout=300)
        for f in sorted(d.glob("*.log")):
            lignes = f.read_text(encoding="utf-8", errors="replace").splitlines()
            print("\n".join(lignes[-60:]))
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    {"socle": socle, "statut": statut, "journal": journal}.get(sys.argv[1] if len(sys.argv) > 1 else "",
                                                               lambda: print(__doc__))()
