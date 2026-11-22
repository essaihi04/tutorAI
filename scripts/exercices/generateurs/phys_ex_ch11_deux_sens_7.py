# Exercice de chimie, ch. 11 (transformations dans les deux sens), niveau supérieur (au-dessus du national, même
# forme) : un vinaigre de laboratoire préparé à partir d'acide éthanoïque pur ; C par la masse volumique, vérifiée
# par un titrage, τ avant et après une dilution par 10, puis la démonstration « pH′ − pH = 1 − log(τ′/τ) » et la
# lecture critique d'une prévision fausse (« le pH augmente d'une unité »). Trois notions du chapitre combinées.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2021 R (Q9 « montrer que τ = 10^(−pH)/C », Q10-11 dilution et τ), 2025 N
#    (1.2-1.3 C par titrage puis C₀ de la solution mère), 2022 N (2.3-2.4 C_a par dosage, dilution par 10),
#    2024 R (2.3-2.4 τ d'une réaction de dosage) — backend/data/exams/physique ;
#  - profs (sources_chimie_ch9_ch11.md, chapitre C : Sbiro, 1 cm³ d'acide pur dans 500 cm³, n₀ par la densité,
#    pH ≈ 3,1, τ ≈ 2,3 % ; dilution chez Sbiro au chapitre suivant) ; titrage et équivalence vus au ch. 10 ;
#    pièges : m = ρ·V oublié, croire que diluer 10 fois augmente le pH de 1 pour un acide faible ;
#  - séries en ligne : talamidi (deux sens, non corrigés 1), alloschool (séance 8 El Goufifa ; « taux d'avancement
#    et conductimétrie corrigé »), moutamadris (cours deux sens 2022), kezakoo (exercices transformation),
#    coursdusoirpc (TD 2 BAC BIOF).
# Ici : nos volumes, notre titrage, nos pH (calculés pour pKa ≈ 4,76, arrondis comme des mesures).
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *
from _ch11 import *

RHO, M = 1.05, 60.0                       # g/mL ; g/mol
VP, V = 0.60, 0.500                       # mL d'acide pur ; L de solution
N0 = RHO * VP / M; C = N0 / V             # 1,05e-2 mol ; 2,1e-2 mol/L
VA, CB, VBE = 20.0, 2.0e-2, 21.0          # mL ; mol/L ; mL
CA = CB * VBE / VA
PH, PH2 = 3.23, 3.74
C2 = C / 10
TAU, TAU2 = 10 ** -PH / C, 10 ** -PH2 / C2
DPH = 1 - math.log10(TAU2 / TAU)
assert abs(C - 2.1e-2) < 1e-12 and abs(CA - C) < 1e-12
assert abs(TAU - 0.0280) < 1e-4 and abs(TAU2 - 0.0867) < 1e-4 and abs(DPH - (PH2 - PH)) < 1e-9 and abs(DPH - 0.51) < 1e-9

sVP = 0.50
sN0 = RHO * sVP / M; sC = sN0 / V; sVBE = sC * VA / CB
sPH, sPH2 = 3.27, 3.78
sTAU, sTAU2 = 10 ** -sPH / sC, 10 ** -sPH2 / (sC / 10)
sDPH = 1 - math.log10(sTAU2 / sTAU)
assert abs(sC - 1.75e-2) < 1e-12 and abs(sVBE - 17.5) < 1e-9 and abs(sDPH - 0.51) < 1e-9

EQD = "CH₃COOH(aq) + HO⁻(aq) → CH₃COO⁻(aq) + H₂O(l)"
EQD_DIT = "l'acide éthanoïque، plus H O moins، donne l'ion éthanoate، plus H deux O"


def sl_mesures(sid, titre, app, centre, depart=False):
    url = T + "dilution.html?vue=mesures" + ("&depart=solution_2" if depart else "")
    if not depart:
        txt = "le bécher اللول: l'acide éthanoïque، zéro virgule zéro un mole par litre، و le p H égale trois virgule quatre. دابا نديرو la dilution: dix millilitres ف une fiole de cent millilitres. المحلول ولا dilué dix fois. le bécher الثاني: le p H égale trois virgule neuf. le p H طلع غير ب zéro virgule cinq. فالتمرين ديالنا: "
        pts = [("le bécher اللول", "moment:solution_1"), ("دابا نديرو la dilution", "moment:dilution_1"), ("le bécher الثاني", "moment:solution_2")]
    else:
        txt = "عندنا deux béchers: trois virgule quatre، و trois virgule neuf. نعاودو نفس الشي: le bécher الثالث، un virgule zéro fois dix puissance moins quatre mole par litre، و le p H égale quatre virgule cinq. كل مرة la concentration كتتقسم على dix، و le p H كيطلع، ولكن ماشي ب un. فالتمرين ديالنا: "
        pts = [("عندنا deux béchers", "moment:solution_2"), ("نعاودو نفس الشي", "moment:dilution_2"), ("le bécher الثالث", "moment:solution_3"), ("كل مرة la concentration", "moment:tableau")]
    return sim(sid, titre, "Diluer 10 fois un acide faible : le pH monte de moins d'une unité.", url, "Dilutions et pH-mètre", txt + app, centre, pts)


QUESTIONS = [
  Q("1", f"On verse un volume V_p = {fr(VP, 2)} mL d'acide éthanoïque pur dans une fiole jaugée de {fr(V * 1000, 0)} mL, que l'on complète avec de l'eau distillée. Calculer la concentration C de la solution S obtenue.",
    f"السؤال un: كنحطو {d(VP, 2)} millilitre ديال l'acide éthanoïque pur ف une fiole jaugée ديال {d(V * 1000, 0)} millilitres، وكنكملو بالما. حسب la concentration C ديال S.",
    val("C", C, "mol/L", f"n₀ = ρ·V_p/M = {fr(RHO, 2)} × {fr(VP, 2)}/{fr(M, 0)} = {sci(N0, 2)} mol ; C = n₀/V = {sci(N0, 2)}/{fr(V, 3)} = {sci(C, 1)} mol/L"),
    (["m = ρ·V", "n = m/M", "C = n/V", "g/mL"], ["C = ρ/M", "n = V_p/M"]),
    [("Le liquide pur se mesure en volume : de son volume, passe à sa masse avec la masse volumique, puis à sa quantité de matière.",
      "l'acide pur كنقيسوه ب le volume. من le volume، دوز ل la masse ب la masse volumique، ومن بعد ل la quantité de matière."),
     ("m = ρ·V_p, n₀ = m/M, puis C = n₀/V (V = 500 mL = 0,500 L).",
      "m égale rho fois V p، n zéro égale m sur M، ومن بعد C égale n zéro sur V، و V ب litre.")],
    [(f"1 : m = ρ·V_p = {fr(RHO, 2)} × {fr(VP, 2)} = {fr(RHO * VP, 2)} g", "m égale rho fois V p"),
     (f"n₀ = m/M = {fr(RHO * VP, 2)}/{fr(M, 0)} = {sci(N0, 2)} mol", "n zéro égale m sur M"),
     (f"C = n₀/V = {sci(C, 1)} mol/L", f"C égale {ds(C, 1)} mole par litre")],
    f"السؤال un. m égale rho fois V p، يعني {d(RHO, 2)} fois {d(VP, 2)}، égale {d(RHO * VP, 2)} gramme. n zéro égale m sur M، يعني {ds(N0, 2)} mole. C égale n zéro sur V، يعني C égale {ds(C, 1)} mole par litre.",
    "ex_1", "fa_1"),
  Q("2", f"Pour vérifier C, on titre V_A = {fr(VA, 1)} mL de S par une solution d'hydroxyde de sodium de concentration C_B = {sci(CB, 1)} mol/L ; l'équivalence est obtenue pour V_BE = {fr(VBE, 1)} mL. Écrire l'équation de la réaction du titrage (totale) et calculer la concentration C_A trouvée. Conclure.",
    f"السؤال deux: باش نتأكدو من C، كنعايرو {d(VA, 1)} millilitres ديال S ب la soude، C B égale {ds(CB, 1)} mole par litre، و l'équivalence ف V B E égale {d(VBE, 1)} millilitres. كتب l'équation، وحسب C A. استنتج.",
    val("C_A", CA, "mol/L", f"{EQD} ; à l'équivalence C_A·V_A = C_B·V_BE donc C_A = {sci(CB, 1)} × {fr(VBE, 1)}/{fr(VA, 1)} = {sci(CA, 1)} mol/L"),
    (["C_A·V_A = C_B·V_BE", "HO⁻", "→"], ["C_A = C_B·V_A/V_BE", "⇌"]),
    [("À l'équivalence, les réactifs du titrage sont dans les proportions de l'équation : ici, une mole de HO⁻ pour une mole d'acide.",
      "ف l'équivalence، les réactifs فالنسب ديال l'équation: هنا un H O moins لكل acide."),
     ("n(acide) = n(HO⁻) versé : C_A·V_A = C_B·V_BE.", "C A fois V A égale C B fois V B E.")],
    [(f"2 : {EQD}", "l'équation"),
     ("à l'équivalence : C_A·V_A = C_B·V_BE", "C A fois V A égale C B fois V B E"),
     (f"C_A = C_B·V_BE/V_A = {sci(CB, 1)} × {fr(VBE, 1)}/{fr(VA, 1)} = {sci(CA, 1)} mol/L = C : la préparation est vérifiée", "نفس C")],
    f"السؤال deux. l'équation: {EQD_DIT}. ف l'équivalence: C A fois V A égale C B fois V B E. إذن C A égale C B fois V B E، sur V A، يعني {ds(CA, 1)} mole par litre: نفس C، إذن la préparation صحيحة.",
    "ex_2", "fa_2"),
  Q("3", f"Le pH de S vaut {fr(PH)} à 25 °C. Calculer le taux d'avancement final τ de la réaction de l'acide éthanoïque avec l'eau (on admet τ = 10^(−pH)/C).",
    f"السؤال trois: le p H ديال S égale {d(PH)}. حسب tau ديال la réaction ديال l'acide éthanoïque مع الما.",
    val("τ", TAU, None, f"τ = 10^(−{fr(PH)})/{sci(C, 1)} = {fr(TAU, 4)}"),
    (["τ = 10^(−pH)/C"], ["τ = 10^(pH)/C", "τ = 10^(−pH)·C"]),
    [("Remplace le pH mesuré et la concentration C dans la relation.", "عوض le p H و C فla relation."),
     ("τ = 10^(−pH)/C ; le résultat est petit devant 1.", "tau égale dix puissance moins p H، sur C.")],
    [(f"3 : τ = 10^(−{fr(PH)})/{sci(C, 1)}", f"dix puissance moins {d(PH)}"),
     (f"τ = {fr(TAU, 4)} < 1 : réaction limitée", f"tau égale {d(TAU, 3)}")],
    f"السؤال trois. tau égale dix puissance moins {d(PH)}، sur {ds(C, 1)}. tau égale {d(TAU, 3)}، صغر من un: la réaction limitée.",
    "ex_3", "fa_3"),
  Q("4", f"On dilue S dix fois ; la solution S′ obtenue (C′ = C/10) a un pH = {fr(PH2)}. Calculer τ′.",
    f"السؤال quatre: كنزيدو الما ل S، dilué dix fois. le p H ديال S prime égale {d(PH2)}. حسب tau prime.",
    val("τ′", TAU2, None, f"τ′ = 10^(−{fr(PH2)})/{sci(C2, 1)} = {fr(TAU2, 4)}"),
    (["τ′ = 10^(−pH′)/C′", "C′ = C/10"], ["C′ = 10·C", "τ′ = τ/10"]),
    [("La concentration de S′ est dix fois plus petite : C′ = C/10.", "la concentration ديال S prime صغر ب dix fois: C sur dix."),
     ("τ′ = 10^(−pH′)/C′ : compare à τ.", "tau prime égale dix puissance moins p H prime، sur C prime. قارن مع tau.")],
    [(f"4 : C′ = C/10 = {sci(C2, 1)} mol/L", "C prime égale C sur dix"),
     (f"τ′ = 10^(−{fr(PH2)})/{sci(C2, 1)} = {fr(TAU2, 4)}", f"tau prime égale {d(TAU2, 3)}"),
     ("τ′ > τ : la dilution augmente le taux d'avancement final", "كبر من tau")],
    f"السؤال quatre. C prime égale C sur dix، يعني {ds(C2, 1)} mole par litre. tau prime égale dix puissance moins {d(PH2)}، sur {ds(C2, 1)}. tau prime égale {d(TAU2, 3)}، كبر من tau: la dilution كتزيد tau.",
    "ex_4", "fa_4"),
  Q("5", "Montrer que pH′ − pH = 1 − log(τ′/τ), puis calculer pH′ − pH avec les valeurs de τ et τ′.",
    "السؤال cinq: بين أن p H prime moins p H égale un moins log de tau prime sur tau. ومن بعد حسبها.",
    val("pH′ − pH", DPH, None, f"[H₃O⁺] = τ·C donc pH = −log(τ·C) ; pH′ − pH = log(C/C′) − log(τ′/τ) = 1 − log(τ′/τ) = 1 − log({fr(TAU2, 4)}/{fr(TAU, 4)}) = {fr(DPH, 2)}", tol=0.04),
    (["[H₃O⁺] = τ·C", "log(a·b) = log a + log b", "log 10 = 1"], ["pH′ − pH = 1", "pH = −log τ"]),
    [("De τ = 10^(−pH)/C, tire [H₃O⁺] = τ·C, puis écris pH = −log(τ·C) pour S et pour S′.",
      "من tau égale dix puissance moins p H، sur C، كنلقاو la concentration des ions H trois O plus égale tau fois C. ومن بعد p H égale moins log de tau fois C، ل S و ل S prime."),
     ("Fais la différence ; log(τ·C) = log τ + log C, et C/C′ = 10 donne log 10 = 1.",
      "دير الفرق. log ديال tau fois C égale log tau plus log C. و C sur C prime égale dix، و log de dix égale un.")],
    [("5 : [H₃O⁺] = τ·C donc pH = −log τ − log C", "p H égale moins log tau moins log C"),
     ("pH′ − pH = log(C/C′) − log(τ′/τ) = 1 − log(τ′/τ)", "un moins log de tau prime sur tau"),
     (f"pH′ − pH = 1 − log({fr(TAU2, 4)}/{fr(TAU, 4)}) = {fr(DPH, 2)}", f"égale {d(DPH, 2)}")],
    f"السؤال cinq. la concentration des ions H trois O plus égale tau fois C، إذن p H égale moins log tau moins log C. الفرق: p H prime moins p H égale log de C sur C prime، moins log de tau prime sur tau. و C sur C prime égale dix، log de dix égale un. إذن p H prime moins p H égale un moins log de tau prime sur tau. l'application numérique: égale {d(DPH, 2)}، وهو بالضبط {d(PH2)} moins {d(PH)}.",
    "ex_5", "fa_5"),
  Q("6", "Avant la mesure, un élève avait prévu : « en diluant dix fois, [H₃O⁺] est divisée par 10, donc le pH augmentera d'une unité ». Critiquer cette prévision.",
    "السؤال six: قبل القياس، تلميذ قال: « ملي نديرو dilué dix fois، la concentration des ions H trois O plus كتتقسم على dix، إذن le p H غادي يطلع ب un ». ناقش هاد التوقع.",
    phrase(f"Fausse pour un acide dont la réaction avec l'eau est limitée : la dilution augmente τ (τ′ > τ), donc [H₃O⁺] = τ·C est divisée par moins de 10 et le pH augmente de moins d'une unité ({fr(DPH, 2)}) ; elle serait juste pour une réaction totale (τ = 1 constant)"),
    (["τ′ > τ", "[H₃O⁺] = τ·C", "log(τ′/τ) > 0", "réaction totale"], ["le pH diminue", "pH′ − pH = 1"]),
    [("Dans pH′ − pH = 1 − log(τ′/τ), que vaut le terme log(τ′/τ) si τ ne change pas ? Et ici ?",
      "ف p H prime moins p H égale un moins log de tau prime sur tau: شحال كيسوى log يلا tau ما تبدلش؟ وهنا؟"),
     ("Ici τ′ > τ : une plus grande part de l'acide réagit, ce qui compense en partie la dilution.",
      "هنا tau prime كبر من tau: جزء كبر من l'acide كيتفاعل، وهادشي كيعوض شوية la dilution.")],
    [("6 : la prévision suppose τ constant (réaction totale)", "tau ما كيتبدلش"),
     ("ici la réaction est limitée et la dilution augmente τ : τ′ > τ, log(τ′/τ) > 0", "tau prime كبر من tau"),
     (f"[H₃O⁺] = τ·C est divisée par moins de 10 : le pH augmente de {fr(DPH, 2)} < 1 ; la prévision est fausse", "أقل من un")],
    f"السؤال six. التلميذ فرض أن tau ما كيتبدلش، وهادا صحيح غير يلا كانت la réaction totale. هنا la réaction limitée، و la dilution كتزيد tau: tau prime كبر من tau، و log de tau prime sur tau موجب. إذن la concentration des ions H trois O plus كتتقسم ب أقل من un dix، و le p H كيطلع ب {d(DPH, 2)}، أقل من un. التوقع غالط.",
    "ex_6", "fa_6"),
]

EXPLICATIONS = [
  sl_concentration("ex_1", "Question 1 : du volume d'acide pur à C",
    f"l'acide pur liquide: m égale rho fois V p، يعني {d(RHO * VP, 2)} gramme. n zéro égale m sur M، يعني {ds(N0, 2)} mole. و C égale n zéro sur V، يعني {ds(C, 1)} mole par litre.",
    [("m = ρ·V_p ; n₀ = m/M ; C = n₀/V", "l'acide pur liquide"), (f"C = {sci(C, 1)} mol/L", f"يعني {ds(C, 1)} mole par litre")]),
  sl_titrage("ex_2", "Question 2 : vérifier C par un titrage",
    f"l'équation: {EQD_DIT}. ف l'équivalence، C A fois V A égale C B fois V B E، إذن C A égale {ds(CA, 1)} mole par litre: نفس C.",
    [(EQD, "l'équation: l'acide éthanoïque"), (f"C_A = C_B·V_BE/V_A = {sci(CA, 1)} mol/L", f"إذن C A égale {ds(CA, 1)} mole par litre")]),
  sl_taux("ex_3", "Question 3 : τ de la solution S",
    f"tau égale dix puissance moins {d(PH)}، sur {ds(C, 1)}، يعني {d(TAU, 3)}. صغر من un: limitée.",
    [(f"τ = {fr(TAU, 4)}", f"يعني {d(TAU, 3)}")]),
  sl_diluer("ex_4", "Question 4 : τ′ après la dilution",
    f"tau prime égale dix puissance moins {d(PH2)}، sur {ds(C2, 1)}، يعني {d(TAU2, 3)}، كبر من {d(TAU, 3)}.",
    [(f"τ′ = {fr(TAU2, 4)} > τ = {fr(TAU, 4)}", f"يعني {d(TAU2, 3)}")]),
  sl_mesures("ex_5", "Question 5 : pH′ − pH = 1 − log(τ′/τ)",
    f"p H égale moins log de tau fois C. الفرق كيعطي un moins log de tau prime sur tau، يعني {d(DPH, 2)}، أقل من un.",
    [("pH′ − pH = 1 − log(τ′/τ)", "الفرق كيعطي"), (f"pH′ − pH = {fr(DPH, 2)}", f"يعني {d(DPH, 2)}")]),
  sl_mesures("ex_6", "Question 6 : pourquoi pas une unité",
    f"tau كبر مع la dilution، إذن la concentration des ions H trois O plus ما كتتقسمش على dix كاملة، و le p H كيطلع ب {d(DPH, 2)} فقط.",
    [("τ′ > τ : pH′ − pH < 1", "tau كبر مع la dilution")], depart=True),
]

FACILES = [
  qcm("fa_1", "Plus facile : la masse d'acide pur", "سؤال ساهل: شحال la masse ديال l'acide؟",
      f"V_p = {fr(VP, 2)} mL d'acide pur, ρ = {fr(RHO, 2)} g/mL. Sa masse vaut…",
      [f"{fr(VP / RHO, 2)} g", f"{fr(RHO * VP, 2)} g", f"{fr(RHO * VP * M, 1)} g"], 1, {
        1: ("juste", f"برافو! m égale rho fois V، يعني {d(RHO * VP, 2)} gramme.", f"Juste : m = ρ·V = {fr(RHO * VP, 2)} g."),
        0: (("لا، قسمتي V على rho. la masse هي rho fois V. عاود اختار.", "On multiplie : m = ρ·V. Réessaie."),
            (f"الجواب: {d(RHO * VP, 2)} gramme.", f"Réponse : m = ρ·V = {fr(RHO * VP, 2)} g.")),
        2: (("لا، M ما كتدخلش هنا: M كتعطي n من m. عاود اختار.", "M ne sert pas à trouver la masse. Réessaie."),
            (f"الجواب: {d(RHO * VP, 2)} gramme، m égale rho fois V.", f"Réponse : {fr(RHO * VP, 2)} g."))},
      f"V p égale {d(VP, 2)} millilitre d'acide pur, rho égale {d(RHO, 2)} gramme par millilitre. Sa masse vaut ?"),
  qcm("fa_2", "Plus facile : la relation à l'équivalence", "سؤال ساهل على l'équivalence.",
      "AH + HO⁻ → A⁻ + H₂O. À l'équivalence…",
      ["C_A·V_BE = C_B·V_A", "C_A + V_A = C_B + V_BE", "C_A·V_A = C_B·V_BE"], 2, {
        2: ("juste", "برافو! la quantité d'acide égale la quantité d'ions H O moins versés.", "Juste : n(AH) = n(HO⁻) versés."),
        0: (("لا، خلطتي les volumes. كل concentration مع le volume ديالها. عاود اختار.", "Chaque concentration va avec son propre volume. Réessaie."),
            ("الجواب: C A fois V A égale C B fois V B E.", "Réponse : C_A·V_A = C_B·V_BE.")),
        1: (("لا، ما كنجمعوش concentration و volume. n égale C fois V. عاود اختار.", "On n'additionne pas : n = C·V. Réessaie."),
            ("الجواب: C A fois V A égale C B fois V B E.", "Réponse : C_A·V_A = C_B·V_BE."))},
      "A H plus H O moins donne A moins plus H deux O. À l'équivalence ?"),
  vf("fa_3", "Plus facile : vrai ou faux", f"pH = {fr(PH)}, C = {sci(C, 1)} mol/L.", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [(f"τ = 10^(−{fr(PH)})/{sci(C, 1)} ≈ {fr(TAU, 3)}.", True, "Application directe de τ = 10^(−pH)/C."),
      ("τ < 1 : la réaction de l'acide éthanoïque avec l'eau est totale.", False, "τ < 1 signifie limitée."),
      ("La réaction de titrage, elle, est totale.", True, "On écrit une flèche simple pour un titrage.")]),
  qcm("fa_4", "Plus facile : τ′", "سؤال ساهل على tau prime.",
      f"S′ : C′ = {sci(C2, 1)} mol/L, pH′ = {fr(PH2)}. τ′ vaut environ…",
      [f"{fr(TAU / 10, 4)}", f"{fr(TAU2, 3)}", f"{fr(TAU, 3)}"], 1, {
        1: ("juste", f"برافو! tau prime égale {d(TAU2, 3)}، كبر من tau.", f"Juste : τ′ = {fr(TAU2, 3)}."),
        0: (("لا، tau ما كيتقسمش على dix مع C. حسب ب p H prime. عاود اختار.", "τ n'est pas divisé par 10 : calcule avec pH′. Réessaie."),
            (f"الجواب: {d(TAU2, 3)}.", f"Réponse : τ′ = 10^(−{fr(PH2)})/{sci(C2, 1)} = {fr(TAU2, 3)}.")),
        2: (("هادي tau ديال S، ماشي ديال S prime. عاود اختار.", "C'est τ de S, pas de S′. Réessaie."),
            (f"الجواب: {d(TAU2, 3)}.", f"Réponse : τ′ = {fr(TAU2, 3)}."))},
      f"C prime égale {ds(C2, 1)} mole par litre, p H prime égale {d(PH2)}. Tau prime vaut environ ?"),
  vf("fa_5", "Plus facile : les étapes", "pH′ − pH = 1 − log(τ′/τ)", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("[H₃O⁺] = τ·C.", True, "C'est τ = [H₃O⁺]/C retournée."),
      ("log(τ·C) = log τ × log C.", False, "Le log d'un produit est une somme : log τ + log C."),
      ("log(C/C′) = log 10 = 1.", True, "C′ = C/10.")]),
  assoc("fa_6", "Plus facile : de combien monte le pH ?", "Relie chaque cas à la hausse du pH quand on dilue 10 fois.",
    "سؤال ساهل: ربط كل حالة مع شحال كيطلع le p H ملي dilué dix fois.",
    "Dilution par 10 : relie chaque cas à la hausse du pH.",
    [("1", "Réaction totale avec l'eau (τ = 1 avant et après)"), ("2", "Réaction limitée (τ augmente)")],
    [("a", "le pH augmente d'une unité"), ("b", "le pH augmente de moins d'une unité"), ("c", "le pH diminue")],
    {"1": "a", "2": "b"},
    {"1-a": (True, "Oui : τ constant, [H₃O⁺] = C est divisée par 10.", "برافو: tau ما تبدلش، la concentration كتتقسم على dix."),
     "1-b": (False, "Si τ ne change pas, log(τ′/τ) = 0.", "لا، يلا tau ما تبدلش، log de tau prime sur tau égale zéro."),
     "2-a": (False, "τ augmente : [H₃O⁺] est divisée par moins de 10.", "لا، tau كيطلع: la concentration كتتقسم ب أقل من dix."),
     "2-b": (True, "Oui : τ′ > τ compense en partie la dilution.", "برافو: tau prime كبر، كيعوض شوية la dilution."),
     "1-c": (False, "En diluant un acide, [H₃O⁺] diminue : le pH ne peut pas baisser.", "لا، ملي كنزيدو الما، le p H ما يمكنش ينقص."),
     "2-c": (False, "En diluant un acide, [H₃O⁺] diminue : le pH ne peut pas baisser.", "لا، ملي كنزيدو الما، le p H ما يمكنش ينقص.")},
    ("(1 ; a) (2 ; b) : pour une réaction limitée, le pH monte de moins d'une unité.", "la réaction limitée: le p H كيطلع ب أقل من un.")),
]

SIM_Q = [
  QS("1", f"V_p = {fr(sVP, 2)} mL d'acide éthanoïque pur dans une fiole de {fr(V * 1000, 0)} mL. Calculer C.",
     val("C", sC, "mol/L", f"n₀ = ρ·V_p/M = {sci(sN0, 3)} mol ; C = n₀/V = {sci(sC, 2)} mol/L"),
     (["m = ρ·V", "n = m/M"], ["C = ρ/M"]),
     [(f"C = ρ·V_p/(M·V) = {sci(sC, 2)} mol/L", f"{ds(sC, 2)} mole par litre")],
     f"m égale rho fois V p، n zéro égale m sur M، و C égale n zéro sur V، يعني {ds(sC, 2)} mole par litre."),
  QS("2", f"Titrage : V_A = {fr(VA, 1)} mL, C_B = {sci(CB, 1)} mol/L, V_BE = {fr(sVBE, 1)} mL. Équation et C_A.",
     val("C_A", sC, "mol/L", f"C_A = C_B·V_BE/V_A = {sci(CB, 1)} × {fr(sVBE, 1)}/{fr(VA, 1)} = {sci(sC, 2)} mol/L"),
     (["C_A·V_A = C_B·V_BE"], ["C_A = C_B·V_A/V_BE"]),
     [(f"{EQD} ; C_A = {sci(sC, 2)} mol/L = C", "C A fois V A égale C B fois V B E")],
     f"{EQD_DIT}. C A fois V A égale C B fois V B E، إذن C A égale {ds(sC, 2)} mole par litre."),
  QS("3", f"pH = {fr(sPH)}. Calculer τ.",
     val("τ", sTAU, None, f"τ = 10^(−{fr(sPH)})/{sci(sC, 2)} = {fr(sTAU, 4)}"),
     (["τ = 10^(−pH)/C"], ["τ = 10^(pH)/C"]),
     [(f"τ = {fr(sTAU, 4)}", f"tau égale {d(sTAU, 3)}")], f"tau égale {d(sTAU, 3)}."),
  QS("4", f"Après dilution par 10, pH′ = {fr(sPH2)}. Calculer τ′.",
     val("τ′", sTAU2, None, f"τ′ = 10^(−{fr(sPH2)})/{sci(sC / 10, 2)} = {fr(sTAU2, 4)}"),
     (["C′ = C/10"], ["τ′ = τ/10"]),
     [(f"τ′ = {fr(sTAU2, 4)}", f"tau prime égale {d(sTAU2, 3)}")], f"tau prime égale {d(sTAU2, 3)}."),
  QS("5", "Montrer que pH′ − pH = 1 − log(τ′/τ) et calculer pH′ − pH.",
     val("pH′ − pH", sDPH, None, f"pH′ − pH = 1 − log({fr(sTAU2, 4)}/{fr(sTAU, 4)}) = {fr(sDPH, 2)}", tol=0.04),
     (["[H₃O⁺] = τ·C"], ["pH′ − pH = 1"]),
     [(f"pH′ − pH = 1 − log(τ′/τ) = {fr(sDPH, 2)}", f"égale {d(sDPH, 2)}")],
     f"p H égale moins log tau moins log C، إذن p H prime moins p H égale un moins log de tau prime sur tau، égale {d(sDPH, 2)}."),
  QS("6", "« Le pH augmentera d'une unité » : critiquer.",
     phrase("Fausse : τ augmente à la dilution (réaction limitée), le pH augmente de moins d'une unité"),
     (["τ′ > τ"], ["pH′ − pH = 1"]),
     [("τ′ > τ : le pH augmente de moins d'une unité", "أقل من un")],
     "غالط: la réaction limitée، tau كيطلع مع la dilution، و le p H كيطلع ب أقل من un."),
]

EX = exercice(
  "phys_ex_ch11_deux_sens_7", "phys_ch11_transformations_deux_sens", "transformations_deux_sens",
  "Un vinaigre de laboratoire : C, titrage, dilution et lecture critique du pH", "difficile", 35,
  ["Calculer C à partir d'un volume d'acide pur (m = ρ·V)", "Vérifier C par un titrage (C_A·V_A = C_B·V_BE)",
   "Calculer τ avant et après une dilution", "Montrer que pH′ − pH = 1 − log(τ′/τ)", "Critiquer une prévision à l'aide de τ"],
  f"Un technicien prépare un « vinaigre de laboratoire » : il verse V_p = {fr(VP, 2)} mL d'acide éthanoïque pur CH₃COOH dans une fiole jaugée de {fr(V * 1000, 0)} mL et complète avec de l'eau distillée : solution S. Il vérifie sa concentration par un titrage, mesure le pH de S, puis dilue S dix fois (solution S′) et mesure de nouveau le pH. Équation de la réaction de l'acide avec l'eau : CH₃COOH(aq) + H₂O(l) ⇌ CH₃COO⁻(aq) + H₃O⁺(aq).",
  f"دابا نقراو l'énoncé. technicien كيحط {d(VP, 2)} millilitre ديال l'acide éthanoïque pur ف une fiole jaugée ديال {d(V * 1000, 0)} millilitres، وكيكمل بالما: هادا هو المحلول S. كيتأكد من la concentration ب un titrage، كيقيس le p H، ومن بعد كيدير dilué dix fois، وكيعاود يقيس le p H.",
  [tableau_texte("Mesures à 25 °C", ["Solution", "C (mol/L)", "pH"], [["S", sci(C, 1), fr(PH)], ["S′ (S diluée 10 fois)", sci(C2, 1), fr(PH2)]])],
  [f"Acide éthanoïque pur : ρ = {fr(RHO, 2)} g/mL ; M = {fr(M, 0)} g/mol", f"Titrage : V_A = {fr(VA, 1)} mL ; C_B = {sci(CB, 1)} mol/L ; V_BE = {fr(VBE, 1)} mL",
   f"pH(S) = {fr(PH)} ; pH(S′) = {fr(PH2)} (25 °C)", "log(a·b) = log a + log b ; log 10 = 1"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  f"On verse V_p = {fr(sVP, 2)} mL d'acide éthanoïque pur dans une fiole de {fr(V * 1000, 0)} mL complétée à l'eau (solution S). Titrage de {fr(VA, 1)} mL de S par la soude à {sci(CB, 1)} mol/L : V_BE = {fr(sVBE, 1)} mL. pH(S) = {fr(sPH)} ; après dilution par 10, pH(S′) = {fr(sPH2)}.",
  f"نفس التمرين، بقيم أخرى. {d(sVP, 2)} millilitre ديال l'acide pur، V B E égale {d(sVBE, 1)} millilitres، p H ديال S {d(sPH)}، و ديال S prime {d(sPH2)}.",
  [], [f"ρ = {fr(RHO, 2)} g/mL ; M = {fr(M, 0)} g/mol", f"V_A = {fr(VA, 1)} mL ; C_B = {sci(CB, 1)} mol/L ; V_BE = {fr(sVBE, 1)} mL", f"pH = {fr(sPH)} ; pH′ = {fr(sPH2)}"],
  SIM_Q)

ecrire(EX)
