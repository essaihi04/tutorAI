"""Nouvelle logique de math_ch1_limites_continuite (architecture : backend/data/curriculum/architecture/
math_ch1_limites_continuite.md). Écrit les diapositives réécrites ou nouvelles, puis la spécification pour
reordonner.py. Rejouable : part toujours du cours en attente tel qu'il est."""
import copy, json, os, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..")
DECK = "math_ch1_limites_continuite"
CH = os.path.join(RACINE, "backend/data/courses/en_attente", DECK + ".json")
SIM = "/media/simulations/maths/limites-continuite-tableau/"
d = json.load(open(CH, encoding="utf-8"))
S = {s["id"]: s for a in d["activities"] for s in a["slides"]}


def texte(s, fr, mixed):
    s["speech_text"] = {"fr": fr, "mixed": mixed}
    s.pop("audio", None)          # texte changé : voix à refaire


# 1. z5 vient maintenant juste avant le facteur (x − a) : ce n'est plus « la dernière base ».
z5 = S["lc_z5_racine_facteur"]
if z5["speech_text"]["mixed"].startswith("آخر حاجة من الأساس"):
    texte(z5, z5["speech_text"]["fr"].replace("Dernière base :", "Une autre base :", 1),
          z5["speech_text"]["mixed"].replace("آخر حاجة من الأساس", "حاجة أخرى من الأساس", 1))

# 2. Le problème national joué question par question : la réponse de l'élève avant la correction.
e1 = S["lc_e1_probleme"]
if e1.get("exercises"):
    ex_tvi = e1.pop("exercises")[0]
    rep_tvi = e1["concentration"]["reponses"].pop("e0")
    q_rec = e1.pop("exercices_fin_de_cours")[0]
    rep_rec = e1.pop("reponses_fin_de_cours")["e1"]
else:                                   # déjà fait : on relit les questions posées
    ex_tvi, rep_tvi = None, None
e1["screen_content"]["bullets"] = [
    "f(x) = x³ + x − 1 sur ℝ.",
    "Quatre questions, une à la fois : limites, sens de variation, solution unique α, réciproque.",
    "Question 1 : à l'infini, le terme de plus haut degré."]

b = S["lc_e1_probleme_b"]
if ex_tvi is not None:
    b["title"] = "Question 2 : le sens de variation"
    b["screen_content"] = {
        "lead": "f′(x), puis son signe.",
        "bullets": ["f′(x) = 3x² + 1.", "x² ≥ 0 : quel est le signe de 3x² + 1 ?"],
        "student_trace": "f′(x) = 3x² + 1 > 0 car x² ≥ 0 : f est strictement croissante sur ℝ."}
    b["visual"] = {"kind": "simulation", "url": SIM + "calculs.html?vue=e1_q2",
                   "caption": "La dérivée, ligne par ligne",
                   "alt": "f′(x) = 3x² + 1 écrit à la craie, puis x² ≥ 0 souligné"}
    texte(b,
          "Question deux : le sens de variation. Pour savoir si f monte ou descend, on calcule sa dérivée. "
          "f prime de x égale trois x carré plus un. Regarde x carré : peut-il être négatif ? Réfléchis. "
          "Question : quel est le signe de f prime de x ?",
          "السؤال الثاني: le sens de variation. باش نعرفو واش f كطلع ولا كتهبط، كنحسبو la dérivée. "
          "f prime de x égale trois x carré plus un. شوف x carré: واش يقدر يكون négatif؟ فكر شوية. "
          "سؤال: شنو هو le signe ديال f prime de x؟")
    b["question"] = {
        "type": "qcm", "prompt": "f′(x) = 3x² + 1. Sur ℝ :",
        "options": ["f′(x) < 0", "f′(x) > 0", "f′ change de signe en 0"], "correct": 1, "timeout_seconds": 40,
        "enonce_dit": "شوف هاد السؤال: f prime de x égale trois x carré plus un. شنو هو le signe ديالها sur R ؟",
        "demonstration": {
            "parole": "x carré دايما positif ولا zéro. إذن trois x carré positif ولا zéro. "
                      "زيد un: trois x carré plus un, أكبر من un، إذن positif. "
                      "f prime positive sur R، إذن f strictement croissante sur R. "
                      "فـ le tableau: f كطلع من moins l'infini حتى لـ plus l'infini.",
            "lignes": [
                {"texte": "Pour tout x ∈ ℝ : x² ≥ 0", "mot": "x carré دايما"},
                {"texte": "donc 3x² ≥ 0", "mot": "إذن trois x carré"},
                {"texte": "donc f′(x) = 3x² + 1 ≥ 1 > 0", "mot": "زيد un:"},
                {"texte": "f′(x) > 0 sur ℝ, donc f est strictement croissante sur ℝ.", "mot": "f prime positive"},
                {"texte": "x : −∞ → +∞ ; f′(x) : + ; f : −∞ ↗ +∞", "mot": "فـ le tableau:"}]}}
    b["concentration"] = {
        "demarrer": "start",
        "pointage": [
            {"mot": "كنحسبو la dérivée.", "commande": "play_until", "parametres": {"moment": "derivee"}},
            {"mot": "شوف x carré:", "commande": "play_until", "parametres": {"moment": "carre"}}],
        "cahier": "f′(x) = 3x² + 1 > 0 car x² ≥ 0 : f est strictement croissante sur ℝ.",
        "reponses": {}}
    b["competence_ids"] = ["K5"]

    t = copy.deepcopy(b)
    t["id"] = "lc_e1_probleme_tvi"
    t["title"] = "Question 3 : la solution unique α, et sa place"
    t["screen_content"] = {
        "lead": "Continue, strictement croissante : une seule traversée.",
        "bullets": ["f est continue sur ℝ car c'est un polynôme ; f est strictement croissante.",
                    "On donne f(1/2) = −3/8 et f(1) = 1 : où est α ?"],
        "student_trace": "f continue et strictement croissante sur [1/2 ; 1], f(1/2) × f(1) < 0 : "
                         "solution unique α et 1/2 < α < 1."}
    t["visual"] = {"kind": "simulation", "url": SIM + "traversee.html?vue=alpha",
                   "caption": "La courbe de x³ + x − 1 traverse l'axe une fois",
                   "alt": "La courbe de f monte et coupe l'axe des abscisses en un seul point α"}
    texte(t,
          "Question trois : la solution unique. On a déjà les deux outils. f est continue sur R, car c'est un "
          "polynôme. Et f est strictement croissante. Regarde la courbe : elle part d'en bas et monte sans "
          "revenir. Elle coupe l'axe une seule fois, en alpha. Maintenant on la place. On donne f de un demi "
          "égale moins trois sur huit, et f de un égale un. Question : où est alpha ?",
          "السؤال الثالث: la solution unique. عندنا جوج ديال les conditions. f continue sur R، حيت polynôme. "
          "وf strictement croissante. شوف la courbe: كتبدا من لتحت وكطلع بلا ما ترجع. "
          "كتقطع l'axe مرة وحدة، ف alpha. دابا نلقاو البلاصة ديالها. "
          "عطاونا f de un demi égale moins trois sur huit، وf de un égale un. سؤال: فين كاينة alpha؟")
    q = dict(ex_tvi)
    q["options"] = q.pop("choices")
    q["timeout_seconds"] = 40
    q.pop("explanation", None)
    t["question"] = q
    t["concentration"] = {
        "demarrer": "start",
        "pointage": [
            {"mot": "شوف la courbe:", "commande": "play_until", "parametres": {"moment": "courbe_tracee"}},
            {"mot": "كتقطع l'axe مرة وحدة", "commande": "play_until", "parametres": {"moment": "alpha_nomme"}}],
        "cahier": t["screen_content"]["student_trace"],
        "reponses": {"q": rep_tvi}}

    c = S["lc_e1_probleme_c"]
    c["title"] = "Question 4 : la fonction réciproque"
    c["screen_content"] = {
        "lead": "Deux conditions, puis J = f(ℝ).",
        "bullets": ["f est continue et strictement croissante sur ℝ.",
                    "lim_{x→−∞} f(x) = −∞ ; lim_{x→+∞} f(x) = +∞ : J = ?"],
        "student_trace": "f continue et strictement croissante sur ℝ : f admet une fonction réciproque f⁻¹ "
                         "définie sur J = f(ℝ) = ℝ ; dans un repère orthonormé, (C_f⁻¹) est la symétrique de "
                         "(C_f) par rapport à la droite d'équation y = x."}
    c["visual"] = {"kind": "simulation", "url": SIM + "calculs.html?vue=e1_q4",
                   "caption": "Les deux conditions, puis l'intervalle J",
                   "alt": "Continue, strictement croissante, puis les deux limites écrites à la craie"}
    texte(c,
          "Question quatre : la fonction réciproque. f est continue et strictement croissante sur R. "
          "Pour trouver J, on prend les limites : en moins l'infini, moins l'infini ; en plus l'infini, plus "
          "l'infini. Question : sur quel ensemble la réciproque de f est-elle définie ?",
          "السؤال الرابع: la fonction réciproque. f continue وstrictement croissante sur R. "
          "باش نلقاو J، كناخدو les limites: فـ moins l'infini، moins l'infini؛ فـ plus l'infini، plus l'infini. "
          "سؤال: فين كتكون définie la réciproque ديال f؟")
    q = dict(q_rec)
    q["options"] = q.pop("choices")
    q.pop("explanation", None)
    q["timeout_seconds"] = 40
    q["demonstration"] = {
        "parole": "f continue sur R حيت polynôme، وstrictement croissante حيت f prime positive. "
                  "إذن f admet une fonction réciproque, définie sur J égale f de R. "
                  "f croissante: J كيبدا من la limite فـ moins l'infini، وكيسالي فـ la limite فـ plus l'infini. "
                  "يعني moins l'infini, plus l'infini، هي R. إذن J égale R. "
                  "وla courbe ديال f moins un, symétrique, par rapport à la droite y égale x.",
        "lignes": [
            {"texte": "f est continue sur ℝ (polynôme) et strictement croissante sur ℝ (f′(x) > 0)", "mot": "f continue sur R"},
            {"texte": "donc f admet une fonction réciproque f⁻¹ définie sur J = f(ℝ)", "mot": "إذن f admet"},
            {"texte": "f croissante : J = ]lim_{x→−∞} f(x) ; lim_{x→+∞} f(x)[", "mot": "f croissante:"},
            {"texte": "J = ]−∞ ; +∞[ = ℝ", "mot": "يعني moins l'infini"},
            {"texte": "Dans un repère orthonormé, (C_f⁻¹) est la symétrique de (C_f) par rapport à la droite d'équation y = x.", "mot": "وla courbe ديال"}]}
    c["question"] = q
    c["concentration"] = {
        "demarrer": "start",
        "pointage": [
            {"mot": "f continue وstrictement", "commande": "play_until", "parametres": {"moment": "conditions"}},
            {"mot": "كناخدو les limites:", "commande": "play_until", "parametres": {"moment": "limites"}}],
        "cahier": c["screen_content"]["student_trace"],
        "reponses": {"q": rep_rec}}
    c["competence_ids"] = ["K7"]
    NOUVELLES = {"lc_e1_probleme_tvi": t}
else:
    NOUVELLES = {}

# 3. Bilan et carte : pas de ligne sur ce qui est retiré (a³ − b³, comparer, équations avec racine).
bl = S["lc_e2_bilan"]["screen_content"]["bullets"]
for i, x in enumerate(bl):
    if x.startswith("8. Racine"):
        bl[i] = ("8. Racine n-ième (n ∈ ℕ*) : ⁿ√x = y ⇔ x = yⁿ (x, y ≥ 0) ; ⁿ√x × ⁿ√y = ⁿ√(x·y) ; "
                 "x^(p/q) = ᑫ√(xᵖ) (x > 0) ; ⁿ√u continue si u est continue et positive. ⚠ Rien de négatif sous ⁿ√.")
open(CH, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")

PARTIES = [
    ("lc_ouverture", "Ouverture — six questions sur une courbe", "situation", ["lc_o1_carte"]),
    ("lc_partie1", "I. Calculer une limite (rappel de 1re bac)", "explanation", [
        "lc_l1_chemin", "lc_l2_remplacer", "lc_l3_zero_sur_zero", "lc_l4_formes", "lc_l4_formes_b",
        "lc_l4c_usuelles", "lc_z1_factoriser", "lc_z5_racine_facteur", "lc_l5_facteur", "lc_l6_conjugue",
        "lc_l7_plus_lourd", "lc_z4_valeur_absolue", "lc_l8_racine_infini", "lc_l8_racine_infini_b",
        "lc_l9_deux_cotes", "lc_l10_signe", "lc_l11_interpreter", "lc_l12_sinus", "lc_l12_sinus_b",
        "lc_l13_devoir"]),
    ("lc_partie2", "II. Continuité en un point", "explanation", [
        "lc_c1_soudee", "lc_c2_limite_image", "lc_c3_deux_branches", "lc_c4_parametre", "lc_c4b_droite_gauche",
        "lc_c5_redaction"]),
    ("lc_partie3", "III. Continuité sur un intervalle", "explanation", [
        "lc_i1_usuelles", "lc_i2_operations", "lc_i3_racine_u", "lc_i4_composee"]),
    ("lc_partie4", "IV. Image d'un intervalle", "explanation", [
        "lc_z3_derivee", "lc_j1_hauteurs", "lc_j2_croissante", "lc_j3_decroissante", "lc_j4_borne_ouverte",
        "lc_j5_non_monotone"]),
    ("lc_partie5", "V. Le théorème des valeurs intermédiaires", "explanation", [
        "lc_t1_couper_axe", "lc_t2_continue", "lc_t3_produit", "lc_t4_au_moins_une", "lc_t5_unique",
        "lc_t6_rediger", "lc_t7_valeur_k", "lc_t8_intervalle_ouvert", "lc_t9_f_alpha"]),
    ("lc_partie7", "VI. La fonction réciproque", "explanation", [
        "lc_r1_aller_retour", "lc_r2_strictement_monotone", "lc_r3_J", "lc_r4_deux_lignes", "lc_r5_sens",
        "lc_r6_miroir", "lc_r7_construire", "lc_r8_expression", "lc_r9_valeur_absolue",
        "lc_r9_valeur_absolue_b"]),
    ("lc_partie8", "VII. Racine n-ième et puissances rationnelles", "explanation", [
        "lc_n1_defaire", "lc_n2_reciproque_xn", "lc_n3_regles", "lc_n4_simplifier", "lc_n6_equation",
        "lc_n6_equation_b", "lc_p1_exposant", "lc_p2_pq", "lc_p3_regles_puissances"]),
    ("lc_partie9", "VIII. Limites et continuité avec ⁿ√u", "application", [
        "lc_lr1_continuite", "lc_lr4_infini"]),
    ("lc_bilan", "IX. Un problème national, question par question, et le bilan", "evaluation", [
        "lc_e1_probleme", "lc_e1_probleme_b", "lc_e1_probleme_tvi", "lc_e1_probleme_c", "lc_e2_bilan",
        "lc_e3_carte"]),
]
SEANCES = [
    ("lc_s1", "Séance 1 — Calculer une limite : remplacer, nommer la forme, choisir l'outil", [
        ("lc_s1_b1", "La carte ; où mène le chemin ; je remplace d'abord", ["lc_o1_carte", "lc_l1_chemin", "lc_l2_remplacer"]),
        ("lc_s1_b2", "0/0 n'est pas une réponse ; les quatre formes", ["lc_l3_zero_sur_zero", "lc_l4_formes", "lc_l4_formes_b"]),
        ("lc_s1_b3", "Limites usuelles ; a² − b² ; une racine donne le facteur", ["lc_l4c_usuelles", "lc_z1_factoriser", "lc_z5_racine_facteur"]),
        ("lc_s1_b4", "Le facteur (x − a), le conjugué, le plus haut degré", ["lc_l5_facteur", "lc_l6_conjugue", "lc_l7_plus_lourd"])]),
    ("lc_s2", "Séance 2 — À l'infini, à droite, à gauche ; continuité en un point", [
        ("lc_s2_b1", "√(x²) = |x| ; racine à l'infini", ["lc_z4_valeur_absolue", "lc_l8_racine_infini", "lc_l8_racine_infini_b"]),
        ("lc_s2_b2", "Par la droite, par la gauche ; interpréter", ["lc_l9_deux_cotes", "lc_l10_signe", "lc_l11_interpreter"]),
        ("lc_s2_b3", "sin(x)/x ; à toi : des limites", ["lc_l12_sinus", "lc_l12_sinus_b", "lc_l13_devoir"]),
        ("lc_s2_b4", "Continue en a : la limite égale l'image", ["lc_c1_soudee", "lc_c2_limite_image", "lc_c3_deux_branches"])]),
    ("lc_s3", "Séance 3 — Continuité et image d'un intervalle", [
        ("lc_s3_b0", "Souder la courbe, à droite et à gauche, rédiger", ["lc_c4_parametre", "lc_c4b_droite_gauche", "lc_c5_redaction"]),
        ("lc_s3_b1", "Les fonctions usuelles, les opérations, √u", ["lc_i1_usuelles", "lc_i2_operations", "lc_i3_racine_u"]),
        ("lc_s3_b2", "Limite d'une composée ; le signe de f′ ; les hauteurs atteintes", ["lc_i4_composee", "lc_z3_derivee", "lc_j1_hauteurs"]),
        ("lc_s3_b3", "Image d'un intervalle : même ordre, ordre inversé, borne ouverte", ["lc_j2_croissante", "lc_j3_decroissante", "lc_j4_borne_ouverte", "lc_j5_non_monotone"])]),
    ("lc_s4", "Séance 4 — Le théorème des valeurs intermédiaires", [
        ("lc_s4_b1", "Couper l'axe ; continue ; une image dessous, une dessus", ["lc_t1_couper_axe", "lc_t2_continue", "lc_t3_produit"]),
        ("lc_s4_b2", "Au moins une solution, puis unique ; rédiger", ["lc_t4_au_moins_une", "lc_t5_unique", "lc_t6_rediger"]),
        ("lc_s4_b3", "Toute valeur k ; intervalle ouvert ; f(α) = 0", ["lc_t7_valeur_k", "lc_t8_intervalle_ouvert", "lc_t9_f_alpha"])]),
    ("lc_s5", "Séance 5 — La fonction réciproque", [
        ("lc_s5_b1", "Aller et retour ; strictement monotone ; J = f(I)", ["lc_r1_aller_retour", "lc_r2_strictement_monotone", "lc_r3_J"]),
        ("lc_s5_b2", "Deux lignes au national ; même sens ; le miroir", ["lc_r4_deux_lignes", "lc_r5_sens", "lc_r6_miroir"]),
        ("lc_s5_b3", "Construire la courbe ; l'expression de f⁻¹", ["lc_r7_construire", "lc_r8_expression", "lc_r9_valeur_absolue", "lc_r9_valeur_absolue_b"])]),
    ("lc_s6", "Séance 6 — Racine n-ième, puissances rationnelles", [
        ("lc_s6_b1", "Défaire la puissance n ; ⁿ√ réciproque de xⁿ ; les règles", ["lc_n1_defaire", "lc_n2_reciproque_xn", "lc_n3_regles"]),
        ("lc_s6_b2", "Simplifier ; résoudre xⁿ = a", ["lc_n4_simplifier", "lc_n6_equation", "lc_n6_equation_b"]),
        ("lc_s6_b3", "Puissances rationnelles et leurs règles", ["lc_p1_exposant", "lc_p2_pq", "lc_p3_regles_puissances"]),
        ("lc_s6_b4", "Continuité et limites avec ⁿ√u", ["lc_lr1_continuite", "lc_lr4_infini"])]),
    ("lc_s7", "Séance 7 — Un problème national, question par question ; le bilan", [
        ("lc_s7_b1", "Le problème national : quatre questions, ta réponse avant la correction", ["lc_e1_probleme", "lc_e1_probleme_b", "lc_e1_probleme_tvi", "lc_e1_probleme_c"]),
        ("lc_s7_b4", "Ce qu'il faut retenir, la carte", ["lc_e2_bilan", "lc_e3_carte"])]),
]
RETIREES = {
    "lc_z2_signe": "doublon de lc_l9_deux_cotes et lc_l10_signe (même signe de x − 1 près de 1, mêmes nombres 1,1 et 1,01) : le signe s'apprend là où il sert",
    "lc_n5_comparer": "comparer deux racines d'indices différents : exercice de devoir, absent du cadre (fonction_reciproque) et des 20 sujets",
    "lc_n7_equation_racine": "équation avec racine cubique : exercice de devoir ; xⁿ = a (lc_n6) couvre la notion",
    "lc_lr2_cle_de_trois": "a³ − b³ et la « clé de trois » : formule absente du cadre et des 20 sujets, seulement aux devoirs",
    "lc_lr3_zero_sur_zero": "0/0 avec racine cubique par a³ − b³ : même raison que lc_lr2",
}
spec = {"deck": DECK, "nouvelles": NOUVELLES, "retirees": RETIREES,
        "parties": [{"id": i, "title": t, "phase": ph, "slides": s} for i, t, ph, s in PARTIES],
        "seances": [{"id": i, "titre": t, "blocs": [{"id": bi, "titre": bt, "slides": bs} for bi, bt, bs in bl]}
                    for i, t, bl in SEANCES]}
p = os.path.join(ICI, "spec_" + DECK + ".json")
open(p, "w", encoding="utf-8").write(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
subprocess.run([sys.executable, os.path.join(ICI, "reordonner.py"), p], check=True)
os.remove(p)

# 4. Après le recoupage : les fins de bloc ne renvoient plus à une diapositive retirée ni à une notion pas encore vue.
d = json.load(open(CH, encoding="utf-8"))
blocs = {b["id"]: b for se in d["seances"] for b in se["blocs"]}
blocs["lc_s1_b3"]["exercice"] = {
    "type": "qcm", "prompt": "P(x) = x² − 5x + 6 et P(2) = 0. Alors :",
    "options": ["P(x) = (x + 2)(x + 3)", "P(x) = (x − 2)(x − 3)", "P(x) = (x − 2)(x + 3)"], "correct": 1,
    "timeout_seconds": 40,
    "enonce_dit": "شوف هاد السؤال: P de x égale x carré moins cinq x plus six، وP de deux égale zéro. شنو هي la factorisation ديال P de x؟",
    "demonstration": {
        "parole": "P de deux égale zéro، إذن x moins deux facteur ديال P de x. P de x égale x moins deux، fois x plus b. "
                  "كنقارنو le terme constant: moins deux fois b égale six، إذن b égale moins trois. "
                  "كنتأكدو: x moins deux، fois x moins trois، égale x carré moins cinq x plus six. إذن P de x égale x moins deux، fois x moins trois.",
        "lignes": [
            {"texte": "P(2) = 4 − 10 + 6 = 0, donc (x − 2) est un facteur de P(x)", "mot": "P de deux égale zéro"},
            {"texte": "P(x) = (x − 2)(x + b)", "mot": "P de x égale x moins deux، fois x plus b"},
            {"texte": "Terme constant : −2b = 6, donc b = −3", "mot": "كنقارنو le terme constant"},
            {"texte": "Vérification : (x − 2)(x − 3) = x² − 3x − 2x + 6 = x² − 5x + 6", "mot": "كنتأكدو"},
            {"texte": "Donc P(x) = (x − 2)(x − 3).", "mot": "إذن P de x égale x moins deux، fois x moins trois"}]}}
blocs["lc_s6_b4"]["retrouver"] = {
    "prompt": "Cahier fermé : à quelle condition ⁿ√u est-elle continue sur I ?",
    "attendu": "ⁿ√u est continue sur I si u est continue et positive sur I.", "competence_id": "K10",
    "enonce_dit": "سؤال: cahier fermé، إمتى كتكون racine n-ième de u continue sur I؟"}
blocs["lc_s6_b4"]["exercice"] = {
    "type": "qcm", "prompt": "lim_{x→+∞} ∛(x + 8) = ?", "options": ["2", "+∞", "0"], "correct": 1,
    "timeout_seconds": 40,
    "enonce_dit": "شوف هاد السؤال: شنو هي la limite ديال racine cubique de x plus huit، quand x tend vers plus l'infini؟",
    "demonstration": {
        "parole": "u de x égale x plus huit، كيمشي ل plus l'infini. وملي u كيمشي ل plus l'infini، racine cubique de u كتمشي حتى هي ل plus l'infini. "
                  "إذن la limite égale plus l'infini.",
        "lignes": [
            {"texte": "u(x) = x + 8 : lim_{x→+∞} u(x) = +∞", "mot": "u de x égale x plus huit"},
            {"texte": "Si lim u = +∞, alors lim ∛u = +∞", "mot": "وملي u كيمشي"},
            {"texte": "Donc lim_{x→+∞} ∛(x + 8) = +∞.", "mot": "إذن la limite"}]}}
for c in d["competences"]:
    c["rappels"] = [r for r in c.get("rappels", []) if "a³" not in r.get("prompt", "")]
open(CH, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
