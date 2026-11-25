/**
 * Onglet « Mode classe » du tableau de bord (24 novembre 2026, demande de l'utilisateur : « récupérer les données des
 * autres classes, ne pas supprimer à chaque séance, enregistré dans l'admin, avec les photos des réponses des élèves »).
 *
 * Chaque séance du mode classe (`public_classe.py`, gardée dans data/classes/) : ses élèves, la note de chacun à chaque
 * question projetée (grille), et, d'un clic sur une case, la réponse corrigée par l'IA (texte lu, ce qui est juste, ce
 * qui est perdu) avec la photo de la feuille.
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { RefreshCw, Download } from 'lucide-react';
import { listClasses, photoClasse, type ReponseClasse, type SeanceClasse } from '../../services/api';

const SUJETS: Record<string, string> = { tc: 'Tronc Commun SVT', examen_physique: '2ᵉ Bac · physique', examen_chimie: '2ᵉ Bac · chimie', examen_tcf: 'Tronc Commun physique-chimie' };
const COULEUR: Record<string, string> = { juste: '#1c7c54', partiel: '#d68a12', faux: '#d03b3b', regarder: '#2a78d6', nonjuge: '#8a8f98' };
const MOT: Record<string, string> = { juste: 'Juste', partiel: 'En partie', faux: 'Faux', regarder: 'À regarder', nonjuge: 'Non jugé' };
const nb = (x: number) => (Math.round(x * 100) / 100).toString().replace('.', ',');
const date = (iso: string) => (iso ? new Date(iso).toLocaleString('fr-FR', { dateStyle: 'medium', timeStyle: 'short' }) : '');

function Photo({ uid, rid }: { uid: string; rid: string }) {
  const [src, setSrc] = useState('');
  const [grand, setGrand] = useState(false);
  useEffect(() => {
    let url = '';
    photoClasse(uid, rid).then(r => { url = URL.createObjectURL(r.data); setSrc(url); }).catch(() => setSrc(''));
    return () => { if (url) URL.revokeObjectURL(url); };
  }, [uid, rid]);
  if (!src) return <p className="text-sm text-slate-500">Photo…</p>;
  return (<>
    <button onClick={() => setGrand(true)} title="Voir en grand"><img src={src} alt="Feuille de l’élève" className="max-h-[420px] w-full rounded-lg border object-contain" /></button>
    {grand && <div className="fixed inset-0 z-50 grid place-items-center bg-black/85 p-2" onClick={() => setGrand(false)}>
      <img src={src} alt="Feuille de l’élève" className="max-h-[95vh] max-w-[96vw] rounded-lg bg-white object-contain" /></div>}
  </>);
}

function csv(s: SeanceClasse, questions: string[]) {
  const ligne = (xs: (string | number)[]) => xs.map(x => `"${String(x).replace(/"/g, '""')}"`).join(';');
  const rows = [ligne(['Prénom', 'Nom', 'Classe', ...questions, 'Total', 'Sur'])];
  for (const p of s.participants) {
    const par = Object.fromEntries(s.reponses.filter(r => r.eleve === p.id).map(r => [r.question, r]));
    const note = questions.reduce((n, q) => n + (par[q]?.note ?? 0), 0);
    const sur = questions.reduce((n, q) => n + (par[q]?.sur ?? 0), 0);
    rows.push(ligne([p.prenom, p.nom, p.classe, ...questions.map(q => (par[q] ? (par[q].note == null ? 'à regarder' : nb(par[q].note!)) : '')), nb(note), nb(sur)]));
  }
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob(['﻿' + rows.join('\n')], { type: 'text/csv;charset=utf-8' }));
  a.download = `classe_${s.code}_${s.debut.slice(0, 10)}.csv`;
  a.click();
}

export default function AdminClasses() {
  const [seances, setSeances] = useState<SeanceClasse[]>([]);
  const [charge, setCharge] = useState(true);
  const [erreur, setErreur] = useState('');
  const [uid, setUid] = useState('');
  const [cas, setCas] = useState<ReponseClasse | null>(null);
  const charger = useCallback(async () => {
    setCharge(true); setErreur('');
    try { const r = await listClasses(); setSeances(r.data.seances); setUid(u => u || r.data.seances[0]?.uid || ''); }
    catch { setErreur('Impossible de lire les séances.'); }
    finally { setCharge(false); }
  }, []);
  useEffect(() => { void charger(); }, [charger]);

  const s = seances.find(x => x.uid === uid);
  const questions = useMemo(() => {
    if (!s) return [];
    const vues = new Set(s.reponses.map(r => r.question));
    return [...s.posees, ...[...vues].filter(q => !s.posees.includes(q))];
  }, [s]);
  const eleves = useMemo(() => {
    if (!s) return [];
    return s.participants.map(p => {
      const par: Record<string, ReponseClasse> = {};
      for (const r of s.reponses) if (r.eleve === p.id) par[r.question] = r;
      const note = Object.values(par).reduce((n, r) => n + (r.note ?? 0), 0);
      const sur = Object.values(par).reduce((n, r) => n + (r.note == null ? 0 : r.sur), 0);
      return { p, par, note, sur, n: Object.keys(par).length };
    }).sort((a, b) => a.p.nom.localeCompare(b.p.nom, 'fr'));
  }, [s]);
  const nomDe = (id: string) => { const p = s?.participants.find(x => x.id === id); return p ? `${p.prenom} ${p.nom}` : 'Élève'; };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <h2 className="text-xl font-bold text-slate-900">Mode classe : les séances gardées</h2>
        <button onClick={() => void charger()} className="ml-auto flex items-center gap-1 rounded-lg border px-3 py-1.5 text-sm hover:bg-slate-50">
          <RefreshCw className={`h-4 w-4 ${charge ? 'animate-spin' : ''}`} /> Actualiser</button>
      </div>
      {erreur && <p className="rounded-lg bg-rose-50 p-3 text-rose-800">{erreur}</p>}
      {!charge && !seances.length && <p className="text-slate-600">Aucune séance pour l’instant : elles apparaîtront ici dès qu’un professeur lance le mode classe.</p>}

      <div className="grid gap-4 lg:grid-cols-[280px_minmax(0,1fr)]">
        <ul className="max-h-[75vh] space-y-1.5 overflow-y-auto">
          {seances.map(x => {
            const nbEleves = x.participants.length;
            return (
              <li key={x.uid}>
                <button onClick={() => { setUid(x.uid); setCas(null); }} className={`w-full rounded-lg border p-2 text-left text-sm ${x.uid === uid ? 'border-[#2a78d6] bg-blue-50' : 'bg-white hover:bg-slate-50'}`}>
                  <div className="flex items-center gap-2"><b>{date(x.debut)}</b>
                    <span className={`ml-auto rounded px-1.5 text-xs ${x.fin ? 'bg-slate-100 text-slate-600' : 'bg-emerald-100 text-emerald-800'}`}>{x.fin ? 'terminée' : 'en cours / non terminée'}</span></div>
                  <div className="text-slate-600">{SUJETS[x.sujet] || x.sujet} · code {x.code}</div>
                  <div className="text-slate-600">{nbEleves} élève{nbEleves > 1 ? 's' : ''} · {x.reponses.length} réponse{x.reponses.length > 1 ? 's' : ''} · {x.reponses.filter(r => r.photo).length} photo{x.reponses.filter(r => r.photo).length > 1 ? 's' : ''}</div>
                </button>
              </li>);
          })}
        </ul>

        {s && (
          <div className="min-w-0 space-y-3">
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="text-lg font-semibold">{SUJETS[s.sujet] || s.sujet} · code {s.code} · {date(s.debut)}</h3>
              <button onClick={() => csv(s, questions)} disabled={!s.participants.length} className="ml-auto flex items-center gap-1 rounded-lg border px-3 py-1.5 text-sm hover:bg-slate-50 disabled:opacity-40">
                <Download className="h-4 w-4" /> CSV</button>
            </div>
            {!s.participants.length ? <p className="text-slate-600">Aucun élève n’a rejoint cette séance.</p> : (
              <div className="overflow-x-auto rounded-lg border bg-white">
                <table className="min-w-full text-sm">
                  <thead className="bg-slate-50 text-slate-600">
                    <tr><th className="sticky left-0 bg-slate-50 px-2 py-1.5 text-left">Élève</th>
                      {questions.map(q => <th key={q} className="px-1.5 py-1.5 text-center font-semibold">{q}</th>)}
                      <th className="px-2 py-1.5 text-right">Total</th></tr>
                  </thead>
                  <tbody>
                    {eleves.map(({ p, par, note, sur, n }) => (
                      <tr key={p.id} className="border-t">
                        <td className="sticky left-0 whitespace-nowrap bg-white px-2 py-1">{p.prenom} {p.nom}{p.classe ? <span className="text-slate-500"> · {p.classe}</span> : null}
                          {!p.telephone && <span className="ml-1 text-xs text-slate-400" title="Ajouté par le professeur (sans téléphone)">(prof)</span>}</td>
                        {questions.map(q => {
                          const r = par[q];
                          return <td key={q} className="px-1 py-1 text-center">
                            {r ? <button onClick={() => setCas(r)} title={`${MOT[r.verdict] || r.verdict}${r.photo ? ' · photo' : ''}`}
                              className={`min-w-[44px] rounded px-1.5 py-0.5 font-semibold text-white ${cas?.id === r.id ? 'ring-2 ring-black' : ''}`} style={{ background: COULEUR[r.verdict] || '#8a8f98' }}>
                              {r.note == null ? '👀' : nb(r.note)}{r.photo ? ' 📷' : ''}</button> : <span className="text-slate-300">·</span>}
                          </td>;
                        })}
                        <td className="whitespace-nowrap px-2 py-1 text-right font-semibold">{nb(note)} / {nb(sur)} <span className="font-normal text-slate-500">({n})</span></td>
                      </tr>))}
                  </tbody>
                </table>
              </div>)}

            {cas && (
              <div className="grid gap-3 rounded-lg border bg-white p-3 md:grid-cols-2">
                <div>{cas.photo ? <Photo uid={s.uid} rid={cas.id} /> : <p className="rounded bg-slate-50 p-3 text-sm text-slate-600">Réponse écrite au téléphone (pas de photo).</p>}</div>
                <div className="min-w-0 text-[15px]">
                  <div className="flex flex-wrap items-center gap-2">
                    <b>{nomDe(cas.eleve)}</b><span className="rounded bg-black px-1.5 text-xs text-white">{cas.question}</span>
                    <span className="rounded px-2 text-white" style={{ background: COULEUR[cas.verdict] || '#8a8f98' }}>{cas.note == null ? MOT[cas.verdict] : `${nb(cas.note)} / ${nb(cas.sur)}`}</span>
                    {cas.heure ? <span className="text-xs text-slate-500">{new Date(cas.heure * 1000).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</span> : null}
                    <button onClick={() => setCas(null)} className="ml-auto rounded border px-2 text-sm">✕</button>
                  </div>
                  {cas.texte && <p className="mt-2 whitespace-pre-wrap rounded bg-slate-50 p-2">{cas.texte}</p>}
                  {cas.lu && cas.lu.trim() !== cas.texte.trim() && <details className="mt-1 text-sm text-slate-600"><summary className="cursor-pointer">Lu par l’IA, avant correction (OCR)</summary>
                    <p className="mt-1 whitespace-pre-wrap rounded border border-dashed p-2">{cas.lu}</p></details>}
                  {!!cas.bien.length && <ul className="mt-2 text-emerald-800">{cas.bien.map((b, k) => <li key={k}>✓ {b}</li>)}</ul>}
                  {!!cas.pertes.length && <ul className="mt-2 text-rose-700">{cas.pertes.map((b, k) => <li key={k}>✘ {b}</li>)}</ul>}
                  {cas.retour && <p className="mt-2 italic text-slate-700">{cas.retour}</p>}
                </div>
              </div>)}
          </div>)}
      </div>
    </div>
  );
}
