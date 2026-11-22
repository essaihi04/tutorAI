# Exercice SVT ch. 1 (réactions responsables de la libération de l'énergie) — niveau difficile (« Supérieur »).
# Ce qu'il entraîne : à partir des réactions globales des étapes (document 1), nommer et localiser chaque étape, compter
# les ATP directs, NADH,H⁺, FADH₂ et CO₂ pour UN glucose (le × 2 après la glycolyse), « montrer que » le bilan vaut 38 ATP
# avec la règle de conversion (3 et 2), calculer la part de la chaîne respiratoire, calculer le rendement avec la valeur
# d'un autre document (36 ATP : on suit l'énoncé, sans expliquer le 36, hors programme), lecture critique d'une copie fausse.
# Cadre vérifié dans l'exploration : valeurs_reperes (2 ATP nets et 2 NADH,H⁺ pour la glycolyse ; 1 NADH,H⁺ et 1 CO₂ par
# acide pyruvique pour l'acétyl-CoA ; Krebs 2 CO₂, 3 NADH,H⁺, 1 FADH₂, 1 ATP par tour ; 10 × 3 + 2 × 2 = 34 ; 38 ATP) ;
# relations du cadre (« 36 ATP si l'énoncé le dit ») ; exclus_hors_programme (navettes, 36 expliqué, 30/32 ATP, H⁺ pompés,
# noms des intermédiaires du cycle : rien de cela n'apparaît).
# Sources comparées (lecture seule, rien de copié) :
#   - exploration : cas_types calcul et equation, pieges (oubli du × 2, 4 NADH,H⁺ par tour, 4 ATP pour la glycolyse,
#     × 100 du rendement), erreurs_examen (rendement : « 38 ou 36 pris sans regarder l'énoncé », 2019 R).
#   - nationaux : 2017 N (réaction globale de la glycolyse), 2021 N (acide pyruvique → acétyl-CoA à compléter),
#     2022 R (tableau 2 ATP / 36 ATP), 2019 R (rendements 40 % et 2 %), 2022 N (définition du rendement).
#   - vidéos (exploration) : compteur « faisons la caisse » des professeurs (Abdellaoui, Sarah), bilan 2 + 2 + 30 + 4.
#   - séries en ligne : réseau bloqué dans cette session (hôtes non résolus) ; comparaison faite avec vidéos + nationaux.
import sys
from _commun import rep, qcm_facile, vrai_faux, association, ecrire

BASE = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/"
KREBS = BASE + "krebs.html?depart=retour_4c"
CPT0 = BASE + "compteur.html?depart=0"
CPT_CONV = BASE + "compteur.html?depart=compte_fadh"
REND = BASE + "rendement.html?depart=0"
GLY = BASE + "glycolyse.html?depart=coupure_en_deux"


def schema_etapes(depart_glucose=True):
    """Document 1 : les étapes numérotées sur une cellule ; les compartiments ne sont pas nommés."""
    el = [{"f": "ellipse", "c": [5, 2.5], "rx": 4.85, "ry": 2.4, "couleur": "vert"},
          {"f": "ellipse", "c": [6.75, 2.4], "rx": 2.75, "ry": 1.45, "couleur": "cyan"},
          {"f": "ellipse", "c": [6.75, 2.4], "rx": 2.35, "ry": 1.1, "couleur": "cyan", "trait": "tirets"},
          {"f": "texte", "at": [6.75, 4.1], "t": "mitochondrie", "taille": "petit", "couleur": "cyan"}]
    if depart_glucose:
        el += [{"f": "texte", "at": [1.3, 3.4], "t": "glucose", "couleur": "blanc"},
               {"f": "fleche", "de": [1.3, 3.1], "a": [1.9, 2.1], "couleur": "jaune", "texte": "1", "pos": "e"},
               {"f": "texte", "at": [2.2, 1.75], "t": "2 acides pyruviques", "taille": "petit", "couleur": "blanc"}]
    else:
        el += [{"f": "texte", "at": [2.2, 2.4], "t": "acide pyruvique", "taille": "petit", "couleur": "blanc"}]
    el += [{"f": "fleche", "de": [3.3, 2.1 if depart_glucose else 2.4], "a": [4.9, 2.4], "couleur": "jaune", "texte": "2", "pos": "n"},
           {"f": "texte", "at": [5.55, 2.4], "t": "acétyl-CoA", "taille": "petit", "couleur": "blanc"},
           {"f": "arc", "c": [7.4, 2.4], "r": 0.55, "de": 30, "a": 330, "couleur": "jaune", "fleche": True},
           {"f": "texte", "at": [7.4, 2.4], "t": "3", "couleur": "jaune"},
           {"f": "texte", "at": [8.85, 2.4], "t": "4", "couleur": "jaune"},
           {"f": "texte", "at": [8.3, 0.75], "t": "NADH,H⁺, FADH₂ → ATP", "taille": "petit", "couleur": "orange"},
           {"f": "fleche", "de": [8.3, 1.0], "a": [8.8, 2.05], "couleur": "orange"}]
    return {"type": "schema", "titre": "Document 1 : les étapes de la dégradation" + (" d'un glucose" if depart_glucose else " de l'acide pyruvique"),
            "legende": "Les étapes sont numérotées ; les compartiments de la cellule et de la mitochondrie ne sont pas nommés.",
            "cadre": {"l": 10, "h": 5}, "elements": el}


def copie(lignes, titre="Document 2 : le calcul d'un élève"):
    h = 0.7 * len(lignes) + 0.6
    el = [{"f": "rect", "de": [0.2, 0.15], "a": [9.8, h - 0.15], "couleur": "faible", "arrondi": True}]
    for i, t in enumerate(lignes):
        el.append({"f": "texte", "at": [0.6, round(h - 0.6 - 0.7 * i, 2)], "t": t, "ancre": "gauche", "couleur": "blanc"})
    return {"type": "schema", "titre": titre, "legende": "Copie reproduite telle qu'elle a été écrite (elle contient des erreurs).",
            "cadre": {"l": 10, "h": round(h, 2)}, "elements": el}


DONNEES = [
  "Étape 1 : C₆H₁₂O₆ + 2 NAD⁺ + 2 ADP + 2 Pi → 2 CH₃-CO-COOH + 2 NADH,H⁺ + 2 ATP",
  "Étape 2 : CH₃-CO-COOH + CoA-H + NAD⁺ → CH₃-CO-CoA + CO₂ + NADH,H⁺",
  "Étape 3 (un tour) : CH₃-CO-CoA + 3 NAD⁺ + FAD + ADP + Pi + 3 H₂O → 2 CO₂ + 3 NADH,H⁺ + FADH₂ + ATP + CoA-H",
  "Étape 4 (règle de la chaîne respiratoire) : 1 NADH,H⁺ → 3 ATP ; 1 FADH₂ → 2 ATP",
  "Une mole d'ATP : 30,5 kJ ; une mole de glucose : 2860 kJ"]

EX = {
  "id": "svt_ex_ch1_bilan_energetique_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "reactions_responsables_liberation_energie", "cours": "svt_ch1_reactions_responsables_liberation_energie",
  "titre": "Faire le bilan : les ATP d'un glucose respiré, et une copie à corriger", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Localiser les étapes de la respiration", "Compter les ATP et les transporteurs réduits par glucose",
                  "Établir le bilan énergétique de la respiration", "Calculer un pourcentage et un rendement", "Lire un calcul de façon critique"],
  "enonce": {
    "intro": "On veut établir le bilan énergétique de la respiration d'une molécule de glucose. Le document 1 situe les étapes de sa dégradation dans la cellule ; les données donnent la réaction globale de chaque étape et la règle de conversion des transporteurs réduits par la chaîne respiratoire. Le document 2 reproduit le calcul d'un élève.",
    "intro_dit": "دابا نقراو l'énoncé. بغينا نديرو le bilan énergétique ديال la respiration d'une molécule de glucose. le document un فيه les étapes، بالأرقام، فla cellule. les données فيهم la réaction globale ديال كل étape، و la règle ديال la chaîne respiratoire. و le document deux فيه le calcul ديال واحد التلميذ.",
    "figures": [schema_etapes(True),
                copie(["Glycolyse : 4 ATP", "Matrice : 1 ATP + 4 NADH,H⁺ + 1 FADH₂", "Chaîne respiratoire : 4 × 3 + 1 × 2 = 14 ATP", "Bilan = 4 + 1 + 14 = 19 ATP"])],
    "donnees": DONNEES,
    "questions": [
      {"id": "1", "texte": "Nommer chaque étape (1 à 4) et préciser son lieu. Puis dresser, pour UNE molécule de glucose, le nombre d'ATP directs, de NADH,H⁺, de FADH₂ et de CO₂ produits par chaque étape, et leurs totaux.",
       "texte_dit": "la question un: سمي كل étape، de un à quatre، وقول فين كتوقع. ومن بعد، d'une molécule de glucose، عطي le nombre ديال les ATP directs، و N A D H, H plus، و F A D H deux، و le C O deux، ديال كل étape، و le total.",
       "reponse": {"type": "phrase", "attendu": "Étape 1 : glycolyse, dans le hyaloplasme : 2 ATP, 2 NADH,H⁺, 0 FADH₂, 0 CO₂. Étape 2 : formation de l'acétyl-CoA, dans la matrice, deux fois (deux acides pyruviques) : 0 ATP, 2 NADH,H⁺, 0 FADH₂, 2 CO₂. Étape 3 : cycle de Krebs, dans la matrice, deux tours : 2 ATP, 6 NADH,H⁺, 2 FADH₂, 4 CO₂. Étape 4 : chaîne respiratoire (phosphorylation oxydative), dans la membrane interne de la mitochondrie. Totaux : 4 ATP directs, 10 NADH,H⁺, 2 FADH₂, 6 CO₂."},
       "clavier": {"aides": ["glycolyse", "hyaloplasme", "acétyl-CoA", "matrice", "cycle de Krebs", "membrane interne", "× 2", "NADH,H⁺", "FADH₂"], "pieges": ["espace intermembranaire", "4 ATP (glycolyse)", "4 NADH,H⁺ par tour"]},
       "aides": [
         {"texte": "Un glucose donne combien d'acides pyruviques (étape 1) ? Les étapes 2 et 3 se font donc combien de fois ?",
          "dit": "un glucose كيعطي شحال ديال l'acide pyruvique فl'étape un؟ إذن les étapes deux et trois، شحال من مرة كيوقعو؟"},
         {"texte": "Multiplie par 2 les produits des étapes 2 et 3, puis additionne colonne par colonne : ATP, NADH,H⁺, FADH₂, CO₂.",
          "dit": "ضرب les produits ديال les étapes deux et trois، fois deux. ومن بعد جمع colonne par colonne: les ATP، و N A D H, H plus، و F A D H deux، و le C O deux."}],
       "correction": {"lignes": [
           {"texte": "1 : étape 1 : glycolyse (hyaloplasme) : 2 ATP, 2 NADH,H⁺", "mot": "la glycolyse، فle hyaloplasme"},
           {"texte": "étape 2 : formation de l'acétyl-CoA (matrice), × 2 : 2 NADH,H⁺, 2 CO₂", "mot": "la formation de l'acétyl-CoA"},
           {"texte": "étape 3 : cycle de Krebs (matrice), × 2 : 2 ATP, 6 NADH,H⁺, 2 FADH₂, 4 CO₂", "mot": "le cycle de Krebs، فla matrice"},
           {"texte": "étape 4 : chaîne respiratoire (membrane interne)", "mot": "la chaîne respiratoire، فla membrane interne"},
           {"texte": "totaux : 4 ATP, 10 NADH,H⁺, 2 FADH₂, 6 CO₂", "mot": "les totaux"}],
         "parole": "la question un. l'étape un هي la glycolyse، فle hyaloplasme: deux ATP، et deux N A D H, H plus. l'étape deux هي la formation de l'acétyl-CoA، فla matrice. un glucose donne deux acides pyruviques، donc deux fois: deux N A D H, H plus، et deux C O deux. l'étape trois هي le cycle de Krebs، فla matrice، deux tours: deux ATP، six N A D H, H plus، deux F A D H deux، et quatre C O deux. l'étape quatre هي la chaîne respiratoire، فla membrane interne. les totaux: quatre ATP، dix N A D H, H plus، deux F A D H deux، et six C O deux."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Montrer que la respiration d'une molécule de glucose produit 38 ATP.",
       "texte_dit": "la question deux: بين بلي la respiration d'une molécule de glucose كتعطي، trente-huit ATP.",
       "reponse": {"type": "valeur", "grandeur": "bilan", "valeur": 38, "unite": "ATP", "tolerance": 0.01,
                   "attendu": "bilan = 4 + (10 × 3) + (2 × 2) = 4 + 30 + 4 = 38 ATP"},
       "clavier": {"aides": ["ATP directs", "NADH,H⁺ × 3", "FADH₂ × 2", "bilan ="], "pieges": ["10 × 2", "2 × 3"]},
       "aides": [
         {"texte": "Les ATP viennent de deux sources : les ATP directs (étapes 1 et 3) et la chaîne respiratoire, qui convertit les transporteurs réduits.",
          "dit": "l'ATP كيجي من جوج البلايص: les ATP directs، ديال les étapes un et trois، و la chaîne respiratoire اللي كتحول les transporteurs réduits."},
         {"texte": "Applique la règle de l'étape 4 aux totaux de la question 1 (NADH,H⁺ × 3, FADH₂ × 2), puis ajoute les ATP directs.",
          "dit": "طبق la règle ديال l'étape quatre sur les totaux ديال la question un: N A D H, H plus، fois trois. F A D H deux، fois deux. ومن بعد زيد les ATP directs."}],
       "correction": {"lignes": [
           {"texte": "2 : ATP directs : 2 + 2 = 4", "mot": "les ATP directs"},
           {"texte": "chaîne respiratoire : (10 × 3) + (2 × 2) = 30 + 4 = 34 ATP", "mot": "donc trente-quatre ATP"},
           {"texte": "bilan = 4 + 34 = 38 ATP par glucose", "mot": "trente-huit ATP par glucose"}],
         "parole": "la question deux. les ATP directs: deux plus deux، égale quatre. la chaîne respiratoire: dix N A D H, H plus fois trois، égale trente، plus deux F A D H deux fois deux، égale quatre. donc trente-quatre ATP. le bilan: quatre plus trente-quatre، égale trente-huit ATP par glucose."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Calculer le pourcentage p des ATP fournis par la chaîne respiratoire (étape 4) dans ce bilan. Que peut-on en conclure ?",
       "texte_dit": "la question trois: حسب le pourcentage p ديال les ATP اللي كتعطي la chaîne respiratoire فهاد le bilan. شنو نستنتجو؟",
       "reponse": {"type": "valeur", "grandeur": "p", "valeur": 89.5, "unite": "%", "tolerance": 0.02,
                   "attendu": "p = 34/38 × 100 ≈ 89,5 %"},
       "clavier": {"aides": ["34", "38", "× 100", "%"], "pieges": ["4/38", "38/34"]},
       "aides": [
         {"texte": "Combien d'ATP la chaîne respiratoire fournit-elle sur les 38 ?",
          "dit": "la chaîne respiratoire، شحال كتعطي ديال ATP، sur trente-huit؟"},
         {"texte": "Pourcentage = ATP de la chaîne / ATP total × 100.",
          "dit": "le pourcentage: les ATP ديال la chaîne، مقسومين على le total، fois cent."}],
       "correction": {"lignes": [
           {"texte": "3 : ATP de la chaîne respiratoire : 30 + 4 = 34", "mot": "trente plus quatre"},
           {"texte": "p = 34/38 × 100 ≈ 89,5 %", "mot": "environ quatre-vingt-neuf virgule cinq pour cent"},
           {"texte": "donc l'essentiel de l'ATP vient de la phosphorylation oxydative (membrane interne)", "mot": "la phosphorylation oxydative"}],
         "parole": "la question trois. la chaîne respiratoire: trente plus quatre، égale trente-quatre ATP. p égale trente-quatre sur trente-huit، fois cent، environ quatre-vingt-neuf virgule cinq pour cent. إذن l'essentiel ديال l'ATP كيجي من la phosphorylation oxydative، فla membrane interne."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Un autre document retient 36 ATP par molécule de glucose respirée. Calculer le rendement énergétique r de la respiration avec cette valeur, puis le comparer à celui obtenu avec 38 ATP.",
       "texte_dit": "la question quatre: واحد document آخر، trente-six ATP par molécule de glucose. حسب le rendement énergétique r بهاد la valeur، ومن بعد قارنو مع le rendement، avec trente-huit ATP.",
       "reponse": {"type": "valeur", "grandeur": "r", "valeur": 38.4, "unite": "%", "tolerance": 0.02,
                   "attendu": "r = (36 × 30,5)/2860 × 100 = 1098/2860 × 100 ≈ 38,4 %"},
       "clavier": {"aides": ["r = (nombre d'ATP × 30,5)/2860 × 100", "36 × 30,5", "%"], "pieges": ["38 × 30,5", "2860/1098"]},
       "aides": [
         {"texte": "Même relation que pour 38 ATP : seul le nombre d'ATP change. On utilise toujours la valeur donnée par l'énoncé.",
          "dit": "نفس la relation، comme avec trente-huit ATP: غير le nombre d'ATP اللي تبدل. وديما خدم ب la valeur ديال l'énoncé."},
         {"texte": "Énergie dans l'ATP : nombre d'ATP × 30,5 kJ ; divise par l'énergie d'une mole de glucose, puis multiplie par 100.",
          "dit": "l'énergie فl'ATP: le nombre d'ATP، fois trente virgule cinq kilojoules. قسمها، sur l'énergie d'une mole de glucose، ومن بعد fois cent."}],
       "correction": {"lignes": [
           {"texte": "4 : énergie dans l'ATP : 36 × 30,5 = 1098 kJ", "mot": "trente-six fois trente virgule cinq"},
           {"texte": "r = 1098/2860 × 100 ≈ 38,4 %", "mot": "environ trente-huit virgule quatre pour cent"},
           {"texte": "avec 38 ATP : r ≈ 40,5 % ; dans les deux cas environ 40 %, le reste part en chaleur", "mot": "le reste part en chaleur"}],
         "parole": "la question quatre. l'énergie فl'ATP: trente-six fois trente virgule cinq، égale mille quatre-vingt-dix-huit kilojoules. r égale mille quatre-vingt-dix-huit، sur deux mille huit cent soixante، fois cent، environ trente-huit virgule quatre pour cent. avec trente-huit ATP، r égale quarante virgule cinq pour cent. فجوج الحالات، environ quarante pour cent، et le reste part en chaleur. وفالامتحان، خدم ديما ب la valeur ديال l'énoncé."},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "Le document 2 reproduit le calcul d'un élève. Relever les erreurs de ce calcul, en les justifiant à l'aide du document 1, puis écrire le calcul corrigé.",
       "texte_dit": "la question cinq: le document deux فيه le calcul ديال واحد التلميذ. لقا les erreurs، وبررهم ب le document un، ومن بعد كتب le calcul الصحيح.",
       "reponse": {"type": "phrase", "attendu": "Erreur 1 : la glycolyse donne 2 ATP nets (4 formés − 2 dépensés), et non 4. Erreur 2 : l'élève oublie les 2 NADH,H⁺ produits par la glycolyse. Erreur 3 : il ne compte qu'un acide pyruvique, alors qu'un glucose en donne deux : les étapes 2 et 3 se font deux fois (2 ATP, 8 NADH,H⁺, 2 FADH₂ dans la matrice). Calcul corrigé : bilan = 2 + 2 + (10 × 3) + (2 × 2) = 38 ATP, et non 19."},
       "clavier": {"aides": ["2 ATP nets", "4 − 2", "2 NADH,H⁺ de la glycolyse", "deux acides pyruviques", "× 2", "38 ATP"], "pieges": ["4 ATP nets", "19 ATP"]},
       "aides": [
         {"texte": "Vérifie trois choses dans la copie : les ATP nets de la glycolyse, ses NADH,H⁺, et le nombre d'acides pyruviques par glucose.",
          "dit": "شوف ثلاث حوايج فle calcul: les ATP nets ديال la glycolyse، و les N A D H, H plus ديالها، و le nombre ديال les acides pyruviques par glucose."},
         {"texte": "Relis l'étape 1 du document 1 (produits nets), puis refais le compte : étapes 2 et 3 × 2, règle 3 et 2.",
          "dit": "عاود قرا l'étape un فle document un. ومن بعد عاود الحساب: les étapes deux et trois، fois deux، و la règle، trois et deux."}],
       "correction": {"lignes": [
           {"texte": "5 : erreur 1 : glycolyse : 2 ATP nets (4 formés − 2 dépensés), pas 4", "mot": "quatre moins deux"},
           {"texte": "erreur 2 : les 2 NADH,H⁺ de la glycolyse sont oubliés", "mot": "les deux N A D H, H plus ديال la glycolyse"},
           {"texte": "erreur 3 : un seul acide pyruvique compté ; il y en a 2 : étapes 2 et 3 × 2", "mot": "un seul acide pyruvique"},
           {"texte": "corrigé : 2 + 2 + (10 × 3) + (2 × 2) = 38 ATP", "mot": "égale trente-huit ATP"}],
         "parole": "la question cinq. l'erreur un: la glycolyse، c'est deux ATP nets: quatre moins deux. l'élève a écrit quatre، وهادا غلط. l'erreur deux: التلميذ نسى les deux N A D H, H plus ديال la glycolyse. l'erreur trois: un glucose donne deux acides pyruviques، ولكن l'élève a compté un seul acide pyruvique. donc les étapes deux et trois، deux fois. le calcul juste: deux plus deux، plus dix fois trois، plus deux fois deux، égale trente-huit ATP، et non dix-neuf."},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : un tour, puis deux tours pour un glucose",
     "screen_content": {"lead": "Un glucose donne deux acides pyruviques : l'acétyl-CoA et le cycle de Krebs comptent deux fois."},
     "visual": {"kind": "simulation", "url": KREBS, "caption": "Le cycle de Krebs dans la matrice, puis le compte par glucose"},
     "speech_text": {"mixed": "شوف l'équation d'un tour: deux C O deux, trois N A D H, H plus, un F A D H deux, et un ATP. ولكن، un glucose donne deux acides pyruviques. donc deux tours: شوف le second tour. فla colonne fois deux، le C O deux: deux avec l'acétyl-CoA، plus quatre avec le cycle، égale six C O deux. و les N A D H, H plus: deux de la glycolyse، plus deux، plus six، égale dix. l'énergie دابا محمولة فles transporteurs: N A D H, H plus، et F A D H deux. وكلشي فla matrice، من غير la glycolyse اللي فle hyaloplasme."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "glycolyse (hyaloplasme) : 2 ATP, 2 NADH,H⁺", "mot": "شوف l'équation d'un tour"},
                  {"texte": "acétyl-CoA × 2 (matrice) : 2 NADH,H⁺, 2 CO₂ ; Krebs × 2 (matrice) : 2 ATP, 6 NADH,H⁺, 2 FADH₂, 4 CO₂", "mot": "donc deux tours"},
                  {"texte": "totaux : 4 ATP, 10 NADH,H⁺, 2 FADH₂, 6 CO₂", "mot": "plus six، égale dix"}],
       "pointage": [{"mot": "شوف l'équation d'un tour", "commande": "play_until", "parametres": {"moment": "equation_tour"}},
                    {"mot": "شوف l'équation d'un tour", "cible": "centre:0"},
                    {"mot": "شوف le second tour", "commande": "play_until", "parametres": {"moment": "second_tour", "duree_s": 3}},
                    {"mot": "donc deux tours", "cible": "centre:1"},
                    {"mot": "فla colonne fois deux", "commande": "play_until", "parametres": {"moment": "compteur_par_glucose"}},
                    {"mot": "égale six C O deux", "commande": "play_until", "parametres": {"moment": "six_co2"}},
                    {"mot": "plus six، égale dix", "commande": "play_until", "parametres": {"moment": "dix_nadh"}},
                    {"mot": "plus six، égale dix", "cible": "centre:2"},
                    {"mot": "l'énergie دابا محمولة", "commande": "play_until", "parametres": {"moment": "energie_transporteurs"}}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : faisons la caisse, 38 ATP",
     "screen_content": {"lead": "bilan = 2 + 2 + (10 × 3) + (2 × 2) = 38 ATP"},
     "visual": {"kind": "simulation", "url": CPT0, "caption": "Le compteur d'ATP d'un glucose respiré"},
     "speech_text": {"mixed": "نديرو الحساب. la glycolyse: deux ATP، et deux N A D H, H plus. l'acétyl-CoA: deux N A D H, H plus. le cycle de Krebs، deux fois: deux ATP، six N A D H, H plus، et deux F A D H deux. نجمعو les ATP directs: quatre. les N A D H, H plus: dix. les F A D H deux: deux. القاعدة: un N A D H, H plus vaut trois A T P، un F A D H deux vaut deux A T P. dix fois trois، trente. deux fois deux، quatre. la chaîne respiratoire: trente-quatre ATP. le bilan: deux، plus deux، plus trente، plus quatre: trente-huit A T P."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "bilan = 2 + 2 + (10 × 3) + (2 × 2) = 38 ATP", "mot": "le bilan: deux، plus deux"}],
       "pointage": [{"mot": "نديرو الحساب", "repere": "tableau"},
                    {"mot": "la glycolyse: deux ATP", "commande": "play_until", "parametres": {"moment": "glycolyse_comptee", "duree_s": 1.2}},
                    {"mot": "l'acétyl-CoA: deux", "commande": "play_until", "parametres": {"moment": "acetyl_compte", "duree_s": 1.2}},
                    {"mot": "le cycle de Krebs، deux fois", "commande": "play_until", "parametres": {"moment": "krebs_fois_deux", "duree_s": 3}},
                    {"mot": "نجمعو les ATP directs", "commande": "play_until", "parametres": {"moment": "compte_atp", "duree_s": 1.8}},
                    {"mot": "les N A D H, H plus: dix", "commande": "play_until", "parametres": {"moment": "compte_nadh", "duree_s": 2.6}},
                    {"mot": "les F A D H deux: deux", "commande": "play_until", "parametres": {"moment": "compte_fadh", "duree_s": 1}},
                    {"mot": "القاعدة:", "commande": "play_until", "parametres": {"moment": "regle", "duree_s": 2.4}},
                    {"mot": "dix fois trois", "commande": "play_until", "parametres": {"moment": "trente"}},
                    {"mot": "deux fois deux، quatre", "commande": "play_until", "parametres": {"moment": "quatre"}},
                    {"mot": "la chaîne respiratoire: trente-quatre", "commande": "play_until", "parametres": {"moment": "total_34"}},
                    {"mot": "le bilan: deux، plus deux", "commande": "play_until", "parametres": {"moment": "total_38"}},
                    {"mot": "le bilan: deux، plus deux", "cible": "centre:0"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : la chaîne respiratoire fournit presque tout",
     "screen_content": {"lead": "34 ATP sur 38 : p = 34/38 × 100 ≈ 89,5 %."},
     "visual": {"kind": "simulation", "url": CPT_CONV, "caption": "Les transporteurs se déchargent sur la chaîne respiratoire"},
     "speech_text": {"mixed": "دابا la conversion: les transporteurs كيتفرغو فla chaîne respiratoire. القاعدة: un N A D H, H plus vaut trois A T P، un F A D H deux vaut deux A T P. dix fois trois، trente. deux fois deux، quatre. la chaîne respiratoire: trente-quatre ATP، sur un total de trente-huit. trente-quatre sur trente-huit، fois cent: environ quatre-vingt-neuf virgule cinq pour cent. والباقي هوما les quatre ATP directs. إذن la phosphorylation oxydative هي اللي كتعطي l'essentiel ديال l'ATP."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "p = 34/38 × 100 ≈ 89,5 %", "mot": "environ quatre-vingt-neuf virgule cinq pour cent"}],
       "pointage": [{"mot": "دابا la conversion", "commande": "play_until", "parametres": {"moment": "conversion", "duree_s": 2.4}},
                    {"mot": "القاعدة:", "commande": "play_until", "parametres": {"moment": "regle", "duree_s": 1}},
                    {"mot": "dix fois trois", "commande": "play_until", "parametres": {"moment": "trente"}},
                    {"mot": "deux fois deux، quatre", "commande": "play_until", "parametres": {"moment": "quatre"}},
                    {"mot": "la chaîne respiratoire: trente-quatre ATP", "commande": "play_until", "parametres": {"moment": "total_34"}},
                    {"mot": "sur un total de trente-huit", "commande": "play_until", "parametres": {"moment": "total_38"}},
                    {"mot": "environ quatre-vingt-neuf virgule cinq pour cent", "cible": "centre:0"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : 36 ou 38 ATP, on suit l'énoncé",
     "screen_content": {"lead": "36 ATP : r ≈ 38,4 % ; 38 ATP : r ≈ 40,5 %."},
     "visual": {"kind": "simulation", "url": REND, "caption": "L'énergie du glucose et les briques d'ATP"},
     "speech_text": {"mixed": "هاد la barre: l'énergie d'une mole de glucose، deux mille huit cent soixante kilojoules. avec trente-huit ATP، le rendement: quarante virgule cinq pour cent. دابا نبدلو، et on prend trente-six ATP. شوف le calcul تبدل. le résultat: trente-huit virgule quatre pour cent. ومن بعد، le reste part en chaleur. فالامتحان، ما تختارش بوحدك: خدم ب la valeur اللي فl'énoncé."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "36 ATP : r = (36 × 30,5)/2860 × 100 = 1098/2860 × 100 ≈ 38,4 %", "mot": "trente-huit virgule quatre pour cent"},
                  {"texte": "38 ATP : r ≈ 40,5 %", "mot": "quarante virgule cinq pour cent"}],
       "pointage": [{"mot": "هاد la barre", "commande": "play_until", "parametres": {"moment": "barre_glucose", "duree_s": 2.4}},
                    {"mot": "avec trente-huit ATP", "commande": "play_until", "parametres": {"moment": "resultat", "duree_s": 3}},
                    {"mot": "quarante virgule cinq pour cent", "cible": "centre:1"},
                    {"mot": "دابا نبدلو", "commande": "set_parameters", "parametres": {"atp": 36}},
                    {"mot": "شوف le calcul تبدل", "repere": "ecrit_application"},
                    {"mot": "le résultat: trente-huit", "repere": "ecrit_resultat"},
                    {"mot": "trente-huit virgule quatre pour cent", "cible": "centre:0"},
                    {"mot": "le reste part en chaleur", "commande": "play_until", "parametres": {"moment": "chaleur", "duree_s": 1.6}}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : les trois erreurs de la copie",
     "screen_content": {"lead": "Glycolyse : 2 ATP nets et 2 NADH,H⁺ ; deux acides pyruviques : tout ce qui suit × 2."},
     "visual": {"kind": "simulation", "url": GLY, "caption": "La glycolyse : ce qu'elle donne vraiment"},
     "speech_text": {"mixed": "شوف la glycolyse. les transporteurs N A D plus كياخدو les hydrogènes: deux N A D H, H plus. هادو التلميذ نساهم. دابا: quatre ATP كيتكونو. ولكن فالبداية، deux ATP تصرفو. le gain net: quatre moins deux، égale deux ATP. وفاللخر: deux acides pyruviques. donc l'acétyl-CoA و le cycle de Krebs، deux fois. l'élève a compté un seul acide pyruvique: هادي l'erreur trois."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "erreur 2 : 2 NADH,H⁺ de la glycolyse oubliés", "mot": "هادو التلميذ نساهم"},
                  {"texte": "erreur 1 : 4 formés − 2 dépensés = 2 ATP nets", "mot": "le gain net"},
                  {"texte": "erreur 3 : 2 acides pyruviques → étapes 2 et 3 × 2 ; bilan = 2 + 2 + 30 + 4 = 38 ATP", "mot": "هادي l'erreur trois"}],
       "pointage": [{"mot": "les transporteurs N A D plus", "commande": "play_until", "parametres": {"moment": "taxis_charges", "duree_s": 2.4}},
                    {"mot": "هادو التلميذ نساهم", "cible": "centre:0"},
                    {"mot": "دابا: quatre ATP", "commande": "play_until", "parametres": {"moment": "quatre_atp_formes", "duree_s": 2}},
                    {"mot": "le gain net", "commande": "play_until", "parametres": {"moment": "gain_net"}},
                    {"mot": "le gain net", "cible": "centre:1"},
                    {"mot": "وفاللخر: deux acides", "commande": "play_until", "parametres": {"moment": "deux_acides_pyruviques"}},
                    {"mot": "هادي l'erreur trois", "cible": "centre:2"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    association("fa_s1", "Plus facile : chaque étape et ses produits (pour un glucose)", "Relie chaque étape à ce qu'elle produit pour UN glucose.",
      "سؤال ساهل: ربط كل étape مع les produits ديالها، d'un glucose.", "Relie chaque étape à ses produits, pour une molécule de glucose.",
      [("1", "Glycolyse"), ("2", "Formation de l'acétyl-CoA (× 2)"), ("3", "Cycle de Krebs (× 2)")],
      [("a", "2 ATP + 2 NADH,H⁺"), ("b", "2 NADH,H⁺ + 2 CO₂"), ("c", "2 ATP + 6 NADH,H⁺ + 2 FADH₂ + 4 CO₂")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : la glycolyse donne 2 ATP nets et 2 NADH,H⁺, sans CO₂.", "برافو: la glycolyse، deux ATP nets، et deux N A D H, H plus، بلا C O deux."),
       "1-b": (False, "Non : la glycolyse ne dégage pas de CO₂ ; le CO₂ sort dans la matrice. Cherche les produits avec de l'ATP.", "لا، la glycolyse ما كتطلقش C O deux. قلب على اللي فيها l'ATP."),
       "1-c": (False, "Non : FADH₂ et CO₂ viennent du cycle de Krebs, pas de la glycolyse.", "لا، F A D H deux و C O deux ديال le cycle de Krebs، ماشي la glycolyse."),
       "2-a": (False, "Non : la formation de l'acétyl-CoA ne produit pas d'ATP ; c'est une décarboxylation (CO₂) et une déshydrogénation.", "لا، l'acétyl-CoA ما كيعطيش l'ATP. فيه C O deux، و N A D H, H plus."),
       "2-b": (True, "Oui : par acide pyruvique, 1 CO₂ et 1 NADH,H⁺ ; × 2 pour un glucose.", "برافو: par acide pyruvique، un C O deux، et un N A D H, H plus. fois deux pour un glucose."),
       "2-c": (False, "Non : FADH₂ et ATP viennent du cycle de Krebs.", "لا، F A D H deux و l'ATP ديال le cycle de Krebs."),
       "3-a": (False, "Non : ce sont les produits de la glycolyse. Le cycle donne aussi du FADH₂ et du CO₂.", "لا، هادو ديال la glycolyse. le cycle كيعطي حتى F A D H deux، و C O deux."),
       "3-b": (False, "Non : c'est l'acétyl-CoA. Un tour de Krebs donne 3 NADH,H⁺, 1 FADH₂, 1 ATP et 2 CO₂.", "لا، هادا l'acétyl-CoA. le cycle، par tour: trois N A D H, H plus، un F A D H deux، un ATP، et deux C O deux."),
       "3-c": (True, "Oui : deux tours : 2 ATP, 6 NADH,H⁺, 2 FADH₂, 4 CO₂.", "برافو: deux tours: deux ATP، six N A D H, H plus، deux F A D H deux، et quatre C O deux.")},
      ("Totaux pour un glucose : 4 ATP directs, 10 NADH,H⁺, 2 FADH₂, 6 CO₂.",
       "le total pour un glucose: quatre ATP directs، dix N A D H, H plus، deux F A D H deux، et six C O deux.")),
    qcm_facile("fa_s2", "Plus facile : le bilan en ATP", "سؤال ساهل: اختار le bilan الصحيح.",
      "Le bilan en ATP d'un glucose respiré s'écrit…", ["2 + 2 + (10 × 3) + (2 × 2) = 38", "4 + (5 × 3) + (1 × 2) = 21", "2 + 2 + 10 + 2 = 16"], 0, {
        "0": {"juste": rep("برافو! les ATP directs، plus dix fois trois، plus deux fois deux: trente-huit ATP.", "Juste : 2 + 2 + (10 × 3) + (2 × 2) = 38 ATP.")},
        "1": {"1": rep("ما تقلقش. un glucose donne deux acides pyruviques. واش ضربتي، fois deux؟ عاود اختار.", "Un glucose donne deux acides pyruviques : as-tu tout multiplié par 2 ? Réessaie."),
              "2": rep("الجواب: deux plus deux، plus dix fois trois، plus deux fois deux، égale trente-huit. نسيتي le fois deux.", "Réponse : 2 + 2 + (10 × 3) + (2 × 2) = 38 ; tu as oublié le × 2.")},
        "2": {"1": rep("قريب! ولكن les transporteurs ماشي ATP: خاصهم يتحولو بla règle. عاود اختار.", "Presque : les transporteurs ne sont pas des ATP, il faut appliquer la règle (× 3 et × 2). Réessaie."),
              "2": rep("الجواب: trente-huit. un N A D H, H plus vaut trois A T P، un F A D H deux vaut deux A T P.", "Réponse : 38 ; 1 NADH,H⁺ → 3 ATP et 1 FADH₂ → 2 ATP.")}},
      "Le bilan en ATP d'un glucose respiré s'écrit ?"),
    qcm_facile("fa_s3", "Plus facile : la part de la chaîne respiratoire", "سؤال ساهل: la part ديال la chaîne respiratoire.",
      "La part des ATP fournis par la chaîne respiratoire est…", ["34/38 × 100 ≈ 89,5 %", "4/38 × 100 ≈ 10,5 %", "38/34 × 100 ≈ 112 %"], 0, {
        "0": {"juste": rep("برافو! trente-quatre sur trente-huit، fois cent: environ quatre-vingt-neuf virgule cinq pour cent.", "Juste : 34/38 × 100 ≈ 89,5 %.")},
        "1": {"1": rep("ما تقلقش. quatre هوما les ATP directs. la chaîne respiratoire كتعطي شحال؟ عاود اختار.", "4, ce sont les ATP directs. Combien la chaîne respiratoire en fournit-elle ? Réessaie."),
              "2": rep("الجواب: trente-quatre sur trente-huit، fois cent. quatre ATP هوما الباقي.", "Réponse : 34/38 × 100 ≈ 89,5 % ; les 4 ATP directs sont le reste.")},
        "2": {"1": rep("قريب! ولكن la part ديما inférieure à cent pour cent. شنو اللي خاصو يكون تحت؟ عاود اختار.", "Une part est toujours inférieure à 100 % : quel nombre doit être au dénominateur ? Réessaie."),
              "2": rep("الجواب: trente-quatre sur trente-huit، fois cent. قلبتي القسمة.", "Réponse : 34/38 × 100 ≈ 89,5 % ; ta fraction est inversée.")}},
      "La part des ATP fournis par la chaîne respiratoire est ?"),
    qcm_facile("fa_s4", "Plus facile : le rendement avec 36 ATP", "سؤال ساهل: le rendement، avec trente-six ATP.",
      "Avec 36 ATP par glucose, le rendement de la respiration est…", ["(36 × 30,5)/2860 × 100 ≈ 38,4 %", "(38 × 30,5)/2860 × 100 ≈ 40,5 %", "2860/(36 × 30,5) × 100 ≈ 260 %"], 0, {
        "0": {"juste": rep("برافو! خدمتي ب la valeur ديال l'énoncé: environ trente-huit virgule quatre pour cent.", "Juste : (36 × 30,5)/2860 × 100 ≈ 38,4 %.")},
        "1": {"1": rep("ما تقلقش. l'énoncé: trente-six، et non trente-huit. عاود اختار.", "L'énoncé donne 36 ATP, pas 38. Réessaie."),
              "2": rep("الجواب: trente-six fois trente virgule cinq، sur deux mille huit cent soixante، fois cent. خدم ب la valeur ديال l'énoncé.", "Réponse : (36 × 30,5)/2860 × 100 ≈ 38,4 % ; on suit la valeur de l'énoncé.")},
        "2": {"1": rep("قريب! ولكن le rendement ما يمكنش يكون supérieur à cent pour cent. عاود اختار.", "Un rendement ne peut pas dépasser 100 %. Réessaie."),
              "2": rep("الجواب: trente-six fois trente virgule cinq، sur deux mille huit cent soixante، fois cent. قلبتي القسمة.", "Réponse : (36 × 30,5)/2860 × 100 ≈ 38,4 % ; ta fraction est inversée.")}},
      "Avec trente-six ATP par glucose, le rendement de la respiration est ?"),
    vrai_faux("fa_s5", "Plus facile : vrai ou faux sur le comptage", "Vrai ou faux ?", "نتمرنو بvrai ou faux على الحساب.", [
      ("La glycolyse donne 4 ATP nets.", False, "Faux : 4 ATP formés − 2 dépensés = 2 ATP nets."),
      ("Un glucose donne deux acides pyruviques : l'acétyl-CoA et le cycle de Krebs se font deux fois.", True, "Vrai : tout ce qui suit la glycolyse est multiplié par 2."),
      ("Un tour du cycle de Krebs donne 4 NADH,H⁺.", False, "Faux : 3 ; le quatrième NADH,H⁺ par acide pyruvique vient de la formation de l'acétyl-CoA."),
      ("La chaîne respiratoire fournit 34 des 38 ATP.", True, "Vrai : (10 × 3) + (2 × 2) = 34.")])
  ]}]},
  "similaire": {
    "id": "svt_ex_ch1_bilan_energetique_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "On fournit de l'acide pyruvique à des mitochondries et on veut le bilan de l'oxydation complète d'UNE molécule d'acide pyruvique (document 1 : étapes 2, 3 et 4 ; mêmes réactions et même règle que dans l'exercice). Le document 2 reproduit le calcul d'un élève. Un manuel donne 2870 kJ pour une mole de glucose et retient 36 ATP par glucose respiré.",
      "intro_dit": "دابا l'acide pyruvique، فdes mitochondries. بغينا le bilan d'une molécule d'acide pyruvique. نفس les réactions، ونفس la règle. le document deux فيه le calcul ديال واحد التلميذ.",
      "figures": [schema_etapes(False), copie(["Matrice : 1 ATP + 3 NADH,H⁺ + 1 FADH₂", "Chaîne respiratoire : 3 × 3 + 1 × 2 = 11 ATP", "Bilan = 1 + 11 = 12 ATP"])],
      "donnees": DONNEES[1:4] + ["Une mole d'ATP : 30,5 kJ ; une mole de glucose : 2870 kJ ; 36 ATP par glucose (manuel)"],
      "questions": [
        {"id": "1", "texte": "Nommer les étapes 2, 3 et 4 et préciser leur lieu. Dresser, pour UNE molécule d'acide pyruvique, le nombre d'ATP directs, de NADH,H⁺, de FADH₂ et de CO₂ produits, et leurs totaux.",
         "reponse": {"type": "phrase", "attendu": "Étape 2 : formation de l'acétyl-CoA (matrice) : 1 NADH,H⁺, 1 CO₂. Étape 3 : cycle de Krebs (matrice), un tour : 1 ATP, 3 NADH,H⁺, 1 FADH₂, 2 CO₂. Étape 4 : chaîne respiratoire (membrane interne). Totaux : 1 ATP, 4 NADH,H⁺, 1 FADH₂, 3 CO₂."},
         "clavier": {"aides": ["matrice", "membrane interne", "acétyl-CoA", "cycle de Krebs"], "pieges": ["× 2", "hyaloplasme"]},
         "correction": {"lignes": [{"texte": "1 : acétyl-CoA (matrice) : 1 NADH,H⁺, 1 CO₂ ; Krebs (matrice) : 1 ATP, 3 NADH,H⁺, 1 FADH₂, 2 CO₂", "mot": "la formation de l'acétyl-CoA"},
                                   {"texte": "chaîne respiratoire (membrane interne) ; totaux : 1 ATP, 4 NADH,H⁺, 1 FADH₂, 3 CO₂", "mot": "les totaux"}],
                        "parole": "la formation de l'acétyl-CoA، فla matrice: un N A D H, H plus، et un C O deux. le cycle de Krebs، un tour: un ATP، trois N A D H, H plus، un F A D H deux، et deux C O deux. la chaîne respiratoire فla membrane interne. les totaux: un ATP، quatre N A D H, H plus، un F A D H deux، et trois C O deux."}},
        {"id": "2", "texte": "Montrer que l'oxydation complète d'une molécule d'acide pyruvique produit 15 ATP.",
         "reponse": {"type": "valeur", "grandeur": "bilan", "valeur": 15, "unite": "ATP", "tolerance": 0.01, "attendu": "bilan = 1 + (4 × 3) + (1 × 2) = 1 + 12 + 2 = 15 ATP"},
         "clavier": {"aides": ["NADH,H⁺ × 3", "FADH₂ × 2", "bilan ="], "pieges": ["3 × 3"]},
         "correction": {"lignes": [{"texte": "2 : chaîne : (4 × 3) + (1 × 2) = 14 ATP", "mot": "égale quatorze"}, {"texte": "bilan = 1 + 14 = 15 ATP", "mot": "égale quinze ATP"}],
                        "parole": "la chaîne respiratoire: quatre fois trois، plus un fois deux، égale quatorze. le bilan: un plus quatorze، égale quinze ATP."}},
        {"id": "3", "texte": "Calculer le pourcentage p des ATP fournis par la chaîne respiratoire dans ce bilan.",
         "reponse": {"type": "valeur", "grandeur": "p", "valeur": 93.3, "unite": "%", "tolerance": 0.02, "attendu": "p = 14/15 × 100 ≈ 93,3 %"},
         "clavier": {"aides": ["14", "15", "× 100", "%"], "pieges": ["1/15", "15/14"]},
         "correction": {"lignes": [{"texte": "3 : p = 14/15 × 100 ≈ 93,3 %", "mot": "quatre-vingt-treize virgule trois pour cent"}],
                        "parole": "p égale quatorze sur quinze، fois cent، environ quatre-vingt-treize virgule trois pour cent."}},
        {"id": "4", "texte": "Avec les valeurs du manuel (36 ATP, 2870 kJ), calculer le rendement énergétique r de la respiration d'un glucose.",
         "reponse": {"type": "valeur", "grandeur": "r", "valeur": 38.3, "unite": "%", "tolerance": 0.02, "attendu": "r = (36 × 30,5)/2870 × 100 = 1098/2870 × 100 ≈ 38,3 %"},
         "clavier": {"aides": ["36 × 30,5", "2870", "%"], "pieges": ["2860", "38 × 30,5"]},
         "correction": {"lignes": [{"texte": "4 : 36 × 30,5 = 1098 kJ", "mot": "trente-six fois trente virgule cinq"}, {"texte": "r = 1098/2870 × 100 ≈ 38,3 %", "mot": "trente-huit virgule trois pour cent"}],
                        "parole": "trente-six fois trente virgule cinq، égale mille quatre-vingt-dix-huit kilojoules. r égale mille quatre-vingt-dix-huit، sur deux mille huit cent soixante-dix، fois cent، environ trente-huit virgule trois pour cent."}},
        {"id": "5", "texte": "Relever l'erreur du calcul de l'élève (document 2), la justifier, puis écrire le calcul corrigé.",
         "reponse": {"type": "phrase", "attendu": "L'élève oublie le NADH,H⁺ produit par la formation de l'acétyl-CoA (étape 2) : il y a 4 NADH,H⁺ par acide pyruvique (1 + 3), et non 3. Calcul corrigé : 1 + (4 × 3) + (1 × 2) = 15 ATP, et non 12."},
         "clavier": {"aides": ["acétyl-CoA", "4 NADH,H⁺", "15 ATP"], "pieges": ["12 ATP"]},
         "correction": {"lignes": [{"texte": "5 : le NADH,H⁺ de l'acétyl-CoA est oublié : 4 NADH,H⁺ (1 + 3)", "mot": "ديال l'acétyl-CoA"},
                                   {"texte": "corrigé : 1 + (4 × 3) + (1 × 2) = 15 ATP", "mot": "égale quinze ATP"}],
                        "parole": "التلميذ نسى le N A D H, H plus ديال l'acétyl-CoA. donc quatre N A D H, H plus، et non trois. le calcul juste: un، plus quatre fois trois، plus un fois deux، égale quinze ATP."}}
      ]}}
}
ecrire(EX, sys.argv[1])
