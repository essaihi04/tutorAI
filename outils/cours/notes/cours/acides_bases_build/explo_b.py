"""Exploration acides_bases, partie B : plan (séances, parties, compétences, 48 diapositives), notions, visuels, décisions.
Importé par explo.py. Ids des diapositives et vues = contrat outils/cours/notes/cours/acides_bases_contrat_simulations.md."""

SEANCES = [
    {"n": 1, "titre": "L'eau, le produit ionique Ke et le pH d'une base",
     "blocs": [["o1", "o2", "r1", "r2"], ["w1", "w2", "w3", "w4"], ["w5", "b1", "b2", "b3"]],
     "parties": [
         {"id": "ab_partie0", "titre": "Ouverture", "ids": ["o1", "o2"]},
         {"id": "ab_partie1", "titre": "I. Rappels : couples acide/base, pH, constante d'équilibre", "ids": ["r1", "r2"]},
         {"id": "ab_partie2", "titre": "II. L'autoprotolyse de l'eau et le produit ionique Ke", "ids": ["w1", "w2", "w3", "w4", "w5"]},
         {"id": "ab_partie3", "titre": "III. Une base dans l'eau : pH et taux d'avancement final", "ids": ["b1", "b2", "b3"]},
     ]},
    {"n": 2, "titre": "Constante d'acidité Ka, pKa et constante d'une réaction acide-base",
     "blocs": [["a1", "a2", "a3", "a4"], ["a5", "c1", "c2", "c3"], ["k1", "k2", "k3", "k4"]],
     "parties": [
         {"id": "ab_partie4", "titre": "IV. La constante d'acidité Ka et le pKa", "ids": ["a1", "a2", "a3", "a4", "a5"]},
         {"id": "ab_partie5", "titre": "V. Comparer des acides et des bases", "ids": ["c1", "c2", "c3"]},
         {"id": "ab_partie6", "titre": "VI. La constante d'équilibre d'une réaction acide-base", "ids": ["k1", "k2", "k3", "k4"]},
     ]},
    {"n": 3, "titre": "Prédominance, indicateurs colorés et dosage acido-basique",
     "blocs": [["p1", "p2", "p3", "p4"], ["i1", "i2", "d1", "d2"], ["d3", "d4", "d5", "d6"]],
     "parties": [
         {"id": "ab_partie7", "titre": "VII. Domaines de prédominance et diagramme de distribution", "ids": ["p1", "p2", "p3", "p4"]},
         {"id": "ab_partie8", "titre": "VIII. Les indicateurs colorés", "ids": ["i1", "i2"]},
         {"id": "ab_partie9", "titre": "IX. Le dosage acido-basique : réaction, équivalence, courbe", "ids": ["d1", "d2", "d3", "d4", "d5", "d6"]},
     ]},
    {"n": 4, "titre": "Exploiter un dosage, sujets du national, bilan",
     "blocs": [["e1", "e2", "e3", "e4"], ["e5", "n1", "n2", "n3"], ["n4", "n5", "bl", "cr"]],
     "parties": [
         {"id": "ab_partie10", "titre": "X. Exploiter une courbe de dosage", "ids": ["e1", "e2", "e3", "e4", "e5"]},
         {"id": "ab_partie11", "titre": "XI. Sujets du national", "ids": ["n1", "n2", "n3", "n4", "n5"]},
         {"id": "ab_bilan", "titre": "XII. Bilan du chapitre", "ids": ["bl", "cr"]},
     ]},
]

def R(id, type, prompt, **kw):
    d = {"id": id, "type": type, "prompt": prompt}
    d.update(kw)
    return d

COMPETENCES = [
    {"id": "C1", "verbe": "Écrire l'autoprotolyse de l'eau, utiliser Ke = [H₃O⁺]·[HO⁻] = 1,0·10⁻¹⁴ (25 °C) et pKe = 14, reconnaître une solution acide, neutre ou basique et calculer [HO⁻] = Ke/[H₃O⁺]",
     "cadre_ids": ["AB1"], "dit": "le produit ionique de l'eau", "rappels": [
        R("C1_r1", "qcm", "À 25 °C, une solution a un pH = 3,41. Elle est :", options=["neutre", "acide", "basique"], correct=1),
        R("C1_r2", "libre", "Écris l'équation de l'autoprotolyse de l'eau et l'expression de Ke.", attendu="2H₂O ⇌ H₃O⁺ + HO⁻ ; Ke = [H₃O⁺]·[HO⁻] = 1,0·10⁻¹⁴ à 25 °C"),
        R("C1_r3", "vrai_faux", "Dans une solution de pH = 3,41, [HO⁻] = 10^(−3,41) mol/L.", correct=False),
        R("C1_r4", "libre", "pH = 3,41 : calcule [HO⁻].", attendu="[HO⁻] = Ke/[H₃O⁺] = 1,0·10⁻¹⁴/3,89·10⁻⁴ = 2,57·10⁻¹¹ mol/L"),
    ]},
    {"id": "C2", "verbe": "Calculer le pH d'une solution basique et le taux d'avancement final de la réaction d'une base avec l'eau à partir de son pH (par Ke)",
     "cadre_ids": ["AB2"], "dit": "le pH et le taux d'avancement d'une base", "rappels": [
        R("C2_r1", "qcm", "Soude à 1,0·10⁻² mol/L. Son pH vaut :", options=["2,0", "7,0", "12,0"], correct=2),
        R("C2_r2", "libre", "Ammoniac C = 1,0·10⁻² mol/L, pH = 10,60. Calcule τ.", attendu="[HO⁻]_éq = 10^(10,60 − 14) = 3,98·10⁻⁴ mol/L ; τ = [HO⁻]_éq/C = 0,040"),
        R("C2_r3", "vrai_faux", "Pour une base dans l'eau, τ = [HO⁻]_éq/C.", correct=True),
    ]},
    {"id": "C3", "verbe": "Écrire la constante d'acidité Ka d'un couple, définir pKa = −log Ka, calculer Ka ou pKa à partir d'une mesure (Ka = Qr,éq ; Ka = Ke/Qr,éq pour une base) et connaître les pKa des couples de l'eau",
     "cadre_ids": ["AB3"], "dit": "la constante d'acidité et le p K a", "rappels": [
        R("C3_r1", "libre", "Écris Ka du couple CH₃COOH/CH₃COO⁻.", attendu="Ka = [CH₃COO⁻]_éq·[H₃O⁺]_éq/[CH₃COOH]_éq"),
        R("C3_r2", "qcm", "Qr,éq de l'acide éthanoïque avec l'eau = 1,57·10⁻⁵. Son pKa vaut :", options=["4,8", "−4,8", "1,57"], correct=0),
        R("C3_r3", "qcm", "NH₃ + H₂O ⇌ NH₄⁺ + HO⁻ a Qr,éq = 1,65·10⁻⁵. Ka(NH₄⁺/NH₃) vaut :", options=["1,65·10⁻⁵", "6,06·10⁻¹⁰", "1,65·10⁻¹⁹"], correct=1),
        R("C3_r4", "vrai_faux", "pKa(H₂O/HO⁻) = 14.", correct=True),
    ]},
    {"id": "C4", "verbe": "Comparer deux acides (ou deux bases) de même concentration à l'aide de Ka ou pKa (τ, pH) et classer des couples sur un axe des pKa",
     "cadre_ids": ["AB4"], "dit": "comparer des acides et des bases", "rappels": [
        R("C4_r1", "qcm", "Même C : acide éthanoïque (pKa 4,8) et acide méthanoïque (pKa 3,75). Le plus petit pH est celui de :",
          options=["l'acide éthanoïque", "l'acide méthanoïque", "les deux sont égaux"], correct=1),
        R("C4_r2", "vrai_faux", "Plus le pKa du couple est grand, plus la base du couple est forte.", correct=True),
        R("C4_r3", "libre", "Classe par force croissante les acides : CH₃COOH (4,8), HCOOH (3,75), NH₄⁺ (9,2).", attendu="NH₄⁺ < CH₃COOH < HCOOH (le pKa diminue)"),
    ]},
    {"id": "C5", "verbe": "Exprimer la constante d'équilibre d'une réaction acide-base avec les Ka des deux couples : K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁) ; K = Ka/Ke pour la réaction avec HO⁻",
     "cadre_ids": ["AB5"], "dit": "la constante d'une réaction acide-base", "rappels": [
        R("C5_r1", "libre", "Montre que K = Ka₁/Ka₂ pour AH₁ + A₂⁻ ⇌ A₁⁻ + AH₂.", attendu="K = [A₁⁻]·[AH₂]/([AH₁]·[A₂⁻]) ; on multiplie en haut et en bas par [H₃O⁺] : K = Ka₁/Ka₂"),
        R("C5_r2", "qcm", "HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH (pKa 3,75 et 4,8). K vaut :", options=["11", "8,9·10⁻²", "1,05"], correct=0),
        R("C5_r3", "vrai_faux", "La réaction CH₃COOH + HO⁻ → CH₃COO⁻ + H₂O a K = Ka/Ke = 1,6·10⁹ : elle est pratiquement totale.", correct=True),
    ]},
    {"id": "C6", "verbe": "Établir pH = pKa + log([A⁻]_éq/[AH]_éq), trouver l'espèce qui prédomine, exploiter un diagramme de distribution et expliquer un indicateur coloré (zone de virage)",
     "cadre_ids": ["AB6", "AB7"], "dit": "la prédominance et les indicateurs colorés", "rappels": [
        R("C6_r1", "qcm", "Acide éthanoïque (pKa 4,8) dans une solution de pH 3,41 : qui prédomine ?", options=["CH₃COOH", "CH₃COO⁻", "aucun"], correct=0),
        R("C6_r2", "libre", "Établis pH = pKa + log([A⁻]_éq/[AH]_éq).", attendu="on prend −log de Ka = [A⁻]·[H₃O⁺]/[AH] : pKa = pH − log([A⁻]/[AH])"),
        R("C6_r3", "vrai_faux", "Sur un diagramme de distribution, les deux courbes se croisent à pH = pKa.", correct=True),
        R("C6_r4", "qcm", "Le BBT (zone de virage 6,0 – 7,6) dans une solution de pH 10,60 est :", options=["jaune", "vert", "bleu"], correct=2),
    ]},
    {"id": "C7", "verbe": "Décrire un dosage acido-basique, écrire la réaction de dosage (rapide, totale, unique), définir l'équivalence et utiliser C_A·V_A = C_B·V_BE (dilution, masse, concentration massique)",
     "cadre_ids": ["AB8"], "dit": "le dosage et l'équivalence", "rappels": [
        R("C7_r1", "libre", "Écris l'équation du dosage de l'acide éthanoïque par la soude.", attendu="CH₃COOH + HO⁻ → CH₃COO⁻ + H₂O"),
        R("C7_r2", "qcm", "V_A = 20,0 mL, C_B = 1,0·10⁻² mol/L, V_BE = 20,0 mL. C_A vaut :", options=["1,0·10⁻² mol/L", "2,0·10⁻² mol/L", "5,0·10⁻³ mol/L"], correct=0),
        R("C7_r3", "vrai_faux", "Une réaction de dosage doit être rapide, totale et unique.", correct=True),
    ]},
    {"id": "C8", "verbe": "Exploiter une courbe de dosage : équivalence par les tangentes parallèles ou la dérivée, nature du pH à l'équivalence, pH = pKa à la demi-équivalence, choix de l'indicateur, courbe σ = f(V)",
     "cadre_ids": ["AB9"], "dit": "exploiter une courbe de dosage", "rappels": [
        R("C8_r1", "qcm", "Dosage de l'acide éthanoïque par la soude : pH_E vaut environ :", options=["7,0", "8,3", "5,7"], correct=1),
        R("C8_r2", "libre", "V_BE = 20,0 mL. Que vaut le pH pour V_B = 10,0 mL (pKa = 4,8) ? Pourquoi ?", attendu="pH = pKa = 4,8 : à la demi-équivalence, [AH] = [A⁻]"),
        R("C8_r3", "vrai_faux", "On choisit l'indicateur dont la zone de virage contient pH_E.", correct=True),
        R("C8_r4", "libre", "Comment lit-on V_BE sur la courbe dérivée dpH/dV_B ?", attendu="V_BE est l'abscisse du maximum de dpH/dV_B"),
    ]},
    {"id": "C9", "verbe": "Rédiger un exercice du national : équation, relation littérale, application numérique avec unité, lecture graphique justifiée, conclusion",
     "cadre_ids": ["AB10"], "dit": "rédiger comme le barème", "rappels": [
        R("C9_r1", "libre", "2016 N : V_A = 5 mL, C_B = 5·10⁻² mol/L, V_BE = 6 mL. Calcule C_A.", attendu="C_A = C_B·V_BE/V_A = 5·10⁻² × 6/5 = 6·10⁻² mol/L"),
        R("C9_r2", "qcm", "2016 N : pH_E = 8,7. Quel indicateur ?", options=["hélianthine (3 – 4,4)", "BBT (6 – 7,6)", "bleu de thymol (8 – 9,6)"], correct=2),
        R("C9_r3", "vrai_faux", "Pour « justifier » un choix d'indicateur, il suffit de donner son nom.", correct=False),
    ]},
]

def D(id, title, lead, marche, visuel, question, prediction, competences, demonstration=()):
    return {"id": id, "title": title, "lead": lead, "marche": marche, "visuel": visuel, "question": question,
            "prediction": prediction, "competences": list(competences), "demonstration": list(demonstration)}

DIAPOS = [
    # Séance 1
    D("o1", "La carte du chapitre : du couple acide/base au dosage", "Que va-t-on savoir faire ?",
      "carte : eau (Ke) → base dans l'eau → constante d'acidité Ka, pKa → comparer → K d'une réaction acide-base → prédominance, indicateur → dosage → exploiter la courbe → national ; « au national : 17 sessions sur 20, un dosage dans 13 »",
      "carte", "Au national, quelle question tombe presque à chaque session dans ce chapitre ?", False, ["C9"]),
    D("o2", "Trois liquides incolores, trois pH", "Même aspect : que contient l'eau ?",
      "trois béchers incolores (vinaigre dilué, eau pure, ammoniac dilué) ; pH-mètre au centième : 3,41 ; 7,00 ; 10,60 ; une goutte de BBT : jaune, vert, bleu ; « même aspect, trois pH : qu'y a-t-il dans l'eau ? »",
      "eau?vue=ouverture", "L'eau pure contient-elle des ions H₃O⁺ ?", True, ["C1"]),
    D("r1", "Rappel : couples acide/base et pH", "Ce qu'on sait déjà.",
      "acide : donneur de proton H⁺ ; base : accepteur ; couple AH/A⁻ ; exemples CH₃COOH/CH₃COO⁻, NH₄⁺/NH₃, H₃O⁺/H₂O, H₂O/HO⁻ ; pH = −log[H₃O⁺] ; pH = 3,41 → [H₃O⁺] = 3,89·10⁻⁴ mol/L",
      "eau?vue=rappel", "Que vaut [H₃O⁺] pour pH = 3,41 ?", False, ["C1"],
      ["[H₃O⁺] = 10^(−pH)", "[H₃O⁺] = 10^(−3,41) = 3,89·10⁻⁴ mol/L"]),
    D("r2", "Rappel : la constante d'équilibre", "Le chapitre précédent, en une ligne.",
      "acide AH dans l'eau : [A⁻]_éq = [H₃O⁺]_éq = C·τ ; [AH]_éq = C·(1 − τ) ; K = C·τ²/(1 − τ) ; K = Qr,éq ne dépend que de la température ; acide éthanoïque K = 1,6·10⁻⁵ ; « et une base dans l'eau ? »",
      "base?vue=constante", "La constante K de l'acide éthanoïque change-t-elle si on dilue ?", False, ["C3"]),
    D("w1", "L'autoprotolyse de l'eau", "Deux molécules d'eau échangent un proton.",
      "loupe : un H⁺ passe d'une molécule H₂O à une autre ; un H₃O⁺ et un HO⁻ apparaissent ; 2H₂O ⇌ H₃O⁺ + HO⁻ ; eau pure : [H₃O⁺] = [HO⁻] = 1,0·10⁻⁷ mol/L (pH 7,00)",
      "eau?vue=autoprotolyse", "Dans l'eau pure, y a-t-il plus d'ions H₃O⁺ que d'ions HO⁻ ?", True, ["C1"]),
    D("w2", "Le produit ionique de l'eau Ke", "Un produit qui ne change pas.",
      "Ke = [H₃O⁺]·[HO⁻] ; eau pure : 1,0·10⁻⁷ × 1,0·10⁻⁷ = 1,0·10⁻¹⁴ ; à 25 °C : Ke = 1,0·10⁻¹⁴ (sans unité) ; pKe = −log Ke = 14 ; vrai dans toute solution aqueuse",
      "eau?vue=ke", "Que vaut Ke à 25 °C ?", False, ["C1"],
      ["Ke = [H₃O⁺]·[HO⁻]", "Ke = 1,0·10⁻⁷ × 1,0·10⁻⁷ = 1,0·10⁻¹⁴", "pKe = −log Ke = 14"]),
    D("w3", "Solution acide, neutre ou basique", "On compare [H₃O⁺] et [HO⁻].",
      "axe des pH ; acide : [H₃O⁺] > [HO⁻], pH < 7 ; neutre : [H₃O⁺] = [HO⁻], pH = 7 ; basique : [HO⁻] > [H₃O⁺], pH > 7 (25 °C) ; poignée pH",
      "eau?vue=solutions", "À pH = 10,60, quelle concentration est la plus grande : [H₃O⁺] ou [HO⁻] ?", True, ["C1"]),
    D("w4", "Calculer [HO⁻] avec Ke", "Le pH donne aussi [HO⁻].",
      "[HO⁻] = Ke/[H₃O⁺] ; pH 3,41 → [HO⁻] = 1,0·10⁻¹⁴/3,89·10⁻⁴ = 2,57·10⁻¹¹ mol/L ; pH 10,60 → [HO⁻] = 10^(pH − 14) = 3,98·10⁻⁴ mol/L ; ⚠ [HO⁻] n'est pas 10^(−pH)",
      "eau?vue=ho", "Calcule [HO⁻] dans la solution d'ammoniac de pH 10,60.", False, ["C1"],
      ["[HO⁻] = Ke/[H₃O⁺]", "[HO⁻] = 10^(pH − 14) = 10^(10,60 − 14) = 3,98·10⁻⁴ mol/L"]),
    D("w5", "Le pH d'une solution de soude", "Une base qui réagit totalement.",
      "soude Na⁺ + HO⁻, C = 1,0·10⁻² mol/L ; [HO⁻] = C = 1,0·10⁻² mol/L ; [H₃O⁺] = Ke/[HO⁻] = 1,0·10⁻¹² mol/L ; pH = 12,00",
      "eau?vue=soude", "Le pH de la soude sera-t-il plus petit ou plus grand que 7 ?", True, ["C2"],
      ["[H₃O⁺] = Ke/[HO⁻] = 1,0·10⁻¹⁴/1,0·10⁻² = 1,0·10⁻¹² mol/L", "pH = −log(1,0·10⁻¹²) = 12,00"]),
    D("b1", "Une base faible dans l'eau : l'ammoniac", "NH₃ capte un proton de l'eau.",
      "ammoniac 1,0·10⁻² mol/L, pH 10,60 ; NH₃ + H₂O ⇌ NH₄⁺ + HO⁻ (l'eau joue l'acide) ; [H₃O⁺]_éq = 2,51·10⁻¹¹ mol/L ; [HO⁻]_éq = Ke/[H₃O⁺]_éq = 3,98·10⁻⁴ mol/L",
      "base?vue=ammoniac", "[HO⁻]_éq sera-t-elle égale à C = 1,0·10⁻² mol/L ?", True, ["C2"],
      ["[HO⁻]_éq = Ke/[H₃O⁺]_éq = 1,0·10⁻¹⁴/2,51·10⁻¹¹ = 3,98·10⁻⁴ mol/L"]),
    D("b2", "Le taux d'avancement final d'une base", "Le tableau, avec HO⁻.",
      "tableau NH₃ · H₂O · NH₄⁺ · HO⁻ ; x_max = C·V ; x_éq = [HO⁻]_éq·V ; τ = [HO⁻]_éq/C = 3,98·10⁻⁴/1,0·10⁻² = 0,040 ; τ < 1 : réaction limitée ; ⚠ pour une base, τ passe par Ke",
      "base?vue=taux", "Calcule τ pour l'ammoniac.", False, ["C2"],
      ["τ = x_éq/x_max = [HO⁻]_éq/C", "τ = 3,98·10⁻⁴/1,0·10⁻² = 0,040"]),
    D("b3", "National 2022 R : la méthylamine", "C_b = 1,0·10⁻² mol/L, pH = 11,30.",
      "CH₃NH₂ + H₂O ⇌ CH₃NH₃⁺ + HO⁻ ; [HO⁻]_éq = 10^(pH − 14) = 2,0·10⁻³ mol/L ; τ = 0,20 (0,5 pt) ; Qr,éq = C·τ²/(1 − τ) = 5,0·10⁻⁴ (1.4, 0,5 pt)",
      "base?vue=national", "Calcule τ pour la méthylamine.", False, ["C2", "C9"],
      ["[HO⁻]_éq = 10^(11,30 − 14) = 2,0·10⁻³ mol/L", "τ = 2,0·10⁻³/1,0·10⁻² = 0,20", "Qr,éq = 1,0·10⁻² × 0,20²/(1 − 0,20) = 5,0·10⁻⁴"]),
    # Séance 2
    D("a1", "La constante d'acidité Ka", "Le K de la réaction d'un acide avec l'eau a un nom.",
      "AH + H₂O ⇌ A⁻ + H₃O⁺ ; constante d'acidité du couple AH/A⁻ : Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq ; ne dépend que de la température ; sans unité",
      "acidite?vue=definition", "Quelles concentrations vont au numérateur de Ka ?", False, ["C3"],
      ["Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq"]),
    D("a2", "Le pKa", "Un nombre plus simple à manier.",
      "pKa = −log Ka ; Ka = 10^(−pKa) ; acide éthanoïque Ka = 1,6·10⁻⁵ → pKa = 4,8 ; acide méthanoïque Ka = 1,8·10⁻⁴ → pKa = 3,75 ; Ka plus grand ⇔ pKa plus petit",
      "acidite?vue=pka", "L'acide qui a le plus grand Ka aura-t-il le plus grand ou le plus petit pKa ?", True, ["C3"],
      ["pKa = −log Ka", "pKa = −log(1,6·10⁻⁵) = 4,8"]),
    D("a3", "Mesurer un pKa avec le pH", "Le pH-mètre affiche 3,41.",
      "acide éthanoïque 1,0·10⁻² mol/L ; Ka = Qr,éq = 10^(−2pH)/(C − 10^(−pH)) = 10^(−6,82)/(1,0·10⁻² − 10^(−3,41)) = 1,57·10⁻⁵ ; pKa = 4,8 ; national 2017 N : acide butanoïque, pKa = 4,8 (0,5 pt)",
      "acidite?vue=mesure", "Calcule le pKa de l'acide éthanoïque.", False, ["C3", "C9"],
      ["Ka = 10^(−6,82)/(1,0·10⁻² − 10^(−3,41)) = 1,57·10⁻⁵", "pKa = −log(1,57·10⁻⁵) = 4,8"]),
    D("a4", "Le Ka du couple d'une base : NH₄⁺/NH₃", "On part de la réaction de NH₃ avec l'eau.",
      "Ka = [NH₃]_éq·[H₃O⁺]_éq/[NH₄⁺]_éq ; NH₃ + H₂O ⇌ NH₄⁺ + HO⁻ : Qr,éq = [NH₄⁺]_éq·[HO⁻]_éq/[NH₃]_éq ; on multiplie en haut et en bas par [H₃O⁺]_éq : Qr,éq = Ke/Ka ; Ka = Ke/Qr,éq = 1,0·10⁻¹⁴/1,65·10⁻⁵ = 6,06·10⁻¹⁰ ; pKa = 9,2 (national 2020 N)",
      "acidite?vue=ammonium", "Ka(NH₄⁺/NH₃) sera-t-il égal à Qr,éq = 1,65·10⁻⁵ ?", True, ["C3"],
      ["Qr,éq = [NH₄⁺]_éq·[HO⁻]_éq/[NH₃]_éq = Ke/Ka", "Ka = Ke/Qr,éq = 1,0·10⁻¹⁴/1,65·10⁻⁵ = 6,06·10⁻¹⁰", "pKa = −log(6,06·10⁻¹⁰) = 9,2"]),
    D("a5", "Les deux couples de l'eau", "L'eau est un acide et une base.",
      "H₃O⁺/H₂O : Ka = 1, pKa(H₃O⁺/H₂O) = 0 ; H₂O/HO⁻ : Ka = [HO⁻]·[H₃O⁺] = Ke, pKa(H₂O/HO⁻) = 14 ; les couples étudiés dans l'eau ont un pKa entre 0 et 14",
      "acidite?vue=eau", "Que vaut le pKa du couple H₂O/HO⁻ ?", False, ["C3"],
      ["pKa(H₃O⁺/H₂O) = 0", "pKa(H₂O/HO⁻) = −log Ke = 14"]),
    D("c1", "Comparer deux acides", "Même concentration, deux pKa.",
      "1,0·10⁻² mol/L : acide éthanoïque (pKa 4,8) pH 3,41, τ = 0,039 ; acide méthanoïque (pKa 3,75) pH 2,90, τ = 0,126 ; même C : plus Ka est grand (pKa petit), plus τ est grand et le pH petit",
      "comparer?vue=acides", "Lequel des deux acides aura le plus petit pH ?", True, ["C4"]),
    D("c2", "Comparer deux bases", "Ammoniac et méthylamine.",
      "1,0·10⁻² mol/L : ammoniac (pKa 9,2) pH 10,60, τ = 0,040 ; méthylamine (pKa 10,7) pH 11,30, τ = 0,20 ; même C : plus le pKa du couple est grand, plus la base est forte",
      "comparer?vue=bases", "Laquelle des deux bases aura le plus grand τ ?", True, ["C4"]),
    D("c3", "Classer les couples sur un axe des pKa", "De 0 à 14.",
      "axe des pKa : H₃O⁺/H₂O (0), HCOOH/HCOO⁻ (3,75), CH₃COOH/CH₃COO⁻ (4,8), NH₄⁺/NH₃ (9,2), CH₃NH₃⁺/CH₃NH₂ (10,7), H₂O/HO⁻ (14) ; acide de plus en plus fort quand le pKa diminue ; base de plus en plus forte quand le pKa augmente",
      "comparer?vue=classement", "Quel est l'acide le plus fort de cette liste ?", False, ["C4"]),
    D("k1", "La constante d'une réaction acide-base", "Deux couples se rencontrent.",
      "AH₁ + A₂⁻ ⇌ A₁⁻ + AH₂ ; K = [A₁⁻]_éq·[AH₂]_éq/([AH₁]_éq·[A₂⁻]_éq) ; on multiplie en haut et en bas par [H₃O⁺]_éq ; K = Ka₁/Ka₂",
      "comparer?vue=reaction", "Montre que K = Ka₁/Ka₂.", False, ["C5"],
      ["K = [A₁⁻]_éq·[AH₂]_éq/([AH₁]_éq·[A₂⁻]_éq)", "K = ([A₁⁻]_éq·[H₃O⁺]_éq/[AH₁]_éq) × ([AH₂]_éq/([A₂⁻]_éq·[H₃O⁺]_éq))", "K = Ka₁/Ka₂"]),
    D("k2", "K avec les pKa", "Une puissance de dix.",
      "K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁) ; HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH : K = 10^(4,8 − 3,75) = 11 ; sens inverse : K = 8,9·10⁻² ; CH₃COOH + NH₃ : K = 10^(9,2 − 4,8) = 2,5·10⁴ ; ⚠ Ka₁ : couple de l'acide qui réagit",
      "comparer?vue=puissance", "La réaction de l'acide méthanoïque avec les ions éthanoate aura-t-elle un K plus grand ou plus petit que 1 ?", True, ["C5"],
      ["K = 10^(pKa₂ − pKa₁)", "K = 10^(4,8 − 3,75) = 11"]),
    D("k3", "Une réaction presque totale : l'acide avec HO⁻", "Préparer le dosage.",
      "CH₃COOH + HO⁻ → CH₃COO⁻ + H₂O ; couple H₂O/HO⁻ : Ka = Ke ; K = Ka/Ke = 10^(14 − 4,8) = 1,6·10⁹ ; K > 10⁴ : réaction pratiquement totale ; elle servira au dosage",
      "comparer?vue=totale", "Cette réaction sera-t-elle limitée ou pratiquement totale ?", True, ["C5", "C7"],
      ["K = Ka/Ke", "K = 10^(−4,8)/10^(−14) = 10^(9,2) = 1,6·10⁹"]),
    D("k4", "National 2020 R : K = 10", "Lire qui est Ka₁ dans le sujet.",
      "HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH ; Ka₁ du sujet : CH₃COOH/CH₃COO⁻ (pKa 4,8) ; Ka₂ : HCOOH/HCOO⁻ (pKa 3,8) ; K = Ka₂/Ka₁ = 10^(4,8 − 3,8) = 10 (0,5 pt) ; la suite (sens) : au semestre 2",
      "comparer?vue=national", "Calcule K.", False, ["C5", "C9"],
      ["K = [HCOO⁻]_éq·[CH₃COOH]_éq/([HCOOH]_éq·[CH₃COO⁻]_éq) = Ka₂/Ka₁", "K = 10^(4,8 − 3,8) = 10"]),
    # Séance 3
    D("p1", "pH et pKa : la relation", "On prend le log de Ka.",
      "Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq ; −log Ka = −log[H₃O⁺]_éq − log([A⁻]_éq/[AH]_éq) ; pH = pKa + log([A⁻]_éq/[AH]_éq) ; [A⁻] = [AH] → pH = pKa = 4,8 ; [A⁻]/[AH] = 10 → pH = 5,8",
      "predominance?vue=relation", "Établis la relation entre pH, pKa et [A⁻]/[AH].", False, ["C6"],
      ["pKa = pH − log([A⁻]_éq/[AH]_éq)", "pH = pKa + log([A⁻]_éq/[AH]_éq)", "pH = 4,8 + log 10 = 5,8"]),
    D("p2", "Les domaines de prédominance", "Qui gagne : l'acide ou la base ?",
      "axe des pH, trait au pKa = 4,8 ; pH < pKa : CH₃COOH prédomine ; pH > pKa : CH₃COO⁻ prédomine ; pH = pKa : [AH] = [A⁻] ; poignée pH",
      "predominance?vue=domaines", "À pH = 3,41, qui prédomine : CH₃COOH ou CH₃COO⁻ ?", True, ["C6"]),
    D("p3", "Le diagramme de distribution", "Les pourcentages de AH et de A⁻.",
      "courbes % CH₃COOH (décroît) et % CH₃COO⁻ (croît) : pH 3,8 → 90,9 % / 9,1 % ; 4,8 → 50 % / 50 % ; 5,8 → 9,1 % / 90,9 % ; croisement à pH = pKa ; poignée pH",
      "predominance?vue=distribution", "Où les deux courbes vont-elles se croiser ?", True, ["C6"]),
    D("p4", "National 2025 R : lire un pKa sur la distribution", "Deux courbes, un croisement.",
      "fig_2025R : croisement à pH = 4,8 → pKa = 4,8 (0,5 pt) ; courbe 1 > 50 % pour pH < pKa : forme acide (0,25 pt) ; pH₁ = 4,2 : 20 % de CH₃COO⁻ → τ₁ = 0,20 (0,5 pt)",
      "figures?fig=fig_2025R", "Quelle courbe correspond à CH₃COOH ? Justifie.", False, ["C6", "C9"],
      ["pH₁ = 4,2 : % CH₃COO⁻ = 20 % → τ₁ = 0,20"]),
    D("i1", "L'indicateur coloré", "Un couple qui change de couleur.",
      "une goutte de BBT dans les trois solutions : jaune (3,41), vert (7,00), bleu (10,60) ; indicateur coloré : couple HInd/Ind⁻ ; HInd et Ind⁻ n'ont pas la même couleur ; BBT : HInd jaune, Ind⁻ bleu",
      "predominance?vue=indicateur", "Dans la solution d'ammoniac, quelle forme du BBT va prédominer ?", True, ["C6"]),
    D("i2", "La zone de virage", "Entre deux couleurs.",
      "BBT : jaune jusqu'à 6,0, vert de 6,0 à 7,6 (zone de virage), bleu après ; pKa(BBT) ≈ 7,0 ; la zone de virage encadre le pKa de l'indicateur ; tableau : hélianthine 3,1 – 4,4 ; rouge de méthyle 4,2 – 6,2 ; BBT 6,0 – 7,6 ; rouge de crésol 7,2 – 8,8",
      "predominance?vue=virage", "Quelle couleur a le BBT à pH = 6,8 ?", False, ["C6"]),
    D("d1", "Le dosage : but et montage", "Trouver une concentration inconnue.",
      "burette (soude, solution titrante) ; bécher de 20,0 mL d'acide éthanoïque (solution titrée) ; agitateur magnétique ; pH-mètre ; but : trouver C_A",
      "dosage?vue=montage", "Quelle solution met-on dans la burette ?", False, ["C7"]),
    D("d2", "La réaction de dosage", "Chaque goutte réagit aussitôt.",
      "CH₃COOH + HO⁻ → CH₃COO⁻ + H₂O ; K = 1,6·10⁹ ; rapide, totale, unique ; flèche simple",
      "dosage?vue=reaction", "Écrira-t-on la réaction de dosage avec une double flèche ?", True, ["C7"]),
    D("d3", "L'équivalence", "Juste assez de base.",
      "tableau : avant (HO⁻ limitant), à l'équivalence (les deux épuisés), après (HO⁻ en excès) ; équivalence : réactifs dans les proportions stœchiométriques ; n(CH₃COOH)_initial = n(HO⁻)_versé ; C_A·V_A = C_B·V_BE ; V_BE = 20,0 mL",
      "dosage?vue=equivalence", "Calcule V_BE pour C_A = C_B = 1,0·10⁻² mol/L et V_A = 20,0 mL.", False, ["C7"],
      ["C_A·V_A = C_B·V_BE", "V_BE = C_A·V_A/C_B = 1,0·10⁻² × 20,0/1,0·10⁻² = 20,0 mL"]),
    D("d4", "La courbe pH = f(V_B)", "Goutte à goutte, le pH monte.",
      "points : 0 → 3,41 ; 5 → 4,34 ; 10 → 4,80 ; 15 → 5,28 ; 19 → 6,08 ; 20 → 8,25 ; 21 → 10,39 ; 30 → 11,30 ; trois zones : montée douce, saut de pH, palier ; poignée V_B",
      "dosage?vue=courbe", "Près de V_B = 20 mL, le pH va-t-il monter doucement ou d'un coup ?", True, ["C8"]),
    D("d5", "La méthode des tangentes parallèles", "Trouver E sur la courbe.",
      "deux tangentes parallèles de part et d'autre du saut ; leur parallèle équidistante coupe la courbe en E ; V_BE = 20,0 mL ; pH_E = 8,3",
      "dosage?vue=tangentes", "Où la parallèle du milieu coupe-t-elle la courbe ?", False, ["C8"]),
    D("d6", "La courbe dérivée dpH/dV_B", "Un pic à l'équivalence.",
      "dpH/dV_B presque nulle puis un pic fin à 20,0 mL ; V_BE = abscisse du maximum de dpH/dV_B ; utilisée en 2021 R, 2022 N, 2024 N",
      "dosage?vue=derivee", "À quel volume la courbe dpH/dV_B a-t-elle son maximum ?", False, ["C8"]),
    # Séance 4
    D("e1", "Le pH à l'équivalence : 7, plus ou moins", "Trois dosages, trois pH_E.",
      "acide chlorhydrique + soude : pH_E = 7,0 ; acide éthanoïque + soude : pH_E = 8,3 > 7 (CH₃COO⁻ est une base) ; ammoniac + acide chlorhydrique : pH_E = 5,7 < 7 (NH₄⁺ est un acide)",
      "exploiter?vue=trois_courbes", "Pour l'acide éthanoïque dosé par la soude, pH_E sera-t-il égal à 7 ?", True, ["C8"]),
    D("e2", "La demi-équivalence : pH = pKa", "À V_BE/2, autant d'acide que de base.",
      "V_B = V_BE/2 = 10,0 mL ; n(CH₃COOH) = n(CH₃COO⁻) = 1,0·10⁻⁴ mol ; [AH] = [A⁻] ; pH = pKa + log 1 ; pH = pKa à V_B = V_BE/2 ; lecture : pH = 4,8",
      "exploiter?vue=demi", "À V_B = 10,0 mL, que vaudra le pH ?", True, ["C8"],
      ["n(CH₃COO⁻) = C_B·V_B = 1,0·10⁻² × 10,0·10⁻³ = 1,0·10⁻⁴ mol", "n(CH₃COOH) = 2,0·10⁻⁴ − 1,0·10⁻⁴ = 1,0·10⁻⁴ mol",
       "pH = pKa + log 1 = pKa = 4,8"]),
    D("e3", "Choisir l'indicateur coloré", "Sa zone de virage doit contenir pH_E.",
      "pH_E = 8,3 ; rouge de crésol (7,2 – 8,8) contient 8,3 ; ⚠ le BBT vire avant le saut ; la couleur change à la goutte de l'équivalence",
      "exploiter?vue=indicateur", "Quel indicateur choisis-tu pour ce dosage ? Justifie.", False, ["C8", "C6"]),
    D("e4", "Doser une base par un acide", "L'ammoniac et l'acide chlorhydrique.",
      "NH₃ + H₃O⁺ → NH₄⁺ + H₂O ; C_B·V_B = C_A·V_AE → V_AE = 20,0 mL ; la courbe descend ; E (20,0 mL ; 5,7) ; demi-équivalence : pH = 9,2 = pKa(NH₄⁺/NH₃) ; rouge de méthyle",
      "exploiter?vue=base", "Ici, pH_E sera-t-il plus grand ou plus petit que 7 ?", True, ["C8"],
      ["C_B·V_B = C_A·V_AE", "V_AE = 1,0·10⁻² × 20,0/1,0·10⁻² = 20,0 mL"]),
    D("e5", "Le dosage conductimétrique", "Une autre façon de trouver l'équivalence.",
      "acide chlorhydrique dilué, soude 1,0·10⁻¹ mol/L ; σ (mS/m) : 38,8 → 11,4 (à 2,0 mL) → 33,5 (à 4,0 mL) ; avant E, H₃O⁺ remplacé par Na⁺ : σ diminue ; après E, Na⁺ et HO⁻ s'ajoutent : σ augmente ; rupture de pente : V_BE = 2,0 mL ; C_A = 1,0·10⁻² mol/L",
      "exploiter?vue=conductimetrie", "Avant l'équivalence, σ va-t-elle augmenter ou diminuer ?", True, ["C7"],
      ["C_A = C_B·V_BE/V_A = 1,0·10⁻¹ × 2,0/20,0 = 1,0·10⁻² mol/L"]),
    D("n1", "National 2016 N : tangentes et indicateur", "Acide propanoïque dosé par la soude.",
      "fig_2016N : tangentes → V_BE = 6 mL, pH_E = 8,7 (0,5) ; C_A = 5·10⁻² × 6/5 = 6·10⁻² mol/L (0,5) ; K = Ka/Ke = 1,26·10⁹ : totale (0,5) ; bleu de thymol (0,5) ; à 7 mL, pH = 11,6 > pKa : C₂H₅COO⁻ prédomine (0,5)",
      "figures?fig=fig_2016N", "Calcule C_A, puis choisis l'indicateur.", False, ["C7", "C9"],
      ["C_A = C_B·V_BE/V_A = 5·10⁻² × 6/5 = 6·10⁻² mol/L", "K = Ka/Ke = 10^(−4,9)/10^(−14) = 1,26·10⁹"]),
    D("n2", "National 2022 R : doser la méthylamine", "Une base dosée par un acide.",
      "fig_2022R : CH₃NH₂ + H₃O⁺ → CH₃NH₃⁺ + H₂O ; E (15 mL ; 6,6) ; C_b = 10⁻² × 15/15 = 10⁻² mol/L ; BBT (6,0 – 7,6) ; à 20,4 mL, pH = 2,8 : [CH₃NH₂]/[CH₃NH₃⁺] = 10^(2,8 − 10,7) = 1,26·10⁻⁸ (0,75 pt)",
      "figures?fig=fig_2022R", "pH_E sera-t-il plus petit ou plus grand que 7 ?", True, ["C8", "C9"],
      ["C_b = C_a·V_aE/V_b = 10⁻² × 15/15 = 10⁻² mol/L", "[CH₃NH₂]/[CH₃NH₃⁺] = 10^(pH − pKa) = 10^(2,8 − 10,7) = 1,26·10⁻⁸"]),
    D("n3", "National 2022 N : la dérivée et le pourcentage", "Acide propanoïque, C_b = 5·10⁻² mol/L.",
      "fig_2022N : maximum de dpH/dV_b → V_bE = 20 mL (0,25) ; C_a = 5·10⁻² mol/L (0,5) ; à V_b = 5 mL, pH = 4,4 : [A⁻]/[AH] = 10^(4,4 − 4,9) = 0,316 → % forme acide = 1/(1 + 0,316) = 76 % (0,5)",
      "figures?fig=fig_2022N", "Calcule le pourcentage de forme acide à V_b = 5 mL.", False, ["C8", "C9"],
      ["[A⁻]/[AH] = 10^(4,4 − 4,9) = 0,316", "% AH = 1/(1 + 0,316) = 0,76 = 76 %"]),
    D("n4", "National 2024 R : distribution d'une amine", "pKa lu au croisement.",
      "fig_2024R : croisement à pH = 10,8 → pKa = 10,8 (0,5) ; pH = 11,88 > pKa : R–NH₂ prédomine (0,5) ; 80 % d'acide : [base]/[acide] = 0,25 → pH = 10,8 + log 0,25 = 10,2 (0,75)",
      "figures?fig=fig_2024R", "Dans la solution de pH 11,88, quelle forme va prédominer ?", True, ["C6", "C9"],
      ["[base]/[acide] = 20/80 = 0,25", "pH = 10,8 + log 0,25 = 10,2"]),
    D("n5", "National 2023 R : la demi-équivalence", "Triméthylamine dans l'urine.",
      "V_B = 20 mL, C_A = 4·10⁻² mol/L ; E (20 mL ; 5,8), Q (10 mL ; 9,9) ; C_B = 4·10⁻² mol/L ; C₀ = 0,4 mol/L (dilution 10) ; pH_E < 7 ; rouge de méthyle ; à V_A = V_AE/2 : [(CH₃)₃NH⁺] = [(CH₃)₃N] → pKa = 9,9 (3,25 pts)",
      "exploiter?vue=national_2023", "Déduis le pKa du couple à partir du point Q.", False, ["C8", "C9"],
      ["C_B = C_A·V_AE/V_B = 4·10⁻² × 20/20 = 4·10⁻² mol/L", "V_A = V_AE/2 : [(CH₃)₃NH⁺] = [(CH₃)₃N] → pH = pKa = 9,9"]),
    D("bl", "Ce qu'il faut retenir", "La fiche du chapitre.",
      "blocs : eau, base, acidité, comparer, réaction, prédominance, dosage, exploiter, rédaction ; page 2 : tes lacunes",
      "bilan", "Quelle ligne de la fiche te paraît la plus difficile ?", False, ["C9"]),
    D("cr", "La carte complète", "Tout le chapitre d'un coup d'œil.",
      "carte complète ; suite : semestre 2 (piles, électrolyse, estérification)",
      "carte", "Par quelle branche commencerais-tu un exercice de dosage ?", False, ["C9"]),
]

PLAN = {
    "principes": ("une idée nouvelle par diapositive ; une chose vue, une phrase, une question ; exemples A à N du contrat pour voir (trois "
                  "solutions au pH-mètre et au BBT, eau pure, soude, ammoniac, deux acides et deux bases de même C, courbes de dosage calculées, "
                  "distribution) ; dix nationaux pour s'entraîner ; chaque bloc a au moins une prédiction ; le dosage (clé dosage de "
                  "perimetre.json) est la partie finale de ce cours (séances 3 et 4) ; la comparaison de Qr,i à K (sens) renvoyée aux piles"),
    "duree_estimee_min": 160,
    "decoupage_conseille": "quatre séances de trois blocs de quatre diapositives (bilan et carte dans le dernier bloc)",
    "prefixe_diapositives": "ab_",
    "parties_pour_les_agents": ("une séance par agent (p1.py = séance 1, p2.py = séance 2, p3.py = séance 3, p4.py = séance 4) ; titres et ids "
                                "des parties dans seances[n].parties ; id de diapositive = ab_<id du plan>_<un mot>"),
    "prerequis_verifies_au_debut": ["logarithme_decimal_puissances", "puissances_dix_unites", "tableau_avancement", "concentration_quantite_matiere",
                                    "acide_base_bronsted_ph", "conductimetrie"],
    "seances": SEANCES,
    "competences": COMPETENCES,
    "diapositives": DIAPOS,
}

NOTIONS = [
    {"id": "ke", "notion": "Ke = [H₃O⁺]·[HO⁻] = 1,0·10⁻¹⁴ dans toute solution aqueuse à 25 °C",
     "pourquoi_difficile": "l'élève croit qu'une solution acide n'a pas d'ions HO⁻ ; il calcule [HO⁻] avec 10^(−pH)",
     "prerequis": ["logarithme_decimal_puissances", "puissances_dix_unites"],
     "marches": [
        {"n": 1, "idee": "l'eau pure contient des ions", "vu": "pH 7,00, BBT vert, loupe", "phrase": "deux molécules d'eau échangent un proton", "question": "y a-t-il des ions ?"},
        {"n": 2, "idee": "le produit est constant", "vu": "1,0·10⁻⁷ × 1,0·10⁻⁷", "phrase": "Ke = 1,0·10⁻¹⁴ à 25 °C", "question": "Ke ?"},
        {"n": 3, "idee": "acide / neutre / basique", "vu": "barres [H₃O⁺] et [HO⁻] sur l'axe des pH", "phrase": "on compare les deux concentrations", "question": "pH 10,60 ?"},
        {"n": 4, "idee": "[HO⁻] = Ke/[H₃O⁺]", "vu": "calcul pour pH 3,41 et 10,60", "phrase": "le pH donne aussi [HO⁻]", "question": "[HO⁻] ?"}],
     "image_mentale": "une balançoire : quand [H₃O⁺] monte, [HO⁻] descend, et leur produit reste 10⁻¹⁴",
     "exemple_chiffre": "pH 10,60 → [HO⁻] = 10^(10,60 − 14) = 3,98·10⁻⁴ mol/L",
     "piege": "[HO⁻] = 10^(−pH)",
     "verification": "soude 1,0·10⁻² mol/L : pH ? (12,00)"},
    {"id": "ka_pka", "notion": "Ka = K de la réaction de l'acide avec l'eau ; pKa = −log Ka ; Ka = Ke/Qr,éq pour une base",
     "pourquoi_difficile": "un nouveau nom pour une constante déjà vue ; le couple d'une base se lit à l'envers",
     "prerequis": ["logarithme_decimal_puissances", "acide_base_bronsted_ph"],
     "marches": [
        {"n": 1, "idee": "Ka = K", "vu": "1,57·10⁻⁵ du chapitre précédent", "phrase": "la constante de AH + H₂O a un nom", "question": "Ka ?"},
        {"n": 2, "idee": "pKa", "vu": "−log 1,6·10⁻⁵ = 4,8", "phrase": "Ka grand, pKa petit", "question": "pKa ?"},
        {"n": 3, "idee": "couple d'une base", "vu": "multiplier par [H₃O⁺]", "phrase": "Qr,éq = Ke/Ka", "question": "Ka(NH₄⁺/NH₃) ?"},
        {"n": 4, "idee": "les couples de l'eau", "vu": "0 et 14 aux bouts de l'axe", "phrase": "tous les pKa entre 0 et 14", "question": "pKa(H₂O/HO⁻) ?"}],
     "image_mentale": "la carte d'identité du couple : chaque couple a son pKa, comme chaque personne sa date de naissance",
     "exemple_chiffre": "Qr,éq(NH₃) = 1,65·10⁻⁵ → Ka = 6,06·10⁻¹⁰ → pKa = 9,2",
     "piege": "pKa = log Ka ; Ka(NH₄⁺/NH₃) = Qr,éq",
     "verification": "2022 R : Qr,éq = 5,0·10⁻⁴ → pKa ? (10,7)"},
    {"id": "k_reaction", "notion": "K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁)",
     "pourquoi_difficile": "quel Ka en haut ? ; la multiplication par [H₃O⁺]/[H₃O⁺] semble « magique »",
     "prerequis": ["logarithme_decimal_puissances"],
     "marches": [
        {"n": 1, "idee": "écrire K", "vu": "quotient de la réaction", "phrase": "produits en haut, réactifs en bas", "question": "K ?"},
        {"n": 2, "idee": "multiplier par [H₃O⁺]", "vu": "deux fractions qui se séparent", "phrase": "on fait apparaître Ka₁ et Ka₂", "question": "laquelle est Ka₁ ?"},
        {"n": 3, "idee": "puissance de dix", "vu": "10^(4,8 − 3,75)", "phrase": "K = 10^(pKa₂ − pKa₁)", "question": "K > 1 ?"},
        {"n": 4, "idee": "avec HO⁻", "vu": "K = 1,6·10⁹", "phrase": "Ka(H₂O/HO⁻) = Ke : réaction totale", "question": "totale ?"}],
     "image_mentale": "un échange de proton entre deux vendeurs : le plus pressé de vendre (l'acide le plus fort) gagne",
     "exemple_chiffre": "HCOOH + CH₃COO⁻ : K = 10^(4,8 − 3,75) = 11",
     "piege": "Ka₂/Ka₁ au lieu de Ka₁/Ka₂",
     "verification": "2023 N : CH₃COOH + HCOO⁻ (4,79 et 3,75) → K ? (9,1·10⁻²)"},
    {"id": "predominance", "notion": "pH = pKa + log([A⁻]/[AH]) et domaines de prédominance",
     "pourquoi_difficile": "un log d'un rapport ; l'élève inverse les domaines",
     "prerequis": ["logarithme_decimal_puissances"],
     "marches": [
        {"n": 1, "idee": "la relation", "vu": "−log de Ka", "phrase": "pH = pKa + log([A⁻]/[AH])", "question": "[A⁻] = [AH] ?"},
        {"n": 2, "idee": "les domaines", "vu": "curseur sur l'axe", "phrase": "à gauche du pKa l'acide, à droite la base", "question": "pH 3,41 ?"},
        {"n": 3, "idee": "les pourcentages", "vu": "deux courbes qui se croisent", "phrase": "au pKa, 50 % chacun", "question": "croisement ?"}],
     "image_mentale": "la balance à deux plateaux réglée sur le pKa",
     "exemple_chiffre": "pH 3,8 : 90,9 % de CH₃COOH",
     "piege": "pH > pKa : « l'acide prédomine »",
     "verification": "2016 N : pH 11,6, pKa 4,9 : qui prédomine ? (C₂H₅COO⁻)"},
    {"id": "dosage", "notion": "équivalence : C_A·V_A = C_B·V_BE ; E par les tangentes ou la dérivée",
     "pourquoi_difficile": "V_B quelconque mis dans la relation ; lecture graphique non justifiée ; trois pH_E différents",
     "prerequis": ["tableau_avancement", "concentration_quantite_matiere"],
     "marches": [
        {"n": 1, "idee": "réaction de dosage", "vu": "chaque goutte réagit", "phrase": "rapide, totale, unique", "question": "→ ou ⇌ ?"},
        {"n": 2, "idee": "équivalence", "vu": "tableau avant / à / après", "phrase": "proportions stœchiométriques", "question": "V_BE ?"},
        {"n": 3, "idee": "courbe et saut", "vu": "points tracés goutte à goutte", "phrase": "le saut de pH signale l'équivalence", "question": "où monte-t-il d'un coup ?"},
        {"n": 4, "idee": "tangentes, dérivée", "vu": "parallèles, pic", "phrase": "E se construit", "question": "V_BE ?"},
        {"n": 5, "idee": "exploiter", "vu": "trois pH_E, demi-équivalence, indicateur", "phrase": "pH = pKa à V_BE/2", "question": "pKa ?"}],
     "image_mentale": "remplir une bouteille : le niveau monte d'un coup au goulot",
     "exemple_chiffre": "C_A = C_B = 1,0·10⁻² mol/L, V_A = 20,0 mL → V_BE = 20,0 mL, pH_E = 8,3, pH(10 mL) = 4,8",
     "piege": "C_A·V_A = C_B·V_B ; pH = pKa à l'équivalence",
     "verification": "2021 N : V_a = 20 mL, C_b = 0,1 mol/L, V_bE = 20 mL → C_a ? (0,1 mol/L)"},
]

QUESTIONS_ELEVES = [
    {"question": "Pourquoi l'eau pure a un pH de 7 et pas 0 ?", "reponse": "Parce qu'elle contient des ions H₃O⁺ (autoprotolyse) : 1,0·10⁻⁷ mol/L à 25 °C, donc pH = 7."},
    {"question": "Ka et K, c'est la même chose ?", "reponse": "Ka est la constante K d'UNE réaction précise : celle de l'acide du couple avec l'eau."},
    {"question": "Pourquoi un pKa plus petit veut dire un acide plus fort ?", "reponse": "pKa = −log Ka : un grand Ka donne un petit pKa ; un grand Ka veut dire que l'acide cède plus son proton."},
    {"question": "Pourquoi pH_E n'est pas 7 quand on dose l'acide éthanoïque ?", "reponse": "À l'équivalence, la solution contient des ions CH₃COO⁻, une base : le pH est au-dessus de 7 (8,3)."},
    {"question": "Comment choisir entre la méthode des tangentes et la dérivée ?", "reponse": "Le sujet donne l'une ou l'autre : tangentes si on a seulement pH = f(V), maximum de dpH/dV si la dérivée est tracée."},
    {"question": "Pourquoi pH = pKa à la demi-équivalence ?", "reponse": "La moitié de l'acide est devenue sa base : [AH] = [A⁻], donc log 1 = 0 et pH = pKa."},
]

COMMENTAIRES = [
    {"plainte": "je calcule [HO⁻] avec 10^(−pH)", "vu": "2020 N, 2020 R, 2022 R (τ d'une base)", "reponse_du_cours": "w4 (Ke/[H₃O⁺]), b1, b2 ; rappels C1, C2"},
    {"plainte": "je ne sais pas trouver le pKa du couple d'une base", "vu": "2020 N, 2020 R, 2022 R", "reponse_du_cours": "a4 (Ka = Ke/Qr,éq pas à pas) ; notion ka_pka ; rappel C3_r3"},
    {"plainte": "je mets Ka₂ en haut", "vu": "2020 R, 2023 N", "reponse_du_cours": "k1 (démonstration), k2 (⚠ Ka₁ : acide qui réagit), k4 (lire le sujet) ; rappels C5"},
    {"plainte": "je confonds équivalence et demi-équivalence", "vu": "2023 R, 2024 N", "reponse_du_cours": "d3, e2 (tableau à V_BE/2), n5 ; rappels C8"},
    {"plainte": "je ne sais pas lire V_E sur la courbe", "vu": "8 sessions", "reponse_du_cours": "d4 (saut), d5 (tangentes), d6 (dérivée), n1, n2, n3"},
    {"plainte": "je choisis toujours le BBT", "vu": "6 sessions", "reponse_du_cours": "e1 (trois pH_E), e3 (rouge de crésol), e4 (rouge de méthyle), n1, n2 ; rappels C8_r3, C9_r2"},
]

COURS_EXISTANT = {
    "fichier": None,
    "constat": ("aucun ancien cours de ce chapitre dans backend/data/courses/ (vérifié le 12/11/2026 : en chimie seulement chem_ch1_kinetics_course_v1 "
                "(cinétique), phys_ch9 à phys_ch12 ; aucun fichier n'enseigne Ka, pKa ou le dosage acido-basique : phys_ch9/ch10 citent le "
                "titrage d'oxydoréduction, phys_ch11 un dosage pour τ = 1) ; le cours est écrit à partir de zéro ; les cours phys_ch11 et "
                "phys_ch12 fournissent les rappels (r1, r2) et les exemples (acide éthanoïque pH 3,41, K = 1,6·10⁻⁵, ammoniac, méthylamine)"),
    "a_garder": ["de phys_ch12 : acide éthanoïque C = 1,0·10⁻² mol/L, pH 3,41, Qr,éq = 1,57·10⁻⁵ (devient Ka) ; acide méthanoïque pH 2,90 ; méthylamine 2022 R"],
    "images": [],
    "a_corriger": [],
    "a_ajouter": ["tout le chapitre"],
    "a_retirer": [],
    "simulations_a_recreer": [{"ancienne": "/media/simulations/chimie/labs/equilibres/index.html",
                               "idee": "laboratoire « Équilibres en solution » (onglets « Acide-base » : Ka, concentration, pH, τ ; « dosage » goutte à goutte ; précipitation)",
                               "nouvelle": ("frontend/public/media/simulations/chimie/acides-bases-tableau/ (eau, base, acidite, comparer, predominance, "
                                            "dosage, exploiter, figures, bilan, carte) d'après le contrat ; ancienne simulation NON reprise "
                                            "(règle du 9 novembre 2026 ; elle assimile activité et concentration et mêle Qr,i/K et précipitation)")}],
}

VISUELS = {
    "_note": ("Simulations à la craie du contrat outils/cours/notes/cours/acides_bases_contrat_simulations.md, dossier "
              "frontend/public/media/simulations/chimie/acides-bases-tableau/ (kit commun.js, exposants.js, ab.css ; moteur des pages "
              "de etat-equilibre-tableau, déjà corrigé : durée d'une étape en plusieurs morceaux = Math.max) ; vues par ?vue=, "
              "moments nommés, repères, ce_qui_se_voit. figures.html?fig=fig_2025R|fig_2016N|fig_2022R|fig_2022N|fig_2024R dessine les "
              "figures des nationaux d'après acides_bases_build/nationaux.md § 5."),
    "v_carte": "carte.html : centre « couple AH/A⁻ : Ka, pKa ; dosage : C_A·V_A = C_B·V_BE » ; branches rappel, eau, base, acidite, comparer, reaction, predominance, indicateur, dosage, exploiter, national, suite",
    "v_eau": "eau.html?vue=ouverture|rappel|autoprotolyse|ke|solutions|ho|soude",
    "v_base": "base.html?vue=constante|ammoniac|taux|national",
    "v_acidite": "acidite.html?vue=definition|pka|mesure|ammonium|eau",
    "v_comparer": "comparer.html?vue=acides|bases|classement|reaction|puissance|totale|national",
    "v_predominance": "predominance.html?vue=relation|domaines|distribution|indicateur|virage",
    "v_dosage": "dosage.html?vue=montage|reaction|equivalence|courbe|tangentes|derivee",
    "v_exploiter": "exploiter.html?vue=trois_courbes|demi|indicateur|base|conductimetrie|national_2023",
    "v_figures": "figures.html?fig=fig_2025R|fig_2016N|fig_2022R|fig_2022N|fig_2024R",
    "v_bilan": "bilan.html : fiche « Ce qu'il faut retenir » (blocs), page 2 de l'élève",
    "agents_simulations": {
        "agent_1": ["eau.html", "base.html", "carte.html"],
        "agent_2": ["acidite.html", "comparer.html"],
        "agent_3": ["predominance.html", "dosage.html"],
        "agent_4": ["exploiter.html", "figures.html", "bilan.html"],
    },
    "manip_labo_3d": ("à proposer (skill labo-virtuel-2bac) : dosage pH-métrique de l'acide éthanoïque par la soude (burette, agitateur, "
                      "pH-mètre ; relever pH = f(V_B), tracer, tangentes ; AB8, AB9) — la manip la plus utile du semestre ; et test au BBT de "
                      "trois solutions (AB1, AB7) ; réutiliser une manip pH-mètre existante si elle existe"),
}

REGLES_SIMULATIONS = ("règles communes du contrat : fond transparent, un seul bouton, rien hors du cadre 760 × 420 ; solutions peintes, couleurs "
                      "vraies des indicateurs, burette, agitateur, pH-mètre au centième, courbes de dosage lues au dixième ; fractions avec barre "
                      "dessinée, exposants, indices et charges rendus ; ⇌ pour les réactions limitées, → pour le dosage ; virgule décimale ; Ke, "
                      "Ka, pKa, K, pH sans unité ; jamais de terme hors cadre à l'écran ; moments EXACTS du contrat, play_until, set_time, "
                      "set_parameters (poignées pH et V_B), highlight ; ce_qui_se_voit dit l'étape et les valeurs affichées ; moteur de "
                      "etat-equilibre-tableau (Math.max)")

REDACTION = {
    "_note": "lignes attendues d'après les corrigés du dépôt (erreurs du dépôt relevées dans acides_bases_build/nationaux.md § 4)",
    "ho_par_ke": ["Ke = [H₃O⁺]·[HO⁻]", "[HO⁻] = Ke/[H₃O⁺] = 10^(pH − 14)", "valeur en mol/L"],
    "pka": ["Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq = Qr,éq (acide) ou Ka = Ke/Qr,éq (base)", "pKa = −log Ka", "valeur sans unité"],
    "k_acide_base": ["équation", "K = quotient à l'équilibre", "× [H₃O⁺]_éq en haut et en bas", "K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁)", "valeur"],
    "predominance": ["pH = pKa + log([A⁻]_éq/[AH]_éq)", "comparer pH et pKa (ou le rapport à 1)", "nommer l'espèce qui prédomine"],
    "dosage": ["équation avec →", "méthode graphique nommée (tangentes / dérivée)", "C_A·V_A = C_B·V_BE", "application numérique avec unités", "dilution : C₀ = F·C"],
    "indicateur": ["pH_E lu ou justifié", "« sa zone de virage [a ; b] contient pH_E »", "nom de l'indicateur"],
}

RENVOIS = {
    "au_chapitre_11": "Brønsted, couples, pH = −log[H₃O⁺], τ d'un acide, conductimétrie (rappelés en r1)",
    "au_chapitre_12": "Qr, Qr,éq, K = Qr,éq, K = C·τ²/(1 − τ) (rappelés en r2 ; Ka les réutilise en a1, a3, a4)",
    "au_semestre_2_piles": "comparer Qr,i à K pour prévoir le sens (2020 R 2.4) ; perimetre.json clé piles_electrolyse",
    "au_semestre_2_esterification": "dosage du reste d'acide après une estérification (2025 R 2.2) : la méthode C_A·V_A = C_B·V_BE est apprise ici, l'estérification plus tard",
}

DECISIONS = [
    {"question": "Dosage : chapitre à part ou dans ce cours ?", "constat": "perimetre.json a une clé dosage séparée, mais programme_semestre1.json n'a PAS de clé dosage (ordre 13 = acides_bases, puis rien) ; 13 nationaux sur 20 mêlent le dosage aux pKa et à la prédominance dans le même exercice", "proposition": "le dosage RESTE DANS ce cours, partie finale (IX à XI : 6 + 5 + 5 diapositives) ; la clé dosage de perimetre.json est couverte par AB8-AB9 ; programme_semestre1.json non modifié"},
    {"question": "pH à l'équivalence de l'exemple J", "constat": "le brief proposait pH_E ≈ 8,4 ; la courbe calculée (pKa 4,8, C = 1,0·10⁻² mol/L, V = 20 + 20 mL) donne 8,25", "proposition": "pH_E = 8,3 (au dixième) ; indicateur rouge de crésol (7,2 – 8,8), pas la phénolphtaléine (8,2 – 10) qui serait à la limite"},
    {"question": "pKa de l'acide méthanoïque", "constat": "3,74 (2021 R), 3,75 (2021 N, 2023 N), 3,8 (2020 R) ; chapitre 12 : K = 1,8·10⁻⁴", "proposition": "pKa = 3,75 dans les exemples (Ka = 1,8·10⁻⁴, cohérent avec le chapitre 12) ; 3,8 gardé seulement en k4 (valeur du sujet 2020 R)"},
    {"question": "Dosage conductimétrique", "constat": "dans perimetre.json (clé dosage) mais jamais demandé 2016-2025", "proposition": "une seule diapositive (e5, acide chlorhydrique, rupture de pente) ; à retirer si l'utilisateur veut alléger"},
    {"question": "K > 10⁴ : réaction pratiquement totale", "constat": "critère utilisé par le corrigé 2016 N (« K ≫ 10⁴ ») ; perimetre.json ne le cite pas", "proposition": "dit une fois en k3 comme repère du corrigé, sans en faire une règle à apprendre"},
    {"question": "Formules du pH d'un acide faible ou à l'équivalence", "constat": "non demandées ; les sujets donnent le pH ou le font lire", "proposition": "aucune formule de pH « toute faite » ; pH_E justifié qualitativement (> 7, < 7) ; courbes calculées sans écrire le modèle"},
    {"question": "Kb, pKb, pOH", "constat": "absents des nationaux et de perimetre.json ; les bases sont classées par le pKa de leur couple", "proposition": "mis en hors cadre"},
    {"question": "Durée, découpage, identifiant", "constat": "48 diapositives, 4 séances, programme_semestre1.json ordre 13 statut a_explorer", "proposition": "160 min ; préfixe ab_ ; cours phys_ch13_acides_bases ; statut à passer à « explore » après validation (prog.py le passe à « construit »)"},
]

LIMITES = [
    "vidéos non auditées (YouTube bloqué depuis le cloud, yt-dlp non tenté) : 10 audits à faire depuis le PC avant validation",
    "texte officiel du cadre de référence non relu en entier : AB1-AB10 provisoires (appuyés sur perimetre.json acides_bases et dosage, et les nationaux)",
    "barème vérifié sur extraction.json pour 4 sessions seulement (2019 R, 2020 N, 2020 R, 2024 N) ; les autres points viennent de exam.json",
    "courbes des exemples J, K, L calculées avec python (pKa, Ke, bilan des charges) et vérifiées dans explo.py ; points des figures des nationaux relevés à l'œil (nationaux.md § 5)",
    "pKa(BBT) ≈ 7,0 et couleurs des indicateurs : valeurs usuelles des manuels, non tirées des nationaux",
]
