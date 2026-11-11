import { useEffect, useRef, useState, type ReactNode } from 'react';
import ChampReponse from '../SaisieReponse';
import { jugerReponseLibre, type QuestionMemoire as Q, type ReponsesPreparees } from './api';
import type { ReactionPreparee } from '../types';

/**
 * Une question du cycle de mémoire : rappel de début de séance, « retrouver » d'un bloc (cahier fermé) ou exercice
 * du bloc. QCM et vrai/faux se corrigent tout de suite ; une réponse libre (écrite, dite ou photographiée) est jugée
 * en direct. Un essai de plus si le premier est faux ; puis la bonne réponse, calmement : jamais une marque rouge.
 */
export const CRAIE = "'Patrick Hand', 'Caveat', cursive";

/** « y_M(t) » s'écrit avec M en indice : jamais de « _ » devant l'élève. */
export function Formule({ t }: { t: string }) {
  const parts: ReactNode[] = [];
  const re = /([A-Za-zτθΔλωφ])_(\{[^}]+\}|[A-Za-z0-9]+)/g;
  let i = 0, m: RegExpExecArray | null, k = 0;
  while ((m = re.exec(t))) {
    if (m.index > i) parts.push(t.slice(i, m.index));
    parts.push(m[1], <sub key={k++} className="text-[0.7em]">{m[2].replace(/[{}]/g, '')}</sub>);
    i = re.lastIndex;
  }
  if (i < t.length) parts.push(t.slice(i));
  return <>{parts}</>;
}

export interface ResultatQuestion {
  reponse: string; reponse_2?: string;
  /** premier essai ; `correct_2` : le second. `null` : rien de jugeable (le juge ne répondait pas). */
  correct: boolean | null; correct_2?: boolean | null;
  /** secondes jusqu'à la première réponse */
  duree_s: number;
}

type Mode = 'rappel' | 'retrouver' | 'exercice';

const choixDe = (q: Q): string[] | null => {
  if (q.options?.length) return q.options;
  if (q.choices?.length) return q.choices;
  if (q.type === 'vrai_faux') return ['Vrai', 'Faux'];
  return null;
};

const REFLECHIS_S = 8;

export default function QuestionMemoire({ question, mode, titre = '', deckId, onResultat, onSuite, onDire, onJouer, reponses, libelleSuite = 'Suite →' }: {
  question: Q; mode: Mode; titre?: string; deckId?: string;
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

  useEffect(() => {
    debut.current = Date.now();
    premier.current = null;
    setReflexion(choix ? REFLECHIS_S : 0); setTentative(1); setExclus([]); setMessage(''); setFini(null);
  }, [question.prompt, question.id]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (reflexion <= 0) return;
    const t = window.setTimeout(() => setReflexion(r => r - 1), 1000);
    return () => window.clearTimeout(t);
  }, [reflexion]);

  const terminer = (r: ResultatQuestion) => { setFini(r); onResultat(r); };

  const repondre = async (reponse: string, verdict: boolean | null, indice: number | null) => {
    if (fini || attente) return;
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
      <p className="text-xl leading-snug md:text-2xl" style={{ fontFamily: CRAIE, color: '#fef3c7' }} dir="auto"><Formule t={question.prompt} /></p>

      {choix && reflexion > 0 && !fini && (
        <p className="text-sm text-sky-200/80">🤔 Réfléchis d’abord… les choix arrivent dans {reflexion} s</p>
      )}
      {choix && reflexion <= 0 && (
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
      {!choix && !fini && (
        <ChampReponse key={tentative} disabled={attente} libelle={attente ? 'Le professeur lit…' : 'Répondre'}
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
      {fini && (
        <button type="button" onClick={onSuite} autoFocus
          className="self-end rounded-full bg-cyan-400/90 px-7 py-3 text-base font-bold text-slate-950 shadow-lg hover:bg-cyan-300">
          {libelleSuite}
        </button>
      )}
    </div>
  );
}
