/**
 * Où poser un mot sur l'ardoise, sachant ce qui y est DÉJÀ.
 *
 * Le tuteur envoie ses croquis élément par élément, et chaque élément portait
 * son texte à la coordonnée qu'il avait choisie, sans jamais regarder le reste
 * du tableau. Deux labels finissaient l'un SUR l'autre — « direction de
 * propagation » et « propagation » superposés au même endroit, illisibles — et
 * un mot posé près du bord sortait de la zone : l'élève voyait « …cule » au
 * lieu de « molécule ».
 *
 * Le prompt demandait déjà de ne pas superposer deux labels. Une consigne ne
 * suffit pas : c'est le tableau qui doit tenir le registre. Ce module fait ce
 * qu'un professeur fait sans y penser — il regarde son tableau avant d'écrire,
 * et décale son mot de deux centimètres quand la place est prise.
 *
 * Il ne DÉPLACE jamais un trait : seuls les mots bougent, et le moins possible.
 */

/** La zone de dessin de `LiveBoard`, en coordonnées de son viewBox. */
export const ZONE_LARGEUR = 500;
export const ZONE_HAUTEUR = 400;

/** Le cadre dans lequel un mot doit rester. Une figure générée a le sien. */
export interface Zone { largeur: number; hauteur: number }
const ZONE_TABLEAU: Zone = { largeur: ZONE_LARGEUR, hauteur: ZONE_HAUTEUR };

/** Le blanc qu'on laisse au bord : un mot collé au cadre se lit mal. */
const MARGE = 6;

/** En dessous, on n'écrit plus : c'est illisible de loin. */
const TAILLE_MIN = 11;
const TAILLE_MAX = 14;

/** Largeur moyenne d'un caractère de la cursive du tableau, en em. */
const LARGEUR_CARACTERE = 0.52;

export interface Boite { x1: number; y1: number; x2: number; y2: number }
export type Ancre = 'start' | 'middle' | 'end';
export interface PoseTexte { x: number; y: number; fontSize: number; ancre: Ancre }

interface Point { x: number; y: number }

/** La forme d'un élément dessiné, vue par ce module (cf. `LiveDrawElement`). */
export interface ElementDessine {
  type: string;
  points?: Point[];
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  radius?: number;
  radiusX?: number;
  radiusY?: number;
  text?: string;
  label?: string;
  fontSize?: number;
  /** L'alignement demandé pour un élément `text` (défaut : `start`). */
  align?: Ancre;
}

/** Ce qu'un élément laisse derrière lui, et que le suivant doit éviter. */
export interface EmpreinteElement {
  /** Le mot écrit, s'il y en a un. Un texte n'en chevauche jamais un autre. */
  texte: Boite | null;
  /** Le trait, l'ellipse, le rectangle : un obstacle mou, qu'on préfère éviter. */
  forme: Boite | null;
}

/** La place que prend un mot, mesurée assez juste pour décider d'un décalage. */
export function mesurerTexte(texte: string, fontSize: number): { w: number; h: number } {
  const longueur = (texte || '').length;
  return {
    w: Math.max(fontSize * 0.6, longueur * fontSize * LARGEUR_CARACTERE),
    h: fontSize * 1.05,
  };
}

/** La boîte occupée par un texte posé à cette pose (y = ligne de base SVG). */
export function boiteDuTexte(texte: string, pose: PoseTexte): Boite {
  const { w, h } = mesurerTexte(texte, pose.fontSize);
  const x1 = pose.ancre === 'middle' ? pose.x - w / 2 : pose.ancre === 'end' ? pose.x - w : pose.x;
  return { x1, y1: pose.y - h * 0.8, x2: x1 + w, y2: pose.y + h * 0.25 };
}

function aireCommune(a: Boite, b: Boite): number {
  const dx = Math.min(a.x2, b.x2) - Math.max(a.x1, b.x1);
  const dy = Math.min(a.y2, b.y2) - Math.max(a.y1, b.y1);
  return dx > 0 && dy > 0 ? dx * dy : 0;
}

function boiteDesPoints(points: Point[] | undefined): Boite | null {
  if (!points || points.length === 0) return null;
  const xs = points.map(p => p.x);
  const ys = points.map(p => p.y);
  return { x1: Math.min(...xs), y1: Math.min(...ys), x2: Math.max(...xs), y2: Math.max(...ys) };
}

/**
 * Ramène un mot DANS le tableau.
 *
 * On déplace l'ancre, pas la boîte : le texte reste aligné comme il a été
 * demandé (centré sous sa forme, à gauche de son trait), il rentre seulement.
 * Un mot plus large que l'ardoise est rapetissé jusqu'au plancher lisible.
 */
function rentrerDansLaZone(texte: string, pose: PoseTexte, zone: Zone): PoseTexte {
  let fontSize = pose.fontSize;
  let mesure = mesurerTexte(texte, fontSize);
  const dispo = zone.largeur - 2 * MARGE;
  if (mesure.w > dispo) {
    fontSize = Math.max(TAILLE_MIN, Math.floor(fontSize * (dispo / mesure.w)));
    mesure = mesurerTexte(texte, fontSize);
  }
  const boite = boiteDuTexte(texte, { ...pose, fontSize });
  let dx = 0;
  let dy = 0;
  if (boite.x1 < MARGE) dx = MARGE - boite.x1;
  else if (boite.x2 > zone.largeur - MARGE) dx = zone.largeur - MARGE - boite.x2;
  if (boite.y1 < MARGE) dy = MARGE - boite.y1;
  else if (boite.y2 > zone.hauteur - MARGE) dy = zone.hauteur - MARGE - boite.y2;
  return { ...pose, fontSize, x: pose.x + dx, y: pose.y + dy };
}

/**
 * Les endroits où un professeur essaie, dans l'ordre : là où il voulait, puis
 * une ligne au-dessus, une en dessous, deux au-dessus… et enfin sur le côté.
 */
function decalages(w: number, h: number): Array<{ dx: number; dy: number }> {
  const pas = h + 3;
  const cote = w * 0.6 + 8;
  const liste: Array<{ dx: number; dy: number }> = [{ dx: 0, dy: 0 }];
  for (let k = 1; k <= 4; k += 1) {
    liste.push({ dx: 0, dy: -k * pas }, { dx: 0, dy: k * pas });
  }
  liste.push({ dx: -cote, dy: 0 }, { dx: cote, dy: 0 });
  for (let k = 1; k <= 3; k += 1) {
    liste.push(
      { dx: -cote, dy: -k * pas }, { dx: cote, dy: -k * pas },
      { dx: -cote, dy: k * pas }, { dx: cote, dy: k * pas },
    );
  }
  return liste;
}

/**
 * La place libre la plus proche de celle qu'on voulait.
 *
 * Trois règles, dans cet ordre :
 *
 * 1. la place DEMANDÉE gagne toujours quand elle est libre — une figure de la
 *    bibliothèque a été composée à la main, et rien ne doit s'y déplacer ;
 * 2. un chevauchement de MOT est rédhibitoire : c'est le défaut qu'on corrige ;
 * 3. quand il FAUT bouger, on va au plus près, en préférant ne pas enterrer le
 *    mot dans un trait.
 *
 * À défaut de place libre, on garde la moins mauvaise : un mot décalé reste
 * lisible, un mot supprimé est une information perdue.
 */
export function placerTexte(
  texte: string,
  souhait: PoseTexte,
  mots: Boite[],
  formes: Boite[],
  zone: Zone = ZONE_TABLEAU,
): { pose: PoseTexte; boite: Boite } {
  const base = rentrerDansLaZone(texte, souhait, zone);
  const { w, h } = mesurerTexte(texte, base.fontSize);
  let retenue: { pose: PoseTexte; boite: Boite } | null = null;
  let meilleurCout = Number.POSITIVE_INFINITY;

  decalages(w, h).forEach((decalage, rang) => {
    const pose = rentrerDansLaZone(texte, {
      ...base,
      x: base.x + decalage.dx,
      y: base.y + decalage.dy,
    }, zone);
    const boite = boiteDuTexte(texte, pose);
    const surMot = mots.reduce((total, autre) => total + aireCommune(boite, autre), 0);
    const surForme = formes.reduce((total, autre) => total + aireCommune(boite, autre), 0);
    const cout = surMot * 1e6 + (rang === 0 ? 0 : rang * 1000 + surForme);
    if (cout < meilleurCout) {
      meilleurCout = cout;
      retenue = { pose, boite };
    }
  });

  return retenue || { pose: base, boite: boiteDuTexte(texte, base) };
}

function dedansOuAuDessus(
  label: string,
  cx: number,
  cy: number,
  largeur: number,
  hautDeLaForme: number,
): PoseTexte {
  // ~0,55 em par caractère pour une cursive : suffisant pour décider si ça tient.
  const tenteDedans = Math.min(TAILLE_MAX, (largeur * 0.9) / (label.length * 0.55));
  if (tenteDedans >= TAILLE_MIN) {
    return { x: cx, y: cy, fontSize: Math.round(tenteDedans), ancre: 'middle' };
  }
  return { x: cx, y: Math.max(TAILLE_MIN, hautDeLaForme - 6), fontSize: TAILLE_MIN, ancre: 'middle' };
}

/**
 * Le texte d'un élément, et l'endroit où il irait si le tableau était vide.
 *
 * C'est la règle d'avant, inchangée : un nom tient DANS sa forme quand il y
 * reste lisible, sinon il se pose au-dessus. Un professeur ne rapetisse pas
 * son écriture pour la faire tenir — il écrit à côté.
 */
export function souhaitDuTexte(el: ElementDessine): { texte: string; pose: PoseTexte } | null {
  if (el.type === 'text') {
    const texte = (el.text || el.label || '').trim();
    if (!texte) return null;
    return {
      texte,
      pose: { x: el.x || 0, y: el.y || 0, fontSize: el.fontSize || 15, ancre: el.align || 'start' },
    };
  }

  const label = (el.label || '').trim();
  if (!label) return null;

  switch (el.type) {
    case 'line':
    case 'path': {
      const pts = el.points || [];
      if (pts.length < 2) return null;
      return { texte: label, pose: { x: pts[0].x, y: pts[0].y - 8, fontSize: 13, ancre: 'start' } };
    }
    case 'arrow': {
      const pts = el.points || [];
      if (pts.length < 2) return null;
      const from = pts[0];
      const to = pts[pts.length - 1];
      return {
        texte: label,
        pose: { x: (from.x + to.x) / 2, y: (from.y + to.y) / 2 - 7, fontSize: 12, ancre: 'middle' },
      };
    }
    case 'rect': {
      const x = el.x || 0, y = el.y || 0, w = el.width || 100, h = el.height || 60;
      return { texte: label, pose: dedansOuAuDessus(label, x + w / 2, y + h / 2 + 5, w, y) };
    }
    case 'circle': {
      const cx = el.x || 0, cy = el.y || 0, r = el.radius || 35;
      return { texte: label, pose: dedansOuAuDessus(label, cx, cy + 4, r * 2, cy - r) };
    }
    // Les cinq formes de SVT portent leur nom SOUS la forme.
    case 'mitochondria':
      return { texte: label, pose: { x: (el.x || 0) + (el.width || 120) / 2, y: (el.y || 0) + (el.height || 60) + 18, fontSize: el.fontSize || 14, ancre: 'middle' } };
    case 'cell':
      return { texte: label, pose: { x: el.x || 0, y: (el.y || 0) + (el.radius || 80) + 20, fontSize: el.fontSize || 14, ancre: 'middle' } };
    case 'nucleus':
      return { texte: label, pose: { x: el.x || 0, y: (el.y || 0) + (el.radius || 40) + 18, fontSize: el.fontSize || 14, ancre: 'middle' } };
    case 'dna':
      return { texte: label, pose: { x: (el.x || 0) + (el.width || 40) / 2, y: (el.y || 0) + (el.height || 100) + 16, fontSize: el.fontSize || 14, ancre: 'middle' } };
    case 'membrane':
      return { texte: label, pose: { x: (el.x || 0) + (el.width || 150) / 2, y: (el.y || 0) + (el.height || 30) + 20, fontSize: el.fontSize || 14, ancre: 'middle' } };
    default:
      return null;
  }
}

/** L'encombrement du TRAIT d'un élément — sans son texte. */
export function boiteDeLaForme(el: ElementDessine): Boite | null {
  switch (el.type) {
    case 'line':
    case 'path':
    case 'arrow':
    case 'polyline':
    case 'polygon':
      return boiteDesPoints(el.points);
    case 'ellipse': {
      const rx = el.radiusX || (el.width || 60) / 2;
      const ry = el.radiusY || (el.height || 40) / 2;
      return { x1: (el.x || 0) - rx, y1: (el.y || 0) - ry, x2: (el.x || 0) + rx, y2: (el.y || 0) + ry };
    }
    case 'rect': {
      const x = el.x || 0, y = el.y || 0;
      return { x1: x, y1: y, x2: x + (el.width || 100), y2: y + (el.height || 60) };
    }
    case 'circle':
    case 'cell':
    case 'nucleus': {
      const parDefaut = el.type === 'cell' ? 80 : el.type === 'nucleus' ? 40 : 35;
      const r = el.radius || parDefaut;
      return { x1: (el.x || 0) - r, y1: (el.y || 0) - r, x2: (el.x || 0) + r, y2: (el.y || 0) + r };
    }
    case 'mitochondria':
    case 'dna':
    case 'membrane': {
      const x = el.x || 0, y = el.y || 0;
      return { x1: x, y1: y, x2: x + (el.width || 120), y2: y + (el.height || 60) };
    }
    default:
      return null;
  }
}

/**
 * Poser une salve d'éléments sur un tableau qui n'est pas vide.
 *
 * `deja` est ce que l'élève a sous les yeux — le croquis des minutes
 * précédentes. On le RELIT avant de tracer, exactement comme on relit le
 * tableau avant d'y ajouter une ligne.
 */
export function poserLesTextes(
  deja: EmpreinteElement[],
  elements: ElementDessine[],
  zone: Zone = ZONE_TABLEAU,
): Array<{ pose: PoseTexte; texte: string } | null> {
  const mots: Boite[] = deja.map(e => e.texte).filter((b): b is Boite => !!b);
  const formes: Boite[] = deja.map(e => e.forme).filter((b): b is Boite => !!b);
  const formesNouvelles = elements.map(boiteDeLaForme);

  return elements.map((el, i) => {
    const souhait = souhaitDuTexte(el);
    const propre = formesNouvelles[i];
    if (!souhait) {
      if (propre) formes.push(propre);
      return null;
    }
    // Sa PROPRE forme n'est pas un obstacle — le nom d'un rectangle s'écrit
    // dedans. Celles qui restent à tracer dans la même salve, elles, comptent.
    const obstacles = formes.concat(
      formesNouvelles.filter((boite, j): boite is Boite => !!boite && j > i),
    );
    const place = placerTexte(souhait.texte, souhait.pose, mots, obstacles, zone);
    mots.push(place.boite);
    if (propre) formes.push(propre);
    return { pose: place.pose, texte: souhait.texte };
  });
}

/** L'empreinte d'un élément une fois posé, pour la salve suivante. */
export function empreinte(
  el: ElementDessine,
  place: { pose: PoseTexte; texte: string } | null,
): EmpreinteElement {
  return {
    texte: place ? boiteDuTexte(place.texte, place.pose) : null,
    forme: boiteDeLaForme(el),
  };
}
