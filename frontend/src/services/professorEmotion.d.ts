export type ProfessorEmotionKind = 'greet' | 'goodbye' | 'celebrate' | 'love' | 'encourage' | 'laugh' | 'surprise' | 'think' | 'wrong';
export type ProfessorGestureKind = 'wave' | 'cheer' | 'heart' | 'nod' | 'laugh' | 'startle' | 'shake';
export const PROFESSOR_EMOTIONS: Record<ProfessorEmotionKind, { gesture: ProfessorGestureKind | null; emojis: string[]; count: number }>;
export const REPONSE_ELEVE_EVENT: 'moalim:reponse-eleve';
export function signalerReponseEleve(juste: boolean): void;
export function detectProfessorEmotion(text: string, speaker?: 'ai' | 'student'): ProfessorEmotionKind | null;
export function emotionPourReponse(juste: boolean): ProfessorEmotionKind;
export function emotionPourEvaluation(evaluation: string): ProfessorEmotionKind | null;
