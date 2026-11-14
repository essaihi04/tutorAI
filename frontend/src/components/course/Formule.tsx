import type { ReactNode } from 'react';

/**
 * Une formule écrite au tableau, sans jamais de « _ » devant l'élève :
 *  - « y_M(t) = y_S(t − τ) » : M et S en indice ;
 *  - « lim_{x→1} (x² + 3x + 1) » : « x→1 » écrit en petit SOUS « lim », comme au tableau et sur la copie
 *    (12 novembre 2026 ; la craie des simulations l'écrit pareil, `LC.limite`).
 */
export function Formule({ t }: { t: string }) {
  const parts: ReactNode[] = [];
  // « lim_{…} » d'abord (l'indice va dessous), puis « lettre_indice »
  const re = /lim_(\{[^}]+\}|[^\s(]+)|([A-Za-zτθΔλωφ])_(\{[^}]+\}|[A-Za-z0-9]+)/g;
  let i = 0, m: RegExpExecArray | null, k = 0;
  while ((m = re.exec(t))) {
    if (m.index > i) parts.push(t.slice(i, m.index));
    if (m[1] !== undefined) {
      parts.push(
        <span key={k++} className="mr-[0.15em] inline-flex flex-col items-center align-baseline leading-none">
          <span>lim</span>
          <span className="mt-0.5 whitespace-nowrap text-[0.55em]">{m[1].replace(/[{}]/g, '')}</span>
        </span>,
      );
    } else {
      parts.push(m[2], <sub key={k++} className="text-[0.7em]">{m[3].replace(/[{}]/g, '')}</sub>);
    }
    i = re.lastIndex;
  }
  if (i < t.length) parts.push(t.slice(i));
  return <>{parts}</>;
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
