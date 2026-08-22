import { useEffect, useId, useRef, useState } from 'react';
import JXG from 'jsxgraph';
import './jsxgraph.css';
import type { JSXGraphElementSpec, JSXGraphVisualSpec, ScientificPoint } from './types';
import { compileSafeMathExpression } from './safeMathExpression';

interface JSXGraphVisualProps {
  spec: JSXGraphVisualSpec;
}

const BOARD_COLORS: Record<string, string> = {
  red: '#ef4444',
  blue: '#3b82f6',
  green: '#22c55e',
  orange: '#f97316',
  purple: '#a855f7',
  cyan: '#06b6d4',
  yellow: '#eab308',
  white: '#e2e8f0',
};

function resolveColor(color?: string): string {
  if (!color) return '#60a5fa';
  return BOARD_COLORS[color] || color;
}

function pointTuple(point: ScientificPoint): [number, number] {
  return [point.x, point.y];
}

function addElement(board: JXG.Board, element: JSXGraphElementSpec) {
  const color = resolveColor(element.color);
  const attributes = {
    name: element.label || '',
    // JSXGraph n'affiche le nom d'un segment, d'une droite, d'une flèche ou
    // d'une courbe QUE si on le demande — seul un point le montre par défaut.
    // Sans cette ligne, « P » et « R » disparaissaient d'un bilan des forces :
    // l'élève voyait deux flèches opposées sans savoir laquelle est le poids.
    withLabel: Boolean(element.label),
    strokeColor: color,
    fillColor: color,
    fixed: element.draggable !== true,
    dash: element.dashed ? 2 : 0,
    strokeWidth: 2.5,
    highlightStrokeColor: color,
    highlightFillColor: color,
    label: { color: '#e2e8f0', fontSize: 14 },
  };
  const points = element.points || [];

  switch (element.type) {
    case 'point':
      if (points[0]) board.create('point', pointTuple(points[0]), attributes);
      break;
    case 'segment':
      if (points.length >= 2) board.create('segment', [pointTuple(points[0]), pointTuple(points[1])], attributes);
      break;
    case 'line':
      if (points.length >= 2) board.create('line', [pointTuple(points[0]), pointTuple(points[1])], attributes);
      break;
    case 'arrow':
      if (points.length >= 2) board.create('arrow', [pointTuple(points[0]), pointTuple(points[1])], attributes);
      break;
    case 'circle':
      if (element.center && typeof element.radius === 'number') {
        board.create('circle', [pointTuple(element.center), element.radius], attributes);
      }
      break;
    case 'function':
      if (element.expression) {
        const fn = compileSafeMathExpression(element.expression);
        if (!fn) break;
        board.create('functiongraph', [fn], attributes);
      }
      break;
  }
}

export default function JSXGraphVisual({ spec }: JSXGraphVisualProps) {
  const reactId = useId();
  const boardId = `science-board-${reactId.replace(/[^a-zA-Z0-9_-]/g, '')}`;
  const containerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let board: JXG.Board | null = null;
    let observer: ResizeObserver | null = null;
    let active = true;
    const reportError = (message: string | null) => {
      queueMicrotask(() => {
        if (active) setError(message);
      });
    };
    try {
      board = JXG.JSXGraph.initBoard(boardId, {
        boundingbox: spec.boundingBox || [-5, 5, 5, -5],
        axis: spec.axis !== false,
        grid: spec.grid === true,
        defaultAxes: {
          x: {
            strokeColor: '#64748b',
            highlightStrokeColor: '#64748b',
            ticks: {
              strokeColor: '#475569',
              label: { color: '#cbd5e1' },
            },
          },
          y: {
            strokeColor: '#64748b',
            highlightStrokeColor: '#64748b',
            ticks: {
              strokeColor: '#475569',
              label: { color: '#cbd5e1' },
            },
          },
        },
        showCopyright: false,
        showNavigation: false,
        keepaspectratio: true,
        pan: { enabled: false },
        zoom: { wheel: false },
      });

      spec.elements.forEach(element => addElement(board as JXG.Board, element));
      board.fullUpdate();

      observer = new ResizeObserver(() => {
        if (!board || !container.clientWidth) return;
        board.resizeContainer(container.clientWidth, 320, true, true);
        board.fullUpdate();
      });
      observer.observe(container);
      reportError(null);
    } catch (reason) {
      console.error('[ScientificVisual][JSXGraph] Render failed:', reason);
      reportError('La figure scientifique ne peut pas être affichée.');
    }

    return () => {
      active = false;
      observer?.disconnect();
      if (board) JXG.JSXGraph.freeBoard(board);
    };
  }, [boardId, spec]);

  return (
    <figure className="my-3 overflow-hidden rounded-xl border border-white/10 bg-slate-950/70 p-2">
      {spec.title && <figcaption className="px-2 pb-2 text-sm font-medium text-cyan-200">{spec.title}</figcaption>}
      {error && <p className="px-2 pb-2 text-sm text-red-300">{error}</p>}
      <div
        id={boardId}
        ref={containerRef}
        className="jxgbox w-full"
        style={{ height: 320, border: 0, background: 'transparent' }}
        role="img"
        aria-label={spec.title || 'Figure scientifique interactive'}
      />
    </figure>
  );
}
