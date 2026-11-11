"""Écrit bilan.html et carte.html de derivation-tableau à partir de ceux de suites-tableau (déjà adaptés au kit maths)."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
M = Path(r"frontend/public/media/simulations/maths")
P = "\\'"   # prime dans une chaîne JS entre apostrophes droites


def rempl(s, a, b, regex=False):
    if regex:
        n = re.subn(a, lambda m: b, s, flags=re.S); assert n[1], a; return n[0]
    assert a in s, a[:80]; return s.replace(a, b)


def bloc(s, debut, fin, nouveau):
    i = s.index(debut); j = s.index(fin, i) + len(fin); return s[:i] + nouveau + s[j:]


BLOCS = """const BLOCS = [
  { id: 'derivabilite', titre: '1 · Dérivabilité en un point', comps: ['K1'], formules: ['lim (f(x) − f(x_0))/(x − x_0) = f§(x_0)'],
    def: "Limite du taux = réel l : f dérivable en x_0, l = f'(x_0). Dérivable en x_0 : dérivable à droite et à gauche, mêmes nombres.",
    attention: "Nombres différents : point anguleux." },
  { id: 'tangente', titre: '2 · Tangente, demi-tangente', comps: ['K2'], formules: ['y = f§(x_0)(x − x_0) + f(x_0)'],
    def: "Tangente en A(x_0 ; f(x_0)). Taux infini : f non dérivable, demi-tangente verticale (vers la courbe).",
    attention: "Vérifier que A est sur (T). f'(x_0) = 0 : horizontale." },
  { id: 'derivees', titre: '3 · Dérivées', comps: ['K3'], formules: ['(u/v)§ = (u§v − uv§)/v²', '(uⁿ)§ = n·u§·uⁿ⁻¹'],
    def: "(u·v)' = u'v + uv' ; (√u)' = u'/(2√u) ; (ⁿ√u)' = u'/(n(ⁿ√u)ⁿ⁻¹). Écrire « f est dérivable sur … ».",
    attention: "Ne jamais oublier u'. Le dénominateur reste factorisé." },
  { id: 'variations', titre: '4 · Variations, extremum', comps: ['K4'], formules: ['f§ > 0 ⟹ f croissante'],
    def: "Le signe de f'(x) est le signe de … ; tableau x | f'(x) | f(x). f' s'annule en changeant de signe : extremum.",
    attention: "Double barre : valeur exclue. Flèches cohérentes avec les limites." },
  { id: 'concavite', titre: '5 · Concavité', comps: ['K5'], formules: ['f§§ ≥ 0 : ∪', 'f§§ ≤ 0 : ∩'],
    def: "f'' s'annule en x_0 en changeant de signe : I(x_0 ; f(x_0)) est un point d'inflexion (la tangente traverse).",
    attention: "f''(x_0) = 0 ne suffit pas (x⁴). Donner le point." },
  { id: 'branches', titre: '6 · Branches infinies', comps: ['K6'], formules: ['x = a', 'y = b', 'y = ax + b'],
    def: "lim f(x)/x : ±∞ → direction (Oy) ; 0 → (Ox) ; a ≠ 0 → lim [f(x) − ax] : b asymptote, ±∞ direction y = ax.",
    attention: "Toujours l'équation et « au voisinage de … »." },
  { id: 'position', titre: '7 · Position relative', comps: ['K7'], formules: ['signe de f(x) − (ax + b)'],
    def: "Positif : (Cf) au-dessus de (Δ) ; négatif : en dessous ; nul : intersection. Tableau avec la ligne du facteur.",
    attention: "Un signe, pas une limite." },
  { id: 'symetrie_trace', titre: '8 · Symétrie et tracé', comps: ['K8', 'K9'], formules: ['f(2a − x) + f(x) = 2b'],
    def: "(2a − x) ∈ Df, puis f(2a − x) = f(x) (axe x = a) ou f(2a − x) + f(x) = 2b (centre Ω(a ; b)). Tracé : droites, points, courbe.",
    attention: "Le domaine d'abord. La courbe en dernier." },
  { id: 'reciproque', titre: '9 · Fonction réciproque', comps: ['K10'], formules: ['(f⁻¹)§(y_0) = 1/f§(x_0)'],
    def: "y_0 = f(x_0), f dérivable en x_0 et f'(x_0) ≠ 0. Courbe de f⁻¹ : symétrique de (Cf) sur I par rapport à y = x.",
    attention: "On dérive f en l'antécédent x_0. f⁻¹ n'est pas 1/f." },
];""".replace("§", P)

# ---------- bilan ----------
s = (M / "suites-tableau/bilan.html").read_text(encoding="utf-8")
s = bloc(s, "const BLOCS = [", "];", BLOCS)
for a, b in [("Ce qu’il faut retenir — suites numériques", "Ce qu’il faut retenir — dérivation et étude des fonctions"),
             ("du cours des suites numériques", "du cours de dérivation et d’étude des fonctions"),
             ("la fiche du chapitre des suites numériques", "la fiche du chapitre de dérivation et étude des fonctions"),
             ("id: 'suites_bilan'", "id: 'derivation_bilan'"), ("id: K1..K8", "id: K1..K10"),
             ("aller(1, 'start', 'termes')", "aller(1, 'start', 'derivabilite')"), ("aller(1, 'reset', 'termes')", "aller(1, 'reset', 'derivabilite')")]:
    s = rempl(s, a, b)
s = rempl(s, r"texte: 'Fiche « Ce qu’il faut retenir » du chapitre des suites numériques[^']*'",
          "texte: 'Fiche « Ce qu’il faut retenir » du chapitre Dérivation et étude des fonctions, sur une page (neuf blocs : dérivabilité, tangente et demi-tangente, dérivées, variations et extremum, concavité, branches infinies, position relative, symétrie et tracé, fonction réciproque ; chacun avec définition, formule, piège), puis la page de l’élève'", regex=True)
s = rempl(s, r"/\*\n \* « Ce qu'il faut retenir » du cours Suites numériques.*?\*/", """/*
 * « Ce qu'il faut retenir » du cours Dérivation et étude des fonctions (math_ch2_derivation_etude_fonctions, diapositive
 * df_fin1_bilan), adapté de la fiche des suites (elle-même du cours témoin). Neuf blocs en trois colonnes, chacun avec la
 * définition, la formule encadrée et le piège en orange (⚠). play_until {moment: <bloc>} écrit ce bloc et le met en lumière.
 * Deuxième page : celle de l'élève (set_parameters {lacunes, acquis, acquis_ids}), compétences K1 à K10.
 * Le prime est écrit ' (le ′ est invisible dans la police de la craie).
 */""", regex=True)
print("restes bilan :", re.findall(r".{30}(?:suites? num|u_n|uₙ).{20}", s, re.I))
(M / "derivation-tableau/bilan.html").write_text(s, encoding="utf-8")

# ---------- carte ----------
NOEUDS = """const CENTRE = { x: 380, y: 212, w: 212, h: 108, comps: ['K9'],
  phrase: "Étudier une fonction : dérivée, variations, branches, concavité, symétrie ; tout finit dans le tracé de sa courbe (Cf)." };
const NOEUDS = [
  { id: 'tangente', x: 136, y: 76, w: 220, h: 64, couleur: 'cyan', comps: ['K1', 'K2'], titre: 'Tangente · dérivabilité',
    lignes: ['lim du taux = fP(x_0)', 'y = fP(x_0)(x − x_0) + f(x_0)'],
    phrase: "Le taux a une limite réelle : f est dérivable, la tangente a pour pente f'(x_0). À droite et à gauche différentes : point anguleux ; infinie : demi-tangente verticale." },
  { id: 'derivees', x: 380, y: 62, w: 214, h: 64, couleur: 'cyan', comps: ['K3'], titre: 'Dérivées',
    lignes: ['(u/v)P = (uPv − uvP)/v²', '(uⁿ)P = n·uP·uⁿ⁻¹ ; (√u)P'],
    phrase: "Produit, quotient, puissance, racine : on nomme u, on dérive u à part, on remplit le gabarit sans oublier u'." },
  { id: 'variations', x: 624, y: 76, w: 212, h: 64, couleur: 'jaune', comps: ['K4'], titre: 'Variations',
    lignes: ['signe de fP → flèches', 'fP s’annule en changeant de signe'],
    phrase: "f' positive : f croissante ; f' négative : f décroissante ; f' s'annule en changeant de signe : extremum." },
  { id: 'concavite', x: 640, y: 212, w: 222, h: 64, couleur: 'jaune', comps: ['K5'], titre: 'Concavité',
    lignes: ['signe de fPP : ∩ ou ∪', 'point d’inflexion'],
    phrase: "f'' positive : courbe tournée vers le haut ; négative : vers le bas ; f'' s'annule en changeant de signe : point d'inflexion." },
  { id: 'branches', x: 624, y: 350, w: 220, h: 64, couleur: 'orange', comps: ['K6', 'K7'], titre: 'Branches · position',
    lignes: ['f(x)/x puis f(x) − ax', 'signe de f(x) − (ax + b)'],
    phrase: "Asymptotes x = a, y = b, y = ax + b ; branches paraboliques ; la position relative vient du signe de f(x) − (ax + b)." },
  { id: 'symetrie', x: 380, y: 362, w: 214, h: 64, couleur: 'vert', comps: ['K8'], titre: 'Symétrie',
    lignes: ['f(2a − x) = f(x) : axe', 'f(2a − x) + f(x) = 2b : centre'],
    phrase: "Axe x = a ou centre Ω(a ; b) : (2a − x) ∈ Df, puis la relation ; la moitié de la courbe suffit." },
  { id: 'trace', x: 136, y: 350, w: 220, h: 64, couleur: 'vert', comps: ['K9'], titre: 'Tracé · lecture',
    lignes: ['droites, points, courbe', 'f(x) = m : intersections'],
    phrase: "On trace les asymptotes et les tangentes, puis les points, puis la courbe d'un trait ; on lit les solutions de f(x) = m." },
  { id: 'reciproque', x: 122, y: 212, w: 200, h: 64, couleur: 'violet', comps: ['K10'], titre: 'Réciproque',
    lignes: ['(f⁻¹)P(y_0) = 1/fP(x_0)', 'miroir y = x'],
    phrase: "f continue et strictement monotone sur I : f⁻¹ existe ; (f⁻¹)'(y_0) = 1/f'(x_0) si f'(x_0) ≠ 0 ; sa courbe est le reflet par rapport à y = x." },
];""".replace("fPP", "f" + P + P).replace("fP", "f" + P).replace("uP", "u" + P).replace("vP", "v" + P).replace(")P", ")" + P)
s = (M / "suites-tableau/carte.html").read_text(encoding="utf-8")
s = bloc(s, "const CENTRE = {", "];", NOEUDS)
for a, b in [("Carte du chapitre — suites numériques", "Carte du chapitre — dérivation et étude des fonctions"),
             ("c.texte('Suite numérique', CENTRE.x, y + 26,", "c.texte('Étude de f', CENTRE.x, y + 26,"),
             ("c.texte('(u_n)', CENTRE.x, y + 47,", "c.texte('la courbe (C_f)', CENTRE.x, y + 47,"),
             ("['à chaque entier n,', 'un nombre u_n :', 'le terme de rang n']", "['dériver, étudier,', 'puis tracer :', 'cinq questions']"),
             ("Carte conceptuelle : « Suite numérique (uₙ) » au centre", "Carte conceptuelle : « Étude de f, la courbe (Cf) » au centre"),
             (" avec sa définition (à chaque entier n, un nombre uₙ)", " avec sa phrase (dériver, étudier, puis tracer)"),
             ("id: 'suites_carte'", "id: 'derivation_carte'"), ("id: K1..K8", "id: K1..K10"),
             ("le centre : la suite numérique et sa définition", "le centre : l’étude de f et la courbe"),
             ("la définition d’une suite numérique", "la phrase du centre : dériver, étudier, puis tracer"),
             ("Au centre : la suite numérique.", "Au centre : l’étude de f et sa courbe.")]:
    s = rempl(s, a, b)
s = rempl(s, r"texte: 'Carte conceptuelle du chapitre des suites numériques[^']*'",
          "texte: 'Carte conceptuelle du chapitre Dérivation et étude des fonctions : l’étude de f au centre, huit branches autour (tangente et dérivabilité, dérivées, variations, concavité, branches infinies et position relative, symétrie, tracé et lecture, fonction réciproque)'", regex=True)
s = re.sub(r'aria-label="Carte conceptuelle[^"]*"', 'aria-label="Carte conceptuelle dessinée à la craie : l’étude d’une fonction au centre, huit branches autour, chacune avec ses formules"', s)
s = rempl(s, r"/\*\n \* La carte conceptuelle du cours Suites numériques.*?\*/", """/*
 * La carte conceptuelle du cours Dérivation et étude des fonctions (math_ch2_derivation_etude_fonctions, diapositive
 * df_fin2_carte), adaptée de la carte des suites. Au centre « Étude de f, la courbe (Cf) » ; sa phrase s'écrit au moment
 * `definition`. Puis huit branches au rythme de la voix (play_until {moment}) : tangente, derivees, variations, concavite,
 * branches, symetrie, trace, reciproque. Le bilan de l'élève (K1 à K10) entoure les branches à reprendre.
 */""", regex=True)
print("restes carte :", re.findall(r".{30}(?:suites? num|u_n|uₙ).{20}", s, re.I))
(M / "derivation-tableau/carte.html").write_text(s, encoding="utf-8")
print("ok")
