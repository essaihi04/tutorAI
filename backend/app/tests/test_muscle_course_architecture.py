import json
import unicodedata
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = PROJECT_ROOT / "backend/data/courses/svt_ch1_muscle_course_v1.json"


def _manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _plain(value):
    return "".join(
        char
        for char in unicodedata.normalize("NFKD", value.casefold())
        if not unicodedata.combining(char)
    )


def test_muscle_course_uses_a_progressive_course_architecture():
    manifest = _manifest()
    activities = manifest["activities"]
    slides = [slide for activity in activities for slide in activity["slides"]]

    assert manifest["version"] >= 3
    assert len(activities) == 5
    assert len(slides) == 18
    assert sum(activity["duration_minutes"] for activity in activities) == 98
    assert [activity["id"] for activity in activities] == [
        "muscle_a11_response",
        "muscle_a12_structure",
        "muscle_a13_sliding",
        "muscle_a14_energy_systems",
        "muscle_a15_bac",
    ]

    assert slides[0]["visual"]["kind"] == "image"
    assert "electrodes" in _plain(slides[0]["visual"]["alt"])
    assert "comment un message electrique" in _plain(slides[0]["screen_content"]["essential_text"])


def test_muscle_course_balances_photos_models_and_interactions():
    slides = [slide for activity in _manifest()["activities"] for slide in activity["slides"]]
    kinds = [slide["visual"]["kind"] for slide in slides]
    scientific = [
        slide["visual"]["scientific"]
        for slide in slides
        if slide["visual"]["kind"] == "scientific"
    ]
    preset_ids = {visual.get("presetId") for visual in scientific}

    assert kinds.count("image") >= 3
    assert kinds.count("simulation") >= 4
    assert kinds.count("scientific") >= 6
    assert {
        "svt_ch1_myogrammes",
        "svt_ch1_glissement_sarcomere",
        "svt_ch1_cycle_actomyosine",
        "svt_ch1_chaleurs_muscle",
        "svt_ch1_filieres_effort",
        "svt_ch1_couplage_excitation_contraction",
    } <= preset_ids
    assert any(
        visual.get("engine") == "three"
        and visual.get("model") == "muscle_excitation_contraction"
        for visual in scientific
    )

    for slide in slides:
        screen = slide["screen_content"]
        assert len(screen.get("bullets") or []) <= 4
        assert slide["speech_text"]["fr"].strip()
        assert slide["speech_text"]["mixed"].strip()
        assert slide["question"]["advance_on_timeout"] is True

        if slide["visual"]["kind"] == "image":
            assert slide["visual"]["alt"].strip()
            assert "Reconstitution" in slide["visual"]["caption"]
