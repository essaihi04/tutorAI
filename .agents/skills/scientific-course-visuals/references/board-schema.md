# Scientific board schema

Emit a `scientific` line only inside `show_board`. The backend sanitizes these declarative objects before they reach the browser.

## JSXGraph example

```json
{
  "type": "scientific",
  "content": "Bilan des forces",
  "scientific": {
    "engine": "jsxgraph",
    "title": "Bilan des forces",
    "boundingBox": [-5, 5, 5, -5],
    "axis": true,
    "grid": false,
    "elements": [
      {"type": "point", "points": [{"x": 0, "y": 0}], "label": "S", "color": "cyan"},
      {"type": "arrow", "points": [{"x": 0, "y": 0}, {"x": 0, "y": -3}], "label": "Poids", "color": "red"}
    ]
  }
}
```

Allowed elements are `point`, `segment`, `line`, `arrow`, `circle`, and `function`. Function expressions may contain `x`, numbers, arithmetic operators, parentheses, and the approved mathematical function names only. Write multiplication explicitly as `2*x`, never `2x`.

## Cytoscape example

```json
{
  "type": "scientific",
  "content": "Respiration cellulaire",
  "scientific": {
    "engine": "cytoscape",
    "title": "Respiration cellulaire",
    "layout": "breadthfirst",
    "nodes": [
      {"id": "glucose", "label": "Glucose"},
      {"id": "pyruvate", "label": "Pyruvate"}
    ],
    "edges": [
      {"from": "glucose", "to": "pyruvate", "label": "Glycolyse"}
    ]
  }
}
```

Allowed layouts are `breadthfirst`, `circle`, `grid`, and `cose`. Every edge endpoint must match a declared node ID.

## Matter.js example

```json
{
  "type": "scientific",
  "content": "Chute verticale",
  "scientific": {
    "engine": "matter",
    "title": "Chute verticale",
    "width": 600,
    "height": 320,
    "gravity": {"x": 0, "y": 1},
    "autoplay": true,
    "bodies": [
      {"id": "sol", "shape": "rectangle", "x": 300, "y": 305, "width": 580, "height": 20, "isStatic": true, "label": "Sol"},
      {"id": "balle", "shape": "circle", "x": 300, "y": 60, "radius": 22, "label": "Balle", "color": "orange", "restitution": 0.5}
    ]
  }
}
```

Allowed shapes are `rectangle` and `circle`. Constraints may reference declared body IDs or fixed points. Keep dimensions within the validator bounds.
