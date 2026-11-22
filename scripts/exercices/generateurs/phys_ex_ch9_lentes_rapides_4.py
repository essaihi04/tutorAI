# Exercice de chimie (physique-chimie), ch. 9 « Transformations lentes et transformations rapides », niveau moyen n° 4 :
# trois expériences, trois courbes n(I₂)(t) — x_max commun, choix des expériences à comparer, température et concentration.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture phys_ch9_transformations_lentes_rapides.md (tl_f8 « une seule
#    variable à la fois », courbes à deux températures / deux concentrations, même palier = réactif limitant),
#    sources_chimie_ch9_ch11.md (exercice type « effet d'un changement de concentration ou de température ») ;
#  - le cours phys_ch9 (tl_f4_courbes, tl_f7_palier, tl_f8_variable, tl_np7, tl_np8) ;
#  - nationaux : 2025 N (trois expériences, associer les courbes, même x_f), 2023 N (quelle courbe, justifier), 2024 N (vrai/faux
#    sur la concentration facteur cinétique) ; ici une situation et des données à nous, sans vitesse ni t½ (ch. 10) ;
#  - séries en ligne : recherche faite (talamidi, moutamadris, dreamjob) ; PDF non ouverts (hôtes hors du réseau autorisé).
#  Courbes calculées avec le modèle de courbe-reglable.html : n(I₂) = n₀(H₂O₂)·(1 − e^(−t/τ)),
#  τ = 6 min · 3^((20 − θ)/20) · (0,1/[I⁻]₀) ; palier atteint vers 5τ.
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch9_lentes_rapides_4"
SIM = "/media/simulations/chimie/transformations-lentes-rapides-tableau/"


def tau(theta, c):
    return 6 * 3 ** ((20 - theta) / 20) * (0.1 / c)


def courbes(n0, exps, etiq, titre, ymax, grad_y, tmax=40):
    """exps : {k: (θ, c)} ; etiq : [(lettre, k, couleur, t_étiquette)]."""
    els = []
    for L, k, col, tx in etiq:
        th, c = exps[k]
        els.append({"f": "courbe", "expr": f"{n0}*(1-exp(-x/{round(tau(th, c), 4)}))", "couleur": col, "texte": f"({L})", "texte_x": round(tx, 2), "pos": "e"})
    return figure_courbe(titre, axe("t", 0, tmax, "min", list(range(0, tmax + 1, 5))),
                         axe("n(I₂)", 0, ymax, "mmol", grad_y), els,
                         legende="Même volume V = 100 mL et même quantité initiale d'eau oxygénée dans les trois expériences.")


def tableau_exp(titre, lignes):
    """Tableau des conditions : colonnes Expérience | θ (°C) | [I⁻]₀ (mol/L)."""
    g = [{"f": "rect", "de": [0.5, 0.3], "a": [11.5, 4.3]}]
    g += fil([0.5, 3.3], [11.5, 3.3]) + fil([3.5, 0.3], [3.5, 4.3]) + fil([7.5, 0.3], [7.5, 4.3])
    g += fil([0.5, 2.3], [11.5, 2.3]) + fil([0.5, 1.3], [11.5, 1.3])
    g += texte([2.0, 3.65], "Expérience", couleur="jaune") + texte([5.5, 3.65], "θ (°C)", couleur="jaune") + texte([9.5, 3.65], "[I⁻]₀ (mol/L)", couleur="jaune")
    for i, (k, th, c) in enumerate(lignes):
        y = 2.65 - i
        g += texte([2.0, y], k) + texte([5.5, y], th) + texte([9.5, y], c)
    return schema(titre, 12, 4.6, g)


N0 = 3.0
EXPS = {1: (20, 0.10), 2: (20, 0.20), 3: (40, 0.20)}
taus = {k: tau(*v) for k, v in EXPS.items()}
assert abs(taus[1] - 6) < 1e-9 and abs(taus[2] - 3) < 1e-9 and abs(taus[3] - 1) < 1e-9
nI2 = round(0.20 * 0.100 * 1e3, 9)                 # 20 mmol (expérience 2)
xm = {k: min(N0, round(c * 0.100 * 1e3, 9) / 2) for k, (th, c) in EXPS.items()}
assert abs(nI2 - 20) < 1e-9 and all(abs(v - 3.0) < 1e-9 for v in xm.values())
# semblable
N0b = 4.0
EXPSb = {1: (20, 0.15), 2: (40, 0.15), 3: (40, 0.30)}
nI3b = round(0.30 * 0.100 * 1e3, 9)                # 30 mmol (expérience 3)
xmb = {k: min(N0b, round(c * 0.100 * 1e3, 9) / 2) for k, (th, c) in EXPSb.items()}
assert abs(nI3b - 30) < 1e-9 and all(abs(v - 4.0) < 1e-9 for v in xmb.values())
tb = {k: tau(*v) for k, v in EXPSb.items()}
assert tb[3] < tb[2] < tb[1]

EQ = "H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l)"
GY = [[k * 0.5, f"{k * 0.5:.1f}".replace(".", ",")] for k in range(8)]

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "transformations_lentes_rapides", "cours": "phys_ch9_transformations_lentes_rapides",
  "titre": "Trois expériences, trois courbes : température et concentration", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Établir l'équation d'oxydoréduction", "Montrer que x_max ne dépend pas des facteurs cinétiques",
                  "Choisir deux expériences qui ne diffèrent que par un seul paramètre", "Associer une courbe à une expérience et justifier"],
  "enonce": {
    "intro": "On étudie la réaction lente entre l'eau oxygénée H₂O₂(aq) et les ions iodure I⁻(aq), en milieu acide (ions H⁺(aq) en excès). On réalise trois expériences ; chaque mélange a un volume V = 100 mL et contient la même quantité initiale d'eau oxygénée n₀(H₂O₂) = 3,0 mmol. Les conditions sont données dans le tableau (figure 1). On suit la quantité de diiode formé : on obtient les courbes (a), (b) et (c) de la figure 2.",
    "intro_dit": "نقراو l'énoncé. la réaction lente بين l'eau oxygénée و les ions iodure، فوسط حمضي. trois expériences: فكل وحدة le volume V égale cent millilitres، و n zéro ديال l'eau oxygénée égale trois millimoles. les conditions ف le tableau، la figure un. وكنتبعو la quantité ديال le diiode: هادي les courbes a، b، et c ف la figure deux.",
    "figures": [tableau_exp("Figure 1 : les conditions des trois expériences", [("1", "20", "0,10"), ("2", "20", "0,20"), ("3", "40", "0,20")]),
                courbes(N0, EXPS, [("a", 3, "rouge", 1.6), ("b", 2, "orange", 4.8), ("c", 1, "cyan", 9.7)],
                        "Figure 2 : n(I₂) en fonction du temps", 3.5, GY)],
    "donnees": ["V = 100 mL = 0,100 L pour chaque mélange", "n₀(H₂O₂) = 3,0 mmol dans chaque expérience",
                "Couples : H₂O₂(aq)/H₂O(l) et I₂(aq)/I⁻(aq)"],
    "questions": [
      question("1", "Écrire les demi-équations des deux couples, puis établir l'équation de la réaction.",
        "السؤال un: كتب les demi-équations ديال les deux couples، ومن بعد استنتج l'équation ديال la réaction.",
        phrase("H₂O₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ 2H₂O(l) ; I₂(aq) + 2e⁻ ⇌ 2I⁻(aq). Réduction de H₂O₂ et oxydation 2I⁻(aq) → I₂(aq) + 2e⁻ : 2 électrons de chaque côté, on additionne : " + EQ + "."),
        ["2H⁺(aq)", "2e⁻", "2H₂O(l)", "2I⁻(aq) → I₂(aq) + 2e⁻", "→"], ["H₂O₂(aq) + 2e⁻ ⇌ 2H₂O(l)", "H₂O₂(aq) + I⁻(aq) → I₂(aq) + H₂O(l)"],
        [aide("Pour H₂O₂/H₂O : les oxygènes avec H₂O, les hydrogènes avec H⁺, puis les charges avec e⁻. Pour I₂/I⁻ : les atomes d'iode, puis les charges.",
              "ف le couple eau oxygénée sur eau: les oxygènes ب l'eau، les hydrogènes ب H plus، ومن بعد les charges ب les électrons. ف le couple diiode sur ion iodure: les atomes d'iode، ومن بعد les charges."),
         aide("H₂O₂ capte les électrons (réduction), I⁻ les cède (oxydation). Les deux demi-équations ont 2e⁻ : additionne-les sans multiplier.",
              "l'eau oxygénée كتشد les électrons، هادي la réduction. les ions iodure كيعطيوهم، هادي l'oxydation. les deux demi-équations ont deux électrons: جمعهم بلا ما تضرب.")],
        corr([("1 : H₂O₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ 2H₂O(l)", "eau oxygénée plus deux H plus plus deux électrons"),
              ("I₂(aq) + 2e⁻ ⇌ 2I⁻(aq)", "diiode plus deux électrons donne deux ions iodure"),
              (EQ, "l'équation: eau oxygénée plus deux ions iodure")],
             "السؤال un. le couple eau oxygénée sur eau: eau oxygénée plus deux H plus plus deux électrons، donne deux molécules d'eau. le couple diiode sur ion iodure: diiode plus deux électrons donne deux ions iodure. l'eau oxygénée كتشد les électrons، و les ions iodure كيعطيوهم، و les deux demi-équations ont deux électrons. كنجمعو. l'équation: eau oxygénée plus deux ions iodure، plus deux H plus، donne diiode plus deux molécules d'eau."),
        "ex_tl4_1", "fa_tl4_1"),
      question("2", "Calculer, en mmol, la quantité initiale d'ions iodure n₀(I⁻) dans l'expérience 2.",
        "السؤال deux: حسب ب millimole la quantité initiale ديال les ions iodure فl'expérience deux.",
        valeur("n₀(I⁻)", 20.0, "mmol", "n₀(I⁻) = [I⁻]₀·V = 0,20 × 0,100 = 2,0·10⁻² mol = 20 mmol"),
        ["n = C·V", "[I⁻]₀", "0,100 L", "mmol"], ["n = 0,20 × 100 = 20 mol", "n = 0,20 / 0,100"],
        [aide("Dans l'expérience 2, lis [I⁻]₀ dans le tableau (figure 1). Le volume du mélange est V = 100 mL, à écrire en litres.",
              "فl'expérience deux، قرا la concentration ديال les ions iodure ف le tableau. و le volume V égale cent millilitres، كتبو بالlitre."),
         aide("n₀(I⁻) = [I⁻]₀·V avec V = 0,100 L ; puis 1 mmol = 10⁻³ mol.",
              "n zéro égale la concentration fois V، و V égale zéro virgule un litre. ومن بعد، un millimole égale dix puissance moins trois mole.")],
        corr([("2 : n₀(I⁻) = [I⁻]₀·V", "n zéro égale la concentration fois V"),
              ("A.N. : n₀(I⁻) = 0,20 × 0,100 = 2,0·10⁻² mol", "zéro virgule deux fois zéro virgule un"),
              ("n₀(I⁻) = 20 mmol", "vingt millimoles")],
             "السؤال deux. n zéro égale la concentration fois V. l'application numérique: zéro virgule deux fois zéro virgule un، égale deux fois dix puissance moins deux mole، يعني vingt millimoles."),
        "ex_tl4_2", "fa_tl4_2"),
      question("3", "Montrer que l'avancement maximal est le même dans les trois expériences ; donner sa valeur et le réactif limitant.",
        "السؤال trois: بين بلي l'avancement maximal هو هو فles trois expériences، وعطي la valeur ديالو و le réactif limitant.",
        valeur("x_max", 3.0, "mmol", "H₂O₂ : 3,0 − x_max = 0 ⇒ 3,0 mmol ; I⁻ : 10 − 2x_max = 0 ⇒ 5,0 mmol (exp. 1), 20 − 2x_max = 0 ⇒ 10 mmol (exp. 2 et 3) ; H₂O₂ limitant partout : x_max = 3,0 mmol"),
        ["n₀ − x", "n₀ − 2x", "la plus petite valeur", "réactif limitant", "x_max"], ["x_max = 5,0 mmol", "x_max = 10 mmol", "I⁻ limitant"],
        [aide("Calcule n₀(I⁻) dans chaque expérience (0,10 ou 0,20 mol/L dans 0,100 L). Pour chaque réactif, cherche la valeur de x qui l'épuise.",
              "حسب n zéro ديال les ions iodure فكل expérience. ومن بعد، لكل réactif، قلب على x اللي كيخليه يسالي."),
         aide("H₂O₂ : 3,0 − x_max = 0 ; I⁻ : n₀(I⁻) − 2x_max = 0. Garde la plus petite valeur dans chaque expérience.",
              "l'eau oxygénée: trois moins x max égale zéro. les ions iodure: n zéro moins deux x max égale zéro. وفكل expérience، خود القيمة الصغيرة.")],
        corr([("3 : H₂O₂ : 3,0 − x_max = 0 ⇒ x_max = 3,0 mmol", "trois moins x max égale zéro"),
              ("I⁻ : 10 − 2x_max = 0 ⇒ 5,0 mmol (exp. 1) ; 20 − 2x_max = 0 ⇒ 10 mmol (exp. 2 et 3)", "dix moins deux x max"),
              ("Dans les trois expériences, H₂O₂ est limitant : x_max = 3,0 mmol.", "x max égale trois millimoles")],
             "السؤال trois. l'eau oxygénée: trois moins x max égale zéro، كتعطي x max à trois millimoles. les ions iodure: dix moins deux x max égale zéro، donne cinq millimoles فl'expérience un، et vingt moins deux x max égale zéro، donne dix millimoles فl'expérience deux et trois. ديما القيمة الصغيرة هي ديال l'eau oxygénée: هي le réactif limitant، و x max égale trois millimoles فles trois expériences."),
        "ex_tl4_3", "fa_tl4_3"),
      question("4", "Quelles expériences faut-il comparer pour étudier l'influence de la température ? Et celle de la concentration initiale des ions iodure ? Pourquoi ne peut-on rien conclure en comparant les expériences 1 et 3 ?",
        "السؤال quatre: شمن expériences نقارنو باش نعرفو l'influence ديال la température؟ وديال la concentration initiale ديال les ions iodure؟ وعلاش ما نقدرو نستنتجو والو من l'expérience un et l'expérience trois؟",
        phrase("Température : expériences 2 et 3 (même [I⁻]₀ = 0,20 mol/L, seule θ change). Concentration : expériences 1 et 2 (même θ = 20 °C, seule [I⁻]₀ change). Entre 1 et 3, la température ET la concentration changent : on ne peut pas savoir lequel des deux facteurs cause la différence."),
        ["une seule variable", "2 et 3", "1 et 2", "θ", "[I⁻]₀"], ["1 et 3 pour la température", "1 et 2 pour la température"],
        [aide("Dans le tableau, compare les lignes deux par deux : quelle colonne change, quelle colonne reste la même ?",
              "ف le tableau، قارن les lignes، deux par deux: شمن colonne كتبدل، وشمن colonne كتبقى هي هي؟"),
         aide("Règle : pour étudier un facteur, on compare deux expériences qui ne diffèrent que par ce seul paramètre.",
              "la règle: pour un facteur، deux expériences، qui ne diffèrent que par ce seul paramètre.")],
        corr([("4 : température : expériences 2 et 3 (seule θ change)", "la température: l'expérience deux et l'expérience trois"),
              ("concentration : expériences 1 et 2 (seule [I⁻]₀ change)", "la concentration: l'expérience un et l'expérience deux"),
              ("1 et 3 : deux paramètres changent, on ne peut rien conclure.", "deux paramètres تبدلو")],
             "السؤال quatre. باش نقراو la température: l'expérience deux et l'expérience trois، حيت غير la température اللي تبدلات. باش نقراو la concentration: l'expérience un et l'expérience deux، حيت غير la concentration اللي تبدلات. بين l'expérience un et l'expérience trois، deux paramètres تبدلو: ما نعرفوش شكون دار الفرق، إذن ما كنستنتجو والو."),
        "ex_tl4_4", "fa_tl4_4"),
      question("5", "En exploitant la figure 2, associer chaque courbe (a), (b) et (c) à son expérience. Justifier.",
        "السؤال cinq: من la figure deux، ربط كل courbe، a، b، et c، مع l'expérience ديالها. برر الجواب.",
        phrase("Les trois courbes ont le même palier 3,0 mmol (même x_max). L'expérience 1 (20 °C ; 0,10 mol/L) est la plus lente : courbe (c), palier vers 30 min. L'expérience 2 (20 °C ; 0,20 mol/L) est plus rapide que 1 car [I⁻]₀ est plus grande : courbe (b), palier vers 15 min. L'expérience 3 (40 °C ; 0,20 mol/L) est plus rapide que 2 car θ est plus élevée : courbe (a), palier vers 5 min."),
        ["(a) ↔ 3", "même palier", "plus raide au début", "température", "concentration"], ["(a) ↔ 1", "le palier le plus haut est le plus rapide"],
        [aide("Les paliers sont-ils différents ? Regarde plutôt à quelle date chaque courbe atteint son palier, et laquelle monte le plus vite au début.",
              "واش les paliers مختلفين؟ شوف بالأحرى فوقاش كل courbe كتوصل ل le palier ديالها، وشكون كتطلع بالزربة فالبداية."),
         aide("Utilise la question 4 : 2 est plus rapide que 1 (concentration plus grande), 3 est plus rapide que 2 (température plus élevée). La courbe la plus raide au début est la plus rapide.",
              "خدم ب السؤال quatre: l'expérience deux plus rapide من l'expérience un، حيت la concentration أكبر. l'expérience trois plus rapide من l'expérience deux، حيت la température أكبر. la courbe la plus raide au début، هي la plus rapide.")],
        corr([("5 : même palier 3,0 mmol : même x_max (H₂O₂ limitant).", "نفس le palier"),
              ("Exp. 3 la plus rapide → (a) ; exp. 2 → (b) ; exp. 1 la plus lente → (c).", "l'expérience trois هي la courbe a")],
             "السؤال cinq. les trois courbes عندهم نفس le palier، trois millimoles، حيت نفس x max. l'expérience trois، à quarante degrés Celsius et zéro virgule deux mole par litre، هي la plus rapide: l'expérience trois هي la courbe a، كتوصل environ à cinq minutes. l'expérience deux هي la courbe b، environ à quinze minutes. و l'expérience un، la plus lente، هي la courbe c، environ à trente minutes."),
        "ex_tl4_5", "fa_tl4_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_tl4_1", "Question 1 : l'équation eau oxygénée / ions iodure", "Réduction de H₂O₂, oxydation de I⁻ : deux électrons de chaque côté.",
      SIM + "equation.html?vue=eau_oxygenee", "Deux demi-équations, puis leur somme, puis la vérification",
      "عندنا les deux couples: eau oxygénée sur eau، و diiode sur ion iodure. اللول، la réduction ديال l'eau oxygénée: eau oxygénée plus deux H plus plus deux électrons، donne deux molécules d'eau. التاني، l'oxydation ديال les ions iodure: deux ions iodure donne diiode plus deux électrons. les deux ont deux électrons: كنجمعو، و les électrons كيمشيو. le résultat: eau oxygénée plus deux ions iodure، plus deux H plus، donne diiode plus deux molécules d'eau. ونتأكدو من les éléments و les charges: zéro على اليسار، et zéro على اليمين.",
      centre=[(EQ, "le résultat: eau oxygénée plus deux ions iodure")],
      pointage=[{"mot": "عندنا les deux couples", "commande": "play_until", "parametres": {"moment": "couples"}},
                {"mot": "اللول، la réduction", "commande": "play_until", "parametres": {"moment": "reduction"}},
                {"mot": "التاني، l'oxydation", "commande": "play_until", "parametres": {"moment": "oxydation"}},
                {"mot": "كنجمعو، و les électrons كيمشيو", "commande": "play_until", "parametres": {"moment": "additionner"}},
                {"mot": "le résultat: eau oxygénée plus deux ions iodure", "repere": "bilan"},
                {"mot": "le résultat: eau oxygénée plus deux ions iodure", "cible": "centre:0"},
                {"mot": "ونتأكدو من les éléments", "commande": "play_until", "parametres": {"moment": "verifier"}}]),
    diapo_sim("ex_tl4_2", "Question 2 : n₀(I⁻) = [I⁻]₀·V", "Concentration deux fois plus grande dans le même volume : deux fois plus d'ions.",
      SIM + "rappels.html?vue=concentration", "C = n/V : doubler la quantité dans le même volume double la concentration",
      "شوف le bécher: zéro virgule zéro un mole dans cent millilitres، la concentration égale zéro virgule un mole par litre. دابا، deux fois plus de soluté، فنفس le volume: la concentration devient zéro virgule deux mole par litre. la relation: C égale n sur V، إذن n égale C fois V. فl'expérience deux: zéro virgule deux mole par litre، fois zéro virgule un litre، égale zéro virgule zéro deux mole، يعني vingt millimoles. وفl'expérience un، zéro virgule un mole par litre، كتعطي la moitié: dix millimoles.",
      centre=[("n₀(I⁻) = 0,20 × 0,100 = 20 mmol", "يعني vingt millimoles")],
      pointage=[{"mot": "شوف le bécher", "commande": "play_until", "parametres": {"moment": "becher"}},
                {"mot": "دابا، deux fois plus de soluté", "commande": "play_until", "parametres": {"moment": "double_n"}},
                {"mot": "la relation: C égale n sur V", "commande": "play_until", "parametres": {"moment": "formule"}},
                {"mot": "يعني vingt millimoles", "cible": "centre:0"}]),
    diapo_sim("ex_tl4_3", "Question 3 : le même palier", "H₂O₂ limitant : le palier vaut n₀(H₂O₂), quelle que soit [I⁻]₀.",
      SIM + "courbe-reglable.html?vue=concentration", "La courbe n(I₂)(t) qu'on règle : [I⁻]₀ et n₀(H₂O₂)",
      "شوف les axes: la quantité ديال le diiode ب millimole، و le temps ب minute. نديرو n zéro ديال l'eau oxygénée égale trois millimoles، و la concentration ديال les ions iodure zéro virgule un mole par litre. la courbe كتطلع وكتوقف à trois millimoles. دابا la concentration zéro virgule deux mole par litre: la courbe كتطلع بالزربة، ولكن كتوقف حتى هي à trois millimoles. علاش؟ l'eau oxygénée هي le réactif limitant: trois moins x max égale zéro، إذن x max égale trois millimoles. les ions iodure en excès: dix ou vingt millimoles، يكفيو بزاف. إذن نفس x max فles trois expériences.",
      centre=[("x_max = n₀(H₂O₂) = 3,0 mmol (H₂O₂ limitant)", "إذن x max égale trois millimoles")],
      pointage=[{"mot": "شوف les axes", "commande": "play_until", "parametres": {"moment": "axes"}},
                {"mot": "شوف les axes", "repere": "axe_n"},
                {"mot": "n zéro ديال l'eau oxygénée égale trois millimoles", "commande": "set_parameters", "parametres": {"c_iodure": 0.1, "n_h2o2_mmol": 3}},
                {"mot": "دابا la concentration zéro virgule deux", "commande": "set_parameters", "parametres": {"c_iodure": 0.2}},
                {"mot": "إذن x max égale trois millimoles", "cible": "centre:0"}]),
    diapo_sim("ex_tl4_4", "Question 4 : une seule variable à la fois", "Deux expériences qui ne diffèrent que par UN paramètre.",
      SIM + "facteurs.html?vue=une_variable", "Un tableau de trois expériences : on compare les lignes deux à deux",
      "شوف هاد le tableau ديال le cours: trois expériences. on compare un et deux: غير la température اللي تبدلات، إذن كنقراو la température. on compare deux et trois: غير la concentration اللي تبدلات. et un et trois؟ deux paramètres تبدلو: ما كنستنتجو والو. la règle: pour un facteur، deux expériences، qui ne diffèrent que par ce seul paramètre. فالتمرين ديالنا، le tableau مختلف: la température، l'expérience deux et l'expérience trois. la concentration، l'expérience un et l'expérience deux. et un et trois، حتى هنا، deux paramètres تبدلو.",
      centre=[("Température : 2 et 3", "la température، l'expérience deux et l'expérience trois"), ("Concentration : 1 et 2", "la concentration، l'expérience un et l'expérience deux"), ("1 et 3 : deux changements, aucune conclusion", "حتى هنا، deux paramètres تبدلو")],
      pointage=[{"mot": "شوف هاد le tableau", "commande": "play_until", "parametres": {"moment": "tableau"}},
                {"mot": "on compare un et deux", "commande": "play_until", "parametres": {"moment": "comparer_1_2"}},
                {"mot": "on compare deux et trois", "commande": "play_until", "parametres": {"moment": "comparer_2_3"}},
                {"mot": "et un et trois؟", "commande": "play_until", "parametres": {"moment": "comparer_1_3"}},
                {"mot": "la règle: pour un facteur", "commande": "play_until", "parametres": {"moment": "conclusion"}},
                {"mot": "la température، l'expérience deux et l'expérience trois", "cible": "centre:0"},
                {"mot": "la concentration، l'expérience un et l'expérience deux", "cible": "centre:1"},
                {"mot": "حتى هنا، deux paramètres تبدلو", "cible": "centre:2"}]),
    diapo_sim("ex_tl4_5", "Question 5 : quelle courbe pour quelle expérience ?", "Même palier ; la courbe la plus raide au début est la plus rapide.",
      SIM + "courbe-reglable.html?vue=temperature", "Deux courbes n(I₂)(t) : 20 °C puis 40 °C",
      "شوف هاد les courbes ديال le cours. la courbe à vingt degrés Celsius كتطلع بشوية، وكتوصل le palier environ à trente minutes. la courbe à quarante degrés Celsius كتطلع بالزربة، وكتوصل environ à dix minutes. نفس le palier. و la courbe la plus raide au début، هي la plus rapide. فالتمرين ديالنا: l'expérience un هي la plus lente، courbe c. l'expérience deux، أكثر ديال les ions iodure، courbe b. و l'expérience trois، نفس la concentration ولكن أسخن، هي la plus rapide: courbe a.",
      centre=[("Même palier : même x_max", "نفس le palier"), ("(a) ↔ 3 ; (b) ↔ 2 ; (c) ↔ 1", "هي la plus rapide: courbe a")],
      pointage=[{"mot": "شوف هاد les courbes", "commande": "play_until", "parametres": {"moment": "axes"}},
                {"mot": "la courbe à vingt degrés Celsius", "commande": "play_until", "parametres": {"moment": "courbe_froid"}},
                {"mot": "la courbe à quarante degrés Celsius", "commande": "play_until", "parametres": {"moment": "courbe_chaud"}},
                {"mot": "نفس le palier", "commande": "play_until", "parametres": {"moment": "meme_palier"}},
                {"mot": "نفس le palier", "cible": "centre:0"},
                {"mot": "la courbe la plus raide au début", "commande": "play_until", "parametres": {"moment": "plus_raide"}},
                {"mot": "هي la plus rapide: courbe a", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_tl4_1", "Plus facile : l'équation", "سؤال ساهل: اختار l'équation الصحيحة.",
      "L'équation de la réaction entre H₂O₂(aq) et I⁻(aq) en milieu acide est…",
      ["H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l)", "H₂O₂(aq) + I⁻(aq) + H⁺(aq) → I₂(aq) + H₂O(l)", "H₂O₂(aq) + 2I⁻(aq) + 2e⁻ → I₂(aq) + 2H₂O(l)"], 0, {
        "0": {"juste": rep("برافو! les atomes و les charges متساويين، وما كاين حتى électron.", "Juste : éléments et charges conservés, aucun électron.")},
        "1": {"1": rep("ما تقلقش. حسب les atomes d'iode: deux على اليمين ف le diiode. وعلى اليسار؟ عاود اختار.", "Compte les atomes d'iode : 2 dans I₂. Et à gauche ? Réessaie."),
              "2": rep("الجواب: deux ions iodure et deux H plus، pour avoir deux atomes d'iode و les charges متساويين.", "Réponse : 2I⁻ et 2H⁺, pour conserver l'iode et les charges.")},
        "2": {"1": rep("قريب. ولكن واش les électrons كيبانو ف l'équation ديال la réaction؟ عاود اختار.", "Les électrons apparaissent-ils dans l'équation de la réaction ? Réessaie."),
              "2": rep("الجواب: ما كاين حتى électron ف l'équation، كيمشيو ملي كنجمعو. وخاص les deux H plus.", "Réponse : pas d'électrons dans l'équation ; il faut 2H⁺.")}},
      "L'équation de la réaction entre l'eau oxygénée et les ions iodure، en milieu acide، est ?"),
    qcm_facile("fa_tl4_2", "Plus facile : n₀(I⁻)", "سؤال ساهل على n égale C fois V.",
      "[I⁻]₀ = 0,20 mol/L et V = 100 mL. n₀(I⁻) vaut…",
      ["2,0 mmol", "20 mmol", "20 mol"], 1, {
        "1": {"juste": rep("برافو! zéro virgule deux fois zéro virgule un، égale vingt millimoles.", "Juste : 0,20 × 0,100 = 0,020 mol = 20 mmol.")},
        "0": {"1": rep("قريب. حسب مزيان: zéro virgule deux fois zéro virgule un، شحال بالmole؟ ومن بعد بدل لmillimole. عاود اختار.", "Refais 0,20 × 0,100 en mol, puis convertis en mmol. Réessaie."),
              "2": rep("الجواب: zéro virgule zéro deux mole، يعني vingt millimoles، pas deux.", "Réponse : 0,020 mol = 20 mmol (pas 2,0).")},
        "2": {"1": rep("ما تقلقش. V خاصو يكون بالlitre، ماشي ب millilitre. عاود اختار.", "V doit être en litres. Réessaie."),
              "2": rep("الجواب: vingt millimoles. le résultat vingt mole، c'est zéro virgule deux fois cent: V بقا ب millilitre.", "Réponse : 20 mmol ; 20 mol vient de V laissé en mL.")}},
      "La concentration égale zéro virgule deux mole par litre، et V égale cent millilitres. n zéro vaut ?"),
    vrai_faux_facile("fa_tl4_3", "Plus facile : vrai ou faux", "قول واش هاد الجمل صحيحة ولا غالطة.",
      "n₀(H₂O₂) = 3,0 mmol dans les trois expériences ; n₀(I⁻) = 10 ou 20 mmol.",
      [("Dans les trois expériences, H₂O₂ est le réactif limitant.", True, "H₂O₂ donne x_max = 3,0 mmol ; I⁻ donnerait 5,0 ou 10 mmol."),
       ("Doubler [I⁻]₀ double l'avancement maximal.", False, "I⁻ est en excès : x_max reste n₀(H₂O₂) = 3,0 mmol ; seule la durée change."),
       ("Le palier des courbes vaut 3,0 mmol dans les trois expériences.", True, "n(I₂) = x et, à la fin, x = x_max = 3,0 mmol.")]),
    association_facile("fa_tl4_4", "Plus facile : quel paramètre ?", "ربط كل comparaison ديال les expériences مع شنو كيسمح نعرفو.",
      "Expériences : 1 (20 °C ; 0,10 mol/L), 2 (20 °C ; 0,20 mol/L), 3 (40 °C ; 0,20 mol/L).",
      "Relie chaque comparaison à ce qu'elle permet d'étudier.",
      [("1", "Comparer 1 et 2"), ("2", "Comparer 2 et 3"), ("3", "Comparer 1 et 3")],
      [("a", "l'influence de la concentration"), ("b", "l'influence de la température"), ("c", "rien : deux paramètres changent")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Juste : entre 1 et 2, seule [I⁻]₀ change.", "صحيح: entre un et deux، غير la concentration اللي تبدلات."),
       "1-b": (False, "Entre 1 et 2, θ vaut 20 °C deux fois : regarde l'autre colonne.", "شوف: entre un et deux، la température هي هي. شمن colonne اللي تبدلات؟"),
       "1-c": (False, "Entre 1 et 2, un seul paramètre change : on peut conclure.", "لا، entre un et deux، seulement un paramètre تبدل: نقدرو نستنتجو."),
       "2-a": (False, "Entre 2 et 3, [I⁻]₀ vaut 0,20 mol/L deux fois : regarde θ.", "entre deux et trois، la concentration هي هي. شوف la température."),
       "2-b": (True, "Juste : entre 2 et 3, seule θ change.", "صحيح: entre deux et trois، غير la température اللي تبدلات."),
       "2-c": (False, "Entre 2 et 3, un seul paramètre change : on peut conclure.", "لا، entre deux et trois، seulement un paramètre تبدل."),
       "3-a": (False, "Entre 1 et 3, la concentration change, mais la température aussi.", "entre un et trois، la concentration تبدلات، ولكن حتى la température."),
       "3-b": (False, "Entre 1 et 3, la température change, mais la concentration aussi.", "entre un et trois، la température تبدلات، ولكن حتى la concentration."),
       "3-c": (True, "Juste : deux paramètres changent, on ne sait pas lequel agit.", "صحيح: deux paramètres تبدلو، ما نعرفوش شكون دار الفرق.")},
      "(1 ; a) (2 ; b) (3 ; c) : un seul paramètre doit changer.", "un seul paramètre خاصو يتبدل بين les deux expériences."),
    qcm_facile("fa_tl4_5", "Plus facile : la courbe de l'expérience 3", "سؤال ساهل على les courbes.",
      "L'expérience 3 (40 °C ; 0,20 mol/L) est la plus rapide. Sa courbe est…",
      ["celle qui a le palier le plus haut", "celle qui atteint son palier le plus tôt", "celle qui monte le plus lentement au début"], 1, {
        "1": {"juste": rep("برافو! la plus rapide كتوصل ل le palier اللولة، وهي la plus raide au début: courbe a.", "Juste : la plus rapide atteint son palier la première (courbe a).")},
        "0": {"1": rep("ما تقلقش. واش les paliers مختلفين هنا؟ شوف: نفس x max. عاود اختار.", "Les paliers sont-ils différents ici ? Même x_max. Réessaie."),
              "2": rep("الجواب: اللي كتوصل اللولة ل le palier. le palier هو هو، حيت نفس x max.", "Réponse : celle qui atteint son palier le plus tôt ; le palier est le même.")},
        "2": {"1": rep("لا، اللي كتطلع بشوية هي la plus lente. والسريعة؟ عاود اختار.", "Celle qui monte lentement est la plus lente. Et la plus rapide ? Réessaie."),
              "2": rep("الجواب: la plus rapide كتطلع بالزربة وكتوصل اللولة ل le palier.", "Réponse : la plus rapide monte vite et atteint son palier la première.")}},
      "L'expérience trois est la plus rapide. Sa courbe est ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même réaction (H⁺(aq) en excès), trois expériences de volume V = 100 mL, avec n₀(H₂O₂) = 4,0 mmol dans chacune. Conditions : figure 1 ; courbes n(I₂)(t) : figure 2.",
      "intro_dit": "نفس la réaction، trois expériences: V égale cent millilitres، و n zéro ديال l'eau oxygénée égale quatre millimoles. les conditions ف la figure un، و les courbes ف la figure deux.",
      "figures": [tableau_exp("Figure 1 : les conditions des trois expériences", [("1", "20", "0,15"), ("2", "40", "0,15"), ("3", "40", "0,30")]),
                  courbes(N0b, EXPSb, [("a", 2, "orange", 2.15), ("b", 3, "rouge", 1.07), ("c", 1, "cyan", 6.4)],
                          "Figure 2 : n(I₂) en fonction du temps", 4.5, [[k * 0.5, f"{k * 0.5:.1f}".replace(".", ",")] for k in range(10)], tmax=20)],
      "donnees": ["V = 100 mL = 0,100 L", "n₀(H₂O₂) = 4,0 mmol dans chaque expérience", "Couples : H₂O₂(aq)/H₂O(l) et I₂(aq)/I⁻(aq)"],
      "questions": [
        question_semblable("1", "Écrire les demi-équations des deux couples, puis établir l'équation de la réaction.",
          phrase("H₂O₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ 2H₂O(l) ; I₂(aq) + 2e⁻ ⇌ 2I⁻(aq) ; " + EQ),
          ["2H⁺(aq)", "2e⁻", "→"], ["H₂O₂(aq) + I⁻(aq) → I₂(aq) + H₂O(l)"],
          corr([("1 : H₂O₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ 2H₂O(l) ; I₂(aq) + 2e⁻ ⇌ 2I⁻(aq)", "les deux demi-équations"), (EQ, "l'équation")],
               "les deux demi-équations ont deux électrons، كنجمعو. l'équation: eau oxygénée plus deux ions iodure، plus deux H plus، donne diiode plus deux molécules d'eau.")),
        question_semblable("2", "Calculer, en mmol, la quantité initiale d'ions iodure n₀(I⁻) dans l'expérience 3.",
          valeur("n₀(I⁻)", 30.0, "mmol", "n₀(I⁻) = [I⁻]₀·V = 0,30 × 0,100 = 3,0·10⁻² mol = 30 mmol"), ["n = C·V", "0,100 L"], ["n = 0,30 × 100 = 30 mol"],
          corr([("2 : n₀(I⁻) = 0,30 × 0,100 = 3,0·10⁻² mol", "zéro virgule trois fois zéro virgule un"), ("n₀(I⁻) = 30 mmol", "trente millimoles")],
               "n zéro égale zéro virgule trois fois zéro virgule un، égale trois fois dix puissance moins deux mole، يعني trente millimoles.")),
        question_semblable("3", "Montrer que l'avancement maximal est le même dans les trois expériences ; donner sa valeur et le réactif limitant.",
          valeur("x_max", 4.0, "mmol", "H₂O₂ : 4,0 − x_max = 0 ⇒ 4,0 mmol ; I⁻ : 15 − 2x_max = 0 ⇒ 7,5 mmol (exp. 1 et 2), 30 − 2x_max = 0 ⇒ 15 mmol (exp. 3) ; H₂O₂ limitant : x_max = 4,0 mmol"),
          ["n₀ − x", "n₀ − 2x", "x_max"], ["x_max = 7,5 mmol"],
          corr([("3 : H₂O₂ : x_max = 4,0 mmol ; I⁻ : 7,5 mmol ou 15 mmol", "quatre millimoles"), ("H₂O₂ limitant partout : x_max = 4,0 mmol", "x max égale quatre millimoles")],
               "l'eau oxygénée donne quatre millimoles، و les ions iodure sept virgule cinq ou quinze millimoles. الصغيرة ديما، c'est quatre millimoles: l'eau oxygénée limitant، و x max égale quatre millimoles.")),
        question_semblable("4", "Quelles expériences comparer pour la température ? Pour la concentration ? Pourquoi rien entre 1 et 3 ?",
          phrase("Température : 1 et 2 (même [I⁻]₀ = 0,15 mol/L). Concentration : 2 et 3 (même θ = 40 °C). Entre 1 et 3, θ et [I⁻]₀ changent toutes les deux : aucune conclusion."),
          ["une seule variable", "1 et 2", "2 et 3"], ["1 et 3"],
          corr([("4 : température : 1 et 2 ; concentration : 2 et 3", "la température: un et deux"), ("1 et 3 : deux paramètres changent.", "deux paramètres")],
               "la température: un et deux. la concentration: deux et trois. entre un et trois، deux paramètres تبدلو: ما كنستنتجو والو.")),
        question_semblable("5", "Associer chaque courbe (a), (b) et (c) à son expérience. Justifier.",
          phrase("Même palier 4,0 mmol (même x_max). Exp. 1 (20 °C ; 0,15) la plus lente : (c). Exp. 2 (40 °C ; 0,15) plus rapide que 1 : (a). Exp. 3 (40 °C ; 0,30) la plus rapide : (b), la plus raide au début."),
          ["même palier", "plus raide au début"], ["(b) ↔ 1"],
          corr([("5 : même palier 4,0 mmol ; (b) ↔ 3, (a) ↔ 2, (c) ↔ 1", "la courbe b")],
               "نفس le palier، quatre millimoles. l'expérience trois la plus rapide، هي la courbe b. l'expérience deux هي la courbe a. و l'expérience un la plus lente هي la courbe c.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
