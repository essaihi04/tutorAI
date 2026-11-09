"""Outils de la voix Kaggle à la demande.

    python -m scripts.kaggle_tts socle    # une fois : prépare le socle (CPU, sans quota GPU)
    python -m scripts.kaggle_tts statut   # état des kernels socle / direct sur Kaggle
    python -m scripts.kaggle_tts journal  # dernières lignes du kernel direct
    python -m scripts.kaggle_tts essai    # réveil réel + mesures (démarrage, premier son, vitesse)
    python -m scripts.kaggle_tts banc     # banc fp32 / fp16 (kernel séparé, ~15 min GPU)
    python -m scripts.kaggle_tts reactions  # enregistre les réactions immédiates (voix Amine)
    python -m scripts.kaggle_tts cours FICHIER  # enregistre d'avance les phrases des cours (cache)

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


def _reveiller_essai():
    """Pousse le serveur sur le kernel d'essai et attend qu'il soit prêt.

    Rend (url, jeton, étapes) ou None. L'annonce au backend est refusée (clé
    inconnue de lui) : l'essai ne touche pas à la voix servie aux élèves. Le
    kernel s'éteint seul après la veille.
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
        return None
    print(f"\nDÉMARRAGE À FROID : {etapes['pret']:.0f} s (push → voix prête)\n")
    return url, jeton, etapes


def essai():
    """Réveille un kernel d'essai comme le ferait une séance, puis mesure."""
    import time

    import httpx

    reveil = _reveiller_essai()
    if not reveil:
        return
    url, jeton, _ = reveil
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
        if settings.kaggle_stt_modele:
            essai_stt(c, url, h)
    print("\nLe kernel s'éteindra seul après", settings.kaggle_tts_veille_s, "s sans parler.")


def essai_stt(c, url, h):
    """Reconnaissance vocale du kernel : attend /health stt=pret, puis transcrit des extraits du test figé
    (chemins dans STT_CLIPS, séparés par des virgules) et un aller-retour voix -> texte."""
    import os
    import time
    t0, etat = time.time(), None
    while time.time() - t0 < 600:
        etat = c.get(f"{url}/health", headers=h).json().get("stt")
        if etat in ("pret", "echec", "absent"):
            break
        time.sleep(5)
    print(f"\nSTT : {etat} ({time.time() - t0:.0f} s après la voix)")
    if etat != "pret":
        return
    audios = [(p, Path(p).read_bytes()) for p in filter(None, os.environ.get("STT_CLIPS", "").split(","))]
    r = c.post(f"{url}/tts", json={"texte": PHRASES_ESSAI[0][1], "langue": "ma"}, headers=h)
    audios.append(("voix du prof : " + PHRASES_ESSAI[0][1], r.content))
    for nom, octets in audios:
        for _ in range(2):          # la 2e fois : temps « à chaud »
            t = time.time()
            r = c.post(f"{url}/stt", params={"langue": "mixed"}, content=octets, headers=h)
            d = r.json() if r.status_code == 200 else {"texte": r.text[:120]}
            print(f"[stt] {r.status_code} aller-retour {(time.time() - t) * 1000:.0f} ms, calcul {d.get('calcul_ms')} ms, "
                  f"audio {d.get('duree_s')} s | {Path(nom).name if '/' in nom else nom}\n   -> {d.get('texte')}")


def banc():
    import base64
    d = Path(tempfile.mkdtemp(prefix="banc_"))
    try:
        ref = base64.b64encode((DOSSIER_KERNEL / settings.kaggle_tts_reference).read_bytes()).decode()
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


def reactions(sortie: str = "/tmp/reactions"):
    """Enregistre les réactions immédiates (kaggle_tts/reactions.json) avec la
    voix d'Amine, sur le kernel d'essai : un WAV par phrase + manifest.json,
    à copier dans frontend/public/media/audio/reactions/."""
    import httpx

    phrases = json.loads((DOSSIER_KERNEL / "reactions.json").read_text(encoding="utf-8"))["reactions"]
    reveil = _reveiller_essai()
    if not reveil:
        return
    url, jeton, _ = reveil
    dossier = Path(sortie)
    dossier.mkdir(parents=True, exist_ok=True)
    h = {"Authorization": f"Bearer {jeton}"}
    faites = []
    with httpx.Client(timeout=120) as c:
        for r in phrases:
            rep = c.post(f"{url}/tts", json={"texte": r["texte"], "langue": "fr" if r["lang"] == "fr" else "ma"},
                         headers=h)
            if rep.status_code != 200 or not rep.content.startswith(b"RIFF"):
                print("échec", r["id"], rep.status_code)
                continue
            (dossier / f"{r['id']}.wav").write_bytes(rep.content)
            faites.append({**r, "url": f"/media/audio/reactions/{r['id']}.wav"})
            print(r["id"], f"{(len(rep.content) - 44) / 2 / 24000:.1f} s", r["texte"])
    (dossier / "manifest.json").write_text(
        json.dumps({"voix": "academy-v4-amine-vif", "reactions": faites}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    print(len(faites), "/", len(phrases), "réactions dans", dossier)


def cours(fichier: str = "/tmp/phrases_cours.json"):
    """Enregistre d'avance, dans le cache vocal du backend, les phrases que le
    tableau des cours prononce (lignes écrites, questions) : elles partent
    ensuite sans attente ni GPU (cf. `synthesize`, qui lit ce cache en premier).

    La liste vient du code même de la page (slideVersScript + toSpokenText),
    pour que les clés de cache soient identiques à celles du tableau. À relancer
    après toute modification d'un cours.
    """
    import asyncio
    import time

    from app.services import kaggle_tts
    from app.services import tts_service

    phrases = json.loads(Path(fichier).read_text(encoding="utf-8"))
    reveil = _reveiller_essai()
    if not reveil:
        return
    url, jeton, _ = reveil
    # Ce processus parle au kernel d'essai, pas à celui des élèves.
    kaggle_tts.pilote.cible = lambda: (url, jeton)
    kaggle_tts.pilote.besoin_de_voix = lambda *a, **k: None

    async def tout():
        sem = asyncio.Semaphore(4)
        faits = {"neuf": 0, "deja": 0, "echec": 0}
        t0 = time.time()

        async def une(p):
            async with sem:
                r = await tts_service.synthesize(p["texte"], p["lang"])
                cle = "deja" if r.cached else ("neuf" if r.audio_b64 and r.provider == "academy" else "echec")
                faits[cle] += 1
                n = sum(faits.values())
                if n % 25 == 0 or cle == "echec":
                    print(f"{n}/{len(phrases)} {faits} {time.time() - t0:.0f} s"
                          + (f" — échec : {p['texte'][:60]}" if cle == "echec" else ""), flush=True)

        await asyncio.gather(*(une(p) for p in phrases))
        print("terminé :", faits, f"en {time.time() - t0:.0f} s")

    asyncio.run(tout())


if __name__ == "__main__":
    {"socle": socle, "statut": statut, "journal": journal, "essai": essai, "banc": banc, "reactions": reactions,
     "cours": lambda: cours(*sys.argv[2:3])}.get(sys.argv[1] if len(sys.argv) > 1 else "",
                                                               lambda: print(__doc__))()
