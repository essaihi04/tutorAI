"""Nombres dits en darija -> en français dans le texte parlé (21/11/2026, règle de l'utilisateur : « ne pas dire les
chiffres en arabe + le mot en français ; tout dire en français : pas « جوج noyaux » mais « deux noyaux » »).

convertir(texte) -> texte. Une suite de mots-nombres darija (avec « و » entre eux, « فاصلة » pour la virgule) est
traduite quand elle touche du français : le mot suivant (après un éventuel « ديال ») ou le mot précédent est écrit
en lettres latines, ou la suite touche « virgule / fois / puissance / au carré… ». « جوج ديال les X » -> « deux X ».
« بجوج » (les deux, tous les deux) -> « les deux ». « واحد / وحدة » seuls ne sont traduits que dans un nombre
(« واحد virgule », « واحد fois », « زيرو فاصلة واحد ») : ailleurs c'est l'article (« واحد la courbe »)."""
import re
from num2words import num2words

U = {'زيرو': 0, 'صفر': 0, 'واحد': 1, 'وحدة': 1, 'جوج': 2, 'زوج': 2, 'اثنان': 2, 'اثنين': 2, 'جوجة': 2, 'تلاتة': 3, 'ثلاثة': 3, 'تلت': 3, 'ثلاث': 3,
     'ربعة': 4, 'أربعة': 4, 'اربعة': 4, 'ربع': None, 'خمسة': 5, 'خمس': 5, 'ستة': 6, 'ست': 6, 'سبعة': 7, 'سبع': 7,
     'تمنية': 8, 'ثمانية': 8, 'ثمان': 8, 'تمن': 8, 'تسعة': 9, 'تسع': 9, 'عشرة': 10, 'عشر': 10,
     'حداش': 11, 'طناش': 12, 'تلطاش': 13, 'ربعطاش': 14, 'خمسطاش': 15, 'سطاش': 16, 'سبعطاش': 17, 'تمنطاش': 18, 'تسعطاش': 19}
U = {k: v for k, v in U.items() if v is not None}
D = {'عشرين': 20, 'تلاتين': 30, 'ثلاثين': 30, 'ربعين': 40, 'أربعين': 40, 'اربعين': 40, 'خمسين': 50, 'ستين': 60,
     'سبعين': 70, 'تمانين': 80, 'ثمانين': 80, 'تسعين': 90}
C = {'مية': 100, 'ميا': 100, 'مائة': 100, 'مئة': 100, 'ميتين': 200}
M = {'ألف': 1000, 'الف': 1000, 'آلاف': 1000, 'الاف': 1000, 'ألفين': 2000, 'مليون': 10 ** 6}
NOMBRE = set(U) | set(D) | set(C) | set(M)
LAT = re.compile(r"[A-Za-zÀ-ÿœŒ]")
ARA = re.compile(r'[؀-ۿ]')
MATHS = {'virgule', 'fois', 'puissance', 'au', 'sur', 'plus', 'moins', 'égale', 'divisé', 'racine', 'pour', 'cent', 'mille',
         'zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize',
         'quatorze', 'quinze', 'seize', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'cents', 'x', 'n'}
# « واحد virgule », « moins واحد » : le nombre ; « كل واحد zéro… » ou « وحدة: deux » : pas un nombre
MATHS_APRES = {'virgule', 'fois', 'puissance', 'au', 'sur', 'pour', 'divisé', 'mille', 'cent', 'cents', 'égale', 'plus', 'moins'}
MATHS_AVANT = {'virgule', 'fois', 'puissance', 'sur', 'plus', 'moins', 'égale', 'divisé', 'racine', 'de', 'à', 'et'}
SEP = {'فاصلة': 'virgule', 'في': 'fois', 'أس': 'puissance'}


def valeur(mots):
    """Valeur d'une suite de mots-nombres (sans « و »), ou None si la suite n'est pas un nombre bien formé."""
    total, courant = 0, 0
    for i, m in enumerate(mots):
        if m in U:
            v = U[m]
            if courant % 100 and v < 10 and m not in ('عشر',):
                # « خمسة عشر » : unité puis عشر = 15 ; sinon deux unités de suite : pas un nombre
                return None
            courant += v
        elif m == 'عشر' or m == 'عشرة':
            courant += 10
        elif m in D:
            courant += D[m]
        elif m in C:
            courant = (courant or 1) * 100 if C[m] == 100 else courant + 200
        elif m in M:
            total += (courant or 1) * M[m] if M[m] in (1000, 10 ** 6) and m not in ('ألفين',) else 2000
            courant = 0
        else:
            return None
    return total + courant


def un_seul_(parties):
    return [m for p in parties for m in p] in (['واحد'], ['وحدة'])


def fr(v):
    return num2words(v, lang='fr')


JETON = re.compile(r'\S+|\s+')


def convertir(texte):
    jetons = JETON.findall(texte)
    mots = [(i, j) for i, j in enumerate(jetons) if not j.isspace()]
    out = list(jetons)
    k = 0
    while k < len(mots):
        i, j = mots[k]
        nu, ponct = _nu(j)
        prefixe_b = False
        if nu.startswith('ب') and nu[1:] in ('جوج', 'زوج'):
            prefixe_b = True
        if not (nu in NOMBRE or prefixe_b or nu == 'فاصلة'):
            k += 1
            continue
        # étendre la suite : nombres, « و » collé (« وستين »), « فاصلة »
        fin = k
        parties = []  # liste de (mots_du_nombre) séparés par فاصلة
        cour = []
        seps = []
        t = k
        while t < len(mots):
            w, p = _nu(mots[t][1])
            ww = w[1:] if (w.startswith('و') and w[1:] in NOMBRE and w not in NOMBRE) else w
            if t == k and prefixe_b:
                cour.append(w[1:]); fin = t
                if p: break
                t += 1; continue
            if ww in NOMBRE:
                cour.append(ww); fin = t
            elif w == 'و' and cour and t + 1 < len(mots) and _nu(mots[t + 1][1])[0] in NOMBRE:
                pass
            elif w in SEP and cour and t + 1 < len(mots) and _nu(mots[t + 1][1])[0] in NOMBRE:
                parties.append(cour); seps.append(SEP[w]); cour = []; fin = t
            else:
                break
            if p:
                break
            t += 1
        if cour:
            parties.append(cour)
        if not parties or not all(parties):
            k = fin + 1
            continue
        vals = [valeur(p) for p in parties]
        if any(v is None for v in vals):
            k = fin + 1
            continue
        seq = [m for p in parties for m in p]
        _, pfin = _nu(mots[fin][1])
        # contexte (une ponctuation coupe le contexte : « فجهة وحدة: deux » n'est pas un nombre de deux)
        apres = mots[fin + 1][1] if fin + 1 < len(mots) and not pfin else ''
        apres2 = mots[fin + 2][1] if fin + 2 < len(mots) and not pfin else ''
        avant = mots[k - 1][1] if k > 0 else ''
        if _nu(avant)[1]:
            avant = ''
        an_, ap_ = _nu(avant)[0].lower(), _nu(apres)[0].lower()
        dial = ap_ == 'ديال'
        cible = apres2 if dial else apres
        cn = _nu(cible or '')[0]
        lat_apres = bool(LAT.match(cn)) and not ARA.search(cn)
        arabe_apres = bool(ARA.search(cn)) or (dial and not lat_apres)
        lat_avant = bool(LAT.search(an_)) and not ARA.search(an_) and not arabe_apres
        maths = ap_ in MATHS_APRES or an_ in MATHS_AVANT or (ap_ == 'مرات' and not un_seul_(parties))
        un_seul = seq in (['واحد'], ['وحدة'])
        # « جوج بجوج » : deux par deux
        if seq in (['جوج'], ['زوج']) and not prefixe_b and _nu(apres)[0] in ('بجوج', 'بزوج'):
            i0, i1 = mots[k][0], mots[fin + 1][0]
            for x in range(i0, i1 + 1): out[x] = ''
            out[i0] = 'deux par deux' + _nu(apres)[1]
            k = fin + 2
            continue
        if un_seul and not (maths or len(parties) > 1):
            k = fin + 1
            continue
        if not (lat_apres or lat_avant or maths or len(parties) > 1):
            k = fin + 1
            continue
        morceaux = [fr(vals[0])]
        for sep_, p_, v_ in zip(seps, parties[1:], vals[1:]):
            zeros = 0
            if sep_ == 'virgule':
                for m_ in p_:
                    if m_ in ('زيرو', 'صفر'): zeros += 1
                    else: break
            morceaux.append(sep_ + ' ' + ' '.join(['zéro'] * zeros + ([fr(v_)] if len(p_) > zeros else [])))
        texte_fr = ' '.join(morceaux)
        if prefixe_b:
            texte_fr = 'les ' + texte_fr
        # « جوج les voies » : « les deux voies » ; « جوج مرات » : « deux fois »
        if not dial and not pfin and ap_ in ('les', 'des') and not prefixe_b:
            texte_fr = 'les ' + texte_fr
            j_ = mots[fin + 1][0]; out[j_] = ''; out[j_ - 1] = ''
        elif not dial and not pfin and ap_ == 'مرات':
            j_ = mots[fin + 1][0]; out[j_] = 'fois' + _nu(mots[fin + 1][1])[1]
        # remplacer les jetons k..fin
        i0, i1 = mots[k][0], mots[fin][0]
        for x in range(i0, i1 + 1):
            out[x] = ''
        # « ديال les X » / « ديال des X » / « ديال l'X » après le nombre : « deux X »
        if dial and not pfin:
            jd = mots[fin + 1][0]
            art = mots[fin + 2] if fin + 2 < len(mots) else None
            if art and _nu(art[1])[0].lower() in ('les', 'des') and fin + 3 < len(mots):
                out[jd] = ''; out[jd - 1] = ''
                out[art[0]] = ''; out[art[0] - 1] = ''
            elif art and LAT.match(art[1]):
                out[jd] = ''; out[jd - 1] = ''
        out[i0] = texte_fr + pfin
        k = fin + 1
    r = re.sub(r'[ ]{2,}', ' ', ''.join(out))
    # « dix أس moins trois » : l'exposant dit en français entre deux mots français
    r = re.sub(r"(?<=[A-Za-zÀ-ÿ]) أس (?=[A-Za-zÀ-ÿ])", ' puissance ', r)
    # « six virgule cinq في dix » : « في » entre deux nombres français = fois
    nb = r"(?:zéro|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|trente|quarante|cinquante|soixante|cent|cents|mille)"
    r = re.sub(r"(\b" + nb + r") في (?=" + nb + r"\b)", r"\1 fois ", r)
    return r


PONCT = '،,.:;!?)»'


def _nu(j):
    p = ''
    while j and j[-1] in PONCT:
        p = j[-1] + p; j = j[:-1]
    return j, p


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
            f.write_text(json.dumps(m, ensure_ascii=False, indent=ind) + ('\n' if brut.endswith('\n') else ''), encoding='utf-8')
            print(f'{f}: {n[0]} textes convertis')
    print(f'{total} textes avec un nombre darija à côté du français' + (' (convertis)' if ecrire else ''))
