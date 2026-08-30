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

import pytest

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


def test_un_schema_valide_devient_une_figure_live():
    steps = SessionHandler._board_lines_to_live_steps([{
        "type": "schema",
        "schema_id": "svt_croquis_glycolyse",
        "content": "On suit le carbone du glucose.",
    }])

    assert steps == [{
        "action": "figure",
        "schema_id": "svt_croquis_glycolyse",
        "say": "On suit le carbone du glucose.",
    }]


@pytest.mark.parametrize("schema_id", [
    "phys_croquis_superposition",
    "chem_croquis_courbes_facteur",
    "math_croquis_tvi",
])
def test_les_croquis_complexes_des_trois_matieres_deviennent_des_figures_live(schema_id):
    steps = SessionHandler._board_lines_to_live_steps([{
        "type": "schema",
        "schema_id": schema_id,
        "content": "On construit le raisonnement couche par couche.",
    }])

    assert steps == [{
        "action": "figure",
        "schema_id": schema_id,
        "say": "On construit le raisonnement couche par couche.",
    }]


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
    handler._visuels_affiches = []
    asyncio.run(handler._send_board_or_live("La mitochondrie", lignes))
    return handler.websocket.envoyes[-1]


def test_le_tableau_envoye_porte_encore_la_figure():
    envoi = _envoi(_cours_avec_figure())

    assert envoi["type"] == "whiteboard_live"
    figures = [s for s in envoi["steps"] if s["action"] == "figure"]
    assert len(figures) == 1
    assert figures[0]["scientific"]["engine"] == "roughsvg"


def test_une_ressource_schema_s_ouvre_dans_le_live_board():
    handler = SessionHandler.__new__(SessionHandler)
    handler.websocket = FauxWebSocket()
    handler._remember_mode = lambda *_args, **_kwargs: None
    handler._visuels_affiches = []

    asyncio.run(handler._display_resource({
        "resource_type": "image",
        "title": "Croquis : bilan de la glycolyse",
        "description": "Suivre le glucose jusqu'aux deux pyruvates.",
        "file_path": None,
        "metadata": {"schema_id": "svt_croquis_glycolyse"},
    }))

    envoi = handler.websocket.envoyes[-1]
    assert envoi["type"] == "whiteboard_live"
    figure = next(step for step in envoi["steps"] if step["action"] == "figure")
    assert figure["schema_id"] == "svt_croquis_glycolyse"


def _handler_sans_media(demande: str, subject: str) -> SessionHandler:
    handler = SessionHandler(FauxWebSocket(), "eleve-test")
    handler.session_context = {
        "subject": subject,
        "chapter_title": "",
        "lesson_title": "",
        "objective": "",
    }
    handler.conversation_history = [{"role": "user", "content": demande}]
    handler.lesson_resources = []
    return handler


def test_le_mode_libre_charge_les_ressources_avec_le_client_serveur(monkeypatch):
    """La clé anon voit zéro ligne sous RLS ; le backend ne doit pas l'utiliser."""

    class Requete:
        def select(self, *_args, **_kwargs):
            return self

        def order(self, *_args, **_kwargs):
            return self

        def execute(self):
            return type("Resultat", (), {"data": [{"id": "ressource-visible"}]})()

    class BaseServeur:
        def table(self, nom):
            assert nom == "lesson_resources"
            return Requete()

    def client_public_interdit():
        raise AssertionError("la lecture serveur ne doit pas passer par la clé anon")

    monkeypatch.setattr(
        "app.websockets.session_handler.get_supabase_admin",
        lambda: BaseServeur(),
    )
    monkeypatch.setattr(
        "app.websockets.session_handler.get_supabase",
        client_public_interdit,
    )

    handler = SessionHandler.__new__(SessionHandler)
    handler.lesson_resources = []
    asyncio.run(handler._load_all_resources())

    assert handler.lesson_resources == [{"id": "ressource-visible"}]


def test_sans_media_db_l_onde_ouvre_la_scene_du_catalogue():
    handler = _handler_sans_media(
        "explique la propagation d'une onde le long d'une corde",
        "Physique",
    )

    ouverte = asyncio.run(handler._afficher_repli_du_catalogue("simulation"))

    assert ouverte is True
    envoi = next(m for m in handler.websocket.envoyes if m["type"] == "whiteboard_live")
    figure = next(step for step in envoi["steps"] if step["action"] == "figure")
    assert figure["scientific"]["presetId"] == "phys_ch1_propagation_onde"
    assert handler._last_resource_surface == "whiteboard"


def test_sans_scene_en_maths_on_descend_vers_un_schema_valide():
    handler = _handler_sans_media(
        "explique la dérivation et la tangente",
        "Mathématiques",
    )

    ouverte = asyncio.run(handler._afficher_repli_du_catalogue("simulation"))

    assert ouverte is True
    assert any(
        m.get("type") == "whiteboard_schema" and m.get("schema_id") == "math_derivation"
        for m in handler.websocket.envoyes
    )
    assert handler._last_resource_surface == "whiteboard"


def test_une_demande_3d_ouvre_le_modele_valide_sans_media_db():
    handler = _handler_sans_media(
        "montre-moi la mitochondrie en 3D pour que je puisse tourner autour",
        "SVT",
    )

    ouverte = asyncio.run(handler._afficher_repli_du_catalogue("simulation"))

    assert ouverte is True
    envoi = next(m for m in handler.websocket.envoyes if m["type"] == "whiteboard_live")
    figure = next(step for step in envoi["steps"] if step["action"] == "figure")
    assert figure["scientific"]["engine"] == "three"
    assert figure["scientific"]["model"] == "mitochondrion"
    assert handler._last_resource_surface == "whiteboard"


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


# ── Une ressource d'une autre matière est hors sujet ───────────────

_LABO_SVT = {
    "id": "svt-muscle",
    "lesson_id": "lecon-svt",
    "resource_type": "simulation",
    "title": "PhysioLab avancé — muscle et énergie",
    "description": "Contraction, calcium et ATP.",
    "concepts": ["muscle", "ATP"],
    "metadata": {"is_primary": True},
    "file_path": "/media/simulations/svt/ch1/labs/muscle-energie/index.html",
    "phase": "activation",
}

_SCENE_PHYSIQUE = {
    "id": "phys-chute",
    "lesson_id": "lecon-physique",
    "resource_type": "simulation",
    "title": "Chute libre d'une bille",
    "description": "Mouvement rectiligne uniformément accéléré.",
    "concepts": ["chute libre"],
    "metadata": {},
    "file_path": "/media/simulations/physics/ch2/chute-libre/index.html",
    "phase": "activation",
}


def _handler_bibliotheque(demande: str, ressources: list[dict]) -> SessionHandler:
    """Une question libre devant la bibliothèque entière, toutes matières."""
    handler = SessionHandler(FauxWebSocket(), "eleve-test")
    handler.session_context = {"subject": "", "chapter_title": "", "lesson_title": "", "objective": ""}
    handler.conversation_history = [{"role": "user", "content": demande}]
    handler.lesson_resources = ressources
    handler.lesson_subjects = {"lecon-svt": "SVT", "lecon-physique": "Physique"}
    handler.current_lesson_id = None
    return handler


def _ressource_ouverte(handler) -> str | None:
    """Le titre du média réellement affiché, sans toucher au transport."""
    affiche: list[dict] = []

    async def _display(resource):
        affiche.append(resource)
        return "media"

    async def _repli(preferred_resource_type=None):
        return False

    handler._display_resource = _display
    handler._afficher_repli_du_catalogue = _repli
    asyncio.run(handler._auto_suggest_resource(preferred_resource_type="simulation"))
    return affiche[-1]["title"] if affiche else None


def test_une_demande_de_physique_n_ouvre_pas_un_labo_de_svt():
    """Le 28 août 2026 : « la chute libre » ouvrait le PhysioLab du muscle.

    Les 142 médias de la bibliothèque étaient tous candidats, et le bonus de
    ressource principale pesait plus que les mots du titre. L'élève voyait un
    laboratoire de physiologie pendant qu'on lui parlait de mécanique.
    """
    handler = _handler_bibliotheque(
        "Explique-moi la chute libre d'une bille avec une scène animée",
        [_LABO_SVT, _SCENE_PHYSIQUE],
    )

    assert _ressource_ouverte(handler) == "Chute libre d'une bille"


def test_sans_media_de_la_bonne_matiere_on_prefere_le_repli():
    """Rien de la bonne matière : le catalogue du tableau, pas le hors-sujet."""
    handler = _handler_bibliotheque(
        "Fais-moi un cours complet sur les ondes mécaniques",
        [_LABO_SVT],
    )

    assert _ressource_ouverte(handler) is None


def test_dans_une_lecon_rattachee_le_filtre_ne_s_applique_pas():
    """Les médias d'une leçon sont déjà de la bonne matière.

    Certains n'ont ni fichier local ni leçon connue de la carte : les filtrer
    les ferait disparaître sans raison.
    """
    handler = _handler_bibliotheque(
        "Manipule le laboratoire du muscle et mesure la force produite",
        [_LABO_SVT],
    )
    handler.current_lesson_id = "lecon-svt"
    handler._load_lesson_resources = lambda _id: asyncio.sleep(0)

    # On isole le filtre de matière : sans ça le routeur ouvrirait une scène
    # contrôlable, qui passe légitimement avant le média de la bibliothèque.
    async def _pas_de_scene(_carte, _preferred=None):
        return False

    handler._afficher_scene_controlable = _pas_de_scene

    assert _ressource_ouverte(handler) == "PhysioLab avancé — muscle et énergie"


# ── La scène contrôlable passe avant la simulation HTML ────────────

def test_la_scene_controlable_passe_avant_le_media_de_la_bibliotheque():
    """Premier choix demandé le 29 août 2026 : la scène que le tuteur pilote.

    Une simulation HTML s'ouvre et se regarde ; une scène contrôlable avance
    au rythme de la parole. Quand les deux existent sur la notion, c'est la
    scène qui part au tableau.
    """
    handler = _handler_bibliotheque(
        "Explique-moi la propagation d'une onde le long d'une corde",
        [_SCENE_PHYSIQUE],
    )
    envoye: list[dict] = []

    async def _display(resource):
        envoye.append(resource)
        return "media"

    handler._display_resource = _display
    asyncio.run(handler._auto_suggest_resource(preferred_resource_type="simulation"))

    assert not envoye, "le média de la bibliothèque ne doit pas passer devant"
    tableau = [m for m in handler.websocket.envoyes if m["type"] in ("whiteboard_live", "whiteboard")]
    assert tableau, "une scène contrôlable devait partir au tableau"


def test_sans_scene_rapprochee_le_media_reprend_la_main():
    """Le premier choix ne doit pas devenir un passage obligé.

    Aucune scène ne se rapproche de la chute libre : la bibliothèque garde
    alors sa simulation, au lieu de laisser le tableau vide.
    """
    handler = _handler_bibliotheque(
        "Explique-moi la chute libre d'une bille",
        [_LABO_SVT, _SCENE_PHYSIQUE],
    )

    assert _ressource_ouverte(handler) == "Chute libre d'une bille"


# ── Il annonce, il écrit, PUIS il lance ────────────────────────────

def _ouvrir_simulation_de_bibliotheque() -> SessionHandler:
    handler = _handler_bibliotheque("Montre-moi la chute libre d'une bille", [_SCENE_PHYSIQUE])
    asyncio.run(handler._display_resource(_SCENE_PHYSIQUE))
    return handler


def test_la_simulation_est_annoncee_au_tableau_avant_de_s_ouvrir():
    """Une scène posée sans un mot n'est qu'une image de plus.

    Le tableau dit d'abord ce que l'élève va regarder ; la simulation attend
    la fin du script pour prendre la surface.
    """
    handler = _ouvrir_simulation_de_bibliotheque()
    types = [m["type"] for m in handler.websocket.envoyes]

    tableau = next(i for i, t in enumerate(types) if t in ("whiteboard_live", "whiteboard"))
    media = types.index("show_media")
    assert tableau < media, "le tableau doit être écrit avant l'ouverture"

    envoi = handler.websocket.envoyes[media]
    assert envoi["defer"] is True


def test_le_tableau_n_est_pas_efface_tant_que_la_simulation_attend():
    """L'ordre de masquage effaçait l'annonce à la seconde où elle était écrite."""
    handler = _ouvrir_simulation_de_bibliotheque()
    asyncio.run(handler._masquer_tableau_apres_media())

    assert "hide_whiteboard" not in [m["type"] for m in handler.websocket.envoyes]


# ── La scène du chapitre ne doit plus être invisible ───────────────

def test_la_scene_du_chapitre_passe_devant_la_photo():
    """Le 29 août 2026 : « fais-moi un cours sur les ondes » ouvrait une photo.

    La scène de propagation existait, mais elle ne marquait qu'un point sur
    deux exigés : le seuil la rendait invisible. C'est la MATIÈRE qui protège
    du hors-sujet maintenant, pas le seuil.
    """
    from app.services.visual_shortlist import carte_des_visuels

    contexte = "ondes mécaniques progressives physique reconnaître une onde"
    stricte = carte_des_visuels(contexte, "Fais-moi un cours complet sur les ondes", [])
    basse = carte_des_visuels(
        contexte, "Fais-moi un cours complet sur les ondes", [], lecon_rattachee=True
    )

    assert stricte["presets"] == []
    assert [p[0] for p in basse["presets"]][:1] == ["phys_ch1_propagation_onde"]


def test_une_scene_d_une_autre_matiere_est_ecartee():
    """Le seuil bas ne doit pas rouvrir la porte au hors-sujet."""
    handler = _handler_bibliotheque("Explique-moi la chute libre d'une bille", [])
    carte = {
        "presets": [("svt_ch1_cycle_atp", 1), ("phys_ch1_celerite_corde", 1)],
        "modeles_3d": [("mitochondrion", 1)],
    }

    filtree = handler._scenes_de_la_matiere(carte)

    assert [p[0] for p in filtree["presets"]] == ["phys_ch1_celerite_corde"]
    # Ce qu'on ne sait pas classer passe : `mitochondrion` ne porte aucun
    # préfixe de matière, et l'écarter sur une supposition coûterait plus
    # qu'il ne rapporte — son rapprochement exige déjà ses propres mots-clés.
    assert [m[0] for m in filtree["modeles_3d"]] == ["mitochondrion"]


def test_un_schema_deja_a_l_ecran_n_est_pas_renvoye():
    """Deux envois du même schéma effaçaient le tableau pour le redessiner."""
    handler = _handler_bibliotheque("Explique les ondes", [])
    handler._noter_visuel_affiche("phys_ondes_mecaniques")

    assert handler._deja_a_l_ecran("phys_ondes_mecaniques")
    assert not handler._deja_a_l_ecran("phys_ch1_types_ondes")


# ── Le tour de présentation ne porte que le plan ───────────────────

def test_aucun_support_ne_passe_pendant_la_presentation():
    """Le routeur retenait le serveur ; le bloc du modèle passait à côté.

    Le 29 août 2026, le premier tour sur les ondes annonçait le plan ET
    posait un schéma : l'élève voyait une figure avant de savoir ce qu'on
    allait en faire.
    """
    handler = _handler_bibliotheque("Fais-moi un cours sur les ondes", [])
    handler._tour_d_introduction = True

    assert handler._support_interdit_ce_tour("Schéma")
    assert handler._support_interdit_ce_tour("Média")

    handler._tour_d_introduction = False
    assert not handler._support_interdit_ce_tour("Schéma")


def test_la_presentation_n_ouvre_aucune_ressource():
    handler = _handler_bibliotheque("Fais-moi un cours sur les ondes", [_SCENE_PHYSIQUE])
    handler._tour_d_introduction = True

    assert _ressource_ouverte(handler) is None
