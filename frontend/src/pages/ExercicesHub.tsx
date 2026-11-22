/** La partie « Exercices » (22 novembre 2026) : les exercices d'application du premier semestre, par matière. */
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import MoalimShell from '../components/MoalimShell';
import StudentNavigation from '../components/StudentNavigation';
import MobileBottomNav from '../components/MobileBottomNav';
import type { FicheIndex, MatiereExercice } from '../components/exercice/types';

const MATIERES: { cle: MatiereExercice; nom: string; icone: string }[] = [
  { cle: 'mathematiques', nom: 'Mathématiques', icone: '∑' },
  { cle: 'physique', nom: 'Physique-chimie', icone: '⚛' },
  { cle: 'svt', nom: 'SVT', icone: '🧬' },
];
const NIVEAU: Record<string, string> = { facile: 'Facile', moyen: 'Moyen', difficile: 'Supérieur' };
const ORDRE: Record<string, number> = { facile: 0, moyen: 1, difficile: 2 };
const COULEUR: Record<string, string> = { facile: 'border border-emerald-600 bg-emerald-50 text-emerald-800', moyen: 'border border-amber-600 bg-amber-50 text-amber-800', difficile: 'border border-rose-600 bg-rose-50 text-rose-800' };

export default function ExercicesHub() {
  const navigate = useNavigate();
  const [fiches, setFiches] = useState<FicheIndex[] | null>(null);
  useEffect(() => {
    fetch('/media/exercices/index.json').then(r => r.json()).then((d: { exercices: FicheIndex[] }) => setFiches(d.exercices)).catch(() => setFiches([]));
  }, []);
  return (
    <MoalimShell>
      <StudentNavigation active="exercices" />
      <main className="mx-auto min-h-[calc(100vh-4rem)] max-w-7xl px-4 pb-28 pt-6 sm:px-6 lg:px-8 lg:pb-12 lg:pt-8">
        <header>
          <h1 className="text-2xl font-bold text-white">Exercices</h1>
          <p className="mt-1 max-w-2xl text-sm text-white/60">Des exercices d’application des cours du premier semestre. Le tuteur t’aide si tu le demandes,
            t’explique avec une animation, te propose une version plus facile pour t’entraîner, puis un exercice semblable à faire seul.
            Les sujets du national sont dans la partie Examen.</p>
          <p className="mt-2 flex flex-wrap gap-2 text-xs">
            <span className={`rounded-full px-2 py-0.5 ${COULEUR.facile}`}>Facile : pour s’entraîner</span>
            <span className={`rounded-full px-2 py-0.5 ${COULEUR.moyen}`}>Moyen : le niveau de l’examen</span>
            <span className={`rounded-full px-2 py-0.5 ${COULEUR.difficile}`}>Supérieur : plus exigeant que l’examen</span>
          </p>
        </header>
        {fiches === null ? <p className="mt-8 text-white/60">Chargement…</p> : (
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            {MATIERES.map(m => {
              const liste = fiches.filter(f => f.matiere === m.cle).sort((a, b) => (ORDRE[a.niveau || ''] ?? 9) - (ORDRE[b.niveau || ''] ?? 9));
              return (
                <section key={m.cle} className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                  <h2 className="mb-3 flex items-center gap-2 text-lg font-semibold text-white"><span className="text-xl">{m.icone}</span>{m.nom}</h2>
                  {liste.length === 0 && <p className="text-sm text-white/50">Bientôt.</p>}
                  <ul className="space-y-2">
                    {liste.map(f => (
                      <li key={f.id}>
                        <button onClick={() => navigate(`/exercices/${f.id}`)} className="w-full rounded-sm bg-white p-3 text-left text-black shadow ring-1 ring-black/10 hover:ring-2 hover:ring-amber-400">
                          <p className="font-semibold" style={{ fontFamily: "'Times New Roman', Georgia, serif" }}>{f.titre}</p>
                          <p className="mt-1 flex items-center gap-2 text-xs text-slate-600"><span className={`rounded-full px-2 py-0.5 ${COULEUR[f.niveau || ''] || ''}`}>{NIVEAU[f.niveau || ''] || ''}</span>{f.duree_min ? `~${f.duree_min} min · ` : ''}{f.questions} questions</p>
                        </button>
                      </li>))}
                  </ul>
                </section>);
            })}
          </div>)}
      </main>
      <MobileBottomNav active="exercices" />
    </MoalimShell>
  );
}
