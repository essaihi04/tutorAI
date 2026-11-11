/* Écrit par le build du cours math_ch1_limites_continuite (maths_build/limites_continuite/build.py) : ne pas éditer à la main. */
window.CALCULS = {
 "o2_bases": {
  "titre": "Trois gestes de base",
  "lignes": [
   {
    "couleur": "cyan",
    "moment": "factoriser",
    "souligne": [
     "(x − 3)(x + 3)"
    ],
    "t": "① x² − 9 = (x − 3)(x + 3)"
   },
   {
    "couleur": "faible",
    "taille": 16,
    "t": "    car a² − b² = (a − b)(a + b)"
   },
   {
    "couleur": "vert",
    "moment": "signe",
    "t": "② x un peu plus grand que 1 : x − 1 > 0, petit"
   },
   {
    "couleur": "faible",
    "taille": 16,
    "t": "    x = 1,01 → x − 1 = 0,01"
   },
   {
    "couleur": "jaune",
    "moment": "variation",
    "t": "③ f’(x) = 3x² + 1 > 0"
   },
   {
    "couleur": "jaune",
    "cadre": "jaune",
    "t": "    donc f est strictement croissante"
   }
  ]
 },
 "l2_remplacer": {
  "titre": "Je remplace d'abord",
  "lignes": [
   {
    "couleur": "jaune",
    "moment": "remplace",
    "cadre": "jaune",
    "t": "Je remplace x par a :"
   },
   {
    "couleur": "vert",
    "dx": 20,
    "moment": "determinee",
    "t": "→ un nombre : c'est le résultat."
   },
   {
    "couleur": "orange",
    "dx": 20,
    "moment": "indeterminee",
    "t": "→ « 0/0 », « ∞/∞ », « +∞ − ∞ », « 0 × ∞ » :"
   },
   {
    "couleur": "orange",
    "dx": 44,
    "t": "forme indéterminée → je transforme l'écriture."
   },
   {
    "lim": "x → 1",
    "couleur": "cyan",
    "moment": "exemple",
    "pause": 0.4,
    "entoure": [
     "5"
    ],
    "t": "(x² + 3x + 1) = 1 + 3 + 1 = 5"
   }
  ]
 },
 "l4_formes": {
  "titre": "Les quatre formes indéterminées",
  "lignes": [
   {
    "couleur": "orange",
    "moment": "quatre",
    "t": "Formes indéterminées :"
   },
   {
    "couleur": "orange",
    "taille": 22,
    "dx": 20,
    "entoure": [
     "0/0",
     "∞/∞",
     "+∞ − ∞",
     "0 × ∞"
    ],
    "t": "0/0     ∞/∞     +∞ − ∞     0 × ∞"
   },
   {
    "couleur": "vert",
    "moment": "determinees",
    "pause": 0.4,
    "t": "Pas indéterminées :"
   },
   {
    "couleur": "vert",
    "dx": 20,
    "t": "+∞ + ∞ → +∞"
   },
   {
    "couleur": "vert",
    "dx": 20,
    "moment": "produit",
    "souligne": [
     "(+∞) × (−∞) → −∞"
    ],
    "t": "(+∞) × (−∞) → −∞   (règle des signes)"
   },
   {
    "couleur": "vert",
    "dx": 20,
    "t": "k/∞ → 0"
   },
   {
    "couleur": "jaune",
    "dx": 20,
    "moment": "k_sur_zero",
    "t": "k/0 (k ≠ 0) : infini, signe à droite et à gauche"
   }
  ]
 },
 "l5_facteur": {
  "titre": "Le facteur (x − 3)",
  "lignes": [
   {
    "lim": "x → 3",
    "frac": [
     "x² − 9",
     "x² − 4x + 3"
    ],
    "apres": "« 0/0 »",
    "couleur": "blanc",
    "entoure": [
     "« 0/0 »"
    ],
    "moment": "zero_zero"
   },
   {
    "lim": "x → 3",
    "frac": [
     "(x − 3)(x + 3)",
     "(x − 3)(x − 1)"
    ],
    "couleur": "cyan",
    "moment": "factorise",
    "t": "="
   },
   {
    "couleur": "cyan",
    "barre": [
     "(x − 3)"
    ],
    "inter": 4
   },
   {
    "lim": "x → 3",
    "frac": [
     "x + 3",
     "x − 1"
    ],
    "apres": "= 6/2 = 3",
    "couleur": "vert",
    "cadre": "vert",
    "moment": "resultat",
    "t": "="
   }
  ]
 },
 "l6_conjugue": {
  "titre": "L'expression conjuguée",
  "lignes": [
   {
    "lim": "x → 1",
    "frac": [
     "√(x + 3) − 2",
     "x − 1"
    ],
    "apres": "« 0/0 »",
    "entoure": [
     "« 0/0 »"
    ],
    "moment": "zero_zero"
   },
   {
    "lim": "x → 1",
    "frac": [
     "(√(x + 3) − 2)(√(x + 3) + 2)",
     "(x − 1)(√(x + 3) + 2)"
    ],
    "couleur": "cyan",
    "moment": "conjugue",
    "souligne": [
     "(√(x + 3) + 2)"
    ],
    "t": "="
   },
   {
    "couleur": "orange",
    "taille": 16,
    "dx": 360,
    "inter": 4,
    "moment": "identite",
    "t": "(a − b)(a + b) = a² − b²"
   },
   {
    "lim": "x → 1",
    "frac": [
     "x + 3 − 4",
     "(x − 1)(√(x + 3) + 2)"
    ],
    "apres": "",
    "couleur": "blanc",
    "moment": "racine_partie",
    "t": "="
   },
   {
    "lim": "x → 1",
    "frac": [
     "1",
     "√(x + 3) + 2"
    ],
    "apres": "= 1/4",
    "couleur": "vert",
    "cadre": "vert",
    "moment": "resultat",
    "t": "="
   }
  ]
 },
 "l7_lourd": {
  "titre": "Le terme de plus haut degré",
  "lignes": [
   {
    "lim": "x → +∞",
    "frac": [
     "3x² + 1",
     "x² − x"
    ],
    "apres": "« ∞/∞ »",
    "entoure": [
     "« ∞/∞ »"
    ],
    "moment": "infini_infini"
   },
   {
    "lim": "x → +∞",
    "frac": [
     "3x²",
     "x²"
    ],
    "couleur": "cyan",
    "moment": "lourds",
    "souligne": [
     "3x²",
     "x²"
    ],
    "t": "="
   },
   {
    "couleur": "vert",
    "cadre": "vert",
    "moment": "resultat",
    "dx": 40,
    "t": "= 3"
   },
   {
    "couleur": "orange",
    "taille": 17,
    "moment": "attention",
    "t": "⚠ seulement en ±∞ ; en un point, je remplace"
   }
  ]
 },
 "l12_sinus": {
  "titre": "sin(x)/x et le changement de variable",
  "lignes": [
   {
    "lim": "x → 0",
    "couleur": "jaune",
    "cadre": "jaune",
    "moment": "reference",
    "t": "sin(x)/x = 1"
   },
   {
    "lim": "x → 0",
    "frac": [
     "sin(3x)",
     "2x"
    ],
    "apres": "« 0/0 »",
    "entoure": [
     "« 0/0 »"
    ],
    "moment": "zero_zero",
    "pause": 0.3
   },
   {
    "lim": "x → 0",
    "frac": [
     "3",
     "2"
    ],
    "apres": "× sin(3x)/(3x)",
    "couleur": "cyan",
    "moment": "faire_apparaitre",
    "entoure": [
     "sin(3x)/(3x)"
    ],
    "t": "="
   },
   {
    "couleur": "orange",
    "moment": "pose_t",
    "t": "on pose t = 3x : x → 0 donc t → 0"
   },
   {
    "couleur": "orange",
    "dx": 40,
    "moment": "bloc_un",
    "t": "sin(t)/t → 1"
   },
   {
    "couleur": "vert",
    "cadre": "vert",
    "moment": "resultat",
    "t": "donc la limite vaut 3/2"
   }
  ]
 },
 "l13_devoir": {
  "titre": "Même dénominateur",
  "lignes": [
   {
    "lim": "x → 1",
    "apres": "  « +∞ − ∞ »",
    "entoure": [
     "« +∞ − ∞ »"
    ],
    "moment": "forme",
    "t": "1/(x − 1) − 2/(x² − 1)"
   },
   {
    "lim": "x → 1",
    "frac": [
     "x + 1 − 2",
     "(x − 1)(x + 1)"
    ],
    "couleur": "cyan",
    "moment": "meme_denominateur",
    "marge": "x² − 1 = (x − 1)(x + 1)",
    "t": "="
   },
   {
    "lim": "x → 1",
    "frac": [
     "x − 1",
     "(x − 1)(x + 1)"
    ],
    "couleur": "cyan",
    "barre": [
     "x − 1"
    ],
    "moment": "simplifie",
    "t": "="
   },
   {
    "lim": "x → 1",
    "frac": [
     "1",
     "x + 1"
    ],
    "apres": "= 1/2",
    "couleur": "vert",
    "cadre": "vert",
    "moment": "resultat",
    "t": "="
   }
  ]
 },
 "c5_redaction": {
  "titre": "Continuité en un point : la rédaction",
  "lignes": [
   {
    "couleur": "cyan",
    "taille": 17,
    "moment": "enonce",
    "t": "f(x) = √(x + 3) si x ≥ 1 ;  f(x) = x + 1 si x < 1"
   },
   {
    "couleur": "jaune",
    "moment": "image",
    "marge": "branche x ≥ 1",
    "t": "f(1) = √(1 + 3) = 2"
   },
   {
    "lim": "x → 1⁺",
    "couleur": "blanc",
    "moment": "droite",
    "t": "√(x + 3) = 2 = f(1)   ①"
   },
   {
    "lim": "x → 1⁻",
    "couleur": "blanc",
    "moment": "gauche",
    "t": "(x + 1) = 2 = f(1)   ②"
   },
   {
    "couleur": "vert",
    "cadre": "vert",
    "moment": "conclusion",
    "t": "D'après ① et ②, f est continue en 1."
   }
  ]
 },
 "t6_rediger": {
  "titre": "Solution unique : la rédaction du national",
  "lignes": [
   {
    "couleur": "cyan",
    "moment": "posons",
    "t": "Posons f(x) = x³ + x − 1."
   },
   {
    "moment": "continue",
    "t": "f est un polynôme, donc continue sur [0 ; 1]."
   },
   {
    "moment": "monotone",
    "t": "f’(x) = 3x² + 1 > 0, donc f est"
   },
   {
    "dx": 30,
    "t": "strictement croissante sur [0 ; 1]."
   },
   {
    "couleur": "jaune",
    "moment": "images",
    "t": "f(0) = −1 < 0 et f(1) = 1 > 0"
   },
   {
    "couleur": "jaune",
    "dx": 30,
    "t": "donc f(0) × f(1) < 0."
   },
   {
    "couleur": "vert",
    "taille": 17,
    "moment": "conclusion",
    "t": "Donc, d'après le théorème des valeurs intermédiaires,"
   },
   {
    "couleur": "vert",
    "taille": 17,
    "cadre": "vert",
    "t": "x³ + x − 1 = 0 admet une solution unique α dans ]0 ; 1[."
   }
  ],
  "tete": "Montrer que x³ + x − 1 = 0 a une solution unique dans ]0 ; 1["
 },
 "r4_existence": {
  "titre": "Réciproque : la rédaction du national",
  "lignes": [
   {
    "couleur": "cyan",
    "moment": "enonce",
    "t": "g(x) = x² − 2x − 1 sur I = [1 ; +∞["
   },
   {
    "moment": "continue",
    "t": "g est continue sur I (polynôme)."
   },
   {
    "taille": 17,
    "moment": "monotone",
    "t": "g’(x) = 2x − 2 ≥ 0 sur I : g est strictement croissante sur I."
   },
   {
    "couleur": "vert",
    "moment": "conclusion",
    "t": "Donc g admet une fonction réciproque g⁻¹"
   },
   {
    "couleur": "vert",
    "dx": 30,
    "t": "définie sur un intervalle J = g(I)."
   },
   {
    "couleur": "jaune",
    "cadre": "jaune",
    "moment": "J",
    "t": "J = [g(1) ; lim g[ = [−2 ; +∞["
   },
   {
    "couleur": "orange",
    "taille": 16,
    "moment": "attention",
    "t": "⚠ ni f(a) × f(b), ni théorème des valeurs intermédiaires"
   }
  ]
 },
 "r8_expression": {
  "titre": "L'expression de f⁻¹(x)",
  "lignes": [
   {
    "couleur": "cyan",
    "taille": 18,
    "moment": "enonce",
    "t": "f(x) = √(x − 1),  I = [1 ; +∞[,  J = [0 ; +∞["
   },
   {
    "couleur": "jaune",
    "cadre": "jaune",
    "moment": "pivot",
    "t": "Soit x ∈ J et y ∈ I :  f⁻¹(x) = y ⇔ f(y) = x"
   },
   {
    "dx": 20,
    "moment": "remplace",
    "t": "⇔ √(y − 1) = x"
   },
   {
    "dx": 20,
    "marge": "ai-je le droit ? x ≥ 0 ✓",
    "moment": "carre",
    "t": "⇔ y − 1 = x²"
   },
   {
    "dx": 20,
    "moment": "isole",
    "t": "⇔ y = x² + 1"
   },
   {
    "couleur": "vert",
    "cadre": "vert",
    "moment": "conclusion",
    "t": "Donc, pour tout x de J, f⁻¹(x) = x² + 1."
   }
  ]
 },
 "r9_valeur_absolue": {
  "titre": "Racine et valeur absolue",
  "lignes": [
   {
    "couleur": "cyan",
    "taille": 17,
    "moment": "enonce",
    "t": "f(x) = x² + 2x − 3,  I = ]−1 ; +∞[,  J = ]−4 ; +∞["
   },
   {
    "dx": 0,
    "moment": "pivot",
    "t": "f⁻¹(x) = y ⇔ y² + 2y − 3 = x"
   },
   {
    "dx": 20,
    "moment": "canonique",
    "souligne": [
     "(y + 1)²"
    ],
    "t": "⇔ (y + 1)² = x + 4"
   },
   {
    "dx": 20,
    "marge": "x + 4 > 0 car x ∈ J",
    "moment": "racine",
    "entoure": [
     "|y + 1|"
    ],
    "t": "⇔ |y + 1| = √(x + 4)"
   },
   {
    "dx": 20,
    "marge": "y ∈ I donc y + 1 > 0",
    "moment": "valeur_absolue",
    "t": "⇔ y + 1 = √(x + 4)"
   },
   {
    "couleur": "vert",
    "cadre": "vert",
    "moment": "conclusion",
    "t": "Donc, pour tout x de J, f⁻¹(x) = √(x + 4) − 1."
   }
  ]
 },
 "n3_regles": {
  "titre": "Les règles : √ et ⁿ√",
  "lignes": [
   {
    "couleur": "faible",
    "moment": "titres",
    "t": "avec √"
   },
   {
    "couleur": "cyan",
    "moment": "produit",
    "t": "√x × √y = √(xy)"
   },
   {
    "couleur": "cyan",
    "moment": "quotient",
    "t": "√x / √y = √(x/y)"
   },
   {
    "couleur": "cyan",
    "moment": "puissance",
    "t": "(√x)² = x"
   },
   {
    "couleur": "cyan",
    "moment": "emboitees",
    "t": "√(√x) = ⁴√x"
   },
   {
    "couleur": "faible",
    "col": 2,
    "t": "avec ⁿ√  (x ≥ 0, y > 0)"
   },
   {
    "couleur": "jaune",
    "col": 2,
    "t": "ⁿ√x × ⁿ√y = ⁿ√(xy)"
   },
   {
    "couleur": "jaune",
    "col": 2,
    "t": "ⁿ√x / ⁿ√y = ⁿ√(x/y)"
   },
   {
    "couleur": "jaune",
    "col": 2,
    "t": "(ⁿ√x)ⁿ = x"
   },
   {
    "couleur": "jaune",
    "col": 2,
    "moment": "exemple",
    "t": "ⁿ√(ᵐ√x) = ⁿᵐ√x"
   },
   {
    "couleur": "vert",
    "col": 2,
    "cadre": "vert",
    "moment": "resultat",
    "t": "∛5 × ∛7 = ∛35"
   }
  ]
 },
 "n4_simplifier": {
  "titre": "Simplifier B = (⁴√9 × √9)/⁸√81",
  "lignes": [
   {
    "couleur": "orange",
    "moment": "puissances",
    "entoure": [
     "3⁴"
    ],
    "t": "9 = 3²     81 = 9 × 9 = 3⁴"
   },
   {
    "couleur": "cyan",
    "moment": "reduire",
    "t": "⁴√9 = ⁴√(3²) = √3"
   },
   {
    "couleur": "cyan",
    "t": "√9 = 3"
   },
   {
    "couleur": "cyan",
    "moment": "reduire2",
    "t": "⁸√81 = ⁸√(3⁴) = √3"
   },
   {
    "frac": [
     "√3 × 3",
     "√3"
    ],
    "apres": "= 3",
    "couleur": "vert",
    "cadre": "vert",
    "moment": "resultat",
    "barre": [
     "√3"
    ],
    "t": "B ="
   }
  ]
 },
 "n5_comparer": {
  "titre": "Comparer ⁷√3 et ⁵√2",
  "lignes": [
   {
    "couleur": "orange",
    "moment": "indice",
    "t": "indice commun : 7 × 5 = 35"
   },
   {
    "couleur": "cyan",
    "moment": "premier",
    "t": "⁷√3 = ³⁵√(3⁵) = ³⁵√243"
   },
   {
    "couleur": "cyan",
    "moment": "second",
    "t": "⁵√2 = ³⁵√(2⁷) = ³⁵√128"
   },
   {
    "couleur": "vert",
    "cadre": "vert",
    "moment": "conclusion",
    "t": "243 > 128  donc  ⁷√3 > ⁵√2"
   }
  ]
 },
 "n7_equation": {
  "titre": "Résoudre ∛(2x³ + 11) = 3",
  "lignes": [
   {
    "couleur": "orange",
    "moment": "condition",
    "t": "condition : 2x³ + 11 ≥ 0"
   },
   {
    "moment": "puissance",
    "t": "∛(2x³ + 11) = 3 ⇔ 2x³ + 11 = 3³"
   },
   {
    "dx": 20,
    "moment": "resout",
    "t": "⇔ 2x³ = 16  ⇔  x³ = 8  ⇔  x = 2"
   },
   {
    "couleur": "vert",
    "taille": 17,
    "moment": "verifie",
    "t": "vérification : 2 × 8 + 11 = 27 ≥ 0, ∛27 = 3 ✓"
   },
   {
    "couleur": "vert",
    "cadre": "vert",
    "moment": "ensemble",
    "t": "S = {2}"
   }
  ]
 },
 "p1_exposant": {
  "titre": "x^(1/n) = ⁿ√x",
  "lignes": [
   {
    "couleur": "orange",
    "moment": "condition",
    "t": "x > 0"
   },
   {
    "couleur": "cyan",
    "moment": "pourquoi",
    "t": "(x^{1/2})² = x^{2/2} = x     et     (√x)² = x"
   },
   {
    "couleur": "jaune",
    "cadre": "jaune",
    "taille": 24,
    "moment": "definition",
    "t": "x^{1/n} = ⁿ√x"
   },
   {
    "couleur": "vert",
    "moment": "exemple",
    "t": "8^{1/3} = ∛8 = 2"
   },
   {
    "couleur": "orange",
    "moment": "attention",
    "t": "⚠ x^{1/n} ≠ 1/xⁿ"
   }
  ]
 },
 "p2_pq": {
  "titre": "x^(p/q) = racine q-ième de xᵖ",
  "lignes": [
   {
    "couleur": "jaune",
    "cadre": "jaune",
    "moment": "regle",
    "t": "x^{p/q} : q = l'indice,  p = l'exposant   (x > 0)"
   },
   {
    "couleur": "cyan",
    "moment": "premiere",
    "t": "8^{2/3} = ∛(8²) = ∛64 = 4"
   },
   {
    "couleur": "cyan",
    "moment": "seconde",
    "t": "8^{2/3} = (∛8)² = 2² = 4"
   },
   {
    "couleur": "vert",
    "cadre": "vert",
    "moment": "exemple",
    "t": "⁵√(x³) = x^{3/5}"
   }
  ]
 },
 "p3_regles": {
  "titre": "Les règles des puissances",
  "lignes": [
   {
    "couleur": "jaune",
    "moment": "regles",
    "t": "x^{r} × x^{s} = x^{r+s}     (x^{r})^{s} = x^{rs}"
   },
   {
    "couleur": "cyan",
    "moment": "enonce",
    "t": "A = ∛4 × 2^{1/3} × √2"
   },
   {
    "dx": 20,
    "moment": "exposants",
    "t": "= 2^{2/3} × 2^{1/3} × 2^{1/2}"
   },
   {
    "dx": 20,
    "moment": "somme",
    "t": "= 2^{2/3 + 1/3 + 1/2} = 2^{3/2}"
   },
   {
    "dx": 20,
    "couleur": "vert",
    "cadre": "vert",
    "moment": "resultat",
    "t": "= 2 × √2 = 2√2"
   }
  ]
 },
 "lr2_cle": {
  "titre": "La clé de 2 et la clé de 3",
  "lignes": [
   {
    "couleur": "cyan",
    "moment": "cle_deux",
    "t": "√ :  a² − b² = (a − b)(a + b)"
   },
   {
    "couleur": "jaune",
    "cadre": "jaune",
    "moment": "cle_trois",
    "t": "∛ :  a³ − b³ = (a − b)(a² + ab + b²)"
   },
   {
    "couleur": "blanc",
    "moment": "choix",
    "t": "a = ∛x,  b = 2 :"
   },
   {
    "couleur": "vert",
    "moment": "resultat",
    "souligne": [
     "(∛(x²) + 2∛x + 4)"
    ],
    "t": "(∛x − 2)(∛(x²) + 2∛x + 4) = x − 8"
   }
  ]
 },
 "lr3_cubique": {
  "titre": "0/0 avec une racine cubique",
  "lignes": [
   {
    "lim": "x → 0",
    "frac": [
     "∛(x + 8) − 2",
     "x"
    ],
    "apres": "« 0/0 »",
    "entoure": [
     "« 0/0 »"
    ],
    "moment": "zero_zero"
   },
   {
    "couleur": "orange",
    "taille": 17,
    "moment": "cle",
    "t": "a = ∛(x + 8), b = 2 = ∛8 :  a³ − b³ = x + 8 − 8 = x"
   },
   {
    "lim": "x → 0",
    "frac": [
     "x",
     "x(∛((x + 8)²) + 2∛(x + 8) + 4)"
    ],
    "couleur": "cyan",
    "barre": [
     "x"
    ],
    "moment": "simplifie",
    "t": "="
   },
   {
    "frac": [
     "1",
     "4 + 4 + 4"
    ],
    "apres": "= 1/12",
    "couleur": "vert",
    "cadre": "vert",
    "moment": "resultat",
    "t": "="
   }
  ]
 },
 "lr4_lourd": {
  "titre": "Le terme le plus lourd en facteur",
  "lignes": [
   {
    "lim": "x → +∞",
    "apres": "  « +∞ − ∞ »",
    "entoure": [
     "« +∞ − ∞ »"
    ],
    "moment": "forme",
    "t": "∛(x² − x) − x"
   },
   {
    "couleur": "orange",
    "moment": "poids",
    "souligne": [
     "x^{2/3}"
    ],
    "t": "∛(x² − x) ≈ x^{2/3}  <  x"
   },
   {
    "couleur": "cyan",
    "taille": 17,
    "moment": "facteur",
    "sous": [
     [
      "∛(1/x − 1/x²)",
      "→ 0"
     ]
    ],
    "t": "= x (∛(x² − x)/x − 1) = x (∛(1/x − 1/x²) − 1)"
   },
   {
    "couleur": "vert",
    "cadre": "vert",
    "moment": "resultat",
    "pause": 0.4,
    "t": "x → +∞  et  (…) → −1   donc la limite est −∞"
   }
  ]
 },
 "e1_probleme": {
  "titre": "f(x) = x³ + x − 1 : le problème",
  "lignes": [
   {
    "couleur": "cyan",
    "taille": 17,
    "moment": "limites",
    "t": "1) lim f = −∞ (−∞) ; lim f = +∞ (+∞)"
   },
   {
    "couleur": "cyan",
    "taille": 17,
    "moment": "variation",
    "t": "2) f’(x) = 3x² + 1 > 0 :"
   },
   {
    "taille": 17,
    "dx": 20,
    "t": "f strictement croissante sur ℝ"
   },
   {
    "couleur": "cyan",
    "taille": 17,
    "moment": "unique",
    "t": "3) f(ℝ) = ℝ, 0 ∈ f(ℝ) :"
   },
   {
    "taille": 17,
    "dx": 20,
    "t": "solution unique α"
   },
   {
    "col": 2,
    "taille": 17,
    "moment": "encadrement",
    "t": "f(1/2) = −3/8 < 0 ; f(1) = 1 > 0"
   },
   {
    "col": 2,
    "taille": 17,
    "dx": 20,
    "couleur": "jaune",
    "t": "donc 1/2 < α < 1"
   },
   {
    "col": 2,
    "couleur": "cyan",
    "taille": 17,
    "moment": "dichotomie",
    "t": "4) f(3/4) = 11/64 > 0"
   },
   {
    "col": 2,
    "taille": 17,
    "dx": 20,
    "couleur": "jaune",
    "t": "donc 1/2 < α < 3/4"
   },
   {
    "col": 2,
    "couleur": "cyan",
    "taille": 17,
    "moment": "reciproque",
    "t": "5) continue et strictement croissante :"
   },
   {
    "col": 2,
    "taille": 17,
    "dx": 20,
    "couleur": "vert",
    "cadre": "vert",
    "t": "réciproque f⁻¹ définie sur J = ℝ"
   }
  ]
 }
};
