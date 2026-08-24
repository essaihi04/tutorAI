import { lazy, Suspense } from 'react';
import type { ScientificControlCommand, ScientificVisualSpec } from './types';

const JSXGraphVisual = lazy(() => import('./JSXGraphVisual'));
const CytoscapeVisual = lazy(() => import('./CytoscapeVisual'));
const MatterSimulation = lazy(() => import('./MatterSimulation'));
const RoughSVGVisual = lazy(() => import('./RoughSVGVisual'));
const ScientificPresetVisual = lazy(() => import('./ScientificPresetVisual'));

interface ScientificVisualProps {
  spec: ScientificVisualSpec;
  /**
   * La figure se pose SUR le tableau, sans son cadre ni son fond.
   *
   * Au tableau en direct, chaque moteur peignait son propre rectangle noir :
   * la figure arrivait comme une vignette collée sur l'ardoise, avec sa
   * bordure et son ombre, au lieu d'y être dessinee. Ici les fonds
   * disparaissent et il ne reste que le trait.
   */
  transparent?: boolean;
  /** Commande reçue du LLM pour la scène de catalogue actuellement visible. */
  control?: ScientificControlCommand | null;
}

function LoadingScientificVisual() {
  return (
    <div className="flex h-64 items-center justify-center text-sm text-cyan-200/70">
      Préparation du visuel scientifique…
    </div>
  );
}

export default function ScientificVisual({ spec, transparent, control }: ScientificVisualProps) {
  return (
    <Suspense fallback={<LoadingScientificVisual />}>
      {spec.engine === 'jsxgraph' && <JSXGraphVisual spec={spec} transparent={transparent} />}
      {spec.engine === 'cytoscape' && <CytoscapeVisual spec={spec} transparent={transparent} />}
      {spec.engine === 'matter' && <MatterSimulation spec={spec} transparent={transparent} />}
      {spec.engine === 'roughsvg' && <RoughSVGVisual spec={spec} transparent={transparent} />}
      {spec.engine === 'preset' && (
        <ScientificPresetVisual spec={spec} transparent={transparent} control={control} />
      )}
    </Suspense>
  );
}
