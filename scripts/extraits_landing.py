"""
Les extraits de la landing : cinq vraies diapositives des cours, avec leur voix et leur animation.

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

# (cours, diapositive, onglet, matière pour la couleur, ce que l'extrait montre du tuteur)
CHOIX = [
    ('math_ch2_derivation_etude_fonctions', 'df_nd2_rapprocher', 'Maths', 'maths', 'Il anime la notion'),
    ('phys_ch1_waves_exemple', 'wx_o1_bouee', 'Physique', 'physique', 'Il part d\'une question'),
    ('svt_ch2_role_muscle_strie_squelettique', 'ms_u4_filaments', 'SVT', 'svt', 'Il construit le schéma'),
    ('phys_ch13_acides_bases', 'ab_d5_tangentes', 'Chimie', 'chimie', 'Il montre la méthode'),
    ('phys_ch1_waves_exemple', 'wx_n7c_correction_2022r', 'National', 'national', 'Il corrige le national'),
]


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


def extrait(fichier: str, ident: str, onglet: str, matiere: str, capacite: str) -> dict:
    cours = lire_cours(fichier)
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
    extraits = [extrait(*c) for c in CHOIX]
    options.sortie.write_bytes((json.dumps(extraits, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    total = sum(e['duree'] for e in extraits)
    sys.stdout.reconfigure(encoding='utf-8')
    for e in extraits:
        print(f"{e['onglet']:9} {e['duree']:5.1f} s  {len(e['commandes'])} commandes  {e['audio'].rsplit('/', 1)[-1]}")
    print(f'{len(extraits)} extraits, {total:.0f} s -> {options.sortie}')


if __name__ == '__main__':
    main()
