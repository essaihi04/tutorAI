import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import AIAvatar, { COLONNE_TUTEUR, type LabControlCommand } from '../session/AIAvatar';
import { observeAvatarMedia } from '../../services/avatarAudio';
import { audioUnlock } from '../../services/audioUnlock';
import type { ProfessorEmotionKind } from '../../services/professorEmotion';
import { focusProfessor } from '../../services/professorFocus';
import type { CourseSlide, ReactionPreparee, SlideConcentration } from './types';

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
 * nouveau résultat, le tuteur l'interprète (DeepSeek, `/course-player/sim-reaction`), le dit tout de suite
 * (`/tts/speak`) et pose une question (QCM, vrai/faux ou directe selon ce que l'élève a montré), sans quitter
 * la diapositive.
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
  /** Passer à la diapositive suivante (quand toutes les questions sont justes, ou à la fin du cycle de reprise). */
  onSuivant?: () => void;
}

const premier = <T,>(champ: Record<string, T> | undefined, langue: Langue): T | undefined =>
  champ ? champ[langue] ?? champ.mixed ?? champ.fr ?? Object.values(champ)[0] : undefined;

const CRAIE = "'Patrick Hand', 'Caveat', cursive";

/** « y_M(t) = y_S(t − τ) » s'affiche avec M et S en indice : jamais de « _ » devant l'élève. */
function Formule({ t }: { t: string }) {
  const parts: ReactNode[] = [];
  const re = /([A-Za-zτθΔλωφ])_(\{[^}]+\}|[A-Za-z0-9]+)/g;
  let i = 0, m: RegExpExecArray | null, k = 0;
  while ((m = re.exec(t))) {
    if (m.index > i) parts.push(t.slice(i, m.index));
    parts.push(m[1], <sub key={k++} className="text-[0.7em]">{m[2].replace(/[{}]/g, '')}</sub>);
    i = re.lastIndex;
  }
  if (i < t.length) parts.push(t.slice(i));
  return <>{parts}</>;
}

/** Le deuxième tableau descend du haut ; chaque question s'y écrit l'une après l'autre. */
const ANIMATIONS = `
@keyframes tableau-descend { from { transform: translateY(-108%); opacity: .5 } 60% { transform: translateY(1.5%) } to { transform: none; opacity: 1 } }
@keyframes question-apparait { from { opacity: 0; transform: translateY(-10px) } to { opacity: 1; transform: none } }
.tableau-questions { animation: tableau-descend .7s cubic-bezier(.2,.8,.2,1) both }
.question-apparait { opacity: 0; animation: question-apparait .45s ease-out both }
`;

/** Durée du vol du tuteur jusqu'au bouton (s), mesurée : la commande arrive ~0,9 s après le geste. */
const AVANCE_COMMANDE = 0.9;

type QuestionSim = {
  type: 'qcm' | 'vrai_faux' | 'directe'; enonce: string; explication?: string;
  choix?: string[]; bonne?: number; affirmations?: { texte: string; vrai: boolean }[]; attendu?: string;
  parole_juste?: string; parole_faux?: string;
};
type Reaction =
  | { phase: 'reflechit' }
  | { phase: 'question'; ecrit: string; question: QuestionSim; verdict?: { correct: boolean; ecrit: string } }
  | { phase: 'erreur'; message: string };
type EtatSim = Record<string, unknown> & { simulation_status?: string; derniere_main?: string; parameters?: unknown; moments?: Record<string, number> };
/** Une reprise (cycle 1 à 3) : ce que le tuteur dit et fait, puis la question jumelle. */
type Reprise = {
  cycle: number; parole: string; ecrit: string; dernier: boolean; reponse_finale?: string; cahier?: string;
  gestes: { commande?: string; parametres?: Record<string, unknown>; repere?: string }[];
  question: QuestionSim;
};
type Cycle = { n: number; phase: 'attente' | 'explique' | 'question' | 'final'; data?: Reprise; depuis: QuestionDiapo };
const MAX_CYCLES = 3;

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

export default function CourseFocusStage({ slide, language, deckControls, tuteur3D = false, deckId, onSuivant }: Props) {
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
  const coursEnPause = useRef(false);
  const eleveATouche = useRef(false);
  const varianteFaite = useRef(false);
  // ── La question libre de l'élève : écrite, au micro ou en image ; le tuteur répond sans quitter la diapositive ──
  type QuestionLibre = { phase: 'saisie' | 'envoi' | 'reponse'; texte: string; image?: { b64: string; mime: string; nom: string }; audio?: string; enregistre: boolean;
    /** La transcription du micro est en cours : elle va s'écrire dans le champ, pour que l'élève la vérifie. */
    transcrit?: boolean; aVerifier?: boolean;
    reponse?: { parole: string; ecrit: string; question_comprise: string }; erreur?: string };
  const [libre, setLibre] = useState<QuestionLibre>({ phase: 'saisie', texte: '', enregistre: false });
  const enregistreur = useRef<MediaRecorder | null>(null);
  const morceauxAudio = useRef<Blob[]>([]);
  // ── Le cycle de reprise : faux → le tuteur réexplique autrement, puis question jumelle ; 3 cycles au plus ──
  const [cycle, setCycle] = useState<Cycle | null>(null);
  const cycleRef = useRef<Cycle | null>(null);
  cycleRef.current = cycle;
  const finies = useRef<Record<string, boolean>>({});
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

  const questions = useMemo(() => questionsDeLaDiapo(slide), [slide]);
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

  // Nouvelle diapositive : tout repart de zéro.
  useEffect(() => {
    setTemps(0); setEnLecture(false); setFinie(!piste?.url); setPanneau(null); setSimPrete(false);
    setDuree((piste?.duration_ms || 0) / 1000);
    dejaFaits.current = new Set(); demarree.current = false;
    setReaction(null); dernierEtat.current = null; dernierResultat.current = null; historique.current = [];
    coursEnPause.current = false; eleveATouche.current = false; varianteFaite.current = false;
    setCycle(null); finies.current = {}; fausses.current = {}; voixLancee.current = false;
    setLibre({ phase: 'saisie', texte: '', enregistre: false });
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
  const dire = useCallback(async (texte: string): Promise<boolean> => {
    if (!texte.trim()) return false;
    try {
      const r = await fetch('/api/v1/tts/speak', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton()}` },
        body: JSON.stringify({ text: texte, language: 'mixed' }) });
      if (!r.ok) return false;
      const url = URL.createObjectURL(await r.blob());
      const voix = voixRef.current;
      if (!voix) return false;
      voix.src = url; await voix.play();
      return true;
    } catch { return false; /* la voix manque : l'écrit suffit */ }
  }, []);

  /** L'élève lève la main : le cours se met en pause et le panneau de la question s'ouvre. */
  const leverLaMain = useCallback(() => {
    const audio = audioRef.current;
    if (audio && !audio.paused) { audio.pause(); coursEnPause.current = true; if (demarree.current) envoyerASim('pause'); }
    setPanneau(p => p === 'question_eleve' ? null : 'question_eleve');
  }, [envoyerASim]);

  const lireFichier = (f: File) => new Promise<string>((ok, ko) => { const fr = new FileReader(); fr.onload = () => ok(String(fr.result)); fr.onerror = ko; fr.readAsDataURL(f); });

  const basculerMicro = useCallback(async () => {
    if (libre.enregistre) { enregistreur.current?.stop(); return; }
    try {
      const flux = await navigator.mediaDevices.getUserMedia({ audio: true });
      const rec = new MediaRecorder(flux);
      morceauxAudio.current = [];
      rec.ondataavailable = e => { if (e.data.size) morceauxAudio.current.push(e.data); };
      rec.onstop = async () => {
        flux.getTracks().forEach(t => t.stop());
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
      rec.start(); enregistreur.current = rec;
      setLibre(l => ({ ...l, enregistre: true, audio: undefined }));
    } catch { setLibre(l => ({ ...l, erreur: 'Le micro n’est pas disponible : écris ta question, ou envoie une image.' })); }
  }, [libre.enregistre]);

  const envoyerQuestion = useCallback(async () => {
    if (libre.phase !== 'saisie' || (!libre.texte.trim() && !libre.audio && !libre.image)) return;
    setLibre(l => ({ ...l, phase: 'envoi', erreur: undefined }));
    ressentir('think');
    iframeRef.current?.contentWindow?.postMessage({ type: 'simulation_manifest_request' }, '*');
    await new Promise(r => window.setTimeout(r, 500));
    try {
      const r = await appelerApi<{ parole: string; ecrit: string; question_comprise: string; gestes: { commande?: string; parametres?: Record<string, unknown>; repere?: string }[] }>('/course-player/question-eleve', {
        deck_id: deckId, slide_id: slide.id, title: slide.title, speech: parole, ce_qui_se_voit: String(dernierEtat.current?.ce_qui_se_voit || ''),
        texte: libre.texte.trim(), audio_b64: libre.audio, image_b64: libre.image?.b64, image_mime: libre.image?.mime || 'image/png',
        moments: dernierEtat.current?.moments || {}, reperes: reperesRef.current,
      });
      setLibre(l => ({ ...l, phase: 'reponse', reponse: r }));
      ressentir('encourage');
      void dire(r.parole);
      r.gestes.forEach((g, i) => window.setTimeout(() => {
        if (g.commande) parTuteur(g.commande, g.parametres || {});
        else if (g.repere) parTuteur('highlight', { target: g.repere });
      }, 1200 + i * 3500));
      void appelerApi('/course-player/acquis', {
        slide_id: slide.id, slide_title: slide.title, deck_id: deckId, cle: 'question_libre', type: 'directe', enonce: r.question_comprise.slice(0, 300),
        reponse: '', tentative: 1, correct: null, reaction_preparee: false, methodes: { visuel: visuel?.kind || 'aucun', question_libre: true },
      }).catch(() => { /* jamais bloquant */ });
    } catch (e) {
      const m = (e as Error).message;
      setLibre(l => ({ ...l, phase: 'saisie', erreur: /^\d+$/.test(m) ? `Le professeur n'a pas pu répondre (${m}).` : m }));
    }
  }, [libre, deckId, slide.id, slide.title, parole, visuel?.kind, dire, parTuteur, ressentir]);

  const reprendreApresQuestion = useCallback(() => {
    voixRef.current?.pause();
    setLibre({ phase: 'saisie', texte: '', enregistre: false });
    setPanneau(null);
    if (coursEnPause.current) { coursEnPause.current = false; void audioRef.current?.play(); if (demarree.current) envoyerASim('resume'); }
  }, [envoyerASim]);

  /** Toutes les questions justes : le tableau se ferme après la voix du bravo et le cours passe à la diapositive suivante. */
  const terminerEtPasser = useCallback(() => {
    const attendreVoix = () => {
      const v = voixRef.current;
      if (v && !v.paused && !v.ended) { window.setTimeout(attendreVoix, 400); return; }
      setPanneau(null); setCycle(null);
      window.setTimeout(() => onSuivant?.(), 700);
    };
    window.setTimeout(attendreVoix, 1200);
  }, [onSuivant]);

  /** Faux : le tuteur réexplique AUTREMENT (DeepSeek, avec tout le contexte), montre dans la simulation, puis question jumelle. */
  const lancerCycle = useCallback(async (n: number, depuis: QuestionDiapo) => {
    setCycle({ n, phase: 'attente', depuis });
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

  const surFinie = useCallback((cle: string, correct: boolean, fraiche: boolean) => {
    finies.current[cle] = correct;
    const c = cycleRef.current;
    if (c && cle.startsWith('cycle')) {
      // Question jumelle : juste → on passe ; faux → cycle suivant, ou la réponse au 3e.
      if (correct) { ressentir('celebrate'); terminerEtPasser(); return; }
      if (c.n < MAX_CYCLES) { void lancerCycle(c.n + 1, c.depuis); return; }
      const d = c.data;
      setCycle({ ...c, phase: 'final' });
      if (d?.reponse_finale) void dire(d.reponse_finale);
      return;
    }
    if (!fraiche) return;
    const toutes = questions.every(q => q.cle in finies.current);
    if (!toutes) return;
    const ratee = questions.find(q => finies.current[q.cle] === false);
    if (!ratee) { terminerEtPasser(); return; }
    void lancerCycle(1, ratee);
  }, [questions, terminerEtPasser, lancerCycle, dire, ressentir]);

  /** Chaque réponse part au suivi des acquis, avec la manière dont la notion a été expliquée sur cette diapositive. */
  const enregistrerReponse = useCallback((r: ReponseNotee) => {
    if (r.correct === false) (fausses.current[r.cle] ||= []).push(r.reponse);
    // juste du premier coup : il exulte ; juste après l'indice : il encourage ; faux : il secoue la tête et tend
    // une idée ; faux une deuxième fois : il encourage quand même ; réponse qu'il ne peut pas juger : il réfléchit.
    ressentir(r.correct === true ? (r.tentative <= 1 ? 'celebrate' : 'encourage') : r.correct === false ? (r.tentative <= 1 ? 'wrong' : 'encourage') : 'think');
    void appelerApi('/course-player/acquis', {
      slide_id: slide.id, slide_title: slide.title, deck_id: deckId, cle: r.cle, type: r.type, enonce: r.enonce, reponse: r.reponse,
      tentative: r.tentative, correct: r.correct, reaction_preparee: r.preparee,
      methodes: {
        visuel: visuel?.kind || (table ? 'table' : 'aucun'), formules_au_centre: centre.length,
        tuteur_a_montre: pointage.length, eleve_a_manipule: eleveATouche.current, variante_du_tuteur: varianteFaite.current,
        exercice: r.cle.startsWith('e'), reexplication: cycleRef.current?.n || 0,
      },
    }).catch(() => { /* le suivi ne doit jamais gêner l'élève */ });
  }, [slide.id, slide.title, deckId, visuel?.kind, table, centre.length, pointage.length, ressentir]);

  /** Une piste déjà prête (réaction préparée) : elle part tout de suite. */
  const jouer = useCallback((url: string) => {
    const voix = voixRef.current;
    if (!voix) return;
    voix.src = url; void voix.play().catch(() => {});
  }, []);

  const declencherReaction = useCallback(async (avant: EtatSim | null, apres: EtatSim) => {
    const audio = audioRef.current;
    if (audio && !audio.paused) { audio.pause(); coursEnPause.current = true; }
    setPanneau(null);
    setReaction({ phase: 'reflechit' });
    try {
      const r = await appelerApi<{ parole: string; ecrit: string; question: QuestionSim }>('/course-player/sim-reaction', {
        mode: 'interpreter', diapo: { title: slide.title, speech: parole }, avant: avant || {}, apres, historique: historique.current,
      });
      setReaction({ phase: 'question', ecrit: r.ecrit || '', question: r.question });
      ressentir('surprise');
      void dire(r.parole);
    } catch (e) {
      setReaction({ phase: 'erreur', message: `Le professeur n'a pas pu répondre (${(e as Error).message}).` });
    }
  }, [slide.title, parole, dire, ressentir]);

  const repondre = useCallback(async (correct: boolean | null, reponseDirecte?: string) => {
    const r = reactionRef.current;
    if (!r || r.phase !== 'question' || r.verdict) return;
    const q = r.question;
    if (q.type === 'directe') {
      setReaction({ ...r, verdict: { correct: false, ecrit: '…' } });
      try {
        const c = await appelerApi<{ correct: boolean; parole: string; ecrit: string }>('/course-player/sim-reaction', {
          mode: 'corriger', diapo: { title: slide.title }, question: q, reponse: reponseDirecte || '',
        });
        historique.current.push({ type: q.type, correct: c.correct });
        ressentir(c.correct ? 'celebrate' : 'wrong');
        setReaction({ ...r, verdict: { correct: c.correct, ecrit: c.ecrit } });
        void dire(c.parole);
      } catch {
        setReaction({ ...r, verdict: { correct: false, ecrit: q.attendu ? `Réponse attendue : ${q.attendu}` : '' } });
      }
      return;
    }
    const juste = !!correct;
    historique.current.push({ type: q.type, correct: juste });
    ressentir(juste ? 'celebrate' : 'wrong');
    setReaction({ ...r, verdict: { correct: juste, ecrit: q.explication || '' } });
    void dire((juste ? q.parole_juste : q.parole_faux) || '');
  }, [slide.title, dire, ressentir]);

  const continuerCours = useCallback(() => {
    voixRef.current?.pause();
    setReaction(null);
    if (coursEnPause.current) { coursEnPause.current = false; void audioRef.current?.play(); }
  }, []);

  // Ce que la simulation renvoie : un nouveau résultat obtenu par l'élève lui-même déclenche la réaction.
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
      if (etat.simulation_status !== 'finished' || avant?.simulation_status === 'finished') return;
      const precedent = dernierResultat.current;
      dernierResultat.current = etat;
      if (etat.derniere_main !== 'eleve' || reactionRef.current) return;
      // Même réglage que le résultat précédent : rien de nouveau à interpréter.
      if (precedent && JSON.stringify(precedent.parameters) === JSON.stringify(etat.parameters)) return;
      eleveATouche.current = true;
      void declencherReaction(precedent, etat);
    };
    window.addEventListener('message', ecouter);
    return () => window.removeEventListener('message', ecouter);
  }, [declencherReaction]);

  // Après la voix, si l'élève n'a rien touché : le tuteur fait la variante lui-même, pour comparer.
  useEffect(() => {
    const v = conc.variante;
    if (!finie || !v?.etapes?.length || varianteFaite.current || !simPrete) return;
    const id = window.setTimeout(() => {
      if (eleveATouche.current || reactionRef.current || varianteFaite.current) return;
      varianteFaite.current = true;
      v.etapes.forEach(e => {
        if (e.commande) parTuteur(e.commande, e.parametres || {});
        else if (e.repere) parTuteur('highlight', { target: e.repere });
      });
    }, (v.apres_s ?? 5) * 1000);
    return () => window.clearTimeout(id);
  }, [finie, conc.variante, simPrete, parTuteur]);

  // Pause de la voix = pause de la simulation : l'élève ne rate rien.
  const basculer = useCallback(() => {
    const audio = audioRef.current;
    if (!audio) return;
    if (audio.paused) { void audio.play(); if (demarree.current) envoyerASim('resume'); }
    else { audio.pause(); if (demarree.current) envoyerASim('pause'); }
  }, [envoyerASim]);

  const reecouter = useCallback(() => {
    const audio = audioRef.current;
    if (!audio) return;
    dejaFaits.current = new Set(); demarree.current = false; setFinie(false);
    if (conc.demarrer) envoyerASim('reset');
    audio.currentTime = 0; void audio.play();
  }, [conc.demarrer, envoyerASim]);

  const toutVisible = finie || !piste?.url;
  const cahier = (conc.cahier || contenu.student_trace || contenu.essential_text || '').trim();
  const exercices = slide.exercises || [];
  const surSim = visuel?.kind === 'simulation';

  return (
    <div className="relative h-full w-full flex flex-col text-white" style={{ background: '#12241c' }}>
      <style>{ANIMATIONS}</style>
      {piste?.url && (
        <audio
          key={piste.url}
          ref={audioRef}
          src={piste.url}
          autoPlay
          preload="auto"
          // La bouche du tuteur suit le SON de la piste (analyseur partagé), pas seulement l'état « il parle ».
          onPlay={event => { setEnLecture(true); void audioUnlock.ensureRunning(); observeAvatarMedia(event.currentTarget); }}
          onPause={() => setEnLecture(false)}
          onLoadedMetadata={event => { const d = event.currentTarget.duration; if (Number.isFinite(d) && d > 0) setDuree(d); }}
          // la bulle du cahier s'ouvre à la demande ; les questions, elles, s'affichent tout de suite
          onEnded={() => { setEnLecture(false); setFinie(true); iframeRef.current?.contentWindow?.postMessage({ type: 'simulation_manifest_request' }, '*'); if (conc.acquis) direLesLacunes(); if (questions.length && !reactionRef.current) setPanneau('questions'); }}
        />
      )}
      <audio ref={voixRef} onPlay={event => { setVoixParle(true); void audioUnlock.ensureRunning(); observeAvatarMedia(event.currentTarget); }} onPause={() => setVoixParle(false)} onEnded={() => setVoixParle(false)} />

      {/* ── Le titre et le sous-titre, seulement ── */}
      <header className="shrink-0 px-6 pt-4 pb-2 text-center">
        <h1 className="text-2xl md:text-3xl" style={{ fontFamily: CRAIE, color: '#fef3c7' }}>{slide.title}</h1>
        {contenu.lead && (
          <p className="mt-1 text-base md:text-lg text-white/70" style={{ fontFamily: CRAIE }}>{contenu.lead}</p>
        )}
      </header>

      {/* ── Au centre : ce qu'on regarde ── */}
      <main className="relative flex-1 min-h-0 flex flex-col items-center justify-center gap-3 px-4 pb-2"
        style={tuteur3D ? { paddingRight: COLONNE_TUTEUR } : undefined}>   {/* la colonne de droite est au tuteur 3D */}
        {/* ── Le deuxième tableau : les questions descendent du haut et couvrent la scène, tout tient sans défiler ── */}
        {panneau === 'questions' && (
          <section className="tableau-questions absolute inset-y-0 left-3 z-30 flex flex-col overflow-hidden rounded-2xl border-2 border-amber-200/40 bg-[#0f2219] shadow-2xl"
            style={{ right: tuteur3D ? COLONNE_TUTEUR + 4 : 12 }}>
            <div className="flex shrink-0 items-center justify-between border-b border-amber-200/20 px-4 py-2">
              <div className="text-base font-semibold text-emerald-200" style={{ fontFamily: CRAIE }}>
                {cycle?.phase === 'final' ? `📓 La réponse · reprise ${cycle.n}/${MAX_CYCLES}` : enReprise ? `↻ Reprise ${cycle!.n}/${MAX_CYCLES} · ${jumelles.questions.length > 1 ? 'vrai ou faux' : 'nouvelle question'}` : `✏️ À toi · ${questions.length} question${questions.length > 1 ? 's' : ''}`}
              </div>
              <button onClick={() => setPanneau(null)} className="text-white/50 hover:text-white text-xl" aria-label="Revenir à la scène">×</button>
            </div>
            {cycle?.phase === 'final' ? (
              <div className="flex min-h-0 flex-1 flex-col justify-center gap-4 p-5" style={{ fontFamily: CRAIE }}>
                <p className="text-lg text-white/85"><Formule t={cycle.data?.ecrit || ''} /></p>
                {cycle.data?.cahier && <p className="rounded-xl border border-amber-200/40 px-4 py-3 text-xl text-amber-100">📓 À écrire dans le cahier : <Formule t={cycle.data.cahier} /></p>}
                <p className="text-sm text-white/55">Cette notion est notée « à reprendre » : le professeur y reviendra autrement, en mode libre et au prochain cours.</p>
                <button onClick={() => { voixRef.current?.pause(); setCycle(null); setPanneau(null); onSuivant?.(); }} className="self-start rounded-full bg-emerald-500/30 px-5 py-2 text-base hover:bg-emerald-500/40">Suivant →</button>
              </div>
            ) : enReprise ? (
              <QuestionsDeLaDiapo key={`cycle${cycle!.n}`} questions={jumelles.questions} diapo={{ title: slide.title, speech: parole, memoire: `${deckId || ''}:${slide.id}` }} dire={dire} jouer={jouer} reponses={jumelles.preparees} onReponse={enregistrerReponse} onFinie={surFinie} essaisMax={1} />
            ) : (
              <QuestionsDeLaDiapo key={slide.id} questions={questions} diapo={{ title: slide.title, speech: parole, memoire: `${deckId || ''}:${slide.id}` }} dire={dire} jouer={jouer} reponses={conc.reponses} onReponse={enregistrerReponse} onFinie={surFinie} />
            )}
          </section>
        )}
        {visuel && (
          <div
            ref={visuelRef}
            className="relative w-full flex-1 min-h-0 flex items-center justify-center"
            style={{ maxWidth: surSim ? 1100 : 900 }}
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
                style={{ aspectRatio: '760 / 470', maxHeight: '100%' }}
                onLoad={() => window.setTimeout(() => setSimPrete(true), 700)}
              />
            )}
            {visuel.kind === 'image' && visuel.url && (
              <img src={visuel.url} alt={visuel.alt || contenu.alt || ''} className="max-h-full max-w-full object-contain" />
            )}
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

        {centre.length > 0 && (
          <div className={`flex ${visuel || table ? 'flex-row flex-wrap justify-center gap-3' : 'flex-col items-center gap-4'}`}>
            {centre.map((c, i) => {
              const vu = toutVisible || temps >= c.t;
              return (
                <div
                  key={i}
                  ref={el => { centreRef.current[i] = el; }}
                  className="rounded-xl px-4 py-2 transition-all duration-700"
                  style={{
                    fontFamily: CRAIE,
                    fontSize: visuel || table ? 22 : 30,
                    color: '#fef9c3',
                    border: '1px dashed rgba(254,249,195,0.35)',
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

        {!visuel && !table && centre.length === 0 && (
          <p className="text-white/40 text-lg" style={{ fontFamily: CRAIE }}>Écoute le professeur…</p>
        )}
      </main>

      {/* ── Les bulles : l'écrit, fermé par défaut ── */}
      {panneau && panneau !== 'questions' && (
        <div style={tuteur3D ? { right: COLONNE_TUTEUR } : undefined} className="absolute left-4 right-4 bottom-[76px] z-30 mx-auto max-w-3xl max-h-[55%] overflow-y-auto rounded-2xl border border-white/15 bg-[#0d1c15]/95 p-5 shadow-2xl backdrop-blur">
          <button onClick={() => setPanneau(null)} className="absolute right-3 top-2 text-white/50 hover:text-white text-xl" aria-label="Fermer">×</button>
          {panneau === 'cahier' && (
            <>
              <div className="text-sm font-semibold text-amber-200">📓 À écrire dans le cahier</div>
              {/* Ce qui s'écrit au cahier commence comme au tableau : le titre, puis le sous-titre s'il y en a un. */}
              <h3 className="mt-2 text-xl underline decoration-amber-200/40 underline-offset-4" style={{ fontFamily: CRAIE, color: '#fef3c7' }}>{slide.title}</h3>
              {contenu.lead && <p className="mt-1 text-base italic" style={{ fontFamily: CRAIE, color: '#e7e5c9' }}>{contenu.lead}</p>}
              {cahier && cahier !== contenu.lead && <p className="mt-2 text-lg leading-relaxed" style={{ fontFamily: CRAIE, color: '#fef3c7' }}><Formule t={cahier} /></p>}
              {centre.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                  {centre.filter(c => /=/.test(c.texte)).map((c, i) => (
                    <span key={i} className="rounded-lg border border-amber-200/30 px-3 py-1" style={{ fontFamily: CRAIE, color: '#fef9c3' }}><Formule t={c.texte} /></span>
                  ))}
                </div>
              )}
              <button onClick={() => { void navigator.clipboard?.writeText([slide.title, contenu.lead, cahier !== contenu.lead ? cahier : ''].filter(Boolean).join('\n')); }} className="mt-3 text-xs text-white/50 hover:text-white">Copier</button>
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
                  <textarea value={libre.texte} onChange={e => setLibre(l => ({ ...l, texte: e.target.value }))} disabled={libre.phase === 'envoi' || libre.transcrit} rows={2}
                    placeholder={libre.transcrit ? 'Transcription de ce que tu as dit…' : 'Écris ta question… (en darija ou en français)'} dir="auto"
                    className="mt-2 w-full resize-none rounded-lg border border-white/20 bg-black/30 px-3 py-2 text-lg outline-none focus:border-sky-300" />
                  <div className="mt-2 flex flex-wrap items-center gap-2">
                    <button onClick={() => void basculerMicro()} disabled={libre.phase === 'envoi'} className={`rounded-full px-4 py-2 text-sm ${libre.enregistre ? 'bg-rose-500/40 animate-pulse' : 'bg-white/10 hover:bg-white/20'}`}>
                      {libre.enregistre ? '■ Arrêter' : libre.audio ? '🎙️ Réenregistrer' : '🎙️ Parler'}
                    </button>
                    {libre.transcrit && <span className="text-sm text-sky-200 animate-pulse">✍️ Transcription…</span>}
                    {libre.audio && !libre.enregistre && !libre.transcrit && <span className="text-sm text-emerald-200">✔ enregistrement prêt</span>}
                    <label className="cursor-pointer rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20">
                      📷 {libre.image ? libre.image.nom.slice(0, 18) : 'Image'}
                      <input type="file" accept="image/*" capture="environment" className="hidden" disabled={libre.phase === 'envoi'}
                        onChange={async e => { const f = e.target.files?.[0]; if (!f) return; const b64 = await lireFichier(f); setLibre(l => ({ ...l, image: { b64, mime: f.type || 'image/png', nom: f.name } })); }} />
                    </label>
                    {libre.image && <img src={libre.image.b64} alt="" className="h-10 rounded border border-white/20" />}
                    <button onClick={() => void envoyerQuestion()} disabled={libre.phase === 'envoi' || libre.enregistre || libre.transcrit || (!libre.texte.trim() && !libre.audio && !libre.image)}
                      className="ml-auto rounded-full bg-sky-500/40 px-5 py-2 text-sm hover:bg-sky-500/50 disabled:opacity-40">
                      {libre.phase === 'envoi' ? 'Le professeur réfléchit…' : 'Envoyer'}
                    </button>
                  </div>
                  {libre.aVerifier && !libre.transcrit && libre.phase === 'saisie' && (
                    <p className="mt-2 text-sm text-sky-200/80">Vérifie ce que le professeur a compris ; corrige si besoin, puis Envoyer.</p>
                  )}
                  {libre.erreur && <p className="mt-2 text-sm text-rose-200">{libre.erreur}</p>}
                </>
              )}
              {libre.phase === 'reponse' && libre.reponse && (
                <>
                  {libre.reponse.question_comprise && <p className="mt-2 text-sm text-white/55">Ta question : « {libre.reponse.question_comprise} »</p>}
                  <p className="mt-2 text-lg leading-relaxed text-white/90"><Formule t={libre.reponse.ecrit || libre.reponse.parole} /></p>
                  <div className="mt-3 flex gap-2">
                    <button onClick={() => setLibre({ phase: 'saisie', texte: '', enregistre: false })} className="rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20">Autre question</button>
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
        <div style={tuteur3D ? { right: COLONNE_TUTEUR } : undefined} className="absolute left-4 right-4 bottom-[76px] z-40 mx-auto max-w-3xl max-h-[45%] overflow-y-auto rounded-2xl border border-cyan-300/30 bg-[#0d1c15]/95 p-5 shadow-2xl backdrop-blur">
          <div className="text-sm font-semibold text-cyan-200">🔬 Ton résultat</div>
          {reaction.phase === 'reflechit' && <p className="mt-2 text-white/70 animate-pulse">Le professeur regarde ton nouveau résultat…</p>}
          {reaction.phase === 'erreur' && (
            <>
              <p className="mt-2 text-rose-200">{reaction.message}</p>
              <button onClick={continuerCours} className="mt-3 rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20">Continuer</button>
            </>
          )}
          {reaction.phase === 'question' && (
            <QuestionSurResultat reaction={reaction} onRepondre={repondre} onContinuer={continuerCours} />
          )}
        </div>
      )}

      {/* ── La barre du bas, hors de la scène ── */}
      <footer className="shrink-0 z-20 flex flex-wrap items-center gap-2 px-3 py-2 border-t border-white/10 bg-black/25">
        {piste?.url && (
          <>
            <button onClick={basculer} className="h-10 w-10 rounded-full bg-white/10 hover:bg-white/20" title={enLecture ? 'Pause' : 'Écouter'}>
              {enLecture ? '❚❚' : '▶'}
            </button>
            <button onClick={reecouter} className="h-10 w-10 rounded-full bg-white/10 hover:bg-white/20" title="Réécouter depuis le début">⟲</button>
            <div className="hidden sm:block w-40 h-1.5 rounded-full bg-white/10 overflow-hidden">
              <div className="h-full bg-emerald-400/80" style={{ width: `${duree ? Math.min(100, (temps / duree) * 100) : 0}%` }} />
            </div>
          </>
        )}
        <Bulle actif={panneau === 'cahier'} pulse={toutVisible && panneau !== 'cahier' && !!cahier} onClick={() => setPanneau(p => p === 'cahier' ? null : 'cahier')} disabled={!cahier}>
          📓 À écrire dans le cahier
        </Bulle>
        <Bulle actif={panneau === 'explication'} onClick={() => setPanneau(p => p === 'explication' ? null : 'explication')}>
          📖 Explication écrite
        </Bulle>
        <Bulle actif={panneau === 'question_eleve'} onClick={leverLaMain}>
          🙋 Question
        </Bulle>
        {questions.length > 0 && (
          <Bulle actif={panneau === 'questions'} pulse={toutVisible && panneau !== 'questions'} onClick={() => setPanneau(p => p === 'questions' ? null : 'questions')}>
            ✏️ À toi ({questions.length})
          </Bulle>
        )}
        <div className="ml-auto flex items-center gap-2">{deckControls}</div>
      </footer>

      {tuteur3D && <AIAvatar isSpeaking={enLecture || voixParle} isProcessing={reaction?.phase === 'reflechit' || cycle?.phase === 'attente'} labControl={labControl} emotion={emotion} discret />}
    </div>
  );
}

/** Une question de la diapositive, telle que l'élève y répond (la clé `bonne` n'existe que pour les exercices). */
type QuestionDiapo = { cle: string; type: 'qcm' | 'vrai_faux' | 'directe'; enonce: string; choix?: string[]; bonne?: number; explication?: string };

function questionsDeLaDiapo(slide: CourseSlide): QuestionDiapo[] {
  const out: QuestionDiapo[] = [];
  const q = slide.question;
  if (q?.prompt) {
    if ((q.options || []).length >= 2) out.push({ cle: 'q', type: 'qcm', enonce: q.prompt, choix: q.options, bonne: q.correct });
    else out.push({ cle: 'q', type: 'directe', enonce: q.prompt });
  }
  (slide.exercises || []).forEach((ex, i) => {
    if (ex.type === 'qcm' && (ex.choices || []).length >= 2) out.push({ cle: `e${i}`, type: 'qcm', enonce: ex.prompt, choix: ex.choices, bonne: ex.correct ?? 0, explication: ex.explanation });
    if (ex.type === 'vrai_faux') (ex.statements || []).forEach((st, j) => {
      out.push({ cle: `e${i}s${j}`, type: 'vrai_faux', enonce: st.text, choix: ['Vrai', 'Faux'], bonne: st.correct ? 0 : 1, explication: st.explanation });
    });
  });
  return out;
}

/**
 * Les questions de la diapositive, affichées dès la fin de la voix. Chaque réponse reçoit la réaction du tuteur,
 * dite à voix haute : juste → ce qui est juste et pourquoi ; fausse au 1er essai → un indice, et il réessaie ;
 * fausse au 2e → la réponse et sa justification. Chaque réponse possible a sa réaction PRÉPARÉE, avec sa voix
 * (`concentration.reponses`) : elle part tout de suite, sans serveur. Seule une réponse écrite librement passe
 * par `/course-player/answer-reaction` (DeepSeek) et la voix en direct.
 */
/** Ce que l'écran note à chaque réponse (suivi des acquis, skill `suivi-des-acquis`). */
export type ReponseNotee = { cle: string; type: QuestionDiapo['type']; enonce: string; reponse: string; tentative: number; correct: boolean | null; preparee: boolean };

function QuestionsDeLaDiapo({ questions, diapo, dire, jouer, reponses, onReponse, onFinie, essaisMax }: {
  questions: QuestionDiapo[]; diapo: { title: string; speech: string; memoire?: string }; dire: (texte: string) => Promise<boolean>;
  jouer: (url: string) => void; reponses?: SlideConcentration['reponses']; onReponse?: (r: ReponseNotee) => void;
  onFinie?: (cle: string, correct: boolean, fraiche: boolean) => void; essaisMax?: number;
}) {
  // Une question à la fois, en carrousel (user rule, 8 novembre 2026) : l'élève répond, lit ou écoute
  // l'explication, puis passe à la suivante avec « Suivant → » (ou la question passe seule après l'explication).
  // Toutes les questions restent montées : leur état ne se perd pas en changeant de page.
  const [index, setIndex] = useState(0);
  const [finiesIci, setFiniesIci] = useState<Record<string, boolean>>({});
  const surFinieLocale = useCallback((cle: string, correct: boolean, fraiche: boolean) => {
    setFiniesIci(f => ({ ...f, [cle]: true }));
    onFinie?.(cle, correct, fraiche);
    // Question finie à l'instant : on laisse le temps d'entendre la réaction, puis on passe à la suivante non répondue.
    if (fraiche) window.setTimeout(() => setIndex(i => {
      const k = questions.findIndex((q, j) => j > i && !finiesIciRef.current[q.cle]);
      return k >= 0 ? k : i;
    }), 4500);
  }, [onFinie, questions]);
  const finiesIciRef = useRef(finiesIci);
  finiesIciRef.current = finiesIci;
  const n = questions.length;
  const courante = Math.min(index, Math.max(0, n - 1));
  return (
    <div className="flex min-h-0 flex-1 flex-col p-3" style={{ fontFamily: CRAIE }}>
      <div className="min-h-0 flex-1">
        {questions.map((q, i) => (
          <div key={q.cle} className={`question-apparait h-full min-h-0 ${i === courante ? '' : 'hidden'}`}>
            <UneQuestion q={q} diapo={diapo} dire={dire} jouer={jouer} preparees={reponses?.[q.cle]} onReponse={onReponse} onFinie={surFinieLocale} essaisMax={essaisMax} />
          </div>
        ))}
      </div>
      {n > 1 && (
        <div className="mt-3 flex shrink-0 items-center justify-between">
          <button onClick={() => setIndex(i => Math.max(0, i - 1))} disabled={courante === 0}
            className="rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20 disabled:opacity-30">← Précédent</button>
          <div className="flex items-center gap-2">
            {questions.map((q, i) => (
              <button key={q.cle} onClick={() => setIndex(i)} aria-label={`Question ${i + 1}`}
                className={`h-3 w-3 rounded-full transition-colors ${i === courante ? 'bg-amber-200' : finiesIci[q.cle] ? 'bg-emerald-400/70' : 'bg-white/25 hover:bg-white/50'}`} />
            ))}
            <span className="ml-2 text-sm text-white/60">{courante + 1} / {n}</span>
          </div>
          <button onClick={() => setIndex(i => Math.min(n - 1, i + 1))} disabled={courante === n - 1}
            className="rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20 disabled:opacity-30">Suivant →</button>
        </div>
      )}
    </div>
  );
}

function UneQuestion({ q, diapo, dire, jouer, preparees, compact = false, onReponse, onFinie, essaisMax = 2 }: {
  q: QuestionDiapo; diapo: { title: string; speech: string; memoire?: string }; dire: (texte: string) => Promise<boolean>;
  jouer: (url: string) => void; preparees?: Record<string, Partial<Record<'juste' | '1' | '2', ReactionPreparee>>>;
  compact?: boolean; onReponse?: (r: ReponseNotee) => void;
  /** Appelé une fois quand la question est terminée ; `fraiche` : terminée à l'instant (pas retrouvée en mémoire). */
  onFinie?: (cle: string, correct: boolean, fraiche: boolean) => void;
  /** Essais permis avant que la question soit close (2 : l'indice puis la réponse ; 1 : question jumelle d'une reprise). */
  essaisMax?: number;
}) {
  const grand = compact ? 'text-sm' : 'text-lg', titre = compact ? 'text-base' : 'text-xl';
  // Une réponse donnée reste donnée : l'état de la question est gardé (par élève, cours, diapositive et question),
  // et retrouvé si l'élève ferme le tableau, revient sur la diapositive ou recharge la page. Il ne peut pas
  // recommencer pour « effacer » sa réponse : c'est elle qui compte pour le suivi des acquis.
  const memoire = `reponse:${diapo.memoire || ''}:${q.cle}`;
  const sauve = useMemo<Partial<{ tentative: number; exclus: number[]; pris: number | null; retour: { correct: boolean | null; ecrit: string } | null }>>(() => {
    try { return JSON.parse(localStorage.getItem(memoire) || '{}'); } catch { return {}; }
  }, [memoire]);
  const [tentative, setTentative] = useState(sauve.tentative ?? 1);
  const [exclus, setExclus] = useState<number[]>(sauve.exclus ?? []);
  const [pris, setPris] = useState<number | null>(sauve.pris ?? null);
  const [texte, setTexte] = useState('');
  const [attente, setAttente] = useState(false);
  const [retour, setRetour] = useState<{ correct: boolean | null; ecrit: string } | null>(sauve.retour ?? null);
  const finie = retour?.correct === true || (retour?.correct === false && tentative > essaisMax) || (q.type === 'directe' && retour?.correct !== null && retour !== null);
  const vientDeFinir = useRef(false);
  const finieSignalee = useRef(false);
  useEffect(() => {
    if (!finie || attente || finieSignalee.current) return;
    finieSignalee.current = true;
    onFinie?.(q.cle, retour?.correct === true, vientDeFinir.current);
  }, [finie, attente, onFinie, q.cle, retour]);
  useEffect(() => {
    if (!retour || attente) return;
    try { localStorage.setItem(memoire, JSON.stringify({ tentative, exclus, pris, retour })); } catch { /* sans mémoire locale, la réponse reste au moins sur le serveur */ }
  }, [memoire, tentative, exclus, pris, retour, attente]);

  const envoyer = async (reponse: string, indice: number | null) => {
    if (attente || finie) return;
    vientDeFinir.current = true;
    const verdict = indice !== null && q.bonne !== undefined ? indice === q.bonne : null;
    // La réaction préparée pour cette réponse : tout de suite, avec sa voix.
    const prete = indice !== null && verdict !== null ? preparees?.[String(indice)]?.[verdict ? 'juste' : (tentative >= essaisMax ? '2' : '1')] : undefined;
    if (prete) {
      onReponse?.({ cle: q.cle, type: q.type, enonce: q.enonce, reponse, tentative, correct: verdict, preparee: true });
      setPris(indice);
      setRetour({ correct: verdict, ecrit: prete.ecrit });
      if (prete.audio) jouer(prete.audio); else void dire(prete.parole);
      if (verdict === false) { setExclus(e => [...e, indice!]); setTentative(t => t + 1); }
      return;
    }
    setAttente(true); setPris(indice);
    if (verdict !== null) setRetour({ correct: verdict, ecrit: '' });     // la couleur tout de suite, la voix suit
    try {
      const r = await appelerApi<{ correct: boolean | null; parole: string; ecrit: string }>('/course-player/answer-reaction', {
        diapo, question: { type: q.type, enonce: q.enonce, choix: q.choix, bonne: q.bonne }, reponse, tentative, verdict,
      });
      onReponse?.({ cle: q.cle, type: q.type, enonce: q.enonce, reponse, tentative, correct: r.correct, preparee: false });
      setRetour({ correct: r.correct, ecrit: r.ecrit });
      void dire(r.parole);
      if (r.correct === false) {
        if (indice !== null) setExclus(e => [...e, indice]);
        setTentative(t => t + 1);
      }
    } catch {
      if (verdict !== null) onReponse?.({ cle: q.cle, type: q.type, enonce: q.enonce, reponse, tentative, correct: verdict, preparee: false });
      setRetour(verdict === null ? { correct: null, ecrit: 'Le professeur ne peut pas répondre pour le moment.' }
        : { correct: verdict, ecrit: verdict ? 'Juste.' : (q.explication || 'Pas tout à fait : réessaie.') });
      if (verdict === false) { if (indice !== null) setExclus(e => [...e, indice]); setTentative(t => t + 1); }
    } finally { setAttente(false); }
  };

  return (
    <div className="flex h-full min-h-0 flex-col overflow-y-auto rounded-xl border border-white/15 p-4">
      <p className={`${titre} text-amber-100`}><Formule t={q.enonce} /></p>
      {q.choix && (
        <div className={q.type === 'vrai_faux' ? 'mt-2 flex gap-2' : `mt-2 ${compact ? 'space-y-1' : 'space-y-2'}`}>
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
        <form onSubmit={e => { e.preventDefault(); if (texte.trim()) void envoyer(texte.trim(), null); }} className="mt-2 flex gap-2">
          <input value={texte} onChange={e => setTexte(e.target.value)} disabled={attente || finie} placeholder="Ta réponse…"
            className="flex-1 rounded-lg border border-white/20 bg-black/30 px-3 py-2 text-base outline-none focus:border-cyan-300" />
          <button disabled={attente || finie || !texte.trim()} className="rounded-lg bg-cyan-500/30 px-4 py-2 text-sm disabled:opacity-40">Répondre</button>
        </form>
      )}
      {attente && <p className="mt-2 text-sm text-white/60 animate-pulse">Le professeur regarde ta réponse…</p>}
      {retour && !attente && retour.ecrit && (
        <p className={`mt-2 ${grand} ${retour.correct === true ? 'text-emerald-200' : retour.correct === false ? 'text-rose-200' : 'text-amber-200'}`}>
          {retour.correct === true ? '✔ ' : retour.correct === false ? (finie ? '✘ ' : '↻ ') : '? '}<Formule t={retour.ecrit} />
        </p>
      )}
    </div>
  );
}

function QuestionSurResultat({ reaction, onRepondre, onContinuer }: {
  reaction: Extract<Reaction, { phase: 'question' }>;
  onRepondre: (correct: boolean | null, reponse?: string) => void;
  onContinuer: () => void;
}) {
  const { question: q, verdict, ecrit } = reaction;
  const [pris, setPris] = useState<number | null>(null);
  const [vf, setVf] = useState<Record<number, boolean>>({});
  const [texte, setTexte] = useState('');
  const affirmations = q.affirmations || [];
  return (
    <div className="mt-2 space-y-3" style={{ fontFamily: CRAIE }}>
      {ecrit && <p className="text-lg text-white/85"><Formule t={ecrit} /></p>}
      <p className="text-lg font-semibold text-amber-100"><Formule t={q.enonce} /></p>
      {q.type === 'qcm' && (q.choix || []).map((c, i) => {
        const montre = verdict && (i === q.bonne || i === pris);
        return (
          <button key={i} disabled={!!verdict} onClick={() => { setPris(i); onRepondre(i === q.bonne); }}
            className={`block w-full rounded-lg border px-3 py-2 text-left text-base ${montre ? (i === q.bonne ? 'border-emerald-400 bg-emerald-500/20' : 'border-rose-400 bg-rose-500/20') : 'border-white/15 hover:bg-white/5'}`}>
            {c}
          </button>
        );
      })}
      {q.type === 'vrai_faux' && affirmations.map((a, i) => (
        <div key={i} className="rounded-lg border border-white/15 px-3 py-2">
          <div className="text-base">{a.texte}</div>
          <div className="mt-1 flex gap-2">
            {[true, false].map(v => (
              <button key={String(v)} disabled={!!verdict} onClick={() => {
                const suite = { ...vf, [i]: v }; setVf(suite);
                if (Object.keys(suite).length === affirmations.length) onRepondre(affirmations.every((x, k) => suite[k] === x.vrai));
              }}
                className={`rounded px-3 py-1 text-sm ${vf[i] === v ? (verdict ? (v === a.vrai ? 'bg-emerald-500/30' : 'bg-rose-500/30') : 'bg-white/30') : 'bg-white/10'}`}>
                {v ? 'Vrai' : 'Faux'}
              </button>
            ))}
          </div>
        </div>
      ))}
      {q.type === 'directe' && (
        <form onSubmit={e => { e.preventDefault(); if (texte.trim()) onRepondre(null, texte.trim()); }} className="flex gap-2">
          <input value={texte} onChange={e => setTexte(e.target.value)} disabled={!!verdict} placeholder="Ta réponse…"
            className="flex-1 rounded-lg border border-white/20 bg-black/30 px-3 py-2 text-base outline-none focus:border-cyan-300" />
          <button disabled={!!verdict || !texte.trim()} className="rounded-lg bg-cyan-500/30 px-4 py-2 text-sm disabled:opacity-40">Répondre</button>
        </form>
      )}
      {verdict && (
        <>
          <p className={`text-base ${verdict.correct ? 'text-emerald-200' : 'text-rose-200'}`}>{verdict.correct ? '✔ Juste. ' : '✘ '}{verdict.ecrit}</p>
          <button onClick={onContinuer} className="rounded-full bg-emerald-500/30 px-4 py-2 text-sm hover:bg-emerald-500/40">Continuer</button>
        </>
      )}
    </div>
  );
}

function Bulle({ children, actif, pulse, disabled, onClick }: { children: ReactNode; actif?: boolean; pulse?: boolean; disabled?: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`h-10 rounded-full px-4 text-sm transition-colors disabled:opacity-30 ${actif ? 'bg-amber-200 text-black' : 'bg-white/10 hover:bg-white/20'} ${pulse ? 'animate-pulse ring-2 ring-amber-200/60' : ''}`}
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
