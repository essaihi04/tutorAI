"""Contrôle voix ↔ simulation d'un cours « au tableau » (17 novembre 2026).

Règle du professeur : ce que dit le tuteur, la simulation le montre au même instant ; la baguette (`highlight`)
se pose sur l'objet nommé dans la phrase, jamais sur un autre ; un processus décrit sans animation est un défaut.

Pour chaque diapositive à simulation, le script liste chaque entrée de `concentration.pointage` :
l'instant estimé dans la voix (même calcul que le lecteur : place du mot dans le texte parlé, rapportée à la durée
de la piste ; une commande part 0,9 s plus tôt), le morceau de phrase, les objets qu'il nomme (lexique ci-dessous)
et la commande ou le repère visé. Il signale :
  - REPERE   la baguette vise un repère que le morceau de phrase ne nomme pas (ou un repère inconnu du lexique) ;
  - PROCESSUS une phrase décrit un processus animé (lexique `PROCESSUS`) sans `play_until` vers un des moments
             attendus dans cette phrase ;
  - MOMENT   un `play_until` vise un moment absent du code de la simulation ;
  - IFRAME   deux diapositives de suite ont la même URL de simulation (l'iframe n'est pas rechargée : la scène de la
             diapositive précédente reste, souvent finie, et les `play_until` sont refusés) ;
  - DEPART   une diapositive pilotée par des `play_until` démarre la scène avec `start` (elle court seule, sans la voix) ;
  - GESTE    un geste qui part plus de 0,6 s après son mot (le tuteur fait un geste par seconde : trop serrés, ils prennent du retard).

Usage : python backend/scripts/verifier_pointage_simulations.py [chemin du cours] [--diapo ID] [--ecarts]
Sortie non nulle s'il reste des écarts (utilisé par backend/app/tests/test_pointage_simulations.py).
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import parse_qs, urlparse

RACINE = Path(__file__).resolve().parents[2]
PUBLIC = RACINE / "frontend" / "public"
COURS_DEFAUT = RACINE / "backend" / "data" / "courses" / "svt_ch1_reactions_responsables_liberation_energie.json"
AVANCE_COMMANDE = 0.9   # CourseFocusStage.tsx : une commande part un peu avant le mot
GESTE_S = 1.0            # CourseFocusStage.tsx : un geste à la fois, une seconde chacun

# ── Lexique : pour chaque simulation, les mots qui nomment chaque repère (voix « mixed » : darija + français) ──
# Un repère sans entrée est accepté s'il est nommé par son identifiant (« sphere » → « sphère »…) ; mieux vaut le décrire.
ECRIT = r"كنكتبو|نكتبو|كتكتب|نكونو|نعاود نقرا|سميتو|سميتها|نسميو|écrit|définition|la réaction|l'équation|le bilan"
LEXIQUE: dict[str, dict[str, str]] = {
    "chaine.html": {
        "mitochondrie_zoom": r"mitochondrie|الصغيرة|المربع",
        "membrane": r"membrane|la bande",
        "matrice": r"matrice",
        "espace": r"espace|الفوق",
        "t1": r"(?<![A-Za-z])[TC] un\b|premier transporteur",
        "t2": r"(?<![A-Za-z])[TC] deux\b",
        "t3": r"(?<![A-Za-z])[TC] trois\b",
        "t4": r"(?<![A-Za-z])[TC] quatre\b|سد",
        "transporteurs": r"transporteurs?\b",
        "taxi": r"N A D H|NADH|N A D plus|NAD\+|taxi|R H deux|transporteurs? réduits?|le transporteur est oxydé|F A D H|ورجع خاوي",
        "electrons": r"électrons?|وتجمعو من اللور",
        "protons": r"protons?|H plus",
        "protons_matrice": r"protons?|H plus|التحت قلال",
        "o2": r"dioxygène|O deux|demi O",
        "poignee_o2": r"نحيدو le dioxygène|بلا dioxygène|sans dioxygène",
        "eau": r"l'eau|H2O|molécule d'eau",
        "atp": r"ATP|ADP|phosphate",
        "sphere": r"sphères?|C cinq",
        "equation": ECRIT + r"|بالflèches|accepteur|gradient|phosphorylation",
        "ecrit_taxi_eq": ECRIT + r"|H plus est oxydé",
        "ecrit_relais": ECRIT + r"|réactions d'oxydoréduction",
        "ecrit_eau_eq": ECRIT + r"|un demi O deux",
        "ecrit_bilan_fadh": r"ATP|كيعطي trois",
        "ecrit_accepteur": r"accepteur",
        "ecrit_gradient": r"gradient",
        "ecrit_atp_eq": r"phosphorylation|" + ECRIT,
        "ecrit_chaine_causale": ECRIT + r"|بالflèches",
        "schema": r"schéma",
        "structures": r"الأرقام|structures|من un حتى",
        "reactions": r"الحروف|réactions",
        "etiquettes": r"étiquettes",
        "legende": r"légende",
    },
}
# Processus décrits par la voix → moments qui les montrent (au moins un `play_until` vers l'un d'eux dans la phrase).
PROCESSUS: dict[str, list[tuple[str, list[str]]]] = {
    "chaine.html": [
        (r"جا N A D H|NADH,H\+ arrive", ["taxi_arrive"]),
        (r"طيح deux protons", ["taxi_decharge", "entree_fadh2"]),
        (r"ورجع خاوي، N A D plus", ["nad_repart"]),
        (r"كيدوزو من T un|ل T deux", ["e_t2", "e_t3", "electrons_passent"]),
        (r"وفاللخر ل T quatre", ["electrons_passent"]),
        (r"كاين le dioxygène", ["o2_arrive"]),
        (r"خدا deux électrons", ["o2_recoit"]),
        (r"وتكون l'eau", ["eau_formee"]),
        (r"un demi O deux, deux protons et deux électrons donnent", ["equation_eau"]),
        (r"accepteur final", ["o2_accepteur"]),
        (r"les électrons بقاو", ["sans_o2_arret", "bloque"]),
        (r"des protons كيطلعو", ["protons_pompes"]),
        (r"تجمعو بزاف ديال les protons", ["espace_charge"]),
        (r"سميتو le gradient", ["gradient_ecrit"]),
        (r"les protons كيهبطو", ["retour_par_la_sphere"]),
        (r"ولاو ATP", ["atp_forme"]),
        (r"N A D H, H plus est oxydé", ["equation_nadh"]),
        (r"سد T quatre", ["cyanure_pose", "bloque"]),
        (r"ما بقاش كياخد les électrons", ["o2_non"]),
        (r"ما بقاش le pompage", ["pas_d_atp", "pas_pompage"]),     # pas_pompage : ?maillons (18 novembre 2026)
        (r"إذن ما بقاش le gradient", ["pas_d_atp", "pas_gradient"]),
        (r"شوف الأرقام", ["structures"]),
        (r"وشوف الحروف", ["reactions"]),
        (r"دابا les réponses", ["solution"]),
        (r"F A D H deux كيعطي", ["entree_fadh2"]),
        (r"كيعطي deux ATP", ["bilan_fadh2"]),
    ],
}
# ── Les autres simulations du cours (17 novembre 2026), même principe : repère → mots qui le nomment ; processus → moments.
LEXIQUE["depart.html"] = {
    "cellule": r"الخلية|la cellule",
    "membrane": r"membrane",
    "hyaloplasme": r"hyaloplasme",
    "noyau": r"noyau",
    "mitochondries": r"mitochondries?",
    "ville": r"البلاد|ville",
    "mairie": r"المدير|mairie",
    "rues": r"الطرقان|rues",
    "usines": r"معامل|usines",
    "pain": r"الخبز|amidon",
    "sang": r"الدم|sang",
    "molecule": r"molécule|six carbones|C six",
    "liaisons": r"liaisons|atomes|énergie chimique",
    "buche": r"العود|bûche",
    "feu": r"كيشعل|الحرارة|brûle",
    "pas_a_pas": r"مرحلة ب مرحلة|بشوية|pas à pas",
}
PROCESSUS["depart.html"] = [
    (r"كيتقطع ويولي glucose", ["g_sang"]),
    (r"كتقطع هاد les liaisons", ["g_casser"]),
    (r"وملي كيشعل", ["g_feu"]),
    (r"مرحلة ب مرحلة", ["g_pas_a_pas"]),
]
LEXIQUE["atp.html"] = {
    "adenosine": r"adénosine",
    "phosphates": r"phosphates",
    "atp": r"l'ATP|A T P|la molécule",
    "liaison": r"la liaison",
    "phosphate_libre": r"le phosphate|Pi\b",
    "adp": r"l'ADP",
    "energie": r"l'énergie",
    "travail": r"للعضلة|muscle|fibre",
    "kj": r"kilojoules|mole",
    "recharge": r"respiration|fermentation|le glucose",
    "ecrit_hydrolyse": ECRIT + r"|hydrolyse|A T P plus l'eau|donne A D P",
    "ecrit_phosphorylation": ECRIT + r"|phosphorylation|donne A T P",
    "equation": ECRIT + r"|hydrolyse|phosphorylation",
    "cycle": r"le cycle",
    "ecrit_regenere": r"كتعاود تكونو|قليل|régénéré",
}
PROCESSUS["atp.html"] = [
    (r"خرج le phosphate", ["liaison_rompue"]),
    (r"خرجات l'énergie", ["energie_liberee"]),
    (r"جات l'énergie من le glucose", ["recharge"]),
    (r"رجع تلصق مع l'ADP", ["atp_reforme"]),
    (r"كنكتبو: A T P plus l'eau", ["hydrolyse"]),
    (r"كنكتبو: A D P plus phosphate", ["phosphorylation"]),
    (r"l'hydrolyse من جهة", ["cycle_hydrolyse"]),
    (r"la phosphorylation من جهة أخرى", ["cycle_phosphorylation"]),
]
LEXIQUE["exao.html"] = {
    "montage": r"le montage|expérience|document",
    "graphique": r"le graphique|la courbe كاملة",
    "medaillon": r"levures",
    "sonde_o2": r"sondes?.*dioxygène|ديال le dioxygène",
    "sonde_co2": r"dioxyde de carbone",
    "seringue": r"seringue",
    "axe_temps": r"l'axe horizontal|le temps",
    "axe_vertical": r"l'axe vertical|la concentration",
    "courbe_o2": r"la courbe|les courbes|dioxygène|quarante pour cent|ثابتة|كينقص|كتنقص",
    "courbe_co2": r"dioxyde de carbone|C O deux",
    "courbe_ethanol": r"éthanol",
    "courbe_atp": r"l'ATP",
    "courbe_h": r"la concentration|la courbe|نوصفو",
    "lecture_o2": r"sept virgule cinq|milligrammes",
    "o2_epuise": r"zéro|تسالا",
    "ecrit_respiration": r"respiration",
    "ecrit_fermentation": r"fermentation",
    "aerobie": r"aérobie",
    "anaerobie": r"anaérobie",
    "mitochondries": r"mitochondries",
    "milieu": r"dioxygène|milieu",
    "solution": r"la solution",
    "electrode": r"pH-mètre|électrode",
    "ajout_glucose": r"glucose",
    "ajout_pyruvate": r"acide pyruvique",
    "ajout_adp_pi": r"ADP",
    "ajout_cyanure": r"cyanure",
    "injection": r"زدنا|dioxygène|injection",
    "pic": r"quarante-quatre|طلعات",
    "note_cya": r"vérifiée|cyanure|بقا ثابت",
    "ecrit_hypothese": r"bloquerait|conditionnel|hypothèse",
}
PROCESSUS["exao.html"] = [
    (r"كتنقص بزربة", ["o2_baisse"]),
    (r"le dioxyde de carbone: كيطلع", ["co2_monte"]),
    (r"وصل لzéro", ["o2_epuise"]),
    (r"باقي كيطلع", ["co2_continue"]),
    (r"l'éthanol بدا كيبان", ["ethanol_apparait"]),
    (r"ولاو كيديرو la fermentation", ["fermentation"]),
    (r"دابا زدنا le glucose", ["glucose_ajoute"]),
    (r"زدنا l'acide pyruvique", ["pyruvate_ajoute"]),
    (r"le dioxygène بدا كينقص", ["ajout_pyruvate"]),
    (r"زدنا ADP و phosphate\.", ["ajout_adp_pi"]),
    (r"le dioxygène طاح", ["o2_baisse_atp_monte"]),
    (r"زدنا شوية ديال le dioxygène", ["o2_injecte"]),
    (r"طلعات بزربة", ["pic"]),
    (r"بدات كتنقص بشوية", ["descente", "valeur_initiale"]),
    (r"وفاللخر le cyanure", ["ajout_cyanure", "palier_final"]),
    (r"كنكتبو بالconditionnel", ["hypothese"]),
]
LEXIQUE["carrefour.html"] = {
    "glucose": r"glucose",
    "hyaloplasme": r"hyaloplasme",
    "glycolyse": r"glycolyse",
    "carrefour": r"carrefour|acides? pyruviques?|جوج الطرق",
    "bilan_glycolyse": r"ATP|N A D H",
    "question": r"dioxygène",
    "o2": r"dioxygène",
    "mitochondrie": r"mitochondrie|matrice",
    "respiration": r"respiration",
    "ecrit_krebs": r"Krebs|acétyl-CoA",
    "ecrit_chaine": r"chaîne respiratoire|membrane interne",
    "fermentation": r"fermentation|hyaloplasme",
    "bilan_respiration": r"ATP|A T P|C O deux|H deux O|produits",
    "bilan_fermentation": r"ATP|A T P|lactique|éthanol|produits",
    "bilans": r"produits|ATP",
    "ecrit_complete": r"dégradation complète",
    "ecrit_incomplete": r"dégradation incomplète",
}
PROCESSUS["carrefour.html"] = [
    (r"le glucose كيتحول|le glucose فle hyaloplasme", ["glycolyse_faite"]),
    (r"كيدخل للmitochondrie|كيدخل للmatrice", ["avec_o2_vers_matrice"]),
    (r"كيبقى فle hyaloplasme", ["sans_o2_sur_place"]),
    (r"le cycle de Krebs", ["matrice_krebs"]),
    (r"la chaîne respiratoire فla membrane", ["chaine_respiratoire"]),
]
LEXIQUE["taxi.html"] = {
    "molecule": r"molécule",
    "hydrogenes": r"hydrogènes",
    "taxi": r"transporteur|N A D|طاكسي",
    "fad": r"F A D",
    "ecrit_2h": r"protons|électrons|hydrogènes",
    "equation": ECRIT + r"|réduit|réduction",
    "ecrit_oxydee": r"oxydée|oxydation",
    "equation_retour": r"oxydé|rend deux protons",
    "regle": r"réduit|oxydé|ربح|خسر",
}
PROCESSUS["taxi.html"] = [
    (r"كتحيد منها des hydrogènes", ["deux_h_arraches"]),
    (r"جا واحد le transporteur", ["taxi_vide_arrive"]),
    (r"شوف: هز جوج hydrogènes", ["taxi_charge"]),
    (r"كيعطي les hydrogènes", ["taxi_part", "taxi_decharge"]),
    (r"il rend deux protons", ["taxi_decharge"]),
    (r"كيهز جوج hydrogènes كيولي F A D", ["fad_charge"]),
]
LEXIQUE["glycolyse.html"] = {
    "noyau": r"noyau",
    "mitochondrie": r"mitochondrie",
    "hyaloplasme": r"hyaloplasme",
    "glucose": r"glucose|six carbones|جا فle hyaloplasme",
    "ecrit_glycolyse": r"glycolyse",
    "sans_o2": r"dioxygène",
    "ecrit_depenses": r"ATP",
    "acide_pyruvique": r"trois|acide pyruvique|المجموعات",
    "nadh": r"N A D|طاكسي",
    "ecrit_formes": r"ATP",
    "gain_net": r"ربحنا|خسرنا|quatre",
    "ecrit_formule": r"formule|C H trois",
    "bilan": r"bilan",
    "reaction_droite": r"اليمين|les produits",
    "reaction_glucose": r"اليسار|عطاتنا|glucose",
    "reaction_adp": r"ADP|phosphates",
    "reaction_nad": r"N A D plus",
    "reaction": r"réaction globale|dégradation du glucose|" + ECRIT,
}
PROCESSUS["glycolyse.html"] = [
    (r"جوج ATP جاو", ["deux_atp_depenses"]),
    (r"ولاو جوج ديال المجموعات", ["coupure_en_deux"]),
    (r"وكل واحد هز جوج hydrogènes", ["taxis_charges"]),
    (r"تكونو quatre ATP", ["quatre_atp_formes"]),
    (r"على اليمين les produits", ["reaction_droite"]),
    (r"خاص deux ADP", ["reaction_adp"]),
    (r"خاص deux N A D plus", ["reaction_nad"]),
]
LEXIQUE["mitochondrie.html"] = {
    "mitochondrie": r"mitochondrie",
    "membrane_externe": r"membrane externe|الغشاء اللي برا",
    "membrane_interne": r"membrane interne|غشاء تاني",
    "cretes": r"crêtes|داخلة وخارجة",
    "espace_intermembranaire": r"espace intermembranaire|الفراغ",
    "matrice": r"matrice",
    "spheres_pedonculees": r"sphères pédonculées|الكورات|الراس ديالهم",
    "medaillon": r"الدائرة الصغيرة|الكورات|crête المكبرة|la crête",
    "lieu_matrice": r"Krebs|acétyl-CoA|matrice",
    "lieu_membrane": r"chaîne respiratoire|synthèse|membrane interne",
    "lieu_hyaloplasme": r"hyaloplasme|glycolyse",
    "titre": r"organite|double membrane",
    "schema": r"mitochondrie",
    "etiquettes": r"étiquettes",
    "zone_membranes": r"الأغشية|الفوق",
    "zone_interieur": r"التحت|matrice",
}
PROCESSUS["mitochondrie.html"] = []
LEXIQUE["pyruvate.html"] = {
    "hyaloplasme": r"hyaloplasme",
    "membranes": r"membranes",
    "matrice": r"matrice",
    "pyruvate": r"acide pyruvique|C H trois C O|دوز من",
    "formule": r"formule",
    "cooh": r"C O O H|دورة",
    "co2": r"C O deux|dioxyde de carbone",
    "ecrit_decarboxylation": r"décarboxylation|le carbone",
    "taxi": r"N A D|طاكسي",
    "ecrit_deshydrogenation": r"déshydrogénation|حيدنا",
    "coa": r"coenzyme A",
    "ecrit_coa": r"transporteur|coenzyme",
    "acetyl": r"acétyl",
    "equation": ECRIT + r"|donne",
    "fois_deux": r"deux fois",
}
PROCESSUS["pyruvate.html"] = [
    (r"دخل للmatrice", ["entre_dans_matrice"]),
    (r"خرج منو C O deux", ["co2_part"]),
    (r"وخدا جوج hydrogènes", ["taxi_prend_2h"]),
    (r"تلصق مع le coenzyme A", ["coa_s_accroche"]),
    (r"كنكتبو la réaction", ["equation"]),
]
LEXIQUE["krebs.html"] = {
    "roue": r"cycle|الدورة|tour",
    "acetyl": r"acétyl",
    "compose_4c": r"quatre carbones",
    "compose_6c": r"six carbones",
    "compose": r"carbones",
    "ecrit_cycle": r"رجعو ليه|cycle",
    "compteur": r"الحساب|compteur|دورة وحدة|deux C O deux",
    "co2": r"C O deux",
    "nadh": r"N A D H",
    "nadh_3": r"N A D H",
    "atp": r"ATP",
    "fadh2": r"F A D",
    "equation": ECRIT,
    "tableau_glucose": r"tableau|C O deux|glucose",
    "ecrit_co2": r"C O deux",
    "ecrit_nadh": r"N A D H",
    "ecrit_energie": r"transporteurs|l'énergie",
}
PROCESSUS["krebs.html"] = [
    (r"و le coenzyme A مشى", ["coa_repart", "compose_6c"]),
    (r"تلصق مع واحد le composé", ["compose_6c"]),
    (r"رجعنا لle composé", ["retour_4c"]),
    (r"اللول: خرج C O deux", ["co2_et_nadh_1"]),
    (r"من بعد: C O deux آخر", ["co2_et_nadh_2"]),
    (r"تصاوب ATP", ["atp"]),
    (r"F A D ولا F A D H deux", ["fadh2"]),
    (r"N A D H, H plus التالت", ["nadh_3"]),
    (r"le deuxième tour", ["second_tour"]),
]
LEXIQUE["vesicules.html"] = {
    "mitochondrie": r"mitochondrie|expérience",
    "ultrasons": r"ultrasons|la membrane interne",
    "vesicule": r"vésicules?|expérience",
    "spheres": r"sphères|protons كيخرجو",
    "interieur": r"داخل",
    "exterieur": r"برا",
    "atp": r"ATP|compteur",
    "pas_atp": r"ما كاينش l'ATP",
    "conclusion": r"synthèse|gradient|sphères",
}
PROCESSUS["vesicules.html"] = [
    (r"بالultrasons، قطعنا", ["manip_ultrasons"]),
    (r"وتكونو des vésicules", ["manip_vesicule"]),
    (r"اللول: le pH داخل كيساوي", ["ph_egaux_pas_d_atp"]),
    (r"les protons كيخرجو من les sphères", ["interieur_acide_atp"]),
    (r"حيدنا les sphères", ["sans_spheres_pas_d_atp"]),
]
LEXIQUE["fermentations.html"] = {
    "mitochondrie": r"mitochondrie",
    "taxi": r"N A D|hydrogènes",
    "glycolyse": r"glycolyse",
    "compteur_nad": r"zéro|شحال بقا|N A D plus",
    "pyruvique": r"acide pyruvique",
    "produit": r"acide lactique|trois carbones|éthanol",
    "reste_2c": r"deux carbones",
    "co2": r"C O deux",
    "ecrit_continue": r"glycolyse|تكمل",
    "ecrit_atp": r"ATP",
    "reaction": ECRIT + r"|acides lactiques|A T P",
    "ecrit_incomplete": r"incomplète|résidu",
    "type_cellule": r"muscle|bactéries|levure",
    "ecrit_manque": r"محتاجة|N A D plus خاوي",
}
PROCESSUS["fermentations.html"] = [
    (r"عطا جوج hydrogènes", ["taxi_rend_2h"]),
    (r"رجع خاوي", ["taxi_reparti_vide"]),
    (r"خرج منو C O deux", ["co2_part"]),
    (r"عطاه جوج hydrogènes", ["taxi_rend_2h"]),
    (r"كنكتبو", ["reaction_globale"]),
]
LEXIQUE["compteur.html"] = {
    "tableau": r"الحساب|tableau",
    "caisse": r"caisse|ATP",
    "glycolyse": r"glycolyse",
    "matrice": r"matrice|Krebs|acétyl",
    "chaine": r"chaîne|transporteurs",
    "ligne_glycolyse": r"glycolyse",
    "ligne_acetyl": r"acétyl",
    "ligne_krebs": r"Krebs|six N A D H|F A D H",
    "ligne_total": r"total",
    "regle": r"القاعدة|vaut",
    "ecrit_30": r"trente\b|dix fois trois",
    "ecrit_4": r"quatre|deux fois deux",
    "ecrit_34": r"trente-quatre",
    "ecrit_38": r"trente-huit",
    "conversion": r"نحولو|vaut",
    "total": r"trente-huit|trente-quatre",
}
PROCESSUS["compteur.html"] = [(r"نحولو les transporteurs", ["conversion"])]
LEXIQUE["rendement.html"] = {
    "barre_glucose": r"la barre|glucose|kilojoules",
    "ecrit_glucose": r"la valeur|glucose",
    "briques": r"briques|ATP|trente virgule cinq",
    "ecrit_1159": r"mille cent cinquante-neuf|trente-huit fois",
    "relation": r"rendement|مقسومة",
    "ecrit_application": r"application|sur deux mille|trente-huit fois",
    "ecrit_resultat": r"quarante virgule cinq|résultat",
    "chaleur": r"chaleur|حرارة|الطوموبيل",
    "barre_fermentation": r"fermentation",
    "residu": r"résidu|lactique|éthanol",
}
PROCESSUS["rendement.html"] = [(r"خرج على شكل la chaleur", ["chaleur"]), (r"شوف هاد les petites briques", ["briques_respiration"])]
LEXIQUE["comparer.html"] = {
    "atp": r"ATP|قطع",
    "ecrit_61": r"kilojoules",
    "rendement": r"rendement|deux virgule treize",
    "residu": r"lactique|éthanol|résidu",
    "ferm_produits": r"résidu|lactique|éthanol",
    "ferm_degradation": r"incomplète|التحليل",
    "resp_degradation": r"complète",
    "mineraux": r"minéraux|C O deux|H deux O",
    "comparaison": r"tableau|الفرق",
    "mitochondrie": r"mitochondrie",
    "glucose": r"glucose",
}
PROCESSUS["comparer.html"] = [(r"باقية فl'acide lactique", ["residu"]), (r"كيبقاو غير des déchets minéraux", ["mineraux"])]
LEXIQUE["bilan.html"] = {}
PROCESSUS["bilan.html"] = []
LEXIQUE["carte.html"] = {}
PROCESSUS["carte.html"] = []
FIN_PHRASE = re.compile(r"[.!?؟]")


@dataclass
class Ligne:
    diapo: str
    t: float
    mot: str
    morceau: str
    nommes: list[str]
    action: str
    ecart: str = ""


@dataclass
class Rapport:
    lignes: list[Ligne] = field(default_factory=list)
    ecarts: list[str] = field(default_factory=list)


def fichier_sim(url: str) -> str:
    return Path(urlparse(url).path).name


def source_sim(url: str) -> str:
    """Le code de la page, suivi des scripts de SON dossier qu'elle charge (18 novembre 2026, maths : les vues de
    calculs.html / etapes.html lisent leurs lignes, moments et repères dans calculs-vues.js ou calculs-donnees.js ;
    sans eux, chaque moment de ces vues était signalé « introuvable » à tort)."""
    chemin = PUBLIC / urlparse(url).path.lstrip("/")
    try:
        code = chemin.read_text(encoding="utf-8")
    except OSError:
        return ""
    for src in re.findall(r"<script[^>]*\bsrc=\"([^\"]+)\"", code):
        voisin = PUBLIC / urlparse(src).path.lstrip("/")
        if voisin.parent == chemin.parent and voisin.suffix == ".js":
            try:
                code += "\n" + voisin.read_text(encoding="utf-8")
            except OSError:
                pass
    return code


def nommes_dans(texte: str, lexique: dict[str, str]) -> list[str]:
    out = []
    for rep, motif in lexique.items():
        m = re.search(motif, texte, re.I)
        if m:
            out.append((m.start(), rep))
    return [r for _, r in sorted(out)]


def bornes_phrase(parole: str, i: int) -> tuple[int, int]:
    debut = 0
    for m in FIN_PHRASE.finditer(parole, 0, i):
        debut = m.end()
    m = FIN_PHRASE.search(parole, i)
    return debut, (m.end() if m else len(parole))


def verifier(cours: dict, seule: str | None = None) -> Rapport:
    r = Rapport()
    precedente = None
    for act in cours.get("activities", []):  # noqa: C901 (un seul parcours, lisible de haut en bas)
        for s in act.get("slides", []):
            vis = s.get("visual") or {}
            url = vis.get("url") or ""
            conc = s.get("concentration") or {}
            simu = vis.get("kind") == "simulation" and "-tableau/" in url
            if seule and s["id"] != seule:
                precedente = url if simu else None
                continue
            if not simu:
                precedente = None
                continue
            nom = fichier_sim(url)
            lexique = LEXIQUE.get(nom, {})
            parole = ((s.get("speech_text") or {}).get("mixed") or "").strip()
            duree = ((s.get("audio") or {}).get("mixed") or {}).get("duration_ms", 0) / 1000
            pointage = conc.get("pointage") or []
            code = source_sim(url)
            if precedente == url:
                r.ecarts.append(f"{s['id']} IFRAME même URL que la diapositive précédente ({url}) : la scène n'est pas rechargée")
            precedente = url
            if conc.get("demarrer") == "start" and any(p.get("commande") == "play_until" for p in pointage):
                r.ecarts.append(f"{s['id']} DEPART demarrer=start : la scène court seule ; ouvrir figée (?depart=…) et demarrer=reset")
            instants = []
            for p in pointage:
                mot = p.get("mot", "")
                i = parole.find(mot)
                t = max(0.0, (i / max(1, len(parole))) * duree - 0.3 - (AVANCE_COMMANDE if p.get("commande") else 0)) if i >= 0 else -1
                instants.append(t)
                deb, fin = bornes_phrase(parole, max(0, i + len(mot) - 1))
                # le morceau qui accompagne le geste : du mot jusqu'au mot du geste suivant ou à la fin de la phrase
                suivants = [parole.find(q.get("mot", ""), i + 1) for q in pointage if q is not p]
                suivants = [j for j in suivants if j > i]
                fin_morceau = min([fin] + [j for j in suivants if j < fin]) if i >= 0 else 0
                morceau = parole[i:max(fin_morceau, i + len(mot))] if i >= 0 else ""
                nommes = nommes_dans(morceau, lexique)
                if p.get("commande"):
                    action = f"{p['commande']} {json.dumps(p.get('parametres') or {}, ensure_ascii=False)}"
                else:
                    action = f"highlight {p.get('repere') or p.get('cible')}"
                ligne = Ligne(s["id"], t, mot, morceau.strip(), nommes, action)
                if i < 0:
                    ligne.ecart = "mot introuvable dans la voix"
                elif p.get("repere"):
                    rep = p["repere"]
                    if lexique and rep not in lexique:
                        ligne.ecart = f"repère « {rep} » absent du lexique"
                    elif lexique and rep not in nommes:
                        ligne.ecart = f"REPERE la baguette va sur « {rep} », la phrase nomme {nommes or 'rien du lexique'}"
                    if code and not re.search(r"['\"`]" + re.escape(rep) + r"['\"`]|'t' \+ \(k \+ 1\)|'ecrit_' \+", code):
                        ligne.ecart = (ligne.ecart + " ; " if ligne.ecart else "") + f"repère « {rep} » introuvable dans {nom}"
                elif p.get("commande") == "play_until":
                    m = (p.get("parametres") or {}).get("moment")
                    if m and code and not re.search(r"\b" + re.escape(m) + r"\b", code):
                        ligne.ecart = f"MOMENT « {m} » introuvable dans {nom}"
                if ligne.ecart:
                    r.ecarts.append(f"{s['id']} {ligne.ecart} — « {ligne.morceau[:70]} »")
                r.lignes.append(ligne)
            # gestes en file : le tuteur fait un geste par seconde ; un geste qui arrive plus de 0,6 s après son mot est en retard
            prochain = -1e9
            for t, p in sorted(((t, p) for t, p in zip(instants, pointage) if t >= 0), key=lambda x: x[0]):
                eff = max(t, prochain)
                prochain = eff + GESTE_S
                mot_t = t + (AVANCE_COMMANDE if p.get("commande") else 0)
                if eff - mot_t > 0.6:
                    r.ecarts.append(f"{s['id']} GESTE « {p.get('mot')} » part à {eff:.1f} s, {eff - mot_t:.1f} s après son mot (gestes trop serrés)")
            # processus dits sans animation
            for motif, moments in PROCESSUS.get(nom, []):
                for m in re.finditer(motif, parole):
                    deb, fin = bornes_phrase(parole, m.start())
                    deb = bornes_phrase(parole, max(0, deb - 2))[0]   # la commande peut partir avec la phrase d'avant
                    ok = False
                    for p in pointage:
                        j = parole.find(p.get("mot", ""))
                        if p.get("commande") == "play_until" and (p.get("parametres") or {}).get("moment") in moments and deb - 1 <= j < fin:
                            ok = True
                    if not ok:
                        r.ecarts.append(f"{s['id']} PROCESSUS « {m.group()} » sans play_until vers {moments} dans la phrase « {parole[deb:fin].strip()[:70]} »")
    return r


def main(argv: list[str]) -> int:
    chemin = COURS_DEFAUT
    seule = None
    juste_ecarts = "--ecarts" in argv
    args = [a for a in argv if a != "--ecarts"]
    if "--diapo" in args:
        k = args.index("--diapo")
        seule = args[k + 1]
        del args[k:k + 2]
    if args:
        chemin = Path(args[0])
    cours = json.loads(chemin.read_text(encoding="utf-8"))
    r = verifier(cours, seule)
    if not juste_ecarts:
        diapo = None
        for l in r.lignes:
            if l.diapo != diapo:
                diapo = l.diapo
                print(f"\n== {diapo}")
            drapeau = "  ✗ " + l.ecart if l.ecart else ""
            print(f"  {l.t:5.1f}s  {l.action:<48} | nomme {','.join(l.nommes) or '—':<28} | « {l.morceau[:60]} »{drapeau}")
    print(f"\n{len(r.ecarts)} écart(s)")
    for e in r.ecarts:
        print("  -", e)
    return 1 if r.ecarts else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
