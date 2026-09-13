import { useEffect, useMemo, useState } from 'react';
import CytoscapeVisual from './CytoscapeVisual';
import JSXGraphVisual from './JSXGraphVisual';
import RoughSVGVisual from './RoughSVGVisual';
import MitochondrionZoomVisual from './MitochondrionZoomVisual';
import PyruvateMitochondrionImageVisual from './PyruvateMitochondrionImageVisual';
import KrebsMatrixImageVisual from './KrebsMatrixImageVisual';
import CristaeIsolationVisual from './CristaeIsolationVisual';
import FermentationPhotoVisual from './FermentationPhotoVisual';
import VesicleExperimentVisual from './VesicleExperimentVisual';
import RespiratoryChainVisual from './RespiratoryChainVisual';
import GlucoseJourneyVisual from './GlucoseJourneyVisual';
import EnergyBalanceVisual from './EnergyBalanceVisual';
import { respiratoryGradientFrame, RESPIRATORY_YIELDS } from './respiratoryChainModel';
import type {
  ScientificControlCommand,
  ScientificPresetVisualSpec,
  ScientificSimulationUpdate,
} from './types';
import {
  SCIENTIFIC_PRESETS,
  normalizePresetVariant,
  resolveScientificPreset,
} from './scientificPresets';

interface ScientificPresetVisualProps {
  spec: ScientificPresetVisualSpec;
  transparent?: boolean;
  control?: ScientificControlCommand | null;
  onStateChange?: (update: ScientificSimulationUpdate) => void;
}

export default function ScientificPresetVisual(props: ScientificPresetVisualProps) {
  const { spec } = props;
  return spec.presetId === 'svt_ch1_vesicules_atp_synthase'
    ? <VesicleExperimentVisual key={`${spec.variant}-${spec.step}-${spec.autoplay}-${spec.parameters?.pHi}-${spec.parameters?.pHe}`} {...props} />
    : <PresetTimelineVisual {...props} />;
}

function PresetTimelineVisual({
  spec,
  transparent: requestedTransparent,
  control,
  onStateChange,
}: ScientificPresetVisualProps) {
  const isMusclePreset = [
    'svt_ch1_myogrammes', 'svt_ch1_glissement_sarcomere', 'svt_ch1_cycle_actomyosine',
    'svt_ch1_chaleurs_muscle', 'svt_ch1_filieres_effort', 'svt_ch1_couplage_excitation_contraction',
  ].includes(spec.presetId);
  const transparent = requestedTransparent || isMusclePreset;
  const meta = SCIENTIFIC_PRESETS[spec.presetId];
  const initialVariant = normalizePresetVariant(meta, spec.variant);
  const [variant, setVariant] = useState(initialVariant);
  const [step, setStep] = useState(() => Math.max(0, Math.min(meta.maxStep, spec.step || 0)));
  const [running, setRunning] = useState(spec.autoplay === true);
  const [lastAction, setLastAction] = useState(spec.autoplay === true ? 'autoplay' : 'ready');
  const frameMs = meta.frameMs;

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const nextMeta = SCIENTIFIC_PRESETS[spec.presetId];
      setVariant(normalizePresetVariant(nextMeta, spec.variant));
      setStep(Math.max(0, Math.min(nextMeta.maxStep, spec.step || 0)));
      setRunning(spec.autoplay === true);
    }, 0);
    return () => window.clearTimeout(timer);
  }, [spec.autoplay, spec.presetId, spec.step, spec.variant]);

  useEffect(() => {
    if (!control || control.presetId !== spec.presetId) return;
    const timer = window.setTimeout(() => {
      const wantedVariant = control.parameters?.variant;
      const wantedStep = control.parameters?.step;
      if (control.command === 'start') {
        setStep(current => current >= meta.maxStep ? 0 : current);
        setRunning(true);
        setLastAction('llm_start');
      } else if (control.command === 'pause') {
        setRunning(false);
        setLastAction('llm_pause');
      } else if (control.command === 'reset') {
        setRunning(false);
        setStep(0);
        setVariant(normalizePresetVariant(meta, spec.variant));
        setLastAction('llm_reset');
      } else if (control.command === 'next') {
        setRunning(false);
        setStep(current => Math.min(meta.maxStep, current + 1));
        setLastAction('llm_next');
      } else if (control.command === 'previous') {
        setRunning(false);
        setStep(current => Math.max(0, current - 1));
        setLastAction('llm_previous');
      } else if (control.command === 'set_variant' || control.command === 'highlight') {
        const nextVariant = normalizePresetVariant(meta, wantedVariant);
        setVariant(nextVariant);
        setStep(typeof wantedStep === 'number'
          ? Math.max(0, Math.min(meta.maxStep, wantedStep))
          : control.command === 'highlight' ? meta.maxStep : 0);
        setRunning(control.command === 'set_variant');
        setLastAction(`llm_${control.command}`);
      }
    }, 0);
    return () => window.clearTimeout(timer);
  }, [control?.sequence, control, meta, spec.presetId, spec.variant]);

  useEffect(() => {
    if (!running) return;
    const timer = window.setInterval(() => {
      setStep(current => {
        if (current >= meta.maxStep) {
          setRunning(false);
          setLastAction('finish_simulation');
          return meta.maxStep;
        }
        return current + 1;
      });
    }, frameMs);
    return () => window.clearInterval(timer);
  }, [frameMs, meta.maxStep, running]);

  useEffect(() => {
    if (!onStateChange) return;
    const respiratory = spec.presetId === 'svt_ch1_chimiosmose' ? respiratoryGradientFrame(step) : null;
    const simulationStatus = running
      ? 'running'
      : step >= meta.maxStep
        ? 'finished'
        : step === 0
          ? 'idle'
          : 'paused';
    onStateChange({
      type: 'simulation_state',
      simulation_id: spec.presetId,
      current_state: {
        simulation_status: simulationStatus,
        preset_id: spec.presetId,
        variant,
        step,
        max_step: meta.maxStep,
        ...(respiratory ? { respiratory_gradient: {
          intermembrane_ph: respiratory.intermembranePH,
          matrix_ph: respiratory.matrixPH,
          delta_pH: respiratory.deltaPH,
          concentration_ratio: respiratory.concentrationRatio,
          proton_pumping: respiratory.pumping,
          atp_synthesis: respiratory.makingAtp,
          school_atp_yield: RESPIRATORY_YIELDS[variant === 'fadh2' ? 'fadh2' : 'nadh'].atp,
        } } : {}),
      },
      student_actions: [{ action: lastAction, variant, step }],
      objective_progress: meta.maxStep > 0 ? step / meta.maxStep : 0,
      timestamp: new Date().toISOString(),
    });
  }, [lastAction, meta.maxStep, onStateChange, running, spec.presetId, step, variant]);

  const resolved = useMemo(
    () => {
      const result = resolveScientificPreset(spec.presetId, variant, step);
      return isMusclePreset && result.engine === 'roughsvg'
        ? { ...result, elements: result.elements.map(element => element.type === 'rect' ? { ...element, fill: undefined } : element) }
        : result;
    },
    [spec.presetId, step, variant, isMusclePreset],
  );
  const isMitochondrionZoom = spec.presetId === 'svt_ch1_ultrastructure_mitochondrie';
  const isPyruvateMitochondrionImage = spec.presetId === 'svt_ch1_pyruvate_acetyl_coa';
  const isKrebsMatrixImage = spec.presetId === 'svt_ch1_krebs_detaille';
  const isCristaeIsolation = spec.presetId === 'svt_ch1_isolement_cretes_ultrasons';
  const isFermentationPhotos = spec.presetId === 'svt_ch1_fermentations_photos';
  const isRespiratoryChain = spec.presetId === 'svt_ch1_chimiosmose';
  const isGlucoseJourney = spec.presetId === 'svt_ch1_schema_bilan_annote';
  const isEnergyBalance = spec.presetId === 'svt_ch1_rendement_energetique';
  // Les libellés décrivent l'expérience, ils ne sont pas des objets animés.
  // On les prend dans l'état final de la variante afin que leur contenu et
  // leur position restent identiques du premier au dernier pas.
  const fixedLabels = useMemo(() => {
    // Les repères anatomiques suivent les filaments mobiles.
    if (spec.presetId === 'svt_ch1_glissement_sarcomere') return undefined;
    const finalSpec = resolveScientificPreset(spec.presetId, variant, meta.maxStep);
    return finalSpec.engine === 'jsxgraph'
      ? finalSpec.elements.filter(element => Boolean(element.label))
      : undefined;
  }, [meta.maxStep, spec.presetId, variant]);

  return (
    <div
      className={`flex h-full w-full flex-col ${isGlucoseJourney || isRespiratoryChain || isEnergyBalance ? 'min-h-0' : 'min-h-[360px]'}`}
      data-scientific-preset={spec.presetId}
      data-simulation-status={running ? 'running' : step >= meta.maxStep ? 'finished' : step === 0 ? 'idle' : 'paused'}
      data-simulation-step={step}
      data-simulation-variant={variant}
    >
      <div className="min-h-0 flex-1">
        {isGlucoseJourney && <GlucoseJourneyVisual
          step={step} maxStep={meta.maxStep} running={running}
          onSelect={nextStep => { setStep(nextStep); setRunning(false); setLastAction(`glucose_stop_${nextStep}`); }}
          onToggle={() => { if (!running && step >= meta.maxStep) setStep(0); setRunning(value => !value); setLastAction(running ? 'pause' : 'start'); }}
          onReset={() => { setStep(0); setRunning(false); setLastAction('reset'); }}
        />}
        {isEnergyBalance && <EnergyBalanceVisual
          step={step}
          running={running}
          variant={variant === 'navette_36' ? 'navette_36' : 'scene'}
          onSelectPhase={nextStep => {
            setStep(nextStep);
            setRunning(false);
            setLastAction(`energy_phase_${nextStep}`);
          }}
          onVariant={nextVariant => {
            setVariant(nextVariant);
            setLastAction(`energy_variant_${nextVariant}`);
          }}
          onToggleRunning={() => {
            if (!running && step >= meta.maxStep) setStep(0);
            setRunning(value => !value);
            setLastAction(running ? 'energy_pause' : 'energy_start');
          }}
          onReset={() => {
            setStep(0);
            setRunning(false);
            setLastAction('energy_reset');
          }}
          onNext={() => {
            setStep(current => Math.min(meta.maxStep, current + 1));
            setRunning(false);
            setLastAction('energy_next');
          }}
        />}
        {isRespiratoryChain && <RespiratoryChainVisual
          variant={variant === 'fadh2' ? 'fadh2' : 'nadh'}
          step={step}
          running={running}
          onVariant={nextVariant => {
            setVariant(nextVariant);
            setStep(0);
            setRunning(true);
            setLastAction(`respiratory_variant_${nextVariant}`);
          }}
          onToggleRunning={() => {
            if (!running && step >= meta.maxStep) setStep(0);
            setRunning(value => !value);
            setLastAction(running ? 'respiratory_pause' : 'respiratory_start');
          }}
          onReset={() => {
            setRunning(false);
            setStep(0);
            setLastAction('respiratory_reset');
          }}
          onNext={() => {
            setRunning(false);
            setStep(current => Math.min(meta.maxStep, current + 1));
            setLastAction('respiratory_next');
          }}
          onSelectPhase={nextStep => {
            setStep(nextStep);
            setRunning(true);
            setLastAction(`respiratory_phase_${nextStep}`);
          }}
        />}
        {isMitochondrionZoom && (
          <MitochondrionZoomVisual
            step={step}
            running={running}
            transparent={transparent}
            onNext={() => {
              setRunning(false);
              setStep(current => Math.min(meta.maxStep, current + 1));
              setLastAction('image_zoom_next');
            }}
            onPrevious={() => {
              setRunning(false);
              setStep(current => Math.max(0, current - 1));
              setLastAction('image_zoom_previous');
            }}
            onSelectStage={(nextStep, stageId) => {
              setRunning(false);
              setStep(Math.max(0, Math.min(meta.maxStep, nextStep)));
              setLastAction(`image_zoom_select_${stageId}`);
            }}
            onToggleRunning={() => {
              if (!running && step >= meta.maxStep) setStep(0);
              setRunning(value => !value);
              setLastAction(running ? 'image_zoom_pause' : 'image_zoom_start');
            }}
            onReset={() => {
              setRunning(false);
              setStep(0);
              setLastAction('image_zoom_reset');
            }}
          />
        )}
        {isPyruvateMitochondrionImage && <PyruvateMitochondrionImageVisual step={step} transparent={transparent} />}
        {isKrebsMatrixImage && <KrebsMatrixImageVisual step={step} transparent={transparent} />}
        {isCristaeIsolation && (
          <CristaeIsolationVisual
            step={step}
            running={running}
            transparent={transparent}
            onToggleRunning={() => {
              if (!running && step >= meta.maxStep) setStep(0);
              setRunning(value => !value);
              setLastAction(running ? 'sonication_pause' : 'sonication_start');
            }}
            onReset={() => {
              setRunning(false);
              setStep(0);
              setLastAction('sonication_reset');
            }}
          />
        )}
        {isFermentationPhotos && (
          <FermentationPhotoVisual
            step={step}
            running={running}
            transparent={transparent}
            onToggleRunning={() => {
              if (!running && step >= meta.maxStep) setStep(0);
              setRunning(value => !value);
              setLastAction(running ? 'fermentation_pause' : 'fermentation_start');
            }}
            onReset={() => {
              setRunning(false);
              setStep(0);
              setLastAction('fermentation_reset');
            }}
          />
        )}
        {!isGlucoseJourney && !isEnergyBalance && !isRespiratoryChain && !isMitochondrionZoom && !isPyruvateMitochondrionImage && !isKrebsMatrixImage && !isCristaeIsolation && !isFermentationPhotos && resolved.engine === 'cytoscape' && <CytoscapeVisual spec={resolved} transparent={transparent} />}
        {!isGlucoseJourney && !isEnergyBalance && !isRespiratoryChain && !isMitochondrionZoom && !isPyruvateMitochondrionImage && !isKrebsMatrixImage && !isCristaeIsolation && !isFermentationPhotos && resolved.engine === 'jsxgraph' && (
          <JSXGraphVisual spec={resolved} transparent={transparent} fixedLabels={fixedLabels} />
        )}
        {!isGlucoseJourney && !isEnergyBalance && !isRespiratoryChain && !isMitochondrionZoom && !isPyruvateMitochondrionImage && !isKrebsMatrixImage && !isCristaeIsolation && !isFermentationPhotos && resolved.engine === 'roughsvg' && <RoughSVGVisual spec={resolved} transparent={transparent} />}
      </div>
      {!isGlucoseJourney && !isEnergyBalance && !isRespiratoryChain && !isMitochondrionZoom && !isCristaeIsolation && !isFermentationPhotos && <div
        className={transparent
          ? 'mx-auto mb-1 flex flex-wrap items-center justify-center gap-2'
          : 'mx-auto mb-1 flex max-w-[96%] flex-wrap items-center justify-center gap-1.5 rounded-xl px-2 py-1.5 text-[11px] text-slate-100'}
        style={transparent ? undefined : { background: 'rgba(2, 12, 27, 0.72)', border: '1px solid rgba(148, 163, 184, 0.24)' }}
        aria-label={`Commandes de la scène : ${meta.title}`}
      >
        <button
          type="button"
          onClick={() => {
            if (!running && step >= meta.maxStep) setStep(0);
            setRunning(value => !value);
            setLastAction(running ? 'pause' : 'start');
          }}
          className={transparent
            ? 'rounded-lg border border-cyan-300/60 bg-transparent px-3 py-1.5 text-xs font-semibold text-white hover:bg-white/10'
            : 'rounded-md px-2 py-1 hover:bg-white/10'}
          aria-label={running ? 'Mettre en pause' : 'Démarrer'}
        >
          {running ? '⏸ Pause' : '▶ Démarrer'}
        </button>
        {!transparent && <button
          type="button"
          onClick={() => { setRunning(false); setStep(0); }}
          className="rounded-md px-2 py-1 hover:bg-white/10"
        >
          ↺ Revenir au début
        </button>}
        {(!transparent || isMusclePreset) && <button
          type="button"
          onClick={() => { setRunning(false); setStep(current => current >= meta.maxStep ? 0 : current + 1); }}
          className="rounded-md px-2 py-1 text-xs text-slate-100 hover:bg-white/10 disabled:opacity-40"
        >
          {step >= meta.maxStep ? 'Recommencer' : 'Étape suivante'}
        </button>}
        {(!transparent || (isMusclePreset && ['svt_ch1_myogrammes', 'svt_ch1_chaleurs_muscle', 'svt_ch1_couplage_excitation_contraction'].includes(spec.presetId))) && <select
          value={variant}
          onChange={event => {
            setVariant(event.target.value);
            setStep(0);
            setRunning(false);
          }}
          className="rounded-md border border-white/15 bg-slate-900/90 px-2 py-1 text-slate-100"
          aria-label="Variante scientifique"
        >
          {meta.variants.map(item => <option key={item.id} value={item.id}>{item.label}</option>)}
        </select>}
        {!transparent && <span className="px-1 text-cyan-200" aria-live="polite">
          {Math.min(step, meta.maxStep)}/{meta.maxStep}
        </span>}
      </div>}
    </div>
  );
}
