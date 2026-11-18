"""Nouvelle logique du cours phys_ch5_energie_nucleaire (18 novembre 2026, skill logique-de-cours).

Lit le cours en ligne backend/data/courses/phys_ch5_energie_nucleaire.json (jamais modifié) et écrit la version en
attente backend/data/courses/en_attente/phys_ch5_energie_nucleaire.json : deux diapositives déplacées, huit textes
réécrits pour que la voix pose les données et la méthode SANS donner le résultat, trois exercices du national joués
en étapes que l'élève fait lui-même. Architecture et raisons :
backend/data/curriculum/architecture/phys_ch5_energie_nucleaire.md.
Relançable : repart toujours du cours en ligne.  Usage : python -X utf8 scripts/voix/logique_ch5_energie_nucleaire.py"""
import copy, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from logique_ch4_radioactivite import r, demo     # mêmes aides (réaction, démonstration vérifiée)

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
DECK = "phys_ch5_energie_nucleaire"
SRC = os.path.join(RACINE, "backend/data/courses", DECK + ".json")
DST = os.path.join(RACINE, "backend/data/courses/en_attente", DECK + ".json")

PARTIES = [
    ("en_partie1", "I. La masse peut devenir énergie", "situation", 26,
     ["en_m1_soleil", "en_p1_energie", "en_p2_puissances", "en_m2_einstein", "en_m2b_un_gramme", "en_m3_unites",
      "en_m3b_electronvolt", "en_m4_931", "en_m4b_energie_masse"]),
    ("en_partie2", "II. Le défaut de masse", "explanation", 18,
     ["en_d1_composition", "en_d2_balance", "en_d3_formule", "en_d4_carbone"]),
    ("en_partie3", "III. L'énergie de liaison", "explanation", 16,
     ["en_l1_separer", "en_l2_former", "en_l3_calcul", "en_l4_par_nucleon"]),
    ("en_partie4", "IV. Stabilité et courbe d'Aston", "explanation", 20,
     ["en_s1_stabilite", "en_s2_piege", "en_a1_courbe", "en_a2_zones", "en_a2b_fission", "en_a3_comparer"]),
    ("en_partie5", "V. Réactions provoquées : fission et fusion", "explanation", 18,
     ["en_r1_spontanee", "en_r2_fission", "en_r3_chaine", "en_p3_charges", "en_r4_fusion", "en_r5_soddy"]),
    ("en_partie6", "VI. Énergie libérée : par les masses", "application", 22,
     ["en_b1_masse_diminue", "en_b2_methode", "en_b2b_energie", "en_b4_fission_calcul", "en_b3_fusion_calcul",
      "en_b5_beta"]),
    ("en_partie7", "VII. Énergie libérée : par les énergies de liaison", "application", 18,
     ["en_e1_diagramme", "en_e2_formule", "en_e3_2023", "en_e4_polonium"]),
    ("en_partie8", "VIII. L'énergie d'un échantillon, applications et dangers", "application", 16,
     ["en_n1_echantillon", "en_n1b_energie_totale", "en_n2_comparaison", "en_n3_2025",
      "en_r3b_applications_dangers"]),
    ("en_partie9", "IX. Cas types du national", "evaluation", 10, ["en_c1_cas_types", "en_c2_qcm2019"]),
    ("en_bilan", "X. Bilan du chapitre", "evaluation", 10, ["en_z1_bilan", "en_z2_carte"]),
]

SEANCES = [
    ("en_s1", "Séance 1 — Les outils, puis E = m·c²", [
        ("en_s1_b0", "Avant de commencer : l'énergie et les puissances de dix", ["en_m1_soleil", "en_p1_energie", "en_p2_puissances"]),
        ("en_s1_b1", "E = m·c² et l'unité de masse u", ["en_m2_einstein", "en_m2b_un_gramme", "en_m3_unites"]),
        ("en_s1_b1b", "L'électronvolt, 1 u = 931,5 MeV/c², l'énergie de masse", ["en_m3b_electronvolt", "en_m4_931", "en_m4b_energie_masse"])]),
    ("en_s2", "Séance 2 — Défaut de masse, énergie de liaison, stabilité", [
        ("en_s1_b2", "Le noyau, on le pèse : le défaut de masse", ["en_d1_composition", "en_d2_balance", "en_d3_formule", "en_d4_carbone"]),
        ("en_s1_b3", "L'énergie de liaison", ["en_l1_separer", "en_l2_former", "en_l3_calcul"]),
        ("en_s2_b1", "E_ℓ/A et la stabilité", ["en_l4_par_nucleon", "en_s1_stabilite", "en_s2_piege"])]),
    ("en_s3", "Séance 3 — La courbe d'Aston, la fission, la fusion", [
        ("en_s2_b2", "La courbe d'Aston", ["en_a1_courbe", "en_a2_zones", "en_a2b_fission", "en_a3_comparer"]),
        ("en_s2_b3", "Spontanée ou provoquée, la fission, la réaction en chaîne", ["en_r1_spontanee", "en_r2_fission", "en_r3_chaine"]),
        ("en_s2_b4", "Deux charges positives, la fusion, l'équation", ["en_p3_charges", "en_r4_fusion", "en_r5_soddy"])]),
    ("en_s4", "Séance 4 — L'énergie libérée : par les masses, par les énergies de liaison", [
        ("en_s3_b1", "La masse diminue : Δm, ΔE, E_lib", ["en_b1_masse_diminue", "en_b2_methode", "en_b2b_energie"]),
        ("en_s3_b2", "Calculer l'énergie libérée avec les masses (exercices du national joués)", ["en_b4_fission_calcul", "en_b3_fusion_calcul", "en_b5_beta"]),
        ("en_s3_b3", "Les énergies de liaison et le diagramme (exercices du national joués)", ["en_e1_diagramme", "en_e2_formule", "en_e3_2023", "en_e4_polonium"])]),
    ("en_s5", "Séance 5 — L'échantillon, les dangers, les cas types et le bilan", [
        ("en_s4_b1", "D'un noyau à un échantillon", ["en_n1_echantillon", "en_n1b_energie_totale", "en_n2_comparaison", "en_n3_2025"]),
        ("en_s4_b2", "Applications, dangers et cas types du national", ["en_r3b_applications_dangers", "en_c1_cas_types", "en_c2_qcm2019"]),
        ("en_s4_b3", "Bilan du chapitre", ["en_z1_bilan", "en_z2_carte"])]),
]

# ── Textes réécrits : la voix pose les données et la méthode, l'élève calcule ──────────────────────────────────────
L3_TEXTE = ("يلا نحسبو l'énergie de liaison ديال l'hélium quatre. la relation: E l égale delta m fois c au carré. "
            "لقينا delta m égale zéro virgule zéro trois mille trente-huit u. إذن E l égale zéro virgule zéro trois "
            "mille trente-huit u fois c au carré. كنبدلو u ب neuf cent trente et un virgule cinq méga électron volt "
            "sur c au carré، و c au carré كيتحيدو. بقات غير الضربة: zéro virgule zéro trois mille trente-huit، fois "
            "neuf cent trente et un virgule cinq. دابا نتا: دير الضربة، وعطي E l ب méga électron volt.")
S2_TEXTE = ("هادا فخ، بزاف ديال التلاميذ كيغلطو فيه. l'uranium deux cent trente-cinq عندو l'énergie de liaison كبيرة "
            "بزاف: mille sept cent quatre-vingt-trois méga électron volt. le fer cinquante-six: غير quatre cent "
            "quatre-vingt-douze. ولكن l'uranium فيه deux cent trente-cinq nucléons، و le fer غير cinquante-six. "
            "تفكر la règle: la stabilité ماشي ف E l. قسم كل وحدة على A ديالها، وقارن بوحدك.")
A3_TEXTE = ("واحد vrai ou faux من le national ديال deux mille vingt-trois. le deutérium، يعني l'hydrogène deux، E l "
            "égale deux virgule trois cent soixante-six méga électron volt. le tritium، يعني l'hydrogène trois، huit "
            "virgule quatre cent soixante-quinze. باش نقارنو la stabilité، ماشي E l: خاصنا E l sur A. قسم كل وحدة "
            "على A ديالها، وقارن بوحدك: واش le tritium، stable كثر من le deutérium؟")
B3_TEXTE = ("national حقيقي، la session normale ديال deux mille seize. كنقراو التمرين: la fusion ديال le deutérium "
            "و le tritium، كتعطي l'hélium و neutron، و les masses فالتمرين ب u. le deutérium: deux virgule zéro un "
            "trois cent cinquante-cinq. le tritium: trois virgule zéro un cinq cent cinquante. l'hélium: quatre virgule "
            "zéro zéro cent cinquante. le neutron: un virgule zéro zéro huit cent soixante-six. السؤال: حسب l'énergie "
            "libérée. كنطبقو الطريقة، خطوة من بعد خطوة، ونتا اللي غادي تدير كل خطوة: delta m، من بعد delta E، "
            "وفاللخر E libérée.")
B5_TEXTE = ("نفس الطريقة كتخدم حتى ل la radioactivité. national ديال deux mille dix-sept، le rattrapage: le cobalt "
            "soixante كيعطي le nickel soixante و électron. كنقراو المعطيات: la masse ديال le cobalt، و le nickel، و "
            "l'électron. رد البال: l'électron عندو la masse، zéro virgule zéro zéro zéro cinquante-cinq u، وهو من "
            "les produits: كيدخل ف delta m. دابا نتا: حسب l'énergie libérée، بنفس الخطوات.")
E3_FIN = "دابا نتا، خطوة من بعد خطوة: الأول delta E، من بعد l'énergie libérée."
E4_TEXTE = ("هادا le diagramme ديال le national ديال deux mille vingt. فيه trois niveaux، كل واحد بالطاقة ديالو. "
            "الفوق: les nucléons بعاد. فالوسط: le polonium deux cent dix. التحت: le plomb و l'hélium. la flèche ديما "
            "هي الوصول ناقص الانطلاق. رد البال ما تنساش dix puissance cinq، وخود جميع الأرقام. دابا نتا: من le "
            "polonium ل les produits، شحال هي l'énergie libérée؟")
C2_FIN = "لكل noyau. من بعد la somme ديال les réactifs ناقص la somme ديال les produits. دابا نتا: الخطوة اللولى، E l ديال le radon."

B3_STEPS = {
    "question": {
        "type": "qcm", "prompt": "Étape 1 — Calcule Δm = Σm(produits) − Σm(réactifs).",
        "options": ["Δm = −0,01889 u", "Δm = +0,01889 u", "Δm = −1,02755 u"], "timeout_seconds": 30, "correct": 0,
        "enonce_dit": "الخطوة اللولى: calcule delta m، la somme des masses des produits moins la somme des masses des réactifs.",
        "demonstration": demo([
            ("Σm(produits) = 4,00150 + 1,00866 = 5,01016 u", "les produits"),
            ("Σm(réactifs) = 2,01355 + 3,01550 = 5,02905 u", "les réactifs"),
            ("Δm = 5,01016 − 5,02905", "delta m égale"),
            ("Δm = −0,01889 u", "le résultat")],
            "les produits: quatre virgule zéro zéro cent cinquante plus un virgule zéro zéro huit cent soixante-six، "
            "يعني cinq virgule zéro un mille seize u. les réactifs: deux virgule zéro un trois cent cinquante-cinq plus "
            "trois virgule zéro un cinq cent cinquante، يعني cinq virgule zéro deux mille neuf cent cinq u. delta m "
            "égale les produits moins les réactifs. le résultat: moins zéro virgule zéro un mille huit cent "
            "quatre-vingt-neuf u.")},
    "exercises": [
        {"type": "qcm", "prompt": "Étape 2 — Calcule ΔE = Δm·c² en MeV (1 u = 931,5 MeV/c²).",
         "choices": ["ΔE ≈ −17,6 MeV", "ΔE ≈ −0,01889 MeV", "ΔE ≈ −1,70·10¹⁵ J"], "correct": 0,
         "explanation": "ΔE = Δm·c² = −0,01889 u·c² = −0,01889 × 931,5 MeV ≈ −17,6 MeV.",
         "enonce_dit": "الخطوة التانية: calcule delta E égale delta m fois c au carré، ب méga électron volt.",
         "demonstration": demo([
             ("ΔE = Δm·c² = −0,01889 u·c²", "la relation"),
             ("1 u·c² = 931,5 MeV", "كنبدلو u"),
             ("ΔE = −0,01889 × 931,5 MeV", "l'application numérique"),
             ("ΔE ≈ −17,6 MeV", "le résultat")],
             "la relation: delta E égale delta m fois c au carré، moins zéro virgule zéro un mille huit cent "
             "quatre-vingt-neuf u fois c au carré. كنبدلو u fois c au carré ب neuf cent trente et un virgule cinq "
             "méga électron volt. l'application numérique: moins zéro virgule zéro un mille huit cent quatre-vingt-neuf، "
             "fois neuf cent trente et un virgule cinq. le résultat: delta E تقريبا moins dix-sept virgule six méga "
             "électron volt.")},
        {"type": "qcm", "prompt": "Étape 3 — Quelle est l'énergie libérée E_lib par cette fusion ?",
         "choices": ["E_lib = −17,6 MeV", "E_lib = 17,6 MeV", "E_lib = 0 : la masse se conserve"], "correct": 1,
         "explanation": "E_lib = |ΔE| = 17,6 MeV : ΔE < 0, le système cède de l'énergie ; l'énergie libérée est positive.",
         "enonce_dit": "الخطوة التالتة: شحال هي l'énergie libérée par cette fusion ؟",
         "demonstration": demo([
             ("ΔE ≈ −17,6 MeV < 0 : le système cède de l'énergie", "delta E négatif"),
             ("E_lib = |ΔE|", "E libérée égale"),
             ("E_lib ≈ 17,6 MeV", "le résultat")],
             "delta E négatif: le système كيعطي l'énergie للخارج. E libérée égale la valeur absolue de delta E. "
             "le résultat: E libérée تقريبا dix-sept virgule six méga électron volt.")}],
}
B3_REPONSES = {
    "q": {"0": {"juste": r("مزيان! les produits ناقص les réactifs: moins zéro virgule zéro un mille huit cent quatre-vingt-neuf u. la masse نقصات.",
                           "Oui ! Produits moins réactifs : Δm = −0,01889 u. La masse a diminué.")},
          "1": {"1": r("العدد صحيح، ولكن شوف le signe. delta m هو les produits ناقص les réactifs: شكون فيهم كبر؟",
                       "Le nombre est juste, mais regarde le signe. Δm = produits − réactifs : lequel est le plus grand ?"),
                "2": r("لا. les produits، cinq virgule zéro un mille seize، صغار من les réactifs، cinq virgule zéro deux mille neuf cent cinq: delta m سالب، moins zéro virgule zéro un mille huit cent quatre-vingt-neuf u.",
                       "Non. Les produits (5,01016 u) pèsent moins que les réactifs (5,02905 u) : Δm = −0,01889 u, négatif.")},
          "2": {"1": r("بديتي مزيان ب les produits ناقص les réactifs. ولكن نسيتي واحد la particule ف les produits. شوف l'équation مزيان.",
                       "Le sens produits − réactifs est bon. Mais il manque une particule dans les produits : relis l'équation."),
                "2": r("لا. نسيتي le neutron. les produits هوما l'hélium و le neutron: cinq virgule zéro un mille seize u. delta m égale moins zéro virgule zéro un mille huit cent quatre-vingt-neuf u.",
                       "Non. Tu as oublié le neutron : produits = He + n = 5,01016 u, donc Δm = −0,01889 u.")}},
    "e0": {"0": {"juste": r("مزيان! بدلتي u fois c au carré ب neuf cent trente et un virgule cinq: delta E تقريبا moins dix-sept virgule six méga électron volt.",
                            "Oui ! u·c² remplacé par 931,5 MeV : ΔE ≈ −17,6 MeV.")},
           "1": {"1": r("خليتي نفس العدد ديال delta m. ولكن u ماشي méga électron volt: خاصك تضرب ف neuf cent trente et un virgule cinq.",
                        "Tu as gardé le nombre de Δm. Mais u n'est pas une énergie : il faut multiplier par 931,5."),
                 "2": r("لا. delta E égale delta m fois c au carré، و u fois c au carré كتساوي neuf cent trente et un virgule cinq méga électron volt: تقريبا moins dix-sept virgule six.",
                        "Non. ΔE = Δm·c², avec 1 u·c² = 931,5 MeV : ΔE ≈ −0,01889 × 931,5 ≈ −17,6 MeV.")},
           "2": {"1": r("ضربتي ف c au carré، مزيان الفكرة. ولكن delta m ب u، ماشي ب kilogramme. هنا الطريق الساهل: u fois c au carré égale neuf cent trente et un virgule cinq méga électron volt.",
                        "Multiplier par c² est l'idée. Mais Δm est en u, pas en kg : utilise 1 u·c² = 931,5 MeV."),
                 "2": r("لا. ماشي u fois c au carré ب les mètres par seconde. كنبدلو u fois c au carré ب neuf cent trente et un virgule cinq méga électron volt: delta E تقريبا moins dix-sept virgule six.",
                        "Non. On ne multiplie pas des u par c² en m²/s². On remplace u·c² par 931,5 MeV : ΔE ≈ −17,6 MeV.")}},
    "e1": {"0": {"1": r("العدد صحيح. ولكن l'énergie libérée ديما positive: هي la valeur absolue ديال delta E.",
                        "Le nombre est juste. Mais l'énergie libérée est toujours positive : c'est |ΔE|."),
                 "2": r("لا. delta E سالب، و E libérée هي la valeur absolue ديالو: dix-sept virgule six méga électron volt.",
                        "Non. ΔE est négatif ; E_lib = |ΔE| = 17,6 MeV.")},
           "1": {"juste": r("مزيان! E libérée égale la valeur absolue de delta E، dix-sept virgule six méga électron volt.",
                            "Oui ! E_lib = |ΔE| = 17,6 MeV.")},
           "2": {"1": r("فالكيمياء la masse كتبقى هي هي. ولكن هنا réaction nucléaire: شفنا بلي la masse نقصات.",
                        "En chimie la masse se conserve. Mais ici, réaction nucléaire : la balance a montré que la masse diminue."),
                 "2": r("لا. la masse نقصات ب zéro virgule zéro un mille huit cent quatre-vingt-neuf u، وولات énergie: E libérée dix-sept virgule six méga électron volt.",
                        "Non. La masse a diminué de 0,01889 u, devenue énergie : E_lib = 17,6 MeV.")}},
}

E3_STEPS = {
    "question": {
        "type": "qcm", "prompt": "Étape 1 — Calcule ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits).",
        "options": ["ΔE ≈ −17,46 MeV", "ΔE ≈ +17,46 MeV", "ΔE ≈ 39,14 MeV"], "timeout_seconds": 30, "correct": 0,
        "enonce_dit": "الخطوة اللولى: calcule delta E، la somme des E l des réactifs moins la somme des E l des produits.",
        "demonstration": demo([
            ("ΔE = [E_ℓ(²H) + E_ℓ(³H)] − [E_ℓ(⁴He) + E_ℓ(n)]", "la relation"),
            ("ΔE = (2,366 + 8,475) − (28,296 + 0)", "l'application numérique"),
            ("ΔE = 10,841 − 28,296", "يعني dix virgule"),
            ("ΔE ≈ −17,46 MeV", "le résultat")],
            "la relation: delta E égale la somme des E l des réactifs moins la somme des E l des produits. "
            "l'application numérique: deux virgule trois cent soixante-six plus huit virgule quatre cent soixante-quinze، "
            "moins، vingt-huit virgule deux cent quatre-vingt-seize plus zéro. يعني dix virgule huit cent quarante et un، "
            "moins vingt-huit virgule deux cent quatre-vingt-seize. le résultat: delta E تقريبا moins dix-sept virgule "
            "quarante-six méga électron volt.")},
    "exercises": [
        {"type": "qcm",
         "prompt": "Étape 2 — L'énergie libérée, comparée au calcul par les masses (17,6 MeV, national 2016 N) :",
         "choices": ["E_lib ≈ 17,5 MeV : presque le même résultat", "E_lib ≈ −17,5 MeV : l'inverse du calcul par les masses",
                     "E_lib ≈ 39,1 MeV : deux fois plus"], "correct": 0,
         "explanation": "E_lib = |ΔE| ≈ 17,5 MeV : la même fusion donne presque la même énergie par les deux méthodes ; le petit écart vient des données des deux énoncés.",
         "enonce_dit": "الخطوة التانية: l'énergie libérée، كيفاش كتجي مع le calcul par les masses، dix-sept virgule six méga électron volt ؟",
         "demonstration": demo([
             ("E_lib = |ΔE| ≈ 17,5 MeV", "E libérée égale"),
             ("Par les masses (2016 N) : 17,6 MeV", "ب les masses"),
             ("Deux méthodes, presque la même énergie", "جوج طرق")],
             "E libérée égale la valeur absolue de delta E، تقريبا dix-sept virgule cinq méga électron volt. ب les "
             "masses، فالتمرين ديال deux mille seize، لقينا dix-sept virgule six. جوج طرق، ونفس l'énergie تقريبا: "
             "الفرق الصغير جا من les valeurs ديال جوج التمارين.")}],
}
E3_REPONSES = {
    "q": {"0": {"juste": r("مزيان! dix virgule huit cent quarante et un moins vingt-huit virgule deux cent quatre-vingt-seize: delta E تقريبا moins dix-sept virgule quarante-six.",
                           "Oui ! 10,841 − 28,296 : ΔE ≈ −17,46 MeV.")},
          "1": {"1": r("العدد صحيح، ولكن قلبتي الترتيب. مع les énergies de liaison، les réactifs هوما اللولين.",
                       "Le nombre est juste, mais l'ordre est inversé : avec les énergies de liaison, ce sont les réactifs d'abord."),
                "2": r("لا. delta E égale les E l des réactifs moins les E l des produits: dix virgule huit cent quarante et un moins vingt-huit virgule deux cent quatre-vingt-seize، تقريبا moins dix-sept virgule quarante-six.",
                       "Non. ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits) = 10,841 − 28,296 ≈ −17,46 MeV.")},
          "2": {"1": r("جمعتي كلشي. ولكن la relation فيها ناقص: les réactifs ناقص les produits.",
                       "Tu as tout additionné. La relation a un signe moins : réactifs − produits."),
                "2": r("لا. ماشي المجموع: delta E égale dix virgule huit cent quarante et un moins vingt-huit virgule deux cent quatre-vingt-seize، تقريبا moins dix-sept virgule quarante-six.",
                       "Non. Ce n'est pas la somme : ΔE = 10,841 − 28,296 ≈ −17,46 MeV.")}},
    "e0": {"0": {"juste": r("مزيان! E libérée تقريبا dix-sept virgule cinq، وب les masses dix-sept virgule six: جوج طرق، ونفس l'énergie تقريبا.",
                            "Oui ! 17,5 MeV ici, 17,6 MeV par les masses : deux méthodes, presque la même énergie.")},
           "1": {"1": r("delta E سالب، صحيح. ولكن l'énergie libérée ديما positive: هي la valeur absolue.",
                        "ΔE est bien négatif. Mais l'énergie libérée est toujours positive : c'est |ΔE|."),
                 "2": r("لا. E libérée égale la valeur absolue de delta E، dix-sept virgule cinq، تقريبا بحال dix-sept virgule six ديال les masses.",
                        "Non. E_lib = |ΔE| ≈ 17,5 MeV, presque les 17,6 MeV trouvés par les masses.")},
           "2": {"1": r("هاد العدد هو المجموع ديال كلشي. رجع ل delta E اللي لقيتي فالخطوة اللولى.",
                        "Ce nombre est la somme de tout. Reprends le ΔE de l'étape 1."),
                 "2": r("لا. E libérée هي la valeur absolue ديال delta E: تقريبا dix-sept virgule cinq méga électron volt.",
                        "Non. E_lib = |ΔE| ≈ 17,5 MeV.")}},
}

C2_ETAPE1 = {
    "type": "qcm",
    "prompt": "Étape 1 — E_ℓ = A·(E_ℓ/A). L'énergie de liaison du radon ²²²Rn (E_ℓ/A = 7,69 MeV/nucléon) vaut :",
    "options": ["7,69 MeV", "1707,18 MeV", "0,0346 MeV"], "timeout_seconds": 30, "correct": 1,
    "enonce_dit": "الخطوة اللولى: E l égale A fois E l sur A. l'énergie de liaison du radon deux cent vingt-deux، E l sur A égale sept virgule soixante-neuf، شحال كتساوي ؟",
    "demonstration": demo([
        ("E_ℓ = A·(E_ℓ/A)", "la relation"),
        ("E_ℓ(²²²Rn) = 222 × 7,69", "l'application numérique"),
        ("E_ℓ(²²²Rn) = 1707,18 MeV", "le résultat")],
        "la relation: E l égale A fois E l sur A. l'application numérique: deux cent vingt-deux fois sept virgule "
        "soixante-neuf. le résultat: mille sept cent sept virgule dix-huit méga électron volt.")}
C2_REP_ETAPE1 = {
    "0": {"1": r("هادي E l sur A، ماشي E l. la relation: E l égale A fois E l sur A.",
                 "Ça, c'est E_ℓ/A, pas E_ℓ. La relation : E_ℓ = A·(E_ℓ/A)."),
          "2": r("لا. خاصك تضرب ف A: deux cent vingt-deux fois sept virgule soixante-neuf، mille sept cent sept virgule dix-huit méga électron volt.",
                 "Non. Il faut multiplier par A : 222 × 7,69 = 1707,18 MeV.")},
    "1": {"juste": r("مزيان! deux cent vingt-deux fois sept virgule soixante-neuf: mille sept cent sept virgule dix-huit méga électron volt.",
                     "Oui ! 222 × 7,69 = 1707,18 MeV.")},
    "2": {"1": r("قسمتي على A. ولكن E l sur A مكتوبة فالتمرين: باش نرجعو ل E l، كنضربو ف A.",
                 "Tu as divisé par A. E_ℓ/A est donnée : pour revenir à E_ℓ, on multiplie par A."),
          "2": r("لا. E l égale A fois E l sur A: deux cent vingt-deux fois sept virgule soixante-neuf، mille sept cent sept virgule dix-huit.",
                 "Non. E_ℓ = A·(E_ℓ/A) = 222 × 7,69 = 1707,18 MeV.")},
}

REACTIONS_EN_MOTS = {
    ("en_m4_931", "e0", "0", "1"): ("1,77·10²⁰", "un virgule soixante-dix-sept fois dix puissance vingt"),
    ("en_b5_beta", "e0", "1", "2"): ("0,97", "zéro virgule quatre-vingt-dix-sept"),
}
RAPPELS_EN_MOTS = {
    ("C8_r2", "1", "1"): [("185 MeV", "cent quatre-vingt-cinq MeV")],
    ("C4_r4", "0", "1"): [("⁵⁶Ni", "le nickel cinquante-six"), ("⁶⁰Ni", "le nickel soixante")],
}


def reecrire(s, mixed, fr=None, lead=None, pointage=None, centre=None, demarrer="reset"):
    s["speech_text"]["mixed"] = mixed
    if fr is not None:
        s["speech_text"]["fr"] = fr
    if lead is not None:
        s["screen_content"]["lead"] = lead
    co = s["concentration"]
    if pointage is not None:
        co["pointage"] = pointage
    if centre is not None:
        co["centre"] = centre
    if demarrer:
        co["demarrer"] = demarrer
    for p in co.get("pointage") or []:
        assert mixed.count(p["mot"]) == 1, (s["id"], p["mot"])
    for p in co.get("centre") or []:
        assert mixed.count(p["mot"]) == 1, (s["id"], p["mot"])
    s.pop("audio", None)


def garder(co, cle, mots):
    return [p for p in co.get(cle) or [] if p["mot"] in mots]


def main():
    m = json.load(open(SRC, encoding="utf-8"))
    S = {s["id"]: s for a in m["activities"] for s in a["slides"]}
    vieux_blocs = [b for se in m["seances"] for b in se["blocs"]]

    s = S["en_l3_calcul"]
    reecrire(s, L3_TEXTE,
             fr="Calculons l'énergie de liaison de l'hélium 4. E_ℓ = Δm·c², avec Δm = 0,03038 u. On remplace u par 931,5 MeV/c², les c² se simplifient. Il reste la multiplication : à toi de la faire, en MeV.",
             lead="⁴₂He : E_ℓ = Δm·c², avec 1 u = 931,5 MeV/c².",
             pointage=garder(s["concentration"], "pointage", ["la relation: E l"]),
             centre=[p for p in s["concentration"]["centre"][:4]])
    s["screen_content"]["bullets"] = ["E_ℓ = Δm·c² avec Δm = 0,03038 u : E_ℓ = 0,03038 u·c².",
                                      "On remplace 1 u par 931,5 MeV/c², les c² se simplifient : E_ℓ = 0,03038 × 931,5 MeV.",
                                      "À toi : le résultat en MeV."]

    s = S["en_s2_piege"]
    reecrire(s, S2_TEXTE,
             fr="Voici le piège le plus fréquent. L'uranium 235 a une énergie de liaison énorme : 1783 MeV. Le fer 56 : seulement 492 MeV. Mais l'uranium a 235 nucléons, le fer 56. La stabilité ne se lit pas sur E_ℓ : divise chacune par A et compare toi-même.",
             lead="²³⁵U a une énorme E_ℓ. Est-il pour autant le plus stable ?",
             pointage=[{"mot": "هادا فخ،", "commande": "play_until", "parametres": {"moment": "courbe_tracee"}}])
    s["screen_content"]["bullets"] = ["E_ℓ(²³⁵U) = 1783,5 MeV ; E_ℓ(⁵⁶Fe) = 492,2 MeV.",
                                      "La stabilité se compare avec E_ℓ/A, jamais avec E_ℓ seule.",
                                      "À toi : E_ℓ/A de chacun, puis la comparaison."]

    s = S["en_a3_comparer"]
    reecrire(s, A3_TEXTE,
             fr="Un vrai-faux du national 2023. Deutérium : E_ℓ = 2,366 MeV. Tritium : E_ℓ = 8,475 MeV. Pour comparer la stabilité, il faut E_ℓ/A : divise chacune par son A et compare toi-même. Le tritium est-il plus stable que le deutérium ?",
             lead="²H ou ³H : lequel est le plus stable ?",
             pointage=[{"mot": "واحد vrai ou faux", "commande": "play_until", "parametres": {"moment": "courbe_tracee"}}])
    s["screen_content"]["bullets"] = ["E_ℓ(²H) = 2,366 MeV ; E_ℓ(³H) = 8,475 MeV.",
                                      "Comparer E_ℓ/A : diviser chaque E_ℓ par son nombre de nucléons A.",
                                      "À toi : E_ℓ/A de chacun, puis la comparaison."]

    s = S["en_b3_fusion_calcul"]
    reecrire(s, B3_TEXTE,
             fr="National 2016, session normale : la fusion du deutérium et du tritium donne l'hélium et un neutron ; les masses en u. On calcule l'énergie libérée étape par étape, et c'est toi qui fais chaque étape : Δm, puis ΔE, puis E_lib.",
             lead="Δm, puis ΔE, puis E_lib : à toi, étape par étape.",
             pointage=[{"mot": "كنقراو التمرين:", "commande": "play_until", "parametres": {"moment": "trace"}},
                       {"mot": "و les masses فالتمرين", "commande": "play_until", "parametres": {"moment": "donnees"}}],
             centre=[{"texte": "Δm = Σm(produits) − Σm(réactifs)", "mot": "delta m، من بعد delta E"}])
    s["title"] = "Énergie libérée par la fusion, étape par étape (national 2016 N)"
    s["screen_content"]["bullets"] = [s["screen_content"]["bullets"][0],
                                      "Étape 1 : Δm = Σm(produits) − Σm(réactifs).",
                                      "Étape 2 : ΔE = Δm·c² (1 u·c² = 931,5 MeV).", "Étape 3 : E_lib = |ΔE|."]
    s["question"] = B3_STEPS["question"]
    s["exercises"] = B3_STEPS["exercises"]
    s["concentration"]["reponses"] = B3_REPONSES

    s = S["en_b5_beta"]
    reecrire(s, B5_TEXTE,
             fr="La même méthode marche pour la radioactivité. National 2017, rattrapage : le cobalt 60 donne le nickel 60 et un électron. Attention : l'électron a une masse, 0,00055 u, et il fait partie des produits : il entre dans Δm. À toi de calculer l'énergie libérée, avec les mêmes étapes.",
             pointage=[{"mot": "national ديال deux mille dix-sept،", "commande": "play_until", "parametres": {"moment": "trace"}},
                       {"mot": "كنقراو المعطيات", "commande": "play_until", "parametres": {"moment": "donnees"}}])
    s["screen_content"]["bullets"] = [s["screen_content"]["bullets"][0],
                                      "Δm = m(Ni) + m(e) − m(Co) : l'électron est un produit.",
                                      "Puis ΔE = Δm·c² et E_lib = |ΔE|.", "⚠ Sans l'électron, le résultat est faux."]

    s = S["en_e3_2023"]
    t = s["speech_text"]["mixed"]
    i = t.index("l'application numérique:")
    reecrire(s, t[:i] + E3_FIN,
             fr="National 2023, session normale : un tableau d'énergies de liaison (deutérium 2,366 MeV ; tritium 8,475 MeV ; hélium 28,296 MeV ; neutron 0). ΔE = somme des E_ℓ des réactifs moins somme des E_ℓ des produits. À toi, étape par étape : d'abord ΔE, puis l'énergie libérée.",
             pointage=garder(s["concentration"], "pointage", ["national ديال deux mille vingt-trois،", "كنقراو le tableau:"]),
             centre=s["concentration"]["centre"][:1])
    s["title"] = "Énergie libérée par les énergies de liaison, étape par étape (national 2023 N)"
    s["screen_content"]["bullets"] = [s["screen_content"]["bullets"][0], s["screen_content"]["bullets"][1].split(" = (")[0],
                                      "Étape 1 : ΔE ; étape 2 : E_lib = |ΔE|, comparée au calcul par les masses."]
    s["question"] = E3_STEPS["question"]
    s["exercises"] = E3_STEPS["exercises"]
    s["concentration"]["reponses"] = E3_REPONSES

    s = S["en_e4_polonium"]
    reecrire(s, E4_TEXTE,
             fr="Le diagramme du national 2020 : trois paliers avec leurs énergies. En haut, les nucléons séparés ; au milieu, le polonium 210 ; en bas, le plomb et l'hélium. Une flèche, c'est toujours arrivée moins départ. N'oublie pas le facteur dix puissance cinq et garde tous les chiffres. À toi : du polonium aux produits, quelle est l'énergie libérée ?",
             pointage=garder(s["concentration"], "pointage", ["هادا le diagramme", "الفوق: les nucléons", "فالوسط: le polonium", "التحت: le plomb"]))
    s["screen_content"]["bullets"] = [s["screen_content"]["bullets"][0], "Une flèche : énergie d'arrivée − énergie de départ.",
                                      "⚠ Garder le facteur 10⁵ et tous les chiffres."]

    s = S["en_c2_qcm2019"]
    t = s["speech_text"]["mixed"]
    i = t.index("ل le radon:")
    reecrire(s, t[:i] + C2_FIN, pointage=garder(s["concentration"], "pointage", ["التمرين كيعطي E l sur A.", "خاصك اللول تضرب ف A:"]))
    ancienne = s.pop("question")
    ex = {k: v for k, v in ancienne.items() if k not in ("options", "timeout_seconds")}
    ex["choices"] = ancienne["options"]
    ex["prompt"] = "Étape 2 — " + ancienne["prompt"]
    ex["explanation"] = "ΔE = E_ℓ(Rn) − [E_ℓ(Po) + E_ℓ(He)] = 1707,18 − (1685,14 + 28,28) = −6,24 MeV ; E_lib = 6,24 MeV."
    s["question"] = C2_ETAPE1
    s["exercises"] = [ex] + (s.get("exercises") or [])
    rep = s["concentration"]["reponses"]
    rep["e0"] = rep.pop("q")
    rep["q"] = C2_REP_ETAPE1

    for (sid, cle, opt, quoi), (a, b) in REACTIONS_EN_MOTS.items():
        rr = S[sid]["concentration"]["reponses"][cle][opt][quoi]
        assert a in rr["parole"], (sid, a)
        rr["parole"] = rr["parole"].replace(a, b); rr.pop("audio", None)
    rappels = {x["id"]: x for c_ in m["competences"] for x in c_.get("rappels", [])}
    for (rid, opt, quoi), reps in RAPPELS_EN_MOTS.items():
        rr = rappels[rid]["reponses"][opt][quoi]
        for a, b in reps:
            assert a in rr["parole"], (rid, a)
            rr["parole"] = rr["parole"].replace(a, b)
        rr.pop("audio", None)

    ordre = [i for p in PARTIES for i in p[4]]
    assert sorted(ordre) == sorted(S), set(S) ^ set(ordre)
    m["activities"] = [{"id": pid, "title": t_, "phase": ph, "duration_minutes": d, "slides": [S[i] for i in ids]}
                       for pid, t_, ph, d, ids in PARTIES]
    assert [i for _, _, bl in SEANCES for _, _, ids in bl for i in ids] == ordre
    vieux_par_id = {b["id"]: b for b in vieux_blocs}
    seances = []
    for sid, titre, bl in SEANCES:
        blocs = []
        for bid, bt, ids in bl:
            vieux = vieux_par_id.get(bid) or max(vieux_blocs, key=lambda b: len(set(b["slide_ids"]) & set(ids)))
            b = copy.deepcopy(vieux)
            b.update({"id": bid, "titre": bt, "slide_ids": ids})
            if set(ids) != set(vieux["slide_ids"]):          # cahier refait sur les diapositives du bloc
                b["cahier"] = [{"texte": S[i]["concentration"]["cahier"]} for i in ids if S[i]["concentration"].get("cahier")]
                figs = [f for i in ids for f in (S[i]["concentration"].get("cahier_figures") or [])][:2]
                if figs:
                    b["cahier_figures"] = figs
                else:
                    b.pop("cahier_figures", None)
            blocs.append(b)
        seances.append({"id": sid, "titre": titre, "blocs": blocs})
    m["seances"] = seances
    for c_ in m["competences"]:
        c_["slide_ids"] = [i for i in ordre if c_["id"] in (S[i].get("competence_ids") or [])]
    m["estimated_minutes"] = sum(p[3] for p in PARTIES)
    m["note"] = (m.get("note", "") + " Logique refaite le 18 novembre 2026 (skill logique-de-cours) : "
                 "backend/data/curriculum/architecture/phys_ch5_energie_nucleaire.md.").strip()
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    json.dump(m, open(DST, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(DST, "a", encoding="utf-8").write("\n")


if __name__ == "__main__":
    main()
    print("écrit :", DST)
