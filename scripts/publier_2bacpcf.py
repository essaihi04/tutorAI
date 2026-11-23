"""Publie le lien libre des révisions de 2ᵉ Bac PC : https://moalim.online/2bacpcf/ (23 novembre 2026).

Deux séances de révision assemblées à partir des cours existants (voix déjà enregistrées) et deux examens de 30 min
faits d'exercices existants (`scripts/sujets_2bacpcf.py`). Comme `publier_tronc_commun.py` : page construite à part
(`frontend/vite.2bacpcf.config.ts`), médias copiés un à un en suivant les chemins `/media/...`, préfixés par
`/2bacpcf/`, envoyés dans `/var/www/moalim/2bacpcf` ; ni déploiement du site ni nginx.
Les médias absents de ce dépôt (copie partielle) sont cherchés dans `--public-secours <dossier frontend/public>`.

Usage :  python -I scripts/publier_2bacpcf.py [--sans-envoi] [--public-secours C:/…/frontend/public]
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
SECOURS = Path(sys.argv[sys.argv.index("--public-secours") + 1]) if "--public-secours" in sys.argv else None
SORTIE = Path(tempfile.gettempdir()) / "moalim-2bacpcf"
PREFIXE = "/2bacpcf"
DEST = "/var/www/moalim/2bacpcf"
DOSSIERS = ["media/simulations/shared/tableau", "media/audio/reactions"]
FICHIERS = ["media/simulations/professor-locate.js", "media/avatar/moalim-professeur.glb", "media/avatar/moalim-professeur.png",
            "media/audio/reactions/manifest.json"]
TEXTE = {".js", ".html", ".css", ".json", ".mjs"}
REF = re.compile(r"/media/[A-Za-z0-9_\-./%]+")
PISTE = re.compile(r"(/media/audio/(?:courses|exercices)/[a-z0-9_]+/[^\"'`\\\s]+?)\.wav")


def src(rel: Path) -> Path:
    """le fichier dans ce dépôt, sinon dans le public de secours (copie complète des médias)"""
    p = PUBLIC / rel
    return p if p.exists() or SECOURS is None else SECOURS / rel


def lancer(*cmd: str, **kw) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True, **kw)


def construire() -> None:
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    lancer(npx, "vite", "build", "--config", "vite.2bacpcf.config.ts", "--outDir", str(SORTIE), cwd=FRONT)
    (SORTIE / "2bacpcf.html").replace(SORTIE / "index.html")


def copier_medias() -> list[Path]:
    a_copier = {Path(f) for f in FICHIERS}
    for d in DOSSIERS:
        if src(Path(d)).is_dir():
            a_copier |= {Path(d) / p.relative_to(src(Path(d))) for p in src(Path(d)).rglob("*") if p.is_file()}
    a_lire = [p for p in SORTIE.rglob("*") if p.suffix in TEXTE] + [src(f) for f in a_copier if f.suffix in TEXTE]
    vus: set[Path] = set()
    while a_lire:
        f = a_lire.pop()
        if f in vus or not f.exists():
            continue
        vus.add(f)
        for ref in REF.findall(f.read_text(encoding="utf-8", errors="ignore")):
            rel = Path(ref.lstrip("/").split("?")[0].split("#")[0].rstrip("."))
            if src(rel).is_file() and rel not in a_copier:
                a_copier.add(rel)
                if rel.suffix in TEXTE:
                    a_lire.append(src(rel))
    # une simulation se sert de fichiers voisins (css, commun.js…) : son dossier entier
    for rel in list(a_copier):
        p = rel.parts
        if len(p) >= 5 and p[0] == "media" and p[1] == "simulations" and rel.suffix == ".html":
            dossier = src(Path(*p[:4]))
            if dossier.is_dir():
                a_copier |= {Path(*p[:4]) / f.relative_to(dossier) for f in dossier.rglob("*") if f.is_file()}
    wav, absents = [], []
    for rel in sorted(a_copier):
        source = src(rel)
        if not source.is_file():
            absents.append(rel)
            continue
        dst = SORTIE / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix == ".wav":
            wav.append(rel)
            continue
        shutil.copyfile(source, dst)
    for rel in absents:
        print("  absent :", rel)
    print(len(a_copier), "médias ;", len(wav), "pistes à convertir ;", len(absents), "absents")
    return wav


def convertir(wav: list[Path]) -> None:
    for rel in wav:
        dst = (SORTIE / rel).with_suffix(".mp3")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src(rel)), "-ac", "1", "-codec:a", "libmp3lame", "-q:a", "5", str(dst)], check=True)


def prefixer() -> None:
    for f in SORTIE.rglob("*"):
        if f.suffix not in TEXTE:
            continue
        t = f.read_text(encoding="utf-8")
        u = PISTE.sub(r"\1.mp3", t)
        u = re.sub(r"(?<![\w/])/media/", PREFIXE + "/media/", u)
        if u != t:
            f.write_text(u, encoding="utf-8")


def envoyer() -> None:
    archive = SORTIE.parent / "2bacpcf.tar.gz"
    lancer("tar", "-czf", str(archive), "-C", str(SORTIE), ".")
    lancer("scp", str(archive), "moalim-vps:/tmp/2bacpcf.tar.gz")
    lancer("ssh", "moalim-vps", f"set -e; rm -rf {DEST}.nouveau; mkdir -p {DEST}.nouveau; tar -xzf /tmp/2bacpcf.tar.gz -C {DEST}.nouveau; "
           f"chmod -R a+rX {DEST}.nouveau; rm -rf {DEST}.ancien; [ -d {DEST} ] && mv {DEST} {DEST}.ancien || true; "
           f"mv {DEST}.nouveau {DEST}; rm -rf {DEST}.ancien /tmp/2bacpcf.tar.gz; du -sh {DEST}")
    archive.unlink()


if __name__ == "__main__":
    construire()
    convertir(copier_medias())
    prefixer()
    taille = sum(p.stat().st_size for p in SORTIE.rglob("*") if p.is_file()) / 1e6
    print(f"page prête : {SORTIE} ({taille:.1f} Mo)")
    if "--sans-envoi" not in sys.argv:
        envoyer()
        print("en ligne : https://moalim.online/2bacpcf/")
