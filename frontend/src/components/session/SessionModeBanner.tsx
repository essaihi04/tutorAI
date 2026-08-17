import { useEffect, useState } from 'react';
import { MODE_LABELS, type TutorMode } from '../../services/sessionMode';

/**
 * Ce que le tuteur est en train de faire — affiché, jamais demandé.
 *
 * La version précédente offrait quatre onglets cliquables. C'était le menu
 * qu'on venait de supprimer, remis à l'horizontale : l'élève arrivait et on
 * lui redemandait de choisir, avant même que le tuteur ait parlé.
 *
 * Le tuteur décide. Ce bandeau ne fait que rendre sa décision LISIBLE — un
 * écran qui change sans explication est vécu comme un bug, pas comme une
 * intention. D'où la raison affichée à côté du mode.
 *
 * Et la porte de sortie n'a jamais eu besoin de boutons : l'élève dit « je
 * veux un examen » et le tuteur bascule. La parole est déjà la surface
 * unique ; le serveur fait passer sa demande devant celle du tuteur
 * (cf. `session_mode.py`).
 */
interface SessionModeBannerProps {
  mode: TutorMode;
  /** Justification jointe par le tuteur à son dernier changement. */
  reason?: string;
}

export default function SessionModeBanner({ mode, reason }: SessionModeBannerProps) {
  const { label, icon, hint } = MODE_LABELS[mode];
  const [annonce, setAnnonce] = useState(reason || '');

  useEffect(() => {
    setAnnonce(reason || '');
  }, [reason, mode]);

  // La raison décrit une TRANSITION, pas l'état courant : elle s'efface.
  useEffect(() => {
    if (!annonce) return;
    const t = window.setTimeout(() => setAnnonce(''), 8000);
    return () => window.clearTimeout(t);
  }, [annonce]);

  return (
    <div
      className="flex items-center gap-2 text-[11px] text-white/40"
      role="status"
      aria-live="polite"
    >
      <span className="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-white/[0.07] bg-white/[0.04] px-2.5 py-1 font-bold text-white/60">
        <span aria-hidden>{icon}</span>
        {label}
      </span>
      <span className="min-w-0 flex-1 truncate">{annonce || hint}</span>
    </div>
  );
}
