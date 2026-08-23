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

Aucun des quatre moteurs ne sait s'écrire craie par craie. Une figure impose
donc le tableau statique, où `MathBoard` la rend pour de bon.
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
    return {
        "type": "scientific",
        "content": "Ultrastructure de la mitochondrie",
        "scientific": {"engine": engine, "elements": []},
    }


def _cours_avec_figure() -> list[dict]:
    """Le tableau typique : on annonce, on explique, on montre."""
    return [
        {"type": "title", "content": "La mitochondrie"},
        {"type": "text", "content": "Sa membrane interne porte les crêtes."},
        _figure(),
    ]


# ── La porte statique / live ──────────────────────────────────────

def test_une_ligne_scientific_interdit_la_conversion_en_direct():
    assert SessionHandler._board_is_live_renderable(_cours_avec_figure()) is False


def test_les_quatre_moteurs_sont_concernes():
    """Le verrou porte sur le TYPE de ligne, donc sur tous les moteurs."""
    for engine in ("jsxgraph", "cytoscape", "matter", "roughsvg"):
        lignes = [{"type": "text", "content": "Observe."}, _figure(engine)]
        assert SessionHandler._board_is_live_renderable(lignes) is False, engine


def test_un_tableau_sans_figure_se_rejoue_toujours_en_direct():
    """Le cours ordinaire ne change pas : le live reste le défaut."""
    lignes = [
        {"type": "title", "content": "Le dipôle RC"},
        {"type": "text", "content": "La charge suit une loi exponentielle."},
    ]
    assert SessionHandler._board_is_live_renderable(lignes) is True


def test_la_conversion_en_direct_ne_sait_pas_rejouer_une_figure():
    """La preuve du danger : convertir PERD la figure, sans rien signaler."""
    steps = SessionHandler._board_lines_to_live_steps(_cours_avec_figure())

    ecrits = [s for s in steps if s["action"] == "write"]
    assert len(ecrits) == 2  # le titre et la phrase — la figure a disparu
    assert not any("scientific" in str(s) for s in steps)


# ── Ce que l'élève reçoit vraiment ────────────────────────────────

def _envoi(lignes: list[dict]) -> dict:
    handler = SessionHandler.__new__(SessionHandler)
    handler.websocket = FauxWebSocket()
    handler._remember_mode = lambda *_args, **_kwargs: None
    asyncio.run(handler._send_board_or_live("La mitochondrie", lignes))
    return handler.websocket.envoyes[-1]


def test_le_tableau_envoye_porte_encore_la_figure():
    envoi = _envoi(_cours_avec_figure())

    assert envoi["type"] == "whiteboard_board"
    types = [ligne["type"] for ligne in envoi["lines"]]
    assert "scientific" in types
    figure = next(l for l in envoi["lines"] if l["type"] == "scientific")
    assert figure["scientific"]["engine"] == "roughsvg"


def test_un_cours_sans_figure_part_toujours_en_direct():
    envoi = _envoi([
        {"type": "title", "content": "Le dipôle RC"},
        {"type": "text", "content": "La charge suit une loi exponentielle."},
    ])

    assert envoi["type"] == "whiteboard_live"
