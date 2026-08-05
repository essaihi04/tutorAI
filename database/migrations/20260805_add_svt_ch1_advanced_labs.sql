-- Two primary investigation labs for Chapter 1 (2e BAC SVT).
-- Idempotent: insert missing rows, then refresh their metadata and priority.
DO $$
DECLARE
    v_chapter_id uuid;
    v_energy_id uuid;
    v_muscle_id uuid;
    v_energy_path text := '/media/simulations/svt/ch1_consommation_matiere_organique/labs/respiration-fermentation/index.html';
    v_muscle_path text := '/media/simulations/svt/ch1_consommation_matiere_organique/labs/muscle-energie/index.html';
BEGIN
    SELECT id INTO v_chapter_id
    FROM chapters
    WHERE title_fr ILIKE 'Consommation de la matière organique%'
    ORDER BY order_index
    LIMIT 1;

    SELECT id INTO v_energy_id FROM lessons
    WHERE chapter_id = v_chapter_id AND title_fr ILIKE 'Libération de l''énergie%'
    LIMIT 1;

    SELECT id INTO v_muscle_id FROM lessons
    WHERE chapter_id = v_chapter_id AND title_fr ILIKE 'Rôle du muscle strié%'
    LIMIT 1;

    IF v_energy_id IS NULL OR v_muscle_id IS NULL THEN
        RAISE EXCEPTION 'Leçons SVT chapitre 1 introuvables';
    END IF;

    INSERT INTO lesson_resources
        (lesson_id, section_title, resource_type, title, description, file_path,
         trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
    SELECT v_energy_id, 'Laboratoire d''investigation', 'simulation',
        'BioLab avancé — respiration et fermentation',
        'Laboratoire visuel avec prédictions, réglages O2-température-glucose, acquisition de courbes, carnet d''essais et exploration de la mitochondrie.',
        v_energy_path, 'ouvre le laboratoire respiration fermentation', 'exploration', 'intermediate',
        jsonb_build_array('levures','O2','CO2','température','respiration','fermentation','mitochondrie','ATP'),
        jsonb_build_object(
            'kind','advanced_virtual_lab','protocol_version','2.0','is_primary',true,
            'llm_readable',true,'llm_controllable',true,
            'interaction_cycle',jsonb_build_array('prédire','manipuler','mesurer','comparer','expliquer'),
            'missions',jsonb_build_array('rôle du dioxygène','effet de la température','localisation cellulaire'),
            'integrated_generated_visuals',3,'estimated_minutes',15),
        1
    WHERE NOT EXISTS (
        SELECT 1 FROM lesson_resources WHERE lesson_id=v_energy_id AND file_path=v_energy_path
    );

    INSERT INTO lesson_resources
        (lesson_id, section_title, resource_type, title, description, file_path,
         trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
    SELECT v_muscle_id, 'Laboratoire d''investigation', 'simulation',
        'PhysioLab avancé — muscle et énergie',
        'Laboratoire visuel avec myogrammes calculés, fréquence de stimulation, rôles du Ca2+ et de l''ATP, filières énergétiques et carnet comparatif.',
        v_muscle_path, 'ouvre le laboratoire muscle énergie', 'exploration', 'intermediate',
        jsonb_build_array('myogramme','secousse','sommation','tétanos','Ca2+','actine','myosine','ATP','filières énergétiques'),
        jsonb_build_object(
            'kind','advanced_virtual_lab','protocol_version','2.0','is_primary',true,
            'llm_readable',true,'llm_controllable',true,
            'interaction_cycle',jsonb_build_array('prédire','stimuler','enregistrer','comparer','expliquer'),
            'missions',jsonb_build_array('fréquence et myogramme','Ca2+ et ponts actine-myosine','filières de régénération de l''ATP'),
            'integrated_generated_visuals',3,'estimated_minutes',15),
        1
    WHERE NOT EXISTS (
        SELECT 1 FROM lesson_resources WHERE lesson_id=v_muscle_id AND file_path=v_muscle_path
    );

    UPDATE lesson_resources SET
        title='BioLab avancé — respiration et fermentation',
        section_title='Laboratoire d''investigation', phase='exploration',
        difficulty_tier='intermediate', order_index=1,
        metadata=jsonb_build_object(
            'kind','advanced_virtual_lab','protocol_version','2.0','is_primary',true,
            'llm_readable',true,'llm_controllable',true,
            'interaction_cycle',jsonb_build_array('prédire','manipuler','mesurer','comparer','expliquer'),
            'missions',jsonb_build_array('rôle du dioxygène','effet de la température','localisation cellulaire'),
            'integrated_generated_visuals',3,'estimated_minutes',15)
    WHERE lesson_id=v_energy_id AND file_path=v_energy_path;

    UPDATE lesson_resources SET
        title='PhysioLab avancé — muscle et énergie',
        section_title='Laboratoire d''investigation', phase='exploration',
        difficulty_tier='intermediate', order_index=1,
        metadata=jsonb_build_object(
            'kind','advanced_virtual_lab','protocol_version','2.0','is_primary',true,
            'llm_readable',true,'llm_controllable',true,
            'interaction_cycle',jsonb_build_array('prédire','stimuler','enregistrer','comparer','expliquer'),
            'missions',jsonb_build_array('fréquence et myogramme','Ca2+ et ponts actine-myosine','filières de régénération de l''ATP'),
            'integrated_generated_visuals',3,'estimated_minutes',15)
    WHERE lesson_id=v_muscle_id AND file_path=v_muscle_path;
END $$;
