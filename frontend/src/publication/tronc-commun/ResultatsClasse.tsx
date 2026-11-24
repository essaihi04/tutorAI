/**
 * Les résultats de la classe pendant une séance du mode classe (25 novembre 2026) : rien n'est enregistré, tout vit le temps
 * de la séance ; le prof peut télécharger un CSV fabriqué dans son navigateur.
 *   - le score de chaque élève (barres horizontales triées, note ramenée sur les points des questions déjà posées, moyenne
 *     de la classe en repère) ;
 *   - la grille élèves × questions (juste / en partie / faux / pas de réponse) et la réussite de chaque question ;
 *   - le petit rapport d'un élève : sa note, ce qu'il réussit, ce qui lui manque, ce qu'il doit revoir (diapositives).
 * Couleurs comme l'onglet admin du Tronc Commun : bleu #2a78d6 pour les barres, rouge critique #d03b3b, verdicts en
 * vert / orange / rouge / gris (pas encore).
 */
import { useMemo } from 'react';
import { pts } from '../../components/exercice/types';
import { configExamen } from './Examen';
import { lienDiapo, REVOIR_TC, type Lien } from './revoir';
import type { QuestionExamen } from './sujet';

export type Participant = { id: string; nom: string; prenom: string; classe: string; regarde?: string };
export type VerdictMur = 'juste' | 'partiel' | 'faux' | 'nonjuge' | 'regarder';
export type ReponseMur = { id: string; numero: number; question: string; texte: string; note: number | null; sur: number; verdict: VerdictMur;
  pertes: string[]; bien: string[]; retour: string; image: boolean; mien: boolean; eleve?: string; heure?: number; ordre?: number };
export type EtatSeance = { code: string; version: number; question: string; correction: boolean; reponses: ReponseMur[]; par_question: Record<string, number>;
  posees: string[]; participants: Participant[]; moi: Participant | null; toutes?: ReponseMur[]; prof?: boolean; demandes_prof?: string[] };

const BLEU = '#2a78d6';
const CRITIQUE = '#d03b3b';
/** juste, en partie, faux, à regarder, pas encore */
export const COULEUR_VERDICT: Record<VerdictMur | 'rien', string> = { juste: '#2e9e5b', partiel: '#e8a33d', faux: CRITIQUE, nonjuge: '#86b6ef', regarder: '#86b6ef', rien: '#c9ccd1' };
export const MOT_VERDICT: Record<VerdictMur | 'rien', string> = { juste: 'juste', partiel: 'en partie', faux: 'faux', nonjuge: 'à regarder', regarder: 'à regarder', rien: 'pas encore' };

export const nomComplet = (p: Participant) => `${p.prenom} ${p.nom}`;
/** le prénom ; avec l'initiale du nom si deux élèves ont le même prénom */
export const nomCourt = (p: Participant, tous: Participant[]) =>
  tous.filter(x => x.prenom.toLowerCase() === p.prenom.toLowerCase()).length > 1 ? `${p.prenom} ${p.nom.charAt(0).toUpperCase()}.` : p.prenom;

export type BilanEleve = { p: Participant; par: Record<string, ReponseMur>; note: number; sur: number; taux: number; repondues: number };
export function bilanClasse(etat: EtatSeance) {
  const qs = configExamen().questions;
  // les questions déjà projetées, dans l'ordre du sujet
  const ordre: QuestionExamen[] = qs.filter(x => etat.posees.includes(x.q.id)).map(x => x.q);
  const sur = ordre.reduce((n, q) => n + q.points, 0);
  const toutes = etat.toutes || [];
  const eleves: BilanEleve[] = etat.participants.map(p => {
    const par: Record<string, ReponseMur> = {};
    for (const r of toutes) if (r.eleve === p.id) par[r.question] = r;
    const note = ordre.reduce((n, q) => n + (par[q.id]?.note ?? 0), 0);
    return { p, par, note, sur, taux: sur ? note / sur : 0, repondues: ordre.filter(q => par[q.id]).length };
  });
  const moyenne = eleves.length ? eleves.reduce((n, e) => n + e.taux, 0) / eleves.length : 0;
  const parQuestion = ordre.map(q => {
    const rs = eleves.map(e => e.par[q.id]).filter((r): r is ReponseMur => !!r);
    const notees = rs.filter(r => r.note != null);
    return { q, n: rs.length, justes: rs.filter(r => r.verdict === 'juste').length,
      taux: notees.length ? notees.reduce((n, r) => n + (r.note || 0) / q.points, 0) / notees.length : 0 };
  });
  return { ordre, sur, eleves, moyenne, parQuestion };
}

const sur20 = (taux: number) => pts(Math.round(taux * 20 * 4) / 4);

/** Le tableau de bord de la classe : scores, grille, réussite par question, CSV. */
export function ResultatsClasse({ etat, onEleve }: { etat: EtatSeance; onEleve: (id: string) => void }) {
  const b = useMemo(() => bilanClasse(etat), [etat]);
  const tries = [...b.eleves].sort((x, y) => y.taux - x.taux || x.p.prenom.localeCompare(y.p.prenom));
  if (!b.eleves.length) return <p className="p-6 text-center text-[clamp(16px,1.4vw,22px)] text-slate-600">Aucun élève pour l’instant : ils entrent leur nom en visant le QR code.</p>;
  return (
    <div className="grid gap-4 xl:grid-cols-2" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <section className="rounded-xl border bg-white p-4">
        <div className="flex flex-wrap items-baseline gap-2">
          <h3 className="text-lg font-bold">Score de chaque élève</h3>
          <span className="text-sm text-slate-500">sur les {b.ordre.length} question{b.ordre.length > 1 ? 's' : ''} posée{b.ordre.length > 1 ? 's' : ''} ({pts(b.sur)} points) · un élève sans réponse a 0</span>
        </div>
        <p className="mb-2 mt-1 flex items-center gap-2 text-sm text-slate-600">
          <span className="inline-block h-3 w-6 rounded-r" style={{ background: BLEU }} /> note de l’élève
          <span className="ml-3 inline-block h-4 border-l-2 border-dashed border-slate-700" /> moyenne de la classe : <b>{pts(Math.round(b.moyenne * b.sur * 100) / 100)} / {pts(b.sur)}</b> ({sur20(b.moyenne)} / 20)
        </p>
        <div className="max-h-[56vh] overflow-y-auto pr-1">
          {tries.map(e => (
            <button key={e.p.id} onClick={() => onEleve(e.p.id)} className="group mb-1 flex w-full items-center gap-2 rounded px-1 py-0.5 text-left text-[15px] hover:bg-slate-50"
              title={`${nomComplet(e.p)} : ${pts(e.note)} / ${pts(e.sur)} — cliquer pour son rapport`}>
              <span className="w-40 shrink-0 truncate font-medium group-hover:underline">{nomComplet(e.p)}</span>
              <span className="relative h-3.5 flex-1 rounded-r bg-slate-100">
                <span className="block h-full rounded-r" style={{ width: `${Math.max(0, Math.min(100, e.taux * 100))}%`, background: BLEU }} />
                <span className="absolute -bottom-1 -top-1 border-l-2 border-dashed border-slate-700" style={{ left: `${b.moyenne * 100}%` }} />
              </span>
              <span className="w-28 shrink-0 whitespace-nowrap text-right text-sm text-slate-800"><b>{pts(e.note)}</b> / {pts(e.sur)}{e.taux < 0.5 && e.repondues ? <span className="ml-1 font-semibold" style={{ color: CRITIQUE }}>!</span> : null}</span>
            </button>))}
        </div>
      </section>

      <section className="rounded-xl border bg-white p-4">
        <h3 className="text-lg font-bold">Élèves × questions</h3>
        <p className="mb-2 mt-1 flex flex-wrap gap-3 text-sm text-slate-600">
          {(['juste', 'partiel', 'faux', 'regarder', 'rien'] as const).map(v => <span key={v} className="flex items-center gap-1"><span className="inline-block h-3.5 w-3.5 rounded-sm" style={{ background: COULEUR_VERDICT[v] }} />{MOT_VERDICT[v]}</span>)}
        </p>
        <div className="max-h-[56vh] overflow-auto">
          <table className="border-separate border-spacing-0.5 text-[13px]">
            <thead><tr><th className="sticky left-0 bg-white" />{b.ordre.map(q => <th key={q.id} className="px-0.5 text-center font-semibold">{q.id}</th>)}</tr></thead>
            <tbody>
              {tries.map(e => (
                <tr key={e.p.id} className="cursor-pointer hover:bg-slate-50" onClick={() => onEleve(e.p.id)}>
                  <td className="sticky left-0 max-w-[9rem] truncate bg-white pr-2 text-[14px]">{nomCourt(e.p, etat.participants)}</td>
                  {b.ordre.map(q => {
                    const r = e.par[q.id];
                    const v = r ? r.verdict : 'rien';
                    return <td key={q.id} className="h-7 min-w-9 rounded text-center font-semibold text-white" style={{ background: COULEUR_VERDICT[v], color: v === 'rien' ? '#555' : v === 'nonjuge' || v === 'regarder' ? '#0b2a4a' : '#fff' }}
                      title={`${nomComplet(e.p)} · question ${q.id} : ${MOT_VERDICT[v]}${r?.note != null ? ` (${pts(r.note)} / ${pts(q.points)})` : ''}`}>{r?.note != null ? pts(r.note) : r ? '?' : ''}</td>;
                  })}
                </tr>))}
              <tr><td className="sticky left-0 bg-white pr-2 pt-1 text-[13px] text-slate-600">Réussite</td>
                {b.parQuestion.map(x => (
                  <td key={x.q.id} className="pt-1 align-bottom" title={`Question ${x.q.id} : ${x.justes} juste${x.justes > 1 ? 's' : ''} sur ${x.n} réponse${x.n > 1 ? 's' : ''} ; ${Math.round(x.taux * 100)} % des points`}>
                    <div className="mx-auto flex h-12 w-3 items-end rounded-t bg-slate-100"><div className="w-full rounded-t" style={{ height: `${x.taux * 100}%`, background: x.taux < 0.5 ? CRITIQUE : BLEU }} /></div>
                    <p className="text-center text-[11px] text-slate-700">{x.n ? `${Math.round(x.taux * 100)}%` : '—'}</p>
                  </td>))}
              </tr>
            </tbody>
          </table>
        </div>
        {!!b.parQuestion.length && (() => {
          const dure = [...b.parQuestion].filter(x => x.n).sort((x, y) => x.taux - y.taux)[0];
          return dure && dure.taux < 0.5 ? <p className="mt-2 text-sm" style={{ color: CRITIQUE }}>La question la moins réussie : <b>{dure.q.id}</b> ({Math.round(dure.taux * 100)} % des points).</p> : null;
        })()}
      </section>
    </div>
  );
}

const court = (t: string, n = 80) => (t.length > n ? `${t.slice(0, n - 1).trimEnd()}…` : t);
/** « Rétention : B retient plus d’eau que A : −0,25 (absente) » → « Rétention : B retient plus d’eau que A » */
const sansPoints = (perte: string) => perte.replace(/\s*:\s*−[\d,]+.*$/, '').replace(/\s*:\s*$/, '').trim();

/** Le petit rapport d'un élève, en mots simples. */
export function RapportEleve({ etat, id, onFermer, onAutre }: { etat: EtatSeance; id: string; onFermer: () => void; onAutre: (id: string) => void }) {
  const b = bilanClasse(etat);
  const k = b.eleves.findIndex(e => e.p.id === id);
  const e = b.eleves[k];
  if (!e) return null;
  const reussies = b.ordre.filter(q => e.par[q.id]?.verdict === 'juste');
  const manques: string[] = [];
  for (const q of b.ordre) {
    const r = e.par[q.id];
    if (!r) { manques.push(`Question ${q.id} : pas de réponse`); continue; }
    if (r.verdict === 'juste') continue;
    if ((q.genre === 'qcm' || q.genre === 'vf') && r.pertes.length) {
      // un QCM : les propositions ratées, par leur lettre
      const items = q.items as { texte: string }[];
      const lettres = r.pertes.map(x => items.findIndex(it => sansPoints(x).startsWith(sansPoints(it.texte)))).filter(j => j >= 0).map(j => String.fromCharCode(97 + j));
      manques.push(items.length > 1 && lettres.length
        ? `Question ${q.id} : ${lettres.length > 1 ? `propositions ${lettres.slice(0, -1).join(', ')} et ${lettres[lettres.length - 1]} fausses` : `proposition ${lettres[0]} fausse`} (${lettres.length} sur ${items.length})`
        : `Question ${q.id} : réponse fausse`);
    } else if (r.pertes.length) r.pertes.forEach(x => manques.push(`${sansPoints(x)} (question ${q.id})`));
    else manques.push(`Question ${q.id} : ${r.verdict === 'faux' ? 'réponse fausse' : r.verdict === 'partiel' ? 'réponse incomplète' : 'à regarder avec le prof'}`);
  }
  const revoir: Lien[] = [];
  for (const q of b.ordre) {
    const r = e.par[q.id];
    if (r && (r.note ?? 0) >= q.points) continue;
    for (const l of REVOIR_TC[q.id] || []) if (!revoir.some(x => x.diapo === l.diapo)) revoir.push(l);
  }
  const bouton = 'rounded-lg border border-slate-400 px-3 py-1.5 text-sm hover:bg-slate-100 disabled:opacity-30';
  return (
    <div className="fixed inset-0 z-[1000] grid place-items-center bg-black/60 p-2" onClick={onFermer} role="dialog" aria-label={`Rapport de ${nomComplet(e.p)}`}>
      <div className="max-h-[94dvh] w-[min(96vw,760px)] overflow-y-auto rounded-2xl bg-white p-5 text-slate-900 shadow-2xl" onClick={ev => ev.stopPropagation()} style={{ fontFamily: 'system-ui, sans-serif' }}>
        <div className="flex flex-wrap items-center gap-2">
          <h3 className="flex-1 text-2xl font-bold">{nomComplet(e.p)}{e.p.classe && <span className="ml-2 text-base font-normal text-slate-500">{e.p.classe}</span>}</h3>
          <button className={bouton} disabled={k <= 0} onClick={() => onAutre(b.eleves[k - 1].p.id)}>← Précédent</button>
          <button className={bouton} disabled={k >= b.eleves.length - 1} onClick={() => onAutre(b.eleves[k + 1].p.id)}>Élève suivant →</button>
          <button className={bouton} onClick={onFermer} aria-label="Fermer">✕</button>
        </div>
        <p className="mt-2 text-xl">Note : <b>{pts(e.note)} / {pts(e.sur)}</b> <span className="text-slate-500">({sur20(e.taux)} / 20)</span>
          <span className="ml-2 text-base text-slate-600">· {e.repondues} réponse{e.repondues > 1 ? 's' : ''} sur {b.ordre.length} question{b.ordre.length > 1 ? 's' : ''}</span></p>
        <div className="mt-3 grid gap-3 sm:grid-cols-2">
          <div className="rounded-xl border-2 border-emerald-600 p-3">
            <p className="font-bold text-emerald-800">✔ Ce qu’il réussit</p>
            {reussies.length ? <ul className="mt-1 space-y-1 text-[15px]">{reussies.map(q => <li key={q.id}><b>{q.id}</b> — {court(q.texte)}</li>)}</ul>
              : <p className="mt-1 text-[15px] text-slate-600">Pas encore de question entièrement juste.</p>}
          </div>
          <div className="rounded-xl border-2 p-3" style={{ borderColor: CRITIQUE }}>
            <p className="font-bold" style={{ color: CRITIQUE }}>✘ Ce qui lui manque</p>
            {manques.length ? <ul className="mt-1 space-y-1 text-[15px]">{manques.map((m, j) => <li key={j}>{m}</li>)}</ul>
              : <p className="mt-1 text-[15px] text-slate-600">Rien : tout est juste.</p>}
          </div>
        </div>
        {!!revoir.length && (
          <div className="mt-3 rounded-xl border-2 p-3" style={{ borderColor: BLEU }}>
            <p className="font-bold" style={{ color: BLEU }}>↻ À revoir</p>
            <ul className="mt-1 flex flex-wrap gap-2">{revoir.map(l => (
              <li key={l.diapo}><a href={lienDiapo(l)} target="_blank" rel="noreferrer" className="inline-block rounded-lg border border-slate-400 px-2 py-1 text-[15px] text-blue-800 underline">{l.titre}</a></li>))}</ul>
          </div>)}
      </div>
    </div>
  );
}

/** Les résultats en CSV (séparateur « ; », pour Excel en français), fabriqué dans le navigateur : rien ne part au serveur. */
export function telechargerCsv(etat: EtatSeance) {
  const b = bilanClasse(etat);
  const champ = (x: string | number) => { const s = String(x); return /[;"\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
  const lignes = [
    ['Élève', 'Classe', ...b.ordre.map(q => `Q ${q.id} (/${pts(q.points)})`), 'Total', 'Sur', 'Sur 20', 'Éléments perdus'],
    ...[...b.eleves].sort((x, y) => x.p.nom.localeCompare(y.p.nom) || x.p.prenom.localeCompare(y.p.prenom)).map(e => [
      nomComplet(e.p), e.p.classe,
      ...b.ordre.map(q => { const r = e.par[q.id]; return r ? (r.note != null ? pts(r.note) : 'à regarder') : ''; }),
      pts(e.note), pts(e.sur), sur20(e.taux),
      b.ordre.flatMap(q => (e.par[q.id]?.pertes || []).map(x => `${q.id} : ${x}`)).join(' | '),
    ]),
  ];
  const texte = '﻿' + lignes.map(l => l.map(champ).join(';')).join('\r\n');
  const url = URL.createObjectURL(new Blob([texte], { type: 'text/csv;charset=utf-8' }));
  const a = document.createElement('a');
  const d = new Date();
  a.href = url; a.download = `resultats-classe-${etat.code}-${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}.csv`;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}
