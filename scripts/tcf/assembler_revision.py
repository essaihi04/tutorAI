# -*- coding: utf-8 -*-
"""Assemble la révision des trois chapitres de /TCF (`tc_tcf_revision`) avec les diapos DÉJÀ faites dans les cours.

Demande de l'utilisateur (25/11/2026) : une révision d'une trentaine de diapos des éléments essentiels des trois
chapitres, « sans rien générer » : chaque diapo est copiée telle quelle de son cours (simulation, tableau, cahier,
questions et réactions, champs audio : mêmes MP3), aucune phrase nouvelle, aucune piste de voix nouvelle.

  - DIAPOS : le choix, dans l'ordre de chaque cours (définitions, méthodes, un exemple et l'exercice de l'élève, le
    « Ce qu'il faut retenir » de chaque chapitre) ;
  - une séance par chapitre ; des blocs de 4 diapos au plus, coupés après chaque diapo à question (une seule « À toi »
    par bloc) ; le cahier d'un bloc = les traces (`concentration.cahier`) de ses diapos, deux figures au plus ;
  - les compétences de chaque cours, restreintes aux diapos gardées (ids préfixés par le cours : sy_C1, at_C2…) avec
    leurs rappels (et leurs voix).
À relancer APRÈS la pose des voix des trois cours (les champs audio sont copiés tels qu'ils sont à ce moment).

Usage : python -X utf8 scripts/tcf/assembler_revision.py [--verifier]
  --verifier : n'écrit rien ; signale chaque diapo, question, réaction ou rappel sans voix, et chaque MP3 absent.
"""
import copy, json, os, sys

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
COURS_DIR = os.path.join(R, 'frontend', 'src', 'publication', 'tcf', 'cours')
PUBLIC = os.path.join(R, 'frontend', 'public')

DIAPOS = [
    ('tc_chim_synthese', 'sy', 'Chimie — Synthèse d’une espèce chimique', [
        'sy_d1_definition', 'sy_n2_types', 'sy_m1_montage', 'sy_r3_bilan', 'sy_t3_etapes',
        'sy_c6_identifier', 'sy_c7_rf', 'sy_c8_rf_eleve', 'sy_b1_bilan']),
    ('tc_chim_atome', 'at', 'Chimie — Modèle de l’atome', [
        'at_s1_atome', 'at_s4_notation', 'at_s6_methode', 'at_m1_masse', 'at_d1_rapport', 'at_e1_isotopes',
        'at_e2_ions', 'at_e3_element', 'at_c2_methode', 'at_c3_toi', 'at_b1_bilan']),
    ('tc_phys_mouvement_inertie', 'mi', 'Physique — Le mouvement et le principe d’inertie', [
        'mi_m3_referentiel', 'mi_v1_moyenne', 'mi_e4_instant', 'mi_e7_vecteur', 'mi_u4_equation', 'mi_u6_eleve',
        'mi_c4_methode', 'mi_i8_enonce', 'mi_i10_grue', 'mi_g3_marteau', 'mi_b1_bilan']),
]


def charger(deck):
    return json.load(open(os.path.join(COURS_DIR, deck + '.json'), encoding='utf-8'))


def lignes_cahier(s):
    c = (s.get('concentration') or {}).get('cahier')
    if not c:
        return []
    # le lecteur lit `bloc.cahier[i].texte` : une chaîne nue s'affichait vide (25/11/2026)
    return [x if isinstance(x, dict) else {'texte': str(x)} for x in (c if isinstance(c, list) else [c])]


def assembler():
    activites, seances, competences, n = [], [], [], 0
    for deck, pre, titre, ids in DIAPOS:
        c = charger(deck)
        toutes = {s['id']: s for a in c['activities'] for s in a['slides']}
        manquantes = [i for i in ids if i not in toutes]
        if manquantes:
            sys.exit(f'{deck} : diapos absentes {manquantes}')
        slides = []
        for i in ids:
            s = copy.deepcopy(toutes[i])
            s['competence_ids'] = [f'{pre}_{k}' for k in s.get('competence_ids', [])]
            s['order_index'] = n
            s['cours_source'] = deck
            n += 1
            slides.append(s)
        activites.append({'id': f'rv_{pre}', 'title': titre, 'phase': 'revision', 'order_index': len(activites),
                          'duration_minutes': max(5, round(sum(((x.get('audio') or {}).get('mixed') or {}).get('duration_ms') or 40000 for x in slides) / 60000) + 2 * len(slides)),
                          'slides': slides})
        # blocs : 4 diapos au plus, coupés après une diapo à question
        blocs, courant = [], []
        for s in slides:
            courant.append(s)
            if s.get('question') or len(courant) == 4:
                blocs.append(courant); courant = []
        if courant:
            blocs.append(courant)
        # Le cahier d'un bloc = le cahier COMPLET des blocs du cours d'où viennent ses diapos (titres, méthode, « Attention »),
        # chacun une seule fois dans la révision. (25/11/2026 : les traces d'une ligne par diapo faisaient passer le lecteur
        # en « une ligne sous chaque titre de diapo » et la page ne montrait que le titre, signalé par l'utilisateur.)
        source = {i: b for se in c.get('seances', []) for b in se.get('blocs', []) for i in b['slide_ids']}
        deja = set()
        rblocs = []
        for k, b in enumerate(blocs):
            srcs = []
            for s in b:
                sb = source.get(s['id'])
                if sb and sb['id'] not in deja:
                    deja.add(sb['id']); srcs.append(sb)
            if not srcs:   # son bloc source est déjà écrit plus haut : on le redonne (jamais une page réduite à un titre)
                srcs = [x for x in {source[s['id']]['id']: source[s['id']] for s in b if s['id'] in source}.values()]
            cahier = [l for sb in srcs for l in sb.get('cahier', [])] or [l for s in b for l in lignes_cahier(s)]
            figures = [f for sb in srcs for f in (sb.get('cahier_figures') or [])][:2]
            rblocs.append({'id': f'rv_{pre}_bloc{k + 1}', 'titre': b[0]['title'], 'slide_ids': [s['id'] for s in b],
                           'cahier': cahier, 'cahier_figures': figures})
        seances.append({'id': f'rv_seance_{pre}', 'titre': titre, 'blocs': rblocs})
        gardees = set(ids)
        for comp in c.get('competences', []):
            sl = [i for i in comp.get('slide_ids', []) if i in gardees]
            if not sl:
                continue
            cc = copy.deepcopy(comp)
            cc['id'] = f"{pre}_{comp['id']}"
            cc['slide_ids'] = sl
            for r in cc.get('rappels', []):
                r['id'] = f"{pre}_{r['id']}"
            competences.append(cc)
    return {
        'id': 'tc_tcf_revision', 'stable_id': 'tc_tcf_revision', 'lesson_id': 'tc_tcf_revision',
        'title': 'Révision des trois chapitres', 'version': 1, 'status': 'draft', 'language': 'mixed',
        'mode': 'concentration', 'niveau': 'tronc_commun_sciences_biof', 'subject': 'physique',
        'estimated_minutes': sum(a['duration_minutes'] for a in activites),
        'note': 'Révision assemblée par scripts/tcf/assembler_revision.py avec les diapos des trois cours, copiées telles '
                'quelles (voix comprises) : rien de nouveau à dire ni à générer (demande de l’utilisateur, 25/11/2026).',
        'activities': activites, 'competences': competences, 'seances': seances,
    }


def verifier(d):
    """Chaque texte parlé copié doit avoir sa voix, et chaque MP3 cité doit exister."""
    sans, absents = [], []

    def voir(obj, champ, ou):
        url = obj.get(champ)
        if not url:
            sans.append(ou)
        elif not os.path.isfile(os.path.join(PUBLIC, url.lstrip('/').split('?')[0])):
            absents.append(f'{ou} → {url}')

    for a in d['activities']:
        for s in a['slides']:
            sid = s['id']
            m = (s.get('audio') or {}).get('mixed') or {}
            voir(m, 'url', f'{sid} (diapo)')
            q = s.get('question') or {}
            if q.get('enonce_dit'):
                voir(q, 'enonce_audio', f'{sid} (énoncé)')
            if (q.get('demonstration') or {}).get('parole'):
                voir(q['demonstration'], 'audio', f'{sid} (démonstration)')
            c = s.get('concentration') or {}
            for cle, opts in (c.get('reponses') or {}).items():
                for opt, ks in (opts or {}).items():
                    for k, r in (ks or {}).items():
                        if isinstance(r, dict) and r.get('parole'):
                            voir(r, 'audio', f'{sid} (réaction {cle}/{opt}/{k})')
            o = c.get('observation')
            if o:
                if o.get('enonce_dit'):
                    voir(o, 'enonce_audio', f'{sid} (observation)')
                for k, x in enumerate(o.get('indices') or []):
                    if x.get('dit'):
                        voir(x, 'audio', f'{sid} (indice {k})')
                for k, x in enumerate(o.get('retours') or []):
                    if x.get('parole'):
                        voir(x, 'audio', f'{sid} (retour {k})')
                if (o.get('solution') or {}).get('parole'):
                    voir(o['solution'], 'audio', f'{sid} (solution)')
    for comp in d['competences']:
        for r in comp.get('rappels', []):
            if r.get('enonce_dit'):
                voir(r, 'enonce_audio', f"{r['id']} (rappel)")
    return sans, absents


if __name__ == '__main__':
    d = assembler()
    nb = sum(len(a['slides']) for a in d['activities'])
    if '--verifier' not in sys.argv:
        sortie = os.path.join(COURS_DIR, 'tc_tcf_revision.json')
        with open(sortie, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(sortie)
    sans, absents = verifier(d)
    print(nb, 'diapos,', sum(len(s['blocs']) for s in d['seances']), 'blocs,', len(d['competences']), 'compétences ;',
          len(sans), 'textes sans voix ;', len(absents), 'MP3 absents')
    for x in (sans + absents)[:20]:
        print('  ', x)
