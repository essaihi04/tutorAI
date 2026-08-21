import asyncio
import hashlib
import json
from pathlib import Path

from app.services.course_player_service import CoursePlayerService


BACKEND_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_ROOT.parent
COURSE_DIR = BACKEND_ROOT / "data" / "courses"
MANIFEST_PATHS = (
    COURSE_DIR / "svt_ch1_energy_course_v1.json",
    COURSE_DIR / "svt_ch1_muscle_course_v1.json",
)


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
