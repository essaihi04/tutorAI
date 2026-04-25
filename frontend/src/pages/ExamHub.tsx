import { useState, useEffect, useMemo, useRef, forwardRef } from 'react';
import { useNavigate } from 'react-router-dom';
import html2canvas from 'html2canvas';
import { listExams, listExtractedExams, getMyExamStats, getExamHistory } from '../services/api';
import { useAuthStore } from '../stores/authStore';
import {
  ArrowLeft, Clock, Award, Play, FileText, GraduationCap, Loader2,
  ChevronDown, Info, X, Sparkles, Calendar, Trophy,
  Share2, Check, Copy, Filter, BarChart3, RotateCcw,
} from 'lucide-react';

interface ExamDetail {
  year: number;
  session: string;
}

interface MySubjectStat {
  subject: string;
  exams: number;
  attempts: number;
  in_progress: number;
  questions: number;
  avg_score_pct: number;
  exams_detail: ExamDetail[];
}

interface MyExamStats {
  exams_taken: number;
  attempts: number;
  in_progress_count: number;
  total_questions_answered: number;
  avg_score_pct: number;
  best_score_pct: number;
  total_duration_seconds: number;
  by_subject: MySubjectStat[];
  exams_detail: (ExamDetail & { subject: string })[];
}

interface InProgressAttempt {
  id: string;
  exam_id: string;
  exam_subject: string;
  exam_year: number;
  exam_session: string;
  mode: string;
  current_question_index: number;
  answered_count: number;
  started_at: string;
  in_progress: boolean;
}

interface ExamMeta {
  id: string;
  subject: string;
  subject_full: string;
  year: number;
  session: string;
  duration_minutes: number;
  coefficient: number;
  total_points: number;
  exam_title?: string;
}

interface SubjectCfg {
  label: string;
  icon: string;
  gradient: string;         // tailwind gradient classes
  ring: string;             // focus ring
  soft: string;             // soft bg for chips
  text: string;             // text accent
  pattern: string;          // decorative svg pattern overlay (inline)
}

const SUBJECT_CONFIG: Record<string, SubjectCfg> = {
  SVT: {
    label: 'SVT',
    icon: '🧬',
    gradient: 'from-emerald-500 via-green-500 to-teal-600',
    ring: 'ring-emerald-400',
    soft: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    text: 'text-emerald-700',
    pattern:
      'radial-gradient(circle at 20% 20%, rgba(255,255,255,0.18) 0, transparent 30%), radial-gradient(circle at 80% 70%, rgba(255,255,255,0.12) 0, transparent 35%)',
  },
  'Physique-Chimie': {
    label: 'Physique-Chimie',
    icon: '⚛️',
    gradient: 'from-sky-500 via-blue-500 to-indigo-600',
    ring: 'ring-blue-400',
    soft: 'bg-blue-50 text-blue-700 border-blue-200',
    text: 'text-blue-700',
    pattern:
      'radial-gradient(circle at 10% 30%, rgba(255,255,255,0.18) 0, transparent 32%), radial-gradient(circle at 90% 80%, rgba(255,255,255,0.12) 0, transparent 35%)',
  },
  Mathematiques: {
    label: 'Mathématiques',
    icon: '📐',
    gradient: 'from-purple-500 via-violet-500 to-fuchsia-600',
    ring: 'ring-purple-400',
    soft: 'bg-purple-50 text-purple-700 border-purple-200',
    text: 'text-purple-700',
    pattern:
      'radial-gradient(circle at 25% 75%, rgba(255,255,255,0.18) 0, transparent 30%), radial-gradient(circle at 85% 25%, rgba(255,255,255,0.12) 0, transparent 35%)',
  },
};

const FALLBACK_CFG: SubjectCfg = {
  label: 'Examen',
  icon: '📝',
  gradient: 'from-slate-500 to-slate-700',
  ring: 'ring-slate-400',
  soft: 'bg-slate-50 text-slate-700 border-slate-200',
  text: 'text-slate-700',
  pattern: '',
};

// Normalise the raw session value coming from the backend ("Normale", "normale",
// "Rattrapage", "rattrapage", …) into a canonical display label.
const normalizeSession = (session?: string): 'Normale' | 'Rattrapage' =>
  (session || '').toLowerCase() === 'rattrapage' ? 'Rattrapage' : 'Normale';

type SessionFilter = 'all' | 'Normale' | 'Rattrapage';

export default function ExamHub() {
  const navigate = useNavigate();
  const { student } = useAuthStore();
  const [exams, setExams] = useState<ExamMeta[]>([]);
  const [myStats, setMyStats] = useState<MyExamStats | null>(null);
  const [statsLoading, setStatsLoading] = useState(true);
  const [loading, setLoading] = useState(true);
  const [selectedExam, setSelectedExam] = useState<ExamMeta | null>(null);
  const [filterSubject, setFilterSubject] = useState<string>('');
  const [filterYear, setFilterYear] = useState<number | 'all'>('all');
  const [filterSession, setFilterSession] = useState<SessionFilter>('all');
  const [shareOpen, setShareOpen] = useState(false);
  const [inProgressAttempts, setInProgressAttempts] = useState<InProgressAttempt[]>([]);

  useEffect(() => {
    loadExams();
    loadMyStats();
    loadInProgress();
  }, []);

  const loadMyStats = async () => {
    setStatsLoading(true);
    try {
      const res = await getMyExamStats();
      setMyStats(res.data);
    } catch (e) {
      // Stats panel is optional — silently degrade
      console.warn('Failed to load my exam stats:', e);
    } finally {
      setStatsLoading(false);
    }
  };

  const loadInProgress = async () => {
    try {
      const res = await getExamHistory(50);
      const rows: InProgressAttempt[] = (res.data || []).filter(
        (r: InProgressAttempt) => r.in_progress
      );
      setInProgressAttempts(rows);
    } catch (e) {
      console.warn('Failed to load in-progress attempts:', e);
    }
  };

  const loadExams = async () => {
    setLoading(true);
    try {
      const [legacyRes, extractedRes] = await Promise.all([
        listExams(),
        listExtractedExams(),
      ]);

      const legacyExams = legacyRes.data.exams || [];
      const extractedExams = (extractedRes.data.exams || []).map((exam: Partial<ExamMeta> & { id: string }) => ({
        id: exam.id,
        subject: exam.subject || 'Examen',
        subject_full: exam.exam_title || exam.subject || 'Examen transféré',
        year: exam.year || new Date().getFullYear(),
        session: exam.session || 'normale',
        duration_minutes: exam.duration_minutes || 120,
        coefficient: exam.coefficient || 1,
        total_points: exam.total_points || 20,
        exam_title: exam.exam_title || undefined,
      }));

      const mergedExams = [...legacyExams];
      const existingIds = new Set(legacyExams.map((exam: ExamMeta) => exam.id));

      extractedExams.forEach((exam: ExamMeta) => {
        if (!existingIds.has(exam.id)) {
          mergedExams.push(exam);
        }
      });

      setExams(mergedExams);
    } catch (e) {
      console.error('Failed to load exams:', e);
    } finally {
      setLoading(false);
    }
  };

  const filteredExams = exams.filter((e) => {
    if (filterSubject && e.subject !== filterSubject) return false;
    if (filterYear !== 'all' && Number(e.year) !== filterYear) return false;
    if (filterSession !== 'all' && normalizeSession(e.session) !== filterSession) return false;
    return true;
  });

  const subjects = [...new Set(exams.map((e) => e.subject))];
  const years = [...new Set(exams.map((e) => Number(e.year) || 0))]
    .filter((y) => y > 0)
    .sort((a, b) => b - a);
  const hasRattrapage = exams.some((e) => normalizeSession(e.session) === 'Rattrapage');
  const hasNormale = exams.some((e) => normalizeSession(e.session) === 'Normale');
  const activeFiltersCount =
    (filterSubject ? 1 : 0) + (filterYear !== 'all' ? 1 : 0) + (filterSession !== 'all' ? 1 : 0);

  const getConfig = (subject: string): SubjectCfg =>
    SUBJECT_CONFIG[subject] || FALLBACK_CFG;

  const startMode = (exam: ExamMeta, mode: 'practice' | 'real') => {
    if (mode === 'practice') {
      navigate(`/exam/practice/${exam.id}`);
    } else {
      navigate(`/exam/real/${exam.id}`);
    }
  };

  // Group exams by year (desc), keeping order by session inside a year.
  const groupedByYear = useMemo(() => {
    const m = new Map<number, ExamMeta[]>();
    for (const e of filteredExams) {
      const y = Number(e.year) || 0;
      if (!m.has(y)) m.set(y, []);
      m.get(y)!.push(e);
    }
    // Sort exams inside each year: Normale before Rattrapage, then subject alpha.
    for (const arr of m.values()) {
      arr.sort((a, b) => {
        const sa = normalizeSession(a.session);
        const sb = normalizeSession(b.session);
        if (sa !== sb) return sa === 'Normale' ? -1 : 1;
        return a.subject.localeCompare(b.subject);
      });
    }
    return [...m.entries()].sort(([a], [b]) => b - a);
  }, [filteredExams]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#070718]">
        <Loader2 className="w-8 h-8 text-indigo-400 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#070718] text-white relative overflow-hidden">
      {/* Decorative orbs */}
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute top-0 left-1/3 w-[600px] h-[600px] rounded-full bg-indigo-600/15 blur-[140px] anim-pulse-glow" />
        <div className="absolute bottom-0 right-[10%] w-[500px] h-[500px] rounded-full bg-amber-500/10 blur-[140px] anim-pulse-glow" style={{ animationDelay: '2s' }} />
      </div>
      {/* Header */}
      <header className="relative z-20 backdrop-blur-2xl bg-[#070718]/70 border-b border-white/5 sticky top-0">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate('/dashboard')}
              className="p-2 -ml-2 rounded-lg hover:bg-slate-100 text-slate-500 transition-colors"
              aria-label="Retour"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div className="flex-1 min-w-0">
              <h1 className="text-xl font-bold text-slate-900">Mode Examen</h1>
              <p className="text-sm text-slate-500 truncate">
                Examens Nationaux BAC — Sciences Physiques BIOF
              </p>
            </div>
            <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-100 text-slate-600 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5" /> {exams.length} examens
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-5 space-y-4">
        {/* Compact personal stats bar */}
        <MyExamStatsPanel
          stats={myStats}
          loading={statsLoading}
          getConfig={getConfig}
          onShare={() => setShareOpen(true)}
        />

        {/* In-progress attempts */}
        {inProgressAttempts.length > 0 && (
          <section className="rounded-2xl border border-amber-200 bg-gradient-to-r from-amber-50 via-orange-50 to-yellow-50 p-4">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center text-white shadow-sm">
                <RotateCcw className="w-4 h-4" />
              </div>
              <div>
                <p className="text-sm font-bold text-slate-900">Examens en cours</p>
                <p className="text-[11px] text-slate-500">{inProgressAttempts.length} examen{inProgressAttempts.length > 1 ? 's' : ''} non terminé{inProgressAttempts.length > 1 ? 's' : ''}</p>
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {inProgressAttempts.map((attempt) => {
                const cfg = getConfig(attempt.exam_subject);
                const session = normalizeSession(attempt.exam_session);
                const modeLabel = attempt.mode === 'real' ? 'Examen Réel' : 'Entraînement';
                const startedDate = new Date(attempt.started_at);
                const ago = Math.round((Date.now() - startedDate.getTime()) / 60000);
                const agoLabel = ago < 60 ? `il y a ${ago}min` : ago < 1440 ? `il y a ${Math.round(ago / 60)}h` : `il y a ${Math.round(ago / 1440)}j`;
                const route = attempt.mode === 'real'
                  ? `/exam/real/${attempt.exam_id}`
                  : `/exam/practice/${attempt.exam_id}`;
                return (
                  <button
                    key={attempt.id}
                    onClick={() => navigate(route)}
                    className="flex items-center gap-3 p-3 bg-white rounded-xl border border-amber-200 hover:border-amber-400 hover:shadow-md transition-all text-left group"
                  >
                    <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${cfg.gradient} flex items-center justify-center text-lg shrink-0`}>
                      {cfg.icon}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-bold text-slate-900 truncate">
                        {cfg.label} — {attempt.exam_year} {session}
                      </p>
                      <div className="flex items-center gap-2 text-[10px] text-slate-500 mt-0.5">
                        <span className={`px-1.5 py-0.5 rounded font-semibold ${attempt.mode === 'real' ? 'bg-rose-50 text-rose-600' : 'bg-blue-50 text-blue-600'}`}>
                          {modeLabel}
                        </span>
                        <span>{attempt.answered_count} rép.</span>
                        <span className="text-slate-400">{agoLabel}</span>
                      </div>
                    </div>
                    <span className="text-amber-600 font-bold text-xs group-hover:translate-x-0.5 transition-transform">
                      Continuer →
                    </span>
                  </button>
                );
              })}
            </div>
          </section>
        )}

        {/* Two-column layout: filters sidebar + exam grid */}
        <div className="flex flex-col lg:flex-row gap-4">
          {/* ─── Left sidebar: filters ─── */}
          <aside className="lg:w-64 xl:w-72 shrink-0">
            <div className="lg:sticky lg:top-[73px] space-y-3">
              {/* Filter card */}
              <div className="rounded-2xl border border-slate-200 bg-white p-3 shadow-sm space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1.5 text-slate-600">
                    <Filter className="w-3.5 h-3.5" />
                    <p className="text-[11px] font-bold uppercase tracking-widest">
                      Filtres
                    </p>
                  </div>
                  {activeFiltersCount > 0 && (
                    <button
                      onClick={() => {
                        setFilterSubject('');
                        setFilterYear('all');
                        setFilterSession('all');
                      }}
                      className="inline-flex items-center gap-1 text-[10px] font-semibold text-slate-500 hover:text-slate-900 transition-colors"
                    >
                      <X className="w-3 h-3" />
                      Effacer ({activeFiltersCount})
                    </button>
                  )}
                </div>

                {/* Matière */}
                <div className="space-y-1.5">
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                    Matière
                  </p>
                  <div className="flex flex-col gap-1">
                    <FilterChip
                      active={!filterSubject}
                      onClick={() => setFilterSubject('')}
                      count={exams.length}
                      sidebar
                    >
                      Toutes les matières
                    </FilterChip>
                    {subjects.map((s) => {
                      const cfg = getConfig(s);
                      const count = exams.filter((e) => e.subject === s).length;
                      return (
                        <FilterChip
                          key={s}
                          active={filterSubject === s}
                          onClick={() => setFilterSubject(s)}
                          count={count}
                          icon={cfg.icon}
                          sidebar
                          activeClass={`bg-gradient-to-r ${cfg.gradient} text-white border-transparent shadow-md`}
                        >
                          {cfg.label}
                        </FilterChip>
                      );
                    })}
                  </div>
                </div>

                {/* Année */}
                <div className="space-y-1.5">
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                    Année
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    <FilterChip
                      active={filterYear === 'all'}
                      onClick={() => setFilterYear('all')}
                      compact
                    >
                      Toutes
                    </FilterChip>
                    {years.map((y) => (
                      <FilterChip
                        key={y}
                        active={filterYear === y}
                        onClick={() => setFilterYear(y)}
                        compact
                        activeClass="bg-slate-900 text-white border-slate-900 shadow-sm"
                      >
                        {y}
                      </FilterChip>
                    ))}
                  </div>
                </div>

                {/* Session */}
                <div className="space-y-1.5">
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                    Session
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    <FilterChip
                      active={filterSession === 'all'}
                      onClick={() => setFilterSession('all')}
                      compact
                    >
                      Toutes
                    </FilterChip>
                    {hasNormale && (
                      <FilterChip
                        active={filterSession === 'Normale'}
                        onClick={() => setFilterSession('Normale')}
                        compact
                        icon="🟢"
                        activeClass="bg-gradient-to-r from-emerald-500 to-green-600 text-white border-transparent shadow-sm"
                      >
                        Normale
                      </FilterChip>
                    )}
                    {hasRattrapage && (
                      <FilterChip
                        active={filterSession === 'Rattrapage'}
                        onClick={() => setFilterSession('Rattrapage')}
                        compact
                        icon="🟡"
                        activeClass="bg-gradient-to-r from-amber-500 to-orange-500 text-white border-transparent shadow-sm"
                      >
                        Rattrapage
                      </FilterChip>
                    )}
                  </div>
                </div>
              </div>

              {/* Mode info */}
              <ModeInfoBar />
            </div>
          </aside>

          {/* ─── Right: exam grid ─── */}
          <section className="flex-1 min-w-0">
            {/* Result count bar */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-slate-400" />
                <p className="text-sm text-slate-500">
                  <span className="font-bold text-slate-900">{filteredExams.length}</span>{' '}
                  examen{filteredExams.length !== 1 ? 's' : ''}
                  {activeFiltersCount > 0 && (
                    <span className="text-slate-400"> · filtrés</span>
                  )}
                </p>
              </div>
            </div>

            {/* Exam cards */}
            {filteredExams.length === 0 ? (
              <div className="bg-white rounded-2xl border border-slate-200 p-10 text-center">
                <div className="w-16 h-16 rounded-2xl bg-slate-100 mx-auto mb-3 flex items-center justify-center">
                  <FileText className="w-8 h-8 text-slate-400" />
                </div>
                <h3 className="text-lg font-bold text-slate-700 mb-1">Aucun examen trouvé</h3>
                <p className="text-sm text-slate-500 mb-3">Ajustez vos filtres.</p>
                {activeFiltersCount > 0 && (
                  <button
                    onClick={() => {
                      setFilterSubject('');
                      setFilterYear('all');
                      setFilterSession('all');
                    }}
                    className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 transition-colors"
                  >
                    <X className="w-3.5 h-3.5" />
                    Réinitialiser
                  </button>
                )}
              </div>
            ) : (
              <div className="space-y-6">
                {groupedByYear.map(([year, items]) => (
                  <section key={year}>
                    <div className="flex items-center gap-2 mb-2.5">
                      <Calendar className="w-3.5 h-3.5 text-slate-400" />
                      <h2 className="text-sm font-bold text-slate-900 tracking-tight">{year}</h2>
                      <div className="flex-1 h-px bg-slate-200" />
                      <span className="text-[10px] font-semibold text-slate-400">
                        {items.length} exam.
                      </span>
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-4 gap-2.5">
                      {items.map((exam) => (
                        <ExamCard
                          key={exam.id}
                          exam={exam}
                          cfg={getConfig(exam.subject)}
                          onOpen={() => setSelectedExam(exam)}
                        />
                      ))}
                    </div>
                  </section>
                ))}
              </div>
            )}
          </section>
        </div>
      </main>

      {/* Modal: choose mode */}
      {selectedExam && (
        <ModeModal
          exam={selectedExam}
          cfg={getConfig(selectedExam.subject)}
          onClose={() => setSelectedExam(null)}
          onStart={(mode) => {
            const ex = selectedExam;
            setSelectedExam(null);
            startMode(ex, mode);
          }}
        />
      )}

      {/* Modal: share my exam progress */}
      {shareOpen && myStats && (
        <ExamShareModal
          studentName={student?.full_name || 'Étudiant'}
          stats={myStats}
          onClose={() => setShareOpen(false)}
        />
      )}
    </div>
  );
}

/* ─────────────────────── Sub-components ─────────────────────── */

function FilterChip({
  children,
  active,
  onClick,
  sidebar,
  count,
  icon,
  activeClass,
  compact,
}: {
  children: React.ReactNode;
  active: boolean;
  onClick: () => void;
  count?: number;
  icon?: string;
  activeClass?: string;
  compact?: boolean;
  sidebar?: boolean;
}) {
  const sizing = compact
    ? 'px-2.5 py-1 text-xs gap-1.5'
    : sidebar
      ? 'w-full px-3 py-1.5 text-xs gap-2 justify-between'
      : 'px-3.5 py-2 text-sm gap-2';
  const radius = sidebar ? 'rounded-lg' : 'rounded-full';
  const base = `inline-flex items-center ${sizing} ${radius} font-semibold border transition-all`;
  const inactive =
    'bg-white text-slate-600 border-slate-200 hover:border-slate-300 hover:bg-slate-50';
  const activeDefault = 'bg-slate-900 text-white border-slate-900';
  return (
    <button
      onClick={onClick}
      className={`${base} ${active ? activeClass || activeDefault : inactive}`}
    >
      <span className="inline-flex items-center gap-1.5 min-w-0">
        {icon && <span className={compact ? 'text-sm leading-none' : 'text-base leading-none'}>{icon}</span>}
        <span className="truncate">{children}</span>
      </span>
      {typeof count === 'number' && (
        <span
          className={`text-[10px] font-bold px-1.5 py-0.5 rounded-full shrink-0 ${
            active ? 'bg-white/25 text-white' : 'bg-slate-100 text-slate-500'
          }`}
        >
          {count}
        </span>
      )}
    </button>
  );
}

function ModeInfoBar() {
  const [open, setOpen] = useState(false);
  return (
    <div className="rounded-2xl border border-slate-200 bg-white overflow-hidden">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center gap-3 px-4 py-3 hover:bg-slate-50 transition-colors"
      >
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200 text-xs font-semibold">
            <Play className="w-3 h-3" /> Entraînement
          </span>
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-rose-50 text-rose-700 border border-rose-200 text-xs font-semibold">
            <Clock className="w-3 h-3" /> Examen Réel
          </span>
        </div>
        <span className="hidden sm:block text-sm text-slate-500 truncate">
          Deux modes disponibles — cliquez sur un examen pour choisir
        </span>
        <div className="ml-auto flex items-center gap-1.5 text-xs font-semibold text-slate-500">
          <Info className="w-3.5 h-3.5" />
          {open ? 'Masquer' : 'Détails'}
          <ChevronDown className={`w-4 h-4 transition-transform ${open ? 'rotate-180' : ''}`} />
        </div>
      </button>

      {open && (
        <div className="grid grid-cols-1 md:grid-cols-2 border-t border-slate-200">
          <div className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 border-b md:border-b-0 md:border-r border-slate-200">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 text-white flex items-center justify-center">
                <Play className="w-4 h-4" />
              </div>
              <p className="font-bold text-slate-900">Mode Entraînement</p>
            </div>
            <ul className="text-sm text-slate-600 space-y-1 pl-1">
              <li>• Questions affichées une par une</li>
              <li>• Correction instantanée par l'IA</li>
              <li>• Explication des erreurs</li>
              <li>• Pas de limite de temps</li>
            </ul>
          </div>
          <div className="p-4 bg-gradient-to-br from-rose-50 to-red-50">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-red-500 to-rose-600 text-white flex items-center justify-center">
                <Clock className="w-4 h-4" />
              </div>
              <p className="font-bold text-slate-900">Mode Examen Réel</p>
            </div>
            <ul className="text-sm text-slate-600 space-y-1 pl-1">
              <li>• Toutes les questions visibles</li>
              <li>• Chronomètre avec durée officielle</li>
              <li>• Aucune correction pendant l'examen</li>
              <li>• Note sur 20 à la fin</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

function ExamCard({
  exam,
  cfg,
  onOpen,
}: {
  exam: ExamMeta;
  cfg: SubjectCfg;
  onOpen: () => void;
}) {
  const session = normalizeSession(exam.session);
  const isRattrapage = session === 'Rattrapage';
  return (
    <button
      onClick={onOpen}
      title={`${cfg.label} — ${exam.year} ${session}`}
      className={`group relative text-left rounded-2xl overflow-hidden bg-white shadow-sm hover:shadow-xl hover:-translate-y-0.5 transition-all duration-200 focus:outline-none focus:ring-2 ${cfg.ring}`}
    >
      {/* VIBRANT colored header */}
      <div className={`relative bg-gradient-to-br ${cfg.gradient} overflow-hidden`}>
        {/* Decorative blobs */}
        <div className="absolute -top-6 -right-6 w-20 h-20 rounded-full bg-white/20 blur-xl" />
        <div className="absolute -bottom-4 -left-4 w-16 h-16 rounded-full bg-white/10 blur-lg" />
        {/* Dotted grid overlay */}
        <div
          className="absolute inset-0 opacity-40"
          style={{
            backgroundImage:
              'radial-gradient(circle, rgba(255,255,255,0.25) 1px, transparent 1px)',
            backgroundSize: '10px 10px',
          }}
        />

        <div className="relative px-3 pt-2.5 pb-2">
          <div className="flex items-start justify-between mb-1">
            <span
              className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[8px] font-black uppercase tracking-wider ${
                isRattrapage
                  ? 'bg-amber-300 text-amber-950'
                  : 'bg-white text-slate-900'
              }`}
            >
              <span
                className={`w-1 h-1 rounded-full ${
                  isRattrapage ? 'bg-amber-700' : 'bg-emerald-500'
                }`}
              />
              {isRattrapage ? 'RATT.' : 'NORM.'}
            </span>
            {/* Compact icon */}
            <div className="w-7 h-7 rounded-lg bg-white/25 backdrop-blur border border-white/40 flex items-center justify-center text-base group-hover:scale-110 transition-transform">
              {cfg.icon}
            </div>
          </div>

          {/* Year */}
          <p className="text-2xl font-black text-white leading-none drop-shadow tracking-tight">
            {exam.year}
          </p>
          <p className="text-[10px] font-bold text-white/90 leading-tight mt-0.5 drop-shadow line-clamp-1">
            {cfg.label}
          </p>
        </div>
      </div>

      {/* Body — ultra compact */}
      <div className="p-2.5 bg-white">
        <div className="flex items-center justify-between text-[10px] text-slate-500 mb-2">
          <span className="inline-flex items-center gap-0.5" title={`${exam.duration_minutes} min`}>
            <Clock className="w-2.5 h-2.5" />
            {exam.duration_minutes}m
          </span>
          <span className="inline-flex items-center gap-0.5" title={`Coefficient ${exam.coefficient}`}>
            <Award className="w-2.5 h-2.5" />
            c.{exam.coefficient}
          </span>
          <span className="inline-flex items-center gap-0.5" title={`${exam.total_points} points`}>
            <FileText className="w-2.5 h-2.5" />
            /{exam.total_points}
          </span>
        </div>

        {/* CTA */}
        <div
          className={`flex items-center justify-center gap-1.5 px-2 py-1.5 rounded-lg bg-gradient-to-r ${cfg.gradient} text-white font-bold text-xs group-hover:shadow-md transition-all`}
        >
          <Play className="w-3 h-3 fill-white" />
          <span>Commencer</span>
        </div>
      </div>
    </button>
  );
}

function ModeModal({
  exam,
  cfg,
  onClose,
  onStart,
}: {
  exam: ExamMeta;
  cfg: SubjectCfg;
  onClose: () => void;
  onStart: (mode: 'practice' | 'real') => void;
}) {
  const session = normalizeSession(exam.session);
  return (
    <div
      className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/40 backdrop-blur-sm p-0 sm:p-4 animate-in fade-in"
      onClick={onClose}
    >
      <div
        className="bg-white w-full sm:max-w-lg rounded-t-3xl sm:rounded-3xl overflow-hidden shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className={`relative bg-gradient-to-br ${cfg.gradient} p-5 text-white`}>
          <button
            onClick={onClose}
            className="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-colors"
            aria-label="Fermer"
          >
            <X className="w-4 h-4" />
          </button>
          <p className="text-[10px] font-bold text-white/80 uppercase tracking-widest">
            Examen National {exam.year}
          </p>
          <h3 className="text-xl font-bold mt-0.5">{cfg.label}</h3>
          <p className="text-sm text-white/90 mt-0.5">Session {session}</p>
          <div className="flex items-center gap-3 mt-3 text-xs text-white/85">
            <span className="inline-flex items-center gap-1">
              <Clock className="w-3 h-3" /> {exam.duration_minutes} min
            </span>
            <span className="inline-flex items-center gap-1">
              <Award className="w-3 h-3" /> Coeff. {exam.coefficient}
            </span>
            <span className="inline-flex items-center gap-1">
              <FileText className="w-3 h-3" /> /{exam.total_points} pts
            </span>
          </div>
        </div>

        {/* Body */}
        <div className="p-5 space-y-3">
          <p className="text-sm text-slate-600 font-medium">Choisissez votre mode :</p>
          <button
            onClick={() => onStart('practice')}
            className="w-full flex items-center gap-4 p-4 bg-white rounded-2xl border-2 border-blue-200 hover:border-blue-500 hover:bg-blue-50 transition-all group text-left"
          >
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white flex items-center justify-center">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-bold text-slate-900">Mode Entraînement</p>
              <p className="text-xs text-slate-500">Feedback instantané + corrections IA</p>
            </div>
            <span className="text-blue-500 text-lg transition-transform group-hover:translate-x-0.5">→</span>
          </button>
          <button
            onClick={() => onStart('real')}
            className="w-full flex items-center gap-4 p-4 bg-white rounded-2xl border-2 border-rose-200 hover:border-rose-500 hover:bg-rose-50 transition-all group text-left"
          >
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-red-500 to-rose-600 text-white flex items-center justify-center">
              <Clock className="w-5 h-5" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-bold text-slate-900">Mode Examen Réel</p>
              <p className="text-xs text-slate-500">
                {exam.duration_minutes} min — conditions du BAC
              </p>
            </div>
            <span className="text-rose-500 text-lg transition-transform group-hover:translate-x-0.5">→</span>
          </button>
        </div>
      </div>
    </div>
  );
}

/* ─────────────────────── MyExamStatsPanel ───────────────────
   Compact overview of the student's exam activity with
   year/session detail per subject and share CTA.
   ──────────────────────────────────────────────────────────── */
function MyExamStatsPanel({
  stats,
  loading,
  getConfig,
  onShare,
}: {
  stats: MyExamStats | null;
  loading: boolean;
  getConfig: (subject: string) => SubjectCfg;
  onShare: () => void;
}) {
  if (loading && !stats) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-4 animate-pulse">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-slate-100" />
          <div className="flex-1 space-y-1.5">
            <div className="h-3 w-1/4 bg-slate-100 rounded" />
            <div className="h-2 w-1/3 bg-slate-100 rounded" />
          </div>
        </div>
      </div>
    );
  }

  const hasActivity =
    !!stats &&
    (stats.attempts > 0 ||
      stats.in_progress_count > 0 ||
      stats.total_questions_answered > 0);

  if (!hasActivity) {
    return (
      <section className="rounded-2xl border border-slate-200 bg-gradient-to-r from-indigo-50 via-white to-blue-50 p-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center text-white shadow-sm shrink-0">
            <Trophy className="w-4 h-4" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-bold text-slate-900">
              Passe ton premier examen pour voir tes stats ici 💪
            </p>
            <p className="text-xs text-slate-500 mt-0.5">
              Tes progrès apparaîtront ici et tu pourras les partager avec tes amis.
            </p>
          </div>
        </div>
      </section>
    );
  }

  const s = stats!;
  const scoreEmoji =
    s.avg_score_pct >= 80 ? '🏆' :
    s.avg_score_pct >= 60 ? '🎯' :
    s.avg_score_pct >= 40 ? '📈' : '💪';

  const durationLabel = (() => {
    const sec = s.total_duration_seconds;
    if (sec <= 0) return null;
    const h = Math.floor(sec / 3600);
    const m = Math.floor((sec % 3600) / 60);
    if (h >= 1) return `${h}h${m.toString().padStart(2, '0')}`;
    return `${m} min`;
  })();

  return (
    <section className="rounded-2xl border border-slate-200 bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-900 text-white shadow-md overflow-hidden">
      <div className="p-4">
        {/* Top bar: title + KPIs inline + share */}
        <div className="flex items-center gap-3 mb-3">
          <div className="flex items-center gap-2 min-w-0">
            <BarChart3 className="w-4 h-4 text-indigo-300 shrink-0" />
            <h2 className="text-sm font-bold tracking-tight truncate">
              Mes stats
            </h2>
          </div>
          <div className="flex-1" />
          <button
            onClick={onShare}
            className="shrink-0 inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-white/15 hover:bg-white/25 text-xs font-bold transition-all border border-white/20"
            title="Partager"
          >
            <Share2 className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Partager</span>
          </button>
        </div>

        {/* Compact KPIs row */}
        <div className="grid grid-cols-4 gap-2 mb-3">
          <div className="bg-white/10 rounded-xl px-2.5 py-2 border border-white/10">
            <p className="text-[9px] font-bold text-indigo-300 uppercase tracking-wider">Examens</p>
            <p className="text-lg font-black leading-tight">{s.exams_taken}</p>
            {s.in_progress_count > 0 && (
              <p className="text-[9px] text-amber-300/90">{s.in_progress_count} en cours</p>
            )}
            {!s.in_progress_count && s.attempts > s.exams_taken && (
              <p className="text-[9px] text-indigo-300/70">{s.attempts} tent.</p>
            )}
          </div>
          <div className="bg-white/10 rounded-xl px-2.5 py-2 border border-white/10">
            <p className="text-[9px] font-bold text-indigo-300 uppercase tracking-wider">Questions</p>
            <p className="text-lg font-black leading-tight">{s.total_questions_answered}</p>
          </div>
          <div className="bg-white/10 rounded-xl px-2.5 py-2 border border-white/10">
            <p className="text-[9px] font-bold text-indigo-300 uppercase tracking-wider">Moyenne</p>
            <p className="text-base font-black leading-tight">{scoreEmoji} {s.avg_score_pct}%</p>
          </div>
          <div className="bg-white/10 rounded-xl px-2.5 py-2 border border-white/10">
            <p className="text-[9px] font-bold text-indigo-300 uppercase tracking-wider">Meilleur</p>
            <p className="text-base font-black leading-tight">{s.best_score_pct}%</p>
            {durationLabel && (
              <p className="text-[9px] text-indigo-300/70">⏱ {durationLabel}</p>
            )}
          </div>
        </div>

        {/* Per-subject rows with year/session badges */}
        {s.by_subject.length > 0 && (
          <div className="space-y-1.5">
            {s.by_subject.map((row) => {
              const cfg = getConfig(row.subject);
              return (
                <div
                  key={row.subject}
                  className="flex items-center gap-2 bg-white/8 rounded-lg px-2.5 py-1.5 border border-white/10 hover:bg-white/12 transition-colors"
                >
                  <div
                    className={`w-7 h-7 shrink-0 rounded-lg bg-gradient-to-br ${cfg.gradient} flex items-center justify-center text-sm shadow-sm`}
                  >
                    {cfg.icon}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <p className="text-xs font-bold truncate">{cfg.label}</p>
                      {row.avg_score_pct > 0 && (
                        <span className="text-[10px] text-indigo-300 font-semibold shrink-0">
                          {row.avg_score_pct}%
                        </span>
                      )}
                    </div>
                    {/* Year/session badges */}
                    <div className="flex items-center gap-1 mt-0.5 flex-wrap">
                      {row.exams_detail?.map((ed, i) => (
                        <span
                          key={i}
                          className={`inline-flex items-center gap-0.5 px-1.5 py-0 rounded text-[9px] font-semibold ${
                            (ed.session || '').toLowerCase() === 'rattrapage'
                              ? 'bg-amber-400/20 text-amber-200'
                              : 'bg-emerald-400/20 text-emerald-200'
                          }`}
                        >
                          {ed.year}
                          <span className="opacity-70">
                            {(ed.session || '').toLowerCase() === 'rattrapage' ? 'R' : 'N'}
                          </span>
                        </span>
                      ))}
                      <span className="text-[9px] text-indigo-300/60 ml-1">
                        {row.questions}q
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}

/* ─────────────────────── ExamShareModal ──────────────────────
   Image-first share modal. Renders a beautiful "shareable card" at
   a fixed size (1080×1080), captures it to PNG via html2canvas and
   shares it through the Web Share API (files). Fallback: download
   the image + prefilled network links where the clickable URL
   points to https://moalim.online.
   ──────────────────────────────────────────────────────────── */
const MOALIM_URL = 'https://moalim.online';

function ExamShareModal({
  studentName,
  stats,
  onClose,
}: {
  studentName: string;
  stats: MyExamStats;
  onClose: () => void;
}) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [generating, setGenerating] = useState(false);
  const [downloaded, setDownloaded] = useState(false);
  const [copied, setCopied] = useState(false);
  const [fileShareUnsupported, setFileShareUnsupported] = useState(false);

  const scoreEmoji =
    stats.avg_score_pct >= 80 ? '🏆' :
    stats.avg_score_pct >= 60 ? '🎯' :
    stats.avg_score_pct >= 40 ? '📈' : '💪';

  const shareText =
    `🎓 ${studentName} progresse sur معلم (Moalim) ! ${scoreEmoji}\n` +
    `✅ ${stats.exams_taken} examens BAC passés\n` +
    `📝 ${stats.total_questions_answered} questions répondues\n` +
    `🎯 Moyenne : ${stats.avg_score_pct}%` +
    (stats.best_score_pct > stats.avg_score_pct
      ? ` (meilleur ${stats.best_score_pct}%)`
      : '') +
    `\n\n👉 Rejoins-moi sur ${MOALIM_URL}`;

  const shareTextShort =
    `🎓 ${studentName} : ${stats.exams_taken} examens BAC passés · ` +
    `${stats.total_questions_answered} questions · moyenne ${stats.avg_score_pct}% ${scoreEmoji} — ${MOALIM_URL}`;

  const encodedText = encodeURIComponent(shareText);
  const encodedShort = encodeURIComponent(shareTextShort);
  const encodedUrl = encodeURIComponent(MOALIM_URL);

  // ── Generate PNG blob from the shareable card ──────────────
  const generatePng = async (): Promise<Blob | null> => {
    if (!cardRef.current) return null;
    const canvas = await html2canvas(cardRef.current, {
      backgroundColor: null,
      scale: 2,
      useCORS: true,
      logging: false,
    });
    return await new Promise<Blob | null>((resolve) =>
      canvas.toBlob((blob) => resolve(blob), 'image/png', 1)
    );
  };

  const safeName = studentName.replace(/\s+/g, '_').replace(/[^\w-]/g, '');
  const fileName = `ma-progression-bac-${safeName || 'eleve'}.png`;

  // ── Native share (Web Share API Level 2 with files) ────────
  const shareNative = async () => {
    setGenerating(true);
    setFileShareUnsupported(false);
    try {
      const blob = await generatePng();
      if (!blob) return;
      const file = new File([blob], fileName, { type: 'image/png' });
      const nav: any = navigator;
      const shareData: any = {
        title: 'معلم — Ma progression',
        text: shareTextShort,
        url: MOALIM_URL,
        files: [file],
      };
      if (nav.canShare && nav.canShare({ files: [file] })) {
        await nav.share(shareData);
        onClose();
      } else {
        // Desktop / unsupported → download + show notice
        await downloadImage(blob);
        setFileShareUnsupported(true);
      }
    } catch (e) {
      // User cancelled or error
      console.warn('Share failed:', e);
    } finally {
      setGenerating(false);
    }
  };

  // ── Download PNG locally ───────────────────────────────────
  const downloadImage = async (preBlob?: Blob) => {
    const blob = preBlob ?? (await generatePng());
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 4000);
    setDownloaded(true);
    setTimeout(() => setDownloaded(false), 2500);
  };

  const handleDownload = async () => {
    setGenerating(true);
    try {
      await downloadImage();
    } finally {
      setGenerating(false);
    }
  };

  const copyText = async () => {
    try {
      await navigator.clipboard.writeText(shareText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      window.prompt('Copie ce message :', shareText);
    }
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
      url: 'https://www.tiktok.com/',
    },
  ];

  // Click on a network button → copy text + download image (so user can paste
  // both in the network app/tab that opens), then open the network URL.
  const handleNetworkClick = async (
    e: React.MouseEvent<HTMLAnchorElement>,
    net: { name: string; url: string }
  ) => {
    e.preventDefault();
    try {
      await navigator.clipboard.writeText(shareText);
    } catch { /* no-op */ }
    await downloadImage();
    window.open(net.url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 overflow-y-auto"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden my-4"
      >
        {/* Header */}
        <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-900 px-6 py-5 text-white">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="text-xl font-bold">Partager mon image</h3>
              <p className="text-sm text-indigo-100 mt-1">
                Ta carte de progression avec ton nom et tes stats {scoreEmoji}
              </p>
            </div>
            <button
              onClick={onClose}
              className="p-1 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Shareable card preview — captured to PNG via html2canvas */}
        <div className="px-4 pt-4 pb-2">
          <a
            href={MOALIM_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="block rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow"
            title={`Ouvrir ${MOALIM_URL}`}
          >
            <ShareableCard
              ref={cardRef}
              studentName={studentName}
              stats={stats}
              scoreEmoji={scoreEmoji}
            />
          </a>
          <p className="text-[10px] text-center text-slate-400 mt-2">
            🖼 Aperçu — l'image partagée redirige vers{' '}
            <span className="font-semibold text-indigo-600">moalim.online</span>
          </p>
        </div>

        {/* Primary: native share with FILE */}
        <div className="px-6 pt-2 pb-2 space-y-2">
          <button
            onClick={shareNative}
            disabled={generating}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-indigo-600 to-blue-700 text-white rounded-xl text-sm font-bold hover:shadow-lg transition-all disabled:opacity-60"
          >
            {generating ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Génération…
              </>
            ) : (
              <>
                <Share2 className="w-4 h-4" />
                Partager mon image
              </>
            )}
          </button>
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={handleDownload}
              disabled={generating}
              className="flex items-center justify-center gap-1.5 px-3 py-2 bg-white border-2 border-slate-200 text-slate-700 rounded-xl text-xs font-semibold hover:border-indigo-400 hover:text-indigo-600 transition-colors disabled:opacity-60"
            >
              {downloaded ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-600" />
                  <span className="text-emerald-600">Téléchargée</span>
                </>
              ) : (
                <>📥 Télécharger l'image</>
              )}
            </button>
            <button
              onClick={copyText}
              className="flex items-center justify-center gap-1.5 px-3 py-2 bg-white border-2 border-slate-200 text-slate-700 rounded-xl text-xs font-semibold hover:border-indigo-400 hover:text-indigo-600 transition-colors"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-600" />
                  <span className="text-emerald-600">Texte copié</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  Copier le texte
                </>
              )}
            </button>
          </div>

          {fileShareUnsupported && (
            <p className="text-[11px] text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 flex items-center gap-2">
              <Check className="w-3.5 h-3.5 flex-shrink-0" />
              Image téléchargée ! Ton navigateur ne supporte pas le partage
              de fichier — joins-la manuellement à ton post.
            </p>
          )}
        </div>

        {/* Social networks — copy text + download image + open network */}
        <div className="px-6 py-4">
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
            Ou directement sur un réseau
          </p>
          <p className="text-[10px] text-slate-400 mb-3">
            Le texte est copié et l'image téléchargée — joins-la à ton post.
          </p>
          <div className="grid grid-cols-5 gap-2">
            {networks.map((net) => (
              <a
                key={net.name}
                href={net.url}
                onClick={(e) => handleNetworkClick(e, net)}
                target="_blank"
                rel="noopener noreferrer"
                className={`flex flex-col items-center gap-1.5 p-2.5 rounded-xl ${net.color} text-white transition-all hover:shadow-md`}
                title={`Partager sur ${net.name}`}
              >
                {net.logo}
                <span className="text-[10px] font-medium">{net.name}</span>
              </a>
            ))}
          </div>
        </div>

        {/* moalim.online CTA */}
        <div className="px-6 pb-6">
          <a
            href={MOALIM_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 border-2 border-indigo-200 rounded-xl text-sm font-semibold text-indigo-700 hover:bg-indigo-50 transition-colors"
          >
            <span>👉 Visiter moalim.online</span>
          </a>
        </div>
      </div>
    </div>
  );
}

/* ─────────────────────── ShareableCard ───────────────────────
   Captured to PNG by html2canvas. Uses fixed pixel sizing (not %)
   so the exported image always has a consistent layout regardless
   of viewport. The whole card is wrapped in a link to moalim.online
   in the modal preview.
   ──────────────────────────────────────────────────────────── */
const ShareableCard = forwardRef<
  HTMLDivElement,
  {
    studentName: string;
    stats: MyExamStats;
    scoreEmoji: string;
  }
>(function ShareableCardImpl({ studentName, stats, scoreEmoji }, ref) {
  const best = stats.best_score_pct > stats.avg_score_pct ? stats.best_score_pct : null;
  return (
    <div
      ref={ref}
      style={{
        width: 480,
        fontFamily:
          'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 45%, #3730a3 100%)',
        color: 'white',
        padding: 24,
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* decorative blobs (rendered as pseudo-elements aren't captured — use divs) */}
      <div
        style={{
          position: 'absolute',
          top: -60,
          right: -50,
          width: 220,
          height: 220,
          borderRadius: '50%',
          background: 'rgba(99,102,241,0.35)',
          filter: 'blur(70px)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          bottom: -60,
          left: -40,
          width: 200,
          height: 200,
          borderRadius: '50%',
          background: 'rgba(59,130,246,0.25)',
          filter: 'blur(70px)',
        }}
      />

      {/* Top row — brand + url */}
      <div
        style={{
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: 18,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div
            style={{
              width: 36,
              height: 36,
              borderRadius: 10,
              background: 'linear-gradient(135deg, #3b82f6, #6366f1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 18,
              fontWeight: 900,
            }}
          >
            🎓
          </div>
          <div style={{ lineHeight: 1 }}>
            <div style={{ fontSize: 22, fontWeight: 900, letterSpacing: 0, fontFamily: "'Cairo', system-ui, sans-serif" }}>
              معلم
            </div>
            <div style={{ fontSize: 10, color: '#c7d2fe', marginTop: 3 }}>
              Sciences Physiques · 2026
            </div>
          </div>
        </div>
        <div
          style={{
            fontSize: 11,
            fontWeight: 700,
            color: 'white',
            background: 'rgba(255,255,255,0.14)',
            border: '1px solid rgba(255,255,255,0.2)',
            padding: '4px 10px',
            borderRadius: 999,
          }}
        >
          moalim.online
        </div>
      </div>

      {/* Student name */}
      <div style={{ position: 'relative', marginBottom: 14 }}>
        <div
          style={{
            fontSize: 10,
            fontWeight: 800,
            letterSpacing: 3,
            textTransform: 'uppercase',
            color: '#a5b4fc',
            marginBottom: 4,
          }}
        >
          Ma progression
        </div>
        <div
          style={{
            fontSize: 28,
            fontWeight: 900,
            letterSpacing: -0.8,
            lineHeight: 1.05,
          }}
        >
          {studentName}
        </div>
      </div>

      {/* 3 KPIs row */}
      <div
        style={{
          position: 'relative',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr 1fr',
          gap: 8,
          marginBottom: 14,
        }}
      >
        <KpiBox label="Examens" value={String(stats.exams_taken)} />
        <KpiBox
          label="Questions"
          value={String(stats.total_questions_answered)}
        />
        <KpiBox
          label="Moyenne"
          value={`${scoreEmoji} ${stats.avg_score_pct}%`}
          small
        />
      </div>

      {/* Per-subject (top 3) */}
      {stats.by_subject.length > 0 && (
        <div
          style={{
            position: 'relative',
            display: 'flex',
            flexDirection: 'column',
            gap: 6,
            marginBottom: 14,
          }}
        >
          {stats.by_subject.slice(0, 3).map((s) => (
            <div
              key={s.subject}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                background: 'rgba(255,255,255,0.09)',
                border: '1px solid rgba(255,255,255,0.14)',
                borderRadius: 10,
                padding: '8px 12px',
              }}
            >
              <div style={{ fontSize: 13, fontWeight: 700 }}>
                {s.subject}
              </div>
              <div
                style={{
                  fontSize: 11,
                  color: '#c7d2fe',
                  fontWeight: 600,
                }}
              >
                {s.exams} exam · {s.questions} q
                {s.avg_score_pct > 0 ? ` · ${s.avg_score_pct}%` : ''}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Best score highlight */}
      {best !== null && (
        <div
          style={{
            position: 'relative',
            fontSize: 11,
            color: '#fde68a',
            marginBottom: 12,
            textAlign: 'center',
            fontWeight: 700,
          }}
        >
          🏅 Meilleur score : {best}%
        </div>
      )}

      {/* CTA strip */}
      <div
        style={{
          position: 'relative',
          background: 'rgba(255,255,255,0.95)',
          color: '#1e1b4b',
          borderRadius: 12,
          padding: '12px 14px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 10,
        }}
      >
        <div style={{ lineHeight: 1.2 }}>
          <div style={{ fontSize: 10, color: '#6366f1', fontWeight: 800, letterSpacing: 1.5, textTransform: 'uppercase' }}>
            Rejoins-moi
          </div>
          <div style={{ fontSize: 15, fontWeight: 900 }}>moalim.online</div>
        </div>
        <div
          style={{
            fontSize: 12,
            fontWeight: 800,
            color: 'white',
            background: 'linear-gradient(135deg, #4f46e5, #2563eb)',
            padding: '8px 14px',
            borderRadius: 999,
          }}
        >
          Clique pour voir →
        </div>
      </div>
    </div>
  );
});

function KpiBox({
  label,
  value,
  small,
}: {
  label: string;
  value: string;
  small?: boolean;
}) {
  return (
    <div
      style={{
        background: 'rgba(255,255,255,0.10)',
        border: '1px solid rgba(255,255,255,0.16)',
        borderRadius: 12,
        padding: '10px 10px 12px',
      }}
    >
      <div
        style={{
          fontSize: 9,
          fontWeight: 800,
          letterSpacing: 1.5,
          textTransform: 'uppercase',
          color: '#a5b4fc',
          marginBottom: 4,
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: small ? 18 : 24,
          fontWeight: 900,
          letterSpacing: -0.5,
          lineHeight: 1,
        }}
      >
        {value}
      </div>
    </div>
  );
}

