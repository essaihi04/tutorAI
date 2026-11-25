# -*- coding: utf-8 -*-
"""Construit le cours /TCF « Le mouvement et le principe d'inertie » (tc_phys_mouvement_inertie) à partir des données
écrites dans scripts/tcf/mi_donnees_*.py (25 novembre 2026).

Écriture compacte des diapos (voir `diapo()`), puis le JSON du lecteur (CourseDeck, mode concentration) :
    python -X utf8 scripts/tcf/mi_construire.py
→ frontend/src/publication/tcf/cours/tc_phys_mouvement_inertie.json
Contrôles faits ici : chaque `mot` (pointage, centre, démonstration, observation) se trouve dans le texte parlé, dans
l'ordre ; chaque réaction est posée pour chaque option ; aucun chiffre ni symbole dans un texte parlé.
"""
import json, os, re, sys, importlib

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, '..', '..'))
sys.path.insert(0, ICI)
DECK = 'tc_phys_mouvement_inertie'
SIM = '/media/simulations/physics/tc_mouvement_inertie-tableau/'
ERREURS = []


def err(m):
    ERREURS.append(m)


PARLE_INTERDIT = re.compile(r'[0-9=+×÷/<>≈→⃗₀-₉⁰-⁹ωπτθΔΣ²³]')


def verif_parle(ou, t):
    if t and PARLE_INTERDIT.search(t):
        err(f'{ou} : chiffre ou symbole dans le texte parlé : « {PARLE_INTERDIT.search(t).group(0)} » … {t[:80]}')


def trouve(ou, texte, mot, apres=0):
    i = texte.find(mot, apres)
    if i < 0:
        err(f'{ou} : mot introuvable « {mot} »')
        return apres
    if texte.count(mot) > 1 and apres == 0:
        pass
    return i


def reponses(ou, opts, correct, r):
    """r = {i: (parole, ecrit)} pour la bonne ; {i: ((p1, e1), (p2, e2))} pour les fausses."""
    out = {}
    for i in range(len(opts)):
        if i not in r:
            err(f'{ou} : réaction manquante pour l’option {i}')
            continue
        v = r[i]
        if i == correct:
            out[str(i)] = {'juste': {'parole': v[0], 'ecrit': v[1]}}
            verif_parle(ou, v[0])
        else:
            out[str(i)] = {'1': {'parole': v[0][0], 'ecrit': v[0][1]}, '2': {'parole': v[1][0], 'ecrit': v[1][1]}}
            verif_parle(ou, v[0][0]); verif_parle(ou, v[1][0])
    return out


def demo(ou, d):
    if not d:
        return None
    parole, lignes = d
    verif_parle(ou + ' démo', parole)
    out, pos = [], 0
    for l in lignes:
        texte, mot = l[0], l[1]
        p = trouve(ou + ' démo', parole, mot, pos)
        if p < pos:
            err(f'{ou} démo : mot hors d’ordre « {mot} »')
        pos = max(pos, p)
        e = {'texte': texte, 'mot': mot}
        if len(l) > 2 and l[2]:
            e['allume'] = l[2]
        out.append(e)
    return {'parole': parole, 'lignes': out}


def question(ou, q):
    """q = dict(type, prompt, options|None, correct, dit, reactions, demo)"""
    o = {'type': q['type'], 'prompt': q['prompt']}
    if q['type'] == 'vrai_faux':
        opts = ['Vrai', 'Faux']
        o['options'] = opts
        o['correct'] = q['correct']
    else:
        opts = q['options']
        o['options'] = opts
        o['correct'] = q['correct']
    o['timeout_seconds'] = q.get('timeout', 60 if q.get('demo') else 40)
    o['enonce_dit'] = q['dit']
    verif_parle(ou + ' énoncé', q['dit'])
    d = demo(ou, q.get('demo'))
    if d:
        o['demonstration'] = d
    return o, reponses(ou, opts, q['correct'], q['reactions'])


def observation(ou, parle, o):
    trouve(ou + ' observation', parle, o['apres_mot'])
    for k in ('enonce_dit',):
        verif_parle(ou, o[k])
    res = {'apres_mot': o['apres_mot']}
    if o.get('cacher'):
        res['sim_avant'] = {'conclusions': False}
        res['sim_apres'] = {'conclusions': True}
    if o.get('gestes'):
        res['gestes'] = o['gestes']
    res.update({'enonce': o['enonce'], 'enonce_dit': o['enonce_dit'], 'silence_s': 8,
                'indices': [{'texte': t, 'dit': d, **({'repere': r} if r else {})} for t, d, r in o['indices']],
                'choix': o['choix'], 'bonne': o['bonne'],
                'retours': [{'parole': p, 'ecrit': e} for p, e in o['retours']],
                'solution': {'parole': o['solution'][0], 'ecrit': o['solution'][1]}})
    for i in o['indices']:
        verif_parle(ou, i[1])
    for p, _ in o['retours']:
        verif_parle(ou, p)
    verif_parle(ou, o['solution'][0])
    if len(o['retours']) != len(o['choix']):
        err(f'{ou} : un retour par choix')
    return res


def diapo(d, ordre):
    sid = d['id']
    parle = d['mixed']
    verif_parle(sid, parle)
    s = {'id': sid, 'slide_type': d.get('type', 'simulation'), 'title': d['titre'],
         'screen_content': {'lead': d['lead'], 'bullets': d.get('puces', [c[0] for c in d.get('centre', [])]),
                            'student_trace': d.get('trace', d.get('cahier', ''))}}
    if d.get('vue'):
        s['visual'] = {'kind': 'simulation', 'url': SIM + d['vue'], 'caption': d['titre'], 'alt': d.get('alt', d['lead'])}
    else:
        s['visual'] = {'kind': 'none'}
    s['speech_text'] = {'fr': d['fr'], 'mixed': parle}
    c = {}
    if d.get('demarrer'):
        c['demarrer'] = d['demarrer']
    pt, pos = [], 0
    for mot, cible in d.get('pointage', []):
        p = trouve(sid, parle, mot, pos)
        if p < pos:
            err(f'{sid} : pointage hors d’ordre « {mot} »')
        pos = max(pos, p)
        if cible.startswith('m:'):
            pt.append({'mot': mot, 'commande': 'play_until', 'parametres': {'moment': cible[2:]}})
        elif cible.startswith('r:'):
            pt.append({'mot': mot, 'repere': cible[2:]})
        else:
            err(f'{sid} : cible inconnue {cible}')
    if pt:
        c['pointage'] = pt
    if d.get('centre'):
        cen = []
        for texte, mot in d['centre']:
            trouve(sid + ' centre', parle, mot)
            cen.append({'texte': texte, 'mot': mot})
        c['centre'] = cen
    if d.get('cahier'):
        c['cahier'] = d['cahier']
    if d.get('figures'):
        c['cahier_figures'] = d['figures']
    if d.get('acquis'):
        c['acquis'] = True
    c['reponses'] = {}
    if d.get('question'):
        q, r = question(sid, d['question'])
        s['question'] = q
        c['reponses']['q'] = r
    if d.get('observation'):
        c['observation'] = observation(sid, parle, d['observation'])
    if d.get('apres_reponse'):
        c['apres_reponse'] = d['apres_reponse']
    s['concentration'] = c
    s['competence_ids'] = d.get('comp', [])
    for k in ('ouverture_cours', 'fermeture_cours'):
        if d.get(k):
            s[k] = True
    s['order_index'] = ordre
    return s


def construire():
    parties = []
    for nom in ('mi_donnees_1', 'mi_donnees_2', 'mi_donnees_3', 'mi_donnees_4'):
        try:
            parties.append(importlib.import_module(nom))
        except ModuleNotFoundError:
            print('(pas encore :', nom, ')')
    tete = importlib.import_module('mi_donnees_tete')
    activites, toutes = [], {}
    for p in parties:
        for act in p.ACTIVITES:
            slides = [diapo(d, i) for i, d in enumerate(act['diapos'])]
            for s in slides:
                if s['id'] in toutes:
                    err('id en double ' + s['id'])
                toutes[s['id']] = s
            activites.append({'id': act['id'], 'title': act['titre'], 'phase': act.get('phase', 'cours'),
                              'duration_minutes': act.get('minutes', 15), 'order_index': len(activites), 'slides': slides})
    seances = []
    for se in tete.SEANCES:
        blocs = []
        for b in se['blocs']:
            for x in b['slide_ids']:
                if x not in toutes:
                    err(f"bloc {b['id']} : diapo inconnue {x}")
            blocs.append(b)
        seances.append({'id': se['id'], 'titre': se['titre'], 'blocs': blocs})
    vus = [x for se in seances for b in se['blocs'] for x in b['slide_ids']]
    if sorted(vus) != sorted(toutes):
        err('blocs ≠ diapos : ' + str(set(vus) ^ set(toutes)))
    if vus != [s for a in activites for s in [x['id'] for x in a['slides']]]:
        err('ordre des blocs ≠ ordre des diapos')
    comps = tete.COMPETENCES
    for cp in comps:
        cp['slide_ids'] = [s for s in toutes if cp['id'] in toutes[s]['competence_ids']]
        for r in cp['rappels']:
            verif_parle(r['id'], r.get('enonce_dit'))
    deck = dict(tete.ENTETE)
    deck['competences'] = comps
    deck['seances'] = seances
    deck['activities'] = activites
    return deck


if __name__ == '__main__':
    deck = construire()
    sortie = os.path.join(RACINE, 'frontend/src/publication/tcf/cours', DECK + '.json')
    with open(sortie, 'w', encoding='utf-8') as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)
        f.write('\n')
    n = sum(len(a['slides']) for a in deck['activities'])
    nq = sum(1 for a in deck['activities'] for s in a['slides'] if s.get('question'))
    print(sortie, n, 'diapos,', sum(len(s['blocs']) for s in deck['seances']), 'blocs,', nq, 'questions')
    for e in ERREURS:
        print('ERREUR', e)
    sys.exit(1 if ERREURS else 0)
