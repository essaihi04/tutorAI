# Exercice de physique, ch. 5 (noyaux, masse et énergie), niveau facile n° 1 : défaut de masse, énergie de liaison et
# énergie de liaison par nucléon du carbone 12 (trois gestes, un par question).
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/energie_nucleaire.json : cas_types « énergie de liaison (et par
#    nucléon) à partir des masses » (4/20), pièges « N = A au lieu de A − Z », « Δm en u multiplié par 9·10¹⁶ » ;
#    valeurs_reperes (m_p = 1,00728 u, m_n = 1,00866 u, 1 u = 931,5 MeV/c², ¹²C : 7,68 MeV/nucléon).
#  - nationaux (exam.json) : 2016 R (E_ℓ/A du ²⁴Mg), 2017 R (E_ℓ/A du ⁶⁰Ni), 2020 R (E_ℓ de ²³⁴U), 2022 R (E_ℓ du ¹⁴C) :
#    « Calculer, en MeV, l'énergie de liaison… » ; ici les gestes un à un (niveau facile).
#  - séries en ligne : recherche faite (talamidi, moutamadris, alloschool : séries « noyaux, masse et énergie », défaut
#    de masse puis E_ℓ en MeV puis E_ℓ/A, hélium, carbone, oxygène) ; les pages elles-mêmes n'étaient pas joignables
#    depuis cette session (réseau), seuls les extraits de recherche ont été lus.
#  - cours phys_ch5_energie_nucleaire, diapositives en_d2_balance, en_d3_formule, en_l4_par_nucleon : la balance
#    balance.html?vue=noyau&noyau=carbone12 montre exactement nos valeurs (12,09564 u ; 11,99671 u ; 0,09893 u ;
#    92,15 MeV ; 7,68 MeV/nucléon).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch5_nucleaire_1"
SIMD = "/media/simulations/physics/energie-nucleaire-tableau/"
MP, MN, U = 1.00728, 1.00866, 931.5


def niveaux(titre, bas, haut):
    """Deux niveaux : le noyau au repos (bas), ses nucléons séparés au repos (haut) ; la flèche E_ℓ monte."""
    return schema(titre, 8, 4.2,
        [{"f": "ligne", "pts": [[0.4, 3.3], [3.8, 3.3]], "couleur": "cyan", "epais": True}],
        texte([4.0, 3.3], haut, "cyan", "gauche"),
        [{"f": "ligne", "pts": [[0.4, 0.9], [3.8, 0.9]], "couleur": "jaune", "epais": True}],
        texte([4.0, 0.9], bas, "jaune", "gauche"),
        [{"f": "fleche", "de": [2.1, 1.0], "a": [2.1, 3.2], "couleur": "orange"}],
        texte([2.3, 2.1], "E_{ℓ} = ?", "orange", "gauche"),
        texte([1.1, 2.1], "on fournit", "faible", "centre"),
        legende="Pour séparer le noyau au repos en ses nucléons au repos, il faut fournir l'énergie de liaison E_ℓ.")


# ---------------------------------------------------------------- calculs (énoncé : carbone 12)
Z, A, M = 6, 12, 11.99671
SOM = Z * MP + (A - Z) * MN            # 12,09564 u
DM = SOM - M                           # 0,09893 u
EL = DM * U                            # 92,15 MeV
ELA = EL / A                           # 7,68 MeV/nucléon
assert abs(SOM - 12.09564) < 1e-9 and abs(DM - 0.09893) < 1e-9 and round(EL, 2) == 92.15 and round(ELA, 2) == 7.68

# semblable : oxygène 16
Z2, A2, M2 = 8, 16, 15.99052
DM2 = Z2 * MP + (A2 - Z2) * MN - M2    # 0,13700 u
EL2 = DM2 * U                          # 127,6 MeV
ELA2 = EL2 / A2                        # 7,98 MeV/nucléon
assert abs(DM2 - 0.137) < 1e-9 and round(EL2, 1) == 127.6 and round(ELA2, 2) == 7.98

URL = SIMD + "balance.html?vue=noyau&noyau=carbone12"

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "energie_nucleaire", "cours": "phys_ch5_energie_nucleaire",
  "titre": "Le carbone 12 : défaut de masse et énergie de liaison", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer le défaut de masse d'un noyau", "Calculer l'énergie de liaison E_ℓ = Δm·c² en MeV",
                  "Calculer l'énergie de liaison par nucléon E_ℓ/A"],
  "enonce": {
    "intro": "Le carbone 12 est le noyau qui sert à définir l'unité de masse atomique. On s'intéresse à la cohésion du noyau ¹²₆C. La figure représente le noyau au repos et ses nucléons séparés au repos.",
    "intro_dit": "دابا نقراو l'énoncé. le carbone douze هو النواة اللي بيها كنعرفو l'unité de masse atomique. غادي نحسبو le défaut de masse ديالو، و l'énergie de liaison ديالو. la figure كتبين النواة واقفة، و les nucléons ديالها بعاد على بعضياتهم وواقفين.",
    "figures": [niveaux("Figure : le noyau ¹²₆C et ses nucléons séparés", "¹²₆C au repos", "6 ¹₁p + 6 ¹₀n séparés")],
    "donnees": ["m(¹²₆C) = 11,99671 u", "m_p = 1,00728 u ; m_n = 1,00866 u", "1 u = 931,5 MeV/c²"],
    "questions": [
      question("1", "Calculer, en u, le défaut de masse Δm du noyau ¹²₆C.",
        "السؤال un: حسب ب u le défaut de masse، delta m، ديال النواة ديال le carbone douze.",
        valeur("Δm", 0.09893, "u", "Δm = Z·m_p + (A − Z)·m_n − m(¹²₆C) = 6 × 1,00728 + 6 × 1,00866 − 11,99671 = 0,09893 u"),
        ["Δm = Z·m_p + (A − Z)·m_n − m", "Z = 6", "A − Z", "u"], ["Δm = m − Z·m_p − A·m_n", "N = A = 12"],
        [aide("Combien de protons et combien de neutrons dans ¹²₆C ? Z est en bas, A en haut, et N = A − Z.",
              "شحال من proton وشحال من neutron فالنواة؟ Z هو اللي لتحت، و A هو اللي لفوق، و le nombre de neutrons هو A moins Z."),
         aide("Δm = Z·m_p + (A − Z)·m_n − m(noyau) : la masse des nucléons séparés moins la masse du noyau. Δm est toujours positif.",
              "delta m égale Z m p plus A moins Z m n، moins la masse ديال النواة. يعني la masse ديال les nucléons بعاد، ناقص la masse ديال النواة. le défaut de masse ديما positif.")],
        corr([("1 : Δm = Z·m_p + (A − Z)·m_n − m(¹²₆C)", "delta m égale Z m p plus A moins Z m n"),
              ("A.N. : Δm = 6 × 1,00728 + 6 × 1,00866 − 11,99671", "six fois un virgule zéro zéro sept cent vingt-huit"),
              ("Δm = 12,09564 − 11,99671 = 0,09893 u", "zéro virgule zéro neuf mille huit cent quatre-vingt-treize u")],
             "السؤال un. delta m égale Z m p plus A moins Z m n، moins m du noyau. هنا Z égale six، و A moins Z égale six. l'application numérique: six fois un virgule zéro zéro sept cent vingt-huit، plus six fois un virgule zéro zéro huit cent soixante-six، moins onze virgule quatre-vingt-dix-neuf mille six cent soixante et onze. كنلقاو delta m égale zéro virgule zéro neuf mille huit cent quatre-vingt-treize u."),
        "ex_n1_1", "fa_n1_1"),
      question("2", "Calculer, en MeV, l'énergie de liaison E_ℓ du noyau ¹²₆C.",
        "السؤال deux: حسب ب méga électron volt l'énergie de liaison، E l، ديال النواة ديال le carbone douze.",
        valeur("E_ℓ", 92.15, "MeV", "E_ℓ = Δm·c² = 0,09893 × 931,5 = 92,15 MeV"),
        ["E_ℓ = Δm·c²", "1 u = 931,5 MeV/c²", "MeV"], ["E_ℓ = Δm × 9·10¹⁶", "E_ℓ = Δm/931,5"],
        [aide("Tu as Δm en u. Quelle relation relie une masse à une énergie ?",
              "عندك delta m ب u. شنو هي la relation اللي كتربط la masse ب l'énergie؟"),
         aide("E_ℓ = Δm·c². Remplace u par 931,5 MeV/c² : c² se simplifie, il reste Δm (en u) × 931,5 en MeV.",
              "E l égale delta m fois c au carré. بدل u par neuf cent trente et un virgule cinq méga électron volt sur c au carré، و c au carré كيتحيدو. كيبقى delta m fois neuf cent trente et un virgule cinq.")],
        corr([("2 : E_ℓ = Δm·c²", "E l égale delta m fois c au carré"),
              ("A.N. : E_ℓ = 0,09893 u·c² = 0,09893 × 931,5 MeV", "zéro virgule zéro neuf mille huit cent quatre-vingt-treize fois neuf cent trente et un virgule cinq"),
              ("E_ℓ = 92,15 MeV", "quatre-vingt-douze virgule quinze méga électron volt")],
             "السؤال deux. E l égale delta m fois c au carré. كنبدلو u par neuf cent trente et un virgule cinq méga électron volt sur c au carré. إذن E l égale zéro virgule zéro neuf mille huit cent quatre-vingt-treize fois neuf cent trente et un virgule cinq، يعني quatre-vingt-douze virgule quinze méga électron volt."),
        "ex_n1_2", "fa_n1_2"),
      question("3", "Calculer, en MeV/nucléon, l'énergie de liaison par nucléon du noyau ¹²₆C.",
        "السؤال trois: حسب l'énergie de liaison par nucléon ديال le carbone douze، ب méga électron volt par nucléon.",
        valeur("E_ℓ/A", 7.68, "MeV/nucléon", "E_ℓ/A = 92,15/12 = 7,68 MeV/nucléon"),
        ["E_ℓ/A", "A = 12", "MeV/nucléon"], ["E_ℓ/Z", "E_ℓ/(A − Z)"],
        [aide("L'énergie de liaison se partage entre tous les nucléons du noyau. Combien y a-t-il de nucléons dans ¹²₆C ?",
              "l'énergie de liaison كتقسم على جميع les nucléons ديال النواة. شحال من nucléon فيها؟"),
         aide("On divise E_ℓ par A (le nombre de nucléons), pas par Z. Contrôle : E_ℓ/A ne dépasse jamais environ 8,8 MeV/nucléon.",
              "كنقسمو E l على A، ماشي على Z. وباش تحقق: E l sur A عمرها ما كتفوت environ huit virgule huit.")],
        corr([("3 : E_ℓ/A = 92,15/12", "E l sur A égale quatre-vingt-douze virgule quinze sur douze"),
              ("E_ℓ/A = 7,68 MeV/nucléon", "sept virgule soixante-huit méga électron volt par nucléon")],
             "السؤال trois. E l sur A égale quatre-vingt-douze virgule quinze sur douze، يعني sept virgule soixante-huit méga électron volt par nucléon. inférieure à huit virgule huit: معقول."),
        "ex_n1_3", "fa_n1_3"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_n1_1", "Question 1 : le défaut de masse", "Δm = 6 m_p + 6 m_n − m(¹²₆C) = 12,09564 − 11,99671 = 0,09893 u",
      URL, "La balance : à gauche les 12 nucléons séparés, à droite le noyau de carbone 12",
      "شوف الميزان. على اليسار، كنحطو les nucléons ديال le carbone douze بعاد على بعضياتهم: six protons et six neutrons. la masse ديالهم: six fois m p plus six fois m n، يعني douze virgule zéro neuf mille cinq cent soixante-quatre u. على اليمين، كنحطو النواة: onze virgule quatre-vingt-dix-neuf mille six cent soixante et onze u. شوف: الميزان كيهبط من جيهة les nucléons. النواة خف. الفرق هو le défaut de masse: delta m égale zéro virgule zéro neuf mille huit cent quatre-vingt-treize u.",
      centre=[("Δm = Z·m_p + (A − Z)·m_n − m(¹²₆C)", "six fois m p plus six fois m n"),
              ("Δm = 12,09564 − 11,99671 = 0,09893 u", "delta m égale zéro virgule zéro neuf mille")],
      pointage=[{"mot": "كنحطو les nucléons", "commande": "play_until", "parametres": {"moment": "nucleons_poses"}},
                {"mot": "six protons et six neutrons", "repere": "nucleons"},
                {"mot": "كنحطو النواة", "commande": "play_until", "parametres": {"moment": "noyau_pose"}},
                {"mot": "الميزان كيهبط", "commande": "play_until", "parametres": {"moment": "balance_penche"}},
                {"mot": "الفرق هو le défaut de masse", "commande": "play_until", "parametres": {"moment": "delta_m"}}]),
    diapo_sim("ex_n1_2", "Question 2 : l'énergie de liaison", "E_ℓ = Δm·c² = 0,09893 × 931,5 = 92,15 MeV",
      URL, "La colonne des masses : Δm, puis E_ℓ = Δm·c²",
      "شوف la colonne ديال les masses. عندنا delta m égale zéro virgule zéro neuf mille huit cent quatre-vingt-treize u. l'énergie اللي كتقابل هاد la masse هي l'énergie de liaison: E l égale delta m fois c au carré. كنبدلو u par neuf cent trente et un virgule cinq méga électron volt sur c au carré، و c au carré كيتحيدو. الضربة: zéro virgule zéro neuf mille huit cent quatre-vingt-treize fois neuf cent trente et un virgule cinq، يعني quatre-vingt-douze virgule quinze méga électron volt. رد البال: ما تضربش delta m ب u، par neuf fois dix puissance seize.",
      centre=[("E_ℓ = Δm·c²", "E l égale delta m fois c au carré"),
              ("E_ℓ = 0,09893 × 931,5 = 92,15 MeV", "quatre-vingt-douze virgule quinze méga électron volt")],
      pointage=[{"mot": "شوف la colonne", "repere": "colonne_masses"},
                {"mot": "عندنا delta m", "commande": "play_until", "parametres": {"moment": "delta_m"}},
                {"mot": "الضربة:", "commande": "play_until", "parametres": {"moment": "energie"}},
                {"mot": "quatre-vingt-douze virgule quinze méga électron volt", "repere": "energie"}]),
    diapo_sim("ex_n1_3", "Question 3 : l'énergie de liaison par nucléon", "E_ℓ/A = 92,15/12 = 7,68 MeV/nucléon",
      URL, "On divise E_ℓ par A = 12",
      "l'énergie de liaison كتقسم على جميع les nucléons. فle carbone douze، A égale douze nucléons. شوف la colonne: E l égale quatre-vingt-douze virgule quinze. sur douze: sept virgule soixante-huit méga électron volt par nucléon. كنقسمو على A، ماشي على Z. وهاد la valeur، inférieure à huit virgule huit، معقولة.",
      centre=[("E_ℓ/A = 92,15/12 = 7,68 MeV/nucléon", "sept virgule soixante-huit méga électron volt par nucléon")],
      pointage=[{"mot": "شوف la colonne", "commande": "play_until", "parametres": {"moment": "energie"}},
                {"mot": "sur douze: sept", "commande": "play_until", "parametres": {"moment": "par_nucleon"}},
                {"mot": "sept virgule soixante-huit méga électron volt par nucléon", "repere": "par_nucleon"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_n1_1", "Plus facile : la formule du défaut de masse", "نتمرنو بسؤال ساهل. اختار la bonne formule.",
      "Pour un noyau X de nombre de masse A, de nombre de charge Z et de masse m, le défaut de masse s'écrit :",
      ["Δm = m − [Z·m_p + (A − Z)·m_n]", "Δm = Z·m_p + (A − Z)·m_n − m", "Δm = Z·m_p + A·m_n − m"], 1, {
        "1": {"juste": rep("برافو! la masse ديال les nucléons بعاد، ناقص la masse ديال النواة. delta m كيجي positif.", "Juste : nucléons séparés moins noyau ; Δm > 0.")},
        "0": {"1": rep("ما تقلقش. فكر: النواة خف ولا تقل من les nucléons بعاد؟ واش هاد الفرق غادي يجي positif؟ عاود اختار.", "Le noyau est plus léger que ses nucléons : cette différence serait négative. Réessaie."),
              "2": rep("الجواب هو Z m p plus A moins Z m n moins m. حيت النواة خف، le défaut de masse ديما positif.", "Réponse : Δm = Z·m_p + (A − Z)·m_n − m, toujours positif.")},
        "2": {"1": rep("قريب. ولكن شحال من neutron فالنواة؟ واش A ولا A moins Z؟ عاود اختار.", "Combien de neutrons : A ou A − Z ? Réessaie."),
              "2": rep("الجواب هو Z m p plus A moins Z m n moins m. le nombre de neutrons هو A moins Z، ماشي A.", "Réponse : N = A − Z neutrons, donc (A − Z)·m_n.")}},
      "Pour un noyau A Z X de masse m, le défaut de masse s'écrit comment ?"),
    qcm_facile("fa_n1_2", "Plus facile : de Δm à E_ℓ", "سؤال ساهل: من delta m ل E l.",
      "Un noyau a un défaut de masse Δm = 0,1 u. Son énergie de liaison vaut :",
      ["9·10¹⁵ MeV", "0,107 MeV", "93,15 MeV"], 2, {
        "2": {"juste": rep("برافو! zéro virgule un fois neuf cent trente et un virgule cinq يعني quatre-vingt-treize virgule quinze méga électron volt.", "Juste : 0,1 × 931,5 = 93,15 MeV.")},
        "0": {"1": rep("ما تقلقش. delta m راه ب u، ماشي ب kilogramme. واش كنضربو u، fois neuf fois dix puissance seize؟ عاود اختار.", "Δm est en u, pas en kg : on ne multiplie pas par 9·10¹⁶. Réessaie."),
              "2": rep("الجواب هو E l égale quatre-vingt-treize virgule quinze méga électron volt. u كنضربوها fois neuf cent trente et un virgule cinq باش نوصلو ل méga électron volt.", "Réponse : 0,1 × 931,5 = 93,15 MeV (u × 931,5 → MeV).")},
        "1": {"1": rep("قريب، ولكن قسمتي. la valeur de un u كتقابل، neuf cent trente et un virgule cinq méga électron volt: واش نقسمو ولا نضربو؟ عاود اختار.", "1 u ↔ 931,5 MeV : faut-il diviser ou multiplier ? Réessaie."),
              "2": rep("الجواب هو E l égale quatre-vingt-treize virgule quinze. كنضربو fois neuf cent trente et un virgule cinq، ما كنقسموش.", "Réponse : 93,15 MeV ; on multiplie par 931,5.")}},
      "Un noyau a un défaut de masse delta m égale zéro virgule un u. Son énergie de liaison vaut combien ?"),
    vrai_faux_facile("fa_n1_3", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
      "¹²₆C : E_ℓ = 92,15 MeV.",
      [("L'énergie de liaison par nucléon du ¹²₆C est 92,15/12 = 7,68 MeV/nucléon.", True, "On divise E_ℓ par A = 12 nucléons."),
       ("On obtient E_ℓ/A en divisant E_ℓ par Z = 6.", False, "On divise par A, le nombre de nucléons, pas par Z."),
       ("Une valeur E_ℓ/A de 15 MeV/nucléon serait possible.", False, "E_ℓ/A ne dépasse jamais environ 8,8 MeV/nucléon : il faut refaire le calcul.")]),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données : l'oxygène 16",
    "enonce": {
      "intro": "On étudie la cohésion du noyau d'oxygène ¹⁶₈O.",
      "intro_dit": "نفس التمرين، مع النواة ديال l'oxygène seize.",
      "figures": [niveaux("Figure : le noyau ¹⁶₈O et ses nucléons séparés", "¹⁶₈O au repos", "8 ¹₁p + 8 ¹₀n séparés")],
      "donnees": ["m(¹⁶₈O) = 15,99052 u", "m_p = 1,00728 u ; m_n = 1,00866 u", "1 u = 931,5 MeV/c²"],
      "questions": [
        question_semblable("1", "Calculer, en u, le défaut de masse Δm du noyau ¹⁶₈O.",
          valeur("Δm", 0.137, "u", "Δm = 8 × 1,00728 + 8 × 1,00866 − 15,99052 = 0,13700 u"),
          ["Δm = Z·m_p + (A − Z)·m_n − m", "u"], ["N = A = 16"],
          corr([("1 : Δm = Z·m_p + (A − Z)·m_n − m(¹⁶₈O) = 8 × 1,00728 + 8 × 1,00866 − 15,99052", "delta m égale Z m p plus A moins Z m n"),
                ("Δm = 0,13700 u", "zéro virgule cent trente-sept u")],
               "delta m égale Z m p plus A moins Z m n moins m du noyau، يعني huit fois un virgule zéro zéro sept cent vingt-huit، plus huit fois un virgule zéro zéro huit cent soixante-six، moins quinze virgule quatre-vingt-dix-neuf mille cinquante-deux. delta m égale zéro virgule cent trente-sept u.")),
        question_semblable("2", "Calculer, en MeV, l'énergie de liaison E_ℓ du noyau ¹⁶₈O.",
          valeur("E_ℓ", 127.6, "MeV", "E_ℓ = Δm·c² = 0,13700 × 931,5 = 127,6 MeV"), ["E_ℓ = Δm·c²", "MeV"], ["E_ℓ = Δm × 9·10¹⁶"],
          corr([("2 : E_ℓ = Δm·c² = 0,13700 × 931,5", "E l égale delta m fois c au carré"), ("E_ℓ = 127,6 MeV", "cent vingt-sept virgule six méga électron volt")],
               "E l égale delta m fois c au carré، يعني zéro virgule cent trente-sept fois neuf cent trente et un virgule cinq، يعني cent vingt-sept virgule six méga électron volt.")),
        question_semblable("3", "Calculer, en MeV/nucléon, l'énergie de liaison par nucléon du noyau ¹⁶₈O.",
          valeur("E_ℓ/A", 7.98, "MeV/nucléon", "E_ℓ/A = 127,6/16 = 7,98 MeV/nucléon"), ["E_ℓ/A", "MeV/nucléon"], ["E_ℓ/Z"],
          corr([("3 : E_ℓ/A = 127,6/16", "E l sur A égale cent vingt-sept virgule six sur seize"), ("E_ℓ/A = 7,98 MeV/nucléon", "sept virgule quatre-vingt-dix-huit")],
               "E l sur A égale cent vingt-sept virgule six sur seize، يعني sept virgule quatre-vingt-dix-huit méga électron volt par nucléon.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
