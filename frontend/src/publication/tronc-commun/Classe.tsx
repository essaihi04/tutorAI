/**
 * Le mode classe (24 novembre 2026) : l'évaluation formative projetée en classe, question par question.
 *
 *   - `?classe`    l'écran du professeur (projeté) : code et QR code, « 12 / 25 élèves ont répondu » et un bouton par élève
 *                  (coloré selon sa réponse ; un clic ouvre sa réponse en grand, « Élève suivant → »), la question projetée,
 *                  le mur des réponses, « Montrer la correction », « 📊 Résultats de la classe » (scores, grille, rapport de
 *                  chaque élève), « ⬇ CSV », « 📱 Mon téléphone » (relier le téléphone du prof) ;
 *   - `?c=<code>`  le téléphone : « Je suis un élève » (nom, prénom, classe, une fois) ou « Je suis le professeur » (le
 *                  code de son écran ; il saisit alors les feuilles des élèves sans téléphone, l'un après l'autre) ; la
 *                  question projetée (suit le prof), « 📷 Photographier » ou « ⌨ Écrire », la note, le mur anonyme.
 *
 * Rien d'enregistré (25/11/2026) : ni fiche, ni suivi, ni compte ; les noms et les réponses vivent en mémoire sur le
 * serveur le temps de la séance (`/api/v1/public/classe`) et disparaissent ; le prof peut télécharger un CSV. La correction reprend celle de l'évaluation (`Examen.tsx`) : QCM, vrai/faux et valeurs notés dans le
 * navigateur, rédactions par le tuteur sur le barème ; triangle et histogramme : la photo du tracé part au mur
 * « à regarder ensemble ».
 */
import { useEffect, useRef, useState } from 'react';
import { COULEUR_VERDICT, MOT_VERDICT, nomComplet, nomCourt, RapportEleve, ResultatsClasse, telechargerCsv, type EtatSeance, type Participant, type ReponseMur, type VerdictMur } from './ResultatsClasse';
import { Formule } from '../../components/course/Formule';
import { pts } from '../../components/exercice/types';
import { choixDuTexte, lienComplet, lienCourt, octets, QrCode, reduireImage } from '../../components/course/photoTelephone';
import { Choix, configExamen, corpsCorrection, DonneesPartie, etatDeCorrection, jugerValeur, noterChoix, Verdict, type CorrectionTuteur, type Etat } from './Examen';
import { Histogramme, histoVide, Triangle } from './Traces';
import type { PartieExamen, QuestionExamen } from './sujet';

const API = '/api/v1/public/classe';
const SUJET = "'Times New Roman', Georgia, serif";
const CRAIE = "'Patrick Hand', 'Caveat', cursive";
const PAGE = () => `${location.origin}${location.pathname}`;


async function appel<T>(chemin: string, init: RequestInit = {}, entetes: Record<string, string> = {}): Promise<T> {
  const r = await fetch(`${API}${chemin}`, { ...init, headers: { 'Content-Type': 'application/json', ...entetes } });
  if (!r.ok) {
    const d = await r.json().then((x: { detail?: unknown }) => (typeof x?.detail === 'string' ? x.detail : '')).catch(() => '');
    throw Object.assign(new Error(d || String(r.status)), { status: r.status });
  }
  return r.json() as Promise<T>;
}

/** L'état de la séance, interrogé toutes les 2,5 s (rien n'est renvoyé si rien n'a changé). */
function useSeance(code: string, entetes: Record<string, string> = {}) {
  const cle = JSON.stringify(entetes);
  const [etat, setEtat] = useState<EtatSeance | null>(null);
  const [perdue, setPerdue] = useState(false);
  const version = useRef(0);
  const [tick, setTick] = useState(0);
  useEffect(() => {
    if (!code) return;
    let fini = false;
    version.current = 0;
    const lire = async () => {
      try {
        const d = await appel<EtatSeance & { inchange?: boolean; prof?: boolean }>(`/${code}?v=${version.current}`, {}, JSON.parse(cle));
        if (fini || d.inchange) return;
        version.current = d.version;
        setEtat(d); setPerdue(false);
      } catch (e) {
        if (!fini && (e as { status?: number }).status === 404) setPerdue(true);
      }
    };
    void lire();
    const t = window.setInterval(() => { void lire(); }, 2500);
    return () => { fini = true; window.clearInterval(t); };
  }, [code, cle, tick]);
  /** relire tout de suite (après une action) */
  const relire = () => setTick(t => t + 1);
  return { etat, perdue, relire };
}

const trouver = (id: string) => configExamen().questions.find(x => x.q.id === id);
const lettre = (k: number) => String.fromCharCode(65 + k);

function compter(rs: ReponseMur[]) {
  return { recues: rs.length, justes: rs.filter(r => r.verdict === 'juste').length, partielles: rs.filter(r => r.verdict === 'partiel').length,
    fausses: rs.filter(r => r.verdict === 'faux').length, regarder: rs.filter(r => r.verdict === 'regarder' || r.verdict === 'nonjuge').length };
}

const COULEURS: Record<VerdictMur, [string, string]> = {
  juste: ['✔ Juste', 'border-emerald-600 bg-emerald-50 text-emerald-900'], partiel: ['◐ En partie', 'border-amber-500 bg-amber-50 text-amber-900'],
  faux: ['✘ Faux', 'border-rose-600 bg-rose-50 text-rose-900'], nonjuge: ['? À regarder', 'border-slate-400 bg-slate-50 text-slate-800'],
  regarder: ['👀 À regarder ensemble', 'border-sky-600 bg-sky-50 text-sky-900'],
};

/** Une réponse du mur : miniature (cliquable), texte lu, note, ce qui est juste, ce qui est perdu. */
function CarteReponse({ r, code, grand = false, onImage, onRetirer }: { r: ReponseMur; code: string; grand?: boolean; onImage: (src: string) => void; onRetirer?: () => void }) {
  const [titre, couleur] = COULEURS[r.verdict];
  const src = `${API}/${code}/image/${r.id}`;
  const t = grand ? 'text-[clamp(15px,1.25vw,22px)]' : 'text-[15px]';
  return (
    <div className={`flex flex-col rounded-xl border-2 p-2 ${couleur}`} style={{ fontFamily: 'system-ui, sans-serif' }}>
      <div className="flex items-center gap-2">
        <span className={`font-bold ${grand ? 'text-[clamp(16px,1.4vw,24px)]' : 'text-[15px]'}`}>Réponse {r.numero}{r.mien ? ' (toi)' : ''}</span>
        <span className="flex-1 text-sm">{titre}</span>
        {r.note != null && <span className={`rounded-md bg-white px-2 font-bold ${grand ? 'text-[clamp(18px,1.6vw,28px)]' : 'text-lg'}`}>{pts(r.note)} / {pts(r.sur)}</span>}
        {onRetirer && <button onClick={onRetirer} className="rounded px-1 text-xs text-slate-500 hover:bg-white" title="Retirer du mur">✕</button>}
      </div>
      <div className="mt-1 flex gap-2">
        {r.image && <button onClick={() => onImage(src)} className="shrink-0" title="Voir la photo en grand">
          <img src={src} alt={`Photo de la réponse ${r.numero}`} loading="lazy" className={`${grand ? 'h-28 w-24' : 'h-20 w-16'} rounded border border-black/20 bg-white object-cover`} /></button>}
        <div className="min-w-0 flex-1">
          {r.texte && <p className={`line-clamp-6 whitespace-pre-wrap text-black ${t}`} style={{ fontFamily: CRAIE }}>{r.texte}</p>}
        </div>
      </div>
      {!!r.bien.length && <ul className={`mt-1 ${grand ? 'text-[clamp(13px,1.05vw,18px)]' : 'text-[13px]'} text-emerald-800`}>{r.bien.map((b, k) => <li key={k}>✓ <Formule t={b} /></li>)}</ul>}
      {!!r.pertes.length && <ul className={`mt-1 ${grand ? 'text-[clamp(13px,1.05vw,18px)]' : 'text-[13px]'} text-rose-700`}>{r.pertes.map((b, k) => <li key={k}>✘ <Formule t={b} /></li>)}</ul>}
      {r.retour && <p className={`mt-1 ${grand ? 'text-[clamp(13px,1vw,17px)]' : 'text-[13px]'} italic text-slate-700`}><Formule t={r.retour} /></p>}
    </div>
  );
}

function Loupe({ src, onFermer }: { src: string; onFermer: () => void }) {
  return (
    <div className="fixed inset-0 z-[1000] grid place-items-center bg-black/85 p-2" onClick={onFermer} role="dialog" aria-label="Photo en grand">
      <img src={src} alt="Photo de la réponse" className="max-h-[94dvh] max-w-[96vw] rounded-lg bg-white object-contain" />
      <button className="absolute right-3 top-3 rounded-full bg-white px-3 py-1 text-lg font-bold text-black">✕</button>
    </div>
  );
}

/** L'énoncé de la question : partie, données, question, propositions ; `correction` : la correction du sujet. */
function Enonce({ p, q, grand, correction, donnees = true }: { p: PartieExamen; q: QuestionExamen; grand: boolean; correction: boolean; donnees?: boolean }) {
  const t = grand ? 'text-[clamp(18px,1.7vw,30px)]' : 'text-[17px]';
  const st = grand ? 'text-[clamp(15px,1.3vw,22px)]' : 'text-[15px]';
  return (
    <div style={{ fontFamily: SUJET }}>
      <h2 className={`font-bold underline underline-offset-4 ${grand ? 'text-[clamp(17px,1.5vw,26px)]' : 'text-[16px]'}`}>{p.titre}</h2>
      {donnees && <DonneesPartie p={p} grand={grand} />}
      <p className={`mt-3 font-semibold ${t}`}><span className="rounded bg-black px-2 text-white">{q.id}</span> <Formule t={q.texte} />
        <span className="ml-2 whitespace-nowrap rounded border border-black px-1.5 text-[0.75em] font-normal" style={{ fontFamily: 'system-ui, sans-serif' }}>{pts(q.points)} pt</span></p>
      {(q.genre === 'qcm' || q.genre === 'vf') && (
        <ol className={`mt-2 space-y-2 ${st}`}>
          {q.items.map((it, k) => {
            const options = q.genre === 'qcm' ? (it as { choix: string[] }).choix : ['Vrai', 'Faux'];
            const bonne = q.genre === 'qcm' ? (it as { bonne: number }).bonne : (it as { vrai: boolean }).vrai ? 0 : 1;
            return (
              <li key={k}>
                {q.items.length > 1 && <b>{String.fromCharCode(97 + k)}) </b>}<Formule t={it.texte} />
                <div className="mt-0.5 flex flex-wrap gap-x-4 gap-y-0.5 pl-4" style={{ fontFamily: 'system-ui, sans-serif' }}>
                  {options.map((o, m) => <span key={m} className={correction && m === bonne ? 'rounded bg-emerald-100 px-1 font-bold text-emerald-900' : ''}>{q.genre === 'qcm' ? `${lettre(m)}. ` : ''}{o}</span>)}
                </div>
                {correction && <p className="pl-4 text-emerald-900" style={{ fontFamily: CRAIE }}>✔ <Formule t={it.explication} /></p>}
              </li>);
          })}
        </ol>)}
      {q.genre === 'histogramme' && (
        <p className={`mt-2 border border-black p-2 ${st}`} style={{ fontFamily: 'system-ui, sans-serif' }}><b>Espèces et indice :</b> {q.especes.map(([e, i]) => `${e} (${i})`).join(' · ')}</p>)}
      {correction && 'correction' in q && (
        <div className="mt-3 border-2 border-rose-700 bg-white p-2">
          <p className="font-bold text-rose-800" style={{ fontFamily: 'system-ui, sans-serif' }}>✍️ Correction</p>
          {q.correction.map((l, k) => <p key={k} className={`${grand ? 'text-[clamp(17px,1.5vw,26px)]' : 'text-[18px]'} text-rose-900`} style={{ fontFamily: CRAIE }}><Formule t={l} /></p>)}
          {q.genre === 'triangle' && <div className="mx-auto mt-2 max-w-[520px]"><Triangle sol={q.sol} actif={false} correction lignes={{}} /></div>}
          {q.genre === 'histogramme' && <div className="mt-2"><Histogramme comptes={q.comptes} actif={false} correction h={histoVide()} /></div>}
        </div>)}
    </div>
  );
}

// ── L'écran du professeur ─────────────────────────────────────────────────────────────────────────────────────────────

const MEMO_PROF = 'classe-prof';
type Prof = { code: string; cle: string };
const lireProf = (): Prof | null => { try { return JSON.parse(sessionStorage.getItem(MEMO_PROF) || 'null'); } catch { return null; } };

export function ProfClasse() {
  const [prof, setProf] = useState<Prof | null>(() => lireProf());
  const [erreur, setErreur] = useState('');
  const garder = (p: Prof | null) => { setProf(p); try { if (p) sessionStorage.setItem(MEMO_PROF, JSON.stringify(p)); else sessionStorage.removeItem(MEMO_PROF); } catch { /* rien */ } };
  const commencer = async () => {
    setErreur('');
    try {
      const d = await appel<{ code: string; cle_prof: string }>('', { method: 'POST', body: JSON.stringify({ sujet: 'tc' }) });
      await appel(`/${d.code}/question`, { method: 'POST', body: JSON.stringify({ question: configExamen().questions[0].q.id }) }, { 'X-Prof': d.cle_prof });
      garder({ code: d.code, cle: d.cle_prof });
    } catch (e) { setErreur((e as Error).message.replace(/^\d+$/, 'Le serveur ne répond pas : réessaie.')); }
  };
  if (!prof) return (
    <div className="min-h-[100dvh] bg-[#0f1a14] px-4 py-6 text-white sm:px-8" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <div className="mx-auto max-w-3xl">
        <a href="./" className="text-sm text-emerald-200/80 underline">← Tronc Commun</a>
        <h1 className="mt-2 text-3xl font-bold">Mode classe — évaluation au tableau</h1>
        <p className="mt-2 text-lg text-white/80">{configExamen().sujet.titre}</p>
        <ol className="mt-4 list-decimal space-y-1.5 pl-6 text-[17px] text-white/85">
          <li>Projette cet écran : la question s’affiche en grand.</li>
          <li>Les élèves répondent sur leur feuille.</li>
          <li>Chaque élève vise le QR code une seule fois avec son téléphone et écrit son nom ; puis, à chaque question, il photographie sa feuille ou écrit sa réponse.</li>
          <li>Les élèves sans téléphone : avec ton téléphone (« 📱 Mon téléphone »), tu photographies leurs feuilles, l’une après l’autre.</li>
          <li>Chaque réponse est lue et corrigée (note, éléments du barème perdus) ; tu vois qui a répondu, la réponse de chacun et les résultats de la classe.</li>
          <li>« Montrer la correction » : la correction s’affiche au tableau et sur les téléphones.</li>
        </ol>
        <p className="mt-3 text-[15px] text-white/60">Rien n’est enregistré : les noms, les photos et les notes s’effacent quand tu termines la séance (ou après 4 h sans activité). Tu peux télécharger les résultats (CSV) avant.</p>
        <button onClick={() => void commencer()} className="mt-5 rounded-xl bg-amber-400 px-6 py-3 text-xl font-bold text-black hover:bg-amber-300">Commencer une séance</button>
        {erreur && <p className="mt-3 text-rose-300">{erreur}</p>}
      </div>
    </div>
  );
  return <SeanceProf prof={prof} onFin={() => garder(null)} />;
}

function SeanceProf({ prof, onFin }: { prof: Prof; onFin: () => void }) {
  const X = { 'X-Prof': prof.cle };
  const { etat, perdue, relire } = useSeance(prof.code, X);
  const [loupe, setLoupe] = useState('');
  // au début de la séance, le QR s'affiche en grand : toute la classe le vise depuis sa place (une seule fois)
  const [qrGrand, setQrGrand] = useState(true);
  const [donnees, setDonnees] = useState(true);
  const [vue, setVue] = useState<'question' | 'resultats'>('question');
  /** la réponse d'un élève à la question projetée, ouverte en grand */
  const [fiche, setFiche] = useState<string | null>(null);
  /** le petit rapport d'un élève */
  const [rapport, setRapport] = useState<string | null>(null);
  const [jeton, setJeton] = useState<{ jeton: string; fin: number } | null>(null);
  const qs = configExamen().questions;
  const k = Math.max(0, qs.findIndex(x => x.q.id === etat?.question));
  const { p, q } = qs[k];
  useEffect(() => { if (perdue) onFin(); }, [perdue]);
  useEffect(() => { if (!jeton) return; const t = window.setTimeout(() => setJeton(null), Math.max(0, jeton.fin - Date.now())); return () => window.clearTimeout(t); }, [jeton]);
  const aller = async (id: string) => { await appel(`/${prof.code}/question`, { method: 'POST', body: JSON.stringify({ question: id }) }, X).catch(() => {}); relire(); };
  const montrer = async (m: boolean) => { await appel(`/${prof.code}/correction`, { method: 'POST', body: JSON.stringify({ montrer: m }) }, X).catch(() => {}); relire(); };
  const terminer = async () => {
    if (!window.confirm('Terminer la séance ? Tout sera effacé (noms, réponses, notes). Télécharge d’abord les résultats (CSV) si tu veux les garder.')) return;
    await appel(`/${prof.code}`, { method: 'DELETE' }, X).catch(() => {});
    onFin();
  };
  const relierTelephone = async () => {
    try { const d = await appel<{ jeton: string; expiration_s: number }>(`/${prof.code}/jeton-prof`, { method: 'POST' }, X); setJeton({ jeton: d.jeton, fin: Date.now() + d.expiration_s * 1000 }); }
    catch { /* séance perdue : le sondage le dira */ }
  };
  const rs = etat?.reponses || [];
  const n = compter(rs);
  const participants = etat?.participants || [];
  const parEleve: Record<string, ReponseMur> = {};
  for (const r of rs) if (r.eleve) parEleve[r.eleve] = r;
  const ontRepondu = participants.filter(x => parEleve[x.id]).length;
  const lien = lienComplet(prof.code, PAGE(), 'c');
  const BTN = 'rounded-lg border border-white/30 px-3 py-1.5 text-[clamp(14px,1.1vw,18px)] hover:bg-white/10 disabled:opacity-30';

  return (
    <div className="flex min-h-[100dvh] flex-col bg-[#0f1a14] text-white lg:h-[100dvh]" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <header className="flex shrink-0 flex-wrap items-center gap-x-4 gap-y-2 border-b border-white/15 px-3 py-2">
        <button onClick={() => setQrGrand(true)} title="QR code en grand"><QrCode lien={lien} className="w-[clamp(64px,7vw,120px)] rounded" /></button>
        <div className="min-w-0">
          <p className="text-[clamp(14px,1.1vw,20px)] text-white/70">Sur ton téléphone : <b className="font-mono text-white">{lienCourt(prof.code, PAGE(), 'c')}</b></p>
          <p className="font-mono text-[clamp(30px,3.6vw,64px)] font-bold leading-none tracking-[0.2em] text-amber-300">{prof.code}</p>
        </div>
        <div className="ml-auto flex flex-wrap items-center gap-2">
          {vue === 'question' && (<>
            <button className={BTN} disabled={k === 0} onClick={() => void aller(qs[k - 1].q.id)}>← Précédente</button>
            <select value={q.id} onChange={e => void aller(e.target.value)} className="rounded-lg border border-white/30 bg-[#12301f] px-2 py-1.5 text-[clamp(14px,1.1vw,18px)]">
              {qs.map(x => <option key={x.q.id} value={x.q.id}>Question {x.q.id}{etat?.par_question[x.q.id] ? ` · ${etat.par_question[x.q.id]} rép.` : ''}</option>)}
            </select>
            <button className={BTN} disabled={k === qs.length - 1} onClick={() => void aller(qs[k + 1].q.id)}>Suivante →</button>
            <button onClick={() => void montrer(!etat?.correction)} className={`rounded-lg px-3 py-1.5 text-[clamp(14px,1.1vw,18px)] font-semibold ${etat?.correction ? 'bg-rose-200 text-rose-950' : 'bg-amber-400 text-black'}`}>
              {etat?.correction ? 'Cacher la correction' : 'Montrer la correction'}</button>
          </>)}
          <button onClick={() => setVue(v => (v === 'question' ? 'resultats' : 'question'))} className="rounded-lg bg-[#2a78d6] px-3 py-1.5 text-[clamp(14px,1.1vw,18px)] font-semibold">
            {vue === 'question' ? '📊 Résultats de la classe' : '← La question'}</button>
          <button onClick={() => etat && telechargerCsv(etat)} disabled={!participants.length} className={BTN} title="Fabriqué dans ce navigateur : rien n’est envoyé">⬇ CSV</button>
          <button onClick={() => void relierTelephone()} className={BTN} title="Saisir les réponses des élèves sans téléphone">📱 Mon téléphone</button>
          <button onClick={() => void terminer()} className="rounded-lg border border-rose-300/60 px-3 py-1.5 text-[clamp(13px,1vw,16px)] text-rose-200 hover:bg-rose-500/20">Terminer</button>
        </div>
      </header>
      <p className="shrink-0 bg-amber-300/15 px-3 py-0.5 text-[13px] text-amber-100">Rien n’est enregistré : tout s’efface à la fin de la séance. Télécharge les résultats (⬇ CSV) avant de terminer.</p>

      {vue === 'resultats' && etat ? (
        <div className="min-h-0 flex-1 overflow-y-auto bg-slate-100 p-3 text-slate-900"><ResultatsClasse etat={etat} onEleve={setRapport} /></div>
      ) : (<>
        <div className="flex shrink-0 flex-wrap items-center gap-1.5 px-3 pt-2">
          <p className="mr-2 text-[clamp(16px,1.5vw,26px)]"><b className="text-amber-300">{ontRepondu} / {participants.length}</b> élève{participants.length > 1 ? 's ont' : ' a'} répondu</p>
          {participants.map(x => {
            const r = parEleve[x.id];
            const v = r ? r.verdict : 'rien';
            return <button key={x.id} onClick={() => setFiche(x.id)} title={`${nomComplet(x)} : ${MOT_VERDICT[v]}${r?.note != null ? ` (${pts(r.note)} / ${pts(r.sur)})` : ''}`}
              className="rounded-full px-3 py-1 text-[clamp(13px,1.1vw,18px)] font-semibold" style={{ background: COULEUR_VERDICT[v], color: v === 'rien' ? '#333' : v === 'nonjuge' || v === 'regarder' ? '#0b2a4a' : '#fff' }}>
              {nomCourt(x, participants)}</button>;
          })}
          {!participants.length && <span className="text-white/60">Les noms des élèves apparaîtront ici quand ils auront visé le QR code.</span>}
        </div>
        <div className="grid min-h-0 flex-1 gap-3 p-3 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,1fr)]">
          <section className="min-h-0 overflow-y-auto rounded-xl bg-white p-4 text-black shadow-md">
            <div className="mb-1 flex items-center gap-2 text-sm text-slate-600" style={{ fontFamily: 'system-ui, sans-serif' }}>
              <span>Question {k + 1} / {qs.length}</span>
              {(p.intro || p.tableau || p.donnees?.length) && <button onClick={() => setDonnees(d => !d)} className="ml-auto rounded border border-slate-400 px-2 text-xs">{donnees ? 'Cacher les données' : 'Montrer les données'}</button>}
            </div>
            <Enonce p={p} q={q} grand correction={!!etat?.correction} donnees={donnees} />
          </section>
          <section className="flex min-h-0 flex-col">
            <div className="flex flex-wrap gap-2 text-[clamp(14px,1.2vw,22px)]">
              <span className="rounded-lg bg-white/10 px-3 py-1">Toutes les réponses : <b>{n.recues}</b></span>
              <span className="rounded-lg bg-emerald-700/70 px-3 py-1">✔ <b>{n.justes}</b></span>
              <span className="rounded-lg bg-amber-600/70 px-3 py-1">◐ <b>{n.partielles}</b></span>
              <span className="rounded-lg bg-rose-700/70 px-3 py-1">✘ <b>{n.fausses}</b></span>
              {!!n.regarder && <span className="rounded-lg bg-sky-700/70 px-3 py-1">👀 <b>{n.regarder}</b></span>}
            </div>
            <div className="mt-2 min-h-0 flex-1 overflow-y-auto">
              {rs.length ? (
                <div className="grid gap-2 [grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr))]">
                  {rs.map(r => <CarteReponse key={r.id} r={r} code={prof.code} grand onImage={setLoupe}
                    onRetirer={() => { if (window.confirm(`Retirer la réponse ${r.numero} du mur ?`)) void appel(`/${prof.code}/reponse/${r.id}`, { method: 'DELETE' }, X).then(relire).catch(() => {}); }} />)}
                </div>
              ) : <p className="mt-6 text-center text-[clamp(16px,1.4vw,24px)] text-white/60">Les réponses apparaîtront ici (le mur ne montre pas les noms).</p>}
            </div>
          </section>
        </div>
      </>)}

      {fiche && etat && <FicheEleve etat={etat} q={q} id={fiche} code={prof.code} onAutre={setFiche} onFermer={() => setFiche(null)} onImage={setLoupe} onRapport={id => { setFiche(null); setRapport(id); }} />}
      {rapport && etat && <RapportEleve etat={etat} id={rapport} onAutre={setRapport} onFermer={() => setRapport(null)} />}
      {loupe && <Loupe src={loupe} onFermer={() => setLoupe('')} />}
      {jeton && (
        <div className="fixed inset-0 z-[1000] flex flex-col items-center justify-center gap-3 bg-white p-4 text-black" role="dialog" aria-label="Relier le téléphone du prof">
          <p className="text-[clamp(18px,2vw,30px)] font-bold">📱 Téléphone du professeur</p>
          <QrCode lien={`${lien}&prof=${jeton.jeton}`} className="w-[min(46vh,70vw)]" />
          <p className="text-[clamp(15px,1.4vw,22px)]">Vise ce QR avec TON téléphone, ou choisis « Je suis le professeur » et tape :</p>
          <p className="font-mono text-[clamp(36px,5vw,72px)] font-bold tracking-[0.3em]">{jeton.jeton}</p>
          <p className="text-sm text-slate-600">Valable 2 minutes, une seule fois. Tu pourras y saisir les réponses des élèves sans téléphone.</p>
          <button onClick={() => setJeton(null)} className="rounded-lg border border-slate-400 px-4 py-2">Fermer</button>
        </div>)}
      {qrGrand && (
        <div className="fixed inset-0 z-[1000] flex flex-col items-center justify-center gap-4 bg-white p-4 text-black" onClick={() => setQrGrand(false)} role="dialog" aria-label="QR code en grand">
          <QrCode lien={lien} className="w-[min(62vh,80vw)]" />
          <p className="text-[clamp(18px,2vw,32px)] font-semibold">Visez ce QR code avec votre téléphone, une seule fois, puis écrivez votre nom</p>
          <p className="font-mono text-[clamp(20px,3vw,44px)]">{lienCourt(prof.code, PAGE(), 'c')} · code <b>{prof.code}</b></p>
          <p className="text-sm text-slate-500">Touchez l’écran pour afficher la question (le QR reste en haut à gauche ; touchez-le pour le revoir en grand)</p>
        </div>)}
    </div>
  );
}

/** La réponse d'un élève à la question projetée, en grand ; « Élève suivant → » jusqu'au dernier. */
function FicheEleve({ etat, q, id, code, onAutre, onFermer, onImage, onRapport }: { etat: EtatSeance; q: QuestionExamen; id: string; code: string;
  onAutre: (id: string) => void; onFermer: () => void; onImage: (src: string) => void; onRapport: (id: string) => void }) {
  const ps = etat.participants;
  const k = ps.findIndex(x => x.id === id);
  const el = ps[k];
  if (!el) return null;
  const r = etat.reponses.find(x => x.eleve === id);
  const v = r ? r.verdict : 'rien';
  const src = r?.image ? `${API}/${code}/image/${r.id}` : '';
  const bouton = 'rounded-lg border border-slate-400 px-3 py-1.5 text-[clamp(14px,1.1vw,18px)] hover:bg-slate-100 disabled:opacity-30';
  return (
    <div className="fixed inset-0 z-[900] grid place-items-center bg-black/60 p-2" onClick={onFermer} role="dialog" aria-label={`Réponse de ${nomComplet(el)}`}>
      <div className="flex max-h-[96dvh] w-[min(97vw,1200px)] flex-col overflow-hidden rounded-2xl bg-white text-slate-900 shadow-2xl" onClick={ev => ev.stopPropagation()} style={{ fontFamily: 'system-ui, sans-serif' }}>
        <div className="flex flex-wrap items-center gap-2 border-b p-3">
          <h3 className="text-[clamp(20px,2vw,32px)] font-bold">{nomComplet(el)}</h3>
          <span className="text-slate-500">question {q.id} · élève {k + 1} / {ps.length}</span>
          {r?.note != null && <span className="rounded-lg px-3 py-0.5 text-[clamp(18px,1.8vw,30px)] font-bold text-white" style={{ background: COULEUR_VERDICT[v] }}>{pts(r.note)} / {pts(r.sur)}</span>}
          {r && r.note == null && <span className="rounded-lg px-3 py-0.5 font-semibold" style={{ background: COULEUR_VERDICT[v] }}>{MOT_VERDICT[v]}</span>}
          <span className="ml-auto flex flex-wrap gap-2">
            <button className={bouton} onClick={() => onRapport(id)}>Son rapport</button>
            <button className={bouton} disabled={k <= 0} onClick={() => onAutre(ps[k - 1].id)}>← Précédent</button>
            <button className={`${bouton} bg-black font-semibold text-white hover:bg-slate-800`} disabled={k >= ps.length - 1} onClick={() => onAutre(ps[k + 1].id)}>Élève suivant →</button>
            <button className={bouton} onClick={onFermer} aria-label="Fermer">✕</button>
          </span>
        </div>
        {r ? (
          <div className="grid min-h-0 flex-1 gap-3 overflow-y-auto p-3 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
            {src ? <button onClick={() => onImage(src)} className="min-h-0"><img src={src} alt={`Feuille de ${nomComplet(el)}`} className="max-h-[70vh] w-full rounded-lg border object-contain" /></button>
              : <p className="self-start rounded-lg bg-slate-100 p-3 text-slate-600">Réponse écrite au téléphone (pas de photo).</p>}
            <div className="min-w-0 text-[clamp(16px,1.3vw,22px)]">
              {r.texte && <p className="whitespace-pre-wrap rounded-lg bg-slate-50 p-2" style={{ fontFamily: CRAIE }}>{r.texte}</p>}
              {!!r.bien.length && <><p className="mt-2 font-bold text-emerald-800">✔ Ce qui est juste</p><ul className="text-emerald-900">{r.bien.map((b, j) => <li key={j}>✓ <Formule t={b} /></li>)}</ul></>}
              {!!r.pertes.length && <><p className="mt-2 font-bold" style={{ color: '#d03b3b' }}>✘ Éléments du barème perdus</p><ul style={{ color: '#b02a2a' }}>{r.pertes.map((b, j) => <li key={j}>✘ <Formule t={b} /></li>)}</ul></>}
              {r.retour && <p className="mt-2 italic text-slate-700"><Formule t={r.retour} /></p>}
            </div>
          </div>
        ) : <p className="p-8 text-center text-[clamp(18px,1.6vw,26px)] text-slate-500">Pas encore de réponse à la question {q.id}.</p>}
      </div>
    </div>
  );
}

// ── Le téléphone ──────────────────────────────────────────────────────────────────────────────────────────────────────

const MEMO_TEL = 'classe-telephone';
const nouvelId = () => crypto.randomUUID?.() || `t-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 12)}`;
function idTelephone() {
  try {
    let t = sessionStorage.getItem(MEMO_TEL) || '';
    if (!t) { t = nouvelId(); sessionStorage.setItem(MEMO_TEL, t); }
    return t;
  } catch { return nouvelId(); }
}
/** la clé du téléphone du prof pour cette séance (sessionStorage) */
const cleProfTel = (code: string) => { try { return sessionStorage.getItem(`classe-prof-tel-${code}`) || ''; } catch { return ''; } };
const garderCleProfTel = (code: string, cle: string) => { try { if (cle) sessionStorage.setItem(`classe-prof-tel-${code}`, cle); else sessionStorage.removeItem(`classe-prof-tel-${code}`); } catch { /* rien */ } };

type Phase = 'vide' | 'lecture' | 'relire' | 'correction' | 'auto' | 'envoi' | 'envoye';
type EtatTel = { phase: Phase; texte: string; choix?: (number | boolean | null)[]; mini?: string; resultat?: Etat & { verdictMur?: VerdictMur }; erreur?: string };

function detailsEnListes(e: Etat) {
  const d = e.details || [];
  return {
    pertes: d.filter(x => x.obtenu < x.sur).map(x => `${x.element.replace(/\s*:\s*$/, '')} : −${pts(x.sur - x.obtenu)}${x.perte ? ` (${x.perte})` : ''}`),
    bien: d.filter(x => x.obtenu >= x.sur && x.sur > 0).map(x => x.element.replace(/\s*:\s*$/, '')),
  };
}

const CHAMP = 'w-full rounded-xl border border-white/30 bg-white/10 px-3 py-2 text-lg text-white outline-none focus:border-emerald-300';

/** Nom, prénom, classe : une seule fois, au début (l'élève), ou pour un élève sans téléphone (le prof). */
function FormNom({ onValider, libelle, attente }: { onValider: (d: { nom: string; prenom: string; classe: string }) => void; libelle: string; attente?: boolean }) {
  const [nom, setNom] = useState(''); const [prenom, setPrenom] = useState(''); const [classe, setClasse] = useState('');
  return (
    <form className="space-y-2" onSubmit={e => { e.preventDefault(); if (nom.trim() && prenom.trim()) onValider({ nom: nom.trim(), prenom: prenom.trim(), classe: classe.trim() }); }}>
      <div className="grid gap-2 sm:grid-cols-2">
        <input value={prenom} onChange={e => setPrenom(e.target.value.slice(0, 60))} placeholder="Prénom" autoComplete="given-name" className={CHAMP} aria-label="Prénom" />
        <input value={nom} onChange={e => setNom(e.target.value.slice(0, 60))} placeholder="Nom" autoComplete="family-name" className={CHAMP} aria-label="Nom" />
      </div>
      <input value={classe} onChange={e => setClasse(e.target.value.slice(0, 20))} placeholder="Classe (facultatif, ex. 12)" className={CHAMP} aria-label="Classe" />
      <button disabled={!nom.trim() || !prenom.trim() || attente} className="w-full rounded-xl bg-amber-400 px-4 py-2.5 text-lg font-bold text-black disabled:opacity-40">{libelle}</button>
    </form>
  );
}

export function TelephoneClasse({ code: initial }: { code: string }) {
  const [code, setCode] = useState(/^\d{4}$/.test(initial) ? initial : '');
  const [saisie, setSaisie] = useState('');
  const [tel] = useState(() => idTelephone());
  const [cleProf, setCleProf] = useState(() => (code ? cleProfTel(code) : ''));
  const entetes: Record<string, string> = { 'X-Telephone': tel, ...(cleProf ? { 'X-Prof-Tel': cleProf } : {}) };
  const { etat, perdue, relire } = useSeance(code, entetes);
  const [etats, setEtats] = useState<Record<string, EtatTel>>({});
  const [loupe, setLoupe] = useState('');
  const [voirDonnees, setVoirDonnees] = useState(false);
  const [role, setRole] = useState<'' | 'eleve' | 'prof'>('');
  const [jetonSaisi, setJetonSaisi] = useState('');
  const [erreur, setErreur] = useState('');
  const [attente, setAttente] = useState(false);
  /** le prof : l'élève dont il saisit la feuille ('' : la liste) */
  const [cible, setCible] = useState('');
  const [nouveau, setNouveau] = useState(false);
  const [envoye, setEnvoye] = useState('');

  // le QR du téléphone du prof (?c=…&prof=1234) : la clé est demandée tout de suite, puis le jeton quitte l'adresse
  const relierProf = async (jeton: string) => {
    setErreur(''); setAttente(true);
    try {
      const d = await appel<{ cle: string }>(`/${code}/prof-telephone`, { method: 'POST', body: JSON.stringify({ jeton }) });
      garderCleProfTel(code, d.cle); setCleProf(d.cle);
    } catch (e) { setErreur((e as Error).message.replace(/^\d+$/, 'Le code du prof n’est pas passé : réessaie.')); }
    finally { setAttente(false); }
  };
  useEffect(() => {
    const j = new URLSearchParams(location.search).get('prof');
    if (code && j && /^\d{4}$/.test(j)) { history.replaceState(null, '', `?c=${code}`); void relierProf(j); }
  }, []);
  // une clé de prof refusée (séance d'avant) : oubliée
  useEffect(() => { if (cleProf && etat && etat.prof === false) { garderCleProfTel(code, ''); setCleProf(''); } }, [etat?.prof]);

  if (!code || perdue) return (
    <div className="min-h-[100dvh] bg-[#0f1a14] px-4 py-6 text-white" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <div className="mx-auto max-w-md">
        <p className="text-sm text-emerald-200/80">Moalim · Tronc Commun · Mode classe</p>
        {perdue && <p className="mt-3 rounded-lg bg-rose-900/60 p-2">Séance introuvable ou terminée : vérifie le code au tableau.</p>}
        <form className="mt-4" onSubmit={e => { e.preventDefault(); if (/^\d{4}$/.test(saisie)) { setCode(saisie); history.replaceState(null, '', `?c=${saisie}`); window.location.reload(); } }}>
          <label className="block text-lg font-semibold">Le code affiché au tableau</label>
          <div className="mt-2 flex gap-2">
            <input value={saisie} onChange={e => setSaisie(e.target.value.replace(/\D/g, '').slice(0, 4))} inputMode="numeric" placeholder="4821"
              className="min-w-0 flex-1 rounded-xl border border-white/30 bg-white/10 px-3 py-2 text-center font-mono text-3xl tracking-[0.3em] outline-none focus:border-emerald-300" />
            <button disabled={saisie.length !== 4} className="rounded-xl bg-amber-400 px-4 text-lg font-semibold text-black disabled:opacity-40">Entrer</button>
          </div>
        </form>
      </div>
    </div>
  );
  if (!etat) return <div className="grid min-h-[100dvh] place-items-center bg-[#0f1a14] p-4 text-center text-white/80">Connexion à la séance…</div>;

  const estProf = !!cleProf && etat.prof === true;
  // au départ : élève (nom une fois) ou professeur (le code de son écran)
  if (!estProf && !etat.moi) return (
    <div className="min-h-[100dvh] bg-[#0f1a14] px-4 py-5 text-white [@media(max-height:520px)]:py-2" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <div className="mx-auto max-w-xl">
        <p className="text-sm text-emerald-200/80">Moalim · Tronc Commun · Classe {code}</p>
        {!role && (<>
          <p className="mt-3 text-xl font-semibold">Qui es-tu ?</p>
          <div className="mt-3 grid gap-3 [@media(max-height:520px)]:grid-cols-2">
            <button onClick={() => setRole('eleve')} className="rounded-2xl bg-amber-400 px-4 py-5 text-xl font-bold text-black">🎒 Je suis un élève</button>
            <button onClick={() => setRole('prof')} className="rounded-2xl border-2 border-white/40 px-4 py-5 text-xl font-bold">👩‍🏫 Je suis le professeur</button>
          </div>
        </>)}
        {role === 'eleve' && (<>
          <p className="mt-3 text-lg font-semibold">Écris ton nom, une seule fois :</p>
          <div className="mt-2"><FormNom libelle="Entrer dans la séance" attente={attente} onValider={async d => {
            setErreur(''); setAttente(true);
            try { await appel(`/${code}/participant`, { method: 'POST', body: JSON.stringify(d) }, { 'X-Telephone': tel }); relire(); }
            catch (e) { setErreur((e as Error).message.replace(/^\d+$/, 'Ça n’est pas passé : réessaie.')); }
            finally { setAttente(false); }
          }} /></div>
        </>)}
        {role === 'prof' && (
          <form className="mt-3" onSubmit={e => { e.preventDefault(); if (/^\d{4}$/.test(jetonSaisi)) void relierProf(jetonSaisi); }}>
            <label className="block text-lg font-semibold">Le code du prof (sur ton écran : « 📱 Mon téléphone »)</label>
            <div className="mt-2 flex gap-2">
              <input value={jetonSaisi} onChange={e => setJetonSaisi(e.target.value.replace(/\D/g, '').slice(0, 4))} inputMode="numeric" placeholder="0000"
                className="min-w-0 flex-1 rounded-xl border border-white/30 bg-white/10 px-3 py-2 text-center font-mono text-3xl tracking-[0.3em] outline-none" />
              <button disabled={jetonSaisi.length !== 4 || attente} className="rounded-xl bg-amber-400 px-4 text-lg font-semibold text-black disabled:opacity-40">Valider</button>
            </div>
          </form>)}
        {role && <button onClick={() => { setRole(''); setErreur(''); }} className="mt-3 text-sm text-white/60 underline">← Revenir</button>}
        {erreur && <p className="mt-3 rounded-lg bg-rose-900/60 p-2">{erreur}</p>}
        <p className="mt-4 text-xs text-white/50">Ton nom sert seulement pendant ce cours : rien n’est enregistré, tout s’efface à la fin de la séance.</p>
      </div>
    </div>
  );

  const x = etat.question ? trouver(etat.question) : undefined;
  if (!x) return <div className="grid min-h-[100dvh] place-items-center bg-[#0f1a14] p-4 text-center text-white/80">Le professeur va projeter la première question.</div>;
  const { p, q } = x;
  const repondus = new Set(etat.reponses.map(r => r.eleve).filter(Boolean) as string[]);
  const eleveCible = estProf ? etat.participants.find(e => e.id === cible) : undefined;

  return (
    <div className="min-h-[100dvh] bg-[#d6d6d0] text-black" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <header className="sticky top-0 z-10 flex items-center gap-2 bg-[#0f1a14] px-3 py-1.5 text-sm text-white">
        <span className="font-semibold">Classe {code}</span>
        <span className="text-white/60">· question {q.id}</span>
        <span className="ml-auto truncate">{estProf ? '👩‍🏫 Professeur' : etat.moi ? `🎒 ${etat.moi.prenom} ${etat.moi.nom}` : ''}</span>
        {etat.correction && <span className="rounded bg-rose-200 px-2 text-xs font-semibold text-rose-950">Correction</span>}
      </header>
      <div className="mx-auto grid max-w-5xl gap-2 p-2 [@media(orientation:landscape)_and_(max-height:520px)]:grid-cols-2">
        <section className="rounded-lg bg-white p-3 shadow">
          <Enonce p={p} q={q} grand={false} correction={etat.correction} donnees={voirDonnees} />
          {(p.intro || p.tableau || p.donnees?.length) && <button onClick={() => setVoirDonnees(v => !v)} className="mt-2 rounded border border-slate-400 px-2 py-0.5 text-sm">{voirDonnees ? 'Cacher les données' : 'Voir les données du sujet'}</button>}
        </section>

        <section className="rounded-lg bg-white p-3 shadow">
          {estProf && !eleveCible ? (
            <div>
              {envoye && <p className="mb-2 rounded-lg bg-emerald-100 p-2 text-emerald-900">{envoye}</p>}
              <p className="font-semibold">Pour quel élève ? <span className="font-normal text-slate-500">({repondus.size} / {etat.participants.length} ont répondu à la {q.id})</span></p>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {etat.participants.map(e => (
                  <button key={e.id} onClick={() => { setCible(e.id); setEnvoye(''); }}
                    className={`rounded-full border-2 px-3 py-1.5 text-[15px] ${repondus.has(e.id) ? 'border-emerald-600 bg-emerald-50 text-emerald-900' : 'border-slate-400'}`}>
                    {repondus.has(e.id) ? '✓ ' : ''}{nomCourt(e, etat.participants)}</button>))}
                <button onClick={() => setNouveau(v => !v)} className="rounded-full bg-black px-3 py-1.5 text-[15px] font-semibold text-white">+ Nouvel élève</button>
              </div>
              {nouveau && <div className="mt-2 rounded-xl bg-[#0f1a14] p-3"><FormNom libelle="Ajouter et répondre pour lui" attente={attente} onValider={async d => {
                setErreur(''); setAttente(true);
                try { const e = await appel<Participant>(`/${code}/eleve`, { method: 'POST', body: JSON.stringify(d) }, entetes); setNouveau(false); setCible(e.id); setEnvoye(''); relire(); }
                catch (e) { setErreur((e as Error).message.replace(/^\d+$/, 'Ça n’est pas passé : réessaie.')); }
                finally { setAttente(false); }
              }} /></div>}
              {erreur && <p className="mt-2 text-sm text-rose-700">{erreur}</p>}
            </div>
          ) : (<>
            {eleveCible && <div className="mb-2 flex items-center gap-2 rounded-lg bg-amber-100 p-2 text-[15px]"><span className="flex-1">Feuille de <b>{eleveCible.prenom} {eleveCible.nom}</b>{repondus.has(eleveCible.id) ? ' (sa réponse sera remplacée)' : ''}</span>
              <button onClick={() => setCible('')} className="rounded border border-slate-500 px-2 text-sm">Changer d’élève</button></div>}
            <PanneauReponse key={`${cible || 'moi'}:${q.id}`} code={code} p={p} q={q} entetes={entetes} eleve={eleveCible?.id}
              e={etats[`${cible || 'moi'}:${q.id}`] || { phase: 'vide', texte: '' }}
              poser={m => setEtats(s => { const k2 = `${cible || 'moi'}:${q.id}`; return { ...s, [k2]: { ...(s[k2] || { phase: 'vide', texte: '' }), ...m } }; })}
              onLoupe={setLoupe}
              onEnvoye={estProf && eleveCible ? r => { setEnvoye(`✓ ${eleveCible.prenom} : ${r.verdictMur === 'regarder' ? 'à regarder ensemble' : `${pts(r.note || 0)} / ${pts(q.points)}`}`); setCible(''); relire(); } : undefined} />
          </>)}
        </section>

        <section className="rounded-lg bg-[#0f1a14] p-2 text-white [@media(orientation:landscape)_and_(max-height:520px)]:col-span-2">
          <p className="mb-1 text-sm font-semibold">Les réponses de la classe ({etat.reponses.length})</p>
          {etat.reponses.length ? <div className="grid gap-2 sm:grid-cols-2">{etat.reponses.map(r => <CarteReponse key={r.id} r={r} code={code} onImage={setLoupe} />)}</div>
            : <p className="text-sm text-white/60">Pas encore de réponse.</p>}
        </section>
      </div>
      {loupe && <Loupe src={loupe} onFermer={() => setLoupe('')} />}
    </div>
  );
}

/** Répondre à la question : photo de la feuille (lue, modifiable) ou réponse écrite ; corrigée ; publiée au mur. */
function PanneauReponse({ code, p, q, entetes, eleve, e, poser, onLoupe, onEnvoye }: { code: string; p: PartieExamen; q: QuestionExamen; entetes: Record<string, string>;
  eleve?: string; e: EtatTel; poser: (m: Partial<EtatTel>) => void; onLoupe: (src: string) => void; onEnvoye?: (r: Etat & { verdictMur?: VerdictMur }) => void }) {
  const trace = q.genre === 'triangle' || q.genre === 'histogramme';
  const enonceOcr = q.genre === 'qcm' || q.genre === 'vf'
    ? `${q.texte} ${q.items.map((it, k) => `${String.fromCharCode(97 + k)}) ${it.texte}${q.genre === 'qcm' ? ' ' + (it as { choix: string[] }).choix.map((c, m) => `${lettre(m)}. ${c}`).join(' ') : ''}`).join(' ')}`
    : q.texte;

  const photo = async (f: File) => {
    poser({ phase: 'lecture', erreur: undefined });
    try {
      let mini = await reduireImage(f, 480, 0.6);
      if (octets(mini) > 110_000) mini = await reduireImage(f, 360, 0.5);
      if (trace) { poser({ phase: 'relire', mini, texte: '' }); return; }
      const grande = await reduireImage(f, 1280, 0.8);
      const { texte } = await appel<{ texte: string }>(`/${code}/lire`, { method: 'POST', body: JSON.stringify({
        image_b64: grande, image_mime: 'image/jpeg', question: q.id, enonce: enonceOcr.slice(0, 1500), titre: p.titre.slice(0, 300),
        matiere: configExamen().matiere, niveau: configExamen().sujet.niveau }) });
      poser({ phase: 'relire', mini, texte, choix: q.genre === 'qcm' || q.genre === 'vf' ? choixDuTexte(q.genre, q.items.length, texte) : undefined });
    } catch (err) {
      poser({ phase: 'vide', erreur: (err as Error).message.replace(/^\d+$/, 'La photo n’a pas pu être lue : réessaie, ou écris la réponse.') });
    }
  };

  const publier = async (r: Etat & { verdictMur?: VerdictMur }, texte: string, mini?: string) => {
    poser({ phase: 'envoi', resultat: r });
    const { pertes, bien } = detailsEnListes(r);
    try {
      await appel(`/${code}/reponse`, { method: 'POST', body: JSON.stringify({
        question: q.id, texte: texte.slice(0, 3000), note: r.verdictMur === 'regarder' ? null : r.note ?? 0, sur: q.points,
        verdict: r.verdictMur || r.verdict || 'nonjuge', pertes, bien, retour: (r.retour || '').slice(0, 800), image_b64: mini || null,
        ...(eleve ? { eleve } : {}) }) }, entetes);
      poser({ phase: 'envoye', resultat: r });
      onEnvoye?.(r);
    } catch (err) {
      poser({ phase: 'relire', resultat: undefined, erreur: (err as Error).message.replace(/^\d+$/, 'L’envoi n’est pas passé : réessaie.') });
    }
  };

  const envoyer = async () => {
    const texte = e.texte.trim();
    if (q.genre === 'qcm' || q.genre === 'vf') {
      const choix = e.choix || [];
      const lu = q.items.map((_, k) => `${q.items.length > 1 ? String.fromCharCode(97 + k) + ') ' : ''}${q.genre === 'qcm' ? lettre(choix[k] as number) : choix[k] ? 'Vrai' : 'Faux'}`).join(' · ');
      return publier({ ...noterChoix(q, choix), choix }, lu, e.mini);
    }
    if (q.genre === 'valeur') return publier(jugerValeur(q, texte), texte, e.mini);
    if (trace) return publier({ fait: true, verdict: 'nonjuge', verdictMur: 'regarder', retour: 'Tracé à regarder ensemble avec la correction.' }, texte, e.mini);
    if (q.genre === 'redaction') {
      poser({ phase: 'correction', erreur: undefined });
      try {
        const r = await appel<CorrectionTuteur>(`/${code}/corriger`, { method: 'POST', body: JSON.stringify(corpsCorrection(p, q, texte)) });
        return publier(etatDeCorrection(q, texte, r), texte, e.mini);
      } catch {
        poser({ phase: 'auto' });   // le tuteur ne répond pas : on compare avec la correction
      }
    }
  };
  const autoNote = (f: number) => {
    const n = q.points * f;
    void publier({ fait: true, texte: e.texte, note: n, verdict: f === 1 ? 'juste' : f > 0 ? 'partiel' : 'faux', retour: 'Noté en comparant avec la correction.' }, e.texte.trim(), e.mini);
  };
  const reprendre = () => poser({ phase: 'vide', texte: '', choix: undefined, mini: undefined, resultat: undefined, erreur: undefined });
  const pret = q.genre === 'qcm' || q.genre === 'vf' ? (e.choix || []).every(c => c !== null && c !== undefined) && (e.choix || []).length === q.items.length
    : trace ? !!e.mini : !!e.texte.trim();
  const de = eleve ? 'sa' : 'ma';

  return (<>
    {(e.phase === 'vide' || e.phase === 'lecture') && (<>
      <label className={`block cursor-pointer rounded-xl px-4 py-4 text-center text-lg font-bold text-white [@media(max-height:520px)]:py-3 ${e.phase === 'lecture' ? 'animate-pulse bg-sky-700' : 'bg-black active:bg-slate-700'}`}>
        {e.phase === 'lecture' ? (trace ? 'Préparation…' : '📷 Lecture de la feuille…') : trace ? `📷 Photographier ${eleve ? 'son' : 'mon'} tracé` : `📷 Photographier ${de} réponse`}
        <input type="file" accept="image/*" capture="environment" className="hidden" disabled={e.phase === 'lecture'}
          onChange={ev => { const f = ev.target.files?.[0]; ev.target.value = ''; if (f) void photo(f); }} />
      </label>
      {e.phase === 'vide' && !trace && <button onClick={() => poser({ phase: 'relire', texte: '', choix: q.genre === 'qcm' || q.genre === 'vf' ? q.items.map(() => null) : undefined })}
        className="mt-2 block w-full rounded-xl border-2 border-black px-4 py-3 text-center text-lg font-bold [@media(max-height:520px)]:py-2">⌨ Écrire {de} réponse</button>}
    </>)}

    {(e.phase === 'relire' || e.phase === 'correction') && (<>
      <div className="flex gap-2">
        {e.mini && <img src={e.mini} alt="La photo" className="h-24 w-20 shrink-0 rounded border object-cover" onClick={() => onLoupe(e.mini!)} />}
        <p className="text-sm text-slate-700">{trace ? 'Le tracé part au mur, à regarder ensemble. Un mot peut l’accompagner (la texture trouvée…).' : e.mini ? 'Relis ce qui a été lu sur la feuille ; corrige si besoin, puis envoie.' : 'Écris la réponse, puis envoie.'}</p>
      </div>
      {(q.genre === 'qcm' || q.genre === 'vf') && (
        <Choix q={q} etat={{ fait: false, choix: e.choix }} onChoisir={(k, v) => poser({ choix: (e.choix || q.items.map(() => null)).map((c, m) => (m === k ? v : c)) })} />)}
      {q.genre !== 'qcm' && q.genre !== 'vf' && (
        <textarea value={e.texte} onChange={ev => poser({ texte: ev.target.value })} rows={trace ? 2 : 5} dir="auto" placeholder={trace ? 'Un mot (facultatif)' : 'La réponse'}
          className="mt-2 w-full rounded-md border border-slate-400 p-2 text-[18px] [@media(max-height:520px)]:h-24" style={{ fontFamily: CRAIE }} />)}
      <div className="mt-2 flex flex-wrap gap-2">
        <button disabled={!pret || e.phase === 'correction'} onClick={() => void envoyer()} className="rounded-lg bg-black px-5 py-2 font-semibold text-white disabled:opacity-40">
          {e.phase === 'correction' ? 'Le tuteur corrige…' : 'Envoyer'}</button>
        <button onClick={reprendre} className="rounded-lg border border-slate-400 px-3 py-2 text-sm">{e.mini ? 'Reprendre la photo' : 'Annuler'}</button>
      </div>
    </>)}

    {e.phase === 'auto' && 'correction' in q && (
      <div className="border-2 border-rose-700 p-2">
        <p className="text-sm text-slate-700">Le tuteur n’est pas joignable : compare la réponse avec la correction.</p>
        {q.correction.map((l, k) => <p key={k} className="text-[17px] text-rose-900" style={{ fontFamily: CRAIE }}><Formule t={l} /></p>)}
        <div className="mt-2 flex flex-wrap gap-2 text-sm">
          <button onClick={() => autoNote(1)} className="rounded-md border border-emerald-700 px-3 py-1 text-emerald-800">Juste</button>
          <button onClick={() => autoNote(0.5)} className="rounded-md border border-amber-600 px-3 py-1 text-amber-800">À moitié</button>
          <button onClick={() => autoNote(0)} className="rounded-md border border-rose-700 px-3 py-1 text-rose-800">Faux</button>
        </div>
      </div>)}

    {(e.phase === 'envoi' || e.phase === 'envoye') && e.resultat && (<>
      {e.resultat.verdictMur === 'regarder'
        ? <p className="rounded-md border-2 border-sky-600 bg-sky-50 p-2 text-sky-900">👀 Le tracé est au mur : on le regarde ensemble avec la correction.</p>
        : (<>
          <p className="text-xl font-bold">{eleve ? 'Sa note' : 'Ta note'} : {pts(e.resultat.note || 0)} / {pts(q.points)}</p>
          <Verdict etat={e.resultat} />
        </>)}
      <p className="mt-2 text-sm text-slate-600">{e.phase === 'envoi' ? 'Envoi au professeur…' : '✓ Réponse reçue par le professeur.'}</p>
      <div className="mt-2"><button onClick={reprendre} className="rounded-lg border border-slate-400 px-3 py-1.5 text-sm">Remplacer {de} réponse</button></div>
    </>)}
    {e.erreur && <p className="mt-2 text-sm text-rose-700">{e.erreur}</p>}
  </>);
}
