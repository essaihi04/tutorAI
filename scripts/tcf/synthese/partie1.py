# -*- coding: utf-8 -*-
"""Séances 1 et 2 : espèces chimiques, chimie de synthèse, définition ; montage à reflux, reflux, traitement."""
from outils import diapo, question, demonstration

A0, A1, A2 = 'sy_ouverture', 'sy_partie1', 'sy_partie2'

# ── Ouverture ────────────────────────────────────────────────────────────────────────────────────────────────────
diapo(A0, 'sy_ouverture_cours', 'Synthèse d’une espèce chimique', 'Bienvenue : ce qu’on va apprendre, et pourquoi c’est utile.',
      'مرحبا بيك فدرس جديد: synthèse d’une espèce chimique. فهاد الدرس غادي نتعلمو كيفاش كنصاوبو واحد l’espèce chimique فالمختبر، '
      'بالتسخين à reflux، كيفاش كنصاوبو le savon، وكيفاش كنعرفو l’espèce اللي درنا، بالقياسات وب la chromatographie. '
      'هادي هي القاعدة ديال la chimie فالتانوي كامل، وغادي تلقاها فالفروض ديالك. كيفاش غادي نخدمو؟ '
      'تسمع مزيان، تجاوب على الأسئلة فالسبورة، وملي يوقف الدرس، تكتب ف الدفتر ديالك. يلا نبداو!',
      centre=[('On apprend : synthèse, reflux, savon, CCM', 'غادي نتعلمو'),
              ('Pourquoi : la base de la chimie, au contrôle', 'هادي هي القاعدة'),
              ('Écouter · répondre au tableau · écrire dans le cahier', 'كيفاش غادي نخدمو')],
      typ='situation', ouverture_cours=True)

diapo(A0, 'sy_o0_situation', 'Situation problème : fabriquer une espèce', 'Reproduire une espèce de la nature, ou en créer une nouvelle.',
      'شوف هاد الورد ديال الياسمين. فيه واحد الريحة زوينة. فالمختبر، نقدرو نصاوبو نفس الريحة، بلا ما نحتاجو للورد. '
      'هادي سميتها une synthèse: كنعاودو نصاوبو واحد l’espèce اللي كاينة فالطبيعة. '
      'ونقدرو حتى نصاوبو des espèces nouvelles، ماكايناش فالطبيعة، بحال le plastique ولا بزاف ديال les médicaments. '
      'إذن عندنا ثلاثة ديال الأسئلة: شنو هي الأنواع ديال la chimie de synthèse؟ كيفاش كنخدمو فالمختبر؟ '
      'وكيفاش كنعرفو بلي الحاجة اللي درنا هي اللي بغينا؟',
      url='notions.html?vue=situation',
      pointage=[('شوف هاد الورد', 'reproduire'), ('نفس الريحة', '@reproduire'), ('des espèces nouvelles', 'creer'),
                ('le plastique', '@creer'), ('ثلاثة ديال الأسئلة', 'questions')],
      centre=[('reproduire une espèce de la nature', 'كاينة فالطبيعة'), ('créer une espèce nouvelle', 'des espèces nouvelles')],
      cahier='Synthèse : reproduire une espèce de la nature, ou créer une espèce nouvelle.', comp=['C2'])

# ── Bloc 1 : l'espèce chimique (rappel, de zéro) ─────────────────────────────────────────────────────────────────
diapo(A1, 'sy_o1_espece', 'Rappel : une espèce chimique', 'Un ensemble d’entités toutes identiques.',
      'قبل ما نبداو، خاصنا نفهمو شنو هي une espèce chimique. شوف l’eau pure فهاد الكاس. ملي نكبرو بالمكبرة، '
      'كنشوفو غير نوع واحد ديال الجزيئات، كلهم بحال بحال: H deux O. هادي espèce chimique واحدة. '
      'دابا شوف l’eau minérale. فيها الما، وفيها حتى des ions مختلفين، بحال le calcium و le magnésium. '
      'إذن فيها بزاف ديال les espèces، يعني هادا mélange. نعاود نقرا: une espèce chimique، '
      'c’est un ensemble d’entités identiques.',
      url='notions.html?vue=espece',
      pointage=[('شوف l’eau pure', 'pure'), ('بالمكبرة', '@pure'), ('دابا شوف l’eau minérale', 'minerale'),
                ('des ions مختلفين', '@minerale'), ('نعاود نقرا', 'definition')],
      centre=[('eau pure : une seule espèce', 'هادي espèce chimique واحدة'), ('eau minérale : un mélange', 'يعني هادا mélange')],
      cahier='Définition : une espèce chimique est un ensemble d’entités identiques (molécules, ions ou atomes).', comp=['C1'])

diapo(A1, 'sy_o2_naturelle', 'Espèce naturelle, espèce synthétique', 'Elle existe dans la nature, ou elle est préparée par l’Homme.',
      'كاين جوج ديال الأنواع ديال les espèces chimiques. اللول: une espèce naturelle، كاينة فالطبيعة، '
      'بحال الريحة اللي فالورد، ولا le sucre. الثاني: une espèce synthétique، الإنسان هو اللي كيصاوبها فالمختبر ولا فالمعمل، '
      'بحال l’aspirine ولا le plastique. وشوف هاد الجوج ديال القرعات ديال الريحة: وحدة جات من الورد، والأخرى تصاوبات فالمختبر. '
      'ملي تكون نفس l’espèce، كتكون عندها نفس الخصائص، واخا جات من بلاصة أخرى.',
      url='notions.html?vue=naturelle',
      pointage=[('une espèce naturelle', 'naturelle'), ('بحال الريحة اللي فالورد', '@naturelle'), ('une espèce synthétique', 'synthetique'),
                ('l’aspirine', '@synthetique'), ('وشوف هاد الجوج ديال القرعات', 'identiques'), ('نفس الخصائص', '@identiques')],
      centre=[('naturelle : existe dans la nature', 'une espèce naturelle'), ('synthétique : préparée par l’Homme', 'une espèce synthétique')],
      cahier='Une espèce naturelle existe dans la nature ; une espèce synthétique est préparée par l’Homme.', comp=['C1'],
      q=question('qcm', 'L’aspirine, préparée au laboratoire, est une espèce…', ['naturelle', 'synthétique', 'impure'], 1,
                 'شوف هاد السؤال: l’aspirine، اللي كتصاوب فالمختبر، شنو هي؟',
                 [(('l’aspirine ماكتجيش من الطبيعة. شكون اللي كيصاوبها؟', 'L’aspirine ne vient pas de la nature : qui la prépare ?'),
                   ('الجواب: synthétique، حيت الإنسان هو اللي كيصاوبها فالمختبر.', 'Réponse : synthétique, car elle est préparée par l’Homme.')),
                  ('برافو! synthétique، حيت الإنسان هو اللي كيصاوبها.', 'Bonne réponse : préparée par l’Homme, elle est synthétique.'),
                  (('السؤال ماشي واش نقية ولا لا. السؤال: من فين جات؟', 'La question n’est pas la pureté : d’où vient-elle ?'),
                   ('الجواب: synthétique، حيت كتصاوب فالمختبر.', 'Réponse : synthétique, car elle est préparée au laboratoire.'))]))

diapo(A1, 'sy_o3_transformation', 'Rappel : la transformation chimique', 'Des espèces disparaissent, de nouvelles espèces apparaissent.',
      'دابا، شنو هي une transformation chimique؟ شوف هاد le bécher. اللول، عندنا جوج ديال les espèces: الكورات الصفرين والكورات الزرقين. '
      'كنسميوهم les réactifs. دابا كتوقع la transformation: les entités كيتفرقو وكيتجمعو بطريقة أخرى. '
      'وفاللخر، كيبانو كورات جداد، بلون آخر: هادو des espèces nouvelles، كنسميوهم les produits. '
      'إذن فواحد la transformation chimique، les réactifs كيتنقصو، و les produits كيبانو.',
      url='notions.html?vue=transformation',
      pointage=[('شوف هاد le bécher', 'avant'), ('كنسميوهم les réactifs', '@avant'), ('دابا كتوقع la transformation', 'transformation'),
                ('كيبانو كورات جداد', 'apres'), ('كنسميوهم les produits', '@apres'), ('إذن فواحد la transformation chimique', 'bilan')],
      centre=[('réactifs : au départ', 'كنسميوهم les réactifs'), ('produits : à la fin', 'كنسميوهم les produits')],
      cahier='Dans une transformation chimique, les réactifs sont consommés et des produits apparaissent.', comp=['C3'])

# ── Bloc 2 : la synthèse ────────────────────────────────────────────────────────────────────────────────────────
diapo(A1, 'sy_d1_definition', 'Définition de la synthèse', 'Préparer une espèce à partir d’autres espèces, par une transformation chimique.',
      'دابا نقدرو نفهمو la synthèse. عندنا جوج ديال les espèces de départ، A و B: هوما les réactifs. '
      'كنحطوهم فواحد le ballon، وكنديرو une transformation chimique. وفاللخر، كنلقاو واحد l’espèce جديدة، C: هي le produit. '
      'نعاود نقرا: synthétiser une espèce chimique، c’est la préparer à partir d’autres espèces، par une transformation chimique. '
      'وبطريقة أخرى: la synthèse هي واحد الطبخة ديال la chimie: كنبداو بالمكونات، وكنساليو بحاجة جديدة.',
      url='notions.html?vue=definition',
      pointage=[('A و B', 'reactifs'), ('هوما les réactifs', '@reactifs'), ('كنحطوهم فواحد le ballon', 'synthese'),
                ('واحد l’espèce جديدة، C', 'produit'), ('هي le produit', '@produit'), ('نعاود نقرا', 'bilan')],
      centre=[('réactifs → produit', 'هي le produit')],
      cahier='Définition : synthétiser une espèce chimique, c’est la préparer à partir d’autres espèces par une transformation chimique.',
      comp=['C3'])

diapo(A1, 'sy_d2_savon', 'Les réactifs et les produits du savon', 'L’huile et la soude donnent le savon.',
      'ناخدو مثال من الحياة: le savon. باش نصاوبو le savon، كنحتاجو لجوج ديال les réactifs: l’huile، بحال زيت الزيتون، '
      'و la soude، اللي هي une solution d’hydroxyde de sodium. ملي كيتفاعلو، كيتنقصو. '
      'وكيبانو les produits: le savon، ومعاه واحد l’espèce أخرى سميتها le glycérol. '
      'إذن: l’huile و la soude هوما les réactifs، و le savon هو le produit اللي بغينا.',
      url='notions.html?vue=savon',
      pointage=[('كنحتاجو لجوج ديال les réactifs', 'reactifs'), ('و la soude', '@reactifs'), ('وكيبانو les produits', 'produits'),
                ('le glycérol', '@produits'), ('إذن: l’huile و la soude', 'bilan')],
      centre=[('huile + soude → savon + glycérol', 'إذن: l’huile و la soude')],
      cahier='Exemple : huile + soude → savon + glycérol (réactifs → produits).', comp=['C3'],
      q=question('qcm', 'Dans la synthèse du savon, la soude est…', ['un produit', 'un réactif', 'le savon'], 1,
                 'شوف هاد السؤال: ف la synthèse ديال le savon، la soude شنو هي؟',
                 [(('واش la soude كتبان فاللخر، ولا كانت من اللول؟', 'La soude est-elle là au départ ou à la fin ?'),
                   ('الجواب: un réactif، حيت كانت من اللول وكتنقص.', 'Réponse : un réactif, présent au départ et consommé.')),
                  ('برافو! la soude réactif، كانت من اللول وكتتفاعل مع l’huile.', 'Bonne réponse : la soude est un réactif, consommé avec l’huile.'),
                  (('le savon هو اللي كيبان فاللخر. و la soude؟', 'Le savon apparaît à la fin. Et la soude ?'),
                   ('الجواب: un réactif. le savon هو le produit.', 'Réponse : un réactif ; le savon est le produit.'))]))

# ── Bloc 3 : nécessité et types de la chimie de synthèse ────────────────────────────────────────────────────────
diapo(A1, 'sy_n1_pourquoi', 'Pourquoi la chimie de synthèse ?', 'Produire beaucoup, moins cher, et des espèces nouvelles.',
      'علاش كنحتاجو la chimie de synthèse؟ شوف: باش نجبدو شوية ديال الريحة من الورد، خاصنا بزاف بزاف ديال الورد. '
      'هادشي غالي وقليل. ولكن بla synthèse، نقدرو نصاوبو كميات كبيرة، وبثمن رخيص. '
      'وزيد على هادشي، la synthèse كتعطينا des espèces nouvelles، اللي ماكايناش فالطبيعة، بحال les plastiques.',
      url='notions.html?vue=pourquoi',
      pointage=[('بزاف بزاف ديال الورد', 'nature'), ('هادشي غالي وقليل', '@nature'), ('نقدرو نصاوبو كميات كبيرة', 'labo'),
                ('وزيد على هادشي', 'nouvelle'), ('بحال les plastiques', '@nouvelle')],
      centre=[('grandes quantités, moins cher', 'كميات كبيرة'), ('des espèces nouvelles', 'كتعطينا des espèces nouvelles')],
      cahier='La chimie de synthèse produit en grandes quantités et moins cher, et crée des espèces nouvelles.', comp=['C2'])

diapo(A1, 'sy_n2_types', 'Les trois types de la chimie de synthèse', 'Chimie lourde, chimie des spécialités, chimie fine.',
      'la chimie de synthèse فيها ثلاثة ديال الأنواع. اللول: la chimie lourde، فالمعامل الكبار، كتصاوب les produits de base '
      'بكميات كبيرة بزاف، بحال les plastiques. الثاني: la chimie des spécialités، كتصاوب des produits intermédiaires، '
      'بحال les peintures. الثالث: la chimie fine، كتصاوب des produits complexes، بكميات صغيرة، بحال les médicaments.',
      url='notions.html?vue=types',
      pointage=[('اللول: la chimie lourde', 'lourde'), ('بحال les plastiques', '@lourde'), ('الثاني: la chimie des spécialités', 'specialites'),
                ('بحال les peintures', '@specialites'), ('الثالث: la chimie fine', 'fine'), ('بحال les médicaments', '@fine')],
      centre=[('lourde : plastiques', 'اللول: la chimie lourde'), ('spécialités : peintures', 'الثاني: la chimie des spécialités'),
              ('fine : médicaments', 'الثالث: la chimie fine')],
      cahier='| Chimie lourde | Chimie des spécialités | Chimie fine |\n| produits de base, très grandes quantités (plastiques) | produits intermédiaires (peintures) | produits complexes, petites quantités (médicaments) |',
      comp=['C2'])

diapo(A1, 'sy_n3_tri', 'Classer des objets du quotidien', 'De la plus grande quantité à la plus petite.',
      'دابا نعاودو بطريقة أخرى: نرتبو حوايج من الدار. هاد les bouteilles en plastique، كيتصاوبو بالملايين: هادي la chimie lourde. '
      'هاد les pots de peinture، كمية متوسطة: هادي la chimie des spécialités. '
      'وهاد le comprimé، كمية صغيرة، ولكن صعيب بزاف فالتصاوب: هادي la chimie fine. '
      'إذن كلما الكمية صغرات والمنتوج ولا صعيب، كنمشيو من la chimie lourde ل la chimie fine.',
      url='notions.html?vue=tri',
      pointage=[('هاد les bouteilles en plastique', 'bouteille'), ('هاد les pots de peinture', 'peinture'), ('وهاد le comprimé', 'comprime'),
                ('إذن كلما الكمية صغرات', 'quantite')],
      cahier='Remarque : de la chimie lourde à la chimie fine, les quantités diminuent et les produits deviennent plus complexes.', comp=['C2'],
      q=question('qcm', 'Un médicament est fabriqué par…', ['la chimie lourde', 'la chimie des spécialités', 'la chimie fine'], 2,
                 'شوف هاد السؤال: le médicament، شكون اللي كيصاوبو؟',
                 [(('la chimie lourde كتصاوب كميات كبيرة بزاف وبسيطة. le médicament؟', 'La chimie lourde fait de très grandes quantités simples. Et un médicament ?'),
                   ('الجواب: la chimie fine، produit complexe بكمية صغيرة.', 'Réponse : la chimie fine (produit complexe, petite quantité).')),
                  (('la chimie des spécialités كتصاوب بحال les peintures. le médicament كثر تعقيد.', 'Les spécialités font les peintures ; un médicament est plus complexe.'),
                   ('الجواب: la chimie fine.', 'Réponse : la chimie fine.')),
                  ('برافو! le médicament produit complexe بكمية صغيرة: la chimie fine.', 'Bonne réponse : produit complexe en petite quantité : chimie fine.')]))

# ── Bloc 4 : le montage à reflux et le contenu du ballon ───────────────────────────────────────────────────────
diapo(A2, 'sy_m1_montage', 'Le montage du chauffage à reflux', 'On le construit pièce par pièce.',
      'باش نصاوبو le savon فالمختبر، كنبنيو واحد le montage سميتو le chauffage à reflux. نبنيوه قطعة بقطعة. '
      'اللول: la potence، كتشد كلشي. من بعد: le support élévateur، باش نطلعو ولا نهبطو. فوقو: le chauffe-ballon، هو اللي كيسخن. '
      'فيه كنحطو le ballon، فيه le mélange. وفوق le ballon: le réfrigérant à boules. '
      'فيه جوج ديال les tuyaux: l’entrée de l’eau froide، لتحت، و la sortie de l’eau، لفوق. '
      'دابا الما البارد كيدخل من تحت، وكيعمر le réfrigérant، وكيخرج من فوق.',
      url='montage.html?vue=montage',
      pointage=[('اللول: la potence', 'potence'), ('le support élévateur', 'elevateur'), ('le chauffe-ballon', 'chauffe'),
                ('فيه كنحطو le ballon', 'ballon'), ('le réfrigérant à boules', 'refrigerant'), ('l’entrée de l’eau froide', 'entree'),
                ('la sortie de l’eau', 'sortie'), ('دابا الما البارد كيدخل', 'eau')],
      centre=[('eau froide : entrée en bas, sortie en haut', 'دابا الما البارد كيدخل')],
      cahier='Montage du chauffage à reflux : potence, support élévateur, chauffe-ballon, ballon, réfrigérant à boules.',
      figures=[{'type': 'schema', 'titre': 'Le montage à reflux', 'legende': 'L’eau froide entre en bas du réfrigérant et sort en haut.',
                'cadre': {'l': 10, 'h': 8},
                'elements': [
                    {'f': 'rect', 'de': [3, 0.3], 'a': [6, 1.2], 'couleur': 'orange'},
                    {'f': 'cercle', 'c': [4.5, 2.3], 'r': 1, 'couleur': 'cyan'},
                    {'f': 'rect', 'de': [4.2, 3.3], 'a': [4.8, 7.6], 'couleur': 'cyan'},
                    {'f': 'fleche', 'de': [6.6, 3.8], 'a': [4.9, 3.8], 'couleur': 'bleu'},
                    {'f': 'fleche', 'de': [4.9, 7.1], 'a': [6.6, 7.1], 'couleur': 'bleu'},
                    {'f': 'texte', 'at': [6.8, 3.8], 't': 'entrée de l’eau', 'ancre': 'gauche'},
                    {'f': 'texte', 'at': [6.8, 7.1], 't': 'sortie de l’eau', 'ancre': 'gauche'},
                    {'f': 'texte', 'at': [3.9, 5.5], 't': 'réfrigérant', 'ancre': 'droite'},
                    {'f': 'texte', 'at': [3.3, 2.3], 't': 'ballon', 'ancre': 'droite'},
                    {'f': 'texte', 'at': [6.2, 0.75], 't': 'chauffe-ballon', 'ancre': 'gauche'}]}],
      comp=['C4'])

diapo(A2, 'sy_m2_contenu', 'Dans le ballon : les réactifs, et la sécurité', 'Huile, éthanol, soude, pierre ponce.',
      'قبل ما نبداو: la soude corrosive، كتحرق الجلد والعينين. إذن ديما كنلبسو les lunettes و les gants. '
      'دابا نعمرو le ballon. اللول: dix millilitres d’huile d’olive. من بعد: vingt millilitres d’éthanol. '
      'من بعد: vingt millilitres de solution de soude. وفاللخر، شوية ديال الحبات ديال la pierre ponce.',
      url='montage.html?vue=contenu',
      pointage=[('la soude corrosive', 'securite'), ('les lunettes و les gants', '@securite'), ('dix millilitres d’huile d’olive', 'huile'),
                ('vingt millilitres d’éthanol', 'ethanol'), ('vingt millilitres de solution de soude', 'soude'), ('la pierre ponce', 'ponce')],
      centre=[('soude corrosive : lunettes + gants', 'les lunettes و les gants')],
      cahier='Attention : la soude est corrosive : lunettes et gants.\nDans le ballon : huile d’olive, éthanol, solution de soude, pierre ponce.',
      comp=['C4'])

diapo(A2, 'sy_m3_roles', 'Le rôle de l’éthanol et de la pierre ponce', 'Un bon contact, une ébullition régulière.',
      'علاش زدنا l’éthanol؟ شوف: بلا éthanol، l’huile كتبقى فوق و la soude لتحت، جوج ديال les couches. '
      'الكورات ديال l’huile ماكيتلاقاوش مزيان مع ديال la soude. مع l’éthanol، كيولي mélange واحد: '
      'l’éthanol favorise le contact entre les réactifs. و la pierre ponce؟ بلا بيها، ملي يغلي، كتطلع بلبولات كبار وكيتطرطق الخليط. '
      'معاها، البلبولات صغار والغليان هادي: une ébullition régulière.',
      url='montage.html?vue=roles',
      pointage=[('بلا éthanol', 'sans_ethanol'), ('مع l’éthanol', 'avec_ethanol'), ('بلا بيها', 'sans_ponce'), ('معاها، البلبولات صغار', 'avec_ponce')],
      centre=[('éthanol : contact entre les réactifs', 'l’éthanol favorise'), ('pierre ponce : ébullition régulière', 'une ébullition régulière')],
      cahier='L’éthanol favorise le contact entre les réactifs ; la pierre ponce régularise l’ébullition.', comp=['C4'],
      q=question('qcm', 'Pourquoi ajoute-t-on de l’éthanol dans le ballon ?',
                 ['pour refroidir le mélange', 'pour favoriser le contact entre les réactifs', 'pour obtenir une ébullition régulière'], 1,
                 'شوف هاد السؤال: علاش كنزيدو l’éthanol ف le ballon؟',
                 [(('l’éthanol مابردش le mélange. شوف شنو وقع للجوج ديال les couches.', 'L’éthanol ne refroidit pas : regarde les deux couches.'),
                   ('الجواب: باش يسهل le contact entre les réactifs.', 'Réponse : il favorise le contact entre les réactifs.')),
                  ('برافو! l’éthanol كيدير mélange واحد، و les réactifs كيتلاقاو مزيان.', 'Bonne réponse : un seul mélange, les réactifs se rencontrent.'),
                  (('هادا هو الدور ديال la pierre ponce، ماشي l’éthanol.', 'C’est le rôle de la pierre ponce, pas de l’éthanol.'),
                   ('الجواب: le contact entre les réactifs.', 'Réponse : le contact entre les réactifs.'))]))

# ── Bloc 5 : le chauffage et le reflux, expliqués deux fois ───────────────────────────────────────────────────
diapo(A2, 'sy_r1_chauffage', 'Le rôle du chauffage', 'Le chauffage rend la transformation plus rapide.',
      'علاش كنسخنو؟ شوف جوج ديال les ballons، فيهم نفس le mélange. اللول بلا تسخين، فيه vingt degrés. '
      'الثاني مسخن، فيه quatre-vingts degrés: les entités كيتحركو بالزربة، وكيتلاقاو كثر. '
      'دابا نخليو الوقت يدوز: vingt minutes. شوف le savon اللي تصاوب. فle ballon اللول قليل، وفle ballon الثاني بزاف. '
      'إذن الحرارة كتزرب la transformation: le chauffage augmente la vitesse de la réaction.',
      url='reflux.html?vue=chauffage',
      pointage=[('اللول بلا تسخين', 'froid'), ('الثاني مسخن', 'chaud'), ('vingt minutes', 'temps'), ('إذن الحرارة كتزرب', 'compare')],
      centre=[('chauffage : réaction plus rapide', 'le chauffage augmente')],
      cahier='Le chauffage augmente la vitesse de la réaction.', comp=['C5'])

diapo(A2, 'sy_r2_reflux', 'Le reflux : rien ne se perd', 'Les vapeurs se condensent et retombent dans le ballon.',
      'دابا نسخنو le montage كامل. le mélange كيغلي. les vapeurs كيطلعو لفوق، ف le réfrigérant. '
      'شوف شنو كيوقع ليهم فوسط الكورات الباردين. les vapeurs كيتلاقاو مع الحيوط الباردين، وكيرجعو سائل: هادي la condensation. '
      'من بعد، les gouttes كيهبطو وكيرجعو ل le ballon. وهكا كتعاود الدورة: كنسخنو، كيطلعو، كيبردو، كيهبطو. '
      'هادا هو le reflux: ما كيضيع لا réactif لا produit.',
      url='reflux.html?vue=reflux',
      pointage=[('le mélange كيغلي', 'chauffe'), ('les vapeurs كيطلعو لفوق', 'vapeurs'), ('شوف شنو كيوقع ليهم', '@refrigerant'),
                ('هادي la condensation', '@condensation'), ('les gouttes كيهبطو', '@gouttes'), ('هادا هو le reflux', 'cycle')],
      centre=[('vapeurs → condensation → gouttes', 'هادي la condensation'), ('reflux : pas de perte', 'هادا هو le reflux')],
      cahier='Le reflux : les vapeurs se condensent dans le réfrigérant et retombent dans le ballon : pas de perte de réactifs ni de produits.',
      obs={'apres_mot': 'شوف شنو كيوقع ليهم فوسط الكورات الباردين.', 'sim_avant': {'conclusions': False}, 'sim_apres': {'conclusions': True},
           'gestes': [{'commande': 'play_until', 'parametres': {'moment': 'gouttes'}}, {'repere': 'refrigerant'}],
           'enonce': 'Dans le réfrigérant froid, que deviennent les vapeurs ?',
           'enonce_dit': 'شوف le réfrigérant. les vapeurs، شنو كيوليو ملي كيوصلو ليه؟', 'silence_s': 8,
           'indices': [{'texte': 'Le réfrigérant est froid : l’eau froide y circule.', 'dit': 'تفكر: le réfrigérant بارد، الما البارد كيدور فيه.', 'repere': 'refrigerant'},
                       {'texte': 'Regarde ce qui descend vers le ballon.', 'dit': 'شوف شنو كيهبط ل le ballon.', 'repere': 'gouttes'}],
           'choix': ['Elles s’échappent dans l’air', 'Elles redeviennent liquides et retombent', 'Elles restent dans le réfrigérant'], 'bonne': 1,
           'retours': [{'parole': 'لا، le réfrigérant بارد، les vapeurs مايخرجوش. شوف شنو كيهبط.', 'ecrit': 'Non : le réfrigérant froid les arrête ; regarde ce qui descend.'},
                       {'parole': 'برافو! كيبردو، كيرجعو سائل، وكيهبطو ل le ballon.', 'ecrit': 'Oui : elles se condensent et retombent dans le ballon.'},
                       {'parole': 'لا، ماكيبقاوش تما. شوف les gouttes كيهبطو.', 'ecrit': 'Non : elles ne restent pas ; regarde les gouttes qui descendent.'}],
           'solution': {'parole': 'les vapeurs كيبردو، كيرجعو سائل، وكيهبطو ل le ballon: هادا هو le reflux.', 'ecrit': 'Les vapeurs se condensent et retombent dans le ballon : c’est le reflux.'}},
      comp=['C5'])

diapo(A2, 'sy_r3_bilan', 'Chauffage à reflux : deux rôles', 'Plus rapide grâce au chauffage, sans perte grâce au réfrigérant.',
      'نعاودو بطريقة أخرى، بثلاثة ديال les montages. اللول: à froid، بلا تسخين: la réaction بطيئة بزاف. '
      'الثاني: كنسخنو بلا réfrigérant. la réaction كتزرب، ولكن شوف: les vapeurs كيخرجو فالهوا، وكنضيعو la matière. '
      'الثالث: le chauffage à reflux. الحرارة كتزرب la réaction، و le réfrigérant كيرجع les vapeurs. '
      'إذن عندنا جوج ديال الأدوار: le chauffage، réaction plus rapide. و le reflux، pas de perte de matière.',
      url='reflux.html?vue=bilan',
      pointage=[('اللول: à froid', 'froid'), ('الثاني: كنسخنو بلا réfrigérant', 'ouvert'), ('les vapeurs كيخرجو فالهوا', 'perte'),
                ('الثالث: le chauffage à reflux', 'reflux'), ('إذن عندنا جوج ديال الأدوار', 'bilan')],
      centre=[('chauffage : plus rapide', 'le chauffage، réaction plus rapide'), ('réfrigérant : sans perte', 'pas de perte de matière')],
      cahier='Donc le chauffage à reflux : réaction plus rapide (chauffage) et sans perte de matière (réfrigérant).', comp=['C5'],
      q=question('qcm', 'Quel est le rôle du réfrigérant à boules ?',
                 ['chauffer le mélange', 'condenser les vapeurs pour éviter les pertes', 'agiter le mélange'], 1,
                 'شوف هاد السؤال: شنو هو الدور ديال le réfrigérant à boules؟',
                 [(('اللي كيسخن هو le chauffe-ballon. le réfrigérant فيه الما البارد.', 'C’est le chauffe-ballon qui chauffe ; le réfrigérant contient de l’eau froide.'),
                   ('الجواب: كيبرد les vapeurs، كيرجعهم سائل، باش مانضيعوش la matière.', 'Réponse : il condense les vapeurs : pas de perte de matière.')),
                  ('برافو! le réfrigérant كيرجع les vapeurs سائل، وما كيضيع والو.', 'Bonne réponse : il condense les vapeurs, rien ne se perd.'),
                  (('le réfrigérant ماكيحركش. شوف شنو كيوقع ل les vapeurs فيه.', 'Le réfrigérant n’agite pas : regarde ce que deviennent les vapeurs.'),
                   ('الجواب: كيبرد les vapeurs، باش مانضيعوش la matière.', 'Réponse : il condense les vapeurs, sans perte de matière.'))]))

# ── Bloc 6 : le traitement ──────────────────────────────────────────────────────────────────────────────────────
diapo(A2, 'sy_t1_refroidir', 'Refroidir, puis verser dans l’eau salée', 'Le savon précipite : il devient solide.',
      'من بعد vingt minutes، كنطفيو le chauffe-ballon، وكنخليو le mélange يبرد. '
      'من بعد كنوجدو de l’eau salée concentrée، يعني الما فيه بزاف ديال le sel ذايب. '
      'دابا نزيدو le mélange فيه. شوف: كيبانو حبيبات بيضين. le savon ماكيذوبش مزيان فl’eau salée، إذن كيولي صلب: le savon précipite.',
      url='traitement.html?vue=refroidir',
      pointage=[('كنطفيو le chauffe-ballon', 'arret'), ('de l’eau salée concentrée', 'salee'), ('دابا نزيدو le mélange', 'verser'),
                ('le savon précipite', 'precipite')],
      centre=[('eau salée : le savon précipite', 'le savon précipite')],
      cahier='Traitement : 1) arrêter le chauffage et laisser refroidir ; 2) verser dans l’eau salée concentrée : le savon précipite.',
      comp=['C6'])

diapo(A2, 'sy_t2_filtrer', 'Filtrer : on obtient le savon', 'Le liquide passe, le savon reste sur le filtre.',
      'دابا كنصفيو. كنحطو le papier filtre فواحد l’entonnoir، ونزيدو le mélange. الما كيدوز، و le savon كيبقى فوق le papier filtre. '
      'هادا هو le savon اللي درنا: un solide. ولكن رد البال: فيه شوية ديال la soude باقية، '
      'إذن ماتقيسوش باليد، وخليو les gants و les lunettes.',
      url='traitement.html?vue=filtrer',
      pointage=[('دابا كنصفيو', 'filtrer'), ('هادا هو le savon اللي درنا', 'savon'), ('ولكن رد البال', 'attention')],
      centre=[('filtration : le savon reste sur le filtre', 'كيبقى فوق le papier filtre')],
      cahier='3) filtrer : le savon solide reste sur le papier filtre.\nAttention : le savon obtenu contient encore de la soude : ne pas le toucher sans gants.',
      comp=['C6'])

diapo(A2, 'sy_t3_etapes', 'Les étapes de la synthèse du savon', 'Chauffage à reflux, refroidissement et eau salée, filtration.',
      'نجمعو كلشي. الخطوة اللولة: le chauffage à reflux، vingt minutes. الخطوة الثانية: كنبردو، ونخلطو مع l’eau salée، و le savon كيترسب. '
      'الخطوة الثالثة: كنصفيو. وفاللخر، عندنا le savon، l’espèce synthétisée.',
      url='traitement.html?vue=etapes',
      pointage=[('الخطوة اللولة', 'e1'), ('الخطوة الثانية', 'e2'), ('الخطوة الثالثة', 'e3'), ('وفاللخر، عندنا le savon', 'savon')],
      cahier='Méthode : 1) chauffage à reflux ; 2) refroidir, verser dans l’eau salée ; 3) filtrer.', comp=['C6'],
      q=question('qcm', 'Pourquoi verse-t-on le mélange dans l’eau salée concentrée ?',
                 ['pour faire précipiter le savon', 'pour chauffer le mélange', 'pour dissoudre le savon'], 0,
                 'شوف هاد السؤال: علاش نزيدو le mélange فl’eau salée concentrée؟',
                 [('برافو! فl’eau salée، le savon ماكيذوبش، كيولي صلب وكيترسب.', 'Bonne réponse : le savon précipite dans l’eau salée.'),
                  (('l’eau salée باردة، ماكتسخنش. شوف شنو كيبان فيه.', 'L’eau salée ne chauffe pas : regarde ce qui apparaît.'),
                   ('الجواب: باش le savon يترسب ويولي صلب.', 'Réponse : pour faire précipiter le savon.')),
                  (('بالعكس: شوف الحبيبات البيضين اللي كيبانو.', 'Au contraire : regarde les flocons blancs qui apparaissent.'),
                   ('الجواب: باش le savon يترسب، ماشي باش يذوب.', 'Réponse : pour faire précipiter le savon, pas le dissoudre.'))]))
