# Exercice facile de physique (ch. 4, décroissance radioactive) : λ = ln2/t½, ce qui reste après n demi-vies,
# la date pour un pourcentage désintégré.
# Sources comparées (skill exercices § 2) :
# - exploration radioactivite.json : cas_types lambda_t_demi (9 fois au national), pourcentage, activite_date ;
#   pieges « à 2t½, 25 % désintégrés », « x % désintégrés pris pour x % restants », « garde le signe moins » ;
#   valeurs_reperes (50 %, 25 %, 12,5 %) ; erreurs_examen « pourcentages ».
# - nationaux comparés : 2021 N (plutonium 238 : durée pour 30 % désintégrés, après lecture de t½ sur a(t) et N₀ = a₀/λ),
#   2022 N (iode 131 : 95 % désintégrés), 2023 N (tritium : QCM 2t½, 90 %), 2018 R / 2019 N (a₀/4 → 2t½).
#   Ici : le bismuth 210 (aucun national), t½ donnée, N(t) à 3t½ puis la date pour 30 % : trois gestes séparés, sans
#   activité ni lecture de courbe ; autre noyau, autres données, autre chaîne que 2021 N.
# - séries en ligne : recherche web faite (séries Talamidi, moutamadris, kezakoo de 2ᵉ Bac BIOF listées) mais les pages
#   sont bloquées par le réseau de la session : seuls les titres et extraits ont été lus.
# - simulations du cours : lambda.html (λ de l'iode 0,087 j⁻¹, curseur λ), population.html?vue=grand_nombre
#   (400 → 200 → 100 → 50 noyaux tous les 8 jours), pourcentages.html (moment « trente »).
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

SIM = "/media/simulations/physics/radioactivite-tableau/"

def calc(t_demi, N0, t1, pct):
    lam = math.log(2) / t_demi
    lam_r = round(lam, 3)                       # valeur écrite au 1)
    n = round(t1 / t_demi)
    assert abs(n * t_demi - t1) < 1e-9
    N1 = N0 / 2 ** n
    t2 = math.log(1 / (1 - pct / 100)) / lam_r
    return dict(lam=lam_r, n=n, N1=N1, t2=t2)

# exercice : bismuth 210 ; similaire : radon 222
D = calc(5.0, 8.0e18, 15, 30)
Db = calc(3.8, 3.2e19, 15.2, 40)
assert (D["lam"], D["n"], round(D["t2"], 1)) == (0.139, 3, 2.6) and abs(D["N1"] - 1.0e18) < 1
assert (Db["lam"], Db["n"], round(Db["t2"], 1)) == (0.182, 4, 2.8) and abs(Db["N1"] - 2.0e18) < 1


def figure(t_demi, N0_coef, tmax, titre):
    lam = math.log(2) / t_demi
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": 0, "max": tmax, "nom": "t", "unite": "jours", "graduations": list(range(0, tmax + 1, 5))},
                     "y": {"min": 0, "max": math.ceil(N0_coef) + 1, "nom": "N", "unite": "× 10¹⁸ noyaux" if N0_coef < 10 else "× 10¹⁹ noyaux",
                           "graduations": list(range(0, math.ceil(N0_coef) + 1, 2 if N0_coef < 10 else 1))}},
            "legende": "Nombre N de noyaux restants en fonction du temps.",
            "elements": [{"f": "courbe", "expr": f"{N0_coef}*exp(-{lam:.5f}*x)", "de": 0, "a": tmax, "couleur": "cyan", "texte": "N(t)", "texte_x": tmax * 0.7, "pos": "ne"},
                         {"f": "point", "at": [0, N0_coef], "t": "N₀", "pos": "e", "couleur": "jaune"}]}


EX = {
  "id": "phys_ex_ch4_demivie_2", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "radioactivite", "cours": "phys_ch4_radioactivite",
  "titre": "Le bismuth 210 : demi-vie, noyaux restants et pourcentage", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer λ = ln2/t½", "Utiliser N(n·t½) = N₀/2ⁿ", "Traduire un pourcentage désintégré et calculer une date avec la loi N(t) = N₀·e^(−λt)"],
  "enonce": {
    "intro": "Le bismuth 210 est radioactif, de demi-vie t½ = 5,0 jours. À la date t = 0, un échantillon contient N₀ = 8,0 × 10¹⁸ noyaux de bismuth 210. La figure représente le nombre N de noyaux restants en fonction du temps : N(t) = N₀·e^(−λt).",
    "intro_dit": "دابا نقراو l'énoncé. le bismuth deux cent dix radioactif، la demi-vie ديالو t un demi égale cinq jours. فt égale zéro، l'échantillon فيه N zéro égale huit fois dix puissance dix-huit noyaux. la courbe كتبين N en fonction de t: N égale N zéro exponentielle moins lambda t.",
    "figures": [figure(5.0, 8.0, 25, "N(t) pour le bismuth 210")],
    "donnees": ["t½ = 5,0 jours", "N₀ = 8,0 × 10¹⁸ noyaux à t = 0", "ln2 ≈ 0,693"],
    "questions": [
      {"id": "1", "texte": "Calculer la constante radioactive λ du bismuth 210, en jour⁻¹.",
       "texte_dit": "Question un: حسب la constante radioactive lambda ديال le bismuth، ب jour puissance moins un.",
       "reponse": valeur("λ", D["lam"], "j⁻¹", f"λ = (ln 2)/t½ = 0,693/5,0 ≈ {fr(D['lam'], 3)} j⁻¹"),
       "clavier": {"aides": ["λ = (ln 2)/t½", "ln 2", "t½", "j⁻¹", "A.N. :"], "pieges": ["λ = t½/(ln 2)", "λ = 1/t½", "s⁻¹"]},
       "aides": [
         aide("λ et t½ sont liées par une relation du cours : t½ = (ln 2)/λ.", "عندنا فالدرس la relation بين lambda و t un demi: t un demi égale ln deux sur lambda."),
         aide("Isole λ : λ = (ln 2)/t½. Avec t½ en jours, λ sort en jour⁻¹.", "عزل lambda: lambda égale ln deux sur t un demi. t un demi بالجور، إذن lambda ب jour puissance moins un.")],
       "correction": correction([
           ("1 : λ = (ln 2)/t½", "lambda égale ln deux sur t un demi"),
           ("λ = 0,693/5,0", "zéro virgule six cent quatre-vingt-treize sur cinq"),
           ("λ ≈ 0,139 j⁻¹", "zéro virgule cent trente-neuf jour puissance moins un")],
         "Question un. lambda égale ln deux sur t un demi. A.N.: zéro virgule six cent quatre-vingt-treize sur cinq. lambda environ zéro virgule cent trente-neuf jour puissance moins un."),
       "explication": "ex_d1", "facile": "fa_d1"},
      {"id": "2", "texte": "Calculer le nombre N₁ de noyaux de bismuth 210 restants à la date t₁ = 15 jours.",
       "texte_dit": "Question deux: حسب N un، le nombre de noyaux اللي بقاو فt un égale quinze jours.",
       "reponse": valeur("N₁", D["N1"], "noyaux", f"t₁ = 15 j = 3·t½ ; N₁ = N₀/2³ = 8,0 × 10¹⁸/8 = {fr(D['N1'] / 1e18, 1)},0 × 10¹⁸ noyaux"),
       "clavier": {"aides": ["N = N₀/2ⁿ", "t₁ = n·t½", "2³ = 8", "A.N. :"], "pieges": ["N = N₀/3", "N = N₀/6", "N₀ − N"]},
       "aides": [
         aide("Combien de demi-vies y a-t-il dans 15 jours ?", "شحال من demi-vie كاينة dans quinze jours؟"),
         aide("À chaque demi-vie, le nombre restant est divisé par 2 : après n demi-vies, N = N₀/2ⁿ.", "فكل demi-vie، N divisé par deux. après n demi-vies، N égale N zéro sur deux puissance n.")],
       "correction": correction([
           ("2 : t₁ = 15 j = 3·t½", "trois demi-vies"),
           ("N₁ = N₀/2³ = 8,0 × 10¹⁸/8", "N un égale N zéro sur deux puissance trois"),
           ("N₁ = 1,0 × 10¹⁸ noyaux", "un fois dix puissance dix-huit noyaux")],
         "Question deux. t un égale quinze jours، soit trois demi-vies. إذن N un égale N zéro sur deux puissance trois، soit huit fois dix puissance dix-huit sur huit. N un égale un fois dix puissance dix-huit noyaux."),
       "explication": "ex_d2", "facile": "fa_d2"},
      {"id": "3", "texte": "Déterminer la date t₂ à laquelle 30 % des noyaux initiaux de bismuth 210 se sont désintégrés.",
       "texte_dit": "Question trois: لقا la date t deux، quand trente pour cent des noyaux initiaux se sont désintégrés.",
       "reponse": valeur("t₂", round(D["t2"], 1), "jours", f"N(t₂) = 0,70·N₀ ; t₂ = (1/λ)·ln(N₀/N) = (1/0,139)·ln(1/0,70) ≈ {fr(D['t2'], 1)} jours"),
       "clavier": {"aides": ["N = N₀·e^(−λt)", "t = (1/λ)·ln(N₀/N)", "0,70·N₀", "ln", "A.N. :"], "pieges": ["N = 0,30·N₀", "t = −(1/λ)·ln(N₀/N)"]},
       "aides": [
         aide("30 % se sont désintégrés : quel pourcentage reste-t-il ? Écris N(t₂) en fonction de N₀.", "trente pour cent تفككو: شحال بقا؟ كتب N de t deux en fonction de N zéro."),
         aide("Il reste 70 % : 0,70·N₀ = N₀·e^(−λt₂). Divise par N₀, puis prends ln : t₂ = (1/λ)·ln(N₀/N).", "il reste soixante-dix pour cent: zéro virgule sept N zéro égale N zéro exponentielle moins lambda t deux. قسم على N zéro، ودير ln.")],
       "correction": correction([
           ("3 : 30 % désintégrés, il reste 70 % : N(t₂) = 0,70·N₀", "il reste soixante-dix pour cent"),
           ("0,70·N₀ = N₀·e^(−λt₂) ⇒ t₂ = (1/λ)·ln(1/0,70)", "t deux égale un sur lambda"),
           ("t₂ = (1/0,139) × ln(1/0,70) ≈ 2,6 jours", "environ deux virgule six jours")],
         "Question trois. trente pour cent désintégrés، إذن il reste soixante-dix pour cent: N de t deux égale zéro virgule sept N zéro. la loi: zéro virgule sept N zéro égale N zéro exponentielle moins lambda t deux. كنديرو ln: t deux égale un sur lambda، fois ln de un sur zéro virgule sept. A.N.: environ deux virgule six jours."),
       "explication": "ex_d3", "facile": "fa_d3"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    diapo_sim("ex_d1", "Question 1 : la constante radioactive λ",
      "λ = (ln 2)/t½, dans l'inverse de l'unité de t½.",
      SIM + "lambda.html", "Deux noyaux, deux constantes λ",
      "شوف l'iode cent trente et un على اليسار، و le carbone quatorze على اليمين. كل نوع ديال noyau عندو la constante radioactive ديالو، lambda. l'iode، t un demi égale huit jours. إذن lambda égale ln deux sur huit، environ zéro virgule zéro quatre-vingt-sept jour puissance moins un. l'unité ديال lambda، هي l'unité ديال t un demi، puissance moins un. فالتمرين، le bismuth deux cent dix: t un demi égale cinq jours. إذن lambda égale ln deux sur cinq، soit zéro virgule cent trente-neuf jour puissance moins un. نحطو هاد lambda فالسبورة، فبلاصة l'iode. lambda كبيرة: les noyaux كيمشيو بالزربة.",
      [("λ = (ln 2)/t½", "إذن lambda égale ln deux sur cinq"), ("λ = 0,693/5,0 ≈ 0,139 j⁻¹", "soit zéro virgule cent trente-neuf jour puissance moins un")],
      [dict(mot="شوف l'iode cent trente et un", commande="start"),
       dict(mot="l'iode، t un demi", commande="play_until", parametres={"moment": "trace"}),
       dict(mot="environ zéro virgule zéro quatre-vingt-sept", repere="lambda_iode"),
       dict(mot="إذن lambda égale ln deux sur cinq", cible="centre:0"),
       dict(mot="soit zéro virgule cent trente-neuf jour puissance moins un", cible="centre:1"),
       dict(mot="نحطو هاد lambda فالسبورة", commande="set_parameters", parametres={"lambda_j": D["lam"]}),
       dict(mot="lambda كبيرة", commande="play_until", parametres={"moment": "course"})]),
    diapo_sim("ex_d2", "Question 2 : après n demi-vies",
      "À chaque demi-vie, N est divisé par 2 : N = N₀/2ⁿ.",
      SIM + "population.html?vue=grand_nombre", "Quatre cents noyaux d'iode 131, comptés tous les 8 jours",
      "شوف l'échantillon: quatre cents noyaux d'iode cent trente et un، t un demi égale huit jours. après huit jours، il reste deux cents. après seize jours، il reste cent. après vingt-quatre jours، il reste cinquante. فكل demi-vie، N divisé par deux. après trois demi-vies، N égale N zéro sur huit. فالتمرين، t un demi égale cinq jours، و t un égale quinze jours: quinze sur cinq، soit trois demi-vies. إذن N un égale N zéro sur huit، soit huit fois dix puissance dix-huit sur huit. N un égale un fois dix puissance dix-huit noyaux.",
      [("N = N₀/2ⁿ", "N égale N zéro sur huit"), ("N₁ = 8,0 × 10¹⁸/2³ = 1,0 × 10¹⁸", "N un égale un fois dix puissance dix-huit noyaux")],
      [dict(mot="شوف l'échantillon", commande="start"),
       dict(mot="après huit jours", commande="play_until", parametres={"moment": "un_t_demi"}),
       dict(mot="après seize jours", commande="play_until", parametres={"moment": "deux_t_demi"}),
       dict(mot="après vingt-quatre jours", commande="play_until", parametres={"moment": "trois_t_demi"}),
       dict(mot="N égale N zéro sur huit", cible="centre:0"),
       dict(mot="N un égale un fois dix puissance dix-huit noyaux", cible="centre:1")]),
    diapo_sim("ex_d3", "Question 3 : 30 % désintégrés",
      "30 % désintégrés : il reste 70 %, puis t = (1/λ)·ln(N₀/N).",
      SIM + "pourcentages.html", "Cent noyaux : désintégrés et restants",
      "شوف l'échantillon de cent noyaux. piège معروف: السؤال كيعطيك les désintégrés، و la loi كتهضر على les restants. إذن كنبدلو الأول. trente pour cent désintégrés: il reste soixante-dix pour cent، N égale zéro virgule sept N zéro. فالتمرين، la loi: zéro virgule sept N zéro égale N zéro exponentielle moins lambda t deux. كنديرو ln: t deux égale un sur lambda، fois ln de un sur zéro virgule sept. soit environ deux virgule six jours.",
      [("N(t₂) = 0,70·N₀", "N égale zéro virgule sept N zéro"), ("t₂ = (1/λ)·ln(1/0,70) ≈ 2,6 j", "soit environ deux virgule six jours")],
      [dict(mot="شوف l'échantillon de cent noyaux", commande="start"),
       dict(mot="trente pour cent désintégrés", commande="play_until", parametres={"moment": "trente"}),
       dict(mot="N égale zéro virgule sept N zéro", repere="ligne_trente"),
       dict(mot="N égale zéro virgule sept N zéro", cible="centre:0"),
       dict(mot="soit environ deux virgule six jours", cible="centre:1")]),
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    vf_facile("fa_d1", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
      "Le bismuth 210 : t½ = 5,0 jours.", [
        ("λ = (ln 2)/t½ = 0,693/5,0 ≈ 0,139 j⁻¹", True, "C'est la relation du cours, avec t½ en jours : λ en jour⁻¹."),
        ("λ = t½/(ln 2) = 5,0/0,693 ≈ 7,2 j⁻¹", False, "Fraction inversée : λ = (ln 2)/t½ ; t½/(ln 2) est la constante de temps τ, en jours.")]),
    qcm_facile("fa_d2", "Plus facile : après trois demi-vies", "سؤال ساهل. اختار الجواب الصحيح.",
      "Après 3 demi-vies, le nombre de noyaux restants est…", ["N₀/3", "N₀/6", "N₀/8"], 2, {
        "2": {"juste": rep("مزيان! N zéro sur deux، من بعد sur quatre، من بعد sur huit.", "Juste : N₀ → N₀/2 → N₀/4 → N₀/8.")},
        "0": {"1": rep("ما تقلقش. فكل demi-vie، N divisé par deux، ماشي par trois. عاود اختار.", "À chaque demi-vie on divise par 2, pas par 3. Réessaie."),
              "2": rep("الجواب: N zéro sur huit. deux fois deux fois deux، soit huit.", "Réponse : N₀/2³ = N₀/8.")},
        "1": {"1": rep("قريب! ولكن فكل demi-vie، N divisé par deux. عاود اختار.", "On divise encore par 2 à chaque demi-vie : 2 × 2 × 2. Réessaie."),
              "2": rep("الجواب: N zéro sur huit. deux puissance trois égale huit، et pas six.", "Réponse : N₀/2³ = N₀/8 (2³ = 8, pas 6).")}},
      "Après trois demi-vies, le nombre de noyaux restants est ?"),
    assoc_facile("fa_d3", "Plus facile : traduire les pourcentages", "سؤال ساهل: ربط كل pourcentage désintégré مع اللي بقا.",
      "Relie chaque pourcentage désintégré au nombre de noyaux restants.", "Relie chaque phrase à N restant.",
      [("1", "30 % désintégrés"), ("2", "90 % désintégrés"), ("3", "75 % désintégrés")],
      [("a", "N = 0,70·N₀"), ("b", "N = 0,10·N₀"), ("c", "N = 0,25·N₀"), ("d", "N = 0,30·N₀")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : 30 % partis, il reste 70 %.", "مزيان: c'est trente pour cent désintégrés، il reste soixante-dix pour cent."),
       "1-b": (False, "0,10·N₀ : il ne resterait que 10 % ; ici 30 % seulement sont partis.", "لا، هنا il reste dix pour cent. ولكن هنا، seulement trente pour cent désintégrés."),
       "1-c": (False, "0,25·N₀ : 75 % partis ; ici c'est 30 %.", "لا، c'est le cas de soixante-quinze pour cent désintégrés."),
       "1-d": (False, "Piège : 0,30·N₀ serait 30 % restants. Ici 30 % sont désintégrés.", "لا، هادا هو le piège: trente pour cent هوما اللي تفككو، ماشي اللي بقاو."),
       "2-a": (False, "0,70·N₀ : 30 % partis ; ici 90 % sont partis.", "لا، c'est le cas de trente pour cent désintégrés."),
       "2-b": (True, "Oui : 90 % partis, il reste 10 %.", "مزيان: c'est quatre-vingt-dix pour cent désintégrés، il reste dix pour cent."),
       "2-c": (False, "0,25·N₀ : 75 % partis ; ici 90 %.", "لا، c'est le cas de soixante-quinze pour cent désintégrés."),
       "2-d": (False, "0,30·N₀ : il resterait 30 % ; il reste 100 − 90.", "لا، شحال بقا؟ c'est cent moins quatre-vingt-dix."),
       "3-a": (False, "0,70·N₀ : 30 % partis ; ici 75 %.", "لا، c'est le cas de trente pour cent désintégrés."),
       "3-b": (False, "0,10·N₀ : 90 % partis ; ici 75 %.", "لا، c'est le cas de quatre-vingt-dix pour cent désintégrés."),
       "3-c": (True, "Oui : 75 % partis, il reste 25 %, le quart (2 t½).", "مزيان: il reste vingt-cinq pour cent، الربع."),
       "3-d": (False, "0,30·N₀ : il resterait 30 % ; il reste 100 − 75.", "لا، شحال بقا؟ c'est cent moins soixante-quinze.")},
      ("On traduit toujours : x % désintégrés, donc il reste (100 − x) %.", "ديما كنبدلو: x pour cent désintégrés، إذن il reste cent moins x pour cent.")),
  ]}]},
  "similaire": {
    "id": "phys_ex_ch4_demivie_2_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Le radon 222 est radioactif, de demi-vie t½ = 3,8 jours. À la date t = 0, un échantillon contient N₀ = 3,2 × 10¹⁹ noyaux de radon 222. La figure représente N(t) = N₀·e^(−λt).",
      "intro_dit": "نفس التمرين، بقيم أخرى. le radon deux cent vingt-deux، t un demi égale trois virgule huit jours. فt égale zéro، N zéro égale trois virgule deux fois dix puissance dix-neuf noyaux.",
      "figures": [figure(3.8, 3.2, 20, "N(t) pour le radon 222")],
      "donnees": ["t½ = 3,8 jours", "N₀ = 3,2 × 10¹⁹ noyaux à t = 0", "ln2 ≈ 0,693"],
      "questions": [
        {"id": "1", "texte": "Calculer la constante radioactive λ du radon 222, en jour⁻¹.",
         "reponse": valeur("λ", Db["lam"], "j⁻¹", f"λ = (ln 2)/t½ = 0,693/3,8 ≈ {fr(Db['lam'], 3)} j⁻¹"),
         "clavier": {"aides": ["λ = (ln 2)/t½", "j⁻¹"], "pieges": ["λ = t½/(ln 2)"]},
         "correction": correction([("1 : λ = (ln 2)/t½ = 0,693/3,8", "lambda égale ln deux sur t un demi"), ("λ ≈ 0,182 j⁻¹", "zéro virgule cent quatre-vingt-deux")],
                                  "lambda égale ln deux sur t un demi، soit zéro virgule six cent quatre-vingt-treize sur trois virgule huit. lambda environ zéro virgule cent quatre-vingt-deux jour puissance moins un.")},
        {"id": "2", "texte": "Calculer le nombre N₁ de noyaux de radon 222 restants à la date t₁ = 15,2 jours.",
         "reponse": valeur("N₁", Db["N1"], "noyaux", f"t₁ = 15,2 j = 4·t½ ; N₁ = N₀/2⁴ = 3,2 × 10¹⁹/16 = {fr(Db['N1'] / 1e18, 1)},0 × 10¹⁸ noyaux"),
         "clavier": {"aides": ["N = N₀/2ⁿ", "t₁ = n·t½"], "pieges": ["N = N₀/4"]},
         "correction": correction([("2 : t₁ = 15,2 j = 4·t½", "quatre demi-vies"), ("N₁ = N₀/2⁴ = 3,2 × 10¹⁹/16 = 2,0 × 10¹⁸ noyaux", "deux fois dix puissance dix-huit noyaux")],
                                  "t un égale quinze virgule deux jours، soit quatre demi-vies. N un égale N zéro sur seize، soit deux fois dix puissance dix-huit noyaux.")},
        {"id": "3", "texte": "Déterminer la date t₂ à laquelle 40 % des noyaux initiaux de radon 222 se sont désintégrés.",
         "reponse": valeur("t₂", round(Db["t2"], 1), "jours", f"N(t₂) = 0,60·N₀ ; t₂ = (1/λ)·ln(N₀/N) = (1/0,182)·ln(1/0,60) ≈ {fr(Db['t2'], 1)} jours"),
         "clavier": {"aides": ["t = (1/λ)·ln(N₀/N)", "0,60·N₀"], "pieges": ["N = 0,40·N₀"]},
         "correction": correction([("3 : il reste 60 % : N(t₂) = 0,60·N₀", "il reste soixante pour cent"), ("t₂ = (1/0,182) × ln(1/0,60) ≈ 2,8 jours", "environ deux virgule huit jours")],
                                  "quarante pour cent désintégrés، إذن il reste soixante pour cent. t deux égale un sur lambda، fois ln de un sur zéro virgule six. t deux environ deux virgule huit jours.")}
      ]}}
}

ecrire(EX)
