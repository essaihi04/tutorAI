# -*- coding: utf-8 -*-
"""Partie A de l'exploration circuit_RLC : ce qui ne dépend pas de la lecture des nationaux
(notions complexes, analogies, à ne pas dire, hors programme, visuels, cours existant).
Capacités citées RLC1 à RLC7 : provisoires (pas encore de fiche circuit_RLC dans cadre_reference_2bac_pc.json) :
RLC1 décharge d'un condensateur dans une bobine, oscillations libres ; RLC2 équation différentielle (RLC et LC) ;
RLC3 solution du LC, T₀ = 2π√(LC), ω₀, homogénéité, U_m et φ ; RLC4 régimes d'amortissement, pseudo-période ;
RLC5 énergie totale, échange, conservation (R = 0), dE/dt = −(R + r)·i² ; RLC6 entretien (u = R₀·i) ;
RLC7 exploitation d'oscillogrammes (T, T₀, U_m, L ou C)."""

notions_complexes = [
 {"id": "decharge_oscillante", "notion": "un condensateur chargé qui se décharge dans une bobine ne se vide pas simplement : u_C change de signe et le courant va et vient (oscillations libres)",
  "pourquoi_difficile": "au RC l'élève a vu une décharge qui descend vers 0 et s'arrête ; ici la courbe passe SOUS zéro : il ne voit pas qui « recharge » le condensateur à l'envers ; il croit que c'est la résistance qui fait osciller",
  "prerequis": ["courant_charge_q_it", "lois_kirchhoff"],
  "marches": [
   {"n": 1, "idee": "rappel : condensateur chargé + résistance seule (RC)", "vu": "K bascule sur R : u_C descend de E vers 0 sans jamais passer en dessous (courbe bleue du RC)", "phrase": "avec une résistance seule, la décharge s'arrête à 0", "question": "au RC, u_C peut-elle devenir négative pendant la décharge ?"},
   {"n": 2, "idee": "on remplace la résistance par une bobine", "vu": "même montage, K bascule sur la bobine : u_C descend, passe par 0, devient négative, remonte… comme une vague", "phrase": "u_C oscille autour de 0 : ce sont des oscillations électriques", "question": "que fait u_C juste après être passée par 0 ?"},
   {"n": 3, "idee": "le condensateur vide, la bobine garde le courant", "vu": "arrêt sur image à u_C = 0 : le courant est maximal, les électrons continuent dans le même sens et chargent l'armature d'en face", "phrase": "la bobine s'oppose à la disparition du courant (RL) : elle recharge le condensateur à l'envers", "question": "au moment où u_C = 0, le courant est-il nul ou maximal ?"},
   {"n": 4, "idee": "le mouvement recommence dans l'autre sens", "vu": "les électrons repartent dans l'autre sens ; le cycle se répète ; personne n'ajoute d'énergie", "phrase": "le circuit oscille tout seul : oscillations libres", "question": "qui fournit l'énergie pendant les oscillations ?"},
   {"n": 5, "idee": "le mot : circuit RLC série, oscillations libres", "vu": "écrit au cahier : condensateur chargé + bobine (L, r) + résistance R en série, sans générateur", "phrase": "« libres » : aucun générateur dans le circuit pendant les oscillations", "question": "pourquoi dit-on « libres » ?"}],
  "image_mentale": "une balançoire qu'on lâche d'en haut : elle descend, dépasse le point le plus bas grâce à son élan, remonte de l'autre côté ; l'élan, c'est la bobine",
  "exemple_chiffre": "C = 10 µF chargé sous E = 6 V, bobine L = 0,1 H : u_C passe de +6 V à −6 V puis revient à +6 V en T₀ ≈ 6,3 ms",
  "piege": "croire que R crée les oscillations (c'est L et C qui échangent ; R ne fait que les amortir)",
  "verification": "si on enlève la bobine et qu'on garde R, le circuit oscille-t-il ? (non : décharge du RC)"},
 {"id": "equation_differentielle", "notion": "établir L·d²q/dt² + (R + r)·dq/dt + q/C = 0, ou LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0",
  "pourquoi_difficile": "première équation du SECOND ordre : il faut dériver deux fois ; i = dq/dt = C·du_C/dt puis di/dt = d²q/dt² ; l'élève oublie r, ou met E au second membre alors que le générateur est sorti",
  "prerequis": ["lois_kirchhoff", "derivee_usuelle", "courant_charge_q_it"],
  "marches": [
   {"n": 1, "idee": "additivité sur le circuit sans générateur", "vu": "flèches u_C, u_R, u_b sur le circuit fermé, sens de i choisi", "phrase": "u_C + u_R + u_b = 0", "question": "après la bascule, y a-t-il un générateur dans le circuit ?"},
   {"n": 2, "idee": "remplacer chaque tension", "vu": "u_R = R·i ; u_b = L·di/dt + r·i ; u_C = q/C apparaissent sous chaque flèche", "phrase": "q/C + R·i + L·di/dt + r·i = 0", "question": "quelle grandeur relie q et i ?"},
   {"n": 3, "idee": "tout écrire avec q", "vu": "i = dq/dt, donc di/dt = d²q/dt² (deux flèches « on dérive »)", "phrase": "L·d²q/dt² + (R + r)·dq/dt + q/C = 0", "question": "que vaut di/dt en fonction de q ?"},
   {"n": 4, "idee": "la même équation en u_C", "vu": "q = C·u_C remplace q ; tout est multiplié par… rien de nouveau, on range", "phrase": "LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0", "question": "par quoi remplace-t-on q pour avoir l'équation en u_C ?"},
   {"n": 5, "idee": "le cas idéal R + r = 0", "vu": "le terme du milieu est barré à la craie", "phrase": "d²u_C/dt² + u_C/(LC) = 0 : circuit LC idéal", "question": "quel terme disparaît quand la résistance totale est nulle ?"}],
  "image_mentale": "la même recette qu'au RC et au RL (additivité, remplacer, ranger) ; nouveauté : on dérive deux fois",
  "exemple_chiffre": "L = 0,1 H, C = 10 µF, R + r = 20 Ω → 0,1·d²q/dt² + 20·dq/dt + 10⁵·q = 0 ; en u_C : 10⁻⁶·d²u_C/dt² + 2·10⁻⁴·du_C/dt + u_C = 0",
  "piege": "oublier r ; écrire E au second membre ; écrire i = C·u_C au lieu de i = C·du_C/dt",
  "verification": "R = 0 et r = 0 : écrire l'équation en q (d²q/dt² + q/(LC) = 0)"},
 {"id": "solution_T0", "notion": "vérifier que u_C = U_m·cos(2πt/T₀ + φ) est solution du LC et en déduire T₀ = 2π√(LC) (et ω₀ = 1/√(LC)), homogène à un temps",
  "pourquoi_difficile": "dériver deux fois un cosinus composé ; voir que la dérivée seconde « redonne » −(2π/T₀)²·u_C ; puis identifier (2π/T₀)² = 1/(LC) ; enfin l'analyse dimensionnelle avec H et F",
  "prerequis": ["derivee_sinus_cosinus", "periode_frequence"],
  "marches": [
   {"n": 1, "idee": "la courbe se répète : une sinusoïde", "vu": "u_C(t) du LC idéal : même hauteur U_m à chaque bosse, même durée T₀ entre deux bosses", "phrase": "on propose u_C = U_m·cos(2πt/T₀ + φ)", "question": "sur la courbe, où lit-on U_m ? et T₀ ?"},
   {"n": 2, "idee": "dériver une fois, puis deux fois", "vu": "du_C/dt = −(2π/T₀)·U_m·sin(…) ; d²u_C/dt² = −(2π/T₀)²·U_m·cos(…)", "phrase": "la dérivée seconde, c'est −(2π/T₀)² fois u_C", "question": "que donne la dérivée de −sin ?"},
   {"n": 3, "idee": "remplacer et identifier", "vu": "−(2π/T₀)²·u_C + u_C/(LC) = 0 pour tout t → (2π/T₀)² = 1/(LC)", "phrase": "T₀ = 2π√(LC) : période propre ; ω₀ = 2π/T₀ = 1/√(LC) : pulsation propre", "question": "L = 0,1 H, C = 10 µF : T₀ = ?"},
   {"n": 4, "idee": "homogénéité : √(LC) est un temps", "vu": "u = L·di/dt → [L] = V·s/A ; i = C·du/dt → [C] = A·s/V ; produit : s²", "phrase": "√(LC) s'exprime en secondes", "question": "quelles relations du cours donnent l'unité de L et celle de C ?"}],
  "image_mentale": "la balançoire : sa durée d'aller-retour ne dépend pas de la force avec laquelle on l'a lâchée ; T₀ dépend seulement de L et C, pas de E",
  "exemple_chiffre": "L = 0,1 H, C = 10 µF → LC = 10⁻⁶ s², √(LC) = 10⁻³ s, T₀ = 2π × 10⁻³ ≈ 6,28·10⁻³ s ; ω₀ = 10³ rad·s⁻¹",
  "piege": "T₀ = 2π√(L/C) ou 2π·LC ; oublier de convertir µF et mH ; croire que T₀ dépend de E",
  "verification": "si on multiplie C par 4, T₀ est multipliée par ? (2)"},
 {"id": "conditions_initiales", "notion": "déterminer U_m et φ avec u_C(0) et le sens de variation de u_C à t = 0 (ou i(0))",
  "pourquoi_difficile": "une seule équation cos φ = u_C(0)/U_m donne deux angles ; il faut le signe de la dérivée (ou de i) pour choisir ; l'élève prend toujours φ = 0",
  "prerequis": ["derivee_sinus_cosinus", "angles_remarquables_formules"],
  "marches": [
   {"n": 1, "idee": "le cas du cours : condensateur chargé, K bascule à t = 0", "vu": "la courbe démarre en haut, à E, avec une tangente horizontale (i(0) = 0)", "phrase": "u_C(0) = U_m·cos φ = E et i(0) = 0 → U_m = E, φ = 0", "question": "à t = 0, que vaut cos(φ) si la courbe part de son maximum ?"},
   {"n": 2, "idee": "lire U_m sur la courbe", "vu": "deux traits horizontaux sur le premier sommet et le premier creux", "phrase": "U_m est la hauteur d'un sommet, pas l'écart sommet–creux", "question": "sommet à 4 V, creux à −4 V : U_m = ?"},
   {"n": 3, "idee": "courbe qui part d'une autre valeur", "vu": "u_C(0) = 3 V, U_m = 6 V : cos φ = 0,5 → deux angles possibles, +π/3 et −π/3", "phrase": "une seule équation ne suffit pas à choisir φ", "question": "cos φ = 0,5 : quels sont les deux angles ?"},
   {"n": 4, "idee": "le sens de départ choisit", "vu": "la courbe MONTE à t = 0 : du_C/dt(0) = −(2π/T₀)·U_m·sin φ > 0 → sin φ < 0 → φ = −π/3", "phrase": "u_C monte au départ → φ négatif ; u_C descend → φ positif", "question": "la courbe part de 0 en montant : φ = ?"}],
  "image_mentale": "une montre qu'on regarde au départ : la position seule ne suffit pas, il faut savoir dans quel sens l'aiguille repart",
  "exemple_chiffre": "U_m = 6 V, u_C(0) = 0 et u_C croissante → cos φ = 0, sin φ < 0 → φ = −π/2 rad ; u_C = 6·cos(2πt/T₀ − π/2)",
  "piege": "φ = 0 par habitude ; prendre U_m = écart sommet–creux ; φ en degrés dans un cos dont l'argument est en radians",
  "verification": "u_C(0) = −U_m : φ = ? (π)"},
 {"id": "regimes", "notion": "rôle de la résistance totale : régime pseudo-périodique (amplitude qui diminue, T ≈ T₀), apériodique (retour sans oscillation), critique (frontière)",
  "pourquoi_difficile": "trois noms proches à reconnaître sur un oscillogramme ; la pseudo-période n'est pas une vraie période (la courbe ne se répète pas exactement) ; la frontière critique n'a pas de formule au programme",
  "prerequis": ["periode_frequence", "energie_electrique_joule"],
  "marches": [
   {"n": 1, "idee": "R petite : oscillations qui s'amortissent", "vu": "u_C oscille, chaque sommet plus bas que le précédent, durée entre deux sommets presque égale à T₀", "phrase": "régime pseudo-périodique ; T, la pseudo-période, est voisine de T₀", "question": "les sommets gardent-ils la même hauteur ?"},
   {"n": 2, "idee": "lire T sur l'axe du temps", "vu": "on compte plusieurs pseudo-périodes entières entre deux sommets éloignés, on divise", "phrase": "mesurer n·T puis diviser par n est plus précis", "question": "3 pseudo-périodes occupent 12 ms : T = ?"},
   {"n": 3, "idee": "R grande : plus d'oscillation", "vu": "u_C revient vers 0 sans passer en dessous, lentement", "phrase": "régime apériodique", "question": "la courbe change-t-elle de signe ?"},
   {"n": 4, "idee": "la frontière", "vu": "on augmente R pas à pas : il existe une valeur où le retour à 0 est le plus rapide sans oscillation", "phrase": "régime critique : la frontière entre les deux (on ne calcule pas cette valeur)", "question": "si R dépasse cette valeur, quel régime obtient-on ?"},
   {"n": 5, "idee": "R = 0 : régime périodique (cas idéal)", "vu": "les trois courbes côte à côte, puis la sinusoïde du LC", "phrase": "plus la résistance totale est grande, plus l'amortissement est fort", "question": "quelle grandeur décide du régime ?"}],
  "image_mentale": "la balançoire dans l'air (pseudo-périodique), dans l'eau de la mer (amortie très vite), dans du miel (elle revient sans dépasser : apériodique)",
  "exemple_chiffre": "C = 4 µF, pseudo-période lue T = 4 ms ≈ T₀ → L = T₀²/(4π²·C) = (16·10⁻⁶)/(40 × 4·10⁻⁶) = 0,1 H (avec π² = 10)",
  "piege": "appeler « périodique » un régime amorti ; lire T entre un sommet et un creux (c'est T/2) ; croire que T dépend beaucoup de R",
  "verification": "sur un oscillogramme où u_C revient à 0 sans changer de signe : nommer le régime (apériodique ou critique)"},
 {"id": "energie_echange", "notion": "énergie totale E = ½·C·u_C² + ½·L·i² : échange entre condensateur et bobine, constante si R = 0",
  "pourquoi_difficile": "deux énergies qui varient en même temps et se compensent ; E_e est maximale quand i = 0 et inversement ; les courbes E_e(t) et E_m(t) oscillent à T₀/2, pas à T₀",
  "prerequis": ["energie_electrique_joule", "energie_potentielle_mecanique"],
  "marches": [
   {"n": 1, "idee": "deux réservoirs d'énergie", "vu": "au cahier : E_e = ½·C·u_C² (RC) et E_m = ½·L·i² (RL) ; deux barres, rouge et verte", "phrase": "le condensateur et la bobine ont chacun leur énergie", "question": "quelle énergie dépend de u_C ? laquelle de i ?"},
   {"n": 2, "idee": "à t = 0 tout est dans le condensateur", "vu": "barre rouge pleine (u_C = E), barre verte vide (i = 0)", "phrase": "E = ½·C·E² au départ", "question": "C = 10 µF, E = 6 V : énergie au départ ?"},
   {"n": 3, "idee": "l'énergie passe d'une barre à l'autre", "vu": "la rouge se vide pendant que la verte se remplit ; à u_C = 0, tout est dans la bobine", "phrase": "échange d'énergie entre le condensateur et la bobine", "question": "quand u_C = 0, où est toute l'énergie ?"},
   {"n": 4, "idee": "la somme ne bouge pas (R = 0)", "vu": "courbes E_e(t), E_m(t) et leur somme : droite horizontale ; E_e repasse au maximum deux fois par T₀", "phrase": "dans le LC idéal, l'énergie totale se conserve", "question": "combien de fois E_e est-elle maximale pendant une période T₀ ?"}],
  "image_mentale": "deux réservoirs d'eau reliés par un tuyau : l'eau passe de l'un à l'autre et revient, la quantité totale reste la même",
  "exemple_chiffre": "C = 10 µF, E = 6 V, L = 0,1 H → E = 1,8·10⁻⁴ J ; quand u_C = 3 V : E_e = 4,5·10⁻⁵ J, E_m = 1,35·10⁻⁴ J ; I_m = √(2E/L) = 0,06 A",
  "piege": "additionner les tensions au lieu des énergies ; écrire ½·C·u_C sans carré ; croire que E_e et E_m ont la période T₀",
  "verification": "quand i = I_m, que vaut u_C ? (0)"},
 {"id": "energie_dissipation", "notion": "avec R + r ≠ 0, l'énergie totale diminue par effet Joule : dE/dt = −(R + r)·i²",
  "pourquoi_difficile": "démonstration attendue : dériver ½·C·u_C² et ½·L·i² (dérivée d'un carré), puis reconnaître l'équation différentielle dans le résultat ; l'élève ne voit pas pourquoi le signe moins prouve la diminution",
  "prerequis": ["derivee_usuelle", "energie_electrique_joule"],
  "marches": [
   {"n": 1, "idee": "on voit la perte", "vu": "barres et courbe E(t) en escalier descendant ; la résistance s'échauffe (lueur rouge)", "phrase": "une partie de l'énergie part en chaleur à chaque oscillation", "question": "où va l'énergie perdue ?"},
   {"n": 2, "idee": "dériver chaque énergie", "vu": "d(½·C·u_C²)/dt = C·u_C·du_C/dt = u_C·i ; d(½·L·i²)/dt = L·i·di/dt", "phrase": "la dérivée de x² est 2x·dx/dt", "question": "pourquoi le ½ disparaît-il ?"},
   {"n": 3, "idee": "mettre i en facteur et utiliser l'équation", "vu": "dE/dt = i·(u_C + L·di/dt) ; or u_C + L·di/dt = −(R + r)·i (équation du circuit)", "phrase": "dE/dt = −(R + r)·i²", "question": "quel est le signe de i² ? et donc de dE/dt ?"},
   {"n": 4, "idee": "chiffrer la perte entre deux sommets", "vu": "aux sommets i = 0 : E = ½·C·u_C² ; on compare deux sommets successifs", "phrase": "énergie perdue = ½·C·(U₁² − U₂²)", "question": "u_C passe de 6 V à 4 V, C = 10 µF : énergie perdue ?"}],
  "image_mentale": "les deux réservoirs d'eau avec un tuyau qui fuit : l'eau va et vient, mais il en reste un peu moins à chaque passage",
  "exemple_chiffre": "C = 10 µF, sommets successifs 6 V puis 4 V → ΔE = ½ × 10⁻⁵ × (36 − 16) = 10⁻⁴ J dissipés par effet Joule",
  "piege": "oublier r dans (R + r) ; écrire dE/dt = −R·i ; calculer l'énergie à un sommet avec ½·L·i² (i = 0 au sommet de u_C)",
  "verification": "R + r = 0 : que vaut dE/dt ? (0, l'énergie se conserve)"},
 {"id": "entretien", "notion": "entretenir les oscillations : un dispositif (générateur à « résistance négative ») fournit u = R₀·i qui compense l'effet Joule quand R₀ = R + r ; le circuit oscille alors à T₀",
  "pourquoi_difficile": "un « générateur » qui ne donne pas une tension fixe mais une tension proportionnelle à i ; le terme en dq/dt disparaît de l'équation ; l'élève croit que l'entretien change la période ou force le circuit",
  "prerequis": ["lois_kirchhoff", "energie_electrique_joule"],
  "marches": [
   {"n": 1, "idee": "le problème : les oscillations s'éteignent", "vu": "oscillogramme pseudo-périodique qui s'écrase", "phrase": "il faut rendre à chaque instant l'énergie perdue", "question": "quelle énergie faut-il compenser ?"},
   {"n": 2, "idee": "le dispositif ajouté en série", "vu": "boîte G (amplificateur opérationnel, admis) dans le circuit, flèche u_G = R₀·i", "phrase": "il fournit une tension proportionnelle au courant", "question": "si i double, que devient la tension fournie ?"},
   {"n": 3, "idee": "nouvelle équation", "vu": "L·d²q/dt² + (R + r − R₀)·dq/dt + q/C = 0 ; le terme du milieu barré si R₀ = R + r", "phrase": "on retrouve l'équation du LC idéal", "question": "quelle valeur faut-il donner à R₀ ?"},
   {"n": 4, "idee": "le résultat", "vu": "R₀ curseur : R₀ < R + r → amorti ; R₀ = R + r → sinusoïde d'amplitude constante, période T₀", "phrase": "oscillations entretenues, à la période propre T₀", "question": "les oscillations entretenues ont-elles la période T₀ ou une autre ?"}],
  "image_mentale": "pousser la balançoire juste ce qu'il faut à chaque passage pour qu'elle garde la même hauteur ; on ne change pas son rythme",
  "exemple_chiffre": "R = 10 Ω, r = 8 Ω → R₀ = 18 Ω ; L = 0,1 H, C = 10 µF → oscillations entretenues de période T₀ ≈ 6,3 ms",
  "piege": "R₀ = R (oubli de r) ; croire que le dispositif impose sa propre période ; parler d'oscillations forcées",
  "verification": "R₀ = 15 Ω avec R + r = 18 Ω : que voit-on ? (oscillations encore amorties)"},
]

analogies_validees = [
 {"notion": "oscillations libres (dépasser la position d'équilibre)", "image": "une balançoire ou un pendule qu'on lâche : il descend, dépasse le point le plus bas grâce à son élan, remonte de l'autre côté",
  "limite_de_l_image": "rien ne bouge dans le circuit comme la balançoire ; ce sont q et i qui varient ; l'« élan » est le rôle de la bobine (elle s'oppose à la variation de i)", "source": "image proposée par Moalim (vidéos non auditées)"},
 {"notion": "pourquoi le courant continue quand le condensateur est vide", "image": "la charrette lancée du RL (karossa) : elle ne s'arrête pas d'un coup, elle dépasse",
  "limite_de_l_image": "même limite qu'au RL : pas de masse dans la bobine", "source": "Moalim, reprise de l'exploration dipole_RL"},
 {"notion": "échange et conservation de l'énergie", "image": "deux réservoirs d'eau reliés par un tuyau : l'eau va de l'un à l'autre et revient, la quantité totale reste la même",
  "limite_de_l_image": "dans un vrai tuyau l'eau s'arrête vite (frottements) : c'est justement l'image de R ; un réservoir = condensateur, l'eau qui coule = la bobine", "source": "Moalim"},
 {"notion": "amortissement et régimes", "image": "la balançoire dans l'air (pseudo-périodique), dans l'eau (amortie vite), dans du miel (revient sans dépasser : apériodique)",
  "limite_de_l_image": "dans le circuit, le « frottement » est la résistance totale R + r, et l'énergie perdue est de la chaleur (effet Joule)", "source": "Moalim"},
 {"notion": "entretien des oscillations", "image": "pousser la balançoire juste ce qu'il faut à chaque passage : elle garde la même hauteur et son propre rythme",
  "limite_de_l_image": "le dispositif ne pousse pas « à chaque passage » : il fournit à chaque instant u = R₀·i", "source": "Moalim"},
 {"notion": "ressemblance avec le ressort", "image": "un ressort (T = k·x, vu au tronc commun) qu'on étire puis qu'on lâche : il va et vient",
  "limite_de_l_image": "rapprochement qualitatif seulement : pas de tableau d'analogie électrique–mécanique (perimetre.json) ; le solide-ressort sera étudié au semestre 2", "source": "perimetre.json circuit_RLC (dire_plutot)"},
 {"notion": "même méthode que le RC et le RL", "image": "la même recette (additivité, remplacer, ranger) ; nouvel ingrédient : on dérive deux fois",
  "limite_de_l_image": "la solution n'est plus une exponentielle mais un cosinus", "source": "Moalim, d'après renvois des explorations dipole_RC et dipole_RL"},
]

a_ne_pas_dire = [
 {"terme": "facteur de qualité, bande passante", "motif": "facteur de qualit[ée]|coefficient de surtension|bande passante|acuit[ée]", "dire_plutot": "« plus l'amplitude diminue vite, plus l'amortissement est fort »"},
 {"terme": "résonance, oscillations forcées, régime forcé", "motif": "r[ée]sonance|oscillations? forc[ée]es?|r[ée]gime (sinuso[iï]dal )?forc[ée]", "dire_plutot": "« oscillations libres » ; avec le dispositif d'entretien : « oscillations entretenues »"},
 {"terme": "impédance, réactance", "motif": "imp[ée]dance|r[ée]actance", "dire_plutot": "« la résistance totale R + r »"},
 {"terme": "équation caractéristique, discriminant, pulsation complexe", "motif": "[ée]quation caract[ée]ristique|discriminant|racines complexes|pulsation complexe", "dire_plutot": "« on vérifie que la solution proposée satisfait l'équation différentielle »"},
 {"terme": "décrément logarithmique, coefficient d'amortissement, enveloppe exponentielle", "motif": "d[ée]cr[ée]ment|coefficient d'amortissement|enveloppe exponentielle|α ?= ?r ?/ ?\\(?2 ?l", "dire_plutot": "« l'amplitude diminue d'une oscillation à l'autre »"},
 {"terme": "résistance critique R_c = 2√(L/C)", "motif": "r[ée]sistance critique|r_?c ?= ?2 ?√|2 ?√ ?\\(? ?l ?/ ?c", "dire_plutot": "« au-delà d'une certaine valeur de la résistance, le régime devient apériodique »"},
 {"terme": "oscillateur harmonique", "motif": "oscillateur harmonique|oscillations harmoniques", "dire_plutot": "« oscillations libres non amorties » (circuit LC idéal)"},
 {"terme": "la résistance crée les oscillations", "motif": "r[ée]sistance (cr[ée]e|produit|provoque) (les )?oscillations", "dire_plutot": "« le condensateur et la bobine échangent l'énergie ; la résistance amortit les oscillations »"},
 {"terme": "l'énergie se conserve (avec R)", "motif": "(avec|malgr[ée]) (la |une )?r[ée]sistance,? l'[ée]nergie (totale )?(se conserve|reste constante)|rlc,? l'[ée]nergie (totale )?(se conserve|reste constante)", "dire_plutot": "« l'énergie totale se conserve seulement si R + r = 0 ; sinon elle diminue par effet Joule »"},
 {"terme": "T₀ = 2π√(L/C)", "motif": "2 ?π ?√ ?\\(? ?l ?/ ?c", "dire_plutot": "« T₀ = 2π√(LC) »"},
 {"terme": "la pseudo-période est la période propre", "motif": "pseudo[- ]p[ée]riode (est |c'est )?(la |[ée]gale [àa] la )?p[ée]riode propre", "dire_plutot": "« la pseudo-période T est voisine de la période propre T₀ quand l'amortissement est faible »"},
 {"terme": "analogie électromécanique (tableau d'équivalences)", "motif": "analogie [ée]lectrom[ée]canique|analogie force[- ]tension", "dire_plutot": "« le circuit LC ressemble à un ressort qu'on lâche » (qualitatif)"},
]

exclus_hors_programme = [
 {"element": "facteur de qualité, bande passante, acuité", "raison": "perimetre.json circuit_RLC.termes_hors_programme"},
 {"element": "régime sinusoïdal forcé, résonance d'intensité, filtre passe-bande", "raison": "perimetre.json ; la résonance n'est vue qu'en mécanique, qualitativement"},
 {"element": "équation caractéristique, racines, solution générale du second ordre amorti (exponentielle × cosinus)", "raison": "perimetre.json : on vérifie seulement la solution sinusoïdale du LC"},
 {"element": "décrément logarithmique, coefficient α = R/(2L), expression de la pseudo-période", "raison": "perimetre.json ; T ≈ T₀ est admis"},
 {"element": "résistance critique R_c = 2√(L/C)", "raison": "perimetre.json : la frontière critique est décrite, jamais calculée"},
 {"element": "tableau d'analogie électromécanique", "raison": "perimetre.json : rapprochement qualitatif autorisé seulement"},
 {"element": "fonctionnement interne du montage à résistance négative (amplificateur opérationnel)", "raison": "perimetre.json demonstrations.admises : u = R₀·i est admis"},
 {"element": "impédance, réactance, déphasage, circuit LC parallèle (bouchon)", "raison": "hors cadre (régime sinusoïdal) ; même décision qu'au RL"},
]

cours_existant = {
 "fichier": "aucun cours RLC dans backend/data/courses ; database/seed_data/lessons/phys_ch8_l1.json (« Laboratoire guidé — Oscillations libres d'un circuit RLC série » : quatre objectifs, parcours observer → prédire → manipuler → mesurer → expliquer, trois cartes : ω₀ = 1/√LC, α = R/(2L), Rcrit = 2√(L/C) ; deux idées fausses ; ticket de sortie ; pas de diapositives) ; database/seed_data/physics_chapters.json chapitre 8 (titre et description seulement)",
 "constat": "pas de deck à comparer ; le seed est un plan de TP autour d'une simulation ancienne ; deux de ses trois cartes sont hors programme ; rien sur l'équation différentielle rédigée, la solution, φ, l'énergie calculée ni l'entretien",
 "a_garder": ["la question guide : comment R décide-t-elle si le circuit oscille ou non ? → regimes", "idée fausse « R crée les oscillations » → decharge_oscillante, a_ne_pas_dire", "idée fausse « l'énergie totale reste constante avec R » → energie_dissipation", "ticket de sortie : rôle de R ; quels réservoirs échangent l'énergie ? → rappels", "faire prédire avant de mesurer (régime obtenu si R augmente)"],
 "images": [
  {"chemin": "frontend/public/media/images/physics/advanced_labs/circuits_lab.webp", "ce_que_ca_montre": "paillasse avec deux oscilloscopes affichant des sinusoïdes, plaque d'essai et carte avec résistances, condensateurs et une bobine, sondes (image générée, utilisée par le seed)", "avis": "réaliste mais montre des signaux de GBF (régime forcé), pas une décharge ; aucun signal amorti", "decision": "garder seulement comme image d'ambiance ou de couverture ; jamais comme oscillogramme du cours", "etape": "ouverture au plus"},
  {"chemin": "frontend/public/media/images/physics/advanced_labs/oscillations_lab.webp", "ce_que_ca_montre": "paillasse de mécanique : solide entre deux ressorts sur rail, pendule simple, pendule de torsion, capteurs (image générée, utilisée par phys_ch14)", "avis": "exacte comme photo d'ambiance ; utile pour l'analogie balançoire/ressort, mais c'est le matériel du chapitre oscillateur mécanique", "decision": "à valider : image fixe possible pour l'analogie (une diapositive), sinon la laisser au chapitre oscillateur_mecanique", "etape": "analogie de decharge_oscillante"},
 ],
 "a_corriger": ["α = R/(2L) et Rcrit = 2√(L/C) (cartes 2 et 3) : hors programme, retirés", "« régime périodique avec R presque nulle » : le régime périodique est le cas idéal R + r = 0 ou entretenu ; avec une petite R il est pseudo-périodique", "la simulation ancienne dit « ω₀ fixe la pseudo-période T₀ » : T₀ est la période propre, la pseudo-période T en est voisine", "« ω₀ = 1/√LC » : écrire 1/√(LC) et donner d'abord T₀ = 2π√(LC), comme les énoncés", "la simulation ancienne calcule quality_factor : hors programme"],
 "a_ajouter": ["décharge dans la bobine montrée pas à pas (pourquoi u_C change de signe)", "équation différentielle en q et en u_C, avec r", "vérification de la solution, T₀, ω₀, homogénéité", "U_m et φ par les conditions initiales", "énergie totale, échange, dE/dt = −(R + r)·i², perte entre deux sommets", "entretien u = R₀·i", "lecture d'oscillogrammes (T, U_m, L ou C), cas types des nationaux"],
 "a_retirer": ["cartes α et Rcrit", "lien vers la simulation advanced/electricity?variant=rlc"],
 "simulations_a_recreer": [{"ancienne": "frontend/public/media/simulations/physics/advanced/electricity/index.html?variant=rlc (CircuitLab, mode RLC)", "montrait": "curseurs R, L, C ; régime affiché (périodique / pseudo-périodique / apériodique) ; ω₀, R critique, facteur de qualité, énergie initiale", "bonne_idee": "faire trouver soi-même les trois régimes en changeant R", "devient": "v_oscillogramme (vues periodique|pseudo|aperiodique|critique, poignée R, sans R critique ni facteur de qualité) et v_periode (influence de L et C sur T₀)"}],
 "autres_traces": ["frontend/public/media/simulations/physics/dipole-rl-tableau/carte.html : branche « suite » « vers le circuit RLC » (lien de fin du RL, à garder cohérent)", "aucune manip RLC/LC dans labo-3d (seulement rc), aucune dans physics/tp (seulement rc), rien dans progressive"],
}

visuels = {
 "_note": "Simulations à la craie à créer dans frontend/public/media/simulations/physics/circuit-rlc-tableau/ (kit shared/tableau, skill simulations-au-tableau, comme dipole-rc-tableau et dipole-rl-tableau) ; moments nommés pilotés par la voix (play_until), highlight, ce_qui_se_voit ; vues choisies par ?vue=. Code couleur proposé (à valider) : rouge = condensateur (u_C, q, E_e, comme la charge au RC), vert = bobine (i, E_m, comme l'établissement au RL), blanc = énergie totale, jaune réservé au surlignage. Valeurs rondes : L = 0,1 H, C = 10 µF (T₀ ≈ 6,3 ms) ou C = 4 µF et π² = 10 (T₀ = 4 ms).",
 "simulations": [
  {"id": "v_carte", "fichier": "carte.html", "ce_que_ca_montre": "carte du chapitre puis carte finale (décharge dans la bobine → équation → LC : solution, T₀ → conditions initiales → régimes → énergie → entretien → oscillogrammes) ; branche d'entrée « depuis le RC et le RL »", "capacite": "toutes", "moments": ["centre", "branches", "complete"], "poignees": []},
  {"id": "v_circuit_lc", "fichier": "circuit-lc.html", "vues": ["montage", "bascule", "echange"], "ce_que_ca_montre": "montage : E, K deux positions, condensateur, bobine (L, r), R, oscilloscope sur u_C ; bascule : K passe sur la bobine, électrons qui vont et viennent, signes des armatures qui s'inversent, u_C(t) qui se trace ; echange : à côté du circuit, barres E_e (rouge) et E_m (verte) synchronisées", "capacite": "RLC1, RLC5", "moments": ["montage", "charge", "bascule", "u_nulle_i_max", "recharge_inverse", "retour", "periode"], "poignees": ["K"]},
  {"id": "v_equation", "fichier": "equation.html", "ce_que_ca_montre": "le circuit après bascule, flèches u_C, u_R, u_b et i ; chaque tension remplacée sous sa flèche ; i = dq/dt puis di/dt = d²q/dt² ; équation en q, puis en u_C ; le terme (R + r) barré pour le LC", "capacite": "RLC2", "moments": ["fleches", "additivite", "remplacer", "deriver_deux_fois", "equation_q", "equation_uc", "lc_ideal"], "poignees": []},
  {"id": "v_oscillogramme", "fichier": "oscillogramme.html", "vues": ["periodique", "pseudo", "aperiodique", "critique"], "ce_que_ca_montre": "écran d'oscilloscope réaliste (grille, sensibilités) ; u_C(t) qui se trace pour la vue choisie ; poignée R : le régime change sous les yeux ; mesure n·T entre sommets ; T comparée à T₀", "capacite": "RLC4, RLC7", "moments": ["trace", "premier_sommet", "sommets_decroissants", "mesure_nT", "T_voisine_T0", "retour_sans_oscillation", "frontiere"], "poignees": ["R"]},
  {"id": "v_solution", "fichier": "solution.html", "vues": ["cos", "phase"], "ce_que_ca_montre": "cos : u_C = U_m·cos(2πt/T₀ + φ) tracée, U_m et T₀ lus, dérivées écrites ; phase : poignée sur le point de départ, u_C(0) et le sens de départ, deux angles possibles, le bon φ choisi", "capacite": "RLC3", "moments": ["courbe", "Um", "T0", "derivee_1", "derivee_2", "identification", "depart", "deux_angles", "phi_choisi"], "poignees": ["φ", "u_C(0)"]},
  {"id": "v_periode", "fichier": "periode.html", "vues": ["T0", "influence_L", "influence_C"], "ce_que_ca_montre": "T0 : T₀ lue puis calculée 2π√(LC), homogénéité (unités H et F) ; influence_L / influence_C : deux courbes superposées, L (ou C) multipliée par 4 → T₀ doublée ; E changée → T₀ inchangée", "capacite": "RLC3, RLC7", "moments": ["lecture_T0", "calcul_T0", "unites", "L_fois_4", "C_fois_4", "E_change"], "poignees": ["L", "C"]},
  {"id": "v_energie", "fichier": "energie.html", "vues": ["echange", "amortie"], "ce_que_ca_montre": "echange : courbes E_e(t), E_m(t) et E totale (horizontale), E_e maximale deux fois par T₀ ; amortie : E en escalier qui descend, résistance qui chauffe, énergie perdue entre deux sommets calculée, dE/dt = −(R + r)·i² écrit", "capacite": "RLC5", "moments": ["depart", "echange", "tout_bobine", "somme_constante", "pertes", "deux_sommets", "derivee"], "poignees": ["R"]},
  {"id": "v_entretien", "fichier": "entretien.html", "ce_que_ca_montre": "circuit RLC + boîte G (u_G = R₀·i) ; poignée R₀ : R₀ < R + r amorti, R₀ = R + r sinusoïde d'amplitude constante à T₀ ; l'équation dont le terme du milieu s'annule", "capacite": "RLC6", "moments": ["amorti", "dispositif", "equation", "compensation", "entretenu", "periode_T0"], "poignees": ["R₀"]},
  {"id": "v_analogie", "fichier": "analogie.html", "ce_que_ca_montre": "à valider : balançoire (ou pendule) peinte de façon réaliste à côté de u_C(t), en phase ; dans l'air, l'eau, le miel (trois régimes)", "capacite": "RLC1, RLC4", "moments": ["lache", "point_bas", "remonte", "air", "eau", "miel"], "poignees": ["frottement"]},
  {"id": "v_figures", "fichier": "figures.html", "ce_que_ca_montre": "figures fixes des nationaux redessinées (?fig=)", "capacite": "RLC7", "moments": [], "poignees": []},
  {"id": "v_bilan", "fichier": "bilan.html", "ce_que_ca_montre": "fiche « Ce qu'il faut retenir » (blocs)", "capacite": "toutes", "moments": [], "poignees": []},
 ],
 "manips_labo_3d": "aucune manip RLC dans labo-3d (seulement rc) : non créée ce passage ; à proposer plus tard (décharge de C dans L à l'oscilloscope, mesurer T₀ pour deux valeurs de C, puis ajouter R).",
}

regles_des_simulations = ("Aucune ancienne simulation n'est reprise : physics/advanced/electricity (CircuitLab, variante rlc) est un ancien labo, à recréer à la craie. "
  "Chaque simulation : craie sur tableau transparent, moments nommés, play_until, highlight, ce_qui_se_voit ; rien hors cadre (pas de facteur de qualité, pas de R critique, pas de α, pas de résonance) ; "
  "l'écran d'oscilloscope peint de façon réaliste, la craie pour les mesures et les écritures ; "
  "écriture des formules comme au cahier (u_C, L·d²q/dt², T₀ = 2π√(LC), E = ½·C·u_C² + ½·L·i², u = R₀·i) ; unités et nombres lisibles ; même kit et même style que dipole-rc-tableau et dipole-rl-tableau.")
