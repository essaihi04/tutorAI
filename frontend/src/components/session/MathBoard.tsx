import { useEffect, useState, useRef, memo } from 'react';
import 'katex/dist/katex.min.css';
import katex from 'katex';
import MindMap from './MindMap';
import { printBoard, downloadAsPDF } from '../../utils/pdfExport';

interface MindMapNode {
  id: string;
  label: string;
  level: number;
  color?: string;
  children?: string[];
  parent?: string;
}

interface BoardLine {
  type: 'title' | 'subtitle' | 'text' | 'math' | 'step' | 'separator' | 'box' | 'note' | 'warning' | 'tip' | 'table' | 'graph' | 'diagram' | 'mindmap' | 'qcm' | 'vrai_faux' | 'association';
  content: string;
  color?: string;
  label?: string;
  // MindMap data
  mindmapNodes?: MindMapNode[];
  centerNode?: string;
  // Table data
  headers?: string[];
  rows?: string[][];
  // Graph data
  curves?: { label: string; fn?: string; points?: { x: number; y: number }[]; color?: string }[];
  xLabel?: string;
  yLabel?: string;
  xRange?: [number, number];
  yRange?: [number, number];
  // Diagram data
  nodes?: { id: string; label: string; x?: number; y?: number; color?: string }[];
  edges?: { from: string; to: string; label?: string }[];
  // Interactive exercise data
  choices?: string[];
  correct?: number | number[] | boolean;
  explanation?: string;
  // Vrai/Faux data
  statements?: { text: string; correct: boolean; explanation?: string }[];
  // Association data
  pairs?: { left: string; right: string }[];
}

interface MathBoardProps {
  lines: BoardLine[];
  title?: string;
  isVisible: boolean;
  onClose?: () => void;
}

// Dark chalkboard color palette — all colors bright for dark background
const BOARD_COLORS: Record<string, string> = {
  red: '#f87171',
  blue: '#60a5fa',
  green: '#4ade80',
  orange: '#fb923c',
  purple: '#c084fc',
  cyan: '#22d3ee',
  pink: '#f472b6',
  yellow: '#facc15',
  white: '#e2e8f0',
  black: '#e2e8f0',
};

// Default text color: chalk white on dark board
const DEFAULT_TEXT_COLOR = '#e2e8f0';

function resolveColor(c?: string): string {
  if (!c) return DEFAULT_TEXT_COLOR;
  return BOARD_COLORS[c] || c;
}

/** Check if a string looks like actual math (not just French text wrapped in $) */
function looksLikeMath(s: string): boolean {
  // If it contains common math operators/symbols, it's likely math
  if (/[\\{}^_=+\-*/÷×∑∫∏√∞≤≥≠∈∉⊂⊃∪∩]/.test(s)) return true;
  // Short single-letter variables are math: $x$, $n$, $f$
  if (/^[a-zA-Z]$/.test(s.trim())) return true;
  // Function-like: f(x), sin, cos, log, lim
  if (/^[a-zA-Z]+\s*\(/.test(s.trim())) return true;
  // Contains accented characters → likely French text, not math
  if (/[àâäéèêëïîôùûüçÀÂÄÉÈÊËÏÎÔÙÛÜÇ]/.test(s)) return false;
  // Multiple words with spaces and no math symbols → probably text
  if (s.trim().split(/\s+/).length > 3 && !/[\\{}^_=]/.test(s)) return false;
  return true;
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/** True if the string contains Arabic/Darija characters.
 * Used to apply dir="rtl" so the Unicode BiDi algorithm orders
 * mixed Arabic + embedded Latin tokens (e.g. "la mécanique") correctly.
 */
function containsArabic(s: string): boolean {
  if (!s) return false;
  // Arabic block (U+0600–U+06FF) + Arabic Supplement + Presentation Forms
  return /[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]/.test(s);
}

/** Render a string that may contain inline LaTeX ($...$, \(...\)) mixed with plain text */
function renderMixedContent(text: string): string {
  if (!text || typeof text !== 'string') return '';
  
  // Strip leftover markdown bold/italic markers
  let cleaned = text.replace(/\*\*(.+?)\*\*/g, '$1').replace(/__(.+?)__/g, '$1');
  
  // First convert \(...\) to $...$ and \[...\] to $$...$$ for uniform handling
  cleaned = cleaned.replace(/\\\((.+?)\\\)/g, (_, m) => `$${m}$`);
  cleaned = cleaned.replace(/\\\[(.+?)\\\]/g, (_, m) => `$$${m}$$`);

  // Auto-wrap bare LaTeX commands (no $ delimiters around them).
  // Critical for genetics boards where the LLM emits cells like
  //   "\dfrac{L}{L} [L]"  or  "\dfrac{g+}{}\,\dfrac{vg}{vg}\;[g+,vg]"
  // without any $...$ wrappers. Without this, the backslashes are
  // HTML-escaped and the user sees raw "\dfrac{L}{L}" as text.
  if (!/\$/.test(cleaned)) {
    // List of common LaTeX commands the LLM emits in board cells.
    const LATEX_CMD_RE = /\\(?:d?frac|tfrac|cfrac|sqrt|text|mathrm|mathbb|mathbf|sum|prod|int|left|right|cdot|times|to|leftarrow|rightarrow|alpha|beta|gamma|delta|sigma|theta|phi|pi|lambda|mu|;|,|:|!|quad|qquad)\b/;
    if (LATEX_CMD_RE.test(cleaned)) {
      // Wrap the whole cell as inline LaTeX. Plain text fragments
      // like "[L]" still render correctly inside KaTeX text mode.
      cleaned = `$${cleaned}$`;
    }
  }

  // Split on $$...$$ (display) and $...$ (inline) patterns
  const parts = cleaned.split(/(\$\$[^$]+\$\$|\$[^$]+\$)/g);
  return parts.map(part => {
    if (part.startsWith('$$') && part.endsWith('$$')) {
      const latex = part.slice(2, -2);
      try {
        return katex.renderToString(latex, { throwOnError: false, displayMode: true, strict: 'ignore' });
      } catch (e) {
        return `<code style="color:#facc15">${escapeHtml(latex)}</code>`;
      }
    }
    if (part.startsWith('$') && part.endsWith('$')) {
      const latex = part.slice(1, -1);
      if (!looksLikeMath(latex)) {
        // Not actual math — render as plain styled text
        return `<em>${escapeHtml(latex)}</em>`;
      }
      try {
        return katex.renderToString(latex, { throwOnError: false, displayMode: false, strict: 'ignore' });
      } catch (e) {
        return `<code style="color:#facc15">${escapeHtml(latex)}</code>`;
      }
    }
    return escapeHtml(part);
  }).join('');
}

/** Render display-mode LaTeX ($$...$$).
 *
 * Defensive routing: when the LLM emits a line of type='math' that actually
 * contains French descriptive text mixed with a formula
 * (e.g. "Terme général : $u_n = u_0 + (n-1) r$"), passing the whole string
 * to KaTeX makes it bail out and re-render the text in red (its native
 * "throwOnError:false" failure styling). To avoid that, we detect mixed
 * content (accents, $...$ delimiters, or several spaced words) and route
 * it through renderMixedContent, which handles plain text + inline math
 * correctly.
 */
function renderDisplayMath(latex: string): string {
  if (!latex || typeof latex !== 'string') return '';

  let clean = latex.trim();

  // Detect "this is not a pure LaTeX expression":
  //   - has French accented letters, OR
  //   - contains inline-math delimiters $...$ or \(...\), OR
  //   - has many spaced words AND no LaTeX backslash command at all.
  const hasAccents = /[àâäéèêëïîôùûüçÀÂÄÉÈÊËÏÎÔÙÛÜÇ]/.test(clean);
  // Inline $…$ that isn't the wrapping $$…$$ of a pure formula.
  const inner = clean.replace(/^\$\$|\$\$$/g, '');
  const hasInlineDelims = /\$[^$\n]+\$/.test(inner) || /\\\([^\n]+?\\\)/.test(inner);
  const wordCount = clean.split(/\s+/).filter(Boolean).length;
  const hasBackslashCmd = /\\[a-zA-Z]+/.test(clean);
  const looksLikeProse = wordCount > 4 && !hasBackslashCmd;

  if (hasAccents || hasInlineDelims || looksLikeProse) {
    // Render as a display-styled mixed-content block instead of a single formula.
    return `<div class="my-1">${renderMixedContent(clean)}</div>`;
  }

  // Strip $$ or single $ wrappers if present (defensive).
  if (clean.startsWith('$$') && clean.endsWith('$$')) {
    clean = clean.slice(2, -2).trim();
  } else if (clean.startsWith('$') && clean.endsWith('$') && clean.length > 2) {
    clean = clean.slice(1, -1).trim();
  }

  try {
    return katex.renderToString(clean, { throwOnError: false, displayMode: true, strict: 'ignore' });
  } catch (e) {
    console.error('[MathBoard] KaTeX display render error:', e);
    return `<pre style="color:#f87171">${escapeHtml(clean)}</pre>`;
  }
}

function MathBoardInner({ lines, title, isVisible, onClose }: MathBoardProps) {
  const [visibleCount, setVisibleCount] = useState(0);
  const [animating, setAnimating] = useState(true);
  const containerRef = useRef<HTMLDivElement>(null);
  const timersRef = useRef<ReturnType<typeof setTimeout>[]>([]);

  // Animate lines appearing one by one
  useEffect(() => {
    timersRef.current.forEach(clearTimeout);
    timersRef.current = [];
    setVisibleCount(0);
    setAnimating(true);

    if (!lines || lines.length === 0) return;

    lines.forEach((_, i) => {
      const delay = (i + 1) * 350;
      const t = setTimeout(() => {
        setVisibleCount(i + 1);
      }, delay);
      timersRef.current.push(t);
    });

    const doneT = setTimeout(() => setAnimating(false), lines.length * 350 + 200);
    timersRef.current.push(doneT);

    return () => {
      timersRef.current.forEach(clearTimeout);
      timersRef.current = [];
    };
  }, [lines]);

  // Auto-scroll to bottom as new lines appear
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [visibleCount]);

  if (!isVisible || !lines || !Array.isArray(lines) || lines.length === 0) {
    return null;
  }

  const visibleLines = lines.slice(0, visibleCount);

  return (
    <div className="w-full h-full flex flex-col rounded-2xl overflow-hidden shadow-lg" style={{ background: '#1a2e1a' }}>
      {/* Toolbar — dark chalkboard frame */}
      <div className="shrink-0 flex items-center justify-between px-4 py-2" style={{ background: '#122412', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <div className="w-2 h-2 rounded-full bg-red-500" />
            <div className="w-2 h-2 rounded-full bg-yellow-500" />
            <div className="w-2 h-2 rounded-full bg-green-500" />
          </div>
          <span className="text-white/70 text-xs font-medium flex items-center gap-1.5">
            <span>Tableau</span>
            {animating && (
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
            )}
          </span>
          {title && (
            <span className="text-cyan-300 text-xs font-semibold truncate max-w-[50vw]">
              — {title}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {/* Print button */}
          <button
            onClick={() => printBoard(lines, title)}
            className="text-[10px] px-2 py-1 rounded font-medium transition-colors flex items-center gap-1"
            style={{ background: 'rgba(34,211,238,0.15)', color: '#22d3ee' }}
            title="Imprimer"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="6 9 6 2 18 2 18 9"></polyline>
              <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
              <rect x="6" y="14" width="12" height="8"></rect>
            </svg>
            <span>Imprimer</span>
          </button>
          
          {/* PDF download button */}
          <button
            onClick={() => downloadAsPDF(lines, title)}
            className="text-[10px] px-2 py-1 rounded font-medium transition-colors flex items-center gap-1"
            style={{ background: 'rgba(34,211,238,0.15)', color: '#22d3ee' }}
            title="Télécharger PDF"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            <span>PDF</span>
          </button>
          
          {animating && (
            <button
              onClick={() => {
                timersRef.current.forEach(clearTimeout);
                setVisibleCount(lines.length);
                setAnimating(false);
              }}
              className="text-[10px] px-2 py-0.5 rounded font-medium transition-colors"
              style={{ background: 'rgba(34,211,238,0.15)', color: '#22d3ee' }}
            >
              Tout afficher
            </button>
          )}
          {onClose && (
            <button
              onClick={onClose}
              className="text-white/40 hover:text-white/80 text-xs px-2 py-0.5 rounded hover:bg-white/5 transition-colors"
            >
              Fermer
            </button>
          )}
        </div>
      </div>

      {/* Board content — dark green chalkboard */}
      <div
        ref={containerRef}
        className="flex-1 min-h-0 overflow-y-auto px-6 py-5"
        style={{
          fontFamily: "'Caveat', 'Patrick Hand', 'Segoe UI', system-ui, sans-serif",
          background: 'linear-gradient(135deg, #1a3a2a 0%, #1e3320 40%, #1a2e1a 100%)',
        }}
      >
        {/* Subtle chalk dust texture */}
        <div
          className="absolute inset-0 pointer-events-none opacity-[0.03]"
          style={{
            backgroundImage: 'linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />

        <div className="relative space-y-3">
          {visibleLines.map((line, i) => (
            <div
              key={i}
              className="animate-[fadeSlideIn_0.3s_ease-out]"
              style={{ animationFillMode: 'both' }}
            >
              {renderLine(line)}
            </div>
          ))}

          {/* Writing cursor — chalk-like */}
          {animating && (
            <div className="flex items-center gap-1 mt-2 opacity-60">
              <div className="w-0.5 h-5 bg-white animate-pulse rounded-full" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
// TABLE — Animated grid table with headers and rows
// ═══════════════════════════════════════════════════════════
function AnimatedTable({ line }: { line: BoardLine }) {
  const headers = line.headers || [];
  const rows = line.rows || [];
  const [visibleRows, setVisibleRows] = useState(0);
  const timersRef = useRef<ReturnType<typeof setTimeout>[]>([]);

  useEffect(() => {
    timersRef.current.forEach(clearTimeout);
    timersRef.current = [];
    setVisibleRows(0);
    // Show header immediately, then rows one by one
    const totalRows = rows.length;
    for (let i = 0; i <= totalRows; i++) {
      const t = setTimeout(() => setVisibleRows(i + 1), i * 280);
      timersRef.current.push(t);
    }
    return () => timersRef.current.forEach(clearTimeout);
  }, [rows.length]);

  if (headers.length === 0 && rows.length === 0) return null;

  return (
    <div className="my-3 overflow-x-auto rounded-lg" style={{ border: '1px solid rgba(255,255,255,0.15)' }}>
      {line.content && (
        <div className="px-3 py-1.5 text-sm font-semibold" style={{ color: '#22d3ee', fontFamily: "'Patrick Hand', cursive", borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
          {line.content}
        </div>
      )}
      <table className="w-full text-sm" style={{ fontFamily: "'Patrick Hand', 'Caveat', cursive", borderCollapse: 'collapse' }}>
        {headers.length > 0 && (
          <thead>
            <tr style={{ background: 'rgba(255,255,255,0.08)' }}>
              {headers.map((h, i) => (
                <th
                  key={i}
                  className="px-3 py-2 text-left font-bold"
                  style={{
                    color: '#60a5fa',
                    borderBottom: '2px solid rgba(96,165,250,0.3)',
                    borderRight: i < headers.length - 1 ? '1px solid rgba(255,255,255,0.08)' : 'none',
                    fontSize: '1rem',
                  }}
                  dangerouslySetInnerHTML={{ __html: renderMixedContent(h) }}
                />
              ))}
            </tr>
          </thead>
        )}
        <tbody>
          {rows.slice(0, Math.max(0, visibleRows - 1)).map((row, ri) => {
            // Defensive: ensure row is an array
            const rowArray = Array.isArray(row) ? row : (typeof row === 'object' && row ? Object.values(row) : [String(row)]);
            return (
              <tr
                key={ri}
                className="animate-[fadeSlideIn_0.3s_ease-out]"
                style={{
                  background: ri % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'rgba(255,255,255,0.05)',
                  animationFillMode: 'both',
                }}
              >
                {rowArray.map((cell, ci) => (
                  <td
                    key={ci}
                    className="px-3 py-1.5"
                    style={{
                      color: ci === 0 ? '#4ade80' : '#e2e8f0',
                      borderBottom: '1px solid rgba(255,255,255,0.06)',
                      borderRight: ci < rowArray.length - 1 ? '1px solid rgba(255,255,255,0.06)' : 'none',
                      fontSize: '0.95rem',
                    }}
                    dangerouslySetInnerHTML={{ __html: renderMixedContent(String(cell ?? '')) }}
                  />
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
// GRAPH — Animated SVG curve drawing (functions, data plots)
// ═══════════════════════════════════════════════════════════
function AnimatedGraph({ line }: { line: BoardLine }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [progress, setProgress] = useState(0);
  const frameRef = useRef<number>(0);

  const curves = line.curves || [];
  const xRange = line.xRange || [-5, 5];
  const yRange = line.yRange || [-5, 5];
  const xLabel = line.xLabel || 'x';
  const yLabel = line.yLabel || 'y';

  // Canvas dimensions
  const W = 480, H = 300;
  const pad = { top: 25, right: 20, bottom: 35, left: 45 };
  const plotW = W - pad.left - pad.right;
  const plotH = H - pad.top - pad.bottom;

  const toSvgX = (x: number) => pad.left + ((x - xRange[0]) / (xRange[1] - xRange[0])) * plotW;
  const toSvgY = (y: number) => pad.top + plotH - ((y - yRange[0]) / (yRange[1] - yRange[0])) * plotH;

  // Animate progress from 0 to 1
  useEffect(() => {
    setProgress(0);
    let start: number | null = null;
    const duration = 1800; // ms
    const step = (ts: number) => {
      if (!start) start = ts;
      const p = Math.min(1, (ts - start) / duration);
      setProgress(p);
      if (p < 1) frameRef.current = requestAnimationFrame(step);
    };
    frameRef.current = requestAnimationFrame(step);
    return () => cancelAnimationFrame(frameRef.current);
  }, [curves.length]);

  // Evaluate a math function string safely
  const evalFn = (fnStr: string, x: number): number | null => {
    try {
      const safeExpr = fnStr
        .replace(/\bsin\b/g, 'Math.sin')
        .replace(/\bcos\b/g, 'Math.cos')
        .replace(/\btan\b/g, 'Math.tan')
        .replace(/\babs\b/g, 'Math.abs')
        .replace(/\bsqrt\b/g, 'Math.sqrt')
        .replace(/\bln\b/g, 'Math.log')
        .replace(/\blog\b/g, 'Math.log10')
        .replace(/\bexp\b/g, 'Math.exp')
        .replace(/\bpi\b/gi, 'Math.PI')
        .replace(/\^/g, '**');
      const result = new Function('x', `"use strict"; return (${safeExpr})`)(x);
      return typeof result === 'number' && isFinite(result) ? result : null;
    } catch {
      return null;
    }
  };

  // Build path for a curve
  const buildPath = (curve: typeof curves[0], pct: number): string => {
    const pts: { x: number; y: number }[] = [];
    if (curve.points && curve.points.length > 0) {
      // Use explicit points
      curve.points.forEach(p => pts.push(p));
    } else if (curve.fn) {
      // Evaluate function
      const steps = 200;
      for (let i = 0; i <= steps; i++) {
        const x = xRange[0] + (i / steps) * (xRange[1] - xRange[0]);
        const y = evalFn(curve.fn, x);
        if (y !== null) pts.push({ x, y });
      }
    }
    if (pts.length === 0) return '';
    const visibleCount = Math.max(1, Math.floor(pts.length * pct));
    const visible = pts.slice(0, visibleCount);
    return visible.map((p, i) => {
      const sx = toSvgX(p.x);
      const sy = toSvgY(p.y);
      // Clamp to plot area
      const cx = Math.max(pad.left, Math.min(W - pad.right, sx));
      const cy = Math.max(pad.top, Math.min(H - pad.bottom, sy));
      return (i === 0 ? 'M' : 'L') + cx.toFixed(1) + ',' + cy.toFixed(1);
    }).join(' ');
  };

  const curveColors = ['#60a5fa', '#f87171', '#4ade80', '#fb923c', '#c084fc', '#22d3ee'];

  if (curves.length === 0) return null;

  // Grid lines
  const gridLinesX: number[] = [];
  const gridLinesY: number[] = [];
  for (let x = Math.ceil(xRange[0]); x <= Math.floor(xRange[1]); x++) gridLinesX.push(x);
  for (let y = Math.ceil(yRange[0]); y <= Math.floor(yRange[1]); y++) gridLinesY.push(y);

  return (
    <div className="my-3 rounded-lg overflow-hidden" style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(255,255,255,0.1)' }}>
      {line.content && (
        <div className="px-3 py-1.5 text-sm font-semibold" style={{ color: '#22d3ee', fontFamily: "'Patrick Hand', cursive", borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
          {line.content}
        </div>
      )}
      <svg ref={svgRef} viewBox={`0 0 ${W} ${H}`} className="w-full" style={{ maxHeight: 320 }}>
        {/* Background */}
        <rect x={pad.left} y={pad.top} width={plotW} height={plotH} fill="rgba(10,15,30,0.6)" rx="4" />

        {/* Grid */}
        {gridLinesX.map(x => (
          <line key={`gx${x}`} x1={toSvgX(x)} y1={pad.top} x2={toSvgX(x)} y2={pad.top + plotH} stroke="rgba(255,255,255,0.08)" strokeWidth="0.5" />
        ))}
        {gridLinesY.map(y => (
          <line key={`gy${y}`} x1={pad.left} y1={toSvgY(y)} x2={pad.left + plotW} y2={toSvgY(y)} stroke="rgba(255,255,255,0.08)" strokeWidth="0.5" />
        ))}

        {/* Axes */}
        {yRange[0] <= 0 && yRange[1] >= 0 && (
          <line x1={pad.left} y1={toSvgY(0)} x2={W - pad.right} y2={toSvgY(0)} stroke="rgba(255,255,255,0.3)" strokeWidth="1" />
        )}
        {xRange[0] <= 0 && xRange[1] >= 0 && (
          <line x1={toSvgX(0)} y1={pad.top} x2={toSvgX(0)} y2={pad.top + plotH} stroke="rgba(255,255,255,0.3)" strokeWidth="1" />
        )}

        {/* Axis labels */}
        <text x={W - pad.right + 5} y={toSvgY(0) + 4} fill="rgba(255,255,255,0.5)" fontSize="11" fontFamily="'Patrick Hand', cursive">{xLabel}</text>
        <text x={toSvgX(0) - 5} y={pad.top - 5} fill="rgba(255,255,255,0.5)" fontSize="11" fontFamily="'Patrick Hand', cursive" textAnchor="end">{yLabel}</text>

        {/* Tick labels */}
        {gridLinesX.filter(x => x !== 0).map(x => (
          <text key={`lx${x}`} x={toSvgX(x)} y={pad.top + plotH + 15} fill="rgba(255,255,255,0.4)" fontSize="9" textAnchor="middle" fontFamily="system-ui">{x}</text>
        ))}
        {gridLinesY.filter(y => y !== 0).map(y => (
          <text key={`ly${y}`} x={pad.left - 8} y={toSvgY(y) + 3} fill="rgba(255,255,255,0.4)" fontSize="9" textAnchor="end" fontFamily="system-ui">{y}</text>
        ))}

        {/* Curves */}
        {curves.map((curve, i) => {
          const path = buildPath(curve, progress);
          const color = curve.color ? (BOARD_COLORS[curve.color] || curve.color) : curveColors[i % curveColors.length];
          return path ? (
            <g key={i}>
              <path d={path} fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
              {progress >= 1 && curve.label && (
                <text x={W - pad.right - 10} y={pad.top + 16 + i * 16} fill={color} fontSize="11" textAnchor="end" fontFamily="'Patrick Hand', cursive" fontWeight="600">
                  {curve.label}
                </text>
              )}
            </g>
          ) : null;
        })}
      </svg>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
// DIAGRAM — Enhanced Mind Map / Carte Mentale with diverse shapes
// ═══════════════════════════════════════════════════════════
function AnimatedDiagram({ line }: { line: BoardLine }) {
  const nodes = line.nodes || [];
  const edges = line.edges || [];
  const [visibleCount, setVisibleCount] = useState(0);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const timersRef = useRef<ReturnType<typeof setTimeout>[]>([]);

  // Branch colors for diverse coloring
  const branchColors = [
    { main: '#3b82f6', light: '#93c5fd', dark: '#1d4ed8' }, // Blue
    { main: '#10b981', light: '#6ee7b7', dark: '#047857' }, // Green
    { main: '#f59e0b', light: '#fcd34d', dark: '#b45309' }, // Amber
    { main: '#8b5cf6', light: '#c4b5fd', dark: '#6d28d9' }, // Purple
    { main: '#ef4444', light: '#fca5a5', dark: '#b91c1c' }, // Red
    { main: '#06b6d4', light: '#67e8f9', dark: '#0e7490' }, // Cyan
  ];

  useEffect(() => {
    timersRef.current.forEach(clearTimeout);
    timersRef.current = [];
    setVisibleCount(0);
    const total = nodes.length + edges.length;
    for (let i = 0; i <= total; i++) {
      const t = setTimeout(() => setVisibleCount(i + 1), i * 180);
      timersRef.current.push(t);
    }
    return () => timersRef.current.forEach(clearTimeout);
  }, [nodes.length, edges.length]);

  if (nodes.length === 0) {
    return <p className="text-yellow-400 text-sm">Carte mentale en cours de chargement...</p>;
  }

  // Detect if this is a mind map (has a "centre" or "center" node)
  const centerNode = nodes.find(n => 
    n.id === 'centre' || n.id === 'center' || n.id === 'central' || 
    n.label?.toLowerCase().includes('limite') || nodes.indexOf(n) === 0
  );
  const isMindMap = centerNode && nodes.length > 1;

  // Mind Map Layout - Radial with 3 levels max
  const W = 650, H = 480;
  const centerX = W / 2;
  const centerY = H / 2;

  // Level colors for mind map
  const levelColors = ['#60a5fa', '#4ade80', '#f472b6', '#facc15', '#c084fc', '#fb923c'];

  // Get shape based on level
  const getShape = (level: number): 'circle' | 'rounded' | 'diamond' | 'pill' => {
    switch (level) {
      case 0: return 'circle';
      case 1: return 'rounded';
      case 2: return 'diamond';
      default: return 'pill';
    }
  };

  // Get dimensions based on level
  const getDims = (level: number) => {
    switch (level) {
      case 0: return { w: 110, h: 55, r: 55 };
      case 1: return { w: 100, h: 42, r: 10 };
      case 2: return { w: 85, h: 38, r: 6 };
      default: return { w: 75, h: 30, r: 15 };
    }
  };

  // Calculate radial positions for mind map with multiple levels
  const getRadialLayout = () => {
    if (!isMindMap) return null;

    const positioned: { [id: string]: { x: number; y: number; level: number; branchIndex: number } } = {};
    
    // Center node
    if (centerNode) {
      positioned[centerNode.id] = { x: centerX, y: centerY, level: 0, branchIndex: -1 };
    }

    // Find level 1 nodes (main branches)
    const level1Nodes = nodes.filter(n => n.id !== centerNode?.id);
    const branchCount = Math.min(level1Nodes.length, 6);
    const angleStep = (2 * Math.PI) / Math.max(branchCount, 1);
    const radius1 = 150;

    level1Nodes.forEach((node, i) => {
      const angle = i * angleStep - Math.PI / 2;
      positioned[node.id] = {
        x: centerX + radius1 * Math.cos(angle),
        y: centerY + radius1 * Math.sin(angle),
        level: 1,
        branchIndex: i
      };
    });

    return positioned;
  };

  const radialPositions = isMindMap ? getRadialLayout() : null;

  // Fallback to vertical flow layout
  const hasPositions = nodes.some(n => n.x !== undefined && n.y !== undefined);
  const layoutNodes = radialPositions 
    ? nodes.map(n => ({
        ...n,
        x: radialPositions[n.id]?.x || centerX,
        y: radialPositions[n.id]?.y || centerY,
        level: radialPositions[n.id]?.level || 0,
        branchIndex: radialPositions[n.id]?.branchIndex ?? 0
      }))
    : nodes.map((n, i) => ({
        ...n,
        x: hasPositions ? (n.x || 0) : 160,
        y: hasPositions ? (n.y || 0) : 40 + i * 80,
        level: 0,
        branchIndex: i
      }));

  const nodeW = isMindMap ? 100 : 140;
  const nodeH = isMindMap ? 40 : 36;
  const totalH = isMindMap ? H : (hasPositions
    ? Math.max(...layoutNodes.map(n => n.y + nodeH + 20), 200)
    : nodes.length * 80 + 40);
  const totalW = isMindMap ? W : 320;

  const getNodeCenter = (id: string) => {
    const n = layoutNodes.find(n => n.id === id);
    if (!n) return { x: totalW / 2, y: 20 };
    return { x: n.x, y: n.y };
  };

  // Render different shapes
  const renderShape = (
    shape: string, 
    x: number, 
    y: number, 
    dims: { w: number; h: number; r: number },
    branchIndex: number,
    isHovered: boolean,
    isSelected: boolean
  ) => {
    const branchColor = branchColors[Math.abs(branchIndex) % branchColors.length];
    const fillId = branchIndex === -1 ? 'center-grad' : `branch-grad-${branchIndex % branchColors.length}`;
    
    const baseStyle: React.CSSProperties = {
      filter: isHovered || isSelected ? 'url(#glow-strong)' : 'url(#glow-effect)',
      transition: 'all 0.25s ease',
      transform: isHovered ? 'scale(1.08)' : 'scale(1)',
      transformOrigin: `${x}px ${y}px`,
    };

    switch (shape) {
      case 'circle':
        return (
          <circle
            cx={x} cy={y} r={dims.r}
            fill={`url(#${fillId})`}
            stroke={branchIndex === -1 ? '#60a5fa' : branchColor.main}
            strokeWidth={isSelected ? 3.5 : 2.5}
            style={baseStyle}
          />
        );
      
      case 'rounded':
        return (
          <rect
            x={x - dims.w / 2} y={y - dims.h / 2}
            width={dims.w} height={dims.h} rx={dims.r}
            fill={`url(#${fillId})`}
            stroke={branchColor.main}
            strokeWidth={isSelected ? 3 : 2}
            style={baseStyle}
          />
        );
      
      case 'diamond':
        const dPoints = [
          `${x},${y - dims.h / 2 - 2}`,
          `${x + dims.w / 2 + 2},${y}`,
          `${x},${y + dims.h / 2 + 2}`,
          `${x - dims.w / 2 - 2},${y}`,
        ].join(' ');
        return (
          <polygon
            points={dPoints}
            fill={`url(#${fillId})`}
            stroke={branchColor.main}
            strokeWidth={isSelected ? 3 : 2}
            style={baseStyle}
          />
        );
      
      case 'pill':
      default:
        return (
          <rect
            x={x - dims.w / 2} y={y - dims.h / 2}
            width={dims.w} height={dims.h} rx={dims.h / 2}
            fill={`url(#${fillId})`}
            stroke={branchColor.main}
            strokeWidth={isSelected ? 2.5 : 1.5}
            style={baseStyle}
          />
        );
    }
  };

  return (
    <div className="my-3 rounded-xl overflow-hidden" style={{ background: 'linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.95))', border: '1px solid rgba(255,255,255,0.15)' }}>
      {/* Title bar */}
      <div className="px-4 py-2.5 flex items-center justify-between" style={{ background: 'rgba(0,0,0,0.3)', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        <div className="flex items-center gap-2">
          <span className="text-lg">🧠</span>
          <span className="text-sm font-semibold" style={{ color: '#22d3ee', fontFamily: "'Patrick Hand', cursive" }}>
            {line.content || 'Carte Mentale'}
          </span>
        </div>
        {selectedNode && (
          <div className="flex items-center gap-2 text-xs text-cyan-400">
            <span>📌 {layoutNodes.find(n => n.id === selectedNode)?.label}</span>
            <button onClick={() => setSelectedNode(null)} className="text-slate-500 hover:text-white">✕</button>
          </div>
        )}
      </div>
      
      <svg viewBox={`0 0 ${totalW} ${totalH}`} className="w-full" style={{ maxHeight: 520, minHeight: 320 }}>
        {/* Gradient definitions */}
        <defs>
          {/* Center gradient */}
          <radialGradient id="center-grad">
            <stop offset="0%" stopColor="#60a5fa" stopOpacity="0.95" />
            <stop offset="70%" stopColor="#3b82f6" stopOpacity="0.85" />
            <stop offset="100%" stopColor="#1d4ed8" stopOpacity="0.7" />
          </radialGradient>
          
          {/* Branch gradients */}
          {branchColors.map((colors, i) => (
            <linearGradient key={`branch-grad-${i}`} id={`branch-grad-${i}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={colors.light} stopOpacity="0.9" />
              <stop offset="50%" stopColor={colors.main} stopOpacity="0.85" />
              <stop offset="100%" stopColor={colors.dark} stopOpacity="0.75" />
            </linearGradient>
          ))}
          
          {levelColors.map((color, i) => (
            <radialGradient key={`grad-${i}`} id={`node-grad-${i}`}>
              <stop offset="0%" stopColor={color} stopOpacity="0.9" />
              <stop offset="100%" stopColor={color} stopOpacity="0.5" />
            </radialGradient>
          ))}
          
          <filter id="glow-effect">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
          <filter id="glow-strong">
            <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        {/* Draw connections for mind map with curved paths */}
        {isMindMap && layoutNodes.slice(1, visibleCount).map((node, i) => {
          const center = getNodeCenter(centerNode?.id || '');
          const nodePos = getNodeCenter(node.id);
          const branchColor = branchColors[node.branchIndex % branchColors.length];
          const isHighlighted = hoveredNode === node.id || selectedNode === node.id;
          
          // Calculate control point for curved path
          const midX = (center.x + nodePos.x) / 2;
          const midY = (center.y + nodePos.y) / 2;
          const dx = nodePos.x - center.x;
          const dy = nodePos.y - center.y;
          const perpX = -dy * 0.12;
          const perpY = dx * 0.12;
          
          return (
            <path
              key={`conn-${i}`}
              d={`M ${center.x} ${center.y} Q ${midX + perpX} ${midY + perpY} ${nodePos.x} ${nodePos.y}`}
              stroke={branchColor.main}
              strokeWidth={isHighlighted ? 3 : 2}
              fill="none"
              opacity={isHighlighted ? 0.8 : 0.45}
              className="transition-all duration-300"
              style={{ animation: `drawLine 0.4s ease-out ${i * 0.1}s both` }}
            />
          );
        })}

        {/* Draw edges for flow diagrams */}
        {!isMindMap && edges.slice(0, Math.max(0, visibleCount - nodes.length)).map((edge, i) => {
          const from = getNodeCenter(edge.from);
          const to = getNodeCenter(edge.to);
          const dx = to.x - from.x;
          const dy = to.y - from.y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;
          const sx = from.x + (dx / dist) * (nodeH / 2 + 2);
          const sy = from.y + (dy / dist) * (nodeH / 2 + 2);
          const ex = to.x - (dx / dist) * (nodeH / 2 + 6);
          const ey = to.y - (dy / dist) * (nodeH / 2 + 6);
          return (
            <g key={`e${i}`} className="animate-[fadeSlideIn_0.3s_ease-out]" style={{ animationFillMode: 'both' }}>
              <defs>
                <marker id={`ah${i}`} markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
                  <path d="M0,0 L8,3 L0,6 Z" fill="rgba(255,255,255,0.6)" />
                </marker>
              </defs>
              <line x1={sx} y1={sy} x2={ex} y2={ey} stroke="rgba(255,255,255,0.4)" strokeWidth="1.5" markerEnd={`url(#ah${i})`} />
              {edge.label && (
                <text x={(sx + ex) / 2 + 8} y={(sy + ey) / 2 - 4} fill="rgba(255,255,255,0.5)" fontSize="9" fontFamily="'Patrick Hand', cursive">{edge.label}</text>
              )}
            </g>
          );
        })}

        {/* Nodes with diverse shapes */}
        {layoutNodes.slice(0, Math.min(visibleCount, nodes.length)).map((node, i) => {
          const isCenter = isMindMap && node.id === centerNode?.id;
          const level = node.level || 0;
          const shape = getShape(level);
          const dims = getDims(level);
          const isHovered = hoveredNode === node.id;
          const isSelected = selectedNode === node.id;
          const fontSize = isCenter ? 13 : level === 1 ? 11 : 10;
          
          return (
            <g 
              key={node.id} 
              className="cursor-pointer"
              onMouseEnter={() => setHoveredNode(node.id)}
              onMouseLeave={() => setHoveredNode(null)}
              onClick={() => setSelectedNode(selectedNode === node.id ? null : node.id)}
              style={{ 
                animation: `nodeAppear 0.35s ease-out ${i * 0.1}s both`,
              }}
            >
              {isMindMap ? (
                <>
                  {renderShape(shape, node.x, node.y, dims, isCenter ? -1 : node.branchIndex, isHovered, isSelected)}
                  <text
                    x={node.x}
                    y={node.y}
                    fill="#fff"
                    fontSize={fontSize}
                    fontWeight={isCenter ? 'bold' : '600'}
                    textAnchor="middle"
                    dominantBaseline="middle"
                    fontFamily="'Patrick Hand', cursive"
                    style={{ textShadow: '0 1px 3px rgba(0,0,0,0.5)', pointerEvents: 'none' }}
                  >
                    {(node.label || '').split('\\n').map((line, li) => (
                      <tspan key={li} x={node.x} dy={li === 0 ? 0 : 13}>{line}</tspan>
                    ))}
                  </text>
                </>
              ) : (
                // Rectangular nodes for flow diagrams
                <>
                  <rect
                    x={node.x - nodeW/2} y={node.y - nodeH/2} width={nodeW} height={nodeH} rx="8"
                    fill="rgba(0,0,0,0.4)" 
                    stroke={branchColors[i % branchColors.length].main} 
                    strokeWidth={isSelected ? 2.5 : 1.5}
                    style={{ filter: isHovered ? 'url(#glow-strong)' : 'url(#glow-effect)' }}
                  />
                  <text
                    x={node.x} y={node.y + 1}
                    fill={branchColors[i % branchColors.length].light} 
                    fontSize="12" fontWeight="600" textAnchor="middle" dominantBaseline="middle"
                    fontFamily="'Patrick Hand', cursive"
                  >
                    {node.label}
                  </text>
                </>
              )}
            </g>
          );
        })}
      </svg>
      
      {/* Interactive legend */}
      <div className="px-4 py-2 flex items-center justify-between" style={{ background: 'rgba(0,0,0,0.25)', borderTop: '1px solid rgba(255,255,255,0.08)' }}>
        <div className="flex items-center gap-4 text-xs" style={{ color: 'rgba(255,255,255,0.5)' }}>
          <div className="flex items-center gap-1.5">
            <div className="w-4 h-4 rounded-full" style={{ background: '#60a5fa' }} />
            <span>Central</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-4 h-3 rounded" style={{ background: '#10b981' }} />
            <span>Branches</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rotate-45" style={{ background: '#f472b6' }} />
            <span>Sous-branches</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-4 h-2.5 rounded-full" style={{ background: '#facc15' }} />
            <span>Détails</span>
          </div>
        </div>
        <span className="text-[10px] text-slate-500">Cliquez sur un nœud pour le sélectionner</span>
      </div>
      
      <style>{`
        @keyframes nodeAppear {
          from { opacity: 0; transform: scale(0.5); }
          to { opacity: 1; transform: scale(1); }
        }
        @keyframes drawLine {
          from { stroke-dashoffset: 200; stroke-dasharray: 200; }
          to { stroke-dashoffset: 0; }
        }
      `}</style>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
// QCM — Interactive multiple-choice question
// ═══════════════════════════════════════════════════════════
function InteractiveQCM({ line }: { line: BoardLine }) {
  const choices = line.choices || [];
  const correct = typeof line.correct === 'number' ? line.correct : 0;
  const [selected, setSelected] = useState<number | null>(null);
  const [revealed, setRevealed] = useState(false);

  if (choices.length === 0) return null;

  const handleSelect = (idx: number) => {
    if (revealed) return;
    setSelected(idx);
    setRevealed(true);
  };

  const isCorrect = selected === correct;

  return (
    <div className="my-4 rounded-xl overflow-hidden" style={{ border: '1px solid rgba(255,255,255,0.15)', background: 'rgba(0,0,0,0.2)' }}>
      {/* Question */}
      <div className="px-4 py-3" style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-bold px-2 py-0.5 rounded" style={{ background: 'rgba(96,165,250,0.2)', color: '#60a5fa' }}>QCM</span>
        </div>
        <p
          className="text-base font-semibold katex-dark"
          style={{ color: '#e2e8f0', fontFamily: "'Patrick Hand', cursive", fontSize: '1.15rem' }}
          dangerouslySetInnerHTML={{ __html: renderMixedContent(line.content || '') }}
        />
      </div>
      {/* Choices */}
      <div className="px-4 py-3 space-y-2">
        {choices.map((choice, idx) => {
          const letter = String.fromCharCode(65 + idx);
          let borderColor = 'rgba(255,255,255,0.12)';
          let bg = 'rgba(255,255,255,0.03)';
          let textColor = '#e2e8f0';
          let icon = '';

          if (revealed) {
            if (idx === correct) {
              borderColor = '#4ade80';
              bg = 'rgba(74,222,128,0.12)';
              textColor = '#4ade80';
              icon = '✓';
            } else if (idx === selected) {
              borderColor = '#f87171';
              bg = 'rgba(248,113,113,0.12)';
              textColor = '#f87171';
              icon = '✗';
            }
          }

          return (
            <button
              key={idx}
              onClick={() => handleSelect(idx)}
              disabled={revealed}
              className="w-full text-left flex items-center gap-3 px-4 py-2.5 rounded-lg transition-all duration-200"
              style={{
                border: `2px solid ${borderColor}`,
                background: bg,
                cursor: revealed ? 'default' : 'pointer',
                opacity: revealed && idx !== correct && idx !== selected ? 0.5 : 1,
              }}
              onMouseEnter={(e) => { if (!revealed) { e.currentTarget.style.borderColor = '#60a5fa'; e.currentTarget.style.background = 'rgba(96,165,250,0.08)'; } }}
              onMouseLeave={(e) => { if (!revealed) { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.12)'; e.currentTarget.style.background = 'rgba(255,255,255,0.03)'; } }}
            >
              <span
                className="shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold"
                style={{ background: revealed && idx === correct ? '#4ade80' : 'rgba(255,255,255,0.1)', color: revealed && idx === correct ? '#1a2e1a' : '#e2e8f0' }}
              >
                {icon || letter}
              </span>
              <span
                className="flex-1 text-sm katex-dark"
                style={{ color: textColor, fontFamily: "'Patrick Hand', cursive", fontSize: '1.05rem' }}
                dangerouslySetInnerHTML={{ __html: renderMixedContent(choice) }}
              />
            </button>
          );
        })}
      </div>
      {/* Feedback */}
      {revealed && (
        <div
          className="px-4 py-3 animate-[fadeSlideIn_0.3s_ease-out]"
          style={{ borderTop: '1px solid rgba(255,255,255,0.1)', background: isCorrect ? 'rgba(74,222,128,0.06)' : 'rgba(248,113,113,0.06)' }}
        >
          <p className="text-sm font-bold mb-1" style={{ color: isCorrect ? '#4ade80' : '#f87171', fontFamily: "'Patrick Hand', cursive" }}>
            {isCorrect ? '✓ Bonne réponse !' : `✗ Mauvaise réponse — la bonne réponse est ${String.fromCharCode(65 + correct)}`}
          </p>
          {line.explanation && (
            <p
              className="text-sm katex-dark"
              style={{ color: '#cbd5e1', fontFamily: "'Patrick Hand', cursive" }}
              dangerouslySetInnerHTML={{ __html: renderMixedContent(line.explanation) }}
            />
          )}
        </div>
      )}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
// VRAI / FAUX — Interactive true/false statements
// ═══════════════════════════════════════════════════════════
function InteractiveVraiFaux({ line }: { line: BoardLine }) {
  const statements = line.statements || [];
  const [answers, setAnswers] = useState<Record<number, boolean | null>>({});
  const [_revealedAll, _setRevealedAll] = useState(false);

  if (statements.length === 0) return null;

  const handleAnswer = (idx: number, answer: boolean) => {
    if (answers[idx] !== undefined && answers[idx] !== null) return;
    setAnswers(prev => ({ ...prev, [idx]: answer }));
  };

  const allAnswered = statements.every((_, idx) => answers[idx] !== undefined && answers[idx] !== null);
  const score = statements.filter((s, idx) => answers[idx] === s.correct).length;

  return (
    <div className="my-4 rounded-xl overflow-hidden" style={{ border: '1px solid rgba(255,255,255,0.15)', background: 'rgba(0,0,0,0.2)' }}>
      {/* Header */}
      <div className="px-4 py-3" style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-bold px-2 py-0.5 rounded" style={{ background: 'rgba(251,146,60,0.2)', color: '#fb923c' }}>VRAI / FAUX</span>
        </div>
        {line.content && (
          <p
            className="text-base font-semibold katex-dark"
            style={{ color: '#e2e8f0', fontFamily: "'Patrick Hand', cursive", fontSize: '1.15rem' }}
            dangerouslySetInnerHTML={{ __html: renderMixedContent(line.content) }}
          />
        )}
      </div>
      {/* Statements */}
      <div className="px-4 py-3 space-y-3">
        {statements.map((stmt, idx) => {
          const userAnswer = answers[idx];
          const answered = userAnswer !== undefined && userAnswer !== null;
          const isCorrect = answered && userAnswer === stmt.correct;

          return (
            <div key={idx} className="rounded-lg p-3" style={{ background: 'rgba(255,255,255,0.03)', border: `1px solid ${answered ? (isCorrect ? 'rgba(74,222,128,0.4)' : 'rgba(248,113,113,0.4)') : 'rgba(255,255,255,0.08)'}` }}>
              <p
                className="text-sm mb-2 katex-dark"
                style={{ color: '#e2e8f0', fontFamily: "'Patrick Hand', cursive", fontSize: '1.05rem' }}
                dangerouslySetInnerHTML={{ __html: renderMixedContent(stmt.text) }}
              />
              <div className="flex gap-2">
                <button
                  onClick={() => handleAnswer(idx, true)}
                  disabled={answered}
                  className="px-4 py-1.5 rounded-lg text-sm font-bold transition-all duration-200"
                  style={{
                    background: answered && userAnswer === true ? (isCorrect ? 'rgba(74,222,128,0.25)' : 'rgba(248,113,113,0.25)') : 'rgba(74,222,128,0.1)',
                    color: answered && userAnswer === true ? (isCorrect ? '#4ade80' : '#f87171') : '#4ade80',
                    border: `2px solid ${answered && userAnswer === true ? (isCorrect ? '#4ade80' : '#f87171') : 'rgba(74,222,128,0.3)'}`,
                    cursor: answered ? 'default' : 'pointer',
                    fontFamily: "'Patrick Hand', cursive",
                  }}
                >
                  {answered && userAnswer === true ? (isCorrect ? '✓ Vrai' : '✗ Vrai') : 'Vrai'}
                </button>
                <button
                  onClick={() => handleAnswer(idx, false)}
                  disabled={answered}
                  className="px-4 py-1.5 rounded-lg text-sm font-bold transition-all duration-200"
                  style={{
                    background: answered && userAnswer === false ? (isCorrect ? 'rgba(74,222,128,0.25)' : 'rgba(248,113,113,0.25)') : 'rgba(248,113,113,0.1)',
                    color: answered && userAnswer === false ? (isCorrect ? '#4ade80' : '#f87171') : '#f87171',
                    border: `2px solid ${answered && userAnswer === false ? (isCorrect ? '#4ade80' : '#f87171') : 'rgba(248,113,113,0.3)'}`,
                    cursor: answered ? 'default' : 'pointer',
                    fontFamily: "'Patrick Hand', cursive",
                  }}
                >
                  {answered && userAnswer === false ? (isCorrect ? '✓ Faux' : '✗ Faux') : 'Faux'}
                </button>
              </div>
              {answered && !isCorrect && stmt.explanation && (
                <p className="mt-2 text-xs animate-[fadeSlideIn_0.3s_ease-out] katex-dark" style={{ color: '#fde68a', fontFamily: "'Patrick Hand', cursive" }}
                  dangerouslySetInnerHTML={{ __html: renderMixedContent(stmt.explanation) }}
                />
              )}
            </div>
          );
        })}
      </div>
      {/* Score */}
      {allAnswered && (
        <div className="px-4 py-3 animate-[fadeSlideIn_0.3s_ease-out]" style={{ borderTop: '1px solid rgba(255,255,255,0.1)', background: score === statements.length ? 'rgba(74,222,128,0.08)' : 'rgba(251,146,60,0.08)' }}>
          <p className="text-sm font-bold" style={{ color: score === statements.length ? '#4ade80' : '#fb923c', fontFamily: "'Patrick Hand', cursive" }}>
            Score : {score}/{statements.length} {score === statements.length ? '— Parfait !' : ''}
          </p>
          {line.explanation && (
            <p className="text-xs mt-1 katex-dark" style={{ color: '#cbd5e1', fontFamily: "'Patrick Hand', cursive" }}
              dangerouslySetInnerHTML={{ __html: renderMixedContent(line.explanation) }}
            />
          )}
        </div>
      )}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
// ASSOCIATION — Interactive drag-style matching (click-based)
// ═══════════════════════════════════════════════════════════
function InteractiveAssociation({ line }: { line: BoardLine }) {
  const pairs = line.pairs || [];
  const [selectedLeft, setSelectedLeft] = useState<number | null>(null);
  const [matches, setMatches] = useState<Record<number, number>>({});
  const [shuffledRight, setShuffledRight] = useState<number[]>([]);
  const [revealed, setRevealed] = useState(false);

  useEffect(() => {
    const indices = pairs.map((_, i) => i);
    for (let i = indices.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [indices[i], indices[j]] = [indices[j], indices[i]];
    }
    setShuffledRight(indices);
    setMatches({});
    setSelectedLeft(null);
    setRevealed(false);
  }, [pairs.length]);

  if (pairs.length === 0) return null;

  const handleLeftClick = (idx: number) => {
    if (revealed || matches[idx] !== undefined) return;
    setSelectedLeft(idx);
  };

  const handleRightClick = (rightIdx: number) => {
    if (revealed || selectedLeft === null) return;
    const alreadyUsed = Object.values(matches).includes(rightIdx);
    if (alreadyUsed) return;
    setMatches(prev => ({ ...prev, [selectedLeft]: rightIdx }));
    setSelectedLeft(null);
  };

  const allMatched = Object.keys(matches).length === pairs.length;

  const handleReveal = () => setRevealed(true);

  const score = pairs.filter((_, idx) => matches[idx] === idx).length;
  const rightUsed = new Set(Object.values(matches));

  return (
    <div className="my-4 rounded-xl overflow-hidden" style={{ border: '1px solid rgba(255,255,255,0.15)', background: 'rgba(0,0,0,0.2)' }}>
      {/* Header */}
      <div className="px-4 py-3" style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-bold px-2 py-0.5 rounded" style={{ background: 'rgba(192,132,252,0.2)', color: '#c084fc' }}>ASSOCIATION</span>
        </div>
        {line.content && (
          <p
            className="text-base font-semibold katex-dark"
            style={{ color: '#e2e8f0', fontFamily: "'Patrick Hand', cursive", fontSize: '1.15rem' }}
            dangerouslySetInnerHTML={{ __html: renderMixedContent(line.content) }}
          />
        )}
        <p className="text-xs mt-1" style={{ color: 'rgba(255,255,255,0.4)', fontFamily: "'Patrick Hand', cursive" }}>
          Clique sur un élément à gauche, puis sur son correspondant à droite
        </p>
      </div>
      {/* Matching area */}
      <div className="px-4 py-3">
        <div className="grid grid-cols-2 gap-4">
          {/* Left column */}
          <div className="space-y-2">
            {pairs.map((pair, idx) => {
              const matched = matches[idx] !== undefined;
              const isSelected = selectedLeft === idx;
              const isCorrect = revealed && matched && matches[idx] === idx;
              const isWrong = revealed && matched && matches[idx] !== idx;
              return (
                <button
                  key={`l${idx}`}
                  onClick={() => handleLeftClick(idx)}
                  disabled={matched || revealed}
                  className="w-full text-left px-3 py-2 rounded-lg text-sm transition-all duration-200"
                  style={{
                    border: `2px solid ${isCorrect ? '#4ade80' : isWrong ? '#f87171' : isSelected ? '#60a5fa' : matched ? 'rgba(96,165,250,0.4)' : 'rgba(255,255,255,0.12)'}`,
                    background: isCorrect ? 'rgba(74,222,128,0.12)' : isWrong ? 'rgba(248,113,113,0.12)' : isSelected ? 'rgba(96,165,250,0.15)' : matched ? 'rgba(96,165,250,0.06)' : 'rgba(255,255,255,0.03)',
                    color: isSelected ? '#60a5fa' : '#e2e8f0',
                    cursor: matched || revealed ? 'default' : 'pointer',
                    fontFamily: "'Patrick Hand', cursive",
                    fontSize: '1rem',
                  }}
                >
                  <span dangerouslySetInnerHTML={{ __html: renderMixedContent(pair.left) }} />
                </button>
              );
            })}
          </div>
          {/* Right column */}
          <div className="space-y-2">
            {shuffledRight.map((origIdx) => {
              const used = rightUsed.has(origIdx);
              const matchedLeftIdx = Object.entries(matches).find(([, v]) => v === origIdx)?.[0];
              const isCorrect = revealed && matchedLeftIdx !== undefined && Number(matchedLeftIdx) === origIdx;
              const isWrong = revealed && matchedLeftIdx !== undefined && Number(matchedLeftIdx) !== origIdx;
              return (
                <button
                  key={`r${origIdx}`}
                  onClick={() => handleRightClick(origIdx)}
                  disabled={used || revealed || selectedLeft === null}
                  className="w-full text-left px-3 py-2 rounded-lg text-sm transition-all duration-200"
                  style={{
                    border: `2px solid ${isCorrect ? '#4ade80' : isWrong ? '#f87171' : used ? 'rgba(192,132,252,0.4)' : selectedLeft !== null ? 'rgba(192,132,252,0.5)' : 'rgba(255,255,255,0.12)'}`,
                    background: isCorrect ? 'rgba(74,222,128,0.12)' : isWrong ? 'rgba(248,113,113,0.12)' : used ? 'rgba(192,132,252,0.06)' : 'rgba(255,255,255,0.03)',
                    color: '#e2e8f0',
                    cursor: used || revealed || selectedLeft === null ? 'default' : 'pointer',
                    fontFamily: "'Patrick Hand', cursive",
                    fontSize: '1rem',
                    opacity: used && selectedLeft !== null ? 0.4 : 1,
                  }}
                >
                  <span dangerouslySetInnerHTML={{ __html: renderMixedContent(pairs[origIdx].right) }} />
                </button>
              );
            })}
          </div>
        </div>
      </div>
      {/* Validate button & score */}
      {allMatched && !revealed && (
        <div className="px-4 py-3" style={{ borderTop: '1px solid rgba(255,255,255,0.1)' }}>
          <button
            onClick={handleReveal}
            className="w-full py-2 rounded-lg text-sm font-bold transition-all duration-200"
            style={{ background: 'rgba(192,132,252,0.2)', color: '#c084fc', border: '2px solid rgba(192,132,252,0.4)', cursor: 'pointer', fontFamily: "'Patrick Hand', cursive" }}
          >
            Vérifier mes réponses
          </button>
        </div>
      )}
      {revealed && (
        <div className="px-4 py-3 animate-[fadeSlideIn_0.3s_ease-out]" style={{ borderTop: '1px solid rgba(255,255,255,0.1)', background: score === pairs.length ? 'rgba(74,222,128,0.08)' : 'rgba(192,132,252,0.08)' }}>
          <p className="text-sm font-bold" style={{ color: score === pairs.length ? '#4ade80' : '#c084fc', fontFamily: "'Patrick Hand', cursive" }}>
            Score : {score}/{pairs.length} {score === pairs.length ? '— Parfait !' : ''}
          </p>
          {score < pairs.length && (
            <div className="mt-2 space-y-1">
              {pairs.map((pair, idx) => matches[idx] !== idx ? (
                <p key={idx} className="text-xs" style={{ color: '#fde68a', fontFamily: "'Patrick Hand', cursive" }}>
                  {pair.left} → {pair.right}
                </p>
              ) : null)}
            </div>
          )}
          {line.explanation && (
            <p className="text-xs mt-2 katex-dark" style={{ color: '#cbd5e1', fontFamily: "'Patrick Hand', cursive" }}
              dangerouslySetInnerHTML={{ __html: renderMixedContent(line.explanation) }}
            />
          )}
        </div>
      )}
    </div>
  );
}

function renderLine(line: BoardLine) {
  // Defensive checks
  if (!line || typeof line !== 'object') {
    console.error('[MathBoard] Invalid line:', line);
    return null;
  }
  
  const color = resolveColor(line.color);
  const content = line.content || '';
  const type = line.type || 'text';
  const isRtl = containsArabic(content);
  const dir: 'rtl' | undefined = isRtl ? 'rtl' : undefined;
  const rtlAlign: 'right' | undefined = isRtl ? 'right' : undefined;

  switch (type) {
    case 'title':
      return (
        <h2
          dir={dir}
          className="text-2xl font-bold pb-2 mb-1 border-b-2"
          style={{ color, borderColor: color + '40', fontFamily: "'Patrick Hand', cursive", textAlign: rtlAlign }}
        >
          {content}
        </h2>
      );

    case 'subtitle':
      return (
        <h3
          dir={dir}
          className="text-lg font-semibold mt-3 mb-1"
          style={{ color, fontFamily: "'Patrick Hand', cursive", textAlign: rtlAlign }}
        >
          {content}
        </h3>
      );

    case 'text':
      return (
        <p
          dir={dir}
          className="text-base leading-relaxed katex-dark"
          style={{ color, fontFamily: "'Patrick Hand', 'Caveat', cursive", fontSize: '1.15rem', textAlign: rtlAlign }}
          dangerouslySetInnerHTML={{ __html: renderMixedContent(content) }}
        />
      );

    case 'math':
      return (
        <div
          className="my-2 py-2 px-3 rounded-lg overflow-x-auto katex-dark"
          style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}
          dangerouslySetInnerHTML={{ __html: renderDisplayMath(content) }}
        />
      );

    case 'step': {
      const label = line.label || '';
      return (
        <div className="flex gap-3 items-start my-1.5" style={{ flexDirection: isRtl ? 'row-reverse' : undefined }}>
          {label && (
            <span
              className="shrink-0 inline-flex items-center justify-center w-7 h-7 rounded-full text-sm font-bold mt-0.5"
              style={{ backgroundColor: color, color: '#1a2e1a', fontFamily: "system-ui" }}
            >
              {label}
            </span>
          )}
          <div
            dir={dir}
            className="flex-1 text-base leading-relaxed katex-dark"
            style={{ color: DEFAULT_TEXT_COLOR, fontFamily: "'Patrick Hand', 'Caveat', cursive", fontSize: '1.1rem', textAlign: rtlAlign }}
            dangerouslySetInnerHTML={{ __html: renderMixedContent(content) }}
          />
        </div>
      );
    }

    case 'box':
      return (
        <div
          className="my-3 p-4 rounded-xl border-2 border-dashed katex-dark"
          style={{ borderColor: color + '60', backgroundColor: 'rgba(255,255,255,0.05)' }}
        >
          <div
            dir={dir}
            className="text-base leading-relaxed"
            style={{ color, fontFamily: "'Patrick Hand', 'Caveat', cursive", fontSize: '1.15rem', textAlign: rtlAlign }}
            dangerouslySetInnerHTML={{ __html: renderMixedContent(content) }}
          />
        </div>
      );

    case 'note':
      return (
        <div className="my-2 flex items-start gap-2 pl-3 rounded-r-lg py-2 pr-3 katex-dark" style={{ borderLeft: '3px solid #facc15', background: 'rgba(250,204,21,0.08)', flexDirection: isRtl ? 'row-reverse' : undefined }}>
          <span className="text-lg" style={{ color: '#facc15' }}>💡</span>
          <span
            dir={dir}
            className="text-sm flex-1"
            style={{ color: '#fde68a', fontFamily: "'Patrick Hand', cursive", textAlign: rtlAlign }}
            dangerouslySetInnerHTML={{ __html: renderMixedContent(content) }}
          />
        </div>
      );

    case 'warning':
      return (
        <div className="my-2 flex items-start gap-2 pl-3 rounded-r-lg py-2 pr-3 katex-dark" style={{ borderLeft: '3px solid #f87171', background: 'rgba(248,113,113,0.12)', flexDirection: isRtl ? 'row-reverse' : undefined }}>
          <span className="text-lg" style={{ color: '#f87171' }}>⚠️</span>
          <span
            dir={dir}
            className="text-sm flex-1"
            style={{ color: '#fca5a5', fontFamily: "'Patrick Hand', cursive", textAlign: rtlAlign }}
            dangerouslySetInnerHTML={{ __html: renderMixedContent(content) }}
          />
        </div>
      );

    case 'tip':
      return (
        <div className="my-2 flex items-start gap-2 pl-3 rounded-r-lg py-2 pr-3 katex-dark" style={{ borderLeft: '3px solid #4ade80', background: 'rgba(74,222,128,0.08)', flexDirection: isRtl ? 'row-reverse' : undefined }}>
          <span className="text-lg" style={{ color: '#4ade80' }}>✅</span>
          <span
            dir={dir}
            className="text-sm flex-1"
            style={{ color: '#86efac', fontFamily: "'Patrick Hand', cursive", textAlign: rtlAlign }}
            dangerouslySetInnerHTML={{ __html: renderMixedContent(content) }}
          />
        </div>
      );

    case 'separator':
      return <hr className="my-3" style={{ borderColor: 'rgba(255,255,255,0.15)' }} />;

    case 'table':
      return <AnimatedTable line={line} />;

    case 'graph':
      return <AnimatedGraph line={line} />;

    case 'diagram':
      return <AnimatedDiagram line={line} />;

    case 'mindmap':
      if (!line.mindmapNodes || !line.centerNode) {
        return <p className="text-red-400">Erreur: données mindmap manquantes</p>;
      }
      return (
        <div className="my-4" style={{ height: '500px' }}>
          <MindMap
            title={content || "Schéma récapitulatif"}
            nodes={line.mindmapNodes}
            centerNode={line.centerNode}
          />
        </div>
      );

    case 'qcm':
      return <InteractiveQCM line={line} />;

    case 'vrai_faux':
      return <InteractiveVraiFaux line={line} />;

    case 'association':
      return <InteractiveAssociation line={line} />;

    default:
      return (
        <p
          dir={dir}
          className="text-base katex-dark"
          style={{ color: DEFAULT_TEXT_COLOR, fontFamily: "'Patrick Hand', cursive", textAlign: rtlAlign }}
          dangerouslySetInnerHTML={{ __html: renderMixedContent(content) }}
        />
      );
  }
}

const MathBoard = memo(MathBoardInner);
export default MathBoard;
