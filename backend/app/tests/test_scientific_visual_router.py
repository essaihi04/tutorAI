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
