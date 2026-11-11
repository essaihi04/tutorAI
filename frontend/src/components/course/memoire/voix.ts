import { observeAvatarMedia } from '../../../services/avatarAudio';
import type { ReactionPreparee } from '../types';

/**
 * La voix du tuteur pendant le cycle de mémoire (rappel, retrouver, exercice du bloc) : une seule piste à la fois.
 * Réaction préparée → sa piste (aucun serveur) ; sinon le texte dit par la voix en direct (`/tts/speak`).
 * Chaque piste passe par l'analyseur partagé pour que la bouche du tuteur suive le son (skill cours-concentration).
 */
let courant: HTMLAudioElement | null = null;
const jeton = () => { try { return localStorage.getItem('token') || ''; } catch { return ''; } };

export function taire() { courant?.pause(); courant = null; }

function lire(src: string) {
  taire();
  const a = new Audio(src);
  courant = a;
  a.addEventListener('play', () => observeAvatarMedia(a), { once: true });
  void a.play().catch(() => { /* lecture refusée (pas encore de geste) : l'écrit reste */ });
}

export async function direTexte(parole: string) {
  if (!parole.trim()) return;
  try {
    const r = await fetch('/api/v1/tts/speak', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton()}` },
      body: JSON.stringify({ text: parole, language: 'mixed' }) });
    if (r.ok) lire(URL.createObjectURL(await r.blob()));
  } catch { /* sans voix, l'écrit suffit */ }
}

export function jouerReaction(r: ReactionPreparee) {
  if (r.audio) lire(r.audio);
  else void direTexte(r.parole);
}
