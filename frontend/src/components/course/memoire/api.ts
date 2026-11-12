/**
 * Mémoire longue (11 novembre 2026) : les données des séances et des blocs, et les appels au serveur
 * (`/course-player/memoire/…`, `backend/app/api/v1/endpoints/memoire.py`). Sur le lien libre, `publication/coursOndes.tsx`
 * renvoie ces mêmes appels vers `/public/cours-ondes/memoire/…` avec l'identifiant du visiteur.
 *
 * Format des cours : skill `cours-concentration`, section « Memory and rhythm » → « Data ».
 */

import type { CourseDeck, EnonceLu, ReactionPreparee } from '../types';

/** Une question de rappel (`competences[].rappels`), d'exercice de bloc ou de « retrouver ». */
export interface QuestionMemoire extends EnonceLu {
  id?: string;
  type?: 'libre' | 'qcm' | 'vrai_faux' | string;
  prompt: string;
  /** La formule ou la définition attendue (réponse libre, jugée en direct). */
  attendu?: string;
  options?: string[];
  /** Index de la bonne option (vrai/faux : 0 = Vrai, 1 = Faux, ou un booléen). */
  correct?: number | boolean;
  demonstration?: unknown;
  competence_id?: string;
  /** Exercice de bloc : `choices` (forme des exercices de diapositive) vaut `options`. */
  choices?: string[];
  /** Exercice de bloc vrai/faux : les affirmations, une par une (chacune ses réactions préparées). */
  statements?: ({ text: string; correct: boolean; explanation?: string; reponses?: ReponsesPreparees } & EnonceLu)[];
  /** Le mot de la fin, montré une fois la question finie. */
  explanation?: string;
  /** L'exercice reprend celui d'une diapositive (`<slide>/e<i>`) : ses réactions préparées y sont lues. */
  reprend?: string;
  /** Réactions préparées : `{option: {juste | 1 | 2: {parole, ecrit, audio}}}` (vrai/faux : 0 = Vrai, 1 = Faux). */
  reponses?: ReponsesPreparees;
}

export type ReponsesPreparees = Record<string, Partial<Record<'juste' | '1' | '2', ReactionPreparee>>>;

export interface BlocCours {
  id: string;
  titre?: string;
  slide_ids: string[];
  cahier?: { texte: string }[];
  retrouver?: QuestionMemoire & { competence_id?: string };
  exercice?: QuestionMemoire;
}

export interface SeanceCours { id: string; titre?: string; blocs: BlocCours[] }

export interface RappelPropose {
  cours_id: string; cours_titre: string; competence_id: string; competence: string;
  marche: number; due: string; en_avance: boolean; jours_de_retard: number; question: QuestionMemoire;
}

export interface RappelsDuJour { matiere: string; nom_matiere: string; questions: RappelPropose[]; minutes: number }

export interface Progression {
  blocs: Record<string, { cahier: boolean; retrouver: string | null; exercice: string | null }>;
  seances_finies: string[];
  reprise: { seance: number; bloc: number; seance_id: string; bloc_id: string; etape: 'cahier' | 'retrouver' | 'exercice' } | null;
  nb_seances: number;
  termine: boolean;
}

export interface DebutSeance { cours_id: string; matiere: string; rappels: RappelsDuJour; progression: Progression | null }

export interface Accueil {
  badge: number;
  dus: Record<string, number>;
  notification: null | { matiere: string; nom_matiere: string; nombre: number; minutes: number; texte: string; niveau: 'banniere' | 'discret'; nouvelle: boolean };
  heure: number;
  heure_habituelle: number | null;
  preferences: { heure: number | null; coupees: boolean };
  ignorees: number;
}

/** Ce que l'écran note (le serveur date chaque événement). */
export interface EvenementMemoire {
  evenement: 'cahier' | 'retrouver' | 'exercice_bloc' | 'rappel' | 'saturation' | 'seance_debut' | 'seance_fin' | 'notification' | 'pause';
  cours_id?: string; seance_id?: string; bloc_id?: string; competence_id?: string; rappel_id?: string; matiere?: string;
  enonce?: string; reponse?: string; reponse_2?: string; correct?: boolean | null; correct_2?: boolean | null;
  duree_s?: number; en_avance?: boolean; complete?: boolean; cause?: string; action?: string;
  bloc_index?: number; seance_index?: number; type?: string;
  /** l'élève a passé la question (12 novembre 2026) : ni juste ni erreur, pas de reprise ; `correct: null` */
  passee?: boolean;
}

const jeton = () => { try { return localStorage.getItem('token') || ''; } catch { return ''; } };

async function appel<T>(chemin: string, init?: RequestInit): Promise<T> {
  const r = await fetch(`/api/v1/course-player/memoire${chemin}`, {
    ...init, headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton()}`, ...(init?.headers || {}) },
  });
  if (!r.ok) throw new Error(`${r.status}`);
  return r.json() as Promise<T>;
}

export const lireDebutSeance = (deckId: string) => appel<DebutSeance>(`/seance/${encodeURIComponent(deckId)}`);
export const lireRappels = (matiere: string) => appel<RappelsDuJour>(`/rappels/${encodeURIComponent(matiere)}`);
export const lireAccueil = () => appel<Accueil>('/accueil');
export const changerPreferences = (p: { heure: number | null; coupees: boolean }) =>
  appel<{ ok: boolean }>('/preferences', { method: 'POST', body: JSON.stringify(p) });

/** Noter un événement : jamais bloquant, un échec ne change rien à l'écran (skill `suivi-des-acquis`, règle 5). */
export function noter(e: EvenementMemoire): Promise<{ ok: boolean; marche?: number; prochaine?: string } | null> {
  return appel<{ ok: boolean; marche?: number; prochaine?: string }>('/evenement', { method: 'POST', body: JSON.stringify(e) }).catch(() => null);
}

/** Une réponse libre jugée en direct (DeepSeek, `/course-player/answer-reaction`), comme les réponses libres du cours. */
export async function jugerReponseLibre(q: QuestionMemoire, reponse: string, tentative: number, titre = ''):
  Promise<{ correct: boolean | null; parole: string; ecrit: string }> {
  const r = await fetch('/api/v1/course-player/answer-reaction', {
    method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton()}` },
    body: JSON.stringify({ diapo: { title: titre, speech: '' }, question: { type: 'directe', enonce: q.prompt, attendu: q.attendu || '' }, reponse, tentative, verdict: null }),
  });
  if (!r.ok) throw new Error(`${r.status}`);
  return r.json();
}

/** La matière d'un cours, comme le serveur la déduit (`memoire_longue.matiere_de`). */
export function matiereDe(deckId: string): string {
  const c = (deckId || '').toLowerCase();
  if (/^(phys|chem|chim|pc_)/.test(c)) return 'physique-chimie';
  if (c.startsWith('svt')) return 'svt';
  if (c.startsWith('math')) return 'mathematiques';
  return '';
}

/** Les séances d'un cours (`deck.seances`), s'il en a : sans séances, le cours marche comme avant. */
export function seancesDe(deck: unknown): SeanceCours[] {
  const s = (deck as { seances?: SeanceCours[] } | null)?.seances;
  return Array.isArray(s) ? s.filter(x => x && Array.isArray(x.blocs) && x.blocs.length) : [];
}

/** Le bloc d'une diapositive et sa place : séance n, bloc n, dernière diapositive du bloc ou non. */
export function placeDansLesSeances(seances: SeanceCours[], slideId: string):
  null | { seance: number; bloc: number; seanceCours: SeanceCours; blocCours: BlocCours; derniereDuBloc: boolean; dernierBlocDeLaSeance: boolean } {
  for (let i = 0; i < seances.length; i++) {
    for (let j = 0; j < seances[i].blocs.length; j++) {
      const b = seances[i].blocs[j];
      const k = b.slide_ids.indexOf(slideId);
      if (k >= 0) return { seance: i, bloc: j, seanceCours: seances[i], blocCours: b, derniereDuBloc: k === b.slide_ids.length - 1, dernierBlocDeLaSeance: j === seances[i].blocs.length - 1 };
    }
  }
  return null;
}

/**
 * Les réactions préparées d'une question du cycle. Rappel : `competences[].rappels[].reponses` ; exercice de bloc :
 * `seances[].blocs[].exercice.reponses` (vrai/faux : `statements[j].reponses`) ; un exercice qui `reprend` celui d'une
 * diapositive (`<slide>/e<i>`) lit celles de la diapositive (`concentration.reponses['e<i>']`, `e<i>s<j>`).
 */
export function reactionsDe(deck: CourseDeck | null | undefined, q: QuestionMemoire, j?: number): ReponsesPreparees | undefined {
  const propres = j === undefined ? q.reponses : q.statements?.[j]?.reponses;
  if (propres && Object.keys(propres).length) return propres;
  const m = /^(.+)\/(e\d+)$/.exec(q.reprend || '');
  if (!m || !deck) return undefined;
  const slide = deck.activities.flatMap(a => a.slides).find(s => s.id === m[1]);
  return slide?.concentration?.reponses?.[j === undefined ? m[2] : `${m[2]}s${j}`];
}
