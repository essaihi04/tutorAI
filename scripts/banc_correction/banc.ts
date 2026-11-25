/** Banc d'essai du mode classe (25/11/2026) : chaque photo passe par la même lecture (`/lire`) et la même correction
 *  (`/corriger`, notes calculées dans la page) qu'en classe, sur le site en ligne, dans une séance de test qui est
 *  fermée à la fin. La note du modèle est comparée à la note du prof (`note_prof` de copies.json).
 *
 *  1. python -X utf8 scripts/banc_correction/rendre.py <dossier>   (copies.json copié dans <dossier> : photos/*.jpg)
 *  2. depuis frontend/ : node -e "require('esbuild').build({entryPoints:['../scripts/banc_correction/banc.ts'],
 *     bundle:true,platform:'node',format:'cjs',outfile:'<dossier>/banc.cjs',jsx:'automatic',
 *     loader:{'.css':'empty','.png':'empty','.svg':'empty','.webp':'empty','.mp3':'empty','.jpg':'empty'},
 *     external:['react','react-dom','react/jsx-runtime']})"
 *  3. copier lancer.cjs dans <dossier>, puis : node <dossier>/lancer.cjs <dossier> [01,07…] [_suffixe]
 *     → <dossier>/resultats<_suffixe>.json (une ligne par copie : lu, note, détails). */
import { readFileSync, writeFileSync } from 'fs';
import { EXAMEN, type PartieExamen, type QuestionExamen } from '../../frontend/src/publication/tronc-commun/sujet';
import { SUJET_PHYSIQUE, SUJET_CHIMIE } from '../../frontend/src/publication/bac2pcf/sujets';
import { configExamen, corpsCorrection, etatDeCorrection, noterValeur, noterChoix, texteDuSujet, utiliserSujet, type CorrectionTuteur, type Etat } from '../../frontend/src/publication/tronc-commun/Examen';
import { choixDuTexte } from '../../frontend/src/components/course/photoTelephone';

const SITE = 'https://moalim.online/api/v1/public/classe';
const dossier = process.argv[2];
const seulement = process.argv[3] ? new Set(process.argv[3].split(',')) : null;
type Copie = { sujet: string; id: string; niveau: string; note_prof: number; photo: string };
const copies = (JSON.parse(readFileSync(`${dossier}/copies.json`, 'utf8')) as Copie[]).filter(c => !seulement || seulement.has(c.photo.slice(0, 2)));
const SUJETS: Record<string, { sujet: unknown; matiere: string; retour: string; cle: string }> = {
  svt_tc: { sujet: { ...EXAMEN, programme: 'la sortie écologique ; les facteurs édaphiques (texture et structure, propriétés chimiques, propriétés hydriques du sol)' }, matiere: 'svt', retour: 'Tronc Commun', cle: 'examen' },
  physique: { sujet: SUJET_PHYSIQUE, matiere: 'physique', retour: '2ᵉ Bac PC', cle: 'examen_physique' },
  chimie: { sujet: SUJET_CHIMIE, matiere: 'chimie', retour: '2ᵉ Bac PC', cle: 'examen_chimie' },
};
const lettre = (k: number) => String.fromCharCode(65 + k);

/** copie de motsDuSujet (Classe.tsx) */
function motsDuSujet(p: PartieExamen, q: QuestionExamen) {
  const sources = [texteDuSujet(p), q.texte, ...('correction' in q ? q.correction : []), ...('elements' in q ? (q as { elements: string[] }).elements : [])];
  if (q.genre === 'valeur') sources.push(q.grandeur, ...q.unites);
  if (q.genre === 'qcm') sources.push(...q.items.flatMap(it => it.choix));
  if (q.genre === 'histogramme') sources.push(...q.especes.flat());
  if (q.genre === 'triangle') sources.push(...q.choix);
  const vus = new Set<string>(); const mots: string[] = [];
  for (const m of sources.join(' ').split(/[\s,;:.!?«»"“”()[\]]+/)) {
    const t = m.replace(/^['’]+|['’]+$/g, '');
    if (t.length < 2 || /^\d+([.,]\d+)?$/.test(t) || vus.has(t.toLowerCase())) continue;
    vus.add(t.toLowerCase()); mots.push(t);
  }
  const grandeurs = sources.join(' ').match(/\b[A-Za-z]{1,3}\([A-Za-z0-9]{1,3}\)/g) || [];
  return [...new Set(grandeurs), ...mots].join(' ').slice(0, 1900);
}

async function appel<T>(chemin: string, corps: unknown, methode = 'POST', entetes: Record<string, string> = {}): Promise<T> {
  for (let essai = 0; ; essai++) {
    const r = await fetch(`${SITE}${chemin}`, { method: methode, headers: { 'Content-Type': 'application/json', ...entetes }, body: corps == null ? undefined : JSON.stringify(corps) });
    if (r.ok) return r.json() as Promise<T>;
    if (essai >= 2 || r.status < 500) throw new Error(`${r.status} ${await r.text()}`);
    await new Promise(f => setTimeout(f, 3000));
  }
}

(async () => {
  const { code, cle_prof } = await appel<{ code: string; cle_prof: string }>('', { sujet: 'banc-essai' });
  console.log('séance de test', code);
  const resultats: unknown[] = [];
  try {
    for (const c of copies) {
      const s = SUJETS[c.sujet];
      utiliserSujet({ sujet: s.sujet as never, piste: () => undefined, suivi: false, matiere: s.matiere, retour: s.retour, cle: s.cle });
      const { p, q } = configExamen().questions.find(x => x.q.id === c.id)!;
      const enonceOcr = q.genre === 'qcm' || q.genre === 'vf'
        ? `${q.texte} ${q.items.map((it, k) => `${String.fromCharCode(97 + k)}) ${it.texte}${q.genre === 'qcm' ? ' ' + (it as { choix: string[] }).choix.map((ch, m) => `${lettre(m)}. ${ch}`).join(' ') : ''}`).join(' ')}`
        : q.genre === 'histogramme' ? `${q.texte} Espèces et indices : ${q.especes.map(([n, i]) => `${n} ${i}`).join(' ; ')}` : q.texte;
      const image = 'data:image/jpeg;base64,' + readFileSync(`${dossier}/photos/${c.photo}`).toString('base64');
      const t0 = Date.now();
      let lu = '', etat: Etat | null = null, erreur = '';
      try {
        lu = (await appel<{ texte: string }>(`/${code}/lire`, { image_b64: image, image_mime: 'image/jpeg', question: q.id, enonce: enonceOcr.slice(0, 1500),
          titre: p.titre.slice(0, 300), matiere: s.matiere, niveau: configExamen().sujet.niveau, vocabulaire: motsDuSujet(p, q) })).texte;
        if (q.genre === 'qcm' || q.genre === 'vf') etat = noterChoix(q, choixDuTexte(q.genre, q.items.length, lu));
        else if (q.genre === 'valeur') etat = await noterValeur(p, q, lu, corps => appel<CorrectionTuteur>(`/${code}/corriger`, { ...corps, question: { ...corps.question, photo: true } }));
        else {
          const corps = q.genre === 'redaction'
            ? (() => { const k = corpsCorrection(p, q, lu); return { ...k, question: { ...k.question, photo: true } }; })()
            : { diapo: { title: `${configExamen().sujet.niveau} — ${p.titre}`, speech: '' },
                question: { type: 'open', enonce: enonceOcr.slice(0, 1500), attendu: q.correction.join(' '), matiere: s.matiere, bareme: q.points, elements: q.correction, photo: true },
                reponse: lu.slice(0, 4000), tentative: 2, verdict: null };
          etat = etatDeCorrection(q, lu, await appel<CorrectionTuteur>(`/${code}/corriger`, corps));
        }
      } catch (e) { erreur = (e as Error).message.slice(0, 300); }
      const r = { ...c, genre: q.genre, points: q.points, lu, note: etat?.note ?? null, verdict: etat?.verdict ?? null, retour: etat?.retour ?? '',
        details: etat?.details ?? [], erreur, secondes: Math.round((Date.now() - t0) / 1000) };
      resultats.push(r);
      console.log(`${c.photo}  prof ${c.note_prof}  modèle ${etat?.note ?? '—'} / ${q.points}  ${erreur}`);
      writeFileSync(`${dossier}/resultats${process.argv[4] || ''}.json`, JSON.stringify(resultats, null, 1));
    }
  } finally {
    await appel(`/${code}`, null, 'DELETE', { 'X-Prof': cle_prof }).catch(() => {});
  }
})();
