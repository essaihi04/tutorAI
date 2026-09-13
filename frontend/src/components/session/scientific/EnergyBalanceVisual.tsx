import { useId, useState } from 'react';
import { ENERGY_PHASES, energyBalance, energyExplanation, energyNumber, energyPhase } from './energyBalanceModel';
import type { EnergyBalanceVariant } from './energyBalanceModel';
import './energyBalance.css';

interface Props {
  step: number;
  running: boolean;
  variant: EnergyBalanceVariant;
  onSelectPhase: (step: number) => void;
  onVariant: (variant: EnergyBalanceVariant) => void;
  onToggleRunning: () => void;
  onReset: () => void;
  onNext: () => void;
}

const GREEN = '#6ee7ad';
const BLUE = '#7dd3fc';
const GOLD = '#fde68a';

function ATP({ x, y, count, label = 'ATP', large = false }: { x: number; y: number; count: number; label?: string; large?: boolean }) {
  return <g transform={`translate(${x} ${y})`} className="energy-appear">
    <rect x={large ? -77 : -58} y="-27" width={large ? 154 : 116} height="54" rx="27" fill="#103c32" stroke={GREEN} strokeWidth="1.5" />
    <path d="M-36 -14 -47 2 -38 2 -43 15 -26 -5 -36 -5Z" transform={large ? 'translate(-17 0)' : undefined} fill={GREEN} />
    <text x="12" y="7" fill={GREEN} fontSize={large ? 28 : 23} fontWeight="700" textAnchor="middle">{count} {label}</text>
  </g>;
}

function CarbonGroup({ x, y, count }: { x: number; y: number; count: number }) {
  return <g transform={`translate(${x} ${y})`}>
    {Array.from({ length: count }, (_, i) => <circle key={i} cx={(i % 3) * 20 - 20} cy={Math.floor(i / 3) * 22 - (count === 6 ? 11 : 0)} r="8" fill={GOLD} />)}
  </g>;
}

function Mitochondrion() {
  return <g>
    <path d="M152 122 C138 47 235 41 288 63 C344 83 423 24 464 91 C510 173 389 234 309 218 C229 201 170 214 152 122Z" fill="#21263b" stroke="#a5b4fc" strokeWidth="3" />
    <path d="M174 123 C160 71 218 56 254 77 L238 127 Q233 144 250 143 L289 96 Q300 84 309 100 L295 155 Q294 171 311 158 L352 100 Q364 84 374 99 L359 161 Q360 181 376 168 L414 95 Q438 62 451 101 C476 156 390 211 314 196 C242 182 193 201 174 123Z" fill="none" stroke="#818cf8" strokeWidth="2" />
  </g>;
}

function Scene({ step, phase, variant, marker }: { step: number; phase: number; variant: EnergyBalanceVariant; marker: string }) {
  const b = energyBalance(variant);
  const arrow = `url(#${marker})`;
  const line = { stroke: BLUE, strokeWidth: 2.5, fill: 'none', markerEnd: arrow };
  if (phase === 0) return <>
    <text x="300" y="29" className="energy-location">DANS LE CYTOPLASME</text>
    <CarbonGroup x={114} y={119} count={6} />
    <text x="114" y="170">1 glucose</text>
    <path d="M158 118 H215 M215 118 Q236 118 248 90 M215 118 Q236 118 248 145" {...line} />
    <g className="energy-appear"><CarbonGroup x={295} y={83} count={3} /><CarbonGroup x={295} y={145} count={3} />
      <text x="295" y="190">2 pyruvates</text></g>
    {step >= 1 && <><path d="M346 105 H406" {...line} /><ATP x={480} y={106} count={2} label="nets" />
      <text x="480" y="151" fill={GREEN}>ATP directs</text></>}
    {step >= 2 && <g className="energy-appear"><rect x="365" y="202" width="212" height="38" rx="19" fill="#122e42" stroke={BLUE} />
      <text x="471" y="227" fill={BLUE}>2 NADH,H⁺ → chaîne</text></g>}
    <text x="115" y="237" className="energy-small">● = un carbone</text>
  </>;
  if (phase === 1) return <>
    <text x="300" y="27" className="energy-location">DANS LA MATRICE</text>
    <Mitochondrion />
    <g transform="translate(305 134)">
      <circle r="40" fill="#151f31" stroke={GOLD} strokeWidth="2.5" strokeDasharray="216 35" className="energy-cycle" />
      <path d="M34 -23 44 -18 43 -32Z" fill={GOLD} />
      <text y="6" fill={GOLD}>Krebs</text>
    </g>
    <CarbonGroup x={60} y={112} count={3} /><text x="67" y="159" fontSize="15">2 pyruvates</text>
    <path d="M96 110 H157" {...line} />
    {step >= 4 && <><path d="M448 124 H477" {...line} /><ATP x={534} y={124} count={2} /></>}
    {step >= 5 && <g className="energy-appear">
      <rect x="154" y="237" width="298" height="35" rx="17" stroke={BLUE} fill="#122e42" />
      <text x="303" y="260" fill={BLUE}>8 NADH,H⁺ + 2 FADH₂ → chaîne</text>
    </g>}
  </>;
  if (phase === 2) return <>
    <text x="300" y="27" className="energy-location">MEMBRANE INTERNE</text>
    <rect x="285" y="57" width="35" height="174" rx="16" fill="#302948" stroke="#c4b5fd" />
    {Array.from({ length: 10 }, (_, i) => <g key={i}><circle cx="285" cy={64 + i * 17} r="5" fill="#c4b5fd" /><circle cx="320" cy={64 + i * 17} r="5" fill="#c4b5fd" /></g>)}
    <text x="121" y="87" fill={BLUE}>10 NADH,H⁺</text>
    <text x="121" y="185" fill={GOLD}>2 FADH₂</text>
    <path d="M96 114 H263 M96 208 H263" {...line} className="energy-flow" />
    <rect x="266" y="114" width="74" height="49" rx="14" fill="#21665c" stroke={GREEN} strokeWidth="2" />
    <path d="M340 139 H365" stroke={GREEN} strokeWidth="9" />
    <ellipse cx="378" cy="139" rx="24" ry="34" fill="#21665c" stroke={GREEN} strokeWidth="2" />
    <text x="453" y="85" className="energy-small">ADP + Pi</text>
    <path d="M447 95 Q417 119 433 137" {...line} />
    {step >= 7 && <ATP x={491} y={161} count={b.chainATP} large />}
    <text x="361" y="263" fontSize="16">Chaîne + ATP synthase</text>
  </>;
  if (phase === 3) return <>
    <text x="300" y="26" className="energy-location">UN SEUL TOTAL · PAR GLUCOSE</text>
    {[['Glycolyse', 105, 2], ['Matrice', 300, 2], ['Chaîne', 495, b.chainATP]].map(([label, x, count]) =>
      <g key={label}>
        <text x={Number(x)} y="70">{label}</text><ATP x={Number(x)} y={110} count={Number(count)} />
        <path d={`M${x} 146 Q${x} 192 300 200`} {...line} className="energy-flow" />
      </g>)}
    <text x="202" y="117" fontSize="24" fill={BLUE}>+</text><text x="398" y="117" fontSize="24" fill={BLUE}>+</text>
    <ATP x={300} y={233} count={b.totalATP} large />
    <text x="96" y="243" className="energy-small">4 ATP directs</text>
    <text x="497" y="243" className="energy-small">{b.chainATP} via la chaîne</text>
  </>;
  return <>
    <text x="300" y="25" className="energy-location">MÊME ÉNERGIE DE DÉPART · 2 860 kJ/mol DE GLUCOSE</text>
    {[{ y: 73, name: 'Respiration', atp: b.totalATP, percent: b.respirationPercent },
      { y: 178, name: 'Fermentation', atp: 2, percent: b.fermentationPercent }].map(row =>
      <g key={row.name}>
        <text x="30" y={row.y} textAnchor="start">{row.name}</text>
        <text x="571" y={row.y} textAnchor="end" fill={GREEN} fontWeight="700">{row.atp} ATP</text>
        <rect x="30" y={row.y + 15} width="450" height="32" rx="7" fill="#394751" />
        <rect x="30" y={row.y + 15} width={450 * row.percent / 100} height="32" rx="4" fill={GREEN} className="energy-bar" />
        <text x="573" y={row.y + 39} textAnchor="end" fill={GREEN} fontSize="23" fontWeight="700">{energyNumber(row.percent, row.atp === 2 ? 2 : 1)} %</text>
      </g>)}
    <circle cx="38" cy="266" r="5" fill={GREEN} /><text x="50" y="272" textAnchor="start" className="energy-small">Énergie en ATP</text>
    <circle cx="234" cy="266" r="5" fill="#82929e" /><text x="246" y="272" textAnchor="start" className="energy-small">Chaleur / énergie restante</text>
  </>;
}

function Explanation({ phase, variant, onPause }: { phase: number; variant: EnergyBalanceVariant; onPause: () => void }) {
  const [open, setOpen] = useState(false);
  const id = useId();
  return <div className="energy-explanation">
    <button type="button" aria-expanded={open} aria-controls={id} onClick={() => { if (!open) onPause(); setOpen(!open); }}>
      {open ? '✕ Fermer' : '? Comprendre'}
    </button>
    {open && <div id={id} className="energy-detail" role="region" aria-label="Explication de l’étape">{energyExplanation(phase, variant)}</div>}
  </div>;
}

export default function EnergyBalanceVisual(props: Props) {
  const { step, running, variant, onSelectPhase, onToggleRunning, onReset, onNext, onVariant } = props;
  const phase = energyPhase(step);
  const marker = useId().replace(/:/g, '');
  const captions = ['Le glucose se scinde et libère un premier gain.', 'La matrice prépare les transporteurs d’électrons.',
    'L’énergie des transporteurs sert à fabriquer l’ATP.', 'On additionne l’ATP, pas les transporteurs.', 'La respiration conserve bien plus d’énergie dans l’ATP.'];
  return <section className="energy-balance" data-running={running} data-energy-phase={phase} aria-label="Bilan énergétique interactif">
    <nav className="energy-phases" aria-label="Étapes du bilan">
      {ENERGY_PHASES.map((item, i) => <button type="button" key={item.step} aria-current={phase === i ? 'step' : undefined}
        onClick={() => onSelectPhase(item.step)}><span>{i + 1}</span>{item.label}</button>)}
    </nav>
    <div className="energy-stage">
      <svg viewBox="0 0 600 290" role="img" aria-labelledby={`${marker}-title ${marker}-desc`}>
        <title id={`${marker}-title`}>{ENERGY_PHASES[phase].label} — bilan énergétique</title>
        <desc id={`${marker}-desc`}>{energyExplanation(phase, variant)}</desc>
        <defs><marker id={marker} markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 6 3 0 6" fill={BLUE} /></marker></defs>
        <g key={phase} className="energy-scene"><Scene step={step} phase={phase} variant={variant} marker={marker} /></g>
      </svg>
    </div>
    <div className="energy-caption"><p aria-live="polite">{captions[phase]}</p>
      <Explanation key={`${phase}-${variant}`} phase={phase} variant={variant} onPause={() => { if (running) onToggleRunning(); }} />
    </div>
    <footer className="energy-controls">
      <button type="button" onClick={onToggleRunning}>{running ? 'Ⅱ Pause' : step >= 10 ? '↻ Rejouer' : '▶ Lire'}</button>
      <button type="button" onClick={onReset} aria-label="Revenir au début">↺</button>
      <button type="button" onClick={onNext} disabled={step >= 10} aria-label="Étape suivante">→</button>
      <label>Convention du cours <select value={variant} onChange={e => onVariant(e.target.value as EnergyBalanceVariant)} aria-label="Convention du bilan ATP">
        <option value="scene">38 ATP</option><option value="navette_36">36 ATP · navette</option>
      </select></label>
    </footer>
  </section>;
}
