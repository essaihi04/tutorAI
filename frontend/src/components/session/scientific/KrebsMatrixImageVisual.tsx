interface KrebsMatrixImageVisualProps {
  step: number;
  transparent?: boolean;
}

interface CycleMolecule {
  name: string;
  carbons: number;
  x: number;
  y: number;
}

interface KrebsReaction {
  title: string;
  inputs: string[];
  outputs: string[];
  note: string;
}

const MATRIX_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_double_membrane_zoom.png';
const ACETYL_COLOR = '#fb923c';
const SKELETON_COLOR = '#22d3ee';

const CYCLE_MOLECULES: CycleMolecule[] = [
  { name: 'Citrate', carbons: 6, x: 450, y: 80 },
  { name: 'Isocitrate', carbons: 6, x: 680, y: 140 },
  { name: 'α-cétoglutarate', carbons: 5, x: 790, y: 265 },
  { name: 'Succinyl-CoA', carbons: 4, x: 680, y: 390 },
  { name: 'Succinate', carbons: 4, x: 450, y: 450 },
  { name: 'Fumarate', carbons: 4, x: 220, y: 390 },
  { name: 'Malate', carbons: 4, x: 110, y: 265 },
  { name: 'Oxaloacétate', carbons: 4, x: 220, y: 140 },
];

const ACETYL_START: CycleMolecule = { name: 'Acétyl-CoA', carbons: 2, x: 82, y: 74 };

const REACTIONS: KrebsReaction[] = [
  {
    title: '1 · Condensation : C₂ + C₄ → C₆',
    inputs: ['Acétyl-CoA', 'H₂O'],
    outputs: ['CoA-SH'],
    note: 'L’acétyl-CoA rejoint l’oxaloacétate : le cycle commence.',
  },
  {
    title: '2 · Isomérisation : C₆ → C₆',
    inputs: [],
    outputs: [],
    note: 'Le squelette carboné est réorganisé sans perte de carbone.',
  },
  {
    title: '3 · Décarboxylation oxydative : C₆ → C₅',
    inputs: ['NAD⁺'],
    outputs: ['CO₂', 'NADH,H⁺'],
    note: 'Un CO₂ sort et le NAD⁺ est réduit.',
  },
  {
    title: '4 · Décarboxylation oxydative : C₅ → C₄',
    inputs: ['NAD⁺', 'CoA-SH'],
    outputs: ['CO₂', 'NADH,H⁺'],
    note: 'Un second CO₂ sort : le squelette revient à quatre carbones.',
  },
  {
    title: '5 · Phosphorylation au niveau du substrat',
    inputs: ['GDP + Pi'],
    outputs: ['GTP ≈ ATP', 'CoA-SH'],
    note: 'L’énergie de la réaction permet de former un GTP.',
  },
  {
    title: '6 · Déshydrogénation',
    inputs: ['FAD'],
    outputs: ['FADH₂'],
    note: 'Le FAD capte des hydrogènes et des électrons.',
  },
  {
    title: '7 · Hydratation',
    inputs: ['H₂O'],
    outputs: [],
    note: 'Une molécule d’eau entre dans la réaction.',
  },
  {
    title: '8 · Déshydrogénation finale',
    inputs: ['NAD⁺'],
    outputs: ['NADH,H⁺'],
    note: 'L’oxaloacétate C₄ est régénéré : le cycle peut recommencer.',
  },
];

function arrowHead(x1: number, y1: number, x2: number, y2: number) {
  const angle = Math.atan2(y2 - y1, x2 - x1);
  const size = 10;
  return `${x2},${y2} ${x2 - size * Math.cos(angle - Math.PI / 6)},${y2 - size * Math.sin(angle - Math.PI / 6)} ${x2 - size * Math.cos(angle + Math.PI / 6)},${y2 - size * Math.sin(angle + Math.PI / 6)}`;
}

function CycleArrow({ from, to, active }: {
  from: Pick<CycleMolecule, 'x' | 'y'>;
  to: Pick<CycleMolecule, 'x' | 'y'>;
  active: boolean;
}) {
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  const length = Math.max(1, Math.hypot(dx, dy));
  const x1 = from.x + (dx / length) * 66;
  const y1 = from.y + (dy / length) * 40;
  const x2 = to.x - (dx / length) * 66;
  const y2 = to.y - (dy / length) * 40;
  const color = active ? '#fef08a' : '#94a3b8';

  return (
    <g opacity={active ? 1 : 0.55}>
      <line
        x1={x1}
        y1={y1}
        x2={x2}
        y2={y2}
        stroke={color}
        strokeWidth={active ? 5 : 3}
        strokeDasharray={active ? undefined : '7 7'}
        strokeLinecap="round"
      />
      <polygon points={arrowHead(x1, y1, x2, y2)} fill={color} />
    </g>
  );
}

function MoleculeNode({ molecule, active }: { molecule: CycleMolecule; active: boolean }) {
  const width = molecule.name.length > 12 ? 134 : 112;
  return (
    <g>
      <rect
        x={molecule.x - width / 2}
        y={molecule.y - 27}
        width={width}
        height="40"
        rx="12"
        fill={active ? '#083344ee' : '#07111fdd'}
        stroke={active ? '#67e8f9' : '#64748b'}
        strokeWidth={active ? 3 : 1.5}
      />
      <text x={molecule.x} y={molecule.y - 9} textAnchor="middle" fill={active ? '#cffafe' : '#e2e8f0'} fontSize="14" fontWeight="800">
        {molecule.name}
      </text>
      <text x={molecule.x} y={molecule.y + 7} textAnchor="middle" fill={active ? '#fef08a' : '#94a3b8'} fontSize="13" fontWeight="800">
        C{molecule.carbons}
      </text>
    </g>
  );
}

function MovingCarbonChain({ molecule }: { molecule: CycleMolecule }) {
  const gap = 17;
  const startX = -((molecule.carbons - 1) * gap) / 2;

  return (
    <g
      style={{
        transform: `translate(${molecule.x}px, ${molecule.y + 29}px)`,
        transition: 'transform 900ms cubic-bezier(0.22, 1, 0.36, 1)',
      }}
      aria-label={`${molecule.name}, ${molecule.carbons} carbones`}
    >
      {Array.from({ length: molecule.carbons }, (_, index) => {
        const acetylCarbon = index < Math.min(2, molecule.carbons);
        const color = acetylCarbon ? ACETYL_COLOR : SKELETON_COLOR;
        return (
          <g key={index}>
            <circle cx={startX + index * gap} cy="0" r="8" fill="#07111f" stroke={color} strokeWidth="3" />
            <text x={startX + index * gap} y="4" textAnchor="middle" fill="#fff" fontSize="9" fontWeight="900">C</text>
          </g>
        );
      })}
    </g>
  );
}

function ReactionTag({ x, y, text, color }: { x: number; y: number; text: string; color: string }) {
  const width = Math.max(76, Math.min(124, text.length * 8 + 22));
  return (
    <g>
      <rect x={x - width / 2} y={y - 17} width={width} height="31" rx="10" fill="#07111fee" stroke={color} strokeWidth="2" />
      <text x={x} y={y + 3} textAnchor="middle" fill={color} fontSize="13" fontWeight="800">{text}</text>
    </g>
  );
}

function ReactionExchange({ from, to, reaction }: {
  from: CycleMolecule;
  to: CycleMolecule;
  reaction: KrebsReaction;
}) {
  const midpoint = { x: (from.x + to.x) / 2, y: (from.y + to.y) / 2 };
  const radialX = midpoint.x - 450;
  const radialY = midpoint.y - 265;
  const radialLength = Math.max(1, Math.hypot(radialX, radialY));
  const ux = radialX / radialLength;
  const uy = radialY / radialLength;
  const tx = -uy;
  const ty = ux;
  const clampX = (value: number) => Math.max(72, Math.min(828, value));
  const clampY = (value: number) => Math.max(66, Math.min(470, value));
  const inputBase = { x: midpoint.x - ux * 66, y: midpoint.y - uy * 66 };
  const outputBase = { x: midpoint.x + ux * 72, y: midpoint.y + uy * 72 };

  if (reaction.inputs.length === 0 && reaction.outputs.length === 0) {
    return <ReactionTag x={midpoint.x} y={midpoint.y} text="réarrangement" color="#fef08a" />;
  }

  return (
    <g>
      {reaction.inputs.map((input, index) => {
        const spread = (index - (reaction.inputs.length - 1) / 2) * 64;
        const x = clampX(inputBase.x + tx * spread);
        const y = clampY(inputBase.y + ty * spread);
        const arrowEndX = midpoint.x - ux * 18;
        const arrowEndY = midpoint.y - uy * 18;
        return (
          <g key={`input-${input}`}>
            <line x1={x} y1={y} x2={arrowEndX} y2={arrowEndY} stroke="#67e8f9" strokeWidth="3" strokeLinecap="round" />
            <polygon points={arrowHead(x, y, arrowEndX, arrowEndY)} fill="#67e8f9" />
            <ReactionTag x={x} y={y} text={input} color="#67e8f9" />
          </g>
        );
      })}
      {reaction.outputs.map((output, index) => {
        const spread = (index - (reaction.outputs.length - 1) / 2) * 70;
        const x = clampX(outputBase.x + tx * spread);
        const y = clampY(outputBase.y + ty * spread);
        const isCo2 = output === 'CO₂';
        const color = isCo2 ? ACETYL_COLOR : '#f0abfc';
        const arrowStartX = midpoint.x + ux * 18;
        const arrowStartY = midpoint.y + uy * 18;
        const arrowEndX = midpoint.x + (x - midpoint.x) * 0.68;
        const arrowEndY = midpoint.y + (y - midpoint.y) * 0.68;
        return (
          <g key={`output-${output}`}>
            <line x1={arrowStartX} y1={arrowStartY} x2={arrowEndX} y2={arrowEndY} stroke={color} strokeWidth="3" strokeLinecap="round" />
            <polygon points={arrowHead(arrowStartX, arrowStartY, arrowEndX, arrowEndY)} fill={color} />
            <ReactionTag x={x} y={y} text={output} color={color} />
          </g>
        );
      })}
    </g>
  );
}

function cumulativeBilan(step: number) {
  return {
    co2: (step >= 3 ? 1 : 0) + (step >= 4 ? 1 : 0),
    nadh: (step >= 3 ? 1 : 0) + (step >= 4 ? 1 : 0) + (step >= 8 ? 1 : 0),
    fadh2: step >= 6 ? 1 : 0,
    gtp: step >= 5 ? 1 : 0,
  };
}

export default function KrebsMatrixImageVisual({ step, transparent }: KrebsMatrixImageVisualProps) {
  const current = Math.max(0, Math.min(8, Math.round(step)));
  const reaction = current > 0 ? REACTIONS[current - 1] : null;
  const activeMolecule: CycleMolecule = current === 0 ? ACETYL_START : CYCLE_MOLECULES[current - 1];
  const activeEdge = current > 0 ? current - 1 : -1;
  const bilan = cumulativeBilan(current);

  return (
    <figure className={transparent ? 'relative my-0 h-full w-full p-0' : 'relative my-3 h-full min-h-[500px] overflow-hidden rounded-xl border border-white/10 bg-slate-950/70 p-2'}>
      <div className="relative mx-auto h-full min-h-[480px] w-full max-w-[1020px] overflow-hidden rounded-lg">
        <img src={MATRIX_IMAGE} alt="Grande vue de la matrice mitochondriale" className="absolute inset-0 h-full w-full object-cover" />
        <div className="absolute inset-0 bg-slate-950/55" />

        <svg viewBox="0 0 900 570" preserveAspectRatio="xMidYMid meet" className="absolute inset-x-0 top-0 w-full" style={{ height: 'calc(100% - 96px)' }} role="img" aria-label="Cycle circulaire de Krebs animé dans la matrice mitochondriale">
          <rect x="202" y="8" width="496" height="38" rx="13" fill="#07111fee" stroke="#67e8f999" strokeWidth="2" />
          <text x="450" y="33" textAnchor="middle" fill="#fef08a" fontSize="18" fontWeight="800">
            {reaction ? reaction.title : 'Départ · l’acétyl-CoA C₂ entre dans le cycle'}
          </text>

          <ellipse cx="450" cy="265" rx="355" ry="205" fill="#02061755" stroke="#67e8f977" strokeWidth="3" strokeDasharray="9 8" />

          {CYCLE_MOLECULES.map((molecule, index) => {
            const next = CYCLE_MOLECULES[(index + 1) % CYCLE_MOLECULES.length];
            return <CycleArrow key={`arrow-${molecule.name}`} from={molecule} to={next} active={activeEdge === (index + 1) % 8} />;
          })}

          <line x1="142" y1="90" x2="378" y2="91" stroke={current <= 1 ? ACETYL_COLOR : '#94a3b8'} strokeWidth={current <= 1 ? 4 : 2} strokeDasharray="7 6" />
          <polygon points={arrowHead(142, 90, 378, 91)} fill={current <= 1 ? ACETYL_COLOR : '#94a3b8'} />

          {CYCLE_MOLECULES.map((molecule, index) => (
            <MoleculeNode key={molecule.name} molecule={molecule} active={current === index + 1} />
          ))}

          <MovingCarbonChain molecule={activeMolecule} />

          {reaction && (
            <ReactionExchange
              from={CYCLE_MOLECULES[(current + 6) % 8]}
              to={CYCLE_MOLECULES[current - 1]}
              reaction={reaction}
            />
          )}
          {!reaction && <ReactionTag x={255} y={102} text="Démarrer" color="#fef08a" />}

          <rect x="190" y="501" width="520" height="29" rx="9" fill="#07111fee" stroke="#cbd5e155" />
          <circle cx="212" cy="515" r="7" fill="#07111f" stroke={ACETYL_COLOR} strokeWidth="3" />
          <text x="226" y="520" fill="#fed7aa" fontSize="12" fontWeight="700">C de l’acétyl-CoA → CO₂ lors de tours ultérieurs</text>
          <circle cx="520" cy="515" r="7" fill="#07111f" stroke={SKELETON_COLOR} strokeWidth="3" />
          <text x="534" y="520" fill="#cffafe" fontSize="12" fontWeight="700">Autres carbones</text>
          <text x="450" y="551" textAnchor="middle" fill="#e2e8f0" fontSize="12" fontWeight="700">
            {reaction?.note ?? 'Les deux carbones orange entrent avec l’acétyl-CoA.'}
          </text>
        </svg>

        <div className="absolute bottom-2 left-3 right-3 overflow-hidden rounded-xl border border-cyan-300/35 bg-slate-950/95 text-center text-[10px] text-slate-100 sm:text-xs">
          <div className="border-b border-cyan-300/25 px-2 py-1 font-bold text-cyan-200">Bilan cumulatif du cycle de Krebs</div>
          <table className="w-full table-fixed border-collapse">
            <thead className="text-[9px] uppercase tracking-wide text-slate-300 sm:text-[10px]">
              <tr>
                <th className="px-1 py-1">Calcul</th>
                <th className="px-1 py-1">ATP ≈ GTP</th>
                <th className="px-1 py-1">NADH,H⁺</th>
                <th className="px-1 py-1">FADH₂</th>
                <th className="px-1 py-1">CO₂</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-t border-white/10 font-bold">
                <th className="px-1 py-1 text-cyan-200">Tour affiché</th>
                <td className="px-1 py-1 text-yellow-300">{bilan.gtp}</td>
                <td className="px-1 py-1 text-violet-300">{bilan.nadh}</td>
                <td className="px-1 py-1 text-pink-300">{bilan.fadh2}</td>
                <td className="px-1 py-1 text-orange-300">{bilan.co2}</td>
              </tr>
              <tr className={`border-t border-white/10 ${current >= 8 ? 'font-extrabold text-white' : 'text-slate-500'}`}>
                <th className="px-1 py-1">1 glucose · 2 tours</th>
                <td className="px-1 py-1">2</td>
                <td className="px-1 py-1">6</td>
                <td className="px-1 py-1">2</td>
                <td className="px-1 py-1">4</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      {!transparent && <figcaption className="px-2 pt-2 text-xs text-slate-300">Un tour du cycle par acétyl-CoA ; deux tours pour un glucose.</figcaption>}
    </figure>
  );
}
