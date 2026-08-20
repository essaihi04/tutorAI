"""Les termes scientifiques arabes que la voix ne sait pas dire.

Le réflexe devant un mot mal prononcé est d'ajouter le tachkil. Ici il
AGGRAVE : le modèle Academy (`oddadmix/lahgtna-chatterbox-v1`) n'a jamais vu
une seule haraka à l'entraînement, et son vocabulaire les accepte quand même
— elles deviennent des tokens dont l'embedding n'a jamais été ajusté, donc du
hors-distribution silencieux. `speech_normalizer._retirer_tachkil` les efface
pour cette raison ; ce module traite la cause d'en dessous.

Cette cause est mesurable, et elle a été mesurée le 19 août 2026 : sur les
226 formes arabes du glossaire officiel (`svt_terminology_ar.SVT_GLOSSARY`),
**198 n'apparaissent NULLE PART** dans les 9 997 transcriptions de
`combined_training_recent/metadata_all.csv`, le corpus sur lequel le
checkpoint en service a été entraîné. Le professeur du corpus ne les dit
jamais : il enseigne en darija et nomme les notions en français. Quand l'app
les envoie quand même, le modèle improvise — c'est ça, « le mot mal
prononcé ».

D'où la règle, qui est aussi celle du prompt : **ces termes-là se disent en
français**. Le BAC BIOF est en français, le tableau l'est déjà, l'élève les
lit sous cette forme dans son épreuve. Seul le texte envoyé au TTS est
réécrit — l'affichage garde ce que le tuteur a écrit.

Les 28 formes que le corpus CONNAÎT ne sont pas ici (الطاقة، الخلية، الحرارة،
الكليكوز، حليل…) : le modèle sait les dire, on ne touche pas à ce qui marche.

La mesure a été refaite une seconde fois, au niveau où la reconnaissance
opère vraiment : le motif accepte un mot SANS son article, et « الأكتين » se
reconnaît donc aussi dans « أكتين ». Deux entrées tombaient dans ce cas —
أكتين (3 fois) et تيمين (2 fois), que le professeur prononce à la française —
et elles ont été retirées. Sur les 186 restantes, le corpus n'en contient
aucune, sous aucune forme.

Cinq formes mesurées absentes sont écartées volontairement — leur sens
courant écrase le sens scientifique, et les traduire abîmerait des phrases
entières :

  الرسول (ARNm)      — « le messager », mot du registre religieux
  الناقل (ARNt)      — « le porteur », mot de tous les jours
  الانتقال (obduction) — « le déplacement », omniprésent
  التكامل (complémentarité) — « l'intégrale » en maths, autre matière
  شريط (brin)        — « la bande », mot de tous les jours

Trois formes arabes portaient DEUX termes français dans le glossaire ;
l'arbitrage est fixé ici, une seule lecture par mot :

  الاستنساخ → « la transcription » (la réplication, c'est التضاعف)
  العبور → « le crossing-over » (nom employé tel quel au BAC marocain)
  الانصهار الجزئي → « la fusion partielle »

Pour ajouter une entrée : vérifier d'abord que la forme est bien ABSENTE du
corpus (`metadata_all.csv`, colonne `text`). Si le professeur la dit, la
laisser en arabe.
"""
from __future__ import annotations

#: Forme arabe → ce que la voix doit dire à la place. L'article français est
#: inclus : « الأكسجين كيدخل » se dit « l'oxygène kaydkhol », pas « oxygène
#: kaydkhol ».
_ABSENTS_DU_CORPUS: dict[str, str] = {
    # ── Consommation de la matière organique et flux d'énergie ──
    "تدفق الطاقة": "le flux d'énergie",
    "الهيولى": "le cytoplasme",
    "الغشاء الهيولي": "la membrane plasmique",
    "ركيزة": "le substrat",
    "الأيض": "le métabolisme",
    "التنفس الخلوي": "la respiration cellulaire",
    "التحلل السكري": "la glycolyse",
    "حمض البيروفيك": "l'acide pyruvique",
    "الأدينوزين ثلاثي الفوسفات": "l'ATP",
    "الأدينوزين ثنائي الفوسفات": "l'ADP",
    "حلقة كريبس": "le cycle de Krebs",
    "السلسلة التنفسية": "la chaîne respiratoire",
    "الفسفرة التأكسدية": "la phosphorylation oxydative",
    "الميتوكوندري": "la mitochondrie",
    "الحشوة": "la matrice mitochondriale",
    "الأعراف الميتوكوندرية": "les crêtes mitochondriales",
    "الغشاء الداخلي": "la membrane interne",
    "الغشاء الخارجي": "la membrane externe",
    "الأكسجين": "l'oxygène",
    "ثنائي أكسيد الكربون": "le dioxyde de carbone",
    "الحصيلة الطاقية": "le bilan énergétique",
    "التخمر": "la fermentation",
    "التخمر الكحولي": "la fermentation alcoolique",
    "التخمر اللبني": "la fermentation lactique",
    "الإيثانول": "l'éthanol",
    "حمض اللبنيك": "l'acide lactique",
    "لاهوائي": "anaérobie",
    "العضلة الهيكلية المخططة": "le muscle strié squelettique",
    "الليف العضلي": "la fibre musculaire",
    "اللييف العضلي": "la myofibrille",
    "القسيم العضلي": "le sarcomère",
    "الساركومير": "le sarcomère",
    "التقلص العضلي": "la contraction musculaire",
    "الارتخاء": "le relâchement",
    "الشبكة الساركوبلازمية": "le réticulum sarcoplasmique",
    "الصفيحة المحركة": "la plaque motrice",
    "كمون العمل": "le potentiel d'action",
    "المنبه": "le stimulus",
    "الكزاز": "le tétanos",
    "التعب العضلي": "la fatigue musculaire",
    "فوسفات الكرياتين": "la créatine phosphate",
    "الكليكوجين": "le glycogène",
    "المجهود العضلي": "l'effort physique",

    # ── Nature et expression du matériel génétique ──
    "المعلومة الوراثية": "l'information génétique",
    "المادة الوراثية": "le matériel génétique",
    "الحمض الريبي النووي الريبوزي الناقص الأكسجين": "l'ADN",
    "الحمض الريبي النووي": "l'ARN",
    "الريبوزومي": "ribosomique",
    "قاعدة آزوتية": "la base azotée",
    "الأدينين": "l'adénine",
    "الكوانين": "la guanine",
    "السيتوزين": "la cytosine",
    "اليوراسيل": "l'uracile",
    "ريبوز ناقص الأكسجين": "le désoxyribose",
    "رابطة فوسفو ثنائية الإستر": "la liaison phosphodiester",
    "رابطة هيدروجينية": "la liaison hydrogène",
    "اللولب المزدوج": "la double hélice",
    "متعاكس التوازي": "antiparallèle",
    "صبغي": "le chromosome",
    "صبغين": "la chromatine",
    "مورثة": "le gène",
    "النمط الوراثي": "le génotype",
    "النمط الظاهري": "le phénotype",
    "طفرة": "la mutation",
    "موقع المورثة": "le locus",
    "الاستنساخ": "la transcription",
    "التضاعف نصف المحافظ": "la réplication semi-conservative",
    "السلسلة القالب": "le brin matrice",
    "شوكة التضاعف": "la fourche de réplication",
    "السلسلة المستنسخة": "le brin transcrit",
    "السلسلة المرمزة": "le brin codant",
    "الترجمة": "la traduction",
    "ريبوزوم": "le ribosome",
    "رامزة": "le codon",
    "الرامزة المضادة": "l'anticodon",
    "حمض أميني": "l'acide aminé",
    "الرمز الوراثي": "le code génétique",
    "رامزة الانطلاق": "le codon initiateur",
    "رامزة التوقف": "le codon stop",
    "عديد الببتيد": "le polypeptide",
    "رابطة ببتيدية": "la liaison peptidique",
    "الانقسام غير المباشر": "la mitose",
    "الطور البيني": "l'interphase",
    "الطور التمهيدي": "la prophase",
    "الطور الاستوائي": "la métaphase",
    "الطور الانفصالي": "l'anaphase",
    "الطور النهائي": "la télophase",
    "انقسام الهيولى": "la cytocinèse",
    "المغزل اللالوني": "le fuseau achromatique",
    "الصفيحة الاستوائية": "la plaque équatoriale",
    "خلية ثنائية الصيغة الصبغية": "une cellule diploïde",
    "خلية أحادية الصيغة الصبغية": "une cellule haploïde",
    "الانقسام الاختزالي الأول": "la division réductionnelle",
    "الانقسام الاختزالي الثاني": "la division équationnelle",
    "الانقسام الاختزالي": "la méiose",
    "مشيج": "le gamète",
    "التوزيع المستقل للصبغيات": "le brassage interchromosomique",
    "العبور": "le crossing-over",
    "التصالب": "le chiasma",
    "رباعية الصبغيات": "la tétrade",
    "ثنائية التكافؤ": "le bivalent",
    "حيوان منوي": "le spermatozoïde",
    "بويضة": "l'ovule",
    "بيضة مخصبة": "le zygote",
    "زيكوت": "le zygote",
    "ثنائي الصيغة الصبغية": "diploïde",
    "أحادي الصيغة الصبغية": "haploïde",

    # ── Matières organiques et inorganiques, environnement ──
    "المادة غير العضوية": "la matière inorganique",
    "إعادة التدوير": "le recyclage",
    "التسميد العضوي": "le compostage",
    "الفرز الانتقائي": "le tri sélectif",
    "قابل للتحلل البيولوجي": "biodégradable",
    "غير قابل للتحلل": "non biodégradable",
    "تلوث الغلاف الجوي": "la pollution atmosphérique",
    "تلوث الماء": "la pollution de l'eau",
    "تلوث التربة": "la pollution du sol",
    "التلوث": "la pollution",
    "الاحتباس الحراري": "l'effet de serre",
    "طبقة الأوزون": "la couche d'ozone",
    "الأمطار الحمضية": "les pluies acides",
    "التخثث": "l'eutrophisation",
    "الإثراء الغذائي": "l'eutrophisation",
    "التنمية المستدامة": "le développement durable",
    "الطاقة المتجددة": "l'énergie renouvelable",
    "الطاقة الأحفورية": "l'énergie fossile",
    "الطاقة النووية": "l'énergie nucléaire",
    "الانشطار النووي": "la fission nucléaire",
    "الاندماج النووي": "la fusion nucléaire",
    "نفايات مشعة": "les déchets radioactifs",
    "محطة نووية": "une centrale nucléaire",
    "عمر النصف": "la demi-vie",

    # ── Phénomènes géologiques et tectonique des plaques ──
    "تكتونية الصفائح": "la tectonique des plaques",
    "صفيحة تكتونية": "une plaque tectonique",
    "الغلاف الصخري": "la lithosphère",
    "الليتوسفير": "la lithosphère",
    "الأستينوسفير": "l'asthénosphère",
    "القشرة القارية": "la croûte continentale",
    "القشرة المحيطية": "la croûte océanique",
    "الرداء العلوي": "le manteau supérieur",
    "الرداء": "le manteau",
    "سلسلة الاندساس": "la chaîne de subduction",
    "سلسلة التصادم": "la chaîne de collision",
    "سلسلة جبلية": "une chaîne de montagnes",
    "الاندساس": "la subduction",
    "الطمر": "la subduction",
    "التصادم": "la collision",
    "التباعد": "la divergence",
    "التقارب": "la convergence",
    "الريفت": "le rift",
    "الصدع": "le rift",
    "الظهرة المحيطية": "la dorsale océanique",
    "الخندق المحيطي": "la fosse océanique",
    "أوفيوليت": "l'ophiolite",
    "طبقة الزحف": "la nappe de charriage",
    "زلزال": "un séisme",
    "البركانية": "le volcanisme",
    "الصهارة الكرانيتية": "le magma granitique",
    "الماغما": "le magma",
    "الصهارة": "le magma",
    "الكرانيت": "le granite",
    "البازلت": "le basalte",
    "الكابرو": "le gabbro",
    "البيريدوتيت": "la péridotite",
    "صخرة متحولة": "une roche métamorphique",
    "صخرة رسوبية": "une roche sédimentaire",
    "صخرة ماغماتية": "une roche magmatique",
    "سحنة التحول": "le faciès métamorphique",
    "الشيست الأخضر": "le schiste vert",
    "الشيست الأزرق": "le schiste bleu",
    "الأمفيبوليت": "l'amphibolite",
    "الإكلوجيت": "l'éclogite",
    "الكرانوليت": "la granulite",
    "المنحدر الجيوحراري": "le gradient géothermique",
    "خطوط تساوي الدرجة": "les isogrades",
    "معدن مؤشر": "un minéral index",
    "الكلوريت": "la chlorite",
    "العقيق": "le grenat",
    "الكلوكوفان": "la glaucophane",
    "الجاديت": "la jadéite",
    "الديستين": "le disthène",
    "السيليمانيت": "la sillimanite",
    "التكرنت": "la granitisation",
    "الانصهار الجزئي": "la fusion partielle",
    "الميغماتيت": "la migmatite",
    "التمايز الصهاري": "la différenciation magmatique",
    "التبلور": "la cristallisation",
}


#: Deuxième table, SECOND CRITÈRE — à ne pas confondre avec la première.
#:
#: Ici ce n'est plus « la voix ne sait pas le dire », c'est « l'élève doit
#: l'entendre en français » : demandé le 20 août 2026, et c'est aussi ce que
#: dit le prompt depuis toujours (« PAS de السرعة، التسارع، القوة »). Une loi,
#: une grandeur, une relation portent au BAC un nom français — c'est celui
#: qu'il écrira sur sa copie, donc celui qu'il doit entendre.
#:
#: La mesure va d'ailleurs dans le même sens : le professeur du corpus ne
#: nomme JAMAIS une loi en arabe. « قانون نيوتن », « قانون أوم »,
#: « قانون مندل », « مبدأ القصور », « انحفاظ الطاقة », « اللوح » — zéro
#: occurrence sur 9 997 transcriptions. Les grandeurs qui, elles, sont
#: attestées (« العلاقة » 97 fois, « السرعة » 9 fois) passent quand même en
#: français : c'est le choix pédagogique, assumé.
#:
#: La demande du 20 août 2026 élargit volontairement la frontière : les mots
#: simples de la classe doivent aussi être en français dans le chat LLM et dans
#: la copie envoyée à la voix. « الكراس » devient donc « le cahier », et non
#: une translittération arabe approximative (« korass »).
#:
#: Cinq écartées malgré le critère, leur sens courant l'emportant de trop
#: loin sur le sens scientifique. Les trois premières se voyaient à l'œil,
#: les deux dernières seulement à la mesure — les 9 997 transcriptions
#: repassées dans le normaliseur, avant et après, puis le diff relu :
#:   النهاية — « la limite » en maths, mais « فالنهاية » veut dire « à la fin »
#:   الشدة   — « بشدة » veut dire « fortement » ; seul « شدة التيار » est gardé
#:   الحل    — « la solution » d'un exercice : mot de la classe, pas grandeur
#:   العلاقة — 97 déclenchements, presque tous sur « عندهم علاقة ب », qui veut
#:             dire « en rapport avec ». « عندهم la relation ب » ne se dit pas.
#:   المجموعة — 13 déclenchements, tous au sens courant de « somme, groupe ».
#:
#: C'est la mesure qui décide, pas l'intuition : faire passer le corpus dans
#: le normaliseur avant/après et LIRE le diff est le seul test qui ait attrapé
#: ces deux-là.
_LOIS_ET_EXPRESSIONS: dict[str, str] = {
    # ── Le tableau ──
    "اللوح": "le tableau",
    "السبورة": "le tableau",

    # ── Lois, principes, théorèmes ──
    "القانون الأول لنيوتن": "la première loi de Newton",
    "القانون الثاني لنيوتن": "la deuxième loi de Newton",
    "القانون الثالث لنيوتن": "la troisième loi de Newton",
    "قوانين نيوتن": "les lois de Newton",
    "قانون نيوتن": "la loi de Newton",
    "قانون أوم": "la loi d'Ohm",
    "قوانين مندل": "les lois de Mendel",
    "قانون مندل": "la loi de Mendel",
    "مبدأ انحفاظ الطاقة": "le principe de conservation de l'énergie",
    "انحفاظ الطاقة": "la conservation de l'énergie",
    "مبدأ القصور": "le principe d'inertie",
    "مبرهنة فيثاغورس": "le théorème de Pythagore",
    "المبرهنة": "le théorème",
    "القانون": "la loi",
    "القوانين": "les lois",
    "المبدأ": "le principe",
    "النظرية": "la théorie",

    # ── Grandeurs, relations, objets mathématiques ──
    "المعادلات": "les équations",
    "المعادلة": "l'équation",
    "الصيغة": "la formule",
    "الدالة": "la fonction",
    "المشتقة": "la dérivée",
    "المتتالية": "la suite",
    "البرهان": "la démonstration",
    "الخاصية": "la propriété",
    "الطاقة الحركية": "l'énergie cinétique",
    "السرعة": "la vitesse",
    "التسارع": "l'accélération",
    "القوة": "la force",
    "شدة التيار": "l'intensité du courant",
    "التيار": "le courant",
    "التوتر": "la tension",
    "المقاومة": "la résistance",
    "الكتلة": "la masse",
    "الحجم": "le volume",
    "التركيز": "la concentration",
    "درجة الحرارة": "la température",
}

#: Mots courants explicitement demandés en français dans le chat LLM.
#:
#: Deux entrées ont été retirées après mesure sur le corpus — elles ne
#: prononçaient pas mal, elles disaient FAUX :
#:   كتب  → « écris » : 14 déclenchements, 12 au passé (« كتب ليا » = « il
#:          m'a écrit »). L'imperatif « اكتب », lui, est bien gardé.
#:   كتبت → « j'ai écrit » : « شكون كتبت؟ » (« qui a écrit ? ») devenait
#:          « شكون j'ai écrit ? », et « القاعدة اللي كتبت فوق » changeait de
#:          sujet au passage.
#: Un mot mal prononcé se rattrape ; une phrase qui dit le contraire de ce
#: qu'elle veut dire, non.
_MOTS_SIMPLES_DU_CHAT: dict[str, str] = {
    "الكراس": "le cahier",
    "كراس": "le cahier",
    "كناش": "le cahier",
    "كوراس": "le cahier",
    "التمرين": "l'exercice",
    "تمرين": "l'exercice",
    "المثال": "l'exemple",
    "مثال": "l'exemple",
    "التعريف": "la définition",
    "تعريف": "la définition",
    "الجواب": "la réponse",
    "جواب": "la réponse",
    "الإجابة": "la réponse",
    "إجابة": "la réponse",
    "السؤال": "la question",
    "سؤال": "la question",
    "الطريقة": "la méthode",
    "طريقة": "la méthode",
    "الخطوة": "l'étape",
    "خطوة": "l'étape",
    "احسب": "calcule",
    "اكتب": "écris",
    "من بعد": "ensuite",
    # Matériel et vocabulaire de classe.
    "الورقة": "la feuille",
    "ورقة": "la feuille",
    "الدفتر": "le cahier",
    "دفتر": "le cahier",
    "القلم": "le stylo",
    "قلم": "le stylo",
    "الفكرة": "l'idée",
    "فكرة": "l'idée",
    "المشكل": "le problème",
    "المشكلة": "le problème",
    "المعلومة": "l'information",
    "المعلومات": "les informations",
    "القاعدة": "la règle",
    "القواعد": "les règles",
    "النتيجة": "le résultat",
    "النتائج": "les résultats",
    "الحساب": "le calcul",
    "المعطى": "la donnée",
    "المعطيات": "les données",
    "القيمة": "la valeur",
    "القيم": "les valeurs",
    "العدد": "le nombre",
    "الأعداد": "les nombres",
    "النسبة": "la proportion",
    "الكسر": "la fraction",
    "الكسور": "les fractions",
    "البسط": "le numérateur",
    "المقام": "le dénominateur",
    "المتغير": "la variable",
    "المجهول": "l'inconnue",
    # Transitions et nombres très fréquents dans les explications orales.
    "هنا": "ici",
    "الآن": "maintenant",
    "إذن": "donc",
    "خطوة بخطوة": "étape par étape",
    "صفر": "zéro",
    "واحد": "un",
    "جوج": "deux",
    "ثلاثة": "trois",
    "ربعة": "quatre",
    "خمسة": "cinq",
    "ستة": "six",
    "سبعة": "sept",
    "ثمانية": "huit",
    "تسعود": "neuf",
    "عشرة": "dix",
    "زائد": "plus",
    "ناقص": "moins",
}

#: Ce que lit `speech_normalizer`. Les deux critères se rejoignent ici, mais
#: restent séparés au-dessus : on n'ajoute pas une entrée dans la première
#: table sans l'avoir mesurée absente du corpus.
TERMES_DITS_EN_FRANCAIS: dict[str, str] = {
    **_ABSENTS_DU_CORPUS,
    **_LOIS_ET_EXPRESSIONS,
    **_MOTS_SIMPLES_DU_CHAT,
}
