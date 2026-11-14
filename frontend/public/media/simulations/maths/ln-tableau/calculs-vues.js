/* Écrit par maths_build/fonctions_ln/build.py depuis les p*.py du cours math_ch5_fonctions_ln : ne pas modifier à la main. */
window.CALCULS = {
 "o2": {
  "titre": "Trois gestes à avoir en main",
  "lignes": [
   {
    "t": "① Une primitive de x³ : x⁴/4 (règle xⁿ → xⁿ⁺¹/(n + 1))",
    "c": "cyan",
    "m": "primitive",
    "taille": 19,
    "r": [
     "primitive",
     "une primitive de x³"
    ]
   },
   {
    "t": "② (x − 1)/(x + 2) : s’annule en 1 ; interdit en −2",
    "c": "cyan",
    "m": "signe_racines",
    "taille": 19
   },
   {
    "t": "x : −∞   −2   1   +∞  ;  quotient : +  ‖  −  0  +",
    "c": "blanc",
    "m": "signe",
    "dx": 30,
    "taille": 18,
    "r": [
     "signe",
     "tableau de signe du quotient"
    ]
   },
   {
    "t": "③ −2x > 4 ⇔ x < 4/(−2) ⇔ x < −2",
    "c": "jaune",
    "m": "sens",
    "taille": 19,
    "r": [
     "sens",
     "diviser par −2 change le sens"
    ]
   },
   {
    "t": "diviser par un négatif : le sens change !",
    "c": "orange",
    "m": "piege",
    "dx": 30,
    "taille": 18,
    "cadre": "orange"
   }
  ]
 },
 "a1": {
  "titre": "La calculatrice : ln 2, ln 3, ln 6",
  "lignes": [
   {
    "t": "ln 2 ≈ 0,69",
    "c": "cyan",
    "m": "deux",
    "taille": 20,
    "inter": 46
   },
   {
    "t": "ln 3 ≈ 1,10",
    "c": "cyan",
    "m": "trois",
    "taille": 20,
    "inter": 46
   },
   {
    "t": "ln 6 ≈ 1,79",
    "c": "jaune",
    "m": "six",
    "taille": 20,
    "inter": 46,
    "r": [
     "six",
     "ln 6 ≈ 1,79"
    ]
   },
   {
    "t": "0,69 + 1,10 = 1,79 : la somme tombe sous ln 6",
    "c": "blanc",
    "m": "somme",
    "taille": 19,
    "inter": 50,
    "r": [
     "somme",
     "la somme de ln 2 et ln 3"
    ]
   },
   {
    "t": "6 = 2 × 3 ⇒ ln(2 × 3) = ln 2 + ln 3",
    "c": "vert",
    "m": "produit",
    "taille": 19,
    "inter": 50
   },
   {
    "t": "ln(ab) = ln a + ln b  (a > 0, b > 0)",
    "c": "jaune",
    "m": "regle",
    "taille": 20,
    "cadre": "jaune",
    "r": [
     "regle",
     "la règle du produit"
    ]
   }
  ]
 },
 "a3": {
  "titre": "L'inverse et le quotient",
  "lignes": [
   {
    "t": "a × (1/a) = 1  ⇒  ln a + ln(1/a) = ln 1 = 0",
    "c": "blanc",
    "m": "produit",
    "taille": 19,
    "inter": 50
   },
   {
    "t": "ln(1/a) = −ln a",
    "c": "jaune",
    "m": "inverse",
    "taille": 20,
    "cadre": "jaune",
    "inter": 52,
    "r": [
     "inverse",
     "l'inverse donne un moins"
    ]
   },
   {
    "t": "a/b = a × (1/b)  ⇒  ln(a/b) = ln a + ln(1/b)",
    "c": "blanc",
    "m": "quotient",
    "taille": 19,
    "inter": 50
   },
   {
    "t": "ln(a/b) = ln a − ln b",
    "c": "jaune",
    "m": "difference",
    "taille": 20,
    "cadre": "jaune",
    "inter": 52,
    "r": [
     "difference",
     "le quotient donne une différence"
    ]
   },
   {
    "t": "ln(1/8) = −ln 8 = −ln(2 × 2 × 2) = −3 ln 2",
    "c": "vert",
    "m": "exemple",
    "taille": 19,
    "r": [
     "exemple",
     "ln(1/8) = −3 ln 2"
    ]
   }
  ]
 },
 "a4": {
  "titre": "La puissance et la racine",
  "lignes": [
   {
    "t": "ln(a²) = ln(a × a) = ln a + ln a = 2 ln a",
    "c": "blanc",
    "m": "carre",
    "taille": 19,
    "inter": 48
   },
   {
    "t": "ln(aⁿ) = n ln a  (n ∈ ℤ)",
    "c": "jaune",
    "m": "puissance",
    "taille": 20,
    "cadre": "jaune",
    "inter": 52,
    "r": [
     "puissance",
     "la puissance descend devant"
    ]
   },
   {
    "t": "√a × √a = a  ⇒  2 ln √a = ln a",
    "c": "blanc",
    "m": "racine_produit",
    "taille": 19,
    "inter": 48
   },
   {
    "t": "ln √a = ½ ln a ;  ln(aʳ) = r ln a  (r ∈ ℚ)",
    "c": "jaune",
    "m": "racine",
    "taille": 20,
    "cadre": "jaune",
    "inter": 52,
    "r": [
     "racine",
     "la racine donne un demi"
    ]
   },
   {
    "t": "ln(√2 × 8) = ½ ln 2 + 3 ln 2 = (7/2) ln 2",
    "c": "vert",
    "m": "exemple",
    "taille": 19,
    "r": [
     "exemple",
     "l'exemple ln(√2 × 8)"
    ]
   }
  ]
 },
 "a5": {
  "titre": "Simplifier A = ln 12 − ln 27 + ln √2",
  "lignes": [
   {
    "t": "A = ln 12 − ln 27 + ln √2",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 46
   },
   {
    "t": "12 = 2² × 3 et 27 = 3³",
    "c": "cyan",
    "m": "premiers",
    "taille": 19,
    "inter": 46,
    "r": [
     "premiers",
     "les facteurs premiers"
    ]
   },
   {
    "t": "A = ln(2² × 3) − ln(3³) + ½ ln 2",
    "c": "blanc",
    "m": "regles",
    "taille": 19,
    "inter": 46
   },
   {
    "t": "= 2 ln 2 + ln 3 − 3 ln 3 + ½ ln 2",
    "c": "blanc",
    "m": "developpe",
    "dx": 24,
    "taille": 19,
    "inter": 46
   },
   {
    "t": "A = (5/2) ln 2 − 2 ln 3",
    "c": "jaune",
    "m": "resultat",
    "taille": 20,
    "cadre": "jaune",
    "r": [
     "resultat",
     "on regroupe les ln 2 et les ln 3"
    ]
   }
  ]
 },
 "a6": {
  "titre": "Deux pièges : la somme et le carré",
  "lignes": [
   {
    "t": "ln(1 + 1) = ln 2 ≈ 0,69",
    "c": "blanc",
    "m": "somme",
    "taille": 19,
    "inter": 44
   },
   {
    "t": "ln 1 + ln 1 = 0 + 0 = 0",
    "c": "blanc",
    "m": "faux",
    "taille": 19,
    "inter": 44
   },
   {
    "t": "ln(a + b) = ln a + ln b",
    "c": "rouge",
    "m": "barre",
    "taille": 19,
    "barre": true,
    "inter": 50,
    "r": [
     "barre",
     "ln ne casse pas une somme"
    ]
   },
   {
    "t": "x = −1 : ln((−1)²) = ln 1 = 0, mais −1 ∉ ]0 ; +∞[",
    "c": "orange",
    "m": "carre",
    "taille": 18,
    "inter": 48
   },
   {
    "t": "Pour x ≠ 0 :  ln(x²) = 2 ln|x|",
    "c": "jaune",
    "m": "regle",
    "taille": 20,
    "cadre": "jaune",
    "r": [
     "regle",
     "ln(x²) = 2 ln|x|"
    ]
   }
  ]
 },
 "a7": {
  "titre": "Trouve l'erreur",
  "lignes": [
   {
    "t": "B = ln 16 − ln 27 + 3 ln 36 − ln √2",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 44
   },
   {
    "t": "= 4 ln 2 − 3 ln 3 + 3 ln(2² × 3²) − ½ ln 2",
    "c": "blanc",
    "m": "decompose",
    "dx": 24,
    "taille": 18,
    "inter": 44
   },
   {
    "t": "= 4 ln 2 − 3 ln 3 − 3 ln 2 + 6 ln 3 − ½ ln 2",
    "c": "rouge",
    "m": "faux",
    "dx": 24,
    "taille": 18,
    "barre": true,
    "inter": 44,
    "r": [
     "faux",
     "la ligne fausse"
    ]
   },
   {
    "t": "= 4 ln 2 − 3 ln 3 + 6 ln 2 + 6 ln 3 − ½ ln 2",
    "c": "vert",
    "m": "corrige",
    "dx": 24,
    "taille": 18,
    "inter": 48,
    "r": [
     "corrige",
     "3 ln 36 = 6 ln 2 + 6 ln 3"
    ]
   },
   {
    "t": "B = (19/2) ln 2 + 3 ln 3",
    "c": "jaune",
    "m": "resultat",
    "taille": 20,
    "cadre": "jaune",
    "r": [
     "resultat",
     "la bonne valeur de B"
    ]
   }
  ]
 },
 "q2": {
  "titre": "ln x = r ⇔ x = eʳ",
  "lignes": [
   {
    "t": "ln(2x − 1) = 1",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 46
   },
   {
    "t": "Domaine : 2x − 1 > 0 ⇔ x > ½",
    "c": "cyan",
    "m": "domaine",
    "taille": 18,
    "r": [
     "domaine",
     "d’abord le domaine"
    ]
   },
   {
    "t": "1 = ln e, donc ln(2x − 1) = ln e",
    "c": "cyan",
    "m": "ecrire",
    "taille": 18,
    "r": [
     "ecrire",
     "on écrit 1 comme un ln"
    ]
   },
   {
    "t": "⇔ 2x − 1 = e ⇔ x = (1 + e)/2 ≈ 1,86",
    "c": "jaune",
    "m": "resoudre",
    "taille": 18
   },
   {
    "t": "(1 + e)/2 > ½ : S = {(1 + e)/2}",
    "c": "vert",
    "m": "resultat",
    "taille": 18,
    "cadre": "vert",
    "r": [
     "resultat",
     "la solution est dans le domaine"
    ]
   },
   {
    "t": "Règle : ln x = r ⇔ x = eʳ",
    "c": "jaune",
    "m": "regle",
    "taille": 18,
    "cadre": "jaune",
    "r": [
     "regle",
     "la règle générale"
    ]
   }
  ]
 },
 "q4": {
  "titre": "Second degré en ln x",
  "lignes": [
   {
    "t": "(ln x)² − ln x − 2 = 0, x ∈ ]0 ; +∞[",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 46
   },
   {
    "t": "On pose X = ln x : X² − X − 2 = 0",
    "c": "cyan",
    "m": "poser",
    "taille": 18,
    "r": [
     "poser",
     "on change d’inconnue"
    ]
   },
   {
    "t": "Δ = 1 + 8 = 9 ; X = (1 − 3)/2 = −1 ou X = (1 + 3)/2 = 2",
    "c": "cyan",
    "m": "delta",
    "taille": 18
   },
   {
    "t": "ln x = −1 ⇔ x = e⁻¹ = 1/e ; ln x = 2 ⇔ x = e²",
    "c": "jaune",
    "m": "retour",
    "taille": 18,
    "r": [
     "retour",
     "on revient à x"
    ]
   },
   {
    "t": "1/e et e² sont dans ]0 ; +∞[ : S = {1/e ; e²}",
    "c": "vert",
    "m": "resultat",
    "taille": 18,
    "cadre": "vert",
    "r": [
     "resultat",
     "les deux solutions"
    ]
   }
  ]
 },
 "q6": {
  "titre": "Un système : X = ln x, Y = ln y",
  "lignes": [
   {
    "t": "ln x + ln y = 3 et ln x − ln y = 1",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 46
   },
   {
    "t": "Conditions : x > 0 et y > 0",
    "c": "cyan",
    "m": "conditions",
    "taille": 18,
    "r": [
     "conditions",
     "les conditions"
    ]
   },
   {
    "t": "On pose X = ln x, Y = ln y : X + Y = 3 et X − Y = 1",
    "c": "cyan",
    "m": "poser",
    "taille": 18,
    "r": [
     "poser",
     "les nouvelles inconnues"
    ]
   },
   {
    "t": "En additionnant : 2X = 4 ⇔ X = 2 ; puis Y = 3 − 2 = 1",
    "c": "jaune",
    "m": "resoudre",
    "taille": 18
   },
   {
    "t": "ln x = 2 ⇔ x = e² ; ln y = 1 ⇔ y = e",
    "c": "jaune",
    "m": "retour",
    "taille": 18,
    "r": [
     "retour",
     "retour à x et y"
    ]
   },
   {
    "t": "S = {(e² ; e)}",
    "c": "vert",
    "m": "resultat",
    "taille": 18,
    "cadre": "vert",
    "r": [
     "resultat",
     "le couple solution"
    ]
   }
  ]
 },
 "q7": {
  "titre": "Le plus petit entier n",
  "lignes": [
   {
    "t": "Plus petit entier n tel que (1/4)ⁿ < 10⁻⁴",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 46
   },
   {
    "t": "ln est strictement croissante : ln((1/4)ⁿ) < ln(10⁻⁴)",
    "c": "cyan",
    "m": "passer",
    "taille": 18,
    "r": [
     "passer",
     "on passe au ln"
    ]
   },
   {
    "t": "⇔ n ln(1/4) < −4 ln 10 ⇔ −n ln 4 < −4 ln 10",
    "c": "cyan",
    "m": "descendre",
    "taille": 18
   },
   {
    "t": "−ln 4 < 0 : on divise, le sens change",
    "c": "orange",
    "m": "sens",
    "taille": 18,
    "r": [
     "sens",
     "diviser par un négatif renverse"
    ]
   },
   {
    "t": "⇔ n > 4 ln 10 / ln 4 ≈ 6,64",
    "c": "jaune",
    "m": "calcul",
    "taille": 18
   },
   {
    "t": "Le plus petit entier : n = 7",
    "c": "vert",
    "m": "resultat",
    "taille": 18,
    "cadre": "vert",
    "r": [
     "resultat",
     "la réponse"
    ]
   }
  ]
 },
 "l6": {
  "titre": "Une forme ∞ − ∞ : factoriser par x",
  "lignes": [
   {
    "t": "lim_{x→+∞} (x − ln x) = ?",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 46
   },
   {
    "t": "x → +∞ et ln x → +∞ : forme indéterminée « ∞ − ∞ »",
    "c": "orange",
    "m": "forme",
    "taille": 18,
    "r": [
     "forme",
     "la forme indéterminée"
    ]
   },
   {
    "t": "Pour x > 0 : x − ln x = x(1 − (ln x)/x)",
    "c": "cyan",
    "m": "factoriser",
    "taille": 19,
    "r": [
     "factoriser",
     "on factorise par x"
    ]
   },
   {
    "t": "lim_{x→+∞} (ln x)/x = 0, donc lim (1 − (ln x)/x) = 1",
    "c": "cyan",
    "m": "base",
    "taille": 18
   },
   {
    "t": "Donc lim_{x→+∞} (x − ln x) = +∞.",
    "c": "vert",
    "m": "conclusion",
    "taille": 19,
    "cadre": "vert",
    "r": [
     "conclusion",
     "la conclusion"
    ]
   }
  ]
 },
 "l7": {
  "titre": "Poser t = √x pour retrouver (ln t)/t",
  "lignes": [
   {
    "t": "Montrer que lim_{x→+∞} (ln x)²/x = 0.",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 46
   },
   {
    "t": "On pose t = √x : x = t² et ln x = 2 ln t ; x → +∞ ⇔ t → +∞.",
    "c": "cyan",
    "m": "poser",
    "taille": 18,
    "r": [
     "poser",
     "le changement t = √x"
    ]
   },
   {
    "t": "(ln x)²/x = (2 ln t)²/t² = 4((ln t)/t)²",
    "c": "cyan",
    "m": "transformer",
    "taille": 19,
    "r": [
     "transformer",
     "la limite de base apparaît"
    ]
   },
   {
    "t": "lim_{t→+∞} (ln t)/t = 0",
    "c": "jaune",
    "m": "base",
    "taille": 19
   },
   {
    "t": "Donc lim_{x→+∞} (ln x)²/x = 4 × 0² = 0.",
    "c": "vert",
    "m": "conclusion",
    "taille": 19,
    "cadre": "vert",
    "r": [
     "conclusion",
     "la conclusion"
    ]
   }
  ]
 },
 "l8": {
  "titre": "Continuité et dérivabilité à droite en 0",
  "lignes": [
   {
    "t": "f(x) = 2x ln x − 2x (x > 0) et f(0) = 0",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 44
   },
   {
    "t": "lim_{x→0⁺} x ln x = 0 et lim_{x→0⁺} 2x = 0,",
    "c": "cyan",
    "m": "base",
    "taille": 18
   },
   {
    "t": "donc lim_{x→0⁺} f(x) = 0 = f(0) : f est continue à droite en 0.",
    "c": "vert",
    "m": "continue",
    "taille": 18,
    "r": [
     "continue",
     "continuité à droite"
    ]
   },
   {
    "t": "(f(x) − f(0))/x = 2 ln x − 2",
    "c": "cyan",
    "m": "taux",
    "taille": 19
   },
   {
    "t": "lim_{x→0⁺} (2 ln x − 2) = −∞ : f n’est pas dérivable à droite en 0,",
    "c": "orange",
    "m": "branche",
    "taille": 18
   },
   {
    "t": "(C) admet en O une demi-tangente verticale.",
    "c": "jaune",
    "m": "conclusion",
    "taille": 19,
    "cadre": "jaune",
    "r": [
     "conclusion",
     "l’interprétation"
    ]
   }
  ]
 },
 "v1": {
  "titre": "La dérivée de ln u : u’ sur u",
  "lignes": [
   {
    "t": "(ln u)’ = u’/u   (u dérivable et u > 0 sur I)",
    "c": "jaune",
    "m": "regle",
    "taille": 19,
    "cadre": "jaune",
    "inter": 50,
    "r": [
     "regle",
     "la règle"
    ]
   },
   {
    "t": "f(x) = ln(x² + 1)",
    "c": "blanc",
    "m": "enonce",
    "taille": 19
   },
   {
    "t": "u(x) = x² + 1 > 0 sur ℝ ; u’(x) = 2x",
    "c": "cyan",
    "m": "u",
    "taille": 19,
    "r": [
     "u",
     "on écrit u et u’ à part"
    ]
   },
   {
    "t": "f’(x) = 2x/(x² + 1)",
    "c": "vert",
    "m": "resultat",
    "taille": 20,
    "cadre": "vert",
    "r": [
     "resultat",
     "le résultat"
    ]
   },
   {
    "t": "(ln u)’ = 1/u",
    "c": "rouge",
    "m": "piege",
    "taille": 19,
    "barre": true
   }
  ]
 },
 "v2": {
  "titre": "Un carré de ln, un produit avec ln",
  "lignes": [
   {
    "t": "((ln x)²)’ = 2 × (1/x) × ln x = 2 ln x / x",
    "c": "cyan",
    "m": "carre",
    "taille": 19,
    "inter": 46,
    "r": [
     "carre",
     "u² avec u = ln x"
    ]
   },
   {
    "t": "(x ln x)’ = 1 × ln x + x × 1/x = ln x + 1",
    "c": "cyan",
    "m": "produit",
    "taille": 19,
    "r": [
     "produit",
     "un produit"
    ]
   },
   {
    "t": "f(x) = x + ½ − ln x + ½(ln x)²   (2019 N)",
    "c": "blanc",
    "m": "enonce",
    "taille": 19
   },
   {
    "t": "f’(x) = 1 − 1/x + ½ × 2 ln x / x",
    "c": "cyan",
    "m": "deriver",
    "taille": 19
   },
   {
    "t": "f’(x) = (x − 1 + ln x)/x",
    "c": "vert",
    "m": "resultat",
    "taille": 20,
    "cadre": "vert",
    "r": [
     "resultat",
     "même dénominateur"
    ]
   }
  ]
 },
 "p3": {
  "titre": "Vérifier une primitive avec ln : on dérive",
  "lignes": [
   {
    "t": "H(x) = x ln x − x ; h(x) = ln x ; I = ]0 ; +∞[",
    "c": "blanc",
    "m": "enonce",
    "taille": 19,
    "inter": 46
   },
   {
    "t": "H est dérivable sur ]0 ; +∞[ (produit et somme de fonctions dérivables).",
    "c": "cyan",
    "m": "derivable",
    "taille": 17,
    "r": [
     "derivable",
     "ligne 1 : H est dérivable"
    ]
   },
   {
    "t": "Pour tout x > 0 : H’(x) = 1 × ln x + x × 1/x − 1",
    "c": "cyan",
    "m": "deriver",
    "taille": 19
   },
   {
    "t": "= ln x + 1 − 1 = ln x = h(x).",
    "c": "jaune",
    "m": "egal",
    "dx": 150,
    "taille": 19,
    "r": [
     "egal",
     "ligne 2 : on trouve h(x)"
    ]
   },
   {
    "t": "Donc H est une primitive de h sur ]0 ; +∞[.",
    "c": "vert",
    "m": "conclusion",
    "taille": 19,
    "cadre": "vert",
    "r": [
     "conclusion",
     "ligne 3 : la conclusion"
    ]
   }
  ]
 }
};
