import { useId, useState } from 'react';
import { GLUCOSE_STOPS, glucoseStop, glucoseStopStep } from './glucoseJourneyModel';
import './glucoseJourney.css';

interface Props {
  step: number; maxStep: number; running: boolean;
  onSelect: (step: number) => void; onToggle: () => void; onReset: () => void;
}

function Carbons({ x, y, count, label }: { x: number; y: number; count: number; label?: string }) {
  return <g transform={`translate(${x} ${y})`}>
    {Array.from({ length: count }, (_, i) => <g key={i}>
      {i > 0 && <path d={`M${(i - 1) * 33} 0h33`} stroke="#fbc86c" strokeWidth="4" />}
      <circle cx={i * 33} r="14" fill="#ffc96d" stroke="#fff0c9" strokeWidth="2" />
      <text x={i * 33} y="5" textAnchor="middle" fill="#50310b" fontSize="14" fontWeight="800">C</text>
    </g>)}
    {label && <text x={(count - 1) * 16.5} y="38" textAnchor="middle" fill="#fff2d4" fontSize="19">{label}</text>}
  </g>;
}

function JourneyScene({ stop, arrow }: { stop: number; arrow: string }) {
  const link = `url(#${arrow})`;
  return <svg className="gj-scene" viewBox="0 0 760 340" role="img" aria-label={`${GLUCOSE_STOPS[stop].short} : ${GLUCOSE_STOPS[stop].note}`}>
    <defs><marker id={arrow} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="18" markerHeight="18" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0 10 5 0 10Z" fill="#86dfd4" /></marker></defs>
    {stop === 0 && <>
      <rect x="16" y="16" width="728" height="308" rx="60" fill="#103c3a" stroke="#348e84" strokeWidth="2" />
      <text x="48" y="53" className="gj-svg-location">HYALOPLASME · dans la cellule</text>
      <Carbons x={79} y={166} count={6} label="1 glucose · 6 C" />
      <path d="M293 166H373M373 166Q400 166 430 110H470" className="gj-route" markerEnd={link} />
      <path d="M373 166Q400 166 430 224H470" className="gj-route" markerEnd={link} />
      <text x="366" y="87" textAnchor="middle">Glycolyse</text>
      <Carbons x={507} y={110} count={3} label="Pyruvate · 3 C" />
      <Carbons x={507} y={224} count={3} label="Pyruvate · 3 C" />
      <text x="160" y="285" fill="#a6f3d0">+ 2 ATP nets</text><text x="440" y="294" fill="#c7b9ff">+ 2 NADH,H⁺</text>
    </>}
    {stop === 1 && <>
      <rect x="16" y="16" width="728" height="308" rx="32" fill="#103c3a" />
      <path d="M290 25V315" stroke="#e9b485" strokeWidth="9" /><path d="M330 25V315" stroke="#a29ae9" strokeWidth="9" />
      <text x="40" y="52" className="gj-svg-location">HYALOPLASME</text><text x="405" y="52" className="gj-svg-location">MATRICE</text>
      <Carbons x={67} y={131} count={3} /><Carbons x={67} y={208} count={3} />
      <text x="102" y="271" textAnchor="middle">2 pyruvates</text>
      <path d="M181 168H425" className="gj-route" markerEnd={link} />
      <text x="270" y="100" textAnchor="middle" fontSize="16">Deux membranes</text>
      <Carbons x={469} y={131} count={2} /><Carbons x={469} y={208} count={2} />
      <text x="497" y="271" textAnchor="middle">2 acétyl-CoA</text>
      <path d="M550 168Q595 168 614 112" className="gj-route" markerEnd={link} />
      <text x="623" y="90" fill="#ffc96d">2 CO₂</text><text x="590" y="220" fontSize="17" fill="#c7b9ff">+ 2 NADH,H⁺</text>
    </>}
    {stop === 2 && <>
      <rect x="16" y="16" width="728" height="308" rx="100" fill="#282841" stroke="#a29ae9" strokeWidth="3" />
      <text x="70" y="56" className="gj-svg-location">MATRICE MITOCHONDRIALE</text>
      <Carbons x={69} y={164} count={2} label="Acétyl-CoA × 2" />
      <path d="M164 164H246" className="gj-route" markerEnd={link} />
      <path d="M356 94A84 84 0 1 1 273 159" fill="none" stroke="#c4b2fa" strokeWidth="9" markerEnd={link} />
      <text x="357" y="169" textAnchor="middle" fontSize="28">Krebs</text><text x="357" y="202" textAnchor="middle">2 tours</text>
      <path d="M458 165H534" className="gj-route" markerEnd={link} />
      <text x="558" y="119" fill="#ffc96d" fontSize="29">4 CO₂</text>
      <text x="558" y="164" fill="#a6f3d0">+ 2 ATP</text><text x="531" y="211" fill="#c7b9ff">6 NADH,H⁺</text><text x="552" y="245" fill="#c7b9ff">2 FADH₂</text>
      <text x="357" y="300" textAnchor="middle" fontSize="16">Bilan : 6 CO₂ libérés depuis le départ</text>
    </>}
    {stop === 3 && <>
      <rect x="16" y="16" width="728" height="127" rx="24" fill="#173e44" />
      <rect x="16" y="164" width="728" height="160" rx="24" fill="#282841" />
      <path d="M16 147H744M16 160H744" stroke="#a29ae9" strokeWidth="6" />
      <text x="35" y="45" className="gj-svg-location">ESPACE INTERMEMBRANAIRE</text>
      <text x="35" y="310" className="gj-svg-location">MATRICE</text>
      {[130, 202, 279, 363, 443, 537, 624].map(x => <g key={x}><circle cx={x} cy="82" r="17" fill="#94e6e0" /><text x={x} y="87" fill="#123b3a" textAnchor="middle" fontSize="15">H⁺</text></g>)}
      <rect x="168" y="129" width="287" height="51" rx="18" fill="#366b76" stroke="#80c9d5" strokeWidth="2" />
      <text x="310" y="160" textAnchor="middle">Chaîne · e⁻ → O₂</text>
      <path d="M269 227V181M269 128V104" className="gj-route" markerEnd={link} />
      <text x="33" y="227" fill="#c7b9ff" fontSize="18">NADH,H⁺ / FADH₂</text>
      <text x="349" y="219" fill="#a3e2fa">O₂ → H₂O</text>
      <rect x="575" y="134" width="36" height="63" rx="12" fill="#f8c775" /><ellipse cx="594" cy="218" rx="46" ry="23" fill="#f8c775" />
      <path d="M593 108V239" className="gj-route" markerEnd={link} />
      <text x="594" y="265" textAnchor="middle">ATP synthase</text>
      <text x="415" y="303" fill="#a6f3d0">ADP + Pi → ATP</text>
      <text x="32" y="118" fontSize="15">Membrane interne ↓</text>
    </>}
  </svg>;
}

export default function GlucoseJourneyVisual({ step, maxStep, running, onSelect, onToggle, onReset }: Props) {
  const stop = glucoseStop(step, maxStep);
  const current = GLUCOSE_STOPS[stop];
  const [details, setDetails] = useState(false);
  const arrow = useId().replace(/:/g, '') + '-journey';
  return <section className="glucose-journey" aria-label="Voyage du glucose">
    <header className="gj-header"><div><span className="gj-eyebrow">LE VOYAGE DU GLUCOSE</span><h3>{current.title}</h3></div><span className="gj-counter">{stop + 1}<small> / 5</small></span></header>
    <nav className="gj-stops" aria-label="Escales du glucose">{GLUCOSE_STOPS.map((item, index) => <button type="button" key={item.short} aria-current={stop === index ? 'step' : undefined} onClick={() => onSelect(glucoseStopStep(index, maxStep))}><span>{index + 1}</span>{item.short}</button>)}</nav>
    <div className="gj-location">
      <svg width="74" height="32" viewBox="0 0 100 42" aria-label="Repère dans la cellule" role="img">
        <rect x="2" y="2" width="96" height="38" rx="18" fill="#173e3a" stroke="#75aa96" />
        <ellipse cx="63" cy="21" rx="27" ry="14" fill="#3b3454" stroke="#c3adf0" />
        <path d="M44 21l8-6 5 12 6-12 6 12 6-12 7 6" fill="none" stroke="#c3adf0" />
        <circle cx={stop === 0 ? 20 : stop === 3 ? 63 : 61} cy={stop === 3 ? 8 : 21} r="5" fill="#ffc96d" stroke="#fff1cc" />
      </svg>{current.place}<small>{stop < 3 ? '● = un carbone' : 'Bilan pour 1 glucose'}</small>
    </div>
    <div className="gj-view" key={stop}>
      {stop < 4 ? <JourneyScene stop={stop} arrow={arrow} /> : <div className="gj-yield">
        <div className="gj-yield-row"><div><strong>Respiration</strong><b>38 ATP</b></div><div className="gj-bar"><i style={{ width: '40.5%' }} /></div><span>40,5 %</span></div>
        <div className="gj-yield-row gj-fermentation"><div><strong>Fermentation</strong><b>2 ATP</b></div><div className="gj-bar"><i style={{ width: '2.13%' }} /></div><span>2,13 %</span></div>
        <p>Même départ : 2 860 kJ par mole de glucose.</p><small>Part colorée : énergie conservée dans l’ATP.<br />Le reste : chaleur et, en fermentation, énergie des produits organiques.</small>
      </div>}
    </div>
    <div className="gj-summary" aria-live="polite"><p>{current.note}</p>{stop < 4 && <div className="gj-tokens"><span>⚡ {current.atp} ATP cumulés</span><span>{current.co2} CO₂ libérés</span></div>}</div>
    {details && <p className="gj-detail" id={`${arrow}-detail`}>{current.detail}</p>}
    <footer className="gj-controls">
      <button type="button" className="gj-play" onClick={onToggle}>{running ? 'Ⅱ Pause' : step >= maxStep ? '↻ Rejouer' : '▶ Voyager'}</button>
      <button type="button" aria-label="Étape précédente" disabled={stop === 0} onClick={() => onSelect(glucoseStopStep(stop - 1, maxStep))}>←</button>
      <button type="button" aria-label="Étape suivante" disabled={stop === 4} onClick={() => onSelect(glucoseStopStep(stop + 1, maxStep))}>→</button>
      <button type="button" aria-label="Revenir au départ" onClick={onReset}>↺</button>
      <button type="button" className="gj-details-button" aria-expanded={details} aria-controls={`${arrow}-detail`} onClick={() => setDetails(value => !value)}>{details ? '− Détails' : '+ Détails'}</button>
    </footer>
    <small className="gj-convention">Convention BAC du cours : 2 + 2 + 34 = 38 ATP.</small>
  </section>;
}
