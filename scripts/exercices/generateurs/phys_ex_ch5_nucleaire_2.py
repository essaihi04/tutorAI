# Exercice de physique, ch. 5 (noyaux, masse et énergie), niveau facile n° 2 : les unités du noyau — u → kg,
# E = m·c² en joule, J → MeV — sur le défaut de masse du deutérium (trois gestes, un par question).
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration energie_nucleaire.json : cas_types « défaut de masse en kg » (national 2020 N : Δm par E_ℓ/931,5 puis
#    × 1,66·10⁻²⁷), pièges « Δm en u multiplié par 9·10¹⁶ », « 1 MeV = 1,6·10⁻¹⁹ J » ; insistance « 1 MeV = 1,6·10⁻¹³ J
#    tombe dans les exercices » (TOP PC) ; meilleure explication « deux lignes : u × 931,5 → MeV ; kg × c² → J » (Noureddine,
#    Ridouan : deux routes qui donnent le même résultat).
#  - nationaux : 2016 R (E_ℓ/A « en J/nucléon »), 2020 N (Δm en kg) : conversions demandées dans l'unité imposée.
#  - séries en ligne (talamidi, moutamadris, alloschool : « énergie de liaison en joule puis en MeV ») : recherche faite,
#    pages non joignables depuis cette session (réseau), seuls les extraits ont été lus.
#  - cours : figures.html?fig=fig_unites (1 u = 1,66·10⁻²⁷ kg ; 1 MeV = 1,6·10⁻¹³ J), fig_einstein (E = m·c², c = 3,00·10⁸
#    m/s), liaison.html?noyau=deuterium (E_ℓ(²H) = 2,23 MeV) : nos valeurs sont celles que ces simulations montrent.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch5_nucleaire_2"
SIMD = "/media/simulations/physics/energie-nucleaire-tableau/"
KG, C, MEV = 1.66e-27, 3.00e8, 1.6e-13


def separation(titre, noyau, nucleons):
    """Le noyau (amas de sphères) à gauche ; ses nucléons séparés à droite ; la flèche « on fournit E_ℓ »."""
    els = []
    def boule(x, y, k):
        els.append({"f": "cercle", "c": [x, y], "r": 0.32, "couleur": "rose" if k == "p" else "bleu", "remplir": "rose" if k == "p" else "bleu"})
        els.append({"f": "texte", "at": [x, y - 0.12], "t": k, "ancre": "centre"})
    for i, k in enumerate(nucleons):
        boule(1.2 + 0.5 * i, 1.6 + (0.25 if i % 2 else 0), k)
    for i, k in enumerate(nucleons):
        boule(5.6 + 1.0 * i, 1.6, k)
    els.append({"f": "fleche", "de": [2.6 + 0.25 * len(nucleons), 1.7], "a": [5.0, 1.7], "texte": "on fournit E_{ℓ}", "couleur": "orange", "pos": "n"})
    els.append({"f": "texte", "at": [1.45 + 0.25 * (len(nucleons) - 2), 0.55], "t": noyau, "couleur": "jaune"})
    els.append({"f": "texte", "at": [5.6 + 0.5 * (len(nucleons) - 1), 0.55], "t": "nucléons séparés", "couleur": "cyan"})
    return {"type": "schema", "titre": titre, "cadre": {"l": 8.4, "h": 3}, "elements": els,
            "legende": "Les nucléons séparés sont au repos ; le noyau est au repos."}


# ---------------------------------------------------------------- calculs (deutérium)
DM_U = 1.00728 + 1.00866 - 2.01355          # 0,00239 u
assert abs(DM_U - 0.00239) < 1e-9
DM_KG = round(DM_U * KG, 32)                         # 3,97·10⁻³⁰ kg
assert abs(DM_U * KG - 3.9674e-30) < 1e-33
DMK = 3.97e-30
EJ = DMK * C ** 2                                    # 3,57·10⁻¹³ J
assert abs(EJ - 3.573e-13) < 1e-16
EJR = 3.57e-13
EMEV = EJR / MEV                                     # 2,23 MeV
assert round(EMEV, 2) == 2.23 and round(DM_U * 931.5, 2) == 2.23   # même valeur par la route u × 931,5

# semblable : tritium
DM3 = 1.00728 + 2 * 1.00866 - 3.01550               # 0,00910 u
assert abs(DM3 - 0.0091) < 1e-9
DMK3 = 1.51e-29
assert abs(DM3 * KG - 1.5106e-29) < 1e-32
EJ3 = DMK3 * C ** 2                                  # 1,359·10⁻¹² J
assert abs(EJ3 - 1.359e-12) < 1e-15
EMEV3 = 1.36e-12 / MEV                               # 8,50 MeV
assert round(EMEV3, 2) == 8.5 and abs(DM3 * 931.5 - 8.48) < 0.01

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "energie_nucleaire", "cours": "phys_ch5_energie_nucleaire",
  "titre": "Le deutérium : du u au joule, puis au MeV", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Convertir une masse de u en kg", "Utiliser E = m·c² avec m en kg et E en joule", "Convertir des joules en MeV"],
  "enonce": {
    "intro": "Le deutérium ²₁H est un isotope de l'hydrogène ; son noyau est formé d'un proton et d'un neutron. Son défaut de masse vaut Δm = 0,00239 u. On veut calculer son énergie de liaison E_ℓ en passant par les unités du système international.",
    "intro_dit": "دابا نقراو l'énoncé. le deutérium، c'est un isotope ديال l'hydrogène. النواة ديالو فيها: un proton et un neutron. le défaut de masse ديالو: delta m égale zéro virgule zéro zéro deux cent trente-neuf u. غادي نحسبو l'énergie de liaison ديالو، بالوحدات ديال le système international.",
    "figures": [separation("Figure : séparer le noyau de deutérium", "²₁H", ["p", "n"])],
    "donnees": ["Δm(²₁H) = 0,00239 u", "1 u = 1,66·10⁻²⁷ kg", "c = 3,00·10⁸ m/s", "1 MeV = 1,6·10⁻¹³ J"],
    "questions": [
      question("1", "Exprimer le défaut de masse Δm du deutérium en kilogramme.",
        "السؤال un: عبر على le défaut de masse ديال le deutérium ب kilogramme.",
        valeur("Δm", 3.97e-30, "kg", "Δm = 0,00239 × 1,66·10⁻²⁷ = 3,97·10⁻³⁰ kg"),
        ["1 u = 1,66·10⁻²⁷ kg", "×", "10⁻²⁷", "kg"], ["Δm = 0,00239/1,66·10⁻²⁷", "Δm = 0,00239 × 931,5"],
        [aide("Une unité u vaut combien de kilogrammes ? Regarde les données.",
              "un u شحال كيساوي ب kilogramme؟ شوف les données."),
         aide("On multiplie la masse en u par 1,66·10⁻²⁷ : Δm (kg) = Δm (u) × 1,66·10⁻²⁷.",
              "كنضربو la masse ب u، fois un virgule soixante-six fois dix puissance moins vingt-sept.")],
        corr([("1 : Δm = 0,00239 u, et 1 u = 1,66·10⁻²⁷ kg", "un u égale un virgule soixante-six fois dix puissance moins vingt-sept kilogramme"),
              ("A.N. : Δm = 0,00239 × 1,66·10⁻²⁷", "zéro virgule zéro zéro deux cent trente-neuf fois un virgule soixante-six"),
              ("Δm = 3,97·10⁻³⁰ kg", "trois virgule quatre-vingt-dix-sept fois dix puissance moins trente kilogramme")],
             "السؤال un. un u égale un virgule soixante-six fois dix puissance moins vingt-sept kilogramme. إذن delta m égale zéro virgule zéro zéro deux cent trente-neuf fois un virgule soixante-six fois dix puissance moins vingt-sept، يعني trois virgule quatre-vingt-dix-sept fois dix puissance moins trente kilogramme."),
        "ex_n2_1", "fa_n2_1"),
      question("2", "En utilisant la relation d'équivalence masse-énergie, calculer l'énergie de liaison E_ℓ du deutérium en joule.",
        "السؤال deux: بالعلاقة ديال l'équivalence masse énergie، حسب l'énergie de liaison ديال le deutérium ب joule.",
        valeur("E_ℓ", 3.57e-13, "J", "E_ℓ = Δm·c² = 3,97·10⁻³⁰ × (3,00·10⁸)² = 3,57·10⁻¹³ J"),
        ["E_ℓ = Δm·c²", "(3,00·10⁸)²", "10¹⁶", "J"], ["E_ℓ = Δm·c", "E_ℓ = 0,00239 × 9·10¹⁶"],
        [aide("Dans E = m·c², pour obtenir des joules, la masse doit être en kg et c en m/s. Tu as Δm en kg à la question 1.",
              "ف E égale m fois c au carré، باش تخرج ب joule، la masse خاصها تكون ب kilogramme، و c ب mètre par seconde. delta m ب kilogramme عندك من السؤال un."),
         aide("E_ℓ = Δm·c², avec c² = (3,00·10⁸)² = 9,00·10¹⁶ m²/s².",
              "E l égale delta m fois c au carré. و c au carré égale trois fois dix puissance huit، الكل au carré، يعني neuf fois dix puissance seize.")],
        corr([("2 : E_ℓ = Δm·c² (Δm en kg, c en m/s, E_ℓ en J)", "E l égale delta m fois c au carré"),
              ("A.N. : E_ℓ = 3,97·10⁻³⁰ × (3,00·10⁸)² = 3,97·10⁻³⁰ × 9·10¹⁶", "trois virgule quatre-vingt-dix-sept fois dix puissance moins trente، fois neuf fois dix puissance seize"),
              ("E_ℓ = 3,57·10⁻¹³ J", "trois virgule cinquante-sept fois dix puissance moins treize joule")],
             "السؤال deux. E l égale delta m fois c au carré، مع delta m ب kilogramme. l'application numérique: trois virgule quatre-vingt-dix-sept fois dix puissance moins trente، fois neuf fois dix puissance seize. كنلقاو E l égale trois virgule cinquante-sept fois dix puissance moins treize joule."),
        "ex_n2_2", "fa_n2_2"),
      question("3", "Convertir E_ℓ en MeV, puis vérifier ce résultat avec 1 u = 931,5 MeV/c².",
        "السؤال trois: حول E l ل méga électron volt، ومن بعد تأكد من النتيجة بالعلاقة: un u égale neuf cent trente et un virgule cinq méga électron volt sur c au carré.",
        valeur("E_ℓ", 2.23, "MeV", "E_ℓ = 3,57·10⁻¹³/1,6·10⁻¹³ = 2,23 MeV"),
        ["1 MeV = 1,6·10⁻¹³ J", "÷", "MeV", "931,5"], ["1 MeV = 1,6·10⁻¹⁹ J", "E_ℓ = 3,57·10⁻¹³ × 1,6·10⁻¹³"],
        [aide("Un MeV vaut combien de joules ? Un nombre de joules contient combien de fois cette quantité ?",
              "un méga électron volt شحال فيه من joule؟ و E l ديالنا فيها شحال من مرة هاد la quantité؟"),
         aide("E (MeV) = E (J) / 1,6·10⁻¹³. Pour vérifier : E_ℓ = Δm (u) × 931,5 MeV.",
              "E ب méga électron volt égale E ب joule، sur un virgule six fois dix puissance moins treize. وباش تتأكد: delta m ب u fois neuf cent trente et un virgule cinq.")],
        corr([("3 : 1 MeV = 1,6·10⁻¹³ J, donc E_ℓ = 3,57·10⁻¹³/1,6·10⁻¹³", "un méga électron volt égale un virgule six fois dix puissance moins treize joule"),
              ("E_ℓ = 2,23 MeV", "E l égale deux virgule vingt-trois méga électron volt"),
              ("Vérification : E_ℓ = 0,00239 × 931,5 = 2,23 MeV : même résultat.", "zéro virgule zéro zéro deux cent trente-neuf fois neuf cent trente et un virgule cinq")],
             "السؤال trois. un méga électron volt égale un virgule six fois dix puissance moins treize joule. إذن كنقسمو: trois virgule cinquante-sept fois dix puissance moins treize، sur un virgule six fois dix puissance moins treize. E l égale deux virgule vingt-trois méga électron volt. وباش نتأكدو: zéro virgule zéro zéro deux cent trente-neuf fois neuf cent trente et un virgule cinq، كتعطي حتى هي، deux virgule vingt-trois. نفس النتيجة بجوج طرق."),
        "ex_n2_3", "fa_n2_3"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_n2_1", "Question 1 : de u à kg", "1 u = 1,66·10⁻²⁷ kg : Δm = 0,00239 × 1,66·10⁻²⁷ = 3,97·10⁻³⁰ kg",
      SIMD + "figures.html?fig=fig_unites", "L'escalier des unités : la première marche, 1 u = 1,66·10⁻²⁷ kg",
      "شوف l'escalier ديال les unités. la première marche: l'unité de masse atomique، u. un u égale un virgule soixante-six fois dix puissance moins vingt-sept kilogramme. باش نحولو من u ل kilogramme، كنضربو fois un virgule soixante-six fois dix puissance moins vingt-sept. بالنسبة ل le deutérium: zéro virgule zéro zéro deux cent trente-neuf fois un virgule soixante-six fois dix puissance moins vingt-sept، يعني trois virgule quatre-vingt-dix-sept fois dix puissance moins trente kilogramme. صغيرة بزاف، ولكن عادي: هادي masse ديال نواة.",
      centre=[("1 u = 1,66·10⁻²⁷ kg", "un u égale un virgule soixante-six"),
              ("Δm = 0,00239 × 1,66·10⁻²⁷ = 3,97·10⁻³⁰ kg", "يعني trois virgule quatre-vingt-dix-sept fois dix puissance moins trente kilogramme")],
      pointage=[{"mot": "شوف l'escalier", "commande": "play_until", "parametres": {"moment": "u"}},
                {"mot": "un u égale un virgule soixante-six", "repere": "u"}]),
    diapo_sim("ex_n2_2", "Question 2 : E = m·c² en joule", "E_ℓ = Δm·c² = 3,97·10⁻³⁰ × 9·10¹⁶ = 3,57·10⁻¹³ J",
      SIMD + "figures.html?fig=fig_einstein", "La relation d'Einstein et ses unités : J, kg, m/s",
      "شوف la relation d'Einstein: E égale m fois c au carré. شوف les unités: E ب joule، m ب kilogramme، و c égale trois virgule zéro zéro fois dix puissance huit mètre par seconde. هادي علاش حولنا delta m ل kilogramme. c au carré: neuf fois dix puissance seize. إذن E l égale trois virgule quatre-vingt-dix-sept fois dix puissance moins trente، fois neuf fois dix puissance seize، يعني trois virgule cinquante-sept fois dix puissance moins treize joule.",
      centre=[("E_ℓ = Δm·c²", "E égale m fois c au carré"),
              ("E_ℓ = 3,97·10⁻³⁰ × 9·10¹⁶ = 3,57·10⁻¹³ J", "يعني trois virgule cinquante-sept fois dix puissance moins treize joule")],
      pointage=[{"mot": "شوف la relation d'Einstein", "commande": "play_until", "parametres": {"moment": "relation"}},
                {"mot": "شوف les unités", "commande": "play_until", "parametres": {"moment": "termes"}},
                {"mot": "E égale m fois c au carré", "repere": "relation"}]),
    diapo_sim("ex_n2_3", "Question 3 : en MeV", "E_ℓ = 3,57·10⁻¹³ / 1,6·10⁻¹³ = 2,23 MeV",
      SIMD + "liaison.html?sens=separer&noyau=deuterium", "Séparer le deutérium : on fournit E_ℓ = 2,23 MeV",
      "شوف النواة ديال le deutérium: un proton et un neutron لاصقين. باش نفرقوهم، خاصنا نعطيو l'énergie. النواة كتهرس، و les nucléons كيتبعدو. l'énergie اللي عطينا هي E l. ب joule لقينا E l égale trois virgule cinquante-sept fois dix puissance moins treize. et un méga électron volt égale un virgule six fois dix puissance moins treize joule. كنقسمو: deux virgule vingt-trois méga électron volt. شوف la flèche: E l égale deux virgule vingt-trois méga électron volt، نفس النتيجة.",
      centre=[("1 MeV = 1,6·10⁻¹³ J", "un méga électron volt égale un virgule six"),
              ("E_ℓ = 3,57·10⁻¹³ / 1,6·10⁻¹³ = 2,23 MeV", "كنقسمو: deux virgule vingt-trois")],
      pointage=[{"mot": "شوف النواة", "commande": "play_until", "parametres": {"moment": "noyau_repos"}},
                {"mot": "خاصنا نعطيو l'énergie", "commande": "play_until", "parametres": {"moment": "energie_fournie"}},
                {"mot": "النواة كتهرس", "commande": "play_until", "parametres": {"moment": "nucleons_separes"}},
                {"mot": "شوف la flèche", "repere": "fleche_El"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_n2_1", "Plus facile : u → kg", "نتمرنو بسؤال ساهل على les unités.",
      "Une masse de 2 u vaut, en kilogramme :",
      ["3,32·10⁻²⁷ kg", "1,20·10²⁷ kg", "1863 kg"], 0, {
        "0": {"juste": rep("برافو! deux fois un virgule soixante-six fois dix puissance moins vingt-sept، يعني trois virgule trente-deux fois dix puissance moins vingt-sept kilogramme.", "Juste : 2 × 1,66·10⁻²⁷ = 3,32·10⁻²⁷ kg.")},
        "1": {"1": rep("ما تقلقش. masse ديال نواة واش تكون كبيرة بزاف ولا صغيرة بزاف؟ واش قسمتي ولا ضربتي؟ عاود اختار.", "Une masse de noyau est minuscule : il faut multiplier, pas diviser. Réessaie."),
              "2": rep("الجواب هو m égale trois virgule trente-deux fois dix puissance moins vingt-sept kilogramme. كنضربو fois un virgule soixante-six fois dix puissance moins vingt-sept.", "Réponse : 2 × 1,66·10⁻²⁷ = 3,32·10⁻²⁷ kg.")},
        "2": {"1": rep("لا، la valeur neuf cent trente et un virgule cinq كتعطي méga électron volt، ماشي kilogramme. شوف la valeur ديال u ب kilogramme. عاود اختار.", "931,5 donne des MeV, pas des kg. Réessaie."),
              "2": rep("الجواب هو m égale trois virgule trente-deux fois dix puissance moins vingt-sept kilogramme. la valeur neuf cent trente et un virgule cinq هي ديال l'énergie.", "Réponse : 3,32·10⁻²⁷ kg ; 931,5 sert pour les MeV.")}},
      "Une masse de deux u vaut combien en kilogramme ?"),
    qcm_facile("fa_n2_2", "Plus facile : les unités de E = m·c²", "سؤال ساهل على les unités ديال E égale m fois c au carré.",
      "Pour obtenir E en joule avec E = m·c², on prend :",
      ["m en u et c en m/s", "m en kg et c en m/s", "m en g et c en km/s"], 1, {
        "1": {"juste": rep("برافو! m ب kilogramme و c ب mètre par seconde، كتخرج E ب joule.", "Juste : kg et m/s donnent des joules.")},
        "0": {"1": rep("قريب. ولكن u ماشي وحدة ديال le système international. شنو هي الوحدة ديال la masse فيه؟ عاود اختار.", "Le u n'est pas une unité du système international. Réessaie."),
              "2": rep("الجواب هو m ب kilogramme و c ب mètre par seconde. يلا بغيتي تخدم ب u، راه avec neuf cent trente et un virgule cinq و méga électron volt.", "Réponse : m en kg, c en m/s. Avec u, on utilise 931,5 et les MeV.")},
        "2": {"1": rep("لا، le gramme و le kilomètre par seconde ماشي ديال le système international. عاود اختار.", "g et km/s ne sont pas des unités SI. Réessaie."),
              "2": rep("الجواب هو m ب kilogramme و c ب mètre par seconde.", "Réponse : m en kg, c en m/s.")}},
      "Pour obtenir E en joule avec E égale m fois c au carré, on prend quelles unités ?"),
    association_facile("fa_n2_3", "Plus facile : relier les unités", "سؤال ساهل: ربط كل وحدة بالقيمة ديالها.",
      "Relie chaque grandeur à sa valeur.", "Associer chaque égalité à sa valeur.",
      [("1", "1 u"), ("2", "1 MeV"), ("3", "1 u·c²")],
      [("a", "1,6·10⁻¹³ J"), ("b", "931,5 MeV"), ("c", "1,66·10⁻²⁷ kg")],
      {"1": "c", "2": "a", "3": "b"},
      {"1-c": (True, "Oui : 1 u = 1,66·10⁻²⁷ kg, c'est une masse.", "صحيح. un u égale un virgule soixante-six fois dix puissance moins vingt-sept kilogramme، هادي masse."),
       "1-a": (False, "1 u est une masse ; 1,6·10⁻¹³ J est une énergie. Cherche une valeur en kg.", "un u هي masse، و هادي énergie ب joule. قلب على valeur ب kilogramme."),
       "1-b": (False, "931,5 MeV est l'énergie de 1 u·c², pas la masse 1 u en kg. Cherche une valeur en kg.", "neuf cent trente et un virgule cinq méga électron volt هي l'énergie ديال u fois c au carré. قلب على valeur ب kilogramme."),
       "2-a": (True, "Oui : 1 MeV = 10⁶ eV = 1,6·10⁻¹³ J.", "صحيح. un méga électron volt égale un virgule six fois dix puissance moins treize joule."),
       "2-b": (False, "931,5 MeV, c'est 1 u·c². 1 MeV tout seul vaut combien de joules ?", "neuf cent trente et un virgule cinq هي u fois c au carré. un méga électron volt بوحدو شحال ب joule؟"),
       "2-c": (False, "1 MeV est une énergie, pas une masse en kg. Cherche une valeur en joule.", "un méga électron volt هو énergie، ماشي masse. قلب على valeur ب joule."),
       "3-b": (True, "Oui : 1 u·c² = 931,5 MeV, donc 1 u = 931,5 MeV/c².", "صحيح. u fois c au carré égale neuf cent trente et un virgule cinq méga électron volt."),
       "3-a": (False, "1,6·10⁻¹³ J, c'est un seul MeV. 1 u·c² en vaut beaucoup plus.", "هادي هي l'énergie de un méga électron volt. u fois c au carré كتساوي كثر بزاف."),
       "3-c": (False, "1 u·c² est une énergie (une masse fois c²), pas une masse en kg.", "u fois c au carré هي énergie، ماشي masse ب kilogramme.")},
      "(1 ; c) (2 ; a) (3 ; b) : u → kg, MeV → J, u·c² → 931,5 MeV.",
      "الأزواج: un avec c، deux avec a، trois avec b. u ل kilogramme، méga électron volt ل joule، و u fois c au carré égale neuf cent trente et un virgule cinq."),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données : le tritium",
    "enonce": {
      "intro": "Le tritium ³₁H est un autre isotope de l'hydrogène (un proton, deux neutrons). Son défaut de masse vaut Δm = 0,00910 u.",
      "intro_dit": "نفس التمرين مع le tritium: un proton et deux neutrons، و delta m égale zéro virgule zéro zéro neuf cent dix u.",
      "figures": [separation("Figure : séparer le noyau de tritium", "³₁H", ["p", "n", "n"])],
      "donnees": ["Δm(³₁H) = 0,00910 u", "1 u = 1,66·10⁻²⁷ kg", "c = 3,00·10⁸ m/s", "1 MeV = 1,6·10⁻¹³ J"],
      "questions": [
        question_semblable("1", "Exprimer le défaut de masse Δm du tritium en kilogramme.",
          valeur("Δm", 1.51e-29, "kg", "Δm = 0,00910 × 1,66·10⁻²⁷ = 1,51·10⁻²⁹ kg"), ["1 u = 1,66·10⁻²⁷ kg", "kg"], ["Δm = 0,00910 × 931,5"],
          corr([("1 : Δm = 0,00910 × 1,66·10⁻²⁷", "zéro virgule zéro zéro neuf cent dix fois un virgule soixante-six"), ("Δm = 1,51·10⁻²⁹ kg", "un virgule cinquante et un fois dix puissance moins vingt-neuf kilogramme")],
               "delta m égale zéro virgule zéro zéro neuf cent dix fois un virgule soixante-six fois dix puissance moins vingt-sept، يعني un virgule cinquante et un fois dix puissance moins vingt-neuf kilogramme.")),
        question_semblable("2", "Calculer l'énergie de liaison E_ℓ du tritium en joule.",
          valeur("E_ℓ", 1.36e-12, "J", "E_ℓ = Δm·c² = 1,51·10⁻²⁹ × 9·10¹⁶ = 1,36·10⁻¹² J"), ["E_ℓ = Δm·c²", "J"], ["E_ℓ = Δm·c"],
          corr([("2 : E_ℓ = Δm·c² = 1,51·10⁻²⁹ × (3,00·10⁸)²", "E l égale delta m fois c au carré"), ("E_ℓ = 1,36·10⁻¹² J", "un virgule trente-six fois dix puissance moins douze joule")],
               "E l égale delta m fois c au carré، يعني un virgule cinquante et un fois dix puissance moins vingt-neuf، fois neuf fois dix puissance seize. كنلقاو E l égale un virgule trente-six fois dix puissance moins douze joule.")),
        question_semblable("3", "Convertir E_ℓ en MeV, puis vérifier avec 1 u = 931,5 MeV/c².",
          valeur("E_ℓ", 8.5, "MeV", "E_ℓ = 1,36·10⁻¹²/1,6·10⁻¹³ = 8,50 MeV"), ["1 MeV = 1,6·10⁻¹³ J", "MeV"], ["1 MeV = 1,6·10⁻¹⁹ J"],
          corr([("3 : E_ℓ = 1,36·10⁻¹²/1,6·10⁻¹³ = 8,50 MeV", "huit virgule cinq méga électron volt"),
                ("Vérification : 0,00910 × 931,5 = 8,48 MeV ≈ 8,50 MeV (arrondis).", "huit virgule quarante-huit")],
               "E l égale un virgule trente-six fois dix puissance moins douze، sur un virgule six fois dix puissance moins treize، يعني huit virgule cinq méga électron volt. وبالطريقة الأخرى: zéro virgule zéro zéro neuf cent dix fois neuf cent trente et un virgule cinq، يعني huit virgule quarante-huit. الفرق صغير، جا من les arrondis.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
