# Exercice de physique, ch. 7 (dipôle RL), niveau moyen n° 5 : exploiter la courbe i(t) de l'établissement —
# r à partir de I_p, analyse dimensionnelle de τ, τ par la tangente, L, énergie de la bobine à t = τ.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RL.json : cas_types « permanent », « r », « tau »
#    (tangente ∩ asymptote), « L », « energie » (½·L·i² avec i lu à l'instant demandé) ; capacité RL6 (τ homogène à un
#    temps) ; erreurs_examen « énergie : I₀ au lieu de i(t) ; oubli du carré ou du ½ », « unités ms, mA non converties ».
#  - nationaux : 2016 R (2, 3, 6, 7, 8 : I_p, r, τ, L, énergie à τ/2), 2018 R (5, 6 : τ, L, énergie à t = τ),
#    2021 R (II-4, II-5 : r, L) : même enchaînement « lire puis déduire » ; nos données (E = 6 V, R = 20 Ω).
#  - cours phys_ch7_dipole_RL : rl_m4_I0, rl_s5_dimension (fig_dimension), rl_l1_tangente (courbe.html?vue=tangente),
#    rl_l3_r, rl_l7_energie.
#  - séries en ligne : recherche web (talamidi, moutamadris, alloschool, série P7 N. Naceiri) ; pages non ouvertes
#    (domaines bloqués dans le conteneur), seuls les intitulés comparés. Données réglées dans circuit-rl.html
#    (E = 6 V, R = 20 Ω, L = 0,18 H, r = 10 Ω) ; la méthode de la tangente est montrée sur courbe.html (valeurs du
#    cours, dites comme telles).
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch7_rl_5"
SIMD = "/media/simulations/physics/dipole-rl-tableau/"
SIM = SIMD + "circuit-rl.html?vue=etablissement&E=6&R_ohm=20&L_H=0.18"
FIG_DIM = SIMD + "figures.html?fig=fig_dimension"
TANG = SIMD + "courbe.html?vue=tangente"


def montage(titre):
    return schema(titre, 8, 4.8,
        dipole([1, 0.8], [1, 3.6], "G", "E", pos="o"),
        fil([1, 3.6], [1.6, 3.6]),
        dipole([1.6, 3.6], [3.4, 3.6], "K", "K"),
        dipole([3.4, 3.6], [6.0, 3.6], "R", "R", pos="s"),
        fil([6.0, 3.6], [7, 3.6]),
        dipole([7, 3.6], [7, 0.8], "L", "(L, r)", pos="o"),
        fil([7, 0.8], [1, 0.8]),
        courant([6.5, 3.6], "d"))


def courbe_i(Ip_mA, tau_ms, tmax, pas, titre):
    return figure_courbe(titre, axe("t", 0, tmax, "ms", list(range(0, tmax + 1, pas))),
        axe("i", 0, Ip_mA * 1.25, "mA", list(range(0, int(Ip_mA * 1.25) + 1, 50))),
        [{"f": "courbe", "expr": f"{Ip_mA}*(1-exp(-x/{tau_ms}))", "couleur": "vert", "texte": "i(t)", "texte_x": tmax * 0.7},
         {"f": "courbe", "expr": f"{Ip_mA}*x/{tau_ms}", "de": 0, "a": tau_ms * 1.12, "couleur": "faible", "trait": "pointille"},
         {"f": "texte", "at": [tau_ms * 0.35, Ip_mA * 0.75], "t": "(T)", "couleur": "faible"},
         {"f": "repere", "y": Ip_mA, "couleur": "faible"}],
        legende="i(t) après la fermeture de K à t = 0 ; (T) : tangente à la courbe en t = 0.")


E, R, r, L = 6, 20, 10, 0.18
IP = E / (R + r)                       # 0,2 A
TAU = L / (R + r)                      # 6 ms
I_TAU = 0.63 * IP                      # 0,126 A
EM = 0.5 * L * I_TAU ** 2              # 1,43·10⁻³ J
assert abs(IP - 0.2) < 1e-12 and abs(TAU - 6e-3) < 1e-12 and abs(EM - 1.42884e-3) < 1e-9
assert abs(0.5 * L * (IP * (1 - math.exp(-1))) ** 2 - 1.43e-3) / 1.43e-3 < 0.03
# semblable
E2, R2, r2, L2 = 12, 45, 15, 0.24
IP2, TAU2 = E2 / (R2 + r2), L2 / (R2 + r2)
EM2 = 0.5 * L2 * (0.63 * IP2) ** 2
assert abs(IP2 - 0.2) < 1e-12 and abs(TAU2 - 4e-3) < 1e-12 and abs(EM2 - 1.90512e-3) < 1e-9

ATT2 = ("u_b = L·di/dt ⇒ [L] = [U]·[T]/[I] ; u_R = R·i ⇒ [R] = [U]/[I]. Donc [L/(R + r)] = [L]/[R] = "
        "([U]·[T]/[I])·([I]/[U]) = [T] : τ est homogène à un temps (en s).")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RL", "cours": "phys_ch7_dipole_RL",
  "titre": "Lire la courbe i(t) : r, τ, L et l'énergie de la bobine", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Lire I_p et en déduire r", "Montrer que τ = L/(R + r) est homogène à un temps",
                  "Déterminer τ par la tangente à l'origine", "Calculer L = τ·(R + r)", "Calculer E_m = ½·L·i² à un instant donné"],
  "enonce": {
    "intro": "On réalise le montage de la figure 1 : générateur idéal de f.é.m. E, interrupteur K, conducteur ohmique de résistance R et bobine d'inductance L et de résistance r inconnues. À t = 0, on ferme K. Un système d'acquisition donne la courbe i(t) de la figure 2, avec (T) la tangente à la courbe à l'origine.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا un générateur E، l'interrupteur K، un conducteur ohmique R، و une bobine، L و r ديالها ما معروفينش. فt égale zéro، كنسدو K. و la figure deux فيها la courbe ديال i en fonction de t، و T هي la tangente ف l'origine.",
    "figures": [montage("Figure 1 : le montage"), courbe_i(200, 6, 36, 3, "Figure 2 : la courbe i(t)")],
    "donnees": ["E = 6 V", "R = 20 Ω", "u_b = L·di/dt + r·i", "On prend 1 − e⁻¹ ≈ 0,63"],
    "questions": [
      question("1", "Lire sur la figure 2 l'intensité I_p du courant en régime permanent, puis montrer que r = 10 Ω.",
        "السؤال un: قرا فla figure deux I p، le courant فle régime permanent، ومن بعد بين بلي r égale dix ohms.",
        valeur("r", 10, "Ω", "I_p = 200 mA = 0,2 A ; I_p = E/(R + r) ⇒ r = E/I_p − R = 6/0,2 − 20 = 10 Ω"),
        ["I_p = E/(R + r)", "r = E/I_p − R", "mA → A", "Ω"], ["r = E/I_p = 30 Ω", "I_p = 200 A"],
        [aide("I_p est la valeur de l'asymptote horizontale de la courbe : attention, l'axe est en mA.",
              "I p هي la valeur ديال l'asymptote الأفقية. رد البال: l'axe بle milliampère."),
         aide("En régime permanent I_p = E/(R + r), donc r = E/I_p − R, avec I_p en ampères.",
              "فle régime permanent، I p égale E sur R plus r. إذن r égale E sur I p moins R، و I p بl'ampère.")],
        corr([("1 : on lit I_p = 200 mA = 0,2 A", "I p égale deux cents milliampères"),
              ("I_p = E/(R + r) ⇒ r = E/I_p − R", "r égale E sur I p moins R"),
              ("A.N. : r = 6/0,2 − 20 = 30 − 20 = 10 Ω", "r égale dix ohms")],
             "السؤال un. كنقراو l'asymptote: I p égale deux cents milliampères، يعني zéro virgule deux ampère. I p égale E sur R plus r، إذن r égale E sur I p moins R. six sur zéro virgule deux، كتعطي trente، moins vingt. r égale dix ohms."),
        "ex_rl5_1", "fa_rl5_1"),
      question("2", "Montrer, par une analyse dimensionnelle, que τ = L/(R + r) est homogène à un temps.",
        "السؤال deux: بين بl'analyse dimensionnelle بلي tau égale L sur R plus r عندها la dimension ديال الوقت.",
        phrase(ATT2),
        ["[L] = [U]·[T]/[I]", "[R] = [U]/[I]", "[τ] = [T]"], ["[L] = [U]·[I]/[T]", "[R] = [U]·[I]"],
        [aide("Écris deux relations du cours : la tension d'une bobine idéale u = L·di/dt, et la loi d'Ohm u = R·i. Isole L et R.",
              "كتب deux relations ديال الدرس: u égale L dé i sur dé t، و la loi d'Ohm u égale R i. عزل L و R."),
         aide("[L] = [U]·[T]/[I] et [R] = [U]/[I] ; divise l'une par l'autre (R + r a la dimension de R).",
              "la dimension de L: U fois T sur I. la dimension de R: U sur I. قسم وحدة على الأخرى. R plus r عندها نفس la dimension ديال R.")],
        corr([("2 : u = L·di/dt ⇒ [L] = [U]·[T]/[I]", "la dimension de L"),
              ("u = R·i ⇒ [R] = [U]/[I] (et [R + r] = [R])", "la dimension de R"),
              ("[τ] = [L]/[R] = ([U]·[T]/[I])·([I]/[U]) = [T] : τ est un temps", "كيبقى غير T")],
             "السؤال deux. u égale L dé i sur dé t، إذن la dimension de L، c'est U fois T sur I. la loi d'Ohm u égale R i، إذن la dimension de R، c'est U sur I. نقسمو: U fois T sur I، fois I sur U. كيبقى غير T. إذن tau homogène à un temps، كتقاس بla seconde."),
        "ex_rl5_2", "fa_rl5_2"),
      question("3", "Déterminer graphiquement la constante de temps τ (en ms).",
        "السؤال trois: لقا بالمبيان la constante de temps tau، بla milliseconde.",
        valeur("τ", 6, "ms", "la tangente (T) coupe l'asymptote i = I_p à t = τ : τ = 6 ms"),
        ["tangente à l'origine", "asymptote i = I_p", "ms"], ["τ = 3 ms", "τ lu au pied de l'asymptote"],
        [aide("Repère sur la figure 2 le point où la tangente (T) rencontre l'asymptote horizontale i = I_p.",
              "قلب فla figure deux على النقطة فين la tangente T كتلاقى مع l'asymptote الأفقية i égale I p."),
         aide("L'abscisse de ce point est τ. Vérification : à t = τ, i = 0,63·I_p = 126 mA.",
              "l'abscisse ديال هاد النقطة هي tau. تأكد: ف t égale tau، i égale zéro virgule soixante-trois fois I p، يعني cent vingt-six milliampères.")],
        corr([("3 : la tangente (T) à l'origine coupe l'asymptote i = I_p à l'instant t = τ", "la tangente T كتقطع l'asymptote"),
              ("on lit τ = 6 ms", "tau égale six millisecondes"),
              ("vérification : i(τ) = 0,63 × 200 = 126 mA", "cent vingt-six milliampères")],
             "السؤال trois. la tangente T كتقطع l'asymptote i égale I p ف t égale tau. كنقراو tau égale six millisecondes. وكنتأكدو: i de tau égale zéro virgule soixante-trois fois deux cents، يعني cent vingt-six milliampères."),
        "ex_rl5_3", "fa_rl5_3"),
      question("4", "En déduire la valeur de l'inductance L de la bobine.",
        "السؤال quatre: استنتج la valeur ديال L، l'inductance ديال la bobine.",
        valeur("L", 0.18, "H", "L = τ·(R + r) = 6·10⁻³ × (20 + 10) = 0,18 H"),
        ["τ = L/(R + r)", "L = τ·(R + r)", "10⁻³", "H"], ["L = τ·R = 0,12 H", "L = 6 × 30 = 180 H"],
        [aide("Utilise τ = L/(R + r) : isole L. N'oublie pas la résistance r trouvée à la question 1.",
              "استعمل tau égale L sur R plus r، و عزل L. ما تنساش r ديال السؤال الأول."),
         aide("L = τ·(R + r), avec τ = 6 ms = 6·10⁻³ s et R + r = 30 Ω.",
              "L égale tau fois R plus r، مع tau égale six fois dix puissance moins trois seconde، و R plus r égale trente ohms.")],
        corr([("4 : τ = L/(R + r) ⇒ L = τ·(R + r)", "L égale tau fois R plus r"),
              ("A.N. : L = 6·10⁻³ × 30", "six fois dix puissance moins trois fois trente"),
              ("L = 0,18 H", "L égale zéro virgule dix-huit henry")],
             "السؤال quatre. tau égale L sur R plus r، إذن L égale tau fois R plus r. l'application numérique: six fois dix puissance moins trois fois trente. L égale zéro virgule dix-huit henry."),
        "ex_rl5_4", "fa_rl5_4"),
      question("5", "Calculer l'énergie magnétique E_m emmagasinée dans la bobine à l'instant t = τ.",
        "السؤال cinq: حسب l'énergie magnétique E m اللي مخزنة فla bobine ف t égale tau.",
        valeur("E_m", 1.43e-3, "J", "i(τ) = 0,63·I_p = 0,126 A ; E_m = ½·L·i² = ½ × 0,18 × 0,126² ≈ 1,43·10⁻³ J"),
        ["E_m = ½·L·i²", "i(τ) = 0,63·I_p", "J"], ["E_m = ½·L·I_p² = 3,6·10⁻³ J", "E_m = ½·L·i = 0,0113 J"],
        [aide("À t = τ, le courant n'a pas encore atteint I_p : quelle est sa valeur ? (lis-la ou calcule-la)",
              "ف t égale tau، le courant مازال ما وصلش ل I p. شحال كيساوي؟ قراه ولا حسبو."),
         aide("i(τ) = 0,63·I_p = 0,126 A, puis E_m = ½·L·i(τ)² (le courant au carré, en ampères).",
              "i de tau égale zéro virgule soixante-trois fois I p، يعني zéro virgule cent vingt-six ampère. من بعد E m égale un demi L i au carré.")],
        corr([("5 : à t = τ : i(τ) = 0,63·I_p = 0,63 × 0,2 = 0,126 A", "i de tau égale zéro virgule soixante-trois fois I p"),
              ("E_m = ½·L·i(τ)² = ½ × 0,18 × 0,126²", "E m égale un demi L i au carré"),
              ("E_m ≈ 1,43·10⁻³ J", "un virgule quarante-trois fois dix puissance moins trois joule")],
             "السؤال cinq. ف t égale tau، i de tau égale zéro virgule soixante-trois fois I p، يعني zéro virgule cent vingt-six ampère. E m égale un demi L i au carré: un demi fois zéro virgule dix-huit، fois zéro virgule cent vingt-six au carré. E m environ un virgule quarante-trois fois dix puissance moins trois joule."),
        "ex_rl5_5", "fa_rl5_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_rl5_1", "Question 1 : I_p puis r", "I_p = 200 mA = 0,2 A ; r = E/I_p − R = 6/0,2 − 20 = 10 Ω.",
      SIM, "Le montage réglé comme l'exercice : E = 6 V, R = 20 Ω, L = 0,18 H",
      "شوف le circuit: E égale six volts، و R égale vingt ohms. كنسدو K. u R كتطلع، وهي l'image ديال i. فle régime permanent، i égale I p، deux cents milliampères، يعني zéro virgule deux ampère. I p égale E sur R plus r. إذن R plus r égale E sur I p: six sur zéro virgule deux، trente ohms. و r égale trente moins vingt، يعني dix ohms. شوف la bobine: r égale dix ohms.",
      centre=[("I_p = E/(R + r) ⇒ r = E/I_p − R", "I p égale E sur R plus r"), ("r = 6/0,2 − 20 = 10 Ω", "يعني dix ohms")],
      pointage=[{"mot": "E égale six volts", "repere": "generateur"},
                {"mot": "R égale vingt ohms", "repere": "resistance"},
                {"mot": "كنسدو K", "commande": "play_until", "parametres": {"moment": "courbe_i"}},
                {"mot": "فle régime permanent", "commande": "play_until", "parametres": {"moment": "permanent"}},
                {"mot": "deux cents milliampères", "repere": "regime_permanent"},
                {"mot": "I p égale E sur R plus r", "cible": "centre:0"},
                {"mot": "يعني dix ohms", "cible": "centre:1"},
                {"mot": "شوف la bobine", "repere": "bobine"}]),
    diapo_sim("ex_rl5_2", "Question 2 : τ est un temps", "[L] = [U]·[T]/[I] ; [R] = [U]/[I] ; [L]/[R] = [T].",
      FIG_DIM, "Trois lignes : la dimension de L, celle de R, puis le quotient",
      "الأول L. u b égale L dé i sur dé t، donc L égale u fois dé t sur dé i. la dimension de L، c'est U fois T sur I. التاني R. la loi d'Ohm: u égale R i، donc la dimension de R، c'est U sur I. و R plus r عندها نفس la dimension. دابا نقسمو: U fois T sur I، fois I sur U. U كتمشي مع U، و I مع I. كيبقى غير T. إذن tau homogène à un temps، كتقاس بla seconde.",
      centre=[("[L] = [U]·[T]/[I] ; [R] = [U]/[I]", "la dimension de R، c'est U sur I"), ("[τ] = [L]/[R] = [T]", "كيبقى غير T")],
      pointage=[{"mot": "الأول L.", "commande": "play_until", "parametres": {"moment": "L"}},
                {"mot": "التاني R.", "commande": "play_until", "parametres": {"moment": "R"}},
                {"mot": "la dimension de R، c'est U sur I", "cible": "centre:0"},
                {"mot": "دابا نقسمو", "commande": "play_until", "parametres": {"moment": "quotient"}},
                {"mot": "كيبقى غير T", "cible": "centre:1"}]),
    diapo_sim("ex_rl5_3", "Question 3 : τ par la tangente", "La tangente à l'origine coupe l'asymptote à t = τ ; ici τ = 6 ms.",
      TANG, "La méthode sur l'exemple du cours (100 mA, 2 ms), puis sur la figure 2",
      "نشوفو الطريقة على المثال ديال الدرس. l'axe des temps بla milliseconde، و l'axe ديال i بle milliampère. هنا l'asymptote: I zéro égale cent milliampères. كنرسمو la tangente à l'origine: كتقطع l'asymptote ف t égale tau. كنهبطو لl'axe des temps: tau égale deux millisecondes فهاد المثال. دابا فla figure deux ديال التمرين، نفس الخطوات: l'asymptote فيها deux cents milliampères، و la tangente T كتقطعها ف six millisecondes. إذن tau égale six millisecondes.",
      centre=[("(T) ∩ asymptote : t = τ", "كتقطع l'asymptote ف t égale tau"), ("figure 2 : τ = 6 ms", "إذن tau égale six millisecondes")],
      pointage=[{"mot": "l'axe des temps بla milliseconde", "repere": "axe_t"},
                {"mot": "l'axe ديال i بle milliampère", "repere": "axe_i"},
                {"mot": "هنا l'asymptote", "commande": "play_until", "parametres": {"moment": "asymptote"}},
                {"mot": "كنرسمو la tangente à l'origine", "commande": "play_until", "parametres": {"moment": "tangente"}},
                {"mot": "كتقطع l'asymptote ف t égale tau", "cible": "centre:0"},
                {"mot": "tau égale deux millisecondes فهاد المثال", "repere": "tau"},
                {"mot": "إذن tau égale six millisecondes", "cible": "centre:1"}]),
    diapo_sim("ex_rl5_4", "Question 4 : L = τ·(R + r)", "L = τ·(R + r) = 6·10⁻³ × 30 = 0,18 H.",
      SIM, "La bobine de l'exercice : L = 0,18 H, r = 10 Ω",
      "tau égale L sur R plus r. إذن L égale tau fois R plus r. tau égale six millisecondes، يعني six fois dix puissance moins trois seconde. و R plus r: vingt plus dix، يعني trente ohms. L égale six fois dix puissance moins trois fois trente، كتعطي zéro virgule dix-huit henry. شوف la bobine فla simulation: L égale zéro virgule dix-huit henry.",
      centre=[("L = τ·(R + r)", "إذن L égale tau fois R plus r"), ("L = 6·10⁻³ × 30 = 0,18 H", "كتعطي zéro virgule dix-huit henry")],
      pointage=[{"mot": "إذن L égale tau fois R plus r", "cible": "centre:0"},
                {"mot": "vingt plus dix", "repere": "resistance"},
                {"mot": "كتعطي zéro virgule dix-huit henry", "cible": "centre:1"},
                {"mot": "شوف la bobine فla simulation", "repere": "bobine"}]),
    diapo_sim("ex_rl5_5", "Question 5 : l'énergie à t = τ", "i(τ) = 0,63 × 0,2 = 0,126 A ; E_m = ½ × 0,18 × 0,126² ≈ 1,43·10⁻³ J.",
      SIM, "À t = τ, le courant n'est qu'à 63 % de I_p",
      "شوف la courbe كتطلع. ف t égale tau، le courant مازال ما وصلش ل I p: وصل غير ل soixante-trois pour cent. i de tau égale zéro virgule soixante-trois fois zéro virgule deux، يعني zéro virgule cent vingt-six ampère. l'énergie ديال la bobine: E m égale un demi L i au carré. un demi fois zéro virgule dix-huit، fois zéro virgule cent vingt-six au carré. E m environ un virgule quarante-trois fois dix puissance moins trois joule. رد البال: ماشي I p، هي i de tau.",
      centre=[("i(τ) = 0,63·I_p = 0,126 A", "يعني zéro virgule cent vingt-six ampère"), ("E_m = ½·L·i² ≈ 1,43·10⁻³ J", "E m environ un virgule quarante-trois")],
      pointage=[{"mot": "شوف la courbe كتطلع", "commande": "play_until", "parametres": {"moment": "courbe_i"}},
                {"mot": "وصل غير ل soixante-trois pour cent", "repere": "regime_transitoire"},
                {"mot": "يعني zéro virgule cent vingt-six ampère", "cible": "centre:0"},
                {"mot": "un demi fois zéro virgule dix-huit", "repere": "bobine"},
                {"mot": "E m environ un virgule quarante-trois", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_rl5_1", "Plus facile : trouver r", "سؤال ساهل باش نلقاو r.",
      "E = 6 V, R = 20 Ω, on lit I_p = 200 mA. La résistance r de la bobine vaut…",
      ["30 Ω", "10 Ω", "20 Ω"], 1, {
        "1": {"juste": rep("برافو! six sur zéro virgule deux، trente، moins vingt، كتعطي dix ohms.", "Juste : r = 6/0,2 − 20 = 10 Ω.")},
        "0": {"1": rep("trente ohms هي R plus r. شحال بقا ل la bobine؟ عاود.", "30 Ω, c'est R + r. Réessaie."),
              "2": rep("الجواب هو dix ohms: E sur I p moins R.", "Réponse : r = E/I_p − R = 30 − 20 = 10 Ω.")},
        "2": {"1": rep("vingt ohms هي R ديال le conducteur ohmique. حنا باغين la résistance ديال la bobine. عاود.", "20 Ω, c'est R. On cherche r. Réessaie."),
              "2": rep("الجواب هو dix ohms: R plus r égale trente، و R égale vingt.", "Réponse : r = 10 Ω.")}},
      "E égale six volts، R égale vingt ohms، I p égale deux cents milliampères. r vaut ?"),
    association_facile("fa_rl5_2", "Plus facile : les dimensions", "سؤال ساهل: ربط كل grandeur ب la dimension ديالها.",
      "Analyse dimensionnelle : [U] tension, [I] intensité, [T] temps.",
      "Associe chaque grandeur à sa dimension.",
      [("1", "[L]"), ("2", "[R]"), ("3", "[L/R]")],
      [("a", "[U]·[T]/[I]"), ("b", "[U]/[I]"), ("c", "[T]")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Juste : u = L·di/dt donne L = u·dt/di.", "صحيح: u égale L dé i sur dé t، إذن L égale u fois dé t sur dé i."),
       "1-b": (False, "[U]/[I], c'est une résistance (loi d'Ohm). Pour L, pense à u = L·di/dt.", "U sur I هي la dimension ديال résistance. ل L، فكر ف u égale L dé i sur dé t."),
       "1-c": (False, "[T] est la dimension de τ = L/R, pas de L seule.", "T هي la dimension ديال tau، ماشي ديال L بوحدها."),
       "2-a": (False, "Ce n'est pas la loi d'Ohm : u = R·i donne R = u/i.", "هادي ماشي la loi d'Ohm. u égale R i، إذن R égale u sur i."),
       "2-b": (True, "Juste : loi d'Ohm u = R·i, donc [R] = [U]/[I].", "صحيح: la loi d'Ohm، R égale u sur i."),
       "2-c": (False, "Une résistance n'est pas un temps : pense à u = R·i.", "la résistance ماشي وقت. فكر ف u égale R i."),
       "3-a": (False, "C'est [L] seule ; divise encore par [R].", "هادي غير L. قسم على la dimension ديال R."),
       "3-b": (False, "C'est [R] ; on cherche le quotient [L]/[R].", "هادي ديال R. حنا باغين L sur R."),
       "3-c": (True, "Juste : [L]/[R] = [T], τ est un temps.", "صحيح: L sur R كتعطي T: tau وقت.")},
      "(1 ; a) (2 ; b) (3 ; c) : [τ] = [L]/[R] = [T].",
      "الجواب: un مع a، deux مع b، trois مع c. إذن tau homogène à un temps."),
    qcm_facile("fa_rl5_3", "Plus facile : la tangente à l'origine", "سؤال ساهل على la tangente.",
      "Établissement du courant : la tangente à l'origine coupe l'asymptote i = I_p à l'instant…",
      ["t = τ", "t = 5τ", "t = 0,63 s"], 0, {
        "0": {"juste": rep("برافو! la tangente à l'origine كتقطع l'asymptote ف t égale tau.", "Juste : en t = τ.")},
        "1": {"1": rep("cinq tau هي فين كيبدا le régime permanent. la tangente كتقطع قبل. عاود.", "5τ marque le régime permanent. Réessaie."),
              "2": rep("الجواب هو t égale tau. cinq tau هي la fin ديال le régime transitoire.", "Réponse : t = τ.")},
        "2": {"1": rep("zéro virgule soixante-trois هي نسبة ديال I p، ماشي وقت. عاود.", "0,63 est une fraction de I_p, pas un temps. Réessaie."),
              "2": rep("الجواب هو t égale tau. و ف tau، i égale zéro virgule soixante-trois fois I p.", "Réponse : t = τ ; à τ, i = 0,63·I_p.")}},
      "La tangente à l'origine coupe l'asymptote à quel instant ?"),
    qcm_facile("fa_rl5_4", "Plus facile : calculer L", "سؤال ساهل باش نحسبو L.",
      "τ = 6 ms et R + r = 30 Ω. L vaut…",
      ["0,18 H", "180 H", "0,12 H"], 0, {
        "0": {"juste": rep("برافو! six fois dix puissance moins trois fois trente، كتعطي zéro virgule dix-huit henry.", "Juste : L = 6·10⁻³ × 30 = 0,18 H.")},
        "1": {"1": rep("نسيتي تحول les millisecondes ل secondes. عاود.", "Tu n'as pas converti les ms en s. Réessaie."),
              "2": rep("الجواب هو zéro virgule dix-huit henry: tau بla seconde، six fois dix puissance moins trois.", "Réponse : 0,18 H (τ = 6·10⁻³ s).")},
        "2": {"1": rep("ضربتي غير ف R. ولكن tau فيها R plus r. عاود.", "Tu as multiplié par R seulement ; il faut R + r. Réessaie."),
              "2": rep("الجواب هو zéro virgule dix-huit henry: L égale tau fois R plus r.", "Réponse : L = τ·(R + r) = 0,18 H.")}},
      "tau égale six millisecondes، R plus r égale trente ohms. L vaut ?"),
    qcm_facile("fa_rl5_5", "Plus facile : le courant à t = τ", "سؤال ساهل قبل ما نحسبو l'énergie.",
      "Pour calculer E_m à t = τ (établissement), on prend i(τ) =…",
      ["I_p", "0,63·I_p", "0,37·I_p"], 1, {
        "1": {"juste": rep("برافو! ف tau، i égale zéro virgule soixante-trois fois I p، ومن بعد E m égale un demi L i au carré.", "Juste : i(τ) = 0,63·I_p, puis E_m = ½·L·i².")},
        "0": {"1": rep("I p هي la valeur النهائية. واش ف tau le courant وصل ليها؟ عاود.", "I_p est la valeur finale ; est-elle atteinte à τ ? Réessaie."),
              "2": rep("الجواب هو zéro virgule soixante-trois fois I p. I p كتوصل غير à cinq tau.", "Réponse : 0,63·I_p ; I_p n'est atteinte que vers 5τ.")},
        "2": {"1": rep("zéro virgule trente-sept هي ديال courbe كتنزل. هنا i كتطلع. عاود.", "0,37 sert pour une courbe qui descend. Ici i monte. Réessaie."),
              "2": rep("الجواب هو zéro virgule soixante-trois fois I p: فl'établissement، i كتطلع.", "Réponse : 0,63·I_p (établissement).")}},
      "Pour calculer E m à t égale tau، on prend i de tau égale ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage (figure 1) avec E = 12 V et R = 45 Ω ; la bobine (L, r) est inconnue. À t = 0, on ferme K ; la figure 2 donne i(t) et sa tangente (T) à l'origine.",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale douze volts، و R égale quarante-cinq ohms. فt égale zéro، كنسدو K.",
      "figures": [courbe_i(200, 4, 24, 2, "Figure 2 : la courbe i(t)")],
      "donnees": ["E = 12 V", "R = 45 Ω", "On prend 1 − e⁻¹ ≈ 0,63"],
      "questions": [
        question_semblable("1", "Lire sur la figure 2 l'intensité I_p du courant en régime permanent, puis montrer que r = 15 Ω.",
          valeur("r", 15, "Ω", "I_p = 0,2 A ; r = E/I_p − R = 12/0,2 − 45 = 15 Ω"), ["r = E/I_p − R", "Ω"], ["r = E/I_p"],
          corr([("1 : I_p = 200 mA = 0,2 A ; r = E/I_p − R = 60 − 45", "r égale E sur I p moins R"), ("r = 15 Ω", "quinze ohms")],
               "I p égale zéro virgule deux ampère. r égale E sur I p moins R، يعني soixante moins quarante-cinq، كتعطي quinze ohms.")),
        question_semblable("2", "Montrer, par une analyse dimensionnelle, que τ = L/(R + r) est homogène à un temps.",
          phrase(ATT2), ["[L] = [U]·[T]/[I]", "[R] = [U]/[I]"], ["[L] = [U]·[I]/[T]"],
          corr([("2 : [L] = [U]·[T]/[I] ; [R] = [U]/[I]", "la dimension de L"), ("[τ] = [L]/[R] = [T]", "كيبقى غير T")],
               "la dimension de L، c'est U fois T sur I. la dimension de R، c'est U sur I. نقسمو: كيبقى غير T.")),
        question_semblable("3", "Déterminer graphiquement la constante de temps τ (en ms).",
          valeur("τ", 4, "ms", "(T) coupe l'asymptote à t = τ : τ = 4 ms"), ["tangente à l'origine", "ms"], ["τ = 2 ms"],
          corr([("3 : (T) coupe l'asymptote i = I_p en t = τ", "la tangente T كتقطع l'asymptote"), ("τ = 4 ms", "quatre millisecondes")],
               "la tangente T كتقطع l'asymptote ف tau: tau égale quatre millisecondes.")),
        question_semblable("4", "En déduire la valeur de l'inductance L de la bobine.",
          valeur("L", 0.24, "H", "L = τ·(R + r) = 4·10⁻³ × 60 = 0,24 H"), ["L = τ·(R + r)", "H"], ["L = τ·R"],
          corr([("4 : L = τ·(R + r) = 4·10⁻³ × 60", "L égale tau fois R plus r"), ("L = 0,24 H", "zéro virgule vingt-quatre henry")],
               "L égale tau fois R plus r، يعني quatre fois dix puissance moins trois fois soixante، كتعطي zéro virgule vingt-quatre henry.")),
        question_semblable("5", "Calculer l'énergie magnétique E_m emmagasinée dans la bobine à l'instant t = τ.",
          valeur("E_m", 1.91e-3, "J", "i(τ) = 0,63 × 0,2 = 0,126 A ; E_m = ½ × 0,24 × 0,126² ≈ 1,91·10⁻³ J"), ["E_m = ½·L·i²", "J"], ["E_m = ½·L·I_p²"],
          corr([("5 : i(τ) = 0,63·I_p = 0,126 A", "i de tau égale zéro virgule cent vingt-six ampère"), ("E_m = ½ × 0,24 × 0,126² ≈ 1,91·10⁻³ J", "un virgule quatre-vingt-onze fois dix puissance moins trois joule")],
               "i de tau égale zéro virgule cent vingt-six ampère. E m égale un demi fois zéro virgule vingt-quatre fois zéro virgule cent vingt-six au carré، يعني un virgule quatre-vingt-onze fois dix puissance moins trois joule.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
