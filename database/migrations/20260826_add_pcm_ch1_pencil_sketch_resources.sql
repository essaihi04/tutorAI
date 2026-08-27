-- 27 croquis progressifs des premiers cours de physique, chimie et maths.
-- Les vidéos servent de référence de geste pour 14 dessins ; le contenu des
-- cours locaux reste la source pédagogique de vérité pour l'ensemble.
BEGIN;

DO $$
DECLARE
    v_course RECORD;
    v_lesson_id UUID;
BEGIN
    FOR v_course IN
        SELECT *
        FROM jsonb_to_recordset($courses$
        [
          {
            "course_id": "phys_ch1_waves",
            "chapter_pattern": "Ondes mécaniques progressives%",
            "resources": [
              {"schema_id":"phys_croquis_propagation_locale","section":"Propagation","title":"Croquis : propagation et mouvement local","description":"Sépare le déplacement de la perturbation de l'oscillation locale d'un point du milieu.","trigger":"dessine propagation onde sans transport matière","phase":"explanation","difficulty":"beginner","order":201,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=E79tE5gmdrk","concepts":["onde mécanique","propagation","mouvement local","énergie"]},
              {"schema_id":"phys_croquis_transversale_longitudinale","section":"Types d'onde","title":"Croquis : transversale ou longitudinale","description":"Compare les directions de propagation et de déplacement sur une corde et un ressort.","trigger":"dessine onde transversale longitudinale corde ressort","phase":"explanation","difficulty":"beginner","order":202,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=E79tE5gmdrk","concepts":["transversale","longitudinale","corde","ressort"]},
              {"schema_id":"phys_croquis_son_milieu","section":"Milieu matériel","title":"Croquis : le son a besoin d'un milieu","description":"Relie sonnette sous cloche, diapason et nécessité d'un milieu matériel.","trigger":"dessine cloche à vide diapason onde sonore","phase":"exploration","difficulty":"intermediate","order":203,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=E79tE5gmdrk","concepts":["son","cloche à vide","diapason","milieu matériel"]},
              {"schema_id":"phys_croquis_superposition","section":"Superposition","title":"Croquis : croisement de deux perturbations","description":"Montre avant, pendant et après le croisement, avec somme algébrique temporaire.","trigger":"dessine superposition deux perturbations avant pendant après","phase":"explanation","difficulty":"advanced","order":204,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=E79tE5gmdrk","concepts":["superposition","perturbations","somme algébrique"]},
              {"schema_id":"phys_croquis_ressort_celerite","section":"Mesure","title":"Croquis : mesurer la célérité sur un ressort","description":"Place deux capteurs, la distance d, les dates et le calcul v=d/τ.","trigger":"dessine ressort capteurs retard célérité","phase":"guided_practice","difficulty":"intermediate","order":205,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=E79tE5gmdrk","concepts":["ressort","capteurs","retard","célérité"]},
              {"schema_id":"phys_croquis_corde_poulie","section":"Facteurs de célérité","title":"Croquis : corde tendue par une masse","description":"Relie tension, poids, masse linéique et célérité sur une corde.","trigger":"dessine corde poulie masse tension célérité","phase":"explanation","difficulty":"advanced","order":206,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=E79tE5gmdrk","concepts":["tension","masse linéique","poulie","célérité"]},
              {"schema_id":"phys_croquis_retard","section":"Retard","title":"Croquis : retard entre S et M","description":"Explique la translation temporelle yM(t)=yS(t−τ) et τ=SM/v.","trigger":"dessine retard source S point M relation temporelle","phase":"explanation","difficulty":"advanced","order":207,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=E79tE5gmdrk","concepts":["retard","source","élongation","translation temporelle"]},
              {"schema_id":"phys_croquis_deux_capteurs","section":"Calcul guidé","title":"Croquis : deux capteurs sur une corde","description":"Décompose distance, dates, conversions, retard et célérité numérique.","trigger":"dessine deux capteurs A B avec distance et dates","phase":"guided_practice","difficulty":"intermediate","order":208,"audit":"curriculum_reviewed","concepts":["capteurs A B","unités","retard","célérité"]},
              {"schema_id":"phys_croquis_signaux_retard","section":"Méthode BAC","title":"Croquis : décalage de deux signaux","description":"Repère deux pics homologues et mesure leur décalage horizontal.","trigger":"dessine deux signaux homologues et leur retard","phase":"consolidation","difficulty":"advanced","order":209,"audit":"curriculum_reviewed","concepts":["signaux","pics homologues","lecture graphique","retard"]},
              {"schema_id":"phys_croquis_bilan_ondes","section":"Synthèse","title":"Croquis : bilan des ondes mécaniques","description":"Carte reliant définition, types d'onde, retard et célérité.","trigger":"dessine bilan complet premier cours ondes","phase":"consolidation","difficulty":"intermediate","order":210,"audit":"curriculum_reviewed","concepts":["bilan","onde mécanique","types","retard","célérité"]}
            ]
          },
          {
            "course_id": "chem_ch1_kinetics",
            "chapter_pattern": "Transformations lentes et transformations rapides%",
            "resources": [
              {"schema_id":"chem_croquis_carte_cinetique","section":"Introduction","title":"Croquis : carte rapide, lente et facteurs","description":"Organise le classement temporel et les premiers facteurs cinétiques.","trigger":"dessine carte transformations rapides lentes","phase":"activation","difficulty":"beginner","order":301,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=WAHItI0S14A","concepts":["rapide","lente","durée","facteurs cinétiques"]},
              {"schema_id":"chem_croquis_transfert_electrons","section":"Rappel oxydoréduction","title":"Croquis : transfert d'électrons","description":"Sépare donneur, accepteur et simplification des électrons dans le bilan.","trigger":"dessine oxydant réducteur transfert électrons","phase":"activation","difficulty":"intermediate","order":302,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=WAHItI0S14A","concepts":["oxydant","réducteur","électrons","demi-équations"]},
              {"schema_id":"chem_croquis_duree_transformation","section":"Classement","title":"Croquis : durée d'une transformation","description":"Lit Δt sur une évolution vers un plateau et distingue rapide de lente.","trigger":"dessine courbe durée transformation rapide lente","phase":"explanation","difficulty":"intermediate","order":303,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=WAHItI0S14A","concepts":["durée","avancement","plateau","rapide","lente"]},
              {"schema_id":"chem_croquis_facteurs_controles","section":"Protocole","title":"Croquis : comparaison concentration-température","description":"Montre pourquoi une comparaison ne change qu'une variable à la fois.","trigger":"dessine deux béchers comparaison contrôlée","phase":"guided_practice","difficulty":"intermediate","order":304,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=WAHItI0S14A","concepts":["concentration","température","témoin","variables contrôlées"]},
              {"schema_id":"chem_croquis_trois_bechers","section":"Diagnostic","title":"Croquis : trois béchers à températures différentes","description":"Fait relier température et intensité du dégagement gazeux à conditions identiques.","trigger":"dessine trois béchers froid tempéré chaud","phase":"activation","difficulty":"beginner","order":305,"audit":"curriculum_reviewed","concepts":["température","bulles","comparaison","hypothèse"]},
              {"schema_id":"chem_croquis_indices_macroscopiques","section":"Suivi","title":"Croquis : indices macroscopiques","description":"Compare couleur, gaz, pH, conductivité et concentration comme grandeurs de suivi.","trigger":"dessine indices macroscopiques suivi cinétique","phase":"explanation","difficulty":"advanced","order":306,"audit":"curriculum_reviewed","concepts":["absorbance","gaz","pH","conductivité","concentration"]},
              {"schema_id":"chem_croquis_quatre_facteurs","section":"Facteurs cinétiques","title":"Croquis : quatre facteurs et mécanismes","description":"Relie température, concentration, surface et catalyse aux chocs ou à la voie réactionnelle.","trigger":"dessine les quatre facteurs cinétiques avec explication","phase":"explanation","difficulty":"advanced","order":307,"audit":"curriculum_reviewed","concepts":["température","concentration","surface","catalyseur","chocs efficaces"]},
              {"schema_id":"chem_croquis_catalyseur","section":"Catalyse","title":"Croquis : ce que change un catalyseur","description":"Compare deux profils énergétiques et distingue accélération, régénération et état final.","trigger":"dessine profil énergie activation catalyseur régénéré","phase":"explanation","difficulty":"advanced","order":308,"audit":"curriculum_reviewed","concepts":["catalyseur","énergie d'activation","voie réactionnelle","état final"]},
              {"schema_id":"chem_croquis_surface_contact","section":"Méthode BAC","title":"Croquis : comprimé entier ou poudre","description":"Construit un protocole contrôlé sur la surface de contact d'un solide.","trigger":"dessine comprimé entier contre poudre même masse","phase":"consolidation","difficulty":"intermediate","order":309,"audit":"curriculum_reviewed","concepts":["surface de contact","poudre","protocole","variables contrôlées"]},
              {"schema_id":"chem_croquis_courbes_facteur","section":"Exploitation","title":"Croquis : deux cinétiques, même état final","description":"Compare pente initiale, temps de demi-réaction et plateau commun.","trigger":"dessine deux courbes cinétiques même plateau","phase":"consolidation","difficulty":"advanced","order":310,"audit":"curriculum_reviewed","concepts":["courbes cinétiques","pente initiale","temps de demi-réaction","état final"]}
            ]
          },
          {
            "course_id": "math_ch1_limits",
            "chapter_pattern": "Limites et continuité%",
            "resources": [
              {"schema_id":"math_croquis_formes_indeterminees","section":"Diagnostic","title":"Croquis : quatre formes indéterminées","description":"Carte les quatre F.I. et rappelle qu'elles ne sont jamais une réponse finale.","trigger":"dessine les quatre formes indéterminées","phase":"activation","difficulty":"beginner","order":401,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=rhN5zNtTiuE","concepts":["formes indéterminées","0/0","infini/infini"]},
              {"schema_id":"math_croquis_boite_factorisation","section":"Outils","title":"Croquis : boîte à outils de factorisation","description":"Regroupe les identités et le facteur x−a utilisé lorsque P(a)=0.","trigger":"dessine boîte identités factorisation limites","phase":"explanation","difficulty":"intermediate","order":402,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=rhN5zNtTiuE","concepts":["factorisation","identités remarquables","racine","x−a"]},
              {"schema_id":"math_croquis_strategie_fi","section":"Méthode","title":"Croquis : stratégie pour lever 0/0","description":"Décompose substitution, diagnostic, factorisation, simplification et conclusion.","trigger":"dessine méthode complète pour lever zéro sur zéro","phase":"guided_practice","difficulty":"advanced","order":403,"audit":"video_reviewed","source":"https://www.youtube.com/watch?v=rhN5zNtTiuE","concepts":["0/0","substitution","factorisation","simplification"]},
              {"schema_id":"math_croquis_trou_limite","section":"Limite finie","title":"Croquis : un trou mais une limite","description":"Distingue valeur au point, valeurs voisines et limite bilatérale.","trigger":"dessine une courbe avec un trou et une limite finie","phase":"explanation","difficulty":"advanced","order":404,"audit":"curriculum_reviewed","concepts":["trou","limite bilatérale","prolongement par continuité"]},
              {"schema_id":"math_croquis_asymptotes","section":"Asymptotes","title":"Croquis : verticale ou horizontale","description":"Relie limite infinie en a à x=a et limite finie à l'infini à y=L.","trigger":"dessine asymptote verticale horizontale avec limites","phase":"application","difficulty":"advanced","order":405,"audit":"curriculum_reviewed","concepts":["asymptote verticale","asymptote horizontale","limite infinie"]},
              {"schema_id":"math_croquis_tvi","section":"Continuité","title":"Croquis : TVI, existence puis unicité","description":"Sépare les hypothèses du TVI de l'argument supplémentaire de monotonie.","trigger":"dessine TVI continuité signe existence unicité","phase":"consolidation","difficulty":"advanced","order":406,"audit":"curriculum_reviewed","concepts":["TVI","continuité","changement de signe","existence","unicité"]},
              {"schema_id":"math_croquis_carte_methodes","section":"Synthèse","title":"Croquis : carte des méthodes de limites","description":"Route calcul direct, F.I., asymptotes et preuve par continuité.","trigger":"dessine carte complète méthodes premier cours limites","phase":"consolidation","difficulty":"advanced","order":407,"audit":"curriculum_reviewed","concepts":["méthodes","limites","asymptotes","continuité","TVI"]}
            ]
          }
        ]
        $courses$::jsonb) AS course(course_id text, chapter_pattern text, resources jsonb)
    LOOP
        SELECT l.id INTO v_lesson_id
        FROM lessons l
        JOIN chapters c ON c.id = l.chapter_id
        WHERE c.title_fr ILIKE v_course.chapter_pattern
        ORDER BY c.order_index, l.order_index
        LIMIT 1;

        IF v_lesson_id IS NULL THEN
            RAISE EXCEPTION 'Cours introuvable pour % (%)', v_course.course_id, v_course.chapter_pattern;
        END IF;

        INSERT INTO lesson_resources
            (lesson_id, section_title, resource_type, title, description,
             trigger_text, phase, difficulty_tier, concepts, metadata, order_index)
        SELECT
            v_lesson_id,
            resource.section,
            'image',
            resource.title,
            resource.description,
            resource.trigger,
            resource.phase,
            resource.difficulty::difficulty_level,
            resource.concepts,
            jsonb_strip_nulls(jsonb_build_object(
                'schema_id', resource.schema_id,
                'render_target', 'live_board',
                'visual_style', 'pencil',
                'resource_role', 'teacher_sketch',
                'course_id', v_course.course_id,
                'palette_id', 'bac-pencil-v1',
                'audit_status', resource.audit,
                'inspiration_url', resource.source,
                'transparent_background', true,
                'library_status', 'validated',
                'library_source', 'core_schema',
                'library_version', 1
            )),
            resource.order_index
        FROM jsonb_to_recordset(v_course.resources) AS resource(
            schema_id text, section text, title text, description text,
            trigger text, phase text, difficulty text, order_index integer,
            audit text, source text, concepts jsonb
        )
        WHERE NOT EXISTS (
            SELECT 1
            FROM lesson_resources existing
            WHERE existing.lesson_id = v_lesson_id
              AND existing.metadata ->> 'schema_id' = resource.schema_id
        );
    END LOOP;
END $$;

COMMIT;
