import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { LucideIcon } from 'lucide-react';
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  ChevronRight,
  FileCheck2,
  GraduationCap,
  MessageCircle,
  PenTool,
  Play,
  Sparkles,
  Trophy,
} from 'lucide-react';
import { getStudyPlan, getTodaySchedule } from '../services/api';
import { useLearningContextStore } from '../stores/learningContextStore';
import type { LearningSubject } from '../stores/learningContextStore';
import MoalimShell from '../components/MoalimShell';
import StudentNavigation from '../components/StudentNavigation';
import MobileBottomNav from '../components/MobileBottomNav';

type TutorMode = {
  icon: LucideIcon;
  title: string;
  description: string;
  hint: string;
  path: string;
  accent: string;
  featured?: boolean;
};

type PendingSession = {
  chapter_id?: string;
  status?: string;
  chapters?: { title_fr?: string };
  subjects?: { name_fr?: string };
};
const EMPTY_SUBJECTS: LearningSubject[] = [];

export default function TutorHub() {
  const navigate = useNavigate();
  const subjects = useLearningContextStore((state) => state.context?.subjects || EMPTY_SUBJECTS);
  const [hasPlan, setHasPlan] = useState(false);
  const [pendingSession, setPendingSession] = useState<PendingSession | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      getStudyPlan().catch(() => null),
      getTodaySchedule().catch(() => null),
    ]).then(([plan, today]) => {
      if (cancelled) return;
      setHasPlan(Boolean(plan?.data?.has_plan));
      const sessions = (today?.data?.sessions || []) as PendingSession[];
      setPendingSession(sessions.find((session) => !['completed', 'skipped'].includes(session.status || '')) || null);
    });
    return () => { cancelled = true; };
  }, []);

  const modes = useMemo<TutorMode[]>(() => [
    {
      icon: BookOpen,
      title: 'Comprendre un cours',
      description: 'Moalim explique le cours étape par étape, vérifie ta compréhension et reprend si nécessaire.',
      hint: pendingSession ? `À continuer : ${pendingSession.chapters?.title_fr || pendingSession.subjects?.name_fr || 'ta séance'}` : 'Cours adapté à ton niveau',
      path: pendingSession?.chapter_id
        ? `/session/${pendingSession.chapter_id}`
        : (hasPlan ? '/coaching/plan' : '/coaching/diagnostic'),
      accent: 'from-indigo-500 to-violet-600',
      featured: true,
    },
    {
      icon: PenTool,
      title: 'Faire des exercices',
      description: 'Choisis un sujet. Le tuteur te laisse chercher, donne un indice et corrige ta méthode.',
      hint: 'Mode entraînement guidé',
      path: '/exam',
      accent: 'from-emerald-500 to-teal-600',
    },
    {
      icon: FileCheck2,
      title: 'Passer un examen',
      description: 'Entraîne-toi avec les examens nationaux, un chronomètre et une note finale.',
      hint: 'Conditions réelles du BAC',
      path: '/exam',
      accent: 'from-amber-500 to-orange-600',
    },
    {
      icon: MessageCircle,
      title: 'Poser une question',
      description: 'Écris ou parle librement. Moalim répond avec le tableau, les schémas et la voix.',
      hint: 'Question libre, réponse immédiate',
      path: '/libre',
      accent: 'from-cyan-500 to-blue-600',
    },
  ], [hasPlan, pendingSession]);

  return (
    <MoalimShell>
      <StudentNavigation active="tutor" />
      <main className="mx-auto max-w-6xl px-4 pb-28 pt-7 sm:px-6 lg:px-8 lg:pb-14 lg:pt-12">
        <section className="text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-cyan-400 shadow-xl shadow-indigo-500/25">
            <GraduationCap className="h-7 w-7 text-white" />
          </div>
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-cyan-300/70">Ton espace unique</p>
          <h1 className="mt-2 text-3xl font-black tracking-tight text-white sm:text-5xl">Que veux-tu faire avec Moalim ?</h1>
          <p className="mx-auto mt-3 max-w-2xl text-sm leading-6 text-white/45 sm:text-base">
            Cours, exercices, questions et examens sont réunis ici. Tu choisis l’objectif, le même tuteur conserve ton parcours.
          </p>

          {subjects.length > 0 && (
            <div className="mt-5 flex flex-wrap justify-center gap-2" aria-label="Matières de l'élève">
              {subjects.map((subject) => (
                <span key={subject.id} className="rounded-full border border-white/[0.08] bg-white/[0.04] px-3 py-1.5 text-xs font-semibold text-white/55">
                  {subject.icon || '•'} {subject.name_fr}
                </span>
              ))}
            </div>
          )}
        </section>

        <section className="mt-10 grid gap-4 md:grid-cols-2">
          {modes.map((mode) => {
            const Icon = mode.icon;
            return (
              <button
                key={mode.title}
                onClick={() => navigate(mode.path)}
                className={`group relative overflow-hidden rounded-[26px] border p-5 text-left transition duration-300 hover:-translate-y-1 sm:p-6 ${
                  mode.featured
                    ? 'border-indigo-400/25 bg-gradient-to-br from-indigo-500/15 via-white/[0.045] to-cyan-500/10 shadow-xl shadow-indigo-950/30'
                    : 'border-white/[0.07] bg-white/[0.035] hover:border-white/15 hover:bg-white/[0.055]'
                }`}
              >
                {mode.featured && (
                  <span className="absolute right-4 top-4 inline-flex items-center gap-1 rounded-full bg-indigo-400/15 px-2.5 py-1 text-[10px] font-black uppercase tracking-wide text-indigo-200">
                    <Sparkles className="h-3 w-3" /> Recommandé
                  </span>
                )}
                <span className={`flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br ${mode.accent} shadow-lg`}>
                  <Icon className="h-5 w-5 text-white" />
                </span>
                <h2 className="mt-5 text-xl font-black text-white">{mode.title}</h2>
                <p className="mt-2 max-w-lg text-sm leading-6 text-white/45">{mode.description}</p>
                <div className="mt-5 flex items-center justify-between gap-3 border-t border-white/[0.06] pt-4">
                  <span className="flex items-center gap-1.5 text-xs font-semibold text-white/35">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" /> {mode.hint}
                  </span>
                  <span className="flex shrink-0 items-center gap-1 text-xs font-black text-cyan-300">
                    Commencer <ChevronRight className="h-4 w-4 transition group-hover:translate-x-1" />
                  </span>
                </div>
              </button>
            );
          })}
        </section>

        <section className="mt-5 grid gap-3 sm:grid-cols-2">
          <button
            onClick={() => navigate('/mock-exam')}
            className="group flex items-center gap-4 rounded-2xl border border-white/[0.07] bg-black/10 p-4 text-left transition hover:border-violet-400/25 hover:bg-violet-500/[0.06]"
          >
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/15 text-violet-300"><Trophy className="h-5 w-5" /></span>
            <span className="min-w-0 flex-1">
              <span className="block text-sm font-bold text-white">Examens blancs générés par IA</span>
              <span className="mt-0.5 block text-xs text-white/35">Une simulation supplémentaire quand tu es prêt.</span>
            </span>
            <ArrowRight className="h-4 w-4 text-white/25 transition group-hover:translate-x-1" />
          </button>
          <button
            onClick={() => navigate('/coaching/plan')}
            className="group flex items-center gap-4 rounded-2xl border border-white/[0.07] bg-black/10 p-4 text-left transition hover:border-cyan-400/25 hover:bg-cyan-500/[0.06]"
          >
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/15 text-cyan-300"><Play className="h-5 w-5" /></span>
            <span className="min-w-0 flex-1">
              <span className="block text-sm font-bold text-white">Voir tout mon programme</span>
              <span className="mt-0.5 block text-xs text-white/35">Retrouve le calendrier seulement quand tu en as besoin.</span>
            </span>
            <ArrowRight className="h-4 w-4 text-white/25 transition group-hover:translate-x-1" />
          </button>
        </section>
      </main>
      <MobileBottomNav active="tutor" />
    </MoalimShell>
  );
}
