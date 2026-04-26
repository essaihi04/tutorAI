/**
 * Exam Grading Utilities — BAC Maroc
 *
 * Shared helpers for:
 *  - Computing the BAC mention (Très Bien, Bien, Assez Bien, Passable, Insuffisant)
 *  - Grading colors / gradients for consistent UI
 *  - Encouraging messages adapted to the score
 *  - Per-subject methodology tips for the pre-start screen
 *  - Score extraction from LLM feedback (same regex as backend)
 *  - localStorage autosave helpers (resilient to crashes)
 */

/* ------------------------------------------------------------------ */
/*  Mention BAC (Maroc)                                                 */
/* ------------------------------------------------------------------ */

export type MentionKey = 'tres_bien' | 'bien' | 'assez_bien' | 'passable' | 'insuffisant';

export interface MentionInfo {
  key: MentionKey;
  label: string;
  emoji: string;
  short: string;
  gradient: string;    // tailwind `from-x to-y`
  bg: string;          // tailwind background class
  border: string;      // tailwind border class
  text: string;        // tailwind text color
  ring: string;        // tailwind ring color
  encouragement: string; // adapted message
}

/**
 * Return the BAC mention info for a score out of 20.
 * Thresholds follow the official Moroccan BAC grid.
 */
export function getMention(scoreOn20: number): MentionInfo {
  const s = Math.max(0, Math.min(20, scoreOn20));

  if (s >= 16) {
    return {
      key: 'tres_bien',
      label: 'Très Bien',
      emoji: '🏆',
      short: 'TB',
      gradient: 'from-emerald-500 to-teal-600',
      bg: 'bg-emerald-500/10',
      border: 'border-emerald-400/30',
      text: 'text-emerald-300',
      ring: 'ring-emerald-400/40',
      encouragement:
        'Excellent niveau ! Tu maîtrises le programme. Continue à t\'entraîner sur les sujets difficiles pour viser encore plus haut.',
    };
  }
  if (s >= 14) {
    return {
      key: 'bien',
      label: 'Bien',
      emoji: '⭐',
      short: 'B',
      gradient: 'from-blue-500 to-indigo-600',
      bg: 'bg-blue-500/10',
      border: 'border-blue-400/30',
      text: 'text-blue-300',
      ring: 'ring-blue-400/40',
      encouragement:
        'Très bon travail ! Tu es sur la bonne voie. Identifie les points à consolider pour viser la mention Très Bien.',
    };
  }
  if (s >= 12) {
    return {
      key: 'assez_bien',
      label: 'Assez Bien',
      emoji: '👍',
      short: 'AB',
      gradient: 'from-sky-500 to-blue-500',
      bg: 'bg-sky-500/10',
      border: 'border-sky-400/30',
      text: 'text-sky-300',
      ring: 'ring-sky-400/40',
      encouragement:
        'Bon résultat. Tu as les bases solides. Travaille les questions de raisonnement et les schémas pour monter en mention.',
    };
  }
  if (s >= 10) {
    return {
      key: 'passable',
      label: 'Passable',
      emoji: '✅',
      short: 'P',
      gradient: 'from-amber-500 to-orange-500',
      bg: 'bg-amber-500/10',
      border: 'border-amber-400/30',
      text: 'text-amber-300',
      ring: 'ring-amber-400/40',
      encouragement:
        'Tu as la moyenne ! Concentre-toi sur les parties où tu as perdu des points et refais les exercices similaires.',
    };
  }
  return {
    key: 'insuffisant',
    label: 'À retravailler',
    emoji: '📚',
    short: 'R',
    gradient: 'from-rose-500 to-red-600',
    bg: 'bg-rose-500/10',
    border: 'border-rose-400/30',
    text: 'text-rose-300',
    ring: 'ring-rose-400/40',
    encouragement:
      'Pas de panique. Reprends les cours un par un, puis refais cet examen en mode Entraînement pour comprendre chaque erreur.',
  };
}

/**
 * Compute the normalized /20 score from a raw score + max.
 * Returns a number rounded to 2 decimals (like the Moroccan BAC transcript).
 */
export function toScoreOn20(rawScore: number, maxScore: number): number {
  if (!maxScore || maxScore <= 0) return 0;
  const s = (rawScore / maxScore) * 20;
  return Math.round(Math.max(0, Math.min(20, s)) * 100) / 100;
}

/**
 * Extract numeric score from LLM feedback text (e.g. "## Note\n1.5/2").
 * Mirror of backend `_extract_score_from_feedback` regex.
 */
export function extractScoreFromFeedback(
  feedback: string,
  maxPoints: number,
): number {
  if (!feedback) return 0;
  const match = feedback.match(
    /(?:##\s*Note|\*?\*?Note)\s*:?[ \t]*\n?[ \t]*(\d+(?:[.,]\d+)?)\s*\//i,
  );
  if (!match) return 0;
  const val = parseFloat(match[1].replace(',', '.'));
  if (Number.isNaN(val)) return 0;
  return Math.min(val, maxPoints);
}

/* ------------------------------------------------------------------ */
/*  BAC thresholds (context for the score screen)                       */
/* ------------------------------------------------------------------ */

/** Rough reference thresholds to contextualise the score (Sciences Physiques BIOF). */
export const BAC_CONTEXT = {
  admission: 10,       // moyenne pour avoir le BAC
  selective: 12,       // seuil "branches sélectives" (médecine, écoles d'ingénieurs)
  excellent: 14,       // seuil "Bien / concours grandes écoles"
  top: 16,             // seuil "Très Bien"
};

export function getBacContextMessage(scoreOn20: number): string {
  if (scoreOn20 >= BAC_CONTEXT.top) {
    return `À ce niveau au BAC, tu viserais les meilleurs concours (médecine, grandes écoles d'ingénieurs).`;
  }
  if (scoreOn20 >= BAC_CONTEXT.excellent) {
    return `Avec cette note au BAC, les filières sélectives te sont ouvertes. Continue comme ça.`;
  }
  if (scoreOn20 >= BAC_CONTEXT.selective) {
    return `Cette note te donne accès à la majorité des filières universitaires. Vise 14+ pour les sélectives.`;
  }
  if (scoreOn20 >= BAC_CONTEXT.admission) {
    return `Tu as la moyenne. L'objectif maintenant : monter à 12+ pour les filières sélectives.`;
  }
  const missing = (BAC_CONTEXT.admission - scoreOn20).toFixed(1);
  return `Il te manque ${missing} points pour la moyenne. Reprends les chapitres faibles avant le prochain essai.`;
}

/* ------------------------------------------------------------------ */
/*  Methodology tips per subject (pre-start screen)                     */
/* ------------------------------------------------------------------ */

export interface SubjectTips {
  subject: string;
  tips: string[];
  timeAdvice: string;
}

export function getSubjectTips(subject: string): SubjectTips {
  const s = (subject || '').toLowerCase();

  if (s.includes('svt') || s.includes('vie') || s.includes('biologie')) {
    return {
      subject: 'SVT',
      timeAdvice:
        'Accorde ~1h à la Restitution des connaissances et ~2h au Raisonnement scientifique.',
      tips: [
        'Lis chaque document 2 fois avant de répondre — schémas, légendes, unités.',
        'Utilise un vocabulaire précis : "document", "observation", "hypothèse", "conclusion".',
        'Pour les schémas, fais un titre, des légendes complètes et respecte les proportions.',
        'Relie toujours la réponse à la question : "Donc, d\'après le document 2…".',
      ],
    };
  }
  if (s.includes('physique') || s.includes('chimie')) {
    return {
      subject: 'Physique-Chimie',
      timeAdvice:
        'Répartis équitablement : une partie physique et une partie chimie. Ne reste jamais bloqué plus de 10 min sur un calcul.',
      tips: [
        'Écris toujours la formule littérale AVANT l\'application numérique.',
        'Vérifie les unités à chaque étape — une erreur d\'unité = points perdus.',
        'Pour la chimie : équilibre les équations et indique les états (s, l, g, aq).',
        'Garde les chiffres significatifs cohérents avec l\'énoncé.',
      ],
    };
  }
  if (s.includes('math')) {
    return {
      subject: 'Mathématiques',
      timeAdvice:
        'Fais d\'abord les exercices où tu te sens fort. Laisse 30 min pour relecture.',
      tips: [
        'Justifie chaque passage — "d\'après le théorème de…", "puisque la fonction est continue…".',
        'Pour les études de fonction : domaine, limites, dérivée, tableau, courbe.',
        'En probabilités/complexes, écris la formule avant de remplacer les valeurs.',
        'Si tu es bloqué, passe à la question suivante et reviens à la fin.',
      ],
    };
  }

  return {
    subject: subject || 'Examen',
    timeAdvice: 'Lis tout le sujet avant de commencer et répartis ton temps par partie.',
    tips: [
      'Lis bien la question avant de répondre.',
      'Commence par les questions que tu maîtrises le mieux.',
      'Soigne la présentation et l\'orthographe.',
      'Garde 10 min à la fin pour te relire.',
    ],
  };
}

/* ------------------------------------------------------------------ */
/*  Autosave helpers (localStorage, resilient to crashes)               */
/* ------------------------------------------------------------------ */

const AUTOSAVE_TTL_MS = 24 * 60 * 60 * 1000; // 24h

export interface AutosavePayload {
  version: number;
  savedAt: number;   // Date.now() ms
  data: unknown;
}

export function autosaveGet<T = unknown>(key: string): T | null {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as AutosavePayload;
    if (!parsed || typeof parsed !== 'object') return null;
    if (Date.now() - (parsed.savedAt || 0) > AUTOSAVE_TTL_MS) {
      localStorage.removeItem(key);
      return null;
    }
    return parsed.data as T;
  } catch {
    return null;
  }
}

export function autosaveSet(key: string, data: unknown): void {
  try {
    const payload: AutosavePayload = {
      version: 1,
      savedAt: Date.now(),
      data,
    };
    localStorage.setItem(key, JSON.stringify(payload));
  } catch {
    // Quota or serialization failure — silent to avoid breaking the exam flow
  }
}

export function autosaveClear(key: string): void {
  try {
    localStorage.removeItem(key);
  } catch {
    /* noop */
  }
}

export function autosaveSavedAt(key: string): number | null {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as AutosavePayload;
    return parsed?.savedAt ?? null;
  } catch {
    return null;
  }
}

/**
 * Human-friendly relative time ("il y a 2 min").
 */
export function timeAgo(timestampMs: number): string {
  const diff = Math.max(0, Date.now() - timestampMs);
  const sec = Math.floor(diff / 1000);
  if (sec < 60) return 'à l\'instant';
  const min = Math.floor(sec / 60);
  if (min < 60) return `il y a ${min} min`;
  const hr = Math.floor(min / 60);
  if (hr < 24) return `il y a ${hr} h`;
  const d = Math.floor(hr / 24);
  return `il y a ${d} j`;
}

/* ------------------------------------------------------------------ */
/*  Duration formatting                                                 */
/* ------------------------------------------------------------------ */

export function formatDuration(seconds: number): string {
  if (!Number.isFinite(seconds) || seconds < 0) return '—';
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  if (h > 0) {
    return `${h}h ${m.toString().padStart(2, '0')}`;
  }
  return `${m}:${s.toString().padStart(2, '0')}`;
}
