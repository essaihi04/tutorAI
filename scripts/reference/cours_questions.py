"""Questions, observations, réactions préparées, blocs (cahier, retrouver, exercice) et compétences du cours de
référence SVT. Lu par construire_cours.py. Chaque réaction : (parole, ecrit) — la parole suit les règles de la voix
(darija simple, français pour les termes, les nombres et les formules en mots), l'écrit est en français, en notation.
"""


def R(p, e):
    return {"parole": p, "ecrit": e}


def qcm(prompt, options, correct, dit, juste, faux, **k):
    """faux : {index: ((parole 1, écrit 1), (parole 2, écrit 2))} — 1 = ce qui est juste + un indice, 2 = la réponse."""
    rep = {}
    for i in range(len(options)):
        if i == correct:
            rep[str(i)] = {"juste": R(*juste)}
        else:
            a, b = faux[i]
            rep[str(i)] = {"1": R(*a), "2": R(*b)}
    q = {"type": "qcm", "prompt": prompt, "options": options, "correct": correct, "timeout_seconds": 40,
         "enonce_dit": dit}
    q.update(k)
    return q, rep


# ───────────────────────── Questions des diapositives (une par bloc) ─────────────────────────

Q = {}

Q["rf_a1_equation_respi"] = qcm(
    "Dans l'expérience 1, après l'injection du glucose…",
    ["le dioxygène augmente et le CO₂ diminue", "le dioxygène diminue et le CO₂ augmente",
     "le dioxygène et le CO₂ restent stables"], 1,
    "سؤال: dans l'expérience un, après l'injection du glucose, que font le dioxygène, et le dioxyde de carbone ?",
    ("بالضبط! قريتي la courbe مزيان: le dioxygène كينقص حيت les levures كياخدو منو، و le dioxyde de carbone كيطلع حيت "
     "كيخرج منهم. هادي هي la respiration cellulaire.",
     "Exact : le dioxygène diminue (il est absorbé) et le CO₂ augmente (il est rejeté) : c'est la respiration cellulaire."),
    {0: (("عندك الحق أن les deux courbes تبدلو من بعد l'injection. ولكن شوف الاتجاه ديال كل وحدة: la courbe الحمرا "
          "ديال le dioxygène، واش طلعات ولا هبطات؟ عاود جرب.",
          "Les deux courbes changent bien après l'injection. Mais regarde le sens de chacune : la courbe rouge du "
          "dioxygène monte-t-elle ou descend-elle ? Réessaie."),
         ("قلبتي الاتجاه، وهادي كتوقع ل بزاف ديال التلاميذ. les levures كياخدو le dioxygène، إذن كينقص حتى ل zéro. "
          "وكيخرج منهم le dioxyde de carbone، إذن كيطلع.",
          "C'est l'inverse : les levures absorbent le dioxygène, qui diminue (5,3 → 0 mg/L), et rejettent du CO₂, "
          "qui augmente (0,16 → 0,31 mmol/L).")),
     2: (("صحيح أن les courbes كانو ثابتة، ولكن هادشي قبل l'injection. السؤال على من بعد. شوف شنو وقع ملي دخل le "
          "glucose، وعاود جرب.",
          "Les courbes sont stables, oui, mais avant l'injection. La question porte sur après : regarde ce qui "
          "change quand le glucose arrive. Réessaie."),
         ("خليني نوريك فين تلفنا: les courbes ثابتة غير قبل le glucose. من بعد l'injection، le dioxygène كينقص حتى ل "
          "zéro، و le dioxyde de carbone كيطلع.",
          "Stables seulement avant le glucose. Après l'injection, le dioxygène diminue jusqu'à 0 et le CO₂ augmente."))},
)

Q["rf_a1_equation_ferm"] = qcm(
    "Quel produit apparaît seulement quand il n'y a plus de dioxygène ?",
    ["Le dioxyde de carbone", "L'eau", "L'éthanol"], 2,
    "جاوبني على هادي: quel produit apparaît seulement, quand il n'y a plus de dioxygène ?",
    ("هادا هو! l'éthanol ما بان حتى تسالا le dioxygène. هو اللي كيبين لينا أن la levure كدير la fermentation "
     "alcoolique.",
     "Oui : l'éthanol n'apparaît qu'une fois le dioxygène épuisé. C'est lui qui prouve la fermentation alcoolique."),
    {0: (("الفكرة ديالك فيها حاجة صحيحة: le dioxyde de carbone كيخرج بلا dioxygène. ولكن كيخرج حتى ف la respiration. قلب "
          "على le produit اللي ما كانش من قبل.",
          "Le CO₂ est bien rejeté sans dioxygène, mais il l'est aussi pendant la respiration. Cherche le produit "
          "qui n'existait pas avant."),
         ("le dioxyde de carbone كاين ف جوج: ف la respiration و ف la fermentation. اللي كيبان غير بلا dioxygène هو "
          "l'éthanol: شوف la courbe ديالو، كتبدا من zéro.",
          "Le CO₂ est produit dans les deux cas. Seul l'éthanol apparaît uniquement sans dioxygène : sa courbe "
          "part de 0 après 190 s.")),
     1: (("l'eau شفناها ف l'équation ديال la respiration، وهادي ملاحظة مزيانة. ولكن la respiration كتحتاج le "
          "dioxygène. شوف l'équation ديال la fermentation: شنو فيها؟",
          "L'eau est un produit de la respiration, qui a besoin de dioxygène. Regarde l'équation de la "
          "fermentation : quels produits contient-elle ? Réessaie."),
         ("l'eau كتخرج ف la respiration، ماشي ف la fermentation. بلا dioxygène، le glucose كيعطي l'éthanol و le "
          "dioxyde de carbone. والجديد فيهم هو l'éthanol.",
          "L'eau est un produit de la respiration. Sans dioxygène, le glucose donne de l'éthanol et du CO₂ : le "
          "produit nouveau est l'éthanol."))},
)

Q["rf_a3_voyage1"] = qcm(
    "Quelle étape est commune à la respiration et à la fermentation ?",
    ["La dégradation de l'acide pyruvique dans la mitochondrie", "La production d'éthanol", "La glycolyse"], 2,
    "شوف la carte، وجاوب: quelle étape est commune, à la respiration et à la fermentation ?",
    ("زوين! la glycolyse كتوقع ف le hyaloplasme، مع le dioxygène وبلا dioxygène. هي البداية ديال جوج ديال الطرق.",
     "Très bien : la glycolyse se fait dans le hyaloplasme, avec ou sans dioxygène. C'est le début des deux voies."),
    {0: (("la mitochondrie كتخدم مزيان مع l'acide pyruvique، هادي صحيحة. ولكن غير مع le dioxygène. شوف la carte: "
          "أشمن مرحلة كاينة قبل ما تفرق الطريق؟",
          "La mitochondrie dégrade bien l'acide pyruvique, mais seulement avec dioxygène. Sur la carte, quelle "
          "étape vient avant que les routes se séparent ?"),
         ("la mitochondrie كتدخل غير ف la respiration. اللي كاين ف جوج هو اللي قبل l'acide pyruvique: la glycolyse، ف "
          "le hyaloplasme.",
          "La mitochondrie n'intervient que dans la respiration. L'étape commune est celle d'avant l'acide "
          "pyruvique : la glycolyse, dans le hyaloplasme.")),
     1: (("l'éthanol كيبان بصح، ولكن غير بلا dioxygène. السؤال على حاجة كاينة ف جوج. رجع ل البداية ديال la carte.",
          "L'éthanol est bien produit, mais seulement sans dioxygène. On cherche ce qui existe dans les deux cas : "
          "reviens au début de la carte."),
         ("l'éthanol هو اللخر ديال la fermentation بوحدها. المرحلة اللي كاينة ف جوج هي la glycolyse: le glucose كيولي "
          "deux acides pyruviques.",
          "L'éthanol est la fin de la fermentation seule. L'étape commune est la glycolyse : le glucose devient "
          "deux acides pyruviques."))},
)

Q["rf_g0_taxi"] = qcm(
    "Le transporteur NAD⁺ prend deux hydrogènes. Il devient…",
    ["NADH,H⁺ : il est réduit", "NADH,H⁺ : il est vide", "de l'ATP"], 0,
    "دابا نتا: le transporteur N A D plus prend deux hydrogènes. Que devient-il ?",
    ("صافي، هادي فهمتيها: الطاكسي هز deux hydrogènes، وولا N A D H, H plus. عامر، يعني réduit.",
     "C'est cela : le taxi a pris deux hydrogènes, il devient NADH,H⁺. Chargé, c'est-à-dire réduit."),
    {1: (("السمية صحيحة: N A D H, H plus. ولكن شوف الطاكسي ف la figure: واش خاوي ولا عامر دابا؟",
          "Le nom est juste : NADH,H⁺. Mais regarde le taxi sur la figure : est-il vide ou chargé maintenant ?"),
         ("السمية عندك، ولكن الطاكسي ماشي خاوي: هز deux hydrogènes. الخاوي هو N A D plus. العامر هو N A D H, H "
          "plus، وكنقولو réduit.",
          "Le taxi n'est pas vide : il porte deux hydrogènes. Vide, c'est NAD⁺ ; chargé, c'est NADH,H⁺, et on dit "
          "réduit.")),
     2: (("l'ATP عرفناه مزيان: هو الدراهم الصغار. ولكن هنا كنهضرو على الطاكسي ديال les hydrogènes. شنو كتولي "
          "السمية ديالو ملي كيولي عامر؟",
          "L'ATP est la monnaie de la cellule, pas le transporteur. Ici on parle du taxi des hydrogènes : quel "
          "nom prend-il quand il est chargé ?"),
         ("فرق بيناتهم: l'ATP هو l'énergie، و N A D plus هو الطاكسي. ملي كيهز deux hydrogènes، كيولي N A D H, H "
          "plus، réduit.",
          "Ne confonds pas : l'ATP porte l'énergie, NAD⁺ porte les hydrogènes. Chargé de deux hydrogènes, il "
          "devient NADH,H⁺, réduit."))},
)

Q["rf_g4_bilan"] = qcm(
    "Pour une molécule de glucose, combien d'ATP la glycolyse fait-elle gagner à la cellule ?",
    ["4 ATP", "2 ATP", "6 ATP"], 1,
    "حسب معايا: pour une molécule de glucose, combien d'A T P, la glycolyse fait-elle gagner à la cellule ?",
    ("هادا هو، وخديتي الطريق الصحيح: quatre ATP تكونو، و deux ATP مشاو ف اللول. بقاو deux.",
     "Exact, et par le bon chemin : 4 ATP formés − 2 ATP consommés au début = 2 ATP gagnés."),
    {0: (("quatre ATP تكونو بصح ف la phase الثالثة، مزيان. ولكن واش la cellule ما عطات والو ف البداية؟ شوف la phase "
          "الأولى.",
          "4 ATP sont bien formés dans la phase 3. Mais la cellule n'a-t-elle rien dépensé au début ? Regarde la "
          "phase 1."),
         ("حسبتي غير اللي تكون. ولكن ف l'activation، la cellule عطات deux ATP. إذن le gain: quatre moins deux, "
          "égale deux ATP.",
          "Tu as compté seulement les ATP formés. À l'activation, 2 ATP sont consommés : gain = 4 − 2 = 2 ATP.")),
     2: (("شفتي أن كاين quatre و deux، وهادي هي الأرقام الصحيحة. ولكن واش خاصنا نجمعوهم؟ deux ATP مشاو، ماشي ربح.",
          "Tu as vu les bons nombres, 4 et 2. Mais faut-il les additionner ? Les 2 ATP du début sont dépensés, pas "
          "gagnés."),
         ("جمعتي quatre و deux، ولكن deux ATP ديال اللول مشاو، ماشي ربح. خاصنا نحيدو هاد deux: quatre moins deux, égale "
          "deux ATP.",
          "Tu as additionné 4 et 2. Or les 2 ATP du début sont consommés : il faut les soustraire, 4 − 2 = 2 ATP."))},
    demonstration={
        "parole": "نحسبو على la figure. la phase الأولى: la cellule عطات deux A T P. la phase الثالثة: كل جهة كتعطي "
                  "deux A T P، وعندنا deux côtés: deux fois deux, égale quatre A T P. le gain: quatre moins "
                  "deux, égale deux A T P. إذن la glycolyse كتعطي deux A T P، ل كل molécule ديال le glucose.",
        "lignes": [
            {"texte": "Phase 1 (activation) : 2 ATP consommés", "mot": "la phase الأولى", "allume": "atp_payes"},
            {"texte": "Phase 3 : 2 ATP par C3, et il y a 2 C3 : 2 × 2 = 4 ATP formés", "mot": "la phase الثالثة",
             "allume": "atp_gagnes"},
            {"texte": "Gain = 4 − 2 = 2 ATP", "mot": "le gain: quatre", "allume": "bilan"},
            {"texte": "Donc la glycolyse fait gagner 2 ATP par molécule de glucose.", "mot": "إذن la glycolyse كتعطي",
             "allume": "bilan"},
        ],
    },
)

Q["rf_m2_pyruvate"] = qcm(
    "Quel métabolite la mitochondrie utilise-t-elle ? Justifie par la courbe.",
    ["Le glucose : le dioxygène baisse dès son ajout",
     "L'éthanol : il est encore riche en énergie",
     "L'acide pyruvique : le dioxygène ne baisse qu'après son ajout"], 2,
    "سؤال ديال الامتحان: quel métabolite la mitochondrie utilise-t-elle ? Justifie par la courbe.",
    ("بالضبط، وعطيتي الدليل من la courbe: le dioxygène بقا ثابت مع le glucose، وما نقص حتى زدنا l'acide pyruvique.",
     "Exact, et justifié par la courbe : stable avec le glucose, le dioxygène ne diminue qu'après l'ajout "
     "d'acide pyruvique (275 → 215 µmol/L)."),
    {0: (("le glucose هو اللي كتبدا بيه الخلية، الفكرة ديالك مفهومة. ولكن شوف la courbe من بعد t un: واش le dioxygène "
          "تبدل ملي زدنا le glucose؟",
          "Le glucose est bien le point de départ de la cellule. Mais regarde la courbe après t1 : le dioxygène "
          "change-t-il quand on ajoute le glucose ?"),
         ("مع le glucose، le dioxygène بقا ثابت: la mitochondrie ما استعملاتوش. نقص غير من بعد l'acide pyruvique. "
          "إذن هو اللي كتستعمل.",
          "Avec le glucose, le dioxygène reste stable : il n'est pas utilisé. Il ne baisse qu'après l'acide "
          "pyruvique : c'est lui que la mitochondrie utilise.")),
     1: (("صحيح أن l'éthanol باقي فيه l'énergie. ولكن واش زدناه ف هاد التجربة؟ شوف شنو دخلنا ف t un و ف t deux.",
          "L'éthanol garde bien de l'énergie, mais l'a-t-on ajouté dans cette expérience ? Regarde ce qui est "
          "injecté à t1 et à t2."),
         ("l'éthanol ما كاينش ف هاد التجربة. زدنا le glucose، وما وقع والو. زدنا l'acide pyruvique، و le dioxygène "
          "نقص. إذن الجواب هو l'acide pyruvique.",
          "L'éthanol n'est pas dans cette expérience. Glucose : rien ne change. Acide pyruvique : le dioxygène "
          "diminue. La réponse est l'acide pyruvique."))},
)

Q["rf_m4_matrice"] = qcm(
    "Pourquoi la membrane interne de la mitochondrie est-elle si riche en protéines ?",
    ["Parce qu'elle porte beaucoup d'enzymes et de transporteurs : c'est un lieu de réactions",
     "Parce qu'elle doit laisser entrer le glucose", "Parce qu'elle est une simple enveloppe, comme la membrane externe"], 0,
    "فكر مزيان: pourquoi la membrane interne de la mitochondrie, est-elle si riche en protéines ?",
    ("زوين، شفتي العلاقة بين la structure و le rôle: quatre-vingts pour cent protéines، حيت فيها les enzymes و les "
     "transporteurs اللي خدامين.",
     "Très bien, tu relies la structure à la fonction : 80 % de protéines, car elle porte les enzymes, les "
     "transporteurs d'électrons et l'ATP synthase."),
    {1: (("فكرتي ف شنو كيدخل ل la mitochondrie، وهادا تفكير مزيان. ولكن تفكر التجربة: واش la mitochondrie كتستعمل "
          "le glucose؟",
          "Tu penses à ce qui entre dans la mitochondrie, c'est une bonne piste. Mais rappelle-toi l'expérience : "
          "la mitochondrie utilise-t-elle le glucose ?"),
         ("le glucose ما كيدخلش ل la mitochondrie: هي كتستعمل l'acide pyruvique. les protéines ديال la membrane "
          "interne هما les enzymes و les transporteurs.",
          "Le glucose n'entre pas dans la mitochondrie (elle utilise l'acide pyruvique). Les protéines de la "
          "membrane interne sont des enzymes et des transporteurs : un lieu de réactions.")),
     2: (("la membrane externe بصح غير كتخلي الحوايج يدوزو. ولكن قارن les pourcentages: soixante و quatre-vingts. "
          "علاش la membrane interne فيها كثر؟",
          "La membrane externe est bien une enveloppe qui laisse passer. Mais compare les pourcentages : 60 % et "
          "80 %. Pourquoi l'interne en a-t-elle plus ?"),
         ("ماشي بحال la membrane externe: la membrane interne فيها quatre-vingts pour cent protéines، حيت فيها les "
          "enzymes، les transporteurs، و l'ATP synthase. هي بلاصة ديال الخدمة.",
          "Elle n'est pas comme la membrane externe : 80 % de protéines, car elle porte enzymes, transporteurs et "
          "ATP synthase. C'est un lieu de réactions."))},
)

# L'association du bloc 4 (règle 47 : une association reste une association, un retour par paire)
ASSOCIATION = {
    "rf_a2_definitions": {
        "type": "association",
        "prompt": "Relie chaque mot à ce qui lui correspond.",
        "timeout_seconds": 180,
        "enonce_dit": "ودابا خدم بيديك: كل كلمة على اليسار، وصلها مع الجملة ديالها على اليمين.",
        "association": {
            "gauche": [{"id": "1", "texte": "Respiration cellulaire"}, {"id": "2", "texte": "Fermentation alcoolique"},
                       {"id": "3", "texte": "Milieu aérobie"}, {"id": "4", "texte": "Milieu anaérobie"}],
            "droite": [{"id": "a", "texte": "oxydation incomplète du glucose : éthanol + CO₂, peu d'énergie"},
                       {"id": "b", "texte": "milieu sans dioxygène"},
                       {"id": "c", "texte": "oxydation complète du glucose : CO₂ + H₂O, beaucoup d'énergie"},
                       {"id": "d", "texte": "milieu qui contient du dioxygène"}],
            "couples": {"1": "c", "2": "a", "3": "d", "4": "b"},
            "essais": 2,
            "retours": {
                "1-c": {"juste": True, "texte": "Oui : la respiration dégrade tout le glucose, jusqu'au CO₂ et à l'eau. (1 ; c)",
                        "dit": "مزيان! ف la respiration، le glucose كيتفكك كامل: oxydation complète، وبزاف ديال l'énergie."},
                "2-a": {"juste": True, "texte": "Oui : la fermentation laisse l'éthanol, encore riche en énergie. (2 ; a)",
                        "dit": "هادا هو: la fermentation كتخلي l'éthanol، وباقي فيه l'énergie. oxydation incomplète."},
                "3-d": {"juste": True, "texte": "Oui : aéro = air ; un milieu aérobie contient du dioxygène. (3 ; d)",
                        "dit": "صحيح: aéro يعني الهوا. milieu aérobie فيه le dioxygène."},
                "4-b": {"juste": True, "texte": "Oui : an = sans ; un milieu anaérobie ne contient pas de dioxygène. (4 ; b)",
                        "dit": "بالضبط: an يعني بلا. milieu anaérobie ما فيهش le dioxygène."},
                "1-*": {"juste": False, "texte": "Pas encore : la respiration est une réaction, pas un milieu, et elle "
                        "dégrade tout le glucose. Cherche la phrase où il ne reste aucun déchet organique.",
                        "dit": "مازال: la respiration ماشي milieu، هي réaction. وفيها le glucose كيتفكك كامل. قلب على الجملة "
                               "اللي ما بقا فيها حتى déchet organique."},
                "2-*": {"juste": False, "texte": "Pas encore : la fermentation est une réaction qui laisse un déchet "
                        "organique. Cherche la phrase où il reste de l'éthanol.",
                        "dit": "قريب، ولكن la fermentation كتخلي واحد le déchet organique. قلب على الجملة اللي فيها "
                               "l'éthanol."},
                "3-*": {"juste": False, "texte": "Pas encore : « aérobie » décrit un milieu, pas une réaction. Pense à "
                        "« aéro » : l'air.",
                        "dit": "لا، aérobie كتهضر على le milieu، ماشي على la réaction. تفكر: aéro يعني الهوا."},
                "4-*": {"juste": False, "texte": "Pas encore : « anaérobie » décrit un milieu. Pense à « an » : sans.",
                        "dit": "شوف الكلمة مزيان: anaérobie كتبدا ب an، يعني بلا. وهي كتهضر على le milieu."},
            },
            "bilan": {"texte": "Respiration : oxydation complète, en milieu aérobie. Fermentation : oxydation "
                               "incomplète, en milieu anaérobie.",
                      "dit": "إذن: la respiration، oxydation complète، ف milieu aérobie. و la fermentation، oxydation "
                             "incomplète، ف milieu anaérobie."},
        },
    }
}

# Le schéma à légender (diapo rf_m3_construire) : réactions selon le résultat de l'élève
LEGENDE = {
    "juste": R("برافو! les six étiquettes كاملين ف البلاصة ديالهم من أول مرة. هاد le schéma دابا ديالك، وغادي يجيك ساهل "
               "ف الامتحان.",
               "Bravo : les 6 étiquettes sont à leur place du premier coup. Ce schéma, tu le sais."),
    "partiel": R("مزيان، كملتي le schéma، ولكن تلفتي شي مرة ف الطريق. تفكر: la membrane interne هي اللي كتدخل وتخرج "
                 "وكتعطي les crêtes، و les sphères pédonculées لاصقين فيها.",
                 "Le schéma est complet, avec une ou deux erreurs en route. Retiens : la membrane interne se replie "
                 "en crêtes et porte les sphères pédonculées."),
    "faux": R("le schéma كمل، ولكن ب بزاف ديال المحاولات، وهادا عادي ف المرة الأولى. شوف: برا la membrane externe، "
              "لداخل la membrane interne مع les crêtes، بيناتهم l'espace intermembranaire، و ف الوسط la matrice.",
              "Le schéma est complet, mais avec plusieurs erreurs : c'est normal la première fois. Dehors la membrane "
              "externe ; dedans la membrane interne et ses crêtes ; entre les deux l'espace intermembranaire ; au "
              "centre la matrice."),
    "aide": R("واخا، أنا غادي نحط les étiquettes. شوف مزيان فين كتمشي كل وحدة، حيت المرة الجاية نتا اللي غادي تحطهم.",
              "Je place les étiquettes : regarde bien où va chacune. La prochaine fois, c'est toi qui les poses."),
}

# ───────────────────────── Questions d'observation (le résultat trouvé par l'élève) ─────────────────────────


def obs(apres, enonce, dit, indices, choix, bonne, retours, solution, gestes=None, silence=8):
    o = {"apres_mot": apres}
    if gestes:
        o["gestes"] = gestes
    o.update({"enonce": enonce, "enonce_dit": dit, "silence_s": silence,
              "indices": [dict(texte=t, dit=d, **({"repere": r} if r else {})) for t, d, r in indices],
              "choix": choix, "bonne": bonne,
              "retours": [{"ecrit": e, "parole": p} for p, e in retours],
              "solution": {"ecrit": solution[1], "parole": solution[0]}})
    return o


OBS = {}

OBS["rf_a1_exp1_injection"] = obs(
    "وشوف la courbe ديال le dioxygène مزيان.",
    "Le glucose vient d'être injecté. D'après notre hypothèse, que va faire le dioxygène dans la cuve ?",
    "le glucose دخل دابا. حسب l'hypothèse ديالنا، le dioxygène ف الما، شنو غادي يوقع ليه؟",
    [("Relis l'hypothèse : « si la levure utilise le glucose avec le dioxygène… »",
      "عاود قرا l'hypothèse: يلا كانت la levure كتستعمل le glucose مع le dioxygène.", None),
     ("Ce qui est utilisé par les levures ne peut pas rester dans l'eau.",
      "الحاجة اللي كيستعملوها les levures، ما تقدرش تبقى ف الما.", "courbe_o2")],
    ["Il va augmenter", "Il va rester stable", "Il va baisser"], 2,
    [("يطلع يعني les levures كينتجو le dioxygène. ولكن l'hypothèse كتقول أنهم كيستعملوه. فكر مرة أخرى.",
      "Augmenter voudrait dire que les levures produisent du dioxygène. Or l'hypothèse dit qu'elles l'utilisent."),
     ("ثابت يعني le glucose ما دار والو. ولكن l'hypothèse كتقول أن la levure كتستعمل le dioxygène مع le glucose.",
      "Stable voudrait dire que le glucose ne change rien. Or l'hypothèse dit que la levure utilise le dioxygène "
      "avec le glucose."),
     ("مزيان! يلا كانو les levures كيستعملو le dioxygène، خاصو ينقص ف الما. يلا نشوفو واش التجربة متافقة معاك.",
      "Oui : si les levures utilisent le dioxygène, il doit baisser dans l'eau. Voyons si l'expérience le confirme.")],
    ("حسب l'hypothèse، le dioxygène خاصو ينقص، حيت les levures كيستعملوه. شوف دابا النتيجة.",
     "D'après l'hypothèse, le dioxygène doit baisser, car les levures l'utilisent. Regarde le résultat."),
)

OBS["rf_a1_exp2_phase2"] = obs(
    "شوف les courbes من بعد هاد اللحظة.",
    "Il n'y a plus de dioxygène. Regarde la courbe du CO₂ : les levures se sont-elles arrêtées ?",
    "ما بقاش le dioxygène. شوف la courbe ديال le dioxyde de carbone: واش les levures وقفو؟",
    [("Suis la courbe du CO₂, à droite de l'instant 190 s.",
      "تبع la courbe ديال le dioxyde de carbone، من بعد cent quatre-vingt-dix secondes.", "courbe_co2"),
     ("Compare sa hauteur à 190 s et un peu plus loin.",
      "قارن الطول ديالها ف cent quatre-vingt-dix secondes، ومن بعد بشوية.", "instant_190")],
    ["Oui : plus rien ne change", "Non : le CO₂ continue de monter", "Oui : le CO₂ redescend"], 1,
    [("شوف مزيان: كاينة courbe باقا كتتحرك من بعد هاد اللحظة. تبع ديال le dioxyde de carbone.",
      "Regarde mieux : une courbe bouge encore après cet instant. Suis celle du CO₂."),
     ("هادا هو! le dioxyde de carbone باقي كيطلع، إذن les levures باقي خدامين، واخا ما بقاش le dioxygène.",
      "Oui : le CO₂ continue de monter, donc les levures travaillent encore, même sans dioxygène."),
     ("لا، ما هبطاتش. قارن la courbe ديال le dioxyde de carbone قبل هاد اللحظة ومن بعدها.",
      "Non, elle ne redescend pas. Compare la courbe du CO₂ avant et après cet instant.")],
    ("la courbe ديال le dioxyde de carbone باقا طالعة: les levures ما وقفوش، واخا le dioxygène ف zéro.",
     "La courbe du CO₂ continue de monter : les levures ne se sont pas arrêtées, même à 0 de dioxygène."),
    gestes=[{"commande": "play_until", "parametres": {"moment": "co2_monte"}}],
)

OBS["rf_a2_deux_levures"] = obs(
    "قارن بيناتهم مزيان، وخود الوقت ديالك.",
    "Compare les deux levures : quel élément n'est pas le même des deux côtés ?",
    "قارن بين les deux levures: شنو اللي ماشي بحال بحال ف جوج؟",
    [("Regarde les petits éléments allongés dans le hyaloplasme.",
      "شوف الحوايج الصغار والطوال اللي ف le hyaloplasme.", "levure_aerobie"),
     ("Compte-les à gauche, puis à droite, et compare leur taille.",
      "حسبهم على اليسار، ومن بعد على اليمين، وقارن الحجم ديالهم.", "levure_anaerobie")],
    ["Le noyau", "Les mitochondries", "La membrane plasmique"], 1,
    [("le noyau كاين ف جوج، وبحال بحال. شوف الحوايج الصغار اللي دايرين بيه.",
      "Le noyau est présent des deux côtés, semblable. Regarde plutôt les petits éléments autour de lui."),
     ("عندك عين مزيانة! les mitochondries بزاف وكبار مع le dioxygène، وقلال وصغار بلا dioxygène.",
      "Bien vu : les mitochondries sont nombreuses et grandes avec dioxygène, rares et petites sans dioxygène."),
     ("la membrane plasmique دايرة ب جوج ديال les levures، وما تبدلاتش. شوف لداخل، ف le hyaloplasme.",
      "La membrane plasmique entoure les deux levures, sans différence. Regarde à l'intérieur, dans le hyaloplasme.")],
    ("الفرق هو les mitochondries: بزاف وكبار ف milieu aérobie، وقلال وصغار ف milieu anaérobie.",
     "La différence, ce sont les mitochondries : nombreuses et développées en milieu aérobie, rares et réduites en "
     "milieu anaérobie."),
)

OBS["rf_a3_avec_o2"] = obs(
    "ولكن هاد المرة le dioxygène كاين.",
    "Avec dioxygène : où va l'acide pyruvique ?",
    "هاد المرة le dioxygène كاين. l'acide pyruvique، فين غادي يمشي؟",
    [("Avec dioxygène, la levure respire. De quel organite la respiration a-t-elle besoin ?",
      "مع le dioxygène، la levure كدير la respiration. و la respiration، أشمن organite كتحتاج؟", None),
     ("Rappelle-toi les deux levures au microscope électronique.",
      "تفكر les deux levures اللي شفنا ب le microscope électronique.", "mitochondrie")],
    ["Il reste dans le hyaloplasme", "Il sort de la levure", "Il entre dans la mitochondrie"], 2,
    [("كيبقى ف le hyaloplasme ملي ما كاينش le dioxygène: هاديك la fermentation. هنا le dioxygène كاين.",
      "Il reste dans le hyaloplasme quand il n'y a pas de dioxygène : c'est la fermentation. Ici, il y en a."),
     ("ما كيخرجش هكاك: باقي فيه l'énergie، و la cellule محتاجاها. فكر ف organite ديال la respiration.",
      "Il ne sort pas ainsi : il contient encore de l'énergie, dont la cellule a besoin. Pense à l'organite de la "
      "respiration."),
     ("بالضبط، وربطتيها مع اللي شفنا: la respiration كتحتاج les mitochondries. يلا نتأكدو ب la figure.",
      "Exact, et tu l'as relié à ce qu'on a vu : la respiration a besoin des mitochondries. Vérifions sur la figure.")],
    ("مع le dioxygène، l'acide pyruvique كيدخل ل la mitochondrie، حيت la respiration كتوقع تما.",
     "Avec dioxygène, l'acide pyruvique entre dans la mitochondrie : c'est là que se fait la respiration."),
)

OBS["rf_m1_etapes"] = obs(
    "فكر فين غادي يكونو.",
    "Les noyaux, plus lourds, sont dans le culot. Où sont les mitochondries, plus légères ?",
    "les noyaux هبطو ف le culot، حيت هما اللي lourd. و les mitochondries، اللي خفيفة، فين هما؟",
    [("À faible vitesse, seul ce qui est le plus lourd descend.",
      "ملي الدورة كتكون بالشوية، غير اللي lourd بزاف كيهبط.", "culot_noyaux"),
     ("Ce qui est léger reste dans le liquide du dessus.",
      "اللي خفيف كيبقى ف السائل اللي الفوق.", None)],
    ["Dans le culot, avec les noyaux", "Dans le surnageant", "Elles ont été détruites par le broyage"], 1,
    [("le culot فيه اللي lourd. و les mitochondries خفيفة على les noyaux، والدورة كانت بالشوية.",
      "Le culot contient ce qui est le plus lourd. Les mitochondries sont plus légères, et la vitesse était faible."),
     ("هادا هو التفكير: خفيفة، إذن بقاو ف السائل اللي الفوق، le surnageant.",
      "C'est le bon raisonnement : légères, elles restent dans le liquide du dessus, le surnageant."),
     ("le broyage كيحل الخلايا، ماشي les organites: les mitochondries بقاو كاملين. فين غادي يكونو؟",
      "Le broyage casse les cellules, pas les organites : les mitochondries sont intactes. Où sont-elles alors ?")],
    ("les mitochondries خفيفة على les noyaux: بقاو ف le surnageant، ومنو غادي نعزلوهم.",
     "Plus légères que les noyaux, les mitochondries sont restées dans le surnageant : c'est de là qu'on les isole."),
)

OBS["rf_m2_glucose"] = obs(
    "شوف la courbe.",
    "On vient d'ajouter du glucose aux mitochondries isolées. Que fait le dioxygène ?",
    "زدنا le glucose ل les mitochondries. شوف la courbe: le dioxygène، شنو وقع ليه؟",
    [("Suis la courbe après l'instant t1.", "تبع la courbe من بعد t un.", "t1"),
     ("Compare sa hauteur avant et après l'ajout.", "قارن الطول ديالها قبل ما نزيدو le glucose، ومن بعد.", "courbe")],
    ["Il baisse", "Il reste stable", "Il augmente"], 1,
    [("شوف la courbe مزيان: واش هبطات بصح من بعد t un؟ قارن مع البداية.",
      "Regarde bien la courbe : descend-elle vraiment après t1 ? Compare avec le début."),
     ("قريتي la courbe مزيان: le dioxygène بقا ثابت. إذن les mitochondries ما استعملوش le glucose.",
      "Bien lu : le dioxygène reste stable. Les mitochondries n'ont donc pas utilisé le glucose."),
     ("les mitochondries ما كينتجوش le dioxygène. تبع la courbe من بعد t un: واش تبدلات؟",
      "Les mitochondries ne produisent pas de dioxygène. Suis la courbe après t1 : a-t-elle changé ?")],
    ("من بعد le glucose، la courbe بقات ثابتة: le dioxygène ما نقصش.",
     "Après l'ajout de glucose, la courbe reste stable : le dioxygène ne diminue pas."),
    gestes=[{"commande": "play_until", "parametres": {"moment": "rien"}}],
)

# ───────────────────────── Compétences et rappels espacés ─────────────────────────


def libre(i, prompt, attendu, dit):
    return {"id": i, "type": "libre", "prompt": prompt, "attendu": attendu, "enonce_dit": dit}


def rqcm(i, prompt, options, correct, dit, juste, faux):
    q, rep = qcm(prompt, options, correct, dit, juste, faux)
    q.pop("timeout_seconds")
    q["id"] = i
    q["reponses"] = rep
    return {k: q[k] for k in ("id", "type", "prompt", "options", "correct", "enonce_dit", "reponses")}


COMPETENCES = [
    {"id": "C1", "label": "Analyser un résultat d'ExAO : lire les axes, décrire, déduire", "cadre_ids": ["LE2", "LE9"],
     "dit": "analyser une courbe : lire les axes, décrire, puis déduire",
     "rappels": [
         libre("C1_r1", "Devant une courbe, quelles sont les trois étapes de l'analyse ?",
               "Lire les axes (grandeur et unité), décrire avec des valeurs, puis déduire (« donc… »).",
               "تفكر معايا: devant une courbe, quelles sont les trois étapes de l'analyse ?"),
         rqcm("C1_r2", "Dans une cuve de levures bien oxygénée, on injecte du glucose. Le dioxygène dissous…",
              ["augmente", "reste stable", "diminue"], 2,
              "سؤال: dans une cuve de levures bien oxygénée, on injecte du glucose. Que fait le dioxygène ?",
              ("مزيان، باقي عاقل: les levures كيستعملو le dioxygène مع le glucose، إذن كينقص.",
               "Oui : les levures utilisent le dioxygène avec le glucose, il diminue."),
              {0: (("les levures ما كينتجوش le dioxygène. فكر: ملي كدير la respiration، واش كتاخد le dioxygène ولا كتعطيه؟",
                    "Les levures ne produisent pas de dioxygène. Quand on respire, prend-on le dioxygène ou le donne-t-on ?"),
                   ("ف la respiration، les levures كياخدو le dioxygène: كينقص ف الما. اللي كيطلع هو le dioxyde de carbone.",
                    "Dans la respiration, les levures absorbent le dioxygène : il diminue. C'est le CO₂ qui augmente.")),
               1: (("ثابت كيكون قبل le glucose. ولكن ملي كيدخل le glucose، les levures كيبداو يخدمو. شنو كيستعملو معاه؟",
                    "Stable, c'est avant le glucose. Quand le glucose arrive, les levures travaillent : qu'utilisent-elles avec lui ?"),
                   ("مع le glucose، les levures كيديرو la respiration: كياخدو le dioxygène، إذن كينقص.",
                    "Avec le glucose, les levures respirent : elles absorbent le dioxygène, qui diminue."))}),
         libre("C1_r3", "Dans « le dioxygène diminue, donc les levures respirent », quelle partie est la description, "
               "quelle partie est la déduction ?",
               "« Le dioxygène diminue » est la description ; « donc les levures respirent » est la déduction.",
               "جاوب بوحدك: dans la phrase, le dioxygène diminue, donc les levures respirent, où est la description, "
               "et où est la déduction ?"),
     ]},
    {"id": "C2", "label": "Définir la respiration et la fermentation et écrire leurs équations", "cadre_ids": ["LE2", "LE7"],
     "dit": "définir la respiration et la fermentation, et écrire leurs équations",
     "rappels": [
         libre("C2_r1", "Écris l'équation de la respiration cellulaire.", "C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + énergie",
               "بلا ما تشوف ف الدفتر: écris l'équation de la respiration cellulaire."),
         libre("C2_r2", "Écris l'équation de la fermentation alcoolique.", "C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂ + énergie",
               "ودابا الثانية: écris l'équation de la fermentation alcoolique."),
         rqcm("C2_r3", "La fermentation alcoolique est…",
              ["une oxydation complète du glucose, en milieu aérobie",
               "une oxydation incomplète du glucose, en milieu anaérobie",
               "une oxydation complète du glucose, en milieu anaérobie"], 1,
              "كمل الجملة: la fermentation alcoolique est…",
              ("هادي هي la définition: incomplète حيت كيبقى l'éthanol، و anaérobie حيت ما كاينش le dioxygène.",
               "C'est la définition : incomplète car il reste l'éthanol, anaérobie car il n'y a pas de dioxygène."),
              {0: (("هاد الجملة صحيحة، ولكن ل la respiration. la fermentation كتوقع بلا dioxygène، وكيبقى منها شي حاجة. شنو؟",
                    "Cette phrase est juste… pour la respiration. La fermentation se fait sans dioxygène et laisse quelque chose : quoi ?"),
                   ("oxydation complète، en milieu aérobie، هادي la respiration. la fermentation: incomplète، en milieu anaérobie.",
                    "Oxydation complète en milieu aérobie : c'est la respiration. La fermentation est incomplète, en milieu anaérobie.")),
               2: (("le milieu عندك صحيح: anaérobie. ولكن واش le glucose كيتفكك كامل؟ تفكر l'éthanol.",
                    "Le milieu est juste : anaérobie. Mais le glucose est-il dégradé entièrement ? Pense à l'éthanol."),
                   ("anaérobie صحيح، ولكن l'oxydation incomplète: كيبقى l'éthanol، وباقي فيه l'énergie.",
                    "Anaérobie, oui ; mais l'oxydation est incomplète : il reste l'éthanol, encore riche en énergie."))}),
         libre("C2_r4", "Définis la respiration cellulaire.",
               "C'est l'oxydation complète du glucose, en milieu aérobie, dans les mitochondries ; elle libère beaucoup d'énergie.",
               "عطيني la définition: qu'est-ce que la respiration cellulaire ?"),
     ]},
    {"id": "C3", "label": "Localiser la respiration (mitochondrie) et la fermentation (hyaloplasme)", "cadre_ids": ["LE4", "LE7"],
     "dit": "localiser la respiration et la fermentation dans la cellule",
     "rappels": [
         rqcm("C3_r1", "La fermentation alcoolique se déroule…",
              ["dans les mitochondries", "dans le noyau", "dans le hyaloplasme"], 2,
              "فين كتوقع؟ la fermentation alcoolique se déroule…",
              ("صحيح: la fermentation ما كتحتاجش les mitochondries، كتوقع ف le hyaloplasme.",
               "Oui : la fermentation n'a pas besoin des mitochondries, elle se fait dans le hyaloplasme."),
              {0: (("les mitochondries مهمين، ولكن ل la respiration. تفكر la levure ديال milieu anaérobie: واش عندها بزاف منهم؟",
                    "Les mitochondries comptent, mais pour la respiration. La levure du milieu anaérobie en a-t-elle beaucoup ?"),
                   ("ف milieu anaérobie، les mitochondries قلال وصغار: la fermentation ما كتحتاجهمش. كتوقع ف le hyaloplasme.",
                    "En milieu anaérobie, les mitochondries sont rares et réduites : la fermentation se fait dans le hyaloplasme.")),
               1: (("le noyau كيتحكم ف الخلية، ولكن les réactions ديال l'énergie ما كيوقعوش فيه. فكر ف السائل ديال الخلية.",
                    "Le noyau commande la cellule, mais les réactions de l'énergie ne s'y font pas. Pense au liquide de la cellule."),
                   ("ماشي ف le noyau: la fermentation كتوقع ف le hyaloplasme، السائل اللي عامر بيه الخلية.",
                    "Pas dans le noyau : la fermentation se fait dans le hyaloplasme, le liquide de la cellule."))}),
         libre("C3_r2", "De quel organite la respiration cellulaire a-t-elle besoin ?", "Des mitochondries.",
               "سؤال قصير: de quel organite, la respiration cellulaire a-t-elle besoin ?"),
         libre("C3_r3", "Quelle différence voit-on entre une levure en milieu aérobie et une levure en milieu anaérobie ?",
               "En milieu aérobie, les mitochondries sont nombreuses et développées ; en milieu anaérobie, rares et réduites.",
               "تفكر les deux levures: quelle différence voit-on, entre le milieu aérobie, et le milieu anaérobie ?"),
     ]},
    {"id": "C4", "label": "Retracer le devenir du glucose : glycolyse commune, acide pyruvique au carrefour", "cadre_ids": ["LE3", "LE10"],
     "dit": "retracer le devenir du glucose dans la cellule",
     "rappels": [
         libre("C4_r1", "Que devient le glucose pendant la glycolyse, et où ?",
               "Il est dégradé en deux acides pyruviques, dans le hyaloplasme.",
               "رجع معايا ل la carte: que devient le glucose pendant la glycolyse, et où ?"),
         rqcm("C4_r2", "En présence de dioxygène, l'acide pyruvique…",
              ["reste dans le hyaloplasme et donne de l'éthanol", "entre dans la mitochondrie, où il est dégradé en CO₂",
               "sort de la cellule sans être transformé"], 1,
              "كمل: en présence de dioxygène, l'acide pyruvique…",
              ("هادا هو الطريق ديال la respiration: l'acide pyruvique كيدخل ل la mitochondrie، وكيخرج le dioxyde de carbone.",
               "C'est la route de la respiration : l'acide pyruvique entre dans la mitochondrie et il sort du CO₂."),
              {0: (("هاد الطريق كاين بصح، ولكن بلا dioxygène. هنا le dioxygène كاين: فين كيمشي l'acide pyruvique؟",
                    "Cette route existe, mais sans dioxygène. Ici il y en a : où va l'acide pyruvique ?"),
                   ("l'éthanol كيبان غير بلا dioxygène. مع le dioxygène، l'acide pyruvique كيدخل ل la mitochondrie.",
                    "L'éthanol n'apparaît que sans dioxygène. Avec dioxygène, l'acide pyruvique entre dans la mitochondrie.")),
               2: (("l'acide pyruvique باقي فيه l'énergie: la cellule ما غاديش تخليه يخرج. فين كتوقع la respiration؟",
                    "L'acide pyruvique contient encore de l'énergie : la cellule ne le laisse pas partir. Où se fait la respiration ?"),
                   ("ما كيخرجش: مع le dioxygène، كيدخل ل la mitochondrie، وتما كيتفكك حتى ل le dioxyde de carbone.",
                    "Il ne sort pas : avec dioxygène, il entre dans la mitochondrie, où il est dégradé en CO₂."))}),
         libre("C4_r3", "Quelle étape est commune à la respiration et à la fermentation ?", "La glycolyse.",
               "بكلمة وحدة: quelle étape est commune, à la respiration et à la fermentation ?"),
     ]},
    {"id": "C5", "label": "Décrire les trois phases et le bilan de la glycolyse", "cadre_ids": ["LE3"],
     "dit": "décrire les phases et le bilan de la glycolyse",
     "rappels": [
         libre("C5_r1", "Écris l'équation globale de la glycolyse.",
               "C₆H₁₂O₆ + 2 ADP + 2 Pi + 2 NAD⁺ → 2 CH₃-CO-COOH + 2 ATP + 2 NADH,H⁺",
               "هادي كتجي ف le national: écris l'équation globale de la glycolyse."),
         rqcm("C5_r2", "Pour une molécule de glucose, le gain de la glycolyse est de…",
              ["2 ATP", "4 ATP", "0 ATP"], 0,
              "شحال؟ pour une molécule de glucose, le gain de la glycolyse est de…",
              ("مزيان، ما نسيتيش الحساب: quatre ATP تكونو، و deux مشاو ف l'activation. بقاو deux.",
               "Oui : 4 ATP formés − 2 ATP consommés à l'activation = 2 ATP."),
              {1: (("quatre هو اللي تكون ف اللخر. ولكن ف البداية، la cellule عطات شي ATP. شحال؟",
                    "4, c'est ce qui est formé à la fin. Mais au début, la cellule a dépensé des ATP : combien ?"),
                   ("quatre ATP تكونو، ولكن deux مشاو ف la phase الأولى. le gain: quatre moins deux, égale deux ATP.",
                    "4 ATP formés, mais 2 consommés dans la phase 1 : gain = 4 − 2 = 2 ATP.")),
               2: (("بصح la cellule كتعطي deux ATP ف اللول. ولكن ف la phase الثالثة، شحال كتاخد؟",
                    "La cellule dépense bien 2 ATP au début. Mais dans la phase 3, combien en gagne-t-elle ?"),
                   ("كتعطي deux، ولكن كتاخد quatre. إذن le gain ماشي zéro: quatre moins deux, égale deux ATP.",
                    "Elle en dépense 2 mais en forme 4 : le gain n'est pas nul, 4 − 2 = 2 ATP."))}),
         libre("C5_r3", "Cite les trois phases de la glycolyse, dans l'ordre.",
               "Activation, scission, puis formation d'énergie (ATP).",
               "ب الترتيب: cite les trois phases de la glycolyse."),
     ]},
    {"id": "C6", "label": "Montrer que la mitochondrie utilise l'acide pyruvique (centrifugation, ExAO)", "cadre_ids": ["LE4", "LE9"],
     "dit": "montrer que la mitochondrie utilise l'acide pyruvique",
     "rappels": [
         rqcm("C6_r1", "On ajoute du glucose à des mitochondries isolées, dans un milieu oxygéné. Le dioxygène…",
              ["diminue", "reste stable", "augmente"], 1,
              "تفكر التجربة: on ajoute du glucose à des mitochondries isolées. Que fait le dioxygène ?",
              ("باقي عاقل على التجربة: le dioxygène كيبقى ثابت، حيت la mitochondrie ما كتستعملش le glucose.",
               "Oui : le dioxygène reste stable, car la mitochondrie n'utilise pas le glucose."),
              {0: (("كينقص بصح، ولكن مع molécule أخرى. تفكر: شنو اللي زدنا ف المرة الثانية؟",
                    "Il diminue bien, mais avec une autre molécule. Rappelle-toi : qu'a-t-on ajouté la deuxième fois ?"),
                   ("le dioxygène كينقص غير مع l'acide pyruvique. مع le glucose كيبقى ثابت: la mitochondrie ما كتستعملوش.",
                    "Le dioxygène ne diminue qu'avec l'acide pyruvique. Avec le glucose il reste stable.")),
               2: (("les mitochondries ما كينتجوش le dioxygène، كيستهلكوه. والسؤال: واش كيستهلكوه مع le glucose؟",
                    "Les mitochondries ne produisent pas de dioxygène, elles en consomment. Mais en consomment-elles avec le glucose ?"),
                   ("ما كيطلعش: مع le glucose، le dioxygène كيبقى ثابت. كينقص غير ملي كنزيدو l'acide pyruvique.",
                    "Il n'augmente pas : avec le glucose il reste stable ; il ne diminue qu'avec l'acide pyruvique."))}),
         libre("C6_r2", "À quoi sert la centrifugation fractionnée ?",
               "À séparer les constituants de la cellule selon leur densité, pour isoler les mitochondries.",
               "سؤال على الطريقة: à quoi sert la centrifugation fractionnée ?"),
         libre("C6_r3", "Quel métabolite la mitochondrie utilise-t-elle ?", "L'acide pyruvique, et non le glucose.",
               "جاوب ب جملة: quel métabolite la mitochondrie utilise-t-elle ?"),
     ]},
    {"id": "C7", "label": "Légender l'ultrastructure de la mitochondrie", "cadre_ids": ["LE4"],
     "dit": "légender le schéma de la mitochondrie",
     "rappels": [
         libre("C7_r1", "Cite les six légendes de la mitochondrie.",
               "Membrane externe, espace intermembranaire, membrane interne, crêtes, matrice, sphères pédonculées.",
               "سد عينيك وتفكر le schéma: cite les six légendes de la mitochondrie."),
         rqcm("C7_r2", "Les replis de la membrane interne s'appellent…",
              ["les sphères pédonculées", "les crêtes", "la matrice"], 1,
              "شنو سميتهم؟ les replis de la membrane interne s'appellent…",
              ("صحيح، les crêtes: la membrane interne كتدخل وتخرج، وهكا كتزيد البلاصة.",
               "Oui, les crêtes : la membrane interne se replie, ce qui augmente sa surface."),
              {0: (("les sphères pédonculées كاينين بصح ف la membrane interne، ولكن هما الكورات الصغار. شنو سمية الدخلة "
                    "والخرجة ديال الغشاء؟",
                    "Les sphères pédonculées sont bien sur la membrane interne, mais ce sont les petites boules. Comment s'appellent les replis ?"),
                   ("les sphères pédonculées هما الكورات اللي لاصقين. الغشاء ملي كيدخل ويخرج، كيعطي les crêtes.",
                    "Les sphères pédonculées sont les boules attachées. Les replis de la membrane, ce sont les crêtes.")),
               2: (("la matrice هي اللي ف الوسط، بين les replis. السؤال على les replis ديال الغشاء.",
                    "La matrice est ce qui remplit le centre, entre les replis. On demande le nom des replis eux-mêmes."),
                   ("la matrice هي الوسط ديال la mitochondrie. les replis ديال la membrane interne سميتهم les crêtes.",
                    "La matrice est l'intérieur de la mitochondrie. Les replis de la membrane interne sont les crêtes."))}),
         libre("C7_r3", "Qu'y a-t-il entre la membrane externe et la membrane interne ?", "L'espace intermembranaire.",
               "شنو كاين بيناتهم؟ entre la membrane externe et la membrane interne, il y a…"),
     ]},
    {"id": "C8", "label": "Relier la composition des membranes et de la matrice à leur rôle", "cadre_ids": ["LE4", "LE5"],
     "dit": "relier la composition de la mitochondrie à son rôle",
     "rappels": [
         rqcm("C8_r1", "La membrane interne de la mitochondrie contient environ…",
              ["40 % de protéines", "60 % de protéines", "80 % de protéines"], 2,
              "تفكر les pourcentages: la membrane interne de la mitochondrie contient environ…",
              ("هادا هو: quatre-vingts pour cent protéines، حيت هي بلاصة ديال الخدمة.",
               "Oui : 80 % de protéines, car c'est un lieu de réactions."),
              {0: (("quarante pour cent كاين بصح ف الدرس، ولكن ديال les lipides ديال la membrane externe. و les protéines "
                    "ديال la membrane interne؟",
                    "40 % existe bien dans le cours : ce sont les lipides de la membrane externe. Et les protéines de l'interne ?"),
                   ("quarante pour cent هو les lipides ديال la membrane externe. la membrane interne فيها quatre-vingts "
                    "pour cent protéines.",
                    "40 % : lipides de la membrane externe. La membrane interne contient 80 % de protéines.")),
               1: (("soixante pour cent هو ديال la membrane externe. la membrane interne فيها كثر، حيت فيها les enzymes.",
                    "60 %, c'est la membrane externe. L'interne en a davantage, car elle porte les enzymes : combien ?"),
                   ("soixante pour cent ل la membrane externe، و quatre-vingts pour cent ل la membrane interne.",
                    "60 % pour la membrane externe, 80 % pour la membrane interne."))}),
         libre("C8_r2", "Que fait une décarboxylase ?", "Elle retire du CO₂ à une molécule.",
               "من السمية ديالها: que fait une décarboxylase ?"),
         libre("C8_r3", "Pourquoi la membrane interne est-elle très riche en protéines ?",
               "Parce qu'elle porte des enzymes, des transporteurs d'électrons et l'ATP synthase : c'est un lieu de réactions.",
               "شرح ليا: pourquoi la membrane interne, est-elle très riche en protéines ?"),
     ]},
]

# ───────────────────────── Blocs : cahier, retrouver, exercice ─────────────────────────


def bloc(i, titre, ids, cahier, retrouver=None, exercice=None, figures=None):
    b = {"id": i, "titre": titre, "slide_ids": ids, "cahier": [{"texte": t} for t in cahier]}
    if figures:
        b["cahier_figures"] = figures      # noms des figures, remplacés par construire_cours.py
    if retrouver:
        p, a, c, d = retrouver
        b["retrouver"] = {"prompt": "Cahier fermé : " + p, "attendu": a, "competence_id": c, "enonce_dit": d}
    if exercice:
        q, rep = exercice
        q = dict(q)
        q.pop("timeout_seconds", None)
        q["reponses"] = rep
        b["exercice"] = q
    return b


SEANCES = [
    {"id": "rf_s1", "titre": "Séance 1 — Une question et trois rappels", "blocs": [
        bloc("rf_s1_b1", "Le problème, la cellule, le glucose, la levure",
             ["rf_ouverture_cours", "rf_o1_pate", "rf_r1_cellule", "rf_r2_glucose", "rf_r3_levure"],
             ["On apprend : respiration, fermentation, glycolyse, mitochondrie.",
              "Problème : d'où une cellule tire-t-elle son énergie ?",
              "Rappel : la cellule : membrane plasmique, hyaloplasme, noyau, organites.",
              "Rappel : le glucose C₆H₁₂O₆ est une matière organique riche en énergie.",
              "Définition : un milieu aérobie contient du dioxygène ; un milieu anaérobie n'en contient pas."]),
    ]},
    {"id": "rf_s2", "titre": "Séance 2 — Activité 1 : mettre en évidence la respiration et la fermentation", "blocs": [
        bloc("rf_s2_b1", "En présence de dioxygène : la respiration",
             ["rf_a1_montage", "rf_a1_exp1_avant", "rf_a1_exp1_injection", "rf_a1_exp1_deduire", "rf_a1_equation_respi"],
             ["I. Mise en évidence de la respiration et de la fermentation",
              "1. En présence de dioxygène : la respiration",
              "Méthode : 1) lire les axes 2) décrire avec des valeurs 3) déduire (« donc… »)",
              "Des levures qui reçoivent du glucose absorbent du dioxygène et rejettent du CO₂.",
              "Donc elles respirent : c'est la respiration cellulaire.",
              "Formule : C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + énergie"],
             retrouver=("écris l'équation de la respiration cellulaire.", "C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + énergie",
                        "C2", "سد الدفتر، وجاوب: écris l'équation de la respiration cellulaire."),
             exercice=qcm(
                 "Devant une courbe d'ExAO, dans quel ordre travaille-t-on ?",
                 ["déduire, décrire, lire les axes", "lire les axes, décrire avec des valeurs, déduire",
                  "décrire, déduire, lire les axes"], 1,
                 "سؤال على الطريقة: devant une courbe, dans quel ordre travaille-t-on ?",
                 ("هادي هي الطريقة ديال الامتحان: les axes، من بعد la description مع les valeurs، ومن بعد donc.",
                  "C'est la méthode du bac : les axes, puis la description avec des valeurs, puis « donc »."),
                 {0: (("la déduction مهمة، ولكن واش نقدرو نستنتجو قبل ما نشوفو؟ شنو خاصنا نقراو اللول ف courbe؟",
                       "La déduction compte, mais peut-on déduire avant d'avoir regardé ? Que lit-on d'abord sur une courbe ?"),
                      ("donc كيجي ف اللخر. اللول les axes، من بعد la description، ومن بعد la déduction.",
                       "« Donc » vient en dernier : d'abord les axes, puis la description, puis la déduction.")),
                  2: (("la description قبل la déduction، هادي صحيحة. ولكن قبل ما نوصفو، خاصنا نعرفو شنو كاين ف كل axe.",
                       "Décrire avant de déduire, c'est juste. Mais avant de décrire, il faut savoir ce que porte chaque axe."),
                      ("les axes هما اللولين: بلا بيهم ما نعرفوش les valeurs. من بعد la description، ومن بعد la déduction.",
                       "Les axes d'abord : sans eux, pas de valeurs. Puis la description, puis la déduction."))})),
        bloc("rf_s2_b2", "En absence de dioxygène : la fermentation",
             ["rf_a1_exp2_axes", "rf_a1_exp2_phase1", "rf_a1_exp2_phase2", "rf_a1_equation_ferm"],
             ["2. En absence de dioxygène : la fermentation",
              "Tant qu'il reste du dioxygène, les levures respirent.",
              "Sans dioxygène, elles consomment encore du glucose, rejettent du CO₂ et produisent de l'éthanol.",
              "Donc elles fermentent : c'est la fermentation alcoolique.",
              "Formule : C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂ + énergie (peu)",
              "Remarque : l'éthanol est encore riche en énergie."],
             retrouver=("écris l'équation de la fermentation alcoolique.", "C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂ + énergie",
                        "C2", "بلا ما تشوف: écris l'équation de la fermentation alcoolique."),
             exercice=qcm(
                 "Des levures sont dans une cuve fermée, avec du glucose. Quand le dioxygène est épuisé, elles…",
                 ["meurent : plus rien ne change dans la cuve", "produisent du dioxygène",
                  "consomment encore du glucose et produisent de l'éthanol et du CO₂"], 2,
                 "كمل الجملة: des levures sont dans une cuve fermée, avec du glucose. Quand le dioxygène est épuisé, elles…",
                 ("صحيح: la levure كتبدل الطريق، وكدير la fermentation alcoolique.",
                  "Oui : la levure change de voie, elle fait la fermentation alcoolique."),
                 {0: (("بزاف ديال الخلايا ما كيقدروش بلا dioxygène، هادي صحيحة. ولكن تفكر les courbes من بعد ما تسالا: واش "
                       "وقفو؟", "Beaucoup de cellules ne vivent pas sans dioxygène, mais rappelle-toi les courbes après son épuisement : s'arrêtent-elles ?"),
                      ("ما كيموتوش: le dioxyde de carbone باقي كيطلع و l'éthanol كيبان. كيديرو la fermentation.",
                       "Elles ne meurent pas : le CO₂ monte encore et l'éthanol apparaît. Elles fermentent.")),
                  1: (("le dioxygène تسالا بصح. ولكن les levures ما كينتجوهش أبدا. شنو اللي بان جديد ف les courbes؟",
                       "Le dioxygène est bien épuisé, mais les levures n'en produisent jamais. Quel produit nouveau apparaît ?"),
                      ("les levures ما كينتجوش le dioxygène. بلا dioxygène، كينتجو l'éthanol و le dioxyde de carbone.",
                       "Les levures ne produisent pas de dioxygène. Sans lui, elles produisent de l'éthanol et du CO₂."))})),
    ]},
    {"id": "rf_s3", "titre": "Séance 3 — Activité 1 (suite) : où, et que devient le glucose ?", "blocs": [
        bloc("rf_s3_b1", "Le lieu de chaque réaction, et les deux définitions",
             ["rf_a2_deux_levures", "rf_a2_localisation", "rf_a2_tableau", "rf_a2_definitions"],
             ["3. Le lieu de chaque réaction",
              "Donc la respiration a besoin des mitochondries ; la fermentation se fait dans le hyaloplasme.",
              "| | Respiration | Fermentation |",
              "| Milieu | aérobie | anaérobie |",
              "| Gaz | O₂ absorbé, CO₂ rejeté | CO₂ rejeté |",
              "| Glucose | dégradé totalement | dégradé en partie (éthanol) |",
              "| Énergie | beaucoup | peu |",
              "| Lieu | mitochondries | hyaloplasme |",
              "Définition : la respiration cellulaire est l'oxydation complète du glucose, en milieu aérobie ; elle libère beaucoup d'énergie.",
              "Définition : la fermentation est l'oxydation incomplète du glucose, en milieu anaérobie ; elle libère peu d'énergie et laisse un déchet organique riche en énergie."],
             retrouver=("donne la définition de la fermentation.",
                        "La fermentation est l'oxydation incomplète du glucose, en milieu anaérobie, dans le hyaloplasme ; "
                        "elle libère peu d'énergie et laisse un déchet organique riche en énergie.",
                        "C2", "سد الدفتر: donne la définition de la fermentation."),
             exercice=qcm(
                 "Une levure cultivée en milieu anaérobie possède…",
                 ["des mitochondries nombreuses et développées", "des mitochondries rares et réduites",
                  "plus de hyaloplasme du tout"], 1,
                 "تفكر الصورة: une levure cultivée en milieu anaérobie possède…",
                 ("باقي عاقل على الصورة: بلا dioxygène، les mitochondries قلال وصغار، حيت la fermentation ما كتحتاجهمش.",
                  "Oui : sans dioxygène, les mitochondries sont rares et réduites, car la fermentation n'en a pas besoin."),
                 {0: (("هادي la levure ديال milieu aérobie. ف milieu anaérobie، واش la levure كتحتاج les mitochondries؟",
                       "C'est la levure du milieu aérobie. En milieu anaérobie, la levure a-t-elle besoin de mitochondries ?"),
                      ("بزاف وكبار، هادي مع le dioxygène. بلا dioxygène، les mitochondries قلال وصغار.",
                       "Nombreuses et développées, c'est avec dioxygène. Sans dioxygène : rares et réduites.")),
                  2: (("le hyaloplasme كاين ف كل خلية، وفيه كتوقع la fermentation. اللي كيتبدل هو شي organite. أشمن واحد؟",
                       "Le hyaloplasme existe dans toute cellule, et la fermentation s'y fait. C'est un organite qui change : lequel ?"),
                      ("le hyaloplasme ديما كاين. اللي كينقص ف milieu anaérobie هو les mitochondries: قلال وصغار.",
                       "Le hyaloplasme est toujours là. Ce qui diminue en milieu anaérobie, ce sont les mitochondries."))})),
        bloc("rf_s3_b2", "Le devenir du glucose",
             ["rf_a3_marquage", "rf_a3_glycolyse", "rf_a3_sans_o2", "rf_a3_avec_o2", "rf_a3_voyage1"],
             ["4. Le devenir du glucose",
              "Le marquage au ¹⁴C permet de suivre le glucose et ce qu'il devient.",
              "Définition : la glycolyse est la dégradation du glucose en deux acides pyruviques, dans le hyaloplasme ; elle est commune à la respiration et à la fermentation.",
              "Sans dioxygène : l'acide pyruvique reste dans le hyaloplasme et donne éthanol + CO₂.",
              "Avec dioxygène : l'acide pyruvique entre dans la mitochondrie, où il est dégradé en CO₂."],
             figures=["voyage"],
             retrouver=("qu'est-ce que la glycolyse, et où a-t-elle lieu ?",
                        "La glycolyse est la dégradation du glucose en deux acides pyruviques ; elle a lieu dans le "
                        "hyaloplasme, avec ou sans dioxygène.",
                        "C4", "بلا الدفتر: qu'est-ce que la glycolyse, et où a-t-elle lieu ?"),
             exercice=qcm(
                 "Des levures reçoivent du glucose marqué au ¹⁴C, sans dioxygène. À la fin, où retrouve-t-on la radioactivité ?",
                 ["Dans l'éthanol et le CO₂, hors de la cellule", "Dans les acides du cycle de Krebs, dans la mitochondrie",
                  "Dans le glucose, resté hors de la cellule"], 0,
                 "تبع le carbone marqué: des levures reçoivent du glucose marqué, sans dioxygène. À la fin, où est la radioactivité ?",
                 ("تبعتي le carbone حتى للخر: بلا dioxygène، le glucose كيولي éthanol و dioxyde de carbone، وكيخرجو.",
                  "Bien suivi : sans dioxygène, le glucose devient éthanol et CO₂, qui sortent de la cellule."),
                 {1: (("les acides du cycle de Krebs كاينين بصح، ولكن ف la mitochondrie، يعني مع le dioxygène. هنا ما كاينش.",
                       "Les acides du cycle de Krebs existent bien, mais dans la mitochondrie, donc avec dioxygène. Ici il n'y en a pas."),
                      ("بلا dioxygène، la mitochondrie ما كيدخل ليها والو. l'acide pyruvique كيولي éthanol و dioxyde de carbone.",
                       "Sans dioxygène, rien n'entre dans la mitochondrie : l'acide pyruvique devient éthanol et CO₂.")),
                  2: (("ف البداية le glucose كان برا، هادي صحيحة. ولكن السؤال على اللخر: واش le glucose بقا كيف ما كان؟",
                       "Au début le glucose est dehors, c'est vrai. Mais à la fin, est-il resté tel quel ?"),
                      ("le glucose دخل وتبدل. ف اللخر، le carbone marqué كاين ف l'éthanol و le dioxyde de carbone، برا الخلية.",
                       "Le glucose est entré et a été transformé. À la fin, le ¹⁴C est dans l'éthanol et le CO₂, dehors."))})),
    ]},
    {"id": "rf_s4", "titre": "Séance 4 — Activité 2 : la glycolyse", "blocs": [
        bloc("rf_s4_b1", "Deux rappels : l'ATP et le transporteur d'hydrogène",
             ["rf_g0_atp", "rf_g0_taxi"],
             ["II. La glycolyse",
              "Rappel : ATP + H₂O → ADP + Pi + énergie ; ADP + Pi + énergie → ATP.",
              "L'ATP est la forme d'énergie directement utilisable par la cellule.",
              "Rappel : NAD⁺ + 2 H⁺ + 2 e⁻ → NADH,H⁺ (transporteur d'hydrogène réduit)."],
             retrouver=("écris la réaction qui charge le transporteur NAD⁺.", "NAD⁺ + 2 H⁺ + 2 e⁻ → NADH,H⁺",
                        "C5", "تفكر الطاكسي: écris la réaction qui charge le transporteur N A D plus."),
             exercice=qcm(
                 "Quand la cellule a besoin d'énergie tout de suite, elle utilise…",
                 ["le glucose, directement", "le NAD⁺", "l'ATP, qui devient ADP + Pi"], 2,
                 "تفكر الدراهم الصغار: quand la cellule a besoin d'énergie tout de suite, elle utilise…",
                 ("هادي هي: l'ATP هو الدراهم الصغار ديال الخلية، وملي كيتخدم كيولي ADP و phosphate.",
                  "Oui : l'ATP est la monnaie de la cellule ; utilisé, il devient ADP + Pi."),
                 {0: (("le glucose فيه l'énergie بزاف، بصح. ولكن هو الورقة ديال مية درهم: واش كتخلص بيها حاجة صغيرة؟",
                       "Le glucose contient beaucoup d'énergie, mais c'est le billet de 100 dirhams : paie-t-on une petite chose avec ?"),
                      ("le glucose هو الورقة الكبيرة. la cellule كتخلص ب الدراهم الصغار: l'ATP.",
                       "Le glucose est le gros billet. La cellule paie avec la monnaie : l'ATP.")),
                  1: (("N A D plus مهم، ولكن هو طاكسي ديال les hydrogènes، ماشي ديال l'énergie. شكون هو الدراهم الصغار؟",
                       "NAD⁺ compte, mais c'est le taxi des hydrogènes, pas la monnaie. Qui est la monnaie de la cellule ?"),
                      ("N A D plus كيهز les hydrogènes. l'énergie اللي كتستعمل la cellule ف الحين هي l'ATP.",
                       "NAD⁺ transporte les hydrogènes. L'énergie utilisable tout de suite, c'est l'ATP."))})),
        bloc("rf_s4_b2", "Les trois phases et le bilan de la glycolyse",
             ["rf_g1_activation", "rf_g2_scission", "rf_g3_oxydation", "rf_g4_bilan"],
             ["1. Les trois phases de la glycolyse (dans le hyaloplasme)",
              "Phase 1, activation : le glucose (C6) reçoit 2 phosphates ; 2 ATP sont consommés.",
              "Phase 2, scission : le C6 est coupé en 2 C3 ; 2 NAD⁺ sont réduits en 2 NADH,H⁺.",
              "Phase 3, formation d'énergie : 4 ATP sont formés ; il reste 2 acides pyruviques.",
              "Formule : C₆H₁₂O₆ + 2 ADP + 2 Pi + 2 NAD⁺ → 2 CH₃-CO-COOH + 2 ATP + 2 NADH,H⁺",
              "Bilan : 4 ATP formés − 2 ATP consommés = 2 ATP, sans dioxygène."],
             figures=["glycolyse"],
             retrouver=("écris l'équation globale de la glycolyse.",
                        "C₆H₁₂O₆ + 2 ADP + 2 Pi + 2 NAD⁺ → 2 CH₃-CO-COOH + 2 ATP + 2 NADH,H⁺",
                        "C5", "سد الدفتر، وكتب: l'équation globale de la glycolyse."),
             exercice=qcm(
                 "Pendant la phase d'activation de la glycolyse, la cellule…",
                 ["consomme 2 ATP", "gagne 2 ATP", "réduit 2 NAD⁺"], 0,
                 "رجع ل la phase الأولى: pendant la phase d'activation de la glycolyse, la cellule…",
                 ("صحيح: ف l'activation، la cellule كتعطي deux ATP، باش le glucose يولي fructose diphosphate.",
                  "Oui : à l'activation, la cellule consomme 2 ATP ; le glucose devient fructose diphosphate."),
                 {1: (("la cellule كتربح ATP بصح، ولكن ف اللخر. ف l'activation، شنو كيوقع ل les deux ATP؟",
                       "La cellule gagne bien des ATP, mais à la fin. À l'activation, que deviennent les deux ATP ?"),
                      ("الربح كيجي ف la phase الثالثة. ف l'activation، la cellule كتعطي deux ATP.",
                       "Le gain vient dans la phase 3. À l'activation, la cellule consomme 2 ATP.")),
                  2: (("N A D plus كيولي réduit ف la glycolyse، صحيح. ولكن ف la phase الثانية، من بعد القسمة. و ف الأولى؟",
                       "NAD⁺ est bien réduit pendant la glycolyse, mais dans la phase 2, après la scission. Et dans la première ?"),
                      ("الطاكسيات كيتعمرو ف la phase الثانية. la phase الأولى، l'activation، فيها deux ATP كيمشيو.",
                       "Les transporteurs sont réduits dans la phase 2. La phase 1, l'activation, consomme 2 ATP."))})),
    ]},
    {"id": "rf_s5", "titre": "Séance 5 — Activité 3 : la mitochondrie, siège de la respiration", "blocs": [
        bloc("rf_s5_b1", "La mitochondrie utilise l'acide pyruvique",
             ["rf_m1_principe", "rf_m1_etapes", "rf_m2_glucose", "rf_m2_pyruvate"],
             ["III. La mitochondrie, siège de la respiration",
              "1. La mitochondrie utilise l'acide pyruvique",
              "Définition : la centrifugation sépare les constituants d'un mélange selon leur densité, par une rotation rapide.",
              "Des mitochondries isolées ne consomment pas de dioxygène avec le glucose ; elles en consomment avec l'acide pyruvique.",
              "Donc la mitochondrie utilise l'acide pyruvique, produit par la glycolyse, et non le glucose."],
             retrouver=("quel métabolite la mitochondrie utilise-t-elle, et d'où vient-il ?",
                        "La mitochondrie utilise l'acide pyruvique, produit par la glycolyse dans le hyaloplasme ; elle "
                        "n'utilise pas le glucose.",
                        "C6", "بلا الدفتر: quel métabolite la mitochondrie utilise-t-elle, et d'où vient-il ?"),
             exercice=qcm(
                 "Après une première centrifugation à faible vitesse d'un broyat de cellules, le culot contient surtout…",
                 ["les mitochondries", "les noyaux", "le hyaloplasme"], 1,
                 "تفكر l'essoreuse: après une première centrifugation à faible vitesse, le culot contient surtout…",
                 ("مزيان: ملي الدورة كتكون بالشوية، غير اللي lourd بزاف كيهبط، وهما les noyaux.",
                  "Oui : à faible vitesse, seuls les plus lourds descendent : les noyaux."),
                 {0: (("les mitochondries كيهبطو بصح ف شي culot، ولكن ف الدورة الثانية، اللي بسرعة كبيرة. و ف الأولى؟",
                       "Les mitochondries forment bien un culot, mais à la deuxième centrifugation, à grande vitesse. Et à la première ?"),
                      ("ف الدورة الأولى، les mitochondries كيبقاو ف le surnageant. le culot فيه les noyaux.",
                       "À la première centrifugation, les mitochondries restent dans le surnageant ; le culot contient les noyaux.")),
                  2: (("le hyaloplasme هو السائل ديال الخلية: واش السائل كيهبط لتحت، ولا كيبقى الفوق؟",
                       "Le hyaloplasme est le liquide de la cellule : un liquide va-t-il au fond, ou reste-t-il au-dessus ?"),
                      ("le hyaloplasme سائل، كيبقى ف le surnageant. le culot ديال الدورة الأولى فيه les noyaux.",
                       "Le hyaloplasme, liquide, reste dans le surnageant. Le premier culot contient les noyaux."))})),
        bloc("rf_s5_b2", "L'ultrastructure de la mitochondrie",
             ["rf_m3_zoom", "rf_m3_legender", "rf_m3_construire"],
             ["2. L'ultrastructure de la mitochondrie",
              "La mitochondrie est un organite en bâtonnet, de 0,5 à 1 µm de diamètre, à double membrane.",
              "La membrane interne forme des crêtes, qui portent des sphères pédonculées ; à l'intérieur : la matrice.",
              "Remarque : la matrice contient l'ADN mitochondrial."],
             figures=["mitochondrie"],
             retrouver=("cite les six légendes de la mitochondrie.",
                        "Membrane externe, espace intermembranaire, membrane interne, crêtes, matrice, sphères pédonculées.",
                        "C7", "سد الدفتر: cite les six légendes de la mitochondrie."),
             exercice=qcm(
                 "Les sphères pédonculées sont portées par…",
                 ["la membrane externe", "la matrice", "la membrane interne (les crêtes)"], 2,
                 "تفكر الدائرة المكبرة: les sphères pédonculées sont portées par…",
                 ("صحيح: les sphères pédonculées لاصقين ف la membrane interne، على les crêtes.",
                  "Oui : les sphères pédonculées sont attachées à la membrane interne, sur les crêtes."),
                 {0: (("la membrane externe هي اللي برا، وهي ملسة. شوف الغشاء اللي كيدخل ويخرج.",
                       "La membrane externe est celle du dehors, lisse. Regarde plutôt la membrane qui se replie."),
                      ("ماشي la membrane externe: les sphères pédonculées كاينين ف la membrane interne، على les crêtes.",
                       "Pas la membrane externe : les sphères sont sur la membrane interne, le long des crêtes.")),
                  1: (("les sphères كيشوفو جهة la matrice، بصح. ولكن la matrice ماشي غشاء: فين لاصقين؟",
                       "Les sphères sont tournées vers la matrice, c'est vrai. Mais la matrice n'est pas une membrane : où sont-elles attachées ?"),
                      ("la matrice هي الوسط. les sphères pédonculées لاصقين ف la membrane interne.",
                       "La matrice est l'intérieur. Les sphères pédonculées sont attachées à la membrane interne."))})),
        bloc("rf_s5_b3", "La composition de la mitochondrie",
             ["rf_m4_membranes", "rf_m4_matrice"],
             ["3. La composition de la mitochondrie",
              "| | Lipides | Protéines |",
              "| Membrane externe | 40 % | 60 % |",
              "| Membrane interne | 20 % | 80 % |",
              "Membrane interne : enzymes d'oxydoréduction, transporteurs d'électrons, ATP synthase (sphères pédonculées).",
              "Matrice : acide pyruvique, pas de glucose ; décarboxylases (retirent du CO₂) et déshydrogénases (retirent des H).",
              "Donc la membrane interne et la matrice sont des lieux de réactions."],
             retrouver=("que font les décarboxylases et les déshydrogénases de la matrice ?",
                        "Les décarboxylases retirent du CO₂ ; les déshydrogénases retirent des hydrogènes, pris par les "
                        "transporteurs (NAD⁺).",
                        "C8", "بلا الدفتر: que font les décarboxylases, et les déshydrogénases de la matrice ?"),
             exercice=qcm(
                 "Dans la matrice de la mitochondrie, on ne trouve pas…",
                 ["d'acide pyruvique", "de glucose", "d'ATP"], 1,
                 "رد البال ل pas: dans la matrice de la mitochondrie, on ne trouve pas…",
                 ("قريتي السؤال حتى للخر، مزيان: ما كاينش le glucose، حيت la mitochondrie كتستعمل l'acide pyruvique.",
                  "Bien lu jusqu'au bout : pas de glucose, car la mitochondrie utilise l'acide pyruvique."),
                 {0: (("l'acide pyruvique هو بالضبط اللي كيدخل ل la mitochondrie. السؤال على اللي ما كاينش. عاود قراه.",
                       "L'acide pyruvique est justement ce qui entre dans la mitochondrie. On cherche ce qui n'y est pas : relis."),
                      ("l'acide pyruvique كاين ف la matrice. اللي ما كاينش هو le glucose: كيتفكك برا، ف le hyaloplasme.",
                       "L'acide pyruvique est dans la matrice. Ce qui manque, c'est le glucose, dégradé dans le hyaloplasme.")),
                  2: (("l'ATP كاين ف la matrice، مع l'ADP و le phosphate. فكر ف التجربة ديال les mitochondries بوحدهم.",
                       "L'ATP est dans la matrice, avec l'ADP et le phosphate. Pense à l'expérience des mitochondries isolées."),
                      ("l'ATP كاين. اللي ما كاينش هو le glucose: la mitochondrie ما كتستعملوش.",
                       "L'ATP y est. Ce qui manque, c'est le glucose : la mitochondrie ne l'utilise pas."))})),
        bloc("rf_s5_b4", "Bilan du chapitre : retenir et réviser",
             ["rf_b1_bilan", "rf_b2_voyage", "rf_fermeture_cours"],
             ["Bilan : glucose → glycolyse (hyaloplasme) → 2 acides pyruviques.",
              "Avec O₂ : l'acide pyruvique entre dans la mitochondrie (respiration) ; sans O₂ : éthanol + CO₂ (fermentation).",
              "À suivre : que devient l'acide pyruvique dans la matrice ?",
              "Méthode : pour réviser : 1) relire le cahier 2) refaire seul les exercices du national 3) rédiger : décrire → déduire → expliquer"]),
    ]},
]
