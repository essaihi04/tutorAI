"""Copies manuscrites simulées : chaque copie de copies.json devient une photo de feuille (JPEG ~1280 px).
Écriture « à la main » (Ink Free ou Comic, lettres qui bougent), exposants et indices en petit, fractions superposées
(\\frac{a}{b}), dessins à main levée (tableau, histogramme et courbe, triangle des textures), papier ligné, photo un peu
tournée, floue et mal éclairée. Usage : python rendre.py <dossier banc>"""
import json, math, random, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from fontTools.ttLib import TTFont

B = Path(sys.argv[1])
F = 'C:/Windows/Fonts/'
MAINS = ['Inkfree.ttf', 'comic.ttf']
SECOURS = ['comic.ttf', 'seguisym.ttf']
CMAP = {f: TTFont(F + f).getBestCmap() for f in set(MAINS + SECOURS)}
SUB = {'₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9'}
SUP = {'²': '2', '³': '3', '⁺': '+', '⁻': '-'}


def bloc(s, i):
    """le contenu entre accolades à partir de s[i] == '{' → (contenu, indice après)"""
    n, j = 0, i
    while True:
        if s[j] == '{':
            n += 1
        elif s[j] == '}':
            n -= 1
            if n == 0:
                return s[i + 1:j], j + 1
        j += 1


def jetons(s, sorte='n'):
    out, i = [], 0
    while i < len(s):
        if s.startswith('\\frac{', i):
            num, i = bloc(s, i + 5)
            den, i = bloc(s, i)
            out.append(('frac', jetons(num), jetons(den)))
            continue
        if s.startswith('^{', i) or s.startswith('_{', i):
            txt, j = bloc(s, i + 1)
            out += [(c, 'sup' if s[i] == '^' else 'sub') for c in txt]
            i = j
            continue
        c = s[i]
        out.append((SUB[c], 'sub') if c in SUB else (SUP[c], 'sup') if c in SUP else (c, sorte))
        i += 1
    return out


class Plume:
    def __init__(self, d, rnd, main, taille, encre):
        self.d, self.rnd, self.main, self.taille, self.encre, self.cache = d, rnd, main, taille, encre, {}

    def police(self, c, t):
        for f in [self.main] + SECOURS:
            if c == ' ' or ord(c) in CMAP[f]:
                return self.cache.setdefault((f, t), ImageFont.truetype(F + f, t))
        return self.cache.setdefault(('seguisym.ttf', t), ImageFont.truetype(F + 'seguisym.ttf', t))

    def largeur(self, js, echelle=1.0):
        w = 0
        for j in js:
            if j[0] == 'frac':
                w += max(self.largeur(j[1], 0.8), self.largeur(j[2], 0.8)) + 16
            else:
                c, s = j
                t = int(self.taille * echelle * (1 if s == 'n' else 0.62))
                w += self.d.textlength(c, font=self.police(c, t)) + (1 if c != ' ' else 4)
        return w

    def ecrire(self, x, y, js, echelle=1.0, dessiner=True):
        rnd = self.rnd
        for j in js:
            if j[0] == 'frac':
                wn, wd = self.largeur(j[1], 0.8), self.largeur(j[2], 0.8)
                w = max(wn, wd) + 10
                self.ecrire(x + (w - wn) / 2, y - self.taille * 0.48, j[1], 0.8)
                ly = y + self.taille * 0.62
                self.d.line([(x, ly + rnd.randint(-1, 1)), (x + w, ly + rnd.randint(-2, 2))], fill=self.encre, width=3)
                self.ecrire(x + (w - wd) / 2, y + self.taille * 0.72, j[2], 0.8)
                x += w + 6
                continue
            c, s = j
            t = max(12, int(self.taille * echelle * (1 if s == 'n' else 0.62)) + rnd.randint(-2, 2))
            fnt = self.police(c, t)
            dy = {'n': 0, 'sup': -int(self.taille * echelle * 0.36), 'sub': int(self.taille * echelle * 0.34)}[s] + rnd.randint(-2, 2)
            self.d.text((x, y + dy), c, font=fnt, fill=self.encre)
            x += self.d.textlength(c, font=fnt) * rnd.uniform(0.96, 1.06) + (1 if c != ' ' else rnd.randint(2, 6))
        return x

    def trait(self, p, q, largeur=3):
        """un trait à main levée (légèrement ondulé)"""
        rnd = self.rnd
        n = max(2, int(math.dist(p, q) / 40))
        pts = []
        for k in range(n + 1):
            t = k / n
            pts.append((p[0] + (q[0] - p[0]) * t + (rnd.uniform(-1.5, 1.5) if 0 < k < n else 0),
                        p[1] + (q[1] - p[1]) * t + (rnd.uniform(-1.5, 1.5) if 0 < k < n else 0)))
        self.d.line(pts, fill=self.encre, width=largeur, joint='curve')


def tableau(pl, x0, y0, lignes):
    hs, w0 = 70, 220
    w1 = max(pl.largeur(jetons(l[1]), 0.8) for l in lignes) + 40
    for k, l in enumerate(lignes):
        y = y0 + k * hs
        pl.ecrire(x0 + 12, y + 14, jetons(l[0]), 0.8)
        pl.ecrire(x0 + w0 + 14, y + 14, jetons(l[1]), 0.8)
    for k in range(len(lignes) + 1):
        pl.trait((x0, y0 + k * hs), (x0 + w0 + w1, y0 + k * hs))
    for x in (x0, x0 + w0, x0 + w0 + w1):
        pl.trait((x, y0), (x, y0 + len(lignes) * hs))
    return y0 + len(lignes) * hs


def histo(pl, x0, y0, spec):
    # le tableau des comptes
    lignes = [['IF', 'I     II     III     IV     V'], ["nombre d'espèces", '     '.join(spec['tableau'])]]
    y = tableau(pl, x0, y0, lignes) + 110
    # les axes
    ox, oy, u, larg = x0 + 90, y + 6 * 60, 60, 110
    pl.trait((ox, oy), (ox + 6 * larg, oy))
    pl.trait((ox + 6 * larg, oy), (ox + 6 * larg - 15, oy - 8)); pl.trait((ox + 6 * larg, oy), (ox + 6 * larg - 15, oy + 8))
    pl.trait((ox, oy), (ox, oy - 6.6 * u))
    pl.trait((ox, oy - 6.6 * u), (ox - 8, oy - 6.6 * u + 15)); pl.trait((ox, oy - 6.6 * u), (ox + 8, oy - 6.6 * u + 15))
    pl.ecrire(ox + 25, oy - 6.9 * u - 10, jetons("nombre d'espèces"), 0.7)
    pl.ecrire(ox + 6 * larg - 160, oy + 45, jetons('indice de fréquence'), 0.7)
    for k in range(1, 7):
        pl.trait((ox - 8, oy - k * u), (ox + 8, oy - k * u), 2)
        pl.ecrire(ox - 40, oy - k * u - 22, jetons(str(k)), 0.7)
    noms = ['I', 'II', 'III', 'IV', 'V']
    ecart = 0 if spec['colles'] else 26
    milieux = []
    for k, h in enumerate(spec['hauteurs']):
        g = ox + 20 + k * (larg + ecart)
        dr = g + larg - (0 if spec['colles'] else 0)
        haut = oy - h * u
        pl.trait((g, oy), (g, haut)); pl.trait((g, haut), (dr, haut)); pl.trait((dr, haut), (dr, oy))
        pl.ecrire(g + larg / 2 - 12, oy + 6, jetons(noms[k]), 0.7)
        milieux.append((g + larg / 2, haut))
    if spec['courbe']:
        pts = [(milieux[0][0] - larg, oy)] + milieux + [(milieux[-1][0] + larg, oy)]
        for p, q in zip(pts, pts[1:]):
            pl.trait(p, q, 3)
        for p in milieux:
            pl.d.ellipse([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], fill=pl.encre)
    return oy + 90


def triangle(pl, x0, y0, spec):
    """sommets : argile en haut, sable en bas à gauche, limon en bas à droite"""
    cote = 560
    A = (x0 + cote / 2, y0)
    S = (x0, y0 + cote * math.sqrt(3) / 2)
    L = (x0 + cote, y0 + cote * math.sqrt(3) / 2)
    pt = lambda a, s, l: (A[0] * a / 100 + S[0] * s / 100 + L[0] * l / 100, A[1] * a / 100 + S[1] * s / 100 + L[1] * l / 100)
    pl.trait(A, S); pl.trait(S, L); pl.trait(L, A)
    for k in range(10, 100, 10):
        pl.ecrire(*pt(k, 100 - k, 0), jetons(str(k)), 0.45)            # axe de l'argile (côté gauche)
        pl.ecrire(*(lambda p: (p[0] + 6, p[1] - 10))(pt(100 - k, 0, k)), jetons(str(k)), 0.45)  # axe du limon (droite)
        pl.ecrire(*(lambda p: (p[0] - 10, p[1] + 8))(pt(0, k, 100 - k)), jetons(str(k)), 0.45)  # axe du sable (base)
    pl.ecrire(x0 - 40, y0 + cote * 0.35, jetons('Argile %'), 0.6)
    pl.ecrire(x0 + cote * 0.78, y0 + cote * 0.35, jetons('Limon %'), 0.6)
    pl.ecrire(x0 + cote * 0.4, y0 + cote * 0.95, jetons('Sable %'), 0.6)
    s = spec['sol']
    P = pt(s['argile'], s['sable'], s['limon'])
    if spec['juste']:
        # chaque ligne part de sa graduation, parallèle au bon côté, jusqu'au point
        pl.trait(pt(s['argile'], 100 - s['argile'], 0), P, 3)
        pl.trait(pt(100 - s['limon'], 0, s['limon']), P, 3)
        pl.trait(pt(0, s['sable'], 100 - s['sable']), P, 3)
    else:
        # lignes tracées au hasard, pas parallèles aux côtés
        pl.trait(pt(s['argile'], 100 - s['argile'], 0), (P[0] + 40, P[1] + 30), 3)
        pl.trait((P[0] - 60, P[1] + 90), P, 3)
    pl.d.ellipse([P[0] - 6, P[1] - 6, P[0] + 6, P[1] + 6], fill=pl.encre)
    pl.ecrire(P[0] + 10, P[1] - 30, jetons('C'), 0.7)
    return y0 + cote + 60


def rendre(copie, chemin, graine):
    rnd = random.Random(graine)
    main = rnd.choice(MAINS)
    taille = rnd.randint(38, 44)
    encre = rnd.choice([(20, 30, 120), (25, 25, 35), (30, 50, 140)])
    lignes = copie['texte'].split('\n')
    haut_txt = sum(150 if '\\frac' in l else 78 for l in lignes)
    haut_dessin = {'tableau': 330, 'histo': 760, 'triangle': 620}.get((copie.get('dessin') or {}).get('type'), 0)
    W, H = 1400, max(600, 120 + haut_txt + haut_dessin + 80)
    papier = Image.new('RGB', (W, H), (rnd.randint(238, 250), rnd.randint(236, 248), rnd.randint(228, 242)))
    d = ImageDraw.Draw(papier)
    for y in range(100, H, 78):
        d.line([(0, y + 12), (W, y + 12)], fill=(190, 205, 225), width=2)
    d.line([(110, 0), (110, H)], fill=(225, 160, 160), width=2)
    pl = Plume(d, rnd, main, taille, encre)
    y = 100 - taille
    dessin = copie.get('dessin')
    for k, ligne in enumerate(lignes):
        if '\\frac' in ligne:
            y += 36
        pl.ecrire(140 + rnd.randint(-6, 10), y, jetons(ligne))
        y += 114 if '\\frac' in ligne else 78
        # le tableau d'avancement se dessine sous la première ligne
        if dessin and dessin['type'] == 'tableau' and k == 0:
            y = tableau(pl, 150, y + 10, dessin['lignes']) + 40
    if dessin and dessin['type'] == 'histo':
        histo(pl, 150, y + 10, dessin)
    if dessin and dessin['type'] == 'triangle':
        triangle(pl, 300, y + 40, dessin)
    papier = papier.rotate(rnd.uniform(-2.5, 2.5), resample=Image.BICUBIC, expand=True, fillcolor=(205, 200, 190))
    papier = papier.filter(ImageFilter.GaussianBlur(rnd.uniform(0.4, 0.9)))
    grad = Image.linear_gradient('L').resize(papier.size).rotate(rnd.choice([0, 90, 180, 270]))
    papier = Image.composite(papier, Image.blend(papier, Image.new('RGB', papier.size, (0, 0, 0)), 0.18), grad.point(lambda v: 255 - v // 3))
    papier.thumbnail((1280, 1280))
    papier.save(chemin, 'JPEG', quality=rnd.randint(72, 86))


copies = json.loads((B / 'copies.json').read_text(encoding='utf-8'))
(B / 'photos').mkdir(exist_ok=True)
for k, c in enumerate(copies):
    c['photo'] = f"{k + 1:02d}_{c['sujet']}_{c['id']}_{c['niveau']}.jpg"
    rendre(c, B / 'photos' / c['photo'], 1000 + k)
(B / 'copies.json').write_text(json.dumps(copies, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(copies), 'photos')
