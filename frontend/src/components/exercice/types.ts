/**
 * Partie « Exercices » (22 novembre 2026) : un exercice d'application du premier semestre, écrit pour Moalim (jamais
 * un sujet du national : ceux-là sont dans la partie Examen), servi en JSON par `/media/exercices/<id>.json`.
 * Contrat complet : skill `.agents/skills/exercices/SKILL.md`.
 *
 * L'énoncé est du contenu (texte + figures en code, comme le cahier) ; l'explication animée et la version facile sont
 * des diapositives au format des cours : elles passent par le même lecteur (`CoursePlayer`), les mêmes simulations,
 * les mêmes réactions préparées et la même chaîne de voix.
 */
import type { FigureCahierData } from '../course/FigureCahier';
import type { CourseSlide } from '../course/types';

export type MatiereExercice = 'physique' | 'mathematiques' | 'svt';

export interface AideExercice {
  /** l'indice écrit (français) */
  texte: string;
  /** ce que dit le tuteur (darija + français, règles de la voix) */
  dit: string;
  audio?: string;
}

export interface LigneCorrection {
  texte: string;
  /** passage de `parole` où la ligne s'écrit */
  mot?: string;
}

export interface ReponseAttendue {
  /** `valeur` : un nombre jugé dans le navigateur (tolérance relative) ; `phrase` : jugée par le tuteur */
  type: 'valeur' | 'phrase';
  /** la réponse complète, telle qu'on l'écrit sur la copie */
  attendu: string;
  grandeur?: string;
  valeur?: number;
  unite?: string;
  /** tolérance relative (0,03 = 3 %) */
  tolerance?: number;
}

export interface QuestionExercice {
  id: string;
  texte: string;
  texte_dit?: string;
  texte_audio?: string;
  reponse: ReponseAttendue;
  /** suggestions du clavier pour CETTE réponse (aides justes et pièges plausibles, jamais la réponse) */
  clavier?: { aides?: string[]; pieges?: string[] };
  /** de la piste à la méthode : jamais la réponse elle-même */
  aides?: AideExercice[];
  correction: { lignes: LigneCorrection[]; parole: string; audio?: string };
  /** id de la diapositive d'explication animée (dans `explication`) */
  explication?: string;
  /** id de la diapositive « plus facile » (QCM, vrai/faux, association) dans `facile` */
  facile?: string;
}

export interface EnonceExercice {
  intro: string;
  intro_dit?: string;
  intro_audio?: string;
  figures?: FigureCahierData[];
  donnees?: string[];
  questions: QuestionExercice[];
}

export interface DeckDiapos {
  activities: { id: string; title: string; slides: CourseSlide[] }[];
}

export interface Exercice {
  id: string;
  type: 'exercice';
  version: number;
  status?: string;
  matiere: MatiereExercice;
  chapitre: string;
  /** le cours dont il applique les notions */
  cours: string;
  titre: string;
  /** facile : une relation, une étape ; moyen : deux étapes ou une lecture de document ; difficile : raisonnement en plusieurs étapes, au niveau des examens */
  niveau?: 'facile' | 'moyen' | 'difficile';
  duree_min?: number;
  origine?: string;
  competences?: string[];
  enonce: EnonceExercice;
  explication: DeckDiapos;
  facile: DeckDiapos;
  /** même exercice, autres données : sans aide ni version facile, le tuteur corrige seulement */
  similaire: { id: string; titre: string; enonce: EnonceExercice };
}

export interface FicheIndex {
  id: string; matiere: MatiereExercice; chapitre: string; cours: string; titre: string; niveau?: string; duree_min?: number; questions: number;
}
