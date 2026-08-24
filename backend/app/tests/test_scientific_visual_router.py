"""Le routeur doit toujours savoir quoi faire d'une demande de schéma BAC."""

from app.services.scientific_visual_router import (
    build_visual_route_prompt,
    recommend_generated_engine,
    route_scientific_visual,
    visual_blueprints,
)


def test_un_schema_svg_valide_reste_prioritaire():
    route = route_scientific_visual("montre-moi le schéma du sarcomère avec actine et myosine")

    assert route["source"] == "schema"
    assert route["schema_id"] == "svt_muscle_sarcomere"


def test_une_notion_manquante_recoit_un_blueprint_disciplinaire():
    route = route_scientific_visual("dessine la réplication semi-conservative de l'ADN")

    assert route["source"] == "blueprint"
    assert route["engine"] == "roughsvg"
    assert "deux brins parentaux" in route["must_show"]
    assert route["avoid"]
    assert route["explicit"] is True


def test_une_demande_inconnue_reste_generable_sans_inventer_un_moteur():
    route = route_scientific_visual("fais un schéma de la structure spatiale d'un appareil scientifique inédit")

    assert route["source"] == "generated"
    assert route["engine"] == "roughsvg"
    assert route["explicit"] is True


def test_le_routeur_heuristique_choisit_les_moteurs_specialises():
    assert recommend_generated_engine("courbe d'une fonction avec asymptote") == "jsxgraph"
    assert recommend_generated_engine("chaîne causale en plusieurs étapes") == "cytoscape"
    assert recommend_generated_engine("simulation de collision mécanique") == "matter"
    assert recommend_generated_engine("coupe et structure d'une cellule") == "roughsvg"
    assert recommend_generated_engine("mitochondrie 3D à tourner et zoomer") == "three"


def test_la_mitochondrie_a_tourner_ne_retombe_pas_sur_une_image_fixe():
    demande = "Je veux la mitochondrie en 3D pour la faire tourner et zoomer"
    route = route_scientific_visual("structure de la mitochondrie", demande)

    assert route["source"] == "mouvement"
    assert route["engine"] == "three"
    prompt = build_visual_route_prompt("structure de la mitochondrie", demande)
    assert "`three`" in prompt
    assert "`mitochondrion`" in prompt


def test_chaque_blueprint_bac_est_exploitable_et_testable():
    allowed = {"jsxgraph", "cytoscape", "matter", "roughsvg"}
    blueprints = visual_blueprints()

    assert len(blueprints) >= 30
    assert len({item["id"] for item in blueprints}) == len(blueprints)
    for blueprint in blueprints:
        assert blueprint["engine"] in allowed, blueprint["id"]
        assert len(blueprint.get("keywords", [])) >= 3, blueprint["id"]
        assert len(blueprint.get("must_show", [])) >= 4, blueprint["id"]
        assert blueprint.get("avoid"), blueprint["id"]

        route = route_scientific_visual(f"schéma {blueprint['keywords'][0]}")
        assert route["source"] in {"schema", "blueprint"}, blueprint["id"]


def test_le_prompt_de_generation_impose_qualite_et_securite():
    prompt = build_visual_route_prompt("dessine la méiose et le crossing-over")

    assert "Moteur imposé" in prompt
    assert "Éléments scientifiques obligatoires" in prompt
    assert "Erreurs scientifiques interdites" in prompt
    assert "aucun texte superposé" in prompt
    assert "JavaScript" in prompt


def test_un_pluriel_ne_change_pas_de_moteur():
    """« bilan des FORCES » partait vers un moteur de réseaux.

    Le mot-clé `force` était au singulier et n'attrapait pas « forces » ;
    `bilan`, lui, appartenait au motif Cytoscape. Trois vecteurs dans un
    repère se retrouvaient donc dessinés en nœuds et flèches — un bilan des
    forces qui ne montre plus aucune force.
    """
    assert recommend_generated_engine("dessine un bilan des forces sur un plan incliné") == "jsxgraph"
    assert recommend_generated_engine("bilan énergétique de la respiration") == "cytoscape"
    assert recommend_generated_engine("les étapes de la glycolyse") == "cytoscape"


def test_l_optique_va_dans_un_repere_et_non_en_dessin_libre():
    """Une lentille se construit avec des rayons, des foyers et une échelle."""
    for demande in (
        "montre la lentille convergente et la construction de l'image",
        "schéma d'un miroir et du rayon réfléchi",
        "la réfraction et l'angle d'incidence",
    ):
        assert recommend_generated_engine(demande) == "jsxgraph", demande


def test_un_arbre_genealogique_n_est_pas_un_reseau():
    """Carrés et ronds rangés par génération : un dessin, pas un graphe.

    Les arbres qui SONT des graphes gardent leur moteur.
    """
    assert recommend_generated_engine("l'arbre généalogique de cette famille") == "roughsvg"
    assert recommend_generated_engine("un arbre phylogénétique des primates") == "cytoscape"


def test_un_echiquier_est_un_tableau_pas_un_dessin():
    """Certaines demandes disent « dessine » sans appeler un dessin.

    Un échiquier dessiné perd l'alignement des gamètes, qui est tout ce qu'un
    échiquier sert à montrer.
    """
    assert recommend_generated_engine("dessine l'échiquier de croisement") == "table"
    assert recommend_generated_engine("le tableau de variations de f") == "table"
    assert recommend_generated_engine("dresse le tableau d'avancement") == "table"

    prompt = build_visual_route_prompt("dessine l'échiquier de croisement du test cross")
    assert "table" in prompt
    assert "scientific" not in prompt or "RÉSERVE" in prompt


def test_la_fiche_de_genetique_ne_contredit_plus_le_protocole():
    """Deux ordres contraires arrivaient au tuteur dans le même prompt.

    La fiche imposait un moteur graphique et listait « échiquier » parmi les
    éléments obligatoires ; le PROTOCOLE GÉNÉTIQUE exige `type=table` pour ce
    même échiquier.
    """
    prompt = build_visual_route_prompt("croisement monohybride chez la drosophile")

    assert "RÉSERVE" in prompt
    assert "`table`" in prompt
    assert "PROTOCOLE GÉNÉTIQUE" in prompt


def test_un_tableau_demande_ne_devient_pas_le_schema_du_chapitre():
    """La route `table` ne servait à rien dès qu'un schéma répondait.

    « Dessine le tableau d'avancement de la réaction » contient « réaction »,
    mot-clé du schéma de cinétique : l'élève recevait la figure du CHAPITRE
    cinétique au lieu du tableau d'avancement de SA réaction. Même piège pour
    « tableau de variations », que « variation » envoyait vers le schéma de
    dérivation.
    """
    for demande in (
        "dessine le tableau d'avancement de la réaction",
        "donne-moi le tableau de variations de la fonction f",
        "fais le tableau de signes de f'(x)",
    ):
        route = route_scientific_visual(demande)
        assert route["engine"] == "table", demande
        assert "TABLEAU" in build_visual_route_prompt(demande), demande


def test_une_fiche_forte_garde_la_main_sur_la_route_tableau():
    """L'échiquier reste un tableau, mais pas au prix du reste de la figure.

    La fiche du monohybridisme demande AUSSI les chromosomes et les gamètes,
    et elle porte déjà la réserve qui laisse l'échiquier lui-même en
    `type=table`. La court-circuiter perdrait tout ce qui l'entoure.
    """
    route = route_scientific_visual("l'échiquier de croisement du monohybridisme chez le pois")

    assert route["source"] == "blueprint"
    assert route["blueprint_id"] == "svt_monohybridisme"
    assert "RÉSERVE" in build_visual_route_prompt(
        "l'échiquier de croisement du monohybridisme chez le pois"
    )


def test_un_choc_se_simule_meme_conjugue():
    """Les verbes du mouvement se conjuguent, les mots-clés non.

    « La bille rebondit » n'était pas attrapé par `\brebond\b`, et « choc »
    n'existait dans aucune des deux listes : deux billes qui se percutent
    partaient en dessin figé. Un choc dessiné ne montre aucun choc.
    """
    for demande in (
        "choc élastique entre deux billes",
        "une bille rebondit sur le sol",
        "simule un chariot qui glisse et percute un mur",
    ):
        assert recommend_generated_engine(demande) == "matter", demande

    # Le second verrou tient toujours : sans mécanique, pas de simulation.
    assert recommend_generated_engine("anime les étapes de la photosynthèse") != "matter"


def test_une_regulation_se_lit_comme_une_boucle():
    """Capteur → centre → effecteur, et la flèche de retour qui referme.

    C'est un graphe orienté ; une coupe anatomique ne montre pas le retour.
    """
    assert recommend_generated_engine("la régulation de la glycémie") == "cytoscape"
    assert recommend_generated_engine("le rétrocontrôle négatif de la testostérone") == "cytoscape"


def test_un_diagramme_de_predominance_est_un_axe_gradue():
    """Sa frontière est le pKa : dessinée à main levée, elle ne veut rien dire."""
    assert recommend_generated_engine("diagramme de prédominance du couple acide-base") == "jsxgraph"
    assert recommend_generated_engine("diagramme de distribution des espèces") == "jsxgraph"


def test_l_objectif_d_une_lecon_ne_transforme_pas_tout_en_tableau():
    """La route `table` lit la DEMANDE, pas la séance entière.

    Le contexte de rapprochement mélange titre, chapitre, objectif et six
    messages. Un objectif de physique-chimie dit « dresser le tableau
    d'avancement de la réaction » : sans distinction, la phrase resterait dans
    le contexte toute la séance et chaque figure demandée ensuite — une
    courbe, un montage — partirait en tableau.
    """
    seance = (
        "suivi temporel d'une transformation chimique cinetique "
        "objectif : dresser le tableau d'avancement de la reaction"
    )

    # L'élève demande une courbe : la séance parle de tableau, pas lui.
    route = route_scientific_visual(seance, "trace-moi la courbe de la concentration au cours du temps")
    assert route.get("engine") != "table"

    # L'élève demande le tableau : là, il l'obtient.
    route = route_scientific_visual(seance, "dresse le tableau d'avancement")
    assert route["engine"] == "table"


def test_sans_demande_le_routeur_lit_le_contexte_comme_avant():
    """Les appels d'origine ne changent pas de comportement."""
    assert route_scientific_visual("dessine le tableau de variations de f")["engine"] == "table"


def test_seule_une_fiche_qui_reclame_le_tableau_garde_la_main():
    """La réserve vise les fiches qui SAVENT placer un tableau, pas les voisines.

    Celle du monohybridisme liste « échiquier » parmi ses obligations et sait
    l'entourer de chromosomes et de gamètes. Celle du suivi temporel n'en dit
    rien : se trouver là ne lui donne pas voix au chapitre.
    """
    from app.services.scientific_visual_router import _fiche_reclame_un_tableau, visual_blueprints

    fiches = {item["id"]: item for item in visual_blueprints()}
    assert _fiche_reclame_un_tableau(fiches["svt_monohybridisme"]) is True
    assert _fiche_reclame_un_tableau(fiches["chem_suivi_temporel"]) is False


def test_un_mot_de_chapitre_seul_n_impose_pas_le_schema_d_un_autre_chapitre():
    """« variation » est un mot-clé de la dérivation, et un mot français partout.

    « Trace la courbe de la variation de la pression artérielle » — une courbe
    de SVT — se voyait proposer le schéma de DÉRIVATION, sur ce seul mot. Une
    vraie leçon de dérivation dit « dérivée » ou « dérivation », et garde donc
    son schéma.
    """
    route = route_scientific_visual("trace la courbe de la variation de la pression artérielle")
    assert route["source"] == "generated"
    assert route["engine"] == "jsxgraph"

    route = route_scientific_visual("la dérivée et la tangente à la courbe")
    assert route["source"] == "schema"
    assert route["schema_id"] == "math_derivation"


def test_une_image_fixe_ne_repond_pas_a_fais_la_bouger():
    """La boucle de la séance du 23 août 2026, en une ligne.

    « dir lya chi simulation de contraction » contient « contraction »,
    mot-clé de `svt_muscle_sarcomere`. Le tuteur recevait « affiche ce schéma,
    NE LE REDESSINE PAS » et renvoyait une photo de sarcomère. L'élève
    redemandait, le tuteur repromettait une simulation qu'il n'avait pas le
    droit de produire : quatre fois le même paragraphe.
    """
    contexte = "sarcomère muscle contraction actine myosine"

    route = route_scientific_visual(contexte, "dir lya chi simulation de contraction")
    assert route["source"] == "mouvement"
    # Le schéma validé ne disparaît pas : il accompagne, il ne répond pas.
    assert route["schema_id"] == "svt_muscle_sarcomere"

    prompt = build_visual_route_prompt(contexte, "dir lya chi simulation de contraction")
    assert "BOUGER" in prompt
    assert "OUVRIR_SIMULATION" in prompt
    assert "`preset`" in prompt
    assert "matter" in prompt
    assert "INTERDIT ABSOLU" in prompt          # promettre sans envoyer
    assert "Ne le redessine pas" not in prompt  # l'ancien ordre a disparu


def test_une_demande_ordinaire_garde_le_schema_valide():
    """Rien ne change pour qui demande simplement le schéma."""
    prompt = build_visual_route_prompt("sarcomère muscle contraction", "rassam lya sarcomere")

    assert "SCHÉMA VALIDÉ DISPONIBLE" in prompt
    assert "svt_muscle_sarcomere" in prompt


def test_le_nom_d_une_notion_n_est_pas_une_demande_d_animation():
    """« mouvement circulaire uniforme » se DESSINE : rayon et vecteurs.

    Sans cette réserve, tout le chapitre de mécanique passait pour une
    demande de simulation.
    """
    for demande in (
        "schéma du mouvement circulaire uniforme",
        "la quantité de mouvement du système",
        "étude dynamique du pendule",
    ):
        assert route_scientific_visual(demande, demande)["source"] != "mouvement", demande
