/**
 * L'évaluation formative de Tronc Commun (22 novembre 2026), même allure que la page d'un exercice (`ExercicePage`) :
 * le sujet sur une feuille blanche à gauche, la copie lignée à droite avec la marge du barème.
 *
 * Pas de chronomètre (demande de l'utilisateur : évaluation formative de préparation, 50 minutes au plus) : la durée
 * conseillée est affichée, l'élève avance à son rythme. Chaque réponse est corrigée dès qu'elle est donnée, en un seul
 * essai comme en examen : verdict, points par élément du barème, puis la correction expliquée.
 * Rien n'est gardé d'une visite à l'autre (règle du lien libre) : les réponses vivent le temps de la page.
 */
import { useEffect, useMemo, useRef, useState } from 'react';
import { Formule } from '../../components/course/Formule';
import ChampReponse from '../../components/course/SaisieReponse';
import ClavierFlottant, { clavier, hauteurClavierTelephone, largeurClavier, useClavier } from '../../components/course/ClavierFlottant';
import { lireNombre } from '../../components/exercice/juger';
import { pts } from '../../components/exercice/types';
import { EXAMEN, type PartieExamen, type QuestionExamen } from './sujet';
import FiguresCahier from '../../components/course/FigureCahier';
import { monExamen, suivre, useTempsPasse, type Progression } from './suivi';
import { lienDiapo, REVOIR_TC, type Lien } from './revoir';
import { Histogramme, histoVide, noterHisto, noterTriangle, Triangle, type Histo, type Ligne } from './Traces';
import { VOIX_EXAMEN } from './voixExamen';
import { inscrireVoix, taireTout } from '../../components/course/voixUnique';
import { BoutonTelephone, useVueTelephone, type VueTelephone } from '../../components/course/photoTelephone';

/** `partie/P1`, `question/1-1`, `correction/1-1` → la piste, si elle existe */
/** Ce qui change d'une page à l'autre (23/11/2026) : le Tronc Commun par défaut ; `/2bacpcf` appelle `utiliserSujet`. */
export interface ConfigExamen {
  sujet: typeof EXAMEN & { programme?: string };
  /** la voix d'une clé `partie/<id>`, `question/<id>`, `correction/<id>` */
  piste: (cle: string) => string | undefined;
  /** fiche, suivi, une seule réponse, ouverture après le cours : seulement là où il y a une fiche d'élève */
  suivi: boolean;
  /** matière donnée au tuteur et au clavier */
  matiere: string;
  /** l'accueil de la page (lien « retour ») */
  retour: string;
  /** la clé de cette évaluation dans le suivi (« examen » au Tronc Commun ; « examen_physique »… sur /2bacpcf) */
  cle?: string;
  /** les diapositives du cours qui expliquent une question (bilan : « à revoir », 24/11/2026) */
  revoir?: (question: string) => Lien[];
}
let CFG: ConfigExamen & { questions: { p: PartieExamen; q: QuestionExamen }[]; total: number } = config({
  sujet: { ...EXAMEN, programme: 'la sortie écologique ; les facteurs édaphiques (texture et structure, propriétés chimiques, propriétés hydriques du sol)' },
  piste: (cle: string) => (VOIX_EXAMEN.includes(cle) ? `/media/audio/courses/tc_svt_examen/${cle}.mp3` : undefined),
  suivi: true, matiere: 'svt', retour: 'Tronc Commun', revoir: q => REVOIR_TC[q] || [],
});
function config(c: ConfigExamen) {
  const questions = c.sujet.parties.flatMap(pa => pa.questions.map(q => ({ p: pa, q })));
  return { ...c, questions, total: questions.reduce((n, x) => n + x.q.points, 0) };
}
/** à appeler avant le premier rendu (une évaluation par page) */
export function utiliserSujet(c: ConfigExamen) { CFG = config(c); }
const piste = (cle: string) => CFG.piste(cle);
/** la configuration en cours (sujet, questions, matière) : le mode classe s'en sert (24/11/2026) */
export const configExamen = () => CFG;
let voixCourante: HTMLAudioElement | null = null;
function jouer(url?: string) {
  voixCourante?.pause();
  voixCourante = null;
  if (!url) return;
  taireTout();
  const a = new Audio(url);
  inscrireVoix(a);
  voixCourante = a;
  void a.play().catch(() => { /* lecture refusée avant un geste : l'élève relance */ });
}

const CRAIE = "'Patrick Hand', 'Caveat', cursive";
const SUJET = "'Times New Roman', Georgia, serif";
const BTN = 'rounded-md border border-slate-400 bg-white px-3 py-1.5 text-sm text-slate-900 hover:bg-slate-100';

export type Detail = { element: string; sur: number; obtenu: number; perte?: string };
export type Etat = {
  fait: boolean;
  /** QCM / vrai-faux : le choix de chaque item (index, ou vrai / faux) */
  choix?: (number | boolean | null)[];
  texte?: string;
  note?: number;
  verdict?: 'juste' | 'partiel' | 'faux' | 'nonjuge' | 'lecture';
  retour?: string;
  details?: Detail[];
  /** le tuteur n'a pas répondu : l'élève se note lui-même en comparant avec la correction */
  autoEval?: boolean;
  /** tracés : les lignes du triangle et la texture choisie ; le tableau, les rectangles et la courbe */
  lignes?: Partial<Record<'argile' | 'limon' | 'sable', Ligne>>; zone?: string; histo?: Histo;
};


export function texteDuSujet(p: PartieExamen) {
  const tab = p.tableau ? [p.tableau.entetes.join(' | '), ...p.tableau.lignes.map(l => l.join(' | '))].join(' ; ') : '';
  return [`Évaluation formative de ${CFG.sujet.matiere}, ${CFG.sujet.niveau} (Maroc) : ${p.titre}.`, p.intro || '', tab, ...(p.donnees || [])].filter(Boolean).join(' ');
}

/** la demande de correction d'une rédaction (barème, éléments) : la même pour l'évaluation et le mode classe */
export function corpsCorrection(p: PartieExamen, q: Extract<QuestionExamen, { genre: 'redaction' }>, reponse: string) {
  return {
    diapo: { title: `${CFG.sujet.niveau} — ${p.titre}`, speech: texteDuSujet(p) },
    question: { type: 'open', enonce: q.texte, attendu: q.attendu, matiere: CFG.matiere, bareme: q.points, elements: q.elements },
    // un seul essai, comme en examen : le tuteur corrige et donne la bonne réponse (pas d'indice pour réessayer)
    reponse: reponse.slice(0, 4000), tentative: 2, verdict: null,
  };
}
export type CorrectionTuteur = { correct: boolean | null; partiel?: boolean; parole: string; ecrit: string; note?: number; details?: Detail[] };
/** la réponse du tuteur → note, verdict, retour (même règle partout) */
export function etatDeCorrection(q: QuestionExamen, texte: string, r: CorrectionTuteur): Etat {
  // 25/11/2026 : le tuteur rend parfois un élément à 0 sans aucune perte (« ✓ » dans son commentaire) : un élément
  // sans perte expliquée garde ses points, et la note est la somme des éléments
  const details = r.details?.map(d => (d.obtenu < d.sur && !(d.perte || '').trim() ? { ...d, obtenu: d.sur } : d));
  const repare = !!details && details.some((d, k) => d.obtenu !== r.details![k].obtenu);
  const somme = details?.length ? Math.min(q.points, details.reduce((n, d) => n + d.obtenu, 0)) : undefined;
  const note = repare && somme != null ? somme : typeof r.note === 'number' ? r.note : r.correct === true ? q.points : r.partiel ? q.points / 2 : 0;
  const verdict = repare ? (note >= q.points ? 'juste' : note > 0 ? 'partiel' : 'faux')
    : r.correct === true ? 'juste' : r.partiel ? 'partiel' : r.correct === false ? 'faux' : 'nonjuge';
  return { fait: true, texte, verdict, note, retour: r.ecrit || r.parole, details };
}

async function corrigerParLeTuteur(p: PartieExamen, q: Extract<QuestionExamen, { genre: 'redaction' }>, reponse: string) {
  const r = await fetch('/api/v1/course-player/answer-reaction', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(corpsCorrection(p, q, reponse)),
  });
  if (!r.ok) throw new Error(String(r.status));
  return r.json() as Promise<CorrectionTuteur>;
}

/** QCM / vrai-faux : la note de chaque item (clé connue, dans le navigateur) */
export function noterChoix(q: Extract<QuestionExamen, { genre: 'qcm' | 'vf' }>, choix: (number | boolean | null | undefined)[]): Etat {
  const parItem = q.points / q.items.length;
  const justes = q.items.map((it, k) => (q.genre === 'qcm' ? choix[k] === (it as { bonne: number }).bonne : choix[k] === (it as { vrai: boolean }).vrai));
  const n = justes.filter(Boolean).length;
  return { fait: true, note: n * parItem, verdict: n === q.items.length ? 'juste' : n > 0 ? 'partiel' : 'faux',
    details: q.items.map((it, k) => ({ element: it.texte, sur: parItem, obtenu: justes[k] ? parItem : 0, perte: justes[k] ? '' : 'réponse fausse' })),
    retour: n === q.items.length ? 'Tout est juste.' : `${n} sur ${q.items.length} juste${n > 1 ? 's' : ''} : lis l’explication sous chaque proposition.` };
}

const motsDe = (s: string) => s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').split(/[^a-z0-9]+/).filter(m => m.length >= 3 && !['les', 'des', 'une', 'est', 'qui'].includes(m));
/** QCM ou vrai/faux lu sur une photo (25/11/2026, copies piégées) :
 *  - chaque ligne est rattachée à sa proposition par son repère (« c) », « ③ »), sinon par son rang : un élève qui
 *    répond dans le désordre (c, a, d, b) n'est plus noté sur la mauvaise proposition ;
 *  - une ligne donne une lettre (A–D, en majuscule ou en minuscule), le texte du choix (« ② ballon ») ou vrai / faux ;
 *  - deux réponses pour une même proposition (« B ou C ») : rien n'est retenu.
 *  `parLettres` : la lecture de choixDuTexte, gardée quand une ligne ne dit rien de plus. */
export function choixLus(q: Extract<QuestionExamen, { genre: 'qcm' | 'vf' }>, texte: string, parLettres: (number | boolean | null)[]): (number | boolean | null)[] {
  const n = q.items.length;
  const parRepere: (string | undefined)[] = Array(n).fill(undefined);
  const sansRepere: string[] = [];
  for (const brute of texte.split(/[\n;]+/)) {
    // le numéro de la question en tête de ligne (« 1) », « 1-1) », « Partie I - 1 ») n'est pas un repère de proposition
    let l = brute.replace(/^\s*(?:partie\s+[ivx]+\s*[-–:]?\s*)?(?:\d+\s*[-.]\s*\d+\s*\)|\d+\s*\)|\d+\s*[-–.]\s*(?=[a-h]\s*[).:-]))\s*/i, '').trim();
    while (l) {
      const m = l.match(/^(?:([a-h])\s*[).:-]|([①-⑧]))\s*/i);
      if (!m) { sansRepere.push(l); break; }
      const k = m[1] ? m[1].toLowerCase().charCodeAt(0) - 97 : m[2].charCodeAt(0) - 0x2460;
      // la suite de la ligne jusqu'au repère suivant (« a) A   b) A »)
      const reste = l.slice(m[0].length);
      const suivant = reste.search(/\s(?:[a-h]\s*[).:-]|[①-⑧])\s*/i);
      const contenu = suivant >= 0 ? reste.slice(0, suivant) : reste;
      if (k >= 0 && k < n && parRepere[k] === undefined) parRepere[k] = contenu.trim();
      l = suivant >= 0 ? reste.slice(suivant).trim() : '';
    }
  }
  const lignes = sansRepere.filter(Boolean);
  const reperes = parRepere.some(x => x !== undefined);
  return q.items.map((it, k) => {
    const brut = reperes ? parRepere[k] : lignes.length === n ? lignes[k] : undefined;
    if (brut === undefined) return parLettres[k] ?? null;
    if (q.genre === 'vf') {
      const vf = [...brut.matchAll(/\b(vrai|faux|v|f)\b/gi)].map(x => /^v/i.test(x[1]));
      // la première affirmation compte (« Faux, c'est l'inverse ») ; « vrai ou faux » sans choix : rien
      if (!vf.length || (/\bou\b/i.test(brut) && new Set(vf).size > 1)) return null;
      return vf[0];
    }
    const lettres = [...new Set([...brut.matchAll(/(?:^|[^A-Za-zÀ-ÿ])([A-Da-d])(?![A-Za-zÀ-ÿ₀-₉0-9])/g)].map(x => x[1].toUpperCase()))];
    if (lettres.length > 1) return null;
    const lm = new Set(motsDe(brut));
    let mieux: number | null = null, score = 0;
    (it as { choix: string[] }).choix.forEach((c, m) => {
      const cm = motsDe(c);
      const commun = cm.filter(w => lm.has(w)).length;
      const s = commun ? commun / cm.length + commun * 0.01 : 0;
      if (s > score) { score = s; mieux = m; }
    });
    // le texte d'un choix l'emporte ; sinon la lettre (une formule comme « C₂H₅ » n'est pas la lettre C)
    if (score >= 0.5) return mieux;
    return lettres.length === 1 ? lettres[0].charCodeAt(0) - 65 : null;
  });
}

/** Une photo de tout l'exercice (25/11/2026) : la copie lue, découpée entre les questions de l'exercice. Chaque réponse
 *  commence par le repère de sa question (« 1-5) », « 1.5 », « Q1-5 », « 3-a) », « 2) », ou « 5) » après « Exercice 1 ») ;
 *  le texte avant le premier repère va à la première question quand elle n'a pas de repère.
 *  → { id: texte de la réponse } ('' : rien trouvé pour cette question). */
export function decouperParQuestions(texte: string, ids: string[]): Record<string, string> {
  const lignes = texte.split(/\r?\n/);
  const motif = (id: string) => {
    const [a, b] = id.split('-');
    const q = '^\\s*(?:q(?:uestion)?\\s*)?';
    if (b === undefined) return new RegExp(`${q}${a}\\s*[)\\]:.–-](?!\\s*\\d)`, 'i');
    if (/^\d+$/.test(b)) return new RegExp(`${q}${a}\\s*[-.]\\s*${b}(?!\\d)\\s*[)\\]:.]?(?=\\s|$)`, 'i');
    return new RegExp(`${q}${a}\\s*[-.]?\\s*${b}\\s*[)\\]:.]`, 'i');
  };
  const motifs = ids.map(id => ({ id, re: motif(id) }));
  // « 5) » après « Exercice 1 » : la question 1-5
  let exercice: string | null = null;
  const debuts: { ligne: number; id: string }[] = [];
  const vus = new Set<string>();
  lignes.forEach((l, k) => {
    const ex = l.trim().match(/^ex(?:ercice|\.)?\s*(\d+)\b/i);
    if (ex) exercice = ex[1];
    let trouve = motifs.find(m => !vus.has(m.id) && m.re.test(l));
    if (!trouve && exercice) {
      const un = l.trim().match(/^(\d+)\s*[)\]:]/);
      if (un) trouve = motifs.find(m => !vus.has(m.id) && m.id === `${exercice}-${un[1]}`);
    }
    if (trouve) { vus.add(trouve.id); debuts.push({ ligne: k, id: trouve.id }); }
  });
  const out: Record<string, string> = Object.fromEntries(ids.map(id => [id, '']));
  debuts.forEach((d, i) => {
    const fin = i + 1 < debuts.length ? debuts[i + 1].ligne : lignes.length;
    out[d.id] = lignes.slice(d.ligne, fin).join('\n').trim();
  });
  // aucun repère : une seule question reçoit tout ; le texte avant le premier repère, à la première question sans repère
  const avant = lignes.slice(0, debuts.length ? debuts[0].ligne : lignes.length).join('\n').trim();
  if (avant) {
    const libre = ids.find(id => !out[id]);
    if (!debuts.length && ids.length === 1) out[ids[0]] = avant;
    else if (libre && libre === ids[0]) out[libre] = avant;
  }
  return out;
}

/** La partie d'une copie qui répond à la question `id` (« 1-1 », « 3-4 », « 2 ») : une photo prend souvent la page
 *  entière, avec d'autres questions (25/11/2026 : les « 1-1 » justes notés 0 parce que le dernier « = » de la page était
 *  celui de la 2-1). Repères reconnus en début de ligne : « 1-1) », « 1.1 : », « Q1-1 », « 1) » après « Exercice 1 ».
 *  `null` quand la copie n'a aucun repère pour cette question. */
export function partieDeLaQuestion(texte: string, id: string): string | null {
  const lignes = texte.split(/\r?\n/);
  const reperes: { ligne: number; id: string }[] = [];
  let exercice: string | null = null;
  lignes.forEach((brute, k) => {
    const l = brute.trim().replace(/^[*•\-–]\s*/, '');
    const ex = l.match(/^ex(?:ercice|\.)?\s*(\d+)\b/i);
    if (ex) { exercice = ex[1]; const reste = l.slice(ex[0].length).replace(/^\s*[:)\-–.]?\s*/, ''); if (!reste) return; }
    const deux = l.match(/^(?:q(?:uestion)?\s*)?(\d+)\s*[-.]\s*(\d+)\s*[)\]:.]?(?=\s|$)/i);
    if (deux) { reperes.push({ ligne: k, id: `${deux[1]}-${deux[2]}` }); return; }
    const un = l.match(/^(?:q(?:uestion)?\s*)?(\d+)\s*[)\]:](?=\s|$)/i);
    if (un) reperes.push({ ligne: k, id: exercice && id.includes('-') ? `${exercice}-${un[1]}` : un[1] });
  });
  const i = reperes.findIndex(r => r.id === id);
  if (i < 0) return null;
  const fin = i + 1 < reperes.length ? reperes[i + 1].ligne : lignes.length;
  return lignes.slice(reperes[i].ligne, fin).join(String.fromCharCode(10));
}

const EXPOSANTS: Record<string, string> = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁺': '+', '⁻': '-',
  '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9' };
/** une grandeur telle qu'on la compare (« [C₂H₅COOH]éq » → « [c2h5cooh] », « x_max » → « xmax ») */
export function formeGrandeur(s: string) {
  return s.toLowerCase().replace(/[⁰-⁹⁺⁻₀-₉¹²³]/g, c => EXPOSANTS[c] ?? c).replace(/[−–]/g, '-').replace(/éq|eq/g, '')
    .replace(/[_\s{}]/g, '').replace(/’/g, "'");
}

/** les lignes où l'élève écrit la grandeur demandée à gauche du premier « = » (une ligne qui commence par « = » continue
 *  la précédente). 25/11/2026 : « [C₂H₅COO⁻]éq = C = 5×10⁻² » était compté juste pour [C₂H₅COOH]éq. */
export function lignesDeLaGrandeur(partie: string, grandeur: string): string[] {
  const g = formeGrandeur(grandeur);
  if (!g) return [];
  const logiques: string[] = [];
  for (const l of partie.split(/\r?\n/)) {
    if (/^\s*[=≈]/.test(l) && logiques.length) logiques[logiques.length - 1] += ' ' + l.trim();
    else if (l.trim()) logiques.push(l);
  }
  return logiques.filter(l => {
    const gauche = l.split(/[=≈]/)[0];
    if (gauche === l) return false;
    const mots = gauche.trim().split(/\s+/).map(formeGrandeur);
    const dernier = (mots[mots.length - 1] || '').replace(/^\d+[-.]\d+\)?/, '').replace(/^\d+\)/, '');
    return g.length <= 3 ? dernier === g : formeGrandeur(gauche).includes(g);
  });
}

/** Un résultat écrit : le nombre et l'unité qui le suit (« 0,02 m » → 0,02 et « m »). */
export interface Resultat { valeur: number; unite: string }

/** les résultats écrits après un « = » ou un « ≈ » : seulement un membre qui est un nombre (avec sa puissance de dix et
 *  son unité), pas un calcul (« = 2Dθ » ne donne pas 2, « = 2 × 2,5 × 4×10⁻³ » ne donne pas 2) ; dans l'ordre.
 *  Une copie sans aucun « = » (« l'aire minimale est 16 m² ») : son premier nombre. */
export function resultatsEcrits(texte: string): Resultat[] {
  const membres = texte.split(/[=≈]/).slice(1).map(m => m.split(/\r?\n/)[0].trim());
  const tete = /^[-−+]?\s*\d+(?:[.,]\d+)?(?:e[-−+]?\d+(?![\d.,])|\s*[×x·*.]\s*10\s*(?:\^\s*\(?\s*[-−]?\d+(?:[.,]\d+)?\s*\)?|[⁻⁺]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+|-\d+))?/;
  const lu = (brut: string): Resultat | null => {
    // « 4.10⁻³ » : le point devant 10 et son exposant est un « fois »
    const m = brut.replace(/(\d)\s*\.\s*10(?=\s*(?:\^|[⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹]))/g, '$1×10');
    const t = m.match(tete);
    if (!t) return null;
    const reste = m.slice(t[0].length);
    // après le nombre : rien, ou une unité séparée par une espace (ou %, °) ; ni chiffre, ni opération, ni lettre grecque
    // collée (« 2Dθ », « 2τ » sont des relations)
    if (reste && !/^(\s|%|°)/.test(reste)) return null;
    if (/[0-9]|^\s*[×x·*/+^(-]|[α-ωϑϕ]/.test(reste)) return null;
    if (/\bou\b/i.test(reste)) return null;
    const v = lireNombre('=' + t[0]);
    return v == null ? null : { valeur: v, unite: reste.trim().split(/[\s,;.)]+/)[0] || '' };
  };
  const vus = membres.map(lu).filter((r): r is Resultat => r != null);
  if (vus.length || /[=≈]/.test(texte)) return vus;
  const m = texte.match(/[-−]?\d+(?:[.,]\d+)?(?:\s*[×x·*]\s*10\s*[⁻⁺]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)?(?:\s*[%°]|\s+[a-zA-Zµ/²³⁻¹]+)?/);
  return m ? [lu(m[0])].filter((r): r is Resultat => r != null) : [];
}

/** unités convertibles (même grandeur) : la valeur d'une unité dans l'unité de base */
const UNITES_CONV: Record<string, [string, number]> = {
  km: ['m', 1e3], m: ['m', 1], dm: ['m', 0.1], cm: ['m', 1e-2], mm: ['m', 1e-3], µm: ['m', 1e-6], um: ['m', 1e-6], nm: ['m', 1e-9],
  kg: ['kg', 1], g: ['kg', 1e-3], mg: ['kg', 1e-6],
  s: ['s', 1], ms: ['s', 1e-3], min: ['s', 60], h: ['s', 3600], j: ['s', 86400], jour: ['s', 86400], jours: ['s', 86400],
  mol: ['mol', 1], mmol: ['mol', 1e-3],
  l: ['l', 1], ml: ['l', 1e-3], cl: ['l', 1e-2],
};
/** une valeur écrite dans une autre unité que celle demandée, ramenée à l'unité demandée (0,02 m → 2 cm ;
 *  2,6 % → 0,026 quand on attend une valeur décimale) ; null si on ne sait pas convertir */
export function versUniteDemandee(r: Resultat, unites: string[]): number | null {
  const u = r.unite.toLowerCase();
  const demandee = (unites[0] || '').toLowerCase().trim();
  if (u === '%' && !demandee.includes('%')) return r.valeur / 100;
  const a = UNITES_CONV[u], b = UNITES_CONV[demandee];
  if (!a || !b || a[0] !== b[0] || u === demandee) return null;
  return r.valeur * a[1] / b[1];
}

export function jugerValeur(q: Extract<QuestionExamen, { genre: 'valeur' }>, texte: string): Etat {
  // seule la partie de la copie qui répond à cette question compte ; sans repère, toute la copie ; et dans cette partie,
  // les lignes de la grandeur demandée quand l'élève l'a écrite
  const toute = partieDeLaQuestion(texte, q.id) ?? texte;
  const lignes = lignesDeLaGrandeur(toute, q.grandeur);
  const partie = lignes.length ? lignes.join(String.fromCharCode(10)) : toute;
  const tol = q.tolerance ?? 0.02;
  // la tolérance est relative à la valeur attendue (25/11/2026 : l'ancien plancher de 10⁻¹² acceptait n'importe quel
  // nombre devant 4×10⁻²⁶ kg ou 3,2×10⁻¹⁹ C, même de signe contraire)
  const bon = (v: number) => (q.valeur === 0 ? Math.abs(v) <= 1e-9 : Math.abs(v - q.valeur) <= tol * Math.abs(q.valeur));
  const resultats = resultatsEcrits(partie);
  // une conversion d'unités entre deux résultats (« 2×10⁻² m = 2 cm ») n'est pas un second résultat
  const conversion = (a: number, b: number) => { if (!a || !b) return false; const r = Math.log10(Math.abs(a / b)); return Math.abs(r - Math.round(r)) < 0.01 && Math.sign(a) === Math.sign(b); };
  const k = resultats.findIndex(r => bon(r.valeur));
  // 25/11/2026 (copies piégées) : le bon nombre suivi d'un autre résultat (« = 5,1×10⁻⁴ » puis « = 3,29×10⁻¹ ») n'est
  // pas juste : la réponse de l'élève est la dernière
  const juste = k >= 0 && resultats.slice(k + 1).every(r => bon(r.valeur) || conversion(r.valeur, q.valeur));
  const contradiction = k >= 0 && !juste;
  // juste dans une autre unité que celle demandée (0,02 m pour 2 cm ; 2,6 % pour 0,026) : le résultat, pas l'unité
  const dernier = resultats[resultats.length - 1];
  const converti = !juste && dernier ? versUniteDemandee(dernier, q.unites) : null;
  const justeAutreUnite = converti != null && bon(converti);
  const lu = juste ? q.valeur : dernier ? dernier.valeur : null;
  const t = toute.toLowerCase().replace(/\s+/g, ' ');
  // une unité d'une ou deux lettres (« C », « j », « m ») doit être un mot à elle seule
  const unite = !justeAutreUnite && q.unites.some(u => { const v = u.toLowerCase().trim(); if (!v) return true;
    return v.length <= 2 ? new RegExp(`(^|[^a-zà-ÿ])${v.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}([^a-zà-ÿ]|$)`).test(t) : t.includes(v); });
  const bonNombre = juste || justeAutreUnite;
  const sansUnite = bonNombre && !unite && q.points > 0.25;
  // le résultat porte les points ; l'unité vaut 0,25 point quand la question en vaut plus
  const surUnite = q.points > 0.25 ? 0.25 : 0;
  const details: Detail[] = [{ element: 'Relation, application numérique et résultat', sur: q.points - surUnite, obtenu: bonNombre ? q.points - surUnite : 0,
    perte: bonNombre ? '' : contradiction ? RESULTATS_CONTRADICTOIRES : lu == null ? 'pas de résultat chiffré' : 'résultat faux' }];
  if (surUnite) details.push({ element: 'Unité du résultat', sur: surUnite, obtenu: bonNombre && unite ? surUnite : 0,
    perte: justeAutreUnite ? `résultat donné en ${dernier!.unite}, demandé en ${q.unites[0] || 'valeur décimale'}` : bonNombre && !unite ? 'unité manquante' : !bonNombre ? 'résultat faux' : '' });
  const note = details.reduce((n, d) => n + d.obtenu, 0);
  return { fait: true, texte, note, details, verdict: bonNombre ? (sansUnite || justeAutreUnite ? 'partiel' : 'juste') : 'faux',
    retour: justeAutreUnite ? `Le résultat est juste, mais il est demandé en ${q.unites[0] || 'valeur décimale'} : convertis-le.`
      : bonNombre ? (sansUnite ? 'Le nombre est juste, mais l’unité manque : sur la copie, elle compte.' : 'Le résultat est juste, avec son unité.')
      : contradiction ? 'Tu donnes deux résultats différents pour la même grandeur : sur la copie, le résultat est compté faux.'
      : lu == null ? 'Je ne trouve pas de résultat chiffré dans ta réponse.' : `Ton résultat (${String(lu).replace('.', ',')}) n’est pas le bon : regarde la correction.` };
}
/** deux résultats différents pour la même grandeur : le correcteur ne choisit pas pour l'élève */
export const RESULTATS_CONTRADICTOIRES = 'deux résultats différents';

/** la demande de correction d'un calcul au tuteur : noté sur les étapes de la correction (relation, application
 *  numérique, résultat, conclusion) */
export function corpsValeur(p: PartieExamen, q: Extract<QuestionExamen, { genre: 'valeur' }>, reponse: string) {
  return {
    diapo: { title: `${CFG.sujet.niveau} — ${p.titre}`, speech: texteDuSujet(p) },
    question: { type: 'open', enonce: q.texte, attendu: q.correction.join(' '), matiere: CFG.matiere, bareme: q.points, elements: q.correction },
    reponse: reponse.slice(0, 4000), tentative: 2, verdict: null,
  };
}
const auQuart = (n: number) => Math.round(n * 4) / 4;
/** la question demande aussi une conclusion (« Conclure », « En déduire… la nature ») : un nombre juste ne suffit pas */
export const demandeConclusion = (q: QuestionExamen) => /\bconclu|\?\s*$/i.test(q.texte.trim());

/** Un calcul noté comme sur la copie du national (25/11/2026, banc de 51 copies) :
 *  - résultat juste : la note du résultat ; si la question demande une conclusion, le tuteur la note aussi (elle vaut
 *    au plus 20 % des points) ;
 *  - résultat faux : la relation et l'application numérique justes gardent leurs points, notés par le tuteur sur les
 *    étapes de la correction (jamais plus de 60 % des points sans le bon résultat).
 *  `corriger` : l'appel au tuteur de la page (évaluation ou mode classe). Sans réponse du tuteur : la note du résultat. */
export async function noterValeur(p: PartieExamen, q: Extract<QuestionExamen, { genre: 'valeur' }>, texte: string,
  corriger: (corps: ReturnType<typeof corpsValeur>) => Promise<CorrectionTuteur>): Promise<Etat> {
  const r = jugerValeur(q, texte);
  const juste = r.verdict === 'juste' || r.verdict === 'partiel';
  if (!texte.trim() || (juste && !demandeConclusion(q)) || r.details?.[0]?.perte === RESULTATS_CONTRADICTOIRES) return r;
  try {
    const t = etatDeCorrection(q, texte, await corriger(corpsValeur(p, q, texte)));
    const tuteur = t.note ?? 0;
    if (juste) {
      const n = auQuart(Math.min(r.note ?? 0, Math.max(tuteur, (r.note ?? 0) - q.points * 0.2)));
      return n >= (r.note ?? 0) ? r : { ...t, note: n, verdict: 'partiel', details: t.details ?? r.details };
    }
    const n = auQuart(Math.min(tuteur, q.points * 0.6));
    if (n <= 0) return r;
    return { ...t, note: n, verdict: 'partiel',
      retour: `Le résultat n’est pas le bon, mais ta démarche rapporte des points. ${t.retour || ''}`.trim() };
  } catch {
    return r;
  }
}

export default function Examen() {
  const [commence, setCommence] = useState(false);
  const [i, setI] = useState(0);
  const [etats, setEtats] = useState<Record<string, Etat>>({});
  const [sujetVu, setSujetVu] = useState(true);
  const clavierOuvert = useClavier().ouvert;
  useEffect(() => { clavier.matiere(CFG.matiere === 'svt' ? 'svt' : 'physique-chimie'); }, []);
  useTempsPasse(CFG.cle || 'examen', commence && CFG.suivi);
  useEffect(() => { if (commence && CFG.suivi) suivre({ type: 'examen_debut', cours: CFG.cle || 'examen' }); }, [commence]);
  // une seule réponse compte (23/11/2026) : les questions déjà rendues reviennent du serveur, verrouillées
  const [repris, setRepris] = useState<'attente' | 'neuf' | 'suite' | 'fini'>('attente');
  // l'évaluation s'ouvre après la révision ou un des deux cours (23/11/2026) ; hors ligne, sans réponse du serveur : ouverte
  const [acces, setAcces] = useState<{ ouvert: boolean; progression?: Progression; seuil?: number }>({ ouvert: true });
  useEffect(() => {
    if (!CFG.suivi) { setRepris('neuf'); return; }
    void monExamen(CFG.cle || 'examen').then(d => {
      const qs = d?.questions || {};
      const ids = Object.keys(qs).filter(id => CFG.questions.some(x => x.q.id === id));
      if (ids.length) {
        const restes: Record<string, Etat> = {};
        for (const id of ids) restes[id] = { ...(qs[id] as Etat), fait: true };
        for (const id of ids) { envoyes.current[id] = `${restes[id].note}|${restes[id].verdict}`; dejaFait.current[id] = true; }
        if (d?.fini) envoyes.current.__fin = '1';
        setEtats(restes);
        const k = CFG.questions.findIndex(x => !restes[x.q.id]);
        setI(k < 0 ? CFG.questions.length - 1 : k);
      }
      setRepris(d?.fini ? 'fini' : ids.length ? 'suite' : 'neuf');
      if (d) setAcces({ ouvert: d.ouvert !== false, progression: d.progression, seuil: d.seuil });
    });
  }, []);

  const { p, q } = CFG.questions[i];
  // la voix se tait quand on change de question ; la correction se dit dès que la réponse est notée
  useEffect(() => () => jouer(undefined), [i]);
  const faitIci = !!etats[q.id]?.fait;
  const dejaFait = useRef<Record<string, boolean>>({});
  useEffect(() => {
    if (faitIci && !dejaFait.current[q.id]) { dejaFait.current[q.id] = true; jouer(piste(`correction/${q.id}`)); }
  }, [faitIci, q.id]);
  const etat: Etat = etats[q.id] || { fait: false };
  const poser = (id: string, e: Partial<Etat>) => setEtats(s => ({ ...s, [id]: { ...(s[id] || { fait: false }), ...e } }));
  const note = Object.values(etats).reduce((n, e) => n + (e.fait && typeof e.note === 'number' ? e.note : 0), 0);
  const faites = CFG.questions.filter(x => etats[x.q.id]?.fait).length;
  const fini = faites === CFG.questions.length;
  const pointsFaits = CFG.questions.filter(x => etats[x.q.id]?.fait).reduce((n, x) => n + x.q.points, 0);

  const rendreTrace = () => {
    if (q.genre === 'triangle') {
      const details = noterTriangle(q, etat.lignes || {}, etat.zone || '');
      const n = details.reduce((s, d) => s + d.obtenu, 0);
      poser(q.id, { fait: true, note: n, details, verdict: n >= q.points ? 'juste' : n > 0 ? 'partiel' : 'faux',
        texte: `${Object.entries(etat.lignes || {}).map(([a, l]) => `${a} ${l!.v} % ∥ ${l!.garde}`).join(' ; ')} → ${etat.zone || '?'}`,
        retour: n >= q.points ? 'Les trois lignes et la texture sont justes.' : 'Compare tes lignes (en couleur) avec les bonnes (en rouge pointillé).' });
    } else if (q.genre === 'histogramme') {
      const h = etat.histo || histoVide();
      const details = noterHisto(q, h);
      const n = details.reduce((s, d) => s + d.obtenu, 0);
      poser(q.id, { fait: true, note: n, details, verdict: n >= q.points ? 'juste' : n > 0 ? 'partiel' : 'faux',
        texte: `tableau ${h.tableau.join('·')} ; rectangles ${h.barres.join('·')} ; courbe ${h.points.join('·')}`,
        retour: n >= q.points ? 'Tableau, rectangles collés et courbe : tout est juste.' : 'Compare avec la correction en rouge pointillé.' });
    }
  };

  const validerChoix = () => {
    if (q.genre !== 'qcm' && q.genre !== 'vf') return;
    poser(q.id, noterChoix(q, etat.choix || []));
  };

  const repondre = async (texte: string) => {
    if (q.genre === 'valeur') {
      const vite = jugerValeur(q, texte);
      // un résultat juste sans conclusion demandée est noté tout de suite ; sinon le tuteur lit la démarche
      if ((vite.verdict === 'juste' || vite.verdict === 'partiel') && !demandeConclusion(q)) { poser(q.id, vite); return; }
      poser(q.id, { texte, verdict: 'lecture', retour: 'Le tuteur lit ta démarche…' });
      poser(q.id, await noterValeur(p, q, texte, async corps => {
        const r = await fetch('/api/v1/course-player/answer-reaction', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(corps) });
        if (!r.ok) throw new Error(String(r.status));
        return r.json() as Promise<CorrectionTuteur>;
      }));
      return;
    }
    if (q.genre !== 'redaction') return;
    poser(q.id, { texte, verdict: 'lecture', retour: 'Le tuteur lit ta réponse…' });
    try {
      const r = await corrigerParLeTuteur(p, q, texte);
      poser(q.id, etatDeCorrection(q, texte, r));
    } catch {
      poser(q.id, { fait: false, texte, autoEval: true, verdict: undefined, retour: '' });
    }
  };

  // chaque question notée part au suivi (onglet admin « Tronc Commun ») : note, verdict, éléments du barème perdus
  const envoyes = useRef<Record<string, string>>({});
  useEffect(() => {
    if (!CFG.suivi) return;
    for (const { p: pa, q: x } of CFG.questions) {
      const e = etats[x.id];
      if (!e?.fait) continue;
      const sig = `${e.note}|${e.verdict}`;
      if (envoyes.current[x.id] === sig) continue;
      envoyes.current[x.id] = sig;
      suivre({ type: 'examen_question', cours: CFG.cle || 'examen', question_id: x.id, partie: pa.titre, note: e.note || 0, sur: x.points,
        verdict: e.verdict, enonce: x.texte, reponse: e.texte || (e.choix || []).map(c => String(c)).join(' ; '),
        pertes: (e.details || []).filter(d => d.obtenu < d.sur).map(d => `${d.element} : ${d.perte || 'manque'}`),
        // ce qu'il faut pour remontrer la question telle quelle si l'élève revient
        etat: { fait: true, choix: e.choix, texte: e.texte?.slice(0, 4000), note: e.note, verdict: e.verdict, retour: e.retour?.slice(0, 700),
          details: e.details, lignes: e.lignes, zone: e.zone, histo: e.histo } });
    }
    if (CFG.questions.every(x => etats[x.q.id]?.fait) && !envoyes.current.__fin) {
      envoyes.current.__fin = '1';
      suivre({ type: 'examen_fin', cours: CFG.cle || 'examen', note: Object.values(etats).reduce((n, e) => n + (e.note || 0), 0), sur: CFG.total });
    }
  }, [etats]);

  const parPartie = useMemo(() => CFG.sujet.parties.map(pa => ({
    pa, sur: pa.questions.reduce((n, x) => n + x.points, 0),
    note: pa.questions.reduce((n, x) => n + (etats[x.id]?.fait ? etats[x.id].note || 0 : 0), 0),
  })), [etats]);

  // liens libres (24/11/2026) : le téléphone relié montre la même question, la suit, y répond (clavier ou photo) ; la page suit
  // aussi le téléphone quand il change de question. Rien ici sans `activerPhotoTelephone` (site principal).
  const vueTel: VueTelephone | null = commence ? {
    titre: CFG.sujet.titre,
    questions: CFG.questions.map(x => ({ id: x.q.id, fait: !!etats[x.q.id]?.fait })),
    courante: { id: q.id, partie: p.titre, texte: q.texte, points: q.points, matiere: CFG.matiere,
      genre: q.genre === 'qcm' || q.genre === 'vf' || q.genre === 'valeur' ? q.genre : q.genre === 'redaction' ? 'texte' : 'trace',
      items: q.genre === 'qcm' ? q.items.map(it => ({ texte: it.texte, choix: it.choix })) : q.genre === 'vf' ? q.items.map(it => ({ texte: it.texte })) : undefined,
      aide: q.genre === 'valeur' ? `${q.grandeur} = … = résultat avec son unité` : undefined },
    brouillon: etat.choix ? { choix: etat.choix } : undefined,
    resultat: etat.fait ? { verdict: etat.verdict, note: etat.note, sur: q.points, retour: etat.retour?.slice(0, 1500), details: etat.details } : null,
    occupe: etat.verdict === 'lecture' ? 'Le tuteur lit ta réponse…' : etat.autoEval && !etat.fait ? 'Le tuteur n’est pas joignable : compare avec la correction sur ton PC.' : '',
  } : null;
  useVueTelephone(vueTel, m => {
    if (m.type === 'aller') { const k = CFG.questions.findIndex(x => x.q.id === m.question); if (k >= 0) setI(k); return; }
    if (m.type !== 'choix' || (q.genre !== 'qcm' && q.genre !== 'vf') || (m.question && m.question !== q.id) || etats[q.id]?.fait) return;
    const c = q.items.map((_, k) => m.choix[k] ?? null);
    if (m.rendre && c.every(x => x !== null)) poser(q.id, { ...noterChoix(q, c), choix: c });
    else poser(q.id, { choix: c });
  });

  // Refaire l'évaluation (25/11/2026, tous les niveaux) : même terminée, l'élève recommence de zéro ; sa nouvelle copie
  // remplace l'ancienne (note comprise) dans l'espace admin. Le serveur ne garde que la dernière tentative.
  const refaire = async () => {
    if (!window.confirm('Refaire l’évaluation : tu recommences de zéro, et ta nouvelle copie remplacera l’ancienne (note comprise). Continuer ?')) return;
    jouer(undefined);
    if (CFG.suivi) await suivre({ type: 'examen_reprise', cours: CFG.cle || 'examen' });
    envoyes.current = {};
    dejaFait.current = {};
    setEtats({});
    setI(0);
    setSujetVu(true);
    setRepris('neuf');
    setCommence(true);
  };

  if (!commence) return <Accueil etat={repris} acces={acces} onCommencer={() => setCommence(true)} onRefaire={refaire} />;

  // « Terminer l'évaluation » : les questions sans réponse comptent 0, verrouillées, puis le bilan
  const terminer = () => {
    const reste = CFG.questions.filter(x => !etats[x.q.id]?.fait);
    if (reste.length && !window.confirm(`Il reste ${reste.length} question${reste.length > 1 ? 's' : ''} sans réponse : ${reste.length > 1 ? 'elles compteront' : 'elle comptera'} 0 point et tu ne pourras plus y répondre. Terminer quand même ?`)) return;
    setEtats(s => {
      const n = { ...s };
      for (const x of reste) n[x.q.id] = { fait: true, note: 0, verdict: 'faux', retour: 'Pas de réponse : 0 point. Lis la correction.',
        details: [{ element: 'Réponse', sur: x.q.points, obtenu: 0, perte: 'pas de réponse' }] };
      return n;
    });
  };

  const noteQ = etat.fait && typeof etat.note === 'number' ? etat.note : null;
  const LIGNES = { lineHeight: '36px', backgroundImage: 'repeating-linear-gradient(transparent 0 35px, #9bb3d6 35px 36px)' };
  const debutPartie = CFG.questions.findIndex(x => x.p === p);

  return (
    <div className="flex h-[100dvh] w-screen flex-col bg-[#d6d6d0] text-black" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <header className="flex shrink-0 flex-wrap items-center gap-2 border-b border-slate-400 bg-white px-3 py-1.5 [@media(max-height:520px)]:py-0.5">
        <a href="./" className={`${BTN} [@media(max-height:520px)]:py-0.5`}>← {CFG.retour}</a>
        <h1 className="min-w-0 flex-1 truncate text-base font-semibold sm:text-lg">{CFG.sujet.titre}</h1>
        <span className="hidden rounded border border-slate-500 px-2 py-0.5 text-sm text-slate-700 sm:inline" title="Durée conseillée, sans chronomètre">⏳ {CFG.sujet.minutes} min conseillées</span>
        <span className="rounded border border-black px-2 py-0.5 text-sm font-semibold">Note : {pts(note)} / {pts(pointsFaits)}{fini ? '' : ` · ${faites}/${CFG.questions.length}`}</span>
        <BoutonTelephone clair />
        {!fini && <button onClick={terminer} className="rounded-md border border-rose-700 bg-rose-50 px-2.5 py-1 text-sm font-semibold text-rose-800 hover:bg-rose-100 [@media(max-height:520px)]:py-0.5">Terminer l’évaluation</button>}
      </header>

      <div className="flex min-h-0 flex-1 gap-2 p-2 sm:gap-3 sm:p-3 [@media(max-height:520px)]:p-1"
        style={{ paddingRight: largeurClavier(clavierOuvert) || undefined, paddingBottom: hauteurClavierTelephone(clavierOuvert) || undefined }}>
        {/* Le sujet : feuille blanche, écriture noire */}
        {sujetVu && (
          <section className="w-[42%] shrink-0 overflow-y-auto bg-white p-3 text-black shadow-md ring-1 ring-black/10 sm:p-5" style={{ fontFamily: SUJET }}>
            <div className="mb-2 flex flex-wrap gap-1" style={{ fontFamily: 'system-ui, sans-serif' }}>
              {CFG.sujet.parties.map(pa => {
                const k = CFG.questions.findIndex(x => x.p === pa);
                const toutes = pa.questions.every(x => etats[x.id]?.fait);
                return <button key={pa.id} onClick={() => setI(k)} className={`rounded border px-2 py-0.5 text-xs ${pa === p ? 'border-black bg-black text-white' : toutes ? 'border-emerald-700 text-emerald-800' : 'border-slate-400'}`}>
                  {pa.court || (pa.id === 'P1' ? 'Partie I' : `Ex. ${Number(pa.id.slice(1)) - 1}`)}</button>;
              })}
            </div>
            <h2 className="text-[17px] font-bold underline underline-offset-4">{p.titre}</h2>
            {piste(`partie/${p.id}`) && <button onClick={() => jouer(piste(`partie/${p.id}`))} className={`mt-1 ${BTN}`} style={{ fontFamily: 'system-ui, sans-serif' }}>🔊 Écouter</button>}
            <p className="mt-0.5 text-[13px] text-slate-600" style={{ fontFamily: 'system-ui, sans-serif' }}>{pts(p.questions.reduce((n, x) => n + x.points, 0))} points · environ {p.minutes} min</p>
            <DonneesPartie p={p} />
            <table className="mt-3 w-full border-collapse text-[15px]">
              <tbody>{p.questions.map((x, k) => {
                const e = etats[x.id];
                const v = e?.fait ? (e.note || 0) >= x.points ? '✔' : (e.note || 0) > 0 ? '◐' : '✘' : '';
                return (
                  <tr key={x.id} onClick={() => setI(debutPartie + k)} className={`cursor-pointer align-top ${x === q ? 'bg-amber-100' : 'hover:bg-slate-50'}`}>
                    <td className="w-12 border-r border-slate-400 py-1 pr-1.5 text-right text-[13px] font-semibold" style={{ fontFamily: 'system-ui, sans-serif' }}>{pts(x.points)} pt</td>
                    <td className="py-1 pl-2"><b>{x.id}.</b> <Formule t={x.texte} /> <span className={v === '✔' ? 'text-emerald-700' : v === '◐' ? 'text-amber-700' : 'text-rose-700'}>{v}</span></td>
                  </tr>);
              })}</tbody>
            </table>
          </section>)}

        {/* La copie : cadre, marge du barème, lignes */}
        <section className="flex min-h-0 min-w-0 flex-1 flex-col overflow-y-auto bg-white text-black shadow-md ring-1 ring-black/10">
          <table className="w-full shrink-0 border-collapse text-[15px]">
            <tbody><tr>
              <td className="border-2 border-black px-2 py-1 font-bold">Question {q.id}</td>
              <td className="w-28 border-2 border-black px-1 py-1 text-center">Barème : <b>{pts(q.points)}</b></td>
              <td className="w-28 border-2 border-black px-1 py-1 text-center">Note : <b className={noteQ === null ? '' : noteQ > 0 ? 'text-emerald-700' : 'text-rose-700'}>{noteQ === null ? '……' : pts(noteQ)}</b></td>
            </tr></tbody>
          </table>
          <div className="flex flex-wrap items-center gap-1 border-b border-slate-300 px-2 py-1 text-sm text-slate-600">
            <button onClick={() => setSujetVu(v => !v)} className="mr-1 rounded border border-slate-400 px-1.5 text-xs">{sujetVu ? '◀ Sujet' : '▶ Sujet'}</button>
            {CFG.questions.map((x, k) => {
              const e = etats[x.q.id];
              const c = k === i ? 'border-black bg-black text-white' : !e?.fait ? 'border-slate-400' : (e.note || 0) >= x.q.points ? 'border-emerald-700 text-emerald-700' : (e.note || 0) > 0 ? 'border-amber-600 text-amber-700' : 'border-rose-700 text-rose-700';
              return <button key={x.q.id} onClick={() => setI(k)} className={`h-6 min-w-7 rounded border px-1 text-xs ${c}`} aria-label={`Question ${x.q.id}`}>{x.q.id}</button>;
            })}
          </div>

          <div className="flex min-h-0 flex-1">
            <div className="w-12 shrink-0 border-r-2 border-rose-400 pt-3 text-center sm:w-14">
              <span className="inline-block rounded border border-black px-1 text-[13px] font-semibold">{pts(q.points)}</span>
              {noteQ !== null && <p className={`mt-2 text-lg font-bold ${noteQ > 0 ? 'text-emerald-700' : 'text-rose-700'}`} style={{ fontFamily: CRAIE }}>{pts(noteQ)}</p>}
            </div>

            <div className="min-w-0 flex-1 p-2 sm:p-4">
              <p className="text-[17px] font-semibold" style={{ fontFamily: SUJET }}><span>{q.id}.</span> <Formule t={q.texte} /></p>
              {piste(`question/${q.id}`) && <button onClick={() => jouer(piste(`question/${q.id}`))} className={`mt-1 ${BTN}`}>🔊 La question</button>}

              {(q.genre === 'qcm' || q.genre === 'vf') && (
                <Choix q={q} etat={etat} onChoisir={(k, v) => setEtats(s => {
                  const e = s[q.id] || { fait: false };
                  if (e.fait) return s;
                  const c = [...(e.choix || q.items.map(() => null))]; c[k] = v;
                  return { ...s, [q.id]: { ...e, choix: c } };
                })} />)}
              {(q.genre === 'qcm' || q.genre === 'vf') && etat.fait && piste(`correction/${q.id}`) && (
                <button onClick={() => jouer(piste(`correction/${q.id}`))} className={`mt-3 ${BTN}`}>🔊 La correction expliquée</button>)}
              {(q.genre === 'qcm' || q.genre === 'vf') && !etat.fait && (
                <button disabled={(etat.choix || []).filter(x => x !== null && x !== undefined).length < q.items.length} onClick={validerChoix}
                  className="mt-3 rounded-md bg-black px-4 py-1.5 text-sm font-semibold text-white disabled:opacity-40">Valider mes réponses</button>)}

              {q.genre === 'triangle' && (
                <div className="mt-2">
                  <Triangle sol={q.sol} actif={!etat.fait} correction={etat.fait} lignes={etat.lignes || {}}
                    onLigne={(axe, l) => setEtats(s => ({ ...s, [q.id]: { ...(s[q.id] || { fait: false }), lignes: { ...(s[q.id]?.lignes || {}), [axe]: l } } }))} />
                  <label className="mt-2 flex flex-wrap items-center gap-2 text-[15px]" style={{ fontFamily: 'system-ui, sans-serif' }}>③ La texture du sol C :
                    <select disabled={etat.fait} value={etat.zone || ''} onChange={e => poser(q.id, { zone: e.target.value })} className="rounded-md border border-slate-400 px-2 py-1">
                      <option value="">— choisis —</option>{q.choix.map(c => <option key={c} value={c}>{c}</option>)}
                    </select></label>
                  {!etat.fait && <button disabled={Object.keys(etat.lignes || {}).length < 3 || !etat.zone} onClick={rendreTrace}
                    className="mt-3 rounded-md bg-black px-4 py-1.5 text-sm font-semibold text-white disabled:opacity-40">Rendre ma réponse</button>}
                </div>)}
              {q.genre === 'histogramme' && (
                <div className="mt-2">
                  <div className="mb-2 border border-black p-2 text-[14px]" style={{ fontFamily: 'system-ui, sans-serif' }}>
                    <p className="mb-1 font-bold">Espèces et indice de fréquence :</p>
                    <p className="leading-relaxed">{q.especes.map(([e, i]) => `${e} (${i})`).join(' · ')}</p>
                  </div>
                  <Histogramme comptes={q.comptes} actif={!etat.fait} correction={etat.fait} h={etat.histo || histoVide()} onH={h => poser(q.id, { histo: h })} />
                  {!etat.fait && <button disabled={!(etat.histo && [...etat.histo.tableau, ...etat.histo.barres, ...etat.histo.points].every(v => v != null))} onClick={rendreTrace}
                    className="mt-3 rounded-md bg-black px-4 py-1.5 text-sm font-semibold text-white disabled:opacity-40">Rendre ma réponse</button>}
                </div>)}
              {(q.genre === 'valeur' || q.genre === 'redaction') && !etat.fait && etat.verdict !== 'lecture' && !etat.autoEval && (
                <div className="mt-2">
                  <ChampReponse key={q.id} papier onEnvoyer={t => void repondre(t)} libelle="Rendre ma réponse" lignes={q.genre === 'valeur' ? 3 : 6}
                    placeholder={q.genre === 'valeur' ? `${q.grandeur} = … = résultat avec son unité` : 'Ta réponse, rédigée et justifiée…'}
                    contexte={{ title: p.titre, enonce: q.texte, matiere: CFG.matiere, chapitre: CFG.sujet.titre }}
                    suggestions={{ slide_id: `examen_${q.id}`, enonce: q.texte, clavier: { aides: [] } }} />
                </div>)}
              {etat.texte && q.genre !== 'triangle' && q.genre !== 'histogramme' && (etat.fait || etat.verdict === 'lecture' || etat.autoEval) && (
                <p className="mt-2 whitespace-pre-wrap text-[20px] text-black" style={{ fontFamily: CRAIE, ...LIGNES }}>{etat.texte}</p>)}

              {etat.retour && <Verdict etat={etat} />}

              {(etat.fait || etat.autoEval) && (q.genre === 'valeur' || q.genre === 'redaction' || q.genre === 'triangle' || q.genre === 'histogramme') && (
                <div className="mt-3 border-2 border-rose-700 p-2 sm:p-3">
                  <div className="mb-1 flex items-center gap-2"><p className="flex-1 font-bold text-rose-800">✍️ Correction</p>
                    {piste(`correction/${q.id}`) && <button onClick={() => jouer(piste(`correction/${q.id}`))} className={BTN}>🔊 Écouter</button>}</div>
                  {q.correction.map((l, k) => <p key={k} className="text-[18px] text-rose-900" style={{ fontFamily: CRAIE }}><Formule t={l} /></p>)}
                  {etat.autoEval && !etat.fait && (
                    <div className="mt-2 flex flex-wrap items-center gap-2 text-[15px]">
                      <span className="text-slate-700">Le tuteur n’est pas joignable pour l’instant : compare toi-même avec la correction.</span>
                      <button onClick={() => poser(q.id, { fait: true, note: q.points, verdict: 'juste' })} className="rounded-md border border-emerald-700 px-3 py-1 text-emerald-800">J’avais juste</button>
                      <button onClick={() => poser(q.id, { fait: true, note: q.points / 2, verdict: 'partiel' })} className="rounded-md border border-amber-600 px-3 py-1 text-amber-800">À moitié</button>
                      <button onClick={() => poser(q.id, { fait: true, note: 0, verdict: 'faux' })} className="rounded-md border border-rose-700 px-3 py-1 text-rose-800">Je m’étais trompé</button>
                    </div>)}
                </div>)}

              <div className="mt-3 flex flex-wrap gap-2">
                {i > 0 && <button onClick={() => setI(i - 1)} className={BTN}>← Précédente</button>}
                {i < CFG.questions.length - 1 && <button onClick={() => setI(i + 1)} className={etat.fait ? 'ml-auto rounded-md bg-black px-4 py-1.5 text-sm font-semibold text-white' : `ml-auto ${BTN}`}>{etat.fait ? 'Question suivante →' : 'Passer →'}</button>}
              </div>

              {fini && <Bilan note={note} parPartie={parPartie} etats={etats} onRefaire={refaire} />}
            </div>
          </div>
        </section>
      </div>
      <ClavierFlottant droite={0} bas={16} />
    </div>
  );
}

/** l'introduction, les figures, le tableau et les données d'une partie (feuille du sujet) ; `grand` : projeté en classe */
export function DonneesPartie({ p, grand = false }: { p: PartieExamen; grand?: boolean }) {
  const t = grand ? 'text-[clamp(16px,1.5vw,24px)]' : 'text-[15px]';
  return (<>
    {p.intro && <p className={`mt-2 leading-snug ${grand ? t : 'text-[16px]'}`}><Formule t={p.intro} /></p>}
    {!!p.figures?.length && <div className="my-2" style={{ filter: 'invert(1) hue-rotate(180deg)' }}><FiguresCahier figures={p.figures as never} /></div>}
    {p.tableau && (
      <div className="mt-2 overflow-x-auto">
        <table className={`w-full border-collapse ${t}`}>
          <thead><tr>{p.tableau.entetes.map((h, k) => <th key={k} className="border border-black bg-slate-100 px-1.5 py-0.5 text-center">{h}</th>)}</tr></thead>
          <tbody>{p.tableau.lignes.map((l, k) => <tr key={k}>{l.map((c, m) => <td key={m} className={`border border-black px-1.5 py-0.5 ${m === 0 ? 'font-semibold' : 'text-center'}`}>{c}</td>)}</tr>)}</tbody>
        </table>
      </div>)}
    {!!p.donnees?.length && (
      <div className={`mt-2 border border-black p-2 ${t}`}>
        <p className="font-bold">Données :</p>
        <ul className="list-disc pl-5">{p.donnees.map((d, k) => <li key={k}><Formule t={d} /></li>)}</ul>
      </div>)}
  </>);
}

export function Choix({ q, etat, onChoisir }: { q: Extract<QuestionExamen, { genre: 'qcm' | 'vf' }>; etat: Etat; onChoisir: (k: number, v: number | boolean) => void }) {
  return (
    <ol className="mt-2 space-y-3">
      {q.items.map((it, k) => {
        const choisi = etat.choix?.[k];
        const options: { v: number | boolean; texte: string }[] = q.genre === 'qcm'
          ? (it as { choix: string[] }).choix.map((c, m) => ({ v: m, texte: c })) : [{ v: true, texte: 'Vrai' }, { v: false, texte: 'Faux' }];
        const bonne = q.genre === 'qcm' ? (it as { bonne: number }).bonne : (it as { vrai: boolean }).vrai;
        return (
          <li key={k} className="text-[16px]" style={{ fontFamily: SUJET }}>
            {q.items.length > 1 && <b>{String.fromCharCode(97 + k)}) </b>}<Formule t={it.texte} />
            <div className={`mt-1 flex flex-wrap gap-1.5 ${q.genre === 'vf' ? '' : 'flex-col sm:flex-row'}`} style={{ fontFamily: 'system-ui, sans-serif' }}>
              {options.map((o, m) => {
                const actif = choisi === o.v;
                const couleur = etat.fait ? (o.v === bonne ? 'border-emerald-700 bg-emerald-50 text-emerald-900' : actif ? 'border-rose-700 bg-rose-50 text-rose-900 line-through' : 'border-slate-300 text-slate-500')
                  : actif ? 'border-black bg-black text-white' : 'border-slate-400 hover:bg-slate-100';
                return <button key={m} disabled={etat.fait} onClick={() => onChoisir(k, o.v)} className={`rounded-md border px-2.5 py-1 text-left text-[15px] ${couleur}`}>
                  {q.genre === 'qcm' ? `${String.fromCharCode(65 + m)}. ` : ''}{o.texte}</button>;
              })}
            </div>
            {etat.fait && (
              <p className={`mt-1 text-[16px] ${choisi === bonne ? 'text-emerald-800' : 'text-rose-800'}`} style={{ fontFamily: CRAIE }}>
                {choisi === bonne ? '✔ ' : '✘ '}<Formule t={it.explication} /></p>)}
          </li>);
      })}
    </ol>
  );
}

export function Verdict({ etat }: { etat: Etat }) {
  const V = { juste: ['✔ Juste', 'border-emerald-700 text-emerald-800'], partiel: ['◐ Juste en partie', 'border-amber-600 text-amber-800'],
    faux: ['✘ Faux', 'border-rose-700 text-rose-800'], nonjuge: ['? Le tuteur n’a pas pu juger ta réponse', 'border-slate-500 text-slate-800'],
    lecture: ['…', 'border-slate-400 text-slate-600'] } as const;
  const [titre, couleur] = V[etat.verdict || 'lecture'];
  return (
    <div className={`mt-3 border-2 p-2 ${couleur}`}>
      {etat.verdict !== 'lecture' && <p className="text-[15px] font-bold">{titre}</p>}
      <p className="text-[18px]" style={{ fontFamily: CRAIE }}><Formule t={etat.retour || ''} /></p>
      {!!etat.details?.length && (
        <table className="mt-2 w-full border-collapse text-[14px] text-slate-900">
          <thead><tr className="bg-slate-100"><th className="border border-slate-400 px-2 py-1 text-left">Élément du barème</th>
            <th className="w-20 border border-slate-400 px-1 py-1">Points</th><th className="border border-slate-400 px-2 py-1 text-left">Points perdus</th></tr></thead>
          <tbody>{etat.details.map((d, k) => (
            <tr key={k} className="align-top">
              <td className="border border-slate-400 px-2 py-1"><Formule t={d.element} /></td>
              <td className={`border border-slate-400 px-1 py-1 text-center font-semibold ${d.obtenu >= d.sur ? 'text-emerald-700' : 'text-rose-700'}`}>{pts(d.obtenu)} / {pts(d.sur)}</td>
              <td className="border border-slate-400 px-2 py-1 text-rose-800">{d.obtenu >= d.sur ? '—' : `−${pts(d.sur - d.obtenu)} : ${d.perte || 'manque'}`}</td>
            </tr>))}
            <tr className="bg-slate-100 font-bold"><td className="border border-slate-400 px-2 py-1 text-right">Note</td>
              <td className="border border-slate-400 px-1 py-1 text-center">{pts(etat.details.reduce((n, d) => n + d.obtenu, 0))} / {pts(etat.details.reduce((n, d) => n + d.sur, 0))}</td><td className="border border-slate-400" /></tr>
          </tbody>
        </table>)}
    </div>
  );
}

function Bilan({ note, parPartie, etats, onRefaire }: { note: number; parPartie: { pa: PartieExamen; sur: number; note: number }[]; etats: Record<string, Etat>; onRefaire: () => void }) {
  const aRevoir = CFG.questions.filter(x => (etats[x.q.id]?.note || 0) < x.q.points);
  return (
    <div className="mt-5 border-2 border-black p-3 sm:p-4">
      <p className="text-xl font-bold">Note finale : {pts(note)} / {pts(CFG.total)}</p>
      <table className="mt-2 w-full border-collapse text-[15px]">
        <tbody>{parPartie.map(({ pa, sur, note: n }) => (
          <tr key={pa.id}><td className="border border-slate-400 px-2 py-1">{pa.titre}</td>
            <td className="w-24 border border-slate-400 px-2 py-1 text-center font-semibold">{pts(n)} / {pts(sur)}</td></tr>))}</tbody>
      </table>
      {aRevoir.length ? (
        <div className="mt-2 text-[15px] text-slate-800">
          <p>À revoir avant la vraie évaluation : relis la correction de chaque question, puis reprends la diapositive du cours qui l’explique.</p>
          <ul className="mt-1 space-y-1">{aRevoir.map(x => (
            <li key={x.q.id}><b>Question {x.q.id}</b> ({pts(etats[x.q.id]?.note || 0)} / {pts(x.q.points)}){' '}
              {(CFG.revoir?.(x.q.id) || []).map(l => <a key={l.diapo} href={lienDiapo(l)} className="ml-1 inline-block rounded border border-slate-500 px-1.5 text-[14px] text-blue-800 underline">↻ {l.titre}</a>)}</li>))}</ul>
        </div>
      ) : <p className="mt-2 text-[15px] text-emerald-800">Tout est juste : tu es prêt pour l’évaluation.</p>}
      <div className="mt-3 flex flex-wrap gap-2">
        <a href="./" className={BTN}>Revoir les cours</a>
        <button onClick={onRefaire} className="rounded-md bg-black px-3 py-1.5 font-semibold text-white">↻ Refaire l’évaluation</button>
      </div>
    </div>
  );
}

const NOMS_COURS: Record<string, string> = { tc_svt_revision: 'Révision avec le tuteur', tc_svt_sortie_ecologique: 'La sortie écologique', tc_svt_facteurs_edaphiques: 'Les facteurs édaphiques' };
function Accueil({ onCommencer, onRefaire, etat, acces }: { onCommencer: () => void; onRefaire: () => void; etat: 'attente' | 'neuf' | 'suite' | 'fini'; acces: { ouvert: boolean; progression?: Progression; seuil?: number } }) {
  return (
    <div className="min-h-[100dvh] bg-[#d6d6d0] p-3 text-black sm:p-6" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <div className="mx-auto max-w-3xl bg-white p-4 shadow-md ring-1 ring-black/10 sm:p-6">
        <a href="./" className="text-sm text-slate-600 underline">← {CFG.retour}</a>
        <table className="my-3 w-full border-collapse text-[15px]">
          <tbody><tr>
            <td className="border border-black px-2 py-1 font-semibold">{CFG.sujet.matiere}</td>
            <td className="border border-black px-2 py-1 text-center">{CFG.sujet.niveau} · {CFG.sujet.minutes} min au plus</td>
            <td className="border border-black px-2 py-1 text-center font-semibold">{pts(CFG.total)} points</td>
          </tr></tbody>
        </table>
        <h1 className="text-xl font-bold" style={{ fontFamily: SUJET }}>{CFG.sujet.titre}</h1>
        <p className="mt-2 text-[16px] leading-relaxed text-slate-800">{CFG.sujet.consigne}</p>
        <table className="mt-3 w-full border-collapse text-[15px]">
          <tbody>{CFG.sujet.parties.map(pa => (
            <tr key={pa.id}><td className="border border-slate-400 px-2 py-1">{pa.titre}</td>
              <td className="w-24 border border-slate-400 px-2 py-1 text-center">{pts(pa.questions.reduce((n, x) => n + x.points, 0))} pts</td>
              <td className="w-24 border border-slate-400 px-2 py-1 text-center text-slate-600">≈ {pa.minutes} min</td></tr>))}</tbody>
        </table>
        <p className="mt-3 text-[14px] text-slate-600">Programme : {CFG.sujet.programme}. Pas de chronomètre : la durée est un repère.</p>
        {CFG.suivi && <p className="mt-3 rounded-md border border-amber-500 bg-amber-50 p-2 text-[14px] text-amber-900">Attention : chaque réponse est enregistrée une seule fois. Une question rendue ne peut plus être changée. Une fois l’évaluation terminée, tu peux la refaire : seule ta dernière copie compte.</p>}
        {!acces.ouvert && etat !== 'attente' && (
          <div className="mt-3 rounded-md border border-sky-700 bg-sky-50 p-3 text-[15px] text-sky-950">
            <p className="font-semibold">L’évaluation s’ouvre quand tu as suivi la révision, ou un des deux cours (au moins {Math.round((acces.seuil || 0.8) * 100)} % des diapositives).</p>
            <ul className="mt-2 space-y-1.5">{Object.entries(acces.progression || {}).map(([id, p]) => {
              const pc = p.total ? Math.min(100, Math.round((100 * p.vues) / p.total)) : 0;
              return (<li key={id} className="flex items-center gap-2">
                <a href={`?cours=${id}`} className="w-48 shrink-0 text-sky-800 underline">{NOMS_COURS[id] || id}</a>
                <span className="h-2.5 flex-1 overflow-hidden rounded-full bg-sky-100"><span className="block h-full rounded-full bg-sky-600" style={{ width: `${pc}%` }} /></span>
                <span className="w-24 shrink-0 text-right text-sm">{p.vues} / {p.total} diapos</span></li>);
            })}</ul>
          </div>)}
        <button disabled={etat === 'attente' || !acces.ouvert} onClick={onCommencer} className="mt-4 rounded-md bg-black px-5 py-2 font-semibold text-white disabled:opacity-40">
          {etat === 'attente' ? 'Chargement…' : etat === 'fini' ? 'Voir mes résultats' : etat === 'suite' ? 'Continuer l’évaluation' : 'Commencer l’évaluation'}</button>
        {etat === 'fini' && (
          <button onClick={onRefaire} className="ml-2 mt-4 rounded-md border border-black bg-white px-5 py-2 font-semibold text-black hover:bg-slate-100">↻ Refaire l’évaluation</button>)}
      </div>
    </div>
  );
}
