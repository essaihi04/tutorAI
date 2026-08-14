import { useEffect, useRef, useState, useCallback, memo } from 'react';
import 'katex/dist/katex.min.css';
import { renderMixedContent, renderDisplayMath, containsArabic } from './MathBoard';
import { speechService } from '../../services/speechService';
import { boardVoice, type BoardSpeakHandle } from '../../services/boardVoice';
import { toSpokenText, estimateSpeechMs } from '../../utils/mathSpeech';
import { useSessionStore } from '../../stores/sessionStore';

/**
 * LiveBoard — "Mode Prof en Direct"
 *
 * Rejoue un script pédagogique comme un vrai professeur au tableau :
 * il ÉCRIT progressivement (révélation manuscrite), DESSINE à côté
 * (tracé animé sur une zone SVG), EFFACE des zones, fait des PAUSES
 * et commente (narration — futur point d'accroche audio/TTS).
 *
 * Script = { title, steps: LiveStep[] } reçu via le message WebSocket
 * `whiteboard_live` (action <ui> "show_live" côté LLM).
 */

// ── Types ──────────────────────────────────────────────────────────

interface LiveLine {
  type?: string; // title | subtitle | text | math | step | box | note | tip | warning | separator
  content: string;
  color?: string;
}

interface DrawPoint { x: number; y: number }

interface LiveDrawElement {
  id?: string;
  type: 'line' | 'arrow' | 'rect' | 'circle' | 'text' | 'path';
  points?: DrawPoint[];
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  radius?: number;
  text?: string;
  label?: string;
  color?: string;
  strokeWidth?: number;
  fontSize?: number;
}

export interface LiveStep {
  action: 'write' | 'draw' | 'erase' | 'pause' | 'narrate' | 'ask' | 'zoom';
  line?: LiveLine;          // write
  elements?: LiveDrawElement[]; // draw
  zone?: 'text' | 'draw' | 'all'; // erase
  duration?: number;        // pause (ms)
  text?: string;            // narrate | ask (question posée)
  /** Phrase à prononcer pendant un `write` (sinon la ligne est transcrite),
   *  un `draw` (le prof commente son croquis) ou un `zoom`. */
  say?: string;
  /** ask : boutons de réponse proposés (la bonne + distracteurs). */
  options?: string[];
  /** zoom : point visé (coordonnées croquis 0-500 × 0-400) + échelle.
   *  scale 1 = retour au tableau entier. */
  x?: number;
  y?: number;
  scale?: number;
  target?: 'draw' | 'text';
}

export interface LiveScript {
  title?: string;
  steps: LiveStep[];
}

interface LiveBoardProps {
  script: LiveScript;
  isVisible: boolean;
  onClose?: () => void;
  /** Envoie une question de l'élève au professeur (chat ou voix) pendant le cours. */
  onStudentMessage?: (text: string) => void;
  /** Dernière réponse texte du professeur — affichée dans la bulle de réponse du plein écran. */
  assistantReply?: string | null;
  /** Le professeur réfléchit (requête LLM en cours). */
  busy?: boolean;
  /** false = tableau muet (la narration est portée par l'audio du chat). */
  voiceEnabled?: boolean;
  /**
   * true tant que la voix du chat parle.
   *
   * C'est LE signal de synchronisation : le tableau n'écrit que pendant que
   * le professeur parle. Sans lui, le script démarrait dès sa réception et
   * finissait de s'écrire bien avant que le premier son n'arrive — la
   * synthèse prend plusieurs secondes.
   */
  audioActive?: boolean;
}

// ── Palette craie (tableau sombre) ─────────────────────────────────

const CHALK: Record<string, string> = {
  red: '#f87171', blue: '#60a5fa', green: '#4ade80', orange: '#fb923c',
  purple: '#c084fc', cyan: '#22d3ee', pink: '#f472b6', yellow: '#facc15',
  white: '#e2e8f0', black: '#e2e8f0',
};
const chalk = (c?: string) => (c ? (CHALK[c] || c) : '#e2e8f0');

// ── Rendu texte + LaTeX ────────────────────────────────────────────
// Le moteur de rendu est celui de MathBoard, éprouvé en production :
// il ré-encapsule le LaTeX nu (`\mathcal{D}_f` sans délimiteurs $),
// distingue une vraie formule d'une phrase française entre $…$, et gère
// les commandes que le LLM émet sans `$`. Une copie locale simplifiée
// avait fait s'afficher `mathcalD_f` et `neq` en toutes lettres.
const renderMixed = renderMixedContent;

// ── Durées (ms) ────────────────────────────────────────────────────

const clampMs = (v: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, v));
const writeDuration = (content: string) => clampMs((content || '').length * 55, 600, 6500);
const narrateDuration = (text: string) => clampMs((text || '').length * 45, 1500, 6000);
const DRAW_ELEMENT_STAGGER = 500;
const DRAW_ELEMENT_MS = 800;
const ERASE_MS = 700;

// ── Entrées d'affichage internes ───────────────────────────────────

interface WrittenEntry {
  key: number;
  line: LiveLine;
  revealMs: number;
  /** true = la révélation suit la voix, pas une durée fixe. */
  voiceDriven?: boolean;
  stepNumber?: number;
}
interface DrawnEntry { key: number; el: LiveDrawElement; delayMs: number; drawMs: number }

function LiveBoardInner({ script, isVisible, onClose, onStudentMessage, assistantReply, busy, voiceEnabled = true, audioActive = false }: LiveBoardProps) {
  const [written, setWritten] = useState<WrittenEntry[]>([]);
  const [drawn, setDrawn] = useState<DrawnEntry[]>([]);
  const [narration, setNarration] = useState<string | null>(null);
  const [erasingZone, setErasingZone] = useState<'text' | 'draw' | 'all' | null>(null);
  const [playing, setPlaying] = useState(true);
  const [finished, setFinished] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [stepIndex, setStepIndex] = useState(0);

  // Le professeur parle pendant qu'il écrit : la révélation de la ligne en
  // cours est pilotée par la progression réelle de la voix (word boundaries),
  // pas par une durée devinée.
  const [soundOn, setSoundOn] = useState(true);
  const [voiceReveal, setVoiceReveal] = useState(1);
  // Clé de la ligne écrite que la voix pilote EN CE MOMENT. Sans elle, un
  // narrate/ask qui remet voiceReveal à 0 faisait disparaître puis réapparaître
  // la dernière ligne écrite (c'est elle qui suivait voiceReveal par défaut).
  const [voiceKey, setVoiceKey] = useState<number | null>(null);

  // ── Question du professeur (step `ask`) : le tableau attend l'élève ──
  const [pendingAsk, setPendingAsk] = useState<{ text: string; options: string[] } | null>(null);
  const [askAnswer, setAskAnswer] = useState<string | null>(null);

  // ── Loupe du tableau : zoom sur un endroit précis + déplacement ──
  const [zoom, setZoom] = useState(1);
  const [pan, setPanState] = useState({ x: 0, y: 0 });
  const [dragging, setDragging] = useState(false);

  // ── Mode plein écran « cours magistral » ──
  // Dès que le professeur prend la parole, le tableau occupe tout l'écran
  // avec une interface minimale (auto-masquée) pour garder l'élève concentré.
  // L'élève peut « lever la main » : le cours se met en pause et il pose sa
  // question au clavier ou à la voix, comme dans une vraie salle de classe.
  const [focus, setFocus] = useState(true);
  const [controlsVisible, setControlsVisible] = useState(true);
  const [askOpen, setAskOpen] = useState(false);
  const [questionText, setQuestionText] = useState('');
  const [listening, setListening] = useState(false);
  const [awaitingReply, setAwaitingReply] = useState(false);
  const language = useSessionStore((s) => s.language);

  const runIdRef = useRef(0);
  const playingRef = useRef(true);
  const speedRef = useRef(1);
  const keyRef = useRef(0);
  const textZoneRef = useRef<HTMLDivElement>(null);
  const stepCounterRef = useRef(0);
  const soundOnRef = useRef(true);
  // Horloge d'écriture de la ligne en cours (id de setInterval).
  const revealClockRef = useRef<number | null>(null);
  const viewportRef = useRef<HTMLDivElement>(null);
  const zoomRef = useRef(1);
  const panRef = useRef({ x: 0, y: 0 });
  const pointersRef = useRef(new Map<number, { x: number; y: number }>());
  const pinchRef = useRef<{ dist: number; zoom: number } | null>(null);
  const panDragRef = useRef<{ startX: number; startY: number; panX: number; panY: number } | null>(null);
  const hideTimerRef = useRef<number | null>(null);
  const replyBaselineRef = useRef<string | null>(null);
  const questionFieldRef = useRef<HTMLInputElement>(null);
  // Résout la promesse sur laquelle le script attend la réponse de l'élève.
  const askResolveRef = useRef<(() => void) | null>(null);
  // Lecture audio en cours (notre voix) + langue de la session, lues depuis
  // le moteur de lecture sans le faire dépendre du cycle de rendu React.
  const voiceHandleRef = useRef<BoardSpeakHandle | null>(null);
  const langRef = useRef<'fr' | 'ar' | 'mixed'>('fr');
  const drawZoneRef = useRef<HTMLDivElement>(null);
  // Zoom piloté par le prof — via ref car défini après play() dans le fichier.
  const zoomToPointRef = useRef<(x: number, y: number, s: number) => void>(() => {});
  // État de la voix du chat, vu depuis la boucle de lecture (voir plus bas).
  const audioActiveRef = useRef(false);
  const audioStartedRef = useRef(false);
  const audioEndedRef = useRef(false);
  /** Instant au-delà duquel on démarre même sans voix (ms, horloge perf). */
  const startDeadlineRef = useRef(0);

  playingRef.current = playing;
  speedRef.current = speed;

  // ── Synchronisation écriture ↔ parole ──────────────────────────────
  //
  // Le tableau avance UNIQUEMENT pendant que la voix du chat parle. Trois
  // garde-fous, chacun pour une panne réelle :
  //
  //  • `audioStartedRef` — avant le premier son, on patiente. Sinon le script
  //    s'écrivait en entier pendant les ~10 s de synthèse, et l'élève voyait
  //    tout le tableau puis entendait le cours par-dessus un tableau fini.
  //  • `audioEndedRef` — une fois la voix terminée, on déroule librement le
  //    reste : le texte du chat est plus court que le script, et geler le
  //    tableau à mi-chemin serait pire que de le finir sans voix.
  //  • `startDeadlineRef` — si aucun son n'arrive (TTS coupé, tunnel mort,
  //    autoplay refusé), on démarre quand même après ce délai. Un tableau
  //    silencieux vaut mieux qu'un tableau figé.
  audioActiveRef.current = audioActive;
  if (audioActive && !audioStartedRef.current) audioStartedRef.current = true;
  if (!audioActive && audioStartedRef.current) audioEndedRef.current = true;
  // `voiceEnabled=false` : le script est trop maigre pour porter le cours,
  // c'est l'audio du chat qui narre — le tableau doit rester muet, sinon
  // deux voix se superposeraient.
  soundOnRef.current = soundOn && voiceEnabled;
  langRef.current = language;

  // La voix vient du serveur : elle est toujours disponible, quel que soit le
  // navigateur (plus de dépendance à la synthèse Web Speech). Le bouton est
  // masqué quand c'est le chat qui porte la narration : le tableau n'a alors
  // aucune voix à couper.
  const canSpeak = voiceEnabled;

  const hasDrawSteps = Array.isArray(script?.steps) && script.steps.some(
    s => s?.action === 'draw' && Array.isArray(s.elements) && s.elements.length > 0
  );

  /**
   * Texte réellement prononcé pour un step — `say` s'il existe, sinon la
   * ligne écrite (transcrite) ou la narration.
   */
  const spokenTextOf = useCallback((step: LiveStep): string => {
    if (!step) return '';
    if (typeof step.say === 'string' && step.say.trim()) return step.say.trim();
    if (step.action === 'write' && typeof step.line?.content === 'string') return step.line.content;
    if ((step.action === 'narrate' || step.action === 'ask') && typeof step.text === 'string') return step.text;
    return '';
  }, []);

  /**
   * Prépare l'audio des prochaines répliques pendant que la courante est lue.
   *
   * Le GPU génère à peu près une seconde d'audio par seconde de calcul : sans
   * ce préchargement, le tableau s'arrêterait à chaque ligne le temps de la
   * synthèse. On garde une petite avance (2 répliques) pour ne pas saturer la
   * file d'un coup — le serveur traite un job à la fois.
   */
  const prefetchFrom = useCallback((steps: LiveStep[], fromIndex: number) => {
    // Tableau muet (son coupé, ou narration portée par le chat) : ne pas
    // faire générer un audio qui ne sera jamais joué.
    if (!soundOnRef.current) return;
    let queued = 0;
    for (let j = fromIndex; j < steps.length && queued < 2; j++) {
      const t = toSpokenText(spokenTextOf(steps[j]));
      if (!t) continue;
      boardVoice.prefetch(t, langRef.current);
      queued += 1;
    }
  }, [spokenTextOf]);

  /**
   * Le tableau a-t-il le droit d'avancer maintenant ?
   *
   * Il suit la voix du chat : il n'écrit que pendant qu'elle parle. Les trois
   * échappatoires évitent qu'un défaut de voix ne fige le cours (voir la note
   * sur les refs de synchronisation).
   */
  const mayAdvance = useCallback((): boolean => {
    if (!voiceEnabled) return true;      // tableau autonome (mode muet assumé)
    if (audioActiveRef.current) return true;   // ça parle → on écrit
    if (audioEndedRef.current) return true;    // ça a parlé et c'est fini → on termine
    return performance.now() >= startDeadlineRef.current;  // la voix n'est jamais venue
  }, [voiceEnabled]);

  // Attente "consciente" : respecte pause + vitesse + annulation + la voix
  const wait = useCallback(async (ms: number, runId: number): Promise<boolean> => {
    let remaining = ms;
    while (remaining > 0) {
      await new Promise(r => setTimeout(r, 50));
      if (runId !== runIdRef.current) return false;
      if (playingRef.current && mayAdvance()) remaining -= 50 * speedRef.current;
    }
    return runId === runIdRef.current;
  }, [mayAdvance]);

  /**
   * Dit une ligne avec NOTRE voix (modèle serveur) en pilotant sa révélation.
   *
   * ⚠️ La synthèse du navigateur n'est plus utilisée : elle ne sait pas dire
   * la darija (elle la lit avec une voix MSA robotique, quand elle ne refuse
   * pas), alors que notre modèle est entraîné exactement pour ça. Le tableau
   * demande donc chaque fragment au serveur et joue le WAV reçu.
   *
   * L'écriture est portée par une horloge (durée estimée), RECALÉE en continu
   * sur la position réelle de lecture de l'audio. L'horloge reste nécessaire :
   * elle couvre le temps de génération avant le premier son, et prend le
   * relais si la voix échoue — sans elle, la ligne resterait figée.
   *
   * Retourne true si la parole a porté l'animation, false s'il faut retomber
   * sur l'animation minutée (son coupé, serveur indisponible, ligne muette).
   */
  const speakAndReveal = useCallback(async (raw: string, runId: number): Promise<boolean> => {
    if (!soundOnRef.current) return false;
    const spoken = toSpokenText(raw);
    if (!spoken) return false;

    const rate = speedRef.current;
    // Durée présumée de la phrase ; recalibrée sur l'audio dès qu'il démarre.
    let estimatedMs = Math.max(600, estimateSpeechMs(spoken, rate));
    let elapsed = 0;
    let revealNow = 0;
    let done = false;
    let last = performance.now();

    setVoiceReveal(0);

    // Horloge d'écriture : avance en continu, se fige quand l'élève met en
    // pause, et ne dépasse jamais 99 % avant la fin réelle de la parole.
    // ⚠️ setInterval, PAS requestAnimationFrame : rAF s'arrête net dès que
    // l'onglet passe en arrière-plan ou que le navigateur suspend le rendu —
    // l'écriture restait alors gelée, puis tout apparaissait d'un coup.
    revealClockRef.current = window.setInterval(() => {
      if (done || runId !== runIdRef.current) return;
      const now = performance.now();
      const dt = now - last;
      last = now;
      if (playingRef.current) elapsed += dt;
      const pct = Math.min(0.99, elapsed / estimatedMs);
      if (pct > revealNow) {
        revealNow = pct;
        setVoiceReveal(pct);
      }
    }, 50);

    const handle = boardVoice.speak(spoken, langRef.current, (ratio) => {
      // ratio >= 1 est le signal de FIN : s'y recaler ferait sauter la ligne
      // à 99 % d'un coup — la rampe de rattrapage s'en charge en douceur.
      if (runId !== runIdRef.current || ratio <= 0 || ratio >= 1) return;
      // Position RÉELLE de lecture : on réaligne l'horloge dessus, sans
      // jamais revenir en arrière.
      const observed = ratio * estimatedMs;
      if (observed > elapsed) elapsed = observed;
      else estimatedMs = Math.max(600, elapsed / Math.max(ratio, 0.01));
    });
    voiceHandleRef.current = handle;
    // L'élève a pu mettre en pause pendant la génération de l'audio.
    if (!playingRef.current) handle.pause();

    const voiceSpoke = await handle.done;
    if (voiceHandleRef.current === handle) voiceHandleRef.current = null;

    // Voix indisponible (serveur muet, lecture refusée) : on laisse l'horloge
    // finir d'écrire lettre après lettre, plutôt que de figer la ligne.
    if (!voiceSpoke && runId === runIdRef.current) {
      while (elapsed < estimatedMs) {
        await new Promise(r => setTimeout(r, 60));
        if (runId !== runIdRef.current) break;
      }
    }

    done = true;
    if (revealClockRef.current !== null) {
      clearInterval(revealClockRef.current);
      revealClockRef.current = null;
    }
    if (runId !== runIdRef.current) return true;

    // Rattrapage en douceur : la voix et l'estimation ne finissent jamais
    // exactement ensemble. Le reste de la ligne s'écrit en une courte rampe
    // (respectant la pause) au lieu d'apparaître brusquement.
    if (revealNow < 0.97) {
      const rampMs = Math.min(800, 150 + (1 - revealNow) * 700);
      const startPct = revealNow;
      let k = 0;
      let prev = performance.now();
      while (k < 1) {
        await new Promise(r => setTimeout(r, 40));
        if (runId !== runIdRef.current) return true;
        const now = performance.now();
        if (playingRef.current) k = Math.min(1, k + (now - prev) / rampMs);
        prev = now;
        setVoiceReveal(startPct + (1 - startPct) * k);
      }
    }
    setVoiceReveal(1);
    return true;
  }, []);

  // Moteur de lecture séquentielle du script
  const play = useCallback(async (steps: LiveStep[], runId: number) => {
    for (let i = 0; i < steps.length; i++) {
      if (runId !== runIdRef.current) return;
      const step = steps[i];
      if (!step || typeof step !== 'object') continue;
      setStepIndex(i);
      // Le professeur prépare déjà ce qu'il dira ensuite.
      prefetchFrom(steps, i + 1);

      switch (step.action) {
        case 'write': {
          const line = step.line;
          if (!line || typeof line.content !== 'string') break;
          const isStep = (line.type || '') === 'step';
          if (isStep) stepCounterRef.current += 1;

          // Texte à prononcer : le script peut l'imposer via `say`
          // (le LLM formule alors une phrase de prof), sinon on transcrit
          // la ligne elle-même en français lisible.
          const toSay = typeof step.say === 'string' && step.say.trim()
            ? step.say.trim()
            : line.content;
          const willSpeak = soundOnRef.current && !!toSpokenText(toSay);

          const entry: WrittenEntry = {
            key: ++keyRef.current,
            line,
            // En mode voix la durée n'est pas connue à l'avance : la
            // révélation est pilotée par speakAndReveal.
            revealMs: willSpeak ? 0 : writeDuration(line.content) / speedRef.current,
            voiceDriven: willSpeak,
            stepNumber: isStep ? stepCounterRef.current : undefined,
          };
          setWritten(prev => [...prev, entry]);

          if (willSpeak) {
            // C'est CETTE ligne (et aucune autre) que la voix révèle.
            setVoiceKey(entry.key);
            const spoke = await speakAndReveal(toSay, runId);
            if (runId !== runIdRef.current) return;
            setVoiceKey(null);
            if (!spoke) {
              // La voix a échoué au dernier moment : on laisse le temps de lire.
              if (!(await wait(estimateSpeechMs(toSpokenText(toSay)), runId))) return;
            }
            if (!(await wait(250, runId))) return;
          } else {
            if (!(await wait(entry.revealMs * speedRef.current + 300, runId))) return;
          }
          break;
        }
        case 'draw': {
          const els = Array.isArray(step.elements) ? step.elements.filter(e => e && e.type) : [];
          if (els.length === 0) break;
          const spd = speedRef.current;
          const entries: DrawnEntry[] = els.map((el, j) => ({
            key: ++keyRef.current,
            el,
            delayMs: (j * DRAW_ELEMENT_STAGGER) / spd,
            drawMs: DRAW_ELEMENT_MS / spd,
          }));
          setDrawn(prev => [...prev, ...entries]);
          const drawTotal = els.length * DRAW_ELEMENT_STAGGER + DRAW_ELEMENT_MS;
          // Le prof commente son croquis pendant qu'il le trace (`say` sur le
          // step draw) : la voix et le tracé courent en parallèle, et on
          // attend la fin du plus long des deux avant de continuer.
          const toSayDraw = typeof step.say === 'string' ? step.say.trim() : '';
          const spokenDraw = toSayDraw && soundOnRef.current ? toSpokenText(toSayDraw) : '';
          if (spokenDraw) {
            const handle = boardVoice.speak(spokenDraw, langRef.current);
            voiceHandleRef.current = handle;
            if (!playingRef.current) handle.pause();
            const [, waited] = await Promise.all([handle.done, wait(drawTotal, runId)]);
            if (voiceHandleRef.current === handle) voiceHandleRef.current = null;
            if (!waited || runId !== runIdRef.current) return;
          } else {
            if (!(await wait(drawTotal, runId))) return;
          }
          break;
        }
        case 'erase': {
          const zone = step.zone === 'text' || step.zone === 'draw' ? step.zone : 'all';
          setErasingZone(zone);
          if (!(await wait(ERASE_MS, runId))) return;
          if (runId !== runIdRef.current) return;
          if (zone === 'text' || zone === 'all') { setWritten([]); stepCounterRef.current = 0; }
          if (zone === 'draw' || zone === 'all') setDrawn([]);
          setErasingZone(null);
          if (!(await wait(250, runId))) return;
          break;
        }
        case 'pause': {
          const d = typeof step.duration === 'number' ? clampMs(step.duration, 200, 8000) : 900;
          if (!(await wait(d, runId))) return;
          break;
        }
        case 'narrate': {
          if (typeof step.text === 'string' && step.text.trim()) {
            const text = step.text.trim();
            setNarration(text);
            const spoke = await speakAndReveal(text, runId);
            if (runId !== runIdRef.current) return;
            // Son coupé ou voix indisponible : on laisse le temps de lire.
            if (!spoke && !(await wait(narrateDuration(text), runId))) return;
          }
          break;
        }
        case 'ask': {
          // Le professeur pose une question et S'ARRÊTE : le cours ne reprend
          // que quand l'élève répond (bouton), demande à continuer, ou pose sa
          // propre question — comme dans une vraie classe.
          const text = typeof step.text === 'string' ? step.text.trim() : '';
          if (!text) break;
          const options = Array.isArray(step.options)
            ? step.options.filter((o): o is string => typeof o === 'string' && !!o.trim()).map(o => o.trim()).slice(0, 4)
            : [];
          setPendingAsk({ text, options });
          setAskAnswer(null);
          const toAsk = typeof step.say === 'string' && step.say.trim() ? step.say.trim() : text;
          await speakAndReveal(toAsk, runId);
          if (runId !== runIdRef.current) return;
          await new Promise<void>(resolve => { askResolveRef.current = resolve; });
          if (runId !== runIdRef.current) return;
          setPendingAsk(null);
          setAskAnswer(null);
          break;
        }
        case 'zoom': {
          // Le professeur zoome lui-même sur une partie du tableau pour
          // concentrer l'attention (scale 1 = retour au tableau entier).
          const rawScale = typeof step.scale === 'number' ? step.scale : 2;
          const scale = Math.max(1, Math.min(4, rawScale));
          const vp = viewportRef.current;
          if (vp) {
            if (scale <= 1.01) {
              zoomToPointRef.current(0, 0, 1);
            } else {
              const vr = vp.getBoundingClientRect();
              let sx = vr.width / 2, sy = vr.height / 2;
              const target = step.target === 'text' ? 'text' : 'draw';
              if (target === 'draw' && drawZoneRef.current) {
                // Coordonnées croquis (0-500 × 0-400, viewBox `meet` centré)
                // → pixels écran relatifs au viewport.
                const zr = drawZoneRef.current.getBoundingClientRect();
                const s = Math.min(zr.width / 500, zr.height / 400) || 1;
                const px = Math.max(0, Math.min(500, step.x ?? 250));
                const py = Math.max(0, Math.min(400, step.y ?? 200));
                sx = zr.left - vr.left + (zr.width - 500 * s) / 2 + px * s;
                sy = zr.top - vr.top + (zr.height - 400 * s) / 2 + py * s;
              } else if (target === 'text' && textZoneRef.current) {
                // Vise la dernière ligne écrite.
                const lines = textZoneRef.current.querySelectorAll('.live-line');
                const lastLine = lines[lines.length - 1] as HTMLElement | undefined;
                if (lastLine) {
                  const lr = lastLine.getBoundingClientRect();
                  sx = lr.left - vr.left + Math.min(lr.width, 240) / 2;
                  sy = lr.top - vr.top + lr.height / 2;
                }
              }
              // Écran → coordonnées non transformées du contenu.
              const cx = (sx - panRef.current.x) / zoomRef.current;
              const cy = (sy - panRef.current.y) / zoomRef.current;
              zoomToPointRef.current(cx, cy, scale);
            }
          }
          const zsay = typeof step.say === 'string' ? step.say.trim() : '';
          if (zsay) {
            const spoke = await speakAndReveal(zsay, runId);
            if (runId !== runIdRef.current) return;
            if (!spoke && !(await wait(narrateDuration(zsay), runId))) return;
          } else {
            if (!(await wait(900, runId))) return;
          }
          break;
        }
        default:
          break;
      }
    }
    if (runId === runIdRef.current) setFinished(true);
  }, [wait, speakAndReveal, prefetchFrom]);

  // (Re)démarrage quand un nouveau script arrive
  useEffect(() => {
    const runId = ++runIdRef.current;
    setWritten([]);
    setDrawn([]);
    setNarration(null);
    setErasingZone(null);
    setFinished(false);
    setStepIndex(0);
    setPlaying(true);
    setVoiceReveal(1);
    stepCounterRef.current = 0;
    // Nouveau cours : le professeur reprend la parole en plein écran, la
    // question en cours est close (la réponse arrive justement via ce script).
    setFocus(true);
    setAskOpen(false);
    setQuestionText('');
    setAwaitingReply(false);
    setVoiceKey(null);
    setPendingAsk(null);
    setAskAnswer(null);
    askResolveRef.current?.();
    askResolveRef.current = null;

    // Nouveau tour : on réarme la synchronisation sur la voix. Le script
    // patiente jusqu'au premier son — sauf si aucun ne vient dans les 15 s,
    // auquel cas il se déroule en silence plutôt que de rester figé. Ce délai
    // couvre largement la synthèse (≈ 1 s de calcul par seconde d'audio).
    audioStartedRef.current = false;
    audioEndedRef.current = false;
    startDeadlineRef.current = performance.now() + 15000;

    // Le tableau prend la parole : on coupe la voix du chat pour ce tour,
    // sinon deux voix se superposent (le backend lit déjà la réponse).
    voiceHandleRef.current?.stop();
    voiceHandleRef.current = null;
    boardVoice.stop();

    if (script && Array.isArray(script.steps) && script.steps.length > 0) {
      // La voix vient du serveur : plus besoin d'attendre la liste des voix
      // du navigateur, le cours démarre immédiatement. On lance en revanche
      // la génération des premières répliques pour que le professeur n'ait
      // pas à marquer un temps d'arrêt entre chaque ligne.
      prefetchFrom(script.steps, 0);
      play(script.steps, runId);
    }
    return () => {
      runIdRef.current += 1;
      voiceHandleRef.current?.stop();
      voiceHandleRef.current = null;
      boardVoice.stop();
      if (revealClockRef.current !== null) {
        clearInterval(revealClockRef.current);
        revealClockRef.current = null;
      }
      // Ne jamais laisser le moteur suspendu sur une question sans réponse.
      askResolveRef.current?.();
      askResolveRef.current = null;
    };
  }, [script, play, prefetchFrom]);

  // Pause / reprise : la voix du professeur suit l'état de lecture.
  useEffect(() => {
    const h = voiceHandleRef.current;
    if (!h) return;
    if (playing) h.resume();
    else h.pause();
  }, [playing]);

  // Couper le son doit faire taire la ligne en cours immédiatement.
  useEffect(() => {
    if (!soundOn) {
      voiceHandleRef.current?.stop();
      voiceHandleRef.current = null;
      boardVoice.stop();
    }
  }, [soundOn]);

  // Auto-scroll de la zone d'écriture
  useEffect(() => {
    const zone = textZoneRef.current;
    if (zone) zone.scrollTo({ top: zone.scrollHeight, behavior: 'smooth' });
  }, [written.length]);

  // ⏭ Aller à la fin : état final calculé d'un coup
  const skipToEnd = useCallback(() => {
    runIdRef.current += 1;
    voiceHandleRef.current?.stop();
    voiceHandleRef.current = null;
    boardVoice.stop();
    if (revealClockRef.current !== null) {
      clearInterval(revealClockRef.current);
      revealClockRef.current = null;
    }
    askResolveRef.current?.();
    askResolveRef.current = null;
    setPendingAsk(null);
    setAskAnswer(null);
    setVoiceKey(null);
    setVoiceReveal(1);
    const finalWritten: WrittenEntry[] = [];
    const finalDrawn: DrawnEntry[] = [];
    let lastNarration: string | null = null;
    let stepNo = 0;
    (script?.steps || []).forEach(step => {
      if (!step) return;
      if (step.action === 'write' && step.line?.content !== undefined) {
        const isStep = (step.line.type || '') === 'step';
        if (isStep) stepNo += 1;
        finalWritten.push({ key: ++keyRef.current, line: step.line, revealMs: 0, stepNumber: isStep ? stepNo : undefined });
      } else if (step.action === 'draw' && Array.isArray(step.elements)) {
        step.elements.forEach(el => el && el.type && finalDrawn.push({ key: ++keyRef.current, el, delayMs: 0, drawMs: 0 }));
      } else if (step.action === 'erase') {
        const zone = step.zone === 'text' || step.zone === 'draw' ? step.zone : 'all';
        if (zone === 'text' || zone === 'all') { finalWritten.length = 0; stepNo = 0; }
        if (zone === 'draw' || zone === 'all') finalDrawn.length = 0;
      } else if (step.action === 'narrate' && step.text) {
        lastNarration = step.text;
      }
    });
    setWritten(finalWritten);
    setDrawn(finalDrawn);
    setNarration(lastNarration);
    setErasingZone(null);
    setFinished(true);
    setStepIndex(Math.max(0, (script?.steps?.length || 1) - 1));
  }, [script]);

  // ↻ Rejouer
  const replay = useCallback(() => {
    const runId = ++runIdRef.current;
    voiceHandleRef.current?.stop();
    voiceHandleRef.current = null;
    boardVoice.stop();
    if (revealClockRef.current !== null) {
      clearInterval(revealClockRef.current);
      revealClockRef.current = null;
    }
    askResolveRef.current?.();
    askResolveRef.current = null;
    setPendingAsk(null);
    setAskAnswer(null);
    setVoiceKey(null);
    setWritten([]);
    setDrawn([]);
    setNarration(null);
    setErasingZone(null);
    setFinished(false);
    setStepIndex(0);
    setPlaying(true);
    setVoiceReveal(1);
    stepCounterRef.current = 0;
    if (script?.steps?.length) play(script.steps, runId);
  }, [script, play]);

  // ── Loupe : zoomer/dézoomer sur un point donné ────────────────────
  // Le point visé (curseur, double-clic, milieu du pincement) reste fixe à
  // l'écran pendant le changement d'échelle, comme une loupe posée sur le
  // tableau. Le déplacement est borné : on ne sort jamais du tableau.

  const clampPan = useCallback((x: number, y: number, z: number) => {
    const el = viewportRef.current;
    if (!el || z <= 1) return { x: 0, y: 0 };
    const minX = el.clientWidth * (1 - z);
    const minY = el.clientHeight * (1 - z);
    return { x: Math.min(0, Math.max(minX, x)), y: Math.min(0, Math.max(minY, y)) };
  }, []);

  const applyZoom = useCallback((next: number, cx: number, cy: number) => {
    const z = zoomRef.current;
    const nz = Math.min(4, Math.max(1, next));
    const ratio = nz / z;
    const p = panRef.current;
    const cl = clampPan(cx - (cx - p.x) * ratio, cy - (cy - p.y) * ratio, nz);
    zoomRef.current = nz;
    panRef.current = cl;
    setZoom(nz);
    setPanState(cl);
  }, [clampPan]);

  const zoomBy = useCallback((factor: number) => {
    const el = viewportRef.current;
    if (!el) return;
    applyZoom(zoomRef.current * factor, el.clientWidth / 2, el.clientHeight / 2);
  }, [applyZoom]);

  const resetZoom = useCallback(() => applyZoom(1, 0, 0), [applyZoom]);

  // Zoom du PROFESSEUR : centre le point visé (coordonnées non transformées
  // du contenu) au milieu du viewport — c'est le geste « regardez ici ».
  const zoomToPoint = useCallback((contentX: number, contentY: number, scale: number) => {
    const el = viewportRef.current;
    if (!el) return;
    const nz = Math.min(4, Math.max(1, scale));
    const cl = clampPan(el.clientWidth / 2 - contentX * nz, el.clientHeight / 2 - contentY * nz, nz);
    zoomRef.current = nz;
    panRef.current = cl;
    setZoom(nz);
    setPanState(cl);
  }, [clampPan]);
  useEffect(() => { zoomToPointRef.current = zoomToPoint; }, [zoomToPoint]);

  // Réponse de l'élève à la question du professeur (step `ask`).
  const answerAsk = useCallback((option?: string) => {
    if (option) {
      setAskAnswer(option);
      // Laisse l'élève voir son choix, puis le cours reprend : la suite du
      // script donne la correction.
      window.setTimeout(() => {
        askResolveRef.current?.();
        askResolveRef.current = null;
      }, 500);
    } else {
      askResolveRef.current?.();
      askResolveRef.current = null;
    }
  }, []);

  // Ctrl+molette (= pincement sur pavé tactile) : zoom centré sur le curseur.
  // Molette simple quand on est déjà zoomé : déplacement du tableau.
  // Listener natif obligatoire : React attache `wheel` en mode passif,
  // ce qui rend preventDefault() inopérant et ferait zoomer toute la page.
  useEffect(() => {
    const el = viewportRef.current;
    if (!el) return;
    const onWheel = (e: WheelEvent) => {
      if (!e.ctrlKey && zoomRef.current === 1) return; // laisse défiler le texte
      e.preventDefault();
      const rect = el.getBoundingClientRect();
      if (e.ctrlKey) {
        applyZoom(zoomRef.current * Math.exp(-e.deltaY * 0.0015), e.clientX - rect.left, e.clientY - rect.top);
      } else {
        const cl = clampPan(panRef.current.x - e.deltaX, panRef.current.y - e.deltaY, zoomRef.current);
        panRef.current = cl;
        setPanState(cl);
      }
    };
    el.addEventListener('wheel', onWheel, { passive: false });
    return () => el.removeEventListener('wheel', onWheel);
  }, [applyZoom, clampPan]);

  // Un doigt (zoomé) = déplacer le tableau ; deux doigts = pincer pour zoomer.
  const onPointerDown = useCallback((e: React.PointerEvent) => {
    const el = viewportRef.current;
    if (!el) return;
    pointersRef.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    // setPointerCapture peut lever (pointeur déjà relâché) : ne jamais laisser
    // cette exception empêcher le démarrage du geste.
    const capture = () => { try { el.setPointerCapture?.(e.pointerId); } catch { /* ignore */ } };
    if (pointersRef.current.size === 2) {
      const [a, b] = [...pointersRef.current.values()];
      pinchRef.current = { dist: Math.max(1, Math.hypot(a.x - b.x, a.y - b.y)), zoom: zoomRef.current };
      panDragRef.current = null;
      capture();
    } else if (zoomRef.current > 1) {
      panDragRef.current = { startX: e.clientX, startY: e.clientY, panX: panRef.current.x, panY: panRef.current.y };
      setDragging(true);
      capture();
      e.preventDefault();
    }
  }, []);

  const onPointerMove = useCallback((e: React.PointerEvent) => {
    if (!pointersRef.current.has(e.pointerId)) return;
    pointersRef.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    const el = viewportRef.current;
    if (!el) return;
    if (pinchRef.current && pointersRef.current.size >= 2) {
      const [a, b] = [...pointersRef.current.values()];
      const dist = Math.max(1, Math.hypot(a.x - b.x, a.y - b.y));
      const rect = el.getBoundingClientRect();
      applyZoom(
        pinchRef.current.zoom * (dist / pinchRef.current.dist),
        (a.x + b.x) / 2 - rect.left,
        (a.y + b.y) / 2 - rect.top,
      );
    } else if (panDragRef.current) {
      const d = panDragRef.current;
      const cl = clampPan(d.panX + (e.clientX - d.startX), d.panY + (e.clientY - d.startY), zoomRef.current);
      panRef.current = cl;
      setPanState(cl);
    }
  }, [applyZoom, clampPan]);

  const onPointerEnd = useCallback((e: React.PointerEvent) => {
    pointersRef.current.delete(e.pointerId);
    if (pointersRef.current.size < 2) pinchRef.current = null;
    if (pointersRef.current.size === 0) {
      panDragRef.current = null;
      setDragging(false);
    }
  }, []);

  // Double-clic : zoomer sur CET endroit ; re-double-clic : revenir au tableau entier.
  const onDoubleClick = useCallback((e: React.MouseEvent) => {
    const el = viewportRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const cx = e.clientX - rect.left, cy = e.clientY - rect.top;
    if (zoomRef.current > 1.01) applyZoom(1, cx, cy);
    else applyZoom(2.2, cx, cy);
  }, [applyZoom]);

  // ── Interface minimale : les commandes s'effacent pendant que le
  // professeur parle, et réapparaissent au moindre geste de l'élève.
  const pokeControls = useCallback(() => {
    setControlsVisible(true);
    if (hideTimerRef.current) window.clearTimeout(hideTimerRef.current);
    hideTimerRef.current = window.setTimeout(() => setControlsVisible(false), 3500);
  }, []);

  useEffect(() => {
    // Hors plein écran, en pause, pendant une question ou à la fin du cours,
    // les commandes restent visibles : on ne masque que pendant l'explication.
    if (!focus || !playing || askOpen || finished) {
      if (hideTimerRef.current) window.clearTimeout(hideTimerRef.current);
      setControlsVisible(true);
      return;
    }
    pokeControls();
    return () => {
      if (hideTimerRef.current) window.clearTimeout(hideTimerRef.current);
    };
  }, [focus, playing, askOpen, finished, pokeControls]);

  // Raccourcis d'élève : Espace = pause/reprendre, Échap = fermer la question
  // puis quitter le plein écran. (Espace est ignoré pendant la saisie.)
  useEffect(() => {
    if (!focus) return;
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      const typing = !!t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
      if (e.key === 'Escape') {
        e.preventDefault();
        if (askOpen) setAskOpen(false);
        else setFocus(false);
      } else if ((e.key === ' ' || e.code === 'Space') && !typing) {
        e.preventDefault();
        setPlaying(p => !p);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [focus, askOpen]);

  // ── Lever la main : le cours se met en pause, l'élève pose sa question ──

  const submitQuestion = useCallback((raw: string) => {
    const text = raw.trim();
    if (!text || !onStudentMessage) return;
    // Mémorise la réponse actuelle : seule une NOUVELLE réponse du professeur
    // sera affichée dans la bulle (pas celle d'un tour précédent).
    replyBaselineRef.current = typeof assistantReply === 'string' ? assistantReply : null;
    setAwaitingReply(true);
    setQuestionText('');
    onStudentMessage(text);
  }, [onStudentMessage, assistantReply]);

  const openAsk = useCallback(() => {
    setPlaying(false); // le professeur s'interrompt et écoute
    setAskOpen(true);
    setTimeout(() => questionFieldRef.current?.focus(), 80);
  }, []);

  const closeAsk = useCallback(() => {
    if (listening) {
      try { speechService.stopListening(); } catch { /* noop */ }
    }
    setListening(false);
    setAskOpen(false);
  }, [listening]);

  const toggleVoiceQuestion = useCallback(() => {
    if (listening) {
      try { speechService.stopListening(); } catch { /* noop */ }
      setListening(false);
      return;
    }
    if (!speechService.isRecognitionSupported()) return;
    voiceHandleRef.current?.stop();
    voiceHandleRef.current = null;
    boardVoice.stop(); // couper la voix du prof avant d'ouvrir le micro
    setPlaying(false);
    setListening(true);
    speechService.listen({
      lang: language,
      continuous: false,
      interimResults: true,
      onResult: (text: string, isFinal: boolean) => {
        const t = (text || '').trim();
        if (isFinal) {
          if (t) submitQuestion(t);
        } else if (t) {
          setQuestionText(t);
        }
      },
      onEnd: () => setListening(false),
      onError: () => setListening(false),
    }).catch(() => setListening(false));
  }, [listening, language, submitQuestion]);

  // Réponse du professeur à afficher : uniquement une réponse arrivée APRÈS
  // l'envoi de la question de l'élève.
  const profReply =
    awaitingReply
    && typeof assistantReply === 'string'
    && assistantReply.trim()
    && assistantReply !== replyBaselineRef.current
      ? assistantReply
      : null;

  // NB : pas d'éponge côté élève — seul le professeur efface le tableau,
  // via les steps `erase` de son script (comme dans une vraie salle de classe).

  if (!isVisible || !script || !Array.isArray(script.steps) || script.steps.length === 0) return null;

  const totalSteps = script.steps.length;
  const eraseText = erasingZone === 'text' || erasingZone === 'all';
  const eraseDraw = erasingZone === 'draw' || erasingZone === 'all';

  return (
    <div
      className={
        focus
          ? 'fixed inset-0 z-[100] flex flex-col overflow-hidden'
          : 'w-full h-full flex flex-col rounded-2xl overflow-hidden shadow-lg relative'
      }
      style={{ background: '#12241c' }}
      onMouseMove={focus ? pokeControls : undefined}
      onPointerDown={focus ? pokeControls : undefined}
    >
      {/* Fil de progression du cours (plein écran) : toujours visible, jamais intrusif */}
      {focus && (
        <div className="absolute top-0 left-0 right-0 z-40 h-0.5 bg-white/10">
          <div
            className="h-full transition-all duration-500"
            style={{
              background: 'rgba(52,211,153,0.85)',
              width: `${finished ? 100 : Math.round((Math.min(stepIndex + 1, totalSteps) / totalSteps) * 100)}%`,
            }}
          />
        </div>
      )}
      <style>{`
        @keyframes liveReveal { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }
        @keyframes liveFadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
        @keyframes liveEraseWipe { from { opacity: 1; filter: blur(0); } to { opacity: 0; filter: blur(6px); } }
        @keyframes liveStroke { from { stroke-dashoffset: 100; } to { stroke-dashoffset: 0; } }
        @keyframes livePenPulse { 0%,100% { opacity: 1; } 50% { opacity: 0.25; } }
        /* La main parcourt la ligne en mode minuté (sans voix). */
        @keyframes livePenTravel { from { left: 0%; } to { left: 100%; } }
        @keyframes livePenWiggle { 0%,100% { transform: translate(-30%, 0) rotate(-8deg); } 50% { transform: translate(-30%, -1.5px) rotate(-2deg); } }
        .live-paused * { animation-play-state: paused !important; }

        /* ── Main du professeur ──
           Placée sur le bord exact de la zone révélée, elle avance donc le
           long du texte à mesure qu'il s'écrit, au lieu d'attendre à la fin
           de la ligne. Le léger tremblement imite le geste de la main. */
        .live-pen {
          position: absolute;
          bottom: -0.2em;
          font-size: 0.95em;
          line-height: 1;
          pointer-events: none;
          white-space: nowrap;
          transform: translate(-30%, 0) rotate(-8deg);
          transform-origin: 20% 80%;
          filter: drop-shadow(0 1px 2px rgba(0,0,0,0.45));
          animation: livePenWiggle 0.45s ease-in-out infinite;
          will-change: left, transform;
        }
        .live-write { position: relative; }

        /* ── Intégrité des lignes ──
           Une information ne doit JAMAIS être coupée en deux lignes : une
           formule reste d'un seul tenant, et si la colonne est trop étroite
           la ligne défile horizontalement au lieu de se briser au milieu.
           Le texte courant, lui, continue de passer à la ligne aux espaces. */
        .live-line { overflow-x: auto; overflow-y: hidden; overscroll-behavior-x: contain; }
        .live-line .katex { white-space: nowrap; }
        .live-line .katex-display { margin: 0.25em 0; overflow-x: auto; overflow-y: hidden; }
        /* Un libellé court suivi d'une formule reste solidaire. */
        .live-line .katex + .katex { margin-left: 0.25em; }
        .live-line::-webkit-scrollbar { height: 4px; }
        .live-line::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.18); border-radius: 2px; }
        .live-line::-webkit-scrollbar-track { background: transparent; }
      `}</style>

      {/* ── Barre d'outils ──
           En plein écran elle flotte au-dessus du tableau et s'efface toute
           seule pendant que le professeur parle (un geste la fait revenir). */}
      <div
        className={`${
          focus
            ? `absolute top-0 left-0 right-0 z-30 transition-all duration-300 ${controlsVisible ? '' : '-translate-y-full opacity-0 pointer-events-none'}`
            : 'shrink-0'
        } flex items-center justify-between px-3 py-1.5`}
        style={{
          background: focus ? 'rgba(13,27,21,0.92)' : '#0d1b15',
          borderBottom: '1px solid rgba(255,255,255,0.08)',
          backdropFilter: focus ? 'blur(6px)' : undefined,
        }}
      >
        <div className="flex items-center gap-2 min-w-0">
          <div className="flex items-center gap-1.5 shrink-0">
            <div className="w-2 h-2 rounded-full bg-red-400" />
            <div className="w-2 h-2 rounded-full bg-yellow-400" />
            <div className="w-2 h-2 rounded-full bg-green-400" />
          </div>
          <span className="text-white/70 text-xs font-medium shrink-0">👨‍🏫 Cours en direct</span>
          {script.title && (
            <span className="text-emerald-300/90 text-xs truncate">— {script.title}</span>
          )}
        </div>
        <div className="flex items-center gap-1.5 shrink-0">
          {!finished && (
            <span className="text-[11px] text-cyan-300/90 hidden sm:flex items-center gap-1.5 mr-1">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-300 animate-pulse" />
              {Math.min(stepIndex + 1, totalSteps)}/{totalSteps}
            </span>
          )}
          {/* Loupe : dézoomer / niveau (clic = 100 %) / zoomer.
              Masquée en plein écran (moins de boutons) : les gestes suffisent
              — double-clic, Ctrl+molette, pincement. */}
          <div className={`${focus ? 'hidden' : 'hidden sm:flex'} items-center gap-0.5 mr-0.5`}>
            <button
              onClick={() => zoomBy(1 / 1.35)}
              className="text-white/70 hover:text-white text-xs px-1.5 py-0.5 rounded hover:bg-white/10 transition-colors disabled:opacity-30"
              disabled={zoom <= 1.01}
              title="Dézoomer"
            >
              −
            </button>
            <button
              onClick={resetZoom}
              className="text-white/70 hover:text-white text-[11px] px-1 py-0.5 rounded hover:bg-white/10 transition-colors tabular-nums"
              title="Revenir au tableau entier (100 %)"
            >
              {Math.round(zoom * 100)}%
            </button>
            <button
              onClick={() => zoomBy(1.35)}
              className="text-white/70 hover:text-white text-xs px-1.5 py-0.5 rounded hover:bg-white/10 transition-colors disabled:opacity-30"
              disabled={zoom >= 3.99}
              title="Zoomer (ou : double-clic / Ctrl+molette sur un endroit du tableau)"
            >
              ＋
            </button>
          </div>
          {canSpeak && (
            <button
              onClick={() => setSoundOn(s => !s)}
              className="text-white/70 hover:text-white text-xs px-1.5 py-0.5 rounded hover:bg-white/10 transition-colors"
              title={soundOn ? 'Couper la voix du professeur' : 'Activer la voix du professeur'}
            >
              {soundOn ? '🔊' : '🔇'}
            </button>
          )}
          <button
            onClick={() => setPlaying(p => !p)}
            disabled={finished}
            className="text-white/70 hover:text-white text-xs px-2 py-0.5 rounded hover:bg-white/10 transition-colors disabled:opacity-30"
            title={playing ? 'Pause' : 'Reprendre'}
          >
            {playing ? '⏸' : '▶'}
          </button>
          <button
            onClick={() => setSpeed(s => (s >= 2 ? 1 : s + 0.5))}
            className="text-white/70 hover:text-white text-[11px] px-1.5 py-0.5 rounded hover:bg-white/10 transition-colors"
            title="Vitesse de lecture"
          >
            ×{speed}
          </button>
          {!finished ? (
            <button onClick={skipToEnd} className="text-white/70 hover:text-white text-xs px-2 py-0.5 rounded hover:bg-white/10 transition-colors" title="Tout afficher">
              ⏭
            </button>
          ) : (
            <button onClick={replay} className="text-white/70 hover:text-white text-xs px-2 py-0.5 rounded hover:bg-white/10 transition-colors" title="Rejouer l'explication">
              ↻
            </button>
          )}
          <button
            onClick={() => setFocus(f => !f)}
            className="text-white/70 hover:text-white text-xs px-1.5 py-0.5 rounded hover:bg-white/10 transition-colors"
            title={focus ? 'Quitter le plein écran (Échap)' : 'Plein écran'}
          >
            {focus ? '⤡' : '⤢'}
          </button>
          {onClose && (
            <button onClick={onClose} className="text-white/40 hover:text-white/80 text-xs px-2 py-0.5 rounded hover:bg-white/10 transition-colors">
              ✕
            </button>
          )}
        </div>
      </div>

      {/* ── Corps : écriture à gauche, dessin à droite ──
           Enveloppé dans une « loupe » : Ctrl+molette ou double-clic zoome
           sur l'endroit visé, un doigt/la souris déplace le tableau zoomé,
           deux doigts pincent pour zoomer. */}
      <div
        ref={viewportRef}
        className="flex-1 min-h-0 relative overflow-hidden"
        style={{
          touchAction: zoom > 1 ? 'none' : 'pan-y',
          cursor: zoom > 1 ? (dragging ? 'grabbing' : 'grab') : undefined,
        }}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerEnd}
        onPointerCancel={onPointerEnd}
        onDoubleClick={onDoubleClick}
      >
      <div
        className={`w-full h-full flex flex-col md:flex-row ${playing ? '' : 'live-paused'}`}
        style={{
          transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
          transformOrigin: '0 0',
          transition: dragging ? 'none' : 'transform 140ms ease-out',
          willChange: 'transform',
        }}
      >
        {/* Zone d'écriture */}
        <div
          ref={textZoneRef}
          className={`flex-1 min-w-0 overflow-y-auto px-5 ${focus ? 'pt-10 pb-16' : 'py-4'}`}
          style={eraseText ? { animation: `liveEraseWipe ${ERASE_MS}ms ease-in forwards` } : undefined}
        >
          {written.map((entry, i) => (
            <LiveWrittenLine
              key={entry.key}
              entry={entry}
              isActive={!finished && i === written.length - 1 && erasingZone === null}
              // Seule la ligne que la voix est EN TRAIN de dire se dévoile à
              // son rythme (voiceKey) ; les autres sont entièrement écrites —
              // une narration ne doit pas ré-animer la dernière ligne.
              voicePct={
                entry.voiceDriven && entry.key === voiceKey && !finished
                  ? voiceReveal
                  : undefined
              }
            />
          ))}
          {written.length === 0 && drawn.length === 0 && !finished && (
            <div className="text-white/30 text-sm italic mt-6 text-center" style={{ fontFamily: "'Patrick Hand', cursive" }}>
              Le professeur prend sa craie…
            </div>
          )}
        </div>

        {/* Zone de dessin (croquis) */}
        {hasDrawSteps && (
          <div
            ref={drawZoneRef}
            className="shrink-0 md:w-[42%] h-[45%] md:h-auto min-h-0 border-t md:border-t-0 md:border-l"
            style={{
              borderColor: 'rgba(255,255,255,0.1)',
              background: 'rgba(0,0,0,0.15)',
              ...(eraseDraw ? { animation: `liveEraseWipe ${ERASE_MS}ms ease-in forwards` } : {}),
            }}
          >
            <svg viewBox="0 0 500 400" className="w-full h-full" preserveAspectRatio="xMidYMid meet">
              {drawn.map(entry => (
                <LiveDrawnElement key={entry.key} entry={entry} />
              ))}
            </svg>
          </div>
        )}
      </div>

      {/* Badge de zoom : rappel discret + retour au tableau entier en un clic */}
      {zoom > 1.01 && (
        <button
          onClick={resetZoom}
          className={`absolute ${focus ? 'top-10' : 'bottom-2'} left-2 z-20 text-[11px] px-2 py-1 rounded-md hover:bg-white/10 transition-colors`}
          style={{ background: 'rgba(13,27,21,0.85)', color: '#a7f3d0', border: '1px solid rgba(255,255,255,0.15)' }}
          title="Revenir au tableau entier"
        >
          🔍 {Math.round(zoom * 100)} % — tableau entier
        </button>
      )}
      </div>

      {/* ── Pause façon lecteur : grand bouton central pour reprendre ── */}
      {focus && !playing && !askOpen && !pendingAsk && !finished && (
        <button
          onClick={() => setPlaying(true)}
          className="absolute inset-0 m-auto z-20 w-20 h-20 rounded-full text-3xl text-white flex items-center justify-center hover:scale-105 transition-transform"
          style={{ background: 'rgba(16,185,129,0.25)', border: '2px solid rgba(52,211,153,0.6)', backdropFilter: 'blur(4px)' }}
          title="Reprendre le cours (Espace)"
        >
          ▶
        </button>
      )}

      {/* ── Coin élève : pause + lever la main + question du prof + réponse ──
           (affiché aussi hors plein écran quand le professeur pose une question) */}
      {(focus || pendingAsk) && (
        <div className="absolute bottom-0 left-0 right-0 z-40 flex flex-col items-center gap-2 px-3 pb-3 pointer-events-none">
          {/* Réponse du professeur à la question posée */}
          {askOpen && profReply && (
            <div
              className="pointer-events-auto w-full max-w-2xl max-h-44 overflow-y-auto rounded-xl px-4 py-3 text-[14px] leading-relaxed"
              style={{ background: 'rgba(13,27,21,0.95)', border: '1px solid rgba(52,211,153,0.3)', color: '#d1fae5' }}
              dir={containsArabic(profReply) ? 'rtl' : 'ltr'}
            >
              <div className="text-[11px] mb-1" style={{ color: '#34d399' }}>👨‍🏫 Réponse du professeur</div>
              <div className="katex-dark" dangerouslySetInnerHTML={{ __html: renderMixed(profReply) }} />
            </div>
          )}

          {askOpen ? (
            /* Main levée : le cours attend, l'élève écrit ou parle */
            <div
              className="pointer-events-auto w-full max-w-2xl rounded-2xl px-3 py-2.5"
              style={{ background: 'rgba(13,27,21,0.95)', border: '1px solid rgba(255,255,255,0.15)', backdropFilter: 'blur(8px)' }}
            >
              <div className="flex items-center gap-2">
                <input
                  ref={questionFieldRef}
                  value={questionText}
                  onChange={e => setQuestionText(e.target.value)}
                  onKeyDown={e => { if (e.key === 'Enter') submitQuestion(questionText); }}
                  placeholder={listening ? '🎙️ Je t’écoute… parle maintenant' : 'Pose ta question au professeur…'}
                  className="flex-1 min-w-0 bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-sm text-white placeholder-white/35 outline-none focus:border-emerald-400/50 transition-colors"
                  disabled={busy}
                />
                {speechService.isRecognitionSupported() && (
                  <button
                    onClick={toggleVoiceQuestion}
                    disabled={busy}
                    className={`shrink-0 w-9 h-9 rounded-full flex items-center justify-center text-sm transition-all ${
                      listening ? 'bg-red-500/80 animate-pulse' : 'bg-white/10 hover:bg-white/20'
                    }`}
                    title={listening ? 'Arrêter le micro' : 'Poser la question à la voix'}
                  >
                    🎙️
                  </button>
                )}
                <button
                  onClick={() => submitQuestion(questionText)}
                  disabled={busy || !questionText.trim()}
                  className="shrink-0 w-9 h-9 rounded-full flex items-center justify-center text-sm bg-emerald-600 hover:bg-emerald-500 text-white transition-colors disabled:opacity-30"
                  title="Envoyer la question"
                >
                  ➤
                </button>
                <button
                  onClick={closeAsk}
                  className="shrink-0 w-9 h-9 rounded-full flex items-center justify-center text-sm text-white/50 hover:text-white hover:bg-white/10 transition-colors"
                  title="Fermer (Échap) — le cours reste en pause"
                >
                  ✕
                </button>
              </div>
              <div className="mt-1.5 text-[11px] text-center" style={{ color: busy ? '#67e8f9' : 'rgba(255,255,255,0.4)' }}>
                {busy
                  ? '👨‍🏫 Le professeur réfléchit à ta question…'
                  : '⏸ Le cours est en pause — pose ta question, le professeur t’écoute'}
              </div>
            </div>
          ) : pendingAsk ? (
            /* ❓ Le professeur pose une question et ATTEND la réponse */
            <div
              className="pointer-events-auto w-full max-w-2xl rounded-2xl px-4 py-3"
              style={{ background: 'rgba(13,27,21,0.96)', border: '1px solid rgba(250,204,21,0.35)', backdropFilter: 'blur(8px)' }}
            >
              <div className="flex items-start gap-2 mb-2">
                <span className="text-base leading-none mt-0.5">❓</span>
                <p
                  className="text-[14px] leading-snug"
                  dir={containsArabic(pendingAsk.text) ? 'rtl' : 'ltr'}
                  style={{ color: '#fef3c7', fontFamily: "'Patrick Hand', cursive" }}
                >
                  {pendingAsk.text}
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-1.5">
                {pendingAsk.options.map(opt => (
                  <button
                    key={opt}
                    onClick={() => answerAsk(opt)}
                    disabled={askAnswer !== null}
                    className="text-xs px-3 py-1.5 rounded-full transition-colors"
                    style={
                      askAnswer === opt
                        ? { background: 'rgba(52,211,153,0.3)', border: '1px solid rgba(52,211,153,0.6)', color: '#d1fae5' }
                        : { background: 'rgba(255,255,255,0.08)', border: '1px solid rgba(255,255,255,0.15)', color: 'rgba(255,255,255,0.85)' }
                    }
                  >
                    {opt}
                  </button>
                ))}
                {onStudentMessage && (
                  <button
                    onClick={openAsk}
                    className="text-xs px-3 py-1.5 rounded-full transition-colors"
                    style={{ background: 'rgba(16,185,129,0.15)', border: '1px solid rgba(52,211,153,0.3)', color: '#a7f3d0' }}
                    title="Répondre librement ou poser une autre question"
                  >
                    ✋ Autre réponse
                  </button>
                )}
                <button
                  onClick={() => answerAsk()}
                  className="text-xs px-3 py-1.5 rounded-full text-white/60 hover:text-white hover:bg-white/10 transition-colors ml-auto"
                >
                  Continuer ➜
                </button>
              </div>
              <div className="mt-1.5 text-[10px] text-center text-white/35">
                Le professeur attend ta réponse pour continuer le cours
              </div>
            </div>
          ) : finished && focus ? (
            /* Fin du cours : bilan et suites possibles */
            <div
              className="pointer-events-auto flex flex-wrap items-center justify-center gap-2 rounded-2xl px-4 py-2.5"
              style={{ background: 'rgba(13,27,21,0.95)', border: '1px solid rgba(255,255,255,0.15)' }}
            >
              <span className="text-sm" style={{ color: '#6ee7b7' }}>✔ Explication terminée</span>
              <button onClick={replay} className="text-white/80 hover:text-white text-xs px-3 py-1.5 rounded-full bg-white/10 hover:bg-white/15 transition-colors">
                ↻ Revoir
              </button>
              {onStudentMessage && (
                <button onClick={openAsk} className="text-xs px-3 py-1.5 rounded-full transition-colors" style={{ background: 'rgba(16,185,129,0.2)', border: '1px solid rgba(52,211,153,0.35)', color: '#a7f3d0' }}>
                  ✋ Une question ?
                </button>
              )}
              <button onClick={() => setFocus(false)} className="text-white/60 hover:text-white text-xs px-3 py-1.5 rounded-full hover:bg-white/10 transition-colors">
                Quitter le plein écran
              </button>
            </div>
          ) : focus ? (
            /* Pendant le cours : deux commandes seulement, auto-masquées */
            <div
              className={`flex items-center gap-2 transition-opacity duration-300 ${
                controlsVisible ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
              }`}
            >
              <button
                onClick={() => setPlaying(p => !p)}
                className="w-10 h-10 rounded-full flex items-center justify-center text-white text-base hover:scale-105 transition-transform"
                style={{ background: 'rgba(13,27,21,0.9)', border: '1px solid rgba(255,255,255,0.18)' }}
                title={playing ? 'Pause (Espace)' : 'Reprendre (Espace)'}
              >
                {playing ? '⏸' : '▶'}
              </button>
              {onStudentMessage && (
                <button
                  onClick={openAsk}
                  className="h-10 px-4 rounded-full text-sm flex items-center gap-2 hover:scale-[1.03] transition-transform"
                  style={{ background: 'rgba(13,27,21,0.9)', border: '1px solid rgba(52,211,153,0.35)', color: '#a7f3d0' }}
                  title="Le cours se met en pause pendant ta question"
                >
                  ✋ Poser une question
                </button>
              )}
            </div>
          ) : null}
        </div>
      )}

      {/* ── Narration du professeur (futur audio) ── */}
      {narration && (
        <div
          className="shrink-0 flex items-start gap-2 px-4 py-2.5"
          style={{
            background: 'rgba(34,211,238,0.07)',
            borderTop: '1px solid rgba(34,211,238,0.2)',
            animation: 'liveFadeIn 0.3s ease-out both',
            // En plein écran le coin élève (pause / question) occupe le bas :
            // la bulle de narration remonte pour rester lisible.
            marginBottom: focus ? '3.25rem' : undefined,
          }}
        >
          <span className="text-lg leading-none mt-0.5">💬</span>
          <p
            className="text-[13px] leading-snug"
            dir={containsArabic(narration) ? 'rtl' : 'ltr'}
            style={{ color: '#a5f3fc', fontFamily: "'Patrick Hand', cursive" }}
          >
            {narration}
          </p>
        </div>
      )}
    </div>
  );
}

// ── Ligne écrite avec révélation manuscrite ────────────────────────

/**
 * Texte qui s'écrit, avec la main du professeur au bout du trait.
 *
 * Le texte est dévoilé par un `clip-path` qui balaie de gauche à droite —
 * les lettres apparaissent donc au fur et à mesure, en se formant — et la
 * main ✍️ est positionnée exactement sur ce bord, si bien qu'elle avance
 * le long de l'écriture au lieu de rester collée à la fin de la ligne.
 */
function WritingSpan({ html, style, pct, revealMs, showPen }: {
  html: string;
  style: React.CSSProperties;
  /** 0→1 quand l'écriture suit la voix ; undefined en mode minuté. */
  pct?: number;
  revealMs: number;
  showPen: boolean;
}) {
  const voiceMode = pct !== undefined;
  // Léger surplomb : le trait est écrit juste avant d'être prononcé, comme
  // une main qui devance d'un ou deux caractères ce qu'elle dit.
  const shown = voiceMode ? Math.min(100, pct * 100 + 6) : 0;

  const clip: React.CSSProperties = voiceMode
    ? { clipPath: `inset(0 ${Math.max(0, 100 - shown)}% 0 0)`, transition: 'clip-path 120ms linear' }
    : revealMs > 0
    ? { animation: `liveReveal ${revealMs}ms linear both` }
    : {};

  const penStyle: React.CSSProperties = voiceMode
    // En mode voix la position vient de React ; le tremblement reste porté
    // par la classe CSS.
    ? { left: `${shown}%`, transition: 'left 120ms linear' }
    // En mode minuté, l'animation inline écrase celle de la classe : on
    // rejoue donc le tremblement en même temps que le déplacement.
    : { animation: `livePenTravel ${revealMs}ms linear both, livePenWiggle 0.45s ease-in-out infinite` };

  return (
    <span className="live-write" style={{ display: 'inline-block', maxWidth: '100%', position: 'relative' }}>
      <span
        className="katex-dark"
        style={{ ...style, ...clip, display: 'inline-block', maxWidth: '100%' }}
        dangerouslySetInnerHTML={{ __html: html }}
      />
      {showPen && <span className="live-pen" style={penStyle} aria-hidden="true">✍️</span>}
    </span>
  );
}

function LiveWrittenLine({ entry, isActive, voicePct }: {
  entry: WrittenEntry;
  isActive: boolean;
  /** 0→1 : avancement de la voix sur cette ligne (mode synchronisé). */
  voicePct?: number;
}) {
  const { line, revealMs, stepNumber } = entry;
  const type = (line.type || 'text').toLowerCase();
  const color = chalk(line.color);
  const rtl = containsArabic(line.content);

  if (type === 'separator') {
    return <hr className="my-3 border-white/15" style={{ animation: 'liveFadeIn 0.4s ease-out both' }} />;
  }

  const html = type === 'math' ? renderDisplayMath(line.content) : renderMixed(line.content);
  const showPen = isActive && (revealMs > 0 || voicePct !== undefined);
  const base: React.CSSProperties = { fontFamily: "'Patrick Hand', 'Caveat', cursive", color };

  const writing = (extra: React.CSSProperties) => (
    <WritingSpan
      html={html}
      style={{ ...base, ...extra }}
      pct={voicePct}
      revealMs={revealMs}
      showPen={showPen}
    />
  );

  switch (type) {
    case 'title':
      return (
        <div className="mb-3 live-line" dir={rtl ? 'rtl' : 'ltr'}>
          {writing({
            color: chalk(line.color || 'yellow'), fontSize: 24, fontWeight: 700,
            borderBottom: `2px solid ${chalk(line.color || 'yellow')}55`, paddingBottom: 2,
          })}
        </div>
      );
    case 'subtitle':
      return (
        <div className="mt-3 mb-2 live-line" dir={rtl ? 'rtl' : 'ltr'}>
          {writing({ color: chalk(line.color || 'cyan'), fontSize: 19, fontWeight: 600 })}
        </div>
      );
    case 'math':
      // renderDisplayMath route une formule pure vers KaTeX display, et une
      // ligne mixte (« Terme général : $u_n = …$ ») vers le rendu mixte —
      // sans quoi KaTeX échoue et réaffiche toute la phrase en rouge.
      return (
        <div className="my-2 live-line" style={{ textAlign: 'center' }}>
          {writing({ fontFamily: undefined, fontSize: 17, color: chalk(line.color || 'white') })}
        </div>
      );
    case 'step':
      return (
        <div className="my-1.5 flex items-start gap-2 live-line" dir={rtl ? 'rtl' : 'ltr'}>
          <span className="shrink-0 w-5 h-5 rounded-full text-[11px] font-bold flex items-center justify-center mt-0.5"
            style={{ background: `${chalk(line.color || 'blue')}33`, color: chalk(line.color || 'blue'), animation: 'liveFadeIn 0.3s ease-out both' }}>
            {stepNumber || '•'}
          </span>
          {writing({ fontSize: 16 })}
        </div>
      );
    case 'box':
      return (
        <div className="my-2 px-3 py-2 rounded-lg live-line" dir={rtl ? 'rtl' : 'ltr'}
          style={{ border: `1.5px solid ${chalk(line.color || 'green')}88`, background: `${chalk(line.color || 'green')}11`, animation: 'liveFadeIn 0.3s ease-out both' }}>
          {writing({ fontSize: 16, color: chalk(line.color || 'green') })}
        </div>
      );
    case 'note':
    case 'tip':
    case 'warning': {
      const icon = type === 'warning' ? '⚠️' : type === 'tip' ? '💡' : '📝';
      const c = chalk(line.color || (type === 'warning' ? 'orange' : type === 'tip' ? 'yellow' : 'cyan'));
      return (
        <div className="my-1.5 flex items-start gap-1.5 live-line" dir={rtl ? 'rtl' : 'ltr'}>
          <span className="text-sm mt-0.5 shrink-0" style={{ animation: 'liveFadeIn 0.3s ease-out both' }}>{icon}</span>
          {writing({ fontSize: 14.5, color: c })}
        </div>
      );
    }
    default:
      return (
        <div className="my-1 live-line" dir={rtl ? 'rtl' : 'ltr'}>
          {writing({ fontSize: 16 })}
        </div>
      );
  }
}

// ── Élément dessiné avec animation de tracé SVG ────────────────────

function LiveDrawnElement({ entry }: { entry: DrawnEntry }) {
  const { el, delayMs, drawMs } = entry;
  const color = chalk(el.color || 'white');
  const sw = el.strokeWidth || 2.5;
  const strokeAnim: React.CSSProperties = drawMs > 0
    ? { strokeDasharray: 100, strokeDashoffset: 100, animation: `liveStroke ${drawMs}ms ease-out ${delayMs}ms forwards` }
    : {};
  const fadeAnim: React.CSSProperties = drawMs > 0
    ? { opacity: 0, animation: `liveFadeIn 0.35s ease-out ${delayMs + drawMs * 0.6}ms forwards` }
    : {};
  const labelStyle: React.CSSProperties = {
    fontFamily: "'Patrick Hand', 'Caveat', cursive",
    ...fadeAnim,
  };

  switch (el.type) {
    case 'line':
    case 'path': {
      const pts = el.points || [];
      if (pts.length < 2) return null;
      const d = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x},${p.y}`).join(' ');
      return (
        <g>
          <path d={d} fill="none" stroke={color} strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round" pathLength={100} style={strokeAnim} />
          {el.label && <text x={pts[0].x} y={pts[0].y - 8} fill={color} fontSize={13} style={labelStyle}>{el.label}</text>}
        </g>
      );
    }
    case 'arrow': {
      const pts = el.points || [];
      if (pts.length < 2) return null;
      const from = pts[0], to = pts[pts.length - 1];
      const angle = Math.atan2(to.y - from.y, to.x - from.x);
      const hl = 12;
      const h1 = { x: to.x - hl * Math.cos(angle - Math.PI / 6), y: to.y - hl * Math.sin(angle - Math.PI / 6) };
      const h2 = { x: to.x - hl * Math.cos(angle + Math.PI / 6), y: to.y - hl * Math.sin(angle + Math.PI / 6) };
      const midX = (from.x + to.x) / 2, midY = (from.y + to.y) / 2;
      return (
        <g>
          <path d={`M${from.x},${from.y} L${to.x},${to.y}`} fill="none" stroke={color} strokeWidth={sw} strokeLinecap="round" pathLength={100} style={strokeAnim} />
          <polygon points={`${to.x},${to.y} ${h1.x},${h1.y} ${h2.x},${h2.y}`} fill={color} style={fadeAnim} />
          {el.label && <text x={midX} y={midY - 7} fill={color} fontSize={12} textAnchor="middle" style={labelStyle}>{el.label}</text>}
        </g>
      );
    }
    case 'rect': {
      const x = el.x || 0, y = el.y || 0, w = el.width || 100, h = el.height || 60;
      return (
        <g>
          <rect x={x} y={y} width={w} height={h} rx={6} fill="none" stroke={color} strokeWidth={sw} pathLength={100} style={strokeAnim} />
          {el.label && (
            <text x={x + w / 2} y={y + h / 2 + 5} fill={color} fontSize={Math.min(14, (w / Math.max(el.label.length, 1)) * 1.7)} textAnchor="middle" style={labelStyle}>
              {el.label}
            </text>
          )}
        </g>
      );
    }
    case 'circle': {
      const cx = el.x || 0, cy = el.y || 0, r = el.radius || 35;
      return (
        <g>
          <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw} pathLength={100} style={strokeAnim} />
          {el.label && <text x={cx} y={cy + 4} fill={color} fontSize={Math.min(13, r * 0.55)} textAnchor="middle" style={labelStyle}>{el.label}</text>}
        </g>
      );
    }
    case 'text': {
      return (
        <text x={el.x || 0} y={el.y || 0} fill={color} fontSize={el.fontSize || 15} style={labelStyle}>
          {el.text || el.label || ''}
        </text>
      );
    }
    default:
      return null;
  }
}

const LiveBoard = memo(LiveBoardInner);
export default LiveBoard;
