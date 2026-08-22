"""Contrat de sécurité des visuels scientifiques produits par le LLM."""

from app.services.scientific_visual_skill import normalize_scientific_visual


def test_jsxgraph_conserve_une_figure_valide_et_ecarte_le_code():
    visual = normalize_scientific_visual({
        "engine": "jsxgraph",
        "title": "Mouvement sinusoïdal",
        "boundingBox": [-6, 4, 6, -4],
        "elements": [
            {"type": "function", "expression": "2*sin(x)", "color": "blue"},
            {"type": "function", "expression": "window.alert(x)", "color": "red"},
            {"type": "arrow", "points": [{"x": 0, "y": 0}, {"x": 2, "y": 1}], "label": "v"},
        ],
    })

    assert visual is not None
    assert visual["engine"] == "jsxgraph"
    assert [element["type"] for element in visual["elements"]] == ["function", "arrow"]
    assert visual["elements"][0]["expression"] == "2*sin(x)"


def test_jsxgraph_refuse_un_payload_sans_element_exploitable():
    assert normalize_scientific_visual({
        "engine": "jsxgraph",
        "elements": [{"type": "function", "expression": "fetch(secret)"}],
    }) is None


def test_jsxgraph_reecrit_les_notations_justes_mais_non_conformes():
    """`x**2` et `2x` sont des maths correctes : on les traduit, on ne les jette pas.

    Le navigateur n'accepte que `^` et la multiplication explicite. Refuser
    l'écriture du modèle faisait disparaître la figure en silence — souvent
    après que le tuteur l'ait annoncée à l'oral.
    """
    visual = normalize_scientific_visual({
        "engine": "jsxgraph",
        "elements": [
            {"type": "function", "expression": "x**2"},
            {"type": "function", "expression": "2x + 1"},
            {"type": "function", "expression": "(x+1)(x-1)"},
        ],
    })

    assert visual is not None
    assert [element["expression"] for element in visual["elements"]] == [
        "x^2", "2*x + 1", "(x+1)*(x-1)",
    ]


def test_jsxgraph_accepte_les_synonymes_de_figure():
    """Un « vecteur » est une flèche, et un cercle peut arriver en deux points."""
    visual = normalize_scientific_visual({
        "engine": "jsxgraph",
        "elements": [
            {"type": "vector", "points": [{"x": 0, "y": 0}, {"x": 2, "y": 2}], "label": "v"},
            {"type": "circle", "points": [{"x": 0, "y": 0}, {"x": 3, "y": 4}]},
        ],
    })

    assert visual is not None
    assert visual["elements"][0]["type"] == "arrow"
    assert visual["elements"][1] == {"type": "circle", "center": {"x": 0, "y": 0}, "radius": 5}


def test_cytoscape_supprime_les_aretes_orphelines_et_normalise_le_layout():
    visual = normalize_scientific_visual({
        "engine": "cytoscape",
        "layout": "inventé",
        "nodes": [
            {"id": "adn", "label": "ADN"},
            {"id": "arn", "label": "ARN messager", "color": "#22c55e"},
        ],
        "edges": [
            {"from": "adn", "to": "arn", "label": "Transcription"},
            {"from": "arn", "to": "proteine", "label": "Traduction"},
        ],
    })

    assert visual is not None
    assert visual["layout"] == "breadthfirst"
    assert visual["edges"] == [{"from": "adn", "to": "arn", "label": "Transcription"}]


def test_matter_borne_dimensions_physiques_et_references():
    visual = normalize_scientific_visual({
        "engine": "matter",
        "width": 5000,
        "height": 10,
        "gravity": {"x": 20, "y": -20},
        "bodies": [
            {"id": "balle", "shape": "circle", "x": 100, "y": 40, "radius": 999, "restitution": 4},
            {"id": "sol", "shape": "rectangle", "x": 300, "y": 300, "width": 500, "height": 20, "isStatic": True},
            {"id": "script", "shape": "javascript", "x": 0, "y": 0},
        ],
        "constraints": [
            {"fromBody": "balle", "toBody": "inconnu", "length": -1, "stiffness": 4},
        ],
    })

    assert visual is not None
    assert visual["width"] == 900
    assert visual["height"] == 220
    assert visual["gravity"] == {"x": 5, "y": -5}
    assert len(visual["bodies"]) == 2
    assert visual["bodies"][0]["radius"] == 160
    assert visual["bodies"][0]["restitution"] == 1
    assert visual["constraints"] == [{"length": 0, "stiffness": 1, "fromBody": "balle"}]


def test_moteur_non_autorise_est_refuse():
    assert normalize_scientific_visual({"engine": "javascript", "code": "alert(1)"}) is None
    assert normalize_scientific_visual("jsxgraph") is None


def test_cytoscape_garde_les_fleches_quand_les_ids_sont_en_francais():
    """Des ids accentués ne doivent pas coûter TOUTES les flèches du processus.

    Avant, le nœud survivait sous un nom de repli et l'arête, qui citait le
    nom d'origine, était jetée : l'élève recevait des cases sans lien, donc
    un processus faux — pire qu'aucun schéma.
    """
    visual = normalize_scientific_visual({
        "engine": "cytoscape",
        "nodes": [
            {"id": "acétyl_coa", "label": "Acétyl-CoA"},
            {"id": "cycle de Krebs", "label": "Cycle de Krebs"},
        ],
        "edges": [{"source": "acétyl_coa", "target": "cycle de Krebs", "label": "Entrée"}],
    })

    assert visual is not None
    assert [node["id"] for node in visual["nodes"]] == ["acetyl_coa", "cycle_de_Krebs"]
    assert visual["edges"] == [
        {"from": "acetyl_coa", "to": "cycle_de_Krebs", "label": "Entrée"}
    ]


def test_matter_conserve_l_inclinaison_d_un_plan():
    visual = normalize_scientific_visual({
        "engine": "matter",
        "bodies": [
            {"id": "plan", "shape": "rectangle", "x": 300, "y": 250, "width": 400,
             "height": 16, "angle": 0.52, "isStatic": True},
            {"id": "hors_limites", "shape": "rectangle", "x": 10, "y": 10, "angle": 99},
        ],
    })

    assert visual is not None
    assert visual["bodies"][0]["angle"] == 0.52
    assert visual["bodies"][1]["angle"] == round(3.141592653589793, 15)
