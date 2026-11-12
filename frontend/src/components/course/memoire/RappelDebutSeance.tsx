import { useEffect, useRef, useState } from 'react';
import QuestionMemoire, { CRAIE, type ResultatQuestion } from './QuestionMemoire';
import { lireRappels, noter, type RappelsDuJour } from './api';
import type { ReactionPreparee } from '../types';
import { direTexte, jouerReaction } from './voix';

/**
 * Les 3 minutes de rappel qui ouvrent chaque séance (skill `suivi-des-acquis`, section 6) : 3 à 5 questions des
 * compétences déjà vues dans la MÊME matière, les plus en retard d'abord, sans le cours et sans aide. Chaque réponse
 * est notée (compétence, marche, jours depuis la dernière fois, réponse, verdict, temps de réponse : le serveur
 * complète). Un rappel raté = « on la revoit bientôt », jamais une marque rouge.
 *
 * `rappels` : déjà lus (début de séance, `lireDebutSeance`) ; sinon `matiere` : lus ici (la notification de l'accueil).
 */
export default function RappelDebutSeance({ rappels: donnes, matiere, onFini, onDire = direTexte, onJouer = jouerReaction, libelleFin = 'Commencer le cours →' }: {
  rappels?: RappelsDuJour; matiere?: string; onFini: () => void; libelleFin?: string;
  onDire?: (parole: string) => void; onJouer?: (r: ReactionPreparee) => void;
}) {
  const [rappels, setRappels] = useState<RappelsDuJour | null>(donnes || null);
  const [i, setI] = useState(0);
  const [mot, setMot] = useState('');
  const [bilan, setBilan] = useState<{ premier: number; total: number }>({ premier: 0, total: 0 });
  const fini = useRef(false);

  useEffect(() => {
    if (donnes || !matiere) return;
    lireRappels(matiere).then(setRappels).catch(() => setRappels({ matiere, nom_matiere: matiere, questions: [], minutes: 0 }));
  }, [donnes, matiere]);
  // rien à rappeler : on passe tout de suite au cours
  useEffect(() => { if (rappels && !rappels.questions.length && !fini.current) { fini.current = true; onFini(); } }, [rappels]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!rappels) return <p className="p-6 text-white/50" style={{ fontFamily: 'system-ui, sans-serif' }}>Un instant…</p>;
  const qs = rappels.questions;
  if (!qs.length) return null;
  const termine = i >= qs.length;
  const r = qs[Math.min(i, qs.length - 1)];

  const resultat = (res: ResultatQuestion) => {
    setBilan(b => ({ premier: b.premier + (res.correct === true ? 1 : 0), total: b.total + 1 }));
    setMot(res.passee ? 'Passée : on la revoit bientôt.' : res.correct === true ? 'Bien ancré.' : res.correct_2 === true ? 'Retrouvé : on la consolide.' : res.correct === null ? '' : 'On la revoit bientôt.');
    void noter({
      evenement: 'rappel', cours_id: r.cours_id, competence_id: r.competence_id, rappel_id: r.question.id, matiere: rappels.matiere,
      enonce: r.question.prompt, type: r.question.type, en_avance: r.en_avance,
      reponse: res.reponse, reponse_2: res.reponse_2, correct: res.correct, correct_2: res.correct_2 ?? null, duree_s: res.duree_s,
      passee: res.passee || undefined,
    }).then(x => {
      if (x?.prochaine && res.correct === true) {
        const jours = Math.round((new Date(x.prochaine).getTime() - Date.now()) / 86_400_000) + 1;
        if (jours > 1) setMot(`Bien ancré : on la revoit dans ${jours} jours.`);
      }
    });
  };

  return (
    <div className="relative flex h-full min-h-0 flex-col gap-4 overflow-y-auto rounded-2xl border border-white/15 bg-[#14201a]/95 p-5 text-white md:p-7">
      <div className="flex flex-wrap items-center gap-2 text-xs text-white/60" style={{ fontFamily: 'system-ui, sans-serif' }}>
        <span className="rounded-full bg-amber-300/15 px-2.5 py-1 text-amber-100">🔁 Rappel de {rappels.nom_matiere}</span>
        <span className="rounded-full bg-white/10 px-2.5 py-1">{termine ? qs.length : i + 1}/{qs.length}</span>
        <span className="flex gap-0.5">{qs.map((_, k) => <span key={k} className={`h-1.5 w-4 rounded-full ${k < i ? 'bg-emerald-300/70' : k === i ? 'bg-cyan-300' : 'bg-white/20'}`} />)}</span>
        <span className="ml-auto text-white/45">~{rappels.minutes} min</span>
      </div>
      {!termine && (
        <>
          <p className="text-sm text-white/55" style={{ fontFamily: 'system-ui, sans-serif' }}>
            {r.cours_titre} · <span className="text-white/75">{r.competence}</span>
          </p>
          <QuestionMemoire key={`${r.cours_id}:${r.competence_id}`} mode="rappel" question={r.question} titre={r.cours_titre} deckId={r.cours_id}
            onDire={onDire} onJouer={onJouer} reponses={r.question.reponses} onResultat={resultat}
            suggestions={{ deck_id: r.cours_id, slide_id: r.competence_id, cle: r.question.id }} onSuite={() => { setMot(''); setI(k => k + 1); }}
            libelleSuite={i + 1 < qs.length ? 'Suite →' : 'Voir le bilan →'} />
          {mot && <p className="text-sm text-white/60" style={{ fontFamily: 'system-ui, sans-serif' }}>{mot}</p>}
        </>
      )}
      {termine && (
        <div className="flex flex-1 flex-col items-center justify-center gap-4 text-center">
          <p className="text-3xl" style={{ fontFamily: CRAIE, color: '#fef3c7' }}>
            {bilan.premier === bilan.total ? 'Tout est resté en mémoire 👏' : `${bilan.premier} sur ${bilan.total} retrouvés du premier coup`}
          </p>
          <p className="max-w-md text-sm text-white/60" style={{ fontFamily: 'system-ui, sans-serif' }}>
            {bilan.premier === bilan.total ? 'Ces notions reviendront plus tard, plus espacées.' : 'Les autres reviennent bientôt : c’est en les retrouvant plusieurs fois qu’elles restent.'}
          </p>
          <button type="button" autoFocus onClick={() => { if (!fini.current) { fini.current = true; onFini(); } }}
            className="rounded-full bg-cyan-400/90 px-7 py-3 text-base font-bold text-slate-950 shadow-lg hover:bg-cyan-300" style={{ fontFamily: 'system-ui, sans-serif' }}>
            {libelleFin}
          </button>
        </div>
      )}
    </div>
  );
}
