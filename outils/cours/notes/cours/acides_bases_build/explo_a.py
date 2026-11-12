"""Exploration acides_bases, partie A : en-tête, sources, cadre, nationaux, pièges, décisions.
Importé par explo.py (même dossier)."""

EXAMS = [f"backend/data/exams/physique/{a}-{s}" for a in range(2016, 2026) for s in ("normale", "rattrapage")]
AVEC_CHAPITRE = ["2016-normale", "2017-normale", "2018-normale", "2019-normale", "2019-rattrapage", "2020-normale", "2020-rattrapage",
                 "2021-normale", "2021-rattrapage", "2022-normale", "2022-rattrapage", "2023-normale", "2023-rattrapage", "2024-normale",
                 "2024-rattrapage", "2025-normale", "2025-rattrapage"]
AVEC_DOSAGE = ["2016-normale", "2018-normale", "2019-rattrapage", "2020-normale", "2021-normale", "2021-rattrapage", "2022-normale",
               "2022-rattrapage", "2023-rattrapage", "2024-normale", "2024-rattrapage", "2025-normale", "2025-rattrapage"]

ENTETE = {
    "cle": "acides_bases",
    "matiere": "Physique-Chimie",
    "filiere": "2e Bac Sciences Physiques BIOF (Maroc)",
    "titre": "Transformations liées aux réactions acide-base",
    "date_exploration": "2026-11-12",
    "_note": ("Exploration faite par la routine cloud du 12 novembre 2026 pour le cours phys_ch13_acides_bases. VIDÉOS NON AUDITÉES : "
              "YouTube est bloqué depuis le conteneur cloud (yt-dlp non tenté). Appui : les 20 nationaux PC 2016-2025 du dépôt (17 touchent "
              "ce chapitre, 13 ont un dosage ; acides_bases_build/nationaux.md, 5 figures regardées, nombres recalculés avec python), "
              "perimetre.json (clés acides_bases ET dosage), programme_semestre1.json (ordre 13, pas de clé dosage : le dosage reste DANS ce "
              "cours, partie finale) et le contrat des simulations acides_bases_contrat_simulations.md (exemples A à N, courbes de dosage "
              "calculées ; vues ; diapositives servies). Chapitres précédents déjà construits : phys_ch11_transformations_deux_sens (Brønsted, "
              "pH, τ) et phys_ch12_etat_equilibre (Qr, K, K = C·τ²/(1 − τ)) — rappelés en deux diapositives (r1, r2) ; ils renvoyaient ici "
              "Ke, autoprotolyse, Ka, pKa, τ d'une base, K = Ka₁/Ka₂, prédominance, indicateur coloré, dosage : tout est repris. Pas d'ancien "
              "cours de ce chapitre dans backend/data/courses/. À compléter par 10 audits vidéo depuis le PC avant validation. La comparaison "
              "de Qr,i à K pour prévoir le sens (piles, semestre 2) reste renvoyée."),
}

SOURCES = {
    "videos": [],
    "videos_note": ("aucune : YouTube inaccessible depuis le conteneur cloud (12/11/2026) ; vidéos non auditées ; 10 audits à faire depuis "
                    "le PC (recherche « التحولات المقرونة بالتفاعلات حمض قاعدة 2 باك », « réactions acido-basiques 2bac biof Ka pKa », "
                    "« dosage acido-basique 2 bac biof méthode des tangentes »)"),
    "examens": EXAMS,
    "examens_avec_le_chapitre": [f"backend/data/exams/physique/{s}" for s in AVEC_CHAPITRE],
    "examens_avec_dosage": [f"backend/data/exams/physique/{s}" for s in AVEC_DOSAGE],
    "autres": [
        "outils/cours/notes/cours/acides_bases_build/nationaux.md (relecture des 20 sujets, 5 figures pour figures.html)",
        "outils/cours/notes/cours/transformations_deux_sens_build/nationaux.md et etat_equilibre_build/nationaux.md (questions renvoyées ici)",
        "outils/cours/notes/cours/acides_bases_contrat_simulations.md (exemples A à N, vues, diapositives servies)",
        "backend/data/curriculum/perimetre.json (clés acides_bases et dosage : notions, méthodes, démonstrations, termes hors programme)",
        "backend/data/curriculum/programme_semestre1.json (ordre 13, clé acides_bases ; pas de clé dosage)",
        "backend/data/curriculum/prerequis.json (logarithme_decimal_puissances, tableau_avancement, concentration_quantite_matiere, conductimetrie)",
        "backend/data/curriculum/exploration/etat_equilibre.json (chapitre précédent, modèle)",
        "backend/data/courses/phys_ch11_transformations_deux_sens.json et phys_ch12_etat_equilibre.json (cours précédents : exemples repris)",
    ],
}

COMPARAISON = {
    "_note": "sans vidéos : comparaison faite entre les corrigés des 17 nationaux qui touchent le chapitre, perimetre.json et les deux chapitres précédents",
    "convergences": [
        "Ka = [A⁻]éq·[H₃O⁺]éq/[AH]éq est la constante d'équilibre K de la réaction de l'acide avec l'eau (2017 N, 2019 N « K représente Ka », 2021 N, 2022 N)",
        "pKa = −log Ka, calculé à partir de Qr,éq (6 sessions) ; pour une base, Ka = Ke/Qr,éq (2020 N, 2020 R, 2022 R)",
        "[HO⁻] = Ke/[H₃O⁺] = 10^(pH − 14) pour le τ d'une base (2020 N, 2020 R, 2022 R)",
        "K d'une réaction acide-base = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁) (2020 R, 2023 N) ; avec HO⁻ : K = Ka/Ke (2016 N, 2024 N, 2025 N)",
        "pH = pKa + log([A⁻]/[AH]) puis prédominance (pH > pKa : la base) — 11 sessions",
        "dosage : équation avec →, C_A·V_A = C_B·V_BE, V_E par les tangentes parallèles ou le maximum de dpH/dV, indicateur dont la zone contient pH_E (13 sessions)",
    ],
    "variantes_admises": [
        {"variante": "Ka ou K_A ; pKa ou pK_A", "decision": "Ka et pKa à l'écran (indice a), comme perimetre.json ; « K a » et « p K a » à la voix"},
        {"variante": "[X]éq, [X]_éq ou [X]_f", "decision": "[X]_éq dans les formules (comme le chapitre 12) ; jamais [X]_f pour une concentration d'équilibre"},
        {"variante": "V_BE, V_bE, V_E ; V_AE, V_aE", "decision": "V_BE (base versée) et V_AE (acide versé) ; on lit la notation du sujet dans les nationaux"},
        {"variante": "méthode des tangentes ou des droites parallèles", "decision": "« méthode des tangentes parallèles » (perimetre.json : méthode des tangentes) ; « droites parallèles » dit une fois (2018 N)"},
        {"variante": "pH au dixième ou au centième", "decision": "pH-mètre au centième pour une solution mesurée (3,41 ; 10,60 ; comme le chapitre 12) ; courbes de dosage lues au dixième (8,3 ; 4,8)"},
        {"variante": "K = Ka₁/Ka₂ ou Ka₂/Ka₁ (2020 R)", "decision": "règle : Ka du couple de l'acide qui réagit au numérateur ; dans un sujet, lire qui est Ka₁"},
    ],
    "meilleures_explications": [
        "trois béchers incolores, trois pH, trois couleurs de BBT : l'eau « cache » des ions H₃O⁺ et HO⁻ en nombres différents",
        "Ka n'est pas une nouvelle grandeur : c'est le K du chapitre précédent, pour la réaction d'un acide avec l'eau (1,57·10⁻⁵ retrouvé)",
        "un curseur glisse sur l'axe des pH : à gauche du pKa l'acide prédomine, à droite la base ; au pKa les deux courbes se croisent",
        "la courbe de dosage se trace goutte à goutte : on VOIT le saut, puis les tangentes parallèles posent E",
        "à la demi-équivalence, il reste autant d'acide qu'il s'est formé de base : pH = pKa se lit sur la courbe",
    ],
}

CADRE = {
    "_note": ("Fiche du chapitre, même forme que cadre_reference_2bac_pc.json. Capacités d'après CDR-PC-2015 (annexe 1, Chimie, sous-domaine 2 "
              "« Transformations associées à des réactions acido-basiques (produit ionique de l'eau, constante d'acidité Ka, pKa … dosage "
              "acido-basique) » ; annexe 2, TP « Dosage par mesure de pH »), OP-PC-2007, perimetre.json (clés acides_bases et dosage : notions, "
              "méthodes autorisées, démonstrations attendues et admises) et les nationaux 2016-2025. Texte officiel du cadre non relu en entier : "
              "AB1 à AB10 provisoires. Formules écrites exactement comme le contrat des simulations."),
    "titre": "Transformations liées aux réactions acide-base",
    "source": ("CDR-PC-2015, annexe 1, Chimie, sous-domaine 2 « Transformations non totales d'un système chimique » : « Transformations "
               "associées à des réactions acido-basiques (produit ionique de l'eau, constante d'acidité Ka, pKa) » et dosage acido-basique ; "
               "annexe 2 : TP « Dosage par mesure de pH » ; OP-PC-2007, 2BAC : autoprotolyse de l'eau, Ke, Ka, pKa, comparaison des acides et "
               "des bases, diagramme de prédominance, indicateurs colorés, dosage pH-métrique, équivalence, tangentes, demi-équivalence ; "
               "perimetre.json clés acides_bases et dosage ; nationaux PC 2016-2025 du dépôt."),
    "capacites": [
        {"id": "AB1", "texte": "Écrire l'équation de l'autoprotolyse de l'eau ; connaître le produit ionique Ke = [H₃O⁺]·[HO⁻] = 1,0·10⁻¹⁴ à 25 °C et pKe = 14 ; reconnaître une solution acide, neutre ou basique ; calculer [HO⁻] = Ke/[H₃O⁺]."},
        {"id": "AB2", "texte": "Calculer le pH d'une solution basique (soude) et le taux d'avancement final de la réaction d'une base avec l'eau à partir de son pH (par Ke)."},
        {"id": "AB3", "texte": "Écrire la constante d'acidité Ka d'un couple AH/A⁻ (constante de la réaction de l'acide avec l'eau) ; définir pKa = −log Ka ; calculer Ka ou pKa à partir d'une mesure (pH, Qr,éq) ; Ka = Ke/Qr,éq pour la réaction d'une base ; pKa des couples de l'eau (0 et 14)."},
        {"id": "AB4", "texte": "Comparer le comportement de deux acides (ou deux bases) de même concentration à l'aide de Ka ou pKa (τ, pH) ; classer des couples sur un axe des pKa."},
        {"id": "AB5", "texte": "Exprimer la constante d'équilibre d'une réaction acide-base en fonction des Ka des deux couples : K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁) ; K = Ka/Ke pour la réaction d'un acide avec HO⁻."},
        {"id": "AB6", "texte": "Établir pH = pKa + log([A⁻]_éq/[AH]_éq) ; déterminer l'espèce qui prédomine (domaines de prédominance) ; exploiter un diagramme de distribution (pKa au croisement, pourcentages)."},
        {"id": "AB7", "texte": "Expliquer le fonctionnement d'un indicateur coloré (couple HInd/Ind⁻, zone de virage qui encadre son pKa) et le choisir pour un dosage (zone de virage qui contient pH_E)."},
        {"id": "AB8", "texte": "Décrire un dosage acido-basique (montage, solution titrante et titrée) ; écrire l'équation de la réaction de dosage (rapide, totale, unique) ; définir l'équivalence et utiliser C_A·V_A = C_B·V_BE (concentration, dilution, masse, concentration massique)."},
        {"id": "AB9", "texte": "Exploiter une courbe de dosage pH = f(V) : équivalence par la méthode des tangentes parallèles ou par le maximum de dpH/dV ; nature du pH à l'équivalence ; pH = pKa à la demi-équivalence ; exploiter une courbe σ = f(V) (rupture de pente)."},
        {"id": "AB10", "texte": "Rédiger un exercice du national : équation, relation littérale, application numérique avec unité, lecture graphique justifiée, conclusion (prédominance, indicateur, réaction totale)."},
    ],
    "formules": [
        {"id": "f_autoprotolyse", "ecriture": "2H₂O ⇌ H₃O⁺ + HO⁻", "capacite": "AB1", "dit": "deux H deux O double flèche H trois O plus plus H O moins", "phrase": "autoprotolyse de l'eau : réaction entre deux molécules d'eau"},
        {"id": "f_ke", "ecriture": "Ke = [H₃O⁺]·[HO⁻]", "capacite": "AB1", "dit": "K e égale la concentration des ions H trois O plus fois la concentration des ions H O moins", "phrase": "produit ionique de l'eau ; vrai dans toute solution aqueuse", "unite": "sans unité"},
        {"id": "f_ke_valeur", "ecriture": "Ke = 1,0·10⁻¹⁴", "capacite": "AB1", "dit": "K e égale dix puissance moins quatorze, à vingt-cinq degrés", "phrase": "à 25 °C"},
        {"id": "f_pke", "ecriture": "pKe = −log Ke = 14", "capacite": "AB1", "dit": "p K e égale moins log de K e, égale quatorze"},
        {"id": "f_ph", "ecriture": "pH = −log[H₃O⁺]", "capacite": "AB1", "dit": "p H égale moins log de la concentration des ions H trois O plus", "phrase": "rappel du chapitre 11 ; [H₃O⁺] en mol/L"},
        {"id": "f_ho", "ecriture": "[HO⁻] = Ke/[H₃O⁺]", "capacite": "AB1", "dit": "la concentration des ions H O moins égale K e sur la concentration des ions H trois O plus", "unite": "mol/L"},
        {"id": "f_ho_ph", "ecriture": "[HO⁻] = 10^(pH − 14)", "capacite": "AB2", "dit": "la concentration des ions H O moins égale dix puissance p H moins quatorze", "phrase": "à 25 °C ; jamais 10^(−pH)", "unite": "mol/L"},
        {"id": "f_tau_base", "ecriture": "τ = [HO⁻]_éq/C", "capacite": "AB2", "dit": "tau égale la concentration des ions H O moins à l'équilibre sur C", "phrase": "base B dans l'eau : B + H₂O ⇌ BH⁺ + HO⁻"},
        {"id": "f_k_tau", "ecriture": "K = C·τ²/(1 − τ)", "capacite": "AB3", "dit": "K égale C fois tau au carré, sur un moins tau", "phrase": "rappel du chapitre 12 (acide ou base avec l'eau)"},
        {"id": "f_ka", "ecriture": "Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq", "capacite": "AB3", "dit": "K a égale la concentration de A moins fois la concentration des ions H trois O plus, sur la concentration de A H, à l'équilibre", "phrase": "constante d'acidité du couple AH/A⁻ : K de AH + H₂O ⇌ A⁻ + H₃O⁺", "unite": "sans unité"},
        {"id": "f_pka", "ecriture": "pKa = −log Ka", "capacite": "AB3", "dit": "p K a égale moins log de K a"},
        {"id": "f_ka_pka", "ecriture": "Ka = 10^(−pKa)", "capacite": "AB3", "dit": "K a égale dix puissance moins p K a"},
        {"id": "f_ka_base", "ecriture": "Ka = Ke/Qr,éq", "capacite": "AB3", "dit": "K a égale K e sur Q r à l'équilibre", "phrase": "Qr,éq de la réaction de la BASE du couple avec l'eau (NH₃ + H₂O ⇌ NH₄⁺ + HO⁻)"},
        {"id": "f_pka_eau_1", "ecriture": "pKa(H₃O⁺/H₂O) = 0", "capacite": "AB3", "dit": "p K a du couple H trois O plus, H deux O, égale zéro"},
        {"id": "f_pka_eau_2", "ecriture": "pKa(H₂O/HO⁻) = 14", "capacite": "AB3", "dit": "p K a du couple H deux O, H O moins, égale quatorze", "phrase": "Ka(H₂O/HO⁻) = Ke"},
        {"id": "f_k_ka", "ecriture": "K = Ka₁/Ka₂", "capacite": "AB5", "dit": "K égale K a un sur K a deux", "phrase": "AH₁ + A₂⁻ ⇌ A₁⁻ + AH₂ ; Ka₁ : couple de l'acide qui réagit"},
        {"id": "f_k_pka", "ecriture": "K = 10^(pKa₂ − pKa₁)", "capacite": "AB5", "dit": "K égale dix puissance p K a deux moins p K a un"},
        {"id": "f_k_ho", "ecriture": "K = Ka/Ke", "capacite": "AB5", "dit": "K égale K a sur K e", "phrase": "réaction d'un acide avec HO⁻ (réaction de dosage)"},
        {"id": "f_ph_pka", "ecriture": "pH = pKa + log([A⁻]_éq/[AH]_éq)", "capacite": "AB6", "dit": "p H égale p K a plus log de la concentration de A moins sur la concentration de A H", "phrase": "tirée de l'expression de Ka (démonstration attendue)"},
        {"id": "f_equivalence", "ecriture": "C_A·V_A = C_B·V_BE", "capacite": "AB8", "dit": "C A fois V A égale C B fois V B E", "phrase": "dosage d'un acide par une base, à l'équivalence"},
        {"id": "f_equivalence_base", "ecriture": "C_B·V_B = C_A·V_AE", "capacite": "AB8", "dit": "C B fois V B égale C A fois V A E", "phrase": "dosage d'une base par un acide, à l'équivalence"},
        {"id": "f_demi", "ecriture": "pH = pKa à V_B = V_BE/2", "capacite": "AB9", "dit": "à la demi-équivalence, p H égale p K a", "phrase": "[AH] = [A⁻] (tableau de dosage)"},
        {"id": "f_cm", "ecriture": "C_m = C·M", "capacite": "AB8", "dit": "C m égale C fois M", "phrase": "concentration massique en g/L", "unite": "g/L"},
    ],
    "mots_cles": ["autoprotolyse", "produit ionique de l'eau", "Ke", "pKe", "solution acide", "solution neutre", "solution basique",
                  "constante d'acidité", "Ka", "pKa", "couple acide/base", "domaine de prédominance", "espèce prédominante",
                  "diagramme de distribution", "indicateur coloré", "zone de virage", "dosage", "titrage", "solution titrante", "solution titrée",
                  "équivalence", "volume équivalent", "méthode des tangentes", "courbe dérivée", "demi-équivalence", "saut de pH",
                  "concentration massique", "dilution", "conductimétrie"],
    "hors_cadre": {
        "_note": ("termes à ne jamais écrire ni dire dans ce cours : hors programme (perimetre.json acides_bases et dosage : termes_hors_programme), "
                  "semestre 2 (critère d'évolution des piles) ; « activité » seul n'y est pas (mot courant), mais « activité chimique » et "
                  "« coefficient d'activité » y sont ; « Gran » seul non plus (il casserait « grand »)."),
        "mots": ["Henderson", "Hasselbalch", "Flood", "Lewis", "Arrhenius", "Ostwald", "loi de dilution", "degré d'ionisation",
                 "coefficient de dissociation", "activité chimique", "coefficient d'activité", "pouvoir tampon", "capacité tampon",
                 "Le Chatelier", "loi de modération", "Guldberg", "loi d'action de masse", "enthalpie", "entropie", "dosage potentiométrique",
                 "potentiométrique", "méthode de Gran", "droite de Gran", "dérivée seconde", "normalité", "équivalent-gramme", "polyacide",
                 "diacide", "deux sauts de pH", "propagation des incertitudes", "incertitude-type", "Kb", "pKb", "pOH", "constante de basicité",
                 "critère d'évolution spontanée", "évolution spontanée"],
    },
    "valeurs_reference": {
        "exemple_A": {"equation": "2H₂O ⇌ H₃O⁺ + HO⁻", "pH_eau_pure": 7.00, "H3O_mol_L": 1.0e-7, "HO_mol_L": 1.0e-7, "Ke": 1.0e-14, "pKe": 14, "temperature_C": 25},
        "exemple_B": {"solutions": ["acide éthanoïque 1,0·10⁻² mol/L", "eau pure", "ammoniac 1,0·10⁻² mol/L"], "pH": [3.41, 7.00, 10.60],
                      "H3O_mol_L": [3.89e-4, 1.0e-7, 2.51e-11], "HO_mol_L": [2.57e-11, 1.0e-7, 3.98e-4], "BBT": ["jaune", "vert", "bleu"]},
        "exemple_C": {"soude_C_mol_L": 1.0e-2, "HO_mol_L": 1.0e-2, "H3O_mol_L": 1.0e-12, "pH": 12.00},
        "exemple_D": {"ammoniac": {"C_mol_L": 1.0e-2, "pH": 10.60, "HO_mol_L": 3.98e-4, "tau": 0.040, "Qr_eq": 1.65e-5},
                      "methylamine": {"C_mol_L": 1.0e-2, "pH": 11.30, "HO_mol_L": 2.0e-3, "tau": 0.20, "Qr_eq": 5.0e-4}},
        "exemple_E": {"Qr_eq_ethanoique": 1.57e-5, "pKa": {"CH3COOH/CH3COO-": 4.8, "HCOOH/HCOO-": 3.75, "NH4+/NH3": 9.2, "CH3NH3+/CH3NH2": 10.7,
                                                            "H3O+/H2O": 0, "H2O/HO-": 14},
                      "Ka": {"CH3COOH/CH3COO-": 1.6e-5, "HCOOH/HCOO-": 1.8e-4, "NH4+/NH3": 6.3e-10, "CH3NH3+/CH3NH2": 2.0e-11},
                      "Ka_NH4_par_Ke": 6.06e-10, "pKa_NH4_par_Ke": 9.22},
        "exemple_F": {"acides": {"ethanoique": {"pKa": 4.8, "pH": 3.41, "tau": 0.039}, "methanoique": {"pKa": 3.75, "pH": 2.90, "tau": 0.126}},
                      "bases": {"ammoniac": {"pKa": 9.2, "pH": 10.60, "tau": 0.040}, "methylamine": {"pKa": 10.7, "pH": 11.30, "tau": 0.20}},
                      "C_mol_L": 1.0e-2},
        "exemple_G": {"K_HCOOH_CH3COO-": 11.2, "K_inverse": 8.9e-2, "K_CH3COOH_NH3": 2.5e4, "K_CH3COOH_HO-": 1.6e9, "K_2020R": 10},
        "exemple_H": {"pKa": 4.8, "rapport_pH": [[1, 4.8], [10, 5.8], [0.1, 3.8]],
                      "distribution_pH": [2.8, 3.8, 4.8, 5.8, 6.8], "pourcent_AH": [99.0, 90.9, 50.0, 9.1, 1.0]},
        "exemple_I": {"helianthine": [3.1, 4.4], "rouge_de_methyle": [4.2, 6.2], "BBT": [6.0, 7.6], "rouge_de_cresol": [7.2, 8.8], "pKa_BBT": 7.0},
        "exemple_J": {"C_A_mol_L": 1.0e-2, "V_A_mL": 20.0, "C_B_mol_L": 1.0e-2, "pKa": 4.8, "V_BE_mL": 20.0, "n_A_mol": 2.0e-4,
                      "V_B_mL": [0, 2, 5, 10, 15, 18, 19, 19.5, 20, 20.5, 21, 22, 25, 30, 40],
                      "pH": [3.41, 3.91, 4.34, 4.80, 5.28, 5.76, 6.08, 6.39, 8.25, 10.09, 10.39, 10.68, 11.05, 11.30, 11.52],
                      "pH_E": 8.3, "pH_demi": 4.8, "derivee_max_par_mL": 11.5, "indicateur": "rouge de crésol"},
        "exemple_K": {"V_B_mL": [0, 5, 10, 15, 18, 19, 19.5, 20, 20.5, 21, 25, 30, 40],
                      "pH": [2.00, 2.22, 2.48, 2.85, 3.28, 3.59, 3.90, 7.00, 10.09, 10.39, 11.05, 11.30, 11.52], "pH_E": 7.0, "indicateur": "BBT"},
        "exemple_L": {"V_A_mL": [0, 2, 5, 10, 15, 18, 19, 19.5, 20, 20.5, 21, 22, 25, 30, 40],
                      "pH": [10.59, 10.09, 9.66, 9.20, 8.72, 8.24, 7.92, 7.61, 5.75, 3.91, 3.61, 3.32, 2.95, 2.70, 2.48],
                      "pH_E": 5.7, "pKa": 9.2, "indicateur": "rouge de méthyle"},
        "exemple_M": {"V_B_mL": [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0], "sigma_mS_m": [38.8, 31.9, 25.0, 18.2, 11.4, 17.0, 22.5, 33.5],
                      "V_BE_mL": 2.0, "lambda_mS_m2_mol": {"H3O+": 35.0, "HO-": 19.9, "Na+": 5.01, "Cl-": 7.63}},
        "exemple_N": {"C_A_mol_L": 4.8e-2, "C0_mol_L": 4.80, "Cm_g_L": 499.2, "M_g_mol": 104},
    },
}

INSISTANCES = [
    "Ke = [H₃O⁺]·[HO⁻] = 1,0·10⁻¹⁴ à 25 °C dans TOUTE solution aqueuse ; [HO⁻] = Ke/[H₃O⁺], jamais 10^(−pH)",
    "Ka est la constante d'équilibre de la réaction de l'acide avec l'eau ; Ka et pKa sans unité ; pKa = −log Ka (signe moins)",
    "Ka grand ⇔ pKa petit ⇔ acide plus fort (même C : τ plus grand, pH plus petit)",
    "K = Ka₁/Ka₂ : Ka du couple de l'ACIDE qui réagit au numérateur",
    "pH < pKa : la forme acide AH prédomine ; pH > pKa : la forme basique A⁻ prédomine",
    "réaction de dosage : rapide, totale, unique — écrite avec →",
    "à l'équivalence : C_A·V_A = C_B·V_BE (le volume À L'ÉQUIVALENCE) ; V_E lu par les tangentes ou la dérivée, pas « à l'œil »",
    "pH = pKa à la DEMI-équivalence, pas à l'équivalence",
    "l'indicateur choisi a une zone de virage qui CONTIENT pH_E (pas forcément 7)",
]

VALEURS_REPERES = [
    "exemple A : eau pure à 25 °C, pH 7,00, [H₃O⁺] = [HO⁻] = 1,0·10⁻⁷ mol/L, Ke = 1,0·10⁻¹⁴, pKe = 14",
    "exemple C : soude 1,0·10⁻² mol/L → [H₃O⁺] = 1,0·10⁻¹² mol/L → pH = 12,00",
    "exemple D : ammoniac 1,0·10⁻² mol/L, pH 10,60 → [HO⁻] = 3,98·10⁻⁴ mol/L, τ = 0,040 ; Ka = Ke/Qr,éq = 6,06·10⁻¹⁰ → pKa = 9,2",
    "exemple E : acide éthanoïque Ka = 1,6·10⁻⁵, pKa = 4,8 ; acide méthanoïque pKa = 3,75 ; NH₄⁺/NH₃ pKa = 9,2 ; CH₃NH₃⁺/CH₃NH₂ pKa = 10,7 ; eau : 0 et 14",
    "exemple G : HCOOH + CH₃COO⁻ : K = 10^(4,8 − 3,75) = 11 ; CH₃COOH + HO⁻ : K = Ka/Ke = 1,6·10⁹",
    "exemple J : dosage acide éthanoïque C_A = 1,0·10⁻² mol/L, V_A = 20,0 mL par la soude 1,0·10⁻² mol/L → V_BE = 20,0 mL, pH_E = 8,3, pH(10 mL) = 4,8 = pKa ; rouge de crésol",
    "exemple K et L : acide chlorhydrique → pH_E = 7,0 (BBT) ; ammoniac par l'acide chlorhydrique → pH_E = 5,7 (rouge de méthyle), pH(10 mL) = 9,2",
    "nationaux : pKa 4,8 (2017 N, 2020 R, 2025 R), 4,2 (2019 N), 9,2 (2020 N), 4,75 (2021 N), 3,74 (2021 R), 4,9 (2022 N), 10,7 (2022 R), 4,79 (2023 N), 9,9 (2023 R), 4,09 (2024 N), 10,8 (2024 R) ; K = 1,26·10⁹ (2016 N), 10 (2020 R), 9,1·10⁻² (2023 N), 8,13·10⁹ (2024 N), 6,31·10⁶ (2025 N)",
]

CAS_TYPES = [
    {"cas": "Équation de la réaction de dosage", "mots": "« Écrire l'équation de la réaction du dosage »", "methode": "acide + HO⁻ → base conjuguée + H₂O (ou base + H₃O⁺ → acide conjugué + H₂O) ; flèche simple", "points": "0,25-0,5", "frequence": "11 sessions"},
    {"cas": "V_E et pH_E sur la courbe", "mots": "« Déterminer graphiquement les coordonnées V_BE et pH_E du point d'équivalence »", "methode": "tangentes parallèles + parallèle équidistante, ou abscisse du maximum de dpH/dV ; écrire la méthode", "points": "0,25-0,5", "frequence": "8 sessions"},
    {"cas": "Concentration à l'équivalence (+ dilution, masse)", "mots": "« Calculer la concentration C_A » ; « En déduire C₀ » ; « Montrer que m = … »", "methode": "C_A·V_A = C_B·V_BE ; C₀ = F·C ; m = C·V·M ; C_m = C·M", "points": "0,25-1,5", "frequence": "13 sessions"},
    {"cas": "Choix de l'indicateur coloré", "mots": "« Choisir, en justifiant, l'indicateur coloré adéquat »", "methode": "zone de virage qui contient pH_E (lu, ou justifié > 7 / < 7)", "points": "0,5", "frequence": "6 sessions"},
    {"cas": "pKa à partir de Qr,éq ou de τ", "mots": "« En déduire la valeur du pKa du couple »", "methode": "acide : Ka = Qr,éq ; base : Ka = Ke/Qr,éq ; pKa = −log Ka", "points": "0,5-0,75", "frequence": "9 sessions"},
    {"cas": "[HO⁻] par Ke (base)", "mots": "« Calculer la concentration effective des ions hydroxyde »", "methode": "[HO⁻] = Ke/[H₃O⁺] = 10^(pH − 14)", "points": "0,5", "frequence": "3 sessions (2020 N, 2020 R, 2022 R)"},
    {"cas": "K d'une réaction acide-base", "mots": "« Trouver l'expression de K en fonction de Ka₁ et Ka₂ » ; « En calculant K, montrer que la réaction est totale »", "methode": "multiplier en haut et en bas par [H₃O⁺]_éq ; K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁) ; avec HO⁻ : K = Ka/Ke", "points": "0,5-0,75", "frequence": "5 sessions"},
    {"cas": "Rapport [A⁻]/[AH], prédominance, pourcentage", "mots": "« Trouver le rapport … puis déduire l'espèce prédominante » ; « pourcentage de la forme acide »", "methode": "pH = pKa + log([A⁻]/[AH]) ; [A⁻]/[AH] = 10^(pH − pKa) ; % AH = 1/(1 + [A⁻]/[AH])", "points": "0,25-1", "frequence": "11 sessions"},
    {"cas": "Diagramme de distribution", "mots": "« En exploitant les courbes, vérifier que pKa = … » ; « Justifier que la courbe 1 correspond à l'acide »", "methode": "pKa = pH au croisement (50 %) ; la forme acide domine pour pH < pKa", "points": "0,25-0,75", "frequence": "2 sessions (2024 R, 2025 R)"},
    {"cas": "Demi-équivalence", "mots": "« Trouver le rapport pour V_A = 10 mL » ; « Déduire que pKa = 9,9 »", "methode": "tableau : à V_E/2, [AH] = [A⁻] → pH = pKa", "points": "0,5-1,5", "frequence": "2 sessions (2023 R, 2024 N)"},
]

PIEGES = [
    {"erreur": "[HO⁻] = 10^(−pH)", "geste": "écrire d'abord Ke = [H₃O⁺]·[HO⁻], puis [HO⁻] = Ke/[H₃O⁺] = 10^(pH − 14)"},
    {"erreur": "pKa = log Ka (signe oublié) ou Ka avec une unité", "geste": "pKa = −log Ka ; vérifier qu'un pKa d'acide carboxylique est vers 4-5"},
    {"erreur": "K = Ka₂/Ka₁ au lieu de Ka₁/Ka₂", "geste": "repérer l'acide qui réagit (à gauche) : son Ka en haut ; contrôle : K > 1 si l'acide qui réagit est le plus fort"},
    {"erreur": "prédominance inversée", "geste": "dessiner l'axe des pH, le trait au pKa, AH à gauche, A⁻ à droite, puis placer le pH"},
    {"erreur": "équation de dosage avec ⇌", "geste": "réaction de dosage = totale : flèche simple →"},
    {"erreur": "C_A·V_A = C_B·V_B avec un V_B quelconque", "geste": "écrire V_BE (le volume versé À L'ÉQUIVALENCE)"},
    {"erreur": "V_E lu « au milieu du saut » sans méthode", "geste": "tracer les deux tangentes parallèles et la parallèle équidistante (ou chercher le maximum de dpH/dV)"},
    {"erreur": "indicateur choisi autour de 7 pour un acide faible", "geste": "la zone de virage doit contenir pH_E (8,3 pour l'acide éthanoïque)"},
    {"erreur": "pH = pKa à l'équivalence", "geste": "pH = pKa à la DEMI-équivalence (V_BE/2) : [AH] = [A⁻]"},
]

ERREURS_EXAMEN = [
    {"erreur": "τ d'une base calculé avec 10^(−pH)/C", "geste": "τ = [HO⁻]_éq/C avec [HO⁻]_éq = Ke/[H₃O⁺]_éq", "source": "2020 N, 2020 R, 2022 R"},
    {"erreur": "Ka d'un couple de base pris égal à Qr,éq", "geste": "la réaction de NH₃ avec l'eau a pour constante Ke/Ka : Ka = Ke/Qr,éq", "source": "2020 N, 2020 R, 2022 R"},
    {"erreur": "équation de dosage avec ⇌ (le corrigé du dépôt le fait en 2022 N)", "geste": "→ : la réaction de dosage est totale", "source": "2022 N"},
    {"erreur": "concentration de la solution mère oubliée (dilution)", "geste": "C₀ = F·C après le calcul à l'équivalence", "source": "2020 N, 2022 N, 2023 R, 2025 N"},
    {"erreur": "indicateur non justifié", "geste": "« sa zone de virage [7,2 ; 8,8] contient pH_E = 8,3 » : la phrase vaut les points", "source": "2016 N, 2018 N, 2019 R, 2020 N, 2022 R, 2023 R"},
    {"erreur": "pourcentage de forme acide calculé avec [A⁻]/[AH] au lieu de 1/(1 + [A⁻]/[AH])", "geste": "% AH = [AH]/([AH] + [A⁻])", "source": "2022 N, 2024 R"},
]

CONSEILS = [
    "dans un exercice d'acide : équation avec l'eau → τ → Qr,éq → pKa → prédominance → dosage : les questions se suivent dans cet ordre",
    "relation littérale, puis application numérique, puis résultat avec unité (Ka, pKa, K, pH sans unité)",
    "une lecture graphique se justifie : nommer la méthode (tangentes parallèles, maximum de la dérivée, croisement des courbes)",
    "avant un dosage d'une solution diluée, noter le facteur de dilution : il servira à la fin",
]

ANALOGIES = [
    {"image": "le marché : un acide vend un proton H⁺, une base l'achète ; l'eau fait les deux (elle est vendeur et acheteur)", "limite": "un proton n'est jamais libre en solution : il passe directement d'une espèce à l'autre"},
    {"image": "la balance à deux plateaux du pKa : au pKa, autant d'acide que de base ; un pH plus haut fait pencher vers la base", "limite": "la balance ne dit pas les quantités, seulement le rapport [A⁻]/[AH]"},
    {"image": "remplir une bouteille au robinet : au début le niveau monte lentement, juste au goulot il monte d'un coup — le saut de pH à l'équivalence", "limite": "après l'équivalence, le pH se stabilise au lieu de déborder"},
]

A_NE_PAS_DIRE = [
    {"terme": "[H₂O] dans Ke ou Ka", "motif": r"\[H₂O\]", "pourquoi": "l'eau est le solvant : elle n'apparaît pas dans Ke ni dans Ka", "dire_plutot": "Ke = [H₃O⁺]·[HO⁻]"},
    {"terme": "Ka, Ke avec une unité", "motif": r"\bp?K[ae]\s*=\s*[0-9][0-9,]*(·10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)?\s*(mol|L)\b", "pourquoi": "Ke, Ka et pKa sont sans unité", "dire_plutot": "Ka = 1,6·10⁻⁵ (sans unité)"},
    {"terme": "pKa = log Ka (signe oublié)", "motif": r"\bpK[ae]\s*=\s*log", "pourquoi": "pKa = −log Ka", "dire_plutot": "pKa = −log Ka"},
    {"terme": "[HO⁻] = 10^(−pH)", "motif": r"\[HO⁻\](_?éq)?\s*=\s*10\^\(−pH\)", "pourquoi": "10^(−pH) est [H₃O⁺] ; [HO⁻] = Ke/[H₃O⁺]", "dire_plutot": "[HO⁻] = 10^(pH − 14)"},
    {"terme": "équation de dosage avec ⇌", "motif": r"\+ HO⁻ ⇌", "pourquoi": "la réaction de dosage est totale", "dire_plutot": "CH₃COOH + HO⁻ → CH₃COO⁻ + H₂O"},
    {"terme": "pH = pKa à l'équivalence", "motif": r"(à|a) l'[ée]quivalence,?\s*(le\s+)?pH\s*=\s*pKa", "pourquoi": "pH = pKa à la demi-équivalence", "dire_plutot": "pH = pKa à V_B = V_BE/2"},
    {"terme": "relation d'équivalence avec un volume quelconque", "motif": r"C_?A\s*·\s*V_?A\s*=\s*C_?B\s*·\s*V_?B(?![E\w])|C_?B\s*·\s*V_?B\s*=\s*C_?A\s*·\s*V_?A(?![E\w])", "pourquoi": "la relation ne vaut qu'à l'équivalence", "dire_plutot": "C_A·V_A = C_B·V_BE"},
    {"terme": "prédominance inversée", "motif": r"pH\s*>\s*pKa\s*[:,]?\s*(c'est\s+)?l'acide\s+(AH\s+)?pr[ée]domin|pH\s*<\s*pKa\s*[:,]?\s*(c'est\s+)?la base\s+(A⁻\s+)?pr[ée]domin", "pourquoi": "pH > pKa : la base prédomine", "dire_plutot": "pH < pKa : AH prédomine ; pH > pKa : A⁻ prédomine"},
    {"terme": "Ka dépend de la concentration", "motif": r"\bp?Ka\b\s+(d[ée]pend|varie|change)\s+(de|avec|selon)\s+(la concentration|la dilution|C\b)", "pourquoi": "Ka ne dépend que de la température", "dire_plutot": "τ dépend de C ; Ka non"},
    {"terme": "pH_E = 7 toujours", "motif": r"[àa] l'[ée]quivalence.{0,30}toujours", "pourquoi": "pH_E = 7 seulement pour acide fort + base forte", "dire_plutot": "pH_E > 7 pour un acide faible dosé par une base forte"},
    {"terme": "Henderson, Ostwald, activité chimique, Lewis", "motif": r"henderson|hasselbalch|ostwald|degr[ée] d'ionisation|activit[ée] chimique|\bflood\b|lewis|arrhenius|pouvoir tampon", "pourquoi": "hors programme (perimetre.json)", "dire_plutot": "pH = pKa + log([A⁻]/[AH]) ; acide et base de Brønsted ; taux d'avancement final τ"},
    {"terme": "critère d'évolution, Le Chatelier", "motif": r"crit[èe]re d'[ée]volution|[ée]volution spontan|chatelier|loi de mod[ée]ration|guldberg|action de masse|enthalpie", "pourquoi": "critère d'évolution : semestre 2 (piles) ; Le Chatelier, Guldberg-Waage, enthalpie : hors programme", "dire_plutot": "au semestre 2, on comparera Qr,i à K"},
    {"terme": "pOH, Kb, pKb", "motif": r"\bpoh\b|\bp?kb\b", "pourquoi": "le programme marocain classe les bases par le pKa de leur couple", "dire_plutot": "plus le pKa du couple est grand, plus la base est forte"},
]

EXCLUS = [
    "pOH, Kb, pKb, constante de basicité : non utilisés au bac marocain (on classe les bases par le pKa de leur couple)",
    "relation de Henderson-Hasselbalch, diagramme de Flood (nom), loi de dilution d'Ostwald, degré d'ionisation, activité chimique, acide/base de Lewis ou d'Arrhenius, pouvoir tampon quantifié : hors programme (perimetre.json)",
    "dosage potentiométrique, méthode de Gran, dérivée seconde, polyacides (plusieurs sauts), incertitudes : hors programme (perimetre.json clé dosage)",
    "formules toutes faites du pH d'un acide faible (pH = ½(pKa − log C)) ou du pH à l'équivalence : non demandées ; les pH d'équivalence sont lus sur la courbe ou justifiés (> 7, < 7)",
    "comparaison de Qr,i à K pour prévoir le sens (2020 R 2.4) : semestre 2 (piles) ; ici on calcule seulement K",
    "Brønsted, pH, τ d'un acide (chapitre 11) et Qr, K, K = C·τ²/(1 − τ) (chapitre 12) : rappelés en r1, r2, utilisés sans être refaits",
]
