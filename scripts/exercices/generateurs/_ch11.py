# Outils du ch. 11 (transformations dans les deux sens) pour les générateurs phys_ex_ch11_deux_sens_* :
#  - nombres dits en français à partir de la valeur (une donnée changée change aussi la voix) ;
#  - diapositives d'explication sur les simulations EXISTANTES du cours (transformations-deux-sens-tableau, et le
#    titrage de cinetique-tableau) : la voix décrit la simulation avec SES valeurs (relues dans le cours par vue.py),
#    puis « فالتمرين ديالنا » applique la méthode aux valeurs de l'exercice (texte `app`, centre écrit).
import math, re, importlib.util
from pathlib import Path
from _chimie import sim, fr, sci

_TP = Path(__file__).resolve().parents[3] / "backend" / "kaggle_tts" / "texte_parle.py"
_sp = importlib.util.spec_from_file_location("tp", _TP); _tp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_tp)
nombre_fr = _tp.nombre_fr


def _dec(s):
    """« 3,29 » -> « trois virgule vingt-neuf » ; « 0,0256 » -> « zéro virgule zéro deux cinq six »."""
    neg = s.startswith("−") or s.startswith("-")
    s = s.lstrip("−-")
    if "," not in s:
        out = nombre_fr(int(s))
    else:
        e, d = s.split(",")
        reste = d.lstrip("0"); z = len(d) - len(reste)
        out = nombre_fr(int(e)) + " virgule" + " zéro" * z
        if reste:
            out += " " + (nombre_fr(int(reste)) if len(reste) <= 2 else " ".join(nombre_fr(int(c)) for c in reste))
    return ("moins " if neg else "") + out


def d(x, n=2):
    """nombre décimal dit : d(3.29) -> « trois virgule vingt-neuf »."""
    return _dec(fr(x, n))


def ds(x, n=1):
    """notation scientifique dite : ds(5.13e-4, 2) -> « cinq virgule treize fois dix puissance moins quatre »."""
    e = int(math.floor(math.log10(abs(x)))); m = x / 10 ** e
    if round(m, n) >= 10:
        m /= 10; e += 1
    if round(m, n) == 1 and n == 0:
        return f"dix puissance {_dec(str(e)) if e >= 0 else 'moins ' + nombre_fr(-e)}"
    p = nombre_fr(e) if e >= 0 else "moins " + nombre_fr(-e)
    return f"{_dec(fr(m, n))} fois dix puissance {p}"


def pc(x, n=1):
    """pourcentage dit : pc(0.0256) -> « deux virgule six pour cent »."""
    return _dec(fr(100 * x, n)) + " pour cent"


T = "transformations-deux-sens-tableau/"


# ------------------------------------------------------------------ diapositives (une par geste du cours)
def sl_acide_eau(sid, titre, app, centre):
    return sim(sid, titre, "Un proton passe de l'acide à l'eau : AH + H₂O ⇌ A⁻ + H₃O⁺.",
        T + "avancement.html?vue=acide_eau", "L'acide cède un proton à l'eau",
        "شوف ب la loupe: molécule ديال l'acide éthanoïque، وحداها molécule ديال l'eau. شوف le proton: كيدوز من l'acide ل l'eau، و l'eau كتولي l'ion H trois O plus. هنا l'eau كتلعب دور la base. بصفة عامة: A H، plus H deux O، donne A moins، plus H trois O plus. les couples: A H sur A moins، و H trois O plus sur H deux O. فالتمرين ديالنا: " + app,
        centre, [("شوف ب la loupe", "moment:loupe"), ("شوف le proton", "moment:transfert"),
                 ("بصفة عامة", "moment:equation"), ("les couples: A H sur A moins", "moment:couples")])


def sl_ph(sid, titre, app, centre):
    return sim(sid, titre, "[H₃O⁺] = 10^(−pH), en mol/L : attention au signe moins.",
        T + "ph.html?vue=calcul", "Du pH à la concentration des ions H₃O⁺",
        "شوف هاد المثال: le p H égale trois virgule quatre. la relation: la concentration des ions H trois O plus، égale dix puissance moins p H. l'application numérique: dix puissance moins trois virgule quatre، كتعطي quatre virgule zéro fois dix puissance moins quatre mole par litre. ردو البال: le signe moins. فالتمرين ديالنا: " + app,
        centre, [("شوف هاد المثال", "moment:donnee"), ("la relation: la concentration", "moment:relation"),
                 ("l'application numérique: dix puissance", "moment:calcul"), ("كتعطي quatre virgule zéro", "moment:resultat"),
                 ("ردو البال: le signe moins", "moment:piege")])


def sl_tableau(sid, titre, app, centre):
    return sim(sid, titre, "Le tableau d'avancement : l'eau en excès, les deux produits valent x.",
        T + "avancement.html?vue=tableau", "Le tableau d'avancement de l'acide avec l'eau",
        "الفوق، l'équation ب la double flèche. السطر اللول، l'état initial: l'acide C fois V، الما en excès، و zéro و zéro. السطر الثاني، en cours: C V moins x، و x، و x. السطر اللخر، l'état final: كنبدلو x ب x f. فالتمرين ديالنا: " + app,
        centre, [("الفوق، l'équation", "moment:equation"), ("السطر اللول", "moment:etat_initial"),
                 ("السطر الثاني", "moment:en_cours"), ("السطر اللخر", "moment:etat_final")])


def sl_xmax(sid, titre, app, centre):
    return sim(sid, titre, "Si la réaction était totale, l'acide serait épuisé : x_max = C·V.",
        T + "avancement.html?vue=x_max", "x_max : l'hypothèse de la réaction totale",
        "شوف المثال ديال le cours: يلا كانت la réaction totale، l'acide كامل غادي يتستهلك، والما en excès. إذن C V moins x max égale zéro، و x max égale C fois V. فالمثال: dix puissance moins deux، fois zéro virgule un، يعني dix puissance moins trois mole. فالتمرين ديالنا: " + app,
        centre, [("شوف المثال ديال le cours", "moment:hypothese"), ("إذن C V moins x max", "moment:relation"),
                 ("فالمثال: dix puissance", "moment:application"), ("يعني dix puissance moins trois mole", "moment:resultat")])


def sl_xf(sid, titre, app, centre):
    return sim(sid, titre, "x_f vient de la mesure : n(H₃O⁺)_f = x_f = [H₃O⁺]·V.",
        T + "avancement.html?vue=x_f", "x_f lu dans la colonne des ions H₃O⁺",
        "شوف la colonne ديال les ions H trois O plus: فاللخر، la quantité ديالهم égale x f. إذن x f égale la concentration des ions H trois O plus، fois V. فالمثال: quatre fois dix puissance moins quatre، fois zéro virgule un، يعني quatre fois dix puissance moins cinq mole. قارن deux barres: x f صغيرة بزاف قدام x max. فالتمرين ديالنا: " + app,
        centre, [("شوف la colonne", "moment:colonne"), ("إذن x f égale la concentration", "moment:relation"),
                 ("فالمثال: quatre fois", "moment:application"), ("يعني quatre fois dix puissance moins cinq mole", "moment:resultat"),
                 ("قارن deux barres", "moment:comparer")])


def sl_taux(sid, titre, app, centre):
    return sim(sid, titre, "τ = x_f/x_max, sans unité : τ < 1, limitée ; τ = 1, totale.",
        T + "avancement.html?vue=taux", "Les barres de x_f et de x_max",
        "la définition: tau égale x f sur x max، بلا وحدة. فالمثال: quatre fois dix puissance moins cinq، sur dix puissance moins trois، يعني zéro virgule zéro quarante. شوف deux barres: la barre ديال x f صغيرة بزاف. tau صغر من un: la réaction est limitée. فالتمرين ديالنا: " + app,
        centre, [("la définition: tau", "moment:definition"), ("فالمثال: quatre fois", "moment:application"),
                 ("يعني zéro virgule zéro quarante", "moment:resultat"), ("شوف deux barres", "moment:barres"),
                 ("tau صغر من un", "moment:limitee")])


def sl_relation(sid, titre, app, centre):
    return sim(sid, titre, "τ = x_f/x_max = [H₃O⁺]·V/(C·V) = 10^(−pH)/C.",
        T + "avancement.html?vue=relation", "La démonstration, ligne par ligne",
        "كنبداو ديما من la définition: tau égale x f sur x max. دابا كنبدلو: x f égale la concentration des ions H trois O plus، fois V، و x max égale C fois V. V لفوق و V لتحت، كيتحيدو. وكيبقى: tau égale dix puissance moins p H، sur C. فالتمرين ديالنا: " + app,
        centre, [("كنبداو ديما", "moment:depart"), ("دابا كنبدلو", "moment:remplacer"),
                 ("V لفوق و V لتحت", "moment:simplifier"), ("وكيبقى", "moment:relation")])


def sl_totale(sid, titre, app, centre):
    return sim(sid, titre, "Acide chlorhydrique : x_f = x_max, τ = 1, réaction totale, flèche simple.",
        T + "avancement.html?vue=totale", "L'acide chlorhydrique : une réaction totale",
        "شوف l'exemple ديال l'acide chlorhydrique: dix puissance moins deux mole par litre، و le p H mètre كيعطي deux virgule zéro. إذن x f égale dix puissance moins trois mole، وهادي هي بالضبط x max. tau égale un: la réaction est totale. ونكتبوها ب واحد la flèche simple. فالتمرين ديالنا: " + app,
        centre, [("شوف l'exemple", "moment:donnees"), ("إذن x f égale dix puissance", "moment:x_f"),
                 ("tau égale un:", "moment:taux"), ("la réaction est totale", "moment:totale"),
                 ("ونكتبوها ب واحد la flèche simple", "moment:fleches")])


def sl_attendu(sid, titre, app, centre):
    return sim(sid, titre, "Si la réaction était totale, [H₃O⁺] = C : on compare ce pH attendu au pH mesuré.",
        T + "avancement.html?vue=attendu", "pH attendu si totale, pH mesuré",
        "نفرضو أن la réaction كانت totale: la concentration des ions H trois O plus égale C، يعني un virgule zéro fois dix puissance moins deux mole par litre، و le p H اللي كنتسناو deux virgule zéro. le p H mètre كيعطي trois virgule quatre. قارن: trois virgule quatre كبر من deux virgule zéro. الخلاصة: la réaction ماشي totale. فالتمرين ديالنا: " + app,
        centre, [("نفرضو أن la réaction", "moment:hypothese"), ("و le p H اللي كنتسناو", "moment:calcul_attendu"),
                 ("le p H mètre كيعطي", "moment:mesure"), ("قارن: trois virgule quatre", "moment:comparer"),
                 ("الخلاصة: la réaction ماشي totale", "moment:conclusion")])


def sl_cond_relation(sid, titre, app, centre):
    return sim(sid, titre, "σ = λ₁·[H₃O⁺] + λ₂·[A⁻] = (λ₁ + λ₂)·[H₃O⁺].",
        T + "conductimetrie.html?vue=relation", "Les deux ions de la solution",
        "نبداو ب la formule: sigma égale la somme des lambda i، fois la concentration de l'ion i. فالمحلول ديال l'acide، كاينين deux ions: les ions H trois O plus، و les ions A moins. les ions H O moins قلال بزاف، كنهملوهم. وفle tableau، deux produits عندهم نفس la concentration، x f sur V. كنجمعو: sigma égale lambda un plus lambda deux، fois la concentration des ions H trois O plus. فالتمرين ديالنا: " + app,
        centre, [("نبداو ب la formule", "moment:formule"), ("كاينين deux ions", "moment:deux_ions"),
                 ("وفle tableau، deux produits", "moment:egalite"), ("كنجمعو: sigma égale", "moment:factoriser")])


def sl_cond_calcul(sid, titre, app, centre):
    return sim(sid, titre, "[H₃O⁺] = σ/(λ₁ + λ₂) en mol/m³, puis ÷ 1000 pour des mol/L.",
        T + "conductimetrie.html?vue=calcul", "Le calcul, avec la conversion des unités",
        "المعطيات: sigma égale un virgule cinquante-six fois dix puissance moins deux siemens par mètre، و les deux lambda بالوحدة millisiemens mètre carré par mole. العلاقة: la concentration des ions H trois O plus، égale sigma sur la somme des deux lambda، و les lambda خاصهم يكونو ب siemens. l'application numérique: كتعطي zéro virgule trois cent quatre-vingt-dix-neuf mole par mètre cube. رد البال: une mole par litre، égale mille moles par mètre cube، إذن كنقسمو على mille. ووصلنا ل tau: هاد la concentration sur C. فالتمرين ديالنا: " + app,
        centre, [("المعطيات:", "moment:donnees"), ("العلاقة:", "moment:relation"),
                 ("l'application numérique: كتعطي", "moment:application"), ("رد البال: une mole par litre", "moment:conversion"),
                 ("ووصلنا ل tau", "moment:taux")])


def sl_cond_ions(sid, titre, app, centre):
    return sim(sid, titre, "Même concentration, pas la même conductivité : pas le même nombre d'ions.",
        T + "conductimetrie.html?vue=ions", "Deux acides, deux conductivités",
        "شوف هاد deux béchers، فيهم نفس la concentration، zéro virgule zéro un mole par litre: l'acide éthanoïque و l'acide chlorhydrique. الرقم اللول: quinze virgule six millisiemens par mètre. الرقم الثاني: quatre cent vingt-six millisiemens par mètre، كبير بزاف. ب la loupe: فاللول كاينين شوية ديال les ions، وفالثاني بزاف. فالتمرين ديالنا: " + app,
        centre, [("شوف هاد deux béchers", "moment:deux_bechers"), ("الرقم اللول", "moment:afficheur_1"),
                 ("الرقم الثاني", "moment:afficheur_2"), ("ب la loupe", "moment:loupe"), ("فالتمرين ديالنا", "moment:conclusion")])


def sl_dilution(sid, titre, app, centre):
    return sim(sid, titre, "Diluer : la quantité de soluté ne change pas, C₀·V₀ = C₁·V₁.",
        T + "prerequis.html?vue=dilution", "Le geste de la dilution",
        "هادي la solution mère. ب la pipette، كناخدو dix millilitres. كنحطوهم ف la fiole jaugée ديال cent millilitres، وكنزيدو الما distillée حتى الخط. la quantité ديال le soluté بقات هي هي. إذن C zéro fois V zéro égale C un fois V un. فالتمرين ديالنا: " + app,
        centre, [("هادي la solution mère", "moment:mere"), ("ب la pipette", "moment:prelever"),
                 ("كنحطوهم ف la fiole jaugée", "moment:fiole"), ("وكنزيدو الما distillée", "moment:completer"),
                 ("la quantité ديال le soluté بقات", "moment:meme_quantite"), ("إذن C zéro fois V zéro", "moment:facteur")])


def sl_diluer(sid, titre, app, centre):
    return sim(sid, titre, "Plus la solution est diluée, plus τ est grand.",
        T + "diluer.html", "Le tableau des τ et ses barres",
        "شوف le tableau ديال le cours: trois solutions ديال نفس l'acide. العلاقة: tau égale dix puissance moins p H، sur C. la ligne اللولة كتعطي zéro virgule zéro quarante. الثانية: zéro virgule treize. الثالثة: zéro virgule trente-deux. شوف les barres: كيطلعو. إذن، plus la solution est diluée، plus tau est grand. فالتمرين ديالنا: " + app,
        centre, [("العلاقة: tau", "moment:relation"), ("la ligne اللولة", "moment:taux_1"), ("الثانية: zéro virgule treize", "moment:taux_2"),
                 ("الثالثة: zéro virgule trente-deux", "moment:taux_3"), ("شوف les barres", "moment:barres"),
                 ("إذن، plus la solution est diluée", "moment:conclusion")])


def sl_nature(sid, titre, app, centre):
    return sim(sid, titre, "À même concentration, τ dépend de l'acide.",
        T + "dilution.html?vue=nature", "Trois acides de même concentration",
        "trois béchers، فيهم نفس la concentration، zéro virgule zéro un mole par litre: l'acide chlorhydrique، l'acide méthanoïque، و l'acide éthanoïque. le p H: deux virgule zéro، deux virgule neuf، trois virgule quatre. و tau: un، zéro virgule treize، zéro virgule zéro quarante. شوف les barres: ماشي بحال بحال. إذن، à même concentration، tau dépend de l'acide. فالتمرين ديالنا: " + app,
        centre, [("trois béchers", "moment:trois_acides"), ("le p H: deux virgule zéro", "moment:mesures"),
                 ("و tau: un", "moment:taux"), ("شوف les barres", "moment:barres"), ("إذن، à même concentration", "moment:conclusion")])


def sl_inverse(sid, titre, app, centre):
    return sim(sid, titre, "Le pH monte : des ions H₃O⁺ sont consommés, la réaction va dans le sens inverse.",
        T + "equilibre.html?vue=inverse", "On ajoute la base conjuguée : le pH monte",
        "شوف هاد le bécher: l'acide chlorhydrique، مع نفس الحجم ديال الما، و le p H égale deux virgule trois. دابا فبلاصة الما، كنزيدو l'éthanoate de sodium. le p H كيطلع، حتى ل trois virgule six. إذن les ions H trois O plus نقصو: les ions éthanoate خداو منهم le proton. l'équation كتمشي فالاتجاه الآخر: le sens deux. فالتمرين ديالنا: " + app,
        centre, [("شوف هاد le bécher", "moment:acide_seul"), ("كنزيدو l'éthanoate de sodium", "moment:ajout"),
                 ("le p H كيطلع", "moment:ph_monte"), ("l'équation كتمشي فالاتجاه الآخر", "moment:equation_inverse"),
                 ("فالتمرين ديالنا", "moment:conclusion")])


def sl_sens(sid, titre, app, centre):
    return sim(sid, titre, "Sens direct (1) et sens inverse (2) : une seule équation, une double flèche.",
        T + "equilibre.html?vue=double_fleche", "Les deux sens d'une même réaction",
        "باللون الخضر، le sens un: l'acide كيعطي le proton ديالو للما. باللون الوردي، le sens deux: la base conjuguée كترجع تاخد le proton من les ions H trois O plus. جوج المعادلات كيتلاقاو فمعادلة وحدة، ب la double flèche. فالتمرين ديالنا: " + app,
        centre, [("باللون الخضر", "moment:sens_1"), ("باللون الوردي", "moment:sens_2"),
                 ("جوج المعادلات", "moment:double_fleche"), ("فالتمرين ديالنا", "moment:phrase")])


def sl_etat(sid, titre, app, centre):
    return sim(sid, titre, "À l'équilibre, les quantités ne changent plus ; réactifs et produits coexistent.",
        T + "equilibre.html?vue=etat", "Le pH ne bouge plus",
        "شوف الوقت كيدور من zéro حتى dix minutes، و le p H بقا trois virgule quatre، ما تبدلش. شوف les barres ديال الكميات: حتى barre ما تحركات. والمتفاعلات والنواتج كاينين فنفس الوقت. فالتمرين ديالنا: " + app,
        centre, [("شوف الوقت كيدور", "moment:chrono"), ("و le p H بقا", "moment:afficheur_stable"),
                 ("شوف les barres", "moment:barres"), ("والمتفاعلات والنواتج", "moment:coexistent"),
                 ("فالتمرين ديالنا", "moment:phrase")])


def sl_dynamique(sid, titre, app, centre):
    return sim(sid, titre, "Équilibre dynamique : v₁ = v₂, les deux réactions continuent.",
        T + "equilibre.html?vue=dynamique", "À la loupe : les deux sens en même temps",
        "من برا، ما كيتبدل والو. ولكن نشوفو ب la loupe. باللون الخضر، le sens un، وفنفس الوقت باللون الوردي، le sens deux. شوف les deux compteurs: كيزيدو مع بعض. شحال ما تفاعل فاتجاه، تفاعل بحالو فالاتجاه الآخر: v un égale v deux. فالتمرين ديالنا: " + app,
        centre, [("نشوفو ب la loupe", "moment:loupe"), ("باللون الخضر، le sens un", "moment:sens_1"),
                 ("باللون الوردي، le sens deux", "moment:sens_2"), ("شوف les deux compteurs", "moment:compteurs"),
                 ("v un égale v deux", "moment:egalite")])


def sl_proportion(sid, titre, app, centre):
    return sim(sid, titre, "α = [AH]/([AH] + [A⁻]) = 1 − τ.",
        T + "avancement.html?vue=proportion", "La proportion de la forme acide",
        "شوف هاد المثال: C A égale cinq virgule zéro fois dix puissance moins deux mole par litre، و le p H égale trois virgule zéro cinq. alpha هي la proportion ديال l'acide اللي بقا: la concentration de l'acide، sur la somme des deux concentrations. نرجعو ل le tableau d'avancement: la concentration de la base égale C fois tau، و la concentration de l'acide égale C moins C fois tau. إذن alpha égale un moins tau. l'application numérique: alpha égale zéro virgule neuf cent quatre-vingt-deux. فالتمرين ديالنا: " + app,
        centre, [("شوف هاد المثال", "moment:donnees"), ("alpha هي la proportion", "moment:definition_alpha"),
                 ("نرجعو ل le tableau d'avancement", "moment:tableau"), ("إذن alpha égale un moins tau", "moment:relation"),
                 ("l'application numérique: alpha", "moment:application")])


def sl_concentration(sid, titre, app, centre):
    return sim(sid, titre, "C = n/V : la quantité de soluté dans chaque litre.",
        T + "prerequis.html?vue=concentration", "Un soluté dissous dans l'eau",
        "شوف هاد le soluté: n égale deux virgule zéro millimoles. كنحطوه ف cent millilitres ديال الما. la relation: C égale n sur V، يعني vingt millimoles par litre. وبالعكس: n égale C fois V. فالتمرين ديالنا: " + app,
        centre, [("شوف هاد le soluté", "moment:solute"), ("كنحطوه ف cent millilitres", "moment:dissoudre"),
                 ("la relation: C égale n sur V", "moment:relation"), ("وبالعكس: n égale C fois V", "moment:n_cv")])


def sl_titrage(sid, titre, app, centre):
    return sim(sid, titre, "À l'équivalence, les réactifs du titrage sont dans les proportions de l'équation.",
        "cinetique-tableau/suivi.html?vue=titrage", "Le titrage jusqu'à l'équivalence",
        "فوق le bécher كاينة burette. كنزيدو بشوية، واللون كيتبدل. هنا l'équivalence. نعاود نقرا: à l'équivalence، les réactifs du titrage، sont dans les proportions stœchiométriques. فالتمرين ديالنا: " + app,
        centre, [("كاينة burette", "moment:burette"), ("كنزيدو بشوية", "moment:verser"), ("هنا l'équivalence", "moment:equivalence")])
