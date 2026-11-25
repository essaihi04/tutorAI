# -*- coding: utf-8 -*-
"""Outils du générateur du cours de /TCF « Synthèse d'une espèce chimique » (tc_chim_synthese, 25/11/2026).

Chaque diapo est écrite par `diapo(...)` ; chaque `mot` (pointage, centre, démonstration, observation) est contrôlé :
il doit être un extrait exact du texte parlé, trouvé dans l'ordre. Les textes parlés suivent la skill voix-du-cours
(darija simple, français pour les termes, les nombres et les unités, aucun chiffre ni symbole).
"""
import re

SIM = '/media/simulations/chimie/tc_synthese-tableau/'
SLIDES = []          # (activité, diapo)
CHIFFRE = re.compile(r'[0-9=+×/<>≈%→]')


def _controle_parole(t, ou):
    assert not CHIFFRE.search(t), f'{ou} : chiffre ou symbole dans la voix : {CHIFFRE.search(t).group()!r} — {t[:80]}'
    assert 'السخانة' not in t and 'سخانة' not in t, f'{ou} : « السخانة »'


def _trouve(t, mot, ou, depuis=0):
    i = t.find(mot, depuis)
    assert i >= 0, f'{ou} : mot introuvable « {mot} »'
    return i


def reponses_qcm(options, correct, reac):
    """reac[i] = (parole, ecrit) pour la bonne option ; ((p1, e1), (p2, e2)) pour une mauvaise."""
    out = {}
    for i, r in enumerate(reac):
        if i == correct:
            _controle_parole(r[0], f'réaction {i}')
            out[str(i)] = {'juste': {'parole': r[0], 'ecrit': r[1]}}
        else:
            (p1, e1), (p2, e2) = r
            _controle_parole(p1, f'réaction {i}.1'); _controle_parole(p2, f'réaction {i}.2')
            out[str(i)] = {'1': {'parole': p1, 'ecrit': e1}, '2': {'parole': p2, 'ecrit': e2}}
    assert len(out) == len(options)
    return out


def demonstration(parole, lignes):
    _controle_parole(parole, 'démonstration')
    pos = 0
    out = []
    for l in lignes:
        texte, mot = l[0], l[1]
        pos = _trouve(parole, mot, 'démonstration', pos)
        d = {'texte': texte, 'mot': mot}
        if len(l) > 2 and l[2]:
            d['allume'] = l[2]
        out.append(d)
    return {'parole': parole, 'lignes': out}


def question(typ, prompt, options, correct, dit, reac, demo=None, timeout=40):
    _controle_parole(dit, 'énoncé dit')
    q = {'type': typ, 'prompt': prompt, 'options': options, 'correct': correct, 'timeout_seconds': timeout, 'enonce_dit': dit}
    if demo:
        q['demonstration'] = demo
    return q, reponses_qcm(options, correct, reac)


def diapo(act, id, titre, lead, texte, url=None, pointage=(), centre=(), cahier=None, comp=(), q=None, obs=None,
          apres=None, demarrer=None, figures=None, bullets=(), trace=None, caption=None, alt=None, typ='simulation', **extra):
    _controle_parole(texte, id)
    c = {}
    if demarrer:
        c['demarrer'] = demarrer
    pts, pos = [], 0
    for mot, cible in pointage:
        pos = _trouve(texte, mot, id, pos)
        if cible.startswith('@'):
            pts.append({'mot': mot, 'repere': cible[1:]})
        elif cible.startswith('='):
            pts.append({'mot': mot, 'commande': 'set_parameters', 'parametres': eval(cible[1:])})
        else:
            pts.append({'mot': mot, 'commande': 'play_until', 'parametres': {'moment': cible}})
    if pts:
        c['pointage'] = pts
    if centre:
        c['centre'] = []
        for t, mot in centre:
            _trouve(texte, mot, id)
            c['centre'].append({'texte': t, 'mot': mot})
    if obs:
        _trouve(texte, obs['apres_mot'], id)
        assert texte.count(obs['apres_mot']) == 1, f'{id} : apres_mot non unique'
        for k in ('enonce_dit',):
            _controle_parole(obs[k], id + ' obs')
        for x in obs['indices']:
            _controle_parole(x['dit'], id + ' indice')
        for x in obs['retours'] + [obs['solution']]:
            _controle_parole(x['parole'], id + ' retour')
        c['observation'] = obs
    if apres:
        c['apres_reponse'] = apres
    if cahier:
        c['cahier'] = cahier
    if figures:
        c['cahier_figures'] = figures
    c.update(extra.pop('conc', {}))
    s = {'id': id, 'slide_type': typ, 'title': titre,
         'screen_content': {'lead': lead, 'bullets': list(bullets) or [t for t, _ in centre], 'student_trace': trace or (cahier or '').replace('\n', ' ')},
         'visual': {'kind': 'simulation', 'url': SIM + url, 'caption': caption or titre, 'alt': alt or lead} if url else {'kind': 'none'},
         'speech_text': {'mixed': texte}}
    if q:
        s['question'], rep = q
        c['reponses'] = {'q': rep}
    else:
        c['reponses'] = {}
    s['concentration'] = c
    s['competence_ids'] = list(comp)
    s.update(extra)
    SLIDES.append((act, s))
    return s
