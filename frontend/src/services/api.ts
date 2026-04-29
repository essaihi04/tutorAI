import axios from 'axios';
import type { AxiosError, InternalAxiosRequestConfig } from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ──────────────────────────────────────────────────────────────
// Auto-refresh on 401 token_expired, then retry the original
// request ONCE. Multiple concurrent 401s share a single refresh.
// ──────────────────────────────────────────────────────────────
type RetriableConfig = InternalAxiosRequestConfig & { _retry?: boolean };

let refreshPromise: Promise<string> | null = null;

async function performRefresh(): Promise<string> {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) throw new Error('no_refresh_token');

  // Use a bare axios instance to avoid recursive interceptor loops
  const res = await axios.post('/api/v1/auth/refresh', { refresh_token: refreshToken });
  const { access_token, refresh_token: newRefresh } = res.data;

  if (!access_token) throw new Error('refresh_failed');
  localStorage.setItem('token', access_token);
  if (newRefresh) localStorage.setItem('refresh_token', newRefresh);
  return access_token;
}

api.interceptors.response.use(
  (res) => res,
  async (error: AxiosError<any>) => {
    const original = error.config as RetriableConfig | undefined;
    const status = error.response?.status;
    const detail = (error.response?.data as any)?.detail;

    const isExpired =
      status === 401 &&
      typeof detail === 'string' &&
      (detail === 'token_expired' || detail.toLowerCase().includes('expired'));

    if (!isExpired || !original || original._retry) {
      // Refresh itself failed → wipe session and force re-login
      if (status === 401 && detail === 'refresh_token_invalid') {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('student');
        if (window.location.pathname !== '/login') {
          window.location.assign('/login');
        }
      }
      return Promise.reject(error);
    }

    original._retry = true;

    try {
      if (!refreshPromise) {
        refreshPromise = performRefresh().finally(() => {
          refreshPromise = null;
        });
      }
      const newToken = await refreshPromise;
      original.headers = original.headers ?? {};
      (original.headers as any).Authorization = `Bearer ${newToken}`;
      return api.request(original);
    } catch (refreshErr) {
      // Refresh failed → session dead
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('student');
      if (window.location.pathname !== '/login') {
        window.location.assign('/login');
      }
      return Promise.reject(refreshErr);
    }
  }
);

// Auth
export const registerStudent = (data: {
  username: string;
  email: string;
  password: string;
  full_name: string;
  preferred_language: string;
}) => api.post('/auth/register', data);

export const loginStudent = (data: { email: string; password: string }) =>
  api.post('/auth/login', data);

export const getMe = () => api.get('/auth/me');

// Content
export const getSubjects = () => api.get('/content/subjects');
export const getChapters = (subjectId: string) =>
  api.get(`/content/subjects/${subjectId}/chapters`);
export const getLessons = (chapterId: string) =>
  api.get(`/content/chapters/${chapterId}/lessons`);
export const getExercises = (lessonId: string) =>
  api.get(`/content/lessons/${lessonId}/exercises`);

// Sessions
export const startSession = (lessonId: string, isReview = false) =>
  api.post('/sessions/start', { lesson_id: lessonId, is_review: isReview });
export const endSession = (sessionId: string) =>
  api.post('/sessions/end', { session_id: sessionId });
export const getProfile = () => api.get('/sessions/profile');

// Coaching Mode
export const startDiagnostic = (subjectId: string, variationSeed?: string) =>
  api.post('/coaching/start-diagnostic', { subject_id: subjectId, variation_seed: variationSeed });
export const startDiagnosticSession = (subjectId: string, numQuestions: number = 10) =>
  api.post('/coaching/start-diagnostic-session', { subject_id: subjectId, num_questions: numQuestions });
export const nextDiagnosticQuestion = (sessionId: string) =>
  api.post('/coaching/next-diagnostic-question', { session_id: sessionId });
export const submitDiagnostic = (subjectId: string, questions: any[], answers: Record<string, string>) =>
  api.post('/coaching/submit-diagnostic', { subject_id: subjectId, questions, answers });
export const generatePlan = (diagnosticScores: Record<string, number>) =>
  api.post('/coaching/generate-plan', { diagnostic_scores: diagnosticScores });
export const getStudyPlan = () => api.get('/coaching/plan');
export const getTodaySchedule = () => api.get('/coaching/today');
export const getAllSessions = () => api.get('/coaching/all-sessions');
export const regeneratePlan = () => api.post('/coaching/regenerate-plan');
export const completeSession = (sessionId: string) =>
  api.post('/coaching/complete-session', { session_id: sessionId });
export const getProgress = () => api.get('/coaching/progress');
export const getExamCountdown = () => api.get('/coaching/exam-countdown');
export const getDiagnosticHistory = () => api.get('/coaching/diagnostic-history');
export const getProficiency = () => api.get('/coaching/proficiency');
export const getAdaptiveNext = () => api.get('/coaching/adaptive-next');
export const adaptPlan = () => api.post('/coaching/adapt-plan');
export const getCoachingContext = () => api.get('/coaching/coaching-context');

// Lesson Progress (Session Memory)
export const getLessonProgress = (lessonId: string) =>
  api.get(`/coaching/lesson-progress/${lessonId}`);
export const getAllLessonProgress = () => api.get('/coaching/all-lesson-progress');
export const markObjectiveCompleted = (lessonId: string, objectiveIndex: number, objectiveText: string, keyPoints?: string[]) =>
  api.post('/coaching/mark-objective', { lesson_id: lessonId, objective_index: objectiveIndex, objective_text: objectiveText, key_points: keyPoints });
export const saveSessionSummary = (lessonId: string, summary: string) =>
  api.post('/coaching/save-session-summary', { lesson_id: lessonId, summary });

// Libre Mode
export const startLibreSession = (title?: string) =>
  api.post('/libre/start', { title });
export const getLibreHistory = (limit = 20) =>
  api.get('/libre/history', { params: { limit } });
export const getLibreConversation = (conversationId: string) =>
  api.get(`/libre/conversation/${conversationId}`);
export const endLibreSession = (conversationId: string) =>
  api.post(`/libre/end/${conversationId}`);

// Exam Mode
export const listExams = (subject?: string, year?: number) =>
  api.get('/exam/list', { params: { subject, year } });
export const getExamStats = () => api.get('/exam/stats');
export const listExtractedExams = (subject?: string, year?: number) =>
  api.get('/exam/extracted/list', { params: { subject, year } });
export const getExamDetail = (examId: string) =>
  api.get(`/exam/detail/${examId}`);
export const getExamQuestion = (examId: string, questionIndex: number) =>
  api.get(`/exam/question/${examId}/${questionIndex}`);
export const evaluateExamAnswer = (
  examId: string,
  questionIndex: number,
  studentAnswer: string,
  studentImage?: string | null,
  attemptId?: string | null,
) =>
  api.post('/exam/evaluate', {
    exam_id: examId,
    question_index: questionIndex,
    student_answer: studentAnswer,
    ...(studentImage ? { student_image: studentImage } : {}),
    ...(attemptId ? { attempt_id: attemptId } : {}),
  });
export const extractTextFromImage = (imageBase64: string, questionContent?: string, subject?: string) =>
  api.post('/exam/extract-text', { image_base64: imageBase64, question_content: questionContent || '', subject: subject || '' });
export const submitExam = (
  examId: string,
  answers: Record<string, string>,
  mode: string,
  durationSeconds: number,
  attemptId?: string | null,
) =>
  api.post('/exam/submit', {
    exam_id: examId,
    answers,
    mode,
    duration_seconds: durationSeconds,
    ...(attemptId ? { attempt_id: attemptId } : {}),
  });
export const startExam = (examId: string, mode: 'practice' | 'real') =>
  api.post('/exam/start', { exam_id: examId, mode });
export const saveExamProgress = (
  attemptId: string,
  data: { answers?: Record<string, string>; current_question_index?: number; duration_seconds?: number },
) => api.post('/exam/save-progress', { attempt_id: attemptId, ...data });
export const getExamHistory = (limit = 20) =>
  api.get('/exam/history', { params: { limit } });
export const getMyExamStats = () => api.get('/exam/my-stats');

// Admin Dashboard
const adminApi = axios.create({
  baseURL: '/api/v1/admin',
  headers: { 'Content-Type': 'application/json' },
});

adminApi.interceptors.request.use((config) => {
  const adminToken = localStorage.getItem('admin_token');
  if (adminToken) {
    config.headers.Authorization = `Bearer ${adminToken}`;
  }
  return config;
});

// On 401, clear the admin token and notify the app to redirect to login
adminApi.interceptors.response.use(
  (res) => res,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token');
      // Notify the AdminDashboard component to switch back to login screen
      window.dispatchEvent(new Event('admin:unauthorized'));
    }
    return Promise.reject(error);
  }
);

export const adminLogin = (password: string) =>
  api.post('/admin/login', { password });
export const getAdminDashboard = () => adminApi.get('/dashboard');
export const getAdminUsers = () => adminApi.get('/users');
export const createAdminUser = (data: { email: string; password: string; full_name: string; username: string; promo_code?: string; is_admin?: boolean }) =>
  adminApi.post('/users', data);
export const updateAdminUser = (userId: string, data: Record<string, any>) =>
  adminApi.put(`/users/${userId}`, data);
export const deleteAdminUser = (userId: string) =>
  adminApi.delete(`/users/${userId}`);
export const bulkUserAction = (userIds: string[], action: 'delete' | 'activate' | 'deactivate') =>
  adminApi.post('/users/bulk-action', { user_ids: userIds, action });
export const resetUserPassword = (userId: string, newPassword: string) =>
  adminApi.post(`/users/${userId}/reset-password`, { new_password: newPassword });
export const getOnlineUsers = () => adminApi.get('/online');
export const getUsageSummary = (days?: number) =>
  adminApi.get('/usage/summary', { params: { days } });
export const getUsageByUser = (days?: number) =>
  adminApi.get('/usage/by-user', { params: { days } });
export const getRecentRequests = (limit?: number) =>
  adminApi.get('/usage/recent', { params: { limit } });
export const listPromoCodes = () => adminApi.get('/promo-codes');
export const createPromoCode = (data: { code: string; label?: string; is_active?: boolean }) =>
  adminApi.post('/promo-codes', data);
export const updatePromoCode = (id: string, data: { label?: string; is_active?: boolean }) =>
  adminApi.patch(`/promo-codes/${id}`, data);
export const deletePromoCode = (id: string) =>
  adminApi.delete(`/promo-codes/${id}`);

// ─── Registration requests (pre-inscriptions) ──────────────────────
export interface RegistrationRequestPayload {
  nom: string;
  prenom: string;
  phone: string;
  ville: string;
  email?: string;
  niveau?: string;
  promo_code?: string;
  message?: string;
}

export const submitRegistrationRequest = (data: RegistrationRequestPayload) =>
  api.post('/registration-requests', data);

export const listRegistrationRequests = (status?: string) =>
  adminApi.get('/registration-requests', { params: status ? { status } : {} });

export const updateRegistrationRequest = (
  id: string,
  data: { status?: string; admin_notes?: string }
) => adminApi.patch(`/registration-requests/${id}`, data);

export const deleteRegistrationRequest = (id: string) =>
  adminApi.delete(`/registration-requests/${id}`);

export const activateRegistration = (
  id: string,
  data: { password: string; account_type: 'test' | 'permanent'; username?: string; promo_code?: string }
) => adminApi.post(`/registration-requests/${id}/activate`, data);

// ─── Mock Exam (Examens Blancs) ───────────────────────────────────────
const mockExamAdminApi = axios.create({
  baseURL: '/api/v1/mock-exam',
  headers: { 'Content-Type': 'application/json' },
});
mockExamAdminApi.interceptors.request.use((config) => {
  const adminToken = localStorage.getItem('admin_token');
  if (adminToken) {
    config.headers.Authorization = `Bearer ${adminToken}`;
  }
  return config;
});

export const generateMockExam = (data: { subject?: string; target_domains?: string[] }) =>
  mockExamAdminApi.post('/generate', data);

export const listMockExams = (subject?: string) =>
  mockExamAdminApi.get('/list', { params: subject ? { subject } : {} });

export const getMockExam = (subject: string, examId: string) =>
  api.get(`/mock-exam/${subject}/${examId}`);

export const getMockExamImagePrompts = (subject: string, examId: string) =>
  mockExamAdminApi.get(`/${subject}/${examId}/image-prompts`);

export const updateMockExamStatus = (subject: string, examId: string, status: string) =>
  mockExamAdminApi.patch(`/${subject}/${examId}/status`, { status });

export const uploadMockExamImage = (subject: string, examId: string, docId: string, file: File) => {
  const formData = new FormData();
  formData.append('doc_id', docId);
  formData.append('file', file);
  return mockExamAdminApi.post(`/${subject}/${examId}/upload-image`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const listMockExamImages = (subject: string, examId: string) =>
  mockExamAdminApi.get(`/${subject}/${examId}/images`);

export const deleteMockExamImage = (subject: string, examId: string, docId: string) =>
  mockExamAdminApi.delete(`/${subject}/${examId}/image/${docId}`);

export const listPublishedMockExams = (subject?: string) =>
  api.get('/mock-exam/published', { params: subject ? { subject } : {} });

// ─── Concours (Orientation Post-BAC) ──────────────────────────────────
export const getConcoursCatalog = () => api.get('/concours/catalog');

export type SimulateInput =
  | { moyenne_bac: number }
  | { cc1?: number; cc2?: number; regional: number; national_estimated: number };

export const simulateConcours = (data: SimulateInput) =>
  api.post('/concours/simulate', data);

export default api;
