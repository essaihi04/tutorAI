"""Exploration etat_equilibre, partie A : en-tête, sources, cadre, nationaux, pièges, décisions.
Importé par explo.py (même dossier)."""

EXAMS = [f"backend/data/exams/physique/{a}-{s}" for a in range(2016, 2026) for s in ("normale", "rattrapage")]
AVEC_QR = ["2016-rattrapage", "2017-normale", "2017-rattrapage", "2018-rattrapage", "2019-normale", "2019-rattrapage", "2020-normale",
           "2020-rattrapage", "2021-normale", "2022-normale", "2022-rattrapage", "2023-normale"]

ENTETE = {
    "cle": "etat_equilibre",
    "matiere": "Physique-Chimie",
    "filiere": "2e Bac Sciences Physiques BIOF (Maroc)",
    "titre": "État d'équilibre d'un système chimique",
    "date_exploration": "2026-11-12",
    "_note": ("Exploration faite par la routine cloud du 12 novembre 2026 pour le cours phys_ch12_etat_equilibre. VIDÉOS NON AUDITÉES : "
              "YouTube est bloqué depuis le conteneur cloud (yt-dlp non tenté). Appui : les 20 nationaux PC 2016-2025 du dépôt (12 touchent "
              "ce chapitre, 7 calculent Qr,éq ou K d'un acide ou d'une base avec l'eau ; etat_equilibre_build/nationaux.md, figure 2017 R "
              "regardée, nombres recalculés avec python), perimetre.json (clé acides_bases, qui couvre les chapitres 11, 12 et 13 ; clé "
              "piles_electrolyse pour le critère d'évolution), programme_semestre1.json (ordre 12) et le contrat des simulations "
              "etat_equilibre_contrat_simulations.md (exemples A à K ; vues ; diapositives servies). Chapitre précédent déjà construit : "
              "phys_ch11_transformations_deux_sens (τ, pH, équilibre dynamique, conductimétrie) — rappelé en deux diapositives. Pas d'ancien "
              "cours de ce chapitre dans backend/data/courses/. À compléter par 10 audits vidéo depuis le PC avant validation. Ka, pKa, Ke "
              "(chapitre 13) et la comparaison de Qr,i à K pour prévoir le sens (piles, semestre 2) sont renvoyés."),
}

SOURCES = {
    "videos": [],
    "videos_note": ("aucune : YouTube inaccessible depuis le conteneur cloud (12/11/2026) ; vidéos non auditées ; 10 audits à faire depuis "
                    "le PC (recherche « حالة توازن مجموعة كيميائية 2 باك », « état d'équilibre d'un système chimique 2bac biof », « quotient "
                    "de réaction constante d'équilibre 2 bac »)"),
    "examens": EXAMS,
    "examens_avec_qr_ou_k": [f"backend/data/exams/physique/{s}" for s in AVEC_QR],
    "autres": [
        "outils/cours/notes/cours/etat_equilibre_build/nationaux.md (relecture des 20 sujets, 1 figure pour figures.html)",
        "outils/cours/notes/cours/transformations_deux_sens_build/nationaux.md (chapitre précédent : τ, pH, σ dans les mêmes exercices)",
        "outils/cours/notes/cours/etat_equilibre_contrat_simulations.md (exemples A à K, vues, diapositives servies)",
        "backend/data/curriculum/perimetre.json (clés acides_bases, piles_electrolyse, esterification_hydrolyse : notions, termes hors programme)",
        "backend/data/curriculum/programme_semestre1.json (ordre 12, clé etat_equilibre)",
        "backend/data/curriculum/prerequis.json (tableau_avancement, concentration_quantite_matiere, logarithme_decimal_puissances, conductimetrie)",
        "backend/data/curriculum/exploration/transformations_deux_sens.json (chapitre précédent, modèle)",
        "backend/data/courses/phys_ch11_transformations_deux_sens.json (cours précédent : exemples A à F repris)",
    ],
}

COMPARAISON = {
    "_note": "sans vidéos : comparaison faite entre les corrigés des 12 nationaux qui touchent le chapitre, perimetre.json et le chapitre précédent",
    "convergences": [
        "Qr écrit avec les concentrations des produits au numérateur et des réactifs au dénominateur, coefficients en exposants (12 sessions sur 12)",
        "l'eau solvant n'apparaît jamais dans Qr d'une réaction en solution aqueuse ; les solides non plus (piles 2017 N, 2018 R, 2019 R)",
        "Qr,éq d'un acide avec l'eau : [A⁻]éq = [H₃O⁺]éq (tableau) et [AH]éq = C − [H₃O⁺]éq, d'où Qr,éq = [H₃O⁺]²/(C − [H₃O⁺]) (2017 N, 2022 N)",
        "avec τ : [A⁻]éq = C·τ, [AH]éq = C(1 − τ), d'où K = C·τ²/(1 − τ) (2019 N, 2020 R, 2021 N, 2022 R) — la relation la plus demandée",
        "Qr,i d'un mélange : concentrations APRÈS mélange, le volume total se simplifie (2020 R)",
        "K = Qr,éq ne dépend que de la température (admis, perimetre.json) ; Qr, K et τ sans unité",
    ],
    "variantes_admises": [
        {"variante": "Qr,éq ou K (même nombre)", "decision": "Qr,éq quand on calcule à partir de mesures ; K = Qr,éq quand on dit que la valeur est la même pour tous les états initiaux"},
        {"variante": "[X]éq, [X]_éq, [X]_f", "decision": "[X]éq à l'écran (indice éq) ; jamais [X]_f pour une concentration d'équilibre"},
        {"variante": "x_éq ou x_f", "decision": "x_éq dans ce chapitre (corrigés 2019 N, 2017 N) ; on dit une fois que x_f = x_éq pour une réaction limitée"},
        {"variante": "pH au dixième (3,4) ou au centième (3,41)", "decision": "au centième dans ce chapitre (Qr,éq est sensible au pH) ; rappel : 3,4 au dixième au chapitre précédent"},
        {"variante": "Qr,éq = 10^(−2pH)/(C − 10^(−pH)) ou C·τ²/(1 − τ)", "decision": "les deux, démontrées ; la seconde est la plus demandée"},
    ],
    "meilleures_explications": [
        "trois concentrations, trois τ différents, un même Qr,éq : la constante se VOIT dans une colonne du tableau",
        "on part des produits (éthanoate + acide chlorhydrique) et on retrouve le même Qr,éq : K ne dépend pas de l'état initial",
        "Qr monte de 0 (état initial) jusqu'à 1,57·10⁻⁵ puis s'arrête : l'équilibre, c'est quand Qr atteint K",
        "le quotient « retourné » pour la réaction inverse : K' = 1/K sans calcul",
        "même acide plus dilué : τ grandit, K ne bouge pas — c'est ce qui explique le résultat du chapitre précédent",
    ],
}

CADRE = {
    "_note": ("Fiche du chapitre, même forme que cadre_reference_2bac_pc.json. Capacités d'après CDR-PC-2015 (annexe 1, Chimie, sous-domaine 2 "
              "« Transformations non totales d'un système chimique » : « État d'équilibre d'un système chimique (quotient de réaction, constante "
              "d'équilibre) »), OP-PC-2007, perimetre.json (clé acides_bases : notions, demonstrations.admises « le quotient de réaction à "
              "l'équilibre est une constante K qui ne dépend que de la température ») et les nationaux 2016-2025. Texte officiel du cadre non relu "
              "en entier : EE1 à EE7 provisoires. Formules écrites exactement comme le contrat des simulations."),
    "titre": "État d'équilibre d'un système chimique",
    "source": ("CDR-PC-2015, annexe 1, Chimie, sous-domaine 2 « Transformations non totales d'un système chimique » : « État d'équilibre d'un "
               "système chimique (quotient de réaction, constante d'équilibre) » ; OP-PC-2007, 2BAC : quotient de réaction Qr, Qr,éq, constante "
               "d'équilibre K, influence de l'état initial et de K sur le taux d'avancement final ; perimetre.json clé acides_bases ; "
               "le critère d'évolution (Qr,i comparé à K) est au sous-domaine 3 « Sens d'évolution d'un système chimique » (clé piles_electrolyse) ; "
               "nationaux PC 2016-2025 du dépôt."),
    "capacites": [
        {"id": "EE1", "texte": "Écrire l'expression du quotient de réaction Qr associé à l'équation d'une réaction en solution aqueuse (l'eau solvant et les espèces solides n'y figurent pas ; concentrations en mol/L ; Qr sans unité)."},
        {"id": "EE2", "texte": "Calculer la valeur de Qr dans un état donné du système, en particulier Qr,i dans l'état initial (mélange : concentrations après mélange) ; savoir que Qr évolue au cours de la transformation."},
        {"id": "EE3", "texte": "Calculer Qr,éq dans l'état d'équilibre à partir d'une mesure (pH, conductivité) et du tableau d'avancement ; l'exprimer en fonction de C et du pH."},
        {"id": "EE4", "texte": "Savoir que Qr,éq prend une valeur K, constante d'équilibre, qui ne dépend que de la température (pas de l'état initial) ; K de la réaction inverse vaut 1/K."},
        {"id": "EE5", "texte": "Établir la relation K = C·τ²/(1 − τ) pour la réaction d'un acide avec l'eau ; déterminer K par pH-métrie et par conductimétrie."},
        {"id": "EE6", "texte": "Savoir que le taux d'avancement final τ dépend de la constante d'équilibre (nature de la réaction) et de l'état initial (concentration) ; la dilution augmente τ sans changer K."},
        {"id": "EE7", "texte": "Rédiger un exercice du national : expression littérale de Qr,i ou Qr,éq, tableau d'avancement, application numérique, résultat sans unité."},
    ],
    "formules": [
        {"id": "f_qr", "ecriture": "Qr = [C]^c·[D]^d/([A]^a·[B]^b)", "capacite": "EE1", "dit": "Q r égale la concentration de C puissance c fois la concentration de D puissance d, sur la concentration de A puissance a fois la concentration de B puissance b", "phrase": "pour aA + bB ⇌ cC + dD en solution aqueuse ; eau solvant et solides absents", "unite": "sans unité"},
        {"id": "f_qr_acide", "ecriture": "Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH]", "capacite": "EE1", "dit": "Q r égale la concentration des ions éthanoate fois la concentration des ions H trois O plus, sur la concentration de l'acide éthanoïque", "phrase": "réaction de l'acide éthanoïque avec l'eau ; l'eau n'y figure pas"},
        {"id": "f_qr_solide", "ecriture": "Qr = [Zn²⁺]/[Cu²⁺]", "capacite": "EE1", "dit": "Q r égale la concentration des ions zinc sur la concentration des ions cuivre", "phrase": "Cu²⁺ + Zn(s) ⇌ Cu(s) + Zn²⁺ : les solides n'y figurent pas"},
        {"id": "f_k", "ecriture": "K = Qr,éq", "capacite": "EE4", "dit": "K égale Q r à l'équilibre", "phrase": "constante d'équilibre ; ne dépend que de la température", "unite": "sans unité"},
        {"id": "f_k_inverse", "ecriture": "K' = 1/K", "capacite": "EE4", "dit": "K prime égale un sur K", "phrase": "constante de la réaction écrite dans l'autre sens"},
        {"id": "f_tau_ph", "ecriture": "τ = 10^(−pH)/C", "capacite": "EE5", "dit": "tau égale dix puissance moins pH, sur C", "phrase": "rappel du chapitre précédent (acide avec l'eau)"},
        {"id": "f_qreq_ph", "ecriture": "Qr,éq = 10^(−2pH)/(C − 10^(−pH))", "capacite": "EE3", "dit": "Q r à l'équilibre égale dix puissance moins deux pH, sur C moins dix puissance moins pH", "phrase": "acide avec l'eau : [A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; [AH]éq = C − 10^(−pH)"},
        {"id": "f_conc_tau", "ecriture": "[A⁻]_éq = [H₃O⁺]_éq = C·τ", "capacite": "EE5", "dit": "la concentration de A moins à l'équilibre égale celle des ions H trois O plus, égale C fois tau", "phrase": "d'après le tableau d'avancement : x_éq/V = C·τ", "unite": "mol/L"},
        {"id": "f_acide_tau", "ecriture": "[AH]_éq = C·(1 − τ)", "capacite": "EE5", "dit": "la concentration de A H à l'équilibre égale C fois un moins tau", "unite": "mol/L"},
        {"id": "f_k_tau", "ecriture": "K = C·τ²/(1 − τ)", "capacite": "EE5", "dit": "K égale C fois tau au carré, sur un moins tau", "phrase": "acide (ou base) avec l'eau ; C en mol/L"},
        {"id": "f_sigma_acide", "ecriture": "σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺]", "capacite": "EE5", "dit": "sigma égale lambda H trois O plus plus lambda A moins, fois la concentration des ions H trois O plus", "phrase": "rappel du chapitre précédent ; [X] en mol/m³"},
        {"id": "f_h3o_sigma", "ecriture": "[H₃O⁺]_éq = σ/(λ(H₃O⁺) + λ(A⁻))", "capacite": "EE5", "dit": "la concentration des ions H trois O plus à l'équilibre égale sigma sur la somme des deux lambda", "phrase": "résultat en mol/m³, à diviser par 10³ pour l'avoir en mol/L"},
    ],
    "mots_cles": ["quotient de réaction", "Qr", "état initial", "Qr,i", "état d'équilibre", "Qr,éq", "constante d'équilibre", "K",
                  "température", "réaction inverse", "solvant", "espèce solide", "concentration molaire effective", "taux d'avancement final",
                  "pH-métrie", "conductimétrie", "dilution", "nature de la réaction"],
    "hors_cadre": {
        "_note": ("termes à ne jamais écrire ni dire dans ce cours : chapitre suivant (réactions acide-base : Ka, pKa, Ke, prédominance, "
                  "indicateurs), semestre 2 (critère d'évolution des piles) et hors programme (perimetre.json acides_bases, esterification_hydrolyse, "
                  "piles_electrolyse : termes_hors_programme)"),
        "mots": ["Ka", "pKa", "Ke", "pKe", "constante d'acidité", "produit ionique", "autoprotolyse", "Henderson", "Hasselbalch",
                 "diagramme de prédominance", "espèce prédominante", "diagramme de distribution", "indicateur coloré", "zone de virage",
                 "activité", "Le Chatelier", "loi de modération", "Guldberg", "Waage", "loi d'action de masse", "enthalpie", "entropie",
                 "critère d'évolution spontanée", "évolution spontanée", "Lewis", "Arrhenius", "Ostwald", "degré d'ionisation",
                 "coefficient de dissociation", "pouvoir tampon"],
    },
    "valeurs_reference": {
        "exemple_A": {"equation": "CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺", "C_mol_L": 1.0e-2, "V_L": 0.100, "pH": 3.41, "pH_au_dixieme": 3.4,
                      "H3O_mol_L": 3.89e-4, "CH3COOH_mol_L": 9.61e-3, "tau": 0.0389, "Qr_eq": 1.57e-5},
        "exemple_B": {"C_mol_L": [1.0e-2, 5.0e-3, 1.0e-3], "pH": [3.41, 3.56, 3.93], "H3O_mol_L": [3.89e-4, 2.75e-4, 1.17e-4],
                      "tau": [0.039, 0.055, 0.117], "Qr_eq": [1.57e-5, 1.61e-5, 1.56e-5], "K": 1.6e-5, "temperature_C": 25},
        "exemple_C": {"melange": "50 mL HCl 1,0·10⁻² + 50 mL éthanoate de sodium 1,0·10⁻²", "pH": 3.56, "H3O_mol_L": 2.75e-4,
                      "CH3COOH_mol_L": 4.72e-3, "Qr_eq": 1.61e-5},
        "exemple_D": {"C_mol_L": 1.0e-3, "sigma_S_m": 4.6e-3, "lambda_mS_m2_mol": {"H3O+": 35.0, "CH3COO-": 4.09},
                      "H3O_mol_m3": 0.118, "H3O_mol_L": 1.18e-4, "tau": 0.118, "K": 1.58e-5},
        "exemple_E": {"acide": "méthanoïque", "C_mol_L": 1.0e-2, "pH": 2.90, "H3O_mol_L": 1.26e-3, "tau": 0.126, "Qr_eq": 1.81e-4, "K": 1.8e-4},
        "exemple_F": {"H3O_mol_L": [0, 1.0e-4, 2.0e-4, 3.0e-4, 3.89e-4], "Qr": [0, 1.01e-6, 4.08e-6, 9.28e-6, 1.57e-5]},
        "exemple_G": {"n_mol": {"HCOOH": 1.0e-2, "CH3COO-": 1.0e-2, "CH3COOH": 5.0e-3, "HCOO-": 5.0e-3}, "V_T_L": 0.300, "Qr_i": 0.25},
        "exemple_H": {"equation": "Cu²⁺ + Zn(s) ⇌ Cu(s) + Zn²⁺", "Cu2+_mol_L": 0.10, "Zn2+_mol_L": 0.010, "Qr_i": 0.10},
        "exemple_I": {"equation": "2I⁻ + S₂O₈²⁻ ⇌ I₂ + 2SO₄²⁻", "Qr": "[I₂]·[SO₄²⁻]²/([I⁻]²·[S₂O₈²⁻])"},
        "exemple_J": {"K": 1.6e-5, "K_inverse": 6.25e4},
        "exemple_K": {"C_mol_L": [1e-4, 1e-3, 1e-2, 1e-1], "tau_K_1_6e-5": [0.33, 0.12, 0.039, 0.013], "tau_K_1_8e-4": [0.72, 0.34, 0.13, 0.042]},
    },
}

INSISTANCES = [
    "produits en haut, réactifs en bas, coefficients en exposants ; l'eau solvant et les solides n'apparaissent pas",
    "Qr se calcule avec des concentrations en mol/L ; Qr et K n'ont pas d'unité",
    "Qr,i : concentrations dans l'état initial, APRÈS mélange (diviser par le volume total)",
    "Qr change pendant la transformation ; à l'équilibre il ne change plus : Qr,éq = K",
    "K ne dépend que de la température : pas de C, pas de l'état initial, pas de la dilution",
    "[AH]éq = C − [H₃O⁺]éq = C(1 − τ) : ne pas remplacer [AH]éq par C",
    "K = C·τ²/(1 − τ) : à démontrer avec le tableau (« montrer que » vaut des points)",
    "τ dépend de K ET de C ; K ne dépend pas de C",
]

VALEURS_REPERES = [
    "exemple A : acide éthanoïque C = 1,0·10⁻² mol/L, pH = 3,41 → [H₃O⁺]éq = 3,89·10⁻⁴ mol/L, [CH₃COOH]éq = 9,61·10⁻³ mol/L, τ = 0,0389, Qr,éq = 1,57·10⁻⁵",
    "exemple B : C = 1,0·10⁻² ; 5,0·10⁻³ ; 1,0·10⁻³ mol/L → τ = 0,039 ; 0,055 ; 0,117 et Qr,éq = 1,57 ; 1,61 ; 1,56·10⁻⁵ → K = 1,6·10⁻⁵ (25 °C)",
    "exemple D : σ = 4,6·10⁻³ S/m (C = 1,0·10⁻³ mol/L) → [H₃O⁺] = 1,18·10⁻⁴ mol/L → τ = 0,118 → K = 1,58·10⁻⁵",
    "exemple E : acide méthanoïque C = 1,0·10⁻² mol/L, pH = 2,90 → τ = 0,126, K = 1,8·10⁻⁴",
    "réaction inverse : K' = 1/(1,6·10⁻⁵) = 6,25·10⁴",
    "nationaux : Qr,éq = 1,57·10⁻⁵ (2017 N), 6,2·10⁻⁵ (2019 N), 1,65·10⁻⁵ (2020 N), 6,31·10⁻¹⁰ (2020 R), 1,77·10⁻⁵ (2021 N), 1,28·10⁻⁵ (2022 N), 5,0·10⁻⁴ (2022 R) ; Qr,i = 1,5 (2017 N), 1 (2018 R, 2019 R, 2020 R)",
]

CAS_TYPES = [
    {"cas": "Qr,éq d'un acide avec l'eau en fonction de C et du pH (ou de [H₃O⁺]éq)", "mots": "« Trouver, en fonction de C et du pH, l'expression du quotient de réaction Qr,éq »", "methode": "Qr,éq = [A⁻]éq·[H₃O⁺]éq/[AH]éq ; [A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; [AH]éq = C − 10^(−pH)", "points": "0,75", "frequence": "2 sessions (2017 N, 2022 N)"},
    {"cas": "Qr,éq (ou K) en fonction de C et τ", "mots": "« Montrer que Qr,éq = C·τ²/(1 − τ) » ; « Trouver l'expression de K en fonction de C et τ »", "methode": "tableau : [A⁻]éq = [H₃O⁺]éq = C·τ (ou [HO⁻] pour une base) ; [AH]éq = C(1 − τ) ; simplifier par C", "points": "0,5-0,75", "frequence": "4 sessions (2019 N, 2020 R, 2021 N, 2022 R)"},
    {"cas": "vérifier une valeur de Qr,éq donnée", "mots": "« Vérifier que Qr,éq = 1,65·10⁻⁵ »", "methode": "écrire l'expression, remplacer, comparer", "points": "0,5", "frequence": "2 sessions (2020 N, 2021 N)"},
    {"cas": "Qr,i d'une pile (solides absents, exposants)", "mots": "« Écrire l'expression du quotient de réaction Qr,i à l'état initial puis calculer sa valeur »", "methode": "Qr,i = [ion produit]ᵢ^c/[ion réactif]ᵢ^a ; pas de solide", "points": "0,5", "frequence": "3 sessions (2017 N, 2018 R, 2019 R) ; la suite (sens) au semestre 2"},
    {"cas": "Qr,i d'un mélange de solutions", "mots": "« Calculer, à l'instant t = 0, le quotient de réaction Qr,i »", "methode": "[X]ᵢ = C·V/V_T pour chaque espèce ; V_T se simplifie", "points": "0,5", "frequence": "1 session (2020 R)"},
    {"cas": "K à partir des quantités à l'équilibre (estérification, hydrolyse)", "mots": "« Montrer que K = 4 » ; « Calculer la constante d'équilibre K »", "methode": "K = Qr,éq ; V se simplifie ; ici l'eau est un produit ou un réactif (pas le solvant)", "points": "0,5-0,75", "frequence": "3 sessions (2016 R, 2017 R, 2018 R) ; chapitre estérification (semestre 2)"},
]

PIEGES = [
    {"erreur": "écrire l'eau solvant dans Qr", "geste": "barrer H₂O dans l'équation avant d'écrire Qr : le solvant n'a pas de concentration à écrire"},
    {"erreur": "écrire un solide dans Qr ([Zn], [Cu])", "geste": "repérer les (s) dans l'équation : ils n'entrent pas dans Qr"},
    {"erreur": "oublier les exposants (2017 N : [Al³⁺]²/[Cu²⁺]³)", "geste": "les coefficients de l'équation deviennent les puissances"},
    {"erreur": "Qr à l'envers (réactifs au numérateur)", "geste": "« produits en haut » : dire la phrase en écrivant la barre de fraction"},
    {"erreur": "[AH]éq = C", "geste": "tableau : [AH]éq = C − x_éq/V = C − [H₃O⁺]éq = C(1 − τ)"},
    {"erreur": "Qr,i avec les concentrations avant mélange", "geste": "calculer n = C·V puis diviser par le volume total V_T"},
    {"erreur": "croire que K change avec la dilution", "geste": "trois concentrations, même Qr,éq (exemple B) : K ne dépend que de la température"},
    {"erreur": "donner une unité à Qr ou à K", "geste": "Qr et K sont sans unité ; on écrit seulement la valeur"},
]

ERREURS_EXAMEN = [
    {"erreur": "expression de Qr,éq sans passer par le tableau (« montrer que » non justifié)", "geste": "écrire [A⁻]éq = [H₃O⁺]éq = C·τ et [AH]éq = C(1 − τ) avant de remplacer", "source": "2019 N, 2020 R, 2021 N, 2022 R"},
    {"erreur": "[AH]éq remplacé par C : Qr,éq = 10^(−2pH)/C", "geste": "garder « C − 10^(−pH) » au dénominateur (le corrigé l'exige)", "source": "2017 N, 2022 N"},
    {"erreur": "τ arrondi trop tôt (0,22 au lieu de 0,225)", "geste": "garder trois chiffres significatifs pour τ dans le calcul de K", "source": "2019 N"},
    {"erreur": "solides ou eau dans Qr,i d'une pile", "geste": "Qr,i = [Zn²⁺]ᵢ/[Cu²⁺]ᵢ : seulement les ions en solution", "source": "2017 N, 2018 R, 2019 R"},
    {"erreur": "concentrations initiales prises avant mélange", "geste": "[X]ᵢ = C·V/V_T ; écrire que V_T se simplifie", "source": "2020 R"},
]

CONSEILS = [
    "écrire d'abord l'équation avec ⇌, barrer l'eau solvant et les solides, puis écrire Qr (produits en haut, réactifs en bas, exposants)",
    "relation littérale, puis application numérique, puis résultat SANS unité",
    "dans un exercice acide + eau, enchaîner : pH → [H₃O⁺]éq → τ → Qr,éq = C·τ²/(1 − τ) (les questions se suivent toujours dans cet ordre)",
    "quand la question dit « vérifier que Qr,éq = … », écrire l'expression puis le calcul : la valeur donnée ne suffit pas",
]

ANALOGIES = [
    {"image": "la recette du thé : chaque famille a ses proportions, mais une fois le thé servi, le rapport sucre/eau ne change plus — K est ce rapport final, propre à la réaction", "limite": "K est un quotient de concentrations avec des exposants, pas un simple rapport de deux quantités"},
    {"image": "le compteur du taxi qui monte puis s'arrête à destination : Qr monte depuis Qr,i et s'arrête à Qr,éq = K", "limite": "Qr peut aussi descendre vers K quand on part des produits"},
    {"image": "la balance réglée sur la même graduation : quelle que soit la quantité de départ, l'aiguille s'arrête au même trait K", "limite": "le trait K change si on change la température"},
]

A_NE_PAS_DIRE = [
    {"terme": "[H₂O] dans Qr", "motif": r"\[H₂O\]", "pourquoi": "l'eau est le solvant : elle n'apparaît pas dans Qr (solution aqueuse)", "dire_plutot": "l'eau solvant n'apparaît pas dans Qr"},
    {"terme": "un solide dans Qr", "motif": r"\[(Zn|Cu|Al|Ni|Cd|Ag|Fe)\]", "pourquoi": "les espèces solides n'apparaissent pas dans Qr", "dire_plutot": "Qr = [Zn²⁺]/[Cu²⁺] (ions seulement)"},
    {"terme": "Qr à l'envers", "motif": r"Q_?r\s*=\s*\[CH₃COOH\]\s*/", "pourquoi": "produits au numérateur, réactifs au dénominateur", "dire_plutot": "Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH]"},
    {"terme": "K dépend de la concentration ou de l'état initial", "motif": r"\bK\b\s+(d[ée]pend|varie|change)\s+(de|avec|selon)\s+(la concentration|l'[ée]tat initial|la dilution|C\b)", "pourquoi": "K ne dépend que de la température", "dire_plutot": "τ dépend de C ; K ne dépend que de la température"},
    {"terme": "la dilution change K", "motif": r"dilu\w*.{0,30}(change|modifie|augmente|diminue|fait varier)\s+(la constante|\bK\b)", "pourquoi": "même Qr,éq pour trois concentrations (exemple B)", "dire_plutot": "la dilution augmente τ ; K ne change pas"},
    {"terme": "K ou Qr avec une unité", "motif": r"\b(K|Q_?r[,\wéq]*)\s*=\s*[0-9][0-9,]*(·10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)?\s*(mol|S/m|L)\b", "pourquoi": "Qr et K sont sans unité", "dire_plutot": "K = 1,6·10⁻⁵ (sans unité)"},
    {"terme": "τ = K (confusion)", "motif": r"τ\s*=\s*K\b|\bK\s*=\s*τ\b", "pourquoi": "τ et K sont deux grandeurs différentes : K = C·τ²/(1 − τ)", "dire_plutot": "K = C·τ²/(1 − τ)"},
    {"terme": "à l'équilibre la réaction s'arrête", "motif": r"(l'[ée]quilibre|la r[ée]action|les r[ée]actions).{0,20}(s'arr[êe]te|est arr[êe]t[ée]e|sont arr[êe]t[ée]es|ne se fait plus|ne se font plus)|plus rien ne se passe|[ée]quilibre statique", "pourquoi": "l'équilibre est dynamique (chapitre précédent)", "dire_plutot": "les deux sens continuent à la même vitesse ; Qr ne change plus"},
    {"terme": "Ka, pKa, Ke (chapitre suivant)", "motif": r"\bp?K[ae]\b|\bp?K_?[AE]\b|produit ionique|autoprotolyse|pr[ée]dominan|constante d'acidit", "pourquoi": "réactions acide-base : chapitre 13", "dire_plutot": "on le verra au chapitre suivant"},
    {"terme": "critère d'évolution, Le Chatelier", "motif": r"crit[èe]re d'[ée]volution|[ée]volution spontan|chatelier|loi de mod[ée]ration|guldberg|action de masse|enthalpie", "pourquoi": "critère d'évolution : semestre 2 (piles) ; Le Chatelier, Guldberg-Waage, enthalpie : hors programme", "dire_plutot": "au semestre 2, on comparera Qr,i à K"},
    {"terme": "Henderson, Ostwald, activité", "motif": r"henderson|hasselbalch|ostwald|degr[ée] d'ionisation|activit[ée]", "pourquoi": "hors programme (perimetre.json)", "dire_plutot": "concentrations en mol/L ; taux d'avancement final τ"},
]

EXCLUS = [
    "constante d'acidité Ka, pKa, produit ionique Ke, [HO⁻] = Ke/[H₃O⁺], K = Ka/Ke, K = Ka₁/Ka₂, prédominance, indicateurs : chapitre 13 (acides_bases) — 2016 N, 2019 N 3.4, 2020 R 2.2, 2023 N 2.2, 2024 N, 2025 N",
    "comparaison de Qr,i à K pour prévoir le sens d'une transformation (piles, semestre 2, perimetre.json clé piles_electrolyse) — 2017 N I.2, 2018 R I.2, 2019 R I.1, 2020 R 2.4",
    "K d'une estérification ou d'une hydrolyse, rendement, déplacement par excès d'un réactif : chapitre esterification_hydrolyse (semestre 2) ; ici seulement n5 (K = 4, 2017 R) comme exemple de K = Qr,éq",
    "loi d'action de masse (Guldberg-Waage), Le Chatelier, loi de modération, enthalpie, activité, Henderson : hors programme (perimetre.json)",
    "valeur de K en fonction de la température (aucune loi au programme : on dit seulement « K ne dépend que de la température »)",
    "τ, pH, conductimétrie, dilution : chapitre précédent (rappelés en r1, r2, m2)",
]
