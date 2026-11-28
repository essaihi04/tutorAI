/**
 * Les nombres que la voix prononce (28 novembre 2026, l'utilisateur sur « Combien de α, combien de β⁻ ? » : « il doit
 * mettre le doigt et indiquer ce qui est dit ; ce qui est dit doit être allumé, surtout les chiffres »).
 *
 * La voix des cours dit les nombres en français, en toutes lettres (« deux cent trente-huit égale deux cent six plus
 * quatre y », « zéro virgule six cent quatre-vingt-treize »), au milieu de la darija. Cette fonction les retrouve dans
 * le texte parlé, avec leur place (le caractère où ils commencent) : le lecteur en tire l'instant où la voix les dit
 * (repères de la piste) et envoie alors `dit {nombre}` à la simulation, qui allume ce nombre là où il est écrit au
 * tableau (`shared/tableau/tableau.js`). Rien à écrire dans les cours : cela vaut pour toutes les diapositives.
 *
 * Ce qui n'est PAS pris pour un nombre :
 *  - « un » / « une » seuls, sauf après un mot de calcul ou de numéro (« égale un », « ب un », « flèche un ») ou avant
 *    « point » / « virgule » (« un point deux ») : c'est le plus souvent l'article ;
 *  - l'exposant d'une puissance (« dix puissance moins trois » : seul « dix » compte).
 */
export interface NombreDit {
  /** La valeur, écrite comme au tableau mais avec un point : « 238 », « 0.693 », « 4.002603 ». */
  valeur: string;
  /** La place du premier caractère du nombre dans le texte parlé. */
  i: number;
}

const VALEURS: Record<string, number> = {
  'zéro': 0, zero: 0, un: 1, une: 1, deux: 2, trois: 3, quatre: 4, cinq: 5, six: 6, sept: 7, huit: 8, neuf: 9, dix: 10,
  onze: 11, douze: 12, treize: 13, quatorze: 14, quinze: 15, seize: 16, vingt: 20, vingts: 20, trente: 30, quarante: 40,
  cinquante: 50, soixante: 60, cent: 100, cents: 100, mille: 1000,
};
/** Avant un « un » seul, ces mots en font un nombre. */
const AVANT_UN = new Set(['égale', 'egale', 'plus', 'moins', 'fois', 'sur', 'de', 'par', 'ب', 'point', 'flèche', 'fleche',
  'numéro', 'numero', 'question', 'étape', 'etape', 'figure', 'document', 'partie', 'exercice']);
const PUISSANCE = new Set(['puissance', 'exposant']);
const PONCTUATION = /[,;:.!?،؛؟()«»"]/;

interface Mot { t: string; i: number; fin: number; parties: string[]; nombre: boolean; chiffres: boolean }

function mots(parole: string): Mot[] {
  const re = /[0-9]+(?:[  ][0-9]{3})*(?:[.,][0-9]+)?|[A-Za-zÀ-ÿ]+(?:-[A-Za-zÀ-ÿ]+)*|[؀-ۿ]+/g;
  const out: Mot[] = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(parole))) {
    const t = m[0].toLowerCase(), chiffres = /^[0-9]/.test(t);
    const parties = chiffres ? [] : t.split('-');
    const nombre = !chiffres && parties.every(p => p in VALEURS || p === 'et') && parties.some(p => p in VALEURS);
    out.push({ t, i: m.index, fin: m.index + m[0].length, parties, nombre, chiffres });
  }
  return out;
}

/** Ajoute un mot de nombre à la valeur en cours ; null s'il ne peut pas la continuer (un autre nombre commence). */
function ajouter(etat: { total: number; cur: number; vide: boolean }, v: number): boolean {
  const { cur } = etat, r = cur % 100;
  if (v === 100) { if (!etat.vide && (r === 0 || r > 9)) return false; etat.cur = (cur || 1) * 100; }
  else if (v === 1000) { if (etat.total) return false; etat.total += (cur || 1) * 1000; etat.cur = 0; }
  else if (v === 20 && r === 4) etat.cur = cur - 4 + 80;                       // quatre-vingt
  else if (v >= 10 && v <= 16) { if (r !== 0 && r !== 60 && r !== 80) return false; etat.cur += v; }
  else if (v >= 20) { if (r !== 0) return false; etat.cur += v; }
  else {                                                                       // 0 à 9
    if (v === 0 && !etat.vide) return false;
    if (r % 10 !== 0 || (r >= 10 && r < 20 && r !== 10) || (etat.cur === 0 && !etat.vide && !etat.total)) return false;
    if (r === 10 && v < 7) return false;                                       // dix-sept, dix-huit, dix-neuf seulement
    etat.cur += v;
  }
  etat.vide = false;
  return true;
}

/** Lit un nombre entier à partir du mot `k` ; renvoie sa valeur et l'indice du mot suivant (null : pas un nombre). */
function entier(M: Mot[], k: number, parole: string): { v: number; suite: number } | null {
  if (M[k].chiffres) return null;
  const etat = { total: 0, cur: 0, vide: true };
  let j = k;
  for (; j < M.length; j++) {
    // « vingt et un », « soixante et onze » : le « et » entre une dizaine et « un » / « onze »
    if (j > k && M[j].t === 'et' && etat.cur % 100 >= 20 && etat.cur % 10 === 0 && ['un', 'une', 'onze'].includes(M[j + 1]?.t)) continue;
    if (!M[j].nombre) break;
    if (j > k && PONCTUATION.test(parole.slice(M[j - 1].fin, M[j].i))) break;
    const copie = { ...etat };
    let ok = true;
    for (const p of M[j].parties) { if (p === 'et') continue; if (!ajouter(etat, VALEURS[p])) { ok = false; break; } }
    if (!ok) { Object.assign(etat, copie); break; }
  }
  // « et » seul entre deux mots (« vingt et un ») : accepté seulement s'il est suivi d'un nombre
  if (j === k) return null;
  return { v: etat.total + etat.cur, suite: j };
}

const sansZeros = (s: string) => s.replace(/^0+(?=\d)/, '');
/** Un nombre écrit en chiffres : « 86 400 », « 0,693 » → « 86400 », « 0.693 ». */
export function normaliserNombre(s: string): string | null {
  const t = String(s ?? '').replace(/[  ]/g, '').replace(',', '.');
  if (!/^\d+(\.\d+)?$/.test(t)) return null;
  const [e, d] = t.split('.');
  return sansZeros(e) + (d !== undefined ? '.' + d : '');
}

export function nombresDits(parole: string): NombreDit[] {
  const M = mots(parole), out: NombreDit[] = [];
  let k = 0;
  while (k < M.length) {
    const mot = M[k];
    // l'exposant d'une puissance n'est pas un nombre écrit seul au tableau
    if (PUISSANCE.has(mot.t)) { k++; if (M[k]?.t === 'moins') k++; if (M[k]?.nombre) { const e = entier(M, k, parole); k = e ? e.suite : k + 1; } continue; }
    if (mot.chiffres) { const v = normaliserNombre(mot.t); if (v) out.push({ valeur: v, i: mot.i }); k++; continue; }
    if (!mot.nombre) { k++; continue; }
    const e = entier(M, k, parole);
    if (!e) { k++; continue; }
    let valeur = String(e.v), suite = e.suite;
    // la partie décimale : « virgule zéro zéro deux mille six cent trois » → ,002603
    if (M[suite]?.t === 'virgule' && M[suite + 1]?.nombre) {
      let j = suite + 1, dec = '';
      while (M[j]?.nombre && M[j].parties.length === 1 && VALEURS[M[j].parties[0]] === 0) { dec += '0'; j++; }
      if (M[j]?.nombre) { const d = entier(M, j, parole); if (d) { dec += String(d.v); j = d.suite; } }
      if (dec) { valeur += '.' + dec; suite = j; }
    }
    const seul = suite === k + 1 && mot.parties.length === 1 && (mot.t === 'un' || mot.t === 'une');
    if (seul) {
      const avant = M[k - 1]?.t, apres = M[k + 1]?.t;
      const colle = k > 0 && !PONCTUATION.test(parole.slice(M[k - 1].fin, mot.i));
      if (!((colle && avant && AVANT_UN.has(avant)) || apres === 'point' || apres === 'virgule')) { k = suite; continue; }
    }
    out.push({ valeur, i: mot.i });
    k = suite;
  }
  return out;
}
