import { useState, useRef, useEffect } from 'react';
import { wsService } from '../../services/websocket';
import { speechService } from '../../services/speechService';
import { useSessionStore } from '../../stores/sessionStore';

interface VoiceInputProps {
  onTextSend: (text: string) => void;
  disabled?: boolean;
  /**
   * Texte à injecter dans le champ de saisie (depuis un raccourci externe).
   * Chaque changement de cette prop (même valeur identique) est détecté via
   * `injectKey`. Ajoute le texte à la fin de l'input existant et focus.
   */
  injectedText?: string;
  injectKey?: number;
}

/**
 * Pick the best MediaRecorder MIME type supported by the current browser.
 * Chrome/Edge: audio/webm;codecs=opus. Firefox: audio/ogg;codecs=opus.
 * Safari 14.1+: audio/mp4. Fallback: let the browser pick.
 */
function pickMimeType(): string {
  if (typeof MediaRecorder === 'undefined') return '';
  const candidates = [
    'audio/webm;codecs=opus',
    'audio/webm',
    'audio/ogg;codecs=opus',
    'audio/ogg',
    'audio/mp4',
  ];
  for (const type of candidates) {
    if (MediaRecorder.isTypeSupported(type)) return type;
  }
  return '';
}

export default function VoiceInput({ onTextSend, disabled = false, injectedText, injectKey }: VoiceInputProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [textInput, setTextInput] = useState('');
  const [inputMode, setInputMode] = useState<'voice' | 'text'>('voice');
  const [micError, setMicError] = useState<string | null>(null);
  const [micHint, setMicHint] = useState<string | null>('Clique pour parler');

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const textFieldRef = useRef<HTMLInputElement>(null);

  // Browser-native STT (Web Speech API) — primary path on Chrome/Edge/Safari/iOS
  const language = useSessionStore((s) => s.language);
  const browserSttActiveRef = useRef(false);
  const browserSttDidFinalRef = useRef(false);

  // Live volume meter (0..100). Lets the user see their mic actually works.
  const [volume, setVolume] = useState(0);
  const peakVolumeRef = useRef(0); // highest level seen during a session
  const audioCtxRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    return () => {
      // Cleanup on unmount
      try { mediaRecorderRef.current?.stop(); } catch {}
      streamRef.current?.getTracks().forEach((t) => t.stop());
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      try { audioCtxRef.current?.close(); } catch {}
    };
  }, []);

  const stopMeter = () => {
    if (rafRef.current) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }
    try { audioCtxRef.current?.close(); } catch {}
    audioCtxRef.current = null;
    analyserRef.current = null;
    setVolume(0);
  };

  const startMeter = (stream: MediaStream) => {
    try {
      const AC = (window as any).AudioContext || (window as any).webkitAudioContext;
      if (!AC) return;
      const ctx: AudioContext = new AC();
      const source = ctx.createMediaStreamSource(stream);
      const analyser = ctx.createAnalyser();
      analyser.fftSize = 512;
      source.connect(analyser);
      audioCtxRef.current = ctx;
      analyserRef.current = analyser;
      peakVolumeRef.current = 0;
      const data = new Uint8Array(analyser.frequencyBinCount);
      const tick = () => {
        if (!analyserRef.current) return;
        analyserRef.current.getByteTimeDomainData(data);
        // RMS around the 128 center (silence = 128)
        let sum = 0;
        for (let i = 0; i < data.length; i++) {
          const v = (data[i] - 128) / 128;
          sum += v * v;
        }
        const rms = Math.sqrt(sum / data.length);
        const pct = Math.min(100, Math.round(rms * 300));
        if (pct > peakVolumeRef.current) peakVolumeRef.current = pct;
        setVolume(pct);
        rafRef.current = requestAnimationFrame(tick);
      };
      rafRef.current = requestAnimationFrame(tick);
    } catch (err) {
      console.warn('[Voice] Meter init failed:', err);
    }
  };

  // Inject text from external source (quick-action chips)
  useEffect(() => {
    if (!injectedText) return;
    setInputMode('text');
    setTextInput((prev) => (prev ? prev.trimEnd() + ' ' + injectedText : injectedText));
    // Focus field once it appears in the DOM
    setTimeout(() => {
      const el = textFieldRef.current;
      if (el) {
        el.focus();
        el.selectionStart = el.selectionEnd = el.value.length;
      }
    }, 50);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [injectKey]);

  // ── Browser-native STT path (Web Speech API) ────────────────────
  // Used as primary path on Chrome/Edge/Safari/iOS. Sends transcribed text
  // directly through `onTextSend` (same pipeline as the text input — the
  // backend then runs the LLM and TTS as usual). No audio upload required.
  const startBrowserSTT = (): boolean => {
    if (!speechService.isRecognitionSupported()) return false;
    if (!wsService.isConnected) {
      setMicError('Pas de connexion au serveur. Recharge la page.');
      return true; // we handled the click; just couldn't start
    }

    setMicError(null);
    browserSttActiveRef.current = true;
    browserSttDidFinalRef.current = false;
    setIsRecording(true);
    setMicHint("Je t'écoute… parle maintenant");

    speechService.listen({
      lang: language,
      continuous: false,
      interimResults: true,
      onResult: (text, isFinal) => {
        const trimmed = (text || '').trim();
        if (isFinal) {
          browserSttDidFinalRef.current = true;
          if (trimmed) onTextSend(trimmed);
        } else if (trimmed) {
          setMicHint(`📝 ${trimmed}`);
        }
      },
      onEnd: () => {
        browserSttActiveRef.current = false;
        setIsRecording(false);
        if (!browserSttDidFinalRef.current) {
          setMicHint('Aucune voix détectée. Parle plus fort ou vérifie ton micro.');
          setTimeout(() => setMicHint('Clique pour parler'), 3000);
        } else {
          setMicHint('Clique pour parler');
        }
      },
      onError: (error) => {
        browserSttActiveRef.current = false;
        setIsRecording(false);
        if (error === 'no-speech') {
          setMicHint('Aucune voix détectée. Parle plus fort ou rapproche-toi du micro.');
          setTimeout(() => setMicHint('Clique pour parler'), 3000);
        } else if (error === 'not-allowed') {
          setMicError("Accès micro refusé. Autorise-le dans les paramètres du navigateur.");
        } else if (error === 'network') {
          setMicError("Erreur réseau pendant la reconnaissance vocale. Réessaie.");
        } else if (error !== 'aborted') {
          setMicError(`Erreur reconnaissance vocale: ${error}`);
        }
      },
    }).catch(() => { /* errors already handled via onError */ });

    return true;
  };

  const startRecording = async () => {
    setMicError(null);

    // 1) Try browser-native STT (instant, no upload, supports fr-FR + ar-MA)
    if (startBrowserSTT()) return;

    // 2) Fallback: MediaRecorder → backend STT (Firefox, older browsers)
    if (typeof window === 'undefined' || !navigator.mediaDevices?.getUserMedia) {
      setMicError('Micro non supporté par ce navigateur. Utilise Chrome ou Edge.');
      return;
    }

    if (!wsService.isConnected) {
      setMicError('Pas de connexion au serveur. Recharge la page.');
      return;
    }

    let stream: MediaStream;
    try {
      // IMPORTANT: keep noiseSuppression OFF by default. On many consumer
      // laptops (low-gain internal mics) the Chrome/Windows noise-suppression
      // filter is so aggressive that it cuts the entire voice signal to
      // silence. We'd rather have a bit of background hiss than an empty
      // audio blob. echoCancellation stays on because it rarely causes this
      // issue and helps when the speaker plays back the AI voice.
      stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: false,
          autoGainControl: true,   // boosts low-volume mics automatically
          sampleRate: 48000,
        },
      });
    } catch (err: any) {
      console.error('[Voice] getUserMedia failed:', err);
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        setMicError("Accès micro refusé. Autorise-le dans les paramètres du navigateur.");
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        setMicError("Aucun micro détecté. Branche un micro et réessaye.");
      } else {
        setMicError(`Impossible d'accéder au micro: ${err.message || err.name || 'inconnu'}`);
      }
      return;
    }

    const mimeType = pickMimeType();
    console.log(`[Voice] Starting MediaRecorder mime=${mimeType || '(default)'}`);

    let recorder: MediaRecorder;
    try {
      recorder = mimeType
        ? new MediaRecorder(stream, { mimeType, audioBitsPerSecond: 64000 })
        : new MediaRecorder(stream);
    } catch (err: any) {
      console.error('[Voice] MediaRecorder construction failed:', err);
      stream.getTracks().forEach((t) => t.stop());
      setMicError('Impossible d\'initialiser l\'enregistreur audio.');
      return;
    }

    chunksRef.current = [];
    recorder.ondataavailable = (evt) => {
      if (evt.data && evt.data.size > 0) chunksRef.current.push(evt.data);
    };
    recorder.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: mimeType || 'audio/webm' });
      const peak = peakVolumeRef.current;
      console.log(`[Voice] Recording stopped. Size=${blob.size} bytes, type=${blob.type}, peakVolume=${peak}`);

      // Release mic + meter
      stopMeter();
      stream.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
      mediaRecorderRef.current = null;

      if (blob.size < 5000) {
        // < 5 KB ≈ < 0.6 s of audio at 64 kbps → too short for a real sentence
        setMicHint('Enregistrement trop court. Parle pendant 1-2 secondes.');
        setTimeout(() => setMicHint('Clique pour parler'), 3000);
        setIsUploading(false);
        return;
      }

      if (peak < 8) {
        // Almost no sound detected — mic muted, too far, or wrong device
        setMicError(
          'Aucun son détecté. Vérifie que ton micro est activé et parle plus fort (ou rapproche-toi).'
        );
        setIsUploading(false);
        setTimeout(() => setMicError(null), 5000);
        return;
      }

      if (!wsService.isConnected) {
        setMicError('Connexion perdue pendant l\'enregistrement.');
        setIsUploading(false);
        return;
      }

      setIsUploading(true);
      setMicHint('Transcription en cours…');
      wsService.sendAudio(blob);
      // Backend will respond with a `transcription` message (handled elsewhere)
      // then process through LLM. We reset UI state after a safety timeout.
      setTimeout(() => {
        setIsUploading(false);
        setMicHint('Clique pour parler');
      }, 15000);
    };
    recorder.onerror = (evt: any) => {
      console.error('[Voice] MediaRecorder error:', evt.error || evt);
      setMicError('Erreur d\'enregistrement audio.');
      setIsRecording(false);
      setIsUploading(false);
      stopMeter();
      stream.getTracks().forEach((t) => t.stop());
    };

    streamRef.current = stream;
    mediaRecorderRef.current = recorder;

    // Fire up the live volume meter so the user can SEE their mic picks up voice
    startMeter(stream);

    try {
      recorder.start(); // single blob on stop
      setIsRecording(true);
      setMicHint('Je t\'écoute… clique à nouveau pour envoyer');
    } catch (err: any) {
      console.error('[Voice] recorder.start() failed:', err);
      stopMeter();
      stream.getTracks().forEach((t) => t.stop());
      setMicError('Impossible de démarrer l\'enregistrement.');
    }
  };

  const stopRecording = () => {
    // Browser-native STT path: ask SpeechRecognition to finalize
    if (browserSttActiveRef.current) {
      try { speechService.stopListening(); } catch { /* noop */ }
      browserSttActiveRef.current = false;
      setIsRecording(false);
      return;
    }
    // MediaRecorder fallback path
    const rec = mediaRecorderRef.current;
    if (rec && rec.state !== 'inactive') {
      try { rec.stop(); } catch (err) { console.warn('[Voice] stop() failed:', err); }
    }
    setIsRecording(false);
  };

  // Listen for transcription result to reset UI
  useEffect(() => {
    const onTranscription = (_data: any) => {
      setIsUploading(false);
      setMicHint('Clique pour parler');
    };
    const onStt = (data: any) => {
      if (data?.stage === 'stt') setMicHint('Transcription en cours…');
    };
    wsService.on('transcription', onTranscription);
    wsService.on('processing', onStt);
    return () => {
      wsService.off('transcription', onTranscription);
      wsService.off('processing', onStt);
    };
  }, []);

  const handleTextSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!textInput.trim() || disabled) return;
    onTextSend(textInput);
    setTextInput('');
  };

  return (
    <div className="shrink-0 border-t border-white/5 bg-[#0c0c1d]/90 backdrop-blur-xl">
      <div className="max-w-3xl mx-auto px-4 py-2.5 sm:py-4">

        {/* Mic error */}
        {micError && (
          <div className="mb-2 sm:mb-3 text-center text-xs text-red-400 bg-red-500/10 rounded-lg px-3 py-2 border border-red-500/20">
            {micError}
          </div>
        )}

        {/* Hint banner: skip the default 'Clique pour parler' (already shown next to mic) to save vertical space on small screens */}
        {micHint && !micError && micHint !== 'Clique pour parler' && (
          <div className="mb-2 sm:mb-3 text-center text-xs text-cyan-300/70 bg-cyan-500/5 rounded-lg px-3 py-2 border border-cyan-500/10">
            {micHint}
          </div>
        )}

        {/* Text input area (collapsible) */}
        {inputMode === 'text' ? (
          <form onSubmit={handleTextSubmit} className="flex gap-2 mb-2 sm:mb-3">
            <input
              ref={textFieldRef}
              type="text"
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Écris ta réponse..."
              className="flex-1 px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/30 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/30 outline-none text-sm transition-all"
              disabled={disabled}
              autoFocus
            />
            <button
              type="submit"
              disabled={disabled || !textInput.trim()}
              className="px-5 py-3 bg-indigo-600 text-white rounded-xl font-medium hover:bg-indigo-500 transition-all disabled:opacity-30 disabled:hover:bg-indigo-600 text-sm"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            </button>
          </form>
        ) : null}

        {/* Controls row */}
        <div className="flex items-center justify-center gap-4">
          {/* Text toggle */}
          <button
            onClick={() => setInputMode(inputMode === 'voice' ? 'text' : 'voice')}
            className={`w-11 h-11 rounded-full flex items-center justify-center transition-all ${
              inputMode === 'text'
                ? 'bg-indigo-600/30 text-indigo-400 border border-indigo-500/30'
                : 'bg-white/5 text-white/40 hover:text-white/70 hover:bg-white/10 border border-white/10'
            }`}
            title="Écrire un message"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className={`h-5 w-5 ${disabled ? 'text-white/30' : 'text-white'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
            </svg>
          </button>

          {/* Microphone button - MAIN */}
          <div className="relative">
            {/* Live volume-driven ring when recording — gives the user
                immediate visual feedback that the mic is picking up their voice. */}
            {isRecording && (
              <>
                <div
                  className="absolute rounded-full border-2 border-red-400 transition-all duration-75 ease-out pointer-events-none"
                  style={{
                    inset: `-${6 + volume * 0.35}px`,
                    opacity: 0.25 + volume / 180,
                    borderColor: volume < 8 ? 'rgba(239,68,68,0.4)' : 'rgba(34,211,238,0.75)',
                  }}
                />
                <div className="absolute inset-[-3px] rounded-full border border-red-400/30 animate-pulse" />
              </>
            )}
            <button
              onClick={isRecording ? stopRecording : startRecording}
              disabled={disabled || isUploading}
              className={`relative z-10 w-16 h-16 rounded-full flex items-center justify-center transition-all duration-300 shadow-lg ${
                isRecording
                  ? 'bg-red-500 shadow-red-500/40 scale-110'
                  : disabled
                    ? 'bg-white/10 cursor-not-allowed shadow-none'
                    : 'bg-gradient-to-br from-indigo-500 to-cyan-500 hover:from-indigo-400 hover:to-cyan-400 shadow-indigo-500/30 hover:scale-105 hover:shadow-indigo-500/50 active:scale-95'
              }`}
            >
              {isRecording ? (
                <div className="w-5 h-5 rounded-sm bg-white" />
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className={`h-7 w-7 ${disabled ? 'text-white/30' : 'text-white'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
              )}
            </button>
          </div>

          {/* Recording / upload state */}
          <div className="min-w-[7rem] text-center">
            {isRecording ? (
              <div className="flex items-center gap-1.5 justify-center">
                <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                <span className="text-red-400 text-sm font-mono">Enregistrement…</span>
              </div>
            ) : isUploading ? (
              <div className="flex items-center gap-1.5 justify-center">
                <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
                <span className="text-cyan-300 text-xs">Transcription…</span>
              </div>
            ) : (
              <span className="text-white/20 text-xs">
                {disabled ? '' : 'Clique pour parler'}
              </span>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
