# -*- coding: utf-8 -*-
"""Branche les voix Bodi du cours « facteurs édaphiques » (tc_svt_facteurs_edaphiques) sur le cours.

Usage :
    python brancher_voix_edaph.py <dossier_public> [--cours <cours.json>] [--voix <voix.json>] [--sortie <cours.json>] [--version N]

Pour chaque piste de tc_svt_facteurs_edaphiques_voix.json dont le MP3 existe dans
<dossier_public>/media/audio/courses/tc_svt_facteurs_edaphiques/<type>/<idsur>.mp3
(idsur = re.sub(r'[^A-Za-z0-9_-]', '__', id)), pose son chemin public dans le champ que lit le lecteur (même
convention que backend/data/courses/svt_ch2_role_muscle_strie_squelettique.json) :
    diapo                -> slide.audio.mixed = {url, duration_ms, version, speech_hash (sha256 du texte mixed), status}
    enonce               -> slide.question.enonce_audio
    demonstration        -> slide.question.demonstration.audio
    reaction             -> slide.concentration.reponses[cle][option][juste|1|2].audio
    observation_enonce   -> slide.concentration.observation.enonce_audio
    observation_indice   -> ...observation.indices[k].audio
    observation_retour   -> ...observation.retours[k].audio
    observation_solution -> ...observation.solution.audio
    rappel_enonce        -> competences[].rappels[].enonce_audio
    rappel_reaction      -> competences[].rappels[].reponses[option][juste|1|2].audio
    bloc_retrouver       -> seances[].blocs[].retrouver.enonce_audio
    bloc_exercice        -> seances[].blocs[].exercice.enonce_audio
    bloc_reaction        -> seances[].blocs[].exercice.reponses[option][juste|1|2].audio
Une piste sans MP3 ne touche à rien. Une piste dont le texte ne correspond plus au texte du cours (cours réécrit
depuis la liste des voix) est sautée et signalée : sa voix serait fausse. À relancer après chaque build_cours.py
(qui réécrit le cours sans les champs audio).
"""
import argparse, hashlib, json, os, re, sys

DECK = 'tc_svt_facteurs_edaphiques'
ICI = os.path.dirname(os.path.abspath(__file__))
WT_COURS = os.path.join(ICI, '..', 'wt-tc', 'frontend', 'src', 'publication', 'tronc-commun', 'cours')

def idsur(i):
    return re.sub(r'[^A-Za-z0-9_-]', '__', i)

def duree_ms(f):
    try:
        from mutagen.mp3 import MP3
        return int(round(MP3(f).info.length * 1000))
    except Exception:
        return None   # MP3 vide ou illisible (essai à blanc) : la durée sera lue par le lecteur

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('public')
    ap.add_argument('--cours', default=os.path.join(WT_COURS, DECK + '.json'))
    ap.add_argument('--voix', default=os.path.join(WT_COURS, DECK + '_voix.json'))
    ap.add_argument('--sortie', default=None, help='par défaut : réécrit --cours')
    ap.add_argument('--version', type=int, default=1)
    a = ap.parse_args()
    cours = json.load(open(a.cours, encoding='utf-8'))
    pistes = json.load(open(a.voix, encoding='utf-8'))['pistes']

    slides = {s['id']: s for act in cours['activities'] for s in act['slides']}
    rappels = {r['id']: r for c in cours.get('competences', []) for r in c.get('rappels', [])}
    blocs = {b['id']: b for se in cours.get('seances', []) for b in se.get('blocs', [])}

    def cible(p):
        """(objet, champ, texte attendu) où poser l’audio de la piste p, ou None."""
        t, i = p['type'], p['id']
        parts = i.split('/')
        if t == 'diapo':
            s = slides.get(i); return (s, '__diapo__', s['speech_text']['mixed']) if s else None
        if t in ('enonce', 'demonstration', 'reaction') or t.startswith('observation'):
            s = slides.get(parts[0])
            if not s: return None
            c = s.get('concentration', {})
            if t == 'enonce': q = s.get('question') or {}; return (q, 'enonce_audio', q.get('enonce_dit'))
            if t == 'demonstration': d = (s.get('question') or {}).get('demonstration'); return (d, 'audio', d and d.get('parole'))
            if t == 'reaction':
                cle, opt, k = parts[1:4]; r = c.get('reponses', {}).get(cle, {}).get(opt, {}).get(k); return (r, 'audio', r and r.get('parole'))
            o = c.get('observation')
            if not o: return None
            if t == 'observation_enonce': return (o, 'enonce_audio', o.get('enonce_dit'))
            if t == 'observation_solution': return (o['solution'], 'audio', o['solution'].get('parole'))
            k = int(parts[1][1:])
            if t == 'observation_indice': x = o['indices'][k]; return (x, 'audio', x.get('dit'))
            if t == 'observation_retour': x = o['retours'][k]; return (x, 'audio', x.get('parole'))
        if t == 'rappel_enonce':
            r = rappels.get(i); return (r, 'enonce_audio', r and r.get('enonce_dit'))
        if t == 'rappel_reaction':
            r = rappels.get(parts[0]); x = r and r.get('reponses', {}).get(parts[1], {}).get(parts[2]); return (x, 'audio', x and x.get('parole'))
        if t == 'bloc_retrouver':
            b = blocs.get(i); x = b and b.get('retrouver'); return (x, 'enonce_audio', x and x.get('enonce_dit'))
        if t == 'bloc_exercice':
            b = blocs.get(i); x = b and b.get('exercice'); return (x, 'enonce_audio', x and x.get('enonce_dit'))
        if t == 'bloc_reaction':
            b = blocs.get(parts[0]); e = b and b.get('exercice'); x = e and e.get('reponses', {}).get(parts[1], {}).get(parts[2]); return (x, 'audio', x and x.get('parole'))
        return None

    poses, manquants, perimes, inconnus = {}, 0, [], []
    for p in pistes:
        f = os.path.join(a.public, 'media', 'audio', 'courses', DECK, p['type'], idsur(p['id']) + '.mp3')
        if not os.path.isfile(f):
            manquants += 1; continue
        c = cible(p)
        if not c or c[0] is None:
            inconnus.append(f"{p['type']} {p['id']}"); continue
        obj, champ, texte = c
        if (texte or '').strip() != p['texte'].strip():
            perimes.append(f"{p['type']} {p['id']}"); continue
        url = f"/media/audio/courses/{DECK}/{p['type']}/{idsur(p['id'])}.mp3"
        if champ == '__diapo__':
            obj.setdefault('audio', {})['mixed'] = {'url': url, 'duration_ms': duree_ms(f), 'version': a.version,
                'speech_hash': hashlib.sha256(texte.encode('utf-8')).hexdigest(), 'status': 'published'}
        else:
            obj[champ] = url
        poses[p['type']] = poses.get(p['type'], 0) + 1

    sortie = a.sortie or a.cours
    with open(sortie, 'w', encoding='utf-8') as fh:
        json.dump(cours, fh, ensure_ascii=False, indent=2); fh.write('\n')
    print('posées :', sum(poses.values()), json.dumps(poses, ensure_ascii=False))
    print('MP3 absents (rien touché) :', manquants)
    if perimes: print('texte changé depuis la liste des voix (sautées) :', len(perimes), perimes[:10])
    if inconnus: print('cible introuvable (sautées) :', inconnus[:10])
    return 0 if not inconnus else 1

if __name__ == '__main__':
    sys.exit(main())
