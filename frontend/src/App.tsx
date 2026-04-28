import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import { useAuthStore } from './stores/authStore';

// ── Eagerly loaded (landing / auth — needed on first paint) ──
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import RegisterInterest from './pages/RegisterInterest';

// ── Lazy-loaded (code-split into separate chunks) ──
const Dashboard = lazy(() => import('./pages/Dashboard'));
const LearningSession = lazy(() => import('./pages/LearningSession'));
const AdminResources = lazy(() => import('./pages/AdminResources'));
const AdminDashboard = lazy(() => import('./pages/AdminDashboard'));
const ExamExtractor = lazy(() => import('./pages/ExamExtractor'));
const DiagnosticQuiz = lazy(() => import('./pages/DiagnosticQuiz'));
const StudyPlan = lazy(() => import('./pages/StudyPlan'));
const ExamHub = lazy(() => import('./pages/ExamHub'));
const ExamPractice = lazy(() => import('./pages/ExamPractice'));
const ExamReal = lazy(() => import('./pages/ExamReal'));
const MockExamHub = lazy(() => import('./pages/MockExamHub'));
const MockExamTake = lazy(() => import('./pages/MockExamTake'));

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
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          {/* Eagerly loaded — no Suspense needed */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/inscription" element={<RegisterInterest />} />

          {/* Lazy-loaded protected routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/session/:chapterId"
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
            element={
              <ProtectedRoute>
                <AdminResources />
              </ProtectedRoute>
            }
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
