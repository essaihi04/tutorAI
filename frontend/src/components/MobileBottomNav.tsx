import { BarChart3, Home, MessageCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import type { StudentNavKey } from './StudentNavigation';

const ITEMS = [
  { key: 'today' as const, icon: Home, label: "Aujourd'hui", path: '/dashboard' },
  { key: 'tutor' as const, icon: MessageCircle, label: 'Mon tuteur', path: '/tutor' },
  { key: 'progress' as const, icon: BarChart3, label: 'Mes progrès', path: '/progress' },
];

export default function MobileBottomNav({ active }: { active: StudentNavKey }) {
  const navigate = useNavigate();

  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-40 border-t border-white/[0.07] bg-[#070718]/92 backdrop-blur-2xl md:hidden"
      style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}
      aria-label="Navigation principale"
    >
      <div className="mx-auto grid max-w-md grid-cols-3 px-2 py-1.5">
        {ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = item.key === active;
          return (
            <button
              key={item.key}
              onClick={() => navigate(item.path)}
              className={`relative flex flex-col items-center justify-center gap-1 rounded-xl px-2 py-2 transition-colors ${
                isActive ? 'text-cyan-300' : 'text-white/40 hover:text-white/70'
              }`}
              aria-current={isActive ? 'page' : undefined}
            >
              {isActive && <span className="absolute -top-1.5 h-0.5 w-10 rounded-full bg-gradient-to-r from-indigo-400 to-cyan-300" />}
              <Icon className="h-5 w-5" />
              <span className="text-[10px] font-bold">{item.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}
