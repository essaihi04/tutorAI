import type { ReactNode } from 'react';

interface PyruvateMitochondrionImageVisualProps {
  step: number;
  transparent?: boolean;
}

const MITOCHONDRION_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_3d_sans_legendes.png';

function arrowHead(x1: number, y1: number, x2: number, y2: number) {
  const angle = Math.atan2(y2 - y1, x2 - x1);
  const size = 13;
  return `${x2},${y2} ${x2 - size * Math.cos(angle - Math.PI / 6)},${y2 - size * Math.sin(angle - Math.PI / 6)} ${x2 - size * Math.cos(angle + Math.PI / 6)},${y2 - size * Math.sin(angle + Math.PI / 6)}`;
}

function Arrow({ x1, y1, x2, y2, color }: { x1: number; y1: number; x2: number; y2: number; color: string }) {
  return (
    <g>
      <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth="6" strokeLinecap="round" />
      <polygon points={arrowHead(x1, y1, x2, y2)} fill={color} />
    </g>
  );
}

function PathArrow({ points, color }: { points: Array<[number, number]>; color: string }) {
  const previous = points[points.length - 2];
  const end = points[points.length - 1];
  return (
    <g>
      <polyline points={points.map(([x, y]) => `${x},${y}`).join(' ')} fill="none" stroke={color} strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
      <polygon points={arrowHead(previous[0], previous[1], end[0], end[1])} fill={color} />
    </g>
  );
}

function CarbonGroup({ x, y, count, color, label }: { x: number; y: number; count: number; color: string; label: string }) {
  return (
    <g>
      {Array.from({ length: count }, (_, index) => (
        <g key={`${label}-${index}`}>
          <circle cx={x + index * 36} cy={y} r="18" fill="#0b1625" stroke={color} strokeWidth="4" />
          <text x={x + index * 36} y={y + 6} textAnchor="middle" fill="#fff" fontSize="16" fontWeight="700">C</text>
        </g>
      ))}
      <text x={x + ((count - 1) * 36) / 2} y={y + 42} textAnchor="middle" fill={color} fontSize="17" fontWeight="700">{label}</text>
    </g>
  );
}

function Tag({ x, y, children, color = '#f8fafc' }: { x: number; y: number; children: ReactNode; color?: string }) {
  return (
    <g>
      <rect x={x - 76} y={y - 26} width="152" height="42" rx="12" fill="#06111dcc" stroke={`${color}99`} strokeWidth="2" />
      <text x={x} y={y + 2} textAnchor="middle" fill={color} fontSize="18" fontWeight="700">{children}</text>
    </g>
  );
}

export default function PyruvateMitochondrionImageVisual({ step, transparent }: PyruvateMitochondrionImageVisualProps) {
  const current = Math.max(0, Math.min(8, Math.round(step)));
  const messages = [
    'La glycolyse fournit un pyruvate à 3 carbones dans le cytoplasme.',
    'Le pyruvate se dirige vers la mitochondrie.',
    'Il franchit la membrane externe puis la membrane interne.',
    'Le pyruvate atteint la matrice mitochondriale.',
    'Un carbone est libéré sous forme de CO₂.',
    'Le NAD⁺ est réduit en NADH,H⁺.',
    'La coenzyme A se fixe au groupement acétyle.',
    'L’acétyl-CoA est prêt à entrer dans le cycle de Krebs.',
    'Bilan : 1 acétyl-CoA + 1 CO₂ + 1 NADH,H⁺ par pyruvate.',
  ];

  return (
    <figure className={transparent ? 'relative my-0 h-full w-full p-0' : 'relative my-3 overflow-hidden rounded-xl border border-white/10 bg-slate-950/70 p-2'}>
      <div className="relative mx-auto w-full max-w-[980px] overflow-hidden rounded-lg" style={{ aspectRatio: '16 / 9' }}>
        <img src={MITOCHONDRION_IMAGE} alt="Mitochondrie en coupe montrant les crêtes et la matrice" className="absolute inset-0 h-full w-full object-cover" />
        <svg viewBox="0 0 900 506" className="absolute inset-0 h-full w-full" role="img" aria-label="Trajet du pyruvate dans une mitochondrie">
          <Tag x={120} y={54} color="#67e8f9">Cytoplasme</Tag>
          <Tag x={650} y={54} color="#86efac">Matrice</Tag>

          {current === 0 && <CarbonGroup x={92} y={268} count={3} color="#fb7185" label="Pyruvate · 3C" />}
          {current >= 1 && <Arrow x1={150} y1={268} x2={265} y2={268} color="#fb7185" />}
          {current === 1 && <CarbonGroup x={244} y={268} count={3} color="#fb7185" label="Pyruvate · 3C" />}
          {current >= 2 && <Arrow x1={280} y1={268} x2={390} y2={268} color="#fb7185" />}
          {current === 2 && <CarbonGroup x={354} y={268} count={3} color="#fb7185" label="Transport" />}
          {current === 3 && <CarbonGroup x={454} y={268} count={3} color="#fb7185" label="Pyruvate · 3C" />}

          {current >= 4 && (
            <>
              <CarbonGroup x={430} y={268} count={2} color="#fbbf24" label={current >= 6 ? 'Acétyl-CoA · 2C' : 'Résidu · 2C'} />
              <PathArrow points={[[484, 246], [470, 126], [788, 88]]} color="#f97316" />
              <text x="820" y="31" textAnchor="middle" fill="#fed7aa" fontSize="17" fontWeight="700">CO₂ rejeté</text>
              <circle cx="820" cy="70" r="27" fill="#7c2d12" stroke="#f97316" strokeWidth="4" />
              <text x="820" y="77" textAnchor="middle" fill="#fff" fontSize="17" fontWeight="700">CO₂</text>
            </>
          )}
          {current >= 5 && (
            <>
              <Tag x={420} y={436} color="#c084fc">NAD⁺</Tag>
              <Arrow x1={500} y1={410} x2={610} y2={410} color="#c084fc" />
              <Tag x={688} y={436} color="#e9d5ff">NADH,H⁺</Tag>
            </>
          )}
          {current >= 6 && <Tag x={360} y={176} color="#4ade80">CoA</Tag>}
          {current >= 7 && (
            <>
              <Arrow x1={484} y1={282} x2={506} y2={252} color="#4ade80" />
              <circle cx="560" cy="220" r="54" fill="#0b1625cc" stroke="#4ade80" strokeWidth="4" strokeDasharray="10 8" />
              <text x="560" y="215" textAnchor="middle" fill="#bbf7d0" fontSize="17" fontWeight="700">Cycle de</text>
              <text x="560" y="238" textAnchor="middle" fill="#bbf7d0" fontSize="19" fontWeight="700">Krebs</text>
            </>
          )}
          <rect x="28" y="461" width="844" height="32" rx="10" fill="#06111dcc" stroke="#67e8f955" strokeWidth="1.5" />
          <text x="450" y="483" textAnchor="middle" fill="#f8fafc" fontSize="16" fontWeight="600">{messages[current]}</text>
        </svg>
      </div>
      {!transparent && <figcaption className="px-2 pt-2 text-xs text-slate-300">Image réaliste de mitochondrie avec animation du trajet du pyruvate et de sa transformation en acétyl-CoA.</figcaption>}
    </figure>
  );
}
