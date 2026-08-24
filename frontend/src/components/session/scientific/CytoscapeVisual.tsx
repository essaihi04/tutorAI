import { useEffect, useRef, useState } from 'react';
import cytoscape from 'cytoscape';
import type { CytoscapeVisualSpec } from './types';

interface CytoscapeVisualProps {
  spec: CytoscapeVisualSpec;
  /** La figure se pose SUR le tableau : ni cadre, ni fond peint. */
  transparent?: boolean;
}

const COLORS: Record<string, string> = {
  red: '#ef4444',
  blue: '#3b82f6',
  green: '#22c55e',
  orange: '#f97316',
  purple: '#a855f7',
  cyan: '#06b6d4',
  yellow: '#eab308',
};

function resolveColor(color?: string): string {
  if (!color) return '#2563eb';
  return COLORS[color] || color;
}


/**
 * Le cadre de la figure. Sur le tableau il n'y en a pas : la figure est
 * dessinee sur l'ardoise, pas collee dessus.
 */
function CADRE_FIGURE(transparent?: boolean): string {
  return transparent
    ? 'my-0 h-full w-full p-0'
    : 'my-3 overflow-hidden rounded-xl border border-white/10 bg-slate-950/70 p-2';
}

export default function CytoscapeVisual({ spec, transparent }: CytoscapeVisualProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    let instance: cytoscape.Core | null = null;
    let observer: ResizeObserver | null = null;
    let active = true;
    const reportError = (message: string | null) => {
      queueMicrotask(() => {
        if (active) setError(message);
      });
    };
    try {
      instance = cytoscape({
        container: containerRef.current,
        elements: [
          ...spec.nodes.map(node => ({
            data: {
              id: node.id,
              label: node.label,
              color: resolveColor(node.color),
              active: node.active === true ? 1 : 0,
            },
          })),
          ...spec.edges.map((edge, index) => ({
            data: {
              id: `edge-${index}-${edge.from}-${edge.to}`,
              source: edge.from,
              target: edge.to,
              label: edge.label || '',
              color: resolveColor(edge.color || (edge.active ? 'cyan' : undefined)),
              active: edge.active === true ? 1 : 0,
            },
          })),
        ],
        layout: {
          name: spec.layout || 'breadthfirst',
          directed: true,
          padding: 24,
          spacingFactor: 1.2,
        } as cytoscape.LayoutOptions,
        style: [
          {
            selector: 'node',
            style: {
              'background-color': 'data(color)',
              'border-color': '#bfdbfe',
              'border-width': 'mapData(active, 0, 1, 2, 5)',
              color: '#f8fafc',
              label: 'data(label)',
              'font-size': 13,
              'font-weight': 600,
              'text-wrap': 'wrap',
              'text-max-width': '110px',
              'text-valign': 'center',
              'text-halign': 'center',
              width: 110,
              height: 48,
              shape: 'round-rectangle',
            },
          },
          {
            selector: 'edge',
            style: {
              width: 'mapData(active, 0, 1, 2.5, 5)',
              'line-color': 'data(color)',
              'target-arrow-color': 'data(color)',
              'target-arrow-shape': 'triangle',
              'curve-style': 'bezier',
              color: '#e2e8f0',
              label: 'data(label)',
              'font-size': 11,
              'text-background-color': '#0f172a',
              'text-background-opacity': 0.85,
              'text-background-padding': '3px',
            },
          },
        ],
        // Les processus du chapitre SVT peuvent avoir 7 niveaux (coenzymes
        // → chaîne → gradient → ATP). À 0,55 le premier et le dernier nœud
        // sortaient du cadre de 320 px ; `fit()` doit pouvoir descendre un
        // peu plus tout en gardant les libellés lisibles.
        minZoom: 0.35,
        maxZoom: 2,
      });

      instance.fit(undefined, 24);
      reportError(null);
      observer = new ResizeObserver(() => {
        instance?.resize();
        instance?.fit(undefined, 24);
      });
      observer.observe(containerRef.current);
    } catch (reason) {
      console.error('[ScientificVisual][Cytoscape] Render failed:', reason);
      reportError('Le réseau scientifique ne peut pas être affiché.');
    }

    return () => {
      active = false;
      observer?.disconnect();
      instance?.destroy();
    };
  }, [spec]);

  return (
    <figure className={CADRE_FIGURE(transparent)}>
      {spec.title && <figcaption className="px-2 pb-2 text-sm font-medium text-cyan-200">{spec.title}</figcaption>}
      {error && <p className="px-2 pb-2 text-sm text-red-300">{error}</p>}
      <div
        ref={containerRef}
        className="h-80 w-full"
        role="img"
        aria-label={spec.title || 'Réseau scientifique interactif'}
      />
    </figure>
  );
}
