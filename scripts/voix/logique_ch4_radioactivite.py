"""Nouvelle logique du cours phys_ch4_radioactivite (18 novembre 2026, skill logique-de-cours).

Lit le cours en ligne backend/data/courses/phys_ch4_radioactivite.json (jamais modifié) et écrit la version en attente
backend/data/courses/en_attente/phys_ch4_radioactivite.json : ordre des diapositives, parties, séances et blocs refaits,
une diapositive nouvelle (ra_l1b_moitie), cinq textes réécrits, deux exercices du national joués en étapes.
L'architecture et ses raisons : backend/data/curriculum/architecture/phys_ch4_radioactivite.md.
Relançable : repart toujours du cours en ligne.  Usage : python -X utf8 scripts/voix/logique_ch4_radioactivite.py"""
import copy, json, os

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
DECK = "phys_ch4_radioactivite"
SRC = os.path.join(RACINE, "backend/data/courses", DECK + ".json")
DST = os.path.join(RACINE, "backend/data/courses/en_attente", DECK + ".json")
SIM = "/media/simulations/physics/radioactivite-tableau/"

# ── Parties (activities) : l'ordre nouveau ──────────────────────────────────────────────────────────────────────────
PARTIES = [
    ("ra_partie1", "I. Le noyau et sa stabilité", "explanation", 36,
     ["ra_n1_ouverture", "ra_n2_atome", "ra_n3_compter", "ra_n4_notation", "ra_n5_composition", "ra_n6_isotopes",
      "ra_s1_diagramme", "ra_s2_vallee", "ra_s5_isotopes_ligne"]),
    ("ra_partie2", "II. La radioactivité et les désintégrations", "explanation", 40,
     ["ra_r1_definition", "ra_r2_caracteres", "ra_r2b_spontanee", "ra_r3_soddy", "ra_d1_alpha", "ra_d2_beta_moins",
      "ra_d3_beta_plus", "ra_d4_gamma", "ra_d5_inconnu", "ra_d6_type"]),
    ("ra_partie3", "III. Les désintégrations sur le diagramme, la famille", "explanation", 26,
     ["ra_s4_fleches", "ra_s4b_alpha", "ra_s3_zones", "ra_f1_famille", "ra_f3_famille2024", "ra_f2_systeme"]),
    ("ra_partie4", "IV. Compter les noyaux, puis la loi de décroissance", "explanation", 56,
     ["ra_p3_puissances", "ra_l1_echantillon", "ra_l1b_moitie", "ra_t1_definition", "ra_l2_proportion",
      "ra_l3_equation", "ra_l4a_exp", "ra_l4_rappel", "ra_l5_loi", "ra_l6_lambda", "ra_l8_restants", "ra_l7_tau",
      "ra_l7b_037", "ra_t2_demo", "ra_t3_paliers", "ra_t4_pourcentages"]),
    ("ra_partie5", "V. L'activité et la datation", "application", 44,
     ["ra_a1_compteur", "ra_a2_definition", "ra_a3_demo", "ra_a3b_loi_activite", "ra_a4_unites", "ra_p4_mole",
      "ra_a5_masse", "ra_a5b_masse_inverse", "ra_a6_courbe_a", "ra_a7_droite_ln", "ra_c1_principe", "ra_c2_demo",
      "ra_c4_fils_pere", "ra_c4b_rapport"]),
    ("ra_partie6", "VI. Exercices du national, joués étape par étape", "evaluation", 22,
     ["ra_x1_cas_types", "ra_c3_calcul", "ra_x2_2021N", "ra_x3_2022N", "ra_x4_2025N"]),
    ("ra_bilan", "VII. Bilan du chapitre", "evaluation", 10, ["ra_z1_bilan", "ra_z2_carte"]),
]

SEANCES = [
    ("ra_s1", "Séance 1 — Le noyau, sa notation et le diagramme (N, Z)", [
        ("ra_s1_b1", "L'atome, le noyau et sa notation", ["ra_n1_ouverture", "ra_n2_atome", "ra_n3_compter", "ra_n4_notation"]),
        ("ra_s1_b2", "Composition, isotopes, le diagramme (N, Z)", ["ra_n5_composition", "ra_n6_isotopes", "ra_s1_diagramme"]),
        ("ra_s1_b3", "La vallée de stabilité, les isotopes sur le diagramme", ["ra_s2_vallee", "ra_s5_isotopes_ligne"])]),
    ("ra_s2", "Séance 2 — La radioactivité et les désintégrations", [
        ("ra_s2_b1", "La radioactivité et ses caractères", ["ra_r1_definition", "ra_r2_caracteres", "ra_r2b_spontanee"]),
        ("ra_s2_b2", "Les lois de Soddy, α et β⁻", ["ra_r3_soddy", "ra_d1_alpha", "ra_d2_beta_moins"]),
        ("ra_s2_b3", "β⁺, γ, le noyau fils et le type", ["ra_d3_beta_plus", "ra_d4_gamma", "ra_d5_inconnu", "ra_d6_type"])]),
    ("ra_s3", "Séance 3 — Le diagramme, la famille, puis compter les noyaux", [
        ("ra_s3_b1", "Chaque désintégration sur le diagramme", ["ra_s4_fleches", "ra_s4b_alpha", "ra_s3_zones"]),
        ("ra_s3_b2", "La famille radioactive", ["ra_f1_famille", "ra_f3_famille2024", "ra_f2_systeme"]),
        ("ra_s3_b3", "Beaucoup de noyaux : on compte, la demi-vie", ["ra_p3_puissances", "ra_l1_echantillon", "ra_l1b_moitie", "ra_t1_definition"])]),
    ("ra_s4", "Séance 4 — La loi de décroissance", [
        ("ra_s4_b1", "La même proportion, l'équation, l'exponentielle", ["ra_l2_proportion", "ra_l3_equation", "ra_l4a_exp"]),
        ("ra_s4_b2", "ln, la loi, λ", ["ra_l4_rappel", "ra_l5_loi", "ra_l6_lambda"]),
        ("ra_s4_b3", "Restants et désintégrés, τ", ["ra_l8_restants", "ra_l7_tau", "ra_l7b_037"])]),
    ("ra_s5", "Séance 5 — La demi-vie par la loi, l'activité", [
        ("ra_s5_b1", "t½ = ln2/λ, les paliers, les pourcentages", ["ra_t2_demo", "ra_t3_paliers", "ra_t4_pourcentages"]),
        ("ra_s5_b2", "L'activité : a = λ·N, puis a(t)", ["ra_a1_compteur", "ra_a2_definition", "ra_a3_demo", "ra_a3b_loi_activite"]),
        ("ra_s5_b3", "Les secondes, la mole, le nombre de noyaux", ["ra_a4_unites", "ra_p4_mole", "ra_a5_masse"])]),
    ("ra_s6", "Séance 6 — Masse, courbes du national, datation", [
        ("ra_s6_b1", "La masse, la courbe a(t), la droite ln N", ["ra_a5b_masse_inverse", "ra_a6_courbe_a", "ra_a7_droite_ln"]),
        ("ra_s6_b2", "Le principe de la datation", ["ra_c1_principe", "ra_c2_demo"]),
        ("ra_s6_b3", "Dater une roche", ["ra_c4_fils_pere", "ra_c4b_rapport"])]),
    ("ra_s7", "Séance 7 — Exercices du national joués, bilan et carte", [
        ("ra_s7_b1", "Cas types, datation 2022 R, national 2021 N", ["ra_x1_cas_types", "ra_c3_calcul", "ra_x2_2021N"]),
        ("ra_s7_b2", "Nationaux 2022 N et 2025 N", ["ra_x3_2022N", "ra_x4_2025N"]),
        ("ra_s7_b3", "Bilan et carte", ["ra_z1_bilan", "ra_z2_carte"])]),
]


def r(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}


def demo(lignes, parole):
    """lignes : [(texte, mot)] ; chaque mot est un extrait exact de parole."""
    for _, m in lignes:
        assert m in parole, m
    return {"parole": parole, "lignes": [{"texte": t, "mot": m} for t, m in lignes]}


# ── Diapositive nouvelle : on compte les noyaux restants tous les 8 jours ───────────────────────────────────────────
L1B_TEXTE = ("دابا نحسبو حنا بيدينا. شوف العدد اللي مكتوب: فالبداية، quatre cents noyaux. كنخليو الوقت يدوز huit jours، "
             "ومن بعد نحبسو. بقاو deux cents. نكملو huit jours أخرى، حتى ل seize jours. بقاو cent. ومن بعد huit jours "
             "حتى هي، حتى ل vingt-quatre jours: بقاو cinquante. quatre cents، deux cents، cent، cinquante. "
             "خود الوقت ديالك، وقارن كل عدد مع اللي قبل منو.")
L1B = {
    "id": "ra_l1b_moitie",
    "slide_type": "concept",
    "title": "Compter les noyaux tous les 8 jours",
    "screen_content": {
        "lead": "On lit le compteur à 0, 8, 16 et 24 jours.",
        "bullets": ["À t = 0 : N₀ = 400 noyaux d'iode 131.",
                    "On arrête à 8 jours, 16 jours, 24 jours et on lit N.",
                    "On compare chaque nombre au précédent."],
        "student_trace": "Iode 131 : 400 → 200 → 100 → 50 noyaux tous les 8 jours ; N est divisé par 2 pendant la même durée."},
    "visual": {"kind": "simulation", "url": SIM + "population.html?vue=grand_nombre&conclusions=0&compter=1",
               "caption": "On compte les noyaux restants",
               "alt": "La grille de 400 noyaux et la courbe N(t) arrêtée à 8, 16 et 24 jours, le nombre restant écrit à chaque arrêt"},
    "speech_text": {
        "fr": "Maintenant on compte nous-mêmes. Au départ, 400 noyaux. On laisse passer 8 jours : il en reste 200. "
              "8 jours de plus, 16 jours : il en reste 100. Encore 8 jours, 24 jours : il en reste 50. 400, 200, 100, 50 : "
              "prends ton temps et compare chaque nombre au précédent.",
        "mixed": L1B_TEXTE},
    "concentration": {
        "demarrer": "reset",
        "pointage": [
            {"mot": "شوف العدد اللي مكتوب", "repere": "compteur"},
            {"mot": "فالبداية، quatre cents", "commande": "play_until", "parametres": {"moment": "depart"}},
            {"mot": "ومن بعد نحبسو.", "commande": "play_until", "parametres": {"moment": "un_t_demi"}},
            {"mot": "نكملو huit jours أخرى", "commande": "play_until", "parametres": {"moment": "deux_t_demi"}},
            {"mot": "ومن بعد huit jours", "commande": "play_until", "parametres": {"moment": "trois_t_demi"}},
            {"mot": "quatre cents، deux cents، cent، cinquante", "repere": "courbe"}],
        "cahier": "Iode 131 : 400 → 200 → 100 → 50 noyaux, tous les 8 jours : N est divisé par 2 pendant la même durée.",
        "reponses": {"q": {
            "0": {"1": r("قريب، العدد كينقص فعلا. ولكن شوف مزيان: من quatre cents ل deux cents، مشاو deux cents، ماشي cent. قارن كل عدد مع اللي قبل منو.",
                         "Le nombre diminue, oui. Mais de 400 à 200, il en part 200, pas 100. Compare chaque nombre au précédent."),
                  "2": r("لا. quatre cents، deux cents، cent، cinquante: كل مرة كنقسمو على deux. ماشي نفس العدد اللي كيمشي، كيمشي النص ديال اللي باقي.",
                         "Non. 400, 200, 100, 50 : chaque fois on divise par 2. Ce n'est pas le même nombre qui part : c'est la moitié de ce qui reste.")},
            "1": {"juste": r("مزيان! كل huit jours، العدد كيتقسم على deux: quatre cents، deux cents، cent، cinquante. هاد المدة، huit jours، عندها سمية: la demi-vie.",
                             "Oui ! Tous les 8 jours, N est divisé par 2 : 400, 200, 100, 50. Cette durée de 8 jours a un nom : la demi-vie.")},
            "2": {"1": r("صحيح غير فالأول: من quatre cents ل deux cents، مشاو deux cents. ولكن من deux cents ل cent، شحال مشاو؟ قارن مزيان.",
                         "Juste pour le premier arrêt : de 400 à 200, il en part 200. Mais de 200 à 100, combien en part-il ? Compare."),
                  "2": r("لا. ف huit jours اللولين مشاو deux cents، من بعد غير cent، من بعد cinquante. اللي كيبقى هو هو: كل مرة كيبقى النص. N كيتقسم على deux.",
                         "Non. Les 8 premiers jours, 200 partent, puis 100, puis 50. Ce qui ne change pas : chaque fois il reste la moitié. N est divisé par 2.")}}}},
    "question": {
        "type": "qcm",
        "prompt": "Tous les 8 jours, que devient le nombre N de noyaux restants ?",
        "options": ["Il diminue de 100 noyaux", "Il est divisé par deux", "Il diminue de 200 noyaux"],
        "timeout_seconds": 30,
        "correct": 1,
        "enonce_dit": "شوف هاد السؤال: tous les huit jours، شنو كيوقع ل le nombre N de noyaux restants ؟",
        "demonstration": demo([
            ("400 → 200 : 400 ÷ 2 = 200", "من quatre cents ل deux cents"),
            ("200 → 100 : 200 ÷ 2 = 100", "من deux cents ل cent"),
            ("100 → 50 : 100 ÷ 2 = 50", "من cent ل cinquante"),
            ("Tous les 8 jours, N est divisé par 2", "إذن كل huit jours")],
            "les données: quatre cents، deux cents، cent، cinquante. من quatre cents ل deux cents: quatre cents sur deux. "
            "من deux cents ل cent: deux cents sur deux. من cent ل cinquante: cent sur deux. "
            "إذن كل huit jours، N كيتقسم على deux.")},
    "competence_ids": ["C7"],
}

# ── Textes réécrits ─────────────────────────────────────────────────────────────────────────────────────────────────
S5_TEXTE = ("les isotopes عندهم نفس Z. إذن، فالرسم، عندهم نفس l'abscisse. كلهم على خط عمودي واحد، perpendiculaire "
            "على l'axe des Z. le carbone douze وسط la vallée: stable. le carbone quatorze فوق la vallée: عندو بزاف ديال "
            "les neutrons، إذن instable. نفس l'élément، ولكن واحد stable وواحد instable. شنو كيدير le carbone quatorze "
            "باش يرجع ل la vallée؟ هادشي اللي غادي نشوفو فالجزء الجاي.")
P3_TEXTE_DEBUT_ANCIEN = "قبل ما نحولو، تذكير صغير على les puissances de dix."
P3_TEXTE_DEBUT = ("دابا غادي نحسبو بزاف ديال les noyaux: فشي شوية ديال la matière، كاينين بزاف بزاف ديال les noyaux. "
                  "باش نكتبو هاد الأعداد، تذكير صغير على les puissances de dix.")
D6_FIN = (" نلقاو X ب Soddy. على A: deux cent quarante et un égale deux cent quarante et un plus A، إذن A égale zéro. "
          "على Z: quatre-vingt-quatorze égale quatre-vingt-quinze plus Z، إذن Z égale moins un. "
          "X هو l'électron: إذن la désintégration هي bêta moins.")
C3_TEXTE = ("فالامتحان الوطني deux mille vingt-deux، عطاونا l'activité ديال واحد الخشب قديم: trois cent dix-huit "
            "becquerels. واحد الخشب جديد عندو نفس la masse: quatre cent dix-huit becquerels، هو a zéro. و la demi-vie ديال "
            "le carbone quatorze: cinq mille sept cent trente ans. السؤال: شحال عندو هاد الخشب ديال العمر؟ "
            "غادي نديروه خطوة من بعد خطوة، ونتا اللي غادي تدير كل خطوة: الأول la relation، من بعد lambda، وفاللخر t.")

C3_STEPS = {
    "question": {
        "type": "qcm",
        "prompt": "Étape 1 — Quelle relation donne l'âge t du bois ?",
        "options": ["t = (1/λ)·ln(a/a₀)", "t = (1/λ)·ln(a₀/a)", "t = λ·ln(a₀/a)"],
        "timeout_seconds": 30, "correct": 1,
        "enonce_dit": "الخطوة اللولى: quelle relation donne l'âge t du bois ?",
        "demonstration": demo([
            ("a = a₀·e^(−λt)", "la loi: a égale a zéro"),
            ("a₀/a = e^(λt)", "a zéro sur a égale exponentielle lambda t"),
            ("ln(a₀/a) = λ·t", "ln de a zéro sur a égale lambda t"),
            ("t = (1/λ)·ln(a₀/a)", "t égale un sur lambda")],
            "la loi: a égale a zéro exponentielle moins lambda t. كنقلبو: a zéro sur a égale exponentielle lambda t. "
            "كنديرو ln: ln de a zéro sur a égale lambda t. إذن t égale un sur lambda fois ln de a zéro sur a.")},
    "exercises": [
        {"type": "qcm",
         "prompt": "Étape 2 — Calcule λ du carbone 14 (t½ = 5730 ans).",
         "choices": ["λ ≈ 1,21·10⁻⁴ an⁻¹", "λ ≈ 3,97·10³ an⁻¹", "λ ≈ 1,21·10⁻⁴ s⁻¹"],
         "correct": 0,
         "explanation": "λ = ln2/t½ = 0,693/5730 ≈ 1,21·10⁻⁴ an⁻¹ : t½ est en ans, donc λ est en an⁻¹.",
         "enonce_dit": "الخطوة التانية: calcule lambda du carbone quatorze، t un demi égale cinq mille sept cent trente ans.",
         "demonstration": demo([
             ("λ = ln2/t½", "la relation: lambda égale ln deux sur t un demi"),
             ("λ = 0,693/5730", "l'application numérique"),
             ("λ ≈ 1,21·10⁻⁴ an⁻¹ (t½ en ans, donc λ en an⁻¹)", "le résultat")],
             "la relation: lambda égale ln deux sur t un demi. l'application numérique: zéro virgule six cent "
             "quatre-vingt-treize sur cinq mille sept cent trente. le résultat: lambda تقريبا un virgule vingt et un "
             "fois dix puissance moins quatre an puissance moins un. t un demi ب ans، إذن lambda ب an puissance moins un.")},
        {"type": "qcm",
         "prompt": "Étape 3 — Calcule l'âge t du bois (a₀ = 418 Bq ; a = 318 Bq).",
         "choices": ["t ≈ 2,26·10³ ans", "t ≈ −2,26·10³ ans", "t ≈ 3,3·10⁻⁵ ans"],
         "correct": 0,
         "explanation": "t = (1/λ)·ln(a₀/a) = ln(418/318)/(1,21·10⁻⁴) ≈ 0,273/(1,21·10⁻⁴) ≈ 2,26·10³ ans.",
         "enonce_dit": "الخطوة التالتة: calcule l'âge t du bois، a zéro égale quatre cent dix-huit becquerels، و a égale trois cent dix-huit becquerels.",
         "demonstration": demo([
             ("t = (1/λ)·ln(a₀/a)", "la relation"),
             ("ln(a₀/a) = ln(418/318) ≈ 0,273", "ln de quatre cent dix-huit"),
             ("t = 0,273/(1,21·10⁻⁴)", "l'application numérique"),
             ("t ≈ 2,26·10³ ans", "le résultat")],
             "la relation: t égale un sur lambda fois ln de a zéro sur a. ln de quatre cent dix-huit sur trois cent "
             "dix-huit، كيعطي تقريبا zéro virgule deux cent soixante-treize. l'application numérique: zéro virgule "
             "deux cent soixante-treize، sur un virgule vingt et un fois dix puissance moins quatre. le résultat: t "
             "تقريبا deux virgule vingt-six fois dix puissance trois ans، يعني تقريبا deux mille deux cent soixante ans.")}],
}
C3_REPONSES = {
    "q": {"0": {"1": r("قريب، فيها ln و un sur lambda. ولكن شوف le rapport: a كتنقص، إذن a sur a zéro صغر من un، و ln ديالو سالب: كتلقى عمر سالب. قلب le rapport.",
                       "Presque : il y a bien 1/λ et ln. Mais a < a₀, donc ln(a/a₀) est négatif : l'âge serait négatif. Retourne la fraction."),
                "2": r("لا. a sur a zéro صغر من un، ln ديالو سالب. الصحيح: t égale un sur lambda fois ln de a zéro sur a، و a zéro sur a كبر من un.",
                       "Non. ln(a/a₀) est négatif. La bonne relation : t = (1/λ)·ln(a₀/a), avec la fraction plus grande que 1.")},
          "1": {"juste": r("مزيان! t égale un sur lambda fois ln de a zéro sur a: a zéro sur a كبر من un، والعمر كيخرج positif.",
                           "Oui ! t = (1/λ)·ln(a₀/a) : la fraction est plus grande que 1, l'âge sort positif.")},
          "2": {"1": r("فيها ln de a zéro sur a، مزيان. ولكن lambda فين خاصها تكون؟ ln ما عندوش unité، و t خاصو يكون مدة. شوف l'unité ديال lambda.",
                       "Le ln(a₀/a) est juste. Mais où va λ ? ln n'a pas d'unité et t est une durée : regarde l'unité de λ."),
                "2": r("لا. lambda ب an puissance moins un، إذن خاصنا نقسمو عليها باش نلقاو مدة: t égale un sur lambda fois ln de a zéro sur a.",
                       "Non. λ est en an⁻¹ : il faut diviser par λ pour obtenir une durée. t = (1/λ)·ln(a₀/a).")}},
    "e0": {"0": {"juste": r("مزيان! lambda égale ln deux sur t un demi، تقريبا un virgule vingt et un fois dix puissance moins quatre an puissance moins un.",
                            "Oui ! λ = ln2/t½ ≈ 1,21·10⁻⁴ an⁻¹.")},
           "1": {"1": r("خديتي ln deux و t un demi، مزيان. ولكن ضربتي واحد فالآخر. la relation هي ln deux مقسوم على t un demi.",
                        "Tu as bien pris ln2 et t½, mais tu les as multipliés. La relation est λ = ln2/t½."),
                 "2": r("لا. lambda égale ln deux sur t un demi، ماشي fois. zéro virgule six cent quatre-vingt-treize sur cinq mille sept cent trente كيعطي un virgule vingt et un fois dix puissance moins quatre.",
                        "Non. λ = ln2/t½, pas ln2 × t½ : 0,693/5730 ≈ 1,21·10⁻⁴ an⁻¹.")},
           "2": {"1": r("العدد صحيح. ولكن شوف l'unité: t un demi مكتوب ب ans. إذن lambda ب شنو؟",
                        "Le nombre est juste. Mais regarde l'unité : t½ est donnée en ans. Alors λ est en quoi ?"),
                 "2": r("لا. t un demi ب ans، إذن lambda ب an puissance moins un، ماشي seconde. هنا ما خاصنا les secondes، حيت بغينا t ب ans.",
                        "Non. t½ est en ans, donc λ est en an⁻¹, pas en s⁻¹. Ici pas besoin de secondes : on veut t en ans.")}},
    "e1": {"0": {"juste": r("مزيان! t تقريبا deux mille deux cent soixante ans. الخشب عندو تقريبا deux mille deux cent soixante ans.",
                            "Oui ! t ≈ 2,26·10³ ans : le bois a environ 2 260 ans.")},
           "1": {"1": r("العدد قريب، ولكن عمر سالب؟ ما يمكنش. شوف: a zéro sur a، ماشي a sur a zéro.",
                        "Le nombre est bon, mais un âge négatif est impossible. Vérifie la fraction : a₀/a, pas a/a₀."),
                 "2": r("لا. ln de quatre cent dix-huit sur trois cent dix-huit positif، إذن t positif: تقريبا deux virgule vingt-six fois dix puissance trois ans.",
                        "Non. ln(418/318) est positif, donc t est positif : t ≈ 2,26·10³ ans.")},
           "2": {"1": r("حسبتي ln de a zéro sur a مزيان. ولكن ضربتي ف lambda. خاصك تقسم على lambda.",
                        "ln(a₀/a) est bien calculé. Mais tu as multiplié par λ : il faut diviser par λ."),
                 "2": r("لا. t égale un sur lambda fois ln de a zéro sur a: zéro virgule deux cent soixante-treize sur un virgule vingt et un fois dix puissance moins quatre، تقريبا deux mille deux cent soixante ans.",
                        "Non. t = ln(a₀/a)/λ = 0,273/(1,21·10⁻⁴) ≈ 2,26·10³ ans.")}},
}

X2_STEPS = {
    "question": {
        "type": "qcm",
        "prompt": "Étape 1 — Calcule λ du plutonium 238 en s⁻¹ (t½ = 88 ans ; 1 an ≈ 3,16·10⁷ s).",
        "options": ["λ ≈ 7,9·10⁻³ s⁻¹", "λ ≈ 2,49·10⁻¹⁰ s⁻¹", "λ ≈ 4,0·10⁹ s⁻¹"],
        "timeout_seconds": 30, "correct": 1,
        "enonce_dit": "الخطوة اللولى: calcule lambda du plutonium deux cent trente-huit، ب seconde puissance moins un. t un demi égale quatre-vingt-huit ans، و un an تقريبا trois virgule seize fois dix puissance sept secondes.",
        "demonstration": demo([
            ("a en Bq, donc λ en s⁻¹ : t½ en secondes", "l'activité ب becquerel"),
            ("t½ = 88 × 3,16·10⁷ s ≈ 2,78·10⁹ s", "t un demi égale quatre-vingt-huit fois"),
            ("λ = ln2/t½ = 0,693/(2,78·10⁹)", "lambda égale ln deux sur t un demi"),
            ("λ ≈ 2,49·10⁻¹⁰ s⁻¹", "le résultat")],
            "l'activité ب becquerel، إذن lambda خاصها ب seconde puissance moins un، و t un demi ب secondes. "
            "t un demi égale quatre-vingt-huit fois trois virgule seize fois dix puissance sept، يعني تقريبا deux "
            "virgule soixante-dix-huit fois dix puissance neuf secondes. lambda égale ln deux sur t un demi: zéro "
            "virgule six cent quatre-vingt-treize sur deux virgule soixante-dix-huit fois dix puissance neuf. "
            "le résultat: lambda تقريبا deux virgule quarante-neuf fois dix puissance moins dix seconde puissance moins un.")},
    "exercises_avant": [
        {"type": "qcm",
         "prompt": "Étape 2 — Calcule le nombre N₀ de noyaux à t = 0 (a₀ = 1,0·10¹¹ Bq).",
         "choices": ["N₀ ≈ 2,5·10¹", "N₀ ≈ 4,0·10²⁰", "N₀ ≈ 1,3·10¹³"],
         "correct": 1,
         "explanation": "a₀ = λ·N₀, donc N₀ = a₀/λ = 1,0·10¹¹/(2,49·10⁻¹⁰) ≈ 4,0·10²⁰ noyaux.",
         "enonce_dit": "الخطوة التانية: calcule N zéro، a zéro égale un fois dix puissance onze becquerels.",
         "demonstration": demo([
             ("a₀ = λ·N₀, donc N₀ = a₀/λ", "a zéro égale lambda N zéro"),
             ("N₀ = 1,0·10¹¹/(2,49·10⁻¹⁰)", "l'application numérique"),
             ("N₀ ≈ 4,0·10²⁰ noyaux", "le résultat")],
             "a zéro égale lambda N zéro، إذن N zéro égale a zéro sur lambda. l'application numérique: un fois dix "
             "puissance onze، sur deux virgule quarante-neuf fois dix puissance moins dix. le résultat: N zéro "
             "تقريبا quatre fois dix puissance vingt noyaux.")}],
}
X2_REPONSES = {
    "q": {"0": {"1": r("ln deux sur quatre-vingt-huit، مزيان. ولكن هادي ب an puissance moins un. l'activité ب becquerel: خاصك t un demi ب secondes.",
                       "ln2/88 est juste, mais c'est en an⁻¹. L'activité est en Bq : il faut t½ en secondes."),
                "2": r("لا. حولنا t un demi ل secondes: deux virgule soixante-dix-huit fois dix puissance neuf. lambda تقريبا deux virgule quarante-neuf fois dix puissance moins dix seconde puissance moins un.",
                       "Non. t½ = 2,78·10⁹ s, donc λ = 0,693/(2,78·10⁹) ≈ 2,49·10⁻¹⁰ s⁻¹.")},
          "1": {"juste": r("مزيان! بدلتي t un demi ل secondes، و lambda تقريبا deux virgule quarante-neuf fois dix puissance moins dix seconde puissance moins un.",
                           "Oui ! t½ en secondes, puis λ ≈ 2,49·10⁻¹⁰ s⁻¹.")},
          "2": {"1": r("بدلتي ل secondes، مزيان. ولكن قسمتي t un demi على ln deux. lambda هي ln deux على t un demi.",
                       "La conversion en secondes est bonne. Mais tu as fait t½/ln2 : λ = ln2/t½."),
                "2": r("لا. lambda égale ln deux sur t un demi، عدد صغير بزاف: تقريبا deux virgule quarante-neuf fois dix puissance moins dix seconde puissance moins un.",
                       "Non. λ = ln2/t½, un très petit nombre : ≈ 2,49·10⁻¹⁰ s⁻¹.")}},
    "e0": {"0": {"1": r("خديتي a zéro و lambda، مزيان. ولكن ضربتي واحد فالآخر. a zéro égale lambda N zéro، إذن N zéro هو a zéro مقسوم على lambda.",
                        "Tu utilises bien a₀ et λ, mais tu les as multipliés. a₀ = λ·N₀, donc N₀ = a₀/λ."),
                 "2": r("لا. N zéro égale a zéro sur lambda: تقريبا quatre fois dix puissance vingt noyaux.",
                        "Non. N₀ = a₀/λ ≈ 4,0·10²⁰ noyaux.")},
           "1": {"juste": r("مزيان! N zéro égale a zéro sur lambda، تقريبا quatre fois dix puissance vingt noyaux.",
                            "Oui ! N₀ = a₀/λ ≈ 4,0·10²⁰ noyaux.")},
           "2": {"1": r("la relation صحيحة، N zéro égale a zéro sur lambda. ولكن شوف lambda اللي خديتي: واش ب seconde puissance moins un؟",
                        "La relation N₀ = a₀/λ est juste. Mais quel λ as-tu pris ? Il doit être en s⁻¹."),
                 "2": r("لا. خاص lambda ب seconde puissance moins un، deux virgule quarante-neuf fois dix puissance moins dix. N zéro تقريبا quatre fois dix puissance vingt.",
                        "Non. Avec λ en s⁻¹ (2,49·10⁻¹⁰ s⁻¹) : N₀ ≈ 4,0·10²⁰.")}},
}

X2_REPONSES_E1 = {
    "0": {"1": r("trente pour cent désintégrés، مزيان. ولكن هادا ماشي trente pour cent ديال t un demi: la loi ماشي خط مستقيم. كتب الأول شحال بقا: soixante-dix pour cent، يعني N égale zéro virgule sept N zéro.",
                 "Ce n'est pas 30 % de t½ : la décroissance n'est pas une droite. Écris d'abord ce qui reste : N = 0,70·N₀."),
          "2": r("لا. كيبقى soixante-dix pour cent: N égale zéro virgule sept N zéro. t égale t un demi sur ln deux، fois ln de un sur zéro virgule sept: تقريبا quarante-cinq ans.",
                 "Non. Il reste 70 % : N = 0,70·N₀. t = (t½/ln2)·ln(1/0,70) = (88/0,693) × 0,357 ≈ 45 ans.")},
    "1": {"juste": r("مزيان! كيبقى soixante-dix pour cent، و t تقريبا quarante-cinq ans. وهادشي مزيان: قل من t un demi، حيت ما مشاش النص.",
                     "Oui ! Il reste 70 % et t ≈ 45 ans : c'est moins que t½, car moins de la moitié s'est désintégrée.")},
    "2": {"1": r("كيبان ليك وقت طويل. ولكن ف t un demi، quatre-vingt-huit ans، كيمشي النص. هنا غير trente pour cent: إذن t خاصو يكون قل من quatre-vingt-huit ans.",
                 "C'est trop long : en t½ = 88 ans, la moitié s'est déjà désintégrée. Ici seulement 30 % : t doit être plus petit que 88 ans."),
          "2": r("لا. كيبقى soixante-dix pour cent: t égale t un demi sur ln deux، fois ln de un sur zéro virgule sept، تقريبا quarante-cinq ans.",
                 "Non. Il reste 70 % : t = (t½/ln2)·ln(1/0,70) ≈ 45 ans.")},
}

D6_EXERCICE_CENTRE = [
    {"texte": "A = 241 − 241 = 0", "mot": "إذن A égale zéro"},
    {"texte": "Z = 94 − 95 = −1 : X = ⁰₋₁e", "mot": "إذن Z égale moins un"},
    {"texte": "²⁴¹₉₄Pu → ²⁴¹₉₅Am + ⁰₋₁e : β⁻", "mot": "إذن la désintégration هي bêta moins"},
]

# Réactions déjà écrites qui portaient des symboles ou des chiffres (la voix ne les lit pas) : réécrites en mots.
REACTIONS_EN_MOTS = {
    ("ra_t3_paliers", "q", "1", "1"): ("1/6", "un sixième"),
    ("ra_a2_definition", "q", "2", "1"): ("100 Bq", "cent becquerels"),
}
RAPPELS_EN_MOTS = {
    ("C4_r2", "1", "1"): ("²⁸₁₃Al", "l'aluminium vingt-huit"),
    ("C7_r2", "0", "1"): ("1/4", "un quart"),
    ("C8_r2", "0", "1"): ("j⁻¹", "jour puissance moins un"),
    ("C8_r2", "0", "2"): ("j⁻¹", "jour puissance moins un"),
}
POSITON = [("⁰ و e", "zéro و e"), ("⁰ ₁ e", "zéro، un، e"), ("⁰₁e", "zéro un e"), ("⁰₋₁e", "zéro moins un e")]


def main():
    m = json.load(open(SRC, encoding="utf-8"))
    S = {s["id"]: s for a in m["activities"] for s in a["slides"]}
    vieux_blocs = [b for se in m["seances"] for b in se["blocs"]]
    reecrites, nouvelles = [], []

    def sans_voix(s):
        s.pop("audio", None)
        reecrites.append(s["id"])

    # ra_l1_echantillon : la simulation n'écrit plus N₀/2 ni t½ (l'élève comptera à la diapositive suivante).
    s = S["ra_l1_echantillon"]
    s["visual"]["url"] = SIM + "population.html?vue=grand_nombre&conclusions=0"

    # ra_s5_isotopes_ligne : β⁻ n'est pas encore enseigné → « instable », annonce de la partie suivante.
    s = S["ra_s5_isotopes_ligne"]
    s["speech_text"]["mixed"] = S5_TEXTE
    s["speech_text"]["fr"] = ("Les isotopes ont le même Z : sur le diagramme, ils ont la même abscisse, sur une même verticale. "
                              "Le carbone 12 est dans la vallée : stable. Le carbone 14 est au-dessus : trop de neutrons, instable. "
                              "Comment le carbone 14 revient-il vers la vallée ? C'est la partie suivante.")
    s["screen_content"]["bullets"] = [b.replace("trop de neutrons, β⁻.", "trop de neutrons, instable.") for b in s["screen_content"]["bullets"]]
    sans_voix(s)

    # ra_p3_puissances : avancée avant le premier grand nombre (N₀ = 8,0·10²⁰ à la courbe de la demi-vie).
    s = S["ra_p3_puissances"]
    t = s["speech_text"]["mixed"]
    assert t.startswith(P3_TEXTE_DEBUT_ANCIEN)
    s["speech_text"]["mixed"] = (P3_TEXTE_DEBUT + t[len(P3_TEXTE_DEBUT_ANCIEN):]).replace("ومن بعدو شي zéros", "ومن بعد شي zéro")
    s["speech_text"]["fr"] = s["speech_text"].get("fr", "").replace("Avant de convertir, un petit rappel", "Un échantillon contient énormément de noyaux. Un petit rappel")
    sans_voix(s)

    # ra_d6_type : l'exemple du national 2018 R s'arrêtait sur « plus X » ; il va jusqu'au bout.
    s = S["ra_d6_type"]
    s["speech_text"]["mixed"] = s["speech_text"]["mixed"].rstrip() + D6_FIN
    s["concentration"]["centre"] = D6_EXERCICE_CENTRE
    sans_voix(s)

    # ra_c3_calcul : exercice du national 2022 R joué en trois étapes que l'élève fait lui-même.
    s = S["ra_c3_calcul"]
    s["speech_text"]["mixed"] = C3_TEXTE
    s["speech_text"]["fr"] = ("National 2022 R : un bois ancien a une activité de 318 Bq ; un bois récent de même masse, 418 Bq ; "
                              "t½ du carbone 14 = 5730 ans. Quel est l'âge du bois ? On le résout étape par étape, et c'est toi "
                              "qui fais chaque étape : la relation, puis λ, puis t.")
    s["title"] = "Dater un bois ancien, étape par étape (national 2022 R)"
    s["screen_content"] = {
        "lead": "Bois ancien : a = 318 Bq ; bois récent : a₀ = 418 Bq ; t½ = 5730 ans.",
        "bullets": ["Bois ancien : a = 318 Bq.", "Bois récent de même masse : a₀ = 418 Bq.", "Carbone 14 : t½ = 5730 ans.",
                    "Étape 1 : la relation ; étape 2 : λ ; étape 3 : t."],
        "student_trace": "t = (1/λ)·ln(a₀/a), λ = ln2/t½ = 1,21·10⁻⁴ an⁻¹ ; bois de 2022 R : t ≈ 2,26·10³ ans."}
    co = s["concentration"]
    co["demarrer"] = "reset"
    co["pointage"] = [{"mot": "عطاونا l'activité", "commande": "play_until", "parametres": {"moment": "mesure"}}]
    co["centre"] = [{"texte": "a = 318 Bq", "mot": "trois cent dix-huit becquerels"},
                    {"texte": "a₀ = 418 Bq", "mot": "quatre cent dix-huit becquerels"},
                    {"texte": "t½ = 5730 ans", "mot": "cinq mille sept cent trente ans"}]
    co["cahier"] = s["screen_content"]["student_trace"]
    co["reponses"] = C3_REPONSES
    s["question"] = C3_STEPS["question"]
    s["exercises"] = C3_STEPS["exercises"]
    sans_voix(s)

    # ra_x2_2021N : le national 2021 N n'avait pas de tableau ; trois étapes (λ en s⁻¹, N₀, l'âge pour 30 %).
    s = S["ra_x2_2021N"]
    s["question"] = X2_STEPS["question"]
    reserve = s.pop("exercices_fin_de_cours", [])
    s.pop("reponses_fin_de_cours", None)
    s["exercises"] = X2_STEPS["exercises_avant"] + reserve           # l'étape 3 (30 % désintégrés) vient de la réserve
    rep = dict(X2_REPONSES)
    rep["e1"] = X2_REPONSES_E1                                      # réactions de la réserve (jamais dites) réécrites en mots
    s["concentration"]["reponses"] = rep

    # ra_a5b_masse_inverse : sa question touchait celle de ra_a5_masse (deux tableaux de suite) → réserve de fin de cours.
    s = S["ra_a5b_masse_inverse"]
    q = s.pop("question")
    q.pop("prompt_dit", None)
    q2 = {k: v for k, v in q.items() if k != "options"}
    q2["choices"] = q["options"]
    s["exercices_fin_de_cours"] = [q2]
    s["reponses_fin_de_cours"] = {"e0": s["concentration"].get("reponses", {}).pop("q", {})}

    # Réactions préparées avec symboles → en mots (leur voix est à refaire).
    pistes_reactions = []
    for (sid, cle, opt, quoi), (a, b) in REACTIONS_EN_MOTS.items():
        rr = S[sid]["concentration"]["reponses"][cle][opt][quoi]
        assert a in rr["parole"], (sid, a)
        rr["parole"] = rr["parole"].replace(a, b); rr.pop("audio", None)
        pistes_reactions.append(("reponses", f"{sid}__{cle}_{opt}_{quoi}", rr["parole"]))
    rappels = {r_["id"]: r_ for c_ in m["competences"] for r_ in c_.get("rappels", [])}
    for (rid, opt, quoi), (a, b) in RAPPELS_EN_MOTS.items():
        rr = rappels[rid]["reponses"][opt][quoi]
        assert a in rr["parole"], (rid, a)
        rr["parole"] = rr["parole"].replace(a, b); rr.pop("audio", None)
        pistes_reactions.append(("reponses", f"rappel_{rid}_{opt}_{quoi}", rr["parole"]))
    for opt, quoi in (("0", "1"), ("0", "2"), ("1", "juste")):
        rr = rappels["C4_r4"]["reponses"][opt][quoi]
        avant = rr["parole"]
        for a, b in POSITON:
            rr["parole"] = rr["parole"].replace(a, b)
        if rr["parole"] != avant:
            rr.pop("audio", None)
            pistes_reactions.append(("reponses", f"rappel_C4_r4_{opt}_{quoi}", rr["parole"]))

    S["ra_l1b_moitie"] = copy.deepcopy(L1B)
    nouvelles.append("ra_l1b_moitie")

    # ── Parties, séances, blocs, compétences dans le nouvel ordre ──
    ordre = [i for p in PARTIES for i in p[4]]
    assert sorted(ordre) == sorted(S), set(S) ^ set(ordre)
    m["activities"] = [{"id": pid, "title": t, "phase": ph, "duration_minutes": d, "slides": [S[i] for i in ids]}
                       for pid, t, ph, d, ids in PARTIES]
    blocs_ordre = [i for _, _, bl in SEANCES for _, _, ids in bl for i in ids]
    assert blocs_ordre == ordre, "les blocs doivent suivre l'ordre des diapositives"
    nouvelles_seances = []
    for sid, titre, bl in SEANCES:
        blocs = []
        for bid, bt, ids in bl:
            vieux = max(vieux_blocs, key=lambda b: len(set(b["slide_ids"]) & set(ids)))
            figs = [f for i in ids for f in (S[i]["concentration"].get("cahier_figures") or [])][:2]
            b = {"id": bid, "titre": bt, "slide_ids": ids,
                 "cahier": [{"texte": S[i]["concentration"]["cahier"]} for i in ids if S[i]["concentration"].get("cahier")]}
            if figs:
                b["cahier_figures"] = figs
            for k in ("retrouver", "exercice"):
                if vieux.get(k):
                    b[k] = copy.deepcopy(vieux[k])
            blocs.append(b)
        nouvelles_seances.append({"id": sid, "titre": titre, "blocs": blocs})
    m["seances"] = nouvelles_seances
    for c_ in m["competences"]:
        c_["slide_ids"] = [i for i in ordre if c_["id"] in (S[i].get("competence_ids") or [])]
    m["estimated_minutes"] = sum(p[3] for p in PARTIES)
    m["note"] = (m.get("note", "") + " Logique refaite le 18 novembre 2026 (skill logique-de-cours) : "
                 "backend/data/curriculum/architecture/phys_ch4_radioactivite.md.").strip()

    os.makedirs(os.path.dirname(DST), exist_ok=True)
    json.dump(m, open(DST, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(DST, "a", encoding="utf-8").write("\n")
    return m, reecrites, nouvelles, pistes_reactions


if __name__ == "__main__":
    m, reecrites, nouvelles, pr = main()
    print("écrit :", DST)
    print("réécrites :", reecrites, "; nouvelles :", nouvelles, "; réactions en mots :", len(pr))
