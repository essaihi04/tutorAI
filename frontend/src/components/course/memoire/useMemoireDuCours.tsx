import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import type { CourseDeck } from '../types';
import CycleBloc, { type EtapeBloc } from './CycleBloc';
import FinDeSeance from './FinDeSeance';
import RappelDebutSeance from './RappelDebutSeance';
import { lireDebutSeance, noter, placeDansLesSeances, reactionsDe, seancesDe, type BlocCours, type QuestionMemoire, type RappelsDuJour } from './api';
import { DetecteurSaturation, useInactivite, type CauseSaturation } from './saturation';
import { direTexte, jouerReaction, taire } from './voix';
import { enteteDuCahier } from '../cahier';

/**
 * La mémoire longue dans le lecteur (11 novembre 2026), au niveau du COURS (`CoursePlayer`) :
 *
 * - au début (`actif` devient vrai) : 3 minutes de rappel de la MÊME matière, puis la séance (noté `seance_debut`) ;
 *   si l'élève s'était arrêté au milieu de la fin d'un bloc (cahier écrit, pas encore retrouvé…), il y reprend ;
 * - `blocAFermer` : la diapositive affichée termine un bloc pas encore bouclé → « Suite → » de `CourseFocusStage`
 *   appelle `fermerBloc()` au lieu de changer de diapositive : cahier → retrouver → exercice, puis `onAvancer` ;
 *   après le dernier bloc d'une séance : la fin de séance et la pause ;
 * - `signalerReponse` (chaque réponse jugée du cours, prédictions exclues) et une longue inactivité : à saturation,
 *   plus de nouvelle idée — le cahier et l'exercice du bloc tout de suite, puis la pause (noté, cause et action).
 * Un cours sans `seances` : `blocAFermer` toujours faux, `ecran` toujours nul ; rien ne change.
 */
type Ecran =
  | { genre: 'rappel'; rappels: RappelsDuJour }
  | { genre: 'cycle'; seance: number; bloc: number; etape: EtapeBloc; puis: 'suite' | 'pause' }
  | { genre: 'fin'; seance: number; raison: 'fin' | 'saturation' };

/** Sans geste ni réponse pendant 5 minutes alors que le cours attend : l'élève décroche. */
const INACTIVITE_MS = 5 * 60_000;

export function useMemoireDuCours({ deck, deckId, slideId, actif, onAvancer, onQuitter }: {
  deck: CourseDeck | null | undefined; deckId: string; slideId: string | undefined; actif: boolean;
  /** passer à la diapositive suivante (après la fin d'un bloc) */
  onAvancer: () => void;
  /** la pause : `avancer` vrai si la séance est finie (la reprise se fera à la diapositive suivante) */
  onQuitter: (avancer: boolean) => void;
}) {
  const seances = useMemo(() => seancesDe(deck), [deck]);
  const avecSeances = seances.length > 0;
  const [ecran, setEcran] = useState<Ecran | null>(null);
  const [, rafraichir] = useState(0);
  const reprise = useRef<Ecran | null>(null);
  const debutMs = useRef<number>(Date.now());
  const blocsFaits = useRef<Set<string>>(new Set());
  const demarre = useRef(false);
  const detecteur = useRef(new DetecteurSaturation());
  const avancer = useRef(onAvancer); avancer.current = onAvancer;
  const quitter = useRef(onQuitter); quitter.current = onQuitter;
  const place = useMemo(() => (slideId && avecSeances ? placeDansLesSeances(seances, slideId) : null), [seances, slideId, avecSeances]);

  const commencerSeance = useCallback((seance: number) => {
    debutMs.current = Date.now();
    detecteur.current.remettreAZero();
    void noter({ evenement: 'seance_debut', cours_id: deckId, seance_id: seances[seance]?.id, seance_index: seance });
  }, [deckId, seances]);

  // Le cours est mis en pause (retour à l'écran d'accueil du cours) : la prochaine reprise est une nouvelle séance.
  useEffect(() => { if (!actif) { demarre.current = false; setEcran(null); taire(); } }, [actif]);

  // Au début : rappel de la même matière, puis la séance (ou la reprise de la fin d'un bloc).
  useEffect(() => {
    if (!avecSeances || !actif || demarre.current) return;
    demarre.current = true;
    commencerSeance(place?.seance ?? 0);
    lireDebutSeance(deckId).then(d => {
      for (const [id, b] of Object.entries(d.progression?.blocs || {})) if (b.cahier && b.retrouver && b.exercice) blocsFaits.current.add(id);
      const r = d.progression?.reprise;
      reprise.current = r && r.etape !== 'cahier' ? { genre: 'cycle', seance: r.seance, bloc: r.bloc, etape: r.etape, puis: 'suite' } : null;
      if (d.rappels.questions.length) setEcran({ genre: 'rappel', rappels: d.rappels });
      else if (reprise.current) setEcran(reprise.current);
      else rafraichir(x => x + 1);
    }).catch(() => { /* sans serveur, le cours continue comme avant */ });
  }, [avecSeances, actif, deckId, place?.seance, commencerSeance]);

  const finDuCycle = useCallback((e: Extract<Ecran, { genre: 'cycle' }>) => {
    blocsFaits.current.add(seances[e.seance]?.blocs[e.bloc]?.id || '');
    detecteur.current.remettreAZero();
    taire();
    if (e.puis === 'pause') { setEcran({ genre: 'fin', seance: e.seance, raison: 'saturation' }); return; }
    if (e.bloc >= (seances[e.seance]?.blocs.length || 0) - 1) { setEcran({ genre: 'fin', seance: e.seance, raison: 'fin' }); return; }
    setEcran(null);
    // le cycle repris au début de la séance n'est pas forcément celui de la diapositive affichée : on avance seulement
    // si la diapositive affichée est bien la dernière du bloc bouclé
    if (place && place.seance === e.seance && place.bloc === e.bloc) avancer.current();
  }, [seances, place]);

  const blocAFermer = !!(avecSeances && place?.derniereDuBloc && !blocsFaits.current.has(place.blocCours.id));
  const fermerBloc = useCallback(() => {
    if (!place) { avancer.current(); return; }
    setEcran({ genre: 'cycle', seance: place.seance, bloc: place.bloc, etape: 'cahier', puis: 'suite' });
  }, [place]);

  const saturer = useCallback((cause: CauseSaturation) => {
    if (!avecSeances || !place || ecran) return;
    const fait = blocsFaits.current.has(place.blocCours.id);
    void noter({ evenement: 'saturation', cours_id: deckId, seance_id: place.seanceCours.id, bloc_id: place.blocCours.id,
      bloc_index: place.bloc, seance_index: place.seance, cause, action: fait ? 'pause' : 'cahier' });
    setEcran(fait ? { genre: 'fin', seance: place.seance, raison: 'saturation' }
      : { genre: 'cycle', seance: place.seance, bloc: place.bloc, etape: 'cahier', puis: 'pause' });
  }, [avecSeances, place, ecran, deckId]);

  const signalerReponse = useCallback((r: { correct: boolean | null; dureeMs?: number; lectureMs?: number }) => {
    const cause = detecteur.current.reponse(r);
    if (cause) saturer(cause);
  }, [saturer]);
  useInactivite(avecSeances && actif && !ecran, () => saturer('inactivite'), INACTIVITE_MS);

  const reactions = useCallback((q: QuestionMemoire, j?: number) => reactionsDe(deck, q, j), [deck]);

  let rendu: ReactNode = null;
  if (ecran?.genre === 'rappel') {
    rendu = <RappelDebutSeance rappels={ecran.rappels} onDire={direTexte} onJouer={jouerReaction} onFini={() => { taire(); setEcran(reprise.current); }} />;
  } else if (ecran?.genre === 'cycle') {
    const s = seances[ecran.seance];
    const b: BlocCours | undefined = s?.blocs[ecran.bloc];
    if (b) {
      const e = ecran;
      rendu = <CycleBloc key={`${s.id}:${b.id}`} bloc={b} etapeInitiale={e.etape} titreCours={deck?.title} onDire={direTexte} onJouer={jouerReaction} reactions={reactions}
        entetes={id => enteteDuCahier(deck, id)}
        place={{ coursId: deckId, seanceId: s.id, seance: e.seance, nbSeances: seances.length, bloc: e.bloc, nbBlocs: s.blocs.length }}
        onFini={() => finDuCycle(e)}
        // fermé par l'élève (12 novembre 2026) : le cours reprend ; le serveur garde ce qui n'est pas fait (reprise)
        onFermer={() => finDuCycle({ ...e, puis: 'suite' })} />;
    }
  } else if (ecran?.genre === 'fin') {
    const e = ecran;
    rendu = <FinDeSeance coursId={deckId} seance={e.seance} seances={seances} debutMs={debutMs.current} raison={e.raison}
      onPause={() => { setEcran(null); quitter.current(e.raison === 'fin'); }}
      onContinuer={() => { setEcran(null); commencerSeance(e.seance + 1); avancer.current(); }} />;
  }

  return { avecSeances, place, nbSeances: seances.length, ecran: rendu, blocAFermer, fermerBloc, signalerReponse };
}
