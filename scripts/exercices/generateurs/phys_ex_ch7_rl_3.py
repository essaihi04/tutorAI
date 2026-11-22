# Exercice de physique, ch. 7 (dipôle RL), niveau moyen n° 3 : deux lampes, le retard à l'établissement du courant,
# l'équation différentielle de la branche de la bobine et sa solution.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RL.json : capacité RL2 (la bobine retarde l'établissement),
#    cas_types « ed_i » (additivité → L·di/dt + (R + r)·i = E), « solution » (dériver, remplacer, regrouper : τ, A),
#    « permanent » ; redaction_nationale « etablir_ED », « verifier_solution » ; pièges « oublier r ».
#  - nationaux : 2016 R (4, 5 : établir l'équation, trouver A et τ), 2020 N (I.1), 2021 R (II-2), 2023 N (1-1, 1-2-1) :
#    même enchaînement « établir → vérifier la solution → A, τ → valeur » que ces sujets (niveau du national).
#  - cours phys_ch7_dipole_RL : rl_b2_lampes, rl_b3_egal (lampes.html : E = 6 V, R = r = 10 Ω, lampes de 20 Ω,
#    L = 1,2 H avec le noyau), rl_e3_equation (fig_ed), rl_s3_tau / rl_s4_A (fig_resolution).
#  - séries en ligne : recherche web (talamidi, moutamadris : expérience des deux lampes en début de série ; série P7
#    N. Naceiri) ; pages non ouvertes (domaines bloqués dans le conteneur), seuls les intitulés comparés. Les séries
#    s'arrêtent à l'observation qualitative ; ici on la prolonge par l'équation de la branche (situation originale).
#    Nos données sont celles de la simulation des lampes, pour que l'explication montre les mêmes valeurs.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch7_rl_3"
SIMD = "/media/simulations/physics/dipole-rl-tableau/"
LAMPES = SIMD + "lampes.html"
FIG_ED = SIMD + "figures.html?fig=fig_ed"
FIG_RES = SIMD + "figures.html?fig=fig_resolution"


def montage(titre):
    """Générateur E et K, puis deux branches en parallèle : L₁ + R (gauche), L₂ + bobine (droite)."""
    return schema(titre, 9, 5.2,
        dipole([1, 0.6], [1, 4.4], "G", "E", pos="o"),
        dipole([1, 4.4], [3.4, 4.4], "K", "K"),
        fil([3.4, 4.4], [7.6, 4.4]),
        dipole([4.6, 4.4], [4.6, 2.5], "lampe", "L₁", pos="o"),
        dipole([4.6, 2.5], [4.6, 0.6], "R", "R", pos="o"),
        dipole([7.6, 4.4], [7.6, 2.5], "lampe", "L₂", pos="e"),
        dipole([7.6, 2.5], [7.6, 0.6], "L", "(L, r)", pos="e"),
        fil([7.6, 0.6], [1, 0.6]),
        courant([4.6, 4.05], "b", "i₁"), courant([7.6, 4.05], "b", "i₂"))


E, RL, R, r, L = 6, 20, 10, 10, 1.2
IP = E / (RL + r)                    # 0,2 A
TAU = L / (RL + r)                   # 0,04 s
T5 = 5 * TAU                         # 0,2 s
I1 = E / (RL + R)                    # 0,2 A : même éclat final
assert abs(IP - 0.2) < 1e-12 and abs(TAU - 0.04) < 1e-12 and abs(T5 - 0.2) < 1e-12 and abs(I1 - IP) < 1e-12
# semblable
E2, RL2, r2, L2 = 12, 30, 10, 0.8
IP2, TAU2 = E2 / (RL2 + r2), L2 / (RL2 + r2)
assert abs(IP2 - 0.3) < 1e-12 and abs(TAU2 - 0.02) < 1e-12 and abs(5 * TAU2 - 0.1) < 1e-12

ATT1 = ("À la fermeture de K, L₁ s'allume aussitôt ; L₂ s'allume progressivement, en retard ; au bout d'un moment, "
        "les deux lampes brillent de la même façon. La bobine s'oppose aux variations du courant : elle retarde "
        "l'établissement du courant i₂ dans sa branche (i₂ ne passe pas d'un coup de 0 à sa valeur finale).")
ATT2 = ("Branche 2 (lampe L₂ + bobine) : u_L₂ + u_b = E, avec u_L₂ = R_L·i₂ et u_b = L·di₂/dt + r·i₂. "
        "Donc L·di₂/dt + (R_L + r)·i₂ = E, soit di₂/dt + ((R_L + r)/L)·i₂ = E/L.")
ATT3 = ("di₂/dt = (A/τ)·e^(−t/τ). On remplace : L·(A/τ)·e^(−t/τ) + (R_L + r)·A·(1 − e^(−t/τ)) = E, "
        "soit A·e^(−t/τ)·(L/τ − (R_L + r)) + (R_L + r)·A = E pour tout t. Donc L/τ − (R_L + r) = 0 et (R_L + r)·A = E : "
        "τ = L/(R_L + r) et A = E/(R_L + r).")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RL", "cours": "phys_ch7_dipole_RL",
  "titre": "Deux lampes : le retard dû à la bobine, mis en équation", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Décrire et justifier le retard à l'établissement du courant dû à une bobine",
                  "Établir l'équation différentielle vérifiée par i(t)", "Déterminer A et τ en remplaçant la solution dans l'équation",
                  "Calculer I_p, τ et la durée du régime transitoire (≈ 5τ)"],
  "enonce": {
    "intro": "On branche sur un générateur de tension E, à travers un interrupteur K, deux branches en parallèle (figure) : la branche 1 contient une lampe L₁ et un conducteur ohmique de résistance R ; la branche 2 contient une lampe L₂, identique à L₁, et une bobine d'inductance L et de résistance r = R. On assimile chaque lampe à un conducteur ohmique de résistance R_L. À t = 0, on ferme K.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا un générateur E و l'interrupteur K، و les deux branches en parallèle. la branche un فيها la lampe L un و un conducteur ohmique R. la branche deux فيها la lampe L deux، بحال L un، و une bobine، l'inductance ديالها L و la résistance ديالها r، و r égale R. كنعتبرو كل lampe بحال un conducteur ohmique، la résistance ديالو R L. فt égale zéro، كنسدو K.",
    "figures": [montage("Figure : deux lampes, deux branches")],
    "donnees": ["E = 6 V", "R = r = 10 Ω", "R_L = 20 Ω (chaque lampe)", "L = 1,2 H", "u_b = L·di/dt + r·i"],
    "questions": [
      question("1", "Décrire ce qu'on observe sur les deux lampes après la fermeture de K, puis justifier le comportement de L₂.",
        "السؤال un: وصف شنو كنشوفو فles deux lampes من بعد ما كنسدو K، ومن بعد برر شنو كيوقع ل L deux.",
        phrase(ATT1),
        ["s'allume aussitôt", "en retard", "la bobine s'oppose aux variations de i"], ["L₂ ne s'allume jamais", "L₂ brille moins à la fin"],
        [aide("Compare les deux branches : elles ont la même résistance totale (R_L + R et R_L + r). Une seule chose les distingue : laquelle ?",
              "قارن les deux branches: نفس la résistance totale. حاجة وحدة كتفرق بيناتهم: شنو هي؟"),
         aide("Une bobine s'oppose aux variations du courant qui la traverse : i₂ ne peut pas sauter de 0 à sa valeur finale. À la fin, i₁ = i₂.",
              "la bobine كتعارض les variations ديال le courant: i deux ما تقدرش تنقز من zéro ل la valeur النهائية. وفاللخر، i un égale i deux.")],
        corr([("1 : L₁ s'allume aussitôt ; L₂ s'allume progressivement, en retard.", "L un كتشعل دغيا"),
              ("Au bout d'un moment, les deux lampes brillent pareil (même résistance totale dans les deux branches).", "les deux lampes كيضويو بحال بحال"),
              ("La bobine s'oppose aux variations du courant : elle retarde l'établissement de i₂.", "la bobine كتعارض les variations ديال le courant")],
             "السؤال un. ملي كنسدو K، L un كتشعل دغيا، و L deux كتشعل بشوية، en retard. من بعد شوية، les deux lampes كيضويو بحال بحال، حيت نفس la résistance totale ف les deux branches. علاش الروطار؟ la bobine كتعارض les variations ديال le courant: كتأخر l'établissement ديال i deux."),
        "ex_rl3_1", "fa_rl3_1"),
      question("2", "Établir l'équation différentielle vérifiée par l'intensité i₂(t) du courant dans la branche 2.",
        "السؤال deux: أثبت l'équation différentielle اللي كتحققها i deux، le courant ديال la branche deux.",
        phrase(ATT2),
        ["u_L₂ + u_b = E", "u_L₂ = R_L·i₂", "u_b = L·di₂/dt + r·i₂"], ["u_b = L·di₂/dt (r oubliée)", "u_L₂ + u_b = 0"],
        [aide("La branche 2 est branchée directement aux bornes du générateur (K fermé) : quelle loi relie u_L₂, u_b et E ?",
              "la branche deux مربوطة مباشرة مع le générateur. أشمن loi كتربط u L deux و u b و E؟"),
         aide("u_L₂ + u_b = E, puis remplace u_L₂ = R_L·i₂ et u_b = L·di₂/dt + r·i₂, et regroupe les termes en i₂.",
              "u L deux plus u b égale E. من بعد عوض u L deux ب R L fois i deux، و u b ب L dé i deux sur dé t plus r i deux، وجمع les termes ديال i deux.")],
        corr([("2 : loi d'additivité dans la branche 2 : u_L₂ + u_b = E", "u L deux plus u b égale E"),
              ("R_L·i₂ + L·di₂/dt + r·i₂ = E", "R L fois i deux، plus L dé i deux sur dé t، plus r fois i deux"),
              ("L·di₂/dt + (R_L + r)·i₂ = E, soit di₂/dt + ((R_L + r)/L)·i₂ = E/L", "L dé i deux sur dé t، plus R L plus r، fois i deux، égale E")],
             "السؤال deux. la loi d'additivité ف la branche deux: u L deux plus u b égale E. كنعوضو: R L fois i deux، plus L dé i deux sur dé t، plus r fois i deux، égale E. كنجمعو: L dé i deux sur dé t، plus R L plus r، fois i deux، égale E. وإلى قسمنا على L، كنلقاو la forme الأخرى."),
        "ex_rl3_2", "fa_rl3_2"),
      question("3", "La solution s'écrit i₂(t) = A·(1 − e^(−t/τ)). Trouver les expressions de A et de τ en fonction de E, L, R_L et r.",
        "السؤال trois: la solution هي i deux égale A، fois un moins exponentielle de moins t sur tau. لقا l'expression ديال A و ديال tau.",
        phrase(ATT3),
        ["di₂/dt = (A/τ)·e^(−t/τ)", "pour tout t", "τ = …", "A = …"], ["τ = (R_L + r)/L", "A = E/R_L"],
        [aide("Calcule d'abord la dérivée di₂/dt, puis remplace i₂ et di₂/dt dans l'équation de la question 2.",
              "حسب الأول la dérivée dé i deux sur dé t، ومن بعد عوض i deux و dé i deux sur dé t ف l'équation ديال السؤال deux."),
         aide("Factorise par e^(−t/τ) : l'égalité est vraie pour tout t seulement si le coefficient de e^(−t/τ) est nul et si le terme constant vaut E.",
              "عمل الفاكتور ديال exponentielle de moins t sur tau. l'égalité صحيحة pour tout t غير إلى كان le coefficient ديال l'exponentielle égale zéro، و le terme constant égale E.")],
        corr([("3 : di₂/dt = (A/τ)·e^(−t/τ)", "dé i deux sur dé t égale A sur tau"),
              ("A·e^(−t/τ)·(L/τ − (R_L + r)) + (R_L + r)·A = E pour tout t", "pour tout t"),
              ("L/τ − (R_L + r) = 0 ⇒ τ = L/(R_L + r)", "tau égale L sur R L plus r"),
              ("(R_L + r)·A = E ⇒ A = E/(R_L + r)", "A égale E sur R L plus r")],
             "السؤال trois. dé i deux sur dé t égale A sur tau، fois exponentielle de moins t sur tau. كنعوضو و كنجمعو: A exponentielle de moins t sur tau، fois L sur tau moins R L plus r، plus R L plus r fois A، égale E، pour tout t. إذن le coefficient ديال l'exponentielle égale zéro: tau égale L sur R L plus r. و le terme constant: A égale E sur R L plus r."),
        "ex_rl3_3", "fa_rl3_3"),
      question("4", "Calculer la valeur I_p = A de l'intensité de i₂ en régime permanent.",
        "السؤال quatre: حسب I p، يعني A، la valeur ديال i deux فle régime permanent.",
        valeur("I_p", 0.2, "A", "I_p = A = E/(R_L + r) = 6/(20 + 10) = 0,2 A"),
        ["A = E/(R_L + r)", "R_L + r", "A"], ["I_p = E/r = 0,6 A", "I_p = E/R_L = 0,3 A"],
        [aide("En régime permanent, e^(−t/τ) → 0 : i₂ tend vers A. Utilise l'expression de A trouvée à la question 3.",
              "فle régime permanent، l'exponentielle كتمشي ل zéro، و i deux كتمشي ل A. استعمل l'expression ديال A ديال السؤال trois."),
         aide("A = E/(R_L + r) avec E = 6 V, R_L = 20 Ω et r = 10 Ω.",
              "A égale E sur R L plus r، مع E égale six volts، R L égale vingt ohms، و r égale dix ohms.")],
        corr([("4 : I_p = A = E/(R_L + r)", "I p égale A égale E sur R L plus r"),
              ("A.N. : I_p = 6/(20 + 10)", "six sur trente"),
              ("I_p = 0,2 A (même valeur que i₁ : même éclat final)", "zéro virgule deux ampère")],
             "السؤال quatre. I p égale A égale E sur R L plus r. l'application numérique: six sur trente، كتعطي zéro virgule deux ampère. نفس la valeur ديال i un، إذن نفس الضو فاللخر."),
        "ex_rl3_4", "fa_rl3_4"),
      question("5", "Calculer τ, puis la durée (en s) au bout de laquelle on peut considérer que L₂ brille comme L₁.",
        "السؤال cinq: حسب tau، ومن بعد la durée بla seconde، اللي من بعدها L deux كتضوي بحال L un.",
        valeur("t", 0.2, "s", "τ = L/(R_L + r) = 1,2/30 = 0,04 s ; t ≈ 5τ = 5 × 0,04 = 0,2 s"),
        ["τ = L/(R_L + r)", "t ≈ 5τ", "s"], ["t = τ = 0,04 s", "τ = L/r = 0,12 s"],
        [aide("L₂ brille comme L₁ quand i₂ a pratiquement atteint I_p : c'est le régime permanent. Au bout de combien de τ l'atteint-on ?",
              "L deux كتضوي بحال L un ملي i deux توصل تقريبا ل I p: هادا le régime permanent. من بعد شحال ديال tau كنوصلو ليه؟"),
         aide("τ = L/(R_L + r), puis t ≈ 5τ (à 5τ, i₂ ≈ 0,99·I_p).",
              "tau égale L sur R L plus r. ومن بعد t environ cinq tau: à cinq tau، i deux égale zéro virgule quatre-vingt-dix-neuf fois I p.")],
        corr([("5 : τ = L/(R_L + r) = 1,2/30 = 0,04 s", "tau égale un virgule deux sur trente"),
              ("Régime permanent pour t ≈ 5τ = 5 × 0,04", "cinq fois zéro virgule zéro quatre"),
              ("t ≈ 0,2 s : après 0,2 s, L₂ brille comme L₁.", "zéro virgule deux seconde")],
             "السؤال cinq. tau égale L sur R L plus r، يعني tau égale un virgule deux sur trente، كتعطي zéro virgule zéro quatre seconde. le régime permanent كيبدا à cinq tau: cinq fois zéro virgule zéro quatre، كتعطي zéro virgule deux seconde. من بعد هاد la durée، L deux كتضوي بحال L un."),
        "ex_rl3_5", "fa_rl3_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_rl3_1", "Question 1 : L₂ s'allume en retard", "L₁ s'allume aussitôt, L₂ en retard ; à la fin, même éclat. La bobine s'oppose aux variations de i.",
      LAMPES, "Deux branches de même résistance : seule la bobine les distingue",
      "شوف الدارة: la branche un فيها la lampe L un و R، و la branche deux فيها la lampe L deux و la bobine. K مازال محلول. دابا كنسدو K. L un كتشعل دغيا. شوف L deux: كتشعل بشوية، en retard. نتسناو شوية: les deux lampes كيضويو بحال بحال. علاش؟ la bobine كتعارض les variations ديال le courant: i deux ما كتنقزش، كتطلع بشوية.",
      centre=[("L₁ : aussitôt ; L₂ : en retard", "كتشعل بشوية، en retard"), ("la bobine s'oppose aux variations de i", "la bobine كتعارض les variations ديال le courant")],
      pointage=[{"mot": "شوف الدارة", "commande": "play_until", "parametres": {"moment": "k_ouvert"}},
                {"mot": "la branche un فيها la lampe L un و R", "repere": "lampe_R"},
                {"mot": "la branche deux فيها la lampe L deux و la bobine", "repere": "lampe_L"},
                {"mot": "دابا كنسدو K", "commande": "play_until", "parametres": {"moment": "k_ferme"}},
                {"mot": "شوف L deux", "commande": "play_until", "parametres": {"moment": "retard"}},
                {"mot": "كتشعل بشوية، en retard", "cible": "centre:0"},
                {"mot": "نتسناو شوية", "commande": "play_until", "parametres": {"moment": "egal"}},
                {"mot": "la bobine كتعارض les variations ديال le courant", "cible": "centre:1"}]),
    diapo_sim("ex_rl3_2", "Question 2 : l'équation différentielle", "u_L₂ + u_b = E ; R_L·i₂ + L·di₂/dt + r·i₂ = E ; L·di₂/dt + (R_L + r)·i₂ = E.",
      FIG_ED, "La méthode du cours : additivité, on remplace, on regroupe",
      "نفس الطريقة ديال الدرس. شوف la figure: le générateur، و la bobine. فالتمرين ديالنا، la résistance R ديال la figure هي la lampe، la résistance ديالها R L. السطر الأول: la loi d'additivité، u L deux plus u b égale E. السطر الثاني: كنعوضو. R L fois i deux، plus L dé i deux sur dé t، plus r i deux، égale E. السطر الثالث: كنجمعو R L i deux و r i deux. le résultat: L dé i deux sur dé t، plus R L plus r fois i deux، égale E.",
      centre=[("u_L₂ + u_b = E", "u L deux plus u b égale E"), ("L·di₂/dt + (R_L + r)·i₂ = E", "le résultat: L dé i deux sur dé t")],
      pointage=[{"mot": "شوف la figure", "commande": "play_until", "parametres": {"moment": "circuit"}},
                {"mot": "السطر الأول", "commande": "play_until", "parametres": {"moment": "additivite"}},
                {"mot": "u L deux plus u b égale E", "cible": "centre:0"},
                {"mot": "السطر الثاني: كنعوضو", "commande": "play_until", "parametres": {"moment": "remplacer"}},
                {"mot": "السطر الثالث", "commande": "play_until", "parametres": {"moment": "regrouper"}},
                {"mot": "le résultat: L dé i deux sur dé t", "commande": "play_until", "parametres": {"moment": "resultat"}}]),
    diapo_sim("ex_rl3_3", "Question 3 : A et τ", "On remplace i₂ = A(1 − e^(−t/τ)) : τ = L/(R_L + r) et A = E/(R_L + r).",
      FIG_RES, "Dériver, remplacer, factoriser : deux conditions pour tout t",
      "شوف la forme ديال la solution: A fois un moins exponentielle de moins t sur tau. الأول la dérivée: A sur tau fois exponentielle de moins t sur tau. من بعد كنعوضو فl'équation. ومن بعد كنعملو الفاكتور ديال l'exponentielle. هاد l'égalité صحيحة pour tout t، إذن deux conditions: le coefficient ديال l'exponentielle égale zéro، و le terme constant égale E. le résultat: tau égale L sur R plus r، و A égale E sur R plus r. فالتمرين ديالنا R هي R L: tau égale L sur R L plus r، و A égale E sur R L plus r.",
      centre=[("τ = L/(R_L + r)", "tau égale L sur R L plus r"), ("A = E/(R_L + r)", "A égale E sur R L plus r")],
      pointage=[{"mot": "شوف la forme ديال la solution", "commande": "play_until", "parametres": {"moment": "forme"}},
                {"mot": "الأول la dérivée", "commande": "play_until", "parametres": {"moment": "deriver"}},
                {"mot": "من بعد كنعوضو فl'équation", "commande": "play_until", "parametres": {"moment": "remplacer"}},
                {"mot": "ومن بعد كنعملو الفاكتور", "commande": "play_until", "parametres": {"moment": "factoriser"}},
                {"mot": "deux conditions", "commande": "play_until", "parametres": {"moment": "accolade"}},
                {"mot": "le résultat:", "commande": "play_until", "parametres": {"moment": "resultat"}},
                {"mot": "tau égale L sur R L plus r", "cible": "centre:0"},
                {"mot": "A égale E sur R L plus r", "cible": "centre:1"}]),
    diapo_sim("ex_rl3_4", "Question 4 : I_p = E/(R_L + r)", "I_p = A = 6/(20 + 10) = 0,2 A = 200 mA, la même valeur que i₁.",
      LAMPES, "À la fin, i₁ et i₂ valent 200 mA : les lampes brillent pareil",
      "شوف الدارة: E égale six volts، و la bobine، r égale dix ohms. la lampe كنعتبروها بحال vingt ohms. كنسدو K، ونتسناو le régime permanent. i deux كتوصل ل A égale E sur R L plus r. six sur vingt plus dix، يعني six sur trente، كتعطي zéro virgule deux ampère، deux cents milliampères. شوف: i un حتى هي deux cents milliampères، حيت r égale R.",
      centre=[("I_p = A = E/(R_L + r)", "i deux كتوصل ل A égale E sur R L plus r"), ("I_p = 6/30 = 0,2 A = 200 mA", "كتعطي zéro virgule deux ampère")],
      pointage=[{"mot": "E égale six volts", "repere": "generateur"},
                {"mot": "r égale dix ohms", "repere": "bobine"},
                {"mot": "ونتسناو le régime permanent", "commande": "play_until", "parametres": {"moment": "egal"}},
                {"mot": "i deux كتوصل ل A égale E sur R L plus r", "cible": "centre:0"},
                {"mot": "كتعطي zéro virgule deux ampère", "repere": "lampe_L"},
                {"mot": "i un حتى هي deux cents milliampères", "repere": "lampe_R"}]),
    diapo_sim("ex_rl3_5", "Question 5 : τ puis 5τ", "τ = 1,2/30 = 0,04 s ; régime permanent à 5τ = 0,2 s.",
      LAMPES, "Avec le noyau, L = 1,2 H : le retard de L₂ dure environ 5τ",
      "شوف la bobine: مع le noyau de fer، L égale un virgule deux henry. tau égale L sur R L plus r، يعني un virgule deux sur trente، كتعطي zéro virgule zéro quatre seconde، quarante millisecondes. كنسدو K: L deux كتشعل بشوية. ف tau، i deux وصلات غير ل soixante-trois pour cent. خاصنا cinq tau: cinq fois zéro virgule zéro quatre، يعني zéro virgule deux seconde. من بعد، les deux lampes بحال بحال.",
      centre=[("τ = L/(R_L + r) = 1,2/30 = 0,04 s", "كتعطي zéro virgule zéro quatre seconde"), ("t ≈ 5τ = 0,2 s", "يعني zéro virgule deux seconde")],
      pointage=[{"mot": "مع le noyau de fer", "repere": "noyau"},
                {"mot": "كتعطي zéro virgule zéro quatre seconde", "cible": "centre:0"},
                {"mot": "كنسدو K", "commande": "play_until", "parametres": {"moment": "retard"}},
                {"mot": "خاصنا cinq tau", "commande": "play_until", "parametres": {"moment": "egal"}},
                {"mot": "يعني zéro virgule deux seconde", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    vrai_faux_facile("fa_rl3_1", "Plus facile : ce qu'on voit", "سؤال ساهل على l'expérience ديال les deux lampes.",
      "On ferme K : L₁ est en série avec R, L₂ avec la bobine (r = R).",
      [("L₁ s'allume aussitôt.", True, "La branche de L₁ ne contient pas de bobine : i₁ s'établit tout de suite."),
       ("L₂ s'allume en retard.", True, "La bobine s'oppose aux variations du courant : i₂ monte progressivement."),
       ("À la fin, L₂ brille moins que L₁ à cause de la bobine.", False, "À la fin i₂ = E/(R_L + r) = i₁ (r = R) : même éclat. La bobine retarde, elle ne change pas la valeur finale.")]),
    association_facile("fa_rl3_2", "Plus facile : les tensions de la branche 2", "سؤال ساهل: ربط كل tension بl'expression ديالها.",
      "Branche 2 : lampe L₂ (R_L) et bobine (L, r), en série, aux bornes de E.",
      "Associe chaque tension à son expression.",
      [("1", "u_L₂ (lampe)"), ("2", "u_b (bobine)"), ("3", "u_L₂ + u_b")],
      [("a", "R_L·i₂"), ("b", "L·di₂/dt + r·i₂"), ("c", "E")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Juste : la lampe est un conducteur ohmique, u = R_L·i₂.", "صحيح: la lampe بحال un conducteur ohmique، u égale R L fois i deux."),
       "1-b": (False, "La lampe n'a pas d'inductance : pas de terme en di₂/dt.", "la lampe ما عندهاش l'inductance، إذن ما كاينش dé i sur dé t. قلب على la loi d'Ohm."),
       "1-c": (False, "E est la tension de toute la branche, pas de la lampe seule.", "E هي la tension ديال la branche كاملة، ماشي غير la lampe."),
       "2-a": (False, "Une bobine n'est pas qu'une résistance : il manque le terme L·di₂/dt.", "la bobine ماشي غير résistance، خاص الجزء L dé i sur dé t."),
       "2-b": (True, "Juste : u_b = L·di₂/dt + r·i₂ (bobine de résistance r).", "صحيح: u b égale L dé i deux sur dé t plus r i deux."),
       "2-c": (False, "u_b n'est égale à E qu'à t = 0 ; en général u_b = L·di₂/dt + r·i₂.", "u b ماشي ديما E، قلب على l'expression ديال la bobine."),
       "3-a": (False, "R_L·i₂, c'est la lampe seule ; la somme des deux tensions est celle du générateur.", "R L i deux غير la lampe. المجموع ديال les deux tensions شنو كيعطي؟"),
       "3-b": (False, "C'est la bobine seule ; la somme vaut la tension du générateur.", "هادي غير la bobine. المجموع كيساوي la tension ديال le générateur."),
       "3-c": (True, "Juste : loi d'additivité, u_L₂ + u_b = E.", "صحيح: la loi d'additivité، u L deux plus u b égale E.")},
      "(1 ; a) (2 ; b) (3 ; c) : R_L·i₂ + L·di₂/dt + r·i₂ = E.",
      "الجواب: un مع a، deux مع b، trois مع c. إذن R L i deux plus L dé i deux sur dé t plus r i deux égale E."),
    qcm_facile("fa_rl3_3", "Plus facile : identifier τ", "سؤال ساهل: من l'équation، لقا tau.",
      "L·di₂/dt + (R_L + r)·i₂ = E et i₂ = A(1 − e^(−t/τ)). Alors τ = …",
      ["L/(R_L + r)", "(R_L + r)/L", "L·(R_L + r)"], 0, {
        "0": {"juste": rep("برافو! tau égale L sur R L plus r، و A égale E sur R L plus r.", "Juste : τ = L/(R_L + r) (et A = E/(R_L + r)).")},
        "1": {"1": rep("هادا هو un sur tau، le coefficient ديال i فla forme المقسومة على L. tau هو المقلوب ديالو. عاود.", "(R_L + r)/L, c'est 1/τ. Réessaie."),
              "2": rep("الجواب هو tau égale L sur R L plus r. R L plus r sur L هي un sur tau.", "Réponse : τ = L/(R_L + r) ; (R_L + r)/L = 1/τ.")},
        "2": {"1": rep("شوف l'unité: tau خاصها تكون seconde. واش henry fois ohm كتعطي seconde؟ عاود.", "τ doit être un temps : henry × ohm n'en est pas un. Réessaie."),
              "2": rep("الجواب هو tau égale L sur R L plus r: henry sur ohm كتعطي seconde.", "Réponse : τ = L/(R_L + r) (H/Ω = s).")}},
      "L dé i deux sur dé t plus R L plus r fois i deux égale E. Alors tau égale ?"),
    qcm_facile("fa_rl3_4", "Plus facile : la valeur finale", "سؤال ساهل على la valeur النهائية ديال i deux.",
      "E = 6 V, R_L = 20 Ω, r = 10 Ω. En régime permanent, i₂ vaut…",
      ["0,6 A", "0,2 A", "0,3 A"], 1, {
        "1": {"juste": rep("برافو! six sur vingt plus dix، يعني six sur trente، كتعطي zéro virgule deux ampère.", "Juste : I_p = 6/30 = 0,2 A.")},
        "0": {"1": rep("قسمتي غير على r. ولكن la lampe حتى هي فla branche. عاود.", "Tu as divisé par r seulement ; la lampe est aussi dans la branche. Réessaie."),
              "2": rep("الجواب هو zéro virgule deux ampère: E sur R L plus r.", "Réponse : E/(R_L + r) = 0,2 A.")},
        "2": {"1": rep("نسيتي la résistance ديال la bobine. عاود.", "Tu as oublié la résistance r de la bobine. Réessaie."),
              "2": rep("الجواب هو zéro virgule deux ampère: six sur vingt plus dix.", "Réponse : 6/(20 + 10) = 0,2 A.")}},
      "E égale six volts، R L égale vingt ohms، r égale dix ohms. En régime permanent، i deux vaut ?"),
    qcm_facile("fa_rl3_5", "Plus facile : la durée du retard", "سؤال ساهل على la durée ديال le régime transitoire.",
      "τ = 40 ms. L₂ atteint pratiquement son éclat final au bout de…",
      ["40 ms", "200 ms", "8 ms"], 1, {
        "1": {"juste": rep("برافو! cinq fois quarante، يعني deux cents millisecondes.", "Juste : 5τ = 200 ms.")},
        "0": {"1": rep("ف tau، i deux وصلات غير ل soixante-trois pour cent. خاص وقت كتر. عاود.", "À τ, i₂ n'est qu'à 63 % de sa valeur finale. Réessaie."),
              "2": rep("الجواب هو deux cents millisecondes: cinq tau، ماشي tau.", "Réponse : 5τ = 200 ms (à τ seulement 63 %).")},
        "2": {"1": rep("قسمتي على cinq، والصحيح نضربو. عاود.", "Il faut multiplier par 5, pas diviser. Réessaie."),
              "2": rep("الجواب هو cinq fois tau، يعني deux cents millisecondes.", "Réponse : 5τ = 5 × 40 = 200 ms.")}},
      "tau égale quarante millisecondes. L deux atteint son éclat final au bout de ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage avec d'autres valeurs : E = 12 V, lampes identiques de résistance R_L = 30 Ω, R = r = 10 Ω, bobine d'inductance L = 0,8 H. À t = 0, on ferme K.",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale douze volts، R L égale trente ohms، R égale r égale dix ohms، و L égale zéro virgule huit henry.",
      "figures": [montage("Figure : deux lampes, deux branches")],
      "donnees": ["E = 12 V", "R = r = 10 Ω", "R_L = 30 Ω", "L = 0,8 H"],
      "questions": [
        question_semblable("1", "Décrire ce qu'on observe sur les deux lampes après la fermeture de K, puis justifier le comportement de L₂.",
          phrase(ATT1), ["en retard", "la bobine s'oppose aux variations de i"], ["L₂ brille moins à la fin"],
          corr([("1 : L₁ s'allume aussitôt, L₂ en retard ; à la fin, même éclat.", "L deux كتشعل en retard"),
                ("La bobine s'oppose aux variations du courant : elle retarde l'établissement de i₂.", "la bobine كتعارض les variations ديال le courant")],
               "L un كتشعل دغيا، و L deux كتشعل en retard، وفاللخر بحال بحال. حيت la bobine كتعارض les variations ديال le courant.")),
        question_semblable("2", "Établir l'équation différentielle vérifiée par l'intensité i₂(t) du courant dans la branche 2.",
          phrase(ATT2), ["u_L₂ + u_b = E", "u_b = L·di₂/dt + r·i₂"], ["u_b = L·di₂/dt"],
          corr([("2 : u_L₂ + u_b = E ; R_L·i₂ + L·di₂/dt + r·i₂ = E", "u L deux plus u b égale E"),
                ("L·di₂/dt + (R_L + r)·i₂ = E", "L dé i deux sur dé t، plus R L plus r")],
               "u L deux plus u b égale E. كنعوضو وكنجمعو: L dé i deux sur dé t، plus R L plus r، fois i deux، égale E.")),
        question_semblable("3", "La solution s'écrit i₂(t) = A·(1 − e^(−t/τ)). Trouver les expressions de A et de τ.",
          phrase(ATT3), ["pour tout t", "τ = …", "A = …"], ["τ = (R_L + r)/L"],
          corr([("3 : A·e^(−t/τ)·(L/τ − (R_L + r)) + (R_L + r)·A = E pour tout t", "pour tout t"),
                ("τ = L/(R_L + r) ; A = E/(R_L + r)", "tau égale L sur R L plus r")],
               "كنعوضو، وكنعملو الفاكتور. pour tout t: tau égale L sur R L plus r، و A égale E sur R L plus r.")),
        question_semblable("4", "Calculer la valeur I_p = A de l'intensité de i₂ en régime permanent.",
          valeur("I_p", 0.3, "A", "I_p = E/(R_L + r) = 12/(30 + 10) = 0,3 A"), ["A = E/(R_L + r)", "A"], ["I_p = E/r"],
          corr([("4 : I_p = E/(R_L + r) = 12/40", "I p égale E sur R L plus r"), ("I_p = 0,3 A", "zéro virgule trois ampère")],
               "I p égale E sur R L plus r، يعني douze sur quarante، كتعطي zéro virgule trois ampère.")),
        question_semblable("5", "Calculer τ, puis la durée (en s) au bout de laquelle on peut considérer que L₂ brille comme L₁.",
          valeur("t", 0.1, "s", "τ = 0,8/40 = 0,02 s ; t ≈ 5τ = 5 × 0,02 = 0,1 s"), ["τ = L/(R_L + r)", "t ≈ 5τ"], ["t = τ"],
          corr([("5 : τ = L/(R_L + r) = 0,8/40 = 0,02 s", "tau égale zéro virgule huit sur quarante"), ("t ≈ 5τ = 0,1 s", "zéro virgule un seconde")],
               "tau égale zéro virgule huit sur quarante، كتعطي zéro virgule zéro deux seconde. à cinq tau: zéro virgule un seconde.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
