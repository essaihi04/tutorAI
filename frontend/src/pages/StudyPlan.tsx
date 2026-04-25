import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getStudyPlan, getTodaySchedule, getAllSessions, regeneratePlan, completeSession as apiCompleteSession, getExamCountdown, getProgress } from '../services/api';
import { useCoachingStore } from '../stores/coachingStore';
import { ArrowLeft, Clock, CheckCircle, Play, Timer, BookOpen, TrendingUp, Loader2, GraduationCap, RefreshCw, Target, FileText, ChevronLeft, ChevronRight, X as XIcon, CalendarDays } from 'lucide-react';
import MobileBottomNav from '../components/MobileBottomNav';

// ════════════════════════════════════════════════════════════════
// Calendar helpers
// ════════════════════════════════════════════════════════════════
const FRENCH_MONTHS = [
  'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
];
const FRENCH_WEEKDAYS_SHORT = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];

const toISODateLocal = (d: Date): string => {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
};

// Hash subject name to a consistent hue for color-coding
const subjectHue = (name: string): number => {
  if (!name) return 210;
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) % 360;
  return h;
};

// ════════════════════════════════════════════════════════════════
// Calendar grid component
// ════════════════════════════════════════════════════════════════
interface CalendarViewProps {
  month: Date;
  setMonth: (d: Date) => void;
  sessionsByDate: Record<string, any[]>;
  onSelectDay: (date: string) => void;
  examDate?: string;
}

const CalendarView: React.FC<CalendarViewProps> = ({ month, setMonth, sessionsByDate, onSelectDay, examDate }) => {
  const today = new Date();
  const todayISO = toISODateLocal(today);

  const year = month.getFullYear();
  const monthIdx = month.getMonth();

  const firstOfMonth = new Date(year, monthIdx, 1);
  const jsWeekday = firstOfMonth.getDay();
  const offset = (jsWeekday + 6) % 7;
  const daysInMonth = new Date(year, monthIdx + 1, 0).getDate();

  const cells: Array<{ date: Date | null; iso: string | null }> = [];
  for (let i = 0; i < offset; i++) cells.push({ date: null, iso: null });
  for (let d = 1; d <= daysInMonth; d++) {
    const date = new Date(year, monthIdx, d);
    cells.push({ date, iso: toISODateLocal(date) });
  }
  while (cells.length % 7 !== 0) cells.push({ date: null, iso: null });

  const examISO = examDate ? examDate.split('T')[0] : null;

  return (
    <div className="glass rounded-2xl overflow-hidden">
      {/* Compact header */}
      <div className="flex items-center justify-between px-3 py-2.5 border-b border-white/5 bg-gradient-to-r from-indigo-600/30 via-purple-600/20 to-cyan-600/20">
        <button
          onClick={() => setMonth(new Date(year, monthIdx - 1, 1))}
          className="w-7 h-7 rounded-lg bg-white/5 hover:bg-white/10 text-white/70 flex items-center justify-center transition-all"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>
        <button
          onClick={() => setMonth(new Date())}
          className="text-sm font-bold tracking-tight text-white hover:bg-white/5 px-2 py-0.5 rounded-lg transition-all"
        >
          {FRENCH_MONTHS[monthIdx]} {year}
        </button>
        <button
          onClick={() => setMonth(new Date(year, monthIdx + 1, 1))}
          className="w-7 h-7 rounded-lg bg-white/5 hover:bg-white/10 text-white/70 flex items-center justify-center transition-all"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      {/* Weekday row */}
      <div className="grid grid-cols-7 border-b border-white/5">
        {FRENCH_WEEKDAYS_SHORT.map((d) => (
          <div key={d} className="py-1.5 text-center text-[10px] font-bold text-white/40 uppercase">
            {d.charAt(0)}
          </div>
        ))}
      </div>

      {/* Day grid — compact */}
      <div className="grid grid-cols-7">
        {cells.map((cell, i) => {
          if (!cell.date || !cell.iso) {
            return <div key={i} className="h-9" />;
          }

          const daySessions = sessionsByDate[cell.iso] || [];
          const isToday = cell.iso === todayISO;
          const isPast = cell.iso < todayISO;
          const isExam = cell.iso === examISO;
          const totalSessions = daySessions.length;
          const completed = daySessions.filter((s: any) => s.status === 'completed').length;
          const allDone = totalSessions > 0 && completed === totalSessions;

          return (
            <button
              key={i}
              onClick={() => totalSessions > 0 && onSelectDay(cell.iso!)}
              disabled={totalSessions === 0}
              className={`relative h-9 flex flex-col items-center justify-center transition-all ${
                isExam
                  ? 'bg-rose-500/10 ring-1 ring-rose-400/30 hover:bg-rose-500/20'
                  : isToday
                  ? 'bg-indigo-500/15 ring-1 ring-indigo-400/40'
                  : totalSessions > 0
                  ? 'hover:bg-white/[.06] cursor-pointer'
                  : ''
              }`}
            >
              <span
                className={`text-xs font-semibold leading-none ${
                  isToday
                    ? 'w-6 h-6 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-400 text-white flex items-center justify-center shadow-lg shadow-indigo-500/30'
                    : isExam
                    ? 'w-6 h-6 rounded-full bg-gradient-to-br from-rose-500 to-red-600 text-white flex items-center justify-center shadow-lg shadow-rose-500/30'
                    : isPast
                    ? 'text-white/25'
                    : totalSessions > 0
                    ? 'text-white'
                    : 'text-white/40'
                }`}
              >
                {cell.date.getDate()}
              </span>
              {/* Session dots */}
              {totalSessions > 0 && (
                <div className="flex items-center gap-0.5 mt-0.5">
                  {daySessions.slice(0, 3).map((s: any, idx: number) => {
                    const hue = subjectHue(s.subjects?.name_fr || '');
                    const isDone = s.status === 'completed';
                    return (
                      <div
                        key={idx}
                        className="w-1.5 h-1.5 rounded-full"
                        style={{
                          background: isDone
                            ? '#10b981'
                            : `hsl(${hue}, 70%, 55%)`,
                        }}
                      />
                    );
                  })}
                  {totalSessions > 3 && (
                    <span className="text-[7px] font-bold text-white/40">+</span>
                  )}
                </div>
              )}
              {allDone && !isExam && (
                <div className="absolute top-0.5 right-0.5">
                  <CheckCircle className="w-2.5 h-2.5 text-emerald-400" />
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════
// Day detail modal
// ════════════════════════════════════════════════════════════════
interface DayDetailModalProps {
  dayISO: string;
  sessions: any[];
  onClose: () => void;
  onStartSession: (chapterId: string) => void;
  onCompleteSession: (sessionId: string) => void;
  completing: string | null;
  sessionTypeColor: (t: string) => string;
  sessionTypeIcon: (t: string) => React.ReactNode;
  sessionTypeLabel: (t: string) => string;
}

const DayDetailModal: React.FC<DayDetailModalProps> = ({
  dayISO,
  sessions,
  onClose,
  onStartSession,
  onCompleteSession,
  completing,
  sessionTypeColor,
  sessionTypeIcon,
  sessionTypeLabel,
}) => {
  const date = new Date(dayISO + 'T00:00:00');
  const weekday = date.toLocaleDateString('fr-FR', { weekday: 'long' });
  const dayNum = date.getDate();
  const monthName = FRENCH_MONTHS[date.getMonth()];

  const todayISO = toISODateLocal(new Date());
  const isToday = dayISO === todayISO;

  const totalMin = sessions.reduce((a, s) => a + (s.duration_minutes || 0), 0);
  const completed = sessions.filter((s) => s.status === 'completed').length;

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center p-4 animate-in fade-in duration-200">
      <div className="glass-strong rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-br from-indigo-600/40 via-purple-600/30 to-cyan-600/30 border-b border-white/10 p-6 text-white relative">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 w-9 h-9 rounded-xl bg-white/20 hover:bg-white/30 backdrop-blur flex items-center justify-center transition-all"
          >
            <XIcon className="w-5 h-5" />
          </button>
          <div className="flex items-end gap-4">
            <div className="bg-white/20 backdrop-blur rounded-2xl p-3 text-center min-w-[80px]">
              <p className="text-xs uppercase tracking-wider font-bold text-blue-100">
                {weekday.slice(0, 3)}
              </p>
              <p className="text-4xl font-black leading-none mt-1">{dayNum}</p>
              <p className="text-[10px] font-semibold text-blue-100 mt-1">
                {monthName.slice(0, 4).toUpperCase()}
              </p>
            </div>
            <div className="flex-1 pb-1">
              <p className="text-xs uppercase tracking-wider font-bold text-blue-100">
                {isToday ? "Aujourd'hui" : 'Sessions planifiées'}
              </p>
              <h3 className="text-2xl font-black capitalize mt-1">
                {weekday} {dayNum} {monthName}
              </h3>
              <div className="flex items-center gap-3 mt-2 text-xs">
                <span className="bg-white/20 backdrop-blur rounded-lg px-2.5 py-1 font-semibold">
                  {sessions.length} session{sessions.length > 1 ? 's' : ''}
                </span>
                <span className="bg-white/20 backdrop-blur rounded-lg px-2.5 py-1 font-semibold">
                  {Math.round(totalMin / 60 * 10) / 10}h
                </span>
                <span className="bg-white/20 backdrop-blur rounded-lg px-2.5 py-1 font-semibold">
                  {completed}/{sessions.length} terminées
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Sessions list */}
        <div className="flex-1 overflow-y-auto p-5 space-y-3 bg-[#0a0a1f]/60">
          {sessions.map((s: any, idx: number) => {
            const name = s.subjects?.name_fr || 'Matière';
            const hue = subjectHue(name);
            const isDone = s.status === 'completed';
            const canStart = s.is_unlocked && !isDone;

            return (
              <div
                key={s.id || idx}
                className={`glass rounded-2xl p-4 transition-all hover:bg-white/[.06] ${
                  isDone ? 'ring-1 ring-emerald-400/30 bg-emerald-500/5' : ''
                }`}
                style={!isDone ? { borderLeftColor: `hsl(${hue}, 70%, 60%)`, borderLeftWidth: '4px' } : {}}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1.5">
                      <span
                        className="text-xs font-bold px-2 py-0.5 rounded-full border"
                        style={{
                          background: `hsl(${hue}, 70%, 50%, 0.15)`,
                          color: `hsl(${hue}, 80%, 75%)`,
                          borderColor: `hsl(${hue}, 70%, 50%, 0.3)`,
                        }}
                      >
                        {name}
                      </span>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1 ${sessionTypeColor(
                          s.session_type || 'cours'
                        )}`}
                      >
                        {sessionTypeIcon(s.session_type || 'cours')}
                        {sessionTypeLabel(s.session_type || 'cours')}
                      </span>
                    </div>
                    <h4 className={`font-bold text-white text-sm mb-1 ${isDone ? 'line-through opacity-60' : ''}`}>
                      Ch.{s.chapters?.chapter_number} — {s.chapters?.title_fr || 'Chapitre'}
                    </h4>
                    <div className="flex items-center gap-3 text-xs text-white/55">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" /> {s.scheduled_time}
                      </span>
                      <span className="flex items-center gap-1">
                        <Timer className="w-3 h-3" /> {s.duration_minutes} min
                      </span>
                      {s.priority === 'high' && (
                        <span className="text-rose-300 font-bold">⚡ Prioritaire</span>
                      )}
                    </div>
                  </div>

                  <div className="flex flex-col gap-1.5">
                    {isDone ? (
                      <span className="flex items-center gap-1 text-emerald-300 font-bold text-xs bg-emerald-500/15 border border-emerald-400/30 px-3 py-1.5 rounded-lg">
                        <CheckCircle className="w-4 h-4" /> Terminé
                      </span>
                    ) : (
                      <>
                        <button
                          onClick={() => onStartSession(s.chapter_id)}
                          disabled={!canStart}
                          className={`px-3 py-1.5 text-xs font-bold rounded-lg flex items-center gap-1.5 transition-all ${
                            canStart
                              ? 'bg-gradient-to-r from-indigo-500 to-cyan-500 text-white shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50'
                              : 'bg-white/5 text-white/30 cursor-not-allowed'
                          }`}
                        >
                          <Play className="w-3 h-3" /> Commencer
                        </button>
                        <button
                          onClick={() => onCompleteSession(s.id)}
                          disabled={completing === s.id || !s.is_unlocked}
                          className="px-3 py-1.5 text-xs font-bold rounded-lg flex items-center gap-1.5 text-emerald-300 hover:bg-emerald-500/10 transition-all disabled:opacity-40"
                        >
                          {completing === s.id ? (
                            <Loader2 className="w-3 h-3 animate-spin" />
                          ) : (
                            <CheckCircle className="w-3 h-3" />
                          )}
                          Marquer fait
                        </button>
                      </>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default function StudyPlan() {
  const navigate = useNavigate();
  const { setActivePlan, setTodaySessions, setExamCountdown, setProgress } = useCoachingStore();
  
  const [plan, setPlan] = useState<any>(null);
  const [todaySessions, setTodaySessionsLocal] = useState<any[]>([]);
  const [allSessionsData, setAllSessionsData] = useState<any>(null);
  const [countdown, setCountdown] = useState<any>(null);
  const [progressData, setProgressData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState<string | null>(null);
  const [calendarMonth, setCalendarMonth] = useState<Date>(new Date());
  const [selectedDay, setSelectedDay] = useState<string | null>(null);
  const [showRegenerateDialog, setShowRegenerateDialog] = useState(false);
  const [regenerating, setRegenerating] = useState(false);

  useEffect(() => {
    loadPlanData();
  }, []);

  // Reload plan data when component receives new state (e.g., after plan generation)
  useEffect(() => {
    const state = window.history.state?.usr;
    if (state?.refresh) {
      loadPlanData();
    }
  }, [window.location.pathname]);

  const loadPlanData = async () => {
    setLoading(true);
    try {
      const [planRes, todayRes, allSessionsRes, countdownRes, progressRes] = await Promise.all([
        getStudyPlan(),
        getTodaySchedule(),
        getAllSessions(),
        getExamCountdown(),
        getProgress()
      ]);

      if (planRes.data.has_plan) {
        setPlan(planRes.data.plan);
        setActivePlan(planRes.data.plan);
      }

      setTodaySessionsLocal(todayRes.data?.sessions || []);
      setTodaySessions(todayRes.data?.sessions || []);
      setAllSessionsData(allSessionsRes.data || {});
      setCountdown(countdownRes.data || {});
      setExamCountdown(countdownRes.data || {});
      setProgressData(progressRes.data || {});
      setProgress(progressRes.data || {});

    } catch (e: any) {
      console.error('Failed to load plan data:', e);
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteSession = async (sessionId: string) => {
    setCompleting(sessionId);
    try {
      await apiCompleteSession(sessionId);
      await loadPlanData(); // Reload to update progress
    } catch (e) {
      console.error('Failed to complete session:', e);
    } finally {
      setCompleting(null);
    }
  };

  const startCoachingSession = (chapterId: string) => {
    console.log('[StudyPlan] Starting session with chapterId:', chapterId);
    if (!chapterId) {
      alert('Erreur: Aucun chapitre associé à cette session. Veuillez régénérer le plan.');
      return;
    }
    navigate(`/session/${chapterId}`);
  };

  const handleRegeneratePlan = async () => {
    setRegenerating(true);
    setShowRegenerateDialog(false);
    try {
      await regeneratePlan();
      await new Promise(resolve => setTimeout(resolve, 500));
      await loadPlanData();
    } catch (e: any) {
      console.error('Failed to regenerate plan:', e);
      alert(e.response?.data?.detail || 'Erreur lors de la régénération du programme');
    } finally {
      setRegenerating(false);
    }
  };

  const getStudentLevel = () => {
    if (!plan?.diagnostic_scores) return 'Intermédiaire';
    const scores = Object.values(plan.diagnostic_scores) as number[];
    const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
    if (avg < 40) return 'Débutant';
    if (avg < 65) return 'Intermédiaire';
    return 'Avancé';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#070718]">
        <Loader2 className="w-8 h-8 text-indigo-400 animate-spin" />
      </div>
    );
  }

  if (!plan) {
    return (
      <div className="min-h-screen bg-[#070718] text-white flex items-center justify-center p-6">
        <div className="glass rounded-3xl p-10 text-center max-w-md">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 border border-white/5 mx-auto mb-4 flex items-center justify-center">
            <BookOpen className="w-8 h-8 text-indigo-300" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">Pas encore de programme</h2>
          <p className="text-white/55 mb-6">Fais d'abord le diagnostic pour générer ton programme personnalisé.</p>
          <button
            onClick={() => navigate('/coaching/diagnostic')}
            className="px-6 py-3 bg-gradient-to-r from-indigo-500 to-cyan-500 text-white rounded-xl font-bold shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 transition-all"
          >
            Commencer le Diagnostic
          </button>
        </div>
      </div>
    );
  }

  const overallProgress = plan.progress_percentage || progressData?.overall_progress || 0;

  const sessionTypeLabel = (t: string) => {
    switch (t) {
      case 'cours': return 'Apprentissage';
      case 'revision': return 'Révision';
      case 'lacunes': return 'Lacunes';
      case 'examen_blanc': return 'Examen Blanc';
      default: return 'Cours';
    }
  };
  const sessionTypeColor = (t: string) => {
    switch (t) {
      case 'cours': return 'bg-indigo-500/15 text-indigo-200 border border-indigo-400/30';
      case 'revision': return 'bg-purple-500/15 text-purple-200 border border-purple-400/30';
      case 'lacunes': return 'bg-orange-500/15 text-orange-200 border border-orange-400/30';
      case 'examen_blanc': return 'bg-rose-500/15 text-rose-200 border border-rose-400/30';
      default: return 'bg-white/5 text-white/60 border border-white/10';
    }
  };
  const sessionTypeIcon = (t: string) => {
    switch (t) {
      case 'cours': return <GraduationCap className="w-3 h-3" />;
      case 'revision': return <RefreshCw className="w-3 h-3" />;
      case 'lacunes': return <Target className="w-3 h-3" />;
      case 'examen_blanc': return <FileText className="w-3 h-3" />;
      default: return <BookOpen className="w-3 h-3" />;
    }
  };

  const todayISO = toISODateLocal(new Date());
  const todayTotalMin = todaySessions.reduce((a: number, s: any) => a + (s.duration_minutes || 0), 0);
  const todayCompleted = todaySessions.filter((s: any) => s.status === 'completed').length;

  return (
    <div className="h-screen flex flex-col bg-[#070718] text-white overflow-hidden relative">
      {/* Decorative orbs */}
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute top-0 left-1/3 w-[600px] h-[600px] rounded-full bg-indigo-600/15 blur-[140px] anim-pulse-glow" />
        <div className="absolute bottom-0 right-[10%] w-[500px] h-[500px] rounded-full bg-cyan-500/10 blur-[140px] anim-pulse-glow" style={{ animationDelay: '2s' }} />
      </div>
      {/* ── Slim header ── */}
      <header className="relative z-20 backdrop-blur-2xl bg-[#070718]/70 border-b border-white/5 sticky top-0">
        <div className="max-w-7xl mx-auto px-4 py-2 flex items-center gap-3">
          <button
            onClick={() => navigate('/dashboard')}
            className="p-1.5 -ml-1 rounded-lg hover:bg-white/5 text-white/60 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div className="min-w-0 flex-1">
            <h1 className="text-base font-bold text-white font-brand truncate">Mon Programme</h1>
            <p className="text-[10px] text-white/50">Sciences Physiques BIOF — BAC 2026</p>
          </div>
          <button
            onClick={() => setShowRegenerateDialog(true)}
            disabled={regenerating}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-indigo-500 to-cyan-500 text-white text-xs font-bold shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 transition-all disabled:opacity-50"
            title="Régénérer le programme"
          >
            {regenerating ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <RefreshCw className="w-3.5 h-3.5" />}
            <span className="hidden sm:inline">Régénérer</span>
          </button>
        </div>

        {/* ── Compact stats dashboard ── */}
        <div className="max-w-7xl mx-auto px-4 pb-2.5">
          <div className="grid grid-cols-4 gap-2">
            {/* Sessions */}
            <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl p-2.5 text-white shadow-sm">
              <div className="flex items-center gap-1 mb-0.5">
                <BookOpen className="w-3 h-3 opacity-80" />
                <span className="text-[9px] font-bold uppercase tracking-wider opacity-90">Sessions</span>
              </div>
              <div className="flex items-baseline gap-1">
                <span className="text-lg font-black leading-none">{plan.completed_sessions || 0}</span>
                <span className="text-[11px] font-bold opacity-70">/{plan.total_sessions || 0}</span>
              </div>
            </div>

            {/* Heures */}
            <div className="bg-gradient-to-br from-amber-500 to-orange-600 rounded-xl p-2.5 text-white shadow-sm">
              <div className="flex items-center gap-1 mb-0.5">
                <Timer className="w-3 h-3 opacity-80" />
                <span className="text-[9px] font-bold uppercase tracking-wider opacity-90">Heures</span>
              </div>
              <div className="flex items-baseline gap-1">
                <span className="text-lg font-black leading-none">
                  {Math.round(((allSessionsData?.completed_duration_minutes || 0)) / 60)}
                </span>
                <span className="text-[11px] font-bold opacity-70">
                  /{Math.round((allSessionsData?.total_duration_minutes || 0) / 60)}h
                </span>
              </div>
            </div>

            {/* Progression */}
            <div className="bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl p-2.5 text-white shadow-sm">
              <div className="flex items-center gap-1 mb-0.5">
                <TrendingUp className="w-3 h-3 opacity-80" />
                <span className="text-[9px] font-bold uppercase tracking-wider opacity-90">Progression</span>
              </div>
              <div className="flex items-baseline gap-1">
                <span className="text-lg font-black leading-none">{Math.round(overallProgress)}</span>
                <span className="text-[11px] font-bold opacity-70">%</span>
              </div>
            </div>

            {/* BAC countdown */}
            <div className="bg-gradient-to-br from-rose-500 to-red-600 rounded-xl p-2.5 text-white shadow-sm">
              <div className="flex items-center gap-1 mb-0.5">
                <Target className="w-3 h-3 opacity-80" />
                <span className="text-[9px] font-bold uppercase tracking-wider opacity-90">BAC 2026</span>
              </div>
              <div className="flex items-baseline gap-1">
                <span className="text-lg font-black leading-none">{countdown?.days_remaining || 0}</span>
                <span className="text-[11px] font-bold opacity-70">jours</span>
              </div>
            </div>
          </div>

          {/* Inline progress bar */}
          <div className="mt-2 h-1.5 bg-white/5 border border-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-400 rounded-full transition-all duration-500"
              style={{ width: `${Math.min(overallProgress, 100)}%` }}
            />
          </div>
        </div>
      </header>

      {/* ── Main content: single page, no scroll ── */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-3 pb-20 lg:pb-3 flex flex-col lg:flex-row gap-3 min-h-0">
        {/* Left column: Calendar */}
        <div className="lg:w-80 xl:w-96 shrink-0 flex flex-col gap-3">
          <CalendarView
            month={calendarMonth}
            setMonth={setCalendarMonth}
            sessionsByDate={allSessionsData?.sessions_by_date || {}}
            onSelectDay={setSelectedDay}
            examDate={plan?.exam_date}
          />

          {/* Legend */}
          <div className="glass rounded-xl p-2.5 text-[10px] text-white/55 space-y-1.5">
            <div className="flex items-center gap-2">
              <span className="w-4 h-4 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-400 text-white text-[9px] font-bold flex items-center justify-center shadow-lg shadow-indigo-500/30">J</span>
              <span>Aujourd'hui</span>
              <span className="w-4 h-4 rounded-full bg-gradient-to-br from-rose-500 to-red-600 text-white text-[9px] font-bold flex items-center justify-center ml-auto shadow-lg shadow-rose-500/30">B</span>
              <span>BAC</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-0.5">
                <div className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                <div className="w-1.5 h-1.5 rounded-full bg-amber-400" />
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              </div>
              <span>Sessions par matière</span>
              <CheckCircle className="w-3 h-3 text-emerald-400 ml-auto" />
              <span>Jour terminé</span>
            </div>
          </div>
        </div>

        {/* Right column: Today's sessions */}
        <section className="flex-1 min-w-0 flex flex-col min-h-0">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-sm font-bold text-white flex items-center gap-1.5">
              <CalendarDays className="w-4 h-4 text-indigo-300" />
              Aujourd'hui
              {todaySessions.length > 0 && (
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-200 border border-indigo-400/30">
                  {todayCompleted}/{todaySessions.length}
                </span>
              )}
            </h2>
            {todayTotalMin > 0 && (
              <span className="text-[10px] font-semibold text-white/50">
                ~{Math.round(todayTotalMin / 60 * 10) / 10}h prévues
              </span>
            )}
          </div>

          {/* Session cards — scrollable if many */}
          <div className="flex-1 overflow-y-auto space-y-2 pr-1">
            {todaySessions.length === 0 ? (
              <div className="glass rounded-2xl p-6 text-center">
                <CheckCircle className="w-10 h-10 text-emerald-400 mx-auto mb-2" />
                <p className="text-sm font-bold text-white">Pas de sessions aujourd'hui</p>
                <p className="text-xs text-white/50 mt-1">Profites-en pour te reposer !</p>
              </div>
            ) : (
              todaySessions.map((session: any) => {
                const name = session.subjects?.name_fr || 'Matière';
                const hue = subjectHue(name);
                const isDone = session.status === 'completed';
                const canStart = session.is_unlocked && !isDone;

                return (
                  <div
                    key={session.id}
                    className={`glass rounded-xl p-3 transition-all hover:bg-white/[.06] ${
                      isDone ? 'ring-1 ring-emerald-400/30 bg-emerald-500/5' : ''
                    }`}
                    style={!isDone ? { borderLeftColor: `hsl(${hue}, 70%, 60%)`, borderLeftWidth: '4px' } : {}}
                  >
                    <div className="flex items-center gap-3">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-1.5 mb-1">
                          <span
                            className="text-[10px] font-bold px-1.5 py-0.5 rounded-full border"
                            style={{
                              background: `hsl(${hue}, 70%, 50%, 0.15)`,
                              color: `hsl(${hue}, 80%, 75%)`,
                              borderColor: `hsl(${hue}, 70%, 50%, 0.3)`,
                            }}
                          >
                            {name}
                          </span>
                          <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full flex items-center gap-0.5 ${sessionTypeColor(session.session_type || 'cours')}`}>
                            {sessionTypeIcon(session.session_type || 'cours')}
                            {sessionTypeLabel(session.session_type || 'cours')}
                          </span>
                          {session.priority === 'high' && (
                            <span className="text-[9px] font-bold text-rose-300">⚡</span>
                          )}
                        </div>
                        <p className={`text-sm font-bold text-white truncate ${isDone ? 'line-through opacity-50' : ''}`}>
                          Ch.{session.chapters?.chapter_number} — {session.chapters?.title_fr || 'Chapitre'}
                        </p>
                        <div className="flex items-center gap-2 mt-0.5 text-[10px] text-white/50">
                          <span className="flex items-center gap-0.5">
                            <Clock className="w-2.5 h-2.5" /> {session.scheduled_time}
                          </span>
                          <span>{session.duration_minutes} min</span>
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex items-center gap-1.5 shrink-0">
                        {isDone ? (
                          <span className="flex items-center gap-1 text-emerald-300 font-bold text-[10px] bg-emerald-500/15 border border-emerald-400/30 px-2 py-1.5 rounded-lg">
                            <CheckCircle className="w-3.5 h-3.5" /> Fait
                          </span>
                        ) : !session.is_unlocked ? (
                          <span className="flex items-center gap-1 text-amber-300 font-bold text-[10px] bg-amber-500/15 border border-amber-400/30 px-2 py-1.5 rounded-lg">
                            🔒 Verrouillé
                          </span>
                        ) : (
                          <>
                            <button
                              onClick={() => startCoachingSession(session.chapter_id)}
                              disabled={!canStart}
                              className={`px-2.5 py-1.5 text-[10px] font-bold rounded-lg flex items-center gap-1 transition-all ${
                                canStart
                                  ? 'bg-gradient-to-r from-indigo-500 to-cyan-500 text-white shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50'
                                  : 'bg-white/5 text-white/30 cursor-not-allowed'
                              }`}
                            >
                              <Play className="w-3 h-3" /> Go
                            </button>
                            <button
                              onClick={() => handleCompleteSession(session.id)}
                              disabled={completing === session.id}
                              className="p-1.5 rounded-lg text-emerald-300 hover:bg-emerald-500/10 transition-all disabled:opacity-30"
                              title="Marquer terminé"
                            >
                              {completing === session.id ? (
                                <Loader2 className="w-4 h-4 animate-spin" />
                              ) : (
                                <CheckCircle className="w-4 h-4" />
                              )}
                            </button>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })
            )}

            {todaySessions.some((session: any) => !session.is_unlocked && session.status !== 'completed') && (
              <div className="bg-amber-500/10 border border-amber-400/30 rounded-lg p-2.5 text-[10px] text-amber-200 font-medium">
                🔒 Termine la session précédente pour débloquer les suivantes.
              </div>
            )}
          </div>
        </section>
      </main>

      {/* Day detail modal */}
      {selectedDay && (
        <DayDetailModal
          dayISO={selectedDay}
          sessions={allSessionsData?.sessions_by_date?.[selectedDay] || []}
          onClose={() => setSelectedDay(null)}
          onStartSession={(chapterId) => {
            setSelectedDay(null);
            startCoachingSession(chapterId);
          }}
          onCompleteSession={handleCompleteSession}
          completing={completing}
          sessionTypeColor={sessionTypeColor}
          sessionTypeIcon={sessionTypeIcon}
          sessionTypeLabel={sessionTypeLabel}
        />
      )}

      {/* Regenerate Confirmation Dialog */}
      {showRegenerateDialog && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-md flex items-center justify-center z-50 p-4">
          <div className="glass-strong rounded-2xl shadow-2xl max-w-md w-full p-6">
            <h3 className="text-xl font-bold text-white mb-4">Régénérer le programme ?</h3>

            <div className="space-y-3 mb-6">
              <div className="glass rounded-lg p-3">
                <p className="text-sm font-medium text-white/70">Temps restant</p>
                <p className="text-2xl font-bold text-indigo-300">{countdown?.days_remaining || 0} jours</p>
              </div>

              <div className="glass rounded-lg p-3">
                <p className="text-sm font-medium text-white/70">Niveau actuel</p>
                <p className="text-2xl font-bold text-purple-300">{getStudentLevel()}</p>
              </div>

              <div className="bg-amber-500/10 border border-amber-400/30 rounded-lg p-3 text-sm text-amber-100">
                <p className="font-bold mb-1">⚠️ Attention</p>
                <p className="text-amber-100/80">Le nouveau programme remplacera l'ancien et sera optimisé selon tes derniers résultats de diagnostic et le temps restant.</p>
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setShowRegenerateDialog(false)}
                className="flex-1 px-4 py-2 border border-white/10 text-white/70 rounded-lg font-medium hover:bg-white/5 transition-colors"
              >
                Annuler
              </button>
              <button
                onClick={handleRegeneratePlan}
                className="flex-1 px-4 py-2 bg-gradient-to-r from-indigo-500 to-cyan-500 text-white rounded-lg font-bold shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 transition-all"
              >
                Confirmer
              </button>
            </div>
          </div>
        </div>
      )}
      <MobileBottomNav active="coaching" />
    </div>
  );
}
