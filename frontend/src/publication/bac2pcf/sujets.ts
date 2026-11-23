/** Généré par scripts/sujets_2bacpcf.py à partir des exercices existants (voix déjà enregistrées) : ne pas modifier à la main. */
import type { PartieExamen } from '../tronc-commun/sujet';

export const SUJET_PHYSIQUE = {
 "titre": "Examen de révision — Physique : ondes lumineuses et décroissance radioactive",
 "niveau": "2ᵉ Bac PC BIOF",
 "matiere": "Physique",
 "minutes": 30,
 "programme": "les ondes lumineuses (diffraction, écart angulaire) ; la décroissance radioactive (demi-vie, loi de décroissance)",
 "consigne": "Révise en conditions d'examen : réponds à chaque question comme sur ta copie. Dès que tu réponds, tu as ta note sur le barème et la correction expliquée, avec la voix du professeur. Prévois 30 minutes ; tu avances à ton rythme.",
 "parties": [
  {
   "id": "E1",
   "court": "Ex. 1",
   "titre": "Exercice 1 — Un laser rouge et une fente fine",
   "minutes": 15,
   "intro": "On éclaire une fente fine verticale de largeur a avec un laser rouge de longueur d'onde λ = 640 nm. Sur un écran placé à la distance D de la fente, on observe une figure de diffraction. La figure représente le montage vu de dessus : θ est l'écart angulaire, L la largeur de la tache centrale.",
   "figures": [
    {
     "type": "schema",
     "titre": "Le montage vu de dessus (angle exagéré)",
     "cadre": {
      "l": 10.4,
      "h": 5
     },
     "legende": "θ va du centre de la tache centrale à son bord ; L est la largeur de la tache centrale.",
     "elements": [
      {
       "f": "rect",
       "de": [
        0.2,
        2.2
       ],
       "a": [
        1.4,
        2.8
       ],
       "couleur": "blanc"
      },
      {
       "f": "texte",
       "at": [
        0.8,
        3.15
       ],
       "t": "laser",
       "couleur": "blanc",
       "ancre": "centre",
       "taille": "petit"
      },
      {
       "f": "ligne",
       "pts": [
        [
         1.4,
         2.5
        ],
        [
         3,
         2.5
        ]
       ],
       "couleur": "rouge",
       "epais": true
      },
      {
       "f": "ligne",
       "pts": [
        [
         3,
         0.9
        ],
        [
         3,
         2.38
        ]
       ],
       "couleur": "blanc",
       "epais": true
      },
      {
       "f": "ligne",
       "pts": [
        [
         3,
         2.62
        ],
        [
         3,
         4.1
        ]
       ],
       "couleur": "blanc",
       "epais": true
      },
      {
       "f": "texte",
       "at": [
        3,
        4.45
       ],
       "t": "fente",
       "couleur": "blanc",
       "ancre": "centre",
       "taille": "petit"
      },
      {
       "f": "texte",
       "at": [
        2.75,
        2.75
       ],
       "t": "a",
       "couleur": "cyan",
       "ancre": "droite"
      },
      {
       "f": "ligne",
       "pts": [
        [
         3,
         2.5
        ],
        [
         9,
         4.0
        ]
       ],
       "couleur": "rouge"
      },
      {
       "f": "ligne",
       "pts": [
        [
         3,
         2.5
        ],
        [
         9,
         1.0
        ]
       ],
       "couleur": "rouge"
      },
      {
       "f": "ligne",
       "pts": [
        [
         3,
         2.5
        ],
        [
         9,
         2.5
        ]
       ],
       "couleur": "faible",
       "trait": "pointille"
      },
      {
       "f": "arc",
       "c": [
        3,
        2.5
       ],
       "r": 1.6,
       "de": 0,
       "a": 14.04,
       "couleur": "orange"
      },
      {
       "f": "texte",
       "at": [
        4.95,
        2.85
       ],
       "t": "θ",
       "couleur": "orange",
       "ancre": "centre"
      },
      {
       "f": "ligne",
       "pts": [
        [
         9,
         0.5
        ],
        [
         9,
         4.5
        ]
       ],
       "couleur": "blanc",
       "epais": true
      },
      {
       "f": "texte",
       "at": [
        9,
        4.8
       ],
       "t": "écran",
       "couleur": "blanc",
       "ancre": "centre",
       "taille": "petit"
      },
      {
       "f": "cote",
       "de": [
        9.5,
        1.0
       ],
       "a": [
        9.5,
        4.0
       ],
       "t": "L",
       "couleur": "jaune",
       "pos": "e"
      },
      {
       "f": "cote",
       "de": [
        3,
        0.35
       ],
       "a": [
        9,
        0.35
       ],
       "t": "D",
       "couleur": "cyan",
       "pos": "n"
      }
     ]
    }
   ],
   "donnees": [
    "λ = 640 nm",
    "a = 0,16 mm",
    "D = 2,5 m",
    "a' = 0,08 mm (question 3)",
    "1 nm = 10⁻⁹ m ; 1 mm = 10⁻³ m"
   ],
   "questions": [
    {
     "id": "1-1",
     "texte": "Calculer l'écart angulaire θ.",
     "points": 3.25,
     "genre": "valeur",
     "grandeur": "θ",
     "valeur": 0.004,
     "unites": [
      "rad"
     ],
     "tolerance": 0.03,
     "correction": [
      "1 : λ = 640 nm = 6,4 × 10⁻⁷ m ; a = 0,16 mm = 1,6 × 10⁻⁴ m",
      "θ = λ/a = 6,4 × 10⁻⁷/(1,6 × 10⁻⁴)",
      "θ = 4 × 10⁻³ rad"
     ]
    },
    {
     "id": "1-2",
     "texte": "D'après la figure, tan θ = (L/2)/D. L'angle θ étant petit, on prend tan θ ≈ θ (θ en radian). Calculer, en cm, la largeur L de la tache centrale.",
     "points": 3.25,
     "genre": "valeur",
     "grandeur": "L",
     "valeur": 2.0,
     "unites": [
      "cm"
     ],
     "tolerance": 0.03,
     "correction": [
      "2 : tan θ = (L/2)/D = L/(2D)",
      "θ petit (en radian) : tan θ ≈ θ, donc L = 2D·θ",
      "L = 2 × 2,5 × 4 × 10⁻³ = 2 × 10⁻² m = 2 cm"
     ]
    },
    {
     "id": "1-3",
     "texte": "On remplace la fente par une fente plus fine, de largeur a' = 0,08 mm ; le laser et l'écran ne changent pas. Calculer, en cm, la nouvelle largeur L' de la tache centrale. Comment varie L quand a diminue ?",
     "points": 3.25,
     "genre": "valeur",
     "grandeur": "L'",
     "valeur": 4.0,
     "unites": [
      "cm"
     ],
     "tolerance": 0.03,
     "correction": [
      "3 : L' = 2λD/a' (λ et D ne changent pas)",
      "L' = 2 × 6,4 × 10⁻⁷ × 2,5/(8 × 10⁻⁵) = 4 cm",
      "a est au dénominateur : quand a diminue, L augmente"
     ]
    }
   ]
  },
  {
   "id": "E2",
   "court": "Ex. 2",
   "titre": "Exercice 2 — Le bismuth 210 : demi-vie, noyaux restants et pourcentage",
   "minutes": 15,
   "intro": "Le bismuth 210 est radioactif, de demi-vie t½ = 5,0 jours. À la date t = 0, un échantillon contient N₀ = 8,0 × 10¹⁸ noyaux de bismuth 210. La figure représente le nombre N de noyaux restants en fonction du temps : N(t) = N₀·e^(−λt).",
   "figures": [
    {
     "type": "courbe",
     "titre": "N(t) pour le bismuth 210",
     "axes": {
      "x": {
       "min": 0,
       "max": 25,
       "nom": "t",
       "unite": "jours",
       "graduations": [
        0,
        5,
        10,
        15,
        20,
        25
       ]
      },
      "y": {
       "min": 0,
       "max": 9,
       "nom": "N",
       "unite": "× 10¹⁸ noyaux",
       "graduations": [
        0,
        2,
        4,
        6,
        8
       ]
      }
     },
     "legende": "Nombre N de noyaux restants en fonction du temps.",
     "elements": [
      {
       "f": "courbe",
       "expr": "8.0*exp(-0.13863*x)",
       "de": 0,
       "a": 25,
       "couleur": "cyan",
       "texte": "N(t)",
       "texte_x": 17.5,
       "pos": "ne"
      },
      {
       "f": "point",
       "at": [
        0,
        8.0
       ],
       "t": "N₀",
       "pos": "e",
       "couleur": "jaune"
      }
     ]
    }
   ],
   "donnees": [
    "t½ = 5,0 jours",
    "N₀ = 8,0 × 10¹⁸ noyaux à t = 0",
    "ln2 ≈ 0,693"
   ],
   "questions": [
    {
     "id": "2-1",
     "texte": "Calculer la constante radioactive λ du bismuth 210, en jour⁻¹.",
     "points": 3.25,
     "genre": "valeur",
     "grandeur": "λ",
     "valeur": 0.139,
     "unites": [
      "j⁻¹",
      "j-1",
      "jour⁻¹",
      "jour-1",
      "/j",
      "/jour",
      "j^-1"
     ],
     "tolerance": 0.03,
     "correction": [
      "1 : λ = (ln 2)/t½",
      "λ = 0,693/5,0",
      "λ ≈ 0,139 j⁻¹"
     ]
    },
    {
     "id": "2-2",
     "texte": "Calculer le nombre N₁ de noyaux de bismuth 210 restants à la date t₁ = 15 jours.",
     "points": 3.25,
     "genre": "valeur",
     "grandeur": "N₁",
     "valeur": 1e+18,
     "unites": [
      "noyau",
      ""
     ],
     "tolerance": 0.03,
     "correction": [
      "2 : t₁ = 15 j = 3·t½",
      "N₁ = N₀/2³ = 8,0 × 10¹⁸/8",
      "N₁ = 1,0 × 10¹⁸ noyaux"
     ]
    },
    {
     "id": "2-3",
     "texte": "Déterminer la date t₂ à laquelle 30 % des noyaux initiaux de bismuth 210 se sont désintégrés.",
     "points": 3.75,
     "genre": "valeur",
     "grandeur": "t₂",
     "valeur": 2.6,
     "unites": [
      "jour",
      "j"
     ],
     "tolerance": 0.03,
     "correction": [
      "3 : 30 % désintégrés, il reste 70 % : N(t₂) = 0,70·N₀",
      "0,70·N₀ = N₀·e^(−λt₂) ⇒ t₂ = (1/λ)·ln(1/0,70)",
      "t₂ = (1/0,139) × ln(1/0,70) ≈ 2,6 jours"
     ]
    }
   ]
  }
 ]
} as unknown as { titre: string; niveau: string; matiere: string; minutes: number; programme: string; consigne: string; parties: PartieExamen[] };
export const VOIX_PHYSIQUE: Record<string, string> = {
 "partie/E1": "/media/audio/exercices/phys_ex_ch3_fente_2/enonce/intro_v1.mp3",
 "question/1-1": "/media/audio/exercices/phys_ex_ch3_fente_2/enonce/q1_v1.mp3",
 "correction/1-1": "/media/audio/exercices/phys_ex_ch3_fente_2/corrections/q1_v1.mp3",
 "question/1-2": "/media/audio/exercices/phys_ex_ch3_fente_2/enonce/q2_v1.mp3",
 "correction/1-2": "/media/audio/exercices/phys_ex_ch3_fente_2/corrections/q2_v1.mp3",
 "question/1-3": "/media/audio/exercices/phys_ex_ch3_fente_2/enonce/q3_v1.mp3",
 "correction/1-3": "/media/audio/exercices/phys_ex_ch3_fente_2/corrections/q3_v1.mp3",
 "partie/E2": "/media/audio/exercices/phys_ex_ch4_demivie_2/enonce/intro_v1.mp3",
 "question/2-1": "/media/audio/exercices/phys_ex_ch4_demivie_2/enonce/q1_v1.mp3",
 "correction/2-1": "/media/audio/exercices/phys_ex_ch4_demivie_2/corrections/q1_v1.mp3",
 "question/2-2": "/media/audio/exercices/phys_ex_ch4_demivie_2/enonce/q2_v1.mp3",
 "correction/2-2": "/media/audio/exercices/phys_ex_ch4_demivie_2/corrections/q2_v1.mp3",
 "question/2-3": "/media/audio/exercices/phys_ex_ch4_demivie_2/enonce/q3_v1.mp3",
 "correction/2-3": "/media/audio/exercices/phys_ex_ch4_demivie_2/corrections/q3_v1.mp3"
};

export const SUJET_CHIMIE = {
 "titre": "Examen de révision — Chimie : transformations dans les deux sens et état d'équilibre",
 "niveau": "2ᵉ Bac PC BIOF",
 "matiere": "Chimie",
 "minutes": 30,
 "programme": "les transformations dans les deux sens (pH, taux d'avancement final) ; l'état d'équilibre (quotient de réaction, constante K)",
 "consigne": "Révise en conditions d'examen : réponds à chaque question comme sur ta copie. Dès que tu réponds, tu as ta note sur le barème et la correction expliquée, avec la voix du professeur. Prévois 30 minutes ; tu avances à ton rythme.",
 "parties": [
  {
   "id": "E1",
   "court": "Ex. 1",
   "titre": "Exercice 1 — L'acide propanoïque dans l'eau : pH, x_max, x_f et τ",
   "minutes": 15,
   "intro": "On prépare un volume V = 200 mL d'une solution aqueuse d'acide propanoïque C₂H₅COOH de concentration C = 2,0 × 10⁻² mol/L. À 25 °C, la mesure du pH de la solution donne pH = 3,29.",
   "figures": [],
   "donnees": [
    "V = 200 mL",
    "C = 2,0 × 10⁻² mol/L",
    "pH = 3,29 (à 25 °C)",
    "Couple : C₂H₅COOH(aq) / C₂H₅COO⁻(aq)"
   ],
   "questions": [
    {
     "id": "1-1",
     "texte": "Écrire l'équation de la réaction de l'acide propanoïque C₂H₅COOH avec l'eau.",
     "points": 2.0,
     "genre": "redaction",
     "attendu": "C₂H₅COOH(aq) + H₂O(l) ⇌ C₂H₅COO⁻(aq) + H₃O⁺(aq)",
     "elements": [
      "1 : l'acide propanoïque cède un proton à l'eau",
      "C₂H₅COOH(aq) + H₂O(l) ⇌ C₂H₅COO⁻(aq) + H₃O⁺(aq)"
     ],
     "correction": [
      "1 : l'acide propanoïque cède un proton à l'eau",
      "C₂H₅COOH(aq) + H₂O(l) ⇌ C₂H₅COO⁻(aq) + H₃O⁺(aq)"
     ]
    },
    {
     "id": "1-2",
     "texte": "La mesure du pH de la solution donne pH = 3,29. Calculer la concentration [H₃O⁺]_éq des ions oxonium dans la solution.",
     "points": 2.75,
     "genre": "valeur",
     "grandeur": "[H₃O⁺]",
     "valeur": 0.0005128613839913648,
     "unites": [
      "mol/l",
      "mol.l",
      "mol·l",
      "mol l"
     ],
     "tolerance": 0.03,
     "correction": [
      "2 : [H₃O⁺]_éq = 10^(−pH)",
      "[H₃O⁺]_éq = 10^(−3,29)",
      "[H₃O⁺]_éq = 5,1 × 10⁻⁴ mol/L"
     ]
    },
    {
     "id": "1-3",
     "texte": "Le volume de la solution est V = 200 mL. En s'aidant du tableau d'avancement, calculer l'avancement maximal x_max.",
     "points": 2.75,
     "genre": "valeur",
     "grandeur": "x_max",
     "valeur": 0.004,
     "unites": [
      "mol"
     ],
     "tolerance": 0.03,
     "correction": [
      "3 : l'eau est en excès, l'acide est limitant : C·V − x_max = 0",
      "x_max = C·V = 2,0 × 10⁻² × 0,200",
      "x_max = 4,0 × 10⁻³ mol"
     ]
    },
    {
     "id": "1-4",
     "texte": "Calculer l'avancement final x_f, puis le taux d'avancement final τ (valeur décimale). Conclure.",
     "points": 2.75,
     "genre": "valeur",
     "grandeur": "τ",
     "valeur": 0.025643069199568245,
     "unites": [
      ""
     ],
     "tolerance": 0.03,
     "correction": [
      "4 : x_f = [H₃O⁺]_éq·V = 5,13 × 10⁻⁴ × 0,200 = 1,03 × 10⁻⁴ mol",
      "τ = x_f/x_max = 1,03 × 10⁻⁴ / 4,0 × 10⁻³ = 0,026",
      "τ < 1 : la réaction de l'acide avec l'eau est limitée"
     ]
    }
   ]
  },
  {
   "id": "E2",
   "court": "Ex. 2",
   "titre": "Exercice 2 — Une solution d'acide propanoïque : du pH à la constante K",
   "minutes": 15,
   "intro": "On prépare une solution aqueuse d'acide propanoïque C₂H₅COOH de concentration C = 5,0 × 10⁻² mol/L. À 25 °C, la mesure du pH de cette solution donne pH = 3,09. La réaction de l'acide avec l'eau est rapide : le pH mesuré est celui de l'état d'équilibre.",
   "figures": [],
   "donnees": [
    "C = 5,0 × 10⁻² mol/L",
    "pH = 3,09 à 25 °C",
    "[H₃O⁺] = 10^(−pH)"
   ],
   "questions": [
    {
     "id": "2-1",
     "texte": "Écrire l'équation de la réaction de l'acide propanoïque avec l'eau.",
     "points": 2.0,
     "genre": "redaction",
     "attendu": "C₂H₅COOH(aq) + H₂O(l) ⇌ C₂H₅COO⁻(aq) + H₃O⁺(aq) (double flèche : réaction limitée)",
     "elements": [
      "1 : C₂H₅COOH(aq) + H₂O(l) ⇌ C₂H₅COO⁻(aq) + H₃O⁺(aq)"
     ],
     "correction": [
      "1 : C₂H₅COOH(aq) + H₂O(l) ⇌ C₂H₅COO⁻(aq) + H₃O⁺(aq)"
     ]
    },
    {
     "id": "2-2",
     "texte": "Calculer la concentration [H₃O⁺]éq des ions oxonium à l'équilibre.",
     "points": 2.0,
     "genre": "valeur",
     "grandeur": "[H₃O⁺]éq",
     "valeur": 0.0008128305161640995,
     "unites": [
      "mol/l",
      "mol.l",
      "mol·l",
      "mol l"
     ],
     "tolerance": 0.03,
     "correction": [
      "2 : [H₃O⁺]éq = 10^(−pH)",
      "[H₃O⁺]éq = 10^(−3,09) = 8,1 × 10⁻⁴ mol/L"
     ]
    },
    {
     "id": "2-3",
     "texte": "À l'aide du tableau d'avancement, déterminer [C₂H₅COO⁻]éq et [C₂H₅COOH]éq.",
     "points": 2.75,
     "genre": "valeur",
     "grandeur": "[C₂H₅COOH]éq",
     "valeur": 0.049187169483835905,
     "unites": [
      "mol/l",
      "mol.l",
      "mol·l",
      "mol l"
     ],
     "tolerance": 0.03,
     "correction": [
      "3 : [C₂H₅COO⁻]éq = [H₃O⁺]éq = 8,1 × 10⁻⁴ mol/L",
      "[C₂H₅COOH]éq = C − [H₃O⁺]éq",
      "[C₂H₅COOH]éq = 5,0 × 10⁻² − 8,1 × 10⁻⁴ = 4,9 × 10⁻² mol/L"
     ]
    },
    {
     "id": "2-4",
     "texte": "Calculer le quotient de réaction Qr,éq dans l'état d'équilibre. En déduire la constante d'équilibre K associée à l'équation.",
     "points": 3.0,
     "genre": "valeur",
     "grandeur": "K",
     "valeur": 1.3432231513641302e-05,
     "unites": [
      ""
     ],
     "tolerance": 0.05,
     "correction": [
      "4 : Qr,éq = [C₂H₅COO⁻]éq·[H₃O⁺]éq / [C₂H₅COOH]éq",
      "Qr,éq = (8,1 × 10⁻⁴)²/4,9 × 10⁻² = 1,3 × 10⁻⁵",
      "K = Qr,éq = 1,3 × 10⁻⁵ (sans unité)"
     ]
    }
   ]
  }
 ]
} as unknown as { titre: string; niveau: string; matiere: string; minutes: number; programme: string; consigne: string; parties: PartieExamen[] };
export const VOIX_CHIMIE: Record<string, string> = {
 "partie/E1": "/media/audio/exercices/phys_ex_ch11_deux_sens_1/enonce/intro_v1.mp3",
 "question/1-1": "/media/audio/exercices/phys_ex_ch11_deux_sens_1/enonce/q1_v1.mp3",
 "correction/1-1": "/media/audio/exercices/phys_ex_ch11_deux_sens_1/corrections/q1_v1.mp3",
 "question/1-2": "/media/audio/exercices/phys_ex_ch11_deux_sens_1/enonce/q2_v1.mp3",
 "correction/1-2": "/media/audio/exercices/phys_ex_ch11_deux_sens_1/corrections/q2_v1.mp3",
 "question/1-3": "/media/audio/exercices/phys_ex_ch11_deux_sens_1/enonce/q3_v1.mp3",
 "correction/1-3": "/media/audio/exercices/phys_ex_ch11_deux_sens_1/corrections/q3_v1.mp3",
 "question/1-4": "/media/audio/exercices/phys_ex_ch11_deux_sens_1/enonce/q4_v1.mp3",
 "correction/1-4": "/media/audio/exercices/phys_ex_ch11_deux_sens_1/corrections/q4_v1.mp3",
 "partie/E2": "/media/audio/exercices/phys_ex_ch12_etat_equilibre_2/enonce/intro_v1.mp3",
 "question/2-1": "/media/audio/exercices/phys_ex_ch12_etat_equilibre_2/enonce/q1_v1.mp3",
 "correction/2-1": "/media/audio/exercices/phys_ex_ch12_etat_equilibre_2/corrections/q1_v1.mp3",
 "question/2-2": "/media/audio/exercices/phys_ex_ch12_etat_equilibre_2/enonce/q2_v1.mp3",
 "correction/2-2": "/media/audio/exercices/phys_ex_ch12_etat_equilibre_2/corrections/q2_v1.mp3",
 "question/2-3": "/media/audio/exercices/phys_ex_ch12_etat_equilibre_2/enonce/q3_v1.mp3",
 "correction/2-3": "/media/audio/exercices/phys_ex_ch12_etat_equilibre_2/corrections/q3_v1.mp3",
 "question/2-4": "/media/audio/exercices/phys_ex_ch12_etat_equilibre_2/enonce/q4_v1.mp3"
};
