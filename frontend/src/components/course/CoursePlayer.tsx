import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import LiveBoard from '../session/LiveBoard';
import { saveCourseProgress } from '../../services/api';
import { slideVersScript } from './slideVersScript';
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
}

interface FlatSlide {
  activity: CourseActivity;
  activityIndex: number;
  slide: CourseSlide;
  slideIndex: number;
}

const clamp = (value: number, min: number, max: number) => Math.max(min, Math.min(max, value));

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
}: CoursePlayerProps) {
  const flatSlides = useMemo<FlatSlide[]>(() =>
    deck.activities.flatMap((activity, activityIndex) =>
      (activity.slides || []).map((slide, slideIndex) => ({ activity, activityIndex, slide, slideIndex })),
    ), [deck.activities]);

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

  useEffect(() => {
    completedSlideIdsRef.current = completedSlideIds;
  }, [completedSlideIds]);

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
  useEffect(() => {
    if (!started || !current || !onNarration) return;
    const cle = `${current.slide.id}:${language}`;
    if (narrationEnvoyeeRef.current === cle) return;
    narrationEnvoyeeRef.current = cle;
    const parole = current.slide.speech_text || {};
    const dit = (parole[language] || parole.mixed || parole.fr || Object.values(parole)[0] || '').trim();
    const lignes: string[] = [];
    if (dit) lignes.push(dit);
    const enonce = current.slide.question?.prompt?.trim();
    if (enonce) {
      lignes.push(enonce);
      (current.slide.question?.options || []).forEach(option => lignes.push(`• ${option}`));
    }
    if (lignes.length) onNarration(lignes.join('\n'));
  }, [current, language, onNarration, started]);

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
    const next = index + 1;
    persist(next, 0, 'in_progress', nextCompleted);
    setIndex(next);
  }, [completedSlideIds, current, flatSlides.length, index, onComplete, persist]);

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
  }, []);

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
  const commandesDuDeck = !courseCompleted ? (
    <>
      <span
        className="px-1 text-[11px] tabular-nums text-white/40 hidden sm:inline"
        title={`${current.activity.title} — activité ${current.activityIndex + 1}/${deck.activities.length}`}
      >
        {current.activityIndex + 1}/{deck.activities.length} · {current.slideIndex + 1}/{activitySlideCount} · {totalProgress}%
      </span>
      <button
        onClick={goToPrevious}
        disabled={index === 0}
        className="w-10 h-10 rounded-full flex items-center justify-center text-white text-sm hover:scale-105 transition-transform disabled:opacity-25 disabled:hover:scale-100"
        style={{ background: 'rgba(13,27,21,0.9)', border: '1px solid rgba(255,255,255,0.18)' }}
        title="Diapositive précédente"
      >
        ←
      </button>
      <button
        onClick={restartFromBeginning}
        className="w-10 h-10 rounded-full flex items-center justify-center text-white text-sm hover:scale-105 transition-transform"
        style={{ background: 'rgba(13,27,21,0.9)', border: '1px solid rgba(255,255,255,0.18)' }}
        title="Recommencer le cours"
      >
        ↺
      </button>
      <button
        onClick={goToNext}
        className="h-10 px-4 rounded-full text-sm font-semibold text-white hover:scale-[1.03] transition-transform"
        style={{ background: 'rgba(79,70,229,0.95)', border: '1px solid rgba(129,140,248,0.5)' }}
      >
        {index >= flatSlides.length - 1 ? 'Terminer ✓' : 'Suivant →'}
      </button>
    </>
  ) : null;

  return (
    <div className="relative h-full w-full overflow-hidden bg-[#07101f] text-white flex flex-col">
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
        {started && (
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
        <div className="absolute inset-0 z-[120] grid place-items-center bg-[#050b14]/90 backdrop-blur-sm p-6">
          <div className="max-w-md text-center">
            <div className="text-5xl">🎓</div>
            <h2 className="mt-4 text-2xl font-semibold">{deck.title}</h2>
            <p className="mt-2 text-sm text-white/60">
              {progress?.status === 'completed'
                ? 'Ce cours est déjà validé. Tu peux le refaire entièrement sans perdre ta réussite.'
                : 'Le professeur écrit au tableau et explique à voix haute. Tu peux lever la main à tout moment : le cours se met en pause.'}
            </p>
            <button
              onClick={progress?.status === 'completed' ? restartFromBeginning : commencer}
              className="mt-6 rounded-2xl bg-gradient-to-r from-cyan-500 to-indigo-500 px-6 py-3 font-semibold shadow-lg shadow-cyan-500/20"
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
