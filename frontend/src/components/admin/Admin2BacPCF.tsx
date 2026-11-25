/**
 * Onglet « 2ᵉ Bac PC » du tableau de bord (23 novembre 2026) : le suivi des élèves du lien https://moalim.online/2bacpcf/,
 * lu comme l'onglet « Tronc Commun ». Fiche remplie une fois (nom, prénom, classe 2BACPCF + numéro, père, téléphone) ;
 * deux examens de 30 min (physique, chimie), six séances au tableau (deux révisions, quatre cours complets).
 * Le choix de l'examen en haut règle les chiffres clés, la réussite par question, les erreurs et les notes.
 * 25/11/2026 : le même onglet sert au lien du Tronc Commun physique-chimie (/TCF, `LIEN_TCF`) : `<Admin2BacPCF lien={LIEN_TCF} />`.
 */
import { Fragment, useCallback, useEffect, useMemo, useState } from 'react';
import { RefreshCw, ChevronDown, ChevronRight, Download } from 'lucide-react';
import { list2BacPCF, listTCF, type Eleve2BacPCF } from '../../services/api';
import { SUJET_CHIMIE, SUJET_PHYSIQUE } from '../../publication/bac2pcf/sujets';
import { SUJET_TCF } from '../../publication/tcf/sujet';
import { Barre, Carte, Etiquette, Tuile } from './AdminTroncCommun';

/** une couleur par matière (palette catégorielle validée) ; les cours complets en teinte claire de leur matière */
const SEANCES_2BAC: { id: string; nom: string; c: string }[] = [
  { id: 'rev_phys_ondes_radioactivite', nom: 'Révision physique', c: '#2a78d6' },
  { id: 'phys_ch3_ondes_lumineuses', nom: 'Ondes lumineuses', c: '#86b6ef' },
  { id: 'phys_ch4_radioactivite', nom: 'Radioactivité', c: '#86b6ef' },
  { id: 'rev_chim_deux_sens_equilibre', nom: 'Révision chimie', c: '#eb6834' },
  { id: 'phys_ch11_transformations_deux_sens', nom: 'Deux sens', c: '#f4a988' },
  { id: 'phys_ch12_etat_equilibre', nom: 'État d’équilibre', c: '#f4a988' },
];
type Sujet = { parties: { titre: string; questions: { id: string; texte: string; points: number }[] }[] };
const court = (t: string) => (t.length > 60 ? `${t.slice(0, 58)}…` : t);
const avecQuestions = (xs: { cle: string; nom: string; sujet: Sujet }[]) =>
  xs.map(x => ({ ...x, questions: x.sujet.parties.flatMap(p => p.questions.map(q => ({ id: q.id, texte: court(q.texte), partie: p.titre }))) }));
/** un lien libre suivi par cet onglet : ses séances, ses examens, sa route admin */
export interface LienSuivi { titre: string; fichier: string; lire: typeof list2BacPCF; seances: typeof SEANCES_2BAC; examens: ReturnType<typeof avecQuestions> }
const LIEN_2BAC: LienSuivi = { titre: '2ᵉ Bac PC', fichier: '2bacpcf', lire: list2BacPCF, seances: SEANCES_2BAC, examens: avecQuestions([
  { cle: 'examen_physique', nom: 'Physique', sujet: SUJET_PHYSIQUE as unknown as Sujet },
  { cle: 'examen_chimie', nom: 'Chimie', sujet: SUJET_CHIMIE as unknown as Sujet },
]) };
/** le Tronc Commun physique-chimie (/TCF, 25/11/2026) : trois cours, une évaluation des trois chapitres */
export const LIEN_TCF: LienSuivi = { titre: 'Tronc Commun PC', fichier: 'tcf', lire: listTCF, seances: [
  { id: 'tc_chim_synthese', nom: 'Synthèse', c: '#eb6834' },
  { id: 'tc_chim_atome', nom: 'Atome', c: '#f4a988' },
  { id: 'tc_phys_mouvement_inertie', nom: 'Mouvement et inertie', c: '#2a78d6' },
], examens: avecQuestions([{ cle: 'examen_tcf', nom: 'Évaluation', sujet: SUJET_TCF as unknown as Sujet }]) };
/** l'onglet affiché (un seul à la fois dans le tableau de bord) : réglé par la prop `lien` à chaque rendu */
let SEANCES = LIEN_2BAC.seances, EXAMENS = LIEN_2BAC.examens;
const BLEU = '#2a78d6', CRITIQUE = '#d03b3b';
const NIVEAUX: { nom: string; min: number; c: string }[] = [
  { nom: 'à soutenir (< 8)', min: 0, c: '#cde2fb' }, { nom: 'fragile (8 à 10)', min: 8, c: '#86b6ef' },
  { nom: 'correct (10 à 14)', min: 10, c: '#3987e5' }, { nom: 'bon (≥ 14)', min: 14, c: '#1c5cab' },
];
const niveauDe = (n: number) => [...NIVEAUX].reverse().find(x => n >= x.min)!;
const pts = (x?: number | null) => (x == null ? '—' : String(Math.round(x * 10) / 10).replace('.', ','));
const minutes = (s: number) => (!s ? '0 min' : s < 3600 ? `${Math.round(s / 60)} min` : `${Math.floor(s / 3600)} h ${Math.round((s % 3600) / 60)}`);
const date = (d?: string | null) => (d ? new Date(d).toLocaleString('fr-MA', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }) : '—');
const tempsCours = (e: Eleve2BacPCF) => SEANCES.reduce((n, c) => n + (e.temps[c.id] || 0), 0);

/** la note d'un examen ramenée sur 20 : celle de l'examen fini, sinon le taux de réussite des questions rendues */
function noteSur20(e: Eleve2BacPCF, cle: string) {
  const x = e.examens[cle];
  if (!x || !x.faites) return null;
  return { n: x.fini ? x.note : x.sur_fait ? (20 * x.note) / x.sur_fait : 0, fini: x.fini, faites: x.faites };
}

export default function Admin2BacPCF({ lien = LIEN_2BAC }: { lien?: LienSuivi }) {
  SEANCES = lien.seances; EXAMENS = lien.examens;
  const [eleves, setEleves] = useState<Eleve2BacPCF[]>([]);
  const [chargement, setChargement] = useState(false);
  const [erreur, setErreur] = useState('');
  const [classe, setClasse] = useState('');
  const [recherche, setRecherche] = useState('');
  const [tout, setTout] = useState(false);
  const [ouvert, setOuvert] = useState<string | null>(null);
  const [cleEx, setCleEx] = useState(EXAMENS[0].cle);
  const ex = EXAMENS.find(x => x.cle === cleEx)!;

  const charger = useCallback(async () => {
    setChargement(true); setErreur('');
    try { setEleves((await lien.lire()).data.eleves || []); }
    catch (e: any) { setErreur(e?.response?.data?.detail || 'Lecture du suivi impossible'); }
    finally { setChargement(false); }
  }, [lien]);
  useEffect(() => { void charger(); }, [charger]);

  const cherche = (e: Eleve2BacPCF) => !recherche || `${e.nom} ${e.pere} ${e.telephone}`.toLowerCase().includes(recherche.toLowerCase());
  const reels = useMemo(() => eleves.filter(e => tout || (!e.test && !e.doublon_de)), [eleves, tout]);
  const masques = eleves.length - eleves.filter(e => !e.test && !e.doublon_de).length;
  const classes = useMemo(() => [...new Set(reels.map(e => e.classe))].sort((a, b) => a.localeCompare(b, 'fr', { numeric: true })), [reels]);
  const visibles = useMemo(() => reels.filter(e => !classe || e.classe === classe).filter(cherche), [reels, classe, recherche]); // eslint-disable-line react-hooks/exhaustive-deps

  const notes = visibles.map(e => noteSur20(e, cleEx)).filter(Boolean) as { n: number; fini: boolean; faites: number }[];
  const moyenne = notes.length ? notes.reduce((s, x) => s + x.n, 0) / notes.length : null;
  const tempsMoyen = visibles.length ? visibles.reduce((s, e) => s + tempsCours(e), 0) / visibles.length : 0;

  // ── par classe : effectif, moyenne de chaque examen, niveau (examen choisi), parcours, lacunes
  const parClasse = useMemo(() => {
    const groupes = new Map<string, Eleve2BacPCF[]>();
    for (const e of reels.filter(cherche)) groupes.set(e.classe, [...(groupes.get(e.classe) || []), e]);
    return [...groupes.entries()].sort((a, b) => a[0].localeCompare(b[0], 'fr', { numeric: true })).map(([nom, es]) => {
      const moys = EXAMENS.map(x => {
        const ns = es.map(e => noteSur20(e, x.cle)).filter(Boolean) as { n: number; fini: boolean }[];
        return { nom: x.nom, cle: x.cle, n: ns.length, finis: ns.filter(y => y.fini).length,
          moy: ns.length ? ns.reduce((s, y) => s + y.n, 0) / ns.length : null, ns };
      });
      const choisi = moys.find(m => m.cle === cleEx)!;
      const lacunes = ex.questions.map(q => {
        let ob = 0, sur = 0, n = 0;
        for (const e of es) { const r = e.examens[cleEx]?.questions[q.id]; if (r) { n++; ob += r.note || 0; sur += r.sur || 0; } }
        return { ...q, n, taux: sur ? (100 * ob) / sur : null };
      }).filter(q => q.n && q.taux != null && q.taux < 60).sort((a, b) => a.taux! - b.taux!).slice(0, 3);
      const parcours = SEANCES.map(c => es.reduce((s, e) => s + Math.min(1, (e.progression[c.id]?.vues || 0) / (e.progression[c.id]?.total || 1)), 0) / es.length);
      return { nom, n: es.length, moys, niveaux: NIVEAUX.map(nv => choisi.ns.filter(x => niveauDe(x.n) === nv).length), commences: choisi.n,
        lacunes, parcours, temps: es.reduce((s, e) => s + tempsCours(e), 0) / es.length };
    });
  }, [reels, recherche, cleEx]); // eslint-disable-line react-hooks/exhaustive-deps

  const parQuestion = useMemo(() => ex.questions.map(q => {
    let n = 0, ob = 0, sur = 0;
    for (const e of visibles) { const r = e.examens[cleEx]?.questions[q.id]; if (r) { n++; ob += r.note || 0; sur += r.sur || 0; } }
    return { ...q, n, taux: sur ? (100 * ob) / sur : null };
  }).filter(q => q.n > 0).sort((a, b) => (a.taux ?? 0) - (b.taux ?? 0)), [visibles, cleEx]); // eslint-disable-line react-hooks/exhaustive-deps

  const erreurs = useMemo(() => {
    const c = new Map<string, number>();
    for (const e of visibles) for (const [id, q] of Object.entries(e.examens[cleEx]?.questions || {})) for (const p of q.pertes || []) {
      const k = `${id} · ${p.split(' : ')[0]}`.slice(0, 90);
      c.set(k, (c.get(k) || 0) + 1);
    }
    return [...c.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8);
  }, [visibles, cleEx]);

  const exporter = () => {
    const lignes = [['Élève', 'Classe', 'Père', 'Téléphone', 'Inscrit le', 'Dernière activité', ...SEANCES.map(c => `${c.nom} (diapos vues)`),
      'Temps dans les cours (min)', ...EXAMENS.flatMap(x => [`${x.nom} : questions rendues`, `${x.nom} : note /20`, `${x.nom} : terminé`]), 'Lacunes']];
    for (const e of visibles) {
      lignes.push([e.nom, e.classe, e.pere, e.telephone, date(e.date), date(e.derniere),
        ...SEANCES.map(c => `${e.progression[c.id]?.vues || 0}/${e.progression[c.id]?.total || 0}`), String(Math.round(tempsCours(e) / 60)),
        ...EXAMENS.flatMap(x => { const n = noteSur20(e, x.cle); return [String(e.examens[x.cle]?.faites || 0), n ? pts(n.n) : '', n?.fini ? 'oui' : 'non']; }),
        e.lacunes.join(' | ')]);
    }
    const csv = '﻿' + lignes.map(l => l.map(x => `"${String(x).replace(/"/g, '""')}"`).join(';')).join('\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    a.download = `${lien.fichier}${classe ? `-${classe.replace(/\s/g, '')}` : ''}.csv`;
    a.click();
  };

  return (
    <div className="space-y-5 text-gray-900">
      <div className="flex flex-wrap items-center gap-2">
        <h2 className="mr-auto text-lg font-semibold">{lien.titre} — suivi des élèves</h2>
        <span className="flex overflow-hidden rounded-lg border text-sm">{EXAMENS.map(x => (
          <button key={x.cle} onClick={() => setCleEx(x.cle)} className={`px-3 py-1.5 ${cleEx === x.cle ? 'bg-gray-900 text-white' : 'hover:bg-gray-50'}`}>Examen {x.nom.toLowerCase()}</button>))}</span>
        <select value={classe} onChange={e => setClasse(e.target.value)} className="rounded-lg border px-2 py-1.5 text-sm">
          <option value="">Toutes les classes</option>
          {classes.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <input value={recherche} onChange={e => setRecherche(e.target.value)} placeholder="Chercher un élève…" className="rounded-lg border px-2 py-1.5 text-sm" />
        <label className="flex items-center gap-1 text-sm text-gray-600"><input type="checkbox" checked={tout} onChange={e => setTout(e.target.checked)} />
          tests et doublons ({masques})</label>
        <button onClick={exporter} className="flex items-center gap-1 rounded-lg border px-2 py-1.5 text-sm hover:bg-gray-50"><Download className="h-4 w-4" /> CSV</button>
        <button onClick={() => void charger()} className="flex items-center gap-1 rounded-lg border px-2 py-1.5 text-sm hover:bg-gray-50">
          <RefreshCw className={`h-4 w-4 ${chargement ? 'animate-spin' : ''}`} /> Actualiser</button>
      </div>
      {erreur && <p className="text-sm text-red-600">{erreur}</p>}

      <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
        <Tuile titre="Élèves" valeur={String(visibles.length)} sous={classe || 'toutes les classes'} />
        <Tuile titre={`Ont commencé l’examen de ${ex.nom.toLowerCase()}`} valeur={String(notes.length)} sous={`sur ${visibles.length}`} />
        <Tuile titre="L’ont terminé" valeur={String(notes.filter(x => x.fini).length)} sous={`sur ${notes.length} commencés`} />
        <Tuile titre="Moyenne" valeur={moyenne == null ? '—' : `${pts(moyenne)} / 20`} sous="sur les questions rendues" />
        <Tuile titre="Temps moyen dans les cours" valeur={minutes(tempsMoyen)} sous="par élève" />
      </div>

      {!visibles.length && !chargement && <p className="text-sm text-gray-500">Aucun élève pour l’instant (lien : https://moalim.online/2bacpcf/).</p>}

      {!!parClasse.length && (
        <div className="rounded-xl border bg-white p-4">
          <p className="font-semibold">Par classe</p>
          <p className="mb-3 text-xs text-gray-500">Moyenne de chaque examen sur les questions rendues (ramenée sur 20) ; niveau et lacunes de l’examen de {ex.nom.toLowerCase()} ; parcours moyen dans les six séances. Cliquer sur une classe la filtre.</p>
          <div className="mb-2 flex flex-wrap gap-3 text-xs text-gray-600">
            <span className="font-medium text-gray-700">Niveau :</span>
            {NIVEAUX.map(nv => <span key={nv.nom} className="flex items-center gap-1"><span className="inline-block h-2.5 w-3 rounded-sm" style={{ background: nv.c }} />{nv.nom}</span>)}
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="text-left text-xs text-gray-500"><tr>
                <th className="py-1 pr-3">Classe</th><th className="py-1 pr-3">Élèves</th><th className="py-1 pr-3">Moyennes</th>
                <th className="py-1 pr-3">Niveau ({ex.nom.toLowerCase()})</th><th className="py-1 pr-3">Parcours des séances</th><th className="py-1">Lacunes principales ({ex.nom.toLowerCase()})</th></tr></thead>
              <tbody>{parClasse.map(c => (
                <tr key={c.nom} onClick={() => setClasse(classe === c.nom ? '' : c.nom)}
                  className={`cursor-pointer border-t align-top hover:bg-gray-50 ${classe === c.nom ? 'bg-blue-50' : ''}`}>
                  <td className="py-2 pr-3 font-semibold whitespace-nowrap">{c.nom}</td>
                  <td className="py-2 pr-3 whitespace-nowrap text-xs text-gray-700"><b className="text-sm text-gray-900">{c.n}</b> inscrits</td>
                  <td className="py-2 pr-3 whitespace-nowrap text-xs">{c.moys.map(m => (
                    <span key={m.cle} className="block"><span className="text-gray-500">{m.nom} :</span> <b className="text-sm">{m.moy == null ? '—' : `${pts(m.moy)} / 20`}</b>
                      <span className="text-gray-500"> · {m.n} commencé{m.n > 1 ? 's' : ''}, {m.finis} fini{m.finis > 1 ? 's' : ''}</span></span>))}</td>
                  <td className="w-44 py-2 pr-3">
                    {c.commences ? <>
                      <span className="flex h-3 w-full overflow-hidden rounded bg-gray-100">{c.niveaux.map((k, i) => k ? (
                        <span key={i} title={`${NIVEAUX[i].nom} : ${k} élève${k > 1 ? 's' : ''}`} style={{ width: `${(100 * k) / c.commences}%`, background: NIVEAUX[i].c }}
                          className="h-full border-r-2 border-white last:border-r-0" />) : null)}</span>
                      <span className="mt-0.5 block text-[11px] text-gray-500">{c.niveaux.map((k, i) => (k ? `${k} ${NIVEAUX[i].nom.split(' (')[0]}` : '')).filter(Boolean).join(' · ')}</span>
                    </> : <span className="text-xs text-gray-400">pas encore d’examen</span>}</td>
                  <td className="w-56 py-2 pr-3">{SEANCES.map((co, i) => (
                    <span key={co.id} className="mb-0.5 flex items-center gap-1.5 text-[11px]" title={`${co.nom} : ${Math.round(c.parcours[i] * 100)} % des diapos en moyenne`}>
                      <span className="w-24 shrink-0 truncate text-gray-600">{co.nom}</span>
                      <span className="h-2 flex-1 rounded-r bg-gray-100"><span className="block h-full rounded-r" style={{ width: `${c.parcours[i] * 100}%`, background: co.c }} /></span>
                      <span className="w-8 shrink-0 text-right text-gray-600">{Math.round(c.parcours[i] * 100)} %</span></span>))}
                    <span className="text-[11px] text-gray-500">{minutes(c.temps)} par élève</span></td>
                  <td className="py-2 text-xs">{c.lacunes.length ? <ul className="space-y-0.5">{c.lacunes.map(q => (
                    <li key={q.id}><span className="font-semibold" style={{ color: CRITIQUE }}>{Math.round(q.taux!)} %</span> · {q.id} {q.texte} <span className="text-gray-400">({q.n} élève{q.n > 1 ? 's' : ''})</span></li>))}</ul>
                    : <span className="text-gray-400">—</span>}</td>
                </tr>))}</tbody>
            </table>
          </div>
        </div>)}

      {!!visibles.length && (
        <div className="grid gap-4 lg:grid-cols-2">
          <Carte titre={`Note de chaque élève — examen de ${ex.nom.toLowerCase()} (sur 20)`} aide="Barre pleine : examen terminé ; barre claire : en cours (note sur les questions déjà rendues).">
            {visibles.map(e => ({ e, n: noteSur20(e, cleEx) })).sort((a, b) => (b.n?.n ?? -1) - (a.n?.n ?? -1)).map(({ e, n }) => (
              <Barre key={e.id} libelle={e.nom} sous={e.classe} valeur={n?.n ?? 0} max={20} couleur={BLEU} clair={!n?.fini}
                texte={n ? `${pts(n.n)} / 20 · ${n.faites} q.` : 'pas commencé'} titre={`${e.nom} — ${n ? `${pts(n.n)} / 20, ${n.faites} questions rendues` : 'examen pas commencé'}`} />))}
          </Carte>
          <Carte titre="Réussite par question" aide="Les plus ratées en haut : c’est par là qu’il faut reprendre en classe.">
            {parQuestion.length ? parQuestion.map(q => (
              <Barre key={q.id} libelle={`${q.id} · ${q.texte}`} valeur={q.taux ?? 0} max={100} couleur={BLEU}
                texte={`${Math.round(q.taux ?? 0)} % · ${q.n} élève${q.n > 1 ? 's' : ''}`} alerte={(q.taux ?? 0) < 50}
                titre={`${q.id} — ${q.texte} : ${Math.round(q.taux ?? 0)} % de réussite (${q.n} élèves)`} />))
              : <p className="text-sm text-gray-500">Aucune question rendue.</p>}
          </Carte>
          <Carte titre="Erreurs les plus fréquentes" aide="Élément du barème perdu, et combien d’élèves l’ont perdu.">
            {erreurs.length ? erreurs.map(([k, n]) => (
              <Barre key={k} libelle={k} valeur={n} max={Math.max(...erreurs.map(x => x[1]))} couleur={BLEU} texte={`${n} élève${n > 1 ? 's' : ''}`} titre={`${k} : ${n}`} />))
              : <p className="text-sm text-gray-500">Pas encore d’erreur relevée.</p>}
          </Carte>
          <Carte titre="Parcours dans les séances (diapositives vues)" aide="Bleu : physique (révision foncée, cours complets clairs) ; orange : chimie.">
            <div className="mb-2 flex flex-wrap gap-3 text-xs text-gray-600">{SEANCES.map(c => <span key={c.id} className="flex items-center gap-1"><span className="inline-block h-2.5 w-3 rounded-sm" style={{ background: c.c }} />{c.nom}</span>)}</div>
            {visibles.map(e => (
              <div key={e.id} className="mb-1.5 flex items-center gap-2 text-sm">
                <span className="w-36 shrink-0 truncate" title={e.nom}>{e.nom}</span>
                <span className="flex flex-1 flex-col gap-0.5">{SEANCES.map(c => {
                  const p = e.progression[c.id]; const pc = p?.total ? Math.min(100, (100 * p.vues) / p.total) : 0;
                  return <span key={c.id} className="h-1.5 w-full rounded-full bg-gray-100" title={`${c.nom} : ${p?.vues || 0} / ${p?.total || 0} diapos`}>
                    <span className="block h-full rounded-full" style={{ width: `${pc}%`, background: c.c }} /></span>;
                })}</span>
                <span className="w-16 shrink-0 text-right text-xs text-gray-500">{minutes(tempsCours(e))}</span>
              </div>))}
          </Carte>
        </div>)}

      {!!visibles.length && (
        <div className="overflow-x-auto rounded-xl border bg-white">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-left text-gray-600">
              <tr><th className="px-3 py-2" /><th className="px-3 py-2">Élève</th><th className="px-3 py-2">Classe</th>
                {EXAMENS.map(x => <th key={x.cle} className="px-3 py-2">{x.nom}</th>)}
                <th className="px-3 py-2">Temps (cours · examens)</th><th className="px-3 py-2">Père · téléphone</th><th className="px-3 py-2">Dernière activité</th></tr>
            </thead>
            <tbody>{visibles.map(e => {
              const vu = ouvert === e.id;
              return (
                <Fragment key={e.id}>
                  <tr className="cursor-pointer border-t hover:bg-gray-50" onClick={() => setOuvert(vu ? null : e.id)}>
                    <td className="px-2 py-2 text-gray-400">{vu ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}</td>
                    <td className="px-3 py-2 font-medium">{e.nom}{e.test && <Etiquette>test</Etiquette>}{e.doublon_de && <Etiquette>doublon</Etiquette>}</td>
                    <td className="px-3 py-2 whitespace-nowrap">{e.classe}</td>
                    {EXAMENS.map(x => { const n = noteSur20(e, x.cle); return (
                      <td key={x.cle} className="px-3 py-2 whitespace-nowrap">{n ? <><b>{pts(n.n)} / 20</b> <span className="text-xs text-gray-500">{n.fini ? 'terminé' : `${n.faites}/${x.questions.length} q.`}</span></> : <span className="text-gray-400">—</span>}</td>); })}
                    <td className="px-3 py-2 whitespace-nowrap">{minutes(tempsCours(e))} · {minutes(EXAMENS.reduce((s, x) => s + (e.temps[x.cle] || 0), 0))}</td>
                    <td className="px-3 py-2 whitespace-nowrap">{e.pere} · <a href={`tel:${e.telephone}`} className="text-blue-700" onClick={x => x.stopPropagation()}>{e.telephone}</a></td>
                    <td className="px-3 py-2 whitespace-nowrap text-gray-500">{date(e.derniere)}</td>
                  </tr>
                  {vu && <tr className="border-t bg-gray-50/60"><td /><td colSpan={7} className="px-3 py-3"><Detail e={e} /></td></tr>}
                </Fragment>);
            })}</tbody>
          </table>
        </div>)}
    </div>
  );
}

function Detail({ e }: { e: Eleve2BacPCF }) {
  return (
    <div className="grid gap-4 lg:grid-cols-3">
      {EXAMENS.map(x => {
        const qs = e.examens[x.cle]?.questions || {};
        return (
          <div key={x.cle}>
            <p className="mb-1 font-semibold text-gray-800">Examen de {x.nom.toLowerCase()}</p>
            {Object.keys(qs).length ? (
              <table className="w-full text-xs"><tbody>{x.questions.filter(q => qs[q.id]).map(q => {
                const r = qs[q.id]; const ok = (r.note || 0) >= (r.sur || 0);
                return (
                  <tr key={q.id} className="border-t align-top">
                    <td className="whitespace-nowrap py-1 pr-2 font-semibold">{q.id}</td>
                    <td className={`py-1 pr-2 whitespace-nowrap font-semibold ${ok ? 'text-green-700' : (r.note || 0) > 0 ? 'text-amber-700' : 'text-red-700'}`}>{pts(r.note)} / {pts(r.sur)}</td>
                    <td className="py-1 text-gray-700">{q.texte}{r.pertes?.length ? <span className="block text-red-700">− {r.pertes.join(' ; ')}</span> : null}</td>
                  </tr>);
              })}</tbody></table>) : <p className="text-xs text-gray-500">Aucune question rendue.</p>}
          </div>);
      })}
      <div>
        <p className="mb-1 font-semibold text-gray-800">Parcours et réponses dans les cours</p>
        <ul className="mb-3 space-y-0.5 text-xs text-gray-700">{SEANCES.map(c => <li key={c.id}>{c.nom} : {e.progression[c.id]?.vues || 0} / {e.progression[c.id]?.total || 0} diapos · {minutes(e.temps[c.id] || 0)}</li>)}
          <li>Réponses dans les cours : {e.reponses_cours.justes} justes, {e.reponses_cours.fausses} fausses</li></ul>
        <p className="mb-1 font-semibold text-gray-800">À retravailler</p>
        {e.lacunes.length ? <ul className="list-disc space-y-0.5 pl-5 text-xs text-gray-700">{e.lacunes.slice(0, 15).map((l, k) => <li key={k}>{l}</li>)}</ul>
          : <p className="text-xs text-gray-500">Rien de signalé.</p>}
        <p className="mt-2 text-xs text-gray-500">Inscrit le {date(e.date)}{e.classe_ecrite && e.classe_ecrite !== e.classe ? ` · classe écrite « ${e.classe_ecrite} »` : ''}</p>
      </div>
    </div>);
}
