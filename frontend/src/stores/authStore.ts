import { create } from 'zustand';
import { useLearningContextStore } from './learningContextStore';

interface AuthState {
  token: string | null;
  refreshToken: string | null;
  student: {
    id: string;
    username: string;
    email: string;
    full_name: string;
    preferred_language: string;
  } | null;
  isAuthenticated: boolean;
  login: (token: string, student: AuthState['student'], refreshToken?: string | null) => void;
  setTokens: (token: string, refreshToken?: string | null) => void;
  setStudent: (student: AuthState['student']) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  refreshToken: localStorage.getItem('refresh_token'),
  student: JSON.parse(localStorage.getItem('student') || 'null'),
  isAuthenticated: !!localStorage.getItem('token'),
  login: (token, student, refreshToken) => {
    useLearningContextStore.getState().reset();
    localStorage.setItem('token', token);
    if (refreshToken) localStorage.setItem('refresh_token', refreshToken);
    localStorage.setItem('student', JSON.stringify(student));
    set({ token, refreshToken: refreshToken ?? null, student, isAuthenticated: true });
  },
  setTokens: (token, refreshToken) => {
    localStorage.setItem('token', token);
    if (refreshToken) localStorage.setItem('refresh_token', refreshToken);
    set({ token, refreshToken: refreshToken ?? null });
  },
  setStudent: (student) => {
    if (student?.id !== useLearningContextStore.getState().context?.student_id) {
      useLearningContextStore.getState().reset();
    }
    if (student) localStorage.setItem('student', JSON.stringify(student));
    set({ student });
  },
  logout: () => {
    useLearningContextStore.getState().reset();
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('student');
    set({ token: null, refreshToken: null, student: null, isAuthenticated: false });
  },
}));
