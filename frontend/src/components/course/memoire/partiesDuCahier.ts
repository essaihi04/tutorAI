import type { FigureCahierData } from '../FigureCahier';

/**
 * Le cahier d'un bloc se recopie partie par partie (20 novembre 2026, demande de l'utilisateur) : l'élève ne voit que
 * la partie à écrire maintenant ; « C'est écrit » la marque écrite et montre la suivante. Les parties se lisent dans
 * les données, sans toucher aux cours :
 *  - une ligne qui commence par « 1. », « 2) »… ouvre une partie (les lignes d'avant forment la première) ; un titre
 *    romain (« II. Titre ») posé juste avant elle ouvre la partie avec elle ;
 *  - un cahier « une ligne par diapositive » (titre de diapositive au-dessus de chaque ligne) : une partie par ligne ;
 *  - sans numéro : des groupes de 3 lignes au plus (4 → 2 + 2, 5 → 3 + 2) ; 3 lignes ou moins : une seule partie.
 * Chaque dessin va avec la partie dont il partage le plus de mots (titre compté double) ; `partie` (1, 2…) dans le
 * dessin l'impose ; sans mot commun, il va avec la dernière partie (sous tout le texte, comme avant).
 */
export interface PartieCahier {
  /** indices des lignes de `bloc.cahier` */
  lignes: number[];
  /** indices des dessins de `bloc.cahier_figures` */
  figures: number[];
}

const NUMERO = /^\s*\d+\s*[.)]\s/;
const ROMAIN = /^\s*[IVXL]+\s*[.)\-–—]\s/;

/** Le cahier a ses parties numérotées (« 1. », « 2) »…) : c'est elles qui le découpent. */
export function cahierNumerote(lignes: { texte: string }[]): boolean {
  return lignes.some(l => NUMERO.test(l.texte || ''));
}
const MOT = /[a-z0-9]{4,}/g;
const VIDES = new Set(['dans', 'avec', 'pour', 'sont', 'est', 'une', 'des', 'les', 'leur', 'cette', 'entre', 'puis', 'donc', 'plus', 'tout', 'tous', 'elle', 'elles', 'quand', 'comme', 'chaque', 'deux', 'trois']);

function mots(t: string): Set<string> {
  const s = (t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  return new Set((s.match(MOT) || []).filter(m => !VIDES.has(m)));
}

export function partiesDuCahier(lignes: { texte: string }[], figures: (FigureCahierData & { partie?: number })[], parLigne: boolean): PartieCahier[] {
  const groupes: number[][] = [];
  if (parLigne) {
    lignes.forEach((_, i) => groupes.push([i]));
  } else if (lignes.some(l => NUMERO.test(l.texte || ''))) {
    // un titre de partie romaine (« II. Titre ») posé juste avant « 1. » ouvre la partie avec elle, au lieu de finir
    // la partie d'avant (audit des cahiers, 20 novembre 2026)
    lignes.forEach((l, i) => {
      const titre = ROMAIN.test(l.texte || '') && NUMERO.test(lignes[i + 1]?.texte || '');
      const suitTitre = i > 0 && ROMAIN.test(lignes[i - 1].texte || '') && NUMERO.test(l.texte || '');
      if (!groupes.length || titre || (NUMERO.test(l.texte || '') && !suitTitre)) groupes.push([i]);
      else groupes[groupes.length - 1].push(i);
    });
  } else if (lignes.length > 3) {
    const k = Math.ceil(lignes.length / 3);
    let i = 0;
    for (let g = 0; g < k; g++) {
      const taille = Math.ceil((lignes.length - i) / (k - g));
      groupes.push(Array.from({ length: taille }, (_, j) => i + j));
      i += taille;
    }
  } else {
    groupes.push(lignes.map((_, i) => i));
  }
  const parties: PartieCahier[] = groupes.map(g => ({ lignes: g, figures: [] }));
  if (!parties.length) parties.push({ lignes: [], figures: [] });

  const motsParties = parties.map(p => mots(p.lignes.map(i => lignes[i].texte).join(' ')));
  figures.forEach((f, fi) => {
    let cible = parties.length - 1;
    if (typeof f.partie === 'number' && f.partie >= 1 && f.partie <= parties.length) cible = f.partie - 1;
    else if (parties.length > 1) {
      const titre = mots(f.titre || '');
      const legende = mots(f.legende || '');
      let meilleur = 0;
      motsParties.forEach((mp, pi) => {
        let score = 0;
        titre.forEach(m => { if (mp.has(m)) score += 2; });
        legende.forEach(m => { if (mp.has(m)) score += 1; });
        if (score > meilleur) { meilleur = score; cible = pi; }
      });
    }
    parties[cible].figures.push(fi);
  });
  return parties;
}
