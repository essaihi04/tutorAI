import { useEffect, useMemo, useState } from 'react';
import CytoscapeVisual from './CytoscapeVisual';
import JSXGraphVisual from './JSXGraphVisual';
import type {
  ScientificControlCommand,
  ScientificPresetVisualSpec,
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
}

export default function ScientificPresetVisual({
  spec,
  transparent,
  control,
}: ScientificPresetVisualProps) {
  const meta = SCIENTIFIC_PRESETS[spec.presetId];
  const initialVariant = normalizePresetVariant(meta, spec.variant);
  const [variant, setVariant] = useState(initialVariant);
  const [step, setStep] = useState(() => Math.max(0, Math.min(meta.maxStep, spec.step || 0)));
  const [running, setRunning] = useState(spec.autoplay === true);

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
        setRunning(true);
      } else if (control.command === 'pause') {
        setRunning(false);
      } else if (control.command === 'reset') {
        setRunning(false);
        setStep(0);
        setVariant(normalizePresetVariant(meta, spec.variant));
      } else if (control.command === 'next') {
        setRunning(false);
        setStep(current => Math.min(meta.maxStep, current + 1));
      } else if (control.command === 'previous') {
        setRunning(false);
        setStep(current => Math.max(0, current - 1));
      } else if (control.command === 'set_variant' || control.command === 'highlight') {
        const nextVariant = normalizePresetVariant(meta, wantedVariant);
        setVariant(nextVariant);
        setStep(typeof wantedStep === 'number'
          ? Math.max(0, Math.min(meta.maxStep, wantedStep))
          : control.command === 'highlight' ? meta.maxStep : 0);
        setRunning(control.command === 'set_variant');
      }
    }, 0);
    return () => window.clearTimeout(timer);
  }, [control?.sequence, control, meta, spec.presetId, spec.variant]);

  useEffect(() => {
    if (!running) return;
    const timer = window.setInterval(() => {
      setStep(current => current >= meta.maxStep ? 0 : current + 1);
    }, meta.frameMs);
    return () => window.clearInterval(timer);
  }, [meta.frameMs, meta.maxStep, running]);

  const resolved = useMemo(
    () => resolveScientificPreset(spec.presetId, variant, step),
    [spec.presetId, step, variant],
  );

  return (
    <div className="flex h-full min-h-[360px] w-full flex-col" data-scientific-preset={spec.presetId}>
      <div className="min-h-0 flex-1">
        {resolved.engine === 'cytoscape' && <CytoscapeVisual spec={resolved} transparent={transparent} />}
        {resolved.engine === 'jsxgraph' && <JSXGraphVisual spec={resolved} transparent={transparent} />}
      </div>
      <div
        className="mx-auto mb-1 flex max-w-[96%] flex-wrap items-center justify-center gap-1.5 rounded-xl px-2 py-1.5 text-[11px] text-slate-100"
        style={{ background: 'rgba(2, 12, 27, 0.72)', border: '1px solid rgba(148, 163, 184, 0.24)' }}
        aria-label={`Commandes de la scène : ${meta.title}`}
      >
        <button
          type="button"
          onClick={() => setRunning(value => !value)}
          className="rounded-md px-2 py-1 hover:bg-white/10"
          aria-label={running ? 'Mettre en pause' : 'Démarrer'}
        >
          {running ? '⏸ Pause' : '▶ Démarrer'}
        </button>
        <button
          type="button"
          onClick={() => { setRunning(false); setStep(0); }}
          className="rounded-md px-2 py-1 hover:bg-white/10"
        >
          ↺ Revenir au début
        </button>
        <button
          type="button"
          onClick={() => { setRunning(false); setStep(current => Math.min(meta.maxStep, current + 1)); }}
          className="rounded-md px-2 py-1 hover:bg-white/10"
        >
          Étape suivante
        </button>
        <select
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
        </select>
        <span className="px-1 text-cyan-200" aria-live="polite">
          {Math.min(step, meta.maxStep)}/{meta.maxStep}
        </span>
      </div>
    </div>
  );
}
