-- Insert missing Physics and Chemistry chapters
-- Run this in Supabase SQL Editor

-- Get subject IDs first (for reference)
-- SELECT id, name_fr FROM subjects WHERE name_fr IN ('Physique', 'Chimie');

-- Insert Physics chapters one by one (safer approach)
DO $$
DECLARE
    phys_id UUID;
BEGIN
    -- Get Physique subject ID
    SELECT id INTO phys_id FROM subjects WHERE name_fr = 'Physique';
    
    IF phys_id IS NULL THEN
        RAISE EXCEPTION 'Subject Physique not found';
    END IF;
    
    -- Insert Physics chapters if not exists
    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 1, 'Ondes mecaniques progressives', 'الأمواج الميكانيكية المتوالية', 
           'Definition, propagation, celerite, retard temporel', 'التعريف، الانتشار، سرعة الانتشار، التأخر الزمني', 
           'intermediate', 3.0, 0
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 1);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 2, 'Ondes mecaniques progressives periodiques', 'الأمواج الميكانيكية المتوالية الدورية', 
           'Periodicite, longueur donde, phenomene de diffraction', 'الدورية، طول الموجة، ظاهرة الحيود', 
           'intermediate', 3.0, 1
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 2);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 3, 'Propagation des ondes lumineuses', 'انتشار الأمواج الضوئية', 
           'Diffraction, dispersion, interferences lumineuses', 'الحيود، التشتت، التداخلات الضوئية', 
           'advanced', 4.0, 2
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 3);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 4, 'Dipole RC', 'ثنائي القطب RC', 
           'Charge et decharge dun condensateur, constante de temps', 'شحن وتفريغ المكثف، ثابت الزمن', 
           'intermediate', 3.0, 3
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 4);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 5, 'Dipole RL', 'ثنائي القطب RL', 
           'Etablissement et rupture du courant, auto-induction', 'تأسيس وانقطاع التيار، الحث الذاتي', 
           'intermediate', 3.0, 4
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 5);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 6, 'Circuit RLC serie', 'دارة RLC التسلسلية', 
           'Regime libre, regime force, resonance', 'النظام الحر، النظام القسري، الرنين', 
           'advanced', 4.0, 5
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 6);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 7, 'Reactions acides-bases', 'تفاعلات الأحماض والقواعد', 
           'Couples acide/base, pH, titrage', 'أزواج الحمض/القاعدة، الأس الهيدروجيني، المعايرة', 
           'intermediate', 3.0, 6
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 7);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 8, 'Reactions de precipitation', 'تفاعلات الترسيب', 
           'Produit de solubilite, precipitation selective', 'حاصل الذوبان، الترسيب الانتقائي', 
           'advanced', 4.0, 7
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 8);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 9, 'Reactions doxydo-reduction', 'تفاعلات الأكسدة والاختزال', 
           'Piles, electrolyse, reactions spontanees', 'الخلايا، التحليل الكهربائي، التفاعلات التلقائية', 
           'advanced', 4.0, 8
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 9);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 10, 'Notion de champs', 'مفهوم المجالات', 
           'Champ gravitationnel, champ electrique', 'المجال الثقالي، المجال الكهربائي', 
           'intermediate', 3.0, 9
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 10);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 11, 'Force de Lorentz', 'قوة لورنتز', 
           'Mouvement dune charge dans B uniforme', 'حركة الشحنة في مجال منتظم', 
           'advanced', 4.0, 10
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 11);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 12, 'Lois de Newton', 'قوانين نيوتن', 
           'Principe dinertie, action-reaction', 'مبدأ القصور الذاتي، الفعل ورد الفعل', 
           'intermediate', 3.0, 11
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 12);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 13, 'Satellites et planetes', 'الأقمار والكواكب', 
           'Mouvement circulaire uniforme, energie', 'الحركة الدائرية المنتظمة، الطاقة', 
           'advanced', 4.0, 12
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 13);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 14, 'Oscillateurs mecaniques', 'المتذبذبات الميكانيكية', 
           'Pendule simple, oscillations amorties', 'البندول البسيط، التذبذبات المضعفة', 
           'advanced', 4.0, 13
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 14);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), phys_id, 15, 'Ondes mecaniques stationnaires', 'الأمواج الميكانيكية القائمة', 
           'Cordes vibrantes, tubes sonores', 'الأوتار المهتزة، الأنابيب الصوتية', 
           'advanced', 4.0, 14
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = phys_id AND chapter_number = 15);

END $$;

-- Insert Chemistry chapters
DO $$
DECLARE
    chem_id UUID;
BEGIN
    -- Get Chimie subject ID
    SELECT id INTO chem_id FROM subjects WHERE name_fr = 'Chimie';
    
    IF chem_id IS NULL THEN
        RAISE EXCEPTION 'Subject Chimie not found';
    END IF;

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 1, 'Transformations lentes et transformations rapides', 'التحولات البطيئة والتحولات السريعة', 
           'Facteurs cinetiques, catalyse, suivi dune reaction', 'العوامل الحركية، الحفز، تتبع تفاعل', 
           'beginner', 2.0, 0
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 1);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 2, 'Suivi temporel dune transformation chimique - Vitesse de reaction', 'التتبع الزمني لتحول كيميائي - سرعة التفاعل', 
           'Vitesse volumique, temps de demi-reaction, methodes de suivi', 'السرعة الحجمية، زمن نصف التفاعل، طرق التتبع', 
           'intermediate', 3.0, 1
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 2);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 3, 'Decroissance radioactive', 'التناقص الإشعاعي', 
           'Radioactivite, loi de decroissance, demi-vie, activite', 'النشاط الإشعاعي، قانون التناقص، عمر النصف، النشاط', 
           'intermediate', 3.0, 2
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 3);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 4, 'Noyaux, masse et energie', 'النوى والكتلة والطاقة', 
           'Equivalence masse-energie, energie de liaison, fission et fusion', 'تكافؤ الكتلة والطاقة، طاقة الربط، الانشطار والاندماج', 
           'intermediate', 3.0, 3
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 4);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 5, 'Transformations chimiques seffectuant dans les 2 sens', 'التحولات الكيميائية التي تتم في المنحيين', 
           'Reaction incomplete, quotient de reaction, avancement final', 'التفاعل غير التام، حاصل التفاعل، التقدم النهائي', 
           'intermediate', 3.0, 4
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 5);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 6, 'Evolution spontanee dun systeme chimique', 'التطور التلقائي للنظام الكيميائي', 
           'Critere devolution, constante dequilibre', 'معيار التطور، ثابت التوازن', 
           'advanced', 4.0, 5
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 6);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 7, 'Evolution dun systeme chimique vers lequilibre', 'تطور النظام الكيميائي نحو التوازن', 
           'Quotient de reaction, sens devolution', 'حاصل التفاعل، اتجاه التطور', 
           'advanced', 4.0, 6
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 7);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 8, 'Reactions acido-basiques', 'تفاعلات الأحماض والقواعد', 
           'Couples acide/base, pH, dosage', 'أزواج الحمض/القاعدة، الأس الهيدروجيني، المعايرة', 
           'intermediate', 3.0, 7
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 8);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 9, 'Reactions de precipitation', 'تفاعلات الترسيب', 
           'Produit de solubilite Ks, precipitation selective', 'حاصل الذوبان، الترسيب الانتقائي', 
           'advanced', 4.0, 8
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 9);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 10, 'Piles electrochimiques', 'الخلايا الكهروكيميائية', 
           'Pile Daniell, force electromotrice', 'خلية دانييل، القوة الدافعة الكهربائية', 
           'advanced', 4.0, 9
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 10);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 11, 'Electrolyse', 'التحليل الكهربائي', 
           'Electrolyse forcee, loi de Faraday', 'التحليل الكهربائي القسري، قانون فاراداي', 
           'advanced', 4.0, 10
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 11);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 12, 'Esterification et hydrolyse', 'الإسترة والتحلل المائي', 
           'Equilibre chimique, cinetique', 'التوازن الكيميائي، الحركية', 
           'intermediate', 3.0, 11
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 12);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 13, 'Controle de levolution dun systeme chimique', 'التحكم في تطور النظام الكيميائي', 
           'Modification des conditions dequilibre', 'تعديل شروط التوازن', 
           'advanced', 4.0, 12
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 13);

    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, difficulty_level, estimated_hours, order_index)
    SELECT gen_random_uuid(), chem_id, 14, 'Phenomenes oxydo-reductions', 'ظواهر الأكسدة والاختزال', 
           'Transfert delectrons, piles', 'انتقال الإلكترونات، الخلايا', 
           'intermediate', 3.0, 13
    WHERE NOT EXISTS (SELECT 1 FROM chapters WHERE subject_id = chem_id AND chapter_number = 14);

END $$;

-- Verify the insertions
SELECT s.name_fr as subject, COUNT(c.id) as chapter_count 
FROM subjects s 
LEFT JOIN chapters c ON s.id = c.subject_id 
GROUP BY s.id, s.name_fr 
ORDER BY chapter_count DESC;
