"""Exploration etat_equilibre, partie B : plan (séances, parties, compétences, 36 diapositives), notions, visuels, décisions.
Importé par explo.py. Ids des diapositives et vues = contrat outils/cours/notes/cours/etat_equilibre_contrat_simulations.md."""

SEANCES = [
    {"n": 1, "titre": "Du taux d'avancement au quotient de réaction",
     "blocs": [["o1", "o2", "r1", "r2"], ["q1", "q2", "q3", "q4"], ["q5", "i1", "i2", "i3"]],
     "parties": [
         {"id": "ee_partie0", "titre": "Ouverture", "ids": ["o1", "o2"]},
         {"id": "ee_partie1", "titre": "I. Rappels : taux d'avancement final et état d'équilibre", "ids": ["r1", "r2"]},
         {"id": "ee_partie2", "titre": "II. Le quotient de réaction Qr", "ids": ["q1", "q2", "q3", "q4", "q5"]},
         {"id": "ee_partie3", "titre": "III. Qr dans l'état initial et au cours de la transformation", "ids": ["i1", "i2", "i3"]},
     ]},
    {"n": 2, "titre": "Quotient de réaction à l'équilibre et constante d'équilibre K",
     "blocs": [["e1", "e2", "e3", "k1"], ["k2", "k3", "k4", "k5"], ["m1", "m2", "m3", "m4"]],
     "parties": [
         {"id": "ee_partie4", "titre": "IV. Le quotient de réaction à l'équilibre Qr,éq", "ids": ["e1", "e2", "e3"]},
         {"id": "ee_partie5", "titre": "V. La constante d'équilibre K", "ids": ["k1", "k2", "k3", "k4", "k5"]},
         {"id": "ee_partie6", "titre": "VI. Déterminer K par le pH et par la conductimétrie", "ids": ["m1", "m2", "m3", "m4"]},
     ]},
    {"n": 3, "titre": "De quoi dépend τ, sujets du national, bilan",
     "blocs": [["f1", "f2", "f3", "f4"], ["n1", "n2", "n3", "n4"], ["n5", "n6", "bl", "cr"]],
     "parties": [
         {"id": "ee_partie7", "titre": "VII. De quoi dépend le taux d'avancement final ?", "ids": ["f1", "f2", "f3", "f4"]},
         {"id": "ee_partie8", "titre": "VIII. Sujets du national", "ids": ["n1", "n2", "n3", "n4", "n5", "n6"]},
         {"id": "ee_bilan", "titre": "IX. Bilan du chapitre", "ids": ["bl", "cr"]},
     ]},
]

def R(id, type, prompt, **kw):
    d = {"id": id, "type": type, "prompt": prompt}
    d.update(kw)
    return d

COMPETENCES = [
    {"id": "C1", "verbe": "Écrire l'expression du quotient de réaction Qr d'une réaction en solution aqueuse (eau solvant et solides absents, coefficients en exposants, sans unité)",
     "cadre_ids": ["EE1"], "dit": "écrire le quotient de réaction", "rappels": [
        R("C1_r1", "qcm", "Pour CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺, Qr vaut :",
          options=["[CH₃COOH]/([CH₃COO⁻]·[H₃O⁺])", "[CH₃COO⁻]·[H₃O⁺]/[CH₃COOH]", "[CH₃COO⁻]·[H₃O⁺]"], correct=1),
        R("C1_r2", "libre", "Écris Qr pour Cu²⁺ + Zn(s) ⇌ Cu(s) + Zn²⁺.", attendu="Qr = [Zn²⁺]/[Cu²⁺] : les solides n'y figurent pas"),
        R("C1_r3", "vrai_faux", "Le quotient de réaction Qr s'exprime en mol/L.", correct=False),
        R("C1_r4", "libre", "Écris Qr pour 2I⁻ + S₂O₈²⁻ ⇌ I₂ + 2SO₄²⁻.", attendu="Qr = [I₂]·[SO₄²⁻]²/([I⁻]²·[S₂O₈²⁻])"),
    ]},
    {"id": "C2", "verbe": "Calculer Qr dans un état donné, en particulier Qr,i dans l'état initial (concentrations après mélange), et savoir que Qr évolue jusqu'à l'équilibre",
     "cadre_ids": ["EE2"], "dit": "le quotient de réaction dans l'état initial", "rappels": [
        R("C2_r1", "qcm", "On verse de l'acide éthanoïque dans l'eau. Au tout premier instant, Qr,i vaut :",
          options=["0", "1", "1,57·10⁻⁵"], correct=0),
        R("C2_r2", "libre", "Mélange : 1,0·10⁻² mol de HCOOH, 1,0·10⁻² mol de CH₃COO⁻, 5,0·10⁻³ mol de CH₃COOH et 5,0·10⁻³ mol de HCOO⁻ dans 300 mL. Calcule Qr,i pour HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH.",
          attendu="Qr,i = (5,0·10⁻³ × 5,0·10⁻³)/(1,0·10⁻² × 1,0·10⁻²) = 0,25 (le volume se simplifie)"),
        R("C2_r3", "vrai_faux", "Pendant la réaction de l'acide éthanoïque avec l'eau, Qr augmente puis reste constant.", correct=True),
    ]},
    {"id": "C3", "verbe": "Calculer Qr,éq à partir du pH et du tableau d'avancement, et l'exprimer en fonction de C et du pH",
     "cadre_ids": ["EE3"], "dit": "le quotient de réaction à l'équilibre", "rappels": [
        R("C3_r1", "libre", "Acide éthanoïque C = 1,0·10⁻² mol/L, pH = 3,41. Calcule Qr,éq.",
          attendu="[H₃O⁺]éq = [CH₃COO⁻]éq = 3,89·10⁻⁴ mol/L ; [CH₃COOH]éq = 9,61·10⁻³ mol/L ; Qr,éq = 1,57·10⁻⁵"),
        R("C3_r2", "qcm", "Dans l'état d'équilibre, [CH₃COOH]éq vaut :", options=["C", "C − [H₃O⁺]éq", "[H₃O⁺]éq"], correct=1),
        R("C3_r3", "vrai_faux", "Qr,éq = 10^(−2pH)/(C − 10^(−pH)) pour la réaction d'un acide avec l'eau.", correct=True),
    ]},
    {"id": "C4", "verbe": "Savoir que Qr,éq = K, constante d'équilibre qui ne dépend que de la température (pas de l'état initial), et que la réaction inverse a pour constante 1/K",
     "cadre_ids": ["EE4"], "dit": "la constante d'équilibre", "rappels": [
        R("C4_r1", "vrai_faux", "Si on dilue la solution d'acide éthanoïque, sa constante d'équilibre K change.", correct=False),
        R("C4_r2", "qcm", "K = 1,6·10⁻⁵ pour CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺. Pour CH₃COO⁻ + H₃O⁺ ⇌ CH₃COOH + H₂O, la constante vaut :",
          options=["1,6·10⁻⁵", "−1,6·10⁻⁵", "6,25·10⁴"], correct=2),
        R("C4_r3", "libre", "De quoi dépend la constante d'équilibre K ?", attendu="seulement de la réaction et de la température ; pas de l'état initial"),
    ]},
    {"id": "C5", "verbe": "Établir K = C·τ²/(1 − τ) et déterminer K par pH-métrie ou par conductimétrie",
     "cadre_ids": ["EE5"], "dit": "K à partir de C et de τ", "rappels": [
        R("C5_r1", "libre", "Montre que K = C·τ²/(1 − τ) pour un acide AH dans l'eau.",
          attendu="[A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C(1 − τ) ; K = (C·τ)²/(C(1 − τ)) = C·τ²/(1 − τ)"),
        R("C5_r2", "qcm", "2019 N : C = 1,0·10⁻³ mol/L, τ = 0,22. K vaut :", options=["6,2·10⁻⁵", "2,2·10⁻⁴", "4,8·10⁻²"], correct=0),
        R("C5_r3", "libre", "σ = 4,6·10⁻³ S/m pour l'acide éthanoïque à 1,0·10⁻³ mol/L (λ(H₃O⁺) + λ(CH₃COO⁻) = 39,09·10⁻³ S·m²·mol⁻¹). Calcule τ puis K.",
          attendu="[H₃O⁺] = 0,118 mol/m³ = 1,18·10⁻⁴ mol/L ; τ = 0,118 ; K = 1,0·10⁻³ × 0,118²/(1 − 0,118) = 1,58·10⁻⁵"),
        R("C5_r4", "vrai_faux", "Dans K = C·τ²/(1 − τ), on met C en mol/L.", correct=True),
    ]},
    {"id": "C6", "verbe": "Expliquer que τ dépend de K (nature de la réaction) et de l'état initial (concentration), et que la dilution augmente τ sans changer K",
     "cadre_ids": ["EE6"], "dit": "de quoi dépend le taux d'avancement final", "rappels": [
        R("C6_r1", "qcm", "On dilue dix fois une solution d'acide éthanoïque. Que se passe-t-il ?",
          options=["τ augmente, K ne change pas", "τ et K augmentent", "τ diminue, K ne change pas"], correct=0),
        R("C6_r2", "vrai_faux", "À même concentration, l'acide de plus grande constante K a le plus grand τ.", correct=True),
        R("C6_r3", "libre", "Acide éthanoïque (K = 1,6·10⁻⁵) et acide méthanoïque (K = 1,8·10⁻⁴), tous deux à 1,0·10⁻² mol/L : lequel a le plus grand τ ?",
          attendu="l'acide méthanoïque (τ = 0,13 contre 0,039) : sa constante K est plus grande"),
    ]},
    {"id": "C7", "verbe": "Rédiger un exercice du national : expression littérale de Qr,i ou Qr,éq, tableau, application numérique, résultat sans unité",
     "cadre_ids": ["EE7"], "dit": "rédiger comme le barème", "rappels": [
        R("C7_r1", "libre", "2022 R : C_b = 1,0·10⁻² mol/L, τ = 0,20. Calcule Qr,éq = C_b·τ²/(1 − τ).", attendu="Qr,éq = 1,0·10⁻² × 0,20²/0,80 = 5,0·10⁻⁴"),
        R("C7_r2", "qcm", "2017 N : 3Cu²⁺ + 2Al(s) ⇌ 3Cu(s) + 2Al³⁺. Qr,i vaut :",
          options=["[Al³⁺]ᵢ²/[Cu²⁺]ᵢ³", "[Al³⁺]ᵢ/[Cu²⁺]ᵢ", "[Cu²⁺]ᵢ³/[Al³⁺]ᵢ²"], correct=0),
        R("C7_r3", "vrai_faux", "Pour « vérifier que Qr,éq = 1,77·10⁻⁵ », il suffit de recopier la valeur.", correct=False),
    ]},
]

def D(id, title, lead, marche, visuel, question, prediction, competences, demonstration=()):
    return {"id": id, "title": title, "lead": lead, "marche": marche, "visuel": visuel, "question": question,
            "prediction": prediction, "competences": list(competences), "demonstration": list(demonstration)}

DIAPOS = [
    # Séance 1
    D("o1", "La carte du chapitre : à l'équilibre, Qr,éq = K", "Que va-t-on savoir faire ?",
      "carte : rappel (τ, équilibre) → quotient de réaction Qr → état initial Qr,i → équilibre Qr,éq → constante K → mesures (pH, σ) → facteurs de τ → national ; « au national : Qr,éq ou K calculé dans 7 sessions sur 20, juste après τ »",
      "carte", "Au national, quelle question suit presque toujours le calcul de τ ?", False, ["C7"]),
    D("o2", "Deux concentrations, deux τ", "Le même acide à deux concentrations : que reste-t-il pareil ?",
      "deux flacons d'acide éthanoïque, 1,0·10⁻² et 1,0·10⁻³ mol/L ; pH-mètre au centième : 3,41 et 3,93 ; τ = 0,039 et 0,117 ; « τ change avec C… un nombre ne change-t-il pas ? » (la question du chapitre)",
      "rappel?vue=ouverture", "Les deux solutions auront-elles le même τ ?", True, ["C6"]),
    D("r1", "Rappel : le taux d'avancement final", "Ce qu'on sait déjà calculer.",
      "tableau de l'acide éthanoïque avec l'eau ; x_max = C·V ; x_éq = [H₃O⁺]éq·V ; τ = 10^(−pH)/C = 10^(−3,41)/1,0·10⁻² = 0,039 ; τ < 1 : réaction limitée",
      "rappel?vue=taux", "Que vaut τ pour pH = 3,41 et C = 1,0·10⁻² mol/L ?", False, ["C5"],
      ["τ = 10^(−pH)/C", "τ = 10^(−3,41)/1,0·10⁻² = 0,039"]),
    D("r2", "Rappel : l'état d'équilibre dynamique", "Dix minutes plus tard, qu'est-ce qui a changé ?",
      "pH toujours 3,41 ; deux compteurs (sens 1, sens 2) qui avancent ensemble ; trois concentrations constantes : [CH₃COOH]éq = 9,61·10⁻³, [CH₃COO⁻]éq = [H₃O⁺]éq = 3,89·10⁻⁴ mol/L ; « quel nombre relie ces trois concentrations ? »",
      "rappel?vue=equilibre", "À l'équilibre, les concentrations vont-elles encore changer ?", False, ["C3"]),
    D("q1", "Le quotient de réaction", "Un seul nombre pour décrire le mélange.",
      "équation CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺ ; les produits montent au numérateur, l'acide descend au dénominateur ; Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH] ; « produits en haut, réactifs en bas »",
      "quotient?vue=definition", "Quelles concentrations vont au numérateur : celles des réactifs ou des produits ?", False, ["C1"],
      ["Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH]"]),
    D("q2", "La forme générale de Qr", "Et si les coefficients ne valent pas 1 ?",
      "aA + bB ⇌ cC + dD → Qr = [C]^c·[D]^d/([A]^a·[B]^b) ; les coefficients deviennent des exposants ; exemple 2I⁻ + S₂O₈²⁻ ⇌ I₂ + 2SO₄²⁻ → Qr = [I₂]·[SO₄²⁻]²/([I⁻]²·[S₂O₈²⁻])",
      "quotient?vue=generale", "Où va le coefficient 2 de I⁻ dans Qr ?", False, ["C1"],
      ["Qr = [C]^c·[D]^d/([A]^a·[B]^b)", "Qr = [I₂]·[SO₄²⁻]²/([I⁻]²·[S₂O₈²⁻])"]),
    D("q3", "L'eau solvant n'apparaît pas", "Et la molécule d'eau de l'équation ?",
      "H₂O entourée dans l'équation de l'acide éthanoïque, puis barrée dans le quotient ; « l'eau est le solvant : elle n'apparaît pas dans Qr » ; ⚠ pas de concentration écrite pour l'eau solvant",
      "quotient?vue=eau", "L'eau va-t-elle figurer dans Qr ?", True, ["C1"]),
    D("q4", "Les solides n'apparaissent pas", "Une lame de zinc dans une solution d'ions cuivre.",
      "bécher bleu de Cu²⁺, lame de zinc ; Cu²⁺ + Zn(s) ⇌ Cu(s) + Zn²⁺ ; Zn(s) et Cu(s) barrés ; Qr = [Zn²⁺]/[Cu²⁺] ; « les solides n'apparaissent pas dans Qr »",
      "quotient?vue=solides", "Le zinc solide va-t-il figurer dans Qr ?", True, ["C1"],
      ["Qr = [Zn²⁺]/[Cu²⁺]"]),
    D("q5", "Qr n'a pas d'unité", "Calculer Qr dans un état donné.",
      "acide éthanoïque en cours de réaction : [H₃O⁺] = [CH₃COO⁻] = 2,0·10⁻⁴ mol/L, [CH₃COOH] = 9,8·10⁻³ mol/L ; Qr = (2,0·10⁻⁴ × 2,0·10⁻⁴)/(9,8·10⁻³) = 4,08·10⁻⁶ ; concentrations en mol/L, Qr sans unité",
      "quotient?vue=sans_unite", "Calcule Qr pour cet état. Quelle unité écris-tu ?", False, ["C1", "C2"],
      ["Qr = (2,0·10⁻⁴ × 2,0·10⁻⁴)/(9,8·10⁻³) = 4,08·10⁻⁶"]),
    D("i1", "Qr dans l'état initial : Qr,i", "Au moment où l'acide touche l'eau.",
      "l'acide est versé dans l'eau ; aucun produit encore : [CH₃COO⁻]ᵢ = [H₃O⁺]ᵢ = 0 ; Qr,i = 0 ; « Qr,i : quotient de réaction dans l'état initial »",
      "quotient?vue=initial", "Que vaut Qr,i quand aucun produit n'est encore formé ?", True, ["C2"]),
    D("i2", "Qr,i d'un mélange", "Quatre solutions versées ensemble.",
      "HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH ; quatre flacons, V_T = 300 mL ; [X]ᵢ = n/V_T ; V_T se simplifie ; Qr,i = (5,0·10⁻³ × 5,0·10⁻³)/(1,0·10⁻² × 1,0·10⁻²) = 0,25",
      "quotient?vue=melange", "Avec quelles concentrations calcule-t-on Qr,i : avant ou après le mélange ?", False, ["C2", "C7"],
      ["[X]ᵢ = n(X)/V_T", "Qr,i = [HCOO⁻]ᵢ·[CH₃COOH]ᵢ/([HCOOH]ᵢ·[CH₃COO⁻]ᵢ)", "Qr,i = (5,0·10⁻³ × 5,0·10⁻³)/(1,0·10⁻² × 1,0·10⁻²) = 0,25"]),
    D("i3", "Qr change pendant la transformation", "De Qr,i à l'équilibre.",
      "points qui montent : Qr = 0 ; 1,01·10⁻⁶ ; 4,08·10⁻⁶ ; 9,28·10⁻⁶ ; puis 1,57·10⁻⁵ et Qr ne bouge plus ; poignée de l'avancement ; « Qr augmente depuis Qr,i jusqu'à une valeur d'équilibre »",
      "quotient?vue=au_cours", "Quand la réaction avance, Qr va-t-il monter ou descendre ?", True, ["C2"]),
    # Séance 2
    D("e1", "Les concentrations à l'équilibre", "Le pH donne les trois concentrations.",
      "pH = 3,41 ; [H₃O⁺]éq = 10^(−pH) = 3,89·10⁻⁴ mol/L ; tableau : [CH₃COO⁻]éq = [H₃O⁺]éq ; [CH₃COOH]éq = C − [H₃O⁺]éq = 9,61·10⁻³ mol/L",
      "equilibre?vue=concentrations", "Que vaut [CH₃COOH]éq ?", False, ["C3"],
      ["[H₃O⁺]éq = 10^(−3,41) = 3,89·10⁻⁴ mol/L", "[CH₃COOH]éq = 1,0·10⁻² − 3,89·10⁻⁴ = 9,61·10⁻³ mol/L"]),
    D("e2", "Le quotient de réaction à l'équilibre", "On remplace dans Qr.",
      "Qr,éq = [CH₃COO⁻]éq·[H₃O⁺]éq/[CH₃COOH]éq = (3,89·10⁻⁴)²/(9,61·10⁻³) = 1,57·10⁻⁵ ; « Qr,éq : quotient de réaction dans l'état d'équilibre »",
      "equilibre?vue=qr_eq", "Qr,éq sera-t-il plus grand ou plus petit que 1 ?", True, ["C3"],
      ["Qr,éq = (3,89·10⁻⁴)²/(9,61·10⁻³) = 1,57·10⁻⁵"]),
    D("e3", "Qr,éq en fonction de C et du pH", "Une expression pour le national.",
      "[CH₃COO⁻]éq = [H₃O⁺]éq = 10^(−pH) ; [CH₃COOH]éq = C − 10^(−pH) ; Qr,éq = 10^(−2pH)/(C − 10^(−pH)) ; vérification 10^(−6,82)/(1,0·10⁻² − 10^(−3,41)) = 1,57·10⁻⁵",
      "equilibre?vue=expression", "Pourquoi trouve-t-on 10^(−2pH) au numérateur ?", False, ["C3", "C7"],
      ["Qr,éq = 10^(−2pH)/(C − 10^(−pH))", "Qr,éq = 10^(−6,82)/(1,0·10⁻² − 10^(−3,41)) = 1,57·10⁻⁵"]),
    D("k1", "Trois concentrations, un même Qr,éq", "On recommence avec 5,0·10⁻³ et 1,0·10⁻³ mol/L.",
      "tableau C · pH · τ · Qr,éq : 1,0·10⁻² · 3,41 · 0,039 · 1,57·10⁻⁵ ; 5,0·10⁻³ · 3,56 · 0,055 · 1,61·10⁻⁵ ; 1,0·10⁻³ · 3,93 · 0,117 · 1,56·10⁻⁵ ; τ change, Qr,éq ne change pas",
      "constante?vue=trois_c", "Qr,éq va-t-il changer avec la concentration, comme τ ?", True, ["C4"]),
    D("k2", "En partant des produits", "Éthanoate de sodium + acide chlorhydrique : quel Qr,éq ?",
      "50 mL d'acide chlorhydrique + 50 mL d'éthanoate de sodium (1,0·10⁻² mol/L) ; sens 2 ; pH 3,56 ; [CH₃COO⁻]éq = [H₃O⁺]éq = 2,75·10⁻⁴ mol/L ; Qr,éq = 1,61·10⁻⁵ : même valeur",
      "constante?vue=produits", "En partant des produits, retrouvera-t-on la même valeur ?", True, ["C4"],
      ["[CH₃COOH]éq = 5,0·10⁻³ − 2,75·10⁻⁴ = 4,72·10⁻³ mol/L", "Qr,éq = 10^(−7,12)/(5,0·10⁻³ − 10^(−3,56)) = 1,61·10⁻⁵"]),
    D("k3", "La constante d'équilibre K", "Un nombre propre à la réaction.",
      "K = Qr,éq ; constante d'équilibre ; ne dépend que de la température, pas de l'état initial ; acide éthanoïque + eau : K = 1,6·10⁻⁵ à 25 °C ; sans unité",
      "constante?vue=definition", "De quoi dépend K ?", False, ["C4"],
      ["K = Qr,éq", "K = 1,6·10⁻⁵ (25 °C)"]),
    D("k4", "La réaction inverse", "Et si on écrit l'équation dans l'autre sens ?",
      "CH₃COO⁻ + H₃O⁺ ⇌ CH₃COOH + H₂O ; le quotient se retourne ; K' = 1/K = 1/(1,6·10⁻⁵) = 6,25·10⁴",
      "constante?vue=inverse", "La constante de la réaction inverse sera-t-elle petite ou grande ?", True, ["C4"],
      ["K' = 1/K", "K' = 1/(1,6·10⁻⁵) = 6,25·10⁴"]),
    D("k5", "K en fonction de C et τ", "La relation la plus demandée au national.",
      "[A⁻]_éq = [H₃O⁺]_éq = C·τ ; [AH]_éq = C·(1 − τ) ; K = (C·τ)²/(C·(1 − τ)) ; un C se simplifie ; K = C·τ²/(1 − τ) ; vérification 1,0·10⁻² × 0,0389²/(1 − 0,0389) = 1,57·10⁻⁵",
      "constante?vue=c_tau", "Pourquoi [AH]éq vaut-il C·(1 − τ) ?", False, ["C5", "C7"],
      ["[A⁻]_éq = [H₃O⁺]_éq = C·τ", "[AH]_éq = C·(1 − τ)", "K = C·τ²/(1 − τ)", "K = 1,0·10⁻² × 0,0389²/(1 − 0,0389) = 1,57·10⁻⁵"]),
    D("m1", "Un autre acide, une autre constante", "L'acide méthanoïque à 1,0·10⁻² mol/L.",
      "pH = 2,90 ; [H₃O⁺]éq = 1,26·10⁻³ mol/L ; Qr,éq = 10^(−5,80)/(1,0·10⁻² − 10^(−2,90)) = 1,81·10⁻⁴ ; K = 1,8·10⁻⁴ à côté de K = 1,6·10⁻⁵ ; chaque réaction a sa constante",
      "constante?vue=autre_acide", "Sa constante K sera-t-elle plus grande que celle de l'acide éthanoïque ?", True, ["C5", "C4"],
      ["Qr,éq = 10^(−5,80)/(1,0·10⁻² − 10^(−2,90)) = 1,81·10⁻⁴"]),
    D("m2", "K par la conductimétrie : la relation", "Le conductimètre affiche 4,6 mS/m.",
      "acide éthanoïque 1,0·10⁻³ mol/L ; σ = λ(H₃O⁺)·[H₃O⁺] + λ(CH₃COO⁻)·[CH₃COO⁻] ; [CH₃COO⁻] = [H₃O⁺] ; σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] ; [H₃O⁺]_éq = σ/(λ(H₃O⁺) + λ(A⁻))",
      "conductimetrie?vue=relation", "Pourquoi peut-on mettre [H₃O⁺] en facteur ?", False, ["C5"],
      ["σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺]", "[H₃O⁺]_éq = σ/(λ(H₃O⁺) + λ(A⁻))"]),
    D("m3", "De σ à K", "σ = 4,6·10⁻³ S/m : que vaut K ?",
      "[H₃O⁺]_éq = 4,6·10⁻³/(39,09·10⁻³) = 0,118 mol/m³ ⚠ ÷ 10³ : 1,18·10⁻⁴ mol/L ; τ = 0,118 ; K = 1,0·10⁻³ × 0,118²/(1 − 0,118) = 1,58·10⁻⁵ ≈ 1,6·10⁻⁵ : même K que par le pH",
      "conductimetrie?vue=calcul", "Trouvera-t-on le même K qu'avec le pH-mètre ?", True, ["C5"],
      ["[H₃O⁺]_éq = 4,6·10⁻³/(39,09·10⁻³) = 0,118 mol/m³ = 1,18·10⁻⁴ mol/L", "τ = 1,18·10⁻⁴/1,0·10⁻³ = 0,118",
       "K = 1,0·10⁻³ × 0,118²/(1 − 0,118) = 1,58·10⁻⁵"]),
    D("m4", "National 2019 N : K par la conductivité", "Acide benzoïque, σ = 8,6·10⁻³ S/m.",
      "C = 1,0·10⁻³ mol/L ; τ = σ/(C·(λ₁ + λ₂)) = 0,22 (chapitre précédent) ; K = C·τ²/(1 − τ) = 1,0·10⁻³ × 0,22²/(1 − 0,22) = 6,2·10⁻⁵ (0,75 pt) ; ⚠ dans K, C en mol/L",
      "conductimetrie?vue=national", "Calcule K avec τ = 0,22.", False, ["C5", "C7"],
      ["K = C·τ²/(1 − τ)", "K = 1,0·10⁻³ × 0,22²/(1 − 0,22) = 6,2·10⁻⁵"]),
    # Séance 3
    D("f1", "Même K, concentration différente", "Pourquoi τ grandit quand on dilue ?",
      "trois barres τ : 0,039 ; 0,055 ; 0,117 quand C passe de 1,0·10⁻² à 1,0·10⁻³ mol/L ; trois étiquettes « K = 1,6·10⁻⁵ » identiques ; même K : plus C est petite, plus τ est grand",
      "facteurs?vue=dilution", "Si on dilue encore, τ va-t-il augmenter ou diminuer ?", True, ["C6"]),
    D("f2", "Même concentration, K différente", "Deux acides à 1,0·10⁻² mol/L.",
      "acide éthanoïque K = 1,6·10⁻⁵, τ = 0,039 ; acide méthanoïque K = 1,8·10⁻⁴, τ = 0,13 ; même C : plus K est grande, plus τ est grand",
      "facteurs?vue=nature", "Lequel des deux acides aura le plus grand τ ?", True, ["C6"]),
    D("f3", "τ dépend de K et de C", "Deux courbes, une poignée.",
      "courbes τ en fonction de C pour K = 1,6·10⁻⁵ et K = 1,8·10⁻⁴ ; poignée C : à 1,0·10⁻⁴ mol/L, τ = 0,33 et 0,72 ; à 1,0·10⁻¹, τ = 0,013 et 0,042 ; « τ dépend de la nature de la réaction (K) et de l'état initial (C) »",
      "facteurs?vue=courbe", "Pour quelle concentration τ est-il le plus proche de 1 ?", False, ["C6"]),
    D("f4", "Quand on dilue : ce qui change, ce qui reste", "Le tableau à retenir.",
      "quand on dilue : C ↓ ; [H₃O⁺] ↓ ; pH ↑ ; τ ↑ ; K inchangée (encadrée) ; ⚠ τ dépend de l'état initial, K non",
      "facteurs?vue=bilan_dilution", "Après une dilution, K sera-t-elle la même ?", True, ["C6", "C4"]),
    D("n1", "National 2017 N : Qr,éq avec C et pH", "Acide butanoïque, C = 1,0·10⁻² mol/L, pH = 3,41.",
      "Qr,éq = [H₃O⁺]éq²/(C − [H₃O⁺]éq) = 10^(−2pH)/(C − 10^(−pH)) = 1,57·10⁻⁵ (0,75 pt)",
      "equilibre?vue=national_2017", "Écris Qr,éq en fonction de C et du pH, puis calcule-le.", False, ["C3", "C7"],
      ["Qr,éq = 10^(−2pH)/(C − 10^(−pH))", "Qr,éq = 10^(−6,82)/(1,0·10⁻² − 10^(−3,41)) = 1,57·10⁻⁵"]),
    D("n2", "National 2022 R : une base avec l'eau", "Méthylamine, C_b = 1,0·10⁻² mol/L, τ = 0,20.",
      "CH₃NH₂ + H₂O ⇌ CH₃NH₃⁺ + HO⁻ ; [CH₃NH₃⁺]éq = [HO⁻]éq = C_b·τ ; [CH₃NH₂]éq = C_b(1 − τ) ; Qr,éq = C_b·τ²/(1 − τ) = 5,0·10⁻⁴ (0,5 pt)",
      "equilibre?vue=base", "Montre que Qr,éq = C_b·τ²/(1 − τ), puis calcule-le.", False, ["C5", "C7"],
      ["Qr,éq = [CH₃NH₃⁺]éq·[HO⁻]éq/[CH₃NH₂]éq = (C_b·τ)²/(C_b(1 − τ))", "Qr,éq = 1,0·10⁻² × 0,20²/0,80 = 5,0·10⁻⁴"]),
    D("n3", "National 2020 R : Qr,i d'un mélange", "Quatre solutions de 100 mL à 0,1 mol/L.",
      "HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH ; V_T = 400 mL ; Qr,i = (C₃V₃·C₄V₄)/(C₁V₁·C₂V₂) = 1 (0,5 pt) ; la suite de l'exercice (sens) : au semestre 2",
      "quotient?vue=national", "Calcule Qr,i.", False, ["C2", "C7"],
      ["Qr,i = (C₃V₃/V_T)·(C₄V₄/V_T)/((C₁V₁/V_T)·(C₂V₂/V_T)) = C₃V₃·C₄V₄/(C₁V₁·C₂V₂)", "Qr,i = (0,1 × 0,1 × 0,1 × 0,1)/(0,1 × 0,1 × 0,1 × 0,1) = 1"]),
    D("n4", "National 2017 N : Qr,i d'une pile", "Aluminium et cuivre, [Cu²⁺]ᵢ = [Al³⁺]ᵢ = 6,5·10⁻¹ mol/L.",
      "3Cu²⁺ + 2Al(s) ⇌ 3Cu(s) + 2Al³⁺ ; solides barrés ; Qr,i = [Al³⁺]ᵢ²/[Cu²⁺]ᵢ³ = (6,5·10⁻¹)²/(6,5·10⁻¹)³ = 1,5 (0,5 pt) ; la suite (piles) : au semestre 2",
      "quotient?vue=pile", "Les lames d'aluminium et de cuivre vont-elles entrer dans Qr,i ?", True, ["C1", "C7"],
      ["Qr,i = [Al³⁺]ᵢ²/[Cu²⁺]ᵢ³", "Qr,i = (6,5·10⁻¹)²/(6,5·10⁻¹)³ = 1,5"]),
    D("n5", "National 2017 R : K = 4", "Une estérification, lue sur une courbe.",
      "fig_2017R : palier n(acide) = 0,2 mol, n₀ = 0,6 mol → x_éq = 0,4 mol ; K = (0,4 × 0,4)/(0,2 × 0,2) = 4 (0,75 pt) ; ici l'eau est un produit, pas le solvant : elle figure (estérification étudiée plus tard)",
      "figures?fig=fig_2017R", "K sera-t-il plus grand ou plus petit que 1 ?", True, ["C4", "C7"],
      ["x_éq = 0,6 − 0,2 = 0,4 mol", "K = n(ester)·n(eau)/(n(acide)·n(alcool)) = (0,4 × 0,4)/(0,2 × 0,2) = 4"]),
    D("n6", "National 2021 N : τ puis Qr,éq", "C_a = 1,0·10⁻¹ mol/L, pH = 2,88.",
      "τ = 10^(−2,88)/0,10 = 0,0132 ; Qr,éq = C_a·τ²/(1 − τ) = 0,10 × 0,0132²/(1 − 0,0132) = 1,77·10⁻⁵ (1,5 pt pour les deux)",
      "equilibre?vue=national_2021", "Calcule τ, puis vérifie que Qr,éq = 1,77·10⁻⁵.", False, ["C5", "C7"],
      ["τ = 10^(−2,88)/0,10 = 0,0132", "Qr,éq = 0,10 × 0,0132²/(1 − 0,0132) = 1,77·10⁻⁵"]),
    D("bl", "Ce qu'il faut retenir", "La fiche du chapitre.",
      "blocs : quotient, état initial, équilibre, constante, mesures, facteurs, rédaction ; page 2 : tes lacunes",
      "bilan", "Quelle ligne de la fiche te paraît la plus difficile ?", False, ["C7"]),
    D("cr", "La carte complète", "Tout le chapitre d'un coup d'œil.",
      "carte complète ; suite : réactions acide-base (chapitre suivant) ; au semestre 2, piles : Qr,i comparé à K",
      "carte", "Par quelle branche commencerais-tu un exercice sur un acide dans l'eau ?", False, ["C7"]),
]

PLAN = {
    "principes": ("une idée nouvelle par diapositive ; une chose vue, une phrase, une question ; exemples A à K du contrat pour voir (acide "
                  "éthanoïque au pH-mètre au centième, trois concentrations, départ par les produits, conductimétrie, acide méthanoïque) ; "
                  "sept nationaux pour s'entraîner ; chaque bloc a au moins une prédiction ; Ka, pKa, Ke renvoyés au chapitre 13 ; la "
                  "comparaison de Qr,i à K (sens) renvoyée aux piles (semestre 2)"),
    "duree_estimee_min": 120,
    "decoupage_conseille": "trois séances de trois blocs de quatre diapositives (bilan et carte dans le dernier bloc)",
    "prefixe_diapositives": "ee_",
    "parties_pour_les_agents": ("une séance par agent (p1.py = séance 1, p2.py = séance 2, p3.py = séance 3) ; titres et ids des parties dans "
                                "seances[n].parties ; id de diapositive = ee_<id du plan>_<un mot>"),
    "prerequis_verifies_au_debut": ["tableau_avancement", "concentration_quantite_matiere", "logarithme_decimal_puissances",
                                    "puissances_dix_unites", "acide_base_bronsted_ph", "conductimetrie", "oxydoreduction_demi_equations"],
    "seances": SEANCES,
    "competences": COMPETENCES,
    "diapositives": DIAPOS,
}

NOTIONS = [
    {"id": "ecrire_qr", "notion": "Qr = [C]^c·[D]^d/([A]^a·[B]^b), sans l'eau solvant ni les solides",
     "pourquoi_difficile": "quatre règles à tenir ensemble (produits en haut, exposants, pas d'eau solvant, pas de solide) ; l'élève écrit l'équation entière dans la fraction",
     "prerequis": ["concentration_quantite_matiere", "oxydoreduction_demi_equations"],
     "marches": [
        {"n": 1, "idee": "produits en haut, réactifs en bas", "vu": "les espèces glissent au-dessus ou au-dessous de la barre", "phrase": "Qr compare ce qui est formé à ce qui reste", "question": "qui va au numérateur ?"},
        {"n": 2, "idee": "coefficients en exposants", "vu": "le 2 de 2I⁻ monte en exposant", "phrase": "chaque coefficient devient une puissance", "question": "exposant de [SO₄²⁻] ?"},
        {"n": 3, "idee": "pas d'eau solvant", "vu": "H₂O barrée", "phrase": "le solvant n'a pas de concentration à écrire", "question": "l'eau figure-t-elle ?"},
        {"n": 4, "idee": "pas de solide", "vu": "Zn(s) et Cu(s) barrés", "phrase": "seules les espèces dissoutes comptent", "question": "Qr pour Cu²⁺ + Zn ?"}],
     "image_mentale": "une recette : on écrit seulement les ingrédients dissous dans la marmite ; la marmite elle-même (l'eau) et les cuillères (les solides) ne comptent pas",
     "exemple_chiffre": "[H₃O⁺] = [CH₃COO⁻] = 2,0·10⁻⁴ mol/L, [CH₃COOH] = 9,8·10⁻³ mol/L → Qr = 4,08·10⁻⁶",
     "piege": "écrire l'eau ou un métal solide dans Qr ; oublier les exposants",
     "verification": "2017 N : Qr,i pour 3Cu²⁺ + 2Al(s) ⇌ 3Cu(s) + 2Al³⁺ ? ([Al³⁺]ᵢ²/[Cu²⁺]ᵢ³ = 1,5)"},
    {"id": "qr_evolue", "notion": "Qr change de Qr,i à Qr,éq",
     "pourquoi_difficile": "Qr est une grandeur qui varie, alors que K est fixe ; l'élève confond les deux",
     "prerequis": ["tableau_avancement"],
     "marches": [
        {"n": 1, "idee": "état initial", "vu": "aucun produit", "phrase": "Qr,i = 0", "question": "Qr,i ?"},
        {"n": 2, "idee": "Qr monte", "vu": "points qui montent", "phrase": "les produits se forment, Qr grandit", "question": "monte ou descend ?"},
        {"n": 3, "idee": "Qr s'arrête", "vu": "dernier point, palier", "phrase": "à l'équilibre Qr ne change plus", "question": "valeur finale ?"}],
     "image_mentale": "le compteur du taxi qui monte puis s'arrête à destination",
     "exemple_chiffre": "0 → 1,01·10⁻⁶ → 4,08·10⁻⁶ → 9,28·10⁻⁶ → 1,57·10⁻⁵",
     "piege": "« Qr est une constante »",
     "verification": "vrai ou faux : Qr,i = Qr,éq pour l'acide éthanoïque versé dans l'eau ? (faux : 0 et 1,57·10⁻⁵)"},
    {"id": "k_constante", "notion": "Qr,éq = K ne dépend pas de l'état initial (seulement de la température)",
     "pourquoi_difficile": "les concentrations à l'équilibre changent d'une expérience à l'autre, mais leur quotient non ; résultat admis, qu'il faut VOIR",
     "prerequis": ["logarithme_decimal_puissances", "puissances_dix_unites"],
     "marches": [
        {"n": 1, "idee": "Qr,éq de l'exemple A", "vu": "1,57·10⁻⁵", "phrase": "un nombre pour l'équilibre", "question": "Qr,éq ?"},
        {"n": 2, "idee": "autres concentrations", "vu": "colonne Qr,éq : 1,57 · 1,61 · 1,56 ·10⁻⁵", "phrase": "τ change, Qr,éq non", "question": "change-t-il ?"},
        {"n": 3, "idee": "autre départ", "vu": "partir des produits : 1,61·10⁻⁵", "phrase": "même valeur", "question": "même K ?"},
        {"n": 4, "idee": "K = Qr,éq", "vu": "encadré, thermomètre", "phrase": "K ne dépend que de la température", "question": "de quoi dépend K ?"}],
     "image_mentale": "la balance réglée : quelle que soit la quantité posée au départ, l'aiguille s'arrête au même trait K",
     "exemple_chiffre": "K = 1,6·10⁻⁵ (acide éthanoïque + eau, 25 °C)",
     "piege": "« diluer change K »",
     "verification": "on dilue 10 fois : K ? (inchangée, 1,6·10⁻⁵)"},
    {"id": "k_c_tau", "notion": "K = C·τ²/(1 − τ)",
     "pourquoi_difficile": "passer des quantités (x_éq) aux concentrations, puis à τ ; simplifier par C ; « montrer que » demandé dans 4 sessions",
     "prerequis": ["tableau_avancement", "concentration_quantite_matiere"],
     "marches": [
        {"n": 1, "idee": "[A⁻]éq = [H₃O⁺]éq = C·τ", "vu": "tableau en concentrations", "phrase": "x_éq/V = C·τ", "question": "pourquoi ?"},
        {"n": 2, "idee": "[AH]éq = C(1 − τ)", "vu": "colonne de l'acide", "phrase": "ce qui reste de l'acide", "question": "[AH]éq ?"},
        {"n": 3, "idee": "remplacer et simplifier", "vu": "un C barré", "phrase": "K = C·τ²/(1 − τ)", "question": "K ?"},
        {"n": 4, "idee": "vérifier", "vu": "1,57·10⁻⁵ retrouvé", "phrase": "même résultat qu'avec le pH", "question": "même valeur ?"}],
     "image_mentale": "une part du gâteau : C·τ est la part partie en produits, C(1 − τ) la part restée acide",
     "exemple_chiffre": "C = 1,0·10⁻², τ = 0,0389 → K = 1,57·10⁻⁵",
     "piege": "[AH]éq = C ; τ arrondi trop tôt",
     "verification": "2022 R : C_b = 1,0·10⁻², τ = 0,20 → Qr,éq ? (5,0·10⁻⁴)"},
    {"id": "tau_k_c", "notion": "τ dépend de K et de C ; K ne dépend pas de C",
     "pourquoi_difficile": "deux grandeurs proches (τ et K) qui ne réagissent pas pareil à la dilution",
     "prerequis": ["logarithme_decimal_puissances"],
     "marches": [
        {"n": 1, "idee": "même K, C ↓ → τ ↑", "vu": "trois barres qui montent, trois K égales", "phrase": "diluer augmente τ", "question": "τ ?"},
        {"n": 2, "idee": "même C, K ↑ → τ ↑", "vu": "deux acides", "phrase": "la nature de la réaction compte", "question": "lequel ?"},
        {"n": 3, "idee": "les deux à la fois", "vu": "deux courbes, poignée C", "phrase": "τ dépend de K et de C", "question": "où τ est-il proche de 1 ?"}],
     "image_mentale": "le salaire (K) est fixé par le métier ; ce qu'on en garde à la fin du mois (τ) dépend aussi de la famille (C)",
     "exemple_chiffre": "C = 1,0·10⁻² → 1,0·10⁻³ : τ 0,039 → 0,117 ; K reste 1,6·10⁻⁵",
     "piege": "« K augmente quand on dilue »",
     "verification": "2025 R (chapitre précédent) : τ passe de 0,06 à 0,20 après dilution ; K ? (inchangée)"},
]

QUESTIONS_ELEVES = [
    {"question": "Pourquoi l'eau n'est pas dans Qr ?", "reponse": "Parce que c'est le solvant : il y en a énormément et sa quantité ne change presque pas. On n'écrit que les espèces dissoutes."},
    {"question": "Qr et K, c'est la même chose ?", "reponse": "Non. Qr change pendant la réaction ; K est la valeur que prend Qr à l'équilibre : K = Qr,éq."},
    {"question": "Pourquoi K n'a pas d'unité alors qu'on divise des mol/L ?", "reponse": "Par convention, on écrit les concentrations en mol/L et on garde seulement leur valeur : Qr et K sont sans unité."},
    {"question": "Si on chauffe, K change ?", "reponse": "Oui, K dépend de la température ; c'est la seule chose qui la change. Les sujets donnent K à 25 °C."},
    {"question": "Si K est fixe, pourquoi τ change quand on dilue ?", "reponse": "Parce que τ dépend aussi de la concentration : K = C·τ²/(1 − τ) ; si C baisse avec K fixe, τ doit augmenter."},
    {"question": "À quoi sert Qr,i ?", "reponse": "Ici, à décrire l'état initial. Au semestre 2 (piles), on le comparera à K pour savoir dans quel sens la réaction va."},
]

COMMENTAIRES = [
    {"plainte": "je mets l'eau ou le métal dans Qr", "vu": "piles 2017 N, 2018 R, 2019 R ; acide + eau partout", "reponse_du_cours": "q3 (eau barrée), q4 (solides barrés), n4 ; rappels C1"},
    {"plainte": "je ne sais pas démontrer K = C·τ²/(1 − τ)", "vu": "2019 N, 2020 R, 2021 N, 2022 R", "reponse_du_cours": "k5 (démonstration pas à pas), n2, n6 ; notion k_c_tau ; rappels C5"},
    {"plainte": "je confonds Qr, Qr,i, Qr,éq et K", "vu": "corrigés (Qr,éq et K pour le même nombre)", "reponse_du_cours": "i1, i3 (Qr qui monte puis s'arrête), e2, k3 (K = Qr,éq) ; rappels C2, C4"},
    {"plainte": "pourquoi K ne change pas alors que les concentrations changent", "vu": "admis du programme", "reponse_du_cours": "k1 (trois concentrations), k2 (départ par les produits), f4 ; notion k_constante"},
    {"plainte": "pour un mélange, je ne sais pas quelles concentrations prendre", "vu": "2020 R", "reponse_du_cours": "i2 (V_T se simplifie), n3 ; rappels C2"},
]

COURS_EXISTANT = {
    "fichier": None,
    "constat": ("aucun ancien cours de ce chapitre dans backend/data/courses/ (vérifié le 12/11/2026 : en chimie seulement "
                "chem_ch1_kinetics_course_v1, phys_ch9, phys_ch10 et phys_ch11 ; aucun fichier ne contient « quotient de réaction » pour la "
                "chimie) ; le cours est écrit à partir de zéro ; le cours précédent phys_ch11_transformations_deux_sens fournit les rappels (r1, r2)"),
    "a_garder": ["de phys_ch11 : exemple A (acide éthanoïque, pH 3,4 au dixième), exemple E (éthanoate + acide chlorhydrique), conductivités molaires ioniques"],
    "images": [],
    "a_corriger": [],
    "a_ajouter": ["tout le chapitre"],
    "a_retirer": [],
    "simulations_a_recreer": [{"ancienne": "/media/simulations/chimie/labs/equilibres/index.html",
                               "idee": "laboratoire « Équilibres en solution » (onglet « Qᵣ / K » : prévoir le sens en comparant Qᵣ,i à K ; dosage ; précipitation)",
                               "nouvelle": ("frontend/public/media/simulations/chimie/etat-equilibre-tableau/ (rappel, quotient, equilibre, constante, "
                                            "conductimetrie, facteurs, figures, bilan, carte) d'après le contrat ; ancienne simulation NON reprise "
                                            "(règle du 9 novembre 2026 ; elle compare Qr,i à K pour le sens, ce qui est au semestre 2)")}],
}

VISUELS = {
    "_note": ("Simulations à la craie du contrat outils/cours/notes/cours/etat_equilibre_contrat_simulations.md, dossier "
              "frontend/public/media/simulations/chimie/etat-equilibre-tableau/ (kit commun.js, exposants.js, ee.css ; moteur des pages "
              "de transformations-deux-sens-tableau, déjà corrigé : durée d'une étape en plusieurs morceaux = Math.max) ; vues par ?vue=, "
              "moments nommés, repères, ce_qui_se_voit. figures.html?fig=fig_2017R dessine la figure du national d'après "
              "etat_equilibre_build/nationaux.md § 5."),
    "v_carte": "carte.html : centre « à l'équilibre : Qr,éq = K » ; branches rappel, quotient, etat_initial, equilibre, constante, inverse, mesures, facteurs, national, suite",
    "v_rappel": "rappel.html?vue=ouverture|taux|equilibre",
    "v_quotient": "quotient.html?vue=definition|generale|eau|solides|sans_unite|initial|melange|au_cours|national|pile",
    "v_equilibre": "equilibre.html?vue=concentrations|qr_eq|expression|national_2017|base|national_2021",
    "v_constante": "constante.html?vue=trois_c|produits|definition|inverse|c_tau|autre_acide",
    "v_conductimetrie": "conductimetrie.html?vue=relation|calcul|national",
    "v_facteurs": "facteurs.html?vue=dilution|nature|courbe|bilan_dilution",
    "v_figures": "figures.html?fig=fig_2017R",
    "v_bilan": "bilan.html : fiche « Ce qu'il faut retenir » (blocs), page 2 de l'élève",
    "manip_labo_3d": "à proposer (skill labo-virtuel-2bac) : mesurer au pH-mètre (au centième) trois solutions d'acide éthanoïque de concentrations différentes et calculer Qr,éq (EE3, EE4, EE6) ; réutiliser la manip pH-mètre du chapitre précédent si elle existe",
}

REGLES_SIMULATIONS = ("règles communes du contrat : fond transparent, un seul bouton, rien hors du cadre 760 × 420 ; solutions peintes, craie pour "
                      "le texte ; fractions avec barre dessinée, exposants, indices et charges rendus ; flèches → ← ⇌ dessinées ; virgule décimale ; "
                      "pH au centième ; Qr, K, τ sans unité ; jamais de terme hors cadre à l'écran ; moments EXACTS du contrat, play_until, "
                      "set_time, set_parameters, highlight ; ce_qui_se_voit dit l'étape et les valeurs affichées ; moteur de "
                      "transformations-deux-sens-tableau (Math.max)")

REDACTION = {
    "_note": "lignes attendues d'après les corrigés du dépôt (erreurs du dépôt relevées dans etat_equilibre_build/nationaux.md § 4)",
    "ecrire_qr": ["équation avec ⇌", "eau solvant et solides barrés", "Qr = [produits]^coef/[réactifs]^coef"],
    "qr_eq_par_ph": ["Qr,éq = [A⁻]éq·[H₃O⁺]éq/[AH]éq", "[A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; [AH]éq = C − 10^(−pH)",
                     "Qr,éq = 10^(−2pH)/(C − 10^(−pH))", "application numérique", "résultat sans unité"],
    "k_par_tau": ["[A⁻]éq = [H₃O⁺]éq = C·τ (tableau)", "[AH]éq = C(1 − τ)", "K = C·τ²/(1 − τ)", "application numérique (C en mol/L)"],
    "qr_i_melange": ["n(X) = C·V pour chaque solution", "[X]ᵢ = n(X)/V_T", "Qr,i ; V_T se simplifie", "valeur"],
    "qr_i_pile": ["équation", "solides absents", "Qr,i = [ion produit]ᵢ^c/[ion réactif]ᵢ^a", "valeur"],
}

RENVOIS = {
    "au_chapitre_precedent": "transformations dans les deux sens : τ = 10^(−pH)/C, tableau, équilibre dynamique, conductimétrie (rappelés en r1, r2, m2)",
    "au_chapitre_suivant": "réactions acide-base : Ka = K de la réaction d'un acide avec l'eau, pKa, Ke, K = Ka₁/Ka₂, prédominance (2017 N 1.3, 2019 N 3.4-3.6, 2020 N 2.5, 2020 R 2.2, 2021 N 2.4, 2022 N 1.4, 2022 R 1.5, 2023 N 2.2, 2016 N, 2024 N, 2025 N)",
    "au_semestre_2_piles": "comparer Qr,i à K pour prévoir le sens d'évolution (2017 N I.2, 2018 R I.2, 2019 R I.1, 2020 R 2.4) ; perimetre.json clé piles_electrolyse",
    "au_semestre_2_esterification": "K d'une estérification ou d'une hydrolyse, rendement, excès d'un réactif (2016 R, 2017 R, 2018 R, 2023 N 3.6) ; n5 seulement comme exemple de K = Qr,éq",
}

DECISIONS = [
    {"question": "Critère d'évolution (Qr,i comparé à K)", "constat": "perimetre.json le place dans piles_electrolyse (CDR sous-domaine 3 « Sens d'évolution »), pas dans acides_bases ; les 4 nationaux qui le demandent l'enchaînent sur une pile ou un mélange (2017 N, 2018 R, 2019 R, 2020 R)", "proposition": "RENVOYÉ au chapitre « évolution spontanée / piles » (semestre 2) ; ici : écrire et calculer Qr,i, voir Qr monter jusqu'à K (i3) sans énoncer la règle ; mots « critère d'évolution spontanée » et « évolution spontanée » mis en hors cadre"},
    {"question": "pH au centième", "constat": "Qr,éq est sensible au pH ; au dixième, trois concentrations donnent 1,46 à 1,81·10⁻⁵ et la constante ne se voit plus ; 2017 N donne pH = 3,41", "proposition": "pH-mètre au centième dans ce chapitre (3,41 ; 3,56 ; 3,93 ; 2,90) ; dire en r1 que c'est le même 3,4 qu'au chapitre précédent"},
    {"question": "Valeur de K de l'acide éthanoïque", "constat": "les mesures donnent 1,56 à 1,61·10⁻⁵ (exemple B) et 1,58·10⁻⁵ (σ)", "proposition": "K = 1,6·10⁻⁵ à 25 °C ; Qr,éq écrits avec 3 chiffres (1,57·10⁻⁵) ; K' = 1/K = 6,25·10⁴"},
    {"question": "Estérification (n5, 2017 R)", "constat": "3 nationaux demandent K d'une estérification / hydrolyse ; l'eau y est un produit (pas le solvant) et figure dans K ; chapitre du semestre 2", "proposition": "garder n5 comme exemple de K = Qr,éq lue sur une courbe, annoncé « étudiée plus tard », avec la phrase « ici l'eau n'est pas le solvant » ; à retirer si l'utilisateur juge que cela trouble la règle de q3"},
    {"question": "Exemples avec des solides (q4, n4)", "constat": "piles au semestre 2, mais 3 nationaux font écrire Qr,i d'une pile ; la règle « solides absents » est de ce chapitre (brief)", "proposition": "q4 (Cu²⁺ + Zn) et n4 (2017 N) gardés pour Qr seulement ; aucune pile expliquée (pas de pont salin, pas de pôles)"},
    {"question": "Base avec l'eau (n2)", "constat": "le τ d'une base passe par Ke (chapitre 13), mais 2022 R donne la question Qr,éq à partir de τ", "proposition": "n2 donne τ = 0,20 comme donnée ; Ke n'est jamais dit"},
    {"question": "Clé perimetre.json", "constat": "pas de clé etat_equilibre : acides_bases couvre les chapitres 11, 12, 13", "proposition": "exploration etat_equilibre.json (clé de programme_semestre1.json) ; perimetre.json NON modifié"},
    {"question": "Durée, découpage, identifiant", "constat": "36 diapositives, 3 séances, programme_semestre1.json ordre 12 statut a_explorer", "proposition": "120 min ; préfixe ee_ ; cours phys_ch12_etat_equilibre ; statut à passer à « explore » après validation"},
]

LIMITES = [
    "vidéos non auditées (YouTube bloqué depuis le cloud, yt-dlp non tenté) : 10 audits à faire depuis le PC avant validation",
    "texte officiel du cadre de référence non relu en entier : EE1-EE7 provisoires (appuyés sur perimetre.json et les nationaux)",
    "exemples A à K du contrat : pH « mesurés » au centième choisis pour être réalistes (K = 1,6·10⁻⁵ pour l'acide éthanoïque, 1,8·10⁻⁴ pour l'acide méthanoïque) et vérifiés avec python (explo.py)",
    "fig_2017R : points relevés à l'œil sur la figure du dépôt (quadrillage coupé vers 0,5 mol, départ 0,6 mol prolongé)",
]
