-- Ajoute quatre visuels sans texte et quatre exercices interactifs au chapitre 1 SVT.
BEGIN;

DO $$
DECLARE
    v_chapter_id UUID;
    v_energy_id UUID;
    v_muscle_id UUID;
BEGIN
    SELECT id INTO v_chapter_id FROM chapters
    WHERE title_fr ILIKE 'Consommation de la matière organique%'
    ORDER BY order_index LIMIT 1;
    SELECT id INTO v_energy_id FROM lessons
    WHERE chapter_id = v_chapter_id AND title_fr ILIKE 'Libération de l''énergie%'
    LIMIT 1;
    SELECT id INTO v_muscle_id FROM lessons
    WHERE chapter_id = v_chapter_id AND title_fr ILIKE 'Rôle du muscle strié%'
    LIMIT 1;

    IF v_energy_id IS NULL OR v_muscle_id IS NULL THEN
        RAISE EXCEPTION 'Leçons du chapitre 1 SVT introuvables';
    END IF;

    INSERT INTO lesson_resources (lesson_id,section_title,resource_type,title,description,file_path,trigger_text,phase,difficulty_tier,concepts,metadata,order_index)
    SELECT v_energy_id,'Respiration cellulaire','image','Mitochondrie 3D à observer','Coupe 3D sans légendes pour faire identifier membranes, crêtes et matrice.','/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_3d_sans_legendes.png','observe mitochondrie 3d','explanation','beginner',jsonb_build_array('mitochondrie','crêtes','matrice'),jsonb_build_object('caption','Reconstitution pédagogique – illustration générée','source_type','ai_generated_reconstruction','interaction','identifier_avant_legendes'),30
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_energy_id AND file_path='/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_3d_sans_legendes.png');

    INSERT INTO lesson_resources (lesson_id,section_title,resource_type,title,description,file_path,trigger_text,phase,difficulty_tier,concepts,metadata,order_index)
    SELECT v_energy_id,'Fermentation','image','Levures : avec ou sans O2','Comparaison visuelle sans texte des produits et du rendement énergétique.','/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/fermentation/levures_aerobie_anaerobie.png','compare levures avec sans oxygene','explanation','beginner',jsonb_build_array('levures','respiration','fermentation','ATP'),jsonb_build_object('caption','Reconstitution pédagogique – illustration générée','source_type','ai_generated_reconstruction','interaction','comparer_deux_conditions'),31
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_energy_id AND file_path='/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/fermentation/levures_aerobie_anaerobie.png');

    INSERT INTO lesson_resources (lesson_id,section_title,resource_type,title,description,file_path,trigger_text,phase,difficulty_tier,concepts,metadata,order_index)
    SELECT v_energy_id,'Respiration cellulaire','simulation','Classe les étapes de la respiration','Exercice visuel : placer glycolyse, Krebs et chaîne respiratoire dans l''ordre.','/media/simulations/svt/ch1_consommation_matiere_organique/exercices/ordre-respiration/index.html','exercice visuel ordre respiration','application','intermediate',jsonb_build_array('glycolyse','Krebs','chaîne respiratoire'),jsonb_build_object('kind','interactive_visual_exercise','interaction','click_to_order','estimated_minutes',3),32
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_energy_id AND file_path='/media/simulations/svt/ch1_consommation_matiere_organique/exercices/ordre-respiration/index.html');

    INSERT INTO lesson_resources (lesson_id,section_title,resource_type,title,description,file_path,trigger_text,phase,difficulty_tier,concepts,metadata,order_index)
    SELECT v_energy_id,'Introduction expérimentale','simulation','Interprète les courbes EXAO','Exercice visuel : associer les courbes O2/CO2 à la respiration ou à la fermentation.','/media/simulations/svt/ch1_consommation_matiere_organique/exercices/lecture-exao/index.html','exercice interactif courbes exao','exploration','intermediate',jsonb_build_array('O2','CO2','EXAO','interprétation'),jsonb_build_object('kind','interactive_visual_exercise','interaction','graph_matching','estimated_minutes',3),33
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_energy_id AND file_path='/media/simulations/svt/ch1_consommation_matiere_organique/exercices/lecture-exao/index.html');

    INSERT INTO lesson_resources (lesson_id,section_title,resource_type,title,description,file_path,trigger_text,phase,difficulty_tier,concepts,metadata,order_index)
    SELECT v_muscle_id,'Structure du muscle','image','Du muscle au sarcomère en 3D','Zoom sans légendes du muscle vers le faisceau, la fibre, la myofibrille et le sarcomère.','/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/hierarchie_muscle_3d.png','observe organisation muscle 3d','explanation','beginner',jsonb_build_array('muscle','faisceau','fibre','myofibrille','sarcomère'),jsonb_build_object('caption','Reconstitution pédagogique – illustration générée','source_type','ai_generated_reconstruction','interaction','nommer_niveaux_organisation'),30
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_muscle_id AND file_path='/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/hierarchie_muscle_3d.png');

    INSERT INTO lesson_resources (lesson_id,section_title,resource_type,title,description,file_path,trigger_text,phase,difficulty_tier,concepts,metadata,order_index)
    SELECT v_muscle_id,'Contraction musculaire','image','Actine–myosine en 3D','Vue rapprochée sans légendes des filaments et des ponts actine-myosine.','/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/contraction/sarcomere_actine_myosine_3d.png','observe actine myosine 3d','explanation','intermediate',jsonb_build_array('actine','myosine','ponts','sarcomère'),jsonb_build_object('caption','Reconstitution pédagogique – illustration générée','source_type','ai_generated_reconstruction','interaction','identifier_filaments'),31
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_muscle_id AND file_path='/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/contraction/sarcomere_actine_myosine_3d.png');

    INSERT INTO lesson_resources (lesson_id,section_title,resource_type,title,description,file_path,trigger_text,phase,difficulty_tier,concepts,metadata,order_index)
    SELECT v_muscle_id,'Mesure de l''activité musculaire','simulation','Reconnais les myogrammes','Exercice visuel : associer secousse, sommation et tétanos à trois tracés.','/media/simulations/svt/ch1_consommation_matiere_organique/exercices/reconnaitre-myogrammes/index.html','exercice interactif myogrammes','exploration','intermediate',jsonb_build_array('secousse','sommation','tétanos','myogramme'),jsonb_build_object('kind','interactive_visual_exercise','interaction','curve_matching','estimated_minutes',3),32
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_muscle_id AND file_path='/media/simulations/svt/ch1_consommation_matiere_organique/exercices/reconnaitre-myogrammes/index.html');

    INSERT INTO lesson_resources (lesson_id,section_title,resource_type,title,description,file_path,trigger_text,phase,difficulty_tier,concepts,metadata,order_index)
    SELECT v_muscle_id,'Métabolisme énergétique','simulation','Choisis la filière de l''effort','Exercice visuel : relier durée d''effort et voie dominante de régénération de l''ATP.','/media/simulations/svt/ch1_consommation_matiere_organique/exercices/filieres-effort/index.html','exercice interactif filieres effort','application','intermediate',jsonb_build_array('phosphocréatine','fermentation lactique','respiration'),jsonb_build_object('kind','interactive_visual_exercise','interaction','scenario_matching','estimated_minutes',3),33
    WHERE NOT EXISTS (SELECT 1 FROM lesson_resources WHERE lesson_id=v_muscle_id AND file_path='/media/simulations/svt/ch1_consommation_matiere_organique/exercices/filieres-effort/index.html');
END $$;

COMMIT;
