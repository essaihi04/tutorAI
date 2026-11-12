# -*- coding: utf-8 -*-
"""Partie B de l'exploration circuit_RLC : compétences, séances et plan des diapositives.
Préfixe des diapositives du futur cours phys_ch8_circuit_RLC : lc_ (ids courts ici, comme au RL).
Tous les calculs des rappels et des diapositives sont refaits dans verifier_calculs() (bas du fichier)."""
from math import pi, sqrt, cos, acos

def R(id, type, prompt, **kw):
    d = {"id": id, "type": type, "prompt": prompt}; d.update(kw); return d

competences = [
 {"id": "C1", "verbe": "Décrire la décharge d'un condensateur chargé dans une bobine (oscillations libres), relier i = dq/dt = C·du_C/dt et trouver son signe, et donner u_b(0⁺) par la continuité de i", "cadre_ids": ["RLC1"],
  "rappels": [R("C1_r1", "qcm", "Un condensateur chargé se décharge dans une bobine de faible résistance. La tension u_C :", options=["descend vers 0 sans changer de signe", "oscille autour de 0 en changeant de signe", "reste constante", "monte vers 2E"], correct=1),
              R("C1_r2", "vrai_faux", "Au moment où u_C passe par 0, l'intensité i est nulle aussi.", correct=False),
              R("C1_r3", "libre", "C = 10 µF ; u_C diminue régulièrement de 2 V en 1 ms. i = C·du_C/dt = ?", attendu="du_C/dt = −2/10⁻³ = −2000 V/s ; i = 10⁻⁵ × (−2000) = −0,02 A = −20 mA (i < 0 car u_C diminue)"),
              R("C1_r4", "libre", "Condensateur chargé sous E = 5 V ; à t = 0, K bascule sur R et la bobine. u_b(0⁺) = ?", attendu="i(0⁺) = 0 (i continue dans la bobine) → u_R(0⁺) = 0 → u_b(0⁺) = −u_C(0) = −5 V")]},
 {"id": "C2", "verbe": "Reconnaître les régimes (périodique, pseudo-périodique, apériodique ; critique = frontière) et prévoir l'influence de la résistance totale R + r", "cadre_ids": ["RLC2"],
  "rappels": [R("C2_r1", "qcm", "Les sommets de u_C diminuent mais la courbe change toujours de signe. Le régime est :", options=["périodique", "apériodique", "pseudo-périodique", "critique"], correct=2),
              R("C2_r2", "vrai_faux", "Plus la résistance totale du circuit est grande, plus l'amortissement est fort.", correct=True),
              R("C2_r3", "qcm", "u_C revient vers 0 sans jamais changer de signe. Le régime est :", options=["pseudo-périodique", "apériodique (ou critique)", "périodique"], correct=1),
              R("C2_r4", "vrai_faux", "C'est la résistance qui fait osciller le circuit.", correct=False)]},
 {"id": "C3", "verbe": "Établir l'équation différentielle vérifiée par q ou par u_C (circuit RLC avec r, puis LC idéal)", "cadre_ids": ["RLC3"],
  "rappels": [R("C3_r1", "libre", "Après la bascule (condensateur, R, bobine L, r), écris la loi d'additivité des tensions.", attendu="u_C + u_R + u_b = 0 (pas de générateur dans la maille)"),
              R("C3_r2", "qcm", "Dans l'équation de la décharge, le second membre vaut :", options=["E", "0", "E/L", "q/C"], correct=1),
              R("C3_r3", "libre", "L = 0,1 H, R + r = 20 Ω, C = 10 µF. Écris l'équation en q avec les nombres.", attendu="0,1·d²q/dt² + 20·dq/dt + 10⁵·q = 0 (1/C = 1/10⁻⁵ = 10⁵)"),
              R("C3_r4", "qcm", "Pour un circuit LC idéal, l'équation en u_C est :", options=["du_C/dt + u_C/(LC) = 0", "d²u_C/dt² + LC·u_C = 0", "d²u_C/dt² − u_C/(LC) = 0", "d²u_C/dt² + u_C/(LC) = 0"], correct=3)]},
 {"id": "C4", "verbe": "Vérifier que u_C = U_m·cos(2πt/T₀ + φ) est solution du LC, en déduire T₀ = 2π√(LC), montrer que √(LC) est un temps, et trouver U_m et φ avec les conditions initiales", "cadre_ids": ["RLC4"],
  "rappels": [R("C4_r1", "libre", "L = 0,1 H, C = 10 µF. T₀ = ?", attendu="LC = 10⁻⁶ s², √(LC) = 10⁻³ s ; T₀ = 2π × 10⁻³ ≈ 6,3·10⁻³ s = 6,3 ms"),
              R("C4_r2", "qcm", "On multiplie C par 4 (L inchangée). T₀ est :", options=["inchangée", "multipliée par 4", "divisée par 2", "multipliée par 2"], correct=3),
              R("C4_r3", "libre", "Dérive deux fois u_C = U_m·cos(2πt/T₀).", attendu="du_C/dt = −(2π/T₀)·U_m·sin(2πt/T₀) ; d²u_C/dt² = −(2π/T₀)²·U_m·cos(2πt/T₀) = −(2π/T₀)²·u_C"),
              R("C4_r4", "libre", "U_m = 6 V ; u_C(0) = 0 et u_C augmente au départ. φ = ?", attendu="cos φ = 0 → φ = ±π/2 ; du_C/dt(0) = −(2π/T₀)·U_m·sin φ > 0 → sin φ < 0 → φ = −π/2 rad")]},
 {"id": "C5", "verbe": "Exploiter un oscillogramme : lire T sur plusieurs périodes, utiliser T ≈ T₀, calculer L ou C (π² = 10), prévoir l'influence de L et de C", "cadre_ids": ["RLC5"],
  "rappels": [R("C5_r1", "libre", "Entre le 1er et le 4e sommet de u_C, on lit 12 ms. T = ?", attendu="du 1er au 4e sommet : 3 pseudo-périodes ; T = 12/3 = 4 ms"),
              R("C5_r2", "libre", "T₀ = 4 ms, C = 4 µF, π² = 10. L = ?", attendu="T₀² = 4π²·L·C → L = T₀²/(4π²·C) = 16·10⁻⁶/(40 × 4·10⁻⁶) = 0,1 H"),
              R("C5_r3", "qcm", "La durée entre un sommet de u_C et le creux qui suit vaut :", options=["T", "2T", "T/2", "T/4"], correct=2),
              R("C5_r4", "vrai_faux", "Si on charge le condensateur sous une tension deux fois plus grande, la période T₀ double.", correct=False)]},
 {"id": "C6", "verbe": "Exprimer l'énergie totale E = ½·C·u_C² + ½·L·i², décrire l'échange entre condensateur et bobine et utiliser sa conservation quand R + r = 0", "cadre_ids": ["RLC6"],
  "rappels": [R("C6_r1", "libre", "C = 10 µF chargé sous E = 6 V, i = 0. Énergie totale ?", attendu="E = ½·C·E² = ½ × 10⁻⁵ × 36 = 1,8·10⁻⁴ J"),
              R("C6_r2", "qcm", "Circuit LC idéal : quand u_C = 0, l'énergie du circuit est :", options=["toute dans le condensateur", "partagée moitié-moitié", "nulle", "toute dans la bobine"], correct=3),
              R("C6_r3", "libre", "LC idéal (2019 N) : E = 5·10⁻⁴ J, C = 10 µF, u_C = −8 V. E_m = ?", attendu="E_e = ½ × 10⁻⁵ × 64 = 3,2·10⁻⁴ J ; E_m = E − E_e = 5·10⁻⁴ − 3,2·10⁻⁴ = 1,8·10⁻⁴ J"),
              R("C6_r4", "libre", "2019 R : C = 5 µF, L = 0,5 H ; à 9 ms, u_C = 4,8 V et i = 12 mA. Énergie totale ?", attendu="½ × 5·10⁻⁶ × 4,8² = 5,76·10⁻⁵ J ; ½ × 0,5 × (12·10⁻³)² = 3,6·10⁻⁵ J ; E = 9,36·10⁻⁵ J (les deux termes)")]},
 {"id": "C7", "verbe": "Expliquer l'amortissement par l'effet Joule, montrer dE/dt = −(R + r)·i², calculer l'énergie perdue entre deux instants et identifier les courbes d'énergie", "cadre_ids": ["RLC7"],
  "rappels": [R("C7_r1", "qcm", "Dans un circuit RLC série, dE/dt vaut :", options=["−(R + r)·i²", "−(R + r)·i", "(R + r)·i²", "0"], correct=0),
              R("C7_r2", "libre", "C = 10 µF ; deux sommets successifs de u_C : 6 V puis 4 V. Énergie perdue ?", attendu="aux sommets i = 0 : |ΔE| = ½·C·(6² − 4²) = ½ × 10⁻⁵ × 20 = 10⁻⁴ J"),
              R("C7_r3", "vrai_faux", "Dans un circuit RLC (R + r ≠ 0), l'énergie totale reste constante.", correct=False),
              R("C7_r4", "qcm", "L'énergie perdue par le circuit devient :", options=["de l'énergie magnétique", "de l'énergie rendue au générateur", "de la chaleur dans les résistances (effet Joule)"], correct=2)]},
 {"id": "C8", "verbe": "Expliquer l'entretien par un générateur u_G = k·i : établir l'équation, montrer que k = R + r, et savoir que le circuit oscille alors à T₀", "cadre_ids": ["RLC8"],
  "rappels": [R("C8_r1", "libre", "R = 10 Ω, r = 8 Ω. Quelle valeur de k donne des oscillations entretenues ?", attendu="k = R + r = 18 Ω"),
              R("C8_r2", "qcm", "Avec u_G = k·i et k = R + r, la période des oscillations est :", options=["plus grande que T₀", "égale à T₀", "imposée par le générateur"], correct=1),
              R("C8_r3", "vrai_faux", "Si k est plus petit que R + r, les oscillations restent amorties.", correct=True),
              R("C8_r4", "libre", "Écris l'équation en q avec le générateur u_G = k·i (R, bobine L et r, condensateur C).", attendu="u_C + u_R + u_b = u_G → L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0")]},
]

def D(id, title, lead, marche, visuel, question, comp, demo, prediction=False, **kw):
    d = {"id": id, "title": title, "lead": lead, "marche": marche, "visuel": visuel, "question": question,
         "prediction": prediction, "competences": comp, "demonstration": demo}
    d.update(kw); return d

diapositives = [
 # Séance 1 — la décharge oscillante et les régimes
 D("o1", "La carte du chapitre : un condensateur qui se vide dans une bobine", "Que va-t-on savoir faire avec un circuit RLC ?", "carte : décharge dans la bobine → équation → LC : solution, T₀ → conditions initiales → régimes → énergie → entretien → oscillogrammes ; « le RLC tombe dans 17 sessions sur 20 : lire T et trouver L ou C dans 13, une énergie dans 14 »", "v_carte (centre, branches)", "Au national, quelles sont les deux questions presque toujours posées ?", ["C5", "C6"], ["Lire la période sur la courbe et en déduire L ou C (13 sessions sur 17).", "Calculer une énergie ½·C·u_C² + ½·L·i² (14 sessions sur 17)."]),
 D("o2", "Trois gestes à avoir en main", "Vérifions les bases avant de commencer.", "une question par prérequis : i = dq/dt et q = C·u_C (RC), u_b = L·di/dt + r·i (RL), dérivée d'un cosinus ; un échec déclenche le rappel ; on annonce la même recette qu'au RC et au RL : additivité, équation, solution", "v_circuit_lc (montage)", "Dérive f(t) = cos(2πt/T₀).", ["C3", "C4"], ["f′(t) = −(2π/T₀)·sin(2πt/T₀)."]),
 D("d1", "Rappel : décharge dans une résistance", "Que fait u_C quand le condensateur se vide dans R seule ?", "montage du RC : K bascule sur R ; u_C descend de E vers 0 sans passer en dessous", "v_circuit_lc (bascule)", "Au RC, u_C peut-elle devenir négative pendant la décharge ?", ["C1"], ["Non : u_C = E·e^(−t/τ) reste positive et tend vers 0."], prediction=True),
 D("d2", "On remplace R par une bobine", "Que fait u_C quand le condensateur se vide dans une bobine ?", "même montage, K bascule sur la bobine : u_C descend, passe par 0, devient négative, remonte… comme une vague", "v_circuit_lc (bascule)", "Après être passée par 0, u_C va-t-elle s'arrêter ou continuer ?", ["C1"], ["Elle continue : u_C devient négative puis remonte ; elle oscille autour de 0."], prediction=True),
 # bloc 2
 D("d3", "Condensateur vide, courant maximal", "Pourquoi u_C dépasse-t-elle 0 ?", "arrêt sur image à u_C = 0 : le courant est maximal ; la bobine s'oppose à sa diminution (RL) ; les électrons continuent et chargent l'armature d'en face", "v_circuit_lc (bascule : u_nulle_i_max, recharge_inverse)", "Au moment où u_C = 0, le courant est-il nul ou maximal ?", ["C1"], ["Maximal : la bobine garde le courant, qui recharge le condensateur à l'envers."], prediction=True),
 D("d4", "Oscillations libres", "Comment appelle-t-on ce va-et-vient ?", "le cycle recommence dans l'autre sens ; écrit au cahier : condensateur chargé + bobine (L, r) + R en série, sans générateur → oscillations électriques libres ; image de la balançoire lâchée", "v_circuit_lc (retour, periode)", "Pourquoi dit-on « libres » ?", ["C1"], ["Aucun générateur n'est dans le circuit pendant les oscillations : le condensateur et la bobine échangent seuls l'énergie de départ."]),
 D("d5", "i = dq/dt et son signe", "Comment savoir si i est positif ou négatif ?", "flèches i et u_C du schéma ; i = dq/dt = C·du_C/dt : quand u_C diminue, i < 0 ; quand u_C augmente, i > 0 (2025 N 2.2.2)", "v_solution (cos)", "Entre deux instants, u_C diminue. Quel est le signe de i ?", ["C1"], ["i = C·du_C/dt.", "u_C diminue, donc du_C/dt < 0, donc i < 0.", "Exemple : C = 10 µF, u_C perd 2 V en 1 ms → i = 10⁻⁵ × (−2000) = −0,02 A."]),
 D("d6", "u_b juste après la bascule", "Que vaut la tension de la bobine au tout début ?", "i est continue dans la bobine : i(0⁺) = 0 → u_R(0⁺) = 0 ; additivité u_C + u_R + u_b = 0 → u_b(0⁺) = −u_C(0) (2024 R 2.1.1)", "v_equation (fleches)", "E = 5 V. Juste après la bascule, que vaut u_b ?", ["C1"], ["i(0⁺) = i(0⁻) = 0 (continuité dans la bobine), donc u_R(0⁺) = R·0 = 0.", "u_b(0⁺) = −u_C(0) − u_R(0⁺) = −5 V."], prediction=True),
 # bloc 3
 D("r1", "Une petite résistance : les sommets baissent", "Que change une résistance dans le circuit ?", "R petite : u_C oscille, chaque sommet plus bas que le précédent ; la durée entre deux sommets reste presque la même ; nom : régime pseudo-périodique, T = pseudo-période", "v_oscillogramme (pseudo : trace, sommets_decroissants)", "Avec une petite R, les sommets de u_C gardent-ils la même hauteur ?", ["C2"], ["Non : ils diminuent, c'est le régime pseudo-périodique."], prediction=True),
 D("r2", "Une grande résistance : plus d'oscillation", "Et si la résistance devient très grande ?", "R grande : u_C revient vers 0 sans changer de signe : régime apériodique ; entre les deux, une valeur frontière où le retour est le plus rapide sans oscillation : régime critique (on ne la calcule pas)", "v_oscillogramme (aperiodique, critique : poignée R)", "Avec une très grande R, u_C change-t-elle encore de signe ?", ["C2"], ["Non : elle revient vers 0 sans osciller (régime apériodique)."], prediction=True),
 D("r3", "La résistance totale décide du régime", "Comment ranger les trois régimes ?", "les trois courbes côte à côte puis la sinusoïde du LC (R + r = 0 : régime périodique) ; plus R + r est grande, plus l'amortissement est fort ; c'est L et C qui font osciller, R + r amortit", "v_oscillogramme (periodique, pseudo, aperiodique)", "Range du moins amorti au plus amorti : apériodique, périodique, pseudo-périodique.", ["C2"], ["Périodique (R + r = 0), puis pseudo-périodique (petite R), puis apériodique (grande R)."]),
 D("r4", "Exercice du national : à chaque courbe sa résistance", "Comment le national pose-t-il les régimes ?", "2021 R III.1 : bobine (L = 0,51 H, r = 5 Ω), C = 100 µF ; courbe (a) peu amortie, courbe (b) très amortie ; R₃ = 10 Ω et R₄ = 100 Ω à affecter ; 2020 R : R₂ = 390 Ω → apériodique", "v_figures (fig=2021R)", "Laquelle des deux résistances donne la courbe (b), très amortie ?", ["C2"], ["Plus la résistance totale est grande, plus l'amortissement est fort.", "R₄ + r = 105 Ω > R₃ + r = 15 Ω : la courbe (b) correspond à R₄ = 100 Ω, la courbe (a) à R₃ = 10 Ω."], prediction=True),
 # Séance 2 — l'équation différentielle et la période propre
 D("e1", "La loi d'additivité, sans générateur", "Quelle relation relie les tensions après la bascule ?", "circuit fermé condensateur, R, bobine ; flèches u_C, u_R, u_b en convention récepteur ; même recette qu'au RC et au RL : u_C + u_R + u_b = 0", "v_equation (fleches, additivite)", "Après la bascule, le second membre de la loi d'additivité vaut-il E ou 0 ?", ["C3"], ["0 : le générateur n'est plus dans la maille ; u_C + u_R + u_b = 0."], prediction=True),
 D("e2", "Remplacer chaque tension", "Que met-on à la place de u_C, u_R et u_b ?", "u_C = q/C ; u_R = R·i ; u_b = L·di/dt + r·i → q/C + R·i + L·di/dt + r·i = 0", "v_equation (remplacer)", "Quels termes contiennent i sans dérivée ?", ["C3"], ["R·i et r·i : on les regroupe en (R + r)·i."]),
 D("e3", "Tout écrire avec q : on dérive deux fois", "Comment n'avoir qu'une seule fonction inconnue ?", "i = dq/dt, donc di/dt = d²q/dt² ; L·d²q/dt² + (R + r)·dq/dt + q/C = 0 : première équation du second ordre", "v_equation (deriver_deux_fois, equation_q)", "Que vaut di/dt en fonction de q ?", ["C3"], ["i = dq/dt, donc di/dt = d²q/dt².", "L·d²q/dt² + (R + r)·dq/dt + q/C = 0."]),
 D("e4", "La même équation en u_C", "Et si l'énoncé demande l'équation vérifiée par u_C ?", "q = C·u_C : i = C·du_C/dt, di/dt = C·d²u_C/dt² → LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0 ; on divise par LC (forme des corrigés)", "v_equation (equation_uc)", "Divise LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0 par LC.", ["C3"], ["d²u_C/dt² + ((R + r)/L)·du_C/dt + u_C/(LC) = 0."]),
 # bloc 2
 D("e5", "Le circuit LC idéal", "Que devient l'équation sans aucune résistance ?", "R + r = 0 : le terme du milieu est barré ; d²u_C/dt² + u_C/(LC) = 0 (ou d²q/dt² + q/(LC) = 0) ; la courbe : sommets tous à la même hauteur", "v_equation (lc_ideal)", "Si R + r = 0, quel terme disparaît, et les sommets baissent-ils encore ?", ["C3", "C2"], ["Le terme en du_C/dt disparaît.", "Plus de perte : l'amplitude reste constante (régime périodique)."], prediction=True),
 D("e6", "Une sinusoïde comme solution", "Quelle fonction a cette forme ?", "u_C(t) du LC : même hauteur U_m à chaque sommet, même durée T₀ entre deux sommets ; on propose u_C = U_m·cos(2πt/T₀ + φ) ; U_m amplitude, T₀ période propre, φ phase à l'origine", "v_solution (cos : courbe, Um, T0)", "Sur la courbe, où lit-on T₀ ?", ["C4"], ["Entre deux sommets successifs (deux maxima) : c'est la période propre T₀."]),
 D("e7", "Dériver deux fois un cosinus", "Que vaut d²u_C/dt² ?", "du_C/dt = −(2π/T₀)·U_m·sin(2πt/T₀ + φ) ; d²u_C/dt² = −(2π/T₀)²·U_m·cos(2πt/T₀ + φ) = −(2π/T₀)²·u_C", "v_solution (derivee_1, derivee_2)", "Dérive −(2π/T₀)·U_m·sin(2πt/T₀ + φ).", ["C4"], ["d²u_C/dt² = −(2π/T₀)²·U_m·cos(2πt/T₀ + φ) = −(2π/T₀)²·u_C."]),
 D("e8", "Identifier : T₀ = 2π√(LC)", "Pourquoi la période propre vaut-elle 2π√(LC) ?", "on remplace : [1/(LC) − (2π/T₀)²]·u_C = 0 pour tout t → (2π/T₀)² = 1/(LC) → T₀ = 2π√(LC) ; pulsation propre ω₀ = 2π/T₀ = 1/√(LC) (les sujets écrivent toujours 2π/T₀)", "v_solution (identification)", "L = 0,1 H, C = 10 µF. T₀ = ?", ["C4"], ["(2π/T₀)² = 1/(LC), donc T₀ = 2π√(LC).", "LC = 0,1 × 10⁻⁵ = 10⁻⁶ s², √(LC) = 10⁻³ s.", "T₀ = 2π × 10⁻³ ≈ 6,3·10⁻³ s = 6,3 ms."]),
 # bloc 3
 D("p1", "√(LC) est un temps", "Comment montrer que T₀ s'exprime en secondes ?", "u = L·di/dt → [L] = [U]·[T]/[I] ; i = C·du/dt → [C] = [I]·[T]/[U] ; [L]·[C] = [T]² ; 2π n'a pas d'unité", "v_periode (T0 : unites)", "De i = C·du/dt, quelle est la dimension de C ?", ["C4"], ["[C] = [I]·[T]/[U].", "[L]·[C] = ([U]·[T]/[I])·([I]·[T]/[U]) = [T]².", "[√(LC)] = [T] : T₀ est un temps."]),
 D("p2", "T₀ ne dépend pas de la charge de départ", "Que change une tension de charge plus grande ?", "deux courbes : condensateur chargé sous 6 V puis sous 12 V ; U_m double, les sommets restent alignés dans le temps", "v_periode (T0 : E_change)", "On charge sous 12 V au lieu de 6 V. T₀ change-t-elle ?", ["C4", "C5"], ["Non : T₀ = 2π√(LC) ne contient pas E ; seule l'amplitude U_m double."], prediction=True),
 D("p3", "Si C (ou L) est multipliée par 4", "Comment L et C changent-ils la période ?", "deux courbes superposées : C × 4 → T₀ × 2 (racine) ; même chose pour L", "v_periode (influence_C, influence_L)", "On multiplie C par 4. T₀ est-elle multipliée par 4, par 2, ou inchangée ?", ["C5", "C4"], ["T₀′ = 2π√(L·4C) = 2 × 2π√(LC) = 2·T₀ : multipliée par 2."], prediction=True),
 D("p4", "Exercice du national : choisir la courbe, trouver L", "Comment le national fait-il reconnaître la solution ?", "2022 N 2.1 : E = 12 V, C = 50 µF, bobine sans résistance ; trois courbes C₁ (cosinus de 12 V), C₂ (10 V), C₃ (amortie) ; puis T₀ = 10 ms lue → L avec π² = 10", "v_figures (fig=2022N)", "Laquelle des trois courbes représente u_C ? Puis calcule L.", ["C4", "C5"], ["r = 0 : régime périodique, on élimine C₃ (amortie).", "u_C(0) = E = 12 V : on élimine C₂ ; c'est C₁.", "T₀² = 4π²·L·C → L = T₀²/(4π²·C) = (10⁻²)²/(40 × 5·10⁻⁵) = 0,05 H."], prediction=True),
 # Séance 3 — conditions initiales, oscillogrammes, énergie
 D("c1", "U_m et φ dans le cas du cours", "Que valent U_m et φ quand on bascule un condensateur chargé ?", "la courbe démarre en haut, à E, avec une tangente horizontale : u_C(0) = U_m·cos φ = E et i(0) = 0 → U_m = E, φ = 0 ; c'est la forme de tous les nationaux : u_C = U₀·cos(2πt/T₀)", "v_solution (phase : depart)", "La courbe part de son maximum. Que vaut φ ?", ["C4"], ["u_C(0) = U_m·cos φ = U_m, donc cos φ = 1 et φ = 0."], prediction=True),
 D("c2", "Lire U_m sur la courbe", "Où lit-on l'amplitude ?", "deux traits horizontaux sur un sommet et un creux : U_m est la hauteur d'un sommet, pas l'écart sommet–creux", "v_solution (cos : Um)", "Sommet à 4 V, creux à −4 V. U_m = ?", ["C4", "C5"], ["U_m = 4 V (l'écart sommet–creux, 8 V, vaut 2·U_m)."]),
 D("c3", "Une équation, deux angles", "Et si la courbe ne part pas d'un sommet ?", "u_C(0) = 3 V, U_m = 6 V : cos φ = 0,5 → deux angles possibles, +π/3 et −π/3", "v_solution (phase : deux_angles)", "cos φ = 0,5 : quels sont les deux angles ?", ["C4"], ["φ = +π/3 ou φ = −π/3 : la valeur de départ ne suffit pas."]),
 D("c4", "Le sens de départ choisit φ", "Comment choisir entre les deux angles ?", "du_C/dt(0) = −(2π/T₀)·U_m·sin φ : courbe qui MONTE au départ → sin φ < 0 → φ négatif ; qui descend → φ positif ; même méthode pour i en 2020 N (φ = +π/2)", "v_solution (phase : phi_choisi)", "La courbe part de 3 V en montant (U_m = 6 V). φ = +π/3 ou −π/3 ?", ["C4"], ["cos φ = 3/6 = 0,5, donc φ = ±π/3.", "La courbe monte : −(2π/T₀)·U_m·sin φ > 0, donc sin φ < 0.", "φ = −π/3 rad."], prediction=True),
 # bloc 2
 D("l1", "Lire T sur plusieurs périodes", "Comment mesurer la pseudo-période avec précision ?", "on compte plusieurs pseudo-périodes entières entre deux sommets éloignés, on divise ; jamais entre un sommet et le creux suivant (T/2) ; 2025 N : 4 carreaux de 7·10⁻⁵ s", "v_oscillogramme (pseudo : mesure_nT)", "Entre le 1er et le 4e sommet, on lit 12 ms. T = ?", ["C5"], ["Du 1er au 4e sommet il y a 3 pseudo-périodes (pas 4).", "T = 12/3 = 4 ms."], prediction=True),
 D("l2", "La pseudo-période est voisine de T₀", "Peut-on utiliser T₀ = 2π√(LC) quand il y a une résistance ?", "admis : si l'amortissement est faible, T ≈ T₀ ; phrase des sujets : « en assimilant la pseudo-période à la période propre » ; 2021 R : T lue 45 ms, T₀ calculée 44,9 ms", "v_oscillogramme (pseudo : T_voisine_T0)", "2021 R : L = 0,51 H, C = 100 µF. Calcule T₀ et compare à T = 45 ms.", ["C5", "C2"], ["T₀ = 2π√(0,51 × 10⁻⁴) ≈ 4,49·10⁻² s ≈ 44,9 ms.", "T = 45 ms ≈ T₀ : l'amortissement est faible."]),
 D("l3", "Trouver C (ou L) : le carré d'abord", "Comment isoler C dans T₀ = 2π√(LC) ?", "on élève au carré : T₀² = 4π²·L·C → C = T₀²/(4π²·L) ; T₀ en secondes ; « on prend π² = 10 » (au moins 9 sessions) ; 2020 N II.3", "cahier", "2020 N : T = 10 ms, L = 1 H, π² = 10. C = ?", ["C5"], ["T ≈ T₀, donc T₀² = 4π²·L·C.", "C = T₀²/(4π²·L) = (10⁻²)²/(40 × 1) = 2,5·10⁻⁶ F = 2,5 µF."]),
 D("l4", "Exercice du national : l'échelle en flèches", "Comment lire T₀ quand l'axe n'a pas de nombres ?", "2023 N 2.2.1 : LC, L = 1 H, courbe u_C(t) avec deux flèches d'échelle (5 V ; 0,5 ms) ; T₀ = 4 graduations = 2 ms → C", "v_figures (fig=2023N)", "Une période occupe 4 graduations de 0,5 ms ; L = 1 H. C = ?", ["C5"], ["T₀ = 4 × 0,5 = 2 ms = 2·10⁻³ s.", "C = T₀²/(4π²·L) = 4·10⁻⁶/(40 × 1) = 10⁻⁷ F = 0,1 µF."]),
 # bloc 3
 D("en1", "Deux réservoirs d'énergie", "Où est l'énergie dans le circuit ?", "au cahier : E_e = ½·C·u_C² (vue au RC, barre rouge) et E_m = ½·L·i² (vue au RL, barre verte) ; énergie totale E = ½·C·u_C² + ½·L·i² (aussi q²/(2C) + ½·L·i²)", "v_circuit_lc (echange)", "Laquelle des deux énergies dépend de i ?", ["C6"], ["E_m = ½·L·i², l'énergie de la bobine."]),
 D("en2", "Au départ, tout est dans le condensateur", "Combien d'énergie au début ?", "t = 0 : u_C = E, i = 0 : barre rouge pleine, barre verte vide ; E = ½·C·E² (ou Q_m²/(2C))", "v_energie (echange : depart)", "2019 N : C = 10 µF, E = 10 V. Énergie au départ ?", ["C6"], ["i(0) = 0, donc E = ½·C·E² = ½ × 10⁻⁵ × 10² = 5·10⁻⁴ J."]),
 D("en3", "L'énergie passe d'un réservoir à l'autre", "Où est l'énergie quand u_C = 0 ?", "la barre rouge se vide pendant que la verte se remplit ; u_C = 0 → tout dans la bobine ; u_C extrême (i = 0) → tout dans le condensateur (2024 N 1.3) ; E_e est maximale deux fois par période", "v_energie (echange : echange, tout_bobine)", "Quand u_C = 0, où est toute l'énergie ?", ["C6"], ["u_C = 0, donc E_e = 0 : toute l'énergie est dans la bobine, i est maximal."], prediction=True),
 D("en4", "Sans résistance, la somme ne bouge pas", "L'énergie totale change-t-elle dans le LC idéal ?", "courbes E_e(t), E_m(t) et leur somme : droite horizontale ; on s'en sert : E_m = E − ½·C·u_C² (2019 N 4.2)", "v_energie (echange : somme_constante)", "2019 N : E = 5·10⁻⁴ J, C = 10 µF ; à 12 ms, u_C = −8 V. E_m = ?", ["C6"], ["R + r = 0 : l'énergie totale se conserve.", "E_e = ½ × 10⁻⁵ × (−8)² = 3,2·10⁻⁴ J.", "E_m = E − E_e = 5·10⁻⁴ − 3,2·10⁻⁴ = 1,8·10⁻⁴ J."], prediction=True),
 # Séance 4 — amortissement, entretien, deux nationaux
 D("a1", "Avec une résistance, l'énergie diminue", "Pourquoi les sommets baissent-ils ?", "barres et courbe E(t) qui descend ; la résistance chauffe : une partie de l'énergie part en chaleur à chaque oscillation (effet Joule, dans R et dans r)", "v_energie (amortie : pertes)", "Avec R + r ≠ 0, l'énergie totale reste-t-elle constante ? Où part-elle ?", ["C7"], ["Non : elle diminue ; elle est dissipée en chaleur par effet Joule dans R et r."], prediction=True),
 D("a2", "Dériver chaque énergie", "Comment calculer dE/dt ?", "dérivée d'un carré : d(x²)/dt = 2x·dx/dt ; d(½·C·u_C²)/dt = C·u_C·du_C/dt = u_C·i ; d(½·L·i²)/dt = L·i·di/dt", "v_energie (amortie : derivee)", "Dérive ½·L·i² par rapport au temps.", ["C7"], ["d(½·L·i²)/dt = ½·L·2i·di/dt = L·i·di/dt."]),
 D("a3", "dE/dt = −(R + r)·i²", "Pourquoi le signe moins prouve-t-il la perte ?", "dE/dt = i·(u_C + L·di/dt) ; l'équation du circuit donne u_C + L·di/dt = −(R + r)·i ; donc dE/dt = −(R + r)·i² ≤ 0 ; bobine seule (2025 N) : −r·i²", "v_energie (amortie : derivee)", "Quel est le signe de −(R + r)·i² ? Que fait E ?", ["C7"], ["dE/dt = C·u_C·du_C/dt + L·i·di/dt = i·(u_C + L·di/dt).", "u_C + R·i + L·di/dt + r·i = 0, donc u_C + L·di/dt = −(R + r)·i.", "dE/dt = −(R + r)·i² ≤ 0 : E diminue (constante si R + r = 0)."]),
 D("a4", "L'énergie perdue entre deux sommets", "Comment chiffrer la perte ?", "aux sommets de q (ou u_C), i = 0 : E = q²/(2C) ; énergie perdue = E(début) − E(fin) > 0 ; 2016 N : q = 120 µC puis 40 µC, C = 10 µF", "v_energie (amortie : deux_sommets)", "2016 N : C = 10 µF, q = 120 µC à t = 0 puis 40 µC à 18 ms (deux sommets). Énergie perdue ?", ["C7"], ["Aux sommets i = 0 : E = q²/(2C).", "E(0) = (120·10⁻⁶)²/(2 × 10⁻⁵) = 7,2·10⁻⁴ J ; E(18 ms) = (40·10⁻⁶)²/(2 × 10⁻⁵) = 8·10⁻⁵ J.", "Énergie perdue par effet Joule : 7,2·10⁻⁴ − 8·10⁻⁵ = 6,4·10⁻⁴ J (ΔE = −6,4·10⁻⁴ J)."], prediction=True),
 # bloc 2
 D("a5", "Reconnaître les courbes d'énergie", "Laquelle est E_e, laquelle E_m ?", "deux courbes qui se croisent : celle qui part de son maximum est E_e (u_C(0) = E), celle qui part de 0 est E_m (i(0) = 0) ; leur somme E_t descend ; 2021 R : E_t passe de 1,80 mJ à 1,26 mJ", "v_energie (amortie : pertes)", "Des deux courbes, laquelle part de 0 ? Puis : énergie perdue de 1,80 mJ à 1,26 mJ ?", ["C7", "C6"], ["E_m = ½·L·i² part de 0 car i(0) = 0 ; E_e part de ½·C·E².", "Énergie dissipée : 1,80 − 1,26 = 0,54 mJ (2021 R)."], prediction=True),
 D("k1", "Entretenir les oscillations", "Comment empêcher les oscillations de s'éteindre ?", "oscillogramme qui s'écrase ; on ajoute en série un générateur G qui délivre une tension proportionnelle à l'intensité : u_G = k·i (fonctionnement interne admis) ; il rend à chaque instant l'énergie perdue", "v_entretien (amorti, dispositif)", "Si i double, que devient la tension u_G ?", ["C8"], ["u_G = k·i : elle double aussi."]),
 D("k2", "La bonne valeur de k", "Quelle valeur faut-il donner à k ?", "additivité : u_C + u_R + u_b = u_G = k·i → L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0 ; terme du milieu barré si k = R + r : on retrouve l'équation du LC", "v_entretien (equation, compensation)", "R = 90 Ω, r = 10 Ω. Quelle valeur de k rend les oscillations sinusoïdales ?", ["C8", "C3"], ["L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0.", "Oscillations sinusoïdales : le terme en dq/dt doit être nul, donc k = R + r = 100 Ω (la résistance totale)."], prediction=True),
 D("k3", "Oscillations entretenues, à la période T₀", "L'entretien change-t-il le rythme du circuit ?", "poignée k : k < R + r amorti ; k = R + r sinusoïde d'amplitude constante, de période T₀ = 2π√(LC) ; 2018 N : k = 5 → r = 5 Ω, T₀ = 2,5 ms et C = 2,5 µF → L ≈ 63 mH", "v_entretien (entretenu, periode_T0)", "Les oscillations entretenues ont-elles la période T₀ ou une autre ?", ["C8", "C5"], ["k = R + r : l'équation est celle du LC, la période est T₀ = 2π√(LC).", "2018 N : L = T₀²/(4π²·C) = (2,5·10⁻³)²/(40 × 2,5·10⁻⁶) ≈ 6,3·10⁻² H."], prediction=True),
 # bloc 3
 D("n1", "Sujet national 2020 N, en entier", "On refait un vrai sujet : décharge puis entretien.", "2020 N Ex IV II-III : bobine du RL (L = 1 H, r = 10 Ω) + R = 90 Ω, courbe u_C pseudo-périodique (T = 10 ms) ; régime, équation, C ; générateur u_G = k·i, k₀ ; i(t) entretenue : I_m = 8 mA, départ à 0 en descendant ; énergie totale, E_e à 16 ms (i = 4,8 mA)", "v_figures (fig=2020N)", "Trouve C, k₀, puis I_m, T₀ et φ de i = I_m·cos(2πt/T₀ + φ), puis E_t et E_e à 16 ms.", ["C2", "C3", "C5", "C8", "C4", "C6"],
   ["II.1 Les sommets diminuent : régime pseudo-périodique.", "II.2 u_C + u_R + u_b = 0 → LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0.",
    "II.3 T ≈ T₀ : C = T₀²/(4π²·L) = (10⁻²)²/(40 × 1) = 2,5·10⁻⁶ F.", "III.1 k₀ = R + r = 90 + 10 = 100 Ω.",
    "III.2 I_m = 8 mA, T₀ = 10 ms ; i(0) = I_m·cos φ = 0 → φ = ±π/2 ; i descend au départ : −(2π/T₀)·I_m·sin φ < 0 → sin φ > 0 → φ = +π/2 rad.",
    "III.3 Quand i = I_m, u_C = 0 : E_t = ½·L·I_m² = ½ × 1 × (8·10⁻³)² = 3,2·10⁻⁵ J (constante).",
    "III.4 E_e = E_t − ½·L·i² = 3,2·10⁻⁵ − ½ × 1 × (4,8·10⁻³)² ≈ 2,05·10⁻⁵ J."]),
 D("n2", "Sujet national 2025 N, en entier", "Un autre sujet : la bobine seule et l'énergie.", "2025 N Ex 3 partie 2 : C₀ = 1 µF chargé à U₀ = 10 V, bobine (L, r) seule ; courbe u_C(t), flèche d'échelle 7·10⁻⁵ s ; t_A sommet à 7 V, u_C décroît entre t_A et t_B ; démontrer dE_T/dt = −r·i² ; énergie Joule entre 0 et t_A", "v_figures (fig=2025N)", "Équation en u_C, pseudo-période, signe de i entre t_A et t_B, dE_T/dt, énergie dissipée entre 0 et t_A.", ["C3", "C5", "C1", "C7"],
   ["2.1 u_C + u_b = 0 avec u_b = L·di/dt + r·i et i = C₀·du_C/dt → L·C₀·d²u_C/dt² + r·C₀·du_C/dt + u_C = 0.",
    "2.2.1 Une pseudo-période occupe 4 carreaux de 7·10⁻⁵ s : T = 4 × 7·10⁻⁵ = 2,8·10⁻⁴ s.",
    "2.2.2 i = C₀·du_C/dt ; u_C décroît entre t_A et t_B, donc i < 0.",
    "2.3 dE_T/dt = C₀·u_C·du_C/dt + L·i·di/dt = i·(u_C + L·di/dt) = i·(−r·i) = −r·i².",
    "2.4 À t = 0 et à t_A (sommets), i = 0 : |E_th| = ½·C₀·(U₀² − u_C(t_A)²) = ½ × 10⁻⁶ × (100 − 49) = 2,55·10⁻⁵ J."], prediction=True),
 D("bl", "Ce qu'il faut retenir", "La fiche du chapitre.", "fiche : oscillations libres, régimes, équation en q et en u_C, T₀ = 2π√(LC), U_m et φ, lecture de T, énergie, dE/dt, entretien k = R + r", "v_bilan", "Quelle formule donne T₀ ?", ["C4"], ["T₀ = 2π√(LC)."]),
 D("cr", "La carte du circuit RLC", "Tout le chapitre sur une carte.", "carte complète ; acquis de l'élève (concentration.acquis)", "v_carte (complete)", "Quelle partie de la carte te semble la plus difficile ?", ["C1"], []),
]

seances = [
 {"n": 1, "titre": "Un condensateur qui se vide dans une bobine : oscillations et régimes", "blocs": [["o1", "o2", "d1", "d2"], ["d3", "d4", "d5", "d6"], ["r1", "r2", "r3", "r4"]]},
 {"n": 2, "titre": "L'équation différentielle et la période propre", "blocs": [["e1", "e2", "e3", "e4"], ["e5", "e6", "e7", "e8"], ["p1", "p2", "p3", "p4"]]},
 {"n": 3, "titre": "Conditions initiales, oscillogrammes et échange d'énergie", "blocs": [["c1", "c2", "c3", "c4"], ["l1", "l2", "l3", "l4"], ["en1", "en2", "en3", "en4"]]},
 {"n": 4, "titre": "Amortissement, entretien, deux nationaux", "blocs": [["a1", "a2", "a3", "a4"], ["a5", "k1", "k2", "k3"], ["n1", "n2", "bl", "cr"]]},
]


def verifier_calculs():
    """Refait en Python chaque calcul chiffré des rappels et des diapositives ; renvoie la liste des contrôles."""
    P2 = 10  # π² = 10 des énoncés
    ok = []
    def chk(nom, val, attendu, tol=0.01):
        assert abs(val - attendu) <= tol * abs(attendu) + 1e-15, (nom, val, attendu)
        ok.append(nom)
    chk("C1_r3/d5 i", 10e-6 * (-2 / 1e-3), -0.02)
    chk("C3_r3 1/C", 1 / 10e-6, 1e5)
    chk("C4_r1/e8 T0", 2 * pi * sqrt(0.1 * 10e-6), 6.3e-3)
    chk("C4_r2/p3 C×4", 2 * pi * sqrt(0.1 * 40e-6) / (2 * pi * sqrt(0.1 * 10e-6)), 2)
    chk("C5_r1/l1 T", 12e-3 / 3, 4e-3)
    chk("C5_r2 L", (4e-3) ** 2 / (4 * P2 * 4e-6), 0.1)
    chk("C6_r1 E", 0.5 * 10e-6 * 6 ** 2, 1.8e-4)
    chk("C6_r3/en4 Em 2019N", 5e-4 - 0.5 * 10e-6 * 8 ** 2, 1.8e-4)
    chk("2019N uC(12ms)", 10 * cos(2 * pi * 12 / 20), -8.09)
    chk("en2 2019N E", 0.5 * 10e-6 * 10 ** 2, 5e-4)
    chk("C6_r4 2019R", 0.5 * 5e-6 * 4.8 ** 2 + 0.5 * 0.5 * (12e-3) ** 2, 9.36e-5)
    chk("C7_r2 perte", 0.5 * 10e-6 * (36 - 16), 1e-4)
    chk("C8_r1 k", 10 + 8, 18)
    chk("p4 2022N L", (10e-3) ** 2 / (4 * P2 * 50e-6), 0.05)
    chk("c3/c4 phi", acos(0.5), pi / 3)
    chk("l2 2021R T0", 2 * pi * sqrt(0.51 * 100e-6), 44.9e-3)
    chk("l3/n1 2020N C", (10e-3) ** 2 / (4 * P2 * 1), 2.5e-6)
    chk("l4 2023N C", (4 * 0.5e-3) ** 2 / (4 * P2 * 1), 1e-7)
    chk("a4 2016N E0", (120e-6) ** 2 / (2 * 10e-6), 7.2e-4)
    chk("a4 2016N E18", (40e-6) ** 2 / (2 * 10e-6), 8e-5)
    chk("a4 2016N perte", ((120e-6) ** 2 - (40e-6) ** 2) / (2 * 10e-6), 6.4e-4)
    chk("a5 2021R E0", (0.6e-3) ** 2 / (2 * 100e-6), 1.8e-3)
    chk("a5 2021R perte", 1.80e-3 - 1.26e-3, 0.54e-3)
    chk("k2/n1 k0", 90 + 10, 100)
    chk("k3 2018N L", (2.5e-3) ** 2 / (4 * pi ** 2 * 2.5e-6), 6.3e-2)
    chk("n1 Et", 0.5 * 1 * (8e-3) ** 2, 3.2e-5)
    chk("n1 Ee", 0.5 * 1 * (8e-3) ** 2 - 0.5 * 1 * (4.8e-3) ** 2, 2.05e-5)
    chk("n1 i(16ms) vrai", 8e-3 * cos(2 * pi * 16 / 10 + pi / 2), 4.70e-3)
    chk("n2 T", 4 * 7e-5, 2.8e-4)
    chk("n2 Eth", 0.5 * 1e-6 * (10 ** 2 - 7 ** 2), 2.55e-5)
    chk("C1_r4/d6 ub", -5 - 0, -5)
    return ok


if __name__ == "__main__":
    print(len(verifier_calculs()), "calculs vérifiés")
