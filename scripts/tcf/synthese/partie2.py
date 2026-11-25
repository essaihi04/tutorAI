# -*- coding: utf-8 -*-
"""Séances 3 à 5 : constantes physiques, CCM, application (acétate de benzyle), bilan, carte, fermeture."""
from outils import diapo, question, demonstration

A3, A4, A5, A6 = 'sy_partie3', 'sy_partie4', 'sy_partie5', 'sy_bilan'

# ── Bloc 7 : identifier par les constantes physiques ───────────────────────────────────────────────────────────
diapo(A3, 'sy_i1_pourquoi', 'Identifier le produit obtenu', 'On mesure ses caractéristiques physiques et on compare aux tables.',
      'درنا واحد le produit. ولكن كيفاش نعرفو واش هو l’espèce اللي بغينا؟ نقيسو les caractéristiques physiques ديالو. '
      'اللولة: la température de fusion ولا la température d’ébullition. الثانية: la solubilité، واش كيذوب ولا لا. '
      'الثالثة: la masse volumique و la densité. وفاللخر، كنقارنو مع les valeurs ديال les tables. '
      'يلا كانو نفس les valeurs، فهي نفس l’espèce.',
      url='constantes.html?vue=pourquoi',
      pointage=[('درنا واحد le produit', 'produit'), ('اللولة: la température', 'temperature'), ('الثانية: la solubilité', 'solubilite'),
                ('الثالثة: la masse volumique', 'densite'), ('وفاللخر، كنقارنو', 'tables')],
      centre=[('mêmes valeurs que les tables → même espèce', 'يلا كانو نفس les valeurs')],
      cahier='III. Identifier l’espèce synthétisée\n1. Les caractéristiques physiques\nOn compare ses caractéristiques physiques (températures de fusion et d’ébullition, solubilité, ρ, d) aux valeurs des tables.',
      comp=['C7'])

diapo(A3, 'sy_i2_temperature', 'La température de fusion ou d’ébullition', 'Une valeur mesurée, comparée à la table.',
      'ناخدو مثال. عندنا واحد le solide بيض فواحد le tube، وكنسخنوه فواحد le bain d’huile. شوف le thermomètre: كيطلع. '
      'عند cent vingt-deux degrés Celsius، le solide كيذوب: هادي la température de fusion ديالو. '
      'دابا نشوفو la table. شكون عندو cent vingt-deux degrés؟ l’acide benzoïque. إذن le solide ديالنا هو l’acide benzoïque. '
      'دابا نتا: واحد le liquide كيغلي عند soixante-dix-huit degrés Celsius. قارن مع la table.',
      url='constantes.html?vue=temperature',
      pointage=[('شوف le thermomètre', 'monte'), ('le solide كيذوب', 'fond'), ('دابا نشوفو la table', 'tables'),
                ('إذن le solide ديالنا', 'compare'), ('دابا نتا', 'atoi')],
      centre=[('fusion : 122 °C → acide benzoïque', 'إذن le solide ديالنا')],
      cahier='Méthode : mesurer la température de fusion (ou d’ébullition), puis chercher la même valeur dans la table.', comp=['C7'],
      q=question('qcm', 'Un liquide bout à 78 °C. D’après la table (eau 100 °C, éthanol 78 °C, cyclohexane 81 °C), c’est…',
                 ['l’eau', 'le cyclohexane', 'l’éthanol'], 2,
                 'شوف هاد السؤال: واحد le liquide كيغلي عند soixante-dix-huit degrés. شكون هو، على حساب la table؟',
                 [(('l’eau كتغلي عند cent degrés، ماشي soixante-dix-huit.', 'L’eau bout à 100 °C, pas à 78 °C.'),
                   ('الجواب: l’éthanol، حيت كيغلي عند soixante-dix-huit degrés.', 'Réponse : l’éthanol, qui bout à 78 °C.')),
                  (('le cyclohexane كيغلي عند quatre-vingt-un degrés. قلب على نفس القيمة بالضبط.', 'Le cyclohexane bout à 81 °C : cherche la même valeur exacte.'),
                   ('الجواب: l’éthanol، soixante-dix-huit degrés.', 'Réponse : l’éthanol (78 °C).')),
                  ('برافو! نفس la valeur ف la table: c’est l’éthanol.', 'Bonne réponse : même valeur que la table : l’éthanol.')]),
      apres=[{'sim_avant': {'conclusions': False},
              'etapes': [{'commande': 'set_parameters', 'parametres': {'conclusions': True}}, {'commande': 'play_until', 'parametres': {'moment': 'reponse'}}, {'repere': 'reponse'}],
              'duree_s': 6}])

diapo(A3, 'sy_i3_solubilite', 'La solubilité', 'Se dissoudre, ou non, dans un solvant.',
      'la solubilité، يعني واش واحد l’espèce كتذوب فواحد le solvant. شوف le sucre فالما: كيختفي، كيذوب. le sucre soluble dans l’eau. '
      'دابا شوف l’huile فالما: كتبقى فوق، ماكتذوبش. l’huile non soluble dans l’eau. '
      'إذن la solubilité هي القدرة ديال l’espèce باش تذوب فواحد le solvant.',
      url='constantes.html?vue=solubilite',
      pointage=[('شوف le sucre فالما', 'sucre'), ('دابا شوف l’huile فالما', 'huile'), ('إذن la solubilité', 'bilan')],
      centre=[('sucre : soluble dans l’eau', 'le sucre soluble'), ('huile : non soluble dans l’eau', 'l’huile non soluble')],
      cahier='Définition : la solubilité est la capacité d’une espèce à se dissoudre dans un solvant.', comp=['C7'])

# ── Bloc 8 : masse volumique et densité ──────────────────────────────────────────────────────────────────────────
diapo(A3, 'sy_i4_masse', 'Calculer une masse volumique', 'ρ = m/V : la masse d’un volume de liquide.',
      'كيفاش نحسبو la masse volumique؟ كنحطو l’éprouvette خاوية فوق la balance، وكنديرو zéro. '
      'من بعد نزيدو dix millilitres ديال le liquide. la balance كتبين huit grammes. '
      'la relation: rho égale m sur V، يعني la masse على le volume. '
      'l’application: rho égale huit grammes sur dix millilitres، يعني zéro virgule huit gramme par millilitre.',
      url='constantes.html?vue=masse',
      pointage=[('l’éprouvette خاوية', 'tare'), ('نزيدو dix millilitres', 'verse'), ('la balance كتبين', 'pese'), ('la relation', 'formule'),
                ('l’application', 'calcul')],
      centre=[('ρ = m/V', 'la relation'), ('ρ = 8 g/10 mL = 0,8 g/mL', 'l’application')],
      cahier='Formule : ρ = m/V (m en g, V en mL : ρ en g/mL)',
      figures=None, comp=['C7'])

diapo(A3, 'sy_i5_densite', 'Calculer une densité', 'd = ρ/ρ(eau), sans unité.',
      'دابا la densité. اللول، شوف الما: dix millilitres ديال الما، la masse ديالهم dix grammes. إذن rho de l’eau égale un gramme par millilitre. '
      'la relation: d égale rho sur rho de l’eau. ماعندهاش unité. '
      'ل le liquide ديالنا: d égale zéro virgule huit sur un، يعني zéro virgule huit. '
      'و d صغر من un، إذن le liquide كيبقى فوق الما. دابا نتا: le liquide B، vingt millilitres، la masse ديالهم vingt-deux grammes.',
      url='constantes.html?vue=densite',
      pointage=[('شوف الما', 'eau'), ('إذن rho de l’eau', 'rho_eau'), ('la relation: d égale', 'formule'), ('ل le liquide ديالنا', 'calcul'),
                ('كيبقى فوق الما', 'flotte'), ('دابا نتا', 'atoi')],
      centre=[('ρ(eau) = 1 g/mL', 'إذن rho de l’eau'), ('d = ρ/ρ(eau)', 'la relation: d égale')],
      cahier='Formule : d = ρ/ρ(eau), sans unité ; ρ(eau) = 1 g/mL\nRemarque : d < 1 : le liquide flotte sur l’eau ; d > 1 : il coule.', comp=['C7'],
      q=question('qcm', 'Liquide B : 20 mL pèsent 22 g. Sa densité est…', ['0,9', '1,1', '22'], 1,
                 'شوف هاد السؤال: le liquide B، vingt millilitres، la masse ديالهم vingt-deux grammes. شحال هي la densité ديالو؟',
                 [(('قلبتي: قسمتي le volume على la masse. rho égale m sur V.', 'Tu as inversé : ρ = m/V, pas V/m.'),
                   ('الجواب: rho égale vingt-deux sur vingt، يعني un virgule un، و d égale un virgule un.', 'Réponse : ρ = 22/20 = 1,1 g/mL ; d = 1,1.')),
                  ('برافو! rho un virgule un gramme par millilitre، و d un virgule un.', 'Bonne réponse : ρ = 1,1 g/mL, d = 1,1.'),
                  (('vingt-deux هي la masse. خاصك تقسم على le volume.', '22 est la masse : il faut diviser par le volume.'),
                   ('الجواب: d égale un virgule un.', 'Réponse : d = 1,1.'))],
                 demo=demonstration(
                     'les données: m égale vingt-deux grammes، و V égale vingt millilitres. la relation: rho égale m sur V. '
                     'l’application: rho égale vingt-deux sur vingt، يعني un virgule un gramme par millilitre. '
                     'من بعد: d égale rho sur rho de l’eau. d égale un virgule un sur un، يعني un virgule un، sans unité. '
                     'و d كبر من un، إذن le liquide B كيبقى تحت الما.',
                     [('Données : m = 22 g ; V = 20 mL', 'les données'), ('ρ = m/V', 'la relation'),
                      ('ρ = 22/20 = 1,1 g/mL', 'l’application'), ('d = ρ/ρ(eau)', 'من بعد'),
                      ('d = 1,1/1 = 1,1 (sans unité)', 'd égale un virgule un sur un'), ('d > 1 : B coule sous l’eau', 'و d كبر من un')])),
      apres=[{'sim_avant': {'conclusions': False},
              'etapes': [{'commande': 'set_parameters', 'parametres': {'conclusions': True}}, {'commande': 'play_until', 'parametres': {'moment': 'reponse'}}, {'repere': 'reponse'}],
              'duree_s': 7}])

# ── Bloc 9 : la CCM pas à pas ────────────────────────────────────────────────────────────────────────────────────
diapo(A4, 'sy_c1_principe', 'La CCM : le principe', 'Une phase fixe, une phase mobile : les espèces se séparent.',
      'كاينة طريقة أخرى باش نعرفو l’espèce: la chromatographie sur couche mince، كنقولو ليها la CCM. '
      'شوف la plaque: عليها واحد la couche بيضا. هي la phase fixe، ماكتحركش. '
      'من بعد كنحطوها فواحد la cuve مسدودة، فيها شوية ديال واحد le solvant: l’éluant. هو la phase mobile. '
      'دابا l’éluant كيطلع فla plaque، وكيجر معاه les espèces. وكل espèce كتطلع بالسرعة ديالها: الزرقا طلعات بزاف، والحمرا شوية. '
      'إذن les espèces كيتفرقو.',
      url='ccm.html?vue=principe',
      pointage=[('شوف la plaque', 'plaque'), ('هي la phase fixe', '@plaque'), ('فواحد la cuve مسدودة', 'cuve'), ('هو la phase mobile', '@cuve'),
                ('دابا l’éluant كيطلع', 'monte'), ('إذن les espèces كيتفرقو', 'bilan')],
      centre=[('plaque : phase fixe', 'هي la phase fixe'), ('éluant : phase mobile', 'هو la phase mobile')],
      cahier='3. La chromatographie sur couche mince (CCM)\n| Phase fixe | Phase mobile |\n| la plaque (gel de silice) | l’éluant (un solvant) |\nL’éluant monte et sépare les espèces.',
      comp=['C8'])

diapo(A4, 'sy_c2_depot', 'La CCM : les dépôts', 'Une ligne au crayon, trois petites gouttes.',
      'الخطوة اللولة: كنرسمو بالقلم ديال الرصاص une ligne de dépôt، un centimètre من التحت. '
      'من بعد، بواحد le tube رقيق، كنحطو نقطة صغيرة: A، واحد l’espèce pure، هي la référence. '
      'من بعد B، espèce pure أخرى. وفاللخر P، le produit اللي بغينا نحللو. '
      'ومن بعد، كنخليو les dépôts ينشفو.',
      url='ccm.html?vue=depot',
      pointage=[('une ligne de dépôt', 'ligne'), ('كنحطو نقطة صغيرة: A', 'depotA'), ('من بعد B', 'depotB'), ('وفاللخر P', 'depotP'),
                ('كنخليو les dépôts ينشفو', 'sec')],
      centre=[('ligne de dépôt au crayon, à 1 cm', 'une ligne de dépôt')],
      cahier='Méthode : 1) tracer au crayon la ligne de dépôt à 1 cm du bas ; 2) déposer une petite goutte de chaque échantillon ; 3) laisser sécher.',
      comp=['C8'])

diapo(A4, 'sy_c3_elution', 'La CCM : l’éluant monte', 'La cuve fermée, l’éluant sous la ligne de dépôt.',
      'دابا كنحطو la plaque ف la cuve. رد البال: l’éluant خاصو يبقى تحت la ligne de dépôt، باش les dépôts ما يذوبوش فيه. '
      'من بعد كنسدو la cuve بالغطا، باش l’éluant مايتبخرش. '
      'شوف: l’éluant كيطلع شوية بشوية، وكيجر معاه les espèces. '
      'قبل ما يوصل للفوق، كنخرجو la plaque، وكنرسمو بالقلم الحد اللي وصل ليه: le front de l’éluant.',
      url='ccm.html?vue=elution',
      pointage=[('دابا كنحطو la plaque', 'plonger'), ('تحت la ligne de dépôt', 'niveau'), ('كنسدو la cuve', 'couvercle'),
                ('l’éluant كيطلع شوية بشوية', 'monte'), ('le front de l’éluant', 'front')],
      centre=[('éluant sous la ligne de dépôt', 'تحت la ligne de dépôt'), ('cuve fermée', 'كنسدو la cuve')],
      cahier='Méthode : 4) éluant sous la ligne de dépôt, cuve fermée ; 5) sortir la plaque avant le haut et marquer le front de l’éluant.',
      comp=['C8'])

diapo(A4, 'sy_c4_revelation', 'La CCM : la révélation', 'Lampe UV ou vapeurs de diiode.',
      'ملي كتنشف la plaque، بزاف ديال المرات ماكنشوفو والو: les espèces incolores. '
      'كنحطوها تحت واحد la lampe UV: les taches كيبانو. وكندورو عليهم بالقلم. '
      'ولا كنحطوها فواحد البوقال فيه le diiode: les taches كيوليو قهويين. '
      'دابا عندنا le chromatogramme.',
      url='ccm.html?vue=revelation',
      pointage=[('les espèces incolores', 'incolores'), ('la lampe UV', 'uv'), ('le diiode', 'diiode'), ('le chromatogramme', 'chromatogramme')],
      centre=[('révéler : lampe UV ou diiode', 'la lampe UV')],
      cahier='Méthode : 6) révéler les taches incolores : lampe UV ou vapeurs de diiode.\nOn obtient le chromatogramme.', comp=['C8'],
      q=question('qcm', 'Pourquoi la ligne de dépôt doit-elle rester au-dessus de l’éluant ?',
                 ['pour que les dépôts ne se dissolvent pas dans l’éluant', 'pour que l’éluant ne s’évapore pas', 'pour voir les taches sous UV'], 0,
                 'شوف هاد السؤال: علاش la ligne de dépôt خاصها تبقى فوق l’éluant؟',
                 [('برافو! يلا كانو les dépôts تحت l’éluant، كيذوبو فl’éluant فالقاع ديال la cuve.', 'Bonne réponse : sinon les dépôts se dissolvent dans l’éluant.'),
                  (('باش l’éluant مايتبخرش، كنسدو la cuve. هادا دور آخر.', 'Contre l’évaporation, on ferme la cuve : c’est un autre rôle.'),
                   ('الجواب: باش les dépôts ما يذوبوش ف l’éluant.', 'Réponse : pour que les dépôts ne se dissolvent pas dans l’éluant.')),
                  (('la lampe UV كتبين les taches من بعد. السؤال على la ligne de dépôt.', 'L’UV sert après ; la question porte sur la ligne de dépôt.'),
                   ('الجواب: باش les dépôts ما يذوبوش ف l’éluant.', 'Réponse : pour que les dépôts ne se dissolvent pas dans l’éluant.'))]))

# ── Bloc 10 : lire un chromatogramme ────────────────────────────────────────────────────────────────────────────
diapo(A4, 'sy_c5_compter', 'Lire le chromatogramme : compter les taches', 'Une espèce pure donne une seule tache.',
      'دابا نقراو le chromatogramme. نحسبو les taches ديال كل dépôt. A: une tache. B: une tache. '
      'P: une، deux taches. إذن A و B espèces pures: كل وحدة عندها غير tache واحدة. '
      'و P فيه deux espèces، إذن هو un mélange.',
      url='ccm.html?vue=compter',
      pointage=[('A: une tache', 'A'), ('B: une tache', 'B'), ('P: une، deux taches', 'P'), ('إذن A و B espèces pures', 'conclusion')],
      centre=[('espèce pure : une seule tache', 'إذن A و B espèces pures'), ('plusieurs taches : un mélange', 'هو un mélange')],
      cahier='| Une seule tache | Plusieurs taches |\n| une espèce pure | un mélange |', comp=['C8'])

diapo(A4, 'sy_c6_identifier', 'Lire le chromatogramme : la même hauteur', 'Même hauteur, même espèce.',
      'دابا كيفاش نعرفو شنو كاين ف P؟ نقارنو الطول. tache ديال P فنفس الطول ديال A: إذن P فيه A. '
      'و la tache الأخرى فنفس الطول ديال B: إذن P فيه B. '
      'القاعدة: deux taches à la même hauteur، c’est la même espèce. إذن P ماشي pur: فيه A و B.',
      url='ccm.html?vue=identifier',
      pointage=[('فنفس الطول ديال A', 'hauteurA'), ('فنفس الطول ديال B', 'hauteurB'), ('القاعدة', 'conclusion'), ('إذن P ماشي pur', 'pure')],
      centre=[('même hauteur → même espèce', 'القاعدة')],
      cahier='Deux taches à la même hauteur correspondent à la même espèce.', comp=['C8'])

diapo(A4, 'sy_c7_rf', 'Le rapport frontal Rf', 'Rf = h/H, sans unité, entre 0 et 1.',
      'باش نعطيو رقم ل كل espèce، كنحسبو le rapport frontal، Rf. نقيسو بالمسطرة. '
      'H: من la ligne de dépôt حتى le front. نحسبو: un، deux، trois… huit. H égale huit centimètres. '
      'h: من la ligne de dépôt حتى الوسط ديال la tache. ل A: quatre centimètres. '
      'la relation: Rf égale h sur H. ماعندوش unité، وديما بين zéro و un. '
      'Rf de A égale quatre sur huit، يعني zéro virgule cinq. ول B، h égale deux centimètres. '
      'Rf de B égale deux sur huit، يعني zéro virgule vingt-cinq. '
      'و Rf de A كبر: إذن A plus soluble dans l’éluant، طلع كثر.',
      url='ccm.html?vue=rf',
      pointage=[('نقيسو بالمسطرة', '@regle'), ('H: من la ligne de dépôt', 'H'), ('ل A: quatre centimètres', 'hA'), ('la relation: Rf égale', 'formule'),
                ('Rf de A égale quatre sur huit', 'calculA'), ('ول B، h égale', 'hB'), ('Rf de B égale deux sur huit', 'calculB'),
                ('و Rf de A كبر', 'soluble')],
      centre=[('Rf = h/H', 'la relation: Rf égale'), ('Rf grand : plus soluble dans l’éluant', 'و Rf de A كبر')],
      cahier='Formule : Rf = h/H (h : de la ligne de dépôt au centre de la tache ; H : de la ligne de dépôt au front), sans unité, 0 < Rf < 1\nRemarque : plus Rf est grand, plus l’espèce est soluble dans l’éluant.',
      figures=[{'type': 'schema', 'titre': 'Le rapport frontal', 'legende': 'h et H se mesurent depuis la ligne de dépôt.',
                'cadre': {'l': 8, 'h': 10},
                'elements': [
                    {'f': 'rect', 'de': [2, 0], 'a': [5, 10]},
                    {'f': 'ligne', 'pts': [[2, 1], [5, 1]], 'couleur': 'blanc'},
                    {'f': 'ligne', 'pts': [[2, 9], [5, 9]], 'trait': 'pointille', 'couleur': 'blanc'},
                    {'f': 'ellipse', 'c': [3.5, 5], 'rx': 0.35, 'ry': 0.25, 'couleur': 'violet', 'remplir': 'violet'},
                    {'f': 'cote', 'de': [5.7, 1], 'a': [5.7, 9], 't': 'H', 'pos': 'e'},
                    {'f': 'cote', 'de': [2.9, 1], 'a': [2.9, 5], 't': 'h', 'pos': 'o'},
                    {'f': 'texte', 'at': [6.3, 9], 't': 'front', 'ancre': 'gauche'},
                    {'f': 'texte', 'at': [6.3, 1], 't': 'ligne de dépôt', 'ancre': 'gauche'}]}],
      comp=['C8'])

diapo(A4, 'sy_c8_rf_eleve', 'À toi : calculer un Rf', 'Une autre plaque, une autre espèce.',
      'دابا نتا. هادي plaque أخرى، فيها l’espèce X. نقيسو H: من la ligne de dépôt حتى le front، dix centimètres. '
      'و h: من la ligne de dépôt حتى الوسط ديال la tache، six centimètres. '
      'دابا نتا: احسب Rf de X.',
      url='ccm.html?vue=rf_eleve',
      pointage=[('هادي plaque أخرى', 'plaque'), ('نقيسو H', 'H'), ('و h: من la ligne de dépôt', 'h'), ('دابا نتا: احسب', 'atoi')],
      cahier='Méthode : 1) mesurer H ; 2) mesurer h ; 3) Rf = h/H.', comp=['C8'],
      q=question('qcm', 'H = 10 cm et h = 6 cm. Le rapport frontal de X est…', ['0,6', '1,67', '6'], 0,
                 'شوف هاد السؤال: H égale dix centimètres، و h égale six centimètres. شحال هو Rf de X؟',
                 [('برافو! Rf égale six sur dix، يعني zéro virgule six، بلا unité.', 'Bonne réponse : Rf = 6/10 = 0,6, sans unité.'),
                  (('قلبتي: Rf égale h sur H، ماشي H sur h. و Rf ديما صغر من un.', 'Tu as inversé : Rf = h/H, et Rf est toujours inférieur à 1.'),
                   ('الجواب: Rf égale six sur dix، يعني zéro virgule six.', 'Réponse : Rf = 6/10 = 0,6.')),
                  (('six هي h بوحدها. خاصك تقسم على H.', '6 est h seul : il faut diviser par H.'),
                   ('الجواب: zéro virgule six.', 'Réponse : 0,6.'))],
                 demo=demonstration(
                     'les données: h égale six centimètres، و H égale dix centimètres. la relation: Rf égale h sur H. '
                     'l’application: Rf égale six sur dix. le résultat: Rf égale zéro virgule six، sans unité، وهو بين zéro و un.',
                     [('Données : h = 6 cm ; H = 10 cm', 'les données', ['cote_h', 'cote_H']), ('Rf = h/H', 'la relation'),
                      ('Rf = 6/10', 'l’application'), ('Rf = 0,6 (sans unité, entre 0 et 1)', 'le résultat', 'reponse')])),
      apres=[{'sim_avant': {'conclusions': False},
              'etapes': [{'commande': 'set_parameters', 'parametres': {'conclusions': True}}, {'commande': 'play_until', 'parametres': {'moment': 'reponse'}}, {'repere': 'l_reponse'}],
              'duree_s': 6}])

# ── Bloc 11 : l'application du livre, avec nos valeurs ─────────────────────────────────────────────────────────
diapo(A5, 'sy_a1_enonce', 'Application : la synthèse de l’acétate de benzyle', 'Une odeur de jasmin, par chauffage à reflux.',
      'دابا تطبيق. باش نصاوبو l’acétate de benzyle، اللي عندو الريحة ديال الياسمين، كنخلطو l’alcool benzylique و l’acide acétique، '
      'وكنسخنو à reflux. دابا نعطيو الأسماء ديال le montage. un: le réfrigérant à boules. deux: le ballon. trois: le chauffe-ballon. '
      'quatre: le support élévateur. وعلاش le reflux؟ الحرارة كتزرب la réaction، و le réfrigérant كيرجع les vapeurs، باش مانضيعو والو.',
      url='montage.html?vue=application',
      pointage=[('l’alcool benzylique و l’acide acétique', 'reactifs'), ('وكنسخنو à reflux', 'chauffage'),
                ('دابا نعطيو الأسماء', 'numeros'), ('un: le réfrigérant', 'noms'), ('un: le réfrigérant', '@n1'), ('deux: le ballon', '@n2'),
                ('trois: le chauffe-ballon', '@n3'), ('quatre: le support', '@n4'), ('وعلاش le reflux', 'role')],
      centre=[('alcool benzylique + acide acétique → acétate de benzyle', 'l’alcool benzylique و l’acide acétique')],
      cahier='Application : synthèse de l’acétate de benzyle (odeur de jasmin) par chauffage à reflux.', comp=['C4', 'C5'])

diapo(A5, 'sy_a2_chromatogramme', 'Application : le chromatogramme', 'Quatre dépôts : A, B, C, D.',
      'من بعد la synthèse، درنا CCM فيها quatre dépôts. A: l’alcool benzylique pur. B: l’acétate de benzyle اللي كنشريوه. '
      'C: le liquide فاللخر ديال la synthèse. D: un extrait naturel de jasmin. '
      'نحسبو les taches ديال D: une، deux، trois. إذن D فيه trois espèces. '
      'دابا C: عندو deux taches. شوف الطول ديالهم. '
      'tache فنفس الطول ديال A، و tache فنفس الطول ديال B. إذن C فيه l’acétate de benzyle اللي تصاوب، وشوية ديال l’alcool اللي بقا.',
      url='ccm.html?vue=application',
      pointage=[('quatre dépôts', 'depots'), ('نحسبو les taches ديال D', 'compterD'), ('دابا C', 'C'), ('إذن C فيه l’acétate', 'conclusion')],
      centre=[('D : 3 taches → 3 espèces', 'إذن D فيه trois espèces'), ('C : A + B', 'إذن C فيه l’acétate')],
      obs={'apres_mot': 'شوف الطول ديالهم.', 'sim_avant': {'conclusions': False}, 'sim_apres': {'conclusions': True},
           'gestes': [{'commande': 'play_until', 'parametres': {'moment': 'C'}}, {'repere': 'depot_C'}],
           'enonce': 'Les deux taches de C sont à la hauteur de quelles taches ?',
           'enonce_dit': 'شوف les deux taches ديال C. فنفس الطول ديال شكون؟', 'silence_s': 8,
           'indices': [{'texte': 'Suis les lignes pointillées vers la gauche.', 'dit': 'تبع الخطوط المقطعين لليسر.', 'repere': 'depot_A'},
                       {'texte': 'Une ligne passe par A, l’autre par B.', 'dit': 'خط كيدوز من A، والآخر من B.', 'repere': 'depot_B'}],
           'choix': ['à la hauteur de A et de B', 'seulement à la hauteur de B', 'à la hauteur des taches de D'], 'bonne': 0,
           'retours': [{'parole': 'برافو! وحدة فطول A، والأخرى فطول B.', 'ecrit': 'Oui : une tache à la hauteur de A, l’autre à la hauteur de B.'},
                       {'parole': 'شوف مزيان: كاينة حتى tache لتحت، فنفس الطول ديال A.', 'ecrit': 'Regarde : la tache du bas est à la hauteur de A.'},
                       {'parole': 'لا، قارن مع A و B، هوما les références.', 'ecrit': 'Non : compare avec A et B, les références.'}],
           'solution': {'parole': 'C فيه tache فطول A، و tache فطول B: إذن فيه A و B.', 'ecrit': 'C : une tache à la hauteur de A, une à la hauteur de B : C contient A et B.'}},
      cahier='Méthode : 1) compter les taches d’un dépôt ; 2) chercher les taches à la même hauteur que les références.', comp=['C8'])

diapo(A5, 'sy_a3_rf', 'Application : les rapports frontaux', 'Calculer Rf(A) et Rf(B), puis comparer.',
      'دابا نحسبو les Rf. H: من la ligne de dépôt حتى le front، dix centimètres. '
      'h de A: trois centimètres. إذن Rf de A égale trois sur dix، يعني zéro virgule trois. '
      'h de B: six centimètres. دابا نتا: احسب Rf de B، وقول شكون plus soluble dans l’éluant.',
      url='ccm.html?vue=application_rf',
      pointage=[('H: من la ligne de dépôt', 'H'), ('h de A', 'hA'), ('إذن Rf de A', 'rfA'), ('h de B', 'hB'), ('دابا نتا', 'atoi')],
      cahier='Remarque : on révèle une espèce incolore avec une lampe UV ou des vapeurs de diiode.', comp=['C8'],
      q=question('qcm', 'H = 10 cm, h(B) = 6 cm. Rf(B) vaut… et l’espèce la plus soluble dans l’éluant est…',
                 ['0,6 ; B est la plus soluble', '0,6 ; A est la plus soluble', '6 ; B est la plus soluble'], 0,
                 'شوف هاد السؤال: H égale dix centimètres، و h de B égale six centimètres. شحال Rf de B، وشكون plus soluble؟',
                 [('برافو! Rf de B zéro virgule six، كبر من zéro virgule trois: B plus soluble dans l’éluant.', 'Bonne réponse : Rf(B) = 0,6 > Rf(A) = 0,3 : B est plus soluble.'),
                  (('le calcul صحيح. ولكن شكون عندو Rf كبر؟', 'Le calcul est juste ; mais qui a le plus grand Rf ?'),
                   ('الجواب: B، حيت Rf de B كبر، وطلع كثر.', 'Réponse : B, car son Rf est le plus grand.')),
                  (('Rf ماعندوش unité وديما صغر من un. خاصك تقسم على H.', 'Rf est sans unité et inférieur à 1 : divise par H.'),
                   ('الجواب: zéro virgule six، و B plus soluble.', 'Réponse : 0,6 ; B est la plus soluble.'))],
                 demo=demonstration(
                     'les données: h de B égale six centimètres، و H égale dix centimètres. la relation: Rf égale h sur H. '
                     'l’application: Rf de B égale six sur dix، يعني zéro virgule six. '
                     'نقارنو: zéro virgule six كبر من zéro virgule trois. إذن B plus soluble dans l’éluant.',
                     [('Données : h(B) = 6 cm ; H = 10 cm', 'les données', ['cote_hB', 'cote_H']), ('Rf = h/H', 'la relation'),
                      ('Rf(B) = 6/10 = 0,6', 'l’application', 'rfB'), ('Rf(B) = 0,6 > Rf(A) = 0,3', 'نقارنو'),
                      ('B est plus soluble dans l’éluant', 'إذن B plus soluble', 'soluble')])),
      apres=[{'sim_avant': {'conclusions': False},
              'etapes': [{'commande': 'set_parameters', 'parametres': {'conclusions': True}}, {'commande': 'play_until', 'parametres': {'moment': 'soluble'}}, {'repere': 'l_soluble'}],
              'duree_s': 7}])

# ── Bilan ─────────────────────────────────────────────────────────────────────────────────────────────────────────
diapo(A6, 'sy_b1_bilan', 'Ce qu’il faut retenir', 'La fiche du cours, bloc par bloc.',
      'هادشي اللي خاصك تحفظ. un: une espèce chimique هي ensemble d’entités identiques، naturelle ولا synthétique. '
      'deux: la chimie de synthèse فيها trois types: lourde، des spécialités، و fine. '
      'trois: la synthèse، كنصاوبو espèce من espèces أخرى، les réactifs كيعطيو les produits. '
      'quatre: le chauffage à reflux: الحرارة كتزرب، و le réfrigérant ما كيخلي والو يضيع. '
      'cinq: le traitement: كنبردو، كنخلطو مع l’eau salée، وكنصفيو. '
      'six: les constantes physiques: rho égale m sur V، و d égale rho sur rho de l’eau. '
      'sept: la CCM: pure، tache واحدة؛ نفس الطول، نفس l’espèce؛ و Rf égale h sur H.',
      url='bilan.html?vue=fiche',
      pointage=[('un: une espèce chimique', 'espece'), ('deux: la chimie de synthèse', 'chimie'), ('trois: la synthèse', 'synthese'),
                ('quatre: le chauffage à reflux', 'reflux'), ('cinq: le traitement', 'traitement'), ('six: les constantes', 'constantes'),
                ('sept: la CCM', 'ccm')],
      bullets=['1 · Espèce chimique : entités identiques ; naturelle ou synthétique.', '2 · Chimie de synthèse : lourde, spécialités, fine.',
               '3 · Synthèse : réactifs → produits.', '4 · Chauffage à reflux : plus rapide, sans perte.', '5 · Traitement : refroidir, eau salée, filtrer.',
               '6 · ρ = m/V ; d = ρ/ρ(eau).', '7 · CCM : une tache = pure ; même hauteur = même espèce ; Rf = h/H.'],
      cahier='Formule : ρ = m/V ; d = ρ/ρ(eau) ; Rf = h/H', typ='synthesis', comp=[], conc={'acquis': True})

diapo(A6, 'sy_b2_carte', 'La carte du chapitre', 'Sept branches autour de la synthèse.',
      'وهادي la carte ديال الدرس. فالوسط، la synthèse d’une espèce chimique. الفرع اللول: l’espèce chimique. '
      'من بعد les types de la chimie de synthèse. من بعد la synthèse، réactifs و produits. من بعد le chauffage à reflux. '
      'من بعد le traitement. من بعد les constantes physiques. وفاللخر، la CCM. قيس على فرع باش تقرا الجملة ديالو.',
      url='bilan.html?vue=carte',
      pointage=[('فالوسط', '@centre'), ('الفرع اللول', 'espece'), ('من بعد les types', 'chimie'), ('من بعد la synthèse', 'synthese'),
                ('من بعد le chauffage', 'reflux'), ('من بعد le traitement', 'traitement'), ('من بعد les constantes', 'constantes'),
                ('وفاللخر، la CCM', 'ccm')],
      bullets=['Espèce · Types · Synthèse · Reflux · Traitement · Constantes · CCM'],
      cahier='La carte du chapitre : espèce, types, synthèse, reflux, traitement, constantes, CCM.', typ='synthesis', comp=[], conc={'acquis': True})

diapo(A6, 'sy_fermeture_cours', 'Ce qu’il faut retenir, et comment réviser', 'Trois idées à retenir, et comment réviser.',
      'وصلنا للخر ديال الدرس: synthèse d’une espèce chimique. شنو خاصك تحفظ؟ ثلاثة ديال الأفكار. '
      'اللولة: la synthèse كتصاوب espèce من espèces أخرى، بالتسخين à reflux، اللي كيزرب وما كيضيع والو. '
      'الثانية: كنعرفو le produit بالقياسات: rho égale m sur V، و d égale rho sur rho de l’eau. '
      'الثالثة: فla CCM، نفس الطول، نفس l’espèce، و Rf égale h sur H. '
      'دابا، كيفاش تراجع؟ عاود قرا الدفتر ديالك، وعاود دير الحسابات بوحدك. '
      'ملي تحسب، كتب la relation، من بعد l’application numérique، من بعد le résultat مع l’unité، حيت كل وحدة عندها النقطة ديالها. '
      'ونهار الفرض، قسم الوقت ديالك، وبدا بالسؤال اللي ساهل عليك. وقبل الفرض، ترتاح مزيان فالليل. '
      'كتب هادشي ف الدفتر ديالك. راك خدمتي مزيان، الله يعاونك!',
      centre=[('Retenir : reflux · ρ et d · CCM et Rf', 'ثلاثة ديال الأفكار'), ('Réviser : relire le cahier, refaire les calculs', 'عاود قرا'),
              ('Rédiger : relation → A.N. → résultat et unité', 'ملي تحسب'), ('Jour J : gérer son temps · bien dormir', 'نهار الفرض')],
      cahier='Méthode : 1) relire le cahier ; 2) refaire seul les calculs (ρ, d, Rf) ; 3) écrire la relation, l’application numérique, le résultat avec son unité ; 4) le jour du contrôle, partager son temps ; 5) la veille, bien dormir.',
      typ='synthesis', comp=[], fermeture_cours=True)
