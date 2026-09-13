import type { ScientificControlCommand, ScientificPresetVisualSpec, VesicleParameters } from './types';

export const VESICLE_PRESET_ID = 'svt_ch1_vesicules_atp_synthase' as const;
export const VESICLE_CASES = [
  { id: 'acide_externe', label: '6 / 4', pHi: 6, pHe: 4, step: 4 },
  { id: 'equilibre', label: '7 / 7', pHi: 7, pHe: 7, step: 5 },
  { id: 'acide_interne', label: '6 / 9', pHi: 6, pHe: 9, step: 6 },
] as const;
export const PREPARATION_DELAYS = [2800, 3400, 3400, 4600];
export const TRIAL_DURATION = 3600;

export function clampPH(value: number, fallback = 7) {
  return Number.isFinite(value) ? Math.round(Math.max(4, Math.min(10, value)) * 2) / 2 : fallback;
}

/** Modèle qualitatif du document 11, pas une cinétique ni un bilan énergétique. */
export function vesicleResult({ pHi, pHe }: VesicleParameters) {
  const deltaPH = pHe - pHi;
  return {
    deltaPH,
    concentrationRatio: 10 ** deltaPH,
    direction: deltaPH > 0 ? 'outward' : deltaPH < 0 ? 'inward' : 'none',
    atpSynthesis: deltaPH > 0,
  } as const;
}

export function vesicleVariant(parameters: VesicleParameters) {
  return VESICLE_CASES.find(item => item.pHi === parameters.pHi && item.pHe === parameters.pHe)?.id ?? 'personnalisee';
}

export interface VesicleExperimentState extends VesicleParameters {
  step: number;
  status: 'idle' | 'running' | 'finished';
  trial: number;
  completed: string[];
  action: string;
}

export function initialVesicleState(spec: ScientificPresetVisualSpec): VesicleExperimentState {
  const example = VESICLE_CASES.find(item => item.id === spec.variant);
  const requestedStep = Number.isFinite(spec.step) ? Math.round(spec.step!) : 0;
  const step = example ? example.step : spec.parameters || spec.variant === 'personnalisee' ? 5 : Math.max(0, Math.min(8, requestedStep));
  const defaults = example ?? (step >= 6 ? VESICLE_CASES[2] : step === 4 ? VESICLE_CASES[0] : VESICLE_CASES[1]);
  return {
    step, pHi: clampPH(spec.parameters?.pHi ?? defaults.pHi), pHe: clampPH(spec.parameters?.pHe ?? defaults.pHe),
    status: spec.autoplay ? 'running' : 'idle', trial: 0, completed: [], action: 'ready',
  };
}

type Action =
  | { type: 'parameters'; parameters: Partial<VesicleParameters> }
  | { type: 'variant'; variant: string }
  | { type: 'start' | 'pause' | 'reset' | 'preparation' | 'next' | 'previous' | 'tick' | 'finish' }
  | { type: 'control'; control: ScientificControlCommand };

function openStep(state: VesicleExperimentState, step: number): VesicleExperimentState {
  const bounded = Math.max(0, Math.min(8, Math.round(step)));
  const example = bounded >= 6 ? VESICLE_CASES[2] : bounded === 5 ? VESICLE_CASES[1] : VESICLE_CASES[0];
  return { ...state, step: bounded, ...(bounded >= 4 ? { pHi: example.pHi, pHe: example.pHe } : {}), trial: state.trial + 1 };
}

export function vesicleReducer(state: VesicleExperimentState, action: Action): VesicleExperimentState {
  switch (action.type) {
    case 'parameters': return {
      ...state, step: Math.max(4, state.step), status: 'running', trial: state.trial + 1, action: 'change_ph',
      pHi: clampPH(action.parameters.pHi ?? state.pHi, state.pHi),
      pHe: clampPH(action.parameters.pHe ?? state.pHe, state.pHe),
    };
    case 'variant': {
      if (action.variant === 'personnalisee') return { ...state, step: Math.max(4, state.step), status: 'running', trial: state.trial + 1, action: 'select_variant' };
      const example = VESICLE_CASES.find(item => item.id === action.variant);
      return example ? { ...openStep(state, example.step), status: 'running', action: 'select_variant' } : state;
    }
    case 'start': return { ...state, status: 'running', trial: state.trial + 1, action: 'start_simulation' };
    case 'pause': return { ...state, status: 'idle', action: 'pause_simulation' };
    case 'reset': return { ...state, pHi: 7, pHe: 7, step: state.step < 4 ? 0 : 5, status: 'idle', trial: state.trial + 1, completed: [], action: 'reset' };
    case 'preparation': return { ...state, step: 0, status: 'idle', action: 'replay_preparation' };
    case 'next': return { ...openStep(state, state.step + 1), status: 'idle', action: 'next' };
    case 'previous': return { ...openStep(state, state.step - 1), status: 'idle', action: 'previous' };
    case 'tick': return { ...openStep(state, Math.min(4, state.step + 1)), action: 'preparation_step' };
    case 'finish': {
      const variant = vesicleVariant(state);
      return { ...state, status: 'finished', action: 'finish_simulation', completed: variant === 'personnalisee' ? state.completed : [...new Set([...state.completed, variant])] };
    }
    case 'control': {
      const { command, parameters } = action.control;
      if (command === 'set_parameters') return vesicleReducer(state, { type: 'parameters', parameters: parameters ?? {} });
      if (command === 'set_variant' || command === 'highlight') {
        let next = parameters?.variant === 'scene' && parameters.step === undefined
          ? openStep(state, command === 'highlight' ? 8 : 0)
          : vesicleReducer(state, { type: 'variant', variant: parameters?.variant ?? '' });
        if (parameters?.step !== undefined) next = openStep(next, parameters.step);
        if (parameters?.pHi !== undefined || parameters?.pHe !== undefined) next = vesicleReducer(next, { type: 'parameters', parameters });
        return { ...next, status: command === 'highlight' ? 'idle' : 'running', trial: next.trial + 1, action: `llm_${command}` };
      }
      return vesicleReducer(state, { type: command });
    }
  }
}
