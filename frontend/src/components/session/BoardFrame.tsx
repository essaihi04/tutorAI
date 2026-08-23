import { useEffect, useState, type ReactNode } from 'react';
import BoardStudentCorner from './BoardStudentCorner';

/**
 * Le cadre commun des tableaux — plein écran, et l'élève peut lever la main.
 *
 * Le mode « prof en direct » s'affichait en plein écran avec un coin élève ;
 * le cours structuré, les schémas et les dessins, eux, restaient dans le
 * cadre du centre, sans micro. Deux tableaux, deux comportements : l'élève
 * devait deviner, selon ce que le professeur affichait, s'il pouvait poser
 * sa question à l'écran ou s'il fallait rouvrir le panneau latéral — donc
 * quitter des yeux la figure sur laquelle portait sa question.
 *
 * LiveBoard garde son propre cadre : son plein écran pilote aussi la lecture
 * du script (pause, vitesse, zoom). Celui-ci sert aux trois autres.
 */
interface BoardFrameProps {
  children: ReactNode;
  /** Le plein écran s'ouvre d'emblée ; l'élève peut en sortir. */
  defaultFocus?: boolean;
  /**
   * Prévient la page qu'on passe en plein écran.
   *
   * Le cadre se pose en `fixed inset-0 z-50` : il recouvre la barre de
   * discussion latérale ET son bouton. Sans ce signal, la barre resterait
   * « ouverte » dans l'état de la page tout en étant invisible et
   * inatteignable — l'élève clique sur un bouton qu'il ne voit plus.
   */
  onFocusChange?: (focus: boolean) => void;
  onStudentMessage?: (text: string) => void;
  assistantReply?: string | null;
  busy?: boolean;
  voiceEnabled?: boolean;
}

export default function BoardFrame({
  children,
  defaultFocus = true,
  onFocusChange,
  onStudentMessage,
  assistantReply,
  busy,
  voiceEnabled,
}: BoardFrameProps) {
  const [focus, setFocus] = useState(defaultFocus);

  useEffect(() => { onFocusChange?.(focus); }, [focus, onFocusChange]);

  // Échap sort du plein écran : c'est le réflexe acquis partout ailleurs, et
  // LiveBoard le respecte déjà. Fermer le tableau reste au ✕ de sa barre.
  useEffect(() => {
    if (!focus) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        setFocus(false);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [focus]);

  return (
    <div
      className={
        focus
          ? 'fixed inset-0 z-50 flex flex-col bg-[#0d1b15]'
          : 'relative w-full h-full flex flex-col'
      }
    >
      {/* Une barre à part, et non un bouton flottant : les trois tableaux
          logent déjà leur titre à gauche et leur ✕ à droite, et un bouton
          posé par-dessus tomberait sur l'un ou sur l'autre. Le ✕ de fermeture
          reste le leur — il est dans le cadre, donc atteignable en plein
          écran. */}
      <div className="shrink-0 flex items-center justify-end px-2 py-1 bg-black/30 border-b border-white/5">
        <button
          onClick={() => setFocus(value => !value)}
          className="text-white/50 hover:text-white/90 text-xs px-2 py-0.5 rounded hover:bg-white/10 transition-colors"
          title={focus ? 'Quitter le plein écran (Échap)' : 'Plein écran'}
        >
          {focus ? '⤡' : '⤢'}
        </button>
      </div>

      <div className="flex-1 min-h-0 relative">
        {children}
      </div>

      <BoardStudentCorner
        onStudentMessage={onStudentMessage}
        assistantReply={assistantReply}
        busy={busy}
        voiceEnabled={voiceEnabled}
      />
    </div>
  );
}
