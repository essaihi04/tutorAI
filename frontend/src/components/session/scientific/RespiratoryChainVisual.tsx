import { useEffect, useId, useRef } from 'react';
import type { RespiratoryChainVariant } from './types';
import { RESPIRATORY_MAX_STEP, RESPIRATORY_YIELDS, respiratoryGradientFrame } from './respiratoryChainModel';
import { AtpReaction, DonorReaction, OxygenReaction } from './RespiratoryReactions';
import './respiratoryChain.css';

interface Props {
  variant: RespiratoryChainVariant;
  step: number;
  running: boolean;
  onVariant: (variant: RespiratoryChainVariant) => void;
  onToggleRunning: () => void;
  onReset: () => void;
  onNext: () => void;
  onSelectPhase: (step: number) => void;
}

const ELECTRON = '#42edff';
const PROTON = '#ff73c6';
const ATP = '#ffe34d';

const french = (value: number, decimals = 2) => value.toFixed(decimals).replace('.', ',');
const SAMPLE_COLUMNS = [205, 250, 295, 340, 385, 430, 530, 610, 650, 750, 790];

function ProtonSample({ count, y, compartment }: { count: number; y: number; compartment: string }) {
  return <g data-proton-sample={compartment} aria-label={`H⁺ dans ${compartment}`}>
    {Array.from({ length: count }, (_, index) => {
      const x = SAMPLE_COLUMNS[index % SAMPLE_COLUMNS.length];
      const cy = y + Math.floor(index / SAMPLE_COLUMNS.length) * 29;
      return <g key={index} data-proton-marker="true" className="rc-pool-proton" aria-hidden="true">
        <circle cx={x} cy={cy} r="13" fill={PROTON} />
        <text x={x} y={cy + 5} textAnchor="middle" fontSize="16" fontWeight="900" fill="#102523">H⁺</text>
      </g>;
    })}
  </g>;
}

function Particle({ path, label, color, delay = 0, duration = 3 }: {
  path: string; label: string; color: string; delay?: number; duration?: number;
}) {
  return <g className="rc-particle" aria-hidden="true">
    <circle r="15" fill={color} />
    <text textAnchor="middle" y="6" fill="#102523" fontSize="18" fontWeight="900">{label}</text>
    <animateMotion path={path} dur={`${duration}s`} begin={`${-delay}s`} repeatCount="indefinite" />
  </g>;
}

function Complex({ x, y, label, color, inactive = false, height = 113 }: {
  x: number; y: number; label: string; color: string; inactive?: boolean; height?: number;
}) {
  return <g opacity={inactive ? 0.3 : 1}>
    <rect x={x - 34} y={y} width="68" height={height} rx="24" fill={color} stroke={color} strokeWidth="4" />
    <path d={`M ${x - 24} ${y + 14} Q ${x} ${y + 2} ${x + 24} ${y + 14}`} stroke="white" strokeOpacity="0.6" strokeWidth="3" fill="none" />
    <text x={x - 4} y={y + height * 0.79} textAnchor="middle" fontSize="25" fontWeight="900" fill="#102523">{label}</text>
  </g>;
}

export default function RespiratoryChainVisual({ variant, step, running, onVariant, onToggleRunning, onReset, onNext, onSelectPhase }: Props) {
  const svg = useRef<SVGSVGElement>(null);
  const id = useId().replace(/:/g, '');
  const data = RESPIRATORY_YIELDS[variant];
  const isNadh = variant === 'nadh';
  const gradient = respiratoryGradientFrame(step);
  const { electrons, pumping, returning, makingAtp, relaxing } = gradient;
  const electronPath = `${isNadh ? 'M 130 260 Q 245 218 320 231' : 'M 257 265 Q 284 251 315 240'} Q 345 228 372 237 Q 421 261 462 229 Q 495 202 536 165 Q 572 145 604 173 Q 664 202 680 270`;
  const caption = step >= RESPIRATORY_MAX_STEP
    ? 'Équilibre du modèle : mêmes concentrations et mêmes pH. Le gradient électrochimique est dissipé : plus de synthèse d’ATP par cette voie.'
    : relaxing
      ? 'Pompage arrêté : les H⁺ reviennent par l’ATP synthase. Le déséquilibre diminue, les pH se rapprochent ; le rotor ralentit.'
      : step === 0
    ? `Prêt pour le relais ? ${data.donor} apporte une paire d’électrons.`
    : step < 4
      ? `${data.donor} → ${isNadh ? 'CI' : 'CII'} → Q → CIII → cyt c → CIV : suis les e⁻ !`
      : step < 7
        ? 'Les H⁺ s’accumulent en haut : concentration élevée, pH bas. Dans la matrice : concentration faible, pH plus élevé.'
        : step < 9
          ? 'Au bout du relais, O₂ accepte les électrons et forme de l’eau avec des H⁺ de la matrice.'
          : step < 11
            ? 'Les H⁺ reviennent vers la matrice par l’ATP synthase. Ce retour réduit le déséquilibre, mais la chaîne le renouvelle tant qu’elle pompe.'
            : `La tête F₁ produit l’ATP côté matrice. Bilan scolaire : ${data.atp} ATP par ${data.donor}. Le gradient reste entretenu par la chaîne.`;

  useEffect(() => {
    const element = svg.current;
    if (!element) return;
    const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
    const sync = () => {
      if (running && !preference.matches) element.unpauseAnimations();
      else element.pauseAnimations();
    };
    sync();
    preference.addEventListener('change', sync);
    return () => preference.removeEventListener('change', sync);
  }, [running, variant]);

  useEffect(() => {
    if (step === 0) svg.current?.setCurrentTime(0);
  }, [step, variant]);

  return <div className="respiratory-chain" data-running={running} data-respiratory-variant={variant} data-gradient-phase={gradient.phase} data-pumping={pumping} data-atp-active={makingAtp}>
    <div className="rc-toolbar" aria-label="Commandes de la chaîne respiratoire">
      <div className="rc-variants" role="group" aria-label="Donneur d’électrons">
        <button type="button" aria-pressed={isNadh} onClick={() => onVariant('nadh')}>NADH,H⁺</button>
        <button type="button" aria-pressed={!isNadh} onClick={() => onVariant('fadh2')}>FADH₂</button>
      </div>
      <button type="button" onClick={onToggleRunning}>{running ? '⏸ Pause' : step >= RESPIRATORY_MAX_STEP ? '↻ Rejouer' : '▶ Animer'}</button>
      <button type="button" onClick={onReset} aria-label="Revenir au début">↺ Début</button>
      <button type="button" onClick={onNext} disabled={step >= RESPIRATORY_MAX_STEP} aria-label="Étape suivante">Étape →</button>
    </div>
    <div className="rc-phases" role="group" aria-label="Étapes du gradient de protons">
      <button type="button" aria-pressed={gradient.phase === 'accumulation'} onClick={() => onSelectPhase(4)}>1 · Accumulation</button>
      <button type="button" aria-pressed={gradient.phase === 'return'} onClick={() => onSelectPhase(9)}>2 · Retour des H⁺</button>
      <button type="button" aria-pressed={relaxing} onClick={() => onSelectPhase(13)}>3 · Vers l’équilibre</button>
    </div>

    <svg key={variant} ref={svg} className="rc-diagram" viewBox="0 0 1000 570" role="group" aria-labelledby={`${id}-title`} aria-describedby={`${id}-desc`}>
      <title id={`${id}-title`}>Chaîne respiratoire et phosphorylation oxydative — {data.donor}</title>
      <desc id={`${id}-desc`}>Membrane interne mitochondriale. Les électrons entrent par le complexe {isNadh ? 'I' : 'II'}, puis passent par Q, III, le cytochrome c et IV vers O₂. {data.pumped} protons sont pompés par paire d’électrons. Leur accumulation rend l’espace intermembranaire plus acide que la matrice. Ils reviennent par l’ATP synthase, dont la tête F₁ produit l’ATP côté matrice. Bilan selon la convention scolaire : {data.atp} ATP par {data.donor}. Après arrêt du pompage, le gradient se dissipe progressivement. Les pH et concentrations sont illustratifs.</desc>
      <defs>
        {[['electron', ELECTRON], ['proton', PROTON], ['atp', ATP]].map(([name, color]) => <marker key={name} id={`${id}-${name}`} markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M 0 0 L 6 3 L 0 6 Z" fill={color} /></marker>)}
      </defs>

      <text x="22" y="30" fill={PROTON} fontSize="23" fontWeight="800">Espace intermembranaire</text>
      <text data-ph="intermembrane" x="22" y="60" fill={PROTON} fontSize="27" fontWeight="900">pH {french(gradient.intermembranePH)}</text>
      <text x="250" y="60" fill={PROTON} fontSize="22">{gradient.strength > 0 ? 'H⁺ élevés' : 'H⁺ équilibrés'}</text>
      {relaxing && <text x="978" y="30" textAnchor="end" fill={ATP} fontSize="22">Pompage arrêté</text>}
      <ProtonSample count={gradient.intermembraneParticles} y={100} compartment="espace intermembranaire" />

      {/* The two phospholipid leaflets remain transparent between their tails. */}
      <g stroke="#94c9be" strokeWidth="2" fill="none" opacity="0.65" aria-label="Bicouche de la membrane interne">
        {Array.from({ length: 49 }, (_, index) => {
          const x = 18 + index * 20;
          return <g key={x}>
            <circle cx={x} cy="197" r="8" /><path d={`M ${x - 4} 205 l -3 14 l 5 14 M ${x + 4} 205 l 3 14 l -5 14`} />
            <circle cx={x} cy="268" r="8" /><path d={`M ${x - 4} 260 l -3 -13 l 5 -13 M ${x + 4} 260 l 3 -13 l -5 -13`} />
          </g>;
        })}
      </g>
      <text x="30" y="308" fill="#b9dbd3" fontSize="19">Membrane interne</text>

      <Complex x={130} y={176} label="CI" color="#adf36a" inactive={!isNadh} />
      <Complex x={257} y={231} label="CII" color="#bba2ff" height={67} inactive={isNadh} />
      <Complex x={472} y={176} label="CIII" color="#6cf0b4" />
      <Complex x={680} y={176} label="CIV" color="#ffbc6b" />
      <circle cx="350" cy="231" r="26" fill={ELECTRON} />
      <text x="350" y="240" textAnchor="middle" fontSize="27" fontWeight="900" fill="#102523">Q</text>
      <ellipse cx="568" cy="158" rx="35" ry="24" fill={ELECTRON} />
      <text x="568" y="164" textAnchor="middle" fontSize="19" fontWeight="900" fill="#102523">cyt c</text>

      <g opacity={electrons ? 1 : 0.3}>
        <path data-flow="electrons" d={electronPath} stroke={ELECTRON} strokeWidth="4" fill="none" markerEnd={`url(#${id}-electron)`} />
        {electrons && step >= 2 && step < 7 && [0, 0.45].map(delay => <Particle key={delay} path={electronPath} label="e⁻" color={ELECTRON} duration={7} delay={delay} />)}
      </g>
      <DonorReaction step={step} donor={data.donor} oxidized={data.oxidized} isNadh={isNadh} onReplay={() => onSelectPhase(0)} />
      <text x="257" y="329" textAnchor="middle" fill="#d3c4ff" fontSize="19">0 H⁺ pompé</text>

      {[{ x: 130, count: 4, enabled: isNadh }, { x: 472, count: 4, enabled: true }, { x: 680, count: 2, enabled: true }].map(pump => <g key={pump.x} opacity={pump.enabled && !relaxing ? 1 : 0.2}>
        <path data-flow={pump.enabled ? 'proton-pump' : 'inactive-pump'} d={`M ${pump.x + 18} 281 L ${pump.x + 18} 96`} stroke={PROTON} strokeWidth="4" fill="none" strokeDasharray={pumping && pump.enabled ? undefined : '6 6'} markerEnd={`url(#${id}-proton)`} />
        <text x={pump.x + 18} y="163" textAnchor="middle" fill={PROTON} fontSize="25" fontWeight="800">{pump.enabled ? pump.count : 0} H⁺</text>
        {pumping && pump.enabled && <Particle path={`M ${pump.x + 18} 278 L ${pump.x + 18} 99`} label="H⁺" color={PROTON} delay={pump.x / 200} duration={2.8} />}
      </g>)}

      <OxygenReaction step={step} onReplay={() => onSelectPhase(6)} />

      {/* F₀ spans the membrane. The catalytic F₁ head is in the MATRIX.
          Only the central rotor turns, never the whole catalytic sphere. */}
      <rect x="836" y="179" width="48" height="101" rx="18" fill="#64ead3" stroke="#b5fff0" strokeWidth="3" />
      <path d="M 839 258 L 824 333 M 881 258 L 896 333" stroke="#a6f5db" strokeWidth="6" fill="none" />
      <rect x="854" y="264" width="12" height="63" rx="6" fill={ATP} />
      <ellipse cx="860" cy="343" rx="57" ry="32" fill="#64ead3" stroke="#b5fff0" strokeWidth="3" />
      <text x="935" y="210" fill="#b5fff0" fontSize="21">F₀</text>
      <text x="939" y="350" fill="#b5fff0" fontSize="21">F₁</text>
      <g opacity={returning ? 1 : 0.35}>
        <path data-flow="proton-return" d="M 860 89 L 860 308 Q 912 321 932 365" stroke={PROTON} strokeWidth="5" fill="none" markerEnd={`url(#${id}-proton)`} />
        {returning && <Particle path="M 860 96 L 860 300 Q 916 320 932 365" label="H⁺" color={PROTON} duration={2.5 / Math.max(0.25, gradient.strength)} />}
      </g>
      <g transform="translate(860 343)" aria-label="Rotor de l’ATP synthase">
        <g>
          <path d="M 0 0 L 0 -22 M 0 0 L 19 11 M 0 0 L -19 11" stroke={ATP} strokeWidth="7" strokeLinecap="round" />
          {returning && <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur={`${2.5 / Math.max(0.25, gradient.strength)}s`} repeatCount="indefinite" />}
        </g>
      </g>
      <text x="885" y="60" textAnchor="middle" fill="#b5fff0" fontSize="22" fontWeight="800">ATP synthase</text>
      <text x="860" y="390" textAnchor="middle" fill="#b5fff0" fontSize="19">Sphère pédonculée</text>
      <AtpReaction step={step} active={makingAtp} onReplay={() => onSelectPhase(9)} />

      <text x="22" y="470" fill="#adf36a" fontSize="25" fontWeight="800">Matrice mitochondriale</text>
      <text data-ph="matrix" x="22" y="501" fill="#adf36a" fontSize="27" fontWeight="900">pH {french(gradient.matrixPH)}</text>
      <text x="250" y="501" fill="#adf36a" fontSize="22">{gradient.strength > 0 ? 'H⁺ faibles' : 'H⁺ équilibrés'}</text>
      <ProtonSample count={gradient.matrixParticles} y={526} compartment="matrice" />
    </svg>

    <div className="rc-gradient" aria-label="Mesure du gradient de pH">
      <strong>ΔpH = {french(gradient.deltaPH)}</strong>
      <meter aria-label="Différence de pH entre matrice et espace intermembranaire" min="0" max="1" value={gradient.deltaPH} />
      <span className="rc-yield"><strong>{data.atp} ATP</strong><span> / {data.donor} · bilan scolaire</span></span>
    </div>
    <p className="sr-only" aria-live="polite">{caption}</p>
    <div className="rc-footnote">
      <span><i style={{ background: ELECTRON }} /> e⁻</span>
      <span><i style={{ background: PROTON }} /> H⁺</span>
      <span><i style={{ background: ATP }} /> ATP</span>
      <span>pH indicatifs · Cliquer sur les molécules pour rejouer</span>
    </div>
  </div>;
}
