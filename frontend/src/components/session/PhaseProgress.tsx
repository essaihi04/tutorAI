const PHASES = [
  { key: 'activation', label: 'Activation', icon: '⚡' },
  { key: 'exploration', label: 'Exploration', icon: '🔍' },
  { key: 'explanation', label: 'Explication', icon: '💡' },
  { key: 'application', label: 'Application', icon: '🧪' },
  { key: 'consolidation', label: 'Consolidation', icon: '🏆' },
] as const;

interface PhaseProgressProps {
  currentPhase: string;
  onAdvance: () => void;
}

export default function PhaseProgress({ currentPhase, onAdvance }: PhaseProgressProps) {
  const currentIdx = PHASES.findIndex((p) => p.key === currentPhase);
  const isLastPhase = currentIdx === PHASES.length - 1;
  const progress = ((currentIdx) / (PHASES.length - 1)) * 100;

  return (
    <div className="shrink-0 bg-[#0c0c1d]/80 backdrop-blur-md border-b border-white/5 px-4 py-2.5">
      <div className="max-w-4xl mx-auto">
        {/* Progress bar background */}
        <div className="relative flex items-center">
          {/* Track */}
          <div className="absolute left-0 right-0 h-[2px] bg-white/5 rounded-full" />
          {/* Filled track */}
          <div
            className="absolute left-0 h-[2px] bg-gradient-to-r from-indigo-500 via-cyan-400 to-emerald-400 rounded-full transition-all duration-700 ease-out"
            style={{ width: `${progress}%` }}
          />
          {/* Glow effect on filled track */}
          <div
            className="absolute left-0 h-[6px] bg-gradient-to-r from-indigo-500/30 via-cyan-400/20 to-emerald-400/30 rounded-full blur-sm transition-all duration-700 ease-out -translate-y-[2px]"
            style={{ width: `${progress}%` }}
          />

          {/* Phase dots */}
          <div className="relative flex justify-between w-full">
            {PHASES.map((phase, idx) => {
              const isActive = phase.key === currentPhase;
              const isDone = idx < currentIdx;

              return (
                <div key={phase.key} className="flex flex-col items-center" style={{ width: '20%' }}>
                  {/* Dot */}
                  <div className={`relative flex items-center justify-center transition-all duration-500 ${isActive ? 'scale-110' : ''}`}>
                    {/* Active glow */}
                    {isActive && (
                      <div className="absolute w-10 h-10 rounded-full bg-indigo-500/20 animate-pulse" />
                    )}
                    <div
                      className={`relative z-10 w-7 h-7 rounded-full flex items-center justify-center text-xs transition-all duration-500 ${
                        isDone
                          ? 'bg-gradient-to-br from-emerald-400 to-cyan-400 text-white shadow-lg shadow-emerald-500/30'
                          : isActive
                            ? 'bg-gradient-to-br from-indigo-500 to-cyan-500 text-white shadow-lg shadow-indigo-500/40 ring-2 ring-indigo-400/30 ring-offset-1 ring-offset-[#0c0c1d]'
                            : 'bg-white/10 text-white/30 border border-white/10'
                      }`}
                    >
                      {isDone ? '✓' : phase.icon}
                    </div>
                  </div>
                  {/* Label */}
                  <span className={`mt-1.5 text-[10px] font-medium tracking-wide transition-colors duration-300 ${
                    isActive ? 'text-indigo-400' : isDone ? 'text-emerald-400/70' : 'text-white/20'
                  }`}>
                    {phase.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Advance button */}
        {!isLastPhase && (
          <div className="flex justify-end mt-1">
            <button
              onClick={onAdvance}
              className="group flex items-center gap-1 px-3 py-1 text-[10px] text-indigo-400/70 hover:text-indigo-300 transition-all"
            >
              <span>Avancer</span>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
