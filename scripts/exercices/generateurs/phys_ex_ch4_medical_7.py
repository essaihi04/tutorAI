# Exercice difficile (« Supérieur ») de physique (ch. 4, décroissance radioactive) : deux sources d'imagerie médicale
# (fluor 18 et carbone 11), la date où leurs activités sont égales.
# Sources comparées (skill exercices § 2) :
#  - exploration radioactivite.json : cas_types « nombre_noyaux » (N₀ = a₀/λ, λ en s⁻¹), « activite_date »
#    (t = (1/λ)·ln(a₀/a)), « pourcentage », « desintegres » ; pièges et erreurs_examen « λ laissé en j⁻¹ ou min⁻¹ dans
#    a = λ·N », « x % désintégrés pris pour x % restants », « m en µg mis dans N = (m/M)·N_A », « ln(a·b) = ln a · ln b » ;
#    valeurs_reperes N_A = 6,02·10²³ mol⁻¹, ln 2 ≈ 0,693.
#  - nationaux comparés : 2021 R ex. 3 (phosphore 32 en médecine : λ par la droite ln N, activité d'une masse donnée),
#    2024 N ex. 3 (iridium 192, curiethérapie : N_d), 2025 N ex. 2 (cadmium 107 : a à 2t½ et 3t½, N_d entre deux dates),
#    2023 N ex. 2 (tritium : activité quand 90 % sont désintégrés). Aucun national ne compare DEUX sources : le nôtre
#    combine deux lois de décroissance (« montrer que » la date d'égalité des activités), la masse restante, un
#    pourcentage désintégré et une lecture critique (a égales ≠ N égaux, car a = λ·N) : au-dessus du national.
#  - séries en ligne (recherche du 22/11/2026 ; pages non ouvrables depuis cette session, seuls les extraits du moteur
#    lus) : moutamadris 2ᵉ Bac SM (iode 131 et iode 123 : « temps au bout duquel les activités deviennent égales »),
#    groupe-reussite (deux noyaux, date d'égalité des activités), exercice BIOF sodium 24 (médecine), labolycée
#    « iode, thyroïde ». Nos nucléides et nos données sont différents.
import sys, os, math, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

_ici = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("tp", os.path.join(_ici, "..", "..", "..", "backend", "kaggle_tts", "texte_parle.py"))
_tp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_tp)
nfr = _tp.nombre_fr


def dn(x, d=2):
    s = fr(x, d).replace("−", "")
    if "," not in s:
        return nfr(int(s))
    e, dec = s.split(",")
    reste = dec.lstrip("0")
    return nfr(int(e)) + " virgule" + " zéro" * (len(dec) - len(reste)) + (" " + nfr(int(reste)) if reste else "")


def ds(x, ch=3):
    e = math.floor(math.log10(abs(x)))
    m = round(x / 10 ** e, ch - 1)
    if abs(m) >= 10:
        m /= 10; e += 1
    t = dn(m, ch - 1)
    return t if e == 0 else f"{t} fois dix puissance {'moins ' if e < 0 else ''}{nfr(abs(e))}"


SIMF = "/media/simulations/physics/radioactivite-tableau/figures.html"
SIML = "/media/simulations/physics/radioactivite-tableau/lambda.html"
SIMP = "/media/simulations/physics/radioactivite-tableau/pourcentages.html"
SIMA = "/media/simulations/physics/radioactivite-tableau/activite.html"
LN2 = 0.693
NA = 6.02e23


def calc(P):
    lF = LN2 / P["TF"]                     # min⁻¹
    lX = LN2 / P["TX"]
    lFs = LN2 / (P["TF"] * 60)             # s⁻¹
    NF0 = P["aF"] / lFs
    mF0 = NF0 / NA * P["MF"]
    te = math.log(P["aX"] / P["aF"]) / (lX - lF)
    mte = mF0 * math.exp(-lF * te)
    pX = (1 - math.exp(-lX * te)) * 100
    ratio = lF / lX
    return dict(lF=lF, lX=lX, lFs=lFs, NF0=NF0, mF0=mF0, te=te, mte=mte, pX=pX, ratio=ratio)


PA = dict(X="C", nomX="carbone 11", symX="¹¹₆C", TX=20.4, aX=6.0e9, TF=110.0, aF=1.5e9, MF=18)
PB = dict(X="Ga", nomX="gallium 68", symX="⁶⁸₃₁Ga", TX=68.0, aX=4.0e9, TF=110.0, aF=2.0e9, MF=18)
A = calc(PA)
B = calc(PB)


def figure(P, C):
    tmax = 120 if P["X"] == "C" else 300
    xpas = 10 if P["X"] == "C" else 25
    ymax = int(math.ceil(P["aX"] / 1e9)) + 1
    return {"type": "courbe", "titre": "Activités des deux sources en fonction du temps",
            "legende": "Les deux sources sont préparées à la même date t = 0.",
            "axes": {"x": {"min": 0, "max": tmax, "nom": "t", "unite": "min", "graduations": list(range(0, tmax + 1, xpas))},
                     "y": {"min": 0, "max": ymax, "nom": "a", "unite": "10⁹ Bq", "graduations": list(range(0, ymax + 1))}},
            "elements": [
                {"f": "courbe", "expr": f"{P['aF'] / 1e9}*exp(-{C['lF']:.6f}*x)", "de": 0, "a": tmax, "couleur": "orange",
                 "texte": "fluor 18", "texte_x": round(tmax * 0.8, 2), "pos": "n"},
                {"f": "courbe", "expr": f"{P['aX'] / 1e9}*exp(-{C['lX']:.6f}*x)", "de": 0, "a": tmax, "couleur": "cyan",
                 "texte": P["nomX"], "texte_x": round(tmax * 0.06, 2), "pos": "e"}]}


def intro(P):
    return (f"Un service d'imagerie médicale reçoit, à la date t = 0, deux sources radioactives émettrices β⁺ : une source de fluor 18 "
            f"(¹⁸₉F) d'activité a_F(0) = {sci(P['aF'], 2)} Bq, et une source de {P['nomX']} ({P['symX']}) d'activité "
            f"a_{P['X']}(0) = {sci(P['aX'], 2)} Bq. La figure représente l'évolution de leurs activités.")


def donnees(P):
    return [f"t½(¹⁸F) = {fr(P['TF'], 1)} min ; t½({P['nomX']}) = {fr(P['TX'], 1)} min", "ln 2 ≈ 0,693",
            "M(¹⁸F) = 18 g/mol ; N_A = 6,02 × 10²³ mol⁻¹", "1 min = 60 s"]


lFsS = sci(A["lFs"], 3)
lFS = f"{A['lF']:.4f}".replace(".", ",")
lCS = f"{A['lX']:.4f}".replace(".", ",")
te, mte, mF0, NF0 = A["te"], A["mte"], A["mF0"], A["NF0"]
DEMO = ("a_F(t) = a_F(0)·e^(−λ_F·t) et a_C(t) = a_C(0)·e^(−λ_C·t) ; à t_e : a_F(0)·e^(−λ_F·t_e) = a_C(0)·e^(−λ_C·t_e) ⇒ "
        "e^((λ_C − λ_F)·t_e) = a_C(0)/a_F(0) ⇒ (λ_C − λ_F)·t_e = ln(a_C(0)/a_F(0)) ⇒ t_e = ln(a_C(0)/a_F(0))/(λ_C − λ_F)")
Q = []
Q.append({"id": "1", "texte": "Calculer, en s⁻¹, la constante radioactive λ_F du fluor 18, puis le nombre N_F(0) de noyaux de fluor 18 présents à t = 0.",
  "texte_dit": "السؤال un: حسب la constante radioactive lambda F ديال le fluor dix-huit، ب seconde puissance moins un، ومن بعد le nombre N F de zéro ديال les noyaux de fluor فt égale zéro.",
  "reponse": valeur("N_F(0)", NF0, "noyaux", f"λ_F = (ln 2)/t½ = 0,693/(110 × 60) ≈ {lFsS} s⁻¹ ; N_F(0) = a_F(0)/λ_F = 1,5 × 10⁹/{lFsS} ≈ {sci(NF0, 3)} noyaux"),
  "clavier": {"aides": ["λ = (ln 2)/t½", "t½ en s", "a = λ·N", "N₀ = a₀/λ", "noyaux"], "pieges": ["λ en min⁻¹", "N₀ = a₀·λ"]},
  "aides": [aide("L'activité est en becquerels, des désintégrations par SECONDE : λ doit être en s⁻¹. Convertis d'abord t½.",
                 "l'activité بالبيكريل، يعني désintégrations par seconde. إذن lambda خاصها ب seconde puissance moins un. حول t un demi للثواني الأول."),
            aide("λ_F = (ln 2)/t½ avec t½ = 110 × 60 s ; puis a = λ·N donne N_F(0) = a_F(0)/λ_F.",
                 "lambda F égale ln deux sur t un demi، و t un demi égale cent dix fois soixante secondes. ومن بعد a égale lambda N، إذن N F de zéro égale a F de zéro sur lambda F.")],
  "correction": correction([("1 : t½ = 110 × 60 = 6600 s ; λ_F = (ln 2)/t½ = 0,693/6600", "égale six mille six cents secondes"),
                            (f"λ_F ≈ {lFsS} s⁻¹", "égale environ " + ds(A["lFs"]) + " seconde puissance moins un"),
                            (f"a = λ·N ⇒ N_F(0) = a_F(0)/λ_F = 1,5 × 10⁹/{lFsS}", "N F de zéro égale a F de zéro sur lambda F"),
                            (f"N_F(0) ≈ {sci(NF0, 3)} noyaux", "environ " + ds(NF0) + " noyaux")],
       "السؤال un. l'activité بالبيكريل، إذن lambda ب seconde puissance moins un. t un demi égale cent dix fois soixante، égale six mille six cents secondes. lambda F égale ln deux sur t un demi، égale environ " + ds(A["lFs"]) + " seconde puissance moins un. a égale lambda N، إذن N F de zéro égale a F de zéro sur lambda F، égale un virgule cinq fois dix puissance neuf، sur " + ds(A["lFs"]) + ". N F de zéro égale environ " + ds(NF0) + " noyaux."),
  "explication": "ex_q1", "facile": "fa_q1"})
Q.append({"id": "2", "texte": "Les deux activités deviennent égales à une date t_e. Montrer que : t_e = ln(a_C(0)/a_F(0))/(λ_C − λ_F).",
  "texte_dit": "السؤال deux: les deux activités كيوليو متساويين فواحد la date t e. بين بلي t e égale ln de a C de zéro sur a F de zéro، sur lambda C moins lambda F.",
  "reponse": phrase(DEMO),
  "clavier": {"aides": ["a(t) = a₀·e^(−λt)", "eᵃ/eᵇ = e^(a − b)", "ln(eˣ) = x"], "pieges": ["ln(a·b) = ln a · ln b", "t_e = ln(a_C(0)/a_F(0))/(λ_C + λ_F)"]},
  "aides": [aide("Écris la loi de l'activité pour chaque source, puis l'égalité a_F(t_e) = a_C(t_e).",
                 "كتب la loi ديال l'activité لكل source، ومن بعد l'égalité: a F de t e égale a C de t e."),
            aide("Regroupe les exponentielles d'un côté et les activités initiales de l'autre, puis prends ln.",
                 "جمع les exponentielles فجهة، و les activités initiales فجهة أخرى، ومن بعد دير ln.")],
  "correction": correction([("2 : a_F(t) = a_F(0)·e^(−λ_F·t) ; a_C(t) = a_C(0)·e^(−λ_C·t)", "la loi لكل source"),
                            ("à t_e : a_F(0)·e^(−λ_F·t_e) = a_C(0)·e^(−λ_C·t_e)", "a F de t e égale a C de t e"),
                            ("e^((λ_C − λ_F)·t_e) = a_C(0)/a_F(0) ⇒ (λ_C − λ_F)·t_e = ln(a_C(0)/a_F(0))", "كنديرو ln"),
                            ("t_e = ln(a_C(0)/a_F(0))/(λ_C − λ_F)", "t e égale ln de a C de zéro sur a F de zéro")],
       "السؤال deux. la loi لكل source: a F de t égale a F de zéro exponentielle moins lambda F t، و a C de t égale a C de zéro exponentielle moins lambda C t. فt e: a F de t e égale a C de t e. كنجمعو: exponentielle de lambda C moins lambda F، fois t e، égale a C de zéro sur a F de zéro. كنديرو ln: lambda C moins lambda F، fois t e، égale ln de a C de zéro sur a F de zéro. إذن t e égale ln de a C de zéro sur a F de zéro، sur lambda C moins lambda F."),
  "explication": "ex_q2", "facile": "fa_q2"})
Q.append({"id": "3", "texte": "Calculer t_e en minutes. Vérifier sur la figure.",
  "texte_dit": "السؤال trois: حسب t e بالدقايق، وتأكد على la figure.",
  "reponse": valeur("t_e", te, "min", f"t_e = ln(6,0/1,5)/({lCS} − {lFS}) ≈ {fr(te, 1)} min"),
  "clavier": {"aides": ["λ = (ln 2)/t½ en min⁻¹", "ln 4", "A.N. : ln(6,0/1,5)/(0,0340 − 0,0063)", "min"], "pieges": ["λ_C + λ_F", "ln(1,5/6,0)", "λ en s⁻¹ avec t en min"]},
  "aides": [aide("Pour avoir t_e en minutes, prends λ_C et λ_F en min⁻¹ (t½ en minutes).",
                 "باش t e تخرج بالدقايق، خود lambda C و lambda F ب minute puissance moins un، يعني t un demi بالدقايق."),
            aide("λ_C = 0,693/20,4 et λ_F = 0,693/110 ; le rapport des activités initiales vaut 4.",
                 "lambda C égale zéro virgule six cent quatre-vingt-treize sur vingt virgule quatre، و lambda F égale zéro virgule six cent quatre-vingt-treize sur cent dix. le rapport des activités initiales égale quatre.")],
  "correction": correction([(f"3 : λ_C = 0,693/20,4 ≈ {lCS} min⁻¹ ; λ_F = 0,693/110 ≈ {lFS} min⁻¹", "lambda C égale environ"),
                            (f"t_e = ln(6,0/1,5)/({lCS} − {lFS}) = ln 4/{fr(A['lX'] - A['lF'], 4)}", "t e égale ln quatre"),
                            (f"t_e ≈ {fr(te, 1)} min ; sur la figure, les deux courbes se coupent vers 50 min", "t e égale environ " + dn(te, 1) + " minutes")],
       "السؤال trois. lambda C égale environ " + dn(A["lX"], 4) + " minute puissance moins un، و lambda F égale environ " + dn(A["lF"], 4) + " minute puissance moins un. t e égale ln quatre، sur " + dn(A["lX"] - A["lF"], 4) + ". t e égale environ " + dn(te, 1) + " minutes. على la figure، les deux courbes كيتلاقاو تقريبا à cinquante minutes."),
  "explication": "ex_q3", "facile": "fa_q3"})
Q.append({"id": "4", "texte": "Calculer la masse m_F de fluor 18 restant dans la source à la date t_e.",
  "texte_dit": "السؤال quatre: حسب la masse m F ديال le fluor dix-huit اللي باقية فla source، فla date t e.",
  "reponse": valeur("m_F(t_e)", mte, "g", f"m_F(0) = N_F(0)·M/N_A ≈ {sci(mF0, 3)} g ; m_F(t_e) = m_F(0)·e^(−λ_F·t_e) ≈ {sci(mte, 3)} g"),
  "clavier": {"aides": ["m = (N/N_A)·M", "m(t) = m₀·e^(−λt)", "λ_F en min⁻¹ avec t_e en min", "g"], "pieges": ["m = N·N_A/M", "m(t) = m₀ − λt"]},
  "aides": [aide("Commence par la masse initiale : m = (N/N_A)·M avec N_F(0) de la question 1.",
                 "بدا ب la masse initiale: m égale N sur N A fois M، ب N F de zéro ديال السؤال un."),
            aide("La masse suit la même loi que N : m(t) = m₀·e^(−λt) (λ et t dans la même unité de temps).",
                 "la masse كتبع نفس la loi ديال N: m de t égale m zéro exponentielle moins lambda t. lambda و t بنفس l'unité ديال الوقت.")],
  "correction": correction([(f"4 : m_F(0) = (N_F(0)/N_A)·M = ({sci(NF0, 3)}/6,02 × 10²³) × 18 ≈ {sci(mF0, 3)} g", "m F de zéro égale N F de zéro sur N A fois M"),
                            ("m_F(t) = m_F(0)·e^(−λ_F·t)", "m F de t égale m F de zéro exponentielle moins lambda F t"),
                            (f"A.N. : m_F(t_e) = {sci(mF0, 3)} × e^(−{lFS} × {fr(te, 1)}) ≈ {sci(mte, 3)} g", "environ " + ds(mte) + " gramme")],
       "السؤال quatre. الأول la masse initiale: m F de zéro égale N F de zéro sur N A fois M، égale environ " + ds(mF0) + " gramme. la masse كتبع نفس la loi: m F de t égale m F de zéro exponentielle moins lambda F t. l'application numérique: فt e، m F égale environ " + ds(mte) + " gramme."),
  "explication": "ex_q4", "facile": "fa_q4"})
Q.append({"id": "5", "texte": "Calculer le pourcentage des noyaux de carbone 11 initialement présents qui se sont désintégrés à la date t_e.",
  "texte_dit": "السؤال cinq: حسب le pourcentage ديال les noyaux de carbone onze اللي تفككو، فla date t e.",
  "reponse": valeur("p", A["pX"], "%", f"p = N_d/N₀ = 1 − e^(−λ_C·t_e) = 1 − e^(−{lCS} × {fr(te, 1)}) ≈ {fr(A['pX'], 1)} %"),
  "clavier": {"aides": ["N_d = N₀ − N(t)", "N/N₀ = e^(−λt)", "p = 1 − e^(−λt)", "%"], "pieges": ["p = e^(−λt)", "p = λ·t"]},
  "aides": [aide("Attention au mot « désintégrés » : la loi donne d'abord la fraction qui RESTE, N/N₀ = e^(−λt).",
                 "رد البال ل la question: كتسول على les désintégrés. la loi كتعطي الأول اللي باقي: N sur N zéro égale exponentielle moins lambda t."),
            aide("Fraction désintégrée = 1 − N/N₀ = 1 − e^(−λ_C·t_e).", "اللي تفكك égale un moins N sur N zéro، égale un moins exponentielle moins lambda C t e.")],
  "correction": correction([("5 : N/N₀ = e^(−λ_C·t_e) reste ; p = (N₀ − N)/N₀ = 1 − e^(−λ_C·t_e)", "p égale un moins exponentielle moins lambda C t e"),
                            (f"A.N. : p = 1 − e^(−{lCS} × {fr(te, 1)}) = 1 − {fr(1 - A['pX'] / 100, 3)}", "un moins zéro virgule"),
                            (f"p ≈ {fr(A['pX'], 1)} % des noyaux de carbone 11 se sont désintégrés", "environ " + dn(A["pX"], 1) + " pour cent")],
       "السؤال cinq. اللي باقي: N sur N zéro égale exponentielle moins lambda C t e. اللي تفكك: p égale un moins exponentielle moins lambda C t e. l'application numérique: un moins " + dn(1 - A["pX"] / 100, 3) + ". p égale environ " + dn(A["pX"], 1) + " pour cent."),
  "explication": "ex_q5", "facile": "fa_q5"})
Q.append({"id": "6", "texte": "Un technicien affirme : « à la date t_e, les deux sources contiennent le même nombre de noyaux radioactifs ». Calculer le rapport N_C(t_e)/N_F(t_e) et conclure.",
  "texte_dit": "السؤال six: واحد le technicien كيقول: فla date t e، les deux sources فيهم نفس العدد ديال les noyaux radioactifs. حسب le rapport N C de t e sur N F de t e، وقول واش عندو الحق.",
  "reponse": valeur("N_C/N_F", A["ratio"], "", f"a = λ·N et a_C(t_e) = a_F(t_e) ⇒ N_C/N_F = λ_F/λ_C = t½(C)/t½(F) = 20,4/110 ≈ {fr(A['ratio'], 3)}"),
  "clavier": {"aides": ["a = λ·N", "λ_F/λ_C", "t½(C)/t½(F)"], "pieges": ["N_C/N_F = 1", "N_C/N_F = λ_C/λ_F"]},
  "aides": [aide("À t_e, les ACTIVITÉS sont égales. Quelle relation relie l'activité au nombre de noyaux ?",
                 "فt e، les activités هوما اللي متساويين. شنو la relation بين l'activité و le nombre de noyaux؟"),
            aide("a = λ·N : λ_C·N_C = λ_F·N_F, donc N_C/N_F = λ_F/λ_C = t½(C)/t½(F).",
                 "a égale lambda N. إذن lambda C N C égale lambda F N F، و N C sur N F égale lambda F sur lambda C، يعني t un demi de C sur t un demi de F.")],
  "correction": correction([("6 : a = λ·N ; à t_e : λ_C·N_C = λ_F·N_F", "lambda C N C égale lambda F N F"),
                            (f"N_C/N_F = λ_F/λ_C = t½(C)/t½(F) = 20,4/110 ≈ {fr(A['ratio'], 3)}", "N C sur N F égale lambda F sur lambda C"),
                            ("N_C ≈ 0,19·N_F : la source de fluor contient environ 5 fois plus de noyaux ; l'affirmation est fausse", "l'affirmation fausse")],
       "السؤال six. a égale lambda N. فt e، lambda C N C égale lambda F N F. إذن N C sur N F égale lambda F sur lambda C، égale vingt virgule quatre sur cent dix، égale environ " + dn(A["ratio"], 3) + ". la source de fluor فيها environ cinq fois plus de noyaux: l'affirmation fausse. نفس l'activité ماشي نفس العدد ديال les noyaux."),
  "explication": "ex_q6", "facile": "fa_q6"})

EXP = [
  diapo_sim("ex_q1", "Question 1 : λ en s⁻¹, puis N₀ = a₀/λ", "a en Bq (par seconde) : t½ en secondes, λ en s⁻¹, puis N₀ = a₀/λ.",
    SIMF + "?fig=fig_unites", "λ et t½ : la même unité de temps",
    "رد البال، le becquerel، هو par seconde. إذن باش a égale lambda N، lambda خاصها تكون ب seconde puissance moins un. فالدرس، le polonium deux cent dix: t un demi égale cent trente-huit jours، كنحولوها للثواني: c'est un virgule dix-neuf fois dix puissance sept secondes. فالتمرين، t un demi égale cent dix minutes، c'est six mille six cents secondes. lambda F égale ln deux sur t un demi، égale environ " + ds(A["lFs"]) + " seconde puissance moins un. ومن بعد N F de zéro égale a F de zéro sur lambda F، égale environ " + ds(NF0) + " noyaux.",
    [("λ_F = 0,693/6600 s", "lambda F égale ln deux sur t un demi"), (f"N_F(0) = a_F(0)/λ_F ≈ {sci(NF0, 3)}", "N F de zéro égale a F de zéro sur lambda F")],
    [dict(mot="رد البال، le becquerel", commande="play_until", parametres={"moment": "trace"}),
     dict(mot="فالدرس، le polonium", commande="play_until", parametres={"moment": "conversion"}),
     dict(mot="فالتمرين، t un demi", commande="play_until", parametres={"moment": "bq"}),
     dict(mot="lambda F égale ln deux sur t un demi", cible="centre:0"),
     dict(mot="N F de zéro égale a F de zéro sur lambda F", cible="centre:1")]),
  diapo_sim("ex_q2", "Question 2 : établir la date t_e", "Les mêmes gestes que pour dater : diviser, prendre ln, isoler t.",
    SIMF + "?fig=fig_datation_demo", "Diviser, prendre ln, isoler t",
    "فالدرس، باش نحسبو la date، كنبداو من la loi: a égale a zéro exponentielle moins lambda t. كنقسمو باش تبقى exponentielle بوحدها. كنديرو ln، حيت ln كيحيد e. وكنعزلو t. فالتمرين، نفس الخطوات ولكن ب les deux sources. a F de t e égale a C de t e. كنجمعو les exponentielles: exponentielle de lambda C moins lambda F، fois t e، égale a C de zéro sur a F de zéro. كنديرو ln، وكنعزلو t e: t e égale ln de a C de zéro sur a F de zéro، sur lambda C moins lambda F.",
    [("e^((λ_C − λ_F)·t_e) = a_C(0)/a_F(0)", "كنجمعو les exponentielles"), ("t_e = ln(a_C(0)/a_F(0))/(λ_C − λ_F)", "t e égale ln de a C de zéro sur a F de zéro")],
    [dict(mot="كنبداو من la loi", commande="play_until", parametres={"moment": "loi"}),
     dict(mot="كنقسمو باش", commande="play_until", parametres={"moment": "rapport"}),
     dict(mot="كنديرو ln، حيت", commande="play_until", parametres={"moment": "ln"}),
     dict(mot="وكنعزلو t.", commande="play_until", parametres={"moment": "resultat"}),
     dict(mot="كنجمعو les exponentielles", cible="centre:0"),
     dict(mot="t e égale ln de a C de zéro sur a F de zéro", cible="centre:1")]),
  diapo_sim("ex_q3", "Question 3 : celle qui a la plus grande λ descend plus vite", "λ_C > λ_F : le carbone 11 part plus haut mais descend plus vite ; les courbes se croisent.",
    SIML, "Deux échantillons, deux λ",
    "شوف les deux échantillons ديال الدرس: l'iode عندو lambda كبيرة، و le carbone quatorze عندو lambda صغيرة بزاف. ملي كيدوز الوقت، l'iode كيخوا بالزربة، و le carbone ما كيتحركش. فالتمرين، le carbone onze عندو t un demi صغيرة، إذن lambda كبيرة: l'activité ديالو كتبدا كبيرة ولكن كتهبط بالزربة، وكتلقى l'activité ديال le fluor. lambda C égale environ " + dn(A["lX"], 4) + "، و lambda F égale environ " + dn(A["lF"], 4) + " minute puissance moins un. t e égale ln quatre، sur " + dn(A["lX"] - A["lF"], 4) + "، égale environ " + dn(te, 1) + " minutes.",
    [("λ_C > λ_F : a_C diminue plus vite", "lambda كبيرة: l'activité ديالو"), (f"t_e = ln 4/{fr(A['lX'] - A['lF'], 4)} ≈ {fr(te, 1)} min", "égale environ " + dn(te, 1) + " minutes")],
    [dict(mot="شوف les deux échantillons", commande="play_until", parametres={"moment": "trace"}),
     dict(mot="ملي كيدوز الوقت", commande="play_until", parametres={"moment": "course"}),
     dict(mot="ملي كيدوز الوقت", repere="conclusion"),
     dict(mot="lambda كبيرة: l'activité ديالو", cible="centre:0"),
     dict(mot="égale environ " + dn(te, 1) + " minutes", cible="centre:1")]),
  diapo_sim("ex_q4", "Question 4 : la masse restante", "m = (N/N_A)·M, et la masse suit la même loi que N : m(t) = m₀·e^(−λt).",
    SIMF + "?fig=fig_masse_N&depart=quantite", "Du nombre de noyaux à la masse",
    "دابا الطريق المقلوب: عندنا العدد ديال les noyaux، وخاصنا la masse. n égale N sur N A، و m égale n fois M. إذن m égale N sur N A fois M، و m ب gramme. و la masse كتبع نفس la loi ديال N: m de t égale m zéro exponentielle moins lambda t. فالتمرين، m F de zéro égale environ " + ds(mF0) + " gramme. فt e، m F égale environ " + ds(mte) + " gramme.",
    [("m = (N/N_A)·M", "إذن m égale N sur N A fois M"), ("m(t) = m₀·e^(−λt)", "m de t égale m zéro exponentielle moins lambda t"), (f"m_F(t_e) ≈ {sci(mte, 3)} g", "m F égale environ " + ds(mte) + " gramme")],
    [dict(mot="دابا الطريق المقلوب", commande="play_until", parametres={"moment": "nombre"}),
     dict(mot="إذن m égale N sur N A fois M", cible="centre:0"),
     dict(mot="و la masse كتبع", commande="play_until", parametres={"moment": "fin"}),
     dict(mot="m de t égale m zéro exponentielle moins lambda t", cible="centre:1"),
     dict(mot="m F égale environ " + ds(mte) + " gramme", cible="centre:2")]),
  diapo_sim("ex_q5", "Question 5 : désintégrés, pas restants", "La loi donne les restants ; désintégrés = 1 − restants.",
    SIMP, "Restants et désintégrés",
    "piège معروف فالامتحان الوطني: كيسولوك على les désintégrés، و la loi كتهضر على les restants. trente pour cent désintégrés: il reste soixante-dix pour cent. quatre-vingt-dix pour cent désintégrés: il reste dix pour cent. فالتمرين، la loi كتعطي اللي باقي: exponentielle moins lambda C t e، égale environ " + dn(1 - A["pX"] / 100, 3) + ". إذن اللي تفكك: p égale un moins " + dn(1 - A["pX"] / 100, 3) + "، égale environ " + dn(A["pX"], 1) + " pour cent.",
    [("restants : N/N₀ = e^(−λt)", "la loi كتعطي اللي باقي"), (f"p = 1 − e^(−λ_C·t_e) ≈ {fr(A['pX'], 1)} %", "إذن اللي تفكك")],
    [dict(mot="piège معروف", repere="echantillon"),
     dict(mot="trente pour cent désintégrés", commande="play_until", parametres={"moment": "trente"}),
     dict(mot="quatre-vingt-dix pour cent désintégrés", commande="play_until", parametres={"moment": "quatre_vingt_dix"}),
     dict(mot="la loi كتعطي اللي باقي", cible="centre:0"),
     dict(mot="إذن اللي تفكك", cible="centre:1")]),
  diapo_sim("ex_q6", "Question 6 : même activité ne veut pas dire même nombre de noyaux", "a = λ·N : à activités égales, la source de plus grande λ contient moins de noyaux.",
    SIMA + "?depart=une_seconde", "Le compteur compte les désintégrations par seconde",
    "le compteur كيحسب les désintégrations ف la seconde: هي l'activité. فالدرس، c'est quatre cents becquerels. ومن بعد ما كيدوز الوقت، les noyaux قلو، و l'activité قلات: a égale lambda N. l'activité كتبع N ولكن حتى lambda. فالتمرين، فt e، l'activité ديال les deux sources كيف كيف: lambda C N C égale lambda F N F. إذن N C sur N F égale lambda F sur lambda C، égale environ " + dn(A["ratio"], 3) + ". l'affirmation ديال le technicien fausse.",
    [("a = λ·N", "a égale lambda N"), (f"N_C/N_F = λ_F/λ_C ≈ {fr(A['ratio'], 3)}", "إذن N C sur N F égale lambda F sur lambda C")],
    [dict(mot="le compteur كيحسب", commande="play_until", parametres={"moment": "definition"}),
     dict(mot="ومن بعد ما كيدوز الوقت", commande="play_until", parametres={"moment": "proportionnelle"}),
     dict(mot="a égale lambda N", cible="centre:0"),
     dict(mot="إذن N C sur N F égale lambda F sur lambda C", cible="centre:1")]),
]

FAC = [
  qcm_facile("fa_q1", "Plus facile : l'unité de λ dans a = λ·N", "نتمرنو بسؤال ساهل: شنو l'unité ديال lambda؟",
    "On veut N₀ = a₀/λ avec a₀ en Bq. t½ = 110 min. Quelle valeur de λ faut-il utiliser ?",
    ["λ = 0,693/110 min⁻¹", "λ = 0,693/(110 × 60) s⁻¹", "λ = 110/0,693 s"], 1, {
      "1": {"juste": rep("برافو! le becquerel par seconde، إذن t un demi بالثواني، و lambda ب seconde puissance moins un.", "Juste : Bq = s⁻¹, donc λ = 0,693/6600 s⁻¹.")},
      "0": {"1": rep("قريب، ولكن le becquerel هو par seconde، ماشي par minute. عاود اختار.", "Le becquerel est « par seconde », pas « par minute ». Réessaie."),
            "2": rep("الجواب: lambda égale zéro virgule six cent quatre-vingt-treize sur cent dix fois soixante، ب seconde puissance moins un.", "Réponse : λ = 0,693/(110 × 60) s⁻¹, car a est en Bq.")},
      "2": {"1": rep("هادي t un demi sur ln deux: هي tau، durée، ماشي lambda. عاود اختار.", "t½/ln 2 est τ, une durée, pas λ. Réessaie."),
            "2": rep("الجواب: lambda égale ln deux sur t un demi، و t un demi بالثواني.", "Réponse : λ = (ln 2)/t½ avec t½ en secondes.")}},
    "On veut N zéro égale a zéro sur lambda, avec a zéro en becquerel. t un demi égale cent dix minutes. Quelle valeur de lambda faut-il utiliser ?"),
  vf_facile("fa_q2", "Plus facile : les gestes de la démonstration", "سؤال ساهل: قول واش صحيحة ولا غالطة.", "a_F(0)·e^(−λ_F·t_e) = a_C(0)·e^(−λ_C·t_e).", [
      ("En divisant, on obtient e^((λ_C − λ_F)·t_e) = a_C(0)/a_F(0).", True, "e^(−λ_F·t_e)/e^(−λ_C·t_e) = e^((λ_C − λ_F)·t_e)."),
      ("ln(a_C(0)·e^(−λ_C·t_e)) = ln a_C(0) · ln e^(−λ_C·t_e).", False, "ln d'un produit est une SOMME : ln(a·b) = ln a + ln b."),
      ("Après ln : (λ_C − λ_F)·t_e = ln(a_C(0)/a_F(0)).", True, "ln enlève e, puis on isole t_e.")]),
  qcm_facile("fa_q3", "Plus facile : qui descend le plus vite ?", "سؤال ساهل: شكون كيهبط بالزربة؟",
    "t½(¹¹C) = 20,4 min et t½(¹⁸F) = 110 min. Au début, a_C > a_F. Que se passe-t-il ?",
    ["a_C reste toujours plus grande que a_F", "a_C diminue plus vite et devient égale à a_F, puis plus petite", "les deux activités diminuent à la même vitesse"], 1, {
      "1": {"juste": rep("مزيان! le carbone onze عندو t un demi صغيرة، يعني lambda كبيرة: كيهبط بالزربة، وكيلقى le fluor.", "Juste : petite t½, grande λ : a_C chute plus vite et croise a_F.")},
      "0": {"1": rep("شوف t un demi ديال le carbone: صغيرة بزاف. واش كيهبط بشوية ولا بالزربة؟ عاود اختار.", "La t½ du carbone 11 est petite : décroît-il lentement ou vite ? Réessaie."),
            "2": rep("الجواب: a C كتهبط بالزربة، وكتولي كيف a F، ومن بعد صغر منها.", "Réponse : a_C diminue plus vite, égale a_F à t_e, puis devient plus petite.")},
      "2": {"1": rep("عندهم t un demi مختلفة، إذن lambda مختلفة. عاود اختار.", "Leurs t½ sont différentes, donc leurs λ aussi. Réessaie."),
            "2": rep("الجواب: a C كتهبط بالزربة، حيت lambda C كبر من lambda F.", "Réponse : a_C diminue plus vite car λ_C > λ_F.")}},
    "t un demi du carbone onze égale vingt virgule quatre minutes, et celle du fluor dix-huit, cent dix minutes. Au début, a C est plus grande que a F. Que se passe-t-il ?"),
  assoc_facile("fa_q4", "Plus facile : de N à la masse", "سؤال ساهل: ربط كل grandeur مع la relation ديالها.",
    "Fluor 18 : M = 18 g/mol.", "Relie chaque grandeur à la relation qui la donne.",
    [("1", "le nombre de noyaux N₀"), ("2", "la masse initiale m₀"), ("3", "la masse à la date t")],
    [("a", "N₀ = a₀/λ"), ("b", "m₀ = (N₀/N_A)·M"), ("c", "m(t) = m₀·e^(−λt)")],
    {"1": "a", "2": "b", "3": "c"}, {
      "1-a": (True, "Juste : a = λ·N donne N₀ = a₀/λ (λ en s⁻¹).", "صحيح: a égale lambda N، إذن N zéro égale a zéro sur lambda."),
      "1-b": (False, "Non : cette relation donne une masse, en grammes.", "لا: هاد la relation كتعطي masse بالغرام."),
      "1-c": (False, "Non : cette relation donne une masse à la date t.", "لا: هادي كتعطي la masse فla date t."),
      "2-a": (False, "Non : a₀/λ est un nombre de noyaux, pas une masse.", "لا: a zéro sur lambda هو عدد ديال les noyaux، ماشي masse."),
      "2-b": (True, "Juste : n = N/N_A, puis m = n·M.", "صحيح: n égale N sur N A، و m égale n fois M."),
      "2-c": (False, "Non : c'est la masse à une date t, pas au départ.", "لا: هادي la masse فla date t، ماشي فالبداية."),
      "3-a": (False, "Non : a₀/λ est le nombre de noyaux au départ.", "لا: a zéro sur lambda هو العدد فالبداية."),
      "3-b": (False, "Non : m₀ est la masse au départ ; elle diminue ensuite.", "لا: m zéro هي la masse فالبداية، ومن بعد كتنقص."),
      "3-c": (True, "Juste : la masse suit la même loi que N.", "صحيح: la masse كتبع نفس la loi ديال N.")},
    ("(1 ; a) (2 ; b) (3 ; c) : N₀ → m₀ → m(t).", "N zéro، من بعد m zéro، من بعد m de t.")),
  qcm_facile("fa_q5", "Plus facile : restants ou désintégrés ?", "سؤال ساهل: رد البال ل les désintégrés.",
    "À t_e, e^(−λ_C·t_e) ≈ 0,18. Le pourcentage de noyaux de carbone 11 désintégrés est…",
    ["18 %", "82 %", "50 %"], 1, {
      "1": {"juste": rep("برافو! zéro virgule dix-huit هو اللي باقي. اللي تفكك: p égale un moins zéro virgule dix-huit، c'est quatre-vingt-deux pour cent.", "Juste : il reste 18 %, donc 82 % se sont désintégrés.")},
      "0": {"1": rep("exponentielle moins lambda t كتعطي اللي باقي، ماشي اللي تفكك. عاود اختار.", "e^(−λt) donne la fraction qui RESTE. Réessaie."),
            "2": rep("الجواب: p égale quatre-vingt-deux pour cent. dix-huit pour cent هوما اللي باقيين.", "Réponse : 82 % désintégrés ; 18 % restent.")},
      "2": {"1": rep("cinquante pour cent هي غير فt un demi. هنا t e كبر بزاف من t un demi ديال le carbone. عاود اختار.", "50 % correspond à t½ ; ici t_e est bien plus grand que t½(C). Réessaie."),
            "2": rep("الجواب: p égale quatre-vingt-deux pour cent، حيت p égale un moins zéro virgule dix-huit.", "Réponse : 1 − 0,18 = 0,82, soit 82 %.")}},
    "À t e, exponentielle moins lambda C t e vaut environ zéro virgule dix-huit. Le pourcentage de noyaux de carbone onze désintégrés est ?"),
  vf_facile("fa_q6", "Plus facile : activité et nombre de noyaux", "سؤال ساهل: قول واش صحيحة ولا غالطة.", "a = λ·N.", [
      ("Deux sources de même activité contiennent toujours le même nombre de noyaux.", False, "a = λ·N : si les λ sont différentes, les N le sont aussi."),
      ("À activité égale, la source de plus grande λ contient moins de noyaux.", True, "N = a/λ : plus λ est grande, plus N est petit."),
      ("À t_e, N_C/N_F = λ_F/λ_C.", True, "λ_C·N_C = λ_F·N_F donne N_C/N_F = λ_F/λ_C.")]),
]


def qb():
    P, C = PB, B
    lG = f"{C['lX']:.4f}".replace(".", ",")
    lF = f"{C['lF']:.4f}".replace(".", ",")
    lFs = sci(C["lFs"], 3)
    return [
      {"id": "1", "texte": "Calculer, en s⁻¹, la constante radioactive λ_F du fluor 18, puis le nombre N_F(0) de noyaux de fluor 18 à t = 0.",
       "reponse": valeur("N_F(0)", C["NF0"], "noyaux", f"λ_F = 0,693/6600 ≈ {lFs} s⁻¹ ; N_F(0) = a_F(0)/λ_F = 2,0 × 10⁹/{lFs} ≈ {sci(C['NF0'], 3)} noyaux"),
       "clavier": Q[0]["clavier"],
       "correction": correction([(f"1 : λ_F = (ln 2)/t½ = 0,693/6600 ≈ {lFs} s⁻¹", "lambda F égale ln deux sur t un demi"),
                                 (f"N_F(0) = a_F(0)/λ_F ≈ {sci(C['NF0'], 3)} noyaux", "N F de zéro égale a F de zéro sur lambda F")],
            "lambda F égale ln deux sur t un demi، égale environ " + ds(C["lFs"]) + " seconde puissance moins un. N F de zéro égale a F de zéro sur lambda F، égale environ " + ds(C["NF0"]) + " noyaux.")},
      {"id": "2", "texte": "Les deux activités deviennent égales à une date t_e. Montrer que : t_e = ln(a_Ga(0)/a_F(0))/(λ_Ga − λ_F).",
       "reponse": phrase(DEMO.replace("a_C", "a_Ga").replace("λ_C", "λ_Ga")), "clavier": Q[1]["clavier"],
       "correction": correction([("2 : a_F(0)·e^(−λ_F·t_e) = a_Ga(0)·e^(−λ_Ga·t_e)", "a F de t e égale a Ga de t e"),
                                 ("t_e = ln(a_Ga(0)/a_F(0))/(λ_Ga − λ_F)", "t e égale ln de a Ga de zéro sur a F de zéro")],
            "a F de t e égale a Ga de t e. كنجمعو les exponentielles وكنديرو ln: t e égale ln de a Ga de zéro sur a F de zéro، sur lambda Ga moins lambda F.")},
      {"id": "3", "texte": "Calculer t_e en minutes. Vérifier sur la figure.",
       "reponse": valeur("t_e", C["te"], "min", f"t_e = ln(4,0/2,0)/({lG} − {lF}) ≈ {fr(C['te'], 1)} min"),
       "clavier": {"aides": ["λ en min⁻¹", "ln 2", "min"], "pieges": ["λ_Ga + λ_F"]},
       "correction": correction([(f"3 : λ_Ga ≈ {lG} min⁻¹ ; λ_F ≈ {lF} min⁻¹", "lambda Ga"), (f"t_e = ln 2/({lG} − {lF}) ≈ {fr(C['te'], 1)} min", "t e égale environ " + dn(C["te"], 1) + " minutes")],
            "lambda Ga égale environ " + dn(C["lX"], 4) + "، و lambda F égale environ " + dn(C["lF"], 4) + " minute puissance moins un. t e égale environ " + dn(C["te"], 1) + " minutes.")},
      {"id": "4", "texte": "Calculer la masse m_F de fluor 18 restant dans la source à la date t_e.",
       "reponse": valeur("m_F(t_e)", C["mte"], "g", f"m_F(0) ≈ {sci(C['mF0'], 3)} g ; m_F(t_e) = m_F(0)·e^(−λ_F·t_e) ≈ {sci(C['mte'], 3)} g"),
       "clavier": Q[3]["clavier"],
       "correction": correction([(f"4 : m_F(0) = (N_F(0)/N_A)·M ≈ {sci(C['mF0'], 3)} g", "m F de zéro"), (f"m_F(t_e) = m_F(0)·e^(−λ_F·t_e) ≈ {sci(C['mte'], 3)} g", "environ " + ds(C["mte"]) + " gramme")],
            "m F de zéro égale N F de zéro sur N A fois M، égale environ " + ds(C["mF0"]) + " gramme. فt e، m F égale environ " + ds(C["mte"]) + " gramme.")},
      {"id": "5", "texte": "Calculer le pourcentage des noyaux de gallium 68 initialement présents qui se sont désintégrés à la date t_e.",
       "reponse": valeur("p", C["pX"], "%", f"p = 1 − e^(−λ_Ga·t_e) = 1 − e^(−{lG} × {fr(C['te'], 1)}) ≈ {fr(C['pX'], 1)} %"),
       "clavier": Q[4]["clavier"],
       "correction": correction([("5 : p = 1 − e^(−λ_Ga·t_e)", "p égale un moins exponentielle"), (f"p ≈ {fr(C['pX'], 1)} %", "environ " + dn(C["pX"], 1) + " pour cent")],
            "p égale un moins exponentielle moins lambda Ga t e، égale environ " + dn(C["pX"], 1) + " pour cent.")},
      {"id": "6", "texte": "Un technicien affirme : « à la date t_e, les deux sources contiennent le même nombre de noyaux radioactifs ». Calculer N_Ga(t_e)/N_F(t_e) et conclure.",
       "reponse": valeur("N_Ga/N_F", C["ratio"], "", f"N_Ga/N_F = λ_F/λ_Ga = t½(Ga)/t½(F) = 68/110 ≈ {fr(C['ratio'], 3)}"),
       "clavier": {"aides": ["a = λ·N", "λ_F/λ_Ga"], "pieges": ["N_Ga/N_F = 1"]},
       "correction": correction([("6 : a = λ·N ; à t_e : λ_Ga·N_Ga = λ_F·N_F", "lambda Ga N Ga égale lambda F N F"),
                                 (f"N_Ga/N_F = λ_F/λ_Ga = 68/110 ≈ {fr(C['ratio'], 3)} : l'affirmation est fausse", "l'affirmation fausse")],
            "lambda Ga N Ga égale lambda F N F، إذن N Ga sur N F égale lambda F sur lambda Ga، égale environ " + dn(C["ratio"], 3) + ": l'affirmation fausse.")},
    ]


EX = {
  "id": "phys_ex_ch4_medical_7", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "radioactivite", "cours": "phys_ch4_radioactivite",
  "titre": "Deux sources d'imagerie médicale : quand leurs activités sont-elles égales ?", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série).",
  "competences": ["Calculer λ en s⁻¹ et N₀ = a₀/λ", "Établir la date d'égalité de deux activités", "Calculer une masse restante m(t) = m₀·e^(−λt)",
                  "Calculer un pourcentage de noyaux désintégrés", "Exploiter a = λ·N pour critiquer une affirmation"],
  "enonce": {
    "intro": intro(PA),
    "intro_dit": "دابا نقراو l'énoncé. واحد le service d'imagerie médicale كيستقبل، فt égale zéro، les deux sources radioactives، émettrices bêta plus. source de fluor dix-huit، l'activité égale un virgule cinq fois dix puissance neuf becquerels. و source de carbone onze، l'activité égale six fois dix puissance neuf becquerels. la figure كتبين l'activité ديال كل source en fonction du temps.",
    "figures": [figure(PA, A)],
    "donnees": donnees(PA),
    "questions": Q},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXP}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FAC}]},
  "similaire": {"id": "phys_ex_ch4_medical_7_b", "titre": "Même exercice, autres données : fluor 18 et gallium 68",
    "enonce": {"intro": intro(PB),
               "intro_dit": "نفس التمرين، بقيم أخرى: source de fluor dix-huit، و source de gallium soixante-huit.",
               "figures": [figure(PB, B)], "donnees": donnees(PB), "questions": qb()}},
}

if __name__ == "__main__":
    ecrire(EX)
