# Exercice de physique, ch. 7 (dipôle RL), niveau difficile n° 6 : deux enregistrements avec deux résistances —
# identifier les courbes, équation en u_R, trouver r ET E à partir des deux paliers, L par la tangente, critiquer
# une affirmation sur l'influence de R.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RL.json : cas_types « courbe » (identifier une courbe,
#    influence de L ou R), « ed_uR » (second membre R·E/L), « permanent », « r », « L » ; capacité RL6 (influence de L
#    et R) ; erreurs_examen « équation en u_R : second membre E au lieu de R·E/L », « courbe pour une autre L (2022 R) ».
#  - nationaux : 2019 R (I-1, I-3, I-4 : identifier, U_R, r), 2022 R (1.3 à 1.6 : courbe pour une autre L),
#    2025 R : au-dessus du national ici (deux inconnues E et r tirées de deux paliers, lecture moins guidée :
#    pas de tangente tracée, pas de valeur de E donnée).
#  - cours phys_ch7_dipole_RL : rl_s8_R (influence.html?vue=R), rl_e5_uR (fig_ed_uR), rl_l1_tangente
#    (courbe.html?vue=tangente : E = 6 V, R = 50 Ω, r = 10 Ω, L = 0,12 H, exactement la courbe (1) de l'exercice).
#  - séries en ligne : recherche web (talamidi, moutamadris, alloschool, série P7 N. Naceiri) ; pages non ouvertes
#    (domaines bloqués dans le conteneur), seuls les intitulés comparés. La courbe (1) reprend la bobine de la
#    simulation (référence fixe de influence.html), la courbe (2) est réglée dans la simulation (R’ = 150 Ω).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch7_rl_6"
SIMD = "/media/simulations/physics/dipole-rl-tableau/"
INFL = SIMD + "influence.html"
FIG_UR = SIMD + "figures.html?fig=fig_ed_uR"
TANG = SIMD + "courbe.html?vue=tangente"


def regler(mot):
    return {"mot": mot, "commande": "set_parameters", "parametres": {"vue": "R", "R": 150}}


def montage(titre):
    return schema(titre, 8, 4.8,
        dipole([1, 0.8], [1, 3.6], "G", "E", pos="o"),
        fil([1, 3.6], [1.6, 3.6]),
        dipole([1.6, 3.6], [3.4, 3.6], "K", "K"),
        dipole([3.4, 3.6], [6.0, 3.6], "R", "R", pos="s"),
        fil([6.0, 3.6], [7, 3.6]),
        dipole([7, 3.6], [7, 0.8], "L", "(L, r)", pos="o"),
        fil([7, 0.8], [1, 0.8]),
        courant([6.5, 3.6], "d"),
        tension([5.6, 4.2], [3.8, 4.2], "u_R", couleur="orange"))


def deux_courbes(I1, t1, I2, t2, tmax, pas, titre):
    """I en mA, τ en ms ; courbe (1) : palier le plus haut."""
    return figure_courbe(titre, axe("t", 0, tmax, "ms", list(range(0, tmax + 1, pas))),
        axe("i", 0, I1 * 1.2, "mA", list(range(0, int(I1 * 1.2) + 1, int(I1 / 5)))),
        [{"f": "courbe", "expr": f"{I1}*(1-exp(-x/{t1}))", "couleur": "vert", "texte": "(1)", "texte_x": tmax * 0.8},
         {"f": "courbe", "expr": f"{I2}*(1-exp(-x/{t2}))", "couleur": "cyan", "texte": "(2)", "texte_x": tmax * 0.8},
         {"f": "repere", "y": I1, "couleur": "faible"},
         {"f": "repere", "y": I2, "t": f"{str(I2).replace('.', ',')} mA", "couleur": "faible"}],
        legende="Courbes i(t) enregistrées avec R₁ et avec R₂ (même bobine, même générateur), K fermé à t = 0.")


R1, R2, r, E, L = 50, 150, 10, 6, 0.12
I1, I2 = E / (R1 + r), E / (R2 + r)                  # 0,1 A ; 0,0375 A
T1, T2 = L / (R1 + r), L / (R2 + r)                  # 2 ms ; 0,75 ms
assert abs(I1 - 0.1) < 1e-12 and abs(I2 - 0.0375) < 1e-12 and abs(T1 - 2e-3) < 1e-12 and abs(T2 - 7.5e-4) < 1e-12
r_calc = (R2 * I2 - R1 * I1) / (I1 - I2)
assert abs(r_calc - 10) < 1e-9 and abs(I1 * (R1 + r_calc) - 6) < 1e-9 and abs(T1 * (R1 + r) - L) < 1e-12
# semblable
S1, S2, sr, SE, SL = 40, 100, 20, 12, 0.3
J1, J2 = SE / (S1 + sr), SE / (S2 + sr)               # 0,2 A ; 0,1 A
U1, U2 = SL / (S1 + sr), SL / (S2 + sr)               # 5 ms ; 2,5 ms
assert abs(J1 - 0.2) < 1e-12 and abs(J2 - 0.1) < 1e-12 and abs((S2 * J2 - S1 * J1) / (J1 - J2) - 20) < 1e-9
assert abs(U1 - 5e-3) < 1e-12 and abs(U2 - 2.5e-3) < 1e-12

ATT1 = ("Courbe (1) : palier 100 mA ; courbe (2) : palier 37,5 mA. En régime permanent I_p = E/(R + r) : plus R est grande, "
        "plus I_p est petite. La courbe (1) correspond donc à R₁ = 50 Ω et la courbe (2) à R₂ = 150 Ω.")
ATT2 = ("u_R + u_b = E avec u_b = L·di/dt + r·i et i = u_R/R, di/dt = (1/R)·du_R/dt : (L/R)·du_R/dt + ((R + r)/R)·u_R = E ; "
        "en multipliant par R/L : du_R/dt + ((R + r)/L)·u_R = R·E/L.")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RL", "cours": "phys_ch7_dipole_RL",
  "titre": "Deux résistances, deux courbes : trouver E, r et L", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Identifier une courbe par son palier I_p = E/(R + r)", "Établir l'équation différentielle en u_R",
                  "Résoudre un système de deux relations pour trouver r et E", "Lire τ et en déduire L",
                  "Prévoir l'influence de R sur τ et critiquer une affirmation"],
  "enonce": {
    "intro": "Un générateur idéal de f.é.m. E inconnue alimente, à travers un interrupteur K, un conducteur ohmique de résistance R en série avec une bobine (L, r) inconnue (figure 1). On fait deux enregistrements de i(t) après la fermeture de K à t = 0 : l'un avec R = R₁ = 50 Ω, l'autre avec R = R₂ = 150 Ω, sans rien changer d'autre. On obtient les courbes (1) et (2) de la figure 2.",
    "intro_dit": "دابا نقراو l'énoncé. un générateur idéal، E ديالو ما معروفاش، l'interrupteur K، un conducteur ohmique R، و une bobine، L و r ديالها ما معروفينش. كنديرو deux enregistrements ديال i en fonction de t: مرة R un égale cinquante ohms، ومرة R deux égale cent cinquante ohms، و ما كنبدلو والو آخر. كنلقاو les courbes un و deux ديال la figure deux.",
    "figures": [montage("Figure 1 : le montage"), deux_courbes(100, 2, 37.5, 0.75, 12, 1, "Figure 2 : les deux enregistrements")],
    "donnees": ["R₁ = 50 Ω ; R₂ = 150 Ω", "E, L et r inconnues", "u_b = L·di/dt + r·i", "On prend 1 − e⁻¹ ≈ 0,63"],
    "questions": [
      question("1", "Associer chaque courbe à la résistance utilisée. Justifier.",
        "السؤال un: ربط كل courbe ب la résistance اللي استعملنا. برر.",
        phrase(ATT1),
        ["I_p = E/(R + r)", "palier", "R₁ < R₂"], ["la courbe la plus lente correspond à R₂", "même palier pour les deux"],
        [aide("Compare les paliers des deux courbes. Quelle relation donne la valeur du palier en fonction de R ?",
              "قارن les paliers ديال les deux courbes. أشمن relation كتعطي le palier بدلالة R؟"),
         aide("I_p = E/(R + r) : avec la même bobine et le même E, une R plus grande donne un palier plus bas.",
              "I p égale E sur R plus r. نفس la bobine و نفس E: إلى كبرات R، le palier كيهبط.")],
        corr([("1 : en régime permanent, I_p = E/(R + r)", "I p égale E sur R plus r"),
              ("R₁ < R₂ ⇒ I_p1 > I_p2", "إلى كبرات R، le palier كيهبط"),
              ("Courbe (1) (palier 100 mA) : R₁ = 50 Ω ; courbe (2) (palier 37,5 mA) : R₂ = 150 Ω", "la courbe un هي R un")],
             "السؤال un. فle régime permanent، I p égale E sur R plus r. نفس E و نفس r: إلى كبرات R، le palier كيهبط. إذن la courbe un هي R un، cinquante ohms، و le palier ديالها cent milliampères. و la courbe deux هي R deux، cent cinquante ohms، و le palier ديالها trente-sept virgule cinq milliampères."),
        "ex_rl6_1", "fa_rl6_1"),
      question("2", "Établir l'équation différentielle vérifiée par la tension u_R(t) aux bornes du conducteur ohmique.",
        "السؤال deux: أثبت l'équation différentielle اللي كتحققها la tension u R ديال le conducteur ohmique.",
        phrase(ATT2),
        ["i = u_R/R", "di/dt = (1/R)·du_R/dt", "× R/L"], ["du_R/dt + ((R + r)/L)·u_R = E/L", "u_R = R·di/dt"],
        [aide("Pars de l'équation en i (additivité), puis remplace i par u_R/R et di/dt par (1/R)·du_R/dt.",
              "بدا من l'équation ديال i، ومن بعد عوض i ب u R sur R، و dé i sur dé t ب un sur R fois dé u R sur dé t."),
         aide("Tu obtiens (L/R)·du_R/dt + ((R + r)/R)·u_R = E : multiplie tout par R/L. Attention au second membre.",
              "غادي تلقى L sur R fois dé u R sur dé t، plus R plus r sur R fois u R، égale E. ضرب كلشي ف R sur L، ورد البال ل الطرف ديال اليمين.")],
        corr([("2 : u_R + u_b = E ; i = u_R/R ; di/dt = (1/R)·du_R/dt", "i égale u R sur R"),
              ("(L/R)·du_R/dt + ((R + r)/R)·u_R = E", "L sur R fois dé u R sur dé t"),
              ("× R/L : du_R/dt + ((R + r)/L)·u_R = R·E/L", "égale R E sur L")],
             "السؤال deux. u R plus u b égale E. و i égale u R sur R: كنعوضو i، و dé i sur dé t ب un sur R fois dé u R sur dé t. كنلقاو L sur R fois dé u R sur dé t، plus R plus r sur R fois u R، égale E. كنضربو ف R sur L: dé u R sur dé t، plus R plus r sur L fois u R، égale R E sur L."),
        "ex_rl6_2", "fa_rl6_2"),
      question("3", "En exploitant les deux paliers, montrer que r = (R₂·I₂ − R₁·I₁)/(I₁ − I₂), puis calculer r.",
        "السؤال trois: باستعمال les deux paliers، بين بلي r égale R deux I deux moins R un I un، sur I un moins I deux، ومن بعد حسب r.",
        valeur("r", 10, "Ω", "E = I₁·(R₁ + r) = I₂·(R₂ + r) ⇒ r = (R₂·I₂ − R₁·I₁)/(I₁ − I₂) = (150 × 0,0375 − 50 × 0,1)/(0,1 − 0,0375) = 10 Ω"),
        ["E = I₁·(R₁ + r)", "E = I₂·(R₂ + r)", "mA → A", "Ω"], ["r = E/I₁ − R₁ (E inconnue)", "r = (R₂ − R₁)/(I₁ − I₂)"],
        [aide("E est inconnue, mais c'est le même générateur : écris I_p = E/(R + r) pour chaque courbe, puis élimine E.",
              "E ما معروفاش، ولكن نفس le générateur. كتب I p égale E sur R plus r ل كل courbe، ومن بعد حيد E."),
         aide("I₁·(R₁ + r) = I₂·(R₂ + r) ⇒ r·(I₁ − I₂) = R₂·I₂ − R₁·I₁. Courants en ampères : I₁ = 0,1 A ; I₂ = 0,0375 A.",
              "I un fois R un plus r égale I deux fois R deux plus r. إذن r fois I un moins I deux égale R deux I deux moins R un I un. les courants بl'ampère.")],
        corr([("3 : E = I₁·(R₁ + r) et E = I₂·(R₂ + r)", "E égale I un fois R un plus r"),
              ("I₁·R₁ + I₁·r = I₂·R₂ + I₂·r ⇒ r = (R₂·I₂ − R₁·I₁)/(I₁ − I₂)", "r égale R deux I deux moins R un I un"),
              ("A.N. : r = (150 × 0,0375 − 50 × 0,1)/(0,1 − 0,0375) = 0,625/0,0625 = 10 Ω", "r égale dix ohms")],
             "السؤال trois. E égale I un fois R un plus r، و E égale I deux fois R deux plus r. كنساويو: I un R un plus I un r égale I deux R deux plus I deux r. إذن r égale R deux I deux moins R un I un، sur I un moins I deux. l'application numérique: zéro virgule six cent vingt-cinq sur zéro virgule zéro six cent vingt-cinq. r égale dix ohms."),
        "ex_rl6_3", "fa_rl6_3"),
      question("4", "En déduire la f.é.m. E du générateur.",
        "السؤال quatre: استنتج E، la force électromotrice ديال le générateur.",
        valeur("E", 6, "V", "E = I₁·(R₁ + r) = 0,1 × (50 + 10) = 6 V"),
        ["E = I₁·(R₁ + r)", "V"], ["E = R₁·I₁ = 5 V", "E = I₁·(R₁ + r) = 100 × 60"],
        [aide("Utilise une des deux relations de la question 3, avec r maintenant connue.",
              "استعمل وحدة من les deux relations ديال السؤال trois، دابا r معروفة."),
         aide("E = I₁·(R₁ + r), avec I₁ en ampères. Vérifie avec la courbe (2).",
              "E égale I un fois R un plus r، و I un بl'ampère. تأكد ب la courbe deux.")],
        corr([("4 : E = I₁·(R₁ + r)", "E égale I un fois R un plus r"),
              ("A.N. : E = 0,1 × 60 = 6 V", "E égale six volts"),
              ("Vérification : I₂·(R₂ + r) = 0,0375 × 160 = 6 V", "zéro virgule zéro trois cent soixante-quinze fois cent soixante")],
             "السؤال quatre. E égale I un fois R un plus r: zéro virgule un fois soixante، E égale six volts. وكنتأكدو ب la courbe deux: zéro virgule zéro trois cent soixante-quinze fois cent soixante، حتى هي six volts."),
        "ex_rl6_4", "fa_rl6_4"),
      question("5", "Déterminer graphiquement la constante de temps τ₁ de la courbe (1), puis calculer L.",
        "السؤال cinq: لقا بالمبيان tau un ديال la courbe un، ومن بعد حسب L.",
        valeur("L", 0.12, "H", "τ₁ = 2 ms (i = 0,63 × 100 = 63 mA) ; L = τ₁·(R₁ + r) = 2·10⁻³ × 60 = 0,12 H"),
        ["0,63·I_p", "L = τ·(R + r)", "H"], ["L = τ₁·R₁ = 0,1 H", "L = 2 × 60 = 120 H"],
        [aide("Aucune tangente n'est tracée : trace-la toi-même, ou utilise 63 % du palier de la courbe (1).",
              "ما كايناش la tangente مرسومة. رسمها نتا، ولا استعمل soixante-trois pour cent ديال le palier ديال la courbe un."),
         aide("i(τ₁) = 0,63 × 100 = 63 mA : horizontale jusqu'à la courbe (1), puis verticale. Ensuite L = τ₁·(R₁ + r).",
              "i de tau un égale soixante-trois milliampères: خط أفقي حتى la courbe un، ومن بعد عمودي. ومن بعد L égale tau un fois R un plus r.")],
        corr([("5 : i(τ₁) = 0,63·I₁ = 63 mA ⇒ on lit τ₁ = 2 ms", "tau un égale deux millisecondes"),
              ("τ₁ = L/(R₁ + r) ⇒ L = τ₁·(R₁ + r) = 2·10⁻³ × 60", "L égale tau un fois R un plus r"),
              ("L = 0,12 H", "L égale zéro virgule douze henry")],
             "السؤال cinq. i de tau un égale zéro virgule soixante-trois fois cent، soixante-trois milliampères. كنقراو tau un égale deux millisecondes. L égale tau un fois R un plus r: deux fois dix puissance moins trois fois soixante. L égale zéro virgule douze henry."),
        "ex_rl6_5", "fa_rl6_5"),
      question("6", "Un élève affirme : « avec R₂, le courant est plus faible, donc il met plus de temps à s'établir ». Calculer τ₂ (en ms) et dire si l'élève a raison.",
        "السؤال six: تلميذ كيقول: مع R deux، le courant صغير، إذن كيطول باش يتأسس. حسب tau deux بla milliseconde، وقول واش عندو الحق.",
        valeur("τ₂", 0.75, "ms", "τ₂ = L/(R₂ + r) = 0,12/160 = 7,5·10⁻⁴ s = 0,75 ms"),
        ["τ = L/(R + r)", "ms"], ["τ₂ = L/R₂ = 0,8 ms", "τ₂ > τ₁"],
        [aide("La durée de l'établissement est fixée par τ. Comment τ = L/(R + r) varie-t-il quand R augmente ?",
              "la durée ديال l'établissement كتحددها tau. كيفاش كتتبدل tau égale L sur R plus r ملي R كتكبر؟"),
         aide("τ₂ = L/(R₂ + r) avec L = 0,12 H et R₂ + r = 160 Ω ; compare à τ₁ = 2 ms.",
              "tau deux égale L sur R deux plus r، مع L égale zéro virgule douze henry و R deux plus r égale cent soixante ohms. قارن مع tau un.")],
        corr([("6 : τ₂ = L/(R₂ + r) = 0,12/160 = 7,5·10⁻⁴ s", "tau deux égale L sur R deux plus r"),
              ("τ₂ = 0,75 ms < τ₁ = 2 ms", "zéro virgule soixante-quinze milliseconde"),
              ("L'élève a tort : avec R₂ le palier est plus bas, mais il est atteint plus vite (τ diminue quand R augmente).", "التلميذ غالط")],
             "السؤال six. tau deux égale L sur R deux plus r: zéro virgule douze sur cent soixante، يعني zéro virgule soixante-quinze milliseconde، صغر من tau un. إذن التلميذ غالط: مع R deux، le palier هابط، ولكن كنوصلو ليه دغيا، حيت tau كتصغر ملي R كتكبر."),
        "ex_rl6_6", "fa_rl6_6"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_rl6_1", "Question 1 : quel palier pour quelle R ?", "I_p = E/(R + r) : R plus grande, palier plus bas (100 mA pour 50 Ω, 37,5 mA pour 150 Ω).",
      INFL, "La courbe de référence (R = 50 Ω) et la deuxième courbe (R’ = 150 Ω)",
      "نديرو التجربة. شوف la courbe الأولى: R égale cinquante ohms، le palier cent milliampères. دابا كنبدلو غير R: cent cinquante ohms. شوف la deuxième courbe: le palier هبط، trente-sept virgule cinq milliampères. علاش؟ I p égale E sur R plus r: R كبرات، إذن I p صغرات. إذن la courbe ذات le palier العالي هي R un، و la courbe ذات le palier الهابط هي R deux.",
      centre=[("I_p = E/(R + r)", "I p égale E sur R plus r"), ("(1) : R₁ = 50 Ω ; (2) : R₂ = 150 Ω", "إذن la courbe ذات le palier العالي هي R un")],
      pointage=[regler("نديرو التجربة"),
                {"mot": "شوف la courbe الأولى", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "دابا كنبدلو غير R", "commande": "play_until", "parametres": {"moment": "R_double"}},
                {"mot": "le palier هبط", "repere": "courbe_R"},
                {"mot": "I p égale E sur R plus r", "cible": "centre:0"},
                {"mot": "إذن la courbe ذات le palier العالي هي R un", "commande": "play_until", "parametres": {"moment": "comparer"}}]),
    diapo_sim("ex_rl6_2", "Question 2 : l'équation en u_R", "i = u_R/R ; on remplace, puis × R/L : du_R/dt + ((R + r)/L)·u_R = R·E/L.",
      FIG_UR, "La méthode du cours : relations, remplacer, multiplier par R/L",
      "الأول les relations: i égale u R sur R، إذن dé i sur dé t égale un sur R، fois dé u R sur dé t. من بعد كنعوضو ف l'équation ديال i. كنلقاو L sur R، fois dé u R sur dé t، plus R plus r sur R، fois u R، égale E. دابا كنضربو كلشي ف R sur L. le résultat: dé u R sur dé t، plus R plus r sur L، fois u R، égale R E sur L. حضي، على اليمين ماشي E، هي R E sur L.",
      centre=[("i = u_R/R ; di/dt = (1/R)·du_R/dt", "i égale u R sur R"), ("du_R/dt + ((R + r)/L)·u_R = R·E/L", "le résultat:")],
      pointage=[{"mot": "الأول les relations:", "commande": "play_until", "parametres": {"moment": "relations"}},
                {"mot": "من بعد كنعوضو", "commande": "play_until", "parametres": {"moment": "remplacer"}},
                {"mot": "دابا كنضربو كلشي ف R sur L.", "commande": "play_until", "parametres": {"moment": "multiplier"}},
                {"mot": "le résultat:", "commande": "play_until", "parametres": {"moment": "resultat"}}]),
    diapo_sim("ex_rl6_3", "Question 3 : deux paliers, une inconnue en moins", "E = I₁(R₁ + r) = I₂(R₂ + r) ⇒ r = (R₂I₂ − R₁I₁)/(I₁ − I₂) = 10 Ω.",
      INFL, "Les deux paliers, 100 mA et 37,5 mA, même générateur",
      "شوف les deux paliers: cent milliampères مع cinquante ohms، و trente-sept virgule cinq milliampères مع cent cinquante ohms. نفس le générateur، إذن نفس E. E égale I un fois R un plus r، و E égale I deux fois R deux plus r. كنساويو، و كنجمعو r: r égale R deux I deux moins R un I un، sur I un moins I deux. cent cinquante fois zéro virgule zéro trois cent soixante-quinze، moins cinquante fois zéro virgule un، كتعطي zéro virgule six cent vingt-cinq. و I un moins I deux égale zéro virgule zéro six cent vingt-cinq. r égale dix ohms.",
      centre=[("I₁(R₁ + r) = I₂(R₂ + r)", "كنساويو"), ("r = 0,625/0,0625 = 10 Ω", "r égale dix ohms")],
      pointage=[regler("شوف les deux paliers"),
                {"mot": "cent milliampères مع cinquante ohms", "commande": "play_until", "parametres": {"moment": "comparer"}},
                {"mot": "trente-sept virgule cinq milliampères", "repere": "palier"},
                {"mot": "كنساويو", "cible": "centre:0"},
                {"mot": "r égale dix ohms", "cible": "centre:1"}]),
    diapo_sim("ex_rl6_4", "Question 4 : E", "E = I₁(R₁ + r) = 0,1 × 60 = 6 V ; vérification : 0,0375 × 160 = 6 V.",
      INFL, "Le même E pour les deux courbes",
      "دابا r معروفة. شوف la courbe الأولى: I un égale cent milliampères، يعني zéro virgule un ampère. E égale I un fois R un plus r: zéro virgule un fois soixante، كتعطي six volts. و la deuxième courbe: zéro virgule zéro trois cent soixante-quinze fois cent soixante، حتى هي six volts. نفس E: le résultat صحيح.",
      centre=[("E = I₁(R₁ + r) = 0,1 × 60 = 6 V", "كتعطي six volts"), ("0,0375 × 160 = 6 V", "حتى هي six volts")],
      pointage=[regler("دابا r معروفة"),
                {"mot": "شوف la courbe الأولى", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "كتعطي six volts", "cible": "centre:0"},
                {"mot": "و la deuxième courbe", "commande": "play_until", "parametres": {"moment": "R_double"}},
                {"mot": "حتى هي six volts", "cible": "centre:1"}]),
    diapo_sim("ex_rl6_5", "Question 5 : τ₁ puis L", "La courbe (1) est celle du cours : τ₁ = 2 ms ; L = τ₁(R₁ + r) = 0,12 H.",
      TANG, "La courbe (1) : 100 mA, la tangente coupe l'asymptote à τ₁",
      "la courbe un هي بالضبط هادي: E égale six volts، R égale cinquante ohms، r égale dix ohms. شوف l'asymptote: cent milliampères. كنرسمو la tangente à l'origine: كتقطع l'asymptote ف tau un. كنهبطو: tau un égale deux millisecondes. وبl'autre méthode: soixante-trois milliampères كتعطي نفس tau. إذن L égale tau un fois R un plus r: deux fois dix puissance moins trois fois soixante، كتعطي zéro virgule douze henry.",
      centre=[("τ₁ = 2 ms", "tau un égale deux millisecondes"), ("L = τ₁(R₁ + r) = 2·10⁻³ × 60 = 0,12 H", "كتعطي zéro virgule douze henry")],
      pointage=[{"mot": "شوف l'asymptote", "commande": "play_until", "parametres": {"moment": "asymptote"}},
                {"mot": "كنرسمو la tangente à l'origine", "commande": "play_until", "parametres": {"moment": "tangente"}},
                {"mot": "tau un égale deux millisecondes", "repere": "tau"},
                {"mot": "كتعطي zéro virgule douze henry", "cible": "centre:1"}]),
    diapo_sim("ex_rl6_6", "Question 6 : R plus grande, τ plus petit", "τ₂ = 0,12/160 = 0,75 ms < τ₁ = 2 ms : le palier est plus bas mais atteint plus vite.",
      INFL, "Deux τ marqués sur l'axe : 2 ms et 0,75 ms",
      "شوف les deux courbes. مع cent cinquante ohms، le palier هابط. ولكن شوف tau: tau deux égale L sur R deux plus r، zéro virgule douze sur cent soixante، كتعطي zéro virgule soixante-quinze milliseconde. و tau un égale deux millisecondes. إذن la deuxième courbe كتوصل ل le palier ديالها دغيا. التلميذ غالط: courant صغير ماشي معناه établissement بطيء.",
      centre=[("τ₂ = L/(R₂ + r) = 0,75 ms", "كتعطي zéro virgule soixante-quinze milliseconde"), ("τ₂ < τ₁ : établissement plus rapide", "التلميذ غالط")],
      pointage=[regler("شوف les deux courbes"),
                {"mot": "ولكن شوف tau", "commande": "play_until", "parametres": {"moment": "comparer"}},
                {"mot": "كتعطي zéro virgule soixante-quinze milliseconde", "repere": "tau"},
                {"mot": "التلميذ غالط", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_rl6_1", "Plus facile : le palier et R", "سؤال ساهل على le palier.",
      "Même bobine, même générateur. Avec la résistance R la plus grande, on obtient…",
      ["le palier le plus haut", "le palier le plus bas", "le même palier"], 1, {
        "1": {"juste": rep("برافو! I p égale E sur R plus r: R كبرات، I p صغرات.", "Juste : I_p = E/(R + r) diminue quand R augmente.")},
        "0": {"1": rep("شوف l'expression: R فين كاينة، فوق ولا لتحت؟ عاود.", "Où est R dans I_p = E/(R + r) ? Réessaie."),
              "2": rep("الجواب: le palier le plus bas. R لتحت ف I p égale E sur R plus r.", "Réponse : le palier le plus bas.")},
        "2": {"1": rep("le palier ما كيتعلقش ب L، ولكن كيتعلق ب R. عاود.", "Le palier ne dépend pas de L, mais il dépend de R. Réessaie."),
              "2": rep("الجواب: le palier le plus bas، حيت I p égale E sur R plus r.", "Réponse : le palier le plus bas.")}},
      "Avec la résistance la plus grande، on obtient quel palier ?"),
    qcm_facile("fa_rl6_2", "Plus facile : le second membre", "سؤال ساهل على l'équation ديال u R.",
      "du_R/dt + ((R + r)/L)·u_R = …",
      ["E", "R·E/L", "E/L"], 1, {
        "1": {"juste": rep("برافو! على اليمين R E sur L.", "Juste : R·E/L.")},
        "0": {"1": rep("ضربنا كلشي ف R sur L، حتى E. عاود.", "On a tout multiplié par R/L, E aussi. Réessaie."),
              "2": rep("الجواب هو R E sur L: E تضربات ف R sur L.", "Réponse : R·E/L.")},
        "2": {"1": rep("E sur L هي ديال l'équation ف i. هنا خاص R حتى هي. عاود.", "E/L, c'est pour l'équation en i. Réessaie."),
              "2": rep("الجواب هو R E sur L، ماشي E sur L.", "Réponse : R·E/L (E/L est pour i).")}},
      "dé u R sur dé t plus R plus r sur L fois u R égale ?"),
    vrai_faux_facile("fa_rl6_3", "Plus facile : vrai ou faux", "سؤال ساهل على les deux paliers.",
      "Même générateur E : palier I₁ avec R₁, palier I₂ avec R₂.",
      [("E = I₁·(R₁ + r)", True, "C'est I_p = E/(R + r) écrit pour la courbe (1)."),
       ("E = I₂·(R₂ + r)", True, "Même générateur : la même relation vaut pour la courbe (2)."),
       ("On peut calculer r = E/I₁ − R₁ directement.", False, "E est inconnue : il faut d'abord égaler les deux expressions de E pour l'éliminer.")]),
    qcm_facile("fa_rl6_4", "Plus facile : E", "سؤال ساهل باش نحسبو E.",
      "I₁ = 100 mA, R₁ = 50 Ω, r = 10 Ω. E vaut…",
      ["6 V", "5 V", "6000 V"], 0, {
        "0": {"juste": rep("برافو! zéro virgule un fois soixante، six volts.", "Juste : E = 0,1 × 60 = 6 V.")},
        "1": {"1": rep("نسيتي r. E égale I un fois R un plus r. عاود.", "Tu as oublié r. Réessaie."),
              "2": rep("الجواب هو six volts: zéro virgule un fois cinquante plus dix.", "Réponse : E = 0,1 × 60 = 6 V.")},
        "2": {"1": rep("حول les milliampères ل ampères. عاود.", "Convertis les mA en A. Réessaie."),
              "2": rep("الجواب هو six volts: cent milliampères هي zéro virgule un ampère.", "Réponse : 6 V (100 mA = 0,1 A).")}},
      "I un égale cent milliampères، R un égale cinquante ohms، r égale dix ohms. E vaut ?"),
    qcm_facile("fa_rl6_5", "Plus facile : calculer L", "سؤال ساهل باش نحسبو L.",
      "τ₁ = 2 ms et R₁ + r = 60 Ω. L vaut…",
      ["0,1 H", "120 H", "0,12 H"], 2, {
        "2": {"juste": rep("برافو! deux fois dix puissance moins trois fois soixante، zéro virgule douze henry.", "Juste : L = 2·10⁻³ × 60 = 0,12 H.")},
        "0": {"1": rep("ضربتي غير ف R un. خاص R un plus r. عاود.", "Il faut R₁ + r, pas R₁ seul. Réessaie."),
              "2": rep("الجواب هو zéro virgule douze henry: tau fois R un plus r.", "Réponse : 0,12 H.")},
        "1": {"1": rep("tau بla seconde: deux millisecondes هي deux fois dix puissance moins trois. عاود.", "τ en secondes. Réessaie."),
              "2": rep("الجواب هو zéro virgule douze henry.", "Réponse : 0,12 H.")}},
      "tau un égale deux millisecondes، R un plus r égale soixante ohms. L vaut ?"),
    qcm_facile("fa_rl6_6", "Plus facile : R et τ", "سؤال ساهل على l'influence ديال R.",
      "Si R augmente (même bobine), la constante de temps τ = L/(R + r)…",
      ["augmente", "diminue", "ne change pas"], 1, {
        "1": {"juste": rep("برافو! R لتحت ف tau: R كتكبر، tau كتصغر، و l'établissement كيولي أسرع.", "Juste : τ diminue, l'établissement est plus rapide.")},
        "0": {"1": rep("شوف فين كاينة R ف tau égale L sur R plus r. عاود.", "Où est R dans τ = L/(R + r) ? Réessaie."),
              "2": rep("الجواب: tau كتنقص، حيت R فle dénominateur.", "Réponse : τ diminue (R au dénominateur).")},
        "2": {"1": rep("tau فيها R plus r. إلى تبدلات R، tau كتتبدل. عاود.", "τ contient R + r. Réessaie."),
              "2": rep("الجواب: tau كتنقص ملي R كتكبر.", "Réponse : τ diminue.")}},
      "Si R augmente، la constante de temps ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage avec une autre bobine (L, r) et un autre générateur (E inconnue). Deux enregistrements : R₁ = 40 Ω, puis R₂ = 100 Ω (figure 2).",
      "intro_dit": "نفس التمرين، بقيم أخرى. R un égale quarante ohms، و R deux égale cent ohms.",
      "figures": [deux_courbes(200, 5, 100, 2.5, 30, 5, "Figure 2 : les deux enregistrements")],
      "donnees": ["R₁ = 40 Ω ; R₂ = 100 Ω", "E, L et r inconnues", "On prend 1 − e⁻¹ ≈ 0,63"],
      "questions": [
        question_semblable("1", "Associer chaque courbe à la résistance utilisée. Justifier.",
          phrase("Courbe (1) : palier 200 mA ; courbe (2) : palier 100 mA. I_p = E/(R + r) diminue quand R augmente : (1) ↔ R₁ = 40 Ω, (2) ↔ R₂ = 100 Ω."),
          ["I_p = E/(R + r)", "palier"], ["même palier"],
          corr([("1 : I_p = E/(R + r) ; R₁ < R₂ ⇒ palier (1) > palier (2)", "I p égale E sur R plus r"), ("(1) : R₁ = 40 Ω ; (2) : R₂ = 100 Ω", "la courbe un هي R un")],
               "I p égale E sur R plus r. إذن la courbe un هي R un، و la courbe deux هي R deux.")),
        question_semblable("2", "Établir l'équation différentielle vérifiée par la tension u_R(t) aux bornes du conducteur ohmique.",
          phrase(ATT2), ["i = u_R/R", "× R/L"], ["… = E/L"],
          corr([("2 : u_R + u_b = E ; i = u_R/R", "i égale u R sur R"), ("du_R/dt + ((R + r)/L)·u_R = R·E/L", "égale R E sur L")],
               "i égale u R sur R. كنعوضو وكنضربو ف R sur L: dé u R sur dé t، plus R plus r sur L fois u R، égale R E sur L.")),
        question_semblable("3", "En exploitant les deux paliers, montrer que r = (R₂·I₂ − R₁·I₁)/(I₁ − I₂), puis calculer r.",
          valeur("r", 20, "Ω", "r = (100 × 0,1 − 40 × 0,2)/(0,2 − 0,1) = 20 Ω"), ["E = I₁·(R₁ + r) = I₂·(R₂ + r)", "Ω"], ["r = E/I₁ − R₁"],
          corr([("3 : I₁·(R₁ + r) = I₂·(R₂ + r) ⇒ r = (R₂·I₂ − R₁·I₁)/(I₁ − I₂)", "r égale R deux I deux moins R un I un"), ("r = (10 − 8)/0,1 = 20 Ω", "vingt ohms")],
               "r égale R deux I deux moins R un I un، sur I un moins I deux: deux sur zéro virgule un، كتعطي vingt ohms.")),
        question_semblable("4", "En déduire la f.é.m. E du générateur.",
          valeur("E", 12, "V", "E = I₁·(R₁ + r) = 0,2 × 60 = 12 V"), ["E = I₁·(R₁ + r)", "V"], ["E = R₁·I₁"],
          corr([("4 : E = I₁·(R₁ + r) = 0,2 × 60", "E égale I un fois R un plus r"), ("E = 12 V", "douze volts")],
               "E égale I un fois R un plus r، يعني zéro virgule deux fois soixante، كتعطي douze volts.")),
        question_semblable("5", "Déterminer graphiquement la constante de temps τ₁ de la courbe (1), puis calculer L.",
          valeur("L", 0.3, "H", "τ₁ = 5 ms ; L = τ₁·(R₁ + r) = 5·10⁻³ × 60 = 0,3 H"), ["L = τ·(R + r)", "H"], ["L = τ₁·R₁"],
          corr([("5 : i(τ₁) = 0,63 × 200 = 126 mA ⇒ τ₁ = 5 ms", "tau un égale cinq millisecondes"), ("L = 5·10⁻³ × 60 = 0,3 H", "zéro virgule trois henry")],
               "tau un égale cinq millisecondes. L égale tau un fois R un plus r، كتعطي zéro virgule trois henry.")),
        question_semblable("6", "Un élève affirme : « avec R₂, le courant est plus faible, donc il met plus de temps à s'établir ». Calculer τ₂ (en ms) et dire si l'élève a raison.",
          valeur("τ₂", 2.5, "ms", "τ₂ = L/(R₂ + r) = 0,3/120 = 2,5·10⁻³ s = 2,5 ms"), ["τ = L/(R + r)", "ms"], ["τ₂ > τ₁"],
          corr([("6 : τ₂ = 0,3/120 = 2,5 ms < τ₁ = 5 ms", "deux virgule cinq millisecondes"), ("L'élève a tort : palier plus bas, atteint plus vite.", "التلميذ غالط")],
               "tau deux égale zéro virgule trois sur cent vingt، يعني deux virgule cinq millisecondes، صغر من tau un. التلميذ غالط.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
