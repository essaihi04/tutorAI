import { createRoot } from 'react-dom/client';
import './index.css';
import ScientificVisual from './components/session/scientific/ScientificVisual';
import type { ScientificVisualSpec } from './components/session/scientific/types';

/** Les figures telles que le validateur les rend au navigateur. */
const CAS: ScientificVisualSpec[] = [
  {
    engine: 'jsxgraph',
    title: 'Plan incliné — bilan des forces (polygon + angle)',
    boundingBox: [-1, 6, 10, -1],
    axis: false,
    elements: [
      { type: 'polygon', points: [{ x: 0, y: 0 }, { x: 8, y: 0 }, { x: 8, y: 4 }], filled: true, color: 'white' },
      { type: 'angle', points: [{ x: 8, y: 0 }, { x: 0, y: 0 }, { x: 8, y: 4 }], label: 'α', color: 'yellow' },
      { type: 'arrow', points: [{ x: 4, y: 2 }, { x: 4, y: 0.2 }], label: 'P', color: 'red' },
      { type: 'arrow', points: [{ x: 4, y: 2 }, { x: 3, y: 4 }], label: 'R', color: 'green' },
      { type: 'text', points: [{ x: 5, y: 5 }], label: 'Solide sur plan incliné', color: 'white' },
    ],
  },
  {
    engine: 'jsxgraph',
    title: 'Projectile — courbe bornée + axes nommés',
    boundingBox: [-1, 4, 12, -1],
    axis: true,
    xLabel: 'x (m)',
    yLabel: 'y (m)',
    elements: [
      { type: 'function', expression: 'x - 0.1*x^2', domain: [0, 10], label: 'trajectoire', color: 'cyan' },
      { type: 'arrow', points: [{ x: 0, y: 0 }, { x: 1.5, y: 1.5 }], label: 'v₀', color: 'red' },
      { type: 'angle', points: [{ x: 2, y: 0 }, { x: 0, y: 0 }, { x: 1.5, y: 1.5 }], label: 'α', color: 'yellow' },
    ],
  },
  {
    engine: 'jsxgraph',
    title: 'Intégrale — aire hachurée entre a et b',
    boundingBox: [-1, 6, 6, -1],
    axis: true,
    xLabel: 'x',
    yLabel: 'f(x)',
    elements: [
      { type: 'function', expression: 'x^2/4+1', color: 'cyan', label: 'f' },
      { type: 'area', expression: 'x^2/4+1', domain: [1, 4], label: 'Aire', color: 'green' },
    ],
  },
  {
    engine: 'jsxgraph',
    title: 'Courbe d’Aston — annotation libre sur la figure',
    boundingBox: [0, 1, 250, -10],
    axis: true,
    xLabel: 'A',
    yLabel: 'E/A (MeV)',
    elements: [
      { type: 'function', expression: '-8.8*x/(x+12)', domain: [1, 240], color: 'cyan' },
      { type: 'text', points: [{ x: 110, y: -6.5 }], label: 'Fe : noyau le plus stable', color: 'yellow' },
    ],
  },
];

/** Une chute libre qui se LIT et se RÈGLE, pas une bille qui tombe. */
const SIMULATION: ScientificVisualSpec = {
  engine: 'matter',
  title: 'Chute libre — mesurer g',
  width: 600,
  height: 400,
  gravity: { x: 0, y: 1 },
  scale: 100,
  autoplay: true,
  bodies: [
    { id: 'sol', shape: 'rectangle', x: 300, y: 380, width: 560, height: 20, isStatic: true, label: 'Sol' },
    { id: 'bille', shape: 'circle', x: 300, y: 40, radius: 16, label: 'Bille', color: 'orange', restitution: 0.4 },
  ],
  measures: [
    { body: 'bille', quantity: 'height', label: 'Hauteur', unit: 'm', decimals: 2, origin: 370 },
    { body: 'bille', quantity: 'speed', label: 'Vitesse', unit: 'm/s', decimals: 2 },
    { quantity: 'time', label: 'Durée', unit: 's', decimals: 2 },
  ],
  parameters: [
    { target: 'gravity', label: 'Pesanteur', min: 0.2, max: 2, step: 0.1, value: 1 },
    { target: 'bille.restitution', label: 'Rebond', min: 0, max: 0.9, step: 0.05, value: 0.4 },
  ],
};

function Lab() {
  if (new URLSearchParams(window.location.search).get('scene') === 'muscle-backgrounds') {
    const musclePresets = ['svt_ch1_myogrammes', 'svt_ch1_glissement_sarcomere', 'svt_ch1_cycle_actomyosine', 'svt_ch1_chaleurs_muscle', 'svt_ch1_filieres_effort', 'svt_ch1_couplage_excitation_contraction'] as const;
    return <main style={{ background: '#10271d', padding: 16 }}>
      {musclePresets.map(presetId => <section key={presetId} style={{ height: 520, marginBottom: 20 }}>
        <ScientificVisual spec={{ engine: 'preset', presetId, step: 8, autoplay: false }} />
      </section>)}
      <section style={{ height: 520 }}><ScientificVisual spec={{ engine: 'three', model: 'muscle_excitation_contraction', step: 6, autoplay: false }} /></section>
    </main>;
  }
  if (new URLSearchParams(window.location.search).get('scene') === 'muscle-structure') {
    return <div style={{ width: '100%', height: '100dvh', padding: 8, background: '#10271d' }}>
      <ScientificVisual spec={{ engine: 'three', model: 'muscle_excitation_contraction', step: 0, labels: true, autoplay: false }} />
    </div>;
  }
  if (new URLSearchParams(window.location.search).get('scene') === 'glucose-journey') {
    return <div style={{ width: '100%', height: '100dvh', padding: 8 }}>
      <ScientificVisual spec={{ engine: 'preset', presetId: 'svt_ch1_schema_bilan_annote', step: 0, autoplay: false }} />
    </div>;
  }
  return (
    <div style={{ padding: 16, maxWidth: 820, margin: '0 auto' }}>
      {[...CAS, SIMULATION].map((spec, index) => (
        <div key={index} style={{ marginBottom: 24 }}>
          <ScientificVisual spec={spec} />
        </div>
      ))}
    </div>
  );
}

createRoot(document.getElementById('root')!).render(<Lab />);
