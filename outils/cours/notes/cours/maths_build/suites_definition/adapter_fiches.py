"""Adapte bilan.html et carte.html (copiés du cours témoin des ondes) au cours des suites. Une seule exécution sur les copies."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"frontend/public/media/simulations/maths/suites-tableau")

def remplacer(s, paires):
    for a, b in paires:
        assert a in s, a[:80]
        s = s.replace(a, b)
    return s

COMMUN = [
 ('<link rel="stylesheet" href="ondes.css">', '<link rel="stylesheet" href="/media/simulations/maths/commun/maths.css">'),
 ('<script src="commun.js"></script>', '<script src="/media/simulations/maths/commun/exposants.js"></script>\n<script src="/media/simulations/maths/commun/maths-tableau.js"></script>'),
]

# ---------------- bilan ----------------
p = D / "bilan.html"; s = p.read_text(encoding="utf-8")
if "const BLOCS = [\n  { id: 'termes'" not in s:
    i = s.index("const BLOCS = ["); j = s.index("];", i) + 2
    s = s[:i] + """const BLOCS = [
  { id: 'termes', titre: '1 · Arithmétique, géométrique', comps: ['K1'], formules: ['u_n = u_p + (n − p)r', 'u_n = u_p·q^{n−p}'],
    def: "Arithmétique : u_{n+1} − u_n = r. Géométrique : u_{n+1} = q·u_n. De u_p à u_n : n − p + 1 termes.",
    attention: "q^{0} = 1, et pas 0." },
  { id: 'recurrence', titre: '2 · Récurrence', comps: ['K2'], formules: ['Initialisation · Hérédité · Conclusion'],
    def: "Vrai au premier rang ; supposé vrai pour UN n, montré au rang n + 1 ; d’après le principe de récurrence, vrai pour tout n.",
    attention: "u_n une fois : opérations ; deux fois : signe de u_{n+1} − a." },
  { id: 'bornee', titre: '3 · Majorée, minorée, bornée', comps: ['K2'], formules: ['u_n ≤ M', 'u_n ≥ m'],
    def: "Majorée par M : pour tout n, u_n ≤ M. Minorée par m : pour tout n, u_n ≥ m. Bornée : les deux.",
    attention: "« pour tout n », pas seulement les premiers termes." },
  { id: 'variation', titre: '4 · Sens de variation', comps: ['K3'], formules: ['u_{n+1} − u_n ≥ 0'],
    def: "Croissante : pour tout n, u_{n+1} ≥ u_n. Signe de u_{n+1} − u_n, ou u_{n+1}/u_n comparé à 1 si u_n > 0.",
    attention: "Deux termes ne suffisent pas." },
  { id: 'auxiliaire', titre: '5 · Suite auxiliaire', comps: ['K4'], formules: ['v_{n+1} = q·v_n', 'v_n = v_0·q^{n}'],
    def: "On écrit v_{n+1}, on remplace u_{n+1} par la relation, on simplifie jusqu’à q·v_n ; puis v_n, puis u_n.",
    attention: "On vise q·v_n : pas de quotient." },
  { id: 'limites', titre: '6 · Limites', comps: ['K5'], formules: ['lim q^{n} = 0 si −1 < q < 1', 'lim f(u_n) = f(a)'],
    def: "q > 1 : +∞ ; q = 1 : 1 ; q ≤ −1 : pas de limite. lim n^{α} = +∞ si α > 0, 0 si α < 0.",
    attention: "La condition « car −1 < q < 1 » avant la limite." },
  { id: 'convergence', titre: '7 · Convergence, comparaison', comps: ['K6'], formules: ['croissante et majorée', 'v_n ≤ u_n ≤ w_n'],
    def: "Croissante et majorée, ou décroissante et minorée : (u_n) converge. Entre v_n et w_n de même limite ℓ : lim u_n = ℓ.",
    attention: "Croissante et minorée : rien. Le plafond n’est pas la limite." },
  { id: 'fonction', titre: '8 · u_{n+1} = f(u_n)', comps: ['K7'], formules: ['ℓ = f(ℓ)'],
    def: "f continue sur I, f(I) ⊂ I, u_0 ∈ I et (u_n) convergente : ℓ est solution de f(x) = x dans I.",
    attention: "Garder la solution qui est dans I." },
  { id: 'problemes', titre: '9 · Rang et somme', comps: ['K8'], formules: ['n − p + 1 termes'],
    def: "Plus petit rang : on résout l’inéquation, n entier. Somme S_n : formule de la somme géométrique, puis sa limite.",
    attention: "La puissance, c’est le nombre de termes." },
];""" + s[j:]
    s = remplacer(s, COMMUN + [
     ("<title>Ce qu'il faut retenir — ondes périodiques</title>", "<title>Ce qu’il faut retenir — suites numériques</title>"),
     ("la fiche du chapitre des ondes progressives périodiques", "la fiche du chapitre des suites numériques"),
     ("Ce qu’il faut retenir — ondes mécaniques progressives périodiques", "Ce qu’il faut retenir — suites numériques"),
     ("id: 'ondes_periodiques_bilan'", "id: 'suites_bilan'"),
     ("title: 'Ce qu’il faut retenir — ondes périodiques'", "title: 'Ce qu’il faut retenir — suites numériques'"),
     ("id: C1..C9", "id: K1..K8"), ("acquis_ids: '[C1, ..]'", "acquis_ids: '[K1, ..]'"),
     ("aller(1, 'start', 'definition')", "aller(1, 'start', 'termes')"),
     ("aller(1, 'reset', 'definition')", "aller(1, 'reset', 'termes')"),
    ])
    s = re.sub(r'aria-label="Fiche de révision[^"]*"', 'aria-label="Fiche de révision écrite à la craie sur une page : pour chaque partie du cours des suites numériques, la définition, les formules et le point d’attention ; deuxième page : ce que l’élève doit retravailler"', s)
    s = re.sub(r"texte: 'Fiche « Ce qu’il faut retenir » du chapitre des ondes[^']*'", "texte: 'Fiche « Ce qu’il faut retenir » du chapitre des suites numériques, sur une page (neuf blocs : arithmétique et géométrique, récurrence, majorée minorée bornée, sens de variation, suite auxiliaire, limites, convergence et comparaison, uₙ₊₁ = f(uₙ), rang et somme ; chacun avec définition, formule, piège), puis la page de l’élève (ce qu’il lui reste à retravailler).'", s)
    k = s.index("/*\n * « Ce qu'"); e = s.index("*/", k) + 2
    s = s[:k] + """/*
 * « Ce qu'il faut retenir » du cours Suites numériques (math_ch3_suites_numeriques, diapositive su_e2_bilan), adapté de
 * la fiche du cours témoin. TOUTE la fiche tient sur UNE page : neuf blocs en trois colonnes, chacun avec la définition,
 * la formule encadrée et le piège en orange (⚠). play_until {moment: <bloc>} écrit ce bloc et le met en lumière ; les blocs
 * déjà dits sont écrits d'un coup. Deuxième page : celle de l'élève (set_parameters {lacunes, acquis, acquis_ids}), K1 à K8.
 */""" + s[e:]
    p.write_text(s, encoding="utf-8")
    print("bilan adapté")

# ---------------- carte ----------------
p = D / "carte.html"; s = p.read_text(encoding="utf-8")
if "comps: ['K1']" not in s:
    i = s.index("const CENTRE = {"); j = s.index("];", i) + 2
    s = s[:i] + """const CENTRE = { x: 380, y: 212, w: 212, h: 108, comps: ['K1'],
  phrase: "Une suite numérique (u_n) associe à chaque entier n un nombre u_n, le terme de rang n." };
const NOEUDS = [
  { id: 'termes', x: 136, y: 76, w: 220, h: 64, couleur: 'cyan', comps: ['K1'], titre: 'Arithmétique · géométrique',
    lignes: ['u_n = u_p + (n − p)r', 'u_n = u_p·q^{n−p}'],
    phrase: "Arithmétique : on ajoute r, u_n = u_p + (n − p)r. Géométrique : on multiplie par q, u_n = u_p·q^{n−p}. Somme : la puissance est le nombre de termes." },
  { id: 'recurrence', x: 380, y: 62, w: 214, h: 64, couleur: 'cyan', comps: ['K2'], titre: 'Récurrence · bornes',
    lignes: ['Initialisation, Hérédité, Conclusion', 'majorée, minorée, bornée'],
    phrase: "La récurrence : vrai au premier rang, puis de n à n + 1, donc pour tout n. Elle sert à montrer qu'une suite est majorée, minorée ou bornée." },
  { id: 'variation', x: 624, y: 76, w: 212, h: 64, couleur: 'jaune', comps: ['K3'], titre: 'Sens de variation',
    lignes: ['signe de u_{n+1} − u_n', 'u_{n+1}/u_n et 1 si u_n > 0'],
    phrase: "Croissante si u_{n+1} ≥ u_n pour tout n : on étudie le signe de u_{n+1} − u_n, ou on compare u_{n+1}/u_n à 1 si les termes sont positifs." },
  { id: 'auxiliaire', x: 640, y: 212, w: 222, h: 64, couleur: 'jaune', comps: ['K4'], titre: 'Suite auxiliaire',
    lignes: ['v_{n+1} = q·v_n → v_n → u_n', 'premier chemin vers u_n'],
    phrase: "La suite auxiliaire v_n est géométrique (ou arithmétique) : on écrit v_n en fonction de n, puis on revient à u_n." },
  { id: 'limites', x: 624, y: 350, w: 220, h: 64, couleur: 'orange', comps: ['K5'], titre: 'Limites',
    lignes: ['lim q^{n} = 0 si −1 < q < 1', 'lim n^{α} ; lim f(u_n) = f(a)'],
    phrase: "lim qⁿ = 0 si −1 < q < 1, +∞ si q > 1 ; lim nᵅ = +∞ si α > 0, 0 si α < 0 ; si u_n → a et f continue en a, f(u_n) → f(a)." },
  { id: 'convergence', x: 380, y: 362, w: 214, h: 64, couleur: 'vert', comps: ['K6'], titre: 'Convergence · comparaison',
    lignes: ['monotone et bornée du bon côté', 'v_n ≤ u_n ≤ w_n → ℓ'],
    phrase: "Croissante et majorée, ou décroissante et minorée : la suite converge. Coincée entre deux suites de même limite ℓ : elle tend vers ℓ." },
  { id: 'fonction', x: 136, y: 350, w: 220, h: 64, couleur: 'vert', comps: ['K7'], titre: 'u_{n+1} = f(u_n)',
    lignes: ['f continue, f(I) ⊂ I, u_0 ∈ I', 'ℓ = f(ℓ) : second chemin'],
    phrase: "Si f est continue sur I, f(I) ⊂ I, u_0 ∈ I et la suite converge, sa limite ℓ est solution de f(x) = x dans I." },
  { id: 'problemes', x: 122, y: 212, w: 200, h: 64, couleur: 'violet', comps: ['K8'], titre: 'Problèmes',
    lignes: ['plus petit rang n', 'somme S_n et sa limite'],
    phrase: "Plus petit rang : on résout une inéquation en n. Somme : n − p + 1 termes, formule géométrique, puis sa limite." },
];""" + s[j:]
    s = remplacer(s, COMMUN + [
     ("<title>Carte du chapitre — ondes périodiques</title>", "<title>Carte du chapitre — suites numériques</title>"),
     ("c.texte('Onde progressive', CENTRE.x, y + 26,", "c.texte('Suite numérique', CENTRE.x, y + 26,"),
     ("c.texte('périodique', CENTRE.x, y + 47,", "c.texte('(u_n)', CENTRE.x, y + 47,"),
     ("'le centre : l’onde progressive périodique et sa définition'", "'le centre : la suite numérique et sa définition'"),
     ("'la définition de l’onde progressive périodique'", "'la définition d’une suite numérique'"),
     ("['la perturbation se répète,', 'identique à elle-même,', 'à intervalles de temps égaux']", "['à chaque entier n,', 'un nombre u_n :', 'le terme de rang n']"),
     ("'Au centre : l’onde progressive périodique.'", "'Au centre : la suite numérique.'"),
     ("Carte conceptuelle : « Onde progressive périodique » au centre", "Carte conceptuelle : « Suite numérique (uₙ) » au centre"),
     ("' avec sa définition (la perturbation se répète, identique à elle-même, à intervalles de temps égaux)'", "' avec sa définition (à chaque entier n, un nombre uₙ)'"),
     ("'Carte du chapitre — ondes mécaniques progressives périodiques'", "'Carte du chapitre — suites numériques'"),
     ("id: 'ondes_periodiques_carte'", "id: 'suites_carte'"),
     ("title: 'Carte du chapitre — ondes périodiques'", "title: 'Carte du chapitre — suites numériques'"),
     ("id: C1..C9", "id: K1..K8"), ("acquis_ids: '[C1, ..]", "acquis_ids: '[K1, ..]"),
    ])
    s = re.sub(r'aria-label="Carte conceptuelle[^"]*"', 'aria-label="Carte conceptuelle dessinée à la craie : la suite numérique au centre avec sa définition, huit branches autour (arithmétique et géométrique, récurrence et bornes, sens de variation, suite auxiliaire, limites, convergence et comparaison, uₙ₊₁ = f(uₙ), problèmes)"', s)
    s = re.sub(r"texte: 'Carte conceptuelle du chapitre des ondes[^']*'", "texte: 'Carte conceptuelle du chapitre des suites numériques : la définition au centre, huit branches autour (arithmétique et géométrique, récurrence et bornes, sens de variation, suite auxiliaire, limites, convergence et comparaison, uₙ₊₁ = f(uₙ), problèmes : rang et somme).'", s)
    k = s.index("/*\n * La carte conceptuelle"); e = s.index("*/", k) + 2
    s = s[:k] + """/*
 * La carte conceptuelle du cours Suites numériques (math_ch3_suites_numeriques, diapositive su_e3_carte), adaptée de la
 * carte du cours témoin. Au centre « Suite numérique (uₙ) » ; sa définition s'écrit au moment `definition`. Puis huit
 * branches dessinées au rythme de la voix (play_until {moment: <branche>}) : termes, recurrence, variation, auxiliaire,
 * limites, convergence, fonction, problemes. L'élève touche une branche : sa phrase s'écrit dans la bulle. Le bilan de
 * l'élève (set_parameters {lacunes, acquis_ids}, K1 à K8) entoure les branches à reprendre.
 */""" + s[e:]
    p.write_text(s, encoding="utf-8")
    print("carte adaptée")
for f in ("bilan.html", "carte.html"):
    t = (D / f).read_text(encoding="utf-8")
    print(f, "restes :", [m for m in re.findall(r".{30}onde.{20}", t, re.I) if "OndesTableau" not in m])
