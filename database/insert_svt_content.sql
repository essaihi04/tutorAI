-- Contenu SVT pour 2ème BAC Sciences Physiques BIOF
-- Programme officiel marocain
-- À exécuter dans le SQL Editor de Supabase Dashboard

-- 1. Récupérer l'ID de la matière SVT
DO $$
DECLARE
    svt_subject_id UUID;
    chapter1_id UUID;
    chapter2_id UUID;
    chapter3_id UUID;
    chapter4_id UUID;
    lesson_id UUID;
BEGIN
    -- Récupérer l'ID de SVT
    SELECT id INTO svt_subject_id FROM subjects WHERE name_fr = 'Sciences de la Vie et de la Terre (SVT)' LIMIT 1;
    
    IF svt_subject_id IS NULL THEN
        RAISE EXCEPTION 'Matière SVT non trouvée. Exécutez d''abord clean_subjects.sql';
    END IF;

    -- ============================================================
    -- CHAPITRE 1: Consommation de la matière organique et flux d'énergie
    -- ============================================================
    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, estimated_hours, order_index)
    VALUES (
        gen_random_uuid(),
        svt_subject_id,
        1,
        'Consommation de la matière organique et flux d''énergie',
        'استهلاك المادة العضوية وتدفق الطاقة',
        'Étude de la libération de l''énergie emmagasinée dans la matière organique et le rôle du muscle strié squelettique',
        'دراسة تحرير الطاقة المخزنة في المادة العضوية ودور العضلة المخططة الهيكلية',
        12.0,
        1
    ) RETURNING id INTO chapter1_id;

    -- Leçon 1.1: Libération de l'énergie
    INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
    VALUES (
        gen_random_uuid(),
        chapter1_id,
        'Libération de l''énergie emmagasinée dans la matière organique',
        'تحرير الطاقة المخزنة في المادة العضوية',
        'theory',
        jsonb_build_object(
            'sections', jsonb_build_array(
                jsonb_build_object(
                    'title', 'Introduction',
                    'content', 'La matière organique (glucose) est la source d''énergie pour les cellules. Cette énergie est libérée par des réactions métaboliques.',
                    'type', 'text',
                    'resources', jsonb_build_array(
                        jsonb_build_object('kind', 'definition', 'title', 'Définition de la matière organique', 'description', 'Carte de définition sur la matière organique et son rôle énergétique.', 'trigger', 'definition introduction', 'phase', 'activation'),
                        jsonb_build_object('kind', 'image', 'title', 'Vue d''ensemble des voies énergétiques', 'description', 'Schéma global des voies de dégradation du glucose.', 'url', '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/introduction/vue_ensemble_voies_energetiques.svg', 'trigger', 'montre vue ensemble energie', 'phase', 'activation')
                    )
                ),
                jsonb_build_object(
                    'title', 'La glycolyse',
                    'content', 'Première étape de dégradation du glucose dans le cytoplasme. Produit 2 ATP et 2 pyruvates.',
                    'type', 'definition',
                    'resources', jsonb_build_array(
                        jsonb_build_object('kind', 'image', 'title', 'Schéma de la glycolyse', 'description', 'Illustration des étapes essentielles de la glycolyse.', 'url', '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/glycolyse/schema_glycolyse.svg', 'trigger', 'regarde ce schéma glycolyse', 'phase', 'explanation'),
                        jsonb_build_object('kind', 'exercise', 'title', 'Exercice glycolyse', 'description', 'Question de vérification sur le lieu et le bilan de la glycolyse.', 'trigger', 'propose exercice glycolyse', 'phase', 'application'),
                        jsonb_build_object('kind', 'evaluation', 'title', 'Mini-évaluation glycolyse', 'description', 'Évaluation rapide sur les produits de la glycolyse.', 'trigger', 'evaluation glycolyse', 'phase', 'consolidation')
                    )
                ),
                jsonb_build_object(
                    'title', 'La respiration cellulaire',
                    'content', 'Oxydation complète du glucose dans les mitochondries en présence d''O2. Produit 36-38 ATP.',
                    'type', 'definition',
                    'resources', jsonb_build_array(
                        jsonb_build_object('kind', 'image', 'title', 'Cycle de Krebs et chaîne respiratoire', 'description', 'Schéma de la respiration cellulaire mitochondriale.', 'url', '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/cycle_krebs_chaine_respiratoire.svg', 'trigger', 'observe cette image respiration', 'phase', 'explanation'),
                        jsonb_build_object('kind', 'simulation', 'title', 'Simulation respiration cellulaire', 'description', 'Simulation interactive sur la production d''ATP en présence d''oxygène.', 'url', '/media/simulations/svt/ch1_consommation_matiere_organique/respiration/index.html', 'trigger', 'lance simulation respiration', 'phase', 'exploration'),
                        jsonb_build_object('kind', 'national_exam', 'title', 'Examen national respiration', 'description', 'Extrait d''un exercice type examen national sur le rendement énergétique.', 'url', '/media/exams/svt/ch1_consommation_matiere_organique/respiration/examen_national_2022.md', 'trigger', 'montre examen national respiration', 'phase', 'application')
                    )
                ),
                jsonb_build_object(
                    'title', 'La fermentation',
                    'content', 'Dégradation incomplète du glucose en absence d''O2. Produit 2 ATP (fermentation lactique ou alcoolique).',
                    'type', 'definition',
                    'resources', jsonb_build_array(
                        jsonb_build_object('kind', 'image', 'title', 'Comparaison respiration et fermentation', 'description', 'Tableau comparatif des deux voies métaboliques.', 'url', '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/fermentation/comparaison_respiration_fermentation.svg', 'trigger', 'compare respiration fermentation', 'phase', 'explanation'),
                        jsonb_build_object('kind', 'video', 'title', 'Vidéo fermentation', 'description', 'Vidéo courte expliquant la fermentation lactique et alcoolique.', 'url', '/media/videos/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/fermentation/video_fermentation.mp4', 'trigger', 'regarde video fermentation', 'phase', 'exploration'),
                        jsonb_build_object('kind', 'definition', 'title', 'Définition fermentation', 'description', 'Fiche de définition de la fermentation.', 'trigger', 'definition fermentation', 'phase', 'consolidation')
                    )
                )
            ),
            'key_concepts', jsonb_build_array('glycolyse', 'respiration', 'fermentation', 'ATP', 'mitochondrie')
        ),
        jsonb_build_array(
            'Comprendre les étapes de la glycolyse',
            'Distinguer respiration et fermentation',
            'Calculer le bilan énergétique de chaque voie métabolique'
        ),
        90,
        1,
        jsonb_build_array(
            jsonb_build_object('type', 'simulation', 'url', '/media/simulations/svt/ch1_consommation_matiere_organique/respiration/index.html', 'title', 'Simulation respiration cellulaire', 'trigger', 'lance simulation respiration'),
            jsonb_build_object('type', 'image', 'url', '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/glycolyse/schema_glycolyse.svg', 'caption', 'Schéma de la glycolyse', 'trigger', 'regarde ce schéma glycolyse'),
            jsonb_build_object('type', 'image', 'url', '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/cycle_krebs_chaine_respiratoire.svg', 'caption', 'Cycle de Krebs et chaîne respiratoire', 'trigger', 'observe cette image respiration')
        )
    ) RETURNING id INTO lesson_id;

    INSERT INTO lesson_resources (lesson_id, section_title, resource_type, title, description, file_path, trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
    VALUES
        (lesson_id, 'Introduction', 'definition', 'Définition de la matière organique', 'Carte de définition sur la matière organique et son rôle énergétique.', NULL, 'definition introduction', 'activation', 'beginner', jsonb_build_array('matière organique', 'énergie'), jsonb_build_object('kind', 'definition_card'), 1),
        (lesson_id, 'Introduction', 'image', 'Vue d''ensemble des voies énergétiques', 'Schéma global des voies de dégradation du glucose.', '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/introduction/vue_ensemble_voies_energetiques.svg', 'montre vue ensemble energie', 'activation', 'beginner', jsonb_build_array('glucose', 'ATP', 'voies énergétiques'), jsonb_build_object('caption', 'Vue d''ensemble des voies énergétiques'), 2),
        (lesson_id, 'La glycolyse', 'image', 'Schéma de la glycolyse', 'Illustration des étapes essentielles de la glycolyse.', '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/glycolyse/schema_glycolyse.svg', 'regarde ce schéma glycolyse', 'explanation', 'beginner', jsonb_build_array('glycolyse', 'ATP', 'cytoplasme'), jsonb_build_object('caption', 'Schéma de la glycolyse'), 3),
        (lesson_id, 'La glycolyse', 'evaluation', 'Mini-évaluation glycolyse', 'Évaluation rapide sur les produits de la glycolyse.', NULL, 'evaluation glycolyse', 'consolidation', 'beginner', jsonb_build_array('glycolyse', 'pyruvate', 'ATP'), jsonb_build_object('format', 'quiz_rapide'), 4),
        (lesson_id, 'La respiration cellulaire', 'image', 'Cycle de Krebs et chaîne respiratoire', 'Schéma de la respiration cellulaire mitochondriale.', '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/cycle_krebs_chaine_respiratoire.svg', 'observe cette image respiration', 'explanation', 'intermediate', jsonb_build_array('respiration', 'mitochondrie', 'ATP'), jsonb_build_object('caption', 'Cycle de Krebs et chaîne respiratoire'), 5),
        (lesson_id, 'La respiration cellulaire', 'simulation', 'Simulation respiration cellulaire', 'Simulation interactive sur la production d''ATP en présence d''oxygène.', '/media/simulations/svt/ch1_consommation_matiere_organique/respiration/index.html', 'lance simulation respiration', 'exploration', 'intermediate', jsonb_build_array('respiration', 'oxygène', 'ATP'), jsonb_build_object('caption', 'Simulation respiration cellulaire'), 6),
        (lesson_id, 'La respiration cellulaire', 'exam', 'Examen national respiration', 'Extrait type examen national sur le rendement énergétique.', '/media/exams/svt/ch1_consommation_matiere_organique/respiration/examen_national_2022.md', 'montre examen national respiration', 'application', 'advanced', jsonb_build_array('respiration', 'rendement énergétique'), jsonb_build_object('year', 2022), 7),
        (lesson_id, 'La fermentation', 'image', 'Comparaison respiration et fermentation', 'Tableau comparatif des deux voies métaboliques.', '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/fermentation/comparaison_respiration_fermentation.svg', 'compare respiration fermentation', 'explanation', 'intermediate', jsonb_build_array('fermentation', 'respiration', 'ATP'), jsonb_build_object('caption', 'Comparaison respiration et fermentation'), 8),
        (lesson_id, 'La fermentation', 'video', 'Vidéo fermentation', 'Vidéo courte expliquant la fermentation lactique et alcoolique.', '/media/videos/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/fermentation/video_fermentation.mp4', 'regarde video fermentation', 'exploration', 'intermediate', jsonb_build_array('fermentation lactique', 'fermentation alcoolique'), jsonb_build_object('duration_seconds', 90), 9);

    -- Exercices pour Leçon 1.1
    -- Niveau Beginner
    INSERT INTO exercises (lesson_id, question_text_fr, question_text_ar, question_type, difficulty_tier, options, correct_answer, explanation_fr, explanation_ar, hints, estimated_time_seconds, order_index)
    VALUES (
        lesson_id,
        'Où se déroule la glycolyse dans la cellule ?',
        'أين تحدث تحلل السكر في الخلية؟',
        'qcm',
        'beginner',
        jsonb_build_array(
            jsonb_build_object('id', 'A', 'text', 'Dans le cytoplasme'),
            jsonb_build_object('id', 'B', 'text', 'Dans la mitochondrie'),
            jsonb_build_object('id', 'C', 'text', 'Dans le noyau'),
            jsonb_build_object('id', 'D', 'text', 'Dans le réticulum endoplasmique')
        ),
        jsonb_build_object('answer', 'A'),
        'La glycolyse se déroule dans le cytoplasme de la cellule, c''est la première étape de dégradation du glucose.',
        'يحدث تحلل السكر في السيتوبلازم',
        jsonb_build_array(
            jsonb_build_object('level', 1, 'text', 'La glycolyse ne nécessite pas d''organite spécialisé'),
            jsonb_build_object('level', 2, 'text', 'Elle se passe avant l''entrée dans la mitochondrie')
        ),
        60,
        1
    );

    INSERT INTO exercises (lesson_id, question_text_fr, question_text_ar, question_type, difficulty_tier, options, correct_answer, explanation_fr, explanation_ar, hints, estimated_time_seconds, order_index)
    VALUES (
        lesson_id,
        'Combien d''ATP sont produits par la glycolyse ?',
        'كم عدد جزيئات ATP المنتجة من تحلل السكر؟',
        'numeric',
        'beginner',
        NULL,
        jsonb_build_object('value', 2, 'tolerance', 0),
        'La glycolyse produit un bilan net de 2 ATP par molécule de glucose.',
        'ينتج تحلل السكر 2 ATP',
        jsonb_build_array(
            jsonb_build_object('level', 1, 'text', 'C''est un petit nombre'),
            jsonb_build_object('level', 2, 'text', 'Moins de 5 ATP')
        ),
        90,
        2
    );

    -- Niveau Intermediate
    INSERT INTO exercises (lesson_id, question_text_fr, question_text_ar, question_type, difficulty_tier, options, correct_answer, explanation_fr, explanation_ar, hints, estimated_time_seconds, order_index)
    VALUES (
        lesson_id,
        'Comparez le rendement énergétique de la respiration et de la fermentation',
        'قارن بين الإنتاجية الطاقية للتنفس والتخمر',
        'open',
        'intermediate',
        NULL,
        jsonb_build_object('keywords', jsonb_build_array('36-38 ATP', '2 ATP', 'oxygène', 'rendement')),
        'La respiration produit 36-38 ATP (avec O2) tandis que la fermentation ne produit que 2 ATP (sans O2). La respiration est donc beaucoup plus efficace énergétiquement.',
        'التنفس ينتج 36-38 ATP بينما التخمر ينتج فقط 2 ATP',
        jsonb_build_array(
            jsonb_build_object('level', 1, 'text', 'Pensez à la présence ou absence d''oxygène'),
            jsonb_build_object('level', 2, 'text', 'Comparez les bilans en ATP'),
            jsonb_build_object('level', 3, 'text', 'La respiration est environ 18 fois plus efficace')
        ),
        180,
        3
    );

    -- Leçon 1.2: Rôle du muscle strié squelettique
    INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
    VALUES (
        gen_random_uuid(),
        chapter1_id,
        'Rôle du muscle strié squelettique dans la conversion de l''énergie',
        'دور العضلة المخططة الهيكلية في تحويل الطاقة',
        'theory',
        jsonb_build_object(
            'sections', jsonb_build_array(
                jsonb_build_object(
                    'title', 'Structure du muscle',
                    'content', 'Le muscle strié est composé de fibres musculaires contenant des myofibrilles avec des sarcomères.',
                    'type', 'text',
                    'resources', jsonb_build_array(
                        jsonb_build_object('kind', 'image', 'title', 'Structure du sarcomère', 'description', 'Schéma annoté du sarcomère.', 'url', '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/schema_sarcomere.svg', 'trigger', 'montre structure sarcomere', 'phase', 'explanation'),
                        jsonb_build_object('kind', 'definition', 'title', 'Définition du sarcomère', 'description', 'Fiche de définition du sarcomère et des myofibrilles.', 'trigger', 'definition sarcomere', 'phase', 'activation')
                    )
                ),
                jsonb_build_object(
                    'title', 'Contraction musculaire',
                    'content', 'La contraction résulte du glissement des filaments d''actine et de myosine, nécessitant de l''ATP.',
                    'type', 'definition',
                    'resources', jsonb_build_array(
                        jsonb_build_object('kind', 'simulation', 'title', 'Animation de la contraction musculaire', 'description', 'Animation interactive du glissement actine-myosine.', 'url', '/media/simulations/svt/ch1_consommation_matiere_organique/muscle/contraction/index.html', 'trigger', 'lance simulation contraction musculaire', 'phase', 'exploration'),
                        jsonb_build_object('kind', 'video', 'title', 'Vidéo contraction musculaire', 'description', 'Vidéo courte montrant les étapes de la contraction.', 'url', '/media/videos/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/contraction/video_contraction_musculaire.mp4', 'trigger', 'video contraction musculaire', 'phase', 'explanation'),
                        jsonb_build_object('kind', 'exercise', 'title', 'Exercice contraction musculaire', 'description', 'Exercice sur le rôle de l''ATP dans la contraction.', 'trigger', 'exercice contraction musculaire', 'phase', 'application')
                    )
                ),
                jsonb_build_object(
                    'title', 'Métabolisme énergétique',
                    'content', 'Le muscle utilise la créatine phosphate, la glycolyse et la respiration selon l''intensité de l''effort.',
                    'type', 'definition',
                    'resources', jsonb_build_array(
                        jsonb_build_object('kind', 'image', 'title', 'Sources d''énergie musculaire', 'description', 'Schéma des filières énergétiques du muscle.', 'url', '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/metabolisme/sources_energie_musculaire.svg', 'trigger', 'montre sources energie musculaire', 'phase', 'explanation'),
                        jsonb_build_object('kind', 'evaluation', 'title', 'Évaluation filières énergétiques', 'description', 'Évaluation sur les sources d''énergie selon le type d''effort.', 'trigger', 'evaluation filieres energetiques', 'phase', 'consolidation'),
                        jsonb_build_object('kind', 'national_exam', 'title', 'Examen national muscle', 'description', 'Extrait type examen sur la conversion d''énergie par le muscle.', 'url', '/media/exams/svt/ch1_consommation_matiere_organique/muscle/examen_national_muscle_2021.md', 'trigger', 'montre examen national muscle', 'phase', 'application')
                    )
                )
            ),
            'key_concepts', jsonb_build_array('sarcomère', 'actine', 'myosine', 'ATP', 'créatine phosphate')
        ),
        jsonb_build_array(
            'Décrire la structure du muscle strié',
            'Expliquer le mécanisme de la contraction',
            'Identifier les sources d''énergie selon le type d''effort'
        ),
        90,
        2,
        jsonb_build_array(
            jsonb_build_object('type', 'image', 'url', '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/schema_sarcomere.svg', 'caption', 'Structure du sarcomère', 'trigger', 'montre structure sarcomere'),
            jsonb_build_object('type', 'simulation', 'url', '/media/simulations/svt/ch1_consommation_matiere_organique/muscle/contraction/index.html', 'title', 'Animation de la contraction musculaire', 'trigger', 'lance simulation contraction musculaire'),
            jsonb_build_object('type', 'video', 'url', '/media/videos/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/contraction/video_contraction_musculaire.mp4', 'title', 'Vidéo contraction musculaire', 'trigger', 'video contraction musculaire')
        )
    );

    INSERT INTO lesson_resources (lesson_id, section_title, resource_type, title, description, file_path, trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
    VALUES
        (lesson_id, 'Structure du muscle', 'image', 'Structure du sarcomère', 'Schéma annoté du sarcomère.', '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/schema_sarcomere.svg', 'montre structure sarcomere', 'explanation', 'beginner', jsonb_build_array('sarcomère', 'myofibrille'), jsonb_build_object('caption', 'Structure du sarcomère'), 1),
        (lesson_id, 'Structure du muscle', 'definition', 'Définition du sarcomère', 'Fiche de définition du sarcomère et des myofibrilles.', NULL, 'definition sarcomere', 'activation', 'beginner', jsonb_build_array('sarcomère', 'fibre musculaire'), jsonb_build_object('kind', 'definition_card'), 2),
        (lesson_id, 'Contraction musculaire', 'simulation', 'Animation de la contraction musculaire', 'Animation interactive du glissement actine-myosine.', '/media/simulations/svt/ch1_consommation_matiere_organique/muscle/contraction/index.html', 'lance simulation contraction musculaire', 'exploration', 'intermediate', jsonb_build_array('actine', 'myosine', 'ATP'), jsonb_build_object('caption', 'Animation de la contraction musculaire'), 3),
        (lesson_id, 'Contraction musculaire', 'video', 'Vidéo contraction musculaire', 'Vidéo courte montrant les étapes de la contraction.', '/media/videos/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/contraction/video_contraction_musculaire.mp4', 'video contraction musculaire', 'explanation', 'intermediate', jsonb_build_array('contraction musculaire', 'ATP'), jsonb_build_object('duration_seconds', 75), 4),
        (lesson_id, 'Contraction musculaire', 'exercise', 'Exercice contraction musculaire', 'Exercice sur le rôle de l''ATP dans la contraction.', NULL, 'exercice contraction musculaire', 'application', 'intermediate', jsonb_build_array('ATP', 'contraction musculaire'), jsonb_build_object('format', 'question_ouverte'), 5),
        (lesson_id, 'Métabolisme énergétique', 'image', 'Sources d''énergie musculaire', 'Schéma des filières énergétiques du muscle.', '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/metabolisme/sources_energie_musculaire.svg', 'montre sources energie musculaire', 'explanation', 'intermediate', jsonb_build_array('créatine phosphate', 'glycolyse', 'respiration'), jsonb_build_object('caption', 'Sources d''énergie musculaire'), 6),
        (lesson_id, 'Métabolisme énergétique', 'evaluation', 'Évaluation filières énergétiques', 'Évaluation sur les sources d''énergie selon le type d''effort.', NULL, 'evaluation filieres energetiques', 'consolidation', 'intermediate', jsonb_build_array('effort musculaire', 'filières énergétiques'), jsonb_build_object('format', 'quiz_rapide'), 7),
        (lesson_id, 'Métabolisme énergétique', 'exam', 'Examen national muscle', 'Extrait type examen sur la conversion d''énergie par le muscle.', '/media/exams/svt/ch1_consommation_matiere_organique/muscle/examen_national_muscle_2021.md', 'montre examen national muscle', 'application', 'advanced', jsonb_build_array('muscle strié', 'conversion énergie'), jsonb_build_object('year', 2021), 8);

    -- ============================================================
    -- CHAPITRE 2: Nature et mécanisme de l'expression du matériel génétique
    -- ============================================================
    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, estimated_hours, order_index)
    VALUES (
        gen_random_uuid(),
        svt_subject_id,
        2,
        'Nature et mécanisme de l''expression du matériel génétique',
        'طبيعة وآلية التعبير عن المادة الوراثية',
        'Étude de l''information génétique, son expression et son transfert lors de la reproduction',
        'دراسة المعلومة الوراثية وتعبيرها ونقلها أثناء التكاثر',
        15.0,
        2
    ) RETURNING id INTO chapter2_id;

    -- Leçon 2.1: Notion de l'information génétique
    INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
    VALUES (
        gen_random_uuid(),
        chapter2_id,
        'Notion de l''information génétique',
        'مفهوم المعلومة الوراثية',
        'theory',
        jsonb_build_object(
            'sections', jsonb_build_array(
                jsonb_build_object(
                    'title', 'L''ADN, support de l''information génétique',
                    'content', 'L''ADN est une double hélice composée de nucléotides (A, T, G, C). Il porte les gènes.',
                    'type', 'definition'
                ),
                jsonb_build_object(
                    'title', 'La réplication de l''ADN',
                    'content', 'Processus semi-conservatif permettant la duplication de l''ADN avant la division cellulaire.',
                    'type', 'definition'
                ),
                jsonb_build_object(
                    'title', 'La mitose',
                    'content', 'Division cellulaire assurant la conservation du nombre de chromosomes (2n → 2n).',
                    'type', 'definition'
                )
            ),
            'key_concepts', jsonb_build_array('ADN', 'nucléotide', 'réplication', 'mitose', 'chromosome'),
            'formulas', jsonb_build_array(
                jsonb_build_object('name', 'Complémentarité des bases', 'text', 'A-T et G-C')
            )
        ),
        jsonb_build_array(
            'Décrire la structure de l''ADN',
            'Expliquer le mécanisme de réplication',
            'Schématiser les phases de la mitose'
        ),
        120,
        1,
        jsonb_build_array(
            jsonb_build_object('type', 'image', 'caption', 'Structure de l''ADN'),
            jsonb_build_object('type', 'simulation', 'title', 'Simulation de la réplication'),
            jsonb_build_object('type', 'image', 'caption', 'Les phases de la mitose')
        )
    );

    -- Leçon 2.2: Expression de l'information génétique
    INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
    VALUES (
        gen_random_uuid(),
        chapter2_id,
        'Expression de l''information génétique',
        'التعبير عن المعلومة الوراثية',
        'theory',
        jsonb_build_object(
            'sections', jsonb_build_array(
                jsonb_build_object(
                    'title', 'La transcription',
                    'content', 'Synthèse de l''ARN messager à partir de l''ADN dans le noyau.',
                    'type', 'definition'
                ),
                jsonb_build_object(
                    'title', 'La traduction',
                    'content', 'Synthèse des protéines à partir de l''ARNm dans les ribosomes.',
                    'type', 'definition'
                ),
                jsonb_build_object(
                    'title', 'Le code génétique',
                    'content', 'Correspondance entre les codons (triplets de nucléotides) et les acides aminés.',
                    'type', 'definition'
                )
            ),
            'key_concepts', jsonb_build_array('transcription', 'traduction', 'ARNm', 'codon', 'ribosome')
        ),
        jsonb_build_array(
            'Expliquer la transcription et la traduction',
            'Utiliser le code génétique',
            'Relier gène et protéine'
        ),
        120,
        2,
        jsonb_build_array(
            jsonb_build_object('type', 'image', 'caption', 'Schéma transcription-traduction'),
            jsonb_build_object('type', 'image', 'caption', 'Tableau du code génétique')
        )
    );

    -- Leçon 2.3: Transfert de l'information génétique (Méiose)
    INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
    VALUES (
        gen_random_uuid(),
        chapter2_id,
        'Transfert de l''information génétique - La méiose',
        'نقل المعلومة الوراثية - الانقسام الاختزالي',
        'theory',
        jsonb_build_object(
            'sections', jsonb_build_array(
                jsonb_build_object(
                    'title', 'La méiose',
                    'content', 'Division réductionnelle produisant 4 cellules haploïdes (n) à partir d''une cellule diploïde (2n).',
                    'type', 'definition'
                ),
                jsonb_build_object(
                    'title', 'Brassage génétique',
                    'content', 'La méiose assure le brassage interchromosomique (anaphase I) et intrachromosomique (crossing-over).',
                    'type', 'definition'
                )
            ),
            'key_concepts', jsonb_build_array('méiose', 'haploïde', 'brassage', 'crossing-over', 'gamètes')
        ),
        jsonb_build_array(
            'Distinguer mitose et méiose',
            'Expliquer le brassage génétique',
            'Calculer les combinaisons possibles'
        ),
        120,
        3,
        jsonb_build_array(
            jsonb_build_object('type', 'image', 'caption', 'Les phases de la méiose'),
            jsonb_build_object('type', 'simulation', 'title', 'Animation du crossing-over')
        )
    );

    -- ============================================================
    -- CHAPITRE 3: Utilisation des matières organiques et inorganiques
    -- ============================================================
    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, estimated_hours, order_index)
    VALUES (
        gen_random_uuid(),
        svt_subject_id,
        3,
        'Utilisation des matières organiques et inorganiques',
        'استعمال المواد العضوية وغير العضوية',
        'Impact environnemental de l''utilisation des matières et solutions durables',
        'الأثر البيئي لاستعمال المواد والحلول المستدامة',
        10.0,
        3
    ) RETURNING id INTO chapter3_id;

    -- Leçon 3.1: Les ordures ménagères
    INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
    VALUES (
        gen_random_uuid(),
        chapter3_id,
        'Les ordures ménagères',
        'النفايات المنزلية',
        'theory',
        jsonb_build_object(
            'sections', jsonb_build_array(
                jsonb_build_object(
                    'title', 'Types d''ordures',
                    'content', 'Ordures organiques (biodégradables) et inorganiques (plastiques, métaux, verre).',
                    'type', 'text'
                ),
                jsonb_build_object(
                    'title', 'Gestion des déchets',
                    'content', 'Tri sélectif, recyclage, compostage, valorisation énergétique.',
                    'type', 'definition'
                )
            ),
            'key_concepts', jsonb_build_array('déchets', 'recyclage', 'compostage', 'biodégradable')
        ),
        jsonb_build_array(
            'Classifier les types de déchets',
            'Proposer des solutions de gestion',
            'Comprendre l''importance du recyclage'
        ),
        60,
        1,
        jsonb_build_array(
            jsonb_build_object('type', 'image', 'caption', 'Tri sélectif des déchets')
        )
    );

    -- Leçon 3.2: Pollution des milieux naturels
    INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
    VALUES (
        gen_random_uuid(),
        chapter3_id,
        'La pollution des milieux naturels',
        'تلوث الأوساط الطبيعية',
        'theory',
        jsonb_build_object(
            'sections', jsonb_build_array(
                jsonb_build_object(
                    'title', 'Pollution de l''air',
                    'content', 'Émissions de CO2, effet de serre, pluies acides.',
                    'type', 'text'
                ),
                jsonb_build_object(
                    'title', 'Pollution de l''eau',
                    'content', 'Eutrophisation, métaux lourds, pesticides.',
                    'type', 'text'
                ),
                jsonb_build_object(
                    'title', 'Solutions',
                    'content', 'Énergies renouvelables, traitement des eaux, agriculture biologique.',
                    'type', 'definition'
                )
            ),
            'key_concepts', jsonb_build_array('pollution', 'effet de serre', 'eutrophisation', 'énergies renouvelables')
        ),
        jsonb_build_array(
            'Identifier les types de pollution',
            'Expliquer leurs conséquences',
            'Proposer des solutions durables'
        ),
        90,
        2,
        jsonb_build_array(
            jsonb_build_object('type', 'image', 'caption', 'Sources de pollution'),
            jsonb_build_object('type', 'image', 'caption', 'Énergies renouvelables')
        )
    );

    -- Leçon 3.3: Énergie nucléaire
    INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
    VALUES (
        gen_random_uuid(),
        chapter3_id,
        'Les matières radioactives et l''énergie nucléaire',
        'المواد المشعة والطاقة النووية',
        'theory',
        jsonb_build_object(
            'sections', jsonb_build_array(
                jsonb_build_object(
                    'title', 'Radioactivité',
                    'content', 'Désintégration naturelle de noyaux instables émettant des rayonnements.',
                    'type', 'definition'
                ),
                jsonb_build_object(
                    'title', 'Énergie nucléaire',
                    'content', 'Fission nucléaire dans les centrales. Avantages et risques.',
                    'type', 'text'
                )
            ),
            'key_concepts', jsonb_build_array('radioactivité', 'fission', 'centrale nucléaire', 'déchets radioactifs')
        ),
        jsonb_build_array(
            'Comprendre la radioactivité',
            'Évaluer avantages et inconvénients du nucléaire',
            'Connaître les précautions de sécurité'
        ),
        90,
        3,
        jsonb_build_array(
            jsonb_build_object('type', 'image', 'caption', 'Centrale nucléaire')
        )
    );

    -- ============================================================
    -- CHAPITRE 4: Géologie - Formation des chaînes de montagnes
    -- ============================================================
    INSERT INTO chapters (id, subject_id, chapter_number, title_fr, title_ar, description_fr, description_ar, estimated_hours, order_index)
    VALUES (
        gen_random_uuid(),
        svt_subject_id,
        4,
        'Les phénomènes géologiques et la tectonique des plaques',
        'الظواهر الجيولوجية وتكتونية الصفائح',
        'Formation des chaînes de montagnes et leur relation avec la tectonique des plaques',
        'تكون السلاسل الجبلية وعلاقتها بتكتونية الصفائح',
        12.0,
        4
    ) RETURNING id INTO chapter4_id;

    -- Leçon 4.1: Tectonique des plaques
    INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
    VALUES (
        gen_random_uuid(),
        chapter4_id,
        'Les chaînes de montagnes et la tectonique des plaques',
        'السلاسل الجبلية وتكتونية الصفائح',
        'theory',
        jsonb_build_object(
            'sections', jsonb_build_array(
                jsonb_build_object(
                    'title', 'Subduction',
                    'content', 'Plongement d''une plaque océanique sous une plaque continentale. Formation de chaînes de type andin.',
                    'type', 'definition'
                ),
                jsonb_build_object(
                    'title', 'Collision',
                    'content', 'Collision de deux plaques continentales. Formation de chaînes de type himalayen.',
                    'type', 'definition'
                ),
                jsonb_build_object(
                    'title', 'Obduction',
                    'content', 'Chevauchement d''une portion de lithosphère océanique sur une marge continentale.',
                    'type', 'definition'
                )
            ),
            'key_concepts', jsonb_build_array('subduction', 'collision', 'obduction', 'tectonique', 'lithosphère')
        ),
        jsonb_build_array(
            'Distinguer les types de chaînes de montagnes',
            'Expliquer les mécanismes de formation',
            'Relier géologie et tectonique des plaques'
        ),
        120,
        1,
        jsonb_build_array(
            jsonb_build_object('type', 'image', 'caption', 'Schéma de subduction'),
            jsonb_build_object('type', 'image', 'caption', 'Collision continentale'),
            jsonb_build_object('type', 'simulation', 'title', 'Animation tectonique des plaques')
        )
    );

    -- Leçon 4.2: Métamorphisme
    INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
    VALUES (
        gen_random_uuid(),
        chapter4_id,
        'Le métamorphisme et sa relation avec la tectonique',
        'التحول وعلاقته بالتكتونية',
        'theory',
        jsonb_build_object(
            'sections', jsonb_build_array(
                jsonb_build_object(
                    'title', 'Définition',
                    'content', 'Transformation des roches à l''état solide sous l''effet de la température et de la pression.',
                    'type', 'definition'
                ),
                jsonb_build_object(
                    'title', 'Types de métamorphisme',
                    'content', 'Métamorphisme de contact (haute T) et métamorphisme régional (haute P et T).',
                    'type', 'text'
                ),
                jsonb_build_object(
                    'title', 'Faciès métamorphiques',
                    'content', 'Schistes verts, amphibolites, éclogites selon les conditions P-T.',
                    'type', 'definition'
                )
            ),
            'key_concepts', jsonb_build_array('métamorphisme', 'faciès', 'pression', 'température', 'roches')
        ),
        jsonb_build_array(
            'Définir le métamorphisme',
            'Identifier les faciès métamorphiques',
            'Relier métamorphisme et contexte géodynamique'
        ),
        90,
        2,
        jsonb_build_array(
            jsonb_build_object('type', 'image', 'caption', 'Diagramme P-T des faciès métamorphiques'),
            jsonb_build_object('type', 'image', 'caption', 'Roches métamorphiques')
        )
    );

    -- Leçon 4.3: Granitisation
    INSERT INTO lessons (id, chapter_id, title_fr, title_ar, lesson_type, content, learning_objectives, duration_minutes, order_index, media_resources)
    VALUES (
        gen_random_uuid(),
        chapter4_id,
        'La granitisation et sa relation avec le métamorphisme',
        'الغرنطة وعلاقتها بالتحول',
        'theory',
        jsonb_build_object(
            'sections', jsonb_build_array(
                jsonb_build_object(
                    'title', 'Formation du granite',
                    'content', 'Fusion partielle de la croûte continentale en profondeur (anatexie).',
                    'type', 'definition'
                ),
                jsonb_build_object(
                    'title', 'Relation avec le métamorphisme',
                    'content', 'Le métamorphisme de haut degré peut conduire à la fusion partielle et la formation de magmas granitiques.',
                    'type', 'text'
                )
            ),
            'key_concepts', jsonb_build_array('granite', 'anatexie', 'fusion partielle', 'magma')
        ),
        jsonb_build_array(
            'Expliquer la formation du granite',
            'Relier granitisation et métamorphisme',
            'Identifier les contextes de granitisation'
        ),
        90,
        3,
        jsonb_build_array(
            jsonb_build_object('type', 'image', 'caption', 'Formation du granite par anatexie')
        )
    );

END $$;

-- Vérifier les données insérées
SELECT 
    s.name_fr as matiere,
    c.chapter_number,
    c.title_fr as chapitre,
    COUNT(l.id) as nombre_lecons
FROM subjects s
JOIN chapters c ON c.subject_id = s.id
LEFT JOIN lessons l ON l.chapter_id = c.id
WHERE s.name_fr = 'Sciences de la Vie et de la Terre (SVT)'
GROUP BY s.name_fr, c.chapter_number, c.title_fr
ORDER BY c.chapter_number;
