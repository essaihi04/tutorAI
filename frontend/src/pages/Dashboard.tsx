import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getExamCountdown, getStudyPlan, getTodaySchedule, getProficiency, getMyExamStats, getMe } from '../services/api';
import { useAuthStore } from '../stores/authStore';
import {
  GraduationCap, MessageCircle, Calendar, Play, LogOut, Settings,
  FileText, Share2, X as XIcon, Copy, Check,
  Flame, Zap, Award, Star, ChevronRight, Target,
} from 'lucide-react';

const SUBJECT_ACCENT: Record<string, string> = {
  'Mathématiques': 'from-blue-500 to-indigo-600',
  'Physique':      'from-indigo-500 to-purple-600',
  'Chimie':        'from-emerald-500 to-teal-600',
  'SVT':           'from-amber-500 to-orange-600',
};

// Canonical name used by proficiency service (accent-free) → display name
const CANONICAL_TO_DISPLAY: Record<string, string> = {
  'Mathematiques': 'Mathématiques',
  'Physique': 'Physique',
  'Chimie': 'Chimie',
  'SVT': 'SVT',
};

// Priority styling for lacunes (aligned with the backend ZPD logic)
const PRIORITY_META: Record<string, { label: string; text: string }> = {
  critique: { label: 'Critique', text: 'text-rose-600' },
  haute:    { label: 'Haute',    text: 'text-amber-600' },
  moyenne:  { label: 'Moyenne',  text: 'text-slate-500' },
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
    // Backfill student record if full_name is missing (e.g. session from before /auth/me wiring)
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

      // Load coaching data + proficiency
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
        // Coaching data not available
      }
    } catch {
      // API not ready
    }
  };

  // Top priorities to revise: weakest topics ordered by urgency (already sorted by backend).
  // We take the 3 most urgent ones to keep the panel scannable.
  const { topLacunes, totalLacunes } = useMemo(() => {
    const all: any[] = (proficiency?.lacunes as any[]) || [];
    return { topLacunes: all.slice(0, 3), totalLacunes: all.length };
  }, [proficiency]);

  // Compute motivational stats
  const examsCompleted = examStats?.unique_exams_taken || 0;
  const questionsAnswered = examStats?.total_questions_answered || 0;
  const avgScore = examStats?.avg_score_pct || 0;
  const inProgressCount = examStats?.in_progress_count || 0;
  const daysRemaining = countdown?.days_remaining || 0;

  // First name extracted from full_name for a personal greeting
  const firstName = (student?.full_name || 'Étudiant').trim().split(/\s+/)[0];

  // Time-based greeting in French
  const hour = new Date().getHours();
  const timeGreeting =
    hour < 12 ? 'Bonjour' : hour < 18 ? 'Bon après-midi' : 'Bonsoir';

  // Encouragement message based on activity
  const encouragement = useMemo(() => {
    if (questionsAnswered >= 100) return { text: "Tu es un champion ! Continue comme ça !", icon: '🏆' };
    if (examsCompleted >= 5) return { text: "Excellent travail, tu progresses vite !", icon: '🚀' };
    if (questionsAnswered >= 30) return { text: "Beau rythme, chaque question te rapproche du BAC !", icon: '💪' };
    if (examsCompleted >= 1) return { text: "Super début ! Tu es sur la bonne voie !", icon: '⭐' };
    return { text: "Commence par un examen, tu vas tout déchirer !", icon: '🎯' };
  }, [examsCompleted, questionsAnswered]);

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20 overflow-hidden">
      {/* ── Slim header ── */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-20">
        <div className="max-w-7xl mx-auto px-4 py-2 flex items-center gap-3">
          <img src="/media/logo.png" alt="معلم" className="h-9 w-auto" />
          <div className="min-w-0 flex-1">
            <h1 className="text-base font-bold text-gray-800 font-brand">معلم</h1>
            <p className="text-[10px] text-gray-500">2ème BAC Sciences Physiques BIOF</p>
          </div>
          <div className="flex items-center gap-1.5">
            <button onClick={() => setShareOpen(true)} className="flex items-center gap-1 px-2.5 py-1.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg text-xs font-medium hover:shadow-md transition-all">
              <Share2 className="w-3.5 h-3.5" /><span className="hidden sm:inline">Partager</span>
            </button>
            <button onClick={() => navigate('/admin/resources')} className="p-1.5 text-gray-400 hover:bg-gray-100 rounded-lg transition-colors"><Settings className="w-4 h-4" /></button>
            <button onClick={logout} className="p-1.5 text-red-400 hover:bg-red-50 rounded-lg transition-colors"><LogOut className="w-4 h-4" /></button>
          </div>
        </div>
      </header>

      {/* ── Main content — no scroll ── */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-3 flex flex-col gap-3 min-h-0 overflow-hidden">
        
        {/* Row 1: Welcome + Countdown + Stats tiles */}
        <div className="flex items-stretch gap-3">
          {/* Welcome + encouragement */}
          <div className="flex-1 bg-gradient-to-br from-indigo-600 via-blue-600 to-purple-700 rounded-2xl p-4 text-white relative overflow-hidden">
            <div className="absolute -top-10 -right-10 w-40 h-40 rounded-full bg-white/10 blur-2xl" />
            <div className="relative">
              <p className="text-[11px] font-semibold text-white/70 uppercase tracking-wider">{timeGreeting}</p>
              <h2 className="text-xl font-black leading-tight mt-0.5">
                {firstName} <span className="inline-block animate-wave">👋</span>
              </h2>
              <div className="flex items-center gap-1.5 mt-2 bg-white/15 backdrop-blur rounded-lg px-2.5 py-1.5 w-fit">
                <span className="text-sm">{encouragement.icon}</span>
                <span className="text-[11px] font-semibold">{encouragement.text}</span>
              </div>
            </div>
          </div>

          {/* BAC Countdown */}
          {countdown && (
            <div className="w-28 shrink-0 bg-gradient-to-br from-rose-500 to-red-600 rounded-2xl p-3 text-white text-center flex flex-col items-center justify-center">
              <Flame className="w-5 h-5 opacity-80 mb-1" />
              <span className="text-3xl font-black leading-none">{daysRemaining}</span>
              <span className="text-[10px] font-bold uppercase tracking-wider opacity-80 mt-0.5">jours</span>
              <span className="text-[9px] opacity-60">avant BAC</span>
            </div>
          )}

          {/* Stats tiles */}
          <div className="hidden md:grid grid-cols-3 gap-2 shrink-0" style={{ width: '320px' }}>
            <div className="bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl p-2.5 text-white">
              <FileText className="w-3.5 h-3.5 opacity-80 mb-1" />
              <span className="text-xl font-black leading-none block">{examsCompleted}</span>
              <span className="text-[9px] font-bold uppercase opacity-80">Examens</span>
              {inProgressCount > 0 && <span className="text-[8px] font-bold text-emerald-200 block">{inProgressCount} en cours</span>}
            </div>
            <div className="bg-gradient-to-br from-amber-500 to-orange-600 rounded-xl p-2.5 text-white">
              <Zap className="w-3.5 h-3.5 opacity-80 mb-1" />
              <span className="text-xl font-black leading-none block">{questionsAnswered}</span>
              <span className="text-[9px] font-bold uppercase opacity-80">Questions</span>
            </div>
            <div className="bg-gradient-to-br from-violet-500 to-purple-600 rounded-xl p-2.5 text-white">
              <Award className="w-3.5 h-3.5 opacity-80 mb-1" />
              <span className="text-xl font-black leading-none block">{Math.round(avgScore)}%</span>
              <span className="text-[9px] font-bold uppercase opacity-80">Moyenne</span>
            </div>
          </div>
        </div>

        {/* Mobile stats row */}
        <div className="grid grid-cols-3 gap-2 md:hidden">
          <div className="bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl p-2 text-white text-center">
            <span className="text-lg font-black leading-none block">{examsCompleted}</span>
            <span className="text-[9px] font-bold uppercase opacity-80">Examens</span>
            {inProgressCount > 0 && <span className="text-[8px] font-bold text-emerald-200 block">{inProgressCount} en cours</span>}
          </div>
          <div className="bg-gradient-to-br from-amber-500 to-orange-600 rounded-xl p-2 text-white text-center">
            <span className="text-lg font-black leading-none block">{questionsAnswered}</span>
            <span className="text-[9px] font-bold uppercase opacity-80">Questions</span>
          </div>
          <div className="bg-gradient-to-br from-violet-500 to-purple-600 rounded-xl p-2 text-white text-center">
            <span className="text-lg font-black leading-none block">{Math.round(avgScore)}%</span>
            <span className="text-[9px] font-bold uppercase opacity-80">Moyenne</span>
          </div>
        </div>

        {/* Row 2: Three mode cards — compact */}
        <div className="grid grid-cols-3 gap-3">
          {/* Coaching */}
          <button
            onClick={() => navigate(hasPlan ? '/coaching/plan' : '/coaching/diagnostic')}
            className="group text-left bg-white rounded-2xl border-2 border-blue-100 p-4 hover:border-blue-400 hover:shadow-lg transition-all relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-bl-full opacity-60 group-hover:opacity-100 transition-opacity" />
            <div className="relative z-10">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center mb-2 shadow-md group-hover:scale-110 transition-transform">
                <GraduationCap className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-sm font-bold text-gray-900">Mode Coaching</h3>
              <p className="text-[11px] text-gray-400 mt-0.5 line-clamp-1">Plan personnalisé</p>
              {hasPlan ? (
                <div className="mt-2">
                  <div className="flex items-center justify-between text-[11px] mb-1">
                    <span className="text-gray-500">Progression</span>
                    <span className="font-bold text-blue-600">{Math.round(planProgress)}%</span>
                  </div>
                  <div className="w-full bg-blue-100 rounded-full h-1.5">
                    <div className="bg-gradient-to-r from-blue-500 to-indigo-600 h-1.5 rounded-full transition-all" style={{ width: `${planProgress}%` }} />
                  </div>
                </div>
              ) : (
                <span className="inline-flex items-center gap-1 text-[11px] font-medium text-blue-600 mt-2"><Play className="w-3 h-3" /> Diagnostic</span>
              )}
            </div>
          </button>

          {/* Libre */}
          <button
            onClick={() => navigate('/libre')}
            className="group text-left bg-white rounded-2xl border-2 border-purple-100 p-4 hover:border-purple-400 hover:shadow-lg transition-all relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-purple-50 to-pink-50 rounded-bl-full opacity-60 group-hover:opacity-100 transition-opacity" />
            <div className="relative z-10">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl flex items-center justify-center mb-2 shadow-md group-hover:scale-110 transition-transform">
                <MessageCircle className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-sm font-bold text-gray-900">Mode Libre</h3>
              <p className="text-[11px] text-gray-400 mt-0.5 line-clamp-1">Questions libres</p>
              <span className="inline-flex items-center gap-1 text-[11px] font-medium text-purple-600 mt-2"><Play className="w-3 h-3" /> Commencer</span>
            </div>
          </button>

          {/* Examen */}
          <button
            onClick={() => navigate('/exam')}
            className="group text-left bg-white rounded-2xl border-2 border-amber-100 p-4 hover:border-amber-400 hover:shadow-lg transition-all relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-amber-50 to-orange-50 rounded-bl-full opacity-60 group-hover:opacity-100 transition-opacity" />
            <div className="relative z-10">
              <div className="w-10 h-10 bg-gradient-to-br from-amber-500 to-orange-600 rounded-xl flex items-center justify-center mb-2 shadow-md group-hover:scale-110 transition-transform">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-sm font-bold text-gray-900">Mode Examen</h3>
              <p className="text-[11px] text-gray-400 mt-0.5 line-clamp-1">Examens nationaux BAC</p>
              <span className="inline-flex items-center gap-1 text-[11px] font-medium text-amber-600 mt-2"><Play className="w-3 h-3" /> S'entraîner</span>
            </div>
          </button>
        </div>

        {/* Row 3: Bottom row — Today's sessions + Subjects */}
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-3 min-h-0">
          {/* Today's sessions */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col min-h-0">
            <div className="flex items-center gap-2 px-4 py-2.5 border-b border-slate-100">
              <Calendar className="w-4 h-4 text-blue-600" />
              <h3 className="text-sm font-bold text-gray-800">Aujourd'hui</h3>
              {todaySessions.length > 0 && (
                <span className="ml-auto text-[10px] font-bold bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full">{todaySessions.length} session{todaySessions.length > 1 ? 's' : ''}</span>
              )}
            </div>
            <div className="flex-1 overflow-y-auto p-2 space-y-1.5">
              {hasPlan && todaySessions.length > 0 ? (
                todaySessions.map((session: any) => (
                  <div key={session.id} className="flex items-center gap-2.5 p-2.5 rounded-xl bg-slate-50 hover:bg-blue-50 transition-colors">
                    <div className={`w-1 h-8 rounded-full ${session.priority === 'high' ? 'bg-red-500' : session.priority === 'medium' ? 'bg-amber-500' : 'bg-emerald-500'}`} />
                    <div className="flex-1 min-w-0">
                      <p className="text-[12px] font-semibold text-gray-800 truncate">{session.subjects?.name_fr || 'Matière'}</p>
                      <p className="text-[10px] text-gray-400 truncate">Ch.{session.chapters?.chapter_number} — {session.chapters?.title_fr}</p>
                    </div>
                    <span className="text-[10px] text-gray-400 shrink-0">{session.scheduled_time?.split('-')[0]}</span>
                    <button
                      onClick={(e) => { e.stopPropagation(); navigate(`/session/${session.chapter_id}`); }}
                      className="w-7 h-7 rounded-lg bg-blue-600 text-white flex items-center justify-center hover:bg-blue-700 shrink-0"
                    >
                      <Play className="w-3 h-3" />
                    </button>
                  </div>
                ))
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-center py-6">
                  <Star className="w-8 h-8 text-amber-300 mb-2" />
                  <p className="text-sm font-semibold text-gray-500">
                    {hasPlan ? 'Aucune session aujourd\'hui' : 'Pas encore de programme'}
                  </p>
                  <button
                    onClick={() => navigate(hasPlan ? '/coaching/plan' : '/coaching/diagnostic')}
                    className="mt-2 text-[11px] font-medium text-blue-600 hover:underline"
                  >
                    {hasPlan ? 'Voir le calendrier' : 'Lancer le diagnostic'} <ChevronRight className="w-3 h-3 inline" />
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Priorités de révision — top 3 weakest topics (actionable) */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col min-h-0">
            <div className="flex items-center gap-2 px-4 py-2.5 border-b border-slate-100">
              <Target className="w-4 h-4 text-rose-600" />
              <h3 className="text-sm font-bold text-gray-800">Priorités de révision</h3>
              {topLacunes.length > 0 && (
                <span className="ml-auto text-[10px] font-bold bg-rose-100 text-rose-600 px-2 py-0.5 rounded-full">
                  {totalLacunes} point{totalLacunes > 1 ? 's' : ''} faible{totalLacunes > 1 ? 's' : ''}
                </span>
              )}
            </div>
            <div className="flex-1 overflow-y-auto p-2 space-y-1.5">
              {topLacunes.length > 0 ? topLacunes.map((lac, i) => {
                const subjectDisplay = CANONICAL_TO_DISPLAY[lac.subject] || lac.subject;
                const accent = SUBJECT_ACCENT[subjectDisplay] || 'from-gray-400 to-gray-500';
                const pri = PRIORITY_META[lac.priority] || PRIORITY_META.moyenne;
                return (
                  <button
                    key={`${lac.subject}-${lac.topic}-${i}`}
                    onClick={() => navigate(hasPlan ? '/coaching/plan' : '/coaching/diagnostic')}
                    className="w-full group flex items-center gap-2.5 p-2.5 rounded-xl hover:bg-slate-50 transition-all text-left border border-transparent hover:border-slate-200"
                  >
                    <div className={`w-1 h-10 rounded-full bg-gradient-to-b ${accent} shrink-0`} />
                    <div className="flex-1 min-w-0">
                      <p className="text-[12px] font-semibold text-gray-800 truncate">{lac.topic}</p>
                      <div className="flex items-center gap-1.5 mt-0.5">
                        <span className="text-[10px] text-gray-400 truncate">{subjectDisplay}</span>
                        <span className="text-gray-300">·</span>
                        <span className={`text-[9px] font-bold uppercase tracking-wider ${pri.text}`}>
                          {pri.label}
                        </span>
                        {typeof lac.score === 'number' && (
                          <>
                            <span className="text-gray-300">·</span>
                            <span className="text-[10px] font-semibold text-gray-500 tabular-nums">{Math.round(lac.score)}%</span>
                          </>
                        )}
                      </div>
                    </div>
                    <ChevronRight className="w-4 h-4 text-gray-300 group-hover:text-rose-500 transition-colors shrink-0" />
                  </button>
                );
              }) : (
                <div className="flex flex-col items-center justify-center h-full text-center py-6 px-4">
                  <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-rose-100 to-amber-100 flex items-center justify-center mb-2">
                    <Target className="w-6 h-6 text-rose-500" />
                  </div>
                  <p className="text-sm font-semibold text-gray-600">Pas encore de données</p>
                  <p className="text-[11px] text-gray-400 mt-1 max-w-[240px]">
                    {hasPlan
                      ? 'Réponds à quelques exercices pour détecter tes priorités.'
                      : 'Lance le diagnostic pour découvrir tes points à travailler.'}
                  </p>
                  <button
                    onClick={() => navigate(hasPlan ? '/exam' : '/coaching/diagnostic')}
                    className="mt-3 inline-flex items-center gap-1.5 px-3 py-1.5 bg-rose-600 text-white rounded-lg text-[11px] font-semibold hover:bg-rose-700 transition-colors"
                  >
                    {hasPlan ? 'Faire un examen' : 'Lancer le diagnostic'}
                    <ChevronRight className="w-3 h-3" />
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Share Modal */}
      {shareOpen && (
        <ShareModal
          studentName={student?.full_name || 'Étudiant'}
          daysRemaining={countdown?.days_remaining}
          onClose={() => setShareOpen(false)}
        />
      )}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
//   ShareModal — Social media sharing with student name
//   Supports: WhatsApp, X (Twitter), Facebook, Snapchat, TikTok
//   Uses Web Share API when available (mobile), otherwise per-network URLs.
// ═══════════════════════════════════════════════════════════════
function ShareModal({
  studentName,
  daysRemaining,
  onClose,
}: {
  studentName: string;
  daysRemaining?: number;
  onClose: () => void;
}) {
  const [copied, setCopied] = useState(false);
  const [tiktokNotice, setTiktokNotice] = useState(false);

  const appUrl = typeof window !== 'undefined' ? window.location.origin : 'https://ai-tutor-bac.app';
  const daysLine = daysRemaining
    ? ` — J-${daysRemaining} avant le BAC`
    : '';
  const shareText = `🎓 ${studentName} prépare le BAC 2026 Sciences Physiques avec معلم (Moalim)${daysLine} ! Rejoins-moi : ${appUrl}`;
  const shareTextShort = `🎓 ${studentName} prépare le BAC 2026 avec معلم (Moalim)${daysLine} !`;

  const encodedText = encodeURIComponent(shareText);
  const encodedShort = encodeURIComponent(shareTextShort);
  const encodedUrl = encodeURIComponent(appUrl);

  const openNative = async () => {
    // Web Share API (mobile) — best UX, lets user pick any installed app
    if (typeof navigator !== 'undefined' && (navigator as any).share) {
      try {
        await (navigator as any).share({
          title: 'معلم — Moalim',
          text: shareTextShort,
          url: appUrl,
        });
        return true;
      } catch {
        // User cancelled — that's fine
      }
    }
    return false;
  };

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(shareText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback: prompt
      window.prompt('Copie ce message :', shareText);
    }
  };

  const handleTikTok = async () => {
    // TikTok has no public web-share URL. Copy text and prompt user to open app.
    try {
      await navigator.clipboard.writeText(shareText);
    } catch {
      /* no-op */
    }
    setTiktokNotice(true);
    setTimeout(() => setTiktokNotice(false), 4000);
  };

  const networks = [
    {
      name: 'WhatsApp',
      color: 'bg-[#25D366] hover:bg-[#1ebe5d]',
      logo: (
        <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.304-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
        </svg>
      ),
      url: `https://wa.me/?text=${encodedText}`,
    },
    {
      name: 'X',
      color: 'bg-black hover:bg-gray-800',
      logo: (
        <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
        </svg>
      ),
      url: `https://twitter.com/intent/tweet?text=${encodedShort}&url=${encodedUrl}`,
    },
    {
      name: 'Facebook',
      color: 'bg-[#1877F2] hover:bg-[#0f63d1]',
      logo: (
        <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
          <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
        </svg>
      ),
      url: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}&quote=${encodedShort}`,
    },
    {
      name: 'Snapchat',
      color: 'bg-[#FFFC00] text-black hover:bg-[#e6e300]',
      logo: (
        <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
          <path d="M12.166 23.445c-.081 0-.16-.003-.24-.009-.062.005-.125.007-.187.007-1.414 0-2.331-.669-3.141-1.258-.582-.424-1.132-.824-1.771-.927-.312-.05-.624-.075-.931-.075-.551 0-.986.082-1.304.142-.195.036-.364.068-.496.068-.141 0-.324-.03-.398-.283-.077-.26-.136-.51-.19-.732-.136-.562-.234-.906-.466-.942-2.51-.388-3.105-.943-3.238-1.335-.024-.07-.038-.14-.042-.213-.008-.185.112-.347.295-.376 2.49-.412 3.606-2.997 3.653-3.104.014-.032.028-.065.04-.097.11-.299.134-.563.07-.783-.124-.417-.666-.606-1.021-.73-.082-.029-.158-.056-.22-.082-.29-.116-1.552-.682-1.3-1.537.186-.63.955-.48 1.3-.33.377.164.72.248 1.02.248.354 0 .528-.117.57-.151-.015-.276-.033-.564-.052-.877-.144-2.309-.323-5.186 1.4-7.12 1.554-1.745 3.54-2.24 4.953-2.24.183 0 .367.008.546.022.1.008.194.017.28.017.08 0 .15-.007.219-.017.168-.013.343-.022.52-.022 1.406 0 3.39.495 4.944 2.24 1.724 1.934 1.545 4.81 1.4 7.12-.018.313-.037.6-.051.877.043.033.21.146.524.152.303-.005.636-.087.99-.248.194-.085.456-.18.73-.18.184 0 .355.037.51.105l.01.004c.22.08.44.223.47.425.036.212-.08.434-.371.653-.125.093-.3.186-.493.28-.36.13-.902.323-1.025.73-.064.22-.042.483.07.782.012.032.025.065.04.097.047.107 1.164 2.692 3.653 3.104.183.03.303.19.295.376-.005.074-.02.145-.04.215-.133.388-.728.944-3.238 1.333-.226.035-.326.32-.466.946-.054.22-.113.466-.188.726-.055.186-.174.276-.369.276h-.027c-.12 0-.293-.025-.498-.065-.381-.073-.805-.138-1.304-.138-.305 0-.617.025-.93.075-.64.103-1.189.503-1.771.927-.811.592-1.728 1.261-3.142 1.261z" />
        </svg>
      ),
      url: `https://www.snapchat.com/scan?attachmentUrl=${encodedUrl}`,
    },
    {
      name: 'TikTok',
      color: 'bg-black hover:bg-gray-800',
      logo: (
        <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor">
          <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64 2.93 2.93 0 01.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005.8 20.1a6.34 6.34 0 0010.86-4.43V8.73a8.16 8.16 0 004.77 1.52V6.8a4.85 4.85 0 01-1.84-.11z" />
        </svg>
      ),
      url: '#',
      custom: handleTikTok,
    },
  ];

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden"
      >
        {/* Header */}
        <div className="bg-gradient-to-br from-blue-600 to-indigo-700 px-6 py-5 text-white">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="text-xl font-bold">Partager ma progression</h3>
              <p className="text-sm text-blue-100 mt-1">
                Invite tes amis à rejoindre {studentName} sur <span className="font-brand">معلم</span>
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

        {/* Preview card */}
        <div className="px-6 pt-5 pb-3">
          <div className="bg-gradient-to-br from-slate-50 to-blue-50 border border-blue-100 rounded-xl p-4">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center">
                <GraduationCap className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="font-bold text-gray-900">{studentName}</p>
                <p className="text-[11px] text-gray-500">2ème BAC Sciences Physiques — BIOF</p>
              </div>
            </div>
            <p className="text-sm text-gray-700 leading-snug">
              🎓 Je prépare le BAC 2026 Sciences Physiques avec
              <span className="font-semibold font-brand"> معلم</span>
              {daysRemaining && (
                <>
                  {' '}—{' '}
                  <span className="font-semibold text-red-600">
                    J-{daysRemaining}
                  </span>
                </>
              )}
              {' '}!
            </p>
          </div>
        </div>

        {/* Native share (mobile) */}
        <div className="px-6 pb-2">
          <button
            onClick={async () => {
              const ok = await openNative();
              if (ok) onClose();
            }}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-gray-900 text-white rounded-xl text-sm font-medium hover:bg-gray-800 transition-colors"
          >
            <Share2 className="w-4 h-4" />
            Partage rapide
          </button>
        </div>

        {/* Social networks */}
        <div className="px-6 py-4">
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Ou choisis un réseau
          </p>
          <div className="grid grid-cols-5 gap-2">
            {networks.map((net) =>
              net.custom ? (
                <button
                  key={net.name}
                  onClick={net.custom}
                  className={`flex flex-col items-center gap-1.5 p-2.5 rounded-xl ${net.color} text-white transition-all hover:shadow-md`}
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
                  className={`flex flex-col items-center gap-1.5 p-2.5 rounded-xl ${net.color} text-white transition-all hover:shadow-md`}
                  title={net.name}
                >
                  {net.logo}
                  <span className="text-[10px] font-medium">{net.name}</span>
                </a>
              )
            )}
          </div>
          {tiktokNotice && (
            <p className="mt-3 text-[11px] text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 flex items-center gap-2">
              <Check className="w-3.5 h-3.5 flex-shrink-0" />
              Texte copié ! Ouvre l'app TikTok et colle-le dans ta publication.
            </p>
          )}
        </div>

        {/* Copy link */}
        <div className="px-6 pb-6">
          <button
            onClick={copyLink}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 border-2 border-gray-200 rounded-xl text-sm font-medium text-gray-700 hover:border-blue-400 hover:text-blue-600 transition-colors"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4 text-emerald-600" />
                <span className="text-emerald-600">Copié !</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                Copier le message
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
