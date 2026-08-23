"""Routing prompt and validation for LLM-generated scientific visuals.

The application LLM cannot load Codex ``SKILL.md`` files at runtime.  This
module mirrors the small, machine-facing part of the project skill and keeps
untrusted visual JSON declarative before it reaches the browser renderers.
"""

from __future__ import annotations

import ast
import math
import re
import unicodedata
from typing import Any

from app.services.visual_gaps import noter_element_refuse


SCIENTIFIC_VISUAL_PROMPT = r"""
[SKILL VISUELS SCIENTIFIQUES — CHOIX DU BON MOTEUR]
N'utilise PAS un moteur spécialisé pour décorer. Choisis le visuel qui sert
directement l'objectif du cours, dans cet ordre :
1. Schéma BAC déjà validé → action `show_schema` (priorité maximale).
2. Tableau, courbe simple, carte mentale ou petit diagramme → types ordinaires
   `table`, `graph`, `mindmap`, `diagram`.
3. Figure scientifique interactive qui exige un moteur spécialisé → une ligne
   `scientific` dans `show_board`.
4. Processus déjà disponible comme ressource de cours → ouvre la simulation
   existante. Ne fabrique une mini-simulation Matter que pour un mécanisme 2D
   simple qui change dans le temps et qu'aucune ressource ne couvre.

MOTEURS AUTORISÉS dans `line.scientific` :
- `jsxgraph` : géométrie, forces, vecteurs, optique, fonctions et courbes.
- `cytoscape` : chaînes, réseaux et processus SVT avec nœuds et flèches.
- `matter` : mécanique 2D simple (chute, choc, pendule, plan, projectile).
- `roughsvg` : structures spatiales, cellules, chromosomes, appareils de
  chimie, circuits et coupes. C'est le moteur de schéma généraliste ; il ne
  reçoit que des primitives SVG déclaratives, jamais du SVG ou du code brut.

Format JSXGraph :
{"type":"scientific","content":"Figure","scientific":{"engine":"jsxgraph","title":"Bilan des forces","boundingBox":[-5,5,5,-5],"axis":true,"grid":false,"elements":[{"type":"point","points":[{"x":0,"y":0}],"label":"S","color":"cyan"},{"type":"arrow","points":[{"x":0,"y":0},{"x":0,"y":-3}],"label":"Poids","color":"red"}]}}
Types d'éléments : `point`, `segment`, `line`, `arrow`, `circle`, `function`,
`text`, `polygon`, `angle`, `area`.
Un cercle se donne par `"center":{"x":..,"y":..}` et `"radius":..`.
`text` : une annotation libre — `"points":[{"x":..,"y":..}]` pour l'ancrage et
  `"label"` pour le texte. Sans `label`, rien ne s'affiche.
`polygon` : 3 à 12 sommets dans `points` (triangle d'un plan incliné, cuve,
  coupe). `"filled":false` pour n'en garder que le contour.
`angle` : TROIS points dans l'ordre scolaire — première branche, SOMMET,
  seconde branche. C'est ce qui matérialise un angle de tir, un angle
  d'incidence ou un argument.
`area` : l'aire sous une courbe entre deux bornes — `expression` + `"from"` et
  `"to"`. C'est le tracé attendu pour une intégrale ou un travail.
Une fonction utilise `expression` avec x, nombres et seulement sin, cos, tan,
sqrt, abs, exp, ln, log, pi, e. Écris toujours la multiplication avec `*` :
`2*x`, jamais `2x`. Ajoute `"from"` et `"to"` (ou `"domain":[a,b]`) dès que la
courbe n'a de sens que sur un intervalle : une trajectoire s'arrête au sol,
une concentration ne commence pas avant t=0.

AXES : donne `"xLabel"` et `"yLabel"` avec l'unité entre parenthèses —
`"xLabel":"t (s)"`, `"yLabel":"U (V)"`. Un axe anonyme est une figure fausse
au BAC.

Format Cytoscape :
{"type":"scientific","content":"Processus","scientific":{"engine":"cytoscape","title":"Respiration cellulaire","layout":"breadthfirst","nodes":[{"id":"glucose","label":"Glucose"},{"id":"pyruvate","label":"Pyruvate"}],"edges":[{"from":"glucose","to":"pyruvate","label":"Glycolyse"}]}}
Layouts : `breadthfirst`, `circle`, `grid`, `cose`.

Format Matter :
{"type":"scientific","content":"Manipulation","scientific":{"engine":"matter","title":"Chute verticale","width":600,"height":320,"gravity":{"x":0,"y":1},"autoplay":true,"bodies":[{"id":"sol","shape":"rectangle","x":300,"y":305,"width":580,"height":20,"isStatic":true,"label":"Sol"},{"id":"balle","shape":"circle","x":300,"y":60,"radius":22,"label":"Balle","color":"orange","restitution":0.5}]}}

Un corps Matter accepte `"angle"` en RADIANS : c'est ce qui incline un plan
(`"angle":0.52` pour 30°). Sans lui, le plan est horizontal.

Format RoughSVG :
{"type":"scientific","content":"Schéma","scientific":{"engine":"roughsvg","title":"Électrolyse","description":"Sens du courant et réactions aux électrodes.","width":800,"height":440,"elements":[{"type":"rect","x":250,"y":110,"width":300,"height":230,"color":"blue"},{"type":"line","points":[{"x":330,"y":90},{"x":330,"y":300}],"color":"gray"},{"type":"text","x":330,"y":80,"text":"Anode (+)","color":"red"},{"type":"arrow","points":[{"x":370,"y":180},{"x":470,"y":180}],"color":"cyan"}],"legend":[{"color":"red","label":"Oxydation"},{"color":"blue","label":"Réduction"}]}}
Primitives : `line`, `arrow`, `rect`, `circle`, `ellipse`, `polygon`,
`polyline`, `text`. Place les légendes hors des objets, utilise des coordonnées
dans le cadre et ajoute une `description` accessible. N'émets ni `path`, ni
HTML, ni URL, ni attribut d'événement.

RÈGLES DE QUALITÉ :
- Toutes les légendes sont courtes et en français.
- Représente uniquement les objets utiles ; pas de surcharge ni chevauchement.
- Respecte les conventions BAC : symboles, sens des flèches, unités et noms.
- Pour RoughSVG : au moins un titre, deux objets scientifiques et leurs
  légendes ; évite tout chevauchement entre textes.
- Une simulation doit faire observer une variable ou tester une hypothèse ;
  sinon un schéma statique suffit.
- N'invente jamais un moteur, un type d'élément ou du code JavaScript.
""".strip()


_COLORS = {
    "red", "blue", "green", "orange", "purple", "cyan", "yellow", "white",
    "black", "gray", "grey",
}
_HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9_.-]{1,48}$")
_EXPRESSION_CHARS = re.compile(r"^[0-9A-Za-z+\-*/^().,\s]+$")
_EXPRESSION_NAMES = {
    "x", "sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "abs",
    "exp", "ln", "log", "floor", "ceil", "round", "pi", "e",
}


def _text(value: Any, limit: int = 80) -> str:
    if not isinstance(value, str):
        return ""
    return re.sub(r"\s+", " ", value).strip()[:limit]


def _number(value: Any, default: float, minimum: float, maximum: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return max(minimum, min(maximum, number))


def _color(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip().lower()
    return cleaned if cleaned in _COLORS or _HEX_COLOR.fullmatch(cleaned) else None


def _identifier(value: Any, fallback: str) -> str:
    if isinstance(value, str) and _IDENTIFIER.fullmatch(value.strip()):
        return value.strip()
    return fallback


def _slug(value: Any) -> str:
    """Un identifiant de nœud écrit en français, ramené au jeu autorisé.

    Un modèle qui parle français nomme ses nœuds `acétyl_coa` ou
    `ADN nucléaire` : accents et espaces, donc identifiant refusé. Le nœud
    survivait sous un nom de repli (`n0`) mais les flèches, elles, citaient
    toujours l'ancien nom et disparaissaient TOUTES — l'élève recevait un
    processus sans une seule flèche, c'est-à-dire un schéma faux.

    On translittère au lieu de renommer, et la même fonction sert aux nœuds
    et aux extrémités des flèches : les deux retombent sur le même mot.
    """
    if not isinstance(value, str):
        return ""
    folded = unicodedata.normalize("NFKD", value.strip())
    folded = "".join(char for char in folded if not unicodedata.combining(char))
    folded = re.sub(r"[^A-Za-z0-9_.-]+", "_", folded).strip("_")
    return folded[:48]


def _point(value: Any, *, minimum: float = -10000, maximum: float = 10000) -> dict[str, float] | None:
    if not isinstance(value, dict):
        return None
    return {
        "x": _number(value.get("x"), 0, minimum, maximum),
        "y": _number(value.get("y"), 0, minimum, maximum),
    }


def _intervalle(domaine: Any, debut: Any = None, fin: Any = None) -> list[float] | None:
    """Les bornes d'une courbe, écrites `domain:[a,b]` ou `from`/`to`.

    Les deux formes viennent du modèle selon qu'il pense « intervalle » ou
    « de … à … ». Une borne seule ne veut rien dire : on rend `None` plutôt
    que d'inventer l'autre.
    """
    if isinstance(domaine, (list, tuple)) and len(domaine) == 2:
        debut, fin = domaine[0], domaine[1]
    if debut is None or fin is None:
        return None
    try:
        a, b = float(debut), float(fin)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(a) or not math.isfinite(b) or a >= b:
        return None
    return [max(-10000.0, a), min(10000.0, b)]


_IMPLICIT_NUMBER_NAME = re.compile(r"(\d)\s*(?=[A-Za-z(])")
_IMPLICIT_CLOSING = re.compile(r"\)\s*(?=[A-Za-z0-9(])")


def _rewrite_expression(expression: str) -> str:
    """Les deux façons dont un modèle écrit juste, sans écrire notre syntaxe.

    Le navigateur ne connaît qu'une notation : `^` pour la puissance et un `*`
    explicite. Un modèle écrit pourtant `x**2` (réflexe Python) et `2x + 1`
    (réflexe de copie manuscrite) — deux formes MATHÉMATIQUEMENT justes que
    l'ancien filtre refusait en bloc. La figure disparaissait alors sans un
    mot, souvent après que le tuteur l'ait annoncée à l'oral.

    On réécrit donc au lieu de refuser. La réécriture est purement
    syntaxique : elle n'ajoute ni nom ni appel, et le contrôle AST juste
    après reste seul juge de ce qui est autorisé.
    """
    expression = expression.replace("**", "^")
    expression = _IMPLICIT_NUMBER_NAME.sub(r"\1*", expression)  # 2x → 2*x, 3(x+1) → 3*(x+1)
    return _IMPLICIT_CLOSING.sub(")*", expression)  # (x+1)(x-1) → (x+1)*(x-1)


def _expression(value: Any) -> str | None:
    expression = _rewrite_expression(_text(value, 100))
    if not expression or not _EXPRESSION_CHARS.fullmatch(expression):
        return None
    names = re.findall(r"[A-Za-z]+", expression)
    if any(name.lower() not in _EXPRESSION_NAMES for name in names):
        return None
    try:
        tree = ast.parse(expression.replace("^", "**"), mode="eval")
    except SyntaxError:
        return None

    binary_operators = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)
    unary_operators = (ast.UAdd, ast.USub)
    functions = _EXPRESSION_NAMES - {"x", "pi", "e"}

    def is_safe(node: ast.AST) -> bool:
        if isinstance(node, ast.Expression):
            return is_safe(node.body)
        if isinstance(node, ast.Constant):
            return type(node.value) in {int, float}
        if isinstance(node, ast.Name):
            return node.id.lower() in {"x", "pi", "e"}
        if isinstance(node, ast.BinOp):
            return (
                isinstance(node.op, binary_operators)
                and is_safe(node.left)
                and is_safe(node.right)
            )
        if isinstance(node, ast.UnaryOp):
            return isinstance(node.op, unary_operators) and is_safe(node.operand)
        if isinstance(node, ast.Call):
            return (
                isinstance(node.func, ast.Name)
                and node.func.id.lower() in functions
                and len(node.args) == 1
                and not node.keywords
                and is_safe(node.args[0])
            )
        return False

    if sum(1 for _ in ast.walk(tree)) > 80 or not is_safe(tree):
        return None
    return expression


def _normalize_jsxgraph(value: dict[str, Any]) -> dict[str, Any] | None:
    raw_elements = value.get("elements")
    if not isinstance(raw_elements, list):
        return None

    elements: list[dict[str, Any]] = []
    allowed = {
        "point", "segment", "line", "arrow", "circle", "function",
        "text", "polygon", "angle", "area",
    }
    # Les mots que le modèle emploie pour une même figure. Un vecteur EST une
    # flèche : refuser le mot faisait disparaître tout un bilan des forces.
    synonymes = {
        "vector": "arrow", "vecteur": "arrow", "fleche": "arrow", "flèche": "arrow",
        "segment_droite": "segment", "droite": "line", "cercle": "circle",
        "courbe": "function", "graph": "function", "curve": "function", "fonction": "function",
        "texte": "text", "label": "text", "annotation": "text", "legende": "text",
        "légende": "text", "note": "text",
        "polygone": "polygon", "triangle": "polygon", "rectangle": "polygon",
        "quadrilatere": "polygon", "quadrilatère": "polygon", "surface": "polygon",
        "angle_marque": "angle", "arc": "angle", "secteur": "angle",
        "aire": "area", "integral": "area", "integrale": "area", "intégrale": "area",
        "hachures": "area",
    }
    refuses: list[str] = []
    for index, raw in enumerate(raw_elements[:40]):
        if not isinstance(raw, dict):
            continue
        element_type = str(raw.get("type", "")).strip().lower()
        element_type = synonymes.get(element_type, element_type)
        if element_type not in allowed:
            refuses.append(element_type or "?")
            continue
        element: dict[str, Any] = {"type": element_type}
        if raw.get("id"):
            element["id"] = _identifier(raw.get("id"), f"e{index}")
        if label := _text(raw.get("label"), 48):
            element["label"] = label
        if color := _color(raw.get("color")):
            element["color"] = color
        if raw.get("draggable") is True:
            element["draggable"] = True
        if raw.get("dashed") is True:
            element["dashed"] = True

        points = [_point(point) for point in raw.get("points", [])[:12]] if isinstance(raw.get("points"), list) else []
        points = [point for point in points if point is not None]
        if element_type == "point" and len(points) >= 1:
            element["points"] = points[:1]
        elif element_type in {"segment", "line", "arrow"} and len(points) >= 2:
            element["points"] = points[:2]
        elif element_type == "circle":
            center = _point(raw.get("center"))
            if center is None and points:
                # Cercle écrit comme les autres éléments : centre en premier
                # point, un point du bord en second. C'est la forme que le
                # modèle produit spontanément, tous les autres types prenant
                # `points`.
                center = points[0]
            if center:
                element["center"] = center
                if raw.get("radius") is not None:
                    element["radius"] = _number(raw.get("radius"), 1, 0.01, 10000)
                elif len(points) >= 2:
                    element["radius"] = _number(
                        math.dist((center["x"], center["y"]), (points[1]["x"], points[1]["y"])),
                        1, 0.01, 10000,
                    )
                else:
                    element["radius"] = 1.0
            else:
                continue
        elif element_type == "function":
            expression = _expression(raw.get("expression"))
            if not expression:
                continue
            element["expression"] = expression
            # Une courbe de BAC vit rarement sur R tout entier : la
            # concentration d'un réactif s'arrête à t=0, une trajectoire de
            # projectile au sol. Sans bornes, la parabole remontait de l'autre
            # côté de l'axe et l'élève lisait un rebond qui n'existe pas.
            if domaine := _intervalle(raw.get("domain"), raw.get("from"), raw.get("to")):
                element["domain"] = domaine
        elif element_type == "text":
            # Un texte SANS légende n'est rien à afficher : le point d'ancrage
            # seul dessinerait une croix muette au milieu de la figure.
            if not points or "label" not in element:
                refuses.append("text")
                continue
            element["points"] = points[:1]
        elif element_type == "polygon":
            # Le triangle d'un plan incliné, le rectangle d'une cuve, le
            # trapèze d'une coupe : trois sommets au moins, sinon c'est un
            # segment et le modèle s'est trompé de type.
            if len(points) < 3:
                refuses.append("polygon")
                continue
            element["points"] = points[:12]
            element["filled"] = raw.get("filled") is not False
        elif element_type == "angle":
            # L'ordre est celui de la notation scolaire : on lit l'angle
            # « ASB » de la première branche vers la seconde, sommet au milieu.
            if len(points) < 3:
                refuses.append("angle")
                continue
            element["points"] = points[:3]
        elif element_type == "area":
            expression = _expression(raw.get("expression"))
            bornes = _intervalle(raw.get("domain"), raw.get("from"), raw.get("to"))
            if not expression or not bornes:
                refuses.append("area")
                continue
            element["expression"] = expression
            element["domain"] = bornes
        else:
            continue
        elements.append(element)

    if refuses:
        # Le tuteur a annoncé cet élément à l'oral. S'il disparaît sans un
        # mot, l'élève cherche sur la figure un angle qu'on ne lui a jamais
        # dessiné : le silence coûte plus cher que la figure manquante.
        noter_element_refuse("jsxgraph", refuses, _text(value.get("title"), 80))

    if not elements:
        return None

    bounding_box = value.get("boundingBox")
    if isinstance(bounding_box, list) and len(bounding_box) == 4:
        bbox = [_number(item, default, -10000, 10000) for item, default in zip(bounding_box, (-5, 5, 5, -5))]
        if bbox[0] >= bbox[2] or bbox[3] >= bbox[1]:
            bbox = [-5, 5, 5, -5]
    else:
        bbox = [-5, 5, 5, -5]

    spec = {
        "engine": "jsxgraph",
        "title": _text(value.get("title"), 80),
        "boundingBox": bbox,
        "axis": value.get("axis") is not False,
        "grid": value.get("grid") is True,
        "elements": elements,
    }
    # Un axe sans nom ni unité coûte des points au BAC, et le correcteur le
    # sanctionne autant que le tracé : « t (s) » et « U (V) » font partie de
    # la figure, pas de la décoration.
    if x_label := _text(value.get("xLabel") or value.get("xlabel"), 24):
        spec["xLabel"] = x_label
    if y_label := _text(value.get("yLabel") or value.get("ylabel"), 24):
        spec["yLabel"] = y_label
    return spec


def _normalize_cytoscape(value: dict[str, Any]) -> dict[str, Any] | None:
    raw_nodes = value.get("nodes")
    raw_edges = value.get("edges")
    if not isinstance(raw_nodes, list) or not isinstance(raw_edges, list):
        return None

    nodes: list[dict[str, Any]] = []
    node_ids: set[str] = set()
    # Le nom d'origine reste la clé de lecture des flèches : elles citent ce
    # que le modèle a écrit, pas ce qu'on en a fait.
    id_par_source: dict[str, str] = {}
    for index, raw in enumerate(raw_nodes[:40]):
        if not isinstance(raw, dict):
            continue
        node_id = _slug(raw.get("id")) or _identifier(raw.get("id"), f"n{index}")
        if node_id in node_ids:
            continue
        node_ids.add(node_id)
        if isinstance(raw.get("id"), str):
            id_par_source[raw["id"].strip()] = node_id
        node = {"id": node_id, "label": _text(raw.get("label"), 60) or node_id}
        if color := _color(raw.get("color")):
            node["color"] = color
        nodes.append(node)

    edges: list[dict[str, str]] = []
    for raw in raw_edges[:60]:
        if not isinstance(raw, dict):
            continue

        def extremite(*cles: str) -> str:
            """`from`/`to`, ou `source`/`target` — les deux vocabulaires courants."""
            for cle in cles:
                brut = str(raw.get(cle, "")).strip()
                if brut:
                    return id_par_source.get(brut) or _slug(brut)
            return ""

        source = extremite("from", "source")
        target = extremite("to", "target")
        if source not in node_ids or target not in node_ids:
            continue
        edge = {"from": source, "to": target}
        if label := _text(raw.get("label"), 48):
            edge["label"] = label
        edges.append(edge)

    if not nodes:
        return None
    layout = str(value.get("layout", "breadthfirst")).lower()
    if layout not in {"breadthfirst", "circle", "grid", "cose"}:
        layout = "breadthfirst"
    return {
        "engine": "cytoscape",
        "title": _text(value.get("title"), 80),
        "layout": layout,
        "nodes": nodes,
        "edges": edges,
    }


def _normalize_matter(value: dict[str, Any]) -> dict[str, Any] | None:
    raw_bodies = value.get("bodies")
    if not isinstance(raw_bodies, list):
        return None

    width = _number(value.get("width"), 600, 320, 900)
    height = _number(value.get("height"), 320, 220, 520)
    bodies: list[dict[str, Any]] = []
    body_ids: set[str] = set()
    for index, raw in enumerate(raw_bodies[:24]):
        if not isinstance(raw, dict):
            continue
        shape = str(raw.get("shape", "")).lower()
        if shape not in {"rectangle", "circle"}:
            continue
        body_id = _identifier(raw.get("id"), f"body{index}")
        if body_id in body_ids:
            continue
        body_ids.add(body_id)
        body: dict[str, Any] = {
            "id": body_id,
            "shape": shape,
            "x": _number(raw.get("x"), width / 2, -width, width * 2),
            "y": _number(raw.get("y"), height / 2, -height, height * 2),
            "isStatic": raw.get("isStatic") is True,
            "restitution": _number(raw.get("restitution"), 0.2, 0, 1),
            "friction": _number(raw.get("friction"), 0.1, 0, 1),
        }
        if shape == "circle":
            body["radius"] = _number(raw.get("radius"), 24, 4, 160)
        else:
            body["width"] = _number(raw.get("width"), 80, 8, width * 1.5)
            body["height"] = _number(raw.get("height"), 36, 8, height * 1.5)
        # Sans l'angle, un plan incliné se dessinait HORIZONTAL et la caisse
        # tombait tout droit : la simulation contredisait la leçon.
        if raw.get("angle") is not None:
            body["angle"] = _number(raw.get("angle"), 0, -math.pi, math.pi)
        if label := _text(raw.get("label"), 32):
            body["label"] = label
        if color := _color(raw.get("color")):
            body["color"] = color
        if velocity := _point(raw.get("velocity"), minimum=-50, maximum=50):
            body["velocity"] = velocity
        bodies.append(body)

    constraints: list[dict[str, Any]] = []
    raw_constraints = value.get("constraints", [])
    if isinstance(raw_constraints, list):
        for raw in raw_constraints[:20]:
            if not isinstance(raw, dict):
                continue
            constraint: dict[str, Any] = {
                "length": _number(raw.get("length"), 100, 0, 1000),
                "stiffness": _number(raw.get("stiffness"), 0.7, 0, 1),
            }
            source = str(raw.get("fromBody", "")).strip()
            target = str(raw.get("toBody", "")).strip()
            if source in body_ids:
                constraint["fromBody"] = source
            if target in body_ids:
                constraint["toBody"] = target
            if point_a := _point(raw.get("pointA"), minimum=-1000, maximum=1000):
                constraint["pointA"] = point_a
            if point_b := _point(raw.get("pointB"), minimum=-1000, maximum=1000):
                constraint["pointB"] = point_b
            if "fromBody" in constraint or "toBody" in constraint or "pointA" in constraint:
                constraints.append(constraint)

    if not bodies:
        return None
    gravity = _point(value.get("gravity"), minimum=-5, maximum=5) or {"x": 0.0, "y": 1.0}
    result: dict[str, Any] = {
        "engine": "matter",
        "title": _text(value.get("title"), 80),
        "width": width,
        "height": height,
        "gravity": gravity,
        "autoplay": value.get("autoplay") is not False,
        "bodies": bodies,
    }
    if constraints:
        result["constraints"] = constraints
    return result


def _normalize_roughsvg(value: dict[str, Any]) -> dict[str, Any] | None:
    """Normalise un schéma SVG dessiné avec des primitives Rough.js sûres.

    Aucun chemin SVG, fragment HTML ou gestionnaire d'événement ne traverse
    cette fonction. Le navigateur reçoit uniquement des nombres bornés, du
    texte court et une palette contrôlée.
    """
    raw_elements = value.get("elements")
    if not isinstance(raw_elements, list):
        return None

    width = _number(value.get("width"), 800, 320, 1000)
    height = _number(value.get("height"), 440, 220, 700)
    allowed = {"line", "arrow", "rect", "circle", "ellipse", "polygon", "polyline", "text"}
    synonyms = {
        "rectangle": "rect", "box": "rect", "boite": "rect", "boîte": "rect",
        "fleche": "arrow", "flèche": "arrow", "vector": "arrow", "vecteur": "arrow",
        "label": "text", "texte": "text", "oval": "ellipse", "ovale": "ellipse",
        "segment": "line", "polyligne": "polyline", "polygone": "polygon",
    }
    elements: list[dict[str, Any]] = []

    def coordinate(raw: Any, default: float, maximum: float) -> float:
        return _number(raw, default, 0, maximum)

    for index, raw in enumerate(raw_elements[:60]):
        if not isinstance(raw, dict):
            continue
        element_type = str(raw.get("type", "")).strip().lower()
        element_type = synonyms.get(element_type, element_type)
        if element_type not in allowed:
            continue

        element: dict[str, Any] = {"type": element_type}
        if raw.get("id"):
            element["id"] = _identifier(raw.get("id"), f"shape{index}")
        if color := _color(raw.get("color") or raw.get("stroke")):
            element["color"] = color
        if fill := _color(raw.get("fill")):
            element["fill"] = fill
        if raw.get("dashed") is True:
            element["dashed"] = True
        if raw.get("strokeWidth") is not None or raw.get("stroke_width") is not None:
            element["strokeWidth"] = _number(
                raw.get("strokeWidth", raw.get("stroke_width")), 2.2, 0.8, 8,
            )

        raw_points = raw.get("points")
        points = []
        if isinstance(raw_points, list):
            for point in raw_points[:20]:
                if not isinstance(point, dict):
                    continue
                points.append({
                    "x": coordinate(point.get("x"), 0, width),
                    "y": coordinate(point.get("y"), 0, height),
                })

        if element_type in {"line", "arrow"}:
            if len(points) < 2:
                continue
            element["points"] = points[:2]
        elif element_type == "polyline":
            if len(points) < 2:
                continue
            element["points"] = points
        elif element_type == "polygon":
            if len(points) < 3:
                continue
            element["points"] = points
        elif element_type == "rect":
            element.update({
                "x": coordinate(raw.get("x"), width / 4, width),
                "y": coordinate(raw.get("y"), height / 4, height),
                "width": _number(raw.get("width"), width / 4, 4, width),
                "height": _number(raw.get("height"), height / 4, 4, height),
            })
            element["width"] = min(element["width"], width - element["x"])
            element["height"] = min(element["height"], height - element["y"])
            if element["width"] < 4 or element["height"] < 4:
                continue
        elif element_type == "circle":
            element.update({
                "x": coordinate(raw.get("x", raw.get("cx")), width / 2, width),
                "y": coordinate(raw.get("y", raw.get("cy")), height / 2, height),
                "radius": _number(raw.get("radius", raw.get("r")), 24, 3, min(width, height) / 2),
            })
        elif element_type == "ellipse":
            element.update({
                "x": coordinate(raw.get("x", raw.get("cx")), width / 2, width),
                "y": coordinate(raw.get("y", raw.get("cy")), height / 2, height),
                "radiusX": _number(raw.get("radiusX", raw.get("rx")), 40, 3, width / 2),
                "radiusY": _number(raw.get("radiusY", raw.get("ry")), 24, 3, height / 2),
            })
        elif element_type == "text":
            text = _text(raw.get("text", raw.get("label")), 72)
            if not text:
                continue
            align = str(raw.get("align", "middle")).lower()
            if align not in {"start", "middle", "end"}:
                align = "middle"
            element.update({
                "x": coordinate(raw.get("x"), width / 2, width),
                "y": coordinate(raw.get("y"), height / 2, height),
                "text": text,
                "fontSize": _number(raw.get("fontSize", raw.get("font_size")), 16, 10, 36),
                "align": align,
            })
        elements.append(element)

    if not elements:
        return None

    legend: list[dict[str, str]] = []
    raw_legend = value.get("legend")
    if isinstance(raw_legend, list):
        for raw in raw_legend[:8]:
            if not isinstance(raw, dict):
                continue
            color = _color(raw.get("color"))
            label = _text(raw.get("label"), 48)
            if color and label:
                legend.append({"color": color, "label": label})

    result: dict[str, Any] = {
        "engine": "roughsvg",
        "title": _text(value.get("title"), 80),
        "description": _text(value.get("description"), 240),
        "width": width,
        "height": height,
        "background": _color(value.get("background")) or "#07111f",
        "elements": elements,
    }
    if legend:
        result["legend"] = legend
    return result


def scientific_visual_quality(value: Any) -> dict[str, Any]:
    """Retourne un score mécanique et des défauts actionnables (0 à 100).

    Ce contrôle ne prétend pas remplacer une validation disciplinaire. Il
    élimine les défauts objectivables avant affichage : figure vide, absence
    de légendes, texte hors cadre ou empilement de libellés.
    """
    normalized = normalize_scientific_visual(value)
    if normalized is None:
        return {"score": 0, "issues": ["Spécification invalide ou vide."], "acceptable": False}

    score = 100
    issues: list[str] = []
    if not normalized.get("title"):
        score -= 10
        issues.append("Ajouter un titre scientifique court.")

    if normalized["engine"] == "roughsvg":
        elements = normalized["elements"]
        shapes = [element for element in elements if element["type"] != "text"]
        texts = [element for element in elements if element["type"] == "text"]
        if len(shapes) < 2:
            score -= 30
            issues.append("Le schéma doit contenir au moins deux objets scientifiques.")
        if not texts:
            score -= 30
            issues.append("Ajouter des légendes directement sur le schéma.")
        if len(normalized.get("description", "")) < 12:
            score -= 10
            issues.append("Ajouter une description accessible du message scientifique.")

        width, height = normalized["width"], normalized["height"]
        boxes: list[tuple[float, float, float, float, str]] = []
        for text in texts:
            font = text.get("fontSize", 16)
            estimated_width = min(width, max(font, len(text["text"]) * font * 0.55))
            x = text["x"]
            if text.get("align") == "start":
                left = x
            elif text.get("align") == "end":
                left = x - estimated_width
            else:
                left = x - estimated_width / 2
            top = text["y"] - font
            right, bottom = left + estimated_width, text["y"] + font * 0.25
            if left < 0 or top < 0 or right > width or bottom > height:
                score -= 8
                issues.append(f"Replacer la légende « {text['text']} » dans le cadre.")
            boxes.append((left, top, right, bottom, text["text"]))

        overlaps = 0
        for index, first in enumerate(boxes):
            for second in boxes[index + 1:]:
                intersection = max(0, min(first[2], second[2]) - max(first[0], second[0])) * max(
                    0, min(first[3], second[3]) - max(first[1], second[1]),
                )
                if intersection > 40:
                    overlaps += 1
        if overlaps:
            score -= min(25, overlaps * 5)
            issues.append(f"Séparer {overlaps} paire(s) de légendes qui se chevauchent.")

    elif normalized["engine"] == "cytoscape":
        if len(normalized["nodes"]) < 2:
            score -= 30
            issues.append("Le processus doit contenir au moins deux étapes.")
        if len(normalized["nodes"]) > 1 and not normalized["edges"]:
            score -= 35
            issues.append("Relier les étapes par des flèches orientées.")
    elif normalized["engine"] == "jsxgraph":
        labelled = sum(bool(element.get("label")) for element in normalized["elements"])
        if labelled == 0:
            score -= 20
            issues.append("Légender les points, vecteurs ou courbes utiles.")
    elif normalized["engine"] == "matter":
        labelled = sum(bool(body.get("label")) for body in normalized["bodies"])
        if labelled < min(2, len(normalized["bodies"])):
            score -= 15
            issues.append("Légender les corps de la simulation.")

    score = max(0, score)
    return {"score": score, "issues": list(dict.fromkeys(issues)), "acceptable": score >= 60}


def normalize_scientific_visual(value: Any) -> dict[str, Any] | None:
    """Return a bounded declarative visual spec, or ``None`` when invalid."""

    if not isinstance(value, dict):
        return None
    engine = str(value.get("engine", "")).strip().lower()
    if engine == "jsxgraph":
        return _normalize_jsxgraph(value)
    if engine == "cytoscape":
        return _normalize_cytoscape(value)
    if engine == "matter":
        return _normalize_matter(value)
    if engine in {"roughsvg", "rough", "svg"}:
        return _normalize_roughsvg(value)
    return None
