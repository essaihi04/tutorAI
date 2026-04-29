import { useNavigate } from 'react-router-dom';
import { BarChart3, GraduationCap, MessageCircle, Trophy, Sparkles } from 'lucide-react';

export type MobileNavKey = 'dashboard' | 'coaching' | 'libre' | 'exam' | 'mock';

const ITEMS: Array<{ key: MobileNavKey; icon: any; label: string; path: string }> = [
  { key: 'dashboard', icon: BarChart3,     label: 'Accueil',   path: '/dashboard' },
  { key: 'coaching',  icon: GraduationCap, label: 'Coaching',  path: '/coaching/plan' },
  { key: 'libre',     icon: MessageCircle, label: 'Libre',     path: '/libre' },
  { key: 'exam',      icon: Trophy,        label: 'Examens',   path: '/exam' },
  { key: 'mock',      icon: Sparkles,      label: 'Blancs',    path: '/mock-exam' },
];

/**
 * MobileBottomNav — barre de navigation fixe en bas, visible uniquement < lg (1024px).
 * Ajoute `pb-20 lg:pb-0` (ou similaire) sur le contenu de la page pour éviter le chevauchement.
 */
export default function MobileBottomNav({ active }: { active: MobileNavKey }) {
  const navigate = useNavigate();

  return (
    <nav
      className="lg:hidden fixed bottom-0 left-0 right-0 z-40 backdrop-blur-2xl bg-[#070718]/85 border-t border-white/5"
      style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}
      aria-label="Navigation principale"
    >
      <div className="flex items-stretch justify-around px-1 py-1">
        {ITEMS.map((it) => {
          const isActive = it.key === active;
          const Icon = it.icon;
          return (
            <button
              key={it.key}
              onClick={() => navigate(it.path)}
              className={`relative flex-1 flex flex-col items-center justify-center gap-0.5 py-2 px-1 rounded-xl transition-colors ${
                isActive
                  ? 'text-indigo-300'
                  : 'text-white/45 hover:text-white/70'
              }`}
              aria-current={isActive ? 'page' : undefined}
            >
              {isActive && (
                <span className="absolute top-0 left-1/2 -translate-x-1/2 w-8 h-[2px] rounded-full bg-gradient-to-r from-indigo-400 to-cyan-400" />
              )}
              <Icon className={`w-5 h-5 ${isActive ? '' : ''}`} />
              <span className="text-[10px] font-semibold leading-tight">{it.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}
