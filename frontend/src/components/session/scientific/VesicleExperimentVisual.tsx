import { useEffect, useId, useReducer, useRef } from 'react';
import VesiclePreparationVisual from './VesiclePreparationVisual';
import type { ScientificControlCommand, ScientificPresetVisualSpec, ScientificSimulationUpdate } from './types';
import { initialVesicleState, PREPARATION_DELAYS, TRIAL_DURATION, VESICLE_CASES, VESICLE_PRESET_ID, vesicleReducer, vesicleResult, vesicleVariant } from './vesicleExperimentModel';
import './vesicleExperiment.css';

interface Props {
  spec: ScientificPresetVisualSpec;
  transparent?: boolean;
  control?: ScientificControlCommand | null;
  onStateChange?: (update: ScientificSimulationUpdate) => void;
}

export default function VesicleExperimentVisual({ spec, transparent, control, onStateChange }: Props) {
  const [state, dispatch] = useReducer(vesicleReducer, spec, initialVesicleState);
  const previousControl = useRef<number | undefined>(undefined);
  const id = useId();
  const preparation = state.step < 4;
  const running = state.status === 'running';
  const result = vesicleResult(state);
  const variant = preparation ? 'scene' : vesicleVariant(state);
  const fmt = (value: number) => value.toLocaleString('fr-FR', { maximumFractionDigits: 1 });

  useEffect(() => {
    if (!control || control.presetId !== VESICLE_PRESET_ID || previousControl.current === control.sequence) return;
    const timer = window.setTimeout(() => {
      previousControl.current = control.sequence;
      dispatch({ type: 'control', control });
    }, 0);
    return () => window.clearTimeout(timer);
  }, [control]);

  useEffect(() => {
    if (!running) return;
    const timer = window.setTimeout(() => dispatch({ type: preparation ? 'tick' : 'finish' }), preparation ? PREPARATION_DELAYS[state.step] : TRIAL_DURATION);
    return () => window.clearTimeout(timer);
  }, [running, preparation, state.step, state.trial]);

  useEffect(() => {
    onStateChange?.({
      type: 'simulation_state', simulation_id: VESICLE_PRESET_ID,
      current_state: {
        simulation_status: state.status, preset_id: VESICLE_PRESET_ID, variant, step: state.step, max_step: 8,
        pHi: state.pHi, pHe: state.pHe, delta_pH: result.deltaPH,
        proton_direction: result.direction, atp_synthesis: !preparation && result.atpSynthesis,
        variants_completed: state.completed,
      },
      student_actions: [{ action: state.action, variant, step: state.step, pHi: state.pHi, pHe: state.pHe }],
      objective_progress: state.completed.length / VESICLE_CASES.length, timestamp: new Date().toISOString(),
    });
  }, [onStateChange, state, variant, preparation, result.deltaPH, result.direction, result.atpSynthesis]);

  const directionText = result.direction === 'outward' ? 'H⁺ : intérieur → extérieur' : result.direction === 'inward' ? 'H⁺ : extérieur → intérieur' : 'Aucun flux net de H⁺ lié au pH';

  return (
    <div className={`vesicle-experiment ${transparent ? '' : 'vesicle-experiment-framed'}`} data-scientific-preset={VESICLE_PRESET_ID}
      data-simulation-status={state.status} data-simulation-step={state.step} data-simulation-variant={variant} data-running={running}>
      {preparation ? <>
        <VesiclePreparationVisual key={state.step} step={state.step} running={running} />
        <div className="vesicle-experiment-buttons">
          <button onClick={() => dispatch({ type: running ? 'pause' : 'start' })}>{running ? 'Pause' : 'Démarrer'}</button>
          <button onClick={() => dispatch({ type: 'reset' })}>Revenir au début</button>
          <button disabled={state.step === 0} onClick={() => dispatch({ type: 'previous' })}>Étape précédente</button>
          <button onClick={() => dispatch({ type: 'next' })}>{state.step === 3 ? 'Ouvrir l’expérience →' : 'Étape suivante'}</button>
        </div>
      </> : <>
        <header className="vesicle-experiment-header">
          <p>Une vésicule, plusieurs gradients de pH</p>
          <div className="vesicle-experiment-cases" role="group" aria-label="Variantes du document 11">
            <span>pHi / pHe :</span>
            {VESICLE_CASES.map(example => <button key={example.id} aria-pressed={variant === example.id}
              onClick={() => dispatch({ type: 'variant', variant: example.id })}>{example.label}</button>)}
          </div>
        </header>
        <svg className="vesicle-experiment-scene" viewBox="0 0 720 290" role="img" aria-labelledby={`${id}-title ${id}-desc`}>
          <title id={`${id}-title`}>Vésicule retournée dans une solution tampon : pHi {fmt(state.pHi)}, pHe {fmt(state.pHe)}</title>
          <desc id={`${id}-desc`}>{directionText}. {result.atpSynthesis ? 'Synthèse d’ATP dans le modèle du document 11.' : 'Pas de synthèse d’ATP dans le modèle du document 11.'} Les sphères pédonculées sont orientées vers l’extérieur.</desc>
          <defs><marker id={`${id}-arrow`} viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10" fill="#fb7185" /></marker></defs>
          <g fontFamily="'Patrick Hand', 'Segoe Print', system-ui" fill="#e2e8f0">
            <text x="175" y="23" textAnchor="middle" fill="#67e8f9" fontSize="23">Solution tampon</text>
            <path d="M 39 34 H 311 L 301 50 V 263 Q 301 273 289 273 H 61 Q 49 273 49 261 V 50 Z" fill="#67e8f9" fillOpacity=".05" stroke="#cbd5e1" strokeWidth="3" />
            <path d="M 51 64 Q 70 60 92 64 T 136 64 T 180 64 T 224 64 T 268 64 T 299 64" fill="none" stroke="#67e8f9" strokeWidth="2" />
            <text x="62" y="88" fill="#67e8f9" fontSize="22">pHe {fmt(state.pHe)}</text>
            <g transform="translate(175 179)">
              <circle r="64" fill="#102c32" stroke="#c4b5fd" strokeWidth="4" />
              <circle r="56" fill="none" stroke="#8b7bb4" strokeWidth="2" />
              {Array.from({ length: 12 }, (_, index) => <g key={index} transform={`rotate(${index * 30})`} stroke="#93c5fd" strokeWidth="3">
                <path d="M 0 -64 V -74" /><circle cy="-79" r="6" fill="#93c5fd" />
              </g>)}
              <text y="12" textAnchor="middle" fill="#fde68a" fontSize="28">pHi {fmt(state.pHi)}</text>
            </g>
            {/* Particules symboliques : leur nombre n'est pas une concentration mesurée. */}
            {[...[[141,157],[202,213],[75,117],[275,232]], ...(result.deltaPH > 0 ? [[151,213],[209,157],[132,195],[218,193]] : result.deltaPH < 0 ? [[276,119],[77,235],[72,179],[278,180]] : [])].map(([x,y], i) => <circle key={i} cx={x} cy={y} r="4" fill="#fb7185" />)}
            {result.direction === 'none' && <text x="265" y="159" fill="#fda4af" fontSize="20">H⁺</text>}
            {result.direction !== 'none' && <>
              <path d={result.direction === 'outward' ? 'M 175 148 V 76' : 'M 175 76 V 148'} stroke="#fb7185" strokeWidth="3" fill="none" markerEnd={`url(#${id}-arrow)`} />
              <g key={`${state.trial}-${result.direction}`} className={result.direction === 'outward' ? 'vesicle-flow-out' : 'vesicle-flow-in'}>
                <circle cx="175" cy={result.direction === 'outward' ? 147 : 78} r="5" fill="#fda4af" />
              </g>
              <text x="194" y="133" fill="#fda4af" fontSize="20">H⁺</text>
            </>}
            {result.atpSynthesis && <text x="231" y="106" fill="#86efac" fontWeight="700" fontSize="22">ATP</text>}
            <text x="346" y="48" fill={result.atpSynthesis ? '#86efac' : '#fda4af'} fontSize="29" fontWeight="700">{result.atpSynthesis ? 'ATP synthétisé' : 'Pas d’ATP synthétisé'}</text>
            <text x="346" y="84" fontSize="23">{directionText}</text>
            <text x="346" y="121" fill="#fde68a" fontSize="23">ΔpH = pHe − pHi = {fmt(result.deltaPH)}</text>
            <text x="346" y="157" fontSize="22">{result.deltaPH > 0 ? 'Plus de H⁺ dedans que dehors.' : result.deltaPH < 0 ? 'Plus de H⁺ dehors que dedans.' : 'Même concentration en H⁺.'}</text>
            <text x="346" y="192" fontSize="21">{result.deltaPH > 0 ? 'Les H⁺ sortent par l’ATP synthase.' : result.deltaPH < 0 ? 'Gradient opposé à la synthèse.' : 'Pas de gradient de pH moteur.'}</text>
            <path d="M 252 179 H 324 V 232 H 341" stroke="#93c5fd" strokeWidth="1.5" fill="none" />
            <text x="346" y="238" fill="#93c5fd" fontSize="21">Sphères vers l’extérieur</text>
            <text x="346" y="272" fill="#bbf7d0" fontSize="21">ADP + Pi disponibles à l’extérieur</text>
          </g>
        </svg>
        <div className="vesicle-experiment-inputs">
          {(['pHi', 'pHe'] as const).map(key => <label key={key} htmlFor={`${id}-${key}`}>
            <span>{key === 'pHi' ? 'pHi · intérieur' : 'pHe · extérieur'} <output htmlFor={`${id}-${key}`}>{fmt(state[key])}</output></span>
            <input id={`${id}-${key}`} type="range" min="4" max="10" step="0.5" value={state[key]}
              onChange={event => dispatch({ type: 'parameters', parameters: { [key]: Number(event.target.value) } })} />
          </label>)}
        </div>
        <p className="vesicle-experiment-live" role="status" aria-live="polite">{result.atpSynthesis ? 'ATP synthétisé' : 'Pas d’ATP synthétisé'} · {directionText}</p>
        <div className="vesicle-experiment-buttons">
          <button onClick={() => dispatch({ type: running ? 'pause' : 'start' })}>{running ? 'Pause' : 'Rejouer le flux'}</button>
          <button onClick={() => dispatch({ type: 'reset' })}>Réinitialiser les pH</button>
          <button onClick={() => dispatch({ type: 'preparation' })}>Revoir la préparation</button>
        </div>
        <p className="vesicle-experiment-note">Modèle qualitatif du document 11 : membrane et ATP synthase intactes, ADP + Pi présents. Δψ et quantité d’ATP non simulés ; pH maintenus pendant l’observation.</p>
      </>}
    </div>
  );
}
