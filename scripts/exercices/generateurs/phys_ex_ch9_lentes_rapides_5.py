# Exercice de chimie (physique-chimie), ch. 9 « Transformations lentes et transformations rapides », niveau moyen n° 5 :
# l'ion permanganate et l'acide oxalique — demi-équation, équation, tableau d'avancement, x_max, CO₂ formé, température.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture phys_ch9_transformations_lentes_rapides.md,
#    sources_chimie_ch9_ch11.md (Mahajar-Tabit et Sbiro : KMnO₄ + acide oxalique à 20 °C et à 40 °C pour la température ;
#    exercice type « couples et équation ; tableau d'avancement et x_max »), docs/parties_voix/phys_ch9_…json ;
#  - le cours phys_ch9 (tl_x4, tl_x5 MnO₄⁻/Mn²⁺, tl_x9_oxalique, tl_r1_bechers, tl_rp5, tl_f2_bains) ;
#  - nationaux : équations d'oxydoréduction avec multiplication des demi-équations (piles 2016 R, 2018 R, 2023 R) ;
#    facteurs cinétiques 2018 N, 2024 N ; état final inchangé par la température (2025 N) ;
#  - séries en ligne : recherche faite (moutamadris « demi-équations en milieu acide », talamidi, dreamjob) ; PDF non ouverts
#    (hôtes hors du réseau autorisé de la session).
#  Durées = celles de bechers.html (acide oxalique ≈ 7 min à 20 °C) ; à 40 °C, environ trois fois plus tôt (facteurs.html).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch9_lentes_rapides_5"
SIM = "/media/simulations/chimie/transformations-lentes-rapides-tableau/"

EQ = "2MnO₄⁻(aq) + 5H₂C₂O₄(aq) + 6H⁺(aq) → 2Mn²⁺(aq) + 10CO₂(aq) + 8H₂O(l)"
DEMI_MN = "MnO₄⁻(aq) + 8H⁺(aq) + 5e⁻ ⇌ Mn²⁺(aq) + 4H₂O(l)"
DEMI_OX = "2CO₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ H₂C₂O₄(aq)"


def r(v):
    return round(v, 9)


# énoncé (quantités en mmol)
nMn, nOx = r(1.0e-2 * 0.020 * 1e3), r(5.0e-2 * 0.020 * 1e3)     # 0,20 et 1,0 mmol
xMn, xOx = r(nMn / 2), r(nOx / 5)                                  # 0,10 et 0,20
XM = min(xMn, xOx)
nCO2 = r(10 * XM)
assert (nMn, nOx, xMn, xOx, XM, nCO2) == (0.2, 1.0, 0.1, 0.2, 0.1, 1.0)
# vérification de l'équation : éléments et charges
assert 2 * 4 + 5 * 4 == 10 * 2 + 8 and 5 * 2 + 6 == 8 * 2 and -2 + 6 == 4 == 2 * 2
# semblable
nMnb, nOxb = r(2.0e-2 * 0.010 * 1e3), r(4.0e-2 * 0.010 * 1e3)   # 0,20 et 0,40
xMnb, xOxb = r(nMnb / 2), r(nOxb / 5)                              # 0,10 et 0,08
XMb = min(xMnb, xOxb)
nCO2b = r(10 * XMb)
assert (nMnb, nOxb, xMnb, xOxb, XMb, nCO2b) == (0.2, 0.4, 0.1, 0.08, 0.08, 0.8)


def montage(titre, legende):
    """Bécher de permanganate acidifié et burette d'acide oxalique, au-dessus."""
    return schema(titre, 12, 6.4,
        fil([3, 3.4], [3, 0.6], [9, 0.6], [9, 3.4]),
        [{"f": "ligne", "pts": [[3, 2.6], [9, 2.6]], "couleur": "violet", "trait": "pointille"}],
        [{"f": "rect", "de": [5.7, 4.0], "a": [6.3, 6.2]}],
        fil([6.0, 4.0], [6.0, 3.5]),
        texte([6.0, 1.8], "MnO₄⁻(aq) + H⁺(aq)", couleur="violet"),
        texte([6.0, 1.1], "(violet)", couleur="violet"),
        texte([6.6, 5.4], "H₂C₂O₄(aq)", ancre="gauche"),
        texte([9.3, 1.6], "V₁ = 20 mL", ancre="gauche"),
        texte([6.6, 4.6], "V₂ = 20 mL", ancre="gauche"),
        legende=legende)


EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "transformations_lentes_rapides", "cours": "phys_ch9_transformations_lentes_rapides",
  "titre": "Permanganate et acide oxalique : équation, avancement et température", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Écrire une demi-équation en milieu acide", "Établir une équation en multipliant les demi-équations",
                  "Déterminer x_max, le réactif limitant et une quantité de produit", "Prévoir l'effet de la température sur la durée et l'état final"],
  "enonce": {
    "intro": "Dans un bécher, on verse V₁ = 20 mL d'une solution de permanganate de potassium, de concentration C₁ = 1,0·10⁻² mol/L en ions MnO₄⁻(aq), acidifiée par de l'acide sulfurique (ions H⁺(aq) en excès). À la date t = 0, on ajoute V₂ = 20 mL d'une solution d'acide oxalique H₂C₂O₄(aq) de concentration C₂ = 5,0·10⁻² mol/L (figure 1). À 20 °C, la couleur violette s'affaiblit peu à peu et le mélange devient incolore au bout d'environ 7 min.",
    "intro_dit": "نقراو l'énoncé. ف le bécher، V un égale vingt millilitres ديال la solution de permanganate de potassium، la concentration ديالها C un égale un fois dix puissance moins deux mole par litre، فوسط حمضي. فt égale zéro، كنزيدو V deux égale vingt millilitres ديال l'acide oxalique، و C deux égale cinq fois dix puissance moins deux mole par litre. à vingt degrés Celsius، اللون البنفسجي كيضعاف بشوية بشوية، و le mélange كيولي بلا لون من بعد environ sept minutes.",
    "figures": [montage("Figure 1 : le mélange", "Les ions Mn²⁺(aq) formés sont pratiquement incolores.")],
    "donnees": ["V₁ = 20 mL ; C₁ = [MnO₄⁻] = 1,0·10⁻² mol/L", "V₂ = 20 mL ; C₂ = [H₂C₂O₄] = 5,0·10⁻² mol/L",
                "Couples : MnO₄⁻(aq)/Mn²⁺(aq) et CO₂(aq)/H₂C₂O₄(aq)", "Demi-équation : " + DEMI_MN],
    "questions": [
      question("1", "Écrire la demi-équation électronique du couple CO₂(aq)/H₂C₂O₄(aq) en milieu acide.",
        "السؤال un: كتب la demi-équation électronique ديال le couple dioxyde de carbone sur acide oxalique، en milieu acide.",
        phrase(DEMI_OX),
        ["2CO₂(aq)", "2H⁺(aq)", "2e⁻", "⇌", "H₂C₂O₄(aq)"], ["CO₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ H₂C₂O₄(aq)", "H₂C₂O₄(aq) + 2e⁻ ⇌ 2CO₂(aq)"],
        [aide("L'oxydant CO₂ à gauche, le réducteur H₂C₂O₄ à droite. Les quatre gestes : atomes de carbone, oxygènes, hydrogènes, charges.",
              "l'oxydant، le dioxyde de carbone، على اليسار، و le réducteur، l'acide oxalique، على اليمين. les quatre gestes: le carbone، les oxygènes، les hydrogènes، و les charges."),
         aide("2 atomes C à droite, donc 2CO₂ ; les O sont 4 et 4 ; 2 H à droite, donc 2H⁺ à gauche ; charges +2 et 0, donc 2e⁻ à gauche.",
              "deux carbone على اليمين، donc deux dioxyde de carbone. les oxygènes: quatre et quatre. deux hydrogènes على اليمين، donc deux H plus على اليسار. les charges: plus deux et zéro، donc deux électrons على اليسار.")],
        corr([("1 : " + DEMI_OX, "deux dioxyde de carbone plus deux H plus plus deux électrons"),
              ("Vérification : C 2 = 2 ; O 4 = 4 ; H 2 = 2 ; charges 0 = 0.", "les charges: zéro et zéro")],
             "السؤال un. deux dioxyde de carbone plus deux H plus plus deux électrons، donne acide oxalique. نتأكدو: le carbone deux et deux، les oxygènes quatre et quatre، les hydrogènes deux et deux، و les charges: zéro et zéro."),
        "ex_tl5_1", "fa_tl5_1"),
      question("2", "Montrer que l'équation de la réaction s'écrit : " + EQ + ".",
        "السؤال deux: بين بلي l'équation هي: deux ions permanganate plus cinq acide oxalique، plus six H plus، donne deux ions manganèse deux، plus dix dioxyde de carbone، plus huit molécules d'eau.",
        phrase("Réduction : MnO₄⁻(aq) + 8H⁺(aq) + 5e⁻ → Mn²⁺(aq) + 4H₂O(l), multipliée par 2. Oxydation : H₂C₂O₄(aq) → 2CO₂(aq) + 2H⁺(aq) + 2e⁻, multipliée par 5. 10 électrons de chaque côté ; on additionne, puis on simplifie 16H⁺ − 10H⁺ = 6H⁺ : " + EQ + ". Charges : −2 + 6 = +4 à gauche, 2 × (+2) = +4 à droite."),
        ["× 2", "× 5", "10 e⁻", "16H⁺ − 10H⁺", "simplifier"], ["MnO₄⁻(aq) + H₂C₂O₄(aq) + … sans multiplier", "16H⁺(aq) à gauche et 10H⁺(aq) à droite, sans simplifier"],
        [aide("L'ion permanganate capte 5 électrons, l'acide oxalique en cède 2. Pour que les électrons cédés égalent les électrons captés, par quoi multiplier chaque demi-équation ?",
              "l'ion permanganate capte cinq électrons، و l'acide oxalique cède deux électrons. باش يكونو les électrons اللي كيتعطاو قد les électrons اللي كيتشدو، fois combien كل demi-équation؟"),
         aide("Multiplie la réduction par 2 et l'oxydation par 5 (10 e⁻). Additionne, puis simplifie les H⁺ présents des deux côtés.",
              "ضرب la réduction fois deux، و l'oxydation fois cinq: dix électrons من كل جهة. جمع، ومن بعد بسط les H plus اللي كاينين من الجهتين.")],
        corr([("2 : (MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O) × 2", "fois deux"),
              ("(H₂C₂O₄ → 2CO₂ + 2H⁺ + 2e⁻) × 5", "fois cinq"),
              ("Somme, puis 16H⁺ − 10H⁺ = 6H⁺ : " + EQ, "seize moins dix، égale six H plus"),
              ("Charges : +4 = +4", "plus quatre")],
             "السؤال deux. la réduction ديال l'ion permanganate avec cinq électrons: كنضربوها fois deux. l'oxydation ديال l'acide oxalique avec deux électrons: كنضربوها fois cinq. دابا، dix électrons من كل جهة. كنجمعو، ومن بعد كنبسطو les H plus: seize moins dix، égale six H plus على اليسار. le résultat هو l'équation المطلوبة. les charges: moins deux plus six، égale plus quatre، et plus quatre على اليمين."),
        "ex_tl5_2", "fa_tl5_2"),
      question("3", "Calculer, en mmol, les quantités de matière initiales n₀(MnO₄⁻) et n₀(H₂C₂O₄).",
        "السؤال trois: حسب ب millimole les quantités initiales ديال les ions permanganate و ديال l'acide oxalique.",
        valeur("n₀(H₂C₂O₄)", 1.0, "mmol", "n₀(MnO₄⁻) = C₁·V₁ = 1,0·10⁻² × 0,020 = 0,20 mmol ; n₀(H₂C₂O₄) = C₂·V₂ = 5,0·10⁻² × 0,020 = 1,0 mmol"),
        ["n = C·V", "0,020 L", "1 mmol = 10⁻³ mol"], ["n = C·V avec V = 20", "n = C·(V₁ + V₂)"],
        [aide("Chaque réactif vient de sa solution : C₁ avec V₁, C₂ avec V₂. Écris 20 mL en litres.",
              "كل réactif جا من la solution ديالو: C un مع V un، و C deux مع V deux. convertis vingt millilitres بالlitre."),
         aide("n = C·V avec V = 0,020 L, puis 10⁻³ mol = 1 mmol.",
              "n égale C fois V، و V égale zéro virgule zéro deux litre. ومن بعد، dix puissance moins trois mole égale un millimole.")],
        corr([("3 : n₀(MnO₄⁻) = C₁·V₁ = 1,0·10⁻² × 0,020 = 2,0·10⁻⁴ mol = 0,20 mmol", "zéro virgule deux millimole"),
              ("n₀(H₂C₂O₄) = C₂·V₂ = 5,0·10⁻² × 0,020 = 1,0·10⁻³ mol = 1,0 mmol", "un millimole ديال l'acide oxalique")],
             "السؤال trois. les ions permanganate: un fois dix puissance moins deux، fois zéro virgule zéro deux، égale deux fois dix puissance moins quatre mole، يعني zéro virgule deux millimole. l'acide oxalique: cinq fois dix puissance moins deux، fois zéro virgule zéro deux، égale dix puissance moins trois mole، يعني un millimole ديال l'acide oxalique."),
        "ex_tl5_3", "fa_tl5_3"),
      question("4", "À l'aide d'un tableau d'avancement, déterminer x_max et le réactif limitant. Justifier que le mélange final est incolore.",
        "السؤال quatre: ب le tableau d'avancement، لقا x max و le réactif limitant. ومن بعد برر علاش le mélange فالأخير بلا لون.",
        valeur("x_max", 0.10, "mmol", "MnO₄⁻ : 0,20 − 2x_max = 0 ⇒ 0,10 mmol ; H₂C₂O₄ : 1,0 − 5x_max = 0 ⇒ 0,20 mmol ; MnO₄⁻ limitant : x_max = 0,10 mmol"),
        ["n₀ − 2x", "n₀ − 5x", "x_max", "réactif limitant", "violet"], ["x_max = 0,20 mmol", "H₂C₂O₄ limitant", "x_max = 0,20 − 0,10"],
        [aide("Ligne « en cours » : n(MnO₄⁻) = 0,20 − 2x et n(H₂C₂O₄) = 1,0 − 5x (les coefficients 2 et 5). Quand chacun serait-il épuisé ?",
              "السطر ديال en cours: les ions permanganate، zéro virgule deux moins deux x. l'acide oxalique، un moins cinq x. فوقاش كل réactif كيسالي؟"),
         aide("La plus petite des deux valeurs est x_max. La seule espèce colorée est MnO₄⁻ (violet) : si c'est lui le réactif limitant, que reste-t-il à la fin ?",
              "القيمة الصغيرة هي x max. والوحيد اللي عندو لون هو l'ion permanganate، البنفسجي. يلا هو le réactif limitant، شنو كيبقى فالأخير؟")],
        corr([("4 : MnO₄⁻ : 0,20 − 2x_max = 0 donne 0,10 mmol ; H₂C₂O₄ : 1,0 − 5x_max = 0 donne 0,20 mmol", "zéro virgule un millimole et zéro virgule deux millimole"),
              ("x_max = 0,10 mmol : MnO₄⁻ est le réactif limitant.", "x max égale zéro virgule un millimole"),
              ("À la fin, n(MnO₄⁻) = 0 : plus d'ions violets, le mélange est incolore (Mn²⁺ pratiquement incolore).", "ما بقاش l'ion permanganate")],
             "السؤال quatre. les ions permanganate: zéro virgule deux moins deux x max égale zéro، كتعطي x max à zéro virgule un millimole. l'acide oxalique: un moins cinq x max égale zéro، كتعطي x max à zéro virgule deux millimole. ناخدو الصغيرة، zéro virgule un millimole et zéro virgule deux millimole: x max égale zéro virgule un millimole، و l'ion permanganate هو le réactif limitant. فالأخير ما بقاش l'ion permanganate، البنفسجي: إذن le mélange بلا لون."),
        "ex_tl5_4", "fa_tl5_4"),
      question("5", "Déterminer, en mmol, la quantité de dioxyde de carbone formée à l'état final.",
        "السؤال cinq: حسب ب millimole la quantité ديال le dioxyde de carbone اللي تكونات فالحالة النهائية.",
        valeur("n(CO₂)f", 1.0, "mmol", "n(CO₂)f = 10x_max = 10 × 0,10 = 1,0 mmol"),
        ["10x", "x_max", "coefficient", "mmol"], ["n(CO₂)f = x_max = 0,10 mmol", "n(CO₂)f = 2x_max"],
        [aide("Dans le tableau, la colonne de CO₂ suit son coefficient dans l'équation : combien de CO₂ se forment pour un avancement x ?",
              "ف le tableau، la colonne ديال le dioxyde de carbone كتبع le coefficient ديالو ف l'équation. شحال كيتكون ملي l'avancement هو x؟"),
         aide("n(CO₂) = 10x ; à l'état final, x = x_max.",
              "n de CO deux égale dix x، وفالأخير x égale x max.")],
        corr([("5 : n(CO₂) = 10x, donc n(CO₂)f = 10x_max", "dix x max"),
              ("A.N. : n(CO₂)f = 10 × 0,10 = 1,0 mmol", "un millimole ديال le dioxyde de carbone")],
             "السؤال cinq. le coefficient ديال le dioxyde de carbone égale dix: n de CO deux égale dix x. فالأخير، dix x max، يعني dix fois zéro virgule un، égale un millimole ديال le dioxyde de carbone."),
        "ex_tl5_5", "fa_tl5_5"),
      question("6", "On refait la même expérience dans un bain-marie à 40 °C. Prévoir la durée de la décoloration par rapport à 20 °C. L'état final est-il modifié ? Justifier.",
        "السؤال six: كنعاودو نفس التجربة ف bain-marie à quarante degrés Celsius. شنو غادي يوقع ل la durée ديال la décoloration؟ واش l'état final كيتبدل؟ برر.",
        phrase("La décoloration est plus rapide (durée plus courte qu'environ 7 min) : la température est un facteur cinétique ; plus elle est élevée, plus la transformation est rapide. L'état final n'est pas modifié : mêmes quantités initiales, même réactif limitant MnO₄⁻, même x_max = 0,10 mmol, même n(CO₂)f = 1,0 mmol."),
        ["plus courte", "facteur cinétique", "même x_max", "même état final"], ["plus de CO₂ formé à 40 °C", "durée plus longue"],
        [aide("Que change la température : la durée de la transformation, ou les quantités de réactifs mises au départ ?",
              "شنو كتبدل la température: la durée ديال la transformation، ولا les quantités ديال les réactifs اللي حطينا فالبداية؟"),
         aide("Plus la température est élevée, plus la transformation est rapide. x_max ne dépend que des quantités initiales et du réactif limitant.",
              "à température plus élevée، la transformation est plus rapide. و x max كيتعلق غير ب les quantités initiales و le réactif limitant.")],
        corr([("6 : à 40 °C, la décoloration est plus rapide : la température est un facteur cinétique.", "la décoloration plus rapide"),
              ("Même état final : mêmes quantités initiales, MnO₄⁻ limitant, x_max = 0,10 mmol.", "نفس l'état final")],
             "السؤال six. à quarante degrés Celsius، la décoloration plus rapide، يعني la durée أقصر من environ sept minutes، حيت la température est un facteur cinétique. ولكن نفس l'état final: نفس les quantités initiales، نفس le réactif limitant، ونفس x max، zéro virgule un millimole."),
        "ex_tl5_6", "fa_tl5_6"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_tl5_1", "Question 1 : le couple CO₂ / H₂C₂O₄", "Carbone, oxygène, hydrogène, charges : 2CO₂ + 2H⁺ + 2e⁻ ⇌ H₂C₂O₄.",
      SIM + "demi-equation.html?vue=oxalique", "La demi-équation du couple dioxyde de carbone / acide oxalique, geste par geste",
      "نبداو ب le couple: le dioxyde de carbone على اليسار، هو l'oxydant، و l'acide oxalique على اليمين، هو le réducteur. الخطوة الأولى، les atomes: deux carbone على اليمين، donc deux dioxyde de carbone. الخطوة التانية، les oxygènes: quatre et quatre، ما كاين ما نزيدو. الخطوة التالتة، les hydrogènes: deux على اليمين، donc deux H plus على اليسار. الخطوة الرابعة، les charges: plus deux على اليسار، et zéro على اليمين. donc deux électrons على اليسار. le résultat: deux dioxyde de carbone plus deux H plus plus deux électrons، donne acide oxalique.",
      centre=[(DEMI_OX, "le résultat: deux dioxyde de carbone")],
      pointage=[{"mot": "نبداو ب le couple", "commande": "play_until", "parametres": {"moment": "couple"}},
                {"mot": "الخطوة الأولى، les atomes", "commande": "play_until", "parametres": {"moment": "atomes"}},
                {"mot": "الخطوة التانية، les oxygènes", "commande": "play_until", "parametres": {"moment": "oxygene"}},
                {"mot": "الخطوة التالتة، les hydrogènes", "commande": "play_until", "parametres": {"moment": "hydrogene"}},
                {"mot": "الخطوة الرابعة، les charges", "commande": "play_until", "parametres": {"moment": "charges"}},
                {"mot": "donc deux électrons على اليسار", "repere": "electrons"},
                {"mot": "le résultat: deux dioxyde de carbone", "commande": "play_until", "parametres": {"moment": "verifier"}},
                {"mot": "le résultat: deux dioxyde de carbone", "cible": "centre:0"}]),
    diapo_sim("ex_tl5_2", "Question 2 : multiplier, additionner, simplifier", "× 2 et × 5 : dix électrons ; puis 16H⁺ − 10H⁺ = 6H⁺.",
      SIM + "equation.html?vue=permanganate", "L'ion permanganate et l'acide oxalique : les deux demi-équations, puis l'équation",
      "اللول، la réduction ديال l'ion permanganate، avec cinq électrons. التاني، l'oxydation ديال l'acide oxalique، avec deux électrons. باش يكون نفس العدد، كنوصلو à dix: كنضربو la première fois deux، et la deuxième fois cinq. كنجمعو، و les électrons كيمشيو. ولكن شوف les H plus: seize على اليسار، et dix على اليمين. كنبسطو: seize moins dix، égale six H plus على اليسار. le résultat: deux ions permanganate plus cinq acide oxalique، plus six H plus، donne deux ions manganèse deux، plus dix dioxyde de carbone، plus huit molécules d'eau. les charges: plus quatre et plus quatre.",
      centre=[("× 2 et × 5 : 10 e⁻ de chaque côté", "كنضربو la première fois deux"), (EQ, "le résultat: deux ions permanganate")],
      pointage=[{"mot": "اللول، la réduction", "commande": "play_until", "parametres": {"moment": "reduction"}},
                {"mot": "التاني، l'oxydation", "commande": "play_until", "parametres": {"moment": "oxydation"}},
                {"mot": "كنضربو la première fois deux", "commande": "play_until", "parametres": {"moment": "multiplier"}},
                {"mot": "كنضربو la première fois deux", "cible": "centre:0"},
                {"mot": "كنجمعو، و les électrons كيمشيو", "commande": "play_until", "parametres": {"moment": "additionner"}},
                {"mot": "كنبسطو", "commande": "play_until", "parametres": {"moment": "simplifier"}},
                {"mot": "كنبسطو", "repere": "simplification"},
                {"mot": "le résultat: deux ions permanganate", "cible": "centre:1"},
                {"mot": "les charges: plus quatre", "commande": "play_until", "parametres": {"moment": "verifier"}}]),
    diapo_sim("ex_tl5_3", "Question 3 : n = C·V en mmol", "Chaque réactif : sa concentration × son volume en litres.",
      SIM + "rappels.html?vue=concentration", "C = n/V, donc n = C·V",
      "شوف le bécher: zéro virgule zéro un mole dans cent millilitres، la concentration égale zéro virgule un mole par litre. la relation: C égale n sur V، إذن n égale C fois V، و V بالlitre. فالتمرين: vingt millilitres égale zéro virgule zéro deux litre. les ions permanganate: un fois dix puissance moins deux، fois zéro virgule zéro deux، égale zéro virgule deux millimole. l'acide oxalique: cinq fois dix puissance moins deux، fois zéro virgule zéro deux، égale un millimole.",
      centre=[("n₀(MnO₄⁻) = 0,20 mmol", "égale zéro virgule deux millimole"), ("n₀(H₂C₂O₄) = 1,0 mmol", "égale un millimole")],
      pointage=[{"mot": "شوف le bécher", "commande": "play_until", "parametres": {"moment": "becher"}},
                {"mot": "la relation: C égale n sur V", "commande": "play_until", "parametres": {"moment": "formule"}},
                {"mot": "égale zéro virgule deux millimole", "cible": "centre:0"},
                {"mot": "égale un millimole", "cible": "centre:1"}]),
    diapo_sim("ex_tl5_4", "Question 4 : x_max avec les coefficients", "Chaque réactif s'épuise pour n₀ − a·x = 0 ; la plus petite valeur est x_max.",
      SIM + "national-pas-a-pas.html?sujet=iodure&etape=5", "La méthode du tableau : chaque réactif, puis la plus petite valeur",
      "شوف la méthode ف le tableau ديال le cours: deux moins x، et dix moins deux x. كل réactif، فوقاش كيسالي؟ ومن بعد ناخدو القيمة الصغيرة. فالتمرين ديالنا، les coefficients sont deux et cinq. les ions permanganate: zéro virgule deux moins deux x max égale zéro، donne zéro virgule un millimole. l'acide oxalique: un moins cinq x max égale zéro، donne zéro virgule deux millimole. x max égale zéro virgule un millimole، و l'ion permanganate هو le réactif limitant. ما بقاش البنفسجي: le mélange بلا لون.",
      centre=[("x_max = 0,10 mmol : MnO₄⁻ limitant", "x max égale zéro virgule un millimole")],
      pointage=[{"mot": "شوف la méthode", "commande": "play_until", "parametres": {"moment": "rappel"}},
                {"mot": "شوف la méthode", "repere": "tableau"},
                {"mot": "كل réactif، فوقاش كيسالي؟", "commande": "play_until", "parametres": {"moment": "question"}},
                {"mot": "ومن بعد ناخدو القيمة الصغيرة", "commande": "play_until", "parametres": {"moment": "correction"}},
                {"mot": "x max égale zéro virgule un millimole", "cible": "centre:0"}]),
    diapo_sim("ex_tl5_5", "Question 5 : le CO₂ formé", "Le coefficient 10 de CO₂ : n(CO₂) = 10x.",
      SIM + "equation.html?vue=permanganate", "L'équation : on lit le coefficient de CO₂",
      "شوف l'équation ف la fin: deux ions permanganate plus cinq acide oxalique، plus six H plus، donne deux ions manganèse deux، plus dix dioxyde de carbone، plus huit molécules d'eau. le coefficient ديال le dioxyde de carbone égale dix. إذن ف le tableau، n de CO deux égale dix x. فالأخير، x égale x max، zéro virgule un millimole. dix fois zéro virgule un، égale un millimole ديال le dioxyde de carbone.",
      centre=[("n(CO₂)f = 10x_max = 10 × 0,10 = 1,0 mmol", "égale un millimole ديال le dioxyde de carbone")],
      pointage=[{"mot": "شوف l'équation", "commande": "play_until", "parametres": {"moment": "fin"}},
                {"mot": "شوف l'équation", "repere": "bilan"},
                {"mot": "égale un millimole ديال le dioxyde de carbone", "cible": "centre:0"}]),
    diapo_sim("ex_tl5_6", "Question 6 : plus chaud, plus rapide, même état final", "La température change la durée, pas x_max.",
      SIM + "facteurs.html?vue=temperature", "Le même mélange dans un bain à 20 °C et un bain à 40 °C",
      "هاد التجربة ديال le cours فيها نفس الفكرة. نفس le mélange dans deux béchers: le premier à vingt degrés Celsius، و le deuxième à quarante degrés Celsius. دابا كنبداو. le bécher السخون كيوصل للون الأخير ديالو environ trois fois plus tôt. ومن بعد، حتى البارد كيوصل. وشوف اللون فاللخر: هو هو. إذن la température est un facteur cinétique: كتبدل la durée، ولكن ما كتبدلش l'état final. فالتمرين ديالنا: à quarante degrés، اللون البنفسجي كيمشي قبل، ولكن نفس x max، zéro virgule un millimole.",
      centre=[("40 °C : décoloration plus rapide", "la température est un facteur cinétique"), ("Même état final : x_max = 0,10 mmol", "نفس x max")],
      pointage=[{"mot": "نفس le mélange", "commande": "play_until", "parametres": {"moment": "melange"}},
                {"mot": "دابا كنبداو", "commande": "play_until", "parametres": {"moment": "depart"}},
                {"mot": "le bécher السخون كيوصل", "commande": "play_until", "parametres": {"moment": "chaud_fini"}},
                {"mot": "حتى البارد كيوصل", "commande": "play_until", "parametres": {"moment": "froid_fini"}},
                {"mot": "وشوف اللون فاللخر", "commande": "play_until", "parametres": {"moment": "meme_final"}},
                {"mot": "la température est un facteur cinétique", "cible": "centre:0"},
                {"mot": "نفس x max", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_tl5_1", "Plus facile : la demi-équation de l'acide oxalique", "سؤال ساهل: اختار la demi-équation الصحيحة.",
      "La demi-équation du couple CO₂(aq)/H₂C₂O₄(aq) est…",
      ["CO₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ H₂C₂O₄(aq)", DEMI_OX, "2CO₂(aq) + 2H⁺(aq) ⇌ H₂C₂O₄(aq) + 2e⁻"], 1, {
        "1": {"juste": rep("برافو! deux carbone، deux H plus، et deux électrons من جهة l'oxydant.", "Juste : 2 C, 2 H⁺ et 2e⁻ du côté de l'oxydant.")},
        "0": {"1": rep("ما تقلقش. حسب les atomes de carbone: شحال ف l'acide oxalique؟ عاود اختار.", "Compte les atomes de carbone dans H₂C₂O₄. Réessaie."),
              "2": rep("الجواب: deux dioxyde de carbone، حيت l'acide oxalique contient deux carbone.", "Réponse : 2CO₂, car H₂C₂O₄ contient 2 atomes C.")},
        "2": {"1": rep("قريب. les atomes صحاح، ولكن les électrons فين خاصهم يكونو؟ عاود اختار.", "Les atomes sont bons ; de quel côté vont les électrons ? Réessaie."),
              "2": rep("الجواب: les électrons ديما من جهة l'oxydant، يعني مع le dioxyde de carbone.", "Réponse : les électrons sont du côté de l'oxydant CO₂.")}},
      "La demi-équation du couple dioxyde de carbone sur acide oxalique est ?"),
    qcm_facile("fa_tl5_2", "Plus facile : par quoi multiplier ?", "سؤال ساهل على les électrons.",
      "MnO₄⁻ capte 5 e⁻, H₂C₂O₄ en cède 2. Pour égaliser les électrons, on multiplie…",
      ["la réduction par 5 et l'oxydation par 2", "la réduction par 2 et l'oxydation par 5", "seulement l'oxydation par 5"], 1, {
        "1": {"juste": rep("برافو! cinq fois deux، et deux fois cinq: dix électrons من كل جهة.", "Juste : 5 × 2 = 2 × 5 = 10 électrons.")},
        "0": {"1": rep("فكر: cinq électrons fois cinq، شحال؟ et deux fois deux؟ واش متساويين؟ عاود اختار.", "5 × 5 et 2 × 2 sont-ils égaux ? Réessaie."),
              "2": rep("الجواب: la réduction fois deux، و l'oxydation fois cinq، pour avoir dix électrons.", "Réponse : réduction × 2, oxydation × 5 (10 e⁻).")},
        "2": {"1": rep("قريب. l'oxydation fois cinq donne dix électrons. و la réduction؟ cinq électrons بوحدهم ما كيكفيوش. عاود اختار.", "L'oxydation × 5 donne 10 e⁻ ; la réduction seule n'en a que 5. Réessaie."),
              "2": rep("الجواب: خاص حتى la réduction fois deux: dix électrons من كل جهة.", "Réponse : il faut aussi la réduction × 2.")}},
      "L'ion permanganate capte cinq électrons، l'acide oxalique en cède deux. On multiplie ?"),
    qcm_facile("fa_tl5_3", "Plus facile : n₀(H₂C₂O₄)", "سؤال ساهل على n égale C fois V.",
      "C₂ = 5,0·10⁻² mol/L et V₂ = 20 mL. n₀(H₂C₂O₄) vaut…",
      ["1,0 mmol", "1,0 mol", "2,5 mmol"], 0, {
        "0": {"juste": rep("برافو! cinq fois dix puissance moins deux، fois zéro virgule zéro deux، égale un millimole.", "Juste : 5,0·10⁻² × 0,020 = 1,0·10⁻³ mol = 1,0 mmol.")},
        "1": {"1": rep("ما تقلقش. V خاصو يكون بالlitre. vingt millilitres، شحال بالlitre؟ عاود اختار.", "V doit être en litres : 20 mL = ? L. Réessaie."),
              "2": rep("الجواب: un millimole. le résultat un mole، c'est fois vingt: V بقا ب millilitre.", "Réponse : 1,0 mmol ; 1,0 mol vient de V laissé en mL.")},
        "2": {"1": rep("قريب. deux virgule cinq جات من C sur V. ولكن n égale C fois V. عاود اختار.", "2,5 vient de C/V. Or n = C·V. Réessaie."),
              "2": rep("الجواب: n égale C fois V، égale un millimole.", "Réponse : n = C·V = 1,0 mmol.")}},
      "C deux égale cinq fois dix puissance moins deux mole par litre، V deux égale vingt millilitres. n zéro vaut ?"),
    vrai_faux_facile("fa_tl5_4", "Plus facile : vrai ou faux", "قول واش هاد الجمل صحيحة ولا غالطة.",
      "n₀(MnO₄⁻) = 0,20 mmol ; n₀(H₂C₂O₄) = 1,0 mmol ; coefficients 2 et 5.",
      [("MnO₄⁻ s'épuise pour x = 0,10 mmol.", True, "0,20 − 2x = 0 donne x = 0,10 mmol."),
       ("H₂C₂O₄ est le réactif limitant, car il en reste à la fin.", False, "Il en reste : il est en excès. Le limitant est celui qui s'épuise, MnO₄⁻."),
       ("Le mélange final est incolore, car il ne reste plus d'ions MnO₄⁻.", True, "MnO₄⁻ (violet) est limitant : il disparaît entièrement.")]),
    qcm_facile("fa_tl5_5", "Plus facile : le CO₂ formé", "سؤال ساهل على le coefficient.",
      "x_max = 0,10 mmol ; le coefficient de CO₂ dans l'équation est 10. n(CO₂)f vaut…",
      ["0,10 mmol", "0,20 mmol", "1,0 mmol"], 2, {
        "2": {"juste": rep("برافو! dix fois zéro virgule un، égale un millimole.", "Juste : 10 × 0,10 = 1,0 mmol.")},
        "0": {"1": rep("zéro virgule un هي x max. ولكن le coefficient ديال le dioxyde de carbone شحال؟ عاود اختار.", "0,10 mmol, c'est x_max ; et le coefficient de CO₂ ? Réessaie."),
              "2": rep("الجواب: n de CO deux égale dix x max، égale un millimole.", "Réponse : n(CO₂)f = 10x_max = 1,0 mmol.")},
        "1": {"1": rep("zéro virgule deux égale deux x max: هادا le coefficient ديال l'ion manganèse deux. وle dioxyde de carbone؟ عاود اختار.", "0,20 = 2x_max : c'est le coefficient de Mn²⁺. Et CO₂ ? Réessaie."),
              "2": rep("الجواب: un millimole، حيت le coefficient ديال le dioxyde de carbone égale dix.", "Réponse : 1,0 mmol (coefficient 10).")}},
      "x max égale zéro virgule un millimole، le coefficient du dioxyde de carbone est dix. n de CO deux finale vaut ?"),
    qcm_facile("fa_tl5_6", "Plus facile : à 40 °C", "سؤال ساهل على la température.",
      "À 40 °C au lieu de 20 °C, pour le même mélange…",
      ["la décoloration est plus rapide et l'état final est le même", "la décoloration est plus rapide et il se forme plus de CO₂", "la décoloration est plus lente"], 0, {
        "0": {"juste": rep("برافو! la température كتبدل la durée، ماشي x max.", "Juste : la température change la durée, pas x_max.")},
        "1": {"1": rep("قريب: plus rapide صحيح. ولكن x max واش كيتبدل؟ شنو اللي كيحددو؟ عاود اختار.", "Plus rapide, oui. Mais x_max change-t-il ? Réessaie."),
              "2": rep("الجواب: نفس l'état final. x max كيتعلق ب les quantités initiales، ماشي ب la température.", "Réponse : même état final ; x_max dépend des quantités initiales.")},
        "2": {"1": rep("لا، السخون كيمشي بالزربة la transformation. عاود اختار.", "Le chaud accélère la transformation. Réessaie."),
              "2": rep("الجواب: plus rapide، ونفس l'état final.", "Réponse : plus rapide, même état final.")}},
      "À quarante degrés Celsius au lieu de vingt، pour le même mélange ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "On mélange, à t = 0 et à 20 °C, V₁ = 10 mL d'une solution acidifiée de permanganate de potassium (C₁ = 2,0·10⁻² mol/L en MnO₄⁻(aq), H⁺(aq) en excès) et V₂ = 10 mL d'une solution d'acide oxalique de concentration C₂ = 4,0·10⁻² mol/L.",
      "intro_dit": "نفس التمرين، بمعطيات أخرى. V un égale dix millilitres، و C un égale deux fois dix puissance moins deux mole par litre. V deux égale dix millilitres، و C deux égale quatre fois dix puissance moins deux mole par litre.",
      "figures": [],
      "donnees": ["V₁ = 10 mL ; C₁ = 2,0·10⁻² mol/L", "V₂ = 10 mL ; C₂ = 4,0·10⁻² mol/L", "Couples : MnO₄⁻(aq)/Mn²⁺(aq) et CO₂(aq)/H₂C₂O₄(aq)", "Demi-équation : " + DEMI_MN],
      "questions": [
        question_semblable("1", "Écrire la demi-équation électronique du couple CO₂(aq)/H₂C₂O₄(aq) en milieu acide.",
          phrase(DEMI_OX), ["2CO₂(aq)", "2H⁺(aq)", "2e⁻"], ["CO₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ H₂C₂O₄(aq)"],
          corr([("1 : " + DEMI_OX, "deux dioxyde de carbone")], "deux dioxyde de carbone plus deux H plus plus deux électrons، donne acide oxalique.")),
        question_semblable("2", "Montrer que l'équation de la réaction s'écrit : " + EQ + ".",
          phrase("Réduction × 2, oxydation × 5 : 10 e⁻ ; on additionne et on simplifie 16H⁺ − 10H⁺ = 6H⁺ : " + EQ + " ; charges +4 = +4."),
          ["× 2", "× 5", "simplifier"], ["sans multiplier"],
          corr([("2 : réduction × 2, oxydation × 5, puis 16H⁺ − 10H⁺ = 6H⁺", "la réduction fois deux et l'oxydation fois cinq"), (EQ, "le résultat")],
               "la réduction fois deux et l'oxydation fois cinq: dix électrons. كنجمعو ونبسطو les H plus. le résultat هو l'équation المطلوبة.")),
        question_semblable("3", "Calculer, en mmol, les quantités de matière initiales n₀(MnO₄⁻) et n₀(H₂C₂O₄).",
          valeur("n₀(H₂C₂O₄)", 0.40, "mmol", "n₀(MnO₄⁻) = 2,0·10⁻² × 0,010 = 0,20 mmol ; n₀(H₂C₂O₄) = 4,0·10⁻² × 0,010 = 0,40 mmol"),
          ["n = C·V", "0,010 L"], ["n = C·(V₁ + V₂)"],
          corr([("3 : n₀(MnO₄⁻) = 0,20 mmol ; n₀(H₂C₂O₄) = 4,0·10⁻² × 0,010 = 0,40 mmol", "zéro virgule quatre millimole")],
               "les ions permanganate: zéro virgule deux millimole. l'acide oxalique: quatre fois dix puissance moins deux، fois zéro virgule zéro un، égale zéro virgule quatre millimole.")),
        question_semblable("4", "Déterminer x_max et le réactif limitant. Le mélange final est-il incolore ? Justifier.",
          valeur("x_max", 0.08, "mmol", "MnO₄⁻ : 0,20 − 2x_max = 0 ⇒ 0,10 mmol ; H₂C₂O₄ : 0,40 − 5x_max = 0 ⇒ 0,080 mmol ; H₂C₂O₄ limitant : x_max = 0,080 mmol"),
          ["n₀ − 2x", "n₀ − 5x", "réactif limitant"], ["x_max = 0,10 mmol", "MnO₄⁻ limitant"],
          corr([("4 : 0,10 mmol (MnO₄⁻) et 0,080 mmol (H₂C₂O₄) : x_max = 0,080 mmol, H₂C₂O₄ limitant", "zéro virgule zéro huit millimole"),
                ("Il reste n(MnO₄⁻) = 0,20 − 2 × 0,080 = 0,040 mmol : le mélange reste violet (pâle).", "le mélange يبقى violet")],
               "les ions permanganate donnent zéro virgule un millimole، و l'acide oxalique zéro virgule zéro huit millimole. x max égale zéro virgule zéro huit millimole، و l'acide oxalique هو le réactif limitant. كيبقى شوية ديال l'ion permanganate، إذن le mélange يبقى violet، ماشي بلا لون.")),
        question_semblable("5", "Déterminer, en mmol, la quantité de dioxyde de carbone formée à l'état final.",
          valeur("n(CO₂)f", 0.80, "mmol", "n(CO₂)f = 10x_max = 10 × 0,080 = 0,80 mmol"), ["10x", "x_max"], ["n(CO₂)f = x_max"],
          corr([("5 : n(CO₂)f = 10x_max = 10 × 0,080 = 0,80 mmol", "zéro virgule huit millimole")],
               "n de CO deux égale dix x max، يعني dix fois zéro virgule zéro huit، égale zéro virgule huit millimole.")),
        question_semblable("6", "On refait l'expérience à 40 °C. Prévoir l'évolution plus ou moins rapide. L'état final est-il modifié ? Justifier.",
          phrase("Plus rapide : la température est un facteur cinétique. Même état final : H₂C₂O₄ reste limitant, x_max = 0,080 mmol, le mélange final reste violet pâle."),
          ["plus rapide", "facteur cinétique", "même état final"], ["l'excès de MnO₄⁻ disparaît à 40 °C"],
          corr([("6 : plus rapide (facteur cinétique) ; même état final, x_max = 0,080 mmol", "نفس l'état final")],
               "à quarante degrés، plus rapide، حيت la température est un facteur cinétique. ولكن نفس l'état final: نفس le réactif limitant و نفس x max.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
