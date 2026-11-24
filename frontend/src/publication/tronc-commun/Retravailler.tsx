/**
 * Le cadre « À retravailler » de l'accueil d'un lien libre avec fiche (24/11/2026) : les questions d'examen ratées de
 * l'élève (éléments du barème perdus) et ses réponses fausses dans les cours, chacune avec le lien vers la diapositive
 * qui l'explique. Rien d'affiché tant qu'il n'y a rien à retravailler.
 */
import { lienDiapo, useARetravailler, type Lien } from './revoir';

export default function Retravailler({ revoir, nomExamen, nomCours }: {
  /** les diapositives d'une question d'examen ratée */
  revoir: (examen: string, question: string) => Lien[];
  nomExamen: (examen: string) => string;
  nomCours: (cours: string) => string;
}) {
  const d = useARetravailler();
  if (!d || (!d.questions.length && !d.cours.length)) return null;
  const pts = (x: number) => String(Math.round(x * 100) / 100).replace('.', ',');
  return (
    <section className="mt-5 rounded-2xl border border-rose-300/40 bg-rose-400/10 p-4 [@media(max-height:520px)]:mt-3 [@media(max-height:520px)]:p-3">
      <h2 className="text-lg font-semibold">À retravailler</h2>
      <p className="text-[14px] text-white/70">Ce que tu as raté : ouvre la diapositive qui l’explique, puis refais la question.</p>
      <ul className="mt-2 space-y-2">
        {d.questions.map(q => (
          <li key={`${q.examen}-${q.id}`} className="rounded-lg bg-black/20 px-3 py-2 text-[14px]">
            <p><b>{nomExamen(q.examen)}, question {q.id}</b> <span className="text-white/60">— {pts(q.note)} / {pts(q.sur)}</span></p>
            {!!q.pertes.length && <p className="text-rose-200">− {q.pertes.slice(0, 3).join(' ; ')}</p>}
            <p className="mt-1 flex flex-wrap gap-1.5">{revoir(q.examen, q.id).map(l => (
              <a key={l.diapo} href={lienDiapo(l)} className="rounded-md bg-white/10 px-2 py-1 text-[13px] font-semibold hover:bg-white/20">↻ {l.titre}</a>))}</p>
          </li>))}
        {d.cours.map(r => (
          <li key={`${r.cours}-${r.slide_id}-${r.enonce}`} className="rounded-lg bg-black/20 px-3 py-2 text-[14px]">
            <p><b>{nomCours(r.cours)}</b> <span className="text-white/60">— réponse fausse dans le cours</span></p>
            {r.enonce && <p className="text-white/80">{r.enonce.slice(0, 160)}</p>}
            <p className="mt-1"><a href={lienDiapo({ cours: r.cours, diapo: r.slide_id })} className="rounded-md bg-white/10 px-2 py-1 text-[13px] font-semibold hover:bg-white/20">↻ {r.titre || 'Revoir la diapositive'}</a></p>
          </li>))}
      </ul>
    </section>
  );
}
