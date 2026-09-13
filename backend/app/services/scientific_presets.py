"""Catalogue ferme des scenes scientifiques animees du tableau.

Un preset n'est pas du code genere par le LLM. C'est un identifiant valide
qui sera resolu, dans le navigateur, vers JSXGraph ou Cytoscape. Le modele ne
peut choisir que la variante et la commande de lecture ; il ne fournit ni
HTML, ni JavaScript, ni URL.
"""

from __future__ import annotations

import math
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
    "svt_ch1_pyruvate_acetyl_coa": {
        "title": "Voyage du pyruvate vers la matrice", "subject": "SVT",
        "keywords": ["pyruvate", "matrice", "acétyl-CoA", "CO2", "NADH,H+", "Krebs"],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 8,
    },
    "svt_ch1_krebs_detaille": {
        "title": "Cycle de Krebs dans la matrice", "subject": "SVT",
        "keywords": ["Krebs", "acétyl-CoA", "décarboxylation", "NADH,H+", "FADH2", "GTP"],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 8,
    },
    "svt_ch1_echelle_redox": {
        "title": "Potentiels d’oxydoréduction", "subject": "SVT",
        "keywords": ["potentiel redox", "électrons", "NADH", "dioxygène", "chaîne respiratoire"],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 8,
    },
    "svt_ch1_molecules_glucose_atp": {
        "title": "Structure du glucose et de l’ATP", "subject": "SVT",
        "keywords": ["glucose", "ATP", "adénine", "ribose", "phosphate", "hydrolyse", "glycolyse"],
        "default_variant": "glucose", "variants": {"glucose", "atp", "scene"}, "max_step": 5,
    },
    "svt_ch1_rendement_energetique": {
        "title": "Bilan en ATP et rendement énergétique", "subject": "SVT",
        "keywords": ["38 ATP", "36 ATP", "40,5 %", "2,13 %", "rendement énergétique"],
        "default_variant": "scene", "variants": {"scene", "navette_36"}, "max_step": 10,
        "steps": {
            0: "glycolyse : glucose vers deux pyruvates",
            1: "gain net de deux ATP", 2: "deux NADH,H⁺ cytoplasmiques",
            3: "matrice : oxydation du pyruvate puis Krebs",
            4: "deux ATP directs", 5: "huit NADH,H⁺ et deux FADH₂",
            6: "transporteurs vers la chaîne", 7: "34 ATP via la chaîne (32 avec navette_36)",
            8: "assemblage visuel : 2 + 2 + 34 = 38 ATP (ou 36)",
            9: "rendements sur la même échelle : respiration et fermentation",
            10: "bilan final : énergie conservée dans l’ATP",
        },
    },
    "svt_ch1_schema_bilan_annote": {
        "title": "Schéma-bilan de la respiration", "subject": "SVT",
        "keywords": ["schéma bilan", "hyaloplasme", "matrice", "membrane interne", "34 ATP"],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 21,
    },
    "svt_ch1_vesicules_atp_synthase": {
        "title": "Rôle des sphères pédonculées", "subject": "SVT",
        "keywords": ["vésicules", "sphères pédonculées", "ATP synthase", "gradient de protons", "pH"],
        "default_variant": "scene", "variants": {"scene", "acide_externe", "equilibre", "acide_interne", "personnalisee"}, "max_step": 8,
        "numeric_parameters": {"pHi": {"min": 4, "max": 10, "step": 0.5}, "pHe": {"min": 4, "max": 10, "step": 0.5}},
        "steps": {
            0: "préparation : mitochondrie isolée",
            1: "ultrasons et fragments de membrane interne",
            2: "repliement en vésicules retournées, sphères vers l’extérieur",
            3: "solution tampon : pHi interne et pHe externe",
            4: "comparaison pHi 6 et pHe 4 : pas d’ATP",
            5: "comparaison pHi 7 et pHe 7 : pas d’ATP",
            6: "comparaison pHi 6 et pHe 9 : ATP synthétisé",
            7: "condition du gradient : pHi inférieur à pHe",
            8: "bilan : gradient sortant, ADP, Pi et ATP synthase",
        },
    },
    "svt_ch1_isolement_cretes_ultrasons": {
        "title": "Isolement des crêtes par ultrasons", "subject": "SVT",
        "keywords": [
            "sonication", "ultrasons", "isolement des crêtes", "membrane interne",
            "fragments membranaires", "vésicules retournées", "orientation inversée",
            "face matricielle", "espace intermembranaire", "sphères pédonculées",
        ],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 3,
        "steps": {
            0: "mitochondrie intacte et prédiction de l’orientation",
            1: "sonication de la suspension mitochondriale",
            2: "fragmentation puis repliement de la membrane interne",
            3: "vésicules retournées : face matricielle externe et côté intermembranaire interne",
        },
    },
    "svt_ch1_fermentations_photos": {
        "title": "Fermentations lactique et alcoolique en photos", "subject": "SVT",
        "keywords": [
            "fermentation lactique", "fermentation alcoolique", "muscle", "levure",
            "lactate", "éthanol", "CO2", "régénération du NAD+", "anaérobiose",
        ],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 3,
        "steps": {
            0: "question : muscle et levure forment-ils les mêmes produits sans O2",
            1: "muscle : pyruvate transformé en lactate et NAD+ régénéré",
            2: "levure : pyruvate transformé en éthanol et CO2, NAD+ régénéré",
            3: "comparaison : produits différents, glycolyse maintenue et 2 ATP nets",
        },
    },
    "svt_ch1_ultrastructure_mitochondrie": {
        "title": "Ultrastructure et composition de la mitochondrie", "subject": "SVT",
        "keywords": [
            "ultrastructure de la mitochondrie", "annoter la mitochondrie", "membrane externe",
            "membrane interne", "crêtes mitochondriales", "espace intermembranaire", "matrice",
            "porine", "gradient de H+", "ATP synthase", "sphère pédonculée",
            "pyruvate", "acétyl-CoA", "NADH,H+", "FADH2", "composition chimique des membranes",
            "بنية الميتوكوندري",
        ],
        "default_variant": "scene", "variants": {"scene"}, "max_step": 4,
        "steps": {
            0: "mitochondrie entière",
            1: "membrane externe et porines",
            2: "membrane interne, crêtes, complexes respiratoires et ATP synthase",
            3: "espace intermembranaire et gradient de H+",
            4: "matrice : pyruvate, acétyl-CoA, NAD/FAD, ATP et H2O",
        },
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
        "title": "Chaîne respiratoire et phosphorylation oxydative",
        "subject": "SVT",
        "keywords": ["mitochondrie", "chimiosmose", "protons", "ATP synthase", "NADH", "FADH2", "phosphorylation oxydative", "sphère pédonculée"],
        "default_variant": "nadh",
        "variants": {"scene", "nadh", "fadh2"},
        "max_step": 18,
        "steps": {
            0: "membrane interne ; scene est un alias historique de nadh",
            1: "électrons : NADH via CI ou FADH₂ via CII, puis Q, CIII, cyt c, CIV",
            4: "accumulation progressive des H⁺ dans l’espace intermembranaire ; CII ne pompe pas",
            7: "exemple : espace pH 7 et 100 nmol/L ; matrice pH 8 et 10 nmol/L ; ΔpH = 1",
            9: "retour des H⁺ par ATP synthase ; le pompage entretient encore le gradient",
            11: "bilan scolaire : 3 ATP/NADH,H⁺ ou 2 ATP/FADH₂ ; synthèse côté matrice",
            13: "arrêt du pompage ; début de dissipation du gradient par retour des H⁺",
            16: "pH qui se rapprochent ; concentration de H⁺ en baisse dans l’espace et en hausse dans la matrice",
            18: "équilibre du modèle : même pH, gradient électrochimique dissipé, synthèse arrêtée",
        },
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


def _numeric_parameters(definition: dict, value: Any) -> dict[str, float]:
    if not isinstance(value, dict):
        return {}
    result = {}
    for key, bounds in definition.get("numeric_parameters", {}).items():
        raw = value.get(key)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            continue
        try:
            number = float(raw)
        except (ValueError, OverflowError):
            continue
        if not math.isfinite(number):
            continue
        number = max(bounds["min"], min(bounds["max"], number))
        result[key] = math.floor(number / bounds["step"] + 0.5) * bounds["step"]
    return result


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

    result = {
        "engine": "preset",
        "presetId": preset_id,
        "variant": variant,
        "autoplay": value.get("autoplay") is True,
        "step": step,
    }
    if parameters := _numeric_parameters(definition, value.get("parameters")):
        result["parameters"] = parameters
    return result


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
    if SCIENTIFIC_PRESETS[preset_id].get("numeric_parameters"):
        allowed.add("set_parameters")
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

    numeric = _numeric_parameters(definition, raw_parameters)
    if command == "set_parameters" and not numeric:
        return None
    if command in {"set_parameters", "set_variant", "highlight"}:
        parameters.update(numeric)

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
    result = {
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
    if preset_id == "svt_ch1_chimiosmose":
        # Recompute the illustrative model from its bounded step; never trust
        # client-supplied pH, yields or claims of ATP synthesis at equilibrium.
        strength = (18 - step) / 5 if step >= 13 else min(1, max(0, (step - 3) / 4))
        outer = 55 + 45 * strength
        matrix = 55 - 45 * strength
        outer_ph, matrix_ph = 9 - math.log10(outer), 9 - math.log10(matrix)
        result["state"]["respiratory_gradient"] = {
            "intermembrane_ph": outer_ph,
            "matrix_ph": matrix_ph,
            "delta_pH": matrix_ph - outer_ph,
            "concentration_ratio": outer / matrix,
            "proton_pumping": 4 <= step < 13,
            "atp_synthesis": 11 <= step < 18,
            "school_atp_yield": 2 if variant == "fadh2" else 3,
        }
    if preset_id == "svt_ch1_vesicules_atp_synthase":
        parameters = _numeric_parameters(definition, raw_state)
        if len(parameters) == 2:
            delta = parameters["pHe"] - parameters["pHi"]
            result["state"].update(parameters)
            # Recalculer, sans croire un résultat arbitraire fourni par le client.
            result["state"].update({
                "delta_pH": delta,
                "proton_direction": "outward" if delta > 0 else "inward" if delta < 0 else "none",
                "atp_synthesis": step >= 4 and delta > 0,
            })
            for item in result["actions"]:
                item.update(parameters)
        completed = raw_state.get("variants_completed")
        known = {"acide_externe", "equilibre", "acide_interne"}
        completed = sorted({item for item in completed if isinstance(item, str) and item in known}) if isinstance(completed, list) else []
        result["state"]["variants_completed"] = completed
        result["progress"] = len(completed) / 3
    return result
