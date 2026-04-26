import { useState, useEffect, useRef, useCallback, forwardRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import html2canvas from 'html2canvas';
import { getExamDetail, submitExam, startExam as apiStartExam, saveExamProgress } from '../services/api';
import { useAuthStore } from '../stores/authStore';
import QuestionRenderer from '../components/exam/QuestionRenderer';
import AnswerInput from '../components/exam/AnswerInput';
import LatexRenderer from '../components/exam/LatexRenderer';
import {
  Clock, AlertTriangle, Send, Loader2, XCircle, ArrowLeft, ArrowRight,
  FileText, Trophy, Target, Lightbulb, CheckCircle2, BookOpen, Sparkles, Save,
  RotateCcw, Share2, X, Copy, Check,
} from 'lucide-react';
import {
  getMention, toScoreOn20, getBacContextMessage, getSubjectTips,
  autosaveGet, autosaveSet, autosaveClear, autosaveSavedAt, timeAgo, formatDuration,
} from '../utils/examGrading';

/* Autosave keys per exam */
const autosaveKey = (examId: string) => `exam_real_autosave_v1_${examId}`;
const MOALIM_URL = 'https://moalim.online';

interface AutosaveState {
  answers: Record<number, string>;
  currentQ: number;
  elapsedSeconds: number;
  questionTimes: Record<number, number>;
  started: boolean;
}

interface Choice {
  letter: string;
  text: string;
}

interface QuestionData {
  index: number;
  content: string;
  details?: any;
  context?: any[];
  documents?: any[];
  page_context?: string;
  points: number;
  type?: 'open' | 'qcm' | 'vrai_faux' | 'association' | 'schema';
  choices?: Choice[];
  items_left?: string[];
  items_right?: string[];
  correct_answer?: string | boolean;
  correction?: { content: string; details?: any; answers?: any } | null;
  part?: string;
  exercise?: string;
  exercise_context?: string;
}

interface ExamData {
  id: string;
  subject: string;
  year: number;
  session: string;
  duration_minutes: number;
  coefficient: number;
  total_points: number;
  questions: QuestionData[];
  question_count: number;
}

const TYPE_BADGE: Record<string, { label: string; bg: string; text: string }> = {
  open: { label: 'Ouverte', bg: 'bg-blue-500/15', text: 'text-blue-200' },
  qcm: { label: 'QCM', bg: 'bg-violet-500/15', text: 'text-purple-200' },
  vrai_faux: { label: 'Vrai / Faux', bg: 'bg-amber-500/15', text: 'text-amber-200' },
  schema: { label: 'Schéma', bg: 'bg-emerald-500/15', text: 'text-emerald-200' },
  association: { label: 'Association', bg: 'bg-rose-500/15', text: 'text-orange-200' },
};

export default function ExamReal() {
  const { examId } = useParams<{ examId: string }>();
  const navigate = useNavigate();
  const { student } = useAuthStore();

  const [exam, setExam] = useState<ExamData | null>(null);
  const [loading, setLoading] = useState(true);
  const [started, setStarted] = useState(false);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [_imageData, setImageData] = useState<Record<number, string | null>>({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [showConfirmSubmit, setShowConfirmSubmit] = useState(false);
  const [resumePrompt, setResumePrompt] = useState<{ savedAt: number; state: AutosaveState } | null>(null);
  const [lastSavedAt, setLastSavedAt] = useState<number | null>(null);
  const [questionTimes, setQuestionTimes] = useState<Record<number, number>>({});
  const [shareOpen, setShareOpen] = useState(false);

  const startTimeRef = useRef<number>(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const currentQRef = useRef<number>(0);
  const lastQChangeRef = useRef<number>(Date.now());
  const attemptIdRef = useRef<string | null>(null);

  // Keep a ref of currentQ for accurate per-question timer tracking
  useEffect(() => { currentQRef.current = currentQ; }, [currentQ]);

  useEffect(() => {
    if (examId) loadExam();
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [examId]);

  // ── Autosave every 5 s while exam is active (local + server) ──
  useEffect(() => {
    if (!started || !examId || results) return;
    const id = setInterval(() => {
      const elapsed = Math.round((Date.now() - startTimeRef.current) / 1000);
      const state: AutosaveState = {
        answers,
        currentQ,
        elapsedSeconds: elapsed,
        questionTimes,
        started: true,
      };
      autosaveSet(autosaveKey(examId), state);
      setLastSavedAt(Date.now());
      // Sync to server
      if (attemptIdRef.current) {
        const answersStr: Record<string, string> = {};
        Object.entries(answers).forEach(([k, v]) => { if (v?.trim()) answersStr[k] = String(v); });
        saveExamProgress(attemptIdRef.current, {
          answers: answersStr,
          current_question_index: currentQ,
          duration_seconds: elapsed,
        }).catch(() => {});
      }
    }, 5000);
    return () => clearInterval(id);
  }, [started, examId, answers, currentQ, questionTimes, results]);

  // ── Save on every answer change (debounced) ──
  useEffect(() => {
    if (!started || !examId || results) return;
    const t = setTimeout(() => {
      const elapsed = Math.round((Date.now() - startTimeRef.current) / 1000);
      autosaveSet(autosaveKey(examId), {
        answers,
        currentQ,
        elapsedSeconds: elapsed,
        questionTimes,
        started: true,
      });
      setLastSavedAt(Date.now());
    }, 800);
    return () => clearTimeout(t);
  }, [answers, currentQ, started, examId, questionTimes, results]);

  // ── Warn before leaving while exam active ──
  useEffect(() => {
    if (!started || results) return;
    const handler = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      e.returnValue = '';
    };
    window.addEventListener('beforeunload', handler);
    return () => window.removeEventListener('beforeunload', handler);
  }, [started, results]);

  // ── Track per-question time ──
  useEffect(() => {
    if (!started) return;
    const now = Date.now();
    const prev = currentQRef.current;
    const elapsed = Math.round((now - lastQChangeRef.current) / 1000);
    if (elapsed > 0) {
      setQuestionTimes((prevMap) => ({
        ...prevMap,
        [prev]: (prevMap[prev] || 0) + elapsed,
      }));
    }
    lastQChangeRef.current = now;
  }, [currentQ, started]);

  const loadExam = async () => {
    setLoading(true);
    try {
      const res = await getExamDetail(examId!);
      setExam(res.data);
      setTimeLeft(res.data.duration_minutes * 60);

      // Check for autosave to offer resume
      if (examId) {
        const saved = autosaveGet<AutosaveState>(autosaveKey(examId));
        const savedAt = autosaveSavedAt(autosaveKey(examId));
        if (saved && saved.started && savedAt) {
          const totalSec = (res.data.duration_minutes || 0) * 60;
          const remaining = Math.max(0, totalSec - (saved.elapsedSeconds || 0));
          if (remaining > 0 && Object.keys(saved.answers || {}).length > 0) {
            setResumePrompt({ savedAt, state: saved });
          }
        }
      }
    } catch (e) {
      console.error('Failed to load exam:', e);
    } finally {
      setLoading(false);
    }
  };

  const startTimer = (secondsLeft: number) => {
    setTimeLeft(secondsLeft);
    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          if (timerRef.current) clearInterval(timerRef.current);
          handleAutoSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const handleStartExam = async () => {
    setStarted(true);
    startTimeRef.current = Date.now();
    lastQChangeRef.current = Date.now();
    if (exam) startTimer(exam.duration_minutes * 60);
    // Register attempt on server
    if (examId) {
      try {
        const res = await apiStartExam(examId, 'real');
        attemptIdRef.current = res.data.attempt_id || null;
      } catch (e) { console.error('Failed to register exam start:', e); }
    }
  };

  const resumeExam = async () => {
    if (!resumePrompt || !exam) return;
    const { state } = resumePrompt;
    setAnswers(state.answers || {});
    setCurrentQ(state.currentQ || 0);
    setQuestionTimes(state.questionTimes || {});
    const totalSec = exam.duration_minutes * 60;
    const remaining = Math.max(0, totalSec - (state.elapsedSeconds || 0));
    startTimeRef.current = Date.now() - (state.elapsedSeconds || 0) * 1000;
    lastQChangeRef.current = Date.now();
    setResumePrompt(null);
    setStarted(true);
    startTimer(remaining);
    // Register/resume attempt on server
    if (examId) {
      try {
        const res = await apiStartExam(examId, 'real');
        attemptIdRef.current = res.data.attempt_id || null;
      } catch (e) { console.error('Failed to register exam resume:', e); }
    }
  };

  const discardResume = () => {
    if (examId) autosaveClear(autosaveKey(examId));
    setResumePrompt(null);
  };

  const handleAutoSubmit = useCallback(async () => {
    if (submitting || results) return;
    await doSubmit();
  }, [submitting, results]);

  const doSubmit = async () => {
    if (!exam || !examId) return;
    setSubmitting(true);
    if (timerRef.current) clearInterval(timerRef.current);

    const duration = Math.round((Date.now() - startTimeRef.current) / 1000);
    const answersStr: Record<string, string> = {};
    Object.entries(answers).forEach(([k, v]) => {
      if (v?.trim()) answersStr[k] = v;
    });

    try {
      const res = await submitExam(examId, answersStr, 'real', duration, attemptIdRef.current);
      setResults(res.data);
      // Clear autosave on successful submit
      autosaveClear(autosaveKey(examId));
      attemptIdRef.current = null;
    } catch (e: any) {
      console.error('Submit failed:', e);
      alert('Erreur lors de la soumission. Ne t\'inquiète pas : tes réponses sont sauvegardées localement. Tu peux réessayer.');
    } finally {
      setSubmitting(false);
      setShowConfirmSubmit(false);
    }
  };

  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    if (h > 0) return `${h}h ${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  const answeredCount = Object.keys(answers).filter((k) => answers[Number(k)]?.trim()).length;
  const isLowTime = timeLeft > 0 && timeLeft < 300; // < 5 min
  const isTimeUp = started && timeLeft <= 0;

  if (loading || !exam) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#070718]">
        <Loader2 className="w-8 h-8 text-indigo-200 animate-spin" />
      </div>
    );
  }

  // Results screen — rich BAC-style report
  if (results) {
    const rawScore = Number(results.total_score || 0);
    const maxScore = Number(results.max_score || exam.total_points || 20);
    const scoreOn20 = toScoreOn20(rawScore, maxScore);
    const mention = getMention(scoreOn20);
    const bacMsg = getBacContextMessage(scoreOn20);
    const percent = maxScore > 0 ? Math.round((rawScore / maxScore) * 100) : 0;
    const firstName = (student?.full_name || student?.username || 'Étudiant').trim().split(/\s+/)[0];
    const sessionLabel = (exam.session || '').toLowerCase() === 'rattrapage' ? 'Rattrapage' : 'Normale';

    // Group scores by part (if available in exam data)
    const partsAgg = new Map<string, { earned: number; max: number; count: number; answered: number }>();
    exam.questions.forEach((q, idx) => {
      const part = q.part || 'Examen';
      const entry = partsAgg.get(part) || { earned: 0, max: 0, count: 0, answered: 0 };
      entry.max += q.points || 0;
      entry.count += 1;
      const score = results.scores?.[String(idx)];
      if (score != null) entry.earned += Number(score);
      if (answers[idx]?.trim()) entry.answered += 1;
      partsAgg.set(part, entry);
    });
    const parts = Array.from(partsAgg.entries());

    return (
      <div className="min-h-screen bg-[#070718] text-white relative overflow-hidden">
        {/* Decorative orbs */}
        <div className="pointer-events-none fixed inset-0 z-0">
          <div className="absolute top-0 left-1/3 w-[600px] h-[600px] rounded-full bg-indigo-600/15 blur-[140px] anim-pulse-glow" />
          <div className="absolute bottom-0 right-[10%] w-[500px] h-[500px] rounded-full bg-amber-500/10 blur-[140px] anim-pulse-glow" style={{ animationDelay: '2s' }} />
        </div>
        {/* Header */}
        <header className="relative z-20 backdrop-blur-2xl bg-[#070718]/70 border-b border-white/5">
          <div className="max-w-4xl mx-auto px-4 py-5 flex items-center gap-3">
            <button onClick={() => navigate('/exam')} className="p-2 -ml-2 rounded-xl hover:bg-white/10 text-white/55">
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div>
              <h1 className="text-xl font-bold text-white">
                Résultats — {exam.subject} {exam.year}
              </h1>
              <p className="text-sm text-white/55">
                Mode Examen Réel · Session {(exam.session || '').toLowerCase() === 'rattrapage' ? 'Rattrapage' : 'Normale'}
              </p>
            </div>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-6 space-y-5">

          {/* ── Main score card with mention ── */}
          <div className={`rounded-3xl border-2 ${mention.border} ${mention.bg} overflow-hidden shadow-sm`}>
            <div className="p-6 md:p-8">
              <div className="flex flex-col md:flex-row items-center gap-6">
                {/* Grade circle */}
                <div className={`relative w-32 h-32 rounded-full bg-gradient-to-br ${mention.gradient} flex flex-col items-center justify-center shadow-lg flex-shrink-0`}>
                  <span className="text-4xl font-black text-white leading-none">{scoreOn20.toFixed(2)}</span>
                  <span className="text-xs font-bold text-white/80 mt-1">/ 20</span>
                </div>

                {/* Mention + context */}
                <div className="flex-1 text-center md:text-left">
                  <div className="inline-flex items-center gap-2 mb-2">
                    <span className="text-2xl">{mention.emoji}</span>
                    <span className={`text-xl font-black ${mention.text}`}>
                      Mention {mention.label}
                    </span>
                  </div>
                  <p className="text-sm text-white/70 leading-relaxed mb-3">
                    {mention.encouragement}
                  </p>
                  <div className="flex items-center gap-2 text-xs text-white/55 flex-wrap justify-center md:justify-start">
                    <Trophy className="w-3.5 h-3.5" />
                    <span>Score brut : <b>{rawScore.toFixed(2)} / {maxScore}</b></span>
                    <span className="text-white/30">·</span>
                    <span>{percent}%</span>
                  </div>
                  <button
                    onClick={() => setShareOpen(true)}
                    className="mt-4 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-blue-700 text-white text-sm font-bold shadow-sm hover:shadow-md transition-all"
                  >
                    <Share2 className="w-4 h-4" />
                    Partager ma réussite
                  </button>
                </div>
              </div>

              {/* BAC context */}
              <div className="mt-5 pt-5 border-t border-white/10 flex items-start gap-2.5">
                <Target className={`w-4 h-4 ${mention.text} mt-0.5 flex-shrink-0`} />
                <p className="text-[13px] text-white/85 leading-relaxed">
                  <span className="font-semibold">Contexte BAC :</span> {bacMsg}
                </p>
              </div>
            </div>
          </div>

          {/* ── Stats grid ── */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div className="glass rounded-2xl p-4 text-center">
              <p className="text-2xl font-black text-white">{results.answered_count || 0}<span className="text-sm font-bold text-white/40">/{results.question_count || 0}</span></p>
              <p className="text-[11px] text-white/55 mt-1 font-medium">Questions répondues</p>
            </div>
            <div className="glass rounded-2xl p-4 text-center">
              <p className="text-2xl font-black text-white">{formatDuration(results.duration_seconds || 0)}</p>
              <p className="text-[11px] text-white/55 mt-1 font-medium">Durée totale</p>
            </div>
            <div className="glass rounded-2xl p-4 text-center">
              <p className="text-2xl font-black text-white">{percent}%</p>
              <p className="text-[11px] text-white/55 mt-1 font-medium">Réussite</p>
            </div>
            <div className="glass rounded-2xl p-4 text-center">
              <p className={`text-2xl font-black ${mention.text}`}>{mention.short}</p>
              <p className="text-[11px] text-white/55 mt-1 font-medium">Mention</p>
            </div>
          </div>

          {/* ── Per-part breakdown ── */}
          {parts.length > 1 && (
            <div className="glass rounded-2xl p-5">
              <h2 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-blue-300" />
                Progression par partie
              </h2>
              <div className="space-y-4">
                {parts.map(([partName, agg]) => {
                  const pct = agg.max > 0 ? Math.round((agg.earned / agg.max) * 100) : 0;
                  const partMention = getMention(toScoreOn20(agg.earned, agg.max));
                  return (
                    <div key={partName}>
                      <div className="flex items-center justify-between mb-1.5">
                        <p className="text-[13px] font-semibold text-white/85">{partName}</p>
                        <div className="flex items-center gap-2 text-xs">
                          <span className="text-white/40">{agg.answered}/{agg.count} q.</span>
                          <span className={`font-bold ${partMention.text}`}>
                            {agg.earned.toFixed(1)}/{agg.max} pts
                          </span>
                        </div>
                      </div>
                      <div className="w-full h-2.5 bg-white/5 rounded-full overflow-hidden">
                        <div
                          className={`h-full bg-gradient-to-r ${partMention.gradient} transition-all duration-700`}
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* ── Detailed corrections ── */}
          {results.feedbacks && Object.keys(results.feedbacks).length > 0 && (
            <div className="space-y-3">
              <h2 className="text-sm font-bold text-white flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-300" />
                Corrections détaillées
              </h2>
              {exam.questions.map((q, idx) => {
                const fb = results.feedbacks?.[String(idx)];
                const score = results.scores?.[String(idx)];
                const hasAnswer = !!answers[idx]?.trim();
                const qScoreOn20 = score != null && q.points > 0 ? (Number(score) / q.points) * 20 : null;
                const qTier = qScoreOn20 != null ? getMention(qScoreOn20) : null;

                return (
                  <div key={idx} className="glass rounded-2xl p-4 md:p-5">
                    <div className="flex items-center justify-between mb-2 gap-3">
                      <div className="flex items-center gap-2 min-w-0">
                        <span className="text-xs font-black text-white/85 bg-white/5 px-2 py-1 rounded-lg">Q{idx + 1}</span>
                        {q.points > 0 && (
                          <span className="text-[11px] text-white/55">{q.points} pt{q.points > 1 ? 's' : ''}</span>
                        )}
                      </div>
                      {score != null && qTier ? (
                        <span className={`text-xs font-bold px-2.5 py-1 rounded-lg ${qTier.bg} ${qTier.text} flex items-center gap-1`}>
                          {qTier.emoji} {Number(score).toFixed(1)}/{q.points}
                        </span>
                      ) : hasAnswer ? (
                        <span className="text-xs text-white/40">En attente</span>
                      ) : (
                        <span className="text-xs text-white/40 flex items-center gap-1">
                          <XCircle className="w-3.5 h-3.5" /> Non répondue
                        </span>
                      )}
                    </div>
                    <LatexRenderer as="p" className="text-[13px] text-white/70 line-clamp-2 mb-2.5 leading-relaxed">{q.content}</LatexRenderer>
                    {hasAnswer && (
                      <div className="bg-white/[.03] rounded-lg p-3 text-[13px] text-white/85 mb-2 border border-white/5">
                        <span className="text-[10px] font-bold text-white/40 uppercase tracking-wider">Ta réponse</span>
                        <p className="mt-1 whitespace-pre-line">{answers[idx]}</p>
                      </div>
                    )}
                    {fb && (
                      <LatexRenderer className="bg-gradient-to-br from-blue-500/10 to-indigo-500/10 rounded-lg p-3 text-[13px] text-white/85 border border-white/5">
                        {fb}
                      </LatexRenderer>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {/* Actions */}
          <div className="flex flex-col sm:flex-row gap-3 pt-2">
            <button
              onClick={() => navigate('/exam')}
              className="flex-1 px-6 py-3 bg-gradient-to-r from-indigo-500 to-cyan-500 text-white rounded-xl font-bold shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 transition-all flex items-center justify-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" /> Retour aux examens
            </button>
            <button
              onClick={() => {
                if (examId) autosaveClear(autosaveKey(examId));
                window.location.reload();
              }}
              className="flex-1 px-6 py-3 glass text-white/85 rounded-xl font-semibold hover:bg-white/[.06] transition-colors flex items-center justify-center gap-2"
            >
              <RotateCcw className="w-4 h-4" /> Refaire cet examen
            </button>
          </div>
        </main>

        {shareOpen && (
          <RealExamShareModal
            firstName={firstName}
            exam={exam}
            rawScore={rawScore}
            maxScore={maxScore}
            scoreOn20={scoreOn20}
            percent={percent}
            mention={mention}
            sessionLabel={sessionLabel}
            answeredCount={results.answered_count || 0}
            questionCount={results.question_count || exam.questions.length}
            durationSeconds={results.duration_seconds || 0}
            onClose={() => setShareOpen(false)}
          />
        )}
      </div>
    );
  }

  // Pre-start screen — rassurant, avec conseils méthodo
  if (!started) {
    const tips = getSubjectTips(exam.subject);

    // Resume prompt — takes priority if an autosave exists
    if (resumePrompt) {
      const answeredCount = Object.values(resumePrompt.state.answers || {}).filter((v) => (v || '').toString().trim()).length;
      const remainingSec = Math.max(0, exam.duration_minutes * 60 - (resumePrompt.state.elapsedSeconds || 0));
      return (
        <div className="min-h-screen bg-[#070718] text-white flex items-center justify-center p-4 relative overflow-hidden">
          <div className="glass-strong rounded-3xl shadow-xl max-w-md w-full overflow-hidden">
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-5 text-white">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-white/20 border border-white/20 flex items-center justify-center">
                  <Save className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-lg font-bold">Examen en cours retrouvé</h2>
                  <p className="text-xs text-blue-100">Tu peux continuer là où tu t'étais arrêté</p>
                </div>
              </div>
            </div>
            <div className="p-6 space-y-4">
              <p className="text-sm text-white/70 leading-relaxed">
                On a gardé tes réponses en sécurité dans ton navigateur. Tu peux reprendre cet examen avec le temps restant, ou recommencer de zéro.
              </p>
              <div className="grid grid-cols-3 gap-2.5">
                <div className="bg-white/[.03] border border-white/5 rounded-xl p-3 text-center">
                  <p className="text-xl font-black text-white">{answeredCount}</p>
                  <p className="text-[10px] text-white/55 font-medium">Réponses</p>
                </div>
                <div className="bg-white/[.03] border border-white/5 rounded-xl p-3 text-center">
                  <p className="text-xl font-black text-white">{formatDuration(remainingSec)}</p>
                  <p className="text-[10px] text-white/55 font-medium">Restant</p>
                </div>
                <div className="bg-white/[.03] border border-white/5 rounded-xl p-3 text-center">
                  <p className="text-[11px] font-bold text-white">{timeAgo(resumePrompt.savedAt)}</p>
                  <p className="text-[10px] text-white/55 font-medium">Sauvé</p>
                </div>
              </div>
              <div className="flex flex-col gap-2 pt-1">
                <button
                  onClick={resumeExam}
                  className="w-full px-4 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all flex items-center justify-center gap-2 shadow-md shadow-blue-500/20"
                >
                  <Sparkles className="w-4 h-4" /> Reprendre l'examen
                </button>
                <button
                  onClick={discardResume}
                  className="w-full px-4 py-2.5 border border-white/15 text-white/85 rounded-xl font-medium hover:bg-white/[.06] transition-colors"
                >
                  Recommencer depuis le début
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="min-h-screen bg-[#070718] text-white flex items-center justify-center p-4 relative overflow-hidden">
        <div className="glass-strong rounded-3xl shadow-xl max-w-xl w-full overflow-hidden">
          {/* Header band */}
          <div className="bg-gradient-to-r from-slate-800 via-slate-900 to-slate-800 px-6 py-5">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-white/10 border border-white/20 flex items-center justify-center">
                <FileText className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="text-[10px] font-bold text-blue-200 uppercase tracking-wider mb-0.5">Examen National BAC</p>
                <h1 className="text-lg font-bold text-white truncate">
                  {exam.subject} — {exam.year}
                </h1>
                <p className="text-xs text-white/30">
                  Session {(exam.session || '').toLowerCase() === 'rattrapage' ? 'Rattrapage' : 'Normale'} · Sciences Physiques BIOF
                </p>
              </div>
            </div>
          </div>

          <div className="p-6 space-y-5">
            {/* Stats */}
            <div className="grid grid-cols-3 gap-2.5">
              <div className="bg-white/[.03] border border-white/5 rounded-xl p-3.5 text-center">
                <Clock className="w-4 h-4 text-white/40 mx-auto mb-1" />
                <p className="text-xl font-black text-white">{exam.duration_minutes}</p>
                <p className="text-[10px] text-white/55 font-medium">minutes</p>
              </div>
              <div className="bg-white/[.03] border border-white/5 rounded-xl p-3.5 text-center">
                <FileText className="w-4 h-4 text-white/40 mx-auto mb-1" />
                <p className="text-xl font-black text-white">{exam.question_count}</p>
                <p className="text-[10px] text-white/55 font-medium">questions</p>
              </div>
              <div className="bg-white/[.03] border border-white/5 rounded-xl p-3.5 text-center">
                <Trophy className="w-4 h-4 text-white/40 mx-auto mb-1" />
                <p className="text-xl font-black text-white">/{exam.total_points}</p>
                <p className="text-[10px] text-white/55 font-medium">points</p>
              </div>
            </div>

            {/* Reassuring message */}
            <div className="bg-gradient-to-br from-blue-500/10 to-indigo-500/10 border border-white/5 rounded-2xl p-4">
              <div className="flex items-start gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-blue-500 flex items-center justify-center flex-shrink-0">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
                <div>
                  <p className="text-[13px] font-bold text-white mb-1">Tu es prêt.</p>
                  <p className="text-[12.5px] text-white/90 leading-relaxed">
                    Cet entraînement reproduit les conditions réelles du BAC. Tes réponses sont
                    <b> sauvegardées automatiquement</b> — si ton navigateur se ferme, rien n'est perdu.
                  </p>
                </div>
              </div>
            </div>

            {/* Subject methodology tips */}
            <div className="glass rounded-2xl overflow-hidden">
              <div className="px-4 py-2.5 bg-gradient-to-r from-amber-500/10 to-orange-500/10 border-b border-amber-400/30 flex items-center gap-2">
                <Lightbulb className="w-4 h-4 text-amber-300" />
                <p className="text-[12px] font-bold text-amber-200">Conseils méthode — {tips.subject}</p>
              </div>
              <div className="p-4 space-y-2">
                <p className="text-[12px] text-white/70 italic leading-relaxed mb-2">{tips.timeAdvice}</p>
                <ul className="space-y-1.5">
                  {tips.tips.map((tip, i) => (
                    <li key={i} className="flex items-start gap-2 text-[12.5px] text-white/85 leading-relaxed">
                      <span className="mt-[7px] h-1.5 w-1.5 rounded-full bg-amber-500 flex-shrink-0" />
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Conditions (compact) */}
            <div className="bg-white/[.03] border border-white/10 rounded-xl px-4 py-3">
              <p className="text-[11px] font-bold text-white/55 uppercase tracking-wider mb-1.5">Règles de l'épreuve</p>
              <ul className="text-[12px] text-white/70 space-y-0.5">
                <li>· Chronomètre officiel · Soumission automatique à la fin</li>
                <li>· Navigation libre entre les questions</li>
                <li>· Correction détaillée après la remise de la copie</li>
              </ul>
            </div>

            <div className="flex gap-3 pt-1">
              <button
                onClick={() => navigate('/exam')}
                className="flex-1 px-4 py-3 border border-white/15 text-white/85 rounded-xl font-medium hover:bg-white/[.06] transition-colors"
              >
                Annuler
              </button>
              <button
                onClick={handleStartExam}
                className="flex-[2] px-4 py-3 bg-gradient-to-r from-indigo-500 to-cyan-500 text-white rounded-xl font-bold shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 transition-all flex items-center justify-center gap-2"
              >
                <Sparkles className="w-4 h-4" /> Commencer l'examen
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Active exam
  const question = exam.questions[currentQ];
  const badge = TYPE_BADGE[question.type || 'open'];
  const goNext = () => { if (currentQ < exam.questions.length - 1) setCurrentQ(currentQ + 1); };
  const goPrev = () => { if (currentQ > 0) setCurrentQ(currentQ - 1); };

  return (
    <div className="h-screen flex flex-col bg-[#070718] text-white">
      {/* ===================== COMPACT HEADER ===================== */}
      <header className={`border-b flex-shrink-0 z-30 backdrop-blur-2xl ${isLowTime ? 'bg-red-500/15 border-red-500/30' : 'bg-[#070718]/70 border-white/5'}`}>
        <div className="max-w-[1600px] mx-auto px-3 lg:px-5">
          <div className="flex items-center gap-2 py-2">
            {/* Back — requires confirmation during active exam (autosave is kept) */}
            <button
              onClick={() => {
                const msg = 'Ton examen est sauvegardé automatiquement. Tu pourras le reprendre plus tard. Quitter maintenant ?';
                if (window.confirm(msg)) navigate('/exam');
              }}
              title="Quitter — les réponses sont sauvegardées"
              className="p-1.5 rounded-lg hover:bg-white/10 text-white/40 transition-colors flex-shrink-0"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>

            {/* Title + progress */}
            <div className="min-w-0 flex-shrink-0">
              <h1 className="text-sm font-bold text-white truncate">
                {exam.subject} — {(exam.session || '').toLowerCase() === 'rattrapage' ? 'R' : 'N'} {exam.year}
              </h1>
              <div className="flex items-center gap-2">
                <span className="text-[10px] text-white/40">{answeredCount}/{exam.question_count}</span>
                <div className="w-16 bg-white/5 rounded-full h-1">
                  <div className="h-1 rounded-full bg-gradient-to-r from-red-500 to-rose-500 transition-all" style={{ width: `${exam.question_count > 0 ? Math.round((answeredCount / exam.question_count) * 100) : 0}%` }} />
                </div>
              </div>
            </div>

            {/* Timer */}
            <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl font-mono text-sm font-bold flex-shrink-0 ${
              isLowTime ? 'bg-red-500/20 text-red-200 animate-pulse' : 'bg-white/5 text-white/85'
            }`}>
              <Clock className="w-3.5 h-3.5" />
              {formatTime(timeLeft)}
            </div>

            {/* Autosave indicator */}
            {lastSavedAt && (
              <div
                className="hidden lg:flex items-center gap-1 px-2 py-1 rounded-lg bg-emerald-500/15 border border-emerald-400/30 text-emerald-200 text-[10px] font-semibold flex-shrink-0"
                title={`Dernière sauvegarde : ${timeAgo(lastSavedAt)}`}
              >
                <Save className="w-3 h-3" />
                <span className="hidden lg:inline">Sauvegardé</span>
              </div>
            )}

            {/* Separator */}
            <div className="w-px h-7 bg-white/10 mx-1 hidden lg:block" />

            {/* Question dots - scrollable */}
            <div className="flex-1 min-w-0 hidden lg:flex items-center gap-1 overflow-x-auto py-1 scrollbar-none">
              {exam.questions.map((_q, qIdx) => {
                const isCurrent = qIdx === currentQ;
                return (
                  <button
                    key={qIdx}
                    onClick={() => setCurrentQ(qIdx)}
                    title={`Q${qIdx + 1} (${_q.points} pts)`}
                    className={`relative w-7 h-7 rounded-lg text-[10px] font-bold transition-all flex-shrink-0 ${
                      isCurrent
                        ? 'ring-2 ring-offset-1 ring-red-400 bg-red-600 text-white'
                        : answers[qIdx]?.trim()
                        ? 'bg-emerald-500/15 text-emerald-200 border border-emerald-400/30'
                        : 'bg-white/5 text-white/55 hover:bg-white/10'
                    }`}
                  >
                    {qIdx + 1}
                  </button>
                );
              })}
            </div>

            {/* Navigation arrows */}
            <div className="flex items-center gap-1 flex-shrink-0">
              <button onClick={goPrev} disabled={currentQ === 0} className="p-1.5 rounded-lg border border-white/10 text-white/55 hover:bg-white/[.06] disabled:opacity-30 transition-colors">
                <ArrowLeft className="w-3.5 h-3.5" />
              </button>
              <span className="text-[11px] font-bold text-white/55 min-w-[40px] text-center">{currentQ + 1}/{exam.questions.length}</span>
              <button onClick={goNext} disabled={currentQ >= exam.questions.length - 1} className="p-1.5 rounded-lg text-white transition-all disabled:opacity-30 bg-gradient-to-r from-red-500 to-rose-600">
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Submit button */}
            <button
              onClick={() => setShowConfirmSubmit(true)}
              disabled={submitting}
              className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 bg-emerald-500 text-white rounded-xl text-xs font-medium hover:bg-emerald-700 transition-colors flex-shrink-0"
            >
              <Send className="w-3.5 h-3.5" /> <span className="hidden lg:inline">Rendre</span>
            </button>
          </div>
        </div>
      </header>

      {/* ===================== 2-COLUMN BODY ===================== */}
      <div className="flex-1 min-h-0 flex">
        {/* --- LEFT PANEL: Question + Documents (lg+ only — phones use stacked) --- */}
        <div className="hidden lg:block flex-1 min-w-0 overflow-y-auto border-r border-white/10">
          <div className="max-w-2xl mx-auto px-3 lg:px-5 py-3 space-y-2">
            {/* Type badge + exercise name */}
            <div className="flex items-center gap-2 flex-wrap">
              {question.exercise && (
                <span className="text-[11px] font-semibold text-white/55">{question.exercise}</span>
              )}
              <span className={`text-[11px] font-bold px-2 py-0.5 rounded-md ${badge.bg} ${badge.text}`}>
                {badge.label}
              </span>
              {question.part && (
                <span className="text-[10px] text-white/40 ml-auto">{question.part}</span>
              )}
            </div>

            {/* Question renderer */}
            <QuestionRenderer question={question} examId={exam.id} />
          </div>
        </div>

        {/* --- RIGHT PANEL: Answer (lg+ only) --- */}
        <div className="lg:w-[48%] flex-shrink-0 overflow-y-auto bg-[#070718]/40 hidden lg:block">
          <div className="px-3 lg:px-4 py-3 space-y-3 max-w-xl">
            <div className="flex items-center gap-2 mb-1">
              <div className="w-5 h-5 rounded-md bg-red-500/20 flex items-center justify-center">
                <FileText className="w-3 h-3 text-white/70" />
              </div>
              <span className="text-xs font-bold text-white/55">Votre réponse</span>
              {questionTimes[currentQ] > 0 && (
                <span
                  className="text-[10px] text-white/40 flex items-center gap-1"
                  title="Temps passé sur cette question"
                >
                  <Clock className="w-2.5 h-2.5" />
                  {formatDuration(questionTimes[currentQ])}
                </span>
              )}
              <span className="text-[10px] text-white/40 ml-auto">Correction après la remise</span>
            </div>
            <AnswerInput
              questionContent={question.content}
              questionType={question.type}
              choices={question.choices}
              itemsLeft={question.items_left}
              itemsRight={question.items_right}
              value={answers[currentQ] || ''}
              onChange={(val) => setAnswers((prev) => ({ ...prev, [currentQ]: val }))}
              onImageChange={(img) => setImageData((prev) => ({ ...prev, [currentQ]: img }))}
              disabled={isTimeUp}
              placeholder="Écrivez votre réponse ici..."
              subject={exam?.subject}
            />
          </div>
        </div>

        {/* --- MOBILE + LANDSCAPE PHONE: stacked layout (<lg) --- */}
        <div className="lg:hidden flex-1 min-w-0 overflow-y-auto">
          <div className="px-3 py-3 space-y-3">
            <div className="flex items-center gap-2">
              <span className={`text-[11px] font-bold px-2 py-0.5 rounded-md ${badge.bg} ${badge.text}`}>{badge.label}</span>
              {question.exercise && <span className="text-[11px] text-white/55">{question.exercise}</span>}
            </div>

            <QuestionRenderer question={question} examId={exam.id}>
              <AnswerInput
                questionContent={question.content}
                questionType={question.type}
                choices={question.choices}
                itemsLeft={question.items_left}
                itemsRight={question.items_right}
                value={answers[currentQ] || ''}
                onChange={(val) => setAnswers((prev) => ({ ...prev, [currentQ]: val }))}
                onImageChange={(img) => setImageData((prev) => ({ ...prev, [currentQ]: img }))}
                disabled={isTimeUp}
                placeholder="Écrivez votre réponse ici..."
                subject={exam?.subject}
              />
            </QuestionRenderer>

            {/* Mobile nav */}
            <div className="flex items-center justify-between pt-3 border-t border-white/10">
              <button onClick={goPrev} disabled={currentQ === 0} className="flex items-center gap-1.5 px-3 py-2 glass rounded-lg text-white/70 text-xs font-medium disabled:opacity-30">
                <ArrowLeft className="w-3.5 h-3.5" /> Préc
              </button>
              <div className="flex gap-1 flex-wrap justify-center max-w-[180px]">
                {exam.questions.map((_, qIdx) => (
                  <button key={qIdx} onClick={() => setCurrentQ(qIdx)} className={`w-6 h-6 rounded-md text-[9px] font-bold ${qIdx === currentQ ? 'bg-red-600 text-white' : answers[qIdx]?.trim() ? 'bg-emerald-500/15 text-emerald-200 border border-emerald-400/30' : 'bg-white/10 text-white/55'}`}>
                    {qIdx + 1}
                  </button>
                ))}
              </div>
              {currentQ < exam.questions.length - 1 ? (
                <button onClick={goNext} className="flex items-center gap-1.5 px-3 py-2 text-white rounded-lg text-xs font-medium bg-gradient-to-r from-red-500 to-rose-600">
                  Suiv <ArrowRight className="w-3.5 h-3.5" />
                </button>
              ) : (
                <button onClick={() => setShowConfirmSubmit(true)} className="flex items-center gap-1.5 px-3 py-2 bg-emerald-500 text-white rounded-lg text-xs font-medium">
                  <Send className="w-3.5 h-3.5" /> Rendre
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Confirm submit dialog */}
      {showConfirmSubmit && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 overflow-y-auto" onClick={onClose}>
          <div onClick={(e) => e.stopPropagation()} className="glass-strong rounded-2xl shadow-2xl w-full max-w-md overflow-hidden my-4">
            <div className="bg-gradient-to-r from-emerald-600 to-teal-600 px-6 py-5 text-white">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-lg font-bold">Rendre la copie ?</h3>
                  <p className="text-xs text-emerald-200 mt-0.5">La correction détaillée sera affichée après la remise</p>
                </div>
                <button onClick={onClose} className="p-1 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-2 gap-2.5 mb-4">
                <div className="bg-blue-500/10 border border-white/5 rounded-xl p-3 text-center">
                  <p className="text-[10px] font-bold text-blue-200 uppercase tracking-wider mb-1">Temps restant</p>
                  <p className="text-lg font-black text-blue-200">{formatTime(timeLeft)}</p>
                </div>
                <div className="bg-emerald-500/10 border border-emerald-400/30 rounded-xl p-3 text-center">
                  <p className="text-[10px] font-bold text-emerald-200 uppercase tracking-wider mb-1">Répondues</p>
                  <p className="text-lg font-black text-emerald-200">
                    {answeredCount}<span className="text-sm text-emerald-300/70">/{exam.question_count}</span>
                  </p>
                </div>
              </div>
              {answeredCount < exam.question_count && (
                <div className="bg-amber-500/10 border border-amber-400/30 rounded-xl p-3 text-[12.5px] text-amber-200 flex items-start gap-2 mb-4">
                  <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                  <span>
                    Il te reste <b>{exam.question_count - answeredCount}</b> question{exam.question_count - answeredCount > 1 ? 's' : ''} sans réponse.
                    Les questions non répondues seront comptées 0.
                  </span>
                </div>
              )}
              {answeredCount === exam.question_count && (
                <div className="bg-emerald-500/10 border border-emerald-400/30 rounded-xl p-3 text-[12.5px] text-emerald-200 flex items-start gap-2 mb-4">
                  <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" />
                  <span>Toutes les questions ont une réponse. Tu peux rendre ta copie en toute confiance.</span>
                </div>
              )}
              <div className="flex gap-3">
                <button
                  onClick={() => setShowConfirmSubmit(false)}
                  className="flex-1 px-4 py-2.5 border border-white/15 text-white/85 rounded-xl font-medium hover:bg-white/[.06] transition-colors"
                >
                  Continuer
                </button>
                <button
                  onClick={doSubmit}
                  disabled={submitting}
                  className="flex-[1.5] px-4 py-2.5 bg-emerald-600 text-white rounded-xl font-semibold hover:bg-emerald-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {submitting ? (
                    <><Loader2 className="w-4 h-4 animate-spin" /> Correction en cours…</>
                  ) : (
                    <><Send className="w-4 h-4" /> Confirmer la remise</>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

interface RealExamShareModalProps {
  firstName: string;
  exam: ExamData;
  rawScore: number;
  maxScore: number;
  scoreOn20: number;
  percent: number;
  mention: ReturnType<typeof getMention>;
  sessionLabel: string;
  answeredCount: number;
  questionCount: number;
  durationSeconds: number;
  onClose: () => void;
}

function RealExamShareModal({
  firstName,
  exam,
  rawScore,
  maxScore,
  scoreOn20,
  percent,
  mention,
  sessionLabel,
  answeredCount,
  questionCount,
  durationSeconds,
  onClose,
}: RealExamShareModalProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [generating, setGenerating] = useState(false);
  const [downloaded, setDownloaded] = useState(false);
  const [copied, setCopied] = useState(false);
  const [fileShareUnsupported, setFileShareUnsupported] = useState(false);

  // Text WITH the URL inline — used for clipboard / WhatsApp / Facebook quote
  const shareText =
    `🎓 ${firstName} a réussi un examen BAC avec Moalim ! ${mention.emoji}\n` +
    `📘 ${exam.subject} ${exam.year} · Session ${sessionLabel}\n` +
    `✅ Note : ${scoreOn20.toFixed(2)}/20 · ${percent}% de réussite\n` +
    `🏅 Mention ${mention.label}\n\n` +
    `👉 Découvre la plateforme : ${MOALIM_URL}`;
  // Same text WITHOUT the URL — used for Web Share API + Twitter (which append url separately)
  const shareTextNoUrl =
    `🎓 ${firstName} a réussi un examen BAC avec Moalim ! ${mention.emoji}\n` +
    `📘 ${exam.subject} ${exam.year} · Session ${sessionLabel}\n` +
    `✅ Note : ${scoreOn20.toFixed(2)}/20 · ${percent}% de réussite\n` +
    `🏅 Mention ${mention.label}`;
  const shareTextShort =
    `🎓 ${firstName} : ${exam.subject} ${exam.year} — ${scoreOn20.toFixed(2)}/20 ${mention.emoji}`;

  const encodedText = encodeURIComponent(shareText);
  const encodedShort = encodeURIComponent(shareTextShort);
  const encodedUrl = encodeURIComponent(MOALIM_URL);
  const safeName = firstName.replace(/\s+/g, '_').replace(/[^\w-]/g, '');
  const fileName = `reussite-bac-${exam.subject.toLowerCase()}-${exam.year}-${safeName || 'eleve'}.png`;

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

  const shareNative = async () => {
    setGenerating(true);
    setFileShareUnsupported(false);
    try {
      const blob = await generatePng();
      if (!blob) return;
      const file = new File([blob], fileName, { type: 'image/png' });
      const nav: any = navigator;
      const shareData: any = {
        title: 'Moalim — Ma réussite BAC',
        text: shareTextNoUrl,
        url: MOALIM_URL,
        files: [file],
      };
      if (nav.canShare && nav.canShare({ files: [file] })) {
        await nav.share(shareData);
        onClose();
      } else {
        await downloadImage(blob);
        setFileShareUnsupported(true);
      }
    } catch (e) {
      console.warn('Share failed:', e);
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = async () => {
    setGenerating(true);
    try { await downloadImage(); } finally { setGenerating(false); }
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
    { name: 'WhatsApp', color: 'bg-[#25D366] hover:bg-[#1ebe5d]', url: `https://wa.me/?text=${encodedText}` },
    { name: 'X', color: 'bg-black hover:bg-zinc-800', url: `https://twitter.com/intent/tweet?text=${encodedShort}&url=${encodedUrl}` },
    { name: 'Facebook', color: 'bg-[#1877F2] hover:bg-[#0f63d1]', url: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}&quote=${encodedShort}` },
  ];

  const handleNetworkClick = async (e: React.MouseEvent<HTMLAnchorElement>, net: { name: string; url: string }) => {
    e.preventDefault();
    try { await navigator.clipboard.writeText(shareText); } catch { /* noop */ }
    await downloadImage();
    window.open(net.url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 overflow-y-auto" onClick={onClose}>
      <div onClick={(e) => e.stopPropagation()} className="glass-strong rounded-2xl shadow-2xl w-full max-w-md overflow-hidden my-4">
        <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-900 px-6 py-5 text-white">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="text-lg font-bold">Partager ma réussite</h3>
              <p className="text-xs text-indigo-100 mt-1">
                {exam.subject} {exam.year} · {scoreOn20.toFixed(2)}/20 · Mention {mention.label}
              </p>
            </div>
            <button onClick={onClose} className="p-1 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div className="px-4 pt-4 pb-2">
          <a href={MOALIM_URL} target="_blank" rel="noopener noreferrer" className="block rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow" title={`Ouvrir ${MOALIM_URL}`}>
            <RealExamShareCard
              ref={cardRef}
              firstName={firstName}
              exam={exam}
              rawScore={rawScore}
              maxScore={maxScore}
              scoreOn20={scoreOn20}
              percent={percent}
              mention={mention}
              sessionLabel={sessionLabel}
              answeredCount={answeredCount}
              questionCount={questionCount}
              durationSeconds={durationSeconds}
            />
          </a>
          <p className="text-[10px] text-center text-white/40 mt-2">
            L'aperçu est cliquable ici. Sur les réseaux, le lien partagé redirige vers{' '}
            <span className="font-semibold text-indigo-300">moalim.online</span>
          </p>
        </div>

        <div className="px-6 pt-2 pb-2 space-y-2">
          <button onClick={shareNative} disabled={generating} className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-indigo-600 to-blue-700 text-white rounded-xl text-sm font-bold hover:shadow-lg transition-all disabled:opacity-60">
            {generating ? (
              <><Loader2 className="w-4 h-4 animate-spin" /> Génération…</>
            ) : (
              <><Share2 className="w-4 h-4" /> Partager l'image + lien</>
            )}
          </button>
          <div className="grid grid-cols-2 gap-2">
            <button onClick={handleDownload} disabled={generating} className="flex items-center justify-center gap-1.5 px-3 py-2 glass rounded-xl text-xs font-semibold text-white/85 hover:border-indigo-400 hover:text-indigo-300 transition-colors disabled:opacity-60">
              {downloaded ? (
                <><Check className="w-3.5 h-3.5 text-emerald-300" /><span className="text-emerald-300">Téléchargée</span></>
              ) : (
                <>📥 Télécharger l'image</>
              )}
            </button>
            <button onClick={copyText} className="flex items-center justify-center gap-1.5 px-3 py-2 glass rounded-xl text-xs font-semibold text-white/85 hover:border-indigo-400 hover:text-indigo-300 transition-colors">
              {copied ? (
                <><Check className="w-3.5 h-3.5 text-emerald-300" /><span className="text-emerald-300">Texte copié</span></>
              ) : (
                <><Copy className="w-3.5 h-3.5" /> Copier le texte</>
              )}
            </button>
          </div>
          {fileShareUnsupported && (
            <p className="text-[11px] text-amber-200 bg-amber-500/10 border border-amber-400/30 rounded-lg px-3 py-2">
              Image téléchargée ! Ton navigateur ne supporte pas le partage de fichier — joins-la manuellement à ton post.
            </p>
          )}
        </div>

        <div className="px-6 py-4">
          <p className="text-xs font-semibold text-white/55 uppercase tracking-wider mb-2">Ou directement sur un réseau</p>
          <div className="grid grid-cols-3 gap-2">
            {networks.map((net) => (
              <a
                key={net.name}
                href={net.url}
                onClick={(e) => handleNetworkClick(e, net)}
                target="_blank"
                rel="noopener noreferrer"
                className={`flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-xl ${net.color} text-white text-xs font-semibold transition-all hover:shadow-md`}
              >
                {net.name}
              </a>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

const RealExamShareCard = forwardRef<
  HTMLDivElement,
  {
    firstName: string;
    exam: ExamData;
    rawScore: number;
    maxScore: number;
    scoreOn20: number;
    percent: number;
    mention: ReturnType<typeof getMention>;
    sessionLabel: string;
    answeredCount: number;
    questionCount: number;
    durationSeconds: number;
  }
>(function RealExamShareCardImpl({
  firstName, exam, rawScore, maxScore, scoreOn20, percent, mention,
  sessionLabel, answeredCount, questionCount, durationSeconds,
}, ref) {
  return (
    <div
      ref={ref}
      style={{
        width: 480,
        fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 42%, #312e81 100%)',
        color: 'white',
        padding: 28,
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <div style={{ position: 'absolute', top: -44, right: -44, width: 170, height: 170, borderRadius: '50%', background: 'rgba(99,102,241,0.26)', filter: 'blur(30px)' }} />
      <div style={{ position: 'absolute', bottom: -50, left: -34, width: 190, height: 190, borderRadius: '50%', background: 'rgba(16,185,129,0.18)', filter: 'blur(35px)' }} />
      <div style={{ position: 'relative' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 22 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{ width: 38, height: 38, borderRadius: 12, background: 'linear-gradient(135deg, #6366f1, #3b82f6)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 19, fontWeight: 900 }}>م</div>
            <div>
              <div style={{ fontSize: 15, fontWeight: 900, letterSpacing: 0.2 }}>Moalim</div>
              <div style={{ fontSize: 10, color: '#94a3b8' }}>Tuteur IA pour le BAC Maroc</div>
            </div>
          </div>
          <div style={{ fontSize: 30 }}>{mention.emoji}</div>
        </div>

        <div style={{ marginBottom: 20 }}>
          <div style={{ fontSize: 12, color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: 1, fontWeight: 800 }}>Réussite BAC partagée</div>
          <div style={{ fontSize: 23, fontWeight: 950, marginTop: 5 }}>{firstName}</div>
          <div style={{ fontSize: 14, color: '#cbd5e1', marginTop: 2 }}>{exam.subject} {exam.year} · Session {sessionLabel}</div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 18, background: 'rgba(255,255,255,0.09)', borderRadius: 20, padding: 18, border: '1px solid rgba(255,255,255,0.13)', marginBottom: 14 }}>
          <div style={{ width: 120, height: 120, borderRadius: '50%', background: scoreOn20 >= 10 ? 'linear-gradient(135deg, #10b981, #0d9488)' : 'linear-gradient(135deg, #f59e0b, #ef4444)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', boxShadow: '0 12px 28px rgba(0,0,0,0.38)', flexShrink: 0 }}>
            <div style={{ fontSize: 34, fontWeight: 950, lineHeight: 1 }}>{scoreOn20.toFixed(2)}</div>
            <div style={{ fontSize: 11, fontWeight: 800, opacity: 0.88, marginTop: 2 }}>/ 20</div>
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 11, color: '#a5b4fc', fontWeight: 800, textTransform: 'uppercase', letterSpacing: 0.8 }}>Mention obtenue</div>
            <div style={{ fontSize: 23, fontWeight: 950, marginTop: 2 }}>{mention.emoji} {mention.label}</div>
            <div style={{ fontSize: 12, color: '#cbd5e1', marginTop: 7, lineHeight: 1.45 }}>{rawScore.toFixed(2)}/{maxScore} pts · {percent}% de réussite</div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8, marginBottom: 14 }}>
          <div style={{ background: 'rgba(255,255,255,0.07)', borderRadius: 12, padding: 10, border: '1px solid rgba(255,255,255,0.08)' }}>
            <div style={{ fontSize: 17, fontWeight: 900 }}>{answeredCount}/{questionCount}</div>
            <div style={{ fontSize: 9, color: '#94a3b8', fontWeight: 700, marginTop: 2 }}>Questions</div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.07)', borderRadius: 12, padding: 10, border: '1px solid rgba(255,255,255,0.08)' }}>
            <div style={{ fontSize: 17, fontWeight: 900 }}>{formatDuration(durationSeconds)}</div>
            <div style={{ fontSize: 9, color: '#94a3b8', fontWeight: 700, marginTop: 2 }}>Durée</div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.07)', borderRadius: 12, padding: 10, border: '1px solid rgba(255,255,255,0.08)' }}>
            <div style={{ fontSize: 17, fontWeight: 900 }}>{percent}%</div>
            <div style={{ fontSize: 9, color: '#94a3b8', fontWeight: 700, marginTop: 2 }}>Réussite</div>
          </div>
        </div>

        <div style={{ background: 'rgba(255,255,255,0.06)', borderRadius: 14, padding: 14, fontSize: 12, color: '#e2e8f0', lineHeight: 1.5, border: '1px solid rgba(255,255,255,0.08)' }}>
          {mention.encouragement}
        </div>
        <div style={{ marginTop: 16, display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: 11, color: '#94a3b8' }}>
          <div>🚀 Prépare ton BAC avec moi</div>
          <div style={{ fontWeight: 900, color: '#a5b4fc' }}>{MOALIM_URL.replace('https://', '')}</div>
        </div>
      </div>
    </div>
  );
});
