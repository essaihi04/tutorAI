-- Insert missing Physics and Chemistry chapters
-- Run this in Supabase SQL Editor

-- First, let's check what subjects exist
-- SELECT id, name_fr FROM subjects;

-- Insert Physics chapters (if not already present)
INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
SELECT 
    gen_random_uuid(),
    (SELECT id FROM subjects WHERE name_fr = 'Physique'),
    chapter_number,
    title_fr,
    title_ar,
    description_fr,
    description_ar,
    difficulty_level,
    estimated_hours,
    order_index
FROM jsonb_to_recordset('[
  {"chapter_number": 1, "title_fr": "Ondes mecaniques progressives", "title_ar": "الأمواج الميكانيكية المتوالية", "description_fr": "Definition, propagation, celerite, retard temporel", "description_ar": "التعريف، الانتشار، سرعة الانتشار، التأخر الزمني", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 0},
  {"chapter_number": 2, "title_fr": "Ondes mecaniques progressives periodiques", "title_ar": "الأمواج الميكانيكية المتوالية الدورية", "description_fr": "Periodicite, longueur d\'onde, phenomene de diffraction", "description_ar": "الدورية، طول الموجة، ظاهرة الحيود", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 1},
  {"chapter_number": 3, "title_fr": "Propagation des ondes lumineuses", "title_ar": "انتشار الأمواج الضوئية", "description_fr": "Diffraction, dispersion, interferences lumineuses", "description_ar": "الحيود، التشتت، التداخلات الضوئية", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 2},
  {"chapter_number": 4, "title_fr": "Dipole RC", "title_ar": "ثنائي القطب RC", "description_fr": "Charge et decharge d\'un condensateur, constante de temps", "description_ar": "شحن وتفريغ المكثف، ثابت الزمن", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 3},
  {"chapter_number": 5, "title_fr": "Dipole RL", "title_ar": "ثنائي القطب RL", "description_fr": "Etablissement et rupture du courant, auto-induction", "description_ar": "تأسيس وانقطاع التيار، الحث الذاتي", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 4},
  {"chapter_number": 6, "title_fr": "Circuit RLC serie", "title_ar": "دارة RLC التسلسلية", "description_fr": "Regime libre, regime force, resonance", "description_ar": "النظام الحر، النظام القسري، الرنين", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 5},
  {"chapter_number": 7, "title_fr": "Reactions acides-bases", "title_ar": "تفاعلات الأحماض والقواعد", "description_fr": "Couples acide/base, pH, titrage", "description_ar": "أزواج الحمض/القاعدة، الأس الهيدروجيني، المعايرة", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 6},
  {"chapter_number": 8, "title_fr": "Reactions de precipitation", "title_ar": "تفاعلات الترسيب", "description_fr": "Produit de solubilite, precipitation selective", "description_ar": "حاصل الذوبان، الترسيب الانتقائي", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 7},
  {"chapter_number": 9, "title_fr": "Reactions d\'oxydo-reduction", "title_ar": "تفاعلات الأكسدة والاختزال", "description_fr": "Piles, electrolyse, reactions spontanees", "description_ar": "الخلايا، التحليل الكهربائي، التفاعلات التلقائية", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 8},
  {"chapter_number": 10, "title_fr": "Notion de champs", "title_ar": "مفهوم المجالات", "description_fr": "Champ gravitationnel, champ electrique", "description_ar": "المجال الثقالي، المجال الكهربائي", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 9},
  {"chapter_number": 11, "title_fr": "Force de Lorentz", "title_ar": "قوة لورنتز", "description_fr": "Mouvement d\'une charge dans B uniforme", "description_ar": "حركة الشحنة في مجال منتظم", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 10},
  {"chapter_number": 12, "title_fr": "Lois de Newton", "title_ar": "قوانين نيوتن", "description_fr": "Principe d\'inertie, action-reaction", "description_ar": "مبدأ القصور الذاتي، الفعل ورد الفعل", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 11},
  {"chapter_number": 13, "title_fr": "Satellites et planetes", "title_ar": "الأقمار والكواكب", "description_fr": "Mouvement circulaire uniforme, energie", "description_ar": "الحركة الدائرية المنتظمة، الطاقة", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 12},
  {"chapter_number": 14, "title_fr": "Oscillateurs mecaniques", "title_ar": "المتذبذبات الميكانيكية", "description_fr": "Pendule simple, oscillations amorties", "description_ar": "البندول البسيط، التذبذبات المضعفة", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 13},
  {"chapter_number": 15, "title_fr": "Ondes mecaniques stationnaires", "title_ar": "الأمواج الميكانيكية القائمة", "description_fr": "Cordes vibrantes, tubes sonores", "description_ar": "الأوتار المهتزة، الأنابيب الصوتية", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 14}
]'::jsonb) AS x(chapter_number int, title_fr text, title_ar text, description_fr text, description_ar text, difficulty_level text, estimated_hours float, order_index int)
WHERE NOT EXISTS (
    SELECT 1 FROM chapters c 
    JOIN subjects s ON c.subject_id = s.id 
    WHERE s.name_fr = 'Physique' AND c.chapter_number = x.chapter_number
);

-- Insert Chemistry chapters (if not already present)
INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
SELECT 
    gen_random_uuid(),
    (SELECT id FROM subjects WHERE name_fr = 'Chimie'),
    chapter_number,
    title_fr,
    title_ar,
    description_fr,
    description_ar,
    difficulty_level,
    estimated_hours,
    order_index
FROM jsonb_to_recordset('[
  {"chapter_number": 1, "title_fr": "Transformations lentes et transformations rapides", "title_ar": "التحولات البطيئة والتحولات السريعة", "description_fr": "Facteurs cinetiques, catalyse, suivi d\'une reaction", "description_ar": "العوامل الحركية، الحفز، تتبع تفاعل", "difficulty_level": "beginner", "estimated_hours": 2.0, "order_index": 0},
  {"chapter_number": 2, "title_fr": "Suivi temporel d\'une transformation chimique - Vitesse de reaction", "title_ar": "التتبع الزمني لتحول كيميائي - سرعة التفاعل", "description_fr": "Vitesse volumique, temps de demi-reaction, methodes de suivi", "description_ar": "السرعة الحجمية، زمن نصف التفاعل، طرق التتبع", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 1},
  {"chapter_number": 3, "title_fr": "Decroissance radioactive", "title_ar": "التناقص الإشعاعي", "description_fr": "Radioactivite, loi de decroissance, demi-vie, activite", "description_ar": "النشاط الإشعاعي، قانون التناقص، عمر النصف، النشاط", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 2},
  {"chapter_number": 4, "title_fr": "Noyaux, masse et energie", "title_ar": "النوى والكتلة والطاقة", "description_fr": "Equivalence masse-energie, energie de liaison, fission et fusion", "description_ar": "تكافؤ الكتلة والطاقة، طاقة الربط، الانشطار والاندماج", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 3},
  {"chapter_number": 5, "title_fr": "Transformations chimiques s\'effectuant dans les 2 sens", "title_ar": "التحولات الكيميائية التي تتم في المنحيين", "description_fr": "Reaction incomplete, quotient de reaction, avancement final", "description_ar": "التفاعل غير التام، حاصل التفاعل، التقدم النهائي", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 4},
  {"chapter_number": 6, "title_fr": "Evolution spontanee d\'un systeme chimique", "title_ar": "التطور التلقائي للنظام الكيميائي", "description_fr": "Critere d\'evolution, constante d\'equilibre", "description_ar": "معيار التطور، ثابت التوازن", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 5},
  {"chapter_number": 7, "title_fr": "Evolution d\'un systeme chimique vers l\'equilibre", "title_ar": "تطور النظام الكيميائي نحو التوازن", "description_fr": "Quotient de reaction, sens d\'evolution", "description_ar": "حاصل التفاعل، اتجاه التطور", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 6},
  {"chapter_number": 8, "title_fr": "Reactions acido-basiques", "title_ar": "تفاعلات الأحماض والقواعد", "description_fr": "Couples acide/base, pH, dosage", "description_ar": "أزواج الحمض/القاعدة، الأس الهيدروجيني، المعايرة", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 7},
  {"chapter_number": 9, "title_fr": "Reactions de precipitation", "title_ar": "تفاعلات الترسيب", "description_fr": "Produit de solubilite Ks, precipitation selective", "description_ar": "حاصل الذوبان، الترسيب الانتقائي", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 8},
  {"chapter_number": 10, "title_fr": "Piles electrochimiques", "title_ar": "الخلايا الكهروكيميائية", "description_fr": "Pile Daniell, force electromotrice", "description_ar": "خلية دانييل، القوة الدافعة الكهربائية", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 9},
  {"chapter_number": 11, "title_fr": "Electrolyse", "title_ar": "التحليل الكهربائي", "description_fr": "Electrolyse forcee, loi de Faraday", "description_ar": "التحليل الكهربائي القسري، قانون فاراداي", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 10},
  {"chapter_number": 12, "title_fr": "Esterification et hydrolyse", "title_ar": "الإسترة والتحلل المائي", "description_fr": "Equilibre chimique, cinetique", "description_ar": "التوازن الكيميائي، الحركية", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 11},
  {"chapter_number": 13, "title_fr": "Controle de l\'evolution d\'un systeme chimique", "title_ar": "التحكم في تطور النظام الكيميائي", "description_fr": "Modification des conditions d\'equilibre", "description_ar": "تعديل شروط التوازن", "difficulty_level": "advanced", "estimated_hours": 4.0, "order_index": 12},
  {"chapter_number": 14, "title_fr": "Phénomenes oxydo-reductions", "title_ar": "ظواهر الأكسدة والاختزال", "description_fr": "Transfert d\'electrons, piles", "description_ar": "انتقال الإلكترونات، الخلايا", "difficulty_level": "intermediate", "estimated_hours": 3.0, "order_index": 13}
]'::jsonb) AS x(chapter_number int, title_fr text, title_ar text, description_fr text, description_ar text, difficulty_level text, estimated_hours float, order_index int)
WHERE NOT EXISTS (
    SELECT 1 FROM chapters c 
    JOIN subjects s ON c.subject_id = s.id 
    WHERE s.name_fr = 'Chimie' AND c.chapter_number = x.chapter_number
);

-- Verify the insertions
SELECT s.name_fr as subject, COUNT(c.id) as chapter_count 
FROM subjects s 
LEFT JOIN chapters c ON s.id = c.subject_id 
GROUP BY s.id, s.name_fr;
