import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './stores/authStore';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import RegisterInterest from './pages/RegisterInterest';
import Dashboard from './pages/Dashboard';
import LearningSession from './pages/LearningSession';
import AdminResources from './pages/AdminResources';
import AdminDashboard from './pages/AdminDashboard';
import ExamExtractor from './pages/ExamExtractor';
import DiagnosticQuiz from './pages/DiagnosticQuiz';
import StudyPlan from './pages/StudyPlan';
import ExamHub from './pages/ExamHub';
import ExamPractice from './pages/ExamPractice';
import ExamReal from './pages/ExamReal';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/inscription" element={<RegisterInterest />} />
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
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/exam-extractor" element={<ExamExtractor />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}
