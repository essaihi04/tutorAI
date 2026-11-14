/* Écrit par maths_build/suites_definition/build.py depuis les p*.py du cours math_ch3_suites_numeriques : ne pas modifier à la main. */
window.CALCULS = {
 "o2": {
  "titre": "Trois gestes de 1re bac",
  "lignes": [
   {
    "t": "① géométrique : u_n = u_0 × q^{n}",
    "c": "jaune"
   },
   {
    "t": "u_0 = 3, q = 2 :  u_3 = 3 × 2³ = 24",
    "c": "cyan",
    "m": "geometrique",
    "dx": 30
   },
   {
    "t": "② signe de (x − 1)/(x + 2) pour x > 1 :",
    "c": "jaune"
   },
   {
    "t": "x − 1 > 0 et x + 2 > 0, donc (x − 1)/(x + 2) > 0",
    "c": "cyan",
    "m": "signe",
    "dx": 30
   },
   {
    "t": "③ même dénominateur :",
    "c": "jaune"
   },
   {
    "t": "1/(x + 1) − 1 = (1 − x − 1)/(x + 1) = −x/(x + 1)",
    "c": "cyan",
    "m": "denominateur",
    "dx": 30
   }
  ]
 },
 "a5": {
  "titre": "Le terme général : arithmétique",
  "lignes": [
   {
    "t": "u_n = u_p + (n − p) r",
    "c": "jaune",
    "m": "formule",
    "cadre": "jaune",
    "r": [
     "formule",
     "uₙ = uₚ + (n − p)r"
    ],
    "taille": 24,
    "inter": 52
   },
   {
    "t": "p = 0 :   u_n = u_0 + n r",
    "c": "cyan",
    "m": "p_zero"
   },
   {
    "t": "p = 1 :   u_n = u_1 + (n − 1) r",
    "c": "cyan",
    "m": "p_un"
   },
   {
    "t": "exemple : u_0 = 2, r = 3  →  u_n = 2 + 3n",
    "c": "blanc",
    "m": "exemple",
    "inter": 40
   }
  ]
 },
 "a7": {
  "titre": "Le terme général : géométrique",
  "lignes": [
   {
    "t": "u_n = u_p × q^{n−p}",
    "c": "jaune",
    "m": "formule",
    "cadre": "jaune",
    "r": [
     "formule",
     "uₙ = uₚ·qⁿ⁻ᵖ"
    ],
    "taille": 24,
    "inter": 52
   },
   {
    "t": "p = 0 :   u_n = u_0 × q^{n}",
    "c": "cyan",
    "m": "p_zero"
   },
   {
    "t": "p = 1 :   u_n = u_1 × q^{n−1}",
    "c": "cyan",
    "m": "p_un"
   },
   {
    "t": "vérifier : n = 0 → u_0 × q^{0} = u_0, car q^{0} = 1",
    "c": "orange",
    "m": "q_zero",
    "r": [
     "q_zero",
     "q⁰ = 1"
    ],
    "inter": 40
   }
  ]
 },
 "a9": {
  "titre": "Additionner sans tout écrire",
  "lignes": [
   {
    "t": "arithmétique :",
    "c": "jaune",
    "inter": 32
   },
   {
    "t": "S = (nombre de termes) × (premier + dernier) / 2",
    "c": "cyan",
    "m": "arith",
    "dx": 20
   },
   {
    "t": "1 + 2 + … + 10 = 10 × (1 + 10) / 2 = 55",
    "c": "blanc",
    "m": "exemple_arith",
    "dx": 20,
    "inter": 46
   },
   {
    "t": "géométrique (q ≠ 1) :",
    "c": "jaune",
    "inter": 32
   },
   {
    "t": "S = premier × (1 − q^{N}) / (1 − q)",
    "c": "cyan",
    "m": "geo",
    "dx": 20,
    "cadre": "cyan"
   },
   {
    "t": "N = nombre de termes",
    "c": "orange",
    "m": "puissance",
    "dx": 20,
    "r": [
     "puissance",
     "la puissance N : le nombre de termes"
    ]
   }
  ]
 },
 "r2": {
  "titre": "Les trois titres d'une récurrence",
  "lignes": [
   {
    "t": "Montrons par récurrence que, pour tout n ∈ ℕ, u_n > 16.",
    "c": "blanc",
    "m": "annonce",
    "taille": 18
   },
   {
    "t": "Initialisation : pour n = 0, u_0 = 17 > 16.",
    "c": "vert",
    "m": "initialisation",
    "taille": 18
   },
   {
    "t": "Hérédité : soit n ∈ ℕ.",
    "c": "cyan",
    "m": "heredite",
    "taille": 18
   },
   {
    "t": "Supposons que u_n > 16",
    "c": "cyan",
    "m": "hypothese",
    "dx": 30,
    "taille": 18,
    "cadre": "cyan",
    "r": [
     "joker",
     "l’hypothèse de récurrence : pour UN n"
    ]
   },
   {
    "t": "et montrons que u_{n+1} > 16.",
    "c": "orange",
    "m": "cible",
    "dx": 30,
    "taille": 18,
    "r": [
     "cible",
     "la cible : le rang n + 1"
    ]
   },
   {
    "t": "Conclusion : d’après le principe de récurrence, pour tout n ∈ ℕ, u_n > 16.",
    "c": "jaune",
    "m": "conclusion",
    "taille": 18
   },
   {
    "t": "Supposons que pour tout n, u_n > 16",
    "c": "rouge",
    "m": "faux",
    "taille": 18,
    "barre": true,
    "r": [
     "faux",
     "l’erreur : supposer pour tout n"
    ]
   }
  ]
 },
 "r3": {
  "titre": "On habille l'hypothèse (national 2016 R)",
  "lignes": [
   {
    "t": "u_{n+1} = (1/16) u_n + 15/16 : u_n apparaît une fois",
    "c": "blanc",
    "m": "enonce",
    "taille": 18
   },
   {
    "t": "u_n > 1",
    "c": "cyan",
    "m": "hypothese",
    "cadre": "cyan",
    "inter": 40
   },
   {
    "t": "× 1/16  (1/16 > 0) :    (1/16) u_n > 1/16",
    "c": "cyan",
    "m": "fois",
    "taille": 18
   },
   {
    "t": "+ 15/16 :    (1/16) u_n + 15/16 > 1/16 + 15/16 = 1",
    "c": "cyan",
    "m": "plus",
    "taille": 18
   },
   {
    "t": "c’est-à-dire u_{n+1} > 1",
    "c": "jaune",
    "m": "cible",
    "cadre": "jaune",
    "inter": 44
   },
   {
    "t": "on fait à l’inégalité ce que la formule fait à u_n",
    "c": "orange",
    "m": "regle",
    "r": [
     "regle",
     "la règle : les opérations de la formule, dans l’ordre"
    ]
   }
  ]
 },
 "r4": {
  "titre": "uₙ en haut et en bas (national)",
  "lignes": [
   {
    "t": "u_{n+1} = (4u_n + 3)/(3u_n + 4) : u_n apparaît deux fois",
    "c": "blanc",
    "m": "enonce",
    "taille": 18
   },
   {
    "t": "u_n > 1 ⇒ 4u_n + 3 > 7 et 3u_n + 4 > 7, et le quotient ?",
    "c": "rouge",
    "m": "essai",
    "taille": 17,
    "barre": true,
    "r": [
     "essai",
     "l’essai qui ne marche pas"
    ]
   },
   {
    "t": "on étudie le signe de u_{n+1} − 1 :",
    "c": "jaune",
    "m": "difference",
    "taille": 18
   },
   {
    "t": "u_{n+1} − 1 = (4u_n + 3 − 3u_n − 4)/(3u_n + 4) = (u_n − 1)/(3u_n + 4)",
    "c": "cyan",
    "m": "calcul",
    "taille": 17
   },
   {
    "t": "u_n − 1 > 0  (hypothèse)   et   3u_n + 4 > 0",
    "c": "vert",
    "m": "signes",
    "taille": 18,
    "r": [
     "signes",
     "un signe sous le haut, un signe sous le bas"
    ]
   },
   {
    "t": "donc u_{n+1} − 1 > 0 : u_{n+1} > 1",
    "c": "jaune",
    "m": "conclusion",
    "cadre": "jaune"
   }
  ]
 },
 "r5": {
  "titre": "Une fois ou deux fois ?",
  "lignes": [
   {
    "t": "u_n apparaît UNE fois  →  opérations sur l’hypothèse",
    "c": "cyan",
    "m": "une_fois",
    "r": [
     "une_fois",
     "une fois : les opérations"
    ]
   },
   {
    "t": "ex. u_{n+1} = ¼ u_n + 12",
    "c": "faible",
    "dx": 30,
    "taille": 17,
    "inter": 44
   },
   {
    "t": "u_n apparaît DEUX fois  →  signe de u_{n+1} − a",
    "c": "vert",
    "m": "deux_fois",
    "r": [
     "deux_fois",
     "deux fois : la différence"
    ]
   },
   {
    "t": "ex. u_{n+1} = (4u_n + 3)/(3u_n + 4)",
    "c": "faible",
    "dx": 30,
    "taille": 17,
    "inter": 44
   },
   {
    "t": "u_{n+1} = f(u_n), f croissante  →  f(a) ≤ f(u_n) ≤ f(b)",
    "c": "orange",
    "m": "fonction",
    "r": [
     "fonction",
     "avec une fonction croissante"
    ]
   },
   {
    "t": "(on le verra avec les fonctions, partie VII)",
    "c": "faible",
    "dx": 30,
    "taille": 16
   }
  ]
 },
 "r6": {
  "titre": "L'écriture donnée par l'énoncé (national 2024)",
  "lignes": [
   {
    "t": "u_{n+1} = (4u_n − 2)/(u_n + 1)",
    "c": "cyan",
    "m": "enonce"
   },
   {
    "t": "vérifier : 4 − 6/(1 + u_n) = (4 + 4u_n − 6)/(1 + u_n) = u_{n+1}",
    "c": "blanc",
    "m": "verifier",
    "taille": 17
   },
   {
    "t": "→ u_n n’apparaît plus qu’une fois : opérations",
    "c": "jaune",
    "m": "outil",
    "r": [
     "outil",
     "l’écriture donnée : l’outil"
    ]
   },
   {
    "t": "attention : 2 ≤ x ≤ 4  ⇒  1/4 ≤ 1/x ≤ 1/2",
    "c": "orange",
    "m": "inverse",
    "r": [
     "inverse",
     "l’inverse change l’ordre"
    ]
   },
   {
    "t": "× (−6) : l’ordre change encore",
    "c": "orange",
    "m": "negatif",
    "dx": 96
   }
  ]
 },
 "r7": {
  "titre": "Strict ou large ?",
  "lignes": [
   {
    "t": "u_{n+1} < 3  ⇒  u_{n+1} ≤ 3   ✓",
    "c": "vert",
    "m": "strict",
    "r": [
     "strict",
     "le strict entraîne le large"
    ]
   },
   {
    "t": "u_{n+1} ≤ 3  n’entraîne pas  u_{n+1} < 3",
    "c": "rouge",
    "m": "large"
   },
   {
    "t": "relire l’énoncé avant d’écrire la conclusion",
    "c": "jaune",
    "m": "relire",
    "cadre": "jaune",
    "inter": 50
   },
   {
    "t": "supposer u_n ≥ 1 … et conclure u_{n+1} > 1",
    "c": "rouge",
    "m": "erreur",
    "barre": true,
    "r": [
     "erreur",
     "l’erreur : changer le signe en route"
    ]
   }
  ]
 },
 "r8": {
  "titre": "À toi : national 2023 R",
  "lignes": [
   {
    "t": "u_0 = 0   et   u_{n+1} = (u_n − 2)/(2u_n + 5)",
    "c": "cyan",
    "m": "enonce"
   },
   {
    "t": "Montrer que pour tout n ∈ ℕ, u_n > −1.",
    "c": "blanc",
    "m": "question"
   },
   {
    "t": "u_n apparaît deux fois  →  signe de u_{n+1} + 1",
    "c": "vert",
    "m": "methode",
    "r": [
     "methode",
     "la méthode : la différence"
    ]
   },
   {
    "t": "Initialisation · Hérédité · Conclusion",
    "c": "jaune",
    "m": "plan",
    "cadre": "jaune"
   }
  ]
 },
 "m2": {
  "titre": "Le signe de la différence (national 2016 R)",
  "lignes": [
   {
    "t": "u_{n+1} − u_n = (1/16) u_n + 15/16 − u_n",
    "c": "blanc",
    "m": "difference"
   },
   {
    "t": "= −(15/16) u_n + 15/16 = −(15/16)(u_n − 1)",
    "c": "cyan",
    "m": "factorise",
    "dx": 30
   },
   {
    "t": "u_n > 1 (récurrence), donc u_n − 1 > 0",
    "c": "vert",
    "m": "signe",
    "r": [
     "signe",
     "le signe vient de la récurrence"
    ]
   },
   {
    "t": "donc u_{n+1} − u_n < 0 : (u_n) est décroissante",
    "c": "jaune",
    "m": "conclusion",
    "cadre": "jaune"
   }
  ]
 },
 "m3": {
  "titre": "L'égalité donnée (national 2024)",
  "lignes": [
   {
    "t": "donné : u_{n+1} − u_n = (u_n − 1)(2 − u_n)/(1 + u_n)",
    "c": "cyan",
    "m": "donne"
   },
   {
    "t": "on sait (récurrence) : 2 ≤ u_n ≤ 4",
    "c": "vert",
    "m": "sait"
   },
   {
    "t": "u_n − 1 : ?      2 − u_n : ?      1 + u_n : ?",
    "c": "jaune",
    "m": "signes",
    "r": [
     "signes",
     "un signe sous chaque facteur"
    ]
   },
   {
    "t": "un signe sous chaque facteur, puis le signe du tout",
    "c": "orange",
    "m": "methode",
    "inter": 40
   }
  ]
 },
 "m4": {
  "titre": "Le quotient comparé à 1",
  "lignes": [
   {
    "t": "si u_n > 0 pour tout n :",
    "c": "jaune",
    "m": "condition",
    "r": [
     "condition",
     "la condition : uₙ > 0"
    ]
   },
   {
    "t": "u_{n+1}/u_n ≤ 1  ⇒  u_{n+1} ≤ u_n : décroissante",
    "c": "cyan",
    "m": "inferieur",
    "dx": 30
   },
   {
    "t": "u_{n+1}/u_n ≥ 1  ⇒  u_{n+1} ≥ u_n : croissante",
    "c": "cyan",
    "m": "superieur",
    "dx": 30
   },
   {
    "t": "si u_n < 0 : multiplier par u_n change l’ordre ⚠",
    "c": "orange",
    "m": "attention",
    "inter": 40
   }
  ]
 },
 "x2": {
  "titre": "vₙ₊₁ = q × vₙ ? (national 2016 R)",
  "lignes": [
   {
    "t": "cible : v_{n+1} = q × v_n",
    "c": "jaune",
    "m": "cible",
    "cadre": "jaune",
    "r": [
     "cible",
     "la cible : q fois vₙ"
    ],
    "inter": 44
   },
   {
    "t": "v_n = u_n − 1 et u_{n+1} = (1/16) u_n + 15/16",
    "c": "faible",
    "taille": 17
   },
   {
    "t": "v_{n+1} = u_{n+1} − 1",
    "c": "blanc",
    "m": "definition"
   },
   {
    "t": "= (1/16) u_n + 15/16 − 1",
    "c": "cyan",
    "m": "remplace",
    "dx": 60,
    "r": [
     "remplace",
     "uₙ₊₁ remplacé par la relation"
    ]
   },
   {
    "t": "= (1/16) u_n − 1/16 = (1/16)(u_n − 1) = (1/16) v_n",
    "c": "cyan",
    "m": "simplifie",
    "dx": 60
   },
   {
    "t": "donc (v_n) est géométrique de raison 1/16",
    "c": "jaune",
    "m": "conclusion"
   }
  ]
 },
 "x3": {
  "titre": "Une fraction de fraction (national 2016)",
  "lignes": [
   {
    "t": "u_{n+1} = (3 + u_n)/(5 − u_n)   et   v_n = (u_n − 1)/(3 − u_n)",
    "c": "faible",
    "m": "enonce",
    "taille": 17
   },
   {
    "t": "v_{n+1} = (u_{n+1} − 1)/(3 − u_{n+1})",
    "c": "blanc",
    "m": "ecrire"
   },
   {
    "t": "on remplace u_{n+1} en haut et en bas",
    "c": "cyan",
    "m": "remplacer"
   },
   {
    "t": "même dénominateur : 5 − u_n en haut et en bas",
    "c": "cyan",
    "m": "meme"
   },
   {
    "t": "(a/b) / (c/b) = a/c",
    "c": "orange",
    "m": "regle",
    "cadre": "orange",
    "r": [
     "regle",
     "la règle : les dénominateurs se simplifient"
    ],
    "inter": 46
   },
   {
    "t": "cible : v_{n+1} = (1/2) v_n",
    "c": "jaune",
    "m": "cible"
   }
  ]
 },
 "x4": {
  "titre": "Revenir à uₙ",
  "lignes": [
   {
    "t": "v_n = u_n − 16   ⇒   u_n = v_n + 16 = 16 + (¼)^{n}",
    "c": "cyan",
    "m": "simple"
   },
   {
    "t": "v_n = (u_n − 1)/(3 − u_n) :",
    "c": "jaune",
    "m": "fraction",
    "inter": 34
   },
   {
    "t": "v_n (3 − u_n) = u_n − 1",
    "c": "blanc",
    "m": "croix",
    "dx": 30
   },
   {
    "t": "3v_n − v_n u_n = u_n − 1   ⇒   u_n + v_n u_n = 3v_n + 1",
    "c": "blanc",
    "m": "regrouper",
    "dx": 30,
    "taille": 18
   },
   {
    "t": "u_n (1 + v_n) = 1 + 3v_n   ⇒   u_n = (1 + 3v_n)/(1 + v_n)",
    "c": "jaune",
    "m": "isoler",
    "dx": 30,
    "taille": 18,
    "cadre": "jaune",
    "r": [
     "isoler",
     "uₙ isolé"
    ]
   }
  ]
 },
 "x5": {
  "titre": "Arithmétique ou géométrique ?",
  "lignes": [
   {
    "t": "arithmétique : v_{n+1} − v_n = r (constante)",
    "c": "cyan",
    "m": "arith",
    "r": [
     "arith",
     "arithmétique : la différence"
    ]
   },
   {
    "t": "géométrique : v_{n+1} = q × v_n",
    "c": "vert",
    "m": "geo",
    "r": [
     "geo",
     "géométrique : la multiplication"
    ],
    "inter": 46
   },
   {
    "t": "national 2021 R :  v_n = 1/(1 − u_n)",
    "c": "faible",
    "taille": 17
   },
   {
    "t": "v_{n+1} − v_n = … = 1/2",
    "c": "blanc",
    "m": "calcul",
    "dx": 30
   },
   {
    "t": "→ arithmétique de raison 1/2 :  v_n = v_0 + n r",
    "c": "jaune",
    "m": "formule",
    "cadre": "jaune"
   }
  ]
 },
 "l5": {
  "titre": "La phrase complète",
  "lignes": [
   {
    "t": "u_n = 16 + (¼)^{n}",
    "c": "cyan",
    "m": "enonce"
   },
   {
    "t": "car −1 < ¼ < 1,   lim (¼)^{n} = 0",
    "c": "vert",
    "m": "condition",
    "cadre": "vert",
    "r": [
     "condition",
     "la condition avant la limite"
    ],
    "inter": 46
   },
   {
    "t": "donc lim u_n = 16 + 0 = 16",
    "c": "jaune",
    "m": "limite"
   },
   {
    "t": "on écrit toujours la condition avant la limite",
    "c": "orange",
    "m": "regle",
    "inter": 40
   }
  ]
 },
 "c5": {
  "titre": "Au plus les 2/5 du précédent (national 2020)",
  "lignes": [
   {
    "t": "u_{n+1} = 2u_n/(2u_n + 5),   u_n > 0",
    "c": "cyan",
    "m": "enonce"
   },
   {
    "t": "méthode 1 : minorer le dénominateur",
    "c": "jaune",
    "m": "methode1",
    "r": [
     "methode1",
     "minorer le dénominateur"
    ]
   },
   {
    "t": "2u_n + 5 ≥ 5   ⇒   1/(2u_n + 5) ≤ 1/5",
    "c": "blanc",
    "m": "minorer",
    "dx": 30
   },
   {
    "t": "méthode 2 : signe de u_{n+1} − (2/5) u_n",
    "c": "jaune",
    "m": "methode2",
    "r": [
     "methode2",
     "la différence"
    ]
   }
  ]
 },
 "f5": {
  "titre": "Les conditions, une à une",
  "lignes": [
   {
    "t": "(u_n) convergente : notons ℓ sa limite",
    "c": "cyan",
    "m": "converge"
   },
   {
    "t": "f continue sur I = [1 ; 2]",
    "c": "cyan",
    "m": "continue"
   },
   {
    "t": "f(I) ⊂ I : l’image de [1 ; 2] est [1 ; 4/3]",
    "c": "cyan",
    "m": "stable",
    "r": [
     "stable",
     "f(I) ⊂ I"
    ]
   },
   {
    "t": "u_0 = 2 ∈ I",
    "c": "cyan",
    "m": "u0"
   },
   {
    "t": "donc ℓ est solution de l’équation f(x) = x dans I",
    "c": "jaune",
    "m": "conclusion",
    "cadre": "jaune",
    "inter": 46
   },
   {
    "t": "sans une condition, le correcteur refuse ℓ = f(ℓ)",
    "c": "orange",
    "m": "attention"
   }
  ]
 },
 "p1": {
  "titre": "À partir de quel rang ?",
  "lignes": [
   {
    "t": "u_n = (n + 1)/(n + 3) ≥ 99/100 ?",
    "c": "cyan",
    "m": "inequation"
   },
   {
    "t": "⇔ 100(n + 1) ≥ 99(n + 3)   (dénominateurs positifs)",
    "c": "blanc",
    "m": "croix",
    "r": [
     "croix",
     "le produit en croix"
    ]
   },
   {
    "t": "⇔ 100n + 100 ≥ 99n + 297   ⇔   n ≥ 197",
    "c": "blanc",
    "m": "resoudre"
   },
   {
    "t": "plus petit entier : n = 197",
    "c": "jaune",
    "m": "rang",
    "cadre": "jaune",
    "inter": 46
   }
  ]
 },
 "p3": {
  "titre": "La limite de Sₙ",
  "lignes": [
   {
    "t": "w_n géométrique, w_0 = 1, raison 1/2",
    "c": "faible",
    "taille": 17
   },
   {
    "t": "S_n = w_0 + w_1 + … + w_n   (n + 1 termes)",
    "c": "cyan",
    "m": "somme"
   },
   {
    "t": "S_n = 1 × (1 − (1/2)^{n+1}) / (1 − 1/2)",
    "c": "blanc",
    "m": "formule"
   },
   {
    "t": "car −1 < 1/2 < 1,  lim (1/2)^{n+1} = 0",
    "c": "vert",
    "m": "condition",
    "r": [
     "condition",
     "la condition sur la raison"
    ]
   },
   {
    "t": "lim S_n = 1/(1 − 1/2) = 2",
    "c": "jaune",
    "m": "limite",
    "cadre": "jaune"
   }
  ]
 },
 "e1": {
  "titre": "Un exercice complet (national 2024)",
  "lignes": [
   {
    "t": "u_0 = 4,   u_{n+1} = (4u_n − 2)/(u_n + 1)",
    "c": "cyan",
    "m": "enonce"
   },
   {
    "t": "1. récurrence : 2 ≤ u_n ≤ 4",
    "c": "blanc",
    "m": "q1",
    "taille": 18,
    "r": [
     "q1",
     "la récurrence"
    ]
   },
   {
    "t": "2. u_{n+1} − u_n = (u_n − 1)(2 − u_n)/(1 + u_n) ≤ 0 : décroissante",
    "c": "blanc",
    "m": "q2",
    "taille": 17,
    "r": [
     "q2",
     "le sens de variation"
    ]
   },
   {
    "t": "3. décroissante et minorée par 2 : (u_n) converge",
    "c": "blanc",
    "m": "q3",
    "taille": 18,
    "r": [
     "q3",
     "la convergence"
    ]
   },
   {
    "t": "4. v_n = (u_n − 2)/(u_n − 1) : géométrique de raison 2/3",
    "c": "blanc",
    "m": "q4",
    "taille": 18,
    "r": [
     "q4",
     "la suite auxiliaire"
    ]
   },
   {
    "t": "5. u_n en fonction de n, puis lim u_n",
    "c": "jaune",
    "m": "q5",
    "taille": 18,
    "r": [
     "q5",
     "la limite"
    ]
   }
  ]
 }
};
