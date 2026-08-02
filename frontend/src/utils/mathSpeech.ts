/**
 * LaTeX → texte lisible à voix haute (français).
 *
 * Le tableau en direct lit ses propres lignes. Sans conversion, la synthèse
 * vocale prononcerait « dollar backslash l n parenthèse x » au lieu de
 * « logarithme népérien de x ». On ne vise pas une lecture exhaustive de tout
 * LaTeX : uniquement ce qui apparaît réellement dans un cours de 2ème Bac.
 */

/** Remplacements appliqués dans l'ordre (les plus spécifiques d'abord). */
const REPLACEMENTS: [RegExp, string][] = [
  // ── Fractions : \frac{a}{b} → « a sur b » ──
  [/\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, ' $1 sur $2 '],
  [/\\[tc]frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, ' $1 sur $2 '],

  // ── Racines ──
  [/\\sqrt\s*\[\s*3\s*\]\s*\{([^{}]*)\}/g, ' racine cubique de $1 '],
  [/\\sqrt\s*\{([^{}]*)\}/g, ' racine carrée de $1 '],

  // ── Fonctions usuelles ──
  [/\\ln(?![a-zA-Z])/g, ' logarithme népérien de '],
  [/\\log(?![a-zA-Z])/g, ' logarithme de '],
  [/\\exp(?![a-zA-Z])/g, ' exponentielle de '],
  [/\\sin(?![a-zA-Z])/g, ' sinus '],
  [/\\cos(?![a-zA-Z])/g, ' cosinus '],
  [/\\tan(?![a-zA-Z])/g, ' tangente '],
  [/\\lim(?![a-zA-Z])/g, ' limite '],
  [/\\int(?![a-zA-Z])/g, ' intégrale '],
  [/\\sum(?![a-zA-Z])/g, ' somme '],
  [/\\prod(?![a-zA-Z])/g, ' produit '],

  // ── Relations ──
  [/\\neq(?![a-zA-Z])/g, ' différent de '],
  [/\\leq(?![a-zA-Z])/g, ' inférieur ou égal à '],
  [/\\geq(?![a-zA-Z])/g, ' supérieur ou égal à '],
  [/\\approx(?![a-zA-Z])/g, ' environ égal à '],
  [/\\equiv(?![a-zA-Z])/g, ' équivalent à '],
  [/\\iff(?![a-zA-Z])/g, ' équivaut à '],
  [/\\implies(?![a-zA-Z])|\\Rightarrow(?![a-zA-Z])/g, ' donc '],
  [/\\rightarrow(?![a-zA-Z])|\\to(?![a-zA-Z])/g, ' tend vers '],
  [/\\in(?![a-zA-Z])/g, ' appartient à '],
  [/\\notin(?![a-zA-Z])/g, " n'appartient pas à "],
  [/\\subset(?![a-zA-Z])/g, ' inclus dans '],
  [/\\cup(?![a-zA-Z])/g, ' union '],
  [/\\cap(?![a-zA-Z])/g, ' inter '],

  // ── Opérateurs ──
  [/\\times(?![a-zA-Z])/g, ' fois '],
  [/\\cdot(?![a-zA-Z])/g, ' fois '],
  [/\\div(?![a-zA-Z])/g, ' divisé par '],
  [/\\pm(?![a-zA-Z])/g, ' plus ou moins '],

  // ── Symboles ──
  [/\\infty(?![a-zA-Z])/g, " l'infini "],
  [/\\pi(?![a-zA-Z])/g, ' pi '],
  [/\\alpha(?![a-zA-Z])/g, ' alpha '],
  [/\\beta(?![a-zA-Z])/g, ' bêta '],
  [/\\gamma(?![a-zA-Z])/g, ' gamma '],
  [/\\delta(?![a-zA-Z])/g, ' delta '],
  [/\\Delta(?![a-zA-Z])/g, ' delta '],
  [/\\theta(?![a-zA-Z])/g, ' thêta '],
  [/\\lambda(?![a-zA-Z])/g, ' lambda '],
  [/\\mu(?![a-zA-Z])/g, ' mu '],
  [/\\sigma(?![a-zA-Z])/g, ' sigma '],
  [/\\omega(?![a-zA-Z])/g, ' oméga '],
  [/\\varphi(?![a-zA-Z])|\\phi(?![a-zA-Z])/g, ' phi '],
  [/\\tau(?![a-zA-Z])/g, ' tau '],

  // ── Puissances courantes (avant le nettoyage générique de ^) ──
  [/\^\s*\{?\s*2\s*\}?/g, ' au carré '],
  [/\^\s*\{?\s*3\s*\}?/g, ' au cube '],
  [/\^\s*\{([^{}]*)\}/g, ' puissance $1 '],
  [/\^\s*(-?\w+)/g, ' puissance $1 '],

  // ── Indices : u_n → « u indice n » ──
  [/_\s*\{([^{}]*)\}/g, ' indice $1 '],
  [/_\s*(\w+)/g, ' indice $1 '],

  // ── Ensembles ──
  [/\\mathbb\s*\{R\}/g, ' R '],
  [/\\mathbb\s*\{N\}/g, ' N '],
  [/\\mathbb\s*\{Z\}/g, ' Z '],
  [/\\mathcal\s*\{([^{}]*)\}/g, ' $1 '],
  [/\\mathrm\s*\{([^{}]*)\}/g, ' $1 '],
  [/\\text\s*\{([^{}]*)\}/g, ' $1 '],
  [/\\vec\s*\{([^{}]*)\}/g, ' vecteur $1 '],

  // ── Structure : on retire ce qui ne se prononce pas ──
  [/\\left|\\right/g, ' '],
  [/\\quad|\\qquad|\\,|\\;|\\:|\\!/g, ' '],
  [/\\\\/g, ' '],
  [/\\begin\{[^}]*\}|\\end\{[^}]*\}/g, ' '],
];

/** Symboles isolés lus en toutes lettres. */
const SYMBOL_WORDS: [RegExp, string][] = [
  [/≠/g, ' différent de '],
  [/≤/g, ' inférieur ou égal à '],
  [/≥/g, ' supérieur ou égal à '],
  [/∞/g, " l'infini "],
  [/×/g, ' fois '],
  [/÷/g, ' divisé par '],
  [/±/g, ' plus ou moins '],
  [/√/g, ' racine de '],
  [/∈/g, ' appartient à '],
  [/⟺|⇔/g, ' équivaut à '],
  [/⇒|→/g, ' donc '],
];

/**
 * Transforme le contenu d'une ligne de tableau en texte prononçable.
 * Renvoie une chaîne vide si rien de lisible ne subsiste.
 */
export function toSpokenText(raw: string): string {
  if (!raw || typeof raw !== 'string') return '';

  let s = raw;

  // Les délimiteurs mathématiques ne se prononcent pas.
  s = s.replace(/\$\$/g, ' ').replace(/\$/g, ' ');
  s = s.replace(/\\\(|\\\)|\\\[|\\\]/g, ' ');

  for (const [re, out] of REPLACEMENTS) s = s.replace(re, out);
  for (const [re, out] of SYMBOL_WORDS) s = s.replace(re, out);

  // Commandes LaTeX résiduelles : on lit le nom plutôt que la barre oblique.
  s = s.replace(/\\([a-zA-Z]+)/g, ' $1 ');

  // Ponctuation technique qui parasite la lecture.
  s = s.replace(/[{}]/g, ' ');
  s = s.replace(/\s*\|\s*/g, ' ');
  s = s.replace(/&/g, ' ');

  // Opérateurs restants, uniquement entourés d'espaces pour ne pas casser
  // les mots (« c'est-à-dire » ne doit pas devenir « c'est moins à-dire »).
  s = s.replace(/\s=\s/g, ' égale ');
  s = s.replace(/\s\+\s/g, ' plus ');
  s = s.replace(/\s-\s/g, ' moins ');

  // Emojis et puces : muets.
  s = s.replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/gu, ' ');
  s = s.replace(/^[\s•·\-–—]+/, '');

  s = s.replace(/\s+/g, ' ').trim();

  // Une ligne qui ne contient plus que de la ponctuation n'est pas lue.
  if (!/[a-zA-ZÀ-ÿ0-9؀-ۿ]/.test(s)) return '';
  return s;
}

/** Estimation de durée (ms) quand la synthèse vocale n'est pas disponible. */
export function estimateSpeechMs(text: string, rate = 1): number {
  const words = (text || '').trim().split(/\s+/).filter(Boolean).length;
  if (words === 0) return 0;
  // ~170 mots/minute pour une diction de cours posée.
  const ms = (words / 170) * 60_000;
  return Math.max(700, Math.min(15_000, ms / rate));
}
