/**
 * Onglet « Tronc Commun » du tableau de bord (22 novembre 2026, refait le 23/11 pour être lu d'un coup d'œil).
 *
 * Les élèves du lien libre https://moalim.online/tronc-commun/ remplissent une fiche une seule fois (nom, prénom, classe
 * TCSF + numéro, père, téléphone) ; la page envoie leur suivi (`public_tronc_commun.py`, une seule réponse comptée par
 * question). Ici : les chiffres clés, la note de chaque élève, la réussite par question, les erreurs les plus fréquentes,
 * le parcours dans les cours, puis le détail d'un élève. Les comptes de test et les doublons sont masqués par défaut.
 */
import { Fragment, useCallback, useEffect, useMemo, useState } from 'react';
import { RefreshCw, ChevronDown, ChevronRight, Download, AlertTriangle } from 'lucide-react';
import { listTroncCommun, type EleveTroncCommun } from '../../services/api';

/** une couleur par cours, la même partout (palette catégorielle validée : bleu, orange, aqua) */
const COURS: { id: string; nom: string; c: string }[] = [
  { id: 'tc_svt_sortie_ecologique', nom: 'Sortie écologique', c: '#1baf7a' },
  { id: 'tc_svt_facteurs_edaphiques', nom: 'Facteurs édaphiques', c: '#eb6834' },
  { id: 'tc_svt_revision', nom: 'Révision', c: '#2a78d6' },
];
const BLEU = '#2a78d6', CRITIQUE = '#d03b3b';
/** ce que vérifie chaque question de l'évaluation, en quelques mots */
const SUJETS: Record<string, string> = {
  '1': 'QCM (texture, calcifuge, eau capillaire, croix)', '2': 'Vrai / faux', '3-a': 'Définir le point de flétrissement', '3-b': 'Définir l’aire minimale',
  '1-1': 'Calcul de P (sol A)', '1-2': 'Calcul de P (sol B)', '1-3': 'Calcul de Vr (sol A)', '1-4': 'Calcul de Vr (sol B)',
  '1-5': 'Comparer : sableux / argileux', '1-6': 'Formes de l’eau, flétrissement', '1-7': 'Tracer dans le triangle des textures',
  '2-1': 'Interpréter éosine / bleu de méthylène', '2-2': 'Charge et constituants du CAH', '2-3': 'Rôle du CAH (nutrition)',
  '3-1': 'Lire l’aire minimale', '3-2': 'Calculer la fréquence F', '3-3': 'Indice de fréquence', '3-4': 'Calculer la densité D',
  '3-5': 'Tableau → histogramme → courbe', '3-6': 'Interpréter la courbe bimodale',
};
const ORDRE = Object.keys(SUJETS);
const pts = (x?: number | null) => (x == null ? '—' : String(Math.round(x * 100) / 100).replace('.', ','));
const minutes = (s: number) => (!s ? '0 min' : s < 3600 ? `${Math.round(s / 60)} min` : `${Math.floor(s / 3600)} h ${Math.round((s % 3600) / 60)}`);
const date = (d?: string | null) => (d ? new Date(d).toLocaleString('fr-MA', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }) : '—');

/** la note de l'élève, ramenée sur 20 : celle de l'évaluation terminée, sinon le taux de réussite des questions rendues */
function noteSur20(e: EleveTroncCommun) {
  const fin = e.examens[e.examens.length - 1];
  const ec = e.examen_en_cours;
  if (fin) return { n: fin.note, fini: true, faites: ec.faites };
  if (ec.faites && ec.sur) return { n: (20 * ec.note) / ec.sur, fini: false, faites: ec.faites };
  return null;
}
const tempsCours = (e: EleveTroncCommun) => COURS.reduce((n, c) => n + (e.temps[c.id] || 0), 0);

export default function AdminTroncCommun() {
  const [eleves, setEleves] = useState<EleveTroncCommun[]>([]);
  const [chargement, setChargement] = useState(false);
  const [erreur, setErreur] = useState('');
  const [classe, setClasse] = useState('');
  const [recherche, setRecherche] = useState('');
  const [tout, setTout] = useState(false);
  const [ouvert, setOuvert] = useState<string | null>(null);

  const charger = useCallback(async () => {
    setChargement(true); setErreur('');
    try { setEleves((await listTroncCommun()).data.eleves || []); }
    catch (e: any) { setErreur(e?.response?.data?.detail || 'Lecture du suivi impossible'); }
    finally { setChargement(false); }
  }, []);
  useEffect(() => { void charger(); }, [charger]);

  const reels = useMemo(() => eleves.filter(e => tout || (!e.test && !e.doublon_de)), [eleves, tout]);
  const masques = eleves.length - eleves.filter(e => !e.test && !e.doublon_de).length;
  const classes = useMemo(() => [...new Set(reels.map(e => e.classe))].sort((a, b) => a.localeCompare(b, 'fr', { numeric: true })), [reels]);
  const visibles = useMemo(() => reels
    .filter(e => !classe || e.classe === classe)
    .filter(e => !recherche || `${e.nom} ${e.pere} ${e.telephone}`.toLowerCase().includes(recherche.toLowerCase())),
  [reels, classe, recherche]);

  // ── chiffres clés
  const notes = visibles.map(noteSur20).filter(Boolean) as { n: number; fini: boolean; faites: number }[];
  const moyenne = notes.length ? notes.reduce((s, x) => s + x.n, 0) / notes.length : null;
  const tempsMoyen = visibles.length ? visibles.reduce((s, e) => s + tempsCours(e), 0) / visibles.length : 0;

  // ── réussite par question (première réponse de chaque élève)
  const parQuestion = useMemo(() => ORDRE.map(id => {
    let n = 0, ob = 0, sur = 0;
    for (const e of visibles) {
      const q = (e.examens[e.examens.length - 1]?.questions || e.examen_en_cours.questions)[id];
      if (!q) continue;
      n += 1; ob += q.note || 0; sur += q.sur || 0;
    }
    return { id, n, taux: sur ? (100 * ob) / sur : null };
  }).filter(q => q.n > 0).sort((a, b) => (a.taux ?? 0) - (b.taux ?? 0)), [visibles]);

  // ── erreurs les plus fréquentes (éléments du barème perdus)
  const erreurs = useMemo(() => {
    const c = new Map<string, number>();
    for (const e of visibles) {
      const qs = e.examens[e.examens.length - 1]?.questions || e.examen_en_cours.questions;
      for (const [id, q] of Object.entries(qs)) for (const p of q.pertes || []) {
        const k = `${id} · ${p.split(' : ')[0]}`.slice(0, 90);
        c.set(k, (c.get(k) || 0) + 1);
      }
    }
    return [...c.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8);
  }, [visibles]);

  const exporter = () => {
    const lignes = [['Élève', 'Classe', 'Père', 'Téléphone', 'Inscrit le', 'Dernière activité', ...COURS.map(c => `${c.nom} (diapos vues)`),
      'Temps dans les cours (min)', 'Temps évaluation (min)', 'Questions rendues', 'Note /20', 'Évaluation terminée', 'Lacunes']];
    for (const e of visibles) {
      const n = noteSur20(e);
      lignes.push([e.nom, e.classe, e.pere, e.telephone, date(e.date), date(e.derniere), ...COURS.map(c => `${e.progression[c.id]?.vues || 0}/${e.progression[c.id]?.total || 0}`),
        String(Math.round(tempsCours(e) / 60)), String(Math.round((e.temps.examen || 0) / 60)), String(e.examen_en_cours.faites),
        n ? pts(n.n) : '', n?.fini ? 'oui' : 'non', e.lacunes.join(' | ')]);
    }
    const csv = '﻿' + lignes.map(l => l.map(x => `"${String(x).replace(/"/g, '""')}"`).join(';')).join('\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    a.download = `tronc-commun${classe ? `-${classe.replace(/\s/g, '')}` : ''}.csv`;
    a.click();
  };

  return (
    <div className="space-y-5 text-gray-900">
      {/* filtres, sur une ligne */}
      <div className="flex flex-wrap items-center gap-2">
        <h2 className="mr-auto text-lg font-semibold">Tronc Commun — suivi des élèves</h2>
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

      {/* chiffres clés */}
      <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
        <Tuile titre="Élèves" valeur={String(visibles.length)} sous={classe || 'toutes les classes'} />
        <Tuile titre="Ont commencé l’évaluation" valeur={String(notes.length)} sous={`sur ${visibles.length}`} />
        <Tuile titre="L’ont terminée" valeur={String(notes.filter(x => x.fini).length)} sous={`sur ${notes.length} commencées`} />
        <Tuile titre="Moyenne" valeur={moyenne == null ? '—' : `${pts(Math.round(moyenne * 10) / 10)} / 20`} sous="sur les questions rendues" />
        <Tuile titre="Temps moyen dans les cours" valeur={minutes(tempsMoyen)} sous="par élève" />
      </div>

      {!visibles.length && !chargement && <p className="text-sm text-gray-500">Aucun élève pour l’instant (lien : https://moalim.online/tronc-commun/).</p>}

      {!!visibles.length && (
        <div className="grid gap-4 lg:grid-cols-2">
          <Carte titre="Note de chaque élève (ramenée sur 20)" aide="Barre pleine : évaluation terminée ; barre claire : en cours (note sur les questions déjà rendues).">
            {visibles.map(e => ({ e, n: noteSur20(e) })).sort((a, b) => (b.n?.n ?? -1) - (a.n?.n ?? -1)).map(({ e, n }) => (
              <Barre key={e.id} libelle={e.nom} sous={e.classe} valeur={n?.n ?? 0} max={20} couleur={BLEU} clair={!n?.fini}
                texte={n ? `${pts(Math.round(n.n * 10) / 10)} / 20 · ${n.faites} q.` : 'pas commencée'} titre={`${e.nom} — ${n ? `${pts(n.n)} / 20, ${n.faites} questions rendues` : 'évaluation pas commencée'}`} />))}
          </Carte>
          <Carte titre="Réussite par question" aide="Les plus ratées en haut : c’est par là qu’il faut reprendre en classe.">
            {parQuestion.map(q => (
              <Barre key={q.id} libelle={`${q.id} · ${SUJETS[q.id]}`} valeur={q.taux ?? 0} max={100} couleur={BLEU}
                texte={`${Math.round(q.taux ?? 0)} % · ${q.n} élève${q.n > 1 ? 's' : ''}`} alerte={(q.taux ?? 0) < 50}
                titre={`${q.id} — ${SUJETS[q.id]} : ${Math.round(q.taux ?? 0)} % de réussite (${q.n} élèves)`} />))}
          </Carte>
          <Carte titre="Erreurs les plus fréquentes" aide="Élément du barème perdu, et combien d’élèves l’ont perdu.">
            {erreurs.length ? erreurs.map(([k, n]) => (
              <Barre key={k} libelle={k} valeur={n} max={Math.max(...erreurs.map(x => x[1]))} couleur={BLEU} texte={`${n} élève${n > 1 ? 's' : ''}`} titre={`${k} : ${n}`} />))
              : <p className="text-sm text-gray-500">Pas encore d’erreur relevée.</p>}
          </Carte>
          <Carte titre="Parcours dans les cours (diapositives vues)" aide="Un élève qui n’a pas suivi le cours ne peut pas passer l’évaluation (révision ou un cours à 80 %).">
            <div className="mb-2 flex flex-wrap gap-3 text-xs text-gray-600">{COURS.map(c => <span key={c.id} className="flex items-center gap-1"><span className="inline-block h-2.5 w-3 rounded-sm" style={{ background: c.c }} />{c.nom}</span>)}</div>
            {visibles.map(e => (
              <div key={e.id} className="mb-1.5 flex items-center gap-2 text-sm">
                <span className="w-36 shrink-0 truncate" title={e.nom}>{e.nom}</span>
                <span className="flex flex-1 flex-col gap-0.5">{COURS.map(c => {
                  const p = e.progression[c.id]; const pc = p?.total ? Math.min(100, (100 * p.vues) / p.total) : 0;
                  return <span key={c.id} className="h-1.5 w-full rounded-full bg-gray-100" title={`${c.nom} : ${p?.vues || 0} / ${p?.total || 0} diapos`}>
                    <span className="block h-full rounded-full" style={{ width: `${pc}%`, background: c.c }} /></span>;
                })}</span>
                <span className="w-16 shrink-0 text-right text-xs text-gray-500">{minutes(tempsCours(e))}</span>
              </div>))}
          </Carte>
        </div>)}

      {/* le détail par élève */}
      {!!visibles.length && (
        <div className="overflow-x-auto rounded-xl border bg-white">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-left text-gray-600">
              <tr><th className="px-3 py-2" /><th className="px-3 py-2">Élève</th><th className="px-3 py-2">Classe</th><th className="px-3 py-2">Évaluation</th>
                <th className="px-3 py-2">Temps (cours · évaluation)</th><th className="px-3 py-2">Père · téléphone</th><th className="px-3 py-2">Dernière activité</th></tr>
            </thead>
            <tbody>{visibles.map(e => {
              const n = noteSur20(e); const vu = ouvert === e.id;
              return (
                <Fragment key={e.id}>
                  <tr className="cursor-pointer border-t hover:bg-gray-50" onClick={() => setOuvert(vu ? null : e.id)}>
                    <td className="px-2 py-2 text-gray-400">{vu ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}</td>
                    <td className="px-3 py-2 font-medium">{e.nom}{e.test && <Etiquette>test</Etiquette>}{e.doublon_de && <Etiquette>doublon</Etiquette>}</td>
                    <td className="px-3 py-2 whitespace-nowrap">{e.classe}</td>
                    <td className="px-3 py-2 whitespace-nowrap">{n ? <><b>{pts(Math.round(n.n * 10) / 10)} / 20</b> <span className="text-xs text-gray-500">{n.fini ? 'terminée' : `${n.faites}/20 q.`}</span></> : <span className="text-gray-400">pas commencée</span>}</td>
                    <td className="px-3 py-2 whitespace-nowrap">{minutes(tempsCours(e))} · {minutes(e.temps.examen || 0)}</td>
                    <td className="px-3 py-2 whitespace-nowrap">{e.pere} · <a href={`tel:${e.telephone}`} className="text-blue-700" onClick={x => x.stopPropagation()}>{e.telephone}</a></td>
                    <td className="px-3 py-2 whitespace-nowrap text-gray-500">{date(e.derniere)}</td>
                  </tr>
                  {vu && <tr className="border-t bg-gray-50/60"><td /><td colSpan={6} className="px-3 py-3"><Detail e={e} /></td></tr>}
                </Fragment>);
            })}</tbody>
          </table>
        </div>)}
    </div>
  );
}


function Tuile({ titre, valeur, sous }: { titre: string; valeur: string; sous: string }) {
  return (
    <div className="rounded-xl border bg-white p-3">
      <p className="text-xs text-gray-500">{titre}</p>
      <p className="mt-0.5 text-2xl font-semibold">{valeur}</p>
      <p className="text-xs text-gray-500">{sous}</p>
    </div>);
}

function Carte({ titre, aide, children }: { titre: string; aide: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border bg-white p-4">
      <p className="font-semibold">{titre}</p>
      <p className="mb-3 text-xs text-gray-500">{aide}</p>
      <div className="max-h-[360px] overflow-y-auto pr-1">{children}</div>
    </div>);
}

/** une barre horizontale fine, extrémité arrondie, valeur écrite au bout ; la cible de survol est toute la ligne */
function Barre({ libelle, sous, valeur, max, couleur, texte, titre, clair, alerte }: {
  libelle: string; sous?: string; valeur: number; max: number; couleur: string; texte: string; titre: string; clair?: boolean; alerte?: boolean;
}) {
  const pc = max ? Math.max(0, Math.min(100, (100 * valeur) / max)) : 0;
  return (
    <div className="group mb-1.5 flex items-center gap-2 rounded px-1 text-sm hover:bg-gray-50" title={titre}>
      <span className="w-44 shrink-0 truncate" title={libelle}>{libelle}{sous && <span className="ml-1 text-xs text-gray-400">{sous}</span>}</span>
      <span className="h-3 flex-1 rounded-r bg-gray-100">
        <span className="block h-full rounded-r" style={{ width: `${pc}%`, background: couleur, opacity: clair ? 0.45 : 1 }} />
      </span>
      <span className="flex w-44 shrink-0 items-center justify-end gap-1.5 whitespace-nowrap text-right text-xs text-gray-700">
        {alerte && <span className="flex items-center gap-0.5 font-semibold" style={{ color: CRITIQUE }}><AlertTriangle className="h-3.5 w-3.5" />à revoir</span>}
        {texte}</span>
    </div>);
}

function Etiquette({ children }: { children: React.ReactNode }) {
  return <span className="ml-1.5 rounded bg-gray-200 px-1.5 py-0.5 text-[11px] font-normal text-gray-600">{children}</span>;
}

function Detail({ e }: { e: EleveTroncCommun }) {
  const qs = e.examens[e.examens.length - 1]?.questions || e.examen_en_cours.questions;
  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <div>
        <p className="mb-1 font-semibold text-gray-800">Évaluation, question par question</p>
        {Object.keys(qs).length ? (
          <table className="w-full text-xs"><tbody>{ORDRE.filter(id => qs[id]).map(id => {
            const q = qs[id]; const ok = (q.note || 0) >= (q.sur || 0);
            return (
              <tr key={id} className="border-t align-top">
                <td className="whitespace-nowrap py-1 pr-2 font-semibold">{id}</td>
                <td className={`py-1 pr-2 whitespace-nowrap font-semibold ${ok ? 'text-green-700' : (q.note || 0) > 0 ? 'text-amber-700' : 'text-red-700'}`}>{pts(q.note)} / {pts(q.sur)}</td>
                <td className="py-1 text-gray-700">{SUJETS[id]}{q.pertes?.length ? <span className="block text-red-700">− {q.pertes.join(' ; ')}</span> : null}</td>
              </tr>);
          })}</tbody></table>) : <p className="text-xs text-gray-500">Aucune question rendue.</p>}
      </div>
      <div>
        <p className="mb-1 font-semibold text-gray-800">Parcours et réponses dans les cours</p>
        <ul className="mb-3 space-y-0.5 text-xs text-gray-700">{COURS.map(c => <li key={c.id}>{c.nom} : {e.progression[c.id]?.vues || 0} / {e.progression[c.id]?.total || 0} diapos · {minutes(e.temps[c.id] || 0)}</li>)}
          <li>Réponses dans les cours : {e.reponses_cours.justes} justes, {e.reponses_cours.fausses} fausses</li></ul>
        <p className="mb-1 font-semibold text-gray-800">À retravailler</p>
        {e.lacunes.length ? <ul className="list-disc space-y-0.5 pl-5 text-xs text-gray-700">{e.lacunes.slice(0, 15).map((l, k) => <li key={k}>{l}</li>)}</ul>
          : <p className="text-xs text-gray-500">Rien de signalé.</p>}
        <p className="mt-2 text-xs text-gray-500">Inscrit le {date(e.date)}{e.classe_ecrite && e.classe_ecrite !== e.classe ? ` · classe écrite « ${e.classe_ecrite} »` : ''}</p>
      </div>
    </div>);
}
