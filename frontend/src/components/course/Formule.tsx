import type { ReactNode } from 'react';

/**
 * Une formule écrite comme au tableau (et comme la craie des simulations), jamais de « _ », de « ^ » ni de barre
 * « / » de calcul devant l'élève :
 *  - « y_M(t) = y_S(t − τ) », « [A⁻]_éq », « Q_r,éq » : indices ; « Qr,éq », « xmax », « Ka » écrits sans « _ » aussi ;
 *  - « e^(−t/τ) », « 10^(−pH) » : exposant écrit en haut ;
 *  - « C·τ²/(1 − τ) », « di/dt », « 1/K » : vraie fraction, le numérateur au-dessus du trait (16 novembre 2026 :
 *    « pas de slash dans les équations : un nombre sur un autre, comme dans les simulations ») ;
 *    la barre reste dans les unités (mol/L), les couples (AH/A⁻, Cu²⁺/Cu), t₁/₂ et dans un exposant ;
 *  - « lim_{x→1} (x² + 3x + 1) » : « x→1 » écrit en petit SOUS « lim » (12 novembre 2026, `LC.limite`).
 */
export function Formule({ t }: { t: string }) {
  return <>{rendre(sansTiretBas(t || ''), { n: 0 })}</>;
}

/** Les indices de chimie que les cours écrivent sans « _ » : Qr,éq → Q_{r,éq}, xmax → x_max, Ka → K_a, [A⁻]éq. */
function sansTiretBas(t: string): string {
  return t
    .replace(/\bQr,(éq|i|f)(?![\wéè])/g, 'Q_{r,$1}')
    .replace(/\bQr(?![\wéè,])/g, 'Q_r')
    .replace(/\bx(max|éq)(?![\wéè])/g, 'x_$1')
    .replace(/\bK([aAe])(?![\wéè])/g, 'K_$1')
    .replace(/\](éq|f|0)(?![\wéè])/g, ']_$1');
}

const UNITE_HAUT = /^(m?mol|[mkμ]?g|[kmcμ]?m|[kM]?J|[kM]?W|[mk]?V|[mk]?A|N|Pa|m?S|rad|tr|L)$/;
const UNITE_BAS = /^(m?L|s|min|h|mol|[kc]?m[²³]?|kg|K|°C|Ω)$/;
/** Une espèce chimique d'un couple : un ion (⁺ ⁻) ou une formule à plusieurs majuscules (AH, NH₄⁺, CH₃COOH). */
const espece = (s: string) => !/[·×()=]|^\d/.test(s) && (/[⁺⁻]/.test(s) || (s.match(/[A-Z]/g) || []).length >= 2);

/** La barre en `i` est-elle une fraction à écrire en deux étages ? */
function estFraction(num: string, den: string, derivee = false): boolean {
  if (!num || !den) return false;
  if (derivee) return true;                                                 // di/dt, d²u_C/dt²
  if (num.startsWith('[') || den.startsWith('[')) return true;              // [A⁻]/[AH] : un rapport de concentrations
  if (/^[A-Za-zéèêàç]{2,}$/.test(num) && /^[A-Za-zéèêàç]{2,}$/.test(den)) return false;   // et/ou, Ox/Red
  if (/[₀-₉]$/.test(num) && /^[₀-₉]/.test(den)) return false;               // t₁/₂
  if (UNITE_HAUT.test(num) && UNITE_BAS.test(den.replace(/[.,;)]$/, ''))) return false;   // mol/L, m/s
  if (espece(num) && espece(den)) return false;                             // AH/A⁻, Fe³⁺/Fe²⁺
  return true;
}

/** Ferme la parenthèse ouverte en `i` (ou ouvre celle fermée en `i`, sens = -1) : l'indice de l'autre. */
function apparier(t: string, i: number, sens: 1 | -1): number {
  const [o, f] = sens === 1 ? ['(', ')'] : [')', '('];
  let d = 0;
  for (let j = i; j >= 0 && j < t.length; j += sens) {
    if (t[j] === o) d++;
    else if (t[j] === f && --d === 0) return j;
  }
  return -1;
}

const BORD_GAUCHE = /[\s=≈<>≤≥+−\-−,;:(\[{|]/;
const BORD_DROIT = /[\s=≈<>≤≥+−\-,;:)\]}·×|[]/;
/** Une virgule décimale (0,0125) fait partie du nombre. */
const decimale = (t: string, j: number) => t[j] === ',' && /\d/.test(t[j - 1] || '') && /\d/.test(t[j + 1] || '');

/** Les fractions du texte (hors exposants) : [début du numérateur, barre, fin du dénominateur). */
function fractions(t: string): { a: number; i: number; b: number }[] {
  const res: { a: number; i: number; b: number }[] = [];
  let exp = -1;   // fin d'un exposant « ^(…) » en cours : sa barre reste dans l'exposant
  for (let i = 0; i < t.length; i++) {
    if (t[i] === '^' && t[i + 1] === '(') { exp = apparier(t, i + 1, 1); continue; }
    if (i <= exp || t[i] !== '/') continue;
    if (t[i - 1] === ' ' || t[i + 1] === ' ') continue;   // « et / ou », barre isolée
    // numérateur : vers la gauche, à travers les parenthèses ; une dérivée « di/dt » n'emporte que « di »
    let a = i, estDerivee = false;
    const derivee = /(?:^|[^A-Za-z])(d²?(?:pH|[A-Za-zθφσλτωΩ])(?:_[A-Za-z]+|_\{[^}]+\}|\([a-z]\))?)$/.exec(t.slice(0, i));
    if (derivee && /^d[A-Za-z²]/.test(t.slice(i + 1))) { a = i - derivee[1].length; estDerivee = true; }
    else {
      while (a > 0) {
        const c = t[a - 1];
        if (c === ')') { const o = apparier(t, a - 1, -1); if (o < 0) break; a = o; continue; }
        if (c === ']') { const o = t.lastIndexOf('[', a - 2); if (o < 0) break; a = o; continue; }
        if (c === '|' && a === i) { const o = t.lastIndexOf('|', a - 2); if (o < 0 || /\s/.test(t.slice(o, a))) break; a = o; continue; }   // |z|/…
        if (decimale(t, a - 1)) { a--; continue; }
        if (BORD_GAUCHE.test(c) || c === '/') break;
        a--;
      }
    }
    // dénominateur : un groupe entre parenthèses, ou jusqu'au prochain bord
    let b = i + 1;
    if (t[b] === '(') { const f = apparier(t, b, 1); if (f < 0) continue; b = f + 1; }
    else if (t[b] === '[') { const f = t.indexOf(']', b); if (f < 0) continue; b = f + 1; }
    else if (t[b] === '|') { const f = t.indexOf('|', b + 1); if (f < 0 || /\s/.test(t.slice(b, f))) continue; b = f + 1; }   // …/|z′|
    while (b < t.length) {
      const c = t[b];
      if (c === '(') { const f = apparier(t, b, 1); if (f < 0) break; b = f + 1; continue; }
      if (decimale(t, b)) { b++; continue; }
      if (c === '·' && t[b + 1] === '[' && t[i + 1] === '[') { const f = t.indexOf(']', b + 1); if (f < 0) break; b = f + 1; continue; }
      if (BORD_DROIT.test(c) || c === '/') break;
      if (c === '.' && (b + 1 >= t.length || /\s/.test(t[b + 1]))) break;   // point final
      b++;
    }
    const num = t.slice(a, i), den = t.slice(i + 1, b);
    if (!estFraction(num, den, estDerivee)) continue;
    if (res.length && a < res[res.length - 1].b) continue;   // chevauche la précédente : on la garde
    res.push({ a, i, b });
    i = b - 1;
  }
  return res;
}

const sansParentheses = (s: string) => (s.startsWith('(') && apparier(s, 0, 1) === s.length - 1 ? s.slice(1, -1) : s);

function rendre(t: string, k: { n: number }): ReactNode[] {
  const parts: ReactNode[] = [];
  let i = 0;
  for (const f of fractions(t)) {
    if (f.a > i) parts.push(...indices(t.slice(i, f.a), k));
    parts.push(
      <span key={k.n++} className="mx-[0.1em] inline-flex flex-col items-center text-center leading-[1.1]" style={{ verticalAlign: 'middle', fontSize: '0.92em' }}>
        <span className="px-[0.15em]">{rendre(sansParentheses(t.slice(f.a, f.i)), k)}</span>
        <span className="w-full border-t border-current" style={{ borderTopWidth: '0.08em' }} aria-hidden="true" />
        <span className="px-[0.15em]">{rendre(sansParentheses(t.slice(f.i + 1, f.b)), k)}</span>
      </span>,
    );
    i = f.b;
  }
  if (i < t.length) parts.push(...indices(t.slice(i), k));
  return parts;
}

/** « lim_{…} » (l'indice dessous), « lettre_indice », « ]_indice », « ^(exposant) » et « ^x ». */
function indices(t: string, k: { n: number }): ReactNode[] {
  const parts: ReactNode[] = [];
  const re = /lim_(\{[^}]+\}|[^\s(]+)|([A-Za-zτθΔλωφℓ\]])_(\{[^}]+\}|[A-Za-z0-9éèêàçℓ]+(?:,[A-Za-zéèêàç]+)?)|\^(\([^()]*(?:\([^()]*\)[^()]*)*\)|[A-Za-z0-9−\-+]+)/g;
  let i = 0, m: RegExpExecArray | null;
  while ((m = re.exec(t))) {
    if (m.index > i) parts.push(t.slice(i, m.index));
    if (m[1] !== undefined) {
      parts.push(
        <span key={k.n++} className="mr-[0.15em] inline-flex flex-col items-center align-baseline leading-none">
          <span>lim</span>
          <span className="mt-0.5 whitespace-nowrap text-[0.55em]">{m[1].replace(/[{}]/g, '')}</span>
        </span>,
      );
    } else if (m[2] !== undefined) {
      parts.push(m[2], <sub key={k.n++} className="text-[0.7em]">{m[3].replace(/[{}]/g, '')}</sub>);
    } else {
      const e = m[4].startsWith('(') ? m[4].slice(1, -1) : m[4];
      parts.push(<sup key={k.n++} className="text-[0.7em]">{indices(e, k)}</sup>);
    }
    i = re.lastIndex;
  }
  if (i < t.length) parts.push(t.slice(i));
  return parts;
}

/**
 * La variable et la valeur d'une limite dans un énoncé : « … quand x → 1 », « lim f(x) en +∞ », « x tend vers 0 ».
 * `null` si l'énoncé n'en dit rien.
 */
export function tendVers(enonce: string): string | null {
  const t = enonce || '';
  const m = /\b([a-zA-Z])\s*(?:→|->|tend\s+vers)\s*([+−-]?\s*∞|[+−-]?\d+(?:[.,]\d+)?|[a-zA-Z]\b|0⁺|0⁻)/.exec(t);
  if (m) return `${m[1]}→${m[2].replace(/\s+/g, '')}`;
  const e = /\b(?:en|quand\s+[a-zA-Z]\s+tend\s+vers)\s+([+−-]\s*∞)/.exec(t);
  return e ? `x→${e[1].replace(/\s+/g, '')}` : null;
}

/**
 * Une ligne de démonstration écrite « lim (x² + 3x + 1) = … » sans dire vers quoi x tend : si l'énoncé de la question
 * le dit (« quand x → 1 »), l'indice est ajouté sous « lim ». Une ligne qui porte déjà son indice ne change pas.
 */
export function limAvecIndice(ligne: string, enonce: string): string {
  if (!/\blim\b(?!_)/.test(ligne)) return ligne;
  const v = tendVers(enonce) || tendVers(ligne);
  if (!v) return ligne;
  // « lim (…) quand x → 1 » écrit en toutes lettres sur la ligne : on le range sous lim
  const sansQuand = ligne.replace(/\s*(?:quand|lorsque)\s+[a-zA-Z]\s*(?:→|->|tend\s+vers)\s*\S+/, '');
  return sansQuand.replace(/\blim\b(?!_)/g, `lim_{${v}}`);
}
