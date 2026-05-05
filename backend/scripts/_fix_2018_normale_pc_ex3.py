"""Reconstruct Partie preambles for 2018-normale PC Ex3 (Électricité).

Before: ex.context was a generic TP intro and the actual setups for
Partie I sub-1, Partie I sub-2, and Partie II were entirely missing —
questions referenced 'figure 2', 'figure 6' etc. without any context.

After: Ex3 is split into 3 Parties matching the official paper:
  Partie 1 → I.1 Détermination de C par générateur de courant
            (Q1.1, Q1.2, Q1.3 — were QI.1.1, QI.1.2, QI.1.3)
  Partie 2 → I.2 Étude de la décharge RC
            (Q2.1, Q2.2, Q2.3 — were QI.2.1, QI.2.2, QI.2.3)
  Partie 3 → II   Étude d'un circuit RLC série
            (Q3.1, Q3.2.1, Q3.2.2, Q3.2.3 — were QII.1, QII.2.1, ...)

The setups are transcribed from sujet_p4.jpg / sujet_p5.jpg / sujet_p6.jpg.
Figures (1-6) are cropped from those pages and added as documents.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
from PIL import Image

DRY = '--apply' not in sys.argv
EXAM_DIR = Path('backend/data/exams/physique/2018-normale')
P = EXAM_DIR / 'exam.json'

# ── Preambles ────────────────────────────────────────────────────────
GLOBAL_INTRO = (
    "Un professeur a consacré, avec ses élèves, une séance de travaux "
    "pratiques de physique pour :\n"
    "- Déterminer expérimentalement la valeur de la capacité d'un "
    "condensateur par deux méthodes différentes.\n"
    "- Étudier un circuit RLC série."
)

PARTIE_1_PREAMBLE = (
    "**Partie 1 - Détermination expérimentale de la capacité d'un "
    "condensateur par un générateur de courant**\n\n"
    "Un premier groupe d'élèves d'une classe réalise, sous les "
    "directives du professeur, le montage expérimental de la figure 1 "
    "constitué des éléments suivants :\n"
    "- un générateur idéal de courant qui alimente le circuit par un "
    "courant électrique d'intensité $I_0$ ;\n"
    "- un conducteur ohmique de résistance $R$ ;\n"
    "- deux condensateurs $(c_1)$ et $(c_2)$ montés en parallèle, "
    "respectivement de capacités $C_1 = 7{,}5\\,\\mathrm{\\mu F}$ et "
    "$C_2$ inconnue ;\n"
    "- un interrupteur $K$.\n\n"
    "À l'instant $t_0 = 0$, un élève ferme le circuit. À l'aide d'un "
    "système d'acquisition informatisé, le groupe d'élèves obtient la "
    "courbe des variations de la charge $q$ du condensateur équivalent "
    "à l'association des deux condensateurs $(c_1)$ et $(c_2)$ en "
    "fonction de la tension $u_{AB}$ (figure 2)."
)

PARTIE_2_PREAMBLE = (
    "**Partie 2 - Étude de la réponse du dipôle RC à un échelon de "
    "tension**\n\n"
    "Un deuxième groupe d'élèves de la même classe réalise le montage "
    "représenté par la figure 3 constitué par :\n"
    "- Un générateur idéal de tension de force électromotrice $E$ ;\n"
    "- Un conducteur ohmique de résistance $R = 1600\\,\\Omega$ ;\n"
    "- Le condensateur précédent de capacité $C_2$ ;\n"
    "- Un interrupteur $K$ à double position.\n\n"
    "Après avoir chargé totalement le condensateur, un élève bascule "
    "l'interrupteur $K$ sur la position (2) à l'instant $t_0 = 0$. À "
    "l'aide d'un système d'acquisition informatisé, le groupe d'élèves "
    "obtient la courbe des variations de la tension $u_{C_2}(t)$ aux "
    "bornes du condensateur (figure 4)."
)

PARTIE_3_PREAMBLE = (
    "**Partie 3 - Étude d'un circuit RLC série**\n\n"
    "Un élève de la même classe réalise le montage représenté sur la "
    "figure 5 qui comporte :\n"
    "- un condensateur, totalement chargé, de capacité "
    "$C = 2{,}5\\,\\mathrm{\\mu F}$ ;\n"
    "- une bobine d'inductance $L$ et de résistance $r$ ;\n"
    "- un interrupteur $K$.\n\n"
    "Après fermeture du circuit, on visualise, à l'aide d'un système "
    "d'acquisition informatisé, des oscillations pseudopériodiques "
    "représentant les variations de la charge $q(t)$ du condensateur."
)

# ── Figure crop jobs (fractional boxes; full page is 1654×2339) ─────
# Boxes determined by visual inspection of the JPG pages.
FIGURE_JOBS = [
    # (id, source_page, crop_box_fractional, title, description)
    ('fig1_circuit_parallele', 'sujet_p5.jpg', (0.18, 0.06, 0.55, 0.30),
     'Figure 1 — Montage avec deux condensateurs en parallèle',
     "Schéma du circuit : générateur de courant I0, interrupteur K, conducteur ohmique R, deux condensateurs (c_1) et (c_2) montés en parallèle entre les points A et B."),
    ('fig2_q_uab', 'sujet_p5.jpg', (0.55, 0.06, 0.97, 0.30),
     'Figure 2 — Charge q en fonction de u_AB',
     "Graphique de la charge q (en μC) en fonction de la tension u_AB (en V). Droite passant par l'origine, avec des graduations à 10 et 20 μC sur l'axe q et 1, 2, 3, 4 V sur l'axe u_AB."),
    ('fig3_circuit_rc', 'sujet_p5.jpg', (0.13, 0.42, 0.55, 0.66),
     'Figure 3 — Circuit RC avec interrupteur double position',
     "Schéma : générateur idéal de tension E, condensateur C_2 avec u_C2, conducteur ohmique R, interrupteur K à double position (1)/(2)."),
    ('fig4_uc2_t', 'sujet_p5.jpg', (0.55, 0.42, 0.97, 0.66),
     'Figure 4 — Tension u_C2 en fonction du temps',
     "Courbe de la tension u_C2 (en V) en fonction du temps t (en ms). Décroissance exponentielle partant de 9 V à t=0, graduations à 4, 8, 12 ms."),
    ('fig5_circuit_rlc', 'sujet_p6.jpg', (0.13, 0.30, 0.50, 0.55),
     'Figure 5 — Circuit RLC série',
     "Schéma : condensateur de capacité C entre les points A et B, bobine d'inductance L et résistance r, interrupteur K."),
    ('fig6_q_t_oscillations', 'sujet_p6.jpg', (0.50, 0.30, 0.97, 0.55),
     'Figure 6 — Oscillations sinusoïdales de la charge q(t)',
     "Courbe de la charge q (en μC) en fonction du temps t (en ms). Oscillations sinusoïdales d'amplitude q_m, avec pseudo-période visible entre les graduations 1, 2, 3, 4 ms."),
]


def crop_figures():
    out = []
    for fid, page, box, title, desc in FIGURE_JOBS:
        src = EXAM_DIR / 'pages' / page
        dst = EXAM_DIR / 'assets' / f'{fid}.jpg'
        img = Image.open(src)
        w, h = img.size
        bb = (int(w * box[0]), int(h * box[1]),
              int(w * box[2]), int(h * box[3]))
        if not DRY:
            dst.parent.mkdir(parents=True, exist_ok=True)
            img.crop(bb).save(dst, 'JPEG', quality=92)
        out.append({
            'id': f'doc_ex3_{fid}',
            'type': 'figure',
            'title': title,
            'description': desc,
            'src': f'assets/{fid}.jpg',
        })
        print(f'  crop {fid}: page={page} box={bb} -> {dst.name}')
    return out


def main():
    d = json.loads(P.read_text(encoding='utf-8-sig'))
    ex = d['parts'][0]['exercises'][2]
    qs = ex['questions']
    print(f'Original Ex3: {len(qs)} questions')
    for q in qs:
        print(f'  Q{q.get("number")}')

    # ── Renumber questions and inject preambles ───────────────────
    # Original numbering → new numbering
    REMAP = {
        'I.1.1': '1.1', 'I.1.2': '1.2', 'I.1.3': '1.3',
        'I.2.1': '2.1', 'I.2.2': '2.2', 'I.2.3': '2.3',
        'II.1':  '3.1',
        'II.2.1': '3.2', 'II.2.2': '3.3', 'II.2.3': '3.4',
    }
    for q in qs:
        old = str(q.get('number'))
        if old in REMAP:
            q['number'] = REMAP[old]

    # Inject preambles on owner questions (1.1, 2.1, 3.1)
    owner_to_preamble = {
        '1.1': PARTIE_1_PREAMBLE,
        '2.1': PARTIE_2_PREAMBLE,
        '3.1': PARTIE_3_PREAMBLE,
    }
    for q in qs:
        n = str(q.get('number'))
        if n in owner_to_preamble:
            preamble = owner_to_preamble[n]
            content = q.get('content', '') or ''
            if not content.lstrip().startswith('**Partie'):
                q['content'] = preamble.strip() + '\n\n---\n\n' + content

    # ── Inject the question 3.2's "Pour obtenir des oscillations..." intro ─
    # Originally QII.2 was a sub-numbered preamble paragraph in the PDF
    # (no question of its own). It serves as setup for 3.2.x. We embed it
    # directly into the new 3.2 question content.
    SUB_3_2_INTRO = (
        "Pour obtenir des oscillations électriques entretenues, un "
        "générateur $G$ délivrant une tension proportionnelle à "
        "l'intensité du courant $u_G(t) = k \\cdot i(t)$ est inséré en "
        "série dans le circuit précédent.\n\n"
    )
    for q in qs:
        if str(q.get('number')) == '3.2':
            c = q.get('content', '') or ''
            if not c.startswith('Pour obtenir'):
                q['content'] = SUB_3_2_INTRO + c
            break

    # ── Reset ex.context to lead-in only ───────────────────────────
    ex['context'] = (
        GLOBAL_INTRO + "\n\nLes trois parties sont indépendantes."
    )

    # ── Crop figures + attach as documents ─────────────────────────
    print('\nCropping figures...')
    docs = crop_figures()
    existing_ids = {doc.get('id') for doc in (ex.get('documents') or [])}
    for doc in docs:
        if doc['id'] not in existing_ids:
            ex.setdefault('documents', []).append(doc)

    # ── Show summary ───────────────────────────────────────────────
    print('\nNew Ex3 questions:')
    for q in qs:
        print(f'  Q{q.get("number")}: {(q.get("content","") or "")[:80]!r}')

    if DRY:
        print('\n[DRY RUN] Re-run with --apply to write.')
    else:
        P.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
        print('\n[APPLIED]')


if __name__ == '__main__':
    main()
