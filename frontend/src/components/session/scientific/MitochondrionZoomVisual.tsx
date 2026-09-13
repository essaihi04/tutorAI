import { useMemo } from 'react';
import { ChevronLeft, ChevronRight, Pause, Play, RefreshCcw } from 'lucide-react';

const MAIN_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_3d_sans_legendes.png';
const OUTER_MEMBRANE_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_membrane_externe_realiste.png';
const INNER_MEMBRANE_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_membrane_interne_realiste.png';
const INTERMEMBRANE_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_espace_intermembranaire_realiste.png';
const MATRIX_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_matrice_realiste.png';

interface MitochondrionZoomVisualProps {
  step: number;
  running: boolean;
  transparent?: boolean;
  onNext: () => void;
  onPrevious: () => void;
  onSelectStage: (stageIndex: number, stageId: string) => void;
  onToggleRunning: () => void;
  onReset: () => void;
}

interface ZoomStage {
  id: string;
  title: string;
  navTitle: string;
  definition: string;
  image: string;
  objectFit: 'contain' | 'cover';
  transform: string;
  transformOrigin: string;
}

/** Une image par niveau, comme le modèle de zoom du muscle. */
export const MITOCHONDRION_ZOOM_STAGES: readonly ZoomStage[] = [
  {
    id: 'whole', title: 'Mitochondrie entière',
    navTitle: 'Vue entière',
    definition: 'Organite délimité par une membrane externe et une membrane interne repliée.',
    image: MAIN_IMAGE, objectFit: 'contain', transform: 'scale(1)', transformOrigin: '50% 50%',
  },
  {
    id: 'outer-membrane', title: 'Membrane externe et porines',
    navTitle: 'Membrane externe',
    definition: 'Les porines permettent le passage des ions et de petits métabolites hydrosolubles.',
    image: OUTER_MEMBRANE_IMAGE, objectFit: 'contain', transform: 'scale(1)', transformOrigin: '50% 50%',
  },
  {
    id: 'inner-membrane', title: 'Membrane interne et crêtes',
    navTitle: 'Membrane interne',
    definition: 'Les complexes respiratoires et les sphères pédonculées sont des protéines transmembranaires.',
    image: INNER_MEMBRANE_IMAGE, objectFit: 'contain', transform: 'scale(1)', transformOrigin: '50% 50%',
  },
  {
    id: 'intermembrane', title: 'Espace intermembranaire',
    navTitle: 'Espace intermembranaire',
    definition: 'Les H⁺ y sont accumulés : leur gradient fournit l’énergie à l’ATP synthase.',
    image: INTERMEMBRANE_IMAGE, objectFit: 'contain', transform: 'scale(1)', transformOrigin: '50% 50%',
  },
  {
    id: 'matrix', title: 'Matrice mitochondriale',
    navTitle: 'Matrice',
    definition: 'Compartiment interne où se déroulent l’oxydation du pyruvate et le cycle de Krebs.',
    image: MATRIX_IMAGE, objectFit: 'contain', transform: 'scale(1)', transformOrigin: '50% 50%',
  },
];

const LABELS = ['Vue d’ensemble', 'Porines', 'Chaîne respiratoire', 'Gradient H⁺', 'Métabolites'];

interface CompositionLabel {
  text: string;
  left: string;
  top: string;
  className: string;
}

const COMPOSITION_LABELS: Readonly<Record<string, readonly CompositionLabel[]>> = {
  'outer-membrane': [
    { text: 'Cytoplasme', left: '15%', top: '25%', className: 'border-cyan-200/40 bg-slate-950/76 text-cyan-50' },
    { text: 'Ions · petits métabolites', left: '50%', top: '18%', className: 'border-yellow-200/50 bg-amber-950/76 text-yellow-100' },
    { text: 'Porines', left: '50%', top: '77%', className: 'border-fuchsia-200/50 bg-violet-950/76 text-fuchsia-100' },
    { text: 'Espace intermembranaire', left: '18%', top: '78%', className: 'border-orange-200/45 bg-orange-950/76 text-orange-100' },
  ],
  'inner-membrane': [
    { text: 'H⁺ pompés', left: '53%', top: '17%', className: 'border-yellow-200/55 bg-amber-950/80 text-yellow-100' },
    { text: 'Complexes I–IV', left: '25%', top: '25%', className: 'border-cyan-200/45 bg-slate-950/78 text-cyan-50' },
    { text: 'Complexes transmembranaires', left: '25%', top: '78%', className: 'border-violet-200/45 bg-violet-950/76 text-violet-100' },
    { text: 'Sphère pédonculée = ATP synthase', left: '74%', top: '78%', className: 'border-emerald-200/50 bg-emerald-950/78 text-emerald-100' },
  ],
  intermembrane: [
    { text: 'Membrane externe', left: '17%', top: '16%', className: 'border-rose-200/50 bg-rose-950/76 text-rose-100' },
    { text: 'H⁺ accumulés', left: '50%', top: '35%', className: 'border-yellow-200/60 bg-amber-950/80 text-yellow-100' },
    { text: 'Membrane interne', left: '18%', top: '58%', className: 'border-amber-200/50 bg-amber-950/76 text-amber-100' },
    { text: 'ATP synthase', left: '76%', top: '51%', className: 'border-violet-200/50 bg-violet-950/78 text-violet-100' },
    { text: 'Matrice', left: '16%', top: '78%', className: 'border-cyan-200/50 bg-slate-950/76 text-cyan-100' },
  ],
  matrix: [
    { text: 'Pyruvate', left: '13%', top: '39%', className: 'border-orange-200/55 bg-orange-950/80 text-orange-100' },
    { text: 'Acétyl-CoA', left: '34%', top: '39%', className: 'border-violet-200/55 bg-violet-950/80 text-violet-100' },
    { text: 'NAD⁺', left: '58%', top: '39%', className: 'border-emerald-200/55 bg-emerald-950/80 text-emerald-100' },
    { text: 'NADH,H⁺', left: '83%', top: '39%', className: 'border-emerald-200/55 bg-emerald-950/80 text-emerald-100' },
    { text: 'FAD', left: '14%', top: '75%', className: 'border-cyan-200/55 bg-cyan-950/80 text-cyan-100' },
    { text: 'FADH₂', left: '38%', top: '75%', className: 'border-cyan-200/55 bg-cyan-950/80 text-cyan-100' },
    { text: 'ATP', left: '64%', top: '75%', className: 'border-yellow-200/55 bg-amber-950/80 text-yellow-100' },
    { text: 'H₂O', left: '88%', top: '75%', className: 'border-blue-200/55 bg-blue-950/80 text-blue-100' },
  ],
};

function safeStep(value: number) {
  return Math.max(0, Math.min(MITOCHONDRION_ZOOM_STAGES.length - 1, Math.round(value)));
}

export default function MitochondrionZoomVisual({
  step,
  running,
  transparent,
  onNext,
  onPrevious,
  onSelectStage,
  onToggleRunning,
  onReset,
}: MitochondrionZoomVisualProps) {
  const index = safeStep(step);
  const stage = MITOCHONDRION_ZOOM_STAGES[index];
  const progressLabel = useMemo(() => `${index + 1}/${MITOCHONDRION_ZOOM_STAGES.length}`, [index]);

  return (
    <figure
      className={`group relative flex h-full min-h-[460px] w-full flex-col overflow-hidden rounded-2xl border border-white/10 shadow-[0_24px_80px_rgba(2,6,23,0.42)] ${transparent ? 'bg-transparent' : 'bg-slate-950'}`}
      data-scientific-engine="image-zoom"
      data-scientific-model="mitochondrion"
      data-stage-index={index}
      data-stage={stage.id}
      data-active-compartment={stage.id}
      data-tutor-stage-index={index}
      data-stage-element={stage.title}
      data-stage-definition={stage.definition}
    >
      <header className="relative z-40 flex min-h-[68px] items-center justify-between gap-3 border-b border-cyan-300/20 bg-slate-950/95 px-4 py-2.5 text-white">
        <div className="min-w-0">
          <div className="text-[10px] font-extrabold uppercase tracking-[0.18em] text-cyan-300">Explorateur de la mitochondrie · {progressLabel}</div>
          <h3 className="truncate text-base font-black leading-tight sm:text-lg">{stage.title}</h3>
          <div className="text-[10px] font-semibold text-slate-300">{LABELS[index]}</div>
        </div>
        <div className="flex shrink-0 gap-1.5">
          <button type="button" onClick={onToggleRunning} className="grid h-9 w-9 place-items-center rounded-lg border border-white/15 bg-slate-900 text-white shadow-lg transition hover:border-cyan-300/60 hover:bg-slate-800" aria-label={running ? 'Mettre le zoom automatique en pause' : 'Lancer le zoom automatique'} data-tutor-action={running ? 'pause' : 'play'}>
            {running ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
          </button>
          <button type="button" onClick={onReset} className="grid h-9 w-9 place-items-center rounded-lg border border-white/15 bg-slate-900 text-white shadow-lg transition hover:border-cyan-300/60 hover:bg-slate-800" aria-label="Afficher la mitochondrie entière" data-tutor-action="reset-compartment">
            <RefreshCcw className="h-4 w-4" />
          </button>
        </div>
      </header>

      <div className="relative min-h-0 flex-1 overflow-hidden">
        <button
          type="button"
          onClick={onNext}
          disabled={index === MITOCHONDRION_ZOOM_STAGES.length - 1}
          className="absolute inset-0 z-10 cursor-zoom-in disabled:cursor-default"
          aria-label={index < MITOCHONDRION_ZOOM_STAGES.length - 1 ? `Afficher ${MITOCHONDRION_ZOOM_STAGES[index + 1].title}` : 'Dernier compartiment affiché'}
        />
        <img
          src={stage.image}
          alt=""
          aria-hidden="true"
          className={`${stage.objectFit === 'cover' ? 'object-cover' : 'object-contain'} absolute inset-0 h-full w-full select-none transition-transform duration-1000 ease-in-out`}
          style={{ transform: stage.transform, transformOrigin: stage.transformOrigin }}
          draggable={false}
        />
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_46%,transparent_42%,rgba(2,6,23,0.62)_100%)]" />
        <div className="pointer-events-none absolute inset-0 z-20" aria-hidden="true">
          {(COMPOSITION_LABELS[stage.id] ?? []).map((label) => (
            <span
              key={label.text}
              className={`absolute -translate-x-1/2 -translate-y-1/2 whitespace-nowrap rounded-full border px-2.5 py-1 text-[clamp(9px,1.15vw,15px)] font-extrabold shadow-lg backdrop-blur ${label.className}`}
              style={{ left: label.left, top: label.top }}
            >
              {label.text}
            </span>
          ))}
        </div>

        <div className="pointer-events-none absolute bottom-2 left-1/2 z-20 w-[min(88%,620px)] -translate-x-1/2 rounded-lg border border-white/15 bg-slate-950/82 px-3 py-1.5 text-center text-[11px] font-semibold text-white shadow-lg backdrop-blur">
          {stage.definition}
        </div>

        <button
          type="button"
          onClick={(event) => { event.stopPropagation(); onPrevious(); }}
          disabled={index === 0}
          className="absolute left-3 top-1/2 z-30 grid h-11 w-11 -translate-y-1/2 place-items-center rounded-xl border border-white/25 bg-slate-950/82 text-white shadow-xl backdrop-blur transition hover:border-cyan-300 hover:bg-cyan-950/90 disabled:pointer-events-none disabled:opacity-25"
          aria-label={index > 0 ? `Afficher ${MITOCHONDRION_ZOOM_STAGES[index - 1].title}` : 'Aucun compartiment précédent'}
          data-tutor-action="previous-compartment"
        >
          <ChevronLeft className="h-6 w-6" />
        </button>
        <button
          type="button"
          onClick={(event) => { event.stopPropagation(); onNext(); }}
          disabled={index === MITOCHONDRION_ZOOM_STAGES.length - 1}
          className="absolute right-3 top-1/2 z-30 grid h-11 w-11 -translate-y-1/2 place-items-center rounded-xl border border-white/25 bg-slate-950/82 text-white shadow-xl backdrop-blur transition hover:border-cyan-300 hover:bg-cyan-950/90 disabled:pointer-events-none disabled:opacity-25"
          aria-label={index < MITOCHONDRION_ZOOM_STAGES.length - 1 ? `Afficher ${MITOCHONDRION_ZOOM_STAGES[index + 1].title}` : 'Aucun compartiment suivant'}
          data-tutor-action="next-compartment"
        >
          <ChevronRight className="h-6 w-6" />
        </button>
      </div>

      <nav
        className="relative z-40 grid min-h-[66px] grid-cols-5 gap-1 border-t border-cyan-300/20 bg-slate-950/95 p-1.5"
        aria-label="Choisir un compartiment mitochondrial"
        data-tutor-control="mitochondrion-compartment-selector"
      >
        {MITOCHONDRION_ZOOM_STAGES.map((candidate, stageIndex) => {
          const active = stageIndex === index;
          return (
            <button
              key={candidate.id}
              type="button"
              onClick={() => onSelectStage(stageIndex, candidate.id)}
              className={`min-w-0 rounded-lg border px-1 py-1 text-[9px] font-extrabold leading-tight transition sm:text-[10px] ${active ? 'border-cyan-300 bg-cyan-400/20 text-cyan-50 shadow-[0_0_18px_rgba(34,211,238,0.18)]' : 'border-white/10 bg-slate-900/80 text-slate-300 hover:border-cyan-300/50 hover:text-white'}`}
              aria-pressed={active}
              aria-label={`Afficher ${candidate.title}`}
              data-tutor-action="select-compartment"
              data-tutor-compartment={candidate.id}
              data-tutor-step={stageIndex}
            >
              <span className="block text-[8px] text-cyan-300/80">{stageIndex + 1}</span>
              <span className="block line-clamp-2">{candidate.navTitle}</span>
            </button>
          );
        })}
      </nav>

      <figcaption className="sr-only" aria-live="polite">
        Étape {index + 1} : {stage.title}. {stage.definition}
      </figcaption>
    </figure>
  );
}
