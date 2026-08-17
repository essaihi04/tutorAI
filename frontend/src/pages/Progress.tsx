import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ArrowRight,
  BarChart3,
  BookOpenCheck,
  Clock3,
  PenTool,
  Target,
  Trophy,
} from 'lucide-react';
import { getMyExamStats, getProficiency, getProgress, getStudyPlan } from '../services/api';
import { useLearningContextStore } from '../stores/learningContextStore';
import type { LearningSubject } from '../stores/learningContextStore';
import MoalimShell from '../components/MoalimShell';
import StudentNavigation from '../components/StudentNavigation';
import MobileBottomNav from '../components/MobileBottomNav';

type ProgressData = {
  overall_progress?: number;
  subject_progress?: Record<string, number>;
};

type PlanData = { plan?: { progress_percentage?: number } };

type ExamStatsData = {
  avg_score_pct?: number;
  total_duration_seconds?: number;
  total_questions_answered?: number;
  unique_exams_taken?: number;
};

type SkillItem = { subject?: string; topic?: string; name?: string };
type ProficiencyData = {
  lacunes?: SkillItem[];
  strengths?: Array<SkillItem | string>;
  points_forts?: Array<SkillItem | string>;
};
const EMPTY_SUBJECTS: LearningSubject[] = [];

export default function Progress() {
  const navigate = useNavigate();
  const subjects = useLearningContextStore((state) => state.context?.subjects || EMPTY_SUBJECTS);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [plan, setPlan] = useState<PlanData | null>(null);
  const [stats, setStats] = useState<ExamStatsData | null>(null);
  const [proficiency, setProficiency] = useState<ProficiencyData | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      getProgress().catch(() => null),
      getStudyPlan().catch(() => null),
      getMyExamStats().catch(() => null),
      getProficiency().catch(() => null),
    ]).then(([progressResponse, planResponse, statsResponse, proficiencyResponse]) => {
      if (cancelled) return;
      setProgress((progressResponse?.data as ProgressData) || null);
      setPlan((planResponse?.data as PlanData) || null);
      setStats((statsResponse?.data as ExamStatsData) || null);
      setProficiency((proficiencyResponse?.data as ProficiencyData) || null);
      setLoading(false);
    });
    return () => { cancelled = true; };
  }, []);

  const overall = Math.round(Number(progress?.overall_progress ?? plan?.plan?.progress_percentage ?? 0));
  const scoreOn20 = Math.round(Number(stats?.avg_score_pct || 0) * 0.2 * 10) / 10;
  const totalSeconds = Number(stats?.total_duration_seconds || 0);
  const timeLabel = totalSeconds >= 3600
    ? `${Math.floor(totalSeconds / 3600)}h ${Math.floor((totalSeconds % 3600) / 60)}min`
    : `${Math.floor(totalSeconds / 60)}min`;
  const weaknesses = useMemo(() => (proficiency?.lacunes || []).slice(0, 3), [proficiency]);
  const strengths = useMemo(() => (proficiency?.strengths || proficiency?.points_forts || []).slice(0, 3), [proficiency]);

  return (
    <MoalimShell>
      <StudentNavigation active="progress" />
      <main className="mx-auto max-w-6xl space-y-7 px-4 pb-28 pt-7 sm:px-6 lg:px-8 lg:pb-14 lg:pt-12">
        <section>
          <p className="text-xs font-bold uppercase tracking-[0.2em] text-cyan-300/70">Mes progrès</p>
          <h1 className="mt-2 text-3xl font-black tracking-tight text-white sm:text-4xl">Vois l’essentiel, puis passe à l’action</h1>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-white/45">Pas de tableaux compliqués : ta progression, tes résultats et les points à renforcer.</p>
        </section>

        {loading ? (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {[0, 1, 2, 3].map((item) => <div key={item} className="h-28 animate-pulse rounded-2xl bg-white/[0.04]" />)}
          </div>
        ) : (
          <section className="grid grid-cols-2 gap-3 lg:grid-cols-4">
            <StatCard icon={BarChart3} label="Parcours terminé" value={`${overall}%`} color="text-indigo-300 bg-indigo-500/15" />
            <StatCard icon={Trophy} label="Moyenne" value={`${scoreOn20}/20`} color="text-amber-300 bg-amber-500/15" />
            <StatCard icon={PenTool} label="Questions traitées" value={String(stats?.total_questions_answered || 0)} color="text-emerald-300 bg-emerald-500/15" />
            <StatCard icon={Clock3} label="Temps de travail" value={timeLabel} color="text-cyan-300 bg-cyan-500/15" />
          </section>
        )}

        <section className="grid gap-4 lg:grid-cols-[1.25fr_0.75fr]">
          <div className="rounded-3xl border border-white/[0.07] bg-white/[0.035] p-5 sm:p-6">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.18em] text-white/30">Par matière</p>
                <h2 className="mt-1 text-lg font-black text-white">Avancement du parcours</h2>
              </div>
              <span className="rounded-full bg-indigo-500/10 px-3 py-1 text-xs font-bold text-indigo-300">{subjects.length} matière{subjects.length > 1 ? 's' : ''}</span>
            </div>
            <div className="space-y-5">
              {subjects.length > 0 ? subjects.map((subject) => {
                const value = Math.round(Number(progress?.subject_progress?.[subject.id] || 0));
                return (
                  <div key={subject.id}>
                    <div className="mb-2 flex items-center justify-between gap-3 text-sm">
                      <span className="truncate font-bold text-white/80">{subject.icon || '•'} {subject.name_fr}</span>
                      <span className="font-black tabular-nums text-white">{value}%</span>
                    </div>
                    <div className="h-2.5 overflow-hidden rounded-full bg-white/[0.06]">
                      <div className="h-full rounded-full bg-gradient-to-r from-indigo-500 via-violet-500 to-cyan-400 transition-all" style={{ width: `${Math.max(2, Math.min(100, value))}%` }} />
                    </div>
                  </div>
                );
              }) : (
                <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-white/35">Les matières apparaîtront ici dès que ton accès sera configuré.</p>
              )}
            </div>
          </div>

          <div className="rounded-3xl border border-white/[0.07] bg-white/[0.035] p-5 sm:p-6">
            <div className="flex h-full flex-col">
              <span className="flex h-11 w-11 items-center justify-center rounded-2xl bg-rose-500/15 text-rose-300"><Target className="h-5 w-5" /></span>
              <h2 className="mt-4 text-lg font-black text-white">À renforcer maintenant</h2>
              {weaknesses.length > 0 ? (
                <div className="mt-4 space-y-2">
                  {weaknesses.map((item, index) => (
                    <div key={`${item.subject}-${item.topic}-${index}`} className="rounded-xl border border-white/[0.06] bg-black/10 px-3 py-2.5">
                      <p className="truncate text-sm font-bold text-white/75">{item.topic || item.name || 'Point à renforcer'}</p>
                      <p className="mt-0.5 text-[11px] text-white/35">{item.subject || 'Ton parcours personnalisé'}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="mt-4 text-sm leading-6 text-white/40">Fais quelques exercices. Moalim identifiera automatiquement tes priorités.</p>
              )}
              <button onClick={() => navigate('/tutor')} className="mt-auto flex items-center justify-center gap-2 rounded-xl bg-white/[0.07] px-4 py-3 text-xs font-black text-white transition hover:bg-white/[0.11]">
                Travailler avec mon tuteur <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        </section>

        <section className="grid gap-4 sm:grid-cols-2">
          <div className="rounded-2xl border border-emerald-400/10 bg-emerald-500/[0.045] p-5">
            <div className="flex items-center gap-2"><BookOpenCheck className="h-5 w-5 text-emerald-300" /><h2 className="font-black text-white">Tes points forts</h2></div>
            {strengths.length > 0 ? (
              <div className="mt-3 flex flex-wrap gap-2">{strengths.map((item, index) => <span key={index} className="rounded-full bg-emerald-500/10 px-3 py-1.5 text-xs font-semibold text-emerald-200">{typeof item === 'string' ? item : (item.topic || item.name || 'Point fort')}</span>)}</div>
            ) : <p className="mt-3 text-xs leading-5 text-white/35">Ils apparaîtront avec tes prochains résultats.</p>}
          </div>
          <button onClick={() => navigate('/exam')} className="group rounded-2xl border border-amber-400/10 bg-amber-500/[0.045] p-5 text-left transition hover:border-amber-300/25">
            <div className="flex items-center gap-2"><Trophy className="h-5 w-5 text-amber-300" /><h2 className="font-black text-white">Mes résultats d’examens</h2></div>
            <p className="mt-3 text-xs leading-5 text-white/35">{stats?.unique_exams_taken || 0} examen{Number(stats?.unique_exams_taken || 0) > 1 ? 's' : ''} réalisé{Number(stats?.unique_exams_taken || 0) > 1 ? 's' : ''}. Consulte les sujets ou poursuis un examen en cours.</p>
            <span className="mt-4 flex items-center gap-1 text-xs font-black text-amber-300">Voir les examens <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-1" /></span>
          </button>
        </section>
      </main>
      <MobileBottomNav active="progress" />
    </MoalimShell>
  );
}

function StatCard({ icon: Icon, label, value, color }: { icon: typeof BarChart3; label: string; value: string; color: string }) {
  return (
    <div className="rounded-2xl border border-white/[0.07] bg-white/[0.035] p-4 sm:p-5">
      <span className={`flex h-9 w-9 items-center justify-center rounded-xl ${color}`}><Icon className="h-4 w-4" /></span>
      <p className="mt-4 text-2xl font-black text-white">{value}</p>
      <p className="mt-1 text-[11px] font-semibold text-white/35">{label}</p>
    </div>
  );
}
