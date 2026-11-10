/**
 * Onglet « Avis des profs » du tableau de bord (10 novembre 2026).
 *
 * Les profs relisent les cours sur le lien libre (https://moalim.online/cours-ondes/?cours=<id>) et laissent, sur chaque
 * diapositive, un vote (bon / à corriger) et un commentaire (`public_cours.py`, route `/avis`). Ici l'admin les retrouve
 * par cours, ouvre la diapositive signalée, la corrige, puis marque l'avis « corrigé ».
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { RefreshCw, ExternalLink, ThumbsUp, ThumbsDown, Check, X, RotateCcw } from 'lucide-react';
import { listAvisProfs, setStatutAvisProf, type AvisProf } from '../../services/api';

const STATUTS: Record<AvisProf['statut'], string> = { a_faire: 'À faire', corrige: 'Corrigé', ignore: 'Ignoré' };

export default function AdminAvisProfs() {
  const [avis, setAvis] = useState<AvisProf[]>([]);
  const [chargement, setChargement] = useState(false);
  const [erreur, setErreur] = useState('');
  const [cours, setCours] = useState('');
  const [vote, setVote] = useState<'' | 'bon' | 'mauvais' | 'commentaire'>('');
  const [statut, setStatut] = useState<'' | AvisProf['statut']>('a_faire');

  const charger = useCallback(async () => {
    setChargement(true); setErreur('');
    try { setAvis((await listAvisProfs()).data.avis || []); }
    catch (e: any) { setErreur(e?.response?.data?.detail || 'Lecture des avis impossible'); }
    finally { setChargement(false); }
  }, []);
  useEffect(() => { void charger(); }, [charger]);

  const lesCours = useMemo(() => [...new Set(avis.map(a => a.deck_id))].sort(), [avis]);
  const visibles = useMemo(() => avis
    .filter(a => !cours || a.deck_id === cours)
    .filter(a => !statut || a.statut === statut)
    .filter(a => !vote || (vote === 'commentaire' ? !!a.commentaire : a.vote === vote))
    .sort((a, b) => a.deck_id.localeCompare(b.deck_id) || (a.position - b.position) || b.date.localeCompare(a.date)),
  [avis, cours, statut, vote]);

  const parCours = useMemo(() => lesCours.map(id => {
    const l = avis.filter(a => a.deck_id === id);
    return { id, bon: l.filter(a => a.vote === 'bon').length, mauvais: l.filter(a => a.vote === 'mauvais').length,
      aFaire: l.filter(a => a.statut === 'a_faire' && (a.vote === 'mauvais' || a.commentaire)).length,
      relecteurs: new Set(l.map(a => a.relecteur || a.visiteur)).size };
  }), [avis, lesCours]);

  const marquer = async (a: AvisProf, s: AvisProf['statut']) => {
    try {
      await setStatutAvisProf(a, s);
      setAvis(prev => prev.map(x => (x.visiteur === a.visiteur && x.deck_id === a.deck_id && x.slide_id === a.slide_id ? { ...x, statut: s } : x)));
    } catch { setErreur('Le statut n’a pas été enregistré'); }
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <h2 className="text-lg font-semibold text-gray-900 mr-auto">Avis des profs sur les cours</h2>
        <select value={cours} onChange={e => setCours(e.target.value)} className="border rounded-lg px-2 py-1.5 text-sm">
          <option value="">Tous les cours</option>
          {lesCours.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <select value={vote} onChange={e => setVote(e.target.value as any)} className="border rounded-lg px-2 py-1.5 text-sm">
          <option value="">Tous les votes</option>
          <option value="mauvais">👎 À corriger</option>
          <option value="bon">👍 Bon</option>
          <option value="commentaire">Avec commentaire</option>
        </select>
        <select value={statut} onChange={e => setStatut(e.target.value as any)} className="border rounded-lg px-2 py-1.5 text-sm">
          <option value="">Tous les statuts</option>
          {Object.entries(STATUTS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
        </select>
        <button onClick={() => void charger()} className="flex items-center gap-1 border rounded-lg px-3 py-1.5 text-sm hover:bg-gray-50">
          <RefreshCw className={`w-4 h-4 ${chargement ? 'animate-spin' : ''}`} /> Actualiser
        </button>
      </div>

      {erreur && <div className="text-sm text-red-600">{erreur}</div>}

      <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
        {parCours.map(c => (
          <button key={c.id} onClick={() => setCours(c.id === cours ? '' : c.id)}
            className={`text-left rounded-xl border p-3 bg-white ${c.id === cours ? 'border-gray-900' : 'border-gray-200'}`}>
            <div className="font-medium text-sm text-gray-900 truncate">{c.id}</div>
            <div className="text-xs text-gray-500 mt-1">👍 {c.bon} · 👎 {c.mauvais} · {c.aFaire} à traiter · {c.relecteurs} relecteur(s)</div>
          </button>
        ))}
        {!parCours.length && !chargement && <div className="text-sm text-gray-500">Aucun avis pour l’instant.</div>}
      </div>

      <div className="bg-white rounded-xl border border-gray-200 divide-y">
        {visibles.map(a => (
          <div key={`${a.visiteur}|${a.deck_id}|${a.slide_id}`} className="p-3 flex flex-col sm:flex-row sm:items-start gap-2">
            <div className="w-16 shrink-0 text-xs text-gray-500">#{a.position}</div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                {a.vote === 'bon' && <span className="inline-flex items-center gap-1 text-xs text-green-700 bg-green-50 rounded px-1.5 py-0.5"><ThumbsUp className="w-3 h-3" />Bon</span>}
                {a.vote === 'mauvais' && <span className="inline-flex items-center gap-1 text-xs text-red-700 bg-red-50 rounded px-1.5 py-0.5"><ThumbsDown className="w-3 h-3" />À corriger</span>}
                <span className="font-medium text-sm text-gray-900">{a.slide_titre || a.slide_id}</span>
                <span className="text-xs text-gray-400">{a.deck_id} · {a.slide_id}</span>
              </div>
              {a.commentaire && <p className="text-sm text-gray-700 mt-1 whitespace-pre-wrap break-words">{a.commentaire}</p>}
              <div className="text-xs text-gray-400 mt-1">{a.relecteur || 'Relecteur anonyme'} · {new Date(a.date).toLocaleString('fr-FR')} · {STATUTS[a.statut]}</div>
            </div>
            <div className="flex gap-1 shrink-0">
              <a href={`/cours-ondes/?cours=${encodeURIComponent(a.deck_id)}&diapo=${encodeURIComponent(a.slide_id)}`} target="_blank" rel="noreferrer"
                className="flex items-center gap-1 border rounded-lg px-2 py-1 text-xs hover:bg-gray-50"><ExternalLink className="w-3 h-3" />Diapo</a>
              {a.statut !== 'corrige' && <button onClick={() => void marquer(a, 'corrige')} className="flex items-center gap-1 border rounded-lg px-2 py-1 text-xs text-green-700 hover:bg-green-50"><Check className="w-3 h-3" />Corrigé</button>}
              {a.statut !== 'ignore' && <button onClick={() => void marquer(a, 'ignore')} className="flex items-center gap-1 border rounded-lg px-2 py-1 text-xs text-gray-600 hover:bg-gray-50"><X className="w-3 h-3" />Ignorer</button>}
              {a.statut !== 'a_faire' && <button onClick={() => void marquer(a, 'a_faire')} className="flex items-center gap-1 border rounded-lg px-2 py-1 text-xs hover:bg-gray-50"><RotateCcw className="w-3 h-3" />À faire</button>}
            </div>
          </div>
        ))}
        {!visibles.length && avis.length > 0 && <div className="p-4 text-sm text-gray-500">Aucun avis avec ces filtres.</div>}
      </div>
    </div>
  );
}
