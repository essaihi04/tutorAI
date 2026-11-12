"""Exploration cinetique, partie A : en-tête, sources, cadre, nationaux, pièges, décisions.
Importé par explo.py (même dossier)."""

EXAMS = [f"backend/data/exams/physique/{a}-{s}" for a in range(2016, 2026) for s in ("normale", "rattrapage")]
SUIVI = ["2016-rattrapage", "2017-normale", "2017-rattrapage", "2018-rattrapage", "2019-rattrapage",
         "2021-normale", "2023-normale", "2024-normale", "2025-normale", "2025-rattrapage"]

ENTETE = {
    "cle": "cinetique",
    "matiere": "Physique-Chimie",
    "filiere": "2e Bac Sciences Physiques BIOF (Maroc)",
    "titre": "Suivi temporel d'une transformation chimique, vitesse de réaction",
    "date_exploration": "2026-11-12",
    "_note": ("Exploration faite par la routine cloud du 12 novembre 2026 pour le cours phys_ch10_cinetique. VIDÉOS NON AUDITÉES : "
              "YouTube est bloqué depuis le conteneur cloud. Appui : les 20 nationaux PC 2016-2025 du dépôt (10 ont un suivi temporel ; "
              "cinetique_build/nationaux.md, figures regardées et nombres recalculés avec python), la grille officielle du barème 2024 N "
              "(capacités citées), perimetre.json (clé cinetique), l'ancien cours chem_ch1_kinetics_course_v1.json (regardé, simulations "
              "non reprises) et le contrat des simulations cinetique_contrat_simulations.md (exemples A, B, C ; vues ; diapositives servies). "
              "À compléter par 10 audits vidéo depuis le PC avant validation. Le chapitre précédent (transformations_lentes_rapides) a "
              "déjà traité facteurs cinétiques, catalyseur et trempe ; ici on les rappelle seulement."),
}

SOURCES = {
    "videos": [],
    "videos_note": ("aucune : YouTube inaccessible depuis le conteneur cloud (12/11/2026) ; vidéos non auditées ; 10 audits à faire depuis "
                    "le PC (recherche « التتبع الزمني لتحول كيميائي سرعة التفاعل 2 باك », « suivi temporel vitesse de réaction 2bac biof »)"),
    "examens": EXAMS,
    "examens_avec_suivi_temporel": [f"backend/data/exams/physique/{s}" for s in SUIVI],
    "autres": [
        "outils/cours/notes/cours/cinetique_build/nationaux.md (relecture des 20 sujets, 10 figures pour figures.html)",
        "outils/cours/notes/cours/cinetique_contrat_simulations.md (exemples A, B, C, vues, diapositives servies)",
        "backend/data/curriculum/perimetre.json (clé cinetique)",
        "backend/data/exams/physique/2024-normale/extraction.json (grille officielle : capacités du cadre citées)",
        "backend/data/courses/chem_ch1_kinetics_course_v1.json (ancien cours, regardé seulement)",
        "backend/data/curriculum/exploration/transformations_lentes_rapides.json (chapitre précédent, modèle)",
    ],
}

COMPARAISON = {
    "_note": "sans vidéos : comparaison faite entre les corrigés des 10 nationaux avec suivi temporel, la grille officielle 2024 N et l'ancien cours",
    "convergences": [
        "suivre une transformation : mesurer une grandeur à différentes dates et en déduire l'avancement x(t)",
        "tableau d'avancement : état initial, en cours (x), état final (x_max) ; le réactif limitant donne la plus petite valeur de x_max",
        "vitesse volumique v(t) = (1/V)·dx/dt, obtenue par le coefficient directeur de la tangente à la courbe x(t) à la date t",
        "la vitesse diminue au cours du temps car la concentration des réactifs diminue ; elle est maximale à t = 0",
        "t₁/₂ : durée au bout de laquelle l'avancement atteint la moitié de sa valeur finale, x(t₁/₂) = x_f/2, lu sur la courbe",
        "en conductimétrie, une relation affine σ(x) (ou G(x)) donnée par l'énoncé permet de passer de σ à x",
    ],
    "variantes_admises": [
        {"variante": "t₁/₂ défini avec x_max/2 ou avec x_f/2", "decision": "x_f/2 (définition du corrigé 2021 N et de la grille) ; on dit que pour une transformation totale x_f = x_max (2016 R, 2018 R écrivent x_max/2)"},
        {"variante": "unité de v : mol·L⁻¹·s⁻¹, mmol·L⁻¹·min⁻¹, mol·m⁻³·min⁻¹, mmol·L⁻¹·h⁻¹", "decision": "on prend l'unité demandée par l'énoncé ; le cours calcule en mmol·L⁻¹·min⁻¹ (exemple A) et montre le passage en mol·m⁻³ (r1, r2)"},
        {"variante": "v notée v ou ν (2016 R)", "decision": "v ; on dit une fois que certains sujets écrivent ν"},
        {"variante": "conductimétrie par G (2018 R) ou par σ (2016 R, 2021 N)", "decision": "G = k·σ (g1) puis σ partout ; G₁/₂ traité en n7"},
        {"variante": "explication de la baisse de vitesse par les « chocs efficaces » (grille 2024 N)", "decision": "non dit (perimetre.json : hors programme) ; « les entités de réactif sont moins nombreuses, elles se rencontrent moins souvent » ; décision à faire valider"},
    ],
    "meilleures_explications": [
        "trempe : le prélèvement versé dans l'eau glacée ne change plus de couleur, le grand bécher continue de brunir (une photo)",
        "vitesse : la pente de la courbe x(t) ; un triangle « Δx en Δt » raide au début, plat à la fin",
        "conductimétrie de la saponification : un HO⁻ (ion rapide, grand λ) remplacé par un CH₃COO⁻ (ion lent, petit λ) : σ descend",
        "t₁/₂ : quatre gestes (x_f sur le palier, x_f/2 sur l'axe, horizontale, verticale)",
    ],
}

CADRE = {
    "_note": ("Fiche du chapitre, même forme que cadre_reference_2bac_pc.json. Capacités d'après CDR-PC-2015 (annexe 1 « Suivi temporel d'une "
              "transformation – vitesse de réaction » ; annexe 2 TP « Suivi temporel par mesure de conductance »), OP-PC-2007, perimetre.json "
              "(clé cinetique), la grille officielle 2024 N (capacités citées mot à mot) et les nationaux 2016-2025. Texte officiel du cadre non "
              "relu en entier : CIN1 à CIN8 provisoires. Formules écrites exactement comme le contrat des simulations."),
    "titre": "Suivi temporel d'une transformation chimique, vitesse de réaction",
    "source": ("CDR-PC-2015, annexe 1, Chimie, sous-domaine 1 « Transformations rapides et lentes d'un système chimique » : « Suivi temporel "
               "d'une transformation – vitesse de réaction (tableau d'avancement, vitesse volumique, temps de demi-réaction) » ; annexe 2, TP "
               "« Suivi temporel par mesure de conductance » ; OP-PC-2007, 2BAC : suivi par titrage, conductimétrie, mesure de pression ou de "
               "volume de gaz ; grille officielle du barème 2024 N ; perimetre.json clé cinetique ; nationaux PC 2016-2025 du dépôt."),
    "capacites": [
        {"id": "CIN1", "texte": "Connaître le principe du suivi temporel d'une transformation (titrage d'un prélèvement après trempe, conductimétrie, mesure de pression ou de volume d'un gaz) et choisir une méthode adaptée."},
        {"id": "CIN2", "texte": "Dresser le tableau d'avancement d'une réaction et l'exploiter : avancement maximal x_max, réactif limitant, composition à une date t."},
        {"id": "CIN3", "texte": "Déterminer l'avancement x à une date t à partir d'un titrage, d'une mesure de conductance ou de conductivité (G = k·σ, σ = Σ λᵢ·[Xᵢ]) ou d'une mesure de pression ou de volume de gaz."},
        {"id": "CIN4", "texte": "Tracer et exploiter la courbe x = f(t) (ou n, σ, G en fonction de t) : lecture de x, de la composition et de l'avancement final x_f."},
        {"id": "CIN5", "texte": "Connaître l'expression de la vitesse volumique de réaction v(t) = (1/V)·dx/dt et la déterminer graphiquement (coefficient directeur de la tangente)."},
        {"id": "CIN6", "texte": "Connaître l'évolution de la vitesse au cours du temps (elle diminue, nulle à la fin) et l'influence de la concentration des réactifs et de la température sur la vitesse volumique."},
        {"id": "CIN7", "texte": "Définir le temps de demi-réaction t₁/₂ et le déterminer graphiquement ou en exploitant des résultats expérimentaux ; comparer deux transformations par leur t₁/₂."},
        {"id": "CIN8", "texte": "Rédiger un exercice de suivi temporel du national : relation littérale, application numérique avec unités cohérentes, résultat avec son unité."},
    ],
    "formules": [
        {"id": "f_vitesse", "ecriture": "v(t) = (1/V)·dx/dt", "capacite": "CIN5", "dit": "la vitesse volumique égale un sur V fois dx sur dt", "phrase": "dx/dt est le coefficient directeur de la tangente à la courbe x(t) à la date t ; V en litres", "unite": "mol·L⁻¹·min⁻¹ (ou mmol·L⁻¹·min⁻¹)"},
        {"id": "f_demi", "ecriture": "x(t₁/₂) = x_f/2", "capacite": "CIN7", "dit": "x à t un demi égale x f sur deux", "phrase": "t₁/₂ : durée au bout de laquelle l'avancement atteint la moitié de sa valeur finale"},
        {"id": "f_conductance", "ecriture": "G = k·σ", "capacite": "CIN3", "dit": "G égale k fois sigma", "phrase": "k : constante de cellule (en m) ; σ en S/m ; G en S"},
        {"id": "f_conductivite", "ecriture": "σ = Σ λᵢ·[Xᵢ]", "capacite": "CIN3", "dit": "sigma égale la somme des lambda i fois la concentration de l'ion i", "phrase": "λ en S·m²·mol⁻¹, [X] en mol/m³ ; 1 mol/L = 10³ mol/m³"},
        {"id": "f_sigma_x", "ecriture": "σ = σ₀ − (λ(HO⁻) − λ(CH₃COO⁻))·x/V", "capacite": "CIN3", "dit": "sigma égale sigma zéro moins (lambda HO moins lambda acétate) fois x sur V", "phrase": "exemple B : chaque HO⁻ consommé est remplacé par un CH₃COO⁻ ; V en m³"},
        {"id": "f_x_sigma", "ecriture": "x = x_max·(σ₀ − σ)/(σ₀ − σ_f)", "capacite": "CIN3", "dit": "x égale x max fois (sigma zéro moins sigma) sur (sigma zéro moins sigma f)", "phrase": "σ affine en x : on passe de σ lue à x"},
        {"id": "f_gaz", "ecriture": "(P − P₀)·V = n(H₂)·R·T", "capacite": "CIN3", "dit": "P moins P zéro, fois V, égale n de H deux fois R fois T", "phrase": "loi des gaz parfaits appliquée au gaz formé ; ici n(H₂) = x"},
        {"id": "f_x_pression", "ecriture": "x = (P − P₀)·V/(R·T)", "capacite": "CIN3", "dit": "x égale (P moins P zéro) fois V sur R T", "phrase": "P en Pa, V en m³, T en K, R = 8,31 Pa·m³·mol⁻¹·K⁻¹"},
        {"id": "f_quantite", "ecriture": "n = C·V", "capacite": "CIN2", "dit": "n égale C fois V", "phrase": "quantité de matière d'un soluté ; C en mol/L, V en L"},
        {"id": "f_equivalence", "ecriture": "n(I₂) = C·V_E/2", "capacite": "CIN3", "dit": "n de I deux égale C fois V E sur deux", "phrase": "à l'équivalence du titrage I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻ (dans le prélèvement)"},
        {"id": "f_volume_gaz", "ecriture": "x = V(H₂)/V_m", "capacite": "CIN3", "dit": "x égale V de H deux sur V m", "phrase": "volume de gaz recueilli, V_m = 24 L/mol dans les conditions de l'expérience"},
    ],
    "mots_cles": ["suivi temporel", "trempe", "prélèvement", "titrage", "équivalence", "conductimétrie", "conductance", "conductivité",
                  "conductivité molaire ionique", "constante de cellule", "pression", "manomètre", "tableau d'avancement", "avancement",
                  "avancement maximal", "avancement final", "réactif limitant", "vitesse volumique", "tangente", "coefficient directeur",
                  "temps de demi-réaction", "facteur cinétique"],
    "hors_cadre": {
        "_note": "termes à ne jamais écrire ni dire dans le cours (perimetre.json et contrat des simulations) ; les modèles des courbes servent au calcul seulement",
        "mots": ["chocs efficaces", "énergie d'activation", "ordre de réaction", "loi de vitesse", "constante de vitesse",
                 "mécanisme réactionnel", "Arrhenius", "Beer-Lambert", "exponentielle", "théorie des collisions"],
    },
    "valeurs_reference": {
        "exemple_A": {"equation": "H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O", "V_mL": 100, "n0_H2O2_mmol": 2.0, "n0_I_mmol": 10.0, "x_max_mmol": 2.0,
                      "mesures_t_min": [0, 2, 4, 6, 8, 10, 15, 20, 30, 40],
                      "mesures_x_mmol": [0, 0.44, 0.79, 1.06, 1.26, 1.43, 1.69, 1.84, 1.95, 1.99],
                      "t_demi_min": 5.5, "pente_0_mmol_min": 0.25, "v0": 2.5, "v8": 0.92, "v20": 0.21, "unite_v": "mmol·L⁻¹·min⁻¹",
                      "x_a_11_min": 1.5, "a_40C": {"t_demi_min": 1.8, "v0": 7.5},
                      "titrage": {"V_p_mL": 10.0, "C_mol_L": 0.020, "V_E_mL_a_8_min": 12.6, "n_I2_mmol": 1.26},
                      "composition_8_min_mmol": {"H2O2": 0.74, "I-": 7.48, "I2": 1.26}},
        "exemple_B": {"equation": "CH₃COOC₂H₅ + HO⁻ → CH₃COO⁻ + C₂H₅OH", "V_m3": 1.0e-4, "n0_mmol": 1.0, "C0_mol_L": 1.0e-2,
                      "lambda_mS_m2_mol": {"Na+": 5.01, "HO-": 19.9, "CH3COO-": 4.09},
                      "sigma0_S_m": 0.249, "sigma_f_S_m": 0.091, "t_demi_min": 10, "sigma_10_min_S_m": 0.170, "x_10_min_mmol": 0.50},
        "exemple_C": {"equation": "Mg + 2H⁺ → Mg²⁺ + H₂", "n0_Mg_mmol": 1.0, "V_gaz_L": 1.0, "T_K": 300, "P0_Pa": 1.013e5,
                      "R": 8.31, "P_max_moins_P0_Pa": 2.49e3, "V_H2_final_mL": 24, "V_m_L_mol": 24},
    },
}

INSISTANCES = [
    "on ne mesure jamais x directement : on mesure une grandeur (V_E, σ, P) à une date t et on en déduit x",
    "dans v = (1/V)·dx/dt, V est le volume du mélange, en litres (ou en m³ si l'unité demandée est en mol·m⁻³)",
    "dx/dt est la pente de la TANGENTE à la date t, pas la pente de la corde entre deux points de la courbe",
    "t₁/₂ se lit à x_f/2 sur l'axe des x, jamais au milieu de l'axe des temps",
    "à 2·t₁/₂ la transformation n'est pas finie",
    "la vitesse diminue au cours du temps parce que les réactifs sont consommés",
]

VALEURS_REPERES = [
    "exemple A : x(8 min) = 1,26 mmol ; t₁/₂ ≈ 5,5 min ; v(0) = 2,5, v(8) ≈ 0,92, v(20) ≈ 0,21 mmol·L⁻¹·min⁻¹ ; à 40 °C t₁/₂ ≈ 1,8 min, v(0) = 7,5",
    "exemple B : σ₀ = 0,249 S/m, σ_f = 0,091 S/m, σ(10 min) = 0,170 S/m → x = 0,50 mmol = x_max/2 → t₁/₂ = 10 min",
    "exemple C : P − P₀ = 2,49·10³ Pa à la fin → x = 1,0·10⁻³ mol ; V(H₂) = 24 mL",
    "nationaux : t₁/₂ de 70 s (2019 R) à 24 h (2024 N) ; v = 1,0·10⁻³ mol·L⁻¹·s⁻¹ (2019 R), 1,6 mmol·L⁻¹·min⁻¹ (2025 R), 0,78 mol·m⁻³·min⁻¹ (2021 N)",
]

CAS_TYPES = [
    {"cas": "lire t₁/₂ sur une courbe", "mots": "« Déterminer graphiquement t₁/₂ le temps de demi-réaction »", "methode": "x_f sur le palier (ou donné), x_f/2 sur l'axe, horizontale jusqu'à la courbe, verticale jusqu'à l'axe des t", "points": "0,25-0,75", "frequence": "9 sessions sur 10 avec suivi"},
    {"cas": "vitesse volumique par la tangente", "mots": "« Déterminer, en mol·L⁻¹·s⁻¹ (ou …), la vitesse volumique à l'instant t₁ ; (T) la tangente »", "methode": "deux points de (T) loin l'un de l'autre → pente Δx/Δt ; v = (1/V)·pente ; V converti ; unité demandée", "points": "0,5-1", "frequence": "5 sessions (2016 R, 2019 R, 2021 N, 2024 N, 2025 R)"},
    {"cas": "tableau d'avancement et x_max", "mots": "« Dresser le tableau d'avancement… Trouver x_max »", "methode": "trois lignes ; deux hypothèses ; la plus petite valeur ; réactif limitant", "points": "0,5-0,75", "frequence": "3 sessions (2016 R, 2019 R, 2021 N)"},
    {"cas": "relation σ(x) ou G(x) donnée", "mots": "« calculer σ₁/₂ (ou G₁/₂) quand x = x_max/2 » ; « montrer que v = −(1/(160·V₀))·dσ/dt »", "methode": "remplacer x = x_max/2 dans la relation, lire t sur σ(t) ; dériver la relation et remplacer dans v = (1/V)·dx/dt", "points": "0,5-0,75", "frequence": "3 sessions (2016 R, 2018 R, 2021 N)"},
    {"cas": "composition ou x_f sur le palier", "mots": "« Déterminer la composition du mélange à l'équilibre »", "methode": "lire le palier ; si c'est un réactif : x_f = n₀ − n_f ; remplir la ligne finale", "points": "0,5-1", "frequence": "3 sessions (2017 R, 2023 N, 2025 N)"},
    {"cas": "comparer deux courbes", "mots": "« En déduire la réaction la plus rapide » ; « la courbe qui correspond au catalyseur »", "methode": "t₁/₂ plus petit (palier atteint plus tôt) = plus rapide ; même palier si mêmes quantités", "points": "0,5-0,75", "frequence": "3 sessions (2017 N, 2023 N, 2025 N)"},
    {"cas": "vrai/faux sur la vitesse et t₁/₂", "mots": "« La vitesse volumique diminue au cours du temps » ; « terminée au bout de 2·t₁/₂ »", "methode": "vrai (la pente diminue, les réactifs s'épuisent) ; faux (à 2·t₁/₂ il reste un quart de chemin à peu près)", "points": "0,25-0,5", "frequence": "2 sessions (2024 N, 2025 R)"},
    {"cas": "définir t₁/₂", "mots": "« Définir le temps de demi-réaction »", "methode": "durée au bout de laquelle l'avancement atteint la moitié de sa valeur finale : x(t₁/₂) = x_f/2", "points": "0,25", "frequence": "1 session (2021 N)"},
    {"cas": "trempe", "mots": "« rôle de l'eau glacée »", "methode": "refroidir brusquement pour bloquer la réaction et doser la quantité présente à cette date", "points": "0,25", "frequence": "1 session (2017 R)"},
]

PIEGES = [
    {"erreur": "V en mL dans v = (1/V)·dx/dt", "geste": "écrire V = 100 mL = 0,100 L avant le calcul ; en m³ si l'unité demandée est en mol·m⁻³"},
    {"erreur": "lire t₁/₂ au milieu de l'axe des temps (t_final/2)", "geste": "on part de l'axe des x : x_f/2, puis horizontale, puis verticale"},
    {"erreur": "lire t₁/₂ à n₀/2 sur une courbe de réactif ou à σ₀/2 sur une courbe de conductivité", "geste": "calculer d'abord la valeur à t₁/₂ : n₀ − x_f/2 (2023 N : 0,6 mol) ou σ₁/₂ par la relation donnée (2021 N : 0,17 S/m)"},
    {"erreur": "prendre la pente entre deux points de la courbe au lieu de la tangente", "geste": "deux points de la tangente (T), éloignés, lus sur le quadrillage"},
    {"erreur": "σ en mS/m (ou G en mS) utilisée comme S/m (ou S)", "geste": "convertir : 170 mS/m = 0,170 S/m"},
    {"erreur": "[X] en mol/L dans σ = Σ λᵢ·[Xᵢ]", "geste": "1 mol/L = 10³ mol/m³ : 1,0·10⁻² mol/L = 10 mol/m³"},
    {"erreur": "croire la transformation finie à 2·t₁/₂", "geste": "regarder la courbe : à 2·t₁/₂, x ≈ 3/4 de x_f seulement (exemple A : 1,5 mmol sur 2,0)"},
    {"erreur": "dire que la vitesse augmente parce que x augmente", "geste": "x augmente, mais de moins en moins vite : la pente diminue"},
]

ERREURS_EXAMEN = [
    {"erreur": "unité de v fausse ou absente", "geste": "écrire l'unité demandée dans l'énoncé (mol·L⁻¹·s⁻¹, mmol·L⁻¹·h⁻¹…)", "source": "2019 R, 2024 N, 2025 R"},
    {"erreur": "V₀ laissé en mL avec une unité en mol·m⁻³", "geste": "V₀ = 100 mL = 10⁻⁴ m³", "source": "2016 R, 2021 N"},
    {"erreur": "signe de la pente de σ(t) gardé dans v", "geste": "v = −(1/(160·V₀))·dσ/dt : dσ/dt < 0, donc v > 0", "source": "2021 N"},
    {"erreur": "t₁/₂ lu à x_max/2 quand x_f < x_max", "geste": "x_f/2 de chaque courbe (0,1 et 0,15 mol)", "source": "2017 N"},
    {"erreur": "temps lu dans la mauvaise unité (s, min, h)", "geste": "recopier l'unité de l'axe : 70 s, 3,5 h, 24 h", "source": "2019 R, 2023 N, 2024 N"},
    {"erreur": "t₁/₂ lu à n₀/2 sur la courbe de l'acide", "geste": "n_A = n₀ − x_f/2 = 0,6 mol", "source": "2023 N"},
]

CONSEILS = [
    "relation littérale d'abord, puis application numérique, puis résultat avec l'unité demandée (règle des corrigés)",
    "marquer sur la figure les deux points de la tangente utilisés et les écrire dans la copie",
    "pour t₁/₂, écrire la valeur cherchée (x_f/2, σ₁/₂ ou n₁/₂) avant de lire le temps",
    "convertir les volumes en une ligne séparée (V = 50 mL = 0,050 L)",
]

ANALOGIES = [
    {"image": "la trempe est une photo : on fige le prélèvement pour le doser tranquillement, pendant que le reste continue", "limite": "le froid ralentit très fort, il n'arrête pas absolument ; c'est assez pour la durée du dosage"},
    {"image": "la vitesse est comme la vitesse d'une voiture sur un graphique distance-temps : la pente de la courbe à un instant", "limite": "ici on divise en plus par le volume V (vitesse « par litre »)"},
    {"image": "la foule qui sort d'une salle : au début beaucoup de monde sort chaque minute, à la fin peu de gens restent, le débit baisse", "limite": "image pour la baisse de vitesse seulement ; les entités ne font pas la queue"},
    {"image": "t₁/₂ comme la mi-temps d'un trajet en quantité : la moitié du chemin en avancement, pas la moitié de la durée", "limite": "le second « demi-chemin » prend plus de temps que le premier"},
]

A_NE_PAS_DIRE = [
    {"terme": "la vitesse augmente au cours du temps", "motif": r"(la )?vitesse (volumique )?(augmente|cro[iî]t) (au cours|avec le) (du )?temps", "pourquoi": "la vitesse diminue : la pente de x(t) baisse (2025 R 3.2)", "dire_plutot": "x augmente, mais la vitesse diminue au cours du temps"},
    {"terme": "t₁/₂ = t_final/2", "motif": r"t[₁1]\s*/\s*[₂2]\s*=\s*t_?(final|f|fin)\s*/\s*2|moiti[ée] de la dur[ée]e (totale|de la r[ée]action)", "pourquoi": "t₁/₂ se lit à x_f/2 ; la seconde moitié de l'avancement prend plus longtemps", "dire_plutot": "x(t₁/₂) = x_f/2"},
    {"terme": "à 2 t₁/₂ la réaction est finie", "motif": r"(à|au bout de|apr[èe]s) 2\s*[·.×]?\s*t[₁1]\s*/\s*[₂2],? (la r[ée]action|la transformation|l'[ée]volution) est (toujours )?(finie|termin[ée]e|achev[ée]e)", "pourquoi": "faux (2024 N 1.b) : à 2·t₁/₂, x ≈ 3/4 de x_f (exemple A : 1,5 sur 2,0 mmol)", "dire_plutot": "à 2·t₁/₂ la transformation n'est pas finie"},
    {"terme": "t₁/₂ = moitié du temps", "motif": r"temps de demi-r[ée]action.{0,40}moiti[ée] du temps", "pourquoi": "définition par l'avancement, pas par le temps", "dire_plutot": "durée au bout de laquelle l'avancement atteint la moitié de sa valeur finale"},
    {"terme": "pente entre deux points de la courbe", "motif": r"(corde|deux points de la courbe).{0,40}(vitesse|pente)", "pourquoi": "la vitesse à la date t est la pente de la tangente", "dire_plutot": "coefficient directeur de la tangente à la date t"},
    {"terme": "V en millilitres dans la vitesse", "motif": r"1\s*/\s*100\s*[×x·]\s*0[,.]25", "pourquoi": "V = 100 mL = 0,100 L : v(0) = (1/0,100) × 0,25", "dire_plutot": "V en litres"},
    {"terme": "chocs efficaces / théorie des collisions", "motif": r"chocs? efficaces?|th[ée]orie des collisions", "pourquoi": "hors programme (perimetre.json), même si la grille 2024 N le cite (décision à valider)", "dire_plutot": "les entités de réactif sont moins nombreuses, elles se rencontrent moins souvent"},
    {"terme": "ordre, loi de vitesse, constante de vitesse, exponentielle", "motif": r"ordre (de r[ée]action|1|2)|loi de vitesse|constante de vitesse|exponentielle|arrh[ée]nius|[ée]nergie d'activation|beer.?lambert|m[ée]canisme r[ée]actionnel", "pourquoi": "hors programme ; les modèles des courbes ne sont jamais écrits", "dire_plutot": "on lit la courbe"},
    {"terme": "le catalyseur augmente x_f", "motif": r"catalyseur (augmente|change|modifie) (x_?f|l'avancement final|l'[ée]tat final|le rendement)", "pourquoi": "même état final (2025 N 2.3)", "dire_plutot": "le catalyseur accélère, x_f est le même"},
]

EXCLUS = [
    "chocs efficaces, théorie des collisions, énergie d'activation, loi d'Arrhenius : hors programme (perimetre.json) ; la grille officielle 2024 N cite les chocs efficaces : décision à valider",
    "ordre de réaction, loi de vitesse, constante de vitesse, mécanisme réactionnel : hors programme",
    "suivi par spectrophotométrie (Beer-Lambert) : hors programme marocain du chapitre, jamais au national",
    "forme mathématique des courbes (exponentielle, hyperbole) : jamais écrite ; les modèles servent seulement à dessiner",
    "types de catalyse : vus (définition seulement) au chapitre précédent",
    "quotient de réaction, taux d'avancement final, K : chapitres suivants (2017 N 2.3, 2023 N 3.5 les demandent dans le même exercice)",
]
