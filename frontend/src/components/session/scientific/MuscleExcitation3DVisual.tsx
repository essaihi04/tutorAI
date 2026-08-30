import { useEffect, useState } from 'react';
import { ChevronLeft, ChevronRight, Pause, Play, RefreshCcw } from 'lucide-react';
import type { MuscleExcitation3DPart, MuscleExcitation3DVisualSpec } from './types';

interface MuscleExcitation3DVisualProps {
  spec: MuscleExcitation3DVisualSpec;
  transparent?: boolean;
}

interface StageInfo {
  id: string;
  element: string;
  definition: string;
  role: string;
  focus: MuscleExcitation3DPart;
  image: string;
  objectFit: 'contain' | 'cover';
  transform: string;
  transformOrigin: string;
}

const HIERARCHY_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/hierarchie_muscle_3d.png';
const MICROGRAPH_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/muscle_strie_micrographie_reconstitution.png';
const SARCOMERE_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/contraction/sarcomere_actine_myosine_3d.png';
const NEUROMUSCULAR_TRIAD_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/contraction/neuromuscular_triad_3d_v2.png';

/** The text stays metadata-only so the tutor can narrate the silent visual. */
export const MUSCLE_EXCITATION_STAGES: readonly StageInfo[] = [
  {
    id: 'muscle', element: 'Muscle strié squelettique',
    definition: 'Organe contractile fixé aux os par des tendons.',
    role: 'Transformer l’énergie chimique de l’ATP en mouvement et en chaleur.',
    focus: 'muscle', image: HIERARCHY_IMAGE, objectFit: 'contain', transform: 'scale(1)', transformOrigin: '8% 52%',
  },
  {
    id: 'fascicle', element: 'Faisceau musculaire',
    definition: 'Ensemble de fibres musculaires entouré de tissu conjonctif.',
    role: 'Organiser les fibres qui produisent ensemble la force du muscle.',
    focus: 'fascicle', image: HIERARCHY_IMAGE, objectFit: 'contain', transform: 'scale(1.38)', transformOrigin: '30% 52%',
  },
  {
    id: 'muscle_fiber', element: 'Fibre musculaire',
    definition: 'Longue cellule plurinucléée limitée par le sarcolemme.',
    role: 'Recevoir le potentiel d’action et contenir les myofibrilles.',
    focus: 'muscle_fiber', image: HIERARCHY_IMAGE, objectFit: 'contain', transform: 'scale(1.86)', transformOrigin: '53% 52%',
  },
  {
    id: 'myofibril', element: 'Myofibrille',
    definition: 'Cylindre contractile formé d’une succession de sarcomères.',
    role: 'Transmettre le raccourcissement des sarcomères à toute la fibre.',
    focus: 'myofibril', image: HIERARCHY_IMAGE, objectFit: 'contain', transform: 'scale(2.42)', transformOrigin: '76% 52%',
  },
  {
    id: 'striated_fibers', element: 'Fibres musculaires striées',
    definition: 'Longues cellules parallèles dont les stries révèlent les sarcomères.',
    role: 'Montrer l’organisation réelle du tissu musculaire.',
    focus: 'muscle_fiber', image: MICROGRAPH_IMAGE, objectFit: 'cover', transform: 'scale(1)', transformOrigin: '50% 50%',
  },
  {
    id: 'sarcomere', element: 'Sarcomère',
    definition: 'Segment de myofibrille compris entre deux stries Z.',
    role: 'Se raccourcir par glissement de l’actine sur la myosine.',
    focus: 'sarcomere', image: SARCOMERE_IMAGE, objectFit: 'contain', transform: 'scale(1)', transformOrigin: '50% 50%',
  },
  {
    id: 'neuromuscular_junction', element: 'Jonction neuromusculaire',
    definition: 'Zone de communication entre le motoneurone et la fibre musculaire.',
    role: 'Déclencher un potentiel d’action musculaire grâce à l’acétylcholine.',
    focus: 'neuromuscular_junction', image: NEUROMUSCULAR_TRIAD_IMAGE, objectFit: 'cover', transform: 'scale(1.1)', transformOrigin: '24% 42%',
  },
  {
    id: 't_tubule', element: 'Tubule transverse T',
    definition: 'Invagination du sarcolemme qui pénètre dans la fibre.',
    role: 'Conduire la dépolarisation au voisinage du réticulum.',
    focus: 't_tubule', image: NEUROMUSCULAR_TRIAD_IMAGE, objectFit: 'cover', transform: 'scale(1.24)', transformOrigin: '49% 50%',
  },
  {
    id: 'calcium_release', element: 'Réticulum sarcoplasmique et Ca²⁺',
    definition: 'Réseau membranaire qui stocke puis libère le calcium.',
    role: 'Augmenter la concentration de Ca²⁺ autour des myofibrilles.',
    focus: 'sarcoplasmic_reticulum', image: NEUROMUSCULAR_TRIAD_IMAGE, objectFit: 'cover', transform: 'scale(1.2)', transformOrigin: '67% 50%',
  },
  {
    id: 'troponin_calcium', element: 'Troponine C et Ca²⁺',
    definition: 'Sous-unité régulatrice qui fixe le calcium.',
    role: 'Changer la conformation du complexe troponine–tropomyosine.',
    focus: 'troponin', image: SARCOMERE_IMAGE, objectFit: 'cover', transform: 'scale(1.18)', transformOrigin: '58% 48%',
  },
  {
    id: 'tropomyosin', element: 'Tropomyosine',
    definition: 'Protéine allongée placée dans le sillon de l’actine.',
    role: 'Découvrir les sites de liaison de la myosine.',
    focus: 'tropomyosin', image: SARCOMERE_IMAGE, objectFit: 'cover', transform: 'scale(1.32)', transformOrigin: '58% 48%',
  },
  {
    id: 'crossbridge', element: 'Pont actomyosine',
    definition: 'Liaison entre une tête de myosine armée et l’actine.',
    role: 'Permettre la transmission de la force au filament d’actine.',
    focus: 'myosin', image: SARCOMERE_IMAGE, objectFit: 'cover', transform: 'scale(1.58)', transformOrigin: '61% 52%',
  },
  {
    id: 'power_stroke', element: 'Coup de force de la myosine',
    definition: 'Pivotement de la tête accompagné de la libération de Pi puis ADP.',
    role: 'Faire glisser l’actine vers le centre du sarcomère.',
    focus: 'actin', image: SARCOMERE_IMAGE, objectFit: 'cover', transform: 'scale(1.76)', transformOrigin: '61% 52%',
  },
  {
    id: 'atp_binding', element: 'Fixation de l’ATP sur la myosine',
    definition: 'Un nouvel ATP se fixe sur la tête de myosine.',
    role: 'Rompre le pont actomyosine et détacher la tête.',
    focus: 'atp', image: SARCOMERE_IMAGE, objectFit: 'cover', transform: 'scale(2.02)', transformOrigin: '62% 54%',
  },
  {
    id: 'atp_hydrolysis', element: 'Hydrolyse de l’ATP',
    definition: 'ATP et eau donnent ADP et phosphate inorganique.',
    role: 'Fournir l’énergie qui réarme la tête de myosine.',
    focus: 'atp', image: SARCOMERE_IMAGE, objectFit: 'cover', transform: 'scale(2.22)', transformOrigin: '62% 54%',
  },
  {
    id: 'relaxation', element: 'Pompe SERCA et relâchement',
    definition: 'SERCA est une pompe du réticulum qui consomme de l’ATP.',
    role: 'Recapturer le Ca²⁺ et permettre à la tropomyosine de remasquer l’actine.',
    focus: 'sarcoplasmic_reticulum', image: NEUROMUSCULAR_TRIAD_IMAGE, objectFit: 'cover', transform: 'scale(1.24)', transformOrigin: '58% 50%',
  },
];

function normalizedStep(value: number | undefined) {
  return Math.max(0, Math.min(MUSCLE_EXCITATION_STAGES.length - 1, Math.round(value || 0)));
}

interface StageLabel {
  text: string;
  left: number;
  top: number;
}

const STAGE_LABELS: readonly (readonly StageLabel[])[] = [
  [
    { text: 'Muscle strié squelettique', left: 12, top: 20 },
    { text: 'Faisceau musculaire', left: 35, top: 24 },
    { text: 'Fibre musculaire', left: 59, top: 24 },
    { text: 'Myofibrille', left: 84, top: 23 },
  ],
  [
    { text: 'Faisceau musculaire', left: 49, top: 18 },
    { text: 'Fibres musculaires', left: 59, top: 57 },
    { text: 'Tissu conjonctif', left: 29, top: 70 },
  ],
  [
    { text: 'Fibre musculaire', left: 52, top: 17 },
    { text: 'Sarcolemme', left: 33, top: 67 },
    { text: 'Myofibrilles', left: 62, top: 60 },
    { text: 'Noyau périphérique', left: 76, top: 37 },
  ],
  [
    { text: 'Myofibrille', left: 50, top: 17 },
    { text: 'Sarcomères', left: 56, top: 49 },
    { text: 'Stries Z', left: 31, top: 67 },
  ],
  [
    { text: 'Fibres musculaires striées', left: 50, top: 14 },
    { text: 'Stries transversales', left: 50, top: 49 },
    { text: 'Noyaux périphériques', left: 22, top: 73 },
  ],
  [
    { text: 'Strie Z', left: 10, top: 47 },
    { text: 'Filament d’actine', left: 28, top: 27 },
    { text: 'Filament de myosine', left: 52, top: 68 },
    { text: 'Têtes de myosine', left: 74, top: 35 },
  ],
  [
    { text: 'Motoneurone', left: 11, top: 13 },
    { text: 'Terminaison nerveuse', left: 24, top: 32 },
    { text: 'Jonction neuromusculaire', left: 24, top: 63 },
    { text: 'Sarcolemme', left: 42, top: 77 },
    { text: 'Myofibrilles', left: 83, top: 20 },
  ],
  [
    { text: 'Tubule T', left: 49, top: 16 },
    { text: 'Réticulum sarcoplasmique', left: 65, top: 66 },
    { text: 'Triade', left: 49, top: 77 },
    { text: 'Myofibrilles', left: 83, top: 20 },
  ],
  [
    { text: 'Réticulum sarcoplasmique', left: 43, top: 18 },
    { text: 'Ions Ca²⁺', left: 66, top: 48 },
    { text: 'Myofibrilles', left: 84, top: 20 },
  ],
  [
    { text: 'Troponine C', left: 43, top: 25 },
    { text: 'Ca²⁺', left: 53, top: 43 },
    { text: 'Actine', left: 28, top: 70 },
    { text: 'Tropomyosine', left: 67, top: 70 },
  ],
  [
    { text: 'Tropomyosine déplacée', left: 51, top: 23 },
    { text: 'Sites de liaison exposés', left: 56, top: 49 },
    { text: 'Actine', left: 30, top: 72 },
  ],
  [
    { text: 'Actine', left: 31, top: 24 },
    { text: 'Tête de myosine–ADP–Pi', left: 57, top: 61 },
    { text: 'Pont actomyosine', left: 68, top: 30 },
    { text: 'Myosine', left: 48, top: 78 },
  ],
  [
    { text: 'Actine en glissement', left: 34, top: 25 },
    { text: 'Tête de myosine pivotée', left: 59, top: 56 },
    { text: 'Centre du sarcomère', left: 76, top: 76 },
  ],
  [
    { text: 'ATP', left: 57, top: 32 },
    { text: 'Tête de myosine détachée', left: 59, top: 62 },
    { text: 'Actine', left: 29, top: 76 },
  ],
  [
    { text: 'ADP', left: 53, top: 27 },
    { text: 'Phosphate inorganique (Pi)', left: 68, top: 31 },
    { text: 'Tête de myosine réarmée', left: 59, top: 63 },
  ],
  [
    { text: 'Réticulum sarcoplasmique', left: 46, top: 18 },
    { text: 'Pompe SERCA', left: 49, top: 64 },
    { text: 'Ca²⁺ recapturé', left: 66, top: 42 },
    { text: 'Myofibrilles au repos', left: 84, top: 22 },
  ],
];

function StageLabels({ step }: { step: number }) {
  return (
    <div className="pointer-events-none absolute inset-0 z-20" aria-hidden="true">
      {(STAGE_LABELS[step] || []).map(label => (
        <span
          key={label.text}
          className="absolute -translate-x-1/2 -translate-y-1/2 rounded-md border border-white/25 bg-slate-950/78 px-2 py-1 text-center text-[10px] font-bold leading-tight text-white shadow-lg backdrop-blur-sm sm:text-xs"
          style={{ left: `${label.left}%`, top: `${label.top}%` }}
        >
          {label.text}
        </span>
      ))}
    </div>
  );
}

export default function MuscleExcitation3DVisual({ spec, transparent }: MuscleExcitation3DVisualProps) {
  const [step, setStep] = useState(() => normalizedStep(spec.step));
  const [running, setRunning] = useState(spec.autoplay === true);
  const currentStage = MUSCLE_EXCITATION_STAGES[step];

  useEffect(() => {
    setStep(normalizedStep(spec.step));
  }, [spec.step]);

  useEffect(() => {
    setRunning(spec.autoplay === true);
  }, [spec.autoplay]);

  useEffect(() => {
    if (!running) return undefined;
    const timer = window.setInterval(() => {
      setStep(current => {
        if (current >= MUSCLE_EXCITATION_STAGES.length - 1) {
          setRunning(false);
          return current;
        }
        return current + 1;
      });
    }, 2600);
    return () => window.clearInterval(timer);
  }, [running]);

  const previous = () => {
    setRunning(false);
    setStep(current => Math.max(0, current - 1));
  };

  const next = () => {
    setRunning(false);
    setStep(current => Math.min(MUSCLE_EXCITATION_STAGES.length - 1, current + 1));
  };

  const reset = () => {
    setRunning(false);
    setStep(0);
  };

  return (
    <figure
      className={`group relative h-full min-h-[440px] w-full overflow-hidden rounded-2xl border border-white/10 shadow-[0_24px_80px_rgba(2,6,23,0.42)] ${transparent ? 'bg-transparent' : 'bg-slate-950'}`}
      data-scientific-engine="three"
      data-scientific-model="muscle_excitation_contraction"
      data-stage-index={step}
      data-stage={currentStage.id}
      data-stage-element={currentStage.element}
      data-stage-definition={currentStage.definition}
      data-stage-role={currentStage.role}
      data-stage-focus={currentStage.focus}
    >
      <button
        type="button"
        onClick={next}
        className="absolute inset-0 z-10 cursor-zoom-in"
        aria-label={`Zoom suivant depuis ${currentStage.element}`}
      />

      <img
        src={currentStage.image}
        alt=""
        aria-hidden="true"
        className={`absolute inset-0 h-full w-full select-none transition-transform duration-1000 ease-in-out ${currentStage.objectFit === 'cover' ? 'object-cover' : 'object-contain'}`}
        style={{ transform: currentStage.transform, transformOrigin: currentStage.transformOrigin }}
        draggable={false}
      />

      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_46%,transparent_45%,rgba(2,6,23,0.58)_100%)]" />
      <StageLabels step={step} />

      <button
        type="button"
        onClick={(event) => { event.stopPropagation(); previous(); }}
        disabled={step === 0}
        className="absolute left-3 top-1/2 z-30 grid h-11 w-11 -translate-y-1/2 place-items-center rounded-lg border border-white/15 bg-slate-950/55 text-white opacity-0 shadow-xl backdrop-blur transition hover:bg-slate-900/85 focus:opacity-100 disabled:pointer-events-none disabled:opacity-0 group-hover:opacity-100"
        aria-label="Zoom précédent"
      >
        <ChevronLeft className="h-6 w-6" />
      </button>

      <button
        type="button"
        onClick={(event) => { event.stopPropagation(); next(); }}
        disabled={step === MUSCLE_EXCITATION_STAGES.length - 1}
        className="absolute right-3 top-1/2 z-30 grid h-11 w-11 -translate-y-1/2 place-items-center rounded-lg border border-white/15 bg-slate-950/55 text-white opacity-0 shadow-xl backdrop-blur transition hover:bg-slate-900/85 focus:opacity-100 disabled:pointer-events-none disabled:opacity-0 group-hover:opacity-100"
        aria-label="Zoom suivant"
      >
        <ChevronRight className="h-6 w-6" />
      </button>

      <div className="absolute right-3 top-3 z-30 flex gap-1.5 opacity-0 transition focus-within:opacity-100 group-hover:opacity-100">
        <button
          type="button"
          onClick={(event) => { event.stopPropagation(); setRunning(value => !value); }}
          className="grid h-9 w-9 place-items-center rounded-lg border border-white/15 bg-slate-950/55 text-white shadow-lg backdrop-blur hover:bg-slate-900/85"
          aria-label={running ? 'Mettre le zoom en pause' : 'Lancer le zoom'}
        >
          {running ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
        </button>
        <button
          type="button"
          onClick={(event) => { event.stopPropagation(); reset(); }}
          className="grid h-9 w-9 place-items-center rounded-lg border border-white/15 bg-slate-950/55 text-white shadow-lg backdrop-blur hover:bg-slate-900/85"
          aria-label="Revenir au muscle entier"
        >
          <RefreshCcw className="h-4 w-4" />
        </button>
      </div>

      <figcaption className="sr-only" aria-live="polite">
        Étape {step} : {currentStage.element}. {currentStage.definition} {currentStage.role}
      </figcaption>
    </figure>
  );
}
