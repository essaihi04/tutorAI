# Exercice de physique, ch. 6 (dipôle RC), niveau difficile n° 7 : une courbe sans le temps, du_C/dt = f(u_C) ;
# E et τ, deux condensateurs identiques en parallèle, énergie, puis l'instant où du_C/dt vaut une valeur donnée.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RC.json : cas_types « courbe_non_temporelle » (pente
#    a = −1/(RC), ordonnée E/(RC)), « association » (parallèle : C_eq = C₁ + C₂), « energie » ; pièges « confondre série
#    et parallèle », « oublier le carré », « lire l'unité de l'axe » ; redaction_nationale « du_dt_f_u » (2021 N), « energie ».
#  - nationaux : 2021 N (droite du_C/dt = f(u_C)), 2018 N (condensateurs en parallèle, q = f(u)), 2023 R (énergie) ;
#    ici au-dessus du national : la droite donne E et τ, puis C₀, puis une valeur de du_C/dt à traduire en u_C,
#    en énergie et en date (ln), avec une lecture critique (t₁ entre τ et 5τ).
#  - cours phys_ch6_dipole_RC : rc_e3_formes (fig_ed_formes), rc_l5_pente (fig_du_dt, valeurs du national 2021 N :
#    la voix les cite comme exemple de la figure), rc_a1_parallele (associations.html?vue=parallele, C₁ et C₂ 1→10 µF),
#    rc_l8_calcul (energie.html?vue=calcul), rc_s6_tableau (courbe-charge.html?vue=tableau) ; nos valeurs y sont réglées.
#  - séries en ligne : recherche faite (Naceiri Mrabti « Série P6 », talamidi, moutamadris, alloschool), pages non
#    lisibles depuis cette session (domaines bloqués) : on s'appuie sur les sources du dépôt.
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch6_rc_7"
SIMD = "/media/simulations/physics/dipole-rc-tableau/"


def montage(titre):
    """E, K, R puis deux condensateurs identiques C₀ en parallèle entre A et B."""
    return schema(titre, 9.0, 4.6,
        dipole([1, 0.8], [1, 3.8], "G", "E", pos="o"),
        fil([1, 3.8], [1.8, 3.8]),
        dipole([1.8, 3.8], [3.4, 3.8], "K", "K"),
        dipole([3.4, 3.8], [5.6, 3.8], "R", "R"),
        fil([5.6, 3.8], [7.6, 3.8]),
        dipole([6.2, 3.8], [6.2, 0.8], "C", "C₀", pos="o"),
        dipole([7.6, 3.8], [7.6, 0.8], "C", "C₀", pos="o"),
        tension([8.2, 1.4], [8.2, 3.2], "u_C", pos="e"),
        fil([7.6, 0.8], [1, 0.8]),
        courant([3.2, 0.8], "g"),
        borne([6.2, 3.8], "A", "n"), borne([6.2, 0.8], "B", "s"))


def droite(E, b, umax, pas_y, titre):
    ymax = b * 1.125
    return figure_courbe(titre, axe("u_C", 0, umax, "V", list(range(0, int(umax)))),
        axe("du_C/dt", 0, ymax, "V/s", [i * pas_y for i in range(int(b / pas_y) + 1)]),
        [{"f": "courbe", "expr": f"{b}-{b / E}*x", "de": 0, "a": E, "couleur": "orange", "texte": "du_C/dt = f(u_C)", "texte_x": E * 0.45, "pos": "ne"}],
        legende="Pendant la charge, la dérivée du_C/dt tracée en fonction de u_C.")


E, R, C0 = 8, 2e3, 5e-6
C = 2 * C0                                  # 10 µF
TAU = R * C                                  # 0,02 s
B = E / TAU                                  # 400 V/s
EMAX = 0.5 * C * E ** 2                      # 3,2·10⁻⁴ J
U1 = E - TAU * 100                           # 6 V
E1 = 0.5 * C * U1 ** 2                       # 1,8·10⁻⁴ J
T1 = TAU * math.log(E / (E - U1))            # 27,7 ms
assert abs(TAU - 0.02) < 1e-12 and abs(B - 400) < 1e-9 and abs(EMAX - 3.2e-4) < 1e-12
assert abs(U1 - 6) < 1e-9 and abs(E1 - 1.8e-4) < 1e-12 and abs(T1 * 1e3 - 27.7) < 0.05
assert TAU < T1 < 5 * TAU
# semblable : E = 6 V, R = 5 kΩ, C₀ = 3 µF → C = 6 µF, τ = 30 ms, b = 200 V/s ; E_max = 1,08·10⁻⁴ J ;
# du_C/dt = 50 V/s → u_C = 4,5 V, E_e = 6,08·10⁻⁵ J, t₁ = 30·ln4 = 41,6 ms
assert abs(5e3 * 6e-6 - 0.03) < 1e-12 and abs(6 / 0.03 - 200) < 1e-9 and abs(0.5 * 6e-6 * 36 - 1.08e-4) < 1e-12
assert abs(6 - 0.03 * 50 - 4.5) < 1e-9 and abs(0.5 * 6e-6 * 4.5 ** 2 - 6.075e-5) < 1e-12 and abs(30 * math.log(4) - 41.6) < 0.05

ED_ATT = ("D'après la loi d'additivité : u_R + u_C = E, avec u_R = R·i et i = C·du_C/dt, donc R·C·du_C/dt + u_C = E. "
          "En isolant la dérivée : du_C/dt = −(1/(R·C))·u_C + E/(R·C) : c'est une fonction affine de u_C, "
          "de pente −1/(R·C) et d'ordonnée à l'origine E/(R·C).")
REG_A = {"commande": "set_parameters", "parametres": {"C1_uF": 5, "C2_uF": 5}}
def avec(d, mot):
    x = dict(d); x["mot"] = mot; return x

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RC", "cours": "phys_ch6_dipole_RC",
  "titre": "Une droite sans le temps : du_C/dt en fonction de u_C", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Écrire l'équation différentielle sous la forme du_C/dt = f(u_C)",
                  "Exploiter une droite : pente, ordonnée à l'origine, intersection avec l'axe",
                  "Utiliser la capacité équivalente en parallèle",
                  "Calculer l'énergie stockée et une date avec ln"],
  "enonce": {
    "intro": "Deux condensateurs identiques, de même capacité C₀, sont montés en parallèle ; l'ensemble, de capacité C, initialement déchargé, est chargé à travers un conducteur ohmique de résistance R = 2 kΩ par un générateur idéal de tension de force électromotrice E (figure 1). À t = 0, on ferme K. Un logiciel calcule la dérivée du_C/dt et la trace en fonction de u_C (figure 2). E et C₀ sont inconnues.",
    "intro_dit": "دابا نقراو l'énoncé. deux condensateurs identiques، la capacité ديال كل condensateur C zéro، مركبين en parallèle. المجموعة عندها la capacité C، وفالبداية déchargée، كنشارجيوها عبر un conducteur ohmique، R égale deux kiloohms، مع un générateur، E. فt égale zéro كنسدو K. le logiciel كيحسب dé u C sur dé t، وكيرسمها en fonction de u C: هادي la figure deux. E و C zéro ما عارفينهومش.",
    "figures": [montage("Figure 1 : le montage"), droite(8, 400, 9.5, 50, "Figure 2 : du_C/dt en fonction de u_C")],
    "donnees": ["R = 2 kΩ = 2·10³ Ω", "E et C₀ inconnues"],
    "questions": [
      question("1", "Établir l'équation différentielle vérifiée par u_C, puis montrer que du_C/dt = −(1/(R·C))·u_C + E/(R·C).",
        "السؤال un: بين l'équation différentielle ديال u C، ومن بعد بين بلي dé u C sur dé t égale moins un sur R C fois u C، plus E sur R C.",
        phrase(ED_ATT),
        ["u_R + u_C = E", "i = C·du_C/dt", "diviser par R·C"], ["du_C/dt = (1/(R·C))·u_C + E/(R·C)", "u_R − u_C = E"],
        [aide("Écris d'abord l'équation habituelle R·C·du_C/dt + u_C = E (additivité, loi d'Ohm, i = C·du_C/dt).",
              "كتب الأول l'équation المعروفة: R C dé u C sur dé t، plus u C، égale E، بl'additivité و la loi d'Ohm."),
         aide("Laisse du_C/dt seule à gauche : passe u_C à droite, puis divise tout par R·C.",
              "خلي dé u C sur dé t بوحدها فاليسار: دوز u C لليمين، ومن بعد قسم كلشي على R C.")],
        corr([("1 : u_R + u_C = E, u_R = R·i, i = C·du_C/dt : R·C·du_C/dt + u_C = E", "R C dé u C sur dé t، plus u C، égale E"),
              ("R·C·du_C/dt = −u_C + E, on divise par R·C", "كنقسمو على R C"),
              ("du_C/dt = −(1/(R·C))·u_C + E/(R·C)", "moins un sur R C fois u C، plus E sur R C")],
             "السؤال un. l'additivité، la loi d'Ohm، و i égale C dé u C sur dé t، كيعطيو R C dé u C sur dé t، plus u C، égale E. كندوزو u C لليمين، وكنقسمو على R C: dé u C sur dé t égale moins un sur R C fois u C، plus E sur R C."),
        "ex_p1", "fa_p1"),
      question("2", "En exploitant la figure 2, déterminer E, puis la constante de temps τ = R·C (en ms).",
        "السؤال deux: استغل la figure deux، وحدد E، ومن بعد la constante de temps tau égale R C، بla milliseconde.",
        valeur("τ", 20, "ms", "du_C/dt = 0 pour u_C = E : E = 8 V ; ordonnée à l'origine E/(R·C) = 400 V/s, donc τ = R·C = E/400 = 8/400 = 0,02 s = 20 ms"),
        ["du_C/dt = 0 ⇒ u_C = E", "ordonnée à l'origine E/(R·C)", "pente −1/(R·C)", "ms"], ["τ = 400 s", "E = 400 V", "τ = 1/400 s"],
        [aide("Quand la charge est finie, u_C ne varie plus : du_C/dt = 0. Où la droite coupe-t-elle l'axe des u_C ? Lis aussi l'ordonnée à l'origine.",
              "ملي la charge كتسالي، u C ما بقاتش كتتبدل: dé u C sur dé t égale zéro. فين la droite كتقطع l'axe ديال u C؟ وقرا حتى l'ordonnée à l'origine."),
         aide("u_C = E quand du_C/dt = 0 ; l'ordonnée à l'origine vaut E/(R·C), donc R·C = E/(ordonnée). (Ou la pente : −1/(R·C).)",
              "u C égale E ملي dé u C sur dé t égale zéro. l'ordonnée à l'origine هي E sur R C، إذن R C égale E sur l'ordonnée. ولا la pente: moins un sur R C.")],
        corr([("2 : si du_C/dt = 0 alors u_C = E : la droite coupe l'axe en E = 8 V", "E égale huit volts"),
              ("Ordonnée à l'origine : E/(R·C) = 400 V/s", "quatre cents volts par seconde"),
              ("τ = R·C = E/400 = 8/400 = 0,02 s = 20 ms (pente : −1/τ = −400/8 = −50 s⁻¹)", "tau égale vingt millisecondes")],
             "السؤال deux. ملي dé u C sur dé t égale zéro، u C égale E: la droite كتقطع l'axe فE égale huit volts. l'ordonnée à l'origine، E sur R C، égale quatre cents volts par seconde. إذن R C égale huit sur quatre cents، zéro virgule zéro deux seconde: tau égale vingt millisecondes."),
        "ex_p2", "fa_p2"),
      question("3", "En déduire la capacité C de l'association, puis la capacité C₀ de chaque condensateur.",
        "السؤال trois: استنتج la capacité C ديال المجموعة، ومن بعد la capacité C zéro ديال كل condensateur.",
        valeur("C₀", 5e-6, "F", "C = τ/R = 0,02/(2·10³) = 10⁻⁵ F ; en parallèle C = C₀ + C₀ = 2·C₀, donc C₀ = C/2 = 5·10⁻⁶ F"),
        ["C = τ/R", "C_eq = C₁ + C₂", "C₀ = C/2", "µF"], ["C₀ = 2·C", "1/C = 1/C₀ + 1/C₀"],
        [aide("Calcule d'abord C = τ/R. Ensuite : en parallèle, les capacités s'ajoutent-elles, ou leurs inverses ?",
              "حسب الأول C égale tau sur R. ومن بعد: en parallèle، واش les capacités كيتزادو، ولا les inverses ديالهم؟"),
         aide("En parallèle : C = C₀ + C₀ = 2·C₀, donc C₀ = C/2.",
              "en parallèle: C égale C zéro plus C zéro، يعني deux fois C zéro. إذن C zéro égale C sur deux.")],
        corr([("3 : C = τ/R = 0,02/(2·10³) = 10⁻⁵ F = 10 µF", "C égale dix puissance moins cinq farad"),
              ("En parallèle : C = C₀ + C₀ = 2·C₀", "C égale deux fois C zéro"),
              ("C₀ = C/2 = 5·10⁻⁶ F = 5 µF", "C zéro égale cinq microfarads")],
             "السؤال trois. C égale tau sur R، zéro virgule zéro deux، sur deux mille: C égale dix puissance moins cinq farad، dix microfarads. en parallèle، les capacités كيتزادو: C égale deux fois C zéro. إذن C zéro égale C sur deux، C zéro égale cinq microfarads."),
        "ex_p3", "fa_p3"),
      question("4", "Calculer l'énergie électrique maximale emmagasinée dans l'association.",
        "السؤال quatre: حسب l'énergie électrique القصوى المخزونة فالمجموعة.",
        valeur("E_e,max", 3.2e-4, "J", "En régime permanent u_C = E : E_e,max = ½·C·E² = ½ × 10⁻⁵ × 8² = 3,2·10⁻⁴ J"),
        ["E_e = ½·C·u_C²", "régime permanent : u_C = E", "J"], ["E_e = ½·C₀·E²", "E_e = ½·C·E"],
        [aide("L'énergie est maximale quand u_C est maximale : à quel moment, et quelle valeur ?",
              "l'énergie كتكون قصوى ملي u C قصوى: إمتى، وشحال؟"),
         aide("E_e,max = ½·C·E², avec la capacité C de l'association (pas C₀).",
              "E e max égale un demi C E au carré، مع C ديال المجموعة، ماشي C zéro.")],
        corr([("4 : en régime permanent, u_C = E", "u C égale E"),
              ("E_e,max = ½·C·E² = ½ × 10⁻⁵ × 8²", "un demi fois C fois E au carré"),
              ("E_e,max = 3,2·10⁻⁴ J", "trois virgule deux fois dix puissance moins quatre joule")],
             "السؤال quatre. فle régime permanent، u C égale E. E e max égale un demi fois C fois E au carré، يعني un demi fois dix puissance moins cinq، fois soixante-quatre. E e max égale trois virgule deux fois dix puissance moins quatre joule."),
        "ex_p4", "fa_p4"),
      question("5", "À une date t₁, la dérivée vaut du_C/dt = 100 V/s. Déterminer u_C(t₁), puis l'énergie E_e(t₁) stockée à cette date.",
        "السؤال cinq: فla date t un، dé u C sur dé t égale cent volts par seconde. حدد u C de t un، ومن بعد l'énergie المخزونة فهاد la date.",
        valeur("E_e(t₁)", 1.8e-4, "J", "100 = −u_C/τ + E/τ donne u_C = E − 100·τ = 8 − 100 × 0,02 = 6 V ; E_e(t₁) = ½·C·u_C² = ½ × 10⁻⁵ × 6² = 1,8·10⁻⁴ J"),
        ["du_C/dt = (E − u_C)/τ", "lecture sur la droite", "E_e = ½·C·u_C²", "J"], ["E_e = ½·C·(du_C/dt)²", "u_C = 100·τ"],
        [aide("Cherche sur la figure 2 (ou avec la relation de la question 1) la valeur de u_C pour laquelle du_C/dt = 100 V/s.",
              "قلب فla figure deux، ولا بla relation ديال السؤال un، على u C اللي كتعطي dé u C sur dé t égale cent volts par seconde."),
         aide("du_C/dt = (E − u_C)/τ, donc u_C = E − τ·(du_C/dt). Puis E_e = ½·C·u_C².",
              "dé u C sur dé t égale E moins u C، sur tau. إذن u C égale E moins tau fois la dérivée. ومن بعد E e égale un demi C u C au carré.")],
        corr([("5 : du_C/dt = (E − u_C)/τ, donc u_C(t₁) = E − τ·(du_C/dt)", "u C égale E moins tau fois la dérivée"),
              ("u_C(t₁) = 8 − 0,02 × 100 = 6 V (on le lit aussi sur la droite)", "u C de t un égale six volts"),
              ("E_e(t₁) = ½·C·u_C² = ½ × 10⁻⁵ × 6² = 1,8·10⁻⁴ J", "un virgule huit fois dix puissance moins quatre joule")],
             "السؤال cinq. dé u C sur dé t égale E moins u C، sur tau، إذن u C égale E moins tau fois la dérivée: huit moins zéro virgule zéro deux fois cent. u C de t un égale six volts. E e égale un demi C u C au carré، un demi fois dix puissance moins cinq، fois trente-six: un virgule huit fois dix puissance moins quatre joule. يعني environ cinquante-six pour cent من l'énergie maximale."),
        "ex_p5", "fa_p5"),
      question("6", "Sachant que u_C(t) = E(1 − e^(−t/τ)), calculer la date t₁ (en ms). Situer t₁ par rapport à τ et à 5τ.",
        "السؤال six: عارفين u C égale E fois un moins exponentielle de moins t sur tau. حسب la date t un بla milliseconde، وقارنها مع tau و cinq tau.",
        valeur("t₁", 27.7, "ms", "1 − e^(−t₁/τ) = 6/8, e^(−t₁/τ) = 0,25, t₁ = τ·ln4 = 20 × 1,386 ≈ 27,7 ms"),
        ["e^(−t₁/τ) = 1 − u_C/E", "ln", "t₁ = τ·ln(E/(E − u_C))", "ms"], ["t₁ = τ·ln(0,75)", "t₁ = 0,75·τ"],
        [aide("Remplace u_C par 6 V et E par 8 V dans u_C = E(1 − e^(−t₁/τ)), puis isole l'exponentielle.",
              "عوض u C ب six volts و E ب huit volts، ومن بعد خلي l'exponentielle بوحدها."),
         aide("e^(−t₁/τ) = 1 − 6/8 = 0,25 ; prends le ln : t₁ = τ·ln(1/0,25) = τ·ln4.",
              "exponentielle de moins t un sur tau égale zéro virgule vingt-cinq. خود ln: t un égale tau fois ln quatre.")],
        corr([("6 : 8(1 − e^(−t₁/τ)) = 6, donc e^(−t₁/τ) = 0,25", "exponentielle de moins t un sur tau égale zéro virgule vingt-cinq"),
              ("t₁ = τ·ln4 = 20 × 1,386 ≈ 27,7 ms", "vingt-sept virgule sept millisecondes"),
              ("τ < t₁ < 5τ : u_C(t₁) = 0,75·E est entre 0,63·E (à τ) et 0,99·E (à 5τ), le résultat est cohérent.", "entre tau و cinq tau")],
             "السؤال six. huit fois un moins exponentielle égale six، إذن exponentielle de moins t un sur tau égale zéro virgule vingt-cinq. t un égale tau fois ln quatre، vingt fois un virgule trois huit six، environ vingt-sept virgule sept millisecondes. هادي entre tau و cinq tau: u C égale zéro virgule soixante-quinze fois E، كبر من zéro virgule soixante-trois E و صغر من E. النتيجة معقولة."),
        "ex_p6", "fa_p6"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_p1", "Question 1 : isoler la dérivée", "R·C·du_C/dt + u_C = E ⇒ du_C/dt = −(1/RC)·u_C + E/(RC).",
      SIMD + "figures.html?fig=fig_ed_formes", "La même équation, écrite autrement",
      "كنبداو من l'équation ديال la charge: R C dé u C sur dé t، plus u C، égale E. كنقسمو على R C. كنلقاو dé u C sur dé t، plus un sur R C fois u C، égale E sur R C. وإلى دوزنا u C لليمين: dé u C sur dé t égale moins un sur R C fois u C، plus E sur R C. هادي fonction affine ديال u C: la pente moins un sur R C، و l'ordonnée à l'origine E sur R C.",
      centre=[("du_C/dt = −(1/RC)·u_C + E/(RC)", "dé u C sur dé t égale moins un sur R C fois u C، plus E sur R C")],
      pointage=[{"mot": "كنبداو من l'équation ديال la charge", "commande": "play_until", "parametres": {"moment": "depart"}},
                {"mot": "كنقسمو على R C", "commande": "play_until", "parametres": {"moment": "diviser"}},
                {"mot": "كنلقاو dé u C sur dé t", "commande": "play_until", "parametres": {"moment": "forme"}},
                {"mot": "dé u C sur dé t égale moins un sur R C fois u C، plus E sur R C", "cible": "centre:0"}]),
    diapo_sim("ex_p2", "Question 2 : lire la droite", "u_C = E là où la droite coupe l'axe ; ordonnée E/(RC) ⇒ τ = E/ordonnée.",
      SIMD + "figures.html?fig=fig_du_dt", "L'exemple de la figure (national 2021 N), puis nos valeurs",
      "la figure كتورينا مثال ديال le national deux mille vingt et un. l'équation: dé u C sur dé t égale moins un sur R C fois u C، plus E sur R C. la droite كتهبط. فالمثال، la droite كتقطع l'axe ديال u C à douze volts: هادي هي E، حيت dé u C sur dé t égale zéro فآخر la charge. la pente سالبة، moins un sur R C. و l'ordonnée à l'origine، E sur R C، égale mille volts par seconde فالمثال. عندنا حنا: la droite كتقطع l'axe à huit volts، إذن E égale huit volts. و l'ordonnée égale quatre cents volts par seconde. إذن R C égale huit sur quatre cents، tau égale vingt millisecondes.",
      centre=[("E = 8 V (du_C/dt = 0)", "إذن E égale huit volts"), ("τ = E/400 = 8/400 = 0,02 s = 20 ms", "tau égale vingt millisecondes")],
      pointage=[{"mot": "l'équation: dé u C sur dé t", "commande": "play_until", "parametres": {"moment": "equation"}},
                {"mot": "la droite كتهبط", "commande": "play_until", "parametres": {"moment": "droite"}},
                {"mot": "la pente سالبة", "commande": "play_until", "parametres": {"moment": "pente"}},
                {"mot": "و l'ordonnée à l'origine", "commande": "play_until", "parametres": {"moment": "ordonnee"}},
                {"mot": "إذن E égale huit volts", "cible": "centre:0"},
                {"mot": "tau égale vingt millisecondes", "cible": "centre:1"}]),
    diapo_sim("ex_p3", "Question 3 : C puis C₀", "C = τ/R = 10 µF ; en parallèle C = C₀ + C₀, donc C₀ = 5 µF.",
      SIMD + "associations.html?vue=parallele", "Deux condensateurs en parallèle : même tension, les charges et les capacités s'ajoutent",
      "الأول C égale tau sur R، يعني zéro virgule zéro deux، sur deux mille، dix puissance moins cinq farad، dix microfarads. دابا شوف deux condensateurs en parallèle: عندهم نفس la tension u. les charges كيتزادو: q égale q un plus q deux. إذن C équivalente égale C un plus C deux. عندنا deux condensateurs identiques: C égale deux fois C zéro. نديرو C un égale cinq microfarads، و C deux égale cinq microfarads: C équivalente كتولي dix microfarads. إذن C zéro égale cinq microfarads.",
      centre=[("C = τ/R = 0,02/(2·10³) = 10⁻⁵ F", "dix puissance moins cinq farad، dix microfarads"), ("C = 2·C₀ ⇒ C₀ = 5 µF", "إذن C zéro égale cinq microfarads")],
      pointage=[{"mot": "dix puissance moins cinq farad، dix microfarads", "cible": "centre:0"},
                {"mot": "دابا شوف deux condensateurs en parallèle", "commande": "play_until", "parametres": {"moment": "circuit"}},
                {"mot": "les charges كيتزادو", "commande": "play_until", "parametres": {"moment": "charges"}},
                {"mot": "إذن C équivalente égale C un plus C deux", "commande": "play_until", "parametres": {"moment": "formule"}},
                avec(REG_A, "نديرو C un égale cinq microfarads"),
                {"mot": "C deux égale cinq microfarads", "repere": "C2"},
                {"mot": "إذن C zéro égale cinq microfarads", "cible": "centre:1"}]),
    diapo_sim("ex_p4", "Question 4 : l'énergie maximale", "E_e,max = ½·C·E² = ½ × 10⁻⁵ × 8² = 3,2·10⁻⁴ J.",
      SIMD + "energie.html?vue=calcul", "C = 10 µF, E = 8 V : l'énergie au régime permanent",
      "l'énergie كتكون قصوى ملي u C قصوى، يعني فle régime permanent: u C égale E égale huit volts. C هي la capacité ديال المجموعة، dix microfarads. E e max égale un demi C E au carré، يعني un demi fois dix puissance moins cinq، fois soixante-quatre. E e max égale trois virgule deux fois dix puissance moins quatre joule.",
      centre=[("E_e,max = ½·C·E²", "E e max égale un demi C E au carré"), ("= ½ × 10⁻⁵ × 8² = 3,2·10⁻⁴ J", "E e max égale trois virgule deux fois dix puissance moins quatre joule")],
      pointage=[avec({"commande": "set_parameters", "parametres": {"u_C": 8, "C_uF": 10}}, "l'énergie كتكون قصوى"),
                {"mot": "فle régime permanent", "commande": "play_until", "parametres": {"moment": "regime_permanent"}},
                {"mot": "E e max égale un demi C E au carré", "repere": "formule"},
                {"mot": "E e max égale un demi C E au carré", "cible": "centre:0"},
                {"mot": "E e max égale trois virgule deux fois dix puissance moins quatre joule", "repere": "resultat"},
                {"mot": "E e max égale trois virgule deux fois dix puissance moins quatre joule", "cible": "centre:1"}]),
    diapo_sim("ex_p5", "Question 5 : de du_C/dt à u_C, puis à l'énergie", "u_C = E − τ·du_C/dt = 6 V ; E_e = ½ × 10⁻⁵ × 6² = 1,8·10⁻⁴ J.",
      SIMD + "energie.html?vue=calcul", "C = 10 µF, u_C = 6 V : l'énergie à la date t₁",
      "من l'équation: dé u C sur dé t égale E moins u C، sur tau. إذن u C égale E moins tau fois la dérivée، يعني huit moins zéro virgule zéro deux fois cent: u C égale six volts. دابا l'énergie مع u C égale six volts: E e égale un demi fois dix puissance moins cinq، fois trente-six، يعني un virgule huit fois dix puissance moins quatre joule. قارن: six sur huit au carré كتعطي environ zéro virgule cinquante-six. ماشي zéro virgule soixante-quinze، حيت l'énergie فيها le carré.",
      centre=[("u_C(t₁) = E − τ·(du_C/dt) = 8 − 0,02 × 100 = 6 V", "u C égale six volts"), ("E_e(t₁) = ½ × 10⁻⁵ × 6² = 1,8·10⁻⁴ J", "un virgule huit fois dix puissance moins quatre joule")],
      pointage=[{"mot": "u C égale six volts", "cible": "centre:0"},
                avec({"commande": "set_parameters", "parametres": {"u_C": 6, "C_uF": 10}}, "دابا l'énergie مع u C égale six volts"),
                {"mot": "E e égale un demi fois dix puissance moins cinq", "commande": "play_until", "parametres": {"moment": "regime_permanent"}},
                {"mot": "un virgule huit fois dix puissance moins quatre joule", "repere": "resultat"},
                {"mot": "un virgule huit fois dix puissance moins quatre joule", "cible": "centre:1"}]),
    diapo_sim("ex_p6", "Question 6 : la date t₁", "e^(−t₁/τ) = 0,25 ⇒ t₁ = τ·ln4 ≈ 27,7 ms, entre τ et 5τ.",
      SIMD + "courbe-charge.html?vue=tableau", "R = 2 kΩ, C = 10 µF, E = 8 V : 0,63·E à τ, presque E à 5τ",
      "شوف le tableau ديال les valeurs، مع E égale huit volts و tau égale vingt millisecondes. فt égale tau، u C égale zéro virgule soixante-trois fois E، cinq virgule zéro quatre volts. à cinq tau، u C presque égale à E. حنا u C de t un égale six volts، يعني zéro virgule soixante-quinze fois E: بيناتهم. الحساب: un moins exponentielle égale six sur huit، إذن exponentielle de moins t un sur tau égale zéro virgule vingt-cinq. t un égale tau fois ln quatre، environ vingt-sept virgule sept millisecondes: كبر من tau و صغر بزاف من cinq tau. النتيجة معقولة.",
      centre=[("e^(−t₁/τ) = 1 − 6/8 = 0,25", "exponentielle de moins t un sur tau égale zéro virgule vingt-cinq"), ("t₁ = τ·ln4 ≈ 27,7 ms", "environ vingt-sept virgule sept millisecondes")],
      pointage=[avec({"commande": "set_parameters", "parametres": {"R_ohm": 2000, "C_uF": 10, "E": 8}}, "شوف le tableau ديال les valeurs"),
                {"mot": "مع E égale huit volts", "commande": "play_until", "parametres": {"moment": "tableau_valeurs"}},
                {"mot": "cinq virgule zéro quatre volts", "repere": "point_tau"},
                {"mot": "à cinq tau", "commande": "play_until", "parametres": {"moment": "cinq_tau"}},
                {"mot": "exponentielle de moins t un sur tau égale zéro virgule vingt-cinq", "cible": "centre:0"},
                {"mot": "environ vingt-sept virgule sept millisecondes", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_p1", "Plus facile : la pente de la droite", "سؤال ساهل على la pente.",
      "On écrit du_C/dt = a·u_C + b. Pendant la charge, la pente a vaut…",
      ["1/(R·C)", "E/(R·C)", "−1/(R·C)"], 2, {
        "2": {"juste": rep("مزيان! la pente سالبة: moins un sur R C. la droite كتهبط.", "Juste : a = −1/(R·C) < 0, la droite descend.")},
        "0": {"1": rep("قريب. ولكن ملي دوزنا u C لليمين، تبدل le signe. عاود اختار.", "En passant u_C à droite, son signe change. Réessaie."),
              "2": rep("الجواب هو moins un sur R C. ملي u C كتكبر، la dérivée كتصغر.", "Réponse : −1/(R·C) ; quand u_C augmente, la dérivée diminue.")},
        "1": {"1": rep("ما تقلقش. E sur R C ما فيهاش u C: هادي l'ordonnée à l'origine. عاود اختار.", "E/(R·C) ne multiplie pas u_C : c'est l'ordonnée à l'origine. Réessaie."),
              "2": rep("الجواب هو moins un sur R C. و E sur R C هي l'ordonnée à l'origine.", "Réponse : a = −1/(R·C) ; b = E/(R·C).")}},
      "On écrit dé u C sur dé t égale a fois u C plus b. La pente a vaut ?"),
    qcm_facile("fa_p2", "Plus facile : où la droite coupe l'axe", "سؤال ساهل على la droite.",
      "La droite du_C/dt = f(u_C) coupe l'axe des u_C (du_C/dt = 0) au point u_C = …",
      ["E", "0", "E/(R·C)"], 0, {
        "0": {"juste": rep("برافو! ملي dé u C sur dé t égale zéro، la charge سالات، و u C égale E.", "Juste : du_C/dt = 0 en fin de charge, u_C = E.")},
        "1": {"1": rep("ما تقلقش. فu C égale zéro، la dérivée كبيرة: هادي l'ordonnée à l'origine. عاود اختار.", "Pour u_C = 0 la dérivée est maximale (ordonnée à l'origine). Réessaie."),
              "2": rep("الجواب هو E. la dérivée كتولي zéro فآخر la charge، فين u C égale E.", "Réponse : u_C = E (fin de charge).")},
        "2": {"1": rep("قريب. E sur R C هي volts par seconde، ماشي volts. عاود اختار.", "E/(R·C) est en V/s, pas en V. Réessaie."),
              "2": rep("الجواب هو E. E sur R C هي l'ordonnée à l'origine.", "Réponse : u_C = E ; E/(R·C) est l'ordonnée à l'origine.")}},
      "La droite coupe l'axe des u C au point u C égale quoi ?"),
    qcm_facile("fa_p3", "Plus facile : deux condensateurs en parallèle", "سؤال ساهل على le parallèle.",
      "Deux condensateurs identiques C₀ = 5 µF sont montés en parallèle. La capacité équivalente vaut…",
      ["2,5 µF", "10 µF", "25 µF"], 1, {
        "1": {"juste": rep("مزيان! en parallèle les capacités كيتزادو: cinq plus cinq، dix microfarads.", "Juste : C = C₀ + C₀ = 10 µF.")},
        "0": {"1": rep("ما تقلقش. هادي ديال la série. en parallèle، la capacité كتكبر. عاود اختار.", "2,5 µF, c'est le montage en série ; en parallèle la capacité augmente. Réessaie."),
              "2": rep("الجواب هو dix microfarads. en parallèle، C équivalente égale C un plus C deux.", "Réponse : 10 µF (C_eq = C₁ + C₂).")},
        "2": {"1": rep("قريب. ضربتي les capacités. en parallèle كنجمعوهم. عاود اختار.", "Tu as multiplié ; en parallèle on additionne. Réessaie."),
              "2": rep("الجواب هو dix microfarads: cinq plus cinq.", "Réponse : 5 + 5 = 10 µF.")}},
      "Deux condensateurs de cinq microfarads en parallèle. La capacité équivalente vaut ?"),
    qcm_facile("fa_p4", "Plus facile : l'énergie maximale", "سؤال ساهل على l'énergie.",
      "C = 10 µF chargé sous E = 8 V. L'énergie maximale vaut…",
      ["6,4·10⁻⁴ J", "4·10⁻⁵ J", "3,2·10⁻⁴ J"], 2, {
        "2": {"juste": rep("برافو! un demi fois dix puissance moins cinq، fois soixante-quatre، كتعطي trois virgule deux fois dix puissance moins quatre joule.", "Juste : ½ × 10⁻⁵ × 64 = 3,2·10⁻⁴ J.")},
        "0": {"1": rep("قريب. نسيتي un demi. عاود اختار.", "Tu as oublié le facteur ½. Réessaie."),
              "2": rep("الجواب هو trois virgule deux fois dix puissance moins quatre joule. E e égale un demi C E au carré.", "Réponse : E_e = ½·C·E² = 3,2·10⁻⁴ J.")},
        "1": {"1": rep("ما تقلقش. نسيتي le carré ديال E. عاود اختار.", "Tu as oublié le carré de E. Réessaie."),
              "2": rep("الجواب هو trois virgule deux fois dix puissance moins quatre joule. huit au carré égale soixante-quatre.", "Réponse : 3,2·10⁻⁴ J (8² = 64).")}},
      "C égale dix microfarads، E égale huit volts. L'énergie maximale vaut ?"),
    vrai_faux_facile("fa_p5", "Plus facile : vrai ou faux", "سؤال ساهل على l'énergie و u C.",
      "u_C passe de 8 V (valeur finale) à 6 V.",
      [("Avec u_C = 6 V au lieu de 8 V, l'énergie est multipliée par (6/8)² ≈ 0,56.", True, "E_e est proportionnelle à u_C² : (0,75)² ≈ 0,56."),
       ("Avec u_C = 6 V au lieu de 8 V, l'énergie vaut 75 % de l'énergie maximale.", False, "Non : à cause du carré, c'est environ 56 %."),
       ("Si du_C/dt = 100 V/s et τ = 20 ms, alors u_C = E − 2 V.", True, "u_C = E − τ·du_C/dt = E − 0,02 × 100 = E − 2 V.")]),
    qcm_facile("fa_p6", "Plus facile : situer une date", "سؤال ساهل: فين كتجي t un؟",
      "Pendant la charge, u_C(t₁) = 0,75·E. La date t₁ est…",
      ["plus petite que τ", "entre τ et 5τ", "plus grande que 5τ"], 1, {
        "1": {"juste": rep("مزيان! فtau، u C égale zéro virgule soixante-trois E، و à cinq tau تقريبا E. zéro virgule soixante-quinze بيناتهم.", "Juste : 0,63·E (à τ) < 0,75·E < 0,99·E (à 5τ).")},
        "0": {"1": rep("ما تقلقش. فtau، u C وصلات غير zéro virgule soixante-trois E. واش zéro virgule soixante-quinze قبل ولا من بعد؟ عاود اختار.", "À τ, u_C = 0,63·E seulement ; 0,75·E vient avant ou après ? Réessaie."),
              "2": rep("الجواب: entre tau و cinq tau، حيت u C كتطلع ديما.", "Réponse : entre τ et 5τ (u_C est croissante).")},
        "2": {"1": rep("قريب. من بعد cinq tau، u C presque égale E، يعني كبر من zéro virgule soixante-quinze E. عاود اختار.", "Après 5τ, u_C ≈ E, déjà plus que 0,75·E. Réessaie."),
              "2": rep("الجواب: entre tau و cinq tau. t un égale tau fois ln quatre، environ un virgule quatre tau.", "Réponse : entre τ et 5τ (t₁ = τ·ln4 ≈ 1,4τ).")}},
      "Pendant la charge، u C de t un égale zéro virgule soixante-quinze fois E. La date t un est où ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage (figure 1) avec R = 5 kΩ et deux condensateurs identiques C₀ en parallèle ; E et C₀ sont inconnues. La figure 2 donne du_C/dt en fonction de u_C pendant la charge.",
      "intro_dit": "نفس التمرين، بقيم أخرى. R égale cinq kiloohms، و deux condensateurs identiques en parallèle. la figure deux كتعطي dé u C sur dé t en fonction de u C.",
      "figures": [droite(6, 200, 7.5, 25, "Figure 2 : du_C/dt en fonction de u_C")],
      "donnees": ["R = 5 kΩ = 5·10³ Ω"],
      "questions": [
        question_semblable("1", "Établir l'équation différentielle, puis montrer que du_C/dt = −(1/(R·C))·u_C + E/(R·C).",
          phrase(ED_ATT), ["u_R + u_C = E", "diviser par R·C"], ["du_C/dt = (1/(R·C))·u_C"],
          corr([("1 : R·C·du_C/dt + u_C = E", "R C dé u C sur dé t، plus u C، égale E"), ("du_C/dt = −(1/(R·C))·u_C + E/(R·C)", "moins un sur R C fois u C")],
               "R C dé u C sur dé t، plus u C، égale E. كنقسمو على R C: dé u C sur dé t égale moins un sur R C fois u C، plus E sur R C.")),
        question_semblable("2", "Déterminer E, puis τ (en ms).",
          valeur("τ", 30, "ms", "E = 6 V ; E/(R·C) = 200 V/s ; τ = 6/200 = 0,03 s = 30 ms"), ["du_C/dt = 0 ⇒ u_C = E", "ordonnée E/(R·C)"], ["τ = 200 s"],
          corr([("2 : la droite coupe l'axe en E = 6 V ; ordonnée 200 V/s", "E égale six volts"), ("τ = E/200 = 0,03 s = 30 ms", "tau égale trente millisecondes")],
               "E égale six volts، و l'ordonnée deux cents volts par seconde. tau égale six sur deux cents، يعني tau égale trente millisecondes.")),
        question_semblable("3", "En déduire C, puis C₀.",
          valeur("C₀", 3e-6, "F", "C = τ/R = 0,03/(5·10³) = 6·10⁻⁶ F ; C₀ = C/2 = 3·10⁻⁶ F"), ["C = τ/R", "C = 2·C₀"], ["C₀ = 2·C"],
          corr([("3 : C = 0,03/(5·10³) = 6·10⁻⁶ F", "six microfarads"), ("C₀ = C/2 = 3·10⁻⁶ F", "C zéro égale trois microfarads")],
               "C égale tau sur R، six microfarads. en parallèle C égale deux C zéro، إذن C zéro égale trois microfarads.")),
        question_semblable("4", "Calculer l'énergie maximale emmagasinée.",
          valeur("E_e,max", 1.08e-4, "J", "E_e,max = ½ × 6·10⁻⁶ × 6² = 1,08·10⁻⁴ J"), ["E_e = ½·C·E²"], ["E_e = ½·C₀·E²"],
          corr([("4 : E_e,max = ½·C·E²", "un demi C E au carré"), ("= ½ × 6·10⁻⁶ × 36 = 1,08·10⁻⁴ J", "un virgule zéro huit fois dix puissance moins quatre joule")],
               "E e max égale un demi C E au carré، un demi fois six fois dix puissance moins six، fois trente-six: un virgule zéro huit fois dix puissance moins quatre joule.")),
        question_semblable("5", "À t₁, du_C/dt = 50 V/s. Déterminer u_C(t₁) puis E_e(t₁).",
          valeur("E_e(t₁)", 6.08e-5, "J", "u_C = E − τ·(du_C/dt) = 6 − 0,03 × 50 = 4,5 V ; E_e = ½ × 6·10⁻⁶ × 4,5² ≈ 6,08·10⁻⁵ J"), ["u_C = E − τ·du_C/dt", "E_e = ½·C·u_C²"], ["u_C = 50·τ"],
          corr([("5 : u_C(t₁) = 6 − 0,03 × 50 = 4,5 V", "quatre virgule cinq volts"), ("E_e = ½ × 6·10⁻⁶ × 4,5² ≈ 6,08·10⁻⁵ J", "six virgule zéro huit fois dix puissance moins cinq joule")],
               "u C égale six moins zéro virgule zéro trois fois cinquante، quatre virgule cinq volts. E e environ six virgule zéro huit fois dix puissance moins cinq joule.")),
        question_semblable("6", "Calculer t₁ (en ms) et le situer par rapport à τ et 5τ.",
          valeur("t₁", 41.6, "ms", "e^(−t₁/τ) = 1 − 4,5/6 = 0,25 ; t₁ = τ·ln4 = 30 × 1,386 ≈ 41,6 ms (entre τ et 5τ)"), ["ln", "t₁ = τ·ln(E/(E − u_C))"], ["t₁ = τ·ln0,75"],
          corr([("6 : e^(−t₁/τ) = 0,25, t₁ = τ·ln4", "tau fois ln quatre"), ("t₁ ≈ 41,6 ms, entre τ et 5τ", "quarante et un virgule six millisecondes")],
               "exponentielle de moins t un sur tau égale zéro virgule vingt-cinq، t un égale tau fois ln quatre، environ quarante et un virgule six millisecondes، entre tau و cinq tau.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
