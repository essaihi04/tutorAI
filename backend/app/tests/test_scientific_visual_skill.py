"""Contrat de sécurité des visuels scientifiques produits par le LLM."""

from app.services.scientific_visual_skill import normalize_scientific_visual, scientific_visual_quality


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


def test_roughsvg_ne_laisse_passer_que_des_primitives_declaratives():
    visual = normalize_scientific_visual({
        "engine": "roughsvg",
        "title": "Cellule",
        "description": "Organisation spatiale d'une cellule.",
        "width": 800,
        "height": 440,
        "elements": [
            {"type": "ellipse", "cx": 400, "cy": 220, "rx": 250, "ry": 150, "fill": "#22c55e"},
            {"type": "text", "x": 400, "y": 220, "text": "Noyau", "onclick": "alert(1)"},
            {"type": "path", "d": "M0 0", "script": "fetch('/secret')"},
            {"type": "image", "url": "https://example.com/track.png"},
        ],
    })

    assert visual is not None
    assert visual["engine"] == "roughsvg"
    assert [element["type"] for element in visual["elements"]] == ["ellipse", "text"]
    assert "onclick" not in visual["elements"][1]
    assert "url" not in str(visual)


def test_roughsvg_borne_le_cadre_et_les_coordonnees():
    visual = normalize_scientific_visual({
        "engine": "svg",
        "width": 5000,
        "height": 10,
        "elements": [
            {"type": "rect", "x": -50, "y": 50, "width": 5000, "height": 5000},
            {"type": "arrow", "points": [{"x": -3, "y": 20}, {"x": 4000, "y": 9000}]},
        ],
    })

    assert visual is not None
    assert visual["engine"] == "roughsvg"
    assert visual["width"] == 1000
    assert visual["height"] == 220
    assert visual["elements"][0]["x"] == 0
    assert visual["elements"][1]["points"][-1] == {"x": 1000, "y": 220}


def test_controle_qualite_signale_une_figure_non_legendee():
    report = scientific_visual_quality({
        "engine": "roughsvg",
        "elements": [
            {"type": "circle", "x": 100, "y": 100, "radius": 30},
            {"type": "circle", "x": 220, "y": 100, "radius": 30},
        ],
    })

    assert report["acceptable"] is False
    assert report["score"] < 60
    assert any("légendes" in issue for issue in report["issues"])


def test_controle_qualite_accepte_un_schema_roughsvg_complet():
    report = scientific_visual_quality({
        "engine": "roughsvg",
        "title": "Cycle ATP–ADP",
        "description": "L'hydrolyse libère de l'énergie et la phosphorylation renouvelle l'ATP.",
        "width": 800,
        "height": 440,
        "elements": [
            {"type": "rect", "x": 80, "y": 150, "width": 180, "height": 90, "color": "blue"},
            {"type": "rect", "x": 540, "y": 150, "width": 180, "height": 90, "color": "green"},
            {"type": "arrow", "points": [{"x": 270, "y": 175}, {"x": 525, "y": 175}]},
            {"type": "arrow", "points": [{"x": 525, "y": 230}, {"x": 270, "y": 230}]},
            {"type": "text", "x": 170, "y": 205, "text": "ATP"},
            {"type": "text", "x": 630, "y": 205, "text": "ADP + Pi"},
        ],
    })

    assert report["acceptable"] is True
    assert report["score"] >= 80


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


def test_jsxgraph_dessine_un_bilan_des_forces_complet():
    """Le plan incliné du BAC : le triangle, les vecteurs ET l'angle.

    Avant, `polygon` et `angle` n'existaient pas au contrat. Le validateur les
    jetait en silence : le tuteur disait « le poids fait un angle alpha avec la
    normale » devant deux flèches flottant sur un plan qui n'était pas dessiné.
    """
    visual = normalize_scientific_visual({
        "engine": "jsxgraph",
        "title": "Plan incliné",
        "axis": False,
        "elements": [
            {"type": "polygon",
             "points": [{"x": 0, "y": 0}, {"x": 8, "y": 0}, {"x": 8, "y": 4}],
             "label": "Plan"},
            {"type": "arrow", "points": [{"x": 5, "y": 2.5}, {"x": 5, "y": 0.5}], "label": "P"},
            {"type": "angle",
             "points": [{"x": 8, "y": 0}, {"x": 0, "y": 0}, {"x": 8, "y": 4}],
             "label": "alpha"},
        ],
    })

    assert visual is not None
    assert [element["type"] for element in visual["elements"]] == ["polygon", "arrow", "angle"]
    assert len(visual["elements"][0]["points"]) == 3
    assert visual["elements"][0]["filled"] is True
    assert len(visual["elements"][2]["points"]) == 3


def test_jsxgraph_borne_une_courbe_qui_n_a_de_sens_que_sur_un_intervalle():
    """Une trajectoire s'arrête au sol ; sans bornes elle remonte et ment."""
    visual = normalize_scientific_visual({
        "engine": "jsxgraph",
        "elements": [
            {"type": "function", "expression": "x - 0.1*x^2", "from": 0, "to": 10},
            {"type": "function", "expression": "sin(x)", "domain": [-3, 3]},
            {"type": "function", "expression": "x^2", "from": 5, "to": 1},
        ],
    })

    assert visual is not None
    assert visual["elements"][0]["domain"] == [0, 10]
    assert visual["elements"][1]["domain"] == [-3, 3]
    # Bornes inversées : on préfère la courbe entière au tracé vide.
    assert "domain" not in visual["elements"][2]


def test_jsxgraph_trace_une_aire_sous_la_courbe():
    """L'intégrale se DESSINE hachurée : c'est sa définition au tableau."""
    visual = normalize_scientific_visual({
        "engine": "jsxgraph",
        "elements": [
            {"type": "integrale", "expression": "x^2/4+1", "from": 1, "to": 4, "label": "Aire"},
            {"type": "area", "expression": "x^2", "label": "sans bornes"},
        ],
    })

    assert visual is not None
    assert [element["type"] for element in visual["elements"]] == ["area"]
    assert visual["elements"][0]["domain"] == [1, 4]


def test_jsxgraph_ecrit_sur_la_figure_et_nomme_les_axes():
    """Une annotation et deux axes unités : ce que le BAC exige d'un graphe."""
    visual = normalize_scientific_visual({
        "engine": "jsxgraph",
        "xLabel": "t (s)",
        "yLabel": "U (V)",
        "elements": [
            {"type": "text", "points": [{"x": 2, "y": 3}], "label": "Régime permanent"},
            {"type": "texte", "points": [{"x": 1, "y": 1}]},
        ],
    })

    assert visual is not None
    assert visual["xLabel"] == "t (s)"
    assert visual["yLabel"] == "U (V)"
    # Un texte sans légende n'est qu'une croix muette : il ne passe pas.
    assert [element["type"] for element in visual["elements"]] == ["text"]
    assert visual["elements"][0]["label"] == "Régime permanent"


def test_un_element_jete_est_ecrit_quelque_part(monkeypatch):
    """L'amputation silencieuse est le vrai défaut : le tuteur l'a annoncé.

    L'élève entend « regarde le vecteur champ » et cherche sur l'écran un
    élément que le validateur a jeté sans un mot. On ne peut pas tout
    dessiner, mais on doit savoir ce qui a manqué.
    """
    from app.services import scientific_visual_skill, visual_gaps

    notes: list[tuple] = []
    monkeypatch.setattr(
        scientific_visual_skill, "noter_element_refuse",
        lambda moteur, types, titre="": notes.append((moteur, sorted(set(types)), titre)),
    )
    visual = normalize_scientific_visual({
        "engine": "jsxgraph",
        "title": "Champ électrostatique",
        "elements": [
            {"type": "point", "points": [{"x": 0, "y": 0}], "label": "O"},
            {"type": "champ_vectoriel", "points": [{"x": 1, "y": 1}]},
        ],
    })

    assert visual is not None
    assert [element["type"] for element in visual["elements"]] == ["point"]
    assert notes == [("jsxgraph", ["champ_vectoriel"], "Champ électrostatique")]
    assert callable(visual_gaps.noter_element_refuse)
