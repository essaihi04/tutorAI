import { create } from 'zustand';

export interface ConversationMessage {
  id: string;
  speaker: 'student' | 'ai';
  text: string;
  timestamp: Date;
  examExercises?: any[];
}

export type SessionLanguage = 'fr' | 'ar' | 'mixed';

export interface ExamPanelState {
  answers: Record<string, string>;
  images: Record<string, string | null>;
  submitted: Record<string, boolean>;
  revealedCorrections: Record<string, boolean>;
  currentExIdx: number;
  currentQIdx: number;
  // Signature of the current exam (e.g. "exam_id-question_count"). Used to
  // detect when a truly new exam is loaded vs. re-mounting the same panel.
  examSignature: string;
}

interface SessionState {
  sessionId: string | null;
  currentPhase: 'activation' | 'exploration' | 'explanation' | 'application' | 'consolidation';
  isProcessing: boolean;
  processingStage: string;
  isRecording: boolean;
  isSpeaking: boolean;
  conversation: ConversationMessage[];
  language: SessionLanguage;
  examPanelState: ExamPanelState;

  setSessionId: (id: string) => void;
  setPhase: (phase: SessionState['currentPhase']) => void;
  setProcessing: (isProcessing: boolean, stage?: string) => void;
  setRecording: (isRecording: boolean) => void;
  setSpeaking: (isSpeaking: boolean) => void;
  addMessage: (speaker: 'student' | 'ai', text: string, streaming?: boolean, examExercises?: any[]) => string;
  updateMessage: (id: string, text: string) => void;
  setLanguage: (lang: SessionLanguage) => void;
  setExamPanelState: (state: Partial<ExamPanelState>) => void;
  resetExamPanelState: () => void;
  // Reset panel state only if the new signature differs from the stored one.
  // Returns true if a reset was performed.
  resetExamPanelIfChanged: (signature: string) => boolean;
  clearSession: () => void;
}

export const useSessionStore = create<SessionState>((set) => ({
  sessionId: null,
  currentPhase: 'activation',
  isProcessing: false,
  processingStage: '',
  isRecording: false,
  isSpeaking: false,
  conversation: [],
  language: 'fr',
  examPanelState: {
    answers: {},
    images: {},
    submitted: {},
    revealedCorrections: {},
    currentExIdx: 0,
    currentQIdx: 0,
    examSignature: '',
  },

  setSessionId: (id) => set({ sessionId: id }),
  setPhase: (phase) => set({ currentPhase: phase }),
  setProcessing: (isProcessing, stage = '') => set({ isProcessing, processingStage: stage }),
  setRecording: (isRecording) => set({ isRecording }),
  setSpeaking: (isSpeaking) => set({ isSpeaking }),
  addMessage: (speaker, text, _streaming?, examExercises?) => {
    const id = crypto.randomUUID();
    set((state) => ({
      conversation: [
        ...state.conversation,
        { id, speaker, text, timestamp: new Date(), ...(examExercises ? { examExercises } : {}) },
      ],
    }));
    return id;
  },
  updateMessage: (id, text) =>
    set((state) => ({
      conversation: state.conversation.map((msg) =>
        msg.id === id ? { ...msg, text } : msg
      ),
    })),
  setLanguage: (language) => set({ language }),
  setExamPanelState: (partial) =>
    set((state) => ({
      examPanelState: { ...state.examPanelState, ...partial },
    })),
  resetExamPanelState: () =>
    set({
      examPanelState: {
        answers: {},
        images: {},
        submitted: {},
        revealedCorrections: {},
        currentExIdx: 0,
        currentQIdx: 0,
        examSignature: '',
      },
    }),
  resetExamPanelIfChanged: (signature) => {
    let didReset = false;
    set((state) => {
      if (state.examPanelState.examSignature === signature) {
        return {} as any;
      }
      didReset = true;
      return {
        examPanelState: {
          answers: {},
          images: {},
          submitted: {},
          revealedCorrections: {},
          currentExIdx: 0,
          currentQIdx: 0,
          examSignature: signature,
        },
      };
    });
    return didReset;
  },
  clearSession: () =>
    set({
      sessionId: null,
      currentPhase: 'activation',
      isProcessing: false,
      processingStage: '',
      isRecording: false,
      isSpeaking: false,
      conversation: [],
      examPanelState: {
        answers: {},
        images: {},
        submitted: {},
        revealedCorrections: {},
        currentExIdx: 0,
        currentQIdx: 0,
        examSignature: '',
      },
    }),
}));
