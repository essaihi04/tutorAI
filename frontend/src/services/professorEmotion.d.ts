export type ProfessorEmotionKind = 'greet' | 'goodbye' | 'celebrate' | 'love' | 'encourage' | 'think';
export type ProfessorGestureKind = 'wave' | 'cheer' | 'heart' | 'nod';
export const PROFESSOR_EMOTIONS: Record<ProfessorEmotionKind, { gesture: ProfessorGestureKind | null; emojis: string[]; count: number }>;
export function detectProfessorEmotion(text: string, speaker?: 'ai' | 'student'): ProfessorEmotionKind | null;
