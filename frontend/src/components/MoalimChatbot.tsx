import { useEffect, useRef, useState } from 'react';
import { Send, X, Sparkles, Loader2, Bot } from 'lucide-react';

/**
 * Moalim — Orientation Chatbot
 * ────────────────────────────────────────────────────────────────
 * Floating chatbot powered by DeepSeek via /api/v1/concours/chat (SSE).
 * Specialized in post-Bac orientation in Morocco with live catalog context.
 */

type Msg = { role: 'user' | 'assistant'; content: string };

const STARTER_QUESTIONS = [
  'Quels concours pour un Bac SM ?',
  'Comment m\'inscrire sur cursussup ?',
  'Médecine vs Ingénierie : que choisir ?',
  'Quand sont les inscriptions 2025 ?',
];

const STORAGE_KEY = 'moalim_chat_history';

export default function MoalimChatbot() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Msg[]>(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch {}
    return [];
  });
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);

  // Persist history
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages.slice(-30)));
    } catch {}
  }, [messages]);

  // Auto-scroll
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, open]);

  const send = async (text?: string) => {
    const content = (text ?? input).trim();
    if (!content || streaming) return;
    setInput('');
    const next: Msg[] = [...messages, { role: 'user', content }, { role: 'assistant', content: '' }];
    setMessages(next);
    setStreaming(true);

    const controller = new AbortController();
    abortRef.current = controller;

    try {
      const res = await fetch('/api/v1/concours/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: next.slice(0, -1).map((m) => ({ role: m.role, content: m.content })),
        }),
        signal: controller.signal,
      });
      if (!res.ok || !res.body) throw new Error(`HTTP ${res.status}`);

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        // Parse SSE frames
        const frames = buffer.split('\n\n');
        buffer = frames.pop() ?? '';
        for (const frame of frames) {
          const line = frame.trim();
          if (!line.startsWith('data: ')) continue;
          const payload = line.slice(6);
          if (payload === '[DONE]') continue;
          try {
            const parsed = JSON.parse(payload);
            if (parsed.error) {
              setMessages((prev) => {
                const copy = [...prev];
                copy[copy.length - 1] = { role: 'assistant', content: `⚠️ ${parsed.error}` };
                return copy;
              });
              continue;
            }
            if (parsed.content) {
              setMessages((prev) => {
                const copy = [...prev];
                const last = copy[copy.length - 1];
                copy[copy.length - 1] = { role: 'assistant', content: (last.content || '') + parsed.content };
                return copy;
              });
            }
          } catch {}
        }
      }
    } catch (e: any) {
      if (e.name !== 'AbortError') {
        setMessages((prev) => {
          const copy = [...prev];
          copy[copy.length - 1] = {
            role: 'assistant',
            content: '⚠️ Désolé, une erreur est survenue. Réessaie dans quelques instants.',
          };
          return copy;
        });
      }
    } finally {
      setStreaming(false);
      abortRef.current = null;
    }
  };

  const clearHistory = () => {
    setMessages([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  return (
    <>
      {/* Floating launcher */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="fixed bottom-5 left-5 z-40 group"
          aria-label="Ouvrir Moalim"
        >
          <MoalimAvatar size={60} online pulse />
          <div className="absolute -top-10 left-0 bg-gray-900 text-white text-xs px-3 py-1.5 rounded-lg shadow-lg whitespace-nowrap opacity-0 group-hover:opacity-100 transition pointer-events-none">
            Parle à Moalim 🎓
          </div>
          <div className="absolute -top-2 -right-2 bg-pink-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full shadow animate-pulse">
            AI
          </div>
        </button>
      )}

      {/* Chat panel */}
      {open && (
        <div className="fixed bottom-0 left-0 sm:bottom-5 sm:left-5 z-50 w-full sm:w-[400px] h-[100dvh] sm:h-[600px] sm:max-h-[85vh] bg-white sm:rounded-3xl shadow-2xl flex flex-col overflow-hidden border border-gray-200">
          {/* Header */}
          <div className="bg-gradient-to-br from-indigo-700 via-purple-700 to-pink-700 text-white px-4 py-3 flex items-center gap-3">
            <MoalimAvatar size={42} online />
            <div className="flex-1 min-w-0">
              <div className="font-bold text-sm flex items-center gap-1.5">
                Moalim
                <span className="text-[10px] bg-white/20 px-1.5 py-0.5 rounded-full">IA</span>
              </div>
              <div className="text-[11px] text-white/80">Conseiller orientation · en ligne</div>
            </div>
            {messages.length > 0 && (
              <button
                onClick={clearHistory}
                className="text-[11px] text-white/70 hover:text-white underline"
                title="Effacer la conversation"
              >
                Effacer
              </button>
            )}
            <button onClick={() => setOpen(false)} className="p-1.5 hover:bg-white/20 rounded-lg" aria-label="Fermer">
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
            {messages.length === 0 && (
              <div className="space-y-4">
                <div className="text-center py-6">
                  <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-pink-500 text-white mb-3 shadow-lg">
                    <Bot className="w-8 h-8" />
                  </div>
                  <h3 className="font-bold text-gray-900 text-base">Salut, je suis Moalim 🎓</h3>
                  <p className="text-sm text-gray-600 mt-1 max-w-xs mx-auto">
                    Ton conseiller d'orientation IA. Pose-moi n'importe quelle question sur les concours,
                    filières, écoles ou dates au Maroc.
                  </p>
                </div>
                <div className="space-y-2">
                  <div className="text-[11px] font-bold uppercase tracking-wider text-gray-500 px-1">
                    Essaie par :
                  </div>
                  {STARTER_QUESTIONS.map((q) => (
                    <button
                      key={q}
                      onClick={() => send(q)}
                      className="w-full text-left text-sm bg-white hover:bg-indigo-50 border border-gray-200 hover:border-indigo-300 rounded-xl px-3 py-2.5 transition flex items-center justify-between gap-2 group"
                    >
                      <span className="text-gray-700 group-hover:text-indigo-800">{q}</span>
                      <Sparkles className="w-3.5 h-3.5 text-indigo-400 group-hover:text-indigo-600 flex-shrink-0" />
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {m.role === 'assistant' && (
                  <div className="flex-shrink-0 mr-2">
                    <MoalimAvatar size={28} />
                  </div>
                )}
                <div
                  className={`max-w-[85%] text-sm px-3.5 py-2.5 rounded-2xl whitespace-pre-wrap leading-relaxed ${
                    m.role === 'user'
                      ? 'bg-gradient-to-br from-indigo-600 to-purple-600 text-white rounded-tr-sm'
                      : 'bg-white text-gray-800 border border-gray-200 rounded-tl-sm shadow-sm'
                  }`}
                >
                  {m.content || (streaming && i === messages.length - 1 ? (
                    <Loader2 className="w-4 h-4 animate-spin text-gray-400" />
                  ) : '')}
                </div>
              </div>
            ))}
            <div ref={endRef} />
          </div>

          {/* Composer */}
          <div className="border-t bg-white p-3 flex items-end gap-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  send();
                }
              }}
              placeholder={streaming ? 'Moalim réfléchit…' : 'Pose ta question…'}
              disabled={streaming}
              rows={1}
              className="flex-1 resize-none text-sm bg-gray-50 border border-gray-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent max-h-24 overflow-y-auto"
            />
            <button
              onClick={() => send()}
              disabled={streaming || !input.trim()}
              className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-indigo-600 to-pink-600 hover:from-indigo-700 hover:to-pink-700 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-xl flex items-center justify-center shadow-md transition"
              aria-label="Envoyer"
            >
              {streaming ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
            </button>
          </div>
        </div>
      )}
    </>
  );
}

/* ─── Sophisticated Robot Avatar ──────────────────────────────── */
function MoalimAvatar({
  size = 48,
  online = false,
  pulse = false,
}: {
  size?: number;
  online?: boolean;
  pulse?: boolean;
}) {
  const eyeColor = '#67e8f9'; // cyan-300
  return (
    <div className="relative inline-block" style={{ width: size, height: size }}>
      {pulse && (
        <span
          className="absolute inset-0 rounded-full bg-gradient-to-br from-indigo-500 to-pink-500 animate-ping opacity-30"
        />
      )}
      <svg
        width={size}
        height={size}
        viewBox="0 0 64 64"
        className="relative drop-shadow-lg"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* gradient defs */}
        <defs>
          <linearGradient id="moalimBg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#4f46e5" />
            <stop offset="50%" stopColor="#7c3aed" />
            <stop offset="100%" stopColor="#db2777" />
          </linearGradient>
          <linearGradient id="moalimFace" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#1e293b" />
            <stop offset="100%" stopColor="#0f172a" />
          </linearGradient>
          <radialGradient id="moalimEye" cx="0.5" cy="0.5" r="0.5">
            <stop offset="0%" stopColor="#ffffff" />
            <stop offset="30%" stopColor={eyeColor} />
            <stop offset="100%" stopColor="#0891b2" />
          </radialGradient>
        </defs>

        {/* Outer gradient disc */}
        <circle cx="32" cy="32" r="31" fill="url(#moalimBg)" />

        {/* Subtle glow */}
        <circle cx="32" cy="32" r="28" fill="none" stroke="#ffffff" strokeOpacity="0.15" strokeWidth="1" />

        {/* Antenna */}
        <line x1="32" y1="14" x2="32" y2="10" stroke="#fbbf24" strokeWidth="1.5" strokeLinecap="round" />
        <circle cx="32" cy="9" r="2" fill="#fbbf24">
          <animate attributeName="opacity" values="0.6;1;0.6" dur="1.8s" repeatCount="indefinite" />
        </circle>

        {/* Robot head */}
        <rect x="18" y="18" width="28" height="26" rx="8" fill="url(#moalimFace)" />

        {/* Screen / visor */}
        <rect x="22" y="24" width="20" height="11" rx="3" fill="#0f172a" stroke={eyeColor} strokeOpacity="0.4" strokeWidth="0.5" />

        {/* Eyes */}
        <circle cx="28" cy="29.5" r="2.4" fill="url(#moalimEye)">
          <animate attributeName="r" values="2.4;0.6;2.4" dur="4.5s" repeatCount="indefinite" keyTimes="0;0.05;0.1" />
        </circle>
        <circle cx="36" cy="29.5" r="2.4" fill="url(#moalimEye)">
          <animate attributeName="r" values="2.4;0.6;2.4" dur="4.5s" repeatCount="indefinite" keyTimes="0;0.05;0.1" />
        </circle>

        {/* Mouth — smile indicator */}
        <path d="M 27 39 Q 32 42 37 39" stroke={eyeColor} strokeWidth="1.3" fill="none" strokeLinecap="round" />

        {/* Side "ears" / audio modules */}
        <rect x="14" y="27" width="3" height="8" rx="1" fill="#1e293b" />
        <rect x="47" y="27" width="3" height="8" rx="1" fill="#1e293b" />
        <circle cx="15.5" cy="31" r="0.8" fill={eyeColor} />
        <circle cx="48.5" cy="31" r="0.8" fill={eyeColor} />

        {/* Chest detail */}
        <rect x="27" y="46" width="10" height="3" rx="1" fill="#0f172a" opacity="0.8" />
      </svg>

      {/* Online indicator */}
      {online && (
        <span
          className="absolute block rounded-full bg-emerald-400 ring-2 ring-white"
          style={{
            width: Math.max(10, size * 0.22),
            height: Math.max(10, size * 0.22),
            right: 1,
            bottom: 1,
          }}
        />
      )}
    </div>
  );
}
