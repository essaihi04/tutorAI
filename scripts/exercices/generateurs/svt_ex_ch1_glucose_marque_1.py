# Exercice SVT ch. 1 (libération de l'énergie), niveau moyen : suivre le carbone 14 du glucose dans la cellule.
# Ce qu'il entraîne : « décrire… puis déduire » sur trois courbes (une ligne par compartiment, valeurs lues), nommer la
# glycolyse et écrire sa réaction globale (2017 N), expliquer l'origine du CO2 (décarboxylations, pas le dioxygène),
# compter les CO2 par glucose (× 2), définir glycolyse et cycle de Krebs (nature + lieu + produits ; 2020 R, 2023 R).
# Sources comparées (lecture seulement, rien de copié) :
# - exploration du cours : cas_types « definition », « equation » ; pièges « oublie le × 2 », « le CO2 vient du dioxygène »,
#   erreurs_examen « réaction globale de la glycolyse » (oubli de 2 NAD+ et 2 ADP + 2 Pi) ; a_ne_pas_dire (C3H6O3, CO2 + O2) ;
# - diapositive du cours le_m3a_glucose_marque (glucose-marque.html, tableau T0 → T4 en « + ») : notre document est différent
#   (courbes de radioactivité en %, temps en minutes, liste des molécules identifiées) ;
# - nationaux 2017 N (réaction globale de la glycolyse), 2020 R (définition du cycle de Krebs), 2023 R (définition de la
#   glycolyse), 2021 N (acide pyruvique → acétyl-CoA) : formes des questions et barème ; aucun national n'a de glucose ¹⁴C ;
# - séries en ligne (recherche du 22/11/2026, extraits seulement : dyrassa, moutamadris, ayoubsvt ; sites bloqués par le
#   réseau) : expérience classique « glucose marqué au 14C : pyruvate, acides du cycle de Krebs, CO2 ».
# Pas de recouvrement : le comptage des ATP / NADH,H+ et le rendement sont dans svt_ex_ch1_bilan_energetique_1 (autre agent).
import sys, math
sys.path.insert(0, __import__("os").path.dirname(__file__))
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

D = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/"
GM = D + "glucose-marque.html?depart=0"
GLY = D + "glycolyse.html?depart=0"
PYR = D + "pyruvate.html?depart=0"
KREBS = D + "krebs.html?depart=0"


def courbes(ph, th, pm, t0m, tm, pc, t0c, tauc, titre):
    """Radioactivité (% de la radioactivité introduite) : hyaloplasme (pic ph à th), matrice (départ t0m, pic pm à tm),
    CO2 du milieu (départ t0c, vers pc). Renvoie la figure et les fonctions (pour vérifier les valeurs lues)."""
    fh = lambda x: ph * (x / th) * math.exp(1 - x / th)
    dm = tm - t0m
    fm = lambda x: pm * ((x - t0m) / dm) * math.exp(1 - (x - t0m) / dm) if x >= t0m else 0
    fc = lambda x: pc * (1 - math.exp(-(x - t0c) / tauc)) if x >= t0c else 0
    assert max(fh(x / 10) + fm(x / 10) + fc(x / 10) for x in range(301)) < 100
    fig = {"type": "courbe", "titre": titre,
           "axes": {"x": {"min": 0, "max": 30, "nom": "t", "unite": "min", "graduations": sorted({0, 5, 10, 15, 20, 25, 30, th, t0m, tm, t0c})},
                    "y": {"min": 0, "max": 100, "nom": "radioactivité", "unite": "%", "graduations": list(range(0, 101, 10))}},
           "legende": "Radioactivité de chaque compartiment, en % de la radioactivité du glucose introduit à t = 0.",
           "elements": [
             {"f": "courbe", "expr": f"{ph}*(x/{th})*exp(1-x/{th})", "de": 0, "a": 30, "couleur": "vert", "texte": "hyaloplasme", "texte_x": th, "pos": "n"},
             {"f": "courbe", "expr": f"{pm}*((x-{t0m})/{dm})*exp(1-(x-{t0m})/{dm})", "de": t0m, "a": 30, "couleur": "rouge", "texte": "matrice", "texte_x": tm + 4, "pos": "ne"},
             {"f": "courbe", "expr": "0", "de": 0, "a": t0m, "couleur": "rouge"},
             {"f": "courbe", "expr": f"{pc}*(1-exp(-(x-{t0c})/{tauc}))", "de": t0c, "a": 30, "couleur": "cyan", "texte": "CO₂ du milieu", "texte_x": 27, "pos": "n"},
             {"f": "repere", "x": th, "y": ph}, {"f": "repere", "x": tm, "y": pm}]}
    return fig, fh, fm, fc


FIG1, fh, fm, fc = courbes(60, 5, 45, 3, 12, 50, 8, 12, "Document 1 : radioactivité des compartiments")
assert round(fh(30)) == 2 and round(fm(30)) == 18 and round(fc(30)) == 42
FIGS, gh, gm, gc = courbes(55, 4, 40, 2, 10, 45, 6, 12, "Document 1 : radioactivité des compartiments")
assert round(gh(30)) == 1 and round(gm(30)) == 11 and round(gc(30)) == 39
N_CO2 = 2 * (1 + 2)   # par glucose : 2 acides pyruviques × (1 CO2 à l'acétyl-CoA + 2 CO2 par tour du cycle)

EX = {
  "id": "svt_ex_ch1_glucose_marque_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "reactions_responsables_liberation_energie", "cours": "svt_ch1_reactions_responsables_liberation_energie",
  "titre": "Suivre les carbones du glucose marqué au ¹⁴C", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Décrire des courbes puis déduire", "Écrire la réaction globale de la glycolyse", "Expliquer l'origine du CO₂ respiratoire", "Définir glycolyse et cycle de Krebs"],
  "enonce": {
    "intro": "Des cellules de foie sont placées dans un milieu riche en dioxygène. À t = 0, on ajoute du glucose dont les six carbones sont radioactifs (carbone 14, ¹⁴C). On mesure ensuite la radioactivité du hyaloplasme, de la matrice des mitochondries et du CO₂ rejeté dans le milieu (document 1). On identifie aussi les molécules radioactives à différents instants (document 2).",
    "intro_dit": "دابا نقراو l'énoncé. حطينا des cellules ديال le foie فmilieu فيه بزاف ديال le dioxygène. à t égale zéro، زدنا le glucose، و les six carbones ديالو radioactifs: le carbone quatorze. من بعد، قسنا la radioactivité فle hyaloplasme، فla matrice ديال les mitochondries، وفle C O deux اللي خرج للmilieu: هادا le document un. وعرفنا حتى شمن molécules radioactives كاينين فكل وقت: هادا le document deux.",
    "figures": [FIG1],
    "donnees": ["Document 2 : molécules radioactives identifiées",
                "à t = 1 min : glucose ¹⁴C dans le hyaloplasme",
                "à t = 5 min : acide pyruvique ¹⁴C (CH₃-CO-COOH) dans le hyaloplasme",
                "à t = 12 min : acide pyruvique, acétyl-CoA et composés du cycle de Krebs ¹⁴C dans la matrice",
                "à t = 20 min : CO₂ ¹⁴C dans la matrice et dans le milieu",
                "Un tour du cycle de Krebs libère 2 CO₂"],
    "questions": [
      {"id": "1", "texte": "Décrire l'évolution de la radioactivité du hyaloplasme, de la matrice et du CO₂ du milieu (document 1), puis déduire le trajet des carbones du glucose dans la cellule.",
       "texte_dit": "السؤال un: وصف l'évolution ديال la radioactivité فle hyaloplasme، فla matrice، وفle C O deux ديال le milieu، فle document un. ومن بعد استنتج الطريق اللي داوها les carbones ديال le glucose فla cellule.",
       "reponse": {"type": "phrase", "attendu": "Hyaloplasme : la radioactivité augmente dès le début, jusqu'à 60 % à 5 min, puis diminue jusqu'à environ 2 % à 30 min. Matrice : nulle avant 3 min, elle augmente jusqu'à 45 % à 12 min, puis diminue jusqu'à environ 18 % à 30 min. CO₂ du milieu : nulle avant 8 min, elle augmente ensuite jusqu'à environ 42 % à 30 min. On en déduit que les carbones du glucose passent d'abord dans le hyaloplasme, puis dans la matrice des mitochondries, et sortent enfin sous forme de CO₂."},
       "clavier": {"aides": ["augmente", "diminue", "nulle avant", "60 % à 5 min", "45 % à 12 min", "On en déduit que", "puis"], "pieges": ["d'abord dans la matrice", "reste constante"]},
       "aides": [
         {"texte": "Prends les courbes une par une, dans l'ordre où elles démarrent : quand la radioactivité apparaît, quand elle est maximale (valeur), ce qu'elle devient à 30 min.",
          "dit": "خود les courbes وحدة بوحدة، بالترتيب اللي كيبداو بيه. قول فوقاش كتبان la radioactivité، فوقاش كتوصل للmaximum مع la valeur، وشنو كتولي à trente minutes."},
         {"texte": "Écris une ligne par compartiment (« augmente jusqu'à … % à … min, puis diminue… »), puis une phrase qui commence par « On en déduit que » avec l'ordre des compartiments.",
          "dit": "كتب ligne لكل compartiment، بحال: augmente jusqu'à، ومن بعد diminue. ومن بعد جملة كتبدا ب on en déduit que، فيها الترتيب ديال les compartiments."}],
       "correction": {"lignes": [
           {"texte": "1 : hyaloplasme : augmente jusqu'à 60 % à 5 min, puis diminue (≈ 2 % à 30 min)", "mot": "soixante pour cent à cinq minutes"},
           {"texte": "matrice : nulle avant 3 min, augmente jusqu'à 45 % à 12 min, puis diminue (≈ 18 % à 30 min)", "mot": "quarante-cinq pour cent à douze minutes"},
           {"texte": "CO₂ du milieu : nulle avant 8 min, puis augmente (≈ 42 % à 30 min)", "mot": "quarante-deux pour cent"},
           {"texte": "On en déduit que les carbones passent : hyaloplasme → matrice → CO₂", "mot": "on en déduit que"}],
         "parole": "السؤال un. فle hyaloplasme، la radioactivité كتطلع من البداية، jusqu'à soixante pour cent à cinq minutes، ومن بعد كتنقص، jusqu'à environ deux pour cent à trente minutes. فla matrice، zéro avant trois minutes، ومن بعد كتطلع jusqu'à quarante-cinq pour cent à douze minutes، ومن بعد كتنقص، jusqu'à environ dix-huit pour cent. le C O deux ديال le milieu، zéro avant huit minutes، ومن بعد كيطلع، jusqu'à environ quarante-deux pour cent à trente minutes. on en déduit que les carbones ديال le glucose كيدوزو اللول فle hyaloplasme، من بعد فla matrice، وفاللخر كيخرجو فle C O deux."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "En exploitant le document 2, nommer la réaction qui se déroule dans le hyaloplasme, puis écrire sa réaction globale.",
       "texte_dit": "السؤال deux: بle document deux، سمي la réaction اللي كتوقع فle hyaloplasme، ومن بعد كتب la réaction globale ديالها.",
       "reponse": {"type": "phrase", "attendu": "Dans le hyaloplasme, le glucose ¹⁴C devient de l'acide pyruvique ¹⁴C : c'est la glycolyse. Réaction globale : C₆H₁₂O₆ + 2 NAD⁺ + 2 ADP + 2 Pi → 2 CH₃-CO-COOH + 2 NADH,H⁺ + 2 ATP."},
       "clavier": {"aides": ["glycolyse", "C₆H₁₂O₆", "2 NAD⁺", "2 ADP + 2 Pi", "2 CH₃-CO-COOH", "2 NADH,H⁺", "2 ATP", "→"], "pieges": ["6 O₂", "4 ATP", "C₃H₆O₃"]},
       "aides": [
         {"texte": "Document 2 : à 1 min puis à 5 min, quelle molécule radioactive remplace le glucose dans le hyaloplasme ?",
          "dit": "فle document deux، à une minute ومن بعد à cinq minutes، شمن molécule radioactive كتاخد البلاصة ديال le glucose فle hyaloplasme؟"},
         {"texte": "Écris d'abord les produits à droite (2 acides pyruviques, 2 NADH,H⁺, 2 ATP), puis à gauche ce qu'il faut pour les obtenir : le glucose, 2 NAD⁺, 2 ADP + 2 Pi.",
          "dit": "كتب اللول les produits على اليمين: deux acides pyruviques، deux N A D H, H plus، et deux ATP. ومن بعد على اليسار، شنو خاص باش يكونو: le glucose، deux N A D plus، et deux ADP avec deux phosphates."}],
       "correction": {"lignes": [
           {"texte": "2 : glucose ¹⁴C → acide pyruvique ¹⁴C dans le hyaloplasme : glycolyse", "mot": "هادي la glycolyse"},
           {"texte": "C₆H₁₂O₆ + 2 NAD⁺ + 2 ADP + 2 Pi → 2 CH₃-CO-COOH + 2 NADH,H⁺ + 2 ATP", "mot": "glucose plus deux N A D plus"}],
         "parole": "السؤال deux. فle hyaloplasme، le glucose radioactif ولا l'acide pyruvique radioactif: هادي la glycolyse. la réaction globale: glucose plus deux N A D plus, plus deux A D P plus deux phosphates, donne deux acides pyruviques, plus deux N A D H, H plus, plus deux A T P."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Expliquer l'apparition du CO₂ radioactif dans la matrice puis dans le milieu.",
       "texte_dit": "السؤال trois: شرح علاش كيبان le C O deux radioactif فla matrice، ومن بعد فle milieu.",
       "reponse": {"type": "phrase", "attendu": "L'acide pyruvique ¹⁴C entre dans la matrice. Il y subit une décarboxylation (et une déshydrogénation) : il donne l'acétyl-CoA et libère un CO₂ radioactif. L'acétyl-CoA entre dans le cycle de Krebs, dont les décarboxylations libèrent d'autres CO₂ radioactifs. Ce CO₂ vient donc des carbones du glucose (pas du dioxygène) ; il diffuse ensuite de la matrice vers le milieu."},
       "clavier": {"aides": ["décarboxylation", "acétyl-CoA", "cycle de Krebs", "matrice", "carbones du glucose"], "pieges": ["le CO₂ vient du dioxygène", "glycolyse"]},
       "aides": [
         {"texte": "Le CO₂ radioactif contient du ¹⁴C : ses carbones viennent forcément du glucose. Dans quelle molécule étaient-ils juste avant, dans la matrice ?",
          "dit": "le C O deux radioactif فيه le carbone quatorze: إذن les carbones ديالو جاو من le glucose. فشمن molécule كانو قبل، فla matrice؟"},
         {"texte": "Une réaction qui enlève un carbone sous forme de CO₂ s'appelle une décarboxylation : elle a lieu à la formation de l'acétyl-CoA et dans le cycle de Krebs.",
          "dit": "la réaction اللي كتحيد واحد le carbone على شكل C O deux، سميتها la décarboxylation. كتوقع ملي كيتكون l'acétyl-CoA، وفle cycle de Krebs."}],
       "correction": {"lignes": [
           {"texte": "3 : l'acide pyruvique ¹⁴C entre dans la matrice", "mot": "كيدخل للmatrice"},
           {"texte": "décarboxylation : acide pyruvique → acétyl-CoA + CO₂ ¹⁴C", "mot": "la décarboxylation"},
           {"texte": "cycle de Krebs : d'autres décarboxylations libèrent du CO₂ ¹⁴C", "mot": "le cycle de Krebs"},
           {"texte": "ce CO₂ vient des carbones du glucose, pas du dioxygène ; il passe dans le milieu", "mot": "ماشي من le dioxygène"}],
         "parole": "السؤال trois. l'acide pyruvique radioactif كيدخل للmatrice. تما كيوقع ليه la décarboxylation: كيخرج منو C O deux radioactif، وكيولي l'acétyl-CoA. من بعد l'acétyl-CoA كيدخل فle cycle de Krebs، وتما décarboxylations أخرين كيخرجو C O deux radioactif. إذن هاد le C O deux جا من les carbones ديال le glucose، ماشي من le dioxygène. ومن بعد كيخرج من la matrice للmilieu."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Calculer le nombre de molécules de CO₂ radioactives libérées dans la matrice par la dégradation complète d'une molécule de glucose.",
       "texte_dit": "السؤال quatre: حسب شحال ديال les molécules ديال C O deux radioactives كيخرجو فla matrice، ملي كتتفكك molécule وحدة ديال le glucose بالكامل.",
       "reponse": {"type": "valeur", "grandeur": "n", "valeur": N_CO2, "unite": "molécules", "tolerance": 0.02,
                   "attendu": "par acide pyruvique : 1 CO₂ (acétyl-CoA) + 2 CO₂ (un tour du cycle de Krebs) = 3 ; un glucose donne 2 acides pyruviques : n = 2 × (1 + 2) = 6 molécules"},
       "clavier": {"aides": ["2 acides pyruviques", "1 + 2", "2 × (1 + 2)", "molécules"], "pieges": ["2 CO₂", "3 CO₂"]},
       "aides": [
         {"texte": "Commence par un seul acide pyruvique : combien de CO₂ à la formation de l'acétyl-CoA, combien dans un tour du cycle de Krebs ?",
          "dit": "بدا ب l'acide pyruvique واحد: شحال ديال C O deux ملي كيتكون l'acétyl-CoA، وشحال فtour واحد ديال le cycle de Krebs؟"},
         {"texte": "N'oublie pas : un glucose donne deux acides pyruviques. Multiplie par 2.",
          "dit": "ما تنساش: le glucose كيعطي deux acides pyruviques. كلشي fois deux."}],
       "correction": {"lignes": [
           {"texte": "4 : par acide pyruvique : 1 CO₂ (acétyl-CoA) + 2 CO₂ (cycle de Krebs) = 3", "mot": "un plus deux، trois"},
           {"texte": "un glucose → 2 acides pyruviques : n = 2 × (1 + 2) = 6 molécules de CO₂", "mot": "n égale six"}],
         "parole": "السؤال quatre. l'acide pyruvique واحد كيعطي un C O deux ملي كيتكون l'acétyl-CoA، et deux C O deux فle cycle de Krebs: un plus deux، trois. و le glucose كيعطي deux acides pyruviques. إذن n égale deux fois trois، n égale six molécules ديال C O deux. les six carbones ديال le glucose كاملين خرجو فle C O deux."},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "Définir la glycolyse et le cycle de Krebs.",
       "texte_dit": "السؤال cinq: عرف la glycolyse و le cycle de Krebs.",
       "reponse": {"type": "phrase", "attendu": "La glycolyse est la dégradation du glucose en deux acides pyruviques, dans le hyaloplasme, sans besoin de dioxygène ; elle produit 2 ATP et 2 NADH,H⁺ (bilan net). Le cycle de Krebs est un ensemble de réactions qui se déroulent dans la matrice de la mitochondrie : l'acétyl-CoA y est dégradé par des décarboxylations et des déshydrogénations ; chaque tour libère 2 CO₂ et produit 3 NADH,H⁺, 1 FADH₂ et 1 ATP."},
       "clavier": {"aides": ["dégradation du glucose", "hyaloplasme", "matrice", "décarboxylations", "déshydrogénations", "3 NADH,H⁺", "FADH₂"], "pieges": ["avec dioxygène", "dans la membrane interne"]},
       "aides": [
         {"texte": "Une définition d'examen a trois éléments : ce que c'est, où cela se passe, ce que cela produit.",
          "dit": "la définition فالامتحان فيها ثلاث ديال الحوايج: شنو هي، فين كتوقع، وشنو كتعطي."},
         {"texte": "Glycolyse : glucose → 2 acides pyruviques, hyaloplasme, 2 ATP et 2 NADH,H⁺. Cycle de Krebs : matrice, acétyl-CoA dégradé, CO₂ et transporteurs réduits.",
          "dit": "la glycolyse: le glucose كيعطي deux acides pyruviques، فle hyaloplasme، avec deux ATP et deux N A D H, H plus. le cycle de Krebs: فla matrice، l'acétyl-CoA كيتفكك، وكيخرج C O deux و des transporteurs réduits."}],
       "correction": {"lignes": [
           {"texte": "5 : glycolyse : dégradation du glucose en 2 acides pyruviques, dans le hyaloplasme, sans O₂ ; 2 ATP et 2 NADH,H⁺", "mot": "la glycolyse، c'est la dégradation du glucose"},
           {"texte": "cycle de Krebs : réactions de la matrice ; l'acétyl-CoA est dégradé (décarboxylations, déshydrogénations)", "mot": "le cycle de Krebs، c'est un ensemble de réactions"},
           {"texte": "par tour : 2 CO₂, 3 NADH,H⁺, 1 FADH₂, 1 ATP", "mot": "trois N A D H, H plus"}],
         "parole": "السؤال cinq. نعاود نقرا: la glycolyse، c'est la dégradation du glucose en deux acides pyruviques, dans le hyaloplasme, sans dioxygène. كتعطي deux ATP et deux N A D H, H plus. و le cycle de Krebs، c'est un ensemble de réactions, dans la matrice de la mitochondrie. فيه l'acétyl-CoA كيتفكك، بdécarboxylations و déshydrogénations. كل tour كيعطي deux C O deux، trois N A D H, H plus، un F A D H deux، و un ATP."},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : suivre la radioactivité, compartiment par compartiment",
     "screen_content": {"lead": "D'abord le hyaloplasme, puis la matrice, enfin le CO₂."},
     "visual": {"kind": "simulation", "url": GM, "caption": "Le glucose ¹⁴C entre dans la cellule, puis dans la mitochondrie"},
     "speech_text": {"mixed": "شوف la cellule. les molécules اللي كيضويو فيهم le carbone quatorze. فالبداية، le glucose radioactif برا، فle milieu. من بعد دخل لle hyaloplasme. شوف: تقطع وولا l'acide pyruvique، فle hyaloplasme. من بعد l'acide pyruvique دخل للmitochondrie، وبانو les composés du cycle de Krebs. وفاللخر، خرج le C O deux radioactif. هادشي هو اللي كتبينو les courbes ديال التمرين: le hyaloplasme كيطلع اللول، jusqu'à soixante pour cent à cinq minutes. من بعد la matrice، jusqu'à quarante-cinq pour cent à douze minutes. وفاللخر le C O deux. ملي كتوصف، عطي لكل courbe فوقاش كتبان، le maximum ديالها، وشنو كتولي."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "hyaloplasme : maximum 60 % à 5 min, puis diminue", "mot": "jusqu'à soixante pour cent à cinq minutes"},
                  {"texte": "matrice : à partir de 3 min, maximum 45 % à 12 min", "mot": "jusqu'à quarante-cinq pour cent à douze minutes"},
                  {"texte": "puis CO₂ du milieu, après 8 min", "mot": "وفاللخر le C O deux. ملي"}],
       "pointage": [{"mot": "le glucose radioactif برا", "commande": "play_until", "parametres": {"moment": "t0"}},
                    {"mot": "من بعد دخل لle hyaloplasme", "commande": "play_until", "parametres": {"moment": "t1"}},
                    {"mot": "تقطع وولا l'acide pyruvique", "commande": "play_until", "parametres": {"moment": "t2"}},
                    {"mot": "دخل للmitochondrie", "commande": "play_until", "parametres": {"moment": "t3"}},
                    {"mot": "خرج le C O deux radioactif", "commande": "play_until", "parametres": {"moment": "t4"}},
                    {"mot": "jusqu'à soixante pour cent à cinq minutes", "cible": "centre:0"},
                    {"mot": "jusqu'à quarante-cinq pour cent à douze minutes", "cible": "centre:1"},
                    {"mot": "وفاللخر le C O deux. ملي", "cible": "centre:2"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : la glycolyse et sa réaction globale",
     "screen_content": {"lead": "Glucose → 2 acides pyruviques + 2 NADH,H⁺ + 2 ATP, dans le hyaloplasme."},
     "visual": {"kind": "simulation", "url": GLY, "caption": "La glycolyse dans le hyaloplasme"},
     "speech_text": {"mixed": "le glucose فle hyaloplasme، بعيد على la mitochondrie. شوف: les six carbones ولاو جوج ديال المجموعات، trois et trois. جاو deux N A D plus، وولاو deux N A D H, H plus. تكونو quatre ATP، ولكن deux تخسرو فالبداية: يبقى deux ATP. chaque groupe de trois carbones، هو l'acide pyruvique. دابا la réaction globale. على اليمين les produits. على اليسار le glucose. باش يكونو deux ATP، خاص deux ADP et deux phosphates. وباش يكونو deux N A D H, H plus، خاص deux N A D plus."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "glycolyse : glucose (6 C) → 2 acides pyruviques (3 C)", "mot": "هو l'acide pyruvique"},
                  {"texte": "C₆H₁₂O₆ + 2 NAD⁺ + 2 ADP + 2 Pi → 2 CH₃-CO-COOH + 2 NADH,H⁺ + 2 ATP", "mot": "خاص deux N A D plus"}],
       "pointage": [{"mot": "le glucose فle hyaloplasme", "commande": "play_until", "parametres": {"moment": "glucose_dans_hyaloplasme"}},
                    {"mot": "trois et trois", "commande": "play_until", "parametres": {"moment": "coupure_en_deux", "duree_s": 2.6}},
                    {"mot": "وولاو deux N A D H, H plus", "commande": "play_until", "parametres": {"moment": "taxis_charges", "duree_s": 2.6}},
                    {"mot": "تكونو quatre ATP", "commande": "play_until", "parametres": {"moment": "quatre_atp_formes", "duree_s": 2}},
                    {"mot": "يبقى deux ATP", "commande": "play_until", "parametres": {"moment": "gain_net"}},
                    {"mot": "هو l'acide pyruvique", "commande": "play_until", "parametres": {"moment": "deux_acides_pyruviques"}},
                    {"mot": "هو l'acide pyruvique", "cible": "centre:0"},
                    {"mot": "على اليمين les produits", "commande": "play_until", "parametres": {"moment": "reaction_droite"}},
                    {"mot": "على اليسار le glucose", "commande": "play_until", "parametres": {"moment": "reaction_glucose"}},
                    {"mot": "خاص deux ADP et deux phosphates", "commande": "play_until", "parametres": {"moment": "reaction_adp"}},
                    {"mot": "خاص deux N A D plus", "commande": "play_until", "parametres": {"moment": "reaction_nad"}},
                    {"mot": "خاص deux N A D plus", "cible": "centre:1"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : d'où vient le CO₂ ?",
     "screen_content": {"lead": "Le CO₂ sort de l'acide pyruvique par décarboxylation, dans la matrice."},
     "visual": {"kind": "simulation", "url": PYR, "caption": "L'acide pyruvique dans la matrice"},
     "speech_text": {"mixed": "شوف l'acide pyruvique: دخل للmatrice. دابا شوف: خرج منو C O deux. هادي la décarboxylation. من بعد N A D plus خدا deux hydrogènes: هادي la déshydrogénation. والجزء اللي بقا تلصق مع le coenzyme A: ولا عندنا l'acétyl-CoA. وl'acétyl-CoA غادي يدخل فle cycle de Krebs، فين كيخرجو C O deux أخرين. إذن les carbones ديال le C O deux جاو من le glucose، ماشي من le dioxygène."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "acide pyruvique → acétyl-CoA + CO₂ : décarboxylation", "mot": "هادي la décarboxylation"},
                  {"texte": "puis cycle de Krebs : d'autres CO₂", "mot": "فين كيخرجو C O deux أخرين"},
                  {"texte": "CO₂ = carbones du glucose, pas du dioxygène", "mot": "ماشي من le dioxygène"}],
       "pointage": [{"mot": "دخل للmatrice", "commande": "play_until", "parametres": {"moment": "entre_dans_matrice"}},
                    {"mot": "خرج منو C O deux", "commande": "play_until", "parametres": {"moment": "co2_part", "duree_s": 1.2}},
                    {"mot": "هادي la décarboxylation", "commande": "play_until", "parametres": {"moment": "decarboxylation"}},
                    {"mot": "هادي la décarboxylation", "cible": "centre:0"},
                    {"mot": "هادي la déshydrogénation", "commande": "play_until", "parametres": {"moment": "deshydrogenation"}},
                    {"mot": "ولا عندنا l'acétyl-CoA", "commande": "play_until", "parametres": {"moment": "acetyl_coa"}},
                    {"mot": "فين كيخرجو C O deux أخرين", "cible": "centre:1"},
                    {"mot": "ماشي من le dioxygène", "cible": "centre:2"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : compter les CO₂, sans oublier le × 2",
     "screen_content": {"lead": "1 + 2 = 3 CO₂ par acide pyruvique ; × 2 : 6 CO₂ par glucose."},
     "visual": {"kind": "simulation", "url": KREBS, "caption": "Un tour du cycle de Krebs, puis le second"},
     "speech_text": {"mixed": "تفكر: ملي تكون l'acétyl-CoA، خرج un C O deux. دابا le cycle de Krebs. شوف: خرج C O deux. وشوف: C O deux آخر. وهنا رجعنا لle composé à quatre carbones: tour واحد كيعطي deux C O deux. إذن l'acide pyruvique واحد: un plus deux، trois C O deux. ولكن le glucose عطانا deux acides pyruviques. شوف le deuxième tour. إذن deux fois trois، six C O deux: les six carbones ديال le glucose."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "un tour du cycle : 2 CO₂", "mot": "tour واحد كيعطي deux C O deux"},
                  {"texte": "par acide pyruvique : 1 + 2 = 3 CO₂", "mot": "un plus deux، trois C O deux"},
                  {"texte": "par glucose : n = 2 × (1 + 2) = 6 CO₂", "mot": "deux fois trois، six C O deux"}],
       "pointage": [{"mot": "شوف: خرج C O deux", "commande": "play_until", "parametres": {"moment": "co2_et_nadh_1", "duree_s": 2.2}},
                    {"mot": "وشوف: C O deux آخر", "commande": "play_until", "parametres": {"moment": "co2_et_nadh_2", "duree_s": 2.2}},
                    {"mot": "وهنا رجعنا", "commande": "play_until", "parametres": {"moment": "retour_4c", "duree_s": 3}},
                    {"mot": "tour واحد كيعطي deux C O deux", "cible": "centre:0"},
                    {"mot": "un plus deux، trois C O deux", "cible": "centre:1"},
                    {"mot": "شوف le deuxième tour", "commande": "play_until", "parametres": {"moment": "second_tour", "duree_s": 3.4}},
                    {"mot": "deux fois trois، six C O deux", "commande": "play_until", "parametres": {"moment": "six_co2"}},
                    {"mot": "deux fois trois، six C O deux", "cible": "centre:2"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : deux définitions, deux lieux",
     "screen_content": {"lead": "Glycolyse : hyaloplasme. Cycle de Krebs : matrice."},
     "visual": {"kind": "simulation", "url": GM, "caption": "Où se fait chaque étape"},
     "speech_text": {"mixed": "باش نعرفو، نتبعو le glucose radioactif. شوف: فle hyaloplasme، le glucose ولا deux acides pyruviques. هادي la glycolyse، فle hyaloplasme، بلا dioxygène، وكتعطي deux ATP et deux N A D H, H plus. من بعد l'acide pyruvique دخل للmitochondrie، وتفكك فla matrice حتى le C O deux: هنا كاين le cycle de Krebs، كل tour كيعطي deux C O deux، trois N A D H, H plus، un F A D H deux، و un ATP. فالتعريف، ديما: شنو هي، فين، وشنو كتعطي."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "glycolyse : glucose → 2 acides pyruviques, hyaloplasme, sans O₂ ; 2 ATP, 2 NADH,H⁺", "mot": "هادي la glycolyse"},
                  {"texte": "cycle de Krebs : matrice ; par tour 2 CO₂, 3 NADH,H⁺, 1 FADH₂, 1 ATP", "mot": "هنا كاين le cycle de Krebs"},
                  {"texte": "définition = nature + lieu + produits", "mot": "شنو هي، فين، وشنو كتعطي"}],
       "pointage": [{"mot": "le glucose ولا deux acides pyruviques", "commande": "play_until", "parametres": {"moment": "t2"}},
                    {"mot": "هادي la glycolyse", "commande": "play_until", "parametres": {"moment": "glycolyse"}},
                    {"mot": "هادي la glycolyse", "cible": "centre:0"},
                    {"mot": "دخل للmitochondrie", "commande": "play_until", "parametres": {"moment": "t4"}},
                    {"mot": "هنا كاين le cycle de Krebs", "commande": "play_until", "parametres": {"moment": "matrice"}},
                    {"mot": "هنا كاين le cycle de Krebs", "cible": "centre:1"},
                    {"mot": "شنو هي، فين، وشنو كتعطي", "cible": "centre:2"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : l'ordre des compartiments", "نتمرنو بسؤال ساهل على les courbes.",
      "D'après le document 1, la radioactivité apparaît dans l'ordre…", ["matrice, puis hyaloplasme, puis CO₂", "hyaloplasme, puis matrice, puis CO₂ du milieu", "CO₂, puis hyaloplasme, puis matrice"], 1, {
        "1": {"juste": rep("برافو! le hyaloplasme اللول، من بعد la matrice، وفاللخر le C O deux.", "Juste : hyaloplasme, puis matrice, puis CO₂.")},
        "0": {"1": rep("ما تقلقش. شوف فين كتبدا كل courbe: la courbe ديال la matrice كتبدا غير après trois minutes. عاود اختار.", "La courbe de la matrice ne démarre qu'après 3 min. Laquelle démarre dès 0 ? Réessaie."),
              "2": rep("الجواب هو le hyaloplasme، من بعد la matrice، من بعد le C O deux. le glucose كيتحول اللول فle hyaloplasme.", "Réponse : hyaloplasme → matrice → CO₂.")},
        "2": {"1": rep("لا، le C O deux كيبان فاللخر، après huit minutes. شوف شمن courbe كتبدا à zéro. عاود اختار.", "Le CO₂ n'apparaît qu'après 8 min. Quelle courbe démarre dès 0 ? Réessaie."),
              "2": rep("الجواب هو le hyaloplasme، من بعد la matrice، وفاللخر le C O deux.", "Réponse : hyaloplasme → matrice → CO₂.")}},
      "D'après le document un, dans quel ordre apparaît la radioactivité ?"),
    qcm_facile("fa_s2", "Plus facile : la gauche de la réaction", "سؤال ساهل على la réaction globale ديال la glycolyse.",
      "Glucose + … → 2 CH₃-CO-COOH + 2 NADH,H⁺ + 2 ATP. Il manque…", ["6 O₂", "2 NADH,H⁺ + 2 ATP", "2 NAD⁺ + 2 ADP + 2 Pi"], 2, {
        "2": {"juste": rep("برافو! باش يكونو deux ATP، خاص deux ADP et deux phosphates، وباش يكونو deux N A D H, H plus، خاص deux N A D plus.", "Juste : 2 NAD⁺ + 2 ADP + 2 Pi.")},
        "0": {"1": rep("لا، la glycolyse ما كتستعملش le dioxygène. شوف les produits: منين جاو l'ATP و N A D H, H plus؟ عاود اختار.", "La glycolyse n'utilise pas de dioxygène. D'où viennent l'ATP et le NADH,H⁺ ? Réessaie."),
              "2": rep("الجواب هو deux N A D plus، deux ADP et deux phosphates. la glycolyse بلا dioxygène.", "Réponse : 2 NAD⁺ + 2 ADP + 2 Pi ; la glycolyse se fait sans O₂.")},
        "1": {"1": rep("هادو هوما les produits، كاينين على اليمين. على اليسار خاص اللي عطاهم. عاود اختار.", "Ce sont les produits, à droite. À gauche, ce qui les a donnés. Réessaie."),
              "2": rep("الجواب هو deux N A D plus، deux ADP et deux phosphates: هوما اللي كيوليو N A D H, H plus و ATP.", "Réponse : 2 NAD⁺ + 2 ADP + 2 Pi.")}},
      "Dans la réaction globale de la glycolyse, que faut-il écrire à gauche avec le glucose ?"),
    vrai_faux("fa_s3", "Plus facile : l'origine du CO₂", "Dis si chaque phrase est vraie ou fausse.",
      "سؤال ساهل: قول واش كل جملة vrai ولا faux.", [
        ("Le CO₂ radioactif vient du dioxygène respiré.", False, "Faux : il contient du ¹⁴C ; ses carbones viennent du glucose."),
        ("Le CO₂ est libéré par des décarboxylations, dans la matrice.", True, "Vrai : à la formation de l'acétyl-CoA et dans le cycle de Krebs."),
        ("La glycolyse libère du CO₂ dans le hyaloplasme.", False, "Faux : la glycolyse donne l'acide pyruvique ; le CO₂ sort dans la matrice.")]),
    qcm_facile("fa_s4", "Plus facile : CO₂ par acide pyruvique", "سؤال ساهل: نحسبو غير ل l'acide pyruvique واحد.",
      "Combien de CO₂ libère un seul acide pyruvique dégradé dans la matrice (acétyl-CoA + un tour du cycle) ?", ["1", "3", "6"], 1, {
        "1": {"juste": rep("برافو! un plus deux، trois. ولle glucose، deux fois trois، six.", "Juste : 1 + 2 = 3 ; pour un glucose, 2 × 3 = 6.")},
        "0": {"1": rep("هادا غير le C O deux ديال l'acétyl-CoA. نساتي le cycle de Krebs. عاود اختار.", "C'est seulement le CO₂ de l'acétyl-CoA ; et le cycle de Krebs ? Réessaie."),
              "2": rep("الجواب هو trois: un ملي كيتكون l'acétyl-CoA، et deux فle cycle de Krebs.", "Réponse : 3 (1 + 2).")},
        "2": {"1": rep("six هو ديال le glucose كامل. هنا l'acide pyruvique واحد. عاود اختار.", "6, c'est pour un glucose entier ; ici un seul acide pyruvique. Réessaie."),
              "2": rep("الجواب هو trois. six هو deux fois trois، ديال le glucose كامل.", "Réponse : 3 ; 6 = 2 × 3 pour le glucose.")}},
      "Combien de molécules de C O deux pour un seul acide pyruvique ?"),
    association("fa_s5", "Plus facile : chaque étape et ce qu'elle fait", "Relie chaque étape à sa description.",
      "سؤال ساهل: ربط كل étape مع الوصف ديالها.", "Relie chaque étape à ce qui la définit.",
      [("1", "Glycolyse"), ("2", "Formation de l'acétyl-CoA"), ("3", "Cycle de Krebs")],
      [("a", "Hyaloplasme : glucose → 2 acides pyruviques + 2 NADH,H⁺ + 2 ATP"),
       ("b", "Matrice : acide pyruvique → acétyl-CoA + CO₂ + NADH,H⁺"),
       ("c", "Matrice : un tour libère 2 CO₂ et donne 3 NADH,H⁺, 1 FADH₂, 1 ATP")],
      {"1": "a", "2": "b", "3": "c"}, {
        "1-a": (True, "Oui : la glycolyse se fait dans le hyaloplasme et donne 2 acides pyruviques.", "برافو: la glycolyse فle hyaloplasme، وكتعطي deux acides pyruviques."),
        "1-b": (False, "Non : la glycolyse part du glucose, pas de l'acide pyruvique, et ne se fait pas dans la matrice.", "لا، la glycolyse كتبدا من le glucose، ماشي من l'acide pyruvique، وما كتوقعش فla matrice."),
        "1-c": (False, "Non : la glycolyse ne libère pas de CO₂ et ne se fait pas dans la matrice.", "لا، la glycolyse ما كتخرجش C O deux، وما كتوقعش فla matrice."),
        "2-a": (False, "Non : l'acétyl-CoA se forme dans la matrice, à partir de l'acide pyruvique.", "لا، l'acétyl-CoA كيتكون فla matrice، من l'acide pyruvique."),
        "2-b": (True, "Oui : une décarboxylation (CO₂) et une déshydrogénation (NADH,H⁺) donnent l'acétyl-CoA.", "برافو: décarboxylation و déshydrogénation، وكيتكون l'acétyl-CoA."),
        "2-c": (False, "Non : cette description est celle d'un tour du cycle, qui suit la formation de l'acétyl-CoA.", "لا، هادا هو tour ديال le cycle، اللي كيجي من بعد l'acétyl-CoA."),
        "3-a": (False, "Non : le cycle de Krebs se fait dans la matrice, pas dans le hyaloplasme.", "لا، le cycle de Krebs كيوقع فla matrice، ماشي فle hyaloplasme."),
        "3-b": (False, "Non : un tour du cycle libère deux CO₂, pas un seul.", "لا، tour واحد ديال le cycle كيخرج deux C O deux، ماشي واحد."),
        "3-c": (True, "Oui : par tour, 2 CO₂, 3 NADH,H⁺, 1 FADH₂ et 1 ATP.", "برافو: كل tour، deux C O deux، trois N A D H, H plus، un F A D H deux، و un ATP.")},
      ("(1 ; a) (2 ; b) (3 ; c)", "la glycolyse فle hyaloplasme، من بعد l'acétyl-CoA، من بعد le cycle de Krebs، بجوج فla matrice."))
  ]}]},
  "similaire": {
    "id": "svt_ex_ch1_glucose_marque_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même expérience avec des cellules musculaires placées dans un milieu riche en dioxygène et du glucose dont les six carbones sont marqués au ¹⁴C. Le document 1 donne la radioactivité du hyaloplasme, de la matrice et du CO₂ du milieu ; le document 2, les molécules radioactives identifiées.",
      "intro_dit": "نفس التجربة، مع des cellules musculaires، فmilieu فيه le dioxygène، و le glucose فيه le carbone quatorze فles six carbones ديالو.",
      "figures": [FIGS],
      "donnees": ["Document 2 : molécules radioactives identifiées",
                  "à t = 1 min : glucose ¹⁴C dans le hyaloplasme",
                  "à t = 4 min : acide pyruvique ¹⁴C dans le hyaloplasme",
                  "à t = 10 min : acide pyruvique, acétyl-CoA et composés du cycle de Krebs ¹⁴C dans la matrice",
                  "à t = 18 min : CO₂ ¹⁴C dans la matrice et dans le milieu",
                  "Un tour du cycle de Krebs libère 2 CO₂"],
      "questions": [
        {"id": "1", "texte": "Décrire l'évolution de la radioactivité du hyaloplasme, de la matrice et du CO₂ du milieu (document 1), puis déduire le trajet des carbones du glucose dans la cellule.",
         "reponse": {"type": "phrase", "attendu": "Hyaloplasme : la radioactivité augmente dès le début jusqu'à 55 % à 4 min, puis diminue jusqu'à environ 1 % à 30 min. Matrice : nulle avant 2 min, elle augmente jusqu'à 40 % à 10 min, puis diminue jusqu'à environ 11 % à 30 min. CO₂ du milieu : nulle avant 6 min, puis augmente jusqu'à environ 39 % à 30 min. On en déduit que les carbones du glucose passent d'abord dans le hyaloplasme, puis dans la matrice, et sortent sous forme de CO₂."},
         "clavier": {"aides": ["augmente", "diminue", "55 % à 4 min", "40 % à 10 min", "On en déduit que"], "pieges": ["d'abord dans la matrice"]},
         "correction": {"lignes": [{"texte": "1 : hyaloplasme : 55 % à 4 min puis diminue ; matrice : dès 2 min, 40 % à 10 min puis diminue", "mot": "cinquante-cinq pour cent à quatre minutes"},
                                   {"texte": "CO₂ : dès 6 min, augmente (≈ 39 % à 30 min) ; trajet : hyaloplasme → matrice → CO₂", "mot": "on en déduit que"}],
                        "parole": "le hyaloplasme كيطلع jusqu'à cinquante-cinq pour cent à quatre minutes، ومن بعد كينقص. la matrice كتبدا à partir de deux minutes، jusqu'à quarante pour cent à dix minutes، ومن بعد كتنقص. le C O deux كيبدا à partir de six minutes، jusqu'à environ trente-neuf pour cent. on en déduit que les carbones كيدوزو من le hyaloplasme، ل la matrice، ل le C O deux."}},
        {"id": "2", "texte": "En exploitant le document 2, nommer la réaction qui se déroule dans le hyaloplasme, puis écrire sa réaction globale.",
         "reponse": {"type": "phrase", "attendu": "Glycolyse : C₆H₁₂O₆ + 2 NAD⁺ + 2 ADP + 2 Pi → 2 CH₃-CO-COOH + 2 NADH,H⁺ + 2 ATP."},
         "clavier": {"aides": ["glycolyse", "2 NAD⁺", "2 ADP + 2 Pi", "2 CH₃-CO-COOH", "2 NADH,H⁺", "2 ATP"], "pieges": ["6 O₂", "4 ATP"]},
         "correction": {"lignes": [{"texte": "2 : glycolyse : C₆H₁₂O₆ + 2 NAD⁺ + 2 ADP + 2 Pi → 2 CH₃-CO-COOH + 2 NADH,H⁺ + 2 ATP", "mot": "la glycolyse"}],
                        "parole": "la glycolyse: glucose plus deux N A D plus, plus deux A D P plus deux phosphates, donne deux acides pyruviques, plus deux N A D H, H plus, plus deux A T P."}},
        {"id": "3", "texte": "Expliquer l'apparition du CO₂ radioactif dans la matrice puis dans le milieu.",
         "reponse": {"type": "phrase", "attendu": "L'acide pyruvique ¹⁴C entre dans la matrice ; sa décarboxylation donne l'acétyl-CoA et un CO₂ radioactif ; les décarboxylations du cycle de Krebs libèrent d'autres CO₂ radioactifs. Ce CO₂ vient des carbones du glucose, pas du dioxygène, puis passe dans le milieu."},
         "clavier": {"aides": ["décarboxylation", "acétyl-CoA", "cycle de Krebs"], "pieges": ["le CO₂ vient du dioxygène"]},
         "correction": {"lignes": [{"texte": "3 : décarboxylation de l'acide pyruvique (acétyl-CoA) puis cycle de Krebs : CO₂ ¹⁴C", "mot": "la décarboxylation"},
                                   {"texte": "le CO₂ vient des carbones du glucose, pas du dioxygène", "mot": "ماشي من le dioxygène"}],
                        "parole": "فla matrice، la décarboxylation ديال l'acide pyruvique، ومن بعد le cycle de Krebs، كيخرجو C O deux radioactif. جا من le glucose، ماشي من le dioxygène."}},
        {"id": "4", "texte": "Calculer le nombre de molécules de CO₂ radioactives libérées dans la matrice par la dégradation complète de deux molécules de glucose.",
         "reponse": {"type": "valeur", "grandeur": "n", "valeur": 2 * N_CO2, "unite": "molécules", "tolerance": 0.02,
                     "attendu": "par glucose : 2 × (1 + 2) = 6 CO₂ ; pour deux glucoses : n = 2 × 6 = 12 molécules"},
         "clavier": {"aides": ["2 × (1 + 2)", "2 × 6", "molécules"], "pieges": ["6"]},
         "correction": {"lignes": [{"texte": "4 : un glucose : 2 × (1 + 2) = 6 CO₂", "mot": "six C O deux"},
                                   {"texte": "deux glucoses : n = 2 × 6 = 12 molécules", "mot": "n égale douze"}],
                        "parole": "le glucose واحد كيعطي deux fois trois، six C O deux. deux glucoses: n égale deux fois six، n égale douze molécules."}},
        {"id": "5", "texte": "Définir la glycolyse et le cycle de Krebs.",
         "reponse": {"type": "phrase", "attendu": "Glycolyse : dégradation du glucose en deux acides pyruviques, dans le hyaloplasme, sans besoin de dioxygène (2 ATP et 2 NADH,H⁺). Cycle de Krebs : ensemble de réactions de la matrice où l'acétyl-CoA est dégradé par décarboxylations et déshydrogénations (par tour : 2 CO₂, 3 NADH,H⁺, 1 FADH₂, 1 ATP)."},
         "clavier": {"aides": ["hyaloplasme", "matrice", "décarboxylations", "déshydrogénations"], "pieges": ["membrane interne"]},
         "correction": {"lignes": [{"texte": "5 : glycolyse : glucose → 2 acides pyruviques, hyaloplasme, sans O₂", "mot": "la glycolyse"},
                                   {"texte": "cycle de Krebs : matrice, acétyl-CoA dégradé ; 2 CO₂, 3 NADH,H⁺, 1 FADH₂, 1 ATP par tour", "mot": "le cycle de Krebs"}],
                        "parole": "la glycolyse: le glucose كيولي deux acides pyruviques، فle hyaloplasme، بلا dioxygène. le cycle de Krebs: فla matrice، l'acétyl-CoA كيتفكك، وكل tour كيعطي deux C O deux، trois N A D H, H plus، un F A D H deux، و un ATP."}}
      ]}}
}

ecrire(EX, sys.argv[1])
