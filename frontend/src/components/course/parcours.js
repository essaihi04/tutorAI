/**
 * Le parcours d'une diapositive à l'autre et le rejeu de la simulation après la réponse (18 novembre 2026).
 * Logique pure (sans React ni navigateur), testée par `tests/parcours-cours.test.mjs`. Deux formats optionnels de
 * `slide.concentration`, sans effet sur un cours qui ne les porte pas :
 *
 * 1. `apres_reponse` — la simulation s'arrête AVANT un moment décisif (le résultat), la question est posée, puis,
 *    la réponse donnée (juste, fausse après ses essais, ou passée), le tuteur rejoue la suite jusqu'au résultat.
 *    Un objet, ou une liste d'objets (un par question de la diapositive, chacun nommant sa `question`) :
 *      { question?: 'q' | 'e0' | 'e0s1' …,           // la question attendue (défaut : la première de la diapositive)
 *        etapes: [{ commande?, parametres?, repere? }], // ce que le tuteur fait, dans l'ordre (comme `variante`)
 *        sim_avant?: {…},                               // `set_parameters` envoyé tant que la question est ouverte
 *        duree_s?: number }                             // le temps laissé pour regarder (défaut 6 s)
 *    Les moments rejoués (`play_until {moment}` des étapes) sont RÉSERVÉS : le lecteur ne les joue pas avant la
 *    réponse à leur question, même si un `pointage`, une `variante` ou une question d'observation les demande.
 *
 * 2. `rappel` — la diapositive est un rappel de prérequis, sauté quand la question diagnostic qui le précède a été
 *    réussie du premier coup :
 *      { si_reussi: '<id de la diapositive diagnostic>' | ['<id>', …] }
 *    Sauté seulement en avançant (« Suite → ») et seulement si TOUTES les questions de chaque diapositive nommée sont
 *    justes au premier essai. Diagnostic sans question, passé, raté ou pas encore fait : le rappel est joué.
 */

/** Les clés des questions de la diapositive, dans l'ordre du tableau (`q`, `e{i}`, `e{i}s{j}`) — comme `questionsDeLaDiapo`. */
export function clesDesQuestions(slide) {
  const out = [];
  if (slide?.question?.prompt) out.push('q');
  (slide?.exercises || []).forEach((ex, i) => {
    if (ex?.type === 'qcm' && (ex.choices || []).length >= 2) out.push(`e${i}`);
    if (ex?.type === 'vrai_faux') (ex.statements || []).forEach((_, j) => out.push(`e${i}s${j}`));
  });
  return out;
}

/** Un rejeu lu et contrôlé ; null s'il est inutilisable (la diapositive se joue alors comme avant). */
function lireRejeu(r, cles, defaut) {
  if (!r || !Array.isArray(r.etapes) || !r.etapes.length) return null;
  const question = r.question || defaut;
  if (!question || !cles.includes(question)) return null;
  const duree = Number(r.duree_s);
  return { question, etapes: r.etapes, sim_avant: r.sim_avant || null, duree_s: Number.isFinite(duree) && duree >= 0 ? duree : 6 };
}

/**
 * Les rejeux de la diapositive (`apres_reponse` : un objet, ou une liste, un par question). Le premier vise par défaut
 * la première question ; les suivants doivent nommer la leur. Deux rejeux sur la même question : le premier compte.
 */
export function rejeuxDe(slide) {
  const brut = slide?.concentration?.apres_reponse;
  const liste = Array.isArray(brut) ? brut : brut ? [brut] : [];
  const cles = clesDesQuestions(slide);
  const vus = new Set();
  const out = [];
  liste.forEach((r, i) => {
    const x = lireRejeu(r, cles, i === 0 ? cles[0] : undefined);
    if (x && !vus.has(x.question)) { vus.add(x.question); out.push(x); }
  });
  return out;
}

/** Le rejeu attaché à la question `cle` (sans `cle` : le premier), ou null. */
export function rejeuDe(slide, cle) {
  const liste = rejeuxDe(slide);
  return (cle === undefined ? liste[0] : liste.find(r => r.question === cle)) || null;
}

/** Les moments qu'un rejeu joue (les `play_until` de ses étapes). */
export function momentsDuRejeu(rejeu) {
  const out = new Set();
  (rejeu?.etapes || []).forEach(e => { if (e?.commande === 'play_until' && e.parametres?.moment != null) out.add(String(e.parametres.moment)); });
  return out;
}

/** Les moments que seuls les rejeux jouent. `faits` : les questions dont le rejeu a eu lieu (leurs moments sont libres). */
export function momentsReserves(slide, faits) {
  const out = new Set();
  rejeuxDe(slide).forEach(r => { if (!faits || !faits.has(r.question)) momentsDuRejeu(r).forEach(m => out.add(m)); });
  return out;
}

/** Une commande qui jouerait un moment réservé avant la réponse : le lecteur la saute. */
export function commandeReservee(commande, parametres, reserves) {
  return commande === 'play_until' && !!reserves && reserves.size > 0 && parametres?.moment != null && reserves.has(String(parametres.moment));
}

/** Le temps du rejeu : le temps de regarder, plus une seconde par geste après le premier (la main du tuteur va au bouton). */
export function dureeDuRejeuMs(rejeu) {
  if (!rejeu) return 0;
  return Math.round((rejeu.duree_s + Math.max(0, rejeu.etapes.length - 1)) * 1000);
}

/** Une question gardée en mémoire est close (juste, fausse après ses essais, passée) : le rejeu peut être joué. */
export function questionClose(etat, essaisMax = 2) {
  if (!etat) return false;
  if (etat.passee) return true;
  const r = etat.retour, t = etat.tentative ?? 1;
  return r?.correct === true || (r?.correct === false && t > essaisMax);
}

/** Les diapositives diagnostic d'un rappel (`concentration.rappel.si_reussi`), ou [] si la diapositive n'est pas un rappel. */
export function diagnosticsDuRappel(slide) {
  const s = slide?.concentration?.rappel?.si_reussi;
  const liste = Array.isArray(s) ? s : s ? [s] : [];
  return liste.filter(x => typeof x === 'string' && x.trim()).map(x => x.trim());
}

/** Juste du premier coup : la réponse est juste et c'était le premier essai (ni indice, ni passage). */
export function justeDuPremierCoup(etat) {
  return !!etat && !etat.passee && etat.retour?.correct === true && (etat.tentative ?? 1) === 1;
}

/**
 * Le rappel peut-il être sauté ? `parId` : les diapositives du cours par id ; `lireEtat(slideId, cle)` : l'état gardé de
 * la question (`localStorage`, clé `reponse:<deck>:<diapo>:<cle>`). Toutes les questions de chaque diagnostic nommé
 * doivent être justes du premier coup ; un diagnostic introuvable ou sans question ne permet jamais le saut.
 */
export function rappelASauter(slide, parId, lireEtat) {
  const diags = diagnosticsDuRappel(slide);
  if (!diags.length) return false;
  return diags.every(id => {
    const d = parId.get ? parId.get(id) : parId[id];
    const cles = clesDesQuestions(d);
    return cles.length > 0 && cles.every(c => justeDuPremierCoup(lireEtat(id, c)));
  });
}

/**
 * La diapositive où « Suite → » mène depuis `index` : la suivante, après les rappels à sauter. Renvoie
 * `{ index, sautes }` (`sautes` : les ids des rappels sautés, dans l'ordre). `index` vaut `slides.length` si le cours
 * est fini. `revus` : les rappels que l'élève a demandé à revoir (« 🔁 Revoir le rappel ») — jamais resautés.
 */
export function diapoSuivante(slides, index, lireEtat, revus) {
  const parId = new Map(slides.map(s => [s.id, s]));
  const sautes = [];
  let i = index + 1;
  while (i < slides.length) {
    const s = slides[i];
    if (revus && revus.has(s.id)) break;
    if (!rappelASauter(s, parId, lireEtat)) break;
    sautes.push(s.id);
    i += 1;
  }
  return { index: i, sautes };
}
