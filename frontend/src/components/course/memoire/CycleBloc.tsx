import { useEffect, useMemo, useRef, useState } from 'react';
import QuestionMemoire, { CRAIE, Formule, type ResultatQuestion } from './QuestionMemoire';
import { noter, type BlocCours, type QuestionMemoire as Q, type ReponsesPreparees } from './api';
import type { ReactionPreparee } from '../types';
import type { EnteteCahier } from '../cahier';
import { taire } from './voix';
import SansDefilement from '../SansDefilement';
import FiguresCahier from '../FigureCahier';
import { invitationCahier } from './invitationsCahier';
import { partiesDuCahier, cahierNumerote, cahierTitre } from './partiesDuCahier';
import { DetecteurSaturation, PHRASES_SATURATION, tempsDeLectureMs, useInactivite, type CauseSaturation } from './saturation';

/**
 * La fin d'un bloc (skill `cours-concentration`, « Memory and rhythm ») : le cours s'arrête et les temps de
 * `ETAPES_FIN_DE_BLOC` se suivent — depuis le 13 novembre 2026, le cahier seul ; à l'origine trois :
 *   1. **cahier** — le tableau du cahier montre les lignes du bloc ; l'élève copie puis appuie « ✍️ C'est écrit » ;
 *   2. **retrouver** — cahier fermé, il redonne de mémoire la formule ou la définition (réponse libre jugée en direct) ;
 *   3. **exercice** du bloc.
 * Chaque temps est noté (bloc, durée, réponse, verdict). L'élève sait toujours où il est (séance n/N, bloc n/3) et
 * combien de temps il reste.
 */

export type EtapeBloc = 'cahier' | 'retrouver' | 'exercice';
/**
 * Les temps joués aujourd'hui (user rule, 13 novembre 2026) : le bloc se ferme sur le **cahier** seul. « Retrouver »
 * juste après avoir recopié n'est pas encore de la mémoire, et l'exercice du bloc rajoutait des questions là où le
 * cours n'en garde qu'une par bloc (skill `professeur`, règle 27). Les deux restent dans les cours (`bloc.retrouver`,
 * `bloc.exercice`, leurs réactions et leurs énoncés) pour l'étape de fin de cours : pour les rejouer ici, les remettre
 * dans cette liste.
 */
export const ETAPES_FIN_DE_BLOC: EtapeBloc[] = ['cahier'];
const ORDRE = ETAPES_FIN_DE_BLOC;
/** Durée moyenne d'un bloc (explication + cahier), pour dire le temps qui reste. */
export const MINUTES_PAR_BLOC = 5;

/** « Séance 2/5 · Bloc 1/3 · encore ~18 min » : où l'élève en est, toujours visible. */
export function OuEnEstOn({ seance, nbSeances, bloc, nbBlocs, etape }: { seance: number; nbSeances: number; bloc: number; nbBlocs: number; etape?: string }) {
  const reste = Math.max(1, (nbBlocs - bloc) * MINUTES_PAR_BLOC - (etape === 'exercice' ? 6 : etape === 'retrouver' ? 5 : etape === 'cahier' ? 4 : 0));
  // une seule étape : pas de fil « Cahier · Retrouver · Exercice » à montrer
  const fil = ORDRE.length > 1;
  return (
    <div className="flex flex-wrap items-center gap-2 text-xs text-white/60" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <span className="rounded-full bg-white/10 px-2.5 py-1">Séance {seance + 1}/{nbSeances}</span>
      <span className="flex items-center gap-1 rounded-full bg-white/10 px-2.5 py-1">
        Bloc {bloc + 1}/{nbBlocs}
        <span className="ml-1 flex gap-0.5">{Array.from({ length: nbBlocs }, (_, i) => (
          <span key={i} className={`h-1.5 w-3 rounded-full ${i < bloc ? 'bg-emerald-300/80' : i === bloc ? 'bg-cyan-300' : 'bg-white/20'}`} />
        ))}</span>
      </span>
      {etape && fil && (
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

/**
 * Le tableau du cahier : les lignes du bloc, écrites à la craie ; l'élève copie puis appuie « C'est écrit ».
 * Partie par partie (20 novembre 2026, `partiesDuCahier.ts`) : seule la partie à écrire est montrée, avec son dessin ;
 * « C'est écrit » la marque écrite et fait apparaître la suivante ; la dernière ferme le cahier du bloc. ◀ / ▶ ne
 * parcourent que les parties déjà écrites et celle à écrire : une partie pas encore atteinte n'apparaît jamais.
 */
export function TableauCahier({ bloc, onEcrit, entetes, relecture }: { bloc: BlocCours; onEcrit: (dureeS: number) => void;
  /** le plan du cahier (12 novembre 2026) : titre du cours, parties numérotées, diapositives numérotées */
  entetes?: (slideId: string) => EnteteCahier | undefined;
  /** Relire le cahier d'un bloc précédent (20 novembre 2026) : toutes ses parties se parcourent, rien n'est à écrire ;
   *  ce bouton prend la place de « C'est écrit » (revenir au bloc en cours). */
  relecture?: { libelle: string; onRetour: () => void } }) {
  const debut = useRef(Date.now());
  const lignes = useMemo(() => bloc.cahier || [], [bloc.cahier]);
  const figures = useMemo(() => bloc.cahier_figures || [], [bloc.cahier_figures]);
  // Une ligne par diapositive du bloc : chaque ligne sous le titre de sa diapositive (et de sa partie quand on y entre) ;
  // sinon les titres d'abord, puis les lignes. Un titre déjà copié dans le bloc ne se répète pas.
  const plan = entetes ? bloc.slide_ids.map(id => entetes(id)) : [];
  // un cahier numéroté (« 1. », « 2. »…) se découpe toujours par ses numéros, même s'il a autant de lignes que de
  // diapositives (audit des cahiers, 20 novembre 2026)
  const parLigne = !!entetes && plan.every(Boolean) && lignes.length === bloc.slide_ids.length && !cahierNumerote(lignes);
  const parties = useMemo(() => partiesDuCahier(lignes, figures, parLigne), [lignes, figures, parLigne]);
  /** la partie à écrire (toutes celles d'avant sont écrites) */
  const n = parties.length;
  const [aEcrire, setAEcrire] = useState(relecture ? n - 1 : 0);
  /** la partie montrée, jamais au-delà de celle à écrire */
  const [vue, setVue] = useState(0);
  useEffect(() => { debut.current = Date.now(); setAEcrire(relecture ? n - 1 : 0); setVue(0); }, [bloc.id]); // eslint-disable-line react-hooks/exhaustive-deps
  const partie = parties[Math.min(vue, n - 1)];
  const dejaEcrite = vue < aEcrire;
  const ecrit = () => {
    if (dejaEcrite) return;
    if (aEcrire >= n - 1) { onEcrit(Math.round((Date.now() - debut.current) / 1000)); return; }
    setAEcrire(aEcrire + 1);
    setVue(aEcrire + 1);
  };
  const figuresVues = partie.figures.map(i => figures[i]);
  const tete = vue === 0 && plan.length > 0 ? plan.find(e => e?.cours)?.cours : undefined;
  const fleche = 'flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-white/10 text-base text-white/80 hover:bg-white/20 disabled:cursor-default disabled:opacity-25 disabled:hover:bg-white/10 court:h-7 court:w-7 court:text-xs';
  return (
    <div className="flex h-full min-h-0 flex-col gap-3 court:gap-1.5">
      {/* « C'est écrit » sur la ligne du titre : la hauteur gagnée va au texte du cahier */}
      <div className="flex shrink-0 items-end gap-3 court:items-center court:gap-2">
        <div className="min-w-0 flex-1">
          <p className={`text-xs uppercase tracking-wide court:hidden ${relecture ? 'text-amber-200/70' : 'text-white/45'}`} style={{ fontFamily: 'system-ui, sans-serif' }}>{relecture ? 'Relecture : un bloc déjà vu' : 'Le cours s’arrête : recopie dans ton cahier'}</p>
          {bloc.titre && <h3 className="mt-1 text-2xl underline decoration-amber-200/40 underline-offset-4 court:mt-0 court:truncate court:text-lg" style={{ fontFamily: CRAIE, color: '#fef3c7' }}><Formule t={bloc.titre} /></h3>}
        </div>
        {n > 1 && (
          <div data-parties-cahier className="flex shrink-0 items-center gap-1.5 court:gap-1" style={{ fontFamily: 'system-ui, sans-serif' }}>
            <button type="button" className={fleche} disabled={vue === 0} onClick={() => setVue(v => Math.max(0, v - 1))} aria-label="Partie précédente" title="Partie précédente">◀</button>
            <span className="flex flex-col items-center px-1 text-xs text-white/65">
              <span className="whitespace-nowrap">Partie {vue + 1}/{n}</span>
              {/* une marque par partie atteinte (écrite : vert ; montrée : cyan) — rien pour celles à venir */}
              <span className="mt-1 flex gap-0.5 court:hidden">{Array.from({ length: aEcrire + 1 }, (_, i) => (
                <span key={i} className={`h-1.5 w-3 rounded-full ${i === vue ? 'bg-cyan-300' : 'bg-emerald-300/80'}`} />
              ))}</span>
            </span>
            <button type="button" className={fleche} disabled={vue >= aEcrire} onClick={() => setVue(v => Math.min(aEcrire, v + 1))} aria-label="Partie suivante" title="Partie suivante">▶</button>
          </div>
        )}
        {relecture ? (
          <button type="button" onClick={relecture.onRetour}
            className="shrink-0 whitespace-nowrap rounded-full bg-amber-300/90 px-6 py-3 text-base font-bold text-slate-950 shadow-lg hover:bg-amber-200 court:px-3 court:py-1.5 court:text-sm"
            style={{ fontFamily: 'system-ui, sans-serif' }}>{relecture.libelle}</button>
        ) : <button type="button" onClick={ecrit} disabled={dejaEcrite}
          className={`shrink-0 rounded-full px-7 py-3 text-base font-bold shadow-lg court:px-4 court:py-1.5 court:text-sm ${dejaEcrite ? 'cursor-default bg-emerald-400/20 text-emerald-100' : 'bg-cyan-400/90 text-slate-950 hover:bg-cyan-300'}`}
          style={{ fontFamily: 'system-ui, sans-serif' }}>
          {dejaEcrite ? '✓ Déjà écrite' : '✍️ C’est écrit'}
        </button>}
      </div>
      {/* Le texte et les dessins tiennent chacun leur place (15 novembre 2026, « le texte du cahier est parfois trop petit
          avec le diagramme ») : un seul zoom pour les deux faisait rétrécir le texte dès que deux dessins s'empilaient.
          Le texte remplit sa colonne (SansDefilement), les dessins se partagent la hauteur de la leur. */}
      <div key={vue} className="flex min-h-0 flex-1 flex-col gap-4 rounded-2xl border border-amber-100/15 bg-[#1d2b22] p-3 shadow-inner md:flex-row md:p-4 court:flex-row court:gap-2 court:p-2" style={{ fontFamily: CRAIE }}>
        {/* les dessins de la partie (courbe, schéma, croquis) : à droite du texte sur grand écran, dessous sur téléphone */}
        <SansDefilement agrandirMax={1.6} zoomMin={0.7} className="min-w-0">
        {tete && (
          <div className="mb-3 text-center court:mb-1">
            <p className="text-3xl text-amber-200 underline decoration-amber-200/50 decoration-2 underline-offset-8 court:text-xl court:underline-offset-4">{tete.titre}</p>
            {tete.sousTitre && <p className="mt-2 text-lg italic text-[#e7e5c9] court:mt-0 court:text-base">{tete.sousTitre}</p>}
          </div>
        )}
        {parLigne ? (
          <div className="space-y-3">
            {partie.lignes.map(i => (
              <div key={i}>
                {plan[i]?.partie && <p className="mb-1 text-2xl text-rose-300">{plan[i]!.partie}</p>}
                <p className="pl-3 text-lg text-amber-100 underline decoration-amber-200/30 underline-offset-4">{plan[i]!.diapo}</p>
                <p className="pl-6 text-xl leading-snug text-[#f5f1dc] md:text-2xl" dir="auto"><Formule t={lignes[i].texte} /></p>
              </div>
            ))}
          </div>
        ) : lignes.length ? (
          <>
            {/* les titres de parties du cours, sauf si le cahier écrit déjà les siens (« I. », « II. ») : ils se
                doublaient, dans le désordre (« II. » au-dessus de « I. »), 20 novembre 2026 */}
            {vue === 0 && !cahierTitre(lignes) && plan.filter(e => e?.partie).map((e, i) => <p key={i} className="mb-1 text-2xl text-rose-300 court:text-xl">{e!.partie}</p>)}
            <ol className="space-y-3">
              {partie.lignes.map(i => (
                <li key={i} className="text-xl leading-snug text-[#f5f1dc] md:text-2xl" dir="auto"><Formule t={lignes[i].texte} /></li>
              ))}
            </ol>
          </>
        ) : <p className="text-lg text-white/60">Écris avec tes mots ce que tu viens de comprendre.</p>}
        </SansDefilement>
        {figuresVues.length > 0 && <FiguresCahier figures={figuresVues} remplir className="h-[42%] shrink-0 md:h-auto md:w-[38%] court:h-auto court:w-[38%]" />}
      </div>
    </div>
  );
}

/** Un bloc d'avant, relisible depuis la fin du bloc en cours : sa place dans le cours (séance, bloc, à partir de 0). */
export interface BlocPrecedent { bloc: BlocCours; seance: number; index: number }

export interface PlaceBloc { coursId: string; seanceId: string; seance: number; nbSeances: number; bloc: number; nbBlocs: number }

/**
 * Les trois temps de la fin d'un bloc. `etapeInitiale` : là où l'élève s'était arrêté.
 * `onSaturation` : deux réponses fausses de suite, réponses trop rapides ou longue inactivité (déjà noté ici) ;
 * le lecteur passe alors à la pause s'il le veut. `onFini` : le bloc est bouclé.
 */
export default function CycleBloc({ bloc, place, etapeInitiale = 'cahier', titreCours = '', onDire, onJouer, reactions, onFini, onSaturation, entetes, onFermer, precedents = [] }: {
  /** × en haut à droite (12 novembre 2026) : l'élève ferme la fenêtre et revient au cours */
  onFermer?: () => void;
  /** les blocs d'avant dans le cours, du plus ancien au plus récent : « ◀ Bloc précédent » relit leur cahier */
  precedents?: BlocPrecedent[];
  bloc: BlocCours; place: PlaceBloc; etapeInitiale?: EtapeBloc; titreCours?: string;
  entetes?: (slideId: string) => EnteteCahier | undefined;
  onDire?: (parole: string) => void; onJouer?: (r: ReactionPreparee) => void;
  /** les réactions préparées d'une question (`reactionsDe`), `j` : l'affirmation d'un vrai/faux */
  reactions?: (q: Q, j?: number) => ReponsesPreparees | undefined;
  onFini: () => void; onSaturation?: (cause: CauseSaturation) => void;
}) {
  const sansRetrouver = !bloc.retrouver?.prompt;
  const sansExercice = !bloc.exercice?.prompt;
  const premiere = (e: EtapeBloc): EtapeBloc | null => {
    // une étape qui n'est plus jouée (reprise enregistrée avant le 13 novembre 2026) : le bloc est bouclé
    if (!ORDRE.includes(e)) return null;
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
  // le cours s'arrête pour le cahier : le tuteur invite à écrire, en darija, une phrase différente à chaque fois
  // (invitationsCahier.ts, 14 novembre 2026) ; une seule fois par bloc
  const invite = useRef('');
  useEffect(() => {
    if (etape !== 'cahier' || invite.current === bloc.id) return;
    invite.current = bloc.id;
    onJouer?.(invitationCahier());
  }, [etape, bloc.id]); // eslint-disable-line react-hooks/exhaustive-deps

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
      reponse: r.reponse, reponse_2: r.reponse_2, correct: r.correct, correct_2: r.correct_2 ?? null, duree_s: r.duree_s, passee: r.passee || undefined });
    if (r.passee) return;   // passée : ni erreur ni signe de saturation
    const lecture = tempsDeLectureMs(q.prompt);
    let cause = detecteur.current.reponse({ correct: r.correct, dureeMs: r.duree_s * 1000, lectureMs: lecture });
    if (!cause && r.correct === false) cause = detecteur.current.reponse({ correct: r.correct_2 ?? null });
    if (cause) saturer(cause, genre === 'retrouver' ? 'exercice' : 'pause');
  };

  /**
   * Revenir en arrière (20 novembre 2026, demande de l'utilisateur) : « ◀ Bloc précédent » relit le cahier des blocs
   * d'avant, sans rien à réécrire ; le cahier du bloc en cours reste monté (caché), ses parties écrites ne se perdent pas.
   */
  const [relu, setRelu] = useState<number | null>(null);
  const lu = relu === null ? null : precedents[relu];
  const blocPrecedent = () => { if (!precedents.length) return; taire(); setRelu(r => (r === null ? precedents.length - 1 : Math.max(0, r - 1))); };
  const blocSuivant = () => setRelu(r => (r === null || r >= precedents.length - 1 ? null : r + 1));

  if (!etape) return null;
  const navBlocs = 'shrink-0 whitespace-nowrap rounded-full bg-white/10 px-3 py-1 text-xs text-white/75 hover:bg-white/20 disabled:cursor-default disabled:opacity-30 court:px-2 court:py-0.5';
  return (
    <div data-fenetre-cycle className="relative flex h-full min-h-0 flex-col gap-3 overflow-y-auto rounded-2xl border border-white/15 bg-[#14201a]/95 p-4 text-white md:p-5 court:gap-1.5 court:p-2">
      {onFermer && (
        <button type="button" onClick={() => { taire(); onFermer(); }} title="Fermer et revenir au cours" aria-label="Fermer"
          className="absolute right-3 top-3 z-10 flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-lg text-white/70 hover:bg-white/20 hover:text-white court:right-1.5 court:top-1.5 court:h-7 court:w-7 court:text-base">×</button>
      )}
      <div className={`flex items-center gap-2 ${onFermer ? 'pr-10' : ''}`}>
        {etape === 'cahier' && precedents.length > 0 && (
          <div data-blocs-precedents className="flex shrink-0 items-center gap-1" style={{ fontFamily: 'system-ui, sans-serif' }}>
            <button type="button" className={navBlocs} onClick={blocPrecedent} disabled={relu === 0} title="Relire le cahier du bloc d'avant">◀ Bloc précédent</button>
            {lu && <button type="button" className={navBlocs} onClick={blocSuivant} title="Bloc suivant">Bloc suivant ▶</button>}
          </div>
        )}
        <div className="min-w-0 flex-1">
          {lu
            ? <p className="text-xs text-amber-200/80" style={{ fontFamily: 'system-ui, sans-serif' }}>Relecture · Séance {lu.seance + 1}/{place.nbSeances} · Bloc {lu.index + 1}</p>
            : <OuEnEstOn seance={place.seance} nbSeances={place.nbSeances} bloc={place.bloc} nbBlocs={place.nbBlocs} etape={etape} />}
        </div>
      </div>
      {alerte && <p className="rounded-lg bg-sky-400/10 px-3 py-2 text-sm text-sky-100" style={{ fontFamily: 'system-ui, sans-serif' }}>{PHRASES_SATURATION[alerte]}</p>}
      {etape === 'cahier' && (
        // tout le cahier du bloc dans l'écran, sans défiler (user rule, 12 novembre 2026) : le texte s'ajuste dans TableauCahier
        <div className={`min-h-0 flex-1 flex-col ${lu ? 'hidden' : 'flex'}`}>
          <TableauCahier bloc={bloc} entetes={entetes} onEcrit={duree => { void noter({ evenement: 'cahier', ...base, duree_s: duree }); suivante(); }} />
        </div>
      )}
      {etape === 'cahier' && lu && (
        <div className="flex min-h-0 flex-1 flex-col">
          <TableauCahier key={lu.bloc.id} bloc={lu.bloc} entetes={entetes} onEcrit={() => {}}
            relecture={{ libelle: 'Mon bloc →', onRetour: () => setRelu(null) }} />
        </div>
      )}
      {etape === 'retrouver' && bloc.retrouver && (
        <QuestionMemoire mode="retrouver" question={bloc.retrouver} titre={bloc.titre || titreCours} deckId={place.coursId} onDire={onDire}
          suggestions={{ deck_id: place.coursId, slide_id: bloc.id, cle: 'retrouver' }}
          onJouer={onJouer} onResultat={r => resultat('retrouver', bloc.retrouver!, r)} onSuite={suivante} />
      )}
      {etape === 'exercice' && bloc.exercice && (
        <ExerciceDuBloc exercice={bloc.exercice} competenceId={bloc.exercice.competence_id || bloc.retrouver?.competence_id}
          titre={bloc.titre || titreCours} deckId={place.coursId} onDire={onDire} onJouer={onJouer} reactions={reactions} blocId={bloc.id}
          onResultat={(q, r) => resultat('exercice_bloc', q, r)} onSuite={suivante}
          libelleFin={place.bloc + 1 >= place.nbBlocs ? 'Terminer la séance ✓' : 'Bloc suivant →'} />
      )}
    </div>
  );
}

/** L'exercice du bloc : QCM, réponse libre, ou vrai/faux en affirmations posées une par une (`statements`). */
function ExerciceDuBloc({ exercice, competenceId, titre, deckId, onDire, onJouer, reactions, onResultat, onSuite, libelleFin, blocId }: {
  exercice: Q; competenceId?: string; titre: string; deckId: string; blocId: string;
  onDire?: (parole: string) => void; onJouer?: (r: ReactionPreparee) => void;
  reactions?: (q: Q, j?: number) => ReponsesPreparees | undefined;
  onResultat: (q: Q & { competence_id?: string }, r: ResultatQuestion) => void; onSuite: () => void; libelleFin: string;
}) {
  const parties = useMemo<{ q: Q; j?: number }[]>(() => exercice.statements?.length
    ? exercice.statements.map((st, j) => ({ j, q: { id: `s${j}`, type: 'vrai_faux', prompt: st.text, correct: st.correct, explanation: st.explanation,
      enonce_audio: st.enonce_audio, enonce_dit: st.enonce_dit,
      // la démonstration de l'exercice s'écrit après sa dernière affirmation
      demonstration: j === (exercice.statements?.length ?? 0) - 1 ? exercice.demonstration : undefined } }))
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
        reponses={reactions?.(exercice, p.j)} suggestions={{ deck_id: deckId, slide_id: blocId, cle: 'exercice_bloc' }}
        onResultat={r => onResultat({ ...p.q, competence_id: competenceId }, r)}
        onSuite={() => (derniere ? onSuite() : setK(x => x + 1))} libelleSuite={derniere ? libelleFin : 'Affirmation suivante →'} />
    </>
  );
}
