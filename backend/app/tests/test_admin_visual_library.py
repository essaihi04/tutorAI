"""Safety and catalogue contract for the unified admin visual library."""

import pytest

from app.admin_auth import verify_admin_token
from app.api import resources
from app.services.admin_visual_library_service import (
    VisualLibraryError,
    admin_visual_library_service,
    extract_llm_json,
    normalize_generated_result,
)
from app.services.admin_course_service import admin_course_service
from app.services.schema_catalog import SCHEMA_CATALOG
from app.services.scientific_presets import SCIENTIFIC_PRESETS
from app.services.scientific_visual_skill import normalize_scientific_visual


def test_catalogue_exposes_every_code_owned_visual_as_protected():
    schemas = admin_visual_library_service._schema_items()
    presets = admin_visual_library_service._preset_items()

    assert len(schemas) == len(SCHEMA_CATALOG)
    assert len(presets) == len(SCIENTIFIC_PRESETS)
    assert all(item["source"] == "core" for item in schemas + presets)
    assert all(item["editable"] is False for item in schemas + presets)
    assert all(item["deletable"] is False for item in schemas + presets)


def test_every_preset_preview_resolves_through_the_shared_validator():
    for item in admin_visual_library_service._preset_items():
        assert normalize_scientific_visual(item["preview"]["scientific"]) is not None


def test_legacy_mitochondrion_png_is_exposed_as_the_interactive_3d_model():
    item = admin_visual_library_service._resource_item({
        "id": "mito-legacy",
        "lesson_id": "lesson-svt",
        "resource_type": "image",
        "title": "Mitochondrie 3D à observer",
        "file_path": "/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_3d_sans_legendes.png",
        "metadata": {},
    }, {"subject_name": "SVT"})

    assert item["kind"] == "scientific"
    assert item["preview"]["scientific"]["engine"] == "three"
    assert item["preview"]["scientific"]["model"] == "mitochondrion"


def test_gene_expression_image_keeps_its_poster_but_opens_the_animated_simulation():
    poster = "/media/images/svt/ch2_information_genetique/lesson_2_expression/adn_arnm_proteine.png"
    item = admin_visual_library_service._resource_item({
        "id": "gene-expression-legacy",
        "lesson_id": "lesson-svt",
        "resource_type": "image",
        "title": "ADN → ARNm → protéine",
        "file_path": poster,
        "metadata": {},
    }, {"subject_name": "SVT"})

    assert item["kind"] == "simulation"
    assert item["preview"]["kind"] == "simulation"
    assert item["preview"]["poster_url"] == poster
    assert item["preview"]["url"].endswith("/expression/index.html")


def test_llm_json_extraction_accepts_fence_but_ignores_prose_after_object():
    result = extract_llm_json('```json\n{"title":"Chute","scientific":{"engine":"matter"}}\n```\nExplication')
    assert result["title"] == "Chute"


def test_generated_visual_is_normalized_and_drops_free_event_handlers():
    result = normalize_generated_result({
        "title": "Deux cellules",
        "scientific": {
            "engine": "roughsvg",
            "title": "Deux cellules",
            "description": "Comparaison de deux cellules du cours.",
            "width": 500,
            "height": 300,
            "elements": [
                {"type": "circle", "x": 140, "y": 150, "radius": 70, "color": "cyan", "onClick": "evil()"},
                {"type": "circle", "x": 350, "y": 150, "radius": 70, "color": "green"},
                {"type": "text", "x": 140, "y": 250, "text": "Cellule A"},
                {"type": "text", "x": 350, "y": 250, "text": "Cellule B"},
            ],
        },
    })

    assert result["scientific"]["engine"] == "roughsvg"
    assert all("onClick" not in element for element in result["scientific"]["elements"])
    assert result["quality"]["acceptable"] is True


def test_generated_visual_rejects_unknown_engine_and_code_payloads():
    with pytest.raises(VisualLibraryError):
        normalize_generated_result({
            "scientific": {"engine": "threejs", "javascript": "alert(1)"},
        })


def test_legacy_resource_crud_routes_now_require_the_admin_dependency():
    protected = [route for route in resources.router.routes if route.path.startswith("/resources") or route.path in {"/upload", "/lessons"}]
    assert protected
    for route in protected:
        dependency_calls = {dependency.call for dependency in route.dependant.dependencies}
        assert verify_admin_token in dependency_calls


def test_existing_schema_is_suggested_before_reinventing_it():
    match = admin_visual_library_service.existing_match("Montrer la structure du sarcomère et le glissement actine myosine")
    assert match is not None
    assert match["id"] == "svt_muscle_sarcomere"


def test_code_catalogue_remains_available_when_database_is_down(monkeypatch):
    def unavailable(_admin):
        raise RuntimeError("database offline")

    monkeypatch.setattr(admin_visual_library_service, "_admin", lambda: object())
    monkeypatch.setattr(admin_course_service, "list_lessons", unavailable)

    result = admin_visual_library_service.list_library()

    assert result["database_available"] is False
    assert len([item for item in result["items"] if item["kind"] == "schema"]) == len(SCHEMA_CATALOG)
    assert len([item for item in result["items"] if item["kind"] == "preset"]) == len(SCIENTIFIC_PRESETS)


def test_metadata_backed_simulation_is_marked_for_lazy_inline_preview():
    item = admin_visual_library_service._resource_item({
        "id": "simulation-1",
        "lesson_id": "lesson-1",
        "resource_type": "simulation",
        "title": "Fermentation",
        "file_path": "local:metadata",
        "metadata": {"mime_type": "text/html", "content": "<!doctype html><html></html>"},
    }, {})

    assert item["preview"]["inline_html"] is True
    assert "url" not in item["preview"]


def test_broken_metadata_marker_is_never_exposed_as_an_iframe_url():
    item = admin_visual_library_service._resource_item({
        "id": "simulation-2",
        "lesson_id": "lesson-1",
        "resource_type": "simulation",
        "title": "Simulation incomplète",
        "file_path": "local:metadata",
        "metadata": {},
    }, {})

    assert item["preview"]["available"] is False
    assert "url" not in item["preview"]


def test_inline_preview_content_is_loaded_only_on_demand(monkeypatch):
    class Result:
        data = [{
            "id": "simulation-1",
            "title": "Fermentation",
            "resource_type": "simulation",
            "file_path": "local:metadata",
            "metadata": {"mime_type": "text/html", "content": "<!doctype html><html>OK</html>"},
        }]

    class Query:
        def select(self, *_args): return self
        def eq(self, *_args): return self
        def limit(self, *_args): return self
        def execute(self): return Result()

    class Admin:
        def table(self, name):
            assert name == "lesson_resources"
            return Query()

    monkeypatch.setattr(admin_visual_library_service, "_admin", lambda: Admin())

    result = admin_visual_library_service.get_preview_content("simulation-1")

    assert result["html"] == "<!doctype html><html>OK</html>"
    assert result["mime_type"] == "text/html"
