# Exercice de physique, ch. 7 (dipôle RL), niveau facile n° 2 : établissement du courant — I₀, τ et u_b en régime permanent.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RL.json : cas_types « permanent » (I₀ = E/(R + r)),
#    « ub_perm » (u_b = r·I₀), « L » (τ = L/(R + r)) ; pièges « τ = L/R alors que la bobine a une résistance r »,
#    « I₀ = E/R » ; erreurs_examen « u_b en régime permanent : écrire 0 pour une bobine réelle ».
#  - nationaux : 2017 N (1.2, I_p), 2020 N (I.2, r en régime permanent), 2025 R (1-4, u_b permanent) ; ici les gestes
#    un à un (niveau facile).
#  - cours phys_ch7_dipole_RL : rl_m2_fermeture, rl_m4_I0 (circuit-rl.html?vue=etablissement), rl_e6_ub, rl_s5_dimension.
#  - séries en ligne : recherche web (talamidi, moutamadris, alloschool, série P7 N. Naceiri) ; pages non ouvertes
#    (domaines bloqués dans le conteneur), seuls les intitulés comparés. Données habituelles E = 6 à 12 V, R ~ 10 à
#    200 Ω, L ~ 0,1 à 1 H. Nos données sont réglées dans la simulation (circuit-rl.html : E = 12 V, R = 110 Ω,
#    L = 0,3 H, r = 10 Ω fixe dans la simulation).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch7_rl_2"
SIMD = "/media/simulations/physics/dipole-rl-tableau/"
SIM = SIMD + "circuit-rl.html?vue=etablissement&E=12&R_ohm=110&L_H=0.3"


def montage(titre):
    """Générateur E, interrupteur K, résistor R, bobine (L, r) en série ; i dans le sens horaire."""
    return schema(titre, 8, 4.8,
        dipole([1, 0.8], [1, 3.6], "G", "E", pos="o"),
        fil([1, 3.6], [1.6, 3.6]),
        dipole([1.6, 3.6], [3.4, 3.6], "K", "K"),
        dipole([3.4, 3.6], [6.0, 3.6], "R", "R", pos="s"),
        fil([6.0, 3.6], [7, 3.6]),
        dipole([7, 3.6], [7, 0.8], "L", "(L, r)", pos="o"),
        fil([7, 0.8], [1, 0.8]),
        courant([6.5, 3.6], "d"),
        tension([5.6, 4.15], [3.8, 4.15], "u_R", couleur="orange"),
        tension([7.6, 1.2], [7.6, 3.2], "u_b", couleur="violet", pos="e"))


E, R, r, L = 12, 110, 10, 0.3
I0 = E / (R + r)                 # 0,1 A
TAU = L / (R + r)                # 2,5 ms
UB = r * I0                      # 1 V
assert abs(I0 - 0.1) < 1e-12 and abs(TAU - 2.5e-3) < 1e-12 and abs(UB - 1) < 1e-12
# semblable
E2, R2, r2, L2 = 6, 40, 20, 0.36
I02, TAU2, UB2 = E2 / (R2 + r2), L2 / (R2 + r2), r2 * E2 / (R2 + r2)
assert abs(I02 - 0.1) < 1e-12 and abs(TAU2 - 6e-3) < 1e-12 and abs(UB2 - 2) < 1e-12

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RL", "cours": "phys_ch7_dipole_RL",
  "titre": "Fermer l'interrupteur : I₀, τ et la tension de la bobine", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer I₀ = E/(R + r) en régime permanent", "Calculer τ = L/(R + r) avec la résistance totale",
                  "Savoir qu'en régime permanent u_b = r·I₀"],
  "enonce": {
    "intro": "On réalise le montage de la figure : un générateur idéal de tension de force électromotrice E, un interrupteur K, un conducteur ohmique de résistance R et une bobine d'inductance L et de résistance r, en série. À la date t = 0, on ferme K ; le courant s'établit, puis le régime permanent est atteint.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا un générateur idéal de tension، la force électromotrice ديالو E، l'interrupteur K، un conducteur ohmique، la résistance ديالو R، و une bobine، l'inductance ديالها L و la résistance ديالها r، كلهم en série. فt égale zéro، كنسدو K: le courant كيتأسس، ومن بعد كنوصلو لle régime permanent.",
    "figures": [montage("Figure : le montage RL")],
    "donnees": ["E = 12 V", "R = 110 Ω", "Bobine : L = 0,3 H ; r = 10 Ω", "Tension de la bobine : u_b = L·di/dt + r·i"],
    "questions": [
      question("1", "Calculer l'intensité I₀ du courant en régime permanent.",
        "السؤال un: حسب I zéro، l'intensité ديال le courant فle régime permanent.",
        valeur("I₀", 0.1, "A", "I₀ = E/(R + r) = 12/(110 + 10) = 0,1 A"),
        ["I₀ = E/(R + r)", "R + r", "A"], ["I₀ = E/R", "I₀ = 12/110 ≈ 0,11 A"],
        [aide("En régime permanent, i ne varie plus : que vaut alors di/dt ? Écris la loi d'additivité u_R + u_b = E avec cette valeur.",
              "فle régime permanent، i ما بقاتش كتبدل. شحال كتساوي dé i sur dé t؟ كتب la loi d'additivité: u R plus u b égale E."),
         aide("di/dt = 0 donne R·I₀ + r·I₀ = E, donc I₀ = E/(R + r) : toutes les résistances de la maille.",
              "dé i sur dé t égale zéro، إذن R fois I zéro plus r fois I zéro égale E. إذن I zéro égale E sur R plus r: جميع les résistances ديال la maille.")],
        corr([("1 : en régime permanent di/dt = 0 : R·I₀ + r·I₀ = E", "R fois I zéro plus r fois I zéro égale E"),
              ("I₀ = E/(R + r) = 12/(110 + 10)", "I zéro égale E sur R plus r"),
              ("I₀ = 0,1 A", "I zéro égale zéro virgule un ampère")],
             "السؤال un. فle régime permanent، dé i sur dé t égale zéro. la loi d'additivité كتعطي R fois I zéro plus r fois I zéro égale E. إذن I zéro égale E sur R plus r، يعني douze sur cent vingt. I zéro égale zéro virgule un ampère."),
        "ex_rl2_1", "fa_rl2_1"),
      question("2", "Calculer la constante de temps τ du dipôle (en ms).",
        "السؤال deux: حسب la constante de temps tau، بla milliseconde.",
        valeur("τ", 2.5, "ms", "τ = L/(R + r) = 0,3/120 = 2,5·10⁻³ s = 2,5 ms"),
        ["τ = L/(R + r)", "10⁻³", "ms"], ["τ = L/R", "τ = (R + r)/L"],
        [aide("La constante de temps d'un dipôle RL fait intervenir L et la résistance totale du circuit, pas seulement R.",
              "la constante de temps ديال le dipôle RL فيها L و la résistance totale ديال الدارة، ماشي غير R."),
         aide("τ = L/(R + r) : calcule en secondes, puis multiplie par 1000 pour l'avoir en ms.",
              "tau égale L sur R plus r. حسب بla seconde، ومن بعد ضرب ف mille باش تكتبها بla milliseconde.")],
        corr([("2 : τ = L/(R + r)", "tau égale L sur R plus r"),
              ("A.N. : τ = 0,3/120 = 2,5·10⁻³ s", "zéro virgule trois sur cent vingt"),
              ("τ = 2,5 ms", "deux virgule cinq millisecondes")],
             "السؤال deux. tau égale L sur R plus r. l'application numérique: zéro virgule trois sur cent vingt، كتعطي deux virgule cinq fois dix puissance moins trois seconde. يعني tau égale deux virgule cinq millisecondes."),
        "ex_rl2_2", "fa_rl2_2"),
      question("3", "Calculer la tension u_b aux bornes de la bobine en régime permanent.",
        "السؤال trois: حسب la tension u b ديال la bobine فle régime permanent.",
        valeur("u_b", 1, "V", "u_b = L·di/dt + r·I₀ = 0 + 10 × 0,1 = 1 V"),
        ["u_b = L·di/dt + r·i", "di/dt = 0", "V"], ["u_b = 0", "u_b = E = 12 V"],
        [aide("La bobine n'est pas idéale : elle a une résistance r. En régime permanent, quel terme de u_b = L·di/dt + r·i disparaît ?",
              "la bobine ماشي idéale، عندها la résistance r. فle régime permanent، أشمن جزء ف u b égale L dé i sur dé t plus r i كيمشي؟"),
         aide("di/dt = 0, donc u_b = r·I₀, avec I₀ de la question 1.",
              "dé i sur dé t égale zéro، إذن u b égale r fois I zéro، و I zéro ديال السؤال الأول.")],
        corr([("3 : u_b = L·di/dt + r·i ; en régime permanent di/dt = 0", "u b égale L dé i sur dé t plus r i"),
              ("u_b = r·I₀ = 10 × 0,1", "u b égale r fois I zéro"),
              ("u_b = 1 V (et non 0 : la bobine a une résistance)", "u b égale un volt")],
             "السؤال trois. u b égale L dé i sur dé t plus r i. فle régime permanent، dé i sur dé t égale zéro. إذن u b égale r fois I zéro، يعني dix fois zéro virgule un. u b égale un volt، ماشي zéro، حيت la bobine عندها la résistance r."),
        "ex_rl2_3", "fa_rl2_3"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_rl2_1", "Question 1 : I₀ = E/(R + r)", "Régime permanent : I₀ = E/(R + r) = 12/120 = 0,1 A = 100 mA.",
      SIM, "K en position 1 : u_R, image de i, monte puis se stabilise",
      "شوف le circuit: E égale douze volts، R égale cent dix ohms، و la bobine، r égale dix ohms. كنحطو K فla position un. شوف l'écran: u R كتطلع، و هي l'image ديال i. من بعد كتبقى ثابتة: هادا هو le régime permanent. فيه i ما بقاتش كتبدل، إذن dé i sur dé t égale zéro. كيبقى R fois I zéro plus r fois I zéro égale E. إذن I zéro égale E sur R plus r، douze sur cent vingt، يعني zéro virgule un ampère، cent milliampères.",
      centre=[("I₀ = E/(R + r)", "إذن I zéro égale E sur R plus r"), ("I₀ = 12/120 = 0,1 A = 100 mA", "يعني zéro virgule un ampère")],
      pointage=[{"mot": "E égale douze volts", "repere": "generateur"},
                {"mot": "R égale cent dix ohms", "repere": "resistance"},
                {"mot": "r égale dix ohms", "repere": "bobine"},
                {"mot": "كنحطو K فla position un", "commande": "play_until", "parametres": {"moment": "fermeture"}},
                {"mot": "شوف l'écran", "commande": "play_until", "parametres": {"moment": "courbe_i"}},
                {"mot": "هادا هو le régime permanent", "commande": "play_until", "parametres": {"moment": "permanent"}},
                {"mot": "إذن I zéro égale E sur R plus r", "cible": "centre:0"},
                {"mot": "يعني zéro virgule un ampère", "repere": "regime_permanent"}]),
    diapo_sim("ex_rl2_2", "Question 2 : τ = L/(R + r)", "τ = L/(R + r) = 0,3/120 = 2,5·10⁻³ s = 2,5 ms.",
      SIM, "La durée de la montée dépend de L et de la résistance totale R + r",
      "شوف la courbe ديال la montée: هاد la durée ديال le régime transitoire كتتعلق ب L و ب la résistance totale. la bobine هنا: L égale zéro virgule trois henry، و r égale dix ohms. و R égale cent dix ohms. إذن R plus r égale cent vingt ohms. la constante de temps: tau égale L sur R plus r، يعني zéro virgule trois sur cent vingt. كتعطي deux virgule cinq millisecondes. رد البال: ماشي L sur R بوحدها.",
      centre=[("τ = L/(R + r)", "la constante de temps: tau égale L sur R plus r"), ("τ = 0,3/120 = 2,5·10⁻³ s = 2,5 ms", "كتعطي deux virgule cinq millisecondes")],
      pointage=[{"mot": "شوف la courbe ديال la montée", "commande": "play_until", "parametres": {"moment": "courbe_i"}},
                {"mot": "le régime transitoire", "repere": "regime_transitoire"},
                {"mot": "L égale zéro virgule trois henry", "repere": "bobine"},
                {"mot": "R égale cent dix ohms", "repere": "resistance"},
                {"mot": "la constante de temps: tau égale L sur R plus r", "cible": "centre:0"},
                {"mot": "كتعطي deux virgule cinq millisecondes", "cible": "centre:1"}]),
    diapo_sim("ex_rl2_3", "Question 3 : u_b = r·I₀ en régime permanent", "Régime permanent : di/dt = 0, u_b = r·I₀ = 10 × 0,1 = 1 V.",
      SIM, "En régime permanent la bobine se comporte comme sa résistance r",
      "شوف la flèche ديال u b، en convention récepteur. u b égale L dé i sur dé t plus r i. فle régime permanent، i ثابتة: dé i sur dé t égale zéro. إذن u b égale r fois I zéro. r égale dix ohms، و I zéro égale zéro virgule un ampère. u b égale un volt. وزيد تأكد: u R égale R fois I zéro، يعني onze volts، و onze plus un égale douze، هي E.",
      centre=[("u_b = L·di/dt + r·i", "u b égale L dé i sur dé t plus r i"), ("u_b = r·I₀ = 10 × 0,1 = 1 V", "u b égale un volt")],
      pointage=[{"mot": "شوف la flèche ديال u b", "repere": "fleche_ub"},
                {"mot": "فle régime permanent", "commande": "play_until", "parametres": {"moment": "permanent"}},
                {"mot": "r égale dix ohms", "repere": "bobine"},
                {"mot": "u b égale un volt", "cible": "centre:1"},
                {"mot": "u R égale R fois I zéro", "repere": "regime_permanent"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_rl2_1", "Plus facile : le courant final", "نتمرنو بسؤال ساهل على I zéro.",
      "E = 12 V, R = 110 Ω, bobine de résistance r = 10 Ω. En régime permanent, I₀ vaut…",
      ["E/R ≈ 0,109 A", "E/(R + r) = 0,1 A", "E/r = 1,2 A"], 1, {
        "1": {"juste": rep("برافو! I zéro égale E sur R plus r: جميع les résistances ديال la maille.", "Juste : I₀ = E/(R + r) = 0,1 A.")},
        "0": {"1": rep("نسيتي شي résistance. la bobine عندها حتى هي la résistance r. عاود.", "Tu as oublié la résistance r de la bobine. Réessaie."),
              "2": rep("الجواب هو E sur R plus r، يعني zéro virgule un ampère. la résistance r ديال la bobine كتزاد مع R.", "Réponse : I₀ = E/(R + r) = 12/120 = 0,1 A.")},
        "2": {"1": rep("R حتى هي فla maille، و le courant كيدوز فيها. عاود.", "Le courant traverse aussi R. Réessaie."),
              "2": rep("الجواب هو E sur R plus r، يعني zéro virgule un ampère. R و r بجوج فla maille.", "Réponse : I₀ = E/(R + r) = 0,1 A.")}},
      "E égale douze volts، R égale cent dix ohms، r égale dix ohms. En régime permanent، I zéro vaut ?"),
    qcm_facile("fa_rl2_2", "Plus facile : la constante de temps", "سؤال ساهل: اختار la bonne relation ديال tau.",
      "La constante de temps d'un dipôle RL (bobine de résistance r) est…",
      ["τ = (R + r)/L", "τ = L/R", "τ = L/(R + r)"], 2, {
        "2": {"juste": rep("برافو! tau égale L sur R plus r: L فوق، و la résistance totale لتحت.", "Juste : τ = L/(R + r).")},
        "0": {"1": rep("قلبتي. إلى كبرات L، le courant كيتأسس بشوية: tau خاصها تكبر مع L. عاود.", "Si L augmente, τ doit augmenter. Réessaie."),
              "2": rep("الجواب هو tau égale L sur R plus r. L كتكبر tau، إذن L فوق.", "Réponse : τ = L/(R + r).")},
        "1": {"1": rep("قريب، ولكن la bobine عندها la résistance r. فين مشات؟ عاود.", "Et la résistance r de la bobine ? Réessaie."),
              "2": rep("الجواب هو tau égale L sur R plus r: la résistance totale ديال الدارة.", "Réponse : τ = L/(R + r), avec la résistance totale.")}},
      "La constante de temps d'un dipôle RL est ?"),
    vrai_faux_facile("fa_rl2_3", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
      "Régime permanent : I₀ = 0,1 A ; bobine L = 0,3 H, r = 10 Ω.",
      [("En régime permanent, di/dt = 0.", True, "Le courant ne varie plus : sa dérivée est nulle."),
       ("En régime permanent, la tension aux bornes de cette bobine est nulle.", False, "Elle vaut r·I₀ = 1 V ; elle est nulle seulement si la bobine est idéale (r = 0)."),
       ("En régime permanent, la bobine se comporte comme un conducteur ohmique de résistance r.", True, "u_b = r·I₀ : seul le terme r·i reste.")]),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage avec d'autres valeurs : E = 6 V, R = 40 Ω, bobine d'inductance L = 0,36 H et de résistance r = 20 Ω. À t = 0, on ferme K.",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale six volts، R égale quarante ohms، L égale zéro virgule trente-six henry، و r égale vingt ohms.",
      "figures": [],
      "donnees": ["E = 6 V", "R = 40 Ω", "Bobine : L = 0,36 H ; r = 20 Ω"],
      "questions": [
        question_semblable("1", "Calculer l'intensité I₀ du courant en régime permanent.",
          valeur("I₀", 0.1, "A", "I₀ = E/(R + r) = 6/(40 + 20) = 0,1 A"), ["I₀ = E/(R + r)", "A"], ["I₀ = E/R"],
          corr([("1 : I₀ = E/(R + r) = 6/60", "I zéro égale E sur R plus r"), ("I₀ = 0,1 A", "zéro virgule un ampère")],
               "I zéro égale E sur R plus r، يعني six sur soixante، كتعطي zéro virgule un ampère.")),
        question_semblable("2", "Calculer la constante de temps τ du dipôle (en ms).",
          valeur("τ", 6, "ms", "τ = L/(R + r) = 0,36/60 = 6·10⁻³ s = 6 ms"), ["τ = L/(R + r)", "ms"], ["τ = L/R"],
          corr([("2 : τ = L/(R + r) = 0,36/60", "tau égale L sur R plus r"), ("τ = 6·10⁻³ s = 6 ms", "six millisecondes")],
               "tau égale L sur R plus r، يعني zéro virgule trente-six sur soixante، كتعطي six millisecondes.")),
        question_semblable("3", "Calculer la tension u_b aux bornes de la bobine en régime permanent.",
          valeur("u_b", 2, "V", "u_b = r·I₀ = 20 × 0,1 = 2 V"), ["u_b = r·I₀", "V"], ["u_b = 0"],
          corr([("3 : di/dt = 0 : u_b = r·I₀ = 20 × 0,1", "u b égale r fois I zéro"), ("u_b = 2 V", "deux volts")],
               "فle régime permanent، dé i sur dé t égale zéro. u b égale r fois I zéro، يعني vingt fois zéro virgule un، كتعطي deux volts.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
