import { useState } from 'react';
import { BookOpen, CheckCircle, Eye, EyeOff, Award, ChevronDown, ChevronUp } from 'lucide-react';

interface ExamExercise {
  exam_id: string;
  exam_label: string;
  subject: string;
  year: number;
  session: string;
  question_index: number;
  part_name?: string;
  exercise_name?: string;
  exercise_context?: string;
  topic?: string;
  content: string;
  type: string;
  points: number;
  correction: string;
  choices?: { letter: string; text: string }[];
  correct_answer?: string | boolean;
}

interface Props {
  exercises: ExamExercise[];
}

export default function ExamExerciseCard({ exercises }: Props) {
  const [revealedCorrections, setRevealedCorrections] = useState<Record<number, boolean>>({});
  const [studentAnswers, setStudentAnswers] = useState<Record<number, string>>({});
  const [expandedContext, setExpandedContext] = useState<Record<number, boolean>>({});

  const toggleCorrection = (idx: number) => {
    setRevealedCorrections((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  const toggleContext = (idx: number) => {
    setExpandedContext((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <div className="space-y-3 w-full max-w-[95%]">
      <div className="flex items-center gap-2 mb-1">
        <div className="w-6 h-6 rounded-lg bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center">
          <BookOpen className="w-3.5 h-3.5 text-white" />
        </div>
        <span className="text-xs font-bold text-amber-300">Exercice du BAC National</span>
      </div>

      {exercises.map((ex, idx) => (
        <div
          key={`${ex.exam_id}-${ex.question_index}-${idx}`}
          className="bg-white/[0.05] border border-white/10 rounded-xl overflow-hidden"
        >
          {/* Header */}
          <div className="px-4 py-2.5 bg-white/[0.03] border-b border-white/5 flex items-center justify-between">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-[10px] font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded-md">
                BAC {ex.year} {ex.session === 'normale' ? 'N' : 'R'}
              </span>
              {ex.topic && (
                <span className="text-[10px] text-white/40">{ex.topic}</span>
              )}
              {ex.exercise_name && (
                <span className="text-[10px] text-white/30">— {ex.exercise_name}</span>
              )}
            </div>
            <div className="flex items-center gap-1.5">
              <Award className="w-3 h-3 text-amber-400" />
              <span className="text-[11px] font-bold text-amber-300">{ex.points} pts</span>
            </div>
          </div>

          {/* Context (collapsible) */}
          {ex.exercise_context && (
            <div className="px-4 pt-2">
              <button
                onClick={() => toggleContext(idx)}
                className="flex items-center gap-1 text-[10px] text-white/40 hover:text-white/60 transition-colors"
              >
                {expandedContext[idx] ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                Contexte de l'exercice
              </button>
              {expandedContext[idx] && (
                <p className="text-[11px] text-white/50 mt-1 pl-4 border-l border-white/10 leading-relaxed">
                  {ex.exercise_context}
                </p>
              )}
            </div>
          )}

          {/* Question */}
          <div className="px-4 py-3">
            <p className="text-sm text-white/90 leading-relaxed whitespace-pre-wrap">{ex.content}</p>

            {/* QCM choices */}
            {ex.choices && ex.choices.length > 0 && (
              <div className="mt-2 space-y-1">
                {ex.choices.map((c) => {
                  const isSelected = studentAnswers[idx]?.toLowerCase() === c.letter.toLowerCase();
                  const isCorrect = revealedCorrections[idx] && ex.correct_answer && String(ex.correct_answer).toLowerCase() === c.letter.toLowerCase();
                  return (
                    <button
                      key={c.letter}
                      onClick={() => setStudentAnswers((prev) => ({ ...prev, [idx]: c.letter }))}
                      className={`w-full text-left px-3 py-2 rounded-lg text-xs transition-all border ${
                        isCorrect
                          ? 'border-emerald-500/50 bg-emerald-500/10 text-emerald-300'
                          : isSelected
                          ? 'border-indigo-500/50 bg-indigo-500/10 text-indigo-300'
                          : 'border-white/5 bg-white/[0.02] text-white/70 hover:bg-white/[0.05]'
                      }`}
                    >
                      <span className="font-bold mr-2">{c.letter.toUpperCase()})</span>
                      {c.text}
                      {isCorrect && <CheckCircle className="w-3.5 h-3.5 inline ml-2 text-emerald-400" />}
                    </button>
                  );
                })}
              </div>
            )}

            {/* Open answer input */}
            {ex.type === 'open' && (
              <textarea
                value={studentAnswers[idx] || ''}
                onChange={(e) => setStudentAnswers((prev) => ({ ...prev, [idx]: e.target.value }))}
                placeholder="Écris ta réponse ici pour t'entraîner..."
                rows={3}
                className="w-full mt-2 bg-white/[0.03] border border-white/10 rounded-lg px-3 py-2 text-xs text-white/80 placeholder-white/20 resize-none focus:outline-none focus:border-indigo-500/30"
              />
            )}
          </div>

          {/* Correction toggle */}
          <div className="px-4 pb-3">
            <button
              onClick={() => toggleCorrection(idx)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[11px] font-medium transition-all ${
                revealedCorrections[idx]
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                  : 'bg-white/[0.04] text-white/50 border border-white/10 hover:bg-white/[0.06]'
              }`}
            >
              {revealedCorrections[idx] ? (
                <><EyeOff className="w-3 h-3" /> Masquer la correction</>
              ) : (
                <><Eye className="w-3 h-3" /> Voir la correction officielle</>
              )}
            </button>

            {revealedCorrections[idx] && (
              <div className="mt-2 p-3 bg-emerald-500/5 border border-emerald-500/10 rounded-lg">
                <div className="flex items-center gap-1.5 mb-1.5">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-[10px] font-bold text-emerald-400">Correction officielle</span>
                </div>
                <p className="text-xs text-white/70 leading-relaxed whitespace-pre-wrap">{ex.correction}</p>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
