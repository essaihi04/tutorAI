/** Une photo de tout l'exercice (25/11/2026) : la copie lue, découpée entre les questions de l'exercice. Chaque réponse
 *  commence par le repère de sa question (« 1-5) », « 1.5 », « Q1-5 », « 3-a) », « 2) », ou « 5) » après « Exercice 1 ») ;
 *  le texte avant le premier repère va à la première question quand elle n'a pas de repère.
 *  → { id: texte de la réponse } ('' : rien trouvé pour cette question). */
export function decouperParQuestions(texte: string, ids: string[]): Record<string, string> {
  const lignes = texte.split(/\r?\n/);
  const motif = (id: string) => {
    const [a, b] = id.split('-');
    const q = '^\\s*(?:q(?:uestion)?\\s*)?';
    if (b === undefined) return new RegExp(`${q}${a}\\s*[)\\]:.–-](?!\\s*\\d)`, 'i');
    if (/^\d+$/.test(b)) return new RegExp(`${q}${a}\\s*[-.]\\s*${b}(?!\\d)\\s*[)\\]:.]?(?=\\s|$)`, 'i');
    return new RegExp(`${q}${a}\\s*[-.]?\\s*${b}\\s*[)\\]:.]`, 'i');
  };
  const motifs = ids.map(id => ({ id, re: motif(id) }));
  // « 5) » après « Exercice 1 » : la question 1-5
  let exercice: string | null = null;
  const debuts: { ligne: number; id: string }[] = [];
  const vus = new Set<string>();
  lignes.forEach((l, k) => {
    const ex = l.trim().match(/^ex(?:ercice|\.)?\s*(\d+)\b/i);
    if (ex) exercice = ex[1];
    let trouve = motifs.find(m => !vus.has(m.id) && m.re.test(l));
    if (!trouve && exercice) {
      const un = l.trim().match(/^(\d+)\s*[)\]:]/);
      if (un) trouve = motifs.find(m => !vus.has(m.id) && m.id === `${exercice}-${un[1]}`);
    }
    if (trouve) { vus.add(trouve.id); debuts.push({ ligne: k, id: trouve.id }); }
  });
  const out: Record<string, string> = Object.fromEntries(ids.map(id => [id, '']));
  debuts.forEach((d, i) => {
    const fin = i + 1 < debuts.length ? debuts[i + 1].ligne : lignes.length;
    out[d.id] = lignes.slice(d.ligne, fin).join('\n').trim();
  });
  // aucun repère : une seule question reçoit tout ; le texte avant le premier repère, à la première question sans repère
  const avant = lignes.slice(0, debuts.length ? debuts[0].ligne : lignes.length).join('\n').trim();
  if (avant) {
    const libre = ids.find(id => !out[id]);
    if (!debuts.length && ids.length === 1) out[ids[0]] = avant;
    else if (libre && libre === ids[0]) out[libre] = avant;
  }
  return out;
}
