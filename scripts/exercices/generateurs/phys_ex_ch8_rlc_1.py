# Exercice de physique, ch. 8 (oscillations libres d'un circuit RLC série), niveau facile n° 1 :
# la période propre T₀ = 2π√(LC) d'un circuit LC idéal, l'effet de C, la dimension de √(LC).
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture backend/data/curriculum/architecture/phys_ch8_circuit_RLC.md
#    (fréquences au national : « lire T puis trouver L ou C » 13 sessions, énergie 14, équation très fréquente) et
#    docs/parties_voix/phys_ch8_circuit_RLC.json ; fiche du cadre circuit_RLC (RLC4 : T₀ = 2π√(LC), √(LC) homogène à un temps ;
#    RLC5 : influence de L et de C, π² = 10).
#  - cours phys_ch8_circuit_RLC : lc_e8_T0 (identification), lc_p1_unites (dimension), lc_p3_influence (C × 4 → T₀ × 2).
#  - nationaux : 2017 R, 2021 N, 2022 N (« trouver l'expression de T₀ »), 2018 R (homogénéité d'une période) ;
#    ici seulement les gestes un à un (niveau facile).
#  - séries en ligne : recherche faite (talamidi, moutamadris, Naceiri, dreamjob : séries « oscillations libres RLC ») mais
#    les PDF ne sont pas joignables depuis cette session (hôtes hors réseau autorisé) : données habituelles L ~ 0,1 à 1 H,
#    C ~ µF, T₀ ~ ms, π² = 10. Nos données sont celles des simulations du cours (L = 0,1 H, C = 4 µF, E = 6 V).
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch8_rlc_1"
SIMD = "/media/simulations/physics/circuit-rlc-tableau/"


def montage(titre, avec_R=True, avec_G=False, bobine="(L, r)", legende=None):
    """K en 1 : le générateur E charge le condensateur ; K en 2 : le condensateur se décharge dans R et la bobine.
    i orienté vers l'armature A ; u_C (flèche vers A) en convention récepteur."""
    g = [dipole([0.8, 0.8], [0.8, 3.6], "G", "E", pos="o"),
         fil([0.8, 3.6], [2.9, 3.6]),
         inverseur([3.4, 2.8], [2.9, 3.6], [3.9, 3.6], t="K", pos_t=[3.95, 2.75]),
         dipole([3.4, 2.8], [3.4, 0.8], "C", "C", pos="e"),
         borne([3.4, 2.05], "A", "o"), borne([3.4, 0.8], "B", "s"),
         tension([2.1, 1.2], [2.1, 2.4], "u_C", pos="o"),
         fil([3.9, 3.6], [4.6, 3.6])]
    if avec_R:
        g += [dipole([4.6, 3.6], [6.6, 3.6], "R", "R"), fil([6.6, 3.6], [7.6, 3.6])]
    else:
        g += [fil([4.6, 3.6], [7.6, 3.6])]
    g += [dipole([7.6, 3.6], [7.6, 0.8], "L", bobine, pos="e")]
    if avec_G:
        g += [fil([7.6, 0.8], [6.6, 0.8]), dipole([6.6, 0.8], [4.6, 0.8], "R", "G", pos="s"), fil([4.6, 0.8], [0.8, 0.8])]
    else:
        g += [fil([7.6, 0.8], [0.8, 0.8])]
    g += [courant([4.1, 0.8], "d")]
    return schema(titre, 9.6, 4.6, *g, legende=legende)


# ---------------------------------------------------------------- données et calculs (π² = 10)
L, C, E = 0.1, 4e-6, 6
T0 = math.sqrt(40 * L * C)                # 4·10⁻³ s
T0p = math.sqrt(40 * L * 16e-6)           # 8·10⁻³ s
assert abs(T0 - 4e-3) < 1e-12 and abs(T0p - 8e-3) < 1e-12
# semblable : L = 0,25 H, C = 10 µF, C' = 40 µF
Lb, Cb = 0.25, 10e-6
T0b = math.sqrt(40 * Lb * Cb); T0bp = math.sqrt(40 * Lb * 40e-6)
assert abs(T0b - 1e-2) < 1e-12 and abs(T0bp - 2e-2) < 1e-12

DIM = ("u = L·di/dt donne [L] = [U]·[T]/[I] ; i = C·du_C/dt donne [C] = [I]·[T]/[U] ; donc [L]·[C] = [T]² et "
       "[√(LC)] = [T] : √(LC) a la dimension d'un temps (2π n'a pas d'unité), T₀ s'exprime en secondes.")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "circuit_RLC", "cours": "phys_ch8_circuit_RLC",
  "titre": "La période propre d'un circuit LC : la calculer, la prévoir", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer la période propre T₀ = 2π√(LC) (π² = 10)", "Prévoir l'effet de C sur T₀", "Montrer que √(LC) a la dimension d'un temps"],
  "enonce": {
    "intro": "On charge totalement un condensateur de capacité C sous la tension E (interrupteur K en position 1, figure 1). À t = 0, on bascule K en position 2 : le condensateur se décharge dans une bobine d'inductance L et de résistance négligeable (on ne monte pas de résistor : circuit LC idéal). La tension u_C oscille alors en régime périodique.",
    "intro_dit": "دابا نقراو l'énoncé. كنشارجيو un condensateur، la capacité ديالو C، تحت la tension E، وl'interrupteur K فla position un. فt égale zéro، كنبدلو K لla position deux: le condensateur كيتفرغ فla bobine، l'inductance ديالها L، وla résistance ديالها مهملة. ما كاينش résistor: هادا le circuit LC idéal. la tension u C كتمشي وتجي، فle régime périodique.",
    "figures": [montage("Figure 1 : le montage (sans résistor : circuit LC)", avec_R=False, bobine="L")],
    "donnees": ["E = 6 V", "L = 0,1 H", "C = 4 µF = 4·10⁻⁶ F", "On prend π² = 10."],
    "questions": [
      question("1", "Rappeler l'expression de la période propre T₀ du circuit LC, puis la calculer (en ms).",
        "السؤال un: عطي l'expression ديال la période propre T zéro ديال le circuit LC، ومن بعد حسبها بles millisecondes.",
        valeur("T₀", 4, "ms", "T₀ = 2π√(LC) = √(4π²·L·C) = √(40 × 0,1 × 4·10⁻⁶) = √(1,6·10⁻⁵) = 4·10⁻³ s = 4 ms"),
        ["T₀ = 2π√(LC)", "π² = 10", "10⁻⁶", "√", "ms"], ["T₀ = 2π·L·C", "T₀ = 2π√(L/C)", "C = 4 F"],
        [aide("T₀ ne dépend que des deux dipôles qui échangent l'énergie : la bobine (L) et le condensateur (C). Écris C en farads : 4 µF = 4·10⁻⁶ F.",
              "T zéro كتعتمد غير على les deux dipôles اللي كيتبادلو l'énergie: la bobine، يعني L، وle condensateur، يعني C. كتب C بle farad: quatre microfarads، يعني quatre fois dix puissance moins six farad."),
         aide("T₀ = 2π√(LC). Pour calculer sans calculatrice, mets tout au carré : T₀² = 4π²·L·C = 40·L·C, puis prends la racine.",
              "T zéro égale deux pi racine de L C. باش تحسب ساهل، طلع كلشي au carré: T zéro au carré égale quatre pi carré fois L fois C، يعني quarante fois L fois C. ومن بعد خود la racine.")],
        corr([("1 : T₀ = 2π√(LC)", "T zéro égale deux pi racine de L C"),
              ("A.N. : T₀² = 4π²·L·C = 40 × 0,1 × 4·10⁻⁶ = 1,6·10⁻⁵ s²", "un virgule six fois dix puissance moins cinq"),
              ("T₀ = 4·10⁻³ s = 4 ms", "T zéro égale quatre millisecondes")],
             "السؤال un. T zéro égale deux pi racine de L C. l'application numérique: T zéro au carré égale quarante، fois zéro virgule un، fois quatre fois dix puissance moins six، يعني un virgule six fois dix puissance moins cinq. la racine كتعطي quatre fois dix puissance moins trois seconde. إذن T zéro égale quatre millisecondes."),
        "ex_lc1_1", "fa_lc1_1"),
      question("2", "On remplace le condensateur par un autre de capacité C' = 4C = 16 µF, sans changer la bobine. Calculer la nouvelle période propre T₀' (en ms).",
        "السؤال deux: كنبدلو le condensateur بcondensateur آخر، la capacité ديالو C prime égale quatre fois C، يعني seize microfarads، وla bobine ما كتبدلش. حسب la nouvelle période propre T zéro prime بles millisecondes.",
        valeur("T₀'", 8, "ms", "T₀' = 2π√(L·4C) = 2·2π√(LC) = 2·T₀ = 2 × 4 = 8 ms"),
        ["T₀' = 2π√(LC')", "√4 = 2", "T₀ = 4 ms", "ms"], ["T₀' = 4·T₀ = 16 ms", "T₀' = T₀/2"],
        [aide("Dans la formule, C est sous la racine. Que devient √(L·C) quand C est multipliée par 4 ?",
              "فla formule، C كاينة تحت la racine. شنو كيوقع لracine de L C ملي C كتضرب par quatre؟"),
         aide("√(L·4C) = √4·√(LC) = 2·√(LC) : la période est multipliée par √4 = 2, pas par 4.",
              "racine de L fois quatre C، égale racine de quatre، fois racine de L C، يعني deux fois racine de L C. إذن la période كتضرب par racine de quatre، يعني deux، ماشي quatre.")],
        corr([("2 : T₀' = 2π√(L·C') = 2π√(L·4C)", "T zéro prime égale deux pi racine de L fois quatre C"),
              ("T₀' = √4 · 2π√(LC) = 2·T₀", "T zéro prime égale deux fois T zéro"),
              ("A.N. : T₀' = 2 × 4 = 8 ms", "T zéro prime égale huit millisecondes")],
             "السؤال deux. T zéro prime égale deux pi racine de L fois quatre C. la racine de quatre هي deux، إذن T zéro prime égale deux fois T zéro. يعني deux fois quatre، T zéro prime égale huit millisecondes. les oscillations ولاو أبطأ."),
        "ex_lc1_2", "fa_lc1_2"),
      question("3", "Montrer, par une analyse dimensionnelle, que la grandeur √(LC) a la dimension d'un temps.",
        "السؤال trois: بين، بl'analyse dimensionnelle، بلي racine de L C عندها la dimension ديال un temps.",
        phrase(DIM),
        ["u = L·di/dt", "i = C·du_C/dt", "[L]·[C] = [T]²", "[U]", "[I]", "[T]"], ["[L] = [U]·[I]/[T]", "[C] = [U]/[I]", "2π a une unité"],
        [aide("Cherche une relation qui contient L (la tension de la bobine) et une qui contient C (l'intensité du condensateur), puis écris la dimension de L et celle de C.",
              "قلب على relation فيها L، وهي la tension ديال la bobine، وrelation فيها C، وهي l'intensité ديال le condensateur. ومن بعد كتب la dimension ديال L وديال C."),
         aide("u = L·di/dt donne [L] = [U]·[T]/[I] ; i = C·du_C/dt donne [C] = [I]·[T]/[U]. Fais le produit [L]·[C].",
              "u égale L dé i sur dé t، إذن la dimension ديال L هي tension fois temps sur intensité. i égale C dé u C sur dé t، إذن la dimension ديال C هي intensité fois temps sur tension. ضرب بجوج.")],
        corr([("3 : u = L·di/dt ⇒ [L] = [U]·[T]/[I]", "la dimension ديال L هي tension fois temps، sur intensité"),
              ("i = C·du_C/dt ⇒ [C] = [I]·[T]/[U]", "la dimension ديال C هي intensité fois temps، sur tension"),
              ("[L]·[C] = [T]², donc [√(LC)] = [T] : √(LC) est un temps (2π est sans dimension).", "racine de L C هي un temps")],
             "السؤال trois. من u égale L dé i sur dé t، la dimension ديال L هي tension fois temps، sur intensité. ومن i égale C dé u C sur dé t، la dimension ديال C هي intensité fois temps، sur tension. ملي كنضربو، la tension كتمشي وl'intensité كتمشي، كيبقى temps au carré. إذن racine de L C هي un temps، et deux pi ما عندو حتى unité."),
        "ex_lc1_3", "fa_lc1_3"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_lc1_1", "Question 1 : T₀ = 2π√(LC)", "L = 0,1 H, C = 4 µF : T₀² = 40 × 0,1 × 4·10⁻⁶, T₀ = 4 ms.",
      SIMD + "solution.html?vue=cos", "La sinusoïde du circuit LC : T₀ se lit entre deux sommets et se calcule par 2π√(LC)",
      "شوف la courbe ديال u C فle circuit LC: كتمشي وتجي، وles sommets كلهم بنفس العلو. هنا L égale zéro virgule un henry، وC égale quatre microfarads، بحال التمرين ديالك. ملي عوضنا la solution فl'équation، لقينا deux pi sur T zéro au carré، égale un sur L C. إذن T zéro égale deux pi racine de L C. باش نحسبو، كنطلعو au carré: T zéro au carré égale quarante fois zéro virgule un fois quatre fois dix puissance moins six. يعني un virgule six fois dix puissance moins cinq. إذن T zéro égale quatre millisecondes، وهي نفس المدة اللي بين deux sommets فla courbe.",
      centre=[("T₀ = 2π√(LC)", "إذن T zéro égale deux pi racine de L C"),
              ("T₀² = 40 × 0,1 × 4·10⁻⁶ = 1,6·10⁻⁵ s²", "يعني un virgule six fois dix puissance moins cinq"),
              ("T₀ = 4·10⁻³ s = 4 ms", "إذن T zéro égale quatre millisecondes")],
      pointage=[{"mot": "شوف la courbe ديال u C", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "les sommets كلهم بنفس العلو", "repere": "courbe"},
                {"mot": "ملي عوضنا la solution", "commande": "play_until", "parametres": {"moment": "identification"}},
                {"mot": "deux pi sur T zéro au carré", "repere": "identification"},
                {"mot": "إذن T zéro égale deux pi racine de L C", "cible": "centre:0"},
                {"mot": "يعني un virgule six fois dix puissance moins cinq", "cible": "centre:1"},
                {"mot": "إذن T zéro égale quatre millisecondes", "cible": "centre:2"},
                {"mot": "نفس المدة اللي بين deux sommets", "repere": "resultat"}]),
    diapo_sim("ex_lc1_2", "Question 2 : C × 4 → T₀ × 2", "C' = 16 µF = 4C : T₀' = 2·T₀ = 8 ms.",
      SIMD + "periode.html?vue=influence_C", "La courbe de référence (C = 4 µF) et, en pointillés, C' = 16 µF : la période double",
      "شوف la courbe ديال المرجع: L égale zéro virgule un henry، وC égale quatre microfarads، وT zéro environ quatre millisecondes. دابا كنبدلو le condensateur: C prime égale seize microfarads، يعني quatre fois C. شوف la courbe بالنقط: كتمشي وتجي بشوية. بين deux sommets، كاينة environ huit millisecondes. علاش ماشي seize؟ حيت C كاينة تحت la racine: racine de quatre égale deux. إذن T zéro prime égale deux fois T zéro، يعني huit millisecondes.",
      centre=[("T₀' = 2π√(L·4C) = 2·T₀", "إذن T zéro prime égale deux fois T zéro"),
              ("T₀' = 2 × 4 = 8 ms", "يعني huit millisecondes")],
      pointage=[{"mot": "شوف la courbe ديال المرجع", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "T zéro environ quatre millisecondes", "repere": "T0"},
                {"mot": "دابا كنبدلو le condensateur", "commande": "play_until", "parametres": {"moment": "C_fois_4"}},
                {"mot": "شوف la courbe بالنقط", "repere": "courbe_C"},
                {"mot": "كاينة environ huit millisecondes", "repere": "T0_double"},
                {"mot": "إذن T zéro prime égale deux fois T zéro", "cible": "centre:0"},
                {"mot": "يعني huit millisecondes", "cible": "centre:1"}]),
    diapo_sim("ex_lc1_3", "Question 3 : √(LC) est un temps", "[L] = [U]·[T]/[I], [C] = [I]·[T]/[U] : [L]·[C] = [T]².",
      SIMD + "periode.html?vue=T0", "La lecture de T₀, son calcul, puis la dimension de L·C",
      "شوف la courbe: T zéro مقروءة بين deux sommets، environ quatre millisecondes. ومحسوبة par deux pi racine de L C. واش racine de L C فعلا un temps؟ كنشوفو les dimensions. فla bobine: u égale L dé i sur dé t. إذن la dimension ديال L هي tension fois temps، sur intensité. فle condensateur: i égale C dé u sur dé t. إذن la dimension ديال C هي intensité fois temps، sur tension. ملي كنضربو، la tension كتمشي وl'intensité كتمشي. كيبقى temps au carré. إذن racine de L C هي un temps، وT zéro كتقاس بla seconde.",
      centre=[("[L] = [U]·[T]/[I]", "la dimension ديال L هي tension fois temps"),
              ("[C] = [I]·[T]/[U]", "la dimension ديال C هي intensité fois temps"),
              ("[L]·[C] = [T]² ⇒ √(LC) est un temps", "كيبقى temps au carré")],
      pointage=[{"mot": "T zéro مقروءة بين deux sommets", "commande": "play_until", "parametres": {"moment": "lecture_T0"}},
                {"mot": "environ quatre millisecondes", "repere": "T0"},
                {"mot": "ومحسوبة par deux pi racine de L C", "commande": "play_until", "parametres": {"moment": "calcul_T0"}},
                {"mot": "كنشوفو les dimensions", "commande": "play_until", "parametres": {"moment": "unites"}},
                {"mot": "la dimension ديال L هي tension fois temps", "cible": "centre:0"},
                {"mot": "la dimension ديال C هي intensité fois temps", "cible": "centre:1"},
                {"mot": "كيبقى temps au carré", "cible": "centre:2"},
                {"mot": "إذن racine de L C هي un temps", "repere": "unites"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_lc1_1", "Plus facile : la formule de T₀", "نتمرنو بسؤال ساهل. اختار la bonne formule.",
      "Quelle est l'expression de la période propre d'un circuit LC ?",
      ["T₀ = 2π·L·C", "T₀ = 2π√(L/C)", "T₀ = 2π√(LC)"], 2, {
        "2": {"juste": rep("برافو! T zéro égale deux pi racine de L C، والضرب L fois C كاين تحت la racine.", "Juste : T₀ = 2π√(LC).")},
        "0": {"1": rep("قريب، L وC بجوج كاينين. ولكن واش L fois C وحدها un temps؟ فكر فla racine. عاود اختار.", "L·C n'est pas un temps (c'est un temps au carré) : il manque quelque chose. Réessaie."),
              "2": rep("الجواب هو T zéro égale deux pi racine de L C. L fois C هي temps au carré، إذن خاص la racine.", "Réponse : T₀ = 2π√(LC) ; L·C est un temps au carré, d'où la racine.")},
        "1": {"1": rep("لا. إلى كبرات C، le condensateur كيتشارجا ويتفرغ بشوية، إذن T zéro خاصها تكبر. واش L sur C كتكبر مع C؟ عاود اختار.", "Si C augmente, les oscillations ralentissent : T₀ doit augmenter avec C. Réessaie."),
              "2": rep("الجواب هو T zéro égale deux pi racine de L C. L وC بجوج كيطولو la période.", "Réponse : T₀ = 2π√(LC) (L et C allongent tous les deux la période).")}},
      "Quelle est l'expression de la période propre d'un circuit L C ?"),
    qcm_facile("fa_lc1_2", "Plus facile : C multipliée par 4", "سؤال ساهل: شنو كيوقع لT zéro ملي C كتضرب par quatre؟",
      "L ne change pas et C est multipliée par 4. La période propre T₀ est…",
      ["multipliée par 4", "multipliée par 2", "divisée par 2"], 1, {
        "1": {"juste": rep("برافو! C كاينة تحت la racine، وracine de quatre égale deux. إذن T zéro كتضرب par deux.", "Juste : T₀ est multipliée par √4 = 2.")},
        "0": {"1": rep("ما تقلقش. شوف la formule: C كاينة تحت la racine. شحال هي racine de quatre؟ عاود اختار.", "C est sous la racine dans T₀ = 2π√(LC). Que vaut √4 ? Réessaie."),
              "2": rep("الجواب: T zéro كتضرب par deux، حيت racine de quatre égale deux.", "Réponse : multipliée par 2, car √4 = 2.")},
        "2": {"1": rep("لا. إلى كبرات C، les oscillations كيوليو أبطأ، إذن T zéro كتكبر، ما كتصغرش. عاود اختار.", "Si C augmente, T₀ augmente : elle ne peut pas diminuer. Réessaie."),
              "2": rep("الجواب: T zéro كتضرب par deux. C كبرات، إذن la période كبرات، بracine de quatre.", "Réponse : multipliée par 2 (√4) ; T₀ augmente avec C.")}},
      "L ne change pas et C est multipliée par quatre. La période propre T zéro est ?"),
    vrai_faux_facile("fa_lc1_3", "Plus facile : vrai ou faux", "سؤال ساهل على les dimensions: قول واش صحيح ولا غالط.",
      "Analyse dimensionnelle de T₀ = 2π√(LC).",
      [("De u = L·di/dt, on tire [L] = [U]·[T]/[I].", True, "L = u/(di/dt) : tension × temps / intensité."),
       ("De i = C·du_C/dt, on tire [C] = [U]·[T]/[I].", False, "C = i/(du_C/dt) : [C] = [I]·[T]/[U] (intensité × temps / tension)."),
       ("[L]·[C] = [T]², donc √(LC) est un temps.", True, "Les tensions et les intensités se simplifient : il reste un temps au carré."),
       ("2π a pour unité la seconde.", False, "2π est un nombre sans dimension : toute l'unité de T₀ vient de √(LC).")]),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage (figure 1), avec E = 9 V, une bobine d'inductance L = 0,25 H (résistance négligeable) et un condensateur de capacité C = 10 µF. On prend π² = 10.",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale neuf volts، L égale zéro virgule vingt-cinq henry، وC égale dix microfarads. وكناخدو pi carré égale dix.",
      "figures": [],
      "donnees": ["E = 9 V", "L = 0,25 H", "C = 10 µF = 10⁻⁵ F", "π² = 10"],
      "questions": [
        question_semblable("1", "Rappeler l'expression de T₀, puis la calculer (en ms).",
          valeur("T₀", 10, "ms", "T₀ = 2π√(LC) = √(40 × 0,25 × 10⁻⁵) = √(10⁻⁴) = 10⁻² s = 10 ms"), ["T₀ = 2π√(LC)", "π² = 10", "ms"], ["T₀ = 2π·L·C"],
          corr([("1 : T₀ = 2π√(LC) ; T₀² = 40 × 0,25 × 10⁻⁵ = 10⁻⁴ s²", "T zéro au carré égale dix puissance moins quatre"), ("T₀ = 10⁻² s = 10 ms", "T zéro égale dix millisecondes")],
               "T zéro égale deux pi racine de L C. T zéro au carré égale quarante fois zéro virgule vingt-cinq fois dix puissance moins cinq، يعني T zéro au carré égale dix puissance moins quatre. إذن T zéro égale dix millisecondes.")),
        question_semblable("2", "On remplace C par C' = 4C = 40 µF. Calculer la nouvelle période propre T₀' (en ms).",
          valeur("T₀'", 20, "ms", "T₀' = 2π√(L·4C) = 2·T₀ = 2 × 10 = 20 ms"), ["√4 = 2", "ms"], ["T₀' = 4·T₀ = 40 ms"],
          corr([("2 : T₀' = 2π√(L·4C) = 2·T₀", "T zéro prime égale deux fois T zéro"), ("T₀' = 20 ms", "vingt millisecondes")],
               "C كاينة تحت la racine، إذن T zéro prime égale deux fois T zéro، يعني vingt millisecondes.")),
        question_semblable("3", "Montrer, par une analyse dimensionnelle, que √(LC) a la dimension d'un temps.",
          phrase(DIM), ["[L] = [U]·[T]/[I]", "[C] = [I]·[T]/[U]"], ["[C] = [U]/[I]"],
          corr([("3 : [L] = [U]·[T]/[I] et [C] = [I]·[T]/[U]", "la dimension ديال L وديال C"), ("[L]·[C] = [T]² : √(LC) est un temps.", "racine de L C هي un temps")],
               "la dimension ديال L وديال C: tension fois temps sur intensité، وintensité fois temps sur tension. الضرب كيعطي temps au carré، إذن racine de L C هي un temps.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
