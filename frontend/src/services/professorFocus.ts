/** Internal board cue; DOM nodes never come from model-generated selectors. */
export const PROFESSOR_FOCUS = 'moalim:board-focus';
/**
 * Délai entre l'arrivée d'une commande de simulation et son exécution : le temps que le
 * professeur vole jusqu'au bouton et appuie dessus. La scène l'attend, l'avatar l'anime.
 */
export const PROFESSOR_REACH_MS = 850;
export function focusProfessor(element: HTMLElement | null) {
  window.dispatchEvent(new CustomEvent(PROFESSOR_FOCUS, { detail: element }));
}
/** Durée pendant laquelle le professeur garde le doigt sur un repère de simulation qu'il explique. */
export const PROFESSOR_POINT_HOLD_MS = 5200;
/** Commandes de simulation qui montrent un repère au lieu d'appuyer sur un bouton. */
export const POINTING_COMMANDS = new Set(['highlight', 'point', 'montrer', 'show']);
