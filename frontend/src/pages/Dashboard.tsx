import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getExamCountdown, getStudyPlan, getTodaySchedule, getProficiency, getMyExamStats, getMe,
} from '../services/api';
import { useAuthStore } from '../stores/authStore';
import {
  GraduationCap, MessageCircle, Calendar, Play, LogOut, Settings,
  FileText, Share2, X as XIcon, Copy, Check,
  Flame, Zap, Award, Star, ChevronRight, Target, Trophy,
} from 'lucide-react';
import MoalimShell, { MoalimLogo } from '../components/MoalimShell';

const SUBJECT_ACCENT: Record<string, string> = {
  'Mathématiques': 'from-amber-400 to-orange-500',
  'Physique':      'from-indigo-400 to-blue-500',
  'Chimie':        'from-rose-400 to-pink-500',
  'SVT':           'from-emerald-400 to-teal-500',
};

const CANONICAL_TO_DISPLAY: Record<string, string> = {
  'Mathematiques': 'Mathématiques',
  'Physique': 'Physique',
  'Chimie': 'Chimie',
  'SVT': 'SVT',
};

const PRIORITY_META: Record<string, { label: string; text: string }> = {
  critique: { label: 'Critique', text: 'text-rose-300' },
  haute:    { label: 'Haute',    text: 'text-amber-300' },
  moyenne:  { label: 'Moyenne',  text: 'text-white/50' },
};

export default function Dashboard() {
  const [countdown, setCountdown] = useState<any>(null);
  const [hasPlan, setHasPlan] = useState(false);
  const [planProgress, setPlanProgress] = useState(0);
  const [todaySessions, setTodaySessions] = useState<any[]>([]);
  const [proficiency, setProficiency] = useState<any>(null);
  const [examStats, setExamStats] = useState<any>(null);
  const [shareOpen, setShareOpen] = useState(false);
  const navigate = useNavigate();
  const { student, logout, setStudent } = useAuthStore();

  useEffect(() => {
    loadData();
    if (!student?.full_name) {
      getMe()
        .then((res) => {
          setStudent({
            id: String(res.data.id || ''),
            username: res.data.username || '',
            email: res.data.email || '',
            full_name: res.data.full_name || '',
            preferred_language: res.data.preferred_language || 'fr',
          });
        })
        .catch(() => {});
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadData = async () => {
    try {
      const countdownRes = await getExamCountdown().catch(() => null);
      if (countdownRes) setCountdown(countdownRes.data);
      try {
        const [planRes, todayRes, profRes, examStatsRes] = await Promise.all([
          getStudyPlan(),
          getTodaySchedule(),
          getProficiency().catch(() => null),
          getMyExamStats().catch(() => null),
        ]);
        if (planRes.data.has_plan) {
          setHasPlan(true);
          setPlanProgress(planRes.data.plan.progress_percentage || 0);
        }
        setTodaySessions(todayRes.data.sessions || []);
        if (profRes?.data) setProficiency(profRes.data);
        if (examStatsRes?.data) setExamStats(examStatsRes.data);
      } catch {
        /* coaching data not available */
      }
    } catch {
      /* api not ready */
    }
  };

  const { topLacunes, totalLacunes } = useMemo(() => {
    const all: any[] = (proficiency?.lacunes as any[]) || [];
    return { topLacunes: all.slice(0, 3), totalLacunes: all.length };
  }, [proficiency]);

  const examsCompleted = examStats?.unique_exams_taken || 0;
  const questionsAnswered = examStats?.total_questions_answered || 0;
  const avgScore = examStats?.avg_score_pct || 0;
  const inProgressCount = examStats?.in_progress_count || 0;
  const daysRemaining = countdown?.days_remaining || 0;

  const firstName = (student?.full_name || 'Étudiant').trim().split(/\s+/)[0];
  const hour = new Date().getHours();
  const timeGreeting =
    hour < 12 ? 'Bonjour' : hour < 18 ? 'Bon après-midi' : 'Bonsoir';

  const encouragement = useMemo(() => {
    if (questionsAnswered >= 100) return { text: 'Tu es un champion ! Continue comme ça !', icon: '🏆' };
    if (examsCompleted >= 5) return { text: 'Excellent travail, tu progresses vite !', icon: '🚀' };
    if (questionsAnswered >= 30) return { text: 'Beau rythme, chaque question te rapproche du BAC !', icon: '💪' };
    if (examsCompleted >= 1) return { text: 'Super début ! Tu es sur la bonne voie !', icon: '⭐' };
    return { text: 'Commence par un examen, tu vas tout déchirer !', icon: '🎯' };
  }, [examsCompleted, questionsAnswered]);

  return (
    <MoalimShell>
      <div className="h-screen flex flex-col">
        {/* ── Header ── */}
        <header className="sticky top-0 z-30 backdrop-blur-2xl bg-[#070718]/70 border-b border-white/5">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 py-2.5 flex items-center gap-3">
            <MoalimLogo size="sm" />
            <div className="hidden md:block ml-2 text-[11px] text-white/40 border-l border-white/10 pl-3">
              2ème BAC PC BIOF
            </div>
            <div className="flex-1" />
            <button onClick={() => setShareOpen(true)} className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-indigo-500 to-cyan-500 text-white text-xs font-semibold hover:shadow-lg hover:shadow-indigo-500/40 transition-all">
              <Share2 className="w-3.5 h-3.5" /> Partager
            </button>
            <button onClick={() => setShareOpen(true)} className="sm:hidden p-2 rounded-lg bg-gradient-to-r from-indigo-500 to-cyan-500 text-white">
              <Share2 className="w-4 h-4" />
            </button>
            <button onClick={() => navigate('/admin/resources')} className="p-2 text-white/40 hover:text-white hover:bg-white/5 rounded-lg transition-colors">
              <Settings className="w-4 h-4" />
            </button>
            <button onClick={logout} className="p-2 text-white/40 hover:text-rose-300 hover:bg-rose-500/10 rounded-lg transition-colors">
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </header>

        {/* ── Main ── */}
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-3 flex flex-col gap-3 min-h-0 overflow-hidden">
          {/* Row 1: Welcome + countdown + stats */}
          <div className="flex items-stretch gap-3">
            {/* Welcome */}
            <div className="flex-1 glass rounded-2xl p-4 sm:p-5 relative overflow-hidden anim-fade-up">
              <div className="absolute -top-12 -right-12 w-40 h-40 rounded-full bg-indigo-500/30 blur-3xl" />
              <div className="absolute -bottom-12 -left-12 w-32 h-32 rounded-full bg-cyan-500/20 blur-3xl" />
              <div className="relative">
                <p className="text-[11px] font-semibold text-white/45 uppercase tracking-widest">{timeGreeting}</p>
                <h2 className="text-2xl sm:text-3xl font-black leading-tight mt-0.5 text-white">
                  {firstName} <span className="inline-block animate-wave">👋</span>
                </h2>
                <div className="inline-flex items-center gap-1.5 mt-2.5 px-2.5 py-1 rounded-lg bg-white/5 border border-white/10">
                  <span className="text-sm">{encouragement.icon}</span>
                  <span className="text-[11px] font-semibold text-white/80">{encouragement.text}</span>
                </div>
              </div>
            </div>

            {/* BAC Countdown */}
            {countdown && (
              <div className="w-28 sm:w-32 shrink-0 rounded-2xl bg-gradient-to-br from-rose-500 to-orange-500 p-3 text-white text-center flex flex-col items-center justify-center shadow-2xl shadow-rose-500/30">
                <Flame className="w-5 h-5 opacity-80 mb-1" />
                <span className="text-3xl font-black leading-none">{daysRemaining}</span>
                <span className="text-[10px] font-bold uppercase tracking-wider opacity-90 mt-0.5">jours</span>
                <span className="text-[9px] opacity-70">avant BAC</span>
              </div>
            )}

            {/* Stats — desktop */}
            <div className="hidden md:grid grid-cols-3 gap-2 shrink-0" style={{ width: '320px' }}>
              <KpiTile icon={FileText} label="Examens" value={examsCompleted} hint={inProgressCount > 0 ? `${inProgressCount} en cours` : undefined} grad="from-emerald-500 to-teal-500" />
              <KpiTile icon={Zap} label="Questions" value={questionsAnswered} grad="from-amber-500 to-orange-500" />
              <KpiTile icon={Award} label="Moyenne" value={`${Math.round(avgScore)}%`} grad="from-violet-500 to-fuchsia-500" />
            </div>
          </div>

          {/* Mobile stats */}
          <div className="grid grid-cols-3 gap-2 md:hidden">
            <KpiTile icon={FileText} label="Examens" value={examsCompleted} hint={inProgressCount > 0 ? `${inProgressCount} en cours` : undefined} grad="from-emerald-500 to-teal-500" compact />
            <KpiTile icon={Zap} label="Questions" value={questionsAnswered} grad="from-amber-500 to-orange-500" compact />
            <KpiTile icon={Award} label="Moyenne" value={`${Math.round(avgScore)}%`} grad="from-violet-500 to-fuchsia-500" compact />
          </div>

          {/* Row 2: 3 mode cards */}
          <div className="grid grid-cols-3 gap-2.5 sm:gap-3">
            <ModeCard
              onClick={() => navigate(hasPlan ? '/coaching/plan' : '/coaching/diagnostic')}
              icon={GraduationCap}
              title="Coaching"
              subtitle="Plan personnalisé"
              grad="from-indigo-500 to-blue-600"
              footer={
                hasPlan ? (
                  <div>
                    <div className="flex items-center justify-between text-[11px] mb-1">
                      <span className="text-white/45">Progression</span>
                      <span className="font-bold text-indigo-300">{Math.round(planProgress)}%</span>
                    </div>
                    <div className="w-full bg-white/5 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-gradient-to-r from-indigo-400 to-cyan-400 h-1.5 rounded-full transition-all" style={{ width: `${planProgress}%` }} />
                    </div>
                  </div>
                ) : (
                  <span className="inline-flex items-center gap-1 text-[11px] font-medium text-indigo-300">
                    <Play className="w-3 h-3" /> Lancer le diagnostic
                  </span>
                )
              }
            />
            <ModeCard
              onClick={() => navigate('/libre')}
              icon={MessageCircle}
              title="Mode Libre"
              subtitle="Questions à l'IA"
              grad="from-cyan-500 to-blue-600"
              footer={
                <span className="inline-flex items-center gap-1 text-[11px] font-medium text-cyan-300">
                  <Play className="w-3 h-3" /> Commencer
                </span>
              }
            />
            <ModeCard
              onClick={() => navigate('/exam')}
              icon={Trophy}
              title="Examens réels"
              subtitle="60 sujets BAC"
              grad="from-amber-500 to-rose-500"
              footer={
                <span className="inline-flex items-center gap-1 text-[11px] font-medium text-amber-300">
                  <Play className="w-3 h-3" /> S'entraîner
                </span>
              }
            />
          </div>

          {/* Row 3: Today + Priorités */}
          <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-3 min-h-0">
            {/* Today's sessions */}
            <Panel
              icon={<Calendar className="w-4 h-4 text-indigo-300" />}
              title="Aujourd'hui"
              badge={todaySessions.length > 0 ? `${todaySessions.length} session${todaySessions.length > 1 ? 's' : ''}` : undefined}
              badgeColor="bg-indigo-500/20 text-indigo-200"
            >
              {hasPlan && todaySessions.length > 0 ? (
                todaySessions.map((session: any) => (
                  <div key={session.id} className="flex items-center gap-2.5 p-2.5 rounded-xl bg-white/[.03] hover:bg-white/[.06] transition-colors group">
                    <div className={`w-1 h-9 rounded-full ${session.priority === 'high' ? 'bg-rose-400' : session.priority === 'medium' ? 'bg-amber-400' : 'bg-emerald-400'}`} />
                    <div className="flex-1 min-w-0">
                      <p className="text-[12px] font-semibold text-white truncate">{session.subjects?.name_fr || 'Matière'}</p>
                      <p className="text-[10px] text-white/45 truncate">Ch.{session.chapters?.chapter_number} — {session.chapters?.title_fr}</p>
                    </div>
                    <span className="text-[10px] text-white/40 shrink-0">{session.scheduled_time?.split('-')[0]}</span>
                    <button
                      onClick={(e) => { e.stopPropagation(); navigate(`/session/${session.chapter_id}`); }}
                      className="w-7 h-7 rounded-lg bg-gradient-to-r from-indigo-500 to-cyan-500 text-white flex items-center justify-center hover:shadow-lg hover:shadow-indigo-500/40 transition-all shrink-0"
                    >
                      <Play className="w-3 h-3" />
                    </button>
                  </div>
                ))
              ) : (
                <EmptyState
                  icon={<Star className="w-8 h-8 text-amber-300/70 mb-2" />}
                  title={hasPlan ? "Aucune session aujourd'hui" : 'Pas encore de programme'}
                  cta={hasPlan ? 'Voir le calendrier' : 'Lancer le diagnostic'}
                  onCta={() => navigate(hasPlan ? '/coaching/plan' : '/coaching/diagnostic')}
                />
              )}
            </Panel>

            {/* Priorités de révision */}
            <Panel
              icon={<Target className="w-4 h-4 text-rose-300" />}
              title="Priorités de révision"
              badge={topLacunes.length > 0 ? `${totalLacunes} point${totalLacunes > 1 ? 's' : ''} faible${totalLacunes > 1 ? 's' : ''}` : undefined}
              badgeColor="bg-rose-500/20 text-rose-200"
            >
              {topLacunes.length > 0 ? topLacunes.map((lac, i) => {
                const subjectDisplay = CANONICAL_TO_DISPLAY[lac.subject] || lac.subject;
                const accent = SUBJECT_ACCENT[subjectDisplay] || 'from-white/40 to-white/30';
                const pri = PRIORITY_META[lac.priority] || PRIORITY_META.moyenne;
                return (
                  <button
                    key={`${lac.subject}-${lac.topic}-${i}`}
                    onClick={() => navigate(hasPlan ? '/coaching/plan' : '/coaching/diagnostic')}
                    className="w-full group flex items-center gap-2.5 p-2.5 rounded-xl bg-white/[.02] hover:bg-white/[.06] transition-all text-left border border-transparent hover:border-white/10"
                  >
                    <div className={`w-1 h-10 rounded-full bg-gradient-to-b ${accent} shrink-0`} />
                    <div className="flex-1 min-w-0">
                      <p className="text-[12px] font-semibold text-white truncate">{lac.topic}</p>
                      <div className="flex items-center gap-1.5 mt-0.5">
                        <span className="text-[10px] text-white/45 truncate">{subjectDisplay}</span>
                        <span className="text-white/20">·</span>
                        <span className={`text-[9px] font-bold uppercase tracking-wider ${pri.text}`}>{pri.label}</span>
                        {typeof lac.score === 'number' && (
                          <>
                            <span className="text-white/20">·</span>
                            <span className="text-[10px] font-semibold text-white/55 tabular-nums">{Math.round(lac.score)}%</span>
                          </>
                        )}
                      </div>
                    </div>
                    <ChevronRight className="w-4 h-4 text-white/30 group-hover:text-rose-300 transition-colors shrink-0" />
                  </button>
                );
              }) : (
                <EmptyState
                  icon={
                    <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-rose-500/20 to-amber-500/20 flex items-center justify-center mb-2 border border-white/5">
                      <Target className="w-6 h-6 text-rose-300" />
                    </div>
                  }
                  title="Pas encore de données"
                  hint={hasPlan ? 'Réponds à quelques exercices pour détecter tes priorités.' : 'Lance le diagnostic pour découvrir tes points à travailler.'}
                  cta={hasPlan ? 'Faire un examen' : 'Lancer le diagnostic'}
                  onCta={() => navigate(hasPlan ? '/exam' : '/coaching/diagnostic')}
                />
              )}
            </Panel>
          </div>
        </main>

        {shareOpen && (
          <ShareModal
            studentName={student?.full_name || 'Étudiant'}
            daysRemaining={countdown?.days_remaining}
            onClose={() => setShareOpen(false)}
          />
        )}
      </div>
    </MoalimShell>
  );
}

// ──────────────────────────────────────────────────────────────
// Reusable building blocks
// ──────────────────────────────────────────────────────────────
function KpiTile({ icon: Icon, label, value, hint, grad, compact = false }: {
  icon: any; label: string; value: number | string; hint?: string; grad: string; compact?: boolean;
}) {
  return (
    <div className={`relative rounded-xl bg-gradient-to-br ${grad} text-white overflow-hidden ${compact ? 'p-2 text-center' : 'p-2.5'}`}>
      <div className="absolute -top-4 -right-4 w-16 h-16 rounded-full bg-white/15 blur-xl" />
      <div className="relative">
        {!compact && <Icon className="w-3.5 h-3.5 opacity-80 mb-1" />}
        <span className={`font-black leading-none block ${compact ? 'text-lg' : 'text-xl'}`}>{value}</span>
        <span className="text-[9px] font-bold uppercase opacity-85 tracking-wider">{label}</span>
        {hint && <span className="text-[8px] font-bold opacity-80 block">{hint}</span>}
      </div>
    </div>
  );
}

function ModeCard({ icon: Icon, title, subtitle, grad, footer, onClick }: {
  icon: any; title: string; subtitle: string; grad: string; footer: React.ReactNode; onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="tilt-card group text-left glass rounded-2xl p-3 sm:p-4 hover:bg-white/[.06] transition-all relative overflow-hidden"
    >
      <div className={`absolute -top-8 -right-8 w-24 h-24 rounded-full bg-gradient-to-br ${grad} blur-2xl opacity-30 group-hover:opacity-50 transition-opacity`} />
      <div className="relative z-10">
        <div className={`w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-gradient-to-br ${grad} flex items-center justify-center mb-2 shadow-lg group-hover:scale-110 transition-transform`}>
          <Icon className="w-5 h-5 text-white" />
        </div>
        <h3 className="text-sm font-bold text-white">{title}</h3>
        <p className="text-[11px] text-white/45 mt-0.5 line-clamp-1">{subtitle}</p>
        <div className="mt-2">{footer}</div>
      </div>
    </button>
  );
}

function Panel({ icon, title, badge, badgeColor, children }: {
  icon: React.ReactNode; title: string; badge?: string; badgeColor?: string; children: React.ReactNode;
}) {
  return (
    <div className="glass rounded-2xl overflow-hidden flex flex-col min-h-0">
      <div className="flex items-center gap-2 px-4 py-2.5 border-b border-white/5">
        {icon}
        <h3 className="text-sm font-bold text-white">{title}</h3>
        {badge && (
          <span className={`ml-auto text-[10px] font-bold px-2 py-0.5 rounded-full ${badgeColor || 'bg-white/10 text-white/70'}`}>
            {badge}
          </span>
        )}
      </div>
      <div className="flex-1 overflow-y-auto moalim-scroll p-2 space-y-1.5">
        {children}
      </div>
    </div>
  );
}

function EmptyState({ icon, title, hint, cta, onCta }: {
  icon: React.ReactNode; title: string; hint?: string; cta?: string; onCta?: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center py-6 px-4">
      {icon}
      <p className="text-sm font-semibold text-white/65">{title}</p>
      {hint && <p className="text-[11px] text-white/40 mt-1 max-w-[240px]">{hint}</p>}
      {cta && onCta && (
        <button
          onClick={onCta}
          className="mt-3 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-indigo-500 to-cyan-500 text-white text-[11px] font-semibold hover:shadow-lg hover:shadow-indigo-500/40 transition-all"
        >
          {cta} <ChevronRight className="w-3 h-3" />
        </button>
      )}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
//   ShareModal — version dark theme
// ═══════════════════════════════════════════════════════════════
function ShareModal({
  studentName, daysRemaining, onClose,
}: {
  studentName: string;
  daysRemaining?: number;
  onClose: () => void;
}) {
  const [copied, setCopied] = useState(false);
  const [tiktokNotice, setTiktokNotice] = useState(false);

  const appUrl = typeof window !== 'undefined' ? window.location.origin : 'https://moalim.online';
  const daysLine = daysRemaining ? ` — J-${daysRemaining} avant le BAC` : '';
  const shareText = `🎓 ${studentName} prépare le BAC 2026 PC BIOF avec Moalim (معلم)${daysLine} ! Rejoins-moi : ${appUrl}`;
  const shareTextShort = `🎓 ${studentName} prépare le BAC 2026 avec Moalim (معلم)${daysLine} !`;

  const encodedText = encodeURIComponent(shareText);
  const encodedShort = encodeURIComponent(shareTextShort);
  const encodedUrl = encodeURIComponent(appUrl);

  const openNative = async () => {
    if (typeof navigator !== 'undefined' && (navigator as any).share) {
      try {
        await (navigator as any).share({ title: 'Moalim — معلم', text: shareTextShort, url: appUrl });
        return true;
      } catch { /* cancelled */ }
    }
    return false;
  };

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(shareText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      window.prompt('Copie ce message :', shareText);
    }
  };

  const handleTikTok = async () => {
    try { await navigator.clipboard.writeText(shareText); } catch { /* */ }
    setTiktokNotice(true);
    setTimeout(() => setTiktokNotice(false), 4000);
  };

  const networks = [
    {
      name: 'WhatsApp',
      color: 'bg-[#25D366] hover:bg-[#1ebe5d]',
      logo: <SvgWhatsApp />,
      url: `https://wa.me/?text=${encodedText}`,
    },
    {
      name: 'X',
      color: 'bg-black hover:bg-gray-900 border border-white/10',
      logo: <SvgX />,
      url: `https://twitter.com/intent/tweet?text=${encodedShort}&url=${encodedUrl}`,
    },
    {
      name: 'Facebook',
      color: 'bg-[#1877F2] hover:bg-[#0f63d1]',
      logo: <SvgFacebook />,
      url: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}&quote=${encodedShort}`,
    },
    {
      name: 'Snapchat',
      color: 'bg-[#FFFC00] text-black hover:bg-[#e6e300]',
      logo: <SvgSnapchat />,
      url: `https://www.snapchat.com/scan?attachmentUrl=${encodedUrl}`,
    },
    {
      name: 'TikTok',
      color: 'bg-black hover:bg-gray-900 border border-white/10',
      logo: <SvgTikTok />,
      url: '#',
      custom: handleTikTok,
    },
  ];

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="glass-strong rounded-3xl w-full max-w-md overflow-hidden shadow-2xl shadow-indigo-500/20 border border-white/10 anim-fade-up"
      >
        {/* Header */}
        <div className="bg-gradient-to-br from-indigo-600 via-purple-600 to-cyan-500 px-6 py-5 text-white relative overflow-hidden">
          <div className="absolute -top-10 -right-10 w-40 h-40 rounded-full bg-white/20 blur-3xl" />
          <div className="relative flex items-start justify-between">
            <div>
              <h3 className="text-xl font-bold">Partager ma progression</h3>
              <p className="text-sm text-white/80 mt-1">
                Invite tes amis à rejoindre {studentName} sur Moalim
              </p>
            </div>
            <button
              onClick={onClose}
              className="p-1 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
            >
              <XIcon className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Preview */}
        <div className="px-6 pt-5 pb-3">
          <div className="rounded-2xl p-4 bg-white/[.04] border border-white/10">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 flex items-center justify-center">
                <GraduationCap className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="font-bold text-white">{studentName}</p>
                <p className="text-[11px] text-white/40">2BAC PC BIOF</p>
              </div>
            </div>
            <p className="text-sm text-white/75 leading-snug">
              🎓 Je prépare le BAC 2026 PC BIOF avec <span className="font-brand font-semibold">معلم</span>
              {daysRemaining && (
                <> — <span className="font-semibold text-rose-300">J-{daysRemaining}</span></>
              )}
              {' '}!
            </p>
          </div>
        </div>

        {/* Native share */}
        <div className="px-6 pb-2">
          <button
            onClick={async () => {
              const ok = await openNative();
              if (ok) onClose();
            }}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 border border-white/10 text-white text-sm font-medium transition-colors"
          >
            <Share2 className="w-4 h-4" /> Partage rapide
          </button>
        </div>

        {/* Networks */}
        <div className="px-6 py-4">
          <p className="text-xs font-semibold text-white/40 uppercase tracking-widest mb-3">Ou choisis un réseau</p>
          <div className="grid grid-cols-5 gap-2">
            {networks.map((net) =>
              net.custom ? (
                <button
                  key={net.name}
                  onClick={net.custom}
                  className={`flex flex-col items-center gap-1.5 p-2.5 rounded-xl ${net.color} text-white transition-all hover:shadow-lg hover:scale-105`}
                  title={net.name}
                >
                  {net.logo}
                  <span className="text-[10px] font-medium">{net.name}</span>
                </button>
              ) : (
                <a
                  key={net.name}
                  href={net.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`flex flex-col items-center gap-1.5 p-2.5 rounded-xl ${net.color} text-white transition-all hover:shadow-lg hover:scale-105`}
                  title={net.name}
                >
                  {net.logo}
                  <span className="text-[10px] font-medium">{net.name}</span>
                </a>
              ),
            )}
          </div>
          {tiktokNotice && (
            <p className="mt-3 text-[11px] text-amber-200 bg-amber-500/10 border border-amber-400/30 rounded-lg px-3 py-2 flex items-center gap-2">
              <Check className="w-3.5 h-3.5 flex-shrink-0" />
              Texte copié ! Ouvre l'app TikTok et colle-le dans ta publication.
            </p>
          )}
        </div>

        {/* Copy link */}
        <div className="px-6 pb-6">
          <button
            onClick={copyLink}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl border border-white/10 bg-white/[.03] text-sm font-medium text-white/80 hover:bg-white/[.07] transition-colors"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4 text-emerald-400" />
                <span className="text-emerald-300">Copié !</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" /> Copier le message
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Social SVG icons ─────────────────────────────────────────
function SvgWhatsApp() {
  return (
    <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.304-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
    </svg>
  );
}
function SvgX() {
  return (
    <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
    </svg>
  );
}
function SvgFacebook() {
  return (
    <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
      <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
    </svg>
  );
}
function SvgSnapchat() {
  return (
    <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
      <path d="M12.166 23.445c-.081 0-.16-.003-.24-.009-.062.005-.125.007-.187.007-1.414 0-2.331-.669-3.141-1.258-.582-.424-1.132-.824-1.771-.927-.312-.05-.624-.075-.931-.075-.551 0-.986.082-1.304.142-.195.036-.364.068-.496.068-.141 0-.324-.03-.398-.283-.077-.26-.136-.51-.19-.732-.136-.562-.234-.906-.466-.942-2.51-.388-3.105-.943-3.238-1.335-.024-.07-.038-.14-.042-.213-.008-.185.112-.347.295-.376 2.49-.412 3.606-2.997 3.653-3.104.014-.032.028-.065.04-.097.11-.299.134-.563.07-.783-.124-.417-.666-.606-1.021-.73-.082-.029-.158-.056-.22-.082-.29-.116-1.552-.682-1.3-1.537.186-.63.955-.48 1.3-.33.377.164.72.248 1.02.248.354 0 .528-.117.57-.151-.015-.276-.033-.564-.052-.877-.144-2.309-.323-5.186 1.4-7.12 1.554-1.745 3.54-2.24 4.953-2.24.183 0 .367.008.546.022.1.008.194.017.28.017.08 0 .15-.007.219-.017.168-.013.343-.022.52-.022 1.406 0 3.39.495 4.944 2.24 1.724 1.934 1.545 4.81 1.4 7.12-.018.313-.037.6-.051.877.043.033.21.146.524.152.303-.005.636-.087.99-.248.194-.085.456-.18.73-.18.184 0 .355.037.51.105l.01.004c.22.08.44.223.47.425.036.212-.08.434-.371.653-.125.093-.3.186-.493.28-.36.13-.902.323-1.025.73-.064.22-.042.483.07.782.012.032.025.065.04.097.047.107 1.164 2.692 3.653 3.104.183.03.303.19.295.376-.005.074-.02.145-.04.215-.133.388-.728.944-3.238 1.333-.226.035-.326.32-.466.946-.054.22-.113.466-.188.726-.055.186-.174.276-.369.276h-.027c-.12 0-.293-.025-.498-.065-.381-.073-.805-.138-1.304-.138-.305 0-.617.025-.93.075-.64.103-1.189.503-1.771.927-.811.592-1.728 1.261-3.142 1.261z" />
    </svg>
  );
}
function SvgTikTok() {
  return (
    <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
      <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64 2.93 2.93 0 01.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005.8 20.1a6.34 6.34 0 0010.86-4.43V8.73a8.16 8.16 0 004.77 1.52V6.8a4.85 4.85 0 01-1.84-.11z" />
    </svg>
  );
}
