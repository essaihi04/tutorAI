import { useEffect, useRef } from 'react';
import type { ConversationMessage } from '../../stores/sessionStore';
import ExamExerciseCard from './ExamExerciseCard';

interface ChatHistoryProps {
  messages: ConversationMessage[];
  isProcessing?: boolean;
}

export default function ChatHistory({ messages, isProcessing }: ChatHistoryProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isProcessing]);

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-center opacity-40">
          <div className="text-4xl mb-3">🧠</div>
          <p className="text-white/60 text-base font-medium">En attente du tuteur IA...</p>
          <p className="text-white/30 text-sm mt-1">La conversation va commencer dans un instant</p>
        </div>
      )}

      {messages.map((msg, index) => {
        const isAI = msg.speaker === 'ai';
        const isFirst = index === 0 || messages[index - 1].speaker !== msg.speaker;
        return (
          <div
            key={msg.id}
            className={`flex ${isAI ? 'justify-start' : 'justify-end'} ${isFirst ? 'mt-3' : 'mt-1'} animate-[fadeSlideIn_0.3s_ease-out]`}
          >
            {/* AI avatar mini */}
            {isAI && isFirst && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-500 flex items-center justify-center mr-2 mt-1 shrink-0 shadow-lg shadow-indigo-500/20">
                <span className="text-white text-xs font-bold">IA</span>
              </div>
            )}
            {isAI && !isFirst && <div className="w-8 mr-2 shrink-0" />}

            {/* Exam exercise card (special message type) */}
            {isAI && msg.examExercises && msg.examExercises.length > 0 ? (
              <div className="max-w-[90%]">
                <ExamExerciseCard exercises={msg.examExercises} />
                <div className="text-[10px] mt-1 text-white/20 ml-1">
                  {msg.timestamp.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ) : (
              <div
                className={`max-w-[80%] px-4 py-3 text-sm leading-relaxed ${
                  isAI
                    ? `bg-white/[0.07] backdrop-blur-sm border border-white/10 text-white/90 ${isFirst ? 'rounded-2xl rounded-tl-md' : 'rounded-2xl'}`
                    : `bg-gradient-to-br from-indigo-600 to-indigo-700 text-white shadow-lg shadow-indigo-600/20 ${isFirst ? 'rounded-2xl rounded-tr-md' : 'rounded-2xl'}`
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.text}</div>
                <div
                  className={`text-[10px] mt-1.5 ${isAI ? 'text-white/25' : 'text-indigo-300/50'}`}
                >
                  {msg.timestamp.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            )}

            {/* Student avatar mini */}
            {!isAI && isFirst && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center ml-2 mt-1 shrink-0 shadow-lg shadow-emerald-500/20">
                <span className="text-white text-xs font-bold">Moi</span>
              </div>
            )}
            {!isAI && !isFirst && <div className="w-8 ml-2 shrink-0" />}
          </div>
        );
      })}

      {/* AI typing indicator */}
      {isProcessing && (
        <div className="flex justify-start mt-3 animate-[fadeSlideIn_0.3s_ease-out]">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-500 flex items-center justify-center mr-2 mt-1 shrink-0">
            <span className="text-white text-xs font-bold">IA</span>
          </div>
          <div className="bg-white/[0.07] backdrop-blur-sm border border-white/10 rounded-2xl rounded-tl-md px-5 py-3">
            <div className="flex gap-1.5 items-center">
              <div className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
