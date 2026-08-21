# Full simulation contract

Start from `frontend/public/media/simulations/TEMPLATE_SIMULATION.html` and preserve its bridge with the tutor.

## Pedagogical contract

- State one observable objective.
- Give the learner one meaningful control or a small set of variants.
- Display the variable, unit, and interpretation in French.
- Include start, reset, and replay behavior.
- Keep the result deterministic when the lesson does not teach randomness.
- Provide a static explanatory fallback when animation is not essential.

## Runtime contract

- Use a stable snake_case simulation ID.
- Fit inside `100vh` without page or internal scrolling.
- Accept `simulation_control` messages for `start`, `set_variant`, and `reset`.
- Publish `simulation_state` messages with the same simulation ID.
- Keep statuses to `idle`, `running`, and `finished`.
- Report current state, completed variants, learner actions, and objective progress.
- Avoid external network requests and third-party runtime scripts.

## Rendering choice

- Use SVG and CSS for most SVT and chemistry processes.
- Use Matter.js for genuine 2D mechanics.
- Use JSXGraph for functions, vectors, geometry, and optics.
- Do not turn a static explanation into a simulation merely to add motion.

Test every control manually and verify that the parent receives the final `finished` state.
