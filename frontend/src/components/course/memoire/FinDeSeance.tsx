import { useEffect, useRef } from 'react';
import { CRAIE } from './QuestionMemoire';
import { noter, type SeanceCours } from './api';

/**
 * La fin d'une séance (3 blocs, 25–30 min) ou la pause demandée par la saturation : une phrase chaleureuse, ce qui
 * vient ensuite, et la pause. L'élève reprendra là où il s'est arrêté (`progression().reprise` côté serveur).
 * Note `seance_fin` (durée, complète ou non) une seule fois.
 */
export default function FinDeSeance({ coursId, seance, seances, debutMs, raison = 'fin', onPause, onContinuer }: {
  coursId: string; seance: number; seances: SeanceCours[]; debutMs?: number; raison?: 'fin' | 'saturation';
  onPause: () => void; onContinuer?: () => void;
}) {
  const note = useRef(false);
  const s = seances[seance];
  const suivante = seances[seance + 1];
  const dureeMin = debutMs ? Math.max(1, Math.round((Date.now() - debutMs) / 60000)) : null;
  useEffect(() => {
    if (note.current || !s) return;
    note.current = true;
    void noter({ evenement: 'seance_fin', cours_id: coursId, seance_id: s.id, seance_index: seance, complete: raison === 'fin',
      duree_s: debutMs ? Math.round((Date.now() - debutMs) / 1000) : undefined, cause: raison === 'saturation' ? 'saturation' : undefined });
  }, [coursId, s, seance, raison, debutMs]);

  const pause = () => { void noter({ evenement: 'pause', cours_id: coursId, seance_id: s?.id, seance_index: seance, action: raison }); onPause(); };

  return (
    <div className="flex h-full min-h-0 flex-col items-center justify-center gap-5 rounded-2xl border border-white/15 bg-[#14201a]/95 p-6 text-center text-white">
      <p className="text-4xl">{raison === 'fin' ? '🌿' : '☕'}</p>
      <p className="max-w-xl text-3xl leading-snug" style={{ fontFamily: CRAIE, color: '#fef3c7' }}>
        {raison === 'fin'
          ? `Séance ${seance + 1} terminée${dureeMin ? ` en ${dureeMin} min` : ''} : beau travail, ce que tu as écrit et retrouvé va rester.`
          : 'On s’arrête là pour l’instant : ton cerveau a besoin de ranger ce qu’il a appris.'}
      </p>
      <div className="max-w-md rounded-xl bg-white/[0.06] px-4 py-3 text-sm text-white/70" style={{ fontFamily: 'system-ui, sans-serif' }}>
        {suivante || raison === 'saturation' ? (
          <>
            <p className="text-white/50">Ensuite</p>
            <p className="mt-1 text-white/85">
              {raison === 'saturation' ? `La suite de la séance ${seance + 1}${s?.titre ? ` — ${s.titre}` : ''}` : `Séance ${seance + 2}/${seances.length}${suivante?.titre ? ` — ${suivante.titre}` : ''}`}
            </p>
            <p className="mt-1 text-white/50">Elle commencera par 3 minutes de rappel. Tu reprendras exactement ici.</p>
          </>
        ) : <p className="text-white/85">C’était la dernière séance du chapitre. Les rappels des prochains jours garderont tout ça en mémoire.</p>}
      </div>
      <button type="button" autoFocus onClick={pause}
        className="rounded-full bg-cyan-400/90 px-8 py-3 text-base font-bold text-slate-950 shadow-lg hover:bg-cyan-300" style={{ fontFamily: 'system-ui, sans-serif' }}>
        ☕ Faire la pause
      </button>
      {onContinuer && suivante && raison === 'fin' && (
        <button type="button" onClick={onContinuer} className="text-xs text-white/40 underline underline-offset-4 hover:text-white/70" style={{ fontFamily: 'system-ui, sans-serif' }}>
          Je continue quand même
        </button>
      )}
    </div>
  );
}
