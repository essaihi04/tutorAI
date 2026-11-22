# Exercice de physique, ch. 6 (dipôle RC), niveau facile n° 2 : charger un condensateur à courant constant.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RC.json : cas_type « generateur_courant » (q = I₀·t,
#    u_C = (I₀/C)·t, pente k → C = I₀/k), piège « I₀ = q/C » (Noureddine), erreurs_examen « C calculée avec un seul
#    point », redaction_nationale « generateur_courant » (2025 N).
#  - nationaux (backend/data/exams/physique) : 2018 N (q = f(u), générateur de courant), 2020 R, 2025 N (droite
#    u_C(t), pente 1 V/s, C = 1 µF) ; ici nos données (I₀ = 4 µA, pente 2 V/s), les gestes un à un (niveau facile).
#  - cours phys_ch6_dipole_RC : diapos rc_g1_generateur et rc_g2_pente (simulation generateur-courant.html :
#    points lus à 2 s et 6 s, paramètres I0_uA 1→10 et C_uF 0,5→5) ; nos valeurs y sont réglées (set_parameters).
#  - séries en ligne : recherche faite (Naceiri Mrabti « Série P6 dipôle RC », talamidi, moutamadris, alloschool) mais
#    pages non lisibles depuis cette session (domaines bloqués) : on s'appuie sur les sources du dépôt ci-dessus.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch6_rc_2"
SIM = "/media/simulations/physics/dipole-rc-tableau/generateur-courant.html"


def montage(titre):
    """Générateur idéal de courant I₀ (flèche vers le haut), interrupteur K, condensateur C ; A = armature du haut."""
    return schema(titre, 7, 4.4,
        dipole([1, 0.8], [1, 3.6], "I", "I₀", pos="o"),
        fil([1, 3.6], [2, 3.6]),
        dipole([2, 3.6], [4, 3.6], "K", "K"),
        fil([4, 3.6], [5.6, 3.6]),
        dipole([5.6, 3.6], [5.6, 0.8], "C", "C", pos="o"),
        fil([5.6, 0.8], [1, 0.8]),
        courant([4.9, 3.6], "d", "I₀"),
        tension([6.2, 1.4], [6.2, 3.0], "u_C", pos="e"),
        borne([5.6, 3.6], "A", "n"), borne([5.6, 0.8], "B", "s"))


def droite(I0_uA, C_uF, titre):
    k = I0_uA / C_uF                       # V/s
    umax = k * 10
    pas = 2 if umax <= 20 else 5
    return figure_courbe(titre, axe("t", 0, 11, "s", list(range(0, 11))),
        axe("u_C", 0, umax, "V", list(range(0, int(umax) + 1, pas))),
        [{"f": "courbe", "expr": f"{k}*x", "de": 0, "a": 10, "couleur": "orange", "texte": "u_C(t)", "texte_x": 7, "pos": "no"},
         {"f": "repere", "x": 2, "y": 2 * k}, {"f": "repere", "x": 6, "y": 6 * k}],
        legende="Tension u_C(t) enregistrée après la fermeture de K à t = 0.")


I0, C = 4e-6, 2e-6
Q6 = I0 * 6                      # 2,4·10⁻⁵ C
K = (6 * I0 / C - 2 * I0 / C) / (6 - 2)   # 2 V/s
assert abs(Q6 - 2.4e-5) < 1e-15 and abs(K - 2) < 1e-12 and abs(I0 / K - 2e-6) < 1e-15
# semblable : I₀ = 6 µA, C = 2 µF → k = 3 V/s ; q(6 s) = 3,6·10⁻⁵ C
assert abs(6e-6 * 6 - 3.6e-5) < 1e-15 and abs(6e-6 / 3 - 2e-6) < 1e-15

SET = {"mot": None, "commande": "set_parameters", "parametres": {"I0_uA": 4, "C_uF": 2}}
def regler(mot):
    d = dict(SET); d["mot"] = mot; return d

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RC", "cours": "phys_ch6_dipole_RC",
  "titre": "Charger un condensateur à courant constant", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Exprimer la charge q = I₀·t d'un condensateur chargé à courant constant",
                  "Calculer la pente d'une droite à partir de deux points lus",
                  "Déduire la capacité C = I₀/k"],
  "enonce": {
    "intro": "Pour déterminer la capacité C d'un condensateur initialement déchargé, on réalise le montage de la figure 1 : un générateur idéal de courant débite un courant d'intensité constante I₀ = 4 µA. À la date t = 0, on ferme l'interrupteur K. Un système d'acquisition enregistre la tension u_C(t) aux bornes du condensateur (figure 2).",
    "intro_dit": "دابا نقراو l'énoncé. بغينا نعرفو la capacité C ديال un condensateur، وفالبداية déchargé. عندنا le montage ديال la figure un: un générateur idéal de courant، كيعطي un courant ثابت، l'intensité ديالو I zéro égale quatre microampères. فt égale zéro، كنسدو l'interrupteur K. ونسجلو la tension u C ديال le condensateur، وهي la figure deux.",
    "figures": [montage("Figure 1 : le montage"), droite(4, 2, "Figure 2 : la tension u_C(t)")],
    "donnees": ["I₀ = 4 µA = 4·10⁻⁶ A", "Le condensateur est déchargé à t = 0."],
    "questions": [
      question("1", "Exprimer la charge q du condensateur en fonction de I₀ et de t, puis calculer q à la date t = 6 s.",
        "السؤال un: عبر على la charge q ديال le condensateur en fonction de I zéro و t، ومن بعد حسب q فt égale six secondes.",
        valeur("q", 2.4e-5, "C", "q = I₀·t = 4·10⁻⁶ × 6 = 2,4·10⁻⁵ C"),
        ["q = I₀·t", "10⁻⁶", "µA", "C (coulomb)"], ["q = I₀/t", "q = I₀/C", "q = 4 × 6 = 24 C"],
        [aide("L'intensité est constante : à chaque seconde, la même quantité de charge arrive sur l'armature A. Que vaut la charge après t secondes ?",
              "l'intensité ثابتة: فكل seconde، نفس la quantité ديال la charge كتوصل لl'armature A. شحال كتولي la charge من بعد t secondes؟"),
         aide("Pour un courant constant : q = I₀·t. Écris I₀ en ampères (1 µA = 10⁻⁶ A), puis multiplie par t = 6 s.",
              "ملي le courant ثابت، q égale I zéro fois t. كتب I zéro بl'ampère: un microampère égale dix puissance moins six ampère. ومن بعد ضرب fois six secondes.")],
        corr([("1 : le courant est constant, donc q = I₀·t", "q égale I zéro fois t"),
              ("A.N. : q = 4·10⁻⁶ × 6", "quatre fois dix puissance moins six، fois six"),
              ("q = 2,4·10⁻⁵ C", "deux virgule quatre fois dix puissance moins cinq coulomb")],
             "السؤال un. le courant ثابت، إذن q égale I zéro fois t. l'application numérique: quatre fois dix puissance moins six، fois six. q égale deux virgule quatre fois dix puissance moins cinq coulomb."),
        "ex_g1", "fa_g1"),
      question("2", "Déterminer graphiquement la pente k de la droite u_C = f(t) de la figure 2.",
        "السؤال deux: حدد مبيانيا la pente k ديال la droite u C en fonction de t، فla figure deux.",
        valeur("k", 2, "V/s", "k = Δu_C/Δt = (12 − 4)/(6 − 2) = 2 V/s"),
        ["k = Δu_C/Δt", "deux points éloignés", "V/s"], ["k = Δt/Δu_C", "k = 12/4"],
        [aide("Choisis deux points de la droite, bien éloignés et faciles à lire : par exemple à t = 2 s et à t = 6 s. Lis u_C pour chacun.",
              "ختار deux points ديال la droite، بعاد على بعضهم وساهلين فالقراءة: مثلا t égale deux secondes و t égale six secondes. قرا u C ديال كل point."),
         aide("La pente est k = Δu_C/Δt : la différence des tensions divisée par la différence des dates.",
              "la pente هي k égale delta u C sur delta t: الفرق ديال les tensions، sur الفرق ديال les dates.")],
        corr([("2 : on lit (2 s ; 4 V) et (6 s ; 12 V) sur la droite", "deux secondes، quatre volts"),
              ("k = Δu_C/Δt = (12 − 4)/(6 − 2)", "k égale delta u C sur delta t"),
              ("k = 2 V/s", "k égale deux volts par seconde")],
             "السؤال deux. كنقراو deux points: deux secondes، quatre volts، و six secondes، douze volts. k égale delta u C sur delta t، يعني douze moins quatre، sur six moins deux. k égale deux volts par seconde."),
        "ex_g2", "fa_g2"),
      question("3", "Sachant que q = C·u_C, montrer que u_C = (I₀/C)·t, puis en déduire la valeur de la capacité C.",
        "السؤال trois: عارفين بلي q égale C fois u C. بين بلي u C égale I zéro sur C، fois t، ومن بعد استنتج la valeur ديال la capacité C.",
        valeur("C", 2e-6, "F", "u_C = q/C = (I₀/C)·t, donc k = I₀/C et C = I₀/k = 4·10⁻⁶/2 = 2·10⁻⁶ F"),
        ["q = C·u_C", "q = I₀·t", "k = I₀/C", "C = I₀/k", "F", "µF"], ["C = k/I₀", "C = I₀·k", "C = q/t"],
        [aide("Tu as deux expressions de la charge : q = C·u_C et q = I₀·t. Égale-les, puis isole u_C.",
              "عندك deux expressions ديال la charge: q égale C fois u C، و q égale I zéro fois t. ساويهم، ومن بعد خلي u C بوحدها."),
         aide("u_C = (I₀/C)·t est une droite par l'origine de pente I₀/C. Donc I₀/C = k, et C = I₀/k.",
              "u C égale I zéro sur C، fois t: هادي droite كتدوز من l'origine، la pente ديالها I zéro sur C. إذن I zéro sur C égale k، و C égale I zéro sur k.")],
        corr([("3 : C·u_C = I₀·t, donc u_C = (I₀/C)·t : droite de pente k = I₀/C", "u C égale I zéro sur C، fois t"),
              ("C = I₀/k", "C égale I zéro sur k"),
              ("A.N. : C = 4·10⁻⁶/2 = 2·10⁻⁶ F = 2 µF", "deux fois dix puissance moins six farad")],
             "السؤال trois. C fois u C égale I zéro fois t، إذن u C égale I zéro sur C، fois t. هادي droite، la pente ديالها k égale I zéro sur C. إذن C égale I zéro sur k. l'application numérique: quatre fois dix puissance moins six، sur deux. C égale deux fois dix puissance moins six farad، يعني deux microfarads."),
        "ex_g3", "fa_g3"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_g1", "Question 1 : q = I₀·t", "Courant constant : q = I₀·t = 4·10⁻⁶ × 6 = 2,4·10⁻⁵ C.",
      SIM, "Le générateur de courant garde I₀ constant : la charge augmente régulièrement",
      "شوف الفوق: les deux générateurs. le générateur de tension كيعطي la tension E ثابتة. أما le générateur de courant، كيعطي l'intensité I zéro ثابتة. هنا، I zéro égale quatre microampères. هاد le courant كيشارجي le condensateur. ملي l'intensité ثابتة، la charge كتزاد بنفس السرعة: q égale I zéro fois t. فt égale six secondes، q égale quatre fois dix puissance moins six، fois six. يعني q égale deux virgule quatre fois dix puissance moins cinq coulomb.",
      centre=[("q = I₀·t", "q égale I zéro fois t"), ("q = 4·10⁻⁶ × 6 = 2,4·10⁻⁵ C", "يعني q égale deux virgule quatre fois dix puissance moins cinq coulomb")],
      pointage=[regler("شوف الفوق"),
                {"mot": "les deux générateurs", "commande": "play_until", "parametres": {"moment": "carte_generateurs"}},
                {"mot": "le générateur de tension كيعطي", "repere": "generateur_tension"},
                {"mot": "أما le générateur de courant", "repere": "generateur_courant"},
                {"mot": "هاد le courant كيشارجي le condensateur", "commande": "play_until", "parametres": {"moment": "droite"}},
                {"mot": "la charge كتزاد بنفس السرعة", "repere": "condensateur"},
                {"mot": "q égale I zéro fois t", "cible": "centre:0"},
                {"mot": "يعني q égale deux virgule quatre fois dix puissance moins cinq coulomb", "cible": "centre:1"}]),
    diapo_sim("ex_g2", "Question 2 : la pente de la droite", "Deux points éloignés : k = (12 − 4)/(6 − 2) = 2 V/s.",
      SIM, "Deux points lus sur la droite, puis la pente k = Δu_C/Δt",
      "شوف la droite ديال u C en fonction de t: كتدوز من l'origine. كناخدو deux points بعاد على بعضهم. le point un: t égale deux secondes، u C égale quatre volts. le point deux: t égale six secondes، u C égale douze volts. la pente هي k égale delta u C sur delta t. يعني douze moins quatre، sur six moins deux. huit sur quatre، كتعطي k égale deux volts par seconde.",
      centre=[("k = Δu_C/Δt", "k égale delta u C sur delta t"), ("k = (12 − 4)/(6 − 2) = 2 V/s", "كتعطي k égale deux volts par seconde")],
      pointage=[regler("شوف la droite"),
                {"mot": "كناخدو deux points", "commande": "play_until", "parametres": {"moment": "deux_points"}},
                {"mot": "le point un", "repere": "point_1"},
                {"mot": "le point deux", "repere": "point_2"},
                {"mot": "la pente هي", "commande": "play_until", "parametres": {"moment": "pente"}},
                {"mot": "k égale delta u C sur delta t", "cible": "centre:0"},
                {"mot": "كتعطي k égale deux volts par seconde", "cible": "centre:1"}]),
    diapo_sim("ex_g3", "Question 3 : C = I₀/k", "u_C = (I₀/C)·t : la pente vaut I₀/C, donc C = I₀/k = 2 µF.",
      SIM, "La pente de la droite donne la capacité : C = I₀/k",
      "عندنا deux relations. q égale C fois u C، و q égale I zéro fois t. إذن C fois u C égale I zéro fois t، يعني u C égale I zéro sur C، fois t. هادي هي la droite ديالنا، la pente ديالها k égale I zéro sur C. إذن C égale I zéro sur k. C égale quatre fois dix puissance moins six، sur deux. C égale deux fois dix puissance moins six farad، يعني deux microfarads.",
      centre=[("u_C = (I₀/C)·t", "يعني u C égale I zéro sur C، fois t"), ("C = I₀/k = 4·10⁻⁶/2 = 2·10⁻⁶ F = 2 µF", "C égale deux fois dix puissance moins six farad")],
      pointage=[regler("عندنا deux relations"),
                {"mot": "يعني u C égale I zéro sur C، fois t", "cible": "centre:0"},
                {"mot": "هادي هي la droite ديالنا", "repere": "droite"},
                {"mot": "إذن C égale I zéro sur k", "commande": "play_until", "parametres": {"moment": "C_deduite"}},
                {"mot": "C égale deux fois dix puissance moins six farad", "cible": "centre:1"},
                {"mot": "يعني deux microfarads", "repere": "resultat"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_g1", "Plus facile : la charge à courant constant", "نتمرنو بسؤال ساهل على la charge.",
      "Un générateur de courant débite I₀ = 4 µA pendant t = 6 s. La charge q du condensateur vaut…",
      ["6,7·10⁻⁷ C", "2,4·10⁻⁵ C", "4·10⁻⁶ C"], 1, {
        "1": {"juste": rep("مزيان! q égale I zéro fois t، يعني quatre fois dix puissance moins six، fois six، كتعطي deux virgule quatre fois dix puissance moins cinq coulomb.", "Juste : q = I₀·t = 4·10⁻⁶ × 6 = 2,4·10⁻⁵ C.")},
        "0": {"1": rep("ما تقلقش. هنا قسمتي I zéro على t. ولكن كل seconde كتزيد la charge، إذن كلما طال الوقت، q كتكبر. عاود اختار.", "Tu as divisé I₀ par t ; or q augmente avec le temps. Réessaie."),
              "2": rep("الجواب هو deux virgule quatre fois dix puissance moins cinq coulomb. q égale I zéro fois t، ماشي I zéro sur t.", "Réponse : q = I₀·t = 2,4·10⁻⁵ C (et non I₀/t).")},
        "2": {"1": rep("قريب. ولكن هادي غير la charge اللي كتوصل فكل seconde. شحال ديال les secondes دازو؟ عاود اختار.", "C'est la charge arrivée en une seconde seulement. Combien de secondes ? Réessaie."),
              "2": rep("الجواب هو deux virgule quatre fois dix puissance moins cinq coulomb. خاصك تضرب فt égale six secondes.", "Réponse : q = I₀·t = 4·10⁻⁶ × 6 = 2,4·10⁻⁵ C.")}},
      "Un générateur de courant débite I zéro égale quatre microampères pendant six secondes. La charge q du condensateur vaut ?"),
    qcm_facile("fa_g2", "Plus facile : la pente d'une droite", "سؤال ساهل على la pente.",
      "On lit sur la droite u_C(t) les points (2 s ; 4 V) et (6 s ; 12 V). La pente k vaut…",
      ["0,5 V/s", "8 V/s", "2 V/s"], 2, {
        "2": {"juste": rep("برافو! delta u C égale huit volts، delta t égale quatre secondes، و huit sur quatre كتعطي deux volts par seconde.", "Juste : k = (12 − 4)/(6 − 2) = 2 V/s.")},
        "0": {"1": rep("ما تقلقش. قسمتي delta t على delta u C. la pente هي la tension sur le temps. عاود اختار.", "Tu as calculé Δt/Δu_C ; la pente est Δu_C/Δt. Réessaie."),
              "2": rep("الجواب هو deux volts par seconde. k égale delta u C sur delta t، يعني huit sur quatre.", "Réponse : k = Δu_C/Δt = 8/4 = 2 V/s.")},
        "1": {"1": rep("قريب. huit volts هو غير delta u C. خاصك تقسم على delta t. عاود اختار.", "8 V, c'est seulement Δu_C ; il faut diviser par Δt. Réessaie."),
              "2": rep("الجواب هو deux volts par seconde. huit volts، sur quatre secondes.", "Réponse : k = 8 V / 4 s = 2 V/s.")}},
      "On lit sur la droite les points deux secondes, quatre volts, et six secondes, douze volts. La pente k vaut ?"),
    association_facile("fa_g3", "Plus facile : relier chaque relation à son sens", "سؤال ساهل: ربط كل relation بالمعنى ديالها.",
      "Relie chaque relation à ce qu'elle exprime.", "Associe chaque relation (1, 2, 3) à sa signification (a, b, c).",
      [("1", "q = C·u_C"), ("2", "q = I₀·t"), ("3", "k = I₀/C")],
      [("a", "la charge quand le courant est constant"), ("b", "le lien entre la charge et la tension du condensateur"), ("c", "la pente de la droite u_C(t)")],
      {"1": "b", "2": "a", "3": "c"},
      {"1-a": (False, "q = C·u_C est vraie pour tout condensateur, même si le courant varie : cherche ce qu'elle relie.", "q égale C fois u C صحيحة ديما، حتى إلى le courant ماشي ثابت. شوف شنو كتربط."),
       "1-b": (True, "Oui : q = C·u_C relie la charge et la tension ; C est la capacité.", "صحيح: q égale C fois u C كتربط la charge و la tension، و C هي la capacité."),
       "1-c": (False, "q = C·u_C ne parle pas de pente ni de temps : cherche ce qu'elle relie.", "q égale C fois u C ما فيهاش le temps. شوف شنو كتربط."),
       "2-a": (True, "Oui : avec un courant constant, la charge augmente régulièrement, q = I₀·t.", "صحيح: ملي le courant ثابت، la charge كتزاد بانتظام، q égale I zéro fois t."),
       "2-b": (False, "q = I₀·t fait intervenir le temps, pas la tension : regarde les lettres.", "q égale I zéro fois t فيها le temps، ماشي la tension. شوف الحروف."),
       "2-c": (False, "q = I₀·t donne une charge en coulombs, pas une pente : regarde l'unité.", "q égale I zéro fois t كتعطي la charge بle coulomb، ماشي la pente."),
       "3-a": (False, "I₀/C se mesure en volts par seconde, pas en coulombs : ce n'est pas une charge.", "I zéro sur C كتقاس بvolt par seconde، ماشي بle coulomb: ماشي la charge."),
       "3-b": (False, "k = I₀/C ne contient ni q ni u_C : cherche plutôt une droite.", "k égale I zéro sur C ما فيهاش q ولا u C. فكر فla droite."),
       "3-c": (True, "Oui : u_C = (I₀/C)·t, donc la pente de la droite est k = I₀/C.", "صحيح: u C égale I zéro sur C، fois t، إذن la pente هي k égale I zéro sur C.")},
      "(1 ; b) (2 ; a) (3 ; c) : de q = C·u_C et q = I₀·t on tire u_C = (I₀/C)·t, puis C = I₀/k.",
      "الخلاصة: من q égale C fois u C، و q égale I zéro fois t، كنلقاو u C égale I zéro sur C، fois t، ومن بعد C égale I zéro sur k."),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage (figure 1) avec un autre condensateur, initialement déchargé, et un générateur idéal de courant qui débite I₀ = 6 µA. À t = 0, on ferme K ; la figure 2 donne u_C(t).",
      "intro_dit": "نفس التمرين، بقيم أخرى. I zéro égale six microampères. فt égale zéro، كنسدو K، وla figure deux كتعطي u C en fonction de t.",
      "figures": [droite(6, 2, "Figure 2 : la tension u_C(t)")],
      "donnees": ["I₀ = 6 µA = 6·10⁻⁶ A"],
      "questions": [
        question_semblable("1", "Exprimer la charge q en fonction de I₀ et de t, puis calculer q à la date t = 6 s.",
          valeur("q", 3.6e-5, "C", "q = I₀·t = 6·10⁻⁶ × 6 = 3,6·10⁻⁵ C"), ["q = I₀·t", "10⁻⁶"], ["q = I₀/t"],
          corr([("1 : q = I₀·t = 6·10⁻⁶ × 6", "q égale I zéro fois t"), ("q = 3,6·10⁻⁵ C", "trois virgule six fois dix puissance moins cinq coulomb")],
               "q égale I zéro fois t، يعني six fois dix puissance moins six، fois six. q égale trois virgule six fois dix puissance moins cinq coulomb.")),
        question_semblable("2", "Déterminer graphiquement la pente k de la droite u_C = f(t).",
          valeur("k", 3, "V/s", "k = Δu_C/Δt = (18 − 6)/(6 − 2) = 3 V/s"), ["k = Δu_C/Δt", "V/s"], ["k = Δt/Δu_C"],
          corr([("2 : points (2 s ; 6 V) et (6 s ; 18 V)", "deux secondes، six volts"), ("k = (18 − 6)/(6 − 2) = 3 V/s", "k égale trois volts par seconde")],
               "كنقراو deux points: deux secondes، six volts، و six secondes، dix-huit volts. k égale douze sur quatre، k égale trois volts par seconde.")),
        question_semblable("3", "Montrer que u_C = (I₀/C)·t, puis en déduire la valeur de C.",
          valeur("C", 2e-6, "F", "C = I₀/k = 6·10⁻⁶/3 = 2·10⁻⁶ F"), ["C = I₀/k", "F"], ["C = k/I₀"],
          corr([("3 : u_C = q/C = (I₀/C)·t, donc k = I₀/C", "la pente égale I zéro sur C"), ("C = I₀/k = 6·10⁻⁶/3 = 2·10⁻⁶ F", "deux fois dix puissance moins six farad")],
               "u C égale I zéro sur C، fois t، إذن la pente égale I zéro sur C. C égale I zéro sur k، يعني six fois dix puissance moins six، sur trois. C égale deux fois dix puissance moins six farad.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
