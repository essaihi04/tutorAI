# Exercice de chimie (physique-chimie), ch. 9 « Transformations lentes et transformations rapides », niveau facile n° 1 :
# une lame de zinc dans une solution d'ions cuivre II (couples, demi-équations, équation, n = C·V).
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture backend/data/curriculum/architecture/
#    phys_ch9_transformations_lentes_rapides.md (+ _voix.json), relevé des profs sources_chimie_ch9_ch11.md (Mahajar-Tabit,
#    Bendaoud, Sbiro, El Goufifa, Karzazi : « couples et équation » = premier exercice type ; Cu + Ag⁺ et Zn + Cu²⁺ en ouverture),
#    docs/parties_voix/phys_ch9_transformations_lentes_rapides.json ;
#  - le cours phys_ch9 (tl_x1_zinc, tl_x2_oxydant, tl_x7_equation, tl_rp4_concentration) : ce qui a été enseigné ;
#  - nationaux (exam.json) : demi-équations et équation écrites dans les parties piles / électrolyse (2016 R, 2018 R, 2023 R) ;
#  - séries en ligne : recherche faite (talamidi « série d'exercices 1 », moutamadris « exercices 9-2 », dreamjob, alloschool) ;
#    les PDF n'ont pas pu être ouverts (hôtes hors du réseau autorisé de la session) : seuls les extraits de recherche
#    (« écrire les demi-équations… établir l'équation », « quantités de matière initiales ») ont été lus.
#  Données = celles des simulations (rappels.html?vue=concentration : 0,01 mol dans 100 mL, C = 0,1 mol/L).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch9_lentes_rapides_1"
SIM = "/media/simulations/chimie/transformations-lentes-rapides-tableau/"


def becher(titre, solution, lame, depot, legende):
    """Bécher avec une lame métallique plongée (schéma). solution, depot : (ligne 1, ligne 2)."""
    return schema(titre, 12, 5.6,
        fil([1, 4.4], [1, 0.6], [7, 0.6], [7, 4.4]),
        [{"f": "ligne", "pts": [[1, 3.6], [7, 3.6]], "couleur": "bleu", "trait": "pointille"}],
        [{"f": "rect", "de": [4.7, 1.2], "a": [5.3, 5.0], "couleur": "faible"}],
        [{"f": "ligne", "pts": [[4.7, 1.3], [4.7, 3.4]], "couleur": "orange", "epais": True},
         {"f": "ligne", "pts": [[5.3, 1.3], [5.3, 3.4]], "couleur": "orange", "epais": True}],
        texte([5.0, 5.3], lame),
        texte([2.75, 2.5], solution[0], couleur="bleu"), texte([2.75, 1.9], solution[1], couleur="bleu"),
        [{"f": "fleche", "de": [7.7, 2.5], "a": [5.45, 2.3], "couleur": "orange"}],
        texte([7.8, 2.8], depot[0], couleur="orange", ancre="gauche"), texte([7.8, 2.2], depot[1], couleur="orange", ancre="gauche"),
        legende=legende)


C, V = 0.1, 0.100
N0 = C * V                       # 0,01 mol
assert abs(N0 - 1.0e-2) < 1e-12
C2, V2 = 0.02, 0.050
N0b = C2 * V2                    # 1,0·10⁻³ mol
assert abs(N0b - 1.0e-3) < 1e-12

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "transformations_lentes_rapides", "cours": "phys_ch9_transformations_lentes_rapides",
  "titre": "Le zinc dans les ions cuivre II : couples, équation et quantité de matière", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Écrire la demi-équation d'un couple oxydant/réducteur", "Établir l'équation d'une réaction d'oxydoréduction et la vérifier",
                  "Calculer une quantité de matière n = C·V"],
  "enonce": {
    "intro": "On plonge une lame de zinc Zn(s) dans un volume V = 100 mL d'une solution de sulfate de cuivre II, de concentration C = 0,1 mol/L en ions cuivre II Cu²⁺(aq) (figure 1). Après quelques minutes, un dépôt rouge de cuivre apparaît sur la lame et la couleur bleue de la solution pâlit.",
    "intro_dit": "نقراو l'énoncé. كنحطو une lame de zinc فواحد la solution de sulfate de cuivre deux، le volume ديالها V égale cent millilitres، و la concentration ديال les ions cuivre deux C égale zéro virgule un mole par litre. من بعد شي minutes، كيبان على la lame un dépôt rouge ديال le cuivre، واللون الأزرق ديال la solution كيضعاف.",
    "figures": [becher("Figure 1 : la lame de zinc dans la solution", ("solution bleue", "Cu²⁺(aq)"), "lame de zinc Zn(s)", ("dépôt rouge", "de cuivre Cu(s)"),
                       "Le dépôt rouge se forme sur la partie de la lame plongée dans la solution.")],
    "donnees": ["V = 100 mL = 0,100 L", "C = [Cu²⁺]₀ = 0,1 mol/L", "Couples : Cu²⁺(aq)/Cu(s) et Zn²⁺(aq)/Zn(s)"],
    "questions": [
      question("1", "Écrire la demi-équation électronique de chaque couple. Préciser l'espèce qui joue le rôle d'oxydant et celle qui joue le rôle de réducteur dans cette transformation.",
        "السؤال un: كتب la demi-équation électronique ديال كل couple. ومن بعد قول شكون هو l'oxydant و شكون هو le réducteur فهاد la transformation.",
        phrase("Cu²⁺(aq) + 2e⁻ ⇌ Cu(s) ; Zn²⁺(aq) + 2e⁻ ⇌ Zn(s). L'oxydant qui réagit est l'ion Cu²⁺(aq) : il capte 2 électrons et devient Cu(s). Le réducteur qui réagit est Zn(s) : il cède 2 électrons et devient Zn²⁺(aq)."),
        ["Ox + n e⁻ ⇌ Red", "2e⁻", "⇌", "Cu²⁺(aq)", "Zn(s)", "capte", "cède"], ["Cu(s) + 2e⁻ ⇌ Cu²⁺(aq)", "le zinc est l'oxydant"],
        [aide("Une demi-équation s'écrit toujours dans le même ordre : l'oxydant à gauche, avec les électrons, et le réducteur à droite. Qui disparaît sur la lame, qui apparaît ?",
              "la demi-équation ديما بنفس الترتيب: l'oxydant على اليسار مع les électrons، و le réducteur على اليمين. شوف شنو كيتكون على la lame، وشنو كيمشي ف la solution."),
         aide("Ox + n e⁻ ⇌ Red : ici n = 2 pour les deux couples (charge +2). Le cuivre se dépose : Cu²⁺ capte les électrons, c'est l'oxydant ; le zinc les cède, c'est le réducteur.",
              "oxydant plus n électrons donne réducteur. هنا n égale deux فبجوج، حيت la charge هي plus deux. le cuivre كيتكون: إذن l'ion cuivre deux كيشد les électrons، هو l'oxydant. و le zinc كيعطيهم، هو le réducteur.")],
        corr([("1 : Cu²⁺(aq) + 2e⁻ ⇌ Cu(s)", "ion cuivre deux plus deux électrons donne cuivre"),
              ("Zn²⁺(aq) + 2e⁻ ⇌ Zn(s)", "ion zinc deux plus deux électrons donne zinc"),
              ("Oxydant : Cu²⁺(aq), il capte 2 e⁻ ; réducteur : Zn(s), il cède 2 e⁻.", "l'oxydant هو l'ion cuivre deux")],
             "السؤال un. le couple ion cuivre deux sur cuivre: ion cuivre deux plus deux électrons donne cuivre. و le couple ion zinc deux sur zinc: ion zinc deux plus deux électrons donne zinc. فهاد la transformation، l'oxydant هو l'ion cuivre deux، كيشد les deux électrons. و le réducteur هو le zinc، كيعطي les deux électrons."),
        "ex_tl1_1", "fa_tl1_1"),
      question("2", "En déduire l'équation de la réaction d'oxydoréduction. Vérifier la conservation des éléments et des charges.",
        "السؤال deux: استنتج l'équation ديال la réaction d'oxydoréduction، ومن بعد تأكد من les éléments و les charges.",
        phrase("Réduction : Cu²⁺(aq) + 2e⁻ → Cu(s) ; oxydation : Zn(s) → Zn²⁺(aq) + 2e⁻. Même nombre d'électrons : on additionne. Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s). Éléments : Zn 1 = 1, Cu 1 = 1 ; charges : +2 à gauche, +2 à droite."),
        ["→", "Zn(s)", "Cu²⁺(aq)", "Zn²⁺(aq)", "Cu(s)", "charges"], ["Zn²⁺(aq) + Cu(s) → Zn(s) + Cu²⁺(aq)", "Zn(s) + Cu²⁺(aq) + 2e⁻ → Zn²⁺(aq) + Cu(s)"],
        [aide("La réduction de l'oxydant d'un couple et l'oxydation du réducteur de l'autre couple : le zinc donne ses électrons, l'ion cuivre II les reçoit. Combien d'électrons de chaque côté ?",
              "la réduction ديال l'oxydant، و l'oxydation ديال le réducteur ديال le couple الآخر. le zinc كيعطي les électrons، و l'ion cuivre deux كيشدهم. شحال من électron من كل جهة؟"),
         aide("Écris l'oxydation dans l'autre sens : Zn → Zn²⁺ + 2e⁻. Les deux demi-équations ont 2e⁻ : additionne-les, les électrons disparaissent. Compte ensuite les atomes et les charges.",
              "كتب l'oxydation فالاتجاه الآخر: zinc donne ion zinc deux plus deux électrons. les deux demi-équations ont deux électrons: جمعهم، و les électrons كيمشيو. ومن بعد حسب les atomes و les charges.")],
        corr([("2 : Cu²⁺(aq) + 2e⁻ → Cu(s) et Zn(s) → Zn²⁺(aq) + 2e⁻", "zinc donne ion zinc deux plus deux électrons"),
              ("Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)", "zinc plus ion cuivre deux، donne ion zinc deux plus cuivre"),
              ("Vérification : Zn 1 = 1 ; Cu 1 = 1 ; charges +2 = +2.", "plus deux على اليسار، و plus deux على اليمين")],
             "السؤال deux. la réduction: ion cuivre deux plus deux électrons donne cuivre. l'oxydation: zinc donne ion zinc deux plus deux électrons. نفس العدد ديال les électrons، إذن كنجمعو. l'équation: zinc plus ion cuivre deux، donne ion zinc deux plus cuivre. نتأكدو: un zinc et un cuivre من كل جهة، و les charges، plus deux على اليسار، و plus deux على اليمين."),
        "ex_tl1_2", "fa_tl1_2"),
      question("3", "Calculer la quantité de matière initiale n₀(Cu²⁺) des ions cuivre II dans la solution.",
        "السؤال trois: حسب la quantité de matière initiale ديال les ions cuivre deux ف la solution.",
        valeur("n₀(Cu²⁺)", 0.01, "mol", "n₀(Cu²⁺) = C·V = 0,1 × 0,100 = 1,0·10⁻² mol"),
        ["n = C·V", "C = n/V", "0,100 L", "mL → L", "mol"], ["n = C/V", "n = 0,1 × 100 = 10 mol"],
        [aide("On connaît la concentration C en mol/L et le volume V. Écris d'abord V en litres : 100 mL = ? L.",
              "عندنا la concentration C ب mole par litre، و le volume V. كتب V بالlitre: cent millilitres، شحال من litre؟"),
         aide("C = n/V, donc n = C·V, avec C en mol/L et V en L ; 100 mL = 0,100 L.",
              "C égale n sur V، إذن n égale C fois V. C ب mole par litre، و V بالlitre: cent millilitres égale zéro virgule un litre.")],
        corr([("3 : n₀(Cu²⁺) = C·V", "n zéro égale C fois V"),
              ("A.N. : n₀(Cu²⁺) = 0,1 × 0,100", "zéro virgule un fois zéro virgule un"),
              ("n₀(Cu²⁺) = 1,0·10⁻² mol", "un fois dix puissance moins deux mole")],
             "السؤال trois. n zéro égale C fois V. l'application numérique: zéro virgule un fois zéro virgule un litre. n zéro égale un fois dix puissance moins deux mole، يعني zéro virgule zéro un mole."),
        "ex_tl1_3", "fa_tl1_3"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_tl1_1", "Question 1 : qui cède, qui capte ?", "Le zinc cède 2 électrons (réducteur), l'ion Cu²⁺ les capte (oxydant).",
      SIM + "transfert.html?vue=zinc", "La lame de zinc dans la solution bleue, puis la loupe sur le transfert des électrons",
      "شوف le bécher: la solution زرقاء، فيها les ions cuivre deux، و la lame de zinc. نخليو الوقت يدوز. شوف la lame: un dépôt rouge، هادا هو le cuivre. دابا بالloupe: l'atome de zinc كيعطي les deux électrons، و l'ion cuivre deux كيشدهم وكيولي cuivre. اللي كيعطي les électrons هو le réducteur: le zinc. واللي كيشد les électrons هو l'oxydant: l'ion cuivre deux. la demi-équation ديال كل couple: oxydant plus deux électrons donne réducteur. ion cuivre deux plus deux électrons donne cuivre، و ion zinc deux plus deux électrons donne zinc.",
      centre=[("Cu²⁺(aq) + 2e⁻ ⇌ Cu(s)", "ion cuivre deux plus deux électrons donne cuivre"), ("Zn²⁺(aq) + 2e⁻ ⇌ Zn(s)", "ion zinc deux plus deux électrons donne zinc")],
      pointage=[{"mot": "شوف le bécher", "commande": "play_until", "parametres": {"moment": "depart"}},
                {"mot": "شوف la lame", "commande": "play_until", "parametres": {"moment": "depot"}},
                {"mot": "دابا بالloupe", "commande": "play_until", "parametres": {"moment": "loupe"}},
                {"mot": "l'atome de zinc كيعطي les deux électrons", "commande": "play_until", "parametres": {"moment": "electrons"}},
                {"mot": "اللي كيعطي les électrons هو le réducteur", "commande": "play_until", "parametres": {"moment": "etiquettes"}},
                {"mot": "اللي كيعطي les électrons هو le réducteur", "repere": "etiquette_reducteur"},
                {"mot": "واللي كيشد les électrons هو l'oxydant", "repere": "etiquette_oxydant"},
                {"mot": "ion cuivre deux plus deux électrons donne cuivre", "cible": "centre:0"},
                {"mot": "ion zinc deux plus deux électrons donne zinc", "cible": "centre:1"}]),
    diapo_sim("ex_tl1_2", "Question 2 : de deux demi-équations à l'équation", "Même nombre d'électrons : on additionne, les électrons disparaissent.",
      SIM + "equation.html?vue=zinc_cuivre", "La réduction de Cu²⁺, l'oxydation de Zn, l'addition, puis la vérification des charges",
      "عندنا les deux couples: ion cuivre deux sur cuivre، و ion zinc deux sur zinc. اللول، la réduction ديال l'oxydant: ion cuivre deux plus deux électrons donne cuivre. التاني، l'oxydation ديال le réducteur، فالاتجاه الآخر: zinc donne ion zinc deux plus deux électrons. le zinc كيعطي les deux électrons، و l'ion cuivre كيشد les deux électrons: نفس العدد، ما كاين ما نضربو. كنجمعو، و les électrons كيمشيو. l'équation: zinc plus ion cuivre deux، donne ion zinc deux plus cuivre. نتأكدو من les charges: plus deux على اليسار، و plus deux على اليمين.",
      centre=[("Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)", "l'équation: zinc plus ion cuivre deux")],
      pointage=[{"mot": "عندنا les deux couples", "commande": "play_until", "parametres": {"moment": "couples"}},
                {"mot": "اللول، la réduction", "commande": "play_until", "parametres": {"moment": "reduction"}},
                {"mot": "التاني، l'oxydation", "commande": "play_until", "parametres": {"moment": "oxydation"}},
                {"mot": "نفس العدد، ما كاين ما نضربو", "commande": "play_until", "parametres": {"moment": "multiplier"}},
                {"mot": "كنجمعو، و les électrons كيمشيو", "commande": "play_until", "parametres": {"moment": "additionner"}},
                {"mot": "l'équation: zinc plus ion cuivre deux", "cible": "centre:0"},
                {"mot": "نتأكدو من les charges", "commande": "play_until", "parametres": {"moment": "verifier"}},
                {"mot": "نتأكدو من les charges", "repere": "charges"}]),
    diapo_sim("ex_tl1_3", "Question 3 : n = C·V", "C = n/V, donc n = C·V : 0,1 mol/L × 0,100 L = 0,01 mol.",
      SIM + "rappels.html?vue=concentration", "Un soluté dans cent millilitres : C = n/V",
      "شوف هاد le bécher: zéro virgule zéro un mole ديال le soluté، dans cent millilitres. la concentration égale zéro virgule un mole par litre. la relation: C égale n sur V. إذن n égale C fois V. رد البال: V خاصو يكون بالlitre. cent millilitres، يعني zéro virgule un litre. فالتمرين ديالنا، نفس الأرقام: zéro virgule un mole par litre، fois zéro virgule un litre، donne zéro virgule zéro un mole، يعني un fois dix puissance moins deux mole.",
      centre=[("n = C·V = 0,1 × 0,100 = 1,0·10⁻² mol", "donne zéro virgule zéro un mole")],
      pointage=[{"mot": "شوف هاد le bécher", "commande": "play_until", "parametres": {"moment": "becher"}},
                {"mot": "la relation: C égale n sur V", "commande": "play_until", "parametres": {"moment": "formule"}},
                {"mot": "la relation: C égale n sur V", "repere": "formule"},
                {"mot": "donne zéro virgule zéro un mole", "cible": "centre:0"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_tl1_1", "Plus facile : le rôle du zinc", "سؤال ساهل: شنو هو الدور ديال le zinc؟",
      "Dans la réaction Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s), le zinc Zn(s) est…",
      ["l'oxydant : il capte des électrons", "le réducteur : il cède des électrons", "le réducteur : il capte des électrons"], 1, {
        "1": {"juste": rep("برافو! le zinc كيعطي les deux électrons وكيولي ion zinc deux: هو le réducteur.", "Juste : Zn cède 2 électrons, c'est le réducteur.")},
        "0": {"1": rep("ما تقلقش. شوف le zinc: كيولي ion zinc deux، يعني plus deux. واش كيشد les électrons ولا كيعطيهم؟ عاود اختار.", "Zn devient Zn²⁺ : il gagne ou il perd des électrons ? Réessaie."),
              "2": rep("الجواب: le zinc هو le réducteur، كيعطي les électrons. l'oxydant هنا هو l'ion cuivre deux، هو اللي كيشدهم.", "Réponse : Zn est le réducteur (il cède 2 e⁻) ; l'oxydant est Cu²⁺.")},
        "2": {"1": rep("قريب: le zinc هو le réducteur. ولكن le réducteur واش كيشد les électrons ولا كيعطيهم؟ عاود اختار.", "Oui, c'est le réducteur. Mais un réducteur capte-t-il ou cède-t-il des électrons ? Réessaie."),
              "2": rep("الجواب: le réducteur كيعطي les électrons. اللي كيشد les électrons هو l'oxydant.", "Réponse : un réducteur cède des électrons ; c'est l'oxydant qui en capte.")}},
      "Dans la réaction du zinc avec les ions cuivre deux, le zinc est ?"),
    vrai_faux_facile("fa_tl1_2", "Plus facile : vrai ou faux", "قول واش هاد الجمل صحيحة ولا غالطة.",
      "L'équation Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s).",
      [("Dans l'équation de la réaction, les électrons n'apparaissent pas.", True, "Les 2 électrons cédés par Zn sont captés par Cu²⁺ : ils s'éliminent quand on additionne."),
       ("Les charges sont conservées : +2 à gauche et +2 à droite.", True, "À gauche 0 + 2 = +2, à droite +2 + 0 = +2."),
       ("L'équation Zn²⁺(aq) + Cu(s) → Zn(s) + Cu²⁺(aq) décrit aussi l'expérience.", False, "Dans l'expérience, le cuivre se dépose et le zinc disparaît : les réactifs sont Zn(s) et Cu²⁺(aq).")]),
    qcm_facile("fa_tl1_3", "Plus facile : n = C·V", "سؤال ساهل على n égale C fois V.",
      "C = 0,1 mol/L et V = 100 mL. La quantité de matière n vaut…",
      ["10 mol", "1,0·10⁻² mol", "1,0 mol"], 1, {
        "1": {"juste": rep("برافو! zéro virgule un fois zéro virgule un litre donne zéro virgule zéro un mole.", "Juste : n = 0,1 × 0,100 = 1,0·10⁻² mol.")},
        "0": {"1": rep("ما تقلقش. واش خدمتي avec cent millilitres؟ V خاصو يكون بالlitre. عاود اختار.", "As-tu laissé V en mL ? Il faut V en litres. Réessaie."),
              "2": rep("الجواب: zéro virgule zéro un mole. le résultat dix mole، c'est zéro virgule un fois cent: V بقا بالmillilitre.", "Réponse : 1,0·10⁻² mol ; 10 mol vient de 0,1 × 100 avec V en mL.")},
        "2": {"1": rep("قريب. un mole هي C sur V: zéro virgule un sur zéro virgule un. ولكن n هي C fois V. عاود اختار.", "1,0 mol, c'est C/V. Or n = C·V. Réessaie."),
              "2": rep("الجواب: n égale C fois V، يعني zéro virgule zéro un mole. un mole جات من C sur V.", "Réponse : n = C·V = 1,0·10⁻² mol (1,0 mol vient de C/V).")}},
      "C égale zéro virgule un mole par litre، و V égale cent millilitres. La quantité de matière n vaut ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "On plonge un fil de cuivre Cu(s) dans V = 50 mL d'une solution de nitrate d'argent de concentration C = 0,02 mol/L en ions argent Ag⁺(aq). Après quelques minutes, un dépôt gris d'argent recouvre le fil et la solution devient bleue.",
      "intro_dit": "نفس التمرين، بمعطيات أخرى. un fil de cuivre ف la solution de nitrate d'argent: V égale cinquante millilitres، و C égale zéro virgule zéro deux mole par litre. كيبان dépôt gris ديال l'argent، و la solution كتولي زرقاء.",
      "figures": [becher("Figure 1 : le fil de cuivre dans la solution", ("solution", "Ag⁺(aq)"), "fil de cuivre Cu(s)", ("dépôt gris", "d'argent Ag(s)"),
                         "La solution bleuit : des ions Cu²⁺(aq) apparaissent.")],
      "donnees": ["V = 50 mL = 0,050 L", "C = [Ag⁺]₀ = 0,02 mol/L", "Couples : Ag⁺(aq)/Ag(s) et Cu²⁺(aq)/Cu(s)"],
      "questions": [
        question_semblable("1", "Écrire la demi-équation électronique de chaque couple. Préciser l'oxydant et le réducteur qui réagissent.",
          phrase("Ag⁺(aq) + e⁻ ⇌ Ag(s) ; Cu²⁺(aq) + 2e⁻ ⇌ Cu(s). L'oxydant qui réagit est Ag⁺(aq) (il capte un électron) ; le réducteur est Cu(s) (il cède 2 électrons)."),
          ["Ox + n e⁻ ⇌ Red", "e⁻", "Ag⁺(aq)", "Cu(s)"], ["Ag(s) + e⁻ ⇌ Ag⁺(aq)", "le cuivre est l'oxydant"],
          corr([("1 : Ag⁺(aq) + e⁻ ⇌ Ag(s) ; Cu²⁺(aq) + 2e⁻ ⇌ Cu(s)", "ion argent plus un électron donne argent"),
                ("Oxydant : Ag⁺(aq) ; réducteur : Cu(s).", "l'oxydant هو l'ion argent")],
               "ion argent plus un électron donne argent. ion cuivre deux plus deux électrons donne cuivre. l'oxydant هو l'ion argent، و le réducteur هو le cuivre.")),
        question_semblable("2", "En déduire l'équation de la réaction. Vérifier la conservation des éléments et des charges.",
          phrase("Ag⁺(aq) + e⁻ → Ag(s) (× 2) ; Cu(s) → Cu²⁺(aq) + 2e⁻. Cu(s) + 2Ag⁺(aq) → Cu²⁺(aq) + 2Ag(s). Éléments : Cu 1 = 1, Ag 2 = 2 ; charges : +2 = +2."),
          ["× 2", "→", "2Ag⁺(aq)", "Cu²⁺(aq)"], ["Cu(s) + Ag⁺(aq) → Cu²⁺(aq) + Ag(s)"],
          corr([("2 : on multiplie la demi-équation de l'argent par 2", "fois deux"),
                ("Cu(s) + 2Ag⁺(aq) → Cu²⁺(aq) + 2Ag(s) ; charges +2 = +2", "cuivre plus deux ions argent")],
               "le cuivre كيعطي les deux électrons، و l'ion argent كيشد seulement un électron: كنضربو la demi-équation ديال l'argent fois deux. cuivre plus deux ions argent، donne ion cuivre deux plus deux argent. les charges: plus deux من كل جهة.")),
        question_semblable("3", "Calculer la quantité de matière initiale n₀(Ag⁺) des ions argent.",
          valeur("n₀(Ag⁺)", 1.0e-3, "mol", "n₀(Ag⁺) = C·V = 0,02 × 0,050 = 1,0·10⁻³ mol"), ["n = C·V", "0,050 L", "mol"], ["n = 0,02 × 50 = 1 mol"],
          corr([("3 : n₀(Ag⁺) = C·V = 0,02 × 0,050", "n zéro égale C fois V"), ("n₀(Ag⁺) = 1,0·10⁻³ mol", "un fois dix puissance moins trois mole")],
               "n zéro égale C fois V، يعني zéro virgule zéro deux fois zéro virgule zéro cinq litre. n zéro égale un fois dix puissance moins trois mole.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
