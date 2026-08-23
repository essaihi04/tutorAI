import { useCallback, useEffect, useRef, useState } from 'react';
import Matter from 'matter-js';
import type { MatterBodySpec, MatterMeasureSpec, MatterVisualSpec } from './types';

interface MatterSimulationProps {
  spec: MatterVisualSpec;
}

interface MatterRuntime {
  engine: Matter.Engine;
  render: Matter.Render;
  runner: Matter.Runner;
  labelHandler: () => void;
}

/**
 * Matter avance d'un pas toutes les 1/60 s : une vitesse sort en pixels par
 * PAS, pas par seconde. Sans ce facteur, une chute libre afficherait une
 * vitesse soixante fois trop petite.
 */
const STEPS_PER_SECOND = 60;

/**
 * Convertit une grandeur du moteur vers l'unité affichée.
 *
 * Le moteur ne connaît que des pixels. `scale` dit combien en vaut un mètre ;
 * sans elle, le validateur a déjà retiré l'unité et le nombre reste dans le
 * repère de la scène. C'est le seul choix honnête : un nombre faux sous une
 * simulation juste se retient mieux qu'un nombre absent.
 */
function readMeasure(measure: MatterMeasureSpec, body: Matter.Body | undefined,
                     seconds: number, scale: number): number {
  if (measure.quantity === 'time') return seconds;
  if (!body) return Number.NaN;
  switch (measure.quantity) {
    case 'x': return body.position.x / scale;
    case 'y': return body.position.y / scale;
    // L'axe y de Matter descend : la hauteur se compte DEPUIS le sol, sinon
    // un corps qui tombe verrait son altitude augmenter.
    case 'height': return ((measure.origin ?? 0) - body.position.y) / scale;
    case 'vx': return (body.velocity.x * STEPS_PER_SECOND) / scale;
    case 'vy': return (body.velocity.y * STEPS_PER_SECOND) / scale;
    case 'speed': return (Matter.Vector.magnitude(body.velocity) * STEPS_PER_SECOND) / scale;
    // Un angle est un angle : aucune échelle en jeu, seulement des degrés.
    case 'angle': return (body.angle * 180) / Math.PI;
    default: return Number.NaN;
  }
}

const COLORS: Record<string, string> = {
  red: '#ef4444', blue: '#3b82f6', green: '#22c55e', orange: '#f97316',
  purple: '#a855f7', cyan: '#06b6d4', yellow: '#eab308', white: '#e2e8f0',
};

function resolveColor(color?: string): string {
  if (!color) return '#38bdf8';
  return COLORS[color] || color;
}

type Overrides = Record<string, number>;

function createBody(body: MatterBodySpec, overrides: Overrides): Matter.Body {
  const tuned = (field: string, fallback: number | undefined, standard: number) =>
    overrides[`${body.id}.${field}`] ?? fallback ?? standard;

  const options: Matter.IChamferableBodyDefinition = {
    isStatic: body.isStatic === true,
    restitution: tuned('restitution', body.restitution, 0.2),
    friction: tuned('friction', body.friction, 0.1),
    // Matter freine par défaut (0,01). Les exercices du BAC négligent les
    // frottements : sans ce zéro, une chute libre atteignait une vitesse
    // limite et démentait la leçon qu'elle illustre.
    frictionAir: body.frictionAir ?? 0,
    label: body.id,
    render: {
      fillStyle: resolveColor(body.color),
      strokeStyle: '#e2e8f0',
      lineWidth: 1.5,
    },
  };

  const created = body.shape === 'circle'
    ? Matter.Bodies.circle(body.x, body.y, body.radius || 24, options)
    : Matter.Bodies.rectangle(body.x, body.y, body.width || 80, body.height || 36, options);

  const angle = tuned('angle', body.angle, 0);
  if (angle !== 0) Matter.Body.setAngle(created, angle);

  const vx = tuned('vx', body.velocity?.x, 0);
  const vy = tuned('vy', body.velocity?.y, 0);
  if (vx !== 0 || vy !== 0) Matter.Body.setVelocity(created, { x: vx, y: vy });
  return created;
}

export default function MatterSimulation({ spec }: MatterSimulationProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const runtimeRef = useRef<MatterRuntime | null>(null);
  // Les mesures changent soixante fois par seconde. Les passer par l'état de
  // React relancerait tout l'arbre à chaque image : on écrit dans le DOM.
  const readoutRef = useRef<HTMLDivElement>(null);
  const [revision, setRevision] = useState(0);
  const [running, setRunning] = useState(spec.autoplay !== false);
  const [error, setError] = useState<string | null>(null);
  const [overrides, setOverrides] = useState<Overrides>(() =>
    Object.fromEntries((spec.parameters || []).map(p => [p.target, p.value])));

  const stopRuntime = useCallback(() => {
    const runtime = runtimeRef.current;
    if (!runtime) return;
    Matter.Events.off(runtime.render, 'afterRender', runtime.labelHandler);
    Matter.Render.stop(runtime.render);
    Matter.Runner.stop(runtime.runner);
    Matter.World.clear(runtime.engine.world, false);
    Matter.Engine.clear(runtime.engine);
    runtime.render.canvas.remove();
    runtime.render.textures = {};
    runtimeRef.current = null;
  }, []);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let active = true;
    const updateStatus = (isRunning: boolean, message: string | null) => {
      queueMicrotask(() => {
        if (!active) return;
        setRunning(isRunning);
        setError(message);
      });
    };
    stopRuntime();
    try {
      const width = spec.width || 600;
      const height = spec.height || 320;
      const engine = Matter.Engine.create();
      engine.gravity.x = overrides.gravityX ?? spec.gravity?.x ?? 0;
      engine.gravity.y = overrides.gravity ?? spec.gravity?.y ?? 1;

      const render = Matter.Render.create({
        element: container,
        engine,
        options: {
          width,
          height,
          wireframes: false,
          background: '#07111f',
          pixelRatio: Math.min(window.devicePixelRatio || 1, 2),
        },
      });
      render.canvas.style.width = '100%';
      render.canvas.style.height = 'auto';
      render.canvas.style.maxHeight = '360px';

      const bodyById = new Map<string, Matter.Body>();
      const bodies = spec.bodies.map(bodySpec => {
        const body = createBody(bodySpec, overrides);
        bodyById.set(bodySpec.id, body);
        return body;
      });
      Matter.Composite.add(engine.world, bodies);

      for (const constraint of spec.constraints || []) {
        const bodyA = constraint.fromBody ? bodyById.get(constraint.fromBody) : undefined;
        const bodyB = constraint.toBody ? bodyById.get(constraint.toBody) : undefined;
        Matter.Composite.add(engine.world, Matter.Constraint.create({
          bodyA,
          bodyB,
          pointA: constraint.pointA,
          pointB: constraint.pointB,
          length: constraint.length,
          stiffness: constraint.stiffness ?? 0.7,
          render: { strokeStyle: '#cbd5e1', lineWidth: 2 },
        }));
      }

      const labelById = new Map(spec.bodies.map(body => [body.id, body.label || '']));
      // Le temps se compte depuis le premier pas SIMULÉ, pas depuis l'arrivée
      // du composant : une pause ne doit pas gonfler la durée de chute.
      let steps = 0;
      Matter.Events.on(engine, 'afterUpdate', () => { steps += 1; });

      const measures = spec.measures || [];
      const scale = spec.scale && spec.scale > 0 ? spec.scale : 1;
      const cells = measures.map(() => document.createElement('span'));
      if (measures.length && readoutRef.current) {
        readoutRef.current.replaceChildren(...measures.map((measure, index) => {
          const cell = document.createElement('div');
          cell.className = 'rounded-md bg-slate-900/70 px-2 py-1';
          const name = document.createElement('span');
          name.className = 'text-slate-400';
          name.textContent = `${measure.label} `;
          cells[index].className = 'font-semibold text-cyan-200 tabular-nums';
          cell.append(name, cells[index]);
          return cell;
        }));
      }

      const labelHandler = () => {
        const context = render.context;
        context.save();
        context.fillStyle = '#f8fafc';
        context.font = "600 14px 'Patrick Hand', sans-serif";
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        for (const body of bodies) {
          const label = labelById.get(body.label);
          if (label) context.fillText(label, body.position.x, body.position.y);
        }
        context.restore();

        measures.forEach((measure, index) => {
          const value = readMeasure(
            measure, measure.body ? bodyById.get(measure.body) : undefined,
            steps / STEPS_PER_SECOND, scale,
          );
          cells[index].textContent = Number.isFinite(value)
            ? `${value.toFixed(measure.decimals)}${measure.unit ? ` ${measure.unit}` : ''}`
            : '—';
        });
      };
      Matter.Events.on(render, 'afterRender', labelHandler);

      const runner = Matter.Runner.create();
      runtimeRef.current = { engine, render, runner, labelHandler };
      Matter.Render.run(render);
      const initiallyRunning = spec.autoplay !== false;
      if (initiallyRunning) Matter.Runner.run(runner, engine);
      updateStatus(initiallyRunning, null);
    } catch (reason) {
      console.error('[ScientificVisual][Matter] Render failed:', reason);
      updateStatus(false, 'La simulation scientifique ne peut pas démarrer.');
    }

    return () => {
      active = false;
      stopRuntime();
    };
  }, [revision, spec, stopRuntime, overrides]);

  const toggleRunning = () => {
    setRunning(value => {
      const next = !value;
      const runtime = runtimeRef.current;
      if (runtime) {
        if (next) Matter.Runner.run(runtime.runner, runtime.engine);
        else Matter.Runner.stop(runtime.runner);
      }
      return next;
    });
  };
  const reset = () => {
    setRevision(value => value + 1);
  };

  return (
    <figure className="my-3 overflow-hidden rounded-xl border border-white/10 bg-slate-950/70 p-2">
      <div className="flex items-center justify-between gap-3 px-2 pb-2">
        <figcaption className="text-sm font-medium text-cyan-200">{spec.title || 'Simulation scientifique'}</figcaption>
        <div className="flex gap-2">
          <button type="button" onClick={toggleRunning} className="rounded-md bg-cyan-600 px-3 py-1 text-xs font-semibold text-white hover:bg-cyan-500">
            {running ? 'Pause' : 'Démarrer'}
          </button>
          <button type="button" onClick={reset} className="rounded-md bg-slate-700 px-3 py-1 text-xs font-semibold text-white hover:bg-slate-600">
            Recommencer
          </button>
        </div>
      </div>
      {error && <p className="px-2 pb-2 text-sm text-red-300">{error}</p>}
      <div ref={containerRef} className="flex w-full justify-center overflow-hidden rounded-lg" />

      {/* Sans lecture, l'élève regarde une bille tomber sans jamais voir sa
          vitesse augmenter : c'est une animation, pas une expérience. */}
      <div
        ref={readoutRef}
        className="mt-2 flex flex-wrap gap-2 px-2 text-xs"
        role="status"
        aria-live="polite"
        aria-label="Grandeurs mesurées"
      />

      {/* Déplacer un curseur rejoue la scène depuis le début : c'est la seule
          façon de comparer deux essais qui ne diffèrent que par ce réglage. */}
      {(spec.parameters || []).length > 0 && (
        <div className="mt-2 grid gap-2 px-2 pb-1 sm:grid-cols-2">
          {(spec.parameters || []).map(parameter => (
            <label key={parameter.target} className="text-xs text-slate-300">
              <span className="flex justify-between gap-2">
                <span>{parameter.label}</span>
                <span className="font-semibold tabular-nums text-cyan-200">
                  {(overrides[parameter.target] ?? parameter.value).toFixed(2)}
                  {parameter.unit ? ` ${parameter.unit}` : ''}
                </span>
              </span>
              <input
                type="range"
                className="mt-1 w-full accent-cyan-500"
                min={parameter.min}
                max={parameter.max}
                step={parameter.step}
                value={overrides[parameter.target] ?? parameter.value}
                onChange={event => {
                  const value = Number(event.target.value);
                  setOverrides(previous => ({ ...previous, [parameter.target]: value }));
                }}
              />
            </label>
          ))}
        </div>
      )}
    </figure>
  );
}
