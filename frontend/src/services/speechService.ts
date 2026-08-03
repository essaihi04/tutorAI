/**
 * Browser-native Speech Service
 * Uses Web Speech API for TTS (SpeechSynthesis) and STT (SpeechRecognition)
 * No API keys needed - works entirely in the browser
 */

import type { SessionLanguage } from '../stores/sessionStore';

// ─── TTS (Text-to-Speech) ───────────────────────────────────────────

interface SpeakOptions {
  lang?: SessionLanguage;
  rate?: number;
  pitch?: number;
  onStart?: () => void;
  onEnd?: () => void;
  onWord?: (charIndex: number) => void;
}

class TTSService {
  private synthesis: SpeechSynthesis;
  private voices: SpeechSynthesisVoice[] = [];

  constructor() {
    this.synthesis = window.speechSynthesis;
    this._loadVoices();
    if (this.synthesis.onvoiceschanged !== undefined) {
      this.synthesis.onvoiceschanged = () => this._loadVoices();
    }
  }

  private _loadVoices() {
    this.voices = this.synthesis.getVoices();
  }

  private _chunkText(text: string): string[] {
    const normalized = text.replace(/\s+/g, ' ').trim();
    if (!normalized) return [];

    const sentences = normalized.split(/(?<=[.!?؟])/).map((part) => part.trim()).filter(Boolean);
    const chunks: string[] = [];
    let current = '';

    for (const sentence of sentences) {
      const candidate = current ? `${current} ${sentence}` : sentence;
      if (candidate.length <= 220) {
        current = candidate;
      } else {
        if (current) {
          chunks.push(current);
        }
        if (sentence.length <= 220) {
          current = sentence;
        } else {
          for (let i = 0; i < sentence.length; i += 220) {
            chunks.push(sentence.slice(i, i + 220).trim());
          }
          current = '';
        }
      }
    }

    if (current) {
      chunks.push(current);
    }

    return chunks;
  }

  private _getVoice(lang: SessionLanguage): SpeechSynthesisVoice | null {
    const normalizedLang = lang === 'mixed' ? 'fr' : lang;
    const langCode = normalizedLang === 'fr' ? 'fr' : 'ar';

    const priorities = normalizedLang === 'fr'
      ? ['Google français', 'Microsoft Paul', 'Microsoft Julie', 'fr-FR', 'fr']
      : ['Google العربية', 'Microsoft', 'ar-SA', 'ar'];

    for (const prio of priorities) {
      const match = this.voices.find(v =>
        v.name.includes(prio) || v.lang.startsWith(prio)
      );
      if (match) return match;
    }

    return this.voices.find(v => v.lang.startsWith(langCode)) || null;
  }

  speak(text: string, options: SpeakOptions = {}): Promise<void> {
    return new Promise((resolve, reject) => {
      this.stop();

      const { lang = 'fr', rate = 1.0, pitch = 1.0, onStart, onEnd } = options;
      const normalizedLang = lang === 'mixed' ? 'fr' : lang;
      const chunks = this._chunkText(text);

      if (chunks.length === 0) {
        onEnd?.();
        resolve();
        return;
      }

      const voice = this._getVoice(lang);
      let started = false;
      let index = 0;

      const speakNext = () => {
        if (index >= chunks.length) {
          onEnd?.();
          resolve();
          return;
        }

        const utterance = new SpeechSynthesisUtterance(chunks[index]);

        if (voice) utterance.voice = voice;
        utterance.lang = normalizedLang === 'fr' ? 'fr-FR' : 'ar-SA';
        utterance.rate = rate;
        utterance.pitch = pitch;
        utterance.volume = 1;

        utterance.onstart = () => {
          if (!started) {
            started = true;
            onStart?.();
          }
        };
        utterance.onend = () => {
          index += 1;
          speakNext();
        };
        utterance.onerror = (e) => {
          onEnd?.();
          if (e.error === 'interrupted' || e.error === 'canceled') {
            resolve();
          } else {
            reject(e);
          }
        };

        this.synthesis.speak(utterance);
      };

      speakNext();
    });
  }

  /**
   * Speak a SHORT text while reporting how far the voice has got (0 → 1).
   *
   * Used by the live board to write at the exact pace of the speech: the
   * `boundary` event fires on each word, so the reveal follows the voice
   * instead of a guessed duration.
   *
   * Deliberately not chunked — callers pass one board line at a time, and
   * chunking would break the char offsets the progress relies on.
   *
   * Resolves when speech ends (or immediately if there is nothing to say).
   * Returns progress 1 at the end so callers can always settle the UI.
   *
   * Resolves `true` only if the voice ACTUALLY started speaking. Chrome can
   * fail an utterance instantly (`not-allowed` without recent user gesture,
   * or the notorious cancel()-then-speak() race) — in that case `onerror`
   * fires immediately and we resolve `false`, so the caller can fall back to
   * a timed animation instead of snapping its UI to the final state.
   */
  speakSynced(
    text: string,
    options: SpeakOptions & { onProgress?: (ratio: number) => void } = {},
  ): Promise<boolean> {
    const { lang = 'fr', rate = 1.0, pitch = 1.0, onStart, onEnd, onProgress } = options;
    const clean = (text || '').replace(/\s+/g, ' ').trim();

    return new Promise((resolve) => {
      if (!clean || typeof window === 'undefined' || !window.speechSynthesis) {
        onProgress?.(1);
        onEnd?.();
        resolve(false);
        return;
      }

      const normalizedLang = lang === 'mixed' ? 'fr' : lang;
      const utterance = new SpeechSynthesisUtterance(clean);
      const voice = this._getVoice(lang);
      if (voice) utterance.voice = voice;
      utterance.lang = normalizedLang === 'fr' ? 'fr-FR' : 'ar-SA';
      utterance.rate = rate;
      utterance.pitch = pitch;
      utterance.volume = 1;

      let settled = false;
      let started = false;
      let watchdog: number | undefined;
      const finish = () => {
        if (settled) return;
        settled = true;
        clearTimeout(watchdog);
        onProgress?.(1);
        onEnd?.();
        resolve(started);
      };
      // Garde-fou : si la synthèse reste coincée en file (Chrome, après un
      // cancel() malheureux) l'utterance ne démarre jamais et n'émet aucun
      // événement — sans ce timeout la promesse ne se résoudrait jamais et
      // le tableau resterait bloqué sur la ligne en cours.
      watchdog = window.setTimeout(() => {
        if (!started && !settled) {
          try { this.synthesis.cancel(); } catch { /* ignore */ }
          finish();
        }
      }, 2500);

      utterance.onstart = () => {
        started = true;
        onStart?.();
      };
      utterance.onboundary = (e: SpeechSynthesisEvent) => {
        const idx = typeof e.charIndex === 'number' ? e.charIndex : 0;
        onProgress?.(Math.max(0, Math.min(1, idx / clean.length)));
      };
      utterance.onend = finish;
      // 'interrupted'/'canceled' happen on every stop() — never treat as fatal.
      utterance.onerror = finish;

      // Chrome laisse parfois la synthèse coincée en "paused" après un
      // cancel() : sans resume(), speak() reste en file et rien ne démarre.
      try { this.synthesis.resume(); } catch { /* ignore */ }
      this.synthesis.speak(utterance);
    });
  }

  /** True when the browser can actually synthesise speech right now. */
  get supported(): boolean {
    return typeof window !== 'undefined' && 'speechSynthesis' in window;
  }

  /** Resolve once the voice list is populated (Chrome loads it async). */
  ensureVoices(timeoutMs = 1500): Promise<void> {
    return new Promise((resolve) => {
      if (this.voices.length > 0) return resolve();
      const done = () => resolve();
      const t = setTimeout(done, timeoutMs);
      const handler = () => {
        this._loadVoices();
        if (this.voices.length > 0) {
          clearTimeout(t);
          this.synthesis.removeEventListener?.('voiceschanged', handler);
          resolve();
        }
      };
      this.synthesis.addEventListener?.('voiceschanged', handler);
      this._loadVoices();
      if (this.voices.length > 0) {
        clearTimeout(t);
        resolve();
      }
    });
  }

  stop() {
    this.synthesis.cancel();
  }

  isSpeaking(): boolean {
    return this.synthesis.speaking;
  }
}

// ─── STT (Speech-to-Text) ───────────────────────────────────────────

interface ListenOptions {
  lang?: SessionLanguage;
  continuous?: boolean;
  interimResults?: boolean;
  onResult?: (text: string, isFinal: boolean) => void;
  onEnd?: () => void;
  onError?: (error: string) => void;
}

class STTService {
  private recognition: any = null;

  get supported(): boolean {
    return 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window;
  }

  start(options: ListenOptions = {}): boolean {
    if (!this.supported) {
      options.onError?.('Speech recognition not supported in this browser');
      return false;
    }

    this.stop();

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    this.recognition = new SpeechRecognition();

    const { lang = 'fr', continuous = false, interimResults = true, onResult, onEnd, onError } = options;

    // Darija is Arabic-based, use ar-MA for recognition
    this.recognition.lang = lang === 'fr' ? 'fr-FR' : 'ar-MA';
    this.recognition.continuous = continuous;
    this.recognition.interimResults = interimResults;

    this.recognition.onresult = (event: any) => {
      let finalTranscript = '';
      let interimTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }

      if (finalTranscript) {
        onResult?.(finalTranscript, true);
      } else if (interimTranscript) {
        onResult?.(interimTranscript, false);
      }
    };

    this.recognition.onend = () => {
      onEnd?.();
    };

    this.recognition.onerror = (event: any) => {
      if (event.error === 'no-speech') {
        onError?.('no-speech');
      } else if (event.error === 'not-allowed') {
        onError?.('not-allowed');
      } else {
        onError?.(`error: ${event.error}`);
      }
    };

    try {
      this.recognition.start();
      return true;
    } catch {
      return false;
    }
  }

  stop() {
    if (this.recognition) {
      try { this.recognition.stop(); } catch {}
      this.recognition = null;
    }
  }
}

// ─── Combined Service ────────────────────────────────────────────────

class CombinedSpeechService {
  private tts = new TTSService();
  private stt = new STTService();

  speak(text: string, options?: SpeakOptions) {
    return this.tts.speak(text, options);
  }

  /** Speak one short line while reporting progress — used to write in sync. */
  speakSynced(text: string, options?: SpeakOptions & { onProgress?: (ratio: number) => void }) {
    return this.tts.speakSynced(text, options);
  }

  get ttsSupported() {
    return this.tts.supported;
  }

  ensureVoices(timeoutMs?: number) {
    return this.tts.ensureVoices(timeoutMs);
  }

  stop() {
    this.tts.stop();
  }

  isSpeaking() {
    return this.tts.isSpeaking();
  }

  isRecognitionSupported() {
    return this.stt.supported;
  }

  listen(options: ListenOptions = {}) {
    return new Promise<void>((resolve, reject) => {
      const success = this.stt.start({
        ...options,
        onEnd: () => {
          options.onEnd?.();
          resolve();
        },
        onError: (error) => {
          options.onError?.(error);
          reject(error);
        },
      });
      if (!success) {
        reject('Failed to start speech recognition');
      }
    });
  }

  stopListening() {
    this.stt.stop();
  }
}

export const speechService = new CombinedSpeechService();
