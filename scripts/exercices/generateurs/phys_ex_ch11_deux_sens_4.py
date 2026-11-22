# Exercice de chimie, ch. 11 (transformations dans les deux sens), niveau moyen (celui du national) : deux acides de
# même concentration suivis par conductimétrie ; σ → [H₃O⁺] (piège mol/m³), « montrer que τ = σ/(C(λ₁ + λ₂)) », τ des
# deux acides, puis la conclusion « totale / limitée, τ dépend de la nature de l'acide ».
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2019 N (2.3.1 [H₃O⁺] par σ, 2.3.2 « montrer que τ = σ/(C(λ₁ + λ₂)) »),
#    2017 N (2.3 « laquelle des deux réactions est totale »), 2024 R (2.4 τ ≈ 1, totale), 2021 R (Q10-11)
#    — backend/data/exams/physique ;
#  - profs (sources_chimie_ch9_ch11.md, chapitre C : Sbiro, acide benzoïque et σ = 36,1 mS/m ; El Founani, formule
#    τ = σ_f/(C(λ₁ + λ₂)) ; Hadjyne, acide fort / acide faible) ; pièges : C en mol/L dans la formule de τ, λ en mS,
#    oublier l'ion du chlorure pour HCl ;
#  - séries en ligne : alloschool (« taux d'avancement et conductimétrie corrigé », séance 8), kezakoo (exercices
#    transformation), talamidi (deux sens, non corrigés 1), moutamadris (fiche 17-2), labolycee (Centres étrangers
#    2010 : méthode pH et conductimétrie, lue seulement).
# Ici : l'acide propanoïque et l'acide chlorhydrique à 4,0 × 10⁻³ mol/L, nos σ (calculées, pKa ≈ 4,87, arrondies).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *
from _ch11 import *

L_H, L_P, L_CL = 35.0, 3.58, 7.63          # mS·m²/mol : H₃O⁺, C₂H₅COO⁻, Cl⁻
C = 4.0e-3; C_M3 = C * 1000                # mol/L ; mol/m³
S1, S2 = 8.64, 170.5                       # mS/m
H1_M3 = S1 / (L_H + L_P); H1 = H1_M3 / 1000
TAU1 = (S1 * 1e-3) / (C_M3 * (L_H + L_P) * 1e-3)
TAU2 = (S2 * 1e-3) / (C_M3 * (L_H + L_CL) * 1e-3)
assert abs(H1 - 2.24e-4) < 1e-6 and abs(TAU1 - 0.0560) < 2e-4 and abs(TAU2 - 1.00) < 0.002

sC = 2.5e-3; sC_M3 = sC * 1000; L_B = 3.26     # acide butanoïque : C₃H₇COO⁻
sS1, sS2 = 7.12, 106.6
sH1 = sS1 / (L_H + L_B) / 1000
sTAU1 = sS1 / (sC_M3 * (L_H + L_B)); sTAU2 = sS2 / (sC_M3 * (L_H + L_CL))
assert abs(sH1 - 1.86e-4) < 1e-6 and abs(sTAU1 - 0.0744) < 2e-4 and abs(sTAU2 - 1.00) < 0.002

EQ1 = "C₂H₅COOH(aq) + H₂O(l) ⇌ C₂H₅COO⁻(aq) + H₃O⁺(aq)"
EQ2 = "HCl(g) + H₂O(l) → Cl⁻(aq) + H₃O⁺(aq)"
REL = "σ₁ = λ₁·[H₃O⁺] + λ₂·[C₂H₅COO⁻] = (λ₁ + λ₂)·x_f/V"

QUESTIONS = [
  Q("1", "Écrire l'équation de la réaction de l'acide propanoïque avec l'eau. En négligeant les ions HO⁻, montrer que σ₁ = (λ₁ + λ₂)·x_f/V.",
    "السؤال un: كتب l'équation ديال l'acide propanoïque مع الما. ومن بعد بين أن sigma un égale lambda un plus lambda deux، fois x f sur V.",
    phrase(EQ1 + " ; " + REL + " car [H₃O⁺] = [C₂H₅COO⁻] = x_f/V"),
    (["⇌", "σ = Σ λᵢ·[Xᵢ]", "x_f/V", "[H₃O⁺] = [C₂H₅COO⁻]"], ["σ₁ = (λ₁ + λ₂)·C", "→"]),
    [("Quels ions la réaction forme-t-elle ? Chacun compte dans σ avec sa conductivité molaire ionique.",
      "شنو هوما les ions اللي كتكون la réaction؟ كل ion كيحسب ف sigma مع lambda ديالو."),
     ("Dans le tableau, n(H₃O⁺)_f = n(C₂H₅COO⁻)_f = x_f, dans le même volume V : même concentration x_f/V.",
      "فle tableau، deux produits عندهم x f، فنفس le volume V: نفس la concentration، x f sur V.")],
    [(f"1 : {EQ1}", "l'équation"),
     ("σ₁ = λ₁·[H₃O⁺] + λ₂·[C₂H₅COO⁻]", "sigma un égale lambda un"),
     ("[H₃O⁺] = [C₂H₅COO⁻] = x_f/V, donc σ₁ = (λ₁ + λ₂)·x_f/V", "إذن sigma un égale lambda un plus lambda deux")],
    "السؤال un. l'équation: l'acide propanoïque، plus H deux O، double flèche، l'ion propanoate، plus H trois O plus. sigma un égale lambda un fois la concentration des ions H trois O plus، plus lambda deux fois la concentration des ions propanoate. وهوما بجوج x f sur V. إذن sigma un égale lambda un plus lambda deux، fois x f sur V.",
    "ex_1", "fa_1"),
  Q("2", "Calculer la concentration [H₃O⁺]_éq dans S₁, en mol/L.",
    "السؤال deux: حسب la concentration des ions H trois O plus ف S un، ب mole par litre.",
    val("[H₃O⁺]", H1, "mol/L", f"[H₃O⁺] = σ₁/(λ₁ + λ₂) = {sci(S1 * 1e-3, 2)}/{sci((L_H + L_P) * 1e-3, 3)} = {fr(H1_M3, 3)} mol/m³ = {sci(H1, 2)} mol/L"),
    (["[H₃O⁺] = σ/(λ₁ + λ₂)", "mS = 10⁻³ S", "1 mol/L = 1000 mol/m³"], [f"{fr(H1_M3, 3)} mol/L", "σ·(λ₁ + λ₂)"]),
    [("x_f/V est justement [H₃O⁺] : isole-la. Mets σ en S/m et les λ en S·m²/mol.",
      "x f sur V هي la concentration des ions H trois O plus. خرجها. و sigma ب siemens par mètre، و lambda ب siemens mètre carré par mole."),
     ("Le résultat sort en mol/m³ : divise par 1000 pour l'avoir en mol/L.", "le résultat كيخرج ب mole par mètre cube: قسم على mille باش يولي ب mole par litre.")],
    [("2 : [H₃O⁺] = σ₁/(λ₁ + λ₂)", "égale sigma un sur lambda un plus lambda deux"),
     (f"[H₃O⁺] = {sci(S1 * 1e-3, 2)}/{sci((L_H + L_P) * 1e-3, 3)} = {fr(H1_M3, 3)} mol/m³", f"{d(H1_M3, 3)} mole par mètre cube"),
     (f"[H₃O⁺] = {sci(H1, 2)} mol/L", f"{ds(H1, 2)} mole par litre")],
    f"السؤال deux. la concentration égale sigma un sur lambda un plus lambda deux، يعني {ds(S1 * 1e-3, 2)}، sur {ds((L_H + L_P) * 1e-3, 3)}. كتعطي {d(H1_M3, 3)} mole par mètre cube، كنقسمو على mille: {ds(H1, 2)} mole par litre.",
    "ex_2", "fa_2"),
  Q("3", "Montrer que τ₁ = σ₁/(C·(λ₁ + λ₂)), puis calculer τ₁.",
    "السؤال trois: بين أن tau un égale sigma un، sur C fois lambda un plus lambda deux. ومن بعد حسب tau un.",
    val("τ₁", TAU1, None, f"τ₁ = x_f/x_max = σ₁·V/((λ₁ + λ₂)·C·V) = σ₁/(C·(λ₁ + λ₂)) = {sci(S1 * 1e-3, 2)}/({fr(C_M3, 1)} × {sci((L_H + L_P) * 1e-3, 3)}) = {fr(TAU1, 3)}"),
    (["τ = x_f/x_max", "x_max = C·V", "C en mol/m³"], [f"C = {sci(C, 1)} mol/m³", "τ = C·(λ₁ + λ₂)/σ"]),
    [("Pars de τ = x_f/x_max : x_f vient de la question 1, x_max = C·V (l'eau en excès).",
      "بدا من tau égale x f sur x max. x f كتجي من السؤال un، و x max égale C fois V."),
     ("x_f = σ₁·V/(λ₁ + λ₂) ; V se simplifie. Attention : C doit être en mol/m³ (4,0 × 10⁻³ mol/L = 4,0 mol/m³).",
      "x f égale sigma un fois V، sur lambda un plus lambda deux. V كيتحيد. ورد البال: C خاصها تكون ب mole par mètre cube.")],
    [("3 : τ₁ = x_f/x_max avec x_f = σ₁·V/(λ₁ + λ₂) et x_max = C·V", "tau un égale x f sur x max"),
     ("τ₁ = σ₁/(C·(λ₁ + λ₂))", "V كيتحيد"),
     (f"τ₁ = {sci(S1 * 1e-3, 2)}/({fr(C_M3, 1)} × {sci((L_H + L_P) * 1e-3, 3)}) = {fr(TAU1, 3)}", f"tau un égale {d(TAU1, 3)}")],
    f"السؤال trois. tau un égale x f sur x max. x f égale sigma un fois V، sur lambda un plus lambda deux، و x max égale C fois V. V كيتحيد: tau un égale sigma un، sur C fois lambda un plus lambda deux. و C ب mole par mètre cube: {d(C_M3, 1)} mole par mètre cube. tau un égale {d(TAU1, 3)}.",
    "ex_3", "fa_3"),
  Q("4", f"La solution S₂ d'acide chlorhydrique, de même concentration C, a une conductivité σ₂ = {fr(S2, 1)} mS/m. Calculer le taux d'avancement final τ₂ de la réaction du chlorure d'hydrogène avec l'eau.",
    f"السؤال quatre: المحلول S deux ديال l'acide chlorhydrique، نفس C، sigma deux égale {d(S2, 1)} millisiemens par mètre. حسب tau deux.",
    val("τ₂", TAU2, None, f"τ₂ = σ₂/(C·(λ₁ + λ₃)) = {sci(S2 * 1e-3, 4)}/({fr(C_M3, 1)} × {sci((L_H + L_CL) * 1e-3, 4)}) = {fr(TAU2, 2)}", tol=0.02),
    (["τ = σ/(C·Σλ)", "λ₃ = λ(Cl⁻)", "mol/m³"], ["λ₂ = λ(C₂H₅COO⁻)", "τ₂ = σ₂/σ₁"]),
    [("Même démonstration qu'en 3 : seuls les ions changent. Quels ions forme le chlorure d'hydrogène avec l'eau ?",
      "نفس la démonstration ديال السؤال trois، غير les ions اللي تبدلو. شنو هوما les ions ديال l'acide chlorhydrique؟"),
     ("Les ions sont H₃O⁺ et Cl⁻ : τ₂ = σ₂/(C·(λ₁ + λ₃)), avec C en mol/m³.",
      "les ions هوما H trois O plus و C l moins: tau deux égale sigma deux، sur C fois lambda un plus lambda trois.")],
    [("4 : les ions de S₂ sont H₃O⁺ et Cl⁻ : τ₂ = σ₂/(C·(λ₁ + λ₃))", "H trois O plus و C l moins"),
     (f"τ₂ = {sci(S2 * 1e-3, 4)}/({fr(C_M3, 1)} × {sci((L_H + L_CL) * 1e-3, 4)})", "sur C fois lambda un plus lambda trois"),
     (f"τ₂ = {fr(TAU2, 2)}", f"tau deux égale {d(TAU2, 2)}")],
    f"السؤال quatre. ف S deux، les ions هوما H trois O plus و C l moins. tau deux égale sigma deux، sur C fois lambda un plus lambda trois. l'application numérique كتعطي tau deux égale {d(TAU2, 2)}، يعني un.",
    "ex_4", "fa_4"),
  Q("5", "Comparer τ₁ et τ₂. Préciser, pour chaque acide, si sa réaction avec l'eau est totale ou limitée et la flèche qui convient. Que peut-on conclure ?",
    "السؤال cinq: قارن tau un و tau deux. قول لكل acide واش la réaction ديالو مع الما totale ولا limitée، وشمن flèche. شنو نستنتجو؟",
    phrase(f"τ₂ ≈ 1 : réaction de HCl totale, {EQ2} ; τ₁ ≈ {fr(TAU1, 3)} < 1 : réaction de l'acide propanoïque limitée (⇌) ; à même concentration, τ dépend de la nature de l'acide"),
    (["τ = 1 : totale", "τ < 1 : limitée", "→", "⇌", "nature de l'acide"], ["τ dépend de C seulement", "les deux sont totales"]),
    [("Une réaction totale a x_f = x_max, donc τ = 1 ; une réaction limitée a τ < 1.",
      "la réaction totale عندها x f égale x max، يعني tau égale un. و la réaction limitée عندها tau صغر من un."),
     ("Les deux solutions ont la même concentration : la différence de τ ne peut venir que de l'acide lui-même.",
      "deux solutions عندهم نفس la concentration. إذن الفرق ف tau جاي غير من l'acide.")],
    [("5 : τ₂ ≈ 1 : la réaction de HCl avec l'eau est totale, flèche simple →", "tau deux égale un"),
     (f"τ₁ ≈ {fr(TAU1, 3)} < 1 : la réaction de l'acide propanoïque est limitée, double flèche ⇌", "tau un صغر من un"),
     ("même concentration, τ différents : τ dépend de la nature de l'acide", "tau dépend de la nature de l'acide")],
    "السؤال cinq. tau deux égale un: la réaction ديال l'acide chlorhydrique مع الما totale، ب flèche simple. tau un صغر من un: la réaction ديال l'acide propanoïque limitée، ب la double flèche. نفس la concentration، ولكن tau ماشي بحال بحال: tau dépend de la nature de l'acide.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sl_cond_relation("ex_1", "Question 1 : σ₁ = (λ₁ + λ₂)·x_f/V",
    "les ions هوما H trois O plus و l'ion propanoate، و بجوج x f sur V. إذن sigma un égale lambda un plus lambda deux، fois x f sur V.",
    [(REL, "إذن sigma un égale lambda un plus lambda deux")]),
  sl_cond_calcul("ex_2", "Question 2 : [H₃O⁺] dans S₁",
    f"sigma un égale {ds(S1 * 1e-3, 2)} siemens par mètre، و lambda un plus lambda deux égale {ds((L_H + L_P) * 1e-3, 3)}. كتعطي {d(H1_M3, 3)} mole par mètre cube، يعني {ds(H1, 2)} mole par litre.",
    [(f"[H₃O⁺] = {fr(H1_M3, 3)} mol/m³", f"كتعطي {d(H1_M3, 3)} mole par mètre cube"), (f"[H₃O⁺] = {sci(H1, 2)} mol/L", f"يعني {ds(H1, 2)} mole par litre")]),
  sl_taux("ex_3", "Question 3 : τ₁ = σ₁/(C·(λ₁ + λ₂))",
    f"x f كتجي من sigma، و x max égale C fois V. V كيتحيد: tau un égale sigma un، sur C fois lambda un plus lambda deux، و C ب mole par mètre cube، {d(C_M3, 1)}. tau un égale {d(TAU1, 3)}، صغر من un.",
    [("τ₁ = σ₁/(C·(λ₁ + λ₂))", "V كيتحيد"), (f"τ₁ = {fr(TAU1, 3)}", f"tau un égale {d(TAU1, 3)}")]),
  sl_cond_ions("ex_4", "Question 4 : l'acide chlorhydrique conduit beaucoup plus",
    f"S deux كتعطي {d(S2, 1)} millisiemens par mètre، بزاف كثر من S un. les ions: H trois O plus و C l moins. tau deux égale sigma deux، sur C fois lambda un plus lambda trois، يعني {d(TAU2, 2)}.",
    [("τ₂ = σ₂/(C·(λ₁ + λ₃))", "les ions: H trois O plus و C l moins"), (f"τ₂ = {fr(TAU2, 2)}", f"يعني {d(TAU2, 2)}")]),
  sl_nature("ex_5", "Question 5 : τ dépend de l'acide",
    "نفس الشي: l'acide chlorhydrique، tau égale un، totale، ب flèche simple. l'acide propanoïque، tau صغر من un، limitée، ب la double flèche.",
    [("HCl : τ = 1, totale (→)", "نفس الشي: l'acide chlorhydrique"), ("C₂H₅COOH : τ < 1, limitée (⇌)", "l'acide propanoïque، tau صغر من un")]),
]

FACILES = [
  vf("fa_1", "Plus facile : vrai ou faux", "Solution d'acide propanoïque : quels ions, quelle relation ?",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("Les molécules C₂H₅COOH participent à la conductivité.", False, "Seuls les ions conduisent : H₃O⁺ et C₂H₅COO⁻."),
      ("[H₃O⁺] = [C₂H₅COO⁻] = x_f/V.", True, "Les deux produits valent x_f dans le tableau, dans le même volume."),
      ("σ₁ = (λ₁ + λ₂)·x_f/V.", True, "On factorise les deux termes de même concentration.")]),
  qcm("fa_2", "Plus facile : mol/m³ ou mol/L ?", "سؤال ساهل على الوحدات.",
      f"On trouve [H₃O⁺] = {fr(H1_M3, 3)} mol/m³. En mol/L, cela fait…",
      [f"{fr(H1_M3 * 1000, 0)} mol/L", f"{sci(H1, 2)} mol/L", f"{fr(H1_M3, 3)} mol/L"], 1, {
        1: ("juste", f"برافو! كنقسمو على mille: {ds(H1, 2)} mole par litre.", f"Juste : {fr(H1_M3, 3)}/1000 = {sci(H1, 2)} mol/L."),
        0: (("لا، ضربتي فmille. le litre صغير من le mètre cube، إذن ف litre كاين قل. عاود اختار.", "Un litre est plus petit qu'un mètre cube : on divise. Réessaie."),
            (f"الجواب: {ds(H1, 2)} mole par litre، كنقسمو على mille.", f"Réponse : {sci(H1, 2)} mol/L.")),
        2: (("نسيتي التحويل: mole par mètre cube ماشي mole par litre. عاود اختار.", "Il manque la conversion. Réessaie."),
            (f"الجواب: {ds(H1, 2)} mole par litre.", f"Réponse : {sci(H1, 2)} mol/L."))},
      f"On trouve {d(H1_M3, 3)} mole par mètre cube. En mole par litre, cela fait ?"),
  qcm("fa_3", "Plus facile : C dans la formule de τ", "سؤال ساهل: شمن قيمة ديال C نحطو؟",
      f"Dans τ₁ = σ₁/(C·(λ₁ + λ₂)), avec σ en S/m et λ en S·m²/mol, on remplace C = {sci(C, 1)} mol/L par…",
      [f"{sci(C, 1)}", f"{fr(C_M3, 1)}", f"{sci(C / 1000, 1)}"], 1, {
        1: ("juste", f"برافو! مع les siemens والمتر، C خاصها تكون ب mole par mètre cube: {d(C_M3, 1)}.", f"Juste : C = {fr(C_M3, 1)} mol/m³."),
        0: (("لا، هادي ب mole par litre. الوحدات ديال sigma و lambda كيطلبو mole par mètre cube. عاود اختار.", "Ça, c'est en mol/L ; il faut des mol/m³. Réessaie."),
            (f"الجواب: {d(C_M3, 1)} mole par mètre cube، حيت une mole par litre égale mille moles par mètre cube.", f"Réponse : {fr(C_M3, 1)} mol/m³.")),
        2: (("لا، قسمتي على mille. من mole par litre ل mole par mètre cube كنضربو. عاود اختار.", "Pour passer en mol/m³, on multiplie par 1000. Réessaie."),
            (f"الجواب: {d(C_M3, 1)} mole par mètre cube.", f"Réponse : {fr(C_M3, 1)} mol/m³."))},
      f"Dans la formule de tau un, on remplace C égale {ds(C, 1)} mole par litre par ?"),
  qcm("fa_4", "Plus facile : τ₂", "سؤال ساهل على tau deux.",
      f"σ₂ = {fr(S2, 1)} mS/m pour HCl à C = {fr(C_M3, 1)} mol/m³, λ₁ + λ₃ = {fr(L_H + L_CL, 2)} mS·m²/mol. τ₂ vaut…",
      ["1,0", "0,056", f"{fr(S2 / (C_M3 * (L_H + L_P)), 2)}"], 0, {
        0: ("juste", "برافو! tau deux égale un: كل l'acide تفاعل، la réaction totale.", "Juste : τ₂ ≈ 1, réaction totale."),
        1: (("لا، هادي tau un ديال l'acide propanoïque. حسب ب sigma deux. عاود اختار.", "C'est τ₁ ; calcule avec σ₂. Réessaie."),
            ("الجواب: un. sigma deux sur C fois lambda un plus lambda trois.", "Réponse : τ₂ = σ₂/(C·(λ₁ + λ₃)) ≈ 1.")),
        2: (("لا، tau ما يمكنش يفوت un. خديتي lambda ديال l'ion propanoate بلاصة C l moins. عاود اختار.", "τ ne dépasse pas 1 : tu as pris λ du propanoate au lieu de Cl⁻. Réessaie."),
            ("الجواب: un، مع lambda ديال C l moins.", "Réponse : τ₂ ≈ 1 avec λ(Cl⁻)."))},
      f"sigma deux égale {d(S2, 1)} millisiemens par mètre, C égale {d(C_M3, 1)} mole par mètre cube. Tau deux vaut ?"),
  assoc("fa_5", "Plus facile : totale ou limitée ?", "Relie chaque acide à ce qui le décrit.",
    "سؤال ساهل: ربط كل acide مع اللي كيوصفو.",
    "Relie chaque solution à la conclusion qui lui convient.",
    [("1", "Acide chlorhydrique, τ₂ ≈ 1"), ("2", f"Acide propanoïque, τ₁ ≈ {fr(TAU1, 3)}")],
    [("a", "réaction totale, flèche →"), ("b", "réaction limitée, double flèche ⇌"), ("c", "pas de réaction avec l'eau")],
    {"1": "a", "2": "b"},
    {"1-a": (True, "Oui : τ = 1, tout l'acide a réagi.", "برافو: tau égale un، l'acide كامل تفاعل."),
     "1-b": (False, "Limitée veut dire τ < 1 : est-ce le cas pour τ₂ ?", "لا، limitée معناها tau صغر من un. واش tau deux صغر من un؟"),
     "1-c": (False, "Il a réagi : la solution conduit beaucoup grâce aux ions formés.", "لا، تفاعل: المحلول كيدوز le courant بزاف بفضل les ions."),
     "2-a": (False, "Totale voudrait dire τ = 1 : ici τ est bien plus petit.", "لا، totale معناها tau égale un، وهنا tau صغير بزاف."),
     "2-b": (True, "Oui : τ < 1, la réaction est limitée et s'écrit avec ⇌.", "برافو: tau صغر من un، la réaction limitée، ب la double flèche."),
     "2-c": (False, "Il a réagi un peu : des ions se sont formés, σ₁ n'est pas nulle.", "لا، تفاعل شوية: تكونو des ions، و sigma un ماشي zéro.")},
    ("(1 ; a) (2 ; b) : à même concentration, τ dépend de la nature de l'acide.",
     "نفس la concentration، ولكن tau dépend de la nature de l'acide.")),
]

SIM_Q = [
  QS("1", "Écrire l'équation de la réaction de l'acide butanoïque C₃H₇COOH avec l'eau et montrer que σ₁ = (λ₁ + λ₂)·x_f/V.",
     phrase("C₃H₇COOH + H₂O ⇌ C₃H₇COO⁻ + H₃O⁺ ; σ₁ = (λ₁ + λ₂)·x_f/V car [H₃O⁺] = [C₃H₇COO⁻] = x_f/V"),
     (["⇌", "x_f/V"], ["→"]),
     [("σ₁ = (λ₁ + λ₂)·x_f/V", "sigma un égale")],
     "l'acide butanoïque، plus H deux O، double flèche، l'ion butanoate، plus H trois O plus. sigma un égale lambda un plus lambda deux، fois x f sur V."),
  QS("2", "Calculer [H₃O⁺]_éq dans S₁, en mol/L.",
     val("[H₃O⁺]", sH1, "mol/L", f"[H₃O⁺] = σ₁/(λ₁ + λ₂) = {fr(sH1 * 1000, 3)} mol/m³ = {sci(sH1, 2)} mol/L"),
     (["σ/(λ₁ + λ₂)", "÷ 1000"], ["× 1000"]),
     [(f"[H₃O⁺] = {fr(sH1 * 1000, 3)} mol/m³ = {sci(sH1, 2)} mol/L", f"{ds(sH1, 2)} mole par litre")],
     f"la concentration égale sigma un sur lambda un plus lambda deux، {d(sH1 * 1000, 3)} mole par mètre cube، يعني {ds(sH1, 2)} mole par litre."),
  QS("3", "Montrer que τ₁ = σ₁/(C·(λ₁ + λ₂)) et calculer τ₁.",
     val("τ₁", sTAU1, None, f"τ₁ = σ₁/(C·(λ₁ + λ₂)) = {sci(sS1 * 1e-3, 2)}/({fr(sC_M3, 1)} × {sci((L_H + L_B) * 1e-3, 3)}) = {fr(sTAU1, 3)}"),
     (["τ = x_f/x_max", "C en mol/m³"], ["C en mol/L"]),
     [(f"τ₁ = {fr(sTAU1, 3)}", f"tau un égale {d(sTAU1, 3)}")],
     f"tau un égale x f sur x max، V كيتحيد، و C ب mole par mètre cube. tau un égale {d(sTAU1, 3)}."),
  QS("4", f"S₂ (acide chlorhydrique, même C) : σ₂ = {fr(sS2, 1)} mS/m. Calculer τ₂.",
     val("τ₂", sTAU2, None, f"τ₂ = σ₂/(C·(λ₁ + λ₃)) = {sci(sS2 * 1e-3, 4)}/({fr(sC_M3, 1)} × {sci((L_H + L_CL) * 1e-3, 4)}) = {fr(sTAU2, 2)}", tol=0.02),
     (["λ(Cl⁻)", "mol/m³"], ["λ(C₃H₇COO⁻)"]),
     [(f"τ₂ = {fr(sTAU2, 2)}", f"tau deux égale {d(sTAU2, 2)}")],
     f"tau deux égale sigma deux، sur C fois lambda un plus lambda trois. tau deux égale {d(sTAU2, 2)}."),
  QS("5", "Comparer τ₁ et τ₂ et conclure (totale ou limitée, flèche, nature de l'acide).",
     phrase("τ₂ ≈ 1 : HCl totale (→) ; τ₁ < 1 : acide butanoïque limitée (⇌) ; τ dépend de la nature de l'acide"),
     (["τ = 1", "τ < 1", "nature"], ["les deux totales"]),
     [("HCl : totale (→) ; acide butanoïque : limitée (⇌) ; τ dépend de la nature de l'acide", "tau dépend de la nature de l'acide")],
     "l'acide chlorhydrique: totale، flèche simple. l'acide butanoïque: limitée، double flèche. tau dépend de la nature de l'acide."),
]

EX = exercice(
  "phys_ex_ch11_deux_sens_4", "phys_ch11_transformations_deux_sens", "transformations_deux_sens",
  "Deux acides, une même concentration : τ par la conductimétrie", "moyen", 25,
  ["Écrire σ en fonction de x_f/V", "Calculer [H₃O⁺] à partir de σ (mS → S, mol/m³ → mol/L)",
   "Montrer que τ = σ/(C(λ₁ + λ₂)) et calculer τ", "Distinguer réaction totale et limitée ; τ dépend de l'acide"],
  f"On dispose, à 25 °C, de deux solutions de même concentration C = {sci(C, 1)} mol/L : S₁, solution d'acide propanoïque C₂H₅COOH, et S₂, solution d'acide chlorhydrique (chlorure d'hydrogène HCl dissous dans l'eau). On mesure leurs conductivités : σ₁ = {fr(S1, 2)} mS/m et σ₂ = {fr(S2, 1)} mS/m. On néglige les ions HO⁻ dans les deux solutions.",
  f"دابا نقراو l'énoncé. عندنا deux solutions، نفس la concentration، C égale {ds(C, 1)} mole par litre. S un ديال l'acide propanoïque، و S deux ديال l'acide chlorhydrique. sigma un égale {d(S1, 2)} millisiemens par mètre، و sigma deux égale {d(S2, 1)} millisiemens par mètre.",
  [tableau_texte("Mesures à 25 °C", ["Solution", "Acide", "C (mol/L)", "σ (mS/m)"],
                 [["S₁", "C₂H₅COOH", sci(C, 1), fr(S1, 2)], ["S₂", "HCl", sci(C, 1), fr(S2, 1)]])],
  [f"C = {sci(C, 1)} mol/L pour S₁ et S₂", f"λ₁ = λ(H₃O⁺) = {fr(L_H, 1)} mS·m²/mol", f"λ₂ = λ(C₂H₅COO⁻) = {fr(L_P, 2)} mS·m²/mol",
   f"λ₃ = λ(Cl⁻) = {fr(L_CL, 2)} mS·m²/mol", "1 mS = 10⁻³ S ; 1 mol/L = 1000 mol/m³"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  f"Deux solutions de même concentration C = {sci(sC, 1)} mol/L : S₁ d'acide butanoïque C₃H₇COOH (σ₁ = {fr(sS1, 2)} mS/m) et S₂ d'acide chlorhydrique (σ₂ = {fr(sS2, 1)} mS/m), à 25 °C.",
  f"نفس التمرين، بقيم أخرى. C égale {ds(sC, 1)} mole par litre. S un ديال l'acide butanoïque، sigma un égale {d(sS1, 2)} millisiemens par mètre. S deux ديال l'acide chlorhydrique، sigma deux égale {d(sS2, 1)} millisiemens par mètre.",
  [], [f"C = {sci(sC, 1)} mol/L", f"λ(H₃O⁺) = {fr(L_H, 1)} ; λ(C₃H₇COO⁻) = {fr(L_B, 2)} ; λ(Cl⁻) = {fr(L_CL, 2)} (mS·m²/mol)"],
  SIM_Q)

ecrire(EX)
