import { useEffect, useRef, useState, useCallback, memo } from 'react';
import SVGSchemaViewer from './schemas/SVGSchemaViewer';
import { getSchemaById } from './schemas';
import MathBoard from './MathBoard';

// Load handwritten fonts
const loadHandwrittenFonts = () => {
  if (typeof document !== 'undefined' && !document.getElementById('handwritten-fonts')) {
    const link = document.createElement('link');
    link.id = 'handwritten-fonts';
    link.rel = 'stylesheet';
    link.href = 'https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&family=Patrick+Hand&display=swap';
    document.head.appendChild(link);
  }
};

// Types for drawing elements
interface DrawPoint {
  x: number;
  y: number;
}

interface DrawElement {
  id: string;
  type: 'line' | 'arrow' | 'rect' | 'circle' | 'text' | 'path' | 'mitochondria' | 'cell' | 'dna' | 'nucleus' | 'membrane';
  points?: DrawPoint[];
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  radius?: number;
  text?: string;
  color: string;
  strokeWidth: number;
  fontSize?: number;
  fill?: string;
  label?: string;
  // 3D effect properties
  shadow?: boolean;
  gradient?: boolean;
  depth?: number;
  // Animation
  delay?: number;
}

interface DrawStep {
  elements: DrawElement[];
  narration?: string;
  title?: string;
  clear?: boolean;
}

interface BoardContent {
  title?: string;
  lines: Array<{
    type: 'title' | 'subtitle' | 'text' | 'math' | 'step' | 'separator' | 'box' | 'note' | 'table' | 'graph' | 'diagram' | 'qcm' | 'vrai_faux' | 'association';
    content: string;
    color?: string;
    label?: string;
    // Interactive exercise data
    choices?: string[];
    correct?: number | number[] | boolean;
    explanation?: string;
    statements?: { text: string; correct: boolean; explanation?: string }[];
    pairs?: { left: string; right: string }[];
    // Table/graph/diagram data (pass-through)
    headers?: string[];
    rows?: string[][];
    curves?: any[];
    nodes?: any[];
    edges?: any[];
    [key: string]: any;
  }>;
}

interface AIWhiteboardProps {
  drawCommands: DrawStep[] | null;
  isVisible: boolean;
  onClose?: () => void;
  schemaId?: string | null;
  activeHighlights?: string[];
  boardContent?: BoardContent | null;
}

// Chalk-on-dark palette — bright shades legible on the dark green chalkboard.
// Any text defaulting to "black" is remapped to chalk-white so it never
// disappears on the board.
const COLORS = {
  black: '#f1f5f9',   // chalk white fallback (was dark navy)
  white: '#f1f5f9',
  red: '#fca5a5',     // chalk red
  blue: '#93c5fd',    // chalk blue
  green: '#86efac',   // chalk green (was #27ae60, too dark)
  orange: '#fdba74',  // chalk orange
  purple: '#d8b4fe',
  cyan: '#67e8f9',
  pink: '#f9a8d4',
  yellow: '#fde047',
};

function resolveColor(color: string): string {
  return (COLORS as any)[color] || color || COLORS.black;
}

  function AIWhiteboardInner({ drawCommands, isVisible, onClose, schemaId, activeHighlights, boardContent }: AIWhiteboardProps) {
  console.log('[AIWhiteboard] Render:', {
    hasDrawCommands: !!(drawCommands && drawCommands.length > 0),
    hasSchemaId: !!schemaId,
    hasBoardContent: !!(boardContent && boardContent.lines?.length > 0),
    isVisible
  });
  const activeSchema = schemaId ? getSchemaById(schemaId) : undefined;
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [drawnElements, setDrawnElements] = useState<DrawElement[]>([]);
  const [animating, setAnimating] = useState(false);
  const [title, setTitle] = useState('');
  const timeoutsRef = useRef<ReturnType<typeof setTimeout>[]>([]);
  const animationRunIdRef = useRef(0);

  // Load handwritten fonts on mount
  useEffect(() => {
    loadHandwrittenFonts();
  }, []);

  // Clear all timeouts on unmount
  useEffect(() => {
    return () => {
      animationRunIdRef.current += 1;
      timeoutsRef.current.forEach(t => clearTimeout(t));
      timeoutsRef.current = [];
    };
  }, []);

  // Animate drawing step by step
  const animateStep = useCallback((commands: DrawStep[], stepIdx: number, runId: number) => {
    if (runId !== animationRunIdRef.current) {
      console.warn('[AIWhiteboard][WARN] Ignoring stale animation run', { runId, activeRunId: animationRunIdRef.current, stepIdx });
      return;
    }

    if (!commands || stepIdx >= commands.length) {
      if (runId === animationRunIdRef.current) {
        if (!commands || commands.length === 0) {
          console.warn('[AIWhiteboard][WARN] animateStep called without usable drawing commands');
        }
        setAnimating(false);
      }
      return;
    }

    const step = commands[stepIdx] as any;
    if (!step) {
      console.warn('[AIWhiteboard][WARN] Null step at index', stepIdx);
      animateStep(commands, stepIdx + 1, runId);
      return;
    }

    // Normalize: ensure step has an elements array
    let elements: DrawElement[] = [];
    if (Array.isArray(step.elements) && step.elements.length > 0) {
      elements = step.elements;
    } else if (Array.isArray(step.lines)) {
      // Convert board-like lines to text DrawElements
      let y = 30;
      elements = step.lines.map((line: any, i: number) => {
        const text = typeof line === 'string' ? line : (line?.content || line?.text || '');
        const lineType = typeof line === 'object' ? (line?.type || 'text') : 'text';
        const fontSize = lineType === 'title' || lineType === 'subtitle' ? 18 : 14;
        const color = lineType === 'title' ? '#FFD700' : '#FFFFFF';
        const el: DrawElement = { id: `l${i}`, type: 'text', x: 20, y, text, color, strokeWidth: 1, fontSize };
        y += fontSize + 8;
        return el;
      });
    } else if (step.type && ['line', 'arrow', 'rect', 'circle', 'text', 'path'].includes(step.type)) {
      // Step IS a single element
      elements = [{ ...step, id: step.id || 'e0', color: step.color || '#FFFFFF', strokeWidth: step.strokeWidth || 2 }];
    } else if (step.content || step.text) {
      // Fallback: single text element from content/text field
      elements = [{ id: 'txt0', type: 'text', x: 20, y: 40, text: step.content || step.text, color: '#FFFFFF', strokeWidth: 1, fontSize: 14 }];
    }

    if (elements.length === 0) {
      console.warn('[AIWhiteboard][WARN] Could not extract elements from step, skipping:', { stepIdx, step });
      animateStep(commands, stepIdx + 1, runId);
      return;
    }

    if (step.title) setTitle(step.title);

    if (step.clear) {
      console.log('[AIWhiteboard] Step requests clear before drawing', { stepIdx, title: step.title || '' });
      setDrawnElements([]);
    }

    // Add elements one by one with delay
    elements.forEach((el, i) => {
      const delay = (el.delay || 0) + i * 300; // 300ms between each element
      const timeout = setTimeout(() => {
        if (runId !== animationRunIdRef.current) return;
        setDrawnElements(prev => [...prev, el]);
      }, delay);
      timeoutsRef.current.push(timeout);
    });

    // Move to next step after all elements are drawn
    const totalDelay = Math.max(
      0,
      ...elements.map((el, i) => (el.delay || 0) + i * 300)
    ) + 800;
    const nextTimeout = setTimeout(() => {
      if (runId !== animationRunIdRef.current) return;
      setCurrentStepIndex(stepIdx + 1);
      animateStep(commands, stepIdx + 1, runId);
    }, totalDelay);
    timeoutsRef.current.push(nextTimeout);
  }, []);

  // Reset when new commands arrive or when cleared
  useEffect(() => {
    const runId = ++animationRunIdRef.current;
    // Clear all pending animations first
    timeoutsRef.current.forEach(t => clearTimeout(t));
    timeoutsRef.current = [];
    
    if (drawCommands && drawCommands.length > 0) {
      console.log('[AIWhiteboard] Starting new animation run', { runId, stepCount: drawCommands.length, firstTitle: drawCommands[0]?.title || '' });
      // New drawing commands - reset and start fresh
      setCurrentStepIndex(0);
      setDrawnElements([]);
      setAnimating(true);
      setTitle(drawCommands[0]?.title || '');
      animateStep(drawCommands, 0, runId);
    } else {
      if (drawCommands && drawCommands.length === 0) {
        console.warn('[AIWhiteboard][WARN] drawCommands was provided but empty; resetting board state');
      }
      // Commands cleared - reset canvas state
      setCurrentStepIndex(0);
      setDrawnElements([]);
      setAnimating(false);
      setTitle('');
    }
  }, [drawCommands, animateStep]);

  // Compute scale to fit elements in canvas
  const computeScale = useCallback((canvasW: number, canvasH: number, elements: DrawElement[]) => {
    if (elements.length === 0) return { scaleX: 1, scaleY: 1, offsetX: 0, offsetY: 0 };
    
    let maxX = 600, maxY = 400; // Default expected canvas from AI
    elements.forEach(el => {
      const ex = (el.x || 0) + (el.width || 0) + 20;
      const ey = (el.y || 0) + (el.height || 0) + 20;
      if (el.points) {
        el.points.forEach(p => {
          if (p.x + 20 > maxX) maxX = p.x + 20;
          if (p.y + 20 > maxY) maxY = p.y + 20;
        });
      }
      if (el.radius) {
        const cr = (el.x || 0) + (el.radius || 0) + 20;
        const cb = (el.y || 0) + (el.radius || 0) + 20;
        if (cr > maxX) maxX = cr;
        if (cb > maxY) maxY = cb;
      }
      if (ex > maxX) maxX = ex;
      if (ey > maxY) maxY = ey;
    });
    
    const scaleX = canvasW / Math.max(maxX, 600);
    const scaleY = canvasH / Math.max(maxY, 400);
    const scale = Math.min(scaleX, scaleY, 2.5); // Cap at 2.5x
    const offsetX = (canvasW - maxX * scale) / 2;
    const offsetY = Math.max(10, (canvasH - maxY * scale) / 2);
    
    return { scaleX: scale, scaleY: scale, offsetX: Math.max(10, offsetX), offsetY };
  }, []);

  // Canvas rendering
  useEffect(() => {
    console.log('[AIWhiteboard] Canvas render effect triggered, drawnElements:', drawnElements.length);

    if (!isVisible) {
      return;
    }

    // Only skip canvas render if board/schema mode is truly active AND we have NO draw elements
    // This prevents stale boardContent from blocking a newly arrived draw command
    const boardActive = boardContent && boardContent.lines?.length > 0;
    const schemaActive = !!activeSchema;
    const hasDrawData = drawCommands && drawCommands.length > 0;
    if ((boardActive || schemaActive) && !hasDrawData) {
      console.log('[AIWhiteboard] Skipping canvas render effect because board/schema mode is active (no draw data)');
      return;
    }

    const canvas = canvasRef.current;
    if (!canvas) {
      console.error('[AIWhiteboard][ERROR] Canvas ref is null; cannot render whiteboard');
      return;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) {
      console.error('[AIWhiteboard][ERROR] Unable to get 2D context from canvas');
      return;
    }

    // Set canvas size with device pixel ratio for sharp rendering
    const container = containerRef.current;
    const dpr = Math.max(window.devicePixelRatio || 1, 2);
    if (container) {
      canvas.width = container.clientWidth * dpr;
      canvas.height = container.clientHeight * dpr;
      canvas.style.width = container.clientWidth + 'px';
      canvas.style.height = container.clientHeight + 'px';
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(dpr, dpr);
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
    } else {
      console.warn('[AIWhiteboard][WARN] Container ref is null; using fallback canvas dimensions');
    }

    const cw = container?.clientWidth || canvas.width;
    const ch = container?.clientHeight || canvas.height;

    // Clear canvas - dark whiteboard background
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, cw, ch);

    // Draw grid (subtle)
    ctx.strokeStyle = '#e8e8e8';
    ctx.lineWidth = 0.5;
    for (let x = 0; x < cw; x += 40) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, ch);
      ctx.stroke();
    }
    for (let y = 0; y < ch; y += 40) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(cw, y);
      ctx.stroke();
    }

    // Scale elements to fit canvas
    const { scaleX, offsetX, offsetY } = computeScale(cw, ch, drawnElements);
    ctx.save();
    ctx.translate(offsetX, offsetY);
    ctx.scale(scaleX, scaleX);

    // Draw all elements
    drawnElements.forEach(el => {
      drawElement(ctx, el);
    });

    ctx.restore();
  }, [drawnElements, computeScale]);

  // Resize handler - triggers re-render by updating a dummy state
  useEffect(() => {
    const handleResize = () => {
      // Force re-render which will re-run the canvas effect
      setDrawnElements(prev => [...prev]);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const drawElement = (ctx: CanvasRenderingContext2D, el: DrawElement) => {
    const color = resolveColor(el.color);
    ctx.strokeStyle = color;
    ctx.fillStyle = el.fill ? resolveColor(el.fill) : color;
    ctx.lineWidth = el.strokeWidth || 2;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // Add subtle shadow for depth
    ctx.shadowColor = 'rgba(0,0,0,0.08)';
    ctx.shadowBlur = 3;
    ctx.shadowOffsetX = 1;
    ctx.shadowOffsetY = 1;

    switch (el.type) {
      case 'rect': {
        const x = el.x || 0;
        const y = el.y || 0;
        const w = el.width || 100;
        const h = el.height || 50;
        const radius = el.radius || 8;

        // Fill with gradient for 3D effect
        if (el.fill) {
          const fillGradient = ctx.createLinearGradient(x, y, x, y + h);
          const baseColor = resolveColor(el.fill);
          fillGradient.addColorStop(0, baseColor);
          fillGradient.addColorStop(0.5, baseColor);
          fillGradient.addColorStop(1, 'rgba(0, 0, 0, 0.2)');
          
          ctx.globalAlpha = 0.4;
          ctx.fillStyle = fillGradient;
          ctx.beginPath();
          ctx.roundRect(x, y, w, h, radius);
          ctx.fill();
          ctx.globalAlpha = 1;
          
          // Add subtle shadow for depth
          ctx.shadowColor = 'rgba(0, 0, 0, 0.2)';
          ctx.shadowBlur = 6;
          ctx.shadowOffsetX = 2;
          ctx.shadowOffsetY = 2;
        }

        // Draw with hand-drawn effect
        ctx.strokeStyle = color;
        ctx.lineWidth = (el.strokeWidth || 2) + 1;
        ctx.beginPath();
        drawHandDrawnRect(ctx, x, y, w, h);
        ctx.stroke();
        
        ctx.shadowBlur = 0;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;

        // Label inside with handwritten font and outline
        if (el.label) {
          ctx.shadowBlur = 0;
          ctx.fillStyle = color;
          const fontSize = Math.max(13, el.fontSize || Math.min(16, w / Math.max(el.label.length, 1) * 1.8));
          ctx.font = `600 ${fontSize}px 'Patrick Hand', 'Caveat', cursive`;
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          
          // White outline for readability
          ctx.strokeStyle = 'white';
          ctx.lineWidth = 2;
          ctx.lineJoin = 'round';
          
          // Wrap text if too long
          const maxWidth = w - 10;
          if (ctx.measureText(el.label).width > maxWidth && el.label.includes(' ')) {
            const words = el.label.split(' ');
            const mid = Math.ceil(words.length / 2);
            const line1 = words.slice(0, mid).join(' ');
            const line2 = words.slice(mid).join(' ');
            ctx.strokeText(line1, x + w / 2, y + h / 2 - fontSize * 0.6, maxWidth);
            ctx.fillText(line1, x + w / 2, y + h / 2 - fontSize * 0.6, maxWidth);
            ctx.strokeText(line2, x + w / 2, y + h / 2 + fontSize * 0.6, maxWidth);
            ctx.fillText(line2, x + w / 2, y + h / 2 + fontSize * 0.6, maxWidth);
          } else {
            ctx.strokeText(el.label, x + w / 2, y + h / 2, maxWidth);
            ctx.fillText(el.label, x + w / 2, y + h / 2, maxWidth);
          }
        }
        break;
      }

      case 'circle': {
        const cx = el.x || 0;
        const cy = el.y || 0;
        const r = el.radius || 30;

        if (el.fill) {
          ctx.globalAlpha = 0.2;
          ctx.fillStyle = resolveColor(el.fill);
          ctx.beginPath();
          ctx.arc(cx, cy, r, 0, Math.PI * 2);
          ctx.fill();
          ctx.globalAlpha = 1;
        }

        ctx.strokeStyle = color;
        ctx.lineWidth = (el.strokeWidth || 2) + 0.5;
        ctx.beginPath();
        drawHandDrawnCircle(ctx, cx, cy, r);
        ctx.stroke();

        if (el.label) {
          ctx.shadowBlur = 0;
          ctx.fillStyle = color;
          const fontSize = el.fontSize || Math.min(13, r * 0.8);
          ctx.font = `600 ${fontSize}px 'Patrick Hand', 'Caveat', cursive`;
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.strokeStyle = 'rgba(255,255,255,0.9)';
          ctx.lineWidth = 1.5;
          ctx.strokeText(el.label, cx, cy, r * 1.8);
          ctx.fillText(el.label, cx, cy, r * 1.8);
        }
        break;
      }

      case 'arrow': {
        if (!el.points || el.points.length < 2) break;
        const from = el.points[0];
        const to = el.points[el.points.length - 1];

        ctx.strokeStyle = color;
        ctx.lineWidth = (el.strokeWidth || 2) + 0.5;
        ctx.beginPath();
        drawHandDrawnLine(ctx, from.x, from.y, to.x, to.y);
        ctx.stroke();

        // Filled arrow head
        const angle = Math.atan2(to.y - from.y, to.x - from.x);
        const headLen = 14;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(to.x, to.y);
        ctx.lineTo(
          to.x - headLen * Math.cos(angle - Math.PI / 6),
          to.y - headLen * Math.sin(angle - Math.PI / 6)
        );
        ctx.lineTo(
          to.x - headLen * Math.cos(angle + Math.PI / 6),
          to.y - headLen * Math.sin(angle + Math.PI / 6)
        );
        ctx.closePath();
        ctx.fill();

        if (el.label) {
          ctx.shadowBlur = 0;
          const midX = (from.x + to.x) / 2;
          const midY = (from.y + to.y) / 2;
          const fontSize = el.fontSize || 12;
          ctx.font = `600 ${fontSize}px 'Patrick Hand', 'Caveat', cursive`;
          // Draw label background
          const labelW = ctx.measureText(el.label).width + 8;
          ctx.fillStyle = 'rgba(248,249,250,0.9)';
          ctx.fillRect(midX - labelW / 2, midY - fontSize - 2, labelW, fontSize + 6);
          // Draw label text
          ctx.fillStyle = color;
          ctx.strokeStyle = 'rgba(255,255,255,0.95)';
          ctx.lineWidth = 1.25;
          ctx.textAlign = 'center';
          ctx.textBaseline = 'bottom';
          ctx.strokeText(el.label, midX, midY);
          ctx.fillText(el.label, midX, midY);
        }
        break;
      }

      case 'line': {
        if (!el.points || el.points.length < 2) break;
        ctx.strokeStyle = color;
        ctx.beginPath();
        ctx.moveTo(el.points[0].x, el.points[0].y);
        for (let i = 1; i < el.points.length; i++) {
          drawHandDrawnLine(ctx, el.points[i - 1].x, el.points[i - 1].y, el.points[i].x, el.points[i].y);
        }
        ctx.stroke();
        break;
      }

      case 'text': {
        ctx.shadowBlur = 0;
        const fontSize = el.fontSize || 16;
        const isBigTitle = fontSize >= 15;
        ctx.fillStyle = color;
        // Use handwritten font for natural professor-like appearance
        ctx.font = `${isBigTitle ? '700 ' : '500 '}${fontSize}px 'Patrick Hand', 'Caveat', cursive`;
        ctx.textAlign = 'left';
        ctx.textBaseline = 'top';
        ctx.strokeStyle = 'rgba(255,255,255,0.85)';
        ctx.lineWidth = isBigTitle ? 1.5 : 1;
        ctx.lineJoin = 'round';
        
        const text = el.text || '';
        const lines = text.split('\n');
        const lineHeight = fontSize * 1.35;
        lines.forEach((line, i) => {
          const textX = Math.round(el.x || 0) + 0.5;
          const textY = Math.round((el.y || 0) + i * lineHeight) + 0.5;
          ctx.strokeText(line, textX, textY);
          ctx.fillText(line, textX, textY);
        });
        break;
      }

      case 'path': {
        if (!el.points || el.points.length < 2) break;
        ctx.strokeStyle = color;
        ctx.beginPath();
        ctx.moveTo(el.points[0].x, el.points[0].y);
        for (let i = 1; i < el.points.length; i++) {
          const xc = (el.points[i].x + el.points[i - 1].x) / 2;
          const yc = (el.points[i].y + el.points[i - 1].y) / 2;
          ctx.quadraticCurveTo(el.points[i - 1].x, el.points[i - 1].y, xc, yc);
        }
        ctx.stroke();
        break;
      }

      case 'mitochondria': {
        // Draw mitochondria with cristae - ENHANCED 3D
        const x = el.x || 0;
        const y = el.y || 0;
        const w = el.width || 120;
        const h = el.height || 60;
        
        // Strong 3D gradient with light source
        const gradient = ctx.createRadialGradient(
          x + w * 0.35, y + h * 0.3, w * 0.1,
          x + w/2, y + h/2, w * 0.6
        );
        gradient.addColorStop(0, '#FFD700');  // Bright golden highlight
        gradient.addColorStop(0.3, '#FFA500');  // Orange
        gradient.addColorStop(0.6, '#FF8C00');  // Dark orange
        gradient.addColorStop(0.85, '#FF6347');  // Red-orange
        gradient.addColorStop(1, 'rgba(139, 69, 19, 0.5)');  // Dark edge
        
        // Shadow for depth
        ctx.shadowColor = 'rgba(0, 0, 0, 0.35)';
        ctx.shadowBlur = 12;
        ctx.shadowOffsetX = 4;
        ctx.shadowOffsetY = 4;
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.ellipse(x + w/2, y + h/2, w/2, h/2, 0, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.shadowBlur = 0;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        
        // Outer membrane with hand-drawn effect
        ctx.strokeStyle = resolveColor(color);
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.ellipse(x + w/2, y + h/2, w/2, h/2, 0, 0, Math.PI * 2);
        ctx.stroke();
        
        // Inner membrane (cristae) - more detailed and visible
        ctx.strokeStyle = 'rgba(139, 69, 19, 0.8)';
        ctx.lineWidth = 2;
        for (let i = 0; i < 5; i++) {
          ctx.beginPath();
          const yPos = y + h * 0.25 + i * (h * 0.13);
          ctx.moveTo(x + w * 0.15, yPos);
          ctx.quadraticCurveTo(x + w * 0.35, yPos - 6, x + w * 0.5, yPos);
          ctx.quadraticCurveTo(x + w * 0.65, yPos + 4, x + w * 0.85, yPos);
          ctx.stroke();
        }
        
        // Matrix granules (small dots for detail)
        ctx.fillStyle = 'rgba(255, 215, 0, 0.4)';
        for (let i = 0; i < 8; i++) {
          const angle = Math.random() * Math.PI * 2;
          const dist = Math.random() * (w * 0.3);
          const dotX = x + w/2 + Math.cos(angle) * dist;
          const dotY = y + h/2 + Math.sin(angle) * (dist * h/w);
          ctx.beginPath();
          ctx.arc(dotX, dotY, 1.5, 0, Math.PI * 2);
          ctx.fill();
        }
        
        // Label with outline for readability
        if (el.label) {
          ctx.shadowBlur = 0;
          ctx.fillStyle = resolveColor(color);
          ctx.font = `600 ${el.fontSize || 13}px 'Patrick Hand', 'Caveat', cursive`;
          ctx.textAlign = 'center';
          ctx.strokeStyle = 'white';
          ctx.lineWidth = 2;
          ctx.strokeText(el.label, x + w/2, y + h + 18);
          ctx.fillText(el.label, x + w/2, y + h + 18);
        }
        break;
      }

      case 'cell': {
        // Draw cell with membrane and organelles - ENHANCED 3D
        const cx = el.x || 0;
        const cy = el.y || 0;
        const r = el.radius || 80;
        
        // Strong 3D sphere gradient with light source from top-left
        const membraneGradient = ctx.createRadialGradient(
          cx - r * 0.3, cy - r * 0.3, r * 0.1,  // Light source position
          cx, cy, r * 1.1
        );
        membraneGradient.addColorStop(0, 'rgba(220, 240, 255, 0.9)');  // Bright highlight
        membraneGradient.addColorStop(0.3, 'rgba(173, 216, 230, 0.7)');
        membraneGradient.addColorStop(0.6, 'rgba(135, 206, 250, 0.8)');
        membraneGradient.addColorStop(0.85, resolveColor(color));
        membraneGradient.addColorStop(1, 'rgba(0, 0, 0, 0.3)');  // Dark edge for depth
        
        // Shadow for depth
        ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
        ctx.shadowBlur = 15;
        ctx.shadowOffsetX = 5;
        ctx.shadowOffsetY = 5;
        
        ctx.fillStyle = membraneGradient;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.shadowBlur = 0;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        
        // Outer membrane with hand-drawn effect
        ctx.strokeStyle = color;
        ctx.lineWidth = 3.5;
        ctx.beginPath();
        drawHandDrawnCircle(ctx, cx, cy, r);
        ctx.stroke();
        
        // Inner membrane (phospholipid bilayer) - more visible
        ctx.strokeStyle = 'rgba(70, 130, 180, 0.6)';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        drawHandDrawnCircle(ctx, cx, cy, r - 5);
        ctx.stroke();
        
        // Cytoplasm texture (small dots for realism)
        ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
        for (let i = 0; i < 15; i++) {
          const angle = Math.random() * Math.PI * 2;
          const dist = Math.random() * (r - 20);
          const dotX = cx + Math.cos(angle) * dist;
          const dotY = cy + Math.sin(angle) * dist;
          ctx.beginPath();
          ctx.arc(dotX, dotY, 1.5, 0, Math.PI * 2);
          ctx.fill();
        }
        
        if (el.label) {
          ctx.shadowBlur = 0;
          ctx.fillStyle = color;
          ctx.font = `600 ${el.fontSize || 14}px 'Patrick Hand', 'Caveat', cursive`;
          ctx.textAlign = 'center';
          ctx.strokeStyle = 'white';
          ctx.lineWidth = 2;
          ctx.strokeText(el.label, cx, cy + r + 20);
          ctx.fillText(el.label, cx, cy + r + 20);
        }
        break;
      }

      case 'nucleus': {
        // Draw nucleus with nuclear envelope - ENHANCED 3D
        const cx = el.x || 0;
        const cy = el.y || 0;
        const r = el.radius || 40;
        
        // Strong 3D gradient with pronounced light source
        const nucGradient = ctx.createRadialGradient(
          cx - r * 0.35, cy - r * 0.35, r * 0.1,
          cx, cy, r * 1.05
        );
        nucGradient.addColorStop(0, '#B19CD9');  // Bright highlight
        nucGradient.addColorStop(0.25, '#9370DB');
        nucGradient.addColorStop(0.6, '#7B68EE');
        nucGradient.addColorStop(0.85, '#6A5ACD');
        nucGradient.addColorStop(1, '#483D8B');  // Dark edge
        
        // Shadow for depth
        ctx.shadowColor = 'rgba(0, 0, 0, 0.4)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetX = 3;
        ctx.shadowOffsetY = 3;
        
        ctx.fillStyle = nucGradient;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.shadowBlur = 0;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        
        // Nuclear envelope (double membrane) - more visible
        ctx.strokeStyle = resolveColor(color);
        ctx.lineWidth = 3;
        ctx.beginPath();
        drawHandDrawnCircle(ctx, cx, cy, r);
        ctx.stroke();
        
        // Inner nuclear membrane
        ctx.strokeStyle = 'rgba(138, 43, 226, 0.5)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        drawHandDrawnCircle(ctx, cx, cy, r - 3);
        ctx.stroke();
        
        // Chromatin (DNA strands inside) - more visible and detailed
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.lineWidth = 1.5;
        for (let i = 0; i < 12; i++) {
          const angle = (i / 12) * Math.PI * 2;
          const x1 = cx + Math.cos(angle) * (r * 0.2);
          const y1 = cy + Math.sin(angle) * (r * 0.2);
          const x2 = cx + Math.cos(angle + 0.4) * (r * 0.7);
          const y2 = cy + Math.sin(angle + 0.4) * (r * 0.7);
          ctx.beginPath();
          ctx.moveTo(x1, y1);
          ctx.lineTo(x2, y2);
          ctx.stroke();
        }
        
        // Nucleolus (small dark spot)
        ctx.fillStyle = 'rgba(75, 0, 130, 0.7)';
        ctx.beginPath();
        ctx.arc(cx + r * 0.15, cy - r * 0.1, r * 0.2, 0, Math.PI * 2);
        ctx.fill();
        
        if (el.label) {
          ctx.shadowBlur = 0;
          ctx.fillStyle = 'white';
          ctx.font = `600 ${el.fontSize || 12}px 'Patrick Hand', 'Caveat', cursive`;
          ctx.textAlign = 'center';
          ctx.strokeStyle = '#4B0082';
          ctx.lineWidth = 1.75;
          ctx.strokeText(el.label, cx, cy + 5);
          ctx.fillText(el.label, cx, cy + 5);
        }
        break;
      }

      case 'dna': {
        // Draw DNA double helix
        const x = el.x || 0;
        const y = el.y || 0;
        const h = el.height || 100;
        const w = el.width || 40;
        
        // Draw two strands with 3D ribbon effect
        ctx.lineWidth = 3;
        
        // Strand 1 (blue)
        ctx.strokeStyle = '#3498db';
        ctx.beginPath();
        for (let i = 0; i <= h; i += 2) {
          const offset = Math.sin((i / h) * Math.PI * 4) * (w / 2);
          const px = x + w/2 + offset;
          const py = y + i;
          if (i === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.stroke();
        
        // Strand 2 (red) - opposite phase
        ctx.strokeStyle = '#e74c3c';
        ctx.beginPath();
        for (let i = 0; i <= h; i += 2) {
          const offset = Math.sin((i / h) * Math.PI * 4 + Math.PI) * (w / 2);
          const px = x + w/2 + offset;
          const py = y + i;
          if (i === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.stroke();
        
        // Base pairs (connecting lines)
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.lineWidth = 1.5;
        for (let i = 0; i <= h; i += 10) {
          const offset1 = Math.sin((i / h) * Math.PI * 4) * (w / 2);
          const offset2 = Math.sin((i / h) * Math.PI * 4 + Math.PI) * (w / 2);
          ctx.beginPath();
          ctx.moveTo(x + w/2 + offset1, y + i);
          ctx.lineTo(x + w/2 + offset2, y + i);
          ctx.stroke();
        }
        
        if (el.label) {
          ctx.shadowBlur = 0;
          ctx.fillStyle = color;
          ctx.font = `600 ${el.fontSize || 12}px 'Patrick Hand', 'Caveat', cursive`;
          ctx.textAlign = 'center';
          ctx.strokeStyle = 'rgba(255,255,255,0.85)';
          ctx.lineWidth = 1.5;
          ctx.strokeText(el.label, x + w/2, y + h + 15);
          ctx.fillText(el.label, x + w/2, y + h + 15);
        }
        break;
      }

      case 'membrane': {
        // Draw phospholipid bilayer membrane
        const x = el.x || 0;
        const y = el.y || 0;
        const w = el.width || 150;
        const h = el.height || 30;
        
        // Draw phospholipid heads (circles) and tails (lines)
        const headRadius = 4;
        const spacing = 12;
        
        // Top layer
        ctx.fillStyle = '#FF6B6B';
        for (let i = 0; i < w; i += spacing) {
          // Head
          ctx.beginPath();
          ctx.arc(x + i, y, headRadius, 0, Math.PI * 2);
          ctx.fill();
          // Tails
          ctx.strokeStyle = '#4ECDC4';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(x + i - 2, y + headRadius);
          ctx.lineTo(x + i - 2, y + h/2);
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(x + i + 2, y + headRadius);
          ctx.lineTo(x + i + 2, y + h/2);
          ctx.stroke();
        }
        
        // Bottom layer (inverted)
        for (let i = 0; i < w; i += spacing) {
          // Tails
          ctx.strokeStyle = '#4ECDC4';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(x + i - 2, y + h/2);
          ctx.lineTo(x + i - 2, y + h - headRadius);
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(x + i + 2, y + h/2);
          ctx.lineTo(x + i + 2, y + h - headRadius);
          ctx.stroke();
          // Head
          ctx.fillStyle = '#FF6B6B';
          ctx.beginPath();
          ctx.arc(x + i, y + h, headRadius, 0, Math.PI * 2);
          ctx.fill();
        }
        
        if (el.label) {
          ctx.shadowBlur = 0;
          ctx.fillStyle = color;
          ctx.font = `500 ${el.fontSize || 11}px 'Patrick Hand', 'Caveat', cursive`;
          ctx.textAlign = 'left';
          ctx.strokeStyle = 'rgba(255,255,255,0.85)';
          ctx.lineWidth = 1.25;
          ctx.strokeText(el.label, x, y + h + 15);
          ctx.fillText(el.label, x, y + h + 15);
        }
        break;
      }
    }

    // Reset shadow after each element
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;
    ctx.globalAlpha = 1;
  };

  // Hand-drawn effects
  const drawHandDrawnLine = (ctx: CanvasRenderingContext2D, x1: number, y1: number, x2: number, y2: number) => {
    const jitter = 1.5;
    ctx.moveTo(x1 + Math.random() * jitter, y1 + Math.random() * jitter);
    ctx.lineTo(x2 + Math.random() * jitter, y2 + Math.random() * jitter);
  };

  const drawHandDrawnRect = (ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number) => {
    const j = 1.2;
    ctx.moveTo(x + Math.random() * j, y + Math.random() * j);
    ctx.lineTo(x + w + Math.random() * j, y + Math.random() * j);
    ctx.lineTo(x + w + Math.random() * j, y + h + Math.random() * j);
    ctx.lineTo(x + Math.random() * j, y + h + Math.random() * j);
    ctx.closePath();
  };

  const drawHandDrawnCircle = (ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number) => {
    const points = 36;
    for (let i = 0; i <= points; i++) {
      const angle = (i / points) * Math.PI * 2;
      const jitter = Math.random() * 1.5;
      const px = cx + (r + jitter) * Math.cos(angle);
      const py = cy + (r + jitter) * Math.sin(angle);
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
  };

  if (!isVisible || (!drawCommands && !activeSchema && !boardContent)) return null;

  const hasActiveDrawCommands = drawCommands && drawCommands.length > 0;

  // ── MathBoard mode: render structured math/text content ──
  // Only show board if there are NO active draw commands (draw takes priority)
  if (!hasActiveDrawCommands && boardContent && boardContent.lines && boardContent.lines.length > 0) {
    return (
      <MathBoard
        lines={boardContent.lines}
        title={boardContent.title}
        isVisible={isVisible}
        onClose={onClose}
      />
    );
  }

  // ── Schema mode: render SVGSchemaViewer instead of canvas ──
  // Only show schema if there are NO active draw commands
  if (!hasActiveDrawCommands && activeSchema) {
    return (
      <div className="w-full h-full flex flex-col bg-white rounded-2xl overflow-hidden shadow-lg">
        {/* Toolbar */}
        <div className="shrink-0 flex items-center justify-between px-3 py-1.5 bg-gray-50 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full bg-red-400" />
              <div className="w-2 h-2 rounded-full bg-yellow-400" />
              <div className="w-2 h-2 rounded-full bg-green-400" />
            </div>
            <span className="text-gray-600 text-xs font-medium">
              Schéma interactif
            </span>
            <span className="text-indigo-500 text-xs truncate max-w-[50vw]">
              — {activeSchema.title}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-indigo-100 text-indigo-600 font-medium uppercase">
              {activeSchema.subject}
            </span>
            {onClose && (
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 text-xs px-2 py-0.5 rounded hover:bg-gray-100 transition-colors"
              >
                ✕
              </button>
            )}
          </div>
        </div>
        {/* SVG Schema Viewer */}
        <div className="flex-1 min-h-0 overflow-hidden">
          <SVGSchemaViewer
            schema={activeSchema}
            activeHighlights={activeHighlights || []}
            autoAnimate={true}
          />
        </div>
      </div>
    );
  }

  // ── Canvas draw mode (original) ──
  if (!drawCommands) return null;

  return (
    <div className="w-full h-full flex flex-col bg-[#0a0a18] rounded-2xl overflow-hidden">
      {/* Toolbar */}
      <div className="shrink-0 flex items-center justify-between px-3 py-1.5 bg-[#0c0c1d] border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <div className="w-2 h-2 rounded-full bg-red-500" />
            <div className="w-2 h-2 rounded-full bg-yellow-500" />
            <div className="w-2 h-2 rounded-full bg-green-500" />
          </div>
          <span className="text-white/70 text-xs font-medium">
            Tableau du professeur
          </span>
          {title && (
            <span className="text-indigo-400 text-xs truncate max-w-[50vw]">
              — {title}
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          {animating && (
            <span className="text-[11px] text-cyan-400 flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
              Le professeur dessine...
            </span>
          )}
          {drawCommands.length > 1 && (
            <span className="text-[11px] text-white/40">
              Étape {Math.min(currentStepIndex + 1, drawCommands.length)}/{drawCommands.length}
            </span>
          )}
          {onClose && (
            <button
              onClick={onClose}
              className="text-white/40 hover:text-white/80 text-xs px-2 py-0.5 rounded hover:bg-white/5 transition-colors"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Canvas area */}
      <div ref={containerRef} className="flex-1 relative overflow-hidden">
        <canvas
          ref={canvasRef}
          className="absolute inset-0 w-full h-full"
          style={{ imageRendering: 'auto' }}
        />

        {/* Color legend */}
        {drawnElements.length > 0 && (
          <div className="absolute bottom-3 right-3 bg-black/60 backdrop-blur-sm rounded-lg px-3 py-2 border border-white/10">
            <div className="flex items-center gap-2">
              {Array.from(new Set(drawnElements.map(e => e.color))).slice(0, 5).map((color, i) => (
                <div
                  key={i}
                  className="w-3 h-3 rounded-full border border-white/20"
                  style={{ backgroundColor: resolveColor(color) }}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const AIWhiteboard = memo(AIWhiteboardInner);
export default AIWhiteboard;
