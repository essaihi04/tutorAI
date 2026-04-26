import { useState, useEffect, useMemo, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCoachingStore } from '../stores/coachingStore';
import { getSubjects, startDiagnosticSession, nextDiagnosticQuestion, submitDiagnostic, generatePlan } from '../services/api';
import LatexRenderer from '../components/LatexRenderer';
import {
  ArrowLeft, ArrowRight, CheckCircle, Loader2, Brain, BarChart3, Sparkles,
  FileText, CheckCheck, HelpCircle, Check, X as XIcon,
  BookOpen, ShieldCheck, Heart, Coffee, Lightbulb
} from 'lucide-react';

// ── Custom dropdown that supports LaTeX rendering inside options ──
// (Native <select><option> cannot render JSX, so we build our own.)
const LatexDropdown = ({
  value,
  options,
  onChange,
  placeholder = 'Choisir…',
}: {
  value: string;
  options: string[];
  onChange: (v: string) => void;
  placeholder?: string;
}) => {
  const [open, setOpen] = useState(false);
  const wrapRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!open) return;
    const onDoc = (e: MouseEvent) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false); };
    document.addEventListener('mousedown', onDoc);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDoc);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  return (
    <div ref={wrapRef} className="relative flex-1">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className={`w-full p-3 rounded-lg border-2 transition-all flex items-center justify-between gap-2 text-sm ${
          value
            ? 'border-blue-400/40 bg-blue-500/10 text-white'
            : 'border-white/10 bg-white/[.04] text-white/55 hover:border-white/20 hover:bg-white/[.06]'
        }`}
        aria-haspopup="listbox"
        aria-expanded={open}
      >
        <span className="flex-1 text-left truncate">
          {value ? <LatexRenderer content={value} /> : <span className="italic">{placeholder}</span>}
        </span>
        <ArrowRight className={`w-4 h-4 transition-transform ${open ? 'rotate-90' : 'rotate-90 opacity-50'}`} />
      </button>
      {open && (
        <div
          role="listbox"
          className="absolute left-0 right-0 mt-1 z-30 rounded-lg border border-white/10 bg-[#0e1024] shadow-2xl shadow-black/40 max-h-64 overflow-y-auto anim-card-in"
        >
          {options.map((opt, i) => {
            const isSelected = opt === value;
            return (
              <button
                key={i}
                type="button"
                role="option"
                aria-selected={isSelected}
                onClick={() => { onChange(opt); setOpen(false); }}
                className={`w-full text-left p-3 text-sm border-b border-white/5 last:border-b-0 transition-colors flex items-center gap-2 ${
                  isSelected
                    ? 'bg-blue-600/30 text-white'
                    : 'text-white/85 hover:bg-white/[.06]'
                }`}
              >
                {isSelected && <Check className="w-3.5 h-3.5 text-blue-300 flex-shrink-0" />}
                <span className="flex-1 min-w-0"><LatexRenderer content={opt} /></span>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

// Association question component
const AssociationQuestion = ({ q, answer, onChange }: { q: Question; answer: Record<string, string>; onChange: (m: Record<string, string>) => void }) => {
  if (!q.pairs) return null;
  const pairs = q.pairs as Array<{ left: string; right: string }>;
  const allRights = pairs.map((p) => p.right);

  const handleSelect = (left: string, right: string) => {
    onChange({ ...answer, [left]: right });
  };

  return (
    <div className="space-y-3">
      {pairs.map((pair, idx) => (
        <div key={idx} className="flex items-center gap-3">
          <div className="flex-1 p-3 rounded-lg bg-white/[.04] border border-white/10">
            <span className="text-sm text-white"><LatexRenderer content={pair.left} /></span>
          </div>
          <span className="text-white/40 text-lg">→</span>
          <LatexDropdown
            value={answer[pair.left] || ''}
            options={allRights}
            onChange={(v) => handleSelect(pair.left, v)}
          />
        </div>
      ))}
    </div>
  );
};

interface Subject {
  id: string;
  name_fr: string;
  name_ar: string;
  icon: string;
}

// Map lucide/text icon names stored in DB to a friendly emoji.
// If the value is already an emoji we return it as-is.
const SUBJECT_EMOJI: Record<string, string> = {
  calculator: '🧮',
  math: '🧮',
  mathematiques: '🧮',
  physics: '⚛️',
  physique: '⚛️',
  atom: '⚛️',
  flask: '🧪',
  chimie: '🧪',
  beaker: '🧪',
  dna: '🧬',
  svt: '🧬',
  leaf: '🌿',
  microscope: '🔬',
  book: '📘',
  history: '📜',
  globe: '🌍',
  language: '🗣️',
};

const subjectIcon = (raw: string | undefined): string => {
  if (!raw) return '📘';
  const v = raw.trim();
  // If first char is non-letter (likely already an emoji or symbol), keep it.
  if (v && !/^[a-zA-Z]/.test(v)) return v;
  return SUBJECT_EMOJI[v.toLowerCase()] || '📘';
};

interface AssocPair { left: string; right: string }

interface Question {
  question: string;
  options: string[];
  correct_answer: string;
  topic: string;
  difficulty: string;
  type?: 'qcm' | 'vrai_faux' | 'association';
  pairs?: AssocPair[];
  bac_year?: string;
  domain?: string;
  grounded_in?: string;
}

type Phase = 'intro' | 'preloading' | 'quiz' | 'submitting' | 'results' | 'generating';

export default function DiagnosticQuiz() {
  const navigate = useNavigate();
  const { addDiagnosticResult, setAllDiagnosticsCompleted } = useCoachingStore();

  const [phase, setPhase] = useState<Phase>('intro');
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [currentSubjectIndex, setCurrentSubjectIndex] = useState(0);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  // New state for question-by-question generation
  const [subjectSessionIds, setSubjectSessionIds] = useState<Record<string, string>>({});
  const [subjectQuestions, setSubjectQuestions] = useState<Record<string, Question[]>>({});
  const [answers, setAnswers] = useState<Record<string, Record<string, any>>>({});
  const [error, setError] = useState<string | null>(null);
  const [subjectScores, setSubjectScores] = useState<Record<string, number>>({});
  const [preloadDone, setPreloadDone] = useState(0);
  // Tracks in-flight preloads per subject to avoid duplicate concurrent calls
  const preloadingRef = useRef<Set<string>>(new Set());
  const TOTAL_QUESTIONS = 10;

  useEffect(() => {
    (async () => {
      try {
        const res = await getSubjects();
        setSubjects(res.data);
      } catch {
        setError('Impossible de charger les matières');
      }
    })();
  }, []);

  // Preload next question in background for ALL subjects in parallel
  // Priority: current subject first, then others
  useEffect(() => {
    if (phase !== 'quiz') return;

    const triggerPreload = (subjectId: string) => {
      const sessionId = subjectSessionIds[subjectId];
      if (!sessionId) return;
      const existing = subjectQuestions[subjectId] || [];
      if (existing.length >= TOTAL_QUESTIONS) return;
      if (preloadingRef.current.has(subjectId)) return;

      preloadingRef.current.add(subjectId);
      nextDiagnosticQuestion(sessionId)
        .then((qRes) => {
          if (qRes.data.question && !qRes.data.completed) {
            setSubjectQuestions((prev) => {
              const cur = prev[subjectId] || [];
              if (cur.length >= TOTAL_QUESTIONS) return prev;
              return { ...prev, [subjectId]: [...cur, qRes.data.question] };
            });
          }
        })
        .catch((e) => console.error('Failed to preload question for', subjectId, e))
        .finally(() => {
          preloadingRef.current.delete(subjectId);
        });
    };

    // 1. Priority: current subject
    const currentSubject = subjects[currentSubjectIndex];
    if (currentSubject) triggerPreload(currentSubject.id);

    // 2. In parallel: all other subjects (including those not yet reached)
    subjects.forEach((s, idx) => {
      if (idx !== currentSubjectIndex) {
        triggerPreload(s.id);
      }
    });
  }, [currentQuestionIndex, currentSubjectIndex, subjectSessionIds, subjectQuestions, subjects, phase]);

  const startFullDiagnostic = async () => {
    if (!subjects.length) return;
    setError(null);
    setPhase('preloading');
    setPreloadDone(0);
    setSubjectQuestions({});
    setSubjectSessionIds({});
    setAnswers({});
    setSubjectScores({});
    setCurrentSubjectIndex(0);
    setCurrentQuestionIndex(0);
    preloadingRef.current.clear();

    let firstReady = false;
    let anyError = false;

    // Start ALL subject sessions in parallel + generate first question for each
    await Promise.all(
      subjects.map(async (subj) => {
        try {
          const res = await startDiagnosticSession(subj.id, 10);
          const sessionId = res.data.session_id;
          setSubjectSessionIds((prev) => ({
            ...prev,
            [subj.id]: sessionId,
          }));

          // Generate first question immediately (in parallel with other subjects)
          const qRes = await nextDiagnosticQuestion(sessionId);
          if (qRes.data.question) {
            setSubjectQuestions((prev) => ({
              ...prev,
              [subj.id]: [qRes.data.question],
            }));
            setPreloadDone((c) => c + 1);

            // Enter quiz as soon as FIRST subject has its first question ready
            if (!firstReady) {
              firstReady = true;
              setPhase('quiz');
            }
          }
        } catch (e) {
          console.error('Failed to start session for subject', subj.id, e);
          anyError = true;
        }
      })
    );

    if (!firstReady && anyError) {
      setError("Les matières n'ont pas pu être générées. Réessaye.");
      setPhase('intro');
    }
  };

  const currentSubject = subjects[currentSubjectIndex];
  const currentQuestions: Question[] = currentSubject ? subjectQuestions[currentSubject.id] || [] : [];
  const currentAnswers = currentSubject ? answers[currentSubject.id] || {} : {};
  const currentQ = currentQuestions[currentQuestionIndex];

  const answeredCount = useMemo(() => {
    return currentQuestions.reduce((acc, q, i) => {
      const a = currentAnswers[String(i)];
      if (q.type === 'association') {
        const filled = a && typeof a === 'object' ? Object.values(a).filter(Boolean).length : 0;
        return acc + (filled >= (q.pairs?.length || 0) ? 1 : 0);
      }
      return acc + (a ? 1 : 0);
    }, 0);
  }, [currentQuestions, currentAnswers]);

  const setAnswerAt = (qIndex: number, value: any) => {
    if (!currentSubject) return;
    setAnswers((prev) => ({
      ...prev,
      [currentSubject.id]: { ...(prev[currentSubject.id] || {}), [String(qIndex)]: value },
    }));
  };

  const submitCurrentSubject = async () => {
    if (!currentSubject) return;
    setPhase('submitting');
    try {
      const res = await submitDiagnostic(currentSubject.id, currentQuestions, currentAnswers);
      addDiagnosticResult(currentSubject.id, res.data);
      const scoreNum = Number(res.data?.score ?? 0);
      setSubjectScores((prev) => ({ ...prev, [currentSubject.name_fr]: isFinite(scoreNum) ? scoreNum : 0 }));

      if (currentSubjectIndex >= subjects.length - 1) {
        setAllDiagnosticsCompleted(true);
        setPhase('results');
      } else {
        setCurrentSubjectIndex(currentSubjectIndex + 1);
        setCurrentQuestionIndex(0);
        setPhase('quiz');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    } catch (e: any) {
      setError(e.response?.data?.detail || "Erreur lors de l'évaluation");
      setPhase('quiz');
    }
  };

  const handleGeneratePlan = async () => {
    setPhase('generating');
    try {
      await generatePlan(subjectScores);
      await new Promise((r) => setTimeout(r, 500));
      navigate('/coaching/plan', { replace: true, state: { refresh: Date.now() } });
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Erreur lors de la génération du plan');
      setPhase('results');
    }
  };

  // ── Render helpers ──
  const difficultyBadge = (d: string) => {
    switch (d?.toLowerCase()) {
      case 'facile': return 'bg-emerald-500/15 text-emerald-200 border-emerald-400/30';
      case 'moyen': return 'bg-amber-500/15 text-amber-200 border-amber-400/30';
      case 'difficile': return 'bg-rose-500/15 text-rose-200 border-rose-400/30';
      default: return 'bg-white/5 text-white/70 border-white/10';
    }
  };

  // ══ PHASE: INTRO ══
  if (phase === 'intro') {
    return (
      <div className="min-h-screen bg-[#070718] text-white p-6 flex items-center relative overflow-hidden">
        <div className="max-w-3xl mx-auto w-full">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 text-white/70 hover:text-white mb-8 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" /> Retour au Dashboard
          </button>

          <div className="glass-strong rounded-3xl shadow-xl p-8 sm:p-10 overflow-hidden relative">
            <div className="absolute -top-24 -right-24 w-72 h-72 bg-gradient-to-br from-blue-400/25 to-indigo-500/25 rounded-full blur-3xl pointer-events-none" />
            <div className="absolute -bottom-24 -left-24 w-72 h-72 bg-gradient-to-tr from-purple-400/20 to-pink-400/20 rounded-full blur-3xl pointer-events-none" />

            <div className="relative">
              {/* Hero icon + welcome chip */}
              <div className="flex items-center gap-3 mb-5">
                <div className="inline-flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-3xl shadow-lg shadow-blue-500/30">
                  <Brain className="w-8 h-8 sm:w-10 sm:h-10 text-white" />
                </div>
                <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-400/30 text-emerald-200 text-xs font-semibold">
                  <Heart className="w-3.5 h-3.5" />
                  Pas de stress, c'est sans pénalité
                </span>
              </div>

              <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight leading-tight">
                On apprend à <span className="bg-gradient-to-r from-blue-300 to-indigo-300 bg-clip-text text-transparent">te connaître</span> !
              </h1>
              <p className="text-white/75 mt-3 text-base sm:text-lg leading-relaxed">
                Avant de te proposer un programme sur-mesure, on va découvrir <span className="font-semibold text-white">tes points forts</span> et tes axes de progrès dans
                {' '}<span className="font-semibold text-indigo-200">tes {subjects.length} matières</span>.
              </p>

              {/* Reassurance row */}
              <div className="grid sm:grid-cols-2 gap-3 mt-6">
                <div className="flex items-start gap-3 p-3.5 rounded-2xl bg-white/[.04] border border-white/10">
                  <div className="w-8 h-8 rounded-lg bg-blue-500/15 text-blue-200 flex items-center justify-center flex-shrink-0">
                    <BookOpen className="w-4 h-4" />
                  </div>
                  <div className="text-xs sm:text-sm">
                    <div className="font-bold text-white">Questions BAC 2020-2025</div>
                    <div className="text-white/60">issues du programme officiel marocain</div>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-3.5 rounded-2xl bg-white/[.04] border border-white/10">
                  <div className="w-8 h-8 rounded-lg bg-emerald-500/15 text-emerald-200 flex items-center justify-center flex-shrink-0">
                    <ShieldCheck className="w-4 h-4" />
                  </div>
                  <div className="text-xs sm:text-sm">
                    <div className="font-bold text-white">Tu peux dire « je ne sais pas »</div>
                    <div className="text-white/60">sans aucune pénalité</div>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-3.5 rounded-2xl bg-white/[.04] border border-white/10">
                  <div className="w-8 h-8 rounded-lg bg-amber-500/15 text-amber-200 flex items-center justify-center flex-shrink-0">
                    <Coffee className="w-4 h-4" />
                  </div>
                  <div className="text-xs sm:text-sm">
                    <div className="font-bold text-white">~3 minutes par matière</div>
                    <div className="text-white/60">{subjects.length * 10} questions au total · pause autorisée</div>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-3.5 rounded-2xl bg-white/[.04] border border-white/10">
                  <div className="w-8 h-8 rounded-lg bg-indigo-500/15 text-indigo-200 flex items-center justify-center flex-shrink-0">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div className="text-xs sm:text-sm">
                    <div className="font-bold text-white">Plan personnalisé à la fin</div>
                    <div className="text-white/60">l'IA construit ta feuille de route</div>
                  </div>
                </div>
              </div>

              {/* Subjects preview */}
              {subjects.length > 0 && (
                <div className="mt-5 flex flex-wrap items-center gap-2">
                  <span className="text-xs text-white/55">Matières :</span>
                  {subjects.map((s) => (
                    <span key={s.id} className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/[.06] border border-white/10 text-xs font-semibold text-white/85">
                      <span>{subjectIcon(s.icon)}</span>
                      <span>{s.name_fr}</span>
                    </span>
                  ))}
                </div>
              )}

              {error && (
                <div className="mt-6 p-4 bg-red-500/15 border border-red-400/30 rounded-xl text-red-200 text-sm">{error}</div>
              )}

              <button
                onClick={startFullDiagnostic}
                disabled={!subjects.length}
                className="mt-8 w-full group relative px-8 py-5 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white rounded-2xl font-bold text-lg shadow-xl shadow-indigo-500/30 hover:shadow-2xl hover:shadow-indigo-500/40 hover:scale-[1.01] active:scale-[0.99] transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
              >
                <Sparkles className="w-6 h-6 group-hover:rotate-12 transition-transform" />
                C'est parti — je commence
                <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
              </button>
              <p className="text-xs text-white/55 text-center mt-3 flex items-center justify-center gap-1.5">
                <Lightbulb className="w-3.5 h-3.5" />
                Les {subjects.length} matières se préparent en parallèle pour démarrer en quelques secondes.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ══ PHASE: PRELOADING ══
  if (phase === 'preloading') {
    const total = subjects.length || 1;
    const pct = Math.round((preloadDone / total) * 100);
    return (
      <div className="min-h-screen bg-[#070718] text-white flex items-center justify-center p-6 relative overflow-hidden">
        <div className="max-w-md w-full glass-strong rounded-3xl shadow-xl p-10 text-center">
          <div className="relative inline-block mb-6">
            <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
              <Loader2 className="w-10 h-10 text-white animate-spin" />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">Préparation en cours…</h2>
          <p className="text-white/70 text-sm mb-6">
            Dès que la 1re matière est prête, tu commences. Les autres se génèrent en arrière-plan.
          </p>
          <div className="w-full bg-white/5 rounded-full h-1.5 overflow-hidden mb-3">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-500"
              style={{ width: `${pct}%` }}
            />
          </div>
          <div className="text-sm font-semibold text-white/85">
            {preloadDone} / {total} matières prêtes
          </div>
          <div className="mt-6 grid grid-cols-2 gap-2">
            {subjects.map((s, i) => {
              const done = i < preloadDone;
              return (
                <div
                  key={s.id}
                  className={`flex items-center gap-2 p-2 rounded-lg text-xs transition-all ${
                    done ? 'bg-emerald-500/15 text-emerald-200' : 'bg-white/5 text-white/40'
                  }`}
                >
                  {done ? <Check className="w-4 h-4" /> : <Loader2 className="w-4 h-4 animate-spin" />}
                  <span className="font-medium truncate">{s.name_fr}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  // ══ PHASE: QUIZ (one-by-one question display) ══
  if ((phase === 'quiz' || phase === 'submitting') && currentQuestions.length > 0 && currentQ) {
    const progress = (answeredCount / TOTAL_QUESTIONS) * 100;
    const currentAns = currentAnswers[String(currentQuestionIndex)];
    const isCurrentAnswered = currentQ.type === 'association'
      ? currentAns && typeof currentAns === 'object' && Object.values(currentAns).filter(Boolean).length >= (currentQ.pairs?.length || 0)
      : !!currentAns;
    const isLastQuestion = currentQuestionIndex >= TOTAL_QUESTIONS - 1;
    const allAnswered = answeredCount === TOTAL_QUESTIONS;
    const submitting = phase === 'submitting';

    const goToQuestion = (idx: number) => {
      setCurrentQuestionIndex(idx);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleNext = async () => {
      if (!isLastQuestion) {
        // Only advance if next question is already loaded
        if (currentQuestionIndex + 1 < currentQuestions.length) {
          goToQuestion(currentQuestionIndex + 1);
        }
      } else if (allAnswered) {
        submitCurrentSubject();
      }
    };

    const handlePrev = () => {
      if (currentQuestionIndex > 0) {
        goToQuestion(currentQuestionIndex - 1);
      }
    };

    return (
      <div className="min-h-screen bg-[#070718] text-white relative overflow-hidden">
        {/* Sticky header */}
        <div className="sticky top-0 z-10 backdrop-blur-2xl bg-[#070718]/70 border-b border-white/5">
          <div className="max-w-4xl mx-auto px-4 py-2">
            {/* Subject navigation row */}
            <div className="flex items-center gap-1.5 mb-2 overflow-x-auto pb-1">
              {subjects.map((s, si) => {
                const isCurrent = si === currentSubjectIndex;
                const isCompleted = subjectScores[s.name_fr] !== undefined;
                const isLocked = si > currentSubjectIndex && !isCompleted;
                return (
                  <button
                    key={s.id}
                    disabled={isLocked}
                    onClick={() => {
                      if (!isLocked && (subjectQuestions[s.id]?.length || 0) > 0) {
                        setCurrentSubjectIndex(si);
                        setCurrentQuestionIndex(0);
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                      }
                    }}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex-shrink-0 ${
                      isCurrent
                        ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md'
                        : isCompleted
                        ? 'bg-emerald-500/15 text-emerald-200 hover:bg-emerald-500/20'
                        : isLocked
                        ? 'bg-white/5 text-white/40 cursor-not-allowed opacity-60'
                        : 'glass text-white/85 hover:bg-white/[.06]'
                    }`}
                  >
                    <span className="text-sm">{subjectIcon(s.icon)}</span>
                    <span>{s.name_fr}</span>
                    {isCompleted && <CheckCircle className="w-3 h-3" />}
                  </button>
                );
              })}
            </div>

            {/* Current subject info + question navigation */}
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <div>
                  <p className="text-[10px] text-white/55">
                    Question {currentQuestionIndex + 1}/{TOTAL_QUESTIONS} · {answeredCount} répondues
                    {preloadDone < subjects.length && (
                      <span className="ml-2 inline-flex items-center gap-1 text-indigo-300">
                        <Loader2 className="w-3 h-3 animate-spin" />
                        {preloadDone}/{subjects.length}
                      </span>
                    )}
                  </p>
                </div>
              </div>
              <div className="hidden sm:flex items-center gap-1">
                {Array.from({ length: TOTAL_QUESTIONS }).map((_, i) => {
                  const a = currentAnswers[String(i)];
                  const isAnswered = !!a && (typeof a !== 'object' || Object.values(a).filter(Boolean).length > 0);
                  const isAvailable = i < currentQuestions.length;
                  return (
                    <button
                      key={i}
                      disabled={!isAvailable}
                      onClick={() => isAvailable && goToQuestion(i)}
                      className={`w-7 h-7 rounded text-[10px] font-bold transition-all ${
                        i === currentQuestionIndex
                          ? 'bg-blue-600 text-white shadow-md scale-110'
                          : isAnswered
                          ? 'bg-emerald-500 text-white shadow-sm'
                          : !isAvailable
                          ? 'bg-white/5 text-white/30 cursor-not-allowed'
                          : 'bg-white/5 text-white/55 hover:bg-white/10'
                      }`}
                    >
                      {i + 1}
                    </button>
                  );
                })}
              </div>
            </div>
            <div className="w-full bg-white/5 rounded-full h-1.5 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        </div>

        <div className="max-w-3xl mx-auto px-4 py-4">
          {error && (
            <div className="mb-4 p-3 bg-red-500/15 border border-red-400/30 rounded-lg text-red-200 text-xs">{error}</div>
          )}

          {/* Single question card — animates on each new question */}
          <div
            key={`q-${currentSubject?.id}-${currentQuestionIndex}`}
            className={`relative glass-strong rounded-2xl shadow-xl border-2 transition-colors anim-card-in ${
              isCurrentAnswered ? 'border-emerald-400/30' : 'border-white/10'
            }`}
          >
            {/* Subtle ambient glow */}
            <div className="pointer-events-none absolute -top-12 -right-12 w-48 h-48 bg-blue-500/10 blur-3xl rounded-full" />

            {/* Question header */}
            <div className="relative flex items-start justify-between gap-3 p-5 pb-3 border-b border-white/5">
              <div className="flex items-start gap-3 flex-1 min-w-0">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-sm font-black flex-shrink-0 transition-all ${
                  isCurrentAnswered
                    ? 'bg-emerald-500 text-white shadow-md shadow-emerald-500/30'
                    : 'bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-md shadow-blue-500/20'
                }`}>
                  {currentQuestionIndex + 1}
                </div>
                <div className="flex-1 min-w-0">
                  {/* Provenance + meta badges row */}
                  <div className="flex flex-wrap items-center gap-1.5 mb-2">
                    {currentSubject && (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-white/[.06] border border-white/10 text-[10px] font-semibold text-white/80">
                        <span>{subjectIcon(currentSubject.icon)}</span>
                        <span>{currentSubject.name_fr}</span>
                      </span>
                    )}
                    {currentQ.bac_year && (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-indigo-500/15 border border-indigo-400/30 text-[10px] font-bold text-indigo-200">
                        <BookOpen className="w-3 h-3" />
                        Inspiré du BAC {currentQ.bac_year}
                      </span>
                    )}
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wide ${difficultyBadge(currentQ.difficulty)}`}>
                      {currentQ.difficulty}
                    </span>
                    <span className="text-[10px] font-semibold text-white/65 bg-white/[.04] border border-white/10 px-2 py-0.5 rounded-full">
                      {currentQ.type === 'vrai_faux' ? 'Vrai / Faux' : currentQ.type === 'association' ? 'Association' : 'QCM'}
                    </span>
                  </div>
                  <h3 className="text-base sm:text-lg font-semibold text-white leading-relaxed">
                    <LatexRenderer content={currentQ.question} />
                  </h3>
                </div>
              </div>
            </div>

            {/* Body */}
            <div className="relative p-5">
              {currentQ.type === 'vrai_faux' ? (
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { val: 'vrai', label: 'Vrai', Icon: Check, color: 'emerald' },
                    { val: 'faux', label: 'Faux', Icon: XIcon, color: 'rose' },
                  ].map(({ val, label, Icon, color }) => {
                    const selected = currentAns === val;
                    const base = color === 'emerald'
                      ? (selected ? 'border-emerald-400/60 bg-emerald-500/15 text-emerald-200 shadow-md scale-[1.02]' : 'border-white/10 text-white/80 hover:border-emerald-400/40 hover:bg-emerald-500/10')
                      : (selected ? 'border-rose-400/60 bg-rose-500/15 text-rose-200 shadow-md scale-[1.02]' : 'border-white/10 text-white/80 hover:border-rose-400/40 hover:bg-rose-500/10');
                    return (
                      <button
                        key={val}
                        onClick={() => setAnswerAt(currentQuestionIndex, val)}
                        className={`p-5 rounded-2xl border-2 transition-all flex items-center justify-center gap-2.5 font-bold text-lg active:scale-[0.98] ${base}`}
                      >
                        <Icon className="w-6 h-6" />
                        {label}
                      </button>
                    );
                  })}
                </div>
              ) : currentQ.type === 'association' && currentQ.pairs ? (
                <AssociationQuestion
                  q={currentQ}
                  answer={(currentAns as Record<string, string>) || {}}
                  onChange={(m) => setAnswerAt(currentQuestionIndex, m)}
                />
              ) : (
                <div className="space-y-2.5">
                  {currentQ.options.map((option, index) => {
                    const letter = String.fromCharCode(65 + index);
                    const isSelected = currentAns === letter;
                    return (
                      <button
                        key={index}
                        onClick={() => setAnswerAt(currentQuestionIndex, letter)}
                        className={`w-full text-left p-3.5 sm:p-4 rounded-xl border-2 transition-all flex items-center gap-3 active:scale-[0.99] ${
                          isSelected
                            ? 'border-blue-400/60 bg-blue-500/15 shadow-md shadow-blue-500/20'
                            : 'border-white/10 hover:border-blue-400/50 hover:bg-white/[.06]'
                        }`}
                      >
                        <span className={`w-9 h-9 rounded-xl flex items-center justify-center text-sm font-black flex-shrink-0 transition-all ${
                          isSelected ? 'bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-md' : 'bg-white/5 text-white/70'
                        }`}>
                          {letter}
                        </span>
                        <span className="text-white text-sm sm:text-base leading-relaxed flex-1">
                          <LatexRenderer content={option} />
                        </span>
                        {isSelected && <Check className="w-4 h-4 text-blue-300 flex-shrink-0" />}
                      </button>
                    );
                  })}
                  <button
                    onClick={() => setAnswerAt(currentQuestionIndex, 'X')}
                    className={`w-full text-left p-3 rounded-xl border-2 transition-all flex items-center gap-2 text-xs sm:text-sm ${
                      currentAns === 'X'
                        ? 'border-slate-500 bg-white/5 text-white/85'
                        : 'border-dashed border-white/15 hover:border-white/25 text-white/60 hover:text-white/80 hover:bg-white/[.03]'
                    }`}
                  >
                    <HelpCircle className="w-4 h-4" />
                    <span className="italic">Je ne sais pas — ce n'est pas grave</span>
                  </button>
                </div>
              )}
            </div>

            {/* Subtle encouragement footer */}
            {!isCurrentAnswered && (
              <div className="px-5 pb-4 pt-1 text-[11px] text-white/45 italic flex items-center gap-1.5">
                <Lightbulb className="w-3 h-3" />
                Prends ton temps. C'est juste pour t'aider à progresser.
              </div>
            )}
          </div>

          {/* Navigation bar */}
          <div className="mt-4 glass-strong rounded-xl shadow-lg p-3 flex items-center justify-between">
            <button
              onClick={handlePrev}
              disabled={currentQuestionIndex === 0}
              className="px-4 py-2 bg-white/5 text-white/85 rounded-lg font-semibold hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-2 transition-all text-sm"
            >
              <ArrowLeft className="w-4 h-4" /> Précédent
            </button>

            <div className="text-center">
              <div className="text-[10px] text-white/55">Progression</div>
              <div className="font-bold text-white text-sm">
                {answeredCount}/{TOTAL_QUESTIONS}
              </div>
            </div>

            <button
              onClick={handleNext}
              disabled={
                !isCurrentAnswered ||
                submitting ||
                (isLastQuestion && !allAnswered) ||
                (!isLastQuestion && currentQuestionIndex + 1 >= currentQuestions.length)
              }
              className="px-5 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg font-bold shadow-lg shadow-indigo-500/30 hover:shadow-xl disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-2 transition-all text-sm"
            >
              {submitting ? (
                <><Loader2 className="w-4 h-4 animate-spin" /> Évaluer…</>
              ) : !isLastQuestion ? (
                currentQuestionIndex + 1 >= currentQuestions.length ? (
                  <><Loader2 className="w-4 h-4 animate-spin" /> Chargement…</>
                ) : (
                  <>Suivant <ArrowRight className="w-4 h-4" /></>
                )
              ) : currentSubjectIndex < subjects.length - 1 ? (
                <>Matière suivante <ArrowRight className="w-4 h-4" /></>
              ) : (
                <>Terminer <CheckCircle className="w-4 h-4" /></>
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ══ PHASE: RESULTS ══
  if (phase === 'results') {
    return (
      <div className="min-h-screen bg-[#070718] text-white p-6 relative overflow-hidden">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-3xl mb-4 shadow-lg shadow-emerald-500/30">
              <BarChart3 className="w-10 h-10 text-white" />
            </div>
            <h1 className="text-4xl font-black text-white">Résultats du Diagnostic</h1>
            <p className="text-white/70 mt-2 text-lg">Voici ton niveau dans chaque matière</p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-500/15 border border-red-400/30 rounded-xl text-red-200">{error}</div>
          )}

          <div className="space-y-4 mb-8">
            {Object.entries(subjectScores).map(([subjectName, scoreRaw]) => {
              const score = Number(scoreRaw) || 0;
              const tone = score >= 70 ? 'emerald' : score >= 50 ? 'amber' : 'rose';
              const label = score >= 70 ? 'Bon niveau' : score >= 50 ? 'À renforcer' : 'Prioritaire';
              const barColor = tone === 'emerald' ? 'bg-emerald-500' : tone === 'amber' ? 'bg-amber-500' : 'bg-rose-500';
              const textColor = tone === 'emerald' ? 'text-emerald-300' : tone === 'amber' ? 'text-amber-300' : 'text-rose-300';
              const badgeColor = tone === 'emerald' ? 'bg-emerald-500/15 text-emerald-200' : tone === 'amber' ? 'bg-amber-500/15 text-amber-200' : 'bg-rose-500/15 text-rose-200';
              return (
                <div key={subjectName} className="glass rounded-2xl p-5">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-bold text-white">{subjectName}</h3>
                    <div className="flex items-center gap-2">
                      <span className={`text-2xl font-black ${textColor}`}>{Math.round(score)}%</span>
                      <span className={`text-xs px-2 py-1 rounded-full font-medium ${badgeColor}`}>{label}</span>
                    </div>
                  </div>
                  <div className="w-full bg-white/5 rounded-full h-3 overflow-hidden">
                    <div className={`${barColor} h-3 rounded-full transition-all duration-1000`} style={{ width: `${score}%` }} />
                  </div>
                </div>
              );
            })}
          </div>

          <div className="text-center space-y-4">
            <button
              onClick={handleGeneratePlan}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl font-bold text-lg hover:shadow-2xl shadow-lg shadow-indigo-500/30 transition-all flex items-center gap-3 mx-auto"
            >
              <Sparkles className="w-6 h-6" />
              Générer mon Programme Personnalisé
            </button>
            <p className="text-sm text-white/55">
              L'IA va créer un programme adapté à ton niveau pour chaque matière
            </p>

            <button
              onClick={() => {
                setPhase('intro');
                setSubjectScores({});
                setCurrentSubjectIndex(0);
                setSubjectQuestions({});
                setAnswers({});
              }}
              className="px-6 py-3 glass text-white/85 rounded-xl font-semibold hover:bg-white/[.06] transition-all flex items-center gap-2 mx-auto"
            >
              <ArrowLeft className="w-5 h-5" />
              Refaire le diagnostic
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ══ PHASE: GENERATING PLAN ══
  if (phase === 'generating') {
    return (
      <div className="min-h-screen bg-[#070718] text-white flex items-center justify-center relative overflow-hidden">
        <div className="pointer-events-none fixed inset-0 z-0">
          <div className="absolute top-1/3 left-1/3 w-[500px] h-[500px] rounded-full bg-indigo-600/15 blur-[140px] anim-pulse-glow" />
        </div>
        <div className="text-center relative z-10">
          <Loader2 className="w-16 h-16 text-indigo-300 animate-spin mx-auto mb-6" />
          <h2 className="text-2xl font-bold text-white mb-2">Génération de ton programme...</h2>
          <p className="text-white/70">L'IA analyse tes résultats et prépare un plan optimal</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#070718]">
      <Loader2 className="w-8 h-8 text-indigo-400 animate-spin" />
    </div>
  );
}

