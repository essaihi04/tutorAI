# Exercice SVT ch. 1 (réactions responsables de la libération de l'énergie) — niveau moyen.
# Ce qu'il entraîne : exploiter un tableau de résultats (deux cultures de levures, avec / sans O₂) ; comparer avec des
# valeurs (« plus élevé chez … que chez … ») puis déduire la voie ; écrire les deux réactions globales avec l'ATP ;
# calculer un rapport et le rendement de la fermentation ; expliquer la différence par les bilans (2 / 38 ATP, résidu organique).
# Sources comparées (lecture seule, rien de copié) :
#   - exploration du cours (backend/data/curriculum/exploration/reactions_responsables_liberation_energie.json) :
#     cas_types levures, calcul, tableau_comparatif, voie_dominante ; pieges (CO₂ de la fermentation, éthanol CH3-CH2-OH,
#     × 100 du rendement) ; erreurs_examen (comparaison sans valeurs, rendement sans %) ; valeurs_reperes 38 / 2 ATP, 2,13 %.
#   - national 2019 R (deux souches de levures P et G, colonies, rendement 40 % / 2 %) : même compétence, autre situation
#     (ici UNE souche, deux milieux, un tableau de masses) ; national 2020 R (appariement des réactions globales) ;
#     national 2022 R (tableau 2 ATP / 36 ATP).
#   - vidéos des professeurs (exploration, sources.videos) : Abdellaoui (fermentation expliquée par son but, rendement
#     calculé), Ouissam (décrire / comparer / déduire), Bouhdadi (devoir corrigé : comparaison avec valeurs).
#   - séries en ligne (moutamadris, dyrassa, alloschool…) : réseau bloqué dans cette session (hôtes non résolus) ;
#     comparaison faite avec les vidéos et les nationaux ci-dessus.
# Données choisies pour que l'ATP explique la croissance : ATP ∝ 10 × 38 = 380 (A) et 50 × 2 = 100 (B) ; 380/100 = 3,8 =
# 4,75/1,25 ; levures par gramme de glucose : 0,475 / 0,025 = 19 = 38/2.
import sys
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

BASE = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/"
COMP = BASE + "comparer.html"
CARR = BASE + "carrefour.html?vue=complet&depart=0"
REND = BASE + "rendement.html?depart=0"
FERM = BASE + "fermentations.html?vue=alcoolique&depart=manque_taxis"


def tableau(titre, legende, entetes, lignes, larg):
    """Tableau dessiné (schema à cadre) : entetes = [..], lignes = [[cellule, ..], ..] ; une cellule peut être une liste
    de deux lignes de texte."""
    L = sum(larg); hl = 0.9; n = len(lignes) + 1; H = n * hl
    el = [{"f": "rect", "de": [0, 0], "a": [L, H], "couleur": "blanc"},
          {"f": "rect", "de": [0, H - hl], "a": [L, H], "couleur": "jaune", "remplir": "jaune"}]
    for i in range(1, n):
        el.append({"f": "ligne", "pts": [[0, H - i * hl], [L, H - i * hl]], "couleur": "faible"})
    x = 0
    for w in larg[:-1]:
        x += w; el.append({"f": "ligne", "pts": [[x, 0], [x, H]], "couleur": "faible"})
    for r, ligne in enumerate([entetes] + lignes):
        x = 0
        for c, (cel, w) in enumerate(zip(ligne, larg)):
            yc = H - (r + 0.5) * hl
            txt = cel if isinstance(cel, list) else [cel]
            for k, t in enumerate(txt):
                dy = 0 if len(txt) == 1 else (0.2 if k == 0 else -0.22)
                el.append({"f": "texte", "at": [round(x + w / 2, 3), round(yc + dy, 3)], "t": t, "taille": "petit",
                           "couleur": "jaune" if r == 0 else ("blanc" if c == 0 else "cyan")})
            x += w
    return {"type": "schema", "titre": titre, "legende": legende, "cadre": {"l": L, "h": round(H, 2)}, "elements": el}


def doc1(gA, gB, lA, lB, eB):
    fr = lambda v: str(v).replace(".", ",")
    return tableau("Document 1 : les deux cultures après 24 h", "Même souche de levures, même milieu de départ ; seule la présence du dioxygène change.",
                   ["Mesure (pour 1 L)", "Culture A (aérée)", "Culture B (sans O₂)"],
                   [["Glucose consommé (g)", fr(gA), fr(gB)],
                    ["Levures formées (g)", fr(lA), fr(lB)],
                    ["Éthanol produit (g)", "0", fr(eB)],
                    ["CO₂ dégagé", "oui", "oui"],
                    ["O₂ consommé", "oui", "pas d'O₂"],
                    ["Mitochondries", ["nombreuses,", "crêtes développées"], ["peu nombreuses,", "peu développées"]]],
                   [3.6, 3.2, 3.2])


EX = {
  "id": "svt_ex_ch1_fermentations_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "reactions_responsables_liberation_energie", "cours": "svt_ch1_reactions_responsables_liberation_energie",
  "titre": "Deux cultures de levures : respirer ou fermenter, et ce que cela rapporte", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Comparer des résultats avec des valeurs puis déduire", "Écrire les réactions globales de la respiration et de la fermentation alcoolique",
                  "Calculer un rapport et un rendement énergétique", "Expliquer une différence par les bilans énergétiques"],
  "enonce": {
    "intro": "On cultive la même souche de levures dans deux milieux identiques contenant du glucose. La culture A est constamment aérée (riche en dioxygène) ; la culture B est privée de dioxygène. Après 24 h, on mesure, pour 1 L de culture, le glucose consommé, la masse de levures formées (matière sèche) et l'éthanol produit, et on observe les levures au microscope électronique (document 1).",
    "intro_dit": "دابا نقراو l'énoncé. عندنا نفس les levures، dans deux milieux بحال بحال، فيهم le glucose. la culture A فيها le dioxygène ديما. la culture B بلا dioxygène. après vingt-quatre heures، قسنا le glucose اللي تستهلك، والكتلة ديال les levures اللي تكونو، و l'éthanol. وشفنا les levures بle microscope électronique. كلشي فle document un.",
    "figures": [doc1(10, 50, 4.75, 1.25, 23)],
    "donnees": ["Culture A (aérée) : glucose consommé 10 g/L ; levures formées 4,75 g/L ; éthanol 0 g/L",
                "Culture B (sans O₂) : glucose consommé 50 g/L ; levures formées 1,25 g/L ; éthanol 23 g/L",
                "Une mole d'ATP : 30,5 kJ ; une mole de glucose : 2860 kJ",
                "Respiration : 38 ATP par molécule de glucose ; fermentation alcoolique : 2 ATP"],
    "questions": [
      {"id": "1", "texte": "En exploitant le document 1, comparer les résultats des cultures A et B (glucose consommé, levures formées, éthanol), puis déduire la voie métabolique utilisée par les levures dans chaque culture. Justifier.",
       "texte_dit": "la question un: استغل le document un، وقارن les résultats ديال la culture A و la culture B: le glucose consommé، les levures formées، و l'éthanol. من بعد استنتج la voie métabolique ديال كل culture، وبرر.",
       "reponse": {"type": "phrase", "attendu": "Le glucose consommé est plus élevé chez B (50 g/L) que chez A (10 g/L), soit 5 fois plus. La masse de levures formées est plus élevée chez A (4,75 g/L) que chez B (1,25 g/L). L'éthanol n'est produit que par B (23 g/L ; 0 chez A). On en déduit que la culture A fait la respiration (O₂ consommé, mitochondries nombreuses à crêtes développées) et que la culture B fait la fermentation alcoolique (absence d'O₂, production d'éthanol et de CO₂, mitochondries peu développées)."},
       "clavier": {"aides": ["plus élevé chez … que chez …", "g/L", "éthanol", "respiration", "fermentation alcoolique", "On en déduit que"], "pieges": ["fermentation lactique", "photosynthèse"]},
       "aides": [
         {"texte": "Compare ligne par ligne : pour chaque mesure, quelle culture a la valeur la plus élevée ? Regarde aussi les lignes O₂ et mitochondries.",
          "dit": "قارن ligne par ligne: فكل mesure، شمن culture عندها la valeur الكبيرة؟ وشوف حتى la ligne ديال le dioxygène، و la ligne ديال les mitochondries."},
         {"texte": "Écris « … est plus élevé chez B (valeur) que chez A (valeur) ». Puis : O₂ consommé et mitochondries développées → quelle voie ? Sans O₂, avec éthanol → quelle voie ?",
          "dit": "كتب: plus élevé chez B، مع la valeur، que chez A، مع la valeur. من بعد: مع le dioxygène و des mitochondries développées، شمن voie؟ وبلا dioxygène، مع l'éthanol، شمن voie؟"}],
       "correction": {"lignes": [
           {"texte": "1 : glucose consommé : plus élevé chez B (50 g/L) que chez A (10 g/L)", "mot": "plus élevé chez B"},
           {"texte": "levures formées : plus élevé chez A (4,75 g/L) que chez B (1,25 g/L)", "mot": "plus élevé chez A"},
           {"texte": "éthanol : seulement chez B (23 g/L)", "mot": "seulement dans la culture B"},
           {"texte": "A : O₂ consommé, mitochondries développées : respiration", "mot": "la culture A كتدير la respiration"},
           {"texte": "B : sans O₂, éthanol produit : fermentation alcoolique", "mot": "la culture B كتدير la fermentation alcoolique"}],
         "parole": "la question un. le glucose consommé، plus élevé chez B، cinquante grammes par litre، que chez A، dix grammes par litre. les levures formées، plus élevé chez A، quatre virgule soixante-quinze grammes par litre، que chez B، un virgule vingt-cinq. l'éthanol كاين seulement dans la culture B، vingt-trois grammes par litre. إذن، la culture A كتدير la respiration: كتستهلك le dioxygène، وعندها des mitochondries développées. و la culture B كتدير la fermentation alcoolique: بلا dioxygène، وكتعطي l'éthanol."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Écrire la réaction globale (avec l'ATP) de la voie utilisée dans la culture A, puis de celle utilisée dans la culture B.",
       "texte_dit": "la question deux: كتب la réaction globale، مع l'ATP، ديال la voie ديال la culture A، ومن بعد ديال la culture B.",
       "reponse": {"type": "phrase", "attendu": "Culture A (respiration) : C₆H₁₂O₆ + 6 O₂ + 38 ADP + 38 Pi → 6 CO₂ + 6 H₂O + 38 ATP. Culture B (fermentation alcoolique) : C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CH₂-OH + 2 CO₂ + 2 ATP."},
       "clavier": {"aides": ["C₆H₁₂O₆", "O₂", "CO₂", "H₂O", "ADP + Pi", "ATP", "CH₃-CH₂-OH", "→"], "pieges": ["CH₃-CHOH-COOH", "CH₃-CHOH-OH", "NADH,H⁺"]},
       "aides": [
         {"texte": "Avec O₂, le glucose est dégradé complètement : en quelles molécules ? Sans O₂, chez la levure : quels produits ?",
          "dit": "مع le dioxygène، le glucose كيتحلل كامل: شنو كيعطي؟ وبلا dioxygène، عند la levure: شنو كيعطي؟"},
         {"texte": "Pour chaque ATP à droite, mets ADP + Pi à gauche (38 pour la respiration, 2 pour la fermentation). Vérifie les C, H et O.",
          "dit": "فكل ATP على اليمين، حط ADP و phosphate على اليسار. la respiration، trente-huit. la fermentation، deux. ومن بعد تأكد من les carbones، les hydrogènes، و les oxygènes."}],
       "correction": {"lignes": [
           {"texte": "2 : A : C₆H₁₂O₆ + 6 O₂ + 38 ADP + 38 Pi → 6 CO₂ + 6 H₂O + 38 ATP", "mot": "et trente-huit A T P"},
           {"texte": "B : C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CH₂-OH + 2 CO₂ + 2 ATP", "mot": "donne deux éthanol"}],
         "parole": "la question deux. la culture A، la respiration: glucose plus six O deux, plus trente-huit A D P et trente-huit phosphates, donne six C O deux, six H deux O, et trente-huit A T P. la culture B، la fermentation alcoolique: glucose plus deux A D P et deux phosphates, donne deux éthanol, deux C O deux, et deux A T P."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Calculer, pour chaque culture, la masse de levures formée par gramme de glucose consommé, puis le rapport de la valeur de A sur celle de B.",
       "texte_dit": "la question trois: حسب، لكل culture، la masse ديال les levures formées par gramme de glucose consommé. ومن بعد حسب le rapport: la valeur ديال A، على la valeur ديال B.",
       "reponse": {"type": "valeur", "grandeur": "rapport", "valeur": 19, "unite": "", "tolerance": 0.02,
                   "attendu": "A : 4,75/10 = 0,475 g/g ; B : 1,25/50 = 0,025 g/g ; rapport = 0,475/0,025 = 19"},
       "clavier": {"aides": ["levures formées / glucose consommé", "4,75/10", "1,25/50", "rapport = A/B"], "pieges": ["10/4,75", "4,75/1,25"]},
       "aides": [
         {"texte": "Pour chaque culture : masse de levures formées divisée par la masse de glucose consommé.",
          "dit": "لكل culture: les levures formées، مقسومين على le glucose consommé."},
         {"texte": "Puis divise le résultat de A par celui de B : combien de fois plus de levures A forme-t-elle avec le même glucose ?",
          "dit": "من بعد قسم la valeur ديال A على la valeur ديال B: شحال من مرة la culture A كتكون كثر ديال les levures، بنفس le glucose؟"}],
       "correction": {"lignes": [
           {"texte": "3 : A : 4,75/10 = 0,475 g de levures par g de glucose", "mot": "zéro virgule quatre cent soixante-quinze gramme"},
           {"texte": "B : 1,25/50 = 0,025 g de levures par g de glucose", "mot": "égale zéro virgule zéro vingt-cinq"},
           {"texte": "rapport = 0,475/0,025 = 19", "mot": "le rapport égale dix-neuf"}],
         "parole": "la question trois. la culture A: quatre virgule soixante-quinze sur dix، égale zéro virgule quatre cent soixante-quinze gramme de levures par gramme de glucose. la culture B: un virgule vingt-cinq sur cinquante، égale zéro virgule zéro vingt-cinq. le rapport: zéro virgule quatre cent soixante-quinze sur zéro virgule zéro vingt-cinq. donc le rapport égale dix-neuf. بنفس le glucose، la culture A كتكون، dix-neuf fois plus de levures."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Calculer le rendement énergétique r de la fermentation alcoolique.",
       "texte_dit": "la question quatre: حسب le rendement énergétique r ديال la fermentation alcoolique.",
       "reponse": {"type": "valeur", "grandeur": "r", "valeur": 2.13, "unite": "%", "tolerance": 0.02,
                   "attendu": "r = (2 × 30,5)/2860 × 100 = 61/2860 × 100 ≈ 2,13 %"},
       "clavier": {"aides": ["r = (énergie dans l'ATP)/(énergie du glucose) × 100", "2 × 30,5", "2860", "%"], "pieges": ["38 × 30,5", "2860/61"]},
       "aides": [
         {"texte": "Le rendement compare l'énergie mise dans l'ATP à l'énergie contenue dans une mole de glucose.",
          "dit": "le rendement كيقارن l'énergie اللي دخلات فl'ATP، مع l'énergie d'une mole de glucose."},
         {"texte": "Énergie dans l'ATP : nombre d'ATP de la fermentation × 30,5 kJ. Divise par 2860 kJ puis multiplie par 100.",
          "dit": "l'énergie فl'ATP: le nombre d'ATP ديال la fermentation، fois trente virgule cinq kilojoules. قسمها، sur deux mille huit cent soixante، ومن بعد fois cent."}],
       "correction": {"lignes": [
           {"texte": "4 : énergie dans l'ATP : 2 × 30,5 = 61 kJ", "mot": "deux fois trente virgule cinq"},
           {"texte": "r = 61/2860 × 100", "mot": "r égale soixante et un"},
           {"texte": "r ≈ 2,13 % (respiration : 40,5 %)", "mot": "environ deux virgule treize pour cent"}],
         "parole": "la question quatre. l'énergie فl'ATP: deux fois trente virgule cinq، égale soixante et un kilojoules. r égale soixante et un، sur deux mille huit cent soixante، fois cent. r égale environ deux virgule treize pour cent. أما la respiration، c'est quarante virgule cinq pour cent."},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "En vous appuyant sur les réponses précédentes, expliquer pourquoi la culture B consomme plus de glucose que la culture A, mais forme moins de levures.",
       "texte_dit": "la question cinq: اعتمد على الأجوبة اللي فاتو، وفسر علاش la culture B كتستهلك كثر ديال le glucose، ولكن كتكون قل ديال les levures.",
       "reponse": {"type": "phrase", "attendu": "Sans O₂, l'acide pyruvique n'entre pas dans la mitochondrie : la dégradation du glucose est incomplète, l'éthanol (résidu organique) garde une grande partie de l'énergie, et chaque glucose ne donne que 2 ATP, contre 38 par la respiration (dégradation complète en CO₂ et H₂O), soit 19 fois moins. La culture B doit donc dégrader beaucoup plus de glucose pour obtenir de l'ATP. Malgré cela, elle produit au total moins d'ATP que A (proportionnel à 50 × 2 = 100 pour B, contre 10 × 38 = 380 pour A) ; or la croissance des levures utilise l'énergie de l'ATP : B forme donc moins de levures."},
       "clavier": {"aides": ["dégradation incomplète", "résidu organique", "2 ATP", "38 ATP", "19 fois", "10 × 38", "50 × 2"], "pieges": ["la fermentation produit plus d'énergie", "B consomme moins de glucose"]},
       "aides": [
         {"texte": "Compare le nombre d'ATP produits par glucose dans chaque voie, et ce que devient l'énergie qui n'est pas mise dans l'ATP.",
          "dit": "قارن le nombre d'ATP par glucose فكل voie، وفين كتمشي l'énergie اللي ما دخلاتش فl'ATP."},
         {"texte": "La quantité totale d'ATP est proportionnelle à (glucose consommé) × (ATP par glucose). Calcule-la pour A et pour B, puis relie l'ATP à la croissance des levures.",
          "dit": "l'ATP total كيتناسب مع le glucose consommé، fois le nombre d'ATP par glucose. حسبو لA ولB، ومن بعد ربط l'ATP مع la croissance ديال les levures."}],
       "correction": {"lignes": [
           {"texte": "5 : B (fermentation) : dégradation incomplète, l'éthanol garde de l'énergie : 2 ATP par glucose", "mot": "dégradation incomplète"},
           {"texte": "A (respiration) : dégradation complète : 38 ATP par glucose, 19 fois plus", "mot": "dégradation complète"},
           {"texte": "B doit dégrader beaucoup de glucose pour obtenir de l'ATP", "mot": "خاصها تستهلك بزاف ديال le glucose"},
           {"texte": "ATP total : A ∝ 10 × 38 = 380 ; B ∝ 50 × 2 = 100 : moins d'ATP, donc moins de levures", "mot": "égale trois cent quatre-vingts"}],
         "parole": "la question cinq. فla culture B، la fermentation، c'est une dégradation incomplète. l'éthanol كيبقى فيه بزاف ديال l'énergie، و chaque glucose donne seulement deux ATP. فla culture A، la respiration، c'est une dégradation complète: trente-huit ATP، dix-neuf fois plus. إذن la culture B خاصها تستهلك بزاف ديال le glucose باش تلقى l'ATP. ولكن l'ATP total ديالها قليل: cinquante fois deux، égale cent. أما la culture A: dix fois trente-huit، égale trois cent quatre-vingts. و les levures كيكبرو بl'énergie ديال l'ATP. إذن la culture B كتكون قل ديال les levures."},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : avec ou sans dioxygène, le même glucose",
     "screen_content": {"lead": "Avec O₂ : respiration, l'acide pyruvique entre dans la mitochondrie. Sans O₂ : fermentation, il reste dans le hyaloplasme."},
     "visual": {"kind": "simulation", "url": COMP, "caption": "Le même glucose, avec puis sans dioxygène"},
     "speech_text": {"mixed": "شوف هاد la simulation: نفس le glucose، مع le dioxygène وبلا بيه. مع le dioxygène، l'acide pyruvique كيدخل للmitochondrie. le carbone كامل كيخرج C O deux، مع l'eau: هادي la respiration. دابا نحيدو le dioxygène. l'acide pyruvique كيبقى فle hyaloplasme، و la mitochondrie واقفة. كيبقى un résidu organique: l'acide lactique، ولا l'éthanol عند la levure. هادي la fermentation. رجع للtableau ديال l'exercice. la culture A عندها le dioxygène، و des mitochondries développées: la respiration. la culture B ما عندهاش le dioxygène، و فيها l'éthanol: la fermentation alcoolique."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "A : O₂ consommé, mitochondries développées, pas d'éthanol : respiration", "mot": "la culture A عندها le dioxygène"},
                  {"texte": "B : glucose 50 g/L contre 10 g/L, levures 1,25 contre 4,75 g/L, éthanol 23 g/L : fermentation alcoolique", "mot": "la culture B ما عندهاش le dioxygène"}],
       "pointage": [{"mot": "مع le dioxygène، l'acide pyruvique", "commande": "play_until", "parametres": {"moment": "mitochondrie"}},
                    {"mot": "le carbone كامل", "commande": "play_until", "parametres": {"moment": "mineraux", "duree_s": 2.4}},
                    {"mot": "هادي la respiration.", "repere": "mineraux"},
                    {"mot": "دابا نحيدو le dioxygène", "commande": "set_parameters", "parametres": {"o2": False}},
                    {"mot": "l'acide pyruvique كيبقى", "commande": "play_until", "parametres": {"moment": "deux_atp", "duree_s": 1.6}},
                    {"mot": "كيبقى un résidu organique", "commande": "play_until", "parametres": {"moment": "residu", "duree_s": 1.6}},
                    {"mot": "ولا l'éthanol عند la levure", "repere": "residu"},
                    {"mot": "رجع للtableau", "repere": "comparaison"},
                    {"mot": "la culture A عندها le dioxygène", "cible": "centre:0"},
                    {"mot": "la culture B ما عندهاش le dioxygène", "cible": "centre:1"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : les deux réactions globales",
     "screen_content": {"lead": "Respiration : 6 CO₂ + 6 H₂O + 38 ATP. Fermentation alcoolique : 2 éthanol + 2 CO₂ + 2 ATP."},
     "visual": {"kind": "simulation", "url": CARR, "caption": "Le carrefour de l'acide pyruvique"},
     "speech_text": {"mixed": "شوف l'acide pyruvique فle carrefour. مع le dioxygène، كيدخل للmitochondrie: la matrice، ومن بعد la chaîne respiratoire. le bilan: six C O deux، six H deux O، et trente-huit ATP. كنكتبو: glucose plus six O deux, plus trente-huit A D P et trente-huit phosphates, donne six C O deux, six H deux O, et trente-huit A T P. بلا dioxygène، كيبقى فle hyaloplasme. عند la levure، le bilan: deux éthanol، deux C O deux، et deux ATP. كنكتبو: glucose plus deux A D P et deux phosphates, donne deux éthanol, deux C O deux, et deux A T P. ردو البال: l'éthanol هو C H trois, C H deux, O H."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "C₆H₁₂O₆ + 6 O₂ + 38 ADP + 38 Pi → 6 CO₂ + 6 H₂O + 38 ATP", "mot": "كنكتبو: glucose plus six O deux"},
                  {"texte": "C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CH₂-OH + 2 CO₂ + 2 ATP", "mot": "كنكتبو: glucose plus deux A D P"}],
       "pointage": [{"mot": "شوف l'acide pyruvique فle carrefour", "commande": "play_until", "parametres": {"moment": "carrefour", "duree_s": 2.4}},
                    {"mot": "مع le dioxygène، كيدخل للmitochondrie", "commande": "play_until", "parametres": {"moment": "avec_o2_vers_matrice", "duree_s": 2.4}},
                    {"mot": "la matrice، ومن بعد", "commande": "play_until", "parametres": {"moment": "matrice_krebs"}},
                    {"mot": "ومن بعد la chaîne respiratoire", "commande": "play_until", "parametres": {"moment": "chaine_respiratoire"}},
                    {"mot": "le bilan: six C O deux", "commande": "play_until", "parametres": {"moment": "bilan_38"}},
                    {"mot": "كنكتبو: glucose plus six O deux", "cible": "centre:0"},
                    {"mot": "بلا dioxygène، كيبقى فle hyaloplasme", "commande": "play_until", "parametres": {"moment": "sans_o2_sur_place", "duree_s": 2}},
                    {"mot": "عند la levure، le bilan", "commande": "play_until", "parametres": {"moment": "bilan_2"}},
                    {"mot": "كنكتبو: glucose plus deux A D P", "cible": "centre:1"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : dix-neuf fois plus de levures, dix-neuf fois plus d'ATP",
     "screen_content": {"lead": "0,475 / 0,025 = 19 : c'est aussi 38 ATP / 2 ATP."},
     "visual": {"kind": "simulation", "url": COMP, "caption": "Les ATP d'un glucose, avec puis sans dioxygène"},
     "speech_text": {"mixed": "pourquoi dix-neuf ؟ شوف: مع le dioxygène، un glucose donne trente-huit ATP. دابا بلا dioxygène. شوف le compteur: seulement deux ATP. trente-huit sur deux، égale dix-neuf. شوف شنو تكتب فle tableau: مع le dioxygène، dix-neuf fois plus d'ATP. وفl'exercice، le rapport ديال les levures حتى هو، dix-neuf. les levures كيكبرو بl'énergie ديال l'ATP."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "A : 4,75/10 = 0,475 g/g ; B : 1,25/50 = 0,025 g/g", "mot": "وفl'exercice، le rapport"},
                  {"texte": "rapport = 0,475/0,025 = 19 = 38/2", "mot": "les levures كيكبرو بl'énergie"}],
       "pointage": [{"mot": "مع le dioxygène، un glucose donne", "commande": "play_until", "parametres": {"moment": "mineraux", "duree_s": 3}},
                    {"mot": "trente-huit ATP. دابا", "repere": "resp_atp"},
                    {"mot": "دابا بلا dioxygène", "commande": "set_parameters", "parametres": {"o2": False}},
                    {"mot": "شوف le compteur", "commande": "play_until", "parametres": {"moment": "deux_atp", "duree_s": 2}},
                    {"mot": "seulement deux ATP", "repere": "ferm_atp"},
                    {"mot": "شوف شنو تكتب فle tableau", "repere": "comparaison"},
                    {"mot": "وفl'exercice، le rapport", "cible": "centre:0"},
                    {"mot": "les levures كيكبرو بl'énergie", "cible": "centre:1"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : le rendement de la fermentation",
     "screen_content": {"lead": "2 briques d'ATP de 30,5 kJ sur les 2860 kJ du glucose : r ≈ 2,13 %."},
     "visual": {"kind": "simulation", "url": REND, "caption": "L'énergie du glucose et les briques d'ATP"},
     "speech_text": {"mixed": "هاد la barre هي l'énergie d'une mole de glucose: deux mille huit cent soixante kilojoules. avec la respiration، trente-huit ATP، le rendement est de quarante virgule cinq pour cent. دابا la fermentation: deux briques، deux ATP، c'est-à-dire soixante et un kilojoules. r égale deux fois trente virgule cinq، sur deux mille huit cent soixante، fois cent: deux virgule treize pour cent. والباقي؟ كيبقى فl'éthanol: un résidu organique، l'énergie ما تحررتش."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "r = (2 × 30,5)/2860 × 100 = 61/2860 × 100 ≈ 2,13 %", "mot": "deux virgule treize pour cent"}],
       "pointage": [{"mot": "هاد la barre", "commande": "play_until", "parametres": {"moment": "barre_glucose", "duree_s": 2.4}},
                    {"mot": "avec la respiration", "commande": "play_until", "parametres": {"moment": "resultat", "duree_s": 3}},
                    {"mot": "دابا la fermentation", "commande": "play_until", "parametres": {"moment": "briques_fermentation", "duree_s": 2.4}},
                    {"mot": "deux virgule treize pour cent", "cible": "centre:0"},
                    {"mot": "والباقي؟", "commande": "play_until", "parametres": {"moment": "residu_organique", "duree_s": 2}},
                    {"mot": "un résidu organique", "repere": "residu"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : peu d'ATP par glucose, donc beaucoup de glucose et peu de levures",
     "screen_content": {"lead": "Fermentation : dégradation incomplète, l'éthanol garde l'énergie, 2 ATP seulement."},
     "visual": {"kind": "simulation", "url": FERM, "caption": "La fermentation alcoolique chez la levure"},
     "speech_text": {"mixed": "شوف عند la levure بلا dioxygène. l'acide pyruvique كيخرج منو C O deux، ومن بعد كيولي l'éthanol. l'éthanol باقي فيه les carbones، يعني باقي فيه l'énergie: هادي dégradation incomplète. وشحال ديال l'ATP؟ seulement deux، ديال la glycolyse. إذن باش تلقى l'ATP، la levure خاصها تستهلك بزاف ديال le glucose. وحيت l'ATP قليل، les levures كيكبرو بشوية."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "ATP total : A ∝ 10 × 38 = 380 ; B ∝ 50 × 2 = 100", "mot": "خاصها تستهلك بزاف"},
                  {"texte": "380/100 = 3,8 = 4,75/1,25 : les levures formées suivent l'ATP", "mot": "les levures كيكبرو بشوية"}],
       "pointage": [{"mot": "كيخرج منو C O deux", "commande": "play_until", "parametres": {"moment": "co2_part", "duree_s": 1.6}},
                    {"mot": "ومن بعد كيولي l'éthanol", "commande": "play_until", "parametres": {"moment": "ethanol", "duree_s": 2.4}},
                    {"mot": "هادي dégradation incomplète", "commande": "play_until", "parametres": {"moment": "degradation_incomplete"}},
                    {"mot": "وشحال ديال l'ATP؟", "commande": "play_until", "parametres": {"moment": "deux_atp", "duree_s": 2}},
                    {"mot": "خاصها تستهلك بزاف", "cible": "centre:0"},
                    {"mot": "les levures كيكبرو بشوية", "cible": "centre:1"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : quelle voie dans la culture B ?", "سؤال ساهل على la culture B.",
      "Dans la culture B (sans O₂, éthanol produit), les levures font…", ["la fermentation alcoolique", "la respiration", "la fermentation lactique"], 0, {
        "0": {"juste": rep("برافو! بلا dioxygène، وكاين l'éthanol: la fermentation alcoolique.", "Juste : sans O₂, avec production d'éthanol : fermentation alcoolique.")},
        "1": {"1": rep("ما تقلقش. la respiration كتحتاج le dioxygène. واش كاين le dioxygène فla culture B؟ عاود اختار.", "La respiration a besoin de dioxygène. Y en a-t-il dans la culture B ? Réessaie."),
              "2": rep("الجواب هو la fermentation alcoolique. la culture B بلا dioxygène، وفيها l'éthanol.", "Réponse : la fermentation alcoolique (pas d'O₂, éthanol produit).")},
        "2": {"1": rep("قريب! هي fermentation، ولكن شنو كتعطي la culture B: l'acide lactique ولا l'éthanol؟ عاود اختار.", "C'est bien une fermentation. Mais la culture B produit-elle de l'acide lactique ou de l'éthanol ? Réessaie."),
              "2": rep("الجواب هو la fermentation alcoolique، حيت كتعطي l'éthanol. la fermentation lactique كتعطي l'acide lactique، و les levures ما كيديروهاش.", "Réponse : la fermentation alcoolique (éthanol). La fermentation lactique donne de l'acide lactique.")}},
      "Dans la culture B, sans dioxygène et avec de l'éthanol, les levures font quelle réaction ?"),
    association("fa_s2", "Plus facile : chaque voie et sa réaction globale", "Relie chaque voie à sa réaction globale.",
      "سؤال ساهل: ربط كل voie مع la réaction globale ديالها.", "Relie chaque voie à sa réaction globale.",
      [("1", "Respiration (culture A)"), ("2", "Fermentation alcoolique (culture B)")],
      [("a", "C₆H₁₂O₆ + 6 O₂ + 38 ADP + 38 Pi → 6 CO₂ + 6 H₂O + 38 ATP"), ("b", "C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CH₂-OH + 2 CO₂ + 2 ATP"),
       ("c", "C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP")],
      {"1": "a", "2": "b"},
      {"1-a": (True, "Oui : dioxygène consommé, CO₂ et H₂O, 38 ATP : la respiration.", "برافو: le dioxygène، C O deux و H deux O، trente-huit ATP: la respiration."),
       "1-b": (False, "Non : sans O₂ et avec éthanol, c'est une fermentation. Cherche la réaction qui consomme O₂.", "لا، هادي بلا dioxygène، وفيها l'éthanol. قلب على la réaction اللي فيها le dioxygène."),
       "1-c": (False, "Non : l'acide lactique, c'est la fermentation lactique. La respiration consomme O₂.", "لا، l'acide lactique ديال la fermentation lactique. la respiration فيها le dioxygène."),
       "2-a": (False, "Non : cette réaction consomme O₂ et donne 38 ATP : c'est la respiration.", "لا، هادي فيها le dioxygène، et trente-huit ATP: هادي la respiration."),
       "2-b": (True, "Oui : éthanol (CH₃-CH₂-OH) et CO₂, 2 ATP : la fermentation alcoolique.", "برافو: l'éthanol، و C O deux، et deux ATP: la fermentation alcoolique."),
       "2-c": (False, "Non : CH₃-CHOH-COOH est l'acide lactique, sans CO₂ : fermentation lactique. Cherche l'éthanol.", "لا، هادا l'acide lactique، بلا C O deux. قلب على l'éthanol.")},
      ("Respiration : 6 CO₂ + 6 H₂O + 38 ATP. Fermentation alcoolique : 2 éthanol + 2 CO₂ + 2 ATP.",
       "la respiration: six C O deux، six H deux O، et trente-huit ATP. la fermentation alcoolique: deux éthanol، deux C O deux، et deux ATP.")),
    qcm_facile("fa_s3", "Plus facile : levures par gramme de glucose", "سؤال ساهل: la masse ديال les levures par gramme de glucose فla culture A.",
      "Dans la culture A, la masse de levures formée par gramme de glucose consommé est…", ["4,75/10 = 0,475 g/g", "10/4,75 ≈ 2,1 g/g", "4,75 × 10 = 47,5 g/g"], 0, {
        "0": {"juste": rep("برافو! les levures formées، على le glucose consommé: zéro virgule quatre cent soixante-quinze gramme par gramme.", "Juste : 4,75/10 = 0,475 g de levures par g de glucose.")},
        "1": {"1": rep("ما تقلقش. par gramme de glucose، يعني le glucose هو اللي كيكون تحت. عاود اختار.", "« Par gramme de glucose » : le glucose est au dénominateur. Réessaie."),
              "2": rep("الجواب: quatre virgule soixante-quinze sur dix. قلبتي القسمة.", "Réponse : 4,75/10 = 0,475 g/g ; ta fraction est inversée.")},
        "2": {"1": rep("قريب! ولكن par gramme كيعني قسمة، ماشي ضرب. عاود اختار.", "« Par gramme » veut dire une division, pas une multiplication. Réessaie."),
              "2": rep("الجواب: quatre virgule soixante-quinze sur dix، égale zéro virgule quatre cent soixante-quinze.", "Réponse : 4,75/10 = 0,475 g/g.")}},
      "Dans la culture A, la masse de levures formée par gramme de glucose consommé est ?"),
    qcm_facile("fa_s4", "Plus facile : la relation du rendement", "سؤال ساهل: اختار la relation ديال le rendement ديال la fermentation.",
      "Le rendement de la fermentation alcoolique s'écrit…", ["r = (2 × 30,5)/2860 × 100", "r = (38 × 30,5)/2860 × 100", "r = (2 × 30,5)/2860"], 0, {
        "0": {"juste": rep("برافو! deux fois trente virgule cinq، sur deux mille huit cent soixante، fois cent: environ deux virgule treize pour cent.", "Juste : r = (2 × 30,5)/2860 × 100 ≈ 2,13 %.")},
        "1": {"1": rep("ما تقلقش. trente-huit ATP هوما ديال la respiration. la fermentation كتعطي شحال؟ عاود اختار.", "38 ATP, c'est la respiration. Combien d'ATP pour la fermentation ? Réessaie."),
              "2": rep("الجواب: deux fois trente virgule cinq، sur deux mille huit cent soixante، fois cent. la fermentation: deux ATP.", "Réponse : r = (2 × 30,5)/2860 × 100 ; la fermentation donne 2 ATP.")},
        "2": {"1": rep("قريب! ولكن le rendement كيتعطى بالpourcentage. شنو ناقص؟ عاود اختار.", "Presque : le rendement se donne en pourcentage. Que manque-t-il ? Réessaie."),
              "2": rep("الجواب هو r égale deux fois trente virgule cinq، sur deux mille huit cent soixante، fois cent. نسيتي fois cent.", "Réponse : r = (2 × 30,5)/2860 × 100 ; tu as oublié le × 100.")}},
      "Le rendement de la fermentation alcoolique s'écrit ?"),
    vrai_faux("fa_s5", "Plus facile : vrai ou faux sur les bilans", "Vrai ou faux ?", "نتمرنو بvrai ou faux على les bilans.", [
      ("Dans la fermentation, l'éthanol garde une partie de l'énergie du glucose.", True, "Vrai : l'éthanol est un résidu organique ; la dégradation du glucose est incomplète."),
      ("La fermentation produit 2 ATP en plus des 2 ATP de la glycolyse.", False, "Faux : les 2 ATP de la fermentation sont ceux de la glycolyse."),
      ("Pour obtenir autant d'ATP, une levure qui fermente doit dégrader 19 fois plus de glucose qu'une levure qui respire.", True, "Vrai : 38/2 = 19."),
      ("La culture B forme moins de levures parce qu'elle consomme moins de glucose.", False, "Faux : elle consomme plus de glucose (50 g/L contre 10 g/L), mais elle en tire peu d'ATP.")])
  ]}]},
  "similaire": {
    "id": "svt_ex_ch1_fermentations_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même expérience avec une autre culture de la même souche, pendant 36 h. Le document 1 donne les résultats pour 1 L. On prend ici 2870 kJ pour l'énergie d'une mole de glucose.",
      "intro_dit": "نفس l'expérience، بقيم أخرى، pendant trente-six heures. les résultats فle document un. وهنا l'énergie d'une mole de glucose: deux mille huit cent soixante-dix kilojoules.",
      "figures": [doc1(12, 60, 5.7, 1.5, 28)],
      "donnees": ["Culture A (aérée) : glucose consommé 12 g/L ; levures formées 5,7 g/L ; éthanol 0 g/L",
                  "Culture B (sans O₂) : glucose consommé 60 g/L ; levures formées 1,5 g/L ; éthanol 28 g/L",
                  "Une mole d'ATP : 30,5 kJ ; une mole de glucose : 2870 kJ ; respiration : 38 ATP ; fermentation : 2 ATP"],
      "questions": [
        {"id": "1", "texte": "Comparer les résultats des cultures A et B, puis déduire la voie métabolique de chaque culture. Justifier.",
         "reponse": {"type": "phrase", "attendu": "Glucose consommé plus élevé chez B (60 g/L) que chez A (12 g/L) ; levures formées plus élevées chez A (5,7 g/L) que chez B (1,5 g/L) ; éthanol seulement chez B (28 g/L). Donc A fait la respiration (O₂ consommé, mitochondries développées) et B la fermentation alcoolique (sans O₂, éthanol)."},
         "clavier": {"aides": ["plus élevé chez … que chez …", "respiration", "fermentation alcoolique"], "pieges": ["fermentation lactique"]},
         "correction": {"lignes": [{"texte": "1 : glucose : B (60 g/L) > A (12 g/L) ; levures : A (5,7 g/L) > B (1,5 g/L) ; éthanol : B seulement (28 g/L)", "mot": "plus élevé chez B"},
                                   {"texte": "A : respiration ; B : fermentation alcoolique", "mot": "la fermentation alcoolique"}],
                        "parole": "le glucose consommé، plus élevé chez B، soixante grammes par litre، que chez A، douze. les levures، plus élevé chez A، cinq virgule sept، que chez B، un virgule cinq. l'éthanol seulement chez B. إذن A، la respiration، و B، la fermentation alcoolique."}},
        {"id": "2", "texte": "Écrire la réaction globale (avec l'ATP) de la voie de A, puis de celle de B.",
         "reponse": {"type": "phrase", "attendu": "A : C₆H₁₂O₆ + 6 O₂ + 38 ADP + 38 Pi → 6 CO₂ + 6 H₂O + 38 ATP. B : C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CH₂-OH + 2 CO₂ + 2 ATP."},
         "clavier": {"aides": ["C₆H₁₂O₆", "ADP + Pi", "CH₃-CH₂-OH", "→"], "pieges": ["CH₃-CHOH-COOH"]},
         "correction": {"lignes": [{"texte": "2 : A : C₆H₁₂O₆ + 6 O₂ + 38 ADP + 38 Pi → 6 CO₂ + 6 H₂O + 38 ATP", "mot": "trente-huit A T P"},
                                   {"texte": "B : C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CH₂-OH + 2 CO₂ + 2 ATP", "mot": "deux éthanol"}],
                        "parole": "A: glucose plus six O deux, plus trente-huit A D P et trente-huit phosphates, donne six C O deux, six H deux O, et trente-huit A T P. B: glucose plus deux A D P et deux phosphates, donne deux éthanol, deux C O deux, et deux A T P."}},
        {"id": "3", "texte": "Calculer, pour chaque culture, la masse de levures formée par gramme de glucose consommé, puis le rapport A/B.",
         "reponse": {"type": "valeur", "grandeur": "rapport", "valeur": 19, "unite": "", "tolerance": 0.02, "attendu": "A : 5,7/12 = 0,475 g/g ; B : 1,5/60 = 0,025 g/g ; rapport = 0,475/0,025 = 19"},
         "clavier": {"aides": ["5,7/12", "1,5/60", "rapport = A/B"], "pieges": ["12/5,7"]},
         "correction": {"lignes": [{"texte": "3 : A : 5,7/12 = 0,475 g/g ; B : 1,5/60 = 0,025 g/g", "mot": "cinq virgule sept sur douze"},
                                   {"texte": "rapport = 0,475/0,025 = 19", "mot": "le rapport égale dix-neuf"}],
                        "parole": "A: cinq virgule sept sur douze، égale zéro virgule quatre cent soixante-quinze. B: un virgule cinq sur soixante، égale zéro virgule zéro vingt-cinq. donc le rapport égale dix-neuf."}},
        {"id": "4", "texte": "Calculer le rendement énergétique r de la fermentation alcoolique (2870 kJ par mole de glucose).",
         "reponse": {"type": "valeur", "grandeur": "r", "valeur": 2.13, "unite": "%", "tolerance": 0.02, "attendu": "r = (2 × 30,5)/2870 × 100 = 61/2870 × 100 ≈ 2,13 %"},
         "clavier": {"aides": ["2 × 30,5", "2870", "× 100", "%"], "pieges": ["38 × 30,5"]},
         "correction": {"lignes": [{"texte": "4 : 2 × 30,5 = 61 kJ", "mot": "deux fois trente virgule cinq"}, {"texte": "r = 61/2870 × 100 ≈ 2,13 %", "mot": "deux virgule treize pour cent"}],
                        "parole": "deux fois trente virgule cinq، égale soixante et un kilojoules. r égale soixante et un، sur deux mille huit cent soixante-dix، fois cent، environ deux virgule treize pour cent."}},
        {"id": "5", "texte": "Expliquer pourquoi la culture B consomme plus de glucose que la culture A, mais forme moins de levures.",
         "reponse": {"type": "phrase", "attendu": "Fermentation : dégradation incomplète (l'éthanol garde de l'énergie), 2 ATP par glucose contre 38 pour la respiration. B doit dégrader beaucoup de glucose, mais produit au total moins d'ATP (∝ 60 × 2 = 120) que A (∝ 12 × 38 = 456) ; la croissance utilise l'ATP, donc B forme moins de levures."},
         "clavier": {"aides": ["dégradation incomplète", "2 ATP", "38 ATP", "12 × 38", "60 × 2"], "pieges": ["B consomme moins de glucose"]},
         "correction": {"lignes": [{"texte": "5 : fermentation : dégradation incomplète, 2 ATP par glucose (respiration : 38)", "mot": "dégradation incomplète"},
                                   {"texte": "ATP total : A ∝ 12 × 38 = 456 ; B ∝ 60 × 2 = 120 : moins d'ATP, moins de levures", "mot": "égale cent vingt"}],
                        "parole": "la fermentation، c'est une dégradation incomplète: seulement deux ATP par glucose، contre trente-huit. l'ATP total ديال B: soixante fois deux، égale cent vingt. ديال A: douze fois trente-huit، égale quatre cent cinquante-six. قل ديال l'ATP، إذن قل ديال les levures."}}
      ]}}
}
ecrire(EX, sys.argv[1])
