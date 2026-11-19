"""Repère les lignes de texte d'une page scannée d'un sujet du national (19 novembre 2026).

Pour construire un énoncé « tel qu'à l'examen » (skill professeur règle 46) dans
`frontend/public/media/simulations/chimie/shared/enonces.json` : il faut, pour chaque donnée lue par le tuteur,
la bande verticale où elle est écrite sur le scan. Ce script découpe la page en lignes d'encre (profil
horizontal), écrit une image annotée (numéro et y en fraction de la page à gauche de chaque ligne) et la liste
des bandes en JSON.

  python scripts/examens/lignes_page.py backend/data/exams/physique/2021-normale/pages/sujet_p2.jpg <sortie_dir> [y0 y1]

Sortie : <sortie_dir>/<annee-session>_<page>.png (largeur 1100 px, recadrée sur y0..y1 si donnés) et .json
[{n, y0, y1}] en fractions de la hauteur de la page (0 = haut).
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def bandes(img, x0=.07, x1=.95, seuil=150, min_ink=6, gap=5):
    g = img.convert("L")
    W, H = g.size
    px = g.load()
    xa, xb = int(W * x0), int(W * x1)
    rows = []
    for y in range(H):
        n = 0
        for x in range(xa, xb, 2):
            if px[x, y] < seuil:
                n += 1
        rows.append(n)
    out, debut, vide = [], None, 0
    for y, n in enumerate(rows):
        if n >= min_ink:
            if debut is None:
                debut = y
            vide = 0
        elif debut is not None:
            vide += 1
            if vide > gap:
                fin = y - vide
                if fin - debut >= 8:
                    out.append((debut, fin))
                debut, vide = None, 0
    if debut is not None:
        out.append((debut, H - 1))
    return [{"n": i + 1, "y0": round(a / H, 4), "y1": round(b / H, 4)} for i, (a, b) in enumerate(out)]


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    ya, yb = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (0.0, 1.0)
    dst.mkdir(parents=True, exist_ok=True)
    img = Image.open(src).convert("RGB")
    W, H = img.size
    bs = [b for b in bandes(img) if b["y1"] >= ya and b["y0"] <= yb]
    crop = img.crop((0, int(H * ya), W, int(H * yb)))
    d = ImageDraw.Draw(crop)
    try:
        f = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
    except OSError:
        f = ImageFont.load_default()
    for b in bs:
        y = int(H * b["y0"]) - int(H * ya)
        d.rectangle((0, y, 8, int(H * b["y1"]) - int(H * ya)), fill=(220, 0, 0))
        d.text((10, y - 4), f"{b['n']}:{b['y0']:.3f}", fill=(220, 0, 0), font=f)
    k = 1100 / W
    crop = crop.resize((1100, max(1, int(crop.height * k))))
    nom = f"{src.parent.parent.name}_{src.stem}"
    crop.save(dst / f"{nom}.png")
    (dst / f"{nom}.json").write_text(json.dumps(bs, indent=0))
    print(dst / f"{nom}.png", len(bs), "lignes")


if __name__ == "__main__":
    main()
