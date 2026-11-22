"""Nombres dits en darija -> en français dans le texte parlé : outil des fichiers de cours (21-22/11/2026).

Règle de l'utilisateur : jamais un mot darija et un mot français successifs dans un nombre ou une formule (« جوج noyaux »
-> « deux noyaux », « x زائد واحد » -> « x plus un », « dix أس ناقص خمسة » -> « dix puissance moins cinq »). La logique
est dans backend/kaggle_tts/texte_parle.py (`nombres_darija_fr`), appliquée en premier par `parle` : la voix en direct
(réponses libres du tuteur), les lots et les cours la suivent donc d'office. Ce script l'écrit dans les fichiers des
cours, pour que le texte affiché et son hash soient déjà justes avant de générer la voix.

    python -X utf8 scripts/voix/nombres_fr.py [--ecrire] [deck …]
Tests : python -X utf8 -m pytest scripts/voix/test_nombres_fr.py"""
import importlib.util
import re
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "texte_parle", Path(__file__).resolve().parents[2] / "backend" / "kaggle_tts" / "texte_parle.py")
_tp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tp)

convertir = _tp.nombres_darija_fr
reparer_mots = _tp._nd_reparer_mots
NOMBRE = _tp._nd_NOMBRE
ARA = re.compile(r'[؀-ۿ]')


if __name__ == '__main__':
    # python -X utf8 scripts/voix/nombres_fr.py [--ecrire] [deck …] : liste (ou convertit) les nombres darija qui touchent
    # du français dans les textes des cours (backend/data/courses et en_attente) ; les mots du pointage sont réalignés.
    import difflib, json, sys
    from pathlib import Path
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    ecrire = '--ecrire' in sys.argv
    racine = Path(__file__).resolve().parents[2] / 'backend' / 'data' / 'courses'
    fichiers = [f for d in (racine, racine / 'en_attente') for f in sorted(d.glob('*.json'))
                if (not args or f.stem in args) and (racine / 'en_attente' / f.name).exists()]

    def realigner(vieux, neuf, mot):
        i = vieux.index(mot); tv, tn = vieux.split(' '), neuf.split(' ')
        debut, fin = len(vieux[:i].split(' ')) - 1, len(vieux[:i + len(mot)].split(' '))
        sm = difflib.SequenceMatcher(None, tv, tn, autojunk=False)
        def carte(x, bord):
            for tag, a1, a2, b1, b2 in sm.get_opcodes():
                if a1 <= x < a2 or (x == a2 and bord):
                    return b1 + (x - a1) if tag == 'equal' else (b2 if bord else b1)
            return len(tn)
        nd, nf = carte(debut, False), carte(fin, True)
        r = ' '.join(tn[nd:max(nf, nd + 1)]).strip()
        return r if r and r in neuf else mot

    total = 0
    for f in fichiers:
        brut = f.read_text(encoding='utf-8'); m = json.loads(brut); n = [0]
        anciens = {id(s): ((s.get('speech_text') or {}).get('mixed') or '',
                           [p.get('mot') for p in ((s.get('concentration') or {}).get('pointage') or [])])
                   for a in m.get('activities', []) for s in a.get('slides', [])}
        def walk(o):
            if isinstance(o, dict):
                for k in o: o[k] = walk(o[k])
                return o
            if isinstance(o, list):
                return [walk(v) for v in o]
            if isinstance(o, str) and ARA.search(o):
                c = convertir(o)
                if c != o:
                    n[0] += 1
                    if not ecrire:
                        print(f'{f.stem}: {o[:160]}')
                return c
            return o
        walk(m)
        for a in m.get('activities', []):
            for s in a.get('slides', []):
                vieux, mots = anciens[id(s)]
                neuf = (s.get('speech_text') or {}).get('mixed') or ''
                for po, mot in zip(((s.get('concentration') or {}).get('pointage') or []), mots):
                    if mot and po.get('mot') not in neuf and mot in vieux:
                        po['mot'] = realigner(vieux, neuf, mot)
        total += n[0]
        if ecrire and n[0]:
            ind = 2 if brut.startswith('{\n  "') else (1 if brut.startswith('{\n "') else None)
            f.write_text(json.dumps(m, ensure_ascii=False, indent=ind) + ('\n' if brut.endswith('\n') else ''), encoding='utf-8',
                         newline='\n')
            print(f'{f}: {n[0]} textes convertis')
    print(f'{total} textes avec un nombre darija à côté du français' + (' (convertis)' if ecrire else ''))
