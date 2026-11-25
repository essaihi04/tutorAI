# -*- coding: utf-8 -*-
"""Liste les textes à mettre en voix d'un cours de /TCF (ou du Tronc Commun) → <cours>_voix.json (25 novembre 2026).

L'inverse exact de `scripts/brancher_voix_edaph.py` : chaque texte parlé du cours devient une piste
`{type, id, texte}` avec les types et les identifiants que le brancheur sait poser (diapo, enonce, demonstration,
reaction, observation_*, rappel_enonce, rappel_reaction, bloc_retrouver, bloc_exercice, bloc_reaction).
Les blocs (`retrouver`, `exercice`) ne sont pas joués aujourd'hui (skill cours-concentration, « Played today ») : ils ne
sont listés qu'avec `--blocs`. Une piste dont l'audio est déjà posé n'est pas relistée avec `--manquantes`.

Puis `--lot <liste.json>` écrit la liste du lot Kaggle sans tunnel (skill voix-du-cours § 3) :
`{"<deck>/<type>/<idsur>": texte}` — `idsur` = l'id où « : » et « / » deviennent « __ » (nom du fichier).

Usage : python -X utf8 scripts/tcf/lister_voix_tcf.py <cours.json> [--blocs] [--manquantes] [--lot <liste.json>]
"""
import argparse, json, os, re, sys


def idsur(i):
    return re.sub(r'[^A-Za-z0-9_-]', '__', i)


def pistes(cours, blocs=False, manquantes=False):
    out = []

    def ajouter(t, i, texte, deja=None):
        if isinstance(texte, str) and texte.strip() and not (manquantes and deja):
            out.append({'type': t, 'id': i, 'texte': texte})

    for act in cours['activities']:
        for s in act['slides']:
            sid = s['id']
            ajouter('diapo', sid, (s.get('speech_text') or {}).get('mixed'), ((s.get('audio') or {}).get('mixed') or {}).get('url'))
            q = s.get('question') or {}
            ajouter('enonce', f'{sid}/q', q.get('enonce_dit'), q.get('enonce_audio'))
            d = q.get('demonstration') or {}
            ajouter('demonstration', f'{sid}/q', d.get('parole'), d.get('audio'))
            c = s.get('concentration') or {}
            for cle, opts in (c.get('reponses') or {}).items():
                for opt, ks in (opts or {}).items():
                    for k, r in (ks or {}).items():
                        if isinstance(r, dict):
                            ajouter('reaction', f'{sid}/{cle}/{opt}/{k}', r.get('parole'), r.get('audio'))
            o = c.get('observation')
            if o:
                ajouter('observation_enonce', sid, o.get('enonce_dit'), o.get('enonce_audio'))
                for k, x in enumerate(o.get('indices') or []):
                    ajouter('observation_indice', f'{sid}/i{k}', x.get('dit'), x.get('audio'))
                for k, x in enumerate(o.get('retours') or []):
                    ajouter('observation_retour', f'{sid}/r{k}', x.get('parole'), x.get('audio'))
                sol = o.get('solution') or {}
                ajouter('observation_solution', sid, sol.get('parole'), sol.get('audio'))
    for comp in cours.get('competences', []):
        for r in comp.get('rappels', []):
            ajouter('rappel_enonce', r['id'], r.get('enonce_dit'), r.get('enonce_audio'))
            for opt, ks in (r.get('reponses') or {}).items():
                for k, x in (ks or {}).items():
                    if isinstance(x, dict):
                        ajouter('rappel_reaction', f"{r['id']}/{opt}/{k}", x.get('parole'), x.get('audio'))
    if blocs:
        for se in cours.get('seances', []):
            for b in se.get('blocs', []):
                rt = b.get('retrouver') or {}
                ajouter('bloc_retrouver', b['id'], rt.get('enonce_dit'), rt.get('enonce_audio'))
                ex = b.get('exercice') or {}
                ajouter('bloc_exercice', b['id'], ex.get('enonce_dit'), ex.get('enonce_audio'))
                for opt, ks in (ex.get('reponses') or {}).items():
                    for k, x in (ks or {}).items():
                        if isinstance(x, dict):
                            ajouter('bloc_reaction', f"{b['id']}/{opt}/{k}", x.get('parole'), x.get('audio'))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cours')
    ap.add_argument('--blocs', action='store_true')
    ap.add_argument('--manquantes', action='store_true')
    ap.add_argument('--lot', default=None)
    a = ap.parse_args()
    cours = json.load(open(a.cours, encoding='utf-8'))
    deck = cours['id']
    ps = pistes(cours, a.blocs, a.manquantes)
    sortie = os.path.splitext(a.cours)[0] + '_voix.json'
    if not a.manquantes:
        with open(sortie, 'w', encoding='utf-8') as f:
            json.dump({'deck': deck, 'voix': 'academy-v6-bodi (par lot, sans tunnel)', 'pistes': ps}, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(sortie)
    if a.lot:
        lot = {f"{deck}/{p['type']}/{idsur(p['id'])}": p['texte'] for p in ps}
        with open(a.lot, 'w', encoding='utf-8') as f:
            json.dump(lot, f, ensure_ascii=False, indent=1)
        print(a.lot, len(lot), 'pistes', sum(len(t) for t in lot.values()), 'caractères')
    from collections import Counter
    print(len(ps), 'pistes', dict(Counter(p['type'] for p in ps)))


if __name__ == '__main__':
    sys.exit(main())
