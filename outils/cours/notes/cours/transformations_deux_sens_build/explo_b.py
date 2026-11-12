"""Exploration transformations_deux_sens, partie B : plan (séances, compétences, 36 diapositives), notions, visuels, décisions.
Importé par explo.py. Ids des diapositives et vues = contrat outils/cours/notes/cours/transformations_deux_sens_contrat_simulations.md."""

SEANCES = [
    {"n": 1, "titre": "Acides et bases selon Brønsted, pH, réaction d'un acide avec l'eau",
     "blocs": [["o1", "o2", "b1", "b2"], ["b3", "b4", "p1", "p2"], ["p3", "p4", "p5", "p6"]]},
    {"n": 2, "titre": "Taux d'avancement final, réaction dans les deux sens, état d'équilibre",
     "blocs": [["a1", "a2", "a3", "a4"], ["a5", "a6", "e1", "e2"], ["e3", "e4", "e5", "e6"]]},
    {"n": 3, "titre": "Conductimétrie, dilution, questions du national, bilan",
     "blocs": [["c1", "c2", "c3", "d1"], ["d2", "d3", "n1", "n2"], ["n3", "n4", "bl", "cr"]]},
]

def R(id, type, prompt, **kw):
    d = {"id": id, "type": type, "prompt": prompt}
    d.update(kw)
    return d

COMPETENCES = [
    {"id": "C1", "verbe": "Définir un acide et une base selon Brønsted, écrire un couple, sa demi-équation et une réaction acido-basique",
     "cadre_ids": ["TD1"], "dit": "acide, base, couple, échange de proton", "rappels": [
        R("C1_r1", "qcm", "Selon Brønsted, une base est une espèce chimique capable de :",
          options=["céder un proton H⁺", "capter un proton H⁺", "céder un électron"], correct=1),
        R("C1_r2", "libre", "Écris la demi-équation du couple CH₃COOH/CH₃COO⁻.", attendu="CH₃COOH ⇌ CH₃COO⁻ + H⁺"),
        R("C1_r3", "vrai_faux", "Dans la réaction CH₃COOH + NH₃ → CH₃COO⁻ + NH₄⁺, le proton passe de CH₃COOH à NH₃.", correct=True),
        R("C1_r4", "qcm", "Quel couple contient l'eau comme acide ?",
          options=["H₃O⁺/H₂O", "H₂O/HO⁻", "CH₃COOH/CH₃COO⁻"], correct=1),
    ]},
    {"id": "C2", "verbe": "Relier pH et [H₃O⁺] (pH = −log[H₃O⁺], [H₃O⁺] = 10^(−pH)) et mesurer un pH avec un pH-mètre étalonné",
     "cadre_ids": ["TD2"], "dit": "le pH et la concentration des ions oxonium", "rappels": [
        R("C2_r1", "libre", "Une solution a pH = 3,4. Calcule [H₃O⁺].", attendu="[H₃O⁺] = 10^(−3,4) = 4,0·10⁻⁴ mol/L"),
        R("C2_r2", "qcm", "[H₃O⁺] = 1,0·10⁻² mol/L. Le pH vaut :", options=["−2,0", "2,0", "0,01"], correct=1),
        R("C2_r3", "vrai_faux", "Plus [H₃O⁺] est grande, plus le pH est grand.", correct=False),
        R("C2_r4", "libre", "Avant de mesurer, que fait-on avec le pH-mètre ?", attendu="on l'étalonne avec des solutions étalons de pH connu (4 et 7), puis on rince la sonde"),
    ]},
    {"id": "C3", "verbe": "Écrire la réaction d'un acide avec l'eau, dresser le tableau, calculer x_max, x_f (par le pH) et τ = x_f/x_max, conclure totale ou limitée",
     "cadre_ids": ["TD3", "TD4"], "dit": "avancement final et taux d'avancement final", "rappels": [
        R("C3_r1", "libre", "Acide éthanoïque C = 1,0·10⁻² mol/L, V = 100 mL, pH = 3,4. Calcule x_max, x_f puis τ.",
          attendu="x_max = C·V = 1,0·10⁻³ mol ; x_f = 10^(−3,4) × 0,100 = 4,0·10⁻⁵ mol ; τ = 0,040 : limitée"),
        R("C3_r2", "qcm", "2017 N : C = 1,0·10⁻² mol/L, pH = 3,41. τ vaut :", options=["0,39", "0,039", "3,41"], correct=1),
        R("C3_r3", "vrai_faux", "Pour l'acide chlorhydrique de pH 2,0 et C = 1,0·10⁻² mol/L, τ = 1 : la réaction est totale.", correct=True),
        R("C3_r4", "libre", "Montre que τ = 10^(−pH)/C pour la réaction d'un acide avec l'eau.",
          attendu="τ = x_f/x_max = [H₃O⁺]·V/(C·V) = 10^(−pH)/C"),
    ]},
    {"id": "C4", "verbe": "Expliquer qu'une réaction limitée se fait dans les deux sens (⇌), définir l'état d'équilibre et l'interpréter comme un équilibre dynamique",
     "cadre_ids": ["TD5"], "dit": "deux sens et équilibre dynamique", "rappels": [
        R("C4_r1", "vrai_faux", "À l'état d'équilibre, les deux réactions (sens 1 et sens 2) s'arrêtent.", correct=False),
        R("C4_r2", "qcm", "On ajoute des ions éthanoate à de l'acide chlorhydrique : le pH monte. Cela montre que :",
          options=["CH₃COO⁻ + H₃O⁺ → CH₃COOH + H₂O a lieu", "l'eau s'évapore", "l'acide chlorhydrique n'est pas un acide"], correct=0),
        R("C4_r3", "libre", "Que reste-t-il dans le bécher d'acide éthanoïque (exemple A) à l'équilibre ?",
          attendu="CH₃COOH (9,6·10⁻⁴ mol), CH₃COO⁻ et H₃O⁺ (4,0·10⁻⁵ mol chacun) et l'eau : réactifs et produits coexistent"),
    ]},
    {"id": "C5", "verbe": "Utiliser σ = Σ λᵢ·[Xᵢ] pour trouver [H₃O⁺], x_f et τ à partir d'une mesure de conductivité",
     "cadre_ids": ["TD6"], "dit": "conductimétrie et taux d'avancement final", "rappels": [
        R("C5_r1", "libre", "σ = 1,56·10⁻² S/m, λ(H₃O⁺) + λ(CH₃COO⁻) = 39,09·10⁻³ S·m²·mol⁻¹. Calcule [H₃O⁺] en mol/L.",
          attendu="[H₃O⁺] = 1,56·10⁻²/39,09·10⁻³ = 0,399 mol/m³ = 3,99·10⁻⁴ mol/L"),
        R("C5_r2", "vrai_faux", "Dans la solution d'acide éthanoïque, [CH₃COO⁻] = [H₃O⁺].", correct=True),
        R("C5_r3", "qcm", "2019 N : C = 1,0·10⁻³ mol/L. Dans τ = σ/(C·(λ₁ + λ₂)), on remplace C par :",
          options=["1,0·10⁻³", "1,0", "1,0·10³"], correct=1),
    ]},
    {"id": "C6", "verbe": "Prévoir l'influence de la dilution et de la nature de l'acide sur τ",
     "cadre_ids": ["TD7"], "dit": "la dilution augmente τ", "rappels": [
        R("C6_r1", "vrai_faux", "Quand on dilue une solution d'acide éthanoïque, τ augmente.", correct=True),
        R("C6_r2", "libre", "Acide éthanoïque C = 1,0·10⁻³ mol/L, pH = 3,9. Calcule τ et compare avec 0,040 (C = 1,0·10⁻²).",
          attendu="τ = 10^(−3,9)/1,0·10⁻³ = 0,13 > 0,040 : la dilution augmente τ"),
        R("C6_r3", "qcm", "À même concentration 1,0·10⁻² mol/L, quel acide a le plus grand τ ?",
          options=["acide éthanoïque (pH 3,4)", "acide méthanoïque (pH 2,9)", "acide chlorhydrique (pH 2,0)"], correct=2),
        R("C6_r4", "libre", "2021 R : pH = 3,6 et τ = 0,45. Calcule C.", attendu="C = 10^(−3,6)/0,45 = 5,58·10⁻⁴ mol/L"),
    ]},
    {"id": "C7", "verbe": "Rédiger un exercice du national : équation avec ⇌, tableau, relation littérale, application numérique, conclusion sur τ",
     "cadre_ids": ["TD8"], "dit": "rédiger comme le barème", "rappels": [
        R("C7_r1", "qcm", "Après avoir trouvé τ = 0,016 (2022 N), il faut encore écrire :",
          options=["rien", "« τ < 1 : la réaction est limitée »", "« τ > 1 : la réaction est totale »"], correct=1),
        R("C7_r2", "libre", "2023 N : C_A = 5,0·10⁻² mol/L, pH = 3,05. Calcule α(CH₃COOH) = 1 − τ.",
          attendu="τ = 10^(−3,05)/5,0·10⁻² = 0,0178 ; α = 0,982 = 98,2 %"),
        R("C7_r3", "vrai_faux", "Pour une réaction limitée, on écrit l'équation avec une double flèche ⇌.", correct=True),
    ]},
]

def D(id, title, lead, marche, visuel, question, prediction, competences, demonstration=()):
    return {"id": id, "title": title, "lead": lead, "marche": marche, "visuel": visuel, "question": question,
            "prediction": prediction, "competences": list(competences), "demonstration": list(demonstration)}

DIAPOS = [
    # Séance 1
    D("o1", "La carte du chapitre : réaction limitée, τ < 1", "Que va-t-on savoir faire ?",
      "carte : Brønsted → pH → acide + eau → τ → deux sens → équilibre → conductimétrie → dilution → national ; « au national : τ calculé dans 11 sessions sur 20, toujours avec le pH ou σ »",
      "carte", "Au national, quelle grandeur mesurée sert presque toujours à calculer τ ?", False, ["C7"]),
    D("o2", "Même concentration, pas le même pH", "Deux acides à 1,0·10⁻² mol/L : que va afficher le pH-mètre ?",
      "deux flacons de même étiquette C = 1,0·10⁻² mol/L ; acide éthanoïque : pH 3,4 ; acide chlorhydrique : pH 2,0 ; « pourquoi ? » (la question du chapitre)",
      "acides?vue=ouverture", "Les deux solutions auront-elles le même pH ?", True, ["C2", "C3"]),
    D("b1", "Un acide cède un proton", "Qu'est-ce qu'un acide selon Brønsted ?",
      "loupe : CH₃COOH perd un proton H⁺ et devient CH₃COO⁻ ; « acide : espèce chimique capable de céder un proton H⁺ »",
      "acides?vue=acide", "Que devient CH₃COOH quand il a cédé son proton ?", False, ["C1"]),
    D("b2", "Une base capte un proton", "Et une base ?",
      "loupe : NH₃ capte un proton H⁺ et devient NH₄⁺ ; « base : espèce chimique capable de capter un proton H⁺ »",
      "acides?vue=base", "NH₃ va-t-il céder ou capter le proton ?", True, ["C1"]),
    D("b3", "Le couple acide/base", "Comment écrire l'acide et sa base ensemble ?",
      "couple AH/A⁻ ; demi-équation AH ⇌ A⁻ + H⁺ ; exemples CH₃COOH/CH₃COO⁻, NH₄⁺/NH₃, H₃O⁺/H₂O, H₂O/HO⁻ ; l'eau appartient à deux couples",
      "acides?vue=couple", "Quelle est la base conjuguée de CH₃COOH ?", False, ["C1"],
      ["CH₃COOH ⇌ CH₃COO⁻ + H⁺", "NH₄⁺ ⇌ NH₃ + H⁺"]),
    D("b4", "La réaction acido-basique", "Que se passe-t-il quand un acide rencontre une base ?",
      "couples CH₃COOH/CH₃COO⁻ et NH₄⁺/NH₃ ; le proton passe de CH₃COOH à NH₃ ; CH₃COOH + NH₃ → CH₃COO⁻ + NH₄⁺ ; un échange de proton entre deux couples",
      "acides?vue=reaction", "Dans quel sens va passer le proton : de CH₃COOH vers NH₃ ou l'inverse ?", True, ["C1"],
      ["CH₃COOH ⇌ CH₃COO⁻ + H⁺", "NH₃ + H⁺ ⇌ NH₄⁺", "CH₃COOH + NH₃ → CH₃COO⁻ + NH₄⁺"]),
    D("p1", "Le pH", "Comment mesurer « combien » une solution est acide ?",
      "loupe sur les ions H₃O⁺ ; pH = −log[H₃O⁺] ([H₃O⁺] en mol/L, solution diluée) ; [H₃O⁺] = 10^(−pH) ; plus [H₃O⁺] est grande, plus le pH est petit",
      "ph?vue=definition", "Si [H₃O⁺] augmente, le pH monte-t-il ou descend-il ?", False, ["C2"]),
    D("p2", "De pH à [H₃O⁺]", "pH = 3,4 : combien d'ions H₃O⁺ par litre ?",
      "poignée pH ; [H₃O⁺] = 10^(−pH) ; à 3,4 : 4,0·10⁻⁴ mol/L ; à 2,0 : 1,0·10⁻² mol/L ; ⚠ le signe moins",
      "ph?vue=calcul", "10^(−3,4) sera-t-il plus grand ou plus petit que 10⁻³ ?", True, ["C2"],
      ["[H₃O⁺] = 10^(−pH)", "[H₃O⁺] = 10^(−3,4) = 4,0·10⁻⁴ mol/L"]),
    D("p3", "Mesurer le pH", "Comment utiliser le pH-mètre ?",
      "étalonnage avec deux solutions étalons (pH 4,0 puis 7,0), rinçage à l'eau distillée, sonde dans l'acide éthanoïque, lecture 3,4 (à 0,1 près)",
      "ph?vue=phmetre", "Pourquoi rince-t-on la sonde entre deux solutions ?", False, ["C2"]),
    D("p4", "L'acide éthanoïque réagit avec l'eau", "Où va le proton de CH₃COOH dans l'eau ?",
      "loupe : CH₃COOH cède son proton à H₂O qui devient H₃O⁺ ; CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺ ; couples CH₃COOH/CH₃COO⁻ et H₃O⁺/H₂O ; ici l'eau joue le rôle de base",
      "avancement?vue=acide_eau", "Dans cette réaction, l'eau va-t-elle céder ou capter le proton ?", True, ["C3", "C1"]),
    D("p5", "Une base réagit avec l'eau", "Et l'ammoniac dans l'eau ?",
      "loupe : NH₃ capte un proton de H₂O qui devient HO⁻ ; NH₃ + H₂O ⇌ NH₄⁺ + HO⁻ ; ici l'eau joue le rôle d'acide ; τ d'une base : au chapitre des réactions acide-base",
      "avancement?vue=base_eau", "Quel ion se forme : H₃O⁺ ou HO⁻ ?", False, ["C1", "C3"]),
    D("p6", "Si la réaction était totale…", "Quel pH aurait l'acide éthanoïque si tout l'acide réagissait ?",
      "hypothèse « totale » : [H₃O⁺] = C = 1,0·10⁻² mol/L → pH attendu 2,0 ; pH mesuré 3,4 ; moins de H₃O⁺ que prévu : la réaction n'est pas totale",
      "avancement?vue=attendu", "Quel pH faudrait-il lire si la réaction était totale ?", True, ["C3", "C2"],
      ["si totale : [H₃O⁺] = C = 1,0·10⁻² mol/L → pH = −log(1,0·10⁻²) = 2,0", "mesuré : pH = 3,4 > 2,0 → [H₃O⁺] < C : pas totale"]),
    # Séance 2
    D("a1", "Le tableau d'avancement", "Comment suivre les quantités avec un seul nombre x ?",
      "tableau CH₃COOH · H₂O · CH₃COO⁻ · H₃O⁺ : initial C·V · excès · 0 · 0 ; en cours C·V − x · excès · x · x ; final C·V − x_f · excès · x_f · x_f",
      "avancement?vue=tableau", "À l'état final, que vaut n(H₃O⁺) ?", False, ["C3"],
      ["n₀(CH₃COOH) = C·V = 1,0·10⁻² × 0,100 = 1,0·10⁻³ mol", "n(H₃O⁺)_f = x_f"]),
    D("a2", "L'avancement maximal", "Jusqu'où irait la réaction si elle était totale ?",
      "hypothèse : tout l'acide réagit : C·V − x_max = 0 → x_max = C·V = 1,0·10⁻³ mol (l'eau est en excès)",
      "avancement?vue=x_max", "x_max dépend-il du pH mesuré ?", True, ["C3"],
      ["C·V − x_max = 0", "x_max = C·V = 1,0·10⁻² × 0,100 = 1,0·10⁻³ mol"]),
    D("a3", "L'avancement final se mesure", "Combien d'acide a vraiment réagi ?",
      "colonne H₃O⁺ : n(H₃O⁺) = x_f ; x_f = [H₃O⁺]_éq·V = 10^(−pH)·V = 4,0·10⁻⁴ × 0,100 = 4,0·10⁻⁵ mol ; barre x_f à côté de x_max",
      "avancement?vue=x_f", "Que vaut x_f ?", False, ["C3"],
      ["x_f = [H₃O⁺]_éq·V", "x_f = 4,0·10⁻⁴ × 0,100 = 4,0·10⁻⁵ mol"]),
    D("a4", "Le taux d'avancement final", "Quelle part de l'acide a réagi ?",
      "τ = x_f/x_max = 4,0·10⁻⁵/1,0·10⁻³ = 0,040 = 4,0 % ; les deux barres ; τ < 1 : réaction limitée",
      "avancement?vue=taux", "τ sera-t-il proche de 1 ou petit ?", True, ["C3", "C4"],
      ["τ = x_f/x_max", "τ = 4,0·10⁻⁵/1,0·10⁻³ = 0,040 = 4,0 %", "τ < 1 : la réaction est limitée"]),
    D("a5", "L'acide chlorhydrique : τ = 1", "Et l'acide chlorhydrique de pH 2,0 ?",
      "HCl + H₂O → Cl⁻ + H₃O⁺ ; [H₃O⁺] = 1,0·10⁻² mol/L → x_f = 1,0·10⁻³ mol = x_max ; τ = 1 : réaction totale, flèche simple",
      "avancement?vue=totale", "Pour l'acide chlorhydrique, τ vaudra-t-il 1 ?", True, ["C3"],
      ["x_f = 10^(−2,0) × 0,100 = 1,0·10⁻³ mol", "τ = 1,0·10⁻³/1,0·10⁻³ = 1 : réaction totale"]),
    D("a6", "τ en fonction du pH", "Une relation pour aller vite au national.",
      "τ = x_f/x_max = [H₃O⁺]·V/(C·V) ; V se simplifie ; τ = 10^(−pH)/C ; vérification : 10^(−3,4)/1,0·10⁻² = 0,040",
      "avancement?vue=relation", "Pourquoi le volume V disparaît-il ?", False, ["C3", "C7"],
      ["τ = x_f/x_max = [H₃O⁺]_éq·V/(C·V)", "τ = 10^(−pH)/C", "τ = 10^(−3,4)/1,0·10⁻² = 0,040"]),
    D("e1", "La réaction se fait aussi à l'envers", "On verse des ions éthanoate dans l'acide chlorhydrique : que fait le pH ?",
      "acide chlorhydrique dilué : pH 2,3 ; on verse l'éthanoate de sodium : pH 3,6 ; les H₃O⁺ sont consommés : CH₃COO⁻ + H₃O⁺ → CH₃COOH + H₂O (sens 2)",
      "equilibre?vue=inverse", "Le pH va-t-il monter, descendre ou rester à 2,3 ?", True, ["C4"]),
    D("e2", "La double flèche", "Comment écrire une réaction qui va dans les deux sens ?",
      "sens 1 (→) et sens 2 (←) superposés : CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺ ; une réaction limitée se fait dans les deux sens",
      "equilibre?vue=double_fleche", "Quelle flèche pour l'acide éthanoïque, et laquelle pour l'acide chlorhydrique ?", False, ["C4", "C7"]),
    D("e3", "L'état d'équilibre", "Dix minutes plus tard, le pH change-t-il encore ?",
      "chrono 0 → 10 min, afficheur toujours 3,4 ; barres constantes : CH₃COOH 9,6·10⁻⁴ mol, CH₃COO⁻ et H₃O⁺ 4,0·10⁻⁵ mol ; réactifs et produits coexistent : état d'équilibre",
      "equilibre?vue=etat", "Le pH affiché va-t-il bouger pendant les dix minutes ?", True, ["C4"],
      ["n(CH₃COOH)_éq = 1,0·10⁻³ − 4,0·10⁻⁵ = 9,6·10⁻⁴ mol"]),
    D("e4", "Un équilibre dynamique", "Rien ne bouge… vraiment ?",
      "loupe : à chaque instant des CH₃COOH cèdent un proton (sens 1) et autant de CH₃COO⁻ en reprennent un (sens 2) ; deux compteurs égaux ; les deux réactions continuent à la même vitesse",
      "equilibre?vue=dynamique", "Les deux compteurs vont-ils avancer ensemble ?", True, ["C4"]),
    D("e5", "Une autre réaction limitée : l'estérification", "2016 N : acide propanoïque + éthanol.",
      "ballon à reflux ; acide + alcool ⇌ ester + eau (étudiée plus tard) ; x(t) monte lentement vers 0,33 mol sous x_max = 0,5 mol ; τ = 0,66 : lente et limitée",
      "equilibre?vue=esterification", "Que vaut τ si x_f = 0,33 mol et x_max = 0,5 mol ?", False, ["C4", "C3"],
      ["τ = 0,33/0,5 = 0,66 < 1 : limitée"]),
    D("e6", "National 2017 N : totale ou limitée ?", "Deux courbes, deux paliers : laquelle est totale ?",
      "fig_2017N : paliers 0,2 et 0,3 mol, x_max = 0,3 mol ; τ₁ = 0,67 ; τ₂ = 1 : la réaction de l'anhydride est totale (0,75 pt)",
      "figures?fig=fig_2017N", "Quelle courbe atteint x_max ?", True, ["C4", "C7"],
      ["τ₁ = 0,2/0,3 = 0,67", "τ₂ = 0,3/0,3 = 1 : l'expérience (2) est totale"]),
    # Séance 3
    D("c1", "Des ions qui conduisent", "Même concentration : laquelle conduit le mieux ?",
      "même cellule dans les deux acides de C = 1,0·10⁻² mol/L : acide éthanoïque 15,6 mS/m, acide chlorhydrique 426 mS/m ; moins d'ions → réaction limitée",
      "conductimetrie?vue=ions", "Quel afficheur montrera la plus grande valeur ?", True, ["C5"]),
    D("c2", "σ et [H₃O⁺]", "Comment relier σ à [H₃O⁺] ?",
      "σ = Σ λᵢ·[Xᵢ] ; σ = λ(H₃O⁺)·[H₃O⁺] + λ(CH₃COO⁻)·[CH₃COO⁻] ; tableau : [CH₃COO⁻] = [H₃O⁺] ; σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺]",
      "conductimetrie?vue=relation", "Pourquoi [CH₃COO⁻] = [H₃O⁺] ?", False, ["C5"]),
    D("c3", "De σ à τ", "σ = 1,56·10⁻² S/m : que vaut τ ?",
      "[H₃O⁺] = σ/(λ(H₃O⁺) + λ(A⁻)) = 1,56·10⁻²/39,09·10⁻³ = 0,399 mol/m³ ⚠ ÷ 10³ : 3,99·10⁻⁴ mol/L ; τ = 0,040, comme avec le pH",
      "conductimetrie?vue=calcul", "En quelle unité sort [H₃O⁺] de ce calcul ?", False, ["C5", "C7"],
      ["[H₃O⁺] = 1,56·10⁻²/(39,09·10⁻³) = 0,399 mol/m³ = 3,99·10⁻⁴ mol/L", "τ = 3,99·10⁻⁴/1,0·10⁻² = 0,040"]),
    D("d1", "Diluer l'acide éthanoïque", "On dilue 10 fois, puis encore 10 fois : que fait le pH ?",
      "1,0·10⁻² mol/L : pH 3,4 ; 1,0·10⁻³ : pH 3,9 ; 1,0·10⁻⁴ : pH 4,5 ; tableau C · pH",
      "dilution?vue=mesures", "Après dilution, le pH va-t-il monter ou descendre ?", True, ["C6"]),
    D("d2", "La dilution augmente τ", "Et la part d'acide qui a réagi ?",
      "τ = 10^(−pH)/C : 0,040 ; 0,13 ; 0,32 ; trois barres qui montent ; plus la solution est diluée, plus τ est grand",
      "dilution?vue=taux", "τ va-t-il augmenter ou diminuer quand on dilue ?", True, ["C6"],
      ["τ₁ = 10^(−3,4)/1,0·10⁻² = 0,040", "τ₂ = 10^(−3,9)/1,0·10⁻³ = 0,13", "τ₃ = 10^(−4,5)/1,0·10⁻⁴ = 0,32"]),
    D("d3", "τ dépend de l'acide", "Trois acides de même concentration.",
      "C = 1,0·10⁻² mol/L : acide chlorhydrique pH 2,0, τ = 1 ; acide méthanoïque pH 2,9, τ = 0,13 ; acide éthanoïque pH 3,4, τ = 0,040",
      "dilution?vue=nature", "Lequel aura le plus petit τ ?", True, ["C6", "C3"],
      ["acide méthanoïque : τ = 10^(−2,9)/1,0·10⁻² = 0,13"]),
    D("n1", "National 2021 R : la dilution", "Une courbe de τ en fonction du pH.",
      "fig_2021R : pH 2,8 → τ ≈ 0,10 → C₁ = 1,58·10⁻² mol/L ; pH 3,6 → τ ≈ 0,45 → C₂ = 5,58·10⁻⁴ mol/L ; C₂ < C₁ et τ₂ > τ₁ : la dilution augmente τ (1 pt)",
      "figures?fig=fig_2021R", "Calcule C pour pH = 2,8 et τ = 0,10.", False, ["C6", "C7"],
      ["C = 10^(−pH)/τ", "C₁ = 10^(−2,8)/0,10 = 1,58·10⁻² mol/L", "C₂ = 10^(−3,6)/0,45 = 5,58·10⁻⁴ mol/L"]),
    D("n2", "National 2019 N : τ par la conductivité", "Acide benzoïque, σ = 8,6·10⁻³ S/m.",
      "C = 1,0·10⁻³ mol/L = 1,0 mol/m³ ⚠ ; σ = (λ₁ + λ₂)·[H₃O⁺] ; τ = σ/(C·(λ(H₃O⁺) + λ(A⁻))) = 8,6·10⁻³/(1,0 × 38,23·10⁻³) = 0,22 (1,5 pt)",
      "conductimetrie?vue=national", "Calcule τ (λ₁ = 35·10⁻³, λ₂ = 3,23·10⁻³ S·m²·mol⁻¹).", False, ["C5", "C7"],
      ["τ = x_f/x_max = [H₃O⁺]·V/(C·V) et [H₃O⁺] = σ/(λ₁ + λ₂)", "τ = σ/(C·(λ₁ + λ₂))", "τ = 8,6·10⁻³/(1,0 × 38,23·10⁻³) = 0,22"]),
    D("n3", "National 2023 N : α = 1 − τ", "Une proportion à démontrer avec le tableau.",
      "C_A = 5,0·10⁻² mol/L, pH = 3,05 ; α = [CH₃COOH]/([CH₃COOH] + [CH₃COO⁻]) ; tableau : C_A(1 − τ) et C_A·τ ; α = 1 − τ = 0,982 (0,75 pt)",
      "avancement?vue=proportion", "Montre que α = 1 − τ, puis calcule α.", False, ["C3", "C7"],
      ["[CH₃COO⁻] = x_f/V = C_A·τ ; [CH₃COOH] = C_A − C_A·τ", "α = C_A(1 − τ)/C_A = 1 − τ", "τ = 10^(−3,05)/5,0·10⁻² = 0,0178 ; α = 0,982"]),
    D("n4", "National 2024 R : un dosage est total", "Amine dosée par l'acide chlorhydrique, pH = 10,2 à V_A = 16,0 mL.",
      "R–NH₂ + H₃O⁺ → R–NH₃⁺ + H₂O ; x_f = C_A·V_A − 10^(−pH)·(V_A + V_B) = 7,2·10⁻⁴ mol ; x_max = C_A·V_A = 7,2·10⁻⁴ mol ; τ = 1 : totale (1,5 pt)",
      "avancement?vue=dosage", "τ de la réaction de dosage sera-t-il égal à 1 ?", True, ["C3", "C7"],
      ["n(H₃O⁺)_f = C_A·V_A − x_f = [H₃O⁺]·(V_A + V_B)", "x_f = 4,5·10⁻² × 16,0·10⁻³ − 10^(−10,2) × 26,0·10⁻³ = 7,2·10⁻⁴ mol",
       "x_max = C_A·V_A = 7,2·10⁻⁴ mol ; τ = 1 : la réaction de dosage est totale"]),
    D("bl", "Ce qu'il faut retenir", "La fiche du chapitre.",
      "blocs : Brønsted, pH, taux, deux sens, conductimétrie, dilution, rédaction ; page 2 : tes lacunes",
      "bilan", "Quelle ligne de la fiche te paraît la plus difficile ?", False, ["C7"]),
    D("cr", "La carte complète", "Tout le chapitre d'un coup d'œil.",
      "carte complète ; suite : état d'équilibre d'un système chimique (chapitre suivant)",
      "carte", "Par quelle branche commencerais-tu un exercice du national sur un acide ?", False, ["C7"]),
]

PLAN = {
    "principes": ("une idée nouvelle par diapositive ; une chose vue, une phrase, une question ; exemples A (acide éthanoïque), B (acide "
                  "chlorhydrique), C (conductimétrie), D (dilution), E (sens 2), F (estérification) du contrat pour voir ; six nationaux pour "
                  "s'entraîner ; chaque bloc a au moins une prédiction ; Qr, K, Ke, pKa renvoyés aux chapitres suivants"),
    "duree_estimee_min": 120,
    "decoupage_conseille": "trois séances de trois blocs de quatre diapositives (bilan et carte dans le dernier bloc)",
    "prefixe_diapositives": "td_",
    "prerequis_verifies_au_debut": ["acide_base_bronsted_ph", "tableau_avancement", "concentration_quantite_matiere",
                                    "logarithme_decimal_puissances", "puissances_dix_unites", "conductimetrie"],
    "seances": SEANCES,
    "competences": COMPETENCES,
    "diapositives": DIAPOS,
}

NOTIONS = [
    {"id": "ph_et_h3o", "notion": "pH = −log[H₃O⁺] et [H₃O⁺] = 10^(−pH)",
     "pourquoi_difficile": "le logarithme décimal est mal connu ; le signe moins est oublié ; l'élève croit qu'un pH plus grand veut dire plus acide",
     "prerequis": ["logarithme_decimal_puissances", "puissances_dix_unites"],
     "marches": [
        {"n": 1, "idee": "des ions H₃O⁺ dans la solution", "vu": "loupe sur le bécher", "phrase": "une solution acide contient des ions H₃O⁺", "question": "combien par litre ?"},
        {"n": 2, "idee": "pH = −log[H₃O⁺]", "vu": "la formule écrite", "phrase": "le pH résume la concentration en un nombre simple", "question": "pH de 1,0·10⁻² mol/L ?"},
        {"n": 3, "idee": "[H₃O⁺] = 10^(−pH)", "vu": "poignée pH, la concentration change", "phrase": "on revient du pH à la concentration", "question": "pH 3,4 → ?"},
        {"n": 4, "idee": "sens de variation", "vu": "pH qui baisse quand [H₃O⁺] monte", "phrase": "plus d'ions H₃O⁺, pH plus petit", "question": "pH 2 ou pH 3, lequel est plus acide ?"}],
     "image_mentale": "le pH comme le numéro d'étage en descendant : un étage plus bas = dix fois plus d'ions H₃O⁺",
     "exemple_chiffre": "pH = 3,4 → [H₃O⁺] = 10^(−3,4) = 4,0·10⁻⁴ mol/L",
     "piege": "10^(pH) au lieu de 10^(−pH)",
     "verification": "pH = 2,9 : [H₃O⁺] ? (1,3·10⁻³ mol/L)"},
    {"id": "taux_avancement_final", "notion": "τ = x_f/x_max : x_max calculé, x_f mesuré",
     "pourquoi_difficile": "deux avancements à ne pas confondre ; x_f ne vient pas du tableau seul mais d'une mesure ; abstraction de « la part qui a réagi »",
     "prerequis": ["tableau_avancement", "concentration_quantite_matiere"],
     "marches": [
        {"n": 1, "idee": "pH attendu si totale", "vu": "pH 2,0 attendu, 3,4 mesuré", "phrase": "il y a moins de H₃O⁺ que prévu", "question": "totale ?"},
        {"n": 2, "idee": "x_max = C·V", "vu": "ligne finale si tout l'acide réagit", "phrase": "ce que la réaction pourrait faire", "question": "x_max ?"},
        {"n": 3, "idee": "x_f = [H₃O⁺]·V", "vu": "colonne H₃O⁺ surlignée", "phrase": "ce que la réaction a vraiment fait", "question": "x_f ?"},
        {"n": 4, "idee": "τ = x_f/x_max", "vu": "deux barres", "phrase": "la part de l'acide qui a réagi", "question": "τ ?"},
        {"n": 5, "idee": "τ = 1 ou τ < 1", "vu": "acide chlorhydrique à côté", "phrase": "totale ou limitée", "question": "laquelle est limitée ?"}],
     "image_mentale": "une note sur 1 : 0,040, c'est 4 % du chemin possible",
     "exemple_chiffre": "x_max = 1,0·10⁻³ mol ; x_f = 4,0·10⁻⁵ mol ; τ = 0,040",
     "piege": "x_f = C·V ; τ inversé",
     "verification": "2022 N : C = 5,0·10⁻² mol/L, pH = 3,1 : τ ? (0,016, limitée)"},
    {"id": "equilibre_dynamique", "notion": "à l'équilibre, les deux sens continuent à la même vitesse",
     "pourquoi_difficile": "à l'œil rien ne bouge : l'élève conclut que la réaction est arrêtée ; il faut imaginer l'échelle des molécules",
     "prerequis": ["acide_base_bronsted_ph"],
     "marches": [
        {"n": 1, "idee": "le sens 2 existe", "vu": "le pH monte quand on ajoute l'éthanoate", "phrase": "CH₃COO⁻ reprend un proton à H₃O⁺", "question": "pH monte ?"},
        {"n": 2, "idee": "⇌", "vu": "deux flèches superposées", "phrase": "la réaction se fait dans les deux sens", "question": "quelle flèche ?"},
        {"n": 3, "idee": "rien ne change à l'œil", "vu": "pH stable 10 min", "phrase": "état d'équilibre : quantités constantes", "question": "pH change ?"},
        {"n": 4, "idee": "tout bouge dans la loupe", "vu": "deux compteurs égaux", "phrase": "autant de réactions dans un sens que dans l'autre", "question": "compteurs ?"}],
     "image_mentale": "le souk à midi : autant de gens entrent que sortent, la foule reste la même",
     "exemple_chiffre": "à l'équilibre : 9,6·10⁻⁴ mol de CH₃COOH, 4,0·10⁻⁵ mol de CH₃COO⁻ et de H₃O⁺, sans changement",
     "piege": "« l'équilibre, c'est quand la réaction s'arrête »",
     "verification": "vrai ou faux : à l'équilibre, des molécules de CH₃COOH réagissent encore ? (vrai)"},
    {"id": "conductimetrie_tau", "notion": "σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] puis τ",
     "pourquoi_difficile": "unités en m³ ; deux ions à sommer ; la relation [A⁻] = [H₃O⁺] vient du tableau",
     "prerequis": ["conductimetrie", "puissances_dix_unites"],
     "marches": [
        {"n": 1, "idee": "σ vient des ions", "vu": "deux afficheurs 15,6 et 426 mS/m", "phrase": "plus d'ions → σ plus grande", "question": "laquelle conduit le mieux ?"},
        {"n": 2, "idee": "deux ions égaux", "vu": "tableau : x_f et x_f", "phrase": "[CH₃COO⁻] = [H₃O⁺]", "question": "pourquoi ?"},
        {"n": 3, "idee": "factoriser", "vu": "σ = (λ₁ + λ₂)·[H₃O⁺]", "phrase": "on isole [H₃O⁺]", "question": "unité ?"},
        {"n": 4, "idee": "conversion", "vu": "0,399 mol/m³ → 3,99·10⁻⁴ mol/L", "phrase": "÷ 10³", "question": "τ ?"}],
     "image_mentale": "chaque ion est un porteur de courant ; H₃O⁺ court très vite (grand λ), CH₃COO⁻ marche (petit λ)",
     "exemple_chiffre": "σ = 1,56·10⁻² S/m → [H₃O⁺] = 0,399 mol/m³ → τ = 0,040",
     "piege": "mol/L gardées avec λ en S·m²·mol⁻¹",
     "verification": "2019 N : τ ? (0,22)"},
    {"id": "dilution_tau", "notion": "la dilution augmente τ",
     "pourquoi_difficile": "le pH monte (solution moins acide) alors que τ augmente : deux sens de variation qui semblent contradictoires",
     "prerequis": ["logarithme_decimal_puissances"],
     "marches": [
        {"n": 1, "idee": "diluer fait monter le pH", "vu": "3,4 → 3,9 → 4,5", "phrase": "moins de H₃O⁺ par litre", "question": "pH monte ?"},
        {"n": 2, "idee": "calculer τ à chaque fois", "vu": "colonne τ", "phrase": "τ = 10^(−pH)/C", "question": "τ ?"},
        {"n": 3, "idee": "τ augmente", "vu": "trois barres qui montent", "phrase": "une plus grande part de l'acide a réagi", "question": "dilution → ?"}],
     "image_mentale": "dans une salle plus grande, les paires se retrouvent moins souvent : le sens 2 ralentit",
     "exemple_chiffre": "0,040 → 0,13 → 0,32",
     "piege": "« moins acide donc τ plus petit »",
     "verification": "2025 R : τ passe de 0,06 à 0,20 après dilution : conclusion ? (la dilution augmente τ)"},
]

QUESTIONS_ELEVES = [
    {"question": "Pourquoi l'acide éthanoïque ne réagit pas totalement avec l'eau ?", "reponse": "Parce que la réaction inverse existe : des ions CH₃COO⁻ reprennent des protons aux ions H₃O⁺. Les deux sens finissent par se compenser : c'est l'état d'équilibre."},
    {"question": "Pourquoi x_max = C·V alors que l'eau réagit aussi ?", "reponse": "L'eau est le solvant, en très grand excès : c'est l'acide qui limite."},
    {"question": "τ en % ou en décimal ?", "reponse": "Les deux sont justes : τ = 0,040 = 4,0 %. Pas d'unité."},
    {"question": "Si on dilue, la solution est moins acide : pourquoi τ augmente ?", "reponse": "Il y a moins de H₃O⁺ par litre (le pH monte), mais par rapport à l'acide versé, une plus grande part a réagi."},
    {"question": "Pourquoi le pH de l'eau pure vaut 7 ?", "reponse": "On le verra au chapitre des réactions acide-base ; ici retiens seulement qu'à 25 °C une solution neutre a pH = 7."},
]

COMMENTAIRES = [
    {"plainte": "je confonds x_f et x_max", "vu": "corrigés (x_éq, x_f, x_max selon les sessions)", "reponse_du_cours": "a2 (x_max calculé), a3 (x_f mesuré), a4 (deux barres), rappels C3"},
    {"plainte": "je ne sais pas calculer 10^(−pH)", "vu": "11 sessions demandent [H₃O⁺]", "reponse_du_cours": "p1, p2 (poignée pH), rappels C2 ; prérequis logarithme_decimal_puissances vérifié au début"},
    {"plainte": "la conductimétrie avec les m³, je me trompe toujours", "vu": "2019 N", "reponse_du_cours": "c2, c3 (⚠ ÷ 10³), n2 ; rappels C5"},
    {"plainte": "je ne comprends pas comment une réaction peut aller dans les deux sens", "vu": "définition de l'équilibre dynamique", "reponse_du_cours": "e1 (sens 2 vu au pH-mètre), e2 (⇌), e3, e4 (compteurs) ; rappels C4"},
    {"plainte": "pourquoi la dilution augmente τ alors que le pH monte", "vu": "2021 R, 2025 R", "reponse_du_cours": "d1, d2, n1 ; notion dilution_tau ; rappels C6"},
]

COURS_EXISTANT = {
    "fichier": None,
    "constat": ("aucun ancien cours de ce chapitre dans backend/data/courses/ (vérifié le 12/11/2026 : seuls chem_ch1_kinetics_course_v1, "
                "phys_ch9 et phys_ch10 pour la chimie) ; le cours est écrit à partir de zéro"),
    "a_garder": [],
    "images": [],
    "a_corriger": [],
    "a_ajouter": ["tout le chapitre"],
    "a_retirer": [],
    "simulations_a_recreer": [{"ancienne": "/media/simulations/chimie/labs/equilibres/index.html", "idee": "laboratoire « Équilibres en solution » (Qr/K, dosage, précipitation)",
                               "nouvelle": "frontend/public/media/simulations/chimie/transformations-deux-sens-tableau/ (acides, ph, avancement, equilibre, conductimetrie, dilution, figures, bilan, carte) d'après le contrat ; ancienne simulation NON reprise (règle du 9 novembre 2026 ; elle affiche Qr et K, hors de ce chapitre)"}],
}

VISUELS = {
    "_note": ("Simulations à la craie du contrat outils/cours/notes/cours/transformations_deux_sens_contrat_simulations.md, dossier "
              "frontend/public/media/simulations/chimie/transformations-deux-sens-tableau/ (kit commun.js, exposants.js, tds.css) ; vues par ?vue=, "
              "moments nommés, repères, ce_qui_se_voit. figures.html?fig=fig_<session> dessine les figures des nationaux d'après "
              "transformations_deux_sens_build/nationaux.md § 5."),
    "v_carte": "carte.html : centre « réaction limitée : τ < 1 » ; branches bronsted, ph, acide_eau, taux, deux_sens, equilibre, conductimetrie, dilution, national, suite",
    "v_acides": "acides.html?vue=ouverture|acide|base|couple|reaction",
    "v_ph": "ph.html?vue=definition|calcul|phmetre",
    "v_avancement": "avancement.html?vue=acide_eau|base_eau|attendu|tableau|x_max|x_f|taux|totale|relation|proportion|dosage",
    "v_equilibre": "equilibre.html?vue=inverse|double_fleche|etat|dynamique|esterification",
    "v_conductimetrie": "conductimetrie.html?vue=ions|relation|calcul|national",
    "v_dilution": "dilution.html?vue=mesures|taux|nature",
    "v_figures": "figures.html?fig=fig_2017N|fig_2021R",
    "v_bilan": "bilan.html : fiche « Ce qu'il faut retenir » (blocs), page 2 de l'élève",
    "manip_labo_3d": "à proposer (skill labo-virtuel-2bac) : mesure du pH d'une solution d'acide éthanoïque au pH-mètre étalonné, puis dilution (TD2, TD7)",
}

REGLES_SIMULATIONS = ("règles communes du contrat : fond transparent, un seul bouton, rien hors du cadre 760 × 420 ; solutions peintes, craie pour "
                      "le texte ; formules avec indices et charges rendus ; flèches → ← ⇌ dessinées ; virgule décimale ; jamais de terme hors cadre "
                      "(Qr, K, Ka, pKa, Ke…) à l'écran ; moments EXACTS du contrat, play_until, set_time, set_parameters, highlight ; "
                      "ce_qui_se_voit dit l'étape et les valeurs affichées")

REDACTION = {
    "_note": "lignes attendues d'après les corrigés du dépôt (erreurs du dépôt relevées dans transformations_deux_sens_build/nationaux.md § 4)",
    "equation_avec_eau": ["AH + H₂O ⇌ A⁻ + H₃O⁺ (acide) ou B + H₂O ⇌ BH⁺ + HO⁻ (base)", "double flèche"],
    "tau_par_ph": ["τ = x_f/x_max", "x_max = C·V ; x_f = [H₃O⁺]_éq·V", "τ = 10^(−pH)/C", "application numérique", "τ < 1 : la réaction est limitée"],
    "tau_par_sigma": ["σ = λ(H₃O⁺)·[H₃O⁺] + λ(A⁻)·[A⁻] et [A⁻] = [H₃O⁺]", "σ = (λ₁ + λ₂)·[H₃O⁺]", "τ = σ/(C·(λ₁ + λ₂)) avec C en mol/m³", "application numérique"],
    "dilution": ["calculer τ pour chaque solution", "comparer C et τ", "conclure : la dilution augmente τ"],
    "bronsted": ["acide : espèce chimique capable de céder un proton H⁺", "base : espèce chimique capable de capter un proton H⁺"],
}

RENVOIS = {
    "au_chapitre_precedent": "cinétique : tableau d'avancement, x_f lu sur un palier (rappelé en a1, e5, e6) ; conductimétrie σ = Σ λᵢ·[Xᵢ] (rappelée en c2)",
    "au_chapitre_suivant": "état d'équilibre : Qr, Qr,éq, K, sens d'évolution (demandés dans les mêmes exercices : 2017 N 1.2, 2019 N 3.3, 2020 R 1.4, 2021 N II.3, 2022 N 1.3, 2022 R 1.4)",
    "au_chapitre_acides_bases": "Ke, [HO⁻], τ d'une base (2020 N, 2020 R, 2022 R), Ka, pKa, prédominance, diagramme de distribution (2025 R 1.4)",
    "au_chapitre_dosage": "dosage acide-base, équivalence, indicateurs (n4 garde seulement τ = 1)",
    "au_chapitre_esterification": "estérification, hydrolyse, rendement (e5, e6 : seulement « lente et limitée » et τ)",
}

DECISIONS = [
    {"question": "Clé perimetre.json", "constat": "perimetre.json n'a pas de clé transformations_deux_sens : la clé acides_bases couvre les chapitres 11, 12 et 13", "proposition": "exploration transformations_deux_sens.json (clé de programme_semestre1.json) ; perimetre.json NON modifié ; à découper en trois clés par l'utilisateur ?"},
    {"question": "τ d'une base", "constat": "3 nationaux (2020 N, 2020 R, 2022 R) calculent τ d'une base par [HO⁻] = Ke/[H₃O⁺] ; Ke est au chapitre des réactions acide-base", "proposition": "ici seulement l'équation d'une base avec l'eau (p5) ; le calcul est renvoyé au chapitre 13"},
    {"question": "Exemple de l'estérification (e5, e6)", "constat": "4 nationaux demandent « lente et limitée » ; l'estérification est un chapitre du semestre 2", "proposition": "garder e5 et e6 comme exemples de réaction limitée/totale par τ, annoncés « étudiée plus tard »"},
    {"question": "pH de l'eau pure = 7", "constat": "il vient de Ke (chapitre 13) mais les élèves le connaissent depuis le collège", "proposition": "dit seulement en réponse à une question (questions_eleves), sans explication"},
    {"question": "Valeurs des exemples", "constat": "pH mesurés arrondis à 0,1 ; τ recalculé à partir du pH affiché (0,040 ; 0,13 ; 0,32)", "proposition": "garder les pH à 0,1 près (comme un pH-mètre) ; les τ suivent ces pH"},
    {"question": "Durée et découpage", "constat": "36 diapositives, 3 séances", "proposition": "120 min ; préfixe td_ ; ids du contrat"},
    {"question": "Clé et identifiant du cours", "constat": "programme_semestre1.json : ordre 11, statut a_explorer", "proposition": "exploration transformations_deux_sens.json ; cours phys_ch11_transformations_deux_sens ; statut à passer à « explore » après validation"},
]

LIMITES = [
    "vidéos non auditées (YouTube bloqué depuis le cloud, yt-dlp non tenté) : 10 audits à faire depuis le PC avant validation",
    "texte officiel du cadre de référence non relu en entier : TD1-TD8 provisoires (appuyés sur perimetre.json et les nationaux)",
    "fig_2021R : courbe calculée pour passer par les deux lectures du corrigé (0,10 et 0,45) ; écart de lecture possible de ± 0,03",
    "exemples A à F du contrat : valeurs choisies pour l'œil et vérifiées avec python (explo.py)",
]
