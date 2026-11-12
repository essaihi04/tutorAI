/* Écrit par maths_build/operations_formes/build.py depuis les p*.py du cours math_ch6_nombres_complexes : ne pas modifier à la main. */
window.CALCULS = {
 "o2": {
  "titre": "Trois gestes à avoir en main",
  "lignes": [
   {
    "t": "① x² − 2x + 4 = 0 : Δ = (−2)² − 4 × 1 × 4",
    "c": "cyan",
    "m": "delta",
    "r": [
     "delta",
     "le discriminant de x² − 2x + 4"
    ]
   },
   {
    "t": "Δ = 4 − 16 = −12 < 0 : pas de solution réelle",
    "c": "orange",
    "m": "negatif",
    "dx": 30,
    "cadre": "orange",
    "r": [
     "negatif",
     "Δ < 0 : pas de solution réelle"
    ]
   },
   {
    "t": "② cos π/3 = 1/2  ;  sin π/3 = √3/2",
    "c": "cyan",
    "m": "angles",
    "r": [
     "angles",
     "cos π/3 et sin π/3"
    ]
   },
   {
    "t": "③ (a − b)(a + b) = a² − b²",
    "c": "cyan",
    "m": "identite",
    "r": [
     "identite",
     "l'identité remarquable"
    ]
   },
   {
    "t": "Δ < 0… et pourtant, avec i, on trouvera des solutions !",
    "c": "jaune",
    "m": "annonce",
    "cadre": "jaune"
   }
  ]
 },
 "a5": {
  "titre": "Deux complexes égaux : deux équations",
  "lignes": [
   {
    "t": "z = z’ ⇔ Re(z) = Re(z’) et Im(z) = Im(z’)",
    "c": "jaune",
    "m": "regle",
    "cadre": "jaune",
    "inter": 46,
    "r": [
     "regle",
     "deux complexes égaux"
    ]
   },
   {
    "t": "(x − 2) + (y + 1)i = 5 − 3i     (x, y réels)",
    "c": "blanc",
    "m": "enonce"
   },
   {
    "t": "Parties réelles : x − 2 = 5",
    "c": "vert",
    "m": "reelles",
    "dx": 30,
    "r": [
     "reelles",
     "les parties réelles"
    ]
   },
   {
    "t": "Parties imaginaires : y + 1 = −3",
    "c": "orange",
    "m": "imaginaires",
    "dx": 30,
    "r": [
     "imaginaires",
     "les parties imaginaires"
    ]
   },
   {
    "t": "Donc x = 7 et y = −4.",
    "c": "jaune",
    "m": "solution",
    "r": [
     "solution",
     "la solution"
    ]
   },
   {
    "t": "Vérification : (7 − 2) + (−4 + 1)i = 5 − 3i : juste",
    "c": "cyan",
    "m": "verification",
    "r": [
     "verification",
     "on vérifie dans les deux équations"
    ]
   }
  ]
 },
 "c1": {
  "titre": "Somme et produit",
  "lignes": [
   {
    "t": "Somme : (3 + i) + (2 − i) = (3 + 2) + (1 − 1)i = 5",
    "c": "cyan",
    "m": "somme",
    "r": [
     "somme",
     "la somme"
    ]
   },
   {
    "t": "Produit : (3 + i)(2 − i) = 6 − 3i + 2i − i²",
    "c": "blanc",
    "m": "developpe",
    "r": [
     "developpe",
     "on développe"
    ]
   },
   {
    "t": "i² = −1 :  = 6 − i − (−1)",
    "c": "orange",
    "m": "remplace",
    "dx": 90,
    "r": [
     "remplace",
     "i² remplacé par −1"
    ]
   },
   {
    "t": "= 6 − i + 1",
    "c": "blanc",
    "m": "regroupe",
    "dx": 150
   },
   {
    "t": "= 7 − i",
    "c": "jaune",
    "m": "resultat",
    "dx": 150,
    "cadre": "jaune",
    "r": [
     "resultat",
     "le résultat"
    ]
   },
   {
    "t": "Re = 7 ; Im = −1",
    "c": "vert",
    "m": "lecture",
    "dx": 150
   }
  ]
 },
 "c2": {
  "titre": "Le carré, puis la puissance",
  "lignes": [
   {
    "t": "(1 + i)² = 1² + 2 × 1 × i + i²",
    "c": "blanc",
    "m": "identite",
    "r": [
     "identite",
     "l'identité remarquable"
    ]
   },
   {
    "t": "= 1 + 2i − 1",
    "c": "orange",
    "m": "remplace",
    "dx": 90
   },
   {
    "t": "(1 + i)² = 2i",
    "c": "jaune",
    "m": "carre",
    "cadre": "jaune",
    "inter": 46,
    "r": [
     "carre",
     "(1 + i)² = 2i"
    ]
   },
   {
    "t": "(1 − i)² = 1 − 2i + i² = −2i",
    "c": "cyan",
    "m": "moins",
    "r": [
     "moins",
     "(1 − i)² = −2i"
    ]
   },
   {
    "t": "(1 + i)⁴ = ((1 + i)²)² = (2i)² = 4i² = −4",
    "c": "vert",
    "m": "puissance",
    "r": [
     "puissance",
     "on passe par le carré"
    ]
   }
  ]
 },
 "c3": {
  "titre": "Un complexe fois son conjugué",
  "lignes": [
   {
    "t": "(2 + i)(2 − i) = 4 − 2i + 2i − i²",
    "c": "blanc",
    "m": "developpe",
    "r": [
     "developpe",
     "on développe"
    ]
   },
   {
    "t": "les termes en i s’annulent : −2i + 2i = 0",
    "c": "orange",
    "m": "annule",
    "dx": 30,
    "r": [
     "annule",
     "les termes en i s’annulent"
    ]
   },
   {
    "t": "= 4 − (−1) = 4 + 1 = 5 : un réel",
    "c": "jaune",
    "m": "reel",
    "dx": 30,
    "r": [
     "reel",
     "un réel"
    ]
   },
   {
    "t": "(a + ib)(a − ib) = a² + b²",
    "c": "jaune",
    "m": "formule",
    "cadre": "jaune",
    "inter": 46,
    "r": [
     "formule",
     "la formule"
    ]
   },
   {
    "t": "a − ib : le conjugué de a + ib",
    "c": "cyan",
    "m": "conjugue"
   },
   {
    "t": "a² − b²",
    "c": "rouge",
    "m": "piege",
    "barre": true,
    "r": [
     "piege",
     "a² − b² : faux"
    ]
   }
  ]
 },
 "c4": {
  "titre": "Le quotient : × le conjugué du bas",
  "lignes": [
   {
    "t": "(3 + i)/(1 + 2i) = (3 + i)(1 − 2i) / ((1 + 2i)(1 − 2i))",
    "c": "blanc",
    "m": "conjugue",
    "r": [
     "conjugue",
     "haut et bas × (1 − 2i)"
    ]
   },
   {
    "t": "en haut ET en bas : × (1 − 2i), le conjugué du bas",
    "c": "orange",
    "m": "pourquoi",
    "dx": 30
   },
   {
    "t": "= (3 − 6i + i − 2i²)/(1 + 4)",
    "c": "blanc",
    "m": "developpe",
    "dx": 60,
    "r": [
     "developpe",
     "on développe"
    ]
   },
   {
    "t": "= (5 − 5i)/5",
    "c": "blanc",
    "m": "reel",
    "dx": 60,
    "r": [
     "reel",
     "le bas est réel"
    ]
   },
   {
    "t": "= 5/5 − (5/5)i = 1 − i",
    "c": "jaune",
    "m": "separe",
    "dx": 60,
    "cadre": "jaune",
    "r": [
     "separe",
     "on sépare : 1 − i"
    ]
   },
   {
    "t": "Vérification : (1 − i)(1 + 2i) = 1 + 2i − i − 2i² = 3 + i",
    "c": "vert",
    "m": "verification",
    "r": [
     "verification",
     "on vérifie"
    ]
   }
  ]
 },
 "j2": {
  "titre": "Le conjugué d’un produit",
  "lignes": [
   {
    "t": "z = 2 + i ; z’ = 1 − 3i",
    "c": "cyan",
    "m": "donnees",
    "r": [
     "donnees",
     "les deux complexes"
    ]
   },
   {
    "t": "① zz’ = (2 + i)(1 − 3i) = 2 − 6i + i − 3i²",
    "c": "blanc",
    "m": "produit"
   },
   {
    "t": "= 2 + 3 − 5i = 5 − 5i ; son conjugué : 5 + 5i",
    "c": "jaune",
    "m": "conj_produit",
    "dx": 30,
    "r": [
     "conj_produit",
     "le conjugué du produit"
    ]
   },
   {
    "t": "② les conjugués : 2 − i et 1 + 3i",
    "c": "cyan",
    "m": "conjugues"
   },
   {
    "t": "(2 − i)(1 + 3i) = 2 + 6i − i − 3i² = 5 + 5i",
    "c": "jaune",
    "m": "produit_conj",
    "dx": 30,
    "r": [
     "produit_conj",
     "le produit des conjugués"
    ]
   },
   {
    "t": "Les deux calculs donnent 5 + 5i",
    "c": "vert",
    "m": "egal",
    "cadre": "vert",
    "r": [
     "egal",
     "le même résultat"
    ]
   },
   {
    "t": "conjugué d’un produit = produit des conjugués",
    "c": "orange",
    "m": "regle",
    "taille": 18,
    "r": [
     "regle",
     "la règle"
    ]
   }
  ]
 },
 "j4": {
  "titre": "Un complexe fois son conjugué",
  "lignes": [
   {
    "t": "(5 − 3i)(5 + 3i) = 25 + 15i − 15i − 9i²",
    "c": "blanc",
    "m": "exemple"
   },
   {
    "t": "= 25 + 9 = 34 : plus de i !",
    "c": "jaune",
    "m": "reel",
    "dx": 30
   },
   {
    "t": "(a + ib)(a − ib) = a² + b²   (réel positif)",
    "c": "vert",
    "m": "formule",
    "cadre": "vert",
    "r": [
     "formule",
     "la règle"
    ]
   },
   {
    "t": "(a + ib)(a − ib) = a² − b²",
    "c": "rouge",
    "m": "piege",
    "barre": true,
    "r": [
     "piege",
     "le piège du signe"
    ]
   },
   {
    "t": "2020 N : c = √2 + i√2 ; son conjugué : √2 − i√2",
    "c": "cyan",
    "m": "donnees_c"
   },
   {
    "t": "(√2 + i√2)(√2 − i√2) = (√2)² + (√2)² = 2 + 2 = 4",
    "c": "jaune",
    "m": "resultat",
    "cadre": "jaune",
    "r": [
     "resultat",
     "le résultat : 4"
    ]
   }
  ]
 },
 "m3": {
  "titre": "Le module d’un produit",
  "lignes": [
   {
    "t": "|zz’| = |z| × |z’| ; |z/z’| = |z|/|z’| ; |zⁿ| = |z|ⁿ",
    "c": "vert",
    "m": "regle",
    "cadre": "vert",
    "taille": 18,
    "r": [
     "regle",
     "le module d’un produit"
    ]
   },
   {
    "t": "2017 N : a = √3 + i",
    "c": "cyan",
    "m": "donnees"
   },
   {
    "t": "|a| = √((√3)² + 1²) = √4 = 2",
    "c": "blanc",
    "m": "module_a"
   },
   {
    "t": "|1 + i| = √(1 + 1) = √2",
    "c": "blanc",
    "m": "module_1i"
   },
   {
    "t": "|(1 + i)a| = |1 + i| × |a| = √2 × 2 = 2√2",
    "c": "jaune",
    "m": "produit",
    "cadre": "jaune",
    "r": [
     "produit",
     "on multiplie les modules"
    ]
   },
   {
    "t": "|1 + (−1)| = 0, mais |1| + |−1| = 2",
    "c": "orange",
    "m": "piege"
   },
   {
    "t": "|z + z’| = |z| + |z’|",
    "c": "rouge",
    "m": "piege_barre",
    "barre": true,
    "r": [
     "piege",
     "la somme : le piège"
    ]
   }
  ]
 },
 "t2": {
  "titre": "2023 N : a = √2 + i√2 sous forme trigonométrique",
  "lignes": [
   {
    "t": "a = √2 + i√2",
    "c": "cyan",
    "m": "donnee",
    "taille": 20,
    "inter": 46
   },
   {
    "t": "|a| = √((√2)² + (√2)²) = √4 = 2",
    "c": "blanc",
    "m": "module",
    "taille": 20,
    "inter": 48,
    "r": [
     "module",
     "le module de a"
    ]
   },
   {
    "t": "a = 2(√2/2 + (√2/2)i)",
    "c": "blanc",
    "m": "facteur",
    "taille": 20,
    "inter": 48,
    "r": [
     "facteur",
     "2 en facteur"
    ]
   },
   {
    "t": "= 2(cos π/4 + i sin π/4)",
    "c": "jaune",
    "m": "forme",
    "taille": 20,
    "inter": 48,
    "dx": 30,
    "cadre": "jaune",
    "r": [
     "forme",
     "la forme trigonométrique"
    ]
   },
   {
    "t": "Donc arg a ≡ π/4 [2π]",
    "c": "vert",
    "m": "argument",
    "taille": 20,
    "inter": 48,
    "r": [
     "argument",
     "la conclusion sur l'argument"
    ]
   },
   {
    "t": "Au national : la forme complète r(cos θ + i sin θ), sans abréviation",
    "c": "orange",
    "m": "complete",
    "taille": 18,
    "inter": 48,
    "r": [
     "complete",
     "la forme complète"
    ]
   }
  ]
 },
 "t6": {
  "titre": "2024 N : a = √3(1 − i)",
  "lignes": [
   {
    "t": "a = √3(1 − i)",
    "c": "cyan",
    "m": "donnee",
    "taille": 20,
    "inter": 46
   },
   {
    "t": "|λz| = |λ| × |z|, avec λ = √3 réel positif",
    "c": "orange",
    "m": "regle",
    "taille": 19,
    "inter": 46,
    "r": [
     "regle",
     "le module d'un produit"
    ]
   },
   {
    "t": "|a| = √3 × |1 − i| = √3 × √2 = √6",
    "c": "blanc",
    "m": "module",
    "taille": 20,
    "inter": 48,
    "r": [
     "module",
     "le module de a"
    ]
   },
   {
    "t": "a = √6(√2/2 − (√2/2)i)",
    "c": "blanc",
    "m": "facteur",
    "taille": 20,
    "inter": 48,
    "r": [
     "facteur",
     "√6 en facteur"
    ]
   },
   {
    "t": "= √6(cos(−π/4) + i sin(−π/4))",
    "c": "jaune",
    "m": "forme",
    "taille": 20,
    "inter": 48,
    "dx": 30,
    "cadre": "jaune",
    "r": [
     "forme",
     "quatrième quart : −π/4"
    ]
   },
   {
    "t": "Donc arg a ≡ −π/4 [2π]",
    "c": "vert",
    "m": "argument",
    "taille": 20,
    "inter": 48,
    "r": [
     "argument",
     "la conclusion sur l'argument"
    ]
   }
  ]
 },
 "r5": {
  "titre": "cos 5π/12 : deux écritures de b",
  "lignes": [
   {
    "t": "b = (1 + i)(√3 + i) = √3 + i + i√3 + i²",
    "c": "blanc",
    "m": "developpe",
    "taille": 18
   },
   {
    "t": "= (√3 − 1) + (√3 + 1)i",
    "c": "jaune",
    "m": "algebrique",
    "dx": 30,
    "taille": 18,
    "r": [
     "algebrique",
     "la forme algébrique de b"
    ]
   },
   {
    "t": "b = 2√2(cos 5π/12 + i sin 5π/12)",
    "c": "cyan",
    "m": "trigo",
    "taille": 18,
    "r": [
     "trigo",
     "la forme trigonométrique de b"
    ]
   },
   {
    "t": "Parties réelles : 2√2 cos 5π/12 = √3 − 1",
    "c": "vert",
    "m": "identifie",
    "taille": 18,
    "r": [
     "identifie",
     "on égale les parties réelles"
    ]
   },
   {
    "t": "cos 5π/12 = (√3 − 1)/(2√2) = (√3 − 1)√2/4",
    "c": "blanc",
    "m": "isole",
    "taille": 18
   },
   {
    "t": "cos 5π/12 = (√6 − √2)/4",
    "c": "jaune",
    "m": "resultat",
    "taille": 18,
    "cadre": "jaune",
    "r": [
     "resultat",
     "le résultat"
    ]
   }
  ]
 },
 "r8": {
  "titre": "2023 R : a²⁰²² est un réel",
  "lignes": [
   {
    "t": "a = √3/2 + (3/2)i",
    "c": "blanc",
    "m": "enonce",
    "taille": 18
   },
   {
    "t": "|a| = √(3/4 + 9/4) = √3",
    "c": "cyan",
    "m": "module",
    "taille": 18,
    "r": [
     "module",
     "le module de a"
    ]
   },
   {
    "t": "a = √3(1/2 + (√3/2)i) = √3(cos π/3 + i sin π/3)",
    "c": "cyan",
    "m": "forme",
    "taille": 18,
    "r": [
     "forme",
     "la forme trigonométrique"
    ]
   },
   {
    "t": "a²⁰²² = (√3)²⁰²²(cos 2022π/3 + i sin 2022π/3)",
    "c": "blanc",
    "m": "moivre",
    "taille": 18,
    "r": [
     "moivre",
     "la formule de Moivre"
    ]
   },
   {
    "t": "⚠ le module aussi : (√3)²⁰²² = 3¹⁰¹¹",
    "c": "rouge",
    "m": "piege",
    "taille": 18,
    "cadre": "rouge",
    "r": [
     "piege",
     "le module aussi est élevé à la puissance"
    ]
   },
   {
    "t": "2022π/3 = 674π = 337 × 2π : cos 674π = 1 ; sin 674π = 0",
    "c": "orange",
    "m": "angle",
    "taille": 18
   },
   {
    "t": "a²⁰²² = 3¹⁰¹¹(cos 674π + i sin 674π) = 3¹⁰¹¹ : un réel",
    "c": "jaune",
    "m": "resultat",
    "taille": 18,
    "cadre": "jaune",
    "r": [
     "resultat",
     "le résultat"
    ]
   }
  ]
 },
 "n1": {
  "titre": "2023 N : la partie 1, question par question",
  "lignes": [
   {
    "t": "a = √2 + i√2 ; b = 1 + √2 + i ; c = conjugué de b ; d = 2i",
    "c": "blanc",
    "m": "donnees",
    "taille": 18
   },
   {
    "t": "1) a = 2(cos π/4 + i sin π/4)",
    "c": "cyan",
    "m": "q1",
    "taille": 18,
    "r": [
     "q1",
     "la forme trigonométrique de a"
    ]
   },
   {
    "t": "2) b − d = 1 + √2 + i − 2i = 1 + √2 − i = c",
    "c": "jaune",
    "m": "q2",
    "taille": 18,
    "r": [
     "q2",
     "b − d = c"
    ]
   },
   {
    "t": "3) (√2 + 1)(b − a) = b − d, donc (b − d)/(b − a) = √2 + 1 ∈ ℝ",
    "c": "vert",
    "m": "q3",
    "taille": 18,
    "r": [
     "q3",
     "un quotient réel"
    ]
   },
   {
    "t": "donc A, B et D sont alignés",
    "c": "vert",
    "m": "alignes",
    "dx": 30,
    "taille": 18
   },
   {
    "t": "4) ac = 2b : arg a + arg c ≡ arg 2 + arg b [2π]",
    "c": "cyan",
    "m": "q4",
    "taille": 18,
    "r": [
     "q4",
     "on passe aux arguments"
    ]
   },
   {
    "t": "π/4 − arg b ≡ arg b, donc 2 arg b ≡ π/4 [2π]",
    "c": "jaune",
    "m": "conclusion",
    "dx": 30,
    "taille": 18,
    "cadre": "jaune",
    "r": [
     "conclusion",
     "2 arg b ≡ π/4 [2π]"
    ]
   },
   {
    "t": "la question suivante (rotation) : partie 2",
    "c": "orange",
    "m": "partie2",
    "taille": 18
   }
  ]
 }
};
