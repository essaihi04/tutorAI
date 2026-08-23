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
