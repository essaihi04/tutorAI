# Engine routing

Choose one primary representation. Do not install or combine every visual library.

## First choice: validated project resources

Use `show_schema` for a matching BAC schema. Use an existing HTML simulation when it already represents the experiment or process. These resources have pedagogical layout and labels that generic engines cannot infer reliably.

## Rough.js

Use only to give live SVG primitives a consistent hand-drawn board style. Keep the underlying geometry explicit. Do not use Rough.js as a scientific layout engine.

## JSXGraph

Use for coordinate-dependent figures:

- mathematical functions and constructions;
- vectors, force diagrams, and trajectories;
- rays, lenses, and geometric optics;
- circles, lines, points, and measurements.

Prefer a static schema when no interaction or coordinate system is needed.

## Cytoscape

Use for node-and-arrow structures:

- metabolic or genetic pathways;
- causal chains and regulatory networks;
- food webs and related process maps.

It is not suitable for anatomical drawings, molecules, apparatus, or spatially accurate cell structures.

## Matter.js

Use for simple 2D mechanics:

- falling bodies and projectiles;
- collisions;
- pendulums and springs;
- motion on a simple plane.

Use it only when motion changes the learner's understanding. A force diagram alone belongs in JSXGraph or a validated schema.

## Deferred tools

Do not add these by default:

- Excalidraw: editor payload and bundle are unnecessary for read-only course rendering.
- Ketcher or RDKit: add later only for editable or generated molecular structures.
- Schemdraw: add through a controlled server-side export only if the existing circuit schemas become insufficient.
- Three.js: add only for a lesson that truly needs 3D depth or camera movement.

Each deferred tool needs a concrete lesson, an accessibility fallback, tests, and a bundle-size review before adoption.
