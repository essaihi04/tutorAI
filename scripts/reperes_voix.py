# -*- coding: utf-8 -*-
"""Repères de synchronisation voix ↔ diapositive (25 novembre 2026).

Signalé par l'utilisateur : « parfois il explique quelque chose alors que la diapo l'a déjà montré ». Le lecteur
plaçait chaque mot du pointage à sa place dans le texte rapportée à la durée de la piste (règle de trois) : avec la
darija et le français mêlés, les nombres et les pauses, l'écart atteignait 1,5 à 2 s (mesuré sur mi_i8_enonce).

Ce script écoute chaque piste de diapositive (`audio.mixed.url`) : ffmpeg repère les pauses (fin de phrase, et les
0,3 s de silence posées entre les morceaux générés), puis une programmation dynamique apparie chaque fin de phrase du
texte (« . ! ? ؟ : … ») à la reprise de la voix qui lui correspond le mieux (débit régulier d'un repère à l'autre).
Résultat : `audio.mixed.reperes = [[caractère, seconde], …]` — du début de la voix (0, t₀) à sa fin (L, t_fin). Le
lecteur (`CourseFocusStage.tsx`, `instant`) interpole entre deux repères au lieu de la règle de trois.

Usage : python -X utf8 scripts/reperes_voix.py <public> <cours.json> [<cours.json> …] [--voir <slide_id>]
À relancer après chaque pose de voix (un texte ou une piste changés → repères recalculés).
"""
import json, math, os, re, subprocess, sys

FIN_PHRASE = re.compile(r'[.!?؟:…]+\s+')


def pauses(mp3: str):
    """(début de la voix, fin de la voix, [reprises de la voix après une pause]) en secondes."""
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', mp3, '-af', 'silencedetect=noise=-38dB:d=0.15',
                          '-f', 'null', '-'], capture_output=True, text=True, encoding='utf-8', errors='ignore').stderr
    duree = re.search(r'Duration: (\d+):(\d+):([\d.]+)', err)
    total = int(duree.group(1)) * 3600 + int(duree.group(2)) * 60 + float(duree.group(3)) if duree else 0.0
    debuts = [float(x) for x in re.findall(r'silence_start: (-?[\d.]+)', err)]
    fins = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    t0, t1, reprises = 0.0, total, []
    for k, d in enumerate(debuts):
        f = fins[k] if k < len(fins) else total
        if d <= 0.05:
            t0 = f
        elif f >= total - 0.05:
            t1 = d
        else:
            reprises.append(f)
    return t0, t1, reprises, total


def apparier(texte: str, t0: float, t1: float, reprises: list[float]):
    """Les repères [(car, s)] : chaque fin de phrase appariée (ou non) à une reprise de la voix."""
    L = len(texte)
    bornes = [m.end() for m in FIN_PHRASE.finditer(texte) if 0 < m.end() < L]
    reps = [r for r in reprises if t0 + 0.2 < r < t1 - 0.2]
    if not bornes or not reps or t1 <= t0:
        return [(0, round(t0, 3)), (L, round(t1, 3))]
    debit = (t1 - t0) / L

    def cout(c0, s0, c1, s1):
        if c1 <= c0 or s1 <= s0:
            return None
        r = ((s1 - s0) / (c1 - c0)) / debit
        if not 0.4 <= r <= 2.5:
            return None
        return abs(math.log(r))

    # points : départ, (borne i, reprise j)…, arrivée ; meilleur score = appariements − 1,5 × écarts de débit
    pts = [(0, t0)] + [(b, r) for b in bornes for r in reps] + [(L, t1)]
    meilleur = {0: (0.0, None)}
    ordre = sorted(range(1, len(pts)), key=lambda k: (pts[k][0], pts[k][1]))
    for k in ordre:
        ck, sk = pts[k]
        best = None
        for p, (sc, _) in meilleur.items():
            cp, sp = pts[p]
            c = cout(cp, sp, ck, sk)
            if c is None:
                continue
            v = sc + (0 if k == len(pts) - 1 else 1) - 1.5 * c
            if best is None or v > best[0]:
                best = (v, p)
        if best:
            meilleur[k] = best
    fin = len(pts) - 1
    if fin not in meilleur:
        return [(0, round(t0, 3)), (L, round(t1, 3))]
    chemin, k = [], fin
    while k is not None:
        chemin.append(pts[k]); k = meilleur[k][1]
    return [(c, round(s, 3)) for c, s in reversed(chemin)]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    voir = sys.argv[sys.argv.index('--voir') + 1] if '--voir' in sys.argv else None
    if voir:
        args.remove(voir)
    public, cours = args[0], args[1:]
    for f in cours:
        d = json.load(open(f, encoding='utf-8'))
        n = sans = 0
        for a in d['activities']:
            for s in a['slides']:
                m = (s.get('audio') or {}).get('mixed') or {}
                texte = ((s.get('speech_text') or {}).get('mixed') or '').strip()
                url = (m.get('url') or '').split('?')[0]
                mp3 = os.path.join(public, url.lstrip('/'))
                if not texte or not url or not os.path.isfile(mp3):
                    m.pop('reperes', None)
                    continue
                t0, t1, reprises, _ = pauses(mp3)
                rep = apparier(texte, t0, t1, reprises)
                m['reperes'] = [list(x) for x in rep]
                n += 1
                sans += len(rep) <= 2
                if s['id'] == voir:
                    print(s['id'], 'reprises', [round(r, 2) for r in reprises])
                    for c, t in rep:
                        print(f'  {t:6.2f} s  car {c:4d}  « {texte[c:c + 40]} »')
        with open(f, 'w', encoding='utf-8') as o:
            json.dump(d, o, ensure_ascii=False, indent=2)
            o.write('\n')
        print(f'{os.path.basename(f)} : {n} pistes repérées ({sans} sans repère intermédiaire)')


if __name__ == '__main__':
    main()
