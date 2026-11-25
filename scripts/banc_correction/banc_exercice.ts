/** Banc d'essai « une photo pour tout l'exercice » (25/11/2026) : la feuille est lue une fois (`/lire`, l'énoncé de
 *  toutes les questions), découpée par decouperParQuestions, puis chaque question est notée comme dans PhotoExercice
 *  (Classe.tsx). Même construction et même lancement que banc.ts ; copies : copies_exercice.json
 *  ({ sujet, exercice: début du titre de la partie, texte, notes_prof: { id: note } }). */
import { readFileSync, writeFileSync } from 'fs';
import { EXAMEN, type PartieExamen, type QuestionExamen } from '../../frontend/src/publication/tronc-commun/sujet';
import { SUJET_PHYSIQUE, SUJET_CHIMIE } from '../../frontend/src/publication/bac2pcf/sujets';
import { SUJET_TCF } from '../../frontend/src/publication/tcf/sujet';
import { choixLus, configExamen, corpsCorrection, decouperParQuestions, etatDeCorrection, noterChoix, noterValeur, texteDuSujet, utiliserSujet, type CorrectionTuteur, type Etat } from '../../frontend/src/publication/tronc-commun/Examen';
import { choixDuTexte } from '../../frontend/src/components/course/photoTelephone';

const SITE = 'https://moalim.online/api/v1/public/classe';
const dossier = process.argv[2];
type Copie = { sujet: string; exercice: string; texte: string; notes_prof: Record<string, number>; photo: string };
const copies = JSON.parse(readFileSync(`${dossier}/copies.json`, 'utf8')) as Copie[];
const SUJETS: Record<string, { sujet: unknown; matiere: string; retour: string; cle: string }> = {
  svt_tc: { sujet: { ...EXAMEN, programme: 'la sortie écologique ; les facteurs édaphiques' }, matiere: 'svt', retour: 'Tronc Commun', cle: 'examen' },
  physique: { sujet: SUJET_PHYSIQUE, matiere: 'physique', retour: '2ᵉ Bac PC', cle: 'examen_physique' },
  chimie: { sujet: SUJET_CHIMIE, matiere: 'chimie', retour: '2ᵉ Bac PC', cle: 'examen_chimie' },
  tcf: { sujet: SUJET_TCF, matiere: 'physique', retour: 'Tronc Commun PC', cle: 'examen_tcf' },
};
const lettre = (k: number) => String.fromCharCode(65 + k);
const enonceLecture = (q: QuestionExamen) => q.genre === 'qcm' || q.genre === 'vf'
  ? `${q.texte} ${q.items.map((it, k) => `${String.fromCharCode(97 + k)}) ${it.texte}${q.genre === 'qcm' ? ' ' + (it as { choix: string[] }).choix.map((c, m) => `${lettre(m)}. ${c}`).join(' ') : ''}`).join(' ')}`
  : q.genre === 'histogramme' ? `${q.texte} Espèces et indices : ${q.especes.map(([n, i]) => `${n} ${i}`).join(' ; ')}` : q.texte;
const motsDuSujet = (p: PartieExamen) => [...new Set([texteDuSujet(p), ...p.questions.map(q => q.texte)].join(' ').split(/[\s,;:.!?«»"“”()[\]]+/).filter(m => m.length > 1 && !/^\d+([.,]\d+)?$/.test(m)))].join(' ').slice(0, 1900);

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
  const sortie: unknown[] = [];
  try {
    for (const c of copies) {
      const s = SUJETS[c.sujet];
      utiliserSujet({ sujet: s.sujet as never, piste: () => undefined, suivi: false, matiere: s.matiere, retour: s.retour, cle: s.cle });
      const p = configExamen().sujet.parties.find(x => x.titre.startsWith(c.exercice))!;
      const image = 'data:image/jpeg;base64,' + readFileSync(`${dossier}/photos/${c.photo}`).toString('base64');
      const enonce = p.questions.map(q => `${q.id}) ${enonceLecture(q)}`).join(' | ');
      const lu = (await appel<{ texte: string }>(`/${code}/lire`, { image_b64: image, image_mime: 'image/jpeg', question: '',
        enonce: `Toutes les questions de l'exercice, chaque réponse commence par son numéro : ${enonce}`.slice(0, 1500), titre: p.titre,
        matiere: s.matiere, niveau: configExamen().sujet.niveau, vocabulaire: motsDuSujet(p) })).texte;
      const parties = decouperParQuestions(lu, p.questions.map(q => q.id));
      const corriger = (corps: { question: object }) => appel<CorrectionTuteur>(`/${code}/corriger`, { ...corps, question: { ...corps.question, photo: true } });
      const questions = [];
      for (const q of p.questions) {
        const t = parties[q.id];
        let e: Etat;
        if (q.genre === 'qcm' || q.genre === 'vf') e = noterChoix(q, choixLus(q, t, choixDuTexte(q.genre, q.items.length, t)));
        else if (!t.trim()) e = { fait: true, note: 0, verdict: 'faux', retour: 'rien trouvé' };
        else if (q.genre === 'valeur') e = await noterValeur(p, q, t, corriger);
        else if (q.genre === 'redaction') e = etatDeCorrection(q, t, await corriger(corpsCorrection(p, q, t)));
        else e = etatDeCorrection(q, t, await corriger({ diapo: { title: p.titre, speech: '' }, question: { type: 'open', enonce: enonceLecture(q), attendu: q.correction.join(' '),
          matiere: s.matiere, bareme: q.points, elements: q.correction }, reponse: t, tentative: 2, verdict: null } as never));
        questions.push({ id: q.id, points: q.points, prof: c.notes_prof[q.id], note: e.note ?? 0, partie: t, retour: e.retour });
        console.log(`${c.photo} ${q.id}: prof ${c.notes_prof[q.id]} modèle ${e.note ?? 0} / ${q.points}   « ${t.replace(/\n/g, ' / ').slice(0, 70)} »`);
      }
      sortie.push({ ...c, lu, questions });
      writeFileSync(`${dossier}/resultats.json`, JSON.stringify(sortie, null, 1));
    }
  } finally {
    await appel(`/${code}`, null, 'DELETE', { 'X-Prof': cle_prof }).catch(() => {});
  }
})();
