import { create } from 'zustand';

export interface DiagnosticResult {
  subject_id: string;
  score: number;
  correct_answers: number;
  total_questions: number;
  weak_topics: string[];
  strong_topics: string[];
}

export interface StudyPlan {
  id: string;
  exam_date: string;
  diagnostic_scores: Record<string, number>;
  total_hours_available: number;
  status: string;
  total_sessions?: number;
  completed_sessions?: number;
  progress_percentage?: number;
}

export interface StudySession {
  id: string;
  plan_id: string;
  subject_id: string;
  chapter_id: string;
  scheduled_date: string;
  scheduled_time: string;
  duration_minutes: number;
  priority: 'high' | 'medium' | 'low';
  status: 'pending' | 'completed' | 'skipped' | 'rescheduled';
  subjects?: { name_fr: string };
  chapters?: { title_fr: string; chapter_number: number };
}

export interface ExamCountdown {
  exam_date: string;
  days_remaining: number;
  hours_remaining: number;
}

export interface Progress {
  overall_progress: number;
  subject_progress: Record<string, number>;
}

interface CoachingState {
  // Diagnostic
  isInDiagnostic: boolean;
  currentDiagnosticSubject: string | null;
  diagnosticResults: Record<string, DiagnosticResult>;
  allDiagnosticsCompleted: boolean;

  // Study Plan
  activePlan: StudyPlan | null;
  hasPlan: boolean;
  todaySessions: StudySession[];
  
  // Progress
  progress: Progress;
  examCountdown: ExamCountdown | null;

  // Actions
  setInDiagnostic: (inDiagnostic: boolean) => void;
  setCurrentDiagnosticSubject: (subjectId: string | null) => void;
  addDiagnosticResult: (subjectId: string, result: DiagnosticResult) => void;
  setAllDiagnosticsCompleted: (completed: boolean) => void;
  
  setActivePlan: (plan: StudyPlan | null) => void;
  setHasPlan: (has: boolean) => void;
  setTodaySessions: (sessions: StudySession[]) => void;
  
  setProgress: (progress: Progress) => void;
  setExamCountdown: (countdown: ExamCountdown) => void;
  
  clearCoachingData: () => void;
}

export const useCoachingStore = create<CoachingState>((set) => ({
  // Initial state
  isInDiagnostic: false,
  currentDiagnosticSubject: null,
  diagnosticResults: {},
  allDiagnosticsCompleted: false,
  
  activePlan: null,
  hasPlan: false,
  todaySessions: [],
  
  progress: {
    overall_progress: 0,
    subject_progress: {}
  },
  examCountdown: null,

  // Actions
  setInDiagnostic: (inDiagnostic) => set({ isInDiagnostic: inDiagnostic }),
  
  setCurrentDiagnosticSubject: (subjectId) => set({ currentDiagnosticSubject: subjectId }),
  
  addDiagnosticResult: (subjectId, result) =>
    set((state) => ({
      diagnosticResults: {
        ...state.diagnosticResults,
        [subjectId]: result
      }
    })),
  
  setAllDiagnosticsCompleted: (completed) => set({ allDiagnosticsCompleted: completed }),
  
  setActivePlan: (plan) => set({ activePlan: plan }),
  
  setHasPlan: (has) => set({ hasPlan: has }),
  
  setTodaySessions: (sessions) => set({ todaySessions: sessions }),
  
  setProgress: (progress) => set({ progress }),
  
  setExamCountdown: (countdown) => set({ examCountdown: countdown }),
  
  clearCoachingData: () =>
    set({
      isInDiagnostic: false,
      currentDiagnosticSubject: null,
      diagnosticResults: {},
      allDiagnosticsCompleted: false,
      activePlan: null,
      hasPlan: false,
      todaySessions: [],
      progress: { overall_progress: 0, subject_progress: {} },
      examCountdown: null
    })
}));
