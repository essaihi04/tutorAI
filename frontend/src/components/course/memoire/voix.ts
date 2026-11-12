import { observeAvatarMedia } from '../../../services/avatarAudio';
import type { Demonstration, EnonceLu, ReactionPreparee } from '../types';
import type { LectureDemo } from '../DemonstrationPleine';

/**
 * La voix du tuteur pendant le cycle de mémoire (rappel, retrouver, exercice du bloc) : une seule piste à la fois.
 * Réaction préparée → sa piste (aucun serveur) ; sinon le texte dit par la voix en direct (`/tts/speak`, normalisé au
 * serveur : symboles, nombres, unités). Chaque piste passe par l'analyseur partagé pour que la bouche du tuteur suive le
 * son (skill cours-concentration).
 */
let courant: HTMLAudioElement | null = null;
/** Chaque nouvelle parole (ou `taire`) invalide celles qui se préparaient encore. */
let tour = 0;
const jeton = () => { try { return localStorage.getItem('token') || ''; } catch { return ''; } };

export function taire() { tour += 1; courant?.pause(); courant = null; }

function lire(src: string): HTMLAudioElement {
  taire();
  const a = new Audio(src);
  courant = a;
  a.addEventListener('play', () => observeAvatarMedia(a), { once: true });
  void a.play().catch(() => { /* lecture refusée (pas encore de geste) : l'écrit reste */ });
  return a;
}

async function voixDe(parole: string): Promise<string | null> {
  try {
    const r = await fetch('/api/v1/tts/speak', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton()}` },
      body: JSON.stringify({ text: parole, language: 'mixed' }) });
    return r.ok ? URL.createObjectURL(await r.blob()) : null;
  } catch { return null; }
}

export async function direTexte(parole: string) {
  if (!parole.trim()) return;
  const t = ++tour;
  const url = await voixDe(parole);
  if (url && t === tour) lire(url);
}

export function jouerReaction(r: ReactionPreparee) {
  if (r.audio) lire(r.audio);
  else void direTexte(r.parole);
}

/**
 * Le tuteur lit l'énoncé quand la question s'ouvre (12 novembre 2026) : `enonce_audio` (piste préparée), sinon
 * `enonce_dit`, sinon l'énoncé écrit (normalisé au serveur). Les options ne sont pas lues. `taire` l'arrête.
 */
export function lireEnonce(q: EnonceLu & { prompt?: string }) {
  if (q.enonce_audio) { lire(q.enonce_audio); return; }
  void direTexte((q.enonce_dit || q.prompt || '').trim());
}

/** La voix qui parle encore (réaction) : la démonstration attend qu'elle ait fini. */
export function attendreLaFin(max = 20000): Promise<void> {
  return new Promise(ok => {
    const debut = Date.now();
    const tic = () => { const a = courant; if (a && !a.paused && !a.ended && Date.now() - debut < max) { window.setTimeout(tic, 250); return; } ok(); };
    window.setTimeout(tic, 300);
  });
}

/** La démonstration dite : sa piste, sinon la voix en direct ; sans voix, au temps de lecture (≈ 14 caractères/s). */
export function lireDemonstration(d: Demonstration): LectureDemo {
  const n = Math.max(1, d.parole.length);
  let arrete = false, finir: () => void = () => {};
  const fin = new Promise<void>(ok => { finir = ok; });
  let audio: HTMLAudioElement | null = null, t0 = 0;
  const sansVoix = () => { if (arrete) return; t0 = performance.now(); window.setTimeout(() => finir(), (n / 14) * 1000 + 1500); };
  const brancher = (a: HTMLAudioElement) => {
    audio = a;
    a.addEventListener('ended', () => finir(), { once: true });
    a.addEventListener('error', () => { audio = null; sansVoix(); }, { once: true });
  };
  if (d.audio) brancher(lire(d.audio));
  else {
    const t = ++tour;
    void voixDe(d.parole).then(url => {
      if (arrete || t !== tour) return;
      if (url) brancher(lire(url)); else sansVoix();
    });
  }
  return {
    position: () => {
      const a = audio;
      if (a) return Number.isFinite(a.duration) && a.duration > 0 ? (a.currentTime / a.duration) * n : 0;
      return t0 ? ((performance.now() - t0) / 1000) * 14 : 0;
    },
    fin,
    arreter: () => { if (arrete) return; arrete = true; if (audio && courant === audio) taire(); finir(); },
  };
}
