import { useEffect, useRef, useState, useCallback, memo } from 'react';
import 'katex/dist/katex.min.css';
import { renderMixedContent, renderDisplayMath, containsArabic } from './MathBoard';

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
  action: 'write' | 'draw' | 'erase' | 'pause' | 'narrate';
  line?: LiveLine;          // write
  elements?: LiveDrawElement[]; // draw
  zone?: 'text' | 'draw' | 'all'; // erase
  duration?: number;        // pause (ms)
  text?: string;            // narrate
}

export interface LiveScript {
  title?: string;
  steps: LiveStep[];
}

interface LiveBoardProps {
  script: LiveScript;
  isVisible: boolean;
  onClose?: () => void;
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

interface WrittenEntry { key: number; line: LiveLine; revealMs: number; stepNumber?: number }
interface DrawnEntry { key: number; el: LiveDrawElement; delayMs: number; drawMs: number }

function LiveBoardInner({ script, isVisible, onClose }: LiveBoardProps) {
  const [written, setWritten] = useState<WrittenEntry[]>([]);
  const [drawn, setDrawn] = useState<DrawnEntry[]>([]);
  const [narration, setNarration] = useState<string | null>(null);
  const [erasingZone, setErasingZone] = useState<'text' | 'draw' | 'all' | null>(null);
  const [playing, setPlaying] = useState(true);
  const [finished, setFinished] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [stepIndex, setStepIndex] = useState(0);

  const runIdRef = useRef(0);
  const playingRef = useRef(true);
  const speedRef = useRef(1);
  const keyRef = useRef(0);
  const textZoneRef = useRef<HTMLDivElement>(null);
  const stepCounterRef = useRef(0);

  playingRef.current = playing;
  speedRef.current = speed;

  const hasDrawSteps = Array.isArray(script?.steps) && script.steps.some(
    s => s?.action === 'draw' && Array.isArray(s.elements) && s.elements.length > 0
  );

  // Attente "consciente" : respecte pause + vitesse + annulation
  const wait = useCallback(async (ms: number, runId: number): Promise<boolean> => {
    let remaining = ms;
    while (remaining > 0) {
      await new Promise(r => setTimeout(r, 50));
      if (runId !== runIdRef.current) return false;
      if (playingRef.current) remaining -= 50 * speedRef.current;
    }
    return runId === runIdRef.current;
  }, []);

  // Moteur de lecture séquentielle du script
  const play = useCallback(async (steps: LiveStep[], runId: number) => {
    for (let i = 0; i < steps.length; i++) {
      if (runId !== runIdRef.current) return;
      const step = steps[i];
      if (!step || typeof step !== 'object') continue;
      setStepIndex(i);

      switch (step.action) {
        case 'write': {
          const line = step.line;
          if (!line || typeof line.content !== 'string') break;
          const revealMs = writeDuration(line.content) / speedRef.current;
          const isStep = (line.type || '') === 'step';
          if (isStep) stepCounterRef.current += 1;
          const entry: WrittenEntry = {
            key: ++keyRef.current,
            line,
            revealMs,
            stepNumber: isStep ? stepCounterRef.current : undefined,
          };
          setWritten(prev => [...prev, entry]);
          if (!(await wait(revealMs * speedRef.current + 300, runId))) return;
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
          if (!(await wait(els.length * DRAW_ELEMENT_STAGGER + DRAW_ELEMENT_MS, runId))) return;
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
            setNarration(step.text.trim());
            // 🔊 Point d'accroche audio : la narration sera lue en TTS ici.
            if (!(await wait(narrateDuration(step.text), runId))) return;
          }
          break;
        }
        default:
          break;
      }
    }
    if (runId === runIdRef.current) setFinished(true);
  }, [wait]);

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
    stepCounterRef.current = 0;
    if (script && Array.isArray(script.steps) && script.steps.length > 0) {
      play(script.steps, runId);
    }
    return () => { runIdRef.current += 1; };
  }, [script, play]);

  // Auto-scroll de la zone d'écriture
  useEffect(() => {
    const zone = textZoneRef.current;
    if (zone) zone.scrollTo({ top: zone.scrollHeight, behavior: 'smooth' });
  }, [written.length]);

  // ⏭ Aller à la fin : état final calculé d'un coup
  const skipToEnd = useCallback(() => {
    runIdRef.current += 1;
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
    setWritten([]);
    setDrawn([]);
    setNarration(null);
    setErasingZone(null);
    setFinished(false);
    setStepIndex(0);
    setPlaying(true);
    stepCounterRef.current = 0;
    if (script?.steps?.length) play(script.steps, runId);
  }, [script, play]);

  if (!isVisible || !script || !Array.isArray(script.steps) || script.steps.length === 0) return null;

  const totalSteps = script.steps.length;
  const eraseText = erasingZone === 'text' || erasingZone === 'all';
  const eraseDraw = erasingZone === 'draw' || erasingZone === 'all';

  return (
    <div className="w-full h-full flex flex-col rounded-2xl overflow-hidden shadow-lg" style={{ background: '#12241c' }}>
      <style>{`
        @keyframes liveReveal { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }
        @keyframes liveFadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
        @keyframes liveEraseWipe { from { opacity: 1; filter: blur(0); } to { opacity: 0; filter: blur(6px); } }
        @keyframes liveStroke { from { stroke-dashoffset: 100; } to { stroke-dashoffset: 0; } }
        @keyframes livePenPulse { 0%,100% { opacity: 1; } 50% { opacity: 0.25; } }
        .live-paused * { animation-play-state: paused !important; }

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

      {/* ── Barre d'outils ── */}
      <div className="shrink-0 flex items-center justify-between px-3 py-1.5" style={{ background: '#0d1b15', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
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
          {onClose && (
            <button onClick={onClose} className="text-white/40 hover:text-white/80 text-xs px-2 py-0.5 rounded hover:bg-white/10 transition-colors">
              ✕
            </button>
          )}
        </div>
      </div>

      {/* ── Corps : écriture à gauche, dessin à droite ── */}
      <div className={`flex-1 min-h-0 flex flex-col md:flex-row ${playing ? '' : 'live-paused'}`}>
        {/* Zone d'écriture */}
        <div
          ref={textZoneRef}
          className="flex-1 min-w-0 overflow-y-auto px-5 py-4"
          style={eraseText ? { animation: `liveEraseWipe ${ERASE_MS}ms ease-in forwards` } : undefined}
        >
          {written.map((entry, i) => (
            <LiveWrittenLine
              key={entry.key}
              entry={entry}
              isActive={!finished && i === written.length - 1 && erasingZone === null}
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

      {/* ── Narration du professeur (futur audio) ── */}
      {narration && (
        <div
          className="shrink-0 flex items-start gap-2 px-4 py-2.5"
          style={{ background: 'rgba(34,211,238,0.07)', borderTop: '1px solid rgba(34,211,238,0.2)', animation: 'liveFadeIn 0.3s ease-out both' }}
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

function LiveWrittenLine({ entry, isActive }: { entry: WrittenEntry; isActive: boolean }) {
  const { line, revealMs, stepNumber } = entry;
  const type = (line.type || 'text').toLowerCase();
  const color = chalk(line.color);
  const rtl = containsArabic(line.content);
  const reveal: React.CSSProperties = revealMs > 0
    ? { animation: `liveReveal ${revealMs}ms linear both`, display: 'inline-block', maxWidth: '100%' }
    : { display: 'inline-block', maxWidth: '100%' };

  if (type === 'separator') {
    return <hr className="my-3 border-white/15" style={{ animation: 'liveFadeIn 0.4s ease-out both' }} />;
  }

  const html = renderMixed(line.content);
  const pen = isActive && revealMs > 0 && (
    <span className="ml-1 text-sm align-middle" style={{ animation: 'livePenPulse 0.9s ease-in-out infinite' }}>✍️</span>
  );

  const base: React.CSSProperties = { fontFamily: "'Patrick Hand', 'Caveat', cursive", color };

  switch (type) {
    case 'title':
      return (
        <div className="mb-3 live-line" dir={rtl ? 'rtl' : 'ltr'}>
          <span style={{ ...base, ...reveal, color: chalk(line.color || 'yellow'), fontSize: 24, fontWeight: 700, borderBottom: `2px solid ${chalk(line.color || 'yellow')}55`, paddingBottom: 2 }}
            className="katex-dark" dangerouslySetInnerHTML={{ __html: html }} />
          {pen}
        </div>
      );
    case 'subtitle':
      return (
        <div className="mt-3 mb-2 live-line" dir={rtl ? 'rtl' : 'ltr'}>
          <span style={{ ...base, ...reveal, color: chalk(line.color || 'cyan'), fontSize: 19, fontWeight: 600 }}
            className="katex-dark" dangerouslySetInnerHTML={{ __html: html }} />
          {pen}
        </div>
      );
    case 'math':
      // renderDisplayMath route une formule pure vers KaTeX display, et une
      // ligne mixte (« Terme général : $u_n = …$ ») vers le rendu mixte —
      // sans quoi KaTeX échoue et réaffiche toute la phrase en rouge.
      return (
        <div className="my-2 live-line" style={{ textAlign: 'center' }}>
          <span style={{ ...reveal, fontSize: 17, color: chalk(line.color || 'white') }}
            className="katex-dark" dangerouslySetInnerHTML={{ __html: renderDisplayMath(line.content) }} />
          {pen}
        </div>
      );
    case 'step':
      return (
        <div className="my-1.5 flex items-start gap-2 live-line" dir={rtl ? 'rtl' : 'ltr'}>
          <span className="shrink-0 w-5 h-5 rounded-full text-[11px] font-bold flex items-center justify-center mt-0.5"
            style={{ background: `${chalk(line.color || 'blue')}33`, color: chalk(line.color || 'blue'), animation: 'liveFadeIn 0.3s ease-out both' }}>
            {stepNumber || '•'}
          </span>
          <span style={{ ...base, ...reveal, fontSize: 16 }} className="katex-dark" dangerouslySetInnerHTML={{ __html: html }} />
          {pen}
        </div>
      );
    case 'box':
      return (
        <div className="my-2 px-3 py-2 rounded-lg live-line" dir={rtl ? 'rtl' : 'ltr'}
          style={{ border: `1.5px solid ${chalk(line.color || 'green')}88`, background: `${chalk(line.color || 'green')}11`, animation: 'liveFadeIn 0.3s ease-out both' }}>
          <span style={{ ...base, ...reveal, fontSize: 16, color: chalk(line.color || 'green') }}
            className="katex-dark" dangerouslySetInnerHTML={{ __html: html }} />
          {pen}
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
          <span style={{ ...base, ...reveal, fontSize: 14.5, color: c }} className="katex-dark" dangerouslySetInnerHTML={{ __html: html }} />
          {pen}
        </div>
      );
    }
    default:
      return (
        <div className="my-1 live-line" dir={rtl ? 'rtl' : 'ltr'}>
          <span style={{ ...base, ...reveal, fontSize: 16 }} className="katex-dark" dangerouslySetInnerHTML={{ __html: html }} />
          {pen}
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
