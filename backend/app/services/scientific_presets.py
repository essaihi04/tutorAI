"""Catalogue ferme des scenes scientifiques animees du tableau.

Un preset n'est pas du code genere par le LLM. C'est un identifiant valide
qui sera resolu, dans le navigateur, vers JSXGraph ou Cytoscape. Le modele ne
peut choisir que la variante et la commande de lecture ; il ne fournit ni
HTML, ni JavaScript, ni URL.
"""

from __future__ import annotations

from typing import Any


SCIENTIFIC_PRESETS: dict[str, dict[str, Any]] = {
    "svt_ch1_cycle_atp": {
        "title": "Cycle ATP–ADP",
        "subject": "SVT",
        "keywords": ["ATP", "ADP", "énergie", "couplage"],
        "default_variant": "cycle_complet",
        "variants": {"cycle_complet", "hydrolyse", "phosphorylation", "couplage"},
        "max_step": 5,
    },
    "svt_ch1_levures_exao": {
        "title": "Levures : respiration ou fermentation",
        "subject": "SVT",
        "keywords": ["levures", "ExAO", "respiration", "fermentation"],
        "default_variant": "comparaison",
        "variants": {"comparaison", "avec_oxygene", "sans_oxygene"},
        "max_step": 24,
    },
    "svt_ch1_chimiosmose": {
        "title": "Chaîne respiratoire et chimiosmose",
        "subject": "SVT",
        "keywords": ["mitochondrie", "chimiosmose", "protons", "ATP synthase"],
        "default_variant": "cycle_complet",
        "variants": {"cycle_complet", "transfert_electrons", "pompage_protons", "synthese_atp"},
        "max_step": 7,
    },
    "svt_ch1_carte_metabolique": {
        "title": "De la matière organique à l’ATP",
        "subject": "SVT",
        "keywords": ["métabolisme", "respiration", "fermentation", "ATP"],
        "default_variant": "vue_ensemble",
        "variants": {"vue_ensemble", "respiration", "fermentation_lactique", "fermentation_alcoolique"},
        "max_step": 8,
    },
    "svt_ch1_myogrammes": {
        "title": "Réponses mécaniques du muscle",
        "subject": "SVT",
        "keywords": ["muscle", "myogramme", "secousse", "tétanos"],
        "default_variant": "secousse",
        "variants": {"secousse", "sommation", "tetanus_incomplet", "tetanus_complet"},
        "max_step": 32,
    },
    "svt_ch1_cycle_actomyosine": {
        "title": "Cycle des ponts actine–myosine",
        "subject": "SVT",
        "keywords": ["actine", "myosine", "contraction", "ATP"],
        "default_variant": "cycle_complet",
        "variants": {"cycle_complet", "fixation", "pivotement", "detachement", "reactivation"},
        "max_step": 5,
    },
    "svt_ch1_filieres_effort": {
        "title": "Régénération de l’ATP pendant l’effort",
        "subject": "SVT",
        "keywords": ["effort", "filières", "muscle", "ATP"],
        "default_variant": "vue_ensemble",
        "variants": {"vue_ensemble", "effort_bref", "effort_intense", "effort_prolonge", "recuperation"},
        "max_step": 7,
    },
}


def normalize_scientific_preset(value: Any) -> dict[str, Any] | None:
    """Normalise une reference de preset sans laisser passer de contenu libre."""

    if not isinstance(value, dict):
        return None
    preset_id = value.get("presetId") or value.get("preset_id") or value.get("preset")
    if not isinstance(preset_id, str) or preset_id not in SCIENTIFIC_PRESETS:
        return None

    definition = SCIENTIFIC_PRESETS[preset_id]
    variant = value.get("variant")
    if not isinstance(variant, str) or variant not in definition["variants"]:
        variant = definition["default_variant"]

    try:
        step = int(value.get("step", 0))
    except (TypeError, ValueError):
        step = 0
    step = max(0, min(definition["max_step"], step))

    return {
        "engine": "preset",
        "presetId": preset_id,
        "variant": variant,
        "autoplay": value.get("autoplay") is True,
        "step": step,
    }


def normalize_scientific_control(value: Any) -> dict[str, Any] | None:
    """Valide une commande LLM destinee a une scene deja affichee."""

    if not isinstance(value, dict):
        return None
    preset_id = value.get("presetId") or value.get("preset_id") or value.get("preset")
    if not isinstance(preset_id, str) or preset_id not in SCIENTIFIC_PRESETS:
        return None

    aliases = {"play": "start", "stop": "pause", "restart": "reset"}
    command = str(value.get("command", "")).strip().lower()
    command = aliases.get(command, command)
    allowed = {"start", "pause", "reset", "next", "previous", "set_variant", "highlight"}
    if command not in allowed:
        return None

    raw_parameters = value.get("parameters")
    raw_parameters = raw_parameters if isinstance(raw_parameters, dict) else {}
    parameters: dict[str, Any] = {}
    definition = SCIENTIFIC_PRESETS[preset_id]

    variant = raw_parameters.get("variant") or value.get("variant")
    if command in {"set_variant", "highlight"}:
        if not isinstance(variant, str) or variant not in definition["variants"]:
            return None
        parameters["variant"] = variant

    if "step" in raw_parameters:
        try:
            step = int(raw_parameters["step"])
        except (TypeError, ValueError):
            step = 0
        parameters["step"] = max(0, min(definition["max_step"], step))

    return {"presetId": preset_id, "command": command, "parameters": parameters}
