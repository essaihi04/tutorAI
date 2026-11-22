# Exercice de chimie (physique-chimie), ch. 9 « Transformations lentes et transformations rapides », niveau facile n° 2 :
# trois béchers, trois durées — reconnaître une transformation rapide ou lente, le signe qui la suit, l'effet de la température.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture phys_ch9_transformations_lentes_rapides.md (+ _voix.json),
#    sources_chimie_ch9_ch11.md (5 cours de profs : rapides = MnO₄⁻ + Fe²⁺, précipitation AgCl, acide-base ; lentes = H₂O₂ + I⁻,
#    thiosulfate + acide sur une croix, MnO₄⁻ + acide oxalique ; température : KMnO₄ + acide oxalique à 20 °C et 40 °C),
#    docs/parties_voix/phys_ch9_transformations_lentes_rapides.json ;
#  - le cours phys_ch9 (tl_r1 à tl_r6, tl_f2_bains, tl_f1_facteur) : définitions lues mot à mot (« achevée dès que les réactifs
#    se rencontrent », « on distingue les états intermédiaires ») ;
#  - nationaux : 2018 N (« proposer deux facteurs cinétiques »), 2024 N (vrai/faux sur un facteur cinétique), 2025 N ;
#  - séries en ligne : recherche faite (talamidi, moutamadris, dreamjob, alloschool, kartable « rapide ou lente à l'aide d'une
#    description ») ; PDF non ouverts (hôtes hors du réseau autorisé de la session), seuls les extraits de recherche lus.
#  Durées = celles des simulations (bechers.html : Fe²⁺ décoloré aussitôt, acide oxalique ≈ 7 min, croix cachée vers 2 min).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch9_lentes_rapides_2"
SIM = "/media/simulations/chimie/transformations-lentes-rapides-tableau/"


def trois_bechers(titre, items, legende):
    """items : [(lettre, ligne 1, ligne 2, couleur)] — trois béchers côte à côte, observation écrite dessous."""
    g = []
    for k, (L, l1, l2, col) in enumerate(items):
        x = 0.6 + 4.2 * k
        g += fil([x, 4.2], [x, 1.6], [x + 3, 1.6], [x + 3, 4.2])
        g += [{"f": "ligne", "pts": [[x, 3.4], [x + 3, 3.4]], "couleur": col, "trait": "pointille"}]
        g += texte([x + 1.5, 2.5], L, couleur="jaune", taille="grand")
        g += texte([x + 1.5, 1.0], l1, couleur=col)
        g += texte([x + 1.5, 0.4], l2, couleur=col)
    return schema(titre, 13, 4.8, g, legende=legende)


EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "transformations_lentes_rapides", "cours": "phys_ch9_transformations_lentes_rapides",
  "titre": "Trois béchers, trois durées : rapide ou lente ?", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Reconnaître une transformation rapide ou lente et justifier", "Citer un signe qui permet de suivre une transformation lente",
                  "Reconnaître la température comme facteur cinétique"],
  "enonce": {
    "intro": "On réalise trois expériences à 20 °C (figure 1).\nA : on verse une solution d'ions fer II Fe²⁺(aq) dans une solution violette d'ions permanganate MnO₄⁻(aq) acidifiée : la couleur violette disparaît dès le mélange.\nB : on verse une solution d'acide oxalique H₂C₂O₄(aq) dans la même solution violette acidifiée : la couleur violette s'affaiblit peu à peu et disparaît au bout d'environ 7 min.\nC : on mélange une solution de thiosulfate de sodium et une solution d'acide chlorhydrique dans un bécher posé sur une croix noire : la croix disparaît au bout d'environ 2 min.",
    "intro_dit": "نقراو l'énoncé. trois expériences، à vingt degrés Celsius. l'expérience A: كنصبو les ions fer deux فواحد la solution بنفسجية ديال les ions permanganate، فوسط حمضي: اللون البنفسجي كيمشي فلحظة. l'expérience B: كنصبو l'acide oxalique فنفس la solution: اللون البنفسجي كيضعاف بشوية بشوية، وكيمشي من بعد environ sept minutes. l'expérience C: كنخلطو le thiosulfate de sodium مع l'acide chlorhydrique، فواحد le bécher فوق une croix كحلة: la croix كتختفي من بعد environ deux minutes.",
    "figures": [trois_bechers("Figure 1 : les trois expériences, à 20 °C",
                             [("A", "violet → incolore", "dès le mélange", "violet"), ("B", "violet → incolore", "en 7 min environ", "violet"),
                              ("C", "trouble jaune pâle", "croix cachée vers 2 min", "jaune")],
                             "Les durées sont mesurées avec un chronomètre, à 20 °C.")],
    "donnees": ["A : MnO₄⁻(aq) + 5Fe²⁺(aq) + 8H⁺(aq) → Mn²⁺(aq) + 5Fe³⁺(aq) + 4H₂O(l)",
                "B : 2MnO₄⁻(aq) + 5H₂C₂O₄(aq) + 6H⁺(aq) → 2Mn²⁺(aq) + 10CO₂(aq) + 8H₂O(l)",
                "C : S₂O₃²⁻(aq) + 2H⁺(aq) → S(s) + SO₂(aq) + H₂O(l)", "Les ions Mn²⁺(aq) sont pratiquement incolores."],
    "questions": [
      question("1", "Classer chacune des transformations A et B en transformation rapide ou lente. Justifier.",
        "السؤال un: صنف la transformation A و la transformation B: rapide ولا lente؟ برر الجواب.",
        phrase("A est rapide : elle est achevée dès que les réactifs se rencontrent, on ne distingue pas d'états intermédiaires (le violet disparaît aussitôt). B est lente : son évolution dure environ 7 min, on la suit à l'œil nu (le violet s'affaiblit peu à peu)."),
        ["rapide", "lente", "états intermédiaires", "à l'œil nu", "durée"], ["A est lente car elle forme peu de produit", "B est rapide car elle finit par se décolorer"],
        [aide("Regarde la durée de chaque transformation : peut-on voir la couleur changer peu à peu, ou tout est-il fini dès le mélange ?",
              "شوف la durée ديال كل transformation: واش كنشوفو اللون كيتبدل بشوية بشوية، ولا كلشي كيسالي فلحظة؟"),
         aide("Rapide : achevée dès que les réactifs se rencontrent, aucun état intermédiaire visible. Lente : dure de quelques secondes à plusieurs heures, on suit son évolution à l'œil nu.",
              "rapide: كتسالا dès que les réactifs se rencontrent، ما كنشوفو حتى état intermédiaire. lente: كتدوم من quelques secondes حتى plusieurs heures، ونقدرو نتبعوها بالعين.")],
        corr([("1 : A est rapide : achevée dès le mélange, aucun état intermédiaire observable.", "A هي rapide"),
              ("B est lente : elle dure environ 7 min ; on voit le violet s'affaiblir peu à peu.", "B هي lente")],
             "السؤال un. A هي rapide: اللون البنفسجي كيمشي dès que les réactifs se rencontrent، وما كنشوفوش des états intermédiaires. B هي lente: كتدوم environ sept minutes، وكنشوفو اللون كيضعاف بشوية بشوية، يعني on distingue les états intermédiaires."),
        "ex_tl2_1", "fa_tl2_1"),
      question("2", "Pour l'expérience C, quel signe permet de suivre l'évolution de la transformation ? Est-elle rapide ou lente ?",
        "السؤال deux: فl'expérience C، شنو هي العلامة اللي كتخلينا نتبعو la transformation؟ واش هي rapide ولا lente؟",
        phrase("Un trouble jaune pâle de soufre S(s) apparaît et s'épaissit peu à peu jusqu'à cacher la croix. On distingue des états intermédiaires pendant environ 2 min : la transformation C est lente."),
        ["soufre S(s)", "trouble", "croix", "lente", "états intermédiaires"], ["la couleur violette", "rapide car la croix disparaît"],
        [aide("Quel produit de l'équation C est un solide ? Que voit-on apparaître dans le bécher posé sur la croix ?",
              "شوف l'équation ديال C: شنو هو le produit اللي solide؟ شنو كيبان ف le bécher اللي فوق la croix؟"),
         aide("Le soufre S(s) forme un trouble qui grandit avec le temps. Si on voit l'état du mélange changer pendant une durée mesurable, la transformation est lente.",
              "le soufre كيدير un trouble، وهاد le trouble كيكبر مع الوقت. يلا كنشوفو le mélange كيتبدل خلال une durée، إذن la transformation lente.")],
        corr([("2 : signe : le trouble de soufre S(s), qui s'épaissit jusqu'à cacher la croix", "le trouble ديال le soufre"),
              ("Évolution visible pendant environ 2 min : la transformation C est lente.", "la transformation C هي lente")],
             "السؤال deux. العلامة هي le trouble ديال le soufre: كيبان وكيكبر بشوية بشوية، حتى كيخبي la croix. كنشوفو des états intermédiaires خلال environ deux minutes: إذن la transformation C هي lente."),
        "ex_tl2_2", "fa_tl2_2"),
      question("3", "On refait l'expérience B dans un bain-marie à 40 °C. La décoloration a-t-elle lieu plus tôt ou plus tard qu'à 20 °C ? Comment appelle-t-on le paramètre qu'on a modifié ?",
        "السؤال trois: كنعاودو l'expérience B فواحد le bain-marie à quarante degrés Celsius. واش اللون كيمشي قبل ولا من بعد؟ وشنو سميتو هاد le paramètre اللي بدلنا؟",
        phrase("La décoloration a lieu plus tôt : plus la température est élevée, plus la transformation est rapide. La température est un facteur cinétique : un paramètre qui modifie la vitesse d'évolution d'une transformation, donc sa durée (l'état final reste le même)."),
        ["plus tôt", "facteur cinétique", "température", "vitesse d'évolution"], ["plus tard", "un catalyseur", "l'état final change"],
        [aide("On garde les mêmes réactifs ; seule la température change. Rappelle-toi les deux béchers du cours, à 20 °C et à 40 °C : lequel a fini le premier ?",
              "نفس les réactifs، غير la température اللي تبدلات. عقل على les deux béchers ديال le cours، à vingt et à quarante degrés Celsius: شكون سالا اللول؟"),
         aide("À température plus élevée, la transformation est plus rapide. Un paramètre qui modifie la vitesse d'évolution d'une transformation s'appelle un facteur cinétique.",
              "à température plus élevée، la transformation est plus rapide. و un paramètre اللي كيبدل la vitesse d'évolution، سميتو un facteur cinétique.")],
        corr([("3 : à 40 °C, la décoloration a lieu plus tôt : la transformation est plus rapide.", "اللون كيمشي قبل"),
              ("La température est un facteur cinétique ; l'état final (incolore) est le même.", "la température est un facteur cinétique")],
             "السؤال trois. à quarante degrés Celsius، اللون كيمشي قبل: la transformation est plus rapide. إذن la température est un facteur cinétique، يعني un paramètre اللي كيبدل la vitesse d'évolution ديال la transformation، و la durée ديالها. ولكن l'état final هو هو."),
        "ex_tl2_3", "fa_tl2_3"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_tl2_1", "Question 1 : le même violet, deux durées", "Fe²⁺ : décoloré aussitôt, rapide ; acide oxalique : plusieurs minutes, lente.",
      SIM + "bechers.html?vue=comparer", "Deux béchers d'ions permanganate acidifiés : ions fer II à gauche, acide oxalique à droite",
      "شوف les deux béchers: فيهم نفس la solution بنفسجية، les ions permanganate فوسط حمضي. فوق اليسار، burette فيها les ions fer deux. فوق اليمين، burette فيها l'acide oxalique. دابا نصبو فبجوج فنفس الوقت. شوف اليسار: اللون مشا فلحظة. هادي transformation rapide: achevée dès que les réactifs se rencontrent. وشوف اليمين: اللون كيضعاف بشوية بشوية، و le chronomètre كيدور عدة minutes. هادي transformation lente: on distingue les états intermédiaires.",
      centre=[("A : rapide (aucun état intermédiaire)", "هادي transformation rapide"), ("B : lente (≈ 7 min, évolution visible)", "هادي transformation lente")],
      pointage=[{"mot": "شوف les deux béchers", "repere": "becher_rapide"},
                {"mot": "burette فيها les ions fer deux", "repere": "burette_fer"},
                {"mot": "burette فيها l'acide oxalique", "repere": "burette_oxalique"},
                {"mot": "دابا نصبو فبجوج", "commande": "play_until", "parametres": {"moment": "verser"}},
                {"mot": "شوف اليسار: اللون مشا فلحظة", "commande": "play_until", "parametres": {"moment": "rapide_fini"}},
                {"mot": "هادي transformation rapide", "cible": "centre:0"},
                {"mot": "وشوف اليمين", "commande": "play_until", "parametres": {"moment": "lente_continue"}},
                {"mot": "le chronomètre كيدور", "repere": "chrono"},
                {"mot": "هادي transformation lente", "commande": "play_until", "parametres": {"moment": "lente_finie"}},
                {"mot": "هادي transformation lente", "cible": "centre:1"}]),
    diapo_sim("ex_tl2_2", "Question 2 : le trouble de soufre", "Le soufre forme un trouble qui cache peu à peu la croix : transformation lente.",
      SIM + "bechers.html?vue=soufre", "Le bécher sur la croix noire : thiosulfate + acide",
      "شوف هاد le bécher: تحتو une croix كحلة. نخلطو les ions thiosulfate مع l'acide. فالبداية، المحلول شفاف، و la croix باينة. دابا شوف: كيبان un trouble jaune pâle، هادا le soufre اللي كيتكون. le trouble كيكبر بشوية بشوية، و le chronomètre كيحسب. وفالأخير، la croix ما بقاتش باينة. كنشوفو des états intermédiaires: إذن هادي transformation lente.",
      centre=[("S₂O₃²⁻(aq) + 2H⁺(aq) → S(s) + SO₂(aq) + H₂O(l)", "هادا le soufre اللي كيتكون"), ("Trouble de soufre visible peu à peu : lente", "إذن هادي transformation lente")],
      pointage=[{"mot": "شوف هاد le bécher", "repere": "becher"},
                {"mot": "تحتو une croix كحلة", "repere": "croix"},
                {"mot": "نخلطو les ions thiosulfate", "commande": "play_until", "parametres": {"moment": "melange"}},
                {"mot": "كيبان un trouble jaune pâle", "commande": "play_until", "parametres": {"moment": "trouble"}},
                {"mot": "هادا le soufre اللي كيتكون", "cible": "centre:0"},
                {"mot": "هادا le soufre اللي كيتكون", "repere": "trouble"},
                {"mot": "la croix ما بقاتش باينة", "commande": "play_until", "parametres": {"moment": "croix_cachee"}},
                {"mot": "إذن هادي transformation lente", "cible": "centre:1"}]),
    diapo_sim("ex_tl2_3", "Question 3 : la température, facteur cinétique", "Même mélange, deux températures : plus chaud, plus rapide ; même état final.",
      SIM + "facteurs.html?vue=temperature", "Le même mélange lent dans un bain à 20 °C et un bain à 40 °C",
      "هادي transformation lente ديال le cours: l'eau oxygénée مع les ions iodure. نفس le mélange dans deux béchers: le premier فالما à vingt degrés Celsius، والآخر à quarante degrés Celsius. شوف les thermomètres. دابا كنبداو. le bécher السخون كيولي brun قبل. وصل للون الأخير ديالو environ trois fois plus tôt. ومن بعد، حتى البارد كيوصل، ونفس brun فبجوج. إذن à température plus élevée، la transformation est plus rapide، و l'état final هو هو. la température est un facteur cinétique. نفس الشي ل l'acide oxalique فالتمرين: à quarante degrés، اللون البنفسجي كيمشي قبل.",
      centre=[("θ plus élevée : transformation plus rapide", "à température plus élevée، la transformation est plus rapide"), ("La température est un facteur cinétique", "la température est un facteur cinétique")],
      pointage=[{"mot": "نفس le mélange", "commande": "play_until", "parametres": {"moment": "melange"}},
                {"mot": "شوف les thermomètres", "repere": "thermometre_chaud"},
                {"mot": "دابا كنبداو", "commande": "play_until", "parametres": {"moment": "depart"}},
                {"mot": "le bécher السخون كيولي brun قبل", "commande": "play_until", "parametres": {"moment": "chaud_fini"}},
                {"mot": "حتى البارد كيوصل", "commande": "play_until", "parametres": {"moment": "froid_fini"}},
                {"mot": "ونفس brun فبجوج", "commande": "play_until", "parametres": {"moment": "meme_final"}},
                {"mot": "à température plus élevée، la transformation est plus rapide", "cible": "centre:0"},
                {"mot": "la température est un facteur cinétique", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_tl2_1", "Plus facile : l'expérience A", "سؤال ساهل على l'expérience A.",
      "Dans A, le violet disparaît dès qu'on verse les ions fer II. La transformation A est…",
      ["lente", "rapide", "très lente"], 1, {
        "1": {"juste": rep("برافو! achevée dès que les réactifs se rencontrent: rapide.", "Juste : achevée dès le mélange, c'est une transformation rapide.")},
        "0": {"1": rep("ما تقلقش. واش شفنا اللون كيتبدل بشوية بشوية؟ ولا مشا فلحظة؟ عاود اختار.", "A-t-on vu des états intermédiaires, ou tout est-il fini aussitôt ? Réessaie."),
              "2": rep("الجواب: rapide. lente كنشوفو فيها اللون كيتبدل بشوية، بحال B.", "Réponse : rapide ; une lente montre des états intermédiaires, comme B.")},
        "2": {"1": rep("لا، très lente كتدوم des jours ولا des années، بحال la rouille. هنا شحال دام؟ عاود اختار.", "Très lente = des jours ou des années (la rouille). Ici, combien de temps ? Réessaie."),
              "2": rep("الجواب: rapide، حيت اللون مشا dès le mélange. très lente هي بحال la rouille.", "Réponse : rapide (fini dès le mélange) ; très lente, c'est comme la rouille.")}},
      "Dans A، le violet disparaît dès qu'on verse les ions fer deux. La transformation A est ?"),
    vrai_faux_facile("fa_tl2_2", "Plus facile : vrai ou faux", "قول واش هاد الجمل صحيحة ولا غالطة.",
      "Expérience C : thiosulfate + acide, sur une croix noire.",
      [("Le trouble qui cache la croix est dû au soufre S(s) formé.", True, "Le soufre est le produit solide de l'équation C : il trouble la solution."),
       ("La transformation C est rapide, puisque la croix finit par disparaître.", False, "La croix disparaît au bout d'environ 2 min, peu à peu : on voit des états intermédiaires, C est lente.")]),
    qcm_facile("fa_tl2_3", "Plus facile : à 40 °C", "سؤال ساهل على la température.",
      "On refait B à 40 °C au lieu de 20 °C. La décoloration a lieu…",
      ["au même moment", "plus tard", "plus tôt"], 2, {
        "2": {"juste": rep("برافو! à température plus élevée، la transformation est plus rapide.", "Juste : plus chaud, plus rapide.")},
        "0": {"1": rep("فكر: la température واش كتبدل la durée؟ عقل على le bécher السخون ف le cours. عاود اختار.", "La température change-t-elle la durée ? Pense au bécher chaud du cours. Réessaie."),
              "2": rep("الجواب: plus tôt. la température est un facteur cinétique: كتبدل la durée.", "Réponse : plus tôt ; la température est un facteur cinétique.")},
        "1": {"1": rep("لا، البرد هو اللي كينقص الزربة، بحال le réfrigérateur. والسخون؟ عاود اختار.", "C'est le froid qui ralentit (le réfrigérateur). Et le chaud ? Réessaie."),
              "2": rep("الجواب: plus tôt. السخون كيمشي بالزربة la transformation، والبارد كينقصها.", "Réponse : plus tôt ; le chaud accélère, le froid ralentit.")}},
      "On refait B à quarante degrés Celsius au lieu de vingt. La décoloration a lieu ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres expériences",
    "enonce": {
      "intro": "Trois autres expériences à 20 °C.\nA : on verse une solution de nitrate d'argent (ions Ag⁺(aq)) dans une solution de chlorure de sodium (ions Cl⁻(aq)) : un précipité blanc de chlorure d'argent AgCl(s) apparaît dès le mélange.\nB : on mélange de l'eau oxygénée H₂O₂(aq) acidifiée et une solution d'iodure de potassium (ions I⁻(aq)) : la solution, incolore au départ, jaunit puis brunit peu à peu pendant environ 30 min.\nC : on plonge de la grenaille de zinc Zn(s) dans de l'acide chlorhydrique : des bulles de dihydrogène H₂(g) se dégagent pendant plusieurs minutes.",
      "intro_dit": "trois expériences أخرى، à vingt degrés Celsius. A: les ions argent مع les ions chlorure: un précipité blanc كيبان فلحظة. B: l'eau oxygénée مع les ions iodure: المحلول كيولي jaune ومن بعد brun بشوية بشوية، environ trente minutes. C: le zinc ف l'acide chlorhydrique: كيخرج le dihydrogène، des bulles خلال plusieurs minutes.",
      "figures": [trois_bechers("Figure 1 : les trois expériences, à 20 °C",
                               [("A", "précipité blanc", "dès le mélange", "blanc"), ("B", "incolore → brun", "en 30 min environ", "orange"),
                                ("C", "bulles de H₂(g)", "pendant plusieurs min", "cyan")],
                               "Les durées sont mesurées avec un chronomètre, à 20 °C.")],
      "donnees": ["A : Ag⁺(aq) + Cl⁻(aq) → AgCl(s)", "B : H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l)", "C : Zn(s) + 2H⁺(aq) → Zn²⁺(aq) + H₂(g)"],
      "questions": [
        question_semblable("1", "Classer chacune des transformations A et B en transformation rapide ou lente. Justifier.",
          phrase("A est rapide : le précipité apparaît dès que les réactifs se rencontrent, aucun état intermédiaire observable. B est lente : la couleur brune du diiode apparaît peu à peu pendant environ 30 min, on suit son évolution à l'œil nu."),
          ["rapide", "lente", "états intermédiaires"], ["B est rapide car la couleur finit par se stabiliser"],
          corr([("1 : A rapide : précipité dès le mélange.", "A هي rapide"), ("B lente : brunit peu à peu pendant 30 min.", "B هي lente")],
               "A هي rapide: le précipité كيبان dès que les réactifs se rencontrent. B هي lente: اللون brun كيبان بشوية بشوية خلال environ trente minutes.")),
        question_semblable("2", "Pour l'expérience C, quel signe permet de suivre l'évolution de la transformation ? Est-elle rapide ou lente ?",
          phrase("Le dégagement de bulles de dihydrogène H₂(g), qui dure plusieurs minutes : on suit l'évolution, la transformation C est lente."),
          ["gaz", "H₂(g)", "bulles", "lente"], ["rapide car le gaz se dégage tout de suite"],
          corr([("2 : signe : les bulles de dihydrogène H₂(g)", "les bulles ديال le dihydrogène"), ("Dégagement pendant plusieurs minutes : C est lente.", "C هي lente")],
               "العلامة هي les bulles ديال le dihydrogène، اللي كيخرجو خلال plusieurs minutes: إذن C هي lente.")),
        question_semblable("3", "On refait l'expérience B dans un bain d'eau glacée à 5 °C. La coloration brune finale est-elle atteinte plus tôt ou plus tard ? Comment appelle-t-on le paramètre modifié ?",
          phrase("Plus tard : à température plus basse, la transformation est plus lente. La température est un facteur cinétique (l'état final est le même)."),
          ["plus tard", "facteur cinétique", "température"], ["plus tôt", "l'état final change"],
          corr([("3 : à 5 °C, plus tard : la transformation est plus lente.", "plus tard"), ("La température est un facteur cinétique.", "la température est un facteur cinétique")],
               "à cinq degrés Celsius، اللون brun كيوصل plus tard: la transformation كتولي plus lente. la température est un facteur cinétique.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
