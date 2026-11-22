/** Juger une réponse chiffrée dans le navigateur : le nombre écrit après le dernier « = » (ou « ≈ »), à la tolérance près. */
import type { ReponseAttendue } from './types';

/** « v = 0,6/0,6 = 1 m/s » → 1 ; « r ≈ 40,5 % » → 40,5 ; « 2,5 × 10⁻² » → 0,025 ; rien → null */
export function lireNombre(texte: string): number | null {
  const exposants: Record<string, string> = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-' };
  let s = texte.replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+/g, m => '^' + [...m].map(c => exposants[c]).join(''));
  const coupe = Math.max(s.lastIndexOf('='), s.lastIndexOf('≈'));
  if (coupe >= 0) s = s.slice(coupe + 1);
  s = s.replace(/\s+/g, '').replace(/,/g, '.').replace(/−/g, '-').replace(/[×x·*]10\^?\(?(-?\d+)\)?/g, 'e$1');
  const m = s.match(/-?\d+(?:\.\d+)?(?:e-?\d+)?/);
  return m ? parseFloat(m[0]) : null;
}

const UNITES: Record<string, RegExp> = {
  'm/s': /m\s*[/.·]\s*s|m\s*s\s*[-−⁻]\s*1|m\.s\^?-1/i, 's': /\bs\b|seconde/i, 'm': /\bm\b|mètre/i, '%': /%|pour\s*cent/i,
};

export interface Verdict { juste: boolean; note?: string; lu: number | null }

export function jugerValeur(rep: ReponseAttendue, texte: string): Verdict {
  const lu = lireNombre(texte);
  if (lu == null || rep.valeur == null) return { juste: false, lu, note: lu == null ? 'Écris le résultat avec sa valeur : « … = nombre unité ».' : undefined };
  const tol = rep.tolerance ?? 0.02;
  const juste = Math.abs(lu - rep.valeur) <= tol * Math.max(Math.abs(rep.valeur), 1e-12);
  let note: string | undefined;
  if (juste && rep.unite) {
    const re = UNITES[rep.unite];
    const vu = re ? re.test(texte) : texte.includes(rep.unite);
    if (!vu) note = `Le nombre est juste. Sur la copie, n'oublie pas l'unité : ${rep.unite}.`;
  }
  return { juste, lu, note };
}
