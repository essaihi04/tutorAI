import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { LucideIcon } from 'lucide-react';
import {
  ArrowRight,
  BookOpen,
  CalendarDays,
  Check,
  ChevronRight,
  Clock3,
  FileCheck2,
  MessageCircle,
  PenTool,
  Play,
  Sparkles,
  Target,
  Trophy,
} from 'lucide-react';
import {
  getAllSessions,
  getExamCountdown,
  getMyExamStats,
  getStudyPlan,
  getTodaySchedule,
} from '../services/api';
import { useAuthStore } from '../stores/authStore';
import { useLearningContextStore } from '../stores/learningContextStore';
import type { LearningSubject } from '../stores/learningContextStore';
import MoalimShell from '../components/MoalimShell';
import StudentNavigation from '../components/StudentNavigation';
import MobileBottomNav from '../components/MobileBottomNav';

type StudySession = {
  id?: string;
  chapter_id?: string;
  duration_minutes?: number;
  scheduled_time?: string;
  status?: string;
  session_type?: string;
  subjects?: { name_fr?: string };
  chapters?: { title_fr?: string; chapter_number?: number };
};

type SessionsData = { sessions_by_date?: Record<string, StudySession[]> };
type CountdownData = { days_remaining?: number };
type ExamStatsData = {
  total_questions_answered?: number;
  avg_score_pct?: number;
};

const isPending = (session: StudySession) => !['completed', 'skipped'].includes(session.status || '');
const EMPTY_SUBJECTS: LearningSubject[] = [];

const sessionTypeLabel = (type?: string) => {
  if (type === 'revision') return 'Révision';
  if (type === 'exercice') return 'Exercices';
  if (type === 'lacunes') return 'Renforcement';
  return 'Cours avec Moalim';
};

export default function Dashboard() {
  const navigate = useNavigate();
  const student = useAuthStore((state) => state.student);
  const subjects = useLearningContextStore((state) => state.context?.subjects || EMPTY_SUBJECTS);
  const [loading, setLoading] = useState(true);
  const [todaySessions, setTodaySessions] = useState<StudySession[]>([]);
  const [allSessionsData, setAllSessionsData] = useState<SessionsData | null>(null);
  const [hasPlan, setHasPlan] = useState(false);
  const [planProgress, setPlanProgress] = useState(0);
  const [countdown, setCountdown] = useState<CountdownData | null>(null);
  const [examStats, setExamStats] = useState<ExamStatsData | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      getTodaySchedule().catch(() => null),
      getAllSessions().catch(() => null),
      getStudyPlan().catch(() => null),
      getExamCountdown().catch(() => null),
      getMyExamStats().catch(() => null),
    ]).then(([today, all, plan, bac, stats]) => {
      if (cancelled) return;
      setTodaySessions(today?.data?.sessions || []);
      setAllSessionsData((all?.data as SessionsData) || null);
      setHasPlan(Boolean(plan?.data?.has_plan));
      setPlanProgress(Number(plan?.data?.plan?.progress_percentage || 0));
      setCountdown((bac?.data as CountdownData) || null);
      setExamStats((stats?.data as ExamStatsData) || null);
      setLoading(false);
    });
    return () => { cancelled = true; };
  }, []);

  const firstName = (student?.full_name || 'Élève').trim().split(/\s+/)[0];
  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Bonjour' : hour < 18 ? 'Bon après-midi' : 'Bonsoir';
  const pendingToday = todaySessions.filter(isPending);
  const completedToday = todaySessions.length - pendingToday.length;

  const nextAction = useMemo(() => {
    if (pendingToday.length > 0) {
      const session = pendingToday[0];
      return {
        eyebrow: "Ta prochaine étape",
        title: session.chapters?.title_fr || `Continuer en ${session.subjects?.name_fr || 'cours'}`,
        detail: `${session.subjects?.name_fr || 'Matière'} · ${session.duration_minutes || 30} min · ${sessionTypeLabel(session.session_type)}`,
        button: 'Continuer maintenant',
        path: session.chapter_id ? `/session/${session.chapter_id}` : '/coaching/plan',
      };
    }

    const sessionsByDate = allSessionsData?.sessions_by_date || {};
    const todayIso = new Date().toISOString().slice(0, 10);
    const futureDate = Object.keys(sessionsByDate)
      .filter((date) => date > todayIso && (sessionsByDate[date] || []).some(isPending))
      .sort()[0];
    if (futureDate) {
      const session = (sessionsByDate[futureDate] || []).find(isPending) as StudySession;
      const dateLabel = new Date(`${futureDate}T00:00:00`).toLocaleDateString('fr-FR', {
        weekday: 'long', day: 'numeric', month: 'long',
      });
      return {
        eyebrow: 'Tout est fait pour aujourd’hui',
        title: `Prochaine séance ${dateLabel}`,
        detail: `${session?.subjects?.name_fr || 'Matière'} · ${session?.chapters?.title_fr || 'Séance planifiée'}`,
        button: 'Voir mon programme',
        path: '/coaching/plan',
      };
    }

    if (hasPlan) {
      return {
        eyebrow: 'À toi de choisir',
        title: 'Ton tuteur est prêt',
        detail: 'Commence un cours, pose une question ou entraîne-toi.',
        button: 'Ouvrir mon tuteur',
        path: '/tutor',
      };
    }

    return {
      eyebrow: 'Première étape',
      title: 'Créons ton parcours personnalisé',
      detail: 'Un diagnostic court permet à Moalim de choisir les bons cours et exercices.',
      button: 'Commencer mon diagnostic',
      path: '/coaching/diagnostic',
    };
  }, [allSessionsData, hasPlan, pendingToday]);

  const quickModes: Array<{
    icon: LucideIcon;
    title: string;
    description: string;
    path: string;
    color: string;
  }> = [
    {
      icon: BookOpen,
      title: 'Apprendre un cours',
      description: 'Explication pas à pas avec ton tuteur.',
      path: '/courses',
      color: 'from-indigo-500 to-violet-500',
    },
    {
      icon: PenTool,
      title: 'Faire des exercices',
      description: 'Entraînement guidé et correction immédiate.',
      path: '/exam',
      color: 'from-emerald-500 to-teal-500',
    },
    {
      icon: FileCheck2,
      title: 'Préparer un examen',
      description: 'Sujets nationaux et conditions réelles.',
      path: '/exam',
      color: 'from-amber-500 to-orange-500',
    },
  ];

  const questionsAnswered = Number(examStats?.total_questions_answered || 0);
  const scoreOn20 = Math.round(Number(examStats?.avg_score_pct || 0) * 0.2 * 10) / 10;
  const daysRemaining = Number(countdown?.days_remaining || 0);

  return (
    <MoalimShell>
      <StudentNavigation active="today" />
      <main className="mx-auto max-w-7xl space-y-8 px-4 pb-28 pt-6 sm:px-6 lg:px-8 lg:pb-12 lg:pt-10">
        <section className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="mb-1 text-sm font-semibold text-cyan-300/80">{greeting}, {firstName}</p>
            <h1 className="text-3xl font-black tracking-tight text-white sm:text-4xl">Que veux-tu réussir aujourd’hui ?</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-white/45">
              Une seule prochaine étape, puis Moalim te guide sans te perdre dans les menus.
            </p>
          </div>
          {subjects.length > 0 && (
            <div className="flex flex-wrap gap-2 lg:hidden">
              {subjects.map((subject) => (
                <span key={subject.id} className="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs font-semibold text-white/60">
                  {subject.icon || '•'} {subject.name_fr}
                </span>
              ))}
            </div>
          )}
        </section>

        <section className="relative overflow-hidden rounded-[28px] border border-indigo-400/20 bg-gradient-to-br from-indigo-600/30 via-violet-600/20 to-cyan-500/10 p-5 shadow-2xl shadow-indigo-950/30 sm:p-8">
          <div className="pointer-events-none absolute -right-16 -top-20 h-64 w-64 rounded-full bg-cyan-400/20 blur-3xl" />
          <div className="relative grid gap-6 lg:grid-cols-[1fr_auto] lg:items-center">
            <div>
              <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.07] px-3 py-1 text-xs font-bold text-cyan-200">
                <Sparkles className="h-3.5 w-3.5" /> {nextAction.eyebrow}
              </div>
              <h2 className="max-w-3xl text-2xl font-black text-white sm:text-3xl">{nextAction.title}</h2>
              <p className="mt-2 text-sm leading-6 text-white/60">{nextAction.detail}</p>
            </div>
            <button
              onClick={() => navigate(nextAction.path)}
              className="flex w-full items-center justify-center gap-2 rounded-2xl bg-white px-5 py-3.5 text-sm font-black text-indigo-950 shadow-xl shadow-black/20 transition hover:-translate-y-0.5 hover:bg-cyan-50 lg:w-auto"
            >
              <Play className="h-4 w-4 fill-current" /> {nextAction.button}
            </button>
          </div>
        </section>

        <section>
          <div className="mb-4 flex items-end justify-between gap-3">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-white/30">Un seul tuteur</p>
              <h2 className="mt-1 text-xl font-black text-white">Choisis simplement ton objectif</h2>
            </div>
            <button onClick={() => navigate('/tutor')} className="hidden items-center gap-1 text-xs font-bold text-cyan-300 hover:text-cyan-200 sm:flex">
              Tout voir <ArrowRight className="h-3.5 w-3.5" />
            </button>
          </div>
          <div className="grid gap-3 md:grid-cols-3">
            {quickModes.map((mode) => {
              const Icon = mode.icon;
              return (
                <button
                  key={mode.title}
                  onClick={() => navigate(mode.path)}
                  className="group flex items-center gap-4 rounded-2xl border border-white/[0.07] bg-white/[0.035] p-4 text-left transition hover:-translate-y-0.5 hover:border-white/15 hover:bg-white/[0.06]"
                >
                  <span className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br ${mode.color} shadow-lg`}>
                    <Icon className="h-5 w-5 text-white" />
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block text-sm font-bold text-white">{mode.title}</span>
                    <span className="mt-1 block text-xs leading-5 text-white/40">{mode.description}</span>
                  </span>
                  <ChevronRight className="h-4 w-4 shrink-0 text-white/20 transition group-hover:translate-x-0.5 group-hover:text-white/60" />
                </button>
              );
            })}
          </div>
        </section>

        <section className="grid gap-4 lg:grid-cols-[1.45fr_0.75fr]">
          <div className="rounded-3xl border border-white/[0.07] bg-white/[0.035] p-4 sm:p-5">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.18em] text-white/30">Aujourd’hui</p>
                <h2 className="mt-1 text-lg font-black text-white">Ton programme</h2>
              </div>
              {todaySessions.length > 0 && (
                <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-bold text-emerald-300">
                  {completedToday}/{todaySessions.length} terminé{todaySessions.length > 1 ? 's' : ''}
                </span>
              )}
            </div>

            {loading ? (
              <div className="h-28 animate-pulse rounded-2xl bg-white/[0.04]" />
            ) : todaySessions.length > 0 ? (
              <div className="space-y-2">
                {todaySessions.map((session, index) => {
                  const done = !isPending(session);
                  return (
                    <button
                      key={session.id || index}
                      disabled={done}
                      onClick={() => navigate(session.chapter_id ? `/session/${session.chapter_id}` : '/coaching/plan')}
                      className={`flex w-full items-center gap-3 rounded-2xl border p-3 text-left transition ${
                        done
                          ? 'border-emerald-500/10 bg-emerald-500/[0.04] opacity-70'
                          : 'border-white/[0.07] bg-black/10 hover:border-indigo-400/30 hover:bg-white/[0.05]'
                      }`}
                    >
                      <span className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${done ? 'bg-emerald-500/15 text-emerald-300' : 'bg-indigo-500/15 text-indigo-300'}`}>
                        {done ? <Check className="h-5 w-5" /> : <span className="text-sm font-black">{index + 1}</span>}
                      </span>
                      <span className="min-w-0 flex-1">
                        <span className="block truncate text-sm font-bold text-white">{session.chapters?.title_fr || sessionTypeLabel(session.session_type)}</span>
                        <span className="mt-1 flex flex-wrap items-center gap-2 text-[11px] text-white/40">
                          <span>{session.subjects?.name_fr || 'Matière'}</span>
                          <span>•</span>
                          <span>{session.duration_minutes || 30} min</span>
                          {session.scheduled_time && <><span>•</span><span>{session.scheduled_time}</span></>}
                        </span>
                      </span>
                      {!done && <ChevronRight className="h-4 w-4 text-white/25" />}
                    </button>
                  );
                })}
              </div>
            ) : (
              <div className="flex flex-col items-center rounded-2xl border border-dashed border-white/10 px-4 py-8 text-center">
                <CalendarDays className="h-7 w-7 text-white/20" />
                <p className="mt-3 text-sm font-bold text-white/70">Aucune séance imposée ce soir</p>
                <p className="mt-1 text-xs text-white/35">Tu peux demander au tuteur de travailler ce dont tu as besoin.</p>
                <button onClick={() => navigate('/tutor')} className="mt-4 text-xs font-bold text-cyan-300">Choisir une activité</button>
              </div>
            )}
          </div>

          <div className="space-y-4">
            <button
              onClick={() => navigate('/libre')}
              className="group w-full overflow-hidden rounded-3xl border border-cyan-400/15 bg-gradient-to-br from-cyan-500/15 to-indigo-500/10 p-5 text-left transition hover:border-cyan-300/30"
            >
              <span className="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400 text-[#07111c] shadow-lg shadow-cyan-500/20">
                <MessageCircle className="h-5 w-5" />
              </span>
              <span className="mt-4 block text-lg font-black text-white">J’ai une question</span>
              <span className="mt-1 block text-xs leading-5 text-white/45">Ouvre directement le tuteur et explique ce qui te bloque.</span>
              <span className="mt-4 flex items-center gap-1 text-xs font-bold text-cyan-300">Parler à Moalim <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-1" /></span>
            </button>

            <div className="grid grid-cols-3 gap-2 rounded-3xl border border-white/[0.07] bg-white/[0.035] p-3">
              <MiniStat icon={Target} value={`${Math.round(planProgress)}%`} label="Parcours" />
              <MiniStat icon={Trophy} value={`${scoreOn20}/20`} label="Moyenne" />
              <MiniStat icon={Clock3} value={daysRemaining > 0 ? `${daysRemaining}j` : '—'} label="Avant BAC" />
            </div>
            {questionsAnswered > 0 && (
              <p className="text-center text-[11px] text-white/30">Déjà {questionsAnswered} question{questionsAnswered > 1 ? 's' : ''} traitée{questionsAnswered > 1 ? 's' : ''}</p>
            )}
          </div>
        </section>
      </main>
      <MobileBottomNav active="today" />
    </MoalimShell>
  );
}

function MiniStat({ icon: Icon, value, label }: { icon: LucideIcon; value: string; label: string }) {
  return (
    <div className="min-w-0 rounded-2xl bg-black/10 px-2 py-3 text-center">
      <Icon className="mx-auto h-4 w-4 text-white/30" />
      <div className="mt-2 truncate text-sm font-black text-white">{value}</div>
      <div className="mt-0.5 truncate text-[9px] font-semibold uppercase tracking-wide text-white/30">{label}</div>
    </div>
  );
}
