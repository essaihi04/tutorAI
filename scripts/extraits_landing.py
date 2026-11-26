"""
Les extraits de la landing : de vraies diapositives des cours, deux par matière, avec leur voix et leur animation.

    python scripts/extraits_landing.py                        # d'après les cours de la copie de travail
    python scripts/extraits_landing.py --ref origin/main       # d'après les cours d'un commit, sans y toucher
    python scripts/extraits_landing.py --ref <sha> --sortie <fichier>

`--ref` sert quand la copie de travail est en retard sur origin : la vitrine publiée doit pointer les voix que le
commit publié contient, pas celles du poste (26 novembre 2026 : le poste avait les pistes v11 à v17, origin v23 à v27).

Écrit frontend/src/components/landing/extraits.json. À relancer quand un de ces cours change (nouvelle version
de la voix, nouvelle animation) : la vitrine suit le cours, elle ne le copie pas.

Chaque extrait reprend de la diapositive : l'adresse de l'animation, la piste de voix publiée, la commande de
départ et les commandes du tuteur (`pointage`), placées dans le temps par la même règle que le lecteur de cours
(CourseFocusStage.instant : place du mot dans le texte parlé, rapportée à la durée, 0,9 s d'avance pour une
commande). Les sous-titres sont le texte français de la diapositive, phrase par phrase.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
COURS = RACINE / 'backend' / 'data' / 'courses'
PUBLIC = RACINE / 'frontend' / 'public'
SORTIE = RACINE / 'frontend' / 'src' / 'components' / 'landing' / 'extraits.json'
AVANCE_COMMANDE = 0.9

# (cours, diapositive, onglet, matière pour la couleur, ce que l'extrait montre du tuteur[, options])
# Deux extraits par matière (26 novembre 2026). Options : `feuille` = la diapositive d'énoncé jouée juste avant
# (la feuille du sujet, montrée en silence), `entete` = le titre de l'examen et son année, en haut du tableau.
NATIONAL = 'National 2022 · session de rattrapage'
# Ordre des onglets (26 novembre 2026) : le national d'abord, puis physique, maths, SVT et chimie.
CHOIX = [
    ('phys_ch1_waves_exemple', 'wx_n7c_correction_2022r', 'National', 'national', 'Il corrige le national',
     {'feuille': 'wx_n7_enonce', 'entete': {'titre': NATIONAL, 'sujet': 'Physique-Chimie · exercice 2 : ondes mécaniques'}}),
    ('phys_ch3_ondes_lumineuses', 'ol_d2_fente_fine', 'Physique', 'physique', "Il fait l'expérience"),
    ('phys_ch4_radioactivite', 'ra_l1b_moitie', 'Physique', 'physique', 'Il compte avec toi'),
    ('math_ch2_derivation_etude_fonctions', 'df_nd2_rapprocher', 'Maths', 'maths', 'Il anime la notion'),
    ('math_ch1_limites_continuite', 'lc_t4_au_moins_une', 'Maths', 'maths', 'Il fait voir le théorème'),
    ('svt_ch1_reactions_responsables_liberation_energie', 'le_c4_relais', 'SVT', 'svt', 'Il anime le mécanisme'),
    ('svt_ch3_notion_information_genetique', 'ig_s4_helice', 'SVT', 'svt', 'Il construit le schéma'),
    ('phys_ch9_transformations_lentes_rapides', 'tl_r1_bechers', 'Chimie', 'chimie', 'Il fait la manip'),
    ('phys_ch12_etat_equilibre', 'ee_o2_flacons', 'Chimie', 'chimie', 'Il mesure avec toi'),
]
# La feuille du sujet reste ce temps-là à l'écran, avant l'explication (s).
DUREE_FEUILLE = 9.0


def diapositive(cours: dict, ident: str) -> dict:
    for activite in cours['activities']:
        for diapo in activite['slides']:
            if diapo['id'] == ident:
                return diapo
    raise SystemExit(f'diapositive introuvable : {ident}')


REF = None   # un commit (--ref) : les cours et les fichiers sont lus dans ce commit, pas sur le disque


def lire_cours(fichier: str) -> dict:
    if not REF:
        return json.loads((COURS / f'{fichier}.json').read_text(encoding='utf-8'))
    r = subprocess.run(['git', 'show', f'{REF}:backend/data/courses/{fichier}.json'], cwd=RACINE, capture_output=True)
    if r.returncode:
        raise SystemExit(f'cours absent de {REF} : {fichier}')
    return json.loads(r.stdout.decode('utf-8'))


def publie(url: str) -> bool:
    chemin = 'frontend/public/' + url.split('?')[0].lstrip('/')
    if not REF:
        return (RACINE / chemin).exists()
    return subprocess.run(['git', 'cat-file', '-e', f'{REF}:{chemin}'], cwd=RACINE, capture_output=True).returncode == 0


def feuille(cours: dict, ident: str, onglet: str, matiere: str, entete: dict) -> dict:
    """La feuille du sujet, telle qu'au bac, montrée en silence avant l'explication : on lit d'abord l'énoncé."""
    d = diapositive(cours, ident)
    if not publie(d['visual']['url']):
        raise SystemExit(f"fichier absent : {d['visual']['url']}")
    # Pas de `highlight` : la feuille ferait défiler jusqu'à la question (scrollIntoView), et la landing avec elle.
    commandes = [{'t': 0.3, 'commande': 'start', 'parametres': {}}]
    return {
        'id': ident, 'onglet': onglet, 'matiere': matiere, 'capacite': "D'abord, le sujet",
        'cours': cours['title'], 'titre': d['title'], 'entete': entete,
        'src': d['visual']['url'], 'audio': None, 'duree': DUREE_FEUILLE,
        'demarrer': d.get('concentration', {}).get('demarrer'), 'commandes': commandes, 'pointes': [3.0],
        'sous_titres': [{'t': 0, 'texte': "D'abord, on lit le sujet, tel qu'il est tombé au bac."},
                        {'t': 4.5, 'texte': 'Puis on le corrige, question par question.'}],
    }


def extraits_de(fichier: str, ident: str, onglet: str, matiere: str, capacite: str, options: dict | None = None) -> list:
    options = options or {}
    cours = lire_cours(fichier)
    avant = [feuille(cours, options['feuille'], onglet, matiere, options.get('entete'))] if options.get('feuille') else []
    e = extrait(cours, ident, onglet, matiere, capacite)
    if options.get('entete'):
        e['entete'] = options['entete']
    return avant + [e]


def extrait(cours: dict, ident: str, onglet: str, matiere: str, capacite: str) -> dict:
    d = diapositive(cours, ident)
    piste = d['audio']['mixed']
    for url in (piste['url'], d['visual']['url']):
        if not publie(url):
            raise SystemExit(f'fichier absent : {url}')
    duree = piste['duration_ms'] / 1000
    parole = d['speech_text']['mixed'].strip()

    def instant(mot: str) -> float:
        i = parole.find(mot)
        return 0.0 if i < 0 else max(0.0, i / max(1, len(parole)) * duree - 0.3)

    conc = d.get('concentration', {})
    commandes, pointes = [], []
    for p in conc.get('pointage', []):
        if p.get('commande'):
            commandes.append({'t': round(max(0.0, instant(p['mot']) - AVANCE_COMMANDE), 2),
                              'commande': p['commande'], 'parametres': p.get('parametres', {})})
        elif p.get('repere') or p.get('cible'):
            pointes.append(round(instant(p['mot']), 2))

    # Sous-titres : les phrases du texte français, réparties selon leur place dans le texte.
    fr = d['speech_text']['fr'].strip()
    phrases = [x.strip() for x in re.split(r'(?<=[.!?…])\s+', fr) if x.strip()]
    sous_titres, place = [], 0
    for ph in phrases:
        sous_titres.append({'t': round(place / max(1, len(fr)) * duree, 2), 'texte': ph})
        place += len(ph) + 1

    return {
        'id': ident, 'onglet': onglet, 'matiere': matiere, 'capacite': capacite,
        'cours': cours['title'], 'titre': d['title'],
        'src': d['visual']['url'], 'audio': piste['url'], 'duree': round(duree, 2),
        'demarrer': conc.get('demarrer'), 'commandes': sorted(commandes, key=lambda c: c['t']),
        'pointes': sorted(pointes), 'sous_titres': sous_titres,
    }


def main() -> None:
    global REF
    analyse = argparse.ArgumentParser(description='Les extraits de la landing, relevés dans les cours.')
    analyse.add_argument('--ref', help='commit dont on lit les cours (ex. origin/main)')
    analyse.add_argument('--sortie', type=Path, default=SORTIE)
    options = analyse.parse_args()
    REF = options.ref
    extraits = [e for c in CHOIX for e in extraits_de(*c)]
    options.sortie.write_bytes((json.dumps(extraits, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    total = sum(e['duree'] for e in extraits)
    sys.stdout.reconfigure(encoding='utf-8')
    for e in extraits:
        print(f"{e['onglet']:9} {e['duree']:5.1f} s  {len(e['commandes'])} commandes  {(e['audio'] or 'feuille, sans voix').rsplit('/', 1)[-1]}")
    print(f'{len(extraits)} extraits, {total:.0f} s -> {options.sortie}')


if __name__ == '__main__':
    main()
