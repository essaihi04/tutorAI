import { useCallback, useEffect, useRef, useState } from 'react';
import 'katex/dist/katex.min.css';
import { renderMixedContent, containsArabic } from './boardLines';
import { speechService } from '../../services/speechService';
import { boardVoice } from '../../services/boardVoice';
import { useSessionStore } from '../../stores/sessionStore';

/**
 * Le coin élève d'un tableau — poser une question sans quitter le tableau.
 *
 * Jusqu'ici, seul le mode « prof en direct » permettait de lever la main :
 * devant un cours structuré, un schéma ou un dessin, l'élève n'avait
 * d'autre recours que de rouvrir le panneau latéral — c'est-à-dire de
 * quitter des yeux la figure sur laquelle portait sa question.
 *
 * LiveBoard garde le sien : y lever la main MET LE COURS EN PAUSE, ce qui n'a
 * aucun sens pour un tableau qui ne se déroule pas dans le temps. Ici, le
 * champ est simplement toujours à portée.
 */
interface BoardStudentCornerProps {
  /** Même canal que le chat latéral : la question part dans la session. */
  onStudentMessage?: (text: string) => void;
  /** Dernière réponse texte du professeur, pour la bulle de réponse. */
  assistantReply?: string | null;
  /** Une requête est déjà en cours : le professeur réfléchit. */
  busy?: boolean;
  /** Le micro n'est proposé que si la voix est active dans la séance. */
  voiceEnabled?: boolean;
}

export default function BoardStudentCorner({
  onStudentMessage,
  assistantReply,
  busy = false,
  voiceEnabled = true,
}: BoardStudentCornerProps) {
  const language = useSessionStore(s => s.language);
  const [open, setOpen] = useState(false);
  const [text, setText] = useState('');
  const [listening, setListening] = useState(false);
  const [awaitingReply, setAwaitingReply] = useState(false);
  const fieldRef = useRef<HTMLInputElement>(null);
  // La réponse affichée doit être NOUVELLE : sans cette borne, la bulle
  // ressort la réponse du tour précédent à la seconde où l'élève ouvre le
  // champ, et il croit que le professeur a répondu avant qu'il ait parlé.
  const replyBaselineRef = useRef<string | null>(null);

  const stopListening = useCallback(() => {
    try { speechService.stopListening(); } catch { /* noop */ }
    setListening(false);
  }, []);

  const submit = useCallback((raw: string) => {
    const question = raw.trim();
    if (!question || !onStudentMessage) return;
    replyBaselineRef.current = typeof assistantReply === 'string' ? assistantReply : null;
    setAwaitingReply(true);
    setText('');
    onStudentMessage(question);
  }, [onStudentMessage, assistantReply]);

  const toggleVoice = useCallback(() => {
    if (listening) {
      stopListening();
      return;
    }
    if (!speechService.isRecognitionSupported()) return;
    // Couper la voix du professeur avant d'ouvrir le micro : sinon le tableau
    // se dicte à lui-même ce qu'il est en train de lire à voix haute.
    boardVoice.stop();
    setListening(true);
    speechService.listen({
      lang: language,
      continuous: false,
      interimResults: true,
      onResult: (heard: string, isFinal: boolean) => {
        const value = (heard || '').trim();
        if (isFinal) {
          if (value) submit(value);
        } else if (value) {
          setText(value);
        }
      },
      onEnd: () => setListening(false),
      onError: () => setListening(false),
    });
  }, [listening, language, stopListening, submit]);

  // Le micro ne doit pas survivre au tableau : un composant démonté qui
  // écoute encore capte la question destinée à l'écran suivant.
  useEffect(() => () => { try { speechService.stopListening(); } catch { /* noop */ } }, []);

  useEffect(() => {
    if (open) setTimeout(() => fieldRef.current?.focus(), 80);
  }, [open]);

  if (!onStudentMessage) return null;

  const reply =
    awaitingReply
    && typeof assistantReply === 'string'
    && assistantReply.trim()
    && assistantReply !== replyBaselineRef.current
      ? assistantReply
      : null;

  return (
    <div className="absolute bottom-0 left-0 right-0 z-40 flex flex-col items-center gap-2 px-3 pb-3 pointer-events-none">
      {open && reply && (
        <div
          className="pointer-events-auto w-full max-w-2xl max-h-44 overflow-y-auto rounded-xl px-4 py-3 text-[14px] leading-relaxed"
          style={{ background: 'rgba(13,27,21,0.95)', border: '1px solid rgba(52,211,153,0.3)', color: '#d1fae5' }}
          dir={containsArabic(reply) ? 'rtl' : 'ltr'}
        >
          <div className="text-[11px] mb-1" style={{ color: '#34d399' }}>👨‍🏫 Réponse du professeur</div>
          <div className="katex-dark" dangerouslySetInnerHTML={{ __html: renderMixedContent(reply) }} />
        </div>
      )}

      {open ? (
        <div
          className="pointer-events-auto w-full max-w-2xl rounded-2xl px-3 py-2.5"
          style={{ background: 'rgba(13,27,21,0.95)', border: '1px solid rgba(255,255,255,0.15)', backdropFilter: 'blur(8px)' }}
        >
          <div className="flex items-center gap-2">
            <input
              ref={fieldRef}
              value={text}
              onChange={event => setText(event.target.value)}
              onKeyDown={event => { if (event.key === 'Enter') submit(text); }}
              placeholder={listening ? '🎙️ Je t’écoute… parle maintenant' : 'Pose ta question au professeur…'}
              className="flex-1 min-w-0 bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-sm text-white placeholder-white/35 outline-none focus:border-emerald-400/50 transition-colors"
              disabled={busy}
            />
            {voiceEnabled && speechService.isRecognitionSupported() && (
              <button
                onClick={toggleVoice}
                disabled={busy}
                className={`shrink-0 w-9 h-9 rounded-full flex items-center justify-center text-sm transition-all ${
                  listening ? 'bg-red-500/80 animate-pulse' : 'bg-white/10 hover:bg-white/20'
                }`}
                title={listening ? 'Arrêter le micro' : 'Poser la question à la voix'}
              >
                🎙️
              </button>
            )}
            <button
              onClick={() => submit(text)}
              disabled={busy || !text.trim()}
              className="shrink-0 px-3 py-2 rounded-xl text-sm font-medium text-white disabled:opacity-40 transition-colors"
              style={{ background: 'rgba(16,185,129,0.35)', border: '1px solid rgba(52,211,153,0.5)' }}
              title="Envoyer la question"
            >
              {busy ? '…' : 'Envoyer'}
            </button>
            <button
              onClick={() => { stopListening(); setOpen(false); }}
              className="shrink-0 text-white/40 hover:text-white/80 text-lg px-1 transition-colors"
              title="Fermer"
            >
              ✕
            </button>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setOpen(true)}
          className="pointer-events-auto flex items-center gap-2 px-3.5 py-2 rounded-full text-sm text-white transition-all hover:scale-[1.03]"
          style={{ background: 'rgba(13,27,21,0.9)', border: '1px solid rgba(52,211,153,0.4)', backdropFilter: 'blur(8px)' }}
          title="Poser une question sans quitter le tableau"
        >
          <span>✋</span>
          <span>Poser une question</span>
        </button>
      )}
    </div>
  );
}
