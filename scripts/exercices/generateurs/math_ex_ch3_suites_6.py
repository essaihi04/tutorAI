# Exercice de maths, ch. 3 (suites numériques), niveau supérieur (au-dessus du national, même forme) :
# une suite qui n'est PAS monotone, étudiée par |uₙ₊₁ − ℓ| ≤ k|uₙ − ℓ|, puis un seuil.
# Sources comparées (lecture seule, rien de recopié) :
#  - exploration suites_definition.json : cadre SU8 (« |uₙ₊₁ − ℓ| ≤ k|uₙ − ℓ| … méthode autorisée, 2020 N, 2021 N, 2025 R »),
#    SU11 (plus petit entier n), redaction_nationale majoration_kn et seuil ; erreurs_examen « limite après une majoration en
#    kⁿ » (citer la comparaison), « déduire uₙ ≤ kⁿu₀ » (récurrence courte) ; pieges « multiplie membre à membre sans
#    vérifier les signes », « u₀ > u₁ ne prouve pas la monotonie » ;
#  - vidéos : Aderdour 5d4DjGTpbu4 (national 2020 : 0 < uₙ₊₁ ≤ (2/5)uₙ, puis (3/2)(2/5)ⁿ), maths variés wXGsw_meVIM
#    (national 2020, recoller les inégalités), Mouad Tahiri b7iH3KUEoZc (récurrence uₙ₊₁ ≤ k·uₙ ≤ k·kⁿu₀) ;
#  - nationaux : 2020 N 3-a / 3-b, 2021 N 4-a, 2025 R 2-c à 2-e (majoration en kⁿ) ; 2017 R 2-c, 2021 R 4 (seuil) —
#    au national la suite est toujours monotone ; ici f est décroissante et la suite oscille autour de 2 : le théorème
#    « monotone et bornée » ne s'applique pas, d'où la méthode de l'écart (niveau au-dessus) ;
#  - séries en ligne (résultats de recherche, pages non ouvertes : réseau fermé) : talamidi 2 bac PC série corrigée 3,
#    fayssalmaths série 3 « limite d'une suite » (2 BIOF), moutamadris 2 bac PC/SVT série 1, pdfmath exercices nationaux
#    corrigés, talamidi examen simili 4.
# Données propres à Moalim : u₀ = 1, uₙ₊₁ = (uₙ + 6)/(uₙ + 2), ℓ = 2, k = 1/3 ; seuil 10⁻³ (3⁷ = 2187).
import sys
from fractions import Fraction as Fr
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa: E402,F401,F403

ID = "math_ex_ch3_suites_6"
S = "/media/simulations/maths/suites-tableau/"


def nuage(f, u0):
    u = [Fr(u0)]
    for _ in range(6):
        u.append(f(u[-1]))
    el = [{"f": "repere", "y": 2, "t": "y = 2", "couleur": "jaune"}]
    for k, v in enumerate(u):
        p = {"f": "point", "at": [k, round(float(v), 3)], "couleur": "cyan"}
        if k < 3:
            p.update({"t": "u" + "₀₁₂"[k], "pos": "n" if v > 2 else "s"})
        el.append(p)
    el.append({"f": "ligne", "pts": [[k, round(float(v), 3)] for k, v in enumerate(u)], "couleur": "faible", "trait": "pointille"})
    return {"type": "courbe", "titre": "Les premiers termes : les points (n ; uₙ)",
            "axes": {"x": {"min": 0, "max": 7, "nom": "n", "graduations": [1, 2, 3, 4, 5, 6]},
                     "y": {"min": 0, "max": 3, "nom": "uₙ", "graduations": [1, 2, 3]}},
            "legende": "Les points passent d'un côté à l'autre de la droite y = 2, de plus en plus près d'elle.", "elements": el}


QUESTIONS = [
    {"id": "1", "texte": "Calculer u₁ et u₂. La suite (uₙ) est-elle monotone ? Justifier.",
     "texte_dit": "السؤال un: حسب u un وu deux. واش la suite monotone؟ برر.",
     "reponse": phrase("u₁ = (1 + 6)/(1 + 2) = 7/3 et u₂ = (7/3 + 6)/(7/3 + 2) = (25/3)/(13/3) = 25/13. On a u₀ < u₁ mais u₁ > u₂ (car 25/13 < 2 < 7/3) : la suite n'est ni croissante ni décroissante, elle n'est pas monotone."),
     "clavier": {"aides": ["u₁ = 7/3", "u₂ = 25/13", "u₀ < u₁", "u₁ > u₂", "n'est pas monotone"], "pieges": ["u₀ < u₁ donc croissante", "u₂ = 25/3"]},
     "aides": [aide("u₁ = f(u₀) avec u₀ = 1 ; pour u₂, garde des fractions : 7/3 + 6 = 25/3 et 7/3 + 2 = 13/3.",
                    "u un، عوض u zéro ب un. وu deux، خلي les fractions: sept sur trois plus six égale vingt-cinq sur trois، وsept sur trois plus deux égale treize sur trois."),
               aide("Monotone veut dire toujours croissante ou toujours décroissante. Compare u₀ et u₁, puis u₁ et u₂.",
                    "monotone يعني ديما croissante ولا ديما décroissante. قارن u zéro مع u un، ومن بعد u un مع u deux.")],
     "correction": correction([
         ("1 : u₁ = (1 + 6)/(1 + 2) = 7/3", "u un égale sept sur trois"),
         ("u₂ = (7/3 + 6)/(7/3 + 2) = (25/3)/(13/3) = 25/13", "u deux égale vingt-cinq sur treize"),
         ("u₀ < u₁ et u₁ > u₂ : (uₙ) n'est pas monotone", "n'est pas monotone")],
         "السؤال un. u un égale un plus six، sur un plus deux: u un égale sept sur trois. u deux: vingt-cinq sur trois، sur treize sur trois، يعني u deux égale vingt-cinq sur treize. u zéro أصغر من u un، ولكن u un أكبر من u deux. طلعات ومن بعد هبطات: la suite n'est pas monotone."),
     "explication": "ex_1", "facile": "fa_1"},
    {"id": "2", "texte": "Vérifier que uₙ₊₁ = 1 + 4/(uₙ + 2) pour tout n, puis montrer par récurrence que uₙ ≥ 1 pour tout entier naturel n.",
     "texte_dit": "السؤال deux: تحقق بلي u indice n plus un égale un plus quatre sur، u indice n plus deux. ومن بعد بين par récurrence بلي u indice n supérieur ou égal à un.",
     "reponse": phrase("1 + 4/(uₙ + 2) = (uₙ + 2 + 4)/(uₙ + 2) = (uₙ + 6)/(uₙ + 2) = uₙ₊₁. Initialisation : u₀ = 1 ≥ 1. Hérédité : si uₙ ≥ 1, alors uₙ + 2 ≥ 3 > 0, donc 4/(uₙ + 2) > 0 et uₙ₊₁ = 1 + 4/(uₙ + 2) > 1, donc uₙ₊₁ ≥ 1. Conclusion : uₙ ≥ 1 pour tout n."),
     "clavier": {"aides": ["(uₙ + 2 + 4)/(uₙ + 2)", "uₙ + 2 > 0", "4/(uₙ + 2) > 0", "uₙ₊₁ > 1"], "pieges": ["uₙ ≥ 1 ⇒ uₙ + 6 ≥ 7 et uₙ + 2 ≥ 3 ⇒ uₙ₊₁ ≥ 7/3"]},
     "aides": [aide("Pars de 1 + 4/(uₙ + 2) et réduis au même dénominateur. Cette écriture n'a plus uₙ qu'une fois.",
                    "بدا من un plus quatre sur، u indice n plus deux، ودير نفس المقام. هاد الكتابة فيها u indice n غير مرة وحدة."),
               aide("Avec uₙ ≥ 1 : uₙ + 2 est positif, donc 4/(uₙ + 2) est positif ; ajoute 1.",
                    "مع u indice n أكبر من un: u indice n plus deux positif، إذن quatre sur، u indice n plus deux، positif. زيد un.")],
     "correction": correction([
         ("2 : 1 + 4/(uₙ + 2) = (uₙ + 2 + 4)/(uₙ + 2) = (uₙ + 6)/(uₙ + 2) = uₙ₊₁", "même dénominateur"),
         ("Initialisation : u₀ = 1 ≥ 1", "u zéro égale un"),
         ("Hérédité : supposons uₙ ≥ 1 : uₙ + 2 ≥ 3 > 0, donc 4/(uₙ + 2) > 0 et uₙ₊₁ = 1 + 4/(uₙ + 2) > 1, donc uₙ₊₁ ≥ 1", "supposons que u indice n"),
         ("Conclusion : d'après le principe de récurrence, uₙ ≥ 1 pour tout n", "d'après le principe de récurrence")],
         "السؤال deux. même dénominateur: u indice n plus deux plus quatre، sur u indice n plus deux، يعني u indice n plus six، sur u indice n plus deux: هادي u indice n plus un. initialisation: u zéro égale un. hérédité: supposons que u indice n supérieur ou égal à un. u indice n plus deux positif، إذن quatre sur، u indice n plus deux، positif، وu indice n plus un أكبر من un. d'après le principe de récurrence، u indice n supérieur ou égal à un pour tout n."),
     "explication": "ex_2", "facile": "fa_2"},
    {"id": "3-1", "texte": "Vérifier que uₙ₊₁ − 2 = −(uₙ − 2)/(uₙ + 2) pour tout n.",
     "texte_dit": "السؤال trois un: تحقق بلي u indice n plus un moins deux، égale moins، u indice n moins deux، sur u indice n plus deux.",
     "reponse": phrase("uₙ₊₁ − 2 = (uₙ + 6 − 2(uₙ + 2))/(uₙ + 2) = (uₙ + 6 − 2uₙ − 4)/(uₙ + 2) = (2 − uₙ)/(uₙ + 2) = −(uₙ − 2)/(uₙ + 2)."),
     "clavier": {"aides": ["2 = 2(uₙ + 2)/(uₙ + 2)", "uₙ + 6 − 2uₙ − 4", "2 − uₙ = −(uₙ − 2)"], "pieges": ["uₙ + 6 − 2uₙ + 4", "(uₙ − 2)/(uₙ + 2)"]},
     "aides": [aide("Même dénominateur : 2 = 2(uₙ + 2)/(uₙ + 2). Attention au signe moins devant la parenthèse.",
                    "نفس المقام: deux égale deux fois، u indice n plus deux، sur u indice n plus deux. رد البال للmoins اللي قدام la parenthèse."),
               aide("Le numérateur donne 2 − uₙ, qui s'écrit −(uₙ − 2).",
                    "le numérateur كيعطي deux moins u indice n، وهي كتكتب moins، u indice n moins deux.")],
     "correction": correction([
         ("3-1 : uₙ₊₁ − 2 = (uₙ + 6 − 2(uₙ + 2))/(uₙ + 2)", "même dénominateur"),
         ("= (uₙ + 6 − 2uₙ − 4)/(uₙ + 2) = (2 − uₙ)/(uₙ + 2)", "deux moins u indice n"),
         ("= −(uₙ − 2)/(uₙ + 2)", "moins، u indice n moins deux")],
         "السؤال trois un. même dénominateur: u indice n plus six، moins deux fois، u indice n plus deux. نوزعو le moins: u indice n plus six moins deux u indice n moins quatre، كتعطي deux moins u indice n. وdeux moins u indice n égale moins، u indice n moins deux. إذن la fraction égale moins، u indice n moins deux، sur u indice n plus deux."),
     "explication": "ex_3", "facile": "fa_3"},
    {"id": "3-2", "texte": "Montrer que |uₙ₊₁ − 2| ≤ (1/3)|uₙ − 2| pour tout entier naturel n.",
     "texte_dit": "السؤال trois deux: بين بلي la valeur absolue ديال u indice n plus un moins deux، inférieur ou égal à un sur trois، fois la valeur absolue ديال u indice n moins deux.",
     "reponse": phrase("D'après 3-1, |uₙ₊₁ − 2| = |uₙ − 2|/(uₙ + 2) car uₙ + 2 > 0. D'après 2, uₙ ≥ 1, donc uₙ + 2 ≥ 3 et 1/(uₙ + 2) ≤ 1/3. Donc |uₙ₊₁ − 2| ≤ (1/3)|uₙ − 2|."),
     "clavier": {"aides": ["|−a| = |a|", "|uₙ − 2|/(uₙ + 2)", "uₙ + 2 ≥ 3", "1/(uₙ + 2) ≤ 1/3"], "pieges": ["1/(uₙ + 2) ≥ 1/3", "uₙ + 2 ≥ 2"]},
     "aides": [aide("Prends la valeur absolue de l'égalité 3-1 : le signe « − » disparaît, et uₙ + 2 est positif.",
                    "خود la valeur absolue ديال l'égalité ديال trois un: le moins كيمشي، وu indice n plus deux positif."),
               aide("La question 2 donne uₙ ≥ 1, donc uₙ + 2 ≥ 3. Passer à l'inverse de nombres positifs change le sens.",
                    "السؤال deux كيعطي u indice n أكبر من un، إذن u indice n plus deux أكبر من trois. والمقلوب ديال أعداد positifs كيبدل الاتجاه.")],
     "correction": correction([
         ("3-2 : |uₙ₊₁ − 2| = |uₙ − 2|/(uₙ + 2) (car uₙ + 2 > 0)", "la valeur absolue"),
         ("d'après 2, uₙ ≥ 1 donc uₙ + 2 ≥ 3, donc 1/(uₙ + 2) ≤ 1/3", "un sur trois"),
         ("donc |uₙ₊₁ − 2| ≤ (1/3)|uₙ − 2|", "inférieur ou égal à un sur trois fois")],
         "السؤال trois deux. la valeur absolue ديال u indice n plus un moins deux، égale la valeur absolue ديال u indice n moins deux، sur u indice n plus deux، حيت هاد الأخير positif. d'après le deux، u indice n plus deux أكبر من trois، إذن المقلوب ديالو أصغر من un sur trois. إذن inférieur ou égal à un sur trois fois la valeur absolue ديال u indice n moins deux."),
     "explication": "ex_4", "facile": "fa_4"},
    {"id": "4", "texte": "En déduire par récurrence que |uₙ − 2| ≤ (1/3)ⁿ pour tout n, puis déterminer la limite de (uₙ).",
     "texte_dit": "السؤال quatre: استنتج par récurrence بلي la valeur absolue ديال u indice n moins deux، inférieur ou égal à un sur trois puissance n. ومن بعد لقا la limite ديال la suite.",
     "reponse": valeur("lim uₙ", 2, "n = 0 : |u₀ − 2| = 1 = (1/3)⁰ ; si |uₙ − 2| ≤ (1/3)ⁿ, alors |uₙ₊₁ − 2| ≤ (1/3)|uₙ − 2| ≤ (1/3)ⁿ⁺¹ ; donc |uₙ − 2| ≤ (1/3)ⁿ ; −1 < 1/3 < 1 donc lim (1/3)ⁿ = 0, et par comparaison lim uₙ = 2"),
     "clavier": {"aides": ["|u₀ − 2| = 1 = (1/3)⁰", "(1/3) × (1/3)ⁿ = (1/3)ⁿ⁺¹", "lim (1/3)ⁿ = 0", "par comparaison", "lim uₙ ="],
                 "pieges": ["(1/3)⁰ = 0", "lim uₙ = lim (1/3)ⁿ = 0"]},
     "aides": [aide("Initialisation : |u₀ − 2| = |1 − 2| = 1, et (1/3)⁰ = 1. Hérédité : enchaîne l'inégalité de 3-2 avec l'hypothèse.",
                    "initialisation: la valeur absolue ديال u zéro moins deux égale un، وun sur trois puissance zéro égale un. hérédité: ربط l'inégalité ديال trois deux مع l'hypothèse."),
               aide("Pour la limite : l'écart |uₙ − 2| est coincé entre 0 et (1/3)ⁿ, qui tend vers 0 car −1 < 1/3 < 1.",
                    "وla limite: l'écart محصور بين zéro وun sur trois puissance n، وهادي كتمشي ل zéro حيت un sur trois بين moins un وun.")],
     "correction": correction([
         ("4 : Initialisation : |u₀ − 2| = 1 = (1/3)⁰", "un sur trois puissance zéro"),
         ("Hérédité : si |uₙ − 2| ≤ (1/3)ⁿ, alors |uₙ₊₁ − 2| ≤ (1/3)|uₙ − 2| ≤ (1/3) × (1/3)ⁿ = (1/3)ⁿ⁺¹", "puissance n plus un"),
         ("Conclusion : |uₙ − 2| ≤ (1/3)ⁿ pour tout n", "pour tout n"),
         ("−1 < 1/3 < 1 donc lim (1/3)ⁿ = 0 ; par comparaison, lim |uₙ − 2| = 0 : lim uₙ = 2", "la limite égale deux")],
         "السؤال quatre. initialisation: l'écart ديال u zéro égale un، وun sur trois puissance zéro égale un. hérédité: l'écart ديال u indice n plus un، inférieur ou égal à un sur trois fois l'écart ديال u indice n، inférieur ou égal à un sur trois fois un sur trois puissance n، يعني un sur trois puissance n plus un. conclusion: صحيح pour tout n. ومن بعد، moins un inférieur à un sur trois، inférieur à un، إذن un sur trois puissance n كتمشي ل zéro. par comparaison، l'écart كيمشي ل zéro: la limite égale deux."),
     "explication": "ex_5", "facile": "fa_5"},
    {"id": "5", "texte": "Déterminer le plus petit entier naturel n tel que (1/3)ⁿ ≤ 10⁻³. En déduire un rang à partir duquel |uₙ − 2| ≤ 10⁻³.",
     "texte_dit": "السؤال cinq: لقا أصغر entier n، اللي فيه un sur trois puissance n، inférieur ou égal à dix puissance moins trois. ومن بعد استنتج رتبة، من بعدها l'écart ديال u indice n على deux، inférieur ou égal à dix puissance moins trois.",
     "reponse": valeur("n", 7, "(1/3)ⁿ ≤ 10⁻³ ⇔ 3ⁿ ≥ 1000 ; 3⁶ = 729 < 1000 et 3⁷ = 2187 ≥ 1000 ; donc pour n ≥ 7, |uₙ − 2| ≤ (1/3)ⁿ ≤ 10⁻³ ; plus petit entier : n = 7"),
     "clavier": {"aides": ["3ⁿ ≥ 1000", "3⁶ = 729", "3⁷ = 2187", "n ≥ 7"], "pieges": ["n = 6", "n = 1000/3"]},
     "aides": [aide("(1/3)ⁿ ≤ 1/1000 revient à 3ⁿ ≥ 1000 (on passe aux inverses de nombres positifs). Calcule les puissances de 3.",
                    "un sur trois puissance n inférieur ou égal à un sur mille، يعني trois puissance n supérieur ou égal à mille. حسب les puissances ديال trois."),
               aide("3⁵ = 243, 3⁶ = 729, 3⁷ = … : lequel dépasse 1000 en premier ? Les puissances de 3 augmentent avec n.",
                    "trois puissance cinq égale deux cent quarante-trois، trois puissance six égale sept cent vingt-neuf. واشمن وحدة كتفوت mille الأولى؟")],
     "correction": correction([
         ("5 : (1/3)ⁿ ≤ 10⁻³ ⇔ 3ⁿ ≥ 1000", "trois puissance n supérieur ou égal à mille"),
         ("3⁶ = 729 < 1000 et 3⁷ = 2187 ≥ 1000 : le plus petit entier est n = 7", "deux mille cent quatre-vingt-sept"),
         ("pour n ≥ 7 : |uₙ − 2| ≤ (1/3)ⁿ ≤ 10⁻³", "à partir de n égale sept")],
         "السؤال cinq. un sur trois puissance n inférieur ou égal à dix puissance moins trois، يعني trois puissance n supérieur ou égal à mille. trois puissance six égale sept cent vingt-neuf، أصغر من mille. trois puissance sept égale deux mille cent quatre-vingt-sept، أكبر من mille. إذن le plus petit entier هو sept. à partir de n égale sept، l'écart ديال u indice n على deux، inférieur ou égal à dix puissance moins trois."),
     "explication": "ex_6", "facile": "fa_6"},
]

EXPLICATION = deck("explication", "Explication animée", [
    sim("ex_1", "Question 1 : deux termes ne font pas une monotonie", "u₀ < u₁ puis u₁ > u₂ : la suite monte puis descend.",
        S + "nuage.html?vue=monotonie", "u₁ > u₀, et pourtant la suite n'est pas croissante",
        "شوف هاد l'exemple: u zéro égale deux، وu un égale trois. طلعات. ولكن النقط اللي من بعد كيهبطو. إذن جوج نقط ما كيقولوش le sens ديال la suite. عندنا: u un égale sept sur trois، أكبر من u zéro. وu deux égale vingt-cinq sur treize، أصغر من u un. طلعات ومن بعد هبطات: la suite n'est pas monotone. إذن ما نقدروش نستعملو monotone et bornée: خاصنا طريقة أخرى.",
        [("u₀ < u₁ et u₁ > u₂", "طلعات ومن بعد هبطات"), ("pas monotone : autre méthode", "خاصنا طريقة أخرى")],
        [jusqua("شوف هاد l'exemple", "deux_points"), jusqua("طلعات.", "fleche"), jusqua("ولكن النقط اللي من بعد", "suite"),
         jusqua("إذن جوج نقط", "contre_exemple"), montre("طلعات ومن بعد هبطات", "centre:0"), montre("خاصنا طريقة أخرى", "centre:1")]),
    sim("ex_2", "Question 2 : l'écriture donnée", "Avec uₙ une seule fois, on raisonne par opérations sur l'hypothèse.",
        S + "calculs.html?vue=r6", "L'écriture donnée par l'énoncé, dans l'exemple du cours",
        "فl'exemple ديال le cours، l'énoncé كيعطي كتابة أخرى ديال u indice n plus un. كنتحققو منها بنفس المقام. وهاد الكتابة فيها u indice n غير مرة وحدة: إذن نقدرو نديرو العمليات. عندنا: un plus quatre sur، u indice n plus deux، égale u indice n plus six، sur u indice n plus deux. مع u indice n أكبر من un، u indice n plus deux positif، إذن quatre sur، u indice n plus deux، positif. إذن u indice n plus un أكبر من un.",
        [("uₙ₊₁ = 1 + 4/(uₙ + 2)", "عندنا"), ("4/(uₙ + 2) > 0 ⇒ uₙ₊₁ > 1", "إذن u indice n plus un أكبر من un")],
        [jusqua("فl'exemple ديال le cours", "enonce"), jusqua("كنتحققو منها", "verifier"), jusqua("وهاد الكتابة", "outil"),
         montre("عندنا", "centre:0"), montre("إذن u indice n plus un أكبر من un", "centre:1")]),
    sim("ex_3", "Question 3-1 : même dénominateur", "On écrit 2 avec le dénominateur uₙ + 2, puis on soustrait.",
        S + "rappels.html?vue=denominateur", "Additionner des fractions : le même dénominateur",
        "ما نقدروش نجمعو أجزاء مختلفة: un sur deux وun sur trois. كنقسمو على six: trois sur six، وdeux sur six. un sur deux plus un sur trois، égale cinq sur six. ونفس الشي بالحروف. عندنا: deux égale deux fois، u indice n plus deux، sur u indice n plus deux. الفوق: u indice n plus six، moins deux u indice n، moins quatre، égale deux moins u indice n. إذن u indice n plus un moins deux، égale moins، u indice n moins deux، sur u indice n plus deux.",
        [("2 = 2(uₙ + 2)/(uₙ + 2)", "عندنا"), ("uₙ₊₁ − 2 = −(uₙ − 2)/(uₙ + 2)", "إذن u indice n plus un moins deux")],
        [jusqua("ما نقدروش نجمعو", "parts"), jusqua("كنقسمو على six", "sixiemes"), jusqua("égale cinq sur six", "somme"),
         jusqua("ونفس الشي بالحروف", "lettres"), montre("عندنا", "centre:0"), montre("إذن u indice n plus un moins deux", "centre:1")]),
    sim("ex_4", "Question 3-2 : l'inverse change le sens", "uₙ + 2 ≥ 3 donne 1/(uₙ + 2) ≤ 1/3.",
        S + "rappels.html?vue=ordre_inverse", "Multiplier par un négatif, passer à l'inverse",
        "un inférieur à trois. ملي كنضربو fois moins un، الترتيب كيتقلب: moins un أكبر من moins trois. وملي كناخدو المقلوب: deux أصغر من quatre، ولكن un sur deux أكبر من un sur quatre. القاعدة: المقلوب ديال أعداد positifs كيقلب الاتجاه. عندنا u indice n plus deux أكبر من trois، إذن un sur، u indice n plus deux، أصغر من un sur trois. ومع la valeur absolue، le moins كيمشي: l'écart الجديد أصغر من un sur trois ديال l'écart القديم.",
        [("uₙ + 2 ≥ 3 ⇒ 1/(uₙ + 2) ≤ 1/3", "عندنا u indice n plus deux أكبر من trois"), ("|uₙ₊₁ − 2| ≤ (1/3)|uₙ − 2|", "ومع la valeur absolue")],
        [jusqua("un inférieur à trois", "depart"), jusqua("ملي كنضربو fois moins un", "miroir"), jusqua("وملي كناخدو المقلوب", "inverse"),
         jusqua("القاعدة", "regle"), montre("عندنا u indice n plus deux أكبر من trois", "centre:0"), montre("ومع la valeur absolue", "centre:1")]),
    sim("ex_5", "Question 4 : on recolle les inégalités", "Chaque pas multiplie l'écart par au plus 1/3 : |uₙ − 2| ≤ (1/3)ⁿ.",
        S + "gendarmes.html?vue=membre", "Dans l'exemple du cours : uₙ₊₁ ≤ (2/5)uₙ, recollées jusqu'à uₙ ≤ (2/5)ⁿu₀",
        "فl'exemple ديال le cours: u un inférieur ou égal à deux sur cinq u zéro. ومن بعد u deux inférieur ou égal à deux sur cinq u un. نلصقو: u deux inférieur ou égal à deux sur cinq، au carré، u zéro. وهكذا حتى ل u indice n. والطريقة النقية هي la récurrence. عندنا: l'écart ديال u zéro égale un. وكل مرة l'écart كيتضرب فun sur trois أو أقل. إذن l'écart ديال u indice n، inférieur ou égal à un sur trois puissance n. وهاد الأخير كيمشي ل zéro: la limite égale deux.",
        [("|uₙ − 2| ≤ (1/3)ⁿ × |u₀ − 2| = (1/3)ⁿ", "إذن l'écart ديال u indice n"), ("(1/3)ⁿ → 0 ⇒ lim uₙ = 2", "la limite égale deux")],
        [jusqua("فl'exemple ديال le cours", "ligne1"), jusqua("ومن بعد u deux", "ligne2"), jusqua("نلصقو", "recolle"),
         jusqua("وهكذا حتى ل u indice n", "ligne_n"), montre("إذن l'écart ديال u indice n", "centre:0"), montre("la limite égale deux", "centre:1")]),
    sim("ex_6", "Question 5 : essayer les puissances", "Chaque puissance multiplie par 3 : 3⁶ = 729, 3⁷ = 2187.",
        S + "rappels.html?vue=puissances", "Les puissances de 2 dans le rappel du cours",
        "فالرappel: deux puissance un égale deux، deux puissance deux égale quatre، deux puissance trois égale huit. كل puissance كتضرب فdeux. وdeux puissance zéro égale un. عندنا: un sur trois puissance n، inférieur ou égal à un sur mille، يعني trois puissance n، supérieur ou égal à mille. نجربو: trois puissance six égale sept cent vingt-neuf، ما وصلناش. trois puissance sept égale deux mille cent quatre-vingt-sept، فاتت mille. إذن le plus petit entier هو sept.",
        [("(1/3)ⁿ ≤ 10⁻³ ⇔ 3ⁿ ≥ 1000", "عندنا"), ("3⁶ = 729 ; 3⁷ = 2187", "نجربو"), ("n = 7", "إذن le plus petit entier هو sept")],
        [jusqua("deux puissance un égale deux", "un"), jusqua("deux puissance deux", "deux"), jusqua("deux puissance trois", "trois"),
         jusqua("وdeux puissance zéro", "retour"), montre("عندنا", "centre:0"), montre("نجربو", "centre:1"),
         montre("إذن le plus petit entier هو sept", "centre:2")]),
])

FACILE = deck("facile", "Plus facile, pour s'entraîner", [
    vrai_faux("fa_1", "Plus facile : vrai ou faux", "u₀ = 1, u₁ = 7/3, u₂ = 25/13 ≈ 1,92.",
        "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.", [
            ("u₀ < u₁, donc la suite est croissante.", False, "Deux termes ne suffisent pas, et ici u₂ < u₁."),
            ("u₁ > u₂, donc la suite n'est pas croissante.", True, "Une suite croissante vérifie uₙ₊₁ ≥ uₙ pour tout n."),
            ("La suite n'est pas monotone.", True, "Elle monte puis descend.")]),
    qcm("fa_2", "Plus facile : la bonne écriture", "نتمرنو: شنو هي الكتابة الصحيحة؟",
        "(uₙ + 6)/(uₙ + 2) = ?", ["1 + 4/(uₙ + 2)", "1 + 6/(uₙ + 2)", "3 + 4/(uₙ + 2)"], 0, [
            ("برافو! u indice n plus six égale، u indice n plus deux، plus quatre.", "Juste : uₙ + 6 = (uₙ + 2) + 4."),
            (("ما تقلقش. u indice n plus six، ناقص u indice n plus deux، كيبقى quatre، ماشي six. عاود اختار.", "(uₙ + 6) − (uₙ + 2) = 4. Réessaie."),
             ("الجواب هو un plus quatre sur، u indice n plus deux.", "Réponse : 1 + 4/(uₙ + 2).")),
            (("قريب! نقص u indice n plus deux مرة وحدة، إذن un، ماشي trois. عاود اختار.", "uₙ + 2 tient une fois dans uₙ + 6. Réessaie."),
             ("الجواب هو un plus quatre sur، u indice n plus deux.", "Réponse : 1 + 4/(uₙ + 2)."))],
        "u indice n plus six، sur u indice n plus deux، égale quoi ?"),
    qcm("fa_3", "Plus facile : le signe moins", "سؤال ساهل على le moins قدام la parenthèse.",
        "uₙ + 6 − 2(uₙ + 2) = ?", ["−uₙ + 10", "2 − uₙ", "3uₙ + 10"], 1, [
            (("ما تقلقش. le moins كيدخل على كلشي: moins deux u indice n moins quatre، ماشي plus quatre. عاود اختار.", "−2(uₙ + 2) = −2uₙ − 4. Réessaie."),
             ("الجواب هو deux moins u indice n.", "Réponse : uₙ + 6 − 2uₙ − 4 = 2 − uₙ.")),
            ("برافو! u indice n plus six moins deux u indice n moins quatre، égale deux moins u indice n.", "Juste : 2 − uₙ."),
            (("قريب! كاين moins قدام la parenthèse. عاود اختار.", "Il y a un « − » devant la parenthèse. Réessaie."),
             ("الجواب هو deux moins u indice n.", "Réponse : 2 − uₙ."))],
        "u indice n plus six moins deux fois، u indice n plus deux، égale quoi ?"),
    association("fa_4", "Plus facile : enchaîner les inégalités", "Relie chaque inégalité à celle qu'on en déduit.",
        "سؤال ساهل: ربط كل inégalité مع اللي كنستنتجو منها.", "Relie chaque inégalité à sa conséquence.",
        [("1", "uₙ ≥ 1"), ("2", "uₙ + 2 ≥ 3"), ("3", "1/(uₙ + 2) ≤ 1/3")],
        [("a", "uₙ + 2 ≥ 3"), ("b", "1/(uₙ + 2) ≤ 1/3"), ("c", "|uₙ − 2|/(uₙ + 2) ≤ (1/3)|uₙ − 2|"), ("d", "1/(uₙ + 2) ≥ 1/3")],
        {"1": "a", "2": "b", "3": "c"},
        {"1-a": ("Oui : on ajoute 2 des deux côtés.", "برافو: كنزيدو deux للجهتين."),
         "1-b": ("Une étape à la fois : d'abord ajouter 2.", "لا، خطوة بخطوة: الأول زيد deux."),
         "1-c": ("Trop loin : d'abord ajouter 2.", "لا، بعيد بزاف: الأول زيد deux."),
         "1-d": ("Non : d'abord ajouter 2, et l'inverse change le sens.", "لا، الأول زيد deux، والمقلوب كيبدل الاتجاه."),
         "2-a": ("C'est la même inégalité, on n'avance pas.", "لا، هادي نفس l'inégalité."),
         "2-b": ("Oui : l'inverse de nombres positifs change le sens.", "برافو: المقلوب ديال positifs كيبدل الاتجاه."),
         "2-c": ("Une étape à la fois : passe d'abord à l'inverse.", "لا، الأول خود المقلوب."),
         "2-d": ("Non : passer à l'inverse change le sens.", "لا، المقلوب كيبدل الاتجاه."),
         "3-a": ("C'est l'étape d'avant.", "لا، هادي الخطوة اللي قبل."),
         "3-b": ("C'est la même inégalité.", "لا، هادي نفس l'inégalité."),
         "3-c": ("Oui : on multiplie par |uₙ − 2| ≥ 0.", "برافو: كنضربو فla valeur absolue، وهي positive."),
         "3-d": ("Non : c'est le sens contraire.", "لا، هادا الاتجاه المعاكس.")},
        ("(1 ; a) (2 ; b) (3 ; c) : d est faux, l'inverse change le sens.", "القاعدة: زيد deux، خود المقلوب وبدل الاتجاه، ومن بعد ضرب فla valeur absolue.")),
    qcm("fa_5", "Plus facile : l'hérédité", "سؤال ساهل على l'hérédité.",
        "|uₙ − 2| ≤ (1/3)ⁿ et |uₙ₊₁ − 2| ≤ (1/3)|uₙ − 2|. Alors |uₙ₊₁ − 2| ≤ …", ["(1/3)ⁿ", "(1/3)ⁿ⁺¹", "(2/3)ⁿ"], 1, [
            (("ما تقلقش. كاين fois un sur trois زايدة. عاود اختار.", "Il y a un facteur 1/3 de plus. Réessaie."),
             ("الجواب هو un sur trois puissance n plus un.", "Réponse : (1/3) × (1/3)ⁿ = (1/3)ⁿ⁺¹.")),
            ("برافو! un sur trois fois un sur trois puissance n، égale un sur trois puissance n plus un.", "Juste : (1/3)ⁿ⁺¹."),
            (("قريب! كنضربو، ما كنجمعوش. عاود اختار.", "On multiplie, on n'additionne pas. Réessaie."),
             ("الجواب هو un sur trois puissance n plus un.", "Réponse : (1/3)ⁿ⁺¹."))],
        "Alors la valeur absolue de u indice n plus un moins deux est inférieure à quoi ?"),
    qcm("fa_6", "Plus facile : le seuil", "سؤال ساهل: أصغر n.",
        "Plus petit n tel que 3ⁿ ≥ 1000 ?", ["n = 6", "n = 7", "n = 1000"], 1, [
            (("ما تقلقش. trois puissance six égale sept cent vingt-neuf، ما وصلش mille. عاود اختار.", "3⁶ = 729 < 1000. Réessaie."),
             ("الجواب هو sept: trois puissance sept égale deux mille cent quatre-vingt-sept.", "Réponse : n = 7.")),
            ("برافو! trois puissance sept égale deux mille cent quatre-vingt-sept، أكبر من mille.", "Juste : 3⁷ = 2187 ≥ 1000."),
            (("قريب! n هو la puissance، ماشي mille. عاود اختار.", "n est l'exposant. Réessaie."),
             ("الجواب هو sept.", "Réponse : n = 7."))],
        "Plus petit n tel que trois puissance n supérieur ou égal à mille ?"),
])

F = lambda v: (v + 6) / (v + 2)
G = lambda v: (v + 8) / (v + 3)

ENONCE = {
    "intro": "On considère la suite numérique (uₙ) définie par : u₀ = 1 et uₙ₊₁ = (uₙ + 6)/(uₙ + 2) pour tout entier naturel n.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا la suite u indice n: u zéro égale un، وu indice n plus un égale، u indice n plus six، sur u indice n plus deux، pour tout n.",
    "figures": [nuage(F, 1)],
    "donnees": ["u₀ = 1", "uₙ₊₁ = (uₙ + 6)/(uₙ + 2) pour tout n ∈ ℕ"],
    "questions": QUESTIONS,
}

SIMILAIRE = {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
        "intro": "On considère la suite (uₙ) définie par : u₀ = 1 et uₙ₊₁ = (uₙ + 8)/(uₙ + 3) pour tout entier naturel n.",
        "intro_dit": "نفس التمرين، بأرقام أخرى: u zéro égale un، وu indice n plus un égale، u indice n plus huit، sur u indice n plus trois.",
        "figures": [nuage(G, 1)],
        "donnees": ["u₀ = 1", "uₙ₊₁ = (uₙ + 8)/(uₙ + 3)"],
        "questions": [
            {"id": "1", "texte": "Calculer u₁ et u₂. La suite (uₙ) est-elle monotone ? Justifier.",
             "reponse": phrase("u₁ = 9/4 et u₂ = (9/4 + 8)/(9/4 + 3) = 41/21 ; u₀ < u₁ et u₁ > u₂ : la suite n'est pas monotone."),
             "clavier": {"aides": ["u₁ = 9/4", "u₂ = 41/21"], "pieges": ["croissante"]},
             "correction": correction([("1 : u₁ = 9/4 ; u₂ = (41/4)/(21/4) = 41/21", "u un égale neuf sur quatre"), ("u₀ < u₁ et u₁ > u₂ : pas monotone", "pas monotone")],
                                      "u un égale neuf sur quatre، وu deux égale quarante et un sur vingt et un. طلعات ومن بعد هبطات: la suite pas monotone.")},
            {"id": "2", "texte": "Vérifier que uₙ₊₁ = 1 + 5/(uₙ + 3), puis montrer par récurrence que uₙ ≥ 1 pour tout n.",
             "reponse": phrase("1 + 5/(uₙ + 3) = (uₙ + 8)/(uₙ + 3) ; u₀ = 1 ≥ 1 ; si uₙ ≥ 1, uₙ + 3 > 0 donc uₙ₊₁ > 1. Donc uₙ ≥ 1 pour tout n."),
             "clavier": {"aides": ["(uₙ + 3 + 5)/(uₙ + 3)", "5/(uₙ + 3) > 0"], "pieges": ["opérations sur la fraction"]},
             "correction": correction([("2 : 1 + 5/(uₙ + 3) = (uₙ + 8)/(uₙ + 3)", "même dénominateur"),
                                       ("u₀ = 1 ≥ 1 ; uₙ ≥ 1 ⇒ 5/(uₙ + 3) > 0 ⇒ uₙ₊₁ > 1", "supposons que"),
                                       ("d'après le principe de récurrence, uₙ ≥ 1 pour tout n", "d'après le principe de récurrence")],
                                      "même dénominateur كيعطي u indice n plus huit، sur u indice n plus trois. u zéro égale un. supposons que u indice n أكبر من un: cinq sur، u indice n plus trois، positif، إذن u indice n plus un أكبر من un. d'après le principe de récurrence، pour tout n.")},
            {"id": "3-1", "texte": "Vérifier que uₙ₊₁ − 2 = −(uₙ − 2)/(uₙ + 3).",
             "reponse": phrase("uₙ₊₁ − 2 = (uₙ + 8 − 2uₙ − 6)/(uₙ + 3) = (2 − uₙ)/(uₙ + 3) = −(uₙ − 2)/(uₙ + 3)."),
             "clavier": {"aides": ["2(uₙ + 3)", "2 − uₙ"], "pieges": ["uₙ + 8 − 2uₙ + 6"]},
             "correction": correction([("3-1 : uₙ₊₁ − 2 = (uₙ + 8 − 2uₙ − 6)/(uₙ + 3) = −(uₙ − 2)/(uₙ + 3)", "même dénominateur")],
                                      "même dénominateur: u indice n plus huit moins deux u indice n moins six، كتعطي deux moins u indice n. إذن moins، u indice n moins deux، sur u indice n plus trois.")},
            {"id": "3-2", "texte": "Montrer que |uₙ₊₁ − 2| ≤ (1/4)|uₙ − 2| pour tout n.",
             "reponse": phrase("|uₙ₊₁ − 2| = |uₙ − 2|/(uₙ + 3) et uₙ + 3 ≥ 4, donc 1/(uₙ + 3) ≤ 1/4 : |uₙ₊₁ − 2| ≤ (1/4)|uₙ − 2|."),
             "clavier": {"aides": ["uₙ + 3 ≥ 4", "1/(uₙ + 3) ≤ 1/4"], "pieges": ["1/(uₙ + 3) ≥ 1/4"]},
             "correction": correction([("3-2 : uₙ ≥ 1 donc uₙ + 3 ≥ 4 et 1/(uₙ + 3) ≤ 1/4", "un sur quatre"),
                                       ("|uₙ₊₁ − 2| = |uₙ − 2|/(uₙ + 3) ≤ (1/4)|uₙ − 2|", "la valeur absolue")],
                                      "u indice n plus trois أكبر من quatre، إذن المقلوب أصغر من un sur quatre. la valeur absolue ديال u indice n plus un moins deux، inférieur ou égal à un sur quatre fois la valeur absolue ديال u indice n moins deux.")},
            {"id": "4", "texte": "En déduire par récurrence que |uₙ − 2| ≤ (1/4)ⁿ pour tout n, puis déterminer la limite de (uₙ).",
             "reponse": valeur("lim uₙ", 2, "|u₀ − 2| = 1 = (1/4)⁰ ; |uₙ₊₁ − 2| ≤ (1/4)|uₙ − 2| ≤ (1/4)ⁿ⁺¹ ; −1 < 1/4 < 1 donc lim (1/4)ⁿ = 0 ; lim uₙ = 2"),
             "clavier": {"aides": ["(1/4)⁰ = 1", "(1/4)ⁿ⁺¹", "lim (1/4)ⁿ = 0"], "pieges": ["lim uₙ = 0"]},
             "correction": correction([("4 : |u₀ − 2| = 1 = (1/4)⁰ ; hérédité : |uₙ₊₁ − 2| ≤ (1/4)(1/4)ⁿ = (1/4)ⁿ⁺¹", "un sur quatre puissance"),
                                       ("−1 < 1/4 < 1 : lim (1/4)ⁿ = 0, donc par comparaison lim uₙ = 2", "la limite égale deux")],
                                      "l'écart ديال u zéro égale un، égale un sur quatre puissance zéro. وكل مرة كيتضرب فun sur quatre: un sur quatre puissance n. وهاد الأخير كيمشي ل zéro، par comparaison la limite égale deux.")},
            {"id": "5", "texte": "Déterminer le plus petit entier n tel que (1/4)ⁿ ≤ 10⁻³. En déduire un rang à partir duquel |uₙ − 2| ≤ 10⁻³.",
             "reponse": valeur("n", 5, "(1/4)ⁿ ≤ 10⁻³ ⇔ 4ⁿ ≥ 1000 ; 4⁴ = 256 < 1000 et 4⁵ = 1024 ≥ 1000 ; plus petit entier : n = 5"),
             "clavier": {"aides": ["4ⁿ ≥ 1000", "4⁵ = 1024"], "pieges": ["n = 4"]},
             "correction": correction([("5 : 4ⁿ ≥ 1000 ; 4⁴ = 256, 4⁵ = 1024 : n = 5", "mille vingt-quatre"),
                                       ("pour n ≥ 5 : |uₙ − 2| ≤ (1/4)ⁿ ≤ 10⁻³", "à partir de n égale cinq")],
                                      "quatre puissance n supérieur ou égal à mille. quatre puissance quatre égale deux cent cinquante-six، وquatre puissance cinq égale mille vingt-quatre. إذن n égale cinq، وà partir de n égale cinq، l'écart inférieur ou égal à dix puissance moins trois.")},
        ]}}

EX = {"id": ID, "type": "exercice", "version": 1, "status": "published", "matiere": "mathematiques",
      "chapitre": "suites_definition", "cours": "math_ch3_suites_numeriques",
      "titre": "Une suite qui n'est pas monotone : majorer l'écart à la limite", "niveau": "difficile", "duree_min": 40,
      "origine": ORIGINE,
      "competences": ["Reconnaître qu'une suite n'est pas monotone", "Rédiger une récurrence avec une écriture donnée",
                      "Majorer |uₙ₊₁ − ℓ| par k|uₙ − ℓ|, puis |uₙ − ℓ| par kⁿ", "Conclure par comparaison et trouver un seuil"],
      "enonce": ENONCE, "explication": EXPLICATION, "facile": FACILE, "similaire": SIMILAIRE}

if __name__ == "__main__":
    ecrire(EX)
