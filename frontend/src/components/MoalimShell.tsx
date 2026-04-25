import type { ReactNode } from 'react';

/**
 * MoalimShell — wrapper sombre commun à toutes les pages.
 * Reproduit l'ambiance de la landing : bg #070718 + 3 orbes flous + grille subtile.
 *
 * Usage minimal :
 *   <MoalimShell>
 *     ...contenu...
 *   </MoalimShell>
 *
 * Variantes :
 *   - withGrid : ajoute la grille en arrière-plan (par défaut true)
 *   - className : classes appliquées au wrapper interne (au-dessus des orbes)
 */
export default function MoalimShell({
  children,
  withGrid = true,
  className = '',
}: {
  children: ReactNode;
  withGrid?: boolean;
  className?: string;
}) {
  return (
    <div className="min-h-screen bg-[#070718] text-white relative overflow-hidden">
      {/* Orbes décoratifs */}
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute top-0 left-1/3 w-[700px] h-[700px] rounded-full bg-indigo-600/20 blur-[150px] anim-pulse-glow" />
        <div
          className="absolute top-[40%] right-[10%] w-[500px] h-[500px] rounded-full bg-cyan-500/15 blur-[140px] anim-pulse-glow"
          style={{ animationDelay: '2s' }}
        />
        <div
          className="absolute bottom-0 left-[5%] w-[600px] h-[600px] rounded-full bg-fuchsia-600/10 blur-[160px] anim-pulse-glow"
          style={{ animationDelay: '4s' }}
        />
        {withGrid && (
          <div className="absolute inset-0 grid-bg opacity-30" />
        )}
      </div>

      {/* Contenu */}
      <div className={`relative z-10 ${className}`}>{children}</div>
    </div>
  );
}

/**
 * MoalimLogo — logo gradient utilisé partout dans la nav.
 */
export function MoalimLogo({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizes = {
    sm: { box: 'w-8 h-8', text: 'text-xs', title: 'text-sm' },
    md: { box: 'w-9 h-9', text: 'text-sm', title: 'text-base' },
    lg: { box: 'w-11 h-11', text: 'text-base', title: 'text-lg' },
  }[size];

  return (
    <div className="flex items-center gap-2.5 group">
      <div className="relative">
        <div
          className={`${sizes.box} rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/30`}
        >
          <span className={`text-white font-bold ${sizes.text} font-brand`}>م</span>
        </div>
        <div
          className={`absolute inset-0 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 blur-md opacity-50 group-hover:opacity-80 transition-opacity`}
        />
      </div>
      <div>
        <div className={`font-bold ${sizes.title} leading-tight text-white`}>Moalim</div>
        <div className="text-[10px] text-white/40 leading-tight font-brand">معلم</div>
      </div>
    </div>
  );
}
