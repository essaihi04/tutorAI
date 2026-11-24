"""Publie le lien libre du Tronc Commun SVT : https://moalim.online/tronc-commun/ (22 novembre 2026).

Deux cours (« La sortie écologique », « Les facteurs édaphiques » activités 1 à 7) et une évaluation formative,
hors du site : ni dans la base des élèves, ni dans l'application. Comme `publier_cours_ondes.py` : une page construite à
part, publiée dans son propre dossier du serveur, sans commit ni déploiement du site et sans toucher à nginx
(`location /` fait `try_files $uri $uri/ /index.html` : le dossier `tronc-commun/` est servi tel quel).

  1. construit la page (`frontend/vite.tronc-commun.config.ts`, base `/tronc-commun/`) ;
  2. copie seulement les médias qu'elle utilise (simulations à la craie des deux cours, images des documents, kit du
     tableau, professeur 3D, réactions), en suivant les chemins `/media/...` de proche en proche ;
  3. convertit les pistes WAV des deux cours en MP3, quand la voix aura été enregistrée ;
  4. préfixe tous les chemins `/media/` par `/tronc-commun/` : rien n'est lu dans les médias du site ;
  5. envoie le dossier sur moalim-vps et le met en place d'un coup (`/var/www/moalim/tronc-commun`).
     `deploy-ubuntu.sh` n'efface que `assets` et `blog` : le dossier survit aux déploiements du site.

Usage :  python -I scripts/publier_tronc_commun.py [--sans-envoi]
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
#: Hors du dépôt : rien à ignorer, rien à commiter par erreur.
SORTIE = Path(tempfile.gettempdir()) / "moalim-tronc-commun"
PREFIXE = "/tronc-commun"
DEST = "/var/www/moalim/tronc-commun"
#: Dossiers copiés en entier (les pages s'y servent de chemins relatifs, ou le lecteur compose les noms).
DOSSIERS = ["media/simulations/shared/tableau", "media/audio/reactions", "media/tronc-commun",
            "media/simulations/svt/tc_sortie_ecologique-tableau", "media/simulations/svt/tc_facteurs_edaphiques-tableau",
            "media/simulations/svt/tc_revision-tableau",
            # voix Bodi (MP3) : l'évaluation compose ses chemins, les cours les citent
            "media/audio/courses/tc_svt_examen", "media/audio/courses/tc_svt_revision",
            "media/audio/courses/tc_svt_sortie_ecologique", "media/audio/courses/tc_svt_facteurs_edaphiques"]
FICHIERS = ["media/simulations/professor-locate.js", "media/avatar/moalim-professeur.glb", "media/avatar/moalim-professeur.png",
            "media/audio/reactions/manifest.json"]
TEXTE = {".js", ".html", ".css", ".json", ".mjs"}
REF = re.compile(r"/media/[A-Za-z0-9_\-./%]+")
PISTE = re.compile(r"(/media/audio/courses/tc_svt_[a-z_]+/[^\"'`\\\s]+?)\.wav")


def lancer(*cmd: str, **kw) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True, **kw)


def construire() -> None:
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    lancer(npx, "vite", "build", "--config", "vite.tronc-commun.config.ts", "--outDir", str(SORTIE), cwd=FRONT)
    (SORTIE / "tronc-commun.html").replace(SORTIE / "index.html")


def copier_medias() -> list[Path]:
    """Copie les médias utilisés ; renvoie les pistes WAV à convertir."""
    a_copier = {Path(f) for f in FICHIERS}
    for d in DOSSIERS:
        if (PUBLIC / d).is_dir():
            a_copier |= {p.relative_to(PUBLIC) for p in (PUBLIC / d).rglob("*") if p.is_file()}
    a_lire = [p for p in SORTIE.rglob("*") if p.suffix in TEXTE] + [PUBLIC / f for f in a_copier if (PUBLIC / f).suffix in TEXTE]
    vus: set[Path] = set()
    while a_lire:
        f = a_lire.pop()
        if f in vus or not f.exists():
            continue
        vus.add(f)
        for ref in REF.findall(f.read_text(encoding="utf-8", errors="ignore")):
            rel = Path(ref.lstrip("/").split("?")[0].split("#")[0].rstrip("."))
            if (PUBLIC / rel).is_file() and rel not in a_copier:
                a_copier.add(rel)
                if rel.suffix in TEXTE:
                    a_lire.append(PUBLIC / rel)
    wav, absents = [], []
    for rel in sorted(a_copier):
        src = PUBLIC / rel
        if not src.is_file():
            absents.append(rel)
            continue
        dst = SORTIE / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix == ".wav" and "/tc_svt_" in "/" + rel.as_posix():
            wav.append(rel)
            continue
        shutil.copyfile(src, dst)
    for rel in absents:
        print("  absent :", rel)
    print(len(a_copier), "médias ;", len(wav), "pistes à convertir")
    return wav


def convertir(wav: list[Path]) -> None:
    for rel in wav:
        dst = (SORTIE / rel).with_suffix(".mp3")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(PUBLIC / rel), "-ac", "1", "-codec:a", "libmp3lame", "-q:a", "5", str(dst)], check=True)


def prefixer() -> None:
    """`/media/…` → `/tronc-commun/media/…`, et les pistes des cours en .mp3, dans la page et dans les médias texte."""
    for f in SORTIE.rglob("*"):
        if f.suffix not in TEXTE:
            continue
        t = f.read_text(encoding="utf-8")
        u = PISTE.sub(r"\1.mp3", t)
        u = re.sub(r"(?<![\w/])/media/", PREFIXE + "/media/", u)
        if u != t:
            f.write_text(u, encoding="utf-8")


def envoyer() -> None:
    archive = SORTIE.parent / "tronc-commun.tar.gz"
    lancer("tar", "-czf", str(archive), "-C", str(SORTIE), ".")
    lancer("scp", str(archive), "moalim-vps:/tmp/tronc-commun.tar.gz")
    lancer("ssh", "moalim-vps", f"set -e; rm -rf {DEST}.nouveau; mkdir -p {DEST}.nouveau; tar -xzf /tmp/tronc-commun.tar.gz -C {DEST}.nouveau; "
           f"chmod -R a+rX {DEST}.nouveau; rm -rf {DEST}.ancien; [ -d {DEST} ] && mv {DEST} {DEST}.ancien || true; "
           f"mv {DEST}.nouveau {DEST}; rm -rf {DEST}.ancien /tmp/tronc-commun.tar.gz; du -sh {DEST}")
    archive.unlink()


if __name__ == "__main__":
    construire()
    convertir(copier_medias())
    prefixer()
    taille = sum(p.stat().st_size for p in SORTIE.rglob("*") if p.is_file()) / 1e6
    print(f"page prête : {SORTIE} ({taille:.1f} Mo)")
    if "--sans-envoi" not in sys.argv:
        envoyer()
        print("en ligne : https://moalim.online/tronc-commun/")
