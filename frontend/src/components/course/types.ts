import type { ScientificVisualSpec } from '../session/scientific/types';

export type CourseSlideType =
  | 'diagnostic'
  | 'situation'
  | 'concept'
  | 'image'
  | 'schema'
  | 'simulation'
  | 'exercise'
  | 'synthesis'
  | 'evaluation';

export interface CourseQuestion {
  type?: 'qcm' | 'prediction' | 'true_false' | 'select' | 'open' | 'ordering' | 'association';
  prompt?: string;
  options?: string[];
  timeout_seconds?: number;
  advance_on_timeout?: boolean;
  /** Index de la bonne option (mode concentration : correction immédiate et réaction préparée). */
  correct?: number;
}

/** Réaction du tuteur préparée d'avance pour une réponse possible (texte dit, texte écrit, piste audio). */
export interface ReactionPreparee { parole: string; ecrit: string; audio?: string }

/**
 * Un exercice CLIQUABLE posé sur le tableau, à la fin d'une étape.
 *
 * `question` interroge à l'oral : le tableau pose l'énoncé, attend une
 * réponse, puis corrige et poursuit. C'est une vérification au passage, une
 * seule, et elle bloque le fil. Une fin d'étape demande autre chose : plusieurs
 * exercices posés ensemble, que l'élève manipule à son rythme et qui se
 * corrigent tout seuls sous ses doigts — QCM à choisir, paires à relier.
 *
 * Ils sont rendus par les mêmes blocs interactifs que le tableau du tuteur
 * (`boardLines`), donc la correction voyage avec l'énoncé : ces exercices
 * s'auto-corrigent dans le navigateur, ils ne notent pas.
 */
export interface CourseExercise {
  type: 'qcm' | 'vrai_faux' | 'association';
  /** L'énoncé. Pour une association, la consigne de mise en relation. */
  prompt: string;
  /** `qcm` : les propositions, et l'index de la bonne. */
  choices?: string[];
  correct?: number;
  /** `vrai_faux` : les affirmations à trancher une par une. */
  statements?: { text: string; correct: boolean; explanation?: string }[];
  /** `association` : les paires à reformer (la colonne de droite est battue). */
  pairs?: { left: string; right: string }[];
  /** Le mot de la fin, affiché une fois l'élève fixé. */
  explanation?: string;
}

export interface CourseVisual {
  /**
   * `scientific` couvre les figures que personne n'a dessinées à l'avance :
   * géométrie et courbes (JSXGraph), chaînes et réseaux (Cytoscape), petite
   * mécanique 2D (Matter). Mêmes moteurs que le tableau du tuteur — une
   * diapositive n'a donc plus à choisir entre une image figée et rien.
   */
  kind?: 'none' | 'image' | 'schema' | 'simulation' | 'scientific';
  url?: string;
  schema_id?: string;
  scientific?: ScientificVisualSpec;
  caption?: string;
  alt?: string;
  required_interaction?: boolean;
  /**
   * `inline` place un croquis dans le fil du texte. C'est utile quand la
   * figure fait partie de l'explication et ne mérite pas un tableau séparé.
   */
  placement?: 'side' | 'inline';
}

export interface PublishedSlideAudio {
  url: string;
  duration_ms?: number | null;
  version?: number;
  speech_hash?: string;
  status?: string;
}

export interface CourseSlide {
  id: string;
  stable_id?: string;
  slide_type: CourseSlideType;
  title: string;
  screen_content?: {
    lead?: string;
    bullets?: string[];
    essential_text?: string;
    student_trace?: string;
    caption?: string;
    alt?: string;
    table?: {
      headers: string[];
      rows: string[][];
    };
  };
  visual?: CourseVisual;
  speech_text?: Record<string, string>;
  question?: CourseQuestion;
  /** Les exercices cliquables posés au tableau après la correction écrite. */
  exercises?: CourseExercise[];
  timing?: {
    auto_advance?: boolean;
    reading_seconds?: number;
    delay_after_feedback_ms?: number;
  };
  audio?: Record<string, PublishedSlideAudio>;
  order_index?: number;
  /** Mode concentration (`CourseFocusStage`) : ce que le tuteur 3D montre, et quand. */
  concentration?: SlideConcentration;
  /** Les compétences du cours que cette diapositive travaille (suivi des acquis). */
  competence_ids?: string[];
}

/** Une compétence du cours : l'unité du suivi des acquis (skill `suivi-des-acquis`). */
export interface CourseCompetence { id: string; label: string; slide_ids?: string[]; /** le nom dit par la voix (sans symbole) */ dit?: string }

/**
 * Le mode concentration : l'écrit est fermé, le tuteur 3D montre au rythme de la voix.
 * `mot` est un extrait exact du texte parlé ; sa place dans le texte donne l'instant.
 */
export interface SlideConcentration {
  /** Commande que le tuteur appuie dans la simulation quand la voix commence (start, fire_pulse). */
  demarrer?: string;
  /**
   * `repere` : repère dessiné dans la simulation ; `cible` : 'visuel', 'ligne:N' (tableau), 'centre:N' ;
   * `commande` : le tuteur appuie (relance la simulation au moment où la voix l'explique).
   */
  pointage?: { mot: string; repere?: string; cible?: string; commande?: string; parametres?: Record<string, unknown> }[];
  /** Formules ou mots-clés écrits au centre au moment où la voix les dit. */
  centre?: { texte: string; mot: string }[];
  /** La trace à recopier (bulle « À écrire dans le cahier »). */
  cahier?: string;
  /**
   * La comparaison que le tuteur fait LUI-MÊME après la voix, si l'élève n'a pas touché la simulation :
   * il change un réglage (M₂ plus loin, le fond plus bas…), rejoue et montre ce qui a changé.
   */
  variante?: { apres_s?: number; etapes: { commande?: string; parametres?: Record<string, unknown>; repere?: string }[] };
  /**
   * Les réactions préparées, pour CHAQUE réponse possible : `reponses[cle][option]` avec `juste` (bonne option)
   * ou `1` (indice, 1er essai) et `2` (réponse et justification, 2e essai). `cle` : `q` (question de la
   * diapositive), `e{i}` (QCM de l'exercice i), `e{i}s{j}` (affirmation j d'un vrai/faux ; option 0 = Vrai).
   */
  reponses?: Record<string, Record<string, Partial<Record<'juste' | '1' | '2', ReactionPreparee>>>>;
  /**
   * La diapositive fait le bilan des acquis (fiche « ce qu'il faut retenir », carte du chapitre) : le lecteur lit le
   * bilan de l'élève (GET /course-player/acquis/{deck}), le donne à la simulation (`set_parameters {lacunes, acquis,
   * acquis_ids}`) et, la voix finie, le tuteur nomme ce qu'il reste à retravailler puis fige la page « lacunes ».
   */
  acquis?: boolean;
}

export interface CourseActivity {
  id: string;
  stable_id?: string;
  title: string;
  phase?: string;
  duration_minutes?: number;
  objective_ids?: string[];
  order_index?: number;
  slides: CourseSlide[];
}

export interface CourseDeck {
  id: string;
  /** Identifiant stable du manifeste (le même en local et en base) : c'est lui que suit le suivi des acquis. */
  stable_id?: string;
  lesson_id: string;
  title: string;
  version?: number;
  language?: string;
  estimated_minutes?: number;
  source?: 'database' | 'manifest';
  activities: CourseActivity[];
  competences?: CourseCompetence[];
  /** `concentration` : le cours se joue en mode concentration, avec le tuteur 3D du cours (cours refaits). */
  mode?: 'tableau' | 'concentration';
}

export interface CourseProgressSnapshot {
  current_activity_id?: string | null;
  current_slide_id?: string | null;
  audio_position_ms?: number;
  completed_slide_ids?: string[];
  status?: 'not_started' | 'in_progress' | 'completed';
}
