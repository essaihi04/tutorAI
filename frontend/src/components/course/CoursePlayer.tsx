import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import LiveBoard from '../session/LiveBoard';
import CourseFocusStage from './CourseFocusStage';
import { useColonneTuteur } from '../session/AIAvatar';
import { useMemoireDuCours } from './memoire/useMemoireDuCours';
import { MINUTES_PAR_BLOC } from './memoire/CycleBloc';
import { saveCourseProgress } from '../../services/api';
import { slideVersScript } from './slideVersScript';
import ClavierFlottant, { clavier, hauteurClavierTelephone, largeurClavier, useClavier } from './ClavierFlottant';
import { matiereDuClavier } from './ClavierScientifique';
import { enteteDuCahier } from './cahier';
import { entrerPleinEcran } from './pleinEcran';
import { diagnosticsDuRappel, diapoSuivante, type EtatGarde } from './parcours';

/**
 * Les questions posées à l'élève sur chaque diapositive sont suspendues pour
 * le moment : le cours se déroule d'une traite, voix et écriture ensemble.
 * Les remettre : passer à `true` (les manifestes les portent toujours).
 */
const QUESTIONS_DES_DIAPOSITIVES = false;
import type { ScientificControlCommand } from '../session/scientific/types';
import type {
  CourseActivity,
  CourseDeck,
  CourseProgressSnapshot,
  CourseSlide,
} from './types';

/**
 * Le cours se donne AU TABLEAU.
 *
 * Ce lecteur ne dessine plus de surface à lui. Il traduit chaque diapositive
 * en script (`slideVersScript`) et laisse `LiveBoard` la donner : le tableau
 * vert, l'écriture à la craie au rythme de la voix, le dessin, les figures et
 * les simulations, la loupe, le plein écran, la pause, et le coin où l'élève
 * lève la main. Tout cela existait déjà, éprouvé, dans le mode libre ; le
 * cours en avait une seconde version, plus pauvre, qui divergeait à chaque
 * retouche.
 *
 * Ce qui reste ici est ce que le tableau ne sait pas : le DECK. L'ordre des
 * diapositives, la progression enregistrée, le passage à la suivante — que
 * l'élève seul décide — et le bandeau de fin.
 */
interface CoursePlayerProps {
  deck: CourseDeck;
  progress?: CourseProgressSnapshot | null;
  language: 'fr' | 'ar' | 'mixed';
  /** Ce que le professeur vient de dire, repris tel quel dans le chat. */
  onNarration?: (text: string) => void;
  /** L'élève lève la main depuis le tableau : sa question part au tuteur. */
  onStudentQuestion?: (text: string) => void;
  /** Dernière réponse du tuteur — le tableau l'affiche dans son coin élève. */
  assistantReply?: string | null;
  /**
   * Le cours passe en plein écran : la page doit replier sa barre latérale.
   *
   * Le plein écran se pose en `fixed inset-0 z-[100]` et recouvre tout, chat
   * compris. La page a besoin de le savoir pour restaurer la colonne de
   * messages exactement comme elle était, une fois le cours refermé.
   */
  onFocusChange?: (focus: boolean) => void;
  tutorBusy?: boolean;
  externalAudioActive?: boolean;
  scientificControl?: ScientificControlCommand | null;
  onSimulationUpdate?: (state: any) => void;
  onComplete?: () => void;
  onRestart?: () => void;
  /**
   * `concentration` : l'écrit est fermé (titre et sous-titre seuls), l'image ou la
   * simulation au centre, le tuteur 3D montre au rythme de la voix (`CourseFocusStage`).
   */
  mode?: 'tableau' | 'concentration';
  /** Monte le tuteur 3D dans le mode concentration (banc local). */
  tuteur3D?: boolean;
  /** La diapositive affichée change (relecture des profs sur le lien libre, 10 novembre 2026). */
  onSlideChange?: (slide: { id: string; title: string; position: number; total: number }) => void;
}

interface FlatSlide {
  activity: CourseActivity;
  activityIndex: number;
  slide: CourseSlide;
  slideIndex: number;
}

const clamp = (value: number, min: number, max: number) => Math.max(min, Math.min(max, value));

/** Le rappel sauté (ou revu) part au suivi des acquis : hors score, gardé dans le trajet (skill `suivi-des-acquis`). */
function noterRappel(deckId: string, slide: CourseSlide, type: 'rappel_saute' | 'rappel_revu') {
  let jeton = '';
  try { jeton = localStorage.getItem('token') || ''; } catch { /* sans jeton */ }
  void fetch('/api/v1/course-player/acquis', {
    method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton}` },
    body: JSON.stringify({
      deck_id: deckId, slide_id: slide.id, slide_title: slide.title || '', cle: 'rappel', type, correct: null, tentative: 1,
      reponse: type === 'rappel_saute' ? `diagnostic réussi du premier coup : ${diagnosticsDuRappel(slide).join(', ')}`.slice(0, 500) : 'revu à la demande',
      methodes: {},
    }),
  }).catch(() => { /* le suivi ne doit jamais gêner l'élève */ });
}

export default function CoursePlayer({
  deck,
  progress,
  language,
  onNarration,
  onStudentQuestion,
  assistantReply,
  onFocusChange,
  tutorBusy = false,
  externalAudioActive = false,
  scientificControl,
  onSimulationUpdate,
  onComplete,
  onRestart,
  mode = 'tableau',
  tuteur3D = false,
  onSlideChange,
}: CoursePlayerProps) {
  const COLONNE_TUTEUR = useColonneTuteur();   // plus étroite sur téléphone en paysage
  const flatSlides = useMemo<FlatSlide[]>(() =>
    deck.activities.flatMap((activity, activityIndex) =>
      (activity.slides || []).map((slide, slideIndex) => ({
        activity,
        activityIndex,
        // Questions suspendues au tableau : la diapositive se lit d'une traite. En mode concentration, elles
        // s'affichent à la fin de la voix et le tuteur réagit à chaque réponse (CourseFocusStage).
        slide: QUESTIONS_DES_DIAPOSITIVES || mode === 'concentration' ? slide : { ...slide, question: undefined },
        slideIndex,
      })),
    ), [deck.activities, mode]);

  const storageKey = `course-player:${deck.id}`;
  const initialIndex = useMemo(() => {
    // Un cours déjà validé reste acquis, mais une nouvelle ouverture doit
    // proposer une révision complète depuis la première diapositive.
    if (progress?.status === 'completed') return 0;
    const targetId = progress?.current_slide_id;
    if (targetId) {
      const found = flatSlides.findIndex(item => item.slide.id === targetId || item.slide.stable_id === targetId);
      if (found >= 0) return found;
    }
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
      return clamp(Number(saved.index || 0), 0, Math.max(0, flatSlides.length - 1));
    } catch {
      return 0;
    }
  }, [flatSlides, progress?.current_slide_id, progress?.status, storageKey]);

  const [index, setIndex] = useState(initialIndex);
  const [started, setStarted] = useState(false);
  const [completedSlideIds, setCompletedSlideIds] = useState<string[]>(progress?.completed_slide_ids || []);
  const [courseCompleted, setCourseCompleted] = useState(false);
  /**
   * Le cours prend l'écran dès qu'il démarre, et le garde d'une diapositive à
   * l'autre. C'est le tableau qui tient l'état ; on n'en garde ici qu'une
   * intention de départ, pour que la diapo suivante n'annule pas le choix de
   * l'élève de sortir du plein écran.
   */
  const [pleinEcranVoulu, setPleinEcranVoulu] = useState(false);
  const completedSlideIdsRef = useRef(completedSlideIds);
  const current = flatSlides[index];
  /**
   * Les rappels déjà sus (`concentration.rappel`, 18 novembre 2026) : en concentration, « Suite → » saute un rappel
   * dont le diagnostic a été réussi du premier coup. `sautes` : où l'élève est arrivé et ce qui a été sauté (le bouton
   * « 🔁 Revoir le rappel » y reste) ; `revus` : les rappels rouverts à la demande, jamais resautés.
   */
  const deckIdSuivi = deck.stable_id || deck.id;
  const [sautes, setSautes] = useState<{ arrivee: number; ids: string[] } | null>(null);
  const revus = useRef<Set<string>>(new Set());
  const memoireRef = useRef<{ fermerBlocDe: (id: string) => boolean } | null>(null);
  const lireEtatGarde = useCallback((slideId: string, cle: string): EtatGarde => {
    try { return JSON.parse(localStorage.getItem(`reponse:${deckIdSuivi}:${slideId}:${cle}`) || 'null') as EtatGarde; } catch { return null; }
  }, [deckIdSuivi]);

  useEffect(() => {
    completedSlideIdsRef.current = completedSlideIds;
  }, [completedSlideIds]);

  useEffect(() => {
    if (current && onSlideChange) onSlideChange({ id: current.slide.id, title: current.slide.title || '', position: index + 1, total: flatSlides.length });
  }, [current, index, flatSlides.length, onSlideChange]);

  const persist = useCallback((
    nextIndex: number,
    audioPositionMs = 0,
    status: 'in_progress' | 'completed' = 'in_progress',
    completedIds = completedSlideIdsRef.current,
  ) => {
    const item = flatSlides[nextIndex] || flatSlides[flatSlides.length - 1];
    if (!item) return;
    const payload = {
      deck_id: deck.id,
      lesson_id: deck.lesson_id,
      activity_id: item.activity.id,
      slide_id: item.slide.id,
      audio_position_ms: Math.max(0, Math.round(audioPositionMs)),
      slide_state: { index: nextIndex },
      completed_slide_ids: completedIds,
      status,
    } as const;
    localStorage.setItem(storageKey, JSON.stringify({ ...payload, index: nextIndex }));
    void saveCourseProgress(payload).catch(() => {});
  }, [deck.id, deck.lesson_id, flatSlides, storageKey]);

  /** La diapositive courante, traduite pour le tableau. */
  const script = useMemo(
    () => (current ? slideVersScript(current.slide, language) : { steps: [] }),
    [current, language],
  );

  /**
   * L'image de la diapo suivante est récupérée pendant la courante.
   *
   * Une `<img>` montée sur une source pas encore en cache s'affiche vide le
   * temps du téléchargement : le tableau clignote au changement de diapo.
   * Le délai laisse d'abord le réseau à ce qui est attendu maintenant.
   */
  const imagePrechargeeRef = useRef<HTMLImageElement | null>(null);
  useEffect(() => {
    if (!started) return;
    const suivante = flatSlides[index + 1]?.slide.visual;
    if (suivante?.kind !== 'image' || !suivante.url) return;
    const differe = window.setTimeout(() => {
      const image = new Image();
      image.decoding = 'async';
      image.src = suivante.url as string;
      imagePrechargeeRef.current = image;
    }, 1500);
    return () => clearTimeout(differe);
  }, [flatSlides, index, started]);

  /**
   * Ce que le professeur dit rejoint le chat.
   *
   * Le tableau parle, il n'archive pas : sans ce report, la colonne de gauche
   * resterait vide toute la leçon et l'élève qui la rouvre ne retrouverait
   * rien de ce qui vient d'être dit. La question de la diapositive part avec,
   * puisqu'elle est posée à l'oral au tableau.
   */
  const narrationEnvoyeeRef = useRef<string | null>(null);
  const correctionEnvoyeeRef = useRef<string | null>(null);
  useEffect(() => {
    if (!started || !current || !onNarration) return;
    const cle = `${current.slide.id}:${language}`;
    if (narrationEnvoyeeRef.current === cle) return;
    narrationEnvoyeeRef.current = cle;
    const parole = current.slide.speech_text || {};
    const dit = (parole[language] || parole.mixed || parole.fr || Object.values(parole)[0] || '').trim();
    const lignes: string[] = [];
    const enonce = current.slide.question?.prompt?.trim();
    if (enonce) {
      lignes.push(enonce);
      (current.slide.question?.options || []).forEach(option => lignes.push(`• ${option}`));
    } else if (dit) {
      // Sans interrogation, l'explication peut rejoindre le chat tout de
      // suite. Avec une question, elle n'y arrive qu'après la réponse.
      lignes.push(dit);
    }
    if (lignes.length) onNarration(lignes.join('\n'));
  }, [current, language, onNarration, started]);

  const archiverCorrectionApresReponse = useCallback(() => {
    if (!current || !onNarration || !current.slide.question?.prompt) return;
    const cle = `${current.slide.id}:${language}`;
    if (correctionEnvoyeeRef.current === cle) return;
    correctionEnvoyeeRef.current = cle;
    const parole = current.slide.speech_text || {};
    const dit = (parole[language] || parole.mixed || parole.fr || Object.values(parole)[0] || '').trim();
    if (dit) onNarration(dit);
  }, [current, language, onNarration]);

  const goToNext = useCallback(() => {
    if (!current) return;
    const slideId = current.slide.id;
    const nextCompleted = completedSlideIds.includes(slideId) ? completedSlideIds : [...completedSlideIds, slideId];
    completedSlideIdsRef.current = nextCompleted;
    setCompletedSlideIds(nextCompleted);
    if (index >= flatSlides.length - 1) {
      persist(index, 0, 'completed', nextCompleted);
      setCourseCompleted(true);
      onComplete?.();
      return;
    }
    let next = index + 1;
    if (mode === 'concentration') {
      const r = diapoSuivante(flatSlides.map(f => f.slide), index, lireEtatGarde, revus.current);
      // un rappel sauté fermait un bloc : le cahier de ce bloc d'abord, puis le cours revient ici (et saute)
      if (r.sautes.some(id => memoireRef.current?.fermerBlocDe(id))) return;
      next = r.index;
      if (r.sautes.length) {
        r.sautes.forEach(id => { const f = flatSlides.find(x => x.slide.id === id); if (f) noterRappel(deckIdSuivi, f.slide, 'rappel_saute'); });
        setSautes({ arrivee: next, ids: r.sautes });
      }
      if (next >= flatSlides.length) {
        persist(flatSlides.length - 1, 0, 'completed', nextCompleted);
        setCourseCompleted(true);
        onComplete?.();
        return;
      }
    }
    persist(next, 0, 'in_progress', nextCompleted);
    setIndex(next);
  }, [completedSlideIds, current, flatSlides, index, onComplete, persist, mode, lireEtatGarde, deckIdSuivi]);

  /** « 🔁 Revoir le rappel » : le premier rappel sauté s'ouvre ; « Suite → » repasse par les autres, puis revient. */
  const revoirRappel = useCallback(() => {
    if (!sautes) return;
    const i = flatSlides.findIndex(f => f.slide.id === sautes.ids[0]);
    if (i < 0) return;
    sautes.ids.forEach(id => revus.current.add(id));
    noterRappel(deckIdSuivi, flatSlides[i].slide, 'rappel_revu');
    setSautes(null);
    setCourseCompleted(false);
    setIndex(i);
    persist(i, 0, 'in_progress');
  }, [sautes, flatSlides, deckIdSuivi, persist]);

  const goToPrevious = useCallback(() => {
    if (index <= 0) return;
    const previous = index - 1;
    setCourseCompleted(false);
    setIndex(previous);
    persist(previous, 0, 'in_progress');
  }, [index, persist]);

  const restartFromBeginning = useCallback(() => {
    completedSlideIdsRef.current = [];
    setCompletedSlideIds([]);
    narrationEnvoyeeRef.current = null;
    setCourseCompleted(false);
    setIndex(0);
    setStarted(true);
    setPleinEcranVoulu(true);
    persist(0, 0, 'in_progress', []);
    onRestart?.();
  }, [onRestart, persist]);

  /** Le cours terminé rend l'écran : le bilan et la séance redeviennent visibles. */
  useEffect(() => { if (courseCompleted) setPleinEcranVoulu(false); }, [courseCompleted]);
  // Démonté en plein écran (fin de séance, changement de leçon), le composant
  // n'a plus l'occasion d'émettre `false` : la page garderait sa colonne de
  // messages repliée sans rien pour la rouvrir.
  useEffect(() => () => onFocusChange?.(false), [onFocusChange]);

  const commencer = useCallback(() => {
    setStarted(true);
    setPleinEcranVoulu(true);
    // Téléphone en paysage (16 novembre 2026) : la barre du navigateur prend un quart de la hauteur ; le plein écran
    // la cache et la rend au tableau. Demandé sur le geste de l'élève (obligatoire) ; refusé (iPhone) : rien ne change.
    if (window.matchMedia('(max-height: 520px) and (orientation: landscape) and (pointer: coarse)').matches) entrerPleinEcran();
  }, []);

  // En concentration, le cours prend toute la place dès qu'il démarre.
  useEffect(() => {
    if (mode === 'concentration' && started && !courseCompleted) onFocusChange?.(true);
  }, [mode, started, courseCompleted, onFocusChange]);

  // La mémoire longue (11 novembre 2026) : rappel de début de séance, fin de bloc (cahier → retrouver → exercice),
  // fin de séance et saturation. Un cours sans `seances` n'est pas touché.
  // le clavier flottant ouvert : la fin de bloc (cahier, retrouver, exercice) lui laisse sa place à droite
  const clavierOuvert = useClavier().ouvert;
  const placeClavier = largeurClavier(clavierOuvert);
  const memoire = useMemoireDuCours({
    deck, deckId: deck.stable_id || deck.id, slideId: current?.slide.id, actif: started && mode === 'concentration' && !courseCompleted,
    onAvancer: goToNext,
    onQuitter: (avancer) => { if (avancer) goToNext(); setStarted(false); },
  });
  memoireRef.current = memoire;
  // fenêtre de fin de bloc ouverte : sur téléphone, le tuteur 3D (qui n'y a pas de colonne) se cache au lieu de la
  // couvrir (AIAvatar.css, `body[data-fenetre-bloc]`) ; sa voix continue (14 novembre 2026)
  const fenetreBloc = started && !!memoire.ecran;
  useEffect(() => {
    if (!fenetreBloc) return;
    document.body.dataset.fenetreBloc = '1';
    return () => { delete document.body.dataset.fenetreBloc; };
  }, [fenetreBloc]);
  if (!current) {
    return <div className="h-full grid place-items-center text-white/60">Ce cours ne contient aucune diapositive.</div>;
  }

  const activitySlideCount = current.activity.slides.length;
  const totalProgress = Math.round(((index + 1) / Math.max(1, flatSlides.length)) * 100);

  /**
   * Les commandes du DECK, posées dans la barre du bas du tableau.
   *
   * Elles avaient leur propre barre : deux barres pour un seul cours, deux
   * « Suivant » à des endroits différents. Le tableau les accueille désormais
   * dans son coin élève, à côté de la pause et de « Poser une question ».
   */
  const ouEnEstOn = memoire.place ? (() => {
    const p = memoire.place;
    const nbBlocs = p.seanceCours.blocs.length;
    return (
      // compact (12 novembre 2026 : la barre du bas tient sur une ligne) ; le détail est dans la bulle d'aide
      <span className="whitespace-nowrap px-1 text-[11px] tabular-nums text-amber-100/70"
        title={`Séance ${p.seance + 1}/${memoire.nbSeances} · Bloc ${p.bloc + 1}/${nbBlocs} · encore ~${(nbBlocs - p.bloc) * MINUTES_PAR_BLOC} min${p.seanceCours.titre ? ` — ${p.seanceCours.titre}` : ''}`}>
        S{p.seance + 1}/{memoire.nbSeances} · B{p.bloc + 1}/{nbBlocs} · ~{(nbBlocs - p.bloc) * MINUTES_PAR_BLOC} min
      </span>
    );
  })() : null;

  const commandesDuDeck = !courseCompleted ? (
    <>
      {ouEnEstOn}
      {sautes && sautes.arrivee === index && (
        // discret : le rappel sauté (diagnostic réussi du premier coup) reste à portée de main
        <button onClick={revoirRappel} data-revoir-rappel
          className="h-9 shrink-0 whitespace-nowrap rounded-full px-3 text-xs text-amber-100/90 hover:bg-white/10"
          style={{ background: 'rgba(13,27,21,0.9)', border: '1px solid rgba(253,230,138,0.35)' }}
          title={`Tu as réussi le diagnostic du premier coup : ${sautes.ids.length > 1 ? `${sautes.ids.length} rappels sautés` : 'rappel sauté'}. Le revoir quand même ?`}>
          🔁<span className="court:hidden"> Revoir le rappel</span>
        </button>
      )}
      <span
        className="px-1 text-[11px] tabular-nums text-white/40 hidden lg:inline"
        title={`${current.activity.title} — partie ${current.activityIndex + 1}/${deck.activities.length}, diapositive ${current.slideIndex + 1}/${activitySlideCount}`}
      >
        {totalProgress}%
      </span>
      <button
        onClick={goToPrevious}
        disabled={index === 0}
        className="w-9 h-9 shrink-0 rounded-full flex items-center justify-center text-white text-sm hover:scale-105 transition-transform disabled:opacity-25 disabled:hover:scale-100"
        style={{ background: 'rgba(13,27,21,0.9)', border: '1px solid rgba(255,255,255,0.18)' }}
        title="Diapositive précédente"
      >
        ←
      </button>
      <button
        onClick={restartFromBeginning}
        className="w-9 h-9 shrink-0 rounded-full flex items-center justify-center text-white text-sm hover:scale-105 transition-transform"
        style={{ background: 'rgba(13,27,21,0.9)', border: '1px solid rgba(255,255,255,0.18)' }}
        title="Recommencer le cours"
      >
        ↺
      </button>
      {/* En concentration, le seul bouton pour avancer est « Suite → », posé par le tableau lui-même. */}
      {mode !== 'concentration' && (
        <button
          onClick={goToNext}
          className="h-10 px-4 rounded-full text-sm font-semibold text-white hover:scale-[1.03] transition-transform"
          style={{ background: 'rgba(79,70,229,0.95)', border: '1px solid rgba(129,140,248,0.5)' }}
        >
          {index >= flatSlides.length - 1 ? 'Terminer ✓' : 'Suivant →'}
        </button>
      )}
    </>
  ) : null;

  return (
    // overflow-clip, pas hidden : un conteneur « hidden » défile encore quand un bouton qui déborde prend le focus,
    // et tout le lecteur glissait hors de l'écran sur téléphone (fenêtre du cahier de fin de bloc, 14 novembre 2026)
    <div data-lecteur-cours className="relative h-full w-full overflow-clip bg-[#07101f] text-white flex flex-col">
      {/* le clavier prend les touches de la matière du cours */}
      <MatiereDuClavier id={deck.stable_id || deck.id} subject={(deck as { subject?: string }).subject} />
      {/* Avancement dans le DECK : deux pixels, comme le fil du tableau. Le
          tableau, lui, compte ses propres étapes dans sa barre d'outils. */}
      <div className="absolute top-0 left-0 right-0 z-20 h-0.5 bg-white/10">
        <div
          className="h-full bg-gradient-to-r from-cyan-500 to-indigo-500 transition-all"
          style={{ width: `${totalProgress}%` }}
        />
      </div>

      {/* Le tableau n'est monté qu'une fois le cours lancé : monté d'avance,
          il jouait sa première diapositive DERRIÈRE l'écran d'accueil — l'élève
          cliquait « Commencer » sur un cours déjà à sa cinquième ligne — et il
          se figeait hors plein écran, `startFocused` ayant été lu au montage. */}
      <div className="flex-1 min-h-0">
        {started && mode === 'concentration' && (
          <CourseFocusStage
            slide={current.slide}
            language={language}
            deckControls={commandesDuDeck}
            tuteur3D={tuteur3D}
            deckId={deck.stable_id || deck.id}
            onSuivant={goToNext}
            libelleSuite={index >= flatSlides.length - 1 ? 'Terminer ✓' : 'Suite →'}
            finDeBloc={memoire.blocAFermer}
            onFermerBloc={memoire.fermerBloc}
            onReponseJugee={memoire.signalerReponse}
            entete={enteteDuCahier(deck, current.slide.id)}
          />
        )}
        {/* le clavier scientifique flottant, à droite (diapositives, cahier, retrouver, exercices, rappels) */}
        {started && mode === 'concentration' && <ClavierFlottant droite={tuteur3D ? COLONNE_TUTEUR : 0} bas={memoire.ecran ? 16 : 76} />}
        {started && memoire.ecran && (
          // le tuteur 3D garde sa colonne à droite : il reste visible et parle pendant le cahier, le rappel, l'exercice
          <div className={`absolute inset-0 z-[110] flex items-stretch justify-center bg-[#07101f]/92 p-2 backdrop-blur-sm sm:p-3 ${tuteur3D ? 'md:pr-[var(--colonne-tuteur)] court:pr-[var(--colonne-tuteur)] court:p-1' : ''}`}
            style={{ ['--colonne-tuteur' as string]: `${COLONNE_TUTEUR + placeClavier}px`, paddingRight: !tuteur3D && placeClavier ? placeClavier : undefined,
              paddingBottom: hauteurClavierTelephone(clavierOuvert) || undefined }}>
            {/* large (14 novembre 2026) : le cahier et ses dessins prennent la place de l'écran au lieu de rester petits */}
            <div className="h-full w-full max-w-6xl">{memoire.ecran}</div>
          </div>
        )}
        {started && mode !== 'concentration' && (
        <LiveBoard
          script={script}
          isVisible
          startFocused={pleinEcranVoulu}
          onFocusChange={onFocusChange}
          onStudentMessage={onStudentQuestion}
          assistantReply={assistantReply}
          busy={tutorBusy}
          audioActive={externalAudioActive}
          scientificControl={scientificControl}
          onSimulationUpdate={onSimulationUpdate}
          onScriptEnd={archiverCorrectionApresReponse}
          deckControls={commandesDuDeck}
          // La parole du professeur est déjà versée dans le chat de gauche
          // (`onNarration`) : la répéter en travers du bas du tableau
          // recouvrait la diapositive d'un paragraphe entier.
          showNarration={false}
        />
        )}
      </div>

      {/* ── Commandes du DECK ──────────────────────────────────────────
          Rien de ce que le tableau sait déjà faire : ni pause, ni son, ni
          vitesse, ni loupe, ni plein écran — sa barre d'outils les porte.
          Seulement ce qui lui échappe, l'ordre des diapositives. */}
      {!started && (
        <div className="absolute inset-0 z-[120] grid place-items-center bg-[#050b14]/90 backdrop-blur-sm p-6 court:p-2">
          <div className="max-w-md text-center">
            <div className="text-5xl court:hidden">🎓</div>
            <h2 className="mt-4 text-2xl font-semibold court:mt-0 court:text-lg">{deck.title}</h2>
            <p className="mt-2 text-sm text-white/60 court:mt-1 court:text-xs">
              {progress?.status === 'completed'
                ? 'Ce cours est déjà validé. Tu peux le refaire entièrement sans perdre ta réussite.'
                : 'Le professeur écrit au tableau et explique à voix haute. Tu peux lever la main à tout moment : le cours se met en pause.'}
            </p>
            <button
              onClick={progress?.status === 'completed' ? restartFromBeginning : commencer}
              className="mt-6 rounded-2xl bg-gradient-to-r from-cyan-500 to-indigo-500 px-6 py-3 font-semibold shadow-lg shadow-cyan-500/20 court:mt-3 court:py-2"
            >
              {progress?.status === 'completed' ? '↺ Recommencer depuis le début' : initialIndex > 0 ? 'Reprendre le cours' : 'Commencer le cours'}
            </button>
          </div>
        </div>
      )}

      {courseCompleted && (
        <div className="absolute inset-0 z-[120] grid place-items-center bg-[#050b14]/92 p-6 backdrop-blur-sm">
          <div className="w-full max-w-lg rounded-3xl border border-emerald-400/25 bg-[#0d1c29] p-6 text-center shadow-2xl shadow-emerald-500/10">
            <div className="text-5xl">🎉</div>
            <h2 className="mt-4 text-2xl font-semibold text-emerald-100">Cours terminé</h2>
            <p className="mt-2 text-sm leading-relaxed text-white/60">Ta réussite reste enregistrée. Tu peux recommencer immédiatement pour consolider les schémas, les questions et les simulations.</p>
            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <button onClick={() => { setCourseCompleted(false); goToPrevious(); }} disabled={index === 0} className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm disabled:opacity-30">← Revoir la diapo précédente</button>
              <button onClick={restartFromBeginning} className="rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 px-5 py-3 text-sm font-semibold text-white">↺ Recommencer depuis le début</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/** La matière du cours donnée au clavier scientifique (`phys_`/`chem_`/`svt_`/`math_` ou le champ `subject`). */
function MatiereDuClavier({ id, subject }: { id: string; subject?: string }) {
  useEffect(() => { clavier.matiere(matiereDuClavier(id, subject)); }, [id, subject]);
  return null;
}
