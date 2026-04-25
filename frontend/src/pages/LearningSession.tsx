import { useEffect, useRef, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { useSessionStore, type SessionLanguage } from '../stores/sessionStore';
import { wsService } from '../services/websocket';
import { getLessons, startSession, endSession } from '../services/api';
import { speechService } from '../services/speechService';
import VoiceInput from '../components/session/VoiceInput';
import AIAvatar from '../components/session/AIAvatar';
import ChatHistory from '../components/session/ChatHistory';
import { SessionMediaDisplay } from '../components/session/MediaViewer';
import AIWhiteboard from '../components/session/AIWhiteboard';
import ExamExercisePanel from '../components/session/ExamExercisePanel';
import type { ExamExercise } from '../components/session/ExamExercisePanel';
import LessonProgressBar from '../components/session/LessonProgressBar';
import QuickActions from '../components/session/QuickActions';
import type { QuickAction } from '../components/session/QuickActions';

/* ------------------------------------------------------------------ */
/*  Raccourcis — adaptés au mode Coaching et au mode Libre/Explain     */
/* ------------------------------------------------------------------ */
const COACHING_QUICK_ACTIONS: QuickAction[] = [
  {
    id: 'compris',
    icon: '✅',
    label: "J'ai compris",
    prompt: "J'ai bien compris cette partie, on peut passer à l'objectif suivant.",
    mode: 'send',
    tooltip: 'Passer à la partie suivante',
  },
  {
    id: 'bloque',
    icon: '❓',
    label: 'Je bloque',
    prompt: 'Je ne comprends pas. Peux-tu réexpliquer différemment avec un autre exemple plus simple ?',
    mode: 'send',
    tooltip: 'Demander une autre explication',
  },
  {
    id: 'quiz',
    icon: '🎯',
    label: 'Quiz',
    prompt: "Pose-moi un petit quiz de 3 questions pour vérifier que j'ai bien compris cette notion.",
    mode: 'send',
    tooltip: 'Vérifier ma compréhension',
  },
  {
    id: 'exo-bac',
    icon: '📝',
    label: 'Exo BAC',
    prompt: 'Donne-moi un exercice de type BAC marocain sur cette leçon, avec sa correction détaillée.',
    mode: 'send',
    tooltip: 'Exercice BAC avec correction',
  },
  {
    id: 'reexplique',
    icon: '🔁',
    label: 'Réexplique',
    prompt: 'Réexplique cette notion autrement, avec un exemple concret et un schéma si possible.',
    mode: 'send',
    tooltip: 'Réexplication alternative',
  },
  {
    id: 'schema',
    icon: '📊',
    label: 'Schéma',
    prompt: 'Fais-moi un schéma au tableau pour illustrer visuellement cette notion.',
    mode: 'send',
    tooltip: 'Schéma au tableau',
  },
  {
    id: 'resume',
    icon: '🎓',
    label: 'Résumer',
    prompt: 'Résume-moi cette leçon en points clés à retenir pour le BAC.',
    mode: 'send',
    tooltip: 'Résumé de la leçon',
  },
];

const LIBRE_QUICK_ACTIONS: QuickAction[] = [
  {
    id: 'cours',
    icon: '📚',
    label: 'Cours',
    prompt: 'Fais-moi un cours complet sur ',
    mode: 'inject',
    tooltip: 'Cours détaillé (complète le sujet)',
  },
  {
    id: 'exercice',
    icon: '📝',
    label: 'Exercice',
    prompt: 'Donne-moi un exercice de type BAC marocain sur le sujet en cours, avec correction détaillée.',
    mode: 'send',
    tooltip: 'Exercice BAC avec correction',
  },
  {
    id: 'corriger',
    icon: '✏️',
    label: 'Corriger',
    prompt: 'Corrige ma réponse :\n',
    mode: 'inject',
    tooltip: 'Faire corriger ta réponse',
  },
  {
    id: 'resume',
    icon: '🎯',
    label: 'Résumé',
    prompt: "Fais-moi un résumé en 3 points clés de ce qu'on vient de voir.",
    mode: 'send',
    tooltip: 'Résumer en 3 points',
  },
  {
    id: 'simple',
    icon: '🧠',
    label: 'Plus simple',
    prompt: 'Réexplique-moi ça plus simplement, comme à un débutant.',
    mode: 'send',
    tooltip: 'Réexpliquer plus simplement',
  },
  {
    id: 'detail',
    icon: '➕',
    label: 'Plus détaillé',
    prompt: 'Développe ta dernière réponse avec plus de détails et un exemple concret.',
    mode: 'send',
    tooltip: 'Plus de détails',
  },
  {
    id: 'schema',
    icon: '📊',
    label: 'Schéma',
    prompt: 'Fais-moi un schéma explicatif au tableau.',
    mode: 'send',
    tooltip: 'Schéma au tableau',
  },
];

interface LearningSessionProps {
  mode?: 'standard' | 'libre' | 'explain';
}

/**
 * Convert any legacy / coaching / libre exercise payload into the unified
 * ExamExercise shape consumed by ExamExercisePanel. This guarantees that ALL
 * exercises — regardless of session mode — render with the same layout,
 * the same question navigation, and the same answer areas as the exam mode.
 */
function adaptExerciseToExamFormat(raw: any): ExamExercise {
  const statement =
    raw?.statement ||
    raw?.question ||
    raw?.description ||
    raw?.content ||
    raw?.prompt ||
    raw?.enonce ||
    '';

  const choices = Array.isArray(raw?.choices)
    ? raw.choices.map((c: any, i: number) => ({
        letter: typeof c === 'string' ? String.fromCharCode(65 + i) : (c.letter || c.key || String.fromCharCode(65 + i)),
        text: typeof c === 'string' ? c : (c.label || c.text || c.content || ''),
      }))
    : undefined;

  const questionType = choices && choices.length > 0 ? 'qcm' : (raw?.type || 'open');

  // Build a single-question exercise from the legacy fields. The hints, if
  // present, are appended to the correction so the student still sees them.
  const hintsText = Array.isArray(raw?.hints) && raw.hints.length > 0
    ? '\n\nIndices :\n' + raw.hints
        .map((h: any) => `• ${typeof h === 'string' ? h : (h.text || h.content || '')}`)
        .join('\n')
    : '';

  const solutionText =
    typeof raw?.solution === 'string'
      ? raw.solution
      : (raw?.solution?.text || raw?.solution?.content || raw?.correction || raw?.answer || '');

  const correction = (solutionText || '').toString() + hintsText;

  const question: any = {
    question_index: 1,
    content: statement,
    type: questionType,
    points: Number(raw?.points || raw?.point || 1) || 1,
    correction,
    choices,
    correct_answer: raw?.correct_answer ?? raw?.answer,
  };

  const title = raw?.title || raw?.name || raw?.topic || 'Exercice';

  return {
    exam_id: String(raw?.id || raw?.exercise_id || `local_${Date.now()}`),
    exam_label: title,
    subject: raw?.subject || 'Exercice',
    year: Number(raw?.year) || new Date().getFullYear(),
    session: raw?.session || '',
    exercise_name: title,
    exercise_context: raw?.context || raw?.exercise_context || '',
    topic: raw?.topic || '',
    questions: [question],
    total_points: Number(raw?.points || raw?.total_points || 1) || 1,
  };
}

export default function LearningSession({ mode = 'standard' }: LearningSessionProps) {
  const { chapterId } = useParams<{ chapterId: string }>();
  const isLibre = mode === 'libre' || mode === 'explain';
  const navigate = useNavigate();
  const { token, student } = useAuthStore();
  const {
    sessionId, setSessionId, setPhase,
    isProcessing, processingStage, setProcessing,
    isSpeaking, setSpeaking, addMessage, updateMessage, conversation,
    setLanguage, clearSession, language,
  } = useSessionStore();

  const [connected, setConnected] = useState(false);
  const [lessonInfo, setLessonInfo] = useState<any>(null);
  const [currentMedia, setCurrentMedia] = useState<any>(null);
  const [showMedia, setShowMedia] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showChat, setShowChat] = useState(true);
  const [ttsErrorMessage, setTtsErrorMessage] = useState<string | null>(null);
  const [whiteboardData, setWhiteboardData] = useState<any[] | null>(null);
  const [whiteboardSchemaId, setWhiteboardSchemaId] = useState<string | null>(null);
  const [boardContent, setBoardContent] = useState<any | null>(null);
  const [showWhiteboard, setShowWhiteboard] = useState(false);
  const [currentExercise, setCurrentExercise] = useState<any | null>(null);
  const [showExercise, setShowExercise] = useState(false);
  const [examExercises, setExamExercises] = useState<ExamExercise[]>([]);
  const [showExamPanel, setShowExamPanel] = useState(false);
  const [examQuery, setExamQuery] = useState<string>('');
  
  // Lesson progress state for coaching mode
  const [learningObjectives, setLearningObjectives] = useState<string[]>([]);
  const [completedObjectives, setCompletedObjectives] = useState<number[]>([]);
  const [currentObjectiveIndex, setCurrentObjectiveIndex] = useState(0);
  const [isResumedSession, setIsResumedSession] = useState(false);
  const [showProgressBar, setShowProgressBar] = useState(false);
  const [lessonCompleted, setLessonCompleted] = useState(false);

  // Quick-actions injection state
  const [injectedText, setInjectedText] = useState<string | undefined>(undefined);
  const [injectKey, setInjectKey] = useState(0);

  // Contextual quick-reply suggestions from the AI (aligned on its last question)
  const [contextSuggestions, setContextSuggestions] = useState<QuickAction[]>([]);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const audioUrlRef = useRef<string | null>(null);
  const handlersRegisteredRef = useRef(false);
  const showExamPanelRef = useRef(false);

  // Keep ref in sync so WS handlers always read current value
  useEffect(() => { showExamPanelRef.current = showExamPanel; }, [showExamPanel]);

  const handleSimulationUpdate = useCallback((simulationState: any) => {
    console.log('[LearningSession] Simulation message received:', simulationState?.type, simulationState);
    if (!wsService.isConnected) {
      console.warn('[LearningSession] WebSocket not connected, cannot forward simulation message');
      return;
    }
    const originalType = simulationState?.type;
    const { type: _ignoredType, ...simulationPayload } = simulationState || {};
    if (originalType === 'simulation_manifest') {
      console.log('[LearningSession] Forwarding simulation_manifest to backend');
      wsService.sendJson({
        ...simulationPayload,
        type: 'simulation_manifest'
      });
    } else {
      wsService.sendJson({
        ...simulationPayload,
        type: 'simulation_update'
      });
    }
  }, []);

  useEffect(() => {
    // Check authentication first
    if (!token) {
      setError('Vous devez être connecté pour accéder à cette page.');
      setTimeout(() => navigate('/login'), 2000);
      return;
    }

    // Delay init so React StrictMode cleanup cancels the first mount's timer
    // before any WebSocket connection opens — ensures exactly ONE connection.
    const initTimer = setTimeout(() => {
      initSession();
    }, 80);

    return () => {
      clearTimeout(initTimer);
      speechService.stop();
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
        audioRef.current = null;
      }
      if (audioUrlRef.current) {
        URL.revokeObjectURL(audioUrlRef.current);
        audioUrlRef.current = null;
      }
      audioChunksRef.current = [];
      isPlayingChunksRef.current = false;
      expectedChunksRef.current = 0;
      streamingTextRef.current = '';
      streamingMsgIdRef.current = null;
      if (streamingRafRef.current) cancelAnimationFrame(streamingRafRef.current);
      streamingRafRef.current = null;
      handlersRegisteredRef.current = false;
      wsService.disconnect();
      if (sessionId) endSession(sessionId).catch(() => {});
      clearSession();
    };
  }, []);

  const initSession = async () => {
    if (!token || (!chapterId && !isLibre)) {
      setIsLoading(false);
      return;
    }

    const preferredLanguage = ((student?.preferred_language as SessionLanguage) || 'fr');
    setLanguage(preferredLanguage === 'mixed' ? 'mixed' : preferredLanguage);

    setIsLoading(true);
    setError(null);

    try {
      if (isLibre) {
        // --- LIBRE / EXPLAIN MODE: no chapter/lesson, connect WS directly ---
        console.log(`[Session] ${mode} mode — setting up handlers then connecting`);
        setupWSHandlers();

        await wsService.connect(token);
        console.log(`[Session] WebSocket connected (${mode})`);
        setConnected(true);

        // For explain mode, read exam question context from sessionStorage
        const explainCtx = mode === 'explain' ? JSON.parse(sessionStorage.getItem('explain_context') || '{}') : {};
        const explainSubject = explainCtx.subject || 'Général';
        const explainHasAnswer = explainCtx.hasAnswer || false;

        wsService.sendJson({
          type: 'init_session',
          mode: mode === 'explain' ? 'explain' : 'libre',
          subject: mode === 'explain' ? explainSubject : 'Général',
          chapter_title: '',
          lesson_title: mode === 'explain' ? 'Explication Examen' : 'Mode Libre',
          objective: mode === 'explain'
            ? (explainHasAnswer
                ? "Expliquer en PROFONDEUR la réponse de cette question d'examen avec démonstration, cours associé, schémas et astuces BAC. UTILISE le tableau (whiteboard) pour illustrer."
                : "Aider l'élève à COMPRENDRE cette question d'examen SANS donner la réponse. Donne la méthode, les notions du cours utiles, et illustre avec des schémas au tableau.")
            : "Répondre aux questions de l'étudiant sur toutes les matières du BAC",
          scenario: mode === 'explain' ? JSON.stringify(explainCtx) : '',
          student_name: student?.full_name || 'l\'étudiant',
          proficiency: 'intermédiaire',
          language: preferredLanguage,
          teaching_mode: 'Socratique',
        });
        console.log(`[Session] init_session sent (${mode})`);
        setIsLoading(false);
        return;
      }

      // --- STANDARD MODE: load chapter/lesson ---
      console.log('[Session] Loading lessons for chapter:', chapterId);
      const lessonsRes = await getLessons(chapterId!);
      console.log('[Session] Lessons response:', lessonsRes);
      const lesson = lessonsRes.data[0];
      
      if (!lesson) {
        console.error('[Session] No lesson found in response:', lessonsRes.data);
        setError('Aucune leçon trouvée pour ce chapitre.');
        setTimeout(() => navigate('/dashboard'), 2000);
        return;
      }
      
      setLessonInfo(lesson);

      // Create session in DB
      try {
        const sessionRes = await startSession(lesson.id);
        setSessionId(sessionRes.data.id);
      } catch (sessionErr: any) {
        if (sessionErr.response?.status === 401) {
          setError('Votre session a expiré. Veuillez vous reconnecter.');
          setTimeout(() => {
            useAuthStore.getState().logout();
            navigate('/login');
          }, 2000);
          return;
        }
        throw sessionErr;
      }

      // Connect WebSocket
      console.log('[Session] Connecting WebSocket with token:', token?.substring(0, 20) + '...');
      await wsService.connect(token);
      console.log('[Session] WebSocket connected');
      setConnected(true);

      // Set up WebSocket handlers
      setupWSHandlers();

      // Initialize AI session
      console.log('[Session] Sending init_session with lesson_id:', lesson.id);
      wsService.sendJson({
        type: 'init_session',
        lesson_id: lesson.id,  // IMPORTANT: needed for loading resources
        subject: 'SVT',
        chapter_title: '',
        lesson_title: lesson.title_fr,
        objective: lesson.learning_objectives?.[0] || '',
        phase: 'activation',
        student_name: student?.full_name || 'l\'étudiant',
        language: preferredLanguage,
        teaching_mode: 'Socratique',
      });
      console.log('[Session] init_session sent');

      setIsLoading(false);

    } catch (err: any) {
      console.error('Failed to init session:', err);
      setError(
        err.response?.status === 401
          ? 'Session expirée. Reconnexion nécessaire...'
          : 'Erreur lors de l\'initialisation. Veuillez réessayer.'
      );
      setIsLoading(false);
      
      if (err.response?.status === 401) {
        setTimeout(() => {
          useAuthStore.getState().logout();
          navigate('/login');
        }, 2000);
      }
    }
  };

  const audioReceivedRef = useRef(false);
  const pendingMediaRef = useRef<any>(null);
  const lastAiTextRef = useRef<string>('');
  const audioChunksRef = useRef<Array<{index: number, audio: string, format: string}>>([]);
  const isPlayingChunksRef = useRef(false);
  const expectedChunksRef = useRef<number>(0);
  const streamingTextRef = useRef<string>('');
  const streamingMsgIdRef = useRef<string | null>(null);
  const streamingRafRef = useRef<number | null>(null);

  const revealPendingMedia = () => {
    if (pendingMediaRef.current) {
      setShowWhiteboard(false);
      setCurrentMedia(pendingMediaRef.current);
      setShowMedia(true);
      pendingMediaRef.current = null;
    }
  };


  const setupWSHandlers = () => {
    if (handlersRegisteredRef.current) return;
    wsService.clearHandlers();
    handlersRegisteredRef.current = true;

    wsService.on('all', (data) => {
      console.log('[WebSocket] Received message:', data?.type, data);
    });

    wsService.on('error', (data) => {
      console.error('[WebSocket] Error message from backend:', data);
      setConnected(false);
      setProcessing(false);
    });

    wsService.on('disconnected', (info: any) => {
      console.warn('[WebSocket] Disconnected', info);
      setConnected(false);
      setProcessing(false);
    });

    // Auth token expired (Supabase JWT) — backend closed with code 4001
    wsService.on('auth_expired', () => {
      console.warn('[WebSocket] Auth expired — redirecting to login');
      setError('Votre session a expiré. Veuillez vous reconnecter.');
      setTimeout(() => {
        useAuthStore.getState().logout();
        navigate('/login');
      }, 1500);
    });

    wsService.on('ai_response', (data) => {
      // Skip if streaming is active (avoid duplicate with ai_response_chunk)
      if (streamingMsgIdRef.current || streamingTextRef.current) return;
      lastAiTextRef.current = data.text;
      audioReceivedRef.current = false;
      setTtsErrorMessage(null);
      // Clean drawing commands from displayed text (including truncated ones)
      let displayText = data.text;
      displayText = displayText.replace(/DESSINER_SCHEMA:.*?(\n|$)/g, '');
      displayText = displayText.replace(/<draw>[\s\S]*?<\/draw>/g, '');
      displayText = displayText.replace(/<draw>[\s\S]*/g, '');  // truncated
      displayText = displayText.trim();
      addMessage('ai', displayText || data.text);
      setProcessing(false);
    });

    // Streaming: receive batched tokens for real-time display
    // Tags are already filtered by backend, so just append directly
    // Throttled with rAF to avoid re-rendering on every token
    wsService.on('ai_response_chunk', (data) => {
      setProcessing(false);
      setTtsErrorMessage(null);
      streamingTextRef.current += (data.token || '');
      if (streamingRafRef.current) return; // already scheduled
      streamingRafRef.current = requestAnimationFrame(() => {
        streamingRafRef.current = null;
        const text = streamingTextRef.current.trim();
        if (!text) return;
        if (streamingMsgIdRef.current) {
          updateMessage(streamingMsgIdRef.current, text);
        } else {
          streamingMsgIdRef.current = addMessage('ai', text);
        }
      });
    });

    // Streaming done: flush any pending rAF update and finalize
    wsService.on('ai_response_done', () => {
      // Cancel pending rAF and do final update
      if (streamingRafRef.current) {
        cancelAnimationFrame(streamingRafRef.current);
        streamingRafRef.current = null;
      }
      const finalText = streamingTextRef.current.trim();
      if (finalText && streamingMsgIdRef.current) {
        updateMessage(streamingMsgIdRef.current, finalText);
      }
      if (streamingTextRef.current) {
        lastAiTextRef.current = streamingTextRef.current;
        audioReceivedRef.current = false;
      }
      streamingTextRef.current = '';
      streamingMsgIdRef.current = null;
    });

    wsService.on('transcription', (data) => {
      addMessage('student', data.text);
    });

    wsService.on('audio_response', (data) => {
      console.log('[Handler] audio_response received');
      audioReceivedRef.current = true;
      setProcessing(false);
      setTtsErrorMessage(null);
      playAudio(data.audio, data.format);
    });

    wsService.on('audio_chunk', (data) => {
      audioReceivedRef.current = true;
      setProcessing(false);
      setTtsErrorMessage(null);
      
      console.log(`[Audio Chunk] Received chunk ${data.chunk_index + 1}/${data.total_chunks}`);
      
      audioChunksRef.current.push({
        index: data.chunk_index,
        audio: data.audio,
        format: data.format
      });
      audioChunksRef.current.sort((a, b) => a.index - b.index);
      expectedChunksRef.current = data.total_chunks;
      
      // Start playing as soon as chunk 0 is available
      if (!isPlayingChunksRef.current && audioChunksRef.current[0]?.index === 0) {
        playAudioChunks();
      }
    });

    wsService.on('tts_error', (data) => {
      setProcessing(false);
      const errorMsg = data?.message || 'Gemini TTS error';
      
      setTtsErrorMessage(`⚠️ Erreur audio: ${errorMsg}`);
      
      console.error('[TTS Error]', errorMsg);
      revealPendingMedia();
    });

    // Server-side routing: for French (or fallback) backend asks us to speak
    // via the free Web Speech API instead of sending audio bytes.
    wsService.on('use_browser_tts', (data) => {
      audioReceivedRef.current = true;
      setProcessing(false);
      setTtsErrorMessage(null);
      const text: string = data?.text || '';
      const lang: SessionLanguage = (data?.language as SessionLanguage) || 'fr';
      if (!text) return;
      console.log(`[TTS] use_browser_tts (lang=${lang}, provider=${data?.provider})`);
      setSpeaking(true);
      speechService
        .speak(text, {
          lang,
          onEnd: () => setSpeaking(false),
        })
        .catch((err) => {
          console.warn('[TTS] Browser TTS failed:', err);
          setSpeaking(false);
        });
    });

    wsService.on('processing', (data) => {
      if (data.stage === 'tts') return;
      setProcessing(true, data.stage);
    });

    wsService.on('phase_changed', (data) => {
      setPhase(data.phase);
    });

    // Handle session initialization with progress data
    wsService.on('session_initialized', (data) => {
      console.log('[Session] session_initialized received:', data);
      if (data.learning_objectives && Array.isArray(data.learning_objectives)) {
        setLearningObjectives(data.learning_objectives);
        setShowProgressBar(true);
      }
      if (data.progress) {
        setCompletedObjectives(data.progress.objectives_completed || []);
        setCurrentObjectiveIndex(data.progress.current_objective_index || 0);
        // Restore lesson completion status
        const isDone = data.progress.status === 'completed' ||
          (data.learning_objectives && Array.isArray(data.learning_objectives) &&
           data.learning_objectives.length > 0 &&
           (data.progress.objectives_completed || []).length >= data.learning_objectives.length);
        setLessonCompleted(!!isDone);
      }
      if (data.is_resumed) {
        setIsResumedSession(true);
      }
    });

    // Contextual quick-reply buttons from the AI (aligned on its last question)
    wsService.on('quick_suggestions', (data) => {
      if (Array.isArray(data?.suggestions)) {
        setContextSuggestions(
          data.suggestions
            .filter((s: any) => s && s.label && s.prompt)
            .map((s: any, i: number) => ({
              id: s.id || `ctx_${i}`,
              icon: s.icon || '💬',
              label: String(s.label),
              prompt: String(s.prompt),
              mode: 'send' as const,
            }))
        );
      }
    });

    // Clear context suggestions as soon as the AI starts a new turn
    wsService.on('processing', () => {
      setContextSuggestions([]);
    });

    // Handle objective completion updates from backend
    wsService.on('objective_completed', (data) => {
      console.log('[Session] objective_completed:', data);
      if (typeof data.objective_index === 'number') {
        setCompletedObjectives(prev => 
          prev.includes(data.objective_index) ? prev : [...prev, data.objective_index]
        );
        setCurrentObjectiveIndex(data.objective_index + 1);
      }
    });

    // Handle full lesson completion — mark lesson as completed globally
    wsService.on('lesson_completed', (data) => {
      console.log('[Session] 🎉 lesson_completed:', data);
      setLessonCompleted(true);
    });

    wsService.on('show_media', (data) => {
      if (!data || !data.media) {
        console.error('[Display][ERROR] show_media received without a valid media payload:', data);
        return;
      }
      console.log('[Display] Showing media, hiding whiteboard', {
        mediaType: data.media?.type,
        title: data.media?.title || data.media?.name || data.media?.resource_name || 'unknown',
      });
      pendingMediaRef.current = null;
      setShowWhiteboard(false);
      setCurrentMedia(data.media);
      setShowMedia(true);
    });

    wsService.on('hide_media', () => {
      if (!currentMedia) {
        console.warn('[Display][WARN] hide_media received while no media is currently shown');
      }
      pendingMediaRef.current = null;
      setShowMedia(false);
    });

    wsService.on('hide_whiteboard', () => {
      if (!whiteboardData && !whiteboardSchemaId && !boardContent) {
        console.warn('[Display][WARN] hide_whiteboard received while the whiteboard is already empty');
      }
      console.log('[Display] Hiding whiteboard');
      setShowWhiteboard(false);
    });

    wsService.on('clear_whiteboard', () => {
      console.log('[Display] Clearing/resetting whiteboard explicitly');
      if (!whiteboardData && !whiteboardSchemaId && !boardContent) {
        console.warn('[Display][WARN] clear_whiteboard received but there was no active whiteboard content to clear');
      }
      // Force clear all whiteboard data to trigger AIWhiteboard reset
      setWhiteboardData(null);
      setWhiteboardSchemaId(null);
      setBoardContent(null);
    });

    wsService.on('whiteboard_draw', (data) => {
      if (!Array.isArray(data?.steps) || data.steps.length === 0) {
        console.error('[Display][ERROR] whiteboard_draw received without valid steps:', data);
        return;
      }

      const normalizedSteps = data.steps.map((step: any) => {
        if (typeof step === 'string') {
          try {
            return JSON.parse(step);
          } catch (e) {
            console.error('[Display][ERROR] Failed to parse step string:', step);
            return null;
          }
        }
        return step;
      }).filter((step: any) => step !== null);

      if (normalizedSteps.length === 0) {
        console.error('[Display][ERROR] No valid steps after normalization');
        return;
      }

      // Hide exam panel if active (but keep data so user can return)
      if (showExamPanelRef.current) {
        console.log('[Display] Switching from exam panel to whiteboard (keeping exam data)');
        setShowExamPanel(false);
        // Don't clear examExercises - user can return to exam
      }

      pendingMediaRef.current = null;
      setWhiteboardSchemaId(null);
      setBoardContent(null);
      // Force clear by setting null first, then new data after a tick
      // This ensures React detects the change and AIWhiteboard resets
      setWhiteboardData(null);
      setShowWhiteboard(true);
      setShowMedia(false);
      setShowExercise(false);
      setTimeout(() => {
        setWhiteboardData(normalizedSteps);
      }, 50);
    });

    wsService.on('whiteboard_schema', (data) => {
      if (!data?.schema_id) {
        console.error('[Display][ERROR] whiteboard_schema received without schema_id:', data);
        return;
      }

      // Hide exam panel if active (but keep data so user can return)
      if (showExamPanelRef.current) {
        console.log('[Display] Switching from exam panel to whiteboard schema (keeping exam data)');
        setShowExamPanel(false);
        // Don't clear examExercises - user can return to exam
      }

      console.log('[Display] Whiteboard schema received:', data.schema_id);
      pendingMediaRef.current = null;
      setWhiteboardData(null);
      setBoardContent(null);
      setWhiteboardSchemaId(data.schema_id);
      setShowWhiteboard(true);
      setShowMedia(false);
      setShowExercise(false);
    });

    wsService.on('whiteboard_board', (data) => {
      if (!data?.lines) {
        console.error('[Display][ERROR] whiteboard_board received without lines:', data);
        return;
      }

      // Hide exam panel if active (but keep data so user can return)
      if (showExamPanelRef.current) {
        console.log('[Display] Switching from exam panel to whiteboard board (keeping exam data)');
        setShowExamPanel(false);
        // Don't clear examExercises - user can return to exam
      }

      console.log('[Display] Whiteboard board received:', data.title, data.lines?.length, 'lines');
      pendingMediaRef.current = null;
      setWhiteboardData(null);
      setWhiteboardSchemaId(null);
      setBoardContent(data);
      setShowWhiteboard(true);
      setShowMedia(false);
      setShowExercise(false);
    });

    wsService.on('show_exercise', (data) => {
      // UNIFIED DISPLAY: convert any legacy/coaching/libre exercise payload
      // into the ExamExercise format so it renders inside the SAME
      // ExamExercisePanel used by exam mode (same layout, same navigation,
      // same answer areas).
      console.log('[Display] Showing exercise (unified panel):', data.exercise_id || data.exercise?.id, data.exercise);
      const raw = data.exercise || { id: data.exercise_id, ...data };
      const examExercise = adaptExerciseToExamFormat(raw);

      // Clear all other panels
      pendingMediaRef.current = null;
      setWhiteboardData(null);
      setWhiteboardSchemaId(null);
      setBoardContent(null);
      setCurrentMedia(null);
      setShowMedia(false);
      setShowWhiteboard(false);
      setShowExercise(false);
      setCurrentExercise(null);

      // Route through the exam panel
      setExamExercises([examExercise]);
      setExamQuery(raw.title || raw.name || raw.topic || '');
      setShowExamPanel(true);
    });

    wsService.on('hide_exercise', () => {
      console.log('[Display] Hiding exercise (unified panel)');
      setShowExercise(false);
      setCurrentExercise(null);
      setShowExamPanel(false);
    });

    wsService.on('exam_exercise', (data) => {
      console.log('[Display] Exam exercise received:', data?.exercises?.length, 'exercises for query:', data?.query);
      if (data?.exercises?.length > 0) {
        // Open the exam panel - clear ALL other panel state completely
        setWhiteboardData(null);
        setWhiteboardSchemaId(null);
        setBoardContent(null);
        setShowWhiteboard(false);
        setCurrentMedia(null);
        setShowMedia(false);
        setShowExercise(false);
        setCurrentExercise(null);
        pendingMediaRef.current = null;
        // Set exam panel state
        setExamExercises(data.exercises);
        setExamQuery(data.query || '');
        setShowExamPanel(true);
      }
    });

    wsService.on('hide_exam_panel', () => {
      console.log('[Display] Hiding exam panel');
      setShowExamPanel(false);
    });

    wsService.on('simulation_control', (data) => {
      console.log('[IA→Simulation] Commande de contrôle reçue:', data);
      
      // Trouver l'iframe de simulation active
      const iframe = document.querySelector('iframe[title="Simulation"]') as HTMLIFrameElement;
      
      if (iframe && iframe.contentWindow) {
        // Relayer la commande à la simulation
        iframe.contentWindow.postMessage(data, '*');
        console.log('[IA→Simulation] Commande relayée à l\'iframe:', data.command);
      } else {
        console.warn('[IA→Simulation] Aucune iframe de simulation active trouvée');
      }
    });
  };

  const playAudioChunks = () => {
    if (isPlayingChunksRef.current) return;
    if (audioChunksRef.current.length === 0) return;
    
    isPlayingChunksRef.current = true;
    let nextIndex = 0;
    
    const playNext = () => {
      const chunk = audioChunksRef.current.find(c => c.index === nextIndex);
      if (chunk) {
        const total = expectedChunksRef.current;
        console.log(`[Audio] Playing chunk ${nextIndex + 1}/${total}`);
        playAudioChunk(chunk.audio, chunk.format, () => {
          nextIndex++;
          if (total > 0 && nextIndex >= total) {
            // All chunks played
            console.log('[Audio] All chunks played');
            isPlayingChunksRef.current = false;
            audioChunksRef.current = [];
            expectedChunksRef.current = 0;
            setSpeaking(false);
          } else {
            playNext();
          }
        });
      } else {
        // Chunk not here yet — wait briefly then retry
        let waited = 0;
        const poll = setInterval(() => {
          waited += 200;
          const c = audioChunksRef.current.find(c => c.index === nextIndex);
          if (c) {
            clearInterval(poll);
            playNext();
          } else if (waited > 3000 || (expectedChunksRef.current > 0 && nextIndex >= expectedChunksRef.current)) {
            clearInterval(poll);
            console.log('[Audio] Done');
            isPlayingChunksRef.current = false;
            audioChunksRef.current = [];
            expectedChunksRef.current = 0;
            setSpeaking(false);
          }
        }, 200);
      }
    };
    
    playNext();
  };

  const playAudioChunk = (base64Audio: string, mimeType: string, onEnd: () => void) => {
    const byteCharacters = atob(base64Audio);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i += 1) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const audioBlob = new Blob([byteArray], { type: mimeType || 'audio/wav' });
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    
    audio.onplay = () => {
      setSpeaking(true);
      revealPendingMedia();
    };
    
    audio.onended = () => {
      console.log('[Audio Chunk] Audio ended event fired');
      URL.revokeObjectURL(audioUrl);
      onEnd();
    };
    
    audio.onerror = (e) => {
      console.error('[Audio Chunk] Audio error:', e);
      URL.revokeObjectURL(audioUrl);
      onEnd();
    };
    
    audio.play().catch((err) => {
      console.error('[Audio Chunk] Play failed:', err);
      URL.revokeObjectURL(audioUrl);
      onEnd();
    });
  };

  const playAudio = (base64Audio: string, mimeType = 'audio/wav') => {
    speechService.stop();
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current = null;
    }
    if (audioUrlRef.current) {
      URL.revokeObjectURL(audioUrlRef.current);
      audioUrlRef.current = null;
    }
    setSpeaking(true);
    const byteCharacters = atob(base64Audio);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i += 1) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const audioBlob = new Blob([byteArray], { type: mimeType || 'audio/wav' });
    const audioUrl = URL.createObjectURL(audioBlob);
    audioUrlRef.current = audioUrl;
    const audio = new Audio(audioUrl);
    audioRef.current = audio;
    audio.onplay = () => {
      revealPendingMedia();
    };
    audio.onended = () => {
      if (audioRef.current === audio) audioRef.current = null;
      if (audioUrlRef.current === audioUrl) {
          URL.revokeObjectURL(audioUrl);
          audioUrlRef.current = null;
      }
      setSpeaking(false);
    };
    audio.onerror = () => {
      if (audioRef.current === audio) audioRef.current = null;
      if (audioUrlRef.current === audioUrl) {
        URL.revokeObjectURL(audioUrl);
        audioUrlRef.current = null;
      }
      setSpeaking(false);
    };
    audio.play().catch(() => {
      if (audioRef.current === audio) audioRef.current = null;
      if (audioUrlRef.current === audioUrl) {
        URL.revokeObjectURL(audioUrl);
        audioUrlRef.current = null;
      }
      setSpeaking(false);
    });
  };


  const handleCloseWhiteboard = useCallback(() => setShowWhiteboard(false), []);

  const handleSendText = (text: string) => {
    if (!text.trim()) return;
    setContextSuggestions([]);
    addMessage('student', text);
    wsService.sendJson({ type: 'text_input', text });
  };

  /** Quick-action: envoie directement le prompt. */
  const handleQuickSend = (text: string) => {
    if (!connected || isProcessing) return;
    handleSendText(text);
  };

  /** Quick-action: injecte le prompt dans le champ texte du VoiceInput. */
  const handleQuickInject = (text: string) => {
    if (!connected) return;
    setInjectedText(text);
    setInjectKey((k) => k + 1);
  };

  const handleCloseExercise = () => {
    setShowExercise(false);
    setCurrentExercise(null);
    wsService.sendJson({ type: 'hide_exercise' });
  };

  const handleEndSession = async () => {
    speechService.stop();
    if (sessionId) {
      await endSession(sessionId).catch(() => {});
    }
    wsService.disconnect();
    clearSession();
    if (mode === 'explain') {
      const returnPath = sessionStorage.getItem('explain_return_path') || '/exam';
      sessionStorage.removeItem('explain_return_path');
      sessionStorage.removeItem('explain_context');
      navigate(returnPath);
    } else {
      navigate('/dashboard');
    }
  };

  // Error screen
  if (error) {
    return (
      <div className="h-screen flex items-center justify-center bg-[#080816]">
        <div className="text-center max-w-md mx-auto p-8">
          <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Oups !</h2>
          <p className="text-white/50 mb-6 text-sm">{error}</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-2.5 bg-white/10 text-white border border-white/10 rounded-xl hover:bg-white/15 transition-all text-sm font-medium"
          >
            Retour au Dashboard
          </button>
        </div>
      </div>
    );
  }

  // Loading screen with sci-fi animation
  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center bg-[#080816]">
        <div className="text-center">
          {/* Animated loading orb */}
          <div className="relative w-24 h-24 mx-auto mb-6">
            <div className="absolute inset-0 rounded-full border border-indigo-500/30 animate-ping" />
            <div className="absolute inset-2 rounded-full border border-cyan-500/20 animate-pulse" />
            <div className="absolute inset-4 rounded-full bg-gradient-to-br from-indigo-600 to-cyan-500 animate-pulse" />
            <div className="absolute inset-[22px] rounded-full bg-[#080816]" />
            <div className="absolute inset-[26px] rounded-full bg-gradient-to-br from-indigo-500 to-cyan-400" />
          </div>
          <p className="text-white/70 font-medium">Initialisation...</p>
          <p className="text-white/30 text-xs mt-2">Connexion au tuteur IA</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-[100dvh] flex flex-col bg-[#080816] text-white overflow-hidden">
      {/* Custom CSS for animations */}
      <style>{`
        @keyframes fadeSlideIn {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .scrollbar-thin::-webkit-scrollbar { width: 4px; }
        .scrollbar-thin::-webkit-scrollbar-track { background: transparent; }
        .scrollbar-thin::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 999px; }
      `}</style>

      {/* Progress Bar for Coaching Mode */}
      {showProgressBar && learningObjectives.length > 0 && !isLibre && (
        <div className="shrink-0 px-3 pt-2">
          <LessonProgressBar
            objectives={learningObjectives}
            completedIndices={completedObjectives}
            currentIndex={currentObjectiveIndex}
            lessonTitle={lessonInfo?.title_fr || 'Leçon'}
            isResumed={isResumedSession}
          />
        </div>
      )}

      {/* Lesson Completed Banner */}
      {lessonCompleted && !isLibre && (
        <div className="shrink-0 px-3 pt-2">
          <div className="rounded-xl bg-gradient-to-r from-emerald-500/20 to-green-500/20 border border-emerald-400/40 px-4 py-3 flex items-center justify-between gap-3 shadow-lg shadow-emerald-500/10">
            <div className="flex items-center gap-3">
              <div className="text-2xl">🎉</div>
              <div>
                <div className="text-emerald-300 font-semibold text-sm">Leçon terminée !</div>
                <div className="text-emerald-200/70 text-xs">
                  Tu as complété tous les objectifs. Cette leçon est marquée comme terminée.
                </div>
              </div>
            </div>
            <button
              onClick={handleEndSession}
              className="shrink-0 px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-white text-xs font-semibold rounded-lg transition-all shadow-md shadow-emerald-500/30"
            >
              Fermer la session
            </button>
          </div>
        </div>
      )}

      {/* Header */}
      <header className="shrink-0 bg-[#0c0c1d]/80 backdrop-blur-xl border-b border-white/5">
        <div className="w-full px-3 py-1.5 flex items-center justify-between gap-3">
          {/* Left: Back + Title */}
          <div className="flex items-center gap-3">
            <button
              onClick={handleEndSession}
              className="w-7 h-7 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center transition-colors border border-white/5"
              title="Quitter la session"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5 text-white/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <div>
              <h1 className="text-xs font-semibold text-white/90 leading-tight">{mode === 'explain' ? 'Explication Examen' : isLibre ? 'Mode Libre' : (lessonInfo?.title_fr || 'Session')}</h1>
              <p className="text-[10px] text-white/30 leading-tight">{mode === 'explain' ? 'Aide interactive au tableau' : isLibre ? 'Pose tes questions sur toutes les matières' : (lessonInfo?.title_ar || 'SVT - 2ème BAC')}</p>
            </div>
          </div>

          {/* Right: Language + Controls */}
          <div className="flex items-center gap-1.5 shrink-0">
            {/* Explain mode: prominent return button */}
            {mode === 'explain' && (
              <button
                onClick={handleEndSession}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500/90 hover:bg-amber-500 text-white text-[11px] font-semibold rounded-lg transition-all shadow-sm shadow-amber-500/20"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3" />
                </svg>
                Retour à l'examen
              </button>
            )}
            {/* Language toggle */}
            <div className="flex bg-white/5 rounded-lg border border-white/5 p-0.5">
              <button
                onClick={() => { setLanguage('fr'); wsService.sendJson({ type: 'set_language', language: 'fr' }); }}
                className={`px-2 py-1 text-[11px] rounded-md transition-all ${
                  language === 'fr'
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-white/40 hover:text-white/60'
                }`}
              >
                FR
              </button>
              <button
                onClick={() => { setLanguage('ar'); wsService.sendJson({ type: 'set_language', language: 'ar' }); }}
                className={`px-2 py-1 text-[11px] rounded-md transition-all ${
                  language === 'ar'
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-white/40 hover:text-white/60'
                }`}
              >
                عربي
              </button>
              <button
                onClick={() => { setLanguage('mixed'); wsService.sendJson({ type: 'set_language', language: 'mixed' }); }}
                className={`px-2 py-1 text-[11px] rounded-md transition-all ${
                  language === 'mixed'
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-white/40 hover:text-white/60'
                }`}
              >
                Darija
              </button>
            </div>

            {/* Display toggle buttons - whiteboard & media */}
            <div className="flex items-center gap-1 bg-white/5 rounded-lg p-0.5">
              {/* Whiteboard toggle */}
              {(whiteboardData || whiteboardSchemaId || boardContent) && (
                <button
                  onClick={() => {
                    if (showWhiteboard) {
                      setShowWhiteboard(false);
                    } else {
                      setShowWhiteboard(true);
                      setShowMedia(false);
                    }
                  }}
                  className={`flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md transition-all ${
                    showWhiteboard 
                      ? 'bg-cyan-600/30 text-cyan-300 shadow-sm' 
                      : 'text-white/40 hover:text-white/60'
                  }`}
                  title="Tableau blanc"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
                  </svg>
                  Tableau
                </button>
              )}
              {/* Media/Image toggle */}
              {currentMedia && (
                <button
                  onClick={() => {
                    if (showMedia) {
                      setShowMedia(false);
                    } else {
                      setShowMedia(true);
                      setShowWhiteboard(false);
                      setShowExamPanel(false);
                    }
                  }}
                  className={`flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md transition-all ${
                    showMedia 
                      ? 'bg-emerald-600/30 text-emerald-300 shadow-sm' 
                      : 'text-white/40 hover:text-white/60'
                  }`}
                  title="Ressource image"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0022.5 18.75V5.25A2.25 2.25 0 0020.25 3H3.75A2.25 2.25 0 001.5 5.25v13.5A2.25 2.25 0 003.75 21z" />
                  </svg>
                  Image
                </button>
              )}
              {/* Exam exercise panel toggle */}
              {examExercises.length > 0 && (
                <button
                  onClick={() => {
                    if (showExamPanel) {
                      setShowExamPanel(false);
                    } else {
                      setShowExamPanel(true);
                      setShowWhiteboard(false);
                      setShowMedia(false);
                      setShowExercise(false);
                    }
                  }}
                  className={`flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md transition-all ${
                    showExamPanel 
                      ? 'bg-amber-600/30 text-amber-300 shadow-sm' 
                      : 'text-white/40 hover:text-white/60'
                  }`}
                  title="Exercice d'examen"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342" />
                  </svg>
                  Examen
                </button>
              )}
            </div>

            {/* Chat toggle */}
            <button
              onClick={() => setShowChat(!showChat)}
              className={`w-7 h-7 rounded-full flex items-center justify-center transition-all border ${
                showChat ? 'bg-indigo-600/20 border-indigo-500/30 text-indigo-400' : 'bg-white/5 border-white/5 text-white/40 hover:text-white/60'
              }`}
              title="Afficher/masquer le chat"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
              </svg>
            </button>

            {/* End session */}
            <button
              onClick={handleEndSession}
              className="px-2.5 py-1 text-[11px] text-red-400/70 hover:text-red-400 border border-red-500/20 hover:border-red-500/30 rounded-lg transition-all hover:bg-red-500/5"
            >
              Terminer
            </button>
          </div>
        </div>
      </header>

      {/* TTS Error Banner */}
      {ttsErrorMessage && (
        <div className="shrink-0 bg-red-500/10 border-y border-red-500/20 px-4 py-2">
          <div className="max-w-7xl mx-auto flex items-center gap-3">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-red-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div className="flex-1 min-w-0">
              <p className="text-red-400 text-sm font-medium">Erreur audio TTS</p>
              <p className="text-red-300/70 text-xs truncate">{ttsErrorMessage}</p>
            </div>
            <button
              onClick={() => setTtsErrorMessage(null)}
              className="text-red-400/70 hover:text-red-400 text-xs px-2 py-1"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* Main content area */}
      <div className="flex-1 flex overflow-hidden relative min-h-0">
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-600/5 rounded-full blur-[120px]" />
          <div className="absolute top-1/4 left-1/4 w-[300px] h-[300px] bg-cyan-600/3 rounded-full blur-[80px]" />
        </div>

        {showChat && (
          <div className="w-[280px] shrink-0 border-r border-white/5 bg-[#0a0a18]/80 backdrop-blur-sm flex flex-col min-w-0">
            <ChatHistory messages={conversation} isProcessing={isProcessing} />
            {contextSuggestions.length > 0 && (
              <QuickActions
                actions={contextSuggestions}
                onInject={handleQuickInject}
                onSend={(text) => { setContextSuggestions([]); handleQuickSend(text); }}
                disabled={!connected || isProcessing}
                theme="dark"
                title="💡 Réponses suggérées"
              />
            )}
            <QuickActions
              actions={isLibre ? LIBRE_QUICK_ACTIONS : COACHING_QUICK_ACTIONS}
              onInject={handleQuickInject}
              onSend={handleQuickSend}
              disabled={!connected || isProcessing}
              theme="dark"
              title={isLibre ? 'Raccourcis' : 'Raccourcis leçon'}
              collapsible
            />
            <VoiceInput
              onTextSend={handleSendText}
              disabled={!connected}
              injectedText={injectedText}
              injectKey={injectKey}
            />
          </div>
        )}

        <div className="flex-1 min-w-0 flex flex-col relative overflow-hidden">
          {/* When media is showing: avatar becomes small pip, media fills the zone */}
          {showExamPanel && examExercises.length > 0 ? (
            <>
              {/* Exam panel - HIGHEST PRIORITY */}
              <div className="flex-1 min-h-0 flex items-center justify-center p-2 animate-[fadeSlideIn_0.5s_ease-out]">
                <div className="w-full h-full rounded-2xl border border-white/10 bg-gradient-to-br from-purple-900/20 to-blue-900/20 backdrop-blur-md overflow-hidden shadow-2xl shadow-black/40">
                  <ExamExercisePanel
                    exercises={examExercises}
                    query={examQuery}
                    onClose={() => setShowExamPanel(false)}
                  />
                </div>
              </div>
            </>
          ) : showExercise && currentExercise ? (
            <>
              {/* Small floating avatar pip */}
              <div className="absolute top-2 right-2 z-20 transition-all duration-500">
                <div className="scale-[0.4] origin-top-right">
                  <AIAvatar isSpeaking={isSpeaking} isProcessing={isProcessing} processingStage={processingStage} />
                </div>
              </div>

              {/* Close button */}
              <div className="absolute top-2 left-2 z-20">
                <button
                  onClick={handleCloseExercise}
                  className="flex items-center gap-2 text-white/50 hover:text-white/90 text-xs px-2.5 py-1 rounded-xl bg-black/40 hover:bg-black/60 backdrop-blur-sm border border-white/10 transition-all"
                  title="Fermer l'exercice"
                >
                  <span>✕</span>
                  <span>Fermer l'exercice</span>
                </button>
              </div>

              <div className="flex-1 min-h-0 flex items-center justify-center p-3 animate-[fadeSlideIn_0.5s_ease-out]">
                <div className="w-full max-w-5xl h-full rounded-2xl border border-amber-400/15 bg-[#111827]/95 backdrop-blur-sm overflow-hidden shadow-2xl shadow-black/40 flex flex-col">
                  <div className="px-5 py-4 border-b border-white/5 bg-white/[0.03] flex items-start justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="inline-flex items-center justify-center w-8 h-8 rounded-xl bg-amber-500/15 text-amber-300 border border-amber-400/20">✏️</span>
                        <h2 className="text-lg font-semibold text-white">{currentExercise.title || currentExercise.name || 'Exercice'}</h2>
                      </div>
                      <p className="text-xs text-white/40">
                        {currentExercise.difficulty_level ? `Niveau ${currentExercise.difficulty_level}` : 'Exercice interactif'}
                        {currentExercise.id || currentExercise.exercise_id ? ` · ID ${currentExercise.id || currentExercise.exercise_id}` : ''}
                      </p>
                    </div>
                    <button
                      onClick={handleCloseExercise}
                      className="text-white/40 hover:text-white/90 text-sm px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 transition-all"
                    >
                      Fermer
                    </button>
                  </div>

                  <div className="flex-1 min-h-0 overflow-y-auto p-5 space-y-5">
                    {(currentExercise.statement || currentExercise.question || currentExercise.description || currentExercise.content || currentExercise.prompt) && (
                      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                        <h3 className="text-sm font-medium text-amber-200 mb-2">Consigne</h3>
                        <p className="text-sm leading-7 text-white/85 whitespace-pre-wrap">
                          {currentExercise.statement || currentExercise.question || currentExercise.description || currentExercise.content || currentExercise.prompt}
                        </p>
                      </div>
                    )}

                    {Array.isArray(currentExercise.choices) && currentExercise.choices.length > 0 && (
                      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                        <h3 className="text-sm font-medium text-amber-200 mb-3">Choix possibles</h3>
                        <div className="grid gap-3">
                          {currentExercise.choices.map((choice: any, index: number) => {
                            const label = typeof choice === 'string' ? choice : (choice.label || choice.text || choice.content || JSON.stringify(choice));
                            return (
                              <div key={index} className="rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-white/85">
                                <span className="inline-flex items-center justify-center w-6 h-6 rounded-lg bg-amber-500/15 text-amber-300 text-xs mr-3">{index + 1}</span>
                                {label}
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    )}

                    {(currentExercise.hints || currentExercise.steps || currentExercise.solution) && (
                      <div className="grid gap-4 md:grid-cols-2">
                        {Array.isArray(currentExercise.hints) && currentExercise.hints.length > 0 && (
                          <div className="rounded-2xl border border-cyan-400/15 bg-cyan-400/5 p-4">
                            <h3 className="text-sm font-medium text-cyan-200 mb-2">Indices</h3>
                            <ul className="space-y-2 text-sm text-white/80">
                              {currentExercise.hints.map((hint: any, index: number) => (
                                <li key={index} className="flex gap-2">
                                  <span className="text-cyan-300">•</span>
                                  <span>{typeof hint === 'string' ? hint : (hint.text || hint.content || JSON.stringify(hint))}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {currentExercise.solution && (
                          <div className="rounded-2xl border border-emerald-400/15 bg-emerald-400/5 p-4 md:col-span-1">
                            <h3 className="text-sm font-medium text-emerald-200 mb-2">Correction / réponse</h3>
                            <p className="text-sm leading-7 text-white/80 whitespace-pre-wrap">
                              {typeof currentExercise.solution === 'string'
                                ? currentExercise.solution
                                : (currentExercise.solution.text || currentExercise.solution.content || JSON.stringify(currentExercise.solution))}
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </>
          ) : showWhiteboard && (whiteboardData || whiteboardSchemaId || boardContent) ? (
            <>
              {/* Small floating avatar pip — bottom-right so it doesn't block toolbar buttons (Print/PDF) */}
              <div className="absolute bottom-3 right-3 z-20 transition-all duration-500">
                <div className="scale-[0.35] origin-bottom-right">
                  <AIAvatar isSpeaking={isSpeaking} isProcessing={isProcessing} processingStage={processingStage} />
                </div>
              </div>

              {/* Close button + Return to exam button */}
              <div className="absolute top-2 left-2 z-20 flex items-center gap-2">
                <button
                  onClick={() => setShowWhiteboard(false)}
                  className="flex items-center gap-2 text-white/50 hover:text-white/90 text-xs px-2.5 py-1 rounded-xl bg-black/40 hover:bg-black/60 backdrop-blur-sm border border-white/10 transition-all"
                  title="Fermer le tableau"
                >
                  <span>✕</span>
                  <span>Fermer le tableau</span>
                </button>
                {examExercises.length > 0 && (
                  <button
                    onClick={() => {
                      setShowWhiteboard(false);
                      setShowExamPanel(true);
                    }}
                    className="flex items-center gap-2 text-amber-300 hover:text-amber-200 text-xs px-2.5 py-1 rounded-xl bg-amber-600/20 hover:bg-amber-600/30 backdrop-blur-sm border border-amber-500/30 transition-all"
                    title="Retour à l'examen"
                  >
                    <span>📝</span>
                    <span>Retour à l'examen</span>
                  </button>
                )}
              </div>

              {/* Whiteboard fills the entire center zone */}
              <div className="flex-1 min-h-0 flex items-center justify-center p-2 animate-[fadeSlideIn_0.5s_ease-out]">
                <div className="w-full h-full rounded-2xl border border-white/10 overflow-hidden shadow-2xl shadow-black/40">
                  <AIWhiteboard
                    drawCommands={whiteboardData}
                    schemaId={whiteboardSchemaId}
                    boardContent={boardContent}
                    isVisible={showWhiteboard}
                    onClose={handleCloseWhiteboard}
                  />
                </div>
              </div>
            </>
          ) : showMedia && currentMedia ? (
            <>
              {/* Small floating avatar pip */}
              <div className="absolute top-2 right-2 z-20 transition-all duration-500">
                <div className="scale-[0.4] origin-top-right">
                  <AIAvatar isSpeaking={isSpeaking} isProcessing={isProcessing} processingStage={processingStage} />
                </div>
              </div>

              {/* Close button */}
              <div className="absolute top-2 left-2 z-20">
                <button
                  onClick={() => setShowMedia(false)}
                  className="flex items-center gap-2 text-white/50 hover:text-white/90 text-xs px-2.5 py-1 rounded-xl bg-black/40 hover:bg-black/60 backdrop-blur-sm border border-white/10 transition-all"
                  title="Fermer la présentation"
                >
                  <span>✕</span>
                  <span>Fermer</span>
                </button>
              </div>

              {/* Media fills the entire center zone */}
              <div className="flex-1 min-h-0 flex items-center justify-center p-2 animate-[fadeSlideIn_0.5s_ease-out]">
                <div className="w-full h-full rounded-2xl border border-white/10 bg-white/[0.03] backdrop-blur-md overflow-hidden shadow-2xl shadow-black/40">
                  <SessionMediaDisplay 
                    media={currentMedia} 
                    isVisible={showMedia}
                    onSimulationUpdate={handleSimulationUpdate}
                  />
                </div>
              </div>
            </>
          ) : (
            <>
              {/* No media: avatar centered as main element */}
              <div className="flex-1 flex flex-col items-center justify-center gap-3">
                <AIAvatar isSpeaking={isSpeaking} isProcessing={isProcessing} processingStage={processingStage} />
                {!connected && (
                  <div className="flex items-center gap-2 text-amber-400/60 text-xs animate-pulse">
                    <div className="w-1.5 h-1.5 rounded-full bg-amber-400" />
                    Connexion...
                  </div>
                )}
                {connected && !conversation.length && !isProcessing && (
                  <div className="flex items-center gap-2 text-emerald-400/60 text-xs">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                    Connecté
                  </div>
                )}
              </div>
            </>
          )}

          {/* Voice input when chat is hidden */}
          {!showChat && (
            <div className="shrink-0 w-full max-w-3xl mx-auto px-6 pb-4">
              <QuickActions
                actions={isLibre ? LIBRE_QUICK_ACTIONS : COACHING_QUICK_ACTIONS}
                onInject={handleQuickInject}
                onSend={handleQuickSend}
                disabled={!connected || isProcessing}
                theme="dark"
                title={isLibre ? 'Raccourcis' : 'Raccourcis leçon'}
                collapsible
              />
              <VoiceInput
                onTextSend={handleSendText}
                disabled={!connected}
                injectedText={injectedText}
                injectKey={injectKey}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
