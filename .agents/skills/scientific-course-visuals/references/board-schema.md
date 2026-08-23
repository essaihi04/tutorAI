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

Allowed elements are `point`, `segment`, `line`, `arrow`, `circle`, `function`, `text`, `polygon`, `angle`, and `area`. Function expressions may contain `x`, numbers, arithmetic operators, parentheses, and the approved mathematical function names only. Write multiplication explicitly as `2*x`, never `2x`.

- `text` needs an anchor in `points` and the wording in `label`; without a label nothing is drawn.
- `polygon` takes 3 to 12 vertices — the triangle of an inclined plane, a tank, a cross-section. Set `"filled": false` to keep the outline only.
- `angle` takes three points in school order: first arm, **vertex**, second arm.
- `area` shades the region under a curve between two bounds: `expression` plus `from` and `to`.
- Add `from`/`to` (or `"domain": [a, b]`) to any `function` that only makes sense on an interval. An unbounded projectile parabola climbs back above the axis and the learner reads a bounce that never happened.
- Set `xLabel` and `yLabel` with the unit — `"t (s)"`, `"U (V)"`. An unnamed axis loses marks at the BAC, and the quality gate deducts for it on any figure that plots a curve.

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

### Measuring and tuning

A scene that cannot be read or adjusted is an animation, not a simulation: the learner watches a ball fall without ever seeing its speed rise. The quality gate deducts when both are missing.

- `scale` — pixels per metre. The engine counts in **pixels**, so without it no reading may carry a unit and the validator strips `"unit"`. Measured: `"scale": 100` with `"gravity": {"x": 0, "y": 1}` gives exactly **g = 10 m/s²**, the BAC value. Keep that pair unless the lesson needs another planet.
- `measures` — up to 6 live readings: `{"body": "balle", "quantity": "speed", "label": "Vitesse", "unit": "m/s"}`. Quantities: `x`, `y`, `height`, `vx`, `vy`, `speed`, `angle`, `time`. `angle` (degrees) and `time` (seconds) need no scale. `height` requires `origin`, the ground's y in pixels — Matter's y axis points **down**, so without it a falling body appears to rise.
- `parameters` — up to 4 sliders; moving one replays the scene from the start, which is the only way to compare two runs that differ by one setting. Targets: `gravity`, or `<bodyId>.angle` / `.restitution` / `.friction` / `.vx` / `.vy`. Add a slider only when moving it changes the lesson.
- `frictionAir` defaults to **0**, matching the "frottements négligés" of BAC problems. Raise it (0.01–0.05) only when the lesson is about drag: measured with Matter's own default, g drifted from 9.5 to 7.5 m/s² within one second and the simulation contradicted the course it illustrated.
