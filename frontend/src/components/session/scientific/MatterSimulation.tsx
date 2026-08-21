import { useCallback, useEffect, useRef, useState } from 'react';
import Matter from 'matter-js';
import type { MatterBodySpec, MatterVisualSpec } from './types';

interface MatterSimulationProps {
  spec: MatterVisualSpec;
}

interface MatterRuntime {
  engine: Matter.Engine;
  render: Matter.Render;
  runner: Matter.Runner;
  labelHandler: () => void;
}

const COLORS: Record<string, string> = {
  red: '#ef4444', blue: '#3b82f6', green: '#22c55e', orange: '#f97316',
  purple: '#a855f7', cyan: '#06b6d4', yellow: '#eab308', white: '#e2e8f0',
};

function resolveColor(color?: string): string {
  if (!color) return '#38bdf8';
  return COLORS[color] || color;
}

function createBody(body: MatterBodySpec): Matter.Body {
  const options: Matter.IChamferableBodyDefinition = {
    isStatic: body.isStatic === true,
    restitution: body.restitution ?? 0.2,
    friction: body.friction ?? 0.1,
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

  if (body.velocity) Matter.Body.setVelocity(created, body.velocity);
  return created;
}

export default function MatterSimulation({ spec }: MatterSimulationProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const runtimeRef = useRef<MatterRuntime | null>(null);
  const [revision, setRevision] = useState(0);
  const [running, setRunning] = useState(spec.autoplay !== false);
  const [error, setError] = useState<string | null>(null);

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
      engine.gravity.x = spec.gravity?.x ?? 0;
      engine.gravity.y = spec.gravity?.y ?? 1;

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
        const body = createBody(bodySpec);
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
  }, [revision, spec, stopRuntime]);

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
    </figure>
  );
}
