import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import AIAvatar, { useColonneTuteur, type LabControlCommand } from '../session/AIAvatar';
import { observeAvatarMedia } from '../../services/avatarAudio';
import { audioUnlock } from '../../services/audioUnlock';
import type { ProfessorEmotionKind } from '../../services/professorEmotion';
import { focusProfessor } from '../../services/professorFocus';
import type { CourseSlide, Demonstration, EnonceLu, QuestionObservation, ReactionPreparee, SlideConcentration } from './types';
import ClavierScientifique, { BoutonSymboles } from './ClavierScientifique';
import { clavier, hauteurClavierTelephone, largeurClavier, useChampClavier, useClavier } from './ClavierFlottant';
import { Formule } from './Formule';
import DemonstrationPleine, { type LectureDemo } from './DemonstrationPleine';
import type { EnteteCahier } from './cahier';
import ChampReponse, { BoutonPhoto, type ContexteOcr } from './SaisieReponse';
import SansDefilement from './SansDefilement';
import FiguresCahier from './FigureCahier';
import { inscrireVoix } from './voixUnique';
import { taire as taireMemoire } from './memoire/voix';

/**
 * Le mode CONCENTRATION d'une diapositive (8 novembre 2026, demande de l'utilisateur).
 *
 * L'élève ne lit pas pendant que le professeur parle : il regarde. Au tableau, seulement le titre et le
 * sous-titre ; au centre, l'image ou la simulation (ou le tableau de la diapositive) ; les formules s'écrivent
 * quand la voix les dit. Le tuteur 3D vole vers ce qu'il explique et le montre du doigt, au rythme de la voix
 * (`slide.concentration.pointage`), et lance lui-même la simulation. L'écrit reste à portée, fermé :
 * la bulle « À écrire dans le cahier » (la trace à recopier) et « Explication écrite » (le contenu complet).
 *
 * Après la voix, si l'élève ne touche à rien, le tuteur fait lui-même la variante (`concentration.variante`) :
 * il change un réglage et rejoue, pour montrer la comparaison. Si l'élève manipule lui-même et obtient un
 * nouveau résultat, rien ne s'ouvre (10 novembre 2026) : « 🔎 Ton résultat » clignote en bas du tableau et le cours
 * continue. Au clic seulement, le cours se met en pause, le tuteur interprète le résultat (DeepSeek,
 * `/course-player/sim-reaction`) et DIT tout ce qui s'écrit dans le panneau (l'écrit suit la voix, par morceaux),
 * puis pose une question (QCM, vrai/faux ou directe) dont chaque option a son retour dit ; une fois le retour dit,
 * le panneau se ferme et le cours reprend tout seuls.
 *
 * Une question de calcul ou de raisonnement porte sa démonstration (`question.demonstration`) : après la réaction,
 * le tableau des questions l'écrit à la main, ligne par ligne, au rythme de la voix, puis passe à la suite.
 */

type Langue = 'fr' | 'ar' | 'mixed';

interface Props {
  slide: CourseSlide;
  language: Langue;
  /** ←, ↺, Suivant : posés dans la barre du bas, hors de la scène. */
  deckControls?: ReactNode;
  /** Monte le tuteur 3D (banc local : la page de séance a déjà le sien). */
  tuteur3D?: boolean;
  /** Le cours, pour le suivi des acquis. */
  deckId?: string;
  /** Passer à la diapositive suivante : seulement quand l'élève appuie sur « Suite → » (11 novembre 2026). */
  onSuivant?: () => void;
  /** Le texte du bouton principal (« Suite → », « Terminer ✓ » sur la dernière diapositive). */
  libelleSuite?: string;
  /**
   * Mémoire longue (11 novembre 2026) : cette diapositive termine un bloc pas encore bouclé. « Suite → » ouvre alors la
   * fin du bloc (cahier → retrouver → exercice, `memoire/useMemoireDuCours` dans `CoursePlayer`) au lieu de changer
   * de diapositive : `onFermerBloc`.
   */
  finDeBloc?: boolean;
  onFermerBloc?: () => void;
  /** Chaque réponse jugée (prédictions exclues) : pour détecter la saturation (deux fausses de suite). */
  onReponseJugee?: (r: { correct: boolean | null }) => void;
  /** Le cahier organisé (12 novembre 2026) : titre du cours au premier écran, partie numérotée en y entrant, diapositive numérotée. */
  entete?: EnteteCahier;
}

const premier = <T,>(champ: Record<string, T> | undefined, langue: Langue): T | undefined =>
  champ ? champ[langue] ?? champ.mixed ?? champ.fr ?? Object.values(champ)[0] : undefined;

const CRAIE = "'Patrick Hand', 'Caveat', cursive";

/** Le deuxième tableau descend du haut ; chaque question s'y écrit l'une après l'autre. */
const ANIMATIONS = `
/* Téléphone en paysage (16 novembre 2026) : la hauteur manque ; titre, barre du bas et boutons se font plus petits
   pour laisser la place au tableau, et tout tient dans un seul écran. */
@media (max-height: 520px) and (orientation: landscape) {
  [data-scene-cours] > header { padding-top: 2px; padding-bottom: 0 }
  [data-scene-cours] > header h1 { font-size: 17px; line-height: 1.15 }
  [data-scene-cours] > header p { font-size: 12px; line-height: 1.2 }
  [data-scene-cours] > main { padding-bottom: 2px }
  [data-scene-cours] [data-pied-cours] { padding-top: 3px; padding-bottom: 3px; gap: 4px; flex-wrap: nowrap }
  [data-scene-cours] [data-pied-cours] button { height: 30px; font-size: 13px }
  [data-scene-cours] [data-pied-cours] button.w-9, [data-scene-cours] [data-pied-cours] .w-9 { width: 30px }
  [data-scene-cours] [data-pied-cours] button[data-suite] { height: 32px; padding-left: 14px; padding-right: 14px; font-size: 14px }
  [data-scene-cours] [data-pied-cours] .px-3 { padding-left: 9px; padding-right: 9px }
  /* le tableau des questions : énoncé et choix plus serrés, les choix d'un QCM sur deux colonnes, tout sans défiler */
  [data-scene-cours]:has(.tableau-questions) > header { display: none }   /* le titre se cache, les questions prennent sa hauteur */
  .tableau-questions > div:first-child { padding-top: 1px; padding-bottom: 1px }
  .tableau-questions > div:first-child .text-base { font-size: 13px }
  .tableau-questions .p-4, .tableau-questions .p-5 { padding: 5px 9px }
  /* la taille suit la hauteur de l'écran : serrée à 266 px (barre du navigateur), plus grande quand la place existe */
  .tableau-questions .text-xl { font-size: clamp(15px, 5vh, 21px); line-height: 1.25 }
  .tableau-questions .text-lg { font-size: clamp(13.5px, 4.6vh, 20px); line-height: 1.25 }
  .tableau-questions .text-base { font-size: 14px }
  .tableau-questions [data-choix] { margin-top: 4px }
  .tableau-questions [data-choix='qcm'] { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(4px, 1.6vh, 8px) }
  .tableau-questions [data-choix='qcm'] > * { margin-top: 0 !important }
  .tableau-questions [data-choix] > button { padding-top: clamp(3px, 1.8vh, 12px); padding-bottom: clamp(3px, 1.8vh, 12px) }
  .tableau-questions .mt-3 { margin-top: 6px }
  .tableau-questions .mt-2 { margin-top: 4px }
  /* les bulles (cahier, explication, question de l'élève) : toute la hauteur du tableau, texte à la taille de l'écran */
  [data-scene-cours] [data-bulle] { top: 4px; bottom: 44px; max-height: none; padding: 10px 14px }
  [data-scene-cours] [data-bulle] .text-2xl { font-size: 18px; line-height: 1.3 }
  [data-scene-cours] [data-bulle] .text-xl { font-size: 16px; line-height: 1.3 }
  [data-scene-cours] [data-bulle] .text-lg { font-size: 14px; line-height: 1.35 }
  [data-scene-cours] [data-bulle] .mt-3 { margin-top: 6px }
  /* la question d'observation, sous la figure : une bande fine, pour laisser la hauteur à la figure */
  [data-scene-cours] [data-observation] { padding: 3px 10px }
  [data-scene-cours] [data-observation] p { font-size: 14px; line-height: 1.25 }
  [data-scene-cours] [data-observation] button { padding-top: 4px; padding-bottom: 4px; font-size: 13px }
  [data-scene-cours] [data-bulle] textarea { min-height: 0; height: 40px; padding-top: 6px; padding-bottom: 6px }
  [data-scene-cours] [data-bulle] .py-2 { padding-top: 3px; padding-bottom: 3px }
  [data-scene-cours] [data-bulle] .mt-2 { margin-top: 4px }
  [data-scene-cours] [data-bulle] .gap-3 { gap: 6px }
}
@keyframes tableau-descend { from { transform: translateY(-108%); opacity: .5 } 60% { transform: translateY(1.5%) } to { transform: none; opacity: 1 } }
@keyframes question-apparait { from { opacity: 0; transform: translateY(-10px) } to { opacity: 1; transform: none } }
.tableau-questions { animation: tableau-descend .7s cubic-bezier(.2,.8,.2,1) both }
.question-apparait { opacity: 0; animation: question-apparait .45s ease-out both }
@keyframes craie-ecrit { from { clip-path: inset(0 100% 0 0) } to { clip-path: inset(0 0 0 0) } }
.craie-ecrit { animation: craie-ecrit 1.4s steps(28) both }
@keyframes brosse-g { from { clip-path: inset(0 100% 0 0) } to { clip-path: inset(0 0 0 0) } }
@keyframes brosse-d { from { clip-path: inset(0 0 0 100%) } to { clip-path: inset(0 0 0 0) } }
@keyframes brosse-trajet {
  0% { left: -6%; top: 6% } 31% { left: 90%; top: 9% } 34% { left: 90%; top: 40% } 64% { left: -6%; top: 42% }
  67% { left: -6%; top: 74% } 100% { left: 90%; top: 76% } }
@keyframes brosse-frotte { 0%, 100% { transform: rotate(-8deg) translateY(0) } 50% { transform: rotate(7deg) translateY(6px) } }
.brosse { position: absolute; width: 112px; height: 50px; animation: brosse-trajet ${3.4}s linear both; z-index: 3 }
.brosse > div { animation: brosse-frotte .26s ease-in-out infinite }
@keyframes poussiere { from { opacity: .55 } to { opacity: 0 } }
@keyframes reflexion-remplit { from { width: 0 } to { width: 100% } }
.reflexion-barre { animation-name: reflexion-remplit; animation-timing-function: linear; animation-fill-mode: both }
`;

/** Les phrases préenregistrées des questions libres (voix du cours) : elles partent sans attente ni GPU. */
const CLIPS = {
  effacer: '/media/audio/reactions/tableau-effacer.mp3',
  suivante: '/media/audio/reactions/notion-plus-tard.mp3',
  hors_cours: '/media/audio/reactions/hors-cours.mp3',
  verifier: '/media/audio/reactions/verifier-compris.mp3',
  merci: '/media/audio/reactions/social-merci.mp3',
  ok: '/media/audio/reactions/social-ok.mp3',
  salut: '/media/audio/reactions/social-salut.mp3',
} as const;
/** Dites à l'instant où une vraie question part : l'élève n'attend jamais dans le silence. */
const CLIPS_QUESTION = ['/media/audio/reactions/q-ma-1.mp3', '/media/audio/reactions/q-ma-7.mp3'];
/** Dites au clic sur « 🔎 Ton résultat » (« إيه، نشوفو هادشي مع بعض. », « واخا، يلاه نشوفو. ») pendant que le LLM regarde. */
const CLIPS_RESULTAT = ['/media/audio/reactions/q-ma-4.mp3', '/media/audio/reactions/q-ma-8.mp3'];

const DEMANDE = /[?؟]|\b(comment|pourquoi|qu['’ ]?est|c['’ ]?est quoi|explique|expliquer|réexplique|peux[- ]tu|quelle?s?|quand|combien|où|donne|montre|calcule)\b|كيفاش|علاش|شنو|اشنو|أشنو|واش|فين|شحال|اشرح|شرح|عاود|kifach|3lach|chno|wach|3awe?d|chra7|fhemni/i;
const NEGATION = /\b(pas|non|rien|aucun|ma ?fhemt|mafhemtch)\b|ما ?فهمت|مافهمت|ماشي|لا\b/i;
const MERCI = /\b(merci|thanks?|thank you|chokran|choukran|chukran)\b|شكرا|شكراً|بارك الله|يعطيك الصحة|الله يحفظك/i;
const SALUT = /^(salut|bonjour|bonsoir|salam|slm|hello|hi|السلام|سلام|اهلا|أهلا|مرحبا)/i;
const ACCORD = /\b(ok|okay|oki|d['’ ]?accord|dacc|compris|c['’ ]?est bon|bien|parfait|super|clair|mzyan|mzian|mezyan|mziane|wakha|wa5a|safi|fhemt|fhamt|oui|on continue|continue|suivant)\b|مزيان|واخا|صافي|فهمت|مفهوم|زوين|تمام|واضح|نكملو|كمل/i;
/**
 * Une conversation normale (9 novembre 2026) : « merci », « مزيان », « d'accord », « bonjour » ne sont pas des
 * demandes d'explication. Reconnus ici, sans serveur : la réponse est une phrase préenregistrée, instantanée.
 */
function motSocial(texte: string): 'merci' | 'ok' | 'salut' | null {
  const t = texte.trim();
  if (!t || t.split(/\s+/).length > 6 || DEMANDE.test(t) || NEGATION.test(t)) return null;
  if (MERCI.test(t)) return 'merci';
  if (SALUT.test(t)) return 'salut';
  if (ACCORD.test(t)) return 'ok';
  return null;
}
/** La parole coupée en morceaux : une première phrase courte (elle part vite), puis des groupes de phrases. */
function decouperParole(texte: string): string[] {
  const phrases = (texte.match(/[^.!?؟…]+[.!?؟…]*/g) || [texte]).map(x => x.trim()).filter(Boolean);
  const out: string[] = [];
  let courant = '';
  for (const ph of phrases) {
    // Le premier morceau reste court (premier son en ~3 s) mais jamais minuscule ; les suivants grandissent :
    // chacun est prêt avant que le précédent ait fini d'être dit (deux cartes calculent en parallèle).
    const limite = [70, 120][out.length] ?? 170;
    if (courant.length >= 25 && courant.length + ph.length > limite) { out.push(courant); courant = ph; }
    else courant = courant ? `${courant} ${ph}` : ph;
  }
  if (courant) out.push(courant);
  return out;
}
/** Durée du coup de brosse (ms) : le temps de préparer l'explication et sa voix. */
const BROSSE_MS = 3400;
const attendre = (ms: number) => new Promise<void>(ok => window.setTimeout(ok, ms));

/** Le petit exercice qui suit l'explication au tableau : il vérifie ce que l'élève a compris. */
type Exercice = {
  type: 'qcm' | 'vrai_faux' | 'association'; enonce: string; explication: string; parole_juste: string; parole_faux: string;
  choix?: string[]; bonne?: number; affirmations?: { texte: string; vrai: boolean }[]; paires?: { gauche: string; droite: string }[];
};
type ReponseLibre = {
  categorie: 'diapo' | 'suivante' | 'prerequis' | 'hors_cours' | 'conversation'; notion: string; diapo_suivante: { id: string; title: string } | null;
  parole: string; ecrit: string; tableau: string[]; question_comprise: string;
  gestes: { commande?: string; parametres?: Record<string, unknown>; repere?: string }[]; exercice?: Exercice | null;
};
/** Le tableau du professeur : il y explique la question à la voix ; le texte n'est montré qu'à la demande. */
type TableauProf = {
  mode: 'diapo' | 'efface'; etape: 'brosse' | 'prepare' | 'ecrit' | 'exercice'; lignes: string[]; vues: number; parole: string; ecrit: string;
  notion: string; question: string; texte: boolean; debut: number; erreur?: string; exercice?: Exercice | null;
};

/** Durée du vol du tuteur jusqu'au bouton (s), mesurée : la commande arrive ~0,9 s après le geste. */
const AVANCE_COMMANDE = 0.9;

/** Le retour d'UNE option de la question sur le résultat : écrit sous l'option, dit quand l'élève la choisit. */
type Retour = { ecrit: string; parole: string };
type QuestionSim = {
  type: 'qcm' | 'vrai_faux' | 'directe'; enonce: string; explication?: string;
  /** QCM : un retour par choix, dans l'ordre de `choix`. Vrai/faux : `affirmations[i].retours` = [si Vrai, si Faux]. */
  choix?: string[]; bonne?: number; retours?: Retour[];
  affirmations?: { texte: string; vrai: boolean; retours?: Retour[] }[]; attendu?: string;
  parole_juste?: string; parole_faux?: string;
};
/**
 * Le panneau « Ton résultat ». `voix` : `prepare` (le LLM a répondu, la voix se calcule), `parle` (l'écrit suit la
 * voix : `nParole` morceaux pour l'interprétation, puis ceux de la question lue), `sansvoix` (l'écrit se dévoile au
 * temps de lecture), `fini` (tout est dit : l'élève répond).
 */
type Reaction =
  | { phase: 'reflechit' }
  | { phase: 'question'; ecrit: string; phrases: string[]; question: QuestionSim; voix: 'prepare' | 'parle' | 'sansvoix' | 'fini';
      nParole: number; nTotal: number; debut: number; pris?: number; vf?: Record<number, boolean>; retoursVf?: Record<number, Retour>;
      verdict?: { correct: boolean; ecrit: string } }
  | { phase: 'erreur'; message: string };
/** La voix d'une démonstration sans piste, calculée d'avance (pendant que la réaction est dite) : ses morceaux. */
type VoixDemo = { textes: string[]; urls: Promise<string | null>[] };
/** L'écrit d'une interprétation, coupé en phrases : elles apparaissent au fil de la voix. */
function phrasesEcrites(texte: string): string[] {
  return (texte.match(/[^.!?…]+(?:[.!?…]+|$)/g) || []).map(x => x.trim()).filter(Boolean);
}
type EtatSim = Record<string, unknown> & { simulation_status?: string; derniere_main?: string; parameters?: unknown; moments?: Record<string, number> };
/** Une reprise (cycle 1 à 3) : ce que le tuteur dit et fait, puis la question jumelle. */
type Reprise = {
  cycle: number; parole: string; ecrit: string; dernier: boolean; reponse_finale?: string; cahier?: string;
  gestes: { commande?: string; parametres?: Record<string, unknown>; repere?: string }[];
  question: QuestionSim;
};
type Cycle = { n: number; phase: 'attente' | 'explique' | 'question' | 'final'; data?: Reprise; depuis: QuestionDiapo };
const MAX_CYCLES = 3;

// ── Le rythme appartient à l'élève (11 novembre 2026, skill cours-concentration « Memory and rhythm ») ──
/** Temps de réflexion avant que les choix d'une question s'affichent (« 🤔 Réfléchis d'abord… »). */
const REFLEXION_MS = 10_000;
/** Un vrai/faux se lit plus vite : ses deux choix arrivent plus tôt. */
const REFLEXION_VRAI_FAUX_MS = 6_000;
/** Silence (sans action de l'élève) au bout duquel le tuteur relance doucement, une seule fois, quand « Suite → » attend. */
const RELANCE_APRES_MS = 45_000;
/** Un schéma à légender : le temps laissé à l'élève sans qu'il touche à rien avant que le tuteur pose les étiquettes. */
const LEGENDE_AIDE_MS = 60_000;
/** La phrase de relance préenregistrée (voix du cours). Absente du dossier : le bouton « Suite → » clignote seulement. */
const CLIP_RELANCE = '/media/audio/reactions/relance-suite.mp3';
/**
 * Ce que fait « Suite → » à cet instant — le SEUL bouton qui fait avancer le cours (plus rien ne passe tout seul) :
 * `voix` (après la prédiction, la voix d'explication part), `ouvrir` (rouvrir le tableau des questions),
 * `question` (la question suivante non répondue), `jumelle` (couper la reprise, la question jumelle), `reprise`
 * (lancer le cycle de reprise suivant), `diapo` (la diapositive suivante), `rien` (le tuteur prépare : on attend).
 * `pret` : l'étape en cours est terminée, le bouton est mis en avant et la relance peut venir.
 */
type EtapeSuite = { quoi: 'voix' | 'ouvrir' | 'question' | 'jumelle' | 'reprise' | 'diapo' | 'bloc' | 'rien'; pret: boolean };
/**
 * La question d'observation en cours (14 novembre 2026) : `observe` (silence, l'élève regarde ; indices puis cartes),
 * `ecoute` (il maintient le micro de réponse), `transcrit`, `juge` (le serveur juge sa réponse dite), `fini` (le retour
 * est dit, la voix du cours va reprendre).
 */
type EtatObservation = {
  etape: 'observe' | 'ecoute' | 'transcrit' | 'juge' | 'fini';
  indices: number; cartes: boolean; exclus: number[]; essai: number;
  /** la carte montrée juste (bonne réponse trouvée, ou montrée après la deuxième erreur) */
  bonneMontree?: boolean;
  entendu?: string; verdict?: { correct: boolean | null; ecrit: string }; erreur?: string;
};
/** Silence d'observation par défaut avant chaque aide (indice, puis cartes). */
const SILENCE_OBSERVATION_S = 8;
/** Une phrase préenregistrée existe-t-elle vraiment ? (le serveur de dev renvoie la page HTML pour un fichier absent) */
async function clipExiste(url: string): Promise<boolean> {
  try {
    const r = await fetch(url, { method: 'HEAD' });
    return r.ok && (r.headers.get('content-type') || '').startsWith('audio');
  } catch { return false; }
}

const jeton = () => { try { return localStorage.getItem('token') || ''; } catch { return ''; } };
/** Le bilan des acquis de l'élève sur ce cours (GET /course-player/acquis/{deck}), tel que le serveur le rend. */
type Bilan = {
  competences: { id: string; label: string; dit?: string; statut: string }[];
  lacunes: { id: string; label: string; dit?: string; statut: string; reprendre_avec: string[] }[];
};
async function lireApi<T>(chemin: string): Promise<T> {
  const r = await fetch(`/api/v1${chemin}`, { headers: { Authorization: `Bearer ${jeton()}` } });
  if (!r.ok) throw new Error(`${r.status}`);
  return r.json() as Promise<T>;
}
/** Ce que le tuteur dit des lacunes à la fin du bilan : darija simple, termes du cours en français (règles de la voix). */
function phraseDesLacunes(b: Bilan): string {
  const evaluees = b.competences.filter(c => c.statut !== 'non_evalue');
  if (!evaluees.length) return '';
  if (!b.lacunes.length) return 'مزيان بزاف. كلشي اللي جاوبتي عليه فهاد الدرس كان صحيح، les compétences ديالك مكتسبة. نكملو.';
  const noms = b.lacunes.slice(0, 3).map(l => l.dit || l.label).join('، ');
  const avec = b.lacunes[0].reprendre_avec?.[0] || 'une simulation que tu manipules toi-même';
  return `شوف، باقي ليك شي حاجة باش تراجع: ${noms}. ماشي مشكل، غادي نعاودوها معا بعضياتنا فle mode libre، ب ${avec}، حتى تولي عندك مكتسبة.`;
}
async function appelerApi<T>(chemin: string, corps: unknown): Promise<T> {
  const r = await fetch(`/api/v1${chemin}`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton()}` }, body: JSON.stringify(corps) });
  if (!r.ok) {
    // Le serveur dit pourquoi (micro qui se prépare, trop de demandes…) : c'est ce que l'élève lit.
    const detail = await r.json().then((d: { detail?: unknown }) => (typeof d?.detail === 'string' ? d.detail : '')).catch(() => '');
    throw new Error(detail || `${r.status}`);
  }
  return r.json() as Promise<T>;
}

export default function CourseFocusStage({ slide, language, deckControls, tuteur3D = false, deckId, onSuivant, libelleSuite = 'Suite →', finDeBloc = false, onFermerBloc, onReponseJugee, entete }: Props) {
  const parole = (premier(slide.speech_text, language) || '').trim();
  const piste = premier(slide.audio, language);
  const conc = slide.concentration || {};
  const contenu = slide.screen_content || {};
  const visuel = slide.visual && slide.visual.kind !== 'none' ? slide.visual : null;
  const table = contenu.table?.headers?.length && contenu.table.rows?.length ? contenu.table : null;

  const audioRef = useRef<HTMLAudioElement>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const visuelRef = useRef<HTMLDivElement>(null);
  const lignesRef = useRef<(HTMLTableRowElement | null)[]>([]);
  const centreRef = useRef<(HTMLDivElement | null)[]>([]);

  const [temps, setTemps] = useState(0);
  const [duree, setDuree] = useState((piste?.duration_ms || 0) / 1000);
  const [enLecture, setEnLecture] = useState(false);
  const [finie, setFinie] = useState(!piste?.url);
  const [panneau, setPanneau] = useState<'cahier' | 'explication' | 'exercices' | 'questions' | 'question_eleve' | null>(null);
  const [labControl, setLabControl] = useState<LabControlCommand | null>(null);
  const [simPrete, setSimPrete] = useState(false);
  const sequence = useRef(0);
  const prochainGeste = useRef(0);
  const gestesEnAttente = useRef<number[]>([]);
  const dejaFaits = useRef<Set<number>>(new Set());
  const demarree = useRef(false);
  // ── L'élève manipule lui-même : le tuteur interprète, parle et pose une question ──
  const voixRef = useRef<HTMLAudioElement>(null);
  const [voixParle, setVoixParle] = useState(false);
  // Le tuteur réagit à chaque réponse avec son corps : bravo, encouragement, doute, surprise.
  const [emotion, setEmotion] = useState<{ kind: ProfessorEmotionKind; key: number } | null>(null);
  const ressentir = useCallback((kind: ProfessorEmotionKind) => setEmotion({ kind, key: Date.now() }), []);
  const [reaction, setReaction] = useState<Reaction | null>(null);
  const reactionRef = useRef<Reaction | null>(null);
  reactionRef.current = reaction;
  const dernierEtat = useRef<EtatSim | null>(null);
  const dernierResultat = useRef<EtatSim | null>(null);
  const historique = useRef<{ type: string; correct: boolean }[]>([]);
  /** Le dernier résultat que l'élève a obtenu lui-même : le bouton « 🔎 Ton résultat » clignote, rien ne s'ouvre. */
  const [resultat, setResultat] = useState<{ avant: EtatSim | null; apres: EtatSim } | null>(null);
  const resultatRef = useRef(resultat);
  resultatRef.current = resultat;
  const tourResultat = useRef(0);
  /** Le panneau ouvert avant « Ton résultat » (les questions) : il revient quand le résultat se ferme. */
  const panneauAvant = useRef<string | null>(null);
  /** Les retours dits l'un après l'autre (vrai/faux : une affirmation après l'autre). */
  const fileRetours = useRef<Promise<void>>(Promise.resolve());
  const tourDemo = useRef(0);
  const coursEnPause = useRef(false);
  const eleveATouche = useRef(false);
  const varianteFaite = useRef(false);
  /**
   * Le schéma à légender de la diapositive (15 novembre 2026) : la simulation dit combien d'étiquettes sont à poser
   * (`legende_total`), combien l'élève en a bien posé, ses erreurs et lesquelles. Tant qu'il n'est pas fini, les
   * questions attendent (elles ne recouvrent plus le schéma) et le tuteur ne pose pas les étiquettes à sa place.
   */
  const legendeRef = useRef<{ total: number; places: number; erreurs: number; mal: string; close: boolean } | null>(null);
  const finirLegendeRef = useRef<(abandon: boolean) => void>(() => {});
  /** Le commentaire écrit du tuteur sur le schéma légendé, sous le tableau. */
  const [legendeMot, setLegendeMot] = useState<{ texte: string; correct: boolean | null } | null>(null);
  /** le schéma à légender attend encore l'élève */
  const legendeEnCours = () => !!legendeRef.current && !legendeRef.current.close;
  // ── La question libre de l'élève : écrite, au micro ou en image ; le tuteur répond sans quitter la diapositive ──
  type QuestionLibre = { phase: 'saisie' | 'envoi' | 'reponse'; texte: string; image?: { b64: string; mime: string; nom: string }; audio?: string; enregistre: boolean;
    /** La transcription du micro est en cours : elle va s'écrire dans le champ, pour que l'élève la vérifie. */
    transcrit?: boolean; aVerifier?: boolean;
    reponse?: ReponseLibre; erreur?: string };
  const [libre, setLibre] = useState<QuestionLibre>({ phase: 'saisie', texte: '', enregistre: false });
  const champQuestion = useRef<HTMLTextAreaElement>(null);
  // Sur téléphone, la bulle de la question et le panneau du résultat prennent toute la largeur : le champ et le
  // clavier scientifique y restent utilisables (la colonne du tuteur leur laisserait 140 px à 375 px).
  const [etroit, setEtroit] = useState(() => typeof window !== 'undefined' && window.innerWidth < 640);
  // la colonne de droite laissée au tuteur 3D : plus étroite sur téléphone en paysage, où il rétrécit
  const COLONNE_TUTEUR = useColonneTuteur();
  useEffect(() => {
    const suivre = () => setEtroit(window.innerWidth < 640);
    window.addEventListener('resize', suivre);
    return () => window.removeEventListener('resize', suivre);
  }, []);
  const [clavierQuestion, setClavierQuestion] = useState(false);
  // Le clavier flottant (12 novembre 2026) : à droite ; le tableau des questions lui laisse sa place.
  const clavierEtat = useClavier();
  const placeClavier = largeurClavier(clavierEtat.ouvert);
  /** sur téléphone le clavier est en bas : le tableau des questions remonte au-dessus de lui (la barre du bas est dessous) */
  const piedRef = useRef<HTMLElement>(null);
  const basClavier = Math.max(0, hauteurClavierTelephone(clavierEtat.ouvert) - (piedRef.current?.offsetHeight || 0));
  const toucherQuestion = useChampClavier(champQuestion, libre.texte, v => setLibre(l => ({ ...l, texte: v })),
    { actif: clavierEtat.hotes > 0 && panneau === 'question_eleve' && libre.phase === 'saisie' });
  // La réponse ne s'écrit pas en texte : le tuteur l'explique au tableau (9 novembre 2026).
  const [tableauProf, setTableauProf] = useState<TableauProf | null>(null);
  const tableauRef = useRef<TableauProf | null>(null);
  tableauRef.current = tableauProf;
  const lignesProfRef = useRef<(HTMLParagraphElement | null)[]>([]);
  const [annonce, setAnnonce] = useState<{ mode: 'suivante' | 'hors_cours'; notion: string; titre?: string } | null>(null);
  const [horloge, setHorloge] = useState(0);
  const tourQuestion = useRef(0);
  /** La voix qui joue est celle de l'explication au tableau : quand elle finit, l'exercice arrive. */
  const voixExplication = useRef(false);
  /** L'explication est dite par morceaux : la suite attend ici pendant que le premier morceau joue. */
  const fileVoix = useRef<Promise<string | null>[]>([]);
  const morceaux = useRef({ total: 1, joues: 0 });
  /** Ce qui suit le dernier morceau (l'exercice, la question du résultat, la fin d'une démonstration). */
  const finMorceaux = useRef<{ encore: () => boolean; fin: () => void } | null>(null);
  const derniereImage = useRef(0);
  const enregistreur = useRef<MediaRecorder | null>(null);
  const morceauxAudio = useRef<Blob[]>([]);
  // ── Le cycle de reprise : faux → le tuteur réexplique autrement, puis question jumelle ; 3 cycles au plus ──
  const [cycle, setCycle] = useState<Cycle | null>(null);
  const cycleRef = useRef<Cycle | null>(null);
  cycleRef.current = cycle;
  /** Les questions closes : juste (true), fausse (false) ou passée par l'élève ('passee' : ni erreur ni reprise). */
  const finies = useRef<Record<string, boolean | 'passee'>>({});
  const fausses = useRef<Record<string, string[]>>({});
  const reperesRef = useRef<Record<string, string>>({});
  // ── La diapositive du bilan : le lecteur va chercher les acquis de l'élève et les donne à la simulation ──
  const [bilan, setBilan] = useState<Bilan | null>(null);
  const bilanRef = useRef<Bilan | null>(null);
  bilanRef.current = bilan;
  const lacunesDites = useRef(false);
  const voixLancee = useRef(false);
  const diapoRef = useRef({ id: slide.id, title: slide.title });
  diapoRef.current = { id: slide.id, title: slide.title };
  // ── La question d'observation (14 novembre 2026) : le tuteur s'arrête, pose la question et laisse l'élève regarder ──
  const observation: QuestionObservation | null = conc.observation?.enonce && (conc.observation.choix || []).length >= 2 ? conc.observation : null;
  const [obs, setObs] = useState<EtatObservation | null>(null);
  const obsRef = useRef<EtatObservation | null>(null);
  obsRef.current = obs;
  /** La question d'observation de cette diapositive est close (répondue ou passée) : la variante et les questions peuvent venir. */
  const [obsClose, setObsClose] = useState(false);
  const obsFaite = useRef(false);
  /** La voix du cours a été arrêtée par la question : elle reprend quand la question se ferme. */
  const obsPause = useRef(false);
  const tourObs = useRef(0);
  const obsAppui = useRef(false);
  const obsRec = useRef<MediaRecorder | null>(null);
  const obsDebut = useRef(0);
  const obsLimite = useRef<number | undefined>(undefined);

  /** L'instant d'un mot : sa place dans le texte parlé, rapportée à la durée de la piste. */
  const instant = useCallback((mot: string) => {
    const i = parole.indexOf(mot);
    if (i < 0 || !duree) return 0;
    return Math.max(0, (i / Math.max(1, parole.length)) * duree - 0.3);
  }, [parole, duree]);

  const pointage = useMemo(
    // Une commande part un peu avant le mot : le temps que la main du tuteur atteigne le bouton.
    () => (conc.pointage || []).map(p => ({ ...p, t: Math.max(0, instant(p.mot) - (p.commande ? AVANCE_COMMANDE : 0)) })),
    [conc.pointage, instant],
  );
  const centre = useMemo(
    () => (conc.centre || []).map(c => ({ ...c, t: instant(c.mot) })),
    [conc.centre, instant],
  );

  // ── Prévoir d'abord (11 novembre 2026) : la question `prediction` est posée AVANT la voix, puis la voix montre ──
  const prediction = useMemo(() => questionDePrediction(slide), [slide]);
  /** La mémoire des réponses de cette diapositive (même clé que chaque question : `reponse:<deck>:<diapo>:<cle>`). */
  const memoireDiapo = `${deckId || ''}:${slide.id}`;
  /** Déjà prédite (réponse retrouvée) : la voix part tout de suite, comme une diapositive ordinaire. */
  const predictionDejaFaite = useMemo(
    () => !!prediction && estTerminee(prediction.type, lireEtatQuestion(`reponse:${memoireDiapo}:${prediction.cle}`), 2),
    [prediction, memoireDiapo],
  );
  /** La diapositive dont la prédiction est close (l'élève a appuyé sur « Suite → ») : sa voix peut partir. */
  const [predictionClose, setPredictionClose] = useState<string | null>(null);
  /** La diapositive dont la question de prédiction vient d'être répondue (réaction dite) : « Suite → » est prêt. */
  const [predictionRepondue, setPredictionRepondue] = useState<string | null>(null);
  const predictionEnCours = !!prediction && !predictionDejaFaite && predictionClose !== slide.id;
  /** Les questions APRÈS la voix : celles de la diapositive, sans la prédiction (elle n'est pas reposée). */
  const questions = useMemo(
    () => questionsDeLaDiapo(slide).filter(q => !(estPrediction(slide) && q.cle === 'q')),
    [slide],
  );
  /** La question montrée par le carrousel du tableau (elle ne change que par l'élève : « Suite → », points, flèches). */
  const [indexQuestion, setIndexQuestion] = useState(0);
  /** Les questions finies changent : l'écran recalcule ce que fait « Suite → ». */
  const [, setVersionFinies] = useState(0);
  /** « Suite → » clignote : la relance douce après un long silence (une fois par diapositive). */
  const [relance, setRelance] = useState(false);
  const relanceFaite = useRef(false);
  /** Ce que le tableau des questions affiche : les questions de la diapositive, ou la question jumelle du cycle. */
  const jumelles = useMemo<{ questions: QuestionDiapo[]; preparees: SlideConcentration['reponses'] }>(() => {
    const q = cycle?.data?.question;
    if (!cycle || cycle.phase !== 'question' || !q) return { questions: [], preparees: undefined };
    const n = cycle.n, prep: NonNullable<SlideConcentration['reponses']> = {};
    const juste = { parole: q.parole_juste || '', ecrit: q.explication || '' }, faux = { parole: q.parole_faux || '', ecrit: q.explication || '' };
    if (q.type === 'qcm' && q.choix) {
      const cle = `cycle${n}`;
      prep[cle] = Object.fromEntries(q.choix.map((_, i) => [String(i), i === q.bonne ? { juste } : { '1': faux, '2': faux }]));
      return { questions: [{ cle, type: 'qcm', enonce: q.enonce, choix: q.choix, bonne: q.bonne, explication: q.explication }], preparees: prep };
    }
    const liste = (q.affirmations || []).map((a, j) => {
      const cle = `cycle${n}s${j}`;
      prep[cle] = { '0': a.vrai ? { juste } : { '1': faux, '2': faux }, '1': a.vrai ? { '1': faux, '2': faux } : { juste } };
      return { cle, type: 'vrai_faux' as const, enonce: a.texte, choix: ['Vrai', 'Faux'], bonne: a.vrai ? 0 : 1, explication: q.explication };
    });
    return { questions: liste, preparees: prep };
  }, [cycle]);
  const enReprise = !!cycle && cycle.phase === 'question';
  const jumellesRef = useRef(jumelles.questions);
  jumellesRef.current = jumelles.questions;

  // Nouvelle diapositive : tout repart de zéro.
  useEffect(() => {
    // Une prédiction à faire : le tableau des questions est là d'emblée, la voix attend.
    setTemps(0); setEnLecture(false); setFinie(!piste?.url); setPanneau(predictionEnCours ? 'questions' : null); setSimPrete(false);
    setIndexQuestion(0); setRelance(false); relanceFaite.current = false;
    setDuree((piste?.duration_ms || 0) / 1000);
    dejaFaits.current = new Set(); demarree.current = false;
    setReaction(null); dernierEtat.current = null; dernierResultat.current = null; historique.current = [];
    setResultat(null); tourResultat.current += 1; tourDemo.current += 1; panneauAvant.current = null;
    coursEnPause.current = false; eleveATouche.current = false; varianteFaite.current = false; setLegendeMot(null);
    // un schéma à légender déclaré dans le cours attend l'élève dès le départ (la simulation donne ensuite son total)
    legendeRef.current = slide.concentration?.legende ? { total: 0, places: 0, erreurs: 0, mal: '', close: false } : null;
    setCycle(null); finies.current = {}; fausses.current = {}; voixLancee.current = false;
    setLibre({ phase: 'saisie', texte: '', enregistre: false });
    setTableauProf(null); setAnnonce(null); tourQuestion.current += 1;
    setObs(null); setObsClose(false); obsFaite.current = false; obsPause.current = false; tourObs.current += 1;
    obsAppui.current = false; if (obsRec.current?.state === 'recording') obsRec.current.stop();
  // eslint-disable-next-line react-hooks/exhaustive-deps -- `predictionEnCours` est lu au changement de diapositive seulement
  }, [slide.id, piste?.url, piste?.duration_ms]);

  // L'élève passe lui-même à une autre diapositive au milieu d'une reprise : la compétence reste NON ACQUISE,
  // pour que le mode libre et le cours suivant la reprennent (le passage est noté comme une réponse manquée).
  useEffect(() => () => {
    const c = cycleRef.current;
    if (!c || c.phase === 'final') return;
    const d = diapoRef.current;
    void appelerApi('/course-player/acquis', {
      slide_id: d.id, slide_title: d.title, deck_id: deckId, cle: `cycle${c.n}_abandon`, type: c.depuis.type, enonce: c.depuis.enonce,
      reponse: 'passage manuel à une autre diapositive', tentative: 1, correct: false, reaction_preparee: false,
      methodes: { visuel: 'reprise', reexplication: c.n, exercice: false },
    }).catch(() => { /* jamais bloquant */ });
  }, [slide.id, deckId]);

  // Le temps de la voix, lu à chaque image (timeupdate ne passe que 4 fois par seconde).
  useEffect(() => {
    let frame = 0;
    const lire = () => {
      const audio = audioRef.current;
      if (audio) setTemps(audio.currentTime);
      if (tableauRef.current?.etape === 'ecrit' && tableauRef.current.vues < tableauRef.current.lignes.length) setHorloge(performance.now());
      else {
        // L'écrit du panneau « Ton résultat » suit la voix : une dizaine d'images par seconde suffisent.
        const r = reactionRef.current, maintenant = performance.now();
        if (r?.phase === 'question' && (r.voix === 'parle' || r.voix === 'sansvoix') && maintenant - derniereImage.current > 100) {
          derniereImage.current = maintenant; setHorloge(maintenant);
        }
      }
      frame = requestAnimationFrame(lire);
    };
    frame = requestAnimationFrame(lire);
    return () => cancelAnimationFrame(frame);
  }, []);

  const envoyerASim = useCallback((command: string, parameters: Record<string, unknown> = {}) => {
    iframeRef.current?.contentWindow?.postMessage({ type: 'simulation_control', command, parameters }, '*');
  }, []);

  const parTuteur = useCallback((command: string, parameters: Record<string, unknown> = {}) => {
    if (!tuteur3D) { envoyerASim(command, parameters); return; }
    // Un geste à la fois : deux commandes dans la même seconde, la seconde attend que la main soit arrivée.
    const maintenant = performance.now();
    const quand = Math.max(maintenant, prochainGeste.current);
    prochainGeste.current = quand + 1000;
    const partir = () => {
      sequence.current += 1;
      setLabControl({ sequence: sequence.current, command, message: { type: 'simulation_control', command, parameters } });
    };
    if (quand <= maintenant) partir();
    else gestesEnAttente.current.push(window.setTimeout(partir, quand - maintenant));
  }, [envoyerASim, tuteur3D]);

  // Changer de diapositive annule les gestes qui n'ont pas encore eu lieu.
  useEffect(() => () => {
    gestesEnAttente.current.forEach(id => window.clearTimeout(id));
    gestesEnAttente.current = []; prochainGeste.current = 0;
  }, [slide.id]);

  // La diapositive du bilan (`concentration.acquis`) : les acquis de l'élève sont lus au serveur…
  useEffect(() => {
    setBilan(null); lacunesDites.current = false;
    if (!conc.acquis || !deckId) return;
    let actif = true;
    lireApi<Bilan>(`/course-player/acquis/${encodeURIComponent(deckId)}`)
      .then(b => { if (actif && b && Array.isArray(b.competences)) setBilan({ competences: b.competences, lacunes: b.lacunes || [] }); })
      .catch(() => { /* sans bilan, la page de l'élève dit « pas encore de réponses » */ });
    return () => { actif = false; };
  }, [conc.acquis, deckId, slide.id]);
  // …et donnés à la simulation dès qu'elle est prête : elle entoure ce qui est à reprendre, coche ce qui est acquis.
  useEffect(() => {
    if (!bilan || !simPrete) return;
    const acquis = bilan.competences.filter(c => c.statut === 'acquis');
    envoyerASim('set_parameters', { lacunes: bilan.lacunes, acquis: acquis.map(c => c.label), acquis_ids: acquis.map(c => c.id) });
  }, [bilan, simPrete, envoyerASim]);
  /** À la fin de la voix du bilan : le tuteur nomme ce qu'il reste à retravailler et ouvre la page de l'élève. */
  const direLesLacunes = useCallback(() => {
    const b = bilanRef.current;
    if (!b || lacunesDites.current) return;
    lacunesDites.current = true;
    if (dernierEtat.current?.moments && 'lacunes' in dernierEtat.current.moments) parTuteur('play_until', { moment: 'lacunes' });
    const phrase = phraseDesLacunes(b);
    if (!phrase) return;
    ressentir(b.lacunes.length ? 'encourage' : 'celebrate');
    void dire(phrase);
  }, [parTuteur, ressentir]);

  // Le tuteur lance la simulation dès que la voix commence (et que la page a déclaré son protocole).
  useEffect(() => {
    if (!simPrete || !enLecture || demarree.current || !conc.demarrer) return;
    demarree.current = true;
    parTuteur(conc.demarrer);
  }, [simPrete, enLecture, conc.demarrer, parTuteur]);

  // Au rythme de la voix, il montre ce qu'il explique.
  useEffect(() => {
    if (!enLecture) return;
    pointage.forEach((p, i) => {
      if (dejaFaits.current.has(i) || temps < p.t || temps > p.t + 4) return;
      dejaFaits.current.add(i);
      if (p.commande) { parTuteur(p.commande, p.parametres || {}); demarree.current = true; return; }
      if (p.repere) { parTuteur('highlight', { target: p.repere }); return; }
      const [type, n] = (p.cible || 'visuel').split(':');
      const element = type === 'ligne' ? lignesRef.current[Number(n)]
        : type === 'centre' ? centreRef.current[Number(n)]
        : visuelRef.current;
      if (element && tuteur3D) focusProfessor(element);
    });
  }, [temps, enLecture, pointage, parTuteur, tuteur3D]);

  /** La voix du tuteur, générée à l'instant (même voix que le cours). Sans voix, le texte reste affiché. */
  /** La voix d'un texte, calculée d'avance (URL du son) : on la joue quand le tableau est prêt. */
  const preparerVoix = useCallback(async (texte: string): Promise<string | null> => {
    if (!texte.trim()) return null;
    try {
      const r = await fetch('/api/v1/tts/speak', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton()}` },
        body: JSON.stringify({ text: texte, language: 'mixed' }) });
      return r.ok ? URL.createObjectURL(await r.blob()) : null;
    } catch { return null; }
  }, []);
  /** La voix d'un texte long, par morceaux calculés en parallèle : le premier (court) arrive en quelques secondes. */
  const preparerTextes = useCallback((textes: string[]): Promise<string | null>[] => {
    // Deux morceaux à la fois, dans l'ordre (un par carte) : envoyés tous ensemble, ils se gênent et le premier
    // arrive après le dernier (mesuré en ligne : 8,2 s au lieu de 4,9 s pour le premier morceau).
    if (!textes.length) return [Promise.resolve(null)];
    const poser: ((u: string | null) => void)[] = [];
    const urls = textes.map(() => new Promise<string | null>(ok => { poser.push(ok); }));
    let suivant = 0;
    const ouvrier = async () => {
      while (suivant < textes.length) { const i = suivant++; poser[i](await preparerVoix(textes[i])); }
    };
    void ouvrier(); void ouvrier();
    return urls;
  }, [preparerVoix]);
  const preparerMorceaux = useCallback((texte: string) => preparerTextes(decouperParole(texte)), [preparerTextes]);
  const dire = useCallback(async (texte: string): Promise<boolean> => {
    const url = await preparerVoix(texte);
    const voix = voixRef.current;
    if (!url || !voix) return false;   // la voix manque : l'écrit suffit
    voixExplication.current = false;   // une nouvelle parole coupe la suite de morceaux en cours
    try { voix.src = url; await voix.play(); return true; } catch { return false; }
  }, [preparerVoix]);
  /** Une phrase préenregistrée, jouée jusqu'au bout (ou `max` ms au plus) ; false si elle n'a pas pu partir. */
  const jouerEtAttendre = useCallback((url: string, max = 9000) => new Promise<boolean>(ok => {
    const voix = voixRef.current;
    if (!voix) { ok(false); return; }
    let fini = false;
    const fin = (b: boolean) => {
      if (fini) return; fini = true; window.clearTimeout(id);
      voix.removeEventListener('ended', bien); voix.removeEventListener('error', mal); ok(b);
    };
    const bien = () => fin(true), mal = () => fin(false);
    voix.addEventListener('ended', bien); voix.addEventListener('error', mal);
    const id = window.setTimeout(() => fin(true), max);
    voixExplication.current = false;
    voix.src = url; voix.play().catch(() => fin(false));
  }), []);

  /*
   * Une seule voix à la fois, celle de l'écran visible (règle utilisateur, 14 novembre 2026 ; skill
   * cours-concentration « Une seule voix »). La piste de la diapo et la voix du tuteur s'inscrivent : quand la voix du
   * tuteur part (énoncé d'une question, réaction, démonstration…), l'explication se met en pause et reprendra à la
   * fermeture de l'écran ; quand l'explication repart, la voix du tuteur se tait.
   */
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;
    return inscrireVoix(audio, () => { coursEnPause.current = true; if (demarree.current) envoyerASim('pause'); });
  }, [piste?.url, envoyerASim]);
  useEffect(() => {
    const voix = voixRef.current;
    if (!voix) return;
    return inscrireVoix(voix, () => { voixExplication.current = false; fileVoix.current = []; finMorceaux.current = null; });
  }, []);
  /** Un écran fermé par l'élève se tait aussitôt, et l'explication de la diapo reprend là où elle s'était arrêtée. */
  const fermerPanneau = useCallback(() => {
    setPanneau(null);
    ++tourEnonce.current;
    voixExplication.current = false; fileVoix.current = []; finMorceaux.current = null;
    voixRef.current?.pause();
    taireMemoire();
    if (coursEnPause.current) { coursEnPause.current = false; void audioRef.current?.play(); if (demarree.current) envoyerASim('resume'); }
  }, [envoyerASim]);
  /** Une bulle ouvre son écran (et fait taire celui d'avant) ou le referme. */
  const basculerPanneau = useCallback((p: 'cahier' | 'explication' | 'questions') => {
    if (panneau === p) { fermerPanneau(); return; }
    if (panneau) { ++tourEnonce.current; voixExplication.current = false; fileVoix.current = []; voixRef.current?.pause(); taireMemoire(); }
    setPanneau(p);
  }, [panneau, fermerPanneau]);

  /** L'élève lève la main : le cours se met en pause et le panneau de la question s'ouvre. */
  const leverLaMain = useCallback(() => {
    const audio = audioRef.current;
    if (audio && !audio.paused) { audio.pause(); coursEnPause.current = true; if (demarree.current) envoyerASim('pause'); }
    setPanneau(p => p === 'question_eleve' ? null : 'question_eleve');
  }, [envoyerASim]);

  const lireFichier = (f: File) => new Promise<string>((ok, ko) => { const fr = new FileReader(); fr.onload = () => ok(String(fr.result)); fr.onerror = ko; fr.readAsDataURL(f); });

  // Le micro se tient comme un talkie-walkie (9 novembre 2026) : appuyer = il écoute, relâcher = il s'arrête et
  // transcrit. `appuiMicro` dit si le doigt est encore posé (il peut se lever avant que le micro soit ouvert).
  const appuiMicro = useRef(false);
  const debutMicro = useRef(0);
  const limiteMicro = useRef<number | undefined>(undefined);

  const arreterMicro = useCallback(() => {
    appuiMicro.current = false;
    window.clearTimeout(limiteMicro.current);
    if (enregistreur.current?.state === 'recording') enregistreur.current.stop();
  }, []);

  const demarrerMicro = useCallback(async () => {
    if (appuiMicro.current || enregistreur.current?.state === 'recording') return;
    appuiMicro.current = true;
    try {
      const flux = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (!appuiMicro.current) {   // relâché pendant l'ouverture du micro : rien n'a été dit
        flux.getTracks().forEach(t => t.stop());
        setLibre(l => ({ ...l, erreur: 'Garde le bouton appuyé pendant que tu parles, puis relâche.' }));
        return;
      }
      const rec = new MediaRecorder(flux);
      morceauxAudio.current = [];
      rec.ondataavailable = e => { if (e.data.size) morceauxAudio.current.push(e.data); };
      rec.onstop = async () => {
        flux.getTracks().forEach(t => t.stop());
        if (performance.now() - debutMicro.current < 500) {   // un simple clic : pas de transcription
          setLibre(l => ({ ...l, enregistre: false, erreur: 'Garde le bouton appuyé pendant que tu parles, puis relâche.' }));
          return;
        }
        const blob = new Blob(morceauxAudio.current, { type: rec.mimeType || 'audio/webm' });
        const b64 = await new Promise<string>(ok => { const fr = new FileReader(); fr.onload = () => ok(String(fr.result)); fr.readAsDataURL(blob); });
        // Ce qu'il vient de dire s'écrit tout de suite dans le champ (MoulSot v4) : il voit si c'est bien compris,
        // corrige au besoin, puis envoie. Si la transcription échoue, l'enregistrement reste et part tel quel.
        setLibre(l => ({ ...l, enregistre: false, audio: b64, transcrit: true, erreur: undefined }));
        try {
          const { texte } = await appelerApi<{ texte: string }>('/course-player/transcrire', { audio_b64: b64 });
          setLibre(l => ({ ...l, transcrit: false, audio: undefined, aVerifier: true, texte: [l.texte.trim(), texte.trim()].filter(Boolean).join(' ') }));
        } catch (e) {
          const m = (e as Error).message;
          setLibre(l => ({ ...l, transcrit: false, erreur: /^\d+$/.test(m) ? 'La transcription n’a pas abouti : ton enregistrement partira tel quel.' : m }));
        }
      };
      rec.start(); enregistreur.current = rec; debutMicro.current = performance.now();
      limiteMicro.current = window.setTimeout(arreterMicro, 60_000);   // une minute au plus
      setLibre(l => ({ ...l, enregistre: true, audio: undefined, erreur: undefined }));
    } catch {
      appuiMicro.current = false;
      setLibre(l => ({ ...l, erreur: 'Le micro n’est pas disponible : écris ta question, ou envoie une image.' }));
    }
  }, [arreterMicro]);

  /** Après l'explication : « واش فهمتي مزيان ؟ » et le petit exercice s'écrit au tableau. */
  const proposerExercice = useCallback((tour: number) => {
    const t = tableauRef.current;
    if (tour !== tourQuestion.current || !t || t.etape !== 'ecrit' || !t.exercice) return;
    setTableauProf({ ...t, etape: 'exercice', vues: t.lignes.length });
    ressentir('think');
    const voix = voixRef.current;
    if (voix) { voix.src = CLIPS.verifier; void voix.play().catch(() => {}); }
  }, [ressentir]);
  /** La voix de l'explication part ; à sa fin (ou, sans voix, après les lignes), l'exercice. */
  /**
   * Une parole longue, dite par morceaux (préparés deux à la fois) : le premier part dès qu'il est prêt, chacun
   * s'enchaîne à la fin du précédent ; `fin` après le dernier. false : rien n'a pu être dit (l'écrit suffit).
   */
  const direMorceaux = useCallback(async (urls: Promise<string | null>[], encore: () => boolean, fin: () => void): Promise<boolean> => {
    const voix = voixRef.current;
    const url = await urls[0];
    if (!encore() || !url || !voix) return false;
    voixExplication.current = true; finMorceaux.current = { encore, fin };
    fileVoix.current = urls.slice(1); morceaux.current = { total: urls.length, joues: 0 };
    voix.src = url;
    try { await voix.play(); return true; } catch { voixExplication.current = false; fileVoix.current = []; finMorceaux.current = null; return false; }
  }, []);
  /**
   * Le tuteur LIT l'énoncé quand une question s'ouvre (12 novembre 2026), pendant le temps de réflexion : la piste
   * préparée (`enonce_audio`, voix du cours), sinon `enonce_dit` ou l'énoncé écrit, dit par la voix en direct par morceaux
   * (le serveur le normalise comme toute voix en direct : symboles, nombres, unités). Les options ne sont pas lues : elles
   * arrivent après le temps de réflexion. La lecture s'arrête dès que l'élève répond ou passe.
   */
  const tourEnonce = useRef(0);
  const sonsEnonce = useRef<Set<string>>(new Set());
  const lireEnonce = useCallback((q: QuestionDiapo) => {
    const voix = voixRef.current;
    if (!voix) return;
    const tour = ++tourEnonce.current;
    const sons = new Set<string>();
    sonsEnonce.current = sons;
    if (q.lu?.enonce_audio) {
      voixExplication.current = false; fileVoix.current = [];
      sons.add(new URL(q.lu.enonce_audio, location.href).href);
      voix.src = q.lu.enonce_audio; void voix.play().catch(() => {});
      return;
    }
    const texte = (q.lu?.enonce_dit || q.enonce || '').trim();
    if (!texte) return;
    const urls = preparerTextes(decouperParole(texte)).map(u => u.then(x => { if (x) sons.add(x); return x; }));
    void direMorceaux(urls, () => tour === tourEnonce.current, () => {});
  // eslint-disable-next-line react-hooks/exhaustive-deps -- direMorceaux est stable
  }, [preparerTextes]);
  /** L'élève répond ou passe : la lecture de l'énoncé s'arrête (et seulement elle : une réaction qui parle continue). */
  const arreterEnonce = useCallback(() => {
    tourEnonce.current += 1;
    const voix = voixRef.current;
    if (voix && sonsEnonce.current.has(voix.src)) {
      voixExplication.current = false; fileVoix.current = [];
      voix.pause();
    }
    sonsEnonce.current = new Set();
  }, []);
  /** Où en est la voix dite par morceaux : morceaux finis + fraction du morceau en cours (null : elle ne parle pas). */
  const progressionMorceaux = (): number | null => {
    const v = voixRef.current;
    if (!v || !voixExplication.current) return null;
    const frac = Number.isFinite(v.duration) && v.duration > 0 ? Math.min(1, v.currentTime / v.duration) : 0;
    return morceaux.current.joues + frac;
  };
  const lancerExplication = useCallback(async (urls: Promise<string | null>[], nLignes: number, tour: number) => {
    const encore = () => tour === tourQuestion.current;
    const dit = await direMorceaux(urls, encore, () => window.setTimeout(() => proposerExercice(tour), 700));
    if (!dit && encore()) window.setTimeout(() => proposerExercice(tour), nLignes * 2400 + 2500);
  }, [direMorceaux, proposerExercice]);
  /** Un morceau est fini : le suivant s'enchaîne ; après le dernier, ce qui suit (exercice, question, fin de démonstration). */
  const morceauFini = useCallback(async () => {
    if (!voixExplication.current) return;
    const suite = finMorceaux.current, voix = voixRef.current;
    while (fileVoix.current.length) {
      const url = await fileVoix.current.shift()!;
      if (!suite?.encore() || !voixExplication.current || finMorceaux.current !== suite) return;
      morceaux.current.joues += 1;
      if (url && voix) { voix.src = url; try { await voix.play(); return; } catch { /* morceau suivant */ } }
    }
    voixExplication.current = false;
    finMorceaux.current = null;
    if (suite?.encore()) suite.fin();
  }, []);
  /**
   * Après une réponse de conversation : le cours reprend ; s'il était fini, les questions reviennent. Jamais la
   * diapositive suivante toute seule : c'est l'élève qui appuie sur « Suite → » (11 novembre 2026).
   */
  const avancerLeCours = useCallback(() => {
    setLibre({ phase: 'saisie', texte: '', enregistre: false });
    setPanneau(null); setTableauProf(null); setAnnonce(null);
    if (predictionEnCours) { setPanneau('questions'); return; }   // la prédiction attend encore sa réponse
    const audio = audioRef.current;
    if (coursEnPause.current) { coursEnPause.current = false; void audio?.play(); if (demarree.current) envoyerASim('resume'); return; }
    if (audio && !audio.ended && audio.currentTime > 0 && piste?.url) return;   // la voix du cours joue encore
    if (questions.some(q => !(q.cle in finies.current)) && !legendeEnCours()) setPanneau('questions');
  }, [envoyerASim, piste?.url, questions, predictionEnCours]);
  /** L'élève a répondu à l'exercice : le tuteur réagit à la voix, la réponse compte pour les acquis. */
  const exerciceFini = useCallback((ex: Exercice, correct: boolean, reponse: string) => {
    ressentir(correct ? 'celebrate' : 'encourage');
    void dire(correct ? ex.parole_juste : ex.parole_faux);
    void appelerApi('/course-player/acquis', {
      slide_id: slide.id, slide_title: slide.title, deck_id: deckId, cle: 'question_libre_exercice', type: ex.type, enonce: (ex.enonce || '').slice(0, 300),
      reponse: reponse.slice(0, 300), tentative: 1, correct, reaction_preparee: false, methodes: { visuel: 'tableau', question_libre: true },
    }).catch(() => { /* jamais bloquant */ });
  }, [ressentir, dire, slide.id, slide.title, deckId]);

  const envoyerQuestion = useCallback(async () => {
    if (libre.phase !== 'saisie' || (!libre.texte.trim() && !libre.audio && !libre.image)) return;
    // « merci », « مزيان », « d'accord », « bonjour » : une conversation normale, pas une demande d'explication.
    // La réponse est préenregistrée (instantanée), puis le cours avance ; rien n'est réexpliqué.
    const social = !libre.audio && !libre.image ? motSocial(libre.texte) : null;
    if (social) {
      const tour = ++tourQuestion.current;
      voixExplication.current = false;
      setLibre(l => ({ ...l, phase: 'envoi', erreur: undefined }));
      ressentir(social === 'ok' ? 'celebrate' : social === 'merci' ? 'love' : 'greet');
      await jouerEtAttendre(CLIPS[social], 6000);
      if (tour === tourQuestion.current) avancerLeCours();
      return;
    }
    setLibre(l => ({ ...l, phase: 'envoi', erreur: undefined }));
    ressentir('think');
    // Une vraie question : le professeur le dit tout de suite (phrase préenregistrée) pendant qu'il prépare sa réponse.
    if (libre.audio || libre.image || DEMANDE.test(libre.texte)) {
      const voix = voixRef.current;
      voixExplication.current = false;
      if (voix) { voix.src = CLIPS_QUESTION[Math.floor(Math.random() * CLIPS_QUESTION.length)]; void voix.play().catch(() => {}); }
    }
    iframeRef.current?.contentWindow?.postMessage({ type: 'simulation_manifest_request' }, '*');
    await new Promise(r => window.setTimeout(r, 150));
    let r: ReponseLibre;
    try {
      r = await appelerApi<ReponseLibre>('/course-player/question-eleve', {
        deck_id: deckId, slide_id: slide.id, title: slide.title, speech: parole, ce_qui_se_voit: String(dernierEtat.current?.ce_qui_se_voit || ''),
        texte: libre.texte.trim(), audio_b64: libre.audio, image_b64: libre.image?.b64, image_mime: libre.image?.mime || 'image/png',
        moments: dernierEtat.current?.moments || {}, reperes: reperesRef.current,
      });
    } catch (e) {
      const m = (e as Error).message;
      setLibre(l => ({ ...l, phase: 'saisie', erreur: /^\d+$/.test(m) ? `Le professeur n'a pas pu répondre (${m}).` : m }));
      return;
    }
    const tour = ++tourQuestion.current;
    const encore = () => tour === tourQuestion.current;   // l'élève a changé de diapositive ou fermé le tableau
    const question = r.question_comprise || libre.texte.trim();
    const categorie = r.categorie || 'diapo';
    setLibre(l => ({ ...l, phase: 'reponse', reponse: r }));
    setPanneau(null);   // la réponse se fait au tableau, pas dans la bulle
    void appelerApi('/course-player/acquis', {
      slide_id: slide.id, slide_title: slide.title, deck_id: deckId, cle: 'question_libre', type: 'directe', enonce: question.slice(0, 300),
      reponse: categorie, tentative: 1, correct: null, reaction_preparee: false, methodes: { visuel: visuel?.kind || 'aucun', question_libre: true },
    }).catch(() => { /* jamais bloquant */ });

    if (categorie === 'conversation') {
      // Une remarque, un mot gentil : une ou deux phrases à la voix, sans tableau ni exercice, puis le cours avance.
      ressentir('love');
      const dit = await dire(r.parole);
      if (!encore()) return;
      if (dit) await new Promise<void>(ok => {
        const v = voixRef.current, max = window.setTimeout(ok, 12000);
        const fin = () => { window.clearTimeout(max); v?.removeEventListener('ended', fin); ok(); };
        if (!v || v.ended || v.paused) fin(); else v.addEventListener('ended', fin);
      });
      if (encore()) avancerLeCours();
      return;
    }

    if (categorie === 'suivante' || categorie === 'hors_cours') {
      // Une notion d'une diapositive qui vient, ou une question hors du cours : il le dit simplement, puis reprend.
      setAnnonce({ mode: categorie, notion: r.notion, titre: r.diapo_suivante?.title });
      ressentir(categorie === 'suivante' ? 'encourage' : 'think');
      await jouerEtAttendre(CLIPS[categorie], 9000);
      if (!encore()) return;
      await attendre(1200);
      if (!encore()) return;
      setAnnonce(null);
      voixRef.current?.pause();
      setLibre({ phase: 'saisie', texte: '', enregistre: false });
      if (coursEnPause.current) { coursEnPause.current = false; void audioRef.current?.play(); if (demarree.current) envoyerASim('resume'); }
      return;
    }

    if (categorie === 'prerequis') {
      // Une notion de base : la brosse efface le tableau pendant une phrase préenregistrée ; pendant ce temps
      // l'explication s'écrit au serveur et sa voix se calcule. Puis il l'explique sur le tableau propre.
      ressentir('encourage');
      setTableauProf({ mode: 'efface', etape: 'brosse', lignes: [], vues: 0, parole: '', ecrit: '', notion: r.notion, question, texte: false, debut: 0 });
      const prepa = (async () => {
        const e = await appelerApi<{ parole: string; ecrit: string; tableau: string[]; exercice?: Exercice | null }>('/course-player/question-eleve/explication', {
          deck_id: deckId, slide_id: slide.id, title: slide.title, speech: parole, question, notion: r.notion,
        });
        const urls = preparerMorceaux(e.parole);
        await urls[0];   // le premier morceau est prêt avant la fin de la brosse (ou juste après)
        return { e, urls };
      })();
      prepa.catch(() => { /* lu plus bas */ });
      await Promise.all([jouerEtAttendre(CLIPS.effacer, 7000), attendre(BROSSE_MS)]);
      if (!encore()) return;
      setTableauProf(t => t && { ...t, etape: 'prepare' });
      try {
        const { e, urls } = await prepa;
        if (!encore()) return;
        setTableauProf(t => t && { ...t, etape: 'ecrit', lignes: e.tableau || [], parole: e.parole, ecrit: e.ecrit, exercice: e.exercice, debut: performance.now() });
        void lancerExplication(urls, (e.tableau || []).length, tour);
      } catch (err) {
        const m = (err as Error).message;
        if (encore()) setTableauProf(t => t && { ...t, etape: 'ecrit', erreur: /^\d+$/.test(m) ? 'Le professeur n’a pas pu préparer son explication.' : m });
      }
      return;
    }

    // La notion de la diapositive : expliquée au tableau, à la voix, avec la figure.
    ressentir('encourage');
    setTableauProf({ mode: 'diapo', etape: 'prepare', lignes: r.tableau || [], vues: 0, parole: r.parole, ecrit: r.ecrit, notion: r.notion, question, texte: false, debut: 0, exercice: r.exercice });
    const urls = preparerMorceaux(r.parole);
    await urls[0];
    if (!encore()) return;
    setTableauProf(t => t && { ...t, etape: 'ecrit', debut: performance.now() });
    void lancerExplication(urls, (r.tableau || []).length, tour);
    (r.gestes || []).forEach((g, i) => window.setTimeout(() => {
      if (!encore()) return;
      if (g.commande) parTuteur(g.commande, g.parametres || {});
      else if (g.repere) parTuteur('highlight', { target: g.repere });
    }, 1200 + i * 3500));
  }, [libre, deckId, slide.id, slide.title, parole, visuel?.kind, preparerMorceaux, dire, jouerEtAttendre, parTuteur, ressentir, envoyerASim, lancerExplication, avancerLeCours]);

  const reprendreApresQuestion = useCallback(() => {
    tourQuestion.current += 1; voixExplication.current = false; fileVoix.current = [];
    voixRef.current?.pause();
    setLibre({ phase: 'saisie', texte: '', enregistre: false });
    setPanneau(null); setTableauProf(null); setAnnonce(null);
    if (coursEnPause.current) { coursEnPause.current = false; void audioRef.current?.play(); if (demarree.current) envoyerASim('resume'); }
  }, [envoyerASim]);

  /** Une autre question : le tableau du professeur se ferme, la bulle de la question se rouvre. */
  const autreQuestion = useCallback(() => {
    tourQuestion.current += 1; voixExplication.current = false; fileVoix.current = [];
    voixRef.current?.pause();
    setTableauProf(null); setAnnonce(null);
    setLibre({ phase: 'saisie', texte: '', enregistre: false });
    setPanneau('question_eleve');
  }, []);

  // Les lignes du tableau s'écrivent au rythme de la voix (sans voix : une ligne toutes les 2,4 s) ; le tuteur
  // montre chaque ligne quand il l'écrit.
  useEffect(() => {
    const t = tableauProf;
    if (!t || t.etape !== 'ecrit' || t.vues >= t.lignes.length) return;
    const v = voixRef.current;
    const n = v && voixParle && Number.isFinite(v.duration) && v.duration > 0
      ? Math.floor(((morceaux.current.joues + v.currentTime / v.duration) / Math.max(1, morceaux.current.total)) * t.lignes.length * 1.15) + 1
      : Math.floor((performance.now() - t.debut) / 2400) + 1;
    if (n > t.vues) {
      const vues = Math.min(n, t.lignes.length);
      setTableauProf({ ...t, vues });
      const el = lignesProfRef.current[vues - 1];
      if (el && tuteur3D) window.setTimeout(() => focusProfessor(el), 50);
    }
  }, [horloge, tableauProf, voixParle, tuteur3D]);

  /**
   * La diapositive suivante, quand l'élève appuie sur « Suite → ». `resolue` : la diapositive est finie pour de bon
   * (questions justes, ou reprise close) ; sinon c'est un passage à la main, et une reprise en cours est notée
   * abandonnée (effet de démontage plus haut).
   */
  const passerALaDiapoSuivante = useCallback((resolue: boolean) => {
    voixExplication.current = false; fileVoix.current = [];
    voixRef.current?.pause();
    setPanneau(null);
    if (resolue) setCycle(null);
    onSuivant?.();
  }, [onSuivant]);

  /** Faux : le tuteur réexplique AUTREMENT (DeepSeek, avec tout le contexte), montre dans la simulation, puis question jumelle. */
  const lancerCycle = useCallback(async (n: number, depuis: QuestionDiapo) => {
    setCycle({ n, phase: 'attente', depuis });
    setIndexQuestion(0);
    setPanneau(null);                                   // la scène redevient visible : le tuteur va y montrer
    ressentir('think');
    const essayees = ['explication du cours', visuel?.kind === 'simulation' ? 'simulation' : visuel?.kind || 'aucun visuel', ...Array.from({ length: n - 1 }, (_, i) => `reprise ${i + 1}`)];
    // Les repères dessinés depuis le début (le retard τ, la cote L… n'existent qu'après la scène) : manifeste à jour.
    iframeRef.current?.contentWindow?.postMessage({ type: 'simulation_manifest_request' }, '*');
    await new Promise(r => window.setTimeout(r, 700));
    try {
      const r = await appelerApi<Reprise>('/course-player/reexplication', {
        deck_id: deckId, slide_id: slide.id, title: slide.title, speech: parole,
        question: { type: depuis.type, enonce: depuis.enonce, choix: depuis.choix, bonne: depuis.bonne },
        reponses_fausses: (fausses.current[depuis.cle] || []).join(' ; '), cycle: n, methodes_essayees: essayees,
        moments: dernierEtat.current?.moments || {}, reperes: reperesRef.current,
      });
      setCycle({ n, phase: 'explique', data: r, depuis });
      voixLancee.current = false;
      const joue = await dire(r.parole);
      if (joue) voixLancee.current = true;        // la fin de la voix amènera la question (effet sur voixParle)
      // Les gestes dans la simulation, l'un après l'autre, pendant qu'il parle.
      r.gestes.forEach((g, i) => window.setTimeout(() => {
        if (cycleRef.current?.n !== n) return;
        if (g.commande) parTuteur(g.commande, g.parametres || {});
        else if (g.repere) parTuteur('highlight', { target: g.repere });
      }, 1500 + i * 3500));
      // Sans voix (serveur de voix absent), la question jumelle arrive après le temps des gestes.
      if (!joue) window.setTimeout(() => { if (cycleRef.current?.n === n && cycleRef.current.phase === 'explique') { setCycle(c => c && c.n === n ? { ...c, phase: 'question' } : c); setPanneau('questions'); } }, 2500 + r.gestes.length * 3500);
    } catch {
      setCycle(null); setPanneau('questions');
    }
  }, [deckId, slide.id, slide.title, parole, visuel?.kind, dire, parTuteur, ressentir]);

  // La voix de la reprise s'arrête : la question jumelle descend sur le tableau.
  useEffect(() => {
    const c = cycleRef.current;
    if (!c || c.phase !== 'explique' || voixParle || !voixLancee.current) return;
    setCycle({ ...c, phase: 'question' }); setPanneau('questions');
  }, [voixParle]);

  /**
   * Le passage seul après une réponse (user rule, 12 novembre 2026) : l'élève a répondu (ou passé), la réaction du
   * tuteur est dite (et la démonstration, son tableau fermé) → ~1,5 s plus tard le cours passe à la question suivante
   * s'il en reste, sinon à la diapositive suivante (ou, pour une prédiction, à la voix qui montre la réponse). Pas de
   * passage si l'élève a touché l'écran entre-temps (il lit, il a ouvert le cahier…). Le reste reste au bouton
   * « Suite → » : fin de la voix d'une diapositive, cycle de reprise, fin de bloc.
   */
  const [tourSuiteSeule, setTourSuiteSeule] = useState(0);
  const suiteSeule = useRef(0);
  const programmerSuite = useCallback((sansReaction = false) => {
    const tour = ++suiteSeule.current;
    let touche = false;
    const marquer = () => { touche = true; };
    const ecouter = window.setTimeout(() => {
      window.addEventListener('pointerdown', marquer, true); window.addEventListener('keydown', marquer, true);
    }, 0);
    const finir = () => { window.clearTimeout(ecouter); window.removeEventListener('pointerdown', marquer, true); window.removeEventListener('keydown', marquer, true); };
    const parle = () => { const v = voixRef.current; return !!v && !v.paused && !v.ended; };
    const debut = Date.now();
    // la voix de la réaction démarre (une voix en direct met quelques secondes : 4 s au plus), puis elle finit
    let partie = false;
    const attendreLaReaction = () => new Promise<void>(ok => {
      const tic = () => {
        if (tour === suiteSeule.current && Date.now() - debut < 60_000) {
          if (parle()) partie = true;
          if (parle() || (!partie && !sansReaction && Date.now() - debut < 4000)) { window.setTimeout(tic, 250); return; }
        }
        ok();
      };
      window.setTimeout(tic, 250);
    });
    void attendreLaReaction().then(() => attendre(1500)).then(() => {
      finir();
      if (touche || tour !== suiteSeule.current || parle()) return;
      setTourSuiteSeule(t => t + 1);
    });
  }, []);

  /**
   * Une question est finie (réaction dite, démonstration écrite et son tableau fermé) : le cours passe seul à la suite
   * (`programmerSuite`) ; une reprise reste au bouton « Suite → ». Exception : la dernière jumelle fausse du dernier
   * cycle montre la réponse (c'est la réaction finale, pas un passage).
   */
  const surFinie = useCallback((cle: string, correct: boolean, fraiche: boolean, apresDemo = false) => {
    finies.current[cle] = correct;
    setVersionFinies(v => v + 1);
    // après la démonstration (son tableau fermé), la réaction est dite depuis longtemps : rien à attendre.
    // Une question ratée ne passe pas seule : la correction reste à l'écran jusqu'à « Suite → » (15 novembre 2026).
    if (fraiche && correct && !cle.startsWith('cycle')) programmerSuite(apresDemo);
    const c = cycleRef.current;
    if (!c || !cle.startsWith('cycle') || !fraiche || c.n < MAX_CYCLES) return;
    const liste = jumellesRef.current;
    if (!liste.every(q => q.cle in finies.current) || liste.every(q => finies.current[q.cle])) return;
    setCycle({ ...c, phase: 'final' });
    if (c.data?.reponse_finale) void dire(c.data.reponse_finale);
  }, [dire, programmerSuite]);

  /** L'élève passe une question (12 novembre 2026) : elle compte comme close pour « Suite → », sans erreur ni reprise ;
   *  il peut y revenir avec les petites flèches et y répondre (sa réponse remplace alors le passage). */
  const surPassee = useCallback((cle: string, fraiche = false) => {
    if (finies.current[cle] === true || finies.current[cle] === false) return;
    finies.current[cle] = 'passee';
    setVersionFinies(v => v + 1);
    if (fraiche) programmerSuite(true);   // passée : pas de réaction à attendre
  }, [programmerSuite]);
  /** La question de prédiction est finie (réaction dite) : la voix qui montre la réponse part seule ensuite. */
  const surPredictionFinie = useCallback((_cle?: string, correct?: boolean | null, fraiche?: boolean) => {
    setPredictionRepondue(slide.id);
    if (fraiche) programmerSuite(correct === null);
  }, [slide.id, programmerSuite]);

  /** Chaque réponse part au suivi des acquis, avec la manière dont la notion a été expliquée sur cette diapositive. */
  const enregistrerReponse = useCallback((r: ReponseNotee) => {
    const predite = r.type === 'prediction';
    if (r.correct === false && !predite) (fausses.current[r.cle] ||= []).push(r.reponse);
    if (!predite && r.correct !== null) onReponseJugee?.({ correct: r.correct });
    if (r.passee) {
      void appelerApi('/course-player/acquis', {
        slide_id: slide.id, slide_title: slide.title, deck_id: deckId, cle: r.cle, type: r.type, enonce: r.enonce, reponse: '',
        tentative: r.tentative, correct: null, passee: true, reaction_preparee: false,
        methodes: { visuel: predite ? 'prediction' : visuel?.kind || (table ? 'table' : 'aucun'), prediction: predite, exercice: r.cle.startsWith('e') },
      }).catch(() => { /* le suivi ne doit jamais gêner l'élève */ });
      return;
    }
    // juste du premier coup : il exulte ; juste après l'indice : il encourage ; faux : il secoue la tête et tend
    // une idée ; faux une deuxième fois : il encourage quand même ; réponse qu'il ne peut pas juger : il réfléchit.
    // Une prédiction fausse n'est pas une erreur : il encourage (« on va voir »).
    ressentir(r.correct === true ? (r.tentative <= 1 ? 'celebrate' : 'encourage') : r.correct === false ? (r.tentative <= 1 && !predite ? 'wrong' : 'encourage') : 'think');
    void appelerApi('/course-player/acquis', {
      slide_id: slide.id, slide_title: slide.title, deck_id: deckId, cle: r.cle, type: r.type, enonce: r.enonce, reponse: r.reponse,
      tentative: r.tentative, correct: r.correct, reaction_preparee: r.preparee,
      // Une prédiction vient AVANT l'explication : aucune méthode n'a encore été employée (hors score côté serveur).
      methodes: predite ? { visuel: 'prediction', prediction: true, exercice: false } : {
        visuel: visuel?.kind || (table ? 'table' : 'aucun'), formules_au_centre: centre.length,
        tuteur_a_montre: pointage.length, eleve_a_manipule: eleveATouche.current, variante_du_tuteur: varianteFaite.current,
        exercice: r.cle.startsWith('e'), reexplication: cycleRef.current?.n || 0,
      },
    }).catch(() => { /* le suivi ne doit jamais gêner l'élève */ });
  }, [slide.id, slide.title, deckId, visuel?.kind, table, centre.length, pointage.length, ressentir, onReponseJugee]);
  /** La réponse à la prédiction : notée `prediction` (une prédiction fausse n'est pas une erreur de compétence). */
  const enregistrerPrediction = useCallback((r: ReponseNotee) => enregistrerReponse({ ...r, type: 'prediction' }), [enregistrerReponse]);

  /** Une piste déjà prête (réaction préparée) : elle part tout de suite. */
  const jouer = useCallback((url: string, secours?: string) => {
    const voix = voixRef.current;
    if (!voix) return;
    // Piste absente ou illisible (404…) : la réaction est dite par la voix en direct plutôt que de rester muette.
    voix.src = url; void voix.play().catch((e: unknown) => { if (secours && (e as Error)?.name !== 'AbortError') void dire(secours); });
  }, [dire]);

  /**
   * Le schéma à légender est fini (toutes les étiquettes à leur place) ou abandonné (le tuteur les pose) : il compte
   * pour les acquis — sans erreur = juste du premier coup ; 1 ou 2 erreurs = juste au 2e essai (partiel) ; plus = raté ;
   * abandonné = passé — le tuteur le commente avec sa réaction préparée, puis les questions de la diapositive viennent.
   */
  const finirLegende = (abandon: boolean) => {
    const L = legendeRef.current;
    if (!L || L.close) return;
    L.close = true;
    const genre = abandon ? 'aide' : L.erreurs === 0 ? 'juste' : L.erreurs <= 2 ? 'partiel' : 'faux';
    const correct = abandon ? null : L.erreurs <= 2;
    const mal = L.mal ? ` Erreurs sur : ${L.mal}.` : '';
    const prep = conc.legende?.reactions?.[genre];
    const ecrits = {
      juste: `Bravo : les ${L.total} étiquettes sont à leur place du premier coup.`,
      partiel: `Toutes les étiquettes sont à leur place, avec ${L.erreurs} erreur${L.erreurs > 1 ? 's' : ''} en route.${mal}`,
      faux: `Le schéma est complet, mais avec ${L.erreurs} erreurs : regarde bien où va chaque étiquette.${mal}`,
      aide: 'Je place les étiquettes : regarde bien où va chacune. La prochaine fois, c’est toi qui les poses.',
    } as const;
    const ecrit = prep?.ecrit ? `${prep.ecrit}${genre === 'partiel' || genre === 'faux' ? mal : ''}` : ecrits[genre];
    void appelerApi('/course-player/acquis', {
      slide_id: slide.id, slide_title: slide.title, deck_id: deckId, cle: 'legende', type: 'legende', enonce: `Légender le schéma : ${slide.title}`.slice(0, 500),
      reponse: abandon ? '' : `${L.places}/${L.total} étiquettes, ${L.erreurs} erreur(s)${L.mal ? ` sur ${L.mal}` : ''}`.slice(0, 500),
      tentative: abandon || L.erreurs === 0 ? 1 : 2, correct, passee: abandon, reaction_preparee: !!prep?.audio,
      methodes: { visuel: visuel?.kind || 'simulation', eleve_a_manipule: !abandon, exercice: true },
    }).catch(() => { /* le suivi ne doit jamais gêner l'élève */ });
    if (correct !== null) onReponseJugee?.({ correct });
    ressentir(genre === 'juste' ? 'celebrate' : genre === 'faux' ? 'wrong' : 'encourage');
    setLegendeMot({ texte: ecrit, correct });
    const parole = prep?.parole || ecrit;
    const finVoix: Promise<unknown> = prep?.audio
      ? (jouer(prep.audio, parole), attendre(1500).then(() => new Promise<void>(ok => {
        const tic = () => { const v = voixRef.current; if (v && !v.paused && !v.ended) window.setTimeout(tic, 300); else ok(); };
        tic();
      })))
      : dire(parole);
    void finVoix.then(() => attendre(800)).then(() => {
      if (legendeRef.current !== L) return;   // l'élève a changé de diapositive
      if (questions.some(q => !(q.cle in finies.current))) setPanneau('questions');
    });
  };
  finirLegendeRef.current = finirLegende;

  /** Un texte dit jusqu'au bout (voix en direct) ; sans voix, le temps de le lire. */
  const direEtAttendre = useCallback(async (url: Promise<string | null>, texte: string) => {
    const u = await url;
    if (u && await jouerEtAttendre(u, 25000)) return;
    await attendre(Math.min(6000, Math.max(1500, texte.length * 45)));
  }, [jouerEtAttendre]);
  /** Les retours se disent l'un après l'autre ; leur voix se calcule dès que l'élève a choisi. */
  const direALaSuite = useCallback((texte: string, encore: () => boolean) => {
    if (!texte.trim()) return fileRetours.current;
    const url = preparerVoix(texte);
    fileRetours.current = fileRetours.current.then(() => (encore() ? direEtAttendre(url, texte) : undefined));
    return fileRetours.current;
  }, [preparerVoix, direEtAttendre]);

  /** Le panneau du résultat se ferme et le cours reprend tout seul (ou les questions reviennent si elles étaient ouvertes). */
  const fermerResultat = useCallback(() => {
    tourResultat.current += 1;
    voixExplication.current = false; fileVoix.current = []; finMorceaux.current = null;
    fileRetours.current = Promise.resolve();
    voixRef.current?.pause();
    setReaction(null);
    if (coursEnPause.current) { coursEnPause.current = false; void audioRef.current?.play(); if (demarree.current) envoyerASim('resume'); }
    else if (panneauAvant.current === 'questions') setPanneau('questions');
    panneauAvant.current = null;
  }, [envoyerASim]);

  /**
   * « 🔎 Ton résultat » (10 novembre 2026) : le cours se met en pause, une phrase préenregistrée part tout de suite
   * pendant que DeepSeek interprète avant/après, puis le tuteur dit TOUT ce qui s'écrit — l'interprétation (l'écrit
   * apparaît au fil de la voix, par morceaux), puis la question et ses choix ; quand la voix finit, l'élève répond.
   */
  const ouvrirResultat = useCallback(async () => {
    const res = resultatRef.current;
    if (!res || reactionRef.current) return;
    setResultat(null);
    const tour = ++tourResultat.current;
    const encore = () => tour === tourResultat.current;
    const audio = audioRef.current;
    if (audio && !audio.paused) { audio.pause(); coursEnPause.current = true; if (demarree.current) envoyerASim('pause'); }
    panneauAvant.current = panneau; setPanneau(null);
    setReaction({ phase: 'reflechit' });
    ressentir('surprise');
    // Jamais de silence (règle 25) : il réagit tout de suite, la réponse du LLM prend 2 à 5 s ; si elle tarde encore,
    // une deuxième phrase préenregistrée suit aussitôt (deux au plus).
    const premiere = Math.floor(Math.random() * CLIPS_RESULTAT.length);
    let clipsDits = 1;
    const accroche = jouerEtAttendre(CLIPS_RESULTAT[premiere], 5000);
    const sansSilence = async (attendu: Promise<unknown>) => {
      await accroche;
      while (encore() && clipsDits < 2 && !(await Promise.race([attendu.then(() => true, () => true), attendre(120).then(() => false)]))) {
        await jouerEtAttendre(CLIPS_RESULTAT[(premiere + clipsDits) % CLIPS_RESULTAT.length], 4000);
        clipsDits += 1;
      }
    };
    const demande = appelerApi<{ parole: string; ecrit: string; parole_question?: string; question: QuestionSim }>('/course-player/sim-reaction', {
      mode: 'interpreter', diapo: { title: slide.title, speech: parole }, avant: res.avant || {}, apres: res.apres, historique: historique.current,
    });
    const remplissage = sansSilence(demande);
    let r: { parole: string; ecrit: string; parole_question?: string; question: QuestionSim };
    try {
      r = await demande;
    } catch (e) {
      if (encore()) setReaction({ phase: 'erreur', message: `Le professeur n'a pas pu répondre (${(e as Error).message}).` });
      return;
    }
    if (!encore()) return;
    const ecrit = (r.ecrit || '').trim();
    const morceauxParole = decouperParole(r.parole || ecrit);
    const morceauxQuestion = decouperParole((r.parole_question || '').trim());
    const urls = preparerTextes([...morceauxParole, ...morceauxQuestion]);
    const base = { phase: 'question' as const, ecrit, phrases: phrasesEcrites(ecrit), question: r.question, nParole: morceauxParole.length,
      nTotal: morceauxParole.length + morceauxQuestion.length };
    setReaction({ ...base, voix: 'prepare', debut: performance.now() });
    // La phrase préenregistrée finit (et la deuxième, si le premier morceau de voix tarde) avant la voix calculée.
    await remplissage;
    await sansSilence(urls[0]);
    if (!encore()) return;
    const toutDit = () => { if (encore()) setReaction(x => x && x.phase === 'question' ? { ...x, voix: 'fini' } : x); };
    const dit = await direMorceaux(urls, encore, toutDit);
    if (!encore()) return;
    if (dit) { setReaction(x => x && x.phase === 'question' ? { ...x, voix: 'parle', debut: performance.now() } : x); return; }
    // Sans voix : l'écrit se dévoile au temps de lecture, puis la question.
    setReaction(x => x && x.phase === 'question' ? { ...x, voix: 'sansvoix', debut: performance.now() } : x);
    window.setTimeout(toutDit, base.phrases.length * 2200 + 1800);
  }, [panneau, slide.title, parole, envoyerASim, ressentir, jouerEtAttendre, preparerTextes, direMorceaux]);

  /** La réponse de l'élève à la question du résultat : CHAQUE option a son retour, écrit et dit ; puis tout se ferme seul. */
  const repondreResultat = useCallback(async (choix: { indice?: number; affirmation?: { i: number; vrai: boolean }; directe?: string }) => {
    const r = reactionRef.current;
    if (!r || r.phase !== 'question' || r.verdict || r.voix !== 'fini') return;
    const tour = tourResultat.current;
    const encore = () => tour === tourResultat.current;
    const q = r.question;
    const fermerApres = async (attente: Promise<void>) => {
      await attente;
      if (!encore()) return;
      await attendre(1200);
      if (encore()) fermerResultat();
    };
    if (q.type === 'directe') {
      setReaction({ ...r, verdict: { correct: false, ecrit: '…' } });
      try {
        const c = await appelerApi<{ correct: boolean; parole: string; ecrit: string }>('/course-player/sim-reaction', {
          mode: 'corriger', diapo: { title: slide.title }, question: q, reponse: choix.directe || '',
        });
        if (!encore()) return;
        historique.current.push({ type: q.type, correct: c.correct });
        ressentir(c.correct ? 'celebrate' : 'wrong');
        setReaction({ ...r, verdict: { correct: c.correct, ecrit: c.ecrit } });
        void fermerApres(direALaSuite(c.parole || c.ecrit, encore));
      } catch {
        if (!encore()) return;
        const ecrit = q.attendu ? `Réponse attendue : ${q.attendu}` : (q.explication || '');
        setReaction({ ...r, verdict: { correct: false, ecrit } });
        void fermerApres(direALaSuite(q.parole_faux || '', encore).then(() => attendre(3000)));
      }
      return;
    }
    if (q.type === 'qcm' && choix.indice !== undefined) {
      const juste = choix.indice === q.bonne;
      const retour = q.retours?.[choix.indice] || { ecrit: q.explication || '', parole: (juste ? q.parole_juste : q.parole_faux) || '' };
      historique.current.push({ type: q.type, correct: juste });
      ressentir(juste ? 'celebrate' : 'wrong');
      setReaction({ ...r, pris: choix.indice, verdict: { correct: juste, ecrit: retour.ecrit } });
      void fermerApres(direALaSuite(retour.parole || retour.ecrit, encore));
      return;
    }
    if (q.type === 'vrai_faux' && choix.affirmation) {
      const { i, vrai } = choix.affirmation;
      const affs = q.affirmations || [];
      if (r.vf?.[i] !== undefined) return;
      const vf = { ...(r.vf || {}), [i]: vrai };
      const a = affs[i];
      const retour = a?.retours?.[vrai ? 0 : 1];
      // Chaque affirmation tranchée a son retour, dit tout de suite (les suivants attendent leur tour).
      if (retour) { ressentir(vrai === a.vrai ? 'celebrate' : 'wrong'); void direALaSuite(retour.parole || retour.ecrit, encore); }
      const retoursVf = retour ? { ...(r.retoursVf || {}), [i]: retour } : r.retoursVf;
      if (Object.keys(vf).length < affs.length) { setReaction({ ...r, vf, retoursVf }); return; }
      const juste = affs.every((x, k) => vf[k] === x.vrai);
      historique.current.push({ type: q.type, correct: juste });
      // Sans retours par affirmation (ancien format) : le verdict d'ensemble, avec parole_juste / parole_faux.
      const global = affs.some(x => x.retours) ? null : (juste ? q.parole_juste : q.parole_faux) || '';
      if (global !== null) ressentir(juste ? 'celebrate' : 'wrong');
      setReaction({ ...r, vf, retoursVf, verdict: { correct: juste, ecrit: global !== null ? q.explication || '' : '' } });
      void fermerApres(global !== null ? direALaSuite(global, encore) : fileRetours.current);
    }
  }, [slide.title, ressentir, direALaSuite, fermerResultat]);

  /** L'élève a eu un nouveau résultat : le bouton clignote. Un résultat plus récent remplace le précédent. */
  const noterResultat = useCallback((avant: EtatSim | null, apres: EtatSim) => setResultat({ avant, apres }), []);

  /**
   * La démonstration d'une question (10 novembre 2026) : écrite à la main ligne par ligne pendant que le tuteur la dit.
   * Avec `audio` : la piste du cours, chaque ligne à la place de son `mot` dans `parole` × la durée (comme le centre) ;
   * sans piste : la voix en direct, par morceaux ; sans voix du tout : au temps de lecture.
   */
  /** La voix d'une démonstration sans piste se calcule dès que la réaction part : elle suit sans silence. */
  const preparerDemo = useCallback((d: Demonstration): VoixDemo | null => {
    if (d.audio || !d.parole.trim()) return null;
    const textes = decouperParole(d.parole);
    return { textes, urls: preparerTextes(textes) };
  }, [preparerTextes]);
  const lireDemonstration = useCallback((d: Demonstration, prete?: VoixDemo | null): LectureDemo => {
    const voix = voixRef.current;
    const n = Math.max(1, d.parole.length);
    const tour = ++tourDemo.current;
    let arrete = false, finir: () => void = () => {};
    const fin = new Promise<void>(ok => { finir = ok; });
    const encore = () => !arrete && tour === tourDemo.current;
    let mode: 'attente' | 'piste' | 'morceaux' | 'temps' = 'attente', t0 = 0;
    let bornes: number[] = [0, n];
    const sansVoix = () => {
      if (!encore()) return;
      mode = 'temps'; t0 = performance.now();
      window.setTimeout(() => finir(), (n / 14) * 1000 + 1500);
    };
    let detacher = () => {};
    if (d.audio && voix) {
      mode = 'piste'; voixExplication.current = false;
      const fini = () => { detacher(); if (encore()) finir(); };
      const erreur = () => { detacher(); sansVoix(); };
      detacher = () => { voix.removeEventListener('ended', fini); voix.removeEventListener('error', erreur); };
      voix.addEventListener('ended', fini); voix.addEventListener('error', erreur);
      voix.src = d.audio; voix.play().catch(erreur);
    } else {
      const textes = prete?.textes || decouperParole(d.parole);
      const total = textes.reduce((k, t) => k + t.length + 1, 0) || 1;
      bornes = textes.reduce<number[]>((b, t) => [...b, b[b.length - 1] + ((t.length + 1) / total) * n], [0]);
      void direMorceaux(prete?.urls || preparerTextes(textes), encore, () => finir()).then(dit => { if (dit) mode = 'morceaux'; else sansVoix(); });
    }
    const position = () => {
      if (mode === 'piste' && voix) return Number.isFinite(voix.duration) && voix.duration > 0 ? (voix.currentTime / voix.duration) * n : 0;
      if (mode === 'morceaux') {
        const p = progressionMorceaux();
        if (p === null) return n;
        const j = Math.min(Math.floor(p), bornes.length - 2);
        return bornes[j] + (p - j) * (bornes[j + 1] - bornes[j]);
      }
      if (mode === 'temps') return ((performance.now() - t0) / 1000) * 14;
      return 0;
    };
    return {
      position, fin,
      arreter: () => {
        if (arrete) return;
        arrete = true; detacher();
        if (tour === tourDemo.current) { voixExplication.current = false; fileVoix.current = []; voix?.pause(); }
        finir();
      },
    };
  }, [direMorceaux, preparerTextes]);
  /** La réaction à la réponse est dite jusqu'au bout avant que la démonstration commence. */
  const attendreVoix = useCallback(() => new Promise<void>(ok => {
    const tic = () => { const v = voixRef.current; if (v && !v.paused && !v.ended) { window.setTimeout(tic, 250); return; } ok(); };
    window.setTimeout(tic, 300);
  }), []);

  // Ce que la simulation renvoie : un nouveau résultat obtenu par l'élève lui-même fait clignoter « 🔎 Ton résultat ».
  useEffect(() => {
    const ecouter = (event: MessageEvent) => {
      const d = event.data as { type?: string; current_state?: EtatSim; capabilities?: { reperes?: Record<string, string> } } | null;
      if (!iframeRef.current || event.source !== iframeRef.current.contentWindow || !d) return;
      if (d.type === 'simulation_manifest') { reperesRef.current = { ...reperesRef.current, ...(d.capabilities?.reperes || {}) }; return; }
      if (d.type !== 'simulation_state' || !d.current_state) return;
      const etat = d.current_state;
      const avant = dernierEtat.current;
      dernierEtat.current = etat;
      if (etat.derniere_main === 'eleve') eleveATouche.current = true;   // il a touché : le tuteur ne fait pas la variante à sa place
      // le schéma à légender : ce que l'élève a posé lui-même (les étiquettes posées par le tuteur ne comptent pas)
      const pl = (etat.parameters || {}) as Record<string, unknown>;
      const total = Number(pl.legende_total) || 0;
      if (total > 0) {
        const L = (legendeRef.current ||= { total, places: 0, erreurs: 0, mal: '', close: false });
        L.total = total;
        if (etat.derniere_main === 'eleve' && !L.close) {
          L.places = Number(pl.legende_places) || 0; L.erreurs = Number(pl.legende_erreurs) || 0; L.mal = String(pl.legende_mal || '');
          if (L.places >= total) finirLegendeRef.current(false);
        }
      }
      if (etat.simulation_status !== 'finished' || avant?.simulation_status === 'finished') return;
      const precedent = dernierResultat.current;
      dernierResultat.current = etat;
      if (etat.derniere_main !== 'eleve' || reactionRef.current) return;
      // Même réglage que le résultat précédent : rien de nouveau à interpréter.
      if (precedent && JSON.stringify(precedent.parameters) === JSON.stringify(etat.parameters)) return;
      eleveATouche.current = true;
      noterResultat(precedent, etat);
    };
    window.addEventListener('message', ecouter);
    return () => window.removeEventListener('message', ecouter);
  }, [noterResultat]);

  // Après la voix, si l'élève n'a rien touché : le tuteur fait la variante lui-même, pour comparer
  // (après la question d'observation, s'il y en a une : la variante ne change pas la scène pendant que l'élève regarde).
  useEffect(() => {
    const v = conc.variante;
    if (!finie || !v?.etapes?.length || varianteFaite.current || !simPrete || (observation && !obsClose)) return;
    // Un schéma à légender laisse à l'élève une minute sans le toucher avant que le tuteur pose les étiquettes.
    const debut = Date.now();
    let id = 0;
    const essayer = () => {
      if (eleveATouche.current || reactionRef.current || varianteFaite.current) return;
      const L = legendeRef.current;
      if (L?.close) return;   // l'élève l'a fini : rien à poser à sa place
      if (L && Date.now() - debut < LEGENDE_AIDE_MS) { id = window.setTimeout(essayer, 1000); return; }
      varianteFaite.current = true;
      v.etapes.forEach(e => {
        if (e.commande) parTuteur(e.commande, e.parametres || {});
        else if (e.repere) parTuteur('highlight', { target: e.repere });
      });
      if (L) finirLegendeRef.current(true);
    };
    id = window.setTimeout(essayer, (v.apres_s ?? 5) * 1000);
    return () => window.clearTimeout(id);
  }, [finie, conc.variante, simPrete, parTuteur, observation, obsClose]);

  // ── La question d'observation ──
  /** L'instant où la voix s'arrête : juste après `apres_mot` (null : la question vient à la fin de la voix). */
  const tObservation = useMemo(() => {
    const m = observation?.apres_mot;
    if (!m || !duree) return null;
    const i = parole.indexOf(m);
    if (i < 0) return null;
    return Math.max(0, ((i + m.length) / Math.max(1, parole.length)) * duree - 0.15);
  }, [observation?.apres_mot, parole, duree]);
  /** Un retour dit jusqu'au bout : la piste préparée, sinon la voix en direct ; sans voix, le temps de le lire. */
  const direRetour = useCallback(async (r?: { parole?: string; ecrit?: string; audio?: string }) => {
    if (!r) { await attendre(1500); return; }
    if (r.audio && await jouerEtAttendre(r.audio, 25000)) return;
    const texte = (r.parole || '').trim();
    if (texte) {
      const url = await preparerVoix(texte);
      if (url && await jouerEtAttendre(url, 25000)) return;
    }
    await attendre(Math.min(6000, Math.max(1500, (r.ecrit || texte).length * 45)));
  }, [jouerEtAttendre, preparerVoix]);
  /** La question se ferme : la voix du cours reprend où elle s'était arrêtée (ou, à la fin de la voix, les questions s'ouvrent). */
  const fermerObservation = useCallback(() => {
    tourObs.current += 1;
    obsAppui.current = false;
    if (obsRec.current?.state === 'recording') obsRec.current.stop();
    voixExplication.current = false; fileVoix.current = [];
    voixRef.current?.pause();
    setObs(null); setObsClose(true);
    if (observation?.sim_apres) envoyerASim('set_parameters', observation.sim_apres);   // la conclusion s'écrit
    const audio = audioRef.current;
    if (obsPause.current) { obsPause.current = false; void audio?.play(); return; }
    if (questions.some(q => !(q.cle in finies.current))) setPanneau('questions');
  }, [questions, observation?.sim_apres, envoyerASim]);
  // La simulation se tait sur la réponse (`sim_avant`) dès qu'elle est prête, tant que la question n'est pas close.
  useEffect(() => {
    if (simPrete && observation?.sim_avant && !obsClose) envoyerASim('set_parameters', observation.sim_avant);
  }, [simPrete, observation?.sim_avant, obsClose, envoyerASim]);
  const finirObservation = useCallback(async (tour: number) => {
    if (tour !== tourObs.current) return;
    await attendre(1400);
    if (tour === tourObs.current) fermerObservation();
  }, [fermerObservation]);
  /** Le tuteur s'arrête, fait ce qu'il faut dans la simulation, pose la question… et se tait. */
  const ouvrirObservation = useCallback(() => {
    const o = observation;
    if (!o || obsFaite.current) return;
    obsFaite.current = true;
    const tour = ++tourObs.current;
    setPanneau(p => (p === 'questions' || p === 'cahier' || p === 'explication' ? null : p));
    let delai = 0;
    (o.gestes || []).forEach(g => {
      // la même commande déjà prévue dans le pointage : faite une seule fois (ici, ou déjà faite juste avant l'arrêt)
      const k = pointage.findIndex(p => !!g.commande && p.commande === g.commande && JSON.stringify(p.parametres || {}) === JSON.stringify(g.parametres || {}));
      if (k >= 0) { const fait = dejaFaits.current.has(k); dejaFaits.current.add(k); if (fait) return; }
      if (g.commande) { parTuteur(g.commande, g.parametres || {}); demarree.current = true; }
      else if (g.repere) parTuteur('highlight', { target: g.repere });
      delai = 1100;
    });
    setObs({ etape: 'observe', indices: 0, cartes: false, exclus: [], essai: 1 });
    ressentir('think');
    window.setTimeout(() => {
      if (tour !== tourObs.current || obsRef.current?.etape !== 'observe') return;
      if (o.enonce_audio) jouer(o.enonce_audio);
      else void dire(o.enonce_dit || o.enonce);
    }, delai);
  }, [observation, pointage, parTuteur, ressentir, jouer, dire]);
  // Au milieu de la voix : elle s'arrête juste après `apres_mot` (la simulation, elle, continue : l'élève regarde).
  useEffect(() => {
    if (!observation || obsFaite.current || tObservation === null || !enLecture || temps < tObservation) return;
    const audio = audioRef.current;
    if (audio && !audio.paused) { audio.pause(); obsPause.current = true; }
    ouvrirObservation();
  }, [temps, enLecture, tObservation, observation, ouvrirObservation]);
  // Sans `apres_mot` (ou introuvable) : à la fin de la voix, une fois la simulation prête.
  useEffect(() => {
    if (!observation || obsFaite.current || tObservation !== null || !finie) return;
    if (visuel?.kind === 'simulation' && !simPrete) return;
    const id = window.setTimeout(ouvrirObservation, 700);
    return () => window.clearTimeout(id);
  }, [observation, tObservation, finie, simPrete, visuel?.kind, ouvrirObservation]);
  /** Un silence de plus : le prochain indice (le tuteur peut montrer un repère), puis les cartes. */
  const aiderObservation = useCallback(() => {
    const o = observation, e = obsRef.current;
    if (!o || !e || e.etape !== 'observe') return;
    const indices = o.indices || [];
    if (e.indices < indices.length) {
      const ind = indices[e.indices];
      setObs({ ...e, indices: e.indices + 1 });
      if (ind.repere) parTuteur('highlight', { target: ind.repere });
      if (ind.audio) jouer(ind.audio); else void dire(ind.dit || ind.texte);
      return;
    }
    if (!e.cartes) { setObs({ ...e, cartes: true }); ressentir('encourage'); }
  }, [observation, parTuteur, jouer, dire, ressentir]);
  // Le silence d'observation se compte quand le tuteur ne parle pas et que l'élève ne répond pas.
  useEffect(() => {
    if (!observation || !obs || obs.etape !== 'observe') return;
    if (obs.cartes && obs.indices >= (observation.indices || []).length) return;   // toutes les aides sont là
    const silence = (observation.silence_s ?? SILENCE_OBSERVATION_S) * 1000;
    let calme = 0;
    const id = window.setInterval(() => {
      const v = voixRef.current;
      if (v && !v.paused && !v.ended) { calme = 0; return; }
      calme += 250;
      if (calme >= silence) { calme = 0; aiderObservation(); }
    }, 250);
    return () => window.clearInterval(id);
  }, [observation, obs?.etape, obs?.indices, obs?.cartes, aiderObservation]); // eslint-disable-line react-hooks/exhaustive-deps
  /**
   * La réponse à la question d'observation (carte ou micro) : juste → ce qu'il fallait voir, puis la voix reprend ;
   * fausse au 1er essai → un indice (la carte est barrée), il réessaie ; fausse au 2e → la réponse ; incomprise → « redis-le ».
   */
  const reagirObservation = useCallback((correct: boolean | null, rep: { carte?: number; texte: string; micro: boolean; retour?: ReactionPreparee }) => {
    const o = observation, e = obsRef.current;
    if (!o || !e) return;
    const tour = tourObs.current;
    const entendu = rep.micro ? rep.texte : e.entendu;
    if (correct === null) {
      ressentir('think');
      setObs({ ...e, etape: 'observe', entendu, cartes: true, verdict: { correct: null, ecrit: rep.retour?.ecrit || 'Je n’ai pas bien compris : redis-le, ou choisis une carte.' } });
      void direRetour(rep.retour);
      return;
    }
    const prepare = (i?: number) => (i === undefined ? undefined : o.retours?.[i]);
    void appelerApi('/course-player/acquis', {
      slide_id: slide.id, slide_title: slide.title, deck_id: deckId, cle: 'obs', type: 'observation', enonce: o.enonce.slice(0, 300),
      reponse: rep.texte.slice(0, 300), tentative: e.essai, correct, reaction_preparee: !rep.micro && !!prepare(rep.carte),
      methodes: { visuel: visuel?.kind || 'aucun', observation: true, micro: rep.micro, eleve_a_manipule: eleveATouche.current },
    }).catch(() => { /* le suivi ne doit jamais gêner l'élève */ });
    if (correct) {
      // juste : le retour préparé de la bonne carte (voix du cours) passe avant celui du serveur
      const retour = prepare(o.bonne) || rep.retour;
      ressentir(e.essai <= 1 ? 'celebrate' : 'encourage');
      setObs({ ...e, etape: 'fini', entendu, bonneMontree: true, verdict: { correct: true, ecrit: retour?.ecrit || 'Oui, c’est bien ça !' } });
      void direRetour(retour).then(() => finirObservation(tour));
      return;
    }
    const exclus = rep.carte !== undefined && !e.exclus.includes(rep.carte) ? [...e.exclus, rep.carte] : e.exclus;
    if (e.essai < 2) {
      const retour = (rep.micro ? rep.retour : prepare(rep.carte)) || rep.retour;
      ressentir('wrong');
      setObs({ ...e, etape: 'observe', essai: 2, exclus, entendu, cartes: true, verdict: { correct: false, ecrit: retour?.ecrit || 'Pas tout à fait : regarde encore la simulation.' } });
      void direRetour(retour);
      return;
    }
    const solution = o.solution || prepare(o.bonne);
    ressentir('encourage');
    setObs({ ...e, etape: 'fini', exclus, entendu, cartes: true, bonneMontree: true, verdict: { correct: false, ecrit: solution?.ecrit || `La réponse : ${o.choix[o.bonne]}.` } });
    void direRetour(solution).then(() => finirObservation(tour));
  }, [observation, slide.id, slide.title, deckId, visuel?.kind, ressentir, direRetour, finirObservation]);
  const repondreCarte = useCallback((i: number) => {
    const o = observation, e = obsRef.current;
    if (!o || !e || e.etape !== 'observe' || e.exclus.includes(i)) return;
    voixExplication.current = false; fileVoix.current = []; voixRef.current?.pause();
    reagirObservation(i === o.bonne, { carte: i, texte: o.choix[i], micro: false });
  }, [observation, reagirObservation]);
  /** Ce que l'élève a dit au micro de réponse : jugé comme RÉPONSE à la question d'observation (jamais une question libre). */
  const jugerReponseDite = useCallback(async (texte: string, tour: number) => {
    const o = observation, e = obsRef.current;
    if (!o || !e) return;
    setObs({ ...e, etape: 'juge', entendu: texte, erreur: undefined });
    ressentir('think');
    try {
      const r = await appelerApi<{ correct: boolean | null; parole: string; ecrit: string }>('/course-player/answer-reaction', {
        diapo: { title: slide.title, speech: parole },
        question: { type: 'qcm', enonce: `Question d'observation (ce que l'élève voit dans la simulation) : ${o.enonce}`, choix: o.choix, bonne: o.bonne },
        reponse: texte, tentative: e.essai, verdict: null,
      });
      if (tour !== tourObs.current) return;
      setObs(x => x && { ...x, etape: 'observe' });
      obsRef.current = { ...obsRef.current!, etape: 'observe' };
      reagirObservation(r.correct, { texte, micro: true, retour: { parole: r.parole, ecrit: r.ecrit } });
    } catch {
      if (tour !== tourObs.current) return;
      setObs(x => x && { ...x, etape: 'observe', cartes: true, erreur: 'Le professeur n’a pas pu juger ta réponse : choisis une carte.' });
    }
  }, [observation, slide.title, parole, ressentir, reagirObservation]);
  const arreterMicroReponse = useCallback(() => {
    obsAppui.current = false;
    window.clearTimeout(obsLimite.current);
    if (obsRec.current?.state === 'recording') obsRec.current.stop();
  }, []);
  /** Le micro de RÉPONSE, maintenu comme un talkie-walkie : le tuteur se tait et écoute, la main à l'oreille. */
  const demarrerMicroReponse = useCallback(async () => {
    const e = obsRef.current;
    if (!e || e.etape !== 'observe' || obsAppui.current || obsRec.current?.state === 'recording') return;
    obsAppui.current = true;
    const tour = tourObs.current;
    voixExplication.current = false; fileVoix.current = []; voixRef.current?.pause();
    setObs(x => x && { ...x, etape: 'ecoute', erreur: undefined });
    const revenir = (erreur: string) => setObs(x => x && { ...x, etape: 'observe', erreur });
    try {
      const flux = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (!obsAppui.current || tour !== tourObs.current) {
        flux.getTracks().forEach(t => t.stop());
        if (tour === tourObs.current) revenir('Garde le bouton appuyé pendant que tu parles, puis relâche.');
        return;
      }
      const rec = new MediaRecorder(flux);
      const morceaux: Blob[] = [];
      rec.ondataavailable = ev => { if (ev.data.size) morceaux.push(ev.data); };
      rec.onstop = async () => {
        flux.getTracks().forEach(t => t.stop());
        if (tour !== tourObs.current) return;
        if (performance.now() - obsDebut.current < 500) { revenir('Garde le bouton appuyé pendant que tu parles, puis relâche.'); return; }
        setObs(x => x && { ...x, etape: 'transcrit' });
        const blob = new Blob(morceaux, { type: rec.mimeType || 'audio/webm' });
        const b64 = await new Promise<string>(ok => { const fr = new FileReader(); fr.onload = () => ok(String(fr.result)); fr.readAsDataURL(blob); });
        try {
          const { texte } = await appelerApi<{ texte: string }>('/course-player/transcrire', { audio_b64: b64 });
          if (tour !== tourObs.current) return;
          if (!texte?.trim()) { revenir('Je n’ai rien entendu : réessaie, ou choisis une carte.'); return; }
          obsRef.current = { ...obsRef.current!, etape: 'observe' };
          void jugerReponseDite(texte.trim(), tour);
        } catch (err) {
          if (tour !== tourObs.current) return;
          const m = (err as Error).message;
          setObs(x => x && { ...x, etape: 'observe', cartes: true, erreur: /^\d+$/.test(m) ? 'La transcription n’a pas abouti : choisis une carte.' : m });
        }
      };
      rec.start(); obsRec.current = rec; obsDebut.current = performance.now();
      obsLimite.current = window.setTimeout(arreterMicroReponse, 30_000);   // une réponse courte : 30 s au plus
    } catch {
      obsAppui.current = false;
      setObs(x => x && { ...x, etape: 'observe', cartes: true, erreur: 'Le micro n’est pas disponible : choisis une carte.' });
    }
  }, [arreterMicroReponse, jugerReponseDite]);

  // Pause de la voix = pause de la simulation : l'élève ne rate rien.
  const basculer = useCallback(() => {
    const audio = audioRef.current;
    if (predictionEnCours) { setPanneau('questions'); return; }   // la voix attend la prédiction
    if (obsRef.current) { fermerObservation(); return; }          // ▶ pendant une observation : la voix reprend
    if (!audio) return;
    if (audio.paused) { void audio.play(); if (demarree.current) envoyerASim('resume'); }
    else { audio.pause(); if (demarree.current) envoyerASim('pause'); }
  }, [envoyerASim, predictionEnCours, fermerObservation]);

  const reecouter = useCallback(() => {
    const audio = audioRef.current;
    if (predictionEnCours) { setPanneau('questions'); return; }
    if (!audio) return;
    dejaFaits.current = new Set(); demarree.current = false; setFinie(false);
    if (conc.demarrer) envoyerASim('reset');
    audio.currentTime = 0; void audio.play();
  }, [conc.demarrer, envoyerASim, predictionEnCours]);

  // ── « Suite → » : l'élève décide quand avancer (11 novembre 2026) ──
  /** La prédiction est faite : le tableau se ferme, la voix et la simulation montrent la réponse. */
  const lancerVoixApresPrediction = useCallback(() => {
    voixExplication.current = false; fileVoix.current = [];
    voixRef.current?.pause();
    setPredictionClose(slide.id); setIndexQuestion(0); setPanneau(null);
    const audio = audioRef.current;
    if (audio && piste?.url) { audio.currentTime = 0; void audio.play(); }
    else if (questions.length) setPanneau('questions');      // sans piste : les exercices de la diapositive
  }, [slide.id, piste?.url, questions.length]);
  const toutVisible = finie || !piste?.url;
  const listeAuTableau = enReprise ? jumelles.questions : questions;
  /** Ce que fait « Suite → » maintenant (recalculé à chaque rendu : questions finies, cycle, voix, tableau). */
  const etapeSuite = ((): EtapeSuite => {
    const e = etapeSuiteDeLaDiapo();
    // la diapositive termine un bloc : « Suite → » ouvre le cahier du bloc (le cahier n'est plus facultatif)
    return e.quoi === 'diapo' && finDeBloc && onFermerBloc ? { quoi: 'bloc', pret: e.pret } : e;
  })();
  function etapeSuiteDeLaDiapo(): EtapeSuite {
    const occupe = !!reaction || !!tableauProf || panneau === 'question_eleve' || !!obs;
    const pret = (e: EtapeSuite): EtapeSuite => ({ ...e, pret: e.pret && !occupe });
    if (predictionEnCours) return pret({ quoi: 'voix', pret: predictionRepondue === slide.id });
    if (cycle?.phase === 'attente') return { quoi: 'rien', pret: false };
    if (cycle?.phase === 'explique') return { quoi: 'jumelle', pret: false };
    if (cycle?.phase === 'final') return pret({ quoi: 'diapo', pret: true });
    if (!toutVisible) return { quoi: 'diapo', pret: false };          // la voix parle encore : passer à la main
    const restantes = listeAuTableau.filter(q => !(q.cle in finies.current));
    if (restantes.length) {
      if (panneau !== 'questions') return { quoi: 'ouvrir', pret: false };
      const courante = listeAuTableau[Math.min(indexQuestion, listeAuTableau.length - 1)];
      if (courante && courante.cle in finies.current) return pret({ quoi: 'question', pret: true });
      return { quoi: restantes.length > 1 ? 'question' : 'diapo', pret: false };
    }
    if (enReprise) {
      const justes = listeAuTableau.every(q => finies.current[q.cle]);
      return pret({ quoi: justes || (cycle?.n ?? MAX_CYCLES) >= MAX_CYCLES ? 'diapo' : 'reprise', pret: true });
    }
    if (questions.some(q => finies.current[q.cle] === false)) return pret({ quoi: 'reprise', pret: true });
    return pret({ quoi: 'diapo', pret: true });
  }
  const faireSuite = () => {
    setRelance(false);
    if (obsRef.current) { fermerObservation(); return; }   // « Suite → » pendant une observation : elle est passée
    switch (etapeSuite.quoi) {
      case 'voix': lancerVoixApresPrediction(); return;
      case 'ouvrir': setPanneau('questions'); return;
      case 'question': {
        // la question suivante non répondue (après la courante, sinon la première)
        const i = Math.min(indexQuestion, listeAuTableau.length - 1);
        const libre = (j: number) => j !== i && !(listeAuTableau[j].cle in finies.current);
        const k = listeAuTableau.findIndex((_, j) => j > i && libre(j));
        setIndexQuestion(k >= 0 ? k : Math.max(0, listeAuTableau.findIndex((_, j) => libre(j))));
        return;
      }
      case 'jumelle':
        voixRef.current?.pause();
        setCycle(c => c && c.phase === 'explique' ? { ...c, phase: 'question' } : c); setIndexQuestion(0); setPanneau('questions');
        return;
      case 'reprise': {
        if (cycle && enReprise) { void lancerCycle(cycle.n + 1, cycle.depuis); return; }
        const ratee = questions.find(q => finies.current[q.cle] === false);
        if (ratee) void lancerCycle(1, ratee);
        return;
      }
      case 'diapo': passerALaDiapoSuivante(etapeSuite.pret); return;
      case 'bloc':
        // comme un changement de diapositive (voix arrêtée, tableau fermé), puis la fin du bloc par-dessus
        voixExplication.current = false; fileVoix.current = [];
        voixRef.current?.pause(); audioRef.current?.pause();
        setPanneau(null);
        if (etapeSuite.pret) setCycle(null);
        onFermerBloc?.();
        return;
      default: return;
    }
  };
  // Le passage seul (après une réponse, sa réaction et sa démonstration) : seulement vers la question suivante, la
  // diapositive suivante ou la voix après une prédiction — jamais une reprise ni une fin de bloc.
  useEffect(() => {
    if (!tourSuiteSeule || panneau !== 'questions' || enReprise || cycle) return;
    if (etapeSuite.pret && (etapeSuite.quoi === 'question' || etapeSuite.quoi === 'diapo' || etapeSuite.quoi === 'voix')) faireSuite();
  // eslint-disable-next-line react-hooks/exhaustive-deps -- un passage par signal
  }, [tourSuiteSeule]);
  // Changer de diapositive annule un passage en attente.
  useEffect(() => { suiteSeule.current += 1; }, [slide.id]);
  // Un long silence alors que « Suite → » attend : le tuteur relance doucement, une seule fois par diapositive —
  // sa phrase préenregistrée si elle existe, sinon le bouton clignote. Toute action de l'élève remet le compte à zéro.
  useEffect(() => {
    if (!etapeSuite.pret || relanceFaite.current) return;
    let id = 0, actif = true;
    const parle = () => { const v = voixRef.current, a = audioRef.current; return (!!v && !v.paused && !v.ended) || (!!a && !a.paused && !a.ended); };
    const relancer = async () => {
      if (!actif) return;
      if (parle()) { armer(); return; }          // le tuteur parle encore : on attend la fin
      relanceFaite.current = true;
      if (await clipExiste(CLIP_RELANCE)) { if (actif && !parle()) { ressentir('encourage'); jouer(CLIP_RELANCE); } }
      else if (actif) setRelance(true);
    };
    const armer = () => { window.clearTimeout(id); id = window.setTimeout(() => void relancer(), RELANCE_APRES_MS); };
    armer();
    window.addEventListener('pointerdown', armer); window.addEventListener('keydown', armer);
    return () => { actif = false; window.clearTimeout(id); window.removeEventListener('pointerdown', armer); window.removeEventListener('keydown', armer); };
  }, [etapeSuite.pret, etapeSuite.quoi, slide.id, ressentir, jouer]);

  /** Ce que l'OCR d'une photo doit savoir : la diapositive et le cours (symboles, unités, notation du chapitre). */
  const contexteOcr: ContexteOcr = { deck_id: deckId, title: slide.title, lead: contenu.lead || '' };
  /** La voix de l'énoncé et la diapositive (suggestions du clavier), pour chaque tableau de questions. */
  const outilsEnonce = { lireEnonce, arreterEnonce, slideId: slide.id };
  /** Le panneau « Ton résultat » : ce qui est déjà dit (donc écrit), au fil de la voix. */
  const vuDuResultat = (() => {
    const r = reaction;
    if (!r || r.phase !== 'question') return { phrases: 0, question: false };
    const n = r.phrases.length;
    if (r.voix === 'fini') return { phrases: n, question: true };
    if (r.voix === 'prepare') return { phrases: 0, question: false };
    if (r.voix === 'sansvoix') {
      const k = Math.floor((performance.now() - r.debut) / 2200) + 1;
      return { phrases: Math.min(n, k), question: k > n };
    }
    const p = progressionMorceaux() ?? r.nTotal;
    const part = Math.min(1, p / Math.max(1, r.nParole));
    return { phrases: Math.min(n, Math.floor(part * n * 1.1) + 1), question: r.nTotal > r.nParole && p >= r.nParole };
  })();
  const cahier = (conc.cahier || contenu.student_trace || contenu.essential_text || '').trim();
  const exercices = slide.exercises || [];
  const surSim = visuel?.kind === 'simulation';

  return (
    <div data-scene-cours className="relative h-full w-full flex flex-col text-white" style={{ background: '#12241c' }}>
      <style>{ANIMATIONS}</style>
      {piste?.url && (
        <audio
          key={piste.url}
          ref={audioRef}
          src={piste.url}
          // une prédiction à faire : la voix attend que l'élève ait répondu et appuyé sur « Suite → »
          autoPlay={!predictionEnCours}
          preload="auto"
          // La bouche du tuteur suit le SON de la piste (analyseur partagé), pas seulement l'état « il parle ».
          onPlay={event => { setEnLecture(true); void audioUnlock.ensureRunning(); observeAvatarMedia(event.currentTarget); }}
          onPause={() => setEnLecture(false)}
          // en plus de chaque image : un onglet caché n'a plus d'images, et l'arrêt d'une question d'observation ne doit pas être dépassé
          onTimeUpdate={event => setTemps(event.currentTarget.currentTime)}
          onLoadedMetadata={event => { const d = event.currentTarget.duration; if (Number.isFinite(d) && d > 0) setDuree(d); }}
          // la bulle du cahier s'ouvre à la demande ; les questions, elles, s'affichent tout de suite
          onEnded={() => { setEnLecture(false); setFinie(true); iframeRef.current?.contentWindow?.postMessage({ type: 'simulation_manifest_request' }, '*'); if (conc.acquis) direLesLacunes(); if (questions.length && !reactionRef.current && !(observation && !obsFaite.current) && !legendeEnCours()) setPanneau('questions'); }}
        />
      )}
      <audio ref={voixRef} onPlay={event => { setVoixParle(true); void audioUnlock.ensureRunning(); observeAvatarMedia(event.currentTarget); }} onPause={() => setVoixParle(false)}
        onEnded={() => {
          setVoixParle(false);
          void morceauFini();
        }} />

      {/* ── Le titre et le sous-titre, seulement ── */}
      {/* Avec une simulation, titre et sous-titre tiennent sur une seule ligne (15 novembre 2026 : « la simulation n'occupe
          qu'une bande étroite ») : la hauteur gagnée va au tableau de la simulation. */}
      <header className={`shrink-0 text-center ${surSim ? 'flex flex-wrap items-baseline justify-center gap-x-4 px-4 pt-1 pb-0.5' : 'px-6 pt-2 pb-1'}`}
        style={tuteur3D ? { paddingRight: COLONNE_TUTEUR } : undefined}>
        <h1 className="text-xl leading-tight md:text-[26px]" style={{ fontFamily: CRAIE, color: '#fef3c7' }}>{slide.title}</h1>
        {/* pendant une question d'observation, le sous-titre se tait : il dit souvent la réponse (« la lumière s'étale ») */}
        {contenu.lead && (
          <p className="text-sm leading-snug md:text-base text-white/70 transition-opacity" style={{ fontFamily: CRAIE, opacity: obs && obs.etape !== 'fini' ? 0 : 1 }}>{contenu.lead}</p>
        )}
      </header>

      {/* ── Au centre : ce qu'on regarde ── */}
      <main className="relative flex-1 min-h-0 flex flex-col items-center justify-center gap-2 px-3 pb-1"
        style={tuteur3D ? { paddingRight: COLONNE_TUTEUR } : undefined}>   {/* la colonne de droite est au tuteur 3D */}
        {/* ── Le deuxième tableau : les questions descendent du haut et couvrent la scène, tout tient sans défiler ── */}
        {panneau === 'questions' && (
          <section className="tableau-questions absolute inset-y-0 left-3 z-30 flex flex-col overflow-hidden rounded-2xl border-2 border-amber-200/40 bg-[#0f2219] shadow-2xl"
            // sur téléphone, le tableau prend toute la largeur (la colonne du tuteur lui laissait 150 px)
            style={{ right: (tuteur3D && !etroit ? COLONNE_TUTEUR + 4 : 12) + placeClavier, bottom: basClavier, transition: 'right .25s ease, bottom .25s ease' }}>
            <div className="flex shrink-0 items-center justify-between border-b border-amber-200/20 px-4 py-2">
              <div className="text-base font-semibold text-emerald-200" style={{ fontFamily: CRAIE }}>
                {predictionEnCours ? '🔮 Avant d’expliquer : que prévois-tu ?' : cycle?.phase === 'final' ? `📓 La réponse · reprise ${cycle.n}/${MAX_CYCLES}` : enReprise ? `↻ Reprise ${cycle!.n}/${MAX_CYCLES} · ${jumelles.questions.length > 1 ? 'vrai ou faux' : 'nouvelle question'}` : `✏️ À toi · ${questions.length} question${questions.length > 1 ? 's' : ''}`}
              </div>
              <div className="flex items-center gap-3">
                {/* le tableau des questions couvre la scène : le bouton du résultat clignote dans son en-tête */}
                {resultat && !reaction && <BoutonResultat onClick={() => void ouvrirResultat()} />}
                <button onClick={fermerPanneau} className="text-white/50 hover:text-white text-xl" aria-label="Revenir à la scène">×</button>
              </div>
            </div>
            {cycle?.phase === 'final' ? (
              <div className="flex min-h-0 flex-1 flex-col justify-center gap-4 p-5" style={{ fontFamily: CRAIE }}>
                <p className="text-lg text-white/85"><Formule t={cycle.data?.ecrit || ''} /></p>
                {cycle.data?.cahier && <p className="rounded-xl border border-amber-200/40 px-4 py-3 text-xl text-amber-100">📓 À écrire dans le cahier : <Formule t={cycle.data.cahier} /></p>}
                <p className="text-sm text-white/55">Cette notion est notée « à reprendre » : le professeur y reviendra autrement, en mode libre et au prochain cours.</p>
              </div>
            ) : predictionEnCours && prediction ? (
              // La prédiction : sa réaction préparée, pas de démonstration (la voix qui suit montre la réponse).
              <QuestionsDeLaDiapo key={`${slide.id}:prediction`} questions={[prediction]} index={0} onIndex={() => {}} diapo={{ title: slide.title, speech: parole, memoire: memoireDiapo }} dire={dire} jouer={jouer} reponses={conc.reponses} onReponse={enregistrerPrediction} onFinie={surPredictionFinie}
                onPasser={(c, f) => surPredictionFinie(c, null, f)} contexte={contexteOcr} {...outilsEnonce} />
            ) : enReprise ? (
              <QuestionsDeLaDiapo key={`cycle${cycle!.n}`} questions={jumelles.questions} index={indexQuestion} onIndex={setIndexQuestion} diapo={{ title: slide.title, speech: parole, memoire: memoireDiapo }} dire={dire} jouer={jouer} reponses={jumelles.preparees} onReponse={enregistrerReponse} onFinie={surFinie} essaisMax={1}
                contexte={contexteOcr} {...outilsEnonce} />
            ) : (
              <QuestionsDeLaDiapo key={slide.id} questions={questions} index={indexQuestion} onIndex={setIndexQuestion} diapo={{ title: slide.title, speech: parole, memoire: memoireDiapo }} dire={dire} jouer={jouer} reponses={conc.reponses} onReponse={enregistrerReponse} onFinie={surFinie} onPasser={surPassee}
                contexte={contexteOcr} lireDemo={lireDemonstration} preparerDemo={preparerDemo} attendreVoix={attendreVoix} {...outilsEnonce} />
            )}
          </section>
        )}
        {visuel && (
          <div
            ref={visuelRef}
            className="relative w-full flex-1 min-h-0 flex items-center justify-center"
            // la simulation prend toute la place (12 novembre 2026) ; une image garde sa largeur de lecture
            style={{ maxWidth: surSim ? undefined : 900 }}
          >
            {surSim && visuel.url && (
              <iframe
                key={visuel.url}
                ref={iframeRef}
                title="Simulation"
                // Nos propres pages (/media/simulations) : même origine, sinon le panneau de test les bloque.
                sandbox="allow-scripts allow-same-origin allow-modals allow-downloads"
                src={visuel.url}
                scrolling="no"
                className="h-full w-full border-0 bg-transparent"
                // les tableaux à la craie se redessinent à la taille du cadre : ils remplissent la zone ; les autres
                // simulations (dessinées pour 760 × 470) gardent leur format
                style={/-tableau\//.test(visuel.url) ? undefined : { aspectRatio: '760 / 470', maxHeight: '100%' }}
                onLoad={() => window.setTimeout(() => setSimPrete(true), 700)}
              />
            )}
            {visuel.kind === 'image' && visuel.url && (
              <img src={visuel.url} alt={visuel.alt || contenu.alt || ''} className="max-h-full max-w-full object-contain" />
            )}
          </div>
        )}

        {/* ── La question d'observation : sous la figure, sans la couvrir ; ses cartes et son micro dans la même bande ── */}
        {obs && observation && (
          <BandeObservation o={observation} e={obs} etroit={etroit} onCarte={repondreCarte} onCartes={() => setObs(x => x && { ...x, cartes: true })}
            onMicro={() => void demarrerMicroReponse()} onMicroFin={arreterMicroReponse} onPasser={fermerObservation} />
        )}

        {/* ── La question de l'élève expliquée au tableau ── */}
        {/* Grand tableau devant la diapositive, toujours (user rule, 12 novembre 2026) : plus de petit cadre sous la figure. */}
        {tableauProf && (
          <div className="absolute inset-y-0 left-3 z-30 flex flex-col pb-2" style={{ right: tuteur3D ? COLONNE_TUTEUR + 4 : 12 }}>
            <TableauDuProf t={tableauProf!} lignesRef={lignesProfRef} plein onFini={exerciceFini} onTexte={() => setTableauProf(t => t && { ...t, texte: !t.texte })}
              onAutre={autreQuestion} onContinuer={reprendreApresQuestion} />
          </div>
        )}
        {annonce && (
          <div className="pointer-events-none absolute inset-x-0 top-3 z-30 flex justify-center" style={tuteur3D ? { paddingRight: COLONNE_TUTEUR } : undefined}>
          <div className="tableau-questions w-[min(92%,640px)] rounded-2xl border-2 border-amber-200/40 bg-[#0f2219] px-5 py-4 text-center shadow-2xl"
            style={{ fontFamily: CRAIE }}>
            {annonce.mode === 'suivante' ? (
              <>
                <p className="craie-ecrit text-xl text-amber-100">📌 {annonce.notion || 'Cette notion'} : on la traite bientôt</p>
                {annonce.titre && <p className="craie-ecrit mt-1 text-lg text-cyan-200" style={{ animationDelay: '.9s' }}>→ diapo « {annonce.titre} »</p>}
                <p className="mt-2 text-sm text-white/60">Maintenant, concentrons-nous sur cette partie.</p>
              </>
            ) : (
              <>
                <p className="craie-ecrit text-xl text-rose-200">Cette question n’est pas dans ce cours{annonce.notion ? ` (${annonce.notion})` : ''}.</p>
                <p className="mt-2 text-sm text-white/60">On revient à notre leçon.</p>
              </>
            )}
          </div>
          </div>
        )}

        {!visuel && table && (
          <table className="w-full max-w-4xl border-collapse text-base md:text-lg" style={{ fontFamily: CRAIE }}>
            <thead>
              <tr>{table.headers.map((h, i) => (
                <th key={i} className="border border-white/25 px-3 py-2 text-left" style={{ color: '#a5f3fc' }}>{h}</th>
              ))}</tr>
            </thead>
            <tbody>
              {table.rows.map((ligne, r) => (
                <tr key={r} ref={el => { lignesRef.current[r] = el; }}>
                  {ligne.map((cellule, c) => <td key={c} className="border border-white/20 px-3 py-2"><Formule t={cellule} /></td>)}
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* Avec une figure, les formules du centre vont dans une bande SOUS la figure, jamais par-dessus (user rule,
            13 novembre 2026 : « ces équations masquent les simulations ») ; la place est gardée dès le début, la figure
            ne saute pas quand une formule apparaît. */}
        {centre.length > 0 && (
          <div className={`flex ${visuel ? 'pointer-events-none w-full shrink-0 flex-row flex-wrap justify-center gap-2' : table ? 'flex-row flex-wrap justify-center gap-3' : 'flex-col items-center gap-4'}`}
            style={visuel && tuteur3D ? { paddingRight: COLONNE_TUTEUR } : undefined}>
            {centre.map((c, i) => {
              const vu = toutVisible || temps >= c.t;
              return (
                <div
                  key={i}
                  ref={el => { centreRef.current[i] = el; }}
                  className="rounded-xl px-4 py-2 transition-all duration-700"
                  style={{
                    fontFamily: CRAIE,
                    fontSize: visuel ? 20 : table ? 22 : 30,
                    color: '#fef9c3',
                    border: '1px dashed rgba(254,249,195,0.35)',
                    background: visuel ? 'rgba(15,34,25,0.92)' : undefined,
                    opacity: vu ? 1 : 0,
                    transform: vu ? 'none' : 'translateY(8px)',
                  }}
                >
                  <Formule t={c.texte} />
                </div>
              );
            })}
          </div>
        )}

        {/* ── Le schéma légendé : le commentaire écrit du tuteur, en bas du tableau, sans couvrir le schéma ── */}
        {legendeMot && panneau !== 'questions' && (
          <p className={`absolute bottom-2 left-1/2 z-20 max-w-[80%] -translate-x-1/2 rounded-xl border px-4 py-2 text-center text-lg ${
            legendeMot.correct === true ? 'border-emerald-400/60 bg-emerald-950/85 text-emerald-100' : legendeMot.correct === false ? 'border-rose-400/60 bg-rose-950/85 text-rose-100' : 'border-amber-300/50 bg-slate-900/85 text-amber-100'}`}
            style={{ fontFamily: CRAIE }}>
            {legendeMot.correct === true ? '✔ ' : legendeMot.correct === false ? '✘ ' : ''}{legendeMot.texte}
          </p>
        )}

        {/* ── Un nouveau résultat de l'élève : rien ne s'ouvre, ce bouton clignote ; le cours continue ── */}
        {resultat && !reaction && panneau !== 'questions' && (
          // dans le coin bas-gauche du tableau : au-dessus de la barre, sans couvrir la figure ni les formules du centre
          <BoutonResultat onClick={() => void ouvrirResultat()} className="absolute bottom-2 left-3 z-20" />
        )}

        {!visuel && !table && centre.length === 0 && (
          <p className="text-white/40 text-lg" style={{ fontFamily: CRAIE }}>Écoute le professeur…</p>
        )}
      </main>

      {/* ── Les bulles : l'écrit, fermé par défaut ── */}
      {panneau && panneau !== 'questions' && (
        <div style={tuteur3D && !etroit ? { right: COLONNE_TUTEUR + placeClavier } : placeClavier ? { right: placeClavier } : undefined} data-bulle className="absolute left-4 right-4 bottom-[76px] z-30 mx-auto max-w-3xl max-h-[55%] overflow-y-auto rounded-2xl border border-white/15 bg-[#0d1c15]/95 p-5 shadow-2xl backdrop-blur">
          <button onClick={fermerPanneau} className="absolute right-3 top-2 text-white/50 hover:text-white text-xl" aria-label="Fermer">×</button>
          {panneau === 'cahier' && (
            <>
              <div className="text-sm font-semibold text-amber-200">📓 À écrire dans le cahier</div>
              {/* Le cahier s'organise comme un cours préparé : le titre du cours (premier écran), la partie numérotée quand on
                  y entre, puis le titre de la diapositive numéroté, puis les lignes (12 novembre 2026). */}
              {entete?.cours && (
                <div className="mt-2 text-center">
                  <h2 className="text-3xl underline decoration-amber-200/50 decoration-2 underline-offset-8" style={{ fontFamily: CRAIE, color: '#fde68a' }}>{entete.cours.titre}</h2>
                  {entete.cours.sousTitre && <p className="mt-2 text-lg italic" style={{ fontFamily: CRAIE, color: '#e7e5c9' }}>{entete.cours.sousTitre}</p>}
                </div>
              )}
              {entete?.partie && <h3 className="mt-3 text-2xl" style={{ fontFamily: CRAIE, color: '#fca5a5' }}>{entete.partie}</h3>}
              <h4 className={`mt-2 text-xl underline decoration-amber-200/40 underline-offset-4 ${entete ? 'pl-4' : ''}`} style={{ fontFamily: CRAIE, color: '#fef3c7' }}>{entete?.diapo || slide.title}</h4>
              {contenu.lead && <p className={`mt-1 text-base italic ${entete ? 'pl-4' : ''}`} style={{ fontFamily: CRAIE, color: '#e7e5c9' }}>{contenu.lead}</p>}
              {cahier && cahier !== contenu.lead && <p className={`mt-2 text-lg leading-relaxed ${entete ? 'pl-4' : ''}`} style={{ fontFamily: CRAIE, color: '#fef3c7' }}><Formule t={cahier} /></p>}
              {/* les dessins du cahier (courbe, schéma, croquis légendés), sous le texte */}
              <FiguresCahier figures={conc.cahier_figures} compact className={`mt-3 ${entete ? 'pl-4' : ''}`} />
              {centre.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                  {centre.filter(c => /=/.test(c.texte)).map((c, i) => (
                    <span key={i} className="rounded-lg border border-amber-200/30 px-3 py-1" style={{ fontFamily: CRAIE, color: '#fef9c3' }}><Formule t={c.texte} /></span>
                  ))}
                </div>
              )}
              <button onClick={() => { void navigator.clipboard?.writeText([entete?.cours?.titre, entete?.cours?.sousTitre, entete?.partie, entete?.diapo || slide.title, contenu.lead, cahier !== contenu.lead ? cahier : ''].filter(Boolean).join('\n')); }} className="mt-3 text-xs text-white/50 hover:text-white">Copier</button>
            </>
          )}
          {panneau === 'explication' && (
            <div style={{ fontFamily: CRAIE }} className="text-lg leading-relaxed">
              <div className="text-sm font-semibold text-cyan-200" style={{ fontFamily: 'inherit' }}>📖 Explication écrite</div>
              {contenu.lead && <p className="mt-2 text-white/80">{contenu.lead}</p>}
              {(contenu.bullets || []).length > 0 && (
                <ul className="mt-2 list-disc pl-6 space-y-1">{contenu.bullets!.map((b, i) => <li key={i}><Formule t={b} /></li>)}</ul>
              )}
              {contenu.essential_text && <p className="mt-3 rounded-lg border border-emerald-300/30 px-3 py-2 text-emerald-100"><Formule t={contenu.essential_text} /></p>}
              {visuel && table && (
                <table className="mt-3 w-full border-collapse text-base">
                  <thead><tr>{table.headers.map((h, i) => <th key={i} className="border border-white/25 px-2 py-1 text-left text-cyan-200">{h}</th>)}</tr></thead>
                  <tbody>{table.rows.map((l, r) => <tr key={r}>{l.map((c, k) => <td key={k} className="border border-white/20 px-2 py-1"><Formule t={c} /></td>)}</tr>)}</tbody>
                </table>
              )}
              {parole && (
                <details className="mt-4 text-base text-white/60">
                  <summary className="cursor-pointer text-sm">Ce que dit le professeur</summary>
                  <p dir="auto" className="mt-2 whitespace-pre-wrap">{parole}</p>
                </details>
              )}
            </div>
          )}
          {panneau === 'exercices' && <Exercices exercices={exercices} />}
          {panneau === 'question_eleve' && (
            <div style={{ fontFamily: CRAIE }}>
              <div className="text-sm font-semibold text-sky-200">🙋 Ta question au professeur</div>
              {libre.phase !== 'reponse' && (
                <>
                  <div className="relative mt-2">
                    <textarea ref={champQuestion} value={libre.texte} onChange={e => setLibre(l => ({ ...l, texte: e.target.value }))} onFocus={toucherQuestion} disabled={libre.phase === 'envoi' || libre.transcrit} rows={2}
                      placeholder={libre.transcrit ? 'Transcription de ce que tu as dit…' : 'Écris ta question… (en darija ou en français)'} dir="auto"
                      className="w-full resize-none rounded-lg border border-white/20 bg-black/30 px-3 py-2 pr-24 text-lg outline-none focus:border-sky-300" />
                    {/* Transcription fausse : on efface tout d'un geste et on recommence (au micro ou au clavier). */}
                    {libre.texte.trim() && !libre.transcrit && libre.phase === 'saisie' && (
                      <button type="button" onClick={() => setLibre(l => ({ ...l, texte: '', aVerifier: false, erreur: undefined }))}
                        className="absolute right-2 top-2 rounded-full bg-white/10 px-3 py-1 text-xs text-white/70 hover:bg-rose-500/30 hover:text-white"
                        aria-label="Effacer le texte">✕ Effacer</button>
                    )}
                  </div>
                  <div className="mt-2 flex flex-wrap items-center gap-2">
                    <button
                      type="button" disabled={libre.phase === 'envoi' || libre.transcrit}
                      // appuyer pour parler, relâcher pour arrêter (souris, doigt, ou barre d'espace)
                      onPointerDown={e => { e.preventDefault(); e.currentTarget.setPointerCapture?.(e.pointerId); void demarrerMicro(); }}
                      onPointerUp={arreterMicro} onPointerCancel={arreterMicro} onLostPointerCapture={arreterMicro}
                      onKeyDown={e => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); void demarrerMicro(); } }}
                      onKeyUp={e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); arreterMicro(); } }}
                      onContextMenu={e => e.preventDefault()}
                      style={{ touchAction: 'none', userSelect: 'none', WebkitUserSelect: 'none' }}
                      className={`rounded-full px-4 py-2 text-sm ${libre.enregistre ? 'bg-rose-500/50 ring-2 ring-rose-300 animate-pulse' : 'bg-white/10 hover:bg-white/20'}`}>
                      {libre.enregistre ? '● Je t’écoute… relâche pour finir' : '🎙️ Maintiens pour parler'}
                    </button>
                    {libre.transcrit && <span className="text-sm text-sky-200 animate-pulse">✍️ Transcription…</span>}
                    {libre.audio && !libre.enregistre && !libre.transcrit && <span className="text-sm text-emerald-200">✔ enregistrement prêt</span>}
                    {/* 📷 Photo : la feuille est lue par l'OCR et le texte s'écrit dans le champ ; l'élève le corrige, puis envoie. */}
                    <BoutonPhoto contexte={contexteOcr} disabled={libre.phase === 'envoi' || libre.transcrit}
                      onTexte={t => setLibre(l => ({ ...l, texte: [l.texte.trim(), t].filter(Boolean).join('\n'), aVerifier: true, erreur: undefined }))}
                      onErreur={m => setLibre(l => ({ ...l, erreur: m }))} />
                    {clavierEtat.hotes > 0
                      ? <BoutonSymboles ouvert={clavierEtat.ouvert} onClick={() => { toucherQuestion(); clavier.basculer(); }} />
                      : <BoutonSymboles ouvert={clavierQuestion} onClick={() => setClavierQuestion(c => !c)} />}
                    {/* 🖼️ Image : un schéma, un exercice joint tel quel à la question (lu au serveur avec la question). */}
                    <label className="cursor-pointer rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20" title="Joindre une image (schéma, exercice) à ta question">
                      🖼️ {libre.image ? libre.image.nom.slice(0, 18) : 'Image'}
                      <input type="file" accept="image/*" className="hidden" disabled={libre.phase === 'envoi'}
                        onChange={async e => { const f = e.target.files?.[0]; if (!f) return; const b64 = await lireFichier(f); setLibre(l => ({ ...l, image: { b64, mime: f.type || 'image/png', nom: f.name } })); }} />
                    </label>
                    {libre.image && <img src={libre.image.b64} alt="" className="h-10 rounded border border-white/20" />}
                    <button onClick={() => void envoyerQuestion()} disabled={libre.phase === 'envoi' || libre.enregistre || libre.transcrit || (!libre.texte.trim() && !libre.audio && !libre.image)}
                      className="ml-auto rounded-full bg-sky-500/40 px-5 py-2 text-sm hover:bg-sky-500/50 disabled:opacity-40">
                      {libre.phase === 'envoi' ? 'Le professeur réfléchit…' : 'Envoyer'}
                    </button>
                  </div>
                  {clavierQuestion && clavierEtat.hotes === 0 && libre.phase === 'saisie' && (
                    <ClavierScientifique cible={champQuestion} valeur={libre.texte} onChange={v => setLibre(l => ({ ...l, texte: v }))} onFermer={() => setClavierQuestion(false)} />
                  )}
                  {libre.aVerifier && !libre.transcrit && libre.phase === 'saisie' && (
                    <p className="mt-2 text-sm text-sky-200/80">Vérifie ce que le professeur a compris ou lu ; corrige si besoin, puis Envoyer.</p>
                  )}
                  {libre.erreur && <p className="mt-2 text-sm text-rose-200">{libre.erreur}</p>}
                </>
              )}
              {libre.phase === 'reponse' && libre.reponse && (
                <>
                  {libre.reponse.question_comprise && <p className="mt-2 text-sm text-white/55">Ta question : « {libre.reponse.question_comprise} »</p>}
                  <p className="mt-2 text-base text-white/70">Le professeur te répond au tableau.</p>
                  <div className="mt-3 flex gap-2">
                    <button onClick={autreQuestion} className="rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20">Autre question</button>
                    <button onClick={reprendreApresQuestion} className="rounded-full bg-emerald-500/30 px-4 py-2 text-sm hover:bg-emerald-500/40">Continuer le cours</button>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      )}

      {/* ── La réaction du tuteur à ce que l'élève a fait lui-même ── */}
      {reaction && (
        <div style={tuteur3D && !etroit ? { right: COLONNE_TUTEUR } : undefined} data-bulle className="absolute left-4 right-4 bottom-[76px] z-40 mx-auto max-w-3xl max-h-[45%] overflow-y-auto rounded-2xl border border-cyan-300/30 bg-[#0d1c15]/95 p-5 shadow-2xl backdrop-blur">
          <div className="flex items-center justify-between">
            <div className="text-sm font-semibold text-cyan-200">🔎 Ton résultat</div>
            <button onClick={fermerResultat} className="text-white/50 hover:text-white text-xl" aria-label="Fermer et reprendre le cours">×</button>
          </div>
          {(reaction.phase === 'reflechit' || (reaction.phase === 'question' && reaction.voix === 'prepare')) && <p className="mt-2 text-white/70 animate-pulse">Le professeur regarde ton nouveau résultat…</p>}
          {reaction.phase === 'erreur' && (
            <>
              <p className="mt-2 text-rose-200">{reaction.message}</p>
              <button onClick={fermerResultat} className="mt-3 rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20">Continuer</button>
            </>
          )}
          {reaction.phase === 'question' && reaction.voix !== 'prepare' && (
            <QuestionSurResultat reaction={reaction} vu={vuDuResultat} onRepondre={c => void repondreResultat(c)} contexte={contexteOcr} />
          )}
        </div>
      )}

      {/* ── La barre du bas, hors de la scène ── */}
      {/* une seule ligne fine (12 novembre 2026) : boutons en icônes (le texte apparaît sur grand écran et au survol) */}
      {/* sur téléphone, la barre passe sur deux lignes (14 novembre 2026) : trop large, elle débordait et le lecteur défilait
          vers « Suite → » quand on le touchait — la fenêtre du cahier de fin de bloc s'ouvrait alors hors de l'écran */}
      <footer ref={piedRef} data-pied-cours className="shrink-0 z-20 flex flex-wrap sm:flex-nowrap items-center gap-1.5 px-2 py-1.5 border-t border-white/10 bg-black/25">
        {piste?.url && (
          <>
            <button onClick={basculer} className="h-9 w-9 shrink-0 rounded-full bg-white/10 hover:bg-white/20" title={enLecture ? 'Pause' : 'Écouter'}>
              {enLecture ? '❚❚' : '▶'}
            </button>
            <button onClick={reecouter} className="h-9 w-9 shrink-0 rounded-full bg-white/10 hover:bg-white/20" title="Réécouter depuis le début">⟲</button>
            <div className="hidden sm:block min-w-[48px] max-w-[160px] flex-1 h-1.5 rounded-full bg-white/10 overflow-hidden">
              <div className="h-full bg-emerald-400/80" style={{ width: `${duree ? Math.min(100, (temps / duree) * 100) : 0}%` }} />
            </div>
          </>
        )}
        <Bulle actif={panneau === 'cahier'} pulse={toutVisible && panneau !== 'cahier' && !!cahier} onClick={() => basculerPanneau('cahier')} disabled={!cahier}>
          <Libelle icone="📓" texte="À écrire dans le cahier" />
        </Bulle>
        <Bulle actif={panneau === 'explication'} onClick={() => basculerPanneau('explication')}>
          <Libelle icone="📖" texte="Explication écrite" />
        </Bulle>
        <Bulle actif={panneau === 'question_eleve'} onClick={leverLaMain}>
          <Libelle icone="🙋" texte="Question" />
        </Bulle>
        {clavierEtat.hotes > 0 && (
          <Bulle actif={clavierEtat.ouvert} onClick={clavier.basculer}>
            <Libelle icone="⌨" texte="Clavier" />
          </Bulle>
        )}
        {(questions.length > 0 || predictionEnCours) && (
          <Bulle actif={panneau === 'questions'} pulse={(toutVisible || predictionEnCours) && panneau !== 'questions'} onClick={() => basculerPanneau('questions')}>
            {predictionEnCours ? '🔮 Prévois' : `✏️ À toi (${questions.length})`}
          </Bulle>
        )}
        <div className="ml-auto flex shrink-0 items-center gap-1.5">
          {deckControls}
          {/* Le seul bouton qui fait avancer le cours : mis en avant quand l'étape est finie ; il clignote à la relance. */}
          <button onClick={faireSuite} disabled={etapeSuite.quoi === 'rien'} data-suite={etapeSuite.quoi}
            title={etapeSuite.pret ? undefined : 'Passer à la suite'}
            className={`h-10 whitespace-nowrap rounded-full px-5 text-base font-semibold transition-colors disabled:opacity-40 ${etapeSuite.pret
              ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-900/40 hover:bg-emerald-400'
              : 'bg-white/10 text-white/60 hover:bg-white/20'} ${relance ? 'animate-pulse ring-2 ring-emerald-200' : ''}`}>
            {etapeSuite.quoi === 'bloc' ? '✍️ Au cahier →' : etapeSuite.quoi === 'diapo' && etapeSuite.pret ? libelleSuite : 'Suite →'}
          </button>
        </div>
      </footer>

      {tuteur3D && <AIAvatar isSpeaking={enLecture || voixParle} isProcessing={reaction?.phase === 'reflechit' || cycle?.phase === 'attente'} labControl={labControl} emotion={emotion} discret
        isListening={obs?.etape === 'ecoute'} mainOreille={obs?.etape === 'ecoute'} />}
    </div>
  );
}

/** Une question de la diapositive, telle que l'élève y répond (la clé `bonne` n'existe que pour les exercices). */
type QuestionDiapo = { cle: string; type: 'qcm' | 'vrai_faux' | 'directe'; enonce: string; choix?: string[]; bonne?: number; explication?: string;
  /** La démonstration manuscrite, écrite après la réaction (pour un vrai/faux : portée par sa dernière affirmation). */
  demonstration?: Demonstration;
  /** L'énoncé lu par le tuteur (`enonce_audio`, `enonce_dit`) et les suggestions du clavier (`clavier`). */
  lu?: EnonceLu };
const luDe = (x?: EnonceLu): EnonceLu | undefined => (x && (x.enonce_audio || x.enonce_dit || x.clavier) ? { enonce_audio: x.enonce_audio, enonce_dit: x.enonce_dit, clavier: x.clavier } : undefined);

function questionsDeLaDiapo(slide: CourseSlide): QuestionDiapo[] {
  const out: QuestionDiapo[] = [];
  const q = slide.question;
  if (q?.prompt) {
    if ((q.options || []).length >= 2) out.push({ cle: 'q', type: 'qcm', enonce: q.prompt, choix: q.options, bonne: q.correct, demonstration: q.demonstration, lu: luDe(q) });
    else out.push({ cle: 'q', type: 'directe', enonce: q.prompt, demonstration: q.demonstration, lu: luDe(q) });
  }
  (slide.exercises || []).forEach((ex, i) => {
    if (ex.type === 'qcm' && (ex.choices || []).length >= 2) out.push({ cle: `e${i}`, type: 'qcm', enonce: ex.prompt, choix: ex.choices, bonne: ex.correct ?? 0, explication: ex.explanation, demonstration: ex.demonstration, lu: luDe(ex) });
    if (ex.type === 'vrai_faux') (ex.statements || []).forEach((st, j, tout) => {
      out.push({ cle: `e${i}s${j}`, type: 'vrai_faux', enonce: st.text, choix: ['Vrai', 'Faux'], bonne: st.correct ? 0 : 1, explication: st.explanation,
        demonstration: j === tout.length - 1 ? ex.demonstration : undefined, lu: luDe(st) });
    });
  });
  return out;
}

/**
 * Plus aucune question AVANT l'explication (user rule, 13 novembre 2026 : « annuler cette étape de prévoir dans tous
 * les cours ») : le bandeau « 🔮 Avant d'expliquer : que prévois-tu ? » ne s'ouvre plus. Une question encore marquée
 * `prediction` est posée comme les autres, après la voix. Remettre `true` pour rétablir l'étape.
 */
const PREDICTIONS_AVANT_LA_VOIX = false;
const estPrediction = (slide: CourseSlide) => PREDICTIONS_AVANT_LA_VOIX && !!slide.question?.prediction;

/** La question de prédiction de la diapositive (`question.prediction`), sans démonstration : la voix montre la réponse. */
function questionDePrediction(slide: CourseSlide): QuestionDiapo | null {
  if (!estPrediction(slide)) return null;
  const q = questionsDeLaDiapo(slide).find(x => x.cle === 'q');
  return q ? { ...q, demonstration: undefined } : null;
}

/** L'état d'une question gardé pour l'élève (`localStorage`, clé `reponse:<deck>:<diapo>:<cle>`). */
type EtatQuestion = Partial<{ tentative: number; exclus: number[]; pris: number | null; retour: { correct: boolean | null; ecrit: string } | null; passee: boolean }>;
function lireEtatQuestion(memoire: string): EtatQuestion {
  try { return JSON.parse(localStorage.getItem(memoire) || '{}') as EtatQuestion; } catch { return {}; }
}
/** Une question est close : juste, fausse après tous ses essais, ou réponse libre jugée. */
function estTerminee(type: QuestionDiapo['type'], e: EtatQuestion, essaisMax: number): boolean {
  const r = e.retour, t = e.tentative ?? 1;
  return r?.correct === true || (r?.correct === false && t > essaisMax) || (type === 'directe' && !!r && r.correct !== null);
}

/**
 * Les questions de la diapositive, affichées dès la fin de la voix. Chaque réponse reçoit la réaction du tuteur,
 * dite à voix haute : juste → ce qui est juste et pourquoi ; fausse au 1er essai → un indice, et il réessaie ;
 * fausse au 2e → la réponse et sa justification. Chaque réponse possible a sa réaction PRÉPARÉE, avec sa voix
 * (`concentration.reponses`) : elle part tout de suite, sans serveur. Seule une réponse écrite librement passe
 * par `/course-player/answer-reaction` (DeepSeek) et la voix en direct.
 */
/** Ce que l'écran note à chaque réponse (suivi des acquis, skill `suivi-des-acquis`). */
export type ReponseNotee = { cle: string; type: QuestionDiapo['type'] | 'prediction'; enonce: string; reponse: string; tentative: number; correct: boolean | null; preparee: boolean;
  /** l'élève a passé la question : ni juste ni erreur (12 novembre 2026) */
  passee?: boolean };

/** Ce que le tableau des questions reçoit pour écrire les démonstrations et lire une photo. */
type OutilsQuestions = {
  contexte?: ContexteOcr; attendreVoix?: () => Promise<void>;
  lireDemo?: (d: Demonstration, prete?: VoixDemo | null) => LectureDemo; preparerDemo?: (d: Demonstration) => VoixDemo | null;
  /** le tuteur lit l'énoncé ; la lecture s'arrête quand l'élève répond ou passe */
  lireEnonce?: (q: QuestionDiapo) => void; arreterEnonce?: () => void;
  /** la diapositive (les suggestions du clavier sont cherchées par diapositive et question) */
  slideId?: string;
};

function QuestionsDeLaDiapo({ questions, index, onIndex, diapo, dire, jouer, reponses, onReponse, onFinie, onPasser, essaisMax, ...outils }: {
  questions: QuestionDiapo[];
  /** La question montrée : tenue par le tableau, elle ne change que par l'élève (« Suite → », points, flèches). */
  index: number; onIndex: (i: number) => void;
  diapo: { title: string; speech: string; memoire?: string }; dire: (texte: string) => Promise<boolean>;
  jouer: (url: string, secours?: string) => void; reponses?: SlideConcentration['reponses']; onReponse?: (r: ReponseNotee) => void;
  onFinie?: (cle: string, correct: boolean, fraiche: boolean, apresDemo?: boolean) => void; essaisMax?: number;
  /** l'élève passe la question (absent : pas de bouton « Passer », ex. la question jumelle d'une reprise) ; `fraiche` :
   *  à l'instant (false : passage retrouvé en mémoire) */
  onPasser?: (cle: string, fraiche?: boolean) => void;
} & OutilsQuestions) {
  // Une question à la fois, en carrousel (user rule, 8 novembre 2026) : l'élève répond, écoute la réaction, puis
  // passe à la suivante avec « Suite → » — jamais toute seule (11 novembre 2026, le rythme est celui de l'élève).
  // Toutes les questions restent montées : leur état ne se perd pas en changeant de page.
  const [finiesIci, setFiniesIci] = useState<Record<string, boolean>>({});
  const [passeesIci, setPasseesIci] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(questions.map(q => [q.cle, !!lireEtatQuestion(`reponse:${diapo.memoire || ''}:${q.cle}`).passee])));
  const surFinieLocale = useCallback((cle: string, correct: boolean, fraiche: boolean, apresDemo?: boolean) => {
    setFiniesIci(f => ({ ...f, [cle]: true }));
    setPasseesIci(f => ({ ...f, [cle]: false }));
    onFinie?.(cle, correct, fraiche, apresDemo);
  }, [onFinie]);
  // une question passée retrouvée (page rechargée) compte comme passée pour « Suite → »
  useEffect(() => { Object.entries(passeesIci).forEach(([cle, p]) => { if (p) onPasser?.(cle, false); }); }, []); // eslint-disable-line react-hooks/exhaustive-deps
  const surPasseeLocale = useCallback((cle: string) => {
    setPasseesIci(f => ({ ...f, [cle]: true }));
    onPasser?.(cle, true);
  }, [onPasser]);
  const n = questions.length;
  const courante = Math.min(index, Math.max(0, n - 1));

  return (
    <div className="flex min-h-0 flex-1 flex-col p-3" style={{ fontFamily: CRAIE }}>
      <div className="min-h-0 flex-1">
        {questions.map((q, i) => (
          <div key={q.cle} className={`question-apparait h-full min-h-0 ${i === courante ? '' : 'hidden'}`}>
            <UneQuestion q={q} diapo={diapo} dire={dire} jouer={jouer} preparees={reponses?.[q.cle]} onReponse={onReponse} onFinie={surFinieLocale} essaisMax={essaisMax}
              actif={i === courante} onPasser={onPasser ? surPasseeLocale : undefined} {...outils} />
          </div>
        ))}
      </div>
      {n > 1 && (
        <div className="mt-3 flex shrink-0 items-center justify-between">
          <button onClick={() => onIndex(Math.max(0, courante - 1))} disabled={courante === 0} aria-label="Question précédente"
            className="rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20 disabled:opacity-30">←</button>
          <div className="flex items-center gap-2">
            {questions.map((q, i) => (
              <button key={q.cle} onClick={() => onIndex(i)} aria-label={`Question ${i + 1}`}
                title={passeesIci[q.cle] && !finiesIci[q.cle] ? 'Question passée : tu peux y revenir' : undefined}
                className={`h-3 w-3 rounded-full transition-colors ${i === courante ? 'bg-amber-200' : finiesIci[q.cle] ? 'bg-emerald-400/70' : passeesIci[q.cle] ? 'border border-white/60 bg-transparent hover:bg-white/30' : 'bg-white/25 hover:bg-white/50'}`} />
            ))}
            <span className="ml-2 text-sm text-white/60">{courante + 1} / {n}</span>
          </div>
          <button onClick={() => onIndex(Math.min(n - 1, courante + 1))} disabled={courante === n - 1} aria-label="Question suivante"
            className="rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20 disabled:opacity-30">→</button>
        </div>
      )}
    </div>
  );
}

function UneQuestion({ q, diapo, dire, jouer, preparees, compact = false, onReponse, onFinie, essaisMax = 2, actif = true, contexte, lireDemo, preparerDemo, attendreVoix,
  lireEnonce, arreterEnonce, slideId, onPasser }: {
  q: QuestionDiapo; diapo: { title: string; speech: string; memoire?: string }; dire: (texte: string) => Promise<boolean>;
  jouer: (url: string, secours?: string) => void; preparees?: Record<string, Partial<Record<'juste' | '1' | '2', ReactionPreparee>>>;
  compact?: boolean; onReponse?: (r: ReponseNotee) => void;
  /** Appelé une fois quand la question est terminée ; `fraiche` : terminée à l'instant (pas retrouvée en mémoire) ;
   *  `apresDemo` : la démonstration vient d'être écrite et dite. */
  onFinie?: (cle: string, correct: boolean, fraiche: boolean, apresDemo?: boolean) => void;
  /** Essais permis avant que la question soit close (2 : l'indice puis la réponse ; 1 : question jumelle d'une reprise). */
  essaisMax?: number;
  /** La question est celle que le carrousel montre : la quitter pendant la démonstration la passe. */
  actif?: boolean;
  /** « Passer » (discret) : la question est notée passée ; l'élève peut y revenir. */
  onPasser?: (cle: string) => void;
} & OutilsQuestions) {
  const grand = compact ? 'text-sm' : 'text-lg', titre = compact ? 'text-base' : 'text-xl';
  // Une réponse donnée reste donnée : l'état de la question est gardé (par élève, cours, diapositive et question),
  // et retrouvé si l'élève ferme le tableau, revient sur la diapositive ou recharge la page. Il ne peut pas
  // recommencer pour « effacer » sa réponse : c'est elle qui compte pour le suivi des acquis.
  const memoire = `reponse:${diapo.memoire || ''}:${q.cle}`;
  const sauve = useMemo(() => lireEtatQuestion(memoire), [memoire]);
  const [tentative, setTentative] = useState(sauve.tentative ?? 1);
  const [exclus, setExclus] = useState<number[]>(sauve.exclus ?? []);
  const [pris, setPris] = useState<number | null>(sauve.pris ?? null);
  const [attente, setAttente] = useState(false);
  const [retour, setRetour] = useState<{ correct: boolean | null; ecrit: string } | null>(sauve.retour ?? null);
  const [passee, setPassee] = useState(!!sauve.passee && !sauve.retour);
  const finie = estTerminee(q.type, { retour, tentative }, essaisMax);
  // Le tuteur lit l'énoncé quand la question s'ouvre (une fois ; « 🔊 » pour réécouter) ; il se tait si elle se ferme.
  const enonceLu = useRef(false);
  useEffect(() => {
    if (!actif || !lireEnonce || enonceLu.current || finie || passee || sauve.retour || (sauve.exclus?.length ?? 0) > 0) return;
    // marqué lu au départ de la voix (le double montage du mode strict annule le premier délai)
    const id = window.setTimeout(() => { enonceLu.current = true; lireEnonce(q); }, 350);   // le tableau finit de descendre
    return () => window.clearTimeout(id);
  // eslint-disable-next-line react-hooks/exhaustive-deps -- une lecture à l'ouverture de la question
  }, [actif]);
  useEffect(() => { if (!actif) arreterEnonce?.(); }, [actif, arreterEnonce]);
  useEffect(() => () => arreterEnonce?.(), [arreterEnonce]);
  const passer = () => {
    if (attente || finie) return;
    arreterEnonce?.();
    setPassee(true);
    try { localStorage.setItem(memoire, JSON.stringify({ ...lireEtatQuestion(memoire), tentative, exclus, pris, passee: true })); } catch { /* sans mémoire locale */ }
    onReponse?.({ cle: q.cle, type: q.type, enonce: q.enonce, reponse: '', tentative, correct: null, preparee: false, passee: true });
    onPasser?.(q.cle);
  };
  // Le temps de réflexion (11 novembre 2026) : l'énoncé seul d'abord, les choix après 10 s (6 s pour un vrai/faux),
  // ou tout de suite sur « Je suis prêt ». Pas pour une question déjà commencée (état retrouvé).
  const dureeReflexion = q.type === 'vrai_faux' ? REFLEXION_VRAI_FAUX_MS : REFLEXION_MS;
  const [choixVisibles, setChoixVisibles] = useState(() => !q.choix || !!sauve.retour || (sauve.exclus?.length ?? 0) > 0);
  useEffect(() => {
    if (choixVisibles || !actif) return;   // le compte ne court que sur la question montrée
    const id = window.setTimeout(() => setChoixVisibles(true), dureeReflexion);
    return () => window.clearTimeout(id);
  }, [choixVisibles, actif, dureeReflexion]);
  const vientDeFinir = useRef(false);
  const finieSignalee = useRef(false);
  // La démonstration manuscrite (10 novembre 2026) : après la réaction dite, juste ou faux, puis la suite du carrousel.
  const avecDemo = !!q.demonstration?.lignes?.length && !!lireDemo;
  // 'dite' : la voix a fini, le tableau de la démonstration reste ouvert jusqu'à ce que l'élève le ferme (12 novembre 2026)
  const [demo, setDemo] = useState<'aucune' | 'attente' | 'ecrit' | 'dite' | 'finie'>('aucune');
  const [revoir, setRevoir] = useState(false);
  const lecture = useRef<LectureDemo | null>(null);
  const [lectureVue, setLectureVue] = useState<LectureDemo | null>(null);
  /** La voix de la réaction : la démonstration attend qu'elle soit partie, puis dite jusqu'au bout. */
  const voixReaction = useRef<Promise<unknown>>(Promise.resolve());
  const demoAnnulee = useRef(false);
  const lancerDemo = useCallback(async () => {
    setDemo('attente');
    await voixReaction.current;
    // la réaction est partie : la voix de la démonstration se calcule pendant qu'elle est dite
    const prete = demoAnnulee.current ? null : preparerDemo?.(q.demonstration!) ?? null;
    await attendreVoix?.();
    if (demoAnnulee.current) return;
    const l = lireDemo!(q.demonstration!, prete);
    lecture.current = l; setLectureVue(l); setDemo('ecrit');
    await l.fin;
    if (lecture.current === l) { lecture.current = null; setDemo(x => (x === 'ecrit' ? 'dite' : x)); }
  }, [attendreVoix, lireDemo, preparerDemo, q.demonstration]);
  const passerDemo = useCallback(() => {
    demoAnnulee.current = true;
    lecture.current?.arreter(); lecture.current = null;
    setDemo('finie');
  }, []);
  useEffect(() => {
    if (!finie || attente || finieSignalee.current) return;
    if (avecDemo && vientDeFinir.current && demo !== 'finie') { if (demo === 'aucune') void lancerDemo(); return; }
    finieSignalee.current = true;
    onFinie?.(q.cle, retour?.correct === true, vientDeFinir.current, avecDemo && vientDeFinir.current);
  }, [finie, attente, onFinie, q.cle, retour, avecDemo, demo, lancerDemo]);
  // L'élève passe à une autre question pendant la démonstration (« Suivant → », un point) : elle est passée.
  useEffect(() => { if (!actif && (demo === 'attente' || demo === 'ecrit' || demo === 'dite')) passerDemo(); }, [actif, demo, passerDemo]);
  /** Le tableau de la démonstration fermé (à la main ou après son délai) : la question est finie, le cours passe à la suite. */
  const fermerDemo = useCallback(() => { passerDemo(); }, [passerDemo]);
  // Le tableau se ferme pendant la démonstration : la voix s'arrête, la question compte comme finie.
  const finRef = useRef({ onFinie, cle: q.cle, correct: retour?.correct === true });
  finRef.current = { onFinie, cle: q.cle, correct: retour?.correct === true };
  const demoRef = useRef(demo);
  demoRef.current = demo;
  useEffect(() => () => {
    if (demoRef.current !== 'attente' && demoRef.current !== 'ecrit' && demoRef.current !== 'dite') return;
    lecture.current?.arreter(); lecture.current = null; demoAnnulee.current = true;
    if (!finieSignalee.current && vientDeFinir.current) { finieSignalee.current = true; finRef.current.onFinie?.(finRef.current.cle, finRef.current.correct, true, true); }
  }, []);
  useEffect(() => {
    if (!retour || attente) return;
    try { localStorage.setItem(memoire, JSON.stringify({ tentative, exclus, pris, retour, passee: false })); } catch { /* sans mémoire locale, la réponse reste au moins sur le serveur */ }
  }, [memoire, tentative, exclus, pris, retour, attente]);

  const envoyer = async (reponse: string, indice: number | null) => {
    if (attente || finie) return;
    arreterEnonce?.();
    setPassee(false);
    vientDeFinir.current = true;
    const verdict = indice !== null && q.bonne !== undefined ? indice === q.bonne : null;
    // Après cette erreur, il ne resterait qu'un seul choix (vrai/faux, ou les autres choix déjà barrés) : le cliquer
    // ne prouverait rien. La question se ferme tout de suite comme une faute, avec la réponse (15 novembre 2026).
    const dernierChoix = verdict === false && !!q.choix && q.choix.length - exclus.length - 1 <= 1;
    const close = verdict === false && (tentative >= essaisMax || dernierChoix);
    /** l'erreur est notée : le choix est barré et, si la question est close, elle passe au-delà des essais permis */
    const noterErreur = (i: number | null) => {
      if (i !== null) setExclus(e => [...e, i]);
      setTentative(t => (dernierChoix ? Math.max(t + 1, essaisMax + 1) : t + 1));
    };
    // La réaction préparée pour cette réponse : tout de suite, avec sa voix.
    const prete = indice !== null && verdict !== null ? preparees?.[String(indice)]?.[verdict ? 'juste' : (close ? '2' : '1')] : undefined;
    if (prete) {
      onReponse?.({ cle: q.cle, type: q.type, enonce: q.enonce, reponse, tentative, correct: verdict, preparee: true });
      setPris(indice);
      setRetour({ correct: verdict, ecrit: prete.ecrit });
      if (prete.audio) { jouer(prete.audio, prete.parole); voixReaction.current = Promise.resolve(); } else voixReaction.current = dire(prete.parole);
      if (verdict === false) noterErreur(indice);
      return;
    }
    setAttente(true); setPris(indice);
    if (verdict !== null) setRetour({ correct: verdict, ecrit: '' });     // la couleur tout de suite, la voix suit
    try {
      const r = await appelerApi<{ correct: boolean | null; parole: string; ecrit: string }>('/course-player/answer-reaction', {
        // une question close donne la réponse : le serveur reçoit le dernier essai permis
        diapo, question: { type: q.type, enonce: q.enonce, choix: q.choix, bonne: q.bonne }, reponse, tentative: close ? Math.max(tentative, essaisMax) : tentative, verdict,
      });
      onReponse?.({ cle: q.cle, type: q.type, enonce: q.enonce, reponse, tentative, correct: r.correct, preparee: false });
      setRetour({ correct: r.correct, ecrit: r.ecrit });
      voixReaction.current = dire(r.parole);
      if (r.correct === false) noterErreur(indice);
    } catch {
      if (verdict !== null) onReponse?.({ cle: q.cle, type: q.type, enonce: q.enonce, reponse, tentative, correct: verdict, preparee: false });
      setRetour(verdict === null ? { correct: null, ecrit: 'Le professeur ne peut pas répondre pour le moment.' }
        : { correct: verdict, ecrit: verdict ? 'Juste.' : close ? (q.explication || 'Pas tout à fait.') : (q.explication || 'Pas tout à fait : réessaie.') });
      if (verdict === false) noterErreur(indice);
    } finally { setAttente(false); }
  };

  return (
    <div className="flex h-full min-h-0 flex-col overflow-y-auto rounded-xl border border-white/15 p-4">
      <RemplirSiCourt>
      <div className="flex items-start gap-2">
        <p className={`${titre} min-w-0 flex-1 text-amber-100`}><Formule t={q.enonce} /></p>
        {lireEnonce && !finie && (
          <button type="button" onClick={() => lireEnonce(q)} title="Réécouter l’énoncé" aria-label="Réécouter l’énoncé"
            className="shrink-0 rounded-full bg-white/10 px-2.5 py-1 text-sm text-white/70 hover:bg-white/20" style={{ fontFamily: 'system-ui, sans-serif' }}>🔊</button>
        )}
      </div>
      {passee && !finie && <p className="mt-1 text-sm text-white/50" style={{ fontFamily: 'system-ui, sans-serif' }}>⏭ Passée — tu peux y répondre quand tu veux.</p>}
      {q.choix && !choixVisibles && (
        <div className="mt-5 flex flex-col items-start gap-3">
          <p className={`${grand} text-white/75`}>🤔 Réfléchis d’abord…</p>
          <div className="h-1.5 w-56 overflow-hidden rounded-full bg-white/10">
            <div key={actif ? 'court' : 'attend'} className="reflexion-barre h-full rounded-full bg-amber-200/70"
              style={{ animationDuration: `${dureeReflexion}ms`, animationPlayState: actif ? 'running' : 'paused' }} />
          </div>
          <button onClick={() => setChoixVisibles(true)} className="text-sm text-white/45 underline-offset-4 hover:text-white hover:underline">Je suis prêt</button>
        </div>
      )}
      {q.choix && choixVisibles && (
        <div data-choix={q.type} className={`question-apparait ${q.type === 'vrai_faux' ? 'mt-2 flex gap-2' : `mt-2 ${compact ? 'space-y-1' : 'space-y-2'}`}`}>
          {q.choix.map((c, i) => {
            const bonneMontree = finie && (q.bonne === i || (retour?.correct && pris === i));
            const fausse = exclus.includes(i);
            return (
              <button key={i} disabled={attente || finie || fausse} onClick={() => void envoyer(c, i)}
                className={`${q.type === 'vrai_faux' ? 'px-4' : 'block w-full px-3 text-left'} rounded-lg border ${compact ? 'py-1' : 'py-2'} ${grand} disabled:cursor-default ${
                  bonneMontree ? 'border-emerald-400 bg-emerald-500/20' : fausse ? 'border-rose-400/60 bg-rose-500/15 line-through opacity-70' : pris === i && attente ? 'border-cyan-300 bg-white/10' : 'border-white/15 hover:bg-white/5'}`}>
                {q.type === 'qcm' ? `${String.fromCharCode(65 + i)}. ` : ''}<Formule t={c} />
              </button>
            );
          })}
        </div>
      )}
      {q.type === 'directe' && (
        // Réponse libre : écrite, dite au micro ou photographiée, avec le clavier scientifique ; relue avant l'envoi.
        <ChampReponse onEnvoyer={t => void envoyer(t, null)} disabled={attente || finie} contexte={{ ...contexte, enonce: q.enonce }}
          clavierAuto actif={actif} suggestions={{ deck_id: contexte?.deck_id, slide_id: slideId, cle: q.cle, enonce: q.enonce, clavier: q.lu?.clavier }} />
      )}
      {attente && <p className="mt-2 text-sm text-white/60 animate-pulse">Le professeur regarde ta réponse…</p>}
      {retour && !attente && retour.ecrit && (
        <p className={`mt-2 ${grand} ${retour.correct === true ? 'text-emerald-200' : retour.correct === false ? 'text-rose-200' : 'text-amber-200'}`}>
          {retour.correct === true ? '✔ ' : retour.correct === false ? (finie ? '✘ ' : '↻ ') : '? '}<Formule t={retour.ecrit} />
        </p>
      )}
      {onPasser && !finie && !attente && !passee && (
        // discret : on peut ne pas répondre ; la question est notée passée, sans marque rouge, et on peut y revenir
        <button type="button" onClick={passer} className="mt-3 self-start text-sm text-white/40 underline-offset-4 hover:text-white/80 hover:underline"
          style={{ fontFamily: 'system-ui, sans-serif' }}>Passer ⏭</button>
      )}
      {q.demonstration?.lignes?.length && finie && (demo === 'finie' || !vientDeFinir.current) && !revoir ? (
        <button type="button" onClick={() => setRevoir(true)} className="mt-3 self-start rounded-full bg-white/10 px-4 py-1.5 text-sm hover:bg-white/20"
          style={{ fontFamily: 'system-ui, sans-serif' }}>✍️ Revoir la démonstration</button>
      ) : null}
      {/* La démonstration sur un tableau à part, par-dessus le tableau de la question (12 novembre 2026). */}
      {q.demonstration?.lignes?.length && finie && (demo === 'attente' || demo === 'ecrit' || demo === 'dite') ? (
        <DemonstrationPleine d={q.demonstration} lecture={demo === 'attente' ? null : lectureVue} complet={false} enonce={q.enonce} onFermer={fermerDemo} />
      ) : null}
      {q.demonstration?.lignes?.length && revoir ? (
        <DemonstrationPleine d={q.demonstration} lecture={null} complet enonce={q.enonce} onFermer={() => setRevoir(false)} />
      ) : null}
      </RemplirSiCourt>
    </div>
  );
}

/**
 * Le tableau du professeur pour la question de l'élève (9 novembre 2026). Il y écrit, ligne après ligne, au rythme
 * de sa voix ; ce qu'il dit n'est montré en texte qu'à la demande. `plein` : le tableau a été effacé à la brosse
 * (notion de base) et couvre toute la scène ; sinon il s'ouvre sous la figure, qui reste visible pour les gestes.
 */
function TableauDuProf({ t, plein = false, lignesRef, onTexte, onAutre, onContinuer, onFini }: {
  t: TableauProf; plein?: boolean; lignesRef: React.MutableRefObject<(HTMLParagraphElement | null)[]>;
  onTexte: () => void; onAutre: () => void; onContinuer: () => void; onFini?: (ex: Exercice, correct: boolean, reponse: string) => void;
}) {
  const enExercice = t.etape === 'exercice' && !!t.exercice;
  const brosse = t.etape === 'brosse';
  const fond = '#0f2219';
  return (
    <section className={`relative flex flex-col overflow-hidden rounded-2xl ${plein ? (brosse ? 'flex-1' : 'tableau-questions flex-1') : 'tableau-questions w-full max-w-4xl shrink-0'} ${brosse ? '' : 'border-2 border-amber-200/40 shadow-2xl'}`}
      style={{ fontFamily: CRAIE, background: brosse ? 'transparent' : fond, maxHeight: plein ? undefined : '42%', minHeight: plein ? undefined : 120 }}>
      {brosse && (
        <>
          {/* Trois passages de brosse : chaque bande redevient un tableau propre derrière elle. */}
          {[0, 1, 2].map(i => (
            <div key={i} className="absolute inset-x-0" style={{
              top: `${i * 33.34}%`, height: '33.4%', background: fond,
              animation: `${i % 2 ? 'brosse-d' : 'brosse-g'} ${BROSSE_MS / 3000}s linear ${(i * BROSSE_MS) / 3000}s both`,
            }} />
          ))}
          <div className="brosse" aria-hidden>
            <div>
              <div style={{ height: 22, borderRadius: '10px 10px 3px 3px', background: 'linear-gradient(#a8743f, #7a4e22)', boxShadow: 'inset 0 2px 0 rgba(255,255,255,.25)' }} />
              <div style={{ height: 18, borderRadius: '0 0 6px 6px', background: 'repeating-linear-gradient(90deg, #e9e4d6 0 6px, #d3cdbb 6px 9px)', boxShadow: '0 10px 22px 6px rgba(240,240,230,.35)' }} />
            </div>
          </div>
          <p className="absolute bottom-3 left-0 right-0 z-[4] text-center text-lg text-amber-100/90">On traite d’abord cet élément{t.notion ? ` : ${t.notion}` : ''}…</p>
        </>
      )}
      {!brosse && (
        <>
          <div className="flex shrink-0 items-center justify-between gap-3 border-b border-amber-200/20 px-4 py-2">
            <div className="truncate text-base text-emerald-200">🧑‍🏫 {t.notion || 'Ta question'}</div>
            <div className="flex shrink-0 gap-2 text-sm" style={{ fontFamily: 'system-ui, sans-serif' }}>
              {(t.etape === 'ecrit' || enExercice) && (t.parole || t.ecrit) && (
                <button onClick={onTexte} className="rounded-full bg-white/10 px-3 py-1 hover:bg-white/20">{t.texte ? 'Masquer le texte' : '📄 Voir le texte'}</button>
              )}
              <button onClick={onAutre} className="rounded-full bg-white/10 px-3 py-1 hover:bg-white/20">Autre question</button>
              <button onClick={onContinuer} className="rounded-full bg-emerald-500/30 px-3 py-1 hover:bg-emerald-500/40">Continuer le cours</button>
            </div>
          </div>
          {/* Tout le tableau dans l'écran, sans défiler (user rule, 12 novembre 2026) : l'écriture prend la taille qui
              tient avec TOUTES ses lignes (les lignes pas encore écrites gardent leur place, invisibles : rien ne saute). */}
          <SansDefilement className="px-6 py-4" centrer={plein && !enExercice} agrandirMax={enExercice ? 1 : 1.6}>
           <div className="flex flex-col gap-2">
            {t.etape === 'prepare' && <p className="animate-pulse text-xl text-white/60">Le professeur prépare le tableau…</p>}
            {t.lignes.map((l, i) => (
              <p key={i} ref={el => { lignesRef.current[i] = el; }} className={i < t.vues ? 'craie-ecrit' : ''} dir="auto" aria-hidden={i >= t.vues || undefined}
                style={{ fontSize: enExercice ? 18 : 26, color: /[=→]/.test(l) ? '#fef9c3' : '#f1f5e9', lineHeight: 1.35, opacity: enExercice ? .7 : 1, visibility: i < t.vues ? 'visible' : 'hidden' }}>
                <Formule t={l} />
              </p>
            ))}
            {t.etape === 'ecrit' && !t.lignes.length && !t.erreur && <p className="text-lg text-white/50">Écoute le professeur…</p>}
            {t.erreur && <p className="text-base text-rose-200" style={{ fontFamily: 'system-ui, sans-serif' }}>{t.erreur}</p>}
            {enExercice && <ExerciceDuTableau ex={t.exercice!} onFini={(c, r) => onFini?.(t.exercice!, c, r)} />}
            {t.texte && (
              <div className="mt-2 rounded-xl border border-white/15 bg-black/25 px-4 py-3 text-base text-white/80" style={{ fontFamily: 'system-ui, sans-serif' }}>
                {t.ecrit && <p><Formule t={t.ecrit} /></p>}
                {t.parole && <p dir="auto" className="mt-2 whitespace-pre-wrap text-white/60">{t.parole}</p>}
              </div>
            )}
           </div>
          </SansDefilement>
        </>
      )}
    </section>
  );
}

/**
 * L'exercice qui suit l'explication au tableau (9 novembre 2026) : QCM, vrai/faux ou association, choisi par le
 * tuteur selon ce qu'il a expliqué. Une seule tentative : la correction s'affiche, le tuteur réagit à la voix.
 */
function ExerciceDuTableau({ ex, onFini }: { ex: Exercice; onFini: (correct: boolean, reponse: string) => void }) {
  const [fini, setFini] = useState<boolean | null>(null);
  const [choix, setChoix] = useState<number | null>(null);
  const [vf, setVf] = useState<(boolean | null)[]>(() => (ex.affirmations || []).map(() => null));
  // Association : la colonne de droite est mélangée une fois ; l'élève touche une notion, puis sa partenaire.
  const droites = useMemo(() => {
    const d = (ex.paires || []).map((p, i) => ({ texte: p.droite, i }));
    for (let k = d.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [d[k], d[j]] = [d[j], d[k]]; }
    if (d.length > 1 && d.every((x, k) => x.i === k)) d.push(d.shift()!);   // jamais déjà dans l'ordre
    return d;
  }, [ex]);
  const [gauche, setGauche] = useState<number | null>(null);
  const [lien, setLien] = useState<Record<number, number>>({});   // gauche → droite (indice de paire)
  const COULEURS = ['#fde68a', '#a5f3fc', '#f9a8d4', '#bbf7d0'];

  const terminer = (correct: boolean, reponse: string) => { setFini(correct); onFini(correct, reponse); };
  const bouton = 'rounded-xl border px-4 py-2 text-left text-lg transition-colors';
  const corrige = fini !== null;

  return (
    <div className="question-apparait mt-3 rounded-2xl border border-amber-200/30 bg-black/20 p-4">
      <div className="text-sm font-semibold text-amber-200">✏️ Tu as bien compris ? Vérifions</div>
      {ex.enonce && <p className="mt-2 text-xl text-white/90"><Formule t={ex.enonce} /></p>}

      {ex.type === 'qcm' && (
        <div className="mt-3 grid gap-2 sm:grid-cols-2">
          {(ex.choix || []).map((c, i) => {
            const etat = !corrige ? '' : i === ex.bonne ? 'border-emerald-300 bg-emerald-500/25' : i === choix ? 'border-rose-300 bg-rose-500/25' : 'opacity-60';
            return (
              <button key={i} disabled={corrige} onClick={() => { setChoix(i); terminer(i === ex.bonne, c); }}
                className={`${bouton} border-white/20 hover:bg-white/10 ${etat}`}><Formule t={c} /></button>
            );
          })}
        </div>
      )}

      {ex.type === 'vrai_faux' && (
        <div className="mt-3 flex flex-col gap-2">
          {(ex.affirmations || []).map((a, i) => {
            const juste = corrige && vf[i] === a.vrai, faux = corrige && vf[i] !== a.vrai;
            return (
              <div key={i} className={`flex items-center gap-3 rounded-xl border px-3 py-2 ${juste ? 'border-emerald-300/70' : faux ? 'border-rose-300/70' : 'border-white/15'}`}>
                <p className="flex-1 text-lg"><Formule t={a.texte} /></p>
                {[true, false].map(v => (
                  <button key={String(v)} disabled={corrige} onClick={() => setVf(x => x.map((y, k) => (k === i ? v : y)))}
                    className={`rounded-full px-3 py-1 text-sm ${vf[i] === v ? 'bg-sky-500/50' : 'bg-white/10 hover:bg-white/20'}`}>{v ? 'Vrai' : 'Faux'}</button>
                ))}
                {corrige && <span className="w-16 text-sm">{juste ? '✔' : `✘ ${a.vrai ? 'Vrai' : 'Faux'}`}</span>}
              </div>
            );
          })}
          {!corrige && (
            <button disabled={vf.some(v => v === null)} onClick={() => {
              const affs = ex.affirmations || [];
              terminer(affs.every((a, i) => vf[i] === a.vrai), affs.map((a, i) => `${a.texte} : ${vf[i] ? 'vrai' : 'faux'}`).join(' ; '));
            }} className="self-end rounded-full bg-sky-500/40 px-5 py-2 text-sm hover:bg-sky-500/50 disabled:opacity-40">Vérifier</button>
          )}
        </div>
      )}

      {ex.type === 'association' && (
        <>
          <p className="mt-1 text-sm text-white/55">Touche un élément à gauche, puis celui qui va avec à droite.</p>
          <div className="mt-3 grid grid-cols-2 gap-3">
            <div className="flex flex-col gap-2">
              {(ex.paires || []).map((p, i) => {
                const n = Object.keys(lien).indexOf(String(i));
                const ok = corrige ? lien[i] === i : null;
                return (
                  <button key={i} disabled={corrige} onClick={() => setGauche(i)}
                    className={`${bouton} ${gauche === i ? 'border-sky-300 bg-sky-500/20' : 'border-white/20 hover:bg-white/10'} ${ok === true ? 'border-emerald-300' : ok === false ? 'border-rose-300' : ''}`}
                    style={lien[i] !== undefined && !corrige ? { boxShadow: `inset 6px 0 0 ${COULEURS[n % 4]}` } : undefined}>
                    <Formule t={p.gauche} />{corrige && ok === false && <span className="block text-sm text-emerald-200">→ <Formule t={p.droite} /></span>}
                  </button>
                );
              })}
            </div>
            <div className="flex flex-col gap-2">
              {droites.map(d => {
                const deQui = Object.entries(lien).find(([, v]) => v === d.i)?.[0];
                const n = deQui === undefined ? -1 : Object.keys(lien).indexOf(deQui);
                return (
                  <button key={d.i} disabled={corrige || gauche === null} onClick={() => {
                    if (gauche === null) return;
                    setLien(l => { const m = Object.fromEntries(Object.entries(l).filter(([, v]) => v !== d.i)); return { ...m, [gauche]: d.i }; });
                    setGauche(null);
                  }} className={`${bouton} border-white/20 hover:bg-white/10 disabled:cursor-default`}
                    style={n >= 0 && !corrige ? { boxShadow: `inset -6px 0 0 ${COULEURS[n % 4]}` } : undefined}>
                    <Formule t={d.texte} />
                  </button>
                );
              })}
            </div>
          </div>
          {!corrige && (
            <button disabled={Object.keys(lien).length < (ex.paires || []).length} onClick={() => {
              const paires = ex.paires || [];
              terminer(paires.every((_, i) => lien[i] === i), paires.map((p, i) => `${p.gauche} → ${paires[lien[i]]?.droite ?? '?'}`).join(' ; '));
            }} className="mt-3 rounded-full bg-sky-500/40 px-5 py-2 text-sm hover:bg-sky-500/50 disabled:opacity-40">Vérifier</button>
          )}
        </>
      )}

      {corrige && (
        <p className={`mt-3 text-lg ${fini ? 'text-emerald-200' : 'text-rose-200'}`}>
          {fini ? '✔ Bravo, c’est compris. ' : '✘ Pas tout à fait. '}{ex.explication && <Formule t={ex.explication} />}
        </p>
      )}
    </div>
  );
}


/**
 * La question sur le résultat de l'élève : l'interprétation s'écrit au fil de la voix (`vu`), puis l'énoncé et ses
 * choix ; on ne répond qu'une fois tout dit. Chaque option a son retour, écrit dessous et dit à voix haute.
 */
function QuestionSurResultat({ reaction, vu, onRepondre, contexte }: {
  reaction: Extract<Reaction, { phase: 'question' }>;
  vu: { phrases: number; question: boolean };
  onRepondre: (choix: { indice?: number; affirmation?: { i: number; vrai: boolean }; directe?: string }) => void;
  contexte: ContexteOcr;
}) {
  const { question: q, verdict, phrases, voix, pris, vf = {}, retoursVf = {} } = reaction;
  const pret = voix === 'fini';
  const affirmations = q.affirmations || [];
  return (
    <div className="mt-2 space-y-3" style={{ fontFamily: CRAIE }}>
      {phrases.length > 0 && (
        <p className="text-lg text-white/85">
          {phrases.slice(0, vu.phrases).map((ph, i) => <span key={i} className="question-apparait inline">{i ? ' ' : ''}<Formule t={ph} /></span>)}
        </p>
      )}
      {vu.question && (
        <div className="question-apparait space-y-2">
          <p className="text-lg font-semibold text-amber-100"><Formule t={q.enonce} /></p>
          {q.type === 'qcm' && (q.choix || []).map((c, i) => {
            const montre = verdict && (i === q.bonne || i === pris);
            return (
              <div key={i}>
                <button disabled={!pret || !!verdict} onClick={() => onRepondre({ indice: i })}
                  className={`block w-full rounded-lg border px-3 py-2 text-left text-base disabled:cursor-default ${montre ? (i === q.bonne ? 'border-emerald-400 bg-emerald-500/20' : 'border-rose-400 bg-rose-500/20') : pret && !verdict ? 'border-white/15 hover:bg-white/5' : 'border-white/10'}`}>
                  {String.fromCharCode(65 + i)}. <Formule t={c} />
                </button>
                {verdict && i === pris && verdict.ecrit && (
                  <p className={`question-apparait mt-1 pl-2 text-base ${verdict.correct ? 'text-emerald-200' : 'text-rose-200'}`}>{verdict.correct ? '✔ ' : '✘ '}<Formule t={verdict.ecrit} /></p>
                )}
              </div>
            );
          })}
          {q.type === 'vrai_faux' && affirmations.map((a, i) => {
            const rep = vf[i], retour = retoursVf[i];
            return (
              <div key={i} className={`rounded-lg border px-3 py-2 ${rep === undefined ? 'border-white/15' : rep === a.vrai ? 'border-emerald-400/70' : 'border-rose-400/70'}`}>
                <div className="text-base"><Formule t={a.texte} /></div>
                <div className="mt-1 flex gap-2">
                  {[true, false].map(v => (
                    <button key={String(v)} disabled={!pret || rep !== undefined} onClick={() => onRepondre({ affirmation: { i, vrai: v } })}
                      className={`min-h-[36px] rounded px-4 py-1 text-sm disabled:cursor-default ${rep === v ? (v === a.vrai ? 'bg-emerald-500/30' : 'bg-rose-500/30') : 'bg-white/10'} ${pret && rep === undefined ? 'hover:bg-white/20' : ''}`}>
                      {v ? 'Vrai' : 'Faux'}
                    </button>
                  ))}
                </div>
                {retour?.ecrit && <p className={`question-apparait mt-1 text-sm ${rep === a.vrai ? 'text-emerald-200' : 'text-rose-200'}`}>{rep === a.vrai ? '✔ ' : '✘ '}<Formule t={retour.ecrit} /></p>}
              </div>
            );
          })}
          {q.type === 'directe' && (
            <ChampReponse onEnvoyer={t => onRepondre({ directe: t })} disabled={!pret || !!verdict} contexte={{ ...contexte, enonce: q.enonce }} clavierAuto
              suggestions={{ deck_id: contexte?.deck_id, enonce: q.enonce }} />
          )}
          {verdict && q.type !== 'qcm' && verdict.ecrit && (
            <p className={`text-base ${verdict.correct ? 'text-emerald-200' : 'text-rose-200'}`}>{verdict.ecrit === '…' ? <span className="animate-pulse">Le professeur regarde ta réponse…</span> : <>{verdict.correct ? '✔ ' : '✘ '}<Formule t={verdict.ecrit} /></>}</p>
          )}
          {!pret && <p className="text-sm text-white/45">Écoute le professeur, puis réponds.</p>}
          {verdict && verdict.ecrit !== '…' && <p className="text-sm text-white/45">Le cours reprend dès que le professeur a fini.</p>}
        </div>
      )}
    </div>
  );
}

/** « 🔎 Ton résultat » : clignote tant que l'élève n'a pas demandé l'explication de son nouveau résultat. */
/**
 * La bande de la question d'observation (14 novembre 2026), sous la simulation : la question, le micro de RÉPONSE
 * (distinct du micro des questions libres, visible seulement ici), les indices au fil des silences, puis trois cartes
 * (ou Vrai / Faux) dans la même bande. Rien ne couvre la figure : l'élève doit pouvoir regarder.
 */
function BandeObservation({ o, e, etroit, onCarte, onCartes, onMicro, onMicroFin, onPasser }: {
  o: QuestionObservation; e: EtatObservation; etroit: boolean;
  onCarte: (i: number) => void; onCartes: () => void; onMicro: () => void; onMicroFin: () => void; onPasser: () => void;
}) {
  const indices = (o.indices || []).slice(0, e.indices);
  const occupe = e.etape === 'transcrit' || e.etape === 'juge' || e.etape === 'fini';
  const v = e.verdict;
  return (
    <section data-observation className="question-apparait relative z-20 w-full max-w-4xl shrink-0 rounded-2xl border-2 border-amber-200/45 bg-[#0f2219]/95 px-4 py-2.5 shadow-2xl"
      style={{ fontFamily: CRAIE }}>
      <div className="flex items-center gap-3">
        <div className="min-w-0 flex-1">
          <div className="text-xs font-semibold uppercase tracking-wide text-emerald-200/80">👀 Observe</div>
          <p className="text-lg leading-snug text-amber-100 md:text-xl"><Formule t={o.enonce} /></p>
        </div>
        <button
          type="button" data-micro-reponse disabled={occupe}
          // maintenir pour répondre, relâcher pour finir (souris, doigt, ou barre d'espace)
          onPointerDown={ev => { ev.preventDefault(); ev.currentTarget.setPointerCapture?.(ev.pointerId); onMicro(); }}
          onPointerUp={onMicroFin} onPointerCancel={onMicroFin} onLostPointerCapture={onMicroFin}
          onKeyDown={ev => { if ((ev.key === ' ' || ev.key === 'Enter') && !ev.repeat) { ev.preventDefault(); onMicro(); } }}
          onKeyUp={ev => { if (ev.key === ' ' || ev.key === 'Enter') { ev.preventDefault(); onMicroFin(); } }}
          onContextMenu={ev => ev.preventDefault()}
          style={{ touchAction: 'none', userSelect: 'none', WebkitUserSelect: 'none' }}
          title="Maintiens le bouton et dis ta réponse"
          className={`shrink-0 rounded-full px-4 py-2.5 text-base font-semibold transition-colors disabled:opacity-40 ${e.etape === 'ecoute'
            ? 'bg-rose-500/60 ring-2 ring-rose-200 animate-pulse' : 'bg-emerald-500/30 ring-1 ring-emerald-300/60 hover:bg-emerald-500/45'}`}>
          {e.etape === 'ecoute' ? '● Je t’écoute… relâche' : etroit ? '🎙️ Réponds' : '🎙️ Maintiens pour répondre'}
        </button>
        {e.etape !== 'fini' && (
          <button type="button" onClick={onPasser} className="shrink-0 self-end text-xs text-white/35 hover:text-white/80" title="Passer : la voix reprend">Passer ⏭</button>
        )}
      </div>
      {/* les indices se remplacent : seul le dernier reste écrit (la figure garde sa place) */}
      {indices.length > 0 && !v?.correct && (
        <p key={indices.length} className="craie-ecrit mt-0.5 text-lg leading-snug text-cyan-200">
          💡 <Formule t={indices[indices.length - 1].texte} />{(o.indices || []).length > 1 && <span className="ml-2 text-xs text-cyan-200/50">{indices.length}/{(o.indices || []).length}</span>}
        </p>
      )}
      {e.etape === 'observe' && !v && !e.cartes && (
        <p className="mt-0.5 text-sm text-white/55">Regarde bien la simulation, prends ton temps…
          <button type="button" onClick={onCartes} className="ml-2 underline decoration-dotted hover:text-white">voir des propositions</button></p>
      )}
      {e.etape === 'transcrit' && <p className="mt-0.5 animate-pulse text-sm text-sky-200">✍️ J’écris ce que tu as dit…</p>}
      {e.etape === 'juge' && <p dir="auto" className="mt-0.5 animate-pulse text-sm text-amber-200">🎙️ « {e.entendu} » — le professeur réfléchit…</p>}
      {v && (
        <p className={`craie-ecrit mt-0.5 text-lg leading-snug ${v.correct ? 'text-emerald-300' : v.correct === false ? 'text-rose-200' : 'text-amber-200'}`}>
          {e.entendu && e.etape !== 'juge' && <span dir="auto" className="mr-2 text-sm text-sky-200/80">🎙️ « {e.entendu} »</span>}
          {v.correct ? '✔ ' : v.correct === false ? '✘ ' : '? '}<Formule t={v.ecrit} />
        </p>
      )}
      {e.erreur && <p className="mt-1 text-sm text-rose-200">{e.erreur}</p>}
      {e.cartes && (
        <div className="question-apparait mt-1.5 grid gap-2" style={{ gridTemplateColumns: `repeat(${etroit && o.choix.length > 2 ? 1 : o.choix.length}, minmax(0, 1fr))` }}>
          {o.choix.map((c, i) => {
            const barree = e.exclus.includes(i), bonne = e.bonneMontree && i === o.bonne;
            return (
              <button key={i} type="button" data-carte={i} onClick={() => onCarte(i)} disabled={barree || e.etape !== 'observe'}
                className={`rounded-xl border px-3 py-1.5 text-left text-lg leading-snug transition-colors ${bonne ? 'border-emerald-300 bg-emerald-500/25 text-emerald-100'
                  : barree ? 'border-rose-300/30 bg-rose-500/10 text-white/40 line-through' : 'border-white/25 bg-white/5 hover:border-amber-200/70 hover:bg-white/10'} disabled:cursor-default`}>
                <Formule t={c} />
              </button>
            );
          })}
        </div>
      )}
    </section>
  );
}

function BoutonResultat({ onClick, className = '' }: { onClick: () => void; className?: string }) {
  return (
    <button onClick={onClick} aria-label="Voir ton résultat expliqué par le professeur"
      className={`${className} animate-pulse rounded-full border border-cyan-300/70 bg-[#0d1c15]/90 px-5 py-2 text-sm text-cyan-100 shadow-lg ring-2 ring-cyan-300/40 hover:bg-cyan-900/60`}>
      🔎 Ton résultat
    </button>
  );
}

/** Le texte d'un bouton de la barre : l'icône toujours, le mot sur grand écran (et au survol, `title`). */
function Libelle({ icone, texte }: { icone: string; texte: string }) {
  return <span title={texte} aria-label={texte}>{icone}<span className="hidden 2xl:inline"> {texte}</span></span>;
}

/** Téléphone en paysage (hauteur < 520 px) : vrai tant que l'écran garde cette forme. */
function useCourt() {
  const requete = '(max-height: 520px) and (orientation: landscape)';
  const [court, setCourt] = useState(() => typeof window !== 'undefined' && window.matchMedia(requete).matches);
  useEffect(() => {
    const m = window.matchMedia(requete), suivre = () => setCourt(m.matches);
    m.addEventListener('change', suivre);
    return () => m.removeEventListener('change', suivre);
  }, []);
  return court;
}

/** Sur téléphone en paysage, la question (énoncé, choix, retour) grandit jusqu'à remplir sa carte (16 novembre 2026 :
 *  « agrandir les suggestions du QCM, il reste de la place ») et se resserre quand le retour du professeur arrive. */
function RemplirSiCourt({ children }: { children: ReactNode }) {
  const court = useCourt();
  return court ? <SansDefilement agrandirMax={1.5} zoomMin={0.85}>{children}</SansDefilement> : <>{children}</>;
}

function Bulle({ children, actif, pulse, disabled, onClick }: { children: ReactNode; actif?: boolean; pulse?: boolean; disabled?: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`h-9 shrink-0 whitespace-nowrap rounded-full px-3 text-sm transition-colors disabled:opacity-30 ${actif ? 'bg-amber-200 text-black' : 'bg-white/10 hover:bg-white/20'} ${pulse ? 'animate-pulse ring-2 ring-amber-200/60' : ''}`}
    >
      {children}
    </button>
  );
}

function Exercices({ exercices }: { exercices: NonNullable<CourseSlide['exercises']> }) {
  const [choix, setChoix] = useState<Record<string, number | boolean>>({});
  return (
    <div className="space-y-5">
      <div className="text-sm font-semibold text-emerald-200">✏️ À toi</div>
      {exercices.map((ex, e) => (
        <div key={e}>
          <p className="font-medium">{ex.prompt}</p>
          {ex.type === 'qcm' && (ex.choices || []).map((c, i) => {
            const pris = choix[`${e}`] === i;
            const juste = i === (ex.correct ?? 0);
            return (
              <button key={i} onClick={() => setChoix(s => ({ ...s, [`${e}`]: i }))}
                className={`mt-2 block w-full rounded-lg border px-3 py-2 text-left ${pris ? (juste ? 'border-emerald-400 bg-emerald-500/20' : 'border-rose-400 bg-rose-500/20') : 'border-white/15 hover:bg-white/5'}`}>
                {c}
              </button>
            );
          })}
          {ex.type === 'qcm' && choix[`${e}`] !== undefined && ex.explanation && <p className="mt-2 text-sm text-white/70">{ex.explanation}</p>}
          {ex.type === 'vrai_faux' && (ex.statements || []).map((st, i) => {
            const cle = `${e}:${i}`;
            const rep = choix[cle];
            return (
              <div key={i} className="mt-2 rounded-lg border border-white/15 px-3 py-2">
                <div>{st.text}</div>
                <div className="mt-1 flex gap-2">
                  {[true, false].map(v => (
                    <button key={String(v)} onClick={() => setChoix(s => ({ ...s, [cle]: v }))}
                      className={`rounded px-3 py-1 text-sm ${rep === v ? (v === st.correct ? 'bg-emerald-500/30' : 'bg-rose-500/30') : 'bg-white/10'}`}>
                      {v ? 'Vrai' : 'Faux'}
                    </button>
                  ))}
                </div>
                {rep !== undefined && st.explanation && <p className="mt-1 text-sm text-white/70">{st.explanation}</p>}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
