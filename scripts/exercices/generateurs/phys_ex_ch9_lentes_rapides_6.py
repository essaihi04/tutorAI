# Exercice de chimie (physique-chimie), ch. 9 « Transformations lentes et transformations rapides », niveau difficile n° 6 :
# arrêter la transformation pour la doser — trempe, titrage rapide du diiode, avancement à un instant, lecture critique.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture phys_ch9_transformations_lentes_rapides.md (tl_t1_trempe,
#    tl_r7_titrage « une réaction de titrage doit être rapide », tl_np9), sources_chimie_ch9_ch11.md (Bendaoud, Sbiro :
#    eau glacée = trempe ; El Goufifa : S₂O₈²⁻ + I⁻, prélèvements dans l'eau froide puis dosage par le thiosulfate) ;
#  - le cours phys_ch9 (tl_t1_trempe, tl_r7_titrage, tl_t3_catalyseur pour l'équation, tl_rp5, tl_np5, tl_np6) ;
#  - nationaux : 2017 R (« objectif de l'eau glacée avant le dosage »), 2018 N (deux facteurs cinétiques) ; ici deux notions
#    combinées (trempe + tableau d'avancement) et une lecture critique d'un résultat ; ni vitesse ni t½ (ch. 10) ;
#  - séries en ligne : recherche faite (talamidi, moutamadris, dreamjob, alloschool) ; PDF non ouverts (hôtes hors du réseau
#    autorisé de la session).
#  La relation d'équivalence est donnée dans l'énoncé (proportions de l'équation), comme au national.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch9_lentes_rapides_6"
SIM = "/media/simulations/chimie/transformations-lentes-rapides-tableau/"
EQ = "S₂O₈²⁻(aq) + 2I⁻(aq) → 2SO₄²⁻(aq) + I₂(aq)"
EQT = "I₂(aq) + 2S₂O₃²⁻(aq) → 2I⁻(aq) + S₄O₆²⁻(aq)"


def r(v, n=12):
    return round(v, n)


def calc(C1, V1, C2, V2, V, V0, Cp, VE):
    n1, n2 = r(C1 * V1 * 1e3), r(C2 * V2 * 1e3)             # mmol
    xm = min(n1, n2 / 2)
    npI2 = r(Cp * VE / 2)                                       # mol dans le prélèvement
    x = r(npI2 * V / V0 * 1e3)                                  # mmol dans le mélange
    VEmax = r(2 * (xm * 1e-3 * V0 / V) / Cp * 1e3)              # mL
    return n1, n2, xm, npI2, x, VEmax


A = calc(2.0e-2, 0.050, 0.10, 0.050, 0.100, 0.010, 1.0e-2, 8.0e-3)
assert A == (1.0, 5.0, 1.0, 4.0e-5, 0.4, 20.0), A
B = calc(3.0e-2, 0.050, 0.20, 0.050, 0.100, 0.010, 2.0e-2, 9.0e-3)
assert B == (1.5, 10.0, 1.5, 9.0e-5, 0.9, 15.0), B


def protocole(titre, t1, legende):
    """Le mélange → prélèvement de 10 mL à t₁ → eau glacée → titrage par le thiosulfate."""
    g = []
    g += fil([0.5, 3.6], [0.5, 1.0], [3.5, 1.0], [3.5, 3.6])
    g += [{"f": "ligne", "pts": [[0.5, 3.0], [3.5, 3.0]], "couleur": "orange", "trait": "pointille"}]
    g += texte([2.0, 0.4], "mélange (100 mL)") + texte([2.0, 2.0], "brunit", couleur="orange")
    g += [{"f": "fleche", "de": [3.8, 2.4], "a": [5.4, 2.4], "texte": f"10 mL à t₁ = {t1} min", "pos": "n"}]
    g += fil([5.7, 3.6], [5.7, 1.0], [8.3, 1.0], [8.3, 3.6])
    g += [{"f": "ligne", "pts": [[5.7, 3.0], [8.3, 3.0]], "couleur": "cyan", "trait": "pointille"}]
    g += [{"f": "rect", "de": [6.1, 1.3], "a": [6.6, 1.8], "couleur": "cyan"}, {"f": "rect", "de": [7.3, 1.5], "a": [7.8, 2.0], "couleur": "cyan"}]
    g += texte([7.0, 0.4], "eau glacée", couleur="cyan")
    g += [{"f": "fleche", "de": [8.6, 2.4], "a": [9.8, 2.4]}]
    g += fil([10.2, 3.0], [10.2, 1.0], [12.4, 1.0], [12.4, 3.0])
    g += [{"f": "rect", "de": [11.05, 3.7], "a": [11.55, 6.0]}] + fil([11.3, 3.7], [11.3, 3.2])
    g += texte([11.3, 0.4], "titrage") + texte([11.8, 6.3], "S₂O₃²⁻(aq), C'", ancre="centre")
    return schema(titre, 13, 6.8, g, legende=legende)


EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "transformations_lentes_rapides", "cours": "phys_ch9_transformations_lentes_rapides",
  "titre": "Figer pour doser : trempe, titrage du diiode et avancement", "niveau": "difficile", "duree_min": 40,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Établir l'équation d'oxydoréduction et déterminer x_max", "Expliquer la trempe par les facteurs cinétiques",
                  "Exploiter un titrage rapide pour obtenir l'avancement à un instant", "Juger un résultat expérimental à l'aide de x_max"],
  "enonce": {
    "intro": "À t = 0, on mélange V₁ = 50 mL d'une solution de peroxodisulfate de potassium (C₁ = 2,0·10⁻² mol/L en ions S₂O₈²⁻(aq)) et V₂ = 50 mL d'une solution d'iodure de potassium (C₂ = 0,10 mol/L en ions I⁻(aq)) ; le volume du mélange est V = 100 mL. La transformation, lente, forme du diiode I₂(aq). À la date t₁ = 10 min, on prélève V₀ = 10,0 mL du mélange, on le verse aussitôt dans de l'eau glacée, puis on titre le diiode de ce prélèvement par une solution de thiosulfate de sodium de concentration C' = 1,0·10⁻² mol/L (figure 1). L'équivalence est obtenue pour V_E = 8,0 mL.",
    "intro_dit": "نقراو l'énoncé. فt égale zéro، كنخلطو V un égale cinquante millilitres ديال le peroxodisulfate de potassium، C un égale deux fois dix puissance moins deux mole par litre، مع V deux égale cinquante millilitres ديال l'iodure de potassium، C deux égale zéro virgule un mole par litre. le volume ديال le mélange، V égale cent millilitres. la transformation lente، وكيتكون le diiode. à t un égale dix minutes، كناخدو V zéro égale dix millilitres من le mélange، كنخويوه دغيا ف l'eau glacée، ومن بعد كنديرو le titrage ديال le diiode ب le thiosulfate de sodium، C prime égale un fois dix puissance moins deux mole par litre. l'équivalence كتكون ف V E égale huit millilitres.",
    "figures": [protocole("Figure 1 : prélèvement, trempe, titrage", 10, "Le titrage du diiode par les ions thiosulfate est une réaction rapide.")],
    "donnees": ["Couples : S₂O₈²⁻(aq)/SO₄²⁻(aq) ; I₂(aq)/I⁻(aq) ; S₄O₆²⁻(aq)/S₂O₃²⁻(aq)",
                "Réaction de titrage (rapide) : " + EQT,
                "À l'équivalence, les réactifs du titrage ont été mélangés dans les proportions de l'équation de titrage.",
                "V₁ = V₂ = 50 mL ; V = 100 mL ; V₀ = 10,0 mL ; C' = 1,0·10⁻² mol/L ; V_E = 8,0 mL"],
    "questions": [
      question("1", "Établir, à partir des demi-équations des couples S₂O₈²⁻(aq)/SO₄²⁻(aq) et I₂(aq)/I⁻(aq), l'équation de la réaction étudiée.",
        "السؤال un: من les demi-équations ديال les deux couples، استنتج l'équation ديال la réaction.",
        phrase("S₂O₈²⁻(aq) + 2e⁻ → 2SO₄²⁻(aq) (réduction) ; 2I⁻(aq) → I₂(aq) + 2e⁻ (oxydation) ; 2 électrons de chaque côté, on additionne : " + EQ + " ; charges −4 = −4."),
        ["2e⁻", "réduction", "oxydation", "→", "charges"], ["S₂O₈²⁻(aq) + I⁻(aq) → SO₄²⁻(aq) + I₂(aq)", "I₂(aq) + 2SO₄²⁻(aq) → …"],
        [aide("Quel réactif capte les électrons, lequel les cède ? Écris les deux demi-équations dans le sens de la réaction.",
              "شكون كيشد les électrons، وشكون كيعطيهم؟ كتب les deux demi-équations فالاتجاه ديال la réaction."),
         aide("S₂O₈²⁻ + 2e⁻ → 2SO₄²⁻ et 2I⁻ → I₂ + 2e⁻ : même nombre d'électrons, on additionne ; vérifie les charges.",
              "ion peroxodisulfate plus deux électrons donne deux ions sulfate، et deux ions iodure donne diiode plus deux électrons. نفس العدد، جمع، وتأكد من les charges.")],
        corr([("1 : S₂O₈²⁻(aq) + 2e⁻ → 2SO₄²⁻(aq) ; 2I⁻(aq) → I₂(aq) + 2e⁻", "les deux demi-équations"),
              (EQ + " ; charges −4 = −4", "ion peroxodisulfate plus deux ions iodure")],
             "السؤال un. la réduction: ion peroxodisulfate plus deux électrons donne deux ions sulfate. l'oxydation: deux ions iodure donne diiode plus deux électrons. نكتبو les deux demi-équations، و les électrons متساويين، كنجمعو: ion peroxodisulfate plus deux ions iodure، donne deux ions sulfate plus diiode. les charges: moins quatre من كل جهة."),
        "ex_tl6_1", "fa_tl6_1"),
      question("2", "Calculer les quantités initiales des réactifs, puis déterminer, à l'aide d'un tableau d'avancement, l'avancement maximal x_max (en mmol) et le réactif limitant.",
        "السؤال deux: حسب les quantités initiales ديال les réactifs، ومن بعد ب le tableau d'avancement لقا x max ب millimole و le réactif limitant.",
        valeur("x_max", 1.0, "mmol", "n₀(S₂O₈²⁻) = 2,0·10⁻² × 0,050 = 1,0 mmol ; n₀(I⁻) = 0,10 × 0,050 = 5,0 mmol ; 1,0 − x_max = 0 ⇒ 1,0 mmol ; 5,0 − 2x_max = 0 ⇒ 2,5 mmol ; S₂O₈²⁻ limitant : x_max = 1,0 mmol"),
        ["n = C·V", "n₀ − x", "n₀ − 2x", "x_max", "réactif limitant"], ["x_max = 2,5 mmol", "x_max = 5,0 mmol"],
        [aide("n = C·V pour chaque solution (V en litres). Puis ligne « en cours » : 1,0 − x pour S₂O₈²⁻ et 5,0 − 2x pour I⁻.",
              "n égale C fois V لكل solution، و V بالlitre. ومن بعد السطر ديال en cours: un moins x ل l'ion peroxodisulfate، et cinq moins deux x ل les ions iodure."),
         aide("Chaque réactif donne une valeur de x qui l'épuise ; x_max est la plus petite.",
              "كل réactif كيعطي x اللي كيخليه يسالي. x max هي القيمة الصغيرة.")],
        corr([("2 : n₀(S₂O₈²⁻) = C₁·V₁ = 1,0 mmol ; n₀(I⁻) = C₂·V₂ = 5,0 mmol", "un millimole et cinq millimoles"),
              ("1,0 − x_max = 0 ⇒ 1,0 mmol ; 5,0 − 2x_max = 0 ⇒ 2,5 mmol", "un millimole et deux virgule cinq millimoles"),
              ("x_max = 1,0 mmol ; S₂O₈²⁻ est le réactif limitant.", "x max égale un millimole")],
             "السؤال deux. n zéro ديال l'ion peroxodisulfate: deux fois dix puissance moins deux، fois zéro virgule zéro cinq، égale un millimole. les ions iodure: zéro virgule un fois zéro virgule zéro cinq، égale cinq millimoles. ناخدو un millimole et cinq millimoles ف le tableau. un moins x max égale zéro، donne un millimole. cinq moins deux x max égale zéro، donne deux virgule cinq millimoles. نختارو un millimole et deux virgule cinq millimoles، الصغيرة: x max égale un millimole، و l'ion peroxodisulfate هو le réactif limitant."),
        "ex_tl6_2", "fa_tl6_2"),
      question("3", "Expliquer le rôle de l'eau glacée et nommer les deux facteurs cinétiques mis en jeu. Pourquoi la réaction de titrage doit-elle être rapide ?",
        "السؤال trois: شرح الدور ديال l'eau glacée، وسمي les deux facteurs cinétiques. وعلاش la réaction de titrage خاصها تكون rapide؟",
        phrase("L'eau glacée réalise une trempe : la température baisse brusquement et la dilution diminue les concentrations des réactifs. La transformation devient très lente : elle est pratiquement bloquée, et la quantité de diiode du prélèvement est celle de la date t₁. Facteurs : la température et la concentration des réactifs. La réaction de titrage doit être rapide pour que chaque goutte réagisse aussitôt et que l'équivalence soit repérée avec précision (disparition de la couleur du diiode)."),
        ["trempe", "température", "concentration", "dilution", "bloquer", "rapide"], ["l'eau glacée détruit le diiode", "un catalyseur"],
        [aide("Deux choses changent quand on verse le prélèvement dans beaucoup d'eau glacée : lesquelles ? Que deviennent-elles pour la vitesse de la transformation ?",
              "جوج حوايج كيتبدلو ملي كنخويو le prélèvement ف l'eau glacée: شنو هوما؟ وشنو كيدير هادشي ل la transformation؟"),
         aide("Froid : la température baisse ; dilution : les concentrations baissent. Ce sont deux facteurs cinétiques : la transformation est pratiquement bloquée, c'est la trempe. Pour le titrage, pense à l'équivalence : il faut voir le moment exact où la couleur disparaît.",
              "البرد كينقص la température، والما كينقص les concentrations: deux facteurs cinétiques. la transformation كتولي très lente، هادي la trempe. و ف le titrage، خاصنا نشوفو بالضبط فوقاش اللون كيمشي، هادي l'équivalence.")],
        corr([("3 : l'eau glacée réalise une trempe : baisse de la température et dilution (baisse des concentrations).", "هادي la trempe"),
              ("Deux facteurs cinétiques : température et concentration ; la transformation est pratiquement bloquée : on dose n(I₂) à la date t₁.", "la température et la concentration"),
              ("Titrage rapide : chaque goutte réagit aussitôt, l'équivalence est repérée avec précision.", "une réaction de titrage، doit être rapide")],
             "السؤال trois. l'eau glacée كتدير la trempe: la température كتهبط دقة وحدة، والما كينقص les concentrations. هادو deux facteurs cinétiques: la température et la concentration. la transformation كتولي très lente، تقريبا محبوسة، إذن كنقيسو la quantité ديال le diiode ديال t un. و une réaction de titrage، doit être rapide: كل نقطة كتفاعل فلحظة، ونشوفو بالضبط l'équivalence."),
        "ex_tl6_3", "fa_tl6_3"),
      question("4", "Montrer que la quantité de diiode dans le prélèvement s'écrit n_p(I₂) = C'·V_E / 2. La calculer.",
        "السؤال quatre: بين بلي la quantité ديال le diiode ف le prélèvement هي C prime fois V E sur deux. ومن بعد حسبها.",
        valeur("n_p(I₂)", 4.0e-5, "mol", "À l'équivalence, n(S₂O₃²⁻) versé = 2·n_p(I₂), donc n_p(I₂) = C'·V_E/2 = 1,0·10⁻² × 8,0·10⁻³ / 2 = 4,0·10⁻⁵ mol"),
        ["n(S₂O₃²⁻) = C'·V_E", "proportions de l'équation", "÷ 2", "8,0·10⁻³ L"], ["n_p(I₂) = C'·V_E", "n_p(I₂) = 2C'·V_E", "V_E = 8,0 L"],
        [aide("D'après l'équation de titrage, combien d'ions thiosulfate réagissent avec une mole de diiode ? À l'équivalence, combien en a-t-on versé ?",
              "من l'équation de titrage: شحال من ion thiosulfate كيتفاعل مع mole ديال le diiode؟ و ف l'équivalence، شحال صبينا؟"),
         aide("Proportions de l'équation : n(S₂O₃²⁻) = 2·n_p(I₂), avec n(S₂O₃²⁻) = C'·V_E (V_E en litres).",
              "حسب l'équation: n ديال le thiosulfate égale deux fois n ديال le diiode، و n ديال le thiosulfate égale C prime fois V E، و V E بالlitre.")],
        corr([("4 : I₂ + 2S₂O₃²⁻ → … : à l'équivalence n(S₂O₃²⁻) = 2·n_p(I₂)", "deux fois n ديال le diiode"),
              ("n(S₂O₃²⁻) = C'·V_E, donc n_p(I₂) = C'·V_E / 2", "C prime fois V E sur deux"),
              ("A.N. : n_p(I₂) = 1,0·10⁻² × 8,0·10⁻³ / 2 = 4,0·10⁻⁵ mol", "quatre fois dix puissance moins cinq mole")],
             "السؤال quatre. ف l'équation de titrage، une mole de diiode كتفاعل مع deux moles de thiosulfate. ف l'équivalence، n ديال le thiosulfate égale deux fois n ديال le diiode. و n ديال le thiosulfate égale C prime fois V E. إذن n ديال le diiode égale C prime fois V E sur deux. l'application numérique: un fois dix puissance moins deux، fois huit fois dix puissance moins trois، sur deux، égale quatre fois dix puissance moins cinq mole."),
        "ex_tl6_4", "fa_tl6_4"),
      question("5", "En déduire l'avancement x(t₁) de la réaction dans le mélange (en mmol). Comparer à x_max et conclure.",
        "السؤال cinq: استنتج l'avancement x ديال t un ف le mélange كامل، ب millimole. قارنو مع x max، واستنتج.",
        valeur("x(t₁)", 0.40, "mmol", "n(I₂) = x ; le mélange (100 mL) contient 10 fois le prélèvement (10 mL) : x(t₁) = 10 × 4,0·10⁻⁵ = 4,0·10⁻⁴ mol = 0,40 mmol"),
        ["n(I₂) = x", "V / V₀ = 10", "x / x_max", "mmol"], ["x(t₁) = 4,0·10⁻⁵ mol", "x(t₁) = 0,040 mmol"],
        [aide("Le prélèvement n'est qu'une partie du mélange : V₀ = 10 mL sur V = 100 mL. Le diiode est réparti de la même façon dans tout le mélange.",
              "le prélèvement غير جزء من le mélange: dix millilitres من cent millilitres. و le diiode موزع بنفس الطريقة ف le mélange كامل."),
         aide("n(I₂) dans le mélange = n_p(I₂) × V/V₀ ; et n(I₂) = x d'après le tableau. Calcule ensuite x/x_max.",
              "n ديال le diiode ف le mélange égale n p fois V sur V zéro. و n ديال le diiode égale x. ومن بعد حسب x sur x max.")],
        corr([("5 : n(I₂) = x et le mélange contient V/V₀ = 10 prélèvements", "dix fois le prélèvement"),
              ("x(t₁) = 10 × 4,0·10⁻⁵ = 4,0·10⁻⁴ mol = 0,40 mmol", "zéro virgule quatre millimole"),
              ("x(t₁)/x_max = 0,40/1,0 = 0,40 : à t₁, la transformation n'est pas terminée (lente).", "la transformation ما سالاتش")],
             "السؤال cinq. n ديال le diiode égale x، و le mélange فيه dix fois le prélèvement. x de t un égale dix fois quatre fois dix puissance moins cinq، égale quatre fois dix puissance moins quatre mole، يعني zéro virgule quatre millimole. x max égale un millimole: x sur x max égale zéro virgule quatre. إذن à dix minutes، la transformation ما سالاتش: هي lente."),
        "ex_tl6_5", "fa_tl6_5"),
      question("6", "Un élève annonce, pour un prélèvement de 10,0 mL fait à t = 60 min et titré de la même façon, un volume équivalent V_E = 25 mL. Calculer le volume équivalent maximal possible (en mL) et juger ce résultat.",
        "السؤال six: تلميذ قال: prélèvement ديال dix millilitres à soixante minutes، و V E égale vingt-cinq millilitres. حسب V E maximal الممكن ب millilitre، وقول واش هاد النتيجة معقولة.",
        valeur("V_E,max", 20.0, "mL", "n_p,max(I₂) = x_max × V₀/V = 1,0·10⁻³ / 10 = 1,0·10⁻⁴ mol ; V_E,max = 2·n_p,max / C' = 2 × 1,0·10⁻⁴ / 1,0·10⁻² = 2,0·10⁻² L = 20 mL"),
        ["x_max", "V₀ / V", "V_E = 2·n_p / C'", "mL"], ["V_E,max = 10 mL", "V_E,max = 200 mL"],
        [aide("Le diiode ne peut jamais dépasser sa valeur finale : n(I₂) ≤ x_max dans le mélange. Combien au plus dans 10 mL ?",
              "le diiode ما يمكنش يفوت la valeur النهائية ديالو: n ديال le diiode أصغر ولا égale x max. شحال على الأكثر ف dix millilitres؟"),
         aide("n_p,max = x_max/10 ; puis V_E,max = 2·n_p,max / C' (en L, puis en mL). Compare à 25 mL.",
              "n p max égale x max sur dix. ومن بعد V E max égale deux fois n p max sur C prime، بالlitre ومن بعد ب millilitre. قارن مع vingt-cinq millilitres.")],
        corr([("6 : n(I₂) ≤ x_max, donc n_p(I₂) ≤ x_max·V₀/V = 1,0·10⁻⁴ mol", "un fois dix puissance moins quatre mole"),
              ("V_E,max = 2 × 1,0·10⁻⁴ / 1,0·10⁻² = 2,0·10⁻² L = 20 mL", "vingt millilitres"),
              ("25 mL > 20 mL : le résultat est impossible (erreur de mesure ou de calcul).", "النتيجة ديال التلميذ غالطة")],
             "السؤال six. le diiode ما يمكنش يفوت x max. ف dix millilitres، على الأكثر x max sur dix، يعني un fois dix puissance moins quatre mole. V E max égale deux fois un fois dix puissance moins quatre، sur un fois dix puissance moins deux، égale deux fois dix puissance moins deux litre، يعني vingt millilitres. vingt-cinq millilitres أكبر من vingt millilitres: النتيجة ديال التلميذ غالطة، ما يمكنش."),
        "ex_tl6_6", "fa_tl6_6"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_tl6_1", "Question 1 : l'équation S₂O₈²⁻ + 2I⁻", "Deux électrons captés, deux électrons cédés : on additionne.",
      SIM + "facteurs.html?vue=catalyseur", "Le mélange des ions peroxodisulfate et iodure, puis son équation",
      "شوف هاد les béchers: نفس le mélange ديال التمرين، les ions peroxodisulfate و les ions iodure، بلا لون فالبداية. l'ion peroxodisulfate capte deux électrons: la réduction. les ions iodure cèdent deux électrons: l'oxydation. نفس العدد، كنجمعو. l'équation: ion peroxodisulfate plus deux ions iodure، donne deux ions sulfate plus diiode.",
      centre=[(EQ, "l'équation: ion peroxodisulfate plus deux ions iodure")],
      pointage=[{"mot": "شوف هاد les béchers", "commande": "play_until", "parametres": {"moment": "melange"}},
                {"mot": "شوف هاد les béchers", "repere": "becher_sans"},
                {"mot": "l'équation: ion peroxodisulfate plus deux ions iodure", "commande": "play_until", "parametres": {"moment": "equation"}},
                {"mot": "l'équation: ion peroxodisulfate plus deux ions iodure", "repere": "equation"},
                {"mot": "l'équation: ion peroxodisulfate plus deux ions iodure", "cible": "centre:0"}]),
    diapo_sim("ex_tl6_2", "Question 2 : x_max", "On calcule n₀ = C·V, puis chaque réactif donne sa valeur de x ; on garde la plus petite.",
      SIM + "national-pas-a-pas.html?sujet=iodure&etape=5", "La méthode du tableau d'avancement",
      "شوف le tableau d'avancement ديال le cours. السطر ديال en cours، ومن بعد كل réactif: فوقاش كيسالي؟ ومن بعد القيمة الصغيرة هي x max. فالتمرين ديالنا: un millimole ديال l'ion peroxodisulfate، et cinq millimoles ديال les ions iodure. un moins x max égale zéro، donne un millimole. cinq moins deux x max égale zéro، donne deux virgule cinq millimoles. x max égale un millimole، و l'ion peroxodisulfate هو le réactif limitant.",
      centre=[("x_max = 1,0 mmol : S₂O₈²⁻ limitant", "x max égale un millimole")],
      pointage=[{"mot": "شوف le tableau d'avancement", "commande": "play_until", "parametres": {"moment": "rappel"}},
                {"mot": "شوف le tableau d'avancement", "repere": "tableau"},
                {"mot": "فوقاش كيسالي؟", "commande": "play_until", "parametres": {"moment": "question"}},
                {"mot": "ومن بعد القيمة الصغيرة", "commande": "play_until", "parametres": {"moment": "correction"}},
                {"mot": "x max égale un millimole", "cible": "centre:0"}]),
    diapo_sim("ex_tl6_3", "Question 3 : la trempe", "Froid et dilution : deux facteurs cinétiques qui figent le prélèvement.",
      SIM + "facteurs.html?vue=trempe", "Le grand bécher, le prélèvement à la pipette, l'eau glacée, puis le titrage",
      "شوف le grand bécher: كيولي brun بشوية بشوية. ب la pipette، كناخدو شوية من le mélange، وكنخويوه ف bécher فيه الما بارد بزاف. شوف هاد الشوية: اللون ديالو ما بقاش كيتبدل. وفنفس الوقت، le grand bécher باقي كيزيد يولي brun. البرد، والما اللي زدنا: la température et la concentration، deux facteurs cinétiques. la transformation كتولي très lente: هادي هي la trempe. من بعد كنديرو le titrage ب les ions thiosulfate. une réaction de titrage، doit être rapide: كل نقطة كتفاعل فلحظة، ونشوفو بالضبط l'équivalence.",
      centre=[("Trempe : θ ↓ et dilution ⇒ transformation pratiquement bloquée", "هادي هي la trempe"), ("Titrage rapide : équivalence précise", "une réaction de titrage، doit être rapide")],
      pointage=[{"mot": "شوف le grand bécher", "commande": "play_until", "parametres": {"moment": "reaction"}},
                {"mot": "شوف le grand bécher", "repere": "grand_becher"},
                {"mot": "ب la pipette", "commande": "play_until", "parametres": {"moment": "prelevement"}},
                {"mot": "ب la pipette", "repere": "pipette"},
                {"mot": "وكنخويوه ف bécher", "commande": "play_until", "parametres": {"moment": "eau_glacee"}},
                {"mot": "شوف هاد الشوية", "commande": "play_until", "parametres": {"moment": "fige"}},
                {"mot": "le grand bécher باقي كيزيد", "commande": "play_until", "parametres": {"moment": "continue"}},
                {"mot": "هادي هي la trempe", "cible": "centre:0"},
                {"mot": "من بعد كنديرو le titrage", "commande": "play_until", "parametres": {"moment": "titrage"}},
                {"mot": "من بعد كنديرو le titrage", "repere": "burette"},
                {"mot": "une réaction de titrage، doit être rapide", "cible": "centre:1"}]),
    diapo_sim("ex_tl6_4", "Question 4 : n_p(I₂) = C'·V_E / 2", "Une mole de diiode réagit avec deux moles d'ions thiosulfate.",
      SIM + "facteurs.html?vue=trempe", "Le titrage du diiode du prélèvement par les ions thiosulfate",
      "شوف le titrage: la burette فيها les ions thiosulfate. diiode plus deux ions thiosulfate، donne deux ions iodure plus ion tétrathionate. كل نقطة كتفاعل فلحظة، و فl'équivalence اللون ديال le diiode كيمشي. فهاد اللحظة، les réactifs dans les proportions de l'équation: n ديال le thiosulfate égale deux fois n ديال le diiode. و n ديال le thiosulfate égale C prime fois V E. إذن n ديال le diiode égale C prime fois V E sur deux. فالتمرين: un fois dix puissance moins deux، fois huit fois dix puissance moins trois، sur deux، égale quatre fois dix puissance moins cinq mole.",
      centre=[(EQT, "diiode plus deux ions thiosulfate"), ("n_p(I₂) = C'·V_E / 2 = 4,0·10⁻⁵ mol", "égale quatre fois dix puissance moins cinq mole")],
      pointage=[{"mot": "شوف le titrage", "commande": "play_until", "parametres": {"moment": "titrage"}},
                {"mot": "شوف le titrage", "repere": "burette"},
                {"mot": "diiode plus deux ions thiosulfate", "cible": "centre:0"},
                {"mot": "égale quatre fois dix puissance moins cinq mole", "cible": "centre:1"}]),
    diapo_sim("ex_tl6_5", "Question 5 : du prélèvement au mélange", "n(I₂) = x ; le mélange contient dix fois le prélèvement.",
      SIM + "national-pas-a-pas.html?sujet=iodure&etape=6", "La courbe n(I₂)(t) et le tableau : n(I₂) = x",
      "شوف la courbe ديال le diiode مع الوقت. ف le tableau، n de I deux égale x. فالتمرين ديالنا، le prélèvement فيه dix millilitres، و le mélange فيه cent millilitres: dix fois plus. إذن x de t un égale dix fois quatre fois dix puissance moins cinq، égale zéro virgule quatre millimole. x max égale un millimole: la courbe à dix minutes باقا ما وصلاتش ل la valeur النهائية. la transformation باقا خدامة، هي lente.",
      centre=[("n(I₂) = x", "n de I deux égale x"), ("x(t₁) = 10 × 4,0·10⁻⁵ mol = 0,40 mmol < x_max", "égale zéro virgule quatre millimole")],
      pointage=[{"mot": "شوف la courbe", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "شوف la courbe", "repere": "graphe_n"},
                {"mot": "n de I deux égale x", "commande": "play_until", "parametres": {"moment": "rappel"}},
                {"mot": "n de I deux égale x", "cible": "centre:0"},
                {"mot": "égale zéro virgule quatre millimole", "cible": "centre:1"}]),
    diapo_sim("ex_tl6_6", "Question 6 : jamais au-dessus de x_max", "La courbe n(I₂) ne dépasse jamais x_max : V_E non plus.",
      SIM + "national-pas-a-pas.html?sujet=iodure&etape=6", "La courbe tend vers x_max : la valeur la plus grande possible",
      "شوف la courbe: كتطلع، ومن بعد كتقرب من x max، وما كتفوتوش أبدا. إذن ف أي لحظة، n ديال le diiode أصغر من x max. فالتمرين ديالنا: ف le mélange، على الأكثر un millimole، و ف dix millilitres، على الأكثر un fois dix puissance moins quatre mole. V E max égale deux fois un fois dix puissance moins quatre، sur un fois dix puissance moins deux، égale vingt millilitres. vingt-cinq millilitres كتفوت vingt millilitres: ما يمكنش.",
      centre=[("n(I₂) ≤ x_max", "ما كتفوتوش أبدا"), ("V_E,max = 20 mL < 25 mL : impossible", "égale vingt millilitres")],
      pointage=[{"mot": "شوف la courbe", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "ومن بعد كتقرب من x max", "commande": "play_until", "parametres": {"moment": "correction"}},
                {"mot": "ومن بعد كتقرب من x max", "repere": "asymptote"},
                {"mot": "ما كتفوتوش أبدا", "cible": "centre:0"},
                {"mot": "égale vingt millilitres", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    vrai_faux_facile("fa_tl6_1", "Plus facile : vrai ou faux", "قول واش هاد الجمل صحيحة ولا غالطة.",
      EQ,
      [("Les ions iodure I⁻ sont oxydés : ils cèdent des électrons.", True, "2I⁻ → I₂ + 2e⁻ : perte d'électrons, oxydation."),
       ("Les ions S₂O₈²⁻ sont le réducteur de la réaction.", False, "S₂O₈²⁻ capte 2 électrons : c'est l'oxydant, il est réduit en SO₄²⁻."),
       ("L'équation conserve les charges : −4 de chaque côté.", True, "−2 + 2 × (−1) = −4 et 2 × (−2) + 0 = −4.")]),
    qcm_facile("fa_tl6_2", "Plus facile : x_max", "سؤال ساهل على x max.",
      "n₀(S₂O₈²⁻) = 1,0 mmol ; n₀(I⁻) = 5,0 mmol ; S₂O₈²⁻ + 2I⁻ → 2SO₄²⁻ + I₂. x_max vaut…",
      ["2,5 mmol", "5,0 mmol", "1,0 mmol"], 2, {
        "2": {"juste": rep("برافو! un et deux virgule cinq: الصغيرة un millimole.", "Juste : 1,0 et 2,5 mmol ; la plus petite, 1,0 mmol.")},
        "0": {"1": rep("deux virgule cinq هي ديال les ions iodure. ولكن l'ion peroxodisulfate واش كيسالي قبل؟ عاود اختار.", "2,5 mmol vient de I⁻. S₂O₈²⁻ s'épuise-t-il avant ? Réessaie."),
              "2": rep("الجواب: un millimole. le réactif اللي كيسالي اللول هو اللي كيحدد x max.", "Réponse : 1,0 mmol ; le premier réactif épuisé fixe x_max.")},
        "1": {"1": rep("cinq millimoles هي n zéro ديال les ions iodure، ماشي x max. عاود اختار.", "5,0 mmol est n₀(I⁻), pas x_max. Réessaie."),
              "2": rep("الجواب: un millimole، القيمة الصغيرة بين un et deux virgule cinq.", "Réponse : 1,0 mmol (plus petite de 1,0 et 2,5).")}},
      "un millimole ديال peroxodisulfate، et cinq millimoles ديال iodure. x max vaut ?"),
    qcm_facile("fa_tl6_3", "Plus facile : l'eau glacée", "سؤال ساهل على la trempe.",
      "On verse le prélèvement dans de l'eau glacée pour…",
      ["accélérer la transformation avant le titrage", "bloquer pratiquement la transformation (froid et dilution)", "détruire le diiode formé"], 1, {
        "1": {"juste": rep("برافو! البرد والما كينقصو la température et la concentration: هادي la trempe.", "Juste : froid et dilution bloquent pratiquement la transformation : la trempe.")},
        "0": {"1": rep("فكر: البرد واش كيمشي بالزربة ولا كينقص الزربة؟ عاود اختار.", "Le froid accélère-t-il ou ralentit-il ? Réessaie."),
              "2": rep("الجواب: باش نحبسو la transformation، ماشي باش نزربوها. البرد كينقص الزربة.", "Réponse : pour la bloquer ; le froid ralentit.")},
        "2": {"1": rep("لا، الما البارد ما كيقضيش على le diiode. واش كيبدل la vitesse ديال la transformation؟ عاود اختار.", "L'eau glacée ne détruit pas I₂. Que fait-elle à la vitesse ? Réessaie."),
              "2": rep("الجواب: كتحبس la transformation، باش نقيسو le diiode اللي كان فهاديك اللحظة.", "Réponse : elle fige la transformation pour doser le diiode de cet instant.")}},
      "On verse le prélèvement dans de l'eau glacée pour ?"),
    qcm_facile("fa_tl6_4", "Plus facile : n_p(I₂)", "سؤال ساهل على l'équivalence.",
      "I₂ + 2S₂O₃²⁻ → … ; à l'équivalence, n(S₂O₃²⁻) = C'·V_E = 8,0·10⁻⁵ mol. n_p(I₂) vaut…",
      ["4,0·10⁻⁵ mol", "8,0·10⁻⁵ mol", "1,6·10⁻⁴ mol"], 0, {
        "0": {"juste": rep("برافو! n ديال le diiode égale la moitié: quatre fois dix puissance moins cinq mole.", "Juste : n(I₂) = n(S₂O₃²⁻)/2 = 4,0·10⁻⁵ mol.")},
        "1": {"1": rep("قريب. ولكن شوف le coefficient deux ديال les ions thiosulfate. عاود اختار.", "Regarde le coefficient 2 de S₂O₃²⁻. Réessaie."),
              "2": rep("الجواب: deux ions thiosulfate لكل diiode، إذن n ديال le diiode هي la moitié.", "Réponse : 2 S₂O₃²⁻ pour 1 I₂ : la moitié, 4,0·10⁻⁵ mol.")},
        "2": {"1": rep("هنا ضربتي fois deux. ولكن les ions thiosulfate هوما اللي كتر، ماشي le diiode. عاود اختار.", "Tu as multiplié par 2 ; or ce sont les S₂O₃²⁻ qui sont deux fois plus nombreux. Réessaie."),
              "2": rep("الجواب: نقسمو sur deux، ماشي fois deux.", "Réponse : on divise par 2 : 4,0·10⁻⁵ mol.")}},
      "À l'équivalence، n du thiosulfate égale huit fois dix puissance moins cinq mole. n du diiode vaut ?"),
    qcm_facile("fa_tl6_5", "Plus facile : du prélèvement au mélange", "سؤال ساهل على V sur V zéro.",
      "n_p(I₂) = 4,0·10⁻⁵ mol dans 10 mL ; le mélange fait 100 mL. x(t₁) vaut…",
      ["4,0·10⁻⁵ mol", "4,0·10⁻⁴ mol", "4,0·10⁻⁶ mol"], 1, {
        "1": {"juste": rep("برافو! le mélange فيه dix fois le prélèvement: quatre fois dix puissance moins quatre mole.", "Juste : 10 × 4,0·10⁻⁵ = 4,0·10⁻⁴ mol.")},
        "0": {"1": rep("هادي غير ديال dix millilitres. والمطلوب le mélange كامل، cent millilitres. عاود اختار.", "C'est la quantité des 10 mL seulement ; on demande les 100 mL. Réessaie."),
              "2": rep("الجواب: fois dix، حيت cent millilitres هي dix fois dix millilitres.", "Réponse : × 10, soit 4,0·10⁻⁴ mol.")},
        "2": {"1": rep("قسمتي sur dix. ولكن le mélange أكبر من le prélèvement. عاود اختار.", "Tu as divisé par 10 ; le mélange est plus grand que le prélèvement. Réessaie."),
              "2": rep("الجواب: نضربو fois dix: quatre fois dix puissance moins quatre mole.", "Réponse : on multiplie par 10 : 4,0·10⁻⁴ mol.")}},
      "quatre fois dix puissance moins cinq mole dans dix millilitres، le mélange fait cent millilitres. x vaut ?"),
    vrai_faux_facile("fa_tl6_6", "Plus facile : vrai ou faux", "قول واش هاد الجمل صحيحة ولا غالطة.",
      "x_max = 1,0 mmol dans 100 mL ; prélèvements de 10 mL ; C' = 1,0·10⁻² mol/L.",
      [("À toute date, n(I₂) dans le mélange est inférieure ou égale à x_max.", True, "n(I₂) = x et x ne dépasse jamais x_max."),
       ("Un prélèvement de 10 mL peut contenir 2,0·10⁻⁴ mol de diiode si on attend assez longtemps.", False, "Au plus x_max/10 = 1,0·10⁻⁴ mol."),
       ("Le volume équivalent ne peut pas dépasser 20 mL.", True, "V_E,max = 2 × 1,0·10⁻⁴ / 1,0·10⁻² = 2,0·10⁻² L = 20 mL.")]),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "À t = 0, on mélange V₁ = 50 mL de solution de peroxodisulfate de potassium (C₁ = 3,0·10⁻² mol/L) et V₂ = 50 mL de solution d'iodure de potassium (C₂ = 0,20 mol/L) ; V = 100 mL. À t₁ = 15 min, on prélève V₀ = 10,0 mL, on le verse dans de l'eau glacée et on titre le diiode par le thiosulfate de sodium (C' = 2,0·10⁻² mol/L) : V_E = 9,0 mL.",
      "intro_dit": "نفس التمرين، بمعطيات أخرى. C un égale trois fois dix puissance moins deux mole par litre، C deux égale zéro virgule deux mole par litre. à quinze minutes، prélèvement ديال dix millilitres، و C prime égale deux fois dix puissance moins deux mole par litre، و V E égale neuf millilitres.",
      "figures": [protocole("Figure 1 : prélèvement, trempe, titrage", 15, "Le titrage du diiode par les ions thiosulfate est une réaction rapide.")],
      "donnees": ["Réaction de titrage (rapide) : " + EQT, "V₁ = V₂ = 50 mL ; V = 100 mL ; V₀ = 10,0 mL ; C' = 2,0·10⁻² mol/L ; V_E = 9,0 mL"],
      "questions": [
        question_semblable("1", "Établir l'équation de la réaction étudiée à partir des demi-équations.",
          phrase("S₂O₈²⁻(aq) + 2e⁻ → 2SO₄²⁻(aq) ; 2I⁻(aq) → I₂(aq) + 2e⁻ ; " + EQ), ["2e⁻", "→"], ["S₂O₈²⁻(aq) + I⁻(aq) → …"],
          corr([("1 : " + EQ, "ion peroxodisulfate plus deux ions iodure")], "ion peroxodisulfate plus deux ions iodure، donne deux ions sulfate plus diiode.")),
        question_semblable("2", "Calculer les quantités initiales, puis x_max (en mmol) et le réactif limitant.",
          valeur("x_max", 1.5, "mmol", "n₀(S₂O₈²⁻) = 1,5 mmol ; n₀(I⁻) = 10 mmol ; 1,5 − x_max = 0 ⇒ 1,5 mmol ; 10 − 2x_max = 0 ⇒ 5,0 mmol ; x_max = 1,5 mmol"),
          ["n = C·V", "x_max"], ["x_max = 5,0 mmol"],
          corr([("2 : 1,5 mmol et 10 mmol ; x_max = 1,5 mmol, S₂O₈²⁻ limitant", "x max égale un virgule cinq millimole")],
               "un virgule cinq millimole et dix millimoles. x max égale un virgule cinq millimole، l'ion peroxodisulfate limitant.")),
        question_semblable("3", "Expliquer le rôle de l'eau glacée et nommer les deux facteurs cinétiques. Pourquoi le titrage doit-il être rapide ?",
          phrase("Trempe : baisse de température et dilution (concentrations plus faibles) ; la transformation est pratiquement bloquée. Titrage rapide : équivalence repérée avec précision."),
          ["trempe", "température", "concentration"], ["catalyseur"],
          corr([("3 : trempe : température et concentration diminuent ; titrage rapide pour une équivalence précise.", "la trempe")],
               "la trempe: la température et la concentration كينقصو، و la transformation كتتحبس تقريبا. le titrage rapide باش l'équivalence تكون مضبوطة.")),
        question_semblable("4", "Montrer que n_p(I₂) = C'·V_E / 2 et la calculer.",
          valeur("n_p(I₂)", 9.0e-5, "mol", "n(S₂O₃²⁻) = 2·n_p(I₂) ⇒ n_p(I₂) = C'·V_E/2 = 2,0·10⁻² × 9,0·10⁻³ / 2 = 9,0·10⁻⁵ mol"),
          ["÷ 2", "C'·V_E"], ["n_p(I₂) = C'·V_E"],
          corr([("4 : n_p(I₂) = C'·V_E/2 = 2,0·10⁻² × 9,0·10⁻³ / 2 = 9,0·10⁻⁵ mol", "neuf fois dix puissance moins cinq mole")],
               "n ديال le diiode égale C prime fois V E sur deux، égale neuf fois dix puissance moins cinq mole.")),
        question_semblable("5", "En déduire x(t₁) dans le mélange (en mmol). Comparer à x_max et conclure.",
          valeur("x(t₁)", 0.90, "mmol", "x(t₁) = 10 × 9,0·10⁻⁵ = 9,0·10⁻⁴ mol = 0,90 mmol"), ["V / V₀ = 10", "n(I₂) = x"], ["x(t₁) = 9,0·10⁻⁵ mol"],
          corr([("5 : x(t₁) = 10 × 9,0·10⁻⁵ mol = 0,90 mmol", "zéro virgule neuf millimole"), ("x/x_max = 0,90/1,5 = 0,60 : pas terminée.", "zéro virgule six")],
               "x égale dix fois neuf fois dix puissance moins cinq، يعني zéro virgule neuf millimole. x sur x max égale zéro virgule six: la transformation ما سالاتش.")),
        question_semblable("6", "Un élève annonce V_E = 18 mL pour un prélèvement de 10,0 mL fait plus tard. Calculer V_E,max (en mL) et juger.",
          valeur("V_E,max", 15.0, "mL", "n_p,max = 1,5·10⁻³/10 = 1,5·10⁻⁴ mol ; V_E,max = 2 × 1,5·10⁻⁴ / 2,0·10⁻² = 1,5·10⁻² L = 15 mL"),
          ["x_max", "V₀ / V", "V_E = 2·n_p / C'"], ["V_E,max = 7,5 mL"],
          corr([("6 : V_E,max = 2 × 1,5·10⁻⁴ / 2,0·10⁻² = 15 mL", "quinze millilitres"), ("18 mL > 15 mL : impossible.", "ما يمكنش")],
               "V E max égale deux fois un virgule cinq fois dix puissance moins quatre، sur deux fois dix puissance moins deux، égale quinze millilitres. dix-huit millilitres كتفوت quinze: ما يمكنش.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
