# Exercice de physique, ch. 7 (dipôle RL), niveau facile n° 1 : la tension aux bornes d'une bobine idéale
# traversée par un courant triangulaire (u_b = L·di/dt, constante par morceaux).
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RL.json : capacité RL1 (u_b = L·di/dt + r·i, bobine idéale),
#    pièges « écrire u_b proportionnelle à i » (u_b dépend de la pente), « mA / ms non convertis » ; vidéos : aucune
#    (YouTube inaccessible lors de l'exploration).
#  - nationaux 2016-2025 (exam.json) : aucun sujet de courant triangulaire ; le geste « u_b = L·di/dt sur une pente »
#    sert aux questions u_L(t) (2018 R, 2023 N) ; ici seulement le geste un à un (niveau facile).
#  - cours phys_ch7_dipole_RL : diapos rl_b6_triangle, rl_b7_inductance (triangle.html, L = 20 mH, 0 → 0,2 A en 10 ms),
#    rl_b9_segments (fig_segments).
#  - séries en ligne : recherche web faite (talamidi « dipôle RL exercices », moutamadris « cours dipôle RL » avec
#    l'expérience du GBF triangulaire, série P7 de N. Naceiri) ; les pages elles-mêmes n'ont pas pu être ouvertes
#    (domaines bloqués dans le conteneur) : seuls les intitulés ont été comparés. Données habituelles : L ~ 10 à 100 mH,
#    pentes ~ 10 à 100 A/s. Nos données suivent la simulation (triangle.html?L_mH=25 : même triangle, L = 25 mH).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch7_rl_1"
SIMD = "/media/simulations/physics/dipole-rl-tableau/"
SIM = SIMD + "triangle.html?L_mH=25"


def triangle(imax_mA, demi_ms, titre, n=2):
    """i(t) triangulaire : de 0 à imax en demi_ms, puis retour à 0 en demi_ms (n périodes)."""
    p = [[0, 0]]
    for k in range(n):
        p += [[(2 * k + 1) * demi_ms, imax_mA], [(2 * k + 2) * demi_ms, 0]]
    tmax = 2 * n * demi_ms
    return figure_courbe(titre, axe("t", 0, tmax, "ms", [demi_ms * j for j in range(2 * n + 1)]),
                         axe("i", 0, imax_mA * 1.25, "mA", list(range(0, int(imax_mA * 1.25) + 1, 50))),
                         [{"f": "ligne", "pts": p, "couleur": "vert"},
                          {"f": "repere", "y": imax_mA, "couleur": "faible"}],
                         legende="Le GBF impose ce courant i(t) dans la bobine.")


def montage(titre):
    return schema(titre, 7, 3.6,
        dipole([1, 0.6], [1, 3.0], "G", pos="o"), texte([0.35, 1.7], "GBF"),
        fil([1, 3.0], [5.6, 3.0]),
        dipole([5.6, 3.0], [5.6, 0.6], "L", "L", pos="e"),
        fil([5.6, 0.6], [1, 0.6]),
        courant([3.2, 3.0], "d"),
        tension([6.5, 0.9], [6.5, 2.7], "u_b", pos="e"))


L = 25e-3
DIDT = 0.2 / 10e-3                   # 20 A/s
U = L * DIDT                         # 0,5 V
assert abs(DIDT - 20) < 1e-9 and abs(U - 0.5) < 1e-12

# semblable
L2, IM2, DT2 = 40e-3, 0.15, 5e-3
DIDT2 = IM2 / DT2                    # 30 A/s
U2 = L2 * DIDT2                      # 1,2 V
assert abs(DIDT2 - 30) < 1e-9 and abs(U2 - 1.2) < 1e-12

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RL", "cours": "phys_ch7_dipole_RL",
  "titre": "Un courant en triangle : la tension u_b = L·di/dt", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer la pente di/dt sur un segment de la courbe i(t)", "Appliquer u_b = L·di/dt pour une bobine idéale",
                  "Savoir que u_b change de signe quand i diminue"],
  "enonce": {
    "intro": "Une bobine d'inductance L et de résistance négligeable (bobine idéale) est branchée à un générateur basse fréquence (GBF) qui lui impose le courant i(t) de la figure 2 : i monte de 0 à 0,2 A en 10 ms, puis redescend à 0 en 10 ms, et ainsi de suite. La tension u_b est orientée en convention récepteur (figure 1).",
    "intro_dit": "دابا نقراو l'énoncé. عندنا une bobine idéale، يعني la résistance ديالها négligeable، و l'inductance ديالها L. le GBF كيفرض فيها un courant i en triangle: i كتطلع من zéro حتى zéro virgule deux ampère ف dix millisecondes، ومن بعد كتنزل حتى zéro ف dix millisecondes. و la tension u b en convention récepteur.",
    "figures": [montage("Figure 1 : la bobine et le GBF"), triangle(200, 10, "Figure 2 : le courant i(t)")],
    "donnees": ["L = 25 mH = 25·10⁻³ H", "Résistance de la bobine négligeable : u_b = L·di/dt", "i : de 0 à 0,2 A entre 0 et 10 ms ; de 0,2 A à 0 entre 10 et 20 ms"],
    "questions": [
      question("1", "Calculer la pente di/dt du courant pendant la montée (entre 0 et 10 ms).",
        "السؤال un: حسب la pente dé i sur dé t ديال le courant فla montée، بين zéro و dix millisecondes.",
        valeur("di/dt", 20, "A/s", "di/dt = Δi/Δt = 0,2/(10·10⁻³) = 20 A/s"),
        ["Δi/Δt", "10⁻³", "A/s", "0,2 A"], ["0,2/10 = 0,02 A/s", "di/dt = i/t = 0,2/20"],
        [aide("Sur la montée, la courbe est un segment de droite : relève Δi (en A) et Δt (en s) entre ses deux extrémités.",
              "فla montée، la courbe هي خط مستقيم. شوف شحال تبدلات i، و شحال دام الوقت. كتب delta i بl'ampère و delta t بla seconde."),
         aide("di/dt = Δi/Δt avec Δi = 0,2 A et Δt = 10 ms = 10·10⁻³ s.",
              "dé i sur dé t égale delta i sur delta t. delta i égale zéro virgule deux ampère، و delta t égale dix millisecondes، يعني dix fois dix puissance moins trois seconde.")],
        corr([("1 : di/dt = Δi/Δt", "dé i sur dé t égale delta i sur delta t"),
              ("A.N. : di/dt = 0,2/(10·10⁻³)", "zéro virgule deux sur dix fois dix puissance moins trois"),
              ("di/dt = 20 A/s", "vingt ampères par seconde")],
             "السؤال un. dé i sur dé t égale delta i sur delta t. l'application numérique: zéro virgule deux sur dix fois dix puissance moins trois. كتعطي vingt ampères par seconde."),
        "ex_rl1_1", "fa_rl1_1"),
      question("2", "En déduire la tension u_b aux bornes de la bobine pendant la montée.",
        "السؤال deux: استنتج la tension u b ديال la bobine فla montée.",
        valeur("u_b", 0.5, "V", "u_b = L·di/dt = 25·10⁻³ × 20 = 0,5 V"),
        ["u_b = L·di/dt", "25·10⁻³", "V"], ["u_b = r·i", "u_b = 25 × 20 = 500 V"],
        [aide("La bobine est idéale : quelle relation donne la tension à ses bornes ? Elle dépend de la pente, pas de la valeur de i.",
              "la bobine idéale. شنو هي la relation ديال la tension ديالها؟ رد البال: u b كتتعلق بla pente، ماشي ب la valeur ديال i."),
         aide("u_b = L·di/dt, avec L = 25 mH = 25·10⁻³ H et la pente trouvée à la question 1.",
              "u b égale L dé i sur dé t. L égale vingt-cinq millihenrys، يعني vingt-cinq fois dix puissance moins trois henry. ضربها فla pente ديال السؤال الأول.")],
        corr([("2 : bobine idéale : u_b = L·di/dt", "u b égale L dé i sur dé t"),
              ("A.N. : u_b = 25·10⁻³ × 20", "vingt-cinq fois dix puissance moins trois fois vingt"),
              ("u_b = 0,5 V, constante pendant toute la montée", "zéro virgule cinq volt")],
             "السؤال deux. la bobine idéale، إذن u b égale L dé i sur dé t. l'application numérique: vingt-cinq fois dix puissance moins trois fois vingt. u b égale zéro virgule cinq volt، و كتبقى constante طول la montée."),
        "ex_rl1_2", "fa_rl1_2"),
      question("3", "Calculer la tension u_b pendant la descente (entre 10 ms et 20 ms).",
        "السؤال trois: حسب la tension u b فla descente، بين dix و vingt millisecondes.",
        valeur("u_b", -0.5, "V", "u_b = L·di/dt = 25·10⁻³ × (−20) = −0,5 V"),
        ["u_b = L·di/dt", "di/dt < 0", "V"], ["u_b = 0", "u_b = +0,5 V"],
        [aide("Pendant la descente, i passe de 0,2 A à 0 en 10 ms : quel est le signe de la pente ?",
              "فla descente، i كتنزل من zéro virgule deux ampère حتى zéro ف dix millisecondes. شنو هي la signe ديال la pente؟"),
         aide("di/dt = (0 − 0,2)/(10·10⁻³) = −20 A/s, puis u_b = L·di/dt.",
              "dé i sur dé t égale zéro moins zéro virgule deux، sur dix fois dix puissance moins trois، يعني moins vingt ampères par seconde. من بعد u b égale L dé i sur dé t.")],
        corr([("3 : di/dt = (0 − 0,2)/(10·10⁻³) = −20 A/s", "moins vingt ampères par seconde"),
              ("u_b = L·di/dt = 25·10⁻³ × (−20)", "vingt-cinq fois dix puissance moins trois fois moins vingt"),
              ("u_b = −0,5 V : u_b change de signe quand i diminue", "moins zéro virgule cinq volt")],
             "السؤال trois. فla descente، la pente égale moins vingt ampères par seconde. u b égale L dé i sur dé t، يعني vingt-cinq fois dix puissance moins trois fois moins vingt. u b égale moins zéro virgule cinq volt: u b كتولي négative ملي i كتنقص."),
        "ex_rl1_3", "fa_rl1_3"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_rl1_1", "Question 1 : la pente di/dt", "di/dt = Δi/Δt = 0,2/0,01 = 20 A/s sur la montée.",
      SIM, "Le GBF impose i(t) en triangle : la pente de la montée",
      "شوف le graphe ديال i en fonction de t. le GBF كيفرض un courant en triangle. فla montée، i كتطلع من zéro حتى zéro virgule deux ampère، ف dix millisecondes. la courbe خط مستقيم، إذن la pente هي نفسها فكل نقطة. la pente هي dé i sur dé t، يعني delta i sur delta t. zéro virgule deux sur zéro virgule zéro un، كتعطي vingt ampères par seconde.",
      centre=[("di/dt = Δi/Δt", "la pente هي dé i sur dé t"), ("di/dt = 0,2/0,01 = 20 A/s", "كتعطي vingt ampères par seconde")],
      pointage=[{"mot": "شوف le graphe ديال i en fonction de t", "commande": "play_until", "parametres": {"moment": "courant"}},
                {"mot": "le GBF كيفرض un courant en triangle", "repere": "graphe_i"},
                {"mot": "la pente هي dé i sur dé t", "commande": "play_until", "parametres": {"moment": "pente_montee"}},
                {"mot": "zéro virgule deux sur zéro virgule zéro un", "repere": "pente"},
                {"mot": "كتعطي vingt ampères par seconde", "cible": "centre:1"}]),
    diapo_sim("ex_rl1_2", "Question 2 : u_b = L·di/dt", "u_b = L·di/dt = 0,025 × 20 = 0,5 V, constante pendant la montée.",
      SIM, "Pendant la montée, u_b reste sur un palier : L fois la pente",
      "la bobine idéale: u b égale L dé i sur dé t. هنا L égale vingt-cinq millihenrys، يعني zéro virgule zéro vingt-cinq henry. شوف le graphe ديال u b: pendant la montée، u b كتبقى constante، لأن la pente constante. u b égale zéro virgule zéro vingt-cinq fois vingt، كتعطي zéro virgule cinq volt. ونقسمو le palier على la pente: كنرجعو ل L.",
      centre=[("u_b = L·di/dt", "u b égale L dé i sur dé t"), ("u_b = 0,025 × 20 = 0,5 V", "كتعطي zéro virgule cinq volt")],
      pointage=[{"mot": "هنا L égale vingt-cinq millihenrys", "repere": "bobine"},
                {"mot": "شوف le graphe ديال u b", "commande": "play_until", "parametres": {"moment": "palier_haut"}},
                {"mot": "u b كتبقى constante", "repere": "palier"},
                {"mot": "كتعطي zéro virgule cinq volt", "cible": "centre:1"},
                {"mot": "ونقسمو le palier على la pente", "commande": "play_until", "parametres": {"moment": "rapport"}}]),
    diapo_sim("ex_rl1_3", "Question 3 : la descente", "di/dt = −20 A/s : u_b = 0,025 × (−20) = −0,5 V.",
      SIM, "Pendant la descente, la pente est négative : u_b aussi",
      "دابا la descente. i كتنزل من zéro virgule deux ampère حتى zéro، ف dix millisecondes. la pente négative: moins vingt ampères par seconde. u b égale L dé i sur dé t، يعني zéro virgule zéro vingt-cinq fois moins vingt. شوف le palier ديال u b: كتعطي moins zéro virgule cinq volt. ملي i كتنقص، u b كتولي négative.",
      centre=[("di/dt = −0,2/0,01 = −20 A/s", "la pente négative"), ("u_b = 0,025 × (−20) = −0,5 V", "كتعطي moins zéro virgule cinq volt")],
      pointage=[{"mot": "دابا la descente", "commande": "play_until", "parametres": {"moment": "pente_descente"}},
                {"mot": "la pente négative", "cible": "centre:0"},
                {"mot": "شوف le palier ديال u b", "commande": "play_until", "parametres": {"moment": "palier_bas"}},
                {"mot": "كتعطي moins zéro virgule cinq volt", "cible": "centre:1"},
                {"mot": "u b كتولي négative", "repere": "graphe_u"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_rl1_1", "Plus facile : la pente", "نتمرنو بسؤال ساهل على la pente.",
      "Le courant passe de 0 à 0,2 A en 10 ms. La pente di/dt vaut…",
      ["0,02 A/s", "20 A/s", "2 A/s"], 1, {
        "1": {"juste": rep("برافو! zéro virgule deux sur zéro virgule zéro un، كتعطي vingt ampères par seconde.", "Juste : di/dt = 0,2/0,01 = 20 A/s.")},
        "0": {"1": rep("ما تقلقش. قسمتي على dix، ولكن dix millisecondes ماشي dix secondes. حول الوقت لla seconde وعاود.", "Tu as divisé par 10 : mais 10 ms = 0,01 s. Convertis le temps en secondes et réessaie."),
              "2": rep("الجواب هو vingt ampères par seconde. dix millisecondes هي zéro virgule zéro un seconde، و zéro virgule deux sur zéro virgule zéro un égale vingt.", "Réponse : 20 A/s, car 10 ms = 0,01 s et 0,2/0,01 = 20.")},
        "2": {"1": rep("قريب، ولكن الحساب ما صحيحش. شحال كتعطي zéro virgule deux sur zéro virgule zéro un؟ عاود.", "Refais la division 0,2/0,01. Réessaie."),
              "2": rep("الجواب هو vingt ampères par seconde: zéro virgule deux sur zéro virgule zéro un égale vingt.", "Réponse : 0,2/0,01 = 20 A/s.")}},
      "Le courant passe de zéro à zéro virgule deux ampère en dix millisecondes. La pente dé i sur dé t vaut ?"),
    qcm_facile("fa_rl1_2", "Plus facile : la relation de la bobine idéale", "سؤال ساهل: اختار la relation ديال la bobine idéale.",
      "Pour une bobine idéale (r négligeable), la tension à ses bornes s'écrit…",
      ["u_b = r·i", "u_b = (di/dt)/L", "u_b = L·di/dt"], 2, {
        "2": {"juste": rep("برافو! u b égale L dé i sur dé t: la tension كتتعلق بla pente ديال i.", "Juste : u_b = L·di/dt, la tension dépend de la pente de i.")},
        "0": {"1": rep("r fois i هو الجزء ديال la résistance. ولكن هنا r négligeable. شنو الجزء اللي كيبقى؟ عاود.", "r·i est le terme de la résistance, ici négligeable. Quel terme reste ? Réessaie."),
              "2": rep("الجواب هو u b égale L dé i sur dé t. r négligeable، إذن الجزء r fois i كيمشي.", "Réponse : u_b = L·di/dt (r·i est nul ici).")},
        "1": {"1": rep("فكر فles unités: إلى كبرات L، واش u b كتكبر ولا كتصغر؟ عاود.", "Si L augmente, u_b doit augmenter. Réessaie."),
              "2": rep("الجواب هو u b égale L dé i sur dé t: L كتضرب فla pente، ماشي كتقسم.", "Réponse : u_b = L·di/dt (L multiplie la pente).")}},
      "Pour une bobine idéale, la tension à ses bornes s'écrit ?"),
    vrai_faux_facile("fa_rl1_3", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
      "Bobine idéale, L = 25 mH ; pendant la descente, i passe de 0,2 A à 0 en 10 ms.",
      [("Pendant la descente, di/dt est négative, donc u_b est négative.", True, "di/dt = −20 A/s, donc u_b = L·di/dt = −0,5 V."),
       ("Pendant la descente, u_b est nulle parce que le courant diminue.", False, "u_b dépend de la pente : la pente vaut −20 A/s, pas 0. u_b = −0,5 V."),
       ("La tension u_b est constante sur toute la descente.", True, "La pente est la même sur tout le segment, donc u_b reste à −0,5 V.")]),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage avec une autre bobine idéale, L = 40 mH. Le GBF impose maintenant un courant qui monte de 0 à 0,15 A en 5 ms, puis redescend à 0 en 5 ms (figure 2).",
      "intro_dit": "نفس التمرين، بقيم أخرى. L égale quarante millihenrys. i كتطلع من zéro حتى zéro virgule quinze ampère ف cinq millisecondes، ومن بعد كتنزل ف cinq millisecondes.",
      "figures": [triangle(150, 5, "Figure 2 : le courant i(t)")],
      "donnees": ["L = 40 mH = 40·10⁻³ H", "Bobine idéale : u_b = L·di/dt", "i : de 0 à 0,15 A entre 0 et 5 ms ; de 0,15 A à 0 entre 5 et 10 ms"],
      "questions": [
        question_semblable("1", "Calculer la pente di/dt du courant pendant la montée (entre 0 et 5 ms).",
          valeur("di/dt", 30, "A/s", "di/dt = Δi/Δt = 0,15/(5·10⁻³) = 30 A/s"), ["Δi/Δt", "10⁻³", "A/s"], ["0,15/5 = 0,03 A/s"],
          corr([("1 : di/dt = Δi/Δt = 0,15/(5·10⁻³)", "dé i sur dé t égale delta i sur delta t"), ("di/dt = 30 A/s", "trente ampères par seconde")],
               "dé i sur dé t égale delta i sur delta t، يعني zéro virgule quinze sur cinq fois dix puissance moins trois. كتعطي trente ampères par seconde.")),
        question_semblable("2", "En déduire la tension u_b aux bornes de la bobine pendant la montée.",
          valeur("u_b", 1.2, "V", "u_b = L·di/dt = 40·10⁻³ × 30 = 1,2 V"), ["u_b = L·di/dt", "V"], ["u_b = r·i"],
          corr([("2 : u_b = L·di/dt = 40·10⁻³ × 30", "u b égale L dé i sur dé t"), ("u_b = 1,2 V", "un virgule deux volt")],
               "u b égale L dé i sur dé t، يعني quarante fois dix puissance moins trois fois trente. u b égale un virgule deux volt.")),
        question_semblable("3", "Calculer la tension u_b pendant la descente (entre 5 ms et 10 ms).",
          valeur("u_b", -1.2, "V", "u_b = L·di/dt = 40·10⁻³ × (−30) = −1,2 V"), ["di/dt < 0", "V"], ["u_b = 0"],
          corr([("3 : di/dt = −30 A/s ; u_b = 40·10⁻³ × (−30)", "moins trente ampères par seconde"), ("u_b = −1,2 V", "moins un virgule deux volt")],
               "فla descente، la pente égale moins trente ampères par seconde. u b égale quarante fois dix puissance moins trois fois moins trente، يعني moins un virgule deux volt.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
