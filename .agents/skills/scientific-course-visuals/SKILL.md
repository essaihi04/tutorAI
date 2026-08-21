---
name: scientific-course-visuals
description: Create or adapt accurate BAC-level scientific diagrams and simulations for this tutoring platform. Use for SVT, physics, chemistry, mathematics, live-board drawing, scientific visual routing, or course simulation work; do not use for decorative photos or unrelated UI graphics.
---

# Scientific Course Visuals

Create the smallest scientifically correct visual that directly serves the lesson objective.

## Route the visual

1. Search the existing schema registry and simulation catalogue first. Reuse a validated BAC resource when one already covers the concept.
2. Use ordinary board content for text, tables, simple graphs, mind maps, and small diagrams.
3. Use a specialized declarative engine only when the concept needs it:
   - JSXGraph for geometry, functions, vectors, forces, optics, and coordinate-based figures.
   - Cytoscape for biological pathways, causal chains, networks, and process maps.
   - Matter.js for simple 2D mechanics that evolves over time.
4. Build a full simulation only when the learner must vary a parameter, observe a variable, or test a hypothesis.
5. Apply Rough.js only as the live-board drawing style. It does not decide scientific structure.

Read [references/engine-routing.md](references/engine-routing.md) before choosing an engine. Read [references/board-schema.md](references/board-schema.md) when emitting or changing board payloads. Read [references/simulation-contract.md](references/simulation-contract.md) when creating a full course simulation.

## Scientific quality

- Use short French labels and BAC curriculum conventions.
- Preserve exact symbol case: `A` majuscule and `a` minuscule are different alleles; apply the same care to units, vectors, ions, genes, and variables.
- Put labels outside shapes when possible and prevent overlaps.
- Keep arrows unambiguous and show only objects needed for the explanation.
- Prefer deterministic SVG or declarative JSON so a result is reproducible and testable.
- Never put LLM-generated JavaScript, HTML, callbacks, URLs, or event handlers in a board payload.
- Add a legend only when colors or symbols carry meaning.

## Project integration

- Existing diagrams: `frontend/src/components/session/schemas/`
- Scientific board renderers: `frontend/src/components/session/scientific/`
- Runtime LLM routing and validation: `backend/app/services/scientific_visual_skill.py`
- Simulation catalogue and template: `frontend/public/media/simulations/`

When adding a visual capability, update the TypeScript contract, backend sanitizer, LLM routing prompt, and tests together. Validate the skill, run targeted backend tests, build the frontend, and visually inspect any new diagram or simulation.
