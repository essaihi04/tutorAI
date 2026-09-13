import { useId, useState } from 'react';
import './vesiclePreparation.css';

const VESICLE_PREPARATION_STAGES = [
  { title: 'Une mitochondrie isolée', lines: ['La membrane interne forme les crêtes.', 'Elle porte les sphères pédonculées, du côté de la matrice.'] },
  { title: 'Les ultrasons fragmentent les membranes', lines: ['Les membranes se rompent en petits fragments.', 'On suit ici les fragments de membrane interne.'] },
  { title: 'Les fragments se referment en vésicules', lines: ['On obtient des vésicules retournées.', 'Les sphères pédonculées sont maintenant tournées vers l’extérieur.'] },
  { title: 'Les vésicules sont placées dans une solution tampon', lines: ['pHi : pH à l’intérieur de la vésicule.  •  pHe : pH du milieu extérieur.', 'On peut maintenant comparer les gradients de pH.'] },
] as const;

/** Dessin déterministe du protocole, avant les résultats du document 11. */
export default function VesiclePreparationVisual({ step, running }: { step: number; running: boolean }) {
  const id = useId();
  // Une étape ouverte manuellement est immédiatement lisible. Une pause en
  // lecture automatique, elle, conserve exactement la progression du mouvement.
  const [animateEntrance] = useState(running);
  const stage = VESICLE_PREPARATION_STAGES[Math.max(0, Math.min(3, step))];
  const arrowId = `${id}-arrow`;

  function arrow(x1: number, x2: number) {
    return <path d={`M ${x1} 172 H ${x2}`} fill="none" stroke="#67e8f9" strokeWidth="3" markerEnd={`url(#${arrowId})`} />;
  }

  function vesicle(x: number, y: number, radius: number, label?: string) {
    return (
      <g transform={`translate(${x} ${y})`}>
        <circle r={radius} fill="#102c32" stroke="#c4b5fd" strokeWidth="4" />
        <circle r={radius - 7} fill="none" stroke="#8b7bb4" strokeWidth="2" />
        {Array.from({ length: 12 }, (_, index) => (
          <g key={index} transform={`rotate(${index * 30})`} stroke="#93c5fd" strokeWidth="2.5">
            <path d={`M 0 ${-radius} v -10`} />
            <circle cy={-radius - 14} r="5" fill="#93c5fd" />
          </g>
        ))}
        {label && <text textAnchor="middle" y="8" fill="#fde68a" fontSize="28" fontWeight="700">{label}</text>}
      </g>
    );
  }

  return (
    <div className="vesicle-preparation flex h-full min-h-[310px] items-center" data-running={running} data-preparation-step={step}>
      <svg viewBox="0 0 900 480" className="w-full" role="img" aria-labelledby={`${id}-title ${id}-description`}>
        <title id={`${id}-title`}>Préparation des vésicules retournées — étape {step + 1} sur 4</title>
        <desc id={`${id}-description`}>{stage.title}. {stage.lines.join(' ')}</desc>
        <defs>
          <marker id={arrowId} viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10" fill="#67e8f9" />
          </marker>
        </defs>
        <g fontFamily="'Patrick Hand', 'Segoe Print', system-ui" fill="#e2e8f0">
          <text x="30" y="34" fill="#67e8f9" fontSize="26" fontWeight="700">Avant l’expérience : préparer les vésicules</text>

          <g transform="translate(105 172)">
            <g className={step === 1 ? 'vesicle-shake' : undefined}>
              <path d="M -55 -53 C -93 -15 -45 25 -27 57 C -4 94 78 59 63 20 C 50 -12 11 -29 9 -56 C 6 -86 -34 -80 -55 -53 Z" fill="#fef08a" fillOpacity=".14" stroke="#fde68a" strokeWidth="3" />
              <path d="M -49 -46 C -72 -21 -39 -10 -42 2 L -17 -13 Q -5 -14 -12 -2 L -30 18 L -18 36 L 9 10 Q 21 3 17 16 L -4 47 L 14 57 L 37 31 Q 46 22 44 37 C 70 12 1 -23 0 -52 C -1 -71 -33 -68 -49 -46 Z" fill="none" stroke="#c4b5fd" strokeWidth="4" />
              {[[-42, 2, 90], [0, -52, -125], [-18, 36, 55], [14, 57, 20]].map(([x, y, rotation], index) => (
                <g key={index} transform={`translate(${x} ${y}) rotate(${rotation})`} stroke="#93c5fd" strokeWidth="2.5">
                  <path d="M 0 0 v -10" /><circle cy="-14" r="4" fill="#93c5fd" />
                </g>
              ))}
            </g>
          </g>
          <text x="105" y="285" textAnchor="middle" fontSize="25">Mitochondrie</text>

          {step >= 1 && (
            <g>
              <text x="215" y="82" textAnchor="middle" fill="#fde68a" fontSize="24">Ultrasons</text>
              <path d="M 200 94 l 19 0 -7 15 16 0 -24 28 6 -19 -15 0 Z" fill="#fbbf24" />
              {[0, 1, 2].map(index => (
                <path key={index} className={step === 1 ? 'vesicle-wave' : undefined} style={{ animationDelay: `${index * 220}ms` }} d={`M ${172 + index * 13} 133 q -13 25 0 49`} fill="none" stroke="#fde68a" strokeWidth="2" />
              ))}
              {arrow(190, 248)}
              <g transform="translate(300 170)" className={step === 1 && animateEntrance ? 'vesicle-fragments' : undefined}>
                {[-1, 0, 1].map((index) => (
                  <g key={index} transform={`translate(${index === 0 ? 18 : -8} ${index * 47}) rotate(${index * 32})`}>
                    <path d="M -28 10 Q 0 -15 28 10" fill="none" stroke="#c4b5fd" strokeWidth="5" />
                    {[-20, 0, 20].map(x => (
                      <g key={x} transform={`translate(${x} ${x === 0 ? -2 : 5})`} stroke="#93c5fd" strokeWidth="2.5">
                        <path d="M 0 0 v -12" /><circle cy="-16" r="4" fill="#93c5fd" />
                      </g>
                    ))}
                  </g>
                ))}
              </g>
            </g>
          )}
          <text x="300" y="285" textAnchor="middle" fontSize="24" opacity={step >= 1 ? 1 : .35}>Fragments de</text>
          <text x="300" y="312" textAnchor="middle" fontSize="24" opacity={step >= 1 ? 1 : .35}>membrane interne</text>

          {step >= 2 && (
            <g>
              {arrow(353, 414)}
              <text x="493" y="82" textAnchor="middle" fill="#c4b5fd" fontSize="24">Repliement</text>
              <g className={step === 2 && animateEntrance ? 'vesicle-close' : undefined}>
                {vesicle(474, 144, 27)}
                {vesicle(527, 216, 25)}
                {vesicle(444, 226, 17)}
              </g>
            </g>
          )}
          <text x="490" y="285" textAnchor="middle" fontSize="24" opacity={step >= 2 ? 1 : .35}>Vésicules</text>
          <text x="490" y="312" textAnchor="middle" fontSize="24" opacity={step >= 2 ? 1 : .35}>retournées</text>

          {step >= 3 && (
            <g className={animateEntrance ? 'vesicle-buffer' : undefined}>
              {arrow(567, 626)}
              <text x="749" y="76" textAnchor="middle" fill="#67e8f9" fontSize="24">Solution tampon</text>
              <path d="M 644 91 H 854 L 845 108 V 281 Q 845 294 831 294 H 666 Q 652 294 652 280 V 108 Z" fill="#67e8f9" fillOpacity=".06" stroke="#cbd5e1" strokeWidth="3" />
              <path d="M 654 131 Q 677 126 697 131 T 740 131 T 784 131 T 843 131" fill="none" stroke="#67e8f9" strokeWidth="2" />
              <text x="749" y="119" textAnchor="middle" fill="#67e8f9" fontSize="24">pHe</text>
              {vesicle(749, 213, 51, 'pHi')}
              <path d="M 814 213 H 869 V 326 H 799" fill="none" stroke="#93c5fd" strokeWidth="1.5" />
              <text x="792" y="331" textAnchor="end" fill="#93c5fd" fontSize="22">Sphères vers l’extérieur</text>
            </g>
          )}
          {step < 3 && <text x="749" y="285" textAnchor="middle" fontSize="24" opacity=".35">Solution tampon</text>}
          <path d="M 30 356 H 870" stroke="#94a3b8" strokeOpacity=".25" />
          <text x="30" y="390" fill="#fde68a" fontSize="26" fontWeight="700">{step + 1}. {stage.title}</text>
          <text x="30" y="427" fontSize="23">{stage.lines[0]}</text>
          <text x="30" y="459" fontSize="23">{stage.lines[1]}</text>
        </g>
      </svg>
    </div>
  );
}
