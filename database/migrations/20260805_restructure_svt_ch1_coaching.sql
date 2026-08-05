-- Restructure le premier chapitre de SVT pour un coaching progressif et
-- rattache au muscle les ressources qui avaient été insérées dans la leçon 1.
-- Migration idempotente : elle peut être rejouée sans dupliquer les ressources.

BEGIN;

DO $$
DECLARE
    v_chapter_id UUID;
    v_energy_lesson_id UUID;
    v_muscle_lesson_id UUID;
BEGIN
    SELECT c.id INTO v_chapter_id
    FROM chapters c
    JOIN subjects s ON s.id = c.subject_id
    WHERE s.name_fr ILIKE '%Sciences de la Vie%'
      AND c.title_fr ILIKE 'Consommation de la matière organique%'
    ORDER BY c.order_index
    LIMIT 1;

    IF v_chapter_id IS NULL THEN
        RAISE EXCEPTION 'Chapitre SVT « Consommation de la matière organique » introuvable';
    END IF;

    SELECT id INTO v_energy_lesson_id
    FROM lessons
    WHERE chapter_id = v_chapter_id
      AND title_fr ILIKE 'Libération de l''énergie%'
    ORDER BY order_index
    LIMIT 1;

    SELECT id INTO v_muscle_lesson_id
    FROM lessons
    WHERE chapter_id = v_chapter_id
      AND title_fr ILIKE 'Rôle du muscle strié%'
    ORDER BY order_index
    LIMIT 1;

    IF v_energy_lesson_id IS NULL OR v_muscle_lesson_id IS NULL THEN
        RAISE EXCEPTION 'Les deux leçons attendues du chapitre SVT sont introuvables';
    END IF;

    UPDATE lessons
    SET learning_objectives = jsonb_build_array(
            'Formuler puis vérifier les conditions de la respiration et de la fermentation à partir de données expérimentales',
            'Décrire le lieu, les étapes essentielles et le bilan de la glycolyse',
            'Relier l''ultrastructure de la mitochondrie aux étapes de la respiration cellulaire',
            'Déterminer les étapes essentielles et le bilan du cycle de Krebs',
            'Expliquer la chaîne respiratoire, le rôle de l''O2 et la phosphorylation oxydative',
            'Comparer les fermentations lactique et alcoolique à partir de leurs bilans',
            'Calculer et représenter les bilans et rendements de la respiration et de la fermentation'
        ),
        content = COALESCE(content, '{}'::jsonb) || jsonb_build_object(
            'coaching_sequence', jsonb_build_array(
                jsonb_build_object('step', 1, 'phase', 'activation', 'action', 'Problème et prédictions à partir du dispositif EXAO sur les levures'),
                jsonb_build_object('step', 2, 'phase', 'exploration', 'action', 'Manipuler ou lire les mesures O2, CO2 et production d''énergie'),
                jsonb_build_object('step', 3, 'phase', 'explanation', 'action', 'Construire glycolyse, mitochondrie, Krebs et chaîne respiratoire'),
                jsonb_build_object('step', 4, 'phase', 'application', 'action', 'Comparer fermentation et respiration et calculer les rendements'),
                jsonb_build_object('step', 5, 'phase', 'consolidation', 'action', 'Résoudre un exercice de type BAC et produire un schéma-bilan')
            )
        )
    WHERE id = v_energy_lesson_id;

    UPDATE lessons
    SET learning_objectives = jsonb_build_array(
            'Analyser des myogrammes : secousse, sommation et tétanos',
            'Exploiter les phénomènes thermiques et chimiques associés à la contraction',
            'Décrire l''organisation du muscle, de la fibre, de la myofibrille et du sarcomère',
            'Expliquer le glissement actine-myosine et le rôle de l''ATP dans la contraction',
            'Identifier les voies de régénération de l''ATP selon l''intensité et la durée de l''effort',
            'Résoudre un problème de type BAC en reliant documents, mécanisme et bilan énergétique'
        ),
        content = COALESCE(content, '{}'::jsonb) || jsonb_build_object(
            'coaching_sequence', jsonb_build_array(
                jsonb_build_object('step', 1, 'phase', 'activation', 'action', 'Problème : comment le muscle transforme-t-il l''énergie chimique en mouvement ?'),
                jsonb_build_object('step', 2, 'phase', 'exploration', 'action', 'Observer EMG, myogrammes, chaleur et modifications chimiques'),
                jsonb_build_object('step', 3, 'phase', 'explanation', 'action', 'Relier organisation du sarcomère, glissement des filaments et ATP'),
                jsonb_build_object('step', 4, 'phase', 'application', 'action', 'Choisir la filière de régénération de l''ATP selon l''effort'),
                jsonb_build_object('step', 5, 'phase', 'consolidation', 'action', 'Traiter des documents de type BAC et rédiger une synthèse')
            )
        )
    WHERE id = v_muscle_lesson_id;

    -- Correction de l'ancien script : lesson_id n'avait pas été réaffecté après
    -- l'insertion de la leçon 2, ce qui a rattaché ses ressources à la leçon 1.
    UPDATE lesson_resources
    SET lesson_id = v_muscle_lesson_id
    WHERE lesson_id = v_energy_lesson_id
      AND (
          title ILIKE '%sarcom%'
          OR title ILIKE '%contraction musculaire%'
          OR title ILIKE '%filières énergétiques%'
          OR title ILIKE '%filieres energetiques%'
          OR title ILIKE '%myogram%'
          OR title ILIKE '%thermique%contraction%'
      );

    UPDATE lesson_resources
    SET section_title = 'Mesure de l''activité musculaire', phase = 'exploration'
    WHERE lesson_id = v_muscle_lesson_id
      AND (title ILIKE '%myogram%' OR title ILIKE '%thermique%contraction%');

    INSERT INTO lesson_resources (
        lesson_id, section_title, resource_type, title, description, file_path,
        trigger_text, phase, difficulty_tier, concepts, metadata, order_index
    )
    SELECT v_energy_lesson_id, 'Introduction expérimentale', 'image',
           'Reconstitution pédagogique — dispositif EXAO levures',
           'Deux montages comparant respiration et fermentation chez les levures. L''élève formule ses prédictions avant l''étude des mesures.',
           '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/introduction/reconstitution_exao_levures.png',
           'observe le dispositif EXAO levures', 'activation', 'beginner',
           jsonb_build_array('levures', 'O2', 'CO2', 'respiration', 'fermentation'),
           jsonb_build_object(
               'caption', 'Reconstitution pédagogique – illustration générée',
               'source_type', 'ai_generated_reconstruction',
               'pedagogical_use', 'situation_probleme',
               'evidence_status', 'illustration_non_documentaire'
           ), 0
    WHERE NOT EXISTS (
        SELECT 1 FROM lesson_resources
        WHERE lesson_id = v_energy_lesson_id
          AND file_path = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/introduction/reconstitution_exao_levures.png'
    );

    INSERT INTO lesson_resources (
        lesson_id, section_title, resource_type, title, description, file_path,
        trigger_text, phase, difficulty_tier, concepts, metadata, order_index
    )
    SELECT v_muscle_lesson_id, 'Introduction expérimentale', 'image',
           'Reconstitution pédagogique — EMG pendant un effort',
           'Montage de physiologie de l''effort avec électrodes de surface et acquisition de données pour lancer le problème énergétique du muscle.',
           '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/introduction/reconstitution_emg_effort.png',
           'observe le montage EMG effort', 'activation', 'beginner',
           jsonb_build_array('muscle strié', 'EMG', 'effort', 'énergie'),
           jsonb_build_object(
               'caption', 'Reconstitution pédagogique – illustration générée',
               'source_type', 'ai_generated_reconstruction',
               'pedagogical_use', 'situation_probleme',
               'evidence_status', 'illustration_non_documentaire'
           ), 0
    WHERE NOT EXISTS (
        SELECT 1 FROM lesson_resources
        WHERE lesson_id = v_muscle_lesson_id
          AND file_path = '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/introduction/reconstitution_emg_effort.png'
    );

    INSERT INTO lesson_resources (
        lesson_id, section_title, resource_type, title, description, file_path,
        trigger_text, phase, difficulty_tier, concepts, metadata, order_index
    )
    SELECT v_muscle_lesson_id, 'Structure du muscle', 'image', 'Structure du sarcomère',
           'Schéma annoté permettant de relier fibre, myofibrille et sarcomère.',
           '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/schema_sarcomere.svg',
           'montre structure sarcomere', 'explanation', 'beginner',
           jsonb_build_array('sarcomère', 'actine', 'myosine'),
           jsonb_build_object('caption', 'Organisation du sarcomère'), 20
    WHERE NOT EXISTS (
        SELECT 1 FROM lesson_resources
        WHERE lesson_id = v_muscle_lesson_id
          AND file_path = '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/schema_sarcomere.svg'
    );

    INSERT INTO lesson_resources (
        lesson_id, section_title, resource_type, title, description, file_path,
        trigger_text, phase, difficulty_tier, concepts, metadata, order_index
    )
    SELECT v_muscle_lesson_id, 'Contraction musculaire', 'simulation', 'Animation de la contraction musculaire',
           'Simulation manipulable du glissement actine-myosine et de l''utilisation de l''ATP.',
           '/media/simulations/svt/ch1_consommation_matiere_organique/muscle/contraction/index.html',
           'lance simulation contraction musculaire', 'exploration', 'intermediate',
           jsonb_build_array('actine', 'myosine', 'ATP'),
           jsonb_build_object('interaction_cycle', 'prédire-observer-expliquer-vérifier'), 21
    WHERE NOT EXISTS (
        SELECT 1 FROM lesson_resources
        WHERE lesson_id = v_muscle_lesson_id
          AND file_path = '/media/simulations/svt/ch1_consommation_matiere_organique/muscle/contraction/index.html'
    );

    INSERT INTO lesson_resources (
        lesson_id, section_title, resource_type, title, description, file_path,
        trigger_text, phase, difficulty_tier, concepts, metadata, order_index
    )
    SELECT v_muscle_lesson_id, 'Métabolisme énergétique', 'image', 'Sources d''énergie musculaire',
           'Schéma comparant phosphocréatine, glycolyse anaérobie et respiration selon l''effort.',
           '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/metabolisme/sources_energie_musculaire.svg',
           'montre sources energie musculaire', 'application', 'intermediate',
           jsonb_build_array('phosphocréatine', 'glycolyse', 'respiration'),
           jsonb_build_object('caption', 'Voies de régénération de l''ATP'), 22
    WHERE NOT EXISTS (
        SELECT 1 FROM lesson_resources
        WHERE lesson_id = v_muscle_lesson_id
          AND file_path = '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/metabolisme/sources_energie_musculaire.svg'
    );
END $$;

COMMIT;
