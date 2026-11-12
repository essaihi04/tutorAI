"""Exploration transformations_deux_sens, partie A : en-tête, sources, cadre, nationaux, pièges, décisions.
Importé par explo.py (même dossier)."""

EXAMS = [f"backend/data/exams/physique/{a}-{s}" for a in range(2016, 2026) for s in ("normale", "rattrapage")]
AVEC_TAU = ["2017-normale", "2019-normale", "2020-normale", "2020-rattrapage", "2021-normale", "2021-rattrapage",
            "2022-normale", "2022-rattrapage", "2023-normale", "2024-rattrapage", "2025-rattrapage"]

ENTETE = {
    "cle": "transformations_deux_sens",
    "matiere": "Physique-Chimie",
    "filiere": "2e Bac Sciences Physiques BIOF (Maroc)",
    "titre": "Transformations chimiques s'effectuant dans les deux sens",
    "date_exploration": "2026-11-12",
    "_note": ("Exploration faite par la routine cloud du 12 novembre 2026 pour le cours phys_ch11_transformations_deux_sens. VIDÉOS NON "
              "AUDITÉES : YouTube est bloqué depuis le conteneur cloud (yt-dlp non tenté). Appui : les 20 nationaux PC 2016-2025 du dépôt "
              "(17 touchent ce chapitre, 11 calculent τ ; transformations_deux_sens_build/nationaux.md, figures regardées et nombres "
              "recalculés avec python), perimetre.json (clé acides_bases, qui couvre ce chapitre et les deux suivants), programme_semestre1.json "
              "(ordre 11) et le contrat des simulations transformations_deux_sens_contrat_simulations.md (exemples A à F ; vues ; diapositives "
              "servies). Pas d'ancien cours de ce chapitre dans backend/data/courses/. À compléter par 10 audits vidéo depuis le PC avant "
              "validation. Qr, K (état d'équilibre) et Ke, Ka, pKa, prédominance (réactions acide-base) sont renvoyés aux chapitres 12 et 13."),
}

SOURCES = {
    "videos": [],
    "videos_note": ("aucune : YouTube inaccessible depuis le conteneur cloud (12/11/2026) ; vidéos non auditées ; 10 audits à faire depuis "
                    "le PC (recherche « التحولات الكيميائية التي تحدث في المنحيين 2 باك », « transformations chimiques s'effectuant dans "
                    "les deux sens 2bac biof », « taux d'avancement final pH 2 bac »)"),
    "examens": EXAMS,
    "examens_avec_calcul_de_tau": [f"backend/data/exams/physique/{s}" for s in AVEC_TAU],
    "autres": [
        "outils/cours/notes/cours/transformations_deux_sens_build/nationaux.md (relecture des 20 sujets, 2 figures pour figures.html)",
        "outils/cours/notes/cours/transformations_deux_sens_contrat_simulations.md (exemples A à F, vues, diapositives servies)",
        "backend/data/curriculum/perimetre.json (clé acides_bases : notions, termes hors programme)",
        "backend/data/curriculum/programme_semestre1.json (ordre 11, clé transformations_deux_sens)",
        "backend/data/curriculum/prerequis.json (acide_base_bronsted_ph, tableau_avancement, logarithme_decimal_puissances, conductimetrie)",
        "backend/data/curriculum/exploration/cinetique.json (chapitre précédent, modèle)",
    ],
}

COMPARAISON = {
    "_note": "sans vidéos : comparaison faite entre les corrigés des 11 nationaux qui calculent τ, perimetre.json et le chapitre précédent",
    "convergences": [
        "équation de l'acide avec l'eau écrite avec ⇌ : AH + H₂O ⇌ A⁻ + H₃O⁺ (11 sessions sur 11)",
        "tableau d'avancement : eau en excès ; x_max = C·V (réaction supposée totale) ; x_f = n(H₃O⁺)_éq = [H₃O⁺]_éq·V",
        "[H₃O⁺] = 10^(−pH) puis τ = x_f/x_max = 10^(−pH)/C (V se simplifie) ; conclusion « τ < 1 : réaction limitée »",
        "réaction totale : τ = 1 (dosage, anhydride, acide chlorhydrique)",
        "conductimétrie : σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] car [A⁻] = [H₃O⁺] ; [X] en mol/m³",
        "la dilution augmente τ (2021 R, 2025 R)",
    ],
    "variantes_admises": [
        {"variante": "x_f ou x_éq, [H₃O⁺]_f ou [H₃O⁺]_éq", "decision": "x_f et [H₃O⁺]_éq (comme 2021 R, 2022 N) ; on dit une fois que certains corrigés écrivent x_éq"},
        {"variante": "τ en décimal (0,040) ou en % (4,0 %)", "decision": "les deux, avec le signe = : τ = 0,040 = 4,0 %"},
        {"variante": "« taux d'avancement final » ou « taux d'avancement »", "decision": "taux d'avancement final (mot du cadre) ; symbole τ"},
        {"variante": "HO⁻ ou OH⁻", "decision": "HO⁻ (sujets marocains) ; OH⁻ jamais écrit"},
        {"variante": "« réaction limitée », « non totale », « équilibrée »", "decision": "limitée (mot des corrigés) ; on dit qu'elle se fait dans les deux sens"},
        {"variante": "proton ou ion H⁺", "decision": "« proton H⁺ » dans les définitions de Brønsted ; [H₃O⁺] pour la concentration, jamais [H⁺]"},
    ],
    "meilleures_explications": [
        "deux flacons de même concentration, deux pH différents (3,4 et 2,0) : la question qui ouvre tout le chapitre",
        "le pH attendu si la réaction était totale (2,0) comparé au pH mesuré (3,4) : la preuve que la réaction n'est pas totale",
        "deux barres x_f et x_max côte à côte : τ se voit avant de se calculer",
        "l'équilibre dynamique : deux compteurs « sens 1 » et « sens 2 » qui avancent ensemble",
        "l'éthanoate ajouté à l'acide chlorhydrique fait MONTER le pH : le sens 2 existe",
    ],
}

CADRE = {
    "_note": ("Fiche du chapitre, même forme que cadre_reference_2bac_pc.json. Capacités d'après CDR-PC-2015 (annexe 1, Chimie, sous-domaine 2 "
              "« Transformations non totales d'un système chimique » : « Transformations chimiques dans les deux sens (acide-base selon Bronsted, "
              "pH, taux d'avancement final, état d'équilibre) »), OP-PC-2007, perimetre.json (clé acides_bases) et les nationaux 2016-2025. "
              "Texte officiel du cadre non relu en entier : TD1 à TD8 provisoires. Formules écrites exactement comme le contrat des simulations."),
    "titre": "Transformations chimiques s'effectuant dans les deux sens",
    "source": ("CDR-PC-2015, annexe 1, Chimie, sous-domaine 2 « Transformations non totales d'un système chimique » : « Transformations chimiques "
               "dans les deux sens (acide-base selon Bronsted, pH, taux d'avancement final, état d'équilibre) » ; OP-PC-2007, 2BAC : couples "
               "acide/base, mesure du pH, taux d'avancement final, réaction limitée, interprétation microscopique de l'état d'équilibre, "
               "conductimétrie ; perimetre.json clé acides_bases ; nationaux PC 2016-2025 du dépôt."),
    "capacites": [
        {"id": "TD1", "texte": "Définir un acide et une base selon Brønsted ; écrire la demi-équation d'un couple acide/base et l'équation d'une réaction acido-basique en identifiant les deux couples."},
        {"id": "TD2", "texte": "Définir le pH d'une solution aqueuse diluée (pH = −log[H₃O⁺]), calculer [H₃O⁺] = 10^(−pH) et inversement ; mesurer un pH avec un pH-mètre étalonné."},
        {"id": "TD3", "texte": "Écrire l'équation de la réaction d'un acide (ou d'une base) avec l'eau ; dresser son tableau d'avancement ; calculer x_max et déterminer x_f à partir d'une mesure (pH ou conductivité)."},
        {"id": "TD4", "texte": "Définir et calculer le taux d'avancement final τ = x_f/x_max ; reconnaître une réaction totale (τ = 1) ou limitée (τ < 1) ; établir τ = 10^(−pH)/C pour un acide."},
        {"id": "TD5", "texte": "Savoir qu'une réaction limitée se fait dans les deux sens (symbole ⇌) ; définir l'état d'équilibre et l'interpréter à l'échelle microscopique (équilibre dynamique)."},
        {"id": "TD6", "texte": "Exploiter une mesure de conductivité (σ = Σ λᵢ·[Xᵢ]) pour déterminer [H₃O⁺], x_f et τ."},
        {"id": "TD7", "texte": "Connaître l'influence de la concentration initiale (dilution) et de la nature de l'acide sur le taux d'avancement final."},
        {"id": "TD8", "texte": "Rédiger un exercice du national : équation avec ⇌, tableau, relation littérale, application numérique avec unités cohérentes, conclusion sur τ."},
    ],
    "formules": [
        {"id": "f_demi", "ecriture": "AH ⇌ A⁻ + H⁺", "capacite": "TD1", "dit": "A H donne A moins plus H plus, dans les deux sens", "phrase": "demi-équation d'un couple acide/base AH/A⁻"},
        {"id": "f_ph", "ecriture": "pH = −log[H₃O⁺]", "capacite": "TD2", "dit": "pH égale moins log de la concentration des ions H trois O plus", "phrase": "[H₃O⁺] en mol/L ; solution aqueuse diluée", "unite": "sans unité"},
        {"id": "f_h3o", "ecriture": "[H₃O⁺] = 10^(−pH)", "capacite": "TD2", "dit": "la concentration des ions H trois O plus égale dix puissance moins pH", "phrase": "résultat en mol/L ; ne pas oublier le signe moins", "unite": "mol/L"},
        {"id": "f_acide_eau", "ecriture": "AH + H₂O ⇌ A⁻ + H₃O⁺", "capacite": "TD3", "dit": "A H plus H deux O donne A moins plus H trois O plus, dans les deux sens", "phrase": "l'eau joue le rôle de base"},
        {"id": "f_base_eau", "ecriture": "B + H₂O ⇌ BH⁺ + HO⁻", "capacite": "TD3", "dit": "B plus H deux O donne B H plus plus H O moins, dans les deux sens", "phrase": "l'eau joue le rôle d'acide ; τ d'une base : au chapitre des réactions acide-base"},
        {"id": "f_quantite", "ecriture": "n = C·V", "capacite": "TD3", "dit": "n égale C fois V", "phrase": "C en mol/L, V en L"},
        {"id": "f_xmax", "ecriture": "x_max = C·V", "capacite": "TD3", "dit": "x max égale C fois V", "phrase": "si la réaction était totale, l'acide serait entièrement consommé", "unite": "mol"},
        {"id": "f_xf", "ecriture": "x_f = [H₃O⁺]_éq·V", "capacite": "TD3", "dit": "x f égale la concentration des ions H trois O plus à l'équilibre fois V", "phrase": "n(H₃O⁺) = x_f d'après le tableau", "unite": "mol"},
        {"id": "f_tau", "ecriture": "τ = x_f/x_max", "capacite": "TD4", "dit": "tau égale x f sur x max", "phrase": "τ = 1 : totale ; τ < 1 : limitée", "unite": "sans unité"},
        {"id": "f_tau_ph", "ecriture": "τ = 10^(−pH)/C", "capacite": "TD4", "dit": "tau égale dix puissance moins pH, sur C", "phrase": "pour la réaction d'un acide avec l'eau ; C en mol/L"},
        {"id": "f_sigma", "ecriture": "σ = Σ λᵢ·[Xᵢ]", "capacite": "TD6", "dit": "sigma égale la somme des lambda i fois la concentration de l'ion i", "phrase": "λ en S·m²·mol⁻¹, [X] en mol/m³ ; 1 mol/L = 10³ mol/m³", "unite": "S/m"},
        {"id": "f_sigma_acide", "ecriture": "σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺]", "capacite": "TD6", "dit": "sigma égale lambda H trois O plus plus lambda A moins, fois la concentration des ions H trois O plus", "phrase": "car [A⁻] = [H₃O⁺] (tableau) ; ions HO⁻ négligés"},
        {"id": "f_h3o_sigma", "ecriture": "[H₃O⁺] = σ/(λ(H₃O⁺) + λ(A⁻))", "capacite": "TD6", "dit": "la concentration des ions H trois O plus égale sigma sur la somme des deux lambda", "phrase": "résultat en mol/m³, à diviser par 10³ pour l'avoir en mol/L"},
        {"id": "f_tau_sigma", "ecriture": "τ = σ/(C·(λ(H₃O⁺) + λ(A⁻)))", "capacite": "TD6", "dit": "tau égale sigma sur C fois la somme des deux lambda", "phrase": "C en mol/m³ (2019 N)"},
    ],
    "mots_cles": ["acide", "base", "Brønsted", "proton", "couple acide/base", "demi-équation", "réaction acido-basique", "pH", "pH-mètre",
                  "étalonnage", "ion oxonium", "réaction avec l'eau", "tableau d'avancement", "avancement maximal", "avancement final",
                  "taux d'avancement final", "réaction totale", "réaction limitée", "deux sens", "état d'équilibre", "équilibre dynamique",
                  "conductimétrie", "conductivité", "conductivité molaire ionique", "dilution"],
    "hors_cadre": {
        "_note": ("termes à ne jamais écrire ni dire dans ce cours : chapitres suivants (état d'équilibre : Qr, K ; réactions acide-base : Ke, Ka, "
                  "pKa, prédominance, indicateurs) et hors programme (perimetre.json acides_bases.termes_hors_programme)"),
        "mots": ["Qr", "quotient de réaction", "constante d'équilibre", "constante d'acidité", "Ka", "pKa", "Ke", "pKe", "produit ionique",
                 "autoprotolyse", "activité", "Lewis", "Arrhenius", "degré d'ionisation", "coefficient de dissociation", "Ostwald",
                 "loi de dilution", "diagramme de prédominance", "diagramme de distribution", "espèce prédominante", "Henderson",
                 "Hasselbalch", "indicateur coloré", "zone de virage", "pouvoir tampon"],
    },
    "valeurs_reference": {
        "exemple_A": {"equation": "CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺", "C_mol_L": 1.0e-2, "V_L": 0.100, "pH": 3.4, "pH_si_totale": 2.0,
                      "H3O_mol_L": 4.0e-4, "x_max_mol": 1.0e-3, "x_f_mol": 4.0e-5, "tau": 0.040,
                      "equilibre_mol": {"CH3COOH": 9.6e-4, "CH3COO-": 4.0e-5, "H3O+": 4.0e-5}},
        "exemple_B": {"equation": "HCl + H₂O → Cl⁻ + H₃O⁺", "C_mol_L": 1.0e-2, "pH": 2.0, "x_f_mol": 1.0e-3, "tau": 1},
        "exemple_C": {"lambda_mS_m2_mol": {"H3O+": 35.0, "CH3COO-": 4.09, "Cl-": 7.63}, "sigma_A_S_m": 1.56e-2, "sigma_B_S_m": 0.426,
                      "H3O_mol_m3": 0.399, "H3O_mol_L": 3.99e-4, "tau": 0.040},
        "exemple_D": {"C_mol_L": [1.0e-2, 1.0e-3, 1.0e-4], "pH": [3.4, 3.9, 4.5], "tau": [0.040, 0.13, 0.32],
                      "nature_meme_C": {"acide chlorhydrique": {"pH": 2.0, "tau": 1}, "acide méthanoïque": {"pH": 2.9, "tau": 0.13},
                                        "acide éthanoïque": {"pH": 3.4, "tau": 0.040}}},
        "exemple_E": {"pH_acide_dilue": 2.3, "pH_avec_ethanoate": 3.6, "equation": "CH₃COO⁻ + H₃O⁺ → CH₃COOH + H₂O"},
        "exemple_F": {"source": "2016 N", "n0_mol": 0.5, "n_ester_mol": 0.33, "tau": 0.66},
    },
}

INSISTANCES = [
    "x_max se CALCULE (réaction supposée totale) ; x_f se MESURE (pH ou conductivité)",
    "[H₃O⁺] = 10^(−pH) : le signe moins ; le résultat est en mol/L",
    "τ = x_f/x_max est toujours ≤ 1 ; τ < 1 : réaction limitée, elle se fait dans les deux sens (⇌)",
    "à l'équilibre les deux réactions continuent à la même vitesse : rien ne change à l'œil, tout bouge à l'échelle des molécules",
    "en conductimétrie, [X] en mol/m³ : 1 mol/L = 10³ mol/m³",
    "la dilution augmente τ (et augmente aussi le pH)",
]

VALEURS_REPERES = [
    "exemple A : acide éthanoïque C = 1,0·10⁻² mol/L, V = 100 mL, pH = 3,4 → [H₃O⁺] = 4,0·10⁻⁴ mol/L, x_f = 4,0·10⁻⁵ mol, x_max = 1,0·10⁻³ mol, τ = 0,040",
    "exemple B : acide chlorhydrique même C, pH = 2,0 → τ = 1",
    "exemple C : σ = 1,56·10⁻² S/m → [H₃O⁺] = 0,399 mol/m³ = 3,99·10⁻⁴ mol/L → τ = 0,040",
    "exemple D : dilution 1,0·10⁻² → 1,0·10⁻³ → 1,0·10⁻⁴ mol/L : pH 3,4 → 3,9 → 4,5 ; τ 0,040 → 0,13 → 0,32",
    "nationaux : τ = 3,9 % (2017 N), 0,22 (2019 N), 4,0 % (2020 N), 1,32 % (2021 N), 1,6 % (2022 N), 0,20 (2022 R), 1,78 % (2023 N), 0,06 (2025 R)",
]

CAS_TYPES = [
    {"cas": "équation d'un acide (ou d'une base) avec l'eau", "mots": "« Écrire l'équation de la réaction de l'acide … avec l'eau »", "methode": "AH + H₂O ⇌ A⁻ + H₃O⁺ ; base : B + H₂O ⇌ BH⁺ + HO⁻ ; double flèche", "points": "0,25-0,5", "frequence": "11 sessions"},
    {"cas": "τ à partir du pH", "mots": "« Calculer le taux d'avancement final τ. Que peut-on conclure ? »", "methode": "[H₃O⁺] = 10^(−pH) ; τ = 10^(−pH)/C ; τ < 1 → limitée", "points": "0,5-0,75", "frequence": "6 sessions pour un acide (2017 N, 2021 N, 2021 R, 2022 N, 2023 N, 2025 R) ; 3 pour une base (Ke : chapitre suivant)"},
    {"cas": "montrer une expression de τ", "mots": "« Montrer que τ = 10^(−pH)/C » ; « τ = σ/(C(λ₁ + λ₂)) » ; « α = 1 − τ »", "methode": "partir de τ = x_f/x_max ; remplacer x_f et x_max par le tableau ; simplifier V", "points": "0,25-0,75", "frequence": "4 sessions (2019 N, 2021 R, 2023 N, 2025 R)"},
    {"cas": "conductimétrie → τ", "mots": "« exprimer σ en fonction de λ₁, λ₂ et [H₃O⁺] »", "methode": "σ = (λ₁ + λ₂)·[H₃O⁺] ; C en mol/m³ ; τ = σ/(C(λ₁ + λ₂))", "points": "1,5", "frequence": "1 session (2019 N)"},
    {"cas": "effet de la dilution sur τ", "mots": "« En déduire l'effet de la dilution sur le taux d'avancement final »", "methode": "comparer deux C et leurs τ : C plus petite → τ plus grand", "points": "0,25-0,5", "frequence": "2 sessions (2021 R, 2025 R)"},
    {"cas": "réaction totale par τ = 1", "mots": "« déduire que la réaction de dosage est totale » ; « laquelle est totale »", "methode": "x_f mesuré = x_max calculé → τ = 1", "points": "0,75", "frequence": "2 sessions (2017 N 2.3, 2024 R 2.4)"},
    {"cas": "définir un acide / une base selon Brønsted", "mots": "« Donner la définition d'une base selon Bronsted »", "methode": "espèce chimique capable de capter (base) / céder (acide) un proton H⁺", "points": "0,25-0,5", "frequence": "2 sessions (2022 R, 2023 R)"},
    {"cas": "caractéristiques d'une estérification / hydrolyse", "mots": "« Citer deux caractéristiques de cette réaction »", "methode": "lente et limitée", "points": "0,5", "frequence": "4 sessions (2016 N, 2016 R, 2018 N, 2018 R)"},
]

PIEGES = [
    {"erreur": "[H₃O⁺] = 10^(pH) (signe oublié)", "geste": "écrire la relation [H₃O⁺] = 10^(−pH) avant le calcul ; vérifier : pH 3,4 → 4,0·10⁻⁴, plus petit que 1"},
    {"erreur": "prendre x_f = C·V", "geste": "x_f vient de la mesure : x_f = [H₃O⁺]_éq·V ; x_max = C·V vient du calcul"},
    {"erreur": "τ = x_max/x_f (inversé, τ > 1)", "geste": "τ est une fraction de x_max : toujours ≤ 1"},
    {"erreur": "[X] en mol/L dans σ = Σ λᵢ·[Xᵢ]", "geste": "1 mol/L = 10³ mol/m³ ; [H₃O⁺] trouvée en mol/m³ → diviser par 10³"},
    {"erreur": "oublier [A⁻] = [H₃O⁺] et ne garder qu'un ion dans σ", "geste": "lire le tableau : les deux produits valent x_f"},
    {"erreur": "flèche simple pour une réaction limitée", "geste": "réaction avec l'eau d'un acide (autre qu'un acide comme HCl) : ⇌"},
    {"erreur": "croire qu'à l'équilibre les réactions s'arrêtent", "geste": "équilibre dynamique : les deux sens continuent à la même vitesse"},
    {"erreur": "croire que diluer diminue τ", "geste": "la dilution augmente τ (2021 R : 0,10 → 0,45 ; 2025 R : 0,06 → 0,20)"},
]

ERREURS_EXAMEN = [
    {"erreur": "conclusion absente après le calcul de τ", "geste": "écrire « τ < 1 : la réaction est limitée » (la conclusion fait partie des points)", "source": "2017 N, 2020 R, 2022 N, 2022 R"},
    {"erreur": "C laissée en mol/L avec λ en S·m²·mol⁻¹", "geste": "C = 1,0·10⁻³ mol/L = 1,0 mol/m³", "source": "2019 N"},
    {"erreur": "équation d'une base avec l'eau qui produit H₃O⁺", "geste": "une base capte le proton de l'eau : il se forme HO⁻ (le corrigé du dépôt 2020 N se trompe lui aussi)", "source": "2020 N, 2022 R, 2024 R"},
    {"erreur": "« montrer que » sans partir de la définition", "geste": "τ = x_f/x_max, puis tableau, puis simplification", "source": "2019 N, 2021 R, 2023 N"},
    {"erreur": "lire τ en % sur une figure graduée de 0 à 1", "geste": "recopier l'échelle de l'axe : τ ≈ 0,10, puis C = 10^(−pH)/τ", "source": "2021 R"},
]

CONSEILS = [
    "écrire d'abord l'équation avec ⇌, puis le tableau (eau en excès), puis x_max, puis x_f, puis τ",
    "relation littérale, application numérique, résultat ; pour τ, toujours la conclusion « limitée » ou « totale »",
    "en conductimétrie, convertir C et [H₃O⁺] sur une ligne à part (mol/L ↔ mol/m³)",
    "dans un exercice mêlé, repérer les questions de ce chapitre (τ, équation avec l'eau) : elles sont rapides et rapportent 1 à 1,5 pt",
]

ANALOGIES = [
    {"image": "le ballon qu'on se passe : un acide lance un proton H⁺, une base l'attrape", "limite": "le proton ne vole pas librement dans l'eau : il passe directement d'une espèce à l'autre"},
    {"image": "le marché du souk à midi : autant de gens entrent que sortent, la foule reste la même — équilibre dynamique", "limite": "à l'équilibre les deux « portes » n'ont pas besoin d'avoir le même nombre de personnes de chaque côté, seulement le même débit"},
    {"image": "τ comme une note sur 1 : 0,040, c'est 4 % du chemin possible", "limite": "ce n'est pas une vitesse ni une durée : c'est la part de l'acide qui a réagi à la fin"},
    {"image": "la dilution : dans une salle plus grande, les paires (CH₃COO⁻, H₃O⁺) se retrouvent moins souvent, le sens 2 ralentit, plus d'acide reste dissocié", "limite": "image qualitative seulement ; la valeur de τ se calcule toujours par 10^(−pH)/C"},
]

A_NE_PAS_DIRE = [
    {"terme": "pH = log[H₃O⁺] (sans le signe moins)", "motif": r"pH\s*=\s*log|\[H₃O⁺\]\s*=\s*10\^?\(?pH", "pourquoi": "le pH serait négatif", "dire_plutot": "pH = −log[H₃O⁺] ; [H₃O⁺] = 10^(−pH)"},
    {"terme": "[H⁺] pour la concentration", "motif": r"\[H⁺\]", "pourquoi": "dans l'eau le proton est porté par H₃O⁺ (notation des sujets)", "dire_plutot": "[H₃O⁺]"},
    {"terme": "τ = x_max/x_f", "motif": r"τ\s*=\s*x_?max\s*/\s*x_?f", "pourquoi": "inversé : τ serait supérieur à 1", "dire_plutot": "τ = x_f/x_max"},
    {"terme": "à l'équilibre la réaction s'arrête", "motif": r"(l'[ée]quilibre|la r[ée]action|les r[ée]actions).{0,20}(s'arr[êe]te|est arr[êe]t[ée]e|sont arr[êe]t[ée]es|ne se fait plus|ne se font plus)|plus rien ne se passe|[ée]quilibre statique", "pourquoi": "l'équilibre est dynamique : les deux sens continuent à la même vitesse", "dire_plutot": "les deux réactions continuent, à la même vitesse ; les quantités ne changent plus"},
    {"terme": "la dilution diminue τ", "motif": r"dilu\w*.{0,30}(diminue|baisse|r[ée]duit|fait baisser).{0,10}(τ|le taux)", "pourquoi": "faux : 2021 R et 2025 R montrent l'inverse", "dire_plutot": "plus la solution est diluée, plus τ est grand"},
    {"terme": "OH⁻", "motif": r"\bOH⁻", "pourquoi": "notation des sujets marocains : HO⁻", "dire_plutot": "HO⁻"},
    {"terme": "Qr, K, Ka, pKa, Ke (chapitres suivants)", "motif": r"\bQ_?r\b|quotient de r[ée]action|constante d'([ée]quilibre|acidit[ée])|\bp?K[ae]\b|produit ionique|autoprotolyse|pr[ée]dominan", "pourquoi": "état d'équilibre et réactions acide-base : chapitres 12 et 13", "dire_plutot": "on le verra au chapitre suivant"},
    {"terme": "degré d'ionisation, Ostwald, Henderson, Lewis, Arrhenius", "motif": r"degr[ée] d'ionisation|coefficient de dissociation|ostwald|loi de dilution|henderson|hasselbalch|lewis|arrh[ée]nius", "pourquoi": "hors programme (perimetre.json acides_bases)", "dire_plutot": "taux d'avancement final τ ; acide et base selon Brønsted"},
    {"terme": "une réaction limitée = une réaction lente", "motif": r"limit[ée]e?,? (c'est|donc|car) (lente|elle est lente)|lente (donc|car) limit", "pourquoi": "limitée concerne l'état final (τ < 1), lente concerne la durée : l'acide éthanoïque réagit vite avec l'eau et sa réaction est limitée", "dire_plutot": "limitée : τ < 1 ; lente ou rapide : c'est la durée"},
]

EXCLUS = [
    "quotient de réaction Qr, Qr,éq, constante d'équilibre K, sens d'évolution spontanée : chapitre 12 (etat_equilibre) — les nationaux les demandent dans le même exercice",
    "produit ionique de l'eau Ke, [HO⁻] = Ke/[H₃O⁺], τ d'une base : chapitre 13 (acides_bases) ; ici on écrit seulement l'équation d'une base avec l'eau",
    "constante d'acidité Ka, pKa, pH = pKa + log, espèce prédominante, diagramme de distribution, indicateurs colorés, dosage : chapitres 13 et dosage",
    "degré d'ionisation, loi de dilution d'Ostwald, Henderson-Hasselbalch, activité, Lewis, Arrhenius : hors programme (perimetre.json)",
    "estérification, hydrolyse, rendement, anhydride : chapitre esterification_hydrolyse (semestre 2) ; ici seulement « lente et limitée » comme exemple (e5, e6)",
    "vitesse, t₁/₂, facteurs cinétiques : chapitre précédent (cinetique)",
]
