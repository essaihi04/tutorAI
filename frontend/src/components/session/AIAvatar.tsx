import { useEffect, useRef } from 'react';

interface AIAvatarProps {
  isSpeaking: boolean;
  isProcessing: boolean;
  processingStage?: string;
}

export default function AIAvatar({ isSpeaking, isProcessing, processingStage }: AIAvatarProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animFrameRef = useRef<number>(0);

  // Determine state for visual
  const state = isSpeaking ? 'speaking' : isProcessing ? 'thinking' : 'idle';

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d')!;
    const size = 220;
    canvas.width = size * 2; // retina
    canvas.height = size * 2;
    canvas.style.width = `${size}px`;
    canvas.style.height = `${size}px`;
    ctx.scale(2, 2);

    const cx = size / 2;
    const cy = size / 2;
    let t = 0;

    const draw = () => {
      t += 0.02;
      ctx.clearRect(0, 0, size, size);

      // Color schemes per state
      const colors = {
        idle: { core: '#6366f1', ring: '#818cf8', glow: 'rgba(99,102,241,0.15)', particle: '#a5b4fc' },
        speaking: { core: '#06b6d4', ring: '#22d3ee', glow: 'rgba(6,182,212,0.25)', particle: '#67e8f9' },
        thinking: { core: '#f59e0b', ring: '#fbbf24', glow: 'rgba(245,158,11,0.2)', particle: '#fcd34d' },
      };
      const c = colors[state];

      // Outer glow
      const glowRadius = state === 'idle' ? 85 : 85 + Math.sin(t * 2) * 8;
      const glow = ctx.createRadialGradient(cx, cy, 30, cx, cy, glowRadius);
      glow.addColorStop(0, c.glow);
      glow.addColorStop(1, 'transparent');
      ctx.fillStyle = glow;
      ctx.fillRect(0, 0, size, size);

      // Orbiting rings (3 rings)
      const ringCount = 3;
      for (let r = 0; r < ringCount; r++) {
        const radius = 42 + r * 16;
        const speed = state === 'idle' ? 0.3 : state === 'speaking' ? 1.2 : 0.7;
        const waveAmp = state === 'speaking' ? 6 + r * 2 : state === 'thinking' ? 3 + r : 1;
        const segments = 120;

        ctx.beginPath();
        for (let i = 0; i <= segments; i++) {
          const angle = (i / segments) * Math.PI * 2;
          const wave = Math.sin(angle * (4 + r) + t * speed * (r + 1)) * waveAmp;
          const wave2 = Math.cos(angle * (3 + r * 2) + t * speed * 1.5) * (waveAmp * 0.5);
          const dist = radius + wave + wave2;
          const x = cx + Math.cos(angle) * dist;
          const y = cy + Math.sin(angle) * dist;
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = c.ring;
        ctx.globalAlpha = 0.3 + (r === 0 ? 0.3 : 0) + (state === 'speaking' ? 0.15 : 0);
        ctx.lineWidth = state === 'speaking' ? 2 : 1.2;
        ctx.stroke();
        ctx.globalAlpha = 1;
      }

      // Core orb
      const coreRadius = state === 'speaking' ? 26 + Math.sin(t * 4) * 4 : state === 'thinking' ? 24 + Math.sin(t * 2) * 2 : 24;
      const coreGrad = ctx.createRadialGradient(cx - 5, cy - 5, 2, cx, cy, coreRadius);
      coreGrad.addColorStop(0, '#fff');
      coreGrad.addColorStop(0.3, c.core);
      coreGrad.addColorStop(1, 'rgba(0,0,0,0.3)');
      ctx.beginPath();
      ctx.arc(cx, cy, coreRadius, 0, Math.PI * 2);
      ctx.fillStyle = coreGrad;
      ctx.fill();

      // Inner glow ring
      ctx.beginPath();
      ctx.arc(cx, cy, coreRadius + 3, 0, Math.PI * 2);
      ctx.strokeStyle = c.ring;
      ctx.globalAlpha = 0.5 + Math.sin(t * 3) * 0.2;
      ctx.lineWidth = 1.5;
      ctx.stroke();
      ctx.globalAlpha = 1;

      // Floating particles
      const particleCount = state === 'speaking' ? 12 : state === 'thinking' ? 8 : 4;
      for (let i = 0; i < particleCount; i++) {
        const angle = (i / particleCount) * Math.PI * 2 + t * 0.5;
        const dist = 55 + Math.sin(t * 1.5 + i * 1.3) * 20;
        const px = cx + Math.cos(angle) * dist;
        const py = cy + Math.sin(angle) * dist;
        const pSize = 1.5 + Math.sin(t * 2 + i) * 0.8;
        ctx.beginPath();
        ctx.arc(px, py, pSize, 0, Math.PI * 2);
        ctx.fillStyle = c.particle;
        ctx.globalAlpha = 0.4 + Math.sin(t + i) * 0.3;
        ctx.fill();
        ctx.globalAlpha = 1;
      }

      // Speaking wave bars (horizontal waveform at center)
      if (state === 'speaking') {
        const barCount = 24;
        const barWidth = 2;
        const totalWidth = barCount * (barWidth + 2);
        const startX = cx - totalWidth / 2;
        for (let i = 0; i < barCount; i++) {
          const h = 3 + Math.abs(Math.sin(t * 6 + i * 0.5)) * 10 + Math.random() * 3;
          const bx = startX + i * (barWidth + 2);
          ctx.fillStyle = c.ring;
          ctx.globalAlpha = 0.6;
          ctx.fillRect(bx, cy - h / 2, barWidth, h);
        }
        ctx.globalAlpha = 1;
      }

      animFrameRef.current = requestAnimationFrame(draw);
    };

    draw();
    return () => cancelAnimationFrame(animFrameRef.current);
  }, [state]);

  const statusLabel = isSpeaking
    ? 'Je parle...'
    : isProcessing
      ? processingStage === 'stt' ? 'Je t\'écoute...' : processingStage === 'tts' ? 'Préparation audio...' : 'Je réfléchis...'
      : 'Prêt';

  const statusColor = isSpeaking ? 'text-cyan-400' : isProcessing ? 'text-amber-400' : 'text-indigo-400';

  return (
    <div className="flex flex-col items-center select-none">
      <div className="relative">
        <canvas ref={canvasRef} className="drop-shadow-2xl" />
      </div>
      <p className={`mt-1 text-sm font-semibold tracking-wide ${statusColor} transition-colors duration-500`}>
        {statusLabel}
      </p>
    </div>
  );
}
