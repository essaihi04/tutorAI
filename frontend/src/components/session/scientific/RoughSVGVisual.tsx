import { useId } from 'react';
import RoughShape from './RoughShape';
import type { RoughSVGElementSpec, RoughSVGVisualSpec, ScientificPoint } from './types';

interface RoughSVGVisualProps {
  spec: RoughSVGVisualSpec;
  /** La figure se pose SUR le tableau : ni cadre, ni fond peint. */
  transparent?: boolean;
}

const COLORS: Record<string, string> = {
  red: '#ef4444', blue: '#3b82f6', green: '#22c55e', orange: '#f97316',
  purple: '#a855f7', cyan: '#06b6d4', yellow: '#eab308', white: '#e2e8f0',
  black: '#0f172a', gray: '#64748b', grey: '#64748b',
};

function resolveColor(color: string | undefined, fallback: string): string {
  if (!color) return fallback;
  return COLORS[color] || color;
}

function arrowHead(points: ScientificPoint[]): ScientificPoint[] {
  if (points.length < 2) return [];
  const start = points[points.length - 2];
  const end = points[points.length - 1];
  const angle = Math.atan2(end.y - start.y, end.x - start.x);
  const size = 11;
  return [
    end,
    { x: end.x - size * Math.cos(angle - Math.PI / 6), y: end.y - size * Math.sin(angle - Math.PI / 6) },
    { x: end.x - size * Math.cos(angle + Math.PI / 6), y: end.y - size * Math.sin(angle + Math.PI / 6) },
  ];
}

function RenderElement({ element, index }: { element: RoughSVGElementSpec; index: number }) {
  const stroke = resolveColor(element.color, '#cbd5e1');
  const fill = element.fill ? resolveColor(element.fill, element.fill) : undefined;
  const strokeWidth = element.strokeWidth || 2.2;
  const points = element.points || [];
  const dashStyle = element.dashed ? { strokeDasharray: '7 6' } : undefined;
  const seed = index + 17;

  if (element.type === 'text') {
    return (
      <text
        x={element.x}
        y={element.y}
        fill={stroke}
        fontSize={element.fontSize || 16}
        fontWeight={element.fontSize && element.fontSize >= 22 ? 700 : 600}
        textAnchor={element.align || 'middle'}
        fontFamily="'Patrick Hand', 'Segoe Print', system-ui"
      >
        {element.text}
      </text>
    );
  }

  if (element.type === 'rect') {
    return <RoughShape kind="rectangle" x={element.x} y={element.y} width={element.width} height={element.height}
      stroke={stroke} strokeWidth={strokeWidth} fill={fill} seed={seed} style={dashStyle} />;
  }
  if (element.type === 'circle') {
    return <RoughShape kind="circle" x={element.x} y={element.y} radius={element.radius}
      stroke={stroke} strokeWidth={strokeWidth} fill={fill} seed={seed} style={dashStyle} />;
  }
  if (element.type === 'ellipse') {
    return <RoughShape kind="ellipse" x={element.x} y={element.y} width={(element.radiusX || 1) * 2}
      height={(element.radiusY || 1) * 2} stroke={stroke} strokeWidth={strokeWidth} fill={fill}
      seed={seed} style={dashStyle} />;
  }
  if (element.type === 'polygon') {
    return <RoughShape kind="polygon" points={points} stroke={stroke} strokeWidth={strokeWidth}
      fill={fill} seed={seed} style={dashStyle} />;
  }
  if (element.type === 'polyline') {
    return <RoughShape kind="linearPath" points={points} stroke={stroke} strokeWidth={strokeWidth}
      seed={seed} style={dashStyle} />;
  }
  if (element.type === 'arrow') {
    return (
      <g>
        <RoughShape kind="linearPath" points={points} stroke={stroke} strokeWidth={strokeWidth}
          seed={seed} style={dashStyle} />
        <RoughShape kind="polygon" points={arrowHead(points)} stroke={stroke} strokeWidth={1.4}
          fill={stroke} seed={seed + 1000} />
      </g>
    );
  }
  return <RoughShape kind="line" points={points} stroke={stroke} strokeWidth={strokeWidth}
    seed={seed} style={dashStyle} />;
}


/**
 * Le cadre de la figure. Sur le tableau il n'y en a pas : la figure est
 * dessinee sur l'ardoise, pas collee dessus.
 */
function CADRE_FIGURE(transparent?: boolean): string {
  return transparent
    ? 'my-0 h-full w-full p-0'
    : 'my-3 overflow-hidden rounded-xl border border-white/10 bg-slate-950/70 p-2';
}

export default function RoughSVGVisual({ spec, transparent }: RoughSVGVisualProps) {
  const titleId = `rough-title-${useId().replace(/[^a-zA-Z0-9_-]/g, '')}`;
  const width = spec.width || 800;
  const height = spec.height || 440;

  return (
    <figure className={CADRE_FIGURE(transparent)}>
      {spec.title && <figcaption id={titleId} className="px-2 pb-2 text-sm font-medium text-cyan-200">{spec.title}</figcaption>}
      <svg
        viewBox={`0 0 ${width} ${height}`}
        className="max-h-[440px] w-full rounded-lg"
        style={{ background: transparent ? 'transparent' : resolveColor(spec.background, '#07111f') }}
        role="img"
        aria-labelledby={spec.title ? titleId : undefined}
        aria-label={!spec.title ? spec.description || 'Schéma scientifique' : undefined}
        preserveAspectRatio="xMidYMid meet"
      >
        {spec.elements.map((element, index) => (
          <RenderElement key={element.id || `${element.type}-${index}`} element={element} index={index} />
        ))}
      </svg>
      {spec.description && <p className="px-2 pt-2 text-xs text-slate-300">{spec.description}</p>}
      {Boolean(spec.legend?.length) && (
        <ul className="flex flex-wrap gap-x-4 gap-y-1 px-2 pt-2 text-xs text-slate-200" aria-label="Légende">
          {spec.legend?.map(item => (
            <li key={`${item.color}-${item.label}`} className="flex items-center gap-1.5">
              <span className="h-2.5 w-2.5 rounded-full" style={{ background: resolveColor(item.color, item.color) }} />
              {item.label}
            </li>
          ))}
        </ul>
      )}
    </figure>
  );
}
