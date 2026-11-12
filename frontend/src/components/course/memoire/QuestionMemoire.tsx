import { useEffect, useMemo, useRef, useState } from 'react';
import ChampReponse from '../SaisieReponse';
import { jugerReponseLibre, type QuestionMemoire as Q, type ReponsesPreparees } from './api';
import type { Demonstration, ReactionPreparee } from '../types';
import type { CleSuggestions } from '../ClavierFlottant';
import DemonstrationPleine, { type LectureDemo } from '../DemonstrationPleine';
import { Formule } from '../Formule';
import { attendreLaFin, lireDemonstration, lireEnonce, taire } from './voix';

/**
 * Une question du cycle de mémoire : rappel de début de séance, « retrouver » d'un bloc (cahier fermé) ou exercice
 * du bloc. QCM et vrai/faux se corrigent tout de suite ; une réponse libre (écrite, dite ou photographiée) est jugée
 * en direct. Un essai de plus si le premier est faux ; puis la bonne réponse, calmement : jamais une marque rouge.
 */
export const CRAIE = "'Patrick Hand', 'Caveat', cursive";

/** « y_M(t) », « lim_{x→1} » : jamais de « _ » devant l'élève (module commun). */
export { Formule };

export interface ResultatQuestion {
  reponse: string; reponse_2?: string;
  /** premier essai ; `correct_2` : le second. `null` : rien de jugeable (le juge ne répondait pas). */
  correct: boolean | null; correct_2?: boolean | null;
  /** secondes jusqu'à la première réponse */
  duree_s: number;
  /** l'élève a passé la question (12 novembre 2026) : `correct: null`, ni juste ni erreur */
  passee?: boolean;
}

type Mode = 'rappel' | 'retrouver' | 'exercice';

const choixDe = (q: Q): string[] | null => {
  if (q.options?.length) return q.options;
  if (q.choices?.length) return q.choices;
  if (q.type === 'vrai_faux') return ['Vrai', 'Faux'];
  return null;
};

const REFLECHIS_S = 8;

/** La correction d'un « retrouver » écrite au tableau : la formule attendue coupée en lignes, puis l'explication. */
function correctionDe(attendu: string, explication?: string): Demonstration {
  const lignes = [...attendu.split(/\s*(?:[;\n]|(?<=\.)\s+(?=[A-ZÀ-Ý]))\s*/), ...(explication ? [explication] : [])]
    .map(t => t.trim()).filter(Boolean).map(texte => ({ texte, mot: '' }));
  return { parole: lignes.map(l => l.texte).join(' '), lignes };
}

/** Sans piste : les lignes s'écrivent à la craie, une toutes les 2,5 s (la voix vient de dire la réaction). */
function lectureMuette(d: Demonstration): LectureDemo {
  const n = Math.max(1, d.parole.length), duree = d.lignes.length * 2500 + 800, t0 = performance.now();
  let finir: () => void = () => {};
  const fin = new Promise<void>(ok => { finir = ok; });
  const id = window.setTimeout(() => finir(), duree);
  return { position: () => Math.min(1, (performance.now() - t0) / duree) * n, fin, arreter: () => { window.clearTimeout(id); finir(); } };
}

export default function QuestionMemoire({ question, mode, titre = '', deckId, onResultat, onSuite, onDire, onJouer, reponses, libelleSuite = 'Suite →', suggestions }: {
  question: Q; mode: Mode; titre?: string; deckId?: string;
  /** où chercher les suggestions du clavier (bloc ou compétence, et la clé de la question) */
  suggestions?: CleSuggestions;
  onResultat: (r: ResultatQuestion) => void; onSuite: () => void; libelleSuite?: string;
  /** la voix en direct (réponse libre jugée) ; `onJouer` : une réaction préparée (sa piste, sans serveur) */
  onDire?: (parole: string) => void; onJouer?: (r: ReactionPreparee) => void;
  /** réactions préparées à chaque option : `{option: {juste | 1 | 2}}` */
  reponses?: ReponsesPreparees;
}) {
  const choix = choixDe(question);
  // vrai/faux : `correct` peut être un booléen (vrai) ou l'index de l'option (0 = Vrai)
  const bonne = typeof question.correct === 'boolean' ? (question.correct ? 0 : 1) : question.correct;
  const debut = useRef(Date.now());
  const [reflexion, setReflexion] = useState(choix ? REFLECHIS_S : 0);
  const [tentative, setTentative] = useState(1);
  const [exclus, setExclus] = useState<number[]>([]);
  const [attente, setAttente] = useState(false);
  const [message, setMessage] = useState('');
  const [fini, setFini] = useState<null | ResultatQuestion>(null);
  const premier = useRef<{ reponse: string; correct: boolean | null; duree_s: number } | null>(null);
  /** passée (12 novembre 2026) : notée seulement si l'élève s'en va sans y revenir (« ← Y revenir » l'annule) */
  const [passee, setPassee] = useState(false);
  // la démonstration, sur un tableau à part par-dessus la question, après la réaction (12 novembre 2026)
  const demoPreparee = (question.demonstration as Demonstration | undefined)?.lignes?.length ? question.demonstration as Demonstration : null;
  // « Retrouver » sans démonstration : la correction s'écrit quand même au tableau, ligne par ligne (12 novembre 2026)
  const demo = useMemo(() => demoPreparee || (mode === 'retrouver' && question.attendu ? correctionDe(question.attendu, question.explanation) : null),
    [demoPreparee, mode, question.attendu, question.explanation]);
  const [lectureDemo, setLectureDemo] = useState<LectureDemo | null>(null);
  const [demoOuverte, setDemoOuverte] = useState<'non' | 'dite' | 'revoir'>('non');

  useEffect(() => {
    debut.current = Date.now();
    premier.current = null;
    setReflexion(choix ? REFLECHIS_S : 0); setTentative(1); setExclus([]); setMessage(''); setFini(null); setPassee(false);
    setDemoOuverte('non'); setLectureDemo(null);
    // le tuteur lit l'énoncé à l'ouverture de la question (pas les options) ; il se tait si elle se ferme
    const id = window.setTimeout(() => lireEnonce(question), 300);
    return () => { window.clearTimeout(id); taire(); };
  }, [question.prompt, question.id]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (reflexion <= 0) return;
    const t = window.setTimeout(() => setReflexion(r => r - 1), 1000);
    return () => window.clearTimeout(t);
  }, [reflexion]);

  const terminer = (r: ResultatQuestion) => {
    setFini(r); onResultat(r);
    // la démonstration s'écrit après la réaction dite, sur son propre tableau
    if (demo && !r.passee) {
      void attendreLaFin().then(() => { setLectureDemo(demo === demoPreparee ? lireDemonstration(demo) : lectureMuette(demo)); setDemoOuverte('dite'); });
    }
  };
  const passer = () => { if (fini || attente) return; taire(); setPassee(true); };
  const suite = () => {
    if (passee && !fini) {
      const r: ResultatQuestion = { reponse: '', correct: null, duree_s: Math.round((Date.now() - debut.current) / 100) / 10, passee: true };
      setFini(r); onResultat(r);
    }
    onSuite();
  };
  const fermerDemo = () => { lectureDemo?.arreter(); setLectureDemo(null); setDemoOuverte('non'); };

  const repondre = async (reponse: string, verdict: boolean | null, indice: number | null) => {
    if (fini || attente) return;
    taire();   // la lecture de l'énoncé s'arrête
    let correct = verdict;
    let ecrit = '';
    // un QCM ou un vrai/faux : la réaction préparée de cette option, s'il y en a une (indice d'abord, réponse au 2e essai)
    const preparee = verdict !== null && indice !== null ? reponses?.[String(indice)]?.[verdict ? 'juste' : (tentative >= 2 || (choix?.length ?? 0) <= 2 ? '2' : '1')] : undefined;
    if (preparee) { ecrit = preparee.ecrit; onJouer?.(preparee); }
    if (verdict === null) {
      setAttente(true);
      try {
        const r = await jugerReponseLibre(question, reponse, tentative, titre);
        correct = r.correct; ecrit = r.ecrit;
        if (r.parole) onDire?.(r.parole);
      } catch { correct = null; }
      finally { setAttente(false); }
    }
    if (tentative === 1) {
      const duree_s = Math.round((Date.now() - debut.current) / 100) / 10;
      premier.current = { reponse, correct, duree_s };
      // un vrai/faux n'a qu'un essai : le second serait l'autre option, sans réfléchir
      if (correct === false && (choix?.length ?? 3) <= 2) {
        setMessage(ecrit || (mode === 'rappel' ? 'Pas grave : on la revoit bientôt.' : 'Voici la bonne réponse.'));
        terminer({ reponse, correct, duree_s });
        return;
      }
      if (correct === false) {
        setTentative(2);
        if (indice !== null) setExclus([indice]);
        setMessage(ecrit || 'Pas tout à fait. Réfléchis encore, tu as un deuxième essai.');
        return;
      }
      setMessage(correct === null ? 'Réponse notée.' : ecrit || 'Bravo, c’est juste !');
      terminer({ reponse, correct, duree_s });
      return;
    }
    const p = premier.current!;
    setMessage(correct ? (ecrit || 'Juste, cette fois !') : (ecrit || (mode === 'rappel' ? 'Pas grave : on la revoit bientôt.' : 'Voici ce qu’il fallait retenir.')));
    terminer({ reponse: p.reponse, correct: p.correct, duree_s: p.duree_s, reponse_2: reponse, correct_2: correct });
  };

  const montrerReponse = fini && fini.correct !== true && fini.correct_2 !== true;
  const ton = mode === 'retrouver' ? 'Cahier fermé : retrouve-le de mémoire.' : mode === 'rappel' ? 'Sans le cours, sans aide.' : 'Exercice du bloc.';

  return (
    <div className="flex flex-col gap-3" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <p className="text-xs uppercase tracking-wide text-white/45">{ton}</p>
      <div className="flex items-start gap-2">
        <p className="min-w-0 flex-1 text-xl leading-snug md:text-2xl" style={{ fontFamily: CRAIE, color: '#fef3c7' }} dir="auto"><Formule t={question.prompt} /></p>
        {!fini && (
          <button type="button" onClick={() => lireEnonce(question)} title="Réécouter l’énoncé" aria-label="Réécouter l’énoncé"
            className="shrink-0 rounded-full bg-white/10 px-2.5 py-1 text-sm text-white/70 hover:bg-white/20">🔊</button>
        )}
      </div>

      {choix && reflexion > 0 && !fini && (
        <p className="text-sm text-sky-200/80">🤔 Réfléchis d’abord… les choix arrivent dans {reflexion} s</p>
      )}
      {passee && !fini ? (
        <div className="flex flex-col gap-3">
          <p className="rounded-lg bg-white/5 px-3 py-2 text-sm text-white/60">⏭ Question passée : elle reviendra plus tard.</p>
          {mode !== 'rappel' && question.attendu && (
            <div className="rounded-lg border border-amber-200/30 bg-amber-200/5 px-3 py-2">
              <p className="text-xs text-amber-100/70">Ce qu’il fallait retrouver :</p>
              <p className="text-lg" style={{ fontFamily: CRAIE, color: '#fef3c7' }} dir="auto"><Formule t={question.attendu} /></p>
            </div>
          )}
          <div className="flex items-center justify-between">
            <button type="button" onClick={() => setPassee(false)} className="rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20">← Y revenir</button>
            <button type="button" onClick={suite} className="rounded-full bg-cyan-400/90 px-7 py-3 text-base font-bold text-slate-950 shadow-lg hover:bg-cyan-300">{libelleSuite}</button>
          </div>
        </div>
      ) : null}
      {choix && reflexion <= 0 && !(passee && !fini) && (
        <div className={question.type === 'vrai_faux' || choix.length === 2 ? 'flex flex-wrap gap-2' : 'flex flex-col gap-2'}>
          {choix.map((c, i) => {
            const estBonne = bonne === i;
            const montree = fini && estBonne && (montrerReponse || fini.correct || fini.correct_2);
            return (
              <button key={i} type="button" disabled={!!fini || attente || exclus.includes(i)}
                onClick={() => void repondre(c, bonne === undefined ? null : bonne === i, i)}
                className={`rounded-xl border px-4 py-2.5 text-left text-base transition ${montree ? 'border-emerald-300/70 bg-emerald-400/15 text-emerald-50' : exclus.includes(i) ? 'border-white/10 bg-white/5 text-white/30 line-through decoration-white/20' : 'border-white/20 bg-white/[0.06] hover:bg-white/[0.12]'} disabled:cursor-default`}
                style={{ fontFamily: CRAIE }} dir="auto">
                <Formule t={c} />
              </button>
            );
          })}
        </div>
      )}
      {!choix && !fini && !passee && (
        <ChampReponse key={tentative} disabled={attente} libelle={attente ? 'Le professeur lit…' : 'Répondre'} clavierAuto
          suggestions={suggestions ? { ...suggestions, deck_id: suggestions.deck_id || deckId, enonce: question.prompt, clavier: question.clavier } : { deck_id: deckId, enonce: question.prompt, clavier: question.clavier }}
          placeholder={mode === 'retrouver' ? 'La formule ou la définition, de mémoire…' : 'Ta réponse…'}
          contexte={{ deck_id: deckId, title: titre, enonce: question.prompt }}
          onEnvoyer={t => void repondre(t, null, null)} />
      )}

      {message && <p className={`rounded-lg px-3 py-2 text-sm ${fini?.correct || fini?.correct_2 ? 'bg-emerald-400/10 text-emerald-100' : 'bg-sky-400/10 text-sky-100'}`} dir="auto">{message}</p>}
      {(montrerReponse || (fini && mode === 'retrouver')) && !choix && question.attendu && (
        <div className="rounded-lg border border-amber-200/30 bg-amber-200/5 px-3 py-2">
          <p className="text-xs text-amber-100/70">{mode === 'retrouver' ? (montrerReponse ? 'Ce qu’il fallait retrouver (relis-le dans ton cahier) :' : 'Compare avec ce que dit le cours :') : 'À retenir :'}</p>
          <p className="text-lg" style={{ fontFamily: CRAIE, color: '#fef3c7' }} dir="auto"><Formule t={question.attendu} /></p>
        </div>
      )}
      {fini && question.explanation && <p className="text-sm text-white/70" dir="auto"><Formule t={question.explanation} /></p>}
      {!fini && !passee && !attente && (
        // discret : l'élève peut ne pas répondre ; noté passé (ni juste ni erreur), il peut y revenir avant de continuer
        <button type="button" onClick={passer} className="self-start text-sm text-white/40 underline-offset-4 hover:text-white/80 hover:underline">Passer ⏭</button>
      )}
      {fini && demo && demoOuverte === 'non' && !fini.passee && (
        <button type="button" onClick={() => setDemoOuverte('revoir')} className="self-start rounded-full bg-white/10 px-4 py-1.5 text-sm hover:bg-white/20">✍️ Revoir la démonstration</button>
      )}
      {demo && demoOuverte !== 'non' && (
        <DemonstrationPleine d={demo} lecture={demoOuverte === 'dite' ? lectureDemo : null} complet={demoOuverte === 'revoir'} enonce={question.prompt}
          onFermer={fermerDemo} />
      )}
      {fini && (
        <button type="button" onClick={suite} autoFocus
          className="self-end rounded-full bg-cyan-400/90 px-7 py-3 text-base font-bold text-slate-950 shadow-lg hover:bg-cyan-300">
          {libelleSuite}
        </button>
      )}
    </div>
  );
}
