/**
 * Ce que l'élève est en train de faire — miroir de `backend/app/services/session_mode.py`.
 *
 * Le serveur est SEUL juge : ce fichier ne décide de rien, il traduit. Un clic
 * sur la barre de modes envoie `set_mode` et n'affiche rien tant que
 * `mode_changed` n'est pas revenu — sinon l'écran montrerait un mode que la
 * session a refusé (mot inconnu, sortie d'examen tentée par le tuteur), et
 * l'élève se retrouverait dans une interface qui ne correspond à rien.
 *
 * Les deux listes ci-dessous doivent rester alignées sur MODES et LEGACY
 * côté serveur. Elles sont courtes exprès : quatre mots, c'est tout ce qu'un
 * lycéen doit avoir à comprendre.
 */

export type TutorMode = 'cours' | 'exercice' | 'examen' | 'question';

export const TUTOR_MODES: TutorMode[] = ['cours', 'exercice', 'examen', 'question'];

export const MODE_LABELS: Record<TutorMode, { label: string; icon: string; hint: string }> = {
  cours: { label: 'Cours', icon: '📚', hint: 'Le tuteur explique et écrit au tableau' },
  exercice: { label: 'Exercice', icon: '✏️', hint: 'Tu cherches, il te guide et corrige' },
  examen: { label: 'Examen', icon: '⏱️', hint: 'Conditions réelles, chrono, note sur 20' },
  question: { label: 'Question', icon: '💬', hint: 'Demande ce que tu veux' },
};

/**
 * Le mode de départ, déduit de la prop de route historique.
 *
 * `explain` est la route ouverte depuis le panneau d'examen : elle porte
 * l'énoncé et la correction, donc elle démarre en `examen`. La confondre avec
 * « explication » enverrait l'élève en cours à la place de son épreuve.
 */
export function modeDepuisRoute(route?: 'standard' | 'libre' | 'explain'): TutorMode {
  if (route === 'explain') return 'examen';
  if (route === 'libre') return 'question';
  return 'cours';
}

export function estUnMode(valeur: unknown): valeur is TutorMode {
  return typeof valeur === 'string' && (TUTOR_MODES as string[]).includes(valeur);
}
