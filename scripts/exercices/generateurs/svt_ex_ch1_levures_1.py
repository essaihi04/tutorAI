# Exercice pilote de SVT (ch. 1, réactions responsables de la libération de l'énergie).
import json, sys
EXAO = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/exao.html?vue=levures"
REND = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/rendement.html"

def rep(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}

def qcm_facile(sid, titre, intro, prompt, options, bonne, reactions, enonce_dit):
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": prompt}, "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "qcm", "prompt": prompt, "options": options, "correct": bonne, "enonce_dit": enonce_dit},
            "concentration": {"demarrer": "reset", "reponses": {"q": reactions}}}

def courbe_o2(t_inj, o2_0, pente_lente, pente, titre):
    o2_inj = o2_0 - pente_lente * t_inj
    t_fin = t_inj + o2_inj / pente
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": 0, "max": 14, "nom": "t", "unite": "min", "graduations": [0, 2, 4, 6, 8, 10, 12, 14]},
                     "y": {"min": 0, "max": 10, "nom": "[O₂]", "unite": "mg/L", "graduations": [0, 2, 4, 6, 8, 10]}},
            "legende": "Concentration du dioxygène dans l'enceinte, mesurée par la sonde (ExAO).",
            "elements": [
              {"f": "courbe", "expr": f"{o2_0}-{pente_lente}*x", "de": 0, "a": t_inj, "couleur": "cyan"},
              {"f": "courbe", "expr": f"{o2_inj}-{pente}*(x-{t_inj})", "de": t_inj, "a": round(t_fin, 3), "couleur": "cyan"},
              {"f": "courbe", "expr": "0.02", "de": round(t_fin, 3), "a": 14, "couleur": "cyan", "texte": "[O₂]", "texte_x": 12, "pos": "n"},
              {"f": "fleche", "de": [t_inj, 9.6], "a": [t_inj, o2_inj + 0.3], "couleur": "jaune", "texte": "glucose", "pos": "e"}]}

EX = {
  "id": "svt_ex_ch1_levures_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "reactions_responsables_liberation_energie", "cours": "svt_ch1_reactions_responsables_liberation_energie",
  "titre": "Des levures dans une enceinte : respiration, fermentation et rendement", "niveau": "facile", "duree_min": 20,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Décrire une courbe ExAO", "Distinguer respiration et fermentation", "Calculer un rendement énergétique"],
  "enonce": {
    "intro": "Des levures sont placées dans une enceinte fermée, avec une solution d'abord riche en dioxygène. Une sonde mesure la concentration du dioxygène [O₂]. À la date t = 2 min, on injecte du glucose. On constate aussi que de l'éthanol apparaît dans le milieu à partir de t = 8 min environ. La figure représente l'évolution de [O₂].",
    "intro_dit": "دابا نقراو l'énoncé. حطينا des levures فenceinte مسدودة، فsolution فيها le dioxygène. une sonde كتقيس la concentration ديال le dioxygène. فt égale deux minutes، زدنا le glucose. و après huit minutes، كيبان l'éthanol فle milieu. la figure كتبين l'évolution ديال la concentration ديال le dioxygène.",
    "figures": [courbe_o2(2, 8.0, 0.25, 1.2, "Évolution de [O₂] dans l'enceinte")],
    "donnees": ["Injection de glucose à t = 2 min", "Éthanol détecté à partir de t ≈ 8 min", "Une mole de glucose : 2860 kJ ; une mole d'ATP : 30,5 kJ ; respiration : 38 ATP par glucose"],
    "questions": [
      {"id": "1", "texte": "Décrire l'évolution de [O₂] avant puis après l'injection du glucose.",
       "texte_dit": "السؤال un: وصف l'évolution ديال la concentration ديال le dioxygène، قبل وبعد ما زدنا le glucose.",
       "reponse": {"type": "phrase", "attendu": "Avant l'injection, [O₂] diminue lentement (de 8 à 7,5 mg/L). Après l'injection, [O₂] diminue rapidement jusqu'à s'annuler vers 8 min, puis reste nulle."},
       "clavier": {"aides": ["diminue lentement", "diminue rapidement", "s'annule", "mg/L"], "pieges": ["augmente"]},
       "aides": [
         {"texte": "Découpe la courbe en trois parties : avant 2 min, de 2 min à l'annulation, après.",
          "dit": "قسم la courbe لثلاث ديال الأجزاء: قبل deux minutes، من deux minutes حتى كتولي zéro، ومن بعد."},
         {"texte": "Pour chaque partie, dis le sens (diminue, augmente, constante), la vitesse (lentement, rapidement) et les valeurs.",
          "dit": "فكل جزء، قول واش كتنقص ولا كتزاد ولا ثابتة، واش بشوية ولا بالزربة، وعطي les valeurs."}],
       "correction": {"lignes": [
           {"texte": "1 : avant 2 min : [O₂] diminue lentement, de 8 à 7,5 mg/L", "mot": "كتنقص بشوية"},
           {"texte": "après l'injection : [O₂] diminue rapidement", "mot": "كتنقص بالزربة"},
           {"texte": "vers 8 min : [O₂] = 0, puis reste nulle", "mot": "كتولي zéro"}],
         "parole": "السؤال un. قبل deux minutes، la concentration ديال le dioxygène كتنقص بشوية، de huit à sept virgule cinq milligrammes par litre. من بعد le glucose، كتنقص بالزربة. وفhuit minutes، كتولي zéro، وكتبقى zéro."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Nommer la réaction qui libère l'énergie entre 2 min et 8 min, puis celle qui se déroule après 8 min. Justifier.",
       "texte_dit": "السؤال deux: سمي la réaction اللي كتحرر l'énergie entre deux minutes et huit minutes، ومن بعد سمي اللي كتوقع après huit minutes. برر.",
       "reponse": {"type": "phrase", "attendu": "Entre 2 et 8 min : la respiration (les levures consomment le dioxygène). Après 8 min : la fermentation alcoolique (milieu sans dioxygène, apparition d'éthanol)."},
       "clavier": {"aides": ["respiration", "fermentation alcoolique", "O₂", "éthanol"], "pieges": ["fermentation lactique", "photosynthèse"]},
       "aides": [
         {"texte": "Entre 2 et 8 min, le dioxygène est consommé. Quelle réaction consomme du dioxygène ?",
          "dit": "entre deux et huit minutes، le dioxygène كيتستهلك. شمن réaction كتستهلك le dioxygène؟"},
         {"texte": "Après 8 min, il n'y a plus de dioxygène et l'éthanol apparaît : c'est une fermentation. Laquelle donne de l'éthanol ?",
          "dit": "après huit minutes، ماكاينش le dioxygène، وكيبان l'éthanol. هادي fermentation. شمن fermentation كتعطي l'éthanol؟"}],
       "correction": {"lignes": [
           {"texte": "2 : de 2 à 8 min, O₂ consommé : respiration", "mot": "هادي la respiration"},
           {"texte": "après 8 min : pas d'O₂, éthanol produit", "mot": "كيبان l'éthanol"},
           {"texte": "donc fermentation alcoolique", "mot": "la fermentation alcoolique"}],
         "parole": "السؤال deux. de deux à huit minutes، les levures كيستهلكو le dioxygène: هادي la respiration. من بعد، ماكاينش le dioxygène، وكيبان l'éthanol: هادي la fermentation alcoolique."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Calculer le rendement énergétique r de la respiration.",
       "texte_dit": "السؤال trois: حسب le rendement énergétique r ديال la respiration.",
       "reponse": {"type": "valeur", "grandeur": "r", "valeur": 40.5, "unite": "%", "tolerance": 0.02,
                   "attendu": "r = (38 × 30,5)/2860 × 100 = 1159/2860 × 100 ≈ 40,5 %"},
       "clavier": {"aides": ["r = (énergie dans l'ATP)/(énergie du glucose) × 100", "38 × 30,5", "2860", "%"], "pieges": ["2860/1159", "2 × 30,5"]},
       "aides": [
         {"texte": "Le rendement compare l'énergie mise dans l'ATP à l'énergie contenue dans le glucose.",
          "dit": "le rendement كيقارن l'énergie اللي دخلات فl'ATP، مع l'énergie اللي كاينة فle glucose."},
         {"texte": "Énergie dans l'ATP : 38 × 30,5 kJ. Divise par 2860 kJ puis multiplie par 100.",
          "dit": "l'énergie فl'ATP هي trente-huit fois trente virgule cinq kilojoules. قسمها على deux mille huit cent soixante، ومن بعد ضرب فcent."}],
       "correction": {"lignes": [
           {"texte": "3 : énergie dans l'ATP : 38 × 30,5 = 1159 kJ", "mot": "trente-huit fois trente virgule cinq"},
           {"texte": "r = 1159/2860 × 100", "mot": "r égale mille cent cinquante-neuf"},
           {"texte": "r ≈ 40,5 %", "mot": "quarante virgule cinq pour cent"}],
         "parole": "السؤال trois. l'énergie فl'ATP: trente-huit fois trente virgule cinq، كتعطي mille cent cinquante-neuf kilojoules. r égale mille cent cinquante-neuf، sur deux mille huit cent soixante، fois cent. r تقريبا quarante virgule cinq pour cent."},
       "explication": "ex_s3", "facile": "fa_s3"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : lire la courbe de [O₂], partie par partie",
     "screen_content": {"lead": "Trois parties : lente avant le glucose, rapide après, puis nulle."},
     "visual": {"kind": "simulation", "url": EXAO, "caption": "L'enceinte, la sonde et la courbe qui se trace"},
     "speech_text": {"mixed": "شوف l'enceinte والsonde. la courbe كتترسم. فالبداية، la concentration ديال le dioxygène كتنقص بشوية. فdeux minutes، كنزيدو le glucose. من بعد، كتنقص بالزربة: les levures كيستهلكو le dioxygène بزاف. حتى كتولي zéro، وكتبقى zéro."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "avant 2 min : diminue lentement", "mot": "كتنقص بشوية"}, {"texte": "après le glucose : diminue rapidement", "mot": "كتنقص بالزربة"}, {"texte": "puis [O₂] = 0", "mot": "حتى كتولي zéro"}],
       "pointage": [{"mot": "la courbe كتترسم", "commande": "play_until", "parametres": {"moment": "avant_glucose"}},
                    {"mot": "كتنقص بشوية", "cible": "centre:0"},
                    {"mot": "كنزيدو le glucose", "commande": "play_until", "parametres": {"moment": "injection"}},
                    {"mot": "كتنقص بالزربة", "commande": "play_until", "parametres": {"moment": "o2_baisse"}},
                    {"mot": "كتنقص بالزربة", "cible": "centre:1"},
                    {"mot": "حتى كتولي zéro", "commande": "play_until", "parametres": {"moment": "o2_epuise"}},
                    {"mot": "حتى كتولي zéro", "cible": "centre:2"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : avec O₂, la respiration ; sans O₂, la fermentation",
     "screen_content": {"lead": "O₂ consommé : respiration. Plus d'O₂ et éthanol : fermentation alcoolique."},
     "visual": {"kind": "simulation", "url": EXAO, "caption": "Avec puis sans dioxygène"},
     "speech_text": {"mixed": "ملي كاين le dioxygène، les levures كيستهلكوه، وكيطلقو le dioxyde de carbone: هادي la respiration، فmilieu aérobie. ملي كيسالي le dioxygène، le dioxyde de carbone كيبقى كيزيد، وكيبان l'éthanol. هادي la fermentation alcoolique، فmilieu anaérobie."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "avec O₂ : respiration (milieu aérobie)", "mot": "هادي la respiration"}, {"texte": "sans O₂ + éthanol : fermentation alcoolique", "mot": "هادي la fermentation alcoolique"}],
       "pointage": [{"mot": "les levures كيستهلكوه", "commande": "play_until", "parametres": {"moment": "co2_monte"}},
                    {"mot": "هادي la respiration", "commande": "play_until", "parametres": {"moment": "respiration"}},
                    {"mot": "هادي la respiration", "cible": "centre:0"},
                    {"mot": "ملي كيسالي le dioxygène", "commande": "play_until", "parametres": {"moment": "o2_epuise"}},
                    {"mot": "وكيبان l'éthanol", "commande": "play_until", "parametres": {"moment": "ethanol_apparait"}},
                    {"mot": "هادي la fermentation alcoolique", "commande": "play_until", "parametres": {"moment": "fermentation"}},
                    {"mot": "هادي la fermentation alcoolique", "cible": "centre:1"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : le rendement, brique par brique",
     "screen_content": {"lead": "38 briques d'ATP de 30,5 kJ, sur les 2860 kJ du glucose : r ≈ 40,5 %."},
     "visual": {"kind": "simulation", "url": REND, "caption": "L'énergie du glucose et les briques d'ATP"},
     "speech_text": {"mixed": "هاد la barre هي l'énergie ديال mole de glucose: deux mille huit cent soixante kilojoules. la respiration كتعطي trente-huit ATP، وكل ATP فيه trente virgule cinq kilojoules. trente-huit fois trente virgule cinq، كتعطي mille cent cinquante-neuf kilojoules. le rendement هو هاد l'énergie، على l'énergie ديال le glucose، fois cent. r تقريبا quarante virgule cinq pour cent. والباقي كيمشي chaleur."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "38 × 30,5 = 1159 kJ", "mot": "كتعطي mille cent cinquante-neuf kilojoules"}, {"texte": "r = 1159/2860 × 100 ≈ 40,5 %", "mot": "r تقريبا quarante virgule cinq pour cent"}],
       "pointage": [{"mot": "هاد la barre", "commande": "play_until", "parametres": {"moment": "barre_glucose"}},
                    {"mot": "la respiration كتعطي trente-huit ATP", "commande": "play_until", "parametres": {"moment": "briques_respiration"}},
                    {"mot": "كتعطي mille cent cinquante-neuf kilojoules", "commande": "play_until", "parametres": {"moment": "produit_1159"}},
                    {"mot": "le rendement هو هاد l'énergie", "commande": "play_until", "parametres": {"moment": "relation"}},
                    {"mot": "r تقريبا quarante virgule cinq pour cent", "commande": "play_until", "parametres": {"moment": "resultat"}},
                    {"mot": "r تقريبا quarante virgule cinq pour cent", "cible": "centre:1"},
                    {"mot": "والباقي كيمشي chaleur", "commande": "play_until", "parametres": {"moment": "chaleur"}}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : lire la courbe", "نتمرنو بسؤال ساهل على la courbe.",
      "Après l'injection du glucose, [O₂]…", ["diminue rapidement", "augmente", "reste constante"], 0, {
        "0": {"juste": rep("برافو عليك! من بعد le glucose، la concentration ديال le dioxygène كتنقص بالزربة.", "Juste : après le glucose, [O₂] diminue rapidement.")},
        "1": {"1": rep("ما تقلقش. شوف la courbe من بعد deux minutes: واش كتطلع ولا كتهبط؟ عاود اختار.", "Regarde la courbe après 2 min : monte-t-elle ou descend-elle ? Réessaie."),
              "2": rep("الجواب هو كتنقص بالزربة. la courbe كتهبط بزاف من بعد le glucose.", "Réponse : [O₂] diminue rapidement.")},
        "2": {"1": rep("قريب! ثابتة غير من بعد ما كتولي zéro. ولكن مباشرة من بعد le glucose، شنو كيوقع؟ عاود اختار.", "Elle n'est constante qu'à la fin (à 0). Juste après le glucose ? Réessaie."),
              "2": rep("الجواب هو كتنقص بالزربة. كتولي ثابتة غير ملي كتوصل ل zéro.", "Réponse : [O₂] diminue rapidement.")}},
      "Après l'injection du glucose, la concentration du dioxygène ?"),
    {"id": "fa_s2", "slide_type": "exercise", "title": "Plus facile : associer", "screen_content": {"lead": "Relie chaque condition à sa réaction."},
     "visual": {"kind": "none"}, "speech_text": {"mixed": "سؤال ساهل: ربط كل حالة مع la réaction ديالها."},
     "question": {"type": "association", "prompt": "Relie chaque situation à la réaction qui libère l'énergie.",
                  "association": {"gauche": [{"id": "1", "texte": "Levures avec dioxygène, O₂ consommé"}, {"id": "2", "texte": "Levures sans dioxygène, éthanol produit"}],
                                  "droite": [{"id": "a", "texte": "Respiration"}, {"id": "b", "texte": "Fermentation alcoolique"}, {"id": "c", "texte": "Fermentation lactique"}],
                                  "couples": {"1": "a", "2": "b"},
                                  "retours": {"1-a": {"juste": True, "texte": "Oui : le dioxygène consommé, c'est la respiration.", "dit": "برافو: le dioxygène كيتستهلك، هادي la respiration."},
                                              "1-b": {"juste": False, "texte": "La fermentation se fait sans dioxygène.", "dit": "لا، la fermentation كتوقع بلا dioxygène."},
                                              "1-c": {"juste": False, "texte": "Pas de dioxygène dans une fermentation, et les levures ne font pas de fermentation lactique.", "dit": "لا، la fermentation بلا dioxygène، وles levures ما كيديروش la fermentation lactique."},
                                              "2-a": {"juste": False, "texte": "La respiration consomme le dioxygène ; ici il n'y en a plus.", "dit": "لا، la respiration كتحتاج le dioxygène، وهنا ماكاينش."},
                                              "2-b": {"juste": True, "texte": "Oui : sans dioxygène, avec de l'éthanol : fermentation alcoolique.", "dit": "برافو: بلا dioxygène، وكاين l'éthanol: la fermentation alcoolique."},
                                              "2-c": {"juste": False, "texte": "La fermentation lactique donne de l'acide lactique, pas de l'éthanol.", "dit": "لا، la fermentation lactique كتعطي l'acide lactique، ماشي l'éthanol."}},
                                  "bilan": {"texte": "Avec O₂ : respiration. Sans O₂, avec éthanol : fermentation alcoolique.", "dit": "مع le dioxygène: la respiration. بلا dioxygène، مع l'éthanol: la fermentation alcoolique."},
                                  "melanger": True, "essais": 2}},
     "concentration": {"demarrer": "reset"}},
    qcm_facile("fa_s3", "Plus facile : la relation du rendement", "سؤال ساهل: اختار la relation ديال le rendement.",
      "Le rendement de la respiration s'écrit…", ["r = (38 × 30,5)/2860 × 100", "r = 2860/(38 × 30,5) × 100", "r = (2 × 30,5)/2860 × 100"], 0, {
        "0": {"juste": rep("برافو! l'énergie فl'ATP، على l'énergie ديال le glucose، fois cent. كتعطي quarante virgule cinq pour cent.", "Juste : r = (38 × 30,5)/2860 × 100 ≈ 40,5 %.")},
        "1": {"1": rep("ما تقلقش. le rendement ديما صغر من cent pour cent: اللي فوق هو l'énergie فl'ATP. عاود اختار.", "Un rendement est inférieur à 100 % : l'énergie de l'ATP est au numérateur. Réessaie."),
              "2": rep("الجواب هو trente-huit fois trente virgule cinq، sur deux mille huit cent soixante، fois cent. قلبتي القسمة.", "Réponse : r = (38 × 30,5)/2860 × 100 ; ta fraction est inversée.")},
        "2": {"1": rep("قريب! deux ATP هوما ديال la fermentation. la respiration كتعطي شحال ديال ATP؟ عاود اختار.", "2 ATP, c'est la fermentation. Combien d'ATP pour la respiration ? Réessaie."),
              "2": rep("الجواب هو trente-huit ATP، ماشي deux. deux ATP ديال la fermentation.", "Réponse : 38 ATP pour la respiration (2 ATP pour la fermentation).")}},
      "Le rendement de la respiration s'écrit ?")
  ]}]},
  "similaire": {
    "id": "svt_ex_ch1_levures_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même expérience avec une autre suspension de levures : [O₂] vaut 9 mg/L au départ, le glucose est injecté à t = 3 min, et l'éthanol apparaît vers t = 7,8 min. On admet ici que la respiration produit 36 ATP par molécule de glucose.",
      "intro_dit": "نفس التجربة، بقيم أخرى: la concentration ديال le dioxygène فالبداية neuf milligrammes par litre، le glucose فtrois minutes، وl'éthanol كيبان تقريبا من sept virgule huit minutes. وهنا la respiration كتعطي trente-six ATP.",
      "figures": [courbe_o2(3, 9.0, 0.3, 1.7, "Évolution de [O₂] dans l'enceinte")],
      "donnees": ["Glucose injecté à t = 3 min", "Éthanol à partir de t ≈ 7,8 min", "2860 kJ par mole de glucose ; 30,5 kJ par mole d'ATP ; 36 ATP"],
      "questions": [
        {"id": "1", "texte": "Décrire l'évolution de [O₂] avant puis après l'injection du glucose.",
         "reponse": {"type": "phrase", "attendu": "Avant 3 min, [O₂] diminue lentement (de 9 à 8,1 mg/L) ; après le glucose, elle diminue rapidement jusqu'à 0 vers 7,8 min, puis reste nulle."},
         "clavier": {"aides": ["diminue lentement", "diminue rapidement", "s'annule"], "pieges": ["augmente"]},
         "correction": {"lignes": [{"texte": "avant 3 min : diminue lentement (9 → 8,1 mg/L)", "mot": "كتنقص بشوية"}, {"texte": "après le glucose : diminue rapidement, nulle vers 7,8 min", "mot": "كتنقص بالزربة"}],
                        "parole": "قبل trois minutes، كتنقص بشوية، de neuf à huit virgule un. من بعد le glucose، كتنقص بالزربة، حتى كتولي zéro تقريبا فsept virgule huit minutes."}},
        {"id": "2", "texte": "Nommer la réaction avant et après t = 7,8 min. Justifier.",
         "reponse": {"type": "phrase", "attendu": "Avant 7,8 min : respiration (O₂ consommé). Après : fermentation alcoolique (pas d'O₂, éthanol produit)."},
         "clavier": {"aides": ["respiration", "fermentation alcoolique"], "pieges": ["fermentation lactique"]},
         "correction": {"lignes": [{"texte": "O₂ consommé : respiration", "mot": "la respiration"}, {"texte": "sans O₂, éthanol : fermentation alcoolique", "mot": "la fermentation alcoolique"}],
                        "parole": "ملي le dioxygène كيتستهلك: la respiration. بلا dioxygène، مع l'éthanol: la fermentation alcoolique."}},
        {"id": "3", "texte": "Calculer le rendement de la respiration avec 36 ATP.",
         "reponse": {"type": "valeur", "grandeur": "r", "valeur": 38.4, "unite": "%", "tolerance": 0.02, "attendu": "r = (36 × 30,5)/2860 × 100 = 1098/2860 × 100 ≈ 38,4 %"},
         "clavier": {"aides": ["36 × 30,5", "2860", "× 100", "%"], "pieges": ["38 × 30,5"]},
         "correction": {"lignes": [{"texte": "36 × 30,5 = 1098 kJ", "mot": "trente-six fois trente virgule cinq"}, {"texte": "r = 1098/2860 × 100 ≈ 38,4 %", "mot": "trente-huit virgule quatre pour cent"}],
                        "parole": "trente-six fois trente virgule cinq، كتعطي mille quatre-vingt-dix-huit kilojoules. r égale mille quatre-vingt-dix-huit، sur deux mille huit cent soixante، fois cent. r تقريبا trente-huit virgule quatre pour cent."}}
      ]}}
}
json.dump(EX, open(sys.argv[1], "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
print("ok", sys.argv[1])
