import { BarChart3, Home, LogOut, MessageCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { useLearningContextStore } from '../stores/learningContextStore';
import type { LearningSubject } from '../stores/learningContextStore';
import { MoalimLogo } from './MoalimShell';

export type StudentNavKey = 'today' | 'tutor' | 'progress';

const NAV_ITEMS = [
  { key: 'today' as const, label: "Aujourd'hui", icon: Home, path: '/dashboard' },
  { key: 'tutor' as const, label: 'Mon tuteur', icon: MessageCircle, path: '/tutor' },
  { key: 'progress' as const, label: 'Mes progrès', icon: BarChart3, path: '/progress' },
];
const EMPTY_SUBJECTS: LearningSubject[] = [];

export default function StudentNavigation({ active }: { active: StudentNavKey }) {
  const navigate = useNavigate();
  const logout = useAuthStore((state) => state.logout);
  const subjects = useLearningContextStore((state) => state.context?.subjects || EMPTY_SUBJECTS);

  const handleLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

  return (
    <header className="sticky top-0 z-40 border-b border-white/[0.07] bg-[#070718]/88 backdrop-blur-2xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center gap-3 px-4 sm:px-6 lg:px-8">
        <button onClick={() => navigate('/dashboard')} className="shrink-0" aria-label="Retour à l'accueil">
          <MoalimLogo size="sm" />
        </button>

        <nav className="mx-auto hidden items-center gap-1 rounded-2xl border border-white/[0.07] bg-white/[0.035] p-1 md:flex" aria-label="Navigation élève">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = active === item.key;
            return (
              <button
                key={item.key}
                onClick={() => navigate(item.path)}
                className={`flex items-center gap-2 rounded-xl px-4 py-2 text-sm font-semibold transition-all ${
                  isActive
                    ? 'bg-white/[0.11] text-white shadow-sm'
                    : 'text-white/45 hover:bg-white/[0.05] hover:text-white/80'
                }`}
                aria-current={isActive ? 'page' : undefined}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </button>
            );
          })}
        </nav>

        <div className="ml-auto flex min-w-0 items-center gap-2 md:ml-0">
          {subjects.length > 0 && (
            <div className="hidden max-w-[260px] items-center gap-1.5 lg:flex" aria-label="Matières accessibles">
              {subjects.slice(0, 3).map((subject) => (
                <span
                  key={subject.id}
                  className="max-w-[90px] truncate rounded-full border border-white/[0.07] bg-white/[0.04] px-2.5 py-1 text-[10px] font-semibold text-white/55"
                  title={subject.name_fr}
                >
                  {subject.icon || '•'} {subject.name_fr}
                </span>
              ))}
            </div>
          )}
          <button
            onClick={handleLogout}
            className="rounded-xl p-2.5 text-white/35 transition-colors hover:bg-rose-500/10 hover:text-rose-300"
            aria-label="Se déconnecter"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </div>
    </header>
  );
}
