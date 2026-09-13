"""Contrat fermé de l'expérience à pHi / pHe réglables."""
import pytest

from app.services.scientific_presets import normalize_scientific_control, normalize_scientific_state
from app.services.scientific_visual_skill import SCIENTIFIC_VISUAL_PROMPT, normalize_scientific_visual

PRESET = "svt_ch1_vesicules_atp_synthase"


@pytest.mark.parametrize("variant", ["scene", "acide_externe", "equilibre", "acide_interne", "personnalisee"])
def test_variants_and_ph_survive_the_closed_contract(variant):
    visual = normalize_scientific_visual({
        "engine": "preset", "presetId": PRESET, "variant": variant,
        "parameters": {"pHi": 6, "pHe": 9, "atp": True, "code": "untrusted"},
    })
    assert visual["variant"] == variant
    assert visual["parameters"] == {"pHi": 6, "pHe": 9}


def test_tutor_can_change_only_one_ph():
    command = normalize_scientific_control({
        "presetId": PRESET, "command": "set_parameters",
        "parameters": {"pHe": 8.5, "atp_synthesis": False, "url": "untrusted"},
    })
    assert command["parameters"] == {"pHe": 8.5}
    assert "command\":\"set_parameters" in SCIENTIFIC_VISUAL_PROMPT


@pytest.mark.parametrize("value,expected", [(-1, 4), (99, 10), (6.25, 6.5), (6.24, 6)])
def test_ph_bounds_and_half_unit_steps(value, expected):
    command = normalize_scientific_control({
        "presetId": PRESET, "command": "set_parameters", "parameters": {"pHi": value},
    })
    assert command["parameters"] == {"pHi": expected}


@pytest.mark.parametrize("value", [None, True, False, "7", "fetch(secret)", [], {}, float("nan"), float("inf"), 10**1000])
def test_reject_invalid_and_nonfinite_ph(value):
    assert normalize_scientific_control({
        "presetId": PRESET, "command": "set_parameters", "parameters": {"pHi": value},
    }) is None


def test_parameters_command_is_not_enabled_for_other_presets():
    assert normalize_scientific_control({
        "presetId": "svt_ch1_cycle_atp", "command": "set_parameters", "parameters": {"pHi": 6},
    }) is None
    visual = normalize_scientific_visual({
        "engine": "preset", "presetId": "svt_ch1_cycle_atp", "parameters": {"pHi": 6},
    })
    assert "parameters" not in visual


@pytest.mark.parametrize("pHi,pHe,direction,atp", [(6, 4, "inward", False), (7, 7, "none", False), (6, 9, "outward", True), (5.5, 8, "outward", True)])
def test_state_contains_actual_ph_and_recomputed_result(pHi, pHe, direction, atp):
    state = normalize_scientific_state({
        "simulation_id": PRESET,
        "current_state": {
            "step": 4, "variant": "personnalisee", "simulation_status": "finished",
            "pHi": pHi, "pHe": pHe, "atp_synthesis": not atp,
            "variants_completed": ["acide_interne", "acide_interne", "invented", {}],
        },
        "student_actions": [{"action": "change_ph"}],
    })
    assert state["state"]["delta_pH"] == pHe - pHi
    assert state["state"]["proton_direction"] == direction
    assert state["state"]["atp_synthesis"] is atp
    assert state["state"]["variants_completed"] == ["acide_interne"]
    assert state["progress"] == pytest.approx(1 / 3)
    assert state["actions"][0]["pHi"] == pHi


def test_preparation_does_not_report_atp_synthesis():
    state = normalize_scientific_state({"simulation_id": PRESET, "current_state": {"step": 3, "pHi": 6, "pHe": 9}})
    assert state["state"]["atp_synthesis"] is False
