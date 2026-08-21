"""Routing prompt and validation for LLM-generated scientific visuals.

The application LLM cannot load Codex ``SKILL.md`` files at runtime.  This
module mirrors the small, machine-facing part of the project skill and keeps
untrusted visual JSON declarative before it reaches the browser renderers.
"""

from __future__ import annotations

import ast
import math
import re
from typing import Any


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

Format JSXGraph :
{"type":"scientific","content":"Figure","scientific":{"engine":"jsxgraph","title":"Bilan des forces","boundingBox":[-5,5,5,-5],"axis":true,"grid":false,"elements":[{"type":"point","points":[{"x":0,"y":0}],"label":"S","color":"cyan"},{"type":"arrow","points":[{"x":0,"y":0},{"x":0,"y":-3}],"label":"Poids","color":"red"}]}}
Types d'éléments : `point`, `segment`, `line`, `arrow`, `circle`, `function`.
Une fonction utilise `expression` avec x, nombres et seulement sin, cos, tan,
sqrt, abs, exp, ln, log, pi, e. Écris toujours la multiplication avec `*` :
`2*x`, jamais `2x`.

Format Cytoscape :
{"type":"scientific","content":"Processus","scientific":{"engine":"cytoscape","title":"Respiration cellulaire","layout":"breadthfirst","nodes":[{"id":"glucose","label":"Glucose"},{"id":"pyruvate","label":"Pyruvate"}],"edges":[{"from":"glucose","to":"pyruvate","label":"Glycolyse"}]}}
Layouts : `breadthfirst`, `circle`, `grid`, `cose`.

Format Matter :
{"type":"scientific","content":"Manipulation","scientific":{"engine":"matter","title":"Chute verticale","width":600,"height":320,"gravity":{"x":0,"y":1},"autoplay":true,"bodies":[{"id":"sol","shape":"rectangle","x":300,"y":305,"width":580,"height":20,"isStatic":true,"label":"Sol"},{"id":"balle","shape":"circle","x":300,"y":60,"radius":22,"label":"Balle","color":"orange","restitution":0.5}]}}

RÈGLES DE QUALITÉ :
- Toutes les légendes sont courtes et en français.
- Représente uniquement les objets utiles ; pas de surcharge ni chevauchement.
- Respecte les conventions BAC : symboles, sens des flèches, unités et noms.
- Une simulation doit faire observer une variable ou tester une hypothèse ;
  sinon un schéma statique suffit.
- N'invente jamais un moteur, un type d'élément ou du code JavaScript.
""".strip()


_COLORS = {
    "red", "blue", "green", "orange", "purple", "cyan", "yellow", "white",
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


def _point(value: Any, *, minimum: float = -10000, maximum: float = 10000) -> dict[str, float] | None:
    if not isinstance(value, dict):
        return None
    return {
        "x": _number(value.get("x"), 0, minimum, maximum),
        "y": _number(value.get("y"), 0, minimum, maximum),
    }


def _expression(value: Any) -> str | None:
    expression = _text(value, 100)
    if not expression or "**" in expression or not _EXPRESSION_CHARS.fullmatch(expression):
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
    allowed = {"point", "segment", "line", "arrow", "circle", "function"}
    for index, raw in enumerate(raw_elements[:40]):
        if not isinstance(raw, dict):
            continue
        element_type = str(raw.get("type", "")).strip().lower()
        if element_type not in allowed:
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

        points = [_point(point) for point in raw.get("points", [])[:4]] if isinstance(raw.get("points"), list) else []
        points = [point for point in points if point is not None]
        if element_type == "point" and len(points) >= 1:
            element["points"] = points[:1]
        elif element_type in {"segment", "line", "arrow"} and len(points) >= 2:
            element["points"] = points[:2]
        elif element_type == "circle":
            center = _point(raw.get("center"))
            if center:
                element["center"] = center
                element["radius"] = _number(raw.get("radius"), 1, 0.01, 10000)
            else:
                continue
        elif element_type == "function":
            expression = _expression(raw.get("expression"))
            if not expression:
                continue
            element["expression"] = expression
        else:
            continue
        elements.append(element)

    if not elements:
        return None

    bounding_box = value.get("boundingBox")
    if isinstance(bounding_box, list) and len(bounding_box) == 4:
        bbox = [_number(item, default, -10000, 10000) for item, default in zip(bounding_box, (-5, 5, 5, -5))]
        if bbox[0] >= bbox[2] or bbox[3] >= bbox[1]:
            bbox = [-5, 5, 5, -5]
    else:
        bbox = [-5, 5, 5, -5]

    return {
        "engine": "jsxgraph",
        "title": _text(value.get("title"), 80),
        "boundingBox": bbox,
        "axis": value.get("axis") is not False,
        "grid": value.get("grid") is True,
        "elements": elements,
    }


def _normalize_cytoscape(value: dict[str, Any]) -> dict[str, Any] | None:
    raw_nodes = value.get("nodes")
    raw_edges = value.get("edges")
    if not isinstance(raw_nodes, list) or not isinstance(raw_edges, list):
        return None

    nodes: list[dict[str, Any]] = []
    node_ids: set[str] = set()
    for index, raw in enumerate(raw_nodes[:40]):
        if not isinstance(raw, dict):
            continue
        node_id = _identifier(raw.get("id"), f"n{index}")
        if node_id in node_ids:
            continue
        node_ids.add(node_id)
        node = {"id": node_id, "label": _text(raw.get("label"), 60) or node_id}
        if color := _color(raw.get("color")):
            node["color"] = color
        nodes.append(node)

    edges: list[dict[str, str]] = []
    for raw in raw_edges[:60]:
        if not isinstance(raw, dict):
            continue
        source = str(raw.get("from", "")).strip()
        target = str(raw.get("to", "")).strip()
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
    return None
