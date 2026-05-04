"""Attach missing figures to 3 math exams.

Approach: crop the relevant figure region from sujet_pN.jpg (estimated
coordinates based on visual inspection), save under assets/, and add
a `documents` entry to the exercise in exam.json.

Crop coordinates are expressed as fractions of (width, height) so they
work regardless of the JPG resolution.
"""
from __future__ import annotations
import json, sys, shutil
from pathlib import Path
from PIL import Image

DRY = '--apply' not in sys.argv
ROOT = Path('backend/data/exams/mathematiques')

# (folder, ex_index, source_page, crop_box_fractional, doc_id, title, description)
JOBS = [
    (
        '2018-rattrapage', 4, 'sujet_p4.jpg',
        # Page 4 of 2018-rattrapage: figure (C_h) in upper-right, ~x=0.62-1.0, y=0.10-0.32
        (0.60, 0.10, 0.99, 0.34),
        'doc_ex5_ch',
        'Figure ci-contre — Représentation graphique de h',
        "Représentation graphique (C_h) de la fonction h sur ]0, +∞[. La courbe coupe l'axe des abscisses au point d'abscisse 1, est décroissante puis tend vers la droite asymptotique y = -1/2 quand x → +∞.",
    ),
    (
        '2022-normale', 4, 'sujet_p4.jpg',
        # Page 4 of 2022-normale: figure (C_g) in upper-right
        (0.55, 0.06, 0.98, 0.34),
        'doc_ex5_cg',
        'Courbe ci-contre — Fonction g',
        "Courbe représentative de la fonction g(x) = (2x+4)e^(x/2) - x - 4. La courbe possède une racine en x = α (avec α ≈ -4,5), passe par un minimum dans la région x ≈ -2, puis croît rapidement.",
    ),
    (
        '2024-rattrapage', 3, 'sujet_p3.jpg',
        # Page 3 of 2024-rattrapage: figure (C_g), (C_h), y=x in upper-right of Problème
        (0.55, 0.30, 0.98, 0.55),
        'doc_ex4_cg_ch',
        "Figure ci-contre — Courbes (C_g), (C_h) et droite y = x",
        "Représentation graphique des courbes (C_g) de g(x) = x/(1+x), (C_h) de h(x) = ln(1+x), et de la droite y = x dans un repère orthonormé sur ]-1, +∞[. Les trois courbes sont rangées : g(x) ≤ ln(1+x) ≤ x.",
    ),
]


def crop_and_save(src_jpg: Path, box_frac: tuple, dst_jpg: Path):
    img = Image.open(src_jpg)
    w, h = img.size
    x0, y0, x1, y1 = box_frac
    box = (int(w * x0), int(h * y0), int(w * x1), int(h * y1))
    cropped = img.crop(box)
    dst_jpg.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(dst_jpg, 'JPEG', quality=92)
    return cropped.size


for folder, ex_idx, page_name, box, doc_id, title, description in JOBS:
    print('=' * 70)
    exam_dir = ROOT / folder
    src = exam_dir / 'pages' / page_name
    dst = exam_dir / 'assets' / f'{doc_id}.jpg'
    print(f'{folder}  Ex{ex_idx+1}')
    print(f'  src: {src}')
    print(f'  dst: {dst}')
    print(f'  crop box (fractional): {box}')

    if not src.exists():
        print(f'  ✗ source missing — SKIP')
        continue

    if DRY:
        img = Image.open(src)
        w, h = img.size
        bb = (int(w * box[0]), int(h * box[1]), int(w * box[2]), int(h * box[3]))
        print(f'  page size: {w}x{h}, would crop to: {bb}, output ~{bb[2]-bb[0]}x{bb[3]-bb[1]}')
    else:
        size = crop_and_save(src, box, dst)
        print(f'  ✓ cropped to {size}')

    # Update exam.json
    exam_json = exam_dir / 'exam.json'
    d = json.loads(exam_json.read_text(encoding='utf-8-sig'))
    ex = d['parts'][0]['exercises'][ex_idx]
    docs = ex.setdefault('documents', [])
    # Avoid double-add
    if any(doc.get('id') == doc_id for doc in docs):
        print(f'  [SKIP] document {doc_id} already in exam.json')
    else:
        docs.append({
            'id': doc_id,
            'type': 'figure',
            'title': title,
            'description': description,
            'src': f'assets/{doc_id}.jpg',
        })
        if not DRY:
            exam_json.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f'  ✓ exam.json updated')
        else:
            print(f'  [DRY] would add document entry')

print()
if DRY:
    print('Re-run with --apply to write files.')
