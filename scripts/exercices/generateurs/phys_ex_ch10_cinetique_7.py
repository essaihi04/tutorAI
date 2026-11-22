# Exercice de chimie, ch. 10 (suivi temporel, vitesse de réaction), niveau difficile (« Supérieur ») : suivi
# conductimétrique d'une saponification, moins guidé ; x_max avec un réactif en excès, « montrer que » σ = A + B·x et
# calcul de A et B, t½ sans indication de σ½, « montrer que » v = (1/(B·V))·dσ/dt et v(0), lecture critique de
# « à 2·t½ la réaction est finie ».
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2016 R (2.1 l'ion A⁻ d'une saponification, 2.3.1 σ½, 2.3.2 t½, 2.3.3 v(0) en
#    mol·m⁻³·min⁻¹), 2018 R (2.2.1 G½ quand x = x_max/2, 2.2.2 t½), 2021 N (2.2 t½ à l'aide de σ = f(x), 2.3
#    « montrer que » v = −1/(160·V₀)·dσ/dt, 2.4 v₁), 2024 N (1.b vrai/faux « terminée au bout de 2·t½ ») —
#    backend/data/exams/physique ;
#  - profs : architecture/sources_chimie_ch9_ch11.md, chapitre B (Hadjyne et El Founani : Zn + H₃O⁺ suivi par
#    σ = A + B·x en littéral ; Mahajar-Tabit, Sbiro : x = x_max·σ/σ_max) et phys_ch10_cinetique.md (le cours explique
#    G = k·σ et la droite σ(x) de la saponification ; piège du signe et de V₀ en m³ dans le « montrer que » de v) ;
#  - séries en ligne (titres et résumés lus par recherche ; PDF non ouverts, réseau du conteneur limité) :
#    talamidi (suivi temporel séries 1 et 2, activités 3), moutamadris (fiches 13-7, 13-8), alloschool (élément
#    119798), coursdusoirpc (TD B. Mouslim), pc1.ma (fiches El Founani / Hadjyne).
# Ici : méthanoate d'éthyle (le cours prend l'éthanoate d'éthyle, 1,0 mmol dans 100 mL : pas ici), nos quantités,
# notre courbe σ(t) (calculée : σ = A + B·x avec x d'ordre un, t½ = 7 min) et notre tangente.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *

L_NA, L_HO, L_ME = 5.01e-3, 19.9e-3, 5.46e-3     # S·m²·mol⁻¹ (Na⁺, HO⁻, HCOO⁻)
# ------------------------------------------------------------------ données
def calc(n_ho, n_est, V, t12, t_tan):
    xm = min(n_ho, n_est)
    A = (L_NA + L_HO) * n_ho / V
    B = -(L_HO - L_ME) / V
    sf = A + B * xm
    x, _ = x_ordre1(xm, t12)
    k = math.log(2) / t12
    expr = f"{A:.6f}-{(A-sf):.6f}*(1-exp(-{k:.6f}*x))"
    pente0 = -(A - sf) * k
    yQ = round(A + pente0 * t_tan, 3)
    return xm, A, B, sf, expr, yQ
V, N_HO, N_EST, T12 = 200e-6, 3.0e-3, 4.0e-3, 7.0
XMAX, A, B, SF, EXPR, yQ = calc(N_HO, N_EST, V, T12, 8)
assert abs(XMAX - 3.0e-3) < 1e-12 and round(A, 3) == 0.374 and abs(B + 72.2) < 1e-9 and round(SF, 3) == 0.157
assert yQ == 0.202, yQ
S12 = (A + SF) / 2                         # 0,265 S/m
V0 = ((0.202 - 0.374) / 8) / (B * V)        # mol·m⁻³·min⁻¹ (valeurs lues)
assert abs(V0 - 1.489) < 0.002, V0
S14 = A - 0.75 * (A - SF)                  # σ(2·t½)
assert round(S14, 3) == 0.211
X14 = (0.374 - 0.211) / 72.2               # 2,26e-3 mol
assert abs(X14 / XMAX - 0.75) < 0.01

def figS(A_, sf, tmax, gx, gy, Qp, expr):
    return courbe_fig("Conductivité σ du mélange en fonction du temps",
        ((0, tmax, "t", "min", gx), (0, gy[-1], "σ", "S/m", gy)),
        [{"f": "courbe", "expr": expr, "de": 0, "a": tmax, "couleur": "cyan", "texte": "σ(t)", "texte_x": tmax * 0.85, "pos": "n"},
         {"f": "courbe", "expr": f"{round(A_, 3)}+{(Qp[1]-round(A_, 3))/Qp[0]:.6f}*x", "de": 0, "a": Qp[0] * 1.1, "couleur": "orange", "trait": "pointille"},
         {"f": "point", "at": [0, round(A_, 3)], "t": f"P (0 ; {fr(A_, 3)})", "pos": "e", "couleur": "orange"},
         {"f": "point", "at": list(Qp), "t": f"Q ({Qp[0]} ; {fr(Qp[1], 3)})", "pos": "so", "couleur": "orange"},
         {"f": "repere", "y": round(sf, 3), "couleur": "faible"}],
        legende="(T) : tangente à la courbe en t = 0, passant par P et Q ; coordonnées en (min ; S/m).")

FIG = figS(A, SF, 56, [0, 7, 14, 21, 28, 35, 42, 49, 56], [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4], (8, yQ), EXPR)

# ------------------------------------------------------------------ similaire
sV, sN_HO, sN_EST, sT12 = 250e-6, 5.0e-3, 6.0e-3, 5.0
sXM, sA, sB, sSF, sEXPR, syQ = calc(sN_HO, sN_EST, sV, sT12, 6)
assert round(sA, 3) == 0.498 and abs(sB + 57.76) < 1e-9 and round(sSF, 3) == 0.209 and syQ == 0.258, (sA, sB, sSF, syQ)
sV0 = ((0.258 - 0.498) / 6) / (sB * sV)     # 2,77
s10 = sA - 0.75 * (sA - sSF)
assert round(s10, 3) == 0.282, s10
sX10 = (0.498 - 0.282) / 57.76               # 3,74e-3
sFIG = figS(sA, sSF, 40, [0, 5, 10, 15, 20, 25, 30, 35, 40], [0, 0.1, 0.2, 0.3, 0.4, 0.5], (6, syQ), sEXPR)

EQ = "HCOOC₂H₅(aq) + HO⁻(aq) → HCOO⁻(aq) + C₂H₅OH(aq)"
QUESTIONS = [
  Q("1", "Déterminer l'avancement maximal x_max et le réactif limitant.",
    "السؤال un: حدد x max و le réactif limitant.",
    val("x_max", XMAX, "mol", "HO⁻ limitant : x_max = n₀(HO⁻) = 3,0 × 10⁻³ mol"),
    (["n₀(HO⁻) − x_max = 0", "n₀(ester) − x_max = 0", "mol"], ["x_max = 4,0 × 10⁻³ mol", "x_max = 7,0 × 10⁻³ mol"]),
    [("Les deux réactifs ont le coefficient 1. Compare simplement leurs quantités initiales.",
      "deux réactifs عندهم le coefficient un. قارن غير les quantités initiales ديالهم."),
     ("Hypothèses : 3,0 × 10⁻³ − x_max = 0 ou 4,0 × 10⁻³ − x_max = 0 ; on garde la plus petite.",
      "les hypothèses: trois virgule zéro fois dix puissance moins trois moins x max égale zéro، ولا quatre virgule zéro. كناخدو الصغيرة.")],
    [("2 hypothèses : x_max = 3,0 × 10⁻³ mol (HO⁻) ou 4,0 × 10⁻³ mol (ester)", "deux hypothèses"),
     ("1 : x_max = 3,0 × 10⁻³ mol ; les ions hydroxyde sont le réactif limitant, l'ester est en excès", "les ions hydroxyde هوما le réactif limitant")],
    "السؤال un. deux hypothèses: les ions hydroxyde كيعطيو trois virgule zéro fois dix puissance moins trois mole، و l'ester quatre virgule zéro fois dix puissance moins trois. كناخدو الصغيرة: x max égale trois virgule zéro fois dix puissance moins trois mole، و les ions hydroxyde هوما le réactif limitant. l'ester en excès.",
    "ex_1", "fa_1"),
  Q("2", "Montrer que la conductivité du mélange s'écrit σ = A + B·x, et calculer A et B (V en m³). Pourquoi σ diminue-t-elle ?",
    "السؤال deux: بين أن sigma égale A plus B fois x، وحسب A و B، مع V ب mètre cube. علاش sigma كتنقص؟",
    val("B", B, "S·m⁻¹·mol⁻¹", "A = (λ(Na⁺) + λ(HO⁻))·n₀/V = 0,374 S/m ; B = −(λ(HO⁻) − λ(HCOO⁻))/V = −72,2 S·m⁻¹·mol⁻¹", tol=0.02),
    (["σ = Σ λᵢ·[Xᵢ]", "[Na⁺] = n₀/V", "[HO⁻] = (n₀ − x)/V", "[HCOO⁻] = x/V", "V = 2,0 × 10⁻⁴ m³"], ["B = +72,2", "[Na⁺] = (n₀ − x)/V"]),
    [("Trois ions à une date t : Na⁺ (spectateur, n₀), HO⁻ (n₀ − x) et HCOO⁻ (x). Écris σ = Σ λᵢ·[Xᵢ] et regroupe les termes sans x et les termes en x.",
      "trois ions ف واحد la date: Na plus spectateur، n zéro، H O moins، n zéro moins x، و l'ion méthanoate، x. كتب sigma égale la somme، وجمع اللي بلا x واللي فيهم x."),
     ("A = (λ(Na⁺) + λ(HO⁻))·n₀/V et B = −(λ(HO⁻) − λ(HCOO⁻))/V ; 200 mL = 2,0 × 10⁻⁴ m³, λ en S·m²·mol⁻¹.",
      "A égale lambda sodium plus lambda hydroxyde، fois n zéro sur V. و B égale moins، lambda hydroxyde moins lambda méthanoate، sur V. و V égale deux fois dix puissance moins quatre mètre cube.")],
    [("2 : σ = λ(Na⁺)·n₀/V + λ(HO⁻)·(n₀ − x)/V + λ(HCOO⁻)·x/V", "sigma égale lambda sodium"),
     ("σ = (λ(Na⁺) + λ(HO⁻))·n₀/V − (λ(HO⁻) − λ(HCOO⁻))·x/V = A + B·x", "إذن sigma égale A plus B fois x"),
     ("A = 24,91 × 10⁻³ × 3,0 × 10⁻³/(2,0 × 10⁻⁴) ≈ 0,374 S/m ; B = −14,44 × 10⁻³/(2,0 × 10⁻⁴) = −72,2 S·m⁻¹·mol⁻¹", "B égale moins soixante-douze virgule deux"),
     ("B < 0 car λ(HO⁻) > λ(HCOO⁻) : chaque ion HO⁻ consommé est remplacé par un ion HCOO⁻ moins conducteur, σ diminue", "علاش sigma كتنقص")],
    "السؤال deux. sigma égale lambda sodium fois n zéro sur V، plus lambda hydroxyde fois n zéro moins x، sur V، plus lambda méthanoate fois x sur V. كنجمعو: إذن sigma égale A plus B fois x، مع A égale lambda sodium plus lambda hydroxyde، fois n zéro sur V، يعني environ zéro virgule trois cent soixante-quatorze siemens par mètre. و B égale moins، lambda hydroxyde moins lambda méthanoate، sur V: B égale moins soixante-douze virgule deux siemens par mètre et par mole. علاش sigma كتنقص؟ كل ion hydroxyde كيتستهلك، وكيجي فبلاصتو ion méthanoate، و lambda ديالو صغيرة.",
    "ex_2", "fa_2"),
  Q("3", "Déterminer le temps de demi-réaction t½.",
    "السؤال trois: حدد le temps de demi-réaction، t un demi.",
    val("t½", T12, "min", "σ½ = A + B·x_max/2 = (σ₀ + σ_f)/2 ≈ 0,265 S/m ; t½ = 7 min", tol=0.06),
    (["x(t½) = x_max/2", "σ½ = A + B·x_max/2", "σ_f = A + B·x_max", "t½"], ["σ½ = σ₀/2", "σ½ = σ_f/2"]),
    [("La courbe donne σ, pas x : calcule la valeur σ½ de σ quand x = x_max/2 (réaction totale).",
      "la courbe كتعطي sigma، ماشي x. حسب sigma un demi ملي x égale x max sur deux."),
     ("σ½ = A + B·x_max/2 = (σ₀ + σ_f)/2, avec σ_f = A + B·x_max. Attention : ce n'est pas σ₀/2.",
      "sigma un demi égale A plus B fois x max sur deux، يعني sigma zéro plus sigma f، sur deux. رد البال: ماشي sigma zéro sur deux.")],
    [("3 : σ_f = A + B·x_max = 0,374 − 72,2 × 3,0 × 10⁻³ ≈ 0,157 S/m", "sigma f égale environ zéro virgule cent cinquante-sept"),
     ("à t½, x = x_max/2 : σ½ = A + B·x_max/2 = (0,374 + 0,157)/2 ≈ 0,265 S/m", "sigma un demi égale environ zéro virgule deux cent soixante-cinq"),
     ("lecture graphique : t½ = 7 min", "t un demi égale sept minutes")],
    "السؤال trois. اللول sigma f: A plus B fois x max، sigma f égale environ zéro virgule cent cinquante-sept siemens par mètre. à t un demi، x égale x max sur deux، إذن sigma un demi égale sigma zéro plus sigma f، sur deux: sigma un demi égale environ zéro virgule deux cent soixante-cinq siemens par mètre. ماشي sigma zéro sur deux. على la courbe: t un demi égale sept minutes.",
    "ex_3", "fa_3"),
  Q("4", "Montrer que v = (1/(B·V))·dσ/dt, puis calculer v(0) en mol·m⁻³·min⁻¹ à l'aide de la tangente (T).",
    "السؤال quatre: بين أن v égale un sur B fois V، fois d sigma sur d t. ومن بعد حسب v de zéro ب mole par mètre cube et par minute، بla tangente T.",
    val("v(0)", V0, "mol·m⁻³·min⁻¹", "v(0) = (dσ/dt)₀/(B·V) = ((0,202 − 0,374)/8)/(−72,2 × 2,0 × 10⁻⁴) ≈ 1,49 mol·m⁻³·min⁻¹", tol=0.04),
    (["v = (1/V)·dx/dt", "dσ/dt = B·dx/dt", "(dσ/dt)₀", "B·V", "mol·m⁻³·min⁻¹"], ["v = −1,49", "v = B·V·dσ/dt"]),
    [("Dérive σ = A + B·x : A et B sont constants. Exprime dx/dt, puis remplace dans v = (1/V)·dx/dt.",
      "اشتق sigma égale A plus B fois x: A و B ثابتين. عبر على d x sur d t، ومن بعد عوض فv égale un sur V fois d x sur d t."),
     ("(dσ/dt)₀ est la pente de (T) entre P et Q : elle est négative, comme B ; v est donc positive.",
      "d sigma sur d t à zéro هي la pente ديال T بين P و Q: سالبة، بحال B. إذن v موجبة.")],
    [("4 : dσ/dt = B·dx/dt, donc dx/dt = (1/B)·dσ/dt et v = (1/V)·dx/dt = (1/(B·V))·dσ/dt", "v égale un sur B fois V"),
     ("(dσ/dt)₀ = (0,202 − 0,374)/(8 − 0) ≈ −2,15 × 10⁻² S·m⁻¹·min⁻¹", "la pente égale environ moins deux virgule quinze fois dix puissance moins deux"),
     ("v(0) = −2,15 × 10⁻²/(−72,2 × 2,0 × 10⁻⁴) ≈ 1,49 mol·m⁻³·min⁻¹", "v de zéro égale environ un virgule quarante-neuf")],
    "السؤال quatre. كنشتقو sigma égale A plus B fois x: d sigma sur d t égale B fois d x sur d t. إذن d x sur d t égale un sur B، fois d sigma sur d t، و v égale un sur B fois V، fois d sigma sur d t. la pente ديال T: zéro virgule deux cent deux moins zéro virgule trois cent soixante-quatorze، sur huit، la pente égale environ moins deux virgule quinze fois dix puissance moins deux siemens par mètre et par minute. على B fois V، يعني moins soixante-douze virgule deux fois deux fois dix puissance moins quatre: v de zéro égale environ un virgule quarante-neuf mole par mètre cube et par minute.",
    "ex_4", "fa_4"),
  Q("5", "Un élève affirme : « à t = 2·t½ = 14 min, la réaction est terminée ». On lit sur la courbe σ(14 min) = 0,211 S/m. Calculer x(14 min) et discuter l'affirmation.",
    "السؤال cinq: واحد التلميذ قال: à deux t un demi، يعني quatorze minutes، la réaction سالات. على la courbe، sigma de quatorze minutes égale zéro virgule deux cent onze siemens par mètre. حسب x de quatorze minutes وناقش.",
    val("x(14)", X14, "mol", "x = (σ − A)/B = (0,211 − 0,374)/(−72,2) ≈ 2,26 × 10⁻³ mol", tol=0.04),
    (["x = (σ − A)/B", "x/x_max", "x_max = 3,0 × 10⁻³ mol"], ["x = σ/B", "x(2t½) = x_max"]),
    [("De σ = A + B·x, isole x. Puis compare le résultat à x_max.",
      "من sigma égale A plus B fois x، خرج x. ومن بعد قارن مع x max."),
     ("x = (σ − A)/B ; si x < x_max, il reste des ions HO⁻ : la réaction continue.",
      "x égale sigma moins A، sur B. يلا x صغيرة من x max، باقيين les ions hydroxyde، و la réaction باقا خدامة.")],
    [("5 : x = (σ − A)/B = (0,211 − 0,374)/(−72,2) ≈ 2,26 × 10⁻³ mol", "x de quatorze minutes égale environ deux virgule vingt-six"),
     ("x/x_max ≈ 2,26/3,0 ≈ 0,75 : x < x_max", "x صغيرة من x max"),
     ("l'affirmation est fausse : à 2·t½ la réaction n'est pas terminée (il faut attendre le palier σ_f ≈ 0,157 S/m)", "l'affirmation fausse")],
    "السؤال cinq. من sigma égale A plus B fois x: x égale sigma moins A، sur B. يعني zéro virgule deux cent onze moins zéro virgule trois cent soixante-quatorze، sur moins soixante-douze virgule deux. x de quatorze minutes égale environ deux virgule vingt-six fois dix puissance moins trois mole، تقريبا trois quarts ديال x max. إذن x صغيرة من x max، و l'affirmation fausse: à deux t un demi، la réaction ما ساليتش. خاصنا نتسناو le palier، sigma f.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : le réactif limitant",
      "Coefficients 1 et 1 : le réactif de plus petite quantité est limitant.",
      "cinetique-tableau/limitant.html", "Les deux hypothèses du réactif limitant",
      "كنرجعو ل l'état final ديال le tableau. كنديرو deux hypothèses. l'hypothèse un، ومن بعد l'hypothèse deux. شمن وحدة ناخدو؟ الصغيرة. ملي يتسالى le réactif limitant، la réaction كتوقف. فالتمرين ديالنا: les ions hydroxyde كيعطيو trois virgule zéro fois dix puissance moins trois mole، و l'ester quatre virgule zéro. إذن x max égale trois virgule zéro fois dix puissance moins trois mole، و les ions hydroxyde هوما le réactif limitant.",
      [("x_max = 3,0 × 10⁻³ mol ; HO⁻ limitant", "و les ions hydroxyde هوما le réactif limitant")],
      [("كنرجعو ل l'état final", "moment:tableau"), ("l'hypothèse un", "moment:hypothese_1"), ("ومن بعد l'hypothèse deux", "moment:hypothese_2"),
       ("الصغيرة", "moment:plus_petite"), ("ملي يتسالى le réactif limitant", "moment:limitant")]),
  sim("ex_2", "Question 2 : σ = A + B·x, une droite qui descend",
      "Trois ions ; on regroupe : σ = σ₀ − (λ(HO⁻) − λ(ester ion))·x/V.",
      "cinetique-tableau/conductimetrie.html?vue=droite", "σ en fonction de x pour une saponification",
      "دابا نبينو علاش sigma كتبدل مع x. ف واحد la date، فالمحلول كاينين trois ions. la concentration de sodium égale n zéro sur V، la concentration d'hydroxyde égale n zéro moins x، sur V، و l'ion اللي كيتكون، x sur V. كنعوضو، ومن بعد كنجمعو اللي فيهم n zéro، واللي فيهم x. دابا نرسمو sigma en fonction de x: خط مستقيم، كيهبط، حيت lambda hydroxyde كبر. فالتمرين ديالنا، l'ion اللي كيتكون هو l'ion méthanoate. A égale environ zéro virgule trois cent soixante-quatorze siemens par mètre، و B égale moins soixante-douze virgule deux.",
      [("σ = A + B·x", "كنعوضو"), ("A ≈ 0,374 S/m ; B = −72,2 S·m⁻¹·mol⁻¹", "و B égale moins soixante-douze virgule deux")],
      [("دابا نبينو", "start"), ("دابا نرسمو sigma en fonction de x", "moment:axes"), ("خط مستقيم", "moment:droite"), ("فالتمرين ديالنا", "moment:relation")]),
  sim("ex_3", "Question 3 : σ½ n'est pas σ₀/2",
      "x = x_max·(σ₀ − σ)/(σ₀ − σ_f) : à x_max/2, σ est au milieu de σ₀ et σ_f.",
      "cinetique-tableau/conductimetrie.html?vue=droite&depart=relation", "De σ à x : le rapport des différences",
      "دابا sigma f، ف l'état final. فاللخر، x égale x max. دابا جوج فروقات: sigma zéro moins sigma، و sigma zéro moins sigma f. كنقسمو: إذن x égale x max، fois sigma zéro moins sigma، sur sigma zéro moins sigma f. ويلا sigma فالنص بين sigma zéro و sigma f، x هي النص ديال x max. فالتمرين ديالنا: sigma un demi égale environ zéro virgule deux cent soixante-cinq siemens par mètre، و على la courbe، t un demi égale sept minutes.",
      [("σ½ = (σ₀ + σ_f)/2 ≈ 0,265 S/m", "sigma un demi égale environ zéro virgule deux cent soixante-cinq"), ("t½ = 7 min", "t un demi égale sept minutes")],
      [("دابا sigma f", "moment:point_final"), ("إذن x égale x max", "moment:inverse")]),
  sim("ex_4", "Question 4 : la vitesse à partir de dσ/dt",
      "v = (1/V)·dx/dt et dx/dt = (1/B)·dσ/dt.",
      "cinetique-tableau/vitesse.html?vue=definition", "La définition de la vitesse volumique et son unité",
      "شوف la formule: v de t égale un sur V، fois d x sur d t. اللول، un sur V: V هو le volume ديال le mélange. الثاني، d x sur d t: le coefficient directeur ديال la tangente. والوحدة: يلا V ب le mètre cube، كنلقاو mole par mètre cube. فالتمرين ديالنا: d x sur d t égale un sur B fois d sigma sur d t. إذن v égale un sur B fois V، fois d sigma sur d t. la pente سالبة، و B سالب: v de zéro égale environ un virgule quarante-neuf mole par mètre cube et par minute.",
      [("v = (1/(B·V))·dσ/dt", "إذن v égale un sur B fois V"), ("v(0) ≈ 1,49 mol·m⁻³·min⁻¹", "v de zéro égale environ un virgule quarante-neuf")],
      [("شوف la formule", "moment:formule"), ("اللول، un sur V", "moment:volume"), ("الثاني، d x sur d t", "moment:derivee"), ("والوحدة", "moment:unite")]),
  sim("ex_5", "Question 5 : lire σ, calculer x, conclure",
      "Une valeur de σ lue sur la courbe donne x ; à 2·t½, x n'est que les trois quarts de x_max.",
      "cinetique-tableau/conductimetrie.html?vue=calcul", "De σ lue sur la courbe à x",
      "شوف على اليسار la courbe sigma en fonction du temps: كتهبط. دابا نختارو une date. نطلعو حتى la courbe، ونقراو sigma. دابا الحساب: من sigma كنحسبو x. ونحطو هاد النقطة، على la courbe x en fonction du temps. فالتمرين ديالنا: à quatorze minutes، sigma égale zéro virgule deux cent onze، إذن x égale environ deux virgule vingt-six fois dix puissance moins trois mole، trois quarts ديال x max. la réaction ما ساليتش.",
      [("x = (σ − A)/B ≈ 2,26 × 10⁻³ mol", "إذن x égale environ deux virgule vingt-six"), ("x < x_max : pas terminée à 2·t½", "la réaction ما ساليتش")],
      [("شوف على اليسار la courbe", "moment:courbe_sigma"), ("دابا نختارو une date", {"set": {"t": 10}}),
       ("نطلعو حتى la courbe", "moment:date"), ("ونقراو sigma", "moment:lecture"), ("دابا الحساب", "moment:calcul"), ("ونحطو هاد النقطة", "moment:report")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : le réactif limitant", "سؤال ساهل على le réactif limitant.",
      "n₀(HO⁻) = 3,0 × 10⁻³ mol, n₀(ester) = 4,0 × 10⁻³ mol, coefficients 1 et 1. Le réactif limitant est…",
      ["l'ester", "les ions hydroxyde", "les ions sodium"], 1, {
        1: ("juste", "برافو! trois virgule zéro صغيرة من quatre virgule zéro.", "Juste : HO⁻ est en plus petite quantité."),
        0: (("لا، l'ester عندو quatre virgule zéro، كثر. هو اللي en excès. عاود اختار.", "L'ester est en plus grande quantité : il est en excès. Réessaie."),
            ("الجواب: les ions hydroxyde، trois virgule zéro fois dix puissance moins trois mole.", "Réponse : les ions HO⁻.")),
        2: (("لا، les ions sodium spectateurs: ما كيتفاعلوش. عاود اختار.", "Les ions sodium sont spectateurs. Réessaie."),
            ("الجواب: les ions hydroxyde.", "Réponse : les ions HO⁻."))},
      "n zéro des ions hydroxyde égale trois virgule zéro fois dix puissance moins trois mole, n zéro de l'ester égale quatre virgule zéro. Le réactif limitant est ?"),
  assoc("fa_2", "Plus facile : associer", "À une date t, dans le mélange de volume V.",
        "سؤال ساهل: ربط كل ion مع la concentration ديالو.",
        "Relie chaque ion à sa concentration à la date t.",
        [("1", "Na⁺"), ("2", "HO⁻"), ("3", "HCOO⁻")],
        [("a", "n₀/V"), ("b", "(n₀ − x)/V"), ("c", "x/V")],
        {"1": "a", "2": "b", "3": "c"},
        {"1-a": (True, "Oui : spectateur, sa quantité ne change pas.", "برافو: spectateur، ما كيتبدلش."),
         "1-*": (False, "Les ions sodium ne réagissent pas : leur quantité reste n₀.", "لا، les ions sodium ما كيتفاعلوش."),
         "2-b": (True, "Oui : réactif, il en reste n₀ − x.", "برافو: réactif، كيبقى n zéro moins x."),
         "2-*": (False, "HO⁻ est un réactif : sa quantité diminue de x.", "لا، H O moins réactif، كينقص ب x."),
         "3-c": (True, "Oui : produit, il s'en forme x.", "برافو: produit، كيتكون x."),
         "3-*": (False, "HCOO⁻ est un produit : au départ il n'y en a pas.", "لا، l'ion méthanoate produit، فالبداية ما كاينش.")},
        ("Na⁺ : n₀/V ; HO⁻ : (n₀ − x)/V ; HCOO⁻ : x/V. On remplace dans σ = Σ λᵢ·[Xᵢ].", "sodium n zéro sur V، hydroxyde n zéro moins x sur V، méthanoate x sur V. ومن بعد كنعوضو ف sigma.")),
  qcm("fa_3", "Plus facile : σ à t½", "سؤال ساهل على sigma un demi.",
      "σ₀ = 0,374 S/m et σ_f = 0,157 S/m. À t½, σ vaut…",
      ["0,187 S/m", "0,079 S/m", "0,265 S/m"], 2, {
        2: ("juste", "برافو! sigma un demi هي الوسط بين sigma zéro و sigma f.", "Juste : (0,374 + 0,157)/2 ≈ 0,265 S/m."),
        0: (("هادا هو le piège: sigma zéro sur deux. sigma ما كتوصلش ل zéro، كتوقف ف sigma f. عاود اختار.", "Piège : σ₀/2. σ ne tend pas vers 0 mais vers σ_f. Réessaie."),
            ("الجواب: zéro virgule deux cent soixante-cinq: sigma zéro plus sigma f، sur deux.", "Réponse : (σ₀ + σ_f)/2 ≈ 0,265 S/m.")),
        1: (("لا، هادي sigma f sur deux. خاصنا الوسط بين sigma zéro و sigma f. عاود اختار.", "C'est σ_f/2 ; il faut le milieu de σ₀ et σ_f. Réessaie."),
            ("الجواب: zéro virgule deux cent soixante-cinq siemens par mètre.", "Réponse : ≈ 0,265 S/m."))},
      "sigma zéro égale zéro virgule trois cent soixante-quatorze et sigma f égale zéro virgule cent cinquante-sept. À t un demi, sigma vaut ?"),
  qcm("fa_4", "Plus facile : le signe de v", "سؤال ساهل على le signe.",
      "Ici dσ/dt < 0 et B < 0. La vitesse v = (1/(B·V))·dσ/dt est…",
      ["négative, car σ diminue", "positive", "nulle, car σ diminue"], 1, {
        1: ("juste", "برافو! سالب على سالب كيعطي موجب، و la vitesse volumique ديما موجبة.", "Juste : (négatif)/(négatif) > 0 ; une vitesse volumique est positive."),
        0: (("لا، B حتى هو سالب. سالب على سالب؟ عاود اختار.", "B est négatif aussi : négatif sur négatif ? Réessaie."),
            ("الجواب: موجبة.", "Réponse : v > 0.")),
        2: (("لا، sigma كتنقص يعني d sigma sur d t ماشي zéro. عاود اختار.", "σ varie, donc dσ/dt ≠ 0. Réessaie."),
            ("الجواب: موجبة: سالب على سالب.", "Réponse : v > 0."))},
      "Ici, d sigma sur d t est négatif et B est négatif. La vitesse est ?"),
  vf("fa_5", "Plus facile : vrai ou faux", "x(2·t½) ≈ 2,26 × 10⁻³ mol et x_max = 3,0 × 10⁻³ mol.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("À 2·t½, la réaction est terminée.", False, "x ≈ 0,75·x_max : il reste des ions HO⁻."),
      ("La réaction est terminée quand σ atteint le palier σ_f.", True, "Au palier, x ne varie plus : x = x_max."),
      ("x se calcule à partir de σ par x = (σ − A)/B.", True, "On isole x dans σ = A + B·x.")]),
]

SIM_Q = [
  QS("1", "Déterminer x_max et le réactif limitant.",
     val("x_max", sXM, "mol", "HO⁻ limitant : x_max = 5,0 × 10⁻³ mol"),
     (["n₀ − x_max = 0"], ["x_max = 6,0 × 10⁻³ mol"]),
     [("hypothèses : 5,0 × 10⁻³ (HO⁻) ou 6,0 × 10⁻³ mol (ester)", "deux hypothèses"), ("x_max = 5,0 × 10⁻³ mol, HO⁻ limitant", "x max égale cinq virgule zéro")],
     "deux hypothèses: cinq virgule zéro ولا six virgule zéro fois dix puissance moins trois mole. x max égale cinq virgule zéro fois dix puissance moins trois mole، les ions hydroxyde limitant."),
  QS("2", "Montrer que σ = A + B·x et calculer A et B (V = 250 mL).",
     val("B", sB, "S·m⁻¹·mol⁻¹", "A = 24,91 × 10⁻³ × 5,0 × 10⁻³/(2,5 × 10⁻⁴) ≈ 0,498 S/m ; B = −14,44 × 10⁻³/(2,5 × 10⁻⁴) = −57,8 S·m⁻¹·mol⁻¹", tol=0.02),
     (["σ = Σ λᵢ·[Xᵢ]", "V en m³"], ["B > 0"]),
     [("σ = (λ(Na⁺) + λ(HO⁻))·n₀/V − (λ(HO⁻) − λ(HCOO⁻))·x/V", "sigma égale A plus B fois x"),
      ("A ≈ 0,498 S/m ; B ≈ −57,8 S·m⁻¹·mol⁻¹", "B égale environ moins cinquante-sept virgule huit")],
     "sigma égale A plus B fois x. A égale environ zéro virgule quatre cent quatre-vingt-dix-huit siemens par mètre، و B égale environ moins cinquante-sept virgule huit."),
  QS("3", "Déterminer t½.",
     val("t½", sT12, "min", "σ½ = (0,498 + 0,209)/2 ≈ 0,354 S/m ; t½ = 5 min", tol=0.06),
     (["σ½ = (σ₀ + σ_f)/2"], ["σ½ = σ₀/2"]),
     [("σ_f = A + B·x_max ≈ 0,209 S/m ; σ½ = (σ₀ + σ_f)/2 ≈ 0,354 S/m", "sigma un demi"), ("t½ = 5 min", "t un demi égale cinq minutes")],
     "sigma f égale environ zéro virgule deux cent neuf، و sigma un demi égale environ zéro virgule trois cent cinquante-quatre. على la courbe: t un demi égale cinq minutes."),
  QS("4", "Montrer que v = (1/(B·V))·dσ/dt, puis calculer v(0) en mol·m⁻³·min⁻¹.",
     val("v(0)", sV0, "mol·m⁻³·min⁻¹", "v(0) = ((0,258 − 0,498)/6)/(−57,76 × 2,5 × 10⁻⁴) ≈ 2,77 mol·m⁻³·min⁻¹", tol=0.04),
     (["dσ/dt = B·dx/dt", "B·V"], ["v < 0"]),
     [("v = (1/(B·V))·dσ/dt ; (dσ/dt)₀ = −0,040 S·m⁻¹·min⁻¹", "la pente"), ("v(0) ≈ 2,77 mol·m⁻³·min⁻¹", "v de zéro égale environ deux virgule soixante-dix-sept")],
     "v égale un sur B fois V، fois d sigma sur d t. la pente égale moins zéro virgule zéro quarante. v de zéro égale environ deux virgule soixante-dix-sept moles par mètre cube et par minute."),
  QS("5", "On lit σ(2·t½ = 10 min) = 0,282 S/m. Calculer x(10 min) et discuter « à 2·t½ la réaction est terminée ».",
     val("x(10)", sX10, "mol", "x = (0,282 − 0,498)/(−57,76) ≈ 3,74 × 10⁻³ mol", tol=0.04),
     (["x = (σ − A)/B"], ["x = σ/B"]),
     [("x = (σ − A)/B ≈ 3,74 × 10⁻³ mol ≈ 0,75·x_max", "x égale environ trois virgule soixante-quatorze"), ("x < x_max : affirmation fausse", "l'affirmation fausse")],
     "x égale sigma moins A، sur B: x égale environ trois virgule soixante-quatorze fois dix puissance moins trois mole، تقريبا trois quarts ديال x max. إذن l'affirmation fausse."),
]

EX = exercice(
  "phys_ex_ch10_cinetique_7", "phys_ch10_cinetique", "cinetique",
  "La saponification du méthanoate d'éthyle : σ = A + B·x", "difficile", 40,
  ["Déterminer x_max avec un réactif en excès", "Établir σ = A + B·x et calculer A et B", "Déterminer t½ à partir de σ½",
   "Établir et calculer v à partir de dσ/dt", "Discuter « la réaction est finie à 2·t½ »"],
  "À t = 0, on mélange une solution d'hydroxyde de sodium (Na⁺ + HO⁻) contenant n₀(HO⁻) = 3,0 × 10⁻³ mol et n₀(ester) = 4,0 × 10⁻³ mol de méthanoate d'éthyle ; le volume du mélange est V = 200 mL, constant. La réaction, lente et totale, a pour équation : " + EQ + ". On suit la conductivité σ du mélange ; la figure donne σ en fonction du temps et la tangente (T) en t = 0.",
  "دابا نقراو l'énoncé. فt égale zéro، كنخلطو la soude، فيها trois virgule zéro fois dix puissance moins trois mole ديال les ions hydroxyde، مع quatre virgule zéro fois dix puissance moins trois mole ديال l'ester، le méthanoate d'éthyle. le volume ديال le mélange deux cents millilitres، ثابت. la réaction بطيئة و totale: l'ester، plus l'ion hydroxyde، كيعطيو l'ion méthanoate و l'éthanol. كنتبعو la conductivité sigma، و la figure كتعطي sigma en fonction du temps، مع la tangente T à t égale zéro.",
  [FIG],
  ["V = 200 mL (constant) ; n₀(HO⁻) = n₀(Na⁺) = 3,0 × 10⁻³ mol ; n₀(ester) = 4,0 × 10⁻³ mol",
   "λ(Na⁺) = 5,01 mS·m²·mol⁻¹ ; λ(HO⁻) = 19,9 mS·m²·mol⁻¹ ; λ(HCOO⁻) = 5,46 mS·m²·mol⁻¹",
   "Tangente (T) : P(0 ; 0,374 S/m) et Q(8 min ; 0,202 S/m)", "Question 5 : σ(14 min) = 0,211 S/m"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Même réaction, mais V = 250 mL, n₀(HO⁻) = n₀(Na⁺) = 5,0 × 10⁻³ mol et n₀(ester) = 6,0 × 10⁻³ mol. La figure donne σ en fonction du temps et la tangente (T) en t = 0.",
  "نفس التمرين، بقيم أخرى: deux cent cinquante millilitres، cinq virgule zéro fois dix puissance moins trois mole ديال les ions hydroxyde، و six virgule zéro ديال l'ester.",
  [sFIG],
  ["V = 250 mL ; n₀(HO⁻) = 5,0 × 10⁻³ mol ; n₀(ester) = 6,0 × 10⁻³ mol", "λ : mêmes valeurs", "(T) : P(0 ; 0,498 S/m) et Q(6 min ; 0,258 S/m)", "Question 5 : σ(10 min) = 0,282 S/m"],
  SIM_Q)

ecrire(EX)
