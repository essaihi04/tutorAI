"""Publie le cours exemple des ondes, en accès libre : https://moalim.online/cours-ondes/

Depuis le 10 novembre 2026, la même page sert aussi les autres cours refaits (`?cours=<id>`, relecture des profs).

Le cours est encore hors du site (il n'est pas dans la base) : on le publie comme une page à part, dans son propre
dossier du serveur, sans commit ni déploiement du site, et sans toucher à la configuration nginx (`location /` sert
déjà `cours-ondes/index.html`) ni aux médias du site.

  1. construit la page (`frontend/vite.cours-ondes.config.ts`, base `/cours-ondes/`) ;
  2. copie seulement les médias qu'elle utilise (simulations à la craie, kit du tableau, professeur 3D, pistes et
     réactions du cours), en suivant les chemins `/media/...` de proche en proche ;
  3. convertit les pistes WAV en MP3 (115 Mo → une douzaine : la page doit se charger sur un téléphone) ;
  4. préfixe tous les chemins `/media/` par `/cours-ondes/` : rien n'est lu dans les médias du site, qu'un
     déploiement du site peut remplacer à tout moment ;
  5. envoie le dossier sur moalim-vps et le met en place d'un coup (`/var/www/moalim/cours-ondes`).
     `deploy-ubuntu.sh` n'efface que `assets` et `blog` : le dossier survit aux déploiements du site.

Usage :  python -I scripts/publier_cours_ondes.py [--sans-envoi]
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
FRONT = RACINE / "frontend"
PUBLIC = FRONT / "public"
#: Hors du dépôt (partagé avec d'autres sessions) : rien à ignorer, rien à commiter par erreur.
SORTIE = Path(tempfile.gettempdir()) / "moalim-cours-ondes"
PREFIXE = "/cours-ondes"
DEST = "/var/www/moalim/cours-ondes"
#: Dossiers copiés en entier : les pages s'y servent de chemins relatifs (ondes.css, commun.js…).
DOSSIERS = ["media/simulations/physics/ondes-tableau", "media/simulations/shared/tableau"]
FICHIERS = ["media/simulations/professor-locate.js", "media/avatar/moalim-professeur.glb", "media/avatar/moalim-professeur.png",
            "media/audio/reactions/manifest.json"]
TEXTE = {".js", ".html", ".css", ".json", ".mjs"}
REF = re.compile(r"/media/[A-Za-z0-9_\-./%]+")
PISTE = re.compile(r"(/media/audio/courses/phys_ch1_waves_exemple/[^\"'`\\\s]+?)\.wav")


def lancer(*cmd: str, **kw) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True, **kw)


def construire() -> None:
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    lancer(npx, "vite", "build", "--config", "vite.cours-ondes.config.ts", "--outDir", str(SORTIE), cwd=FRONT)
    (SORTIE / "cours-ondes.html").replace(SORTIE / "index.html")


def copier_medias() -> list[Path]:
    """Copie les médias utilisés ; renvoie les pistes WAV à convertir."""
    a_copier = {Path(f) for f in FICHIERS}
    for d in DOSSIERS:
        a_copier |= {p.relative_to(PUBLIC) for p in (PUBLIC / d).rglob("*") if p.is_file()}
    # les chemins cités par la page construite et, de proche en proche, par les médias copiés
    a_lire = [p for p in SORTIE.rglob("*") if p.suffix in TEXTE] + [PUBLIC / f for f in a_copier if (PUBLIC / f).suffix in TEXTE]
    vus: set[Path] = set()
    while a_lire:
        f = a_lire.pop()
        if f in vus or not f.exists():
            continue
        vus.add(f)
        for ref in REF.findall(f.read_text(encoding="utf-8", errors="ignore")):
            rel = Path(ref.lstrip("/").split("?")[0].rstrip("."))
            if (PUBLIC / rel).is_file() and rel not in a_copier:
                a_copier.add(rel)
                if rel.suffix in TEXTE:
                    a_lire.append(PUBLIC / rel)
    # Une simulation se sert de fichiers voisins par chemins relatifs (ondes.css, commun.js…) : on copie son dossier
    # entier (cours de relecture du 10 novembre 2026 : ondes-periodiques-tableau/…).
    for rel in list(a_copier):
        p = rel.parts
        if len(p) >= 5 and p[0] == "media" and p[1] == "simulations" and rel.suffix == ".html":
            dossier = PUBLIC / Path(*p[:4])
            a_copier |= {f.relative_to(PUBLIC) for f in dossier.rglob("*") if f.is_file()}
    wav = []
    for rel in sorted(a_copier):
        src = PUBLIC / rel
        if not src.is_file():
            print("  absent :", rel)
            continue
        dst = SORTIE / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix == ".wav" and "phys_ch1_waves_exemple" in rel.as_posix():
            wav.append(rel)
            continue
        shutil.copyfile(src, dst)
    print(len(a_copier), "médias ;", len(wav), "pistes à convertir")
    return wav


def convertir(wav: list[Path]) -> None:
    for rel in wav:
        dst = (SORTIE / rel).with_suffix(".mp3")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(PUBLIC / rel), "-ac", "1", "-codec:a", "libmp3lame", "-q:a", "5", str(dst)], check=True)


def prefixer() -> None:
    """`/media/…` → `/cours-ondes/media/…`, et les pistes du cours en .mp3, dans la page et dans les médias texte."""
    for f in SORTIE.rglob("*"):
        if f.suffix not in TEXTE:
            continue
        t = f.read_text(encoding="utf-8")
        u = PISTE.sub(r"\1.mp3", t)
        u = re.sub(r"(?<![\w/])/media/", PREFIXE + "/media/", u)
        if u != t:
            f.write_text(u, encoding="utf-8")


def envoyer() -> None:
    archive = SORTIE.parent / "cours-ondes.tar.gz"
    lancer("tar", "-czf", str(archive), "-C", str(SORTIE), ".")
    lancer("scp", str(archive), "moalim-vps:/tmp/cours-ondes.tar.gz")
    lancer("ssh", "moalim-vps", f"set -e; rm -rf {DEST}.nouveau; mkdir -p {DEST}.nouveau; tar -xzf /tmp/cours-ondes.tar.gz -C {DEST}.nouveau; "
           f"chmod -R a+rX {DEST}.nouveau; rm -rf {DEST}.ancien; [ -d {DEST} ] && mv {DEST} {DEST}.ancien || true; "
           f"mv {DEST}.nouveau {DEST}; rm -rf {DEST}.ancien /tmp/cours-ondes.tar.gz; du -sh {DEST}")
    archive.unlink()


if __name__ == "__main__":
    construire()
    convertir(copier_medias())
    prefixer()
    taille = sum(p.stat().st_size for p in SORTIE.rglob("*") if p.is_file()) / 1e6
    print(f"page prête : {SORTIE} ({taille:.1f} Mo)")
    if "--sans-envoi" not in sys.argv:
        envoyer()
        print("en ligne : https://moalim.online/cours-ondes/")
