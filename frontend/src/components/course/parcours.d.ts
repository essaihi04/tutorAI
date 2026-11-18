import type { CourseSlide } from './types';

/** L'état gardé d'une question (`localStorage`, clé `reponse:<deck>:<diapo>:<cle>`). */
export type EtatGarde = Partial<{ tentative: number; retour: { correct: boolean | null; ecrit?: string } | null; passee: boolean }> | null | undefined;
export type Etape = { commande?: string; parametres?: Record<string, unknown>; repere?: string };
export type Rejeu = { question: string; etapes: Etape[]; sim_avant: Record<string, unknown> | null; duree_s: number };

export function clesDesQuestions(slide: CourseSlide | null | undefined): string[];
export function rejeuxDe(slide: CourseSlide | null | undefined): Rejeu[];
export function rejeuDe(slide: CourseSlide | null | undefined, cle?: string): Rejeu | null;
export function momentsDuRejeu(rejeu: Rejeu | null | undefined): Set<string>;
export function momentsReserves(slide: CourseSlide | null | undefined, faits?: Set<string>): Set<string>;
export function commandeReservee(commande: string | undefined, parametres: Record<string, unknown> | undefined, reserves: Set<string> | null | undefined): boolean;
export function dureeDuRejeuMs(rejeu: Rejeu | null): number;
export function questionClose(etat: EtatGarde, essaisMax?: number): boolean;
export function diagnosticsDuRappel(slide: CourseSlide | null | undefined): string[];
export function justeDuPremierCoup(etat: EtatGarde): boolean;
export function rappelASauter(slide: CourseSlide, parId: Map<string, CourseSlide> | Record<string, CourseSlide>, lireEtat: (slideId: string, cle: string) => EtatGarde): boolean;
export function diapoSuivante(slides: CourseSlide[], index: number, lireEtat: (slideId: string, cle: string) => EtatGarde, revus?: Set<string>): { index: number; sautes: string[] };
