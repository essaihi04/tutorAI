"""Catalogue ferme des scenes scientifiques animees du tableau.

Un preset n'est pas du code genere par le LLM. C'est un identifiant valide
qui sera resolu, dans le navigateur, vers JSXGraph ou Cytoscape. Le modele ne
peut choisir que la variante et la commande de lecture ; il ne fournit ni
HTML, ni JavaScript, ni URL.
"""

from __future__ import annotations

from typing import Any


SCIENTIFIC_PRESETS: dict[str, dict[str, Any]] = {
    "phys_ch1_propagation_onde": {
        "title": "Propagation, retard et superposition d’une onde",
        "subject": "Physique",
        "keywords": ["onde", "propagation", "retard", "superposition"],
        "default_variant": "propagation",
        "variants": {"propagation", "retard", "superposition"},
        "max_step": 40,
    },
    "phys_ch1_types_ondes": {
        "title": "Ondes transversales et longitudinales",
        "subject": "Physique",
        "keywords": ["onde transversale", "onde longitudinale", "déplacement", "propagation"],
        "default_variant": "comparaison",
        "variants": {"comparaison", "transversale", "longitudinale"},
        "max_step": 40,
    },
    "phys_ch1_celerite_corde": {
        "title": "Célérité d’une onde sur une corde",
        "subject": "Physique",
        "keywords": ["célérité", "corde", "tension", "masse linéique"],
        "default_variant": "forte_tension",
        "variants": {"forte_tension", "faible_tension", "forte_masse_lineique"},
        "max_step": 40,
    },
    "chem_ch1_facteurs_cinetiques": {
        "title": "Facteurs cinétiques",
        "subject": "Chimie",
        "keywords": ["cinétique", "température", "concentration", "catalyseur", "surface"],
        "default_variant": "temperature",
        "variants": {"temperature", "concentration", "catalyseur", "surface_contact"},
        "max_step": 36,
    },
    "chem_ch1_energie_activation": {
        "title": "Énergie d’activation et catalyse",
        "subject": "Chimie",
        "keywords": ["énergie d’activation", "catalyseur", "profil énergétique", "Ea"],
        "default_variant": "comparaison",
        "variants": {"comparaison", "sans_catalyseur", "avec_catalyseur"},
        "max_step": 36,
    },
    "chem_ch1_oxydoreduction": {
        "title": "Transfert d’électrons en oxydoréduction",
        "subject": "Chimie",
        "keywords": ["oxydoréduction", "électrons", "pile", "électrolyse"],
        "default_variant": "transfert_direct",
        "variants": {"transfert_direct", "pile", "electrolyse"},
        "max_step": 7,
    },
    "svt_ch1_respiration_mitochondriale": {
        "title": "Bilan de la respiration mitochondriale",
        "subject": "SVT",
        "keywords": ["mitochondrie", "Krebs", "chaîne respiratoire", "ATP"],
        "default_variant": "bilan",
        "variants": {"bilan", "krebs", "chaine_respiratoire"},
        "max_step": 9,
    },
    "svt_ch1_glissement_sarcomere": {
        "title": "Glissement des filaments et raccourcissement du sarcomère",
        "subject": "SVT",
        "keywords": ["sarcomère", "actine", "myosine", "glissement", "contraction"],
        "default_variant": "contraction",
        "variants": {"repos", "contraction", "comparaison"},
        "max_step": 30,
    },
    "svt_ch1_couplage_excitation_contraction": {
        "title": "Couplage excitation–contraction–relaxation",
        "subject": "SVT",
        "keywords": ["potentiel d’action", "calcium", "réticulum", "contraction", "relaxation"],
        "default_variant": "cycle_complet",
        "variants": {"cycle_complet", "liberation_calcium", "contraction", "relaxation"},
        "max_step": 8,
    },
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
    "svt_ch1_glycolyse_etapes": {
        "title": "Les étapes de la glycolyse", "subject": "SVT",
        "keywords": ["glycolyse", "enzymes", "ATP net", "NADH,H+", "pyruvate"],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 9,
    },
    "svt_ch1_krebs_detaille": {
        "title": "Oxydation du pyruvate et cycle de Krebs", "subject": "SVT",
        "keywords": ["Krebs", "acétyl-CoA", "décarboxylation", "NADH,H+", "FADH2"],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 10,
    },
    "svt_ch1_echelle_redox": {
        "title": "Potentiels d’oxydoréduction", "subject": "SVT",
        "keywords": ["potentiel redox", "électrons", "NADH", "dioxygène", "chaîne respiratoire"],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 8,
    },
    "svt_ch1_molecules_glucose_atp": {
        "title": "Structure du glucose et de l’ATP", "subject": "SVT",
        "keywords": ["glucose", "ATP", "adénine", "ribose", "phosphate", "hydrolyse"],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 5,
    },
    "svt_ch1_rendement_energetique": {
        "title": "Bilan en ATP et rendement énergétique", "subject": "SVT",
        "keywords": ["38 ATP", "36 ATP", "40,5 %", "2,13 %", "rendement énergétique"],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 10,
    },
    "svt_ch1_schema_bilan_annote": {
        "title": "Schéma-bilan de la respiration", "subject": "SVT",
        "keywords": ["schéma bilan", "hyaloplasme", "matrice", "membrane interne", "34 ATP"],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 21,
    },
    "svt_ch1_vesicules_atp_synthase": {
        "title": "Rôle des sphères pédonculées", "subject": "SVT",
        "keywords": ["vésicules", "sphères pédonculées", "ATP synthase", "gradient de protons", "pH"],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 8,
    },
    "svt_ch1_ultrastructure_mitochondrie": {
        "title": "Ultrastructure et composition de la mitochondrie", "subject": "SVT",
        "keywords": [
            "ultrastructure de la mitochondrie", "annoter la mitochondrie", "membrane externe",
            "membrane interne", "crêtes mitochondriales", "espace intermembranaire", "matrice",
            "ADN mitochondrial", "porine", "composition chimique des membranes",
            "بنية الميتوكوندري",
        ],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 12,
    },
    "svt_ch1_flux_protons": {
        "title": "Réduction du dioxygène et flux de protons", "subject": "SVT",
        "keywords": [
            "flux de protons", "pulse de dioxygène", "pH-mètre", "concentration en protons",
            "espace intermembranaire", "gradient de H+", "réduction du dioxygène",
            "تدفق البروتونات",
        ],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 8,
    },
    "svt_ch1_chimiosmose": {
        "title": "Chaîne respiratoire et chimiosmose",
        "subject": "SVT",
        "keywords": ["mitochondrie", "chimiosmose", "protons", "ATP synthase"],
        "default_variant": "scene",
        "variants": {"scene"},
        "max_step": 12,
    },
    "svt_ch1_carte_metabolique": {
        "title": "De la matière organique à l’ATP",
        "subject": "SVT",
        "keywords": ["métabolisme", "respiration", "fermentation", "ATP"],
        "default_variant": "scene",
        "variants": {"scene"},
        "max_step": 10,
    },
    "svt_ch1_myogrammes": {
        "title": "Réponses mécaniques du muscle",
        "subject": "SVT",
        "keywords": ["muscle", "myogramme", "secousse", "tétanos"],
        "default_variant": "secousse",
        "variants": {"secousse", "sommation", "tetanus_incomplet", "tetanus_complet"},
        "max_step": 32,
    },
    "svt_ch1_chaleurs_muscle": {
        "title": "Secousse musculaire et dégagements de chaleur",
        "subject": "SVT",
        "keywords": ["muscle", "myogramme", "chaleur initiale", "chaleur retardée", "oxygène", "récupération"],
        "default_variant": "comparaison",
        "variants": {"comparaison", "avec_oxygene", "sans_oxygene"},
        "max_step": 36,
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


def normalize_scientific_state(value: Any) -> dict[str, Any] | None:
    """Borne l'état remonté par une scène de catalogue avant de l'exposer au LLM."""

    if not isinstance(value, dict):
        return None
    preset_id = value.get("simulation_id")
    if not isinstance(preset_id, str) or preset_id not in SCIENTIFIC_PRESETS:
        return None
    definition = SCIENTIFIC_PRESETS[preset_id]
    raw_state = value.get("current_state")
    raw_state = raw_state if isinstance(raw_state, dict) else {}
    variant = raw_state.get("variant")
    if not isinstance(variant, str) or variant not in definition["variants"]:
        variant = definition["default_variant"]
    try:
        step = int(raw_state.get("step", 0))
    except (TypeError, ValueError):
        step = 0
    step = max(0, min(definition["max_step"], step))
    status = raw_state.get("simulation_status")
    if status not in {"idle", "running", "paused", "finished"}:
        status = "idle"
    action = ""
    raw_actions = value.get("student_actions")
    if isinstance(raw_actions, list) and raw_actions and isinstance(raw_actions[-1], dict):
        candidate = raw_actions[-1].get("action")
        if isinstance(candidate, str):
            action = candidate.strip()[:40]
    return {
        "id": preset_id,
        "state": {
            "simulation_status": status,
            "preset_id": preset_id,
            "variant": variant,
            "step": step,
            "max_step": definition["max_step"],
        },
        "actions": ([{"action": action, "variant": variant, "step": step}] if action else []),
        "progress": step / definition["max_step"] if definition["max_step"] else 0,
    }
