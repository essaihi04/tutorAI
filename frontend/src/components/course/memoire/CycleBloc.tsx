import { useEffect, useMemo, useRef, useState } from 'react';
import QuestionMemoire, { CRAIE, Formule, type ResultatQuestion } from './QuestionMemoire';
import { noter, type BlocCours, type QuestionMemoire as Q, type ReponsesPreparees } from './api';
import type { ReactionPreparee } from '../types';
import { DetecteurSaturation, PHRASES_SATURATION, tempsDeLectureMs, useInactivite, type CauseSaturation } from './saturation';

/**
 * La fin d'un bloc (skill `cours-concentration`, « Memory and rhythm ») : le cours s'arrête et trois temps se suivent,
 * toujours les mêmes :
 *   1. **cahier** — le tableau du cahier montre les lignes du bloc ; l'élève copie puis appuie « ✍️ C'est écrit » ;
 *   2. **retrouver** — cahier fermé, il redonne de mémoire la formule ou la définition (réponse libre jugée en direct) ;
 *   3. **exercice** du bloc.
 * Chaque temps est noté (bloc, durée, réponse, verdict). L'élève sait toujours où il est (séance n/N, bloc n/3) et
 * combien de temps il reste.
 */

export type EtapeBloc = 'cahier' | 'retrouver' | 'exercice';
const ORDRE: EtapeBloc[] = ['cahier', 'retrouver', 'exercice'];
/** Durée moyenne d'un bloc (explication + cahier + retrouver + exercice), pour dire le temps qui reste. */
export const MINUTES_PAR_BLOC = 9;

/** « Séance 2/5 · Bloc 1/3 · encore ~18 min » : où l'élève en est, toujours visible. */
export function OuEnEstOn({ seance, nbSeances, bloc, nbBlocs, etape }: { seance: number; nbSeances: number; bloc: number; nbBlocs: number; etape?: string }) {
  const reste = Math.max(1, (nbBlocs - bloc) * MINUTES_PAR_BLOC - (etape === 'exercice' ? 6 : etape === 'retrouver' ? 5 : etape === 'cahier' ? 4 : 0));
  return (
    <div className="flex flex-wrap items-center gap-2 text-xs text-white/60" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <span className="rounded-full bg-white/10 px-2.5 py-1">Séance {seance + 1}/{nbSeances}</span>
      <span className="flex items-center gap-1 rounded-full bg-white/10 px-2.5 py-1">
        Bloc {bloc + 1}/{nbBlocs}
        <span className="ml-1 flex gap-0.5">{Array.from({ length: nbBlocs }, (_, i) => (
          <span key={i} className={`h-1.5 w-3 rounded-full ${i < bloc ? 'bg-emerald-300/80' : i === bloc ? 'bg-cyan-300' : 'bg-white/20'}`} />
        ))}</span>
      </span>
      {etape && (
        <span className="flex gap-1">{ORDRE.map(e => (
          <span key={e} className={`rounded-full px-2 py-0.5 ${e === etape ? 'bg-cyan-400/25 text-cyan-100' : ORDRE.indexOf(e) < ORDRE.indexOf(etape as EtapeBloc) ? 'text-emerald-200/70' : 'text-white/35'}`}>
            {e === 'cahier' ? '✍️ Cahier' : e === 'retrouver' ? '🧠 Retrouver' : '✏️ Exercice'}
          </span>
        ))}</span>
      )}
      <span className="ml-auto text-white/45">encore ~{reste} min</span>
    </div>
  );
}

/** Le tableau du cahier : les lignes du bloc, écrites à la craie ; l'élève copie puis appuie « C'est écrit ». */
export function TableauCahier({ bloc, onEcrit }: { bloc: BlocCours; onEcrit: (dureeS: number) => void }) {
  const debut = useRef(Date.now());
  const lignes = bloc.cahier || [];
  useEffect(() => { debut.current = Date.now(); }, [bloc.id]);
  return (
    <div className="flex flex-col gap-4">
      <div>
        <p className="text-xs uppercase tracking-wide text-white/45" style={{ fontFamily: 'system-ui, sans-serif' }}>Le cours s’arrête : recopie dans ton cahier</p>
        {bloc.titre && <h3 className="mt-1 text-2xl underline decoration-amber-200/40 underline-offset-4" style={{ fontFamily: CRAIE, color: '#fef3c7' }}>{bloc.titre}</h3>}
      </div>
      <div className="rounded-2xl border border-amber-100/15 bg-[#1d2b22] p-5 shadow-inner" style={{ fontFamily: CRAIE }}>
        {lignes.length ? (
          <ol className="space-y-3">
            {lignes.map((l, i) => (
              <li key={i} className="text-xl leading-snug text-[#f5f1dc] md:text-2xl" dir="auto"><Formule t={l.texte} /></li>
            ))}
          </ol>
        ) : <p className="text-lg text-white/60">Écris avec tes mots ce que tu viens de comprendre.</p>}
      </div>
      <button type="button" onClick={() => onEcrit(Math.round((Date.now() - debut.current) / 1000))}
        className="self-end rounded-full bg-cyan-400/90 px-7 py-3 text-base font-bold text-slate-950 shadow-lg hover:bg-cyan-300"
        style={{ fontFamily: 'system-ui, sans-serif' }}>
        ✍️ C’est écrit
      </button>
    </div>
  );
}

export interface PlaceBloc { coursId: string; seanceId: string; seance: number; nbSeances: number; bloc: number; nbBlocs: number }

/**
 * Les trois temps de la fin d'un bloc. `etapeInitiale` : là où l'élève s'était arrêté.
 * `onSaturation` : deux réponses fausses de suite, réponses trop rapides ou longue inactivité (déjà noté ici) ;
 * le lecteur passe alors à la pause s'il le veut. `onFini` : le bloc est bouclé.
 */
export default function CycleBloc({ bloc, place, etapeInitiale = 'cahier', titreCours = '', onDire, onJouer, reactions, onFini, onSaturation }: {
  bloc: BlocCours; place: PlaceBloc; etapeInitiale?: EtapeBloc; titreCours?: string;
  onDire?: (parole: string) => void; onJouer?: (r: ReactionPreparee) => void;
  /** les réactions préparées d'une question (`reactionsDe`), `j` : l'affirmation d'un vrai/faux */
  reactions?: (q: Q, j?: number) => ReponsesPreparees | undefined;
  onFini: () => void; onSaturation?: (cause: CauseSaturation) => void;
}) {
  const sansRetrouver = !bloc.retrouver?.prompt;
  const sansExercice = !bloc.exercice?.prompt;
  const premiere = (e: EtapeBloc): EtapeBloc | null => {
    for (const x of ORDRE.slice(ORDRE.indexOf(e))) {
      if (x === 'retrouver' && sansRetrouver) continue;
      if (x === 'exercice' && sansExercice) continue;
      return x;
    }
    return null;
  };
  const [etape, setEtape] = useState<EtapeBloc | null>(() => premiere(etapeInitiale));
  const [alerte, setAlerte] = useState<CauseSaturation | null>(null);
  const detecteur = useRef(new DetecteurSaturation());
  const base = { cours_id: place.coursId, seance_id: place.seanceId, bloc_id: bloc.id, bloc_index: place.bloc, seance_index: place.seance };

  useEffect(() => { if (etape === null) onFini(); }, [etape]); // eslint-disable-line react-hooks/exhaustive-deps

  const saturer = (cause: CauseSaturation, action: 'exercice' | 'pause') => {
    void noter({ evenement: 'saturation', ...base, cause, action });
    setAlerte(cause);
    onSaturation?.(cause);
  };
  useInactivite(etape !== null, () => saturer('inactivite', etape === 'exercice' ? 'pause' : 'exercice'));

  const suivante = () => setEtape(e => {
    const i = e ? ORDRE.indexOf(e) : ORDRE.length;
    return i + 1 < ORDRE.length ? premiere(ORDRE[i + 1]) : null;
  });

  const resultat = (genre: 'retrouver' | 'exercice_bloc', q: { prompt: string; competence_id?: string; type?: string }, r: ResultatQuestion) => {
    void noter({ evenement: genre, ...base, competence_id: q.competence_id, enonce: q.prompt, type: q.type,
      reponse: r.reponse, reponse_2: r.reponse_2, correct: r.correct, correct_2: r.correct_2 ?? null, duree_s: r.duree_s });
    const lecture = tempsDeLectureMs(q.prompt);
    let cause = detecteur.current.reponse({ correct: r.correct, dureeMs: r.duree_s * 1000, lectureMs: lecture });
    if (!cause && r.correct === false) cause = detecteur.current.reponse({ correct: r.correct_2 ?? null });
    if (cause) saturer(cause, genre === 'retrouver' ? 'exercice' : 'pause');
  };

  if (!etape) return null;
  return (
    <div className="flex h-full min-h-0 flex-col gap-4 overflow-y-auto rounded-2xl border border-white/15 bg-[#14201a]/95 p-5 text-white md:p-7">
      <OuEnEstOn seance={place.seance} nbSeances={place.nbSeances} bloc={place.bloc} nbBlocs={place.nbBlocs} etape={etape} />
      {alerte && <p className="rounded-lg bg-sky-400/10 px-3 py-2 text-sm text-sky-100" style={{ fontFamily: 'system-ui, sans-serif' }}>{PHRASES_SATURATION[alerte]}</p>}
      {etape === 'cahier' && (
        <TableauCahier bloc={bloc} onEcrit={duree => { void noter({ evenement: 'cahier', ...base, duree_s: duree }); suivante(); }} />
      )}
      {etape === 'retrouver' && bloc.retrouver && (
        <QuestionMemoire mode="retrouver" question={bloc.retrouver} titre={bloc.titre || titreCours} deckId={place.coursId} onDire={onDire}
          onJouer={onJouer} onResultat={r => resultat('retrouver', bloc.retrouver!, r)} onSuite={suivante} />
      )}
      {etape === 'exercice' && bloc.exercice && (
        <ExerciceDuBloc exercice={bloc.exercice} competenceId={bloc.exercice.competence_id || bloc.retrouver?.competence_id}
          titre={bloc.titre || titreCours} deckId={place.coursId} onDire={onDire} onJouer={onJouer} reactions={reactions}
          onResultat={(q, r) => resultat('exercice_bloc', q, r)} onSuite={suivante}
          libelleFin={place.bloc + 1 >= place.nbBlocs ? 'Terminer la séance ✓' : 'Bloc suivant →'} />
      )}
    </div>
  );
}

/** L'exercice du bloc : QCM, réponse libre, ou vrai/faux en affirmations posées une par une (`statements`). */
function ExerciceDuBloc({ exercice, competenceId, titre, deckId, onDire, onJouer, reactions, onResultat, onSuite, libelleFin }: {
  exercice: Q; competenceId?: string; titre: string; deckId: string;
  onDire?: (parole: string) => void; onJouer?: (r: ReactionPreparee) => void;
  reactions?: (q: Q, j?: number) => ReponsesPreparees | undefined;
  onResultat: (q: Q & { competence_id?: string }, r: ResultatQuestion) => void; onSuite: () => void; libelleFin: string;
}) {
  const parties = useMemo<{ q: Q; j?: number }[]>(() => exercice.statements?.length
    ? exercice.statements.map((st, j) => ({ j, q: { id: `s${j}`, type: 'vrai_faux', prompt: st.text, correct: st.correct, explanation: st.explanation } }))
    : [{ q: exercice }], [exercice]);
  const [k, setK] = useState(0);
  const p = parties[Math.min(k, parties.length - 1)];
  const derniere = k >= parties.length - 1;
  return (
    <>
      {exercice.statements?.length ? (
        <p className="text-sm text-white/60" style={{ fontFamily: 'system-ui, sans-serif' }} dir="auto">
          <Formule t={exercice.prompt} /> <span className="ml-2 rounded-full bg-white/10 px-2 py-0.5 text-xs">{k + 1}/{parties.length}</span>
        </p>
      ) : null}
      <QuestionMemoire key={k} mode="exercice" question={p.q} titre={titre} deckId={deckId} onDire={onDire} onJouer={onJouer}
        reponses={reactions?.(exercice, p.j)}
        onResultat={r => onResultat({ ...p.q, competence_id: competenceId }, r)}
        onSuite={() => (derniere ? onSuite() : setK(x => x + 1))} libelleSuite={derniere ? libelleFin : 'Affirmation suivante →'} />
    </>
  );
}
