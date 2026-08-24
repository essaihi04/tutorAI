import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { lazy, Suspense, useEffect } from 'react';
import { useAuthStore } from './stores/authStore';
import { useLearningContextStore } from './stores/learningContextStore';

// ── Eagerly loaded (landing / auth — needed on first paint) ──
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import RegisterInterest from './pages/RegisterInterest';

// ── Lazy-loaded (code-split into separate chunks) ──
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Progress = lazy(() => import('./pages/Progress'));
const CourseLibrary = lazy(() => import('./pages/CourseLibrary'));
const LearningSession = lazy(() => import('./pages/LearningSession'));
const AdminDashboard = lazy(() => import('./pages/AdminDashboard'));
const ExamExtractor = lazy(() => import('./pages/ExamExtractor'));
const DiagnosticQuiz = lazy(() => import('./pages/DiagnosticQuiz'));
const StudyPlan = lazy(() => import('./pages/StudyPlan'));
const ExamHub = lazy(() => import('./pages/ExamHub'));
const ExamPractice = lazy(() => import('./pages/ExamPractice'));
const ExamReal = lazy(() => import('./pages/ExamReal'));
const MockExamHub = lazy(() => import('./pages/MockExamHub'));
const MockExamTake = lazy(() => import('./pages/MockExamTake'));
const Orientation = lazy(() => import('./pages/Orientation'));
const DiagnosticBac = lazy(() => import('./pages/DiagnosticBac'));
const DiagnosticBacResults = lazy(() => import('./pages/DiagnosticBacResults'));

// Planche de contrôle des visuels — jamais servie en production.
const VisualAudit = lazy(() => import('./dev/VisualAudit'));
// Planche de contrôle des tableaux — jamais servie en production.
const BoardAudit = lazy(() => import('./dev/BoardAudit'));
const AdminVisualLibraryAudit = lazy(() => import('./dev/AdminVisualLibraryAudit'));

function PageLoader() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#070718]">
      <div className="flex flex-col items-center gap-3">
        <div className="w-10 h-10 border-4 border-indigo-500/30 border-t-indigo-400 rounded-full animate-spin" />
        <span className="text-sm text-white/50">Chargement…</span>
      </div>
    </div>
  );
}

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const studentId = useAuthStore((s) => s.student?.id || 'authenticated-student');
  const loadLearningContext = useLearningContextStore((s) => s.load);
  const readyForStudentId = useLearningContextStore((s) => s.readyForStudentId);

  useEffect(() => {
    if (isAuthenticated) void loadLearningContext(studentId);
  }, [isAuthenticated, loadLearningContext, studentId]);

  if (!isAuthenticated) return <Navigate to="/login" />;
  if (readyForStudentId !== studentId) return <PageLoader />;
  return <>{children}</>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          {/* Eagerly loaded — no Suspense needed */}
          <Route path="/" element={<Landing />} />
          {import.meta.env.DEV && <Route path="/dev/visual-audit" element={<VisualAudit />} />}
          {import.meta.env.DEV && <Route path="/dev/board-audit" element={<BoardAudit />} />}
          {import.meta.env.DEV && <Route path="/dev/admin-visual-library" element={<AdminVisualLibraryAudit />} />}
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/inscription" element={<RegisterInterest />} />
          <Route path="/orientation" element={<Orientation />} />
          <Route path="/bac-diagnostic" element={<DiagnosticBac />} />
          <Route path="/bac-diagnostic/results" element={<DiagnosticBacResults />} />

          {/* Lazy-loaded protected routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          {/* `/tutor` n'est plus un menu : c'est la session elle-même.
              L'élève y entre et il est déjà en train de travailler ; le mode
              (cours, exercice, examen, question) change DANS l'écran, sans
              navigation, et le tuteur peut en décider lui-même. */}
          <Route
            path="/tutor"
            element={
              <ProtectedRoute>
                <LearningSession mode="libre" />
              </ProtectedRoute>
            }
          />
          <Route
            path="/courses"
            element={
              <ProtectedRoute>
                <CourseLibrary />
              </ProtectedRoute>
            }
          />
          <Route
            path="/progress"
            element={
              <ProtectedRoute>
                <Progress />
              </ProtectedRoute>
            }
          />
          <Route
            path="/session/:chapterId/:lessonId?"
            element={
              <ProtectedRoute>
                <LearningSession />
              </ProtectedRoute>
            }
          />
          <Route
            path="/coaching/diagnostic"
            element={
              <ProtectedRoute>
                <DiagnosticQuiz />
              </ProtectedRoute>
            }
          />
          <Route
            path="/coaching/plan"
            element={
              <ProtectedRoute>
                <StudyPlan />
              </ProtectedRoute>
            }
          />
          <Route
            path="/libre"
            element={
              <ProtectedRoute>
                <LearningSession mode="libre" />
              </ProtectedRoute>
            }
          />
          <Route
            path="/exam-explain"
            element={
              <ProtectedRoute>
                <LearningSession mode="explain" />
              </ProtectedRoute>
            }
          />
          <Route
            path="/exam"
            element={
              <ProtectedRoute>
                <ExamHub />
              </ProtectedRoute>
            }
          />
          <Route
            path="/exam/practice/:examId"
            element={
              <ProtectedRoute>
                <ExamPractice />
              </ProtectedRoute>
            }
          />
          <Route
            path="/exam/real/:examId"
            element={
              <ProtectedRoute>
                <ExamReal />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/resources"
            element={<Navigate to="/admin?tab=visuals" replace />}
          />
          <Route
            path="/mock-exam"
            element={
              <ProtectedRoute>
                <MockExamHub />
              </ProtectedRoute>
            }
          />
          <Route
            path="/mock-exam/:subject/:examId"
            element={
              <ProtectedRoute>
                <MockExamTake />
              </ProtectedRoute>
            }
          />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/exam-extractor" element={<ExamExtractor />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
