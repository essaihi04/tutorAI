import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getExamCountdown, getStudyPlan, getTodaySchedule, getProficiency, getMyExamStats, getMe, getAllSessions,
} from '../services/api';
import { useAuthStore } from '../stores/authStore';
import {
  GraduationCap, MessageCircle, Calendar, Play, LogOut, Trophy,
  Award, BarChart3, ArrowRight, Clock, PenLine, Flame,
  ChevronRight, Target, ChevronLeft, CheckCircle, X as XIcon,
} from 'lucide-react';
import MoalimShell, { MoalimLogo } from '../components/MoalimShell';
import MobileBottomNav from '../components/MobileBottomNav';

/* ──────────────────────────────────────────────────────────────
   DASHBOARD MOALIM — structure inspirée de la landing
   ─ Sidebar gauche (nav)
   ─ Welcome banner + Continuer ma session
   ─ 4 KPIs (Heures · Exercices · Score moy. · BAC J-X)
   ─ Performance par matière (bar chart `by_subject`)
   ─ Mention projetée (cercle SVG)
   ─ Sessions aujourd'hui + Priorités de révision (en dessous)
   ─ Données 100% via services existants — aucun ajout
   ────────────────────────────────────────────────────────────── */

const SUBJECT_COLOR: Record<string, { bar: string; dot: string; label: string }> = {
  Physique:       { bar: 'from-indigo-400 to-indigo-300',   dot: 'bg-indigo-400',  label: 'PC' },
  Chimie:         { bar: 'from-rose-400 to-rose-300',       dot: 'bg-rose-400',    label: 'Chimie' },
  'Mathématiques':{ bar: 'from-amber-400 to-amber-300',     dot: 'bg-amber-400',   label: 'Math' },
  Mathematiques:  { bar: 'from-amber-400 to-amber-300',     dot: 'bg-amber-400',   label: 'Math' },
  Math:           { bar: 'from-amber-400 to-amber-300',     dot: 'bg-amber-400',   label: 'Math' },
  SVT:            { bar: 'from-emerald-400 to-emerald-300', dot: 'bg-emerald-400', label: 'SVT' },
};

const normalizeSubjectName = (value: unknown) => {
  const raw = String(value || '').trim();
  const lower = raw.toLowerCase();
  if (lower.includes('svt') || lower.includes('vie') || lower.includes('terre')) return 'SVT';
  if (lower.includes('math')) return 'Mathématiques';
  if (lower.includes('chim')) return 'Chimie';
  if (lower.includes('phys') || lower.includes('pc') || lower.includes('2bac')) return 'Physique';
  return raw || 'Inconnu';
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
  const [allSessionsData, setAllSessionsData] = useState<any>(null);
  const [calendarMonth, setCalendarMonth] = useState<Date>(new Date());
  const [selectedDay, setSelectedDay] = useState<string | null>(null);
  const navigate = useNavigate();
  const { student, logout, setStudent } = useAuthStore();

  useEffect(() => {
    loadData();
    if (!student?.full_name) {
      getMe().then((res) => {
        setStudent({
          id: String(res.data.id || ''),
          username: res.data.username || '',
          email: res.data.email || '',
          full_name: res.data.full_name || '',
          preferred_language: res.data.preferred_language || 'fr',
        });
      }).catch(() => {});
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadData = async () => {
    try {
      const countdownRes = await getExamCountdown().catch(() => null);
      if (countdownRes) setCountdown(countdownRes.data);
      const [planRes, todayRes, profRes, examStatsRes, allSessRes] = await Promise.all([
        getStudyPlan().catch(() => null),
        getTodaySchedule().catch(() => null),
        getProficiency().catch(() => null),
        getMyExamStats().catch(() => null),
        getAllSessions().catch(() => null),
      ]);
      if (planRes?.data?.has_plan) {
        setHasPlan(true);
        setPlanProgress(planRes.data.plan.progress_percentage || 0);
      }
      if (todayRes?.data?.sessions) setTodaySessions(todayRes.data.sessions);
      if (profRes?.data) setProficiency(profRes.data);
      if (examStatsRes?.data) setExamStats(examStatsRes.data);
      if (allSessRes?.data) setAllSessionsData(allSessRes.data);
    } catch {
      /* api not ready */
    }
  };

  const firstName = (student?.full_name || 'Étudiant').trim().split(/\s+/)[0];
  const hour = new Date().getHours();
  const timeGreeting = hour < 12 ? 'Bonjour' : hour < 18 ? 'Bon après-midi' : 'Bonsoir';

  // ─── KPIs depuis examStats (services existants) ───────────────
  const totalSeconds = examStats?.total_duration_seconds || 0;
  const totalHours = Math.floor(totalSeconds / 3600);
  const totalMinutes = Math.floor((totalSeconds % 3600) / 60);
  const hoursDisplay = totalHours > 0 ? `${totalHours}h` : `${totalMinutes}min`;

  const questionsAnswered = examStats?.total_questions_answered || 0;
  const avgScorePct = examStats?.avg_score_pct || 0;
  const scoreOn20 = Math.round(avgScorePct * 0.2 * 10) / 10; // /20 avec 1 décimale
  const examsTaken = examStats?.unique_exams_taken || 0;
  const inProgressCount = examStats?.in_progress_count || 0;
  const daysRemaining = countdown?.days_remaining || 0;

  // Mention BAC marocain
  const mention = useMemo(() => {
    if (scoreOn20 >= 16) return { label: 'Très Bien', color: 'text-emerald-300', bg: 'bg-emerald-500/15', icon: '🏆' };
    if (scoreOn20 >= 14) return { label: 'Bien',       color: 'text-cyan-300',    bg: 'bg-cyan-500/15',    icon: '⭐' };
    if (scoreOn20 >= 12) return { label: 'Assez Bien', color: 'text-indigo-300',  bg: 'bg-indigo-500/15',  icon: '👍' };
    if (scoreOn20 >= 10) return { label: 'Passable',   color: 'text-amber-300',   bg: 'bg-amber-500/15',   icon: '✓' };
    return                 { label: 'En préparation', color: 'text-white/60',    bg: 'bg-white/5',        icon: '🎯' };
  }, [scoreOn20]);

  // Lacunes pour panel "Priorités"
  const { topLacunes, totalLacunes } = useMemo(() => {
    const all: any[] = (proficiency?.lacunes as any[]) || [];
    return { topLacunes: all.slice(0, 3), totalLacunes: all.length };
  }, [proficiency]);

  // by_subject pour le bar chart
  const subjectStats: Array<{ subject: string; questions: number; avg: number; exams: number }> =
    useMemo(() => {
      const rows = (examStats?.by_subject as any[]) || [];
      const grouped = new Map<string, { subject: string; questions: number; scoreSum: number; weight: number; exams: number }>();

      rows.forEach((row) => {
        const subject = normalizeSubjectName(row?.subject);
        const questions = Number(row?.questions || 0);
        const avg = Number(row?.avg_score_pct ?? row?.avg ?? 0);
        const exams = Number(row?.exams || 0);
        const safeAvg = Number.isFinite(avg) ? avg : 0;
        const weight = Math.max(questions, exams, 1);
        const current = grouped.get(subject) || { subject, questions: 0, scoreSum: 0, weight: 0, exams: 0 };

        current.questions += Number.isFinite(questions) ? questions : 0;
        current.scoreSum += safeAvg * weight;
        current.weight += weight;
        current.exams += Number.isFinite(exams) ? exams : 0;
        grouped.set(subject, current);
      });

      return Array.from(grouped.values())
        .map((row) => ({
          subject: row.subject,
          questions: row.questions,
          avg: row.weight > 0 ? row.scoreSum / row.weight : 0,
          exams: row.exams,
        }))
        .filter((row) => row.questions > 0 || row.exams > 0)
        .sort((a, b) => b.questions - a.questions)
        .slice(0, 4);
    }, [examStats]);

  const maxQuestions = Math.max(1, ...subjectStats.map((s) => s.questions));

  // Suggestion CTA dynamique — ne propose que les séances du jour NON terminées,
  // sinon cherche la prochaine séance en attente dans le calendrier, sinon
  // félicite et propose les fallbacks (examens / lacunes / plan / diagnostic).
  const continueCta = useMemo(() => {
    const isPending = (s: any) => s?.status !== 'completed' && s?.status !== 'skipped';

    // 1) Séances d'aujourd'hui non terminées
    const pendingToday = (todaySessions || []).filter(isPending);
    if (pendingToday.length > 0) {
      const s = pendingToday[0];
      const subj = s.subjects?.name_fr || 'matière';
      return {
        text: `Tu as ${pendingToday.length} session${pendingToday.length > 1 ? 's' : ''} à faire en ${subj}`,
        href: `/session/${s.chapter_id}`,
      };
    }

    const todayHadSessions = (todaySessions || []).length > 0;
    const todayAllDone = todayHadSessions && pendingToday.length === 0;

    // 2) Prochaine séance future en attente (la plus proche)
    const byDate = allSessionsData?.sessions_by_date || {};
    const todayISO = new Date().toISOString().slice(0, 10);
    const futureDates = Object.keys(byDate)
      .filter((iso) => iso > todayISO)
      .sort();
    for (const iso of futureDates) {
      const list = (byDate[iso] || []).filter(isPending);
      if (list.length > 0) {
        const s = list[0];
        const subj = s.subjects?.name_fr || 'matière';
        const d = new Date(iso + 'T00:00:00');
        const dayLabel = d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });
        if (todayAllDone) {
          return {
            text: `🎉 Bravo, journée terminée ! Prochaine séance ${dayLabel} en ${subj}`,
            href: '/coaching/plan',
          };
        }
        return {
          text: `Prochaine séance ${dayLabel} en ${subj}`,
          href: '/coaching/plan',
        };
      }
    }

    // 3) Aujourd'hui terminé mais aucune séance future trouvée
    if (todayAllDone) {
      if (inProgressCount > 0) {
        return {
          text: `🎉 Journée terminée ! Tu peux finir ${inProgressCount} examen${inProgressCount > 1 ? 's' : ''} en cours`,
          href: '/exam',
        };
      }
      return {
        text: '🎉 Bravo, journée terminée ! Prends de l\'avance avec un examen',
        href: '/exam',
      };
    }

    // 4) Fallbacks existants
    if (inProgressCount > 0) {
      return {
        text: `${inProgressCount} examen${inProgressCount > 1 ? 's' : ''} en cours à terminer`,
        href: '/exam',
      };
    }
    if (totalLacunes > 0) {
      return {
        text: `${totalLacunes} point${totalLacunes > 1 ? 's' : ''} faible${totalLacunes > 1 ? 's' : ''} à renforcer`,
        href: hasPlan ? '/coaching/plan' : '/coaching/diagnostic',
      };
    }
    if (hasPlan) {
      return { text: 'Continue ton plan personnalisé', href: '/coaching/plan' };
    }
    return { text: 'Lance ton diagnostic pour commencer', href: '/coaching/diagnostic' };
  }, [todaySessions, allSessionsData, inProgressCount, totalLacunes, hasPlan]);

  return (
    <MoalimShell>
      <div className="min-h-screen flex flex-col lg:flex-row">
        {/* ═══ SIDEBAR ═══ */}
        <Sidebar firstName={firstName} timeGreeting={timeGreeting} onLogout={logout} />

        {/* ═══ MAIN ═══ */}
        <main className="flex-1 min-w-0 p-4 sm:p-5 lg:p-6 space-y-4 sm:space-y-5 pb-24 lg:pb-6">
          {/* Welcome banner */}
          <WelcomeBanner
            firstName={firstName}
            ctaText={continueCta.text}
            onContinue={() => navigate(continueCta.href)}
          />

          {/* 4 KPI tiles */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
            <KpiCard icon={Clock}    grad="from-indigo-500 to-blue-600"     label="Heures"      value={hoursDisplay}      sub={examsTaken > 0 ? `${examsTaken} examens` : undefined} />
            <KpiCard icon={PenLine}  grad="from-emerald-500 to-teal-600"    label="Exercices"   value={String(questionsAnswered)} sub={questionsAnswered > 0 ? 'questions' : undefined} />
            <KpiCard icon={Trophy}   grad="from-amber-500 to-orange-500"    label="Score moy."  value={`${scoreOn20}/20`} sub={mention.label} />
            <KpiCard icon={Flame}    grad="from-rose-500 to-pink-600"       label="BAC dans"    value={daysRemaining > 0 ? `${daysRemaining}j` : '—'} sub={daysRemaining > 0 ? 'restants' : undefined} />
          </div>

          {/* Charts row */}
          <div className="grid lg:grid-cols-[1.4fr_1fr] gap-3 sm:gap-4">
            {/* Performance par matière */}
            <div className="glass rounded-2xl p-4 sm:p-5">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <div className="text-sm font-semibold text-white">Performance par matière</div>
                  <div className="text-[11px] text-white/45 mt-0.5">Score moyen + nombre de questions traitées</div>
                </div>
                <div className="text-[10px] text-white/40 hidden sm:block">2BAC PC BIOF</div>
              </div>

              {subjectStats.length > 0 ? (
                <>
                  <div className="flex items-end gap-3 sm:gap-4 h-36 px-1">
                    {subjectStats.map((s) => {
                      const color = SUBJECT_COLOR[s.subject] || { bar: 'from-white/40 to-white/30', dot: 'bg-white/40', label: s.subject };
                      const avgLabel = Number.isFinite(s.avg) ? Math.round(s.avg) : 0;
                      const questionCount = Number.isFinite(s.questions) ? s.questions : 0;
                      const heightPct = Math.max(8, (questionCount / maxQuestions) * 100);
                      return (
                        <div key={s.subject} className="flex-1 flex flex-col items-center gap-1.5 group">
                          <div className="text-[11px] font-bold text-white tabular-nums">{avgLabel}%</div>
                          <div className="w-full flex flex-col justify-end h-full">
                            <div
                              className={`w-full rounded-t-md bg-gradient-to-t ${color.bar} group-hover:brightness-110 transition-all relative`}
                              style={{ height: `${heightPct}%` }}
                            >
                              <div className="absolute inset-x-0 top-1.5 text-center text-[9px] font-bold text-black/60">
                                {questionCount}
                              </div>
                            </div>
                          </div>
                          <div className="text-[10px] text-white/55 text-center truncate w-full">{color.label}</div>
                        </div>
                      );
                    })}
                  </div>
                  <div className="flex flex-wrap gap-3 mt-4 pt-3 border-t border-white/5 text-[10px] text-white/55">
                    {subjectStats.map((s) => {
                      const color = SUBJECT_COLOR[s.subject] || { bar: '', dot: 'bg-white/40', label: s.subject };
                      return (
                        <span key={s.subject} className="flex items-center gap-1.5">
                          <span className={`w-2 h-2 rounded-sm ${color.dot}`} />
                          {color.label} · {s.questions} questions
                        </span>
                      );
                    })}
                  </div>
                </>
              ) : (
                <EmptyChart
                  icon={<BarChart3 className="w-10 h-10 text-white/20 mb-2" />}
                  title="Pas encore de données"
                  hint="Termine un examen ou un exercice pour voir ta performance par matière."
                  cta="Faire un examen"
                  onCta={() => navigate('/exam')}
                />
              )}
            </div>

            {/* Mention projetée */}
            <div className="glass rounded-2xl p-4 sm:p-5 flex flex-col">
              <div className="text-sm font-semibold text-white">Mention projetée</div>
              <div className="text-[11px] text-white/45 mt-0.5 mb-1">
                {examsTaken > 0
                  ? `Sur la base de tes ${examsTaken} évaluation${examsTaken > 1 ? 's' : ''}`
                  : 'Pas encore de score — fais ton premier examen'}
              </div>

              <div className="flex-1 flex items-center justify-center relative py-2">
                <MentionRing scoreOn20={scoreOn20} />
              </div>

              <div className="text-center mt-2">
                <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full ${mention.bg} ${mention.color} text-[11px] font-bold`}>
                  <span>{mention.icon}</span> Mention {mention.label}
                </span>
              </div>
            </div>
          </div>

          {/* Bottom row : Calendrier coaching + Priorités */}
          <div className="grid lg:grid-cols-[1.4fr_1fr] gap-3 sm:gap-4 pb-6">
            <CalendarPanel
              month={calendarMonth}
              setMonth={setCalendarMonth}
              sessionsByDate={allSessionsData?.sessions_by_date || {}}
              onSelectDay={setSelectedDay}
              hasPlan={hasPlan}
              onCta={() => navigate(hasPlan ? '/coaching/plan' : '/coaching/diagnostic')}
            />

            <Panel
              icon={<Target className="w-4 h-4 text-rose-300" />}
              title="Priorités de révision"
              badge={topLacunes.length > 0 ? `${totalLacunes} faible${totalLacunes > 1 ? 's' : ''}` : undefined}
              badgeColor="bg-rose-500/20 text-rose-200"
            >
              {topLacunes.length > 0 ? topLacunes.map((lac, i) => {
                const pri = PRIORITY_META[lac.priority] || PRIORITY_META.moyenne;
                const color = SUBJECT_COLOR[lac.subject] || { dot: 'bg-white/40', label: lac.subject };
                return (
                  <button
                    key={`${lac.subject}-${lac.topic}-${i}`}
                    onClick={() => navigate(hasPlan ? '/coaching/plan' : '/coaching/diagnostic')}
                    className="w-full group flex items-center gap-2.5 p-2.5 rounded-xl bg-white/[.02] hover:bg-white/[.06] transition-all text-left border border-transparent hover:border-white/10"
                  >
                    <div className={`w-1 h-10 rounded-full ${color.dot}`} />
                    <div className="flex-1 min-w-0">
                      <p className="text-[12px] font-semibold text-white truncate">{lac.topic}</p>
                      <div className="flex items-center gap-1.5 mt-0.5">
                        <span className="text-[10px] text-white/45 truncate">{color.label}</span>
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

          {/* Day detail modal */}
          {selectedDay && (
            <DayDetailModal
              dayISO={selectedDay}
              sessions={allSessionsData?.sessions_by_date?.[selectedDay] || []}
              onClose={() => setSelectedDay(null)}
              onStartSession={(chapterId) => {
                setSelectedDay(null);
                navigate(`/session/${chapterId}`);
              }}
            />
          )}

          {/* Plan progress (si plan actif) */}
          {hasPlan && (
            <div className="glass rounded-2xl p-4 mb-6 hidden sm:block">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Award className="w-4 h-4 text-indigo-300" />
                  <span className="text-sm font-semibold text-white">Progression du plan d'étude</span>
                </div>
                <span className="text-sm font-bold text-indigo-300 tabular-nums">{Math.round(planProgress)}%</span>
              </div>
              <div className="w-full bg-white/5 rounded-full h-2 overflow-hidden">
                <div className="h-2 bg-gradient-to-r from-indigo-400 via-cyan-400 to-amber-400 transition-all" style={{ width: `${planProgress}%` }} />
              </div>
            </div>
          )}
        </main>
      </div>
      <MobileBottomNav active="dashboard" />
    </MoalimShell>
  );
}

// ═════════════════════════════════════════════════════════════
//   SIDEBAR
// ═════════════════════════════════════════════════════════════
function Sidebar({ firstName, timeGreeting, onLogout }: {
  firstName: string; timeGreeting: string; onLogout: () => void;
}) {
  const navigate = useNavigate();
  const items = [
    { icon: BarChart3,    label: 'Tableau de bord', path: '/dashboard',     active: true },
    { icon: GraduationCap,label: 'Coaching IA',     path: '/coaching/plan', active: false },
    { icon: MessageCircle,label: 'Mode libre',      path: '/libre',         active: false },
    { icon: Trophy,       label: 'Examens réels',   path: '/exam',          active: false },
  ];

  return (
    <aside className="lg:w-[260px] lg:flex-shrink-0 lg:p-5 lg:border-r lg:border-white/5 lg:min-h-screen">
      {/* Mobile top bar */}
      <div className="lg:hidden flex items-center justify-between p-4 border-b border-white/5 backdrop-blur-2xl bg-[#070718]/70 sticky top-0 z-30">
        <MoalimLogo size="sm" />
        <button onClick={onLogout} className="p-2 text-white/40 hover:text-rose-300 hover:bg-rose-500/10 rounded-lg transition-colors">
          <LogOut className="w-4 h-4" />
        </button>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:flex flex-col gap-1 sticky top-5">
        <div className="glass rounded-2xl p-4 mb-3">
          <MoalimLogo size="md" />
          <div className="mt-3 px-1">
            <p className="text-[10px] uppercase tracking-widest text-white/35 font-semibold">{timeGreeting}</p>
            <p className="text-sm font-bold text-white truncate">{firstName}</p>
          </div>
        </div>

        <nav className="space-y-0.5">
          {items.map((it) => (
            <button
              key={it.label}
              onClick={() => navigate(it.path)}
              className={`w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-sm transition-colors ${
                it.active
                  ? 'bg-indigo-500/15 text-indigo-200 border border-indigo-400/20'
                  : 'text-white/55 hover:text-white hover:bg-white/[.04]'
              }`}
            >
              <it.icon className="w-4 h-4" />
              <span className="font-medium">{it.label}</span>
            </button>
          ))}
        </nav>

        <div className="mt-auto pt-6">
          <button onClick={onLogout} className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs text-white/45 hover:text-rose-300 hover:bg-rose-500/10 transition-colors">
            <LogOut className="w-3.5 h-3.5" /> Déconnexion
          </button>
        </div>
      </div>
    </aside>
  );
}

// ═════════════════════════════════════════════════════════════
//   WELCOME BANNER
// ═════════════════════════════════════════════════════════════
function WelcomeBanner({ firstName, ctaText, onContinue }: {
  firstName: string; ctaText: string; onContinue: () => void;
}) {
  return (
    <div className="rounded-2xl p-5 sm:p-6 bg-gradient-to-br from-indigo-600/30 via-purple-600/20 to-cyan-600/20 border border-white/5 relative overflow-hidden anim-fade-up">
      <div className="absolute -top-12 -right-10 w-44 h-44 rounded-full bg-cyan-400/25 blur-3xl" />
      <div className="absolute -bottom-12 -left-10 w-40 h-40 rounded-full bg-fuchsia-500/15 blur-3xl" />
      <div className="relative flex items-center justify-between flex-wrap gap-3">
        <div className="min-w-0">
          <h2 className="text-xl sm:text-2xl font-black text-white truncate">
            Bon retour, {firstName} <span className="inline-block">✨</span>
          </h2>
          <p className="text-sm text-white/65 mt-1">{ctaText}</p>
        </div>
        <button
          onClick={onContinue}
          className="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 border border-white/15 text-sm font-semibold text-white flex items-center gap-2 transition-all backdrop-blur"
        >
          Continuer ma session <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

// ═════════════════════════════════════════════════════════════
//   KPI CARD
// ═════════════════════════════════════════════════════════════
function KpiCard({ icon: Icon, label, value, sub, grad }: {
  icon: any; label: string; value: string; sub?: string; grad: string;
}) {
  return (
    <div className="glass rounded-2xl p-4 relative overflow-hidden">
      <div className={`w-9 h-9 rounded-xl bg-gradient-to-br ${grad} flex items-center justify-center mb-2 shadow-lg`}>
        <Icon className="w-4 h-4 text-white" />
      </div>
      <div className="text-[11px] text-white/45 font-medium uppercase tracking-wider">{label}</div>
      <div className="flex items-baseline gap-1.5 mt-0.5">
        <span className="text-xl sm:text-2xl font-black text-white tabular-nums">{value}</span>
        {sub && <span className="text-[10px] text-white/45 font-medium truncate">{sub}</span>}
      </div>
    </div>
  );
}

// ═════════════════════════════════════════════════════════════
//   MENTION RING (cercle SVG comme dans la landing)
// ═════════════════════════════════════════════════════════════
function MentionRing({ scoreOn20 }: { scoreOn20: number }) {
  const radius = 52;
  const circumference = 2 * Math.PI * radius; // 326
  const pct = Math.max(0, Math.min(20, scoreOn20)) / 20;
  const offset = circumference * (1 - pct);

  return (
    <div className="relative">
      <svg className="w-32 h-32 sm:w-36 sm:h-36 -rotate-90" viewBox="0 0 128 128">
        <circle cx="64" cy="64" r={radius} stroke="rgba(255,255,255,.08)" strokeWidth="10" fill="none" />
        <circle
          cx="64" cy="64" r={radius}
          stroke="url(#mentionGrad)"
          strokeWidth="10"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 1s ease-out' }}
        />
        <defs>
          <linearGradient id="mentionGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stopColor="#6366f1" />
            <stop offset="0.5" stopColor="#22d3ee" />
            <stop offset="1" stopColor="#fbbf24" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <div className="text-3xl sm:text-4xl font-black gradient-text leading-none">{scoreOn20.toFixed(1)}</div>
        <div className="text-[10px] text-white/55 mt-1">/ 20</div>
      </div>
    </div>
  );
}

// ═════════════════════════════════════════════════════════════
//   PANEL + EMPTY STATES
// ═════════════════════════════════════════════════════════════
function Panel({ icon, title, badge, badgeColor, children }: {
  icon: React.ReactNode; title: string; badge?: string; badgeColor?: string; children: React.ReactNode;
}) {
  return (
    <div className="glass rounded-2xl overflow-hidden flex flex-col">
      <div className="flex items-center gap-2 px-4 py-2.5 border-b border-white/5">
        {icon}
        <h3 className="text-sm font-bold text-white">{title}</h3>
        {badge && (
          <span className={`ml-auto text-[10px] font-bold px-2 py-0.5 rounded-full ${badgeColor || 'bg-white/10 text-white/70'}`}>
            {badge}
          </span>
        )}
      </div>
      <div className="p-2 space-y-1.5 max-h-[240px] overflow-y-auto moalim-scroll">
        {children}
      </div>
    </div>
  );
}

function EmptyState({ icon, title, hint, cta, onCta }: {
  icon: React.ReactNode; title: string; hint?: string; cta?: string; onCta?: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-6 px-4">
      {icon}
      <p className="text-sm font-semibold text-white/65">{title}</p>
      {hint && <p className="text-[11px] text-white/40 mt-1 max-w-[260px]">{hint}</p>}
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

function EmptyChart({ icon, title, hint, cta, onCta }: {
  icon: React.ReactNode; title: string; hint?: string; cta?: string; onCta?: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-6 px-4 h-32">
      {icon}
      <p className="text-sm font-semibold text-white/65">{title}</p>
      {hint && <p className="text-[11px] text-white/40 mt-1 max-w-[300px]">{hint}</p>}
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

// ═════════════════════════════════════════════════════════════
//   CALENDAR PANEL — version dark-theme du calendrier coaching
// ═════════════════════════════════════════════════════════════
const FRENCH_MONTHS = [
  'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre',
];
const FRENCH_WEEKDAYS_INITIAL = ['L', 'M', 'M', 'J', 'V', 'S', 'D'];

const toISODateLocal = (d: Date): string => {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
};

const subjectHueDot: Record<string, string> = {
  Physique: 'bg-indigo-400',
  Chimie: 'bg-rose-400',
  'Mathématiques': 'bg-amber-400',
  Mathematiques: 'bg-amber-400',
  SVT: 'bg-emerald-400',
};

function CalendarPanel({
  month, setMonth, sessionsByDate, onSelectDay, hasPlan, onCta,
}: {
  month: Date;
  setMonth: (d: Date) => void;
  sessionsByDate: Record<string, any[]>;
  onSelectDay: (date: string) => void;
  hasPlan: boolean;
  onCta: () => void;
}) {
  const today = new Date();
  const todayISO = toISODateLocal(today);
  const year = month.getFullYear();
  const monthIdx = month.getMonth();

  const firstOfMonth = new Date(year, monthIdx, 1);
  const jsWeekday = firstOfMonth.getDay();
  const offset = (jsWeekday + 6) % 7; // Monday-first
  const daysInMonth = new Date(year, monthIdx + 1, 0).getDate();

  const cells: Array<{ date: Date | null; iso: string | null }> = [];
  for (let i = 0; i < offset; i++) cells.push({ date: null, iso: null });
  for (let d = 1; d <= daysInMonth; d++) {
    const date = new Date(year, monthIdx, d);
    cells.push({ date, iso: toISODateLocal(date) });
  }
  while (cells.length % 7 !== 0) cells.push({ date: null, iso: null });

  const totalSessionsThisMonth = Object.entries(sessionsByDate).reduce((acc, [iso, list]) => {
    if (iso.startsWith(`${year}-${String(monthIdx + 1).padStart(2, '0')}`)) {
      return acc + (list?.length || 0);
    }
    return acc;
  }, 0);

  return (
    <div className="glass rounded-2xl overflow-hidden flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-white/5 bg-gradient-to-r from-indigo-600/30 via-purple-600/20 to-cyan-600/20">
        <div className="flex items-center gap-2">
          <Calendar className="w-4 h-4 text-indigo-300" />
          <h3 className="text-sm font-bold text-white">Calendrier</h3>
          {totalSessionsThisMonth > 0 && (
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-200">
              {totalSessionsThisMonth} sessions
            </span>
          )}
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => setMonth(new Date(year, monthIdx - 1, 1))}
            className="w-7 h-7 rounded-lg bg-white/5 hover:bg-white/10 text-white/70 flex items-center justify-center transition"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => setMonth(new Date())}
            className="text-xs font-bold text-white px-2 py-1 rounded-lg hover:bg-white/5 transition tabular-nums"
          >
            {FRENCH_MONTHS[monthIdx]} {year}
          </button>
          <button
            onClick={() => setMonth(new Date(year, monthIdx + 1, 1))}
            className="w-7 h-7 rounded-lg bg-white/5 hover:bg-white/10 text-white/70 flex items-center justify-center transition"
          >
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {!hasPlan ? (
        <div className="p-6">
          <EmptyState
            icon={
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 flex items-center justify-center mb-2 border border-white/5">
                <Calendar className="w-6 h-6 text-indigo-300" />
              </div>
            }
            title="Aucun programme actif"
            hint="Lance ton diagnostic pour générer un calendrier personnalisé jusqu'au BAC."
            cta="Lancer le diagnostic"
            onCta={onCta}
          />
        </div>
      ) : (
        <>
          {/* Weekday row */}
          <div className="grid grid-cols-7 border-b border-white/5">
            {FRENCH_WEEKDAYS_INITIAL.map((d, i) => (
              <div key={i} className="py-1.5 text-center text-[10px] font-bold text-white/40 uppercase">
                {d}
              </div>
            ))}
          </div>

          {/* Day grid */}
          <div className="grid grid-cols-7 p-1.5 gap-0.5">
            {cells.map((cell, i) => {
              if (!cell.date || !cell.iso) {
                return <div key={i} className="h-11" />;
              }
              const daySessions = sessionsByDate[cell.iso] || [];
              const totalSessions = daySessions.length;
              const completed = daySessions.filter((s: any) => s.status === 'completed').length;
              const allDone = totalSessions > 0 && completed === totalSessions;
              const isToday = cell.iso === todayISO;
              const isPast = cell.iso < todayISO;
              const hasContent = totalSessions > 0;

              return (
                <button
                  key={i}
                  onClick={() => hasContent && onSelectDay(cell.iso!)}
                  disabled={!hasContent}
                  className={`relative h-11 flex flex-col items-center justify-center rounded-lg transition-all ${
                    isToday
                      ? 'bg-indigo-500/15 ring-1 ring-indigo-400/40'
                      : hasContent
                        ? 'hover:bg-white/[.06] cursor-pointer'
                        : ''
                  }`}
                >
                  <span
                    className={`text-xs font-semibold leading-none ${
                      isToday
                        ? 'w-6 h-6 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-400 text-white flex items-center justify-center shadow-lg shadow-indigo-500/30'
                        : isPast
                          ? 'text-white/25'
                          : hasContent
                            ? 'text-white'
                            : 'text-white/40'
                    }`}
                  >
                    {cell.date.getDate()}
                  </span>
                  {totalSessions > 0 && (
                    <div className="flex items-center gap-0.5 mt-1">
                      {daySessions.slice(0, 3).map((s: any, idx: number) => {
                        const isDone = s.status === 'completed';
                        const subj = s.subjects?.name_fr || '';
                        const dotClass = isDone ? 'bg-emerald-400' : (subjectHueDot[subj] || 'bg-white/40');
                        return <div key={idx} className={`w-1 h-1 rounded-full ${dotClass}`} />;
                      })}
                      {totalSessions > 3 && <span className="text-[7px] font-bold text-white/40">+</span>}
                    </div>
                  )}
                  {allDone && (
                    <CheckCircle className="absolute top-0.5 right-0.5 w-2.5 h-2.5 text-emerald-400" />
                  )}
                </button>
              );
            })}
          </div>

          {/* Légende */}
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1.5 px-4 py-2.5 border-t border-white/5 text-[10px] text-white/55">
            <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-indigo-400" />PC</span>
            <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-rose-400" />Chimie</span>
            <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-amber-400" />Math</span>
            <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-emerald-400" />Terminé</span>
            <span className="ml-auto text-[10px] text-white/40">Clique sur un jour</span>
          </div>
        </>
      )}
    </div>
  );
}

// ═════════════════════════════════════════════════════════════
//   DAY DETAIL MODAL (dark)
// ═════════════════════════════════════════════════════════════
function DayDetailModal({
  dayISO, sessions, onClose, onStartSession,
}: {
  dayISO: string;
  sessions: any[];
  onClose: () => void;
  onStartSession: (chapterId: string) => void;
}) {
  const date = new Date(dayISO + 'T00:00:00');
  const weekday = date.toLocaleDateString('fr-FR', { weekday: 'long' });
  const dayNum = date.getDate();
  const monthName = FRENCH_MONTHS[date.getMonth()];
  const todayISO = toISODateLocal(new Date());
  const isToday = dayISO === todayISO;
  const totalMin = sessions.reduce((a, s) => a + (s.duration_minutes || 0), 0);
  const completed = sessions.filter((s) => s.status === 'completed').length;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="glass-strong rounded-3xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl shadow-indigo-500/20 border border-white/10 anim-fade-up"
      >
        {/* Header */}
        <div className="bg-gradient-to-br from-indigo-600 via-purple-600 to-cyan-500 p-6 text-white relative overflow-hidden">
          <div className="absolute -top-10 -right-10 w-40 h-40 rounded-full bg-white/20 blur-3xl" />
          <button
            onClick={onClose}
            className="absolute top-4 right-4 w-9 h-9 rounded-xl bg-white/15 hover:bg-white/25 backdrop-blur flex items-center justify-center transition-all"
          >
            <XIcon className="w-5 h-5" />
          </button>
          <div className="relative flex items-end gap-4">
            <div className="bg-white/15 backdrop-blur rounded-2xl p-3 text-center min-w-[80px] border border-white/20">
              <p className="text-xs uppercase tracking-wider font-bold text-white/85">{weekday.slice(0, 3)}</p>
              <p className="text-4xl font-black leading-none mt-1">{dayNum}</p>
              <p className="text-[10px] font-semibold text-white/85 mt-1">{monthName.slice(0, 4).toUpperCase()}</p>
            </div>
            <div className="flex-1 pb-1 min-w-0">
              <p className="text-xs uppercase tracking-wider font-bold text-white/85">
                {isToday ? "Aujourd'hui" : 'Sessions planifiées'}
              </p>
              <h3 className="text-2xl font-black capitalize mt-1 truncate">
                {weekday} {dayNum} {monthName}
              </h3>
              <div className="flex items-center gap-2 mt-2 text-xs flex-wrap">
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
        <div className="flex-1 overflow-y-auto moalim-scroll p-4 space-y-2">
          {sessions.length === 0 ? (
            <div className="text-center py-10 text-white/45 text-sm">Aucune session ce jour-là.</div>
          ) : sessions.map((s) => {
            const subj = s.subjects?.name_fr || '';
            const dot = subjectHueDot[subj] || 'bg-white/40';
            const isDone = s.status === 'completed';
            return (
              <div
                key={s.id}
                className={`flex items-center gap-3 p-3 rounded-xl border transition-colors ${
                  isDone
                    ? 'bg-emerald-500/5 border-emerald-500/20'
                    : 'bg-white/[.04] border-white/10 hover:bg-white/[.07]'
                }`}
              >
                <div className={`w-1.5 h-12 rounded-full ${isDone ? 'bg-emerald-400' : dot}`} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-white truncate">{subj}</span>
                    {isDone && (
                      <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    )}
                  </div>
                  <p className="text-xs text-white/55 truncate">
                    Ch.{s.chapters?.chapter_number} — {s.chapters?.title_fr}
                  </p>
                  <div className="flex items-center gap-2 mt-1 text-[10px] text-white/40">
                    <Clock className="w-3 h-3" />
                    {s.duration_minutes || 0} min
                    {s.scheduled_time && (
                      <>
                        <span>·</span>
                        <span>{s.scheduled_time}</span>
                      </>
                    )}
                  </div>
                </div>
                {!isDone && (
                  <button
                    onClick={() => onStartSession(s.chapter_id)}
                    className="px-3 py-2 rounded-lg bg-gradient-to-r from-indigo-500 to-cyan-500 text-white text-xs font-semibold flex items-center gap-1.5 hover:shadow-lg hover:shadow-indigo-500/40 transition-all flex-shrink-0"
                  >
                    <Play className="w-3 h-3" /> Démarrer
                  </button>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
