import { useEffect, useRef } from 'react';

/**
 * La saturation arrête les explications (skill `cours-concentration`, « Memory and rhythm ») : deux réponses fausses de
 * suite, des réponses données bien plus vite que le temps de les lire, ou une longue inactivité → plus de nouvelle idée ;
 * le tuteur passe au cahier, à l'exercice ou à la pause, et c'est noté (`evenement: 'saturation'`, cause et action).
 */
export type CauseSaturation = 'deux_fausses' | 'trop_rapide' | 'inactivite';

/** Le temps qu'il faut pour lire un texte (≈ 200 mots par minute, 2 s au moins). */
export function tempsDeLectureMs(...textes: (string | undefined)[]): number {
  const mots = textes.join(' ').split(/\s+/).filter(Boolean).length;
  return Math.max(2000, (mots / 3.3) * 1000);
}

/** Une réponse est « bien plus rapide que la lecture » sous 40 % du temps de lecture. */
export const FACTEUR_TROP_RAPIDE = 0.4;

export class DetecteurSaturation {
  private fausses = 0;
  private rapides = 0;

  /** Chaque réponse jugée : rend la cause si l'élève sature. */
  reponse({ correct, dureeMs, lectureMs }: { correct: boolean | null; dureeMs?: number; lectureMs?: number }): CauseSaturation | null {
    if (correct === false) this.fausses += 1;
    else if (correct === true) this.fausses = 0;
    if (dureeMs !== undefined && lectureMs && dureeMs < lectureMs * FACTEUR_TROP_RAPIDE) this.rapides += 1;
    else this.rapides = 0;
    if (this.fausses >= 2) { this.fausses = 0; return 'deux_fausses'; }
    if (this.rapides >= 2) { this.rapides = 0; return 'trop_rapide'; }
    return null;
  }

  remettreAZero() { this.fausses = 0; this.rapides = 0; }
}

/** Une longue inactivité (aucun geste, aucune touche) pendant que l'écran attend l'élève. */
export function useInactivite(actif: boolean, onInactif: () => void, delaiMs = 3 * 60_000) {
  const rappel = useRef(onInactif);
  rappel.current = onInactif;
  useEffect(() => {
    if (!actif) return;
    let minuteur = window.setTimeout(() => rappel.current(), delaiMs);
    const geste = () => { window.clearTimeout(minuteur); minuteur = window.setTimeout(() => rappel.current(), delaiMs); };
    const evts = ['pointerdown', 'keydown', 'wheel', 'touchstart'] as const;
    evts.forEach(e => window.addEventListener(e, geste, { passive: true }));
    return () => { window.clearTimeout(minuteur); evts.forEach(e => window.removeEventListener(e, geste)); };
  }, [actif, delaiMs]);
}

/** Ce que le tuteur fait quand l'élève sature : jamais une nouvelle idée. */
export function actionApresSaturation(etape: 'diapo' | 'cahier' | 'retrouver' | 'exercice', blocAvecCahier: boolean): 'cahier' | 'exercice' | 'pause' {
  if (etape === 'diapo' && blocAvecCahier) return 'cahier';
  if (etape === 'diapo' || etape === 'cahier' || etape === 'retrouver') return 'exercice';
  return 'pause';
}

export const PHRASES_SATURATION: Record<CauseSaturation, string> = {
  deux_fausses: 'On s’arrête un instant sur ce qu’on a déjà vu : pas de nouvelle idée pour l’instant.',
  trop_rapide: 'Tu vas très vite : prends le temps de lire, on consolide avant d’avancer.',
  inactivite: 'Tu as l’air fatigué : on range ce qu’on a vu, puis une petite pause.',
};
