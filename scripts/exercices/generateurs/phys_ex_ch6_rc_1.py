# Exercice de physique, ch. 6 (dipôle RC), niveau facile n° 1 : la charge d'un condensateur sous un échelon de tension.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RC.json : cas_types « τ graphique » et « calcul de C ou R »,
#    pièges « projeter 0,63·E sur la tangente », « oublier de convertir µF », « lire l'unité de l'axe » ;
#    erreurs_examen « τ graphique » (charge → 0,63 ; projeter sur la courbe), « résultat sans unité ».
#  - nationaux : 2016 N, 2019 N, 2021 N, 2022 N (exam.json) : « déterminer graphiquement τ », « calculer C » ;
#    ici seulement les gestes un à un (niveau facile).
#  - séries en ligne (talamidi, moutamadris, alloschool, dyrassa, sigmaprof : séries « dipôle RC », exercices 1-2 de
#    charge sous E = 6 à 12 V) : données habituelles R ~ kΩ, C ~ 100 µF, τ ~ 0,1 s ; nos données sont celles de la
#    simulation du cours (E = 12 V, R = 1 kΩ, C = 220 µF), pour que l'explication montre les mêmes valeurs.
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch6_rc_1"
SIMD = "/media/simulations/physics/dipole-rc-tableau/"


def montage(titre):
    """Montage de charge : générateur E, interrupteur K, conducteur ohmique R, condensateur C, en série."""
    return schema(titre, 8, 4.4,
        dipole([1, 0.8], [1, 3.6], "G", "E", pos="o"),
        fil([1, 3.6], [2, 3.6]),
        dipole([2, 3.6], [4, 3.6], "K", "K"),
        dipole([4, 3.6], [6.6, 3.6], "R", "R"),
        fil([6.6, 3.6], [7, 3.6]),
        dipole([7, 3.6], [7, 0.8], "C", "C", pos="o"),
        fil([7, 0.8], [1, 0.8]),
        courant([3.2, 0.8], "g"),
        tension([7.6, 1.4], [7.6, 3.0], "u_C", pos="e"),
        borne([7, 3.6], "A", "n"), borne([7, 0.8], "B", "s"))


def charge(E, tau, tmax, titre, grad_t):
    return figure_courbe(titre, axe("t", 0, tmax, "s", grad_t), axe("u_C", 0, E * 1.2, "V", list(range(0, int(E * 1.2) + 1, 2))),
        [{"f": "courbe", "expr": f"{E}*(1-exp(-x/{tau}))", "couleur": "orange", "texte": "u_C(t)", "texte_x": tmax * 0.8},
         {"f": "repere", "y": E, "couleur": "faible"}],
        legende="Courbe enregistrée après la fermeture de K à t = 0.")


E, R, C = 12, 1e3, 220e-6
TAU = R * C                      # 0,22 s
U63 = 0.63 * E                   # 7,56 V
assert abs(TAU - 0.22) < 1e-12 and abs(U63 - 7.56) < 1e-12

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RC", "cours": "phys_ch6_dipole_RC",
  "titre": "Charger un condensateur : calculer et lire τ", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer la constante de temps τ = R·C", "Lire τ sur la courbe u_C(t) par la méthode des 63 %", "Reconnaître le régime permanent (t ≈ 5τ)"],
  "enonce": {
    "intro": "On réalise le montage de la figure 1 : un générateur idéal de tension de force électromotrice E, un interrupteur K, un conducteur ohmique de résistance R et un condensateur de capacité C, initialement déchargé. À la date t = 0, on ferme K. Un système d'acquisition enregistre la tension u_C(t) aux bornes du condensateur (figure 2).",
    "intro_dit": "دابا نقراو l'énoncé. عندنا le montage ديال la figure un: un générateur idéal de tension، la force électromotrice ديالو E، l'interrupteur K، un conducteur ohmique، la résistance ديالو R، و un condensateur، la capacité ديالو C، وفالبداية déchargé. فt égale zéro، كنسدو K. ونسجلو la tension u C ديال le condensateur، وهي la figure deux.",
    "figures": [montage("Figure 1 : le montage"),
                charge(E, TAU, 1.4, "Figure 2 : la tension u_C(t)", [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])],
    "donnees": ["E = 12 V", "R = 1 kΩ = 10³ Ω", "C = 220 µF = 220·10⁻⁶ F"],
    "questions": [
      question("1", "Calculer la constante de temps τ du dipôle RC.",
        "السؤال un: حسب la constante de temps tau ديال le dipôle RC.",
        valeur("τ", 0.22, "s", "τ = R·C = 10³ × 220·10⁻⁶ = 0,22 s"),
        ["τ = R·C", "10³", "10⁻⁶", "µF", "s"], ["τ = R/C", "τ = 10³ × 220 = 220 000 s"],
        [aide("Quels sont les deux dipôles qui fixent la durée de la charge ? Écris leurs valeurs en unités du système international (Ω et F).",
              "شوف شنو هوما les deux dipôles اللي كيحددو la durée ديال la charge. كتب R بl'ohm، وC بle farad: un microfarad هو dix puissance moins six farad."),
         aide("La constante de temps est le produit de R par C : τ = R·C. Remplace R par 10³ Ω et C par 220·10⁻⁶ F.",
              "la constante de temps هي R fois C. إذن tau égale R fois C. عوض R ب dix puissance trois ohm، وC ب deux cent vingt fois dix puissance moins six farad.")],
        corr([("1 : τ = R·C", "tau égale R fois C"),
              ("A.N. : τ = 10³ × 220·10⁻⁶", "dix puissance trois fois deux cent vingt"),
              ("τ = 0,22 s", "tau égale zéro virgule vingt-deux seconde")],
             "السؤال un. tau égale R fois C. l'application numérique: dix puissance trois fois deux cent vingt fois dix puissance moins six. tau égale zéro virgule vingt-deux seconde."),
        "ex_rc1", "fa_rc1"),
      question("2", "Calculer la valeur de u_C à la date t = τ, puis expliquer comment on vérifie τ sur la courbe de la figure 2.",
        "السؤال deux: حسب la valeur ديال u C فt égale tau، ومن بعد شرح كيفاش نتأكدو من tau على la courbe ديال la figure deux.",
        valeur("u_C(τ)", 7.56, "V", "u_C(τ) = 0,63·E = 0,63 × 12 = 7,56 V"),
        ["u_C(τ) = 0,63·E", "E", "V", "projeter sur la courbe"], ["u_C(τ) = 0,37·E", "projeter sur la tangente"],
        [aide("À la date τ, le condensateur a atteint 63 % de sa tension finale. Quelle est la tension finale u_C quand la charge est finie ?",
              "فt égale tau، le condensateur وصل à soixante-trois pour cent من la tension النهائية ديالو. شحال هي la tension النهائية ملي كتسالي la charge؟"),
         aide("u_C(τ) = 0,63·E. Ensuite, sur la figure 2 : horizontale à cette valeur jusqu'à la courbe, puis verticale vers l'axe des temps.",
              "u C de tau égale zéro virgule soixante-trois fois E. من بعد، فla figure deux: كنرسمو خط أفقي من هاد la valeur حتى la courbe، ومن تما كنهبطو عمودي لl'axe des temps.")],
        corr([("2 : à t = τ, u_C(τ) = 0,63·E", "u C de tau égale zéro virgule soixante-trois fois E"),
              ("A.N. : u_C(τ) = 0,63 × 12 = 7,56 V", "sept virgule cinquante-six volts"),
              ("On trace l'horizontale u_C = 7,56 V jusqu'à la courbe, puis on descend sur l'axe des temps : on lit τ ≈ 0,22 s.", "كنقراو tau environ zéro virgule vingt-deux seconde")],
             "السؤال deux. فt égale tau، u C de tau égale zéro virgule soixante-trois fois E. يعني zéro virgule soixante-trois fois douze، كتعطي sept virgule cinquante-six volts. من بعد، كنرسمو الخط الأفقي حتى la courbe، ومن بعد كنهبطو لl'axe des temps: كنقراو tau environ zéro virgule vingt-deux seconde."),
        "ex_rc2", "fa_rc2"),
      question("3", "Au bout de combien de temps peut-on considérer que le condensateur est chargé (régime permanent) ? Calculer cette durée.",
        "السؤال trois: من بعد شحال ديال الوقت نقدرو نقولو le condensateur تشارجا، يعني le régime permanent؟ حسب هاد la durée.",
        valeur("t", 1.1, "s", "t ≈ 5τ = 5 × 0,22 = 1,1 s"),
        ["t ≈ 5τ", "τ", "régime permanent", "s"], ["t = τ", "t = 0,63·τ"],
        [aide("À t = τ, u_C n'a atteint que 63 % de E. Regarde la figure 2 : à partir de quelle date la courbe devient-elle presque horizontale ?",
              "فt égale tau، u C وصلات غير à soixante-trois pour cent من E. شوف la figure deux: من أي وقت la courbe كتولي تقريبا أفقية؟"),
         aide("On admet que le régime permanent est atteint à t ≈ 5τ (u_C ≈ 0,99·E). Multiplie τ par 5.",
              "كنقبلو بلي le régime permanent كيبدا تقريبا à cinq tau، فين u C كتوصل à zéro virgule quatre-vingt-dix-neuf fois E. إذن t égale cinq fois tau.")],
        corr([("3 : le régime permanent est atteint pour t ≈ 5τ", "le régime permanent كيبدا à cinq tau"),
              ("A.N. : t ≈ 5 × 0,22", "cinq fois zéro virgule vingt-deux"),
              ("t ≈ 1,1 s : après 1,1 s, u_C ≈ E = 12 V.", "un virgule un seconde")],
             "السؤال trois. le régime permanent كيبدا à cinq tau. يعني cinq fois zéro virgule vingt-deux، كتعطي un virgule un seconde. من بعد هاد la durée، u C presque égale à E، يعني douze volts."),
        "ex_rc3", "fa_rc3"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_rc1", "Question 1 : τ = R·C", "τ = R·C : avec R = 1 kΩ et C = 220 µF, τ = 0,22 s.",
      SIMD + "tau-rc.html", "Le circuit E, K, R, C et la charge : τ s'écrit là où u_C atteint 63 % de E",
      "شوف le circuit: le générateur، l'interrupteur K، la résistance R، وle condensateur C. شوف la courbe ديال la charge: u C كتطلع وكتمشي نحو E. هنا R égale un kiloohm، وC égale deux cent vingt microfarads. la constante de temps هي tau égale R fois C. نكتبو كلشي بl'unité internationale: dix puissance trois ohm، و deux cent vingt fois dix puissance moins six farad. إذن tau égale zéro virgule vingt-deux seconde.",
      centre=[("τ = R·C", "la constante de temps هي tau égale R fois C"), ("τ = 10³ × 220·10⁻⁶ = 0,22 s", "إذن tau égale zéro virgule vingt-deux seconde")],
      pointage=[{"mot": "شوف la courbe ديال la charge", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "R égale un kiloohm", "repere": "R"},
                {"mot": "C égale deux cent vingt microfarads", "repere": "C"},
                {"mot": "la constante de temps هي tau égale R fois C", "cible": "centre:0"},
                {"mot": "إذن tau égale zéro virgule vingt-deux seconde", "cible": "centre:1"}]),
    diapo_sim("ex_rc2", "Question 2 : la méthode des 63 %", "u_C(τ) = 0,63·E = 7,56 V : horizontale jusqu'à la courbe, puis verticale : τ ≈ 0,22 s.",
      SIMD + "courbe-charge.html?vue=pourcent", "0,63·E : l'horizontale jusqu'à la courbe, puis la verticale",
      "شوف la courbe ديال la charge، مع E égale douze volts. فt égale tau، u C كتوصل à zéro virgule soixante-trois fois E. يعني zéro virgule soixante-trois fois douze، sept virgule cinquante-six volts. كنرسمو الخط الأفقي ديال sept virgule cinquante-six volts حتى la courbe، ماشي حتى la tangente. ومن تما كنهبطو عمودي لl'axe des temps. كنقراو tau environ zéro virgule vingt-deux seconde، نفس القيمة ديال R fois C.",
      centre=[("u_C(τ) = 0,63·E = 0,63 × 12 = 7,56 V", "sept virgule cinquante-six volts"), ("on lit τ ≈ 0,22 s", "كنقراو tau environ zéro virgule vingt-deux seconde")],
      pointage=[{"mot": "شوف la courbe ديال la charge", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "sept virgule cinquante-six volts", "cible": "centre:0"},
                {"mot": "كنرسمو الخط الأفقي", "commande": "play_until", "parametres": {"moment": "ligne_63"}},
                {"mot": "كنهبطو عمودي", "commande": "play_until", "parametres": {"moment": "projection"}},
                {"mot": "كنقراو tau environ zéro virgule vingt-deux seconde", "cible": "centre:1"}]),
    diapo_sim("ex_rc3", "Question 3 : le régime permanent à 5τ", "À t ≈ 5τ = 1,1 s, u_C ≈ E : le condensateur est chargé.",
      SIMD + "courbe-charge.html?vue=tableau", "Trois valeurs : 0 à t = 0, 0,63·E à τ, presque E à 5τ",
      "شوف le tableau ديال les valeurs. فt égale zéro، u C égale zéro. فt égale tau، u C égale sept virgule cinquante-six volts. ومن بعد la courbe كتطلع بشوية بشوية. à cinq tau، u C presque égale à E: هادا هو le régime permanent. قبل منو، le régime transitoire. هنا، cinq fois zéro virgule vingt-deux كتعطي un virgule un seconde.",
      centre=[("t ≈ 5τ = 5 × 0,22 = 1,1 s", "cinq fois zéro virgule vingt-deux كتعطي un virgule un seconde")],
      pointage=[{"mot": "شوف le tableau ديال les valeurs", "commande": "play_until", "parametres": {"moment": "tableau_valeurs"}},
                {"mot": "ومن بعد la courbe كتطلع", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "à cinq tau", "commande": "play_until", "parametres": {"moment": "cinq_tau"}},
                {"mot": "cinq fois zéro virgule vingt-deux كتعطي un virgule un seconde", "cible": "centre:0"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_rc1", "Plus facile : la constante de temps", "نتمرنو بسؤال ساهل. اختار la bonne relation.",
      "Quelle relation donne la constante de temps d'un dipôle RC ?",
      ["τ = R·C", "τ = R/C", "τ = C/R"], 0, {
        "0": {"juste": rep("برافو! tau égale R fois C. وإلى كبر R ولا كبر C، la charge كتولي بطيئة.", "Juste : τ = R·C ; si R ou C augmente, la charge est plus lente.")},
        "1": {"1": rep("ما تقلقش. فكر: إلى كبرات la capacité C، le condensateur كيبغي وقت كتر باش يتشارجا. واش R sur C كتكبر ملي كتكبر C؟ عاود اختار.", "Si C augmente, la charge dure plus longtemps : τ doit augmenter avec C. Réessaie."),
              "2": rep("الجواب هو tau égale R fois C. R وC بجوج كيطولو la charge، إذن بجوج كيضربو.", "Réponse : τ = R·C (R et C ralentissent tous les deux la charge).")},
        "2": {"1": rep("قريب. ولكن إلى كبرات la résistance R، le courant كيصغر وla charge كتطول. واش C sur R كتكبر ملي كيكبر R؟ عاود اختار.", "Si R augmente, la charge est plus lente : τ doit augmenter avec R. Réessaie."),
              "2": rep("الجواب هو tau égale R fois C. R وC بجوج كيضربو.", "Réponse : τ = R·C.")}},
      "Quelle relation donne la constante de temps d'un dipôle RC ?"),
    qcm_facile("fa_rc2", "Plus facile : la tension à t = τ", "سؤال ساهل على la méthode ديال soixante-trois pour cent.",
      "Charge sous E = 12 V. À la date t = τ, la tension u_C vaut…",
      ["7,56 V", "4,44 V", "12 V"], 0, {
        "0": {"juste": rep("برافو! zéro virgule soixante-trois fois douze كتعطي sept virgule cinquante-six volts.", "Juste : u_C(τ) = 0,63 × 12 = 7,56 V.")},
        "1": {"1": rep("ما تقلقش. quatre virgule quarante-quatre هي zéro virgule trente-sept fois E، وهادي ديال la décharge. فla charge، u C كتطلع: شحال وصلات فtau؟ عاود اختار.", "4,44 V = 0,37·E sert pour une décharge. En charge, u_C monte. Réessaie."),
              "2": rep("الجواب هو sept virgule cinquante-six volts. فla charge، u C de tau égale zéro virgule soixante-trois fois E.", "Réponse : u_C(τ) = 0,63·E = 7,56 V (0,37·E, c'est pour une décharge).")},
        "2": {"1": rep("لا، douze volts هي la valeur النهائية، كتوصل ليها u C تقريبا à cinq tau، ماشي فtau. عاود اختار.", "12 V est la valeur finale, atteinte vers 5τ, pas à τ. Réessaie."),
              "2": rep("الجواب هو sept virgule cinquante-six volts. فtau، u C مازال ما وصلاتش لE: وصلات غير à soixante-trois pour cent.", "Réponse : 7,56 V ; à τ, u_C n'est qu'à 63 % de E.")}},
      "Charge sous E égale douze volts. À la date t égale tau, la tension u C vaut ?"),
    vrai_faux_facile("fa_rc3", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
      "τ = 0,22 s et E = 12 V.",
      [("À t = 5τ = 1,1 s, on considère que le condensateur est chargé : u_C ≈ E.", True, "À 5τ, u_C ≈ 0,99·E : c'est le régime permanent."),
       ("À t = τ = 0,22 s, le condensateur est déjà complètement chargé.", False, "À τ, u_C n'est qu'à 63 % de E ; il faut attendre environ 5τ.")]),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage (figure 1) avec d'autres valeurs : E = 6 V, R = 2 kΩ, C = 100 µF. Le condensateur est initialement déchargé ; à t = 0, on ferme K.",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale six volts، R égale deux kiloohms، وC égale cent microfarads. فt égale zéro، كنسدو K.",
      "figures": [charge(6, 0.2, 1.4, "Figure 2 : la tension u_C(t)", [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])],
      "donnees": ["E = 6 V", "R = 2 kΩ = 2·10³ Ω", "C = 100 µF = 100·10⁻⁶ F"],
      "questions": [
        question_semblable("1", "Calculer la constante de temps τ du dipôle RC.",
          valeur("τ", 0.2, "s", "τ = R·C = 2·10³ × 100·10⁻⁶ = 0,2 s"), ["τ = R·C", "10³", "10⁻⁶", "s"], ["τ = R/C"],
          corr([("1 : τ = R·C = 2·10³ × 100·10⁻⁶", "tau égale R fois C"), ("τ = 0,2 s", "zéro virgule deux seconde")],
               "tau égale R fois C، يعني deux fois dix puissance trois، fois cent fois dix puissance moins six. tau égale zéro virgule deux seconde.")),
        question_semblable("2", "Calculer la valeur de u_C à la date t = τ, puis expliquer comment on vérifie τ sur la courbe.",
          valeur("u_C(τ)", 3.78, "V", "u_C(τ) = 0,63·E = 0,63 × 6 = 3,78 V"), ["u_C(τ) = 0,63·E", "V"], ["u_C(τ) = 0,37·E"],
          corr([("2 : u_C(τ) = 0,63·E = 0,63 × 6 = 3,78 V", "trois virgule soixante-dix-huit volts"),
                ("Horizontale à 3,78 V jusqu'à la courbe, puis verticale : τ ≈ 0,2 s.", "كنقراو tau environ zéro virgule deux seconde")],
               "u C de tau égale zéro virgule soixante-trois fois six، يعني trois virgule soixante-dix-huit volts. الخط الأفقي حتى la courbe، ومن بعد كنهبطو: كنقراو tau environ zéro virgule deux seconde.")),
        question_semblable("3", "Au bout de combien de temps le condensateur est-il chargé (régime permanent) ? Calculer cette durée.",
          valeur("t", 1.0, "s", "t ≈ 5τ = 5 × 0,2 = 1 s"), ["t ≈ 5τ", "s"], ["t = τ"],
          corr([("3 : t ≈ 5τ = 5 × 0,2", "cinq fois zéro virgule deux"), ("t ≈ 1 s", "un seconde")],
               "le régime permanent à cinq tau، يعني cinq fois zéro virgule deux، كتعطي un seconde.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
