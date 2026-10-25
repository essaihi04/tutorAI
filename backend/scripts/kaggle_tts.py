"""Outils de la voix Kaggle à la demande.

    python -m scripts.kaggle_tts socle    # une fois : prépare le socle (CPU, sans quota GPU)
    python -m scripts.kaggle_tts statut   # état des kernels socle / direct sur Kaggle
    python -m scripts.kaggle_tts journal  # dernières lignes du kernel direct
    python -m scripts.kaggle_tts essai    # réveil réel + mesures (démarrage, premier son, vitesse)
    python -m scripts.kaggle_tts banc     # banc fp32 / fp16 (kernel séparé, ~15 min GPU)

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
ESSAI = "academy-tts-essai"


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


PHRASES_ESSAI = [
    ("ma", "دابا غادي نشوفو الشحن ديال المكثف، و شنو كيوقع للتوتر ديالو مع الوقت."),
    ("fr", "Donc retiens bien : la constante de temps tau est égale à R fois C."),
    ("fr", "Bonjour ! Aujourd'hui, on étudie le dipôle RC. Il est formé d'un conducteur ohmique et d'un "
           "condensateur montés en série. Quand on ferme l'interrupteur, le condensateur se charge "
           "progressivement. Qu'est-ce qui se passe pour la tension à ses bornes ?"),
]


def essai():
    """Réveille un kernel direct comme le ferait une séance, puis mesure.

    L'annonce au backend est refusée (clé inconnue de lui) : l'essai ne touche
    pas à la voix servie aux élèves. Le kernel s'éteint seul après la veille.
    """
    import re
    import secrets
    import subprocess
    import time

    import httpx

    from app.services.kaggle_tts import pousser_kernel
    jeton = secrets.token_urlsafe(24)
    t0 = time.time()
    # Kernel à part : pousser une nouvelle version de academy-tts-direct
    # couperait la voix d'une séance en cours.
    print(pousser_kernel(secrets.token_urlsafe(24), "essai", jeton, kernel=ESSAI).splitlines()[-1])
    print(f"poussé en {time.time() - t0:.1f} s ; suivi du journal…")
    env = {**__import__("os").environ, "KAGGLE_USERNAME": settings.kaggle_username,
           "KAGGLE_API_TOKEN": settings.kaggle_api_token}
    url, etapes = None, {}
    while not etapes.get("pret") and time.time() - t0 < 900:
        p = subprocess.Popen([sys.executable, "-m", "kaggle", "kernels", "logs", "-f",
                              f"{settings.kaggle_username}/{ESSAI}"],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env,
                             encoding="utf-8", errors="replace")
        for ligne in p.stdout:
            # Motifs sans accents : selon la locale, le CLI rend « prêt » en « prÃªt ».
            for cle, motif in (("socle", "socle :"), ("tunnel", "tunnel https"), ("copie", "en local"),
                               ("deps", "pendances pr"), ("gpu0", "gpu0 pr"), ("gpu1", "gpu1 pr"),
                               ("pret", " s sur "), ("echec", "CHEC")):
                if motif in ligne and cle not in etapes:
                    etapes[cle] = time.time() - t0
                    print(f"  +{etapes[cle]:6.1f} s  {ligne.strip()[:150]}")
            m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", ligne)
            if m and not url:
                url = m.group(0)
            if "Traceback" in ligne or "Error:" in ligne:
                print("  !", ligne.strip()[:200])
            if etapes.get("pret"):
                break
        p.kill()
        if not etapes.get("pret"):
            time.sleep(10)          # le kernel est encore en file : les journaux ne sont pas ouverts
    if not url or not etapes.get("pret"):
        print("pas prêt après 15 min — voir `journal`")
        return
    print(f"\nDÉMARRAGE À FROID : {etapes['pret']:.0f} s (push → voix prête)\n")
    h = {"Authorization": f"Bearer {jeton}"}
    with httpx.Client(timeout=120) as c:
        t = time.time()
        c.get(f"{url}/health", headers=h)
        print(f"aller-retour tunnel (/health) : {(time.time() - t) * 1000:.0f} ms")
        for langue, texte in PHRASES_ESSAI:
            t = time.time()
            premier, octets = None, 0
            with c.stream("POST", f"{url}/tts/stream", json={"texte": texte, "langue": langue}, headers=h) as r:
                for b in r.iter_bytes():
                    octets += len(b)
                    if premier is None and octets > 44:
                        premier = time.time() - t
            total = time.time() - t
            duree = (octets - 44) / 2 / 24000
            print(f"[{langue}] {len(texte):3d} car. : premier son {premier:.2f} s, fini {total:.2f} s, "
                  f"audio {duree:.1f} s, vitesse {total / max(duree, 0.01):.2f}× temps réel")
    print("\nLe kernel s'éteindra seul après", settings.kaggle_tts_veille_s, "s sans parler.")


def banc():
    import base64
    d = Path(tempfile.mkdtemp(prefix="banc_"))
    try:
        ref = base64.b64encode((DOSSIER_KERNEL / "reference_amine.flac").read_bytes()).decode()
        source = (DOSSIER_KERNEL / "banc_fp16.py").read_text(encoding="utf-8")
        source = source.replace('"__REF_B64__"', repr(ref), 1).replace('"__MODELE__"', repr(settings.kaggle_tts_modele), 1)
        (d / "banc.py").write_text(source, encoding="utf-8")
        u = settings.kaggle_username
        meta = {"id": f"{u}/academy-tts-banc-fp16", "title": "academy-tts-banc-fp16", "code_file": "banc.py",
                "language": "python", "kernel_type": "script", "is_private": True, "enable_gpu": True,
                "enable_internet": True, "machine_shape": "NvidiaTeslaT4", "dataset_sources": [],
                "competition_sources": [],
                "kernel_sources": [f"{u}/{settings.kaggle_tts_modele}", f"{u}/{SOCLE}"]}
        (d / "kernel-metadata.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
        print(kaggle_cli("kernels", "push", "-p", str(d), "-t", "2400"))
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    {"socle": socle, "statut": statut, "journal": journal, "essai": essai, "banc": banc}.get(sys.argv[1] if len(sys.argv) > 1 else "",
                                                               lambda: print(__doc__))()
