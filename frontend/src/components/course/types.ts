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
  };
  visual?: CourseVisual;
  speech_text?: Record<string, string>;
  question?: CourseQuestion;
  timing?: {
    auto_advance?: boolean;
    reading_seconds?: number;
    delay_after_feedback_ms?: number;
  };
  audio?: Record<string, PublishedSlideAudio>;
  order_index?: number;
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
  lesson_id: string;
  title: string;
  version?: number;
  language?: string;
  estimated_minutes?: number;
  source?: 'database' | 'manifest';
  activities: CourseActivity[];
}

export interface CourseProgressSnapshot {
  current_activity_id?: string | null;
  current_slide_id?: string | null;
  audio_position_ms?: number;
  completed_slide_ids?: string[];
  status?: 'not_started' | 'in_progress' | 'completed';
}
