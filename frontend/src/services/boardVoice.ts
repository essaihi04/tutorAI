/**
 * Voix du tableau en direct — NOTRE modèle vocal, jamais celui du navigateur.
 *
 * La synthèse du navigateur (Web Speech API) ne sait pas dire la darija : elle
 * lit l'arabe avec une voix MSA robotique, ou échoue. Le tableau demande donc
 * chaque ligne à notre serveur (modèle Academy en tête) et joue le WAV reçu.
 *
 * Deux propriétés importantes pour le rendu « prof en direct » :
 *  • `speak()` expose la progression réelle de la lecture (0 → 1), ce qui
 *    permet d'écrire le texte exactement au rythme de la voix ;
 *  • `prefetch()` prépare la ligne suivante pendant que la courante est lue —
 *    sans quoi le tableau s'arrêterait entre chaque ligne, le temps que le GPU
 *    génère l'audio.
 */

export interface BoardSpeakHandle {
  /** Résolue à la fin de la lecture. `true` si la voix a réellement parlé. */
  done: Promise<boolean>;
  /** Interrompt la lecture immédiatement. */
  stop: () => void;
  /** Met en pause / reprend, en suivant l'état de lecture du tableau. */
  pause: () => void;
  resume: () => void;
}

type Lang = 'fr' | 'ar' | 'mixed';

const CACHE_MAX = 40;

class BoardVoiceService {
  /** Fragments déjà synthétisés (clé = langue + texte) → URL d'objet. */
  private cache = new Map<string, string>();
  /** Requêtes en vol, pour ne jamais demander deux fois le même fragment. */
  private inflight = new Map<string, Promise<string | null>>();
  private current: HTMLAudioElement | null = null;

  private key(text: string, lang: Lang) {
    return `${lang}|${text}`;
  }

  /** Récupère l'audio du serveur (ou du cache). `null` si indisponible. */
  private fetchAudio(text: string, lang: Lang): Promise<string | null> {
    const k = this.key(text, lang);
    const cached = this.cache.get(k);
    if (cached) return Promise.resolve(cached);

    const pending = this.inflight.get(k);
    if (pending) return pending;

    const req = (async (): Promise<string | null> => {
      try {
        const resp = await fetch('/api/v1/tts/speak', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text, language: lang }),
        });
        if (!resp.ok) {
          console.warn(`[BoardVoice] TTS indisponible (HTTP ${resp.status})`);
          return null;
        }
        const blob = await resp.blob();
        const url = URL.createObjectURL(blob);
        // Cache borné : on libère les plus anciens objets pour ne pas fuir.
        if (this.cache.size >= CACHE_MAX) {
          const oldest = this.cache.keys().next().value;
          if (oldest) {
            const old = this.cache.get(oldest);
            if (old) URL.revokeObjectURL(old);
            this.cache.delete(oldest);
          }
        }
        this.cache.set(k, url);
        return url;
      } catch (err) {
        console.warn('[BoardVoice] Échec de la requête TTS:', err);
        return null;
      } finally {
        this.inflight.delete(k);
      }
    })();

    this.inflight.set(k, req);
    return req;
  }

  /** Prépare un fragment à l'avance (sans le jouer). */
  prefetch(text: string, lang: Lang) {
    const clean = (text || '').trim();
    if (!clean) return;
    void this.fetchAudio(clean, lang);
  }

  /**
   * Dit un fragment avec notre voix.
   *
   * `onProgress` reçoit l'avancement réel de la lecture (0 → 1) : c'est lui
   * qui pilote l'écriture manuscrite, donc le texte se forme exactement au
   * rythme de la parole du professeur.
   */
  speak(
    text: string,
    lang: Lang,
    onProgress?: (ratio: number) => void,
  ): BoardSpeakHandle {
    const clean = (text || '').trim();
    let audio: HTMLAudioElement | null = null;
    let stopped = false;
    let wantPaused = false;

    const done = (async (): Promise<boolean> => {
      if (!clean) return false;
      const url = await this.fetchAudio(clean, lang);
      if (stopped || !url) return false;

      audio = new Audio(url);
      this.current = audio;

      return await new Promise<boolean>((resolve) => {
        const el = audio as HTMLAudioElement;
        let finished = false;
        const settle = (spoke: boolean) => {
          if (finished) return;
          finished = true;
          clearInterval(timer);
          if (this.current === el) this.current = null;
          onProgress?.(1);
          resolve(spoke);
        };

        // Progression réelle de la lecture, 20 fois par seconde.
        const timer = window.setInterval(() => {
          if (!el.duration || !isFinite(el.duration)) return;
          onProgress?.(Math.min(0.99, el.currentTime / el.duration));
        }, 50);

        el.onended = () => settle(true);
        el.onerror = () => settle(false);

        el.play()
          .then(() => {
            // Le tableau a pu demander la pause avant le début effectif.
            if (wantPaused) el.pause();
          })
          .catch((err) => {
            // Autoplay refusé (pas d'interaction utilisateur récente) :
            // le tableau retombera sur son écriture minutée.
            console.warn('[BoardVoice] Lecture refusée par le navigateur:', err);
            settle(false);
          });
      });
    })();

    return {
      done,
      stop: () => {
        stopped = true;
        if (audio) {
          try {
            audio.pause();
            audio.currentTime = 0;
          } catch { /* ignore */ }
          audio.onended?.(new Event('ended'));
        }
      },
      pause: () => {
        wantPaused = true;
        try { audio?.pause(); } catch { /* ignore */ }
      },
      resume: () => {
        wantPaused = false;
        try { void audio?.play(); } catch { /* ignore */ }
      },
    };
  }

  /** Coupe la voix en cours (changement de cours, fermeture du tableau…). */
  stop() {
    if (this.current) {
      try {
        this.current.pause();
        this.current.currentTime = 0;
      } catch { /* ignore */ }
      this.current = null;
    }
  }
}

export const boardVoice = new BoardVoiceService();
