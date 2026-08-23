import json
from pathlib import Path

from app.services.admin_course_service import AdminCourseService


COURSE_DIR = Path(__file__).resolve().parents[2] / "data" / "courses"


def _minimal_payload() -> dict:
    return {
        "stable_id": "test_course",
        "title": "Cours de test",
        "language": "fr",
        "estimated_minutes": 15,
        "catalog": {},
        "lesson_match": ["test"],
        "intent_aliases": ["cours de test"],
        "activities": [{
            "stable_id": "test_course_a01",
            "title": "Activité",
            "phase": "diagnostic",
            "duration_minutes": 15,
            "objective_ids": ["observer"],
            "slides": [{
                "stable_id": "test_course_s01",
                "slide_type": "diagnostic",
                "title": "Diapositive",
                "screen_content": {"lead": "Observer."},
                "visual": {"kind": "schema", "schema_id": "phys_ondes_mecaniques"},
                "speech_text": {"fr": "Observe le schéma.", "mixed": "شوف هاد schéma."},
                "question": {
                    "type": "true_false",
                    "prompt": "Vrai ou faux ?",
                    "options": ["Vrai", "Faux"],
                    "answer_key": "Vrai",
                    "timeout_seconds": 15,
                    "advance_on_timeout": True,
                },
                "timing": {"auto_advance": True},
            }],
        }],
    }


def test_all_authored_manifests_are_publishable_by_the_admin_editor():
    service = AdminCourseService()
    paths = sorted(COURSE_DIR.glob("*_course_v1.json"))

    assert paths
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert service.validate_payload(payload, for_publish=True) == [], path.name


def test_publish_validation_requires_darija_question_and_auto_advance():
    service = AdminCourseService()
    payload = _minimal_payload()
    slide = payload["activities"][0]["slides"][0]
    slide["speech_text"].pop("mixed")
    slide["question"]["prompt"] = ""
    slide["question"]["advance_on_timeout"] = False

    issues = service.validate_payload(payload, for_publish=True)
    paths = {issue["path"] for issue in issues if issue["level"] == "error"}

    assert "activities[0].slides[0].speech_text.mixed" in paths
    assert "activities[0].slides[0].question.prompt" in paths
    assert "activities[0].slides[0].question.advance_on_timeout" in paths


def test_editor_rejects_unknown_schema_and_non_persistent_simulation():
    service = AdminCourseService()
    payload = _minimal_payload()
    slide = payload["activities"][0]["slides"][0]
    slide["visual"] = {"kind": "schema", "schema_id": "schema_invente"}
    schema_issues = service.validate_payload(payload)

    slide["visual"] = {"kind": "simulation", "url": "https://example.org/lab.html"}
    simulation_issues = service.validate_payload(payload)

    assert any(issue["path"].endswith("visual.schema_id") for issue in schema_issues)
    assert any(issue["path"].endswith("visual.url") for issue in simulation_issues)


def test_editor_rejects_duplicate_slide_ids_and_javascript_visuals():
    service = AdminCourseService()
    payload = _minimal_payload()
    original = payload["activities"][0]["slides"][0]
    duplicate = json.loads(json.dumps(original))
    duplicate["visual"] = {
        "kind": "scientific",
        "scientific": {"engine": "javascript", "code": "alert(1)"},
    }
    payload["activities"][0]["slides"].append(duplicate)

    issues = service.validate_payload(payload)

    assert any("dupliqué" in issue["message"] for issue in issues)
    assert any(issue["path"].endswith("visual.scientific") for issue in issues)


def test_sanitiser_keeps_only_normalised_declarative_scientific_payload():
    service = AdminCourseService()
    payload = _minimal_payload()
    payload["activities"][0]["slides"][0]["visual"] = {
        "kind": "scientific",
        "scientific": {
            "engine": "jsxgraph",
            "title": "Segment",
            "boundingBox": [-5, 5, 5, -5],
            "elements": [{
                "type": "segment",
                "points": [{"x": -1, "y": 0}, {"x": 1, "y": 0}],
                "label": "AB",
                "onclick": "alert(1)",
            }],
            "script": "alert(1)",
        },
    }

    cleaned = service._sanitise_payload(payload)
    scientific = cleaned["activities"][0]["slides"][0]["visual"]["scientific"]

    assert scientific["engine"] == "jsxgraph"
    assert "script" not in scientific
    assert "onclick" not in scientific["elements"][0]
