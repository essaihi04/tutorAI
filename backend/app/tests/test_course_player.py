import asyncio
import hashlib
import json
import re
from pathlib import Path
from types import SimpleNamespace

import app.services.course_player_service as course_player_module
from app.services.course_player_service import CoursePlayerService


BACKEND_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_ROOT.parent
COURSE_DIR = BACKEND_ROOT / "data" / "courses"
MANIFEST_PATHS = (
    COURSE_DIR / "svt_ch1_energy_course_v1.json",
    COURSE_DIR / "svt_ch1_muscle_course_v1.json",
)
SVT_SCHEMA_REGISTRY = PROJECT_ROOT / "frontend/src/components/session/schemas/schemas_svt.ts"


def _manifests():
    return [json.loads(path.read_text(encoding="utf-8")) for path in MANIFEST_PATHS]


def test_full_chapter_has_sixteen_timed_activities_and_microquestions():
    manifests = _manifests()
    activities = [activity for manifest in manifests for activity in manifest["activities"]]

    assert len(activities) == 16
    assert sum(activity["duration_minutes"] for activity in activities) == 295
    assert all(15 <= activity["duration_minutes"] <= 20 for activity in activities)
    for activity in activities:
        assert activity["objective_ids"]
        assert len(activity["slides"]) >= 2
        for slide in activity["slides"]:
            assert slide["speech_text"]["fr"].strip()
            assert slide["question"]["prompt"].strip()
            assert slide["question"]["advance_on_timeout"] is True
            assert 10 <= slide["question"]["timeout_seconds"] <= 30


def test_all_manifest_file_visuals_exist_in_frontend_public():
    for manifest in _manifests():
        for activity in manifest["activities"]:
            for slide in activity["slides"]:
                visual = slide.get("visual") or {}
                url = visual.get("url")
                if url and url.startswith("/media/"):
                    assert (PROJECT_ROOT / "frontend" / "public" / url.lstrip("/")).exists(), url


def test_each_course_has_a_complete_catalog_cover():
    for manifest in _manifests():
        catalog = manifest.get("catalog") or {}
        cover = catalog.get("cover_image") or ""

        assert catalog.get("summary", "").strip()
        assert len(catalog.get("essential_topics") or []) >= 4
        assert cover.startswith("/media/images/course-covers/")
        assert (PROJECT_ROOT / "frontend" / "public" / cover.lstrip("/")).exists()


def test_all_manifest_schema_visuals_exist_in_validated_registry():
    schema_source = SVT_SCHEMA_REGISTRY.read_text(encoding="utf-8")
    declared_ids = set(re.findall(r"\bid:\s*'([^']+)'", schema_source))
    referenced_ids = {
        slide["visual"]["schema_id"]
        for manifest in _manifests()
        for activity in manifest["activities"]
        for slide in activity["slides"]
        if (slide.get("visual") or {}).get("kind") == "schema"
    }

    assert {
        "svt_cellule_mitochondrie",
        "svt_mitochondrie_structure",
        "svt_fibre_musculaire",
        "svt_muscle_sarcomere",
    }.issubset(declared_ids)
    assert referenced_ids <= declared_ids


def test_answer_keys_are_removed_from_student_payload():
    service = CoursePlayerService()
    source = {
        "id": "slide",
        "question": {
            "type": "qcm",
            "answer_key": "A",
            "accepted_answers": ["A"],
            "evaluation_regex": "^A$",
        },
    }
    public = service._public_slide(source, [])

    assert public["question"] == {"type": "qcm"}
    assert source["question"]["answer_key"] == "A"


def test_only_published_audio_matching_current_speech_is_exposed():
    service = CoursePlayerService()
    speech = "Texte vérifié."
    source = {"id": "slide", "speech_text": {"fr": speech}, "question": {}}
    current_hash = hashlib.sha256(speech.encode("utf-8")).hexdigest()
    public = service._public_slide(source, [
        {"language": "fr", "file_path": "/old.mp3", "speech_hash": "old", "status": "published"},
        {"language": "mixed", "file_path": "/current.mp3", "speech_hash": current_hash, "status": "published"},
        {"language": "ar", "file_path": "/draft.mp3", "speech_hash": current_hash, "status": "generated"},
    ])

    assert public["audio"] == {
        "mixed": {
            "url": "/current.mp3",
            "duration_ms": None,
            "version": 1,
            "speech_hash": current_hash,
            "status": "published",
        }
    }


def test_local_answer_evaluation_and_timeout_feedback():
    service = CoursePlayerService()
    correct, _, requeue = asyncio.run(service.evaluate_attempt({
        "slide_id": "energy_a02_s01",
        "answer": "Faux",
        "outcome": "answered",
    }))
    skipped, _, skipped_requeue = asyncio.run(service.evaluate_attempt({
        "slide_id": "energy_a02_s01",
        "outcome": "skipped_timeout",
    }))

    assert correct is True
    assert requeue is False
    assert skipped is None
    assert skipped_requeue is True


def test_explicit_natural_language_requests_resolve_to_the_expected_course():
    service = CoursePlayerService()

    energy = service.match_manifest_intent("Je veux un cours sur l'ATP")
    typo_energy = service.match_manifest_intent(
        "Donne-moi un curs sur la consomation de la matière organique"
    )
    muscle = service.match_manifest_intent("Je veux réviser la contraction musculaire")

    assert energy and energy["stable_id"] == "svt_ch1_energy"
    assert typo_energy and typo_energy["stable_id"] == "svt_ch1_energy"
    assert muscle and muscle["stable_id"] == "svt_ch1_muscle"


def test_ordinary_topic_question_does_not_open_the_full_course():
    service = CoursePlayerService()

    assert service.match_manifest_intent("C'est quoi l'ATP ?") is None
    assert service.match_manifest_intent("Pourquoi le muscle se contracte ?") is None
    assert service.match_manifest_intent("Aide-moi") is None


def test_catalog_cards_and_tutor_requests_use_the_same_manifests(monkeypatch):
    subject_id = "subject-svt"
    lessons = [
        {
            "id": "lesson-energy",
            "title_fr": "Consommation de la matière organique",
            "chapter_id": "chapter-energy",
            "chapters": {
                "id": "chapter-energy",
                "title_fr": "Libération de l'énergie",
                "subject_id": subject_id,
                "subjects": {"id": subject_id, "name_fr": "SVT"},
            },
        },
        {
            "id": "lesson-muscle",
            "title_fr": "Rôle du muscle strié squelettique",
            "chapter_id": "chapter-muscle",
            "chapters": {
                "id": "chapter-muscle",
                "title_fr": "Conversion de l'énergie",
                "subject_id": subject_id,
                "subjects": {"id": subject_id, "name_fr": "SVT"},
            },
        },
    ]

    class FakeQuery:
        def __init__(self, rows):
            self.rows = rows

        def select(self, *_args, **_kwargs):
            return self

        def execute(self):
            return SimpleNamespace(data=self.rows)

    class FakeAdmin:
        def table(self, name):
            return FakeQuery(lessons if name == "lessons" else [])

    monkeypatch.setattr(course_player_module, "get_supabase_admin", lambda: FakeAdmin())
    monkeypatch.setattr(
        course_player_module.subject_access_service,
        "get_context",
        lambda _student: {
            "subjects": [{
                "id": subject_id,
                "name_fr": "Sciences de la Vie et de la Terre",
                "name_ar": "",
                "catalog_key": "svt",
            }],
        },
    )

    service = CoursePlayerService()
    catalog = asyncio.run(service.get_catalog({"id": "student"}))
    courses = catalog["subjects"][0]["courses"]

    assert catalog["total_courses"] == 2
    assert {course["lesson_id"] for course in courses} == {"lesson-energy", "lesson-muscle"}
    for course in courses:
        matched = service.match_manifest_intent(course["tutor_request"])
        assert matched and matched["stable_id"] == course["stable_id"]


def test_new_simulations_expose_platform_bridge_contract():
    simulation_paths = (
        PROJECT_ROOT / "frontend/public/media/simulations/svt/ch1_consommation_matiere_organique/atp-adp/index.html",
        PROJECT_ROOT / "frontend/public/media/simulations/svt/ch1_consommation_matiere_organique/chimiosmose/index.html",
        PROJECT_ROOT / "frontend/public/media/simulations/svt/ch1_consommation_matiere_organique/muscle/contraction/index.html",
    )
    for path in simulation_paths:
        source = path.read_text(encoding="utf-8")
        assert "simulation_manifest" in source
        assert "simulation_state" in source
        assert "postMessage" in source
        assert "set_variant" in source
        assert "reset" in source


def test_slide_scientific_visual_is_normalised_before_reaching_the_browser():
    """Une figure de diapositive passe le même filtre que celles du tableau."""
    slide = {
        "visual": {
            "kind": "scientific",
            "scientific": {
                "engine": "cytoscape",
                "title": "Respiration",
                "nodes": [{"id": "glucose", "label": "Glucose"}, {"id": "pyruvate", "label": "Pyruvate"}],
                "edges": [{"from": "glucose", "to": "pyruvate", "label": "Glycolyse"}],
            },
        },
        "question": {"prompt": "?", "answer_key": "secret"},
    }

    public = CoursePlayerService._public_slide(slide, [])

    assert public["visual"]["scientific"]["engine"] == "cytoscape"
    assert len(public["visual"]["scientific"]["nodes"]) == 2
    assert "answer_key" not in public["question"]


def test_slide_scientific_visual_refuses_an_unknown_engine():
    slide = {
        "visual": {"kind": "scientific", "scientific": {"engine": "javascript", "code": "alert(1)"}},
        "question": {},
    }

    public = CoursePlayerService._public_slide(slide, [])

    # La diapositive part quand même : le lecteur retombe sur le texte essentiel.
    assert public["visual"]["scientific"] is None


def test_schema_catalog_matches_the_browser_registry():
    """Le catalogue serveur nomme EXACTEMENT les schémas que le front sait rendre.

    Sans cette égalité, le tuteur cite des identifiants qui n'affichent rien —
    ou ignore des schémas déjà dessinés. Régénérer avec
    `python tools/generate_schema_catalog.py`.
    """
    from app.services.schema_catalog import SCHEMA_IDS

    declared = set()
    for path in (PROJECT_ROOT / "frontend/src/components/session/schemas").glob("schemas_*.ts"):
        declared |= set(re.findall(r"\bid:\s*'([a-z]+_[a-z0-9_]+)',\s*\n?\s*title:", path.read_text(encoding="utf-8")))

    assert declared, "aucun schéma trouvé dans la bibliothèque du navigateur"
    assert declared == set(SCHEMA_IDS)
