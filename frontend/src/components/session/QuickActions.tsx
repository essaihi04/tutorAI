import { useEffect, useState } from 'react';
import { Zap, ChevronDown, ChevronUp } from 'lucide-react';

/**
 * QuickAction — un bouton raccourci.
 *  - `inject`  : remplit le champ de saisie (l'élève complète avant d'envoyer)
 *  - `send`    : envoie directement le message
 */
export interface QuickAction {
  id: string;
  icon: string;           // emoji
  label: string;          // texte court visible
  prompt: string;         // contenu injecté ou envoyé
  mode: 'inject' | 'send';
  tooltip?: string;       // description longue (title attr)
}

interface QuickActionsProps {
  actions: QuickAction[];
  onInject: (text: string) => void;
  onSend: (text: string) => void;
  disabled?: boolean;
  /** 'light' = fond blanc (Mode Libre) | 'dark' = fond sombre (Coaching) */
  theme?: 'light' | 'dark';
  /** Titre de la barre (ex: "Raccourcis") */
  title?: string;
  /** Permet de plier/déplier la barre (utile sur mobile) */
  collapsible?: boolean;
  /** État replié initial — synchronisé via prop (utile pour auto-replier quand un panneau s'ouvre) */
  defaultCollapsed?: boolean;
}

export default function QuickActions({
  actions,
  onInject,
  onSend,
  disabled = false,
  theme = 'light',
  title = 'Raccourcis',
  collapsible = false,
  defaultCollapsed = false,
}: QuickActionsProps) {
  const [collapsed, setCollapsed] = useState(defaultCollapsed);

  // Resync when parent updates defaultCollapsed (e.g. board/exam panel opens on mobile)
  useEffect(() => {
    setCollapsed(defaultCollapsed);
  }, [defaultCollapsed]);

  if (!actions || actions.length === 0) return null;

  const handleClick = (a: QuickAction) => {
    if (disabled) return;
    if (a.mode === 'send') onSend(a.prompt);
    else onInject(a.prompt);
  };

  // ---- Theming ---------------------------------------------------------
  const isDark = theme === 'dark';

  const wrapperCls = isDark
    ? 'border-t border-white/5 bg-[#0c0c1d]/60 backdrop-blur-sm'
    : 'border-t border-slate-200 bg-slate-50/80 backdrop-blur-sm';

  const titleCls = isDark
    ? 'text-[10px] font-semibold text-white/40 uppercase tracking-wider'
    : 'text-[10px] font-semibold text-slate-400 uppercase tracking-wider';

  const chipCls = (disabled: boolean) =>
    isDark
      ? `flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs font-medium whitespace-nowrap transition-all ${
          disabled
            ? 'bg-white/5 border-white/5 text-white/20 cursor-not-allowed'
            : 'bg-white/5 border-white/10 text-white/80 hover:bg-indigo-500/20 hover:border-indigo-400/40 hover:text-white active:scale-95'
        }`
      : `flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs font-medium whitespace-nowrap transition-all ${
          disabled
            ? 'bg-slate-100 border-slate-200 text-slate-300 cursor-not-allowed'
            : 'bg-white border-slate-200 text-slate-700 hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700 active:scale-95 shadow-sm'
        }`;

  const toggleCls = isDark
    ? 'text-white/40 hover:text-white/70'
    : 'text-slate-400 hover:text-slate-600';

  return (
    <div className={wrapperCls}>
      <div className="max-w-4xl mx-auto px-3 py-2">
        {/* Header (title + collapse toggle) */}
        <div className="flex items-center justify-between mb-1.5">
          <div className="flex items-center gap-1.5">
            <Zap className={`w-3 h-3 ${isDark ? 'text-indigo-400' : 'text-indigo-500'}`} />
            <span className={titleCls}>{title}</span>
          </div>
          {collapsible && (
            <button
              onClick={() => setCollapsed((v) => !v)}
              className={`${toggleCls} transition-colors`}
              title={collapsed ? 'Afficher les raccourcis' : 'Masquer les raccourcis'}
            >
              {collapsed ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronUp className="w-3.5 h-3.5" />}
            </button>
          )}
        </div>

        {/* Chips (scrollable horizontally) */}
        {!collapsed && (
          <div className="flex items-center gap-1.5 overflow-x-auto scrollbar-none pb-1 -mx-1 px-1">
            {actions.map((a) => (
              <button
                key={a.id}
                onClick={() => handleClick(a)}
                disabled={disabled}
                title={a.tooltip || a.label}
                className={chipCls(disabled)}
              >
                <span className="text-sm leading-none">{a.icon}</span>
                <span>{a.label}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
