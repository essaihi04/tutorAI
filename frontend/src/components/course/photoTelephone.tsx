/**
 * « 📱 Avec mon téléphone » (24 novembre 2026) : l'élève travaille sur un PC et répond avec SON téléphone.
 *
 * Le PC ouvre un canal du relais (`/api/v1/public/relais`, en mémoire sur le serveur, 3 h sans activité au plus) : un QR
 * code, un code court de 6 caractères faciles (sans 0/O/1/I) et un lien court (moalim.online/tronc-commun/?t=K7P4QX).
 * Le téléphone le rejoint UNE SEULE FOIS (`PageTelephone`) ; ensuite il suit le PC en continu :
 *   - le PC publie sa « vue » : la question en cours (énoncé, genre, propositions), la liste des questions, le brouillon,
 *     le résultat (`useVueTelephone`, appelé par la page — l'évaluation —, et `useChampTelephone`, par le champ de réponse
 *     visible : dans le lecteur de cours, c'est lui qui donne l'énoncé) ;
 *   - le téléphone envoie des messages : aller à une question (le PC suit), le texte tapé au clavier ou lu sur la photo de
 *     la feuille (OCR sur le téléphone, texte modifiable ; il s'écrit en direct dans le champ du PC), les choix d'un QCM,
 *     « rendre » (une seule fois : la correction s'affiche sur les deux écrans).
 * Le canal est gardé dans le sessionStorage des deux côtés : un rechargement ne casse pas la liaison.
 *
 * Seulement sur les liens libres : la page du lien appelle `activerPhotoTelephone(...)` avant le premier rendu ; le lecteur
 * du site principal (élèves connectés) ne montre jamais ce choix.
 */
import { useEffect, useRef, useState, useSyncExternalStore } from 'react';
import QRCode from 'qrcode';

const API = '/api/v1/public/relais';

/** Réduit une photo de téléphone (plusieurs Mo) en JPEG : `max` px sur le grand côté. Renvoie une data URL. */
export async function reduireImage(f: Blob, max: number, qualite = 0.8): Promise<string> {
  const url = URL.createObjectURL(f);
  try {
    const img = await new Promise<HTMLImageElement>((ok, ko) => { const i = new Image(); i.onload = () => ok(i); i.onerror = ko; i.src = url; });
    const k = Math.min(1, max / Math.max(img.naturalWidth, img.naturalHeight));
    const c = document.createElement('canvas');
    c.width = Math.max(1, Math.round(img.naturalWidth * k)); c.height = Math.max(1, Math.round(img.naturalHeight * k));
    const g = c.getContext('2d')!;
    g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height);
    g.drawImage(img, 0, 0, c.width, c.height);
    return c.toDataURL('image/jpeg', qualite);
  } finally { URL.revokeObjectURL(url); }
}
/** taille en octets d'une data URL base64 */
export const octets = (dataUrl: string) => Math.floor((dataUrl.length - dataUrl.indexOf(',') - 1) * 0.75);

async function json<T>(r: Response): Promise<T> {
  if (!r.ok) {
    const d = await r.json().then((x: { detail?: unknown }) => (typeof x?.detail === 'string' ? x.detail : '')).catch(() => '');
    throw Object.assign(new Error(d || String(r.status)), { status: r.status });
  }
  return r.json() as Promise<T>;
}

let LIEN = '';
/** à appeler par la page d'un lien libre ; `lien` : l'adresse de la page (location.origin + location.pathname) */
export function activerPhotoTelephone(lien: string) { LIEN = lien; if (canal) setTimeout(demarrer, 0); }
export const photoTelephoneActive = () => !!LIEN;
/** « moalim.online/tronc-commun/?t=K7P4QX » (sans https:// : c'est ce qu'on tape) */
export const lienCourt = (code: string, base = LIEN, cle = 't') => `${base.replace(/^https?:\/\//, '').replace(/\?.*$/, '')}?${cle}=${code}`;
/** le lien complet (celui du QR code) : https://moalim.online/tronc-commun/?t=K7P4QX, ou l'adresse locale en essai */
export const lienComplet = (code: string, base = LIEN, cle = 't') => `${base.replace(/\?.*$/, '')}?${cle}=${code}`;

/** Un QR code (SVG) du lien : le téléphone le vise avec son appareil photo et ouvre la page. */
export function QrCode({ lien, className = '' }: { lien: string; className?: string }) {
  const [svg, setSvg] = useState('');
  useEffect(() => {
    let vivant = true;
    QRCode.toString(lien, { type: 'svg', margin: 1, errorCorrectionLevel: 'M', color: { dark: '#000000', light: '#ffffff' } })
      .then(s => { if (vivant) setSvg(s); }).catch(() => setSvg(''));
    return () => { vivant = false; };
  }, [lien]);
  // SVG produit par la bibliothèque à partir de notre propre lien
  return <div className={`aspect-square bg-white [&>svg]:block [&>svg]:h-full [&>svg]:w-full ${className}`} role="img" aria-label={`QR code : ${lien}`} dangerouslySetInnerHTML={{ __html: svg }} />;
}

// ── Ce qui passe dans le canal ────────────────────────────────────────────────────────────────────────────────────────

export type DetailTel = { element: string; sur: number; obtenu: number; perte?: string };
export type VueTelephone = {
  titre?: string;
  /** pour naviguer depuis le téléphone (l'évaluation) */
  questions?: { id: string; fait?: boolean }[];
  courante?: {
    id: string; partie?: string; texte: string; points?: number;
    /** texte, valeur : un champ ; qcm, vf : des boutons ; trace : à faire sur le PC ; aucune : rien à répondre */
    genre: 'texte' | 'valeur' | 'qcm' | 'vf' | 'trace' | 'aucune';
    items?: { texte: string; choix?: string[] }[]; aide?: string; matiere?: string;
  };
  brouillon?: { texte?: string; choix?: (number | boolean | null)[] };
  resultat?: { verdict?: string; note?: number; sur?: number; retour?: string; details?: DetailTel[] } | null;
  /** « Le tuteur lit ta réponse… » */
  occupe?: string;
  /** un champ de réponse est ouvert sur le PC (le texte du téléphone s'y écrit) */
  champ?: boolean;
};
export type MessageTelephone =
  | { type: 'aller'; question: string }
  | { type: 'texte'; texte: string; rendre?: boolean }
  | { type: 'choix'; choix: (number | boolean | null)[]; rendre?: boolean; question?: string };

// ── Le PC : un canal par page ─────────────────────────────────────────────────────────────────────────────────────────

type Canal = { code: string; cle: string; telephone: boolean };
type Champ = { enonce: string; texte: () => string; remplacer?: (t: string) => void; ajouter?: (t: string) => void; rendre?: (t: string) => void };
type Controleur = { vue: VueTelephone; onMessage: (m: MessageTelephone) => void };
const MEMO = 'relais-telephone-pc';
let canal: Canal | null = null;
try { const m = JSON.parse(sessionStorage.getItem(MEMO) || 'null'); if (m?.code && m?.cle) canal = { code: m.code, cle: m.cle, telephone: false }; } catch { /* rien */ }
const abonnes = new Set<() => void>();
const annoncer = () => abonnes.forEach(f => f());
const poser = (c: Canal | null) => {
  canal = c;
  try { if (c) sessionStorage.setItem(MEMO, JSON.stringify({ code: c.code, cle: c.cle })); else sessionStorage.removeItem(MEMO); } catch { /* rien */ }
  annoncer();
};
const champs: Champ[] = [];
let controleur: Controleur | null = null;
let minuteur: number | undefined;
let attentePublier: number | undefined;
let derniereVue = '';

const champ = () => champs[champs.length - 1];

function composer(): VueTelephone {
  const ch = champ();
  const base: VueTelephone = controleur?.vue
    ?? (ch ? { courante: { id: `champ-${ch.enonce.slice(0, 40)}`, texte: ch.enonce, genre: 'texte' } } : { courante: { id: 'rien', texte: '', genre: 'aucune' } });
  return { ...base, champ: !!ch, brouillon: { ...base.brouillon, ...(ch ? { texte: ch.texte() } : {}) } };
}
/** la vue part au téléphone (regroupée : 250 ms après le dernier changement) */
export function publierVue() {
  if (!canal) return;
  window.clearTimeout(attentePublier);
  attentePublier = window.setTimeout(() => {
    const c = canal;
    if (!c) return;
    const vue = composer();
    const s = JSON.stringify(vue);
    if (s === derniereVue) return;
    derniereVue = s;
    void fetch(`${API}/${c.code}/vue`, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Pc': c.cle }, body: JSON.stringify({ vue }) })
      .then(r => { if (!r.ok) derniereVue = ''; }).catch(() => { derniereVue = ''; });
  }, 250);
}

function appliquer(m: MessageTelephone) {
  if (m.type === 'texte') {
    const ch = champ();
    if (ch) {
      ch.remplacer?.(m.texte);
      if (m.rendre) { if (ch.rendre) ch.rendre(m.texte); else ch.ajouter?.(m.texte); }
      return;
    }
  }
  controleur?.onMessage(m);
}

async function interroger() {
  const c = canal;
  if (!c) return;
  try {
    const d = await json<{ messages: MessageTelephone[]; telephone: boolean }>(await fetch(`${API}/${c.code}/messages`, { headers: { 'X-Pc': c.cle } }));
    if (canal !== c) return;
    d.messages.forEach(appliquer);
    if (d.telephone !== c.telephone) poser({ ...c, telephone: d.telephone });
  } catch (e) {
    const s = (e as { status?: number }).status;
    if (s === 404 || s === 403) arreter(false);   // canal expiré : l'élève en rouvre un
  }
}
function demarrer() {
  if (minuteur || !canal || !LIEN) return;
  minuteur = window.setInterval(() => { void interroger(); }, 1200);
  derniereVue = '';
  publierVue();
  void interroger();
}
export async function ouvrirCanal(): Promise<void> {
  if (canal) { demarrer(); return; }
  const d = await json<{ code: string; cle_pc: string }>(await fetch(API, { method: 'POST' }));
  poser({ code: d.code, cle: d.cle_pc, telephone: false });
  demarrer();
}
/** « Déconnecter le téléphone » */
export function arreter(prevenir = true) {
  const c = canal;
  window.clearInterval(minuteur); minuteur = undefined;
  poser(null);
  if (c && prevenir) void fetch(`${API}/${c.code}`, { method: 'DELETE', headers: { 'X-Pc': c.cle } }).catch(() => {});
}

export function useCanal() {
  return useSyncExternalStore(f => { abonnes.add(f); return () => { abonnes.delete(f); }; }, () => canal);
}

/** La page (l'évaluation) publie ce qu'elle montre et reçoit la navigation et les choix du téléphone. */
export function useVueTelephone(vue: VueTelephone | null, onMessage: (m: MessageTelephone) => void) {
  const ref = useRef(onMessage);
  ref.current = onMessage;
  const cle = JSON.stringify(vue);
  useEffect(() => {
    if (!LIEN || !vue) return;
    controleur = { vue, onMessage: m => ref.current(m) };
    publierVue();
  }, [cle]);
  useEffect(() => () => { controleur = null; publierVue(); }, []);
}

/** Le champ de réponse visible : le texte du téléphone s'y écrit en direct ; « rendre » l'envoie. */
export function useChampTelephone(c: { enonce: string; texte: string; remplacer?: (t: string) => void; ajouter?: (t: string) => void; rendre?: (t: string) => void }, actif: boolean) {
  const ref = useRef(c);
  ref.current = c;
  useEffect(() => {
    if (!actif || !LIEN) return;
    const r: Champ = {
      enonce: c.enonce, texte: () => ref.current.texte,
      remplacer: c.remplacer && (t => ref.current.remplacer?.(t)), ajouter: c.ajouter && (t => ref.current.ajouter?.(t)), rendre: c.rendre && (t => ref.current.rendre?.(t)),
    };
    champs.push(r);
    publierVue();
    return () => { const k = champs.indexOf(r); if (k >= 0) champs.splice(k, 1); publierVue(); };
  }, [c.enonce, actif, !!c.remplacer, !!c.rendre]);
  useEffect(() => { if (actif && LIEN) publierVue(); }, [c.texte, actif]);
}

/** Le QR code, le code court et le lien à ouvrir sur le téléphone ; « Déconnecter le téléphone ». */
export function CodeTelephone({ code, telephone, onFermer, onArreter }: { code: string; telephone: boolean; onFermer: () => void; onArreter: () => void }) {
  return (
    <div className="fixed inset-x-0 bottom-3 z-[1000] mx-auto max-h-[96dvh] w-[min(94vw,460px)] overflow-y-auto rounded-2xl border border-slate-300 bg-white p-4 text-slate-900 shadow-2xl [@media(max-height:520px)]:bottom-1 [@media(max-height:520px)]:w-[min(94vw,560px)] [@media(max-height:520px)]:p-2.5"
      style={{ fontFamily: 'system-ui, sans-serif' }} role="dialog" aria-label="Relier mon téléphone">
      <div className="flex items-start gap-2">
        <p className="flex-1 text-[15px] font-semibold">📱 Réponds avec ton téléphone</p>
        <button type="button" onClick={onFermer} className="rounded px-2 text-slate-500 hover:bg-slate-100" aria-label="Fermer">✕</button>
      </div>
      {telephone ? (
        <p className="mt-2 rounded-lg bg-emerald-50 p-2 text-[15px] text-emerald-900">✓ Téléphone relié. Il suit tes questions : réponds au clavier du téléphone ou photographie ta feuille ; la réponse s’écrit ici.</p>
      ) : (
        <div className="mt-2 flex flex-col items-center gap-3 [@media(max-height:520px)]:flex-row [@media(max-height:520px)]:items-center">
          <QrCode lien={lienComplet(code)} className="w-52 rounded-lg border border-slate-200 p-1 [@media(max-height:520px)]:w-32" />
          <div className="min-w-0 flex-1 text-center">
            <p className="text-[14px] text-slate-700">Vise ce QR code avec l’appareil photo de ton téléphone (une seule fois), ou ouvre :</p>
            <p className="mt-1 select-all break-all rounded-lg bg-slate-100 px-2 py-1 font-mono text-[16px] font-semibold text-sky-800">{lienCourt(code)}</p>
            <p className="mt-1 text-[13px] text-slate-600">Code :</p>
            <p className="font-mono text-4xl font-bold tracking-[0.25em] [@media(max-height:520px)]:text-2xl" aria-label={`Code ${code.split('').join(' ')}`}>{code.slice(0, 3)} {code.slice(3)}</p>
            <p className="mt-1 animate-pulse text-[13px] text-slate-500">En attente du téléphone…</p>
          </div>
        </div>
      )}
      <div className="mt-2 flex justify-end"><button type="button" onClick={onArreter} className="rounded-md border border-rose-300 px-2 py-1 text-[13px] text-rose-700 hover:bg-rose-50">Déconnecter le téléphone</button></div>
    </div>
  );
}

/** Le bouton « 📱 Avec mon téléphone » ; il n'existe que sur les liens libres. */
export function BoutonTelephone({ petit, disabled, clair = false }: { petit?: boolean; disabled?: boolean; clair?: boolean }) {
  const c = useCanal();
  const [voir, setVoir] = useState(false);
  const [erreur, setErreur] = useState('');
  const avant = useRef(!!c?.telephone);
  // le téléphone vient de se relier : la carte du code se referme d'elle-même
  useEffect(() => {
    const vient = !!c?.telephone && !avant.current;
    avant.current = !!c?.telephone;
    if (vient && voir) { const t = window.setTimeout(() => setVoir(false), 2500); return () => window.clearTimeout(t); }
  }, [c?.telephone, voir]);
  if (!LIEN) return null;
  const fond = c?.telephone ? 'bg-emerald-600 text-white' : clair ? 'border border-slate-400 bg-white text-slate-900 hover:bg-slate-100' : 'bg-white/10 hover:bg-white/20';
  return (<>
    <button type="button" disabled={disabled}
      onClick={async () => { setErreur(''); try { await ouvrirCanal(); setVoir(true); } catch (e) { setErreur((e as Error).message.replace(/^\d+$/, 'Connexion impossible pour l’instant.')); } }}
      className={`shrink-0 rounded-full ${petit ? 'px-3 py-1 text-xs' : 'px-3 py-1.5 text-sm'} ${fond} disabled:opacity-40`}
      style={{ fontFamily: 'system-ui, sans-serif' }} title="Répondre avec ton téléphone (clavier ou photo de ta feuille)">
      {c?.telephone ? '📱 Téléphone relié' : c ? `📱 ${c.code}` : '📱 Avec mon téléphone'}
    </button>
    {erreur && <span className="text-xs text-rose-600">{erreur}</span>}
    {voir && c && <CodeTelephone code={c.code} telephone={c.telephone} onFermer={() => setVoir(false)} onArreter={() => { arreter(); setVoir(false); }} />}
  </>);
}

// ── Le téléphone : ?t=K7P4QX ──────────────────────────────────────────────────────────────────────────────────────────

const propre = (s: string) => s.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 6);
const MEMO_TEL = 'relais-telephone';
const VERDICTS: Record<string, [string, string]> = {
  juste: ['✔ Juste', 'border-emerald-500 bg-emerald-900/40'], partiel: ['◐ Juste en partie', 'border-amber-400 bg-amber-900/40'],
  faux: ['✘ Faux', 'border-rose-500 bg-rose-900/40'], nonjuge: ['? Pas jugé', 'border-slate-400 bg-white/5'],
};
const virgule = (x: number) => String(Math.round(x * 100) / 100).replace('.', ',');

/** La photo de la feuille, lue sur le téléphone : la page du lien libre envoie `/course-player/ocr-reponse` à sa route publique. */
async function lireFeuille(f: File, enonce: string, matiere?: string): Promise<string> {
  let img = await reduireImage(f, 1600, 0.82);
  if (octets(img) > 2_500_000) img = await reduireImage(f, 1200, 0.7);
  const d = await json<{ texte: string }>(await fetch('/api/v1/course-player/ocr-reponse', { method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_b64: img, image_mime: 'image/jpeg', enonce: enonce.slice(0, 600), matiere: matiere || '' }) }));
  return (d.texte || '').trim();
}

/** La page du téléphone : elle suit le PC (même question), on y répond au clavier ou en photo ; jamais de nouveau code. */
export function PageTelephone({ code: initial, titre = 'Moalim' }: { code: string; titre?: string }) {
  const [code, setCode] = useState(() => { let c = propre(initial); try { if (!c) c = sessionStorage.getItem(MEMO_TEL) || ''; } catch { /* rien */ } return c; });
  const [saisie, setSaisie] = useState('');
  const [vue, setVue] = useState<VueTelephone | null>(null);
  const [erreur, setErreur] = useState('');
  const [texte, setTexte] = useState('');
  const [choix, setChoix] = useState<(number | boolean | null)[]>([]);
  const [lecture, setLecture] = useState(false);
  const [rendu, setRendu] = useState('');
  const version = useRef(0);
  const champ = useRef<HTMLTextAreaElement>(null);
  const attente = useRef<number | undefined>(undefined);

  useEffect(() => {
    if (code.length !== 6) return;
    try { sessionStorage.setItem(MEMO_TEL, code); } catch { /* rien */ }
    if (!new URLSearchParams(location.search).get('t')) history.replaceState(null, '', `?t=${code}`);
    let fini = false;
    version.current = 0;
    const lire = async () => {
      try {
        const d = await json<{ version: number; vue?: VueTelephone; inchange?: boolean }>(await fetch(`${API}/${code}?v=${version.current}`));
        if (fini || d.inchange) return;
        version.current = d.version; setVue(d.vue || {}); setErreur('');
      } catch (e) {
        if (fini) return;
        if ((e as { status?: number }).status === 404) {
          setVue(null); setCode(''); setErreur('Liaison terminée ou code inconnu : ouvre « 📱 Avec mon téléphone » sur ton PC et vise le nouveau QR code.');
          try { sessionStorage.removeItem(MEMO_TEL); } catch { /* rien */ }
        }
      }
    };
    void lire();
    const t = window.setInterval(() => { void lire(); }, 1300);
    return () => { fini = true; window.clearInterval(t); };
  }, [code]);

  const envoyer = async (m: MessageTelephone) => {
    try { await json(await fetch(`${API}/${code}/message`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: m }) })); setErreur(''); }
    catch (e) { setErreur((e as Error).message.replace(/^\d+$/, 'Le message n’est pas parti : vérifie ta connexion.')); }
  };
  const q = vue?.courante;
  // une autre question : le champ repart du brouillon du PC
  useEffect(() => {
    setTexte(vue?.brouillon?.texte || '');
    setChoix(vue?.brouillon?.choix || (q?.items || []).map(() => null));
    setRendu('');
  }, [q?.id]);
  // le PC a écrit dans son champ : on le reprend, sauf pendant la frappe sur le téléphone
  useEffect(() => {
    const b = vue?.brouillon?.texte;
    if (b != null && document.activeElement !== champ.current && attente.current === undefined) setTexte(b);
    if (vue?.brouillon?.choix) setChoix(vue.brouillon.choix);
  }, [vue?.brouillon?.texte, JSON.stringify(vue?.brouillon?.choix)]);

  const taper = (t: string) => {
    setTexte(t);
    window.clearTimeout(attente.current);
    attente.current = window.setTimeout(() => { attente.current = undefined; void envoyer({ type: 'texte', texte: t }); }, 450);
  };
  const photo = async (f: File) => {
    setLecture(true); setErreur('');
    try {
      const items = (q?.items || []).map((it, j) => `${String.fromCharCode(97 + j)}) ${it.texte}${it.choix ? ' ' + it.choix.map((c, m) => `${String.fromCharCode(65 + m)}. ${c}`).join(' ') : ''}`).join(' ');
      const lu = await lireFeuille(f, [q?.texte || '', items].filter(Boolean).join(' '), q?.matiere);
      if (!lu) { setErreur('Rien de lisible sur la photo : reprends-la de plus près, bien éclairée.'); return; }
      if (q?.genre === 'qcm' || q?.genre === 'vf') {
        const c = choixDuTexte(q.genre, q.items?.length || 0, lu);
        setChoix(c); void envoyer({ type: 'choix', choix: c, question: q?.id });
      } else taper([texte.trim(), lu].filter(Boolean).join('\n'));
    } catch (e) {
      setErreur((e as Error).message.replace(/^\d+$/, 'La photo n’a pas pu être lue : réessaie, ou écris ta réponse.'));
    } finally { setLecture(false); }
  };
  const rendre = () => {
    window.clearTimeout(attente.current); attente.current = undefined;
    setRendu('Envoyé…');
    void envoyer(q?.genre === 'qcm' || q?.genre === 'vf' ? { type: 'choix', choix, rendre: true, question: q.id } : { type: 'texte', texte, rendre: true });
  };

  if (code.length !== 6) return (
    <Cadre titre={titre}>
      <form className="mt-4" onSubmit={e => { e.preventDefault(); setErreur(''); setCode(propre(saisie)); }}>
        <label className="block text-lg font-semibold">Tape le code affiché sur ton PC</label>
        <div className="mt-2 flex gap-2">
          <input value={saisie} onChange={e => setSaisie(propre(e.target.value))} autoCapitalize="characters" autoComplete="off" spellCheck={false}
            placeholder="K7P4QX" className="min-w-0 flex-1 rounded-xl border border-white/30 bg-white/10 px-3 py-2 text-center font-mono text-3xl tracking-[0.2em] outline-none focus:border-emerald-300" />
          <button disabled={saisie.length !== 6} className="rounded-xl bg-emerald-500 px-4 text-lg font-semibold text-black disabled:opacity-40">Relier</button>
        </div>
      </form>
      {erreur && <p className="mt-3 rounded-lg bg-rose-900/60 p-2 text-[15px] text-rose-100">{erreur}</p>}
    </Cadre>
  );

  const qs = vue?.questions || [];
  const k = qs.findIndex(x => x.id === q?.id);
  const r = vue?.resultat;
  const choixComplets = choix.length === (q?.items?.length || 0) && choix.every(c => c !== null && c !== undefined);
  return (
    <Cadre titre={titre} code={code}>
      {!!qs.length && (
        <div className="mt-1 flex items-center gap-1.5">
          <button disabled={k <= 0} onClick={() => void envoyer({ type: 'aller', question: qs[k - 1].id })} className="rounded-lg border border-white/30 px-3 py-1.5 disabled:opacity-30" aria-label="Question précédente">←</button>
          <select value={q?.id || ''} onChange={e => void envoyer({ type: 'aller', question: e.target.value })} className="min-w-0 flex-1 rounded-lg border border-white/30 bg-[#12301f] px-2 py-1.5">
            {qs.map(x => <option key={x.id} value={x.id}>Question {x.id}{x.fait ? ' ✔' : ''}</option>)}
          </select>
          <button disabled={k < 0 || k >= qs.length - 1} onClick={() => void envoyer({ type: 'aller', question: qs[k + 1].id })} className="rounded-lg border border-white/30 px-3 py-1.5 disabled:opacity-30" aria-label="Question suivante">→</button>
        </div>)}
      <div className="mt-2 grid gap-2 [@media(orientation:landscape)_and_(max-height:520px)]:grid-cols-2">
        <div className="rounded-xl border border-white/15 bg-white/5 p-3">
          {q?.partie && <p className="text-xs text-white/60">{q.partie}</p>}
          <p className="text-[17px] leading-snug">{q?.texte || 'Ouvre une question sur ton PC : elle s’affichera ici.'}{q?.points ? <span className="ml-2 rounded border border-white/40 px-1 text-xs">{virgule(q.points)} pt</span> : null}</p>
        </div>
        <div>
          {vue?.occupe && <p className="animate-pulse rounded-lg bg-sky-900/60 p-2 text-[15px]">{vue.occupe}</p>}
          {r ? (
            <div className={`rounded-xl border-2 p-3 ${(VERDICTS[r.verdict || 'nonjuge'] || VERDICTS.nonjuge)[1]}`}>
              <p className="font-bold">{(VERDICTS[r.verdict || 'nonjuge'] || VERDICTS.nonjuge)[0]}{r.note != null && r.sur != null ? ` · ${virgule(r.note)} / ${virgule(r.sur)}` : ''}</p>
              {r.retour && <p className="mt-1 text-[15px]">{r.retour}</p>}
              {!!r.details?.length && <ul className="mt-1 space-y-0.5 text-[14px]">{r.details.map((d, j) => (
                <li key={j} className={d.obtenu >= d.sur ? 'text-emerald-200' : 'text-rose-200'}>{d.obtenu >= d.sur ? '✓' : '✘'} {d.element} — {virgule(d.obtenu)} / {virgule(d.sur)}{d.obtenu < d.sur && d.perte ? ` (${d.perte})` : ''}</li>))}</ul>}
              <p className="mt-1 text-xs text-white/60">La correction complète est sur ton PC.</p>
            </div>
          ) : q && (q.genre === 'qcm' || q.genre === 'vf') ? (<>
            <ol className="space-y-2">{(q.items || []).map((it, j) => (
              <li key={j} className="rounded-lg bg-white/5 p-2">
                <p className="text-[15px]">{(q.items || []).length > 1 && <b>{String.fromCharCode(97 + j)}) </b>}{it.texte}</p>
                <div className="mt-1 flex flex-wrap gap-1.5">
                  {(q.genre === 'qcm' ? (it.choix || []).map((c, m) => ({ v: m as number | boolean, t: `${String.fromCharCode(65 + m)}. ${c}` })) : [{ v: true, t: 'Vrai' }, { v: false, t: 'Faux' }]).map(o => (
                    <button key={String(o.v)} onClick={() => { const c = (choix.length ? choix : (q.items || []).map(() => null)).map((x, m) => (m === j ? o.v : x)); setChoix(c); void envoyer({ type: 'choix', choix: c, question: q?.id }); }}
                      className={`rounded-md border px-2.5 py-1.5 text-left text-[15px] ${choix[j] === o.v ? 'border-emerald-300 bg-emerald-500 text-black' : 'border-white/30'}`}>{o.t}</button>))}
                </div>
              </li>))}</ol>
            <BoutonsReponse lecture={lecture} onPhoto={photo} onRendre={rendre} pret={choixComplets} rendu={rendu} />
          </>) : q && (q.genre === 'texte' || q.genre === 'valeur') ? (<>
            <textarea ref={champ} value={texte} onChange={e => taper(e.target.value)} rows={q.genre === 'valeur' ? 3 : 6} dir="auto"
              placeholder={q.aide || (q.genre === 'valeur' ? 'Relation = … = résultat avec son unité' : 'Ta réponse…')}
              className="w-full rounded-xl border border-white/30 bg-white px-3 py-2 text-[18px] text-black outline-none focus:border-emerald-300 [@media(max-height:520px)]:h-[5.5rem] [@media(max-height:520px)]:text-[16px]" />
            {vue?.champ === false && <p className="text-xs text-amber-200">Ouvre le champ de réponse sur ton PC pour que ta réponse s’y écrive.</p>}
            <BoutonsReponse lecture={lecture} onPhoto={photo} onRendre={rendre} pret={!!texte.trim() && vue?.champ !== false} rendu={rendu} />
          </>) : q?.genre === 'trace' ? <p className="rounded-lg bg-white/5 p-2 text-[15px]">Cette question se trace sur le PC (à la souris ou au doigt).</p> : null}
        </div>
      </div>
      {erreur && <p className="mt-3 rounded-lg bg-rose-900/60 p-2 text-[15px] text-rose-100">{erreur}</p>}
    </Cadre>
  );
}

function Cadre({ titre, code, children }: { titre: string; code?: string; children: React.ReactNode }) {
  return (
    <div className="min-h-[100dvh] bg-[#0f1a14] px-3 py-3 text-white [@media(max-height:520px)]:py-1.5" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <div className="mx-auto max-w-3xl">
        <p className="text-sm text-emerald-200/80">{titre} · 📱 {code ? `relié au PC (${code})` : 'répondre pour mon PC'}</p>
        {children}
        <p className="mt-3 text-xs text-white/45">Rien n’est gardé : ta réponse va à ton PC, la photo est oubliée après la lecture.</p>
      </div>
    </div>
  );
}

function BoutonsReponse({ lecture, onPhoto, onRendre, pret, rendu }: { lecture: boolean; onPhoto: (f: File) => void; onRendre: () => void; pret: boolean; rendu: string }) {
  return (
    <div className="mt-2 flex flex-wrap items-center gap-2">
      <label className={`cursor-pointer rounded-xl px-4 py-2.5 [@media(max-height:520px)]:py-1.5 text-[16px] font-semibold ${lecture ? 'animate-pulse bg-sky-700' : 'bg-white/15 active:bg-white/25'}`}>
        {lecture ? '📷 Lecture de la feuille…' : '📷 Photographier ma feuille'}
        <input type="file" accept="image/*" capture="environment" className="hidden" disabled={lecture} onChange={e => { const f = e.target.files?.[0]; e.target.value = ''; if (f) onPhoto(f); }} />
      </label>
      <button disabled={!pret || !!rendu} onClick={onRendre} className="rounded-xl bg-emerald-500 px-4 py-2.5 [@media(max-height:520px)]:py-1.5 text-[16px] font-bold text-black disabled:opacity-40">{rendu || 'Rendre ma réponse'}</button>
    </div>
  );
}

/** QCM / vrai-faux : les choix lus sur la feuille (« a) B ; b) C … » ou « B C C B ») ; l'élève les vérifie en touchant. */
export function choixDuTexte(genre: 'qcm' | 'vf', n: number, texte: string): (number | boolean | null)[] {
  const lire = (l: string): number | boolean | null => {
    if (genre === 'vf') { const m = l.match(/\b(vrai|faux|v|f)\b/i); return m ? /^v/i.test(m[1]) : null; }
    const m = l.match(/\b([A-D])\b/) || l.match(/\b([a-d])\b/);
    return m ? m[1].toUpperCase().charCodeAt(0) - 65 : null;
  };
  const lignes = texte.split(/[\n;]+/).map(l => l.replace(/^\s*(?:\d+[-.)]\s*)?[a-h]\s*[).:-]\s*/i, '')).filter(l => l.trim());
  let out = lignes.map(lire).filter(x => x !== null);
  if (out.length < n) {
    const tous = genre === 'vf' ? [...texte.matchAll(/\b(vrai|faux|v|f)\b/gi)].map(m => /^v/i.test(m[1]))
      : [...texte.matchAll(/\b([A-D])\b/g)].map(m => m[1].charCodeAt(0) - 65);
    if (tous.length >= out.length) out = tous;
  }
  return Array.from({ length: n }, (_, k) => (out[k] ?? null) as number | boolean | null);
}
