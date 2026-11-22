# Exercice de chimie, ch. 12 (état d'équilibre), niveau moyen (celui du national) : mesurer K par la conductimétrie
# (G = k·σ, σ = (λ₁ + λ₂)·[H₃O⁺]éq, le piège mol/m³), puis l'effet d'une dilution sur τ et sur K.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2019 N (2.3.1 σ → [H₃O⁺]éq, 2.3.2 montrer τ = σ/(C(λ₁ + λ₂)), 2.4 K en
#    fonction de C et τ), 2016 R (2.3.1 σ½ à partir de σ = f(x)), 2018 R (2.2.1 conductance G½), 2021 R (10-11 effet
#    de la dilution sur τ) — backend/data/exams/physique ;
#  - profs (architecture/phys_ch12_etat_equilibre.md § 1 et § 6 : El Goufifa, Moutamadris, fiche 2BAC : Qr,éq par
#    conductimétrie ; aucun ne détaille G = k·σ) ; pièges relevés : [Xᵢ] en mol·m⁻³ dans σ = Σλᵢ[Xᵢ], σ donnée en
#    mS·m⁻¹, négliger [HO⁻] sans le dire ;
#  - séries en ligne : alloschool (El Goufifa, séance 9 : acide méthanoïque, acide benzoïque), moutamadris (exercices
#    état d'équilibre), talamidi (état d'équilibre, activités 1), Naceiri Mrabti (livre 2BAC, activité des trois
#    solutions par σ), docs Google d'un prof BIOF, coursdusoirpc (TD BIOF).
# Ici : l'acide méthanoïque à nos concentrations, notre cellule (k = 5,0 × 10⁻² m) et nos conductances (calculées à
# partir de K = 1,8 × 10⁻⁴).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch12 import *

L1, L2 = 35.0e-3, 5.46e-3          # S·m²·mol⁻¹ : H3O+, HCOO-
LS = L1 + L2
KC = 5.0e-2                         # constante de cellule (m) : G = k·σ


def mesures(C, G):
    sig = G / KC                    # S/m
    hm3 = sig / LS                  # mol/m³
    h = hm3 / 1000                  # mol/L
    tau = h / C
    return sig, hm3, h, tau, C * tau ** 2 / (1 - tau)


C, G, Gd = 2.0e-3, 1.05e-3, 0.452e-3
SIG, HM3, H, TAU, K = mesures(C, G)
Cd = C / 4
SIGd, HM3d, Hd, TAUd, Kd = mesures(Cd, Gd)
assert fr(SIG, 3) == "0,021" and fr(HM3, 3) == "0,519" and sci(H, 1) == "5,2 × 10⁻⁴" and fr(TAU, 2) == "0,26"
assert sci(K, 1) == "1,8 × 10⁻⁴" and fr(TAUd, 2) == "0,45" and abs(Kd / K - 1) < 0.03
sC, sG, sGd = 4.0e-3, 1.54e-3, 0.695e-3
sSIG, sHM3, sH, sTAU, sK = mesures(sC, sG)
sCd = sC / 4
sSIGd, sHM3d, sHd, sTAUd, sKd = mesures(sCd, sGd)
assert fr(sSIG, 4) == "0,0308" and fr(sTAU, 2) == "0,19" and sci(sK, 1) == "1,8 × 10⁻⁴" and fr(sTAUd, 2) == "0,34" and abs(sKd / sK - 1) < 0.03

VUES["conductance"] = ("etat-equilibre-tableau/conductimetrie.html?vue=relation", "Le conductimètre : G = k·σ",
    "شوف la cellule: deux plaques قدام بعضياتهم، كندخلوهم فالمحلول. le conductimètre كيقيس la conductance G، en siemens. la relation: G égale k fois sigma. k هي la constante de cellule، كتعلق غير ب la cellule، en mètre. و sigma هي la conductivité ديال المحلول، en siemens par mètre.",
    [("شوف la cellule", "moment:mesure")])

EQ = "HCOOH(aq) + H₂O(l) ⇌ HCOO⁻(aq) + H₃O⁺(aq)"
SREL = "σ = λ(H₃O⁺)·[H₃O⁺]éq + λ(HCOO⁻)·[HCOO⁻]éq = (λ₁ + λ₂)·[H₃O⁺]éq"

QUESTIONS = [
  Q("1", "Écrire l'équation de la réaction de l'acide méthanoïque avec l'eau, puis montrer que σ = (λ₁ + λ₂)·[H₃O⁺]éq (on néglige les ions HO⁻).",
    "السؤال un: كتب l'équation ديال l'acide méthanoïque مع الما، ومن بعد بين بلي sigma égale lambda un plus lambda deux، fois la concentration des ions H trois O plus à l'équilibre.",
    phrase(EQ + " ; " + SREL + " car [HCOO⁻]éq = [H₃O⁺]éq (tableau d'avancement)"),
    (["⇌", "σ = Σλᵢ·[Xᵢ]", "[HCOO⁻]éq = [H₃O⁺]éq", "λ₁ + λ₂"], ["σ = λ₁·λ₂·[H₃O⁺]", "[HO⁻]"]),
    [("Quels ions portent le courant dans la solution ? Écris la contribution de chacun : λᵢ·[Xᵢ].",
      "شكون les ions اللي كيوصلو التيار فالمحلول؟ كتب la part ديال كل واحد: lambda fois la concentration."),
     ("Le tableau d'avancement donne [HCOO⁻]éq = [H₃O⁺]éq : mets la concentration en facteur commun.",
      "le tableau d'avancement كيعطي: la concentration des ions méthanoate égale celle des ions H trois O plus. خرجها facteur commun.")],
    [("1 : " + EQ, "l'acide méthanoïque، plus الما"),
     ("σ = λ₁·[H₃O⁺]éq + λ₂·[HCOO⁻]éq", "sigma égale lambda un fois"),
     ("[HCOO⁻]éq = [H₃O⁺]éq donc σ = (λ₁ + λ₂)·[H₃O⁺]éq", "facteur commun")],
    "السؤال un. l'acide méthanoïque، plus الما، ب la double flèche، كيعطيو les ions méthanoate، plus les ions H trois O plus. les ions اللي كيوصلو التيار: sigma égale lambda un fois la concentration des ions H trois O plus، plus lambda deux fois la concentration des ions méthanoate. من le tableau، جوج التراكيز متساويين، إذن نخرجوها facteur commun: sigma égale lambda un plus lambda deux، fois la concentration des ions H trois O plus.",
    "ex_1", "fa_1"),
  Q("2", "La conductance mesurée est G = 1,05 mS avec une cellule de constante k = 5,0 × 10⁻² m. Calculer la conductivité σ de la solution, en S·m⁻¹.",
    "السؤال deux: la conductance اللي قسنا، G égale un virgule zéro cinq millisiemens، و la constante de cellule k égale cinq virgule zéro fois dix puissance moins deux mètre. حسب sigma، en siemens par mètre.",
    val("σ", SIG, "S/m", f"σ = G/k = 1,05 × 10⁻³/(5,0 × 10⁻²) = {sci(SIG, 1)} S·m⁻¹"),
    (["G = k·σ", "σ = G/k", "mS = 10⁻³ S", "S·m⁻¹"], ["σ = k·G", "σ = G·k"]),
    [("Quelle relation lie G, k et σ ? Mets G en siemens.", "شنو la relation بين G و k و sigma؟ ورد G ب siemens."),
     ("G = k·σ donc σ = G/k, avec G = 1,05 × 10⁻³ S.", "G égale k fois sigma، إذن sigma égale G sur k، و G égale un virgule zéro cinq fois dix puissance moins trois siemens.")],
    [("2 : G = k·σ donc σ = G/k", "sigma égale G sur k"),
     (f"σ = 1,05 × 10⁻³/(5,0 × 10⁻²) = {sci(SIG, 1)} S·m⁻¹", f"sigma égale {dsci(SIG, 1)} siemens par mètre")],
    f"السؤال deux. G égale k fois sigma، إذن sigma égale G sur k: un virgule zéro cinq fois dix puissance moins trois، sur cinq virgule zéro fois dix puissance moins deux. sigma égale {dsci(SIG, 1)} siemens par mètre.",
    "ex_2", "fa_2"),
  Q("3", "Calculer [H₃O⁺]éq en mol·m⁻³, puis en mol·L⁻¹.",
    "السؤال trois: حسب la concentration des ions H trois O plus à l'équilibre، ب mole par mètre cube، ومن بعد ب mole par litre.",
    val("[H₃O⁺]éq", H, "mol/L", f"[H₃O⁺]éq = σ/(λ₁ + λ₂) = {sci(SIG, 1)}/(40,46 × 10⁻³) = {fr(HM3, 3)} mol·m⁻³ = {sci(H, 1)} mol/L"),
    (["[H₃O⁺]éq = σ/(λ₁ + λ₂)", "mol·m⁻³", "1 mol/L = 10³ mol·m⁻³", "mol/L"], ["× 1000", "[H₃O⁺] = σ·(λ₁ + λ₂)"]),
    [("Isole [H₃O⁺]éq dans la relation de la question 1. Avec σ en S·m⁻¹ et λ en S·m²·mol⁻¹, dans quelle unité sort-elle ?",
      "خرج la concentration من la relation ديال السؤال un. ب sigma ب siemens par mètre، و lambda ب siemens mètre carré par mole، ب شنو كتخرج la concentration؟"),
     ("[H₃O⁺]éq = σ/(λ₁ + λ₂) sort en mol·m⁻³ ; 1 mol/L = 1000 mol·m⁻³ : divise par 1000.",
      "la concentration égale sigma sur lambda un plus lambda deux، وكتخرج ب mole par mètre cube. un mole par litre égale mille moles par mètre cube: قسم على mille.")],
    [("3 : [H₃O⁺]éq = σ/(λ₁ + λ₂)", "sigma sur lambda un plus lambda deux"),
     (f"[H₃O⁺]éq = {sci(SIG, 1)}/(40,46 × 10⁻³) = {fr(HM3, 3)} mol·m⁻³", f"{dfr(HM3, 3)} mole par mètre cube"),
     (f"[H₃O⁺]éq = {sci(H, 1)} mol·L⁻¹", f"{dsci(H, 1)} mole par litre")],
    f"السؤال trois. la concentration des ions H trois O plus égale sigma sur lambda un plus lambda deux: {dsci(SIG, 1)}، sur quarante virgule quarante-six fois dix puissance moins trois. égale {dfr(HM3, 3)} mole par mètre cube. نقسمو على mille: {dsci(H, 1)} mole par litre.",
    "ex_3", "fa_3"),
  Q("4", "Calculer le taux d'avancement final τ de la réaction. Conclure.",
    "السؤال quatre: حسب tau، le taux d'avancement final، واستنتج.",
    val("τ", TAU, None, f"τ = x_éq/x_max = [H₃O⁺]éq/C = {sci(H, 2)}/(2,0 × 10⁻³) ≈ {fr(TAU, 2)} < 1 : réaction limitée", tol=0.05),
    (["τ = x_éq/x_max", "τ = [H₃O⁺]éq/C", "< 1"], ["τ = C/[H₃O⁺]", "C en mol·m⁻³ avec [H₃O⁺] en mol/L"]),
    [("x_max = C·V (l'eau en excès) et x_éq = [H₃O⁺]éq·V : V se simplifie.", "x max égale C fois V، و x éq égale la concentration des ions H trois O plus fois V. و V كيتحيد."),
     ("τ = [H₃O⁺]éq/C, les deux en mol/L.", "tau égale la concentration des ions H trois O plus، sur C، بجوج ب mole par litre.")],
    [("4 : τ = [H₃O⁺]éq/C", "la concentration des ions H trois O plus، sur C"),
     (f"τ = {sci(H, 2)}/(2,0 × 10⁻³) ≈ {fr(TAU, 2)}", f"tau égale {dfr(TAU, 2)}"),
     ("τ < 1 : la réaction est limitée", "la réaction محدودة")],
    f"السؤال quatre. tau égale x éq sur x max، يعني la concentration des ions H trois O plus، sur C. l'application numérique: {dsci(H, 2)}، sur deux virgule zéro fois dix puissance moins trois. tau égale {dfr(TAU, 2)}، صغير من un: la réaction محدودة.",
    "ex_4", "fa_4"),
  Q("5", "Montrer que K = C·τ²/(1 − τ), puis calculer K.",
    "السؤال cinq: بين بلي K égale C fois tau au carré، sur un moins tau، ومن بعد حسب K.",
    val("K", K, None, f"[HCOO⁻]éq = [H₃O⁺]éq = C·τ ; [HCOOH]éq = C(1 − τ) ; K = C·τ²/(1 − τ) = 2,0 × 10⁻³ × {fr(TAU, 3)}²/(1 − {fr(TAU, 3)}) = {sci(K, 1)}", tol=0.05),
    (["K = Qr,éq", "C·τ", "C(1 − τ)", "C·τ²/(1 − τ)"], ["K = C·τ", "[HCOOH]éq = C"]),
    [("Écris les trois concentrations à l'équilibre avec C et τ, puis remplace-les dans K = Qr,éq.",
      "كتب les trois concentrations à l'équilibre ب C و tau، ومن بعد عوضهم ف K égale Q r à l'équilibre."),
     ("[HCOO⁻]éq = [H₃O⁺]éq = C·τ, [HCOOH]éq = C(1 − τ) ; un C se simplifie.",
      "les ions méthanoate و les ions H trois O plus: C fois tau. l'acide: C fois un moins tau. واحد C كيتحيد.")],
    [("5 : [HCOO⁻]éq = [H₃O⁺]éq = C·τ ; [HCOOH]éq = C(1 − τ)", "C fois tau"),
     ("K = (C·τ)²/(C(1 − τ)) = C·τ²/(1 − τ)", "C fois tau au carré، sur un moins tau"),
     (f"K = 2,0 × 10⁻³ × {fr(TAU, 3)}²/(1 − {fr(TAU, 3)}) = {sci(K, 1)}", f"K égale {dsci(K, 1)}")],
    f"السؤال cinq. les ions méthanoate و les ions H trois O plus: C fois tau. l'acide: C fois un moins tau. K égale Q r à l'équilibre، وواحد C كيتحيد: K égale C fois tau au carré، sur un moins tau. l'application numérique: deux virgule zéro fois dix puissance moins trois، fois {dfr(TAU, 3)} au carré، sur un moins {dfr(TAU, 3)}. K égale {dsci(K, 1)}.",
    "ex_5", "fa_5"),
  Q("6", "On dilue quatre fois la solution (C' = 5,0 × 10⁻⁴ mol/L) ; la conductance devient G' = 0,452 mS (même cellule). Calculer le nouveau taux τ'. Quel est l'effet de la dilution sur τ et sur K ?",
    "السؤال six: كنخففو la solution quatre fois، C prime égale cinq virgule zéro fois dix puissance moins quatre mole par litre، و la conductance ولات zéro virgule quatre cent cinquante-deux millisiemens. حسب tau prime. شنو l'effet ديال la dilution على tau و على K؟",
    val("τ'", TAUd, None, f"σ' = G'/k = {sci(SIGd, 2)} S·m⁻¹ ; [H₃O⁺]' = {fr(HM3d, 3)} mol·m⁻³ = {sci(Hd, 2)} mol/L ; C'·τ'²/(1 − τ') redonne K ≈ {sci(Kd, 1)} (inchangée) ; τ' = {sci(Hd, 2)}/(5,0 × 10⁻⁴) ≈ {fr(TAUd, 2)} > τ", tol=0.05),
    (["σ = G/k", "σ/(λ₁ + λ₂)", "÷ 1000", "τ = [H₃O⁺]/C"], ["K diminue", "τ' = τ/4"]),
    [("Refais les étapes 2, 3 et 4 avec G' et C'.", "عاود les étapes deux و trois و quatre ب G prime و C prime."),
     ("σ' = G'/k, [H₃O⁺]' = σ'/(λ₁ + λ₂) ÷ 1000, τ' = [H₃O⁺]'/C'. Puis calcule C'·τ'²/(1 − τ') et compare à K.",
      "sigma prime égale G prime sur k. la concentration égale sigma prime sur la somme des lambda، وقسم على mille. tau prime égale la concentration sur C prime. ومن بعد حسب C prime fois tau prime au carré، sur un moins tau prime، وقارن مع K.")],
    [(f"6 : σ' = G'/k = {sci(SIGd, 2)} S·m⁻¹ ; [H₃O⁺]' = {sci(Hd, 2)} mol/L", "sigma prime égale G prime sur k"),
     (f"τ' = {sci(Hd, 2)}/(5,0 × 10⁻⁴) ≈ {fr(TAUd, 2)} > τ = {fr(TAU, 2)}", f"tau prime égale {dfr(TAUd, 2)}"),
     (f"C'·τ'²/(1 − τ') ≈ {sci(Kd, 1)} = K : la dilution augmente τ, K ne change pas", "K ما كتبدلش")],
    f"السؤال six. sigma prime égale G prime sur k، يعني {dsci(SIGd, 2)} siemens par mètre. la concentration des ions H trois O plus: {dsci(Hd, 2)} mole par litre. tau prime égale {dfr(TAUd, 2)}، كبر من {dfr(TAU, 2)}. و C prime fois tau prime au carré، sur un moins tau prime، كتعطي {dsci(Kd, 1)}: نفس K. إذن la dilution كتكبر tau، و K ما كتبدلش.",
    "ex_6", "fa_6"),
]

EXPLICATIONS = [
  slide("ex_1", "cond_rel", "Question 1 : σ = (λ₁ + λ₂)·[H₃O⁺]éq",
        "Deux ions portent le courant ; le tableau dit qu'ils ont la même concentration.",
        "فالتمرين ديالنا، نفس الشي: les ions H trois O plus، و les ions méthanoate. إذن sigma égale lambda un plus lambda deux، fois la concentration des ions H trois O plus à l'équilibre.",
        [(SREL, "فالتمرين ديالنا، نفس الشي")]),
  slide("ex_2", "conductance", "Question 2 : σ = G/k",
        "Le conductimètre lit G ; la cellule a sa constante k : σ = G/k.",
        f"فالتمرين ديالنا: G égale un virgule zéro cinq millisiemens، يعني un virgule zéro cinq fois dix puissance moins trois siemens، و k égale cinq virgule zéro fois dix puissance moins deux mètre. إذن sigma égale G sur k، يعني {dsci(SIG, 1)} siemens par mètre.",
        [("σ = G/k", "إذن sigma égale G sur k"), (f"σ = {sci(SIG, 1)} S·m⁻¹", f"يعني {dsci(SIG, 1)} siemens par mètre")]),
  slide("ex_3", "cond_calc", "Question 3 : [H₃O⁺]éq, et la conversion",
        "σ/(λ₁ + λ₂) sort en mol·m⁻³ : on divise par 1000 pour avoir des mol/L.",
        f"فالتمرين ديالنا: {dsci(SIG, 1)}، sur quarante virgule quarante-six fois dix puissance moins trois، كتعطي {dfr(HM3, 3)} mole par mètre cube. نقسمو على mille: {dsci(H, 1)} mole par litre.",
        [(f"[H₃O⁺]éq = {fr(HM3, 3)} mol·m⁻³", f"كتعطي {dfr(HM3, 3)} mole par mètre cube"), (f"= {sci(H, 1)} mol/L", f"نقسمو على mille: {dsci(H, 1)}")]),
  slide("ex_4", "taux", "Question 4 : τ = [H₃O⁺]éq/C",
        "x_éq/x_max : la même relation, ici avec la concentration trouvée par σ.",
        f"فالتمرين ديالنا، la concentration des ions H trois O plus جات من sigma: tau égale {dsci(H, 2)}، sur deux virgule zéro fois dix puissance moins trois، يعني {dfr(TAU, 2)}. صغير من un: la réaction محدودة.",
        [("τ = [H₃O⁺]éq/C", "فالتمرين ديالنا، la concentration"), (f"τ ≈ {fr(TAU, 2)} < 1", f"يعني {dfr(TAU, 2)}")]),
  slide("ex_5", "c_tau", "Question 5 : K = C·τ²/(1 − τ)",
        "Les concentrations à l'équilibre en C et τ, puis K = Qr,éq.",
        f"فالتمرين ديالنا: K égale deux virgule zéro fois dix puissance moins trois، fois {dfr(TAU, 3)} au carré، sur un moins {dfr(TAU, 3)}. K égale {dsci(K, 1)}.",
        [(f"K = 2,0 × 10⁻³ × {fr(TAU, 3)}²/(1 − {fr(TAU, 3)}) = {sci(K, 1)}", f"K égale {dsci(K, 1)}")]),
  slide("ex_6", "dilution", "Question 6 : diluer quatre fois",
        "Même acide, même température : même K, et τ plus grand.",
        f"فالتمرين ديالنا: ب C prime égale cinq virgule zéro fois dix puissance moins quatre mole par litre، tau prime égale {dfr(TAUd, 2)}، كبر من {dfr(TAU, 2)}. و K بقات {dsci(Kd, 1)}: ما تبدلاتش.",
        [(f"τ' ≈ {fr(TAUd, 2)} > τ ≈ {fr(TAU, 2)}", f"tau prime égale {dfr(TAUd, 2)}"), ("K inchangée", "ما تبدلاتش")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : l'expression de σ", "سؤال ساهل: اختار l'expression ديال sigma.",
      "Dans la solution d'acide méthanoïque (HO⁻ négligés), σ = …",
      ["λ₁·λ₂·[H₃O⁺]éq", "(λ₁ + λ₂)·[H₃O⁺]éq", "λ₁·[H₃O⁺]éq"], 1, {
        1: ("juste", "برافو! deux ions كيوصلو التيار، وعندهم نفس la concentration: lambda un plus lambda deux، fois la concentration.", "Juste : σ = (λ₁ + λ₂)·[H₃O⁺]éq."),
        0: (("لا، sigma هي مجموع: كل ion كيزيد la part ديالو. ماشي ضرب lambda fois lambda. عاود اختار.", "σ est une somme de contributions, pas un produit. Réessaie."),
            ("الجواب: sigma égale lambda un plus lambda deux، fois la concentration.", "Réponse : σ = (λ₁ + λ₂)·[H₃O⁺]éq.")),
        2: (("قريب! ولكن نسيتي les ions méthanoate: حتى هوما كيوصلو التيار. عاود اختار.", "Les ions HCOO⁻ conduisent aussi. Réessaie."),
            ("الجواب: deux ions، إذن lambda un plus lambda deux.", "Réponse : σ = (λ₁ + λ₂)·[H₃O⁺]éq."))},
      "Dans la solution d'acide méthanoïque، sigma égale quoi ?"),
  qcm("fa_2", "Plus facile : σ à partir de G", "سؤال ساهل: من G ل sigma.",
      "G = 1,05 × 10⁻³ S et k = 5,0 × 10⁻² m. σ vaut…",
      ["5,3 × 10⁻⁵ S·m⁻¹", "2,1 × 10⁻² S·m⁻¹", "21 S·m⁻¹"], 1, {
        1: ("juste", "برافو! sigma égale G sur k، deux virgule un fois dix puissance moins deux siemens par mètre.", "Juste : σ = G/k = 2,1 × 10⁻² S·m⁻¹."),
        0: (("لا، هادي G fois k. la relation هي G égale k fois sigma، إذن sigma égale G sur k. عاود اختار.", "C'est G·k ; il faut σ = G/k. Réessaie."),
            ("الجواب: sigma égale G sur k، deux virgule un fois dix puissance moins deux.", "Réponse : σ = G/k = 2,1 × 10⁻² S·m⁻¹.")),
        2: (("قريب! ولكن G خاصها تكون ب siemens، ماشي ب millisiemens. عاود اختار.", "G doit être en siemens. Réessaie."),
            ("الجواب: deux virgule un fois dix puissance moins deux siemens par mètre.", "Réponse : σ = 1,05 × 10⁻³/5,0 × 10⁻² = 2,1 × 10⁻² S·m⁻¹."))},
      "G égale un virgule zéro cinq fois dix puissance moins trois siemens، و k égale cinq virgule zéro fois dix puissance moins deux mètre. sigma vaut ?"),
  qcm("fa_3", "Plus facile : la conversion", "سؤال ساهل على الوحدة.",
      "[H₃O⁺]éq = 0,519 mol·m⁻³. En mol/L, cela fait…",
      ["519 mol/L", "0,519 mol/L", "5,19 × 10⁻⁴ mol/L"], 2, {
        2: ("juste", "برافو! un mole par litre égale mille moles par mètre cube، إذن نقسمو على mille.", "Juste : 0,519/1000 = 5,19 × 10⁻⁴ mol/L."),
        0: (("لا، ضربتي ف mille. litre صغير من mètre cube: فكل litre كاين قل. عاود اختار.", "Un litre est plus petit qu'un m³ : il faut diviser par 1000. Réessaie."),
            ("الجواب: نقسمو على mille: cinq virgule dix-neuf fois dix puissance moins quatre mole par litre.", "Réponse : 5,19 × 10⁻⁴ mol/L.")),
        1: (("لا، نسيتي التحويل. mole par mètre cube ماشي mole par litre. عاود اختار.", "Tu n'as pas converti. Réessaie."),
            ("الجواب: cinq virgule dix-neuf fois dix puissance moins quatre mole par litre.", "Réponse : 0,519 mol·m⁻³ = 5,19 × 10⁻⁴ mol/L."))},
      "La concentration égale zéro virgule cinq cent dix-neuf mole par mètre cube. En mole par litre ?"),
  vf("fa_4", "Plus facile : vrai ou faux", "τ = [H₃O⁺]éq/C.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("Pour calculer τ, [H₃O⁺]éq et C doivent être dans la même unité.", True, "Les deux en mol/L : 5,19 × 10⁻⁴/2,0 × 10⁻³ ≈ 0,26."),
      ("τ = 0,26 : la réaction est totale.", False, "τ < 1 : la réaction est limitée."),
      ("x_max = C·V, car l'eau est en excès.", True, "L'acide est le réactif limitant.")]),
  qcm("fa_5", "Plus facile : la bonne expression de K", "سؤال ساهل: اختار l'expression ديال K.",
      "Pour un acide de concentration C et de taux τ, K = …",
      ["C·τ²/(1 − τ)", "C·τ/(1 − τ)", "τ²/(1 − τ)"], 0, {
        0: ("juste", "برافو! C fois tau au carré، sur un moins tau.", "Juste : K = C·τ²/(1 − τ)."),
        1: (("لا، فالفوق كاينين deux concentrations، كل وحدة C fois tau. إذن tau au carré. عاود اختار.", "Le numérateur a deux concentrations C·τ : τ au carré. Réessaie."),
            ("الجواب: C fois tau au carré، sur un moins tau.", "Réponse : K = C·τ²/(1 − τ).")),
        2: (("قريب! ولكن واحد C كيبقى: C au carré الفوق، و C التحت. عاود اختار.", "Un seul C se simplifie : il en reste un. Réessaie."),
            ("الجواب: C fois tau au carré، sur un moins tau.", "Réponse : K = C·τ²/(1 − τ)."))},
      "Pour un acide de concentration C et de taux tau، K égale quoi ?"),
  assoc("fa_6", "Plus facile : quand on dilue", "Dilution de la solution d'acide méthanoïque.",
        "سؤال ساهل: ربط كل grandeur مع شنو كيوقع ليها ملي كنخففو.",
        "Relie chaque grandeur à ce qu'elle devient quand on dilue la solution.",
        [("1", "τ"), ("2", "K"), ("3", "[H₃O⁺]éq")],
        [("a", "Augmente"), ("b", "Diminue"), ("c", "Ne change pas")],
        {"1": "a", "2": "c", "3": "b"},
        {"1-a": (True, "Oui : même K, C plus petite, τ plus grand.", "برافو: نفس K، و C صغرات، إذن tau كبر."),
         "1-*": (False, "Compare τ = 0,26 avant et τ' = 0,45 après.", "لا، قارن tau zéro virgule vingt-six قبل، و zéro virgule quarante-cinq من بعد."),
         "2-c": (True, "Oui : K ne dépend que de la température.", "برافو: K كتتعلق غير ب la température."),
         "2-*": (False, "K dépend-elle de la concentration ? Seulement de la température.", "لا، واش K كتتعلق ب la concentration؟ غير ب la température."),
         "3-b": (True, "Oui : moins d'acide par litre, moins d'ions H₃O⁺ (σ diminue).", "برافو: la conductance نقصات، إذن les ions H trois O plus نقصو."),
         "3-*": (False, "Regarde G : elle passe de 1,05 mS à 0,452 mS.", "لا، شوف G: نقصات من un virgule zéro cinq ل zéro virgule quatre cent cinquante-deux millisiemens.")},
        ("Quand on dilue : τ augmente, [H₃O⁺]éq diminue, K ne change pas.", "ملي كنخففو: tau كيكبر، la concentration des ions H trois O plus كتنقص، و K ما كتبدلش.")),
]

SIM_Q = [
  QS("1", "Écrire l'équation de HCOOH avec l'eau et montrer que σ = (λ₁ + λ₂)·[H₃O⁺]éq.",
     phrase(EQ + " ; " + SREL), (["⇌", "σ = Σλᵢ·[Xᵢ]"], ["σ = λ₁·λ₂·[H₃O⁺]"]),
     [(EQ, "l'acide méthanoïque، plus الما"), (SREL, "facteur commun")],
     "l'acide méthanoïque، plus الما، ب la double flèche، كيعطيو les ions méthanoate و les ions H trois O plus. جوج التراكيز متساويين، إذن facteur commun: sigma égale lambda un plus lambda deux، fois la concentration des ions H trois O plus."),
  QS("2", "G = 1,54 mS, k = 5,0 × 10⁻² m. Calculer σ.",
     val("σ", sSIG, "S/m", f"σ = G/k = 1,54 × 10⁻³/(5,0 × 10⁻²) = {sci(sSIG, 2)} S·m⁻¹"),
     (["σ = G/k"], ["σ = k·G"]),
     [(f"σ = G/k = {sci(sSIG, 2)} S·m⁻¹", f"{dsci(sSIG, 2)} siemens par mètre")],
     f"sigma égale G sur k، يعني {dsci(sSIG, 2)} siemens par mètre."),
  QS("3", "Calculer [H₃O⁺]éq en mol·m⁻³ puis en mol/L.",
     val("[H₃O⁺]éq", sH, "mol/L", f"[H₃O⁺]éq = {sci(sSIG, 2)}/(40,46 × 10⁻³) = {fr(sHM3, 3)} mol·m⁻³ = {sci(sH, 1)} mol/L"),
     (["σ/(λ₁ + λ₂)", "÷ 1000"], ["× 1000"]),
     [(f"[H₃O⁺]éq = {fr(sHM3, 3)} mol·m⁻³", f"{dfr(sHM3, 3)} mole par mètre cube"), (f"= {sci(sH, 1)} mol/L", f"{dsci(sH, 1)} mole par litre")],
     f"la concentration égale sigma sur la somme des lambda: {dfr(sHM3, 3)} mole par mètre cube، يعني {dsci(sH, 1)} mole par litre."),
  QS("4", "Calculer τ et conclure.",
     val("τ", sTAU, None, f"τ = {sci(sH, 2)}/(4,0 × 10⁻³) ≈ {fr(sTAU, 2)} < 1 : limitée", tol=0.05),
     (["τ = [H₃O⁺]éq/C"], ["τ = C/[H₃O⁺]"]),
     [(f"τ = [H₃O⁺]éq/C ≈ {fr(sTAU, 2)} < 1 : réaction limitée", f"tau égale {dfr(sTAU, 2)}")],
     f"tau égale la concentration des ions H trois O plus، sur C. tau égale {dfr(sTAU, 2)}، صغير من un: la réaction محدودة."),
  QS("5", "Montrer que K = C·τ²/(1 − τ) et calculer K.",
     val("K", sK, None, f"K = 4,0 × 10⁻³ × {fr(sTAU, 3)}²/(1 − {fr(sTAU, 3)}) = {sci(sK, 1)}", tol=0.05),
     (["C·τ", "C(1 − τ)"], ["K = C·τ"]),
     [("K = C·τ²/(1 − τ)", "C fois tau au carré"), (f"K = {sci(sK, 1)}", f"{dsci(sK, 1)}")],
     f"K égale C fois tau au carré، sur un moins tau، يعني {dsci(sK, 1)}."),
  QS("6", "On dilue quatre fois (C' = 1,0 × 10⁻³ mol/L) ; G' = 0,695 mS. Calculer τ' ; effet de la dilution sur τ et K ?",
     val("τ'", sTAUd, None, f"σ' = {sci(sSIGd, 2)} S·m⁻¹ ; [H₃O⁺]' = {sci(sHd, 2)} mol/L ; τ' ≈ {fr(sTAUd, 2)} > τ ; K inchangée", tol=0.05),
     (["σ = G/k", "τ = [H₃O⁺]/C"], ["K diminue"]),
     [(f"τ' ≈ {fr(sTAUd, 2)} > τ", f"tau prime égale {dfr(sTAUd, 2)}"), ("K ne change pas", "K ما كتبدلش")],
     f"sigma prime égale G prime sur k، و la concentration {dsci(sHd, 2)} mole par litre. tau prime égale {dfr(sTAUd, 2)}، كبر من tau. و K ما كتبدلش."),
]

EX = exercice(
  "phys_ex_ch12_etat_equilibre_4", "phys_ch12_etat_equilibre", "etat_equilibre",
  "L'acide méthanoïque au conductimètre : τ, K et la dilution", "moyen", 30,
  ["Établir σ = (λ₁ + λ₂)·[H₃O⁺]éq", "Utiliser G = k·σ", "Convertir mol·m⁻³ en mol/L", "Calculer τ et K", "Prévoir l'effet de la dilution"],
  "On prépare une solution S d'acide méthanoïque HCOOH de concentration C = 2,0 × 10⁻³ mol/L. À 25 °C, on plonge dans S la cellule d'un conductimètre, de constante k = 5,0 × 10⁻² m : la conductance mesurée est G = 1,05 mS. La réaction de l'acide avec l'eau est rapide : la mesure est faite à l'équilibre. On néglige la contribution des ions HO⁻.",
  "دابا نقراو l'énoncé. solution S ديال l'acide méthanoïque، C égale deux virgule zéro fois dix puissance moins trois mole par litre. كندخلو فيها la cellule ديال le conductimètre، la constante ديالها k égale cinq virgule zéro fois dix puissance moins deux mètre. la conductance اللي قسنا: G égale un virgule zéro cinq millisiemens. la réaction سريعة: la mesure à l'équilibre. و les ions hydroxyde كنهملوهم.",
  [], ["C = 2,0 × 10⁻³ mol/L ; G = 1,05 mS ; k = 5,0 × 10⁻² m (G = k·σ)",
       "λ₁ = λ(H₃O⁺) = 35,0 × 10⁻³ S·m²·mol⁻¹ ; λ₂ = λ(HCOO⁻) = 5,46 × 10⁻³ S·m²·mol⁻¹",
       "Question 6 : C' = 5,0 × 10⁻⁴ mol/L ; G' = 0,452 mS"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Solution d'acide méthanoïque de concentration C = 4,0 × 10⁻³ mol/L ; même cellule (k = 5,0 × 10⁻² m) : G = 1,54 mS à 25 °C. Mêmes λ.",
  "نفس التمرين، بقيم أخرى: C égale quatre virgule zéro fois dix puissance moins trois mole par litre، و G égale un virgule cinquante-quatre millisiemens.",
  [], ["C = 4,0 × 10⁻³ mol/L ; G = 1,54 mS ; k = 5,0 × 10⁻² m", "λ₁ = 35,0 × 10⁻³ ; λ₂ = 5,46 × 10⁻³ S·m²·mol⁻¹",
       "Question 6 : C' = 1,0 × 10⁻³ mol/L ; G' = 0,695 mS"],
  SIM_Q)

ecrire(EX)
