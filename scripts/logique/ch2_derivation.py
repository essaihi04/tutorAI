"""Nouvelle logique de math_ch2_derivation_etude_fonctions (architecture : backend/data/curriculum/architecture/
math_ch2_derivation_etude_fonctions.md). Rejouable depuis la copie en attente d'avant."""
import copy, json, os, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..")
DECK = "math_ch2_derivation_etude_fonctions"
CH = os.path.join(RACINE, "backend/data/courses/en_attente", DECK + ".json")
d = json.load(open(CH, encoding="utf-8"))
S = {s["id"]: s for a in d["activities"] for s in a["slides"]}
NOUVELLES = {}


def texte(s, fr, mixed):
    s["speech_text"] = {"fr": fr, "mixed": mixed}
    s.pop("audio", None)


def vers_reserve(s):
    """La question d'un rappel va dans la réserve de fin de cours : un seul « À toi » par bloc."""
    q = s.pop("question")
    q["choices"] = q.pop("options")
    s.setdefault("exercices_fin_de_cours", []).append(q)
    rep = s["concentration"].get("reponses", {}).pop("q", None)
    if rep:
        s.setdefault("reponses_fin_de_cours", {})["e%d" % (len(s["exercices_fin_de_cours"]) - 1)] = rep


def de_reserve(s, i, cle):
    """Une question de la réserve redevient la question de la diapositive, avec ses réactions."""
    q = s["exercices_fin_de_cours"].pop(i)
    q["options"] = q.pop("choices")
    q.pop("explanation", None)
    q.setdefault("timeout_seconds", 40)
    rep = s.get("reponses_fin_de_cours", {}).pop(cle, None)
    if not s.get("exercices_fin_de_cours"):
        s.pop("exercices_fin_de_cours", None)
        s.pop("reponses_fin_de_cours", None)
    return q, rep


# 1. Rappels déplacés là où ils servent : leurs mots d'ordre changent.
z5 = S["df_z5_un_sur_x"]
if z5["speech_text"]["mixed"].startswith("آخر حاجة:"):
    texte(z5, z5["speech_text"]["fr"].replace("Dernier rappel :", "Un rappel :", 1),
          z5["speech_text"]["mixed"].replace("آخر حاجة:", "واحد التذكير:", 1))
    vers_reserve(z5)
dv1 = S["df_dv1_tableau"]
if dv1["speech_text"]["mixed"].startswith("فالبداية ديال الدرس، شفنا"):
    texte(dv1, dv1["speech_text"]["fr"].replace("Au début du cours, on a dérivé les polynômes.",
                                                "On vient de dériver les polynômes.", 1),
          dv1["speech_text"]["mixed"].replace("فالبداية ديال الدرس، شفنا كيفاش نشتقو polynôme.",
                                              "دابا شفنا كيفاش نشتقو polynôme.", 1))
    for q in dv1["concentration"]["pointage"]:
        if q["mot"] == "فالبداية ديال الدرس،":
            q["mot"] = "دابا شفنا كيفاش"

# 2. L'étude complète jouée étape par étape : chaque étape demandée à l'élève avant sa correction.
e = S["df_ec3_etude"]
if "question" not in e:
    fr_ancien, mx_ancien = e["speech_text"]["fr"], e["speech_text"]["mixed"]
    pt_ancien = e["concentration"]["pointage"]
    q_dom, rep_dom = de_reserve(e, 1, "q")          # l'ensemble de définition
    q_br, rep_br = de_reserve(e, 0, "e1")           # interpréter lim f(x)/x = +∞
    e["question"] = q_dom
    e["concentration"]["reponses"] = {"q": rep_dom}
    e["title"] = "Une étude complète, pas à pas : l'ensemble de définition"
    e["screen_content"] = {
        "lead": "Une étude se fait une question à la fois.",
        "bullets": ["f(x) = x√(x + 1).", "Étape 1 : sous la racine, positif ou nul. Df = ?"],
        "student_trace": "f(x) = x√(x + 1) : f(x) existe si x + 1 ≥ 0, donc Df = [−1 ; +∞["}
    texte(e,
          "Une étude complète rassemble tout, mais pas à pas. f de x égale x racine de x plus un. Étape un, "
          "l'ensemble de définition : ce qui est sous la racine doit être positif ou nul. À toi : quel est "
          "l'ensemble de définition de f ?",
          "دراسة كاملة، كنجمعو فيها كلشي، ولكن خطوة بخطوة. f de x égale x racine de x plus un. "
          "الخطوة اللولة، المجموعة ديال التعريف: اللي تحت la racine خاصو يكون positif ولا zéro. "
          "دابا نتا: شنو هي المجموعة ديال التعريف ديال f؟")
    e["concentration"]["pointage"] = [pt_ancien[0]]
    e["concentration"]["cahier"] = e["screen_content"]["student_trace"]

    a2 = copy.deepcopy(e)
    a2["id"] = "df_ec3_etude_a2"
    a2.pop("question")
    a2["concentration"]["reponses"] = {}
    a2.pop("exercices_fin_de_cours", None)
    a2.pop("reponses_fin_de_cours", None)
    a2["title"] = "Une étude complète, pas à pas : le bord −1"
    a2["screen_content"] = {
        "lead": "Étape 2 : dérivable à droite en −1 ?",
        "bullets": ["Taux en −1 à droite : x√(x + 1)/(x + 1) = x/√(x + 1).",
                    "x → −1 et √(x + 1) → 0⁺, donc le taux → −∞ : pas dérivable à droite en −1.",
                    "Demi-tangente verticale en (−1 ; 0), dirigée vers le bas."],
        "student_trace": "En −1 à droite, le taux x/√(x + 1) → −∞ : f n'est pas dérivable à droite en −1 ; "
                         "demi-tangente verticale vers le bas en (−1 ; 0)."}
    a2["speech_text"] = {"fr": fr_ancien[fr_ancien.index("Étape 2"):],
                         "mixed": mx_ancien[mx_ancien.index("الخطوة الثانية،"):]}
    a2["concentration"]["pointage"] = pt_ancien[1:]
    a2["concentration"]["cahier"] = a2["screen_content"]["student_trace"]
    a2["competence_ids"] = ["K1", "K2", "K9"]
    NOUVELLES["df_ec3_etude_a2"] = a2

    c = S["df_ec3_etude_c"]
    c["title"] = "Une étude complète, pas à pas : le minimum, O, la branche infinie"
    c["screen_content"]["bullets"] = [
        "f′ négative puis positive : minimum f(−2/3) = (−2/3)·√(1/3) = −2/(3√3) = −2√3/9.",
        "f(0) = 0 : la courbe passe par O.",
        "En +∞ : lim_{x→+∞} f(x)/x = lim_{x→+∞} √(x + 1) = +∞. Quelle branche ?"]
    texte(c,
          "On l'a vu : f prime est négative avant moins deux tiers, et positive après. Donc f de moins deux tiers "
          "est le minimum. Étape quatre : f de zéro égale zéro, la courbe passe par O. Étape cinq, en plus "
          "l'infini : f de x sur x égale racine de x plus un, qui tend vers plus l'infini. Question : que veut "
          "dire cette limite ?",
          "شفنا: f prime négative قبل moins deux tiers، و positive من بعد. إذن f de moins deux tiers هو le minimum. "
          "الخطوة الرابعة: f de zéro égale zéro، إذن la courbe كدوز من O. الخطوة الخامسة، ف plus l'infini: "
          "f de x sur x كتساوي racine de x plus un، اللي كتمشي ل plus l'infini. سؤال: شنو كتعني هاد la limite؟")
    c["concentration"]["pointage"] = [p for p in c["concentration"]["pointage"] if not p["mot"].startswith("إذن branche")]
    q_br["demonstration"] = {
        "parole": "ف plus l'infini، f de x كتمشي ل plus l'infini. وf de x sur x، كتمشي حتى هي ل plus l'infini. "
                  "إذن la courbe admet une branche parabolique, de direction l'axe des ordonnées. "
                  "يعني la courbe كطلع بحال l'axe des ordonnées. ومن بعد كنرسمو، بالترتيب: les droites، les points، و la courbe.",
        "lignes": [
            {"texte": "lim_{x→+∞} f(x) = lim_{x→+∞} x√(x + 1) = +∞", "mot": "ف plus l'infini، f de x"},
            {"texte": "lim_{x→+∞} f(x)/x = lim_{x→+∞} √(x + 1) = +∞", "mot": "وf de x sur x"},
            {"texte": "Donc (C_f) admet une branche parabolique de direction l'axe des ordonnées au voisinage de +∞.", "mot": "إذن la courbe admet"},
            {"texte": "Tracé : les droites, puis les points, puis la courbe.", "mot": "ومن بعد كنرسمو"}]}
    c["question"] = q_br
    c["concentration"]["reponses"] = {"q": rep_br}
open(CH, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")

P = lambda *ids: ["df_" + i for i in ids]
PARTIES = [
    ("df_partie1", "I. Pourquoi dériver ; le nombre dérivé", "situation",
     P("c1_carte", "z1_pente", "nd1_secante", "nd2_rapprocher", "nd3_nombre_derive", "nd4_calcul", "nd4_calcul_b")),
    ("df_partie2", "II. L'équation de la tangente", "explanation",
     P("z2_equation_droite", "tg1_equation", "tg2_ecrire", "tg3_verifier")),
    ("df_partie3", "III. À droite, à gauche : demi-tangentes et point anguleux", "explanation",
     P("dt1_droite", "dt2_gauche", "dt3_anguleux", "z5_un_sur_x", "dt4_infini", "dt5_sens", "dt5_sens_b", "dt6_morceaux")),
    ("df_partie4", "IV. Calculer une dérivée", "explanation",
     P("z3_deriver_polynome", "dv1_tableau", "dv2_produit_quotient", "dv2_produit_quotient_b", "dv3_puissance",
       "dv4_racine", "dv5_racine_n", "dv5b_intervalle", "dv6_montrer")),
    ("df_partie5", "V. Signe de f' et variations", "explanation",
     P("va1_monte", "va2_sommet", "va2_sommet_b", "z4_signe_produit", "va3_factoriser", "va4_tableau",
       "va5_double_barre", "va6_extremum", "va7_auxiliaire")),
    ("df_partie6", "VI. Concavité et point d'inflexion", "explanation",
     P("co1_sous", "co2_traverse", "co3_f_seconde", "co4_changeant")),
    ("df_partie7", "VII. Branches infinies", "explanation",
     P("bi1_verticale", "bi2_horizontale", "bi3_oblique", "bi4_pente_om", "bi5_direction", "bi6_arbre", "bi6_arbre_b",
       "bi7_droite_donnee")),
    ("df_partie8", "VIII. Position relative d'une courbe et d'une droite", "explanation",
     P("pr1_dessus", "pr2_signe", "pr3_tableau")),
    ("df_partie9", "IX. Axe et centre de symétrie", "explanation",
     P("sy1_symetrique", "sy2_axe", "sy3_centre", "sy4_rediger")),
    ("df_partie10", "X. Construire et lire la courbe", "application",
     P("tr1_tableau_lu", "tr2_droites", "tr3_points", "tr4_branche", "tr5_symetrie", "tr6_lire")),
    ("df_partie11", "XI. Dérivée et courbe de la fonction réciproque", "explanation",
     P("rec1_miroir", "rec2_pente", "rec3_formule", "rec4_condition", "rec5_national", "rec6_courbe")),
    ("df_partie12", "XII. Le problème d'analyse, étape par étape", "evaluation",
     P("ec1_ordre", "ec2_forme", "ec3_etude", "ec3_etude_a2", "ec3_etude_b", "ec3_etude_c", "ec4_unique")),
    ("df_bilan", "XIII. Bilan du chapitre", "evaluation", P("fin1_bilan", "fin2_carte")),
]
SEANCES = [
    ("df_s1", "Séance 1 — Du taux d'accroissement à la tangente", [
        ("df_n1_b1", "La carte ; la pente d'une droite ; la pente d'une sécante", P("c1_carte", "z1_pente", "nd1_secante")),
        ("df_n1_b2", "Le nombre dérivé ; le calcul, un polynôme puis une racine", P("nd2_rapprocher", "nd3_nombre_derive", "nd4_calcul", "nd4_calcul_b")),
        ("df_n1_b3", "L'équation d'une droite ; la tangente", P("z2_equation_droite", "tg1_equation", "tg2_ecrire")),
        ("df_n1_b4", "Vérifier sa tangente ; arriver par la droite, par la gauche", P("tg3_verifier", "dt1_droite", "dt2_gauche"))]),
    ("df_s2", "Séance 2 — Demi-tangentes ; calculer une dérivée", [
        ("df_n2_b1", "Point anguleux ; 1/x près de 0 ; le taux part à l'infini", P("dt3_anguleux", "z5_un_sur_x", "dt4_infini")),
        ("df_n2_b2", "Demi-tangente vers le haut ou le bas ; deux morceaux", P("dt5_sens", "dt5_sens_b", "dt6_morceaux")),
        ("df_n2_b3", "Dériver un polynôme ; le tableau ; produit et quotient", P("z3_deriver_polynome", "dv1_tableau", "dv2_produit_quotient", "dv2_produit_quotient_b")),
        ("df_n2_b4", "Puissance, racine, racine n-ième d'une expression", P("dv3_puissance", "dv4_racine", "dv5_racine_n"))]),
    ("df_s3", "Séance 3 — La fonction dérivée et le sens de variation", [
        ("df_n3_b1", "Dérivable sur un intervalle ; « montrer que f′(x) = … » ; la courbe monte", P("dv5b_intervalle", "dv6_montrer", "va1_monte")),
        ("df_n3_b2", "Le sommet, le creux ; le signe d'un produit", P("va2_sommet", "va2_sommet_b", "z4_signe_produit")),
        ("df_n3_b3", "Factoriser f′ ; le tableau de variations ; la valeur exclue", P("va3_factoriser", "va4_tableau", "va5_double_barre")),
        ("df_n3_b4", "Lire un extremum ; le signe venu d'une autre fonction", P("va6_extremum", "va7_auxiliaire"))]),
    ("df_s4", "Séance 4 — Concavité et branches infinies", [
        ("df_s4_b1", "Concavité et point d'inflexion", P("co1_sous", "co2_traverse", "co3_f_seconde", "co4_changeant")),
        ("df_s4_b2", "Les asymptotes", P("bi1_verticale", "bi2_horizontale", "bi3_oblique", "bi4_pente_om")),
        ("df_s4_b3", "Branches paraboliques et phrases types", P("bi5_direction", "bi6_arbre", "bi6_arbre_b", "bi7_droite_donnee"))]),
    ("df_s5", "Séance 5 — Position relative, symétrie, préparer le tracé", [
        ("df_s5_b1", "Position relative d'une courbe et d'une droite", P("pr1_dessus", "pr2_signe", "pr3_tableau")),
        ("df_s5_b2", "Axe et centre de symétrie", P("sy1_symetrique", "sy2_axe", "sy3_centre", "sy4_rediger")),
        ("df_s5_b3", "Préparer le tracé", P("tr1_tableau_lu", "tr2_droites", "tr3_points"))]),
    ("df_s6", "Séance 6 — Lire une courbe ; la fonction réciproque", [
        ("df_s6_b1", "Tracer d'un seul trait et lire la courbe", P("tr4_branche", "tr5_symetrie", "tr6_lire")),
        ("df_s6_b2", "La réciproque dans le miroir y = x", P("rec1_miroir", "rec2_pente", "rec3_formule")),
        ("df_s6_b3", "Rédiger comme au national et tracer la réciproque", P("rec4_condition", "rec5_national", "rec6_courbe"))]),
    ("df_s7", "Séance 7 — Le problème d'analyse, étape par étape ; le bilan", [
        ("df_n7_b1", "L'ordre du problème ; la forme demandée ; l'ensemble de définition", P("ec1_ordre", "ec2_forme", "ec3_etude")),
        ("df_n7_b2", "Le bord, le signe de f′, la branche ; une solution unique", P("ec3_etude_a2", "ec3_etude_b", "ec3_etude_c", "ec4_unique")),
        ("df_s7_b3", "Le bilan et la carte", P("fin1_bilan", "fin2_carte"))]),
]
spec = {"deck": DECK, "nouvelles": NOUVELLES, "retirees": {},
        "parties": [{"id": i, "title": t, "phase": ph, "slides": s} for i, t, ph, s in PARTIES],
        "seances": [{"id": i, "titre": t, "blocs": [{"id": bi, "titre": bt, "slides": bs} for bi, bt, bs in bl]}
                    for i, t, bl in SEANCES]}
p = os.path.join(ICI, "spec_" + DECK + ".json")
open(p, "w", encoding="utf-8").write(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
subprocess.run([sys.executable, os.path.join(ICI, "reordonner.py"), p], check=True)
os.remove(p)
