# Exercice de chimie (physique-chimie), ch. 9 « Transformations lentes et transformations rapides », niveau moyen n° 3 :
# les ions peroxodisulfate et les ions iodure — couples, équation, tableau d'avancement, x_max, lecture de n(I₂)(t).
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture phys_ch9_transformations_lentes_rapides.md (2ᵉ passe :
#    « exercice type national » = demi-équations, équation, tableau ligne par ligne, x_max, grandeur suivie n(I₂) = x),
#    sources_chimie_ch9_ch11.md (exercice corrigé de Bendaoud : couples, équation, tableau, x_max, n(I₂) ; S₂O₈²⁻ + I⁻ chez A2),
#    docs/parties_voix/phys_ch9_transformations_lentes_rapides.json ;
#  - le cours phys_ch9 (tl_x6b_diiode, tl_t3_catalyseur pour l'équation S₂O₈²⁻ + 2I⁻, tl_rp4, tl_rp5_avancement, tl_np3 à tl_np6) ;
#  - nationaux : demi-équations (2016 R, 2018 R, 2023 R), courbes d'une grandeur suivie (2023 N, 2025 N) ; ni vitesse ni t½ (ch. 10) ;
#  - séries en ligne : recherche faite (talamidi « série 1 » : demi-équations + quantités initiales ; moutamadris ; dreamjob) ;
#    PDF non ouverts (hôtes hors du réseau autorisé de la session), extraits de recherche seulement.
#  Données choisies pour retrouver les nombres des simulations (2 mmol et 10 mmol, x_max = 2 mmol, comme national-pas-a-pas.html).
#  Courbe : modèle de facteurs.html (S₂O₈²⁻ + I⁻ sans catalyseur, τ = 8 min) : n(I₂) = x_max·(1 − e^(−t/8)), t en min.
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch9_lentes_rapides_3"
SIM = "/media/simulations/chimie/transformations-lentes-rapides-tableau/"
TAU = 8.0


def courbe(xm, titre):
    return figure_courbe(titre, axe("t", 0, 50, "min", [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]),
        axe("n(I₂)", 0, 2.4, "mmol", [[round(0.2 * k, 1), f"{0.2 * k:.1f}".replace(".", ",")] for k in range(13)]),
        [{"f": "courbe", "expr": f"{xm}*(1-exp(-x/{TAU}))", "couleur": "orange", "texte": "n(I₂)", "texte_x": 42},
         {"f": "repere", "x": 10, "couleur": "faible"}],
        legende="Mélange à 20 °C, préparé à t = 0 ; la quantité de diiode est mesurée au cours du temps.")


# données de l'énoncé
C1, V1, C2, V2 = 4.0e-2, 0.050, 0.20, 0.050
n1, n2 = round(C1 * V1 * 1e3, 9), round(C2 * V2 * 1e3, 9)          # mmol : 2,0 et 10
XM = min(n1 / 1, n2 / 2)                          # 2,0 mmol, S₂O₈²⁻ limitant
L10 = XM * (1 - math.exp(-10 / TAU))              # 1,43 mmol lu ≈ 1,4
nI_10 = n2 - 2 * 1.4                              # 7,2 mmol
assert abs(n1 - 2.0) < 1e-9 and abs(n2 - 10) < 1e-9 and abs(XM - 2.0) < 1e-9 and abs(n2 / 2 - 5) < 1e-9
assert abs(L10 - 1.43) < 0.01 and abs(nI_10 - 7.2) < 1e-9 and abs((n2 - 2 * L10) - 7.2) / 7.2 < 0.03
# semblable
C1b, V1b, C2b, V2b = 3.0e-2, 0.050, 0.10, 0.050
n1b, n2b = round(C1b * V1b * 1e3, 9), round(C2b * V2b * 1e3, 9)      # 1,5 et 5,0 mmol
XMb = min(n1b, n2b / 2)                           # 1,5
L10b = XMb * (1 - math.exp(-10 / TAU))            # 1,07 lu ≈ 1,1
nI_10b = n2b - 2 * 1.1                            # 2,8
assert abs(n1b - 1.5) < 1e-9 and abs(n2b - 5.0) < 1e-9 and abs(XMb - 1.5) < 1e-9 and abs(L10b - 1.07) < 0.01
assert abs(nI_10b - 2.8) < 1e-9 and abs((n2b - 2 * L10b) - 2.8) / 2.8 < 0.05

EQ = "S₂O₈²⁻(aq) + 2I⁻(aq) → 2SO₄²⁻(aq) + I₂(aq)"

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "transformations_lentes_rapides", "cours": "phys_ch9_transformations_lentes_rapides",
  "titre": "Peroxodisulfate et iodure : équation, tableau d'avancement et courbe n(I₂)", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Écrire les demi-équations et établir l'équation d'oxydoréduction", "Calculer des quantités de matière n = C·V",
                  "Dresser un tableau d'avancement, déterminer x_max et le réactif limitant", "Exploiter une courbe n(I₂)(t) : transformation lente, n(I₂) = x"],
  "enonce": {
    "intro": "À la date t = 0, on mélange, à 20 °C, un volume V₁ = 50 mL d'une solution de peroxodisulfate de potassium de concentration C₁ = 4,0·10⁻² mol/L en ions S₂O₈²⁻(aq) et un volume V₂ = 50 mL d'une solution d'iodure de potassium de concentration C₂ = 0,20 mol/L en ions I⁻(aq). Le mélange, incolore au départ, jaunit puis brunit peu à peu : il se forme du diiode I₂(aq). Une méthode de suivi donne la quantité de diiode n(I₂) au cours du temps (figure 1).",
    "intro_dit": "نقراو l'énoncé. فt égale zéro، كنخلطو à vingt degrés Celsius، V un égale cinquante millilitres ديال la solution de peroxodisulfate de potassium، la concentration ديالها C un égale quatre fois dix puissance moins deux mole par litre، مع V deux égale cinquante millilitres ديال la solution d'iodure de potassium، la concentration ديالها C deux égale zéro virgule deux mole par litre. le mélange فالبداية بلا لون، ومن بعد كيولي jaune ومن بعد brun بشوية بشوية: كيتكون le diiode. و la figure un كتعطي la quantité ديال le diiode مع الوقت.",
    "figures": [courbe(XM, "Figure 1 : la quantité de diiode n(I₂) en fonction du temps")],
    "donnees": ["V₁ = 50 mL ; C₁ = [S₂O₈²⁻] = 4,0·10⁻² mol/L", "V₂ = 50 mL ; C₂ = [I⁻] = 0,20 mol/L",
                "Couples : S₂O₈²⁻(aq)/SO₄²⁻(aq) et I₂(aq)/I⁻(aq)"],
    "questions": [
      question("1", "Écrire la demi-équation électronique de chacun des deux couples.",
        "السؤال un: كتب la demi-équation électronique ديال كل couple.",
        phrase("S₂O₈²⁻(aq) + 2e⁻ ⇌ 2SO₄²⁻(aq) ; I₂(aq) + 2e⁻ ⇌ 2I⁻(aq)"),
        ["Ox + n e⁻ ⇌ Red", "2SO₄²⁻(aq)", "2I⁻(aq)", "2e⁻", "⇌"], ["S₂O₈²⁻(aq) ⇌ 2SO₄²⁻(aq) + 2e⁻", "I₂(aq) + e⁻ ⇌ I⁻(aq)"],
        [aide("Pour chaque couple : l'oxydant à gauche, le réducteur à droite. Commence par les atomes : combien d'atomes de soufre dans S₂O₈²⁻, combien d'iode dans I₂ ?",
              "فكل couple: l'oxydant على اليسار و le réducteur على اليمين. بدا ب les atomes: شحال من soufre ف l'ion peroxodisulfate، وشحال من iode ف le diiode؟"),
         aide("2 atomes S donnent 2SO₄²⁻ ; 2 atomes I donnent 2I⁻. Compte ensuite les charges : −2 à gauche et −4 à droite pour le premier, 0 et −2 pour le second ; les électrons se placent du côté de l'oxydant.",
              "deux soufre donnent deux ions sulfate، et deux iode donnent deux ions iodure. من بعد حسب les charges: moins deux على اليسار et moins quatre على اليمين ف le premier couple، zéro et moins deux ف le deuxième. les électrons ديما من جهة l'oxydant.")],
        corr([("1 : S₂O₈²⁻(aq) + 2e⁻ ⇌ 2SO₄²⁻(aq)", "ion peroxodisulfate plus deux électrons donne deux ions sulfate"),
              ("I₂(aq) + 2e⁻ ⇌ 2I⁻(aq)", "diiode plus deux électrons donne deux ions iodure")],
             "السؤال un. le couple ion peroxodisulfate sur ion sulfate: ion peroxodisulfate plus deux électrons donne deux ions sulfate. les charges: moins deux moins deux، égale moins quatre، et moins quatre على اليمين. و le couple diiode sur ion iodure: diiode plus deux électrons donne deux ions iodure."),
        "ex_tl3_1", "fa_tl3_1"),
      question("2", "Montrer que l'équation de la réaction s'écrit : " + EQ + ".",
        "السؤال deux: بين بلي l'équation ديال la réaction هي: ion peroxodisulfate plus deux ions iodure، donne deux ions sulfate plus diiode.",
        phrase("S₂O₈²⁻ est l'oxydant qui réagit (réduction) : S₂O₈²⁻(aq) + 2e⁻ → 2SO₄²⁻(aq). I⁻ est le réducteur qui réagit (oxydation) : 2I⁻(aq) → I₂(aq) + 2e⁻. Même nombre d'électrons (2) : on additionne et les électrons disparaissent : " + EQ + ". Charges : −4 = −4."),
        ["réduction", "oxydation", "2I⁻(aq) → I₂(aq) + 2e⁻", "additionner", "charges"], ["S₂O₈²⁻(aq) + 2I⁻(aq) + 2e⁻ → 2SO₄²⁻(aq) + I₂(aq)", "I₂(aq) + 2SO₄²⁻(aq) → …"],
        [aide("Les réactifs mis ensemble sont S₂O₈²⁻ et I⁻. Lequel capte les électrons, lequel les cède ? Écris l'oxydation de I⁻ dans le bon sens.",
              "les réactifs هوما l'ion peroxodisulfate و les ions iodure. شكون كيشد les électrons، وشكون كيعطيهم؟ كتب l'oxydation ديال les ions iodure فالاتجاه الصحيح."),
         aide("Réduction de S₂O₈²⁻ (2e⁻) et oxydation 2I⁻ → I₂ + 2e⁻ : même nombre d'électrons, on additionne sans multiplier. Vérifie les charges : −2 − 2 à gauche, 2 × (−2) à droite.",
              "la réduction ديال l'ion peroxodisulfate، avec deux électrons، و l'oxydation: deux ions iodure donne diiode plus deux électrons. نفس العدد: كنجمعو بلا ما نضربو. ومن بعد نتأكدو من les charges.")],
        corr([("2 : réduction : S₂O₈²⁻(aq) + 2e⁻ → 2SO₄²⁻(aq)", "la réduction ديال l'ion peroxodisulfate"),
              ("oxydation : 2I⁻(aq) → I₂(aq) + 2e⁻", "deux ions iodure donne diiode plus deux électrons"),
              ("Somme : " + EQ + " ; charges : −4 = −4", "les charges: moins quatre")],
             "السؤال deux. la réduction ديال l'ion peroxodisulfate: ion peroxodisulfate plus deux électrons donne deux ions sulfate. l'oxydation ديال les ions iodure: deux ions iodure donne diiode plus deux électrons. نفس العدد ديال les électrons، كنجمعو و les électrons كيمشيو. l'équation: ion peroxodisulfate plus deux ions iodure، donne deux ions sulfate plus diiode. les charges: moins quatre على اليسار، et moins quatre على اليمين."),
        "ex_tl3_2", "fa_tl3_2"),
      question("3", "Calculer, en mmol, les quantités de matière initiales n₀(S₂O₈²⁻) et n₀(I⁻).",
        "السؤال trois: حسب ب millimole les quantités de matière initiales ديال les ions peroxodisulfate و les ions iodure.",
        valeur("n₀(I⁻)", 10.0, "mmol", "n₀(S₂O₈²⁻) = C₁·V₁ = 4,0·10⁻² × 0,050 = 2,0·10⁻³ mol = 2,0 mmol ; n₀(I⁻) = C₂·V₂ = 0,20 × 0,050 = 10 mmol"),
        ["n = C·V", "0,050 L", "10⁻³ mol = 1 mmol", "mmol"], ["n = C·V avec V = 50", "n = C·(V₁ + V₂)"],
        [aide("Chaque réactif est apporté par sa propre solution : utilise C₁ avec V₁, et C₂ avec V₂. Écris les volumes en litres.",
              "كل réactif جا من la solution ديالو: خدم ب C un مع V un، و C deux مع V deux. وكتب les volumes بالlitre."),
         aide("n = C·V avec V en L : 50 mL = 0,050 L. Puis 1 mmol = 10⁻³ mol.",
              "n égale C fois V، و V بالlitre: cinquante millilitres égale zéro virgule zéro cinq litre. et un millimole égale dix puissance moins trois mole.")],
        corr([("3 : n₀(S₂O₈²⁻) = C₁·V₁ = 4,0·10⁻² × 0,050 = 2,0·10⁻³ mol = 2,0 mmol", "deux millimoles ديال les ions peroxodisulfate"),
              ("n₀(I⁻) = C₂·V₂ = 0,20 × 0,050 = 1,0·10⁻² mol = 10 mmol", "dix millimoles ديال les ions iodure")],
             "السؤال trois. n zéro égale C fois V، لكل réactif. les ions peroxodisulfate: quatre fois dix puissance moins deux، fois zéro virgule zéro cinq، égale deux fois dix puissance moins trois mole، يعني deux millimoles ديال les ions peroxodisulfate. les ions iodure: zéro virgule deux fois zéro virgule zéro cinq، égale dix puissance moins deux mole، يعني dix millimoles ديال les ions iodure."),
        "ex_tl3_3", "fa_tl3_3"),
      question("4", "Dresser le tableau d'avancement de la réaction. Déterminer l'avancement maximal x_max et le réactif limitant.",
        "السؤال quatre: دير le tableau d'avancement، ومن بعد لقا l'avancement maximal x max و le réactif limitant.",
        valeur("x_max", 2.0, "mmol", "2,0 − x_max = 0 ⇒ 2,0 mmol ; 10 − 2x_max = 0 ⇒ 5,0 mmol ; S₂O₈²⁻ limitant : x_max = 2,0 mmol"),
        ["n₀ − x", "n₀ − 2x", "x_max", "la plus petite valeur", "réactif limitant"], ["x_max = 5,0 mmol", "x_max = 10 mmol", "I⁻ limitant"],
        [aide("Ligne « en cours » : chaque coefficient de l'équation dit combien part ou se forme. Pour S₂O₈²⁻ : 2,0 − x ; pour I⁻ : 10 − 2x ; pour I₂ : x.",
              "السطر ديال en cours: les coefficients ديال l'équation كيقولو شحال كيمشي و شحال كيتكون. l'ion peroxodisulfate: deux moins x. les ions iodure: dix moins deux x. le diiode: x."),
         aide("Cherche quand chaque réactif serait épuisé (quantité nulle), puis garde la plus petite des deux valeurs : c'est x_max ; le réactif correspondant est limitant.",
              "قلب فوقاش كل réactif كيسالي، يعني la quantité égale zéro. ومن بعد خود القيمة الصغيرة: هي x max، و le réactif ديالها هو le réactif limitant.")],
        corr([("4 : état initial : 2,0 | 10 | 0 | 0 (mmol) ; en cours : 2,0 − x | 10 − 2x | 2x | x", "deux moins x، dix moins deux x"),
              ("2,0 − x_max = 0 donne x_max = 2,0 mmol ; 10 − 2x_max = 0 donne x_max = 5,0 mmol", "deux millimoles et cinq millimoles"),
              ("x_max = 2,0 mmol : S₂O₈²⁻ est le réactif limitant.", "x max égale deux millimoles")],
             "السؤال quatre. l'état initial: deux، dix، zéro، zéro millimoles. en cours: deux moins x، dix moins deux x، deux x ديال les ions sulfate، و x ديال le diiode. يلا سالاو les ions peroxodisulfate: deux moins x max égale zéro، كتعطي x max à deux millimoles. يلا سالاو les ions iodure: dix moins deux x max égale zéro، كتعطي x max à cinq millimoles. ناخدو الصغيرة، deux millimoles et cinq millimoles: x max égale deux millimoles، و l'ion peroxodisulfate هو le réactif limitant."),
        "ex_tl3_4", "fa_tl3_4"),
      question("5", "En exploitant la figure 1, justifier que cette transformation est lente. Quelle relation lie n(I₂) à l'avancement x ? Lire la valeur finale de n(I₂) et la comparer à x_max.",
        "السؤال cinq: من la figure un، برر بلي هاد la transformation lente. شنو هي العلاقة بين n de I deux و l'avancement x؟ قرا la valeur finale ديال n de I deux، وقارنها مع x max.",
        valeur("n(I₂)f", 2.0, "mmol", "n(I₂) augmente peu à peu pendant environ 40 min : lente ; n(I₂) = x, donc n(I₂)f = x_max = 2,0 mmol"),
        ["lente", "états intermédiaires", "n(I₂) = x", "palier", "x_max"], ["n(I₂) = 2x", "rapide car n(I₂) devient constante"],
        [aide("Regarde la courbe : n(I₂) atteint-elle sa valeur finale dès le mélange, ou monte-t-elle pendant des minutes ? Lis la valeur où la courbe devient horizontale.",
              "شوف la courbe: واش n de I deux كتوصل للقيمة الأخيرة فلحظة، ولا كتطلع خلال des minutes؟ قرا la valeur فين la courbe كتولي أفقية."),
         aide("Dans le tableau, la colonne de I₂ vaut x : n(I₂) = x. À la fin, x = x_max.",
              "ف le tableau، la colonne ديال le diiode هي x: n de I deux égale x. وفالأخير، x égale x max.")],
        corr([("5 : n(I₂) croît peu à peu pendant environ 40 min : on suit l'évolution, la transformation est lente.", "la transformation lente"),
              ("D'après le tableau, n(I₂) = x ; la courbe tend vers n(I₂)f = 2,0 mmol.", "n de I deux égale x"),
              ("n(I₂)f = x_max = 2,0 mmol : accord avec la question 4.", "égale x max، deux millimoles")],
             "السؤال cinq. n de I deux كتطلع بشوية بشوية خلال environ quarante minutes: كنتبعو l'évolution، إذن la transformation lente. ومن le tableau، n de I deux égale x. la courbe كتوصل لواحد la valeur أفقية: n de I deux finale égale x max، deux millimoles. نفس الجواب ديال السؤال quatre."),
        "ex_tl3_5", "fa_tl3_5"),
      question("6", "Lire sur la figure 1 la quantité de diiode à la date t = 10 min. En déduire, en mmol, la quantité d'ions iodure restant à cette date.",
        "السؤال six: قرا على la figure un la quantité ديال le diiode à dix minutes. ومن بعد استنتج la quantité ديال les ions iodure اللي بقات فهاد اللحظة.",
        valeur("n(I⁻)", 7.2, "mmol", "x(10 min) = n(I₂) ≈ 1,4 mmol ; n(I⁻) = 10 − 2x = 10 − 2 × 1,4 = 7,2 mmol", tol=0.05),
        ["x = n(I₂)", "n(I⁻) = n₀(I⁻) − 2x", "lecture graphique", "mmol"], ["n(I⁻) = 10 − 1,4", "n(I⁻) = 1,4 mmol"],
        [aide("Monte verticalement de t = 10 min jusqu'à la courbe, puis lis n(I₂) sur l'axe vertical. Cette valeur est l'avancement x à cette date.",
              "طلع عمودي à partir de dix minutes حتى la courbe، ومن بعد قرا n de I deux على l'axe العمودي. هاد la valeur هي l'avancement x فهاد اللحظة."),
         aide("Ligne « en cours » du tableau : n(I⁻) = 10 − 2x (le coefficient de I⁻ est 2).",
              "السطر ديال en cours: n de I moins égale dix moins deux x، حيت le coefficient ديال les ions iodure égale deux.")],
        corr([("6 : à t = 10 min, n(I₂) ≈ 1,4 mmol, donc x ≈ 1,4 mmol", "n de I deux environ un virgule quatre millimoles"),
              ("n(I⁻) = n₀(I⁻) − 2x = 10 − 2 × 1,4", "dix moins deux fois un virgule quatre"),
              ("n(I⁻) ≈ 7,2 mmol", "sept virgule deux millimoles")],
             "السؤال six. à dix minutes، كنقراو n de I deux environ un virgule quatre millimoles، إذن x environ un virgule quatre millimoles. n de I moins égale dix moins deux fois un virgule quatre، كتعطي environ sept virgule deux millimoles."),
        "ex_tl3_6", "fa_tl3_6"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_tl3_1", "Question 1 : une demi-équation en quatre gestes", "Atomes, oxygènes, hydrogènes, charges : les électrons du côté de l'oxydant.",
      SIM + "demi-equation.html?vue=iode", "Le couple diiode / ion iodure, geste par geste",
      "نبداو ب le couple diiode sur ion iodure. le diiode على اليسار، و l'ion iodure على اليمين. les atomes: deux atomes d'iode على اليسار، donc deux ions iodure على اليمين. ما كاين لا oxygène لا hydrogène. les charges: zéro على اليسار، et moins deux على اليمين. إذن on ajoute deux électrons من جهة l'oxydant. le résultat: diiode plus deux électrons donne deux ions iodure. نفس الطريقة ل l'ion peroxodisulfate: deux atomes de soufre، donc deux ions sulfate. les charges: moins deux على اليسار، et moins quatre على اليمين: حتى هنا، on ajoute deux électrons على اليسار.",
      centre=[("I₂(aq) + 2e⁻ ⇌ 2I⁻(aq)", "diiode plus deux électrons donne deux ions iodure"), ("S₂O₈²⁻(aq) + 2e⁻ ⇌ 2SO₄²⁻(aq)", "حتى هنا، on ajoute deux électrons على اليسار")],
      pointage=[{"mot": "نبداو ب le couple", "commande": "play_until", "parametres": {"moment": "couple"}},
                {"mot": "les atomes: deux atomes d'iode", "commande": "play_until", "parametres": {"moment": "atomes"}},
                {"mot": "ما كاين لا oxygène لا hydrogène", "commande": "play_until", "parametres": {"moment": "hydrogene"}},
                {"mot": "les charges: zéro على اليسار", "commande": "play_until", "parametres": {"moment": "charges"}},
                {"mot": "on ajoute deux électrons من جهة", "repere": "electrons"},
                {"mot": "diiode plus deux électrons donne deux ions iodure", "repere": "resultat"},
                {"mot": "diiode plus deux électrons donne deux ions iodure", "cible": "centre:0"},
                {"mot": "نفس الطريقة", "commande": "play_until", "parametres": {"moment": "verifier"}},
                {"mot": "حتى هنا، on ajoute deux électrons على اليسار", "cible": "centre:1"}]),
    diapo_sim("ex_tl3_2", "Question 2 : l'équation S₂O₈²⁻ + 2I⁻", "Deux électrons captés, deux électrons cédés : on additionne.",
      SIM + "facteurs.html?vue=catalyseur", "Le mélange des ions peroxodisulfate et iodure, puis son équation",
      "شوف هاد les béchers: فيهم نفس le mélange، les ions peroxodisulfate و les ions iodure. هادا هو le mélange ديال التمرين. l'ion peroxodisulfate capte deux électrons: هادي la réduction. les ions iodure cèdent deux électrons: deux ions iodure donne diiode plus deux électrons، هادي l'oxydation. نفس العدد، إذن كنجمعو، و les électrons كيمشيو. l'équation: ion peroxodisulfate plus deux ions iodure، donne deux ions sulfate plus diiode. les charges: moins quatre على اليسار، et moins quatre على اليمين.",
      centre=[("2I⁻(aq) → I₂(aq) + 2e⁻", "deux ions iodure donne diiode plus deux électrons"), (EQ, "l'équation: ion peroxodisulfate plus deux ions iodure")],
      pointage=[{"mot": "شوف هاد les béchers", "commande": "play_until", "parametres": {"moment": "melange"}},
                {"mot": "شوف هاد les béchers", "repere": "becher_sans"},
                {"mot": "deux ions iodure donne diiode plus deux électrons", "cible": "centre:0"},
                {"mot": "l'équation: ion peroxodisulfate plus deux ions iodure", "commande": "play_until", "parametres": {"moment": "equation"}},
                {"mot": "l'équation: ion peroxodisulfate plus deux ions iodure", "repere": "equation"},
                {"mot": "l'équation: ion peroxodisulfate plus deux ions iodure", "cible": "centre:1"}]),
    diapo_sim("ex_tl3_3", "Question 3 : n = C·V pour chaque réactif", "Chaque réactif avec SA concentration et SON volume, en litres.",
      SIM + "rappels.html?vue=concentration", "C = n/V : la quantité de soluté et le volume de la solution",
      "شوف هاد le bécher: zéro virgule zéro un mole ديال le soluté dans cent millilitres. la relation: C égale n sur V، إذن n égale C fois V، و V بالlitre. فالتمرين، كل réactif عندو la solution ديالو. les ions peroxodisulfate: C un fois V un، يعني quatre fois dix puissance moins deux، fois zéro virgule zéro cinq litre، égale deux millimoles. les ions iodure: C deux fois V deux، يعني zéro virgule deux fois zéro virgule zéro cinq، égale dix millimoles. رد البال: ما نخدموش ب le volume total هنا، حيت C un و C deux هوما les concentrations ديال les solutions قبل الخلط.",
      centre=[("n₀(S₂O₈²⁻) = C₁·V₁ = 2,0 mmol", "égale deux millimoles"), ("n₀(I⁻) = C₂·V₂ = 10 mmol", "égale dix millimoles")],
      pointage=[{"mot": "شوف هاد le bécher", "commande": "play_until", "parametres": {"moment": "becher"}},
                {"mot": "la relation: C égale n sur V", "commande": "play_until", "parametres": {"moment": "formule"}},
                {"mot": "la relation: C égale n sur V", "repere": "formule"},
                {"mot": "égale deux millimoles", "cible": "centre:0"},
                {"mot": "égale dix millimoles", "cible": "centre:1"}]),
    diapo_sim("ex_tl3_4", "Question 4 : x_max et le réactif limitant", "Chaque réactif donne une valeur de x_max : on garde la plus petite.",
      SIM + "national-pas-a-pas.html?sujet=iodure&etape=5", "Le tableau d'avancement : la ligne en cours, puis l'état final",
      "شوف le tableau d'avancement ديال le cours: نفس الأرقام ديالنا، deux millimoles et dix millimoles. السطر ديال en cours: deux moins x، dix moins deux x، و x. دابا كل réactif، فوقاش كيسالي؟ deux moins x max égale zéro، كتعطي x max à deux millimoles. dix moins deux x max égale zéro، كتعطي x max à cinq millimoles. ناخدو القيمة الصغيرة: x max égale deux millimoles. فالتمرين ديالنا، l'ion peroxodisulfate هو اللي عندو seulement deux millimoles: هو le réactif limitant.",
      centre=[("x_max = 2,0 mmol : S₂O₈²⁻ limitant", "x max égale deux millimoles")],
      pointage=[{"mot": "شوف le tableau d'avancement", "commande": "play_until", "parametres": {"moment": "rappel"}},
                {"mot": "شوف le tableau d'avancement", "repere": "tableau"},
                {"mot": "deux moins x، dix moins deux x، و x", "commande": "play_until", "parametres": {"moment": "case_3"}},
                {"mot": "فوقاش كيسالي", "commande": "play_until", "parametres": {"moment": "question"}},
                {"mot": "ناخدو القيمة الصغيرة", "commande": "play_until", "parametres": {"moment": "correction"}},
                {"mot": "x max égale deux millimoles", "cible": "centre:0"}]),
    diapo_sim("ex_tl3_5", "Question 5 : une transformation lente", "Le diiode se forme peu à peu : on distingue les états intermédiaires.",
      SIM + "bechers.html?vue=lente", "Un mélange qui brunit peu à peu : le diiode se forme",
      "شوف هاد le bécher: المحلول فالبداية بلا لون. كيولي jaune، ومن بعد brun، بشوية بشوية: هادا هو le diiode اللي كيتكون. le chronomètre كيدور عدة minutes، ومن بعد اللون كيوقف. on distingue les états intermédiaires: إذن transformation lente. نفس الشي ف la figure un: n de I deux كتطلع خلال environ quarante minutes. و n de I deux égale x، إذن فالأخير n de I deux égale x max، deux millimoles.",
      centre=[("Lente : n(I₂) croît pendant ≈ 40 min", "إذن transformation lente"), ("n(I₂) = x ; n(I₂)f = x_max = 2,0 mmol", "n de I deux égale x max")],
      pointage=[{"mot": "شوف هاد le bécher", "repere": "becher"},
                {"mot": "كيولي jaune", "commande": "play_until", "parametres": {"moment": "jaune"}},
                {"mot": "ومن بعد brun", "commande": "play_until", "parametres": {"moment": "brun"}},
                {"mot": "le chronomètre كيدور", "repere": "chrono"},
                {"mot": "ومن بعد اللون كيوقف", "commande": "play_until", "parametres": {"moment": "palier"}},
                {"mot": "إذن transformation lente", "cible": "centre:0"},
                {"mot": "n de I deux égale x max", "cible": "centre:1"}]),
    diapo_sim("ex_tl3_6", "Question 6 : lire x, puis calculer n(I⁻)", "n(I₂) = x : on lit x sur la courbe, puis n(I⁻) = n₀ − 2x.",
      SIM + "national-pas-a-pas.html?sujet=iodure&etape=6", "La courbe n(I₂)(t) et le tableau : n(I₂) = x",
      "شوف la courbe ديال n de I deux مع الوقت. ف le tableau، la colonne ديال le diiode هي x: n de I deux égale x. إذن فأي لحظة، كنقراو x مباشرة على la courbe. فالتمرين ديالنا، à dix minutes، كنطلعو عمودي حتى la courbe، وكنقراو environ un virgule quatre millimoles. من بعد السطر ديال en cours: n de I moins égale dix moins deux x. dix moins deux fois un virgule quatre، كتعطي environ sept virgule deux millimoles.",
      centre=[("n(I₂) = x", "n de I deux égale x"), ("n(I⁻) = 10 − 2 × 1,4 ≈ 7,2 mmol", "environ sept virgule deux millimoles")],
      pointage=[{"mot": "شوف la courbe", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "شوف la courbe", "repere": "graphe_n"},
                {"mot": "n de I deux égale x", "commande": "play_until", "parametres": {"moment": "rappel"}},
                {"mot": "n de I deux égale x", "cible": "centre:0"},
                {"mot": "environ sept virgule deux millimoles", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_tl3_1", "Plus facile : la demi-équation du peroxodisulfate", "سؤال ساهل: اختار la demi-équation الصحيحة.",
      "La demi-équation du couple S₂O₈²⁻(aq)/SO₄²⁻(aq) est…",
      ["S₂O₈²⁻(aq) ⇌ 2SO₄²⁻(aq) + 2e⁻", "S₂O₈²⁻(aq) + e⁻ ⇌ SO₄²⁻(aq)", "S₂O₈²⁻(aq) + 2e⁻ ⇌ 2SO₄²⁻(aq)"], 2, {
        "2": {"juste": rep("برافو! deux soufre، donc deux ions sulfate، et deux électrons من جهة l'oxydant.", "Juste : 2 S donc 2SO₄²⁻, et 2e⁻ du côté de l'oxydant.")},
        "0": {"1": rep("قريب. les atomes صحاح، ولكن les électrons فين خاصهم يكونو؟ عاود اختار.", "Les atomes sont bons, mais de quel côté se placent les électrons ? Réessaie."),
              "2": rep("الجواب: les électrons ديما من جهة l'oxydant، يعني على اليسار مع l'ion peroxodisulfate.", "Réponse : S₂O₈²⁻ + 2e⁻ ⇌ 2SO₄²⁻ ; les électrons sont toujours du côté de l'oxydant.")},
        "1": {"1": rep("ما تقلقش. حسب les atomes de soufre: شحال على اليسار، وشحال على اليمين؟ عاود اختار.", "Compte les atomes de soufre à gauche et à droite. Réessaie."),
              "2": rep("الجواب: deux soufre على اليسار، donc deux ions sulfate، و les charges donnent deux électrons.", "Réponse : 2 S à gauche donc 2SO₄²⁻ ; les charges imposent 2e⁻.")}},
      "La demi-équation du couple ion peroxodisulfate sur ion sulfate est ?"),
    vrai_faux_facile("fa_tl3_2", "Plus facile : vrai ou faux", "قول واش هاد الجمل صحيحة ولا غالطة.",
      EQ,
      [("Dans cette réaction, les ions iodure I⁻ cèdent des électrons : ils sont oxydés.", True, "2I⁻ → I₂ + 2e⁻ : une perte d'électrons, c'est une oxydation."),
       ("Les électrons doivent apparaître dans l'équation de la réaction.", False, "Les 2 électrons cédés par I⁻ sont captés par S₂O₈²⁻ : ils disparaissent dans la somme."),
       ("Les charges sont conservées : −4 à gauche et −4 à droite.", True, "À gauche −2 + 2 × (−1) = −4 ; à droite 2 × (−2) + 0 = −4.")]),
    qcm_facile("fa_tl3_3", "Plus facile : n₀(I⁻)", "سؤال ساهل على n égale C fois V.",
      "C₂ = 0,20 mol/L et V₂ = 50 mL. La quantité n₀(I⁻) vaut…",
      ["10 mmol", "10 mol", "4,0 mmol"], 0, {
        "0": {"juste": rep("برافو! zéro virgule deux fois zéro virgule zéro cinq litre، égale dix millimoles.", "Juste : 0,20 × 0,050 = 1,0·10⁻² mol = 10 mmol.")},
        "1": {"1": rep("ما تقلقش. V خدمتي بيه ب millilitre؟ خاصو يكون بالlitre. عاود اختار.", "V doit être en litres. Réessaie."),
              "2": rep("الجواب: dix millimoles. le résultat dix mole، c'est zéro virgule deux fois cinquante، V بقا ب millilitre.", "Réponse : 10 mmol ; 10 mol vient de 0,20 × 50 avec V en mL.")},
        "2": {"1": rep("قريب. quatre égale zéro virgule deux sur zéro virgule zéro cinq: C sur V. ولكن n égale C fois V. عاود اختار.", "4 vient de C/V. Or n = C·V. Réessaie."),
              "2": rep("الجواب: n égale C fois V، égale dix millimoles. quatre جات من C sur V.", "Réponse : n = C·V = 10 mmol (4 vient de C/V).")}},
      "C deux égale zéro virgule deux mole par litre، V deux égale cinquante millilitres. n zéro de I moins vaut ?"),
    qcm_facile("fa_tl3_4", "Plus facile : x_max", "سؤال ساهل على x max.",
      "n₀(S₂O₈²⁻) = 2,0 mmol, n₀(I⁻) = 10 mmol, équation S₂O₈²⁻ + 2I⁻ → 2SO₄²⁻ + I₂. L'avancement maximal x_max vaut…",
      ["5,0 mmol", "2,0 mmol", "10 mmol"], 1, {
        "1": {"juste": rep("برافو! deux et cinq: ناخدو الصغيرة، x max égale deux millimoles.", "Juste : 2,0 et 5,0 mmol, on garde la plus petite : 2,0 mmol.")},
        "0": {"1": rep("cinq millimoles هي ديال les ions iodure. ولكن l'ion peroxodisulfate كيسالي قبل: فوقاش؟ عاود اختار.", "5,0 mmol, c'est pour I⁻. Mais S₂O₈²⁻ s'épuise-t-il avant ? Réessaie."),
              "2": rep("الجواب: deux millimoles. le réactif اللي كيسالي اللول هو اللي كيحبس la réaction: الصغيرة.", "Réponse : 2,0 mmol ; le premier réactif épuisé arrête la réaction : la plus petite valeur.")},
        "2": {"1": rep("ما تقلقش. dix هي n zéro ديال les ions iodure، ماشي x max. résous dix moins deux x max égale zéro. عاود اختار.", "10 mmol est n₀(I⁻), pas x_max : résous 10 − 2x_max = 0. Réessaie."),
              "2": rep("الجواب: deux millimoles. dix moins deux x max donne cinq، et deux moins x max donne deux: la plus petite، c'est deux.", "Réponse : 2,0 mmol (I⁻ donnerait 5,0 mmol, pas 10).")}},
      "deux millimoles ديال peroxodisulfate، et dix millimoles ديال iodure. x max vaut ?"),
    vrai_faux_facile("fa_tl3_5", "Plus facile : vrai ou faux", "قول واش هاد الجمل صحيحة ولا غالطة.",
      "La courbe n(I₂)(t) de la figure 1.",
      [("La transformation est lente : n(I₂) augmente pendant plusieurs dizaines de minutes.", True, "On suit son évolution : on distingue les états intermédiaires."),
       ("D'après le tableau d'avancement, n(I₂) = 2x.", False, "Le coefficient de I₂ est 1 : n(I₂) = x."),
       ("La valeur finale de n(I₂) est égale à x_max = 2,0 mmol.", True, "n(I₂) = x et, à la fin, x = x_max.")]),
    qcm_facile("fa_tl3_6", "Plus facile : n(I⁻) à t = 10 min", "سؤال ساهل على السطر ديال en cours.",
      "À t = 10 min, x = 1,4 mmol et n₀(I⁻) = 10 mmol. La quantité d'ions iodure restante vaut…",
      ["8,6 mmol", "1,4 mmol", "7,2 mmol"], 2, {
        "2": {"juste": rep("برافو! dix moins deux fois un virgule quatre، égale sept virgule deux millimoles.", "Juste : 10 − 2 × 1,4 = 7,2 mmol.")},
        "0": {"1": rep("قريب. huit virgule six égale dix moins un virgule quatre. ولكن le coefficient ديال les ions iodure شحال؟ عاود اختار.", "8,6 = 10 − 1,4. Quel est le coefficient de I⁻ ? Réessaie."),
              "2": rep("الجواب: sept virgule deux millimoles. le coefficient ديال les ions iodure égale deux: dix moins deux x.", "Réponse : 7,2 mmol ; n(I⁻) = 10 − 2x (coefficient 2).")},
        "1": {"1": rep("un virgule quatre هي x، يعني la quantité ديال le diiode. والسؤال على les ions iodure. عاود اختار.", "1,4 mmol, c'est x = n(I₂). On demande n(I⁻). Réessaie."),
              "2": rep("الجواب: n de I moins égale dix moins deux x، égale sept virgule deux millimoles.", "Réponse : n(I⁻) = 10 − 2x = 7,2 mmol.")}},
      "À dix minutes، x égale un virgule quatre millimoles. La quantité d'ions iodure restante vaut ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "À t = 0, on mélange à 20 °C V₁ = 50 mL d'une solution de peroxodisulfate de potassium de concentration C₁ = 3,0·10⁻² mol/L et V₂ = 50 mL d'une solution d'iodure de potassium de concentration C₂ = 0,10 mol/L. On suit la quantité de diiode formé (figure 1).",
      "intro_dit": "نفس التمرين، بمعطيات أخرى. V un égale cinquante millilitres، و C un égale trois fois dix puissance moins deux mole par litre. V deux égale cinquante millilitres، و C deux égale zéro virgule un mole par litre.",
      "figures": [courbe(XMb, "Figure 1 : la quantité de diiode n(I₂) en fonction du temps")],
      "donnees": ["V₁ = 50 mL ; C₁ = 3,0·10⁻² mol/L", "V₂ = 50 mL ; C₂ = 0,10 mol/L", "Couples : S₂O₈²⁻(aq)/SO₄²⁻(aq) et I₂(aq)/I⁻(aq)"],
      "questions": [
        question_semblable("1", "Écrire la demi-équation électronique de chacun des deux couples.",
          phrase("S₂O₈²⁻(aq) + 2e⁻ ⇌ 2SO₄²⁻(aq) ; I₂(aq) + 2e⁻ ⇌ 2I⁻(aq)"), ["Ox + n e⁻ ⇌ Red", "2e⁻"], ["S₂O₈²⁻(aq) ⇌ 2SO₄²⁻(aq) + 2e⁻"],
          corr([("1 : S₂O₈²⁻(aq) + 2e⁻ ⇌ 2SO₄²⁻(aq) ; I₂(aq) + 2e⁻ ⇌ 2I⁻(aq)", "ion peroxodisulfate plus deux électrons")],
               "ion peroxodisulfate plus deux électrons donne deux ions sulfate. diiode plus deux électrons donne deux ions iodure.")),
        question_semblable("2", "Montrer que l'équation de la réaction s'écrit : " + EQ + ".",
          phrase("Réduction S₂O₈²⁻(aq) + 2e⁻ → 2SO₄²⁻(aq) ; oxydation 2I⁻(aq) → I₂(aq) + 2e⁻ ; somme : " + EQ + " ; charges −4 = −4."),
          ["réduction", "oxydation", "charges"], ["S₂O₈²⁻(aq) + 2I⁻(aq) + 2e⁻ → …"],
          corr([("2 : réduction + oxydation (2e⁻ chacune) : " + EQ, "كنجمعو")],
               "la réduction ديال l'ion peroxodisulfate، و l'oxydation ديال les ions iodure، avec deux électrons: كنجمعو، و les électrons كيمشيو.")),
        question_semblable("3", "Calculer, en mmol, les quantités de matière initiales n₀(S₂O₈²⁻) et n₀(I⁻).",
          valeur("n₀(I⁻)", 5.0, "mmol", "n₀(S₂O₈²⁻) = C₁·V₁ = 3,0·10⁻² × 0,050 = 1,5 mmol ; n₀(I⁻) = C₂·V₂ = 0,10 × 0,050 = 5,0 mmol"),
          ["n = C·V", "0,050 L", "mmol"], ["n = C·(V₁ + V₂)"],
          corr([("3 : n₀(S₂O₈²⁻) = 3,0·10⁻² × 0,050 = 1,5 mmol", "un virgule cinq millimoles"), ("n₀(I⁻) = 0,10 × 0,050 = 5,0 mmol", "cinq millimoles")],
               "n zéro égale C fois V. les ions peroxodisulfate: un virgule cinq millimoles. les ions iodure: cinq millimoles.")),
        question_semblable("4", "Dresser le tableau d'avancement. Déterminer x_max et le réactif limitant.",
          valeur("x_max", 1.5, "mmol", "1,5 − x_max = 0 ⇒ 1,5 mmol ; 5,0 − 2x_max = 0 ⇒ 2,5 mmol ; S₂O₈²⁻ limitant : x_max = 1,5 mmol"),
          ["n₀ − x", "n₀ − 2x", "x_max"], ["x_max = 2,5 mmol"],
          corr([("4 : 1,5 − x_max = 0 : 1,5 mmol ; 5,0 − 2x_max = 0 : 2,5 mmol", "un virgule cinq et deux virgule cinq"), ("x_max = 1,5 mmol ; S₂O₈²⁻ limitant", "x max égale un virgule cinq millimoles")],
               "les deux valeurs: un virgule cinq et deux virgule cinq millimoles. x max égale un virgule cinq millimoles، و l'ion peroxodisulfate هو le réactif limitant.")),
        question_semblable("5", "Justifier que la transformation est lente. Quelle relation lie n(I₂) à x ? Lire n(I₂) final et le comparer à x_max.",
          valeur("n(I₂)f", 1.5, "mmol", "n(I₂) croît pendant environ 40 min : lente ; n(I₂) = x, donc n(I₂)f = x_max = 1,5 mmol"),
          ["lente", "n(I₂) = x", "x_max"], ["n(I₂) = 2x"],
          corr([("5 : évolution visible pendant ≈ 40 min : lente ; n(I₂) = x", "lente"), ("n(I₂)f = x_max = 1,5 mmol", "un virgule cinq millimoles")],
               "n de I deux كتطلع خلال environ quarante minutes: lente. n de I deux égale x، إذن فالأخير égale x max، un virgule cinq millimoles.")),
        question_semblable("6", "Lire n(I₂) à la date t = 10 min. En déduire, en mmol, la quantité d'ions iodure restant à cette date.",
          valeur("n(I⁻)", 2.8, "mmol", "x(10 min) = n(I₂) ≈ 1,1 mmol ; n(I⁻) = 5,0 − 2 × 1,1 = 2,8 mmol", tol=0.05),
          ["x = n(I₂)", "n(I⁻) = n₀(I⁻) − 2x"], ["n(I⁻) = 5,0 − 1,1"],
          corr([("6 : à 10 min, x = n(I₂) ≈ 1,1 mmol", "un virgule un millimole"), ("n(I⁻) = 5,0 − 2 × 1,1 ≈ 2,8 mmol", "deux virgule huit millimoles")],
               "à dix minutes، x environ un virgule un millimole. n de I moins égale cinq moins deux fois un virgule un، environ deux virgule huit millimoles.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
