import { useState, type RefObject } from 'react';

/**
 * Le clavier scientifique (user rule, 10 novembre 2026) : à côté de chaque champ où l'élève écrit (réponse libre,
 * question au professeur, réponse directe d'une simulation), « ⌨ Symboles » ouvre ce petit clavier qui insère au
 * curseur tout ce que le 2ᵉ Bac PC écrit — lettres grecques, exposants et indices, unités, flèches de réaction,
 * ensembles et opérateurs des maths. Le même bouton le referme. Touches de 44 px au moins : au doigt, sur téléphone.
 */

type Touche = string | { l: string; t: string; titre?: string };

/** `t` : ce qui est inséré ; `l` : ce qui est affiché sur la touche (quand ils diffèrent). */
const ONGLETS: Record<'Physique' | 'Chimie' | 'Maths', { titre: string; touches: Touche[] }[]> = {
  Physique: [
    { titre: 'Lettres grecques', touches: ['λ', 'τ', 'θ', 'ω', 'φ', 'Δ', 'μ', 'ρ', 'σ', 'ε', 'α', 'β', 'γ', 'π'] },
    { titre: 'Opérations', touches: ['·', '×', '÷', '±', '≈', '≠', '≤', '≥', '∝', '√', { l: 'a/b', t: '/' }, '=', '(', ')'] },
    { titre: 'Exposants', touches: ['²', '³', '⁻¹', '⁻²', '⁻³', '⁻⁶', '⁻⁹', { l: '10ⁿ', t: '×10' }, '⁰', '¹', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹', '⁻', '⁺'] },
    { titre: 'Indices', touches: ['₀', '₁', '₂', '₃', 'ₘ', 'ₛ', 'ₙ', 'ₓ'] },
    { titre: 'Unités', touches: [{ l: 'm·s⁻¹', t: ' m·s⁻¹' }, { l: 'Hz', t: ' Hz' }, 'Ω', 'µ', { l: '°C', t: ' °C' }, { l: 'ms', t: ' ms' }, { l: 'μs', t: ' μs' }, { l: 'nm', t: ' nm' }, { l: 'J', t: ' J' }, { l: 'W', t: ' W' }, { l: 'V', t: ' V' }, { l: 'A', t: ' A' }, { l: 'F', t: ' F' }, { l: 'H', t: ' H' }, { l: 'Bq', t: ' Bq' }, { l: 'eV', t: ' eV' }] },
    { titre: 'Vecteurs', touches: [{ l: 'v⃗', t: '⃗', titre: 'flèche de vecteur sur la lettre qui précède' }, '→', { l: '‖v‖', t: '‖‖' }] },
  ],
  Chimie: [
    { titre: 'Réactions', touches: ['→', '⇌', '+', '⁺', '⁻', '²⁺', '³⁺', '²⁻', '³⁻', '↑', '↓'] },
    { titre: 'Espèces', touches: ['H₃O⁺', 'HO⁻', 'H₂O', 'H⁺', 'Na⁺', 'Cl⁻', 'CO₂', 'NH₃', 'NH₄⁺', 'CH₃COOH', 'CH₃COO⁻'] },
    { titre: 'Indices', touches: ['₂', '₃', '₄', '₅', '₆', '₁', '₀'] },
    { titre: 'Grandeurs', touches: ['[ ]', '[', ']', 'pH', 'pKa', 'Ka', 'Ke', 'Qr', 'Qr,éq', 'K', 'τ', 'xmax', 'xéq', 'σ', 'Δ', '×10', '·', '≈'] },
    { titre: 'Unités', touches: [{ l: 'mol·L⁻¹', t: ' mol·L⁻¹' }, { l: 'mol', t: ' mol' }, { l: 'g·mol⁻¹', t: ' g·mol⁻¹' }, { l: 'L', t: ' L' }, { l: 'mL', t: ' mL' }, { l: 'S·m⁻¹', t: ' S·m⁻¹' }, { l: 'C', t: ' C' }] },
  ],
  Maths: [
    { titre: 'Ensembles et logique', touches: ['∞', '∈', '∉', '⊂', '∪', '∩', 'ℝ', 'ℕ', 'ℤ', 'ℂ', 'ℚ', '∅', '∀', '∃', '⇒', '⇔', '≡'] },
    { titre: 'Analyse', touches: [{ l: 'lim', t: 'lim ' }, '∫', '∑', { l: 'ln', t: 'ln(' }, { l: 'eˣ', t: 'e^' }, { l: 'log', t: 'log(' }, '√', 'f′', '→', '+∞', '-∞', '≤', '≥', '≠', '±', 'π'] },
    { titre: 'Complexes', touches: [{ l: '|z|', t: '|z|' }, { l: 'z̄', t: 'z̄' }, { l: 'arg', t: 'arg(' }, 'i', { l: 'e^(iθ)', t: 'e^(iθ)' }, 'θ', 'Re', 'Im'] },
    { titre: 'Exposants et indices', touches: ['²', '³', 'ⁿ', '⁻¹', '₀', '₁', 'ₙ', 'ₙ₊₁', { l: 'a/b', t: '/' }, '(', ')'] },
  ],
};

type Champ = HTMLInputElement | HTMLTextAreaElement;

/** Insère au curseur du champ (ou remplace la sélection) et y replace le curseur, après le rendu de React. */
function insererAuCurseur(champ: Champ | null, valeur: string, texte: string, poser: (v: string) => void) {
  const debut = champ?.selectionStart ?? valeur.length;
  const fin = champ?.selectionEnd ?? debut;
  const suite = valeur.slice(0, debut) + texte + valeur.slice(fin);
  poser(suite);
  const curseur = debut + texte.length;
  requestAnimationFrame(() => {
    if (!champ) return;
    champ.focus({ preventScroll: true });
    try { champ.setSelectionRange(curseur, curseur); } catch { /* champ sans sélection */ }
  });
}

/** Le bouton « ⌨ Symboles » : ouvre et referme le clavier. */
export function BoutonSymboles({ ouvert, onClick, petit = false }: { ouvert: boolean; onClick: () => void; petit?: boolean }) {
  return (
    <button type="button" onClick={onClick} aria-pressed={ouvert} aria-label="Clavier de symboles scientifiques"
      // garder le curseur dans le champ : le bouton ne prend pas le focus
      onMouseDown={e => e.preventDefault()}
      className={`shrink-0 rounded-full ${petit ? 'px-3 py-1 text-xs' : 'px-4 py-2 text-sm'} ${ouvert ? 'bg-amber-200 text-black' : 'bg-white/10 hover:bg-white/20'}`}
      style={{ fontFamily: 'system-ui, sans-serif' }}>
      ⌨ Symboles
    </button>
  );
}

export default function ClavierScientifique({ cible, valeur, onChange, onFermer }: {
  /** Le champ où l'élève écrit (le curseur y est lu, puis replacé après l'insertion). */
  cible: RefObject<Champ | null>;
  valeur: string;
  onChange: (v: string) => void;
  onFermer?: () => void;
}) {
  const [onglet, setOnglet] = useState<keyof typeof ONGLETS>(() => {
    try { return (localStorage.getItem('clavier-scientifique:onglet') as keyof typeof ONGLETS) || 'Physique'; } catch { return 'Physique'; }
  });
  const choisir = (o: keyof typeof ONGLETS) => {
    setOnglet(o);
    try { localStorage.setItem('clavier-scientifique:onglet', o); } catch { /* sans mémoire locale */ }
  };
  const taper = (t: Touche) => {
    const texte = typeof t === 'string' ? (t === '[ ]' ? '[]' : t) : t.t;
    insererAuCurseur(cible.current, valeur, texte, onChange);
  };
  return (
    <div className="question-apparait mt-2 rounded-xl border border-amber-200/30 bg-[#0b1912] p-2 text-white" role="group" aria-label="Clavier scientifique"
      style={{ fontFamily: 'system-ui, "Segoe UI Symbol", "Cambria Math", sans-serif' }}
      // un appui sur le clavier ne doit jamais faire perdre le curseur du champ
      onMouseDown={e => e.preventDefault()}>
      <div className="mb-2 flex items-center gap-1">
        {(Object.keys(ONGLETS) as (keyof typeof ONGLETS)[]).map(o => (
          <button key={o} type="button" onClick={() => choisir(o)} role="tab" aria-selected={onglet === o}
            className={`min-h-[40px] rounded-lg px-3 text-sm ${onglet === o ? 'bg-amber-200 text-black' : 'bg-white/10 hover:bg-white/20'}`}>{o}</button>
        ))}
        {onFermer && <button type="button" onClick={onFermer} aria-label="Fermer le clavier" className="ml-auto min-h-[40px] min-w-[40px] rounded-lg text-white/60 hover:bg-white/10">×</button>}
      </div>
      <div className="max-h-[38vh] space-y-2 overflow-y-auto pr-1">
        {ONGLETS[onglet].map(g => (
          <div key={g.titre}>
            <div className="mb-1 text-[11px] uppercase tracking-wide text-white/45">{g.titre}</div>
            <div className="grid gap-1" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(44px, 1fr))' }}>
              {g.touches.map((t, i) => {
                const l = typeof t === 'string' ? t : t.l;
                return (
                  <button key={`${l}-${i}`} type="button" onClick={() => taper(t)} title={typeof t === 'string' ? t : t.titre || t.t.trim()}
                    className="min-h-[44px] rounded-lg border border-white/10 bg-white/[0.06] px-1 text-[17px] leading-none hover:bg-white/15 active:bg-amber-200/30"
                    style={{ touchAction: 'manipulation', gridColumn: l.length > 4 ? 'span 2' : undefined }}>
                    {l}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
