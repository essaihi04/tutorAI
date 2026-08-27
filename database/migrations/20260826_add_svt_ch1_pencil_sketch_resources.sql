-- Croquis déterministes du premier cours de SVT « Consommation de la matière
-- organique ». `resource_type = image` conserve le routage historique des
-- ressources visuelles ; `metadata.schema_id` demande au serveur de les poser
-- dans la zone dessin du Live Board, sans fichier ni fond opaque.
BEGIN;

DO $$
DECLARE
    v_chapter_id UUID;
    v_energy_id UUID;
BEGIN
    SELECT c.id INTO v_chapter_id
    FROM chapters c
    JOIN subjects s ON s.id = c.subject_id
    WHERE s.name_fr ILIKE '%Sciences de la Vie%'
      AND c.title_fr ILIKE 'Consommation de la matière organique%'
    ORDER BY c.order_index
    LIMIT 1;

    SELECT l.id INTO v_energy_id
    FROM lessons l
    WHERE l.chapter_id = v_chapter_id
      AND l.title_fr ILIKE 'Libération de l''énergie%'
    ORDER BY l.order_index
    LIMIT 1;

    IF v_energy_id IS NULL THEN
        RAISE EXCEPTION 'Premier cours SVT de consommation de la matière organique introuvable';
    END IF;

    INSERT INTO lesson_resources
        (lesson_id, section_title, resource_type, title, description,
         trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
    SELECT
        v_energy_id,
        resource.section_title,
        'image',
        resource.title,
        resource.description,
        resource.trigger_text,
        resource.phase,
        resource.difficulty_tier::difficulty_level,
        resource.concepts,
        resource.metadata,
        resource.order_index
    FROM (VALUES
        (
            'Introduction',
            'Croquis : de la cellule à la mitochondrie',
            'Croquis progressif localisant la mitochondrie, siège de la respiration, dans une cellule eucaryote.',
            'dessine cellule mitochondrie au tableau',
            'activation', 'beginner',
            '["cellule", "mitochondrie", "respiration cellulaire", "localisation"]'::jsonb,
            jsonb_build_object(
                'schema_id', 'svt_croquis_cellule_mitochondrie',
                'render_target', 'live_board', 'visual_style', 'pencil',
                'resource_role', 'teacher_sketch', 'course_id', 'svt_ch1_energy',
                'transparent_background', true, 'library_status', 'validated',
                'library_source', 'core_schema', 'library_version', 1,
                'llm_intents', jsonb_build_array('dessiner une cellule avec mitochondries', 'faire un zoom cellule-mitochondrie'),
                'drawing_steps', jsonb_build_array('cellule et noyau', 'mitochondries', 'zoom et fonction')
            ),
            101
        ),
        (
            'ATP',
            'Croquis : cycle ATP–ADP',
            'Croquis du couplage entre hydrolyse de l''ATP, activités cellulaires et régénération par les voies énergétiques.',
            'dessine cycle ATP ADP au tableau',
            'explanation', 'beginner',
            '["ATP", "ADP", "hydrolyse", "phosphorylation", "couplage énergétique"]'::jsonb,
            jsonb_build_object(
                'schema_id', 'svt_croquis_atp_adp',
                'render_target', 'live_board', 'visual_style', 'pencil',
                'resource_role', 'teacher_sketch', 'course_id', 'svt_ch1_energy',
                'transparent_background', true, 'library_status', 'validated',
                'library_source', 'core_schema', 'library_version', 1,
                'llm_intents', jsonb_build_array('dessiner le cycle ATP-ADP', 'expliquer le couplage énergétique'),
                'drawing_steps', jsonb_build_array('ATP à trois phosphates', 'hydrolyse', 'phosphorylation', 'couplage')
            ),
            102
        ),
        (
            'Introduction expérimentale',
            'Croquis : levures avec ou sans dioxygène',
            'Montage comparatif avec levures, glucose, capteurs O₂/CO₂ et produits attendus pour respiration et fermentation.',
            'dessine expérience levures avec sans oxygène',
            'exploration', 'beginner',
            '["levures", "O2", "CO2", "éthanol", "EXAO", "respiration", "fermentation"]'::jsonb,
            jsonb_build_object(
                'schema_id', 'svt_croquis_experience_levures',
                'render_target', 'live_board', 'visual_style', 'pencil',
                'resource_role', 'teacher_sketch', 'course_id', 'svt_ch1_energy',
                'transparent_background', true, 'library_status', 'validated',
                'library_source', 'core_schema', 'library_version', 1,
                'llm_intents', jsonb_build_array('dessiner le protocole des levures', 'comparer avec et sans O2'),
                'drawing_steps', jsonb_build_array('deux enceintes', 'conditions O2', 'capteurs', 'résultats')
            ),
            103
        ),
        (
            'Glycolyse',
            'Croquis : bilan de la glycolyse',
            'Croquis carboné et énergétique du passage d''un glucose C6 à deux pyruvates C3 dans le cytoplasme.',
            'dessine bilan glycolyse glucose pyruvate',
            'explanation', 'beginner',
            '["glycolyse", "glucose", "pyruvate", "cytoplasme", "2 ATP nets", "NADH,H+"]'::jsonb,
            jsonb_build_object(
                'schema_id', 'svt_croquis_glycolyse',
                'render_target', 'live_board', 'visual_style', 'pencil',
                'resource_role', 'teacher_sketch', 'course_id', 'svt_ch1_energy',
                'transparent_background', true, 'library_status', 'validated',
                'library_source', 'core_schema', 'library_version', 1,
                'llm_intents', jsonb_build_array('dessiner le bilan de la glycolyse', 'expliquer les 2 ATP nets'),
                'drawing_steps', jsonb_build_array('glucose C6', 'activation et coupure', 'deux pyruvates C3', 'bilan net')
            ),
            104
        ),
        (
            'Mitochondrie',
            'Croquis : ultrastructure de la mitochondrie',
            'Croquis annoté de la double membrane, des crêtes, de l''espace intermembranaire et de la matrice.',
            'dessine mitochondrie annotée au tableau',
            'explanation', 'beginner',
            '["mitochondrie", "membrane interne", "membrane externe", "crêtes", "matrice", "espace intermembranaire"]'::jsonb,
            jsonb_build_object(
                'schema_id', 'svt_croquis_mitochondrie',
                'render_target', 'live_board', 'visual_style', 'pencil',
                'resource_role', 'teacher_sketch', 'course_id', 'svt_ch1_energy',
                'transparent_background', true, 'library_status', 'validated',
                'library_source', 'core_schema', 'library_version', 1,
                'llm_intents', jsonb_build_array('dessiner une mitochondrie annotée', 'localiser Krebs et chaîne respiratoire'),
                'drawing_steps', jsonb_build_array('membrane externe', 'membrane interne et crêtes', 'compartiments', 'localisation des étapes')
            ),
            105
        ),
        (
            'Cycle de Krebs',
            'Croquis : bilan du cycle de Krebs',
            'Croquis de deux tours par glucose mettant en évidence CO₂, ATP et transporteurs réduits.',
            'dessine bilan cycle Krebs au tableau',
            'explanation', 'intermediate',
            '["cycle de Krebs", "acétyl-CoA", "CO2", "NADH,H+", "FADH2", "matrice"]'::jsonb,
            jsonb_build_object(
                'schema_id', 'svt_croquis_krebs',
                'render_target', 'live_board', 'visual_style', 'pencil',
                'resource_role', 'teacher_sketch', 'course_id', 'svt_ch1_energy',
                'transparent_background', true, 'library_status', 'validated',
                'library_source', 'core_schema', 'library_version', 1,
                'llm_intents', jsonb_build_array('dessiner le cycle de Krebs', 'résumer ses entrées et sorties'),
                'drawing_steps', jsonb_build_array('cycle', 'acétyl-CoA', 'CO2', 'transporteurs et ATP')
            ),
            106
        ),
        (
            'Phosphorylation oxydative',
            'Croquis : chaîne respiratoire et ATP synthase',
            'Croquis séparant le flux d''électrons, le pompage de H+, le rôle final de O₂ et la synthèse d''ATP.',
            'dessine chaîne respiratoire ATP synthase',
            'explanation', 'intermediate',
            '["chaîne respiratoire", "électrons", "gradient H+", "ATP synthase", "O2", "phosphorylation oxydative"]'::jsonb,
            jsonb_build_object(
                'schema_id', 'svt_croquis_chaine_respiratoire',
                'render_target', 'live_board', 'visual_style', 'pencil',
                'resource_role', 'teacher_sketch', 'course_id', 'svt_ch1_energy',
                'transparent_background', true, 'library_status', 'validated',
                'library_source', 'core_schema', 'library_version', 1,
                'llm_intents', jsonb_build_array('dessiner la chaîne respiratoire', 'expliquer le gradient protonique et ATP synthase'),
                'drawing_steps', jsonb_build_array('membrane interne', 'complexes et électrons', 'pompage H+', 'ATP synthase')
            ),
            107
        ),
        (
            'Fermentation',
            'Croquis : respiration ou fermentation',
            'Bifurcation après la glycolyse comparant les produits et les rendements avec et sans dioxygène.',
            'dessine comparaison respiration fermentation',
            'explanation', 'beginner',
            '["respiration", "fermentation", "avec O2", "sans O2", "pyruvate", "rendement ATP"]'::jsonb,
            jsonb_build_object(
                'schema_id', 'svt_croquis_respiration_fermentation',
                'render_target', 'live_board', 'visual_style', 'pencil',
                'resource_role', 'teacher_sketch', 'course_id', 'svt_ch1_energy',
                'transparent_background', true, 'library_status', 'validated',
                'library_source', 'core_schema', 'library_version', 1,
                'llm_intents', jsonb_build_array('dessiner la bifurcation respiration-fermentation', 'comparer avec et sans O2'),
                'drawing_steps', jsonb_build_array('glycolyse commune', 'bifurcation O2', 'produits', 'rendements')
            ),
            108
        ),
        (
            'Synthèse',
            'Croquis : bilan de la respiration cellulaire',
            'Schéma-bilan reliant glucose, glycolyse, cycle de Krebs, chaîne respiratoire, dioxygène et ATP.',
            'dessine bilan complet respiration cellulaire',
            'consolidation', 'intermediate',
            '["bilan respiration cellulaire", "glycolyse", "cycle de Krebs", "chaîne respiratoire", "ATP", "CO2", "H2O"]'::jsonb,
            jsonb_build_object(
                'schema_id', 'svt_croquis_bilan_respiration',
                'render_target', 'live_board', 'visual_style', 'pencil',
                'resource_role', 'teacher_sketch', 'course_id', 'svt_ch1_energy',
                'transparent_background', true, 'library_status', 'validated',
                'library_source', 'core_schema', 'library_version', 1,
                'llm_intents', jsonb_build_array('dessiner le bilan complet de la respiration', 'résumer le premier cours'),
                'drawing_steps', jsonb_build_array('glucose', 'trois étapes et lieux', 'O2 CO2 H2O', 'ATP et chaleur')
            ),
            109
        )
    ) AS resource(
        section_title, title, description, trigger_text, phase,
        difficulty_tier, concepts, metadata, order_index
    )
    WHERE NOT EXISTS (
        SELECT 1
        FROM lesson_resources existing
        WHERE existing.lesson_id = v_energy_id
          AND existing.metadata ->> 'schema_id' = resource.metadata ->> 'schema_id'
    );
END $$;

COMMIT;
