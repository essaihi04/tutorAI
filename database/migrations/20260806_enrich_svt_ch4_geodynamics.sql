-- Géodynamique interne — 2BAC PC BIOF
-- Met à jour les trois leçons du chapitre 4 et ajoute leurs visuels/laboratoires.
-- Migration idempotente : elle peut être réexécutée dans l'éditeur SQL Supabase.

BEGIN;

DO $migration$
DECLARE
    v_chapter_id uuid;
    v_updated integer;
    lesson_row record;
    media_row record;
    v_lesson_id uuid;
    v_phase text;
    v_concepts jsonb;
    v_metadata jsonb;
BEGIN
    SELECT c.id
      INTO v_chapter_id
      FROM public.chapters c
     WHERE c.chapter_number = 4
       AND (
            lower(c.title_fr) LIKE '%tectonique%'
         OR lower(c.title_fr) LIKE '%geologique%'
         OR lower(c.title_fr) LIKE '%géologique%'
       )
     ORDER BY c.created_at
     LIMIT 1;

    IF v_chapter_id IS NULL THEN
        RAISE EXCEPTION 'Chapitre SVT 4 de géodynamique interne introuvable';
    END IF;

    IF (
        SELECT count(*)
          FROM public.lessons
         WHERE chapter_id = v_chapter_id
           AND order_index IN (1, 2, 3)
    ) < 3 THEN
        RAISE EXCEPTION 'Les trois leçons attendues (ordre 1, 2 et 3) sont introuvables dans le chapitre %', v_chapter_id;
    END IF;

    FOR lesson_row IN
        SELECT *
          FROM (VALUES
            (1, $lesson1${"title_fr":"Les cha\u00eenes de montagnes et la tectonique des plaques","title_ar":"\u0627\u0644\u0633\u0644\u0627\u0633\u0644 \u0627\u0644\u062c\u0628\u0644\u064a\u0629 \u0648\u062a\u0643\u062a\u0648\u0646\u064a\u0629 \u0627\u0644\u0635\u0641\u0627\u0626\u062d","lesson_type":"theory","duration_minutes":120,"order_index":1,"learning_objectives":["Distinguer une cha\u00eene de subduction, une cha\u00eene d'obduction et une cha\u00eene de collision \u00e0 partir d'indices structuraux et p\u00e9trographiques","Relier les cha\u00eenes de montagnes r\u00e9centes \u00e0 la convergence des plaques lithosph\u00e9riques","Classer plis, failles et nappes de charriage et les relier aux contraintes tectoniques","Reconstituer une histoire g\u00e9ologique simple \u00e0 partir d'une carte, d'une coupe et d'indices rocheux"],"content":{"prerequisites":["Distinguer lithosph\u00e8re oc\u00e9anique et lithosph\u00e8re continentale","Reconna\u00eetre divergence et convergence","Savoir qu'une roche peut conserver la trace d'un ancien contexte"],"guiding_question":"Comment des roches oc\u00e9aniques et des couches d\u00e9form\u00e9es peuvent-elles se retrouver au sommet d'une cha\u00eene de montagnes ?","learning_path":[{"step":1,"student_action":"Observer le cycle orog\u00e9nique et rep\u00e9rer oc\u00e9an, fosse, volcanisme et relief.","teacher_move":"Faire d\u00e9crire les indices avant de nommer les m\u00e9canismes."},{"step":2,"student_action":"Comparer les coupes de subduction, d'obduction et de collision.","teacher_move":"Exiger un indice structural et un indice p\u00e9trographique pour chaque contexte."},{"step":3,"student_action":"Remettre les \u00e9tapes oc\u00e9anisation, subduction, obduction et collision dans l'ordre.","teacher_move":"Faire justifier chaque transition par un \u00e9l\u00e9ment visible."},{"step":4,"student_action":"Modifier contrainte, comportement et raccourcissement dans le laboratoire.","teacher_move":"Relier compression, comportement ductile ou cassant et structure produite."},{"step":5,"student_action":"Interpr\u00e9ter une coupe type Bac et r\u00e9diger une chronologie.","teacher_move":"Demander : indice observ\u00e9 \u2192 processus \u2192 conclusion chronologique."}],"micro_enseignements":[{"id":"svt_ch4_l1_observer_cycle","title":"1. J'observe le cycle d'une cha\u00eene","type":"observation","resources":["cycle_orogenique","geo_lab_chains"]},{"id":"svt_ch4_l1_subduction","title":"2. Je reconnais une subduction","type":"processus","resources":["zone_subduction"]},{"id":"svt_ch4_l1_obduction_collision","title":"3. Je distingue obduction et collision","type":"comparaison","resources":["collision_obduction"]},{"id":"svt_ch4_l1_deformations","title":"4. Je relie contraintes et d\u00e9formations","type":"manipulation","resources":["plis_failles_charriage","geo_lab_deformations"]},{"id":"svt_ch4_l1_bac","title":"5. Je reconstitue une histoire g\u00e9ologique","type":"application","resources":["geo_lab_chains"]},{"id":"svt_ch4_l1_validation","title":"6. Je conclus \u00e0 partir des indices","type":"evaluation","resources":[]}],"phases":{"activation":{"duration_minutes":10,"focus_micro_enseignements":["svt_ch4_l1_observer_cycle"]},"exploration":{"duration_minutes":30,"focus_micro_enseignements":["svt_ch4_l1_subduction","svt_ch4_l1_obduction_collision"]},"explanation":{"duration_minutes":30,"focus_micro_enseignements":["svt_ch4_l1_deformations"]},"application":{"duration_minutes":35,"focus_micro_enseignements":["svt_ch4_l1_bac"]},"consolidation":{"duration_minutes":15,"focus_micro_enseignements":["svt_ch4_l1_validation"]}},"interactive_exercises":[{"id":"orogenic_timeline_lab","type":"geological_timeline","instruction":"Ordonner quatre \u00e9tapes et justifier chaque \u00e9tape par un indice visible","difficulty":"intermediate","llm_reads":["student_answer","errors","attempts","observed_hotspots"]},{"id":"tectonic_deformation_lab","type":"constraint_deformation_experiment","instruction":"Tester les param\u00e8tres qui produisent pli, faille inverse et nappe","difficulty":"advanced","llm_reads":["deformation_parameters","deformation_tests","observations"]}],"misconceptions":[{"error":"Une montagne se forme seulement par volcanisme.","remediation":"Comparer l'arc volcanique de subduction \u00e0 la racine crustale et aux nappes d'une collision."},{"error":"Obduction et subduction sont synonymes.","remediation":"Subduction : lithosph\u00e8re oc\u00e9anique plongeante ; obduction : fragment oc\u00e9anique transport\u00e9 sur le continent."},{"error":"Toute faille est une faille normale.","remediation":"Observer le d\u00e9placement des compartiments et relier faille inverse et chevauchement \u00e0 la compression."},{"error":"Un pli est une cassure.","remediation":"Le pli est une d\u00e9formation continue ; la faille est une d\u00e9formation discontinue avec rupture."}],"differentiation":{"support":"Commencer par trois indices visuels : fosse, ophiolite et racine crustale.","standard":"Comparer les trois contextes puis obtenir les trois d\u00e9formations dans la simulation.","challenge":"Reconstituer une chronologie compl\u00e8te \u00e0 partir d'une coupe non l\u00e9gend\u00e9e et d'assemblages rocheux."},"exit_ticket":["Cite un indice de subduction et un indice de collision.","Explique pourquoi une ophiolite constitue la trace d'un ancien oc\u00e9an.","Relie compression, pli, faille inverse et nappe de charriage."]},"media_resources":[{"type":"image","url":"/media/images/svt/ch4_geodynamique_interne/cycle_orogenique_3d.webp","caption":"Cycle visuel : oc\u00e9anisation, subduction, obduction puis collision.","trigger":"observe le cycle orog\u00e9nique"},{"type":"image","url":"/media/images/svt/ch4_geodynamique_interne/zone_subduction_3d.webp","caption":"Coupe 3D d'une zone de subduction : fosse, plan sismique, fusion partielle et arc volcanique.","trigger":"observe la zone de subduction"},{"type":"image","url":"/media/images/svt/ch4_geodynamique_interne/collision_obduction_3d.webp","caption":"Collision continentale : raccourcissement, racine crustale, nappes et fragment ophiolitique.","trigger":"compare obduction et collision"},{"type":"image","url":"/media/images/svt/ch4_geodynamique_interne/plis_failles_charriage.webp","caption":"Bloc tectonique : plis, faille inverse, chevauchement et nappe de charriage.","trigger":"observe les d\u00e9formations tectoniques"},{"type":"simulation","url":"/media/simulations/svt/ch4_geodynamique_interne/index.html?variant=chains","caption":"Laboratoire avanc\u00e9 : reconstruire une cha\u00eene puis produire les d\u00e9formations de compression.","trigger":"lance le laboratoire des cha\u00eenes de montagnes"}]}$lesson1$::jsonb),
            (2, $lesson2${"title_fr":"Le m\u00e9tamorphisme et sa relation avec la tectonique","title_ar":"\u0627\u0644\u062a\u062d\u0648\u0644 \u0648\u0639\u0644\u0627\u0642\u062a\u0647 \u0628\u062a\u0643\u062a\u0648\u0646\u064a\u0629 \u0627\u0644\u0635\u0641\u0627\u0626\u062d","lesson_type":"theory","duration_minutes":90,"order_index":2,"learning_objectives":["D\u00e9finir le m\u00e9tamorphisme comme une transformation min\u00e9ralogique et structurale \u00e0 l'\u00e9tat solide","Utiliser les min\u00e9raux index et un diagramme pression-temp\u00e9rature pour d\u00e9terminer les conditions de formation d'une roche","Relier schiste bleu et \u00e9clogite \u00e0 la subduction et gneiss au m\u00e9tamorphisme r\u00e9gional de collision","Distinguer m\u00e9tamorphisme dynamique, thermodynamique et thermique de contact"],"content":{"prerequisites":["Lire deux axes gradu\u00e9s","Distinguer pression et temp\u00e9rature","Reconna\u00eetre les contextes de subduction et de collision"],"guiding_question":"Comment une roche peut-elle r\u00e9v\u00e9ler la pression, la temp\u00e9rature et le contexte tectonique qu'elle a subis ?","learning_path":[{"step":1,"student_action":"Comparer quatre roches et leurs lames minces.","teacher_move":"Faire relever couleur, min\u00e9raux et foliation sans donner imm\u00e9diatement le faci\u00e8s."},{"step":2,"student_action":"Associer glaucophane, grenat, jad\u00e9ite et foliation \u00e0 des roches.","teacher_move":"Introduire le min\u00e9ral index comme indicateur d'un domaine de stabilit\u00e9."},{"step":3,"student_action":"D\u00e9placer un point sur le diagramme P-T.","teacher_move":"Faire lire d'abord P et T, puis le faci\u00e8s, enfin le contexte."},{"step":4,"student_action":"Enregistrer schiste bleu, \u00e9clogite, gneiss et corn\u00e9enne.","teacher_move":"Comparer HP-BT, m\u00e9tamorphisme r\u00e9gional et m\u00e9tamorphisme de contact."},{"step":5,"student_action":"Tracer mentalement ou graphiquement un trajet m\u00e9tamorphique.","teacher_move":"Demander une chronologie prograde puis r\u00e9trograde fond\u00e9e sur les min\u00e9raux."}],"micro_enseignements":[{"id":"svt_ch4_l2_roches","title":"1. J'observe les roches et les lames minces","type":"observation","resources":["roches_metamorphiques"]},{"id":"svt_ch4_l2_index","title":"2. J'identifie les min\u00e9raux index","type":"concept","resources":["roches_metamorphiques"]},{"id":"svt_ch4_l2_pt","title":"3. Je manipule pression et temp\u00e9rature","type":"manipulation","resources":["geo_lab_metamorphism"]},{"id":"svt_ch4_l2_contextes","title":"4. Je relie faci\u00e8s et contexte tectonique","type":"raisonnement","resources":["zone_subduction","collision_obduction","geo_lab_metamorphism"]},{"id":"svt_ch4_l2_bac","title":"5. J'interpr\u00e8te une s\u00e9rie m\u00e9tamorphique","type":"application","resources":["geo_lab_metamorphism"]}],"phases":{"activation":{"duration_minutes":8,"focus_micro_enseignements":["svt_ch4_l2_roches"]},"exploration":{"duration_minutes":20,"focus_micro_enseignements":["svt_ch4_l2_index","svt_ch4_l2_pt"]},"explanation":{"duration_minutes":25,"focus_micro_enseignements":["svt_ch4_l2_contextes"]},"application":{"duration_minutes":25,"focus_micro_enseignements":["svt_ch4_l2_bac"]},"consolidation":{"duration_minutes":12,"focus_micro_enseignements":["svt_ch4_l2_bac"]}},"interactive_exercises":[{"id":"pt_metamorphic_lab","type":"pressure_temperature_exploration","instruction":"Explorer les domaines P-T et enregistrer quatre signatures min\u00e9ralogiques","difficulty":"advanced","llm_reads":["pt_conditions","metamorphic_records","minerals","context","errors"]}],"misconceptions":[{"error":"Le m\u00e9tamorphisme fait fondre enti\u00e8rement la roche.","remediation":"Le m\u00e9tamorphisme transforme la roche \u00e0 l'\u00e9tat solide ; la fusion partielle marque le passage vers l'anatexie."},{"error":"Une m\u00eame roche correspond toujours \u00e0 une seule temp\u00e9rature.","remediation":"Un faci\u00e8s occupe un domaine P-T ; les assemblages min\u00e9raux apportent l'indice."},{"error":"Forte pression signifie toujours forte temp\u00e9rature.","remediation":"La subduction froide produit un m\u00e9tamorphisme HP-BT, notamment le schiste bleu."},{"error":"Tout m\u00e9tamorphisme est un m\u00e9tamorphisme de contact.","remediation":"Comparer l'aur\u00e9ole limit\u00e9e d'une intrusion au m\u00e9tamorphisme r\u00e9gional d'une cha\u00eene."}],"differentiation":{"support":"Utiliser d'abord les quatre pr\u00e9r\u00e9glages rocheux du diagramme.","standard":"Modifier librement P et T puis expliquer chaque faci\u00e8s obtenu.","challenge":"Reconstituer un trajet prograde et r\u00e9trograde et l'associer \u00e0 une subduction."},"exit_ticket":["Quel min\u00e9ral index caract\u00e9rise le schiste bleu ?","Pourquoi l'\u00e9clogite indique-t-elle une subduction profonde ?","Distingue m\u00e9tamorphisme dynamique, r\u00e9gional thermodynamique et thermique de contact."]},"media_resources":[{"type":"image","url":"/media/images/svt/ch4_geodynamique_interne/roches_metamorphiques_lames_minces.webp","caption":"Roches et lames minces : schiste vert, schiste bleu, \u00e9clogite et gneiss.","trigger":"observe les roches m\u00e9tamorphiques"},{"type":"image","url":"/media/images/svt/ch4_geodynamique_interne/zone_subduction_3d.webp","caption":"La plaque froide entra\u00eene des roches vers des conditions de haute pression et basse temp\u00e9rature.","trigger":"relie subduction et m\u00e9tamorphisme"},{"type":"image","url":"/media/images/svt/ch4_geodynamique_interne/collision_obduction_3d.webp","caption":"L'\u00e9paississement crustal d'une collision produit un m\u00e9tamorphisme r\u00e9gional.","trigger":"relie collision et m\u00e9tamorphisme"},{"type":"simulation","url":"/media/simulations/svt/ch4_geodynamique_interne/index.html?variant=metamorphism","caption":"Laboratoire P-T : manipuler pression et temp\u00e9rature, identifier min\u00e9raux, faci\u00e8s et contexte.","trigger":"lance le laboratoire pression temp\u00e9rature"}]}$lesson2$::jsonb),
            (3, $lesson3${"title_fr":"La granitisation et sa relation avec le m\u00e9tamorphisme","title_ar":"\u0627\u0644\u063a\u0631\u0627\u0646\u062a\u0629 \u0648\u0639\u0644\u0627\u0642\u062a\u0647\u0627 \u0628\u0627\u0644\u062a\u062d\u0648\u0644","lesson_type":"theory","duration_minutes":90,"order_index":3,"learning_objectives":["Expliquer l'origine du granite d'anatexie par fusion partielle profonde de la cro\u00fbte continentale","Relier granite d'anatexie, migmatite et m\u00e9tamorphisme r\u00e9gional de haut degr\u00e9","Expliquer la mise en place d'un granite intrusif et la formation d'une aur\u00e9ole de m\u00e9tamorphisme de contact","Distinguer granite d'anatexie et granite intrusif \u00e0 partir d'une carte, d'une coupe et des roches encaissantes"],"content":{"prerequisites":["Distinguer transformation \u00e0 l'\u00e9tat solide et fusion partielle","Reconna\u00eetre gneiss, migmatite et granite","Lire une coupe g\u00e9ologique simple"],"guiding_question":"Quels indices permettent de savoir si un granite s'est form\u00e9 sur place par anatexie ou s'est inject\u00e9 dans des roches plus anciennes ?","learning_path":[{"step":1,"student_action":"Observer la coupe comparant anatexie et intrusion.","teacher_move":"Faire d\u00e9crire contacts, largeur des transformations et roches voisines."},{"step":2,"student_action":"Rep\u00e9rer gneiss, migmatite, pluton et aur\u00e9ole.","teacher_move":"Construire la cha\u00eene m\u00e9tamorphisme intense \u2192 fusion partielle \u2192 magma granitique."},{"step":3,"student_action":"Classer six indices dans le laboratoire.","teacher_move":"Exiger une justification spatiale pour chaque indice."},{"step":4,"student_action":"Comparer la relation granite\u2013encaissant dans les deux cas.","teacher_move":"Anatexie : transition r\u00e9gionale ; intrusion : contact net et aur\u00e9ole limit\u00e9e."},{"step":5,"student_action":"Interpr\u00e9ter une carte ou une coupe type Bac.","teacher_move":"Faire r\u00e9diger une conclusion en trois preuves."}],"micro_enseignements":[{"id":"svt_ch4_l3_observer","title":"1. J'observe deux contextes granitiques","type":"observation","resources":["granitisation_comparee"]},{"id":"svt_ch4_l3_anatexie","title":"2. Je relie migmatite, anatexie et granite","type":"processus","resources":["granitisation_comparee"]},{"id":"svt_ch4_l3_intrusion","title":"3. Je relie pluton et m\u00e9tamorphisme de contact","type":"processus","resources":["granitisation_comparee"]},{"id":"svt_ch4_l3_classer","title":"4. Je classe les indices","type":"manipulation","resources":["geo_lab_granitization"]},{"id":"svt_ch4_l3_bac","title":"5. Je conclus \u00e0 partir d'une coupe","type":"application","resources":["geo_lab_granitization"]}],"phases":{"activation":{"duration_minutes":8,"focus_micro_enseignements":["svt_ch4_l3_observer"]},"exploration":{"duration_minutes":22,"focus_micro_enseignements":["svt_ch4_l3_anatexie","svt_ch4_l3_intrusion"]},"explanation":{"duration_minutes":25,"focus_micro_enseignements":["svt_ch4_l3_classer"]},"application":{"duration_minutes":25,"focus_micro_enseignements":["svt_ch4_l3_bac"]},"consolidation":{"duration_minutes":10,"focus_micro_enseignements":["svt_ch4_l3_bac"]}},"interactive_exercises":[{"id":"granite_evidence_lab","type":"geological_evidence_sorting","instruction":"Classer six indices entre granite d'anatexie et granite intrusif","difficulty":"advanced","llm_reads":["granite_assignments","expected_answer","errors","attempts"]}],"misconceptions":[{"error":"Tout granite est un granite d'anatexie.","remediation":"Comparer continuit\u00e9 avec la migmatite et limites nettes d'un pluton intrusif."},{"error":"Le granite d'anatexie est une roche m\u00e9tamorphique non fondue.","remediation":"L'anatexie correspond \u00e0 une fusion partielle ; le liquide cristallise ensuite en granite."},{"error":"Une aur\u00e9ole de contact est r\u00e9gionale et tr\u00e8s large.","remediation":"L'aur\u00e9ole thermique entoure localement une intrusion ; elle est limit\u00e9e dans l'espace."},{"error":"La migmatite ne contient que du granite.","remediation":"La migmatite associe des parties m\u00e9tamorphiques et des parties issues de fusion partielle."}],"differentiation":{"support":"Comparer seulement deux indices : migmatite et aur\u00e9ole de contact.","standard":"Classer les six indices puis justifier les deux mod\u00e8les.","challenge":"Interpr\u00e9ter une carte d'affleurements et proposer l'ordre m\u00e9tamorphisme\u2013fusion\u2013intrusion\u2013\u00e9rosion."},"exit_ticket":["D\u00e9finis l'anatexie en une phrase.","Cite deux indices d'un granite intrusif.","Explique la relation entre m\u00e9tamorphisme de haut degr\u00e9, migmatite et granite d'anatexie."]},"media_resources":[{"type":"image","url":"/media/images/svt/ch4_geodynamique_interne/granitisation_anatexie_intrusion.webp","caption":"Comparaison visuelle : granite d'anatexie dans les migmatites et pluton intrusif entour\u00e9 d'une aur\u00e9ole.","trigger":"compare les deux granites"},{"type":"image","url":"/media/images/svt/ch4_geodynamique_interne/roches_metamorphiques_lames_minces.webp","caption":"Du gneiss \u00e0 la migmatite : les roches enregistrent l'augmentation du degr\u00e9 m\u00e9tamorphique.","trigger":"observe gneiss et migmatite"},{"type":"simulation","url":"/media/simulations/svt/ch4_geodynamique_interne/index.html?variant=granitization","caption":"Laboratoire de granitisation : classer les indices d'anatexie, d'intrusion et de m\u00e9tamorphisme de contact.","trigger":"lance le laboratoire de granitisation"}]}$lesson3$::jsonb)
          ) AS payload(order_index, lesson)
    LOOP
        UPDATE public.lessons
           SET title_fr = lesson_row.lesson ->> 'title_fr',
               title_ar = lesson_row.lesson ->> 'title_ar',
               lesson_type = (lesson_row.lesson ->> 'lesson_type')::lesson_type,
               duration_minutes = (lesson_row.lesson ->> 'duration_minutes')::integer,
               learning_objectives = lesson_row.lesson -> 'learning_objectives',
               content = lesson_row.lesson -> 'content',
               media_resources = lesson_row.lesson -> 'media_resources'
         WHERE chapter_id = v_chapter_id
           AND order_index = lesson_row.order_index
        RETURNING id INTO v_lesson_id;

        GET DIAGNOSTICS v_updated = ROW_COUNT;
        IF v_updated <> 1 THEN
            RAISE EXCEPTION 'Mise à jour ambiguë pour la leçon d''ordre % (lignes modifiées : %)', lesson_row.order_index, v_updated;
        END IF;

        CASE lesson_row.order_index
            WHEN 1 THEN v_concepts := '["géodynamique interne","subduction","obduction","collision","plis","failles inverses","nappes de charriage"]'::jsonb;
            WHEN 2 THEN v_concepts := '["métamorphisme","pression","température","minéraux index","schiste bleu","éclogite","gneiss"]'::jsonb;
            WHEN 3 THEN v_concepts := '["granitisation","anatexie","migmatite","pluton intrusif","métamorphisme de contact"]'::jsonb;
        END CASE;

        FOR media_row IN
            SELECT item, ordinality::integer AS media_order
              FROM jsonb_array_elements(lesson_row.lesson -> 'media_resources')
                   WITH ORDINALITY AS media(item, ordinality)
        LOOP
            v_phase := CASE
                WHEN media_row.item ->> 'type' = 'simulation' THEN 'exploration'
                WHEN media_row.media_order = 1 THEN 'activation'
                WHEN lesson_row.order_index = 3 THEN 'application'
                ELSE 'explanation'
            END;

            IF media_row.item ->> 'type' = 'simulation' THEN
                v_metadata := jsonb_build_object(
                    'kind', 'advanced_virtual_lab',
                    'protocol_version', '1.0',
                    'simulation_id', 'svt_internal_geodynamics_advanced_lab',
                    'is_primary', true,
                    'llm_readable', true,
                    'llm_controllable', true,
                    'variants', jsonb_build_array('chains','deformations','metamorphism','granitization'),
                    'commands', jsonb_build_array(
                        'start','set_variant','reset','place_stage',
                        'set_deformation_parameters','run_deformation_test',
                        'set_pt','record_pt','assign_granite_evidence',
                        'check','reveal_hint','highlight'
                    ),
                    'integrated_generated_visuals', 6,
                    'viewport', 'responsive_native',
                    'estimated_minutes', 18
                );
            ELSE
                v_metadata := jsonb_build_object(
                    'source_type', 'ai_generated_educational_reconstruction',
                    'visual', true,
                    'generated_for_curriculum', true,
                    'caption', media_row.item ->> 'caption'
                );
            END IF;

            IF EXISTS (
                SELECT 1
                  FROM public.lesson_resources existing
                 WHERE existing.lesson_id = v_lesson_id
                   AND existing.file_path = media_row.item ->> 'url'
            ) THEN
                UPDATE public.lesson_resources
                   SET section_title = CASE
                           WHEN media_row.item ->> 'type' = 'simulation'
                           THEN 'Laboratoire virtuel avancé'
                           ELSE 'Document visuel'
                       END,
                       resource_type = media_row.item ->> 'type',
                       title = left(media_row.item ->> 'caption', 200),
                       description = media_row.item ->> 'caption',
                       trigger_text = media_row.item ->> 'trigger',
                       phase = v_phase,
                       difficulty_tier = 'intermediate'::difficulty_level,
                       concepts = v_concepts,
                       metadata = v_metadata,
                       order_index = media_row.media_order - 1
                 WHERE lesson_id = v_lesson_id
                   AND file_path = media_row.item ->> 'url';
            ELSE
                INSERT INTO public.lesson_resources (
                    lesson_id, section_title, resource_type, title, description,
                    file_path, trigger_text, phase, difficulty_tier,
                    concepts, metadata, order_index
                )
                VALUES (
                    v_lesson_id,
                    CASE
                        WHEN media_row.item ->> 'type' = 'simulation'
                        THEN 'Laboratoire virtuel avancé'
                        ELSE 'Document visuel'
                    END,
                    media_row.item ->> 'type',
                    left(media_row.item ->> 'caption', 200),
                    media_row.item ->> 'caption',
                    media_row.item ->> 'url',
                    media_row.item ->> 'trigger',
                    v_phase,
                    'intermediate'::difficulty_level,
                    v_concepts,
                    v_metadata,
                    media_row.media_order - 1
                );
            END IF;
        END LOOP;
    END LOOP;
END
$migration$;

COMMIT;

