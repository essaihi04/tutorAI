-- Médias créés pour le lecteur de cours SVT. Les reconstitutions générées
-- restent explicitement distinguées des documents scientifiques authentiques.
BEGIN;

DO $$
DECLARE
    v_chapter_id UUID;
    v_energy_id UUID;
    v_muscle_id UUID;
BEGIN
    SELECT c.id INTO v_chapter_id
    FROM chapters c
    JOIN subjects s ON s.id = c.subject_id
    WHERE s.name_fr ILIKE '%Sciences de la Vie%'
      AND c.title_fr ILIKE 'Consommation de la matière organique%'
    LIMIT 1;

    SELECT id INTO v_energy_id FROM lessons
    WHERE chapter_id = v_chapter_id AND title_fr ILIKE 'Libération de l''énergie%'
    ORDER BY order_index LIMIT 1;

    SELECT id INTO v_muscle_id FROM lessons
    WHERE chapter_id = v_chapter_id AND title_fr ILIKE 'Rôle du muscle strié%'
    ORDER BY order_index LIMIT 1;

    IF v_energy_id IS NULL OR v_muscle_id IS NULL THEN
        RAISE EXCEPTION 'Leçons SVT du chapitre 1 introuvables';
    END IF;

    INSERT INTO lesson_resources
        (lesson_id, section_title, resource_type, title, description, file_path,
         trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
    SELECT v_energy_id, 'Diagnostic', 'image', 'Test à l''iode sur feuille panachée',
           'Support du diagnostic sur les acquis de photosynthèse et de production de matière organique.',
           '/media/images/svt/ch1_consommation_matiere_organique/diagnostic/test_iode_amidon_reconstitution.png',
           'montre le test iode amidon', 'activation', 'beginner',
           jsonb_build_array('photosynthèse', 'amidon', 'chlorophylle', 'lumière'),
           jsonb_build_object('source_type', 'ai_generated_reconstruction', 'evidence_status', 'illustration_non_documentaire', 'caption', 'Reconstitution pédagogique générée'), -10
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_energy_id AND file_path='/media/images/svt/ch1_consommation_matiere_organique/diagnostic/test_iode_amidon_reconstitution.png');

    INSERT INTO lesson_resources
        (lesson_id, section_title, resource_type, title, description, file_path,
         trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
    SELECT v_energy_id, 'ATP', 'simulation', 'Cycle ATP-ADP',
           'Animation déterministe de l''hydrolyse, de la phosphorylation et du couplage énergétique.',
           '/media/simulations/svt/ch1_consommation_matiere_organique/atp-adp/index.html',
           'lance le cycle ATP ADP', 'explanation', 'beginner',
           jsonb_build_array('ATP', 'ADP', 'phosphorylation', 'couplage'),
           jsonb_build_object('simulation_id', 'svt_ch1_atp_adp', 'interaction_cycle', 'prédire-observer-expliquer-vérifier'), 2
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_energy_id AND file_path='/media/simulations/svt/ch1_consommation_matiere_organique/atp-adp/index.html');

    INSERT INTO lesson_resources
        (lesson_id, section_title, resource_type, title, description, file_path,
         trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
    SELECT v_energy_id, 'Mitochondrie', 'image', 'Ultrastructure mitochondriale',
           'Reconstitution pédagogique de type MET pour identifier la double membrane, les crêtes et la matrice.',
           '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_micrographie_reconstitution.png',
           'montre micrographie mitochondrie', 'explanation', 'beginner',
           jsonb_build_array('mitochondrie', 'crêtes', 'matrice', 'membrane interne'),
           jsonb_build_object('source_type', 'ai_generated_reconstruction', 'evidence_status', 'illustration_non_documentaire', 'caption', 'Reconstitution pédagogique, non issue d''une acquisition microscopique'), 12
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_energy_id AND file_path='/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_micrographie_reconstitution.png');

    INSERT INTO lesson_resources
        (lesson_id, section_title, resource_type, title, description, file_path,
         trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
    SELECT v_energy_id, 'Phosphorylation oxydative', 'simulation', 'Chimiosmose mitochondriale',
           'Simulation du flux d''électrons, du gradient protonique, de l''ATP synthase et du rôle de O2.',
           '/media/simulations/svt/ch1_consommation_matiere_organique/chimiosmose/index.html',
           'lance simulation chimiosmose', 'explanation', 'intermediate',
           jsonb_build_array('chaîne respiratoire', 'H+', 'ATP synthase', 'O2'),
           jsonb_build_object('simulation_id', 'svt_ch1_chimiosmose', 'interaction_cycle', 'prédire-observer-expliquer-vérifier'), 15
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_energy_id AND file_path='/media/simulations/svt/ch1_consommation_matiere_organique/chimiosmose/index.html');

    INSERT INTO lesson_resources
        (lesson_id, section_title, resource_type, title, description, file_path,
         trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
    SELECT v_muscle_id, 'Structure du muscle', 'image', 'Muscle strié squelettique en coupe longitudinale',
           'Reconstitution pédagogique de microscopie pour identifier fibres parallèles, striation et noyaux périphériques.',
           '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/muscle_strie_micrographie_reconstitution.png',
           'montre micrographie muscle strié', 'explanation', 'beginner',
           jsonb_build_array('fibre musculaire', 'striation', 'noyaux périphériques'),
           jsonb_build_object('source_type', 'ai_generated_reconstruction', 'evidence_status', 'illustration_non_documentaire', 'caption', 'Reconstitution pédagogique, non issue d''une acquisition microscopique'), 10
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_muscle_id AND file_path='/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/muscle_strie_micrographie_reconstitution.png');

    UPDATE lesson_resources
    SET description = 'Simulation déterministe du glissement actine-myosine testant séparément Ca2+ et ATP.',
        concepts = jsonb_build_array('actine', 'myosine', 'Ca2+', 'ATP', 'sarcomère'),
        metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object('simulation_id', 'svt_ch1_contraction_actine_myosine', 'interaction_cycle', 'prédire-observer-expliquer-vérifier')
    WHERE lesson_id = v_muscle_id
      AND file_path = '/media/simulations/svt/ch1_consommation_matiere_organique/muscle/contraction/index.html';
END $$;

COMMIT;
