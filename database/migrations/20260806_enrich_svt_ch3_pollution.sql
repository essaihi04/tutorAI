-- Enrichit la leçon « La pollution des milieux naturels » avec deux laboratoires
-- visuels avancés. La migration est idempotente et peut être collée telle quelle
-- dans l'éditeur SQL de Supabase.

BEGIN;

DO $$
DECLARE
    v_lesson_id uuid;
    r record;
BEGIN
    SELECT l.id INTO v_lesson_id
    FROM lessons l
    JOIN chapters c ON c.id = l.chapter_id
    WHERE c.chapter_number = 3
      AND lower(c.title_fr) LIKE '%mati%organique%inorganique%'
      AND lower(l.title_fr) LIKE '%pollution%milieux naturels%'
    ORDER BY l.created_at
    LIMIT 1;

    IF v_lesson_id IS NULL THEN
        RAISE EXCEPTION 'Leçon SVT « La pollution des milieux naturels » introuvable';
    END IF;

    UPDATE lessons
    SET duration_minutes = 110,
        learning_objectives = jsonb_build_array(
            'Identifier les sources, les polluants et les milieux récepteurs à partir de documents',
            'Expliquer la chaîne causale nutriments → prolifération algale → décomposition → hypoxie',
            'Distinguer bioaccumulation et biomagnification dans un réseau trophique',
            'Relier émissions, vent et inversion thermique à la dispersion du smog',
            'Expliquer la formation des dépôts acides et leurs effets sur les écosystèmes',
            'Comparer des stratégies de prévention, de traitement et de restauration à partir d’indicateurs'
        ),
        content = jsonb_build_object(
            'guiding_question', 'Comment une activité humaine perturbe-t-elle un milieu, et comment démontrer qu’une solution le restaure ?',
            'micro_enseignements', jsonb_build_array(
                jsonb_build_object('id','svt_ch3_pollution_diagnostic','title','1. Diagnostiquer : source → polluant → milieu → indicateur','type','activation'),
                jsonb_build_object('id','svt_ch3_pollution_eutrophisation','title','2. Enquêter : nutriments, algues et manque de O₂','type','exploration'),
                jsonb_build_object('id','svt_ch3_pollution_reseau','title','3. Suivre un polluant dans le réseau trophique','type','exploration'),
                jsonb_build_object('id','svt_ch3_pollution_air','title','4. Modéliser : émissions, météo et smog','type','exploration'),
                jsonb_build_object('id','svt_ch3_pollution_acide','title','5. Relier les émissions aux dépôts acides','type','explanation'),
                jsonb_build_object('id','svt_ch3_pollution_solutions','title','6. Décider : prévention, traitement et restauration','type','application'),
                jsonb_build_object('id','svt_ch3_pollution_bac','title','7. Argumenter comme au BAC avec des indicateurs','type','consolidation')
            ),
            'prerequisites', jsonb_build_array(
                'Lire une courbe et comparer un témoin à un essai',
                'Connaître respiration, photosynthèse et réseau trophique',
                'Utiliser le pH et une concentration comme indicateurs'
            ),
            'sections', jsonb_build_array(
                jsonb_build_object('title','Pollution des eaux','content','Les apports excessifs en nitrates et phosphates favorisent les algues. Leur décomposition augmente la demande biologique en O₂ et peut conduire à l’hypoxie.','type','modele_causal'),
                jsonb_build_object('title','Polluants persistants','content','Un polluant peut s’accumuler dans un organisme et atteindre des concentrations croissantes aux niveaux trophiques supérieurs.','type','modele_causal'),
                jsonb_build_object('title','Pollution atmosphérique','content','La concentration au sol dépend à la fois des émissions et de la dispersion par le vent et la stabilité de l’atmosphère.','type','modele_causal'),
                jsonb_build_object('title','Dépôts acides','content','SO₂ et NOₓ peuvent former des acides, être transportés puis déposés. Les effets dépendent aussi du pouvoir tampon du milieu.','type','modele_causal'),
                jsonb_build_object('title','Solutions','content','Réduire à la source, intercepter les flux et restaurer le milieu sont des actions complémentaires dont l’efficacité se mesure.','type','decision')
            ),
            'phases', jsonb_build_object(
                'activation',jsonb_build_object('duration_minutes',10,'focus',jsonb_build_array('photographies-problèmes','hypothèses')),
                'exploration',jsonb_build_object('duration_minutes',45,'focus',jsonb_build_array('AquaLab','AtmosLab','essais contrôlés')),
                'explanation',jsonb_build_object('duration_minutes',25,'focus',jsonb_build_array('chaînes causales','indicateurs','limites des modèles')),
                'application',jsonb_build_object('duration_minutes',20,'focus',jsonb_build_array('stratégies multi-barrières','comparaison avant-après')),
                'consolidation',jsonb_build_object('duration_minutes',10,'focus',jsonb_build_array('argumentation type BAC','ticket de sortie'))
            ),
            'investigation_cycle', jsonb_build_array('observer','prédire','manipuler une variable','mesurer','comparer au témoin','expliquer','proposer une solution'),
            'misconceptions', jsonb_build_array(
                jsonb_build_object('error','Les algues produisent O₂, donc un bloom augmente toujours O₂.','remediation','La respiration nocturne et surtout la décomposition de la biomasse consomment O₂ et peuvent provoquer l’hypoxie.'),
                jsonb_build_object('error','Une faible concentration dans l’eau signifie aucun risque.','remediation','Un polluant persistant peut se concentrer dans les organismes puis le long du réseau trophique.'),
                jsonb_build_object('error','Le vent supprime la pollution.','remediation','Il dilue localement mais transporte aussi le panache vers d’autres zones.'),
                jsonb_build_object('error','Planter des arbres suffit à éliminer toutes les sources.','remediation','La végétation réduit surtout l’exposition locale ; la priorité reste la réduction des émissions et des rejets.')
            ),
            'bac_method', jsonb_build_array('nommer l’indicateur','décrire la variation chiffrée','relier cause et mécanisme','conclure sans dépasser les données'),
            'exit_ticket', jsonb_build_array(
                'Reconstitue en quatre étapes le mécanisme de l’eutrophisation.',
                'Explique pourquoi un prédateur supérieur peut être le plus contaminé.',
                'Propose deux actions complémentaires et l’indicateur qui vérifiera leur efficacité.'
            )
        ),
        media_resources = jsonb_build_array(
            jsonb_build_object('type','image','url','/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/assets/reservoir-bloom.webp','caption','Réservoir marocain : zone claire et prolifération algale.','trigger','observe le réservoir et formule une hypothèse'),
            jsonb_build_object('type','simulation','url','/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/index.html','caption','AquaLab : eutrophisation, biomagnification et restauration.','trigger','ouvre le laboratoire pollution de l’eau'),
            jsonb_build_object('type','image','url','/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/assets/food-web.webp','caption','Réseau trophique aquatique pour suivre un polluant persistant.','trigger','observe le réseau trophique aquatique'),
            jsonb_build_object('type','image','url','/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/assets/restoration.webp','caption','Traitement, zone humide et bande végétalisée.','trigger','compare les dispositifs de dépollution'),
            jsonb_build_object('type','image','url','/media/simulations/svt/ch3_pollution/labs/air-dispersion/assets/urban-smog.webp','caption','Ville marocaine sous une couche de smog.','trigger','observe le smog urbain et ses sources'),
            jsonb_build_object('type','simulation','url','/media/simulations/svt/ch3_pollution/labs/air-dispersion/index.html','caption','AtmosLab : dispersion, dépôts acides et solutions.','trigger','ouvre le laboratoire pollution de l’air'),
            jsonb_build_object('type','image','url','/media/simulations/svt/ch3_pollution/labs/air-dispersion/assets/acid-rain.webp','caption','Du panache industriel au lac soumis aux dépôts acides.','trigger','observe le trajet des dépôts acides'),
            jsonb_build_object('type','image','url','/media/simulations/svt/ch3_pollution/labs/air-dispersion/assets/clean-air-transition.webp','caption','Transport collectif, filtration et énergies renouvelables.','trigger','compare les solutions pour la qualité de l’air')
        )
    WHERE id = v_lesson_id;

    FOR r IN
        SELECT * FROM (VALUES
            ('Situation-problème','image','Réservoir : du clair au bloom algal','Observer une prolifération algale et repérer les sources possibles avant toute explication.','/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/assets/reservoir-bloom.webp','observe le réservoir et formule une hypothèse','activation','beginner','["eutrophisation","nutriments","réservoir"]'::jsonb,'{"caption":"Reconstitution pédagogique générée — sans valeur documentaire locale","source_type":"ai_generated_educational_reconstruction","visual":true}'::jsonb,0),
            ('Laboratoire d''investigation','simulation','AquaLab avancé — pollution de l’eau','Trois missions avec prédictions, courbes algues-O₂, réseau trophique, solutions et carnet comparatif.','/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/index.html','ouvre le laboratoire pollution de l''eau','exploration','intermediate','["eutrophisation","O2 dissous","DBO","biomagnification","restauration"]'::jsonb,'{"kind":"advanced_virtual_lab","protocol_version":"2.0","simulation_id":"svt_ch3_aqualab_pollution_v2","is_primary":true,"llm_readable":true,"llm_controllable":true,"variants":["eutrophication","biomagnification","remediation"],"interaction_cycle":["prédire","manipuler","mesurer","comparer","expliquer"],"integrated_generated_visuals":3,"estimated_minutes":18,"viewport":"responsive_no_external_dependency"}'::jsonb,1),
            ('Réseau trophique','image','Polluant persistant dans le réseau aquatique','Identifier les niveaux trophiques avant de suivre la concentration du polluant.','/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/assets/food-web.webp','observe le réseau trophique aquatique','explanation','intermediate','["plancton","poisson","prédateur","bioaccumulation","biomagnification"]'::jsonb,'{"caption":"Reconstitution pédagogique générée","source_type":"ai_generated_educational_reconstruction","visual":true}'::jsonb,2),
            ('Solutions pour l''eau','image','Restauration multi-barrières d’un réservoir','Comparer bande végétalisée, zone humide construite et station de traitement.','/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/assets/restoration.webp','compare les dispositifs de dépollution','application','intermediate','["prévention","traitement","zone humide","restauration"]'::jsonb,'{"caption":"Reconstitution pédagogique générée","source_type":"ai_generated_educational_reconstruction","visual":true}'::jsonb,3),
            ('Situation-problème','image','Smog au-dessus d’une ville marocaine','Repérer trafic, industrie, station de mesure et couche de smog.','/media/simulations/svt/ch3_pollution/labs/air-dispersion/assets/urban-smog.webp','observe le smog urbain et ses sources','activation','beginner','["smog","trafic","industrie","PM2.5"]'::jsonb,'{"caption":"Reconstitution pédagogique générée — sans valeur documentaire locale","source_type":"ai_generated_educational_reconstruction","visual":true}'::jsonb,4),
            ('Laboratoire d''investigation','simulation','AtmosLab avancé — pollution de l’air','Trois missions sur dispersion du smog, dépôts acides et stratégie de réduction multi-actions.','/media/simulations/svt/ch3_pollution/labs/air-dispersion/index.html','ouvre le laboratoire pollution de l''air','exploration','intermediate','["dispersion","vent","inversion thermique","SO2","NOx","pluie acide","PM2.5"]'::jsonb,'{"kind":"advanced_virtual_lab","protocol_version":"2.0","simulation_id":"svt_ch3_atmoslab_pollution_v2","is_primary":true,"llm_readable":true,"llm_controllable":true,"variants":["dispersion","acid_rain","solutions"],"interaction_cycle":["prédire","manipuler","modéliser","comparer","argumenter"],"integrated_generated_visuals":3,"estimated_minutes":18,"viewport":"responsive_no_external_dependency"}'::jsonb,5),
            ('Dépôts acides','image','Du panache industriel au lac acidifié','Faire décrire transport atmosphérique, dépôt, pH et sensibilité de l’écosystème.','/media/simulations/svt/ch3_pollution/labs/air-dispersion/assets/acid-rain.webp','observe le trajet des dépôts acides','explanation','intermediate','["SO2","NOx","pH","dépôt acide","pouvoir tampon"]'::jsonb,'{"caption":"Reconstitution pédagogique générée","source_type":"ai_generated_educational_reconstruction","visual":true}'::jsonb,6),
            ('Solutions pour l''air','image','Ville en transition vers un air plus propre','Comparer transport collectif, filtration industrielle, renouvelables et ceinture verte.','/media/simulations/svt/ch3_pollution/labs/air-dispersion/assets/clean-air-transition.webp','compare les solutions pour la qualité de l''air','application','intermediate','["transport collectif","filtration","énergies renouvelables","exposition"]'::jsonb,'{"caption":"Reconstitution pédagogique générée","source_type":"ai_generated_educational_reconstruction","visual":true}'::jsonb,7)
        ) AS x(section_title,resource_type,title,description,file_path,trigger_text,phase,difficulty_tier,concepts,metadata,order_index)
    LOOP
        IF EXISTS (SELECT 1 FROM lesson_resources lr WHERE lr.lesson_id = v_lesson_id AND lr.file_path = r.file_path) THEN
            UPDATE lesson_resources
            SET section_title=r.section_title, resource_type=r.resource_type, title=r.title,
                description=r.description, trigger_text=r.trigger_text, phase=r.phase,
                difficulty_tier=r.difficulty_tier::difficulty_level, concepts=r.concepts,
                metadata=r.metadata, order_index=r.order_index
            WHERE lesson_id=v_lesson_id AND file_path=r.file_path;
        ELSE
            INSERT INTO lesson_resources
                (lesson_id,section_title,resource_type,title,description,file_path,trigger_text,phase,difficulty_tier,concepts,metadata,order_index)
            VALUES
                (v_lesson_id,r.section_title,r.resource_type,r.title,r.description,r.file_path,r.trigger_text,r.phase,r.difficulty_tier::difficulty_level,r.concepts,r.metadata,r.order_index);
        END IF;
    END LOOP;
END $$;

COMMIT;
