"""Safety and catalogue contract for the unified admin visual library."""

from pathlib import Path
import re

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


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def test_catalogue_exposes_every_code_owned_visual_as_protected():
    schemas = admin_visual_library_service._schema_items()
    presets = admin_visual_library_service._preset_items()

    assert len(schemas) == len(SCHEMA_CATALOG)
    assert len(presets) == len(SCIENTIFIC_PRESETS)
    assert all(item["source"] == "core" for item in schemas + presets)
    assert all(item["editable"] is False for item in schemas + presets)
    assert all(item["deletable"] is False for item in schemas + presets)


@pytest.mark.parametrize("schema_id, subject_key, course_id", [
    ("svt_croquis_glycolyse", "svt", "svt_ch1_energy"),
    ("phys_croquis_signaux_retard", "physics", "phys_ch1_waves"),
    ("chem_croquis_catalyseur", "chemistry", "chem_ch1_kinetics"),
    ("math_croquis_tvi", "math", "math_ch1_limits"),
])
def test_pencil_schemas_are_exposed_with_course_metadata(schema_id, subject_key, course_id):
    item = next(
        item for item in admin_visual_library_service._schema_items()
        if item["catalog_id"] == schema_id
    )

    assert item["preview"] == {"kind": "schema", "schema_id": schema_id}
    assert item["subject_key"] == subject_key
    assert item["metadata"]["courseId"] == course_id
    assert item["metadata"]["resourceRole"] == "teacher_sketch"
    assert item["metadata"]["visualStyle"] == "pencil"
    assert item["chapter"]
    assert item["lesson"]


def test_database_schema_resource_previews_the_core_schema():
    item = admin_visual_library_service._resource_item({
        "id": "resource-glycolyse",
        "lesson_id": "lesson-svt",
        "resource_type": "image",
        "title": "Croquis : bilan de la glycolyse",
        "file_path": None,
        "metadata": {"schema_id": "svt_croquis_glycolyse"},
    }, {"subject_name": "SVT"})

    assert item["kind"] == "schema"
    assert item["preview"] == {"kind": "schema", "schema_id": "svt_croquis_glycolyse"}


def test_every_preset_preview_resolves_through_the_shared_validator():
    for item in admin_visual_library_service._preset_items():
        assert normalize_scientific_visual(item["preview"]["scientific"]) is not None


def test_les_scenes_du_muscle_sont_classees_dans_la_bonne_lecon():
    muscle_ids = {
        "svt_ch1_myogrammes",
        "svt_ch1_chaleurs_muscle",
        "svt_ch1_glissement_sarcomere",
        "svt_ch1_couplage_excitation_contraction",
        "svt_ch1_cycle_actomyosine",
        "svt_ch1_filieres_effort",
    }
    items = {
        item["catalog_id"]: item
        for item in admin_visual_library_service._preset_items()
        if item["catalog_id"] in muscle_ids
    }

    assert set(items) == muscle_ids
    assert all("muscle strié" in item["lesson"] for item in items.values())


def test_le_modele_3d_du_couplage_musculaire_est_dans_la_bibliotheque():
    items = admin_visual_library_service._three_model_items()

    assert len(items) == 1
    item = items[0]
    assert item["catalog_id"] == "muscle_excitation_contraction"
    assert item["kind"] == "scientific"
    assert "muscle strié" in item["lesson"]
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


def test_local_simulation_preview_keeps_module_origin_without_weakening_inline_html():
    source = (
        PROJECT_ROOT / "frontend/src/components/admin/AdminVisualLibrary.tsx"
    ).read_text(encoding="utf-8")

    assert re.search(
        r'srcDoc=\{inlinePreview\.html\}[\s\S]{0,220}sandbox="allow-scripts"',
        source,
    )
    assert re.search(
        r'src=\{preview\.url\}[\s\S]{0,220}sandbox="allow-scripts allow-same-origin"',
        source,
    )


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
