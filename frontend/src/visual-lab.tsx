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

function Lab() {
  return (
    <div style={{ padding: 16, maxWidth: 820, margin: '0 auto' }}>
      {CAS.map((spec, index) => (
        <div key={index} style={{ marginBottom: 24 }}>
          <ScientificVisual spec={spec} />
        </div>
      ))}
    </div>
  );
}

createRoot(document.getElementById('root')!).render(<Lab />);
