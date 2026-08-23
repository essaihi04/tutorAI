"""Une figure demandée doit ARRIVER au tableau, pas seulement être produite.

Tout le travail de routage et de validation des moteurs (JSXGraph, Cytoscape,
Matter.js, Rough.js) s'arrêtait à une porte que personne ne regardait : le
choix entre le tableau STATIQUE et le script « prof en direct ».

Le tuteur qui répond « voici le schéma » écrit un tableau ordinaire — un
titre, deux phrases, et la ligne `scientific` qui porte la figure. Un titre et
deux phrases se rejouent très bien en direct : le tableau partait donc en
script live, et la conversion jetait en silence la seule ligne qui comptait.
L'élève entendait « regarde le schéma » devant un tableau qui n'en portait
aucun — et concluait, comme toujours, qu'il n'avait pas compris.

La figure n'est plus jetée : elle devient un pas `figure` du script, posé dans
la ZONE DE DESSIN du tableau en direct pendant que le texte s'écrit à gauche.
C'est le seul endroit où la figure et l'explication arrivent ensemble, au
rythme de la parole — le tableau statique, lui, affichait tout d'un bloc.
"""
import asyncio

from app.websockets.session_handler import SessionHandler


class FauxWebSocket:
    """On ne teste pas le transport : on regarde ce qui part vers l'élève."""

    def __init__(self):
        self.envoyes: list[dict] = []

    async def send_json(self, message: dict):
        self.envoyes.append(message)


def _figure(engine: str = "roughsvg") -> dict:
    """Une figure minimale mais VALIDE pour chaque moteur.

    Le normaliseur refuse une spécification vide : lui en donner une ferait
    passer les tests pour une raison qui n'a rien à voir avec ce qu'ils
    vérifient.
    """
    specs = {
        "roughsvg": {
            "engine": "roughsvg",
            "title": "Ultrastructure de la mitochondrie",
            "elements": [
                {"type": "ellipse", "x": 200, "y": 150, "radiusX": 150, "radiusY": 90, "color": "cyan"},
                {"type": "text", "x": 200, "y": 40, "text": "Membrane externe", "color": "cyan"},
            ],
        },
        "jsxgraph": {
            "engine": "jsxgraph",
            "title": "Bilan des forces",
            "elements": [
                {"type": "point", "points": [{"x": 0, "y": 0}], "label": "S"},
                {"type": "arrow", "points": [{"x": 0, "y": 0}, {"x": 0, "y": -3}], "label": "P"},
            ],
        },
        "cytoscape": {
            "engine": "cytoscape",
            "title": "Glycolyse",
            "nodes": [{"id": "a", "label": "Glucose"}, {"id": "b", "label": "Pyruvate"}],
            "edges": [{"from": "a", "to": "b", "label": "glycolyse"}],
        },
        "matter": {
            "engine": "matter",
            "title": "Chute libre",
            "scale": 100,
            "bodies": [
                {"id": "sol", "shape": "rectangle", "x": 300, "y": 380, "width": 600, "height": 20,
                 "isStatic": True, "label": "Sol"},
                {"id": "bille", "shape": "circle", "x": 300, "y": 60, "radius": 18, "label": "Bille"},
            ],
            "measures": [{"quantity": "time", "label": "t", "unit": "s", "decimals": 2}],
        },
    }
    return {"type": "scientific", "content": "Regarde la figure", "scientific": specs[engine]}


def _cours_avec_figure(engine: str = "roughsvg") -> list[dict]:
    """Le tableau typique : on annonce, on explique, on montre."""
    return [
        {"type": "title", "content": "La mitochondrie"},
        {"type": "text", "content": "Sa membrane interne porte les crêtes."},
        _figure(engine),
    ]


# ── La figure survit à la conversion en direct ────────────────────

def test_la_figure_devient_un_pas_du_script():
    steps = SessionHandler._board_lines_to_live_steps(_cours_avec_figure())

    actions = [s["action"] for s in steps]
    assert "figure" in actions, actions
    figure = next(s for s in steps if s["action"] == "figure")
    assert figure["scientific"]["engine"] == "roughsvg"
    # La légende de la ligne devient ce que le professeur DIT en la montrant.
    assert figure["say"] == "Regarde la figure"


def test_les_quatre_moteurs_traversent():
    for engine in ("jsxgraph", "cytoscape", "matter", "roughsvg"):
        steps = SessionHandler._board_lines_to_live_steps(_cours_avec_figure(engine))
        figures = [s for s in steps if s["action"] == "figure"]
        assert len(figures) == 1, engine
        assert figures[0]["scientific"]["engine"] == engine


def test_le_texte_continue_de_s_ecrire_a_cote():
    """La figure ne remplace pas l'explication : les deux zones vivent."""
    steps = SessionHandler._board_lines_to_live_steps(_cours_avec_figure())

    ecrits = [s for s in steps if s["action"] == "write"]
    assert [e["line"]["content"] for e in ecrits] == [
        "La mitochondrie",
        "Sa membrane interne porte les crêtes.",
    ]


def test_une_figure_seule_vaut_un_tableau():
    """« Dessine-moi la mitochondrie » n'a pas d'autre texte que sa légende.

    Exiger une ligne écrite renverrait ce cas — le plus fréquent — au tableau
    statique, qui affiche la figure d'un bloc et sans un mot.
    """
    steps = SessionHandler._board_lines_to_live_steps([_figure()])

    assert len(steps) == 1
    assert steps[0]["action"] == "figure"


def test_une_figure_invalide_ne_casse_pas_le_tableau():
    lignes = [
        {"type": "title", "content": "La mitochondrie"},
        {"type": "scientific", "content": "Figure", "scientific": {"engine": "inconnu"}},
    ]
    steps = SessionHandler._board_lines_to_live_steps(lignes)

    assert [s["action"] for s in steps] == ["write", "pause"]


# ── Ce que l'élève reçoit vraiment ────────────────────────────────

def _envoi(lignes: list[dict]) -> dict:
    handler = SessionHandler.__new__(SessionHandler)
    handler.websocket = FauxWebSocket()
    handler._remember_mode = lambda *_args, **_kwargs: None
    asyncio.run(handler._send_board_or_live("La mitochondrie", lignes))
    return handler.websocket.envoyes[-1]


def test_le_tableau_envoye_porte_encore_la_figure():
    envoi = _envoi(_cours_avec_figure())

    assert envoi["type"] == "whiteboard_live"
    figures = [s for s in envoi["steps"] if s["action"] == "figure"]
    assert len(figures) == 1
    assert figures[0]["scientific"]["engine"] == "roughsvg"


def test_un_echiquier_voyage_dans_le_script_sans_se_perdre():
    """Un tableau à double entrée ne s'écrit pas craie par craie — il se POSE.

    Il retenait pour cela le tableau statique tout entier : le cours qui
    l'accompagnait s'affichait d'un bloc, sans un mot. Il part désormais dans
    le script en direct comme un bloc, à son tour dans le déroulé, pendant que
    le reste s'écrit. L'alignement des gamètes, seule raison d'être d'un
    échiquier, est intact — c'est le rendu commun qui le pose.
    """
    envoi = _envoi([
        {"type": "title", "content": "Monohybridisme"},
        {"type": "table", "headers": ["", "A", "a"], "rows": [["A", "AA", "Aa"]]},
    ])

    assert envoi["type"] == "whiteboard_live"
    bloc = next(s for s in envoi["steps"] if s["action"] == "bloc")
    assert bloc["line"]["type"] == "table"
    assert bloc["line"]["rows"] == [["A", "AA", "Aa"]]


def test_le_tuteur_peut_poser_un_echiquier_dans_son_script():
    handler = SessionHandler.__new__(SessionHandler)
    _titre, steps = handler._normalize_live_steps({
        "steps": [
            {"action": "write", "line": {"type": "title", "content": "Monohybridisme"}},
            {"action": "bloc", "line": {"type": "table", "headers": ["", "A"], "rows": [["a", "Aa"]]}},
        ],
    })

    bloc = next(s for s in steps if s["action"] == "bloc")
    assert bloc["line"]["headers"] == ["", "A"]


def test_un_bloc_de_type_invente_ne_part_pas():
    """Une ligne dont personne ne sait faire le rendu disparaîtrait à l'écran."""
    handler = SessionHandler.__new__(SessionHandler)
    _titre, steps = handler._normalize_live_steps({
        "steps": [
            {"action": "write", "line": {"type": "text", "content": "Observe."}},
            {"action": "bloc", "line": {"type": "hologramme", "content": "?"}},
        ],
    })

    assert not any(s["action"] == "bloc" for s in steps)


# ── Le tuteur peut émettre le pas lui-même ────────────────────────

def test_le_tuteur_peut_poser_une_figure_dans_son_script():
    handler = SessionHandler.__new__(SessionHandler)
    titre, steps = handler._normalize_live_steps({
        "title": "La mitochondrie",
        "steps": [
            {"action": "write", "line": {"type": "title", "content": "La mitochondrie"}},
            {"action": "figure", "scientific": _figure()["scientific"], "say": "شوف الرسم"},
        ],
    })

    assert titre == "La mitochondrie"
    figure = next(s for s in steps if s["action"] == "figure")
    assert figure["scientific"]["engine"] == "roughsvg"
    # La darija est chez elle dans ce qui est PRONONCÉ ; seul l'écrit au
    # tableau reste en français, l'élève le recopiant sur sa copie.
    assert figure["say"] == "شوف الرسم"


def test_une_figure_refusee_par_la_porte_de_qualite_ne_part_pas():
    """Une figure vide traverserait le normaliseur mais n'apprend rien."""
    handler = SessionHandler.__new__(SessionHandler)
    titre, steps = handler._normalize_live_steps({
        "steps": [
            {"action": "write", "line": {"type": "text", "content": "Observe."}},
            {"action": "figure", "scientific": {"engine": "cytoscape", "nodes": [], "edges": []}},
        ],
    })

    assert titre is not None
    assert not any(s["action"] == "figure" for s in steps)


# ── Les cinq formes de SVT ────────────────────────────────────────

def test_les_formes_biologiques_traversent_le_script():
    """Elles vivaient sur un canvas à part, refusé par le script en direct.

    `drawable_types` ne connaissait que les primitives : une mitochondrie
    posée dans un `show_live` était filtrée en silence, et l'élève voyait un
    croquis amputé de la seule chose qu'on lui demandait de reconnaître.
    """
    handler = SessionHandler.__new__(SessionHandler)
    _titre, steps = handler._normalize_live_steps({
        "steps": [
            {"action": "write", "line": {"type": "title", "content": "La cellule"}},
            {"action": "draw", "elements": [
                {"type": "cell", "x": 130, "y": 130, "radius": 95, "label": "Cellule"},
                {"type": "nucleus", "x": 110, "y": 120, "radius": 38, "label": "Noyau"},
                {"type": "mitochondria", "x": 280, "y": 60, "width": 170, "height": 80, "label": "Mitochondrie"},
                {"type": "dna", "x": 300, "y": 200, "width": 55, "height": 130, "label": "ADN"},
                {"type": "membrane", "x": 60, "y": 320, "width": 180, "height": 34, "label": "Bicouche"},
            ]},
        ],
    })

    dessin = next(s for s in steps if s["action"] == "draw")
    assert [e["type"] for e in dessin["elements"]] == [
        "cell", "nucleus", "mitochondria", "dna", "membrane",
    ]


def test_une_forme_inventee_reste_refusee():
    """Le filtre garde son rôle : un type inconnu n'a aucun rendu."""
    handler = SessionHandler.__new__(SessionHandler)
    _titre, steps = handler._normalize_live_steps({
        "steps": [
            {"action": "write", "line": {"type": "text", "content": "Observe."}},
            {"action": "draw", "elements": [
                {"type": "chloroplaste", "x": 10, "y": 10},
                {"type": "circle", "x": 50, "y": 50, "radius": 20},
            ]},
        ],
    })

    dessin = next(s for s in steps if s["action"] == "draw")
    assert [e["type"] for e in dessin["elements"]] == ["circle"]


# ── Le tableau ne s'efface pas dans le vide ───────────────────────

class _HandlerRessource:
    """Un handler réduit à la question posée : qui efface, et quand."""

    def __init__(self, ressource_trouvee: bool):
        self.websocket = FauxWebSocket()
        self._trouve = ressource_trouvee
        self._defaut_accord = ""

    async def _auto_suggest_resource(self, preferred_resource_type=None):
        if self._trouve:
            await self.websocket.send_json({"type": "show_media", "url": "/media/sim.html"})
        return self._trouve

    _noter_simulation_introuvable = SessionHandler._noter_simulation_introuvable


def _ouvrir_simulation(handler) -> list[str]:
    """Rejoue la branche `simulation/open` de `_execute_ai_commands`."""
    async def scenario():
        ouverte = await handler._auto_suggest_resource(preferred_resource_type="simulation")
        if ouverte:
            await handler.websocket.send_json({"type": "hide_whiteboard"})
        else:
            handler._noter_simulation_introuvable()
    asyncio.run(scenario())
    return [m["type"] for m in handler.websocket.envoyes]


def test_sans_simulation_disponible_le_tableau_reste():
    """La séance du 24 août : « peux-tu créer une simulation ? »

    Le tuteur promet, demande au système d'ouvrir, le tableau s'efface — et
    rien n'arrive. L'élève regarde un panneau vide en l'entendant lui dire de
    regarder. Le tableau ne s'efface plus tant que rien ne le remplace.
    """
    handler = _HandlerRessource(ressource_trouvee=False)

    assert "hide_whiteboard" not in _ouvrir_simulation(handler)


def test_le_tuteur_apprend_qu_il_doit_la_dessiner_lui_meme():
    """Il ne le savait pas : le serveur ne répondait rien quand il ne trouvait pas.

    Il repromettait donc au tour suivant — trois fois le même paragraphe.
    """
    handler = _HandlerRessource(ressource_trouvee=False)
    _ouvrir_simulation(handler)

    rappel = handler._defaut_accord
    assert "matter" in rappel
    assert "OUVRIR_SIMULATION" in rappel
    assert "measures" in rappel


def test_avec_une_simulation_disponible_le_tableau_cede_la_place():
    """Le comportement d'origine ne change pas quand il y a bien quelque chose."""
    handler = _HandlerRessource(ressource_trouvee=True)

    assert _ouvrir_simulation(handler) == ["show_media", "hide_whiteboard"]
    assert handler._defaut_accord == ""
