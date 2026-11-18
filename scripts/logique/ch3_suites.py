"""Nouvelle logique de math_ch3_suites_numeriques (architecture : backend/data/curriculum/architecture/
math_ch3_suites_numeriques.md). Rejouable depuis la copie en attente d'avant."""
import copy, json, os, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..")
DECK = "math_ch3_suites_numeriques"
CH = os.path.join(RACINE, "backend/data/courses/en_attente", DECK + ".json")
SIM = "/media/simulations/maths/suites-tableau/"
d = json.load(open(CH, encoding="utf-8"))
S = {s["id"]: s for a in d["activities"] for s in a["slides"]}
NOUVELLES = {}
P = lambda *ids: ["su_" + i for i in ids]


def texte(s, fr, mixed):
    s["speech_text"] = {"fr": fr, "mixed": mixed}
    s.pop("audio", None)


def pt(mot, moment):
    return {"mot": mot, "commande": "play_until", "parametres": {"moment": moment}}


def qcm(prompt, options, correct, enonce_dit, parole, lignes):
    return {"type": "qcm", "prompt": prompt, "options": options, "correct": correct, "timeout_seconds": 40,
            "enonce_dit": enonce_dit,
            "demonstration": {"parole": parole, "lignes": [{"texte": t, "mot": m} for t, m in lignes]}}


# 1. r4 vient juste après le rappel « signe de la différence » : ce n'est plus « la règle vue au début ».
r4 = S["su_r4_heredite_fraction"]
if "vue au début" in r4["speech_text"]["fr"]:
    texte(r4, r4["speech_text"]["fr"].replace("C'est la règle vue au début", "C'est la règle qu'on vient de voir"),
          r4["speech_text"]["mixed"].replace("هادي هي القاعدة اللي شفنا فالأول:", "هادي هي القاعدة اللي شفنا دابا:")
          .replace("شوف السطر المشطب: نقدرو نحصرو الفوق ولتحت، ولكن ما نعرفوش نقسمو جوج inégalités. هادشي ما كيمشيش.",
                   "شوف السطر اللي عليه خط: نقدرو نحددو الفوق ولتحت، ولكن مايمكنش نقسمو جوج inégalités. هاد الطريقة ماشي هي."))
    for q in r4["concentration"]["pointage"]:
        q["mot"] = {"شوف السطر المشطب:": "شوف السطر اللي عليه خط:", "هادشي ما كيمشيش.": "هاد الطريقة ماشي هي."}.get(q["mot"], q["mot"])

# 2. L'exercice du national 2024 joué question par question.
e1 = S["su_e1_complet"]
if e1.get("exercises"):
    q_v, rep_v = e1.pop("exercises")[0], e1["concentration"]["reponses"].pop("e0")
    q_lim, rep_lim = e1.pop("question"), e1["concentration"]["reponses"].pop("q")
    base = copy.deepcopy(e1)
    for k in ("audio",):
        base.pop(k, None)

    e1["title"] = "National 2024, question 1 : l'encadrement par récurrence"
    e1["screen_content"] = {
        "lead": "Une question à la fois : ta réponse, puis la correction.",
        "bullets": ["National 2024 : u₀ = 4, uₙ₊₁ = (4uₙ − 2)/(uₙ + 1).",
                    "1. Montrer par récurrence que 2 ≤ uₙ ≤ 4.",
                    "Hérédité : uₙ₊₁ − 2 = 2(uₙ − 2)/(uₙ + 1) : son signe ?"],
        "student_trace": "Récurrence : initialisation u₀ = 4 ∈ [2 ; 4] ; hérédité : uₙ₊₁ − 2 = 2(uₙ − 2)/(uₙ + 1) ≥ 0 "
                         "et uₙ₊₁ − 4 = −6/(uₙ + 1) < 0 ; donc pour tout n ∈ ℕ, 2 ≤ uₙ ≤ 4."}
    e1["visual"] = {"kind": "simulation", "url": SIM + "calculs.html?vue=e1_q1",
                    "caption": "Question 1, ligne par ligne", "alt": "L'énoncé, l'initialisation et l'hérédité écrits à la craie"}
    texte(e1,
          "Un exercice du national deux mille vingt-quatre, joué question par question. u zéro égale quatre, et u "
          "indice n plus un égale quatre u indice n moins deux, sur u indice n plus un. Question un : montrer par "
          "récurrence que u indice n est entre deux et quatre. Initialisation : u zéro égale quatre, il est entre "
          "deux et quatre. Hérédité : on suppose deux inférieur ou égal à u indice n, inférieur ou égal à quatre. "
          "On calcule u indice n plus un moins deux : on trouve deux fois, u indice n moins deux, sur u indice n "
          "plus un. Question : quel est le signe de cette différence ?",
          "هادا تمرين ديال الوطني ديال deux mille vingt-quatre، غادي نديروه سؤال بسؤال. u zéro égale quatre، "
          "وu indice n plus un égale quatre u indice n moins deux، sur u indice n plus un. السؤال اللول: بين par "
          "récurrence بلي u indice n بين deux وquatre. l'initialisation: u zéro égale quatre، كاين بين deux وquatre. "
          "l'hérédité: نفترضو بلي deux inférieur ou égal à u indice n، inférieur ou égal à quatre. كنحسبو u indice n "
          "plus un moins deux: كنلقاو deux fois، u indice n moins deux، sur u indice n plus un. "
          "سؤال: شنو هو le signe ديال هاد la différence؟")
    e1["question"] = qcm(
        "Si 2 ≤ uₙ ≤ 4, le signe de uₙ₊₁ − 2 = 2(uₙ − 2)/(uₙ + 1) est :",
        ["négatif", "positif ou nul", "on ne peut pas savoir"], 1,
        "شوف هاد السؤال: يلا كان u indice n بين deux وquatre، شنو هو le signe ديال u indice n plus un moins deux؟",
        "u indice n plus un moins deux، كنديرو نفس المقام: quatre u indice n moins deux، moins deux u indice n moins deux، "
        "sur u indice n plus un. يعني deux، u indice n moins deux، sur u indice n plus un. "
        "u indice n moins deux positif ولا zéro، حيت u indice n plus grand que deux. وu indice n plus un positif. "
        "إذن u indice n plus un moins deux positif ولا zéro: u indice n plus un plus grand que deux. "
        "ونفس الشي: u indice n plus un moins quatre égale moins six، sur u indice n plus un، négatif. "
        "إذن u indice n plus un plus petit que quatre. الخلاصة: pour tout n، u indice n بين deux وquatre.",
        [("uₙ₊₁ − 2 = (4uₙ − 2)/(uₙ + 1) − 2 = (4uₙ − 2 − 2uₙ − 2)/(uₙ + 1)", "u indice n plus un moins deux، كنديرو"),
         ("= (2uₙ − 4)/(uₙ + 1) = 2(uₙ − 2)/(uₙ + 1)", "يعني deux، u indice n"),
         ("uₙ − 2 ≥ 0 (car uₙ ≥ 2) et uₙ + 1 > 0", "u indice n moins deux positif"),
         ("donc uₙ₊₁ − 2 ≥ 0, soit uₙ₊₁ ≥ 2", "إذن u indice n plus un moins deux"),
         ("uₙ₊₁ − 4 = (4uₙ − 2 − 4uₙ − 4)/(uₙ + 1) = −6/(uₙ + 1) < 0, soit uₙ₊₁ < 4", "ونفس الشي:"),
         ("Conclusion : pour tout n ∈ ℕ, 2 ≤ uₙ ≤ 4.", "الخلاصة:")])
    e1["concentration"] = {
        "demarrer": "start",
        "pointage": [pt("u zéro égale quatre، وu", "enonce"), pt("السؤال اللول:", "q1"),
                     pt("l'initialisation:", "init"), pt("l'hérédité:", "hyp"), pt("كنحسبو u indice n", "calcul")],
        "cahier": e1["screen_content"]["student_trace"], "reponses": {}}
    e1["competence_ids"] = ["K2"]

    def nouvelle(ident, titre, lead, bullets, trace, url, caption, alt, fr, mixed, question, pointage, comp, reponses=None):
        s = copy.deepcopy(base)
        s.update({"id": ident, "title": titre, "competence_ids": comp,
                  "screen_content": {"lead": lead, "bullets": bullets, "student_trace": trace},
                  "visual": {"kind": "simulation", "url": url, "caption": caption, "alt": alt},
                  "speech_text": {"fr": fr, "mixed": mixed}, "question": question,
                  "concentration": {"demarrer": "start", "pointage": pointage, "cahier": trace,
                                    "reponses": reponses or {}}})
        NOUVELLES[ident] = s

    nouvelle("su_e1_q2", "National 2024, question 2 : le sens de variation", "Le signe de uₙ₊₁ − uₙ.",
             ["uₙ₊₁ − uₙ = −(uₙ − 1)(uₙ − 2)/(uₙ + 1).", "Avec 2 ≤ uₙ ≤ 4 (question 1) : croissante ou décroissante ?"],
             "uₙ₊₁ − uₙ = −(uₙ − 1)(uₙ − 2)/(uₙ + 1) ≤ 0 car 2 ≤ uₙ ≤ 4 : (uₙ) est décroissante.",
             SIM + "calculs.html?vue=e1_q2", "La différence, ligne par ligne",
             "uₙ₊₁ − uₙ mis au même dénominateur et factorisé, à la craie",
             "Question deux : le sens de variation. On calcule u indice n plus un moins u indice n. On met au même "
             "dénominateur, et on factorise le haut : on trouve moins, u indice n moins un, fois u indice n moins "
             "deux, sur u indice n plus un. On sait que u indice n est entre deux et quatre. Question : la suite "
             "est-elle croissante ou décroissante ?",
             "السؤال الثاني: le sens de variation. كنحسبو u indice n plus un moins u indice n. كنديرو نفس المقام، "
             "وكنديرو la factorisation ديال الفوق: كنلقاو moins، u indice n moins un، fois u indice n moins deux، "
             "sur u indice n plus un. عارفين بلي u indice n بين deux وquatre. "
             "سؤال: واش la suite croissante ولا décroissante؟",
             qcm("uₙ₊₁ − uₙ = −(uₙ − 1)(uₙ − 2)/(uₙ + 1) et 2 ≤ uₙ ≤ 4. La suite (uₙ) est :",
                 ["croissante", "décroissante", "ni croissante ni décroissante"], 1,
                 "شوف هاد السؤال: واش la suite u indice n croissante ولا décroissante؟",
                 "u indice n plus un moins u indice n، égale quatre u indice n moins deux، moins u indice n fois، "
                 "u indice n plus un، sur u indice n plus un. الفوق: moins u indice n au carré، plus trois u indice n، "
                 "moins deux. هادا هو moins، u indice n moins un، fois u indice n moins deux. "
                 "u indice n moins un positif، u indice n moins deux positif ولا zéro، وu indice n plus un positif. "
                 "مع moins اللي قدام، la différence négative ولا zéro. إذن la suite décroissante.",
                 [("uₙ₊₁ − uₙ = (4uₙ − 2 − uₙ(uₙ + 1))/(uₙ + 1)", "u indice n plus un moins u indice n، égale"),
                  ("= (−uₙ² + 3uₙ − 2)/(uₙ + 1) = −(uₙ − 1)(uₙ − 2)/(uₙ + 1)", "الفوق:"),
                  ("2 ≤ uₙ ≤ 4 : uₙ − 1 > 0, uₙ − 2 ≥ 0 et uₙ + 1 > 0", "u indice n moins un positif"),
                  ("donc uₙ₊₁ − uₙ ≤ 0 pour tout n : (uₙ) est décroissante.", "مع moins")]),
             [pt("كنحسبو u indice n plus un moins u indice n.", "difference"), pt("كنلقاو moins،", "calcul"),
              pt("عارفين بلي", "question")], ["K3"])

    nouvelle("su_e1_q3", "National 2024, question 3 : la convergence", "Le bon couple.",
             ["Question 1 : uₙ ≥ 2 (minorée).", "Question 2 : décroissante.", "Donc ?"],
             "(uₙ) est décroissante et minorée par 2 : elle est convergente.",
             SIM + "plafond.html?vue=couple", "Les deux bons couples",
             "Une suite qui monte sous un plafond, une suite qui descend au-dessus d'un plancher",
             "Question trois : la convergence. Regarde les deux bons couples. Une suite croissante et majorée "
             "converge. Une suite décroissante et minorée converge aussi. Notre suite descend, et u "
             "indice n reste plus grand que deux. Question : que peut-on dire ?",
             "السؤال الثالث: la convergence. شوف جوج ديال les couples المزيانين. suite croissante et majorée، "
             "كتكون convergente. وsuite décroissante et minorée، حتى هي convergente. la suite ديالنا décroissante، "
             "وu indice n ديما أكبر من deux. سؤال: شنو نقدرو نقولو؟",
             qcm("(uₙ) est décroissante et minorée par 2. Donc :",
                 ["(uₙ) est convergente", "lim uₙ = −∞", "on ne peut rien dire"], 0,
                 "شوف هاد السؤال: la suite décroissante et minorée par deux. شنو نقدرو نقولو؟",
                 "la suite décroissante، حسب السؤال الثاني. وminorée par deux، حسب السؤال اللول. "
                 "كل suite décroissante et minorée كتكون convergente. إذن u indice n convergente. "
                 "la limite ديالها غادي نحسبوها فالسؤال الخامس.",
                 [("(uₙ) est décroissante (question 2)", "la suite décroissante، حسب"),
                  ("(uₙ) est minorée par 2 (question 1 : uₙ ≥ 2)", "وminorée par deux"),
                  ("Toute suite décroissante et minorée est convergente.", "كل suite décroissante"),
                  ("Donc (uₙ) est convergente ; sa limite se calcule à la question 5.", "إذن u indice n convergente")]),
             [pt("suite croissante et majorée،", "croissante_majoree"), pt("وsuite décroissante et minorée،", "miroir_decroissante")], ["K6"])

    q_v["options"] = q_v.pop("choices")
    q_v.pop("explanation", None)
    q_v["timeout_seconds"] = 40
    nouvelle("su_e1_q4", "National 2024, question 4 : la suite auxiliaire", "vₙ₊₁ en fonction de vₙ.",
             ["vₙ = (uₙ − 2)/(uₙ − 1).", "Données : uₙ₊₁ − 2 = 2(uₙ − 2)/(uₙ + 1) ; uₙ₊₁ − 1 = 3(uₙ − 1)/(uₙ + 1).",
              "vₙ₊₁ = ?"],
             "vₙ₊₁ = (uₙ₊₁ − 2)/(uₙ₊₁ − 1) = (2/3)vₙ : (vₙ) est géométrique de raison 2/3 et de premier terme v₀ = 2/3.",
             SIM + "calculs.html?vue=e1_q4", "Question 4, ligne par ligne",
             "vₙ, puis les deux égalités données, écrites à la craie",
             "Question quatre : la suite auxiliaire. On pose v indice n égale u indice n moins deux, sur u indice n "
             "moins un. L'énoncé donne deux relations : u indice n plus un moins deux égale deux fois, u indice n "
             "moins deux, sur u indice n plus un. Et u indice n plus un moins un égale trois fois, u indice n moins "
             "un, sur u indice n plus un. Question : v indice n plus un égale quoi ?",
             "السؤال الرابع: la suite auxiliaire. كنحطو v indice n égale u indice n moins deux، sur u indice n moins un. "
             "السؤال كيعطينا جوج ديال les relations: u indice n plus un moins deux égale deux fois، u indice n moins deux، "
             "sur u indice n plus un. وu indice n plus un moins un égale trois fois، u indice n moins un، sur u indice "
             "n plus un. سؤال: v indice n plus un كتساوي شنو؟",
             q_v, [pt("كنحطو v indice n", "pose"), pt("السؤال كيعطينا", "donnees"), pt("سؤال: v indice n", "question")],
             ["K4"], {"q": rep_v})

    nouvelle("su_e1_q5", "National 2024, question 5 : uₙ en fonction de n, puis la limite", "De vₙ à uₙ.",
             ["v₀ = (4 − 2)/(4 − 1) = 2/3 ; vₙ = (2/3)ⁿ⁺¹.", "On isole uₙ, puis lim uₙ = ?"],
             "vₙ = (2/3)ⁿ⁺¹ ; uₙ = (2 − vₙ)/(1 − vₙ) = 1 + 1/(1 − (2/3)ⁿ⁺¹) ; −1 < 2/3 < 1 donc lim uₙ = 2.",
             SIM + "calculs.html?vue=e1_q5", "Question 5, ligne par ligne", "v₀, vₙ, puis uₙ à isoler, à la craie",
             "Question cinq : u indice n en fonction de n, puis la limite. v zéro égale quatre moins deux, sur quatre "
             "moins un : deux tiers. Donc v indice n égale deux tiers puissance n plus un. Ensuite on isole u indice "
             "n à partir de v indice n. Question : quelle est la limite de u indice n ?",
             "السؤال الخامس: u indice n en fonction de n، ومن بعد la limite. v zéro égale quatre moins deux، sur quatre "
             "moins un: deux tiers. إذن v indice n égale deux tiers puissance n plus un. ومن بعد كنخرجو u indice n "
             "من v indice n. سؤال: شنو هي la limite ديال u indice n؟",
             q_lim, [pt("v zéro égale", "v0"), pt("إذن v indice n", "vn"), pt("ومن بعد كنخرجو", "question")],
             ["K4", "K5"], {"q": rep_lim})
# 3. La suite du problème (uₙ₊₁ = g(uₙ)) en deux étapes : le sens de variation, puis la convergence et la limite.
f7 = S["su_f7_national"]
if "su_f7_national_b" not in S and f7["question"]["prompt"].startswith("Montre que (uₙ) est croissante, puis"):
    ancienne = f7["question"]["demonstration"]["lignes"]
    base7 = copy.deepcopy(f7)
    f7["title"] = "À toi : la suite du problème, étape 1 — le sens de variation"
    f7["screen_content"] = {
        "lead": "Étape 1 : le signe de g(x) − x.",
        "bullets": ["g(x) = (4x + 3)/(x + 2), u₀ = 1, uₙ₊₁ = g(uₙ) ; on a montré 1 ≤ uₙ ≤ 3.",
                    "uₙ₊₁ − uₙ = g(uₙ) − uₙ : le signe de g(x) − x sur [1 ; 3] ?"],
        "student_trace": "g(x) − x = (3 − x)(x + 1)/(x + 2) ≥ 0 sur [1 ; 3] et uₙ ∈ [1 ; 3], donc uₙ₊₁ − uₙ ≥ 0 : "
                         "(uₙ) est croissante."}
    texte(f7,
          "À toi, avec une suite de problème. g de x égale quatre x plus trois, sur x plus deux. u zéro égale un, et u "
          "indice n plus un égale g de u indice n. On a déjà montré que tous les termes sont entre un et trois. "
          "Regarde l'escalier : il part de un. Étape un, le sens de variation : u indice n plus un moins u indice n, "
          "c'est g de u indice n moins u indice n. On étudie donc le signe de g de x moins x, entre un et trois. "
          "Question : la suite est-elle croissante ou décroissante ?",
          "دابا نتا، مع suite ديال problème. g de x égale quatre x plus trois، sur x plus deux. u zéro égale un، "
          "وu indice n plus un égale g de u indice n. ديجا بينا بلي كاع les termes بين un وtrois. "
          "شوف الخطوط: كيبداو من un. الخطوة اللولة، le sens de variation: u indice n plus un moins u indice n، "
          "هي g de u indice n moins u indice n. إذن كنقراو le signe ديال g de x moins x، بين un وtrois. "
          "سؤال: واش la suite croissante ولا décroissante؟")
    f7["question"] = qcm(
        "g(x) − x = (3 − x)(x + 1)/(x + 2) et 1 ≤ uₙ ≤ 3. La suite (uₙ) est :",
        ["décroissante", "croissante", "constante"], 1,
        "شوف هاد السؤال: g de x moins x égale trois moins x، fois x plus un، sur x plus deux. واش la suite croissante ولا décroissante؟",
        "g de x moins x، كنديرو نفس المقام: moins x carré plus deux x plus trois، sur x plus deux. "
        "كنديرو la factorisation ديال الفوق: trois moins x، fois x plus un. بين un وtrois: trois moins x positif، "
        "x plus un وx plus deux positifs، إذن g de x moins x positif. u indice n بين un وtrois، "
        "إذن u indice n plus un moins u indice n positif: la suite croissante.",
        [(ancienne[0]["texte"], "g de x moins x، كنديرو"), (ancienne[1]["texte"], "كنديرو la factorisation"),
         (ancienne[2]["texte"], "بين un وtrois:"), (ancienne[3]["texte"], "u indice n بين un")])
    f7["concentration"] = {
        "demarrer": "start",
        "pointage": [pt("شوف الخطوط: كيبداو", "escalier")],
        "cahier": f7["screen_content"]["student_trace"], "reponses": {}}

    b7 = base7
    b7["id"] = "su_f7_national_b"
    b7["title"] = "À toi : la suite du problème, étape 2 — convergente, puis ℓ = g(ℓ)"
    b7["screen_content"] = {
        "lead": "Étape 2 : convergente, puis la limite.",
        "bullets": ["(uₙ) est croissante (étape 1) et majorée par 3.",
                    "g est continue sur I = [1 ; 3] car dérivable ; g(I) = [7/3 ; 3] ⊂ I ; u₀ ∈ I.",
                    "ℓ = g(ℓ) dans I : ℓ = ?"],
        "student_trace": "(uₙ) croissante et majorée par 3 : convergente ; g continue sur I (car dérivable), "
                         "g(I) = [g(1) ; g(3)] ⊂ I, u₀ ∈ I : ℓ = g(ℓ), ℓ ∈ I, donc ℓ = 3."}
    texte(b7,
          "Étape deux. La suite est croissante, et majorée par trois : elle est convergente. Regarde la courbe : elle "
          "coupe la droite y égale x en deux points. Pour la limite l, on vérifie les conditions : g est continue sur "
          "l'intervalle, l'image de l'intervalle est dans l'intervalle, et u zéro est dedans. Alors l égale g de l. "
          "Question : quelle est la limite de la suite ?",
          "الخطوة الثانية. la suite croissante، وmajorée par trois: إذن convergente. شوف la courbe: كتقطع la droite "
          "y égale x فجوج ديال النقط. باش نلقاو la limite l، كنشوفو les conditions: g continue sur l'intervalle، "
          "l'image ديال l'intervalle داخل l'intervalle، وu zéro داخل حتى هو. إذن l égale g de l. "
          "سؤال: شنو هي la limite ديال la suite؟")
    b7["question"] = qcm(
        "ℓ = g(ℓ) et ℓ ∈ [1 ; 3]. lim uₙ = ?", ["−1", "1", "3"], 2,
        "شوف هاد السؤال: l égale g de l، وl بين un وtrois. شنو هي la limite ديال u indice n؟",
        "la suite croissante وmajorée par trois، إذن convergente. g continue sur l'intervalle، حيت dérivable. "
        "وg prime de x égale cinq، sur x plus deux au carré، positif. إذن l'image ديال l'intervalle، "
        "من g de un حتى g de trois، من sept tiers حتى trois، داخل l'intervalle. وu zéro égale un، داخل حتى هو. "
        "إذن l solution ديال g de x égale x: trois moins x، fois x plus un، égale zéro، x égale trois ولا moins un. "
        "moins un ماشي فl'intervalle، إذن la limite هي trois.",
        [(ancienne[4]["texte"], "la suite croissante وmajorée"), (ancienne[5]["texte"], "g continue sur"),
         (ancienne[6]["texte"], "إذن l'image ديال"), (ancienne[7]["texte"], "إذن l solution"),
         (ancienne[8]["texte"], "moins un ماشي")])
    b7["concentration"] = {
        "demarrer": "start",
        "pointage": [pt("شوف la courbe:", "courbe_et_droite"), {"mot": "فجوج ديال النقط.", "repere": "point_trois"}],
        "cahier": b7["screen_content"]["student_trace"], "reponses": {}}
    NOUVELLES["su_f7_national_b"] = b7
open(CH, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")

PARTIES = [
    ("su_partie1", "I. Une suite, ses termes ; arithmétique et géométrique", "situation",
     P("o1_questions", "a1_liste", "a2_indice", "a3_termes", "a3b_recurrence", "a4_arithmetique", "a5_terme_arith",
       "z1_puissances", "a6_geometrique", "a7_terme_geo", "a8_nombre_termes", "a9_sommes", "a9b_somme_geo")),
    ("su_partie2", "II. Le raisonnement par récurrence", "explanation",
     P("r1_dominos", "r2_trois_titres", "r2b_heredite", "r2c_conclusion", "z2_ordre_garde", "z3_ordre_inverse",
       "r3_heredite_affine", "z4_difference", "z5_denominateur", "r4_heredite_fraction", "r4b_calcul", "r5_choisir",
       "r6_ecriture_donnee", "r7_strict_large", "r8_national")),
]
d2 = json.load(open(CH, encoding="utf-8"))
for a in d2["activities"]:
    if a["id"] not in ("su_partie1", "su_partie2", "su_partie8"):
        ids = [s["id"] for s in a["slides"]]
        if "su_f7_national" in ids and "su_f7_national_b" not in ids:
            ids.insert(ids.index("su_f7_national") + 1, "su_f7_national_b")
        PARTIES.append((a["id"], a["title"], a["phase"], ids))
PARTIES.sort(key=lambda p: int(p[0].replace("su_partie", "").replace("su_bilan", "99")))
PARTIES.insert(-1, ("su_partie8", "VIII. Problèmes : rang, somme ; un exercice national question par question", "evaluation",
                    P("p1_rang", "p2_somme_mixte", "p3_limite_somme", "e1_complet", "e1_q2", "e1_q3", "e1_q4", "e1_q5")))
for i, p in enumerate(PARTIES):
    if p[0] == "su_bilan":
        PARTIES[i] = (p[0], p[1], p[2], P("e2_bilan", "e3_carte"))
PARTIES.append(PARTIES.pop([p[0] for p in PARTIES].index("su_bilan")))

anciens = {b["id"]: b["slide_ids"] for se in d2["seances"] for b in se["blocs"]}
A = lambda i: (i, None, anciens[i])
SEANCES = [
    ("su_s1", "Séance 1 — Une suite ; arithmétique et géométrique", [
        ("su_n1_b1", "La carte ; une liste numérotée ; uₙ₊₁ n'est pas uₙ + 1", P("o1_questions", "a1_liste", "a2_indice")),
        ("su_n1_b2", "Par une formule, par récurrence ; suite arithmétique", P("a3_termes", "a3b_recurrence", "a4_arithmetique", "a5_terme_arith")),
        ("su_n1_b3", "Les puissances ; suite géométrique", P("z1_puissances", "a6_geometrique", "a7_terme_geo")),
        ("su_n1_b4", "Nombre de termes ; les deux sommes", P("a8_nombre_termes", "a9_sommes", "a9b_somme_geo"))]),
    ("su_s2", "Séance 2 — Le raisonnement par récurrence", [
        ("su_n2_b1", "Les dominos ; l'annonce, l'initialisation, l'hérédité", P("r1_dominos", "r2_trois_titres", "r2b_heredite")),
        ("su_n2_b2", "La conclusion ; le sens d'une inégalité", P("r2c_conclusion", "z2_ordre_garde", "z3_ordre_inverse")),
        ("su_n2_b3", "Hérédité affine ; comparer par la différence ; même dénominateur", P("r3_heredite_affine", "z4_difference", "z5_denominateur")),
        ("su_n2_b4", "Hérédité avec une fraction ; choisir sa méthode", P("r4_heredite_fraction", "r4b_calcul", "r5_choisir"))]),
    ("su_s3", "Séance 3 — Récurrence du national ; bornée ; sens de variation", [
        ("su_n3_b1", "L'écriture donnée ; strict ou large ; une récurrence du national", P("r6_ecriture_donnee", "r7_strict_large", "r8_national")),
        ("su_n3_b2", "Majorée, minorée, bornée ; croissante pour tout n", P("b1_plancher", "b2_bornee", "m1_pour_tout_n")),
        ("su_s3_b1", "Le sens de variation : différence et quotient", P("m2_difference", "m3_egalite_donnee", "m4_quotient"))]),
]
reste = [b for se in d2["seances"] for b in se["blocs"]]
ordre_blocs = [b["id"] for b in reste]
suite = ordre_blocs[ordre_blocs.index("su_s3_b2"):ordre_blocs.index("su_s6_b2")]
titres = {b["id"]: b["titre"] for b in reste}
for k, (sid, st) in enumerate([("su_s4", "Séance 4 — La suite auxiliaire ; les limites de référence"),
                                ("su_s5", "Séance 5 — Limites d'une suite et convergence"),
                                ("su_s6", "Séance 6 — La suite uₙ₊₁ = f(uₙ) ; rang et somme")]):
    blocs = suite[3 * k:3 * k + 3]
    if blocs:
        lignes = []
        for b in blocs:
            if b == "su_s5_b3":
                lignes.append(("su_n6_b2", "Sens de variation par f(x) − x ; les conditions ; choisir ℓ", P("f4_sens_f", "f5_conditions", "f6_choisir")))
                lignes.append(("su_n6_b3", "La suite du problème, en deux étapes : ta réponse avant la correction", P("f7_national", "f7_national_b")))
            else:
                lignes.append((b, titres[b], [i for i in anciens[b] if i != "su_f7_national_b"]))
        SEANCES.append((sid, st, lignes))
SEANCES.append(("su_s7", "Séance 7 — Un exercice national, question par question ; le bilan", [
    ("su_n8_b1", "National 2024 : cinq questions, ta réponse avant la correction", P("e1_complet", "e1_q2", "e1_q3", "e1_q4", "e1_q5")),
    ("su_n8_b2", "Ce qu'il faut retenir ; la carte", P("e2_bilan", "e3_carte"))]))
spec = {"deck": DECK, "nouvelles": NOUVELLES, "retirees": {},
        "parties": [{"id": i, "title": t, "phase": ph, "slides": s} for i, t, ph, s in PARTIES],
        "seances": [{"id": i, "titre": t, "blocs": [{"id": bi, "titre": bt, "slides": bs} for bi, bt, bs in bl]}
                    for i, t, bl in SEANCES]}
p = os.path.join(ICI, "spec_" + DECK + ".json")
open(p, "w", encoding="utf-8").write(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
subprocess.run([sys.executable, os.path.join(ICI, "reordonner.py"), p], check=True)
os.remove(p)
