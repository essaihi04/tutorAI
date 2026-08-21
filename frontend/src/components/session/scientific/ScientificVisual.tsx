import { lazy, Suspense } from 'react';
import type { ScientificVisualSpec } from './types';

const JSXGraphVisual = lazy(() => import('./JSXGraphVisual'));
const CytoscapeVisual = lazy(() => import('./CytoscapeVisual'));
const MatterSimulation = lazy(() => import('./MatterSimulation'));

interface ScientificVisualProps {
  spec: ScientificVisualSpec;
}

function LoadingScientificVisual() {
  return (
    <div className="flex h-64 items-center justify-center text-sm text-cyan-200/70">
      Préparation du visuel scientifique…
    </div>
  );
}

export default function ScientificVisual({ spec }: ScientificVisualProps) {
  return (
    <Suspense fallback={<LoadingScientificVisual />}>
      {spec.engine === 'jsxgraph' && <JSXGraphVisual spec={spec} />}
      {spec.engine === 'cytoscape' && <CytoscapeVisual spec={spec} />}
      {spec.engine === 'matter' && <MatterSimulation spec={spec} />}
    </Suspense>
  );
}

