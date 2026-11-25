# -*- coding: utf-8 -*-
"""Construit le cours /TCF « Modèle de l'atome » (tc_chim_atome) : frontend/src/publication/tcf/cours/tc_chim_atome.json
(25 novembre 2026, session cloud). Le cours est écrit ici, diapo par diapo, puis vérifié (chaque `mot` du pointage et du
centre est un extrait exact du texte parlé, dans l'ordre ; aucun chiffre ni symbole dans ce que la voix dit).
Le contenu suit docs/tcf/CONTENU_LIVRE.md (section « Modèle de l'atome ») ; les simulations sont dans
frontend/public/media/simulations/chimie/tc_atome-tableau/.

Usage : python -X utf8 scripts/tcf/construire_tc_chim_atome.py   (puis scripts/tcf/lister_voix_tcf.py sur le cours)
"""
import json, os, re, sys

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SORTIE = os.path.join(RACINE, 'frontend/src/publication/tcf/cours/tc_chim_atome.json')
SIM = '/media/simulations/chimie/tc_atome-tableau/'
PARLE = []   # (lieu, texte) : tout ce que la voix dira, contrôlé à la fin


def pu(mot, moment):
    return {'mot': mot, 'commande': 'play_until', 'parametres': {'moment': moment}}


def rp(mot, repere):
    return {'mot': mot, 'repere': repere}


def ce(mot, texte):
    return {'texte': texte, 'mot': mot}


def reac(juste=None, faux=None):
    """juste : (parole, ecrit) ; faux : {option: ((p1, e1), (p2, e2))}."""
    out = {}
    if juste:
        i, (p, e) = juste
        out[str(i)] = {'juste': {'parole': p, 'ecrit': e}}
    for i, ((p1, e1), (p2, e2)) in (faux or {}).items():
        out[str(i)] = {'1': {'parole': p1, 'ecrit': e1}, '2': {'parole': p2, 'ecrit': e2}}
    return out


def question(typ, prompt, options, correct, dit, juste, faux, demo=None, timeout=40):
    q = {'type': typ, 'prompt': prompt, 'options': options, 'correct': correct, 'timeout_seconds': timeout, 'enonce_dit': dit}
    if demo:
        q['demonstration'] = {'parole': demo[0], 'lignes': [{'texte': t, 'mot': m, **({'allume': a} if a else {})} for t, m, a in demo[1]]}
    return q, {'q': reac((correct, juste), faux)}


def diapo(id, titre, lead, bullets, trace, url, caption, alt, fr, mx, pointage=(), centre=(), cahier='', comps=(),
          q=None, demarrer=None, observation=None, apres=None, figures=None, typ='simulation', extra=None):
    s = {'id': id, 'slide_type': typ, 'title': titre,
         'screen_content': {'lead': lead, 'bullets': list(bullets), 'student_trace': trace},
         'visual': {'kind': 'simulation', 'url': SIM + url, 'caption': caption, 'alt': alt} if url else {'kind': 'none'},
         'speech_text': {'fr': fr, 'mixed': mx}}
    c = {}
    if demarrer:
        c['demarrer'] = demarrer
    if pointage:
        c['pointage'] = list(pointage)
    if centre:
        c['centre'] = list(centre)
    if observation:
        c['observation'] = observation
    if apres:
        c['apres_reponse'] = apres
    if cahier:
        c['cahier'] = cahier
    if figures:
        c['cahier_figures'] = figures
    c['reponses'] = {}
    if q:
        s['question'], c['reponses'] = q
    s['concentration'] = c
    s['competence_ids'] = list(comps)
    if extra:
        s.update(extra)
    return s


def obs(apres_mot, enonce, dit, indices, choix, bonne, retours, solution, gestes=(), sim_avant=None, sim_apres=None):
    o = {'apres_mot': apres_mot}
    if sim_avant is not None:
        o['sim_avant'] = sim_avant
    if sim_apres is not None:
        o['sim_apres'] = sim_apres
    if gestes:
        o['gestes'] = list(gestes)
    o.update({'enonce': enonce, 'enonce_dit': dit, 'silence_s': 8,
              'indices': [{'texte': t, 'dit': d, **({'repere': r} if r else {})} for t, d, r in indices],
              'choix': choix, 'bonne': bonne,
              'retours': [{'parole': p, 'ecrit': e} for p, e in retours],
              'solution': {'parole': solution[0], 'ecrit': solution[1]}})
    return o


D = {}   # les diapos, par id

# ═════════════════════════════════ SÉANCE 1 — le point de départ ═════════════════════════════════

D['at_ouverture_cours'] = diapo(
    'at_ouverture_cours', 'Modèle de l’atome', 'Bienvenue : ce qu’on va apprendre, et pourquoi c’est utile.',
    ['On apprend : l’atome, son noyau, ses électrons', 'Pourquoi : la base de toute la chimie',
     'Écouter · répondre au tableau · écrire dans le cahier'],
    'Modèle de l’atome — on apprend : l’atome, son noyau, ses électrons.', None, '', '',
    'Bienvenue dans un nouveau cours : Modèle de l’atome. Dans ce cours, nous allons voir comment les savants ont '
    'découvert l’atome, de quoi il est fait, comment on écrit son noyau, quelle est sa masse et sa taille, ce que sont '
    'les ions et l’élément chimique, et comment ses électrons se rangent en couches. C’est la base de toute la chimie '
    'que tu feras jusqu’au bac. Comment allons-nous travailler ? Tu écoutes bien, tu réponds aux questions au tableau, '
    'et quand le cours s’arrête, tu écris dans ton cahier. Allons-y !',
    'مرحبا بيك فدرس جديد: Modèle de l’atome. فهاد الدرس غادي نتعلمو كيفاش العلماء اكتشفو l’atome، شنو فيه، كيفاش '
    'نكتبو le noyau ديالو، شحال la masse ديالو و شحال كبير، شنو هما les ions و l’élément chimique، وكيفاش les '
    'électrons ديالو كيترتبو ف les couches. هادي هي الأساس ديال كاع la chimie اللي غادي تقرا حتى للباك. كيفاش غادي '
    'نخدمو؟ تسمع مزيان، تجاوب على الأسئلة فالسبورة، وملي يوقف الدرس، تكتب ف الدفتر ديالك. يلا نبداو!',
    centre=[ce('غادي نتعلمو', 'On apprend : l’atome, son noyau, ses électrons'),
            ce('هادي هي الأساس', 'Pourquoi : la base de toute la chimie'),
            ce('كيفاش غادي نخدمو', 'Écouter · répondre au tableau · écrire dans le cahier')],
    typ='situation', extra={'ouverture_cours': True})

D['at_o1_situation'] = diapo(
    'at_o1_situation', 'Toute la matière est faite d’atomes', 'Qu’est-ce qu’un atome ? De quoi est-il fait ?',
    ['Une pièce de cuivre grossie, puis grossie encore : des petites boules serrées, les atomes.'],
    'Toute la matière est faite d’atomes liés les uns aux autres.', 'prerequis.html?vue=zoom',
    'La pièce de cuivre grossie jusqu’aux atomes', 'Une pièce de cuivre ; la loupe la grossit ; encore : des atomes serrés',
    'Regarde cette pièce de cuivre. Avec une loupe, on la grossit : on voit des grains. On grossit encore, beaucoup plus : '
    'on voit des petites boules serrées les unes contre les autres. Ce sont les atomes. Toute la matière, le cuivre, '
    'l’eau, l’air et ton corps, est faite d’atomes liés les uns aux autres. Alors voici la question de ce cours : '
    'qu’est-ce qu’un atome, et de quoi est-il fait ?',
    'شوف هاد la pièce ديال le cuivre. بواحد la loupe، كنكبروها: كنشوفو des grains. كنكبرو كثر، بزاف: كنشوفو '
    'كويرات صغار لاصقين فبعضياتهم. هادو هما les atomes. كاع la matière، le cuivre، الما، الهوا، وحتى الجسم ديالك، '
    'مصنوعة من les atomes مربوطين مع بعضياتهم. إذن هادا هو السؤال ديال هاد الدرس: شنو هو l’atome، وشنو فيه؟',
    pointage=[rp('هاد la pièce', 'piece'), pu('بواحد la loupe', 'loupe'), pu('كنكبرو كثر', 'atomes'),
              rp('هادو هما les atomes', 'atomes'), pu('هادا هو السؤال', 'questions')],
    centre=[ce('هادو هما les atomes', 'la matière = des atomes')],
    cahier='Toute la matière est faite d’atomes liés les uns aux autres.', comps=['C1'])

D['at_p1_modele'] = diapo(
    'at_p1_modele', 'Qu’est-ce qu’un modèle ?', 'On ne voit pas l’atome : on en fait un modèle.',
    ['Le globe est un modèle de la Terre : plus petit, plus simple.', 'L’atome est trop petit pour être vu : on imagine un modèle, qu’on change quand une expérience ne colle plus.'],
    'Un modèle est une représentation simplifiée d’une chose réelle ; il change avec les expériences.', 'prerequis.html?vue=modele',
    'La Terre et le globe ; l’atome invisible', 'La Terre peinte, puis le globe, son modèle ; l’atome, un nuage avec un point d’interrogation',
    'Avant de parler de l’atome, une idée importante : le modèle. Voici la Terre, la vraie. Et voici un globe : c’est un '
    'modèle de la Terre, plus petit et plus simple, mais il nous aide à la comprendre. L’atome est trop petit pour être '
    'vu, même avec le meilleur microscope de l’école. Alors les savants imaginent un modèle de l’atome. Quand une nouvelle '
    'expérience ne colle plus avec le modèle, on change le modèle. C’est exactement l’histoire de l’atome.',
    'قبل ما نهضرو على l’atome، واحد الفكرة مهمة: le modèle. هادي هي la Terre، الحقيقية. وهادا le globe: هو modèle '
    'ديال la Terre، صغير وساهل، ولكن كيعاونا نفهموها. l’atome صغير بزاف، ما كيتشافش، حتى بأحسن microscope ديال '
    'المدرسة. إذن العلماء كيتخيلو واحد le modèle ديال l’atome. ملي كتجي واحد التجربة جديدة وما كتوافقش مع le '
    'modèle، كنبدلو le modèle. هادي هي بالضبط القصة ديال l’atome.',
    pointage=[pu('هادي هي la Terre', 'terre'), pu('وهادا le globe', 'globe'), rp('وهادا le globe', 'globe'),
              pu('l’atome صغير بزاف', 'atome'), pu('كنبدلو le modèle', 'change')],
    centre=[ce('هو modèle', 'modèle = représentation simplifiée'), ce('كنبدلو le modèle', 'nouvelle expérience → nouveau modèle')],
    cahier='Définition : un modèle est une représentation simplifiée de la réalité ; il change avec les expériences.',
    comps=['C1'],
    q=question('qcm', 'Pourquoi les savants ont-ils changé plusieurs fois le modèle de l’atome ?',
               ['Parce que l’atome a changé de forme', 'Parce qu’une nouvelle expérience ne collait plus avec l’ancien modèle', 'Parce qu’on a enfin vu l’atome à l’œil nu'],
               1, 'شوف هاد السؤال: علاش العلماء بدلو le modèle ديال l’atome بزاف ديال المرات؟',
               ('برافو! ملي كتجي تجربة جديدة وما كتوافقش مع le modèle، كنبدلوه.', 'Oui : une nouvelle expérience qui ne colle plus oblige à changer le modèle.'),
               {0: (('لا، l’atome ما تبدلش. اللي تبدل هو الفكرة ديالنا عليه. فكر فالتجارب.', 'Non : l’atome n’a pas changé, c’est notre idée de lui qui change. Pense aux expériences.'),
                    ('الجواب: تجربة جديدة ما كتوافقش مع le modèle القديم، إذن كنبدلو le modèle.', 'Réponse : une nouvelle expérience ne collait plus, on a changé le modèle.')),
                2: (('لا، l’atome صغير بزاف، ما كيتشافش بالعين. شنو اللي كيخلينا نبدلو le modèle؟', 'Non : l’atome est bien trop petit pour être vu. Qu’est-ce qui fait changer un modèle ?'),
                    ('الجواب: تجربة جديدة. l’atome ما كيتشافش، والتجارب هي اللي كتبدل le modèle.', 'Réponse : une nouvelle expérience ; l’atome ne se voit pas, ce sont les expériences qui changent le modèle.'))}))

D['at_p2_charges'] = diapo(
    'at_p2_charges', 'Rappel : la charge électrique', 'Deux sortes de charges : positive (+) et négative (−).',
    ['Deux charges de même signe se repoussent.', 'Deux charges de signes contraires s’attirent.'],
    'Même signe : répulsion ; signes contraires : attraction.', 'prerequis.html?vue=charges',
    'Attraction et répulsion de charges', 'Deux + s’écartent, deux − s’écartent, une + et une − se rapprochent',
    'Pour comprendre l’atome, il faut d’abord connaître la charge électrique. Il y a deux sortes de charges : la charge '
    'positive, notée plus, et la charge négative, notée moins. Regarde : deux charges positives s’écartent, elles se '
    'repoussent. Deux charges négatives aussi se repoussent. Mais une charge positive et une charge négative se '
    'rapprochent : elles s’attirent. Retiens la règle : même signe, elles se repoussent ; signes contraires, elles '
    's’attirent.',
    'باش نفهمو l’atome، خاصنا اللول نعرفو la charge électrique. كاينين جوج أنواع: la charge positive، كنكتبوها '
    'plus، و la charge négative، كنكتبوها moins. شوف: deux charges positives كيتباعدو، يعني se repoussent. deux '
    'charges négatives حتى هوما se repoussent. ولكن واحد positive وواحد négative كيتقربو: s’attirent. حفظ la règle: '
    'même signe، se repoussent؛ signes contraires، s’attirent.',
    pointage=[pu('deux charges positives', 'plus_plus'), pu('deux charges négatives', 'moins_moins'),
              pu('ولكن واحد positive', 'plus_moins'), pu('حفظ la règle', 'regle'), rp('حفظ la règle', 'regle')],
    centre=[ce('حفظ la règle', '+ et + : répulsion · + et − : attraction')],
    cahier='Rappel : deux charges de même signe se repoussent ; deux charges de signes contraires s’attirent.',
    comps=['C0'])

D['at_p3_ballon'] = diapo(
    'at_p3_ballon', 'Neutre ou chargé ?', 'Un corps neutre a autant de charges + que de charges −.',
    ['On frotte un ballon sur les cheveux : des électrons passent des cheveux au ballon.', 'Le ballon gagne des charges − : il devient négatif ; les cheveux deviennent positifs.'],
    'Neutre : autant de charges + que de charges −. Gagner des électrons rend négatif ; en perdre rend positif.', 'prerequis.html?vue=ballon',
    'Le ballon frotté sur les cheveux', 'Quatre + et quatre − sur chacun ; deux électrons passent au ballon ; les cheveux se dressent',
    'Deuxième façon de voir la charge. Un ballon et des cheveux : chacun a quatre charges plus et quatre charges moins. '
    'Autant de plus que de moins : ils sont neutres. Maintenant on frotte le ballon sur les cheveux. Deux petites '
    'charges négatives passent des cheveux au ballon : ce sont des électrons. Le ballon a maintenant quatre plus et six '
    'moins : il est chargé négativement. Les cheveux ont quatre plus et deux moins : ils sont chargés positivement. '
    'Et voilà : plus et moins, ils s’attirent, les cheveux se dressent vers le ballon.',
    'طريقة ثانية باش نشوفو la charge. واحد le ballon والشعر: كل واحد فيه quatre charges plus و quatre charges moins. '
    'نفس العدد ديال plus و moins: إذن neutres. دابا كنحكو le ballon مع الشعر. deux charges négatives صغار كيدوزو '
    'من الشعر ل le ballon: هادو هما les électrons. دابا le ballon فيه quatre plus و six moins: chargé négativement. '
    'والشعر فيه quatre plus و deux moins: chargé positivement. وها هو: plus و moins، s’attirent، والشعر كينوض '
    'نيشان ل le ballon.',
    pointage=[rp('واحد le ballon', 'ballon'), pu('إذن neutres', 'neutres'), pu('دابا كنحكو', 'frotter'),
              pu('دابا le ballon فيه', 'charges'), rp('دابا le ballon فيه', 'ballon'), rp('والشعر فيه', 'cheveux'),
              pu('وها هو', 'attire')],
    centre=[ce('إذن neutres', 'neutre : autant de + que de −'), ce('chargé négativement', 'gagne des électrons → chargé −')],
    cahier='Un corps neutre a autant de charges + que de charges − ; s’il gagne des électrons, il devient négatif ; s’il en perd, positif.',
    comps=['C0'],
    q=question('qcm', 'Un corps a 5 charges + et 7 charges −. Il est…',
               ['neutre', 'chargé positivement', 'chargé négativement'], 2,
               'شوف هاد السؤال: واحد الجسم فيه cinq charges plus و sept charges moins. واش neutre، chargé positivement، ولا chargé négativement؟',
               ('برافو! sept moins كثر من cinq plus: الجسم chargé négativement.', 'Oui : 7 charges − et seulement 5 charges + : il est chargé négativement.'),
               {0: (('لا، neutre يعني نفس العدد ديال plus و moins. قارن cinq مع sept.', 'Non : neutre veut dire autant de + que de −. Compare 5 et 7.'),
                    ('sept moins كثر من cinq plus، إذن chargé négativement، ماشي neutre.', 'Il y a plus de charges − (7) que de + (5) : chargé négativement.')),
                1: (('لا. شوف شكون كثر: les charges plus ولا les charges moins؟', 'Non. Regarde lesquelles sont les plus nombreuses : les + ou les − ?'),
                    ('les charges moins هما الكثار، sept، إذن chargé négativement.', 'Les charges − sont plus nombreuses (7 contre 5) : chargé négativement.'))}))

D['at_p4_puissances'] = diapo(
    'at_p4_puissances', 'Rappel : les puissances de dix', 'Pour écrire des nombres très petits : 10⁻¹, 10⁻², … 10⁻¹⁰.',
    ['1 m ÷ 10 = 0,1 m = 10⁻¹ m ; 0,01 m = 10⁻² m (1 cm) ; 0,001 m = 10⁻³ m (1 mm).', '0,0000000001 m : le 1 est à la 10ᵉ place après la virgule → 10⁻¹⁰ m.'],
    '10⁻ⁿ : le 1 est à la n-ième place après la virgule ; 10⁻³ m = 1 mm.', 'prerequis.html?vue=puissances',
    'Diviser par dix, encore et encore', 'Une règle de 1 m divisée par 10 ; les dix places après la virgule s’allument',
    'L’atome est très petit : il faut savoir écrire des nombres très petits. Voici un mètre. On le divise par dix : zéro '
    'virgule un mètre, c’est dix puissance moins un mètre. On divise encore par dix : zéro virgule zéro un, dix puissance '
    'moins deux, c’est un centimètre. Encore : dix puissance moins trois, c’est un millimètre. Et pour dix puissance moins '
    'dix ? Comptons les places après la virgule : un, deux, trois, jusqu’à dix. Le un est à la dixième place : dix '
    'puissance moins dix mètre. C’est la taille d’un atome. Et le noyau, nous le verrons, c’est dix puissance moins quinze.',
    'l’atome صغير بزاف: خاصنا نعرفو نكتبو des nombres صغار بزاف. هادا un mètre. كنقسموه على dix: zéro virgule un '
    'mètre، يعني dix puissance moins un mètre. كنقسمو مرة أخرى على dix: zéro virgule zéro un، dix puissance moins deux، '
    'يعني un centimètre. مرة أخرى: dix puissance moins trois، يعني un millimètre. و dix puissance moins dix؟ نحسبو '
    'les places من بعد la virgule: un، deux، trois، حتى dix. le un كاين فla place dix: dix puissance moins dix mètre. '
    'هادي هي la taille ديال l’atome. و le noyau، غادي نشوفوه، هو dix puissance moins quinze.',
    pointage=[pu('هادا un mètre', 'metre'), pu('كنقسموه على dix', 'dixieme'), pu('كنقسمو مرة أخرى', 'centieme'),
              pu('مرة أخرى: dix puissance moins trois', 'millieme'), pu('نحسبو', 'places'), rp('le un كاين', 'places'),
              pu('هادي هي la taille', 'atome'), pu('و le noyau', 'noyau')],
    centre=[ce('يعني un centimètre', '10⁻² m = 1 cm'), ce('dix puissance moins dix mètre', '10⁻¹⁰ m : 10ᵉ place')],
    cahier='Rappel : 10⁻¹ m = 0,1 m ; 10⁻² m = 1 cm ; 10⁻³ m = 1 mm ; 10⁻ⁿ : le 1 est à la n-ième place après la virgule.',
    comps=['C0'])

D['at_p5_calculs'] = diapo(
    'at_p5_calculs', 'Calculer avec les puissances de dix', 'Multiplier : on ajoute les exposants ; diviser : on les retranche.',
    ['10² × 10³ = 10⁵ (cinq zéros).', '10ᵃ × 10ᵇ = 10ᵃ⁺ᵇ ; 10ᵃ/10ᵇ = 10ᵃ⁻ᵇ.', '20 × 10⁻²⁷ = 2 × 10⁻²⁶ : un seul chiffre avant la virgule.'],
    '10ᵃ × 10ᵇ = 10ᵃ⁺ᵇ ; 10ᵃ/10ᵇ = 10ᵃ⁻ᵇ ; écriture scientifique : un seul chiffre (non nul) avant la virgule.', 'prerequis.html?vue=calculs',
    'Les règles de calcul', 'Les zéros de 100 × 1 000 comptés ; les règles ; 10⁻¹⁰/10⁻¹⁵ ; 20 × 10⁻²⁷',
    'Deux règles suffisent. Première : dix puissance deux fois dix puissance trois, c’est cent fois mille, cent mille. '
    'Comptons les zéros : un, deux, trois, quatre, cinq. Donc dix puissance cinq. On ajoute les exposants : deux plus '
    'trois, cinq. Deuxième règle, pour diviser, on retranche les exposants : dix puissance moins dix sur dix puissance '
    'moins quinze, égale dix puissance cinq. Et une dernière chose : vingt fois dix puissance moins vingt-sept, on l’écrit '
    'deux fois dix puissance moins vingt-six. On garde un seul chiffre avant la virgule.',
    'جوج ديال les règles كافيين. اللولة: dix puissance deux fois dix puissance trois، يعني cent fois mille، cent mille. '
    'نحسبو les zéros: un، deux، trois، quatre، cinq. إذن dix puissance cinq. كنزيدو les exposants: deux plus trois، '
    'cinq. la règle الثانية، باش نقسمو، كننقصو les exposants: dix puissance moins dix sur dix puissance moins quinze، '
    'égale dix puissance cinq. وحاجة أخيرة: vingt fois dix puissance moins vingt-sept، كنكتبوها deux fois dix '
    'puissance moins vingt-six. كنخليو chiffre واحد قبل la virgule.',
    pointage=[pu('نحسبو les zéros', 'produit'), pu('كنزيدو les exposants', 'regle_produit'),
              pu('la règle الثانية', 'quotient'), pu('وحاجة أخيرة', 'ecriture')],
    centre=[ce('كنزيدو les exposants', '10ᵃ × 10ᵇ = 10ᵃ⁺ᵇ'), ce('كننقصو les exposants', '10ᵃ/10ᵇ = 10ᵃ⁻ᵇ')],
    cahier='Formule : 10ᵃ × 10ᵇ = 10ᵃ⁺ᵇ ; 10ᵃ/10ᵇ = 10ᵃ⁻ᵇ',
    comps=['C0'],
    q=question('qcm', 'Combien vaut 10⁻⁸/10⁻¹⁰ ?', ['10²', '10⁻¹⁸', '10⁻²'], 0,
               'شوف هاد السؤال: شحال كيساوي dix puissance moins huit sur dix puissance moins dix؟',
               ('برافو! كننقصو les exposants: moins huit moins moins dix، يعني deux. dix puissance deux.', 'Oui : 10⁻⁸/10⁻¹⁰ = 10⁻⁸⁺¹⁰ = 10².'),
               {1: (('هادي جمعتي les exposants. ملي كنقسمو، كننقصو les exposants.', 'Tu as additionné les exposants ; pour une division, on les retranche.'),
                    ('moins huit moins moins dix كيساوي plus deux: الجواب dix puissance deux.', '−8 − (−10) = +2 : la réponse est 10².')),
                2: (('رد البال للإشارة: moins moins dix كتولي plus dix.', 'Attention au signe : retrancher −10, c’est ajouter 10.'),
                    ('moins huit plus dix كيساوي plus deux، ماشي moins deux: dix puissance deux.', '−8 + 10 = +2, pas −2 : 10².'))},
               demo=('la règle: dix puissance a sur dix puissance b égale dix puissance a moins b. هنا a égale moins huit و b égale moins dix. '
                     'a moins b égale moins huit plus dix، يعني deux. le résultat: dix puissance deux.',
                     [('10ᵃ/10ᵇ = 10ᵃ⁻ᵇ', 'la règle', None), ('a = −8 ; b = −10', 'هنا a égale', None),
                      ('a − b = −8 + 10 = 2', 'a moins b', None), ('10⁻⁸/10⁻¹⁰ = 10²', 'le résultat', None)])))

# ═════════════════════════════════ SÉANCE 2 — l'histoire du modèle ═════════════════════════════════

D['at_h1_elements'] = diapo(
    'at_h1_elements', 'Antiquité : les quatre éléments', 'Les Grecs : toute la matière vient de la terre, de l’eau, du feu et de l’air.',
    ['Le bois qui brûle donne le feu, la fumée (l’air), la vapeur d’eau (l’eau) et la cendre (la terre).'],
    'Antiquité : quatre éléments (terre, eau, feu, air), idée tirée de la combustion du bois.', 'histoire.html?vue=elements',
    'Le bois qui brûle et les quatre éléments', 'Un morceau de bois brûle : le feu, la fumée, la vapeur, la cendre',
    'Commençons l’histoire, il y a très longtemps, chez les Grecs. Ils regardaient un morceau de bois qui brûle. '
    'Il y a le feu. Il y a la fumée qui monte : pour eux, c’est l’air. Il y a de la vapeur d’eau : c’est l’eau. Et à la '
    'fin, il reste la cendre : c’est la terre. Alors ils ont pensé que toute la matière est faite de quatre éléments : '
    'la terre, l’eau, le feu et l’air. C’est le tout premier modèle.',
    'نبداو القصة، من زمان بزاف، عند les Grecs. كانو كيشوفو واحد الحطبة كتشعل. كاين le feu. كاينة '
    'la fumée كتطلع: بالنسبة ليهم، هادي هي l’air. كاين la vapeur d’eau: هادي هي l’eau. وفالأخير، كتبقى la cendre: '
    'هادي هي la terre. إذن قالو بلي كاع la matière مصنوعة من quatre éléments: la terre، l’eau، le feu و l’air. هادا '
    'هو أول modèle.',
    pointage=[rp('واحد الحطبة', 'bois'), pu('كاين le feu', 'feu'), pu('كاينة la fumée', 'fumee'),
              pu('كاين la vapeur', 'vapeur'), pu('كتبقى la cendre', 'cendre'), pu('quatre éléments', 'quatre'),
              rp('quatre éléments', 'quatre')],
    centre=[ce('quatre éléments', 'terre · eau · feu · air')],
    cahier='I. Histoire du modèle de l’atome', comps=['C1'])

D['at_h2_dalton'] = diapo(
    'at_h2_dalton', 'Dalton : des sphères pleines', 'Dalton (1766-1844) : la matière est faite de petites sphères.',
    ['Des sphères pleines, qu’on ne peut pas couper.', 'Plusieurs sortes d’atomes, qui s’assemblent pour faire la matière.'],
    'Dalton : l’atome est une petite sphère pleine ; il existe plusieurs sortes d’atomes.', 'histoire.html?vue=dalton',
    'Les sphères de Dalton', 'Des petites sphères pleines de plusieurs couleurs, qui s’assemblent',
    'Beaucoup plus tard, le savant Dalton propose un autre modèle. Pour lui, la matière est faite de toutes petites '
    'sphères pleines, qu’on ne peut pas couper : les atomes. Il y a plusieurs sortes d’atomes, ici en plusieurs couleurs. '
    'Et ces atomes s’assemblent pour faire toute la matière. Retiens : Dalton, des sphères pleines.',
    'من بعد بزاف، العالم Dalton عطا modèle آخر. بالنسبة ليه، la matière مصنوعة من des sphères صغار بزاف و pleines، '
    'ما يمكنش نقطعوهم: هادو هما les atomes. كاينين بزاف ديال الأنواع ديال les atomes، هنا بألوان مختلفين. وهاد les '
    'atomes كيتجمعو باش يديرو كاع la matière. حفظ: Dalton، des sphères pleines.',
    pointage=[pu('des sphères صغار', 'spheres'), rp('des sphères صغار', 'spheres'), pu('كاينين بزاف ديال الأنواع', 'sortes'),
              pu('كيتجمعو', 'assemble'), rp('كيتجمعو', 'assemble')],
    centre=[ce('حفظ: Dalton', 'Dalton : sphères pleines')],
    cahier='Dalton : l’atome est une petite sphère pleine ; plusieurs sortes d’atomes.', comps=['C1'])

D['at_h3_thomson'] = diapo(
    'at_h3_thomson', 'Thomson : l’électron et le pain aux raisins', 'Thomson (1897) découvre l’électron, une particule négative.',
    ['Dans un tube, des particules sont attirées par la plaque + : elles sont négatives. Ce sont les électrons.', 'Modèle de Thomson (1898) : une boule de matière positive avec des électrons dedans, comme les raisins dans un pain.'],
    'Thomson découvre l’électron (négatif) ; modèle du « pain aux raisins » : des électrons dans une matière positive.', 'histoire.html?vue=thomson',
    'Le tube de Thomson et le pain aux raisins', 'Des particules déviées vers la plaque + ; une boule rose avec des électrons dedans',
    'En mille huit cent quatre-vingt-dix-sept, le savant Thomson fait une expérience dans un tube de verre. Des petites '
    'particules sortent d’une plaque. Regarde : elles sont attirées par la plaque positive. Rappelle-toi la règle : '
    'signes contraires, elles s’attirent. Donc ces particules sont négatives : ce sont les électrons. Alors la sphère '
    'pleine de Dalton ne suffit plus. Thomson propose un nouveau modèle : une boule de matière positive, et les électrons '
    'sont dedans, comme les raisins dans un pain. On l’appelle le pain aux raisins.',
    'ف mille huit cent quatre-vingt-dix-sept، العالم Thomson دار واحد التجربة فواحد le tube ديال الزاج. كيخرجو des '
    'particules صغار من واحد la plaque. شوف: كيمشيو نيشان ل la plaque positive. تفكر la règle: signes contraires، '
    's’attirent. إذن هاد les particules négatives: هادو هما les électrons. إذن la sphère pleine ديال Dalton ما بقاتش '
    'كافية. Thomson عطا modèle جديد: واحد الكورة ديال matière positive، و les électrons داخلها، بحال الزبيب فالخبز. '
    'كنسميوه le pain aux raisins.',
    pointage=[pu('واحد le tube', 'tube'), rp('واحد le tube', 'tube'), pu('شوف: كيمشيو', 'devie'), rp('شوف: كيمشيو', 'devie'),
              pu('هادو هما les électrons', 'electron'), pu('واحد الكورة', 'pain'), rp('واحد الكورة', 'pain'),
              pu('بحال الزبيب', 'raisins')],
    centre=[ce('هادو هما les électrons', 'électron : particule négative'), ce('le pain aux raisins', 'Thomson : électrons dans une matière +')],
    cahier='Thomson (1897) découvre l’électron, négatif ; modèle du « pain aux raisins » : électrons dans une matière positive.',
    comps=['C1'],
    q=question('qcm', 'Dans le modèle de Thomson, les électrons sont…',
               ['des sphères pleines sans charge', 'des particules positives', 'des particules négatives, dans une boule de matière positive'], 2,
               'شوف هاد السؤال: ف le modèle ديال Thomson، شنو هما les électrons؟',
               ('برافو! les électrons négatifs، داخل واحد الكورة ديال matière positive، بحال الزبيب فالخبز.', 'Oui : des particules négatives dans une boule de matière positive, comme des raisins dans un pain.'),
               {0: (('لا، هادا هو le modèle ديال Dalton. Thomson لقى des particules عندهم charge.', 'Non : ça, c’est le modèle de Dalton. Thomson a trouvé des particules chargées.'),
                    ('الجواب: les électrons négatifs، داخل matière positive. des sphères pleines هادا Dalton.', 'Réponse : des électrons négatifs dans une matière positive ; les sphères pleines, c’est Dalton.')),
                1: (('لا. les électrons كيمشيو ل la plaque positive: شنو هي la charge ديالهم؟', 'Non : les électrons vont vers la plaque + ; quelle est donc leur charge ?'),
                    ('signes contraires كيتجادبو: les électrons négatifs، داخل matière positive.', 'Signes contraires s’attirent : les électrons sont négatifs, dans une matière positive.'))}))

D['at_h4_montage'] = diapo(
    'at_h4_montage', 'L’expérience de Rutherford : le montage', 'Des particules α (chargées +) envoyées sur une feuille d’or très mince.',
    ['Une boîte de plomb envoie des particules α, chargées positivement.', 'Une feuille d’or très mince au centre ; un écran fluorescent tout autour : chaque particule qui le touche fait un petit éclair.'],
    'Rutherford : on bombarde une feuille d’or très mince avec des particules α (positives).', 'rutherford.html?vue=montage',
    'Le montage de Rutherford, vu de dessus', 'La boîte de plomb, le faisceau α, la feuille d’or, l’écran en anneau',
    'Vers mille neuf cent dix, le savant Rutherford veut vérifier le modèle de Thomson. Regarde le montage, vu de dessus. '
    'À gauche, une boîte de plomb : elle envoie des particules alpha, toutes petites, chargées positivement. Au centre, '
    'une feuille d’or très très mince. Tout autour, un écran fluorescent : quand une particule le touche, il fait un petit '
    'éclair. Comme ça, on voit où chaque particule arrive.',
    'تقريبا ف mille neuf cent dix، العالم Rutherford بغا يتأكد من le modèle ديال Thomson. شوف le montage، من الفوق. '
    'على اليسر، واحد la boîte ديال le plomb: كتصيفط des particules alpha، صغار بزاف، chargées positivement. فالوسط، '
    'واحد la feuille d’or رقيقة بزاف. وداير بيها، واحد l’écran fluorescent: ملي كتقيسو شي particule، كيدير واحد '
    'éclair صغير. هكا كنشوفو فين كتوصل كل particule.',
    pointage=[pu('على اليسر', 'source'), rp('على اليسر', 'source'), pu('كتصيفط des particules alpha', 'faisceau'),
              pu('فالوسط', 'feuille'), rp('فالوسط', 'feuille'), pu('وداير بيها', 'ecran'), rp('وداير بيها', 'ecran'),
              pu('éclair صغير', 'eclair')],
    centre=[ce('chargées positivement', 'particules α : charge +'), ce('la feuille d’or', 'feuille d’or très mince')],
    cahier='Rutherford : des particules α (chargées +) sont envoyées sur une feuille d’or très mince.', comps=['C1'])

D['at_h5_resultats'] = diapo(
    'at_h5_resultats', 'Rutherford : ce qu’on observe', 'On tire beaucoup de particules α : où arrivent-elles ?',
    ['La plupart traversent la feuille sans être déviées.', 'Quelques-unes sont déviées ; de très rares reviennent en arrière.'],
    'La plupart des particules α traversent la feuille d’or sans déviation ; quelques-unes sont déviées.', 'rutherford.html?vue=resultats',
    'Les éclairs sur l’écran', 'Presque tous les éclairs derrière la feuille ; quelques-uns sur les côtés ; un très rare du côté de la source',
    'Maintenant on tire beaucoup de particules alpha sur la feuille d’or, et on regarde les éclairs sur l’écran. '
    'Observe bien où ils arrivent. Presque toutes les particules passent tout droit, à travers la feuille, sans être '
    'déviées. Quelques-unes sont déviées sur le côté. Et une très rare revient en arrière, comme une balle qui rebondit '
    'sur un mur. Rutherford a été très surpris : avec le pain aux raisins, toutes devaient passer.',
    'دابا كنضربو بزاف ديال les particules alpha على la feuille d’or، وكنشوفو les éclairs على l’écran. شوف مزيان '
    'فين كيوصلو. تقريبا كاع les particules كيدوزو نيشان، من وسط la feuille، بلا ما يتعوجو. شي وحدين كيتعوجو على '
    'الجنب. وواحدة نادرة بزاف كترجع اللور، بحال كورة كتضرب فالحيط. Rutherford تفاجأ بزاف: مع le pain aux raisins، '
    'كاملين كان خاصهم يدوزو.',
    demarrer='reset',
    pointage=[pu('دابا كنضربو', 'tir'), pu('تقريبا كاع les particules', 'traversent'), pu('شي وحدين كيتعوجو', 'deviees'),
              rp('شي وحدين كيتعوجو', 'deviees'), pu('وواحدة نادرة', 'rebondit'), rp('وواحدة نادرة', 'rebondit'),
              pu('Rutherford تفاجأ', 'bilan')],
    centre=[ce('كيدوزو نيشان', 'la plupart : tout droit'), ce('كترجع اللور', 'très rares : retour')],
    observation=obs('شوف مزيان فين كيوصلو.', 'Où arrivent presque toutes les particules α ?',
                    'فين كيوصلو تقريبا كاع les particules alpha؟',
                    [('Regarde les éclairs les plus nombreux sur l’écran.', 'شوف فين كاينين بزاف ديال les éclairs.', 'traversent'),
                     ('Sont-ils derrière la feuille, ou du côté de la source ?', 'واش من ور la feuille، ولا من جيهة la boîte؟', None)],
                    ['Elles reviennent toutes en arrière', 'Presque toutes passent tout droit à travers la feuille', 'Elles restent toutes collées à la feuille'], 1,
                    [('لا، غير واحدة نادرة بزاف اللي رجعات. شوف فين كاينين كثر ديال les éclairs.', 'Non : une seule, très rare, revient. Regarde où sont la plupart des éclairs.'),
                     ('برافو! تقريبا كاملين دازو نيشان من وسط la feuille.', 'Oui : presque toutes traversent la feuille tout droit.'),
                     ('لا، les éclairs كاينين على l’écran، ماشي على la feuille. فين كاينين كثرهم؟', 'Non : les éclairs sont sur l’écran, pas sur la feuille. Où sont-ils surtout ?')],
                    ('الجواب: تقريبا كاع les particules دازو نيشان من وسط la feuille، بلا ما يتعوجو.', 'Presque toutes les particules α traversent la feuille tout droit, sans déviation.'),
                    gestes=[pu('', 'traversent') | {}, {'repere': 'traversent'}], sim_avant={'conclusions': False}, sim_apres={'conclusions': True}),
    cahier='La plupart des α traversent la feuille d’or sans déviation ; quelques-unes sont déviées ; très rares reviennent.',
    comps=['C1'])
D['at_h5_resultats']['concentration']['observation']['gestes'] = [{'commande': 'play_until', 'parametres': {'moment': 'traversent'}}, {'repere': 'traversent'}]

D['at_h6_interpretation'] = diapo(
    'at_h6_interpretation', 'Rutherford : le noyau et le vide', 'L’atome est surtout du vide, avec au centre un noyau très petit, chargé +.',
    ['Loin des noyaux, la particule α ne rencontre rien : elle passe tout droit.', 'Près d’un noyau : + et + se repoussent, elle est déviée ; droit sur un noyau : elle revient.'],
    'Conclusion de Rutherford : l’atome est surtout du vide ; au centre, un noyau très petit, chargé positivement, où est presque toute la masse.', 'rutherford.html?vue=interpretation',
    'Les atomes d’or vus de très près', 'Trois trajets de particules α : loin des noyaux, près d’un noyau, droit sur un noyau',
    'Comment expliquer ça ? Zoomons sur la feuille d’or : elle est faite d’atomes. Rutherford imagine chaque atome comme '
    'un grand espace presque vide, avec au centre un noyau minuscule, chargé positivement. Une particule alpha qui passe '
    'loin des noyaux ne rencontre rien : elle passe tout droit. Une particule qui passe près d’un noyau : plus et plus, '
    'ils se repoussent, elle est déviée. Et une particule qui arrive droit sur un noyau revient en arrière. Conclusion : '
    'l’atome est surtout du vide, avec au centre un noyau très petit et positif.',
    'كيفاش نفسرو هادشي؟ نكبرو la feuille d’or: مصنوعة من des atomes. Rutherford تخيل كل atome بحال واحد البلاصة '
    'كبيرة تقريبا خاوية، وفالوسط واحد le noyau صغير بزاف، chargé positivement. particule alpha اللي كدوز بعيدة على les '
    'noyaux ما كتلقى والو: كدوز نيشان. particule اللي كدوز قريبة من شي noyau: plus و plus، se repoussent، '
    'كتتعوج. و particule اللي جاية نيشان على le noyau كترجع اللور. la conclusion: l’atome فيه غير الخوا تقريبا، '
    'وفالوسط واحد le noyau صغير بزاف و positif.',
    pointage=[pu('نكبرو la feuille', 'zoom'), rp('نكبرو la feuille', 'zoom'), pu('اللي كدوز بعيدة', 'vide'), rp('اللي كدوز بعيدة', 'vide'),
              pu('اللي كدوز قريبة', 'devie'), rp('اللي كدوز قريبة', 'devie'), pu('اللي جاية نيشان', 'rebond'), rp('اللي جاية نيشان', 'rebond'),
              pu('la conclusion', 'conclusion'), rp('la conclusion', 'conclusion')],
    centre=[ce('la conclusion', 'atome : surtout du vide + noyau positif')],
    cahier='Donc l’atome est surtout du vide ; au centre, un noyau très petit, chargé positivement.',
    comps=['C1'],
    q=question('qcm', 'Pourquoi la plupart des particules α traversent-elles la feuille d’or sans être déviées ?',
               ['Parce que la feuille d’or est trouée', 'Parce que l’atome est surtout du vide', 'Parce que les particules α n’ont pas de charge'], 1,
               'شوف هاد السؤال: علاش تقريبا كاع les particules alpha كيدوزو من la feuille d’or بلا ما يتعوجو؟',
               ('برافو! l’atome فيه غير الخوا تقريبا، و le noyau صغير بزاف: ما كتلقى والو.', 'Oui : l’atome est surtout du vide ; le noyau est minuscule, la particule ne rencontre rien.'),
               {0: (('لا، la feuille ما فيهاش ثقوب كبار. فكر فشنو كاين داخل l’atome.', 'Non : la feuille n’a pas de trous. Pense à ce qu’il y a dans l’atome.'),
                    ('الجواب: l’atome فيه غير الخوا تقريبا، داكشي علاش كيدوزو.', 'Réponse : l’atome est surtout du vide ; c’est pour ça qu’elles passent.')),
                2: (('لا، les particules alpha chargées positivement. شنو كاين داخل l’atome؟', 'Non : les particules α sont chargées + . Qu’y a-t-il dans l’atome ?'),
                    ('الجواب: l’atome فيه غير الخوا تقريبا؛ les particules alpha عندهم charge plus.', 'Réponse : l’atome est surtout du vide ; les α sont bien chargées +.'))}))

D['at_h7_bohr'] = diapo(
    'at_h7_bohr', 'Bohr : des orbites', 'Bohr (1913) : les électrons tournent sur des orbites, comme des planètes.',
    ['Le noyau au centre ; les électrons tournent sur des orbites de rayon bien défini.', 'Comme les planètes autour du Soleil.'],
    'Bohr (1913) : les électrons tournent autour du noyau sur des orbites de rayon défini.', 'histoire.html?vue=bohr',
    'Le modèle de Bohr', 'Un noyau ; deux orbites ; les électrons tournent ; le Soleil et ses planètes',
    'Après Rutherford, le savant Bohr, en mille neuf cent treize, précise le modèle. Au centre, le noyau. Autour, des '
    'orbites, des cercles de rayon bien défini. Et les électrons tournent sur ces orbites. C’est comme les planètes qui '
    'tournent autour du Soleil : le noyau joue le rôle du Soleil, les électrons sont les planètes.',
    'من بعد Rutherford، العالم Bohr، ف mille neuf cent treize، زاد وضح le modèle. فالوسط، le noyau. ودايرين بيه، des '
    'orbites، يعني دوائر عندهم rayon محدد. و les électrons كيدورو على هاد les orbites. بحال les planètes اللي كيدورو '
    'على الشمس: le noyau هو الشمس، و les électrons هما les planètes.',
    pointage=[pu('فالوسط، le noyau', 'noyau'), rp('فالوسط، le noyau', 'noyau'), pu('des orbites', 'orbites'), rp('des orbites', 'orbites'),
              pu('كيدورو على هاد', 'tournent'), pu('بحال les planètes', 'planetes'), rp('بحال les planètes', 'planetes')],
    centre=[ce('كيدورو على هاد', 'Bohr : électrons sur des orbites')],
    cahier='Bohr (1913) : les électrons tournent autour du noyau sur des orbites de rayon défini.', comps=['C1'])

D['at_h8_nuage'] = diapo(
    'at_h8_nuage', 'Aujourd’hui : le nuage électronique', 'On ne peut pas connaître exactement la position d’un électron.',
    ['Schrödinger et De Broglie (1926) : l’électron est quelque part dans un nuage autour du noyau.', 'Le nuage est plus dense là où l’électron a le plus de chances d’être.'],
    'Modèle actuel : le noyau entouré d’un nuage électronique ; la position exacte d’un électron ne peut pas être connue.', 'histoire.html?vue=nuage',
    'Le nuage électronique et la frise des modèles', 'Les orbites s’effacent ; un nuage ; la frise des six modèles s’allume',
    'En mille neuf cent vingt-six, les savants Schrödinger et De Broglie montrent qu’on ne peut pas connaître exactement '
    'la position d’un électron. Alors les orbites s’effacent. L’électron est quelque part dans un nuage autour du noyau : '
    'c’est le nuage électronique. Voici toute l’histoire en une frise : les quatre éléments, Dalton, Thomson, Rutherford, '
    'Bohr, et le nuage d’aujourd’hui. Chaque modèle a changé à cause d’une nouvelle expérience.',
    'ف mille neuf cent vingt-six، العلماء Schrödinger و De Broglie بينو بلي ما يمكنش نعرفو بالضبط فين كاين l’électron. '
    'إذن les orbites كيتمسحو. l’électron كاين شي بلاصة فواحد السحابة دايرة ب le noyau: هادا هو le nuage '
    'électronique. هادي هي القصة كاملة فواحد la frise: les quatre éléments، Dalton، Thomson، Rutherford، Bohr، و le '
    'nuage ديال اليوم. كل modèle تبدل بسبب واحد التجربة جديدة.',
    pointage=[pu('les orbites كيتمسحو', 'flou'), pu('هادا هو le nuage', 'nuage'), rp('هادا هو le nuage', 'nuage'),
              pu('هادي هي القصة', 'frise'), rp('les quatre éléments، Dalton', 'modele_1'), pu('و le nuage ديال اليوم', 'frise_fin'),
              rp('كل modèle تبدل', 'frise')],
    centre=[ce('هادا هو le nuage', 'aujourd’hui : le nuage électronique')],
    cahier='Aujourd’hui : un noyau entouré d’un nuage électronique ; on ne peut pas connaître la position exacte d’un électron.',
    comps=['C1'],
    q=question('true_false', 'Dans le modèle actuel, on connaît exactement la position de chaque électron.', ['Vrai', 'Faux'], 1,
               'شوف هاد الجملة: ف le modèle ديال اليوم، كنعرفو بالضبط فين كاين كل électron. vrai ou faux؟',
               ('برافو، faux! ما يمكنش نعرفو بالضبط فين كاين l’électron: كاين شي بلاصة ف le nuage.', 'Bonne réponse : Faux. On ne peut pas connaître la position exacte ; l’électron est quelque part dans le nuage.'),
               {0: (('لا. شوف شنو وقع ل les orbites فالآخر ديال القصة.', 'Non : regarde ce que sont devenues les orbites à la fin de l’histoire.'),
                    ('faux: ما يمكنش نعرفو بالضبط فين كاين l’électron؛ داكشي علاش كنهضرو على le nuage.', 'Faux : on ne peut pas connaître sa position exacte ; c’est pourquoi on parle de nuage.'))}, timeout=30))

# ═════════════════════════════════ SÉANCE 3 — les constituants et l'écriture du noyau ═════════════════════════════════

D['at_s1_atome'] = diapo(
    'at_s1_atome', 'La structure de l’atome', 'Un noyau positif, entouré d’un nuage d’électrons négatifs.',
    ['Au centre : le noyau, minuscule, chargé +.', 'Autour : le nuage électronique, avec les électrons, chargés −.'],
    'L’atome est formé d’un noyau chargé positivement, entouré d’un nuage d’électrons chargés négativement.', 'structure.html?vue=atome',
    'L’atome de carbone', 'Un nuage bleu avec six électrons ; au centre, le noyau, agrandi dans la loupe',
    'Voici l’atome tel qu’on le voit aujourd’hui, ici l’atome de carbone. D’abord, le nuage électronique. Dedans, '
    'les électrons, qui bougent tout le temps : ils sont chargés négativement. Et au centre, tout petit, le noyau : '
    'il est chargé positivement. Agrandissons-le dans la loupe : il est fait de petites billes. Retiens : un noyau '
    'positif au centre, entouré d’un nuage d’électrons négatifs.',
    'هادا هو l’atome كيفما كنشوفوه اليوم، هنا l’atome ديال le carbone. اللول، le nuage électronique. داخلو، les '
    'électrons، اللي كيتحركو ديما: chargés négativement. وفالوسط، صغير بزاف، le noyau: chargé positivement. نكبروه '
    'ف la loupe: مصنوع من كويرات صغار. حفظ: noyau positif فالوسط، داير بيه nuage ديال les électrons négatifs.',
    pointage=[pu('اللول، le nuage', 'nuage'), rp('اللول، le nuage', 'nuage'), pu('داخلو، les', 'electrons'), rp('داخلو، les', 'electrons'),
              pu('نكبروه', 'noyau'), rp('نكبروه', 'noyau'), pu('حفظ: noyau positif', 'vide')],
    centre=[ce('حفظ: noyau positif', 'atome = noyau (+) + nuage d’électrons (−)')],
    cahier='II. Les constituants de l’atome', comps=['C2'])

D['at_s2_electron'] = diapo(
    'at_s2_electron', 'L’électron', 'Une particule de charge −e et de masse très petite.',
    ['Charge : q = −e, avec e = 1,6 × 10⁻¹⁹ C (charge élémentaire ; C : le coulomb).', 'Masse : m_e = 9,1 × 10⁻³¹ kg.'],
    'Électron : q = −e ; e = 1,6 × 10⁻¹⁹ C ; m_e = 9,1 × 10⁻³¹ kg.', 'structure.html?vue=electron',
    'L’électron et sa carte d’identité', 'Un électron agrandi ; sa charge et sa masse s’écrivent',
    'Regardons de près l’électron. Sa charge est q égale moins e. Le petit e, c’est la charge élémentaire : e égale un '
    'virgule six fois dix puissance moins dix-neuf coulomb. Le coulomb, noté C, c’est l’unité de la charge électrique. '
    'Et sa masse est très très petite : m e égale neuf virgule un fois dix puissance moins trente et un kilogramme.',
    'نشوفو l’électron من قريب. la charge ديالو هي q égale moins e. le petit e، هي la charge élémentaire: e égale un '
    'virgule six fois dix puissance moins dix-neuf coulomb. le coulomb، كنكتبوه C، هو l’unité ديال la charge '
    'électrique. و la masse ديالو صغيرة بزاف: m e égale neuf virgule un fois dix puissance moins trente et un kilogramme.',
    pointage=[pu('نشوفو l’électron', 'electron'), rp('نشوفو l’électron', 'electron'), pu('q égale moins e', 'charge'),
              pu('le petit e', 'e'), pu('و la masse ديالو', 'masse')],
    centre=[ce('q égale moins e', 'q = −e'), ce('moins dix-neuf coulomb', 'e = 1,6 × 10⁻¹⁹ C'), ce('trente et un kilogramme', 'm_e = 9,1 × 10⁻³¹ kg')],
    cahier='Formule : électron : q = −e ; e = 1,6 × 10⁻¹⁹ C (coulomb) ; m_e = 9,1 × 10⁻³¹ kg', comps=['C2'])

D['at_s3_noyau'] = diapo(
    'at_s3_noyau', 'Le noyau : protons et neutrons', 'Les nucléons : des protons (+e) et des neutrons (neutres).',
    ['Proton : charge +e ; m_p = 1,673 × 10⁻²⁷ kg.', 'Neutron : charge nulle ; m_n = 1,675 × 10⁻²⁷ kg.', 'Nucléons = protons + neutrons ; m_p ≈ m_n.'],
    'Le noyau est formé de nucléons : des protons (charge +e) et des neutrons (neutres) ; m_p ≈ m_n.', 'structure.html?vue=noyau',
    'Le noyau de carbone compté', 'Les six protons s’allument un à un, puis les six neutrons',
    'Entrons dans le noyau de l’atome de carbone. Il contient deux sortes de billes. Les protons d’abord : comptons-les. '
    'Un, deux, trois, quatre, cinq, six : six protons. Chaque proton a la charge plus e, et sa masse est un virgule six '
    'sept trois fois dix puissance moins vingt-sept kilogramme. Les autres billes sont les neutrons : un, deux, trois, '
    'quatre, cinq, six. Le neutron est neutre, sa charge est nulle, et sa masse est presque la même que celle du proton. '
    'Les protons et les neutrons ensemble s’appellent les nucléons.',
    'ندخلو ل le noyau ديال l’atome ديال le carbone. فيه جوج أنواع ديال الكويرات. les protons اللول: نحسبوهم. un، '
    'deux، trois، quatre، cinq، six: six protons. كل proton عندو la charge plus e، و la masse ديالو un virgule six sept '
    'trois fois dix puissance moins vingt-sept kilogramme. الكويرات الأخرين هما les neutrons: un، deux، trois، quatre، '
    'cinq، six. le neutron neutre، la charge ديالو nulle، و la masse ديالو تقريبا بحال ديال le proton. les protons و '
    'les neutrons مع بعض كنسميوهم les nucléons.',
    pointage=[rp('ندخلو ل le noyau', 'noyau'), pu('نحسبوهم', 'protons'), rp('six protons', 'protons'),
              pu('الكويرات الأخرين', 'neutrons'), rp('le neutron neutre', 'neutrons'), pu('مع بعض كنسميوهم', 'nucleons'), rp('مع بعض كنسميوهم', 'nucleons')],
    centre=[ce('la charge plus e', 'proton : +e'), ce('nulle', 'neutron : 0'), ce('les nucléons', 'nucléons = protons + neutrons')],
    cahier='| Particule | Charge | Masse |\n| électron | −e | 9,1 × 10⁻³¹ kg |\n| proton | +e | 1,673 × 10⁻²⁷ kg |\n| neutron | 0 | 1,675 × 10⁻²⁷ kg |',
    comps=['C2'],
    q=question('qcm', 'Le noyau d’un atome est formé…', ['de protons et d’électrons', 'de protons et de neutrons', 'd’électrons et de neutrons'], 1,
               'شوف هاد السؤال: le noyau ديال l’atome، من شنو مصنوع؟',
               ('برافو! le noyau فيه les protons و les neutrons، يعني les nucléons.', 'Oui : le noyau est formé de protons et de neutrons, les nucléons.'),
               {0: (('لا. les électrons ماشي فوسط le noyau. فين كاينين؟', 'Non : les électrons ne sont pas dans le noyau. Où sont-ils ?'),
                    ('les électrons كاينين ف le nuage. le noyau فيه les protons و les neutrons.', 'Les électrons sont dans le nuage ; le noyau contient protons et neutrons.')),
                2: (('لا. les électrons ف le nuage، ماشي ف le noyau. شنو هما الكويرات positives ديال le noyau؟', 'Non : les électrons sont dans le nuage. Comment s’appellent les billes + du noyau ?'),
                    ('le noyau فيه les protons، chargés plus، و les neutrons. les électrons داير بيه.', 'Le noyau contient les protons (+) et les neutrons ; les électrons sont autour.'))}))

D['at_s4_notation'] = diapo(
    'at_s4_notation', 'L’écriture du noyau : A, Z et N', 'ᴬ_Z X : A nucléons (en haut), Z protons (en bas).',
    ['A : nombre de nucléons (nombre de masse) ; Z : nombre de protons (numéro atomique).', 'N = A − Z : nombre de neutrons.'],
    'Noyau noté ᴬ_Z X : A = nombre de nucléons, Z = nombre de protons, N = A − Z = nombre de neutrons.', 'structure.html?vue=notation',
    'L’écriture ¹²₆C et le noyau compté', 'A : les douze nucléons comptés ; Z : les six protons ; N : les six neutrons',
    'Comment écrire un noyau ? On écrit le symbole de l’atome, ici C pour le carbone. En haut à gauche, le nombre A. '
    'Comptons les nucléons : un, deux, trois, jusqu’à douze. A égale douze : c’est le nombre de nucléons, on l’appelle '
    'aussi le nombre de masse. En bas à gauche, le nombre Z. Comptons seulement les protons : un, deux, jusqu’à six. Z '
    'égale six : c’est le nombre de protons, le numéro atomique. Et les neutrons ? N égale A moins Z, douze moins six, '
    'six neutrons.',
    'كيفاش نكتبو le noyau؟ كنكتبو le symbole ديال l’atome، هنا C ديال le carbone. الفوق على اليسر، le nombre A. '
    'نحسبو les nucléons: un، deux، trois، حتى douze. A égale douze: هادا هو le nombre de nucléons، كنسميوه حتى le '
    'nombre de masse. التحت على اليسر، le nombre Z. نحسبو غير les protons: un، deux، حتى six. Z égale six: هادا هو le '
    'nombre de protons، le numéro atomique. و les neutrons؟ N égale A moins Z، douze moins six، six neutrons.',
    pointage=[pu('كنكتبو le symbole', 'symbole'), rp('كنكتبو le symbole', 'symbole'), rp('الفوق على اليسر', 'A'),
              pu('نحسبو les nucléons', 'A'), rp('التحت على اليسر', 'Z'), pu('نحسبو غير les protons', 'Z'),
              pu('N égale A moins Z', 'N'), rp('N égale A moins Z', 'N')],
    centre=[ce('A égale douze', 'A = nombre de nucléons'), ce('Z égale six', 'Z = nombre de protons'), ce('N égale A moins Z', 'N = A − Z')],
    cahier='Définition : noyau noté ᴬ_Z X ; A = nombre de nucléons (nombre de masse) ; Z = nombre de protons (numéro atomique).\nFormule : N = A − Z (nombre de neutrons)',
    figures=[{'type': 'schema', 'titre': 'L’écriture du noyau', 'legende': 'A en haut à gauche, Z en bas à gauche du symbole.',
              'cadre': {'l': 10, 'h': 5},
              'elements': [{'f': 'texte', 't': 'X', 'at': [5, 2.2], 'taille': 'grand', 'ancre': 'centre'},
                           {'f': 'texte', 't': 'A', 'at': [4.1, 3.4], 'ancre': 'centre', 'couleur': 'jaune'},
                           {'f': 'texte', 't': 'Z', 'at': [4.1, 1.2], 'ancre': 'centre', 'couleur': 'rose'},
                           {'f': 'fleche', 'de': [2.2, 4.2], 'a': [3.8, 3.5], 'texte': 'nucléons', 'pos': 'o'},
                           {'f': 'fleche', 'de': [2.2, 0.5], 'a': [3.8, 1.1], 'texte': 'protons', 'pos': 'o'},
                           {'f': 'texte', 't': 'N = A − Z', 'at': [7.8, 2.4], 'ancre': 'centre', 'couleur': 'cyan'}]}],
    comps=['C3'])

D['at_s5_neutralite'] = diapo(
    'at_s5_neutralite', 'L’atome est neutre', 'Autant d’électrons que de protons : Z électrons.',
    ['Noyau : Z protons → charge +Z·e ; électrons : Z → charge −Z·e.', 'Somme : 0 : l’atome est électriquement neutre.'],
    'L’atome est électriquement neutre : il a autant d’électrons que de protons (Z électrons).', 'structure.html?vue=neutralite',
    'Les charges de l’atome de carbone', 'Le noyau +6e ; les six électrons comptés −6e ; la somme vaut zéro',
    'Une propriété très importante : l’atome est neutre. Prenons encore le carbone. Le noyau a six protons : sa charge '
    'est plus six e. Comptons les électrons du nuage : un, deux, trois, quatre, cinq, six. Six électrons : leur charge '
    'est moins six e. Plus six e plus moins six e, égale zéro : l’atome est neutre. Donc, dans un atome, le nombre '
    'd’électrons égale le nombre de protons, égale Z.',
    'واحد la propriété مهمة بزاف: l’atome neutre. ناخدو مرة أخرى le carbone. le noyau فيه six protons: la charge '
    'ديالو plus six e. نحسبو les électrons ديال le nuage: un، deux، trois، quatre، cinq، six. six électrons: la charge '
    'ديالهم moins six e. plus six e plus moins six e، égale zéro: l’atome neutre. إذن، ف l’atome، le nombre '
    'd’électrons égale le nombre de protons، égale Z.',
    pointage=[pu('le noyau فيه six protons', 'noyau'), rp('le noyau فيه six protons', 'noyau'), pu('نحسبو les électrons', 'electrons'),
              rp('six électrons: la charge', 'electrons'), pu('plus six e plus moins', 'charges'), pu('égale zéro', 'neutre'),
              pu('إذن، ف l’atome', 'regle'), rp('إذن، ف l’atome', 'regle')],
    centre=[ce('égale zéro', '+6e + (−6e) = 0'), ce('égale Z', 'nombre d’électrons = Z')],
    cahier='L’atome est neutre : Q_noyau = +Z·e et Q_électrons = −Z·e ; donc nombre d’électrons = Z.',
    comps=['C3'])

D['at_s6_methode'] = diapo(
    'at_s6_methode', 'Méthode : le tableau des particules (¹²₆C)', 'Lire Z et A, puis remplir nombre et charge de chaque particule.',
    ['Protons : Z ; charge +Z·e.', 'Neutrons : N = A − Z ; charge 0.', 'Électrons : Z (atome neutre) ; charge −Z·e.'],
    'Méthode : protons = Z ; neutrons = A − Z ; électrons = Z ; charges +Z·e, 0, −Z·e.', 'structure.html?vue=tableau&atome=C',
    'Le tableau de ¹²₆C', 'Les particules de l’atome s’allument et se comptent, chaque nombre vole dans sa case',
    'Voici la méthode, pas à pas, avec le carbone douze six. On dessine un tableau : protons, neutrons, électrons, avec '
    'leur nombre et leur charge. Première étape, les protons : Z égale six. On les compte : six protons, et leur charge '
    'plus six e. Deuxième étape, les neutrons : N égale A moins Z, douze moins six, six. Leur charge : zéro. Troisième '
    'étape, les électrons : l’atome est neutre, donc autant que les protons : six électrons, charge moins six e. Le '
    'tableau est rempli.',
    'هادي هي la méthode، خطوة بخطوة، مع le carbone douze six. كنرسمو واحد le tableau: les protons، les neutrons، les '
    'électrons، مع le nombre و la charge. الخطوة اللولة، les protons: Z égale six. كنحسبوهم: six protons، و la charge '
    'plus six e. الخطوة الثانية، les neutrons: N égale A moins Z، douze moins six، six. la charge ديالهم: zéro. الخطوة '
    'الثالثة، les électrons: l’atome neutre، إذن بحال les protons: six électrons، charge moins six e. le tableau عمر.',
    demarrer='reset',
    pointage=[pu('كنرسمو واحد le tableau', 'notation'), rp('كنرسمو واحد le tableau', 'tableau'), pu('الخطوة اللولة', 'protons'),
              rp('plus six e', 'case_protons'), pu('الخطوة الثانية', 'neutrons'), rp('douze moins six', 'calcul_N'),
              pu('الخطوة الثالثة', 'electrons'), rp('le tableau عمر', 'tableau')],
    centre=[ce('Z égale six', 'protons : Z'), ce('N égale A moins Z', 'neutrons : A − Z'), ce('بحال les protons', 'électrons : Z')],
    cahier='Méthode : 1) protons = Z, charge +Z·e ; 2) neutrons N = A − Z, charge 0 ; 3) électrons = Z, charge −Z·e',
    comps=['C3'])

D['at_s7_toi'] = diapo(
    'at_s7_toi', 'À toi : le tableau du chlore ³⁵₁₇Cl', 'Même méthode, sur l’atome de chlore.',
    ['³⁵₁₇Cl : A = 35, Z = 17.'],
    'Exemple : ³⁵₁₇Cl : 17 protons (+17e), 18 neutrons (0), 17 électrons (−17e).', 'structure.html?vue=tableau&atome=Cl',
    'Le tableau de ³⁵₁₇Cl', 'L’atome de chlore et son tableau, rempli après ta réponse',
    'À toi maintenant, avec l’atome de chlore : trente-cinq, dix-sept, C l. Voici son écriture et son tableau vide. '
    'Lis bien A et Z, puis fais les trois étapes dans ta tête : les protons, les neutrons, les électrons. Ensuite, '
    'réponds à la question au tableau.',
    'دابا نتا، مع l’atome ديال le chlore: trente-cinq، dix-sept، C l. هادي هي الكتابة ديالو و le tableau خاوي. قرا '
    'مزيان A و Z، ومن بعد دير les trois étapes فراسك: les protons، les neutrons، les électrons. من بعد، جاوب على '
    'السؤال فالسبورة.',
    demarrer='reset',
    pointage=[pu('هادي هي الكتابة', 'notation'), rp('هادي هي الكتابة', 'notation'), rp('قرا', 'notation'), rp('les trois étapes', 'tableau')],
    centre=[ce('قرا', 'A = 35 · Z = 17')],
    apres=[{'etapes': [pu('', 'protons') | {}, {'commande': 'play_until', 'parametres': {'moment': 'neutrons'}},
                       {'commande': 'play_until', 'parametres': {'moment': 'electrons'}}, {'repere': 'case_neutrons'}], 'duree_s': 9}],
    cahier='Exemple : ³⁵₁₇Cl : protons 17 (+17e) ; neutrons 35 − 17 = 18 (0) ; électrons 17 (−17e).',
    comps=['C3'],
    q=question('qcm', 'Combien de neutrons le noyau ³⁵₁₇Cl contient-il ?', ['17', '18', '35'], 1,
               'شوف هاد السؤال: شحال من neutron كاين ف le noyau ديال le chlore trente-cinq dix-sept؟',
               ('برافو! N égale A moins Z، trente-cinq moins dix-sept، dix-huit neutrons.', 'Oui : N = A − Z = 35 − 17 = 18 neutrons.'),
               {0: (('dix-sept هو Z، يعني les protons. les neutrons كنحسبوهم ب A moins Z.', '17, c’est Z : le nombre de protons. Les neutrons : N = A − Z.'),
                    ('N égale trente-cinq moins dix-sept، dix-huit. dix-sept هما les protons.', 'N = 35 − 17 = 18 ; 17, ce sont les protons.')),
                2: (('trente-cinq هو A، يعني كاع les nucléons. نقص منو les protons.', '35, c’est A : tous les nucléons. Retire les protons.'),
                    ('N égale A moins Z، trente-cinq moins dix-sept، يعني dix-huit.', 'N = A − Z = 35 − 17 = 18.'))},
               demo=('les données: A égale trente-cinq، Z égale dix-sept. la relation: N égale A moins Z. l’application: N égale '
                     'trente-cinq moins dix-sept. le résultat: N égale dix-huit neutrons. و les électrons: l’atome neutre، إذن dix-sept électrons.',
                     [('A = 35 ; Z = 17', 'les données', 'notation'), ('N = A − Z', 'la relation', None),
                      ('N = 35 − 17', 'l’application', 'calcul_N'), ('N = 18 neutrons', 'le résultat', None),
                      ('atome neutre : 17 électrons', 'و les électrons', None)])))
D['at_s7_toi']['concentration']['apres_reponse'][0]['etapes'][0] = {'commande': 'play_until', 'parametres': {'moment': 'protons'}}

# ═════════════════════════════════ SÉANCE 4 — la masse et les dimensions ═════════════════════════════════

D['at_m1_masse'] = diapo(
    'at_m1_masse', 'La masse de l’atome', 'Les électrons sont si légers qu’on les néglige : m ≈ A·m_p.',
    ['m = Z·m_p + N·m_n + Z·m_e.', 'm_p ≈ 1 840 × m_e : on néglige les électrons ; m_p ≈ m_n.', 'Donc m ≈ A·m_p : la masse est dans le noyau.'],
    'm = Z·m_p + N·m_n + Z·m_e ; m_e ≪ m_p et m_p ≈ m_n, donc m ≈ A·m_p : la masse de l’atome est concentrée dans le noyau.', 'masse.html?vue=somme',
    'Un proton contre un électron sur la balance', 'La balance penche avec un proton ; un électron ne la fait presque pas bouger',
    'Quelle est la masse d’un atome ? On additionne tout : la masse des Z protons, plus celle des N neutrons, plus celle '
    'des Z électrons. Mais regarde la balance. On pose un proton : elle penche. De l’autre côté, on pose un électron : '
    'elle ne bouge presque pas. Calculons le rapport : m p sur m e, environ mille huit cent quarante. Un proton pèse '
    'comme mille huit cent quarante électrons ! Alors on néglige les électrons. Et comme m p est presque égale à m n, '
    'chaque nucléon pèse environ m p : m environ égale A fois m p. La masse de l’atome est dans son noyau.',
    'شحال la masse ديال l’atome؟ كنجمعو كلشي: la masse ديال Z protons، plus ديال N neutrons، plus ديال Z électrons. '
    'ولكن شوف la balance. كنحطو واحد le proton: كتميل. من الجيهة الأخرى، كنحطو واحد l’électron: تقريبا ما '
    'كتتحركش. نحسبو le rapport: m p sur m e، تقريبا mille huit cent quarante. واحد le proton وزنو بحال mille huit cent '
    'quarante électrons! إذن كنهملو les électrons. وحيت m p تقريبا égale m n، كل nucléon وزنو تقريبا m p: m environ '
    'égale A fois m p. la masse ديال l’atome كاينة ف le noyau ديالو.',
    pointage=[pu('كنجمعو كلشي', 'formule'), rp('كنجمعو كلشي', 'formule'), rp('ولكن شوف la balance', 'balance'),
              pu('كنحطو واحد le proton', 'proton'), pu('كنحطو واحد l’électron', 'electron'), pu('نحسبو le rapport', 'rapport'),
              rp('نحسبو le rapport', 'rapport'), pu('إذن كنهملو', 'neglige'), pu('وحيت m p', 'approx'), rp('A fois m p', 'approx')],
    centre=[ce('كنجمعو كلشي', 'm = Z·m_p + N·m_n + Z·m_e'), ce('mille huit cent quarante électrons', 'm_p ≈ 1 840 × m_e'), ce('A fois m p', 'm ≈ A·m_p')],
    cahier='III. La masse et les dimensions de l’atome\nFormule : m ≈ A·m_p (m_p ≈ 1,67 × 10⁻²⁷ kg) : la masse de l’atome est dans le noyau.',
    comps=['C4'])

D['at_m2_methode'] = diapo(
    'at_m2_methode', 'Méthode : la masse de l’atome d’oxygène ¹⁶₈O', 'Lire A, appliquer m ≈ A·m_p, écrire le résultat avec l’unité.',
    ['A = 16 ; m ≈ A·m_p = 16 × 1,67 × 10⁻²⁷ kg ≈ 2,67 × 10⁻²⁶ kg.'],
    'Méthode : 1) lire A ; 2) m ≈ A·m_p ; 3) application numérique ; 4) résultat en kg.', 'masse.html?vue=methode&atome=O',
    'La masse de l’atome d’oxygène', 'Les seize nucléons comptés ; le calcul s’écrit ligne par ligne',
    'La méthode, avec l’oxygène seize huit. Première étape : lire A sur l’écriture. Comptons les nucléons : seize. A '
    'égale seize. Deuxième étape, la relation : m environ égale A fois m p. Troisième étape, l’application numérique : '
    'm environ égale seize fois un virgule six sept fois dix puissance moins vingt-sept kilogramme. Seize fois un virgule '
    'six sept, ça fait vingt-six virgule soixante-douze. Dernière étape, on écrit avec un seul chiffre avant la virgule : '
    'm environ égale deux virgule six sept fois dix puissance moins vingt-six kilogramme.',
    'la méthode، مع l’oxygène seize huit. الخطوة اللولة: نقراو A ف الكتابة. نحسبو les nucléons: seize. A égale seize. '
    'الخطوة الثانية، la relation: m environ égale A fois m p. الخطوة الثالثة، l’application numérique: m environ égale '
    'seize fois un virgule six sept fois dix puissance moins vingt-sept kilogramme. seize fois un virgule six sept، '
    'كيعطي vingt-six virgule soixante-douze. الخطوة الأخيرة، كنكتبو ب chiffre واحد قبل la virgule: m environ égale deux '
    'virgule six sept fois dix puissance moins vingt-six kilogramme.',
    demarrer='reset',
    pointage=[pu('الخطوة اللولة', 'donnees'), rp('الخطوة اللولة', 'donnees'), pu('نحسبو les nucléons', 'A'),
              pu('الخطوة الثانية', 'relation'), pu('الخطوة الثالثة', 'an'), pu('كيعطي vingt-six', 'calcul'),
              pu('الخطوة الأخيرة', 'resultat'), rp('الخطوة الأخيرة', 'resultat')],
    centre=[ce('الخطوة الأخيرة', 'm ≈ 2,67 × 10⁻²⁶ kg')],
    cahier='Méthode : 1) lire A ; 2) m ≈ A·m_p ; 3) remplacer (m_p ≈ 1,67 × 10⁻²⁷ kg) ; 4) résultat en kg, un chiffre avant la virgule',
    comps=['C4'])

D['at_m3_toi'] = diapo(
    'at_m3_toi', 'À toi : la masse de l’atome de carbone ¹²₆C', 'Même méthode : A, puis m ≈ A·m_p.',
    ['¹²₆C ; m_p ≈ 1,67 × 10⁻²⁷ kg.'],
    'Exemple : ¹²₆C : m ≈ 12 × 1,67 × 10⁻²⁷ ≈ 2,0 × 10⁻²⁶ kg.', 'masse.html?vue=methode&atome=C',
    'La masse de l’atome de carbone', 'Le noyau du carbone ; le calcul s’écrit après ta réponse',
    'À toi, avec le carbone douze six. Voici son écriture et son noyau. Lis A, écris la relation, fais l’application '
    'numérique, puis choisis le bon résultat au tableau. N’oublie pas l’unité : le kilogramme.',
    'دابا نتا، مع le carbone douze six. هادي هي الكتابة ديالو و le noyau ديالو. قرا A، كتب la relation، دير '
    'l’application numérique، ومن بعد ختار le résultat الصحيح فالسبورة. ما تنساش l’unité: le kilogramme.',
    demarrer='reset',
    pointage=[pu('هادي هي الكتابة', 'donnees'), rp('هادي هي الكتابة', 'donnees'), rp('و le noyau ديالو', 'noyau')],
    apres=[{'sim_avant': {'conclusions': False},
            'etapes': [{'commande': 'set_parameters', 'parametres': {'conclusions': True}},
                       {'commande': 'play_until', 'parametres': {'moment': 'A'}}, {'commande': 'play_until', 'parametres': {'moment': 'resultat'}},
                       {'repere': 'resultat'}], 'duree_s': 9}],
    cahier='Exemple : ¹²₆C : m ≈ 12 × 1,67 × 10⁻²⁷ kg ≈ 2,0 × 10⁻²⁶ kg.',
    comps=['C4'],
    q=question('qcm', 'La masse approchée de l’atome ¹²₆C est… (m_p ≈ 1,67 × 10⁻²⁷ kg)',
               ['m ≈ 1,0 × 10⁻²⁶ kg', 'm ≈ 2,0 × 10⁻²⁶ kg', 'm ≈ 2,0 × 10⁻²⁷ kg'], 1,
               'شوف هاد السؤال: شحال تقريبا la masse ديال l’atome ديال le carbone douze six؟',
               ('برافو! m environ égale douze fois un virgule six sept fois dix puissance moins vingt-sept، يعني تقريبا deux fois dix puissance moins vingt-six kilogramme.', 'Oui : m ≈ 12 × 1,67 × 10⁻²⁷ ≈ 2,0 × 10⁻²⁶ kg.'),
               {0: (('هادي ضربتي ف Z، six. la relation فيها A، le nombre de nucléons.', 'Tu as multiplié par Z = 6 ; la relation utilise A, le nombre de nucléons.'),
                    ('A égale douze، ماشي six: douze fois un virgule six sept كيعطي vingt virgule zéro quatre، يعني deux fois dix puissance moins vingt-six.', 'A = 12, pas 6 : 12 × 1,67 = 20,04 → 2,0 × 10⁻²⁶ kg.')),
                2: (('الحساب قريب، ولكن شوف la puissance de dix ملي كتنقل la virgule.', 'Le calcul est proche, mais regarde la puissance de dix quand tu déplaces la virgule.'),
                    ('vingt fois dix puissance moins vingt-sept كيساوي deux fois dix puissance moins vingt-six، ماشي moins vingt-sept.', '20 × 10⁻²⁷ = 2,0 × 10⁻²⁶ kg, pas 10⁻²⁷.'))},
               demo=('les données: A égale douze، m p environ égale un virgule six sept fois dix puissance moins vingt-sept kilogramme. '
                     'la relation: m environ égale A fois m p. l’application: m environ égale douze fois un virgule six sept fois dix puissance moins vingt-sept. '
                     'douze fois un virgule six sept égale vingt virgule zéro quatre. le résultat: m environ égale deux fois dix puissance moins vingt-six kilogramme.',
                     [('A = 12 ; m_p ≈ 1,67 × 10⁻²⁷ kg', 'les données', 'donnees'), ('m ≈ A·m_p', 'la relation', None),
                      ('m ≈ 12 × 1,67 × 10⁻²⁷', 'l’application', None), ('12 × 1,67 = 20,04', 'douze fois un virgule six sept égale', None),
                      ('m ≈ 2,0 × 10⁻²⁶ kg', 'le résultat', None)])))

D['at_d1_rapport'] = diapo(
    'at_d1_rapport', 'Les dimensions de l’atome', 'Rayon de l’atome ≈ 10⁻¹⁰ m ; rayon du noyau ≈ 10⁻¹⁵ m.',
    ['r_atome/r_noyau = 10⁻¹⁰/10⁻¹⁵ = 10⁵ : le noyau est cent mille fois plus petit.', 'L’atome est surtout du vide : structure lacunaire.'],
    'r_atome ≈ 10⁻¹⁰ m ; r_noyau ≈ 10⁻¹⁵ m ; r_atome/r_noyau = 10⁵ : l’atome a une structure lacunaire.', 'dimensions.html?vue=rapport',
    'L’atome et son noyau', 'Le rayon de l’atome ; le noyau invisible, agrandi ; le rapport 10⁵',
    'Combien mesure un atome ? Son rayon est de l’ordre de dix puissance moins dix mètre. Et le noyau ? Il est si petit '
    'qu’on ne le voit même pas ici : agrandissons-le. Son rayon est de l’ordre de dix puissance moins quinze mètre. '
    'Calculons le rapport : dix puissance moins dix sur dix puissance moins quinze, on retranche les exposants, dix '
    'puissance cinq. Le noyau est cent mille fois plus petit que l’atome ! Entre les deux, il y a du vide : on dit que '
    'l’atome a une structure lacunaire.',
    'شحال كبير l’atome؟ le rayon ديالو تقريبا dix puissance moins dix mètre. و le noyau؟ صغير بزاف حتى ما كيبانش هنا: '
    'نكبروه. le rayon ديالو تقريبا dix puissance moins quinze mètre. نحسبو le rapport: dix puissance moins dix sur dix '
    'puissance moins quinze، كننقصو les exposants، dix puissance cinq. le noyau صغير ب cent mille مرة من l’atome! '
    'بيناتهم كاين الخوا: كنقولو بلي l’atome عندو structure lacunaire.',
    pointage=[pu('le rayon ديالو تقريبا dix puissance moins dix', 'atome'), rp('le rayon ديالو تقريبا dix puissance moins dix', 'atome'),
              pu('نكبروه', 'noyau'), rp('نكبروه', 'noyau'), pu('نحسبو le rapport', 'rapport'), rp('نحسبو le rapport', 'rapport'),
              pu('بيناتهم كاين الخوا', 'vide'), rp('بيناتهم كاين الخوا', 'vide')],
    centre=[ce('dix puissance cinq', 'r_atome/r_noyau = 10⁵')],
    cahier='Formule : r_atome ≈ 10⁻¹⁰ m ; r_noyau ≈ 10⁻¹⁵ m ; r_atome/r_noyau = 10⁵\nDonc l’atome est surtout du vide : structure lacunaire.',
    comps=['C5'])

D['at_d2_stade'] = diapo(
    'at_d2_stade', 'Une image : la bille au centre du stade', 'Si le noyau était une bille de 1 mm, l’atome serait grand comme un stade.',
    ['1 mm × 10⁵ = 10⁵ mm = 100 m.', 'Les électrons seraient sur les tribunes ; entre eux et la bille : du vide.'],
    'Image : noyau = bille de 1 mm ; atome = stade de 100 m.', 'dimensions.html?vue=stade',
    'La bille et le stade', 'Une bille d’un millimètre ; la caméra recule : la bille au centre d’un stade',
    'Une deuxième façon de voir ce vide. Imagine que le noyau est une petite bille d’un millimètre. L’atome est cent mille '
    'fois plus grand : un millimètre fois dix puissance cinq, ça fait cent mètres. Reculons : la bille est au centre '
    'd’un stade de foot ! Les électrons seraient tout là-bas, sur les tribunes. Et entre la bille et les tribunes, du '
    'vide, rien que du vide.',
    'طريقة ثانية باش نشوفو هاد الخوا. تخيل بلي le noyau واحد البيلة صغيرة ديال un millimètre. l’atome كبر منها ب cent '
    'mille مرة: un millimètre fois dix puissance cinq، كيعطي cent mètres. نرجعو اللور: البيلة فالوسط ديال واحد '
    'الملعب ديال الكورة! les électrons غادي يكونو بعاد، فوق les tribunes. وبين البيلة و les tribunes، الخوا، غير الخوا.',
    pointage=[pu('تخيل بلي le noyau', 'bille'), rp('تخيل بلي le noyau', 'bille'), pu('un millimètre fois', 'fois'),
              pu('نرجعو اللور', 'stade'), rp('نرجعو اللور', 'stade'), pu('les électrons غادي يكونو', 'electrons'), pu('وبين البيلة', 'vide')],
    centre=[ce('كيعطي cent mètres', '1 mm × 10⁵ = 100 m')],
    comps=['C5'],
    q=question('qcm', 'Le rayon d’un atome est environ … fois plus grand que celui de son noyau.', ['10²', '10⁵', '10¹⁵'], 1,
               'شوف هاد السؤال: le rayon ديال l’atome كبر من le rayon ديال le noyau بشحال من مرة؟',
               ('برافو! dix puissance moins dix sur dix puissance moins quinze، dix puissance cinq، cent mille مرة.', 'Oui : 10⁻¹⁰/10⁻¹⁵ = 10⁵, cent mille fois.'),
               {0: (('صغير بزاف. عاود le rapport: dix puissance moins dix sur dix puissance moins quinze.', 'Trop petit. Refais le rapport 10⁻¹⁰/10⁻¹⁵.'),
                    ('moins dix moins moins quinze كيساوي cinq: dix puissance cinq.', '−10 − (−15) = 5 : 10⁵.')),
                2: (('dix puissance moins quinze هو le rayon ديال le noyau، ماشي le rapport. قسم.', '10⁻¹⁵ m est le rayon du noyau, pas le rapport. Divise.'),
                    ('le rapport: dix puissance moins dix sur dix puissance moins quinze، يعني dix puissance cinq.', 'Le rapport : 10⁻¹⁰/10⁻¹⁵ = 10⁵.'))},
               demo=('les données: r atome environ dix puissance moins dix mètre، r noyau environ dix puissance moins quinze mètre. '
                     'le rapport: r atome sur r noyau. l’application: dix puissance moins dix sur dix puissance moins quinze. '
                     'كننقصو les exposants: moins dix plus quinze، cinq. le résultat: dix puissance cinq.',
                     [('r_atome ≈ 10⁻¹⁰ m ; r_noyau ≈ 10⁻¹⁵ m', 'les données', None), ('r_atome/r_noyau', 'le rapport', None),
                      ('10⁻¹⁰/10⁻¹⁵ = 10⁻¹⁰⁺¹⁵', 'l’application', None), ('= 10⁵', 'le résultat', None)])))

# ═════════════════════════════════ SÉANCE 5 — isotopes, ions, élément chimique ═════════════════════════════════

D['at_e1_isotopes'] = diapo(
    'at_e1_isotopes', 'Les isotopes', 'Même Z, A différent : des isotopes.',
    ['¹²₆C, ¹³₆C, ¹⁴₆C : 6 protons chacun ; 6, 7 et 8 neutrons.', 'Des isotopes : même nombre de protons Z, nombres de neutrons (et A) différents.'],
    'Isotopes : atomes de même Z mais de A différents (nombres de neutrons différents).', 'element.html?vue=isotopes',
    'Les trois isotopes du carbone', 'Trois noyaux de carbone ; les protons comptés (6) ; les neutrons (6, 7, 8)',
    'IV. Voici trois noyaux de carbone : carbone douze, carbone treize et carbone quatorze. Comptons leurs protons : '
    'chacun en a six. Même Z, égale six : ce sont tous des atomes de carbone. Maintenant les neutrons : six dans le '
    'premier, sept dans le deuxième, huit dans le troisième. Ils n’ont pas le même A. On dit que ce sont des isotopes : '
    'même Z, mais A différent.',
    'هادو trois noyaux ديال le carbone: carbone douze، carbone treize و carbone quatorze. نحسبو les protons ديالهم: كل '
    'واحد فيه six. نفس Z، égale six: كاملين atomes ديال le carbone. دابا les neutrons: six فاللول، sept فالثاني، huit '
    'فالثالث. ما عندهمش نفس A. كنقولو بلي هادو des isotopes: même Z، ولكن A différent.',
    pointage=[pu('carbone douze', 'c12'), pu('carbone treize', 'c13'), pu('carbone quatorze', 'c14'),
              pu('نحسبو les protons', 'protons'), pu('دابا les neutrons', 'neutrons'), pu('كنقولو بلي هادو des isotopes', 'definition'),
              rp('كنقولو بلي هادو des isotopes', 'definition')],
    centre=[ce('des isotopes', 'isotopes : même Z, A différent')],
    cahier='IV. L’élément chimique\nDéfinition : des isotopes sont des atomes de même Z mais de nombres de nucléons A différents.',
    comps=['C6'])
D['at_e1_isotopes']['speech_text']['fr'] = D['at_e1_isotopes']['speech_text']['fr'].replace('IV. ', '')

D['at_e2_ions'] = diapo(
    'at_e2_ions', 'Les ions monoatomiques', 'Un atome qui perd ou gagne des électrons devient un ion.',
    ['Na perd un électron → Na⁺ : 11 + et 10 − → cation (ion positif).', 'Cl gagne un électron → Cl⁻ : 17 + et 18 − → anion (ion négatif).'],
    'Ion monoatomique : atome qui a perdu des électrons (cation, positif) ou en a gagné (anion, négatif).', 'element.html?vue=ions',
    'L’ion sodium et l’ion chlorure', 'L’atome de sodium perd un électron ; l’atome de chlore en gagne un',
    'Un atome peut perdre ou gagner des électrons. Regarde l’atome de sodium : onze protons, onze électrons, il est '
    'neutre. Il perd un électron : il reste onze plus et dix moins. Il a une charge plus e : c’est l’ion Na plus, un '
    'cation, un ion positif. Maintenant l’atome de chlore : dix-sept protons, dix-sept électrons. Il gagne un électron : '
    'dix-sept plus et dix-huit moins. Charge moins e : c’est l’ion Cl moins, un anion, un ion négatif. Attention : le '
    'noyau ne change pas, seuls les électrons changent.',
    'l’atome يمكن ليه يخسر ولا يربح des électrons. شوف l’atome ديال le sodium: onze protons، onze électrons، neutre. '
    'كيخسر واحد l’électron: كيبقاو onze plus و dix moins. عندو charge plus e: هادا هو l’ion Na plus، un cation، ion '
    'positif. دابا l’atome ديال le chlore: dix-sept protons، dix-sept électrons. كيربح واحد l’électron: dix-sept plus و '
    'dix-huit moins. charge moins e: هادا هو l’ion Cl moins، un anion، ion négatif. رد البال: le noyau ما كيتبدلش، غير '
    'les électrons اللي كيتبدلو.',
    pointage=[pu('شوف l’atome ديال le sodium', 'na'), rp('شوف l’atome ديال le sodium', 'sodium'), pu('كيخسر واحد', 'perd'),
              pu('هادا هو l’ion Na plus', 'cation'), pu('دابا l’atome ديال le chlore', 'cl'), rp('دابا l’atome ديال le chlore', 'chlore'),
              pu('كيربح واحد', 'gagne'), pu('هادا هو l’ion Cl moins', 'anion')],
    centre=[ce('un cation', 'perd des électrons → cation (+)'), ce('un anion', 'gagne des électrons → anion (−)')],
    cahier='Définition : un ion monoatomique est un atome qui a perdu (cation, ex. Na⁺) ou gagné (anion, ex. Cl⁻) des électrons.\nAttention : le noyau ne change pas ; seuls les électrons changent.',
    figures=[{'type': 'schema', 'titre': 'Atome → ion', 'legende': 'Le noyau reste le même ; seul le nombre d’électrons change.', 'cadre': {'l': 10, 'h': 4},
              'elements': [{'f': 'texte', 't': 'Na', 'at': [1.2, 3], 'ancre': 'centre'}, {'f': 'fleche', 'de': [2.2, 3], 'a': [4.2, 3], 'texte': '− 1 e⁻', 'pos': 'n'},
                           {'f': 'texte', 't': 'Na⁺ (cation)', 'at': [6.2, 3], 'ancre': 'centre', 'couleur': 'rose'},
                           {'f': 'texte', 't': 'Cl', 'at': [1.2, 1], 'ancre': 'centre'}, {'f': 'fleche', 'de': [2.2, 1], 'a': [4.2, 1], 'texte': '+ 1 e⁻', 'pos': 'n'},
                           {'f': 'texte', 't': 'Cl⁻ (anion)', 'at': [6.2, 1], 'ancre': 'centre', 'couleur': 'cyan'}]}],
    comps=['C6'],
    q=question('qcm', 'L’atome d’aluminium (Z = 13) donne l’ion Al³⁺. Cet ion…', ['a gagné 3 électrons', 'a perdu 3 électrons', 'a perdu 3 protons'], 1,
               'شوف هاد السؤال: l’atome ديال l’aluminium كيعطي l’ion Al trois plus. شنو وقع ليه؟',
               ('برافو! trois plus: خسر trois électrons، كيبقاو treize plus و dix moins.', 'Oui : Al³⁺ a perdu 3 électrons : 13 + et 10 −.'),
               {0: (('لا. ملي كيربح des électrons، كتولي la charge négative. هنا la charge plus.', 'Non : gagner des électrons rend l’ion négatif ; ici il est positif.'),
                    ('trois plus يعني خسر trois électrons: treize plus و dix moins.', 'Al³⁺ a perdu 3 électrons : 13 + et 10 −.')),
                2: (('لا، le noyau ما كيتبدلش. غير les électrons اللي كيتبدلو.', 'Non : le noyau ne change pas ; seuls les électrons changent.'),
                    ('les protons كيبقاو treize؛ خسر trois électrons، إذن trois plus.', 'Les protons restent 13 ; il a perdu 3 électrons, d’où 3+.'))}))

D['at_e3_element'] = diapo(
    'at_e3_element', 'L’élément chimique', 'Toutes les entités de même Z forment un élément chimique.',
    ['¹⁶₈O, ¹⁷₈O et l’ion O²⁻ ont tous Z = 8 : ils appartiennent à l’élément oxygène.'],
    'Élément chimique : ensemble des entités (atomes, isotopes, ions) qui ont le même Z.', 'element.html?vue=element',
    'L’élément oxygène', 'Deux isotopes de l’oxygène et l’ion oxyde ; Z = 8 s’allume pour les trois',
    'Voici l’atome oxygène seize, l’atome oxygène dix-sept, et l’ion O deux moins, qui a gagné deux électrons. Ils sont '
    'différents, mais regarde le nombre en bas : Z égale huit pour les trois. Huit protons chacun. On dit qu’ils '
    'appartiennent au même élément chimique : l’élément oxygène. Un élément chimique, c’est toutes les entités qui ont '
    'le même Z.',
    'هادا l’atome oxygène seize، و l’atome oxygène dix-sept، و l’ion O deux moins، اللي ربح deux électrons. مختلفين، '
    'ولكن شوف le nombre اللي التحت: Z égale huit للثلاثة. huit protons كل واحد. كنقولو بلي كاملين ف نفس l’élément '
    'chimique: l’élément oxygène. l’élément chimique هو كاع اللي عندهم نفس Z.',
    pointage=[pu('هادا l’atome oxygène seize', 'o16'), pu('l’atome oxygène dix-sept', 'o17'), pu('l’ion O deux moins', 'ion'),
              rp('l’ion O deux moins', 'ion'), pu('ولكن شوف le nombre', 'z'), pu('كنقولو بلي كاملين', 'element'), rp('كنقولو بلي كاملين', 'element')],
    centre=[ce('نفس Z', 'élément chimique = même Z')],
    cahier='Définition : un élément chimique est l’ensemble des entités (atomes, ions) qui ont le même numéro atomique Z.',
    comps=['C6'],
    q=question('qcm', '¹⁶₈O, ¹⁷₈O et O²⁻ appartiennent au même élément chimique car ils ont le même…',
               ['nombre de protons Z', 'nombre de neutrons', 'nombre d’électrons'], 0,
               'شوف هاد السؤال: oxygène seize، oxygène dix-sept و O deux moins ف نفس l’élément. علاش؟',
               ('برافو! نفس Z، huit protons. هادا هو اللي كيحدد l’élément.', 'Oui : même Z = 8 protons ; c’est Z qui définit l’élément.'),
               {1: (('لا. oxygène seize فيه huit neutrons و oxygène dix-sept فيه neuf. شوف le nombre اللي التحت.', 'Non : ¹⁶O a 8 neutrons, ¹⁷O en a 9. Regarde le nombre du bas.'),
                    ('les neutrons مختلفين. اللي كيتشابهو فيه هو Z، huit protons.', 'Les neutrons diffèrent ; ce qu’ils ont en commun, c’est Z = 8.')),
                2: (('لا. O deux moins فيه dix électrons، والآخرين huit. شنو اللي ما كيتبدلش؟', 'Non : O²⁻ a 10 électrons, les autres 8. Qu’est-ce qui ne change pas ?'),
                    ('les électrons مختلفين؛ اللي كيبقى هو Z، huit protons.', 'Les électrons diffèrent ; ce qui reste, c’est Z = 8.'))}))

D['at_e4_conservation'] = diapo(
    'at_e4_conservation', 'L’élément chimique se conserve', 'Sulfate de cuivre + soude : un précipité bleu ; le cuivre est toujours là.',
    ['Solution bleue de sulfate de cuivre (ions Cu²⁺) + soude (ions HO⁻) → précipité bleu Cu(OH)₂(s).', 'L’élément cuivre change de forme, mais il ne disparaît pas.'],
    'L’élément chimique se conserve au cours d’une transformation chimique : Cu²⁺(aq) + 2HO⁻(aq) → Cu(OH)₂(s).', 'element.html?vue=conservation',
    'La conservation de l’élément cuivre', 'Un bécher bleu ; la soude goutte à goutte ; un précipité bleu tombe au fond',
    'Une expérience. Dans ce bécher, une solution de sulfate de cuivre : elle est bleue, à cause des ions cuivre Cu deux '
    'plus. Avec le compte-gouttes, on ajoute de la soude, qui contient des ions hydroxyde H O moins. Regarde bien ce qui '
    'se passe dans le bécher. Un précipité bleu se forme et tombe au fond : c’est l’hydroxyde de cuivre. Les ions cuivre '
    'ont quitté la solution, mais le cuivre n’a pas disparu : il est dans le précipité. Cu deux plus plus deux H O moins '
    'donne Cu O H deux fois. L’élément cuivre se conserve.',
    'تجربة. فهاد le bécher، واحد la solution ديال le sulfate de cuivre: زرقا، بسبب les ions cuivre، Cu deux plus. '
    'ب le compte-gouttes، كنزيدو la soude، اللي فيها les ions hydroxyde، H O moins. شوف مزيان شنو كيوقع ف le bécher. '
    'كيتكون واحد le précipité زرق وكيطيح للتحت: هادا هو l’hydroxyde de cuivre. les ions cuivre خرجو من la solution، '
    'ولكن le cuivre ما تمشاش: كاين ف le précipité. l’élément cuivre كيبقى، كنقولو se conserve.',
    pointage=[pu('فهاد le bécher', 'becher'), rp('فهاد le bécher', 'becher'), pu('ب le compte-gouttes', 'soude'),
              pu('كيتكون واحد le précipité', 'precipite'), rp('كيتكون واحد le précipité', 'precipite'), pu('les ions cuivre خرجو', 'cuivre'),
              pu('l’élément cuivre كيبقى', 'conserve')],
    centre=[ce('les ions cuivre خرجو', 'Cu²⁺(aq) + 2HO⁻(aq) → Cu(OH)₂(s)'), ce('se conserve', 'l’élément cuivre se conserve')],
    observation=obs('شوف مزيان شنو كيوقع ف le bécher.', 'Que se forme-t-il dans le bécher ?', 'شنو اللي كيتكون ف le bécher؟',
                    [('Regarde le fond du bécher.', 'شوف القاع ديال le bécher.', 'precipite'), ('Ce sont de petits flocons bleus.', 'كاينين des flocons صغار زرقين.', None)],
                    ['Des bulles de gaz', 'Un précipité bleu qui tombe au fond', 'Rien, la solution reste pareille'], 1,
                    [('لا، ما كاينش gaz. شوف القاع ديال le bécher.', 'Non : pas de gaz. Regarde le fond du bécher.'),
                     ('برافو! واحد le précipité زرق كيتكون وكيطيح للتحت.', 'Oui : un précipité bleu se forme et tombe au fond.'),
                     ('لا، كاين شي حاجة كتتكون. شوف القاع.', 'Non : quelque chose se forme. Regarde le fond.')],
                    ('الجواب: واحد le précipité زرق، l’hydroxyde de cuivre، كيطيح للتحت.', 'Un précipité bleu (hydroxyde de cuivre) se forme et tombe au fond.'),
                    gestes=[{'commande': 'play_until', 'parametres': {'moment': 'precipite'}}, {'repere': 'precipite'}],
                    sim_avant={'conclusions': False}, sim_apres={'conclusions': True}),
    cahier='Exemple : Cu²⁺(aq) + 2HO⁻(aq) → Cu(OH)₂(s) (précipité bleu).\nDonc un élément chimique se conserve au cours d’une transformation chimique.',
    comps=['C6'])

# ═════════════════════════════════ SÉANCE 6 — la répartition électronique ═════════════════════════════════

D['at_c1_couches'] = diapo(
    'at_c1_couches', 'Les couches électroniques K, L, M', 'Les électrons se rangent en couches ; chaque couche a un nombre limité de places.',
    ['K : 2 électrons au plus ; L : 8 ; M : 8 (pour Z ≤ 18).', 'Règle 1 : une couche contient un nombre limité d’électrons.', 'Règle 2 : on remplit K, puis L, puis M.'],
    'Couches K (2), L (8), M (8) ; règle 1 : nombre limité ; règle 2 : on remplit K, puis L, puis M.', 'couches.html?vue=couches',
    'Les couches et leurs places', 'Autour du noyau, trois couches ; leurs places s’allument et se comptent',
    'V. Les électrons ne sont pas rangés n’importe comment : ils sont sur des couches autour du noyau. La première couche '
    's’appelle K : comptons ses places, une, deux. La couche K prend deux électrons au plus. La deuxième couche, L : un, '
    'deux, jusqu’à huit places. La troisième, M : huit places aussi, pour les atomes de ce cours. Première règle : une '
    'couche contient un nombre limité d’électrons. Deuxième règle : on remplit d’abord K, puis L, puis M.',
    'les électrons ماشي مرتبين كيفما جا: كاينين على des couches داير بيهم le noyau. la couche اللولة سميتها K: نحسبو '
    'les places ديالها، une، deux. la couche K كتاخد deux électrons على الأكثر. la couche الثانية، L: un، deux، حتى huit '
    'places. الثالثة، M: huit places حتى هي، ل les atomes ديال هاد الدرس. la règle اللولة: la couche فيها عدد محدود '
    'ديال les électrons. la règle الثانية: كنعمرو K اللول، من بعد L، من بعد M.',
    pointage=[rp('داير بيهم le noyau', 'noyau'), pu('la couche اللولة', 'k'), rp('la couche K كتاخد', 'k'), pu('la couche الثانية', 'l'),
              rp('la couche الثانية', 'l'), pu('الثالثة، M', 'm'), rp('الثالثة، M', 'm'), pu('la règle اللولة', 'regle1'), pu('la règle الثانية', 'regle2')],
    centre=[ce('deux électrons على الأكثر', 'K : 2 · L : 8 · M : 8'), ce('la règle الثانية', 'on remplit K, puis L, puis M')],
    cahier='V. La répartition électronique\n| Couche | K | L | M |\n| Électrons au plus | 2 | 8 | 8 |\nRègle 1 : une couche contient un nombre limité d’électrons.\nRègle 2 : on remplit K, puis L, puis M.',
    comps=['C7'])
D['at_c1_couches']['speech_text']['fr'] = D['at_c1_couches']['speech_text']['fr'].replace('V. ', '')

D['at_c2_methode'] = diapo(
    'at_c2_methode', 'Méthode : la structure électronique de ¹⁶₈O', 'Compter les électrons, puis remplir K, puis L.',
    ['O : Z = 8 → 8 électrons.', 'K : 2 (saturée) ; L : 6.', 'Structure : (K)²(L)⁶ ; couche externe : L (6 électrons).'],
    'Méthode : 1) nombre d’électrons ; 2) remplir K, puis L, puis M ; 3) écrire (K)ᵃ(L)ᵇ(M)ᶜ ; 4) couche externe.', 'couches.html?vue=remplir&atome=O',
    'Les électrons de l’oxygène tombent couche par couche', 'Huit électrons comptés ; deux tombent dans K, six dans L',
    'La méthode, avec l’atome d’oxygène. Première étape : combien d’électrons ? Z égale huit, l’atome est neutre, donc '
    'huit électrons. Comptons-les : un, deux, trois, jusqu’à huit. Deuxième étape : on les place. D’abord K : deux '
    'électrons, la couche K est pleine, on dit qu’elle est saturée. Ensuite L : les six qui restent. Troisième étape : '
    'on écrit la structure électronique : K deux, L six. La dernière couche occupée, ici L, s’appelle la couche externe : '
    'elle a six électrons.',
    'la méthode، مع l’atome ديال l’oxygène. الخطوة اللولة: شحال من électron؟ Z égale huit، l’atome neutre، إذن huit '
    'électrons. نحسبوهم: un، deux، trois، حتى huit. الخطوة الثانية: كنحطوهم. اللول K: deux électrons، la couche K '
    'عمرات، كنقولو saturée. من بعد L: les six اللي بقاو. الخطوة الثالثة: كنكتبو la structure électronique: K deux، L '
    'six. la couche الأخيرة اللي فيها électrons، هنا L، كنسميوها la couche externe: فيها six électrons.',
    demarrer='reset',
    pointage=[pu('نحسبوهم', 'compte'), rp('نحسبوهم', 'electrons'), pu('اللول K', 'k'), rp('اللول K', 'k'), pu('من بعد L', 'l'),
              rp('من بعد L', 'l'), pu('الخطوة الثالثة', 'structure'), rp('الخطوة الثالثة', 'structure_txt'), pu('la couche الأخيرة', 'externe'),
              rp('la couche الأخيرة', 'externe_txt')],
    centre=[ce('كنقولو saturée', 'couche pleine = saturée'), ce('K deux، L six', 'O : (K)²(L)⁶')],
    cahier='Définition : la couche externe est la dernière couche occupée ; une couche pleine est saturée.\nMéthode : 1) électrons = Z (− charge si ion) ; 2) remplir K, puis L, puis M ; 3) écrire (K)ᵃ(L)ᵇ(M)ᶜ ; 4) couche externe',
    figures=[{'type': 'schema', 'titre': 'O : (K)²(L)⁶', 'legende': 'K est saturée (2) ; la couche externe L porte 6 électrons.', 'cadre': {'l': 10, 'h': 6},
              'elements': [{'f': 'cercle', 'c': [5, 3], 'r': 0.4, 'remplir': 'rose', 'couleur': 'rose'},
                           {'f': 'cercle', 'c': [5, 3], 'r': 1.2, 'couleur': 'vert'}, {'f': 'cercle', 'c': [5, 3], 'r': 2.3, 'couleur': 'orange'},
                           {'f': 'texte', 't': 'K (2)', 'at': [6.1, 4.3], 'ancre': 'gauche', 'couleur': 'vert'},
                           {'f': 'texte', 't': 'L (6) : externe', 'at': [7.1, 5.4], 'ancre': 'gauche', 'couleur': 'orange'},
                           {'f': 'point', 'at': [5, 4.2]}, {'f': 'point', 'at': [5, 1.8]},
                           {'f': 'point', 'at': [5, 5.3]}, {'f': 'point', 'at': [5, 0.7]}, {'f': 'point', 'at': [2.7, 3]},
                           {'f': 'point', 'at': [7.3, 3]}, {'f': 'point', 'at': [3.4, 4.6]}, {'f': 'point', 'at': [6.6, 1.4]}]}],
    comps=['C7'])

D['at_c3_toi'] = diapo(
    'at_c3_toi', 'À toi : la structure électronique de ³⁵₁₇Cl', 'Même méthode : compter, remplir K, L, M, écrire.',
    ['Cl : Z = 17.'],
    'Exemple : Cl (Z = 17) : (K)²(L)⁸(M)⁷ ; couche externe M (7 électrons).', 'couches.html?vue=remplir&atome=Cl',
    'Les couches du chlore', 'Les dix-sept électrons attendent ; ils tombent après ta réponse',
    'À toi, avec l’atome de chlore. Z égale dix-sept. Voici ses électrons, qui attendent d’être placés. Fais les étapes '
    'dans ta tête : combien d’électrons, puis K, puis L, puis M. Ensuite choisis la bonne structure au tableau.',
    'دابا نتا، مع l’atome ديال le chlore. Z égale dix-sept. هادو هما les électrons ديالو، كيتسناو نحطوهم. دير les '
    'étapes فراسك: شحال من électron، من بعد K، من بعد L، من بعد M. ومن بعد ختار la structure الصحيحة فالسبورة.',
    demarrer='reset',
    pointage=[pu('هادو هما les électrons', 'compte'), rp('هادو هما les électrons', 'electrons')],
    apres=[{'sim_avant': {'conclusions': False},
            'etapes': [{'commande': 'set_parameters', 'parametres': {'conclusions': True}}, {'commande': 'play_until', 'parametres': {'moment': 'k'}},
                       {'commande': 'play_until', 'parametres': {'moment': 'l'}}, {'commande': 'play_until', 'parametres': {'moment': 'm'}},
                       {'commande': 'play_until', 'parametres': {'moment': 'externe'}}, {'repere': 'structure_txt'}], 'duree_s': 12}],
    cahier='Exemple : Cl (Z = 17) : (K)²(L)⁸(M)⁷ ; couche externe : M, 7 électrons.',
    comps=['C7'],
    q=question('qcm', 'La structure électronique de l’atome de chlore (Z = 17) est…', ['(K)²(L)⁸(M)⁷', '(K)²(L)⁷(M)⁸', '(K)⁸(L)⁸(M)¹'], 0,
               'شوف هاد السؤال: شنو هي la structure électronique ديال l’atome ديال le chlore، Z égale dix-sept؟',
               ('برافو! K deux، L huit، M sept. la couche externe هي M، فيها sept électrons.', 'Oui : (K)²(L)⁸(M)⁷ ; couche externe M, 7 électrons.'),
               {1: (('L كتاخد huit، ماشي sept. عمر L كاملة عاد دوز ل M.', 'L prend 8 électrons : remplis-la entièrement avant M.'),
                    ('K deux، L huit، والباقي sept ف M: K deux، L huit، M sept.', 'K : 2, L : 8, et les 7 restants dans M : (K)²(L)⁸(M)⁷.')),
                2: (('K كتاخد غير deux électrons على الأكثر.', 'K ne prend que 2 électrons au plus.'),
                    ('K deux، L huit، M sept: dix-sept électrons.', '(K)²(L)⁸(M)⁷ : 2 + 8 + 7 = 17.'))},
               demo=('les données: Z égale dix-sept، l’atome neutre، إذن dix-sept électrons. la couche K: deux، saturée. la couche L: huit، saturée. '
                     'la couche M: dix-sept moins dix، sept. la structure: K deux، L huit، M sept. la couche externe: M، sept électrons.',
                     [('Z = 17 → 17 électrons', 'les données', 'electrons'), ('K : 2 (saturée)', 'la couche K', 'k'), ('L : 8 (saturée)', 'la couche L', 'l'),
                      ('M : 17 − 10 = 7', 'la couche M', 'm'), ('(K)²(L)⁸(M)⁷', 'la structure', 'structure_txt'), ('couche externe : M (7 électrons)', 'la couche externe', 'externe_txt')])))

D['at_c4_ion'] = diapo(
    'at_c4_ion', 'La structure électronique d’un ion', 'Pour un ion, on compte d’abord ses électrons : Z − charge.',
    ['Na⁺ : 11 − 1 = 10 électrons → (K)²(L)⁸ : couche externe L saturée.'],
    'Ion : nombre d’électrons = Z − q (q : charge de l’ion) ; puis même méthode. Na⁺ : (K)²(L)⁸.', 'couches.html?vue=remplir&atome=Na&q=1',
    'Les couches de l’ion sodium', 'Dix électrons comptés ; deux dans K, huit dans L',
    'Et pour un ion ? La seule différence, c’est le nombre d’électrons. L’ion sodium Na plus : l’atome a onze électrons, '
    'il en a perdu un. Onze moins un, dix électrons. Comptons-les : un, deux, jusqu’à dix. On remplit : K deux, saturée. '
    'L huit, saturée aussi. La structure de Na plus : K deux, L huit. Sa couche externe, L, est saturée.',
    'و ل l’ion؟ الفرق الوحيد هو le nombre ديال les électrons. l’ion sodium Na plus: l’atome فيه onze électrons، خسر '
    'واحد. onze moins un، dix électrons. نحسبوهم: un، deux، حتى dix. كنعمرو: K deux، saturée. L huit، saturée حتى '
    'هي. la structure ديال Na plus: K deux، L huit. la couche externe ديالو، L، saturée.',
    demarrer='reset',
    pointage=[pu('onze moins un', 'compte'), rp('نحسبوهم', 'electrons'), pu('كنعمرو: K deux', 'k'), pu('L huit، saturée حتى', 'l'),
              pu('la structure ديال Na plus', 'structure'), rp('la structure ديال Na plus', 'structure_txt'), pu('la couche externe ديالو', 'externe')],
    centre=[ce('onze moins un', 'Na⁺ : 11 − 1 = 10 électrons'), ce('K deux، L huit.', 'Na⁺ : (K)²(L)⁸')],
    cahier='Exemple : Na⁺ : 11 − 1 = 10 électrons → (K)²(L)⁸ ; couche externe L saturée.',
    comps=['C7'],
    q=question('qcm', 'L’ion oxyde O²⁻ (Z = 8) a pour structure électronique…', ['(K)²(L)⁶', '(K)²(L)⁸', '(K)²(L)⁴'], 1,
               'شوف هاد السؤال: l’ion O deux moins، Z égale huit. شنو هي la structure électronique ديالو؟',
               ('برافو! ربح deux électrons: huit plus deux، dix. K deux، L huit.', 'Oui : 8 + 2 = 10 électrons : (K)²(L)⁸.'),
               {0: (('هادي ديال l’atome. l’ion O deux moins ربح deux électrons.', 'Ça, c’est l’atome O. L’ion O²⁻ a gagné 2 électrons.'),
                    ('huit plus deux، dix électrons: K deux، L huit.', '8 + 2 = 10 électrons : (K)²(L)⁸.')),
                2: (('لا، deux moins يعني ربح، ماشي خسر.', 'Non : 2− veut dire qu’il a gagné 2 électrons, pas perdu.'),
                    ('ربح deux électrons: dix électrons، K deux، L huit.', 'Il a gagné 2 électrons : 10 électrons, (K)²(L)⁸.'))},
               demo=('les données: Z égale huit، l’ion deux moins ربح deux électrons. le nombre d’électrons: huit plus deux، dix. '
                     'la couche K: deux. la couche L: dix moins deux، huit. la structure: K deux، L huit.',
                     [('Z = 8 ; O²⁻ a gagné 2 électrons', 'les données', None), ('électrons : 8 + 2 = 10', 'le nombre d’électrons', None),
                      ('K : 2', 'la couche K', None), ('L : 10 − 2 = 8', 'la couche L', None), ('O²⁻ : (K)²(L)⁸', 'la structure', None)])))

# ═════════════════════════════════ BILAN, CARTE, FERMETURE ═════════════════════════════════

D['at_b1_bilan'] = diapo(
    'at_b1_bilan', 'Ce qu’il faut retenir', 'La fiche du modèle de l’atome, bloc par bloc.',
    ['1 · Histoire : Dalton → Thomson → Rutherford (noyau + vide) → Bohr → nuage électronique.',
     '2 · Constituants : noyau (protons +e, neutrons 0) + électrons (−e) ; e = 1,6 × 10⁻¹⁹ C.',
     '3 · ᴬ_Z X : A nucléons, Z protons ; N = A − Z ; électrons = Z.',
     '4 · Masse : m ≈ A·m_p.', '5 · Dimensions : 10⁻¹⁰ m et 10⁻¹⁵ m ; rapport 10⁵ ; structure lacunaire.',
     '6 · Isotopes (même Z), ions (cation, anion), élément chimique (même Z, se conserve).',
     '7 · Couches K (2), L (8), M (8) ; couche externe.'],
    'Fiche : histoire du modèle ; constituants ; A, Z, N ; m ≈ A·m_p ; 10⁻¹⁰ m et 10⁻¹⁵ m ; isotopes, ions, élément ; couches K, L, M.',
    'bilan.html?vue=fiche', 'Ce qu’il faut retenir', 'La fiche à la craie : sept blocs, définition, relation, piège',
    'Voici ce qu’il faut retenir. Un : l’histoire du modèle, de Dalton au nuage électronique ; Rutherford a montré que '
    'l’atome est surtout du vide. Deux : un noyau de protons et de neutrons, entouré d’électrons. Trois : A, le nombre de '
    'nucléons, Z, le nombre de protons, et N égale A moins Z. Quatre : la masse, m environ égale A fois m p. Cinq : dix '
    'puissance moins dix mètre pour l’atome, dix puissance moins quinze pour le noyau. Six : isotopes, ions et élément '
    'chimique, tout se joue sur Z. Sept : les couches K, L, M, qu’on remplit dans l’ordre.',
    'هادشي اللي خاصك تحفظ. un: القصة ديال le modèle، من Dalton حتى le nuage électronique؛ Rutherford بين بلي l’atome '
    'فيه غير الخوا تقريبا. deux: noyau فيه les protons و les neutrons، داير بيه les électrons. trois: A، le nombre de '
    'nucléons، Z، le nombre de protons، و N égale A moins Z. quatre: la masse، m environ égale A fois m p. cinq: dix '
    'puissance moins dix mètre ل l’atome، dix puissance moins quinze ل le noyau. six: les isotopes، les ions و l’élément '
    'chimique، كلشي على حساب Z. sept: les couches K، L، M، اللي كنعمروهم بالترتيب.',
    pointage=[pu('un: القصة', 'histoire'), pu('deux: noyau', 'constituants'), pu('trois: A', 'ecriture'), pu('quatre: la masse', 'masse'),
              pu('cinq: dix', 'dimensions'), pu('six: les isotopes', 'element'), pu('sept: les couches', 'couches')],
    cahier='Fiche : N = A − Z ; électrons = Z ; m ≈ A·m_p ; r_atome/r_noyau = 10⁵ ; (K)²(L)⁸(M)…',
    typ='synthesis')
D['at_b1_bilan']['concentration']['acquis'] = True

D['at_b2_carte'] = diapo(
    'at_b2_carte', 'La carte du chapitre', 'Sept branches autour de l’atome.',
    ['Histoire · Constituants · Écriture du noyau · Masse · Dimensions · Isotopes, ions, élément · Couches K, L, M.'],
    'Carte : l’atome → histoire, constituants, A Z N, masse, dimensions, élément chimique, couches.',
    'bilan.html?vue=carte', 'La carte du chapitre', 'L’atome au centre, sept branches',
    'Et voici la carte du chapitre. Au centre, l’atome. Première branche : l’histoire du modèle. Puis les constituants. '
    'Puis l’écriture du noyau. Puis la masse. Puis les dimensions. Puis les isotopes, les ions et l’élément chimique. '
    'Et enfin, les couches électroniques. Touche une branche pour relire sa phrase.',
    'وهادي هي la carte ديال الدرس. فالوسط، l’atome. الفرع اللول: القصة ديال le modèle. من بعد les constituants. من '
    'بعد l’écriture ديال le noyau. من بعد la masse. من بعد les dimensions. من بعد les isotopes، les ions و l’élément '
    'chimique. وفالأخير، les couches électroniques. ضغط على شي فرع باش تعاود تقرا الجملة ديالو.',
    pointage=[rp('فالوسط، l’atome', 'centre'), pu('الفرع اللول', 'histoire'), pu('من بعد les constituants', 'constituants'),
              pu('من بعد l’écriture', 'ecriture'), pu('من بعد la masse', 'masse'), pu('من بعد les dimensions', 'dimensions'),
              pu('من بعد les isotopes', 'element'), pu('وفالأخير، les couches', 'couches')],
    cahier='Carte : histoire → constituants → A, Z, N → masse → dimensions → isotopes, ions, élément → couches K, L, M.',
    typ='synthesis')
D['at_b2_carte']['concentration']['acquis'] = True

D['at_fermeture_cours'] = diapo(
    'at_fermeture_cours', 'Ce qu’il faut retenir, et comment réviser', 'Trois idées à retenir, et comment réviser.',
    ['Retenir : N = A − Z · électrons = Z · m ≈ A·m_p', 'Réviser : relire le cahier, refaire les méthodes seul',
     'Rédiger : relation → application → résultat et unité', 'Jour J : gérer son temps · bien dormir la veille'],
    'Pour réviser : relire le cahier ; refaire seul les méthodes (tableau des particules, masse, structure électronique) ; rédiger relation, application, résultat avec unité ; le jour du contrôle, partager son temps ; la veille, bien dormir.',
    None, '', '',
    'Nous arrivons à la fin du cours : Modèle de l’atome. Que faut-il retenir ? Trois idées. Première : le noyau ᴬ Z X '
    'contient Z protons et N égale A moins Z neutrons, et l’atome neutre a Z électrons. Deuxième : la masse de l’atome '
    'est dans son noyau, m environ égale A fois m p. Troisième : les électrons remplissent K, puis L, puis M. Maintenant, '
    'quelques conseils pour réviser. Relis ton cahier, et refais seul les trois méthodes. Dans un calcul, écris la '
    'relation, puis l’application numérique, puis le résultat avec son unité, car chaque étape a ses points. Le jour du '
    'contrôle, partage ton temps, et commence par la question qui te paraît facile. La veille, dors bien. Écris ces '
    'conseils dans ton cahier. Tu as bien travaillé, bon courage !',
    'وصلنا للخر ديال الدرس: Modèle de l’atome. شنو خاصك تحفظ؟ ثلاثة ديال الأفكار. اللولة: le noyau فيه Z protons و N '
    'égale A moins Z neutrons، و l’atome neutre فيه Z électrons. الثانية: la masse ديال l’atome كاينة ف le noyau، m '
    'environ égale A fois m p. الثالثة: les électrons كيعمرو K، من بعد L، من بعد M. دابا، كيفاش تراجع؟ عاود قرا الدفتر '
    'ديالك، وعاود دير les trois méthodes بوحدك. فالحساب، كتب la relation، من بعد l’application numérique، من بعد le '
    'résultat مع l’unité ديالو، حيت كل وحدة عندها النقطة ديالها. ونهار الفرض، قسم الوقت ديالك، وبدا بالسؤال اللي ساهل '
    'عليك. وقبل الفرض، ترتاح مزيان فالليل. كتب هادشي ف الدفتر ديالك. راك خدمتي مزيان، الله يعاونك!',
    centre=[ce('ثلاثة ديال الأفكار', 'Retenir : N = A − Z · électrons = Z · m ≈ A·m_p'), ce('عاود قرا', 'Réviser : relire le cahier, refaire les méthodes seul'),
            ce('فالحساب', 'Rédiger : relation → application → résultat et unité'), ce('نهار الفرض', 'Jour J : gérer son temps · bien dormir la veille')],
    typ='synthesis', extra={'fermeture_cours': True})
D['at_fermeture_cours']['speech_text']['fr'] = D['at_fermeture_cours']['speech_text']['fr'].replace('le noyau ᴬ Z X contient', 'le noyau contient')

# ═════════════════════════════════ COMPÉTENCES, SÉANCES, ASSEMBLAGE ═════════════════════════════════

def R(id, typ, prompt, dit, attendu=None, options=None, correct=None):
    r = {'id': id, 'type': typ, 'prompt': prompt, 'enonce_dit': dit}
    if attendu is not None:
        r['attendu'] = attendu
    if options is not None:
        r['options'] = options
    if correct is not None:
        r['correct'] = correct
    return r


COMPETENCES = [
    ('C0', 'Utiliser la charge électrique et les puissances de dix', 'utiliser les charges et les puissances de dix',
     ['at_p2_charges', 'at_p3_ballon', 'at_p4_puissances', 'at_p5_calculs'],
     [R('C0_r1', 'libre', 'Que font deux charges de même signe ? et de signes contraires ?', 'شوف هاد السؤال: شنو كيديرو deux charges عندهم même signe؟ و signes contraires؟', 'Même signe : elles se repoussent ; signes contraires : elles s’attirent.'),
      R('C0_r2', 'qcm', '10² × 10⁴ = …', 'شوف هاد السؤال: dix puissance deux fois dix puissance quatre، شحال؟', options=['10⁸', '10⁶', '10²'], correct=1),
      R('C0_r3', 'vrai_faux', 'Un corps qui gagne des électrons devient chargé positivement.', 'شوف هاد الجملة: الجسم اللي كيربح des électrons كيولي chargé positivement. vrai ou faux؟', correct=False)]),
    ('C1', 'Décrire l’évolution du modèle de l’atome (Dalton, Thomson, Rutherford, Bohr, nuage électronique)', 'décrire l’histoire du modèle de l’atome',
     ['at_o1_situation', 'at_p1_modele', 'at_h1_elements', 'at_h2_dalton', 'at_h3_thomson', 'at_h4_montage', 'at_h5_resultats', 'at_h6_interpretation', 'at_h7_bohr', 'at_h8_nuage'],
     [R('C1_r1', 'libre', 'Quelle conclusion Rutherford a-t-il tirée de son expérience ?', 'شوف هاد السؤال: شنو استنتج Rutherford من التجربة ديالو؟', 'L’atome est surtout du vide ; au centre, un noyau très petit, chargé positivement.'),
      R('C1_r2', 'qcm', 'Le modèle du « pain aux raisins » est celui de…', 'شوف هاد السؤال: le modèle ديال le pain aux raisins، ديال شكون؟', options=['Dalton', 'Thomson', 'Bohr'], correct=1),
      R('C1_r3', 'vrai_faux', 'Dans l’expérience de Rutherford, la plupart des particules α rebondissent sur la feuille d’or.', 'شوف هاد الجملة: ف التجربة ديال Rutherford، تقريبا كاع les particules alpha كيرجعو من la feuille d’or. vrai ou faux؟', correct=False)]),
    ('C2', 'Connaître les constituants de l’atome, leur charge et leur masse', 'connaître les constituants de l’atome',
     ['at_s1_atome', 'at_s2_electron', 'at_s3_noyau'],
     [R('C2_r1', 'libre', 'De quoi est formé un atome ?', 'شوف هاد السؤال: من شنو مصنوع l’atome؟', 'D’un noyau (protons et neutrons) chargé positivement, entouré d’un nuage d’électrons chargés négativement.'),
      R('C2_r2', 'qcm', 'La charge d’un proton est…', 'شوف هاد السؤال: شنو هي la charge ديال le proton؟', options=['−e', '0', '+e'], correct=2),
      R('C2_r3', 'vrai_faux', 'Le neutron est chargé négativement.', 'شوف هاد الجملة: le neutron chargé négativement. vrai ou faux؟', correct=False)]),
    ('C3', 'Exploiter l’écriture ᴬ_Z X : déterminer Z, A, N et le nombre d’électrons', 'exploiter l’écriture du noyau',
     ['at_s4_notation', 'at_s5_neutralite', 'at_s6_methode', 'at_s7_toi'],
     [R('C3_r1', 'libre', 'Pour ²³₁₁Na, donne le nombre de protons, de neutrons et d’électrons.', 'شوف هاد السؤال: ل le sodium vingt-trois onze، عطيني le nombre ديال les protons، les neutrons و les électrons.', '11 protons ; N = 23 − 11 = 12 neutrons ; 11 électrons (atome neutre).'),
      R('C3_r2', 'qcm', 'Dans ᴬ_Z X, Z est…', 'شوف هاد السؤال: ف l’écriture A Z X، شنو هو Z؟', options=['le nombre de nucléons', 'le nombre de protons', 'le nombre de neutrons'], correct=1),
      R('C3_r3', 'vrai_faux', 'Un atome neutre a autant d’électrons que de neutrons.', 'شوف هاد الجملة: l’atome neutre فيه نفس العدد ديال les électrons و les neutrons. vrai ou faux؟', correct=False)]),
    ('C4', 'Calculer la masse approchée d’un atome : m ≈ A·m_p', 'calculer la masse d’un atome',
     ['at_m1_masse', 'at_m2_methode', 'at_m3_toi'],
     [R('C4_r1', 'libre', 'Pourquoi peut-on écrire m ≈ A·m_p ?', 'شوف هاد السؤال: علاش نقدرو نكتبو m environ égale A fois m p؟', 'Parce que la masse des électrons est négligeable devant celle des nucléons, et que m_p ≈ m_n.'),
      R('C4_r2', 'qcm', 'Masse approchée de ⁴₂He (m_p ≈ 1,67 × 10⁻²⁷ kg) :', 'شوف هاد السؤال: شحال تقريبا la masse ديال l’hélium quatre deux؟', options=['6,68 × 10⁻²⁷ kg', '3,34 × 10⁻²⁷ kg', '6,68 × 10⁻²⁶ kg'], correct=0),
      R('C4_r3', 'vrai_faux', 'La masse d’un atome est surtout celle de ses électrons.', 'شوف هاد الجملة: la masse ديال l’atome هي بالخصوص la masse ديال les électrons. vrai ou faux؟', correct=False)]),
    ('C5', 'Comparer les dimensions de l’atome et du noyau', 'comparer la taille de l’atome et du noyau',
     ['at_d1_rapport', 'at_d2_stade'],
     [R('C5_r1', 'libre', 'Donne l’ordre de grandeur du rayon d’un atome et de celui d’un noyau.', 'شوف هاد السؤال: عطيني تقريبا le rayon ديال l’atome و le rayon ديال le noyau.', 'Atome : environ 10⁻¹⁰ m ; noyau : environ 10⁻¹⁵ m.'),
      R('C5_r2', 'qcm', 'Le noyau est environ … fois plus petit que l’atome.', 'شوف هاد السؤال: le noyau صغير من l’atome بشحال تقريبا؟', options=['10', '10⁵', '10¹⁰'], correct=1),
      R('C5_r3', 'vrai_faux', 'L’atome a une structure lacunaire : il est surtout fait de vide.', 'شوف هاد الجملة: l’atome عندو structure lacunaire، فيه غير الخوا تقريبا. vrai ou faux؟', correct=True)]),
    ('C6', 'Définir les isotopes, les ions monoatomiques et l’élément chimique', 'définir isotopes, ions et élément chimique',
     ['at_e1_isotopes', 'at_e2_ions', 'at_e3_element', 'at_e4_conservation'],
     [R('C6_r1', 'libre', 'Qu’est-ce qu’un élément chimique ?', 'شوف هاد السؤال: شنو هو l’élément chimique؟', 'L’ensemble des entités (atomes, ions) qui ont le même numéro atomique Z ; il se conserve au cours d’une transformation chimique.'),
      R('C6_r2', 'qcm', 'Un anion est un atome qui…', 'شوف هاد السؤال: l’anion، هو atome اللي…', options=['a perdu des électrons', 'a gagné des électrons', 'a gagné des protons'], correct=1),
      R('C6_r3', 'vrai_faux', '¹²₆C et ¹⁴₆C sont des isotopes.', 'شوف هاد الجملة: carbone douze و carbone quatorze هما des isotopes. vrai ou faux؟', correct=True)]),
    ('C7', 'Établir la structure électronique d’un atome ou d’un ion (Z ≤ 18)', 'établir la structure électronique',
     ['at_c1_couches', 'at_c2_methode', 'at_c3_toi', 'at_c4_ion'],
     [R('C7_r1', 'libre', 'Donne la structure électronique de l’atome d’azote (Z = 7) et sa couche externe.', 'شوف هاد السؤال: عطيني la structure électronique ديال l’azote، Z égale sept، و la couche externe ديالو.', '(K)²(L)⁵ ; couche externe : L, 5 électrons.'),
      R('C7_r2', 'qcm', 'La couche L peut contenir au plus…', 'شوف هاد السؤال: la couche L، شحال كتاخد على الأكثر؟', options=['2 électrons', '8 électrons', '18 électrons'], correct=1),
      R('C7_r3', 'vrai_faux', 'On remplit la couche L avant la couche K.', 'شوف هاد الجملة: كنعمرو la couche L قبل la couche K. vrai ou faux؟', correct=False)]),
]


def B(id, titre, slides, cahier, retrouver, exercice, figures=None):
    b = {'id': id, 'titre': titre, 'slide_ids': slides, 'cahier': [{'texte': t} for t in cahier], 'retrouver': retrouver, 'exercice': exercice}
    if figures:
        b['cahier_figures'] = figures
    return b


def RT(prompt, attendu, comp):
    return {'prompt': prompt, 'attendu': attendu, 'competence_id': comp}


def EX(prompt, options, correct):
    return {'type': 'qcm', 'prompt': prompt, 'options': options, 'correct': correct}


SEANCES = [
    {'id': 'at_se1', 'titre': 'Séance 1 — Le point de départ : matière, charge, puissances de dix', 'blocs': [
        B('at_bl1', 'La matière et le modèle', ['at_ouverture_cours', 'at_o1_situation', 'at_p1_modele'],
          ['On apprend : l’atome, son noyau, ses électrons.', 'Toute la matière est faite d’atomes liés les uns aux autres.',
           'Définition : un modèle est une représentation simplifiée de la réalité ; il change avec les expériences.'],
          RT('Cahier fermé : qu’est-ce qu’un modèle ?', 'Une représentation simplifiée de la réalité, qu’on change quand une expérience ne colle plus.', 'C1'),
          EX('Un globe terrestre est…', ['la Terre réelle', 'un modèle de la Terre', 'un atome'], 1)),
        B('at_bl2', 'La charge électrique', ['at_p2_charges', 'at_p3_ballon'],
          ['Rappel : la charge électrique', '| Charges | Effet |', '| même signe | se repoussent |', '| signes contraires | s’attirent |',
           'Un corps neutre a autant de charges + que de charges − ; gagner des électrons le rend négatif, en perdre le rend positif.'],
          RT('Cahier fermé : quand un corps est-il neutre ?', 'Quand il a autant de charges + que de charges −.', 'C0'),
          EX('Deux charges négatives…', ['s’attirent', 'se repoussent', 'ne font rien'], 1)),
        B('at_bl3', 'Les puissances de dix', ['at_p4_puissances', 'at_p5_calculs'],
          ['Rappel : les puissances de dix', '| 10⁻¹ m | 10⁻² m | 10⁻³ m |', '| 0,1 m | 1 cm | 1 mm |',
           'Formule : 10ᵃ × 10ᵇ = 10ᵃ⁺ᵇ ; 10ᵃ/10ᵇ = 10ᵃ⁻ᵇ',
           'Remarque : en écriture scientifique, un seul chiffre (non nul) avant la virgule : 20 × 10⁻²⁷ = 2 × 10⁻²⁶.'],
          RT('Cahier fermé : comment calcule-t-on 10ᵃ/10ᵇ ?', '10ᵃ/10ᵇ = 10ᵃ⁻ᵇ : on retranche les exposants.', 'C0'),
          EX('10³ × 10⁻⁵ = …', ['10⁻²', '10⁸', '10⁻¹⁵'], 0)),
    ]},
    {'id': 'at_se2', 'titre': 'Séance 2 — L’histoire du modèle de l’atome', 'blocs': [
        B('at_bl4', 'Des quatre éléments à Thomson', ['at_h1_elements', 'at_h2_dalton', 'at_h3_thomson'],
          ['I. Histoire du modèle de l’atome', '1. Les premiers modèles', '| Qui | Modèle |', '| Les Grecs | quatre éléments : terre, eau, feu, air |',
           '| Dalton | sphères pleines ; plusieurs sortes d’atomes |', '| Thomson (1897) | découvre l’électron (−) ; « pain aux raisins » |'],
          RT('Cahier fermé : décris le modèle de Thomson.', 'Une boule de matière positive avec des électrons négatifs dedans (pain aux raisins).', 'C1'),
          EX('Qui a découvert l’électron ?', ['Dalton', 'Thomson', 'Bohr'], 1)),
        B('at_bl5', 'L’expérience de Rutherford', ['at_h4_montage', 'at_h5_resultats', 'at_h6_interpretation'],
          ['2. L’expérience de Rutherford', 'Des particules α (+) sont envoyées sur une feuille d’or très mince.',
           '| Observation | Interprétation |', '| la plupart passent tout droit | l’atome est surtout du vide |',
           '| quelques-unes déviées | + et + se repoussent près du noyau |', 'Donc l’atome : un noyau très petit, chargé +, entouré de vide.'],
          RT('Cahier fermé : quelle est la conclusion de Rutherford ?', 'L’atome est surtout du vide ; au centre, un noyau très petit chargé positivement.', 'C1'),
          EX('Les particules α utilisées par Rutherford sont…', ['chargées +', 'chargées −', 'neutres'], 0)),
        B('at_bl6', 'Bohr et le nuage électronique', ['at_h7_bohr', 'at_h8_nuage'],
          ['3. Le modèle actuel', 'Bohr (1913) : les électrons tournent sur des orbites de rayon défini.',
           'Aujourd’hui : un noyau entouré d’un nuage électronique ; la position exacte d’un électron ne peut pas être connue.'],
          RT('Cahier fermé : qu’est-ce que le nuage électronique ?', 'La région autour du noyau où se trouvent les électrons, sans position exacte.', 'C1'),
          EX('Dans le modèle de Bohr, les électrons…', ['sont dans une matière positive', 'tournent sur des orbites', 'sont dans le noyau'], 1)),
    ]},
    {'id': 'at_se3', 'titre': 'Séance 3 — Les constituants et l’écriture du noyau', 'blocs': [
        B('at_bl7', 'Électrons, protons, neutrons', ['at_s1_atome', 'at_s2_electron', 'at_s3_noyau'],
          ['II. Les constituants de l’atome', 'Définition : l’atome est formé d’un noyau chargé +, entouré d’un nuage d’électrons chargés −.',
           '| Particule | Charge | Masse (kg) |', '| électron | −e | 9,1 × 10⁻³¹ |', '| proton | +e | 1,673 × 10⁻²⁷ |', '| neutron | 0 | 1,675 × 10⁻²⁷ |',
           'Formule : e = 1,6 × 10⁻¹⁹ C (charge élémentaire) ; nucléons = protons + neutrons'],
          RT('Cahier fermé : donne la charge de l’électron, du proton et du neutron.', 'Électron : −e ; proton : +e ; neutron : 0.', 'C2'),
          EX('Les nucléons sont…', ['les protons et les électrons', 'les protons et les neutrons', 'les électrons seuls'], 1)),
        B('at_bl8', 'L’écriture ᴬ_Z X et la méthode du tableau', ['at_s4_notation', 'at_s5_neutralite', 'at_s6_methode', 'at_s7_toi'],
          ['1. L’écriture du noyau', 'Définition : noyau ᴬ_Z X : A = nombre de nucléons (nombre de masse) ; Z = nombre de protons (numéro atomique).',
           'Formule : N = A − Z', 'L’atome est neutre : nombre d’électrons = Z.',
           'Méthode : 1) protons = Z, charge +Z·e ; 2) neutrons N = A − Z, charge 0 ; 3) électrons = Z, charge −Z·e'],
          RT('Cahier fermé : comment trouve-t-on le nombre de neutrons ?', 'N = A − Z.', 'C3'),
          EX('Pour ²⁷₁₃Al, le nombre de neutrons est…', ['13', '14', '27'], 1),
          figures=None),
    ]},
    {'id': 'at_se4', 'titre': 'Séance 4 — La masse et les dimensions de l’atome', 'blocs': [
        B('at_bl9', 'La masse de l’atome', ['at_m1_masse', 'at_m2_methode', 'at_m3_toi'],
          ['III. La masse et les dimensions de l’atome', 'Formule : m = Z·m_p + N·m_n + Z·m_e',
           'm_e est environ 1 840 fois plus petite que m_p (on néglige les électrons) et m_p ≈ m_n.',
           'Formule : m ≈ A·m_p, avec m_p ≈ 1,67 × 10⁻²⁷ kg',
           'Méthode : 1) lire A ; 2) m ≈ A·m_p ; 3) remplacer ; 4) résultat en kg, un chiffre avant la virgule'],
          RT('Cahier fermé : écris la masse approchée d’un atome.', 'm ≈ A·m_p.', 'C4'),
          EX('Masse approchée de ¹⁴₇N (m_p ≈ 1,67 × 10⁻²⁷ kg) :', ['2,34 × 10⁻²⁶ kg', '1,17 × 10⁻²⁶ kg', '2,34 × 10⁻²⁷ kg'], 0)),
        B('at_bl10', 'Les dimensions de l’atome', ['at_d1_rapport', 'at_d2_stade'],
          ['| Rayon de l’atome | Rayon du noyau |', '| ≈ 10⁻¹⁰ m | ≈ 10⁻¹⁵ m |', 'Formule : r_atome/r_noyau = 10⁵',
           'Donc l’atome est surtout du vide : structure lacunaire (noyau = bille de 1 mm au centre d’un stade de 100 m).'],
          RT('Cahier fermé : que veut dire « structure lacunaire » ?', 'L’atome est surtout du vide : le noyau est 10⁵ fois plus petit que l’atome.', 'C5'),
          EX('Le rayon d’un noyau est de l’ordre de…', ['10⁻¹⁰ m', '10⁻¹⁵ m', '10⁻⁵ m'], 1)),
    ]},
    {'id': 'at_se5', 'titre': 'Séance 5 — Isotopes, ions et élément chimique', 'blocs': [
        B('at_bl11', 'Isotopes et ions', ['at_e1_isotopes', 'at_e2_ions'],
          ['IV. L’élément chimique', 'Définition : des isotopes sont des atomes de même Z mais de A différents (ex. ¹²₆C, ¹³₆C, ¹⁴₆C).',
           'Définition : un ion monoatomique est un atome qui a perdu ou gagné des électrons.', '| Cation | Anion |',
           '| a perdu des électrons : ion + (Na⁺) | a gagné des électrons : ion − (Cl⁻) |'],
          RT('Cahier fermé : qu’est-ce qu’un cation ?', 'Un atome qui a perdu un ou plusieurs électrons : un ion positif.', 'C6'),
          EX('Mg²⁺ (Z = 12) a…', ['12 électrons', '10 électrons', '14 électrons'], 1)),
        B('at_bl12', 'L’élément chimique et sa conservation', ['at_e3_element', 'at_e4_conservation'],
          ['Définition : un élément chimique est l’ensemble des entités (atomes, ions) de même Z.',
           'Exemple : Cu²⁺(aq) + 2HO⁻(aq) → Cu(OH)₂(s) (précipité bleu).', 'Donc un élément chimique se conserve au cours d’une transformation chimique.'],
          RT('Cahier fermé : qu’est-ce qu’un élément chimique ?', 'L’ensemble des entités qui ont le même Z ; il se conserve.', 'C6'),
          EX('Ce qui caractérise un élément chimique, c’est…', ['son nombre de neutrons', 'son numéro atomique Z', 'sa charge'], 1)),
    ]},
    {'id': 'at_se6', 'titre': 'Séance 6 — La répartition électronique, bilan', 'blocs': [
        B('at_bl13', 'Les couches K, L, M', ['at_c1_couches', 'at_c2_methode', 'at_c3_toi'],
          ['V. La répartition électronique', '| Couche | K | L | M |', '| Électrons au plus | 2 | 8 | 8 |',
           'Règle 1 : une couche contient un nombre limité d’électrons. Règle 2 : on remplit K, puis L, puis M.',
           'Définition : la couche externe est la dernière couche occupée ; une couche pleine est saturée.',
           'Méthode : 1) électrons = Z ; 2) remplir K, puis L, puis M ; 3) écrire (K)ᵃ(L)ᵇ(M)ᶜ ; 4) couche externe'],
          RT('Cahier fermé : donne les deux règles de remplissage.', 'Une couche contient un nombre limité d’électrons (K : 2, L : 8, M : 8) ; on remplit K, puis L, puis M.', 'C7'),
          EX('Structure électronique de l’atome de sodium (Z = 11) :', ['(K)²(L)⁹', '(K)²(L)⁸(M)¹', '(K)¹(L)⁸(M)²'], 1),
          figures=[D['at_c2_methode']['concentration']['cahier_figures'][0]]),
        B('at_bl14', 'Les ions, et ce qu’il faut retenir', ['at_c4_ion', 'at_b1_bilan', 'at_b2_carte'],
          ['Méthode : pour un ion, électrons = Z − charge (Na⁺ : 10 électrons → (K)²(L)⁸).',
           'Fiche : N = A − Z ; électrons = Z ; m ≈ A·m_p ; r_atome/r_noyau = 10⁵ ; isotopes : même Z ; élément : même Z.'],
          RT('Cahier fermé : combien d’électrons a l’ion Cl⁻ (Z = 17) ?', '17 + 1 = 18 électrons.', 'C7'),
          EX('L’ion Mg²⁺ (Z = 12) a pour structure…', ['(K)²(L)⁸', '(K)²(L)⁸(M)²', '(K)²(L)¹⁰'], 0)),
        B('at_bloc_fin_cours', 'Fin du cours : retenir et réviser', ['at_fermeture_cours'],
          ['Pour réviser : relire le cahier ; refaire seul les méthodes (tableau des particules, masse, structure électronique).',
           'Rédiger : relation → application numérique → résultat avec son unité.', 'Le jour du contrôle : partager son temps ; la veille, bien dormir.'],
          RT('Cahier fermé : quelles sont les trois méthodes du chapitre ?', 'Le tableau des particules (Z, N = A − Z, électrons) ; la masse m ≈ A·m_p ; la structure électronique (K, L, M).', 'C7'),
          EX('Dans un calcul, on écrit d’abord…', ['le résultat', 'la relation', 'l’unité'], 1)),
    ]},
]
# la figure de la notation dans le bloc 8
SEANCES[2]['blocs'][1]['cahier_figures'] = [D['at_s4_notation']['concentration']['cahier_figures'][0]]
SEANCES[4]['blocs'][0]['cahier_figures'] = [D['at_e2_ions']['concentration']['cahier_figures'][0]]

ORDRE = [sid for se in SEANCES for b in se['blocs'] for sid in b['slide_ids']]
ACTIVITES = [
    ('at_a0', 'Point de départ : la matière, la charge, les puissances de dix', 'ouverture', 25, ['at_ouverture_cours', 'at_o1_situation', 'at_p1_modele', 'at_p2_charges', 'at_p3_ballon', 'at_p4_puissances', 'at_p5_calculs']),
    ('at_a1', 'L’histoire du modèle de l’atome', 'decouverte', 25, ['at_h1_elements', 'at_h2_dalton', 'at_h3_thomson', 'at_h4_montage', 'at_h5_resultats', 'at_h6_interpretation', 'at_h7_bohr', 'at_h8_nuage']),
    ('at_a2', 'Les constituants et l’écriture du noyau', 'apprentissage', 25, ['at_s1_atome', 'at_s2_electron', 'at_s3_noyau', 'at_s4_notation', 'at_s5_neutralite', 'at_s6_methode', 'at_s7_toi']),
    ('at_a3', 'La masse et les dimensions', 'apprentissage', 20, ['at_m1_masse', 'at_m2_methode', 'at_m3_toi', 'at_d1_rapport', 'at_d2_stade']),
    ('at_a4', 'Isotopes, ions et élément chimique', 'apprentissage', 20, ['at_e1_isotopes', 'at_e2_ions', 'at_e3_element', 'at_e4_conservation']),
    ('at_a5', 'La répartition électronique', 'apprentissage', 20, ['at_c1_couches', 'at_c2_methode', 'at_c3_toi', 'at_c4_ion']),
    ('at_a6', 'Bilan', 'bilan', 10, ['at_b1_bilan', 'at_b2_carte', 'at_fermeture_cours']),
]


def assembler():
    acts = []
    for i, (aid, titre, phase, mn, ids) in enumerate(ACTIVITES):
        slides = []
        for k, sid in enumerate(ids):
            s = D[sid]
            s['order_index'] = k
            slides.append(s)
        acts.append({'id': aid, 'title': titre, 'phase': phase, 'duration_minutes': mn, 'order_index': i, 'slides': slides})
    assert [s['id'] for a in acts for s in a['slides']] == ORDRE, 'ordre des activités ≠ ordre des blocs'
    assert set(ORDRE) == set(D), set(D) ^ set(ORDRE)
    comps = []
    for cid, label, dit, ids, rappels in COMPETENCES:
        comps.append({'id': cid, 'label': label, 'dit': dit, 'slide_ids': ids, 'rappels': rappels})
        for sid in ids:
            assert cid in D[sid]['competence_ids'], (cid, sid)
    return {
        'id': 'tc_chim_atome', 'stable_id': 'tc_chim_atome', 'lesson_id': 'tc_chim_atome', 'title': 'Modèle de l’atome', 'version': 1,
        'status': 'draft', 'language': 'mixed', 'estimated_minutes': 145, 'mode': 'concentration', 'niveau': 'tronc_commun_sciences_biof',
        'subject': 'chimie', 'lesson_match': [], 'catalog': {},
        'note': 'Cours /TCF écrit en mode concentration d’après le livre « Cours physique-chimie TCSF » (résumé : docs/tcf/CONTENU_LIVRE.md). '
                'Pas encore de voix : les textes à dire sont listés dans tc_chim_atome_voix.json. Construit par scripts/tcf/construire_tc_chim_atome.py.',
        'activities': acts, 'competences': comps, 'seances': SEANCES}


# ═════════════════════════════════ CONTRÔLES ═════════════════════════════════

INTERDIT = re.compile(r'[0-9=+×÷/<>≈²³⁰¹⁴-⁹₀-₉αβΔ%]')


def parles(cours):
    for a in cours['activities']:
        for s in a['slides']:
            yield s['id'], s['speech_text']['mixed']
            q = s.get('question') or {}
            if q:
                yield s['id'] + '/q', q['enonce_dit']
                if q.get('demonstration'):
                    yield s['id'] + '/demo', q['demonstration']['parole']
            for cle, ops in s['concentration'].get('reponses', {}).items():
                for o, ks in ops.items():
                    for k, r in ks.items():
                        yield f"{s['id']}/{cle}/{o}/{k}", r['parole']
            o = s['concentration'].get('observation')
            if o:
                yield s['id'] + '/obs', o['enonce_dit']
                for i in o['indices']:
                    yield s['id'] + '/obs_i', i['dit']
                for r in o['retours']:
                    yield s['id'] + '/obs_r', r['parole']
                yield s['id'] + '/obs_s', o['solution']['parole']
    for c in cours['competences']:
        for r in c['rappels']:
            yield r['id'], r['enonce_dit']


def controler(cours):
    err = []
    for lieu, t in parles(cours):
        if INTERDIT.search(t):
            err.append(f'{lieu} : chiffre ou symbole dit : {INTERDIT.findall(t)}')
        if 'السخانة' in t:
            err.append(f'{lieu} : السخانة')
    for a in cours['activities']:
        for s in a['slides']:
            mx, c = s['speech_text']['mixed'], s['concentration']
            pos = 0
            for p in c.get('pointage', []):
                i = mx.find(p['mot'])
                if i < 0:
                    err.append(f"{s['id']} : mot absent « {p['mot']} »")
                elif i < pos:
                    err.append(f"{s['id']} : mot hors d’ordre « {p['mot']} »")
                else:
                    pos = i
            for k in c.get('centre', []):
                if k['mot'] not in mx:
                    err.append(f"{s['id']} : mot du centre absent « {k['mot']} »")
            o = c.get('observation')
            if o and mx.count(o['apres_mot']) != 1:
                err.append(f"{s['id']} : apres_mot « {o['apres_mot']} » trouvé {mx.count(o['apres_mot'])} fois")
            q = s.get('question') or {}
            d = q.get('demonstration')
            if d:
                for l in d['lignes']:
                    if l['mot'] not in d['parole']:
                        err.append(f"{s['id']} : mot de démonstration absent « {l['mot']} »")
            if q:
                n = len(q['options'])
                rep = c['reponses']['q']
                for i in range(n):
                    attendu = {'juste'} if i == q['correct'] else {'1', '2'}
                    if set(rep.get(str(i), {})) != attendu:
                        err.append(f"{s['id']} : réactions de l’option {i} : {sorted(rep.get(str(i), {}))}")
    return err


if __name__ == '__main__':
    cours = assembler()
    err = controler(cours)
    for e in err:
        print('ERREUR', e)
    with open(SORTIE, 'w', encoding='utf-8') as f:
        json.dump(cours, f, ensure_ascii=False, indent=2)
        f.write('\n')
    n = sum(len(a['slides']) for a in cours['activities'])
    nq = sum(1 for a in cours['activities'] for s in a['slides'] if s.get('question'))
    print(SORTIE, n, 'diapos', sum(len(se['blocs']) for se in cours['seances']), 'blocs', len(cours['competences']), 'compétences', nq, 'questions', len(err), 'erreurs')
