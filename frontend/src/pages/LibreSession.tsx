import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { wsService } from '../services/websocket';
import { startLibreSession } from '../services/api';
import { Send, ArrowLeft, Loader2, MessageCircle, Sparkles } from 'lucide-react';
import QuickActions from '../components/session/QuickActions';
import type { QuickAction } from '../components/session/QuickActions';

/* ------------------------------------------------------------------ */
/*  Raccourcis Mode Libre                                               */
/* ------------------------------------------------------------------ */
const LIBRE_QUICK_ACTIONS: QuickAction[] = [
  {
    id: 'cours',
    icon: '📚',
    label: 'Cours',
    prompt: 'Fais-moi un cours complet sur ',
    mode: 'inject',
    tooltip: 'Demander un cours détaillé (complète le sujet)',
  },
  {
    id: 'exercice',
    icon: '📝',
    label: 'Exercice BAC',
    prompt: 'Donne-moi un exercice de type BAC marocain sur le sujet en cours, avec correction détaillée.',
    mode: 'send',
    tooltip: 'Demander un exercice BAC avec correction',
  },
  {
    id: 'corriger',
    icon: '✏️',
    label: 'Corriger',
    prompt: 'Corrige ma réponse et explique-moi mes erreurs :\n',
    mode: 'inject',
    tooltip: 'Faire corriger ta réponse (colle-la après)',
  },
  {
    id: 'resume',
    icon: '🎯',
    label: 'Résumé',
    prompt: "Fais-moi un résumé en 3 points clés de ce qu'on vient de voir.",
    mode: 'send',
    tooltip: "Résumer la conversation en 3 points",
  },
  {
    id: 'simple',
    icon: '🧠',
    label: 'Plus simple',
    prompt: 'Réexplique-moi ça plus simplement, comme à un débutant, avec un exemple concret.',
    mode: 'send',
    tooltip: 'Réexpliquer plus simplement',
  },
  {
    id: 'detail',
    icon: '➕',
    label: 'Plus détaillé',
    prompt: 'Développe ta dernière réponse avec plus de détails, un exemple et une démonstration.',
    mode: 'send',
    tooltip: 'Demander plus de détails',
  },
  {
    id: 'schema',
    icon: '📊',
    label: 'Schéma',
    prompt: 'Fais-moi un schéma explicatif au tableau pour illustrer cette notion.',
    mode: 'send',
    tooltip: 'Demander un schéma au tableau',
  },
];

interface Message {
  id: string;
  speaker: 'student' | 'ai';
  text: string;
  timestamp: Date;
}

export default function LibreSession() {
  const navigate = useNavigate();
  const { token, student } = useAuthStore();

  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentAiText, setCurrentAiText] = useState('');
  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const initCalledRef = useRef(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentAiText]);

  useEffect(() => {
    if (initCalledRef.current) return;
    initCalledRef.current = true;

    if (!token) {
      navigate('/login');
      return;
    }

    initLibreSession();

    return () => {
      wsService.disconnect();
    };
  }, []);

  const initLibreSession = async () => {
    try {
      // Create libre conversation record
      await startLibreSession('Conversation libre');

      // Register WS handlers before connecting
      wsService.clearHandlers();

      wsService.on('connected', () => {
        setConnected(true);
        // Init session in libre mode (no chapter, no lesson)
        wsService.sendJson({
          type: 'init_session',
          mode: 'libre',
          subject: 'Général',
          chapter_title: '',
          lesson_title: 'Mode Libre',
          objective: "Répondre aux questions de l'étudiant sur toutes les matières du BAC marocain",
          scenario: '',
          student_name: student?.full_name || 'Étudiant',
          proficiency: 'intermédiaire',
          language: 'fr',
          teaching_mode: 'Socratique',
        });
      });

      wsService.on('session_initialized', () => {
        setIsProcessing(false);
      });

      wsService.on('ai_response_chunk', (data: any) => {
        setIsProcessing(false);
        setCurrentAiText((prev) => prev + (data.token || ''));
      });

      wsService.on('ai_response_done', () => {
        setCurrentAiText((prev) => {
          if (prev) {
            const msgId = crypto.randomUUID();
            setMessages((msgs) => [
              ...msgs,
              { id: msgId, speaker: 'ai', text: prev, timestamp: new Date() }
            ]);
          }
          return '';
        });
        setIsProcessing(false);
      });

      wsService.on('processing', () => {
        setIsProcessing(true);
      });

      wsService.on('error', (data: any) => {
        setError(data.message || 'Une erreur est survenue');
        setIsProcessing(false);
      });

      wsService.on('disconnected', () => {
        setConnected(false);
      });

      // Auth token expired (Supabase JWT) — backend closed with code 4001
      wsService.on('auth_expired', () => {
        setError('Votre session a expiré. Veuillez vous reconnecter.');
        setTimeout(() => {
          useAuthStore.getState().logout();
          navigate('/login');
        }, 1500);
      });

      // Connect WebSocket
      await wsService.connect(token!);

    } catch (e: any) {
      setError('Erreur de connexion. Réessayez.');
    }
  };

  /** Core send — used both by the form submit and by quick-action chips. */
  const sendText = (rawText: string) => {
    if (isProcessing || !connected) return;
    const text = rawText.trim();
    if (!text) return;

    const msgId = crypto.randomUUID();
    setMessages((prev) => [
      ...prev,
      { id: msgId, speaker: 'student', text, timestamp: new Date() }
    ]);

    setIsProcessing(true);
    wsService.sendJson({ type: 'text_input', text });
  };

  const sendMessage = () => {
    if (!input.trim()) return;
    sendText(input);
    setInput('');
  };

  /** Quick-action: inject text into the textarea and focus it. */
  const handleQuickInject = (text: string) => {
    setInput((prev) => (prev ? prev + ' ' + text : text));
    // Focus on next tick once the state has rendered
    setTimeout(() => {
      const el = inputRef.current;
      if (el) {
        el.focus();
        el.selectionStart = el.selectionEnd = el.value.length;
      }
    }, 0);
  };

  /** Quick-action: send the prompt directly. */
  const handleQuickSend = (text: string) => {
    sendText(text);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const suggestedQuestions = [
    "C'est quoi la glycolyse ?",
    "Explique-moi les lois de Newton",
    "Comment calculer une dérivée ?",
    "Quelle est la différence entre acide et base ?",
  ];

  return (
    <div className="min-h-screen bg-[#070718] text-white flex flex-col relative overflow-hidden">
      {/* Decorative orbs */}
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute top-0 left-1/3 w-[600px] h-[600px] rounded-full bg-indigo-600/15 blur-[140px] anim-pulse-glow" />
        <div className="absolute bottom-0 right-[10%] w-[500px] h-[500px] rounded-full bg-cyan-500/10 blur-[140px] anim-pulse-glow" style={{ animationDelay: '2s' }} />
      </div>
      {/* Header */}
      <header className="relative z-20 backdrop-blur-2xl bg-[#070718]/70 border-b border-white/5 sticky top-0">
        <div className="max-w-4xl mx-auto px-3 sm:px-4 py-2.5 sm:py-3 flex items-center justify-between gap-2">
          <div className="flex items-center gap-3">
            <button onClick={() => navigate('/dashboard')} className="text-gray-500 hover:text-gray-700">
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-full flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-gray-800">Mode Libre</h1>
                <p className="text-xs text-gray-500">Pose n'importe quelle question</p>
              </div>
            </div>
          </div>
          <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
        </div>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-3 sm:px-4 py-4 sm:py-6 space-y-3 sm:space-y-4">
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
              {error}
            </div>
          )}

          {/* Welcome + Suggestions when empty */}
          {messages.length === 0 && !currentAiText && !isProcessing && (
            <div className="text-center py-12">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-3xl mb-6">
                <MessageCircle className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Pose-moi une question !</h2>
              <p className="text-gray-500 mb-8 max-w-md mx-auto">
                Je suis ton tuteur IA. Je peux t'aider en Math, Physique, Chimie et SVT.
                Je choisirai le meilleur format pour te répondre.
              </p>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-lg mx-auto">
                {suggestedQuestions.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => {
                      setInput(q);
                    }}
                    className="text-left p-3 bg-white rounded-xl border hover:border-blue-300 hover:shadow-md transition-all text-sm text-gray-700"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Message list */}
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.speaker === 'student' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[88%] sm:max-w-[80%] rounded-2xl px-3.5 sm:px-5 py-2.5 sm:py-3 ${
                msg.speaker === 'student'
                  ? 'bg-blue-600 text-white rounded-br-md'
                  : 'bg-white border text-gray-800 rounded-bl-md shadow-sm'
              }`}>
                <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.text}</p>
                <p className={`text-xs mt-1 ${
                  msg.speaker === 'student' ? 'text-blue-200' : 'text-gray-400'
                }`}>
                  {msg.timestamp.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </div>
          ))}

          {/* Streaming AI response */}
          {currentAiText && (
            <div className="flex justify-start">
              <div className="max-w-[88%] sm:max-w-[80%] bg-white border rounded-2xl rounded-bl-md px-3.5 sm:px-5 py-2.5 sm:py-3 shadow-sm">
                <p className="whitespace-pre-wrap text-sm leading-relaxed text-gray-800">{currentAiText}</p>
              </div>
            </div>
          )}

          {/* Processing indicator */}
          {isProcessing && !currentAiText && (
            <div className="flex justify-start">
              <div className="bg-white border rounded-2xl rounded-bl-md px-5 py-3 shadow-sm">
                <div className="flex items-center gap-2 text-gray-500">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span className="text-sm">En train de réfléchir...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input + raccourcis */}
      <div className="bg-white sticky bottom-0 border-t">
        {/* Barre de raccourcis */}
        <QuickActions
          actions={LIBRE_QUICK_ACTIONS}
          onInject={handleQuickInject}
          onSend={handleQuickSend}
          disabled={!connected || isProcessing}
          theme="light"
          title="Raccourcis"
        />

        <div className="max-w-4xl mx-auto px-3 sm:px-4 py-2.5 sm:py-3">
          <div className="flex items-end gap-2 sm:gap-3">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Pose ta question ici..."
              rows={1}
              className="flex-1 resize-none rounded-xl border border-gray-300 px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm"
              style={{ maxHeight: '120px' }}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isProcessing || !connected}
              className="p-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
