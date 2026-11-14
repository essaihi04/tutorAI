/* Écrit par maths_build/primitives/build.py depuis les p*.py du cours math_ch4_primitives : ne pas modifier à la main. */
window.CALCULS = {
 "d3": {
  "titre": "Vérifier une primitive : trois lignes",
  "lignes": [
   {
    "t": "F(x) = x³ − 1/x + 1 ; f(x) = 3x² + 1/x² ; I = ]0 ; +∞[",
    "c": "blanc",
    "m": "enonce",
    "taille": 18,
    "inter": 46
   },
   {
    "t": "F est dérivable sur ]0 ; +∞[ (somme de fonctions dérivables).",
    "c": "cyan",
    "m": "derivable",
    "taille": 18,
    "r": [
     "derivable",
     "ligne 1 : F est dérivable sur I"
    ]
   },
   {
    "t": "Pour tout x de ]0 ; +∞[ : F’(x) = 3x² − (−1/x²) + 0",
    "c": "cyan",
    "m": "deriver",
    "taille": 18
   },
   {
    "t": "= 3x² + 1/x² = f(x).",
    "c": "jaune",
    "m": "egal",
    "dx": 150,
    "taille": 18,
    "r": [
     "egal",
     "ligne 2 : on trouve f(x)"
    ]
   },
   {
    "t": "Donc F est une primitive de f sur ]0 ; +∞[.",
    "c": "vert",
    "m": "conclusion",
    "taille": 18,
    "cadre": "vert",
    "r": [
     "conclusion",
     "ligne 3 : la conclusion"
    ]
   }
  ]
 },
 "d4": {
  "titre": "Vérifier quand F est un produit",
  "lignes": [
   {
    "t": "H(x) = x sin x ; h(x) = sin x + x cos x ; sur ℝ",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 44
   },
   {
    "t": "H est dérivable sur ℝ (produit de fonctions dérivables).",
    "c": "cyan",
    "m": "derivable",
    "taille": 18
   },
   {
    "t": "u(x) = x ; u’(x) = 1        v(x) = sin x ; v’(x) = cos x",
    "c": "orange",
    "m": "a_part",
    "taille": 18,
    "cadre": "orange",
    "r": [
     "a_part",
     "u, u’, v, v’ écrits à part"
    ]
   },
   {
    "t": "(uv)’ = u’v + uv’",
    "c": "jaune",
    "m": "formule",
    "taille": 20,
    "r": [
     "formule",
     "la dérivée d’un produit"
    ]
   },
   {
    "t": "Pour tout x ∈ ℝ : H’(x) = 1·sin x + x·cos x = h(x).",
    "c": "cyan",
    "m": "deriver",
    "taille": 18,
    "r": [
     "deriver",
     "on trouve h(x)"
    ]
   },
   {
    "t": "Donc H est une primitive de h sur ℝ.",
    "c": "vert",
    "m": "conclusion",
    "taille": 18,
    "cadre": "vert"
   }
  ]
 },
 "e1": {
  "titre": "Continue sur un intervalle : des primitives",
  "lignes": [
   {
    "t": "f continue sur I  ⇒  f admet des primitives sur I",
    "c": "jaune",
    "m": "propriete",
    "taille": 22,
    "cadre": "jaune",
    "inter": 56,
    "r": [
     "propriete",
     "la propriété admise"
    ]
   },
   {
    "t": "f(x) = x² − 3x + 1",
    "c": "blanc",
    "m": "exemple",
    "taille": 20
   },
   {
    "t": "f est une fonction polynôme, donc f est continue sur ℝ.",
    "c": "cyan",
    "m": "continue",
    "taille": 18,
    "r": [
     "continue",
     "on justifie la continuité"
    ]
   },
   {
    "t": "Donc f admet des primitives sur ℝ.",
    "c": "vert",
    "m": "conclusion",
    "taille": 18,
    "cadre": "vert"
   }
  ]
 },
 "e4": {
  "titre": "Toutes les primitives : F + k",
  "lignes": [
   {
    "t": "(F(x) + k)’ = F’(x) + 0 = f(x)",
    "c": "cyan",
    "m": "plus_k",
    "taille": 20,
    "r": [
     "plus_k",
     "F + k est une primitive"
    ]
   },
   {
    "t": "G autre primitive : (G − F)’(x) = f(x) − f(x) = 0",
    "c": "cyan",
    "m": "difference",
    "taille": 19,
    "r": [
     "difference",
     "la dérivée de G − F est nulle"
    ]
   },
   {
    "t": "dérivée nulle sur un intervalle : G(x) − F(x) = k",
    "c": "orange",
    "m": "constante",
    "taille": 19
   },
   {
    "t": "G(x) = F(x) + k, k ∈ ℝ",
    "c": "jaune",
    "m": "toutes",
    "taille": 24,
    "cadre": "jaune",
    "r": [
     "toutes",
     "toutes les primitives : F + k"
    ]
   }
  ]
 },
 "e7": {
  "titre": "La condition F(1) = 3 : calcul plus long",
  "lignes": [
   {
    "t": "f(x) = 2x² + x + 1 + 1/x²  sur ]0 ; +∞[",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 40
   },
   {
    "t": "F(x) = (2/3)x³ + (1/2)x² + x − 1/x + k, k ∈ ℝ",
    "c": "cyan",
    "m": "primitives",
    "taille": 19,
    "r": [
     "primitives",
     "toutes les primitives, avec + k"
    ]
   },
   {
    "t": "F(1) = 3 ⇔ 2/3 + 1/2 + 1 − 1 + k = 3",
    "c": "cyan",
    "m": "remplacer",
    "taille": 19,
    "r": [
     "remplacer",
     "on remplace x par 1"
    ]
   },
   {
    "t": "⇔ 7/6 + k = 3 ⇔ k = 3 − 7/6 = 11/6",
    "c": "orange",
    "m": "resoudre",
    "taille": 19,
    "r": [
     "resoudre",
     "on résout en k"
    ]
   },
   {
    "t": "F(x) = (2/3)x³ + (1/2)x² + x − 1/x + 11/6",
    "c": "jaune",
    "m": "resultat",
    "taille": 20,
    "cadre": "jaune",
    "r": [
     "resultat",
     "F écrite complète"
    ]
   }
  ]
 },
 "u3": {
  "titre": "Le coefficient reste devant",
  "lignes": [
   {
    "t": "2x³ = 2 × x³",
    "c": "blanc",
    "m": "ecrire",
    "taille": 24,
    "inter": 50
   },
   {
    "t": "le 2 reste devant : on ne le touche pas",
    "c": "orange",
    "m": "devant",
    "dx": 30,
    "r": [
     "coefficient",
     "le coefficient 2 reste devant"
    ]
   },
   {
    "t": "une primitive : 2 × x⁴/4 = x⁴/2",
    "c": "jaune",
    "m": "primitive",
    "cadre": "jaune",
    "taille": 22,
    "inter": 50,
    "r": [
     "primitive",
     "une primitive de 2x³ : x⁴/2"
    ]
   },
   {
    "t": "vérification : (x⁴/2)’ = 4x³/2 = 2x³",
    "c": "vert",
    "m": "verification",
    "r": [
     "verification",
     "on dérive pour vérifier"
    ]
   },
   {
    "t": "2x³ → 2x × x⁴/4",
    "c": "rouge",
    "m": "piege",
    "barre": true,
    "r": [
     "piege",
     "le coefficient ne se primitive pas"
    ]
   }
  ]
 },
 "l2": {
  "titre": "Un produit : facteur par facteur ?",
  "lignes": [
   {
    "t": "x cos x : facteur par facteur ?",
    "c": "blanc",
    "m": "question",
    "taille": 22,
    "inter": 46
   },
   {
    "t": "x → x²/2   et   cos x → sin x",
    "c": "orange",
    "m": "facteurs",
    "dx": 24
   },
   {
    "t": "essai : (x²/2)·sin x",
    "c": "orange",
    "m": "essai",
    "dx": 24
   },
   {
    "t": "on dérive : ((x²/2)·sin x)’ = x·sin x + (x²/2)·cos x",
    "c": "cyan",
    "m": "derivee",
    "r": [
     "derivee",
     "on dérive le produit : u’v + uv’"
    ]
   },
   {
    "t": "x·sin x + (x²/2)·cos x ≠ x cos x",
    "c": "rouge",
    "m": "different",
    "r": [
     "different",
     "ce n’est pas x cos x"
    ]
   },
   {
    "t": "(x²/2)·sin x est une primitive de x cos x",
    "c": "rouge",
    "m": "faux",
    "barre": true,
    "r": [
     "faux",
     "la fausse réponse"
    ]
   },
   {
    "t": "Un produit ne se primitive pas facteur par facteur.",
    "c": "jaune",
    "m": "regle",
    "cadre": "jaune",
    "r": [
     "regle",
     "la règle"
    ]
   }
  ]
 },
 "l3": {
  "titre": "Transformer l’écriture avant de primitiver",
  "lignes": [
   {
    "t": "f(x) = (x² + 1)/x²   sur ]0 ; +∞[",
    "c": "blanc",
    "m": "enonce",
    "taille": 22,
    "inter": 46
   },
   {
    "t": "pas dans le tableau : on transforme",
    "c": "orange",
    "m": "transformer",
    "r": [
     "transformer",
     "on transforme l’écriture"
    ]
   },
   {
    "t": "f(x) = x²/x² + 1/x² = 1 + 1/x²",
    "c": "cyan",
    "m": "separer",
    "r": [
     "separer",
     "on sépare la fraction"
    ]
   },
   {
    "t": "1 → x   ;   1/x² → −1/x",
    "c": "cyan",
    "m": "tableau",
    "dx": 24
   },
   {
    "t": "primitives : x ↦ x − 1/x + k, k ∈ ℝ",
    "c": "jaune",
    "m": "resultat",
    "cadre": "jaune",
    "taille": 21,
    "inter": 48,
    "r": [
     "resultat",
     "les primitives de f sur ]0 ; +∞["
    ]
   },
   {
    "t": "autres gestes : développer (x + 1)² ; écrire √x = x^{1/2}",
    "c": "blanc",
    "m": "autres",
    "taille": 17
   }
  ]
 },
 "c1": {
  "titre": "u’uⁿ : la dérivée lue à l’envers",
  "lignes": [
   {
    "t": "(u^{n+1})’ = (n + 1) u’ uⁿ",
    "c": "blanc",
    "m": "derivee",
    "taille": 22,
    "r": [
     "derivee",
     "la dérivée de u^{n+1}"
    ]
   },
   {
    "t": "la puissance descend, et u’ apparaît",
    "c": "faible",
    "dx": 30,
    "taille": 17
   },
   {
    "t": "on divise par n + 1 :",
    "c": "blanc",
    "taille": 19
   },
   {
    "t": "(u^{n+1}/(n + 1))’ = u’ uⁿ",
    "c": "cyan",
    "m": "divise",
    "dx": 30,
    "taille": 22
   },
   {
    "t": "u’ uⁿ  →  u^{n+1}/(n + 1)    (n ∈ ℕ*)",
    "c": "jaune",
    "m": "regle",
    "taille": 23,
    "cadre": "jaune",
    "r": [
     "regle",
     "une primitive de u’uⁿ"
    ]
   },
   {
    "t": "exemple : ((x² + 1)⁴)’ = 4 × 2x × (x² + 1)³ = 8x(x² + 1)³",
    "c": "vert",
    "m": "exemple",
    "taille": 18,
    "r": [
     "exemple",
     "la dérivée de (x² + 1)⁴"
    ]
   }
  ]
 },
 "c4": {
  "titre": "(2x − 1)³ : la bulle donne un nombre",
  "lignes": [
   {
    "t": "f(x) = (2x − 1)³",
    "c": "blanc",
    "m": "expression",
    "taille": 22
   },
   {
    "t": "bulle : (2x − 1)’ = 2",
    "c": "cyan",
    "m": "bulle",
    "dx": 30,
    "taille": 20,
    "cadre": "cyan",
    "r": [
     "bulle",
     "la dérivée de 2x − 1 : un nombre"
    ]
   },
   {
    "t": "f(x) = ½ × 2(2x − 1)³ = ½ (2x − 1)’(2x − 1)³",
    "c": "blanc",
    "m": "reecrire",
    "taille": 19
   },
   {
    "t": "forme u’uⁿ, n = 3",
    "c": "vert",
    "dx": 30,
    "taille": 18
   },
   {
    "t": "F(x) = ½ × (2x − 1)⁴/4 = (2x − 1)⁴/8",
    "c": "jaune",
    "m": "primitive",
    "taille": 22,
    "cadre": "jaune",
    "r": [
     "primitive",
     "une primitive : (2x − 1)⁴/8"
    ]
   },
   {
    "t": "F(x) = (2x − 1)⁴/4",
    "c": "rouge",
    "m": "piege",
    "taille": 19,
    "barre": true,
    "r": [
     "piege",
     "l’oubli du ½"
    ]
   }
  ]
 },
 "c5": {
  "titre": "Une racine : on passe en puissance",
  "lignes": [
   {
    "t": "f(x) = 6x · ∛(3x² + 1)",
    "c": "blanc",
    "m": "expression",
    "taille": 22
   },
   {
    "t": "bulle : (3x² + 1)’ = 6x   et   3x² + 1 > 0",
    "c": "cyan",
    "m": "bulle",
    "dx": 30,
    "taille": 19,
    "cadre": "cyan",
    "r": [
     "bulle",
     "u’ = 6x et u > 0"
    ]
   },
   {
    "t": "∛(3x² + 1) = (3x² + 1)^{1/3}",
    "c": "blanc",
    "m": "puissance",
    "taille": 20,
    "r": [
     "puissance",
     "la racine écrite en puissance"
    ]
   },
   {
    "t": "f(x) = (3x² + 1)’ (3x² + 1)^{1/3} : forme u’uʳ, r = 1/3",
    "c": "vert",
    "m": "forme",
    "taille": 18
   },
   {
    "t": "F(x) = (3x² + 1)^{4/3}/(4/3) = (3/4) ∛((3x² + 1)⁴)",
    "c": "jaune",
    "m": "primitive",
    "taille": 20,
    "cadre": "jaune",
    "r": [
     "primitive",
     "une primitive"
    ]
   }
  ]
 },
 "c6": {
  "titre": "u’/u² : un carré en bas",
  "lignes": [
   {
    "t": "(−1/u)’ = u’/u²   donc   u’/u² → −1/u",
    "c": "jaune",
    "m": "regle",
    "taille": 21,
    "cadre": "jaune",
    "r": [
     "regle",
     "une primitive de u’/u²"
    ]
   },
   {
    "t": "f(x) = x/(x² + 1)²",
    "c": "blanc",
    "m": "expression",
    "taille": 21
   },
   {
    "t": "bulle : (x² + 1)’ = 2x",
    "c": "cyan",
    "m": "bulle",
    "dx": 30,
    "taille": 19,
    "cadre": "cyan",
    "r": [
     "bulle",
     "u’ = 2x : il manque 2"
    ]
   },
   {
    "t": "f(x) = ½ × 2x/(x² + 1)² = ½ × (x² + 1)’/(x² + 1)²",
    "c": "blanc",
    "m": "reecrire",
    "taille": 18
   },
   {
    "t": "forme u’/u²",
    "c": "vert",
    "dx": 30,
    "taille": 18
   },
   {
    "t": "F(x) = ½ × (−1/(x² + 1)) = −1/(2(x² + 1))",
    "c": "jaune",
    "m": "primitive",
    "taille": 20,
    "cadre": "jaune",
    "r": [
     "primitive",
     "une primitive"
    ]
   }
  ]
 },
 "c7": {
  "titre": "u’/√u : une racine en bas",
  "lignes": [
   {
    "t": "(√u)’ = u’/(2√u)",
    "c": "blanc",
    "m": "derivee",
    "taille": 21,
    "r": [
     "derivee",
     "la dérivée de √u"
    ]
   },
   {
    "t": "(2√u)’ = u’/√u   donc   u’/√u → 2√u   (u > 0)",
    "c": "jaune",
    "m": "regle",
    "taille": 20,
    "cadre": "jaune",
    "r": [
     "regle",
     "une primitive de u’/√u"
    ]
   },
   {
    "t": "f(x) = x/√(x² + 1)",
    "c": "blanc",
    "m": "expression",
    "taille": 21
   },
   {
    "t": "bulle : (x² + 1)’ = 2x   et   x² + 1 > 0",
    "c": "cyan",
    "m": "bulle",
    "dx": 30,
    "taille": 19,
    "cadre": "cyan"
   },
   {
    "t": "f(x) = ½ × (x² + 1)’/√(x² + 1) : forme u’/√u",
    "c": "blanc",
    "m": "reecrire",
    "taille": 19
   },
   {
    "t": "F(x) = ½ × 2√(x² + 1) = √(x² + 1)",
    "c": "jaune",
    "m": "primitive",
    "taille": 21,
    "cadre": "jaune",
    "r": [
     "primitive",
     "une primitive"
    ]
   }
  ]
 },
 "c9": {
  "titre": "u’·cos u et u’·sin u",
  "lignes": [
   {
    "t": "u’·cos u → sin u     u’·sin u → −cos u",
    "c": "jaune",
    "m": "regle",
    "taille": 21,
    "cadre": "jaune",
    "r": [
     "regle",
     "les deux formes trigonométriques"
    ]
   },
   {
    "t": "f(x) = πx · cos(πx² + 3)",
    "c": "blanc",
    "m": "expression",
    "taille": 21
   },
   {
    "t": "bulle : (πx² + 3)’ = 2πx",
    "c": "cyan",
    "m": "bulle",
    "dx": 30,
    "taille": 19,
    "cadre": "cyan",
    "r": [
     "bulle",
     "u’ = 2πx : il manque 2"
    ]
   },
   {
    "t": "f(x) = ½ × 2πx · cos(πx² + 3) = ½ (πx² + 3)’ cos(πx² + 3)",
    "c": "blanc",
    "m": "reecrire",
    "taille": 17
   },
   {
    "t": "forme u’·cos u",
    "c": "vert",
    "dx": 30,
    "taille": 18
   },
   {
    "t": "F(x) = ½ sin(πx² + 3)",
    "c": "jaune",
    "m": "primitive",
    "taille": 22,
    "cadre": "jaune",
    "r": [
     "primitive",
     "une primitive"
    ]
   }
  ]
 },
 "r2": {
  "titre": "(u’v − uv’)/v² : la dérivée d’un quotient",
  "lignes": [
   {
    "t": "(u’v − uv’)/v² → u/v",
    "c": "jaune",
    "m": "regle",
    "taille": 22,
    "cadre": "jaune",
    "r": [
     "regle",
     "la dérivée d’un quotient lue à l’envers"
    ]
   },
   {
    "t": "f(x) = (x² + 2x)/(x + 1)²   sur ]−1 ; +∞[",
    "c": "blanc",
    "m": "expression",
    "taille": 20
   },
   {
    "t": "u = x², u’ = 2x ;  v = x + 1, v’ = 1",
    "c": "cyan",
    "m": "bulle",
    "dx": 30,
    "taille": 19,
    "cadre": "cyan",
    "r": [
     "bulle",
     "u, u’, v, v’ écrits à part"
    ]
   },
   {
    "t": "(u’v − uv’)/v² = (2x(x + 1) − x²)/(x + 1)² = (x² + 2x)/(x + 1)²",
    "c": "blanc",
    "m": "verifie",
    "taille": 17
   },
   {
    "t": "F(x) = x²/(x + 1)",
    "c": "jaune",
    "m": "primitive",
    "taille": 22,
    "cadre": "jaune",
    "r": [
     "primitive",
     "une primitive"
    ]
   },
   {
    "t": "autre écriture : x + 1/(x + 1) = x²/(x + 1) + 1 : même famille",
    "c": "vert",
    "m": "famille",
    "taille": 17,
    "r": [
     "famille",
     "deux primitives, une constante d’écart"
    ]
   }
  ]
 },
 "x1": {
  "titre": "Type national : H est une primitive de h",
  "lignes": [
   {
    "t": "H(x) = (x² + 1)√x ;  h(x) = (5x² + 1)/(2√x) ;  I = ]0 ; +∞[",
    "c": "blanc",
    "taille": 18,
    "inter": 40
   },
   {
    "t": "H est dérivable sur ]0 ; +∞[ (produit de fonctions dérivables)",
    "c": "cyan",
    "m": "derivable",
    "taille": 18,
    "r": [
     "derivable",
     "H est dérivable sur l’intervalle"
    ]
   },
   {
    "t": "Pour tout x de ]0 ; +∞[ :",
    "c": "blanc",
    "taille": 18,
    "inter": 34
   },
   {
    "t": "H’(x) = 2x·√x + (x² + 1)·1/(2√x)",
    "c": "blanc",
    "m": "derivee",
    "dx": 30,
    "taille": 19,
    "r": [
     "derivee",
     "la dérivée d’un produit u’v + uv’"
    ]
   },
   {
    "t": "= (4x² + x² + 1)/(2√x)",
    "c": "blanc",
    "m": "calcul",
    "dx": 30,
    "taille": 19
   },
   {
    "t": "= (5x² + 1)/(2√x) = h(x)",
    "c": "jaune",
    "dx": 30,
    "taille": 19,
    "inter": 46,
    "r": [
     "calcul",
     "même dénominateur 2√x"
    ]
   },
   {
    "t": "Donc H est une primitive de h sur ]0 ; +∞[.",
    "c": "vert",
    "m": "conclusion",
    "cadre": "vert",
    "taille": 19,
    "r": [
     "conclusion",
     "la conclusion avec l’intervalle"
    ]
   }
  ]
 },
 "x2": {
  "titre": "Forme u’uⁿ, puis la condition F(0) = 1",
  "lignes": [
   {
    "t": "f(x) = (2x + 1)(x² + x + 1)² sur ℝ ;  F(0) = 1",
    "c": "blanc",
    "taille": 19,
    "inter": 40
   },
   {
    "t": "(x² + x + 1)’ = 2x + 1",
    "c": "orange",
    "m": "bulle",
    "taille": 19,
    "cadre": "orange",
    "r": [
     "bulle",
     "la bulle : u’ = 2x + 1"
    ]
   },
   {
    "t": "f(x) = (x² + x + 1)’(x² + x + 1)² : forme u’u², n = 2",
    "c": "cyan",
    "taille": 18
   },
   {
    "t": "F(x) = (x² + x + 1)³/3 + k, k ∈ ℝ",
    "c": "jaune",
    "m": "primitives",
    "taille": 19,
    "inter": 44,
    "r": [
     "primitives",
     "toutes les primitives"
    ]
   },
   {
    "t": "F(0) = 1 ⇔ 1³/3 + k = 1",
    "c": "blanc",
    "m": "condition",
    "taille": 19
   },
   {
    "t": "⇔ k = 1 − 1/3 = 2/3",
    "c": "blanc",
    "dx": 30,
    "taille": 19,
    "inter": 46,
    "r": [
     "condition",
     "on résout en k"
    ]
   },
   {
    "t": "F(x) = (x² + x + 1)³/3 + 2/3",
    "c": "vert",
    "m": "resultat",
    "cadre": "vert",
    "taille": 21,
    "r": [
     "resultat",
     "la primitive cherchée"
    ]
   }
  ]
 },
 "x3": {
  "titre": "Exercice bilan : existence, formes, condition",
  "lignes": [
   {
    "t": "f(x) = x/(x² + 1)² + cos(2x) ;  F(0) = 0",
    "c": "blanc",
    "taille": 19,
    "inter": 38
   },
   {
    "t": "x² + 1 ≠ 0 : f est continue sur ℝ,",
    "c": "cyan",
    "taille": 18,
    "inter": 30
   },
   {
    "t": "donc f admet des primitives sur ℝ.",
    "c": "cyan",
    "m": "continuite",
    "dx": 30,
    "taille": 18,
    "inter": 38,
    "r": [
     "continuite",
     "continue sur ℝ : des primitives existent"
    ]
   },
   {
    "t": "x/(x² + 1)² = ½ × (x² + 1)’/(x² + 1)² : forme u’/u²",
    "c": "blanc",
    "m": "forme",
    "taille": 18,
    "r": [
     "forme",
     "la forme u’/u² avec le ½"
    ]
   },
   {
    "t": "F(x) = −1/(2(x² + 1)) + ½ sin(2x) + k, k ∈ ℝ",
    "c": "jaune",
    "m": "primitives",
    "taille": 18,
    "inter": 40,
    "r": [
     "primitives",
     "une primitive de chaque terme, une seule k"
    ]
   },
   {
    "t": "F(0) = 0 ⇔ −1/2 + 0 + k = 0 ⇔ k = 1/2",
    "c": "blanc",
    "m": "condition",
    "taille": 18,
    "inter": 42,
    "r": [
     "condition",
     "la condition donne k"
    ]
   },
   {
    "t": "F(x) = −1/(2(x² + 1)) + ½ sin(2x) + 1/2",
    "c": "vert",
    "m": "resultat",
    "cadre": "vert",
    "taille": 19,
    "r": [
     "resultat",
     "la primitive cherchée"
    ]
   }
  ]
 }
};
