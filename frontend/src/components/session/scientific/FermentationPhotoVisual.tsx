import type { CSSProperties, ReactNode } from 'react';

interface FermentationPhotoVisualProps {
  step: number;
  running: boolean;
  transparent?: boolean;
  onToggleRunning: () => void;
  onReset: () => void;
}

const MEDIA_ROOT = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/fermentation';
const MUSCLE_IMAGE = `${MEDIA_ROOT}/fermentation_lactique_muscle_realiste.png`;
const YEAST_IMAGE = `${MEDIA_ROOT}/fermentation_alcoolique_levure_realiste.png`;

const STAGES = [
  {
    title: 'Question de départ',
    conclusion: 'Même absence de O₂ : le muscle et la levure forment-ils les mêmes produits ?',
  },
  {
    title: 'Fermentation lactique',
    conclusion: 'Dans le muscle : le pyruvate est réduit en lactate et le NAD⁺ est régénéré.',
  },
  {
    title: 'Fermentation alcoolique',
    conclusion: 'Chez la levure : le pyruvate donne de l’éthanol et du CO₂, avec régénération du NAD⁺.',
  },
  {
    title: 'Comparer les deux fermentations',
    conclusion: 'Deux produits différents, mais une même fonction : régénérer le NAD⁺ pour maintenir la glycolyse.',
  },
] as const;

const panelStyle: CSSProperties = {
  background: 'rgba(2, 12, 27, 0.88)',
  border: '1px solid rgba(255, 255, 255, 0.22)',
  boxShadow: '0 10px 28px rgba(2, 12, 27, 0.48)',
};

function PhotoPanel({ src, alt, title, children }: {
  src: string;
  alt: string;
  title: string;
  children?: ReactNode;
}) {
  return (
    <div className="relative h-full min-h-0 overflow-hidden">
      <img src={src} alt={alt} className="h-full w-full object-cover" />
      <div className="absolute inset-0 bg-gradient-to-t from-slate-950/85 via-slate-950/10 to-slate-950/25" />
      <div className="absolute left-3 top-3 rounded-lg px-3 py-2 text-xs font-black text-white" style={panelStyle}>
        {title}
      </div>
      {children}
    </div>
  );
}

function StageContent({ step }: { step: number }) {
  if (step === 0) {
    return (
      <div className="grid h-full grid-cols-2 gap-px bg-cyan-100/20">
        <PhotoPanel
          src={MUSCLE_IMAGE}
          alt="Fibres musculaires striées observées pendant un effort intense"
          title="Cellule musculaire"
        />
        <PhotoPanel
          src={YEAST_IMAGE}
          alt="Suspension de levures produisant des bulles de dioxyde de carbone dans un flacon fermé"
          title="Levure"
        />
        <div className="absolute left-1/2 top-1/2 w-[72%] -translate-x-1/2 -translate-y-1/2 rounded-2xl border border-amber-200/70 bg-slate-950/90 px-5 py-3 text-center shadow-2xl">
          <div className="text-[10px] font-black uppercase tracking-[0.16em] text-amber-300">À toi de prévoir</div>
          <div className="mt-1 text-sm font-black text-white sm:text-base">Sans O₂, obtient-on le même produit dans les deux cellules ?</div>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <PhotoPanel
        src={MUSCLE_IMAGE}
        alt="Fibres musculaires striées, siège de la fermentation lactique dans le hyaloplasme"
        title="Muscle · hyaloplasme · sans consommation directe de O₂"
      >
        <div className="absolute left-1/2 top-1/2 w-[88%] -translate-x-1/2 -translate-y-1/2 rounded-2xl px-4 py-3 text-center" style={panelStyle}>
          <div className="text-[11px] font-bold text-cyan-200">2 pyruvates + 2 NADH,H⁺</div>
          <div className="my-1 text-2xl font-black text-amber-300">→</div>
          <div className="text-base font-black text-white">2 lactates + 2 NAD⁺</div>
        </div>
        <div className="absolute bottom-3 left-3 rounded-full bg-emerald-300 px-3 py-1.5 text-[11px] font-black text-slate-950">
          NAD⁺ régénéré
        </div>
        <div className="absolute bottom-3 right-3 rounded-full bg-amber-300 px-3 py-1.5 text-[11px] font-black text-slate-950">
          CO₂ : non produit
        </div>
      </PhotoPanel>
    );
  }

  if (step === 2) {
    return (
      <PhotoPanel
        src={YEAST_IMAGE}
        alt="Levures en anaérobiose produisant de l’éthanol et du dioxyde de carbone"
        title="Levure · hyaloplasme · sans consommation directe de O₂"
      >
        <div className="absolute left-[4%] top-1/2 w-[50%] -translate-y-1/2 rounded-2xl px-4 py-3 text-center" style={panelStyle}>
          <div className="text-[11px] font-bold text-cyan-200">2 pyruvates + 2 NADH,H⁺</div>
          <div className="my-1 text-2xl font-black text-amber-300">→</div>
          <div className="text-base font-black text-white">2 C₂H₅OH + 2 CO₂ + 2 NAD⁺</div>
        </div>
        <div className="absolute bottom-3 left-3 rounded-full bg-emerald-300 px-3 py-1.5 text-[11px] font-black text-slate-950">
          NAD⁺ régénéré
        </div>
        <div className="absolute bottom-3 right-3 animate-pulse rounded-full bg-cyan-300 px-3 py-1.5 text-[11px] font-black text-slate-950">
          Bulles de CO₂
        </div>
      </PhotoPanel>
    );
  }

  return (
    <div className="grid h-full grid-cols-2 gap-px bg-cyan-100/20">
      <PhotoPanel src={MUSCLE_IMAGE} alt="Fermentation lactique dans le muscle" title="Fermentation lactique">
        <div className="absolute bottom-4 left-1/2 w-[88%] -translate-x-1/2 rounded-xl px-3 py-2 text-center" style={panelStyle}>
          <div className="text-sm font-black text-white">Pyruvate → lactate</div>
          <div className="mt-1 text-[10px] font-bold text-amber-200">CO₂ non produit</div>
        </div>
      </PhotoPanel>
      <PhotoPanel src={YEAST_IMAGE} alt="Fermentation alcoolique chez la levure" title="Fermentation alcoolique">
        <div className="absolute bottom-4 left-1/2 w-[88%] -translate-x-1/2 rounded-xl px-3 py-2 text-center" style={panelStyle}>
          <div className="text-sm font-black text-white">Pyruvate → éthanol + CO₂</div>
          <div className="mt-1 text-[10px] font-bold text-amber-200">Dégagement gazeux</div>
        </div>
      </PhotoPanel>
      <div className="absolute left-1/2 top-[54%] w-[66%] -translate-x-1/2 -translate-y-1/2 rounded-2xl border border-emerald-200/65 bg-slate-950/92 px-4 py-3 text-center shadow-2xl">
        <div className="text-sm font-black text-emerald-300">NAD⁺ régénéré → glycolyse maintenue</div>
        <div className="mt-1 text-xs font-bold text-white">Bilan énergétique commun : 2 ATP nets par glucose</div>
      </div>
    </div>
  );
}

export default function FermentationPhotoVisual({
  step,
  running,
  transparent,
  onToggleRunning,
  onReset,
}: FermentationPhotoVisualProps) {
  const safeStep = Math.max(0, Math.min(STAGES.length - 1, Math.round(step)));
  const stage = STAGES[safeStep];

  return (
    <figure
      className="flex h-full min-h-[390px] w-full flex-col overflow-hidden rounded-2xl text-slate-100"
      style={transparent ? undefined : { background: '#06151d', border: '1px solid rgba(34, 211, 238, 0.24)' }}
      aria-label={`Étape ${safeStep + 1} : ${stage.title}. ${stage.conclusion}`}
      data-active-fermentation-stage={safeStep}
      data-tutor-experiment="comparaison-fermentations"
    >
      <header className="flex items-center justify-between gap-3 border-b border-white/10 bg-slate-950/85 px-4 py-2.5">
        <div className="min-w-0">
          <div className="text-[10px] font-black uppercase tracking-[0.18em] text-cyan-300">Fermentations · {safeStep + 1}/4</div>
          <h3 className="truncate text-base font-black text-white sm:text-lg">{stage.title}</h3>
        </div>
        <div className="hidden items-center gap-1.5 sm:flex" aria-label="Progression de la comparaison">
          {STAGES.map((item, index) => (
            <span key={item.title} className={`h-2.5 w-8 rounded-full ${index <= safeStep ? 'bg-cyan-300' : 'bg-slate-700'}`} />
          ))}
        </div>
      </header>

      <div className="relative min-h-0 flex-1" key={safeStep}>
        <StageContent step={safeStep} />
      </div>

      <figcaption className="border-t border-white/10 bg-slate-950/90 px-4 py-2 text-center text-xs font-semibold text-cyan-50">
        {stage.conclusion}
      </figcaption>

      <div className="flex items-center justify-center gap-2 bg-slate-950/95 px-3 py-2.5" aria-label="Commandes de la comparaison des fermentations">
        <button
          type="button"
          onClick={onToggleRunning}
          className="min-w-[150px] rounded-xl bg-cyan-300 px-4 py-2 text-xs font-black text-slate-950 shadow-lg transition hover:bg-cyan-200"
          data-tutor-action="toggle-fermentation-comparison"
        >
          {running ? '⏸ Pause' : safeStep >= STAGES.length - 1 ? '▶ Revoir' : safeStep === 0 ? '▶ Vérifier l’hypothèse' : '▶ Continuer'}
        </button>
        <button
          type="button"
          onClick={onReset}
          className="rounded-xl border border-white/20 bg-white/5 px-4 py-2 text-xs font-bold text-white transition hover:bg-white/10"
          data-tutor-action="reset-fermentation-comparison"
        >
          ↺ Recommencer
        </button>
      </div>
    </figure>
  );
}
