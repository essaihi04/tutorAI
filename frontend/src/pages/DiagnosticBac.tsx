import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getBacDiagnosticQuestions, submitBacDiagnostic } from '../services/api';
import LatexRenderer from '../components/LatexRenderer';
import BacCountdown from '../components/BacCountdown';
import {
  ArrowLeft, ArrowRight, CheckCircle, Loader2, Brain,
  Check, HelpCircle, Zap, Trophy,
} from 'lucide-react';

interface Choice { letter: string; text: string }
interface Question {
  id: string;
  position: number;
  subject: string;
  domain: string;
  year: number;
  session: string;
  content: string;
  choices: Choice[];
  type: string;
}

const SUBJECT_COLOR: Record<string, string> = {
  'SVT': 'from-emerald-600 to-teal-600',
  'Physique-Chimie': 'from-blue-600 to-indigo-600',
  'Mathématiques': 'from-violet-600 to-purple-600',
};
const SUBJECT_ICON: Record<string, string> = {
  'SVT': '🧬',
  'Physique-Chimie': '⚗️',
  'Mathématiques': '📐',
};

export default function DiagnosticBac() {
  const navigate = useNavigate();
  const [phase, setPhase] = useState<'intro' | 'loading' | 'quiz' | 'submitting'>('intro');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [sessionId, setSessionId] = useState('');
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [current, setCurrent] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const currentQ = questions[current];
  const total = questions.length || 20;
  const answeredCount = Object.keys(answers).length;
  const currentAns = currentQ ? answers[String(currentQ.position)] : undefined;
  const isAnswered = !!currentAns;
  const isLast = current === questions.length - 1;
  const allAnswered = answeredCount === questions.length && questions.length > 0;

  const loadQuestions = async () => {
    setPhase('loading');
    setError(null);
    try {
      const res = await getBacDiagnosticQuestions();
      setQuestions(res.data.questions);
      setSessionId(res.data.session_id);
      setAnswers({});
      setCurrent(0);
      setPhase('quiz');
    } catch {
      setError('Impossible de charger les questions. Réessaie.');
      setPhase('intro');
    }
  };

  const pick = (letter: string) => {
    if (!currentQ) return;
    setAnswers(prev => ({ ...prev, [String(currentQ.position)]: letter }));
  };

  const goTo = (idx: number) => {
    setCurrent(idx);
    containerRef.current?.scrollTo({ top: 0, behavior: 'smooth' });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleNext = () => {
    if (!isLast) {
      goTo(current + 1);
    }
  };

  const handleSubmit = async () => {
    setPhase('submitting');
    try {
      const res = await submitBacDiagnostic(sessionId, answers);
      navigate('/bac-diagnostic/results', { state: { results: res.data } });
    } catch {
      setError('Erreur lors de la soumission. Réessaie.');
      setPhase('quiz');
    }
  };

  // ── INTRO ────────────────────────────────────────────────────────────────
  if (phase === 'intro') {
    return (
      <div className="min-h-screen bg-[#070718] text-white flex items-center justify-center p-4 relative overflow-hidden">
        {/* Ambient glow */}
        <div className="pointer-events-none absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-indigo-600/20 blur-[120px] rounded-full" />
        <div className="pointer-events-none absolute bottom-0 right-0 w-[400px] h-[300px] bg-emerald-600/15 blur-[100px] rounded-full" />

        <div className="max-w-lg w-full relative z-10">
          {/* Countdown banner */}
          <div className="mb-6 bg-red-500/10 border border-red-400/25 rounded-2xl p-4">
            <p className="text-center text-red-200 text-xs font-bold mb-3 uppercase tracking-widest">
              🔥 Temps restant avant l'Examen National BAC 2026
            </p>
            <BacCountdown size="lg" />
            <p className="text-center text-white/30 text-[10px] mt-2">4 Juin 2026 · 08h00</p>
          </div>

          {/* Main card */}
          <div className="bg-white/[.04] border border-white/10 rounded-3xl p-8 shadow-2xl backdrop-blur-sm">
            <div className="text-center mb-6">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center mx-auto mb-4 shadow-lg shadow-indigo-500/30">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h1 className="text-2xl sm:text-3xl font-black text-white mb-2">
                Teste ton niveau BAC
              </h1>
              <p className="text-white/60 text-sm leading-relaxed">
                20 questions tirées des <span className="text-white font-semibold">vrais examens BAC marocains</span>.
                Découvre ta note estimée et ton plan de révision personnalisé.
              </p>
            </div>

            {/* Stats row */}
            <div className="grid grid-cols-3 gap-3 mb-6">
              {[
                { icon: '📝', label: '20 questions', sub: 'SVT + PC + Maths' },
                { icon: '⏱️', label: '~15 minutes', sub: 'à ton rythme' },
                { icon: '🎯', label: 'Note /20', sub: 'prédite BAC' },
              ].map((s, i) => (
                <div key={i} className="bg-white/[.03] border border-white/8 rounded-xl p-3 text-center">
                  <div className="text-2xl mb-1">{s.icon}</div>
                  <div className="text-white font-semibold text-xs">{s.label}</div>
                  <div className="text-white/45 text-[10px]">{s.sub}</div>
                </div>
              ))}
            </div>

            {/* What you get */}
            <div className="bg-indigo-500/10 border border-indigo-400/20 rounded-xl p-4 mb-6">
              <p className="text-indigo-200 text-xs font-semibold mb-2">📊 À la fin tu obtiendras :</p>
              <ul className="space-y-1.5">
                {[
                  'Ta note estimée au BAC (sur 20)',
                  'Tes points forts et tes lacunes par chapitre',
                  'Un plan de révision personnalisé jour par jour',
                  'Le nombre de points que tu peux encore gagner',
                ].map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-white/75">
                    <Check className="w-3.5 h-3.5 text-indigo-300 mt-0.5 flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            {error && (
              <div className="mb-4 p-3 bg-red-500/15 border border-red-400/30 rounded-lg text-red-200 text-sm">
                {error}
              </div>
            )}

            <button
              onClick={loadQuestions}
              className="w-full py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-bold text-base shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:scale-[1.01] active:scale-[0.99] transition-all"
            >
              <span className="flex items-center justify-center gap-2">
                <Zap className="w-5 h-5" />
                Commencer le diagnostic gratuit
              </span>
            </button>
            <p className="text-center text-white/30 text-xs mt-3">Gratuit · Sans inscription · Questions d'entraînement niveau BAC</p>
          </div>
        </div>
      </div>
    );
  }

  // ── LOADING ──────────────────────────────────────────────────────────────
  if (phase === 'loading') {
    return (
      <div className="min-h-screen bg-[#070718] text-white flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-10 h-10 text-indigo-400 animate-spin mx-auto mb-4" />
          <p className="text-white/60">Chargement des questions BAC…</p>
        </div>
      </div>
    );
  }

  // ── QUIZ ─────────────────────────────────────────────────────────────────
  if ((phase === 'quiz' || phase === 'submitting') && currentQ) {
    const progress = (answeredCount / total) * 100;
    const gradClass = SUBJECT_COLOR[currentQ.subject] || 'from-blue-600 to-indigo-600';

    return (
      <div ref={containerRef} className="min-h-screen bg-[#070718] text-white flex flex-col">
        {/* ── Sticky header ── */}
        <div className="sticky top-0 z-20 bg-[#070718]/90 backdrop-blur-xl border-b border-white/5">
          <div className="max-w-2xl mx-auto px-4 py-2">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-base">{SUBJECT_ICON[currentQ.subject] || '📚'}</span>
                <span className="text-xs font-semibold text-white/70">{currentQ.subject}</span>
              </div>
              <div className="flex items-center gap-3">
                <BacCountdown size="sm" />
                <span className="text-xs font-bold text-white">{answeredCount}/{total}</span>
              </div>
            </div>

            {/* Dot navigation */}
            <div className="flex gap-1 mb-2 overflow-x-auto pb-1">
              {questions.map((q, i) => {
                const a = answers[String(q.position)];
                const isActive = i === current;
                return (
                  <button
                    key={i}
                    onClick={() => goTo(i)}
                    className={`flex-shrink-0 w-6 h-6 rounded-md text-[10px] font-bold transition-all ${
                      isActive
                        ? `bg-gradient-to-br ${gradClass} text-white shadow-md scale-110`
                        : a
                        ? 'bg-emerald-500/80 text-white'
                        : 'bg-white/10 text-white/50 hover:bg-white/15'
                    }`}
                  >
                    {i + 1}
                  </button>
                );
              })}
            </div>

            {/* Progress bar */}
            <div className="w-full bg-white/5 rounded-full h-1 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        </div>

        {/* ── Question ── */}
        <div className="flex-1 max-w-2xl mx-auto w-full px-4 py-6">
          {error && (
            <div className="mb-4 p-3 bg-red-500/15 border border-red-400/30 rounded-xl text-red-200 text-sm">
              {error}
            </div>
          )}

          <div className={`bg-white/[.03] border border-white/10 rounded-2xl shadow-xl overflow-hidden mb-4`}>
            {/* Question header */}
            <div className={`bg-gradient-to-r ${gradClass} px-4 py-3 flex items-center gap-3`}>
              <div className="w-8 h-8 bg-white/20 rounded-xl flex items-center justify-center font-black text-sm">
                {current + 1}
              </div>
              <div>
                <div className="text-white/80 text-[10px] font-semibold uppercase tracking-wider">
                  {currentQ.domain || currentQ.subject}
                </div>
                <div className="text-white/60 text-[10px]">Question d'entraînement · {currentQ.subject}</div>
              </div>
              {isAnswered && <CheckCircle className="w-5 h-5 text-white/70 ml-auto" />}
            </div>

            {/* Question content */}
            <div className="px-4 pt-4 pb-3">
              <p className="text-white text-sm sm:text-base leading-relaxed font-medium">
                <LatexRenderer content={currentQ.content} />
              </p>
            </div>

            {/* Choices */}
            <div className="px-4 pb-4 space-y-2">
              {currentQ.choices.map((c) => {
                const isSelected = currentAns === c.letter;
                return (
                  <button
                    key={c.letter}
                    onClick={() => pick(c.letter)}
                    className={`w-full text-left p-3 rounded-xl border-2 transition-all flex items-center gap-3 active:scale-[0.99] ${
                      isSelected
                        ? `border-indigo-400/60 bg-indigo-500/15 shadow-md`
                        : 'border-white/10 hover:border-indigo-400/40 hover:bg-white/[.04]'
                    }`}
                  >
                    <span className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-black flex-shrink-0 transition-all ${
                      isSelected ? 'bg-indigo-600 text-white' : 'bg-white/8 text-white/60'
                    }`}>
                      {c.letter.toUpperCase()}
                    </span>
                    <span className="text-white text-sm flex-1">
                      <LatexRenderer content={c.text} />
                    </span>
                    {isSelected && <Check className="w-4 h-4 text-indigo-300 flex-shrink-0" />}
                  </button>
                );
              })}
              {/* Skip option */}
              <button
                onClick={() => pick('skip')}
                className={`w-full text-left px-3 py-2 rounded-xl border-2 transition-all flex items-center gap-2 text-xs ${
                  currentAns === 'skip'
                    ? 'border-slate-500/60 bg-white/5 text-white/70'
                    : 'border-dashed border-white/15 hover:border-white/25 text-white/40 hover:text-white/60'
                }`}
              >
                <HelpCircle className="w-3.5 h-3.5" />
                <span className="italic">Je ne sais pas</span>
              </button>
            </div>
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-between gap-3">
            <button
              onClick={() => goTo(Math.max(0, current - 1))}
              disabled={current === 0}
              className="px-4 py-2.5 bg-white/5 text-white/80 rounded-xl font-semibold hover:bg-white/10 disabled:opacity-30 flex items-center gap-1.5 text-sm transition-all"
            >
              <ArrowLeft className="w-4 h-4" /> Précédent
            </button>

            {!isLast ? (
              <button
                onClick={handleNext}
                disabled={!isAnswered}
                className="flex-1 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-bold shadow-lg disabled:opacity-40 flex items-center justify-center gap-2 text-sm transition-all hover:shadow-xl"
              >
                Suivant <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={!allAnswered || phase === 'submitting'}
                className="flex-1 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-xl font-bold shadow-lg disabled:opacity-40 flex items-center justify-center gap-2 text-sm transition-all hover:shadow-xl"
              >
                {phase === 'submitting' ? (
                  <><Loader2 className="w-4 h-4 animate-spin" /> Calcul en cours…</>
                ) : (
                  <><Trophy className="w-4 h-4" /> Voir mes résultats</>
                )}
              </button>
            )}
          </div>

          {isLast && !allAnswered && (
            <p className="text-center text-white/40 text-xs mt-3">
              Réponds à toutes les questions pour voir tes résultats
              ({questions.length - answeredCount} restante{questions.length - answeredCount > 1 ? 's' : ''})
            </p>
          )}
        </div>
      </div>
    );
  }

  return null;
}
