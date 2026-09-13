"""The authored respiratory-chain scene and its closed tutor contract."""
import json
from pathlib import Path

import pytest

from app.services.scientific_presets import normalize_scientific_control, normalize_scientific_state
from app.services.scientific_visual_skill import SCIENTIFIC_VISUAL_PROMPT, normalize_scientific_visual


@pytest.mark.parametrize("variant", ["nadh", "fadh2", "scene"])
def test_respiratory_variants_are_preserved_in_visual_control_and_state(variant):
    preset_id = "svt_ch1_chimiosmose"
    visual = normalize_scientific_visual({
        "engine": "preset", "presetId": preset_id, "variant": variant, "step": 999,
    })
    assert visual["variant"] == variant
    assert visual["step"] == 18
    command = normalize_scientific_control({
        "presetId": preset_id, "command": "set_variant",
        "parameters": {"variant": variant, "javascript": "untrusted"},
    })
    assert command["parameters"] == {"variant": variant}
    state = normalize_scientific_state({
        "simulation_id": preset_id,
        "current_state": {"variant": variant, "step": 18, "simulation_status": "finished"},
        "student_actions": [{"action": "finish_simulation"}],
    })
    assert state["state"]["variant"] == variant
    assert state["state"]["simulation_status"] == "finished"
    assert state["progress"] == 1


def test_unknown_donor_falls_back_to_nadh():
    visual = normalize_scientific_visual({
        "engine": "preset", "presetId": "svt_ch1_chimiosmose", "variant": "invented",
    })
    assert visual["variant"] == "nadh"


def test_course_scene_matches_its_two_donors_and_matrix_orientation():
    manifest_path = Path(__file__).resolve().parents[2] / "data/courses/svt_ch1_energy_course_v1.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    slide = next(slide for activity in manifest["activities"] for slide in activity["slides"]
                 if slide["id"] == "energy_a07_s02")
    assert slide["title"] == "Chaîne respiratoire et phosphorylation oxydative"
    assert slide["visual"]["scientific"]["variant"] == "nadh"
    assert slide["visual"]["scientific"]["autoplay"] is True
    assert "FADH₂" in slide["screen_content"]["lead"]
    assert "Compare O₂" not in slide["screen_content"]["lead"]
    speech = slide["speech_text"]["fr"]
    for expected in ("3 ATP", "2 ATP", "convention scolaire", "matrice mitochondriale", "sphère pédonculée", "pH", "équilibre"):
        assert expected in speech
    assert slide["question"]["answer_key"] in slide["question"]["options"]
    assert "variant=nadh" in SCIENTIFIC_VISUAL_PROMPT
    assert "variant=fadh2" in SCIENTIFIC_VISUAL_PROMPT


@pytest.mark.parametrize("variant,atp", [("nadh", 3), ("fadh2", 2), ("scene", 3)])
def test_gradient_is_derived_safely_and_school_yields_are_explicit(variant, atp):
    frames = []
    for step in range(19):
        result = normalize_scientific_state({
            "simulation_id": "svt_ch1_chimiosmose",
            "current_state": {"step": step, "variant": variant, "respiratory_gradient": {
                "matrix_ph": -99, "atp_synthesis": True, "school_atp_yield": 999,
            }},
        })
        frame = result["state"]["respiratory_gradient"]
        assert frame["school_atp_yield"] == atp
        assert 7 <= frame["intermembrane_ph"] <= frame["matrix_ph"] <= 8
        frames.append(frame)
    assert frames[7]["intermembrane_ph"] == 7
    assert frames[7]["matrix_ph"] == 8
    assert frames[7]["concentration_ratio"] == 10
    assert frames[11]["proton_pumping"] and frames[11]["atp_synthesis"]
    for previous, current in zip(frames[13:], frames[14:]):
        assert not current["proton_pumping"]
        assert current["delta_pH"] < previous["delta_pH"]
    assert frames[18]["delta_pH"] == 0
    assert not frames[18]["atp_synthesis"]
