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
