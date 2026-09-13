import type { CSSProperties } from 'react';

interface CristaeIsolationVisualProps {
  step: number;
  running: boolean;
  transparent?: boolean;
  onToggleRunning: () => void;
  onReset: () => void;
}

const MEDIA_ROOT = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration';

const STAGES = [
  {
    short: 'Mitochondrie',
    title: 'Mitochondrie intacte',
    conclusion: 'Les crêtes sont des replis de la membrane interne.',
  },
  {
    short: 'Ultrasons',
    title: 'Fragmentation par ultrasons',
    conclusion: 'Les ultrasons rompent les membranes en petits fragments.',
  },
  {
    short: 'Fragments',
    title: 'Fragments de membrane interne',
    conclusion: 'Les fragments issus des crêtes se courbent puis se referment.',
  },
  {
    short: 'Vésicules',
    title: 'Vésicules retournées obtenues',
    conclusion: 'La face matricielle est exposée dehors ; le côté intermembranaire est enfermé.',
  },
] as const;

const labelStyle: CSSProperties = {
  background: 'rgba(2, 12, 27, 0.88)',
  border: '1px solid rgba(103, 232, 249, 0.58)',
  boxShadow: '0 8px 24px rgba(2, 12, 27, 0.42)',
};

function StageImage({ step }: { step: number }) {
  if (step === 0) {
    return (
      <div className="relative h-full w-full overflow-hidden">
        <img
          src={`${MEDIA_ROOT}/mitochondrie_micrographie_reconstitution.png`}
          alt="Micrographie électronique d’une mitochondrie intacte présentant de nombreuses crêtes"
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950/75 via-transparent to-slate-950/20" />
        <div className="absolute left-[8%] top-[14%] rounded-lg px-3 py-2 text-xs font-bold text-cyan-100" style={labelStyle}>
          Membrane externe
        </div>
        <div className="absolute left-[44%] top-[41%] rounded-lg px-3 py-2 text-xs font-bold text-amber-100" style={{ ...labelStyle, borderColor: 'rgba(251, 191, 36, 0.68)' }}>
          Crêtes mitochondriales
        </div>
        <div className="absolute bottom-[13%] right-[9%] rounded-lg px-3 py-2 text-xs font-bold text-emerald-100" style={{ ...labelStyle, borderColor: 'rgba(74, 222, 128, 0.65)' }}>
          Matrice
        </div>
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 rounded-full bg-amber-300 px-4 py-2 text-center text-xs font-black text-slate-950 shadow-lg">
          À prédire : quelle face sera exposée après les ultrasons ?
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="relative h-full w-full overflow-hidden">
        <img
          src={`${MEDIA_ROOT}/sonication_mitochondries_realiste.png`}
          alt="Sonde à ultrasons plongée dans une suspension froide de mitochondries isolées"
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-slate-950/55 via-transparent to-slate-950/30" />
        <div className="absolute left-1/2 top-[7%] -translate-x-1/2 rounded-lg px-3 py-2 text-xs font-bold text-cyan-100" style={labelStyle}>
          Sonde à ultrasons
        </div>
        <div className="absolute bottom-[11%] left-1/2 -translate-x-1/2 rounded-lg px-3 py-2 text-xs font-bold text-amber-100" style={{ ...labelStyle, borderColor: 'rgba(251, 191, 36, 0.68)' }}>
          Suspension de mitochondries isolées
        </div>
        <div className="absolute left-1/2 top-[48%] h-24 w-24 -translate-x-1/2 -translate-y-1/2 animate-ping rounded-full border-2 border-cyan-300/70" />
        <div className="absolute left-1/2 top-[48%] h-40 w-40 -translate-x-1/2 -translate-y-1/2 animate-pulse rounded-full border border-cyan-200/50" />
        <div className="absolute bottom-4 left-4 rounded-full bg-cyan-300 px-3 py-1.5 text-[11px] font-black text-slate-950">
          Bain de glace : limite l’échauffement
        </div>
      </div>
    );
  }

  if (step === 2) {
    const fragments = [
      { left: '8%', top: '14%', width: '39%', rotate: '-7deg', position: 'left center' },
      { left: '53%', top: '8%', width: '39%', rotate: '8deg', position: 'right center' },
      { left: '26%', top: '57%', width: '48%', rotate: '2deg', position: 'center bottom' },
    ];
    return (
      <div className="relative h-full w-full overflow-hidden bg-[#031b2c]">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.18),transparent_68%)]" />
        {fragments.map((fragment, index) => (
          <div
            key={fragment.left}
            className="absolute overflow-hidden rounded-[40%] border-2 border-cyan-300/65 shadow-[0_0_26px_rgba(34,211,238,0.25)] transition-transform duration-700"
            style={{ left: fragment.left, top: fragment.top, width: fragment.width, height: '31%', transform: `rotate(${fragment.rotate})` }}
          >
            <img
              src={`${MEDIA_ROOT}/mitochondrie_membrane_interne_realiste.png`}
              alt={index === 0 ? 'Fragments réalistes de membrane interne portant des protéines transmembranaires et des ATP synthases' : ''}
              className="h-full w-full object-cover"
              style={{ objectPosition: fragment.position }}
            />
          </div>
        ))}
        <div className="absolute left-1/2 top-1/2 z-10 -translate-x-1/2 -translate-y-1/2 rounded-full bg-amber-300 px-4 py-2 text-center text-xs font-black text-slate-950 shadow-xl">
          Repliement spontané
        </div>
        <div className="absolute bottom-4 left-4 rounded-lg px-3 py-2 text-xs font-bold text-cyan-100" style={labelStyle}>
          Fragments de membrane interne
        </div>
        <div className="absolute bottom-4 right-4 rounded-lg px-3 py-2 text-xs font-bold text-amber-100" style={{ ...labelStyle, borderColor: 'rgba(251, 191, 36, 0.68)' }}>
          ATP synthases conservées
        </div>
      </div>
    );
  }

  return (
    <div className="relative h-full w-full overflow-hidden">
      <img
        src={`${MEDIA_ROOT}/vesicules_retournees_realistes.png`}
        alt="Vésicules retournées de membrane interne dont les ATP synthases sont orientées vers l’extérieur"
        className="h-full w-full object-cover"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-slate-950/65 via-transparent to-slate-950/20" />
      <div className="absolute left-[6%] top-[8%] max-w-[36%] rounded-lg px-3 py-2 text-xs font-black text-cyan-100" style={labelStyle}>
        Face matricielle → extérieur
      </div>
      <div className="absolute left-1/2 top-1/2 max-w-[34%] -translate-x-1/2 -translate-y-1/2 rounded-lg px-3 py-2 text-center text-xs font-black text-amber-100" style={{ ...labelStyle, borderColor: 'rgba(251, 191, 36, 0.72)' }}>
        Côté espace intermembranaire → intérieur de la vésicule
      </div>
      <div className="absolute bottom-[12%] right-[5%] max-w-[34%] rounded-lg px-3 py-2 text-xs font-black text-emerald-100" style={{ ...labelStyle, borderColor: 'rgba(74, 222, 128, 0.68)' }}>
        Sphères pédonculées exposées vers l’extérieur
      </div>
    </div>
  );
}

export default function CristaeIsolationVisual({
  step,
  running,
  transparent,
  onToggleRunning,
  onReset,
}: CristaeIsolationVisualProps) {
  const safeStep = Math.max(0, Math.min(STAGES.length - 1, Math.round(step)));
  const stage = STAGES[safeStep];

  return (
    <figure
      className="flex h-full min-h-[390px] w-full flex-col overflow-hidden rounded-2xl text-slate-100"
      style={transparent ? undefined : { background: '#061c23', border: '1px solid rgba(34, 211, 238, 0.24)' }}
      aria-label={`Étape ${safeStep + 1} : ${stage.title}. ${stage.conclusion}`}
      data-active-experiment-stage={safeStep}
      data-tutor-experiment="isolement-cretes-ultrasons"
    >
      <header className="flex items-center justify-between gap-3 border-b border-cyan-200/15 bg-slate-950/75 px-4 py-2.5">
        <div className="min-w-0">
          <div className="text-[10px] font-black uppercase tracking-[0.18em] text-cyan-300">
            Expérience d’isolement des crêtes · {safeStep + 1}/4
          </div>
          <h3 className="truncate text-base font-black text-white sm:text-lg">{stage.title}</h3>
        </div>
        <div className="hidden items-center gap-1.5 sm:flex" aria-label="Progression de l’expérience">
          {STAGES.map((item, index) => (
            <span
              key={item.short}
              className={`h-2.5 w-8 rounded-full transition-colors ${index <= safeStep ? 'bg-cyan-300' : 'bg-slate-700'}`}
              title={item.short}
            />
          ))}
        </div>
      </header>

      <div className="relative min-h-0 flex-1" key={safeStep}>
        <StageImage step={safeStep} />
      </div>

      <figcaption className="border-t border-cyan-200/15 bg-slate-950/85 px-4 py-2 text-center text-xs font-semibold text-cyan-50">
        {stage.conclusion}
      </figcaption>

      <div className="flex items-center justify-center gap-2 bg-slate-950/90 px-3 py-2.5" aria-label="Commandes de l’expérience">
        <button
          type="button"
          onClick={onToggleRunning}
          className="min-w-[150px] rounded-xl bg-cyan-300 px-4 py-2 text-xs font-black text-slate-950 shadow-lg transition hover:bg-cyan-200"
          data-tutor-action="toggle-sonication-experiment"
        >
          {running ? '⏸ Pause' : safeStep >= STAGES.length - 1 ? '▶ Revoir' : safeStep === 0 ? '▶ Lancer l’expérience' : '▶ Continuer'}
        </button>
        <button
          type="button"
          onClick={onReset}
          className="rounded-xl border border-white/20 bg-white/5 px-4 py-2 text-xs font-bold text-white transition hover:bg-white/10"
          data-tutor-action="reset-sonication-experiment"
        >
          ↺ Recommencer
        </button>
      </div>
    </figure>
  );
}
