"""
Glossaire officiel SVT - 2ème BAC Sciences Physiques BIOF
Termes scientifiques en arabe tels qu'utilisés dans le programme marocain officiel.
Source: Manuels scolaires marocains (AlloSchool, Moutamadris, etc.)

Chaque terme est au format: terme_fr -> terme_ar
L'IA doit utiliser EXACTEMENT ces termes lorsqu'elle communique en arabe.
"""

SVT_GLOSSARY = {
    # ============================================================
    # CHAPITRE 1: Consommation de la matière organique et flux d'énergie
    # استهلاك المادة العضوية وتدفق الطاقة
    # ============================================================
    
    # Termes généraux
    "matière organique": "المادة العضوية",
    "énergie": "الطاقة",
    "flux d'énergie": "تدفق الطاقة",
    "cellule": "الخلية",
    "cytoplasme": "الهيولى",
    "noyau": "النواة",
    "membrane plasmique": "الغشاء الهيولي",
    "enzyme": "إنزيم",
    "substrat": "ركيزة",
    "métabolisme": "الأيض",
    "catabolisme": "الهدم",
    "anabolisme": "البناء",
    
    # Respiration cellulaire
    "respiration cellulaire": "التنفس الخلوي",
    "glycolyse": "التحلل السكري",  # ou "انحلال الكليكوز"
    "glucose": "الكليكوز",
    "pyruvate": "حمض البيروفيك",
    "acide pyruvique": "حمض البيروفيك",
    "ATP": "ATP (الأدينوزين ثلاثي الفوسفات)",
    "ADP": "ADP (الأدينوزين ثنائي الفوسفات)",
    "NAD": "NAD",
    "NADH": "NADH",
    "FAD": "FAD",
    "FADH2": "FADH2",
    "cycle de Krebs": "حلقة كريبس",
    "chaîne respiratoire": "السلسلة التنفسية",
    "phosphorylation oxydative": "الفسفرة التأكسدية",
    "mitochondrie": "الميتوكوندري",
    "matrice mitochondriale": "الحشوة (الماتريس)",
    "crêtes mitochondriales": "الأعراف الميتوكوندرية",
    "membrane interne": "الغشاء الداخلي",
    "membrane externe": "الغشاء الخارجي",
    "oxygène": "الأكسجين",
    "dioxyde de carbone": "ثنائي أكسيد الكربون",
    "CO2": "CO2",
    "H2O": "H2O (الماء)",
    "bilan énergétique": "الحصيلة الطاقية",
    "rendement énergétique": "المردود الطاقي",
    
    # Fermentation
    "fermentation": "التخمر",
    "fermentation alcoolique": "التخمر الكحولي",
    "fermentation lactique": "التخمر اللبني",
    "éthanol": "الإيثانول",
    "acide lactique": "حمض اللبنيك",
    "anaérobie": "لاهوائي",
    "aérobie": "هوائي",
    
    # Muscle strié squelettique
    "muscle strié squelettique": "العضلة الهيكلية المخططة",
    "fibre musculaire": "الليف العضلي",
    "myofibrille": "اللييف العضلي",
    "sarcomère": "القسيم العضلي (الساركومير)",
    "actine": "الأكتين",
    "myosine": "الميوزين",
    "contraction musculaire": "التقلص العضلي",
    "relâchement": "الارتخاء",
    "calcium": "الكالسيوم",
    "réticulum sarcoplasmique": "الشبكة الساركوبلازمية",
    "plaque motrice": "الصفيحة المحركة",
    "potentiel d'action": "كمون العمل",
    "stimulus": "المنبه",
    "tétanos": "الكزاز",
    "fatigue musculaire": "التعب العضلي",
    "créatine phosphate": "فوسفات الكرياتين",
    "glycogène": "الكليكوجين",
    "effort physique": "المجهود العضلي",
    
    # ============================================================
    # CHAPITRE 2: Nature et mécanisme de l'expression du matériel génétique
    # طبيعة وآلية التعبير عن المادة الوراثية
    # ============================================================
    
    # ADN et information génétique
    "information génétique": "المعلومة الوراثية",
    "matériel génétique": "المادة الوراثية",
    "ADN": "ADN (الحمض الريبي النووي الريبوزي الناقص الأكسجين)",
    "ARN": "ARN (الحمض الريبي النووي)",
    "ARNm": "ARNm (الرسول)",
    "ARNt": "ARNt (الناقل)",
    "ARNr": "ARNr (الريبوزومي)",
    "nucléotide": "نيكليوتيد",
    "base azotée": "قاعدة آزوتية",
    "adénine": "الأدينين (A)",
    "thymine": "التيمين (T)",
    "guanine": "الكوانين (G)",
    "cytosine": "السيتوزين (C)",
    "uracile": "اليوراسيل (U)",
    "désoxyribose": "ريبوز ناقص الأكسجين",
    "ribose": "ريبوز",
    "liaison phosphodiester": "رابطة فوسفو ثنائية الإستر",
    "liaison hydrogène": "رابطة هيدروجينية",
    "double hélice": "اللولب المزدوج",
    "brin": "سلسلة (شريط)",
    "complémentarité": "التكامل",
    "antiparallèle": "متعاكس التوازي",
    "chromosome": "صبغي",
    "chromatine": "صبغين",
    "gène": "مورثة",
    "allèle": "حليل",
    "génotype": "النمط الوراثي",
    "phénotype": "النمط الظاهري",
    "mutation": "طفرة",
    "locus": "موقع المورثة",
    
    # Réplication
    "réplication": "تضاعف ADN (الاستنساخ)",
    "réplication semi-conservative": "التضاعف نصف المحافظ",
    "ADN polymérase": "ADN بوليميراز",
    "brin matrice": "السلسلة القالب",
    "brin néoformé": "السلسلة الجديدة",
    "fourche de réplication": "شوكة التضاعف",
    
    # Transcription
    "transcription": "الاستنساخ",
    "ARN polymérase": "ARN بوليميراز",
    "brin transcrit": "السلسلة المستنسخة",
    "brin codant": "السلسلة المرمزة",
    "promoteur": "المحفز",
    
    # Traduction
    "traduction": "الترجمة",
    "ribosome": "ريبوزوم",
    "codon": "رامزة",
    "anticodon": "الرامزة المضادة",
    "acide aminé": "حمض أميني",
    "protéine": "بروتين",
    "code génétique": "الرمز الوراثي",
    "codon initiateur": "رامزة الانطلاق (AUG)",
    "codon stop": "رامزة التوقف",
    "polypeptide": "عديد الببتيد",
    "liaison peptidique": "رابطة ببتيدية",
    
    # Mitose
    "mitose": "الانقسام غير المباشر",
    "interphase": "الطور البيني",
    "prophase": "الطور التمهيدي",
    "métaphase": "الطور الاستوائي",
    "anaphase": "الطور الانفصالي",
    "télophase": "الطور النهائي",
    "cytocinèse": "انقسام الهيولى",
    "fuseau achromatique": "المغزل اللالوني",
    "plaque équatoriale": "الصفيحة الاستوائية",
    "cellule diploïde": "خلية ثنائية الصيغة الصبغية (2n)",
    
    # Méiose
    "méiose": "الانقسام الاختزالي",
    "division réductionnelle": "الانقسام الاختزالي الأول",
    "division équationnelle": "الانقسام الاختزالي الثاني",
    "cellule haploïde": "خلية أحادية الصيغة الصبغية (n)",
    "gamète": "مشيج",
    "brassage interchromosomique": "التوزيع المستقل للصبغيات",
    "brassage intrachromosomique": "العبور (crossing-over)",
    "crossing-over": "العبور",
    "chiasma": "التصالب",
    "tétrade": "رباعية الصبغيات",
    "bivalent": "ثنائية التكافؤ",
    "spermatozoïde": "حيوان منوي",
    "ovule": "بويضة",
    "fécondation": "الإخصاب",
    "zygote": "بيضة مخصبة (زيكوت)",
    "diploïde": "ثنائي الصيغة الصبغية (2n)",
    "haploïde": "أحادي الصيغة الصبغية (n)",
    
    # ============================================================
    # CHAPITRE 3: Utilisation des matières organiques et inorganiques
    # استعمال المواد العضوية وغير العضوية
    # ============================================================
    
    "matière inorganique": "المادة غير العضوية",
    "ordures ménagères": "النفايات المنزلية",
    "recyclage": "إعادة التدوير",
    "compostage": "التسميد العضوي",
    "tri sélectif": "الفرز الانتقائي",
    "biodégradable": "قابل للتحلل البيولوجي",
    "non biodégradable": "غير قابل للتحلل",
    "pollution": "التلوث",
    "pollution atmosphérique": "تلوث الغلاف الجوي",
    "pollution de l'eau": "تلوث الماء",
    "pollution du sol": "تلوث التربة",
    "effet de serre": "الاحتباس الحراري",
    "couche d'ozone": "طبقة الأوزون",
    "pluies acides": "الأمطار الحمضية",
    "eutrophisation": "التخثث (الإثراء الغذائي)",
    "développement durable": "التنمية المستدامة",
    "énergie renouvelable": "الطاقة المتجددة",
    "énergie fossile": "الطاقة الأحفورية",
    "énergie nucléaire": "الطاقة النووية",
    "radioactivité": "النشاط الإشعاعي",
    "fission nucléaire": "الانشطار النووي",
    "fusion nucléaire": "الاندماج النووي",
    "déchet radioactif": "نفايات مشعة",
    "centrale nucléaire": "محطة نووية",
    "uranium": "اليورانيوم",
    "rayonnement": "إشعاع",
    "demi-vie": "عمر النصف",
    
    # ============================================================
    # CHAPITRE 4: Phénomènes géologiques et tectonique des plaques
    # الظواهر الجيولوجية وتكتونية الصفائح
    # ============================================================
    
    "tectonique des plaques": "تكتونية الصفائح",
    "plaque tectonique": "صفيحة تكتونية",
    "lithosphère": "الغلاف الصخري (الليتوسفير)",
    "asthénosphère": "الأستينوسفير",
    "croûte continentale": "القشرة القارية",
    "croûte océanique": "القشرة المحيطية",
    "manteau": "الرداء",
    "manteau supérieur": "الرداء العلوي",
    "subduction": "الاندساس (الطمر)",
    "collision": "التصادم",
    "obduction": "الانتقال (obduction)",
    "divergence": "التباعد",
    "convergence": "التقارب",
    "rift": "الريفت (الصدع)",
    "dorsale océanique": "الظهرة المحيطية",
    "fosse océanique": "الخندق المحيطي",
    "chaîne de montagnes": "سلسلة جبلية",
    "chaîne de subduction": "سلسلة الاندساس",
    "chaîne de collision": "سلسلة التصادم",
    "ophiolite": "أوفيوليت",
    "nappe de charriage": "طبقة الزحف",
    "séisme": "زلزال",
    "volcanisme": "البركانية",
    "magma": "الماغما (الصهارة)",
    "granite": "الكرانيت",
    "basalte": "البازلت",
    "gabbro": "الكابرو",
    "péridotite": "البيريدوتيت",
    
    # Métamorphisme
    "métamorphisme": "التحول",
    "roche métamorphique": "صخرة متحولة",
    "roche sédimentaire": "صخرة رسوبية",
    "roche magmatique": "صخرة ماغماتية",
    "faciès métamorphique": "سحنة التحول",
    "schiste vert": "الشيست الأخضر",
    "schiste bleu": "الشيست الأزرق",
    "amphibolite": "الأمفيبوليت",
    "éclogite": "الإكلوجيت",
    "granulite": "الكرانوليت",
    "pression": "الضغط",
    "température": "الحرارة",
    "gradient géothermique": "المنحدر الجيوحراري",
    "isogrades": "خطوط تساوي الدرجة",
    "minéral index": "معدن مؤشر",
    "chlorite": "الكلوريت",
    "grenat": "العقيق",
    "glaucophane": "الكلوكوفان",
    "jadéite": "الجاديت",
    "disthène": "الديستين",
    "sillimanite": "السيليمانيت",
    
    # Granitisation
    "granitisation": "التكرنت",
    "anatexie": "الانصهار الجزئي",
    "fusion partielle": "الانصهار الجزئي",
    "migmatite": "الميغماتيت",
    "magma granitique": "الصهارة الكرانيتية",
    "différenciation magmatique": "التمايز الصهاري",
    "cristallisation": "التبلور",
}

# Termes groupés par chapitre pour faciliter l'accès
SVT_CHAPTERS_AR = {
    "ch1_energie": {
        "title_fr": "Consommation de la matière organique et flux d'énergie",
        "title_ar": "استهلاك المادة العضوية وتدفق الطاقة",
        "key_terms": [
            "respiration cellulaire", "glycolyse", "glucose", "ATP",
            "mitochondrie", "cycle de Krebs", "chaîne respiratoire",
            "fermentation", "muscle strié squelettique", "sarcomère",
            "contraction musculaire", "actine", "myosine"
        ]
    },
    "ch2_genetique": {
        "title_fr": "Nature et mécanisme de l'expression du matériel génétique",
        "title_ar": "طبيعة وآلية التعبير عن المادة الوراثية",
        "key_terms": [
            "ADN", "ARN", "gène", "chromosome", "réplication",
            "transcription", "traduction", "codon", "protéine",
            "mitose", "méiose", "crossing-over", "mutation"
        ]
    },
    "ch3_environnement": {
        "title_fr": "Utilisation des matières organiques et inorganiques",
        "title_ar": "استعمال المواد العضوية وغير العضوية",
        "key_terms": [
            "pollution", "recyclage", "effet de serre",
            "énergie renouvelable", "énergie nucléaire",
            "développement durable", "radioactivité"
        ]
    },
    "ch4_geologie": {
        "title_fr": "Les phénomènes géologiques et la tectonique des plaques",
        "title_ar": "الظواهر الجيولوجية وتكتونية الصفائح",
        "key_terms": [
            "tectonique des plaques", "subduction", "collision",
            "métamorphisme", "granitisation", "lithosphère",
            "dorsale océanique", "fosse océanique"
        ]
    }
}


def get_glossary_for_prompt(chapter_key: str = None) -> str:
    """
    Génère un glossaire formaté pour injection dans le prompt IA.
    Si chapter_key est fourni, ne retourne que les termes de ce chapitre.
    """
    if chapter_key and chapter_key in SVT_CHAPTERS_AR:
        terms = SVT_CHAPTERS_AR[chapter_key]["key_terms"]
        glossary_lines = []
        for term in terms:
            ar = SVT_GLOSSARY.get(term, "")
            if ar:
                glossary_lines.append(f"- {term} = {ar}")
        return "\n".join(glossary_lines)
    
    # Retourne tout le glossaire (limité aux termes les plus importants)
    glossary_lines = []
    for fr, ar in SVT_GLOSSARY.items():
        glossary_lines.append(f"- {fr} = {ar}")
    return "\n".join(glossary_lines)


def get_full_glossary_text() -> str:
    """Retourne le glossaire complet formaté pour le prompt système."""
    lines = []
    for fr, ar in SVT_GLOSSARY.items():
        lines.append(f"  {fr} → {ar}")
    return "\n".join(lines)
