import React, { useState } from 'react';
import { CheckCircle, Circle, Target, Trophy, ChevronDown, ChevronUp } from 'lucide-react';

interface LessonProgressBarProps {
  objectives: string[];
  completedIndices: number[];
  currentIndex: number;
  lessonTitle: string;
  isResumed?: boolean;
}

export const LessonProgressBar: React.FC<LessonProgressBarProps> = ({
  objectives,
  completedIndices,
  currentIndex,
  lessonTitle,
  isResumed = false,
}) => {
  const [expanded, setExpanded] = useState(false);
  const totalObjectives = objectives.length;
  const completedCount = completedIndices.length;
  const progressPercent = totalObjectives > 0 ? (completedCount / totalObjectives) * 100 : 0;
  const allDone = completedCount === totalObjectives && totalObjectives > 0;

  const getObjectiveStatus = (index: number) => {
    if (completedIndices.includes(index)) return 'completed';
    if (index === currentIndex) return 'current';
    return 'pending';
  };

  return (
    <div className="bg-gradient-to-r from-indigo-900/80 via-purple-900/80 to-indigo-900/80 backdrop-blur-sm rounded-lg shadow border border-indigo-500/20 overflow-hidden">
      {/* Compact header — always visible, clickable to toggle */}
      <button
        type="button"
        onClick={() => setExpanded(v => !v)}
        className="w-full flex items-center gap-2 px-3 py-1.5 hover:bg-white/5 transition-colors"
      >
        <Target className="w-3.5 h-3.5 text-indigo-300 shrink-0" />
        <span className="text-white/90 text-xs font-medium truncate max-w-[180px]">
          {lessonTitle}
        </span>
        {isResumed && (
          <span className="px-1.5 py-0.5 bg-amber-500/20 text-amber-300 text-[10px] rounded-full border border-amber-500/30 shrink-0">
            Reprise
          </span>
        )}
        {allDone && <Trophy className="w-3.5 h-3.5 text-yellow-400 shrink-0" />}

        {/* Thin progress track in header */}
        <div className="flex-1 mx-2 h-1 bg-indigo-950/60 rounded-full overflow-hidden min-w-[40px]">
          <div
            className="h-full bg-gradient-to-r from-green-500 to-teal-400 rounded-full transition-all duration-500"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        <span className="text-indigo-200 text-[11px] tabular-nums shrink-0">
          {completedCount}/{totalObjectives}
        </span>
        <span className="text-white font-semibold text-[11px] tabular-nums shrink-0 w-8 text-right">
          {Math.round(progressPercent)}%
        </span>
        {expanded ? (
          <ChevronUp className="w-3.5 h-3.5 text-indigo-300 shrink-0" />
        ) : (
          <ChevronDown className="w-3.5 h-3.5 text-indigo-300 shrink-0" />
        )}
      </button>

      {/* Expandable objectives list */}
      {expanded && (
        <div className="px-3 pb-2 pt-1 border-t border-indigo-500/20 flex flex-wrap gap-1.5">
          {objectives.map((objective, index) => {
            const status = getObjectiveStatus(index);
            return (
              <div
                key={index}
                className={`
                  flex items-center gap-1 px-2 py-1 rounded-full text-[11px] font-medium
                  transition-all duration-200
                  ${status === 'completed'
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                    : status === 'current'
                      ? 'bg-indigo-500/30 text-white border border-indigo-400'
                      : 'bg-gray-800/50 text-gray-400 border border-gray-700/60'
                  }
                `}
                title={objective}
              >
                {status === 'completed' ? (
                  <CheckCircle className="w-3 h-3" />
                ) : (
                  <Circle className={`w-3 h-3 ${status === 'current' ? 'fill-indigo-400' : ''}`} />
                )}
                <span className="truncate max-w-[180px]">{objective}</span>
              </div>
            );
          })}
          {allDone && (
            <div className="w-full mt-1 text-center text-yellow-400 text-xs font-semibold">
              🎉 Leçon terminée — Bravo !
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LessonProgressBar;
