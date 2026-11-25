# -*- coding: utf-8 -*-
"""Pose les voix Bodi d'un deck de /TCF dès qu'une partie Kaggle revient (25 novembre 2026, « les poser au fur et à mesure »).

Entrée : le dossier `att_<deck>/` rapatrié du VPS (`<type>/<idsur>.wav` + `<type>/cours.json` = [{id, hash}], hash =
sha256 du texte de la liste du lot) et les fichiers `fautes_kaggle_<P>.json` des parties (pistes encore signalées par
le contrôle des nombres après 3 prises).
Pour chaque piste de `<deck>_voix.json` (ou de la liste du lot pour l'évaluation) :
  - WAV présent, hash = sha256 du texte ACTUEL, piste non signalée → MP3 (mono, VBR q5) dans
    `frontend/public/media/audio/courses/<deck>/<type>/<idsur>.mp3` ;
  - piste signalée → mise de côté pour l'écoute de l'utilisateur (`docs/tcf/voix_a_ecouter.json`), rien posé ;
  - hash différent (texte changé depuis le lot) → sautée et signalée.
Ensuite : les cours → `scripts/brancher_voix_edaph.py` (champs audio) ; l'évaluation → `VOIX_TCF` de `tcf/sujet.ts`.

Usage : python -X utf8 scripts/tcf/poser_voix_tcf.py <deck> <dossier att_deck> [fautes_kaggle_*.json ...]
"""
import glob, hashlib, json, os, re, subprocess, sys

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
COURS = os.path.join(R, 'frontend', 'src', 'publication', 'tcf', 'cours')
PUBLIC = os.path.join(R, 'frontend', 'public')
A_ECOUTER = os.path.join(R, 'docs', 'tcf', 'voix_a_ecouter.json')


def idsur(i):
    return re.sub(r'[^A-Za-z0-9_-]', '__', i)


def main():
    deck, att, fautes_f = sys.argv[1], sys.argv[2], sys.argv[3:]
    voix = json.load(open(os.path.join(COURS, deck + '_voix.json'), encoding='utf-8'))['pistes']
    signalees = {}
    for f in fautes_f:
        signalees.update(json.load(open(f, encoding='utf-8')))
    hashes = {}
    for cj in glob.glob(os.path.join(att, '*', 'cours.json')):
        t = os.path.basename(os.path.dirname(cj))
        for x in json.load(open(cj, encoding='utf-8')):
            hashes[f"{t}/{x['id']}"] = x['hash']
    poses, cote, perimes, absents = [], {}, [], 0
    for p in voix:
        # l'évaluation garde ses ids tels quels ; les cours les écrivent avec « __ » (brancher_voix_edaph.py)
        nom = p['id'] if deck == 'tc_tcf_examen' else idsur(p['id'])
        rel = f"{p['type']}/{nom}"
        wav = os.path.join(att, p['type'], nom + '.wav')
        if not os.path.isfile(wav):
            absents += 1
            continue
        cle = f'{deck}/{rel}'
        if cle in signalees:
            cote[cle] = {'texte': p['texte'], 'fautes': signalees[cle]}
            continue
        if hashes.get(rel) != hashlib.sha256(p['texte'].encode('utf-8')).hexdigest():
            perimes.append(rel)
            continue
        mp3 = os.path.join(PUBLIC, 'media', 'audio', 'courses', deck, p['type'], nom + '.mp3')
        os.makedirs(os.path.dirname(mp3), exist_ok=True)
        if os.path.getsize(wav) < 2000:   # WAV vide ou cassé rendu par le lot (25/11/2026 : 332 octets) : à refaire
            cote[cle] = {'texte': p['texte'], 'fautes': ['WAV invalide : à régénérer']}
            continue
        if not os.path.isfile(mp3) or os.path.getmtime(mp3) < os.path.getmtime(wav):
            r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav, '-ac', '1', '-codec:a', 'libmp3lame',
                                '-q:a', '5', mp3])
            if r.returncode != 0:
                cote[cle] = {'texte': p['texte'], 'fautes': ['WAV illisible : à régénérer']}
                if os.path.isfile(mp3):
                    os.remove(mp3)
                continue
        poses.append(rel)
    deja = json.load(open(A_ECOUTER, encoding='utf-8')) if os.path.isfile(A_ECOUTER) else {}
    deja = {k: v for k, v in deja.items() if not (k.startswith(deck + '/') and k.split('/', 1)[1] in poses)}
    deja.update(cote)
    with open(A_ECOUTER, 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(deja.items())), f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f'{deck} : {len(poses)} MP3 posés ; {len(cote)} mis de côté (écoute) ; {len(perimes)} texte changé ; '
          f'{absents} pas encore générés')
    for x in perimes[:10]:
        print('  texte changé :', x)
    if deck == 'tc_tcf_examen':
        dossier = os.path.join(PUBLIC, 'media', 'audio', 'courses', deck)
        cles = sorted(os.path.relpath(m, dossier).replace(os.sep, '/')[:-4] for m in glob.glob(os.path.join(dossier, '*', '*.mp3')))
        ts = os.path.join(R, 'frontend', 'src', 'publication', 'tcf', 'sujet.ts')
        s = open(ts, encoding='utf-8').read()
        s2 = re.sub(r'export const VOIX_TCF: string\[\] = \[[^\]]*\];',
                    'export const VOIX_TCF: string[] = [\n' + ''.join(f"  '{c}',\n" for c in cles) + '];', s, count=1)
        if s2 == s and 'VOIX_TCF' not in s:
            sys.exit('VOIX_TCF introuvable dans sujet.ts')
        open(ts, 'w', encoding='utf-8').write(s2)
        print(len(cles), 'pistes dans VOIX_TCF')
    else:
        subprocess.run([sys.executable, '-X', 'utf8', os.path.join(R, 'scripts', 'brancher_voix_edaph.py'), PUBLIC,
                        '--cours', os.path.join(COURS, deck + '.json'), '--voix', os.path.join(COURS, deck + '_voix.json')],
                       check=True)


if __name__ == '__main__':
    main()
