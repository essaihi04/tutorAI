/* ════════════════════════════════════════════════════════════
   Moalim — Analytics helper (Umami)
   ────────────────────────────────────────────────────────────
   Wrapper typé autour de window.moalimTrack (défini dans /js/umami.js).
   Échoue silencieusement si Umami n'est pas chargé (dev, ad-blocker…).
   ════════════════════════════════════════════════════════════ */

type EventData = Record<string, string | number | boolean>;

declare global {
  interface Window {
    moalimTrack?: (eventName: string, eventData?: EventData) => void;
    umami?: {
      track: (eventName: string, eventData?: EventData) => void;
    };
  }
}

/**
 * Track un événement custom Umami.
 * Usage :
 *   track('diagnostic_started', { filiere: 'svt' })
 *   track('signup_clicked')
 */
export function track(eventName: string, eventData?: EventData): void {
  if (typeof window === 'undefined') return;
  try {
    if (typeof window.moalimTrack === 'function') {
      window.moalimTrack(eventName, eventData);
    } else if (window.umami && typeof window.umami.track === 'function') {
      if (eventData) window.umami.track(eventName, eventData);
      else window.umami.track(eventName);
    }
  } catch {
    // silent fail — never break the UX for analytics
  }
}

/* ─── Constantes des événements (single source of truth) ─── */
export const EVENTS = {
  // Diagnostic gratuit (home)
  DIAGNOSTIC_FILIERE_CHOSEN: 'diagnostic_filiere_chosen',
  DIAGNOSTIC_QUESTION_ANSWERED: 'diagnostic_question_answered',
  DIAGNOSTIC_COMPLETED: 'diagnostic_completed',
  DIAGNOSTIC_RESTARTED: 'diagnostic_restarted',

  // Conversion
  CTA_SIGNUP_CLICKED: 'cta_signup_clicked',
  CTA_DEMO_CLICKED: 'cta_demo_clicked',
  CTA_PREDICTIONS_CLICKED: 'cta_predictions_clicked',

  // Auth
  SIGNUP_STARTED: 'signup_started',
  SIGNUP_COMPLETED: 'signup_completed',
  LOGIN_COMPLETED: 'login_completed',

  // Blog / contenu
  BLOG_ARTICLE_VIEW: 'blog_article_view',
  BLOG_CTA_CLICKED: 'blog_cta_clicked',
} as const;

export type MoalimEvent = (typeof EVENTS)[keyof typeof EVENTS];
