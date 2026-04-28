import { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getMockExam } from '../services/api';
import { useAuthStore } from '../stores/authStore';
import LatexRenderer from '../components/exam/LatexRenderer';
import {
  Clock, Send, Loader2, ArrowLeft, ArrowRight,
  FileText, Trophy, CheckCircle2, Sparkles,
  AlertTriangle, BookOpen, Award, X,
} from 'lucide-react';

/* ─── Types ───────────────────────────────────────────────── */

interface DocData {
  id: string;
  type: string;
  title: string;
  description: string;
  PROMPT_IMAGE?: string;
  src?: string;
}

interface SubQuestion {
  number?: string;
  content: string;
  points: number;
  choices?: { letter: string; text: string }[];
  correction?: { content?: string; correct_answer?: string };
}

interface QuestionData {
  id?: string;
  number?: string;
  content: string;
  type: string;
  points: number;
  documents?: string[];
  sub_questions?: SubQuestion[];
  choices?: { letter: string; text: string }[];
  items_left?: string[];
  items_right?: string[];
  correct_pairs?: { left: string; right: string }[];
  correction?: { content?: string; correct_answer?: string };
}

interface ExerciseData {
  name: string;
  points: number;
  context?: string;
  documents?: DocData[];
  questions?: QuestionData[];
}

interface PartData {
  name: string;
  points: number;
  questions?: QuestionData[];
  exercises?: ExerciseData[];
}

interface MockExamData {
  id: string;
  title: string;
  subject: string;
  duration_minutes: number;
  total_points: number;
  difficulty: string;
  parts: PartData[];
}

interface FlatQuestion {
  partName: string;
  exerciseName?: string;
  exerciseContext?: string;
  exerciseDocs?: DocData[];
  question: QuestionData;
  globalIdx: number;
}

const TYPE_BADGE: Record<string, { label: string; bg: string; text: string }> = {
  open:        { label: 'Ouverte',     bg: 'bg-blue-500/15',    text: 'text-blue-200' },
  qcm:         { label: 'QCM',         bg: 'bg-violet-500/15',  text: 'text-purple-200' },
  vrai_faux:   { label: 'Vrai / Faux', bg: 'bg-amber-500/15',  text: 'text-amber-200' },
  association: { label: 'Association',  bg: 'bg-rose-500/15',   text: 'text-orange-200' },
};

/* ─── Component ───────────────────────────────────────────── */

export default function MockExamTake() {
  const { subject, examId } = useParams<{ subject: string; examId: string }>();
  const navigate = useNavigate();
  useAuthStore();

  const [exam, setExam] = useState<MockExamData | null>(null);
  const [loading, setLoading] = useState(true);
  const [started, setStarted] = useState(false);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [showCorrection, setShowCorrection] = useState(false);
  const [showConfirmSubmit, setShowConfirmSubmit] = useState(false);

  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const startTimeRef = useRef<number>(0);

  /* Flatten all questions */
  const flatQuestions: FlatQuestion[] = [];
  if (exam) {
    let gIdx = 0;
    for (const part of exam.parts) {
      // Part 1: direct questions
      if (part.questions) {
        for (const q of part.questions) {
          flatQuestions.push({ partName: part.name, question: q, globalIdx: gIdx++ });
        }
      }
      // Part 2: exercises > questions
      if (part.exercises) {
        for (const ex of part.exercises) {
          for (const q of (ex.questions || [])) {
            flatQuestions.push({
              partName: part.name,
              exerciseName: ex.name,
              exerciseContext: ex.context,
              exerciseDocs: ex.documents,
              question: q,
              globalIdx: gIdx++,
            });
          }
        }
      }
    }
  }

  useEffect(() => {
    if (subject && examId) loadExam();
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [subject, examId]);

  const loadExam = async () => {
    setLoading(true);
    try {
      const res = await getMockExam(subject!, examId!);
      setExam(res.data);
      setTimeLeft((res.data.duration_minutes || 180) * 60);
    } catch (e) {
      console.error('Failed to load mock exam:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleStart = () => {
    setStarted(true);
    startTimeRef.current = Date.now();
    const total = (exam?.duration_minutes || 180) * 60;
    setTimeLeft(total);
    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          if (timerRef.current) clearInterval(timerRef.current);
          setShowCorrection(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const handleFinish = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    setShowCorrection(true);
    setShowConfirmSubmit(false);
  };

  const formatTime = (sec: number) => {
    const h = Math.floor(sec / 3600);
    const m = Math.floor((sec % 3600) / 60);
    const s = sec % 60;
    if (h > 0) return `${h}h ${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  const answeredCount = Object.keys(answers).filter(k => answers[Number(k)]?.trim()).length;
  const isLowTime = timeLeft > 0 && timeLeft < 300;

  /* ─── Loading ─── */
  if (loading || !exam) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#070718]">
        <Loader2 className="w-8 h-8 text-violet-400 animate-spin" />
      </div>
    );
  }

  /* ─── Correction Screen ─── */
  if (showCorrection) {
    return (
      <div className="min-h-screen bg-[#070718] text-white pb-10">
        {/* Header */}
        <div className="sticky top-0 z-30 bg-[#070718]/95 backdrop-blur-md border-b border-white/5">
          <div className="max-w-4xl mx-auto px-4 py-3 flex items-center gap-3">
            <button onClick={() => navigate('/mock-exam')} className="p-2 rounded-xl bg-white/5 hover:bg-white/10 transition">
              <ArrowLeft size={18} />
            </button>
            <div className="flex items-center gap-2">
              <Trophy size={20} className="text-amber-400" />
              <h1 className="text-lg font-bold">Correction — {exam.title}</h1>
            </div>
          </div>
        </div>

        <div className="max-w-4xl mx-auto px-4 pt-6 space-y-6">
          {/* Summary Card */}
          <div className="p-5 rounded-2xl bg-gradient-to-r from-violet-600/20 to-purple-600/20 border border-violet-500/20">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 rounded-xl bg-violet-500/20"><CheckCircle2 size={20} className="text-violet-300" /></div>
              <h2 className="text-lg font-bold text-violet-200">Examen terminé !</h2>
            </div>
            <p className="text-sm text-white/50">
              Vous avez répondu à <span className="text-violet-300 font-semibold">{answeredCount}</span> / {flatQuestions.length} questions.
              Consultez les corrections détaillées ci-dessous.
            </p>
          </div>

          {/* All questions with corrections */}
          {flatQuestions.map((fq, idx) => {
            const q = fq.question;
            const studentAns = answers[idx] || '';
            const badge = TYPE_BADGE[q.type] || TYPE_BADGE.open;
            return (
              <div key={idx} className="p-5 rounded-2xl bg-white/[0.03] border border-white/[0.06] space-y-4">
                {/* Part / Exercise label */}
                <div className="flex items-center gap-2 text-xs text-white/30">
                  <span>{fq.partName}</span>
                  {fq.exerciseName && <><span>›</span><span>{fq.exerciseName}</span></>}
                  <span className={`ml-auto px-2 py-0.5 rounded-md ${badge.bg} ${badge.text}`}>{badge.label}</span>
                  <span className="text-violet-300">{q.points} pt{q.points > 1 ? 's' : ''}</span>
                </div>

                {/* Context + Documents */}
                {fq.exerciseContext && idx === 0 || (idx > 0 && flatQuestions[idx - 1].exerciseName !== fq.exerciseName) ? (
                  <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 text-sm text-white/50 leading-relaxed">
                    <LatexRenderer>{fq.exerciseContext || ''}</LatexRenderer>
                  </div>
                ) : null}

                {/* Documents descriptions (images not available yet) */}
                {q.documents && fq.exerciseDocs && (
                  <div className="flex flex-wrap gap-2">
                    {q.documents.map(docId => {
                      const doc = fq.exerciseDocs?.find(d => d.id === docId);
                      if (!doc) return null;
                      return (
                        <div key={docId} className="p-2.5 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-xs max-w-xs">
                          <div className="font-semibold text-indigo-300 mb-1">{doc.title}</div>
                          <p className="text-white/40 leading-relaxed">{doc.description}</p>
                        </div>
                      );
                    })}
                  </div>
                )}

                {/* Question content */}
                <div className="text-sm text-white/80 leading-relaxed">
                  <LatexRenderer>{q.content}</LatexRenderer>
                </div>

                {/* Student's answer */}
                <div className="p-3 rounded-xl bg-white/[0.04] border border-white/5">
                  <div className="text-xs text-white/30 mb-1 font-medium">Votre réponse :</div>
                  <p className="text-sm text-white/60">
                    {studentAns || <span className="italic text-white/20">Pas de réponse</span>}
                  </p>
                </div>

                {/* Correction */}
                <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                  <div className="text-xs text-emerald-300 mb-1 font-medium flex items-center gap-1">
                    <CheckCircle2 size={12} /> Correction :
                  </div>
                  <div className="text-sm text-white/70 leading-relaxed">
                    <LatexRenderer>{q.correction?.content || q.correction?.correct_answer || 'Correction non disponible'}</LatexRenderer>
                  </div>
                  {/* Sub-questions corrections */}
                  {q.sub_questions && q.sub_questions.length > 0 && (
                    <div className="mt-3 space-y-2">
                      {q.sub_questions.map((sq, si) => (
                        <div key={si} className="pl-3 border-l-2 border-emerald-500/20">
                          <div className="text-xs text-white/40 mb-0.5">{sq.content}</div>
                          <div className="text-xs text-emerald-200">
                            {sq.correction?.correct_answer || sq.correction?.content || '—'}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })}

          {/* Back button */}
          <div className="flex justify-center pt-4 pb-8">
            <button
              onClick={() => navigate('/mock-exam')}
              className="px-6 py-3 rounded-xl bg-violet-600 hover:bg-violet-700 text-white font-semibold transition"
            >
              Retour aux examens blancs
            </button>
          </div>
        </div>
      </div>
    );
  }

  /* ─── Pre-start Screen ─── */
  if (!started) {
    const diffCfg: Record<string, string> = { facile: 'text-green-300', moyen: 'text-amber-300', difficile: 'text-red-300' };
    return (
      <div className="min-h-screen bg-[#070718] text-white flex items-center justify-center">
        <div className="max-w-lg mx-auto px-4">
          <div className="p-8 rounded-3xl bg-white/[0.03] border border-white/[0.06] text-center space-y-6">
            <div className="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
              <Sparkles size={28} />
            </div>
            <div>
              <h1 className="text-2xl font-bold mb-2">{exam.title}</h1>
              <p className={`text-sm ${diffCfg[exam.difficulty] || 'text-white/50'}`}>
                Niveau {exam.difficulty}
              </p>
            </div>
            <div className="grid grid-cols-3 gap-3 text-center">
              <div className="p-3 rounded-xl bg-white/5">
                <Clock size={18} className="mx-auto mb-1 text-white/30" />
                <div className="text-lg font-bold">{exam.duration_minutes / 60}h</div>
                <div className="text-[10px] text-white/30">Durée</div>
              </div>
              <div className="p-3 rounded-xl bg-white/5">
                <Award size={18} className="mx-auto mb-1 text-white/30" />
                <div className="text-lg font-bold">{exam.total_points}</div>
                <div className="text-[10px] text-white/30">Points</div>
              </div>
              <div className="p-3 rounded-xl bg-white/5">
                <FileText size={18} className="mx-auto mb-1 text-white/30" />
                <div className="text-lg font-bold">{flatQuestions.length}</div>
                <div className="text-[10px] text-white/30">Questions</div>
              </div>
            </div>
            <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-left">
              <div className="flex items-start gap-2">
                <AlertTriangle size={16} className="text-amber-400 mt-0.5 shrink-0" />
                <p className="text-xs text-amber-200/80 leading-relaxed">
                  L'examen est chronométré. Le temps restant sera affiché en permanence.
                  Vous ne pouvez pas mettre en pause une fois commencé.
                </p>
              </div>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => navigate('/mock-exam')}
                className="flex-1 py-3 rounded-xl bg-white/5 hover:bg-white/10 text-white/60 font-medium transition"
              >
                Retour
              </button>
              <button
                onClick={handleStart}
                className="flex-1 py-3 rounded-xl bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700 text-white font-bold transition"
              >
                Commencer l'examen
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  /* ─── Active Exam ─── */
  const fq = flatQuestions[currentQ];
  const q = fq?.question;
  const badge = q ? (TYPE_BADGE[q.type] || TYPE_BADGE.open) : TYPE_BADGE.open;

  return (
    <div className="min-h-screen bg-[#070718] text-white">
      {/* Timer Bar */}
      <div className={`sticky top-0 z-40 px-4 py-2.5 flex items-center justify-between border-b ${isLowTime ? 'bg-red-900/30 border-red-500/30' : 'bg-[#070718]/95 border-white/5'} backdrop-blur-md`}>
        <div className="flex items-center gap-2 text-sm">
          <button onClick={() => navigate('/mock-exam')} className="p-1.5 rounded-lg bg-white/5 hover:bg-white/10">
            <ArrowLeft size={16} />
          </button>
          <span className="text-white/40">{currentQ + 1} / {flatQuestions.length}</span>
        </div>
        <div className={`flex items-center gap-1.5 font-mono font-bold text-lg ${isLowTime ? 'text-red-400 animate-pulse' : 'text-white/80'}`}>
          <Clock size={16} />
          {formatTime(timeLeft)}
        </div>
        <button
          onClick={() => setShowConfirmSubmit(true)}
          className="px-3 py-1.5 rounded-lg bg-violet-600 hover:bg-violet-700 text-sm font-medium transition"
        >
          <Send size={14} className="inline mr-1" /> Terminer
        </button>
      </div>

      {/* Progress Bar */}
      <div className="h-1 bg-white/5">
        <div
          className="h-full bg-gradient-to-r from-violet-500 to-purple-500 transition-all duration-300"
          style={{ width: `${((currentQ + 1) / flatQuestions.length) * 100}%` }}
        />
      </div>

      {/* Question Area */}
      <div className="max-w-4xl mx-auto px-4 py-6 space-y-4">
        {/* Part / Exercise header */}
        <div className="flex items-center gap-2 text-xs text-white/30">
          <span>{fq.partName}</span>
          {fq.exerciseName && <><span>›</span><span className="text-white/50">{fq.exerciseName}</span></>}
          <span className={`ml-auto px-2 py-0.5 rounded-md ${badge.bg} ${badge.text}`}>{badge.label}</span>
          <span className="text-violet-300">{q.points} pt{q.points > 1 ? 's' : ''}</span>
        </div>

        {/* Context (show once per exercise) */}
        {fq.exerciseContext && (currentQ === 0 || flatQuestions[currentQ - 1]?.exerciseName !== fq.exerciseName) && (
          <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 text-sm text-white/50 leading-relaxed">
            <BookOpen size={14} className="inline mr-1 text-white/30" />
            <LatexRenderer>{fq.exerciseContext || ''}</LatexRenderer>
          </div>
        )}

        {/* Documents */}
        {q.documents && fq.exerciseDocs && (
          <div className="flex flex-wrap gap-2">
            {q.documents.map(docId => {
              const doc = fq.exerciseDocs?.find(d => d.id === docId);
              if (!doc) return null;
              return (
                <div key={docId} className="p-3 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-xs max-w-sm">
                  <div className="font-semibold text-indigo-300 mb-1">{doc.title}</div>
                  <p className="text-white/40 leading-relaxed">{doc.description}</p>
                  {doc.src && !doc.PROMPT_IMAGE && (
                    <img src={`/api/v1/mock-exam/${subject}/${examId}/assets/${doc.src.replace('assets/', '')}`}
                         alt={doc.title} className="mt-2 rounded-lg max-h-60 object-contain" />
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* Question */}
        <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/[0.06]">
          <div className="text-sm text-white/80 leading-relaxed mb-4">
            <LatexRenderer>{q.content}</LatexRenderer>
          </div>

          {/* QCM choices */}
          {q.type === 'qcm' && q.sub_questions && (
            <div className="space-y-3">
              {q.sub_questions.map((sq, si) => (
                <div key={si} className="space-y-1.5">
                  <div className="text-xs text-white/50"><LatexRenderer>{sq.content}</LatexRenderer></div>
                  {sq.choices && (
                    <div className="flex flex-wrap gap-2">
                      {sq.choices.map(c => {
                        const isSelected = (answers[currentQ] || '').includes(`${si + 1}:${c.letter}`);
                        return (
                          <button
                            key={c.letter}
                            onClick={() => {
                              const prev = answers[currentQ] || '';
                              const parts = prev.split(';').filter(p => p.trim() && !p.startsWith(`${si + 1}:`));
                              parts.push(`${si + 1}:${c.letter}`);
                              setAnswers({ ...answers, [currentQ]: parts.join(';') });
                            }}
                            className={`px-3 py-1.5 rounded-lg text-xs transition ${
                              isSelected
                                ? 'bg-violet-600 text-white'
                                : 'bg-white/5 text-white/50 hover:bg-white/10'
                            }`}
                          >
                            {c.letter}. {c.text}
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Vrai/Faux */}
          {q.type === 'vrai_faux' && q.sub_questions && (
            <div className="space-y-2">
              {q.sub_questions.map((sq, si) => {
                const current = (answers[currentQ] || '').split(';').find(p => p.startsWith(`${si}:`))?.split(':')[1];
                return (
                  <div key={si} className="flex items-center gap-3">
                    <span className="text-xs text-white/50 flex-1"><LatexRenderer as="span">{sq.content}</LatexRenderer></span>
                    <div className="flex gap-1.5">
                      {['vrai', 'faux'].map(v => (
                        <button
                          key={v}
                          onClick={() => {
                            const prev = answers[currentQ] || '';
                            const parts = prev.split(';').filter(p => p.trim() && !p.startsWith(`${si}:`));
                            parts.push(`${si}:${v}`);
                            setAnswers({ ...answers, [currentQ]: parts.join(';') });
                          }}
                          className={`px-3 py-1 rounded-lg text-xs transition ${
                            current === v
                              ? 'bg-violet-600 text-white'
                              : 'bg-white/5 text-white/40 hover:bg-white/10'
                          }`}
                        >
                          {v === 'vrai' ? 'Vrai' : 'Faux'}
                        </button>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Association */}
          {q.type === 'association' && q.items_left && q.items_right && (
            <div className="space-y-2">
              {q.items_left.map((item, i) => (
                <div key={i} className="flex items-center gap-3">
                  <span className="text-xs text-white/50 min-w-[120px]">{i + 1}. {item}</span>
                  <select
                    value={(answers[currentQ] || '').split(';').find(p => p.startsWith(`${i + 1}:`))?.split(':')[1] || ''}
                    onChange={(e) => {
                      const prev = answers[currentQ] || '';
                      const parts = prev.split(';').filter(p => p.trim() && !p.startsWith(`${i + 1}:`));
                      if (e.target.value) parts.push(`${i + 1}:${e.target.value}`);
                      setAnswers({ ...answers, [currentQ]: parts.join(';') });
                    }}
                    className="bg-white/5 border border-white/10 rounded-lg px-2 py-1 text-xs text-white/70 focus:outline-none focus:border-violet-500"
                  >
                    <option value="">—</option>
                    {q.items_right!.map((r, ri) => (
                      <option key={ri} value={String.fromCharCode(97 + ri)}>{String.fromCharCode(97 + ri)}. {r}</option>
                    ))}
                  </select>
                </div>
              ))}
            </div>
          )}

          {/* Open answer */}
          {(q.type === 'open' || !['qcm', 'vrai_faux', 'association'].includes(q.type)) && (
            <textarea
              value={answers[currentQ] || ''}
              onChange={(e) => setAnswers({ ...answers, [currentQ]: e.target.value })}
              placeholder="Écrivez votre réponse ici..."
              rows={6}
              className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white/80 placeholder-white/20 focus:outline-none focus:border-violet-500 resize-y"
            />
          )}
        </div>

        {/* Navigation */}
        <div className="flex items-center justify-between pt-2">
          <button
            onClick={() => setCurrentQ(Math.max(0, currentQ - 1))}
            disabled={currentQ === 0}
            className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-sm font-medium disabled:opacity-30 transition"
          >
            <ArrowLeft size={14} /> Précédent
          </button>

          {/* Question dots */}
          <div className="hidden md:flex gap-1 overflow-x-auto max-w-[300px]">
            {flatQuestions.map((_, i) => (
              <button
                key={i}
                onClick={() => setCurrentQ(i)}
                className={`w-6 h-6 rounded-full text-[10px] font-medium transition ${
                  i === currentQ
                    ? 'bg-violet-600 text-white'
                    : answers[i]?.trim()
                    ? 'bg-emerald-500/30 text-emerald-300'
                    : 'bg-white/5 text-white/30 hover:bg-white/10'
                }`}
              >
                {i + 1}
              </button>
            ))}
          </div>

          <button
            onClick={() => setCurrentQ(Math.min(flatQuestions.length - 1, currentQ + 1))}
            disabled={currentQ === flatQuestions.length - 1}
            className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-sm font-medium disabled:opacity-30 transition"
          >
            Suivant <ArrowRight size={14} />
          </button>
        </div>

        {/* Answered counter */}
        <div className="text-center text-xs text-white/25">
          {answeredCount} / {flatQuestions.length} questions répondues
        </div>
      </div>

      {/* Confirm Submit Modal */}
      {showConfirmSubmit && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center">
          <div className="mx-4 max-w-sm w-full p-6 rounded-2xl bg-[#0f0f2a] border border-white/10 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold">Terminer l'examen ?</h3>
              <button onClick={() => setShowConfirmSubmit(false)} className="p-1.5 rounded-lg bg-white/5 hover:bg-white/10">
                <X size={16} />
              </button>
            </div>
            <p className="text-sm text-white/50">
              Vous avez répondu à <span className="text-violet-300 font-semibold">{answeredCount}</span> / {flatQuestions.length} questions.
              {answeredCount < flatQuestions.length && (
                <span className="text-amber-300"> {flatQuestions.length - answeredCount} question(s) sans réponse.</span>
              )}
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowConfirmSubmit(false)}
                className="flex-1 py-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-sm font-medium transition"
              >
                Continuer
              </button>
              <button
                onClick={handleFinish}
                className="flex-1 py-2.5 rounded-xl bg-violet-600 hover:bg-violet-700 text-sm font-bold transition"
              >
                Voir la correction
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
