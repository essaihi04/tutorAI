/**
 * Le mode classe (24 novembre 2026) : l'évaluation formative projetée en classe, question par question.
 *
 *   - `?classe`    l'écran du professeur (projeté) : code et QR code, la question projetée, le mur des réponses corrigées,
 *                  les compteurs, « Montrer la correction » ;
 *   - `?c=<code>`  le téléphone (de l'élève, ou du prof pour la feuille d'un élève) : la question projetée (suit le prof),
 *                  « 📷 Photographier ma réponse », le texte lu modifiable, « Envoyer », la note, puis les réponses des
 *                  camarades, anonymes.
 *
 * Ni nom, ni fiche, ni suivi, ni enregistrement : la séance vit en mémoire sur le serveur (`/api/v1/public/classe`) et
 * disparaît. La correction reprend celle de l'évaluation (`Examen.tsx`) : QCM, vrai/faux et valeurs notés dans le
 * navigateur, rédactions par le tuteur sur le barème ; triangle et histogramme : la photo du tracé part au mur
 * « à regarder ensemble ».
 */
import { useEffect, useRef, useState } from 'react';
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

type VerdictMur = 'juste' | 'partiel' | 'faux' | 'nonjuge' | 'regarder';
type ReponseMur = { id: string; numero: number; question: string; texte: string; note: number | null; sur: number; verdict: VerdictMur;
  pertes: string[]; bien: string[]; retour: string; image: boolean; mien: boolean };
type EtatSeance = { code: string; version: number; question: string; correction: boolean; reponses: ReponseMur[]; par_question: Record<string, number> };

async function appel<T>(chemin: string, init: RequestInit = {}, entetes: Record<string, string> = {}): Promise<T> {
  const r = await fetch(`${API}${chemin}`, { ...init, headers: { 'Content-Type': 'application/json', ...entetes } });
  if (!r.ok) {
    const d = await r.json().then((x: { detail?: unknown }) => (typeof x?.detail === 'string' ? x.detail : '')).catch(() => '');
    throw Object.assign(new Error(d || String(r.status)), { status: r.status });
  }
  return r.json() as Promise<T>;
}

/** L'état de la séance, interrogé toutes les 2,5 s (rien n'est renvoyé si rien n'a changé). */
function useSeance(code: string, telephone = '') {
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
        const d = await appel<EtatSeance & { inchange?: boolean }>(`/${code}?v=${version.current}`, {}, telephone ? { 'X-Telephone': telephone } : {});
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
  }, [code, telephone, tick]);
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
          <li>Chaque élève vise le QR code (ou tape le lien et le code) avec son téléphone, et photographie sa feuille — ou toi, avec ton téléphone, pour la feuille d’un élève.</li>
          <li>La réponse est lue et corrigée (note, éléments du barème perdus) et apparaît ici, sans nom.</li>
          <li>« Montrer la correction » : la correction s’affiche au tableau et sur les téléphones.</li>
        </ol>
        <p className="mt-3 text-[15px] text-white/60">Rien n’est enregistré : ni nom, ni photo, ni note. La séance s’efface quand tu la termines (ou après 4 h sans activité).</p>
        <button onClick={() => void commencer()} className="mt-5 rounded-xl bg-amber-400 px-6 py-3 text-xl font-bold text-black hover:bg-amber-300">Commencer une séance</button>
        {erreur && <p className="mt-3 text-rose-300">{erreur}</p>}
      </div>
    </div>
  );
  return <SeanceProf prof={prof} onFin={() => garder(null)} />;
}

function SeanceProf({ prof, onFin }: { prof: Prof; onFin: () => void }) {
  const { etat, perdue, relire } = useSeance(prof.code);
  const [loupe, setLoupe] = useState('');
  // au début de la séance, le QR s'affiche en grand : toute la classe le vise depuis sa place (une seule fois)
  const [qrGrand, setQrGrand] = useState(true);
  const [donnees, setDonnees] = useState(true);
  const X = { 'X-Prof': prof.cle };
  const qs = configExamen().questions;
  const k = Math.max(0, qs.findIndex(x => x.q.id === etat?.question));
  const { p, q } = qs[k];
  useEffect(() => { if (perdue) onFin(); }, [perdue]);
  const aller = async (id: string) => { await appel(`/${prof.code}/question`, { method: 'POST', body: JSON.stringify({ question: id }) }, X).catch(() => {}); relire(); };
  const montrer = async (m: boolean) => { await appel(`/${prof.code}/correction`, { method: 'POST', body: JSON.stringify({ montrer: m }) }, X).catch(() => {}); relire(); };
  const terminer = async () => {
    if (!window.confirm('Terminer la séance ? Toutes les réponses seront effacées.')) return;
    await appel(`/${prof.code}`, { method: 'DELETE' }, X).catch(() => {});
    onFin();
  };
  const rs = etat?.reponses || [];
  const n = compter(rs);
  const lien = lienComplet(prof.code, PAGE(), 'c');
  const BTN = 'rounded-lg border border-white/30 px-3 py-1.5 text-[clamp(14px,1.1vw,18px)] hover:bg-white/10 disabled:opacity-30';

  return (
    <div className="flex min-h-[100dvh] flex-col bg-[#0f1a14] text-white lg:h-[100dvh]" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <header className="flex shrink-0 flex-wrap items-center gap-x-4 gap-y-2 border-b border-white/15 px-3 py-2">
        <button onClick={() => setQrGrand(true)} title="QR code en grand"><QrCode lien={lien} className="w-[clamp(72px,8vw,132px)] rounded" /></button>
        <div className="min-w-0">
          <p className="text-[clamp(14px,1.1vw,20px)] text-white/70">Sur ton téléphone : <b className="font-mono text-white">{lienCourt(prof.code, PAGE(), 'c')}</b></p>
          <p className="font-mono text-[clamp(34px,4vw,72px)] font-bold leading-none tracking-[0.2em] text-amber-300">{prof.code}</p>
        </div>
        <div className="ml-auto flex flex-wrap items-center gap-2">
          <button className={BTN} disabled={k === 0} onClick={() => void aller(qs[k - 1].q.id)}>← Précédente</button>
          <select value={q.id} onChange={e => void aller(e.target.value)} className="rounded-lg border border-white/30 bg-[#12301f] px-2 py-1.5 text-[clamp(14px,1.1vw,18px)]">
            {qs.map(x => <option key={x.q.id} value={x.q.id}>Question {x.q.id}{etat?.par_question[x.q.id] ? ` · ${etat.par_question[x.q.id]} rép.` : ''}</option>)}
          </select>
          <button className={BTN} disabled={k === qs.length - 1} onClick={() => void aller(qs[k + 1].q.id)}>Suivante →</button>
          <button onClick={() => void montrer(!etat?.correction)} className={`rounded-lg px-3 py-1.5 text-[clamp(14px,1.1vw,18px)] font-semibold ${etat?.correction ? 'bg-rose-200 text-rose-950' : 'bg-amber-400 text-black'}`}>
            {etat?.correction ? 'Cacher la correction' : 'Montrer la correction'}</button>
          <button onClick={() => void terminer()} className="rounded-lg border border-rose-300/60 px-3 py-1.5 text-[clamp(13px,1vw,16px)] text-rose-200 hover:bg-rose-500/20">Terminer</button>
        </div>
      </header>

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
            <span className="rounded-lg bg-white/10 px-3 py-1">Réponses : <b>{n.recues}</b></span>
            <span className="rounded-lg bg-emerald-700/70 px-3 py-1">✔ Justes : <b>{n.justes}</b></span>
            <span className="rounded-lg bg-amber-600/70 px-3 py-1">◐ Partielles : <b>{n.partielles}</b></span>
            <span className="rounded-lg bg-rose-700/70 px-3 py-1">✘ Fausses : <b>{n.fausses}</b></span>
            {!!n.regarder && <span className="rounded-lg bg-sky-700/70 px-3 py-1">👀 À regarder : <b>{n.regarder}</b></span>}
          </div>
          <div className="mt-2 min-h-0 flex-1 overflow-y-auto">
            {rs.length ? (
              <div className="grid gap-2 [grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr))]">
                {rs.map(r => <CarteReponse key={r.id} r={r} code={prof.code} grand onImage={setLoupe}
                  onRetirer={() => { if (window.confirm(`Retirer la réponse ${r.numero} du mur ?`)) void appel(`/${prof.code}/reponse/${r.id}`, { method: 'DELETE' }, X).then(relire).catch(() => {}); }} />)}
              </div>
            ) : <p className="mt-6 text-center text-[clamp(16px,1.4vw,24px)] text-white/60">Les réponses photographiées apparaîtront ici, sans nom.</p>}
          </div>
        </section>
      </div>
      {loupe && <Loupe src={loupe} onFermer={() => setLoupe('')} />}
      {qrGrand && (
        <div className="fixed inset-0 z-[1000] flex flex-col items-center justify-center gap-4 bg-white p-4 text-black" onClick={() => setQrGrand(false)} role="dialog" aria-label="QR code en grand">
          <QrCode lien={lien} className="w-[min(62vh,80vw)]" />
          <p className="text-[clamp(18px,2vw,32px)] font-semibold">Visez ce QR code avec votre téléphone, une seule fois</p>
          <p className="font-mono text-[clamp(20px,3vw,44px)]">{lienCourt(prof.code, PAGE(), 'c')} · code <b>{prof.code}</b></p>
          <p className="text-sm text-slate-500">Touchez l’écran pour afficher la question (le QR reste en haut à gauche ; touchez-le pour le revoir en grand)</p>
        </div>)}
    </div>
  );
}

// ── Le téléphone ──────────────────────────────────────────────────────────────────────────────────────────────────────

const MEMO_TEL = 'classe-telephone';
const nouvelId = () => crypto.randomUUID?.() || `t-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 12)}`;
function idTelephone(neuf = false) {
  try {
    let t = neuf ? '' : sessionStorage.getItem(MEMO_TEL) || '';
    if (!t) { t = nouvelId(); sessionStorage.setItem(MEMO_TEL, t); }
    return t;
  } catch { return nouvelId(); }
}

type Phase = 'vide' | 'lecture' | 'relire' | 'correction' | 'auto' | 'envoi' | 'envoye';
type EtatTel = { phase: Phase; texte: string; choix?: (number | boolean | null)[]; mini?: string; resultat?: Etat & { verdictMur?: VerdictMur }; erreur?: string };

function detailsEnListes(e: Etat) {
  const d = e.details || [];
  return {
    pertes: d.filter(x => x.obtenu < x.sur).map(x => `${x.element} : −${pts(x.sur - x.obtenu)}${x.perte ? ` (${x.perte})` : ''}`),
    bien: d.filter(x => x.obtenu >= x.sur && x.sur > 0).map(x => x.element),
  };
}

export function TelephoneClasse({ code: initial }: { code: string }) {
  const [code, setCode] = useState(/^\d{4}$/.test(initial) ? initial : '');
  const [saisie, setSaisie] = useState('');
  const [tel, setTel] = useState(() => idTelephone());
  const { etat, perdue } = useSeance(code, tel);
  const [etats, setEtats] = useState<Record<string, EtatTel>>({});
  const [loupe, setLoupe] = useState('');
  const [voirDonnees, setVoirDonnees] = useState(false);
  const x = etat?.question ? trouver(etat.question) : undefined;

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
  if (!etat || !x) return <div className="grid min-h-[100dvh] place-items-center bg-[#0f1a14] p-4 text-center text-white/80">{etat ? 'Le professeur va projeter la première question.' : 'Connexion à la séance…'}</div>;

  const { p, q } = x;
  const e: EtatTel = etats[q.id] || { phase: 'vide', texte: '' };
  const poser = (m: Partial<EtatTel>) => setEtats(s => ({ ...s, [q.id]: { ...(s[q.id] || { phase: 'vide', texte: '' }), ...m } }));
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
      poser({ phase: 'vide', erreur: (err as Error).message.replace(/^\d+$/, 'La photo n’a pas pu être lue : réessaie, ou écris ta réponse.') });
    }
  };

  const publier = async (r: Etat & { verdictMur?: VerdictMur }, texte: string, mini?: string) => {
    poser({ phase: 'envoi', resultat: r });
    const { pertes, bien } = detailsEnListes(r);
    try {
      await appel(`/${code}/reponse`, { method: 'POST', body: JSON.stringify({
        question: q.id, texte: texte.slice(0, 3000), note: r.verdictMur === 'regarder' ? null : r.note ?? 0, sur: q.points,
        verdict: r.verdictMur || r.verdict || 'nonjuge', pertes, bien, retour: (r.retour || '').slice(0, 800), image_b64: mini || null }) }, { 'X-Telephone': tel });
      poser({ phase: 'envoye', resultat: r });
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
        poser({ phase: 'auto' });   // le tuteur ne répond pas : l'élève compare avec la correction
      }
    }
  };
  const autoNote = (f: number) => {
    const n = q.points * f;
    void publier({ fait: true, texte: e.texte, note: n, verdict: f === 1 ? 'juste' : f > 0 ? 'partiel' : 'faux', retour: 'Noté par l’élève en comparant avec la correction.' }, e.texte.trim(), e.mini);
  };
  const reprendre = (autre = false) => {
    if (autre) setTel(idTelephone(true));
    poser({ phase: 'vide', texte: '', choix: undefined, mini: undefined, resultat: undefined, erreur: undefined });
  };
  const pret = q.genre === 'qcm' || q.genre === 'vf' ? (e.choix || []).every(c => c !== null && c !== undefined) && (e.choix || []).length === q.items.length
    : trace ? !!e.mini : !!e.texte.trim();
  const autres = etat.reponses;

  return (
    <div className="min-h-[100dvh] bg-[#d6d6d0] text-black" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <header className="sticky top-0 z-10 flex items-center gap-2 bg-[#0f1a14] px-3 py-1.5 text-sm text-white">
        <span className="font-semibold">Classe {code}</span>
        <span className="text-white/60">· question {q.id}</span>
        {etat.correction && <span className="ml-auto rounded bg-rose-200 px-2 text-xs font-semibold text-rose-950">Correction au tableau</span>}
      </header>
      <div className="mx-auto grid max-w-5xl gap-2 p-2 [@media(orientation:landscape)_and_(max-height:520px)]:grid-cols-2">
        <section className="rounded-lg bg-white p-3 shadow">
          <Enonce p={p} q={q} grand={false} correction={etat.correction} donnees={voirDonnees} />
          {(p.intro || p.tableau || p.donnees?.length) && <button onClick={() => setVoirDonnees(v => !v)} className="mt-2 rounded border border-slate-400 px-2 py-0.5 text-sm">{voirDonnees ? 'Cacher les données' : 'Voir les données du sujet'}</button>}
        </section>

        <section className="rounded-lg bg-white p-3 shadow">
          {(e.phase === 'vide' || e.phase === 'lecture') && (<>
            <label className={`block cursor-pointer rounded-xl px-4 py-4 text-center text-lg font-bold text-white ${e.phase === 'lecture' ? 'animate-pulse bg-sky-700' : 'bg-black active:bg-slate-700'}`}>
              {e.phase === 'lecture' ? (trace ? 'Préparation…' : '📷 Lecture de la feuille…') : trace ? '📷 Photographier mon tracé' : '📷 Photographier ma réponse'}
              <input type="file" accept="image/*" capture="environment" className="hidden" disabled={e.phase === 'lecture'}
                onChange={ev => { const f = ev.target.files?.[0]; ev.target.value = ''; if (f) void photo(f); }} />
            </label>
            {e.phase === 'vide' && !trace && <button onClick={() => poser({ phase: 'relire', texte: '', choix: q.genre === 'qcm' || q.genre === 'vf' ? q.items.map(() => null) : undefined })}
              className="mt-2 block w-full rounded-xl border-2 border-black px-4 py-3 text-center text-lg font-bold">⌨ Écrire ma réponse</button>}
          </>)}

          {(e.phase === 'relire' || e.phase === 'correction') && (<>
            <div className="flex gap-2">
              {e.mini && <img src={e.mini} alt="Ta photo" className="h-24 w-20 shrink-0 rounded border object-cover" onClick={() => setLoupe(e.mini!)} />}
              <p className="text-sm text-slate-700">{trace ? 'Ton tracé part au mur, à regarder ensemble. Tu peux ajouter un mot (la texture trouvée…).' : e.mini ? 'Relis ce qui a été lu sur ta feuille ; corrige si besoin, puis envoie.' : 'Écris ta réponse, puis envoie.'}</p>
            </div>
            {(q.genre === 'qcm' || q.genre === 'vf') && (
              <Choix q={q} etat={{ fait: false, choix: e.choix }} onChoisir={(k, v) => poser({ choix: (e.choix || q.items.map(() => null)).map((c, m) => (m === k ? v : c)) })} />)}
            {q.genre !== 'qcm' && q.genre !== 'vf' && (
              <textarea value={e.texte} onChange={ev => poser({ texte: ev.target.value })} rows={trace ? 2 : 5} dir="auto" placeholder={trace ? 'Un mot (facultatif)' : 'Ta réponse'}
                className="mt-2 w-full rounded-md border border-slate-400 p-2 text-[18px]" style={{ fontFamily: CRAIE }} />)}
            <div className="mt-2 flex flex-wrap gap-2">
              <button disabled={!pret || e.phase === 'correction'} onClick={() => void envoyer()} className="rounded-lg bg-black px-5 py-2 font-semibold text-white disabled:opacity-40">
                {e.phase === 'correction' ? 'Le tuteur corrige…' : 'Envoyer'}</button>
              <button onClick={() => reprendre()} className="rounded-lg border border-slate-400 px-3 py-2 text-sm">{e.mini ? 'Reprendre la photo' : 'Annuler'}</button>
            </div>
          </>)}

          {e.phase === 'auto' && 'correction' in q && (
            <div className="border-2 border-rose-700 p-2">
              <p className="text-sm text-slate-700">Le tuteur n’est pas joignable : compare ta réponse avec la correction.</p>
              {q.correction.map((l, k) => <p key={k} className="text-[17px] text-rose-900" style={{ fontFamily: CRAIE }}><Formule t={l} /></p>)}
              <div className="mt-2 flex flex-wrap gap-2 text-sm">
                <button onClick={() => autoNote(1)} className="rounded-md border border-emerald-700 px-3 py-1 text-emerald-800">J’avais juste</button>
                <button onClick={() => autoNote(0.5)} className="rounded-md border border-amber-600 px-3 py-1 text-amber-800">À moitié</button>
                <button onClick={() => autoNote(0)} className="rounded-md border border-rose-700 px-3 py-1 text-rose-800">Je m’étais trompé</button>
              </div>
            </div>)}

          {(e.phase === 'envoi' || e.phase === 'envoye') && e.resultat && (<>
            {e.resultat.verdictMur === 'regarder'
              ? <p className="rounded-md border-2 border-sky-600 bg-sky-50 p-2 text-sky-900">👀 Ton tracé est au mur : on le regarde ensemble avec la correction.</p>
              : (<>
                <p className="text-xl font-bold">Ta note : {pts(e.resultat.note || 0)} / {pts(q.points)}</p>
                <Verdict etat={e.resultat} />
              </>)}
            <p className="mt-2 text-sm text-slate-600">{e.phase === 'envoi' ? 'Envoi au tableau…' : '✓ Ta réponse est au tableau (sans ton nom).'}</p>
            <div className="mt-2 flex flex-wrap gap-2">
              <button onClick={() => reprendre()} className="rounded-lg border border-slate-400 px-3 py-1.5 text-sm">Remplacer ma réponse</button>
              <button onClick={() => reprendre(true)} className="rounded-lg border border-slate-400 px-3 py-1.5 text-sm" title="Pour le prof qui photographie les copies">📷 Feuille d’un autre élève</button>
            </div>
          </>)}
          {e.erreur && <p className="mt-2 text-sm text-rose-700">{e.erreur}</p>}
        </section>

        <section className="rounded-lg bg-[#0f1a14] p-2 text-white [@media(orientation:landscape)_and_(max-height:520px)]:col-span-2">
          <p className="mb-1 text-sm font-semibold">Les réponses de la classe ({autres.length})</p>
          {autres.length ? <div className="grid gap-2 sm:grid-cols-2">{autres.map(r => <CarteReponse key={r.id} r={r} code={code} onImage={setLoupe} />)}</div>
            : <p className="text-sm text-white/60">Pas encore de réponse.</p>}
        </section>
      </div>
      {loupe && <Loupe src={loupe} onFermer={() => setLoupe('')} />}
    </div>
  );
}

