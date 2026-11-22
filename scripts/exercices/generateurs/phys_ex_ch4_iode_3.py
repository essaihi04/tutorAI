# Exercice moyen de physique (ch. 4, décroissance radioactive) : une gélule d'iode 131, de la masse à l'activité.
# Sources comparées (skill exercices § 2) :
# - exploration radioactivite.json : cas_types equation, lambda_t_demi, nombre_noyaux (6 fois au national),
#   activite_date (8 fois), pourcentage ; erreurs_examen « λ laissé en j⁻¹ dans a = λ·N », « m en µg ou en kg dans
#   N = (m/M)·N_A », « x % désintégrés pris pour x % restants », « temps négatif » ; valeurs_reperes (λ de l'iode 131
#   ≈ 0,0866 j⁻¹ ≈ 1,0·10⁻⁶ s⁻¹ ; 1 jour = 86 400 s).
# - nationaux comparés : 2022 N (iode 131 : équation avec tableau Te/Xe/Cs, t½ = 8 jours LUE sur la courbe a(t),
#   N₀ = a₀·t½/ln2, durée pour 95 % désintégrés), 2021 R (phosphore 32 : ln N = f(t), N₀ = (m₀/M)·N_A, a₀ = λ·N₀, a à 2t½),
#   2023 N (tritium : m₀ = 2 µg, activité quand 90 % désintégrés), 2020 N (polonium : λ en s⁻¹, date pour a₁).
#   Ici : t½ donnée, la masse d'une gélule (1,0 µg) → N₀ (« montrer que ») → a₀ = λ·N₀ (λ en s⁻¹) → a à 10 jours
#   (hors palier) → date où l'activité a DIMINUÉ de 80 % ; ni courbe à lire, ni 95 % : autre chaîne et autres données
#   que 2022 N, autre noyau que 2021 R.
# - séries en ligne : recherche web faite (séries Talamidi BIOF sur l'iode 131 : activité d'une masse donnée, masse
#   pour une activité ; moutamadris, kezakoo) mais les pages sont bloquées par le réseau de la session : seuls les
#   titres et extraits des résultats ont été lus.
# - simulations du cours : desintegration.html?type=beta_moins, lambda.html, figures.html (fig_masse_N,
#   fig_activite_demo), activite.html (a₀ = 400 Bq, t½ = 8 j, set_parameters t_j), pourcentages.html (desintegres_pct).
# Hors chapitre évité : défaut de masse, énergie (cours suivant), neutrino.
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

SIM = "/media/simulations/physics/radioactivite-tableau/"
NA, JOUR = 6.02e23, 86400


def calc(t_demi, m0_g, M, t1, baisse_pct):
    lj = math.log(2) / t_demi
    ls = lj / JOUR
    N0 = m0_g / M * NA
    a0 = ls * N0
    a1 = a0 * math.exp(-lj * t1)
    t2 = math.log(100 / (100 - baisse_pct)) / lj
    return dict(lj=lj, ls=ls, N0=N0, a0=a0, a1=a1, t2=t2)

# exercice : iode 131 ; similaire : strontium 89
D = calc(8.0, 1.0e-6, 131, 10, 80)
Db = calc(50.5, 2.0e-6, 89, 30, 90)
# contrôles indépendants (valeurs écrites)
assert abs(D["lj"] - 0.0866) < 5e-5 and abs(D["ls"] - 1.0e-6) < 0.01e-6
assert abs(D["N0"] - 4.6e15) / 4.6e15 < 0.01 and abs(D["a0"] - 4.6e9) / 4.6e9 < 0.01
assert abs(D["a1"] - 1.9e9) / 1.9e9 < 0.03 and round(D["t2"], 1) == 18.6
assert abs(400 * 2 ** (-10 / 8) - 168) < 0.5          # ce qu'affiche activite.html au jour 10
assert abs(Db["ls"] - 1.59e-7) / 1.59e-7 < 0.01 and abs(Db["N0"] - 1.35e16) / 1.35e16 < 0.01
assert abs(Db["a0"] - 2.15e9) / 2.15e9 < 0.01 and abs(Db["a1"] - 1.42e9) / 1.42e9 < 0.01 and round(Db["t2"]) == 168


def schema(nom, m0_txt, titre):
    """La gélule et le tableau des numéros atomiques."""
    return {"type": "schema", "titre": titre, "cadre": {"l": 4.2, "h": 2.0},
            "legende": f"À t = 0, la gélule contient m₀ = {m0_txt} de {nom}.",
            "elements": [
                {"f": "rect", "de": [0.3, 0.7], "a": [1.5, 1.3], "couleur": "jaune", "remplir": "faible", "arrondi": True},
                {"f": "texte", "at": [0.9, 0.95], "t": nom, "couleur": "blanc", "ancre": "centre"},
                {"f": "texte", "at": [0.9, 0.35], "t": f"m₀ = {m0_txt}", "couleur": "jaune", "ancre": "centre"},
                {"f": "fleche", "de": [1.6, 1.0], "a": [2.1, 1.0], "couleur": "rose", "texte": "β⁻", "pos": "n"},
                {"f": "texte", "at": [3.1, 1.45], "t": "noyau fils ?", "couleur": "cyan", "ancre": "centre"},
                {"f": "texte", "at": [3.1, 0.95], "t": "+ électron ⁰₋₁e", "couleur": "cyan", "ancre": "centre"}]}


I131, XE = "¹³¹₅₃I", "¹³¹₅₄Xe"

EX = {
  "id": "phys_ex_ch4_iode_3", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "radioactivite", "cours": "phys_ch4_radioactivite",
  "titre": "Une gélule d'iode 131 : de la masse à l'activité", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Écrire une équation β⁻ avec les lois de Soddy", "Calculer λ en j⁻¹ et en s⁻¹", "Calculer N₀ = (m₀/M)·N_A",
                  "Calculer a₀ = λ·N₀ et a(t) = a₀·e^(−λt)", "Calculer la date pour une baisse d'activité donnée"],
  "enonce": {
    "intro": f"L'iode 131, {I131}, est radioactif β⁻. On l'utilise en médecine pour soigner la glande thyroïde. Une gélule préparée à la date t = 0 contient une masse m₀ = 1,0 µg d'iode 131.",
    "intro_dit": "دابا نقراو l'énoncé. l'iode cent trente et un radioactif bêta moins. كيستعملوه فالطب، باش يداويو la glande thyroïde. واحد la gélule، وجدوها فt égale zéro، فيها m zéro égale un micro gramme d'iode cent trente et un.",
    "figures": [schema("iode 131", "1,0 µg", "La gélule d'iode 131")],
    "donnees": ["Demi-vie de l'iode 131 : t½ = 8,0 jours", "Masse molaire : M(¹³¹I) = 131 g·mol⁻¹", "N_A = 6,02 × 10²³ mol⁻¹",
                "1 jour = 86 400 s ; ln2 ≈ 0,693",
                "Extrait du tableau périodique : ₅₁Sb ; ₅₂Te ; ₅₃I ; ₅₄Xe ; ₅₅Cs"],
    "questions": [
      {"id": "1", "texte": "Écrire l'équation de désintégration de l'iode 131 en précisant les lois utilisées, et identifier le noyau fils.",
       "texte_dit": "Question un: كتب l'équation ديال la désintégration ديال l'iode، وقول les lois اللي استعملتي، وعرف le noyau fils.",
       "reponse": phrase(f"{I131} → ᴬ_Z X + ⁰₋₁e. Lois de Soddy : 131 = A + 0, donc A = 131 ; 53 = Z − 1, donc Z = 54. Dans le tableau, Z = 54 : le xénon. {I131} → {XE} + ⁰₋₁e."),
       "clavier": {"aides": ["→", "⁰₋₁e", "A = A₁ + A₂", "Z = Z₁ + Z₂", "Xe"], "pieges": ["Z = 52 (Te)", "⁰₁e"]},
       "aides": [
         aide(f"Écris {I131} → ᴬ_Z X + ⁰₋₁e : l'électron, c'est la particule β⁻.", "كتب l'iode كيعطي X، plus l'électron. l'électron هو la particule bêta moins."),
         aide("Soddy : une ligne pour A, une ligne pour Z ; puis cherche Z (pas A) dans le tableau.", "Soddy: سطر ل A، وسطر ل Z. من بعد قلب على Z فالجدول، ماشي على A.")],
       "correction": correction([
           (f"1 : {I131} → ᴬ_Z X + ⁰₋₁e", "l'iode كيعطي X"),
           ("Soddy : 131 = A + 0 ⇒ A = 131 ; 53 = Z − 1 ⇒ Z = 54", "donc Z égale cinquante-quatre"),
           (f"Z = 54 : xénon ; {I131} → {XE} + ⁰₋₁e", "c'est le xénon")],
         "Question un. l'iode كيعطي X، plus l'électron. d'après les lois de Soddy: cent trente et un égale A plus zéro، donc A égale cent trente et un. cinquante-trois égale Z moins un، donc Z égale cinquante-quatre. فالجدول، c'est le xénon cent trente et un."),
       "explication": "ex_i1", "facile": "fa_i1"},
      {"id": "2", "texte": "Calculer la constante radioactive λ de l'iode 131 en jour⁻¹, puis en s⁻¹.",
       "texte_dit": "Question deux: حسب la constante radioactive lambda، الأول ب jour puissance moins un، ومن بعد ب seconde puissance moins un.",
       "reponse": valeur("λ", D["ls"], "s⁻¹", f"λ = (ln 2)/t½ = 0,693/8,0 ≈ {fr(D['lj'], 4)} j⁻¹ ; λ = {fr(D['lj'], 4)}/86 400 ≈ {sci(D['ls'], 2).replace('1 ×', '1,0 ×')} s⁻¹"),
       "clavier": {"aides": ["λ = (ln 2)/t½", "1 j = 86 400 s", "j⁻¹", "s⁻¹", "A.N. :"], "pieges": ["× 86 400", "λ = t½/(ln 2)"]},
       "aides": [
         aide("λ = (ln 2)/t½ : avec t½ en jours, λ sort en jour⁻¹.", "lambda égale ln deux sur t un demi. t un demi بالجور، إذن lambda ب jour puissance moins un."),
         aide("Un jour = 86 400 s : « par jour » devient « par seconde » en divisant par 86 400.", "un jour égale quatre-vingt-six mille quatre cents secondes. باش نمشيو ل seconde puissance moins un، كنقسمو par quatre-vingt-six mille quatre cents.")],
       "correction": correction([
           ("2 : λ = (ln 2)/t½ = 0,693/8,0 ≈ 0,0866 j⁻¹", "zéro virgule zéro huit cent soixante-six jour puissance moins un"),
           ("λ = 0,0866/86 400", "sur quatre-vingt-six mille quatre cents"),
           ("λ ≈ 1,0 × 10⁻⁶ s⁻¹", "un virgule zéro fois dix puissance moins six seconde puissance moins un")],
         "Question deux. lambda égale ln deux sur t un demi، soit zéro virgule six cent quatre-vingt-treize sur huit. lambda environ zéro virgule zéro huit cent soixante-six jour puissance moins un. من بعد كنقسمو sur quatre-vingt-six mille quatre cents. lambda environ un virgule zéro fois dix puissance moins six seconde puissance moins un."),
       "explication": "ex_i2", "facile": "fa_i2"},
      {"id": "3", "texte": "Montrer que le nombre de noyaux d'iode 131 contenus dans la gélule à t = 0 est N₀ ≈ 4,6 × 10¹⁵.",
       "texte_dit": "Question trois: بين بلي le nombre de noyaux فla gélule، فt égale zéro، هو N zéro environ quatre virgule six fois dix puissance quinze.",
       "reponse": valeur("N₀", D["N0"], "noyaux", f"N₀ = (m₀/M)·N_A = (1,0 × 10⁻⁶/131) × 6,02 × 10²³ ≈ {sci(D['N0'], 2)}"),
       "clavier": {"aides": ["n = m/M", "N₀ = (m₀/M)·N_A", "1 µg = 10⁻⁶ g", "N_A", "A.N. :"], "pieges": ["10⁻⁹ kg", "N₀ = M·N_A/m₀", "1,0 µg = 10⁻³ g"]},
       "aides": [
         aide("Passe par la quantité de matière : n = m/M, avec m en grammes (1 µg = 10⁻⁶ g).", "دوز من la quantité de matière: n égale m sur M، و m بالغرام. un micro gramme égale dix puissance moins six gramme."),
         aide("Une mole contient N_A noyaux : N₀ = n·N_A = (m₀/M)·N_A.", "une mole فيها N A noyaux. إذن N zéro égale m zéro sur M، fois N A.")],
       "correction": correction([
           ("3 : N₀ = n·N_A = (m₀/M)·N_A", "N zéro égale m zéro sur M، fois N A"),
           ("N₀ = (1,0 × 10⁻⁶/131) × 6,02 × 10²³", "un fois dix puissance moins six sur cent trente et un"),
           ("N₀ ≈ 4,6 × 10¹⁵ noyaux", "quatre virgule six fois dix puissance quinze noyaux")],
         "Question trois. N zéro égale m zéro sur M، fois N A. A.N.: un fois dix puissance moins six sur cent trente et un، fois six virgule zéro deux fois dix puissance vingt-trois. N zéro environ quatre virgule six fois dix puissance quinze noyaux. c'est le résultat demandé."),
       "explication": "ex_i3", "facile": "fa_i3"},
      {"id": "4", "texte": "Calculer l'activité a₀ de la gélule à la date t = 0.",
       "texte_dit": "Question quatre: حسب l'activité a zéro ديال la gélule، فt égale zéro.",
       "reponse": valeur("a₀", D["a0"], "Bq", f"a₀ = λ·N₀ = 1,0 × 10⁻⁶ × 4,6 × 10¹⁵ ≈ {sci(D['a0'], 2)} Bq"),
       "clavier": {"aides": ["a₀ = λ·N₀", "λ en s⁻¹", "Bq", "A.N. :"], "pieges": ["λ en j⁻¹", "a₀ = N₀/λ"]},
       "aides": [
         aide("L'activité est proportionnelle au nombre de noyaux présents : quelle relation du cours ?", "l'activité proportionnelle ل le nombre de noyaux. شنو هي la relation ديال الدرس؟"),
         aide("a₀ = λ·N₀, avec λ en s⁻¹ pour avoir des becquerels (désintégrations par seconde).", "a zéro égale lambda N zéro. و lambda خاصها ب seconde puissance moins un، باش يخرج le becquerel.")],
       "correction": correction([
           ("4 : a₀ = λ·N₀ (λ en s⁻¹)", "a zéro égale lambda N zéro"),
           ("a₀ = 1,0 × 10⁻⁶ × 4,6 × 10¹⁵", "un virgule zéro fois dix puissance moins six"),
           ("a₀ ≈ 4,6 × 10⁹ Bq", "quatre virgule six fois dix puissance neuf becquerels")],
         "Question quatre. a zéro égale lambda N zéro، و lambda ب seconde puissance moins un. A.N.: un virgule zéro fois dix puissance moins six، fois quatre virgule six fois dix puissance quinze. a zéro environ quatre virgule six fois dix puissance neuf becquerels."),
       "explication": "ex_i4", "facile": "fa_i4"},
      {"id": "5", "texte": "Calculer l'activité a₁ de la gélule à la date t₁ = 10 jours.",
       "texte_dit": "Question cinq: حسب l'activité a un، فt un égale dix jours.",
       "reponse": valeur("a₁", D["a1"], "Bq", f"a₁ = a₀·e^(−λt₁) = 4,6 × 10⁹ × e^(−0,0866 × 10) ≈ {sci(D['a1'], 2)} Bq"),
       "clavier": {"aides": ["a(t) = a₀·e^(−λt)", "λ·t sans unité", "e^(−0,866)", "A.N. :"], "pieges": ["a₀/10", "a₀·e^(λt)", "λ en s⁻¹ et t en jours"]},
       "aides": [
         aide("10 jours n'est pas un nombre entier de demi-vies : utilise la loi de l'activité.", "dix jours ماشي عدد صحيح ديال demi-vies. استعمل la loi ديال l'activité."),
         aide("a(t) = a₀·e^(−λt) ; λ et t dans la même unité : λ = 0,0866 j⁻¹ et t₁ = 10 j.", "a de t égale a zéro exponentielle moins lambda t. lambda و t بنفس l'unité: lambda ب jour puissance moins un، و t بالجور.")],
       "correction": correction([
           ("5 : a₁ = a₀·e^(−λt₁)", "a un égale a zéro exponentielle moins lambda t un"),
           ("a₁ = 4,6 × 10⁹ × e^(−0,0866 × 10) = 4,6 × 10⁹ × 0,42", "fois zéro virgule quarante-deux"),
           ("a₁ ≈ 1,9 × 10⁹ Bq", "un virgule neuf fois dix puissance neuf becquerels")],
         "Question cinq. a un égale a zéro exponentielle moins lambda t un. lambda fois t un، zéro virgule zéro huit cent soixante-six fois dix، soit zéro virgule huit cent soixante-six. exponentielle moins zéro virgule huit cent soixante-six، environ zéro virgule quarante-deux. إذن a un égale quatre virgule six fois dix puissance neuf، fois zéro virgule quarante-deux. a un environ un virgule neuf fois dix puissance neuf becquerels."),
       "explication": "ex_i5", "facile": "fa_i5"},
      {"id": "6", "texte": "Déterminer la date t₂ à laquelle l'activité de la gélule a diminué de 80 % par rapport à a₀.",
       "texte_dit": "Question six: لقا la date t deux، quand l'activité a diminué de quatre-vingts pour cent par rapport à a zéro.",
       "reponse": valeur("t₂", round(D["t2"], 1), "jours", f"a(t₂) = 0,20·a₀ ; t₂ = (1/λ)·ln(a₀/a) = (ln 5)/0,0866 ≈ {fr(D['t2'], 1)} jours"),
       "clavier": {"aides": ["a = a₀·e^(−λt)", "t = (1/λ)·ln(a₀/a)", "0,20·a₀", "ln 5", "A.N. :"], "pieges": ["a = 0,80·a₀", "t = −(1/λ)·ln(a₀/a)"]},
       "aides": [
         aide("« A diminué de 80 % » : quelle part de a₀ reste-t-il ?", "l'activité a diminué de quatre-vingts pour cent: شحال بقا من a zéro؟"),
         aide("Il reste 20 % : 0,20·a₀ = a₀·e^(−λt₂) ; divise par a₀, prends ln : t₂ = (1/λ)·ln(a₀/a) = (ln 5)/λ.", "il reste vingt pour cent: zéro virgule deux a zéro égale a zéro exponentielle moins lambda t deux. قسم على a zéro، ودير ln.")],
       "correction": correction([
           ("6 : baisse de 80 %, il reste 20 % : a(t₂) = 0,20·a₀", "il reste vingt pour cent"),
           ("0,20·a₀ = a₀·e^(−λt₂) ⇒ t₂ = (1/λ)·ln(a₀/a) = (ln 5)/λ", "t deux égale ln cinq sur lambda"),
           ("t₂ = (ln 5)/0,0866 ≈ 18,6 jours", "environ dix-huit virgule six jours")],
         "Question six. l'activité a diminué de quatre-vingts pour cent، إذن il reste vingt pour cent: a de t deux égale zéro virgule deux a zéro. la loi: zéro virgule deux a zéro égale a zéro exponentielle moins lambda t deux. كنديرو ln: t deux égale ln cinq sur lambda. A.N.: ln cinq sur zéro virgule zéro huit cent soixante-six. t deux environ dix-huit virgule six jours."),
       "explication": "ex_i6", "facile": "fa_i6"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    diapo_sim("ex_i1", "Question 1 : l'équation β⁻ de l'iode 131",
      "Soddy : A, puis Z, puis le tableau.",
      SIM + "desintegration.html?type=beta_moins", "La désintégration β⁻ du carbone 14",
      "شوف le carbone quatorze. لداخل le noyau، neutron كيولي proton، وكيخرج l'électron: la particule bêta moins. l'équation: le carbone quatorze كيعطي l'azote quatorze، plus l'électron. Soddy pour A: quatorze égale quatorze plus zéro. pour Z: six égale sept moins un. فالتمرين، l'iode cent trente et un كيعطي X، plus l'électron. pour A: cent trente et un égale A plus zéro، donc A égale cent trente et un. pour Z: cinquante-trois égale Z moins un، donc Z égale cinquante-quatre. فالجدول، Z égale cinquante-quatre، c'est le xénon.",
      [("53 = Z − 1 ⇒ Z = 54", "donc Z égale cinquante-quatre"), ("¹³¹₅₃I → ¹³¹₅₄Xe + ⁰₋₁e", "c'est le xénon")],
      [dict(mot="شوف le carbone quatorze", commande="start"),
       dict(mot="neutron كيولي proton", commande="play_until", parametres={"moment": "transformation"}),
       dict(mot="وكيخرج l'électron", commande="play_until", parametres={"moment": "emission"}),
       dict(mot="l'équation:", commande="play_until", parametres={"moment": "equation"}),
       dict(mot="Soddy pour A", commande="play_until", parametres={"moment": "soddy_A"}),
       dict(mot="pour Z: six", commande="play_until", parametres={"moment": "soddy_Z"}),
       dict(mot="donc Z égale cinquante-quatre", cible="centre:0"),
       dict(mot="c'est le xénon", cible="centre:1")]),
    diapo_sim("ex_i2", "Question 2 : λ en jour⁻¹ puis en s⁻¹",
      "λ = (ln 2)/t½ ; 1 jour = 86 400 s.",
      SIM + "lambda.html", "La constante radioactive de l'iode 131",
      "شوف l'iode cent trente et un على اليسار. فالسبورة: lambda égale zéro virgule zéro quatre-vingt-sept jour puissance moins un، soit un virgule zéro fois dix puissance moins six seconde puissance moins un. نفس lambda، avec deux unités. فالتمرين، lambda égale ln deux sur huit، environ zéro virgule zéro huit cent soixante-six jour puissance moins un. un jour égale quatre-vingt-six mille quatre cents secondes. إذن كنقسمو: lambda environ un virgule zéro fois dix puissance moins six seconde puissance moins un. lambda fois t ما عندوش unité: lambda و t ديما بنفس l'unité.",
      [("λ = 0,693/8,0 ≈ 0,0866 j⁻¹", "environ zéro virgule zéro huit cent soixante-six jour puissance moins un"),
       ("λ = 0,0866/86 400 ≈ 1,0 × 10⁻⁶ s⁻¹", "إذن كنقسمو")],
      [dict(mot="شوف l'iode cent trente et un", commande="start"),
       dict(mot="فالسبورة: lambda", commande="play_until", parametres={"moment": "trace"}),
       dict(mot="نفس lambda", repere="lambda_iode"),
       dict(mot="environ zéro virgule zéro huit cent soixante-six jour puissance moins un", cible="centre:0"),
       dict(mot="إذن كنقسمو", cible="centre:1"),
       dict(mot="lambda fois t", commande="play_until", parametres={"moment": "conversion"})]),
    diapo_sim("ex_i3", "Question 3 : de la masse au nombre de noyaux",
      "N₀ = (m₀/M)·N_A, avec m₀ en grammes.",
      SIM + "figures.html?fig=fig_masse_N", "De la masse au nombre de noyaux",
      "شوف الطريق. الأول la quantité de matière: n égale m sur M. من بعد le nombre de noyaux: N égale m sur M، fois N A. l'exemple فالسبورة: le tritium، deux micro grammes، N zéro égale quatre fois dix puissance dix-sept. le piège: m بالغرام. فالتمرين، m zéro égale un micro gramme، soit un fois dix puissance moins six gramme. N zéro égale un fois dix puissance moins six sur cent trente et un، fois six virgule zéro deux fois dix puissance vingt-trois. N zéro environ quatre virgule six fois dix puissance quinze noyaux.",
      [("N₀ = (m₀/M)·N_A", "N égale m sur M، fois N A"), ("N₀ = (10⁻⁶/131) × 6,02 × 10²³ ≈ 4,6 × 10¹⁵", "N zéro environ quatre virgule six fois dix puissance quinze noyaux")],
      [dict(mot="الأول la quantité", commande="play_until", parametres={"moment": "quantite"}),
       dict(mot="من بعد le nombre de noyaux", commande="play_until", parametres={"moment": "nombre"}),
       dict(mot="N égale m sur M، fois N A", cible="centre:0"),
       dict(mot="l'exemple فالسبورة", commande="play_until", parametres={"moment": "exemple"}),
       dict(mot="le piège", commande="play_until", parametres={"moment": "piege"}),
       dict(mot="N zéro environ quatre virgule six fois dix puissance quinze noyaux", cible="centre:1")]),
    diapo_sim("ex_i4", "Question 4 : l'activité initiale a₀",
      "a₀ = λ·N₀, λ en s⁻¹ : a₀ en becquerels.",
      SIM + "figures.html?fig=fig_activite_demo&depart=derivee", "a = λ·N, a₀ = λ·N₀",
      "عندنا a égale lambda N. فالبداية، t égale zéro، إذن a zéro égale lambda N zéro. رد البال: a ب becquerel، يعني désintégrations par seconde. إذن lambda خاصها ب seconde puissance moins un. فالتمرين: a zéro égale un virgule zéro fois dix puissance moins six، fois quatre virgule six fois dix puissance quinze. a zéro environ quatre virgule six fois dix puissance neuf becquerels.",
      [("a₀ = λ·N₀", "إذن a zéro égale lambda N zéro"), ("a₀ = 1,0 × 10⁻⁶ × 4,6 × 10¹⁵ ≈ 4,6 × 10⁹ Bq", "a zéro environ quatre virgule six fois dix puissance neuf becquerels")],
      [dict(mot="فالبداية، t égale zéro", commande="play_until", parametres={"moment": "resultat"}),
       dict(mot="إذن a zéro égale lambda N zéro", repere="resultat"),
       dict(mot="إذن a zéro égale lambda N zéro", cible="centre:0"),
       dict(mot="a zéro environ quatre virgule six fois dix puissance neuf becquerels", cible="centre:1")]),
    diapo_sim("ex_i5", "Question 5 : l'activité après 10 jours",
      "a(t) = a₀·e^(−λt) : après 10 jours, il reste 42 % de l'activité.",
      SIM + "activite.html", "Le compteur Geiger devant une fiole d'iode 131",
      "شوف la fiole d'iode cent trente et un، قدام le compteur Geiger. فالبداية، le compteur affiche quatre cents désintégrations en une seconde: a zéro égale quatre cents becquerels. دابا نحطو le calendrier à dix jours. l'afficheur: cent soixante-huit becquerels. cent soixante-huit sur quatre cents، soit zéro virgule quarante-deux: c'est exponentielle moins lambda fois dix jours. فالتمرين، نفس l'iode، إذن نفس le rapport. a un égale a zéro exponentielle moins lambda t un، soit quatre virgule six fois dix puissance neuf، fois zéro virgule quarante-deux. a un environ un virgule neuf fois dix puissance neuf becquerels.",
      [("a₁ = a₀·e^(−λt₁)", "a un égale a zéro exponentielle moins lambda t un"), ("a₁ = 4,6 × 10⁹ × 0,42 ≈ 1,9 × 10⁹ Bq", "a un environ un virgule neuf fois dix puissance neuf becquerels")],
      [dict(mot="شوف la fiole", commande="start"),
       dict(mot="فالبداية، le compteur", commande="play_until", parametres={"moment": "une_seconde"}),
       dict(mot="دابا نحطو le calendrier", commande="set_parameters", parametres={"t_j": 10}),
       dict(mot="l'afficheur: cent soixante-huit", repere="affichage"),
       dict(mot="a un égale a zéro exponentielle moins lambda t un", cible="centre:0"),
       dict(mot="a un environ un virgule neuf fois dix puissance neuf becquerels", cible="centre:1")]),
    diapo_sim("ex_i6", "Question 6 : une baisse de 80 %",
      "Baisse de 80 % : il reste 20 % ; t = (1/λ)·ln(a₀/a).",
      SIM + "pourcentages.html", "Désintégrés et restants : traduire le pourcentage",
      "شوف l'échantillon de cent noyaux. نحطو le curseur: quatre-vingts pour cent désintégrés. il reste vingt pour cent: N égale zéro virgule deux N zéro. و a égale lambda N، إذن l'activité حتى هي égale zéro virgule deux a zéro. فالتمرين، l'activité a diminué de quatre-vingts pour cent: il reste vingt pour cent. la loi: zéro virgule deux a zéro égale a zéro exponentielle moins lambda t deux. كنديرو ln: t deux égale ln cinq sur lambda. A.N.: ln cinq sur zéro virgule zéro huit cent soixante-six، soit environ dix-huit virgule six jours.",
      [("a(t₂) = 0,20·a₀", "il reste vingt pour cent: N"), ("t₂ = (ln 5)/λ = 1,61/0,0866 ≈ 18,6 jours", "soit environ dix-huit virgule six jours")],
      [dict(mot="شوف l'échantillon", commande="start"),
       dict(mot="نحطو le curseur", commande="set_parameters", parametres={"desintegres_pct": 80}),
       dict(mot="il reste vingt pour cent: N", repere="a_toi"),
       dict(mot="il reste vingt pour cent: N", cible="centre:0"),
       dict(mot="soit environ dix-huit virgule six jours", cible="centre:1")]),
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_i1", "Plus facile : le noyau fils", "نتمرنو بسؤال ساهل. اختار le noyau fils.",
      f"{I131} → ᴬ_Z X + ⁰₋₁e. Le noyau fils est…", ["¹³¹₅₂Te", "¹³¹₅₄Xe", "¹³⁰₅₄Xe"], 1, {
        "1": {"juste": rep("مزيان! A égale cent trente et un، و Z égale cinquante-trois plus un، cinquante-quatre: le xénon.", "Juste : A = 131, Z = 53 + 1 = 54 : le xénon.")},
        "0": {"1": rep("رد البال للإشارة: l'électron عندو Z égale moins un. cinquante-trois égale Z moins un. عاود اختار.", "L'électron a Z = −1 : 53 = Z − 1. Réessaie."),
              "2": rep("الجواب: le xénon cent trente et un. Z égale cinquante-quatre، et pas cinquante-deux.", "Réponse : ¹³¹₅₄Xe ; Z = 54, pas 52.")},
        "2": {"1": rep("قريب! ولكن l'électron ماعندو حتى nucléon: A كيبقى هو هو. عاود اختار.", "L'électron a A = 0 : A ne change pas. Réessaie."),
              "2": rep("الجواب: le xénon cent trente et un. A reste cent trente et un.", "Réponse : ¹³¹₅₄Xe ; A reste 131.")}},
      "L'iode cent trente et un donne X plus un électron. Le noyau fils est ?"),
    vf_facile("fa_i2", "Plus facile : λ en s⁻¹", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
      "λ = 0,0866 j⁻¹ et 1 jour = 86 400 s.", [
        ("λ = 0,0866/86 400 ≈ 1,0 × 10⁻⁶ s⁻¹", True, "Par jour → par seconde : une seconde est 86 400 fois plus courte, donc λ est 86 400 fois plus petit."),
        ("λ = 0,0866 × 86 400 ≈ 7,5 × 10³ s⁻¹", False, "On divise, on ne multiplie pas : en une seconde, il se désintègre beaucoup moins qu'en un jour.")]),
    qcm_facile("fa_i3", "Plus facile : la masse en grammes", "سؤال ساهل. اختار الكتابة الصحيحة.",
      "Dans N₀ = (m₀/M)·N_A, avec M en g/mol, la masse m₀ = 1,0 µg s'écrit…", ["1,0 × 10⁻⁶ kg", "1,0 × 10⁻⁶ g", "1,0 × 10⁻³ g"], 1, {
        "1": {"juste": rep("مزيان! micro، c'est dix puissance moins six، و m بالغرام بحال M.", "Juste : 1 µg = 10⁻⁶ g, en grammes comme M en g/mol.")},
        "0": {"1": rep("ما تقلقش. M ب gramme par mole، إذن m خاصها بالغرام، ماشي بالكيلو. عاود اختار.", "M est en g/mol : m doit être en grammes. Réessaie."),
              "2": rep("la réponse: un fois dix puissance moins six gramme. le kilogramme كيعطي نتيجة غالطة.", "Réponse : 1,0 × 10⁻⁶ g.")},
        "2": {"1": rep("قريب! dix puissance moins trois هو milli، ماشي micro. عاود اختار.", "10⁻³, c'est milli ; micro, c'est 10⁻⁶. Réessaie."),
              "2": rep("la réponse: un fois dix puissance moins six gramme. micro égale dix puissance moins six.", "Réponse : 1,0 × 10⁻⁶ g (micro = 10⁻⁶).")}},
      "La masse m zéro égale un micro gramme s'écrit ?"),
    assoc_facile("fa_i4", "Plus facile : les unités", "سؤال ساهل: ربط كل grandeur مع l'unité ديالها فa zéro égale lambda N zéro.",
      "Dans a₀ = λ·N₀, relie chaque grandeur à son unité.", "Relie chaque grandeur à son unité.",
      [("1", "a₀"), ("2", "λ"), ("3", "N₀")],
      [("a", "Bq (désintégrations par seconde)"), ("b", "s⁻¹"), ("c", "sans unité (un nombre de noyaux)"), ("d", "g/mol")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : l'activité se mesure en becquerels.", "مزيان: l'activité بالbecquerel."),
       "1-b": (False, "s⁻¹ est l'unité de λ ; l'activité compte des désintégrations par seconde : le becquerel.", "لا، هادي l'unité ديال lambda. l'activité بالbecquerel."),
       "1-c": (False, "N₀ est un nombre ; l'activité est un nombre PAR SECONDE : le becquerel.", "لا، l'activité هي عدد فla seconde: le becquerel."),
       "1-d": (False, "g/mol est l'unité d'une masse molaire.", "لا، هادي l'unité ديال la masse molaire."),
       "2-a": (False, "Le becquerel est pour a₀ ; λ s'exprime en inverse d'un temps.", "لا، le becquerel ديال a zéro. lambda هي المقلوب ديال الوقت."),
       "2-b": (True, "Oui : pour avoir des Bq, λ en s⁻¹.", "مزيان: باش يخرج le becquerel، lambda ب seconde puissance moins un."),
       "2-c": (False, "λ a une unité : l'inverse d'un temps (ici s⁻¹).", "لا، lambda عندها unité: المقلوب ديال الوقت."),
       "2-d": (False, "g/mol est l'unité de M, pas de λ.", "لا، هادي l'unité ديال M."),
       "3-a": (False, "N₀ compte des noyaux, sans « par seconde ».", "لا، N zéro كيحسب les noyaux، بلا seconde."),
       "3-b": (False, "s⁻¹ est l'unité de λ ; N₀ est un simple nombre.", "لا، هادي ديال lambda. N zéro غير عدد."),
       "3-c": (True, "Oui : N₀ est un nombre de noyaux.", "مزيان: N zéro عدد ديال les noyaux، بلا unité."),
       "3-d": (False, "g/mol est l'unité de M.", "لا، هادي l'unité ديال M.")},
      ("a₀ en Bq = λ en s⁻¹ × N₀ (nombre) : λ doit être en s⁻¹.", "a zéro بالbecquerel، égale lambda ب seconde puissance moins un، fois N zéro.")),
    qcm_facile("fa_i5", "Plus facile : la loi de l'activité", "سؤال ساهل. اختار la bonne expression.",
      "λ = 0,0866 j⁻¹ et t₁ = 10 jours. L'activité à t₁ s'écrit…", ["a₁ = a₀·e^(0,866)", "a₁ = a₀·e^(−0,866)", "a₁ = a₀ − 0,866"], 1, {
        "1": {"juste": rep("مزيان! a un égale a zéro exponentielle moins lambda t، و lambda t égale zéro virgule huit cent soixante-six.", "Juste : a₁ = a₀·e^(−λt₁), λt₁ = 0,866.")},
        "0": {"1": rep("ما تقلقش. l'activité كتنقص مع الوقت. exponentielle plus كتكبر. عاود اختار.", "L'activité diminue : l'exposant doit être négatif. Réessaie."),
              "2": rep("الجواب: a zéro exponentielle moins zéro virgule huit cent soixante-six. le signe moins ضروري.", "Réponse : a₁ = a₀·e^(−0,866).")},
        "2": {"1": rep("قريب! ولكن la loi exponentielle، ماشي طرح. عاود اختار.", "La loi est exponentielle, pas une soustraction. Réessaie."),
              "2": rep("الجواب: a zéro exponentielle moins zéro virgule huit cent soixante-six.", "Réponse : a₁ = a₀·e^(−0,866).")}},
      "L'activité à t un s'écrit ?"),
    vf_facile("fa_i6", "Plus facile : traduire « a diminué de 80 % »", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
      "L'activité a diminué de 80 % par rapport à a₀.", [
        ("Il reste a = 0,20·a₀.", True, "Diminuer de 80 %, c'est perdre 80 % : il reste 100 − 80 = 20 %."),
        ("Il reste a = 0,80·a₀.", False, "0,80·a₀ voudrait dire qu'on a perdu seulement 20 % ; ici on a perdu 80 %.")]),
  ]}]},
  "similaire": {
    "id": "phys_ex_ch4_iode_3_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Le strontium 89, ⁸⁹₃₈Sr, est radioactif β⁻. On l'utilise en médecine pour soulager les douleurs des os. Un flacon préparé à la date t = 0 contient une masse m₀ = 2,0 µg de strontium 89.",
      "intro_dit": "نفس التمرين، بقيم أخرى. le strontium quatre-vingt-neuf radioactif bêta moins. فt égale zéro، le flacon فيه m zéro égale deux micro grammes.",
      "figures": [schema("strontium 89", "2,0 µg", "Le flacon de strontium 89")],
      "donnees": ["t½ = 50,5 jours", "M(⁸⁹Sr) = 89 g·mol⁻¹", "N_A = 6,02 × 10²³ mol⁻¹", "1 jour = 86 400 s ; ln2 ≈ 0,693",
                  "Extrait du tableau périodique : ₃₇Rb ; ₃₈Sr ; ₃₉Y ; ₄₀Zr"],
      "questions": [
        {"id": "1", "texte": "Écrire l'équation de désintégration du strontium 89 en précisant les lois utilisées, et identifier le noyau fils.",
         "reponse": phrase("⁸⁹₃₈Sr → ᴬ_Z X + ⁰₋₁e ; Soddy : 89 = A + 0, A = 89 ; 38 = Z − 1, Z = 39 : l'yttrium. ⁸⁹₃₈Sr → ⁸⁹₃₉Y + ⁰₋₁e."),
         "clavier": {"aides": ["→", "⁰₋₁e", "Y"], "pieges": ["Z = 37 (Rb)"]},
         "correction": correction([("1 : ⁸⁹₃₈Sr → ᴬ_Z X + ⁰₋₁e", "le strontium كيعطي X"), ("89 = A + 0 ⇒ A = 89 ; 38 = Z − 1 ⇒ Z = 39 : ⁸⁹₃₉Y", "c'est l'yttrium")],
                                  "le strontium كيعطي X، plus l'électron. A égale quatre-vingt-neuf، و Z égale trente-neuf: c'est l'yttrium.")},
        {"id": "2", "texte": "Calculer λ en jour⁻¹, puis en s⁻¹.",
         "reponse": valeur("λ", Db["ls"], "s⁻¹", f"λ = 0,693/50,5 ≈ {fr(Db['lj'], 4)} j⁻¹ ; λ = {fr(Db['lj'], 4)}/86 400 ≈ {sci(Db['ls'], 3)} s⁻¹"),
         "clavier": {"aides": ["λ = (ln 2)/t½", "1 j = 86 400 s"], "pieges": ["× 86 400"]},
         "correction": correction([("2 : λ = (ln 2)/t½ = 0,693/50,5 ≈ 0,0137 j⁻¹", "zéro virgule zéro cent trente-sept"), ("λ = 0,0137/86 400 ≈ 1,59 × 10⁻⁷ s⁻¹", "un virgule cinquante-neuf fois dix puissance moins sept")],
                                  "lambda égale ln deux sur t un demi، environ zéro virgule zéro cent trente-sept jour puissance moins un. sur quatre-vingt-six mille quatre cents: un virgule cinquante-neuf fois dix puissance moins sept seconde puissance moins un.")},
        {"id": "3", "texte": "Montrer que N₀ ≈ 1,35 × 10¹⁶ noyaux.",
         "reponse": valeur("N₀", Db["N0"], "noyaux", f"N₀ = (m₀/M)·N_A = (2,0 × 10⁻⁶/89) × 6,02 × 10²³ ≈ {sci(Db['N0'], 3)}"),
         "clavier": {"aides": ["N₀ = (m₀/M)·N_A", "1 µg = 10⁻⁶ g"], "pieges": ["10⁻⁹ kg"]},
         "correction": correction([("3 : N₀ = (2,0 × 10⁻⁶/89) × 6,02 × 10²³", "N zéro égale m zéro sur M"), ("N₀ ≈ 1,35 × 10¹⁶ noyaux", "un virgule trente-cinq fois dix puissance seize")],
                                  "N zéro égale m zéro sur M، fois N A: deux fois dix puissance moins six sur quatre-vingt-neuf، fois six virgule zéro deux fois dix puissance vingt-trois. N zéro environ un virgule trente-cinq fois dix puissance seize noyaux.")},
        {"id": "4", "texte": "Calculer l'activité a₀ du flacon à t = 0.",
         "reponse": valeur("a₀", Db["a0"], "Bq", f"a₀ = λ·N₀ = 1,59 × 10⁻⁷ × 1,35 × 10¹⁶ ≈ {sci(Db['a0'], 3)} Bq"),
         "clavier": {"aides": ["a₀ = λ·N₀", "λ en s⁻¹"], "pieges": ["λ en j⁻¹"]},
         "correction": correction([("4 : a₀ = λ·N₀ = 1,59 × 10⁻⁷ × 1,35 × 10¹⁶", "a zéro égale lambda N zéro"), ("a₀ ≈ 2,15 × 10⁹ Bq", "deux virgule quinze fois dix puissance neuf becquerels")],
                                  "a zéro égale lambda N zéro، avec lambda ب seconde puissance moins un. a zéro environ deux virgule quinze fois dix puissance neuf becquerels.")},
        {"id": "5", "texte": "Calculer l'activité a₁ à la date t₁ = 30 jours.",
         "reponse": valeur("a₁", Db["a1"], "Bq", f"a₁ = a₀·e^(−λt₁) = 2,15 × 10⁹ × e^(−0,0137 × 30) ≈ {sci(Db['a1'], 3)} Bq"),
         "clavier": {"aides": ["a(t) = a₀·e^(−λt)"], "pieges": ["a₀·e^(λt)"]},
         "correction": correction([("5 : a₁ = a₀·e^(−λt₁) = 2,15 × 10⁹ × e^(−0,412)", "a un égale a zéro exponentielle moins lambda t un"), ("a₁ ≈ 1,42 × 10⁹ Bq", "un virgule quarante-deux fois dix puissance neuf")],
                                  "a un égale a zéro exponentielle moins lambda t un، soit deux virgule quinze fois dix puissance neuf، fois exponentielle moins zéro virgule quatre cent douze. a un environ un virgule quarante-deux fois dix puissance neuf becquerels.")},
        {"id": "6", "texte": "Déterminer la date t₂ à laquelle l'activité du flacon a diminué de 90 % par rapport à a₀.",
         "reponse": valeur("t₂", round(Db["t2"]), "jours", f"a(t₂) = 0,10·a₀ ; t₂ = (1/λ)·ln(a₀/a) = (ln 10)/0,0137 ≈ {round(Db['t2'])} jours"),
         "clavier": {"aides": ["t = (1/λ)·ln(a₀/a)", "0,10·a₀"], "pieges": ["a = 0,90·a₀"]},
         "correction": correction([("6 : il reste 10 % : a(t₂) = 0,10·a₀", "il reste dix pour cent"), ("t₂ = (ln 10)/λ = (ln 10)/0,0137 ≈ 168 jours", "environ cent soixante-huit jours")],
                                  "l'activité a diminué de quatre-vingt-dix pour cent، إذن il reste dix pour cent. t deux égale ln dix sur lambda. t deux environ cent soixante-huit jours.")}
      ]}}
}

ecrire(EX)
