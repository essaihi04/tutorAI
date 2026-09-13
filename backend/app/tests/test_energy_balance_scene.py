"""Closed variants and tutor navigation for the compact energy balance."""
import pytest

from app.services.scientific_presets import SCIENTIFIC_PRESETS, normalize_scientific_control, normalize_scientific_state
from app.services.scientific_visual_skill import SCIENTIFIC_VISUAL_PROMPT, normalize_scientific_visual

PRESET = "svt_ch1_rendement_energetique"


@pytest.mark.parametrize("variant", ["scene", "navette_36"])
def test_energy_variants_roundtrip_through_visual_control_and_state(variant):
    visual = normalize_scientific_visual({"engine": "preset", "presetId": PRESET, "variant": variant, "step": 999})
    assert visual["variant"] == variant
    assert visual["step"] == 10
    command = normalize_scientific_control({"presetId": PRESET, "command": "set_variant", "parameters": {"variant": variant, "javascript": "untrusted"}})
    assert command["parameters"] == {"variant": variant}
    result = normalize_scientific_state({"simulation_id": PRESET, "current_state": {"variant": variant, "step": 10, "simulation_status": "finished"}})
    assert result["state"]["variant"] == variant
    assert result["state"]["simulation_status"] == "finished"
    assert result["progress"] == 1


@pytest.mark.parametrize("step", range(11))
def test_every_visual_phase_remains_tutor_addressable(step):
    command = normalize_scientific_control({"presetId": PRESET, "command": "highlight", "parameters": {"variant": "scene", "step": step}})
    assert command["parameters"]["step"] == step
    assert step in SCIENTIFIC_PRESETS[PRESET]["steps"]


def test_unknown_variant_defaults_and_prompt_routes_to_contextual_views():
    result = normalize_scientific_visual({"engine": "preset", "presetId": PRESET, "variant": "invented"})
    assert result["variant"] == "scene"
    assert "variant=navette_36" in SCIENTIFIC_VISUAL_PROMPT
    assert "sans bloc de calculs permanent" in SCIENTIFIC_VISUAL_PROMPT
    assert "9–10 rendement" in SCIENTIFIC_VISUAL_PROMPT
