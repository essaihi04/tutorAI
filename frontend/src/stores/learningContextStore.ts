import { create } from 'zustand';
import { getLearningContext } from '../services/api';

export interface LearningSubject {
  id: string;
  name_fr: string;
  name_ar: string;
  icon?: string | null;
  color?: string | null;
  order_index?: number;
  catalog_key: string;
}

export interface LearningContext {
  student_id: string;
  filiere: string | null;
  access_mode: 'legacy' | 'managed';
  subjects: LearningSubject[];
  subject_ids: string[];
  subject_names: string[];
  exam_subject_keys: string[];
  primary_subject_id: string | null;
}

interface LearningContextState {
  context: LearningContext | null;
  loading: boolean;
  readyForStudentId: string | null;
  error: string | null;
  load: (studentId: string) => Promise<void>;
  reset: () => void;
}

let inFlight: Promise<void> | null = null;

export const useLearningContextStore = create<LearningContextState>((set, get) => ({
  context: null,
  loading: false,
  readyForStudentId: null,
  error: null,

  load: async (studentId: string) => {
    if (get().readyForStudentId === studentId) return;
    if (inFlight) return inFlight;

    set({ loading: true, error: null });
    inFlight = getLearningContext()
      .then((response) => {
        set({
          context: response.data as LearningContext,
          readyForStudentId: studentId,
          loading: false,
          error: null,
        });
      })
      .catch((error) => {
        console.error('Failed to load learning context:', error);
        // Mark the attempt ready so a temporary backend problem does not trap
        // the student on a permanent loader. Student endpoints still enforce
        // access independently.
        set({
          context: null,
          readyForStudentId: studentId,
          loading: false,
          error: "Impossible de charger les matières de l'élève",
        });
      })
      .finally(() => {
        inFlight = null;
      });

    return inFlight;
  },

  reset: () => set({ context: null, loading: false, readyForStudentId: null, error: null }),
}));
