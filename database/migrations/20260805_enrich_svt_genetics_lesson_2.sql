-- Enrichit la leçon 2 du chapitre génétique sans recréer les chapitres.
-- Migration idempotente : les ressources sont identifiées par leur titre.

BEGIN;

WITH target AS (
    SELECT l.id
    FROM lessons l
    JOIN chapters c ON c.id = l.chapter_id
    WHERE c.chapter_number = 2
      AND l.order_index = 2
      AND lower(c.title_fr) LIKE '%génétique%'
    ORDER BY l.created_at
    LIMIT 1
)
UPDATE lessons l
SET title_fr = 'Expression de l''information génétique : de l''ADN au caractère',
    lesson_type = 'theory',
    duration_minutes = 95,
    learning_objectives = jsonb_build_array(
        'Distinguer ADN, ARNm et protéine et préciser leur lieu dans la cellule',
        'Construire la séquence d''ARNm à partir d''un brin d''ADN',
        'Traduire une séquence d''ARNm en acides aminés à l''aide du code génétique',
        'Expliquer la relation gène → protéine → caractère et l''effet possible d''une mutation'
    ),
    content = jsonb_build_object(
        'guiding_question', 'Comment une information écrite dans l''ADN devient-elle un caractère observable ?',
        'micro_enseignements', jsonb_build_array(
            jsonb_build_object('id', 'svt_ch2_l2_vue_ensemble', 'title', '1. J''observe : ADN → ARNm → protéine', 'type', 'observation'),
            jsonb_build_object('id', 'svt_ch2_l2_transcription', 'title', '2. Je construis l''ARNm : la transcription', 'type', 'processus'),
            jsonb_build_object('id', 'svt_ch2_l2_traduction', 'title', '3. Je traduis les codons : la traduction', 'type', 'processus'),
            jsonb_build_object('id', 'svt_ch2_l2_relation', 'title', '4. Je relie gène, protéine et caractère', 'type', 'raisonnement'),
            jsonb_build_object('id', 'svt_ch2_l2_bac', 'title', '5. Je m''entraîne avec une séquence type Bac', 'type', 'application'),
            jsonb_build_object('id', 'svt_ch2_l2_validation', 'title', '6. Je valide sans réciter', 'type', 'evaluation')
        ),
        'prerequisites', jsonb_build_array(
            'Connaître les nucléotides A, T, C et G de l''ADN',
            'Appliquer la complémentarité A-T et C-G',
            'Savoir qu''un gène est une portion d''ADN'
        ),
        'sections', jsonb_build_array(
            jsonb_build_object(
                'title', '1. J''observe : ADN → ARNm → protéine',
                'content', 'L''ADN reste dans le noyau. Une copie appelée ARNm traverse un pore nucléaire et rejoint un ribosome dans le cytoplasme.',
                'type', 'observation'
            ),
            jsonb_build_object(
                'title', '2. Je construis l''ARNm : la transcription',
                'content', 'La transcription copie l''information d''un gène sous forme d''ARNm. Dans l''ARN, U remplace T.',
                'type', 'processus'
            ),
            jsonb_build_object(
                'title', '3. Je traduis les codons : la traduction',
                'content', 'Le ribosome lit l''ARNm de 5'' vers 3'', codon par codon, et assemble les acides aminés jusqu''à un codon STOP.',
                'type', 'processus'
            ),
            jsonb_build_object(
                'title', '4. Je relie gène, protéine et caractère',
                'content', 'Une mutation peut changer un codon, parfois un acide aminé, puis la structure ou la fonction de la protéine et le caractère.',
                'type', 'raisonnement'
            ),
            jsonb_build_object(
                'title', '5. Je m''entraîne comme au Bac',
                'content', 'Comparer deux séquences, transcrire, traduire puis construire une conclusion fondée sur les documents.',
                'type', 'application'
            )
        ),
        'phases', jsonb_build_object(
            'activation', jsonb_build_object('duration_minutes', 8, 'focus', jsonb_build_array('observation globale')),
            'exploration', jsonb_build_object('duration_minutes', 17, 'focus', jsonb_build_array('image et simulation')),
            'explanation', jsonb_build_object('duration_minutes', 30, 'focus', jsonb_build_array('transcription', 'traduction', 'relation gène-protéine-caractère')),
            'application', jsonb_build_object('duration_minutes', 25, 'focus', jsonb_build_array('comparaison de séquences type Bac')),
            'consolidation', jsonb_build_object('duration_minutes', 15, 'focus', jsonb_build_array('explication causale et ticket de sortie'))
        ),
        'reference_example', jsonb_build_object(
            'coding_dna_5_3', 'ATG GAA TTT CCG TAA',
            'mrna_5_3', 'AUG GAA UUU CCG UAA',
            'protein', 'Met – Glu – Phe – Pro – STOP'
        ),
        'interactive_exercises', jsonb_build_array(
            jsonb_build_object('id', 'transcription_lab', 'type', 'molecule_drag_drop', 'difficulty', 'intermediate', 'llm_reads', jsonb_build_array('student_answer', 'errors', 'attempts', 'hints_used')),
            jsonb_build_object('id', 'translation_lab', 'type', 'trna_amino_acid_assembly', 'difficulty', 'intermediate', 'llm_reads', jsonb_build_array('student_answer', 'expected_answer', 'observations')),
            jsonb_build_object('id', 'mutation_lab', 'type', 'mutation_comparison', 'difficulty', 'advanced', 'llm_reads', jsonb_build_array('mutation_tests', 'mutation_type', 'protein_effect'))
        ),
        'misconceptions', jsonb_build_array(
            jsonb_build_object('error', 'L''ADN sort du noyau.', 'remediation', 'L''ADN reste dans le noyau ; seule la copie ARNm en sort.'),
            jsonb_build_object('error', 'Transcription et traduction sont identiques.', 'remediation', 'Transcription = copie ; traduction = changement de langage.'),
            jsonb_build_object('error', 'Le code génétique se lit avec l''ADN.', 'remediation', 'Le tableau se lit avec les codons de l''ARNm orienté 5'' → 3''.'),
            jsonb_build_object('error', 'Toute mutation change le caractère.', 'remediation', 'L''effet dépend du codon et de la fonction de la protéine.')
        ),
        'exit_ticket', jsonb_build_array(
            'Replace dans l''ordre : caractère, ARNm, ADN, protéine.',
            'À partir de 5''-ATG GCT TAA-3'', écris l''ARNm et la chaîne peptidique.',
            'Explique pourquoi une substitution peut ne pas modifier la protéine.'
        )
    ),
    media_resources = jsonb_build_array(
        jsonb_build_object(
            'type', 'image',
            'url', '/media/images/svt/ch2_information_genetique/lesson_2_expression/chromosome_adn_gene.png',
            'caption', 'Zoom visuel : chromosome → ADN → gène.',
            'trigger', 'observe le zoom chromosome ADN gène'
        ),
        jsonb_build_object(
            'type', 'image',
            'url', '/media/images/svt/ch2_information_genetique/lesson_2_expression/adn_arnm_proteine.png',
            'caption', 'Du noyau à la protéine : ADN → ARNm → protéine.',
            'trigger', 'observe le trajet ADN ARNm protéine'
        ),
        jsonb_build_object(
            'type', 'image',
            'url', '/media/images/svt/ch2_information_genetique/lesson_2_expression/transcription_arnm.png',
            'caption', 'La transcription construit une copie ARNm dans le noyau.',
            'trigger', 'observe la transcription de l''ARNm'
        ),
        jsonb_build_object(
            'type', 'image',
            'url', '/media/images/svt/ch2_information_genetique/lesson_2_expression/traduction_ribosome.png',
            'caption', 'Le ribosome lit les codons et assemble les acides aminés.',
            'trigger', 'observe la traduction au ribosome'
        ),
        jsonb_build_object(
            'type', 'simulation',
            'url', '/media/simulations/svt/ch2_information_genetique/expression/index.html',
            'caption', 'Laboratoire visuel : observe, transcris, traduis puis teste une mutation.',
            'trigger', 'lance la simulation expression génétique'
        ),
        jsonb_build_object(
            'type', 'image',
            'url', '/media/images/svt/ch2_information_genetique/lesson_2_expression/mutation_gene_proteine_caractere.png',
            'caption', 'Une mutation peut modifier une protéine et parfois le caractère.',
            'trigger', 'compare gène normal et gène muté'
        )
    )
FROM target
WHERE l.id = target.id;

WITH target AS (
    SELECT l.id
    FROM lessons l
    JOIN chapters c ON c.id = l.chapter_id
    WHERE c.chapter_number = 2
      AND l.order_index = 2
      AND lower(c.title_fr) LIKE '%génétique%'
    ORDER BY l.created_at
    LIMIT 1
), resources(section_title, resource_type, title, description, file_path, trigger_text, phase, difficulty_tier, concepts, metadata, order_index) AS (
    VALUES
      ('Prérequis visuel', 'image', 'Chromosome → ADN → gène', 'Zoom montrant qu''un gène est une portion d''ADN.', '/media/images/svt/ch2_information_genetique/lesson_2_expression/chromosome_adn_gene.png', 'observe le zoom chromosome ADN gène', 'activation', 'beginner', '["chromosome","ADN","gène"]'::jsonb, '{"caption":"Du chromosome au gène"}'::jsonb, 0),
      ('Vue d''ensemble', 'image', 'ADN → ARNm → protéine', 'Illustration du trajet de l''information génétique du noyau au ribosome.', '/media/images/svt/ch2_information_genetique/lesson_2_expression/adn_arnm_proteine.png', 'observe le trajet ADN ARNm protéine', 'activation', 'beginner', '["ADN","ARNm","ribosome","protéine"]'::jsonb, '{"caption":"Du noyau à la protéine"}'::jsonb, 1),
      ('Transcription', 'image', 'La transcription en image', 'Gros plan sur l''ARN polymérase et l''ARNm en formation.', '/media/images/svt/ch2_information_genetique/lesson_2_expression/transcription_arnm.png', 'observe la transcription de l''ARNm', 'explanation', 'beginner', '["ADN","ARN polymérase","ARNm"]'::jsonb, '{"caption":"Transcription dans le noyau"}'::jsonb, 2),
      ('Traduction', 'image', 'La traduction en image', 'Gros plan sur le ribosome, les ARNt et la chaîne polypeptidique.', '/media/images/svt/ch2_information_genetique/lesson_2_expression/traduction_ribosome.png', 'observe la traduction au ribosome', 'explanation', 'beginner', '["ARNm","ribosome","ARNt","acide aminé"]'::jsonb, '{"caption":"Traduction dans le cytoplasme"}'::jsonb, 3),
      ('Transcription et traduction', 'simulation', 'Laboratoire avancé de l''expression génétique', 'Trois laboratoires manipulables et pilotables par l''IA : construire l''ARNm, assembler la protéine et comparer trois mutations.', '/media/simulations/svt/ch2_information_genetique/expression/index.html', 'lance la simulation expression génétique', 'exploration', 'intermediate', '["gène","transcription","traduction","codon","mutation"]'::jsonb, '{"visual":true,"simulation_id":"svt_gene_expression_advanced_lab","simulation_version":"2.0","variants":["transcription","translation","mutations"],"llm_readable_state":true,"llm_controllable":true,"viewport":"native_100vh_no_scroll"}'::jsonb, 4),
      ('Relation gène-protéine-caractère', 'image', 'Du gène muté au caractère', 'Comparaison visuelle d''un allèle normal et d''un allèle muté.', '/media/images/svt/ch2_information_genetique/lesson_2_expression/mutation_gene_proteine_caractere.png', 'compare gène normal et gène muté', 'explanation', 'intermediate', '["mutation","protéine","caractère"]'::jsonb, '{"caption":"Effet possible d’une mutation"}'::jsonb, 3),
      ('Application type Bac', 'exercise', 'Comparer deux allèles', 'Transcrire, traduire puis expliquer l''effet possible d''une substitution.', NULL, 'exercice séquences allèle normal muté', 'application', 'intermediate', '["allèle","séquence","code génétique"]'::jsonb, '{"format":"document_scientifique"}'::jsonb, 4)
)
INSERT INTO lesson_resources (lesson_id, section_title, resource_type, title, description, file_path, trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
SELECT target.id, r.section_title, r.resource_type, r.title, r.description, r.file_path, r.trigger_text, r.phase, r.difficulty_tier::difficulty_level, r.concepts, r.metadata, r.order_index
FROM target CROSS JOIN resources r
WHERE NOT EXISTS (
    SELECT 1 FROM lesson_resources existing
    WHERE existing.lesson_id = target.id AND existing.title = r.title
);

COMMIT;
