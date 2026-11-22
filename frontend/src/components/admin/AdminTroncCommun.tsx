/**
 * Onglet « Tronc Commun » du tableau de bord (22 novembre 2026).
 *
 * Les élèves du lien libre https://moalim.online/tronc-commun/ remplissent une fiche une seule fois (nom, classe, nom du
 * père, téléphone) ; la page envoie ensuite leur suivi (`public_tronc_commun.py`). Ici l'admin voit chaque élève : le temps
 * passé dans chaque cours et sur l'évaluation, sa progression dans les diapositives, ses réponses dans les cours, ses notes
 * à l'évaluation question par question, et ses lacunes (éléments du barème perdus, réponses fausses).
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { RefreshCw, ChevronDown, ChevronRight, Download } from 'lucide-react';
import { listTroncCommun, type EleveTroncCommun } from '../../services/api';

const COURS: Record<string, string> = {
  tc_svt_sortie_ecologique: 'Sortie écologique', tc_svt_facteurs_edaphiques: 'Facteurs édaphiques', tc_svt_revision: 'Révision', examen: 'Évaluation',
};
const duree = (s: number) => (!s ? '—' : s < 3600 ? `${Math.round(s / 60)} min` : `${Math.floor(s / 3600)} h ${Math.round((s % 3600) / 60)} min`);
const date = (d?: string | null) => (d ? new Date(d).toLocaleString('fr-MA', { dateStyle: 'short', timeStyle: 'short' }) : '—');
const pts = (x?: number | null) => (x == null ? '—' : String(Math.round(x * 100) / 100).replace('.', ','));

function noteExamen(e: EleveTroncCommun) {
  const der = e.examens[e.examens.length - 1];
  if (der) return { note: der.note, sur: der.sur, fini: true };
  if (e.examen_en_cours.faites) return { note: e.examen_en_cours.note, sur: e.examen_en_cours.sur, fini: false };
  return null;
}

export default function AdminTroncCommun() {
  const [eleves, setEleves] = useState<EleveTroncCommun[]>([]);
  const [chargement, setChargement] = useState(false);
  const [erreur, setErreur] = useState('');
  const [classe, setClasse] = useState('');
  const [recherche, setRecherche] = useState('');
  const [ouvert, setOuvert] = useState<string | null>(null);

  const charger = useCallback(async () => {
    setChargement(true); setErreur('');
    try { setEleves((await listTroncCommun()).data.eleves || []); }
    catch (e: any) { setErreur(e?.response?.data?.detail || 'Lecture du suivi impossible'); }
    finally { setChargement(false); }
  }, []);
  useEffect(() => { void charger(); }, [charger]);

  const classes = useMemo(() => [...new Set(eleves.map(e => e.classe))].sort(), [eleves]);
  const visibles = useMemo(() => eleves
    .filter(e => !classe || e.classe === classe)
    .filter(e => !recherche || `${e.nom} ${e.pere} ${e.telephone}`.toLowerCase().includes(recherche.toLowerCase())),
  [eleves, classe, recherche]);

  const exporter = () => {
    const lignes = [['Élève', 'Classe', 'Père', 'Téléphone', 'Inscrit le', 'Dernière activité', ...Object.values(COURS).map(c => `Temps ${c} (min)`),
      'Évaluation', 'Réponses cours justes', 'Réponses cours fausses', 'Lacunes']];
    for (const e of visibles) {
      const n = noteExamen(e);
      lignes.push([e.nom, e.classe, e.pere, e.telephone, date(e.date), date(e.derniere),
        ...Object.keys(COURS).map(c => String(Math.round((e.temps[c] || 0) / 60))),
        n ? `${pts(n.note)}/${pts(n.sur)}${n.fini ? '' : ' (en cours)'}` : '', String(e.reponses_cours.justes), String(e.reponses_cours.fausses), e.lacunes.join(' | ')]);
    }
    const csv = '﻿' + lignes.map(l => l.map(x => `"${String(x).replace(/"/g, '""')}"`).join(';')).join('\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    a.download = `tronc-commun-suivi${classe ? `-${classe}` : ''}.csv`;
    a.click();
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <h2 className="mr-auto text-lg font-semibold text-gray-900">Tronc Commun — élèves et suivi ({visibles.length})</h2>
        <input value={recherche} onChange={e => setRecherche(e.target.value)} placeholder="Nom, père ou téléphone…" className="rounded-lg border px-2 py-1.5 text-sm" />
        <select value={classe} onChange={e => setClasse(e.target.value)} className="rounded-lg border px-2 py-1.5 text-sm">
          <option value="">Toutes les classes</option>
          {classes.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <button onClick={exporter} className="flex items-center gap-1 rounded-lg border px-2 py-1.5 text-sm hover:bg-gray-50"><Download className="h-4 w-4" /> CSV</button>
        <button onClick={() => void charger()} className="flex items-center gap-1 rounded-lg border px-2 py-1.5 text-sm hover:bg-gray-50">
          <RefreshCw className={`h-4 w-4 ${chargement ? 'animate-spin' : ''}`} /> Actualiser</button>
      </div>
      {erreur && <p className="text-sm text-red-600">{erreur}</p>}
      {!visibles.length && !chargement && <p className="text-sm text-gray-500">Aucun élève inscrit pour l’instant (lien : https://moalim.online/tronc-commun/).</p>}

      <div className="overflow-x-auto rounded-xl border bg-white">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-left text-gray-600">
            <tr>
              <th className="px-3 py-2" />
              <th className="px-3 py-2">Élève</th><th className="px-3 py-2">Classe</th><th className="px-3 py-2">Père · téléphone</th>
              {Object.values(COURS).map(c => <th key={c} className="px-3 py-2 whitespace-nowrap">{c}</th>)}
              <th className="px-3 py-2">Évaluation</th><th className="px-3 py-2">Réponses cours</th><th className="px-3 py-2">Dernière activité</th>
            </tr>
          </thead>
          <tbody>
            {visibles.map(e => {
              const n = noteExamen(e);
              const vu = ouvert === e.id;
              return (
                <FragmentLigne key={e.id}>
                  <tr className="cursor-pointer border-t hover:bg-gray-50" onClick={() => setOuvert(vu ? null : e.id)}>
                    <td className="px-2 py-2 text-gray-400">{vu ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}</td>
                    <td className="px-3 py-2 font-medium text-gray-900">{e.nom}</td>
                    <td className="px-3 py-2">{e.classe}</td>
                    <td className="px-3 py-2 whitespace-nowrap">{e.pere} · <a href={`tel:${e.telephone}`} className="text-blue-600" onClick={x => x.stopPropagation()}>{e.telephone}</a></td>
                    {Object.keys(COURS).map(c => {
                      const p = e.progression[c];
                      return <td key={c} className="px-3 py-2 whitespace-nowrap">{duree(e.temps[c] || 0)}
                        {p?.total ? <span className="ml-1 text-xs text-gray-500">({p.vues}/{p.total} diapos)</span> : null}</td>;
                    })}
                    <td className="px-3 py-2 whitespace-nowrap font-semibold">{n ? `${pts(n.note)} / ${pts(n.sur)}` : '—'}{n && !n.fini && <span className="ml-1 text-xs font-normal text-amber-600">en cours</span>}</td>
                    <td className="px-3 py-2 whitespace-nowrap"><span className="text-green-700">{e.reponses_cours.justes} ✔</span> · <span className="text-red-600">{e.reponses_cours.fausses} ✘</span></td>
                    <td className="px-3 py-2 whitespace-nowrap text-gray-500">{date(e.derniere)}</td>
                  </tr>
                  {vu && (
                    <tr className="border-t bg-gray-50/60">
                      <td />
                      <td colSpan={11} className="px-3 py-3">
                        <Detail e={e} />
                      </td>
                    </tr>)}
                </FragmentLigne>);
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function FragmentLigne({ children }: { children: React.ReactNode }) { return <>{children}</>; }

function Detail({ e }: { e: EleveTroncCommun }) {
  const der = e.examens[e.examens.length - 1];
  const questions = der ? der.questions : e.examen_en_cours.questions;
  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <div>
        <p className="mb-1 font-semibold text-gray-800">Évaluation {der ? `(terminée le ${date(der.date)}, ${e.examens.length} passage${e.examens.length > 1 ? 's' : ''})` : e.examen_en_cours.faites ? '(en cours)' : '(pas commencée)'}</p>
        {Object.keys(questions).length ? (
          <table className="w-full text-xs">
            <tbody>{Object.entries(questions).sort(([a], [b]) => a.localeCompare(b, 'fr', { numeric: true })).map(([id, q]) => (
              <tr key={id} className="border-t align-top">
                <td className="py-1 pr-2 font-semibold">{id}</td>
                <td className={`py-1 pr-2 whitespace-nowrap font-semibold ${(q.note || 0) >= (q.sur || 0) ? 'text-green-700' : (q.note || 0) > 0 ? 'text-amber-600' : 'text-red-600'}`}>{pts(q.note)} / {pts(q.sur)}</td>
                <td className="py-1 text-gray-700">{q.enonce}{q.pertes?.length ? <span className="block text-red-700">− {q.pertes.join(' ; ')}</span> : null}</td>
              </tr>))}</tbody>
          </table>) : <p className="text-xs text-gray-500">Aucune question rendue.</p>}
      </div>
      <div>
        <p className="mb-1 font-semibold text-gray-800">Lacunes à travailler</p>
        {e.lacunes.length ? <ul className="list-disc space-y-0.5 pl-5 text-xs text-gray-700">{e.lacunes.map((l, k) => <li key={k}>{l}</li>)}</ul>
          : <p className="text-xs text-gray-500">Rien de signalé pour l’instant.</p>}
        <p className="mt-3 text-xs text-gray-500">Inscrit le {date(e.date)} · temps total {duree(Object.values(e.temps).reduce((n, s) => n + s, 0))}</p>
      </div>
    </div>
  );
}
