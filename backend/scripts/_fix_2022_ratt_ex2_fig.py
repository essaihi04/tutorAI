"""Attach the missing wave figure to 2022-rattrapage PC Ex2.

The sinusoidal y_M(t) curve referenced in Q1 (and needed for Q2/Q3/Q4)
sits at the bottom-right of sujet_p3.jpg.
"""
import json, sys
from pathlib import Path
from PIL import Image

DRY = '--apply' not in sys.argv
BASE = Path('backend/data/exams/physique/2022-rattrapage')
src = BASE / 'pages' / 'sujet_p3.jpg'
dst = BASE / 'assets' / 'fig1_onde_ym_t.jpg'

img = Image.open(src)
w, h = img.size
# Wave curve occupies bottom-right: roughly (0.43, 0.72) to (0.99, 0.97)
box = (int(w * 0.43), int(h * 0.72), int(w * 0.99), int(h * 0.97))
print(f'  src: {src.name} ({w}x{h}) → crop {box}')

if not DRY:
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.crop(box).save(dst, 'JPEG', quality=92)

P = BASE / 'exam.json'
d = json.loads(P.read_text(encoding='utf-8-sig'))
ex = d['parts'][0]['exercises'][1]
doc = {
    'id': 'doc_ex2_fig1_onde_ym_t',
    'type': 'figure',
    'title': 'Figure 1 — Élongation y_M du point M en fonction du temps',
    'description': ("Courbe sinusoïdale de l'élongation y_M (en mm) d'un point M "
                    "du milieu situé à la distance L=2,5 cm du point S, en fonction "
                    "du temps t (en ms). Oscillations visibles avec amplitude ≈ 6 mm "
                    "et graduations à 10, 25, 35, 45 ms."),
    'src': 'assets/fig1_onde_ym_t.jpg',
}
existing_ids = {doc.get('id') for doc in (ex.get('documents') or [])}
if doc['id'] not in existing_ids:
    ex.setdefault('documents', []).append(doc)
    print(f'  added doc: {doc["id"]}')

if DRY:
    print('\n[DRY RUN]')
else:
    P.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print('\n[APPLIED]')
