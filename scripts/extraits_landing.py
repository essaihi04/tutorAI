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


def _module_reperes():
    """scripts/reperes_voix.py (pauses de la voix <-> fins de phrase), pris sur le disque ou dans origin/main."""
    import types
    f = RACINE / 'scripts' / 'reperes_voix.py'
    src = f.read_text(encoding='utf-8') if f.exists() else subprocess.run(
        ['git', 'show', 'origin/main:scripts/reperes_voix.py'], cwd=RACINE, capture_output=True).stdout.decode('utf-8')
    m = types.ModuleType('reperes_voix')
    exec(compile(src, 'reperes_voix.py', 'exec'), m.__dict__)
    return m


RV = None


def seconde_du_caractere(reperes, i):
    """Comme CourseFocusStage.secondeDuCaractere : interpolation entre les deux repères qui entourent le caractère."""
    k = 0
    while k < len(reperes) - 1 and reperes[k + 1][0] <= i:
        k += 1
    c0, s0 = reperes[k]
    c1, s1 = reperes[min(k + 1, len(reperes) - 1)]
    return s0 + (i - c0) / (c1 - c0) * (s1 - s0) if c1 > c0 else s0


def fichier_mp3(url: str) -> str:
    """Un chemin local vers la piste (sur le disque, ou extraite du commit --ref dans un fichier temporaire)."""
    import tempfile
    chemin = 'frontend/public/' + url.split('?')[0].lstrip('/')
    if not REF or (RACINE / chemin).exists() and subprocess.run(
            ['git', 'cat-file', '-e', f'{REF}:{chemin}'], cwd=RACINE, capture_output=True).returncode:
        return str(RACINE / chemin)          # pas encore dans le commit : la piste du disque
    octets = subprocess.run(['git', 'show', f'{REF}:{chemin}'], cwd=RACINE, capture_output=True).stdout
    t = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
    t.write(octets); t.close()
    return t.name


def reperes_piste(url: str, texte: str, connus=None):
    """Les repères [[caractère, seconde]] de la piste : ceux du cours s'ils valent pour cette piste, sinon calculés."""
    global RV
    if connus and len(connus) >= 2:
        return [list(x) for x in connus]
    RV = RV or _module_reperes()
    t0, t1, reprises, _ = RV.pauses(fichier_mp3(url))
    return [list(x) for x in RV.apparier(texte, t0, t1, reprises)]
COURS = RACINE / 'backend' / 'data' / 'courses'
PUBLIC = RACINE / 'frontend' / 'public'
SORTIE = RACINE / 'frontend' / 'src' / 'components' / 'landing' / 'extraits.json'
AVANCE_COMMANDE = 0.25   # + les 0,15 s de l'instant : 0,4 s d'avance, le temps que la main atteigne le bouton

# (cours, diapositive, onglet, matière pour la couleur, ce que l'extrait montre du tuteur[, options])
# Deux extraits par matière (26 novembre 2026). Options : `feuille` = la diapositive d'énoncé jouée juste avant
# (la feuille du sujet, montrée en silence), `entete` = le titre de l'examen et son année, en haut du tableau.
NATIONAL = 'National 2022 · session de rattrapage'
# Ordre des onglets (26 novembre 2026) : le national d'abord, puis physique, maths, SVT et chimie.
CHOIX = [
    ('phys_ch1_waves_exemple', 'wx_n7c_correction_2022r', 'National', 'national', 'Il corrige le national',
     {'feuille': 'wx_n7_enonce', 'entete': {'titre': NATIONAL, 'sujet': 'Physique-Chimie · exercice 2 : ondes mécaniques'}}),
    ('phys_ch3_ondes_lumineuses', 'ol_d2_fente_fine', 'Physique', 'physique', "Il fait l'expérience"),
    ('phys_ch5_energie_nucleaire', 'en_r4_fusion', 'Physique', 'physique', 'Il montre la fusion'),   # la fission (voix v11) sonnait mal
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

    # (26/11/2026, « synchroniser finement ») l'instant d'un mot vient des repères de la piste — où la voix dit
    # vraiment chaque phrase —, comme dans le lecteur de cours ; la diapo ne prend plus que 0,15 s d'avance (0,4 s
    # pour une commande) au lieu de la règle de trois qui avançait de 1,5 à 2 s.
    m = d['audio']['mixed']
    connus = m.get('reperes') if m.get('reperes_duree') and abs(m['reperes_duree'] - duree) < 0.3 else None
    reperes = reperes_piste(piste['url'], parole, connus)

    def instant(mot: str) -> float:
        i = parole.find(mot)
        return 0.0 if i < 0 else max(0.0, min(seconde_du_caractere(reperes, i), duree) - 0.15)

    conc = d.get('concentration', {})
    commandes, pointes = [], []
    for p in conc.get('pointage', []):
        if p.get('commande'):
            commandes.append({'t': round(max(0.0, instant(p['mot']) - AVANCE_COMMANDE), 2),
                              'commande': p['commande'], 'parametres': p.get('parametres', {})})
        elif p.get('repere') or p.get('cible'):
            pointes.append(round(instant(p['mot']), 2))

    # Sous-titres : les phrases du texte français. Même nombre de phrases que le texte dit : la k-ième part quand la
    # voix dit la k-ième phrase ; sinon, à la même proportion du texte dit, placée par les repères.
    fr = d['speech_text']['fr'].strip()
    phrases = [x.strip() for x in re.split(r'(?<=[.!?…])\s+', fr) if x.strip()]
    debuts_dits = [0] + [mt.end() for mt in re.finditer(r'[.!?؟…]+\s+', parole) if mt.end() < len(parole)]
    sous_titres, place = [], 0
    for k, ph in enumerate(phrases):
        c = debuts_dits[k] if len(debuts_dits) == len(phrases) else place / max(1, len(fr)) * len(parole)
        sous_titres.append({'t': round(min(seconde_du_caractere(reperes, c), duree), 2), 'texte': ph})
        place += len(ph) + 1

    return {
        'id': ident, 'onglet': onglet, 'matiere': matiere, 'capacite': capacite,
        'cours': cours['title'], 'titre': d['title'],
        'src': d['visual']['url'], 'audio': piste['url'], 'duree': round(duree, 2),
        'demarrer': conc.get('demarrer'), 'commandes': sorted(commandes, key=lambda c: c['t']),
        'pointes': sorted(pointes), 'sous_titres': sous_titres,
    }


# La bienvenue du tableau (media/audio/landing/bienvenue.mp3) : le texte dit et le début de chacune de ses parties
# (une bulle et une ligne écrite au tableau par partie) — chaque partie s'allume quand la voix la dit.
BIENVENUE = ('مرحبا بيك! أنا Moalim. ماشي ChatGPT: أنا أستاذ متخصص فالباك المغربي. كنشرح ليك بالدارجة بحال شي أستاذ '
             'حقيقي، خطوة بخطوة: الدروس كاملين، وكل سؤال من الامتحانات الوطنية كنصححوه مع بعض. وفي le mode libre، '
             'سولني على أي حاجة وغادي نجاوبك. أنا كنفهمك، وكنفهم المستوى ديالك، وغادي نبقاو نتحسنو مع بعض. أنا معاك '
             'فالدار، فأي وقت. أنا وياك، غادي نجيبو الباك ب mention!')
BIENVENUE_PARTIES = ['مرحبا بيك', 'كنشرح ليك', 'وفي le mode libre', 'أنا كنفهمك', 'أنا معاك']
VOIX_LANDING = RACINE / 'frontend' / 'src' / 'components' / 'landing' / 'voix_landing.json'


def voix_landing() -> dict:
    global RV
    RV = RV or _module_reperes()
    t0, t1, reprises, total = RV.pauses(fichier_mp3('/media/audio/landing/bienvenue.mp3'))
    reperes = [list(x) for x in RV.apparier(BIENVENUE, t0, t1, reprises)]
    debuts = [round(seconde_du_caractere(reperes, BIENVENUE.find(m)), 2) for m in BIENVENUE_PARTIES]
    return {'bienvenue': {'duree': round(total, 2), 'debuts': debuts}}


def main() -> None:
    global REF
    analyse = argparse.ArgumentParser(description='Les extraits de la landing, relevés dans les cours.')
    analyse.add_argument('--ref', help='commit dont on lit les cours (ex. origin/main)')
    analyse.add_argument('--sortie', type=Path, default=SORTIE)
    options = analyse.parse_args()
    REF = options.ref
    extraits = [e for c in CHOIX for e in extraits_de(*c)]
    options.sortie.write_bytes((json.dumps(extraits, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    VOIX_LANDING.write_bytes((json.dumps(voix_landing(), ensure_ascii=False, indent=1) + chr(10)).encode('utf-8'))
    total = sum(e['duree'] for e in extraits)
    sys.stdout.reconfigure(encoding='utf-8')
    for e in extraits:
        print(f"{e['onglet']:9} {e['duree']:5.1f} s  {len(e['commandes'])} commandes  {(e['audio'] or 'feuille, sans voix').rsplit('/', 1)[-1]}")
    print(f'{len(extraits)} extraits, {total:.0f} s -> {options.sortie}')


if __name__ == '__main__':
    main()
