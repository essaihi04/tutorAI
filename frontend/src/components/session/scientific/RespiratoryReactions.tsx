import type { CSSProperties, KeyboardEvent } from 'react';

const activate = (event: KeyboardEvent<SVGGElement>, action: () => void) => {
  if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); action(); }
};

function Incoming({ dx, dy, label, delay = 0 }: { dx: number; dy: number; label: string; delay?: number }) {
  return <g className="rc-incoming" style={{ '--dx': `${dx}px`, '--dy': `${dy}px`, animationDelay: `${delay}s` } as CSSProperties}>
    <circle r="12" fill={label === 'e⁻' ? '#42edff' : '#ff73c6'} />
    <text textAnchor="middle" y="5" fontSize="14" fontWeight="900" fill="#102523">{label}</text>
  </g>;
}

function Water({ x }: { x: number }) {
  return <g transform={`translate(${x} 0)`}>
    <path d="M 0 0 L -23 22 M 0 0 L 23 22" stroke="#dcfcff" strokeWidth="5" />
    <circle r="19" fill="#ff866e" />
    <circle cx="-23" cy="22" r="12" fill="#dcfcff" />
    <circle cx="23" cy="22" r="12" fill="#dcfcff" />
  </g>;
}

/** One whole O₂ consumes TWO pairs of electrons and forms TWO waters.
 * This local molecular event is not the per-coenzyme ATP accounting unit.
 */
export function OxygenReaction({ step, onReplay }: { step: number; onReplay: () => void }) {
  const arrived = step >= 8;
  return <g transform="translate(650 367)" role="button" tabIndex={0} className="rc-reaction"
    aria-label="Rejouer : O₂ attend les électrons puis forme deux molécules d’eau" onClick={onReplay} onKeyDown={event => activate(event, onReplay)}
    data-reaction="oxygen" data-reaction-state={arrived ? 'water' : step === 7 ? 'receiving' : 'waiting'}>
    <title>Cliquer pour rejouer : O₂ reçoit quatre électrons et quatre H⁺ de la matrice, puis forme deux H₂O.</title>
    <rect x="-88" y="-45" width="176" height="108" rx="18" className="rc-reaction-hit" />
    {!arrived ? <g>
      <path d="M -19 -4 H 19 M -19 4 H 19" stroke="#ffb0a1" strokeWidth="5" />
      <circle cx="-20" r="22" fill="#ff866e" /><circle cx="20" r="22" fill="#ff866e" />
      <text y="56" textAnchor="middle" fontSize="27" fontWeight="800" fill="#ffb0a1">O₂</text>
    </g> : <g className="rc-product">
      <Water x={-43} /><Water x={43} />
      {[-43, 43].map(x => <text key={x} x={x} y="61" textAnchor="middle" fontSize="25" fontWeight="800" fill="#dcfcff">H₂O</text>)}
    </g>}
    {step === 7 && <g aria-hidden="true">
      {[0, 1, 2, 3].map(index => <Incoming key={`e${index}`} dx={18 + index * 13} dy={-76 - (index % 2) * 24} label="e⁻" delay={index * 0.12} />)}
      {[0, 1, 2, 3].map(index => <Incoming key={`h${index}`} dx={-64 + index * 38} dy={70} label="H⁺" delay={index * 0.12} />)}
    </g>}
  </g>;
}

export function AtpReaction({ step, active, onReplay }: { step: number; active: boolean; onReplay: () => void }) {
  const bound = step >= 11;
  return <g transform="translate(826 433)" role="button" tabIndex={0} className="rc-reaction"
    aria-label="Rejouer : le retour des H⁺ permet de fixer le phosphate à l’ADP et de former ATP" onClick={onReplay} onKeyDown={event => activate(event, onReplay)}
    data-reaction="atp" data-reaction-state={bound ? 'atp' : step === 10 ? 'binding' : 'adp'}>
    <title>Cliquer pour rejouer la fixation du phosphate à l’ADP, entraînée par le retour des H⁺ à travers l’ATP synthase.</title>
    <rect x="-50" y="-24" width="188" height="75" rx="14" className="rc-reaction-hit" />
    <g className={bound && active ? 'rc-product' : undefined} key={bound ? 'atp' : 'adp'}>
      <rect x="-40" y="-18" width="57" height="36" rx="16" fill="#bba2ff" />
      <path d={`M 8 0 H ${bound ? 98 : 67}`} stroke="#ffe34d" strokeWidth="4" />
      {[35, 66, ...(bound ? [97] : [])].map(x => <g key={x}>
        <circle cx={x} r="14" fill="#ffe34d" /><text x={x} y="5" textAnchor="middle" fontSize="16" fontWeight="900" fill="#102523">P</text>
      </g>)}
      <text x="25" y="46" textAnchor="middle" fill={bound ? '#ffe34d' : '#d3c4ff'} fontSize="27" fontWeight="900">{bound ? 'ATP' : 'ADP'}</text>
    </g>
    {!bound && <g transform="translate(97 0)">
      <g className={step === 10 ? 'rc-phosphate-binding' : undefined} style={step < 10 ? { transform: 'translate(9px, 40px)' } : undefined}>
        <circle r="14" fill="#ffe34d" /><text textAnchor="middle" y="5" fontSize="16" fontWeight="900" fill="#102523">Pi</text>
      </g>
    </g>}
  </g>;
}

export function DonorReaction({ step, donor, oxidized, isNadh, onReplay }: {
  step: number; donor: string; oxidized: string; isNadh: boolean; onReplay: () => void;
}) {
  return <g transform={`translate(${isNadh ? 130 : 257} 367)`} role="button" tabIndex={0} className="rc-reaction"
    aria-label={`Rejouer le don d’électrons de ${donor}`} onClick={onReplay} onKeyDown={event => activate(event, onReplay)}
    data-reaction="donor" data-reaction-state={step >= 2 ? 'oxidized' : 'reduced'}>
    <title>Cliquer pour rejouer le départ des deux électrons du coenzyme réduit.</title>
    <rect x="-86" y="-25" width="172" height="51" rx="25" fill={step >= 2 ? '#80b9a9' : '#42edff'} />
    <text textAnchor="middle" y="8" fontSize="25" fontWeight="900" fill="#102523">{step >= 2 ? oxidized : donor}</text>
    {step <= 1 && [-20, 20].map(x => <g key={x} transform={`translate(${x} -40)`}>
      <g className={step === 1 ? 'rc-donor-electron' : undefined}>
        <circle r="12" fill="#42edff" /><text textAnchor="middle" y="5" fontSize="15" fontWeight="900" fill="#102523">e⁻</text>
      </g>
    </g>)}
  </g>;
}
