import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { getSchemaById } from '../session/schemas';
import SVGSchemaViewer from '../session/schemas/SVGSchemaViewer';
import { SessionMediaDisplay } from '../session/MediaViewer';
import { saveCourseProgress, saveSlideAttempt } from '../../services/api';
import type {
  CourseActivity,
  CourseDeck,
  CourseProgressSnapshot,
  CourseSlide,
} from './types';

interface CoursePlayerProps {
  deck: CourseDeck;
  progress?: CourseProgressSnapshot | null;
  language: 'fr' | 'ar' | 'mixed';
  onStudentQuestion?: (text: string) => void;
  onResumeCourse?: () => void;
  assistantReply?: string | null;
  tutorBusy?: boolean;
  externalAudioActive?: boolean;
  onSimulationUpdate?: (state: any) => void;
  onComplete?: () => void;
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
  onStudentQuestion,
  onResumeCourse,
  assistantReply,
  tutorBusy = false,
  externalAudioActive = false,
  onSimulationUpdate,
  onComplete,
}: CoursePlayerProps) {
  const flatSlides = useMemo<FlatSlide[]>(() =>
    deck.activities.flatMap((activity, activityIndex) =>
      (activity.slides || []).map((slide, slideIndex) => ({ activity, activityIndex, slide, slideIndex })),
    ), [deck.activities]);

  const storageKey = `course-player:${deck.id}`;
  const initialIndex = useMemo(() => {
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
  }, [flatSlides, progress?.current_slide_id, storageKey]);

  const [index, setIndex] = useState(initialIndex);
  const [started, setStarted] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [muted, setMuted] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [questionVisible, setQuestionVisible] = useState(false);
  const [questionAnswer, setQuestionAnswer] = useState('');
  const [questionStartedAt, setQuestionStartedAt] = useState(0);
  const [remaining, setRemaining] = useState(0);
  const [feedback, setFeedback] = useState<{ text: string; correct?: boolean | null } | null>(null);
  const [completedSlideIds, setCompletedSlideIds] = useState<string[]>(progress?.completed_slide_ids || []);
  const [questionPanelOpen, setQuestionPanelOpen] = useState(false);
  const [studentQuestion, setStudentQuestion] = useState('');
  const [waitingTutor, setWaitingTutor] = useState(false);
  const [tutorResponse, setTutorResponse] = useState<string | null>(null);
  const [simulationStatus, setSimulationStatus] = useState<string>('idle');

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const revealTimerRef = useRef<number | null>(null);
  const advanceTimerRef = useRef<number | null>(null);
  const questionIntervalRef = useRef<number | null>(null);
  const pausedAudioPositionRef = useRef(0);
  const replyBaselineRef = useRef<string | null>(null);
  const completedSlideIdsRef = useRef(completedSlideIds);
  const current = flatSlides[index];

  useEffect(() => {
    completedSlideIdsRef.current = completedSlideIds;
  }, [completedSlideIds]);

  const clearTimers = useCallback(() => {
    if (revealTimerRef.current !== null) clearTimeout(revealTimerRef.current);
    if (advanceTimerRef.current !== null) clearTimeout(advanceTimerRef.current);
    if (questionIntervalRef.current !== null) clearInterval(questionIntervalRef.current);
    revealTimerRef.current = null;
    advanceTimerRef.current = null;
    questionIntervalRef.current = null;
  }, []);

  const stopAudio = useCallback(() => {
    const audio = audioRef.current;
    if (audio) {
      audio.pause();
      audio.src = '';
    }
    audioRef.current = null;
    setPlaying(false);
  }, []);

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

  const currentAudio = useMemo(() => {
    const audio = current?.slide.audio || {};
    return audio[language] || audio.mixed || audio.fr || Object.values(audio)[0];
  }, [current?.slide.audio, language]);

  const transcript = useMemo(() => {
    const speech = current?.slide.speech_text || {};
    return speech[language] || speech.mixed || speech.fr || Object.values(speech)[0] || '';
  }, [current?.slide.speech_text, language]);

  const showQuestion = useCallback(() => {
    if (!current) return;
    const question = current.slide.question;
    if (!question?.prompt) {
      const delay = current.slide.timing?.delay_after_feedback_ms ?? 900;
      advanceTimerRef.current = window.setTimeout(() => {
        setIndex(prev => Math.min(prev + 1, flatSlides.length - 1));
      }, delay);
      return;
    }
    setQuestionVisible(true);
    setQuestionAnswer('');
    setFeedback(null);
    setQuestionStartedAt(Date.now());
    setRemaining(question.timeout_seconds ?? 14);
  }, [current, flatSlides.length]);

  const beginSlide = useCallback(() => {
    if (!current || !started) return;
    clearTimers();
    stopAudio();
    setQuestionVisible(false);
    setQuestionAnswer('');
    setFeedback(null);
    setSimulationStatus('idle');

    if (currentAudio?.url) {
      const audio = new Audio(currentAudio.url);
      audio.preload = 'auto';
      audio.playbackRate = speed;
      audio.muted = muted;
      const storedPosition = index === initialIndex ? (progress?.audio_position_ms || 0) : 0;
      if (storedPosition > 0) audio.currentTime = Math.max(0, storedPosition / 1000 - 1.5);
      audio.ontimeupdate = () => persist(index, audio.currentTime * 1000);
      audio.onended = () => { setPlaying(false); showQuestion(); };
      audio.onerror = () => {
        setPlaying(false);
        revealTimerRef.current = window.setTimeout(showQuestion, 1500);
      };
      audioRef.current = audio;
      audio.play().then(() => setPlaying(true)).catch(() => {
        setPlaying(false);
        revealTimerRef.current = window.setTimeout(showQuestion, 1800);
      });
    } else {
      const seconds = current.slide.timing?.reading_seconds ?? clamp(Math.ceil(transcript.length / 22), 6, 18);
      revealTimerRef.current = window.setTimeout(showQuestion, seconds * 1000);
    }
  }, [clearTimers, current, currentAudio?.url, index, initialIndex, muted, persist, progress?.audio_position_ms, showQuestion, speed, started, stopAudio, transcript.length]);

  useEffect(() => {
    beginSlide();
    return () => { clearTimers(); stopAudio(); };
  }, [beginSlide, clearTimers, stopAudio]);

  useEffect(() => {
    if (!questionVisible || feedback || questionPanelOpen || externalAudioActive || document.hidden) return;
    if (remaining <= 0) return;
    questionIntervalRef.current = window.setInterval(() => {
      setRemaining(value => Math.max(0, value - 1));
    }, 1000);
    return () => {
      if (questionIntervalRef.current !== null) clearInterval(questionIntervalRef.current);
      questionIntervalRef.current = null;
    };
  }, [externalAudioActive, feedback, questionPanelOpen, questionVisible, remaining]);

  const goToNext = useCallback(() => {
    if (!current) return;
    const slideId = current.slide.id;
    const nextCompleted = completedSlideIds.includes(slideId) ? completedSlideIds : [...completedSlideIds, slideId];
    completedSlideIdsRef.current = nextCompleted;
    setCompletedSlideIds(nextCompleted);
    if (index >= flatSlides.length - 1) {
      persist(index, 0, 'completed', nextCompleted);
      onComplete?.();
      return;
    }
    const next = index + 1;
    persist(next, 0, 'in_progress', nextCompleted);
    setIndex(next);
  }, [completedSlideIds, current, flatSlides.length, index, onComplete, persist]);

  const submitAttempt = useCallback(async (
    outcome: 'answered' | 'skipped_timeout' | 'skipped_manual',
    answerOverride?: string,
  ) => {
    if (!current || feedback) return;
    clearTimers();
    const responseMs = questionStartedAt ? Date.now() - questionStartedAt : undefined;
    try {
      const result = await saveSlideAttempt({
        deck_id: deck.id,
        lesson_id: deck.lesson_id,
        slide_id: current.slide.id,
        answer: (answerOverride ?? questionAnswer) || undefined,
        outcome,
        response_time_ms: responseMs,
      });
      setFeedback({ text: result.data.feedback, correct: result.data.is_correct });
    } catch {
      setFeedback({
        text: outcome === 'answered' ? 'Réponse enregistrée.' : 'La notion sera reproposée plus tard.',
        correct: null,
      });
    }
    const delay = current.slide.timing?.delay_after_feedback_ms ?? 2200;
    advanceTimerRef.current = window.setTimeout(goToNext, delay);
  }, [clearTimers, current, deck.id, deck.lesson_id, feedback, goToNext, questionAnswer, questionStartedAt]);

  useEffect(() => {
    if (!questionVisible || feedback || remaining > 0) return;
    if (current?.slide.question?.advance_on_timeout === false) return;
    void submitAttempt('skipped_timeout');
  }, [current?.slide.question?.advance_on_timeout, feedback, questionVisible, remaining, submitAttempt]);

  useEffect(() => {
    if (!waitingTutor || tutorBusy || !assistantReply || assistantReply === replyBaselineRef.current) return;
    setTutorResponse(assistantReply);
    setWaitingTutor(false);
  }, [assistantReply, tutorBusy, waitingTutor]);

  useEffect(() => {
    const pauseForVisibility = () => {
      if (document.hidden && audioRef.current && !audioRef.current.paused) {
        pausedAudioPositionRef.current = audioRef.current.currentTime;
        audioRef.current.pause();
        setPlaying(false);
      }
    };
    document.addEventListener('visibilitychange', pauseForVisibility);
    return () => document.removeEventListener('visibilitychange', pauseForVisibility);
  }, []);

  const togglePlayback = () => {
    const audio = audioRef.current;
    if (!audio) return;
    if (audio.paused) void audio.play().then(() => setPlaying(true));
    else { audio.pause(); setPlaying(false); }
  };

  const openTutorQuestion = () => {
    const audio = audioRef.current;
    if (audio) {
      pausedAudioPositionRef.current = audio.currentTime;
      audio.pause();
      setPlaying(false);
    }
    clearTimers();
    setQuestionPanelOpen(true);
    setTutorResponse(null);
  };

  const askTutor = () => {
    const text = studentQuestion.trim();
    if (!text || !onStudentQuestion) return;
    replyBaselineRef.current = assistantReply || null;
    setWaitingTutor(true);
    onStudentQuestion(`Pendant le cours, activité « ${current?.activity.title} », diapo « ${current?.slide.title} » : ${text}`);
  };

  const resumeAfterTutor = () => {
    if (externalAudioActive) return;
    onResumeCourse?.();
    setQuestionPanelOpen(false);
    setStudentQuestion('');
    setTutorResponse(null);
    setWaitingTutor(false);
    const audio = audioRef.current;
    if (audio && audio.duration && pausedAudioPositionRef.current < audio.duration) {
      audio.currentTime = Math.max(0, pausedAudioPositionRef.current - 1.5);
      void audio.play().then(() => setPlaying(true)).catch(() => showQuestion());
    } else if (!questionVisible) {
      showQuestion();
    }
  };

  const cancelTutorQuestion = () => {
    setQuestionPanelOpen(false);
    setStudentQuestion('');
    setTutorResponse(null);
    setWaitingTutor(false);
    const audio = audioRef.current;
    if (audio && audio.duration && pausedAudioPositionRef.current < audio.duration) {
      audio.currentTime = pausedAudioPositionRef.current;
      void audio.play().then(() => setPlaying(true)).catch(() => beginSlide());
    } else {
      beginSlide();
    }
  };

  const handleSimulation = (state: any) => {
    const status = state?.current_state?.simulation_status || state?.simulation_status || 'running';
    setSimulationStatus(status);
    onSimulationUpdate?.(state);
  };

  if (!current) {
    return <div className="h-full grid place-items-center text-white/60">Ce cours ne contient aucune diapositive.</div>;
  }

  const activitySlideCount = current.activity.slides.length;
  const totalProgress = Math.round(((index + 1) / Math.max(1, flatSlides.length)) * 100);
  const visual = current.slide.visual || { kind: 'none' as const };
  const schema = visual.kind === 'schema' && visual.schema_id ? getSchemaById(visual.schema_id) : undefined;

  return (
    <div className="relative h-full w-full overflow-hidden bg-[#07101f] text-white flex flex-col">
      <div className="shrink-0 border-b border-white/10 bg-[#0b1628] px-3 py-2">
        <div className="flex items-center gap-2 text-xs">
          <span className="rounded-full bg-cyan-500/15 border border-cyan-400/25 px-2 py-1 text-cyan-200">
            Activité {current.activityIndex + 1}/{deck.activities.length}
          </span>
          <span className="truncate text-white/80 font-medium">{current.activity.title}</span>
          <span className="ml-auto tabular-nums text-white/50">Diapo {current.slideIndex + 1}/{activitySlideCount}</span>
          <span className="tabular-nums text-cyan-300">{totalProgress}%</span>
        </div>
        <div className="mt-2 h-1 overflow-hidden rounded-full bg-white/10">
          <div className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-indigo-500 transition-all" style={{ width: `${totalProgress}%` }} />
        </div>
      </div>

      <div className="flex-1 min-h-0 grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_340px]">
        <section className="min-h-0 flex flex-col p-3 lg:p-4">
          <div className="shrink-0 mb-2">
            <p className="text-[11px] uppercase tracking-[0.18em] text-cyan-300/70">{current.slide.slide_type}</p>
            <h2 className="text-lg lg:text-2xl font-semibold leading-tight">{current.slide.title}</h2>
            {current.slide.screen_content?.lead && <p className="mt-1 text-sm text-white/65">{current.slide.screen_content.lead}</p>}
          </div>

          <div className="flex-1 min-h-0 rounded-2xl border border-white/10 bg-white/[0.04] overflow-hidden relative">
            {visual.kind === 'image' && visual.url && (
              <div className="h-full w-full flex flex-col p-3">
                <img src={visual.url} alt={visual.alt || current.slide.screen_content?.alt || current.slide.title} className="flex-1 min-h-0 w-full object-contain rounded-xl" />
                {(visual.caption || current.slide.screen_content?.caption) && <p className="shrink-0 pt-2 text-center text-xs text-white/55">{visual.caption || current.slide.screen_content?.caption}</p>}
              </div>
            )}
            {visual.kind === 'schema' && schema && <SVGSchemaViewer schema={schema} autoAnimate className="p-2" />}
            {visual.kind === 'simulation' && visual.url && (
              <SessionMediaDisplay media={{ type: 'simulation', url: visual.url, caption: visual.caption }} isVisible onSimulationUpdate={handleSimulation} />
            )}
            {(visual.kind === 'none' || !visual.kind || (visual.kind === 'schema' && !schema)) && (
              <div className="h-full grid place-items-center p-8 text-center">
                <div className="max-w-2xl">
                  <p className="text-xl lg:text-3xl font-semibold text-cyan-100">{current.slide.screen_content?.essential_text || current.slide.screen_content?.lead || current.slide.title}</p>
                  {!!current.slide.screen_content?.bullets?.length && <ul className="mt-5 space-y-3 text-left text-white/75">{current.slide.screen_content.bullets.map(item => <li key={item} className="flex gap-2"><span className="text-cyan-400">●</span><span>{item}</span></li>)}</ul>}
                </div>
              </div>
            )}
          </div>
        </section>

        <aside className="min-h-0 border-t lg:border-t-0 lg:border-l border-white/10 bg-[#0a1424] p-3 flex flex-col gap-3 overflow-y-auto">
          <div className="rounded-xl border border-white/10 bg-white/[0.04] p-3">
            <div className="flex items-center gap-2 text-xs text-white/45 mb-2"><span>🎧</span><span>Transcription du professeur</span>{!currentAudio?.url && <span className="ml-auto text-amber-300/80">audio à valider</span>}</div>
            <p className="text-sm leading-relaxed text-white/80">{transcript || 'Le speech de cette diapositive est en préparation.'}</p>
          </div>

          {current.slide.screen_content?.student_trace && (
            <div className="rounded-xl border border-emerald-400/20 bg-emerald-500/10 p-3"><p className="text-[11px] uppercase tracking-wide text-emerald-300">Trace à retenir</p><p className="mt-1 text-sm text-emerald-50/90">{current.slide.screen_content.student_trace}</p></div>
          )}

          {questionVisible && current.slide.question?.prompt && (
            <div className="rounded-2xl border border-indigo-400/30 bg-indigo-500/10 p-3 animate-[fadeSlideIn_.25s_ease-out]">
              <div className="flex items-center gap-2"><span className="text-sm font-semibold text-indigo-100">Question minute</span><span className="ml-auto rounded-full bg-black/25 px-2 py-0.5 text-xs tabular-nums text-indigo-200">{remaining}s</span></div>
              <p className="mt-2 text-sm text-white/90">{current.slide.question.prompt}</p>
              {!!current.slide.question.options?.length ? (
                <div className="mt-3 grid gap-2">{current.slide.question.options.map(option => <button key={option} disabled={!!feedback} onClick={() => { setQuestionAnswer(option); void submitAttempt('answered', option); }} className={`rounded-xl border px-3 py-2 text-left text-sm transition ${questionAnswer === option ? 'border-cyan-300 bg-cyan-500/20' : 'border-white/10 bg-white/5 hover:bg-white/10'}`}>{option}</button>)}</div>
              ) : (
                <div className="mt-3 flex gap-2"><input value={questionAnswer} onChange={e => setQuestionAnswer(e.target.value)} onKeyDown={e => { if (e.key === 'Enter' && questionAnswer.trim()) void submitAttempt('answered'); }} className="min-w-0 flex-1 rounded-xl border border-white/15 bg-black/20 px-3 py-2 text-sm outline-none focus:border-cyan-400" placeholder="Ta réponse en une phrase…"/><button onClick={() => void submitAttempt('answered')} disabled={!questionAnswer.trim()} className="rounded-xl bg-cyan-500 px-3 py-2 text-sm font-semibold text-slate-950 disabled:opacity-40">Valider</button></div>
              )}
              {feedback && <p className={`mt-3 rounded-lg px-3 py-2 text-xs ${feedback.correct === true ? 'bg-emerald-500/15 text-emerald-200' : feedback.correct === false ? 'bg-amber-500/15 text-amber-100' : 'bg-white/5 text-white/70'}`}>{feedback.text}</p>}
            </div>
          )}

          <div className="mt-auto flex flex-wrap items-center gap-2">
            <button onClick={() => { persist(Math.max(0, index - 1)); setIndex(Math.max(0, index - 1)); }} disabled={index === 0} className="rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-xs disabled:opacity-30">← Retour</button>
            {currentAudio?.url && <button onClick={togglePlayback} className="rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-xs">{playing ? '⏸ Pause' : '▶ Reprendre'}</button>}
            <button onClick={() => setMuted(value => { const next = !value; if (audioRef.current) audioRef.current.muted = next; return next; })} className="rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-xs">{muted ? '🔇' : '🔊'}</button>
            <select value={speed} onChange={e => { const next = Number(e.target.value); setSpeed(next); if (audioRef.current) audioRef.current.playbackRate = next; }} className="rounded-lg border border-white/10 bg-[#111c2e] px-2 py-2 text-xs"><option value={0.85}>0,85×</option><option value={1}>1×</option><option value={1.15}>1,15×</option><option value={1.3}>1,3×</option></select>
            <button onClick={openTutorQuestion} className="rounded-lg border border-violet-400/25 bg-violet-500/10 px-3 py-2 text-xs text-violet-100">✋ Question</button>
            <button onClick={() => questionVisible && !feedback ? void submitAttempt('skipped_manual') : goToNext()} className="ml-auto rounded-lg bg-indigo-500 px-3 py-2 text-xs font-semibold">Suivant →</button>
          </div>
          {visual.kind === 'simulation' && <p className="text-[10px] text-white/35">État de la simulation : {simulationStatus}</p>}
        </aside>
      </div>

      {!started && (
        <div className="absolute inset-0 z-30 grid place-items-center bg-[#050b14]/90 backdrop-blur-sm p-6">
          <div className="max-w-md text-center"><div className="text-5xl">🎓</div><h2 className="mt-4 text-2xl font-semibold">{deck.title}</h2><p className="mt-2 text-sm text-white/60">Le premier clic autorise le son. Les audios validés seront ensuite lus sans aucune régénération.</p><button onClick={() => setStarted(true)} className="mt-6 rounded-2xl bg-gradient-to-r from-cyan-500 to-indigo-500 px-6 py-3 font-semibold shadow-lg shadow-cyan-500/20">Commencer l’activité</button></div>
        </div>
      )}

      {questionPanelOpen && (
        <div className="absolute inset-0 z-40 grid place-items-center bg-black/70 p-4 backdrop-blur-sm">
          <div className="w-full max-w-xl rounded-2xl border border-violet-400/30 bg-[#11172a] p-4 shadow-2xl">
            <h3 className="font-semibold text-violet-100">✋ Poser une question au professeur</h3>
            <p className="mt-1 text-xs text-white/45">Le cours est en pause à « {current.slide.title} ».</p>
            {!tutorResponse && <textarea value={studentQuestion} onChange={e => setStudentQuestion(e.target.value)} rows={3} disabled={waitingTutor || tutorBusy} className="mt-3 w-full resize-none rounded-xl border border-white/15 bg-black/20 p-3 text-sm outline-none focus:border-violet-400" placeholder="Qu’est-ce que tu veux comprendre ?" />}
            {(waitingTutor || tutorBusy) && <p className="mt-3 animate-pulse text-sm text-violet-200">Le professeur prépare sa réponse…</p>}
            {tutorResponse && <div className="mt-3 max-h-56 overflow-y-auto rounded-xl bg-white/5 p-3 text-sm leading-relaxed text-white/85">{tutorResponse}</div>}
            <div className="mt-4 flex justify-end gap-2">
              {!waitingTutor && !tutorBusy && !tutorResponse && <button onClick={cancelTutorQuestion} className="rounded-lg px-3 py-2 text-sm text-white/55">Annuler</button>}
              {!tutorResponse ? <button onClick={askTutor} disabled={!studentQuestion.trim() || waitingTutor || tutorBusy} className="rounded-lg bg-violet-500 px-4 py-2 text-sm font-semibold disabled:opacity-40">Envoyer</button> : <button onClick={resumeAfterTutor} disabled={externalAudioActive} className="rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 disabled:cursor-wait disabled:opacity-50">{externalAudioActive ? 'Réponse audio en cours…' : 'Reprendre le cours'}</button>}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
