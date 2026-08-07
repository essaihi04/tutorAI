-- Chimie 2e BAC : 14 leçons, 5 laboratoires avancés et 15 missions manipulables.
-- Migration idempotente : elle crée les leçons absentes et actualise les autres.
DO $migration$
DECLARE
    v_subject_id uuid;
    v_chapter_id uuid;
    v_lesson_id uuid;
    spec jsonb;
    mission jsonb;
    media jsonb;
    item jsonb;
    resource_path text;
    simulation_id text;
BEGIN
    SELECT id INTO v_subject_id
    FROM public.subjects
    WHERE lower(name_fr) LIKE '%chimi%'
    ORDER BY order_index, id
    LIMIT 1;

    IF v_subject_id IS NULL THEN
        RAISE EXCEPTION 'Matière Chimie introuvable';
    END IF;

    FOR spec IN
        SELECT value FROM jsonb_array_elements($specs$
        [
          {"n":1,"fr":"Transformations lentes et transformations rapides","ar":"التحولات البطيئة والتحولات السريعة","question":"Comment accélérer une transformation sans modifier son état final ?","objectives":["Classer une transformation à partir de son échelle de temps","Tester séparément concentration, température et catalyseur","Distinguer facteur cinétique et état final"],"focus":"facteurs cinétiques","formula":"k augmente quand la température ou l'efficacité catalytique augmente","bac":"Comparer deux essais qui ne diffèrent que par un seul facteur.","error":"Un catalyseur augmente la quantité finale de produit.","lab":"/media/simulations/chimie/labs/cinetique/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-cinetique.webp","caption":"Spectrophotomètre, bain thermostaté, concentrations et catalyseur.","missions":[{"id":"facteurs","title":"Facteurs cinétiques","trigger":"teste les facteurs cinétiques"}]},
          {"n":2,"fr":"Suivi temporel dune transformation chimique - Vitesse de reaction","ar":"التتبع الزمني لتحول كيميائي - سرعة التفاعل","question":"Comment une série de mesures permet-elle de retrouver vitesse et temps de demi-réaction ?","objectives":["Relier absorbance et avancement","Tracer et interpréter une courbe temporelle","Déterminer t½ et une vitesse de réaction"],"focus":"suivi temporel","formula":"A(t) = A₀e⁻ᵏᵗ et t½ = ln(2)/k dans le modèle proposé","bac":"Nommer les axes, localiser la moitié de la valeur initiale puis projeter sur l'axe du temps.","error":"Le temps de demi-réaction est la moitié de la durée totale observée.","lab":"/media/simulations/chimie/labs/cinetique/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-cinetique.webp","caption":"Acquisition spectrophotométrique d'une courbe A(t).","missions":[{"id":"suivi","title":"Suivi A(t) et t½","trigger":"mesure le temps de demi-réaction"}]},
          {"n":3,"fr":"Decroissance radioactive","ar":"التناقص الإشعاعي","question":"Comment un phénomène aléatoire à l'échelle du noyau devient-il prévisible pour une population ?","objectives":["Simuler des désintégrations aléatoires","Exploiter la loi N(t) et la demi-vie","Déterminer un âge radiométrique"],"focus":"décroissance et datation","formula":"N(t) = N₀·2⁻ᵗ/ᵗ½","bac":"Exprimer d'abord N/N₀, compter les demi-vies puis convertir en durée.","error":"Tous les noyaux d'un échantillon se désintègrent au même instant.","lab":"/media/simulations/chimie/labs/nucleaire/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-nucleaire.webp","caption":"Détection protégée, traces et échantillon de datation.","missions":[{"id":"demi-vie","title":"Demi-vie aléatoire","trigger":"observe la décroissance radioactive"},{"id":"datation","title":"Datation isotopique","trigger":"date un échantillon"}]},
          {"n":4,"fr":"Noyaux, masse et energie","ar":"النوى والكتلة والطاقة","question":"Où se cache l'énergie libérée lors d'une transformation nucléaire ?","objectives":["Calculer un défaut de masse","Relier défaut de masse et énergie de liaison","Interpréter la courbe d'énergie par nucléon"],"focus":"défaut de masse et stabilité","formula":"Eₗ = Δm·c² ; 1 u·c² = 931,5 MeV","bac":"Calculer Δm avec des unités cohérentes puis annoncer le signe et l'unité de l'énergie.","error":"La masse se conserve séparément de l'énergie dans une réaction nucléaire.","lab":"/media/simulations/chimie/labs/nucleaire/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-nucleaire.webp","caption":"Instrumentation de mesure nucléaire et courbe de stabilité.","missions":[{"id":"liaison","title":"Énergie de liaison","trigger":"compare la stabilité des noyaux"}]},
          {"n":5,"fr":"Transformations chimiques seffectuant dans les 2 sens","ar":"التحولات الكيميائية التي تحدث في الاتجاهين","question":"Comment prouver que réactifs et produits réagissent simultanément ?","objectives":["Reconnaître une transformation réversible","Lire l'évolution des espèces dans les deux sens","Décrire l'équilibre comme dynamique"],"focus":"réversibilité","formula":"À l'équilibre : v_directe = v_inverse","bac":"Distinguer absence d'évolution macroscopique et arrêt microscopique.","error":"À l'équilibre, les réactions directe et inverse sont arrêtées.","lab":"/media/simulations/chimie/labs/equilibres/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-equilibres.webp","caption":"Gradients de couleur d'un système chimique réversible.","missions":[{"id":"equilibre","title":"Équilibre dynamique","trigger":"observe les deux sens de réaction"}]},
          {"n":6,"fr":"Evolution spontanee dun systeme chimique","ar":"التطور التلقائي لمجموعة كيميائية","question":"Peut-on prévoir le sens d'évolution avant toute observation ?","objectives":["Calculer un quotient de réaction initial","Comparer Qᵣ,i à K","Prévoir le sens spontané"],"focus":"critère d'évolution spontanée","formula":"Qᵣ,i < K : sens direct ; Qᵣ,i > K : sens inverse","bac":"Écrire Qᵣ, remplacer par les valeurs initiales, comparer à K puis conclure en une phrase.","error":"Le système évolue toujours dans le sens écrit de l'équation.","lab":"/media/simulations/chimie/labs/equilibres/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-equilibres.webp","caption":"Système coloré permettant de visualiser le sens d'évolution.","missions":[{"id":"equilibre","title":"Comparer Qᵣ et K","trigger":"prévois le sens spontané"}]},
          {"n":7,"fr":"Evolution dun systeme chimique vers lequilibre","ar":"تطور مجموعة كيميائية نحو حالة التوازن","question":"Comment calculer la composition atteinte lorsque Qᵣ devient égal à K ?","objectives":["Construire un tableau d'avancement","Résoudre la condition Qᵣ,f = K","Interpréter la composition d'équilibre"],"focus":"composition d'équilibre","formula":"À l'état final d'équilibre : Qᵣ,f = K","bac":"Exprimer toutes les concentrations en fonction de ξ avant d'utiliser Qᵣ,f = K.","error":"À l'équilibre, réactifs et produits ont nécessairement la même concentration.","lab":"/media/simulations/chimie/labs/equilibres/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-equilibres.webp","caption":"Évolution progressive des concentrations vers l'équilibre.","missions":[{"id":"equilibre","title":"Composition à l'équilibre","trigger":"calcule la composition à l'équilibre"}]},
          {"n":8,"fr":"Reactions acido-basiques","ar":"التفاعلات حمض-قاعدة","question":"Comment le pH révèle-t-il l'état d'une réaction acido-basique et l'équivalence d'un dosage ?","objectives":["Relier Kₐ, pKₐ, pH et taux d'avancement","Distinguer transformation totale et limitée","Repérer l'équivalence d'un dosage pH-métrique"],"focus":"équilibre acido-basique et dosage","formula":"pH = −log[H₃O⁺] ; à l'équivalence n(acide) = n(base) ajoutée","bac":"Pour un dosage, établir la relation stœchiométrique à l'équivalence avant l'application numérique.","error":"Une solution acide faible est toujours moins concentrée qu'une solution d'acide fort.","lab":"/media/simulations/chimie/labs/equilibres/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-equilibres.webp","caption":"Burette, pH-mètre et solutions acido-basiques.","missions":[{"id":"acide-base","title":"Dissociation d'un acide faible","trigger":"mesure le pH d'un acide faible"},{"id":"dosage","title":"Dosage pH-métrique","trigger":"cherche le volume équivalent"}]},
          {"n":9,"fr":"Reactions de precipitation","ar":"تفاعلات الترسيب","question":"À partir de quelles concentrations un solide apparaît-il ?","objectives":["Écrire un produit ionique","Comparer Q à Kₛ","Prévoir précipitation ou dissolution"],"focus":"produit de solubilité","formula":"Q > Kₛ : précipitation ; Q < Kₛ : solution non saturée","bac":"Respecter les exposants stœchiométriques dans le produit ionique.","error":"Mélanger deux ions formant un sel peu soluble produit toujours un précipité visible.","lab":"/media/simulations/chimie/labs/equilibres/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-equilibres.webp","caption":"Solutions limpides et apparition d'un précipité blanc.","missions":[{"id":"precipitation","title":"Seuil de précipitation","trigger":"fais apparaître un précipité"}]},
          {"n":10,"fr":"Piles electrochimiques","ar":"الأعمدة الكهروكيميائية","question":"Comment une transformation spontanée impose-t-elle une tension et un courant ?","objectives":["Identifier anode, cathode et sens des électrons","Calculer une tension en conditions non standard","Relier charge débitée et matière transformée"],"focus":"pile Daniell","formula":"E = E° − (0,0592/n) log Q à 25 °C","bac":"Écrire les demi-équations puis vérifier que les électrons vont de l'anode vers la cathode.","error":"Les électrons traversent le pont salin.","lab":"/media/simulations/chimie/labs/electrochimie/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-electrochimie.webp","caption":"Pile Daniell réelle, pont salin et voltmètre.","missions":[{"id":"pile","title":"Pile Daniell en charge","trigger":"branche et mesure la pile"}]},
          {"n":11,"fr":"Electrolyse","ar":"التحليل الكهربائي","question":"Comment piloter une transformation non spontanée avec un générateur ?","objectives":["Repérer les réactions aux électrodes","Calculer la charge Q = IΔt","Utiliser la loi de Faraday pour prévoir masse ou volume"],"focus":"loi de Faraday","formula":"n(e⁻) = IΔt/F","bac":"Convertir le temps en secondes et utiliser le nombre d'électrons de la demi-équation.","error":"La masse déposée dépend de la tension seule.","lab":"/media/simulations/chimie/labs/electrochimie/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-electrochimie.webp","caption":"Cellule d'électrolyse avec bulles et dépôt métallique.","missions":[{"id":"electrolyse","title":"Électrolyse quantitative","trigger":"produis un dépôt par électrolyse"}]},
          {"n":12,"fr":"Esterification et hydrolyse","ar":"الأسترة والحلمأة","question":"Pourquoi chauffer accélère-t-il l'estérification sans la rendre totale ?","objectives":["Reconnaître estérification et hydrolyse","Calculer le rendement d'équilibre","Distinguer facteurs cinétiques et déplacement d'équilibre"],"focus":"estérification limitée et réversible","formula":"K = [ester][eau]/([acide][alcool])","bac":"Séparer la question vitesse de la question rendement avant de justifier le rôle du reflux.","error":"Le chauffage à reflux augmente toujours le rendement final.","lab":"/media/simulations/chimie/labs/synthese-organique/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-synthese.webp","caption":"Montage à reflux et séparation du produit organique.","missions":[{"id":"esterification","title":"Équilibre d'estérification","trigger":"mesure le rendement d'estérification"},{"id":"vitesse","title":"Cinétique sous reflux","trigger":"teste chauffage et catalyse"}]},
          {"n":13,"fr":"Controle de levolution dun systeme chimique","ar":"التحكم في تطور مجموعة كيميائية","question":"Quelles décisions expérimentales accélèrent la synthèse et lesquelles augmentent le rendement ?","objectives":["Choisir un excès de réactif pertinent","Expliquer l'effet du retrait d'un produit","Comparer réaction réversible et transformation quasi totale"],"focus":"contrôle cinétique et thermodynamique","formula":"Déplacer l'équilibre : modifier Q ; accélérer : modifier k","bac":"Pour chaque action, préciser si elle agit sur la vitesse, le quotient de réaction ou les deux.","error":"Un catalyseur déplace l'équilibre vers les produits.","lab":"/media/simulations/chimie/labs/synthese-organique/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-synthese.webp","caption":"Reflux, retrait d'eau et contrôle du rendement de synthèse.","missions":[{"id":"optimisation","title":"Optimisation du rendement","trigger":"optimise la synthèse"}]},
          {"n":14,"fr":"Phenomenes oxydo-reductions","ar":"ظواهر الأكسدة والاختزال","question":"Comment prévoir qui cède les électrons avant de fermer le circuit ?","objectives":["Identifier oxydant et réducteur","Équilibrer des demi-équations électroniques","Prévoir le sens spontané par la tension ou Qᵣ"],"focus":"transfert d'électrons","formula":"Oxydation à l'anode ; réduction à la cathode","bac":"Conserver atomes et charges dans chaque demi-équation avant de les additionner.","error":"Une oxydation est nécessairement une réaction avec le dioxygène.","lab":"/media/simulations/chimie/labs/electrochimie/index.html","image":"/media/simulations/chimie/shared/assets/laboratoire-electrochimie.webp","caption":"Électrodes de zinc et cuivre et circulation des électrons.","missions":[{"id":"oxydoreduction","title":"Sens d'oxydo-réduction","trigger":"identifie le donneur d'électrons"}]}
        ]
        $specs$::jsonb)
    LOOP
        SELECT id INTO v_chapter_id
        FROM public.chapters
        WHERE subject_id = v_subject_id
          AND chapter_number = (spec->>'n')::integer
        ORDER BY id
        LIMIT 1;

        IF v_chapter_id IS NULL THEN
            RAISE EXCEPTION 'Chapitre de chimie % introuvable', spec->>'n';
        END IF;

        media := jsonb_build_array(jsonb_build_object(
            'type', 'image',
            'url', spec->>'image',
            'caption', spec->>'caption',
            'trigger', 'observe le montage de ' || (spec->>'focus')
        ));
        FOR mission IN SELECT value FROM jsonb_array_elements(spec->'missions')
        LOOP
            media := media || jsonb_build_array(jsonb_build_object(
                'type', 'simulation',
                'url', (spec->>'lab') || '?mission=' || (mission->>'id'),
                'caption', 'Laboratoire manipulable : ' || (mission->>'title') || '.',
                'trigger', mission->>'trigger'
            ));
        END LOOP;

        SELECT id INTO v_lesson_id
        FROM public.lessons
        WHERE chapter_id = v_chapter_id
        ORDER BY order_index, created_at, id
        LIMIT 1;

        IF v_lesson_id IS NULL THEN
            INSERT INTO public.lessons (
                chapter_id, title_fr, title_ar, lesson_type, content,
                learning_objectives, duration_minutes, order_index, media_resources
            ) VALUES (
                v_chapter_id, spec->>'fr', spec->>'ar', 'theory', '{}'::jsonb,
                spec->'objectives', 95, 1, media
            ) RETURNING id INTO v_lesson_id;
        END IF;

        UPDATE public.lessons
        SET title_fr = spec->>'fr',
            title_ar = spec->>'ar',
            lesson_type = 'theory',
            duration_minutes = 95,
            order_index = 1,
            learning_objectives = spec->'objectives',
            media_resources = media,
            content = jsonb_build_object(
                'course_design', 'prediction-manipulation-measure-model-bac',
                'guiding_question', spec->>'question',
                'key_formula', spec->>'formula',
                'learning_path', jsonb_build_array(
                    jsonb_build_object('step',1,'student_action','Observer le montage réel et identifier les grandeurs mesurées.','teacher_move','Faire décrire avant de donner le modèle.'),
                    jsonb_build_object('step',2,'student_action','Choisir une prédiction avant de lancer l''expérience.','teacher_move','Demander une justification courte fondée sur une grandeur.'),
                    jsonb_build_object('step',3,'student_action','Modifier une seule variable et enregistrer au moins deux essais.','teacher_move','Contrôler les autres paramètres et faire comparer les mesures.'),
                    jsonb_build_object('step',4,'student_action','Expliquer les résultats avec ' || (spec->>'formula') || '.','teacher_move','Relier la courbe, la mesure numérique et le modèle.'),
                    jsonb_build_object('step',5,'student_action','Résoudre une question type Bac en citant mesure, loi et conclusion.','teacher_move','Méthode : ' || (spec->>'bac'))
                ),
                'micro_enseignements', jsonb_build_array(
                    jsonb_build_object('id','chem_ch' || (spec->>'n') || '_observe','title','1. J''observe le dispositif','type','observation'),
                    jsonb_build_object('id','chem_ch' || (spec->>'n') || '_predict','title','2. Je prédis','type','hypothesis'),
                    jsonb_build_object('id','chem_ch' || (spec->>'n') || '_measure','title','3. Je manipule et mesure','type','simulation','missions',spec->'missions'),
                    jsonb_build_object('id','chem_ch' || (spec->>'n') || '_model','title','4. Je modélise','type','reasoning'),
                    jsonb_build_object('id','chem_ch' || (spec->>'n') || '_bac','title','5. J''applique au Bac','type','application')
                ),
                'phases', jsonb_build_object(
                    'activation',jsonb_build_object('duration_minutes',8,'focus','observer et prédire'),
                    'exploration',jsonb_build_object('duration_minutes',30,'focus','manipuler un paramètre à la fois'),
                    'explanation',jsonb_build_object('duration_minutes',22,'focus','relier mesures et modèle'),
                    'application',jsonb_build_object('duration_minutes',25,'focus','raisonnement type Bac'),
                    'consolidation',jsonb_build_object('duration_minutes',10,'focus','expliquer sans la simulation')
                ),
                'interactive_exercises', jsonb_build_array(jsonb_build_object(
                    'id','chem_ch' || (spec->>'n') || '_virtual_lab',
                    'type','advanced_virtual_lab',
                    'missions',spec->'missions',
                    'instruction','Prédire, effectuer deux essais contrôlés, comparer les mesures et conclure.',
                    'llm_reads',jsonb_build_array('variables','measurements','student_prediction','trial_history','scientific_observation')
                )),
                'misconceptions', jsonb_build_array(jsonb_build_object(
                    'error',spec->>'error',
                    'remediation','Créer deux essais qui isolent la variable en cause puis confronter la prédiction aux mesures.'
                )),
                'differentiation', jsonb_build_object(
                    'support','Utiliser les valeurs initiales et verbaliser le sens de variation.',
                    'standard','Comparer deux essais en contrôlant les autres variables.',
                    'challenge','Justifier quantitativement avec la formule et discuter les limites du modèle.'
                ),
                'bac_method', spec->>'bac',
                'exit_ticket', jsonb_build_array(
                    'Explique le rôle de ' || (spec->>'focus') || ' en une phrase.',
                    'Interprète la relation : ' || (spec->>'formula') || '.',
                    'Cite une mesure de la simulation qui soutient ta conclusion.'
                )
            )
        WHERE id = v_lesson_id;

        FOR item IN SELECT value FROM jsonb_array_elements(media)
        LOOP
            resource_path := item->>'url';
            simulation_id := CASE
                WHEN resource_path LIKE '%/cinetique/%' THEN 'chimie-cinetique-2bac'
                WHEN resource_path LIKE '%/nucleaire/%' THEN 'chimie-nucleaire-2bac'
                WHEN resource_path LIKE '%/equilibres/%' THEN 'chimie-equilibres-2bac'
                WHEN resource_path LIKE '%/electrochimie/%' THEN 'chimie-electrochimie-2bac'
                WHEN resource_path LIKE '%/synthese-organique/%' THEN 'chimie-synthese-organique-2bac'
                ELSE NULL
            END;

            IF EXISTS (
                SELECT 1 FROM public.lesson_resources
                WHERE lesson_id = v_lesson_id AND file_path = resource_path
            ) THEN
                UPDATE public.lesson_resources
                SET section_title = left(spec->>'fr', 200),
                    resource_type = item->>'type',
                    title = left(item->>'caption', 200),
                    description = item->>'caption',
                    trigger_text = left(item->>'trigger', 200),
                    phase = CASE WHEN item->>'type' = 'simulation' THEN 'exploration' ELSE 'activation' END,
                    difficulty_tier = (CASE WHEN item->>'type' = 'simulation' THEN 'advanced' ELSE 'intermediate' END)::difficulty_level,
                    concepts = jsonb_build_array('chimie 2e BAC', spec->>'focus'),
                    metadata = CASE WHEN item->>'type' = 'simulation' THEN jsonb_build_object(
                        'visual',true,'source_type','interactive_scientific_lab','subject','Chimie 2e BAC',
                        'chapter_number',(spec->>'n')::integer,'simulation_id',simulation_id,'simulation_version','2.0',
                        'mission_id',split_part(resource_path,'?mission=',2),'llm_readable_state',true,'llm_controllable',true,
                        'state_contract',jsonb_build_array('variables','measurements','student_prediction','mission_coverage','trial_history','scientific_observation','model_limits'),
                        'commands',jsonb_build_array('start','reset','set_variant','set_parameters','run_trial','highlight','get_state','set_prediction'),
                        'viewport','responsive'
                    ) ELSE jsonb_build_object(
                        'visual',true,'source_type','ai_generated_lab_scene','subject','Chimie 2e BAC','chapter_number',(spec->>'n')::integer
                    ) END
                WHERE lesson_id = v_lesson_id AND file_path = resource_path;
            ELSE
                INSERT INTO public.lesson_resources (
                    lesson_id, section_title, resource_type, title, description, file_path,
                    trigger_text, phase, difficulty_tier, concepts, metadata, order_index
                ) VALUES (
                    v_lesson_id, left(spec->>'fr',200), item->>'type', left(item->>'caption',200),
                    item->>'caption', resource_path, left(item->>'trigger',200),
                    CASE WHEN item->>'type'='simulation' THEN 'exploration' ELSE 'activation' END,
                    (CASE WHEN item->>'type'='simulation' THEN 'advanced' ELSE 'intermediate' END)::difficulty_level,
                    jsonb_build_array('chimie 2e BAC',spec->>'focus'),
                    CASE WHEN item->>'type'='simulation' THEN jsonb_build_object(
                        'visual',true,'source_type','interactive_scientific_lab','subject','Chimie 2e BAC',
                        'chapter_number',(spec->>'n')::integer,'simulation_id',simulation_id,'simulation_version','2.0',
                        'mission_id',split_part(resource_path,'?mission=',2),'llm_readable_state',true,'llm_controllable',true,
                        'state_contract',jsonb_build_array('variables','measurements','student_prediction','mission_coverage','trial_history','scientific_observation','model_limits'),
                        'commands',jsonb_build_array('start','reset','set_variant','set_parameters','run_trial','highlight','get_state','set_prediction'),
                        'viewport','responsive'
                    ) ELSE jsonb_build_object(
                        'visual',true,'source_type','ai_generated_lab_scene','subject','Chimie 2e BAC','chapter_number',(spec->>'n')::integer
                    ) END,
                    CASE WHEN item->>'type'='image' THEN 1 ELSE 2 END
                );
            END IF;
        END LOOP;
    END LOOP;
END
$migration$;

-- Contrôle : 14 chapitres doivent avoir au moins une leçon et deux ressources visuelles.
SELECT c.chapter_number, c.title_fr, count(DISTINCT l.id) AS lessons, count(lr.id) AS resources
FROM public.chapters c
JOIN public.subjects s ON s.id = c.subject_id
LEFT JOIN public.lessons l ON l.chapter_id = c.id
LEFT JOIN public.lesson_resources lr ON lr.lesson_id = l.id
WHERE lower(s.name_fr) LIKE '%chimi%'
GROUP BY c.chapter_number, c.title_fr
ORDER BY c.chapter_number;
