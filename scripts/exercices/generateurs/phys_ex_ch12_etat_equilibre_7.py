# Exercice de chimie, ch. 12 (état d'équilibre), niveau supérieur (au-dessus du national, même forme) :
# conductimétrie d'un acide, K, puis le problème RETOURNÉ : retrouver la concentration inconnue d'une solution à
# partir de sa conductivité et de K ; une lecture critique d'une erreur d'unité.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2019 N (2.3.1 σ → [H₃O⁺]éq, 2.3.2 montrer τ = σ/(C(λ₁ + λ₂)), 2.4 K en
#    fonction de C et τ), 2021 R (10-11 dilution), 2020 N (2.2-2.4 concentration, τ, Qr,éq) —
#    backend/data/exams/physique ; au national on va de C vers K ; ici on va aussi de K vers C ;
#  - profs (architecture/phys_ch12_etat_equilibre.md § 1 et § 6 : El Goufifa, Moutamadris, fiche 2BAC : Qr,éq par
#    conductimétrie) ; piège central relevé : [H₃O⁺] sort en mol·m⁻³ de σ/(λ₁ + λ₂) (τ > 1 absurde si on oublie) ;
#  - séries en ligne : alloschool (El Goufifa, séance 9), moutamadris (exercices état d'équilibre), talamidi (état
#    d'équilibre, activités 1), Naceiri Mrabti (livre 2BAC : activité des conductivités), docs Google d'un prof BIOF,
#    coursdusoirpc (TD BIOF).
# Ici : l'acide fluorhydrique HF à nos concentrations ; σ calculées à partir de K = 6,8 × 10⁻⁴ ;
# λ(H₃O⁺) = 35,0 et λ(F⁻) = 5,54 mS·m²·mol⁻¹.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch12 import *

L1, L2 = 35.0e-3, 5.54e-3
LS = L1 + L2


def de_sigma(sig):
    hm3 = sig / LS
    return hm3, hm3 / 1000


C1, SIG1, SIG2 = 1.0e-2, 92.8e-3, 22.4e-3
HM1, H1 = de_sigma(SIG1)
T1 = H1 / C1
K = C1 * T1 ** 2 / (1 - T1)
HM2, H2 = de_sigma(SIG2)
C2 = H2 + H2 ** 2 / K
T2 = H2 / C2
FAUX = HM1 / C1          # τ « trouvé » sans conversion
assert sci(H1, 2) == "2,29 × 10⁻³" and fr(T1, 2) == "0,23" and sci(K, 1) == "6,8 × 10⁻⁴"
assert sci(H2, 2) == "5,53 × 10⁻⁴" and sci(C2, 1) == "1,0 × 10⁻³" and fr(T2, 2) == "0,55" and round(FAUX) == 229
assert abs(C2 * T2 ** 2 / (1 - T2) - K) < 1e-12
sC1, sSIG1, sSIG2 = 5.0e-2, 223e-3, 35.5e-3
sHM1, sH1 = de_sigma(sSIG1)
sT1 = sH1 / sC1
sK = sC1 * sT1 ** 2 / (1 - sT1)
sHM2, sH2 = de_sigma(sSIG2)
sC2 = sH2 + sH2 ** 2 / sK
sT2 = sH2 / sC2
assert sci(sH1, 2) == "5,50 × 10⁻³" and fr(sT1, 2) == "0,11" and sci(sK, 1) == "6,8 × 10⁻⁴"
assert sci(sC2, 1) == "2,0 × 10⁻³" and fr(sT2, 2) == "0,44"

EQ = "HF(aq) + H₂O(l) ⇌ F⁻(aq) + H₃O⁺(aq)"
REL_C = "C₂ = [H₃O⁺]éq + [H₃O⁺]éq²/K"
REL_C_DIT = "C deux égale la concentration des ions H trois O plus، plus la concentration au carré، sur K"

QUESTIONS = [
  Q("1", "Montrer que [H₃O⁺]éq = σ/(λ₁ + λ₂), puis calculer [H₃O⁺]éq dans S₁, en mol·L⁻¹.",
    "السؤال un: بين بلي la concentration des ions H trois O plus égale sigma sur lambda un plus lambda deux، ومن بعد حسبها فS un ب mole par litre.",
    val("[H₃O⁺]éq", H1, "mol/L", f"σ₁ = λ₁[H₃O⁺]éq + λ₂[F⁻]éq = (λ₁ + λ₂)[H₃O⁺]éq ; [H₃O⁺]éq = 92,8 × 10⁻³/(40,54 × 10⁻³) = {fr(HM1, 2)} mol·m⁻³ = {sci(H1, 2)} mol/L"),
    (["σ = Σλᵢ[Xᵢ]", "[F⁻]éq = [H₃O⁺]éq", "mol·m⁻³", "÷ 1000"], ["× 1000", "σ = λ₁·λ₂·[H₃O⁺]"]),
    [("Deux ions conduisent : écris leurs deux contributions et utilise le tableau d'avancement.", "deux ions كيوصلو التيار: كتب la part ديال كل واحد، واستعمل le tableau d'avancement."),
     ("[F⁻]éq = [H₃O⁺]éq, donc σ = (λ₁ + λ₂)[H₃O⁺]éq. Le résultat sort en mol·m⁻³ : divise par 1000.", "les ions fluorure و H trois O plus عندهم نفس التركيز، إذن sigma égale lambda un plus lambda deux، fois la concentration. وكتخرج ب mole par mètre cube: قسم على mille.")],
    [("1 : σ₁ = λ₁[H₃O⁺]éq + λ₂[F⁻]éq et [F⁻]éq = [H₃O⁺]éq", "نفس التركيز"),
     ("[H₃O⁺]éq = σ₁/(λ₁ + λ₂)", "sigma un sur lambda un plus lambda deux"),
     (f"[H₃O⁺]éq = 92,8 × 10⁻³/(40,54 × 10⁻³) = {fr(HM1, 2)} mol·m⁻³ = {sci(H1, 2)} mol/L", f"{dsci(H1, 2)} mole par litre")],
    f"السؤال un. sigma un égale lambda un fois la concentration des ions H trois O plus، plus lambda deux fois la concentration des ions fluorure. وعندهم نفس التركيز، إذن la concentration égale sigma un sur lambda un plus lambda deux: quatre-vingt-douze virgule huit fois dix puissance moins trois، sur quarante virgule cinquante-quatre fois dix puissance moins trois. كتعطي {dfr(HM1, 2)} mole par mètre cube، يعني {dsci(H1, 2)} mole par litre.",
    "ex_1", "fa_1"),
  Q("2", "Calculer le taux d'avancement final τ₁. Un camarade trouve τ₁ = 229 : expliquer son erreur.",
    "السؤال deux: حسب tau un. واحد صاحبك لقى tau un égale deux cent vingt-neuf: شرح الغلطة ديالو.",
    val("τ₁", T1, None, f"τ₁ = [H₃O⁺]éq/C₁ = {sci(H1, 2)}/(1,0 × 10⁻²) ≈ {fr(T1, 2)} ; erreur : {fr(HM1, 2)} mol·m⁻³ divisé par C₁ en mol/L ; τ ≤ 1 toujours ; τ₁ ≈ {fr(T1, 2)}", tol=0.05),
    (["τ = [H₃O⁺]éq/C", "même unité", "τ ≤ 1"], ["τ = 229", "τ = C/[H₃O⁺]"]),
    [("τ = x_éq/x_max = [H₃O⁺]éq/C : les deux concentrations doivent être dans la même unité.", "tau égale la concentration des ions H trois O plus، sur C: بجوج خاصهم يكونو بنفس الوحدة."),
     ("229 = 2,29/0,010 : il a gardé les mol·m⁻³ en haut et les mol/L en bas. Un τ plus grand que 1 est impossible.", "deux cent vingt-neuf هي deux virgule vingt-neuf sur zéro virgule zéro dix: خلى mole par mètre cube الفوق و mole par litre التحت. و tau ما يمكنش يفوت un.")],
    [("2 : τ₁ = [H₃O⁺]éq/C₁", "tau un égale la concentration"),
     (f"τ₁ = {sci(H1, 2)}/(1,0 × 10⁻²) ≈ {fr(T1, 2)} < 1 : réaction limitée", f"tau un égale {dfr(T1, 2)}"),
     (f"l'erreur : {fr(HM1, 2)} (mol·m⁻³) divisé par 0,010 (mol/L) ; τ > 1 est impossible", "الغلطة ديال صاحبك")],
    f"السؤال deux. tau un égale la concentration des ions H trois O plus، sur C un: {dsci(H1, 2)}، sur un virgule zéro fois dix puissance moins deux. tau un égale {dfr(T1, 2)}، صغير من un: la réaction محدودة. الغلطة ديال صاحبك: قسم {dfr(HM1, 2)} mole par mètre cube على C ب mole par litre. و tau أكبر من un مستحيل: x éq ما يفوتش x max.",
    "ex_2", "fa_2"),
  Q("3", "Calculer la constante d'équilibre K associée à l'équation de la réaction de HF avec l'eau.",
    "السؤال trois: حسب la constante d'équilibre K ديال HF مع الما.",
    val("K", K, None, f"K = Qr,éq = C₁·τ₁²/(1 − τ₁) = 1,0 × 10⁻² × {fr(T1, 3)}²/(1 − {fr(T1, 3)}) ≈ {sci(K, 1)}", tol=0.05),
    (["K = Qr,éq", "C·τ²/(1 − τ)"], ["K = C·τ", "K = τ²"]),
    [("K = Qr,éq : écris les concentrations à l'équilibre en fonction de C₁ et τ₁.", "K égale Q r à l'équilibre: كتب les concentrations à l'équilibre ب C un و tau un."),
     ("K = C₁·τ₁²/(1 − τ₁) ; garde trois chiffres pour τ₁.", "K égale C un fois tau un au carré، sur un moins tau un. خلي trois chiffres ف tau un.")],
    [("3 : K = [F⁻]éq·[H₃O⁺]éq/[HF]éq = C₁·τ₁²/(1 − τ₁)", "égale C un fois tau un au carré"),
     (f"K = 1,0 × 10⁻² × {fr(T1, 3)}²/(1 − {fr(T1, 3)}) ≈ {sci(K, 1)}", f"K égale {dsci(K, 1)}")],
    f"السؤال trois. K égale Q r à l'équilibre، égale C un fois tau un au carré، sur un moins tau un. l'application numérique: un virgule zéro fois dix puissance moins deux، fois {dfr(T1, 3)} au carré، sur un moins {dfr(T1, 3)}. K égale {dsci(K, 1)}.",
    "ex_3", "fa_3"),
  Q("4", "Une solution S₂ d'acide fluorhydrique, de concentration C₂ inconnue, a une conductivité σ₂ = 22,4 mS·m⁻¹ à 25 °C. Montrer que C₂ = [H₃O⁺]éq + [H₃O⁺]éq²/K, puis calculer C₂.",
    "السؤال quatre: solution S deux ديال l'acide fluorhydrique، C deux ما معروفاش، و sigma deux égale vingt-deux virgule quatre millisiemens par mètre. بين بلي " + REL_C_DIT + "، ومن بعد حسب C deux.",
    val("C₂", C2, "mol/L", f"[H₃O⁺]éq = 22,4 × 10⁻³/(40,54 × 10⁻³) = {fr(HM2, 3)} mol·m⁻³ = {sci(H2, 2)} mol/L ; K = [H₃O⁺]²/[HF] ⇒ [HF]éq = [H₃O⁺]²/K ; C₂ = [H₃O⁺] + [HF]éq = {sci(H2, 2)} + {sci(H2 ** 2 / K, 2)} ≈ {sci(C2, 1)} mol/L", tol=0.04),
    (["[HF]éq = C₂ − [H₃O⁺]éq", "K = [H₃O⁺]²/[HF]", "÷ 1000", "mol/L"], ["C₂ = [H₃O⁺]éq", "C₂ = [H₃O⁺]²/K"]),
    [("K est la même (même acide, même température). Écris K avec [H₃O⁺]éq et [HF]éq, puis isole [HF]éq.", "K هي هي: نفس l'acide، نفس la température. كتب K ب la concentration des ions H trois O plus و HF، وخرج HF."),
     ("[HF]éq = [H₃O⁺]²/K, et l'acide apporté est C₂ = [HF]éq + [H₃O⁺]éq (ce qui reste + ce qui a réagi).", "HF égale la concentration au carré، sur K. و C deux égale اللي بقا، plus اللي تفاعل: HF plus H trois O plus.")],
    [(f"4 : [H₃O⁺]éq = σ₂/(λ₁ + λ₂) = {sci(H2, 2)} mol/L", "sigma deux sur lambda un plus lambda deux"),
     ("K = [H₃O⁺]éq²/[HF]éq ⇒ [HF]éq = [H₃O⁺]éq²/K ; C₂ = [HF]éq + [H₃O⁺]éq", "إذن " + REL_C_DIT),
     (f"C₂ = {sci(H2, 2)} + {sci(H2 ** 2 / K, 2)} ≈ {sci(C2, 1)} mol/L", f"C deux égale {dsci(C2, 1)} mole par litre")],
    f"السؤال quatre. أولا، la concentration des ions H trois O plus: sigma deux sur lambda un plus lambda deux، يعني {dsci(H2, 2)} mole par litre. ثانيا، K هي هي، و K égale la concentration au carré، sur HF. إذن HF égale la concentration au carré، sur K. و l'acide اللي حطينا هو اللي بقا plus اللي تفاعل: إذن {REL_C_DIT}. l'application numérique: {dsci(H2, 2)}، plus {dsci(H2 ** 2 / K, 2)}. C deux égale {dsci(C2, 1)} mole par litre.",
    "ex_4", "fa_4"),
  Q("5", "Calculer τ₂ et le comparer à τ₁. Les résultats sont-ils cohérents avec ce que le cours dit de l'influence de la concentration sur τ ?",
    "السؤال cinq: حسب tau deux وقارنو مع tau un. واش النتائج متافقة مع شنو كيقول le cours على l'effet ديال la concentration على tau؟",
    val("τ₂", T2, None, f"τ₂ = [H₃O⁺]éq/C₂ = {sci(H2, 2)}/{sci(C2, 2)} ≈ {fr(T2, 2)} > τ₁ ≈ {fr(T1, 2)} : C₂ < C₁ et τ₂ > τ₁ ; cohérent ; τ₂ ≈ {fr(T2, 2)}", tol=0.05),
    (["τ = [H₃O⁺]éq/C", "même K", "C₂ < C₁"], ["τ₂ = τ₁", "K₂ < K"]),
    [("Même relation qu'à la question 2, avec S₂.", "نفس la relation ديال السؤال deux، ب S deux."),
     ("Compare C₂ et C₁, puis τ₂ et τ₁ : à K égale, comment varie τ quand C diminue ?", "قارن C deux مع C un، و tau deux مع tau un: بنفس K، كيفاش كيتبدل tau ملي C كتنقص؟")],
    [(f"5 : τ₂ = {sci(H2, 2)}/{sci(C2, 2)} ≈ {fr(T2, 2)}", f"يعني {dfr(T2, 2)}"),
     (f"C₂ < C₁ et τ₂ > τ₁ : à K égale, plus C est petite, plus τ est grand ; cohérent", "plus C est petite، plus tau est grand")],
    f"السؤال cinq. tau deux égale la concentration des ions H trois O plus، sur C deux، يعني {dfr(T2, 2)}. C deux صغر من C un، و tau deux كبر من tau un: نفس K، plus C est petite، plus tau est grand. متافق مع le cours.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  slide("ex_1", "cond_rel", "Question 1 : [H₃O⁺]éq = σ/(λ₁ + λ₂)",
        "Deux ions, la même concentration : on met en facteur, puis on isole.",
        f"فالتمرين ديالنا: les ions H trois O plus و les ions fluorure. la concentration égale quatre-vingt-douze virgule huit fois dix puissance moins trois، sur quarante virgule cinquante-quatre fois dix puissance moins trois، يعني {dfr(HM1, 2)} mole par mètre cube، و {dsci(H1, 2)} mole par litre.",
        [("[H₃O⁺]éq = σ₁/(λ₁ + λ₂)", "فالتمرين ديالنا"), (f"= {sci(H1, 2)} mol/L", f"و {dsci(H1, 2)} mole par litre")]),
  slide("ex_2", "cond_calc", "Question 2 : τ₁, et le piège des unités",
        "σ/(λ₁ + λ₂) sort en mol·m⁻³ : sans conversion, τ dépasse 1.",
        f"فالتمرين ديالنا: يلا ما قسمناش على mille، كنلقاو tau égale deux cent vingt-neuf: مستحيل. ب mole par litre: tau un égale {dsci(H1, 2)}، sur un virgule zéro fois dix puissance moins deux، يعني {dfr(T1, 2)}.",
        [(f"τ₁ ≈ {fr(T1, 2)} (et non 229)", f"يعني {dfr(T1, 2)}")]),
  slide("ex_3", "c_tau", "Question 3 : K = C·τ²/(1 − τ)",
        "K = Qr,éq, avec les concentrations en C et τ.",
        f"فالتمرين ديالنا: K égale un virgule zéro fois dix puissance moins deux، fois {dfr(T1, 3)} au carré، sur un moins {dfr(T1, 3)}. K égale {dsci(K, 1)}.",
        [(f"K ≈ {sci(K, 1)}", f"K égale {dsci(K, 1)}")]),
  slide("ex_4", "concentrations", "Question 4 : remonter à la concentration apportée",
        "L'acide apporté = l'acide restant + l'acide qui a réagi.",
        f"هنا كنمشيو فالجهة الأخرى. فالتمرين ديالنا، la concentration des ions H trois O plus جات من sigma deux: {dsci(H2, 2)} mole par litre. l'acide اللي بقا، HF، égale la concentration au carré، sur K. و C deux égale اللي بقا plus اللي تفاعل: يعني {dsci(C2, 1)} mole par litre.",
        [(REL_C, "و C deux égale اللي بقا plus اللي تفاعل"), (f"C₂ ≈ {sci(C2, 1)} mol/L", f"يعني {dsci(C2, 1)} mole par litre")]),
  slide("ex_5", "dilution", "Question 5 : τ₂ plus grand, même K",
        "Moins concentrée, même acide : τ plus grand.",
        f"فالتمرين ديالنا: C deux صغيرة، و tau deux égale {dfr(T2, 2)}، كبر من tau un، {dfr(T1, 2)}. و K هي هي.",
        [(f"τ₂ ≈ {fr(T2, 2)} > τ₁ ≈ {fr(T1, 2)}", f"و tau deux égale {dfr(T2, 2)}")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : la conversion", "سؤال ساهل على الوحدة.",
      "σ/(λ₁ + λ₂) = 2,29 mol·m⁻³. En mol/L, [H₃O⁺]éq = …",
      ["2,29 × 10³ mol/L", "2,29 mol/L", "2,29 × 10⁻³ mol/L"], 2, {
        2: ("juste", "برافو! un mole par litre égale mille moles par mètre cube، إذن نقسمو على mille.", "Juste : 2,29/1000 = 2,29 × 10⁻³ mol/L."),
        0: (("لا، ضربتي ف mille. litre صغير بزاف من mètre cube. عاود اختار.", "Un litre est mille fois plus petit qu'un m³ : on divise. Réessaie."),
            ("الجواب: deux virgule vingt-neuf fois dix puissance moins trois mole par litre.", "Réponse : 2,29 × 10⁻³ mol/L.")),
        1: (("لا، ما حولتيش الوحدة. عاود اختار.", "Tu n'as pas converti. Réessaie."),
            ("الجواب: نقسمو على mille: deux virgule vingt-neuf fois dix puissance moins trois.", "Réponse : 2,29 × 10⁻³ mol/L."))},
      "sigma sur la somme des lambda égale deux virgule vingt-neuf mole par mètre cube. En mole par litre ?"),
  qcm("fa_2", "Plus facile : un τ possible ?", "سؤال ساهل: اختار tau اللي ممكن.",
      "Quelle valeur peut être un taux d'avancement final ?",
      ["229", "0,23", "−0,23"], 1, {
        1: ("juste", "برافو! tau ديما بين zéro و un: x éq ما يفوتش x max.", "Juste : 0 < τ ≤ 1."),
        0: (("لا، tau égale x éq sur x max، و x éq ما يفوتش x max. عاود اختار.", "τ ne dépasse pas 1. Réessaie."),
            ("الجواب: zéro virgule vingt-trois. deux cent vingt-neuf جات من غلطة ديال الوحدة.", "Réponse : 0,23 ; 229 vient d'un oubli de conversion.")),
        2: (("لا، tau ما يكونش سالب: جوج quantités موجبة. عاود اختار.", "Un taux n'est jamais négatif. Réessaie."),
            ("الجواب: zéro virgule vingt-trois.", "Réponse : 0,23."))},
      "Quelle valeur peut être un taux d'avancement final ?"),
  vf("fa_3", "Plus facile : vrai ou faux", "La constante K de HF avec l'eau.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("K = C·τ²/(1 − τ) pour un acide de concentration C dans l'eau.", True, "[F⁻] = [H₃O⁺] = C·τ et [HF] = C(1 − τ)."),
      ("Dans S₂, moins concentrée, K est plus petite.", False, "K ne dépend que de la température."),
      ("K est sans unité.", True, "Comme tout quotient de réaction.")]),
  qcm("fa_4", "Plus facile : l'acide apporté", "سؤال ساهل: شحال حطينا من l'acide؟",
      "À l'équilibre : [H₃O⁺]éq = 5,5 × 10⁻⁴ mol/L et [HF]éq = 4,5 × 10⁻⁴ mol/L. La concentration apportée C₂ vaut…",
      ["1,0 × 10⁻³ mol/L", "4,5 × 10⁻⁴ mol/L", "1,0 × 10⁻⁴ mol/L"], 0, {
        0: ("juste", "برافو! l'acide اللي حطينا égale اللي بقا، plus اللي تفاعل.", "Juste : C₂ = 4,5 × 10⁻⁴ + 5,5 × 10⁻⁴ = 1,0 × 10⁻³ mol/L."),
        1: (("لا، هادا غير اللي بقا. و اللي تفاعل وولا H trois O plus؟ عاود اختار.", "C'est seulement l'acide restant. Réessaie."),
            ("الجواب: un virgule zéro fois dix puissance moins trois: اللي بقا plus اللي تفاعل.", "Réponse : C₂ = [HF]éq + [H₃O⁺]éq = 1,0 × 10⁻³ mol/L.")),
        2: (("لا، طرحتي بلاصة ما تجمع. عاود اختار.", "Il faut additionner, pas soustraire. Réessaie."),
            ("الجواب: un virgule zéro fois dix puissance moins trois mole par litre.", "Réponse : C₂ = 1,0 × 10⁻³ mol/L."))},
      "À l'équilibre، H trois O plus égale cinq virgule cinq fois dix puissance moins quatre، et HF égale quatre virgule cinq fois dix puissance moins quatre mole par litre. C deux vaut ?"),
  vf("fa_5", "Plus facile : comparer S₁ et S₂", "S₂ est moins concentrée que S₁.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("τ₂ > τ₁, car C₂ < C₁ avec la même K.", True, "τ₂ ≈ 0,55 et τ₁ ≈ 0,23."),
      ("τ₂ > 0,5 : la réaction dans S₂ est totale.", False, "Totale veut dire τ = 1 ; ici τ₂ < 1 : limitée."),
      ("σ₂ < σ₁, car S₂ contient moins d'ions.", True, "[H₃O⁺] passe de 2,29 × 10⁻³ à 5,5 × 10⁻⁴ mol/L.")]),
]

SIM_Q = [
  QS("1", "S₁ : C₁ = 5,0 × 10⁻² mol/L, σ₁ = 223 mS·m⁻¹. Montrer que [H₃O⁺]éq = σ/(λ₁ + λ₂), puis la calculer en mol/L.",
     val("[H₃O⁺]éq", sH1, "mol/L", f"[H₃O⁺]éq = 223 × 10⁻³/(40,54 × 10⁻³) = {fr(sHM1, 2)} mol·m⁻³ = {sci(sH1, 2)} mol/L"),
     (["σ/(λ₁ + λ₂)", "÷ 1000"], ["× 1000"]),
     [(f"[H₃O⁺]éq = σ₁/(λ₁ + λ₂) = {fr(sHM1, 2)} mol·m⁻³ = {sci(sH1, 2)} mol/L", f"{dsci(sH1, 2)} mole par litre")],
     f"la concentration égale sigma un sur lambda un plus lambda deux، {dfr(sHM1, 2)} mole par mètre cube، يعني {dsci(sH1, 2)} mole par litre."),
  QS("2", "Calculer τ₁. Que vaudrait τ₁ sans la conversion, et pourquoi est-ce impossible ?",
     val("τ₁", sT1, None, f"sans conversion : {fr(sHM1 / sC1, 0)} > 1, impossible ; τ₁ = {sci(sH1, 2)}/(5,0 × 10⁻²) ≈ {fr(sT1, 2)}", tol=0.05),
     (["τ = [H₃O⁺]/C", "τ ≤ 1"], ["τ = 110"]),
     [(f"τ₁ ≈ {fr(sT1, 2)} ; sans conversion on trouverait {fr(sHM1 / sC1, 0)} > 1, impossible", f"tau un égale {dfr(sT1, 2)}")],
     f"tau un égale {dfr(sT1, 2)}. بلا التحويل كنلقاو {dire(fr(sHM1 / sC1, 0))}، أكبر من un: مستحيل."),
  QS("3", "Calculer K.",
     val("K", sK, None, f"K = 5,0 × 10⁻² × {fr(sT1, 3)}²/(1 − {fr(sT1, 3)}) ≈ {sci(sK, 1)}", tol=0.05),
     (["C·τ²/(1 − τ)"], ["K = C·τ"]),
     [(f"K ≈ {sci(sK, 1)}", f"{dsci(sK, 1)}")],
     f"K égale C un fois tau un au carré، sur un moins tau un، يعني {dsci(sK, 1)}."),
  QS("4", "S₂ : σ₂ = 35,5 mS·m⁻¹. Montrer que C₂ = [H₃O⁺]éq + [H₃O⁺]éq²/K et calculer C₂.",
     val("C₂", sC2, "mol/L", f"[H₃O⁺]éq = {sci(sH2, 2)} mol/L ; C₂ = {sci(sH2, 2)} + {sci(sH2 ** 2 / sK, 2)} ≈ {sci(sC2, 1)} mol/L", tol=0.04),
     (["[HF]éq = [H₃O⁺]²/K"], ["C₂ = [H₃O⁺]"]),
     [(REL_C, REL_C_DIT), (f"C₂ ≈ {sci(sC2, 1)} mol/L", f"{dsci(sC2, 1)} mole par litre")],
     f"HF égale la concentration au carré، sur K، و {REL_C_DIT}. C deux égale {dsci(sC2, 1)} mole par litre."),
  QS("5", "Calculer τ₂ et comparer à τ₁.",
     val("τ₂", sT2, None, f"τ₂ = {sci(sH2, 2)}/{sci(sC2, 2)} ≈ {fr(sT2, 2)} > τ₁", tol=0.05),
     (["τ = [H₃O⁺]/C"], ["τ₂ = τ₁"]),
     [(f"τ₂ ≈ {fr(sT2, 2)} > τ₁ : C plus petite, τ plus grand", f"tau deux égale {dfr(sT2, 2)}")],
     f"tau deux égale {dfr(sT2, 2)}، كبر من tau un: C صغيرة، tau كبير."),
]

EX = exercice(
  "phys_ex_ch12_etat_equilibre_7", "phys_ch12_etat_equilibre", "etat_equilibre",
  "L'acide fluorhydrique : de σ à K, puis de K à la concentration", "difficile", 35,
  ["Établir [H₃O⁺]éq = σ/(λ₁ + λ₂) et convertir", "Repérer une erreur d'unité par τ ≤ 1", "Calculer K", "Retrouver une concentration à partir de K et σ"],
  "L'acide fluorhydrique HF réagit avec l'eau selon : " + EQ + ". À 25 °C, une solution S₁ de concentration C₁ = 1,0 × 10⁻² mol/L a une conductivité σ₁ = 92,8 mS·m⁻¹. On néglige les ions HO⁻ ; les mesures sont faites à l'équilibre. Une autre solution S₂ du même acide, de concentration inconnue, a une conductivité σ₂ = 22,4 mS·m⁻¹ à 25 °C.",
  "دابا نقراو l'énoncé. l'acide fluorhydrique، HF، كيتفاعل مع الما ب la double flèche، وكيعطي les ions fluorure و les ions H trois O plus. S un، C un égale un virgule zéro fois dix puissance moins deux mole par litre، و sigma un égale quatre-vingt-douze virgule huit millisiemens par mètre. و S deux، نفس l'acide، la concentration ديالها ما معروفاش، و sigma deux égale vingt-deux virgule quatre millisiemens par mètre.",
  [], ["S₁ : C₁ = 1,0 × 10⁻² mol/L ; σ₁ = 92,8 mS·m⁻¹", "S₂ : C₂ inconnue ; σ₂ = 22,4 mS·m⁻¹",
       "λ₁ = λ(H₃O⁺) = 35,0 × 10⁻³ S·m²·mol⁻¹ ; λ₂ = λ(F⁻) = 5,54 × 10⁻³ S·m²·mol⁻¹"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Acide fluorhydrique à 25 °C : S₁ de concentration C₁ = 5,0 × 10⁻² mol/L, σ₁ = 223 mS·m⁻¹ ; S₂ de concentration inconnue, σ₂ = 35,5 mS·m⁻¹. Mêmes λ.",
  "نفس التمرين، بقيم أخرى: C un égale cinq virgule zéro fois dix puissance moins deux mole par litre، sigma un égale deux cent vingt-trois millisiemens par mètre، و sigma deux égale trente-cinq virgule cinq millisiemens par mètre.",
  [], ["S₁ : C₁ = 5,0 × 10⁻² mol/L ; σ₁ = 223 mS·m⁻¹", "S₂ : σ₂ = 35,5 mS·m⁻¹", "λ₁ = 35,0 × 10⁻³ ; λ₂ = 5,54 × 10⁻³ S·m²·mol⁻¹"],
  SIM_Q)

ecrire(EX)
