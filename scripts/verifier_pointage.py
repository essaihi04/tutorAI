"""Contrôle statique du pointage d'un cours (voix ↔ simulation ↔ baguette).

Pour chaque diapositive à simulation, vérifie que :
  - chaque `mot` du pointage se trouve dans la parole (sinon la commande part à t = 0) ;
  - les mots sont dans l'ordre de la parole ;
  - chaque `repere` est déclaré dans la simulation (c.repere('id', ...)) ;
  - chaque `play_until {moment}` existe dans les moments de la simulation ;
  - la phrase autour du mot nomme bien l'objet du repère (mots-clés du libellé du repère) — sinon « à revoir ».

Usage : python scripts/verifier_pointage.py backend/data/courses/<cours>.json
"""
import json, re, sys, unicodedata
from pathlib import Path

SEMANTIQUE = '--semantique' in sys.argv   # heuristique « la phrase nomme-t-elle l'objet ? » (bruyante en darija)
RACINE = Path(__file__).resolve().parents[1]
PUBLIC = RACINE / 'frontend' / 'public'
VIDES = set("le la les l de du des d un une et ou à a au aux dans sur en par pour avec sans son sa ses ce cette qui que est c s n y il elle on deux".split())

def sans_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')

def mots_cles(s):
    return {m for m in re.findall(r"[a-z0-9]+", sans_accents(s)) if len(m) > 2 and m not in VIDES}

def lire_sim(url):
    chemin = PUBLIC / url.split('?')[0].lstrip('/')
    if not chemin.exists() or chemin.suffix != '.html':
        return None, {}, set()
    src = chemin.read_text(encoding='utf-8')
    reperes = {}
    for m in re.finditer(r"""repere\(\s*['"]([\w-]+)['"](?:[^;]*?,\s*['"`]([^'"`]*)['"`]\s*\))?""", src):
        reperes.setdefault(m.group(1), m.group(2) or m.group(1))
    moments = set()
    for m in re.finditer(r"const M\s*=\s*\{([^;]*?)\}\s*;", src, re.S):
        moments |= set(re.findall(r"(\w+)\s*:", m.group(1)))
    for m in re.finditer(r"moments\s*:\s*\{([^}]*)\}", src):
        moments |= set(re.findall(r"(\w+)\s*:", m.group(1)))
    # ids construits à l'exécution (c.repere(a.id, …), rep('courbe_o2', …), MOTIFS.x = …) : non lisibles ici
    dynamique = bool(re.search(r"repere\(\s*[^'\"\s]", src)) or bool(re.search(r"rep\(", src))
    moments |= set(re.findall(r"MOTIFS\.(\w+)\s*=", src))
    for m in re.finditer(r"const M\w*\s*=\s*\{([^;]*?)\}", src):
        moments |= set(re.findall(r"(\w+)\s*:", m.group(1)))
    for m in re.finditer(r"rep\(\s*['\"]([\w-]+)['\"]", src):
        reperes.setdefault(m.group(1), m.group(1))
    reperes['__dynamique__'] = dynamique
    return chemin, reperes, moments

def diapos(cours):
    for a in cours.get('activities', []):
        for s in a.get('slides', []):
            yield s

def main(fichier):
    cours = json.loads(Path(fichier).read_text(encoding='utf-8'))
    total = 0
    for s in diapos(cours):
        conc = s.get('concentration') or {}
        pts = conc.get('pointage') or []
        url = (s.get('visual') or {}).get('url', '')
        if not pts:
            continue
        parole = (s.get('speech_text') or {}).get('mixed') or (s.get('speech_text') or {}).get('fr') or ''
        chemin, reperes, moments = lire_sim(url) if url else (None, {}, set())
        defauts = []
        dernier = -1
        for p in pts:
            mot = p.get('mot', '')
            i = parole.find(mot)
            if i < 0:
                defauts.append(f"mot introuvable dans la parole : « {mot} »")
                continue
            if i < dernier:
                defauts.append(f"ordre : « {mot} » avant le mot précédent")
            dernier = i
            if p.get('repere') and chemin is not None:
                r = p['repere']
                if r not in reperes:
                    if reperes.get('__dynamique__'):
                        print(f"  (info) [{s.get('id')}] repère « {r} » construit à l'exécution : à confirmer avec verifier_baguette.py")
                    else:
                        defauts.append(f"repère inconnu de la simulation : {r}")
                elif SEMANTIQUE:
                    # la phrase autour du mot (jusqu'au prochain point) doit nommer l'objet montré
                    fin = min([k for k in (parole.find('.', i), parole.find('؟', i), parole.find(':', i + len(mot))) if k > 0] or [len(parole)])
                    phrase = parole[i:fin + 1]
                    attendus = mots_cles(reperes[r]) | mots_cles(r.replace('_', ' '))
                    if attendus and not (attendus & mots_cles(phrase)):
                        defauts.append(f"à revoir : « {mot} » montre « {reperes[r]} » ({r}) mais la phrase ne le nomme pas : « {phrase.strip()[:90]} »")
            if p.get('commande') == 'play_until' and chemin is not None:
                mo = (p.get('parametres') or {}).get('moment')
                if mo and moments and mo not in moments:
                    if reperes.get('__dynamique__'):
                        print(f"  (info) [{s.get('id')}] moment « {mo} » non lu statiquement : à confirmer avec verifier_baguette.py")
                    else:
                        defauts.append(f"moment inconnu de la simulation : {mo}")
        if url and chemin is None and url.split("?")[0].endswith(".html"):
            defauts.append(f"simulation introuvable : {url}")
        if defauts:
            total += len(defauts)
            print(f"\n[{s.get('id')}] {s.get('title')}  ({url.split('/')[-1]})")
            for d in defauts:
                print('  -', d)
    print(f"\n{total} défaut(s).")
    return 1 if total else 0

if __name__ == '__main__':
    sys.exit(main([a for a in sys.argv[1:] if not a.startswith('--')][0]))
