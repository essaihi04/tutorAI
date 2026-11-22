# Exercice de chimie, ch. 11 (transformations dans les deux sens), niveau facile : τ par la conductimétrie, un geste
# à la fois (les ions qui conduisent, σ = (λ₁ + λ₂)·[H₃O⁺], les unités mS → S et mol/m³ → mol/L, τ).
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2019 N (2.3.1 [H₃O⁺] par σ, 2.3.2 « montrer que τ = σ/(C(λ₁ + λ₂)) »),
#    2016 R et 2018 R (σ et G en cinétique, mêmes unités), 2021 R (τ et dilution) — backend/data/exams/physique ;
#  - profs (sources_chimie_ch9_ch11.md, chapitre C, § 6 : la conductimétrie n'apparaît qu'en exercice, chez Sbiro
#    avec l'acide benzoïque, et en formule chez El Founani) ; piège relevé partout : C en mol/L au lieu de mol/m³,
#    λ en mS au lieu de S ;
#  - séries en ligne : alloschool (« taux d'avancement et conductimétrie corrigé »), kezakoo (exercices
#    transformation), talamidi (deux sens, non corrigés 1 ; état d'équilibre, activités 1), moutamadris (fiche
#    exercices 17-2), labolycee (Centres étrangers 2010, pH et conductimétrie : méthode seulement).
# Ici : l'acide méthanoïque à 5,0 × 10⁻³ mol/L, notre σ (calculée pour pKa ≈ 3,75 puis arrondie comme une mesure).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *
from _ch11 import *

L1, L2 = 35.0, 5.46                 # mS·m²/mol : H₃O⁺, HCOO⁻
C, SIG = 5.0e-3, 34.4               # mol/L ; mS/m
H_M3 = (SIG * 1e-3) / ((L1 + L2) * 1e-3)   # mol/m³
H = H_M3 / 1000                     # mol/L
TAU = H / C
assert abs(H_M3 - 0.850) < 1e-3 and abs(TAU - 0.170) < 1e-3

sC, sSIG = 2.0e-3, 20.8
sH_M3 = sSIG / (L1 + L2); sH = sH_M3 / 1000; sTAU = sH / sC
assert abs(sH_M3 - 0.514) < 1e-3 and abs(sTAU - 0.257) < 1e-3

REL = "σ = λ₁·[H₃O⁺] + λ₂·[HCOO⁻] = (λ₁ + λ₂)·[H₃O⁺]"
REL_DIT = "sigma égale lambda un fois la concentration des ions H trois O plus، plus lambda deux fois la concentration des ions méthanoate، و هوما بجوج عندهم نفس la concentration، إذن sigma égale lambda un plus lambda deux، fois la concentration des ions H trois O plus"

QUESTIONS = [
  Q("1", "Quels ions assurent la conduction de la solution ? Montrer que σ = (λ₁ + λ₂)·[H₃O⁺]_éq (on néglige les ions HO⁻).",
    "السؤال un: شكون هوما les ions اللي كيدوزو le courant؟ بين أن sigma égale lambda un plus lambda deux، fois la concentration des ions H trois O plus.",
    phrase("Ions H₃O⁺ et HCOO⁻ ; " + REL + " car [HCOO⁻]_éq = [H₃O⁺]_éq = x_f/V"),
    (["σ = Σ λᵢ·[Xᵢ]", "[HCOO⁻] = [H₃O⁺]", "x_f/V"], ["HCOOH conduit", "σ = λ₁ + λ₂"]),
    [("Seuls les ions conduisent le courant : quels ions la réaction de l'acide avec l'eau a-t-elle formés ?",
      "غير les ions اللي كيدوزو le courant. شنو هوما les ions اللي تكونو ملي تفاعل l'acide مع الما؟"),
     ("σ = λ₁·[H₃O⁺] + λ₂·[HCOO⁻]. Dans le tableau, les deux produits valent x_f : même concentration x_f/V. Factorise.",
      "sigma égale lambda un fois la concentration des ions H trois O plus، plus lambda deux fois la concentration des ions méthanoate. فle tableau، deux produits عندهم x f، إذن نفس la concentration. جمع.")],
    [("1 : les ions H₃O⁺ et HCOO⁻ conduisent (HO⁻ négligeables)", "les ions H trois O plus و les ions méthanoate"),
     ("σ = λ₁·[H₃O⁺] + λ₂·[HCOO⁻]", "sigma égale lambda un fois"),
     ("[HCOO⁻] = [H₃O⁺] = x_f/V donc σ = (λ₁ + λ₂)·[H₃O⁺]", "إذن sigma égale lambda un plus lambda deux")],
    f"السؤال un. les ions اللي كيدوزو le courant هوما les ions H trois O plus و les ions méthanoate. {REL_DIT}.",
    "ex_1", "fa_1"),
  Q("2", f"La conductivité de la solution vaut σ = {fr(SIG, 1)} mS/m. Calculer [H₃O⁺]_éq en mol·m⁻³.",
    f"السؤال deux: sigma égale {d(SIG, 1)} millisiemens par mètre. حسب la concentration des ions H trois O plus ب mole par mètre cube.",
    val("[H₃O⁺]", H_M3, "mol/m³", f"[H₃O⁺] = σ/(λ₁ + λ₂) = {sci(SIG * 1e-3, 2)} / {sci((L1 + L2) * 1e-3, 3)} = {fr(H_M3, 3)} mol/m³"),
    (["[H₃O⁺] = σ/(λ₁ + λ₂)", "mS = 10⁻³ S", "mol·m⁻³"], ["[H₃O⁺] = σ·(λ₁ + λ₂)", "mol/L"]),
    [("Isole [H₃O⁺] dans la relation de la question 1, puis regarde les unités : σ en S/m et λ en S·m²/mol.",
      "خرج la concentration من la relation ديال السؤال un. ومن بعد شوف الوحدات: sigma ب siemens par mètre، و lambda ب siemens mètre carré par mole."),
     ("[H₃O⁺] = σ/(λ₁ + λ₂), avec 1 mS = 10⁻³ S : le résultat sort en mol/m³.",
      "la concentration égale sigma sur lambda un plus lambda deux. و un millisiemens égale dix puissance moins trois siemens. le résultat كيخرج ب mole par mètre cube.")],
    [("2 : [H₃O⁺] = σ/(λ₁ + λ₂)", "égale sigma sur lambda un plus lambda deux"),
     (f"[H₃O⁺] = {sci(SIG * 1e-3, 2)} / {sci((L1 + L2) * 1e-3, 3)}", f"{ds(SIG * 1e-3, 2)} siemens par mètre"),
     (f"[H₃O⁺] = {fr(H_M3, 3)} mol/m³", f"{d(H_M3, 3)} mole par mètre cube")],
    f"السؤال deux. la concentration égale sigma sur lambda un plus lambda deux. sigma égale {ds(SIG * 1e-3, 2)} siemens par mètre، و lambda un plus lambda deux égale {ds((L1 + L2) * 1e-3, 3)} siemens mètre carré par mole. le résultat: {d(H_M3, 3)} mole par mètre cube.",
    "ex_2", "fa_2"),
  Q("3", "Exprimer cette concentration en mol/L.",
    "السؤال trois: كتب هاد la concentration ب mole par litre.",
    val("[H₃O⁺]", H, "mol/L", f"[H₃O⁺] = {fr(H_M3, 3)} × 10⁻³ = {sci(H, 2)} mol/L"),
    (["1 m³ = 1000 L", "÷ 1000", "mol/L"], ["× 1000", f"{fr(H_M3 * 1000, 0)} mol/L"]),
    [("Un mètre cube contient mille litres : dans un litre, il y a mille fois moins d'ions que dans un mètre cube.",
      "le mètre cube فيه mille litres. إذن ف litre واحد، كاين mille fois قل ديال les ions."),
     ("1 mol/L = 1000 mol/m³ : on divise par 1000.", "une mole par litre égale mille moles par mètre cube. إذن كنقسمو على mille.")],
    [("3 : 1 mol/L = 1000 mol/m³", "une mole par litre égale mille moles par mètre cube"),
     (f"[H₃O⁺] = {fr(H_M3, 3)} / 1000 = {sci(H, 2)} mol/L", f"{ds(H, 2)} mole par litre")],
    f"السؤال trois. une mole par litre égale mille moles par mètre cube. إذن كنقسمو على mille: {ds(H, 2)} mole par litre.",
    "ex_3", "fa_3"),
  Q("4", f"La concentration de l'acide est C = {sci(C, 1)} mol/L. Sachant que τ = [H₃O⁺]_éq/C, calculer τ. La réaction est-elle totale ?",
    f"السؤال quatre: C égale {ds(C, 1)} mole par litre. tau égale la concentration des ions H trois O plus sur C. حسب tau. واش la réaction totale؟",
    val("τ", TAU, None, f"τ = [H₃O⁺]/C = {sci(H, 2)} / {sci(C, 1)} = {fr(TAU, 2)} < 1 : limitée"),
    (["τ = [H₃O⁺]/C", "< 1", "limitée"], ["τ = C/[H₃O⁺]", f"τ = {fr(H_M3, 3)}/{sci(C, 1)}"]),
    [("Les deux concentrations doivent être dans la même unité : prends celle en mol/L.",
      "خاص deux concentrations يكونو بنفس الوحدة: خود اللي ب mole par litre."),
     ("τ = [H₃O⁺]/C ; si τ < 1, la réaction est limitée.", "tau égale la concentration des ions H trois O plus sur C. يلا tau صغر من un، la réaction limitée.")],
    [(f"4 : τ = [H₃O⁺]/C = {sci(H, 2)} / {sci(C, 1)}", "tau égale la concentration"),
     (f"τ = {fr(TAU, 2)}", f"tau égale {d(TAU, 2)}"),
     ("τ < 1 : la réaction n'est pas totale, elle est limitée", "la réaction limitée")],
    f"السؤال quatre. tau égale la concentration des ions H trois O plus sur C، يعني {ds(H, 2)}، sur {ds(C, 1)}. tau égale {d(TAU, 2)}. tau صغر من un، إذن la réaction ماشي totale: la réaction limitée.",
    "ex_4", "fa_4"),
]

EXPLICATIONS = [
  sl_cond_relation("ex_1", "Question 1 : σ = (λ₁ + λ₂)·[H₃O⁺]",
    "l'acide méthanoïque كيعطي les ions H trois O plus و les ions méthanoate. إذن sigma égale lambda un plus lambda deux، fois la concentration des ions H trois O plus.",
    [(REL, "إذن sigma égale lambda un plus lambda deux")]),
  sl_cond_calcul("ex_2", "Question 2 : [H₃O⁺] en mol/m³",
    f"sigma égale {ds(SIG * 1e-3, 2)} siemens par mètre، و lambda un plus lambda deux égale {d(L1 + L2, 2)} millisiemens، يعني {ds((L1 + L2) * 1e-3, 3)} siemens mètre carré par mole. إذن la concentration égale {d(H_M3, 3)} mole par mètre cube.",
    [("[H₃O⁺] = σ/(λ₁ + λ₂)", f"sigma égale {ds(SIG * 1e-3, 2)} siemens"), (f"[H₃O⁺] = {fr(H_M3, 3)} mol/m³", f"إذن la concentration égale {d(H_M3, 3)} mole par mètre cube")]),
  sl_cond_calcul("ex_3", "Question 3 : de mol/m³ à mol/L",
    f"{d(H_M3, 3)} mole par mètre cube، كنقسمو على mille: {ds(H, 2)} mole par litre.",
    [("1 mol/L = 1000 mol/m³", f"{d(H_M3, 3)} mole par mètre cube، كنقسمو"), (f"[H₃O⁺] = {sci(H, 2)} mol/L", f"{ds(H, 2)} mole par litre")]),
  sl_taux("ex_4", "Question 4 : τ et la conclusion",
    f"x f égale la concentration fois V، و x max égale C fois V: V كيتحيد، و tau égale la concentration des ions H trois O plus sur C، يعني {d(TAU, 2)}. tau صغر من un: la réaction limitée.",
    [("τ = [H₃O⁺]/C", "و tau égale la concentration des ions H trois O plus sur C"), (f"τ = {fr(TAU, 2)} < 1 : limitée", f"يعني {d(TAU, 2)}")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : qui conduit le courant ?", "سؤال ساهل: شكون كيدوز le courant فالمحلول؟",
      "Dans la solution d'acide méthanoïque, le courant est transporté par…",
      ["les molécules HCOOH", "les molécules d'eau", "les ions H₃O⁺ et HCOO⁻"], 2, {
        2: ("juste", "برافو! غير les ions اللي كيدوزو le courant: les ions H trois O plus و les ions méthanoate.", "Juste : seuls les ions conduisent, ici H₃O⁺ et HCOO⁻."),
        0: (("ما تقلقش. واش la molécule ديال l'acide عندها charge؟ غير les ions اللي كيدوزو le courant. عاود اختار.", "Une molécule n'a pas de charge : elle ne transporte pas le courant. Réessaie."),
            ("الجواب: les ions H trois O plus و les ions méthanoate. les molécules ما عندهومش charge.", "Réponse : les ions H₃O⁺ et HCOO⁻ ; les molécules ne conduisent pas.")),
        1: (("لا، الما ماشي ion. شنو تكون ملي l'acide عطا le proton؟ عاود اختار.", "L'eau n'est pas un ion. Que forme l'acide en cédant son proton ? Réessaie."),
            ("الجواب: les ions H trois O plus و les ions méthanoate، اللي تكونو فla réaction.", "Réponse : les ions formés par la réaction, H₃O⁺ et HCOO⁻."))},
      "Dans la solution d'acide méthanoïque, le courant est transporté par ?"),
  qcm("fa_2", "Plus facile : les millisiemens", "سؤال ساهل على الوحدات.",
      f"σ = {fr(SIG, 1)} mS/m. En S/m, σ vaut…",
      [f"{fr(SIG * 1000, 0)} S/m", f"{sci(SIG * 1e-3, 2)} S/m", f"{fr(SIG, 1)} S/m"], 1, {
        1: ("juste", f"برافو! un millisiemens égale dix puissance moins trois siemens، إذن {ds(SIG * 1e-3, 2)} siemens par mètre.", f"Juste : {fr(SIG, 1)} mS/m = {sci(SIG * 1e-3, 2)} S/m."),
        0: (("لا، ضربتي فmille. le millisiemens صغير من le siemens: كنقسمو. عاود اختار.", "Le millisiemens est plus petit que le siemens : on divise par 1000. Réessaie."),
            (f"الجواب: {ds(SIG * 1e-3, 2)} siemens par mètre، حيت un millisiemens égale dix puissance moins trois siemens.", f"Réponse : {sci(SIG * 1e-3, 2)} S/m (1 mS = 10⁻³ S).")),
        2: (("ما تقلقش، نسيتي التحويل. un millisiemens ماشي un siemens. عاود اختار.", "Il manque la conversion : 1 mS ≠ 1 S. Réessaie."),
            (f"الجواب: {ds(SIG * 1e-3, 2)} siemens par mètre.", f"Réponse : {sci(SIG * 1e-3, 2)} S/m."))},
      f"sigma égale {d(SIG, 1)} millisiemens par mètre. En siemens par mètre, sigma vaut ?"),
  vf("fa_3", "Plus facile : vrai ou faux", f"[H₃O⁺] = {fr(H_M3, 3)} mol/m³.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("1 mol/L = 1000 mol/m³.", True, "Un mètre cube contient 1000 litres."),
      (f"[H₃O⁺] = {fr(H_M3 * 1000, 0)} mol/L.", False, "On divise par 1000, on ne multiplie pas."),
      (f"[H₃O⁺] = {sci(H, 2)} mol/L.", True, f"{fr(H_M3, 3)} / 1000 = {sci(H, 2)} mol/L.")]),
  qcm("fa_4", "Plus facile : τ", "سؤال ساهل على tau.",
      f"[H₃O⁺] = {sci(H, 2)} mol/L et C = {sci(C, 1)} mol/L. τ vaut…",
      [f"{fr(TAU, 2)}", f"{fr(1 / TAU, 2)}", "1"], 0, {
        0: ("juste", f"برافو! tau égale la concentration des ions H trois O plus sur C، يعني {d(TAU, 2)}. صغر من un: la réaction limitée.", f"Juste : τ = {fr(TAU, 2)} < 1, réaction limitée."),
        1: (("لا، قلبتي la fraction. tau ديما صغر ولا يساوي un. عاود اختار.", "Fraction inversée : τ ne dépasse jamais 1. Réessaie."),
            (f"الجواب: {d(TAU, 2)}، tau égale la concentration des ions H trois O plus sur C.", f"Réponse : τ = [H₃O⁺]/C = {fr(TAU, 2)}.")),
        2: (("لا، tau égale un غير يلا كانت la réaction totale، يعني la concentration des ions H trois O plus égale C. واش هنا égale؟ عاود اختار.", "τ = 1 seulement si [H₃O⁺] = C. Est-ce le cas ? Réessaie."),
            (f"الجواب: {d(TAU, 2)}. la concentration des ions H trois O plus صغر من C.", f"Réponse : τ = {fr(TAU, 2)}, car [H₃O⁺] < C."))},
      f"La concentration des ions H trois O plus égale {ds(H, 2)} mole par litre, et C égale {ds(C, 1)} mole par litre. Tau vaut ?"),
]

SIM_Q = [
  QS("1", "Quels ions conduisent ? Montrer que σ = (λ₁ + λ₂)·[H₃O⁺]_éq.",
     phrase("H₃O⁺ et HCOO⁻ ; " + REL + " car [HCOO⁻] = [H₃O⁺]"),
     (["σ = Σ λᵢ·[Xᵢ]", "[HCOO⁻] = [H₃O⁺]"], ["σ = λ₁ + λ₂"]),
     [(REL, "إذن sigma égale")], f"les ions H trois O plus و les ions méthanoate. {REL_DIT}."),
  QS("2", f"σ = {fr(sSIG, 1)} mS/m. Calculer [H₃O⁺]_éq en mol·m⁻³.",
     val("[H₃O⁺]", sH_M3, "mol/m³", f"[H₃O⁺] = σ/(λ₁ + λ₂) = {sci(sSIG * 1e-3, 2)} / {sci((L1 + L2) * 1e-3, 3)} = {fr(sH_M3, 3)} mol/m³"),
     (["σ/(λ₁ + λ₂)", "mol·m⁻³"], ["σ·(λ₁ + λ₂)"]),
     [(f"[H₃O⁺] = {fr(sH_M3, 3)} mol/m³", f"{d(sH_M3, 3)} mole par mètre cube")],
     f"la concentration égale sigma sur lambda un plus lambda deux، يعني {d(sH_M3, 3)} mole par mètre cube."),
  QS("3", "Exprimer cette concentration en mol/L.",
     val("[H₃O⁺]", sH, "mol/L", f"[H₃O⁺] = {fr(sH_M3, 3)} × 10⁻³ = {sci(sH, 2)} mol/L"),
     (["÷ 1000", "mol/L"], ["× 1000"]),
     [(f"[H₃O⁺] = {sci(sH, 2)} mol/L", f"{ds(sH, 2)} mole par litre")],
     f"كنقسمو على mille: {ds(sH, 2)} mole par litre."),
  QS("4", f"C = {sci(sC, 1)} mol/L. Avec τ = [H₃O⁺]_éq/C, calculer τ et conclure.",
     val("τ", sTAU, None, f"τ = {sci(sH, 2)} / {sci(sC, 1)} = {fr(sTAU, 2)} < 1 : limitée"),
     (["τ = [H₃O⁺]/C"], ["τ = C/[H₃O⁺]"]),
     [(f"τ = {fr(sTAU, 2)} < 1 : réaction limitée", f"tau égale {d(sTAU, 2)}")],
     f"tau égale {d(sTAU, 2)}. صغر من un: la réaction limitée."),
]

EX = exercice(
  "phys_ex_ch11_deux_sens_2", "phys_ch11_transformations_deux_sens", "transformations_deux_sens",
  "L'acide méthanoïque : τ par la conductimétrie", "facile", 15,
  ["Identifier les ions qui conduisent", "Calculer [H₃O⁺] = σ/(λ₁ + λ₂) avec les bonnes unités",
   "Convertir mol/m³ en mol/L", "Calculer τ et conclure"],
  f"On mesure, à 25 °C, la conductivité d'une solution aqueuse d'acide méthanoïque HCOOH de concentration C = {sci(C, 1)} mol/L : σ = {fr(SIG, 1)} mS/m. L'équation de la réaction de l'acide avec l'eau s'écrit : HCOOH(aq) + H₂O(l) ⇌ HCOO⁻(aq) + H₃O⁺(aq).",
  f"دابا نقراو l'énoncé. عندنا محلول ديال l'acide méthanoïque، C égale {ds(C, 1)} mole par litre. la conductivité ديالو sigma égale {d(SIG, 1)} millisiemens par mètre. l'équation: l'acide méthanoïque، plus H deux O، double flèche، l'ion méthanoate، plus H trois O plus.",
  [],
  [f"C = {sci(C, 1)} mol/L", f"σ = {fr(SIG, 1)} mS/m", f"λ₁ = λ(H₃O⁺) = {fr(L1, 1)} mS·m²/mol", f"λ₂ = λ(HCOO⁻) = {fr(L2, 2)} mS·m²/mol",
   "1 mS = 10⁻³ S ; 1 m³ = 1000 L"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  f"Une solution d'acide méthanoïque de concentration C = {sci(sC, 1)} mol/L a, à 25 °C, une conductivité σ = {fr(sSIG, 1)} mS/m.",
  f"نفس التمرين، بقيم أخرى. C égale {ds(sC, 1)} mole par litre، و sigma égale {d(sSIG, 1)} millisiemens par mètre.",
  [], [f"C = {sci(sC, 1)} mol/L", f"σ = {fr(sSIG, 1)} mS/m", f"λ₁ = {fr(L1, 1)} mS·m²/mol ; λ₂ = {fr(L2, 2)} mS·m²/mol"],
  SIM_Q)

ecrire(EX)
