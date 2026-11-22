# Outils du ch. 12 (état d'équilibre) : nombres dits en français (le même nombre écrit et dit, sans faute de
# recopie), et les débuts de voix des vues de simulation du cours, avec les valeurs que la simulation MONTRE
# (relevées dans backend/data/courses/phys_ch12_etat_equilibre.json) ; la suite de la voix applique la méthode
# aux données de l'exercice (« فالتمرين ديالنا »).
from _chimie import *

_U = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze",
      "treize", "quatorze", "quinze", "seize"]
_D = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def entier(n):
    """entier en lettres (règles de 1990 non appliquées : comme les profs, « vingt et un », « quatre-vingts »)."""
    if n < 0:
        return "moins " + entier(-n)
    if n <= 16:
        return _U[n]
    if n < 20:
        return "dix-" + _U[n - 10]
    if n < 70:
        d, u = divmod(n, 10)
        if u == 0:
            return _D[d]
        return _D[d] + (" et un" if u == 1 else "-" + _U[u])
    if n < 80:
        u = n - 60
        return "soixante et onze" if u == 11 else "soixante-" + entier(u)
    if n < 100:
        u = n - 80
        return "quatre-vingts" if u == 0 else "quatre-vingt-" + entier(u)
    if n < 1000:
        c, r = divmod(n, 100)
        tete = "cent" if c == 1 else _U[c] + " cent" + ("s" if r == 0 else "")
        return tete if r == 0 else tete + " " + entier(r)
    m, r = divmod(n, 1000)
    tete = "mille" if m == 1 else entier(m) + " mille"
    return tete if r == 0 else tete + " " + entier(r)


def dire(s):
    """« 0,039 » -> « zéro virgule zéro trente-neuf » ; « 1,57 » -> « un virgule cinquante-sept » ; « −3 »."""
    s = s.replace("−", "-").replace(" ", "")
    neg = s.startswith("-")
    s = s.lstrip("-")
    if "," in s:
        a, b = s.split(",")
        z = len(b) - len(b.lstrip("0"))
        reste = b.lstrip("0")
        dec = " ".join(["zéro"] * z + ([entier(int(reste))] if reste else []))
        out = entier(int(a)) + " virgule " + dec
    else:
        out = entier(int(s))
    return ("moins " if neg else "") + out


def dfr(x, n=2):
    """le nombre écrit fr(x, n), dit."""
    return dire(fr(x, n))


def dsci(x, n=1):
    """le nombre écrit sci(x, n), dit : « un virgule cinq fois dix puissance moins cinq »."""
    if x == 0:
        return "zéro"
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    if round(m, n) >= 10:
        m /= 10; e += 1
    t = dfr(m, n)
    return t if e == 0 else f"{t} fois dix puissance {entier(e)}"


# ------------------------------------------------------------------ vues de simulation du cours
# clé -> (url, légende, début de voix avec les valeurs de la simulation, pointage [(mot, commande)])
VUES = {
  "definition": ("etat-equilibre-tableau/quotient.html?vue=definition", "Le quotient de réaction de l'acide éthanoïque",
    "شوف l'équation ديال l'acide éthanoïque مع الما، ب la double flèche. شوف les produits: les ions éthanoate و les ions H trois O plus، كيطلعو الفوق، ف le numérateur. ودابا le réactif، l'acide éthanoïque: كيهبط اللتحت، ف le dénominateur. الما هو le solvant، ما كيدخلش.",
    [("شوف l'équation ديال l'acide éthanoïque", "moment:equation"), ("شوف les produits", "moment:produits"),
     ("ودابا le réactif", "moment:reactifs"), ("ف le dénominateur", "moment:quotient")]),
  "generale": ("etat-equilibre-tableau/quotient.html?vue=generale", "La forme générale de Qr",
    "هادي هي la forme générale: a A plus b B، كيعطي c C plus d D، ب la double flèche. les produits الفوق، les réactifs التحت. شوف les coefficients: كيطلعو وكيوليو des exposants.",
    [("هادي هي la forme générale", "moment:forme"), ("شوف les coefficients", "moment:exposants")]),
  "eau": ("etat-equilibre-tableau/quotient.html?vue=eau", "L'eau, solvant, n'entre pas dans Qr",
    "رجع ل l'équation ديال l'acide éthanoïque مع الما. شوف الما: هو le solvant، كاين بزاف بزاف. شوف le quotient: الما مشطب، ما كيدخلش.",
    [("رجع ل l'équation", "moment:equation"), ("شوف الما", "moment:eau"), ("شوف le quotient", "moment:barree")]),
  "solides": ("etat-equilibre-tableau/quotient.html?vue=solides", "Les solides n'entrent pas dans Qr",
    "شوف le bécher: les ions cuivre، ودخلنا فيه la lame de zinc. شوف Zn s و Cu s: هادو solides، ما عندهمش concentration فالمحلول، كنشطبوهم. le quotient: Q r égale la concentration des ions zinc، sur la concentration des ions cuivre.",
    [("شوف le bécher", "moment:becher"), ("شوف Zn s و Cu s", "moment:solides"), ("le quotient: Q r égale", "moment:quotient")]),
  "sans_unite": ("etat-equilibre-tableau/quotient.html?vue=sans_unite", "Calculer Qr : un nombre sans unité",
    "ف l'exemple ديال le cours، les données هوما les concentrations، en mole par litre. l'application numérique: كنعوضو فQ r. le résultat: Q r égale quatre virgule zéro huit fois dix puissance moins six. والوحدة؟ Q r est sans unité.",
    [("les données", "moment:donnees"), ("l'application numérique", "moment:remplacer"), ("le résultat", "moment:resultat"), ("والوحدة؟", "moment:unite")]),
  "melange": ("etat-equilibre-tableau/quotient.html?vue=melange", "Un mélange : les concentrations dans le volume total",
    "شوف quatre flacons ديال l'exemple ديال le cours. كنزيدوهم كاملين ف واحد le bécher كبير: le volume total، V T égale trois cents millilitres. لكل نوع، la concentration initiale égale n sur V T. وفQ r i، V T الفوق و V T التحت كيتحيدو: نقدرو نخدمو ب les quantités de matière.",
    [("شوف quatre flacons", "moment:flacons"), ("كنزيدوهم كاملين", "moment:melange"), ("لكل نوع", "moment:concentrations"),
     ("V T الفوق و V T التحت كيتحيدو", "moment:simplifier")]),
  "concentrations": ("etat-equilibre-tableau/equilibre.html?vue=concentrations", "Du pH aux trois concentrations à l'équilibre",
    "شوف l'afficheur ديال le p H mètre ف l'exemple ديال le cours: trois virgule quarante et un. أولا، la concentration des ions H trois O plus à l'équilibre: dix puissance moins p H، يعني trois virgule quatre-vingt-neuf fois dix puissance moins quatre mole par litre. ثانيا، les ions éthanoate عندهم نفس التركيز. ثالثا، l'acide: C moins la concentration des ions H trois O plus.",
    [("شوف l'afficheur", "moment:mesure"), ("أولا، la concentration des ions H trois O plus", "moment:h3o"),
     ("ثانيا، les ions éthanoate", "moment:base"), ("ثالثا، l'acide", "moment:acide")]),
  "qr_eq": ("etat-equilibre-tableau/equilibre.html?vue=qr_eq", "Qr dans l'état d'équilibre",
    "دابا نعوضو les trois concentrations ف Q r. la définition: Q r à l'équilibre، هو le quotient de réaction، dans l'état d'équilibre. ف l'exemple ديال le cours، l'application numérique كتعطي un virgule cinquante-sept fois dix puissance moins cinq، بلا وحدة.",
    [("la définition", "moment:definition"), ("l'application numérique", "moment:application"), ("بلا وحدة", "moment:resultat")]),
  "expression": ("etat-equilibre-tableau/equilibre.html?vue=expression", "Qr,éq en fonction de C et du pH",
    "نبداو من la définition ديال Q r à l'équilibre. la base و les ions H trois O plus عندهم نفس التركيز: dix puissance moins p H. و l'acide: C moins dix puissance moins p H. دابا نعوضو ف Q r: الفوق، dix puissance moins p H fois dix puissance moins p H. إذن la relation: Q r à l'équilibre، égale dix puissance moins deux p H، sur C moins dix puissance moins p H.",
    [("نبداو من la définition", "moment:depart"), ("دابا نعوضو ف Q r", "moment:remplacer"), ("إذن la relation", "moment:relation")]),
  "taux": ("etat-equilibre-tableau/rappel.html?vue=taux", "Le taux d'avancement final par le tableau",
    "نتفكرو le tableau d'avancement، ب trois lignes. l'état initial: l'acide C fois V. en cours: l'acide كينقص ب x. l'état d'équilibre: x égale x éq. الما en excès، إذن x max égale C fois V. و x éq égale la concentration des ions H trois O plus، fois V. إذن la relation: tau égale x éq sur x max، يعني dix puissance moins p H، sur C.",
    [("نتفكرو le tableau d'avancement", "moment:tableau"), ("l'état initial", "moment:ligne_initial"),
     ("en cours", "moment:ligne_en_cours"), ("l'état d'équilibre", "moment:ligne_equilibre"),
     ("x max égale C fois V", "moment:x_max"), ("و x éq égale", "moment:x_eq"), ("إذن la relation: tau", "moment:taux")]),
  "c_tau": ("etat-equilibre-tableau/constante.html?vue=c_tau", "K = C·τ²/(1 − τ), à partir du tableau",
    "نبداو من le tableau d'avancement ب les concentrations. la base و les ions H trois O plus، à l'équilibre: C fois tau. l'acide خسر C fois tau، إذن كيبقى C fois un moins tau. دابا نعوضو ف K: الفوق، C au carré fois tau au carré، والتحت، C fois un moins tau. واحد C كيتحيد. إذن la relation: K égale C fois tau au carré، sur un moins tau.",
    [("نبداو من le tableau d'avancement", "moment:tableau"), ("دابا نعوضو ف K", "moment:remplacer"),
     ("واحد C كيتحيد", "moment:simplifier"), ("إذن la relation: K", "moment:relation")]),
  "trois_c": ("etat-equilibre-tableau/constante.html?vue=trois_c", "Trois concentrations, le même Qr,éq",
    "ف l'exemple ديال le cours، trois béchers ديال l'acide éthanoïque، ب trois concentrations. la colonne ديال tau كتتبدل: zéro virgule zéro trente-neuf، zéro virgule zéro cinquante-cinq، و zéro virgule cent dix-sept. ولكن la colonne ديال Q r à l'équilibre كتبقى قريبة من un virgule six fois dix puissance moins cinq.",
    [("trois béchers", "moment:bechers"), ("la colonne ديال tau", "moment:ligne_3"), ("ولكن la colonne", "moment:comparer")]),
  "k_def": ("etat-equilibre-tableau/constante.html?vue=definition", "La constante d'équilibre K",
    "شوف l'encadré: K égale Q r à l'équilibre، la constante d'équilibre. K ما كتتعلق غير ب la température. و K ما كتتعلقش ب l'état initial.",
    [("شوف l'encadré", "moment:encadre"), ("K ما كتتعلق غير ب la température", "moment:temperature"),
     ("و K ما كتتعلقش ب l'état initial", "moment:etat_initial")]),
  "inverse": ("etat-equilibre-tableau/constante.html?vue=inverse", "La réaction inverse : K' = 1/K",
    "الفوق، le sens un، مع la constante K ديالو. دابا نكتبو l'équation فالجهة الأخرى. شوف le quotient: اللي كان الفوق ولا لتحت. إذن la relation: K prime égale un sur K.",
    [("الفوق، le sens un", "moment:sens_1"), ("دابا نكتبو l'équation", "moment:sens_2"),
     ("شوف le quotient", "moment:retourner"), ("إذن la relation: K prime", "moment:relation")]),
  "cond_rel": ("etat-equilibre-tableau/conductimetrie.html?vue=relation", "σ = (λ₁ + λ₂)·[H₃O⁺]éq",
    "ف l'exemple ديال le cours، la cellule ديال le conductimètre فواحد l'acide éthanoïque، و l'afficheur كيعطي quatre virgule six millisiemens par mètre. les ions اللي كيوصلو التيار: les ions H trois O plus و les ions de la base. إذن sigma égale lambda un fois la concentration des ions H trois O plus، plus lambda deux fois la concentration de la base. ولكن من le tableau d'avancement، جوج التراكيز متساويين. إذن نخرجوها facteur commun: sigma égale lambda un plus lambda deux، fois la concentration des ions H trois O plus. ومنها، la concentration égale sigma sur la somme des deux lambda.",
    [("la cellule ديال le conductimètre", "moment:mesure"), ("إذن sigma égale lambda un", "moment:formule"),
     ("ولكن من le tableau d'avancement", "moment:egalite"), ("إذن نخرجوها facteur commun", "moment:factoriser"),
     ("ومنها، la concentration", "moment:isoler")]),
  "cond_calc": ("etat-equilibre-tableau/conductimetrie.html?vue=calcul", "De σ à τ et K, ligne par ligne",
    "دابا الحساب ف l'exemple ديال le cours. sigma égale quatre virgule six millisiemens par mètre، يعني quatre virgule six fois dix puissance moins trois siemens par mètre. sigma sur la somme des deux lambda، كتعطي zéro virgule cent dix-huit mole par mètre cube. رد البال: هادي ب mole par mètre cube، ماشي ب mole par litre. un mole par litre égale mille moles par mètre cube، إذن نقسمو على mille.",
    [("دابا الحساب", "moment:donnees"), ("sigma sur la somme des deux lambda", "moment:concentration"), ("رد البال", "moment:conversion")]),
  "dilution": ("etat-equilibre-tableau/facteurs.html?vue=dilution", "Diluer : même K, τ plus grand",
    "شوف les barres ديال l'exemple ديال le cours: نفس l'acide éthanoïque، ب trois concentrations. ب un virgule zéro fois dix puissance moins deux mole par litre، tau égale zéro virgule zéro trente-neuf. ب un virgule zéro fois dix puissance moins trois mole par litre، tau égale zéro virgule cent dix-sept. و la constante d'équilibre K نفسها فالتلاتة: un virgule six fois dix puissance moins cinq. إذن: même K، plus C est petite، plus tau est grand.",
    [("شوف les barres", "moment:barres"), ("ب un virgule zéro fois dix puissance moins deux", "moment:taux_1"),
     ("ب un virgule zéro fois dix puissance moins trois", "moment:taux_3"), ("و la constante d'équilibre K", "moment:constante"),
     ("إذن: même K", "moment:conclusion")]),
  "nature": ("etat-equilibre-tableau/facteurs.html?vue=nature", "Même C, deux acides : K et τ",
    "ف l'exemple ديال le cours، deux béchers بنفس la concentration: l'acide éthanoïque و l'acide méthanoïque. pour l'acide éthanoïque، K égale un virgule six fois dix puissance moins cinq، و tau égale zéro virgule zéro trente-neuf. pour l'acide méthanoïque، K égale un virgule huit fois dix puissance moins quatre، و tau égale zéro virgule treize. إذن: même C، plus K est grande، plus tau est grand.",
    [("deux béchers", "moment:deux_acides"), ("pour l'acide éthanoïque، K", "moment:constantes"),
     ("و tau égale zéro virgule zéro trente-neuf", "moment:taux"), ("إذن: même C", "moment:conclusion")]),
  "courbe": ("etat-equilibre-tableau/facteurs.html?vue=courbe", "τ en fonction de C, pour deux acides",
    "شوف les axes: l'axe vertical هو tau، و l'axe horizontal هو la concentration C. la courbe الزرقة: l'acide éthanoïque. دابا نحركو la poignée C: ب C égale dix puissance moins quatre mole par litre، tau égale zéro virgule trente-trois. ب C égale dix puissance moins un mole par litre، tau égale zéro virgule zéro treize. كل ما صغرات C، كبر tau.",
    [("شوف les axes", "moment:axes"), ("la courbe الزرقة", "moment:courbe_1"),
     ("ب C égale dix puissance moins quatre", {"set": {"C": 0.0001}}), ("ب C égale dix puissance moins un", {"set": {"C": 0.1}})]),
  "diluer": ("etat-equilibre-tableau/diluer.html", "Quand on dilue : le tableau",
    "le tableau: quand on dilue. السطر اللول: C كتنقص. السطر الثاني: la concentration des ions H trois O plus كتنقص، إذن le p H كيطلع. السطر الثالث: tau كيكبر. السطر الرابع: K ما كتبدلش، حيت K كتتبدل غير ب la température.",
    [("le tableau: quand on dilue", "moment:titre"), ("السطر اللول", "moment:ligne_c"), ("السطر الثاني", "moment:ligne_ph"),
     ("السطر الثالث", "moment:ligne_taux"), ("السطر الرابع", "moment:ligne_k")]),
  "couple": ("acides-bases-tableau/eau.html?vue=rappel", "Le couple acide/base et le pH",
    "l'acide، هو espèce chimique، قادرة تعطي un proton H plus. la base، قادرة تاخد un proton H plus. والما كاين ف deux couples: مع l'acide، الما هو la base. و le p H égale moins log، de la concentration des ions H trois O plus.",
    [("l'acide، هو espèce chimique", "moment:acide_base"), ("والما كاين ف deux couples", "moment:eau_deux_couples"),
     ("و le p H égale moins log", "moment:ph")]),
}


def slide(sid, cle, titre, lead, suite, centre):
    """diapositive d'explication : la vue du cours (sa voix et ses valeurs), puis la suite propre à l'exercice."""
    url, caption, debut, pts = VUES[cle]
    return sim(sid, titre, lead, url, caption, debut + " " + suite, centre, pts)


def h3o(pH):
    return 10 ** (-pH)
