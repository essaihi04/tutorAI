/**
 * Onglet « Rétention » du tableau de bord (mémoire longue, 11 novembre 2026).
 *
 * Ce qui reste vraiment : la réussite du premier coup aux rappels espacés faits au moins un jour après la dernière
 * fois, à J+7 (7 à 29 jours après l'apprentissage) et à J+30 (30 jours et plus), par cours, par compétence et par
 * élève (`GET /admin/retention`, `backend/app/services/memoire_longue.py`). Réussir pendant le cours ne prouve rien.
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { RefreshCw } from 'lucide-react';
import { getAdminUsers, getRetention, type Retention, type TauxRetention } from '../../services/api';

function Taux({ t, vide = '—' }: { t: TauxRetention; vide?: string }) {
  if (!t.n) return <span className="text-gray-300">{vide}</span>;
  const p = Math.round((t.taux || 0) * 100);
  const couleur = p >= 80 ? 'bg-emerald-500' : p >= 50 ? 'bg-amber-400' : 'bg-rose-400';
  return (
    <span className="inline-flex items-center gap-2 tabular-nums">
      <span className="relative h-1.5 w-14 overflow-hidden rounded-full bg-gray-100"><span className={`absolute inset-y-0 left-0 ${couleur}`} style={{ width: `${p}%` }} /></span>
      <span className="font-semibold text-gray-900">{p} %</span>
      <span className="text-xs text-gray-400">({t.reussis}/{t.n})</span>
    </span>
  );
}

const cumul = (l: TauxRetention[]): TauxRetention => {
  const n = l.reduce((s, x) => s + x.n, 0), r = l.reduce((s, x) => s + x.reussis, 0);
  return { n, reussis: r, taux: n ? r / n : null };
};

const MATIERES: Record<string, string> = { 'physique-chimie': 'Physique-chimie', svt: 'SVT', mathematiques: 'Maths' };

export default function AdminRetention() {
  const [data, setData] = useState<Retention | null>(null);
  const [noms, setNoms] = useState<Record<string, string>>({});
  const [chargement, setChargement] = useState(false);
  const [erreur, setErreur] = useState('');
  const [cours, setCours] = useState('');
  const [publics, setPublics] = useState(false);

  const charger = useCallback(async () => {
    setChargement(true); setErreur('');
    try {
      setData((await getRetention()).data);
      const u = (await getAdminUsers().catch(() => null))?.data?.users || [];
      setNoms(Object.fromEntries(u.map((x: { id: string; full_name?: string; username?: string }) => [String(x.id), x.full_name || x.username || ''])));
    } catch (e: any) { setErreur(e?.response?.data?.detail || 'Lecture de la rétention impossible'); }
    finally { setChargement(false); }
  }, []);
  useEffect(() => { void charger(); }, [charger]);

  const eleves = useMemo(() => (data?.par_eleve || []).filter(e => publics || !e.public), [data, publics]);
  const global = useMemo(() => ({
    j7: cumul(eleves.map(e => e.j7)), j30: cumul(eleves.map(e => e.j30)), tous: cumul(eleves.map(e => e.rappels)),
    dus: eleves.reduce((s, e) => s + e.dus, 0), seances: eleves.reduce((s, e) => s + e.seances, 0),
  }), [eleves]);
  const comps = useMemo(() => (data?.par_competence || []).filter(c => !cours || c.cours_id === cours), [data, cours]);

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center gap-2">
        <div className="mr-auto">
          <h2 className="text-lg font-semibold text-gray-900">Rétention : ce qui reste vraiment</h2>
          <p className="text-xs text-gray-500">{data?.definition}</p>
        </div>
        <label className="flex items-center gap-1.5 text-sm text-gray-600">
          <input type="checkbox" checked={publics} onChange={e => setPublics(e.target.checked)} /> visiteurs du lien libre
        </label>
        <button onClick={() => void charger()} className="flex items-center gap-1 rounded-lg border px-3 py-1.5 text-sm hover:bg-gray-50">
          <RefreshCw className={`h-4 w-4 ${chargement ? 'animate-spin' : ''}`} /> Actualiser
        </button>
      </div>
      {erreur && <div className="text-sm text-red-600">{erreur}</div>}

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
        {[
          { l: 'Rétention à J+7', v: <Taux t={global.j7} vide="pas encore" /> },
          { l: 'Rétention à J+30', v: <Taux t={global.j30} vide="pas encore" /> },
          { l: 'Tous les rappels (≥ 1 jour)', v: <Taux t={global.tous} vide="aucun" /> },
          { l: 'Rappels dus aujourd’hui', v: <span className="text-xl font-bold text-gray-900">{global.dus}</span> },
          { l: 'Séances terminées', v: <span className="text-xl font-bold text-gray-900">{global.seances}</span> },
        ].map(k => (
          <div key={k.l} className="rounded-xl border border-gray-200 bg-white p-3">
            <p className="text-xs text-gray-500">{k.l}</p>
            <div className="mt-1">{k.v}</div>
          </div>
        ))}
      </div>

      <section className="rounded-xl border border-gray-200 bg-white">
        <h3 className="border-b px-4 py-2 text-sm font-semibold text-gray-700">Par cours</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-left text-xs text-gray-500"><tr><th className="px-4 py-2">Cours</th><th>Matière</th><th>J+7</th><th>J+30</th><th>Tous les rappels</th></tr></thead>
            <tbody>
              {(data?.par_cours || []).map(c => (
                <tr key={c.cours_id} onClick={() => setCours(c.cours_id === cours ? '' : c.cours_id)}
                  className={`cursor-pointer border-t hover:bg-gray-50 ${c.cours_id === cours ? 'bg-gray-50' : ''}`}>
                  <td className="px-4 py-2"><div className="font-medium text-gray-900">{c.titre}</div><div className="text-xs text-gray-400">{c.cours_id}</div></td>
                  <td>{MATIERES[c.matiere] || c.matiere || '—'}</td>
                  <td><Taux t={c.j7} /></td><td><Taux t={c.j30} /></td><td><Taux t={c.rappels} /></td>
                </tr>
              ))}
              {!data?.par_cours.length && <tr><td colSpan={5} className="px-4 py-6 text-center text-gray-400">Aucun cours suivi pour l’instant.</td></tr>}
            </tbody>
          </table>
        </div>
      </section>

      <section className="rounded-xl border border-gray-200 bg-white">
        <h3 className="flex items-center gap-2 border-b px-4 py-2 text-sm font-semibold text-gray-700">
          Par compétence {cours && <button onClick={() => setCours('')} className="rounded-full bg-gray-100 px-2 text-xs font-normal">{cours} ✕</button>}
        </h3>
        <div className="max-h-[420px] overflow-auto">
          <table className="w-full text-sm">
            <thead className="sticky top-0 bg-white text-left text-xs text-gray-500"><tr><th className="px-4 py-2">Compétence</th><th>J+7</th><th>J+30</th><th>Tous les rappels</th></tr></thead>
            <tbody>
              {comps.map(c => (
                <tr key={c.cle} className="border-t">
                  <td className="px-4 py-2"><span className="mr-2 text-xs text-gray-400">{c.competence_id}</span>{c.label}{!cours && <span className="ml-2 text-xs text-gray-400">{c.cours_id}</span>}</td>
                  <td><Taux t={c.j7} /></td><td><Taux t={c.j30} /></td><td><Taux t={c.rappels} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="rounded-xl border border-gray-200 bg-white">
        <h3 className="border-b px-4 py-2 text-sm font-semibold text-gray-700">Par élève</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-left text-xs text-gray-500">
              <tr><th className="px-4 py-2">Élève</th><th>J+7</th><th>J+30</th><th>Compétences</th><th>Dus</th><th>Séances</th><th>Cahiers</th><th>Saturations</th><th>Notifications</th><th>Dernière activité</th></tr>
            </thead>
            <tbody>
              {eleves.map(e => (
                <tr key={e.eleve} className="border-t align-top">
                  <td className="px-4 py-2"><div className="font-medium text-gray-900">{noms[e.eleve] || (e.public ? 'Visiteur' : 'Élève')}</div><div className="text-xs text-gray-400">{e.eleve.slice(0, 18)}</div></td>
                  <td><Taux t={e.j7} /></td><td><Taux t={e.j30} /></td>
                  <td className="tabular-nums">{e.competences_suivies}</td>
                  <td className="tabular-nums">{e.dus}</td>
                  <td className="tabular-nums">{e.seances}{e.duree_moyenne_min ? <span className="text-xs text-gray-400"> · {e.duree_moyenne_min} min</span> : null}</td>
                  <td className="tabular-nums">{e.cahiers}</td>
                  <td className="text-xs text-gray-600">{Object.entries(e.saturations).map(([k, v]) => `${k.replace('_', ' ')} ${v}`).join(', ') || '—'}</td>
                  <td className="text-xs text-gray-600">{e.notifications.envoyee ? `${e.notifications.ouverte || 0}/${e.notifications.envoyee} ouvertes` : '—'}</td>
                  <td className="text-xs text-gray-500">{e.dernier_evenement ? new Date(e.dernier_evenement).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' }) : ''}</td>
                </tr>
              ))}
              {!eleves.length && <tr><td colSpan={10} className="px-4 py-6 text-center text-gray-400">Aucun élève suivi pour l’instant.</td></tr>}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
