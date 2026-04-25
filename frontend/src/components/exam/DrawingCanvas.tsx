import { useRef, useState, useEffect, useCallback } from 'react';
import { Undo2, Trash2 } from 'lucide-react';

interface Props {
  width?: number;
  height?: number;
  showGrid?: boolean;
  showAxes?: boolean;
  disabled?: boolean;
  onDrawingChange?: (dataUrl: string) => void;
}

const COLORS = [
  { value: '#1e293b', label: 'Noir' },
  { value: '#2563eb', label: 'Bleu' },
  { value: '#dc2626', label: 'Rouge' },
  { value: '#16a34a', label: 'Vert' },
  { value: '#9333ea', label: 'Violet' },
  { value: '#ea580c', label: 'Orange' },
];

const SIZES = [2, 3, 5];

export default function DrawingCanvas({
  width = 520,
  height = 280,
  showGrid = true,
  showAxes = true,
  disabled = false,
  onDrawingChange,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [color, setColor] = useState('#1e293b');
  const [lineWidth, setLineWidth] = useState(3);
  const [history, setHistory] = useState<ImageData[]>([]);
  const [canvasSize, setCanvasSize] = useState({ w: width, h: height });

  // Responsive canvas sizing
  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        const containerWidth = containerRef.current.clientWidth;
        const w = Math.min(containerWidth - 2, width);
        const h = Math.round((w / width) * height);
        setCanvasSize({ w, h });
      }
    };
    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, [width, height]);

  const drawBackground = useCallback((ctx: CanvasRenderingContext2D) => {
    const { w, h } = canvasSize;
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, w, h);

    if (showGrid) {
      const gridSize = 20;
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 0.5;
      for (let x = gridSize; x < w; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
      }
      for (let y = gridSize; y < h; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }
    }

    if (showAxes) {
      const cx = Math.round(w * 0.12);
      const cy = Math.round(h * 0.85);

      // Axes
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 1.5;

      // X axis
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(w - 20, cy);
      ctx.stroke();
      // X arrow
      ctx.beginPath();
      ctx.moveTo(w - 20, cy);
      ctx.lineTo(w - 28, cy - 5);
      ctx.moveTo(w - 20, cy);
      ctx.lineTo(w - 28, cy + 5);
      ctx.stroke();

      // Y axis
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx, 20);
      ctx.stroke();
      // Y arrow
      ctx.beginPath();
      ctx.moveTo(cx, 20);
      ctx.lineTo(cx - 5, 28);
      ctx.moveTo(cx, 20);
      ctx.lineTo(cx + 5, 28);
      ctx.stroke();

      // Labels
      ctx.fillStyle = '#64748b';
      ctx.font = 'bold 12px sans-serif';
      ctx.fillText('x', w - 18, cy + 16);
      ctx.fillText('y', cx - 16, 24);
      ctx.fillText('O', cx - 14, cy + 16);

      // Tick marks
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 1;
      const tickSpacing = 40;
      for (let x = cx + tickSpacing; x < w - 30; x += tickSpacing) {
        ctx.beginPath();
        ctx.moveTo(x, cy - 3);
        ctx.lineTo(x, cy + 3);
        ctx.stroke();
      }
      for (let y = cy - tickSpacing; y > 30; y -= tickSpacing) {
        ctx.beginPath();
        ctx.moveTo(cx - 3, y);
        ctx.lineTo(cx + 3, y);
        ctx.stroke();
      }
    }
  }, [canvasSize, showGrid, showAxes]);

  // Init canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    canvas.width = canvasSize.w;
    canvas.height = canvasSize.h;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    drawBackground(ctx);
    setHistory([ctx.getImageData(0, 0, canvasSize.w, canvasSize.h)]);
  }, [canvasSize, drawBackground]);

  const getPos = (e: React.MouseEvent | React.TouchEvent) => {
    const canvas = canvasRef.current!;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    if ('touches' in e) {
      const touch = e.touches[0] || e.changedTouches[0];
      return {
        x: (touch.clientX - rect.left) * scaleX,
        y: (touch.clientY - rect.top) * scaleY,
      };
    }
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY,
    };
  };

  const startDrawing = (e: React.MouseEvent | React.TouchEvent) => {
    if (disabled) return;
    e.preventDefault();
    const ctx = canvasRef.current?.getContext('2d');
    if (!ctx) return;
    const pos = getPos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
    ctx.strokeStyle = color;
    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    setIsDrawing(true);
  };

  const draw = (e: React.MouseEvent | React.TouchEvent) => {
    if (!isDrawing || disabled) return;
    e.preventDefault();
    const ctx = canvasRef.current?.getContext('2d');
    if (!ctx) return;
    const pos = getPos(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
  };

  const stopDrawing = () => {
    if (!isDrawing) return;
    setIsDrawing(false);
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx) return;
    ctx.closePath();
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    setHistory((prev) => [...prev, imageData]);
    onDrawingChange?.(canvas.toDataURL('image/png'));
  };

  const undo = () => {
    if (history.length <= 1) return;
    const ctx = canvasRef.current?.getContext('2d');
    if (!ctx) return;
    const newHistory = history.slice(0, -1);
    setHistory(newHistory);
    ctx.putImageData(newHistory[newHistory.length - 1], 0, 0);
    onDrawingChange?.(canvasRef.current!.toDataURL('image/png'));
  };

  const clear = () => {
    const ctx = canvasRef.current?.getContext('2d');
    if (!ctx) return;
    drawBackground(ctx);
    const imageData = ctx.getImageData(0, 0, canvasSize.w, canvasSize.h);
    setHistory([imageData]);
    onDrawingChange?.('');
  };

  return (
    <div ref={containerRef} className="space-y-2.5">
      {/* Toolbar */}
      <div className="flex items-center gap-2 flex-wrap">
        {/* Colors */}
        <div className="flex items-center gap-1 bg-slate-50 rounded-lg p-1 border border-slate-200">
          {COLORS.map((c) => (
            <button
              key={c.value}
              title={c.label}
              onClick={() => setColor(c.value)}
              className={`w-6 h-6 rounded-md transition-all ${color === c.value ? 'ring-2 ring-offset-1 ring-blue-500 scale-110' : 'hover:scale-105'}`}
              style={{ backgroundColor: c.value }}
            />
          ))}
        </div>

        {/* Sizes */}
        <div className="flex items-center gap-1 bg-slate-50 rounded-lg p-1 border border-slate-200">
          {SIZES.map((s, i) => (
            <button
              key={s}
              title={['Fin', 'Normal', 'Épais'][i]}
              onClick={() => setLineWidth(s)}
              className={`w-7 h-7 rounded-md flex items-center justify-center transition-all ${lineWidth === s ? 'bg-white shadow-sm border border-slate-200' : 'hover:bg-white/50'}`}
            >
              <span className="rounded-full bg-current" style={{ width: s + 2, height: s + 2, color }} />
            </button>
          ))}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-1 ml-auto">
          <button
            onClick={undo}
            disabled={history.length <= 1}
            className="flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium text-slate-500 bg-slate-50 border border-slate-200 rounded-lg hover:bg-white disabled:opacity-30 transition-all"
          >
            <Undo2 className="w-3.5 h-3.5" /> Annuler
          </button>
          <button
            onClick={clear}
            className="flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium text-red-500 bg-red-50 border border-red-200 rounded-lg hover:bg-red-100 transition-all"
          >
            <Trash2 className="w-3.5 h-3.5" /> Effacer
          </button>
        </div>
      </div>

      {/* Canvas */}
      <div className="border border-slate-200 rounded-xl overflow-hidden bg-white shadow-inner">
        <canvas
          ref={canvasRef}
          className="w-full cursor-crosshair touch-none"
          style={{ height: `${canvasSize.h}px` }}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseLeave={stopDrawing}
          onTouchStart={startDrawing}
          onTouchMove={draw}
          onTouchEnd={stopDrawing}
        />
      </div>

      <p className="text-[10px] text-slate-400 text-center">
        Dessinez directement sur le canvas · Utilisez les couleurs pour différencier les éléments
      </p>
    </div>
  );
}
