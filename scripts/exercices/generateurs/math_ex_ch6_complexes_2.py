# Exercice du ch. 6 (nombres complexes, partie 1), niveau facile : module, argument, forme trigonométrique.
# Usage : python -X utf8 scripts/exercices/generateurs/math_ex_ch6_complexes_2.py frontend/public/media/exercices/math_ex_ch6_complexes_2.json
# Gestes entraînés (cas_types module, forme_trigonometrique — 17 sujets sur 20 ; pièges : i dans la racine,
# (−a)² écrit négatif, angle lu sans regarder les signes, [2π] oublié, r négatif).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _commun_ch6 import *  # noqa
# SOURCES : voir _commun_ch6.SOURCES (vidéos des 10 professeurs, nationaux 2016-2025, séries marocaines, cours).

ID = "math_ex_ch6_complexes_2"
R3, R2 = 3 ** .5, 2 ** .5


def figure(a, b, ta, tb):
    return plan(f"Les points A({ta}) et B({tb})", "Le module est la distance à O ; l'argument est l'angle depuis u⃗.",
                [("A", a.real, a.imag, "cyan", "ne"), ("B", b.real, b.imag, "orange", "no")], xs=(-4, 3), ys=(-4, 3),
                autres=[{"f": "ligne", "pts": [[0, 0], [a.real, a.imag]], "couleur": "cyan", "trait": "pointille"},
                        {"f": "ligne", "pts": [[0, 0], [b.real, b.imag]], "couleur": "orange", "trait": "pointille"}])


def ass_angles():
    G = [("1", "cos θ = 1/2 et sin θ = √3/2"), ("2", "cos θ = √3/2 et sin θ = 1/2"), ("3", "cos θ = √2/2 et sin θ = √2/2")]
    D = [("a", "θ = π/6"), ("b", "θ = π/4"), ("c", "θ = π/3"), ("d", "θ = 2π/3")]
    C = {"1": "c", "2": "a", "3": "b"}
    R = {
      "1-a": ("π/6 a un cosinus √3/2, pas 1/2 : regarde où se trouve 1/2 dans le tableau.", "لا، pi sur six عندها cosinus racine de trois sur deux. شوف فين كاين un demi فـ le tableau."),
      "1-b": ("π/4 a cos et sin égaux ; ici ils sont différents.", "لا، pi sur quatre عندها cos و sin متساويين. هنا ماشي متساويين."),
      "1-c": ("Oui : cos π/3 = 1/2 et sin π/3 = √3/2.", "برافو: cos pi sur trois égale un demi، و sin pi sur trois égale racine de trois sur deux."),
      "1-d": ("2π/3 a un cosinus négatif, −1/2 ; ici cos θ = 1/2 est positif.", "لا، deux pi sur trois عندها cosinus négatif، moins un demi. هنا le cosinus positif."),
      "2-a": ("Oui : cos π/6 = √3/2 et sin π/6 = 1/2.", "برافو: cos pi sur six égale racine de trois sur deux، و sin pi sur six égale un demi."),
      "2-b": ("π/4 a cos et sin égaux ; ici ils sont différents.", "لا، pi sur quatre عندها cos و sin متساويين. هنا ماشي متساويين."),
      "2-c": ("Pour π/3, c'est le cosinus qui vaut 1/2 ; ici c'est le sinus.", "لا، فـ pi sur trois، le cosinus هو اللي كيساوي un demi. هنا le sinus."),
      "2-d": ("2π/3 a un cosinus négatif ; ici il est positif.", "لا، deux pi sur trois عندها cosinus négatif. هنا positif."),
      "3-a": ("π/6 a cos et sin différents ; ici ils sont égaux.", "لا، pi sur six، cos و sin ماشي متساويين. هنا متساويين."),
      "3-b": ("Oui : cos π/4 = sin π/4 = √2/2.", "برافو: cos pi sur quatre égale sin pi sur quatre، égale racine de deux sur deux."),
      "3-c": ("π/3 a cos et sin différents ; ici ils sont égaux.", "لا، pi sur trois، cos و sin ماشي متساويين. هنا متساويين."),
      "3-d": ("2π/3 a un cosinus négatif ; ici il est positif.", "لا، deux pi sur trois عندها cosinus négatif. هنا positif."),
    }
    return association("fa_c2_2", "Plus facile : reconnaître l'angle", "Relie chaque couple (cos θ ; sin θ) à son angle.",
      "سؤال ساهل: ربط كل cos و sin مع la valeur ديال teta.", "Relie chaque couple (cos θ ; sin θ) à l'angle θ.", G, D, C, R,
      ("(1 ; c) (2 ; a) (3 ; b) : 2π/3 est de trop, son cosinus est négatif.", "un مع c، deux مع a، trois مع b. deux pi sur trois زايدة: le cosinus ديالها négatif."))


EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "mathematiques", "chapitre": "operations_formes", "cours": "math_ch6_nombres_complexes",
  "titre": "Module, argument et forme trigonométrique", "niveau": "facile", "duree_min": 15,
  "origine": ORIGINE,
  "competences": ["Calculer un module |a + ib| = √(a² + b²)", "Écrire un complexe sous forme trigonométrique r(cos θ + i sin θ)",
                  "Choisir l'angle selon les signes de a et b (quadrants)"],
  "enonce": {
    "intro": "Dans le plan complexe rapporté à un repère orthonormé direct (O, u⃗, v⃗), on considère les points A et B d'affixes a = 1 + i√3 et b = −2 + 2i.",
    "intro_dit": "دابا نقراو l'énoncé. فـ le plan complexe، عندنا deux points: A، l'affixe ديالها a égale un plus i racine de trois، و B، l'affixe ديالها b égale moins deux plus deux i.",
    "figures": [figure(complex(1, R3), complex(-2, 2), "1 + i√3", "−2 + 2i")],
    "donnees": ["a = 1 + i√3", "b = −2 + 2i"],
    "questions": [
      question("1", "Calculer le module |a|.",
        "السؤال un: حسب le module de a.",
        valeur("|a|", 2, "|a| = √(1² + (√3)²) = √(1 + 3) = √4 = 2"),
        (["√(a² + b²)", "(√3)² = 3"], ["√(1 − 3)", "1 + √3"]),
        [("Le module est la distance OA : √(partie réelle² + partie imaginaire²), sans le i.",
          "le module هو la distance O A: la racine de، la partie réelle au carré، plus la partie imaginaire au carré، بلا i."),
         ("Ici la partie réelle vaut 1 et la partie imaginaire √3 ; (√3)² = 3.",
          "هنا la partie réelle un، و la partie imaginaire racine de trois. racine de trois، au carré، égale trois.")],
        [("1 : |a| = √(1² + (√3)²)", "le module de a"), ("= √(1 + 3) = √4", "racine de un plus trois"), ("donc |a| = 2", "égale deux")],
        "السؤال un. le module de a، égale la racine de، un au carré، plus، racine de trois au carré. يعني racine de un plus trois، racine de quatre. إذن le module de a égale deux.",
        "ex_c2_1", "fa_c2_1"),
      question("2", "Écrire a sous forme trigonométrique, puis donner un argument de a.",
        "السؤال deux: كتب a sous forme trigonométrique، ومن بعد عطي un argument de a.",
        phrase("a = 2(1/2 + (√3/2)i) = 2(cos π/3 + i sin π/3) ; arg a ≡ π/3 [2π]"),
        (["a = |a|(… + … i)", "cos π/3", "sin π/3", "[2π]"], ["π/6", "2(cos π/3 − i sin π/3)"]),
        [("Mets le module 2 en facteur : a = 2(1/2 + (√3/2)i).",
          "دير le module deux en facteur: a égale deux fois، un demi، plus racine de trois sur deux i."),
         ("Cherche dans le tableau l'angle θ tel que cos θ = 1/2 et sin θ = √3/2 (les deux positifs : premier quart).",
          "قلب فـ le tableau على teta: cos teta égale un demi، و sin teta égale racine de trois sur deux. les deux positifs: الربع اللول.")],
        [("2 : a = 2(1/2 + (√3/2)i)", "deux en facteur"),
         ("= 2(cos π/3 + i sin π/3)", "deux fois، cos pi sur trois، plus i sin pi sur trois"),
         ("donc arg a ≡ π/3 [2π]", "l'argument de a، congru à pi sur trois")],
        "السؤال deux. كنديرو deux en facteur: a égale deux fois، un demi، plus racine de trois sur deux i. un demi هو cos pi sur trois، و racine de trois sur deux هو sin pi sur trois. إذن a égale deux fois، cos pi sur trois، plus i sin pi sur trois. و l'argument de a، congru à pi sur trois، modulo deux pi.",
        "ex_c2_2", "fa_c2_2"),
      question("3", "Calculer le module |b|.",
        "السؤال trois: حسب le module de b.",
        phrase("|b| = √((−2)² + 2²) = √(4 + 4) = √8 = 2√2"),
        (["(−2)² = 4", "√8 = 2√2"], ["√(−4 + 4)", "√(4 − 4)"]),
        [("La partie réelle est −2 : son carré est (−2)² = 4, un carré n'est jamais négatif.",
          "la partie réelle هي moins deux: le carré ديالها quatre. le carré عمرو ما يكون négatif."),
         ("|b| = √(4 + 4) = √8 ; simplifie : √8 = √(4 × 2) = 2√2.",
          "le module de b، égale racine de huit. نبسطوها: racine de huit، égale deux racine de deux.")],
        [("3 : |b| = √((−2)² + 2²)", "le module de b"), ("= √(4 + 4) = √8", "racine de quatre plus quatre"), ("donc |b| = 2√2", "deux racine de deux")],
        "السؤال trois. le module de b، égale la racine de، moins deux au carré، plus deux au carré. moins deux au carré égale quatre. إذن racine de quatre plus quatre، يعني racine de huit. و racine de huit، égale deux racine de deux.",
        "ex_c2_3", "fa_c2_3"),
      question("4", "Écrire b sous forme trigonométrique.",
        "السؤال quatre: كتب b sous forme trigonométrique.",
        phrase("b = 2√2(−√2/2 + (√2/2)i) = 2√2(cos 3π/4 + i sin 3π/4) ; arg b ≡ 3π/4 [2π]"),
        (["b = 2√2(… + … i)", "π − π/4", "cos 3π/4", "[2π]"], ["π/4", "−2√2(cos π/4 + i sin π/4)"]),
        [("Mets 2√2 en facteur : −2/(2√2) = −√2/2 et 2/(2√2) = √2/2.",
          "دير deux racine de deux en facteur: moins deux، sur deux racine de deux، égale moins racine de deux sur deux. و deux sur deux racine de deux، égale racine de deux sur deux."),
         ("Le cosinus est négatif et le sinus positif : B est à gauche et en haut, l'angle est π − π/4.",
          "le cosinus négatif و le sinus positif: B على اليسار والفوق. الزاوية هي pi moins pi sur quatre.")],
        [("4 : b = 2√2(−√2/2 + (√2/2)i)", "deux racine de deux en facteur"),
         ("cos θ < 0 et sin θ > 0 : θ = π − π/4 = 3π/4", "pi moins pi sur quatre"),
         ("b = 2√2(cos 3π/4 + i sin 3π/4) ; arg b ≡ 3π/4 [2π]", "cos trois pi sur quatre")],
        "السؤال quatre. كنديرو deux racine de deux en facteur: b égale deux racine de deux، fois، moins racine de deux sur deux، plus racine de deux sur deux i. le cosinus négatif و le sinus positif: الربع الثاني. الزاوية: pi moins pi sur quatre، يعني trois pi sur quatre. إذن b égale deux racine de deux، fois، cos trois pi sur quatre، plus i sin trois pi sur quatre.",
        "ex_c2_4", "fa_c2_4"),
    ]},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    anime("ex_c2_1", "Question 1 : le module, une distance", "|a + ib| = OM = √(a² + b²), par Pythagore.",
      "module.html?vue=triangle", "Le triangle rectangle OHM et Pythagore",
      "شوف النقطة M، de coordonnées trois، quatre. كنسقطوها على l'axe réel: النقطة H. le triangle O H M قايم فـ H. Pythagore: O M au carré، égale trois au carré plus quatre au carré، égale vingt-cinq. إذن O M égale cinq: هادا هو le module de trois plus quatre i. فالتمرين ديالنا: un au carré، plus racine de trois au carré، égale quatre. إذن le module de a égale deux.",
      [("|a| = √(1² + (√3)²) = √4", "فالتمرين ديالنا"), ("|a| = 2", "إذن le module de a égale deux")],
      [("شوف النقطة M", "play_until", "point"), ("le triangle O H M", "play_until", "triangle"),
       ("Pythagore", "play_until", "pythagore"), ("فالتمرين ديالنا", "centre", 0), ("إذن le module de a égale deux", "centre", 1)]),
    anime("ex_c2_2", "Question 2 : du module à l'angle", "a = r(a/r + (b/r)i), puis on lit cos θ et sin θ dans le tableau.",
      "trig.html?vue=passage", "Le passage de √3 + i à la forme trigonométrique",
      "شوف النقطة racine de trois plus i. اللول، le module: deux. من بعد كنديرو deux en facteur: racine de trois sur deux، plus un demi i. فـ le tableau: racine de trois sur deux هو cos pi sur six، و un demi هو sin pi sur six. القوس كيترسم. la forme trigonométrique: deux fois، cos pi sur six، plus i sin pi sur six. فالتمرين ديالنا، العكس: un demi هو le cosinus، و racine de trois sur deux هو le sinus. الزاوية pi sur trois.",
      [("a = 2(1/2 + (√3/2)i)", "فالتمرين ديالنا"), ("= 2(cos π/3 + i sin π/3)", "الزاوية pi sur trois")],
      [("شوف النقطة", "play_until", "point"), ("اللول، le module", "play_until", "module"),
       ("كنديرو deux en facteur", "play_until", "facteur"), ("القوس كيترسم", "play_until", "angle"),
       ("la forme trigonométrique", "play_until", "forme"), ("فالتمرين ديالنا", "centre", 0), ("الزاوية pi sur trois", "centre", 1)]),
    anime("ex_c2_3", "Question 3 : un carré n'est jamais négatif", "(−2)² = 4 ; et le i ne rentre jamais dans la racine.",
      "module.html?vue=cercle", "Le cercle de rayon 5 et les deux erreurs à éviter",
      "شوف le cercle، le centre ديالو O، و le rayon ديالو cinq. النقطة M كتمشي عليه، كدوز من moins trois plus quatre i. le module كيبقى cinq. la règle: la racine de، a carré plus b carré. a و b réels، و i ما كيدخلش لداخل la racine. ورد بالك: moins racine de trois، au carré، égale trois. le carré عمرو ما يكون négatif. فالتمرين ديالنا: moins deux au carré، égale quatre. إذن racine de huit، يعني deux racine de deux.",
      [("|b| = √((−2)² + 2²) = √(4 + 4)", "فالتمرين ديالنا"), ("= √8 = 2√2", "يعني deux racine de deux")],
      [("شوف le cercle", "play_until", "cercle"), ("كدوز من moins trois plus quatre i", "play_until", "autres"),
       ("la règle", "play_until", "sans_i"), ("فالتمرين ديالنا", "centre", 0), ("يعني deux racine de deux", "centre", 1)]),
    anime("ex_c2_4", "Question 4 : regarder les signes avant l'angle", "Cosinus négatif, sinus positif : θ = π − (angle du tableau).",
      "trig.html?vue=signes", "−√3 + i : le point à gauche et en haut",
      "شوف النقطة moins racine de trois plus i. هي على اليسار والفوق: a négatif، و b positif. le module deux. كنديرو deux en facteur: moins racine de trois sur deux، plus un demi i. رد بالك: ماشي pi sur six، حيت le cosinus négatif. القوس كيوصل للربع الثاني: pi moins pi sur six، يعني cinq pi sur six. فالتمرين ديالنا: B حتى هي على اليسار والفوق. le tableau كيعطي pi sur quatre، والزاوية هي pi moins pi sur quatre، يعني trois pi sur quatre.",
      [("b = 2√2(−√2/2 + (√2/2)i)", "فالتمرين ديالنا"), ("θ = π − π/4 = 3π/4", "يعني trois pi sur quatre")],
      [("شوف النقطة", "play_until", "point"), ("le module deux", "play_until", "module"),
       ("كنديرو deux en facteur", "play_until", "facteur"), ("القوس كيوصل للربع الثاني", "play_until", "angle"),
       ("يعني cinq pi sur six", "play_until", "forme"), ("فالتمرين ديالنا", "centre", 0), ("يعني trois pi sur quatre", "centre", 1)]),
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm("fa_c2_1", "Plus facile : un module", "نتمرنو بسؤال ساهل: شحال كيساوي le module ديال un plus i racine de trois؟",
      "|1 + i√3| = ?", ["2", "4", "1 + √3"], 0, {
        "0": {"juste": rep("برافو! la racine de، un plus trois، égale racine de quatre، يعني deux.", "Juste : √(1 + 3) = √4 = 2.")},
        "1": {"1": rep("قريب! un plus trois égale quatre، ولكن le module هو la racine. عاود اختار.", "1 + 3 = 4, mais le module est la racine de ce nombre. Réessaie."),
              "2": rep("الجواب هو deux: la racine de quatre.", "Réponse : 2 = √4.")},
        "2": {"1": rep("ما تقلقش. le module ماشي la somme ديال les parties. خاصنا la racine des carrés. عاود اختار.", "Le module n'est pas la somme des parties : c'est la racine de la somme des carrés. Réessaie."),
              "2": rep("الجواب هو deux: la racine de، un au carré plus racine de trois au carré.", "Réponse : √(1² + (√3)²) = 2.")}},
      "Le module de un plus i racine de trois égale ?"),
    ass_angles(),
    vrai_faux("fa_c2_3", "Plus facile : vrai ou faux", "Le module de a + ib (a, b réels) est √(a² + b²).",
      "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.", [
        ("|−2 + 2i| = √(−4 + 4) = 0", False, "(−2)² = 4, pas −4 : |−2 + 2i| = √8 = 2√2."),
        ("|−2 + 2i| = √8 = 2√2", True, "√((−2)² + 2²) = √8 = √(4 × 2) = 2√2."),
        ("|3i| = √(3i)²", False, "Le i ne rentre pas dans la racine : |3i| = √(0² + 3²) = 3.")]),
    qcm("fa_c2_4", "Plus facile : le bon angle", "سؤال ساهل: le cosinus négatif و le sinus positif. شمن زاوية؟",
      "cos θ = −√2/2 et sin θ = √2/2. Alors θ ≡ … [2π]", ["π/4", "3π/4", "−π/4", "5π/4"], 1, {
        "1": {"juste": rep("برافو! cosinus négatif و sinus positif: الربع الثاني. pi moins pi sur quatre، يعني trois pi sur quatre.", "Juste : θ = π − π/4 = 3π/4.")},
        "0": {"1": rep("قريب! pi sur quatre عندها cosinus positif. هنا le cosinus négatif. عاود اختار.", "cos π/4 est positif ; ici le cosinus est négatif. Réessaie."),
              "2": rep("الجواب هو trois pi sur quatre: pi moins pi sur quatre.", "Réponse : 3π/4.")},
        "2": {"1": rep("ما تقلقش. moins pi sur quatre عندها sinus négatif، التحت. هنا le sinus positif. عاود اختار.", "sin(−π/4) est négatif ; ici le sinus est positif. Réessaie."),
              "2": rep("الجواب هو trois pi sur quatre: اليسار والفوق.", "Réponse : 3π/4.")},
        "3": {"1": rep("قريب! cinq pi sur quatre هي اليسار والتحت: le sinus négatif. هنا le sinus positif. عاود اختار.", "5π/4 : à gauche et en bas, sinus négatif. Réessaie."),
              "2": rep("الجواب هو trois pi sur quatre: اليسار والفوق.", "Réponse : 3π/4.")}},
      "Cos teta égale moins racine de deux sur deux، et sin teta égale racine de deux sur deux. Teta égale ?"),
  ]}]},
  "similaire": {"id": ID + "_b", "titre": "Même exercice, autres données", "enonce": {
    "intro": "Dans le plan complexe rapporté à un repère orthonormé direct (O, u⃗, v⃗), on considère les points A et B d'affixes a = √3 − i et b = −3 − 3i.",
    "intro_dit": "نفس التمرين، بأعداد أخرى: a égale racine de trois moins i، و b égale moins trois moins trois i.",
    "figures": [figure(complex(R3, -1), complex(-3, -3), "√3 − i", "−3 − 3i")],
    "donnees": ["a = √3 − i", "b = −3 − 3i"],
    "questions": [
      question("1", "Calculer le module |a|.", None, valeur("|a|", 2, "|a| = √((√3)² + (−1)²) = √4 = 2"),
        (["√(a² + b²)"], ["√(3 − 1)"]), None,
        [("|a| = √(3 + 1)", "racine de trois plus un"), ("|a| = 2", "égale deux")],
        "le module de a، égale racine de trois plus un، يعني racine de quatre، égale deux."),
      question("2", "Écrire a sous forme trigonométrique, puis donner un argument de a.", None,
        phrase("a = 2(√3/2 − (1/2)i) = 2(cos(−π/6) + i sin(−π/6)) ; arg a ≡ −π/6 [2π]"),
        (["cos(−π/6)", "[2π]"], ["π/6", "2(cos π/6 − i sin π/6)"]), None,
        [("a = 2(√3/2 − (1/2)i)", "deux en facteur"), ("= 2(cos(−π/6) + i sin(−π/6))", "moins pi sur six")],
        "deux en facteur: racine de trois sur deux، moins un demi i. le sinus négatif: الربع الرابع، الزاوية moins pi sur six. إذن a égale deux fois، cos moins pi sur six، plus i sin moins pi sur six."),
      question("3", "Calculer le module |b|.", None, phrase("|b| = √((−3)² + (−3)²) = √18 = 3√2"),
        (["(−3)² = 9", "√18 = 3√2"], ["√(−9 − 9)"]), None,
        [("|b| = √(9 + 9) = √18", "racine de dix-huit"), ("|b| = 3√2", "trois racine de deux")],
        "le module de b، égale racine de neuf plus neuf، يعني racine de dix-huit، égale trois racine de deux."),
      question("4", "Écrire b sous forme trigonométrique.", None,
        phrase("b = 3√2(−√2/2 − (√2/2)i) = 3√2(cos(−3π/4) + i sin(−3π/4)) ; arg b ≡ −3π/4 [2π]"),
        (["−π + π/4", "cos(−3π/4)"], ["π/4", "3π/4"]), None,
        [("b = 3√2(−√2/2 − (√2/2)i)", "trois racine de deux en facteur"), ("= 3√2(cos(−3π/4) + i sin(−3π/4))", "moins trois pi sur quatre")],
        "trois racine de deux en facteur: moins racine de deux sur deux، moins racine de deux sur deux i. les deux négatifs: اليسار والتحت. الزاوية moins trois pi sur quatre. إذن b égale trois racine de deux، fois، cos moins trois pi sur quatre، plus i sin moins trois pi sur quatre."),
    ]}},
}

if __name__ == "__main__":
    ecrire(EX, sys.argv[1])
