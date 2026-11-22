# Exercice SVT ch. 1 (réactions responsables de la libération de l'énergie) — niveau difficile (« Supérieur »).
# Ce qu'il entraîne : décrire par périodes (une ligne par période, avec les valeurs) les courbes de [O₂] et d'ATP d'une
# suspension de mitochondries qui a déjà de l'acide pyruvique (ajouts : ADP + Pi, puis cyanure), puis déduire ; calculer
# des vitesses de consommation de O₂ et leur rapport (le couplage se lit dans les pentes) ; exploiter un tableau de tubes
# (il manque O₂, acide pyruvique ou ADP + Pi) pour dégager les conditions de la phosphorylation oxydative ; expliquer le
# couplage par la chaîne respiratoire, le gradient de H⁺ et les sphères pédonculées ; expliquer l'effet du cyanure en flèches.
# Angle différent de svt_ex_ch1_mitochondries_1 (glucose sans effet / pyruvate consommé) : pas de glucose ici, l'acide
# pyruvique est présent dès le départ ; on travaille ADP + Pi, le rapport des vitesses, le couplage et l'inhibiteur.
# Cadre : cyanure présent dans le cours (diapositives le_c9_poison, le_x3c) et dans les nationaux (2021 R, 2025 N KCN) ;
# pas de complexes nommés, pas de nombre de H⁺ pompés, pas de force proton-motrice (exclus_hors_programme).
# Sources comparées (lecture seule, rien de copié) :
#   - exploration : cas_types mitochondries_isolees (« conditions de la synthèse d'ATP : pyruvate, ADP + Pi, O₂ ;
#     consommation de O₂ et production d'ATP couplées »), inhibiteur (dérouler la chaîne en flèches), hypothese ;
#     erreurs_examen « décrire… puis déduire » (une ligne par période avec la valeur), « expliquer » (maillons en flèches).
#   - nationaux : 2016 R (glucose, pyruvate, pyruvate + ADP + Pi), 2019 N, 2020 R, 2021 R (cyanure), 2025 N (KCN) :
#     même type de document, autre protocole et autres valeurs ici (aucun sujet réécrit).
#   - vidéos (exploration) : Bouhdadi (devoir corrigé : description par périodes, effet d'un inhibiteur), Ouissam
#     (décrire / déduire / expliquer), Sarah (construction de la chaîne respiratoire).
#   - séries en ligne : réseau bloqué dans cette session (hôtes non résolus) ; comparaison faite avec vidéos + nationaux.
# Les explications utilisent exao.html?vue=mitochondries (mêmes formes de courbes ; la voix ne dit pas les valeurs de la
# simulation, les valeurs de l'exercice sont écrites au centre) et chaine.html (couplage ; poison=cyanure&maillons).
import sys
from _commun import rep, qcm_facile, vrai_faux, association, ecrire

BASE = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/"
EXAO_PYR = BASE + "exao.html?vue=mitochondries&conclusions=false&depart=pyruvate_ajoute"
EXAO_PENTE = BASE + "exao.html?vue=mitochondries&conclusions=false&depart=ajout_pyruvate"
EXAO_0 = BASE + "exao.html?vue=mitochondries&depart=0"
CHAINE = BASE + "chaine.html?depart=membrane_seule"
CYAN = BASE + "chaine.html?poison=cyanure&maillons&depart=0"


def fr(v):
    return (f"{v:g}").replace(".", ",")


def doc1(t_adp, t_cya, o2_adp, o2_cya, atp0, atp1):
    """[O₂] (%) et ATP (UA) : acide pyruvique dès le départ ; ADP + Pi à t_adp ; cyanure à t_cya."""
    p1 = (100 - o2_adp) / t_adp; p2 = (o2_adp - o2_cya) / (t_cya - t_adp); pa = (atp1 - atp0) / (t_cya - t_adp)
    return {"type": "courbe", "titre": "Document 1 : [O₂] et ATP dans la suspension de mitochondries",
            "axes": {"x": {"min": 0, "max": 10, "nom": "t", "unite": "min", "graduations": list(range(0, 11))},
                     "y": {"min": 0, "max": 120, "nom": "[O₂] (%) ; ATP (UA)", "graduations": [0, 20, 40, 60, 80, 100]}},
            "legende": "En bleu : [O₂] en % de la valeur initiale ; en vert : concentration de l'ATP (UA). L'acide pyruvique est présent dès t = 0.",
            "elements": [
              {"f": "courbe", "expr": f"100-{p1:g}*x", "de": 0, "a": t_adp, "couleur": "cyan"},
              {"f": "courbe", "expr": f"{o2_adp}-{p2:g}*(x-{t_adp})", "de": t_adp, "a": t_cya, "couleur": "cyan"},
              {"f": "courbe", "expr": f"{o2_cya}", "de": t_cya, "a": 10, "couleur": "cyan", "texte": "[O₂]", "texte_x": 9.2, "pos": "s"},
              {"f": "courbe", "expr": f"{atp0}", "de": 0, "a": t_adp, "couleur": "vert"},
              {"f": "courbe", "expr": f"{atp0}+{pa:g}*(x-{t_adp})", "de": t_adp, "a": t_cya, "couleur": "vert"},
              {"f": "courbe", "expr": f"{atp1}", "de": t_cya, "a": 10, "couleur": "vert", "texte": "ATP", "texte_x": 9.2, "pos": "n"},
              {"f": "fleche", "de": [t_adp, 118], "a": [t_adp, 104], "couleur": "jaune", "texte": "ADP + Pi", "pos": "e"},
              {"f": "fleche", "de": [t_cya, 118], "a": [t_cya, 104], "couleur": "rouge", "texte": "cyanure", "pos": "e"},
              {"f": "repere", "x": t_adp, "y": o2_adp}, {"f": "repere", "x": t_cya, "y": o2_cya},
              {"f": "repere", "x": t_cya, "y": atp1}]}


def doc2(atp0, o2_c):
    L = [3.1, 2.4, 2.3, 2.2]; ent = ["Contenu du tube", "manque", "[O₂] à 10 min", "ATP à 10 min"]
    lignes = [["A : pyruvate + ADP + Pi", "O₂", "0 (pas d'O₂)", f"{atp0} UA"],
              ["B : O₂ + ADP + Pi", "acide pyruvique", "100 %", f"{atp0} UA"],
              ["C : O₂ + pyruvate", "ADP + Pi", f"{o2_c} %", f"{atp0} UA"]]
    hl = 0.9; n = 4; H = n * hl; W = sum(L)
    el = [{"f": "rect", "de": [0, 0], "a": [W, H], "couleur": "blanc"},
          {"f": "rect", "de": [0, H - hl], "a": [W, H], "couleur": "jaune", "remplir": "jaune"}]
    for i in range(1, n):
        el.append({"f": "ligne", "pts": [[0, H - i * hl], [W, H - i * hl]], "couleur": "faible"})
    x = 0
    for w in L[:-1]:
        x += w; el.append({"f": "ligne", "pts": [[x, 0], [x, H]], "couleur": "faible"})
    for r, ligne in enumerate([ent] + lignes):
        x = 0
        for c, (t, w) in enumerate(zip(ligne, L)):
            el.append({"f": "texte", "at": [round(x + w / 2, 3), round(H - (r + 0.5) * hl, 3)], "t": t, "taille": "petit",
                       "couleur": "jaune" if r == 0 else ("blanc" if c == 0 else ("rouge" if c == 1 else "cyan"))})
            x += w
    return {"type": "schema", "titre": "Document 2 : trois tubes, il manque un élément à chacun",
            "legende": "Mêmes mitochondries, même milieu tamponné ; mesures au bout de 10 min (« pyruvate » = acide pyruvique).",
            "cadre": {"l": W, "h": round(H, 2)}, "elements": el}


EX = {
  "id": "svt_ex_ch1_conditions_mitochondrie_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "reactions_responsables_liberation_energie", "cours": "svt_ch1_reactions_responsables_liberation_energie",
  "titre": "Des mitochondries isolées : à quelles conditions fabriquent-elles l'ATP ?", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Décrire des courbes par périodes puis déduire", "Calculer et comparer des vitesses de consommation de O₂",
                  "Dégager les conditions de la phosphorylation oxydative", "Expliquer le couplage entre la chaîne respiratoire et la synthèse d'ATP",
                  "Expliquer l'effet d'un inhibiteur maillon par maillon"],
  "enonce": {
    "intro": "Des mitochondries isolées de cellules de foie sont placées dans un milieu tamponné riche en dioxygène qui contient déjà de l'acide pyruvique en quantité suffisante. Des sondes mesurent la concentration du dioxygène [O₂] (en % de sa valeur initiale) et la concentration de l'ATP (en unités arbitraires, UA). À t = 3 min, on ajoute de l'ADP et du phosphate inorganique (ADP + Pi) ; à t = 7 min, on ajoute du cyanure (document 1). Dans une seconde série, trois tubes contiennent les mêmes mitochondries, mais il manque à chacun un élément ; les mesures sont faites au bout de 10 min (document 2).",
    "intro_dit": "دابا نقراو l'énoncé. عندنا des mitochondries ديال le foie، فmilieu فيه le dioxygène، وفيه déjà l'acide pyruvique. كنقيسو le dioxygène بالpourcentage، و l'ATP. après trois minutes، زدنا ADP و phosphate. و après sept minutes، زدنا le cyanure. هادا le document un. وفle document deux، trois tubes، وفكل tube كاينة حاجة ناقصة. قسنا après dix minutes.",
    "figures": [doc1(3, 7, 97, 49, 8, 80), doc2(8, 90)],
    "donnees": ["Document 1 : à t = 0 : [O₂] = 100 %, ATP = 8 UA ; à t = 3 min : [O₂] = 97 % ; à t = 7 min : [O₂] = 49 %, ATP = 80 UA",
                "Après le cyanure (t > 7 min) : [O₂] reste à 49 % et l'ATP à 80 UA",
                "Le cyanure se fixe sur le dernier transporteur de la chaîne respiratoire et bloque le transfert des électrons vers le dioxygène."],
    "questions": [
      {"id": "1", "texte": "Décrire l'évolution de [O₂] et de la concentration de l'ATP dans le document 1, période par période, puis déduire.",
       "texte_dit": "la question un: وصف l'évolution ديال le dioxygène و l'ATP فle document un، période par période، ومن بعد استنتج.",
       "reponse": {"type": "phrase", "attendu": "De 0 à 3 min (acide pyruvique seul) : [O₂] diminue lentement, de 100 à 97 % ; l'ATP reste stable à 8 UA. De 3 à 7 min (après l'ajout d'ADP + Pi) : [O₂] diminue rapidement, de 97 à 49 %, et l'ATP augmente de 8 à 80 UA. Après 7 min (cyanure) : [O₂] reste stable à 49 % et l'ATP reste stable à 80 UA. On en déduit que les mitochondries ne produisent de l'ATP qu'en présence d'ADP + Pi, que cette production s'accompagne d'une forte consommation de O₂, et que le cyanure arrête en même temps la consommation de O₂ et la synthèse d'ATP."},
       "clavier": {"aides": ["De 0 à 3 min", "diminue lentement", "diminue rapidement", "augmente", "reste stable", "%", "UA", "On en déduit que"], "pieges": ["[O₂] augmente", "l'ATP diminue"]},
       "aides": [
         {"texte": "Les ajouts découpent le temps en trois périodes : 0–3 min, 3–7 min, après 7 min. Lis les deux courbes dans chaque période.",
          "dit": "les ajouts كيقسمو le temps، en trois périodes: de zéro à trois minutes، de trois à sept minutes، و après sept minutes. فكل période، قرا les deux courbes."},
         {"texte": "Une ligne par période : le sens (diminue, augmente, stable), la vitesse (lentement, rapidement) et les valeurs lues. Puis une phrase « On en déduit que ».",
          "dit": "une ligne par période: واش كتنقص، ولا كتزاد، ولا stable، بشوية ولا بالزربة، مع les valeurs. ومن بعد جملة: on en déduit que."}],
       "correction": {"lignes": [
           {"texte": "1 : de 0 à 3 min : [O₂] diminue lentement (100 → 97 %) ; ATP stable à 8 UA", "mot": "كينقص بشوية"},
           {"texte": "de 3 à 7 min (ADP + Pi) : [O₂] diminue rapidement (97 → 49 %) ; ATP augmente (8 → 80 UA)", "mot": "كينقص بالزربة"},
           {"texte": "après 7 min (cyanure) : [O₂] stable à 49 % ; ATP stable à 80 UA", "mot": "les deux stables"},
           {"texte": "on en déduit : ATP produit seulement avec ADP + Pi, avec forte consommation de O₂ ; le cyanure arrête les deux", "mot": "on en déduit que"}],
         "parole": "la question un. de zéro à trois minutes، le dioxygène كينقص بشوية، de cent à quatre-vingt-dix-sept pour cent، و l'ATP stable، à huit unités arbitraires. de trois à sept minutes، après ADP et phosphate، le dioxygène كينقص بالزربة، de quatre-vingt-dix-sept à quarante-neuf pour cent، و l'ATP كيطلع، de huit à quatre-vingts. après sept minutes، avec le cyanure، le dioxygène و l'ATP، les deux stables: quarante-neuf pour cent، et quatre-vingts. on en déduit que la mitochondrie كتصاوب l'ATP غير ملي كاين ADP و phosphate، وكتستهلك بزاف ديال le dioxygène، و le cyanure كيوقف les deux، فنفس الوقت."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Calculer la vitesse moyenne de consommation du dioxygène v₁ entre 0 et 3 min, puis v₂ entre 3 et 7 min (en % par min). En déduire le rapport v₂/v₁.",
       "texte_dit": "la question deux: حسب la vitesse moyenne ديال la consommation ديال le dioxygène، v un، entre zéro et trois minutes، و v deux، entre trois et sept minutes. ومن بعد حسب le rapport، v deux sur v un.",
       "reponse": {"type": "valeur", "grandeur": "v₂/v₁", "valeur": 12, "unite": "", "tolerance": 0.02,
                   "attendu": "v₁ = (100 − 97)/3 = 1 %/min ; v₂ = (97 − 49)/(7 − 3) = 12 %/min ; v₂/v₁ = 12/1 = 12"},
       "clavier": {"aides": ["v = Δ[O₂]/Δt", "(100 − 97)/3", "(97 − 49)/4", "%/min", "v₂/v₁"], "pieges": ["49/7", "97/3"]},
       "aides": [
         {"texte": "La vitesse de consommation, c'est la baisse de [O₂] divisée par la durée de la période.",
          "dit": "la vitesse ديال la consommation: شحال نقص le dioxygène، مقسوم على la durée ديال la période."},
         {"texte": "v₁ : de 100 à 97 % en 3 min ; v₂ : de 97 à 49 % en 4 min. Puis divise v₂ par v₁.",
          "dit": "v un: de cent à quatre-vingt-dix-sept pour cent، en trois minutes. v deux: de quatre-vingt-dix-sept à quarante-neuf، en quatre minutes. ومن بعد قسم v deux، sur v un."}],
       "correction": {"lignes": [
           {"texte": "2 : v₁ = (100 − 97)/3 = 1 %/min", "mot": "v un égale"},
           {"texte": "v₂ = (97 − 49)/(7 − 3) = 48/4 = 12 %/min", "mot": "v deux égale"},
           {"texte": "v₂/v₁ = 12 : avec ADP + Pi, O₂ est consommé 12 fois plus vite", "mot": "douze fois plus vite"}],
         "parole": "la question deux. v un égale cent moins quatre-vingt-dix-sept، sur trois، égale un pour cent par minute. v deux égale quatre-vingt-dix-sept moins quarante-neuf، sur quatre، égale douze pour cent par minute. le rapport، v deux sur v un، égale douze. إذن مع ADP et phosphate، le dioxygène كيتستهلك، douze fois plus vite."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "En exploitant les documents 1 et 2, dégager les conditions nécessaires à la synthèse d'ATP par les mitochondries. Justifier chaque condition par une donnée.",
       "texte_dit": "la question trois: استغل le document un و le document deux، وعطي les conditions اللي خاصهم باش la mitochondrie تصاوب l'ATP. وبرر كل condition بdonnée.",
       "reponse": {"type": "phrase", "attendu": "Tube A : sans O₂, l'ATP reste à 8 UA : le dioxygène est nécessaire. Tube B : sans acide pyruvique, ni O₂ consommé (100 %) ni ATP produit : un substrat oxydable, l'acide pyruvique, est nécessaire. Tube C et document 1 avant 3 min : sans ADP + Pi, l'ATP reste à 8 UA et O₂ est peu consommé : ADP + Pi sont nécessaires. Document 1 après 7 min : le cyanure, qui bloque la chaîne respiratoire, arrête la synthèse d'ATP : la chaîne respiratoire doit fonctionner. Donc la synthèse d'ATP par les mitochondries exige : de l'acide pyruvique, du dioxygène, de l'ADP + Pi et une chaîne respiratoire fonctionnelle."},
       "clavier": {"aides": ["acide pyruvique", "O₂", "ADP + Pi", "chaîne respiratoire", "tube A", "tube B", "tube C", "donc"], "pieges": ["glucose", "lumière"]},
       "aides": [
         {"texte": "Pour chaque tube, regarde ce qui manque et si l'ATP a augmenté : ce qui manque quand l'ATP ne bouge pas est une condition.",
          "dit": "فكل tube، شوف شنو ناقص، وواش l'ATP طلع. يلا l'ATP ما تحركش، داك الشي اللي ناقص هو condition."},
         {"texte": "Ajoute ce que montre le cyanure (document 1, après 7 min) : quelle structure doit fonctionner ?",
          "dit": "وزيد شنو كيبين le cyanure، après sept minutes: شمن structure خاصها تخدم؟"}],
       "correction": {"lignes": [
           {"texte": "3 : tube A (sans O₂) : ATP stable à 8 UA : O₂ nécessaire", "mot": "le dioxygène ضروري"},
           {"texte": "tube B (sans acide pyruvique) : O₂ à 100 %, ATP à 8 UA : substrat nécessaire", "mot": "l'acide pyruvique ضروري"},
           {"texte": "tube C et 0–3 min (sans ADP + Pi) : ATP à 8 UA : ADP + Pi nécessaires", "mot": "ADP et phosphate ضروريين"},
           {"texte": "cyanure : ATP stoppé : chaîne respiratoire fonctionnelle nécessaire", "mot": "la chaîne respiratoire خاصها تخدم"}],
         "parole": "la question trois. le tube A، بلا dioxygène، l'ATP بقا à huit: إذن le dioxygène ضروري. le tube B، بلا acide pyruvique، le dioxygène بقا à cent pour cent، و l'ATP huit: إذن l'acide pyruvique ضروري. le tube C، بلا ADP و phosphate، l'ATP ما طلعش: إذن ADP et phosphate ضروريين. و le cyanure كيوقف l'ATP: إذن la chaîne respiratoire خاصها تخدم."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Expliquer, en vous appuyant sur vos connaissances, pourquoi la consommation du dioxygène et la synthèse d'ATP se font ensemble entre 3 et 7 min (couplage).",
       "texte_dit": "la question quatre: فسر بالمعلومات ديالك، علاش la consommation ديال le dioxygène و la synthèse ديال l'ATP كيوقعو مع بعض، entre trois et sept minutes. هادا هو le couplage.",
       "reponse": {"type": "phrase", "attendu": "L'oxydation de l'acide pyruvique dans la matrice réduit les transporteurs (NADH,H⁺, FADH₂). Dans la membrane interne, la chaîne respiratoire les réoxyde : les électrons passent de transporteur en transporteur jusqu'au dioxygène, accepteur final, qui est réduit en eau : c'est la consommation de O₂. Ce transfert d'électrons permet le pompage des H⁺ de la matrice vers l'espace intermembranaire, ce qui crée un gradient de H⁺. Les H⁺ reviennent vers la matrice par les sphères pédonculées (ATP synthase), ce qui fournit l'énergie de la phosphorylation de l'ADP : ADP + Pi → ATP. Consommer O₂ et produire l'ATP sont donc deux étapes liées d'un même processus, la phosphorylation oxydative."},
       "clavier": {"aides": ["NADH,H⁺", "chaîne respiratoire", "accepteur final", "½ O₂ + 2 H⁺ + 2 e⁻ → H₂O", "gradient de H⁺", "sphère pédonculée", "ADP + Pi → ATP"], "pieges": ["les H⁺ sont pompés vers la matrice", "le CO₂ vient du O₂"]},
       "aides": [
         {"texte": "Suis les électrons : d'où viennent-ils (transporteurs réduits), où finissent-ils (O₂) ? Puis suis les H⁺ : où sont-ils pompés, par où reviennent-ils ?",
          "dit": "تبع les électrons: منين جاو، ولفين كيوصلو؟ ومن بعد تبع les protons: لفين كيتطلعو، ومن فين كيرجعو؟"},
         {"texte": "Écris la chaîne en flèches, un maillon par flèche : transporteurs réduits → chaîne → O₂ réduit en eau ; H⁺ pompés → gradient → retour par les sphères → ATP.",
          "dit": "كتب السلسلة بles flèches، maillon par maillon: les transporteurs réduits، la chaîne، le dioxygène كيولي l'eau. les protons كيتطلعو، le gradient، كيرجعو من les sphères، l'ATP."}],
       "correction": {"lignes": [
           {"texte": "4 : acide pyruvique oxydé dans la matrice → NADH,H⁺, FADH₂", "mot": "فla matrice"},
           {"texte": "chaîne respiratoire : électrons jusqu'au O₂ (accepteur final) → H₂O : O₂ consommé", "mot": "l'accepteur final"},
           {"texte": "transfert des e⁻ → H⁺ pompés de la matrice vers l'espace intermembranaire → gradient", "mot": "كيتكون le gradient"},
           {"texte": "retour des H⁺ par les sphères pédonculées → ADP + Pi → ATP : couplage (phosphorylation oxydative)", "mot": "كيتكون l'ATP"}],
         "parole": "la question quatre. l'acide pyruvique كيتأكسد فla matrice، وكيعطي N A D H, H plus، et F A D H deux. فla membrane interne، la chaîne respiratoire كتاخد منهم les électrons، وكتدوزهم حتى لle dioxygène، l'accepteur final، اللي كيولي l'eau: هادي هي la consommation ديال le dioxygène. هاد الدوران ديال les électrons كيطلع les protons من la matrice لl'espace intermembranaire: كيتكون le gradient. les protons كيرجعو لla matrice من les sphères pédonculées، وتما كيتكون l'ATP، من ADP et phosphate. إذن les deux مرتبطين: هادي la phosphorylation oxydative."},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "Sachant que le cyanure bloque le transfert des électrons vers le dioxygène, expliquer les résultats obtenus après t = 7 min.",
       "texte_dit": "la question cinq: le cyanure كيسد le transfert ديال les électrons لle dioxygène. فسر les résultats après sept minutes.",
       "reponse": {"type": "phrase", "attendu": "Le cyanure bloque le transfert des électrons vers le dioxygène → O₂ n'est plus réduit en eau, il n'est plus consommé : [O₂] reste à 49 % → la chaîne respiratoire ne pompe plus de H⁺ de la matrice vers l'espace intermembranaire → plus de gradient de H⁺ → plus de retour des H⁺ par les sphères pédonculées → plus de phosphorylation de l'ADP : l'ATP n'augmente plus et reste à 80 UA."},
       "clavier": {"aides": ["→", "O₂ non consommé", "pas de pompage des H⁺", "pas de gradient", "sphères pédonculées", "pas d'ATP", "49 %", "80 UA"], "pieges": ["l'ATP est détruit", "O₂ consommé plus vite"]},
       "aides": [
         {"texte": "Pars du maillon touché (le dernier transporteur) et demande-toi à chaque étape ce qui ne peut plus se faire.",
          "dit": "بدا من le maillon اللي تسد، وفكل étape، سول راسك شنو ما بقاش يمكن يوقع."},
         {"texte": "Déroule la chaîne en flèches jusqu'à l'ATP, et cite les valeurs du document 1 (49 % et 80 UA).",
          "dit": "كتب السلسلة بles flèches حتى l'ATP، وعطي les valeurs ديال le document un: quarante-neuf pour cent، et quatre-vingts."}],
       "correction": {"lignes": [
           {"texte": "5 : cyanure → transfert des e⁻ bloqué → O₂ non réduit, non consommé ([O₂] stable à 49 %)", "mot": "le dioxygène ما بقاش كيتستهلك"},
           {"texte": "→ pas de pompage des H⁺ → pas de gradient de H⁺", "mot": "ما كاينش le gradient"},
           {"texte": "→ pas de retour des H⁺ par les sphères → pas de phosphorylation de l'ADP (ATP stable à 80 UA)", "mot": "ما بقاش كيتكون l'ATP"}],
         "parole": "la question cinq. le cyanure كيسد le transfert ديال les électrons. إذن le dioxygène ما بقاش كيولي l'eau، و le dioxygène ما بقاش كيتستهلك: il reste à quarante-neuf pour cent. la chaîne ما بقاتش كتطلع les protons، إذن ما كاينش le gradient. les protons ما كيرجعوش من les sphères، و ما بقاش كيتكون l'ATP: il reste à quatre-vingts unités arbitraires."},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : décrire période par période",
     "screen_content": {"lead": "Acide pyruvique seul : O₂ baisse peu, ATP stable. ADP + Pi : O₂ baisse vite, ATP monte. Cyanure : tout s'arrête."},
     "visual": {"kind": "simulation", "url": EXAO_PYR, "caption": "Mitochondries isolées : [O₂] et ATP en direct"},
     "speech_text": {"mixed": "شوف هاد l'expérience: des mitochondries، فmilieu فيه le dioxygène. ملي كاين l'acide pyruvique بوحدو، le dioxygène كينقص بشوية، و l'ATP stable. دابا زدنا ADP و phosphate. شوف les deux courbes: le dioxygène كينقص بالزربة، و l'ATP كيطلع، فنفس الوقت. فاللخر le cyanure: le dioxygène و l'ATP كيوليو stables. فالامتحان: une ligne par période، مع les valeurs، ومن بعد: on en déduit que. وفl'exercice، les valeurs مكتوبين حدا la simulation."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "0 à 3 min : [O₂] 100 → 97 % (lentement) ; ATP stable à 8 UA", "mot": "le dioxygène كينقص بشوية"},
                  {"texte": "3 à 7 min (ADP + Pi) : [O₂] 97 → 49 % (rapidement) ; ATP 8 → 80 UA", "mot": "le dioxygène كينقص بالزربة"},
                  {"texte": "après 7 min (cyanure) : [O₂] stable à 49 % ; ATP stable à 80 UA", "mot": "كيوليو stables"}],
       "pointage": [{"mot": "des mitochondries، فmilieu", "repere": "mitochondries"},
                    {"mot": "ملي كاين l'acide pyruvique بوحدو", "commande": "play_until", "parametres": {"moment": "ajout_pyruvate", "duree_s": 1.6}},
                    {"mot": "le dioxygène كينقص بشوية", "repere": "courbe_o2"},
                    {"mot": "le dioxygène كينقص بشوية", "cible": "centre:0"},
                    {"mot": "دابا زدنا ADP", "commande": "play_until", "parametres": {"moment": "ajout_adp_pi"}},
                    {"mot": "شوف les deux courbes", "commande": "play_until", "parametres": {"moment": "o2_baisse_atp_monte", "duree_s": 2.6}},
                    {"mot": "le dioxygène كينقص بالزربة", "cible": "centre:1"},
                    {"mot": "و l'ATP كيطلع", "repere": "courbe_atp"},
                    {"mot": "فاللخر le cyanure", "commande": "play_until", "parametres": {"moment": "palier_final", "duree_s": 1.6}},
                    {"mot": "كيوليو stables", "cible": "centre:2"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : la vitesse, c'est la pente",
     "screen_content": {"lead": "v = baisse de [O₂] / durée ; après ADP + Pi, la pente est bien plus forte."},
     "visual": {"kind": "simulation", "url": EXAO_PENTE, "caption": "Les deux pentes de la courbe de [O₂]"},
     "speech_text": {"mixed": "la vitesse ديال la consommation هي la pente: شحال نقص le dioxygène، مقسوم على la durée. قبل ADP و phosphate، la pente صغيرة: le dioxygène كينقص بشوية. من بعد ADP و phosphate، la pente كبيرة بزاف. le rapport، v deux sur v un، كيقول شحال من مرة la consommation زربات. وفl'exercice: v un، un pour cent par minute. v deux، douze pour cent par minute. le rapport égale douze."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "v₁ = (100 − 97)/3 = 1 %/min", "mot": "v un، un pour cent"},
                  {"texte": "v₂ = (97 − 49)/(7 − 3) = 12 %/min", "mot": "v deux، douze pour cent"},
                  {"texte": "v₂/v₁ = 12/1 = 12", "mot": "le rapport égale douze"}],
       "pointage": [{"mot": "la vitesse ديال la consommation هي la pente", "repere": "courbe_o2"},
                    {"mot": "قبل ADP و phosphate", "repere": "periode_pyruvate"},
                    {"mot": "من بعد ADP و phosphate، la pente", "commande": "play_until", "parametres": {"moment": "o2_baisse_atp_monte", "duree_s": 2.6}},
                    {"mot": "la pente كبيرة بزاف", "repere": "periode_adp"},
                    {"mot": "v un، un pour cent", "cible": "centre:0"},
                    {"mot": "v deux، douze pour cent", "cible": "centre:1"},
                    {"mot": "le rapport égale douze", "cible": "centre:2"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : ce qui manque, et ce qui ne se fait plus",
     "screen_content": {"lead": "Conditions : acide pyruvique, O₂, ADP + Pi, chaîne respiratoire fonctionnelle."},
     "visual": {"kind": "simulation", "url": EXAO_0, "caption": "Les mêmes ajouts, dans un milieu sans dioxygène"},
     "speech_text": {"mixed": "نشوفو نفس l'expérience، ولكن بلا dioxygène. شوف: كنزيدو l'acide pyruvique، و ADP و phosphate، و l'ATP بقا stable. إذن le dioxygène ضروري: هادا هو le tube A. فle tube B، ماكاينش l'acide pyruvique: حتى هو ضروري. فle tube C، ماكاينش ADP و phosphate: l'ATP ما يمكنش يتكون. وملي le cyanure كيوقف la chaîne respiratoire، كيوقف l'ATP. donc quatre conditions."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "tube A (sans O₂) : ATP 8 UA → O₂ nécessaire", "mot": "هادا هو le tube A"},
                  {"texte": "tube B (sans acide pyruvique) : O₂ 100 %, ATP 8 UA → substrat nécessaire", "mot": "حتى هو ضروري"},
                  {"texte": "tube C (sans ADP + Pi) : ATP 8 UA → ADP + Pi nécessaires", "mot": "l'ATP ما يمكنش يتكون"},
                  {"texte": "cyanure : chaîne respiratoire bloquée → pas d'ATP", "mot": "كيوقف l'ATP"}],
       "pointage": [{"mot": "ولكن بلا dioxygène", "commande": "set_parameters", "parametres": {"sans_o2": True}},
                    {"mot": "شوف: كنزيدو", "commande": "play_until", "parametres": {"moment": "palier_final", "duree_s": 3}},
                    {"mot": "و l'ATP بقا stable", "repere": "courbe_atp"},
                    {"mot": "هادا هو le tube A", "cible": "centre:0"},
                    {"mot": "حتى هو ضروري", "cible": "centre:1"},
                    {"mot": "l'ATP ما يمكنش يتكون", "cible": "centre:2"},
                    {"mot": "كيوقف l'ATP", "cible": "centre:3"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : le couplage, maillon par maillon",
     "screen_content": {"lead": "Électrons jusqu'au O₂ (consommé) ; H⁺ pompés, puis retour par la sphère : ATP."},
     "visual": {"kind": "simulation", "url": CHAINE, "caption": "La chaîne respiratoire et la sphère pédonculée"},
     "speech_text": {"mixed": "دابا نفهمو الرابط. N A D H, H plus، اللي جا من l'acide pyruvique فla matrice، كيوصل لla chaîne respiratoire. كيعطي les électrons. les électrons كيدوزو من transporteur ل transporteur، حتى لle dioxygène. le dioxygène كياخدهم، وكيولي l'eau: هادي هي la consommation ديال le dioxygène. فنفس الوقت، la chaîne كتطلع les protons من la matrice لl'espace intermembranaire. كيتكون le gradient. les protons كيرجعو غير من la sphère pédonculée، وتما كيتكون l'ATP. إذن la consommation ديال le dioxygène و la synthèse ديال l'ATP مرتبطين: هادا هو le couplage."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "NADH,H⁺ → chaîne → e⁻ → O₂ réduit en H₂O (O₂ consommé)", "mot": "وكيولي l'eau"},
                  {"texte": "H⁺ pompés (matrice → espace intermembranaire) → gradient → sphère pédonculée → ADP + Pi → ATP", "mot": "وتما كيتكون l'ATP"}],
       "pointage": [{"mot": "كيوصل لla chaîne respiratoire", "commande": "play_until", "parametres": {"moment": "taxi_arrive", "duree_s": 1.2}},
                    {"mot": "كيعطي les électrons", "commande": "play_until", "parametres": {"moment": "taxi_decharge"}},
                    {"mot": "les électrons كيدوزو", "commande": "play_until", "parametres": {"moment": "electrons_passent", "duree_s": 2.4}},
                    {"mot": "le dioxygène كياخدهم", "commande": "play_until", "parametres": {"moment": "o2_recoit"}},
                    {"mot": "وكيولي l'eau", "commande": "play_until", "parametres": {"moment": "eau_formee"}},
                    {"mot": "وكيولي l'eau", "cible": "centre:0"},
                    {"mot": "la chaîne كتطلع les protons", "commande": "play_until", "parametres": {"moment": "protons_pompes", "duree_s": 2.4}},
                    {"mot": "كيتكون le gradient", "commande": "play_until", "parametres": {"moment": "gradient_ecrit"}},
                    {"mot": "les protons كيرجعو", "commande": "play_until", "parametres": {"moment": "retour_par_la_sphere", "duree_s": 1.6}},
                    {"mot": "وتما كيتكون l'ATP", "commande": "play_until", "parametres": {"moment": "atp_forme"}},
                    {"mot": "وتما كيتكون l'ATP", "cible": "centre:1"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : le cyanure arrête toute la chaîne",
     "screen_content": {"lead": "Transfert des e⁻ bloqué → O₂ non consommé → pas de pompage → pas de gradient → pas d'ATP."},
     "visual": {"kind": "simulation", "url": CYAN, "caption": "Le cyanure sur la chaîne respiratoire"},
     "speech_text": {"mixed": "دابا le cyanure. شوف: كيتحط على اللخر ديال la chaîne. les électrons ما بقاوش كيدوزو. le dioxygène ما بقاش كياخدهم: ما بقاش كيتستهلك. ما بقاش le pompage ديال les protons. ما كاينش le gradient. إذن ما كاينش l'ATP. وهادشي اللي فle document: le dioxygène stable، و l'ATP stable، من بعد le cyanure."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "cyanure → e⁻ bloqués → O₂ non consommé ([O₂] stable à 49 %)", "mot": "ما بقاش كيتستهلك"},
                  {"texte": "→ pas de pompage → pas de gradient → pas d'ATP (stable à 80 UA)", "mot": "إذن ما كاينش l'ATP"}],
       "pointage": [{"mot": "شوف: كيتحط", "commande": "play_until", "parametres": {"moment": "cyanure_pose"}},
                    {"mot": "les électrons ما بقاوش كيدوزو", "commande": "play_until", "parametres": {"moment": "bloque", "duree_s": 2.4}},
                    {"mot": "le dioxygène ما بقاش كياخدهم", "commande": "play_until", "parametres": {"moment": "o2_non"}},
                    {"mot": "ما بقاش كيتستهلك", "cible": "centre:0"},
                    {"mot": "ما بقاش le pompage", "commande": "play_until", "parametres": {"moment": "pas_pompage"}},
                    {"mot": "ما كاينش le gradient", "commande": "play_until", "parametres": {"moment": "pas_gradient"}},
                    {"mot": "إذن ما كاينش l'ATP", "commande": "play_until", "parametres": {"moment": "pas_d_atp"}},
                    {"mot": "إذن ما كاينش l'ATP", "cible": "centre:1"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : après l'ajout d'ADP + Pi", "سؤال ساهل على les courbes.",
      "Entre 3 et 7 min (après l'ajout d'ADP + Pi)…", ["[O₂] diminue rapidement et l'ATP augmente", "[O₂] augmente et l'ATP diminue", "[O₂] reste stable et l'ATP augmente"], 0, {
        "0": {"juste": rep("برافو! le dioxygène كينقص بالزربة، و l'ATP كيطلع، فنفس الوقت.", "Juste : [O₂] diminue rapidement (97 → 49 %) et l'ATP augmente (8 → 80 UA).")},
        "1": {"1": rep("ما تقلقش. شوف la courbe ديال le dioxygène من بعد ADP و phosphate: كتطلع ولا كتهبط؟ عاود اختار.", "Regarde la courbe de [O₂] après ADP + Pi : monte-t-elle ou descend-elle ? Réessaie."),
              "2": rep("الجواب: le dioxygène كينقص بالزربة، و l'ATP كيطلع. قلبتي الاتجاه.", "Réponse : [O₂] diminue rapidement et l'ATP augmente ; tu as inversé les sens.")},
        "2": {"1": rep("قريب! l'ATP كيطلع، صحيح. ولكن le dioxygène، واش بقا stable؟ عاود اختار.", "L'ATP augmente, c'est juste. Mais [O₂] reste-t-elle stable ? Réessaie."),
              "2": rep("الجواب: le dioxygène كينقص بالزربة. stable غير من بعد le cyanure.", "Réponse : [O₂] diminue rapidement ; elle n'est stable qu'après le cyanure.")}},
      "Entre trois et sept minutes, après l'ajout d'ADP et de phosphate ?"),
    qcm_facile("fa_s2", "Plus facile : comparer les deux vitesses", "سؤال ساهل: قارن les deux vitesses.",
      "v₁ = 1 %/min avant ADP + Pi et v₂ = 12 %/min après. Après l'ajout, la consommation de O₂ est…", ["12 fois plus rapide", "12 fois plus lente", "la même"], 0, {
        "0": {"juste": rep("برافو! douze sur un، égale douze: douze fois plus rapide.", "Juste : v₂/v₁ = 12/1 = 12 : douze fois plus rapide.")},
        "1": {"1": rep("ما تقلقش. v deux كبر من v un ولا صغر؟ عاود اختار.", "v₂ est-elle plus grande ou plus petite que v₁ ? Réessaie."),
              "2": rep("الجواب: douze fois plus rapide، حيت v deux كبر بزاف من v un.", "Réponse : 12 fois plus rapide (v₂ > v₁).")},
        "2": {"1": rep("قريب! douze n'est pas égal à un. واش la pente تبدلات؟ عاود اختار.", "12 n'est pas égal à 1 : la pente a-t-elle changé ? Réessaie."),
              "2": rep("الجواب: douze fois plus rapide. la pente ولات كبيرة من بعد ADP و phosphate.", "Réponse : 12 fois plus rapide ; la pente devient forte après ADP + Pi.")}},
      "Après l'ajout d'ADP et de phosphate, la consommation du dioxygène est ?"),
    association("fa_s3", "Plus facile : chaque tube et sa condition", "Relie chaque résultat à la condition qu'il montre.",
      "سؤال ساهل: ربط كل tube مع la condition اللي كيبين.", "Relie chaque résultat à la condition qu'il démontre.",
      [("1", "Tube A : sans O₂, ATP stable à 8 UA"), ("2", "Tube B : sans acide pyruvique, O₂ à 100 %, ATP à 8 UA"), ("3", "Tube C : sans ADP + Pi, ATP à 8 UA")],
      [("a", "Le dioxygène est nécessaire (accepteur final des électrons)"), ("b", "Un substrat oxydable est nécessaire (acide pyruvique)"), ("c", "ADP + Pi sont nécessaires (ils sont phosphorylés en ATP)")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : sans O₂, accepteur final, la chaîne ne fonctionne pas : pas d'ATP.", "برافو: بلا dioxygène، la chaîne ما كتخدمش، و ماكاينش l'ATP."),
       "1-b": (False, "Non : dans le tube A, l'acide pyruvique est présent. Qu'est-ce qui manque ?", "لا، فle tube A كاين l'acide pyruvique. شنو ناقص؟"),
       "1-c": (False, "Non : dans le tube A, ADP + Pi sont présents. Qu'est-ce qui manque ?", "لا، فle tube A كاين ADP و phosphate. شنو ناقص؟"),
       "2-a": (False, "Non : le tube B a du dioxygène (100 %). Qu'est-ce qui manque ?", "لا، فle tube B كاين le dioxygène. شنو ناقص؟"),
       "2-b": (True, "Oui : sans acide pyruvique, pas de transporteurs réduits : ni O₂ consommé ni ATP.", "برافو: بلا acide pyruvique، ماكاين لا dioxygène مستهلك، لا ATP."),
       "2-c": (False, "Non : le tube B a ADP + Pi. Qu'est-ce qui manque ?", "لا، فle tube B كاين ADP و phosphate. شنو ناقص؟"),
       "3-a": (False, "Non : le tube C a du dioxygène. Qu'est-ce qui manque ?", "لا، فle tube C كاين le dioxygène. شنو ناقص؟"),
       "3-b": (False, "Non : le tube C a de l'acide pyruvique. Qu'est-ce qui manque ?", "لا، فle tube C كاين l'acide pyruvique. شنو ناقص؟"),
       "3-c": (True, "Oui : sans ADP + Pi, il n'y a rien à phosphoryler : l'ATP ne peut pas se former.", "برافو: بلا ADP و phosphate، l'ATP ما يمكنش يتكون.")},
      ("Conditions : acide pyruvique, dioxygène, ADP + Pi, et une chaîne respiratoire qui fonctionne.",
       "les conditions: l'acide pyruvique، le dioxygène، ADP et phosphate، و la chaîne respiratoire اللي كتخدم.")),
    vrai_faux("fa_s4", "Plus facile : vrai ou faux sur le couplage", "Vrai ou faux ?", "نتمرنو بvrai ou faux على le couplage.", [
      ("Le dioxygène est l'accepteur final des électrons de la chaîne respiratoire.", True, "Vrai : il est réduit en eau, c'est la consommation de O₂."),
      ("La chaîne respiratoire pompe les H⁺ de l'espace intermembranaire vers la matrice.", False, "Faux : elle les pompe de la matrice vers l'espace intermembranaire ; ils reviennent par les sphères pédonculées."),
      ("L'ATP est synthétisé quand les H⁺ reviennent vers la matrice par les sphères pédonculées.", True, "Vrai : la sphère pédonculée est l'ATP synthase."),
      ("La consommation de O₂ et la synthèse d'ATP sont deux phénomènes indépendants.", False, "Faux : elles sont couplées : le transfert des électrons jusqu'au O₂ crée le gradient de H⁺ qui permet la synthèse d'ATP.")]),
    qcm_facile("fa_s5", "Plus facile : la chaîne des conséquences du cyanure", "سؤال ساهل على le cyanure.",
      "Le cyanure bloque le transfert des électrons vers O₂. Quelle suite de conséquences est juste ?",
      ["O₂ non consommé → pas de pompage des H⁺ → pas de gradient → pas d'ATP", "O₂ consommé plus vite → plus de gradient → plus d'ATP", "l'ATP est détruit → O₂ consommé normalement"], 0, {
        "0": {"juste": rep("برافو! les électrons ما بقاوش كيوصلو، le dioxygène ما كيتستهلكش، ما كاينش le gradient، و ما كاينش l'ATP.", "Juste : O₂ non consommé → pas de pompage → pas de gradient → pas d'ATP.")},
        "1": {"1": rep("ما تقلقش. يلا les électrons تسدو، واش le dioxygène غادي ياخدهم؟ عاود اختار.", "Si les électrons sont bloqués, peuvent-ils arriver au dioxygène ? Réessaie."),
              "2": rep("الجواب: le dioxygène ما بقاش كيتستهلك، وكلشي كيوقف حتى l'ATP. فle document، le dioxygène stable.", "Réponse : O₂ n'est plus consommé et tout s'arrête jusqu'à l'ATP ([O₂] reste stable).")},
        "2": {"1": rep("قريب! ولكن l'ATP ما تهرسش: بقا stable. و le dioxygène، واش كيتستهلك؟ عاود اختار.", "L'ATP n'est pas détruit, il reste stable. Et O₂ est-il encore consommé ? Réessaie."),
              "2": rep("الجواب: le dioxygène ما بقاش كيتستهلك، ما كاينش le pompage، ما كاينش le gradient، و ما كاينش l'ATP جديد.", "Réponse : O₂ non consommé → pas de pompage → pas de gradient → pas de nouvel ATP.")}},
      "Le cyanure bloque le transfert des électrons vers le dioxygène. Quelle suite de conséquences est juste ?")
  ]}]},
  "similaire": {
    "id": "svt_ex_ch1_conditions_mitochondrie_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même protocole avec une autre préparation de mitochondries (acide pyruvique présent dès t = 0) : ADP + Pi sont ajoutés à t = 2 min et le cyanure à t = 6 min (document 1). Le document 2 donne les trois tubes témoins, mesurés au bout de 10 min.",
      "intro_dit": "نفس l'expérience، بقيم أخرى. ADP و phosphate، après deux minutes. و le cyanure، après six minutes. و les tubes فle document deux.",
      "figures": [doc1(2, 6, 96, 48, 5, 70), doc2(5, 80)],
      "donnees": ["Document 1 : à t = 0 : [O₂] = 100 %, ATP = 5 UA ; à t = 2 min : [O₂] = 96 % ; à t = 6 min : [O₂] = 48 %, ATP = 70 UA",
                  "Après le cyanure (t > 6 min) : [O₂] reste à 48 % et l'ATP à 70 UA",
                  "Le cyanure bloque le transfert des électrons vers le dioxygène."],
      "questions": [
        {"id": "1", "texte": "Décrire l'évolution de [O₂] et de l'ATP, période par période, puis déduire.",
         "reponse": {"type": "phrase", "attendu": "De 0 à 2 min : [O₂] diminue lentement (100 → 96 %) ; ATP stable à 5 UA. De 2 à 6 min (ADP + Pi) : [O₂] diminue rapidement (96 → 48 %) ; ATP augmente (5 → 70 UA). Après 6 min (cyanure) : [O₂] stable à 48 %, ATP stable à 70 UA. Donc l'ATP n'est produit qu'avec ADP + Pi, avec une forte consommation de O₂ ; le cyanure arrête les deux."},
         "clavier": {"aides": ["diminue lentement", "diminue rapidement", "augmente", "reste stable", "On en déduit que"], "pieges": ["[O₂] augmente"]},
         "correction": {"lignes": [{"texte": "1 : 0–2 min : [O₂] 100 → 96 % (lentement), ATP 5 UA ; 2–6 min : [O₂] 96 → 48 % (rapidement), ATP 5 → 70 UA", "mot": "كينقص بالزربة"},
                                   {"texte": "après 6 min : [O₂] 48 %, ATP 70 UA (stables) ; on en déduit : ATP avec ADP + Pi, couplé à la consommation de O₂", "mot": "on en déduit que"}],
                        "parole": "de zéro à deux minutes، le dioxygène كينقص بشوية، و l'ATP stable. de deux à six minutes، le dioxygène كينقص بالزربة، de quatre-vingt-seize à quarante-huit pour cent، و l'ATP كيطلع، de cinq à soixante-dix. من بعد le cyanure، les deux stables. on en déduit que l'ATP كيتكون غير مع ADP et phosphate، مع بزاف ديال le dioxygène."}},
        {"id": "2", "texte": "Calculer v₁ (0 à 2 min) et v₂ (2 à 6 min) en % par min, puis le rapport v₂/v₁.",
         "reponse": {"type": "valeur", "grandeur": "v₂/v₁", "valeur": 6, "unite": "", "tolerance": 0.02, "attendu": "v₁ = (100 − 96)/2 = 2 %/min ; v₂ = (96 − 48)/(6 − 2) = 12 %/min ; v₂/v₁ = 12/2 = 6"},
         "clavier": {"aides": ["(100 − 96)/2", "(96 − 48)/4", "v₂/v₁"], "pieges": ["48/6"]},
         "correction": {"lignes": [{"texte": "2 : v₁ = 4/2 = 2 %/min ; v₂ = 48/4 = 12 %/min", "mot": "v deux égale douze"}, {"texte": "v₂/v₁ = 12/2 = 6", "mot": "le rapport égale six"}],
                        "parole": "v un égale quatre sur deux، égale deux pour cent par minute. v deux égale douze pour cent par minute. le rapport égale six."}},
        {"id": "3", "texte": "En exploitant les documents 1 et 2, dégager les conditions de la synthèse d'ATP par les mitochondries, en justifiant chacune.",
         "reponse": {"type": "phrase", "attendu": "Tube A (sans O₂) : ATP stable à 5 UA : O₂ nécessaire. Tube B (sans acide pyruvique) : O₂ à 100 %, ATP à 5 UA : substrat nécessaire. Tube C (sans ADP + Pi) : ATP à 5 UA : ADP + Pi nécessaires. Cyanure : synthèse arrêtée : chaîne respiratoire fonctionnelle nécessaire."},
         "clavier": {"aides": ["O₂", "acide pyruvique", "ADP + Pi", "chaîne respiratoire"], "pieges": ["glucose"]},
         "correction": {"lignes": [{"texte": "3 : A : O₂ nécessaire ; B : acide pyruvique nécessaire ; C : ADP + Pi nécessaires", "mot": "le dioxygène، l'acide pyruvique"},
                                   {"texte": "cyanure : chaîne respiratoire fonctionnelle nécessaire", "mot": "la chaîne respiratoire"}],
                        "parole": "les conditions: le dioxygène، l'acide pyruvique، ADP et phosphate، و la chaîne respiratoire اللي كتخدم."}},
        {"id": "4", "texte": "Expliquer pourquoi la consommation de O₂ et la synthèse d'ATP se font ensemble entre 2 et 6 min.",
         "reponse": {"type": "phrase", "attendu": "Les transporteurs réduits (NADH,H⁺, FADH₂) issus de l'acide pyruvique sont réoxydés par la chaîne respiratoire ; les électrons vont jusqu'au O₂, accepteur final, réduit en eau (O₂ consommé). Ce transfert pompe les H⁺ de la matrice vers l'espace intermembranaire (gradient) ; leur retour par les sphères pédonculées permet ADP + Pi → ATP. Les deux phénomènes sont couplés (phosphorylation oxydative)."},
         "clavier": {"aides": ["accepteur final", "gradient de H⁺", "sphère pédonculée", "ADP + Pi → ATP"], "pieges": ["vers la matrice"]},
         "correction": {"lignes": [{"texte": "4 : e⁻ jusqu'au O₂ (réduit en H₂O) → H⁺ pompés → gradient", "mot": "كيتكون le gradient"},
                                   {"texte": "retour des H⁺ par les sphères → ATP : couplage", "mot": "كيتكون l'ATP"}],
                        "parole": "les électrons كيمشيو حتى لle dioxygène، اللي كيولي l'eau. فنفس الوقت، les protons كيتطلعو: كيتكون le gradient. كيرجعو من les sphères pédonculées، وكيتكون l'ATP. هادا le couplage."}},
        {"id": "5", "texte": "Le cyanure bloquant le transfert des électrons vers O₂, expliquer les résultats après t = 6 min.",
         "reponse": {"type": "phrase", "attendu": "Transfert des électrons bloqué → O₂ non réduit, non consommé ([O₂] stable à 48 %) → pas de pompage des H⁺ → pas de gradient → pas de retour des H⁺ par les sphères → pas de phosphorylation de l'ADP (ATP stable à 70 UA)."},
         "clavier": {"aides": ["→", "pas de gradient", "48 %", "70 UA"], "pieges": ["l'ATP est détruit"]},
         "correction": {"lignes": [{"texte": "5 : e⁻ bloqués → O₂ non consommé (48 %) → pas de pompage → pas de gradient", "mot": "ما كاينش le gradient"},
                                   {"texte": "→ pas d'ATP formé (stable à 70 UA)", "mot": "ما كاينش l'ATP"}],
                        "parole": "les électrons تسدو، le dioxygène ما بقاش كيتستهلك، quarante-huit pour cent. ما كاينش le pompage، ما كاينش le gradient، إذن ما كاينش l'ATP جديد: soixante-dix."}}
      ]}}
}
ecrire(EX, sys.argv[1])
