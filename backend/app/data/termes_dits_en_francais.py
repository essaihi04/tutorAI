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
TERMES_DITS_EN_FRANCAIS: dict[str, str] = {
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
