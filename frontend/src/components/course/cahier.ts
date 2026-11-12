import type { CourseDeck } from './types';

/**
 * Le cahier de l'élève sort organisé comme un cours qu'on prépare (12 novembre 2026), à partir des données qui
 * existent déjà (aucun cours à changer) :
 *  - premier écran à copier : le titre du cours (`deck.title`) en grand, son sous-titre s'il en a un, puis la partie ;
 *  - en entrant dans une nouvelle partie (`activities[].title`) : son titre, numéroté I, II, III… ;
 *  - puis le titre de la diapositive en petit sous-titre numéroté dans sa partie (1., 2., …), puis les lignes.
 * La numérotation suit l'ordre du cours : elle ne change pas quand l'élève revient en arrière.
 */
export interface EnteteCahier {
  /** seulement sur le premier écran du cours */
  cours?: { titre: string; sousTitre?: string };
  /** seulement en entrant dans la partie (première diapositive de la partie) */
  partie?: string;
  /** « 2. Je remplace d'abord » */
  diapo: string;
}

const ROMAINS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX'];
/** « I. Rappel : … », « IV - … », « Partie 2 : … » : le titre porte déjà son numéro. */
const NUMEROTE = /^\s*(?:[IVXLC]+\s*[.\-–—)]|partie\s+\d+|\d+\s*[.\-–—)])/i;

const caches = new WeakMap<CourseDeck, Map<string, EnteteCahier>>();

export function planDuCahier(deck: CourseDeck): Map<string, EnteteCahier> {
  const deja = caches.get(deck);
  if (deja) return deja;
  const plan = new Map<string, EnteteCahier>();
  const acts = (deck.activities || []).filter(a => (a.slides || []).length);
  // Le cours numérote déjà ses parties (« I. Rappel… ») : on garde SA numérotation (une ouverture sans numéro reste
  // sans numéro) ; sinon on numérote I, II, III dans l'ordre.
  const dejaNumerotees = acts.some(a => NUMEROTE.test(a.title || ''));
  let n = 0;
  const d = deck as CourseDeck & { subtitle?: string; sous_titre?: string; catalog?: { subtitle?: string; sous_titre?: string } };
  const sousTitre = d.subtitle || d.sous_titre || d.catalog?.subtitle || d.catalog?.sous_titre || undefined;
  acts.forEach((a, ia) => {
    const titre = (a.title || '').trim();
    const partie = !titre ? undefined : dejaNumerotees ? titre : `${ROMAINS[n++] || n}. ${titre}`;
    a.slides.forEach((s, is) => {
      plan.set(s.id, {
        cours: ia === 0 && is === 0 ? { titre: deck.title, sousTitre } : undefined,
        partie: is === 0 ? partie : undefined,
        diapo: `${is + 1}. ${(s.title || '').trim()}`,
      });
    });
  });
  caches.set(deck, plan);
  return plan;
}

export function enteteDuCahier(deck: CourseDeck | null | undefined, slideId: string): EnteteCahier | undefined {
  return deck ? planDuCahier(deck).get(slideId) : undefined;
}
