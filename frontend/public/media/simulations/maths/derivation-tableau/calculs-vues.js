/* Écrit par maths_build/derivation_etude_fonctions/build.py depuis les p*.py du cours math_ch2_derivation_etude_fonctions : ne pas modifier à la main. */
window.CALCULS = {
 "carte": {
  "titre": "Cinq questions sur une courbe",
  "lignes": [
   {
    "t": "Une courbe (C_f) : que veut-on savoir ?",
    "c": "jaune",
    "m": "courbe",
    "taille": 20,
    "inter": 44
   },
   {
    "t": "① Où penche-t-elle ?  →  la tangente : limite du taux, f′(x_0)",
    "c": "cyan",
    "m": "tangente",
    "r": [
     "q_tangente",
     "la tangente"
    ]
   },
   {
    "t": "② Monte-t-elle ?  →  le signe de f′",
    "c": "cyan",
    "m": "variations",
    "r": [
     "q_variations",
     "le signe de f′"
    ]
   },
   {
    "t": "③ De quel côté est-elle creuse ?  →  le signe de f″",
    "c": "cyan",
    "m": "concavite",
    "r": [
     "q_concavite",
     "le signe de f″"
    ]
   },
   {
    "t": "④ Où part-elle au bout ?  →  les limites : branches infinies",
    "c": "cyan",
    "m": "branches",
    "r": [
     "q_branches",
     "les branches infinies"
    ]
   },
   {
    "t": "⑤ Se répète-t-elle ?  →  axe ou centre de symétrie",
    "c": "cyan",
    "m": "symetrie",
    "r": [
     "q_symetrie",
     "la symétrie"
    ]
   },
   {
    "t": "Tout finit dans le tracé : 8 à 11 points sur 20 au national",
    "c": "orange",
    "m": "trace",
    "inter": 30
   }
  ]
 },
 "bases": {
  "titre": "Trois gestes à avoir en main",
  "lignes": [
   {
    "t": "① (3x² − 5x)′ = 3 × 2x − 5 = 6x − 5",
    "c": "cyan",
    "m": "deriver",
    "r": [
     "deriver",
     "dériver un polynôme"
    ]
   },
   {
    "t": "② signe de (x − 1)(x + 1) :",
    "c": "cyan",
    "m": "signe_titre"
   },
   {
    "t": "",
    "tab": {
     "cols": [
      "−∞",
      "−1",
      "1",
      "+∞"
     ],
     "rows": [
      {
       "nom": "x + 1",
       "cells": [
        [
         0.5,
         "−"
        ],
        [
         1,
         "0"
        ],
        [
         1.5,
         "+"
        ],
        [
         2.5,
         "+"
        ]
       ]
      },
      {
       "nom": "x − 1",
       "cells": [
        [
         0.5,
         "−"
        ],
        [
         1.5,
         "−"
        ],
        [
         2,
         "0"
        ],
        [
         2.5,
         "+"
        ]
       ]
      },
      {
       "nom": "produit",
       "cells": [
        [
         0.5,
         "+",
         "vert"
        ],
        [
         1,
         "0"
        ],
        [
         1.5,
         "−",
         "rouge"
        ],
        [
         2,
         "0"
        ],
        [
         2.5,
         "+",
         "vert"
        ]
       ],
       "m": "signe",
       "r": [
        "signe",
        "le signe du produit"
       ]
      }
     ],
     "w": 520,
     "nomW": 96
    }
   },
   {
    "t": "③ lim 1/x = +∞ quand x → 0⁺   (1 > 0 et x → 0⁺)",
    "c": "cyan",
    "m": "limite",
    "r": [
     "limite",
     "une limite à droite"
    ]
   }
  ]
 },
 "nd4": {
  "titre": "Montrer que f est dérivable en un point",
  "lignes": [
   {
    "t": "f(x) = x² en 1 :   f(1) = 1",
    "c": "jaune",
    "m": "f_x0",
    "r": [
     "f_x0",
     "f(x₀) calculé à part"
    ]
   },
   {
    "t": "lim_{x→1} (x² − 1)/(x − 1)  :  forme « 0/0 »",
    "c": "cyan",
    "m": "forme",
    "r": [
     "forme",
     "la forme indéterminée nommée"
    ]
   },
   {
    "t": "= lim_{x→1} (x − 1)(x + 1)/(x − 1) = lim_{x→1} (x + 1) = 2 ∈ ℝ",
    "c": "cyan",
    "m": "factorise"
   },
   {
    "t": "donc f est dérivable en 1 et f′(1) = 2",
    "c": "vert",
    "m": "conclusion1",
    "cadre": "vert",
    "inter": 44
   },
   {
    "t": "g(x) = √(x + 1) en 3 :   g(3) = 2",
    "c": "jaune",
    "m": "g_x0"
   },
   {
    "t": "lim_{x→3} (√(x + 1) − 2)/(x − 3) = lim (x + 1 − 4)/((x − 3)(√(x + 1) + 2))",
    "c": "cyan",
    "m": "conjugue",
    "taille": 17,
    "r": [
     "conjugue",
     "le conjugué, en haut et en bas"
    ]
   },
   {
    "t": "= lim_{x→3} 1/(√(x + 1) + 2) = 1/4 ∈ ℝ :  g est dérivable en 3, g′(3) = 1/4",
    "c": "vert",
    "m": "conclusion2",
    "taille": 17
   }
  ]
 },
 "tg2": {
  "titre": "Écrire la tangente en 2 à la courbe de x + 1/x",
  "lignes": [
   {
    "t": "f(x) = x + 1/x,  x_0 = 2",
    "c": "jaune",
    "m": "enonce"
   },
   {
    "t": "f(2) = 2 + 1/2 = 5/2",
    "c": "cyan",
    "m": "f2",
    "r": [
     "f2",
     "f(x₀)"
    ]
   },
   {
    "t": "f′(x) = 1 − 1/x²,  f′(2) = 1 − 1/4 = 3/4",
    "c": "cyan",
    "m": "fp2",
    "r": [
     "fp2",
     "f′(x₀)"
    ]
   },
   {
    "t": "(T) : y = f′(2)(x − 2) + f(2)",
    "c": "blanc",
    "m": "formule"
   },
   {
    "t": "y = (3/4)(x − 2) + 5/2 = (3/4)x − 3/2 + 5/2",
    "c": "blanc",
    "m": "remplace"
   },
   {
    "t": "(T) : y = (3/4)x + 1",
    "c": "vert",
    "m": "resultat",
    "cadre": "vert",
    "r": [
     "resultat",
     "l’équation de la tangente"
    ]
   }
  ]
 },
 "dt6": {
  "titre": "Deux morceaux, deux côtés (type national 2021)",
  "lignes": [
   {
    "t": "f(x) = x√x − 2x si x > 0 ;  f(x) = x³ + 3x si x ≤ 0 ;  f(0) = 0",
    "c": "jaune",
    "m": "enonce",
    "taille": 17
   },
   {
    "t": "à droite : lim_{x→0⁺} (x√x − 2x)/x = lim_{x→0⁺} (√x − 2) = −2 ∈ ℝ",
    "c": "cyan",
    "m": "droite",
    "taille": 17,
    "r": [
     "droite",
     "à droite : la ligne x > 0"
    ]
   },
   {
    "t": "f est dérivable à droite en 0, f_d′(0) = −2 : demi-tangente à droite de pente −2",
    "c": "blanc",
    "m": "phrase_droite",
    "taille": 16
   },
   {
    "t": "à gauche : lim_{x→0⁻} (x³ + 3x)/x = lim_{x→0⁻} (x² + 3) = 3 ∈ ℝ",
    "c": "cyan",
    "m": "gauche",
    "taille": 17,
    "r": [
     "gauche",
     "à gauche : la ligne x ≤ 0"
    ]
   },
   {
    "t": "f est dérivable à gauche en 0, f_g′(0) = 3 : demi-tangente à gauche de pente 3",
    "c": "blanc",
    "m": "phrase_gauche",
    "taille": 16
   },
   {
    "t": "f_d′(0) ≠ f_g′(0) : f n'est pas dérivable en 0 ; O est un point anguleux",
    "c": "vert",
    "m": "conclusion",
    "taille": 17,
    "cadre": "vert"
   }
  ]
 },
 "dv1": {
  "titre": "Le tableau des dérivées",
  "lignes": [
   {
    "t": "f(x)            f′(x)",
    "c": "jaune",
    "m": "entete",
    "taille": 20,
    "inter": 36
   },
   {
    "t": "k (constante)   →   0",
    "c": "cyan",
    "m": "constante"
   },
   {
    "t": "x   →   1",
    "c": "cyan",
    "m": "x"
   },
   {
    "t": "xⁿ   →   n·xⁿ⁻¹",
    "c": "cyan",
    "m": "puissance",
    "cadre": "cyan",
    "r": [
     "puissance",
     "xⁿ → n·xⁿ⁻¹"
    ]
   },
   {
    "t": "1/x   →   −1/x²",
    "c": "cyan",
    "m": "inverse",
    "r": [
     "inverse",
     "1/x → −1/x²"
    ]
   },
   {
    "t": "√x   →   1/(2√x)   (x > 0)",
    "c": "cyan",
    "m": "racine"
   },
   {
    "t": "(u + v)′ = u′ + v′ ;   (k·u)′ = k·u′",
    "c": "orange",
    "m": "somme"
   }
  ]
 },
 "dv2": {
  "titre": "Produit et quotient",
  "lignes": [
   {
    "t": "(u·v)′ = u′v + uv′",
    "c": "cyan",
    "m": "produit",
    "cadre": "cyan",
    "r": [
     "produit",
     "le produit"
    ]
   },
   {
    "t": "(u/v)′ = (u′v − uv′) / v²",
    "c": "cyan",
    "m": "quotient",
    "cadre": "cyan",
    "r": [
     "quotient",
     "le quotient : un moins"
    ]
   },
   {
    "t": "f(x) = (2x + 1)/(x − 3) :  u = 2x + 1, u′ = 2 ;  v = x − 3, v′ = 1",
    "c": "blanc",
    "m": "uv",
    "taille": 17
   },
   {
    "t": "f′(x) = (2(x − 3) − (2x + 1) × 1) / (x − 3)²",
    "c": "blanc",
    "m": "remplace",
    "taille": 18,
    "r": [
     "parentheses",
     "une parenthèse autour de chaque produit"
    ]
   },
   {
    "t": "= (2x − 6 − 2x − 1) / (x − 3)² = −7/(x − 3)²",
    "c": "vert",
    "m": "resultat",
    "cadre": "vert"
   },
   {
    "t": "le dénominateur reste factorisé : on ne développe pas (x − 3)²",
    "c": "orange",
    "m": "piege",
    "taille": 16
   }
  ]
 },
 "dv3": {
  "titre": "La puissance d'une expression",
  "lignes": [
   {
    "t": "f(x) = (x² − 2x + 3)³",
    "c": "jaune",
    "m": "enonce",
    "taille": 21
   },
   {
    "t": "u = x² − 2x + 3",
    "c": "cyan",
    "m": "u",
    "cadre": "cyan",
    "r": [
     "u",
     "on nomme u"
    ]
   },
   {
    "t": "u′ = 2x − 2",
    "c": "cyan",
    "m": "u_prime",
    "dx": 40,
    "r": [
     "u_prime",
     "u′ dans la marge"
    ]
   },
   {
    "t": "(uⁿ)′ = n · u′ · uⁿ⁻¹",
    "c": "orange",
    "m": "gabarit",
    "cadre": "orange"
   },
   {
    "t": "f′(x) = 3 · (2x − 2) · (x² − 2x + 3)²",
    "c": "vert",
    "m": "rempli",
    "r": [
     "rempli",
     "les trois cases remplies"
    ]
   },
   {
    "t": "(u³)′ = 3u²  : u′ oublié",
    "c": "rouge",
    "m": "faux",
    "barre": true,
    "taille": 17
   }
  ]
 },
 "dv4": {
  "titre": "La racine d'une expression",
  "lignes": [
   {
    "t": "(√u)′ = u′ / (2√u)",
    "c": "orange",
    "m": "gabarit",
    "cadre": "orange",
    "r": [
     "gabarit",
     "u′ en haut"
    ]
   },
   {
    "t": "f(x) = √(x² + 1)",
    "c": "jaune",
    "m": "enonce"
   },
   {
    "t": "u = x² + 1 ;  u′ = 2x",
    "c": "cyan",
    "m": "u"
   },
   {
    "t": "f′(x) = 2x / (2√(x² + 1)) = x / √(x² + 1)",
    "c": "vert",
    "m": "resultat",
    "cadre": "vert"
   },
   {
    "t": "(√u)′ = 1/(2√u)  : u′ oublié",
    "c": "rouge",
    "m": "faux",
    "barre": true,
    "taille": 17
   }
  ]
 },
 "dv5": {
  "titre": "La racine n-ième et la composée",
  "lignes": [
   {
    "t": "(ⁿ√u)′ = u′ / (n · (ⁿ√u)ⁿ⁻¹)   (u > 0)",
    "c": "orange",
    "m": "gabarit",
    "cadre": "orange",
    "r": [
     "gabarit",
     "la racine n-ième"
    ]
   },
   {
    "t": "(³√x)′ = 1 / (3 (³√x)²)   (x > 0)",
    "c": "cyan",
    "m": "exemple",
    "r": [
     "exemple",
     "n = 3, u = x"
    ]
   },
   {
    "t": "(f∘g)′(x) = g′(x) · f′(g(x))",
    "c": "cyan",
    "m": "composee",
    "cadre": "cyan"
   },
   {
    "t": "au programme, rare au national récent",
    "c": "faible",
    "m": "remarque",
    "taille": 16
   }
  ]
 },
 "dv6": {
  "titre": "Montrer que f′(x) = (3x + 2)/(2√(x + 1))",
  "lignes": [
   {
    "t": "f est dérivable sur ]−1 ; +∞[ et pour tout x de ]−1 ; +∞[ :",
    "c": "jaune",
    "m": "derivable",
    "taille": 18,
    "r": [
     "derivable",
     "la première ligne"
    ]
   },
   {
    "t": "f′(x) = 1 × √(x + 1) + x × 1/(2√(x + 1))",
    "c": "cyan",
    "m": "produit",
    "taille": 18
   },
   {
    "t": "= (2(x + 1) + x) / (2√(x + 1))",
    "c": "cyan",
    "m": "meme_denominateur",
    "r": [
     "meme_denominateur",
     "même dénominateur"
    ]
   },
   {
    "t": "= (3x + 2) / (2√(x + 1))",
    "c": "vert",
    "m": "forme",
    "cadre": "vert",
    "r": [
     "forme",
     "la forme de l’énoncé"
    ]
   }
  ]
 },
 "va3": {
  "titre": "Factoriser pour lire le signe",
  "lignes": [
   {
    "t": "f(x) = x³ − 3x ;  f est dérivable sur ℝ",
    "c": "jaune",
    "m": "derivable"
   },
   {
    "t": "f′(x) = 3x² − 3 = 3(x² − 1) = 3(x − 1)(x + 1)",
    "c": "cyan",
    "m": "factorise",
    "r": [
     "factorise",
     "f′ factorisée"
    ]
   },
   {
    "t": "3 > 0, donc le signe de f′(x) est le signe de (x − 1)(x + 1)",
    "c": "vert",
    "m": "phrase",
    "cadre": "vert",
    "taille": 18,
    "r": [
     "phrase",
     "la phrase du signe"
    ]
   },
   {
    "t": "",
    "tab": {
     "cols": [
      "−∞",
      "−1",
      "1",
      "+∞"
     ],
     "rows": [
      {
       "nom": "x + 1",
       "cells": [
        [
         0.5,
         "−"
        ],
        [
         1,
         "0"
        ],
        [
         1.5,
         "+"
        ],
        [
         2.5,
         "+"
        ]
       ]
      },
      {
       "nom": "x − 1",
       "cells": [
        [
         0.5,
         "−"
        ],
        [
         1.5,
         "−"
        ],
        [
         2,
         "0"
        ],
        [
         2.5,
         "+"
        ]
       ]
      },
      {
       "nom": "f'(x)",
       "cells": [
        [
         0.5,
         "+",
         "vert"
        ],
        [
         1,
         "0"
        ],
        [
         1.5,
         "−",
         "rouge"
        ],
        [
         2,
         "0"
        ],
        [
         2.5,
         "+",
         "vert"
        ]
       ],
       "m": "signe"
      }
     ],
     "w": 520,
     "nomW": 96
    }
   }
  ]
 },
 "va5": {
  "titre": "x + 1/x : la double barre",
  "lignes": [
   {
    "t": "f′(x) = 1 − 1/x² = (x² − 1)/x² = (x − 1)(x + 1)/x²",
    "c": "cyan",
    "m": "derivee",
    "taille": 18
   },
   {
    "t": "x² > 0 : le signe de f′(x) est le signe de (x − 1)(x + 1)",
    "c": "vert",
    "m": "phrase",
    "taille": 18
   },
   {
    "t": "",
    "tab": {
     "cols": [
      "−∞",
      "−1",
      "0",
      "1",
      "+∞"
     ],
     "rows": [
      {
       "nom": "x − 1",
       "cells": [
        [
         0.5,
         "−"
        ],
        [
         1.5,
         "−"
        ],
        [
         2.5,
         "−"
        ],
        [
         3,
         "0"
        ],
        [
         3.5,
         "+"
        ]
       ]
      },
      {
       "nom": "x + 1",
       "cells": [
        [
         0.5,
         "−"
        ],
        [
         1,
         "0"
        ],
        [
         1.5,
         "+"
        ],
        [
         2.5,
         "+"
        ],
        [
         3.5,
         "+"
        ]
       ]
      },
      {
       "nom": "f'(x)",
       "cells": [
        [
         0.5,
         "+",
         "vert"
        ],
        [
         1,
         "0"
        ],
        [
         1.5,
         "−",
         "rouge"
        ],
        [
         2.5,
         "−",
         "rouge"
        ],
        [
         3,
         "0"
        ],
        [
         3.5,
         "+",
         "vert"
        ]
       ],
       "m": "ligne_signe",
       "r": [
        "ligne_signe",
        "le signe de f′(x)"
       ]
      },
      {
       "nom": "f(x)",
       "var": [
        [
         0,
         "−∞",
         "b"
        ],
        [
         1,
         "−2",
         "h"
        ],
        [
         2,
         "−∞",
         "b"
        ],
        [
         2,
         "+∞",
         "h",
         true
        ],
        [
         3,
         "2",
         "b"
        ],
        [
         4,
         "+∞",
         "h"
        ]
       ],
       "m": "ligne_fleches",
       "r": [
        "ligne_fleches",
        "les flèches et les limites"
       ]
      }
     ],
     "w": 640,
     "nomW": 96,
     "barres": [
      2
     ],
     "r": [
      "tableau",
      "le tableau de variations de x + 1/x"
     ]
    }
   }
  ]
 },
 "va6": {
  "titre": "Du tableau à l'inégalité",
  "lignes": [
   {
    "t": "",
    "tab": {
     "cols": [
      "0",
      "1",
      "+∞"
     ],
     "rows": [
      {
       "nom": "f'(x)",
       "cells": [
        [
         0.5,
         "−",
         "rouge"
        ],
        [
         1,
         "0"
        ],
        [
         1.5,
         "+",
         "vert"
        ]
       ]
      },
      {
       "nom": "f(x)",
       "var": [
        [
         0,
         "+∞",
         "h"
        ],
        [
         1,
         "2",
         "b"
        ],
        [
         2,
         "+∞",
         "h"
        ]
       ],
       "m": "tableau"
      }
     ],
     "w": 420,
     "nomW": 96,
     "barres": [
      0
     ]
    }
   },
   {
    "t": "sur ]0 ; +∞[, f admet un minimum : f(1) = 2",
    "c": "cyan",
    "m": "minimum",
    "r": [
     "minimum",
     "le minimum lu dans le tableau"
    ]
   },
   {
    "t": "donc pour tout x > 0 :  f(x) ≥ 2",
    "c": "cyan",
    "m": "inegalite"
   },
   {
    "t": "c’est-à-dire  x + 1/x ≥ 2",
    "c": "vert",
    "m": "conclusion",
    "cadre": "vert"
   }
  ]
 },
 "va7": {
  "titre": "Le signe vient de la partie I",
  "lignes": [
   {
    "t": "Partie I : g admet un minimum g(1) = 1 > 0",
    "c": "jaune",
    "m": "partie1"
   },
   {
    "t": "donc pour tout x > 0 :  g(x) ≥ 1 > 0",
    "c": "cyan",
    "m": "signe_g",
    "r": [
     "signe_g",
     "le signe de g"
    ]
   },
   {
    "t": "Partie II : on a montré  f′(x) = g(x)/x²",
    "c": "jaune",
    "m": "partie2"
   },
   {
    "t": "x² > 0, donc le signe de f′(x) est le signe de g(x)",
    "c": "cyan",
    "m": "lien",
    "r": [
     "lien",
     "le lien entre f′ et g"
    ]
   },
   {
    "t": "g(x) > 0, donc f′(x) > 0 : f est strictement croissante sur ]0 ; +∞[",
    "c": "vert",
    "m": "conclusion",
    "cadre": "vert",
    "taille": 17
   }
  ]
 },
 "bi7": {
  "titre": "Montrer que (D) : y = x − 1 est asymptote",
  "lignes": [
   {
    "t": "f(x) = (x² − 2x + 2)/(x − 1) = x − 1 + 1/(x − 1)   (x ≠ 1)",
    "c": "jaune",
    "m": "enonce",
    "taille": 17
   },
   {
    "t": "f(x) − (x − 1) = 1/(x − 1)",
    "c": "cyan",
    "m": "difference",
    "r": [
     "difference",
     "on retire la droite"
    ]
   },
   {
    "t": "lim_{x→+∞} [f(x) − (x − 1)] = lim_{x→+∞} 1/(x − 1) = 0",
    "c": "cyan",
    "m": "limite"
   },
   {
    "t": "donc la droite (D) : y = x − 1 est une asymptote oblique à (C_f) au voisinage de +∞",
    "c": "vert",
    "m": "conclusion",
    "cadre": "vert",
    "taille": 16
   },
   {
    "t": "on ne refait pas tout l'arbre : une seule limite",
    "c": "orange",
    "m": "remarque",
    "taille": 16
   }
  ]
 },
 "sy4": {
  "titre": "Ω(2 ; 1) est un centre de symétrie de (C_f)",
  "lignes": [
   {
    "t": "f(x) = (x + 1)/(x − 2),  D_f = ℝ∖{2}",
    "c": "jaune",
    "m": "enonce"
   },
   {
    "t": "① x ≠ 2  ⟹  4 − x ≠ 2,  donc (4 − x) ∈ D_f",
    "c": "cyan",
    "m": "domaine",
    "r": [
     "domaine",
     "la première ligne : le domaine"
    ]
   },
   {
    "t": "② f(4 − x) + f(x) = (5 − x)/(2 − x) + (x + 1)/(x − 2)",
    "c": "cyan",
    "m": "somme",
    "taille": 18
   },
   {
    "t": "= (x − 5)/(x − 2) + (x + 1)/(x − 2) = (2x − 4)/(x − 2) = 2 = 2 × 1",
    "c": "cyan",
    "m": "calcul",
    "taille": 18
   },
   {
    "t": "donc Ω(2 ; 1) est un centre de symétrie de (C_f)",
    "c": "vert",
    "m": "conclusion",
    "cadre": "vert"
   },
   {
    "t": "parité : a = 0 :  paire f(−x) = f(x) ;  impaire f(−x) = −f(x)",
    "c": "orange",
    "m": "parite",
    "taille": 16
   }
  ]
 },
 "rec5": {
  "titre": "Calculer (f⁻¹)′(2) pour f(x) = x³ + x",
  "lignes": [
   {
    "t": "① f(1) = 1 + 1 = 2,  donc f⁻¹(2) = 1",
    "c": "cyan",
    "m": "antecedent",
    "r": [
     "antecedent",
     "l’antécédent"
    ]
   },
   {
    "t": "② f est dérivable en 1 :  f′(x) = 3x² + 1,  f′(1) = 4 ≠ 0",
    "c": "cyan",
    "m": "condition",
    "r": [
     "condition",
     "f′(x₀) ≠ 0"
    ]
   },
   {
    "t": "③ donc f⁻¹ est dérivable en 2 et",
    "c": "cyan",
    "m": "conclusion"
   },
   {
    "t": "(f⁻¹)′(2) = 1/f′(1) = 1/4",
    "c": "vert",
    "m": "formule",
    "cadre": "vert",
    "taille": 22
   }
  ]
 },
 "ec1": {
  "titre": "L'ordre d'un problème d'analyse",
  "lignes": [
   {
    "t": "1. domaine, limites aux bornes",
    "c": "cyan",
    "m": "limites"
   },
   {
    "t": "2. branches infinies : asymptotes, branches paraboliques",
    "c": "cyan",
    "m": "branches"
   },
   {
    "t": "3. dérivabilité en un point ; « montrer que f′(x) = … »",
    "c": "cyan",
    "m": "derivee"
   },
   {
    "t": "4. signe de f′ et tableau de variations",
    "c": "cyan",
    "m": "variations",
    "r": [
     "variations",
     "le tableau de variations"
    ]
   },
   {
    "t": "5. concavité, point d'inflexion  ·  position relative",
    "c": "cyan",
    "m": "concavite"
   },
   {
    "t": "6. tracé de (C_f)  ·  7. fonction réciproque",
    "c": "cyan",
    "m": "trace"
   },
   {
    "t": "une question, un cas type, une phrase",
    "c": "orange",
    "m": "regle",
    "inter": 30
   }
  ]
 },
 "ec2": {
  "titre": "Lire la forme demandée",
  "lignes": [
   {
    "t": "« vérifier que f(x) = x − 1 + 1/(x − 1) »",
    "c": "jaune",
    "m": "verifier"
   },
   {
    "t": "on part de x − 1 + 1/(x − 1) = ((x − 1)² + 1)/(x − 1) = (x² − 2x + 2)/(x − 1) = f(x)",
    "c": "cyan",
    "m": "un_membre",
    "taille": 16,
    "r": [
     "un_membre",
     "partir d’un seul membre"
    ]
   },
   {
    "t": "cette écriture sert ensuite : f(x) − (x − 1) = 1/(x − 1) → 0",
    "c": "vert",
    "m": "sert",
    "taille": 17
   },
   {
    "t": "question bloquée : on utilise le résultat donné et on continue",
    "c": "orange",
    "m": "bloque",
    "taille": 17,
    "r": [
     "bloque",
     "utiliser le résultat donné"
    ]
   }
  ]
 },
 "ec4": {
  "titre": "Une solution unique, lue dans le tableau",
  "lignes": [
   {
    "t": "f(x) = x³ + x − 1 sur [0 ; 1] :",
    "c": "jaune",
    "m": "enonce"
   },
   {
    "t": "f est continue sur [0 ; 1]",
    "c": "cyan",
    "m": "continue"
   },
   {
    "t": "f′(x) = 3x² + 1 > 0 : f est strictement croissante sur [0 ; 1]",
    "c": "cyan",
    "m": "monotone",
    "r": [
     "monotone",
     "strictement monotone"
    ]
   },
   {
    "t": "f(0) = −1 et f(1) = 1 : f(0) × f(1) < 0",
    "c": "cyan",
    "m": "signes"
   },
   {
    "t": "donc f(x) = 0 admet une solution unique α dans ]0 ; 1[",
    "c": "vert",
    "m": "conclusion",
    "cadre": "vert",
    "taille": 18
   }
  ]
 }
};
