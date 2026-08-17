import { useEffect, useRef, useState } from 'react';
import { MODE_LABELS, TUTOR_MODES, type TutorMode } from '../../services/sessionMode';

/**
 * Les quatre modes, toujours visibles, jamais dans un menu.
 *
 * Deux raisons de la garder à l'écran plutôt que de laisser le tuteur décider
 * seul :
 *
 *  1. **La porte de sortie.** Un tuteur qui décide de tout peut décider mal,
 *     et un lycéen enfermé ferme l'application. L'élève passe toujours devant
 *     — y compris pour quitter un examen, que le tuteur ne peut pas
 *     interrompre lui-même.
 *  2. **Rendre le changement lisible.** Quand le tuteur bascule de lui-même,
 *     l'élève doit voir POURQUOI. Un écran qui change sans explication est
 *     vécu comme un bug, pas comme une intention.
 *
 * Le bouton actif suit le serveur, pas le clic : tant que `mode_changed` n'est
 * pas revenu, rien ne bouge. C'est ce qui garantit que la barre montre l'état
 * réel de la session et pas une intention.
 */
interface SessionModeBarProps {
  mode: TutorMode;
  /** Justification jointe par le tuteur à son dernier changement. */
  reason?: string;
  onSelect: (mode: TutorMode) => void;
  disabled?: boolean;
}

export default function SessionModeBar({ mode, reason, onSelect, disabled }: SessionModeBarProps) {
  // Le mot « demandé » reste affiché en attente pour que le clic ne semble
  // pas ignoré, mais il ne devient JAMAIS le mode actif de lui-même.
  const [demande, setDemande] = useState<TutorMode | null>(null);
  const [annonce, setAnnonce] = useState<string>('');
  const modePrecedent = useRef(mode);

  useEffect(() => {
    if (mode !== modePrecedent.current) {
      modePrecedent.current = mode;
      setDemande(null);
      setAnnonce(reason || '');
    }
  }, [mode, reason]);

  // L'explication s'efface : elle informe d'une transition, elle ne décrit
  // pas l'état courant.
  useEffect(() => {
    if (!annonce) return;
    const t = window.setTimeout(() => setAnnonce(''), 6000);
    return () => window.clearTimeout(t);
  }, [annonce]);

  const choisir = (cible: TutorMode) => {
    if (disabled || cible === mode) return;
    setDemande(cible);
    onSelect(cible);
  };

  return (
    <div className="flex flex-col gap-1.5">
      <div
        className="flex items-center gap-1 rounded-2xl border border-white/[0.07] bg-white/[0.035] p-1"
        role="group"
        aria-label="Ce que tu fais maintenant"
      >
        {TUTOR_MODES.map((cle) => {
          const { label, icon, hint } = MODE_LABELS[cle];
          const actif = cle === mode;
          const enAttente = cle === demande && !actif;
          return (
            <button
              key={cle}
              onClick={() => choisir(cle)}
              disabled={disabled}
              title={hint}
              aria-current={actif ? 'true' : undefined}
              className={`flex flex-1 items-center justify-center gap-1.5 rounded-xl px-2 py-2 text-xs font-bold transition-all disabled:opacity-40 ${
                actif
                  ? 'bg-white/[0.11] text-white shadow-sm'
                  : enAttente
                    ? 'text-cyan-300/70'
                    : 'text-white/40 hover:bg-white/[0.05] hover:text-white/80'
              }`}
            >
              <span aria-hidden>{icon}</span>
              <span className="hidden sm:inline">{label}</span>
              {enAttente && <span className="h-1 w-1 animate-pulse rounded-full bg-cyan-300" />}
            </button>
          );
        })}
      </div>

      {annonce && (
        <p className="px-2 text-[11px] leading-snug text-cyan-300/70" role="status">
          {annonce}
        </p>
      )}
    </div>
  );
}
