# Exercice de chimie (physique-chimie), ch. 9 « Transformations lentes et transformations rapides », niveau difficile n° 7 :
# la croix qui disparaît — thiosulfate en milieu acide : deux couples de l'ion thiosulfate, concentration après mélange,
# choix des expériences (dont une comparaison piège), réactif limitant, interprétation par les rencontres des entités.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture phys_ch9_transformations_lentes_rapides.md (tl_r4_indices,
#    tl_f6_rencontres : « chocs efficaces » réservé au ch. 10, on dit « les entités se rencontrent plus souvent »),
#    sources_chimie_ch9_ch11.md (thiosulfate + acide chez 4 profs sur 5 ; Mahajar : la concentration avec thiosulfate + HCl) ;
#  - le cours phys_ch9 (tl_r4_indices : couples S₂O₃²⁻/S et SO₂/S₂O₃²⁻ ; tl_rp4 dilution ; tl_f5, tl_f6, tl_f8 ; tl_rp5) ;
#  - nationaux : 2024 N (vrai/faux concentration facteur cinétique), 2025 N (tableau de trois expériences), 2018 N ;
#    ici deux notions combinées, un document moins guidé (tableau de volumes) et une comparaison piège ;
#  - séries en ligne : recherche faite (talamidi, moutamadris, dreamjob, alloschool) ; PDF non ouverts (hôtes hors du réseau
#    autorisé de la session).
#  Durées Δt cohérentes avec les modèles des simulations : Δt ∝ 1/[S₂O₃²⁻]₀ et ÷ 3 pour + 20 °C (facteurs.html).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch9_lentes_rapides_7"
SIM = "/media/simulations/chimie/transformations-lentes-rapides-tableau/"
EQ = "S₂O₃²⁻(aq) + 2H⁺(aq) → S(s) + SO₂(aq) + H₂O(l)"
D1 = "S₂O₃²⁻(aq) + 6H⁺(aq) + 4e⁻ ⇌ 2S(s) + 3H₂O(l)"
D2 = "2SO₂(aq) + 2H⁺(aq) + 4e⁻ ⇌ S₂O₃²⁻(aq) + H₂O(l)"
# vérification des demi-équations (éléments S, O, H et charges) et de l'équation
assert (2, 3, 6, -2 + 6 - 4) == (2, 3, 2 * 3, 0)
assert (2, 4, 2, 2 - 4) == (2, 3 + 1, 2, -2)


def r(v):
    return round(v, 9)


def donnees(C, Ca, Va, lignes, V=50):
    """lignes : [(V_S mL, θ, Δt s)] ; renvoie concentrations après mélange, n₀ (mmol) et x_max de l'expérience 1."""
    cs = [r(C * vs / V) for vs, _, _ in lignes]
    nS = r(C * lignes[0][0])            # mmol (mol/L × mL)
    nH = r(Ca * Va)
    xm = min(nS, nH / 2)
    return cs, nS, nH, xm


L = [(40, 20, 50), (20, 20, 100), (20, 40, 35), (10, 40, 70)]
cs, nS, nH, xm = donnees(0.10, 2.0, 5.0, L)
assert cs == [0.08, 0.04, 0.04, 0.02] and (nS, nH, xm) == (4.0, 10.0, 4.0)
# cohérence des durées : Δt ∝ 1/c et ÷ 3 pour +20 °C (arrondies)
assert abs(L[1][2] / L[0][2] - cs[0] / cs[1]) < 1e-9 and abs(L[1][2] / 3 - L[2][2]) < 2 and abs(L[3][2] / L[2][2] - 2) < 1e-9
Lb = [(25, 20, 40), (10, 20, 100), (10, 40, 35), (5, 40, 70)]
csb, nSb, nHb, xmb = donnees(0.20, 3.0, 5.0, Lb)
assert csb == [0.1, 0.04, 0.04, 0.02] and (nSb, nHb, xmb) == (5.0, 15.0, 5.0)
assert abs(Lb[1][2] / Lb[0][2] - csb[0] / csb[1]) < 1e-9


def tableau(titre, lignes, legende):
    cols = [(1.2, "Exp."), (3.4, "V_S (mL)"), (6.0, "V_eau (mL)"), (8.5, "θ (°C)"), (10.9, "Δt (s)")]
    n = len(lignes)
    h = 1.0 * (n + 1)
    g = [{"f": "rect", "de": [0.2, 0.2], "a": [12.0, 0.2 + h]}]
    for x in (2.2, 4.7, 7.3, 9.7):
        g += fil([x, 0.2], [x, 0.2 + h])
    for k in range(1, n + 1):
        g += fil([0.2, 0.2 + k], [12.0, 0.2 + k])
    for x, t in cols:
        g += texte([x, 0.2 + h - 0.6], t, couleur="jaune")
    for i, (vs, th, dt) in enumerate(lignes):
        y = 0.2 + h - 1.6 - i
        for (x, _), v in zip(cols, [str(i + 1), str(vs), str(45 - vs), str(th), str(dt)]):
            g += texte([x, y], v)
    return schema(titre, 12.2, h + 0.4, g, legende=legende)


EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "transformations_lentes_rapides", "cours": "phys_ch9_transformations_lentes_rapides",
  "titre": "La croix qui disparaît : thiosulfate, concentration et température", "niveau": "difficile", "duree_min": 40,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Écrire les demi-équations des deux couples de l'ion thiosulfate et établir l'équation",
                  "Calculer une concentration initiale dans un mélange", "Exploiter un tableau d'expériences : un seul paramètre à la fois",
                  "Déterminer le réactif limitant et la quantité de soufre formé", "Interpréter l'effet de la concentration par les rencontres des entités"],
  "enonce": {
    "intro": "Dans un bécher posé sur une croix noire, on verse un volume V_S d'une solution de thiosulfate de sodium de concentration C = 0,10 mol/L en ions S₂O₃²⁻(aq), puis un volume V_eau d'eau distillée. À t = 0, on ajoute V_a = 5,0 mL d'acide chlorhydrique de concentration C_a = 2,0 mol/L en ions H⁺(aq) ; le volume total est toujours V = 50 mL. Du soufre S(s) se forme peu à peu et trouble la solution ; on note la durée Δt au bout de laquelle la croix n'est plus visible. Les quatre expériences sont résumées dans le tableau (figure 1).",
    "intro_dit": "نقراو l'énoncé. ف le bécher فوق une croix كحلة، كنصبو V S ديال le thiosulfate de sodium، C égale zéro virgule un mole par litre، ومن بعد V eau ديال الما. فt égale zéro، كنزيدو V a égale cinq millilitres ديال l'acide chlorhydrique، C a égale deux moles par litre. le volume total ديما V égale cinquante millilitres. le soufre كيتكون بشوية بشوية، وكنقيسو la durée delta t حتى la croix ما بقاتش باينة. les quatre expériences ف le tableau، la figure un.",
    "figures": [tableau("Figure 1 : les quatre expériences", L, "V_a = 5,0 mL d'acide dans chaque expérience ; V = V_S + V_eau + V_a = 50 mL.")],
    "donnees": ["C = 0,10 mol/L (S₂O₃²⁻) ; C_a = 2,0 mol/L (H⁺) ; V_a = 5,0 mL ; V = 50 mL",
                "Couples : S₂O₃²⁻(aq)/S(s) et SO₂(aq)/S₂O₃²⁻(aq)"],
    "questions": [
      question("1", "L'ion thiosulfate appartient aux deux couples donnés. Écrire leurs demi-équations électroniques, puis établir l'équation de la réaction : " + EQ + ".",
        "السؤال un: l'ion thiosulfate كاين ف les deux couples. كتب les demi-équations ديالهم، ومن بعد استنتج l'équation ديال la réaction.",
        phrase(D1 + " ; " + D2 + ". L'ion S₂O₃²⁻ est réduit en S (première, sens direct) et oxydé en SO₂ (seconde, sens inverse : S₂O₃²⁻(aq) + H₂O(l) → 2SO₂(aq) + 2H⁺(aq) + 4e⁻). 4 électrons de chaque côté : on additionne, 2S₂O₃²⁻(aq) + 4H⁺(aq) → 2S(s) + 2SO₂(aq) + 2H₂O(l), puis on divise par 2 : " + EQ + "."),
        ["4e⁻", "6H⁺(aq)", "3H₂O(l)", "sens inverse", "diviser par 2"], ["S₂O₃²⁻(aq) + 2e⁻ ⇌ S(s)", "les électrons restent dans l'équation"],
        [aide("Couple S₂O₃²⁻/S : 2 atomes S à gauche, donc 2S ; puis O avec H₂O, H avec H⁺, charges avec e⁻. Couple SO₂/S₂O₃²⁻ : 2SO₂ pour 2 atomes S.",
              "le couple ion thiosulfate sur soufre: deux soufre على اليسار، donc deux soufre على اليمين. ومن بعد les oxygènes ب l'eau، les hydrogènes ب H plus، و les charges ب les électrons. le couple dioxyde de soufre sur ion thiosulfate: deux dioxyde de soufre."),
         aide("Les deux demi-équations ont 4e⁻. L'ion thiosulfate est l'oxydant de la première et le réducteur de la seconde : écris la seconde dans le sens inverse, additionne, puis simplifie (H⁺, H₂O) et divise par 2.",
              "les deux demi-équations ont quatre électrons. l'ion thiosulfate هو l'oxydant ف la première، و le réducteur ف la deuxième: كتب la deuxième فالاتجاه الآخر، جمع، بسط، ومن بعد قسم sur deux.")],
        corr([("1 : " + D1, "ion thiosulfate plus six H plus plus quatre électrons"),
              (D2, "deux dioxyde de soufre plus deux H plus plus quatre électrons"),
              ("Somme (4e⁻ de chaque côté), simplification, ÷ 2 : " + EQ, "قسم sur deux")],
             "السؤال un. le premier couple: ion thiosulfate plus six H plus plus quatre électrons، donne deux soufre plus trois molécules d'eau. le deuxième couple: deux dioxyde de soufre plus deux H plus plus quatre électrons، donne ion thiosulfate plus eau. l'ion thiosulfate كيتنقص ف la première، وكيتأكسد ف la deuxième، اللي كنكتبوها فالاتجاه الآخر. quatre électrons من كل جهة: كنجمعو، كنبسطو les H plus و l'eau، ومن بعد قسم sur deux: ion thiosulfate plus deux H plus، donne soufre plus dioxyde de soufre plus eau."),
        "ex_tl7_1", "fa_tl7_1"),
      question("2", "Calculer la concentration initiale [S₂O₃²⁻]₀ des ions thiosulfate dans le mélange de l'expérience 1 (en mol/L).",
        "السؤال deux: حسب la concentration initiale ديال les ions thiosulfate ف le mélange ديال l'expérience un.",
        valeur("[S₂O₃²⁻]₀", 0.080, "mol/L", "[S₂O₃²⁻]₀ = C·V_S / V = 0,10 × 40 / 50 = 0,080 mol/L"),
        ["n = C·V_S", "[ ]₀ = n / V", "V = 50 mL", "mol/L"], ["[S₂O₃²⁻]₀ = C = 0,10 mol/L", "[S₂O₃²⁻]₀ = 0,10 × 50 / 40"],
        [aide("Les ions thiosulfate viennent seulement du volume V_S de solution, mais une fois mélangés ils occupent tout le volume V = 50 mL.",
              "les ions thiosulfate جاو غير من V S، ولكن من بعد الخلط كيكونو ف le volume كامل، V égale cinquante millilitres."),
         aide("n = C·V_S, puis [S₂O₃²⁻]₀ = n / V = C·V_S / V (les mL se simplifient).",
              "n égale C fois V S، ومن بعد la concentration égale n sur V، يعني C fois V S sur V.")],
        corr([("2 : n₀(S₂O₃²⁻) = C·V_S ; [S₂O₃²⁻]₀ = C·V_S / V", "C fois V S sur V"),
              ("A.N. : [S₂O₃²⁻]₀ = 0,10 × 40 / 50 = 0,080 mol/L", "zéro virgule zéro huit mole par litre")],
             "السؤال deux. n zéro égale C fois V S، ومن بعد كيتوزع ف le volume V. la concentration égale C fois V S sur V، يعني zéro virgule un fois quarante sur cinquante، égale zéro virgule zéro huit mole par litre."),
        "ex_tl7_2", "fa_tl7_2"),
      question("3", "Quelles expériences permettent d'étudier l'influence de la concentration initiale des ions thiosulfate ? Conclure.",
        "السؤال trois: شمن expériences كيسمحو نعرفو l'influence ديال la concentration initiale ديال les ions thiosulfate؟ استنتج.",
        phrase("Expériences 1 et 2 : même température (20 °C), seule [S₂O₃²⁻]₀ change (0,080 et 0,040 mol/L). La croix disparaît en 50 s pour 1 et en 100 s pour 2 : plus la concentration initiale est grande, plus la transformation est rapide. La concentration initiale des réactifs est un facteur cinétique."),
        ["1 et 2", "même θ", "Δt plus court", "facteur cinétique", "concentration"], ["1 et 4", "Δt plus long donc plus rapide"],
        [aide("Cherche deux lignes avec la même température, mais un volume V_S différent. Calcule [S₂O₃²⁻]₀ pour chacune.",
              "قلب على les deux lignes فيهم نفس la température، ولكن V S مختلف. حسب la concentration ديال كل وحدة."),
         aide("Une durée Δt plus courte signifie une transformation plus rapide. Compare Δt des deux expériences choisies.",
              "delta t أقصر يعني la transformation plus rapide. قارن delta t ديال les deux expériences.")],
        corr([("3 : expériences 1 et 2 : même θ = 20 °C, [S₂O₃²⁻]₀ = 0,080 et 0,040 mol/L", "l'expérience un et l'expérience deux"),
              ("Δt = 50 s < 100 s : plus [S₂O₃²⁻]₀ est grande, plus la transformation est rapide.", "plus la concentration est grande")],
             "السؤال trois. l'expérience un et l'expérience deux: نفس la température، غير la concentration اللي تبدلات، zéro virgule zéro huit et zéro virgule zéro quatre mole par litre. la croix كتختفي à cinquante secondes ف la première، et à cent secondes ف la deuxième. إذن plus la concentration est grande، plus la transformation est rapide: la concentration est un facteur cinétique."),
        "ex_tl7_3", "fa_tl7_3"),
      question("4", "Quelles expériences permettent d'étudier l'influence de la température ? Conclure. Un élève compare les expériences 1 et 4 et conclut que la température ralentit la transformation : critiquer.",
        "السؤال quatre: شمن expériences ل la température؟ استنتج. تلميذ قارن l'expérience un et l'expérience quatre، وقال la température كتنقص الزربة: شنو رأيك؟",
        phrase("Expériences 2 et 3 : même [S₂O₃²⁻]₀ = 0,040 mol/L, seule θ change (20 °C et 40 °C) ; Δt passe de 100 s à 35 s : plus la température est élevée, plus la transformation est rapide. Entre 1 et 4, la température ET la concentration changent (0,080 mol/L à 20 °C ; 0,020 mol/L à 40 °C) : on ne peut pas attribuer la différence à la température ; la conclusion de l'élève n'est pas valable."),
        ["2 et 3", "un seul paramètre", "deux paramètres changent", "température"], ["1 et 4 pour la température", "la température ralentit"],
        [aide("Pour la température, il faut la même concentration dans les deux expériences. Entre 1 et 4, qu'est-ce qui change ?",
              "ل la température، خاص نفس la concentration ف les deux expériences. بين l'expérience un et l'expérience quatre، شنو تبدل؟"),
         aide("Calcule [S₂O₃²⁻]₀ dans l'expérience 4 (V_S = 10 mL) : si deux paramètres changent, on ne peut pas savoir lequel agit.",
              "حسب la concentration ف l'expérience quatre، V S égale dix millilitres. يلا les deux paramètres تبدلو، ما نعرفوش شكون اللي دار الفرق.")],
        corr([("4 : expériences 2 et 3 : même [S₂O₃²⁻]₀ = 0,040 mol/L ; θ = 20 et 40 °C ; Δt = 100 s et 35 s", "l'expérience deux et l'expérience trois"),
              ("Plus la température est élevée, plus la transformation est rapide.", "plus la température est élevée"),
              ("1 et 4 : θ et [S₂O₃²⁻]₀ (0,080 et 0,020 mol/L) changent toutes les deux : conclusion non valable.", "deux paramètres تبدلو")],
             "السؤال quatre. ل la température: l'expérience deux et l'expérience trois، نفس la concentration، zéro virgule zéro quatre mole par litre. delta t كيهبط de cent secondes à trente-cinq secondes: plus la température est élevée، plus la transformation est rapide. بين l'expérience un et l'expérience quatre، deux paramètres تبدلو: la température، و la concentration اللي هبطات de zéro virgule zéro huit à zéro virgule zéro deux. ما نقدروش نقولو شكون السبب: la conclusion ديال التلميذ غالطة."),
        "ex_tl7_4", "fa_tl7_4"),
      question("5", "Pour l'expérience 1, montrer que les ions H⁺ sont en excès et déterminer, en mmol, la quantité de soufre formé à l'état final.",
        "السؤال cinq: ف l'expérience un، بين بلي les ions H plus en excès، وحسب ب millimole la quantité ديال le soufre فالحالة النهائية.",
        valeur("n(S)f", 4.0, "mmol", "n₀(S₂O₃²⁻) = 0,10 × 40·10⁻³ = 4,0 mmol ; n₀(H⁺) = 2,0 × 5,0·10⁻³ = 10 mmol ; 4,0 − x_max = 0 ⇒ 4,0 mmol ; 10 − 2x_max = 0 ⇒ 5,0 mmol ; S₂O₃²⁻ limitant, H⁺ en excès : n(S)f = x_max = 4,0 mmol"),
        ["n = C·V", "n₀ − x", "n₀ − 2x", "x_max", "n(S) = x"], ["H⁺ limitant", "n(S)f = 2x_max", "n(S)f = 5,0 mmol"],
        [aide("Calcule n₀(S₂O₃²⁻) = C·V_S et n₀(H⁺) = C_a·V_a. Ligne « en cours » : 4,0 − x et n₀(H⁺) − 2x.",
              "حسب n zéro ديال les ions thiosulfate، C fois V S، و n zéro ديال H plus، C a fois V a. السطر ديال en cours: quatre moins x، et n zéro ديال H plus moins deux x."),
         aide("La plus petite valeur de x est x_max ; l'autre réactif est en excès. Le coefficient de S est 1 : n(S) = x.",
              "القيمة الصغيرة هي x max، و le réactif الآخر en excès. le coefficient ديال le soufre égale un: n de S égale x.")],
        corr([("5 : n₀(S₂O₃²⁻) = C·V_S = 4,0 mmol ; n₀(H⁺) = C_a·V_a = 10 mmol", "quatre millimoles et dix millimoles"),
              ("4,0 − x_max = 0 ⇒ 4,0 mmol ; 10 − 2x_max = 0 ⇒ 5,0 mmol : x_max = 4,0 mmol, S₂O₃²⁻ limitant, H⁺ en excès", "les ions H plus en excès"),
              ("n(S)f = x_max = 4,0 mmol", "n de S finale égale quatre millimoles")],
             "السؤال cinq. n zéro ديال les ions thiosulfate égale zéro virgule un fois quarante millilitres، يعني quatre millimoles. n zéro ديال H plus égale deux fois cinq millilitres، يعني dix millimoles. ف le tableau: quatre millimoles et dix millimoles. quatre moins x max égale zéro، donne quatre millimoles. dix moins deux x max égale zéro، donne cinq millimoles. الصغيرة، c'est quatre: l'ion thiosulfate limitant، و les ions H plus en excès. n de S égale x، إذن n de S finale égale quatre millimoles."),
        "ex_tl7_5", "fa_tl7_5"),
      question("6", "Interpréter, à l'échelle des entités, pourquoi l'expérience 1 est plus rapide que l'expérience 2.",
        "السؤال six: فسر على مستوى les entités، علاش l'expérience un plus rapide من l'expérience deux.",
        phrase("Dans l'expérience 1, il y a deux fois plus d'ions thiosulfate dans le même volume (0,080 contre 0,040 mol/L). Les entités réactives (S₂O₃²⁻ et H⁺) se rencontrent plus souvent : plus la concentration est grande, plus les entités se rencontrent souvent, et plus la transformation est rapide. L'état final est atteint plus tôt."),
        ["entités", "se rencontrent plus souvent", "même volume", "concentration"], ["les ions vont plus vite", "il y a plus d'énergie"],
        [aide("Pour réagir, les entités doivent se rencontrer. Dans le même volume, y a-t-il plus ou moins d'ions thiosulfate dans l'expérience 1 ?",
              "باش يتفاعلو، les entités خاصهم يتلاقاو. ف نفس le volume، واش كاينين كتر ولا قل ديال les ions thiosulfate ف l'expérience un؟"),
         aide("Plus d'entités dans le même volume : plus de rencontres, donc une transformation plus rapide (même température : l'agitation est la même).",
              "كتر ديال les entités ف نفس le volume: كيتلاقاو كتر، إذن la transformation plus rapide. و la température هي هي.")],
        corr([("6 : expérience 1 : [S₂O₃²⁻]₀ deux fois plus grande dans le même volume", "deux fois plus d'ions thiosulfate"),
              ("Les entités se rencontrent plus souvent : la transformation est plus rapide.", "plus la concentration est grande، plus les entités se rencontrent souvent")],
             "السؤال six. ف l'expérience un، deux fois plus d'ions thiosulfate ف نفس le volume. باش يتفاعلو، les entités خاصهم يتلاقاو. نعاود نقرا: plus la concentration est grande، plus les entités se rencontrent souvent، et plus la transformation est rapide."),
        "ex_tl7_6", "fa_tl7_6"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_tl7_1", "Question 1 : l'ion thiosulfate, oxydant et réducteur", "Deux couples, quatre électrons : on additionne, on simplifie, on divise par 2.",
      SIM + "bechers.html?vue=soufre", "Le bécher sur la croix noire : thiosulfate + acide",
      "شوف هاد le bécher: تحتو une croix كحلة. نخلطو les ions thiosulfate مع l'acide. كيبان un trouble: هادا le soufre اللي كيتكون. وفالأخير، la croix ما بقاتش باينة. المعادلة: ion thiosulfate، plus deux H plus، donne soufre، plus dioxyde de soufre، plus eau. l'ion thiosulfate عندو les deux rôles: هو l'oxydant ف le couple ion thiosulfate sur soufre، و هو le réducteur ف le couple dioxyde de soufre sur ion thiosulfate. les deux demi-équations ont quatre électrons: كنجمعو، كنبسطو، ومن بعد كنقسمو sur deux.",
      centre=[(D1, "هو l'oxydant"), (D2, "و هو le réducteur"), (EQ, "كنقسمو sur deux")],
      pointage=[{"mot": "شوف هاد le bécher", "repere": "becher"},
                {"mot": "تحتو une croix كحلة", "repere": "croix"},
                {"mot": "نخلطو les ions thiosulfate", "commande": "play_until", "parametres": {"moment": "melange"}},
                {"mot": "كيبان un trouble", "commande": "play_until", "parametres": {"moment": "trouble"}},
                {"mot": "كيبان un trouble", "repere": "trouble"},
                {"mot": "la croix ما بقاتش باينة", "commande": "play_until", "parametres": {"moment": "croix_cachee"}},
                {"mot": "هو l'oxydant", "cible": "centre:0"},
                {"mot": "و هو le réducteur", "cible": "centre:1"},
                {"mot": "كنقسمو sur deux", "cible": "centre:2"}]),
    diapo_sim("ex_tl7_2", "Question 2 : la concentration dans le mélange", "Même quantité dans un plus grand volume : la concentration diminue.",
      SIM + "rappels.html?vue=concentration", "C = n/V et la dilution : même quantité, plus d'eau, concentration plus petite",
      "شوف le bécher: zéro virgule zéro un mole dans cent millilitres، zéro virgule un mole par litre. la relation: C égale n sur V. ويلا حطينا نفس الكمية dans deux fois plus d'eau؟ اللون كيولي خفيف: la concentration divisée par deux، zéro virgule zéro cinq mole par litre. فالتمرين: n zéro égale C fois V S، ومن بعد كيتوزع dans cinquante millilitres. la concentration égale zéro virgule un fois quarante sur cinquante، égale zéro virgule zéro huit mole par litre.",
      centre=[("[S₂O₃²⁻]₀ = C·V_S / V = 0,10 × 40 / 50 = 0,080 mol/L", "égale zéro virgule zéro huit mole par litre")],
      pointage=[{"mot": "شوف le bécher", "commande": "play_until", "parametres": {"moment": "becher"}},
                {"mot": "la relation: C égale n sur V", "commande": "play_until", "parametres": {"moment": "formule"}},
                {"mot": "ويلا حطينا نفس الكمية", "commande": "play_until", "parametres": {"moment": "dilution"}},
                {"mot": "égale zéro virgule zéro huit mole par litre", "cible": "centre:0"}]),
    diapo_sim("ex_tl7_3", "Question 3 : la concentration, facteur cinétique", "Même température, concentration doublée : plus rapide, même état final.",
      SIM + "facteurs.html?vue=concentration", "Deux béchers à 20 °C : la concentration simple et la concentration double",
      "voici deux béchers ديال le cours، à vingt degrés Celsius. ف le premier، zéro virgule un mole par litre. ف le deuxième، zéro virgule deux mole par litre: deux fois plus. دابا نخلطو، ونطلقو le chronomètre. le bécher le plus concentré كيوصل اللول ل l'état final ديالو. التاني باقي، ومن بعد حتى هو كيوصل. نفس الشي فالتمرين: l'expérience un، zéro virgule zéro huit mole par litre، la croix كتختفي à cinquante secondes. l'expérience deux، zéro virgule zéro quatre، à cent secondes. plus la concentration est grande، plus la transformation est rapide.",
      centre=[("1 et 2 : même θ ; Δt = 50 s et 100 s", "la croix كتختفي à cinquante secondes"), ("Concentration plus grande : plus rapide", "plus la concentration est grande، plus la transformation est rapide")],
      pointage=[{"mot": "voici deux béchers", "commande": "play_until", "parametres": {"moment": "melange"}},
                {"mot": "ف le premier", "repere": "etiquette_dilue"},
                {"mot": "ف le deuxième", "repere": "etiquette_concentre"},
                {"mot": "دابا نخلطو", "commande": "play_until", "parametres": {"moment": "depart"}},
                {"mot": "le bécher le plus concentré كيوصل اللول", "commande": "play_until", "parametres": {"moment": "concentre_fini"}},
                {"mot": "حتى هو كيوصل", "commande": "play_until", "parametres": {"moment": "dilue_fini"}},
                {"mot": "la croix كتختفي à cinquante secondes", "cible": "centre:0"},
                {"mot": "plus la concentration est grande، plus la transformation est rapide", "cible": "centre:1"}]),
    diapo_sim("ex_tl7_4", "Question 4 : la comparaison piège", "Deux paramètres changent : aucune conclusion.",
      SIM + "facteurs.html?vue=une_variable", "Un tableau d'expériences : on compare deux lignes qui ne diffèrent que par un paramètre",
      "شوف هاد le tableau ديال le cours. on compare un et deux: غير la température اللي تبدلات. on compare deux et trois: غير la concentration. et un et trois؟ deux paramètres تبدلو: ما كنستنتجو والو. la règle: pour un facteur، deux expériences، qui ne diffèrent que par ce seul paramètre. فالتمرين ديالنا: la température، l'expérience deux et l'expérience trois، delta t كيهبط de cent à trente-cinq secondes. و l'expérience un et l'expérience quatre: la température تبدلات، et la concentration حتى هي. التلميذ ما عندوش الحق.",
      centre=[("Température : 2 et 3 (100 s → 35 s)", "delta t كيهبط"), ("1 et 4 : θ et [S₂O₃²⁻]₀ changent : pas de conclusion", "التلميذ ما عندوش الحق")],
      pointage=[{"mot": "شوف هاد le tableau", "commande": "play_until", "parametres": {"moment": "tableau"}},
                {"mot": "on compare un et deux", "commande": "play_until", "parametres": {"moment": "comparer_1_2"}},
                {"mot": "on compare deux et trois", "commande": "play_until", "parametres": {"moment": "comparer_2_3"}},
                {"mot": "et un et trois؟", "commande": "play_until", "parametres": {"moment": "comparer_1_3"}},
                {"mot": "la règle: pour un facteur", "commande": "play_until", "parametres": {"moment": "conclusion"}},
                {"mot": "delta t كيهبط", "cible": "centre:0"},
                {"mot": "التلميذ ما عندوش الحق", "cible": "centre:1"}]),
    diapo_sim("ex_tl7_5", "Question 5 : le réactif limitant", "Chaque réactif donne sa valeur de x ; la plus petite est x_max.",
      SIM + "national-pas-a-pas.html?sujet=iodure&etape=5", "La méthode du tableau d'avancement",
      "شوف la méthode ف le tableau ديال le cours: كل réactif، فوقاش كيسالي؟ ومن بعد القيمة الصغيرة. فالتمرين ديالنا: quatre millimoles ديال les ions thiosulfate، et dix millimoles ديال H plus. quatre moins x max égale zéro، donne quatre millimoles. dix moins deux x max égale zéro، donne cinq millimoles. x max égale quatre millimoles: l'ion thiosulfate limitant، و les ions H plus en excès. و n de S égale x: quatre millimoles ديال le soufre.",
      centre=[("x_max = 4,0 mmol ; H⁺ en excès", "x max égale quatre millimoles"), ("n(S)f = x_max = 4,0 mmol", "quatre millimoles ديال le soufre")],
      pointage=[{"mot": "شوف la méthode", "commande": "play_until", "parametres": {"moment": "rappel"}},
                {"mot": "شوف la méthode", "repere": "tableau"},
                {"mot": "فوقاش كيسالي؟", "commande": "play_until", "parametres": {"moment": "question"}},
                {"mot": "ومن بعد القيمة الصغيرة", "commande": "play_until", "parametres": {"moment": "correction"}},
                {"mot": "x max égale quatre millimoles", "cible": "centre:0"},
                {"mot": "quatre millimoles ديال le soufre", "cible": "centre:1"}]),
    diapo_sim("ex_tl7_6", "Question 6 : plus d'entités, plus de rencontres", "Même volume, plus d'entités : elles se rencontrent plus souvent.",
      SIM + "rencontres.html?vue=concentration", "Deux loupes : les entités et leurs rencontres, à deux concentrations",
      "شوف la loupe ديال le bécher le plus concentré: بزاف ديال les entités ف نفس le volume. كيتلاقاو بزاف. دابا شوف le bécher الآخر: les entités قلال، وكيتلاقاو قل. الصورة ديال le cours فيها les ions iodure، ولكن نفس الفكرة ل les ions thiosulfate: ف l'expérience un، deux fois plus d'ions thiosulfate. نعاود نقرا: plus la concentration est grande، plus les entités se rencontrent souvent، et plus la transformation est rapide.",
      centre=[("Plus d'entités dans le même volume : plus de rencontres", "plus les entités se rencontrent souvent")],
      pointage=[{"mot": "شوف la loupe", "commande": "play_until", "parametres": {"moment": "rencontres"}},
                {"mot": "شوف la loupe", "repere": "becher_concentre"},
                {"mot": "كيتلاقاو بزاف", "repere": "compteur_concentre"},
                {"mot": "دابا شوف le bécher الآخر", "repere": "becher_dilue"},
                {"mot": "وكيتلاقاو قل", "repere": "compteur_dilue"},
                {"mot": "plus les entités se rencontrent souvent", "cible": "centre:0"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    vrai_faux_facile("fa_tl7_1", "Plus facile : vrai ou faux", "قول واش هاد الجمل صحيحة ولا غالطة.",
      EQ,
      [("Dans cette réaction, l'ion thiosulfate est à la fois oxydant et réducteur.", True, "Il est réduit en S (couple S₂O₃²⁻/S) et oxydé en SO₂ (couple SO₂/S₂O₃²⁻)."),
       ("Le trouble qui cache la croix est dû au dioxyde de soufre SO₂.", False, "SO₂(aq) reste dissous ; le trouble est dû au soufre solide S(s)."),
       ("L'équation conserve les charges : −2 + 2 = 0 à gauche et 0 à droite.", True, "À droite S, SO₂ et H₂O sont neutres.")]),
    qcm_facile("fa_tl7_2", "Plus facile : la concentration après mélange", "سؤال ساهل على la concentration.",
      "40 mL de solution à 0,10 mol/L sont mélangés pour faire 50 mL en tout. [S₂O₃²⁻]₀ vaut…",
      ["0,10 mol/L", "0,080 mol/L", "0,125 mol/L"], 1, {
        "1": {"juste": rep("برافو! zéro virgule un fois quarante sur cinquante، égale zéro virgule zéro huit.", "Juste : 0,10 × 40 / 50 = 0,080 mol/L.")},
        "0": {"1": rep("ما تقلقش. ملي زدنا الما و l'acide، le volume كبر: واش la concentration بقات هي هي؟ عاود اختار.", "Le volume a augmenté : la concentration reste-t-elle la même ? Réessaie."),
              "2": rep("الجواب: zéro virgule zéro huit. نفس الكمية ف volume أكبر: la concentration كتنقص.", "Réponse : 0,080 mol/L ; même quantité dans un plus grand volume.")},
        "2": {"1": rep("قلبتي la fraction: cinquante sur quarante. ولكن la concentration خاصها تنقص. عاود اختار.", "Tu as fait 50/40 : or la concentration doit diminuer. Réessaie."),
              "2": rep("الجواب: C fois V S sur V، يعني quarante sur cinquante: zéro virgule zéro huit.", "Réponse : C·V_S/V = 0,10 × 40/50 = 0,080 mol/L.")}},
      "quarante millilitres à zéro virgule un mole par litre، dans cinquante millilitres en tout. La concentration vaut ?"),
    qcm_facile("fa_tl7_3", "Plus facile : la concentration", "سؤال ساهل على delta t.",
      "Exp. 1 : 0,080 mol/L, Δt = 50 s ; exp. 2 : 0,040 mol/L, Δt = 100 s (même θ). On conclut que…",
      ["plus la concentration est grande, plus la transformation est rapide", "plus la concentration est grande, plus la transformation est lente", "la concentration n'a pas d'effet"], 0, {
        "0": {"juste": rep("برافو! delta t أقصر ف l'expérience un: plus rapide.", "Juste : Δt plus court pour la plus concentrée.")},
        "1": {"1": rep("رد البال: delta t كبير يعني lente. شكون عندو delta t الصغير؟ عاود اختار.", "Un grand Δt signifie lent. Qui a le plus petit Δt ? Réessaie."),
              "2": rep("الجواب: l'expérience un، الأكثر concentrée، عندها delta t الصغير: هي la plus rapide.", "Réponse : la plus concentrée a le Δt le plus court : plus rapide.")},
        "2": {"1": rep("شوف: cinquante secondes et cent secondes، واش نفس delta t؟ عاود اختار.", "50 s et 100 s : est-ce la même durée ? Réessaie."),
              "2": rep("الجواب: كاين effet: la concentration est un facteur cinétique.", "Réponse : la concentration est un facteur cinétique.")}},
      "Plus concentrée، cinquante secondes، moins concentrée، cent secondes. On conclut ?"),
    association_facile("fa_tl7_4", "Plus facile : quelle comparaison ?", "ربط كل comparaison مع شنو كتسمح نعرفو.",
      "Exp. 1 (0,080 mol/L ; 20 °C), 2 (0,040 ; 20 °C), 3 (0,040 ; 40 °C), 4 (0,020 ; 40 °C).",
      "Relie chaque comparaison à ce qu'elle permet d'étudier.",
      [("1", "Comparer 1 et 2"), ("2", "Comparer 2 et 3"), ("3", "Comparer 1 et 4")],
      [("a", "l'influence de la concentration"), ("b", "l'influence de la température"), ("c", "rien : deux paramètres changent")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Juste : même θ, seule la concentration change.", "صحيح: نفس la température، غير la concentration اللي تبدلات."),
       "1-b": (False, "Entre 1 et 2, θ vaut 20 °C deux fois.", "entre un et deux، la température هي هي، vingt degrés."),
       "1-c": (False, "Entre 1 et 2, un seul paramètre change.", "لا، entre un et deux، seulement un paramètre تبدل."),
       "2-a": (False, "Entre 2 et 3, la concentration est la même (0,040 mol/L).", "entre deux et trois، la concentration هي هي."),
       "2-b": (True, "Juste : même concentration, seule θ change.", "صحيح: نفس la concentration، غير la température اللي تبدلات."),
       "2-c": (False, "Entre 2 et 3, un seul paramètre change.", "لا، entre deux et trois، seulement un paramètre تبدل."),
       "3-a": (False, "Entre 1 et 4, la concentration change, mais la température aussi.", "entre un et quatre، la concentration تبدلات، ولكن حتى la température."),
       "3-b": (False, "Entre 1 et 4, la température change, mais la concentration aussi.", "entre un et quatre، la température تبدلات، ولكن حتى la concentration."),
       "3-c": (True, "Juste : deux paramètres changent, aucune conclusion.", "صحيح: deux paramètres تبدلو، ما كنستنتجو والو.")},
      "(1 ; a) (2 ; b) (3 ; c) : un seul paramètre doit changer.", "un seul paramètre خاصو يتبدل."),
    qcm_facile("fa_tl7_5", "Plus facile : la quantité de soufre", "سؤال ساهل على x max.",
      "n₀(S₂O₃²⁻) = 4,0 mmol ; n₀(H⁺) = 10 mmol ; S₂O₃²⁻ + 2H⁺ → S + SO₂ + H₂O. n(S)f vaut…",
      ["4,0 mmol", "5,0 mmol", "10 mmol"], 0, {
        "0": {"juste": rep("برافو! quatre et cinq: la plus petite، c'est quatre، و n de S égale x max.", "Juste : x_max = 4,0 mmol (S₂O₃²⁻ limitant), n(S)f = 4,0 mmol.")},
        "1": {"1": rep("cinq millimoles هي ديال H plus. ولكن l'ion thiosulfate كيسالي قبل. عاود اختار.", "5,0 mmol vient de H⁺ ; S₂O₃²⁻ s'épuise avant. Réessaie."),
              "2": rep("الجواب: quatre millimoles. القيمة الصغيرة هي x max.", "Réponse : 4,0 mmol, la plus petite valeur.")},
        "2": {"1": rep("dix millimoles هي n zéro ديال H plus، ماشي le soufre. عاود اختار.", "10 mmol est n₀(H⁺), pas n(S). Réessaie."),
              "2": rep("الجواب: n de S égale x max، égale quatre millimoles.", "Réponse : n(S)f = x_max = 4,0 mmol.")}},
      "quatre millimoles de thiosulfate، dix millimoles de H plus. n de S finale vaut ?"),
    qcm_facile("fa_tl7_6", "Plus facile : pourquoi plus rapide ?", "سؤال ساهل على les rencontres.",
      "À la même température, la solution la plus concentrée réagit plus vite parce que…",
      ["les entités se rencontrent plus souvent", "les entités s'agitent plus vite", "l'état final est différent"], 0, {
        "0": {"juste": rep("برافو! كتر ديال les entités ف نفس le volume: كيتلاقاو كتر.", "Juste : plus d'entités dans le même volume, plus de rencontres.")},
        "1": {"1": rep("l'agitation كتتبدل مع la température. وهنا la température هي هي. عاود اختار.", "L'agitation dépend de la température, qui est la même ici. Réessaie."),
              "2": rep("الجواب: كيتلاقاو كتر، حيت كتر ديال les entités. l'agitation هي ديال la température.", "Réponse : plus de rencontres ; l'agitation, c'est la température.")},
        "2": {"1": rep("l'état final ماشي هو السبب ديال la vitesse. فكر ف les entités. عاود اختار.", "L'état final n'explique pas la rapidité. Pense aux entités. Réessaie."),
              "2": rep("الجواب: les entités se rencontrent plus souvent.", "Réponse : les entités se rencontrent plus souvent.")}},
      "À la même température، la solution la plus concentrée réagit plus vite parce que ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même protocole avec une solution de thiosulfate de sodium de concentration C = 0,20 mol/L et V_a = 5,0 mL d'acide chlorhydrique de concentration C_a = 3,0 mol/L ; volume total V = 50 mL. Les quatre expériences sont dans le tableau (figure 1).",
      "intro_dit": "نفس التمرين، بمعطيات أخرى. C égale zéro virgule deux mole par litre، و C a égale trois moles par litre، و V a égale cinq millilitres. le volume total V égale cinquante millilitres.",
      "figures": [tableau("Figure 1 : les quatre expériences", Lb, "V_a = 5,0 mL d'acide dans chaque expérience ; V = 50 mL.")],
      "donnees": ["C = 0,20 mol/L ; C_a = 3,0 mol/L ; V_a = 5,0 mL ; V = 50 mL", "Couples : S₂O₃²⁻(aq)/S(s) et SO₂(aq)/S₂O₃²⁻(aq)"],
      "questions": [
        question_semblable("1", "Écrire les demi-équations des deux couples de l'ion thiosulfate, puis établir l'équation " + EQ + ".",
          phrase(D1 + " ; " + D2 + " ; somme (4e⁻), simplification et ÷ 2 : " + EQ), ["4e⁻", "÷ 2"], ["S₂O₃²⁻(aq) + 2e⁻ ⇌ S(s)"],
          corr([("1 : " + D1 + " ; " + D2, "les deux demi-équations"), (EQ, "قسم sur deux")],
               "les deux demi-équations ont quatre électrons. كنجمعو، كنبسطو، ومن بعد قسم sur deux.")),
        question_semblable("2", "Calculer [S₂O₃²⁻]₀ dans le mélange de l'expérience 1 (en mol/L).",
          valeur("[S₂O₃²⁻]₀", 0.10, "mol/L", "[S₂O₃²⁻]₀ = C·V_S / V = 0,20 × 25 / 50 = 0,10 mol/L"), ["C·V_S / V"], ["[S₂O₃²⁻]₀ = 0,20 mol/L"],
          corr([("2 : [S₂O₃²⁻]₀ = 0,20 × 25 / 50 = 0,10 mol/L", "zéro virgule un mole par litre")],
               "C fois V S sur V، يعني zéro virgule deux fois vingt-cinq sur cinquante، égale zéro virgule un mole par litre.")),
        question_semblable("3", "Quelles expériences pour l'influence de la concentration ? Conclure.",
          phrase("1 et 2 : même θ = 20 °C ; 0,10 et 0,040 mol/L ; Δt = 40 s et 100 s : plus la concentration est grande, plus la transformation est rapide."),
          ["1 et 2", "même θ"], ["1 et 4"],
          corr([("3 : 1 et 2 : Δt = 40 s < 100 s : concentration plus grande, plus rapide", "plus la concentration est grande")],
               "l'expérience un et l'expérience deux: plus la concentration est grande، plus la transformation est rapide.")),
        question_semblable("4", "Quelles expériences pour la température ? Conclure. Critiquer la comparaison des expériences 1 et 4.",
          phrase("2 et 3 : même [S₂O₃²⁻]₀ = 0,040 mol/L ; Δt = 100 s à 20 °C et 35 s à 40 °C : plus θ est élevée, plus c'est rapide. Entre 1 et 4, θ et [S₂O₃²⁻]₀ (0,10 et 0,020 mol/L) changent : aucune conclusion."),
          ["2 et 3", "deux paramètres changent"], ["1 et 4 pour la température"],
          corr([("4 : 2 et 3 : plus θ est élevée, plus c'est rapide ; 1 et 4 : deux paramètres changent.", "deux paramètres تبدلو")],
               "ل la température: deux et trois. entre un et quatre، deux paramètres تبدلو: ما كنستنتجو والو.")),
        question_semblable("5", "Pour l'expérience 1, montrer que H⁺ est en excès et calculer n(S)f en mmol.",
          valeur("n(S)f", 5.0, "mmol", "n₀(S₂O₃²⁻) = 0,20 × 25·10⁻³ = 5,0 mmol ; n₀(H⁺) = 3,0 × 5,0·10⁻³ = 15 mmol ; 15 − 2x_max = 0 ⇒ 7,5 mmol ; x_max = 5,0 mmol ; n(S)f = 5,0 mmol"),
          ["n = C·V", "x_max", "n(S) = x"], ["n(S)f = 7,5 mmol"],
          corr([("5 : 5,0 mmol et 15 mmol ; x_max = 5,0 mmol (S₂O₃²⁻ limitant), H⁺ en excès", "cinq millimoles"), ("n(S)f = 5,0 mmol", "n de S finale")],
               "cinq millimoles et quinze millimoles. x max égale cinq millimoles، l'ion thiosulfate limitant. n de S finale égale cinq millimoles.")),
        question_semblable("6", "Interpréter, à l'échelle des entités, pourquoi l'expérience 1 est plus rapide que l'expérience 2.",
          phrase("Dans l'expérience 1, plus d'ions thiosulfate dans le même volume (0,10 contre 0,040 mol/L) : les entités se rencontrent plus souvent, la transformation est plus rapide."),
          ["se rencontrent plus souvent"], ["plus d'agitation"],
          corr([("6 : plus d'entités dans le même volume : plus de rencontres, plus rapide.", "plus les entités se rencontrent souvent")],
               "plus la concentration est grande، plus les entités se rencontrent souvent، et plus la transformation est rapide.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
